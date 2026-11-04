"""
Wiring between on-disk state (near_miss_queue.md, a proposed new
rotation_state.json) and candidate_selection.select_stage2_batch()'s
input types. Non-transactional: file reads/writes only, no network, no
broker, no order.

rotation_state.json does not exist yet in this repository — it is
PROPOSED new state, parallel to trades_log.md/near_miss_queue.md, not
created or written by this patch. See README for why it's needed and
what populates it going forward if adopted.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from dev_scanner.candidate_selection import NearMissEntry, Stage1Entry

_ROW_RE = re.compile(
    r"^\|\s*([A-Z]{1,6})\s*\|.*\|\s*(\d+)\s*\|\s*\d{4}-\d{2}-\d{2}\s*\|\s*$"
)
# Matches a genuine single-line queue row: "| SYMBOL | ... | <cycles_checked:int> | <expires:date> |"
# Deliberately strict: a malformed/struck-through/multi-line historical
# "removed" entry (e.g. "| ~~ZETA~~ | **REMOVED ...") will NOT match this
# pattern and is correctly excluded, not mis-parsed.


def parse_near_miss_queue(markdown_text: str, *, section_heading: str = "## Current queue — Mode B/C equities") -> list[NearMissEntry]:
    """
    Extracts live (not struck-through/removed) rows from the named section
    of near_miss_queue.md. Stops at the next '## ' heading. Returns one
    NearMissEntry per genuinely still-queued symbol, cycles_queued taken
    from the table's own 'Cycles checked' column.
    """
    lines = markdown_text.splitlines()
    in_section = False
    entries: list[NearMissEntry] = []

    for line in lines:
        if line.startswith("## "):
            if in_section:
                break  # left the target section
            in_section = line.startswith(section_heading)
            continue
        if not in_section:
            continue
        if line.startswith("| Symbol") or line.startswith("|---"):
            continue  # header / separator row
        if "~~" in line:
            continue  # struck-through / removed historical entry — never a live row
        m = _ROW_RE.match(line.strip())
        if m:
            symbol, cycles_checked = m.group(1), int(m.group(2))
            entries.append(NearMissEntry(symbol=symbol, cycles_queued=cycles_checked))

    return entries


def load_rotation_state(path: Path) -> dict:
    """{symbol: last_full_eval_utc_iso}. Missing file -> empty state (cold start), not an error."""
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save_rotation_state(path: Path, state: dict) -> None:
    path.write_text(json.dumps(state, indent=2, sort_keys=True))


def compute_stage1_entries(
    universe_symbols: list[str],
    rotation_state: dict,
    *,
    now_utc: Optional[datetime] = None,
    cycle_interval_minutes: int = 60,
    never_evaluated_sentinel: int = 9999,
) -> list[Stage1Entry]:
    """
    Converts raw rotation_state timestamps into the
    cycles_since_last_eval figure select_stage2_batch() actually sorts on.
    Stage-1 `score` is intentionally left at 0 here — candidate_selection's
    rotation logic never uses score, by design (see that module's own
    docstring); score is wired in separately, for prioritization context
    only, by whatever Stage-1 step produced the ranked universe.
    """
    now = now_utc or datetime.now(timezone.utc)
    out = []
    for symbol in universe_symbols:
        last_eval_iso = rotation_state.get(symbol)
        if last_eval_iso is None:
            cycles_since = never_evaluated_sentinel
        else:
            last_eval = datetime.fromisoformat(last_eval_iso.replace("Z", "+00:00"))
            minutes_since = (now - last_eval).total_seconds() / 60.0
            cycles_since = max(int(minutes_since // cycle_interval_minutes), 0)
        out.append(Stage1Entry(symbol=symbol, score=0.0, cycles_since_last_eval=cycles_since))
    return out
