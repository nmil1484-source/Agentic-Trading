"""
END-TO-END fixture tests — distinct from test_dev_scanner.py's HELPER
(pure-logic, synthetic-input) tests. Every fixture here is either real
data exported verbatim from this repo's own trades_log.md /
near_miss_queue.md, or is explicitly labeled SYNTHETIC where no real
counterpart exists yet. Run with:
    python3 -m unittest dev_scanner.test_integration_e2e -v
(from the repo root). No network, no broker, no live trigger call.
"""

import unittest
from pathlib import Path

from dev_scanner.run_record import CoverageState, LaneStatus
from dev_scanner.trigger_integration import (
    map_fresh_candle_json_to_run_record,
    detect_cycle_completion,
)
from dev_scanner.rotation_state import parse_near_miss_queue

REPO_ROOT = Path(__file__).resolve().parent.parent

# --- REAL fixture 1: trades_log.md, line 57715, 2026-11-04T16:14:54Z --------
# Mode C explicitly NOT_RUN but WITH a disclosed reason ("deprioritized
# this cycle, logged honestly").
REAL_CYCLE_1614 = {
    "cycle": "Mode B/C Entry Screening — Fresh Candle", "timestamp_utc": "2026-11-04T16:14:54Z",
    "modes_covered": ["B", "C"], "status_gate": "ACTIVE", "circuit_breakers_active": [],
    "positions": {"mode_b_count": 1, "mode_c_count": 0},
    "stop_audit": {"checked": 1, "missing_found": 0, "placed": 0},
    "options_stop_check": {"checked": 0, "breached": 0, "exited": 0},
    "coverage": {"universe_size": 74, "triaged": 61, "full_gate_evaluated": 12, "rejected_with_evidence": 9,
                 "not_evaluated": [], "session_cumulative_touched": 24, "tool_failures": 0},
    "near_miss_queue": {"reassessed": 0, "reassessment_deferred_reason": "candle unchanged since First Scan 45min ago",
                         "cleared": 0, "still_near_miss": 0, "new_near_miss": ["PGY", "IGV", "PLTR"],
                         "invalidated": 0, "ineligible": 0, "expired": 0},
    "leveraged_etf_coverage": {"universe_size": 9, "evaluated": 9, "rejected_with_evidence": 6, "near_miss": 1,
                                "invalidated": 2, "not_evaluated": [], "coverage_complete": True,
                                "reused_from": "2026-11-04T16:08Z diagnostic, same candle"},
    "mode_c": {"realized_pl_today": 0, "open_positions": 0, "dedicated_screen_performed": False,
               "reason": "deprioritized this cycle, logged honestly"},
    "tvremix_calls_used_today": 6, "exits": [], "entries": [], "orders_placed": 0, "git_push": "pending",
}

# --- REAL fixture 2: trades_log.md, line 57806, 2026-11-04T17:14:23Z -------
# The important one: Mode C is False with NO "reason" field at all — a
# genuine real-world example of exactly the "false clean scan" gap this
# whole patch exists to catch. This cycle's own narrative did not flag
# this omission at the time it was logged.
REAL_CYCLE_1714 = {
    "cycle": "Mode B/C Entry Screening — Fresh Candle", "timestamp_utc": "2026-11-04T17:14:23Z",
    "modes_covered": ["B", "C"], "status_gate": "ACTIVE", "circuit_breakers_active": [],
    "positions": {"mode_b_count": 1, "mode_c_count": 0},
    "stop_audit": {"checked": 1, "missing_found": 0, "placed": 0},
    "options_stop_check": {"checked": 0, "breached": 0, "exited": 0},
    "coverage": {"universe_size": 74, "triaged": 61, "full_gate_evaluated": 12, "rejected_with_evidence": 9,
                 "not_evaluated": [], "session_cumulative_touched": 33, "tool_failures": 0},
    "near_miss_queue": {"reassessed": 5, "cleared": 0, "still_near_miss": 2, "new_near_miss": ["ZETA"],
                         "resolved_to_rejected": ["CVX", "ZS", "DIS"], "ineligible": 0, "expired": 0},
    "leveraged_etf_coverage": {"universe_size": 9, "evaluated": 9, "rejected_with_evidence": 7,
                                "near_miss": ["TNA", "SPXL"], "not_evaluated": [], "coverage_complete": True},
    "mode_c": {"realized_pl_today": 0, "open_positions": 0, "dedicated_screen_performed": False},
    "tvremix_calls_used_today": 10, "exits": [], "entries": [], "orders_placed": 0, "git_push": "pending",
}

# --- REAL fixture 3: trades_log.md, line 58135, 2026-11-04T18:04:13Z -------
# The DATA_BLOCKED cycle. Mode C partial (5/74, Robinhood-native fallback).
REAL_CYCLE_1804 = {
    "cycle": "Mode B/C Entry Screening — Fresh Candle", "timestamp_utc": "2026-11-04T18:04:13Z",
    "timestamp_pacific": "2026-11-04T10:04:13-08:00",
    "modes_covered": ["B", "C"], "status_gate": "ACTIVE", "coverage_state": "DATA_BLOCKED",
    "circuit_breakers_active": [], "positions": {"mode_b_count": 1, "mode_c_count": 0},
    "stop_audit": {"checked": 1, "missing_found": 0, "placed": 0},
    "options_stop_check": {"checked": 0, "breached": 0, "exited": 0},
    "portfolio_heat_cap": {"current_heat_usd": 61.88, "cap_usd": 359.04, "blocked_or_resized": False},
    "coverage": {"universe_size": 74, "triaged": 74, "full_gate_evaluated": 0, "rejected_with_evidence": 0,
                 "not_evaluated": [{"symbols": ["TEM", "SOFI", "PGY", "IGV", "TSM", "HPE", "NBIS", "ONDS",
                                                 "CBRS", "VRT", "STM", "BE"],
                                     "reason": "tool failure — analyze_structure_batch connector-wide 429, 2/2 attempts"}],
                 "tool_failures": 12, "partial_structural_reads_not_counted_as_evaluated": ["DUOL", "AMZN", "DIS"]},
    "near_miss_queue": {"reassessed": 0, "cleared": 0, "still_near_miss": 4, "invalidated": 0, "ineligible": 0,
                         "expired": 0, "amd_pending_eligibility_status": "resolved_2026-11-04T16:08Z"},
    "leveraged_etf_coverage": {"universe_size": 9, "evaluated": 0, "rejected_with_evidence": 0,
                                "not_evaluated": [{"symbol": s, "reason": "tool failure — tvremix connector-wide 429"}
                                                   for s in ["TQQQ", "SQQQ", "SOXL", "SOXS", "SPXL", "SPXU", "TNA", "TZA", "AMDG"]],
                                "coverage_complete": False},
    "mode_c": {"realized_pl_today": 0, "open_positions": 0, "partial_screen_names": ["SPY", "QQQ", "AAPL", "AMZN", "TSLA"],
               "partial_screen_of_universe": "5 of 74", "dedicated_screen_performed": "partial", "candidates": 0},
    "tvremix_calls_used_today": 14, "exits": [], "entries": [], "orders_placed": 0, "git_push": "pending",
}


class TestMappingRealCycles(unittest.TestCase):
    def test_disclosed_mode_c_gap_is_incomplete(self):
        """Fixture 1: Mode C NOT_RUN but WITH a disclosed reason — still incomplete, disclosure doesn't exempt it."""
        rec = map_fresh_candle_json_to_run_record(
            REAL_CYCLE_1614, trigger_id="trig_01KrBsTt9mssjU4hPGtM3cBe",
            run_id="trig_01KrBsTt9mssjU4hPGtM3cBe:2026-11-04T16:14:54Z", policy_version="EP-v2.1",
        )
        self.assertEqual(rec.lanes["mode_c"].status, LaneStatus.NOT_RUN)
        self.assertIn("deprioritized", rec.lanes["mode_c"].detail)

    def test_silent_mode_c_gap_is_caught_same_as_disclosed_one(self):
        """
        Fixture 2 is the real regression case: unlike fixture 1, this real
        logged cycle gives NO reason for Mode C being skipped — at the
        time it was logged, nothing flagged this as a gap. This test
        proves the validator catches it anyway, honesty of the original
        log entry aside.
        """
        rec = map_fresh_candle_json_to_run_record(
            REAL_CYCLE_1714, trigger_id="trig_01KrBsTt9mssjU4hPGtM3cBe",
            run_id="trig_01KrBsTt9mssjU4hPGtM3cBe:2026-11-04T17:14:23Z", policy_version="EP-v2.1",
        )
        self.assertEqual(rec.lanes["mode_c"].status, LaneStatus.NOT_RUN)
        self.assertIn("NO reason given", rec.lanes["mode_c"].detail)

        from dev_scanner.run_record import validate_run_record
        result = validate_run_record(rec, seen_run_ids=set())
        self.assertEqual(result["coverage_state"], CoverageState.INCOMPLETE)
        self.assertIn("mode_c", result["missing_lanes"])

    def test_data_blocked_cycle_is_blocked_not_complete_and_mode_c_partial_flagged(self):
        """Fixture 3: mode_c PARTIAL (not EVALUATED), several lanes DATA_BLOCKED — never reads as COMPLETE."""
        rec = map_fresh_candle_json_to_run_record(
            REAL_CYCLE_1804, trigger_id="trig_01KrBsTt9mssjU4hPGtM3cBe",
            run_id="trig_01KrBsTt9mssjU4hPGtM3cBe:2026-11-04T18:04:13Z", policy_version="EP-v2.1",
        )
        self.assertEqual(rec.lanes["mode_c"].status, LaneStatus.PARTIAL)
        self.assertEqual(rec.lanes["stocks_stage2"].status, LaneStatus.DATA_BLOCKED)
        self.assertEqual(rec.lanes["leveraged_etf_s22"].status, LaneStatus.DATA_BLOCKED)

        from dev_scanner.run_record import validate_run_record
        result = validate_run_record(rec, seen_run_ids=set())
        self.assertNotEqual(result["coverage_state"], CoverageState.COMPLETE)

    def test_options_leaps_sourcing_always_not_run_under_current_schema(self):
        """Documents the real, current schema gap — not a mapping bug."""
        rec = map_fresh_candle_json_to_run_record(
            REAL_CYCLE_1714, trigger_id="t", run_id="r", policy_version="v",
        )
        self.assertEqual(rec.lanes["options_sourcing_s18"].status, LaneStatus.NOT_RUN)
        self.assertEqual(rec.lanes["leaps_sourcing_s19"].status, LaneStatus.NOT_RUN)
        self.assertIn("no dedicated field", rec.lanes["options_sourcing_s18"].detail)


class TestSilentSkipDetection(unittest.TestCase):
    """
    REAL fixture: trig_01KrBsTt9mssjU4hPGtM3cBe's own last_run object, as
    returned live by get_trigger() this session (2026-11-04), and the
    logged entries that eventually (late) accounted for each fire.
    """

    def test_real_1604_fire_found_late_not_as_silent_skip(self):
        # trades_log.md, 2026-11-04T16:09:55Z diagnostic entry:
        # fired_at 2026-11-04T16:04:20.496Z, finished_at 2026-11-04T16:04:20.507Z
        # (11ms dispatch gap) — genuinely processed and logged later at 16:14:54Z.
        last_run = {"status": "ROUTINE_RUN_STATUS_SUCCEEDED",
                    "fired_at": "2026-11-04T16:04:20.496Z", "finished_at": "2026-11-04T16:04:20.507Z"}
        logged = [{"cycle": "Mode B/C Entry Screening — Fresh Candle", "timestamp_utc": "2026-11-04T16:14:54Z"}]
        result = detect_cycle_completion(last_run, logged)
        self.assertAlmostEqual(result["dispatch_gap_seconds"], 0.011, places=2)
        self.assertFalse(result["dispatch_gap_is_evidence_of_work"])
        self.assertEqual(result["status"], "FOUND_LATE")  # ~10.4 min lag — found, but flagged late, not a hard failure
        self.assertGreater(result["lag_minutes"], 10.0)

    def test_real_1704_fire_found_late_matches_1714_log_entry(self):
        # From this session's own live get_trigger() call on
        # trig_01KrBsTt9mssjU4hPGtM3cBe: last_run.fired_at
        # "2026-11-04T17:04:05.835208Z", finished_at "...843945Z" (~8.7ms
        # gap) — the nearest logged entry for this trigger is 17:14:23Z,
        # ~10.3 minutes later. Same pattern as the 16:04 case above.
        last_run = {"status": "ROUTINE_RUN_STATUS_SUCCEEDED",
                    "fired_at": "2026-11-04T17:04:05.835208Z", "finished_at": "2026-11-04T17:04:05.843945Z"}
        logged = [{"cycle": "Mode B/C Entry Screening — Fresh Candle", "timestamp_utc": "2026-11-04T17:14:23Z"}]
        result = detect_cycle_completion(last_run, logged)
        self.assertEqual(result["status"], "FOUND_LATE")
        self.assertAlmostEqual(result["lag_minutes"], 10.3, delta=0.2)

    def test_synthetic_true_silent_skip_no_matching_entry_within_max_lag(self):
        """SYNTHETIC — no real counterpart exists on file for this exact shape (a fire with NO log entry ever)."""
        last_run = {"status": "ROUTINE_RUN_STATUS_SUCCEEDED",
                    "fired_at": "2026-11-04T20:03:00.000Z", "finished_at": "2026-11-04T20:03:00.010Z"}
        logged = [{"cycle": "Mode B/C Entry Screening — Fresh Candle", "timestamp_utc": "2026-11-04T19:14:23Z"}]  # an older, unrelated entry
        result = detect_cycle_completion(last_run, logged)
        self.assertEqual(result["status"], "LIKELY_SILENT_SKIP")

    def test_near_zero_dispatch_gap_is_explicitly_never_treated_as_work_evidence(self):
        """Structural assertion: every real fire this session shows a near-zero gap regardless of outcome."""
        last_run = {"status": "ROUTINE_RUN_STATUS_SUCCEEDED",
                    "fired_at": "2026-11-04T18:04:13.000Z", "finished_at": "2026-11-04T18:04:13.009Z"}
        logged = [{"cycle": "Mode B/C Entry Screening — Fresh Candle", "timestamp_utc": "2026-11-04T18:04:13Z"}]
        result = detect_cycle_completion(last_run, logged)
        self.assertFalse(result["dispatch_gap_is_evidence_of_work"])
        self.assertEqual(result["status"], "FOUND_ON_TIME")  # this one DOES have an on-time match — gap is still not why


class TestNearMissQueueParsing(unittest.TestCase):
    """REAL fixture: this repo's own near_miss_queue.md, read directly off disk."""

    def test_parses_real_file_live_rows_only(self):
        text = (REPO_ROOT / "near_miss_queue.md").read_text()
        entries = parse_near_miss_queue(text)
        symbols = {e.symbol for e in entries}

        # As of this session's own last update to the file, these four are
        # the genuinely live (non-struck-through) Mode B/C queue rows:
        for expected in ("TEM", "SOFI", "PGY", "IGV"):
            self.assertIn(expected, symbols, f"expected live row {expected} not parsed")

        # ZETA and PLTR were REMOVED (struck-through, multi-line prose) —
        # must never be parsed back in as live rows:
        self.assertNotIn("ZETA", symbols)
        self.assertNotIn("PLTR", symbols)

    def test_cycles_queued_values_are_real_not_defaulted(self):
        text = (REPO_ROOT / "near_miss_queue.md").read_text()
        entries = {e.symbol: e.cycles_queued for e in parse_near_miss_queue(text)}
        self.assertEqual(entries.get("TEM"), 3)
        self.assertEqual(entries.get("PGY"), 1)


if __name__ == "__main__":
    unittest.main()
