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
| ~~TEM~~ | **REMOVED 2026-11-13T16:48Z (Fresh Candle) — INVALIDATED, bullish thesis dead; fresh bearish check also fails.** Today TEM gapped down hard and continued falling: last completed 1h bar (t=1794583800) closed $69.56 (low $68.485), down from yesterday's ~$75.9 close — a confirmed breakdown well below the entire recent 75-77 consolidation range, moving sharply AWAY from the $79.41 reclaim level the queued bullish thesis needed (change -8.59% today, `MARating_1h: StrongSell`). The bullish reclaim thesis is now dead, not merely still-pending. Checked the mirror bearish breakout-continuation setup too (stop just above the broken ~$75.47 swing low, ATR-based target): R:R computed at **~0.50:1** on the genuine structural stop — fails item 4 outright, same "crashed stock, stop too far from entry relative to achievable target" pattern as HPE below. No qualifying trade either direction. Removed as invalidated. | — | — | — | — | — | — | — |
| ~~TEM-OLD~~ | **REMOVED 2026-11-19T16:03:39Z (Fresh Candle) — stale orphaned duplicate, cleaned up.** This row was never updated after 2026-11-12 while a separate, newer "TEM" row (added later, now itself removed/invalidated twice — see entries dated 2026-11-11T16:04Z and 2026-11-13T16:48Z above) superseded it. TEM's real current status is "invalidated" per those later entries, not "still a near-miss" per this stale row. Removed for hygiene; not re-evaluated fresh this cycle (budget was prioritized on the market-reversal re-check — see trades_log.md). | — | — | — | — | — | — |
| ~~IGV~~ | **REMOVED 2026-11-13T16:26Z (First Scan/Fresh Candle gap closure) — EXPIRED, time-based removal independent of price data.** Added 2026-11-04, 7-trading-session expiry window reached (today, 2026-11-13, is the 7th-plus trading session since; 25+ cycles checked without ever clearing the dual-leg structural absence). Removed per this file's own rule 5 — not invalidated, not cleared, simply timed out. If IGV develops a genuine computable setup on a future cycle it is re-added fresh, not restored from this entry. | — | — | — | — | — | — |
| ~~HPE~~ | **REMOVED 2026-11-17T16:03Z (Fresh Candle) — CLEARED the equity-thesis Bearish Mirror Gate in full, resolved to NO_TRADE, not re-queued (same category as the 2026-11-12 NBIS entry below).** Today's first completed hourly bar (15:00-16:00Z) closed $45.64 (open $46.6825, low $44.84) — a genuine bearish breakdown-continuation candle, volume 775,834 vs. a real §13.H baseline (Friday's final 3 hours) of 583,427 = 1.33x, confirming. Item 7 now clears. Equity-thesis R:R (entry $46.00, stop $46.83 just above the bar's high, target $42.25 via 1.5x ATR≈2.5) = **4.52:1** — excellent. But HPE has no inverse-ETF path and short selling is banned, so the only executable instrument is a §18 long put — and no cap-compliant strike clears the OPTION's own 1.5:1 floor on a realistic (first-order delta) basis: the $44p (Dec 18, delta -0.380, ask $4.00) gives estimated R:R **0.356:1** against the same $42.25 target — nowhere close. Resolved NO_TRADE: thesis correct, no instrument can express it at an acceptable R:R. | — | — | — | — | — | — |
| ~~DUOL~~ | **REMOVED 2026-11-17T16:03Z (Fresh Candle) — INVALIDATED.** Today's first completed hourly bar (15:00-16:00Z) printed a low of $158.67 — well below the $162.00 structural low flagged at the last cycle as the level a confirmed reclaim would need to hold above. Price moved through the level that would have been the stop before any reclaim trigger ever confirmed. The bullish pullback-to-support thesis is dead; one bad day of RS data is not enough evidence to open a fresh bearish thesis instead, so this is logged as invalidated/disqualified for now, not flipped to a new near-miss. | — | — | — | — | — | — |
| ~~DIS~~ | **REMOVED 2026-11-17T16:03Z (Fresh Candle) — INVALIDATED, failed breakout.** Today's first completed hourly bar (15:00-16:00Z): high $122.10 (briefly exceeded the $120.44 breakout level this thesis needed to hold above) but closed $119.47 — back BELOW $120.44, and below the day's own open, on a broad market selloff (SPY -1.1%+ today). This is a rejected breakout, not a confirmed continuation. Removed as invalidated. | — | — | — | — | — | — |
| ~~FIG~~ | **REMOVED 2026-11-17T17:03Z (Fresh Candle) — INVALIDATED.** Second completed hourly bar (16:00-17:00Z) closed $18.465, up from bar1's $18.20 close — a second consecutive hour moving AWAY from the $18.08 floor rather than confirming a breakdown, now +2.3% off bar1's close. Two hours without a break, the second one a real recovery, outweighs the original momentum confirmation (RSI/MACD readings that are themselves now stale). Removed as invalidated. | — | — | — | — | — | — |
| ~~NOW~~ | **REMOVED 2026-11-17T16:03Z (Fresh Candle) — CLEARED the equity-thesis Bearish Mirror Gate in full, resolved to NO_TRADE, not re-queued (same category as HPE above and the 2026-11-12 NBIS entry below).** Today's first completed hourly bar (15:00-16:00Z) closed $93.12 (open $95.70, low $92.254) — a strong bearish breakdown-continuation candle, volume 2,022,410 vs. a real §13.H baseline of 416,392 = **4.86x**, decisively confirming. Item 7 clears. Equity-thesis R:R (entry $93.415, stop $95.82 just above the bar's high, target $88.3 via 1.5x ATR≈3.4, post-crash structure per §13.F) = **2.13:1** — clears easily. No inverse-ETF path, short banned → only a §18 long put. The $86p (Dec 18, delta -0.372, ask $4.35) gives realistic-exit R:R **0.438:1** against the same target — fails decisively. Checked a §24 paper bear-put-spread too (long $86p/short $80p, net debit $2.91, width $6): even the MAX-PROFIT-AT-EXPIRATION basis is only **1.06:1** (`vertical_spread_risk_reward`), already short of §24's 1.5:1 floor before even computing the realistic-exit figure, which would be lower still — not logged as a §24 PAPER candidate since it fails before reaching that step. Resolved NO_TRADE: thesis correct, no instrument (single put or spread) clears at an acceptable R:R. | — | — | — | — | — | — |
| ~~ZS~~ | **REMOVED 2026-11-17T18:03Z (Fresh Candle) — INVALIDATED.** Third consecutive completed hourly bar (17:00-18:00Z) closed $184.43 (high $184.699, low $182.76) — a third straight hour holding/grinding higher off the original $180.47 breakdown low (bar1 $183.77 → bar2 $184.28 → bar3 $184.43), with the live quote now $184.77, the highest read yet. Three hours without any continuation lower, each one slightly higher than the last, is no longer "a stale trigger awaiting confirmation" — it is active evidence the breakdown itself failed to hold. Removed as invalidated rather than carried forward a third time. | — | — | — | — | — | — |
| ~~BE~~ | **REMOVED 2026-11-17T18:03Z (Fresh Candle) — INVALIDATED, same pattern as ZS.** Third consecutive completed hourly bar (17:00-18:00Z) closed $169.70 (high $171.91, low $166.91) — the highest close of the three bars (bar1 $168.09 → bar2 $168.055 → bar3 $169.70), with the live quote now $169.25. Three hours of holding/recovering off the $162.93 breakdown low, not continuing lower. Removed as invalidated. | — | — | — | — | — | — |
| ~~UBER~~ | **Removed 2026-11-16T18:06Z (Fresh Candle) — CLEARED into a real live trade.** Price pulled back from the breakout high ($70.62) toward the originally-broken level, bringing the entry close enough to a principled stop (just beyond the $69.685 pre-today high, at $69.60) that R:R recomputed to **~1.57:1**, clearing the 1.3:1 floor for the first time this ticker was queued. Bought 31 shares @ avg fill $70.1999, protective GTC stop_market placed and confirmed resting at $69.60. See `trades_log.md`'s 2026-11-16T18:03:39Z entry for the full real-fill Trade Card. | — | — | — | — | — | — | — |
| ~~HPE-OLD~~ | **REMOVED 2026-11-19T16:03:39Z (Fresh Candle) — stale orphaned duplicate, cleaned up.** Superseded by the separate, newer "HPE" row above, which already cleared the equity-thesis Bearish Mirror Gate in full and resolved to NO_TRADE (2026-11-17T16:03Z — no option strike cleared the economics floor). This row was never updated after 2026-11-12. Removed for hygiene. | — | — | — | — | — | — |
| ~~NBIS~~ | **REMOVED 2026-11-12T16:04Z (Fresh Candle) — CLEARED the equity-thesis Bearish Mirror Gate in full, but resolved to NO_TRADE, not queued further.** Today's opening-hour bar (t=1794493800) completed with a close of $126.38 (vs. the prior completed bar's $155.05) — a decisive, now-confirmed hourly breakdown below the prior 1h swing low ($153.48), on volume 2,087,103 vs. a real §13.H baseline of 380,040 = **5.49x** (clears item 3's Volume floor emphatically). Daily Trend/State (9<20 EMA, 145.21 vs 159.37) and catalyst (item 2, already verified) both hold. **Items 1-3, 5-7 all clear — this is not a near-miss on the equity thesis, it is a full clear.** Resolved to NO_TRADE anyway because Mode B has no instrument to express a cleared bearish equity thesis at the size this account can actually use: NBIS is not on the §22 allowlist, so the only path is a §18 long put, and **no put strike that fits the 12%-of-equity premium cap (~$676) also clears item 2's own ≥1.5:1 R:R-on-the-option's-economics floor** — tested the $110 strike (Dec 18 expiry, delta -0.234, ask $6.55, fits the cap) and the $115 strike (Dec 4 expiry, delta -0.260, ask $6.05, fits the cap); using a first-order delta-based estimate of option-value gain to the equity-thesis target ($113.30, prior swing low) and to the more aggressive §13.F ATR target ($105.46), the best estimated R:R was ~1.07:1 — short of 1.5:1 at every cap-compliant strike. This is a genuine instrument-fit failure, the same category as the AMD pending-eligibility resolution below (§19, 2026-11-04) — not a rejection of the thesis itself. **A real bear put spread was found and logged separately as a §24 PAPER — NOT EXECUTED candidate** (long $115p/short $105p, Dec 18, net debit $3.55, R:R 1.82:1 — clears §24's floor even though the single-leg put didn't clear §18's) — see trades_log.md, 2026-11-12T16:04:23Z entry. Not re-queued: the thesis is resolved (cleared), not pending. **Addendum, 2026-11-12 later same day (see CLAUDE.md §12 change log, "AMDG/NBIS repair"):** the 1.82:1 figure cited above for the §24 paper spread is the max-profit-**at-expiration** basis (`vertical_spread_risk_reward()`), not a realistic planned-exit figure — recomputed via the new `vertical_spread_realistic_exit_value()`, the spread's realistic early-exit R:R is only **~0.425:1** (equity-thesis target) to **~0.62:1** (aggressive ATR target), well short of the 1.5:1 floor on the basis that actually matters for a 2-15 session swing exit. The single-leg put conclusion above (NO_TRADE, ~1.07:1 best case) is unaffected and was already computed on a realistic-exit basis. This entry is left as originally written; this addendum does not retroactively change it. | — | — | — | — | — | — |
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
| ~~AMDG~~ | **REMOVED 2026-11-13T16:48Z (Fresh Candle) — INVALIDATED, structural reversal, not merely still-failing stop-distance.** Today's §22 mandatory screen (Stage A): `MARating_1D: "Sell"`, `MARating_1h: "StrongSell"`, change **-19.57%** — AMDG/AMD cratering hard today, the opposite direction from the bullish structure this ticker needs for a leveraged-long entry. The near-miss blocker had always been a tight-but-closing stop-distance ceiling on an otherwise-clearing bullish setup; today that setup itself no longer exists. Removed as invalidated, not carried forward as a technicality. No order ever placed against this candidate. | — | — | — | — | — | — | — |
| ~~AMDG-OLD~~ | §22 leveraged-long | **Reassessed 2026-11-12T16:04Z (Fresh Candle), full `tv_structure.py` on real Stage-B OHLCV — a GENUINE REVERSAL from every prior check: cleared items 1-3/5-7 in full, failed only on the stop-distance ceiling, and only because of how far price ran during the evaluation itself.** Real, dated, same-day catalyst confirmed (`get_news(AMD)`: "AMD Shares Jump on Stunning Upgrade Amid Nvidia Turmoil," GuruFocus, and a Barron's AI-trade-rotation piece, both published today) — item 2 clears cleanly for the first time this ticker has been queued. Daily: last completed bar (11/11) closed $94.87, `current_above_prior_swing_high: true` (broke above the prior $90.05 high) — Location confirmed. 1h: EMA9/20 = 93.59/87.69 (bullish alignment) — Trend/State confirmed. RSI14(1h) 62.7, improving — Momentum confirmed. Breakout-bar volume 5,362 vs. a real 3-bar baseline of 309 = **17.4x** — Volume confirmed emphatically. At the entry price used for the gate check ($97.61), stop (1h swing low $94.80) sat at 2.88% of entry — well inside the 8% ceiling — and R:R on the §13.F ATR target ($117.95) came to **7.24:1**, far above the 1.3:1 floor. **Resolved to NO_TRADE anyway**: by the time sizing/tradability were checked moments later, the live price had already run to $106.68 (the stock moved ~9% intraday during this cycle's own evaluation) — recomputing `validate_stop_distance()` at that price against the same real structural stop ($94.80) put the distance at **11.14% of entry, now exceeding the 8% ceiling**. Per §22 item 4's own text, this is a hard reject — never widen the debit/ceiling, never chase with a tighter artificial stop that isn't independently structurally justified. This is the first time this ticker's blocker has been a single item (and only because of intra-cycle price movement, not a structural flaw) rather than two independent, structural failures — logged as a genuine near-miss, not the same persistent double-failure as every prior check. **Addendum, 2026-11-12 later same day (see CLAUDE.md §12 change log, "AMDG/NBIS repair"):** diagnosed as a stale-anchor-price bug, not real-time price outrunning a careful check — the $97.61 figure was the last-completed-hourly-bar close (correct for the structure/confirmation checks), reused as "current price" for the stop-distance/R:R math even though a fresher live quote (~$106.5, from the §22 Stage-A batch pulled *before* the completed-bar OHLCV) was already in hand. Fixed via `dev_scanner.tv_structure.finalize_candidate()` (atomic fresh-price stop-distance/R:R/sizing, tested 85/85) and a matching update to the Fresh Candle trigger's prompt; not yet applied to the First Scan or Crypto 24/7 triggers (flagged as the remaining gap). This entry is left as originally written; this addendum does not retroactively change it. **Reassessed again 2026-11-12T17:04Z (Fresh Candle), first real use of the now-fixed `finalize_candidate()` pipeline on this ticker.** One further completed 1h bar exists (t=1794497400: open $96.50, high $106.98, low $96.50, close $106.52, volume 10,292 vs. a 3-bar baseline of 2,054 = 5.01x, confirming Volume again) — `swing_points()` on the full 60-bar set confirms the structural stop is unchanged at $94.80 (still the deeper, governing swing low) and the swing high extended to $106.98 (`current_above_prior_swing_high: true` holds). ATR14(1h) recomputed at $4.00; 1h EMA9/20 = 96.17/89.48 (bullish, Trend/State still confirmed); RSI14(1h) 79.0 (very extended, but §13.F's RSI-exhaustion veto was removed 2026-10-29 — not a block). Pulled one fresh quote ($104.3937, last trade) and called `finalize_candidate()` once, atomically: **still NO_TRADE, `stop_distance_exceeds_ceiling`** — distance $9.59 = **9.19% of entry**, vs. the 8% ceiling (ceiling $8.35) — improved from 11.14% (at the $106.68 price checked last cycle) as price has pulled back from its intrabar high, but still over. No order placed. This is now a real, atomic single-call result (not a two-pass sequence) and still lands on the identical conclusion: everything but the stop-distance ceiling clears, and the ceiling itself is closer to passing than last cycle but not there yet. **Reassessed again 2026-11-12T18:04Z (Fresh Candle).** One further completed 1h bar (t=1794501000: O107.21/H107.25/L103.53/C103.53, a pullback off the 108.8 intrabar high) — `swing_points()` unchanged: stop still $94.80, swing high now $108.8. ATR14 $4.08. Fresh quote $104.62 → `finalize_candidate()`: **still NO_TRADE, `stop_distance_exceeds_ceiling`** — 9.39% vs. 8% (essentially flat vs. last cycle's 9.19%, chopping in the same 9-11% band as price oscillates $103-108). No order placed. **Reassessed again 2026-11-12T19:04Z (Fresh Candle) — closest yet to clearing.** Next completed 1h bar (t=1794504600) closed $104.84 (a bounce off the $102.60 intrabar low). `swing_points()` unchanged, stop still $94.80. Fresh quote $103.275 → distance $8.475 = **8.21% of entry** vs. the 8% ceiling ($8.262) — still `stop_distance_exceeds_ceiling`, but now the closest of any check yet (was 11.14% → 9.19% → 9.39% → **8.21%** as price has pulled back from its $108.80 high toward the stop). No order placed; still correctly rejected per the hard ceiling. | Item 4 — stop-distance ceiling only (8.21% vs. 8% this cycle — closest yet; has ranged 8.21-11.14% across the last four checks), purely a function of where price sits right now; every other item cleared | 2026-11-12T19:04Z (Fresh Candle, live-authority), via `dev_scanner.tv_structure.finalize_candidate()`, last completed 1h bar t=1794504600; fresh quote $103.275 | 2026-11-05 | 13 |
| ~~TNA~~ | **REMOVED 2026-11-13T16:48Z (Fresh Candle) — INVALIDATED, structural reversal.** Today's §22 mandatory screen (Stage A): `MARating_1D: "StrongSell"`, `MARating_1h: "StrongSell"`, change **-2.18%** — small-caps falling broadly today (IWM also StrongSell, -0.70%), the opposite direction from the bullish structure TNA needs. The prior blocker (R:R 0.33:1, stop-distance 12.8%) was itself already a double structural failure, not a close near-miss; today's outright reversal removes any remaining ambiguity. Removed as invalidated. No order ever placed. | — | — | — | — | — | — | — |
| ~~TNA-OLD~~ | §22 leveraged-long | **Refreshed 2026-11-11T18:03Z (Fresh Candle, first live-authority cycle) — still NO_TRADE; item 4 (R:R) and the 8% stop-distance ceiling both still fail despite today's continued rally (+2.8%).** Daily last completed bar unchanged (t=1794321000, close 57.69 — today's forming daily bar at $59.34 correctly dropped). 1H last completed (t=1794414600, close 59.40). Real 5-day `swing_points()`: unchanged prior swing high 61.90 / prior swing low 51.775 (the 2026-11-05 crash levels). `risk_reward()` at the current price: **0.33:1**, still far short of 1.3:1. `validate_stop_distance()`: real stop distance now **12.8% of entry — still over the 8% ceiling**. No order placed — this is a real, live-authority NO_TRADE on the actual math. | Item 4 (R:R, 0.33:1) AND the §22 8% stop-distance ceiling (12.8% actual) both still fail | 2026-11-11T18:03Z (Fresh Candle, live-authority), via `tv_structure.py`, last completed daily bar t=1794321000 / 1h bar t=1794414600 | 2026-11-11 | 6 |
| ~~SQQQ~~ | **Removed 2026-11-16T16:03Z (Fresh Candle) — CLEARED into a real live trade.** The item-7 blocker logged at 15:04Z (First Scan) resolved the moment the first hourly bar of the session (14:30-15:30 UTC) actually completed: fresh OHLCV confirmed a completed-bar close at $44.72, above the $43.56 swing high, on 3.55x §13.H baseline volume. Underlying (QQQ) bearish thesis re-verified unchanged. Bought 18 shares @ avg fill $44.8071, protective GTC stop_market placed and confirmed resting at $43.90, R:R 1.664:1 at fill. See `trades_log.md`'s 2026-11-16T16:03:23Z entry for the full real-fill Trade Card. | — | — | — | — | — | — | — |
| ~~SOXS~~ | **Removed 2026-11-16T16:03Z (Fresh Candle) — CLEARED into a real live trade.** The item-7 blocker logged at 15:04Z (First Scan) resolved the moment the first hourly bar of the session (14:30-15:30 UTC) actually completed: fresh OHLCV confirmed a completed-bar close at $56.80, above the $55.36 swing high, on 5.79x §13.H baseline volume. Underlying (SOXX) bearish thesis re-verified unchanged. Bought 14 shares @ avg fill $57.7599, protective GTC stop_market placed and confirmed resting at $55.65, R:R 2.043:1 at fill. See `trades_log.md`'s 2026-11-16T16:03:23Z entry for the full real-fill Trade Card. | — | — | — | — | — | — | — |
| ~~SPXU~~ | **REMOVED 2026-11-19T20:03:17Z (Fresh Candle) — INVALIDATED, a different/additional structural item now fails, not merely still-failing R:R.** Structural stop unchanged at today's first-hour low $38.24. Fresh ask $41.68 → risk $3.44 = **8.25% of entry, now EXCEEDS the 8% stop-distance ceiling** (was 7.37% at 19:03:26Z) — a new, additional failure on top of the already-failing R:R, which also deteriorated further (fresh 3-bar ATR(1h) proxy $0.927 → 1.5x target $43.07, reward $1.39 → R:R ≈0.40:1, worse than 19:03:26Z's 0.57:1). Two independent items now fail simultaneously. Removed as invalidated rather than carried forward as a technicality, same principle as AMDG-OLD/TNA-OLD above. No order ever placed against this candidate. | — | — | — | — | — | — |
| **TZA** | §22 inverse (underlying IWM) | **Reassessed 2026-11-20T20:03:22Z (Fresh Candle, last cycle of today's window) — still weakening, item 2 unresolved, 5th consecutive cycle.** Fresh 5-completed-bar read (15:00-20:00Z): IWM moved 265.30→258.14 (-2.70%) vs. SPY 717.19→695.06 (-3.09%) over the identical session window — IWM still outperforming (smaller decline by 0.39pp), same relative-strength-not-weakness pattern persisting all day. Item 2 still fails. TZA's own chart still bullish (53.44→58.00 over the 5 bars) but moot while item 2 fails. Market-shock breaker independently active a 4th consecutive Mode B/C cycle (SPY -3.02%/QQQ -4.78% vs. yesterday's close). STILL A NEAR-MISS on item 2. Next scheduled Mode B/C new-entry cycle is Monday's First Scan — this entry will be reassessed fresh from scratch then, per standing rule; today's intraday evidence does not carry forward unverified. | Item 2 (relative-weakness driver on IWM, contradicted a 5th cycle running) | 2026-11-20T20:0x Z (Fresh Candle), fresh IWM/SPY 5-bar hourly series via Robinhood historicals (TradingView exhausted) | 2026-11-16 | 10 |
| **SQQQ** | §22 inverse (underlying QQQ) | **Reassessed 2026-11-20T20:03:22Z (Fresh Candle, last cycle of today's window) — ITEM 7 NOW CLEARS. A genuine, real, finalize_candidate()-verified qualifying setup, blocked from execution ONLY by the active market-shock circuit breaker this cycle — not a near-miss on its own merits anymore.** 5 completed hourly bars now exist (full history pulled back to 2026-11-13 via Robinhood historicals, TradingView still exhausted). QQQ continuing bearish (641.60→615.08 over the 5 bars, -4.78% vs. yesterday's close) — underlying leg clears decisively. SQQQ's own chart: bar5 closed $56.375 (completed-bar basis) / fresh quote ask $56.80, a genuine close-through break above the real `swing_points()`-confirmed prior swing high ($55.55, bar4's high) — `current_above_prior_swing_high: True`, confirmed via the real module on a 35-bar (6-session) history, not just today's 5 bars; today's bar5 high ($56.95) is also the highest print in the full 6-session window pulled (prior max was $49.59 on 11/19). Volume: bar5 7,968,496 vs. the real §13.H baseline (avg of bars 2-4: 6,320,711) = **1.261x — clears the ≥1.2x floor for the first time this ticker was queued.** Item 7 clears. Structural stop placed just below the broken level ($55.50); real ATR14(1h) = 1.824; target via §13.F ATR_TARGET (1.5x ATR) from the fresh entry = $59.54; R:R on the fresh quote ≈ **2.1:1**, clears the 1.3:1 equity-thesis floor comfortably; stop distance ≈2.3% of entry, well inside the §22 8% ceiling. **Every §22/§5B-Bearish-Mirror-Gate item now clears.** The ONLY reason no order was placed this cycle: the market-shock circuit breaker (SPY -3.02%/QQQ -4.78% vs. yesterday's close) is independently active and blocks every new entry this cycle, per its own explicit "skip new entries this cycle only" text — this is not a gate failure on SQQQ's part, it is a cross-mode breaker that would block any candidate regardless of quality. Kept queued (not cleared/removed) since no trade resulted; the next scheduled Mode B/C new-entry cycle (Monday's First Scan) will reassess this fresh from scratch per the standing rule — today's specific breakout/volume evidence will not carry forward unverified across the weekend gap. | Active market-shock breaker only (SPY -3.02%/QQQ -4.78%) — every §5B/§22 gate item itself clears | 2026-11-20T20:0x Z (Fresh Candle), QQQ/SQQQ 5-bar hourly series + fresh quote (ask $56.80) via Robinhood historicals/quotes (TradingView exhausted) | 2026-11-20 | 1 |
| **SOXS** | §22 inverse (underlying SOXX) | **Reassessed 2026-11-20T20:03:22Z (Fresh Candle, last cycle of today's window) — own-chart price DID break out fresh this bar, but volume confirmation still fails, worse than ever.** 5 completed hourly bars now exist. SOXX bounced intraday but remains net bearish for the session (134.48→125.19, -6.9% today) — underlying leg clears. SOXS's own chart: bar5 high $82.08 and close $80.76 both clear above bar3's prior high ($80.60) and bar4's range — a genuine fresh close-through this time, unlike bar4's failed attempt. But volume: bar5 3,847,390 vs. the §13.H baseline (avg of bars 2-4: 4,731,072) = **0.813x — still fails the ≥1.2x floor**, almost unchanged from bar4's 0.448x-then-partial-recovery pattern (now worse than bar3's original 0.616x read). Item 7 does not clear on volume despite the genuine price breakout. STILL A NEAR-MISS — item 7/volume confirmation only; this is now the cleanest single-item near-miss of the three (price structure itself is no longer in question). Next scheduled Mode B/C new-entry cycle is Monday's First Scan — reassessed fresh from scratch then. | Item 7 (hourly trigger — volume 0.813x baseline, below 1.2x floor; price itself DID break out cleanly this bar) | 2026-11-20T20:0x Z (Fresh Candle), SOXX/SOXS 5-bar hourly series via Robinhood historicals (TradingView exhausted) | 2026-11-20 | 1 |

**SPXU, TZA — same underlying-bearish-thesis-confirmed / inverse-ETF-bullish / item-7-unconfirmable
pattern as SQQQ/SOXS above, not separately deep-dived this cycle (Stage A only) to avoid spending
a second Stage-2 slot re-confirming an identical, already-established finding.** SPY (SPXU's
underlying) and IWM (TZA's underlying) both show Stage A StrongSell on both timeframes; SPXU and
TZA both show Stage A StrongBuy on both timeframes — directionally identical to SQQQ/SOXS. Not
added as separate near-miss rows; flagged here for the next cycle's screen to deep-dive properly
once a completed hourly bar exists.

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
| BTC | crypto (§21) | §21 item 2 — catalyst/RS remains the sole structural blocker (RS-vs-BTC inapplicable to BTC itself, no catalyst ever verified); item 7 (no fresh 1H breakout) also fails this cycle. | 4H Momentum still improving (MACD hist +1.446, unchanged 4h bar). 1H RSI 78.90 (still very elevated), no breakout (close $60,345.4 < prior 1h high $60,361.4). Catalyst/RS: still NOT VERIFIED. | 2026-11-21T22:37:49Z cycle, 4h last_t 1795276800 (unchanged) / 1h last_t 1795294800 (fresh) | 2026-11-21T13:37:36Z | 7 | 2026-12-01 |
| ETH | crypto (§21) | §21 item 3 — 4H setup fails both ways (Location: close $1,683.6 < prior high $1,715.84; Momentum: hist -0.118, still negative, unchanged 4h bar). Item 7 also fails. | RS vs BTC +1.98pp (still strongest of the 7 alts). 1H RSI 77.81, close $1,685.19 < prior 1h high $1,686.9 (very close) — no trigger. | 2026-11-21T22:37:49Z cycle, 4h last_t 1795276800 (unchanged) / 1h last_t 1795294800 (fresh) | 2026-11-21T14:38:01Z | 6 | 2026-12-01 |
| SOL | crypto (§21) | §21 item 2 (RS vs BTC flipped to **-0.34pp**, negative — first negative read this ticker has shown) AND item 3 (Location fails, close $70.28 < prior high $70.84; Momentum hist -0.079 still negative) AND item 7 (no 1H trigger). | 1H RSI 81.86 (highest of the cycle besides AVAX), close < prior 1h high $70.84 by a hair — no trigger. | 2026-11-21T22:37:49Z cycle, 4h last_t 1795276800 (unchanged) / 1h last_t 1795294800 (fresh) | 2026-11-21T12:38:01Z | 8 | 2026-12-01 |
| LINK | crypto (§21) | §21 item 2 (RS vs BTC **-1.18pp**, negative, worsened from last cycle's +0.31pp) AND item 3 (Location fails, close $8.59595 < prior high $8.64482; Momentum hist -0.00255 unchanged) AND item 7 (no 1H trigger). | 1H RSI 72.32, close < prior 1h high $8.64482 — no trigger. Volume 1h 2731 vs. baseline 14514 (0.19x) — now fails Volume too, a new concurrent failure. | 2026-11-21T22:37:49Z cycle, 4h last_t 1795276800 (unchanged) / 1h last_t 1795294800 (fresh) | 2026-11-21T12:38:01Z | 8 | 2026-12-01 |
| HBAR | crypto (§21) | §21 item 2 (RS vs BTC **-1.93pp**, negative, worsened) AND item 3 (Location fails, close $0.05169 < prior high $0.05205; Momentum hist +0.000263, flipped slightly positive but negligible) AND item 7 (no 1H trigger). | 1H RSI 71.90, close < prior 1h high $0.05205 — no trigger. Volume 1h roughly at baseline (1.01x). | 2026-11-21T22:37:49Z cycle, 4h last_t 1795276800 (unchanged) / 1h last_t 1795294800 (fresh) | 2026-11-21T14:38:01Z | 6 | 2026-12-01 |
| AVAX | crypto (§21) | §21 item 2 (RS vs BTC **-1.37pp**, negative, still worsened from the cycle it first flipped) AND item 3 (Location still fails, close $6.622 vs. prior high $6.641, essentially at the level again) AND item 7 (no 1H trigger). | 1H RSI 84.30 (highest of any pair this cycle), close < prior 1h high $6.641 — no trigger. MACD hist 4h -0.00117, still negative, unchanged bar. | 2026-11-21T22:37:49Z cycle, 4h last_t 1795276800 (unchanged) / 1h last_t 1795294800 (fresh) | 2026-11-21T10:37:53Z | 10 | 2026-12-01 |

**CLEARED 2026-11-21T20:37:37Z — XRP, removed from the queue — cleared into a real live trade (2nd trade this session).**
After 4 cycles of its 4H setup confirming but R:R failing at the live ask (widening each cycle,
1.31:1→1.13:1), XRP's 4h candle rolled over this cycle and the pair **broke out on both the 4h and
1h charts simultaneously** — close $0.93549 > prior 4h swing high $0.9329, and > prior 1h swing
high $0.93525. This genuinely cleared every §21 item 3 item: Location (4h+1h) and Momentum
(4h via MACD-improving, 1h via RSI 79.93/hist +0.00631) confirmed; RS vs BTC +1.68pp over 24h (a
real, computed, positive driver); R:R ≈1.69:1 at the live fill price, clean stop-distance
validation (risk comfortably clear of both the ATR ceiling and the tight-stop flag). **Flagged
explicitly, not hidden**: 1h RSI at 79.93 is extremely overbought — a real elevated reversal risk,
the same category of risk that preceded AAVE's stop-out two cycles ago — but §21 item 3 has no RSI
ceiling, only a floor (>45), so this is a disclosed judgment call, not a gate exception. Full
detail and the Trade Card are in `trades_log.md`'s 2026-11-21T20:37:37Z entry. No other pair
showed a fresh breakout on either timeframe this cycle.

**CLEARED 2026-11-21T16:38:10Z — AAVE, removed from the queue — cleared into a real live trade.**
After 7 consecutive cycles as a near-miss (first queued 2026-11-21T10:37:53Z), the 4h candle
finally rolled over this cycle and AAVE's 4h chart showed a genuine breakout (close $100.15 >
prior confirmed 4h swing high $99.94) with 4h MACD improving (hist -0.388, up from -0.788) —
Location and Momentum (via MACD-improving) both confirmed on 4H for the first time, alongside the
already-strong 1h Momentum (RSI 56.30, hist +0.973) and a real, computed RS-vs-BTC driver (+2.6pp
over 24h, the strongest of any allowlisted pair). Full detail and the Trade Card are in
`trades_log.md`'s 2026-11-21T16:38:10Z entry. **Key finding that shaped this decision**: using the
Kraken-derived close as "entry" initially showed BTC, ETH, SOL, XRP, and AAVE all confirming a 4H
setup simultaneously — but once the live Robinhood ask price was used (the actual realistic fill
price, given a real, material bid-ask spread on this account's market-maker routing), only AAVE's
R:R still cleared the 1.5:1 floor (≈2.07:1); ETH (≈1.40:1), SOL (≈1.22:1), and XRP (≈1.31:1) all
fell short at the real tradable price and were correctly rejected despite looking identical on
the Kraken chart. BTC was separately excluded on the catalyst/RS item — RS-vs-BTC is inapplicable
to BTC itself and no catalyst was verified. This distinction (chart-derived technical levels vs.
the live execution price) is the same category of lesson as the AMDG stale-anchor-price incident
logged in CLAUDE.md §12 — now applied prospectively rather than discovered after the fact.

**Added 2026-11-21T14:38:01Z — ALL 8 ALLOWLISTED PAIRS now confirm a 1h breakout simultaneously; a
sharp, broad-based rally hit the entire crypto allowlist within this single hourly cycle.** BTC
jumped from $58,768 to $60,462 (+2.9% in the hour), and every other pair moved comparably — ETH
+2.98% to $1699.19, SOL +3.09% to $70.66, XRP +3.33% to $0.930, LINK +2.82% to $8.67, AAVE +2.21%
to $101.44, HBAR +3.26% to $0.0518, AVAX +3.82% to $6.66. Every pair's 1h close is now above its
own prior confirmed swing high, and RSI sits between 51.68 (HBAR) and 67.22 (ETH) — well clear of
the 45 Momentum threshold — with every MACD histogram strongly positive. **6 of 8 pairs (BTC, ETH,
SOL, XRP, AAVE, AVAX) now confirm all three role-groups (Location/Momentum/Volume) on 1h** — LINK
and HBAR confirm Location+Momentum only, Volume still cooling off from an earlier spike (LINK) or
simply below baseline (HBAR), but that's still above the 1-role-group floor. **Despite this,
still no trade — the 4h chart has not caught up.** The 4h candle is the same one cached since the
last roll (`last_t` 1795248000, only ~1 hour old) and reflects conditions *before* this rally —
every 4h read still shows a bearish EMA stack and sub-35 RSI. §21 item 3 requires a confirming 4H
setup in addition to the 1H trigger; this rally happened entirely within one hourly candle and the
4H timeframe has not yet absorbed it. **AAVE remains the most mature candidate** — 5 consecutive
cycles as a near-miss, now with its strongest read yet (MACD hist +0.97) and all three role-groups
confirming for a 3rd straight cycle — still blocked purely on the missing 4H confirmation. Every
other previously-near-miss pair (ETH, which had invalidated 4 cycles ago; XRP; HBAR — previously
never queued) now also qualifies on the same 1h basis. This is the strongest, broadest signal
logged this session; worth flagging to the user as notable even with zero trades placed, given how
close the entire allowlist now sits to the only remaining gate item.

**Added 2026-11-21T13:37:36Z — BTC, new near-miss with a clean fresh breakout; SOL/LINK/AAVE/AVAX
all reassessed, all remain near-misses with an ambiguous (pullback, not reversal) Location
reading.** The 4h chart is unchanged this cycle (same cached candle, `last_t` 1795248000, only 1
hour elapsed since its roll). **BTC itself broke out on 1h for the first time this session** —
close $58,768.10 > prior confirmed swing high $58,579.40 — with all three role-groups (Location,
Momentum RSI 48.18/hist +230.6, Volume 1.63x baseline) confirming cleanly on the first read, same
strength AAVE and LINK showed at their own best moments. Meanwhile SOL, LINK, AAVE, and AVAX each
pulled back slightly under their own most-recently-set 1h swing high this cycle (a normal
consolidation within an ongoing move, the same pattern AVAX showed two cycles ago) — none reversed
through the level that originally qualified them, so all four stay in the queue as near-misses
rather than being invalidated. AAVE remains the most mature candidate (4 consecutive cycles).
ETH/XRP/HBAR showed no breakout this cycle either; none added. **Still no trade** — the 4H setup
remains the sole blocker for every candidate.

**Added 2026-11-21T12:38:01Z — SOL and LINK, two new near-misses; AAVE and AVAX reassessed and
both still near-misses, strengthening.** The 4h candle finally rolled over this cycle (`last_t`
1795248000, first new bar in 4 consecutive cycles) — 4h RSI improved materially for every pair
(e.g. AAVE 24.71→33.75, AVAX 19.13→26.30, SOL 24.24→29.34, LINK 27.65→31.49) but remains well
below the 45 Momentum threshold for all 8, and no pair shows a 4h breakout or bullish EMA
alignment — **still no confirmed 4H setup anywhere**, despite the real improvement. On 1h, the
breakout structure broadened materially this cycle: SOL and LINK both closed through their prior
confirmed 1h swing highs for the first time ($68.75 > $68.41; $8.44 > $8.44 respectively), each
with RSI>45-and-rising and a positive/improving MACD histogram — Location + Momentum confirmed on
1h for both, same basis as every other near-miss this session. LINK additionally cleared Volume
convincingly (79412 vs. baseline 12154, 6.53x — the strongest volume confirmation logged this
session). AAVE's breakout continued for a 3rd consecutive cycle (now $99.45 > $97.67) with all
three role-groups (Location/Momentum/Volume) confirming for a 2nd straight cycle — **the closest
candidate to qualifying this session**, pending only the 4H setup. AVAX's breakout resumed after
last cycle's ambiguous pause ($6.422 > $6.412), though its 1h RSI dipped just under 45 this cycle
(43.04, down from 47.04) — MACD improving still independently satisfies the Momentum role-group.
No other pair (BTC, ETH, XRP, HBAR) showed a 1h breakout this cycle — BTC/XRP/HBAR remain just
under their respective prior swing highs, ETH remains below the level its own breakout failed at
2 cycles ago. None of those four added. **Still no trade** — every candidate remains blocked on
the 4H setup, which is improving in the right direction (RSI climbing broadly) but has not yet
produced a qualifying confirmation on any of the 8 charts.

**Added 2026-11-21T10:37:53Z — AAVE and AVAX, both new near-misses, same shape as ETH's prior
near-miss (now invalidated, see the removal note below).** The 4h chart is unchanged from the
last two cycles (same cached candle, `last_t` 1795233600, still decisively bearish across all 8
pairs) — this is purely a 1h-timeframe development. Both names closed through their prior
confirmed 1h swing high this cycle (AAVE: $96.57 vs. $96.41; AVAX: $6.39 vs. $6.364), with RSI
climbing through/toward 45 over the last 2-3 cycles and MACD histogram turning clearly positive
in both cases — genuinely confirming two role-groups (Location + Momentum) on the 1h execution-
trigger timeframe, same basis ETH had. **Not a qualifying entry for either**: §21 item 3 requires
a confirming 4H setup, and the 4H chart has not rolled over to a new candle since this near-miss
precedent first appeared — it still shows the same decisively bearish structure (bearish EMA
stacks, RSI 19-25, no breakout) that has produced every rejection this session. Volume fails the
baseline check for both on 1h (below the 3-bar average) — not itself blocking, since Location/
Momentum already clear the role-group floor, but noted for completeness. No catalyst/RS verified
this cycle for either. Worth tracking closely as the 4h candle eventually rolls — not acted on
until the 4H setup itself independently confirms. No other pair showed a comparably concrete 1h
structural break this cycle (BTC/ETH/SOL/XRP/LINK/HBAR all showed Momentum strengthening but no
`current_above_prior_swing_high`); none of those added.

**Removed 2026-11-21T08:37:36Z — ETH, invalidated this cycle (a different, structural item now
fails — the 1h Location/breakout confirmation that was this near-miss's basis has reversed, not
merely "still missing the 4H setup").** Fresh data this cycle: the 4h candle finally rolled over
(`last_t` 1795233600, first new bar in 6 consecutive cycles vs. the prior stale 1795219200) — 4h
RSI improved to 29.97 (from 21.86) but remains well below the 45 Momentum threshold, EMA stack
still fully bearish (9<20<50: 1674.67<1736.70<1803.54), MACD still below signal (-57.72 vs.
-43.16, hist -14.56) and no breakout/retest on the 4h swing structure
(`current_above_prior_swing_high: false`) — still no genuine 4H setup, same as before. But on the
1h chart, the close ($1627.57) has fallen back **below** the prior swing high ($1654.99) that it
had broken through last cycle ($1637.61 close vs. $1625.72 level) —
`current_above_prior_swing_high` is now `false` where it was `true` last cycle. The breakout
failed to hold through the next completed candle: a false breakout, not a continuing one. Momentum
(1h) still technically passes (RSI 49.58, up from 48.55 and >45; MACD hist +3.81, up from +0.66,
still macd>signal) — but with Location's confirmation reversed, ETH now has only one role-group
(Momentum) instead of two, and no 4H setup regardless. Removed as invalidated rather than
re-logged as "still a near-miss" since the specific structural evidence that made it one no longer
holds. Re-add if a fresh breakout forms and holds through a subsequent candle. No other pair
showed a 4H setup or a confirmed 1h breakout this cycle either (full detail in `trades_log.md`'s
2026-11-21T08:37:36Z entry) — queue is empty.

**Added 2026-11-21T07:38:09Z — ETH, first near-miss since the 16:38:03Z invalidation (see the
removal note below).** After ~5 consecutive cycles of a decisively bearish, unchanged 4h candle
across all 8 allowlisted pairs, this cycle's fresh 1h data shows a broad stabilization/bounce:
every pair's 24h change improved materially (e.g. BTC -8.77%→-6.49%, AVAX -10.36%→-8.35%), and ETH
specifically closed through its prior confirmed 1h swing high with RSI crossing back above 45 and
MACD flipping positive — two real role-group confirmations (Location, Momentum) on the 1h
execution-trigger timeframe. **Not yet a qualifying entry**: §21 item 3 requires a genuine 4H
setup in addition to the 1H trigger, and the 4H chart has not rolled over to a new candle in 5
cycles — it still shows the same decisively bearish structure (RSI 21.86, bearish EMA stack,
below prior swing low) that produced every rejection this session. This is the first concrete
sign this session that the broader selloff may be stabilizing, worth tracking closely on the next
few cycles as the 4h candle eventually rolls — but not acted on until the 4H setup itself
independently confirms. No other pair showed a comparably concrete 1h structural break this
cycle (SOL/XRP/LINK/HBAR/AAVE/AVAX all showed RSI recovering toward/through 45 but no
`above_prior_swing_high`/`pullback_depth()` structural confirmation); none added.

**Removed 2026-11-20T16:38:03Z — ETH, AVAX, both invalidated this cycle (Momentum, their sole
remaining confirming role-group, has now flipped to failing — a different, harder item, not
merely still-failing Location) — on a genuine fresh 4h candle (the first new 4h bar in 4
consecutive cycles, last_t 1795176000 vs. the prior 1795161600).** A broad, severe market-wide
crash hit every one of the 8 allowlisted pairs this cycle simultaneously with a sharp equity
selloff (SPY -1.67%/QQQ -3.23% vs. yesterday's close) — all 8 pairs now show 24h changes of
-5.76% (BTC) to -7.72% (LINK), all bearish EMA9<EMA20<EMA50 stacks, all RSI in the 12.8-21.0 range,
all closed below their prior 4h swing low (`current_below_prior_swing_low: true`), 0 confirming
role-groups across the board:
- **ETH**: Momentum flipped decisively (MACD hist +0.32418→**-5.57777**, now macd<signal; RSI
  35.72→**20.98**, collapsing, not improving — both legs of the Momentum test now fail). Location
  still fails independently (no pullback structure, straight breakdown). Trend/State fails
  (EMA9 1742.28<EMA20 1772.13<EMA50 1850.25). Volume fails in the bullish sense (3.05x baseline,
  but this is abnormal selling pressure on a breakdown bar, not bullish confirmation). RS vs BTC
  -1.37pp (underperforming). Zero confirming role-groups remain.
- **AVAX**: Momentum flipped decisively (MACD hist +0.00869→**-0.01748**, now macd<signal; RSI
  31.61→**17.78**, collapsing). Location still fails independently. Trend/State fails
  (EMA9 6.8668<EMA20 7.0067<EMA50 7.3517). Volume fails in the bullish sense (4.78x baseline on a
  breakdown bar). RS vs BTC -1.31pp (underperforming). Zero confirming role-groups remain.

Neither qualifies as a fresh single-item near-miss on this cycle's data (both now fail every
role-group, not just Location/4H-setup), so neither is re-added. Re-add either if a future cycle's
fresh data independently re-establishes a confirming role-group.

**Removed 2026-11-20T12:38:17Z — SOL, XRP, HBAR, all invalidated this cycle on a genuine fresh 4h
candle (the first new 4h bar in 5 consecutive cycles, last_t 1795161600 vs. the prior 1795147200).**
A broad bearish 4h move hit every one of the 8 allowlisted pairs this cycle (BTC -3.34% over 24h,
alts ranging -3.25% to -7.09%) — each of these three lost the single confirming role-group that
had kept it queued:
- **SOL**: Momentum flipped (hist +0.0354→**-0.05647**, now macd<signal; RSI 31.84→29.86, falling).
  0 confirming role-groups remain (Trend/State, Location, Volume already failed).
- **XRP**: Momentum flipped (hist +0.000149→**-0.00072**, now macd<signal; RSI 42.76→40.54,
  falling). 0 confirming role-groups remain.
- **HBAR**: Volume collapsed (1.905x→**0.302x** baseline, well under the 1.2x floor). Momentum
  still fails independently (RSI 24.91, MACD hist -0.00014, macd<signal, unchanged). 0 confirming
  role-groups remain.

None of the three qualify as a fresh single-item near-miss on this same cycle's data (all three
now fail multiple items, not just Location/4H-setup), so none is re-added. Re-add any of them if a
future cycle's fresh data independently re-establishes a confirming role-group.

**Removed 2026-11-20T09:37:42Z — BTC, invalidated this cycle (data-convergence correction, not a new rule).**
Last cycle logged BTC's Momentum role-group as confirming via "MACD hist +6.60, macd>signal."
Recomputing this cycle on the SAME unchanged 4h candle (last_t 1795147200) found that figure was
an artifact of computing `macd()` over only the minimum 60-bar window (the 60-bar window actually
produces +6.5976 here, matching the prior log almost exactly) — MACD's 26+9 smoothing has not
fully converged at 60 bars. Recomputed on the full 736-bar cached history (and independently
confirmed stable from ~100 bars onward), the same candle's MACD histogram is **-18.15
(macd<signal)** — Momentum does NOT confirm. Checked every other queued/off-queue pair's
histogram sign at both 60-bar and 200+/full-bar windows: all stable (magnitude varies slightly,
sign does not) — only BTC flips. With Momentum now failing, BTC has 0 confirming role-groups
(Trend/State, Location, Volume already failed; RS vs BTC is not applicable to BTC itself) — same
as AAVE/LINK. Removed as invalidated, not a near-miss. **Methodology note for future cycles:**
when computing `macd()` from cached/merged bar history, prefer a window long enough to have
converged (verified stable by 100 bars here) over the bare minimum `count>=60` — this is a
computation best-practice, not a change to any gate, confirmation count, or threshold.

**Re-verified 2026-11-20T10:37:46Z — BTC correction holds.** Same unchanged 4h candle
(last_t 1795147200); full-736-bar MACD still hist -18.15 (macd<signal) vs. the 60-bar window's
+6.5976 — divergence unchanged, confirming this isn't a one-off computation glitch. BTC remains
correctly off-queue (0 confirming role-groups). AAVE and LINK also re-verified off-queue this
cycle (0 confirming role-groups each, unchanged).

**Removed 2026-11-20T08:37:58Z — LINK, invalidated this cycle.** Last cycle LINK had 2 confirming
role-groups (Momentum + Volume). This cycle's new 4h candle (close 8.87043, last_t 1795147200)
shows both have failed: Momentum (MACD hist -0.00348, macd<signal) and Volume (0.3475x baseline,
down from 1.466x) — 0 confirming role-groups remain, same as AAVE. Removed as invalidated, not a
near-miss; re-add if a future cycle shows a genuine confirming role-group again.

**Removed 2026-11-20T04:37:20Z — HBAR, invalidated this cycle.** Last cycle HBAR qualified on
Volume alone (2.058x baseline). This cycle's new 4h candle (close 0.05309, last_t 1795132800)
shows Volume has fallen to 0.7696x baseline (fails), Trend/State fails (EMA9 0.05495<EMA20
0.05612<EMA50 0.05884, bearish), Momentum fails (RSI 31.48<45, MACD hist -0.0001727, deteriorating
not improving), and relative strength vs BTC is negative on both 24h (-4.87% vs BTC -1.66%) and
96h (-9.96% vs BTC -4.55%) — HBAR is underperforming BTC, not outperforming, so no RS confirmation
either. Zero confirming role-groups remain — genuinely invalidated, not merely still-blocked-on-
Location. current_below_prior_swing_low is also True (a bearish breakdown, not a bullish setup,
so Location fails on its own separate terms too).

**Added 2026-11-20T04:37:20Z — AVAX, newly qualifies as a near-miss.** Previously 0 confirming
role-groups (correctly excluded from the queue). This cycle's new 4h candle (close 6.903) shows
MACD improving (hist +0.01587, macd -0.13537 > signal -0.15124) — Momentum now confirms. Trend/
State still fails (EMA9 7.0096<EMA20 7.1018<EMA50 7.4292, bearish); Volume fails (0.5729x
baseline); RS vs BTC mixed/marginal (96h -4.47% vs BTC -4.55%, essentially flat-to-slightly-better,
not a clean outperformance claim). Location fails (no breakout past prior swing high 7.164 or
below prior swing low 6.88, pullback_depth() None) — the sole binding failure, 1 confirming
role-group (Momentum) clears the 1-of-6 floor.

**Removed 2026-11-20T00:38Z — ETH, AAVE, AVAX, all three invalidated this cycle (a different,
harder item now fails for each — not merely still near-misses), computed via a full fresh pull
on `dev_scanner/tv_structure.py` against real TradingView 4h bars (TradingView's quota reset for
the new UTC date, 17 calls spent, no Kraken needed this cycle). Each had been clearing the
confirmation-count floor as of the 23:37:43Z cycle via exactly one or two role-groups; this cycle
every one of those confirming role-groups independently re-checked and failed, dropping each to
zero confirming role-groups (Location/4H-setup already failed for all three regardless, unchanged).**
- **ETH**: last cycle cleared via Momentum (MACD improving) + Volume (2.18x). This cycle: Momentum
  fails (RSI 43.98<45; MACD histogram declining for several bars, 6.75→5.81→4.48→2.81 — fading, not
  improving, despite staying barely positive) AND Volume fails (1.115x, down from 2.18x, below the
  1.2x floor). Trend/State also fails (EMA9 1782.6<EMA20 1799.52). Zero confirming role-groups.
- **AAVE**: last cycle cleared via Volume alone (3.24x). This cycle: Volume collapsed to 0.449x
  (well below the 1.2x floor — a sharp reversal, not noise). Momentum still fails (RSI 29.98<45,
  MACD histogram negative -0.472, declining). Trend/State fails (EMA9 107.49<EMA20 108.79). Zero
  confirming role-groups.
- **AVAX**: last cycle cleared via Momentum (MACD improving, RSI 39.47). This cycle: RSI rose to
  44.96 (improving, bar-over-bar from 40.07) but fell **0.04 short** of the required ">45" — flagged
  explicitly as an extremely marginal miss, not a clean rejection. MACD histogram is positive but
  declining (0.0344→0.0274→0.0264→0.0245 — fading, not improving), so the alternate "MACD improving"
  leg also fails. Volume fails (0.527x). Trend/State fails (EMA9 7.0414<EMA20 7.1285). Zero
  confirming role-groups under the current reading, despite being the closest of the three to
  re-qualifying — worth re-adding quickly if RSI clears 45 on fresh data, since the broader RSI
  trend (39.86→40.07→44.96) is a real, strengthening uptick, not noise.

All three removed from the queue; re-add fresh (not reinstated) if a future cycle's full gate
check finds a genuine confirming role-group again.

**Removed 2026-11-18T01:37Z — XRP, invalidated (structural reversal, not merely still a
near-miss).** Reassessed with fresh TradingView data (same session as last cycle's own Stage B
pull, no re-fetch needed for this pair before the quota re-exhausted mid-cycle). The 1H execution
trigger that qualified this candidate last cycle — close $0.9837 above the broken level $0.9793 —
has now reversed: the next completed 1H bar (t=1794960000) closed **$0.9781, back below** that
same $0.9793 level. The breakout failed to hold. 4H itself hasn't produced a fresh close yet
(still the same $0.9837 bar), but the 1H leg of the dual-timeframe test is what this candidate's
qualification actually depended on, and that leg has now flipped to the opposite side of the
level. Removed as invalidated per the same "different, harder item now fails" principle used for
AAVE's 2026-11-17 and 2026-11-12 removals — not carried forward as a lingering near-miss.

**Cleared 2026-11-18T00:37Z — SOL, cleared into a real live trade.** Both 4H (close $75.19 >
prior 4H swing high ~$73.54, bar t=1794945600) and 1H (close $75.19 > prior 1H swing high $74.20,
bar t=1794952800) breakouts confirmed on fresh TradingView/Binance data (TradingView's daily quota
reset for the new UTC day, used per protocol instead of the Kraken fallback). 1H volume 2.08x the
§13.H baseline; RS vs. BTC +1.91pp/6h — a real, checkable edge. Stop placed at $74.10 (just below
the broken level, §13.G item 4), passing both `validate_stop_distance` checks (within the 2-2.5x
ATR(1h) ceiling at $0.9569 ATR, and above the 0.5x-ATR tight-stop threshold). R:R at the actual
fill (19.9 SOL @ avg $75.8949) = 1.60:1, clearing the 1.5:1 floor. See the
2026-11-18T00:37:28Z trades_log.md entry and Trade Card for the full detail. Removed from the
queue — this is the referenced live trade, not carried forward as a near-miss.

**Removed 2026-11-17T17:38Z — AAVE, invalidated (not merely still a near-miss — a different,
harder item now fails).** First reassessment using the new Kraken-fallback data path (TradingView
confirmed quota-exhausted this cycle via a real Stage-A attempt — `TOOL_QUOTA_EXCEEDED`, recorded
in the shared `dev_scanner/data_budget.py` state; fell back to `dev_scanner/kraken_fallback.py`
for real OHLC on all 8 allowlist pairs, 1h/4h, 720 bars each — the first live use of today's
newly-enabled fallback). The prior recorded blocker (item 4, R:R ~1.17:1 on the ask-side spread)
is now moot: price has fallen through the structure that blocker was computed against. Fresh
4H close (t=1794916800) $112.50 with `pullback_low` $110.92 (the 4H pullback's own support) and
a confirmed 1H breakdown — last completed 1H bar (t=1794931200) closed $110.27, **below** the
prior confirmed 1H swing low ($110.63) — `current_below_prior_swing_low: true`. A fresh live
quote (`get_crypto_quotes`, updated 17:41:12Z) shows bid $108.304 / ask $110.3897 / mark
$109.3468 — **already trading below both the 4H pullback-low ($110.92) and the 1H swing low
($110.63)** that would have served as this setup's stop. The bullish pullback-hold thesis (which
cleared items 1/2/3/5/6 — RS vs. BTC still +4.23%/24h and +4.07pp/7d outperformance, several
confirmation role-groups on the 4H) no longer holds on the one item that matters most: item 7's
1H execution trigger has flipped from "awaiting" to a confirmed opposing breakdown, and live
price is now through the level a stop would sit at. Per the same principle used for AVAX's
2026-11-12 invalidation, this is a structural reversal, not a technicality — removed outright
rather than carried forward. No order was ever placed against this candidate this time around
(0 crypto positions held). If AAVE reclaims $110.63+ on a fresh completed 1H bar with a newly
confirmed higher low, it is re-added fresh on that new evidence, not restored from this entry.

**Removed 2026-11-16T04:38Z — AAVE, CLEARED into a real live trade (§21, Crypto 24/7 Scan, genuine
scheduled-trigger authority, `trigger_id trig_01UUXAtYHjn7nBgzkdvZU4Rv`).** A fresh completed 4H
bar (t=1794787200, 00:00-04:00 UTC, close $109.37) and enough subsequent 1H bars confirmed a new,
tighter structural swing low at $107.93 (1H bar t=1794790800) — verified as a genuine 5-bar
fractal (two confirmed higher-low bars on each side: t=1794783600/1794787200 before, t=1794794400/
1794798000 after). This let the position use a materially tighter stop than the prior $105.70
level that had been failing the ATR stop-distance ceiling as price ran away from it. Real
executable price via `preview_crypto_order`/`place_crypto_order`: filled at average $110.42726627.
Stop distance at the real fill: $2.52727 (2.288% of entry) — comfortably inside the 2-2.5x
ATR(1H) ceiling (~2.77-3.46% at this ATR reading) and above the 0.5x-ATR tight-stop-flag floor, so
no flag and a clean ceiling pass. R:R via the newly-authorized §21 ATR-target rule (1.5x ATR(4H),
no need to invoke the 2x alternative): target $115.2375, R:R = **1.903:1**, clearing the 1.5:1
floor without stretching. RS vs. BTC still holds (+7.45pp recomputed fresh: AAVE +8.72% vs. BTC
+1.27% from the same crash-trough basis used throughout this candidate's life). Confirmation
role-groups (Location, Volume, Momentum) all still independently confirm. See `trades_log.md`'s
2026-11-16T04:38Z entry for the full real-fill Trade Card. | 14.48831 AAVE @ avg fill
$110.42726627 ($1,599.90 notional); resting GTC stop_loss, qty 14.48831, stop $107.90, order id
`6afa891e-9403-4840-9ac6-4c2f9344e4c8`, confirmed resting.

*(Prior entry note: AAVE was removed as invalidated at 02:38Z when price ran to $110.63 and blew well past the ceiling; re-added at 03:38Z as price pulled back to the boundary; now cleared for real at 04:38Z once a fresh, tighter confirmed stop became available.)*

**Removed 2026-11-16T02:38Z — AAVE, invalidated (not merely still a near-miss).** A different, harder item now fails than the one previously recorded. Price has continued running up with no new confirmed structural stop forming: fresh `preview_crypto_order` resolved the real executable price at **$110.6349** (up from $109.16 the prior two cycles), while the only confirmed structural stop remains $105.70 (the same 5-bar-fractal swing low at $105.72 — no fresher fractal low has confirmed; the recent 1H retest low of $107.93 is only 1 bar past, not yet the required 2 bars, so it cannot be used). Stop distance at the new price: $4.9349 = **4.46% of entry — now exceeds the 2-2.5x ATR(1H) stop-distance ceiling outright** (ATRP|60 1.446% × entry ≈ $1.60 ATR; 2.5x ceiling ≈ $4.00 = 3.62% of entry). Per §21 item 4's own hard rule, a stop exceeding the ceiling is a reject, never resized or widened to fit, and never routed around with an unconfirmed tighter stop. This is a genuine structural deterioration from last cycle's marginal R:R-only shortfall (1.45:1 vs. 1.5:1, stop-distance ceiling still passing then) — now the stop-distance check itself fails, a different and more fundamental item. Removed as invalidated rather than carried forward as a technicality; items 1/2/3/5/6/7 (catalyst/RS, confirmations, timing, 4H+1H trigger) are unaffected and still would hold, but item 4 now fails on a harder basis than before. No order was ever placed against this candidate (0 crypto positions held throughout its 3 cycles in the queue). If AAVE pulls back toward a level where the existing $105.70 stop again fits inside the ATR ceiling, or a fresh, confirmed tighter swing low forms, it is re-added fresh on its own new evidence, not restored from this entry.

**Removed 2026-11-12T13:38:16Z — AVAX, invalidated (not merely still-near-miss).** Last cycle
(12:38:13Z) had already found two genuinely new structural failures — item 2 (relative strength,
now weakness not strength) and item 7 (a confirmed 1H bearish breakdown) — while holding off on
formal invalidation because no completed bar had yet closed below the $8.379 structural stop.
This cycle removes that last hesitation: the last completed 4H bar is still t=1794470400 (no new
4H close yet — next due 16:00:00Z), but the broader decline has continued and deepened on every
available measure. Stage A shows AVAX live at $8.3424 — already trading **below** the $8.379
stop level intraday (not yet a completed-bar close below it, but the forming 4H/1H candles both
show lows well through it: 4H forming bar low $8.243, 1H forming bar low $8.243 too). Relative
strength has not just failed to recover but worsened: AVAX down ~1.54% from the last completed
close ($8.473→$8.3424 live) vs. BTC down ~0.58% over the same window ($72,909→$72,484.52) —
continued, deepening underperformance, the opposite of the relative-strength driver item 2
requires. The last completed 1H bar (t=1794484800, close $8.412) confirms the 1H breakdown
identified last cycle was real and continuing, not a one-bar wobble. **Given two structurally
different items (RS and the 1H trigger) have now failed for two consecutive cycles, with price
having fallen through the stop level itself on an intracandle basis and continuing to deteriorate
on every completed read available, waiting for the technicality of one more completed-bar close
below $8.379 before calling this invalidated would be a distinction without a difference — the
original bullish thesis (confirmed 4H uptrend, bullish momentum, RS-driven entry) no longer holds
on any dimension.** Removed as invalidated rather than carried forward as a technically-still-
near-miss. No order was ever placed against this read (0 crypto positions held throughout). | 1H
confirmed bearish breakdown (12:38:13Z) + RS weakness, now deepening (13:38:16Z) + live price
trading through the $8.379 structural stop intraday | 2026-11-12T13:38:16Z (Crypto 24/7 Scan),
last completed 4H bar t=1794470400 (unchanged) / 1H bar t=1794484800, via
`dev_scanner/tv_structure.py` | — | 10 (final) | invalidated, not expired |

**Removed 2026-11-11T23:37:54Z — HBAR, invalidated (not cleared, not merely still-near-miss).**
Reassessed on fresh completed bars (4H t=1794412800 close 0.0664, unchanged from the prior cycle;
1H t=1794434400 close 0.06536, down from 0.06595). The 1H chart now shows a **confirmed completed-
bar breakdown**, not just a forming-candle wobble: `swing_points()` reports
`current_below_prior_swing_low: true` with prior_swing_low 0.06607 broken on a completed bar (the
prior cycle's version of this same signal was only visible in the still-forming bar). 1H RSI14 fell
to 49.00 (from 58.10) and 1H MACD flipped bearish (macd −0.00004 < signal −0.00002, a fresh
bearish cross — the prior cycle had this bullish). The 4H completed-bar reading is technically
unchanged (same last completed bar as last cycle — Momentum/Volume/Location still nominally clear
on that stale bar), but the practical effect of the price drop is that entry would now sit only
~0.00035 above the 4H swing-low stop (0.06501) — i.e. a fresh entry would be opened almost directly
on top of its own invalidation level, which is not a viable trade regardless of what the resulting
R:R arithmetic says. **Invalidated on a structural basis (confirmed 1H breakdown + entry-collapsed-
onto-stop), not merely "still short of a numeric floor" — removed from the queue rather than carried
forward.** No order placed, no new near-miss added in its place this cycle (the other 7 allowlisted
pairs all rejected cleanly on Stage A). | 1H confirmed breakdown below prior swing low (bearish
MACD cross, RSI14 1H 49.00 falling); entry has collapsed onto the only defensible 4H stop level |
2026-11-11T23:37:54Z (Crypto 24/7 Scan), last completed 4H bar t=1794412800 / 1H bar t=1794434400,
via `dev_scanner/tv_structure.py` | — | 4 (final) | invalidated, not expired |

**Removed 2026-11-11T21:37:41Z — AVAX, cleared into a real live trade (§21, Crypto 24/7 Scan,
genuine scheduled-trigger authority, `trigger_id trig_01UUXAtYHjn7nBgzkdvZU4Rv`).** Reassessed on
fresh Stage B completed-bar structure: items 1/2/3/6/7 all cleared decisively (catalyst strongly
reconfirmed via the real NYSE-infrastructure-partnership news cluster; Trend/State and Momentum
both independently confirming on 4H and 1H). Item 4 (R:R), the queue's standing blocker, computed
at **1.76:1** on the structurally-defensible 4H swing-low stop (8.376) against the last-completed-
1H-close entry basis (8.618) used for the gate decision — clearing the 1.5:1 floor for the first
time this candidate has been checked. **Material note on execution, logged honestly rather than
glossed over:** by the time broker verification and order placement actually ran a few minutes
later, AVAX's live price had drifted up to a real fill of 8.69710511 — at that higher real entry,
the same 4H swing-low stop (8.376) would have computed to only ~1.33:1, short of the floor. Rather
than treat the gate's own last-completed-bar R:R as still valid at execution, the stop actually
placed was re-derived from the real fill price using a different, equally real structural level —
the 1H prior swing low — landing at **8.50** (broker-rounded to the $0.01 increment from the
underlying 8.507 level) for a real-fill R:R of **~2.16:1**, comfortably past the floor and backed
by an independently-confirmed (not reverse-engineered) swing point. See `trades_log.md`'s
2026-11-11T21:37:41Z entry for the full real-fill Trade Card. | 129.9225 AVAX @ avg fill
8.69710511 ($1,129.95 notional); resting GTC stop_loss, qty 129.9225, stop $8.50, order id
`6af4e561-3267-4f8d-816d-ea503ab60d3a`, confirmed resting.

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

## Options/LEAPS Sourcing Queue (§18 item 11 / §19 item 8 — persistent rotation, added 2026-11-11)

**Repairs a real coverage gap, not a gate or risk change.** Options/LEAPS candidate sourcing
(§18 item 11, §19 item 8) was previously only ever evaluated out of whatever TradingView-call
budget was left after the Mode B equity rotation — on a tight-budget cycle it could silently
disappear entirely, with no distinct record that it had been skipped rather than evaluated and
cleared. Two fixes, both pure coverage/accounting, neither touching any CLAUDE.md gate, R:R
floor, confirmation count, position cap, or instrument permission:
1. `dev_scanner/tv_structure.py::allocate_scan_budget()` now reserves
   `options_leaps_calls_needed` calls for this sourcing step, ranked ahead of the Mode B equity
   rotation (priority 3 of 4, after the mandatory §22 ETF screen and Mode C) — it can only be
   reduced below what it asked for if the higher-priority reservations already exhausted the
   cycle's total budget, and that specific case is flagged via `options_leaps_deferred`, never
   silently zeroed.
2. `rotate_options_leaps_sourcing_queue()` gives this sourcing step the same persistent,
   least-recently-sourced-first rotation `watchlist.md`'s own equity rotation already uses — this
   table is that rotation's persisted state across cycles. A symbol with no row below (never
   sourced) ranks oldest and is always selected before any symbol with a real timestamp, however
   old.

**Four-way labeling, never conflated** (`validate_options_leaps_sourcing_label()`): every symbol
this step touches this cycle gets exactly one of **evaluated** (a real chain pull + full §18
item 2/§19 item 2 gate check ran), **rejected** (evaluated and failed a named gate item — cite
it), **data_blocked** (a tool failure prevented evaluation — never logged as a rejection), or
**deferred** (rotation/budget didn't reach this symbol this cycle — never logged as a rejection
or a tool failure). A tool failure and an unreached rotation slot are both honest non-results,
not disqualifications — same principle as the existing §5B Screening Coverage methodology's
tool-failure/rotation-skip distinction.

| Symbol | Last sourced (UTC) | Last label | Notes |
|---|---|---|---|
| AVAV | §18 put | evaluated — rejected | **Evaluated 2026-11-19T18:03:47Z.** Equity-side bearish thesis still clear (confirmed earlier cycles). Pulled the 2026-12-18 chain (29 DTE, within window); checked 3 strikes meeting the ~0.20+ delta floor: $85 (delta -0.249, ask $4.90), $90 (delta -0.318, ask $6.60), $95 (delta -0.392, ask $8.90) — all within the 12%-of-equity premium cap (~$598). Computed daily ATR14 from real bars (10/29-11/17) ≈$9.117; 1.5x-ATR downside target from live price ~$98.35 ≈$84.67 (price_move_in_favor ≈$13.68). Realistic pre-expiration exit value (delta-based estimate, `option_realistic_exit_value` method) for each strike: $85 → reward≈$3.41, R:R≈0.70:1; $90 → reward≈$4.35, R:R≈0.66:1; $95 → reward≈$5.36, R:R≈0.60:1. **All three fail the 1.5:1 floor on the option's own realistic economics** (the naive intrinsic-at-expiration figure would look better but is explicitly not the basis per §18 item 11/item 2). Rejected on R:R — not deferred, not data_blocked. |
| *(all other symbols — table seeded 2026-11-11; not yet sourced, rank oldest-first)* | — | — | — |

## Pending-eligibility (timing-restricted, not a gate near-miss — priority on eligibility, not a queued gate failure)

| Symbol | Instrument focus | Restriction | Restriction basis | Re-check method | Expected clear |
|---|---|---|---|---|---|
*(AMD row removed 2026-11-19T15:04:08Z First Scan — re-verified clear via `get_earnings_results(AMD)`: next report 2027-02-02, unverified/tentative, ~75 days out, no §4 conflict. §19 LEAPS re-evaluated fresh: daily RSI14 50.76 (neutral), EMA9 519.46 < EMA20 522.91 (still not a clean uptrend-or-basing per item 2's research gate — AMD remains in a wide post-crash recovery swing, $404 low on 11/5 to $544 today, not a settled structure), MACD improving (-7.69 vs sig -11.98). Still does not clear §19 item 2's research gate cleanly. Not re-queued — eligibility itself is resolved and stays resolved; this is an ordinary fresh re-evaluation, not a pending-eligibility matter anymore.)*

Once clear: AMD gets a **prioritized** full §18/§19 Stage-2 slot (via the existing §18 item
11/§19 item 8 options/LEAPS sourcing steps) at the next eligible cycle, ahead of ordinary rotation
— not an automatic pass. It must still independently clear the full §5B/Bearish Mirror Gate and
§18/§19's own sizing/DTE/delta/R:R requirements like any other candidate.

## Change log

- **2026-11-11 (later same day): added the Options/LEAPS Sourcing Queue table** (development/
  read-only, per the user's own scope — "reserve a bounded screening budget and persist
  unfinished candidates so options/LEAPS sourcing cannot silently disappear behind equity
  rotation... Log evaluated, rejected, data-blocked and deferred separately"). No gate, R:R
  floor, confirmation count, position cap, or instrument permission changed — same "tracks WHICH
  candidates get priority and WHEN, never a shortcut" principle as every other table in this
  file. See CLAUDE.md §12 change log and `dev_scanner/tv_structure.py`'s
  `allocate_scan_budget()`/`rotate_options_leaps_sourcing_queue()`/
  `validate_options_leaps_sourcing_label()` for the mechanism this table persists state for.
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
