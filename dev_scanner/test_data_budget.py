"""
Tests for data_budget.py — run via: python3 -I dev_scanner/test_data_budget.py

Uses a temp directory for every file-touching test so this never reads or
writes the real dev_scanner/state/ directory that live trigger cycles use.
"""

import sys
import tempfile
import os

sys.path.insert(0, "/home/user/Agentic-Trading")

from dev_scanner.data_budget import (
    cache_key,
    is_cache_fresh_enough,
    load_cached_bars,
    load_state,
    merge_bars,
    record_tradingview_result,
    save_cached_bars,
    save_state,
    should_attempt_tradingview,
    tradingview_status_summary,
)

PASS = 0
FAIL = 0


def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"PASS  {name}")
    else:
        FAIL += 1
        print(f"FAIL  {name}  {detail}")


# ---------------------------------------------------------------------------
# Cold start
# ---------------------------------------------------------------------------

with tempfile.TemporaryDirectory() as tmp:
    cold_path = os.path.join(tmp, "nonexistent_state.json")
    cold_state = load_state(cold_path)
    check("COLD START: load_state on a nonexistent path returns an empty-but-valid structure",
          cold_state == {"tradingview": {}, "cache_meta": {}}, detail=str(cold_state))

    cold_cache = load_cached_bars("AAVE", "1h", cache_dir=tmp)
    check("COLD START: load_cached_bars with no cache file yet returns []", cold_cache == [])


# ---------------------------------------------------------------------------
# should_attempt_tradingview / record_tradingview_result — never assume reset
# ---------------------------------------------------------------------------

state = {"tradingview": {}, "cache_meta": {}}
check("untested date -> should_attempt is True (must still make a real attempt, never a free pass)",
      should_attempt_tradingview(state, "2026-11-17") is True)

record_tradingview_result(state, "2026-11-17", success=False, quota_error=True, at_epoch=1000.0)
check("after a quota_error, should_attempt for the SAME date is now False",
      should_attempt_tradingview(state, "2026-11-17") is False)
check("exhausted flag is actually set in state (not just the derived function)",
      state["tradingview"]["2026-11-17"]["exhausted"] is True)

# Critical: the next calendar date is NOT assumed available — but it IS
# "untested," which still means "try once," matching the task's own
# instruction ("do not assume a midnight reset... without respecting the
# provider's limits" — i.e. don't keep hammering a KNOWN-exhausted date, but
# a new date has no such record yet and must be tested for real).
check("a DIFFERENT (later) date with no record of its own is untested, not inherited as exhausted",
      should_attempt_tradingview(state, "2026-11-18") is True)
check("...and the ORIGINAL exhausted date is unaffected by checking a different date",
      should_attempt_tradingview(state, "2026-11-17") is False)

record_tradingview_result(state, "2026-11-17", success=True, quota_error=False, at_epoch=2000.0)
check("exhausted clears ONLY on a real recorded success for that exact date — never a time-based assumption",
      should_attempt_tradingview(state, "2026-11-17") is True)
check("attempts counter incremented across both recorded calls for that date",
      state["tradingview"]["2026-11-17"]["attempts"] == 2)

summary_exhausted_date = tradingview_status_summary(state, "2026-11-17")
check("tradingview_status_summary reflects AVAILABLE after the recorded success",
      summary_exhausted_date["status"] == "AVAILABLE")
summary_untested = tradingview_status_summary(state, "2099-01-01")
check("tradingview_status_summary for a never-touched date reports UNTESTED_TODAY, not AVAILABLE",
      summary_untested["status"] == "UNTESTED_TODAY")

# A second quota_error on an already-exhausted date keeps it exhausted and
# still increments attempts (proves repeated real attempts are tracked, even
# though should_attempt_tradingview would have told the caller not to make
# this one — the function doesn't enforce that itself, callers must check
# should_attempt_tradingview before calling the real TradingView tool; this
# just records whatever the caller actually observed).
record_tradingview_result(state, "2026-11-19", success=False, quota_error=True, at_epoch=3000.0)
record_tradingview_result(state, "2026-11-19", success=False, quota_error=True, at_epoch=3100.0)
check("repeated quota errors on one date: still exhausted, attempts=2",
      state["tradingview"]["2026-11-19"]["exhausted"] is True and state["tradingview"]["2026-11-19"]["attempts"] == 2)


# ---------------------------------------------------------------------------
# save_state / load_state round-trip (real file I/O, temp dir only)
# ---------------------------------------------------------------------------

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "state.json")
    save_state(state, path)
    reloaded = load_state(path)
    check("save_state -> load_state round-trips the exhausted/attempts data exactly",
          reloaded["tradingview"]["2026-11-17"]["attempts"] == 2 and
          reloaded["tradingview"]["2026-11-19"]["exhausted"] is True,
          detail=str(reloaded))
    check("save_state is atomic (no leftover .tmp file after a successful write)",
          not os.path.exists(path + ".tmp"))


# ---------------------------------------------------------------------------
# merge_bars — dedupe by t, fresh wins on collision, sorted
# ---------------------------------------------------------------------------

existing = [{"t": 100, "c": 1.0}, {"t": 200, "c": 2.0}, {"t": 300, "c": 3.0}]
fresh = [{"t": 300, "c": 3.5}, {"t": 400, "c": 4.0}]  # 300 collides, revised; 400 is new
merged = merge_bars(existing, fresh)
check("merge_bars: result is sorted by t", [b["t"] for b in merged] == [100, 200, 300, 400])
check("merge_bars: colliding timestamp takes the FRESH value, not the stale cached one",
      next(b["c"] for b in merged if b["t"] == 300) == 3.5)
check("merge_bars: a previously-cached bar not superseded by fresh data is preserved",
      any(b["t"] == 100 for b in merged))
check("merge_bars: a genuinely new bar from fresh is added", any(b["t"] == 400 for b in merged))

empty_merge = merge_bars([], [])
check("merge_bars: empty+empty -> empty, not an error", empty_merge == [])


# ---------------------------------------------------------------------------
# is_cache_fresh_enough — the real "skip the network call" decision
# ---------------------------------------------------------------------------

now = 1_800_000_000.0
interval_seconds = 3600

enough_bars = [{"t": int(now - i * interval_seconds)} for i in range(25)]
fresh_check = is_cache_fresh_enough(enough_bars, interval_seconds, now, min_completed_bars=20)
check("is_cache_fresh_enough: enough bars AND most-recent bar already covers the current interval -> fresh_enough",
      fresh_check["fresh_enough"] is True, detail=str(fresh_check))

too_few_bars = enough_bars[:5]
few_check = is_cache_fresh_enough(too_few_bars, interval_seconds, now, min_completed_bars=20)
check("is_cache_fresh_enough: too few cached bars -> NOT fresh enough, must fetch",
      few_check["fresh_enough"] is False)

stale_cache_bars = [{"t": int(now - 10 * interval_seconds - i * interval_seconds)} for i in range(25)]
stale_check = is_cache_fresh_enough(stale_cache_bars, interval_seconds, now, min_completed_bars=20)
check("is_cache_fresh_enough: a newer completed bar should exist beyond the cache -> NOT fresh enough",
      stale_check["fresh_enough"] is False, detail=str(stale_check))


# ---------------------------------------------------------------------------
# save_cached_bars / load_cached_bars round-trip
# ---------------------------------------------------------------------------

with tempfile.TemporaryDirectory() as tmp:
    bars_to_cache = [{"t": 1, "o": 1, "h": 1, "l": 1, "c": 1, "v": 1},
                      {"t": 2, "o": 2, "h": 2, "l": 2, "c": 2, "v": 2}]
    save_cached_bars("AAVE", "1h", bars_to_cache, cache_dir=tmp)
    reloaded_bars = load_cached_bars("AAVE", "1h", cache_dir=tmp)
    check("save_cached_bars -> load_cached_bars round-trips exactly", reloaded_bars == bars_to_cache)

    check("cache_key is symbol/interval-specific (AAVE/1h != AAVE/4h)",
          cache_key("AAVE", "1h") != cache_key("AAVE", "4h"))
    check("cache_key normalizes case", cache_key("aave", "1H") == cache_key("AAVE", "1h"))


print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
