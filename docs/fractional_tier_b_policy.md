# Fractional Tier-B Pilot Policy

Standalone reference copy. **CLAUDE.md §§15-16 are authoritative** — if this document and
CLAUDE.md ever diverge, CLAUDE.md governs. This is a scoped, tightly-capped exception carved out
of the existing Agentic Trading rules, not an additional or parallel allowance. It counts inside
the existing account caps, not on top of them. All Tier-A rules not explicitly modified here still
apply in full (see CLAUDE.md §§1-14).

Added 2026-08-13 at explicit user instruction.

## Terminology

- **Tier-A**: the existing whole-share process (CLAUDE.md §§1-14) — unchanged by this policy.
- **Tier-B**: this new fractional-share pilot lane.

## Section 15 — Fractional Tier-B Pilot Policy

1. **Instrument scope and pre-trade checks.** Fractional shares are allowed only for liquid,
   exchange-listed common stocks and non-leveraged ETFs, and only when `get_equity_tradability`
   confirms fractional support AND `review_equity_order` returns no warning or error immediately
   before entry. This is a scoped exception to the "no fractional-share limit orders" rule (§2),
   applying only to Tier-B pilots meeting every requirement below — Tier-A proposals still require
   an exact whole-share quantity, no exception.

2. **Allocation sizing.** Maximum pilot allocation per position is the **lower of**:
   - $35
   - 15% of Agentic Account equity
   - a Tier-B-specific per-position sub-cap of **20% of Agentic Account equity** (tighter than
     Tier-A's 80% per-position cap)
   - whatever headroom currently remains under the shared 90%-total-deployed ceiling (90% of
     equity minus everything already deployed across Tier-A and Tier-B combined, raised 2026-08-19
     from 80% — see CLAUDE.md §12) — a Tier-B pilot is sized within that shared ceiling, not in
     addition to it

   **While the FTA Regime Dashboard is UNKNOWN_DEGRADED, halve all four of those figures**
   ($17.50 / 7.5% / 10% / half of remaining headroom) — paired with the reward-to-risk change in
   item 5. Minimum order size: $5. Orders must specify an exact fractional share quantity, never a
   dollar-buy command.

3. **LUC eligibility.** A Tier-B pilot is eligible when LUC is **GREEN or WHITE**. LUC RED is
   always no-entry. This is a scoped exception to the standard GREEN-only requirement (§2(a)),
   available only to Tier-B and only subject to the stricter confirmation in item 4 when LUC is
   WHITE.

4. **LUC WHITE confirmation (3-of-5).** For LUC WHITE specifically, require at least 3 of these 5
   confirmations (not all 5):
   - price is above, reclaiming, or within 2% below the 50-day SMA
   - 9/20 EMA alignment is bullish or improving
   - price is at a visible support, retest, or 38.2%–61.8% Fibonacci area
   - RSI is above 45 and rising, or MACD is improving
   - volume is stable-to-positive with no abnormal selling pressure

   For LUC GREEN, this 3-of-5 check is not required — GREEN already reflects LUC's own buy-zone
   confirmation — but the full §13 technical scorecard still applies as it does for Tier-A.

5. **Catalyst and reward-to-risk.** Require a verified catalyst or sector tailwind (URL and date).
   Minimum reward-to-risk: **1.5:1**, but only when the FTA Regime Dashboard is returning a
   current, valid classification (not UNKNOWN_DEGRADED). **While UNKNOWN_DEGRADED, Tier-B uses a
   2:1 floor instead** — stronger than Tier-B's normal 1.5:1, though still looser than Tier-A's
   3:1-while-degraded floor — combined with the item 2 halved allocation cap while in that state.
   Do not require a perfect FTA A-grade score for a Tier-B pilot — LUC status plus the item 4
   confirmations (when WHITE) are sufficient.

   **UNKNOWN_DEGRADED rule (explicit).** When the FTA Regime Dashboard is unavailable, stale, or
   returns placeholders — classified UNKNOWN_DEGRADED — Tier-B fractional pilots may execute
   **only at half of the normal calculated allocation** (item 2) **and only with reward-to-risk of
   at least 2:1** (not the normal 1.5:1). All other Tier-B conditions (items 1, 3, 4, 6-9), the
   global position/deployment caps, daily/weekly trade limits, and circuit breakers remain
   unchanged while in this state.

6. **Timing.** Entries are allowed up to three trading sessions before earnings, but the Trade
   Card must flag the event risk explicitly. No entry within 30 minutes of CPI, FOMC, major
   employment data, or the first/last 15 minutes of the regular session — unchanged from §4.

7. **Position-count caps — inside, not in addition to, existing limits.** A Tier-B pilot counts as
   an ordinary new position against the existing account caps: maximum one new position per day
   and three per calendar week, Tier-A and Tier-B combined. There is no separate or additional
   Tier-B allowance beyond those shared limits.  Never average down. Add only after a position is
   profitable and original support remains valid.

8. **Exit discipline.** Use a documented technical invalidation — see Section 16 for the full
   exit/loss-control mechanics that govern every Tier-B pilot. If invalidation hits, reduce or
   exit only after re-checking tradability and reviewing the order. If the review fails, send an
   urgent alert and do not trade.

9. **Logging.** Log LUC color, the item-4 technical evidence (3-of-5, when WHITE), catalyst, exact
   fractional quantity, dollar allocation, current quote, stop/invalidation, and source timestamps
   in every Trade Card and in `trades_log.md`, tagged **TIER-B** so it's distinguishable from
   Tier-A entries in the daily/weekly count reconciliation.

## Section 16 — Locked Exit and Loss-Control Policy (Tier-B Fractional Pilots)

Applies to every Tier-B fractional pilot. All existing circuit breakers (§6) remain in force
unchanged and independently of this section.

1. **Exit plan required up front.** Every entry must have an exit plan before the order is
   placed. The Trade Card must record: entry price, initial stop/invalidation, maximum planned
   loss in dollars, first profit target, and a time-stop date.

2. **Initial stop sizing.** Set the technical invalidation at the nearest valid support break, but
   never let the planned loss exceed 6% of entry price or 1% of total Agentic Account equity,
   whichever is smaller. If no technically valid stop fits inside that risk budget, do not take
   the trade.

3. **Stop execution.** When last price trades at or below the documented invalidation,
   immediately call `get_equity_tradability` and `review_equity_order`, then submit an exit for
   the full remaining fractional position. Do not widen, remove, or lower the stop. If the exit
   cannot be verified or submitted, create an URGENT EXIT FAILURE alert and halt all new Tier-B
   entries (Tier-A is unaffected unless a §6 circuit breaker independently triggers).

4. **Gap rule.** If price opens below the stop, do not wait for a bounce — review and exit the
   full position at the earliest available eligible execution. Log actual slippage and enter
   HARD_OBSERVE_MODE for the remainder of that session.

5. **Breakeven rule.** After a position reaches +1R, move the stop to entry price or the nearest
   higher technical support, whichever is higher. Never move the stop lower afterward. **Applies
   unconditionally, same-day entry or not (2026-09-03) — see CLAUDE.md §16 item 5, authoritative.**

6. **Profit protection.** At +2R, sell 50% of the position and trail the remainder below the 9/20
   EMA, prior-day low, or nearest higher support. At +3R, sell an additional 25% and continue
   trailing the remaining 25%. **This doc predates the §17 day-trade-protection and 2026-09-03
   trailing/trim decoupling changes — CLAUDE.md §16 item 6 is authoritative on current mechanics
   (the trim waits for a same-day entry's post-close review; the stop itself trails continuously
   regardless).**

7. **Momentum failure.** Exit the full remaining position if price closes below the 20-EMA for
   two consecutive sessions and RSI/MACD are both deteriorating, unless the original stop would
   trigger sooner.

8. **Time stop.** If the position has not reached +0.5R within 10 trading sessions, issue a
   mandatory exit review. If price is below entry and momentum is not improving, exit the full
   position — do not keep capital trapped in a stagnant trade.

9. **No averaging down.** No exception for "oversold," social-media sentiment, or a lower price.
   An invalidated Tier-B trade is closed, documented, and not re-entered for 30 calendar days
   unless a fresh setup meeting the full Tier-A bar (not just Tier-B's lighter bar) forms.

10. **Rolling stop-out circuit breaker.** After any three stop-outs in a rolling 10-trading-day
    window (Tier-A and Tier-B combined), enter HARD_OBSERVE_MODE. No new entries of either tier
    until the next full regime review is complete.

11. **Exit record-keeping.** Record every exit with planned loss, actual loss, slippage, the rule
    that triggered the exit, and whether the exit submitted successfully, in `trades_log.md`.
    These records must be included in the weekly system review.

## Drafting note (resolved)

An earlier draft flagged that "the existing half-size restriction" under UNKNOWN_DEGRADED
referenced something not previously in CLAUDE.md. Confirmed 2026-08-13 in the explicit
UNKNOWN_DEGRADED rule above (Section 15, item 5): the halved allocation plus 2:1 reward-to-risk
floor is a newly-introduced rule as of this policy, not a pre-existing restriction that was
already in force.
