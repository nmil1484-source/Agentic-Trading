"""
Real tests for tv_structure.py — run via `python3 -m pytest dev_scanner/test_tv_structure.py -v`
or plain `python3 dev_scanner/test_tv_structure.py` (has a __main__ runner, no pytest required).
"""
from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dev_scanner.tv_structure import (
    REGULAR_SESSION_SECONDS,
    Bar,
    atr14,
    atr_target,
    completed_bars,
    ema,
    macd,
    pullback_depth,
    position_size,
    risk_reward,
    rsi14,
    swing_points,
    validate_stop_distance,
    volume_baseline_13h,
)


def _mk_bars(start_t, interval, closes, highs=None, lows=None, vols=None):
    bars = []
    for i, c in enumerate(closes):
        t = start_t + i * interval
        h = highs[i] if highs else c + 0.5
        l = lows[i] if lows else c - 0.5
        v = vols[i] if vols else 1000
        bars.append({"t": t, "o": c, "h": h, "l": l, "c": c, "v": v})
    return bars


def test_completed_bars_drops_forming_last_bar():
    bars = _mk_bars(0, 3600, [1, 2, 3])
    now = 3600 * 2 + 1800  # last bar (t=7200) only half done
    out = completed_bars(bars, 3600, now)
    assert [b.t for b in out] == [0, 3600]
    print("PASS test_completed_bars_drops_forming_last_bar")


def test_completed_bars_keeps_all_if_last_bar_fully_elapsed():
    bars = _mk_bars(0, 3600, [1, 2, 3])
    now = 3600 * 3 + 1
    out = completed_bars(bars, 3600, now)
    assert [b.t for b in out] == [0, 3600, 7200]
    print("PASS test_completed_bars_keeps_all_if_last_bar_fully_elapsed")


def test_completed_bars_daily_session_aware_override():
    # daily bar opened at t=0 (market open); 20000s later (< REGULAR_SESSION_SECONDS)
    # should NOT be complete under the session-aware override even though it's
    # "the same calendar day" by a flat-24h rule would also say incomplete here.
    bars = _mk_bars(0, 86400, [100])
    now_incomplete = 20000
    out = completed_bars(bars, 86400, now_incomplete, last_bar_duration_seconds=REGULAR_SESSION_SECONDS)
    assert out == []
    now_complete = REGULAR_SESSION_SECONDS + 1
    out2 = completed_bars(bars, 86400, now_complete, last_bar_duration_seconds=REGULAR_SESSION_SECONDS)
    assert len(out2) == 1
    print("PASS test_completed_bars_daily_session_aware_override")


def test_ema_known_value():
    closes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    e = ema(closes, 5)
    assert e is not None and abs(e - 8.0) < 1e-9  # verified by hand: seed=avg(1..5)=3, then EMA recursion -> 8.0
    assert ema([1, 2], 5) is None
    print("PASS test_ema_known_value")


def test_rsi_all_gains_is_100():
    closes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    r = rsi14(closes)
    assert r == 100.0
    print("PASS test_rsi_all_gains_is_100")


def test_rsi_all_losses_is_0():
    closes = list(range(20, 4, -1))
    r = rsi14(closes)
    assert r == 0.0
    print("PASS test_rsi_all_losses_is_0")


def test_rsi_insufficient_data_is_none():
    assert rsi14([1, 2, 3]) is None
    print("PASS test_rsi_insufficient_data_is_none")


def test_macd_insufficient_data_is_none():
    assert macd(list(range(10))) is None
    print("PASS test_macd_insufficient_data_is_none")


def test_macd_runs_on_enough_data():
    closes = [100 + i * 0.5 for i in range(40)]
    m = macd(closes)
    assert m is not None
    assert "macd" in m and "signal" in m and "hist" in m
    print("PASS test_macd_runs_on_enough_data")


def test_atr14_basic():
    bars_dicts = _mk_bars(0, 3600, [10] * 16, highs=[11] * 16, lows=[9] * 16)
    bars = [Bar(**b) for b in bars_dicts]
    a = atr14(bars)
    assert a is not None and abs(a - 2.0) < 1e-9
    print("PASS test_atr14_basic")


def test_atr14_insufficient_data_is_none():
    bars = [Bar(t=i, o=1, h=1, l=1, c=1) for i in range(5)]
    assert atr14(bars) is None
    print("PASS test_atr14_insufficient_data_is_none")


def test_volume_baseline_full_sample():
    bars = [Bar(t=i, o=1, h=1, l=1, c=1, v=v) for i, v in enumerate([10, 20, 30, 999])]
    result = volume_baseline_13h(bars, as_of_index=3, lookback=3)
    assert result == {"baseline": 20.0, "sample_size": 3}
    print("PASS test_volume_baseline_full_sample")


def test_volume_baseline_reduced_sample_flagged():
    bars = [Bar(t=0, o=1, h=1, l=1, c=1, v=50), Bar(t=1, o=1, h=1, l=1, c=1, v=999)]
    result = volume_baseline_13h(bars, as_of_index=1, lookback=3)
    assert result["sample_size"] == 1
    assert result["baseline"] == 50.0
    print("PASS test_volume_baseline_reduced_sample_flagged")


def test_volume_baseline_no_prior_bars_is_none():
    bars = [Bar(t=0, o=1, h=1, l=1, c=1, v=50)]
    assert volume_baseline_13h(bars, as_of_index=0, lookback=3) is None
    print("PASS test_volume_baseline_no_prior_bars_is_none")


def test_swing_points_breakout_detected():
    # prior 5 bars range 10-15, then a clean break above
    bars = [Bar(t=i, o=0, h=10 + i, l=10, c=10) for i in range(5)]
    bars.append(Bar(t=5, o=0, h=20, l=14, c=16))  # breaks above prior max high (14)
    sp = swing_points(bars, as_of_index=5, lookback=5)
    assert sp["current_above_prior_swing_high"] is True
    print("PASS test_swing_points_breakout_detected")


def test_swing_points_no_breakout():
    bars = [Bar(t=i, o=0, h=10 + i, l=10, c=10) for i in range(5)]
    bars.append(Bar(t=5, o=0, h=13, l=10, c=12))  # inside range, no breakout
    sp = swing_points(bars, as_of_index=5, lookback=5)
    assert sp["current_above_prior_swing_high"] is False
    print("PASS test_swing_points_no_breakout")


def test_swing_points_rejects_out_of_range_index():
    bars = [Bar(t=0, o=1, h=1, l=1, c=1)]
    try:
        swing_points(bars, as_of_index=5, lookback=5)
        assert False, "expected ValueError"
    except ValueError:
        pass
    print("PASS test_swing_points_rejects_out_of_range_index")


def test_pullback_depth_detects_real_pullback():
    # impulse up from 10 to 20 over bars 0-4, then bar 5 pulls back to 15 (50% retrace)
    highs = [10, 12, 15, 18, 20, 16]
    lows = [9, 11, 14, 17, 19, 15]
    closes = [10, 12, 15, 18, 20, 16]
    bars = [Bar(t=i, o=c, h=highs[i], l=lows[i], c=c) for i, c in enumerate(closes)]
    pd = pullback_depth(bars, as_of_index=5, lookback=5)
    assert pd is not None
    assert pd["impulse_high"] == 20
    assert 0 < pd["depth_pct"] < 100
    print("PASS test_pullback_depth_detects_real_pullback")


def test_pullback_depth_none_when_insufficient_lookback():
    bars = [Bar(t=0, o=1, h=1, l=1, c=1)]
    assert pullback_depth(bars, as_of_index=0, lookback=5) is None
    print("PASS test_pullback_depth_none_when_insufficient_lookback")


def test_atr_target_long_and_short():
    assert atr_target(100, 2, "long", 1.5) == 103.0
    assert atr_target(100, 2, "short", 1.5) == 97.0
    try:
        atr_target(100, 2, "sideways")
        assert False
    except ValueError:
        pass
    print("PASS test_atr_target_long_and_short")


def test_risk_reward_long():
    rr = risk_reward(entry=100, stop=95, target=115, direction="long")
    assert abs(rr - 3.0) < 1e-9  # risk 5, reward 15
    print("PASS test_risk_reward_long")


def test_risk_reward_short():
    rr = risk_reward(entry=100, stop=110, target=70, direction="short")
    assert abs(rr - 3.0) < 1e-9  # risk 10, reward 30
    print("PASS test_risk_reward_short")


def test_risk_reward_zero_or_negative_risk_is_none():
    assert risk_reward(entry=100, stop=100, target=120, direction="long") is None
    assert risk_reward(entry=100, stop=105, target=120, direction="long") is None  # backwards stop
    print("PASS test_risk_reward_zero_or_negative_risk_is_none")


def test_validate_stop_distance_within_ceiling():
    v = validate_stop_distance(entry=100, stop=94, atr_value=5, ceiling_multiple=2.0)
    # distance=6, ceiling=10 -> within
    assert v["exceeds_ceiling"] is False
    assert v["needs_structural_justification"] is False  # 6 > 0.5*5=2.5
    print("PASS test_validate_stop_distance_within_ceiling")


def test_validate_stop_distance_exceeds_ceiling():
    v = validate_stop_distance(entry=100, stop=80, atr_value=5, ceiling_multiple=2.0)
    # distance=20, ceiling=10 -> exceeds
    assert v["exceeds_ceiling"] is True
    print("PASS test_validate_stop_distance_exceeds_ceiling")


def test_validate_stop_distance_needs_structural_justification():
    v = validate_stop_distance(entry=100, stop=99, atr_value=5, ceiling_multiple=2.0)
    # distance=1, 0.5*atr=2.5 -> flagged, but 1 < ceiling(10) so not rejected
    assert v["exceeds_ceiling"] is False
    assert v["needs_structural_justification"] is True
    print("PASS test_validate_stop_distance_needs_structural_justification")


def test_position_size_long_normal():
    size = position_size(risk_dollars=100, entry=50, stop=48, direction="long")
    assert abs(size - 50.0) < 1e-9  # 100 / 2
    print("PASS test_position_size_long_normal")


def test_position_size_short_normal():
    size = position_size(risk_dollars=100, entry=50, stop=55, direction="short")
    assert abs(size - 20.0) < 1e-9  # 100 / 5
    print("PASS test_position_size_short_normal")


def test_position_size_refuses_backwards_long_stop():
    # stop ABOVE entry on a long — must refuse, never abs()-size it
    assert position_size(risk_dollars=100, entry=50, stop=55, direction="long") is None
    print("PASS test_position_size_refuses_backwards_long_stop")


def test_position_size_refuses_backwards_short_stop():
    assert position_size(risk_dollars=100, entry=50, stop=45, direction="short") is None
    print("PASS test_position_size_refuses_backwards_short_stop")


def test_position_size_refuses_zero_or_negative_entry():
    assert position_size(risk_dollars=100, entry=0, stop=-5, direction="long") is None
    print("PASS test_position_size_refuses_zero_or_negative_entry")


_ALL_TESTS = [v for k, v in list(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    failures = 0
    for fn in _ALL_TESTS:
        try:
            fn()
        except AssertionError as e:
            failures += 1
            print(f"FAIL {fn.__name__}: {e}")
        except Exception as e:
            failures += 1
            print(f"ERROR {fn.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(_ALL_TESTS) - failures}/{len(_ALL_TESTS)} passed")
    if failures:
        raise SystemExit(1)
