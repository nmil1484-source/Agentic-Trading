"""
Non-transactional Stage-2 candidate-selection balancer.

Mirrors the selection policy in CLAUDE.md's "Screening Coverage and Triage
Methodology" subsection (§5B) as testable code, separate from the live
trigger prompt's own prose description of the same rule. This module does
not evaluate any entry gate itself and does not place, size, or affect any
order — it only decides WHICH names receive a Stage-2 slot this cycle,
given the cycle's known inputs. It is a pure function over its inputs: no
network calls, no broker access, no file I/O.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Stage1Entry:
    symbol: str
    score: float  # Stage-1 technical score — context/prioritization only, never itself a gate
    cycles_since_last_eval: int  # rotation age; a never-evaluated name should be given a large value


@dataclass
class NearMissEntry:
    symbol: str
    cycles_queued: int


def select_stage2_batch(
    universe: List[Stage1Entry],
    near_miss_queue: List[NearMissEntry],
    *,
    total_cap: int = 12,
    max_near_miss_slots: int = 5,
) -> dict:
    """
    Returns {"near_miss_slots": [...], "rotation_slots": [...], ...}.

    - Near-miss slots: up to max_near_miss_slots, longest-queued first.
      These are consumed FROM total_cap, never in addition to it, per the
      policy's explicit "never in addition to" rule.
    - Rotation slots: fill whatever capacity remains, by
      least-recently-evaluated-first (largest cycles_since_last_eval
      first) — deliberately NOT by Stage-1 score. A name's Stage-1 score
      (how big a mover it is) is explicitly excluded as a selection
      criterion here, matching the policy's "large percentage mover is
      never a precondition for a Stage-2 slot" rule — this is what keeps
      a big one-day gap from crowding out quieter, longer-queued names.
    """
    if max_near_miss_slots > total_cap:
        raise ValueError("max_near_miss_slots cannot exceed total_cap")

    near_miss_sorted = sorted(near_miss_queue, key=lambda e: -e.cycles_queued)
    near_miss_slots = [e.symbol for e in near_miss_sorted[:max_near_miss_slots]]

    remaining = total_cap - len(near_miss_slots)
    already_taken = set(near_miss_slots)
    rotation_candidates = [u for u in universe if u.symbol not in already_taken]
    rotation_sorted = sorted(rotation_candidates, key=lambda u: -u.cycles_since_last_eval)
    rotation_slots = [u.symbol for u in rotation_sorted[: max(remaining, 0)]]

    return {
        "near_miss_slots": near_miss_slots,
        "rotation_slots": rotation_slots,
        "total_selected": len(near_miss_slots) + len(rotation_slots),
        "total_cap": total_cap,
        "unfilled_slots": max(total_cap - len(near_miss_slots) - len(rotation_slots), 0),
    }
