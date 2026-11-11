"""
Reusable structure/indicator/sizing calculations for TRADING_VIEW_2-sourced OHLCV bars.

This module exists to close a real gap found 2026-11-11: trigger prompts for the
First Scan, Fresh Candle, and Crypto 24/7 routines repeatedly reference a
"tv_structure.py" module (completed_bars/ema/rsi14/macd/atr14/volume_baseline_13h/
swing_points/pullback_depth/atr_target/risk_reward/validate_stop_distance/
position_size) as already "built and live-verified." No such file existed anywhere
in this repository, its git history, or any scratchpad before this commit — every
cycle this session actually computed stops/R:R/ATR by hand, inline, per name, via
ad-hoc Python. This module is the real implementation those trigger prompts
describe, built and tested now so future cycles can call one reviewed,
version-controlled function set instead of re-deriving the arithmetic each time.

Pure functions only: no network calls, no broker access, no file I/O, no order
placement. It only computes numbers from bars already fetched elsewhere.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence

REGULAR_SESSION_SECONDS = 23400  # 6.5h, 9:30am-4:00pm ET


@dataclass(frozen=True)
class Bar:
    t: int
    o: float
    h: float
    l: float
    c: float
    v: float = 0.0


def _as_bars(bars: Sequence[dict]) -> List[Bar]:
    return [Bar(t=b["t"], o=b["o"], h=b["h"], l=b["l"], c=b["c"], v=b.get("v", 0.0)) for b in bars]


def completed_bars(
    bars: Sequence[dict],
    interval_seconds: int,
    now_epoch: float,
    last_bar_duration_seconds: Optional[int] = None,
) -> List[Bar]:
    """
    Drop any bar that has not actually finished as of now_epoch.

    A bar at time t has finished once t + interval_seconds <= now_epoch, EXCEPT
    the single most-recently-started bar, whose true completion event may differ
    from a flat interval (e.g. a daily equity bar completes at the regular
    session's close, ~23400s after a 9:30am ET open, not a full 24h later).
    last_bar_duration_seconds overrides the interval for that one most-recent bar
    only; every earlier bar already has a later bar after it and is judged by the
    flat interval_seconds rule regardless (that later bar's own existence proves
    the earlier one closed).
    """
    parsed = sorted(_as_bars(bars), key=lambda b: b.t)
    out: List[Bar] = []
    n = len(parsed)
    for i, b in enumerate(parsed):
        is_last = i == n - 1
        dur = last_bar_duration_seconds if (is_last and last_bar_duration_seconds is not None) else interval_seconds
        if b.t + dur <= now_epoch:
            out.append(b)
    return out


def ema(closes: Sequence[float], period: int) -> Optional[float]:
    if len(closes) < period:
        return None
    k = 2 / (period + 1)
    e = sum(closes[:period]) / period
    for c in closes[period:]:
        e = c * k + e * (1 - k)
    return e


def rsi14(closes: Sequence[float], period: int = 14) -> Optional[float]:
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def macd(closes: Sequence[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Optional[dict]:
    if len(closes) < slow + signal:
        return None
    macd_series = []
    for end in range(slow, len(closes) + 1):
        window = closes[:end]
        ef = ema(window, fast)
        es = ema(window, slow)
        if ef is None or es is None:
            continue
        macd_series.append(ef - es)
    if len(macd_series) < signal:
        return None
    signal_line = ema(macd_series, signal)
    if signal_line is None:
        return None
    return {"macd": macd_series[-1], "signal": signal_line, "hist": macd_series[-1] - signal_line}


def atr14(bars: Sequence[Bar], period: int = 14) -> Optional[float]:
    if len(bars) < period + 1:
        return None
    trs = []
    for i in range(1, len(bars)):
        h, l, pc = bars[i].h, bars[i].l, bars[i - 1].c
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    if len(trs) < period:
        return None
    return sum(trs[-period:]) / period


def volume_baseline_13h(bars: Sequence[Bar], as_of_index: int, lookback: int = 3) -> Optional[dict]:
    """
    §13.H: "normal" volume for the bar at as_of_index is the average volume of the
    `lookback` (default 3) most recently COMPLETED bars immediately preceding it,
    same timeframe, no lookahead. Returns {"baseline": float, "sample_size": int}
    with sample_size < lookback flagged explicitly when fewer prior bars exist
    (minimum 1); the name is kept for continuity with the trigger prompts' own
    existing field name, not a literal "13 hour" window.
    """
    if as_of_index <= 0:
        return None
    start = max(0, as_of_index - lookback)
    prior = bars[start:as_of_index]
    if not prior:
        return None
    return {"baseline": sum(b.v for b in prior) / len(prior), "sample_size": len(prior)}


def swing_points(bars: Sequence[Bar], as_of_index: int, lookback: int = 5) -> dict:
    """
    Symmetric 5-bar (default) fractal lookback over bars[:as_of_index+1]. Returns
    the highest high and lowest low within the trailing `lookback` completed bars
    up to and including as_of_index, plus whether the as_of_index bar's own close
    broke past that prior range (for the §13.G breakout-continuation path).
    as_of_index must be the CURRENT completed-bar index — never a later one (no
    backdating a pivot to before it was actually confirmable).
    """
    if as_of_index < 0 or as_of_index >= len(bars):
        raise ValueError("as_of_index out of range")
    window_start = max(0, as_of_index - lookback + 1)
    window = bars[window_start : as_of_index + 1]
    # prior_window excludes the current bar itself — a breakout is measured
    # against what came BEFORE this bar, never including this bar's own high/low.
    prior_window = bars[max(0, as_of_index - lookback) : as_of_index] or window[:-1] or window
    swing_high = max(b.h for b in window)
    swing_low = min(b.l for b in window)
    prior_high = max(b.h for b in prior_window)
    prior_low = min(b.l for b in prior_window)
    current_close = bars[as_of_index].c
    return {
        "swing_high": swing_high,
        "swing_low": swing_low,
        "current_above_prior_swing_high": current_close > prior_high,
        "current_below_prior_swing_low": current_close < prior_low,
        "prior_swing_high": prior_high,
        "prior_swing_low": prior_low,
    }


def pullback_depth(bars: Sequence[Bar], as_of_index: int, lookback: int = 5) -> Optional[dict]:
    """
    Detects a pullback-to-swing structure (NOT breakout/retest or range
    contraction — those are checked separately via swing_points). Returns None
    when no clean impulse-then-pullback leg is identifiable in the lookback
    window; callers must not treat None as proof no other permitted entry method
    exists (per §13.G/the 2026-11-11 correction) — check swing_points() for a
    breakout/retest read before concluding "no computable entry."
    """
    if as_of_index < lookback:
        return None
    window = bars[as_of_index - lookback + 1 : as_of_index + 1]
    impulse_high = max(b.h for b in window[:-1]) if len(window) > 1 else None
    impulse_low = min(b.l for b in window[:-1]) if len(window) > 1 else None
    current = window[-1]
    if impulse_high is None or impulse_low is None or impulse_high == impulse_low:
        return None
    depth_from_high = (impulse_high - current.l) / (impulse_high - impulse_low) if impulse_high != impulse_low else None
    if depth_from_high is None or not (0 < depth_from_high < 1):
        return None
    return {
        "impulse_high": impulse_high,
        "impulse_low": impulse_low,
        "pullback_low": current.l,
        "depth_pct": depth_from_high * 100,
    }


def atr_target(entry: float, atr_value: float, direction: str, multiple: float = 1.5) -> float:
    """§13.F ATR_TARGET: entry +/- multiple*ATR, used when no real structural target exists."""
    if direction not in ("long", "short"):
        raise ValueError("direction must be 'long' or 'short'")
    return entry + multiple * atr_value if direction == "long" else entry - multiple * atr_value


def risk_reward(entry: float, stop: float, target: float, direction: str) -> Optional[float]:
    if direction == "long":
        risk = entry - stop
        reward = target - entry
    elif direction == "short":
        risk = stop - entry
        reward = entry - target
    else:
        raise ValueError("direction must be 'long' or 'short'")
    if risk <= 0:
        return None
    return reward / risk


def validate_stop_distance(entry: float, stop: float, atr_value: float, ceiling_multiple: float) -> dict:
    """
    Two independent checks, never merged into one:
    - exceeds_ceiling: the stop is genuinely too wide for the given ceiling_multiple
      of ATR (or ceiling_multiple itself can already be a flat %-of-entry when the
      caller passes atr_value as a flat distance basis instead) — a hard reject.
    - needs_structural_justification: the stop sits closer than 0.5x ATR to entry —
      a FLAG only, never an auto-reject, never a reason to widen the stop.
    """
    distance = abs(entry - stop)
    ceiling = ceiling_multiple * atr_value
    return {
        "distance": distance,
        "distance_pct_of_entry": distance / entry * 100 if entry else None,
        "ceiling": ceiling,
        "exceeds_ceiling": distance > ceiling,
        "needs_structural_justification": distance < 0.5 * atr_value,
    }


def orb_breakout(
    bars: Sequence[Bar],
    session_start_index: int,
    as_of_index: int,
    volume_lookback: int = 3,
    min_volume_multiple: float = 1.2,
) -> dict:
    """
    §20 item 5 Opening Range Breakout, hourly-adapted — corrected 2026-11-11: the
    qualifying breakout candle is NEVER assumed to be the second bar. The opening
    range is bars[session_start_index] (the session's first completed hourly bar).
    This scans every completed bar after it, in chronological order up to
    as_of_index, for the FIRST one whose close breaks the opening range's high
    (long) or low (short) with volume >= min_volume_multiple times the §13.H
    baseline (volume_baseline_13h) computed at that bar — whichever bar that
    actually is: second, third, fourth, or later. "Only one ORB attempt per name
    per day" means once a qualifying bar is found, no further bars are scanned
    for a new breakout that day on this symbol.

    Returns a dict:
      - opening_range_high / opening_range_low
      - breakout_bar_index / breakout_bar_t / breakout_direction: the qualifying
        bar, or None/None/None if no completed bar so far qualifies
      - is_fresh: True only if the qualifying bar IS as_of_index (the most
        recently completed bar — actionable this cycle). False means a real
        breakout occurred on an earlier bar that was never evaluated while it
        was fresh; the caller logs this as MISSED_NOT_EVALUATED, never as a
        setup rejection.
      - no_breakout_yet: True if every completed bar scanned stayed inside the
        opening range — not a rejection, a later completed bar may still break
        out on a future cycle.
    """
    if session_start_index < 0 or session_start_index >= len(bars):
        raise ValueError("session_start_index out of range")
    if as_of_index < session_start_index or as_of_index >= len(bars):
        raise ValueError("as_of_index out of range")
    opening = bars[session_start_index]
    or_high, or_low = opening.h, opening.l
    for i in range(session_start_index + 1, as_of_index + 1):
        bar = bars[i]
        vb = volume_baseline_13h(bars, as_of_index=i, lookback=volume_lookback)
        vol_ok = vb is not None and bar.v >= min_volume_multiple * vb["baseline"]
        if vol_ok and bar.c > or_high:
            direction = "long"
        elif vol_ok and bar.c < or_low:
            direction = "short"
        else:
            continue
        return {
            "opening_range_high": or_high,
            "opening_range_low": or_low,
            "breakout_bar_index": i,
            "breakout_bar_t": bar.t,
            "breakout_direction": direction,
            "is_fresh": i == as_of_index,
            "no_breakout_yet": False,
        }
    return {
        "opening_range_high": or_high,
        "opening_range_low": or_low,
        "breakout_bar_index": None,
        "breakout_bar_t": None,
        "breakout_direction": None,
        "is_fresh": False,
        "no_breakout_yet": True,
    }


def allocate_scan_budget(
    total_calls: int,
    etf_calls_needed: int,
    mode_c_calls_needed: int,
    options_leaps_calls_needed: int,
    mode_b_default_calls: int,
) -> dict:
    """
    Read-only scanner call-budget allocation (added 2026-11-11, extended
    2026-11-11 later the same day to add the options_leaps_calls_needed
    reservation — see CLAUDE.md §12 change log, "options/LEAPS scheduled
    research coverage repair") — governs how many TradingView calls a single
    screening cycle spends where, within the SAME existing per-cycle budget
    (never a larger one). No order, risk, or schedule effect of any kind.

    Priority order, applied after mandatory account/protection checks (assumed
    already spent before this is called):
      1. The mandatory §22 leveraged/inverse-ETF screen — etf_calls_needed calls,
         funded first and in full, never reduced.
      2. Time-sensitive Mode C setup evaluation — up to mode_c_calls_needed calls,
         reserved next, before the broad Mode B swing rotation.
      3. §18 item 11 / §19 item 8 options/LEAPS candidate sourcing — up to
         options_leaps_calls_needed calls, reserved next — this is the real gap
         being closed: options/LEAPS sourcing was previously only ever evaluated
         out of whatever was left after the Mode B equity rotation, which let it
         silently disappear entirely on a tight-budget cycle with no distinct
         record of that happening. Giving it its own reservation, ranked ahead of
         Mode B, means it can only be reduced below what it asked for if the
         higher-priority ETF/Mode C reservations above it already exhausted the
         total — and that specific case is flagged explicitly via
         `options_leaps_deferred`, never silently zeroed.
      4. The ordinary Mode B rotation — whatever remains, capped at
         mode_b_default_calls; this is the bucket that absorbs any shortfall.

    Returns {"etf_calls", "mode_c_calls", "options_leaps_calls", "mode_b_calls",
    "mode_b_deferred", "options_leaps_deferred"} — each `_deferred` flag is True
    whenever that bucket ended up below what it asked for because the budget
    ran out before reaching it.
    """
    remaining = max(0, total_calls)
    etf_calls = min(etf_calls_needed, remaining)
    remaining -= etf_calls
    mode_c_calls = min(mode_c_calls_needed, remaining)
    remaining -= mode_c_calls
    options_leaps_calls = min(options_leaps_calls_needed, remaining)
    remaining -= options_leaps_calls
    mode_b_calls = min(mode_b_default_calls, remaining)
    return {
        "etf_calls": etf_calls,
        "mode_c_calls": mode_c_calls,
        "options_leaps_calls": options_leaps_calls,
        "mode_b_calls": mode_b_calls,
        "mode_b_deferred": mode_b_calls < mode_b_default_calls,
        "options_leaps_deferred": options_leaps_calls < options_leaps_calls_needed,
    }


_OPTIONS_LEAPS_SOURCING_LABELS = {"evaluated", "rejected", "data_blocked", "deferred"}


def validate_options_leaps_sourcing_label(label: str) -> bool:
    """
    §18 item 11 / §19 item 8 per-symbol sourcing coverage uses exactly these
    four distinct labels, never conflated: "evaluated" (a real chain pull and
    gate check happened this cycle), "rejected" (evaluated and failed a named
    gate item — cite it), "data_blocked" (a tool failure prevented evaluation —
    never logged as a rejection), "deferred" (rotation/budget didn't reach this
    symbol this cycle — never logged as a rejection or a tool failure). Returns
    True only for one of these four exact strings.
    """
    return label in _OPTIONS_LEAPS_SOURCING_LABELS


def rotate_options_leaps_sourcing_queue(
    persisted_last_sourced: dict,
    universe: Sequence[str],
    max_slots: int,
) -> dict:
    """
    Deterministic least-recently-sourced-first rotation + persistence for
    options/LEAPS candidate sourcing (§18 item 11/§19 item 8) — added
    2026-11-11 so coverage survives across cycles instead of silently
    restarting from nothing (or silently never reaching a name) whenever the
    Mode B equity rotation crowds it out. A symbol with no entry in
    persisted_last_sourced (never sourced) ranks oldest and is always picked
    before any symbol that already has a real timestamp, regardless of how
    old that timestamp is.

    persisted_last_sourced: {symbol: iso_timestamp_str} — the queue state
      carried over from the prior cycle (e.g. persisted in near_miss_queue.md's
      "Options/LEAPS Sourcing Queue" table). A symbol absent from this dict has
      never been sourced.
    universe: every symbol currently eligible for options/LEAPS sourcing this
      cycle (e.g. watchlist.md plus any earnings-calendar/politician-trade/
      elevated-IV names already surfaced this cycle).
    max_slots: this cycle's reserved budget for sourcing, in symbols (not raw
      tool calls — the caller converts from options_leaps_calls above).

    Returns {"selected": [...], "deferred": [...]} — selected is ordered
    oldest-first, length <= min(max_slots, len(universe)). This function does
    not mutate persisted_last_sourced or decide labels — the caller sources
    each selected symbol, logs its evaluated/rejected/data_blocked label via
    validate_options_leaps_sourcing_label(), updates that symbol's timestamp to
    the current cycle's time, and persists the updated dict.
    """
    def sort_key(sym: str):
        ts = persisted_last_sourced.get(sym)
        return ("", sym) if ts is None else (str(ts), sym)

    ordered = sorted(universe, key=sort_key)
    slots = max(0, max_slots)
    return {"selected": ordered[:slots], "deferred": ordered[slots:]}


def validate_vertical_spread(
    spread_type: str,
    long_strike: float,
    short_strike: float,
    net_debit: float,
) -> dict:
    """
    Structural validation for a two-leg vertical debit spread (CLAUDE.md §24) —
    bull call (long lower strike call + short higher strike call) or bear put
    (long higher strike put + short lower strike put), same underlying/expiration,
    equal quantity both legs, net debit only. Never a credit spread, ratio spread,
    calendar, or any other multi-leg structure — those stay prohibited regardless
    of what this function returns; it only validates the two permitted shapes.

    Returns {"valid", "reason" (None if valid), "width", "max_loss_per_spread",
    "max_profit_per_spread"} — width/max_loss/max_profit are per single spread
    unit; the caller applies the contract multiplier and quantity separately via
    vertical_spread_max_loss()/vertical_spread_position_size().
    """
    if spread_type not in ("bull_call", "bear_put"):
        return {"valid": False, "reason": f"unsupported spread_type {spread_type!r} — only bull_call/bear_put permitted",
                "width": None, "max_loss_per_spread": None, "max_profit_per_spread": None}
    if spread_type == "bull_call" and not (long_strike < short_strike):
        return {"valid": False, "reason": "bull call spread requires long_strike < short_strike",
                "width": None, "max_loss_per_spread": None, "max_profit_per_spread": None}
    if spread_type == "bear_put" and not (long_strike > short_strike):
        return {"valid": False, "reason": "bear put spread requires long_strike > short_strike",
                "width": None, "max_loss_per_spread": None, "max_profit_per_spread": None}
    width = abs(long_strike - short_strike)
    if not (0 < net_debit < width):
        return {"valid": False,
                "reason": f"net_debit must be a positive debit strictly less than the spread width ({width}) — got {net_debit}",
                "width": width, "max_loss_per_spread": None, "max_profit_per_spread": None}
    return {
        "valid": True,
        "reason": None,
        "width": width,
        "max_loss_per_spread": net_debit,
        "max_profit_per_spread": width - net_debit,
    }


def vertical_spread_max_loss(net_debit: float, quantity: int, multiplier: float = 100.0, fees: float = 0.0) -> float:
    """
    §24 risk computation: the full contractual max loss, counted in full toward
    per-trade risk (§16 item 2 analog) and the §3 portfolio heat cap — never
    reduced by an assumed stop or by current moneyness. A debit spread has no
    stop mechanism; its worst case is always the full net debit paid, for as long
    as the position is open, regardless of today's mark-to-market P&L.
    """
    return net_debit * multiplier * quantity + fees


def vertical_spread_risk_reward(net_debit: float, width: float) -> Optional[float]:
    """R:R computed on the spread's own economics: (width - net_debit) / net_debit."""
    if net_debit <= 0:
        return None
    reward = width - net_debit
    if reward <= 0:
        return None
    return reward / net_debit


def vertical_spread_position_size(risk_dollars: float, net_debit: float, multiplier: float = 100.0) -> Optional[int]:
    """
    Whole spreads only, rounded down. Returns None (NO_TRADE) the moment even one
    spread's max loss (net_debit * multiplier) exceeds risk_dollars — never widen
    the debit, never substitute a fractional spread, never round up.
    """
    if net_debit <= 0:
        return None
    per_spread_loss = net_debit * multiplier
    if per_spread_loss <= 0:
        return None
    qty = int(risk_dollars // per_spread_loss)
    return qty if qty >= 1 else None


def reconcile_vertical_spread_positions(recorded: dict, positions: Sequence[dict]) -> dict:
    """
    Deterministic, read-only reconciliation of a recorded vertical-debit-spread
    (CLAUDE.md §24 item 7) against actual broker position data. Matches ONLY by
    exact `option_id` equality — never by strike/expiration proximity or any
    other heuristic. A position whose option_id doesn't exactly equal one of the
    two recorded leg ids is never assumed to belong to this spread, no matter how
    similar it looks (same underlying, adjacent strike, etc.) — "never guess
    pairings" is the entire point of this function.

    recorded: {"long_option_id": str, "short_option_id": str, "quantity": int}
      — the two leg ids and the equal per-leg quantity this spread was opened
      with (both legs always have the same quantity by definition of a vertical).
    positions: sequence of dicts shaped like get_option_positions entries, each
      with at least {"option_id": str, "quantity": float, "type": "long"|"short"}
      — only nonzero positions should be passed in (filter before calling, same
      as the broker tool's own `nonzero=true` convention).

    Returns {"status", "detail", "long_leg", "short_leg", "unrecognized_positions"}:
      - status "MATCHED": both legs found, correct type, quantities equal to
        `recorded["quantity"]` and to each other.
      - status "MISMATCHED_QUANTITY": both legs found but quantities disagree
        (with each other or with the recorded quantity) — flagged, never
        silently averaged or assumed to be the smaller/larger figure.
      - status "SHORT_LEG_ABSENT": the long leg is present as recorded but the
        short leg is not found at all. This is NOT asserted to be an assignment
        — a manual close of just the short leg produces the exact same observed
        state from position data alone. Flagged "NEEDS_INVESTIGATION", always;
        the caller must check get_option_orders history to actually determine
        the cause before acting.
      - status "LONG_LEG_ABSENT": the mirror case (short leg present, long leg
        missing) — e.g. the long leg was independently exercised or closed.
        Also flagged NEEDS_INVESTIGATION, same reasoning.
      - status "NOT_OPEN": neither leg found — the spread is fully closed or was
        never opened under these exact ids.
      - status "WRONG_TYPE": a position with a matching option_id exists but its
        `type` field contradicts the recorded leg role (e.g. the recorded long
        leg's option_id shows up with type="short") — a real data inconsistency,
        never silently reinterpreted.
      `unrecognized_positions` always lists every position in the input whose
      option_id matches neither recorded leg id, regardless of status above —
      these are never folded into this spread's reconciliation, and never
      silently dropped from the report either.
    """
    long_id = recorded["long_option_id"]
    short_id = recorded["short_option_id"]
    expected_qty = recorded["quantity"]

    long_matches = [p for p in positions if p.get("option_id") == long_id]
    short_matches = [p for p in positions if p.get("option_id") == short_id]
    unrecognized = [p for p in positions if p.get("option_id") not in (long_id, short_id)]

    long_leg = long_matches[0] if len(long_matches) == 1 else (long_matches or None)
    short_leg = short_matches[0] if len(short_matches) == 1 else (short_matches or None)

    # Multiple positions reporting the SAME option_id is itself a data anomaly —
    # never pick one arbitrarily.
    if len(long_matches) > 1 or len(short_matches) > 1:
        return {"status": "AMBIGUOUS_DUPLICATE_POSITION", "detail":
                "more than one position reported the same option_id for a recorded leg — cannot reconcile without guessing",
                "long_leg": long_matches or None, "short_leg": short_matches or None,
                "unrecognized_positions": unrecognized}

    long_present = long_leg is not None
    short_present = short_leg is not None

    if not long_present and not short_present:
        return {"status": "NOT_OPEN", "detail": "neither recorded leg found in current positions — closed or never opened",
                "long_leg": None, "short_leg": None, "unrecognized_positions": unrecognized}

    if long_present and long_leg.get("type") != "long":
        return {"status": "WRONG_TYPE", "detail": f"recorded long leg's option_id has type={long_leg.get('type')!r}, not 'long'",
                "long_leg": long_leg, "short_leg": short_leg, "unrecognized_positions": unrecognized}
    if short_present and short_leg.get("type") != "short":
        return {"status": "WRONG_TYPE", "detail": f"recorded short leg's option_id has type={short_leg.get('type')!r}, not 'short'",
                "long_leg": long_leg, "short_leg": short_leg, "unrecognized_positions": unrecognized}

    if long_present and not short_present:
        return {"status": "SHORT_LEG_ABSENT — NEEDS_INVESTIGATION", "detail":
                "long leg still open, short leg not found — could be assignment, exercise, or an independent manual close; position data alone cannot distinguish these, check get_option_orders/get_option_positions(nonzero=false) history",
                "long_leg": long_leg, "short_leg": None, "unrecognized_positions": unrecognized}
    if short_present and not long_present:
        return {"status": "LONG_LEG_ABSENT — NEEDS_INVESTIGATION", "detail":
                "short leg still open, long leg not found — could be an independent exercise/close of the long leg; check order history before acting",
                "long_leg": None, "short_leg": short_leg, "unrecognized_positions": unrecognized}

    long_qty = long_leg.get("quantity")
    short_qty = short_leg.get("quantity")
    if long_qty != short_qty or long_qty != expected_qty:
        return {"status": "MISMATCHED_QUANTITY", "detail":
                f"long_qty={long_qty}, short_qty={short_qty}, recorded_quantity={expected_qty} — not all equal",
                "long_leg": long_leg, "short_leg": short_leg, "unrecognized_positions": unrecognized}

    return {"status": "MATCHED", "detail": "both legs present, correct type, quantities agree",
            "long_leg": long_leg, "short_leg": short_leg, "unrecognized_positions": unrecognized}


def _leg_fill_balance(legs, tolerance: float = 1e-9):
    """
    Given a multi-leg order's per-leg fill data (a list of dicts, each with a
    total `quantity` and a `filled_quantity` — or `quantity_filled`, either
    key name accepted), determine whether every leg filled in the SAME
    proportion of its own quantity (a balanced partial fill of the paired
    strategy — fewer complete spreads filled, not an unpaired leg) versus a
    genuinely uneven fill across legs (demonstrated legging risk).

    Returns "balanced_partial", "imbalanced", or None when the supplied data
    is insufficient to tell either way (no legs, or any leg missing a usable
    quantity/filled_quantity, or a zero/negative quantity) — None is the
    honest answer in that case, never a guess in either direction.
    """
    if not legs:
        return None
    ratios = []
    for leg in legs:
        qty = leg.get("quantity")
        filled = leg.get("filled_quantity", leg.get("quantity_filled"))
        if qty is None or filled is None or qty <= 0:
            return None
        ratios.append(filled / qty)
    if max(ratios) - min(ratios) <= tolerance:
        return "balanced_partial"
    return "imbalanced"


def classify_multileg_order_state(order: dict) -> dict:
    """
    Classifies a multi-leg option order's broker-reported `state` (the field
    get_option_orders returns: queued/confirmed/partially_filled/filled/
    rejected/cancelled/failed/voided/pending_cancelled) for the one state that
    matters specifically for paired-leg execution risk: `partially_filled`.

    A native multi-leg order structurally prevents the two legs being submitted
    as independently-timed orders — but the broker's own documented state enum
    still includes `partially_filled` as a possible outcome for ANY option
    order, multi-leg included, and nothing in the tool schema states multi-leg
    orders are exempt from it or guaranteed to fill/cancel atomically.

    **Corrected 2026-11-11 (see CLAUDE.md §12 change log — a focused external
    review of CLAUDE.md/this module caught that the prior version asserted
    `legging_risk_materialized: True` from the bare `partially_filled` state
    string alone.** That state is consistent with two different real
    outcomes — fewer complete paired spreads filled (a balanced partial fill
    of the strategy, no leg imbalance at all) or a genuine per-leg imbalance
    (real legging risk) — and the enum value by itself does not distinguish
    them. This function now only asserts `legging_risk_materialized: True`
    when per-leg fill-quantity data (`order["legs"]`, each with `quantity`
    and `filled_quantity`/`quantity_filled`) is actually supplied and shows a
    real imbalance across legs. When `partially_filled` is reported with no
    such per-leg data, or with per-leg data that is itself incomplete, the
    balance is `"unknown_pending_reconciliation"` and
    `legging_risk_materialized` is `None` — never asserted either way from
    the state string alone. A balanced partial fill, once actually
    demonstrated, is explicitly not treated as legging risk.

    Returns {"state", "legging_risk_materialized", "leg_fill_balance", "note"}.
    """
    state = order.get("state")
    if state == "filled":
        return {"state": state, "legging_risk_materialized": False, "leg_fill_balance": "full",
                "note": "fully filled — reconcile against positions to confirm, never assume from order state alone"}
    if state == "partially_filled":
        balance = _leg_fill_balance(order.get("legs"))
        if balance == "balanced_partial":
            return {"state": state, "legging_risk_materialized": False, "leg_fill_balance": "balanced_partial",
                    "note": "per-leg fill data supplied and shows every leg filled the same proportion of its own quantity — fewer complete paired spreads filled, not an unpaired leg; this is NOT legging risk. Still reconcile against real positions (reconcile_vertical_spread_positions) before trusting it, never assumed from this classification alone."}
        if balance == "imbalanced":
            return {"state": state, "legging_risk_materialized": True, "leg_fill_balance": "imbalanced",
                    "note": "per-leg fill data supplied and shows a genuine, demonstrated imbalance across legs — this is exactly the legging-risk scenario a native multi-leg order is meant to avoid structurally, now actually observed. Reconcile immediately against real positions (reconcile_vertical_spread_positions)."}
        return {"state": state, "legging_risk_materialized": None, "leg_fill_balance": "unknown_pending_reconciliation",
                "note": "partially_filled alone does not establish whether legs filled proportionally (a balanced partial strategy fill) or unevenly (genuine legging risk) — no usable per-leg fill-quantity data was supplied this call (pass order['legs'], each with quantity and filled_quantity, to resolve this). Treat balance as unknown and reconcile against real positions (reconcile_vertical_spread_positions/get_option_positions) before concluding either way — never assert legging risk from the state string alone."}
    if state in ("queued", "confirmed"):
        return {"state": state, "legging_risk_materialized": False, "leg_fill_balance": "not_applicable",
                "note": "not yet executed — no position exists from this order yet"}
    if state in ("rejected", "cancelled", "failed", "voided", "pending_cancelled"):
        return {"state": state, "legging_risk_materialized": False, "leg_fill_balance": "not_applicable",
                "note": "did not execute — no position should exist from this order; verify via reconcile_vertical_spread_positions if in doubt"}
    return {"state": state, "legging_risk_materialized": None, "leg_fill_balance": None,
            "note": f"unrecognized state {state!r} — not one of the documented get_option_orders values, treat as unresolved"}


def validate_execution_authority(origin: dict, known_scheduled_trigger_ids: Sequence[str]) -> dict:
    """
    Universal Safety Kernel item 12 (added 2026-11-11, closing the real RDW
    authority breach — see CLAUDE.md §12 change log): determines whether THIS
    turn may use an autonomous order-placement exception (§1 Mode B/Mode C, §21
    item 6, §22 item 8, §24 once live), or must fall back to §1's default
    OBSERVE_AND_PROPOSE / exact-CONFIRM-ORDER-phrase requirement.

    Fails closed, always: any ambiguity, missing field, or unrecognized/absent
    trigger_id resolves to CHAT_REQUESTED_OBSERVE_AND_PROPOSE (no authority) —
    this function never defaults to granting autonomous authority.

    Deliberately does NOT trust:
      - A self-assigned `cycle`/label string anywhere in origin, no matter how
        closely it names or mimics a real scheduled trigger's own cycle name
        (e.g. "fresh_candle_entry_screening") — a label is never evidence.
      - `origin["source"] == "scheduled_trigger"` by itself — that claim must
        be corroborated by a `trigger_id` that is actually in
        `known_scheduled_trigger_ids` (the real, currently-enabled trigger
        list — read fresh via list_triggers/get_trigger, never hardcoded from
        memory by the caller).
      - A real/valid-looking trigger_id present WITHOUT source=="scheduled_trigger"
        (e.g. one merely mentioned in a chat message) — both fields must agree.

    origin: {"source": "scheduled_trigger"|"chat_request"|..., "trigger_id": str|None, ...}
            (extra keys, including any self-labeled "cycle" name, are accepted
            and ignored for the authority decision — logged by the caller for
            audit only, never consulted here).
    known_scheduled_trigger_ids: the real, currently-enabled autonomous trigger
      ids (e.g. from list_triggers) — authority can only attach to one of these.

    Returns {"authority": "SCHEDULED_AUTONOMOUS"|"CHAT_REQUESTED_OBSERVE_AND_PROPOSE", "reason": str}.
    """
    if not isinstance(origin, dict):
        return {"authority": "CHAT_REQUESTED_OBSERVE_AND_PROPOSE", "reason": "no origin record provided — fails closed"}
    source = origin.get("source")
    trigger_id = origin.get("trigger_id")
    known = set(known_scheduled_trigger_ids or [])
    if source == "scheduled_trigger" and trigger_id and trigger_id in known:
        return {"authority": "SCHEDULED_AUTONOMOUS",
                "reason": f"verified scheduled-trigger origin, trigger_id={trigger_id} matches the known enabled trigger list"}
    if source == "scheduled_trigger" and trigger_id and trigger_id not in known:
        return {"authority": "CHAT_REQUESTED_OBSERVE_AND_PROPOSE",
                "reason": f"source claims scheduled_trigger but trigger_id={trigger_id} is not in the known enabled trigger list — never trusted on the source claim alone"}
    if source == "scheduled_trigger" and not trigger_id:
        return {"authority": "CHAT_REQUESTED_OBSERVE_AND_PROPOSE",
                "reason": "source claims scheduled_trigger but no trigger_id given — a claim alone, including any self-labeled cycle name, is never sufficient"}
    return {"authority": "CHAT_REQUESTED_OBSERVE_AND_PROPOSE",
            "reason": "origin is a chat-requested (or unverified) turn — running the same protocol steps a scheduled Routine would run does not confer scheduled authority; exact CONFIRM ORDER phrase required for any order"}


def position_size(risk_dollars: float, entry: float, stop: float, direction: str) -> Optional[float]:
    """
    Refuses (returns None) on a backwards stop rather than sizing via abs() — the
    2026-11-xx §20 item 2 bug fix this mirrors: a stop on the wrong side of entry
    must NO_TRADE, never silently size as if it were valid.
    """
    if direction == "long":
        if not (0 < stop < entry):
            return None
        stop_distance = entry - stop
    elif direction == "short":
        if not (stop > entry > 0):
            return None
        stop_distance = stop - entry
    else:
        raise ValueError("direction must be 'long' or 'short'")
    if stop_distance <= 0:
        return None
    return risk_dollars / stop_distance
