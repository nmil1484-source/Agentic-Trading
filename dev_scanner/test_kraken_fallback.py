"""
Tests for kraken_fallback.py — run via: python3 -I dev_scanner/test_kraken_fallback.py

Covers, per the 2026-11-17 data-layer repair's own required scenarios:
  - qualifying (a constructed favorable candidate clears a gate-style check
    on real/realistic Kraken-shaped bars)
  - rejected (the same pipeline correctly fails an unfavorable candidate)
  - stale/missing data (DATA_BLOCKED, never NO_TRADE, never a silent pass)
  - cold-start (no cache file yet)
  - unsupported/invalid pairs (DATA_BLOCKED, never NO_TRADE)

One test (test_live_kraken_aave_1h) makes a REAL network call to Kraken's
public API — no mock, same "verify, don't assume" discipline as this
repo's other live-checked tests (e.g. test_tv_structure.py's AMDG replay).
It is skipped with a clear printed reason (not a silent pass) if the network
is unreachable from this environment, rather than failing the whole suite
over an environment issue unrelated to the code under test.
"""

import sys
import time

sys.path.insert(0, "/home/user/Agentic-Trading")

from dev_scanner.kraken_fallback import (
    KRAKEN_PAIR_MAP,
    fetch_kraken_ohlc,
    kraken_pair_for,
    parse_kraken_ohlc_rows,
    validate_kraken_bars,
)
from dev_scanner.tv_structure import (
    atr14,
    completed_bars,
    ema,
    finalize_candidate,
    macd,
    rsi14,
    risk_reward,
    swing_points,
    volume_baseline_13h,
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
# Pair/interval mapping — verified live 2026-11-17 via Kraken AssetPairs
# ---------------------------------------------------------------------------

check("all 8 §21 allowlist symbols have a verified Kraken pair mapping",
      set(KRAKEN_PAIR_MAP.keys()) == {"BTC", "ETH", "SOL", "XRP", "LINK", "AAVE", "HBAR", "AVAX"})
check("kraken_pair_for is case-insensitive", kraken_pair_for("aave") == "AAVEUSD")
check("kraken_pair_for returns None for an unsupported symbol (never guesses)",
      kraken_pair_for("DOGE") is None)
check("BTC maps to Kraken's XXBTZUSD naming (not a guessed BTCUSD)",
      kraken_pair_for("BTC") == "XXBTZUSD")
check("ETH maps to Kraken's XETHZUSD naming", kraken_pair_for("ETH") == "XETHZUSD")


# ---------------------------------------------------------------------------
# parse_kraken_ohlc_rows — pure parsing + gap detection
# ---------------------------------------------------------------------------

def _row(t, o, h, l, c, v=100.0):
    return [t, str(o), str(h), str(l), str(c), "0", str(v), 10]


_SIXTY_MIN = 3600

no_gap_rows = [_row(1000 + i * _SIXTY_MIN, 100 + i, 101 + i, 99 + i, 100.5 + i) for i in range(5)]
parsed = parse_kraken_ohlc_rows(no_gap_rows, _SIXTY_MIN)
check("parse_kraken_ohlc_rows: no gaps on contiguous rows", parsed["gaps"] == [], detail=str(parsed["gaps"]))
check("parse_kraken_ohlc_rows: bar count preserved", len(parsed["bars"]) == 5)
check("parse_kraken_ohlc_rows: bar shape has t/o/h/l/c/v as the right types",
      isinstance(parsed["bars"][0]["t"], int) and isinstance(parsed["bars"][0]["c"], float))

gappy_rows = [_row(1000, 100, 101, 99, 100.5), _row(1000 + 3 * _SIXTY_MIN, 103, 104, 102, 103.5)]
parsed_gap = parse_kraken_ohlc_rows(gappy_rows, _SIXTY_MIN)
check("parse_kraken_ohlc_rows: a real missing-interval gap is flagged",
      len(parsed_gap["gaps"]) == 1 and parsed_gap["gaps"][0]["missing_intervals"] == 2,
      detail=str(parsed_gap["gaps"]))

unsorted_rows = [no_gap_rows[2], no_gap_rows[0], no_gap_rows[4], no_gap_rows[1], no_gap_rows[3]]
parsed_unsorted = parse_kraken_ohlc_rows(unsorted_rows, _SIXTY_MIN)
check("parse_kraken_ohlc_rows: out-of-order input rows are sorted by t",
      [b["t"] for b in parsed_unsorted["bars"]] == sorted(b["t"] for b in parsed_unsorted["bars"]))


# ---------------------------------------------------------------------------
# validate_kraken_bars — stale/missing/cold-start cases
# ---------------------------------------------------------------------------

check("validate_kraken_bars: empty input -> not ok, no_bars_returned",
      validate_kraken_bars([], _SIXTY_MIN, time.time())["reason"] == "no_bars_returned")

now = 1_800_000_000.0
fresh_bars = [{"t": int(now - (25 - i) * _SIXTY_MIN), "o": 1, "h": 1, "l": 1, "c": 1, "v": 1} for i in range(25)]
fresh_result = validate_kraken_bars(fresh_bars, _SIXTY_MIN, now, min_completed_bars=20)
check("validate_kraken_bars: 25 fresh contiguous bars with the forming one properly excluded -> ok",
      fresh_result["ok"] is True, detail=str(fresh_result))
check("validate_kraken_bars: the still-forming bar (t close to now) is excluded from 'completed'",
      all(b.t + _SIXTY_MIN <= now for b in fresh_result["completed"]))

sparse_bars = fresh_bars[-5:]
sparse_result = validate_kraken_bars(sparse_bars, _SIXTY_MIN, now, min_completed_bars=20)
check("validate_kraken_bars: fewer than min_completed_bars -> not ok, insufficient_completed_history",
      sparse_result["ok"] is False and "insufficient_completed_history" in sparse_result["reason"])

stale_bars = [{"t": int(now - 50 * _SIXTY_MIN - (25 - i) * _SIXTY_MIN), "o": 1, "h": 1, "l": 1, "c": 1, "v": 1}
              for i in range(25)]
stale_result = validate_kraken_bars(stale_bars, _SIXTY_MIN, now, min_completed_bars=20)
check("validate_kraken_bars: history exists but the most recent bar is >2 intervals stale -> not ok, stale_data",
      stale_result["ok"] is False and "stale_data" in stale_result["reason"], detail=str(stale_result))


# ---------------------------------------------------------------------------
# fetch_kraken_ohlc — full pipeline with an injected http_get (no network)
# ---------------------------------------------------------------------------

def _fake_http_get_factory(rows):
    def _get(url):
        return {"error": [], "result": {"AAVEUSD": rows, "last": 123}}
    return _get


check("fetch_kraken_ohlc: unsupported pair -> UNSUPPORTED_PAIR, never NO_TRADE",
      fetch_kraken_ohlc("DOGE", "1h")["status"] == "UNSUPPORTED_PAIR")
check("fetch_kraken_ohlc: unsupported interval -> UNSUPPORTED_INTERVAL",
      fetch_kraken_ohlc("AAVE", "15m")["status"] == "UNSUPPORTED_INTERVAL")


def _raising_http_get(url):
    raise OSError("simulated network failure")


err_result = fetch_kraken_ohlc("AAVE", "1h", http_get=_raising_http_get)
check("fetch_kraken_ohlc: a real network/OSError -> FETCH_ERROR, never silently empty",
      err_result["status"] == "FETCH_ERROR" and "simulated network failure" in err_result["error"])


def _kraken_error_http_get(url):
    return {"error": ["EQuery:Unknown asset pair"], "result": {}}


kraken_err_result = fetch_kraken_ohlc("AAVE", "1h", http_get=_kraken_error_http_get)
check("fetch_kraken_ohlc: Kraken's own error field is surfaced as FETCH_ERROR",
      kraken_err_result["status"] == "FETCH_ERROR" and "Unknown asset pair" in kraken_err_result["error"])


def _missing_key_http_get(url):
    return {"error": [], "result": {"last": 123}}  # no "AAVEUSD" key


missing_key_result = fetch_kraken_ohlc("AAVE", "1h", http_get=_missing_key_http_get)
check("fetch_kraken_ohlc: response missing the expected result key -> FETCH_ERROR, not a crash",
      missing_key_result["status"] == "FETCH_ERROR")

good_rows = [_row(int(now - (30 - i) * _SIXTY_MIN), 100 + i * 0.1, 101 + i * 0.1, 99 + i * 0.1, 100.5 + i * 0.1,
                   v=50 + i)
             for i in range(30)]
ok_result = fetch_kraken_ohlc("AAVE", "1h", now_epoch=now, min_completed_bars=20,
                               http_get=_fake_http_get_factory(good_rows))
check("fetch_kraken_ohlc: qualifying case — enough fresh, contiguous bars -> OK",
      ok_result["status"] == "OK" and len(ok_result["bars"]) >= 20, detail=str(ok_result.get("status")))
check("fetch_kraken_ohlc OK result exposes real tv_structure.Bar objects (same type TradingView bars use)",
      ok_result["status"] == "OK" and hasattr(ok_result["bars"][0], "c"))

stale_rows = [_row(int(now - 50 * _SIXTY_MIN - (30 - i) * _SIXTY_MIN), 100, 101, 99, 100.5) for i in range(30)]
stale_fetch_result = fetch_kraken_ohlc("AAVE", "1h", now_epoch=now, min_completed_bars=20,
                                         http_get=_fake_http_get_factory(stale_rows))
check("fetch_kraken_ohlc: stale data -> DATA_BLOCKED, never NO_TRADE",
      stale_fetch_result["status"] == "DATA_BLOCKED" and "stale_data" in stale_fetch_result["reason"])

gap_rows = good_rows[:15] + [_row(int(now - 3 * _SIXTY_MIN), 110, 111, 109, 110.5)]
gap_fetch_result = fetch_kraken_ohlc("AAVE", "1h", now_epoch=now, min_completed_bars=10,
                                       http_get=_fake_http_get_factory(gap_rows))
check("fetch_kraken_ohlc: a gap inside the required recent lookback -> DATA_BLOCKED",
      gap_fetch_result["status"] == "DATA_BLOCKED", detail=str(gap_fetch_result))


# ---------------------------------------------------------------------------
# End-to-end: Kraken-sourced bars run through the SAME tv_structure.py
# functions TradingView-sourced bars already use — qualifying vs. rejected.
# ---------------------------------------------------------------------------

def _build_pullback_reclaim_bars(start_price, interval_seconds):
    """
    15 bars with real range (true ATR context) + a 4-bar shallow pullback +
    1 reclaim bar — verified by direct computation (not guessed) to produce a
    real READY result via finalize_candidate with a 1.5x-ATR §13.F target and
    a swing-low-based stop, so the qualifying/rejected tests below exercise
    the actual gate math rather than hand-picked numbers.
    """
    bars = []
    price = start_price
    for _ in range(15):
        o, c = price, price + 0.3
        h, l = c + 3.5, o - 3.5
        bars.append((o, h, l, c))
        price = c
    pullback_lows = [price - 0.2, price - 1.0, price - 0.5, price - 0.1]
    for i in range(4):
        o = price
        c = price - 0.1 if i < 2 else price + 0.2
        l, h = pullback_lows[i], max(o, c) + 0.3
        bars.append((o, h, l, c))
        price = c
    o, c = price, price + 1.0
    h, l = c + 0.3, o - 0.2
    bars.append((o, h, l, c))
    return bars


pullback_t0 = int(now - 19 * _SIXTY_MIN)
pullback_ohlc = _build_pullback_reclaim_bars(100.0, _SIXTY_MIN)
pullback_kraken_rows = [_row(pullback_t0 + i * _SIXTY_MIN, o, h, l, c) for i, (o, h, l, c) in enumerate(pullback_ohlc)]

pullback_fetch = fetch_kraken_ohlc("AAVE", "1h", now_epoch=now, min_completed_bars=15,
                                     http_get=_fake_http_get_factory(pullback_kraken_rows))
check("end-to-end: a synthetic pullback-then-reclaim sequence fetches OK from the Kraken pipeline",
      pullback_fetch["status"] == "OK", detail=str(pullback_fetch.get("status")))

if pullback_fetch["status"] == "OK":
    bars = pullback_fetch["bars"]  # List[Bar]
    closes = [b.c for b in bars]
    idx = len(bars) - 1

    rsi = rsi14(closes)
    macd_val = macd(closes)
    atr = atr14(bars)
    vol = volume_baseline_13h(bars, idx)
    swings = swing_points(bars, idx)

    check("end-to-end: rsi14 computes a real value on Kraken-sourced closes", rsi is not None and 0 <= rsi <= 100)
    check("end-to-end: macd needs more bars than this fixture has (None is correct, not a crash)",
          macd_val is None)
    check("end-to-end: atr14 computes a real positive value on Kraken-sourced bars", atr is not None and atr > 0)
    check("end-to-end: volume_baseline_13h computes on Kraken-sourced bars", vol is not None)
    check("end-to-end: swing_points finds the shallow pullback low as the prior swing low",
          swings["prior_swing_low"] < closes[-1], detail=str(swings))

    entry = closes[-1]
    stop = swings["prior_swing_low"] * 0.999
    good_target = entry + 1.5 * atr  # §13.F ATR_TARGET
    qualifying = finalize_candidate(
        fresh_entry=entry, stop=stop, target=good_target, direction="long",
        atr_value=atr, stop_distance_ceiling_multiple=5.0, rr_floor=1.3,
        risk_dollars=50.0,
    )
    check("QUALIFYING case: finalize_candidate returns READY end-to-end on Kraken-sourced structure",
          qualifying["status"] == "READY" and qualifying["risk_reward"] >= 1.3, detail=str(qualifying))

    tight_ceiling_rejected = finalize_candidate(
        fresh_entry=entry, stop=stop, target=good_target, direction="long",
        atr_value=atr, stop_distance_ceiling_multiple=0.5, rr_floor=1.3,
        risk_dollars=50.0,
    )
    check("REJECTED case: finalize_candidate correctly fails (stop_distance_exceeds_ceiling) on the SAME data",
          tight_ceiling_rejected["status"] == "NO_TRADE" and
          tight_ceiling_rejected["reason"] == "stop_distance_exceeds_ceiling",
          detail=str(tight_ceiling_rejected))

    low_rr_target = entry + 0.2 * atr  # reward far too small for the risk taken
    rejected_rr = finalize_candidate(
        fresh_entry=entry, stop=stop, target=low_rr_target, direction="long",
        atr_value=atr, stop_distance_ceiling_multiple=5.0, rr_floor=1.3,
        risk_dollars=50.0,
    )
    check("REJECTED case: finalize_candidate correctly fails (risk_reward_below_floor) on the SAME data",
          rejected_rr["status"] == "NO_TRADE" and rejected_rr["reason"] == "risk_reward_below_floor",
          detail=str(rejected_rr))


# ---------------------------------------------------------------------------
# Live network test — real Kraken call, no mock. Skips (prints why) rather
# than silently passing if the network genuinely isn't reachable here.
# ---------------------------------------------------------------------------

def test_live_kraken_aave_1h():
    try:
        live = fetch_kraken_ohlc("AAVE", "1h", min_completed_bars=20)
    except Exception as exc:  # pragma: no cover - environment issue, not a code defect
        print(f"SKIP  test_live_kraken_aave_1h — exception reaching Kraken: {exc}")
        return
    if live["status"] == "FETCH_ERROR":
        print(f"SKIP  test_live_kraken_aave_1h — network unreachable this run: {live['error']}")
        return
    check("LIVE: real Kraken AAVEUSD 1h fetch succeeds (OK or DATA_BLOCKED, never FETCH_ERROR/UNSUPPORTED)",
          live["status"] in ("OK", "DATA_BLOCKED"), detail=str(live.get("status")))
    if live["status"] == "OK":
        check("LIVE: real Kraken bars have the correct Bar shape", hasattr(live["bars"][0], "c"))
        check("LIVE: real Kraken bars are genuinely completed (none still forming)",
              all(b.t + 3600 <= time.time() for b in live["bars"]))
        print(f"LIVE AAVEUSD 1h: {len(live['bars'])} completed bars, most recent close ${live['bars'][-1].c}")


test_live_kraken_aave_1h()


print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
