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
| TEM | Equity (Mode B) | §5B item 7 — no hourly reclaim/breakout trigger; hourly bars faded 81.57→80.305 | Item 2 clears (+68.9% vs. SPY -1.95%); item 3 clears 2-of-5 (Trend/State + Momentum) | ~17:55:31Z (hourly bars through 17:00Z) | 2026-11-03 | 1 | 2026-11-12 |
| CVX | Equity (Mode B) | §5B item 7 — sideways consolidation (225.99→226.50→226.30→226.40), no reclaim/breakout trigger | Item 2 clears (+19.1% vs. SPY -1.95%); item 3 clears 1-of-5 (Trend/State) | ~17:55:31Z | 2026-11-03 | 1 | 2026-11-12 |
| ZS | Equity (Mode B) | §5B item 7 — hourly reversal/giveback from highs (228.85 high → 225.065), not a reclaim | Item 2 clears (+36.3% vs. SPY -1.95%); item 3 clears 1-of-5 (Trend/State) | ~18:55:15Z | 2026-11-03 | 1 | 2026-11-12 |
| SOFI | Equity (Mode B) | §5B item 2 — 5wk RS -11.5% vs. SPY -1.95% (underperformance, not a driver); no catalyst sourced | Item 3 clears 2-of-5 (Trend/State + Momentum) | ~18:55:15Z | 2026-11-03 | 1 | 2026-11-12 |
| DIS | Equity (Mode B), §13.G breakout-continuation | §13.G item 2 — confirmed 18:00Z bar volume 241,643 = 0.78x its own §13.H 3-prior-bar baseline (309,770); required ≥1.2x | Item 2 clears (+10.9% 5wk RS vs. SPY -1.95%); item 3 clears 2-of-5 (Trend/State + Momentum); hourly structure is a clean 4-bar grind higher | ~19:55:33Z (confirmed 18:00Z bar) | 2026-11-03 | 1 | 2026-11-12 |

## Current queue — §22 leveraged/inverse ETFs (tracked for history only — already re-screened every cycle via the existing mandatory §22 step; no separate reserved slot needed)

| Symbol | Instrument | Failed item (exact) | Other items' status | Data timestamp used | Added | Cycles checked |
|---|---|---|---|---|---|---|
| TNA | §22 leveraged-long | §5B item 2 (read on TNA's own chart) — RS vs. SPY only +0.09 to +0.74pp intraday, too thin; no catalyst | Item 3 clears, 9>20 (marginal), RSI 46-48/improving | ~19:55:33Z | 2026-11-03 | 1 (re-verified again 19:55:33Z unchanged from 17:55:31Z) |
| SQQQ | §22 inverse | Bearish Mirror Gate item 7 (read on QQQ) — no reclaim trigger, QQQ continuing to rise | Underlying bearish thesis holds (9<20 on QQQ, RSI 32.5, RS -5.8pp); ETF's own bullish-entry read (9>20, RSI 67.7, MACD improving) | ~19:55:33Z (narrative-confirmed; table row omitted that cycle — flagged as a logging gap, not a re-evaluation gap) | 2026-11-03 | 1 |
| SOXS | §22 inverse | Bearish Mirror Gate item 7 — forming, unconfirmed: underlying SOXX shows a real intraday breakdown (4 declining hourly closes); SOXS printing a fresh high but in the still-OPEN 19:00-20:00Z bar, not a closed candle. Last confirmed bar (18:00Z) closed $53.26, did not exceed the day's prior high ($53.95). | Underlying bearish thesis holds; ETF's own bullish-entry structure forming | ~19:55:33Z (confirmed 18:00Z bar; 19:00Z bar unconfirmed at log time) | 2026-11-03 | 1 — **priority re-check: did the 19:00-20:00Z bar close above $53.95 with §13.H volume confirmation?** |

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
| AMD | §18 options / §19 LEAPS — kept prioritized for options research per explicit user instruction | §4 earnings blackout (30 min before/after the report) | Reported Q3 2026 earnings 2026-11-03, timing "pm" (after today's regular-session close), actual EPS $2.09 vs. est. $1.89 (a beat), per `get_earnings_results`. Exact release minute not independently known beyond "pm." `rank_symbol_setups`' own conservative multi-day earnings-proximity skip (which flagged AMD "0 days to earnings" at today's first-scan) is a screener heuristic, NOT the actual §4 rule, and must not be used as the gating check here. | Every eligible cycle: re-verify via `get_earnings_results(AMD)` plus a direct computation of the actual §4 30-minute window against the real release timestamp — not the screener's skip heuristic. | By 2026-11-04's first-scan-of-day cycle at the latest — today's regular session already closed, and any reasonable "pm" release time tonight will be well past 30 minutes clear by tomorrow's open. |

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
