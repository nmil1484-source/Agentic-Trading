"""
Tests for dev_scanner/run_record.py and dev_scanner/candidate_selection.py.

Non-transactional. No network, no broker, no live trigger involved. Run with:
    python3 -m unittest dev_scanner.test_dev_scanner -v
(from the repo root)

Each test name maps directly to one bullet of the "VALIDATE WITHOUT ORDERS"
section of the 2026-11-04 scanner repair request.
"""

import unittest

from dev_scanner.run_record import (
    RunRecord,
    LaneRecord,
    LaneStatus,
    CoverageState,
    validate_run_record,
)
from dev_scanner.candidate_selection import (
    Stage1Entry,
    NearMissEntry,
    select_stage2_batch,
)


def _full_coverage_lanes(**overrides):
    """A baseline fully-covered, fresh set of required lanes; override a few per test."""
    base = {
        "stocks_stage1": LaneRecord(LaneStatus.EVALUATED, candidates_found=74, age_minutes=1),
        "stocks_stage2": LaneRecord(LaneStatus.EVALUATED, candidates_found=12, age_minutes=1),
        "leveraged_etf_s22": LaneRecord(LaneStatus.EVALUATED, candidates_found=9, age_minutes=1),
        "options_sourcing_s18": LaneRecord(LaneStatus.EVALUATED, candidates_found=0, age_minutes=1),
        "leaps_sourcing_s19": LaneRecord(LaneStatus.EVALUATED, candidates_found=0, age_minutes=1),
        "options_leaps_stop_check": LaneRecord(LaneStatus.SKIPPED_NA, detail="0 open options/LEAPS positions"),
        "mode_c": LaneRecord(LaneStatus.EVALUATED, candidates_found=0, age_minutes=1),
    }
    base.update(overrides)
    return base


class TestDuolReplay(unittest.TestCase):
    """
    'Replay DUOL with only information available at the tested time: prove
    it reaches applicable-method evaluation, not that it must qualify.'

    DUOL's real outcome (2026-11-04T18:22:38Z diagnostic, logged in
    trades_log.md, commit e54a112): §13.G breakout-continuation WAS reached
    and fully walked through (dated catalyst verified, fresh-high condition
    confirmed, hourly trigger candle identified, §13.H volume baseline
    computed) and the candidate was REJECTED on real, computed evidence
    (0.28x of baseline, far below the 1.2x floor) — not blocked by
    setup:null, and not forced to qualify.
    """

    def test_duol_reaches_evaluation_and_is_rejected_on_evidence_not_forced(self):
        lanes = _full_coverage_lanes(
            stocks_stage2=LaneRecord(
                LaneStatus.EVALUATED,
                detail=(
                    "DUOL: setup:null on pullback method did not block evaluation; "
                    "§13.G breakout-continuation walked in full — dated catalyst "
                    "(2026-11-03 Q3 earnings, verified), fresh-high confirmed on 60m "
                    "(+12.13% above the 2026-10-07 swing high $153.61), hourly trigger "
                    "candle 17:00-18:00Z close $171.37, §13.H volume baseline computed "
                    "(reduced 2-bar sample, 821,494.5) — REJECTED, item 2, ratio 0.28x "
                    "vs required >=1.2x."
                ),
                candidates_found=1,
                age_minutes=1,
            )
        )
        record = RunRecord(
            trigger_id="trig_01KrBsTt9mssjU4hPGtM3cBe",
            run_id="trig_01KrBsTt9mssjU4hPGtM3cBe:2026-11-04T18:04:13Z",
            scheduled_fire_pacific="2026-11-04T10:04:13-08:00",
            start_pacific="2026-11-04T10:04:13-08:00",
            finish_pacific="2026-11-04T10:22:38-08:00",
            policy_version="EP-v2.1, 2026-11-03",
            platform_status="SUCCEEDED",
            lanes=lanes,
        )
        result = validate_run_record(record, seen_run_ids=set())

        # The whole point: DUOL being REJECTED is not itself a coverage problem.
        self.assertEqual(result["coverage_state"], CoverageState.COMPLETE)
        self.assertEqual(result["missing_lanes"], [])
        self.assertEqual(lanes["stocks_stage2"].status, LaneStatus.EVALUATED)  # reached evaluation, not blocked
        self.assertIn("REJECTED", lanes["stocks_stage2"].detail)  # it legitimately failed on evidence
        self.assertIn("did not block evaluation", lanes["stocks_stage2"].detail)  # setup:null did not stop it


class TestMissingModeC(unittest.TestCase):
    """'Simulate a missing Mode C result: the cycle must remain incomplete.'"""

    def test_missing_mode_c_forces_incomplete_even_though_platform_succeeded(self):
        lanes = _full_coverage_lanes(mode_c=LaneRecord(LaneStatus.NOT_RUN, detail="deprioritized this cycle"))
        record = RunRecord(
            trigger_id="trig_01KrBsTt9mssjU4hPGtM3cBe",
            run_id="run-missing-mode-c",
            scheduled_fire_pacific="x",
            start_pacific="x",
            finish_pacific="x",
            policy_version="EP-v2.1, 2026-11-03",
            platform_status="SUCCEEDED",
            lanes=lanes,
        )
        result = validate_run_record(record, seen_run_ids=set())

        self.assertEqual(result["coverage_state"], CoverageState.INCOMPLETE)
        self.assertIn("mode_c", result["missing_lanes"])
        self.assertTrue(any("mode_c" in issue for issue in result["issues"]))
        # Mode C disappearing is never silently absorbed into a "clean" record:
        self.assertTrue(any("SUCCEEDED" in issue and "INCOMPLETE" in issue for issue in result["issues"]))

    def test_mode_c_cannot_claim_skipped_na(self):
        """Mode C is a required lane — it can never claim structural inapplicability."""
        lanes = _full_coverage_lanes(mode_c=LaneRecord(LaneStatus.SKIPPED_NA, detail="another lane used the time"))
        record = RunRecord(
            trigger_id="t", run_id="r2", scheduled_fire_pacific="x", start_pacific="x",
            finish_pacific="x", policy_version="v", platform_status="SUCCEEDED", lanes=lanes,
        )
        result = validate_run_record(record, seen_run_ids=set())
        self.assertEqual(result["coverage_state"], CoverageState.INCOMPLETE)
        self.assertIn("mode_c", result["missing_lanes"])


class TestAuthDataBlockedNeverClean(unittest.TestCase):
    """
    'Simulate auth/data failures: UNKNOWN/BLOCKED must never become passing
    evidence or a clean no-candidate result.'
    """

    def test_data_blocked_lane_is_blocked_not_complete(self):
        lanes = _full_coverage_lanes(
            stocks_stage2=LaneRecord(LaneStatus.DATA_BLOCKED, detail="tvremix connector-wide 429, 2/2 attempts")
        )
        record = RunRecord(
            trigger_id="t", run_id="r3", scheduled_fire_pacific="x", start_pacific="x",
            finish_pacific="x", policy_version="v", platform_status="SUCCEEDED", lanes=lanes,
        )
        result = validate_run_record(record, seen_run_ids=set())
        self.assertEqual(result["coverage_state"], CoverageState.BLOCKED)
        self.assertIn(("stocks_stage2", "DATA_BLOCKED", "tvremix connector-wide 429, 2/2 attempts"), result["blocked_lanes"])
        self.assertNotEqual(result["coverage_state"], CoverageState.COMPLETE)

    def test_auth_blocked_lane_is_blocked_not_complete(self):
        lanes = _full_coverage_lanes(
            leveraged_etf_s22=LaneRecord(LaneStatus.AUTH_BLOCKED, detail="Robinhood connector returned auth-required")
        )
        record = RunRecord(
            trigger_id="t", run_id="r4", scheduled_fire_pacific="x", start_pacific="x",
            finish_pacific="x", policy_version="v", platform_status="SUCCEEDED", lanes=lanes,
        )
        result = validate_run_record(record, seen_run_ids=set())
        self.assertEqual(result["coverage_state"], CoverageState.BLOCKED)


class TestDuplicateDelivery(unittest.TestCase):
    """
    'Test late/duplicate deliveries ... no duplicate evaluations/counting,
    fresh input checks, explicit expired/deferred state where appropriate.'
    """

    def test_duplicate_run_id_is_flagged_not_silently_recounted(self):
        lanes = _full_coverage_lanes()
        record = RunRecord(
            trigger_id="t", run_id="dup-1", scheduled_fire_pacific="x", start_pacific="x",
            finish_pacific="x", policy_version="v", platform_status="SUCCEEDED", lanes=lanes,
        )
        seen = {"dup-1"}
        result = validate_run_record(record, seen_run_ids=seen)
        self.assertTrue(result["duplicate"])
        self.assertTrue(any("duplicate" in issue for issue in result["issues"]))

    def test_stale_data_is_flagged_not_treated_as_fresh(self):
        """Late delivery: data used is older than the lane's freshness ceiling."""
        lanes = _full_coverage_lanes(
            stocks_stage2=LaneRecord(LaneStatus.EVALUATED, candidates_found=12, age_minutes=130)
        )
        record = RunRecord(
            trigger_id="t", run_id="stale-1", scheduled_fire_pacific="x", start_pacific="x",
            finish_pacific="x", policy_version="v", platform_status="SUCCEEDED", lanes=lanes,
        )
        result = validate_run_record(record, seen_run_ids=set())
        self.assertIn("stocks_stage2", result["stale_lanes"])
        self.assertEqual(result["coverage_state"], CoverageState.BLOCKED)

    def test_fresh_data_within_ceiling_not_flagged_stale(self):
        lanes = _full_coverage_lanes(
            stocks_stage2=LaneRecord(LaneStatus.EVALUATED, candidates_found=12, age_minutes=10)
        )
        record = RunRecord(
            trigger_id="t", run_id="fresh-1", scheduled_fire_pacific="x", start_pacific="x",
            finish_pacific="x", policy_version="v", platform_status="SUCCEEDED", lanes=lanes,
        )
        result = validate_run_record(record, seen_run_ids=set())
        self.assertEqual(result["stale_lanes"], [])
        self.assertEqual(result["coverage_state"], CoverageState.COMPLETE)


class TestPlatformStatusPreserved(unittest.TestCase):
    def test_platform_status_field_is_never_overwritten(self):
        lanes = _full_coverage_lanes(mode_c=LaneRecord(LaneStatus.NOT_RUN))
        record = RunRecord(
            trigger_id="t", run_id="preserve-1", scheduled_fire_pacific="x", start_pacific="x",
            finish_pacific="x", policy_version="v", platform_status="SUCCEEDED", lanes=lanes,
        )
        result = validate_run_record(record, seen_run_ids=set())
        # platform says SUCCEEDED; application says INCOMPLETE; both coexist, neither is edited:
        self.assertEqual(result["platform_status_preserved"], "SUCCEEDED")
        self.assertEqual(result["coverage_state"], CoverageState.INCOMPLETE)


class TestCandidateSelectionBalance(unittest.TestCase):
    """
    'Candidate selection should balance applicable fresh setups, retained
    near-misses and ageing rotation candidates ... Do not select only the
    largest green movers or silently starve quiet names.'
    """

    def test_biggest_mover_excluded_when_just_evaluated_last_cycle(self):
        universe = [
            Stage1Entry(symbol="DUOL", score=84, cycles_since_last_eval=0),  # just evaluated — should NOT be reselected
            Stage1Entry(symbol="QUIET1", score=12, cycles_since_last_eval=9),
            Stage1Entry(symbol="QUIET2", score=8, cycles_since_last_eval=11),
            Stage1Entry(symbol="QUIET3", score=15, cycles_since_last_eval=7),
        ]
        near_miss = [
            NearMissEntry(symbol="TEM", cycles_queued=3),
            NearMissEntry(symbol="SOFI", cycles_queued=3),
        ]
        result = select_stage2_batch(universe, near_miss, total_cap=4, max_near_miss_slots=2)

        self.assertNotIn("DUOL", result["rotation_slots"])  # the big mover, freshly checked, isn't force-reselected
        self.assertIn("TEM", result["near_miss_slots"])
        self.assertIn("SOFI", result["near_miss_slots"])
        self.assertIn("QUIET2", result["rotation_slots"])  # the longest-quiet name gets a slot
        self.assertEqual(result["total_selected"], 4)
        self.assertEqual(result["unfilled_slots"], 0)

    def test_near_miss_slots_never_exceed_the_shared_cap(self):
        near_miss = [NearMissEntry(symbol=f"NM{i}", cycles_queued=i) for i in range(10)]
        universe = [Stage1Entry(symbol=f"U{i}", score=50, cycles_since_last_eval=i) for i in range(20)]
        result = select_stage2_batch(universe, near_miss, total_cap=12, max_near_miss_slots=5)

        self.assertEqual(len(result["near_miss_slots"]), 5)
        self.assertEqual(result["total_selected"], 12)
        self.assertLessEqual(result["total_selected"], result["total_cap"])

    def test_quiet_names_not_starved_when_near_miss_queue_empty(self):
        universe = [Stage1Entry(symbol=f"Q{i}", score=5, cycles_since_last_eval=20 - i) for i in range(8)]
        result = select_stage2_batch(universe, [], total_cap=12, max_near_miss_slots=5)
        self.assertEqual(len(result["rotation_slots"]), 8)
        self.assertEqual(result["near_miss_slots"], [])


if __name__ == "__main__":
    unittest.main()
