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
| ~~TEM~~ | **REMOVED 2026-11-11T16:04Z (Fresh Candle) — invalidated, item 2 (catalyst/RS) now contradicted, not merely a stop-distance near-miss anymore.** Last completed 1h bar (today's opening hour): close 81.01, high 85.03 — price has continued rallying for 3+ consecutive sessions off the original crash low (~67 → ~82+, +22%), with Stage-1 data now showing **StrongBuy aligned on both 1D and 1h** (RSI60 59.6, bullish MACD cross, +2.35% today, live price 82.54). The stop-distance ceiling item that had been the sole blocker actually **cleared this cycle** (distance to the 85.705 swing high narrowed to 5.80%, now under the 6% ceiling) — but that's now moot: per §5B Bearish Mirror Gate item 2's directional-catalyst rule, a persistent, strengthening bullish move that negates the only bearish catalyst/RS evidence on file fails item 2 on its own terms, not via an unwritten veto. Three consecutive up-sessions with no bearish reversal signal is exactly that negating evidence. Removed as invalidated rather than left queued on a technicality that no longer reflects the real thesis. | — | — | — | — | — | — |
| IGV | Equity (Mode B, ETF) | **Reassessed 2026-11-11T16:04Z (Fresh Candle), Stage-1 snapshot check only — no material change from the 15:05Z First Scan read.** Now $102.57 (+2.23% today), still inside the same ~98-104 chop range, getting closer to the 104.37 period high but no confirmed break yet. Same dual-leg blocker (no bullish breakout / no clean bearish setup) persists. | Structural absence (bullish leg, no breakout) / no clean bearish setup (bearish leg) both persist | 2026-11-11T16:04Z (Fresh Candle) | 2026-11-04 | 19 | 2026-11-13 |
| ~~PGY~~ | **REMOVED 2026-11-10T16:04Z — invalidated, not a near-miss anymore.** Last cycle (15:05Z) recorded a real 60m `pullback_long` setup (R:R 2.39:1) with only item 3 (confirmation role-groups, vs. a contradicting Stage-1 bearish-leaning score) genuinely unresolved. This cycle's fresh candle: **both legs now show `setup: null`** — 60m pullback deepened to 100.7% ("very_deep"/overextended, was a healthy/computable structure last cycle), 1D pullback 89.4% (also overextended, `setup: null`). Checked the §13.G breakout-continuation alternative on both legs too: `current_above_max_swing_high` is `false` on both (60m -19.87% vs. its own 21.09 max swing high; 1D -36.94% vs. 26.8) — no fresh-high condition either, so there is no computable entry under any currently-permitted method on either timeframe. This is a different, more fundamental item failing (no stop/target to compute from at all) than last cycle's item-3 ambiguity — a structural invalidation per this file's own rule 4, not a continuing near-miss. Removed rather than left queued; item 3's unresolved role-group question is now moot until a real setup reappears. | — | — | — | — |
| ~~GDX~~ | **REMOVED 2026-11-10T15:05Z — invalidated, not a single-item near-miss anymore.** Last cycle (2026-11-09T20:03Z) had item 4 (R:R) clearing at 1.42:1 with only item 7 (hourly trigger) blocking — a genuine single-item near-miss. This cycle: the 1D `pullback_short` setup's own computed R:R **dropped to 0.81:1** (entry 86.585, stop 107.44, target 69.74) — now failing item 4's 1.3:1 floor outright, a real deterioration in the underlying price geometry, not a stale read (fresh `analyze_structure_batch` data, 1D bar 2026-11-10). 60m still shows `setup: null` (100% overextended) — item 7 still fails too. With two items now failing simultaneously (R:R and the hourly trigger), this is no longer a true single-item near-miss per this file's own entry criteria — removed as invalidated rather than left queued. Items 2/3 (catalyst, confirmation role-groups) were never independently re-verified beyond the swing-structure read at any point this ticker was queued — flagged for the record, not a basis for removal here. | — | — | — | — |
| ~~PLTR~~ | **REMOVED 2026-11-04T17:17Z — invalidated, not a near-miss anymore.** Price moved 176.48→171.37 (-2.9%) between the 16:13Z and 17:17Z checks (63 min). The 1D pullback deepened from "deep" (75.3%) to "very_deep/overextended" (85.9%), and **the tool's own daily `setup` object is now `null`** — the computable pullback_long structure PLTR was queued on no longer exists at all, not merely still-unconfirmed. 60m also now shows price **below its own recent swing low** (`current_below_min_swing_low: true`, -7.6%). This is a real, structural invalidation (a different item now genuinely fails: there is no stop/target to compute from), not a stale repeat of the 16:13Z read — the user's own instruction not to reuse quotes beyond their freshness limits is exactly why this was re-pulled fresh rather than restated. | — | — | — | — |
| ~~ZETA~~ | **REMOVED 2026-11-04T17:23Z — resolved to REJECTED, not merely unverified.** Item 2 research
completed this cycle (`get_news`, `get_politician_trades`, dated daily-bar RS computation vs SPY
— all 2026-11-04) rather than deferred: **no real catalyst** — the only news since 10/26 is a
generic investor-conference notice (11/3), an earnings-estimate preview (11/2), and a headline
literally reporting the stock "trading down" (10/30); next earnings 11/9 (5 days out, a real
disclosed event-risk for a multi-session hold, though not itself a today-blocker under §4's
30-minute window). **RS is contradictory, not a clean pass**: the 5-week window (9/29→11/3, 25
sessions) shows ZETA +6.61% vs SPY -1.63% (+8.24pp) — but that figure is entirely carried by a
9/30 gap-up over a month ago. The most recent week (10/28→11/3, 4 sessions) shows ZETA **-7.4%
vs SPY -2.33% (-5.07pp)** — ZETA underperforming badly in the period immediately preceding today.
No politician-trade signal. **Item 2 fails on the evidence actually gathered — this is a real
rejection, not an "unverified, defer to next cycle" case.** See the full reasoning in
`trades_log.md`, 2026-11-04T17:23Z entry, including what the entry/invalidation/target/R:R would
have been had item 2 cleared (it didn't, so no trade follows from this). | — | — | — | — |

**SOFI — REMOVED 2026-11-04T19:04Z (Fresh Candle 20:04:04Z) — resolved to REJECTED (invalidated),
not a near-miss anymore.** Structure data alone (`analyze_structure_batch`) still showed
`pullback_short` setups on both TFs (60m R:R 2.48 "ok", 1D R:R 1.37), which on its face looked like
item 7 might now clear — worth checking items 2/3 before concluding that, which the queue's own
reassessment rule requires. `get_news` (6 most recent headlines, 2026-11-04) and `get_technicals_rating`
(requested 60m, **tool silently returned interval "1D" instead** — noted, not treated as a 60m
read) both show the opposite of a bearish thesis: Q3 earnings beat with analyst price-target raises
(UBS $21→$22 on 10/29, Truist $16→$17 on 11/3, both reiterating/raising, not cutting), a
"SoFi Stock Rises" headline (11/2), price +3.44% intraday today, RSI 60.8 and rising, MACD positive
and improving, moving-averages "Strong Buy," overall "Buy" recommendation. **No bearish catalyst,
headwind, or relative-weakness driver remains on file — item 2 fails outright on its own terms**
(§5B Bearish Mirror Gate item 2's explicit directional-catalyst rule: a bullish headline that
negates the only bearish evidence fails item 2, not an unwritten veto). This is a real structural
invalidation, not a stale repeat — the bearish `pullback_short` structure read is real but not
actionable without a bearish catalyst to pair it with. Removed from the queue as rejected, not
merely expired or still-pending.

**CVX, ZS, DIS — RESOLVED this cycle (2026-11-04T17:04Z), removed from the queue for real this
time.** A new completed hourly candle (`latest_bar_time` advanced from 1793806200 to 1793809800)
gave each of these a genuine fresh read rather than a repeat of stale data:
- **CVX**: now shows a real computable setup — 1D `pullback_long`, R:R **0.12:1**. The §13.G
  ambiguity from the prior two cycles is resolved: there IS a pullback leg to measure from, it's
  just a very poor one. **Rejected with evidence — item 4 (R:R 0.12:1, far below the 1.3:1 floor).**
- **DIS**: confirmed above its own prior max swing high on BOTH 1D (+3.06%) and 60m (+5.47%) — a
  genuine two-timeframe fresh-high condition, the cleanest §13.G candidate seen this session.
  Checked for real this time: `get_equity_historicals` (hourly, today) returns only 2 completed
  regular-session bars (15:00Z vol 1,007,951; 16:00Z vol 610,019) — insufficient for a full
  3-prior-bar §13.H baseline, so the reduced-sample rule applies (baseline = the 1 available prior
  bar). Volume on the bar being tested (16:00Z, 610,019) vs. that baseline (1,007,951) = **0.61x**
  — fails the ≥1.2x §13.G item 2 floor outright, even on the generously small sample. **Rejected
  with evidence — §13.G item 2 (volume 0.61x of a 1-bar-reduced baseline, explicitly noted as
  reduced).**
- **ZS**: still no pullback setup and no fresh-high/low condition on either TF (60m overextended
  pullback, `setup: null`, `current_above_max_swing_high: false`; 1D `ranging/neutral`, same).
  Having now checked both the pullback-based and fresh-high/breakout-continuation paths on two
  separate fresh candles without finding either, this is a genuine, now-confirmed structural
  absence rather than an unresolved pending state. **Rejected with evidence — no computable entry
  under any currently-permitted Mode B method (checked twice, two different candles).**

## Current queue — §22 leveraged/inverse ETFs (tracked for history only — already re-screened every cycle via the existing mandatory §22 step; no separate reserved slot needed)

**TNA, SPXL, SPXU, TZA — REMOVED 2026-11-06T20:03:47Z, invalidated (not merely reassessed).** The
persistent "insufficient bars (0)" tool failure these four carried for 3 consecutive cycles is
now resolved (corrected AMEX exchange prefixes persisted to `watchlist.md` this session) — this
cycle's `analyze_structure_batch` call succeeded for all 9 §22 names with no tool failure. The
real result: the setups that produced their queued R:R figures (TNA 1D 1.9:1, SPXL 1D 1.9:1,
SPXU 60m 2.38:1, TZA 60m 2.4:1, each from the stale 2026-11-04T19:04Z data) **no longer exist** —
all four now show `setup: null` on both 1D and 60m (deeper, overextended pullbacks, 80–150%
depth). This is a structural invalidation per this file's own rule (a different, more
fundamental item now fails), not a continuing near-miss — removed rather than left queued.

| Symbol | Instrument | Failed item (exact) | Other items' status | Data timestamp used | Added | Cycles checked |
|---|---|---|---|---|---|---|
| AMDG | §22 leveraged-long | **Reassessed 2026-11-11T16:04Z (Fresh Candle), Stage-1 snapshot check only.** Continuing to rally: now $94.61 (+14.1% today, up from $92.00 at 15:05Z), consensus still aligned bullish both timeframes. Item 2 (catalyst) still not independently verified this cycle — standing blocker unchanged from the 15:05Z read. Liquidity flag from last cycle unchanged. | Item 2 (catalyst) still the standing blocker | 2026-11-11T16:04Z (Fresh Candle) | 2026-11-05 | 6 |
| TNA | §22 leveraged-long | **Reassessed 2026-11-11T16:04Z (Fresh Candle), Stage-1 snapshot check only.** Continuing higher: now $59.10 (+2.44% today, up from $58.385 at 15:05Z) — moving further above the 56.055 pullback low used as the stop reference, which would widen the R:R if re-measured against the same 59.67 target, but not independently recomputed this cycle given budget; item 2 (catalyst) still unverified. | Item 4 (R:R) likely improved but not recomputed; item 2 (catalyst) unverified | 2026-11-11T16:04Z (Fresh Candle) | 2026-11-11 | 2 |

**TQQQ, SQQQ, SOXL, SOXS, SPXL, SPXU, TZA — checked 2026-11-11T15:05Z (First Scan of Day), not near-misses, no entry.** Full mandatory 9-name §22 screen this cycle (Stage-1 snapshot, TRADING_VIEW_2): **SQQQ, SOXS, SPXU, TZA (the 4 inverse names) all fail at the gate's first step** — each one's required underlying is itself clearly bullish today, not bearish, so the Bearish Mirror Gate's underlying-thesis leg fails outright regardless of the inverse ETF's own chart: QQQ (SQQQ's underlying) Buy-rated 1h, MACD bullish cross, +1.68% today; SOXX (SOXS's underlying) 1h RSI 68.0 and +4.24% today despite a stale "StrongSell" 1D label; SPY (SPXU's underlying) Buy-rated 1h, MACD bullish cross, +0.81%; IWM (TZA's underlying) StrongBuy both 1D and 1h, +0.44%. **TQQQ, SOXL, SPXL (the 3 other leveraged-long names) show mixed consensus** (1D StrongSell/Sell vs. 1h Buy) with no clean same-direction alignment — structural absence on their own chart, not queued. (AMDG and TNA — see the table above, both reassessed/added this cycle with real near-miss evidence.)

**TQQQ, SQQQ — checked 2026-11-05T16:04:53Z (Fresh Candle cycle), not near-misses, no entry.**
TQQQ: mixed consensus (1D bullish weak but no setup/inactive pullback; 60m bearish moderate, no
setup) — no bullish-aligned structure either TF, structural absence, not queued. SQQQ: underlying
QQQ's own consensus is itself mixed (1D bullish weak, 60m bearish moderate) — the required
underlying-bearish-thesis leg (§22 item 2) is not established, so SQQQ fails at the gate's first
step regardless of SQQQ's own chart (which is also mixed: 60m bullish no setup, 1D bearish no
setup) — structural absence, not queued. SOXL, SOXS, SPXL, SPXU, TNA, TZA this cycle: see the
table above (TNA/SPXL/SPXU/TZA already queued, reassessment blocked by tool failure this cycle;
SOXL/SOXS not queued, same tool-failure block applies to them too — both retried once, same
"insufficient bars (0)" result both times).

**SOXL, SOXS — checked 2026-11-04T19:04Z (Fresh Candle 20:04:04Z), not near-misses, no entry.** SOXL: no setup on either TF (1D bullish moderate but pullback overextended/`setup: null`; 60m bearish weak, `setup: null`) — structural absence, not queued. SOXS: no setup on either TF either (60m bullish moderate but inactive pullback/`setup: null`; 1D bearish moderate/`setup: null`) — structural absence, not queued. TQQQ, SQQQ, AMDG: **not evaluated — tool failure**, `analyze_structure_batch` returned "insufficient bars (0)" for all three this cycle.

**Removed 2026-11-04T16:08Z — SQQQ, SOXS, reassessed and invalidated: their underlying bearish thesis no longer holds.** Fresh `analyze_structure_batch` data: **QQQ's 1D read is now bullish** (weak, pullback overextended) — not bearish, so SQQQ's required "bearish thesis on the underlying" (Bearish Mirror Gate) fails outright, a reversal from the 19:55:33Z note ("underlying bearish thesis holds"). Same for SOXS: **SOXX's 1D read is now bullish** (moderate) — SOXS's underlying bearish thesis also no longer holds. Neither ETF's own chart shows a qualifying bullish entry either (SQQQ: 60m `pullback_long` setup is null; 1D is bearish, wrong direction. SOXS: 60m bullish but setup null; 1D bearish, wrong direction). Both removed as invalidated, not near-misses — re-add if the underlying flips bearish again on a future cycle.

## Current queue — Crypto (§21)

**tvremix recovered since this file's creation** — 8 consecutive successful crypto cycles logged
(2026-11-03T22:38Z through 2026-11-04T05:38Z, `tvremix_consecutive_failed_cycles: 0` throughout);
the "DATA_BLOCKED" note below is now stale history, left only for audit context.

| Symbol | Instrument | Failed item (exact) | Other items' status | Data timestamp used | Added | Cycles checked | Expires (10 days) |
|---|---|---|---|---|---|---|---|
| AVAX | Crypto (§21), spot long | **Item shifts this cycle — stop-distance (item 4) now CLEARS, but item 7 (1H trigger) is now the blocker, and the short-term structure just weakened rather than improved.** Using the last completed 4H bar (08:00-12:00 UTC, close 8.577) with a freshly computed ATR14(4H) = 0.2933 (3.42% of entry): distance to the confirmed swing low (8.068) = **5.93%, now inside both the 2×ATR (6.84%) and 2.5×ATR (8.55%) ceilings** — resolves last cycle's straddle in favor of clearing. **However, the last completed 1H bar (14:00-15:00 UTC) printed a fresh LOWER low (7-tier: close 8.535, low 8.477) — below both of the prior two bars' lows (8.491, 8.521) that had been read as a tentative higher-low stabilization** — that stabilization read is now invalidated on the 1H timeframe; no 1H reclaim/breakout trigger exists this cycle. Net: the gate's remaining blocker moved from item 4 to item 7, and the pattern direction worsened, not improved. | Items 1/2/3/6 unchanged/still clear; item 4 (stop-distance) now clears for the first time; item 7 (1H execution trigger) is the new sole blocker | 2026-11-11T15:37Z (Crypto 24/7 Scan), last completed 4H bar t=1794384000 / 1H bar t=1794405600 | 2026-11-11 | 8 | 2026-11-21 |

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
