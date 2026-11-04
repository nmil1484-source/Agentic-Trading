"""
Application-level run-record schema and validator for Mode B/C scanner cycles.

NON-TRANSACTIONAL, READ-ONLY DEVELOPMENT CODE. This module places no order,
modifies no order, routes nothing, and does not alter any live trigger,
schedule, account permission, risk limit, stop, or policy. It defines the
structured record a scanner cycle SHOULD produce, as a layer distinct from
the scheduler's own dispatch status, per the 2026-11-04 "Focused scanner
repair request" item 2: a platform "SUCCEEDED" dispatch is never, by
itself, evidence that the cycle's required evaluation work actually
completed. The platform's own status is always preserved verbatim
(`platform_status`) — this module never pretends to change scheduler
semantics; it only computes and exposes a second, independent
`coverage_state`.

Scope: Mode B/C entry-screening cycles (First Scan, Fresh Candle) only.
Crypto keeps its own separate cycle/record (explicitly out of scope here,
per the request). Mode A remains research-only — no run-record requirement.

This file is new, dev-only code — not wired into any live trigger prompt,
not imported by anything that executes against the broker. Integrating it
(e.g. having each cycle's JSON summary validated against this schema
before being logged) is a proposed next step, pending separate review —
not performed by this patch.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class LaneStatus(str, Enum):
    EVALUATED = "EVALUATED"          # applicable checks ran with usable evidence this cycle
    PARTIAL = "PARTIAL"              # some but not all required sub-steps completed
    AUTH_BLOCKED = "AUTH_BLOCKED"    # a required connector returned auth-required, not data
    DATA_BLOCKED = "DATA_BLOCKED"    # a tool call failed after its normal retry
    BUDGET_BLOCKED = "BUDGET_BLOCKED"  # a shared daily call reserve was exhausted
    NOT_RUN = "NOT_RUN"              # this lane's step was never attempted this cycle
    SKIPPED_NA = "SKIPPED_NA"        # genuinely structurally inapplicable this cycle


class CoverageState(str, Enum):
    COMPLETE = "COMPLETE"
    INCOMPLETE = "INCOMPLETE"
    BLOCKED = "BLOCKED"


# The lanes CLAUDE.md requires every eligible Mode B/C cycle to address.
# "swing options" / "independent LEAPS" are candidate-SOURCING lanes (§18
# item 11 / §19 item 8) — distinct from the options/LEAPS protective
# STOP-CHECK lane for already-open positions (§18 item 4 / §19 item 3).
# The trigger prompts' current JSON schema conflates these two under one
# `options_stop_check` field; this module tracks them as separate required
# lanes, which is itself one of the gaps this patch surfaces (see README).
REQUIRED_LANES_MODE_BC = (
    "stocks_stage1",
    "stocks_stage2",
    "leveraged_etf_s22",
    "options_sourcing_s18",
    "leaps_sourcing_s19",
    "options_leaps_stop_check",
    "mode_c",
)

# A lane may be SKIPPED_NA only when it can be structurally inapplicable
# this cycle for a reason unrelated to coverage (e.g. zero open options
# positions to stop-check). A required screening lane (stocks, §22 ETFs,
# Mode C, candidate sourcing) is never allowed to claim SKIPPED_NA — doing
# so is flagged as a misuse, not accepted as coverage.
LANES_ALLOWING_SKIPPED_NA = {"options_leaps_stop_check"}

_BLOCKED_STATUSES = {LaneStatus.AUTH_BLOCKED, LaneStatus.DATA_BLOCKED, LaneStatus.BUDGET_BLOCKED}


@dataclass
class LaneRecord:
    status: LaneStatus
    detail: str = ""
    candidates_found: int = 0
    data_timestamp_pacific: Optional[str] = None
    age_minutes: Optional[float] = None  # age of the data actually used, at the time it was used


@dataclass
class RunRecord:
    trigger_id: str
    run_id: str  # unique per actually-fired instance, e.g. f"{trigger_id}:{scheduled_fire_utc}"
    scheduled_fire_pacific: str
    start_pacific: str
    finish_pacific: Optional[str]
    policy_version: str      # e.g. "EP-v2.1, 2026-11-03" — read live from CLAUDE.md at run time
    platform_status: str     # the scheduler's own reported status, e.g. "SUCCEEDED" — never overwritten
    lanes: dict = field(default_factory=dict)  # lane_name -> LaneRecord
    tvremix_calls_used_today: int = 0
    notes: str = ""

    def required_lanes(self) -> tuple:
        return REQUIRED_LANES_MODE_BC


# Freshness ceilings per lane, in minutes — how old the data used to
# evaluate a lane may be before it's treated as stale/expired rather than
# "the current candle." Mode B/C equities use hourly candles; a read taken
# more than one full cycle-interval (here, ~65 min with a small buffer) old
# is a late/stale delivery, not fresh evidence for a new decision.
DEFAULT_LANE_FRESHNESS_MINUTES = {
    "stocks_stage1": 65,
    "stocks_stage2": 65,
    "leveraged_etf_s22": 65,
    "options_sourcing_s18": 65,
    "leaps_sourcing_s19": 24 * 60,  # LEAPS research gate is weekly/daily-basis, not hourly
    "options_leaps_stop_check": 24 * 60,  # checked at least once/trading day per §18/§19
    "mode_c": 65,
}


def validate_run_record(
    record: RunRecord,
    *,
    seen_run_ids: set,
    lane_freshness_limits_minutes: Optional[dict] = None,
) -> dict:
    """
    Computes the APPLICATION-level coverage_state, independent of and never
    overriding record.platform_status. Returns:
      coverage_state, missing_lanes, blocked_lanes, stale_lanes,
      duplicate, issues (human-readable), platform_status_preserved.
    """
    limits = lane_freshness_limits_minutes or DEFAULT_LANE_FRESHNESS_MINUTES
    issues: list[str] = []
    missing: list[str] = []
    blocked: list[tuple] = []
    stale: list[str] = []

    duplicate = record.run_id in seen_run_ids
    if duplicate:
        issues.append(
            f"run_id '{record.run_id}' already present in the run-record history — "
            "treated as a duplicate delivery, not re-evaluated or re-counted"
        )

    for lane_name in record.required_lanes():
        lane = record.lanes.get(lane_name)

        if lane is None or lane.status == LaneStatus.NOT_RUN:
            missing.append(lane_name)
            issues.append(f"required lane '{lane_name}' is NOT_RUN or absent this cycle")
            continue

        if lane.status == LaneStatus.SKIPPED_NA and lane_name not in LANES_ALLOWING_SKIPPED_NA:
            missing.append(lane_name)
            issues.append(
                f"lane '{lane_name}' marked SKIPPED_NA, but this lane is never "
                "structurally optional — treated as missing coverage, not addressed"
            )
            continue

        if lane.status in _BLOCKED_STATUSES:
            blocked.append((lane_name, lane.status.value, lane.detail))
            continue

        if lane.status == LaneStatus.PARTIAL:
            blocked.append((lane_name, "PARTIAL", lane.detail))
            issues.append(f"lane '{lane_name}' only partially covered: {lane.detail or 'no detail given'}")
            continue

        # lane.status is EVALUATED or an allowed SKIPPED_NA from here on —
        # still subject to a freshness check before being trusted.
        limit = limits.get(lane_name)
        if limit is not None and lane.age_minutes is not None and lane.age_minutes > limit:
            stale.append(lane_name)
            issues.append(
                f"lane '{lane_name}' evidence is {lane.age_minutes:.0f} min old, "
                f"exceeding the {limit} min freshness ceiling — treated as stale, "
                "not fresh evidence for a new decision this cycle"
            )

    if missing:
        coverage_state = CoverageState.INCOMPLETE
    elif blocked or stale:
        coverage_state = CoverageState.BLOCKED
    else:
        coverage_state = CoverageState.COMPLETE

    if record.platform_status == "SUCCEEDED" and coverage_state != CoverageState.COMPLETE:
        issues.append(
            "platform reported SUCCEEDED, but application coverage_state is "
            f"{coverage_state.value} — platform_status is preserved as-is below; "
            "it is never treated as proof the cycle's work actually completed"
        )

    return {
        "coverage_state": coverage_state,
        "missing_lanes": missing,
        "blocked_lanes": blocked,
        "stale_lanes": stale,
        "duplicate": duplicate,
        "issues": issues,
        "platform_status_preserved": record.platform_status,
    }
