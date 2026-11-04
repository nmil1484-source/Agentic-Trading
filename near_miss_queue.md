# Near-Miss Queue — Persistent Unresolved-Candidate Tracker

**Added 2026-11-03, user-approved ("Authorize the near-miss queue repair only... Keep AMD
prioritized for options research once its existing earnings restrictions permit evaluation").**
This file persists candidates that failed exactly one specific, named gate item on their most
recent full evaluation (a genuine near-miss, not a structural reject) across cycles, so they are
automatically prioritized for reassessment on fresh completed data instead of being mentioned once
in `trades_log.md` and then silently dropped. That gap was real and specific: TEM and CVX were
both flagged "worth a fresh hourly-trigger check next cycle" in the 2026-11-03T17:55:31Z entry, and
neither was actually re-checked in either of the two Mode B/C cycles that followed (18:55:15Z,
19:55:33Z) — each of those cycles instead drew a fresh rotation batch and never returned to them.

**This file changes NO gate, threshold, risk limit, or permission.** It only tracks WHICH
candidates get reassessment priority and WHEN they age out of consideration. §13.G's volume
clause text, every R:R floor, every confirmation-count floor, every position/risk cap, and every
instrument permission are read fresh from CLAUDE.md on every reassessment, exactly as for a
brand-new candidate — this queue never grants a shortcut, waiver, or relaxed recheck. The §13.G
"or clear accumulation/distribution" alternative-evidence-route proposal discussed separately this
session is **not** part of this authorization and is not applied anywhere in this file.

## Mechanism (reference — operative step text lives in each trigger's own prompt)

1. **Entry criteria.** A candidate is added when a Stage-2 full-gate evaluation clears every
   required item except exactly one — a true near-miss. A structural absence (no catalyst at all,
   0-of-5 confirmations, no computable stop) is an ordinary reject, not a near-miss, and is not
   queued. Record: symbol, mode/instrument, the single failed item (cited exactly, with the
   measured value vs. threshold), every other item's pass evidence, the data/candle timestamp
   used, and the cycle timestamp added.
2. **Reassessment priority.** Every eligible screening cycle (Mode B/C entry-screening, first-scan,
   and crypto), reassess queued candidates before drawing that cycle's normal Stage-2 rotation
   batch — using the full current gate, every item re-verified fresh on the newest completed
   candle, never just re-checking the one item that previously failed (a previously-passing item
   can have changed too).
3. **Budget/coverage preservation.** Reassessment draws from the EXISTING Stage-2 cap (12/cycle for
   Mode B/C; the already-mandatory full-allowlist batch call for crypto and the already-mandatory
   full-9-name §22 screen) — it is never an addition to either. For the general equity/options
   queue specifically (the §22 leveraged/inverse-ETF entries below are already fully re-screened
   every cycle regardless via the existing mandatory §22 step, so they draw no separate slot):
   reserve **up to 5 of the 12 Mode B/C Stage-2 slots per cycle** for queue reassessment (fewer if
   the queue has fewer than 5; 0 reserved if empty), leaving at least 7 slots/cycle for the normal
   least-recently-evaluated-first rotation. *Calibration filled in by Claude — the user specified
   the principle ("preserve required coverage and the current budget"), not this exact split.
   Chosen so today's 5-item backlog can clear in one cycle while a majority (7/12) of rotation
   capacity is still preserved; this reservation shrinks automatically as the queue shrinks, and
   the resulting temporary reduction in new-name rotation throughput (12→7/cycle while the queue is
   at its current size) must be stated plainly in that cycle's log, not glossed over.* If more than
   5 items are queued, reassess the 5 longest-since-last-reassessed first (same least-recently-
   evaluated-first principle as ordinary rotation); the rest simply wait for the next eligible
   cycle — not penalized, not removed.
4. **Outcome handling, every reassessment:**
   - **Cleared** (now passes every gate item): remove from the queue, proceed exactly as an
     ordinary freshly-qualifying candidate — normal Trade Card, sizing, caps, existing autonomous
     authority. No fast-track into an order; the full normal entry process still applies in full.
   - **Still a near-miss** (same or a different single item fails): update the failed-item field,
     the data timestamp, and increment `cycles_checked`. Stays queued.
   - **Invalidated** (a *different, structural* item now fails — confirmations drop out, catalyst
     is contradicted or stale, or price has moved through the level that would have been the
     stop): remove immediately, log as invalidated with the new failing evidence. It is a reject
     now, not a near-miss.
   - **Ineligible** (removed from `watchlist.md`, or a tradability/halt check fails): remove
     immediately regardless of time in queue, log as ineligible.
5. **Expiration — explicit, time-based**, mirroring this document's own existing exit-side
   time-stop philosophy (§16 item 8's 7-trading-session time-stop; §21 item 5's 10-calendar-day
   crypto time-stop) applied here to a not-yet-entered candidate:
   - Mode B/C equities, §18/§19 options/LEAPS, §22 leveraged/inverse ETFs: **7 trading sessions**
     in the queue without clearing → remove, log as expired.
   - Crypto: **10 calendar days** without clearing → remove, log as expired.
   *Calibration filled in by Claude for consistency with the existing exit-side numbers — the user
   specified "remove when invalidated or expired under an explicit documented rule," not these
   exact figures; adjustable.*
6. **No gate/risk/permission change of any kind**, restated: nothing in this file raises, lowers,
   or bypasses any CLAUDE.md number or instrument permission. Every reassessment re-reads CLAUDE.md
   live.

## Current queue — Mode B/C equities / §13.G

Reassessed from the reserved Stage-2 slots (item 3 above). All five entries below were last
checked in the cycle shown and have NOT been reassessed since — this is the exact backlog this
repair exists to clear starting at the next eligible cycle.

| Symbol | Instrument | Failed item (exact) | Other items' status | Data timestamp used | Added | Cycles checked | Expires (7 sessions) |
|---|---|---|---|---|---|---|---|
| TEM | Equity (Mode B), Bearish Mirror Gate | §5B item 4 (mirror) — `pullback_short` now present on BOTH 1D (R:R 1.09:1) and 60m (R:R 1.27:1) per fresh `analyze_structure_batch`, but both fail the 1.3:1 floor | Item 7 (mirror) now actually clears — daily+hourly both show the bearish pullback_short structure, aligned; items 2/3 not independently re-verified this cycle (no fresh catalyst/RS pull) | 2026-11-04T15:28Z (latest_bar_time 1793802600) | 2026-11-03 | 2 | 2026-11-12 |
| SOFI | Equity (Mode B), Bearish Mirror Gate | §5B item 7 (mirror) — 1D shows `pullback_short` (R:R 1.34:1, now clears item 4) but 60m setup is null, no confirming hourly breakdown trigger | Item 4 (mirror) now clears on 1D; items 2/3 not independently re-verified this cycle (no fresh catalyst/RS pull) | 2026-11-04T15:28Z | 2026-11-03 | 2 | 2026-11-12 |
| PGY | Equity (Mode B) | §5B item 7 — 1D `pullback_long` R:R exactly 1.30:1 (clears item 4, marginally); 60m is `ranging/neutral` with no setup — no confirming hourly reclaim trigger | Item 4 clears (marginally); items 2/3 (catalyst/RS, confirmations) not independently checked this cycle | 2026-11-04T16:13Z | 2026-11-04 | 1 | 2026-11-13 |
| IGV | Equity (Mode B, ETF) | §5B item 7 — 1D `pullback_long` R:R 1.57:1 (clears item 4 comfortably); 60m shows an overextended pullback with no setup — no confirming hourly trigger | Item 4 clears; items 2/3 not independently checked this cycle | 2026-11-04T16:13Z | 2026-11-04 | 1 | 2026-11-13 |
| PLTR | Equity (Mode B) | §5B item 7 — 1D `pullback_long` R:R 2.15:1 (clears item 4 strongly); 60m shows an overextended pullback with no setup and price below its own recent swing low — no confirming hourly trigger | Item 4 clears strongly; items 2/3 not independently checked this cycle | 2026-11-04T16:13Z | 2026-11-04 | 1 | 2026-11-13 |

**Note on this cycle's reassessment (2026-11-04T16:13Z Entry Screening cycle):** TEM/SOFI above
were NOT re-reassessed this cycle — the most recent completed hourly candle is unchanged from the
First Scan cycle 45 minutes earlier (`latest_bar_time` identical), so a re-check would only
reproduce the same result already on file. The 5-slot reservation was used instead for CVX/ZS/DIS
(see the §13.G correction below) — wait, those are also unchanged this cycle for the same reason.
**Correction to this note**: no near-miss-queue reservation was actually drawn this cycle; all 12
Stage-2 slots went to fresh rotation names (AVA, UBER, TTD, SHOP, AMD, ETHA, IBIT, PGY, MU, TSM,
IGV, PLTR), which is where PGY/IGV/PLTR above were newly found. This is a deliberate, logged
deviation from "reassess up to 5 every cycle" specifically because the candle hadn't advanced —
re-check TEM/SOFI/CVX/ZS/DIS for real at the next cycle whose candle has actually moved forward.

**CORRECTION, same day 2026-11-04T15:xxZ entry superseded — CVX/ZS/DIS were NOT properly
invalidated; "removed" above was a mislabeling, caught on user review.** `analyze_structure_batch`
with `methods:["swing"]` only detects pullback-anchored setups (`pullback_long`/`pullback_short`)
— a `setup: null` from this tool means "no pullback-based setup," not "no permitted entry
structure of any kind." It says nothing about §13.G breakout-continuation eligibility (a fresh
high/low with no pullback to measure), which is a separate, independently permitted entry method
this tool does not check. Re-reading the same data pulled this cycle: **DIS's 60m read shows
`current_above_max_swing_high: true`** (118.61 vs. prior max 113.38, +4.6%) — a genuine fresh-high
condition, a real §13.G candidate, not a structural absence. **CVX's 1D read also shows
`current_above_max_swing_high: true`** (219.82 vs. 217.78, +0.94%, barely) — also §13.G-eligible
in principle, though marginal. Neither was actually checked against §13.G (mandatory volume
confirmation per §13.H, catalyst/RS) this cycle — that check was simply never run, not run and
failed. **Corrected status: both restored to the queue as "not evaluated — §13.G volume/catalyst
UNKNOWN this cycle," not invalidated.** Only **ZS** shows neither a pullback setup nor a fresh
high/low on either timeframe (60m overextended pullback, `setup: null`; 1D `ranging/neutral`,
`current_above_max_swing_high: false`) — closest to a genuine structural absence, but even this is
"no positive candidate found this cycle," not a disproof, so it is also restored as
not-evaluated rather than invalidated (invalidation requires actually disproving a previously-held
condition, e.g. price moving through the would-be stop — none of that was shown here).

| Symbol | Instrument | Status this cycle | What's UNKNOWN (not evaluated, not failing) | Data timestamp | Added | Cycles checked | Expires (7 sessions) |
|---|---|---|---|---|---|---|---|
| CVX | Equity (Mode B), §13.G candidate | Fresh high on 1D (+0.94% above prior swing high) — §13.G path not checked | Volume confirmation (§13.H), catalyst/RS | 2026-11-04T15:28Z | 2026-11-03 | 2 | 2026-11-12 |
| DIS | Equity (Mode B), §13.G candidate | Fresh high on 60m (+4.6% above prior swing high) — §13.G path not checked | Volume confirmation (§13.H), catalyst/RS | 2026-11-04T15:28Z | 2026-11-03 | 2 | 2026-11-12 |
| ZS | Equity (Mode B) | No pullback or fresh-high/low structure found this cycle on either TF | Catalyst/RS; whether a different entry method (e.g. range breakout) applies | 2026-11-04T15:28Z | 2026-11-03 | 2 | 2026-11-12 |

None of these three were confirmed qualifying or confirmed disqualified this cycle — all three
stay queued, pending a §13.G-aware re-check (CVX/DIS) or a fresh look at whether a non-pullback
entry structure exists at all (ZS), at the next eligible cycle.

## Current queue — §22 leveraged/inverse ETFs (tracked for history only — already re-screened every cycle via the existing mandatory §22 step; no separate reserved slot needed)

| Symbol | Instrument | Failed item (exact) | Other items' status | Data timestamp used | Added | Cycles checked |
|---|---|---|---|---|---|---|
| TNA | §22 leveraged-long | §5B item 7 (read on TNA's own chart) — 1D shows `pullback_long` R:R 2.23:1 (**item 4 now clears, strongly**), but 60m shows an *opposing* `pullback_short` read — no confirming bullish hourly trigger for the daily setup | Item 4 now clears cleanly on 1D; items 2/3 (catalyst/RS, confirmation role-groups) not independently re-verified this cycle | 2026-11-04T16:08Z | 2026-11-03 | 2 |

**Removed 2026-11-04T16:08Z — SQQQ, SOXS, reassessed and invalidated: their underlying bearish thesis no longer holds.** Fresh `analyze_structure_batch` data: **QQQ's 1D read is now bullish** (weak, pullback overextended) — not bearish, so SQQQ's required "bearish thesis on the underlying" (Bearish Mirror Gate) fails outright, a reversal from the 19:55:33Z note ("underlying bearish thesis holds"). Same for SOXS: **SOXX's 1D read is now bullish** (moderate) — SOXS's underlying bearish thesis also no longer holds. Neither ETF's own chart shows a qualifying bullish entry either (SQQQ: 60m `pullback_long` setup is null; 1D is bearish, wrong direction. SOXS: 60m bullish but setup null; 1D bearish, wrong direction). Both removed as invalidated, not near-misses — re-add if the underlying flips bearish again on a future cycle.

## Current queue — Crypto (§21)

**tvremix recovered since this file's creation** — 8 consecutive successful crypto cycles logged
(2026-11-03T22:38Z through 2026-11-04T05:38Z, `tvremix_consecutive_failed_cycles: 0` throughout);
the "DATA_BLOCKED" note below is now stale history, left only for audit context.

*Empty as of the 2026-11-04T07:38:39Z reassessment below.*

| Symbol | Instrument | Failed item (exact) | Other items' status | Data timestamp used | Added | Cycles checked | Expires (10 days) |
|---|---|---|---|---|---|---|---|

**Removed 2026-11-04T07:38:39Z — BTC, reassessed and invalidated on a methodology correction, not
a market change.** Queued last cycle (06:38:39Z) as a near-miss failing only item 2 (catalyst),
with items 3/4/7 noted as clearing via a `pullback_short` structural setup. On reassessment this
cycle it became clear that framing was wrong at a more basic level, independent of the catalyst
question: **§21 is spot-only, buy-to-open-longs-only — there is no shorting, margin, or inverse
instrument anywhere in the crypto lane (§21 item 2; unlike equities, crypto has no §22-style
inverse-ETF workaround for a bearish thesis).** A `pullback_short` structural read, however clean
its R:R or timeframe alignment, describes a trade direction this account can never actually place
— it was never an executable candidate, not a near-miss on one item. Standing correction, applied
from this cycle forward: **only a `pullback_long`/`breakout_long` (bullish) structural setup, on
both the 4H and 1H timeframe, is ever a candidate for a crypto trade here.** A bearish-aligned 4H/1H
read on an allowlisted pair means stand aside on that pair, not a queued near-miss. No order was
ever placed under the prior framing (this account held 0 crypto positions the entire time BTC was
queued) — this is a logging/reasoning correction only, not a trade-error correction. Flagged to the
user in chat as worth a possible drafting-clarification addition to CLAUDE.md §21 item 3.

---

Prior note (historical, now stale): no crypto candidate qualified as a true single-item near-miss
while the lane was DATA_BLOCKED (tvremix connector-wide outage) for 7+ consecutive hourly cycles as
of this file's creation (2026-11-03T21:38:26Z).

## Pending-eligibility (timing-restricted, not a gate near-miss — priority on eligibility, not a queued gate failure)

| Symbol | Instrument focus | Restriction | Restriction basis | Re-check method | Expected clear |
|---|---|---|---|---|---|
| AMD | §18 options / §19 LEAPS — RESOLVED 2026-11-04T16:08Z, see below | **CLEARED, issuer-verified** — AMD's own IR site (`ir.amd.com`) confirms Q3 2026 results released 2026-11-03, 4:15 PM EST (after close). **No Q4/FY2026 earnings date has been announced by AMD** — the IR calendar lists no scheduled date; TradingView's `next_earnings_date: 2026-12-31` is a placeholder/fiscal-year-end convention, NOT an issuer-confirmed date, and must not be relied on as a real blackout trigger. Today's §4 window is clear either way (next report, whenever it actually lands, is realistically ~3 months out based on AMD's own quarterly cadence: May/Aug/Nov reports this year). | — (resolved) | `ir.amd.com` IR Calendar + `get_earnings_calendar` cross-check | **Both gates evaluated read-only 2026-11-04T16:08Z — see trades_log.md.** §18 (21-75 DTE call): FAILS §5B item 7 — 1D shows a bullish `pullback_long` (R:R 2.44:1, clears), but 60m is bearish with no setup — no confirming hourly trigger, direction mismatch. §19 (LEAPS, 2027-09-17 ≈10.4mo DTE): item 2's research gate is ambiguous (weekly read is `ranging/neutral`, not a clean uptrend-or-basing) but has a real multi-quarter catalyst (Anthropic 2GW Instinct deal, Microsoft deployment, World Labs/Taalas acquisitions, all confirmed via web search) — **moot regardless: the cheapest ~0.20-delta strike (840C) costs $25.50/contract × 100 = $2,550, vs. the 6%-of-equity premium cap (~$389 at current $6,483.65 equity) — fails affordability by ~6.5x, not marginally.** No qualifying AMD options/LEAPS trade right now; not a data gap, a real gate/affordability result. Remove from Pending-eligibility (resolved, not a trade). |

Once clear: AMD gets a **prioritized** full §18/§19 Stage-2 slot (via the existing §18 item
11/§19 item 8 options/LEAPS sourcing steps) at the next eligible cycle, ahead of ordinary rotation
— not an automatic pass. It must still independently clear the full §5B/Bearish Mirror Gate and
§18/§19's own sizing/DTE/delta/R:R requirements like any other candidate.

## Change log

- **2026-11-03: File created, user-approved** ("Authorize the near-miss queue repair only...
  Persist unresolved candidates with their failed/pending gate and data timestamp. Automatically
  prioritize their reassessment on fresh completed data in the existing eligible cycles, while
  preserving required coverage and the current budget. Recheck the full current gate before any
  entry. Remove candidates when invalidated or expired under an explicit documented rule. Do not
  lower volume thresholds, alter §13.G, or change risk limits or permissions... Keep AMD
  prioritized for options research once its existing earnings restrictions permit evaluation.").
  Seeded entirely from `trades_log.md`'s own logged evidence (TEM/CVX from 17:55:31Z; ZS/SOFI from
  18:55:15Z; DIS/TNA/SQQQ/SOXS from 19:55:33Z) — no entry invented without a specific,
  already-logged item-level failure to cite; AMD's earnings timing verified live via
  `get_earnings_results` at file-creation time, not estimated. All three screening triggers
  (first-scan, entry-screening, crypto) updated in the same pass to read, reassess, and update this
  file every eligible cycle, within existing Stage-2/allowlist budgets.
