# Integration proposal (NOT applied) — Fresh Candle trigger only

Scope, per instruction: smallest concrete integration diff, starting with
**one** existing scanning trigger — `trig_01KrBsTt9mssjU4hPGtM3cBe`
("Mode B/C Entry Screening — Fresh Candle"). First Scan is intentionally
left untouched pending review of this one trigger's result. **Nothing in
this file has been applied to the live trigger.** No order, risk limit,
permission, schedule, stop, or existing order is touched by anything
here.

## 1. Completion reporting — where real evidence maps into RunRecord

`dev_scanner/trigger_integration.py` → `map_fresh_candle_json_to_run_record()`
takes exactly the JSON block the live cycle already produces at step 15
and maps each field into a lane. Tested against **three real, verbatim
cycle exports** from this repo's own `trades_log.md` (not paraphrased —
copied as logged): `2026-11-04T16:14:54Z`, `2026-11-04T17:14:23Z`,
`2026-11-04T18:04:13Z`. See `test_integration_e2e.py`.

The mapping is deliberately honest about what the *current* schema can
and cannot say:

| Lane | Source field today | What's real vs. assumed |
|---|---|---|
| `stocks_stage1` / `stocks_stage2` | `coverage.triaged` / `.full_gate_evaluated` vs `universe_size`, and the top-level `coverage_state` when present | Real counts; `DATA_BLOCKED` etc. propagated directly, not re-derived |
| `leveraged_etf_s22` | `leveraged_etf_coverage.coverage_complete`/`.evaluated` | Real; a tool-failure reason string drives `DATA_BLOCKED` vs `NOT_RUN` |
| **`options_sourcing_s18`** | **none exists** | **Always `NOT_RUN`, explicitly.** The live schema has never tracked §18 item 11 candidate *sourcing* separately from the stop-check. This is not a mapping bug — it's the real gap items (1) and (2) of the request both point at. |
| **`leaps_sourcing_s19`** | **none exists** | Same — always `NOT_RUN` under the current schema. |
| `options_leaps_stop_check` | `options_stop_check.checked` | `SKIPPED_NA`, flagged with a caveat: `checked:0` is ambiguous between "0 open positions" and "never attempted" in the *current* schema — this function cannot resolve that ambiguity from the field alone (see Remaining limitations). |
| `mode_c` | `mode_c.dedicated_screen_performed` (+ optional `.reason`) | `True`→`EVALUATED`, `"partial"`→`PARTIAL`, `False`→`NOT_RUN`. **The 17:14:23Z real fixture has `False` with no `reason` field at all** — this is the literal, already-on-file "missing work silently absorbed into a clean-looking cycle" case. `test_silent_mode_c_gap_is_caught_same_as_disclosed_one` proves the validator catches it exactly like the 16:14:54Z cycle that *did* disclose a reason — disclosure in the prose doesn't matter; the structured field is what's checked. |

**Why "swing options" and "independent LEAPS" needed separate lanes, not
just reusing `options_stop_check`:** the stop-check (step 2b) answers "is
an *already-open* position's stop still correct?" — a protective-exit
question, always in scope regardless of new-candidate budget. Sourcing
(steps 3a/3b) answers "did we look for *new* options/LEAPS candidates
this cycle?" — a screening-coverage question. Collapsing them into one
field (as today's schema does) means a cycle that skipped sourcing
entirely but had zero open options positions (so `options_stop_check`
trivially reads `{"checked":0,...}`) looks identical in the log to a
cycle that genuinely checked sourcing and found nothing. `run_record.py`
tracks them as two separate required lanes specifically so that
distinction becomes visible.

## 1b. Detecting a cycle that never reaches the final validator

`detect_cycle_completion()` answers this using only fields the runtime
already exposes: `get_trigger(trigger_id).last_run` (`fired_at`,
`finished_at`, `status`) plus whatever's already logged in
`trades_log.md`. The key empirical finding, measured from **two real
pairs on file this session**, not assumed:

- `trig_01KrBsTt9mssjU4hPGtM3cBe` fired `2026-11-04T16:04:20.496Z`,
  `finished_at` `...507Z` — an **11ms** dispatch gap. Real work was
  logged **10.6 minutes later**, at `16:14:54Z` (confirmed via this
  session's own diagnostic, `trades_log.md` line 57612:
  `"log_entry_found": false` at the time it was first checked, 5 minutes
  after the fire).
- The same trigger's *next* fire, `17:04:05.835208Z` → `...843945Z`
  (**8.7ms** gap), has its nearest matching log entry at `17:14:23Z` —
  **10.3 minutes later**. Same pattern, independently measured.

**The dispatch gap is near-zero on every single real fire examined this
session, regardless of whether real work followed quickly, slowly, or (in
the one confirmed case, 16:04:20Z) not at all until manually caught.**
This is the concrete, already-logged evidence that `finished_at -
fired_at` is dispatch-queueing latency, not cycle-completion time — it
can never be used as completion evidence, and `detect_cycle_completion()`
encodes that as an explicit `dispatch_gap_is_evidence_of_work: False`
field rather than a comment, so nothing downstream can mistake a fast
dispatch for a fast cycle.

The function then looks for the nearest same-trigger `trades_log.md`
entry at or after `fired_at`:
- found within 10 min → `FOUND_ON_TIME`
- found within 10–30 min → `FOUND_LATE` (both real fixtures above land
  here — a ~10 min processing lag appears to be this session's normal
  pattern when a trigger fires mid-other-work, not necessarily a fault
  each time)
- nothing within 30 min → `LIKELY_SILENT_SKIP` (synthetic fixture only —
  no real on-file example of a fire that was *never* eventually caught;
  the one real near-miss was caught at ~5 minutes via manual diagnostic,
  before this detector would even have fired)

This is read-only analysis over already-logged data — it does not watch
triggers live, does not poll, and does not itself write anything.

## 2. Candidate selection — where it's actually invoked, and what its output feeds

Demonstrated against real data, not just asserted in a test:

```
$ python3 -c "
from pathlib import Path
from dev_scanner.rotation_state import parse_near_miss_queue, compute_stage1_entries
from dev_scanner.candidate_selection import select_stage2_batch
near_miss = parse_near_miss_queue(Path('near_miss_queue.md').read_text())
stage1 = compute_stage1_entries([...74 watchlist names...], rotation_state={})
print(select_stage2_batch(stage1, near_miss, total_cap=12, max_near_miss_slots=5))
"
near_miss_slots: ['TEM', 'SOFI', 'PGY', 'IGV']
rotation_slots:  ['TSM', 'HPE', 'NBIS', 'ONDS', 'CBRS', 'VRT', 'STM', 'BE']
```

That is the **exact same 12-name batch** (4 queued near-misses + 8
rotation names) I hand-selected for the real `18:04:13Z` Fresh Candle
cycle earlier this session — the formalized function reproduces what was
previously done by hand, which is the actual cross-check that it encodes
the right policy, not a different one. (`rotation_state={}` here is a
cold start — see Remaining limitations: `rotation_state.json` doesn't
exist yet, so every name starts at the "never evaluated" sentinel and
rotation order among non-near-miss names is effectively unordered until
the first cycle populates it.)

**Invocation point, proposed:** at the top of the trigger prompt's
existing step 3 ("Screen watchlist.md against BOTH the full §5B Swing
Entry Gate..."), *before* the Stage-2 rotation batch is drawn by hand.
**Output destination:** `select_stage2_batch()`'s `near_miss_slots +
rotation_slots` becomes the literal symbol list passed to
`analyze_structure_batch(symbols=<that list>, ...)` in the existing Stage
2 step — i.e. it decides *which 12 names get the real market-data call*,
it does not replace or skip that call. **It evaluates nothing itself** —
after the batch call returns real structure data, the cycle still does
its own §5B/Bearish-Mirror/§13.G walk-through exactly as before; this
module only answers "which names," never "do they qualify." This is the
direct answer to "logging omissions alone does not complete breakout
checks or Mode C" — selection code and evaluation code are different
things, and this patch is explicit that it only replaces the former.

## Proposed trigger-text diff (NOT applied)

Two targeted insertions into Fresh Candle's live prompt text, shown as a
diff against the verbatim text fetched from `get_trigger()` this session.

```diff
@@ Stage 2 — full-gate evaluation, bounded and rotated: @@
-- **Stage 2 — full-gate evaluation, bounded and rotated:** fully evaluate a cycle-specific batch
-  of candidates against §5B/the Bearish Mirror Gate/§20 item 5 as applicable. Select that batch by
-  least-recently-fully-evaluated-first rotation (track each name's last full-evaluation timestamp
-  in trades_log.md's history; never-evaluated names count as oldest). ...
++ **Stage 2 — full-gate evaluation, bounded and rotated.** Compute this cycle's 12-name batch via
++ the dev_scanner integration (pending review — do NOT run this until approved):
++ `python3 -c "from dev_scanner.rotation_state import parse_near_miss_queue, load_rotation_state,
++ compute_stage1_entries; from dev_scanner.candidate_selection import select_stage2_batch; from
++ pathlib import Path; nm = parse_near_miss_queue(Path('near_miss_queue.md').read_text()); rs =
++ load_rotation_state(Path('rotation_state.json')); s1 =
++ compute_stage1_entries(<current watchlist.md universe>, rs); print(select_stage2_batch(s1, nm))"`
++ — the printed `near_miss_slots + rotation_slots` list IS this cycle's Stage-2 batch, fed directly
++ into the existing `analyze_structure_batch(symbols=<that list>, ...)` call below. Evaluation
++ (§5B/Bearish-Mirror/§13.G) proceeds exactly as it already does on that batch's returned data —
++ this step only changes how the batch is chosen, nothing about how it's evaluated. After Stage 2
++ completes, update `rotation_state.json` with each evaluated name's timestamp (new step, see
++ below) — this file does not yet exist; its first real population happens on first live use.

@@ step 15 — ALWAYS, regardless of outcome: append one entry to trades_log.md @@
   ...tvremix_calls_used_today (running count, reset at the UTC day boundary), exits, entries,
   orders_placed, git_push), then git add trades_log.md near_miss_queue.md && git commit ...
++
++ 15b. **Application-level coverage check (pending review — do NOT run this until approved).**
++ Build this cycle's RunRecord from the step-15 JSON via
++ `dev_scanner.trigger_integration.map_fresh_candle_json_to_run_record()`, run
++ `validate_run_record()` against it, and log the result as an additional
++ `application_coverage_state` field in the same JSON block — never replacing `coverage_state` or
++ any existing field, only adding alongside it. If `application_coverage_state` is
++ INCOMPLETE/BLOCKED while the platform's own dispatch reads SUCCEEDED, state both explicitly in
++ the narrative, exactly as 15b's own validator already does in its `issues` list.
```

This diff is **illustrative and precise about insertion points**, not a
literal drop-in — the real edit would go through the same
`get_trigger`/`update_trigger` full-prompt-replacement process used for
the 2026-11-04 coverage-repair patch, reconstructing the complete prompt
text with these two sections added. Not performed by this proposal.

## Tests performed — helper vs. end-to-end, explicitly distinguished

- **Helper tests** (`test_dev_scanner.py`, 12 tests): pure logic against
  hand-constructed synthetic inputs — `run_record.py` and
  `candidate_selection.py` in isolation. No file I/O.
- **End-to-end tests** (`test_integration_e2e.py`, 10 tests): real
  exported `trades_log.md` JSON (3 cycles, verbatim) run through the
  actual mapping function; real `get_trigger()` `last_run` data (2 fires,
  verbatim) run through the actual skip-detector; the real
  `near_miss_queue.md` file on disk parsed by the actual parser. One
  fixture (`test_synthetic_true_silent_skip...`) is explicitly labeled
  SYNTHETIC because no real on-file example of a true, never-caught
  silent skip exists — flagged rather than passed off as real.

```
$ python3 -m unittest dev_scanner.test_dev_scanner dev_scanner.test_integration_e2e -v
...
Ran 22 tests in 0.003s
OK
```

## Call-budget impact

- **Actual, measured this session:** zero. Every test and the
  demonstration above ran against in-memory data or local files already
  on disk (`near_miss_queue.md`). No `analyze_structure_batch`,
  `rank_symbol_setups`, or Robinhood call was made by any of this code.
- **Estimated, if wired into the live cycle:** also zero *incremental*
  calls. `select_stage2_batch()` only decides which symbols go into the
  Stage-2 `analyze_structure_batch` call the trigger already makes every
  cycle (1 call, per the existing tvremix-budget note) — it does not add
  a call, and it does not change the existing Stage-1 call either. The
  validator (`validate_run_record`) runs after all data has already been
  fetched and logged, purely as a local computation over that cycle's own
  JSON — also zero calls. Net projected change to the existing ~2
  calls/cycle, ~10/day Fresh Candle budget: **+0**.

## Remaining limitations (honest, not glossed over)

1. **`rotation_state.json` does not exist yet.** Without it,
   `compute_stage1_entries()` starts every name at the "never evaluated"
   sentinel every time it's called cold — rotation among non-near-miss
   names is effectively unordered until a live cycle populates the file
   at least once. This is a real gap this proposal surfaces but does not
   close; populating it retroactively from `trades_log.md`'s own history
   (74 names × many cycles of free-text evaluation mentions) was judged
   out of scope for "smallest."
2. **`options_leaps_stop_check`'s `checked:0` ambiguity is not resolved**
   by this patch — the current schema cannot distinguish "confirmed zero
   open positions" from "the check was never attempted" from the JSON
   alone. Closing this needs a schema change to the live step 2b (e.g. an
   explicit `open_positions_count` field), which is a larger edit than
   this proposal's scope.
3. **This validator is still not wired into any live cycle.** Everything
   above is proven against real, already-logged data and a real,
   already-on-disk file — not yet proven against a live firing that
   actually calls this code mid-cycle. That remains the next integration
   step, explicitly deferred to your review per the proposed diff above.
4. **The proposed trigger-text diff is not syntactically a true unified
   diff against the full live prompt** (reproducing the entire ~9KB
   prompt text here was judged unnecessary noise for review) — it shows
   the two exact insertion points and the exact text to add, which is
   what a reviewer needs to approve or reject the change; the literal
   `update_trigger` full-text reconstruction would happen only after
   approval.
