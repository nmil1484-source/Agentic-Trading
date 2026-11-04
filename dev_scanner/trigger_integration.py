"""
Maps the EXISTING trades_log.md JSON cycle-summary schema into a RunRecord,
and detects a cycle whose trigger dispatched but whose protocol may never
have actually run — using only fields the live runtime already provides
(Claude_Code_Remote's `get_trigger().last_run`) plus trades_log.md's own
logged history. Non-transactional: reads already-logged data, computes,
returns a result. No network/tool/broker call, no order, no trigger edit.

Scope: Mode B/C entry-screening cycles (First Scan, Fresh Candle). Built
and fixture-tested against Fresh Candle (trig_01KrBsTt9mssjU4hPGtM3cBe)
specifically, per "starting with ONE existing scanning trigger."
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from dev_scanner.run_record import LaneRecord, LaneStatus, RunRecord


def _parse_utc(ts: str) -> datetime:
    # trades_log.md / get_trigger timestamps are RFC3339 UTC ('...Z' or '...+00:00' or with fractional seconds)
    ts = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(ts)


def map_fresh_candle_json_to_run_record(
    cycle_json: dict,
    *,
    trigger_id: str,
    run_id: str,
    policy_version: str,
) -> RunRecord:
    """
    Builds a RunRecord from one real Fresh Candle (or First Scan) cycle's
    already-logged JSON summary block. Honest by construction: a field the
    current schema does not actually carry maps to NOT_RUN with a detail
    explaining the gap — it is never inferred or assumed present.
    """
    lanes: dict[str, LaneRecord] = {}

    top_level_block = cycle_json.get("coverage_state")  # "DATA_BLOCKED" / "AUTH_BLOCKED" / "BUDGET_BLOCKED", when present

    coverage = cycle_json.get("coverage", {})
    universe_size = coverage.get("universe_size")
    triaged = coverage.get("triaged")
    full_gate_evaluated = coverage.get("full_gate_evaluated")

    # --- stocks_stage1 ---
    if top_level_block in ("DATA_BLOCKED", "AUTH_BLOCKED", "BUDGET_BLOCKED") and (not triaged):
        lanes["stocks_stage1"] = LaneRecord(LaneStatus(top_level_block), detail="cycle-level block, Stage 1 not completed")
    elif universe_size is not None and triaged == universe_size:
        lanes["stocks_stage1"] = LaneRecord(LaneStatus.EVALUATED, candidates_found=triaged)
    elif triaged:
        lanes["stocks_stage1"] = LaneRecord(LaneStatus.PARTIAL, detail=f"triaged {triaged} of {universe_size}")
    else:
        lanes["stocks_stage1"] = LaneRecord(LaneStatus.NOT_RUN, detail="no Stage-1 triage recorded this cycle")

    # --- stocks_stage2 ---
    if top_level_block in ("DATA_BLOCKED", "AUTH_BLOCKED", "BUDGET_BLOCKED") and not full_gate_evaluated:
        lanes["stocks_stage2"] = LaneRecord(LaneStatus(top_level_block), detail=str(coverage.get("not_evaluated")))
    elif full_gate_evaluated:
        lanes["stocks_stage2"] = LaneRecord(LaneStatus.EVALUATED, candidates_found=full_gate_evaluated)
    else:
        lanes["stocks_stage2"] = LaneRecord(LaneStatus.NOT_RUN, detail="no Stage-2 full-gate evaluations recorded this cycle")

    # --- leveraged_etf_s22 ---
    etf = cycle_json.get("leveraged_etf_coverage")
    if etf is None:
        lanes["leveraged_etf_s22"] = LaneRecord(LaneStatus.NOT_RUN, detail="leveraged_etf_coverage field absent from this cycle's JSON")
    elif etf.get("coverage_complete") is True:
        lanes["leveraged_etf_s22"] = LaneRecord(LaneStatus.EVALUATED, candidates_found=etf.get("evaluated", 0))
    elif etf.get("evaluated", 0) > 0:
        lanes["leveraged_etf_s22"] = LaneRecord(LaneStatus.PARTIAL, detail=f"{etf.get('evaluated')} of {etf.get('universe_size')} evaluated")
    else:
        not_eval = etf.get("not_evaluated", [])
        is_tool_failure = any("tool failure" in str(e.get("reason", "")).lower() or "429" in str(e.get("reason", "")) for e in not_eval if isinstance(e, dict))
        status = LaneStatus.DATA_BLOCKED if is_tool_failure else LaneStatus.NOT_RUN
        lanes["leveraged_etf_s22"] = LaneRecord(status, detail=f"0 of {etf.get('universe_size')} evaluated; coverage_complete=False")

    # --- options_sourcing_s18 / leaps_sourcing_s19 ---
    # The CURRENT live schema has no dedicated field for candidate-SOURCING
    # coverage (§18 item 11 / §19 item 8) — only `options_stop_check`, which
    # covers the protective stop-check on an ALREADY-OPEN position (§18
    # item 4 / §19 item 3), a different question. Until the schema is
    # extended (see README), these two lanes can never be anything but
    # NOT_RUN from real historical data — that is the honest mapping, not
    # a bug in this function.
    lanes["options_sourcing_s18"] = LaneRecord(
        LaneStatus.NOT_RUN,
        detail="no dedicated field in the current cycle-JSON schema (conflated with options_stop_check historically)",
    )
    lanes["leaps_sourcing_s19"] = LaneRecord(
        LaneStatus.NOT_RUN,
        detail="no dedicated field in the current cycle-JSON schema (conflated with options_stop_check historically)",
    )

    # --- options_leaps_stop_check ---
    stop_check = cycle_json.get("options_stop_check")
    if stop_check is None:
        lanes["options_leaps_stop_check"] = LaneRecord(LaneStatus.NOT_RUN, detail="options_stop_check field absent this cycle")
    else:
        # checked:0 is logged under the existing convention to mean "0 open
        # positions, nothing to check" — but the schema cannot actually
        # distinguish that from "the check was never attempted." Flagged
        # here rather than silently assumed.
        lanes["options_leaps_stop_check"] = LaneRecord(
            LaneStatus.SKIPPED_NA,
            detail="checked:0 in source schema — ambiguous between '0 open positions' and 'not attempted'; see README",
        )

    # --- mode_c ---
    mc = cycle_json.get("mode_c")
    if mc is None:
        lanes["mode_c"] = LaneRecord(LaneStatus.NOT_RUN, detail="mode_c field absent from this cycle's JSON entirely")
    elif mc.get("dedicated_screen_performed") is True:
        lanes["mode_c"] = LaneRecord(LaneStatus.EVALUATED, candidates_found=mc.get("candidates", 0))
    elif mc.get("dedicated_screen_performed") == "partial":
        lanes["mode_c"] = LaneRecord(
            LaneStatus.PARTIAL,
            detail=f"partial screen: {mc.get('partial_screen_of_universe', 'extent unknown')}",
        )
    else:
        reason = mc.get("reason")
        detail = reason if reason else "dedicated_screen_performed:false, NO reason given — silent gap"
        lanes["mode_c"] = LaneRecord(LaneStatus.NOT_RUN, detail=detail)

    return RunRecord(
        trigger_id=trigger_id,
        run_id=run_id,
        scheduled_fire_pacific=cycle_json.get("timestamp_pacific", ""),
        start_pacific=cycle_json.get("timestamp_pacific", ""),
        finish_pacific=None,
        policy_version=policy_version,
        platform_status="SUCCEEDED",  # cycle_json only exists because a session logged it; dispatch-level status is separate, see detect_cycle_completion
        lanes=lanes,
        tvremix_calls_used_today=cycle_json.get("tvremix_calls_used_today", 0),
    )


def detect_cycle_completion(
    trigger_last_run: dict,
    logged_entries: list,
    *,
    warn_lag_minutes: float = 10.0,
    max_lag_minutes: float = 30.0,
) -> dict:
    """
    trigger_last_run: the `last_run` object exactly as returned by
        get_trigger() — {"status", "fired_at", "finished_at", ...}.
    logged_entries: list of {"cycle": str, "timestamp_utc": str} already
        parsed from trades_log.md for this trigger (caller's job to filter
        to the right trigger/cycle-name; kept out of this function so it
        stays pure and testable without touching the filesystem).

    A near-zero (finished_at - fired_at) gap is NEVER itself evidence of
    completed work — Claude_Code_Remote's dispatch marks a persistent-
    session trigger "finished" the moment the message is queued, not when
    the session actually processes it. This is measured directly from two
    real fired_at/finished_at pairs logged this session (both ~10ms gaps
    on cycles that in fact took 10+ minutes of real work to actually log).
    """
    fired_at = _parse_utc(trigger_last_run["fired_at"])
    finished_at = _parse_utc(trigger_last_run["finished_at"])
    dispatch_gap_seconds = (finished_at - fired_at).total_seconds()

    best_match = None
    best_lag_minutes = None
    for entry in logged_entries:
        entry_time = _parse_utc(entry["timestamp_utc"])
        lag = (entry_time - fired_at).total_seconds() / 60.0
        if lag < -1:
            continue  # a logged entry materially BEFORE this fire can't be this cycle's own record
        if best_lag_minutes is None or lag < best_lag_minutes:
            best_lag_minutes = lag
            best_match = entry

    if best_match is None or best_lag_minutes > max_lag_minutes:
        status = "LIKELY_SILENT_SKIP"
    elif best_lag_minutes > warn_lag_minutes:
        status = "FOUND_LATE"
    else:
        status = "FOUND_ON_TIME"

    return {
        "status": status,
        "dispatch_gap_seconds": dispatch_gap_seconds,
        "dispatch_gap_is_evidence_of_work": False,  # always False — stated as an explicit field, not just a comment
        "matched_entry": best_match,
        "lag_minutes": best_lag_minutes,
    }
