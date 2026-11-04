# dev_scanner — non-transactional development patch (pending review)

Scope: this directory implements the two remaining behaviors from the
2026-11-04 "Focused scanner repair request." It is **new, dev-only code**:
not imported by anything that executes against the broker, not wired into
any live trigger prompt, not referenced by CLAUDE.md. Nothing here places,
modifies, routes, or cancels an order, and nothing here alters a live
trigger, schedule, account permission, risk limit, or stop.

## What's here

- `run_record.py` — defines `RunRecord`/`LaneRecord` and
  `validate_run_record()`, which computes an **application-level**
  `coverage_state` (COMPLETE / INCOMPLETE / BLOCKED) independent of, and
  never overriding, the platform's own `platform_status`
  (e.g. `"SUCCEEDED"`). A platform-SUCCEEDED dispatch with a missing or
  blocked required lane is reported as INCOMPLETE/BLOCKED, with the
  platform status preserved verbatim alongside it — not replaced.
- `candidate_selection.py` — `select_stage2_batch()`, a pure function
  implementing the Stage-2 selection balance already described in prose
  in the live trigger prompts (near-miss reassessment slots, then
  least-recently-evaluated-first rotation) — as real, independently
  testable code, so the "don't just chase the biggest mover" rule is an
  assertion a test suite can actually check, not only a sentence in a
  prompt.
- `test_dev_scanner.py` — 12 tests, one per "VALIDATE WITHOUT ORDERS"
  bullet in the request. All pass (`python3 -m unittest
  dev_scanner.test_dev_scanner -v` → `Ran 12 tests ... OK`).

## Item 1 — DUOL regression case: reused, not re-run

Per the request's own "do not duplicate the patch ... or claim an
already-fixed issue is still missing," DUOL's full §13.G walk-through was
already completed as a live read-only diagnostic this session (see
`trades_log.md`, entry timestamped `2026-11-04T18:22:38Z`, commit
`e54a112`): verified dated catalyst, confirmed fresh-high condition on the
60-minute chart, identified the actual completed hourly trigger candle,
computed the §13.H volume baseline with an explicit reduced-sample
disclosure, and reached a definitive **REJECTED** result (§13.G item 2 —
volume 0.28x of baseline, far below the 1.2x floor) — independent of R:R,
and without ever being blocked by `setup: null`.

`test_duol_reaches_evaluation_and_is_rejected_on_evidence_not_forced`
encodes that real outcome as a `RunRecord`/`LaneRecord` and asserts the
record layer classifies it correctly: lane status `EVALUATED` (not
`NOT_RUN`, not silently absorbed into a blocked/no-candidate result), and
the cycle's `coverage_state` is `COMPLETE`. This is a test of the **record
layer's honesty**, not a re-run of the live evaluation itself — the
evaluation that produced DUOL's real numbers already happened, live,
against real broker/market data, and is not reproduced here.

## Item 2 — a real schema gap this patch surfaces (not fixed by this patch alone)

Building `REQUIRED_LANES_MODE_BC` against CLAUDE.md surfaced a genuine gap
in the *existing* trigger-prompt JSON schema used in `trades_log.md`: the
schema currently has one field, `options_stop_check`, covering the
protective stop-check for already-open §18/§19 positions (step 2b) — but
the request separately lists **"swing options"** and **"independent
LEAPS"** as required *candidate-sourcing* lanes (§18 item 11 / §19 item
8), which is a different question ("did we look for new options/LEAPS
candidates this cycle?" vs. "is an existing position's stop still
honored?"). The live trigger prompts already perform both as narrative
steps (3a/3b for sourcing, 2b for the stop-check), but the JSON summary
schema has never tracked sourcing coverage as its own field — so an
incomplete options/LEAPS *sourcing* pass has no structured field to show
up in, only prose. This module's `REQUIRED_LANES_MODE_BC` tracks
`options_sourcing_s18` and `leaps_sourcing_s19` as separate lanes from
`options_leaps_stop_check`, which is the schema-level fix; wiring the live
cycle to actually populate those two new fields is the integration step
below, not done by this patch.

## Tests performed and results

```
$ python3 -m unittest dev_scanner.test_dev_scanner -v
... (12 tests)
Ran 12 tests in 0.001s
OK
```

One bug was found and fixed during testing: an overly strict string-match
assertion in the DUOL replay test itself (not in `run_record.py`) that
incorrectly flagged the word "setup:null" appearing anywhere in the lane's
own detail text, even while *describing* that setup:null did not block
evaluation. Fixed to assert on the lane's actual `status` enum and on the
substantive claim ("did not block evaluation") instead of raw string
position — the kind of mistake this whole exercise exists to catch, found
in my own test, not shipped.

## Call-budget impact

**Zero.** Every test runs against hand-constructed in-memory data —
no network call, no MCP tool call, no Robinhood or tvremix request. This
patch cannot be exhausted by, and does not draw from, any existing daily
reserve.

## What still blocks reliable evaluation (honest, not glossed over)

1. **There is no separate "development copy" of the actual scanner.** The
   live evaluation logic (Stage-1/Stage-2 screening, the §13.G walk-through,
   the §22/options/LEAPS/Mode-C steps) lives entirely in the *stored prompt
   text* of the two live `Claude_Code_Remote` triggers
   (`trig_01RN6ZbtgxKpoDApzmGswWAs`, `trig_01KrBsTt9mssjU4hPGtM3cBe`) and in
   `CLAUDE.md` — there is no committed, executable application distinct
   from that prompt text that this patch could fork into a dev/prod split.
   This module is therefore a **new, additive layer** (a record schema +
   validator + selection function), not a modification of the existing
   evaluation code, because no such separately-editable code exists in this
   repository. This is the honest answer to "if the fault is outside the
   editable scanner code, identify the component" — the component is the
   live trigger prompt text itself, which this request correctly places
   off-limits.
2. **This validator is not yet wired into any live cycle.** It exists and
   passes its own tests, but nothing currently calls it during an actual
   trigger firing. Integrating it (e.g., having each cycle's JSON summary
   constructed as a `RunRecord` and validated before being written to
   `trades_log.md`) requires editing the live trigger prompt text — which
   this request explicitly defers to "separate review," so it is not done
   here.
3. **A later unattended-cycle report is still needed** (as the request's
   own closing section says) to show this actually changes real-cycle
   behavior, not just that the module's own unit tests pass against
   synthetic data.

## Proposed next integration step (not applied — for your decision)

Add a short, final step to both live trigger prompts: after step 15's
existing JSON summary is assembled, populate a `RunRecord` with that
cycle's real lane outcomes (including the two new sourcing-coverage
fields above) and compute `validate_run_record()` against it; log the
resulting `coverage_state`/`issues` as an explicit additional field
(e.g. `application_coverage_state`) alongside the existing
`coverage_state`/`platform` fields already in use — never replacing them.
This is a live-trigger-prompt edit and is **not performed by this
patch**; flagging it as the smallest next step, pending your approval.
