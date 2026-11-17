"""
Kraken public-OHLCV fallback for the §21 crypto allowlist (CLAUDE.md), added
2026-11-17 at explicit user instruction after TradingView (TRADING_VIEW_2)
introduced a daily MCP call quota effective 2026-11-17 and the crypto lane's
structure pipeline (Stage B) hit it mid-session with no non-TradingView path
for crypto (unlike equities, which already fall back to Robinhood's own
get_equity_historicals/get_equity_technical_indicators).

Scope, stated plainly because this module is easy to over-build:
  - This is a DATA SOURCE only. It fetches and validates OHLCV bars from
    Kraken's public (unauthenticated, read-only) REST API and hands them back
    in the exact same bar-dict shape ({"t","o","h","l","c","v"}) that
    tv_structure.py already consumes from TRADING_VIEW_2 — so every existing
    indicator/structure/sizing function in tv_structure.py (completed_bars,
    ema, rsi14, macd, atr14, volume_baseline_13h, swing_points, pullback_depth,
    atr_target, risk_reward, validate_stop_distance, finalize_candidate, ...)
    works UNCHANGED on Kraken-sourced bars. Nothing in tv_structure.py was
    modified to build this.
  - It does NOT change any §21 gate item, risk number, position cap, R:R
    floor, confirmation count, or allowlist. It does NOT grant, remove, or
    alter any order-placement authority. It never calls a broker or
    order-placing tool, and never will (no network call in this module
    targets Robinhood or any order-placement endpoint).
  - It is NOT wired into any live scheduled-trigger prompt by this change. A
    trigger only starts using it once that is a separate, explicit, approved
    step (see the "Approval needed before enabling" note this module's
    author reports alongside this file) — this module existing and passing
    its own tests does not, by itself, change what any cycle actually does.
  - Unsupported or invalid pairs, and genuinely stale/missing data, resolve
    to a DATA_BLOCKED-shaped result — never silently treated as NO_TRADE
    (a real gate rejection) and never silently treated as a valid read.

Verified live, 2026-11-17 (see data_budget.py's companion module for the
call-budget/cache logic that decides WHEN this module's fetch function is
even invoked):
  - Kraken's public AssetPairs endpoint confirms all 8 names on the current
    §21 allowlist are live, online pairs quoted in USD: AAVEUSD, AVAXUSD,
    HBARUSD, LINKUSD, SOLUSD, XETHZUSD (ETH), XXBTZUSD (BTC), XXRPZUSD (XRP).
  - A real OHLC fetch (AAVEUSD, interval=60) returned 721 real 1h bars with no
    `error` entries; the most recent bar's own start time was still inside its
    own still-open hour relative to request time — i.e. Kraken's OHLC
    endpoint, like TradingView's, includes the forming candle and the caller
    must exclude it via the existing completed_bars() no-lookahead logic, not
    a new one.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Callable, List, Optional, Sequence

# --- Pair mapping, verified live 2026-11-17 via Kraken's public AssetPairs
# endpoint (see module docstring) — not assumed, not guessed. A symbol absent
# from this map is UNSUPPORTED and must resolve to DATA_BLOCKED, never to a
# silently-skipped pair or a fabricated price.
KRAKEN_PAIR_MAP = {
    "BTC": "XXBTZUSD",
    "ETH": "XETHZUSD",
    "SOL": "SOLUSD",
    "XRP": "XXRPZUSD",
    "LINK": "LINKUSD",
    "AAVE": "AAVEUSD",
    "HBAR": "HBARUSD",
    "AVAX": "AVAXUSD",
}

# Only these two timeframes are in scope for this repair, matching the §21
# Stage B pipeline (4H setup + 1H execution trigger) exactly — no 1m/5m/1D
# support is added here.
KRAKEN_INTERVAL_MINUTES = {"1h": 60, "4h": 240}
KRAKEN_INTERVAL_SECONDS = {"1h": 3600, "4h": 14400}

KRAKEN_OHLC_URL = "https://api.kraken.com/0/public/OHLC"

# A Kraken OHLC row with a gap bigger than this many whole bar-intervals
# between it and the previous row is flagged — Kraken's public feed is read
# directly from its own matching engine and does not guarantee a bar for
# every interval on a thinly-traded pair; a genuine gap must be visible to
# the caller, never silently smoothed over.
MAX_UNFLAGGED_GAP_INTERVALS = 1


def kraken_pair_for(symbol: str) -> Optional[str]:
    """Returns the Kraken pair code for a §21 allowlist symbol, or None if unsupported."""
    return KRAKEN_PAIR_MAP.get(symbol.upper())


def parse_kraken_ohlc_rows(rows: Sequence[Sequence], interval_seconds: int) -> dict:
    """
    Pure parser: Kraken's own OHLC row shape is
    [time, open, high, low, close, vwap, volume, count] (all strings except
    time/count). Converts to the bar-dict shape tv_structure.py already
    expects ({"t": int, "o": float, "h": float, "l": float, "c": float,
    "v": float}), sorted by t, and flags any gap wider than
    MAX_UNFLAGGED_GAP_INTERVALS whole intervals between consecutive rows.

    No network access, no file I/O — safe to unit-test with fixture rows.

    Returns {"bars": [...], "gaps": [{"after_t", "before_t", "missing_intervals"}]}.
    """
    parsed = []
    for row in rows:
        t, o, h, l, c = int(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4])
        v = float(row[6]) if len(row) > 6 else 0.0
        parsed.append({"t": t, "o": o, "h": h, "l": l, "c": c, "v": v})
    parsed.sort(key=lambda b: b["t"])

    gaps = []
    for prev, cur in zip(parsed, parsed[1:]):
        delta = cur["t"] - prev["t"]
        missing = round(delta / interval_seconds) - 1
        if missing > MAX_UNFLAGGED_GAP_INTERVALS - 1 and missing > 0:
            gaps.append({"after_t": prev["t"], "before_t": cur["t"], "missing_intervals": missing})

    return {"bars": parsed, "gaps": gaps}


def validate_kraken_bars(
    bars: Sequence[dict],
    interval_seconds: int,
    now_epoch: float,
    min_completed_bars: int = 20,
) -> dict:
    """
    Pure validation, no network access. Excludes the forming candle via the
    SAME tv_structure.completed_bars() logic every TradingView-sourced pull
    already uses (imported here, not reimplemented) — Kraken and TradingView
    bars are validated identically once parsed into the shared bar-dict shape.

    Freshness check mirrors the existing TRADING_VIEW_2 recovery-verification
    rule (CLAUDE.md §21 outage-reporting section): the most recent COMPLETED
    bar must satisfy t >= now_epoch - 2*interval_seconds (no more than one
    full bar-period of slack beyond the bar that should have just closed) —
    a same-calendar-date check is never used for a 24/7 market.

    Returns {"ok": bool, "reason": str|None, "completed": [Bar,...]} — "completed"
    is the list of tv_structure.Bar objects (never raw dicts) once ok is True;
    empty/absent when ok is False.
    """
    from dev_scanner.tv_structure import completed_bars  # local import: no import-time coupling

    if not bars:
        return {"ok": False, "reason": "no_bars_returned", "completed": []}

    completed = completed_bars(bars, interval_seconds, now_epoch)
    if len(completed) < min_completed_bars:
        return {
            "ok": False,
            "reason": f"insufficient_completed_history ({len(completed)} < {min_completed_bars})",
            "completed": [],
        }

    most_recent = completed[-1]
    if most_recent.t < now_epoch - 2 * interval_seconds:
        return {
            "ok": False,
            "reason": f"stale_data (most recent completed bar t={most_recent.t}, now={now_epoch}, "
            f"gap={now_epoch - most_recent.t}s exceeds 2x interval {2 * interval_seconds}s)",
            "completed": [],
        }

    return {"ok": True, "reason": None, "completed": completed}


def _default_http_get(url: str, timeout: float = 15.0) -> dict:
    """Real network call — isolated here so every other function stays unit-testable without it."""
    req = urllib.request.Request(url, headers={"User-Agent": "agentic-trading-kraken-fallback/1"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def fetch_kraken_ohlc(
    symbol: str,
    interval: str,
    now_epoch: Optional[float] = None,
    min_completed_bars: int = 20,
    http_get: Optional[Callable[[str], dict]] = None,
) -> dict:
    """
    End-to-end fetch + parse + validate for one §21 allowlist symbol and one
    of the two supported timeframes ("1h" or "4h"). This is the one function
    a trigger cycle (or data_budget.get_structure_bars, see that module)
    calls to get real, completed, gap-checked Kraken bars.

    Returns one of:
      {"status": "UNSUPPORTED_PAIR", "symbol": ..., "interval": ...}
      {"status": "UNSUPPORTED_INTERVAL", "symbol": ..., "interval": ...}
      {"status": "FETCH_ERROR", "symbol": ..., "interval": ..., "error": str}
      {"status": "DATA_BLOCKED", "symbol": ..., "interval": ..., "reason": str, "gaps": [...]}
      {"status": "OK", "symbol": ..., "interval": ..., "pair": ..., "bars": [Bar,...], "gaps": [...]}

    "DATA_BLOCKED" (insufficient history, stale data, or a flagged gap inside
    the required lookback) is a DISTINCT outcome from "UNSUPPORTED_PAIR" — both
    must be reported as data problems, never as a gate rejection (NO_TRADE)
    and never silently treated as a clean read.
    """
    interval = interval.lower()
    if interval not in KRAKEN_INTERVAL_MINUTES:
        return {"status": "UNSUPPORTED_INTERVAL", "symbol": symbol, "interval": interval}

    pair = kraken_pair_for(symbol)
    if pair is None:
        return {"status": "UNSUPPORTED_PAIR", "symbol": symbol, "interval": interval}

    getter = http_get or _default_http_get
    minutes = KRAKEN_INTERVAL_MINUTES[interval]
    interval_seconds = KRAKEN_INTERVAL_SECONDS[interval]
    url = f"{KRAKEN_OHLC_URL}?pair={pair}&interval={minutes}"

    try:
        raw = getter(url)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"status": "FETCH_ERROR", "symbol": symbol, "interval": interval, "error": str(exc)}

    if not isinstance(raw, dict):
        return {"status": "FETCH_ERROR", "symbol": symbol, "interval": interval, "error": "non-dict response"}

    kraken_errors = raw.get("error") or []
    if kraken_errors:
        return {"status": "FETCH_ERROR", "symbol": symbol, "interval": interval, "error": "; ".join(kraken_errors)}

    result = raw.get("result") or {}
    rows = result.get(pair)
    if rows is None:
        return {"status": "FETCH_ERROR", "symbol": symbol, "interval": interval,
                 "error": f"Kraken response missing result[{pair!r}] — keys were {list(result.keys())!r}"}

    parsed = parse_kraken_ohlc_rows(rows, interval_seconds)
    now = now_epoch if now_epoch is not None else time.time()
    validation = validate_kraken_bars(parsed["bars"], interval_seconds, now, min_completed_bars)

    # A flagged gap inside the actual lookback we'll use (the trailing
    # min_completed_bars completed bars) is itself a data-quality problem,
    # not something the caller should silently compute indicators through —
    # recent-gap-aware, not "any gap anywhere in 721 bars of history".
    if validation["ok"]:
        completed_ts = {b.t for b in validation["completed"][-min_completed_bars:]}
        recent_gaps = [g for g in parsed["gaps"] if g["before_t"] in completed_ts or g["after_t"] in completed_ts]
        if recent_gaps:
            return {
                "status": "DATA_BLOCKED",
                "symbol": symbol,
                "interval": interval,
                "reason": f"gap detected inside the required lookback window: {recent_gaps}",
                "gaps": recent_gaps,
            }
        return {
            "status": "OK",
            "symbol": symbol,
            "interval": interval,
            "pair": pair,
            "bars": validation["completed"],
            "gaps": parsed["gaps"],
        }

    return {
        "status": "DATA_BLOCKED",
        "symbol": symbol,
        "interval": interval,
        "reason": validation["reason"],
        "gaps": parsed["gaps"],
    }
