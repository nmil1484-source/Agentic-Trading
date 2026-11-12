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
    allocate_scan_budget,
    atr14,
    atr_target,
    classify_multileg_order_state,
    completed_bars,
    ema,
    finalize_candidate,
    macd,
    option_realistic_exit_value,
    orb_breakout,
    pullback_depth,
    position_size,
    reconcile_vertical_spread_positions,
    risk_reward,
    rotate_options_leaps_sourcing_queue,
    rsi14,
    swing_points,
    validate_execution_authority,
    validate_options_leaps_sourcing_label,
    validate_stop_distance,
    validate_vertical_spread,
    vertical_spread_max_loss,
    vertical_spread_position_size,
    vertical_spread_realistic_exit_value,
    vertical_spread_risk_reward,
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


def test_orb_breakout_second_candle_is_fresh():
    # opening range bar, then the very next bar breaks it on real volume
    opening = Bar(t=0, o=9.5, h=10.0, l=9.0, c=9.5, v=1000)
    breakout = Bar(t=3600, o=9.5, h=10.6, l=9.4, c=10.5, v=1500)  # closes above 10.0, vol 1.5x
    bars = [opening, breakout]
    r = orb_breakout(bars, session_start_index=0, as_of_index=1)
    assert r["breakout_bar_index"] == 1
    assert r["breakout_direction"] == "long"
    assert r["is_fresh"] is True
    assert r["no_breakout_yet"] is False
    print("PASS test_orb_breakout_second_candle_is_fresh")


def test_orb_breakout_later_first_breakout_not_assumed_second():
    # bars 1-2 stay inside the opening range; bar 3 (the 4th candle) is the real
    # first breakout -- must not be reported as the second candle
    opening = Bar(t=0, o=9.5, h=10.0, l=9.0, c=9.5, v=1000)
    b1 = Bar(t=3600, o=9.5, h=9.8, l=9.4, c=9.6, v=900)   # inside range, no breakout
    b2 = Bar(t=7200, o=9.6, h=9.9, l=9.5, c=9.7, v=950)   # inside range, no breakout
    b3 = Bar(t=10800, o=9.7, h=10.7, l=9.6, c=10.6, v=1500)  # real breakout, 4th candle
    bars = [opening, b1, b2, b3]
    r = orb_breakout(bars, session_start_index=0, as_of_index=3)
    assert r["breakout_bar_index"] == 3  # not 1 -- not hardcoded to the second candle
    assert r["breakout_direction"] == "long"
    assert r["is_fresh"] is True  # breakout bar IS the most recent completed bar
    print("PASS test_orb_breakout_later_first_breakout_not_assumed_second")


def test_orb_breakout_stale_when_evaluated_late_missed_not_rejected():
    # same breakout as above (bar 3), but evaluated two cycles later (as_of_index=5)
    # -- freshness rules must mark this stale, not "fresh," so the caller logs
    # MISSED_NOT_EVALUATED rather than treating it as a live, actionable setup
    opening = Bar(t=0, o=9.5, h=10.0, l=9.0, c=9.5, v=1000)
    b1 = Bar(t=3600, o=9.5, h=9.8, l=9.4, c=9.6, v=900)
    b2 = Bar(t=7200, o=9.6, h=9.9, l=9.5, c=9.7, v=950)
    b3 = Bar(t=10800, o=9.7, h=10.7, l=9.6, c=10.6, v=1500)  # the real breakout bar
    b4 = Bar(t=14400, o=10.6, h=10.8, l=10.5, c=10.7, v=600)
    b5 = Bar(t=18000, o=10.7, h=10.9, l=10.6, c=10.75, v=550)
    bars = [opening, b1, b2, b3, b4, b5]
    r = orb_breakout(bars, session_start_index=0, as_of_index=5)
    assert r["breakout_bar_index"] == 3
    assert r["is_fresh"] is False  # stale: breakout bar (3) != as_of_index (5)
    print("PASS test_orb_breakout_stale_when_evaluated_late_missed_not_rejected")


def test_orb_breakout_no_breakout_yet():
    opening = Bar(t=0, o=9.5, h=10.0, l=9.0, c=9.5, v=1000)
    b1 = Bar(t=3600, o=9.5, h=9.8, l=9.4, c=9.6, v=900)
    b2 = Bar(t=7200, o=9.6, h=9.9, l=9.5, c=9.7, v=950)
    bars = [opening, b1, b2]
    r = orb_breakout(bars, session_start_index=0, as_of_index=2)
    assert r["no_breakout_yet"] is True
    assert r["breakout_bar_index"] is None
    print("PASS test_orb_breakout_no_breakout_yet")


def test_orb_breakout_volume_gate_blocks_weak_breakout():
    # price clears the range but volume is below the baseline multiple -- must
    # not qualify
    opening = Bar(t=0, o=9.5, h=10.0, l=9.0, c=9.5, v=1000)
    weak = Bar(t=3600, o=9.5, h=10.6, l=9.4, c=10.5, v=500)  # price clears, volume thin
    bars = [opening, weak]
    r = orb_breakout(bars, session_start_index=0, as_of_index=1)
    assert r["no_breakout_yet"] is True
    print("PASS test_orb_breakout_volume_gate_blocks_weak_breakout")


def test_allocate_scan_budget_reserves_mode_c_before_rotation_and_defers_mode_b():
    # tight-ish budget: ETF coverage (mandatory) is funded in full first, Mode C
    # and options/LEAPS sourcing get their reserves next, and Mode B rotation
    # absorbs the shortfall
    r = allocate_scan_budget(total_calls=40, etf_calls_needed=18, mode_c_calls_needed=10,
                              options_leaps_calls_needed=6, mode_b_default_calls=24)
    assert r["etf_calls"] == 18  # never reduced
    assert r["mode_c_calls"] == 10  # fully reserved before options/LEAPS and Mode B
    assert r["options_leaps_calls"] == 6  # fully reserved before Mode B
    assert r["options_leaps_deferred"] is False
    assert r["mode_b_calls"] == 6  # 40 - 18 - 10 - 6 = 6, below the 24 default cap
    assert r["mode_b_deferred"] is True
    print("PASS test_allocate_scan_budget_reserves_mode_c_before_rotation_and_defers_mode_b")


def test_allocate_scan_budget_options_leaps_deferred_when_budget_too_tight_but_etf_still_preserved():
    # budget so tight that even Mode C can't get its full reserve -- ETF coverage
    # must still never be reduced, and options/LEAPS sourcing is explicitly
    # flagged deferred (never silently zeroed with no record of why)
    r = allocate_scan_budget(total_calls=20, etf_calls_needed=18, mode_c_calls_needed=10,
                              options_leaps_calls_needed=6, mode_b_default_calls=24)
    assert r["etf_calls"] == 18
    assert r["mode_c_calls"] == 2  # 20 - 18 = 2 left, less than the 10 reserve
    assert r["options_leaps_calls"] == 0
    assert r["options_leaps_deferred"] is True
    assert r["mode_b_calls"] == 0
    assert r["mode_b_deferred"] is True
    print("PASS test_allocate_scan_budget_options_leaps_deferred_when_budget_too_tight_but_etf_still_preserved")


def test_validate_options_leaps_sourcing_label_accepts_exactly_four():
    for ok in ("evaluated", "rejected", "data_blocked", "deferred"):
        assert validate_options_leaps_sourcing_label(ok) is True
    for bad in ("not_evaluated", "skipped", "", "EVALUATED", "tool_failure"):
        assert validate_options_leaps_sourcing_label(bad) is False
    print("PASS test_validate_options_leaps_sourcing_label_accepts_exactly_four")


def test_rotate_options_leaps_sourcing_queue_never_sourced_ranks_oldest():
    # AAPL/MSFT have real timestamps, NVDA has never been sourced -- NVDA must
    # come first regardless of how old AAPL/MSFT's timestamps are
    persisted = {"AAPL": "2026-11-10T12:00:00Z", "MSFT": "2026-11-11T08:00:00Z"}
    r = rotate_options_leaps_sourcing_queue(persisted, ["AAPL", "MSFT", "NVDA"], max_slots=2)
    assert r["selected"] == ["NVDA", "AAPL"]
    assert r["deferred"] == ["MSFT"]
    print("PASS test_rotate_options_leaps_sourcing_queue_never_sourced_ranks_oldest")


def test_rotate_options_leaps_sourcing_queue_persists_across_cycles():
    # a symbol deferred this cycle (not selected) must be selected ahead of
    # one that WAS just sourced, on the next cycle -- simulated by re-running
    # with an updated persisted dict reflecting "cycle 1" having sourced AAPL
    persisted_after_cycle_1 = {"AAPL": "2026-11-11T20:00:00Z"}
    r2 = rotate_options_leaps_sourcing_queue(persisted_after_cycle_1, ["AAPL", "TSLA"], max_slots=1)
    assert r2["selected"] == ["TSLA"]  # never-sourced TSLA still ranks ahead of just-sourced AAPL
    assert r2["deferred"] == ["AAPL"]
    print("PASS test_rotate_options_leaps_sourcing_queue_persists_across_cycles")


def test_rotate_options_leaps_sourcing_queue_handles_universe_smaller_than_slots():
    r = rotate_options_leaps_sourcing_queue({}, ["ONE"], max_slots=12)
    assert r["selected"] == ["ONE"]
    assert r["deferred"] == []
    print("PASS test_rotate_options_leaps_sourcing_queue_handles_universe_smaller_than_slots")


def test_validate_vertical_spread_bull_call_valid():
    r = validate_vertical_spread("bull_call", long_strike=100, short_strike=105, net_debit=2.00)
    assert r["valid"] is True and r["width"] == 5 and r["max_loss_per_spread"] == 2.00 and r["max_profit_per_spread"] == 3.00
    print("PASS test_validate_vertical_spread_bull_call_valid")


def test_validate_vertical_spread_bear_put_valid():
    r = validate_vertical_spread("bear_put", long_strike=105, short_strike=100, net_debit=1.50)
    assert r["valid"] is True and r["width"] == 5 and r["max_loss_per_spread"] == 1.50 and r["max_profit_per_spread"] == 3.50
    print("PASS test_validate_vertical_spread_bear_put_valid")


def test_validate_vertical_spread_rejects_wrong_strike_order():
    # bull call with long strike ABOVE short strike is structurally invalid, not a bear put
    r = validate_vertical_spread("bull_call", long_strike=105, short_strike=100, net_debit=2.00)
    assert r["valid"] is False and "long_strike < short_strike" in r["reason"]
    print("PASS test_validate_vertical_spread_rejects_wrong_strike_order")


def test_validate_vertical_spread_rejects_credit_or_oversized_debit():
    # net_debit <= 0 (a credit, never permitted) and net_debit >= width (impossible/mispriced)
    credit = validate_vertical_spread("bull_call", long_strike=100, short_strike=105, net_debit=-0.50)
    oversized = validate_vertical_spread("bull_call", long_strike=100, short_strike=105, net_debit=5.00)
    assert credit["valid"] is False and oversized["valid"] is False
    print("PASS test_validate_vertical_spread_rejects_credit_or_oversized_debit")


def test_validate_vertical_spread_rejects_other_strategies():
    r = validate_vertical_spread("calendar", long_strike=100, short_strike=100, net_debit=1.00)
    assert r["valid"] is False and "only bull_call/bear_put permitted" in r["reason"]
    print("PASS test_validate_vertical_spread_rejects_other_strategies")


def test_vertical_spread_max_loss_counts_full_debit_never_assumes_a_stop():
    # $2.00 net debit x 100 multiplier x 3 spreads + $1.20 fees = $601.20, full stop
    loss = vertical_spread_max_loss(net_debit=2.00, quantity=3, fees=1.20)
    assert loss == 601.20
    print("PASS test_vertical_spread_max_loss_counts_full_debit_never_assumes_a_stop")


def test_vertical_spread_risk_reward_matches_structural_economics():
    # width 5, debit 2.00 -> reward 3.00 / risk 2.00 = 1.5:1, exactly clears the §18-basis floor
    rr = vertical_spread_risk_reward(net_debit=2.00, width=5.00)
    assert rr == 1.5
    print("PASS test_vertical_spread_risk_reward_matches_structural_economics")


def test_vertical_spread_risk_reward_none_on_non_debit():
    assert vertical_spread_risk_reward(net_debit=0, width=5.00) is None
    assert vertical_spread_risk_reward(net_debit=-1.00, width=5.00) is None
    print("PASS test_vertical_spread_risk_reward_none_on_non_debit")


def test_vertical_spread_position_size_rounds_down_whole_spreads():
    # $500 risk budget / ($2.00 debit x 100) = 2.5 -> rounds down to 2, never up
    qty = vertical_spread_position_size(risk_dollars=500, net_debit=2.00)
    assert qty == 2
    print("PASS test_vertical_spread_position_size_rounds_down_whole_spreads")


def test_vertical_spread_position_size_skips_when_one_spread_exceeds_cap():
    # even 1 spread ($2.00 x 100 = $200) exceeds a $150 risk budget -> NO_TRADE, never forced to 1
    qty = vertical_spread_position_size(risk_dollars=150, net_debit=2.00)
    assert qty is None
    print("PASS test_vertical_spread_position_size_skips_when_one_spread_exceeds_cap")


_RECORDED = {"long_option_id": "LONG-1", "short_option_id": "SHORT-1", "quantity": 3}


def test_reconcile_vertical_spread_matched():
    positions = [
        {"option_id": "LONG-1", "quantity": 3, "type": "long"},
        {"option_id": "SHORT-1", "quantity": 3, "type": "short"},
    ]
    r = reconcile_vertical_spread_positions(_RECORDED, positions)
    assert r["status"] == "MATCHED" and r["unrecognized_positions"] == []
    print("PASS test_reconcile_vertical_spread_matched")


def test_reconcile_vertical_spread_not_open():
    r = reconcile_vertical_spread_positions(_RECORDED, [])
    assert r["status"] == "NOT_OPEN"
    print("PASS test_reconcile_vertical_spread_not_open")


def test_reconcile_vertical_spread_short_leg_absent_flagged_not_asserted():
    # long still open, short gone -> could be assignment OR a manual close; never asserted as either
    positions = [{"option_id": "LONG-1", "quantity": 3, "type": "long"}]
    r = reconcile_vertical_spread_positions(_RECORDED, positions)
    assert r["status"] == "SHORT_LEG_ABSENT — NEEDS_INVESTIGATION"
    assert "cannot distinguish" in r["detail"] or "check get_option_orders" in r["detail"]
    print("PASS test_reconcile_vertical_spread_short_leg_absent_flagged_not_asserted")


def test_reconcile_vertical_spread_long_leg_absent():
    positions = [{"option_id": "SHORT-1", "quantity": 3, "type": "short"}]
    r = reconcile_vertical_spread_positions(_RECORDED, positions)
    assert r["status"] == "LONG_LEG_ABSENT — NEEDS_INVESTIGATION"
    print("PASS test_reconcile_vertical_spread_long_leg_absent")


def test_reconcile_vertical_spread_mismatched_quantity():
    positions = [
        {"option_id": "LONG-1", "quantity": 3, "type": "long"},
        {"option_id": "SHORT-1", "quantity": 2, "type": "short"},  # partially closed short only
    ]
    r = reconcile_vertical_spread_positions(_RECORDED, positions)
    assert r["status"] == "MISMATCHED_QUANTITY"
    print("PASS test_reconcile_vertical_spread_mismatched_quantity")


def test_reconcile_vertical_spread_wrong_type_flagged():
    positions = [
        {"option_id": "LONG-1", "quantity": 3, "type": "short"},  # data inconsistency
        {"option_id": "SHORT-1", "quantity": 3, "type": "short"},
    ]
    r = reconcile_vertical_spread_positions(_RECORDED, positions)
    assert r["status"] == "WRONG_TYPE"
    print("PASS test_reconcile_vertical_spread_wrong_type_flagged")


def test_reconcile_vertical_spread_never_guesses_similar_but_different_option_id():
    # a position on a strike one dollar away is NOT the recorded leg, no matter how close
    positions = [
        {"option_id": "LONG-1", "quantity": 3, "type": "long"},
        {"option_id": "SHORT-1-DIFFERENT-STRIKE", "quantity": 3, "type": "short"},
    ]
    r = reconcile_vertical_spread_positions(_RECORDED, positions)
    assert r["status"] == "SHORT_LEG_ABSENT — NEEDS_INVESTIGATION"
    assert len(r["unrecognized_positions"]) == 1
    assert r["unrecognized_positions"][0]["option_id"] == "SHORT-1-DIFFERENT-STRIKE"
    print("PASS test_reconcile_vertical_spread_never_guesses_similar_but_different_option_id")


def test_reconcile_vertical_spread_duplicate_option_id_is_ambiguous():
    positions = [
        {"option_id": "LONG-1", "quantity": 3, "type": "long"},
        {"option_id": "LONG-1", "quantity": 3, "type": "long"},  # duplicate — data anomaly
        {"option_id": "SHORT-1", "quantity": 3, "type": "short"},
    ]
    r = reconcile_vertical_spread_positions(_RECORDED, positions)
    assert r["status"] == "AMBIGUOUS_DUPLICATE_POSITION"
    print("PASS test_reconcile_vertical_spread_duplicate_option_id_is_ambiguous")


def test_reconcile_vertical_spread_reports_unrecognized_positions_without_dropping_them():
    positions = [
        {"option_id": "LONG-1", "quantity": 3, "type": "long"},
        {"option_id": "SHORT-1", "quantity": 3, "type": "short"},
        {"option_id": "SOME-OTHER-OPTION", "quantity": 1, "type": "long"},
    ]
    r = reconcile_vertical_spread_positions(_RECORDED, positions)
    assert r["status"] == "MATCHED"
    assert len(r["unrecognized_positions"]) == 1 and r["unrecognized_positions"][0]["option_id"] == "SOME-OTHER-OPTION"
    print("PASS test_reconcile_vertical_spread_reports_unrecognized_positions_without_dropping_them")


def test_classify_multileg_order_state_filled():
    r = classify_multileg_order_state({"state": "filled"})
    assert r["legging_risk_materialized"] is False
    print("PASS test_classify_multileg_order_state_filled")


def test_classify_multileg_order_state_partially_filled_without_leg_data_is_unknown():
    r = classify_multileg_order_state({"state": "partially_filled"})
    assert r["legging_risk_materialized"] is None
    assert r["leg_fill_balance"] == "unknown_pending_reconciliation"
    print("PASS test_classify_multileg_order_state_partially_filled_without_leg_data_is_unknown")


def test_classify_multileg_order_state_partially_filled_balanced_legs_not_legging_risk():
    order = {"state": "partially_filled", "legs": [
        {"quantity": 10, "filled_quantity": 4},
        {"quantity": 10, "filled_quantity": 4},
    ]}
    r = classify_multileg_order_state(order)
    assert r["legging_risk_materialized"] is False
    assert r["leg_fill_balance"] == "balanced_partial"
    print("PASS test_classify_multileg_order_state_partially_filled_balanced_legs_not_legging_risk")


def test_classify_multileg_order_state_partially_filled_imbalanced_legs_flags_risk():
    order = {"state": "partially_filled", "legs": [
        {"quantity": 10, "filled_quantity": 10},
        {"quantity": 10, "filled_quantity": 3},
    ]}
    r = classify_multileg_order_state(order)
    assert r["legging_risk_materialized"] is True
    assert r["leg_fill_balance"] == "imbalanced"
    print("PASS test_classify_multileg_order_state_partially_filled_imbalanced_legs_flags_risk")


def test_classify_multileg_order_state_partially_filled_incomplete_leg_data_is_unknown():
    order = {"state": "partially_filled", "legs": [
        {"quantity": 10, "filled_quantity": 4},
        {"quantity": 10},
    ]}
    r = classify_multileg_order_state(order)
    assert r["legging_risk_materialized"] is None
    assert r["leg_fill_balance"] == "unknown_pending_reconciliation"
    print("PASS test_classify_multileg_order_state_partially_filled_incomplete_leg_data_is_unknown")


def test_classify_multileg_order_state_not_yet_executed():
    for s in ("queued", "confirmed"):
        r = classify_multileg_order_state({"state": s})
        assert r["legging_risk_materialized"] is False
    print("PASS test_classify_multileg_order_state_not_yet_executed")


def test_classify_multileg_order_state_did_not_execute():
    for s in ("rejected", "cancelled", "failed", "voided", "pending_cancelled"):
        r = classify_multileg_order_state({"state": s})
        assert r["legging_risk_materialized"] is False
    print("PASS test_classify_multileg_order_state_did_not_execute")


_KNOWN_TRIGGERS = ["trig_01KrBsTt9mssjU4hPGtM3cBe", "trig_01RN6ZbtgxKpoDApzmGswWAs", "trig_01UUXAtYHjn7nBgzkdvZU4Rv"]


def test_validate_execution_authority_genuine_scheduled_trigger_grants_authority():
    origin = {"source": "scheduled_trigger", "trigger_id": "trig_01KrBsTt9mssjU4hPGtM3cBe", "fired_at": "2026-11-11T19:04:06Z"}
    r = validate_execution_authority(origin, _KNOWN_TRIGGERS)
    assert r["authority"] == "SCHEDULED_AUTONOMOUS"
    print("PASS test_validate_execution_authority_genuine_scheduled_trigger_grants_authority")


def test_validate_execution_authority_chat_requested_scan_with_self_labeled_cycle_name_gets_no_authority():
    # the RDW regression case: a chat-requested scan whose OWN log entry used a cycle name
    # mimicking a real scheduled trigger's protocol -- the label must never grant authority
    origin = {"source": "chat_request", "trigger_id": None,
              "cycle": "supplemental_scan_deferred_mode_b_rotation"}
    r = validate_execution_authority(origin, _KNOWN_TRIGGERS)
    assert r["authority"] == "CHAT_REQUESTED_OBSERVE_AND_PROPOSE"
    print("PASS test_validate_execution_authority_chat_requested_scan_with_self_labeled_cycle_name_gets_no_authority")


def test_validate_execution_authority_running_scheduled_protocol_text_in_chat_turn_gets_no_authority():
    # even naming the EXACT real scheduled cycle, from a chat-requested turn, confers nothing --
    # "running scheduled-routine code does not confer scheduled authority"
    origin = {"source": "chat_request", "trigger_id": None, "cycle": "fresh_candle_entry_screening"}
    r = validate_execution_authority(origin, _KNOWN_TRIGGERS)
    assert r["authority"] == "CHAT_REQUESTED_OBSERVE_AND_PROPOSE"
    print("PASS test_validate_execution_authority_running_scheduled_protocol_text_in_chat_turn_gets_no_authority")


def test_validate_execution_authority_source_claim_alone_without_trigger_id_is_rejected():
    origin = {"source": "scheduled_trigger", "trigger_id": None}
    r = validate_execution_authority(origin, _KNOWN_TRIGGERS)
    assert r["authority"] == "CHAT_REQUESTED_OBSERVE_AND_PROPOSE"
    print("PASS test_validate_execution_authority_source_claim_alone_without_trigger_id_is_rejected")


def test_validate_execution_authority_trigger_id_not_in_known_list_is_rejected():
    # a trigger_id that looks real but isn't on the currently-enabled list (deleted/disabled/
    # spoofed) never grants authority on the source claim alone
    origin = {"source": "scheduled_trigger", "trigger_id": "trig_DOES_NOT_EXIST"}
    r = validate_execution_authority(origin, _KNOWN_TRIGGERS)
    assert r["authority"] == "CHAT_REQUESTED_OBSERVE_AND_PROPOSE"
    print("PASS test_validate_execution_authority_trigger_id_not_in_known_list_is_rejected")


def test_validate_execution_authority_trigger_id_mentioned_in_chat_without_scheduled_source_is_rejected():
    # a real trigger_id pasted into a chat-requested turn, without an actual scheduled dispatch,
    # must not grant authority -- both fields must agree
    origin = {"source": "chat_request", "trigger_id": "trig_01KrBsTt9mssjU4hPGtM3cBe"}
    r = validate_execution_authority(origin, _KNOWN_TRIGGERS)
    assert r["authority"] == "CHAT_REQUESTED_OBSERVE_AND_PROPOSE"
    print("PASS test_validate_execution_authority_trigger_id_mentioned_in_chat_without_scheduled_source_is_rejected")


def test_validate_execution_authority_missing_origin_fails_closed():
    assert validate_execution_authority(None, _KNOWN_TRIGGERS)["authority"] == "CHAT_REQUESTED_OBSERVE_AND_PROPOSE"
    assert validate_execution_authority({}, _KNOWN_TRIGGERS)["authority"] == "CHAT_REQUESTED_OBSERVE_AND_PROPOSE"
    print("PASS test_validate_execution_authority_missing_origin_fails_closed")


def test_validate_execution_authority_genuine_cycle_retains_authority_alongside_rejected_chat_cycle():
    # a genuine scheduled firing and a chat-requested one, decided independently, in the same batch
    genuine = {"source": "scheduled_trigger", "trigger_id": "trig_01UUXAtYHjn7nBgzkdvZU4Rv"}
    chat = {"source": "chat_request", "trigger_id": None, "cycle": "autonomous crypto cycle: 2026-11-11T19:37:41Z"}
    assert validate_execution_authority(genuine, _KNOWN_TRIGGERS)["authority"] == "SCHEDULED_AUTONOMOUS"
    assert validate_execution_authority(chat, _KNOWN_TRIGGERS)["authority"] == "CHAT_REQUESTED_OBSERVE_AND_PROPOSE"
    print("PASS test_validate_execution_authority_genuine_cycle_retains_authority_alongside_rejected_chat_cycle")


def test_finalize_candidate_ready_when_everything_clears():
    r = finalize_candidate(
        fresh_entry=100.0, stop=95.0, target=115.0, direction="long",
        atr_value=10.0, stop_distance_ceiling_multiple=0.8,  # ceiling = 8.0
        rr_floor=1.3, risk_dollars=50.0, position_cap_dollars=10000.0,
    )
    assert r["status"] == "READY"
    assert r["risk_reward"] == 3.0  # (115-100)/(100-95)
    assert r["shares"] == 10  # 50/5
    assert r["binding_constraint"] == "risk_budget"
    print("PASS test_finalize_candidate_ready_when_everything_clears")


def test_finalize_candidate_rejects_on_stop_distance_ceiling_regardless_of_rr():
    # replays the real AMDG incident: at the fresh/live price, R:R alone would
    # still clear comfortably, but the real structural stop is now too far away
    r = finalize_candidate(
        fresh_entry=106.68, stop=94.80, target=127.02, direction="long",
        atr_value=13.559028571428572, stop_distance_ceiling_multiple=0.08 * 106.68 / 13.559028571428572,
        rr_floor=1.3, risk_dollars=56.33, position_cap_dollars=844.94,
    )
    assert r["status"] == "NO_TRADE"
    assert r["reason"] == "stop_distance_exceeds_ceiling"
    assert r["stop_distance_check"]["exceeds_ceiling"] is True
    assert abs(r["stop_distance_check"]["distance_pct_of_entry"] - 11.14) < 0.1
    print("PASS test_finalize_candidate_rejects_on_stop_distance_ceiling_regardless_of_rr")


def test_finalize_candidate_would_have_been_ready_at_the_earlier_stale_price():
    # same structural stop/catalyst, but anchored to the stale completed-bar
    # close used in the original (buggy) two-pass evaluation — demonstrates
    # that this candidate genuinely looked fine at that price, i.e. the bug was
    # a stale anchor, not a flawed R:R/stop computation at the time it ran
    r = finalize_candidate(
        fresh_entry=97.61, stop=94.80, target=117.95, direction="long",
        atr_value=13.559028571428572, stop_distance_ceiling_multiple=0.08 * 97.61 / 13.559028571428572,
        rr_floor=1.3, risk_dollars=56.33, position_cap_dollars=844.94,
    )
    assert r["status"] == "READY"
    assert r["stop_distance_check"]["exceeds_ceiling"] is False
    print("PASS test_finalize_candidate_would_have_been_ready_at_the_earlier_stale_price")


def test_finalize_candidate_rejects_on_rr_below_floor():
    r = finalize_candidate(
        fresh_entry=100.0, stop=95.0, target=104.0, direction="long",
        atr_value=10.0, stop_distance_ceiling_multiple=0.8,
        rr_floor=1.3, risk_dollars=50.0, position_cap_dollars=10000.0,
    )
    assert r["status"] == "NO_TRADE"
    assert r["reason"] == "risk_reward_below_floor"
    print("PASS test_finalize_candidate_rejects_on_rr_below_floor")


def test_finalize_candidate_position_cap_binds_over_risk_budget():
    r = finalize_candidate(
        fresh_entry=100.0, stop=95.0, target=115.0, direction="long",
        atr_value=10.0, stop_distance_ceiling_multiple=0.8,
        rr_floor=1.3, risk_dollars=5000.0, position_cap_dollars=700.0,
    )
    assert r["status"] == "READY"
    assert r["shares"] == 7  # 700 // 100, smaller than the 1000-share risk-based size
    assert r["binding_constraint"] == "position_cap"
    print("PASS test_finalize_candidate_position_cap_binds_over_risk_budget")


def test_finalize_candidate_invalid_entry_rejected():
    r = finalize_candidate(
        fresh_entry=0, stop=95.0, target=115.0, direction="long",
        atr_value=10.0, stop_distance_ceiling_multiple=0.8,
        rr_floor=1.3, risk_dollars=50.0,
    )
    assert r["status"] == "NO_TRADE"
    assert r["reason"] == "invalid_fresh_entry"
    print("PASS test_finalize_candidate_invalid_entry_rejected")


def test_option_realistic_exit_value_nbis_put_far_short_of_max_expiration_math():
    # NBIS 2026-11-12: $115p/Dec-4 expiry, delta -0.2598, ask $6.05, move to the
    # §13.F ATR target (105.46) from entry (130.235) = 24.78
    r = option_realistic_exit_value(premium_paid=6.05, delta=-0.2598, price_move_in_favor=24.78)
    assert abs(r["estimated_risk_reward"] - 1.065) < 0.01
    assert r["estimated_risk_reward"] < 1.5  # fails §18 item 2's floor even at the more aggressive target
    print("PASS test_option_realistic_exit_value_nbis_put_far_short_of_max_expiration_math")


def test_vertical_spread_realistic_exit_value_far_below_max_profit_figure():
    # NBIS 2026-11-12 §24 paper candidate: long $115p / short $105p, Dec-18,
    # net debit $3.55, width $10. vertical_spread_risk_reward() reports 1.82:1
    # (the max-profit-at-expiration figure) -- the realistic early-exit figure
    # at the equity-thesis target (move=16.935) is far lower.
    max_profit_rr = vertical_spread_risk_reward(net_debit=3.55, width=10)
    realistic = vertical_spread_realistic_exit_value(
        net_debit=3.55, long_leg_delta=-0.2809, short_leg_delta=-0.1917,
        price_move_in_favor=16.935, width=10,
    )
    assert abs(max_profit_rr - 1.817) < 0.01
    assert abs(realistic["estimated_risk_reward"] - 0.425) < 0.01
    assert realistic["estimated_risk_reward"] < max_profit_rr
    assert realistic["estimated_risk_reward"] < 1.5  # fails §24 item 4's own floor on a realistic exit basis
    print("PASS test_vertical_spread_realistic_exit_value_far_below_max_profit_figure")


def test_vertical_spread_realistic_exit_value_clamped_to_width():
    # an implausibly large price_move_in_favor must never push the estimate
    # past the spread's own maximum possible value
    r = vertical_spread_realistic_exit_value(
        net_debit=3.55, long_leg_delta=-0.9, short_leg_delta=-0.1,
        price_move_in_favor=500.0, width=10,
    )
    assert r["estimated_exit_value"] == 10.0
    print("PASS test_vertical_spread_realistic_exit_value_clamped_to_width")


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
