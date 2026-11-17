"""
Persistent, cross-trigger data-layer state for the §21 crypto lane, added
2026-11-17 at explicit user instruction after TradingView introduced a daily
MCP call quota (effective 2026-11-17) and the crypto lane — which has no
Robinhood-native OHLC fallback, unlike equities — started logging consecutive
DATA_BLOCKED cycles.

Two jobs, kept separate on purpose:
  1. A shared TradingView call-budget record so the Crypto 24/7 trigger, the
     Mode B/C First Scan trigger, and the Mode B/C Fresh Candle trigger all
     read and write the SAME persisted state instead of each independently
     re-discovering (and re-spending calls to discover) that the quota is
     already exhausted for the day. "Shared across triggers" means shared
     via this one state file on disk, read fresh at the start of a cycle and
     written back at the end — not an in-memory object, since each trigger
     fires as its own fresh turn.
  2. A completed-candle cache so a symbol/interval whose last completed bar
     hasn't changed since it was last fetched does not need a fresh network
     call at all this cycle — real call-budget relief, not just outage
     bookkeeping.

Explicit, load-bearing rule (per the task that created this module): NEVER
assume a midnight UTC reset. An exhausted-today flag is cleared ONLY when a
fresh real attempt actually succeeds — not by the calendar date rolling over
on its own. A new UTC date with no recorded entry yet is "untested," which
still means "try once, record the real result" — it is never silently
treated as "N calls available," because no one has verified that.

Pure logic lives in plain functions over plain dicts, independently testable
without touching disk. The on-disk file itself is a thin JSON blob at
STATE_PATH / cache files under CACHE_DIR — load_state()/save_state() are the
only functions that touch the filesystem.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional, Sequence

STATE_DIR = os.path.join(os.path.dirname(__file__), "state")
STATE_PATH = os.path.join(STATE_DIR, "data_budget_state.json")
CACHE_DIR = os.path.join(STATE_DIR, "candle_cache")

_EMPTY_STATE = {"tradingview": {}, "cache_meta": {}}


def _ensure_dirs() -> None:
    os.makedirs(STATE_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)


def load_state(path: str = STATE_PATH) -> dict:
    """Returns the persisted state dict, or a fresh empty one if the file doesn't exist yet (cold start)."""
    if not os.path.exists(path):
        return {"tradingview": {}, "cache_meta": {}}
    with open(path, "r") as f:
        data = json.load(f)
    data.setdefault("tradingview", {})
    data.setdefault("cache_meta", {})
    return data


def save_state(state: dict, path: str = STATE_PATH) -> None:
    _ensure_dirs()
    tmp_path = path + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(state, f, indent=2, sort_keys=True)
    os.replace(tmp_path, path)  # atomic on POSIX — never leaves a half-written state file


# ---------------------------------------------------------------------------
# TradingView quota tracking (pure functions over the "tradingview" sub-dict)
# ---------------------------------------------------------------------------

def should_attempt_tradingview(state: dict, utc_date: str) -> bool:
    """
    False only if THIS utc_date already has a recorded quota-exhaustion event.
    True for a date with no entry yet (untested — the caller must still make
    one real attempt and record the result via record_tradingview_result;
    this function never licenses skipping that attempt, it only tells the
    caller whether a PRIOR attempt today already proved the quota is dead).
    """
    entry = state.get("tradingview", {}).get(utc_date)
    if entry is None:
        return True
    return not entry.get("exhausted", False)


def record_tradingview_result(
    state: dict,
    utc_date: str,
    success: bool,
    quota_error: bool,
    at_epoch: float,
) -> dict:
    """
    Records one real TradingView call attempt's outcome for utc_date.
    - quota_error=True sets exhausted=True for utc_date, permanently for that
      date (a later success on the SAME calendar date would be surprising
      given a quota is daily, but if it happens this still only clears the
      flag — see the explicit note below — never assumed in advance).
    - success=True (and quota_error=False) clears exhausted for utc_date and
      records last_success_at — this is the ONLY way exhausted ever clears;
      never a time-based assumption.
    Mutates and returns `state` (caller is responsible for save_state()).
    """
    tv = state.setdefault("tradingview", {})
    entry = tv.setdefault(utc_date, {"exhausted": False, "attempts": 0})
    entry["attempts"] = entry.get("attempts", 0) + 1
    entry["last_attempt_at"] = at_epoch
    if quota_error:
        entry["exhausted"] = True
        entry["exhausted_at"] = at_epoch
    elif success:
        entry["exhausted"] = False
        entry["last_success_at"] = at_epoch
    return state


def tradingview_status_summary(state: dict, utc_date: str) -> dict:
    """Read-only convenience summary for logging — never used to make the attempt/skip decision itself."""
    entry = state.get("tradingview", {}).get(utc_date)
    if entry is None:
        return {"utc_date": utc_date, "status": "UNTESTED_TODAY", "attempts": 0}
    return {
        "utc_date": utc_date,
        "status": "EXHAUSTED" if entry.get("exhausted") else "AVAILABLE",
        "attempts": entry.get("attempts", 0),
        "last_attempt_at": entry.get("last_attempt_at"),
        "exhausted_at": entry.get("exhausted_at"),
        "last_success_at": entry.get("last_success_at"),
    }


# ---------------------------------------------------------------------------
# Completed-candle cache (pure merge/freshness logic; file I/O isolated below)
# ---------------------------------------------------------------------------

def cache_key(symbol: str, interval: str) -> str:
    return f"{symbol.upper()}_{interval.lower()}"


def merge_bars(existing: Sequence[dict], fresh: Sequence[dict]) -> List[dict]:
    """
    Union of existing and fresh bars, deduplicated by timestamp `t` (fresh
    wins on a timestamp collision — a re-fetched bar is assumed more
    authoritative than a cached one at the same t, since exchanges can
    revise a very recent bar's volume shortly after it closes), sorted
    ascending. Never drops a previously-cached bar that isn't superseded —
    the cache only grows (modulo the trim the caller applies) across cycles.
    """
    by_t: Dict[int, dict] = {b["t"]: b for b in existing}
    for b in fresh:
        by_t[b["t"]] = b
    return [by_t[t] for t in sorted(by_t.keys())]


def is_cache_fresh_enough(
    cached_bars: Sequence[dict],
    interval_seconds: int,
    now_epoch: float,
    min_completed_bars: int = 20,
) -> dict:
    """
    Decides whether the cache alone can serve this cycle WITHOUT a new
    network call — true only if (a) there are enough bars, and (b) the most
    recent bar in the cache already covers the latest bar that SHOULD exist
    as completed right now (i.e. a fresh fetch would not reveal a newer
    completed bar than what's cached). This is a real freshness check
    against now_epoch, never a blind "cache exists so use it."

    Returns {"fresh_enough": bool, "reason": str}.
    """
    if len(cached_bars) < min_completed_bars:
        return {"fresh_enough": False, "reason": f"only {len(cached_bars)} cached bars, need {min_completed_bars}"}
    most_recent_t = max(b["t"] for b in cached_bars)
    # The latest bar that should already exist as a COMPLETED bar is the one
    # whose start time is <= now_epoch - interval_seconds (it has fully
    # closed). If the cache's most recent bar already covers that boundary
    # (i.e. no full extra interval has elapsed since it), nothing newer is
    # available to fetch yet — the cache is current, not merely old-but-unchecked.
    if most_recent_t + interval_seconds >= now_epoch - interval_seconds:
        return {"fresh_enough": True, "reason": "cached most-recent completed bar already covers the current interval"}
    return {"fresh_enough": False, "reason": "a newer completed bar should exist beyond what's cached"}


def load_cached_bars(symbol: str, interval: str, cache_dir: str = CACHE_DIR) -> List[dict]:
    path = os.path.join(cache_dir, cache_key(symbol, interval) + ".json")
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def save_cached_bars(symbol: str, interval: str, bars: Sequence[dict], cache_dir: str = CACHE_DIR) -> None:
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, cache_key(symbol, interval) + ".json")
    tmp_path = path + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(list(bars), f)
    os.replace(tmp_path, path)
