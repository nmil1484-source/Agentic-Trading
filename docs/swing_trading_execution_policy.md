# Swing-Trading Execution Policy (Mode B)

Standalone reference copy. **CLAUDE.md §17 (day-trade/settlement) and the relevant parts of §5B,
§7, and §16 are authoritative** — if this document and CLAUDE.md ever diverge, CLAUDE.md governs.
Added 2026-08-13 at explicit user instruction, concurrent with removing Mode B's 1/day, 3/week
trade-count quota (CLAUDE.md §3/§12), and extended the same day with a risk-based capacity system
and two direct edits to §16.

## Context: why this exists

Mode B (SWING_TRADING) is a swing-trading system, not a day-trading system. Its intended holding
period is 1 to 15 trading sessions (CLAUDE.md §5B). As of 2026-08-13, Mode B is no longer subject
to a fixed daily/weekly trade-count quota — it may scan every eligible cycle and take every valid
setup that fits within the remaining risk-capacity limits (§3 dollar caps plus the position-count
and correlation caps below).

Removing the count quota makes it structurally possible for Mode B to behave like a day-trading
system if nothing else stops it. This document is that stop, plus the capacity system that
replaced the quota as the actual bound on how much Mode B can be doing at once.

## Section 1 — Mode B mandate

- Mode B is a swing-trading system, not a day-trading system. Intended holding period: 1 to 15
  trading sessions.
- It may scan every eligible cycle and take every valid setup that fits risk capacity; it is not
  subject to a fixed daily or weekly trade quota (CLAUDE.md §3, changed 2026-08-13).
- Candidate universe: the TradingView watchlist (`watchlist.md`), liquid market leaders,
  sector-relative-strength leaders, and verified catalyst-driven names.
- LUC, the FTA Research Hub, and the FTA Trade Tracker are context sources only in Mode B and must
  never function as a required eligibility gate (unchanged from the 2026-08-13 strategy-mode
  refactor, CLAUDE.md §2/§5B).

## Section 2 — Day-trade and settlement protection

1. **Settled-funds check.** Before every entry and exit, query Robinhood account capabilities and
   settled buying power. Use only settled cash for new purchases. Never use unsettled sale
   proceeds, margin, or borrowed funds.

2. **No same-day close by design.** Do not intentionally close a newly opened position on the same
   trading day. Every ordinary swing entry must be designed to be held overnight.

3. **Same-day exit exceptions — narrow, and logged.** The only same-day exit exceptions are:
   - a hard stop/invalidation being hit,
   - major adverse news,
   - a broker risk event, or
   - a market-wide risk circuit breaker.

   Record each exception as **SAME_DAY_PROTECTIVE_EXIT** in `trades_log.md`, and verify account
   status before the next order.

4. **No same-day loss re-entry.** Never re-enter the same ticker on the same trading day after a
   loss exit.

5. **Broker restriction check.** Do not open a new position if the broker reports a day-trading,
   good-faith-violation, free-riding, settled-cash, or other trading restriction on the account.

## Section 3 — Swing-entry rules (see CLAUDE.md §5B for the authoritative gate)

A Mode B swing entry requires, per §5B:

1. A liquid exchange-listed common stock or non-leveraged ETF that Robinhood MCP confirms is
   tradable.
2. **A daily-chart setup plus an hourly-chart execution trigger** — the daily setup (item 4 below)
   says a name is worth watching; the hourly trigger is the specific candle/level that times the
   actual entry.
3. A verified catalyst, sector tailwind, or relative-strength driver.
4. At least **2 of 6** technical confirmations (lowered 2026-08-14 from 3-of-6, see CLAUDE.md §12):
   9/20 EMA bullish alignment/reclaim; price above/reclaiming the 50-day SMA; breakout/retest/
   range-contraction/Fib-pullback location; relative strength vs. benchmark/sector; volume ≥1.2x
   normal or no abnormal selling; RSI >45 and improving or MACD improving.
5. A documented technical invalidation and reward-to-risk of at least **1.5:1, flat, regardless of
   regime dashboard state** (flattened 2026-08-14, see CLAUDE.md §12 — reduced position sizing
   while UNKNOWN_DEGRADED still applies, only the reward-to-risk distinction was removed).
6. No opening order in the first 15 minutes after open or the final 15 minutes before close.

## Section 4 — Risk-based capacity and sizing

Replaces the removed daily/weekly trade quota. A qualifying position may only be entered if all
existing hard limits (CLAUDE.md §3 dollar caps) plus these are satisfied:

1. Total deployed capital remains at or below 80% of Agentic Account equity after the order.
2. **No more than four Mode B positions simultaneously open.**
3. **No more than two open positions share one sector, industry, or catalyst theme.**
4. The existing per-position/fractional-pilot cap remains in force (§3/§15).
5. **Maximum planned loss per new trade is the lower of 1% of current Agentic Account equity or
   the loss implied by the defined technical stop.** Calculate share/fractional-share quantity
   from the entry-to-stop distance; round down within the existing allocation cap.
6. Never average down. A later add is allowed only after the original position is profitable, the
   setup remains valid, and all capacity tests above remain clear.
7. **Only one new entry per scheduled scan cycle** — a pacing limit, not a revival of the daily/
   weekly count quota.

## Section 5 — Exit management (see CLAUDE.md §16 for the authoritative rules)

1. Every entry carries an entry price, technical stop, risk in dollars, first target, second
   target, and expected holding window.
2. A hard-stop breach triggers a protective exit as soon as tradability/order review completes.
   Never widen, remove, or lower a stop.
3. At +1R, move the stop to breakeven or the nearest higher technical support, whichever is
   higher.
4. **At +2R, sell 50% only if the position has been held through at least one regular-session
   close** (2026-08-13 addition — day-trade protection); trail the remainder using the 9/20 EMA,
   prior-day low, or nearest support.
5. At +3R, sell another 25% and trail the remaining 25%.
6. **Time stop: 7 trading sessions** (shortened 2026-08-13 from 10). If the trade hasn't reached
   +0.5R by then and momentum isn't improving, exit at the next eligible execution.
7. If price closes below the 20-EMA for two consecutive sessions with weakening RSI/MACD, exit
   unless the stop triggers first.
8. Existing circuit breakers unchanged: 3% daily-loss halt, three-stop-out halt, API-error halt,
   position-reconciliation halt, and the `PAUSE AUTONOMOUS TRADING` command.

## Section 6 — Logging and notifications

- Every scan gets a concise scan record.
- Every entry/exit gets a Trade Card: strategy mode, LUC label (context only), catalyst/source
  timestamp, daily *and* hourly technical evidence, entry, stop, targets, risk dollars, planned
  holding window, settled-cash status, and whether a same-day protective exception applied.
- Post-fill and circuit-breaker notifications go through the configured Claude/GitHub path.
  Notifications report activity; they do not request per-trade approval while Mode B autonomous
  authority is active (note: autonomous execution remains PAUSED as of this writing — see
  CLAUDE.md §14).

## Account/broker facts checked 2026-08-13 (informational, not authoritative — re-verify live)

- Agentic Account (••••8058): `type: limited_margin` — not a plain cash account, not full margin.
  Limited margin permits trading with unsettled funds without adding borrowing/leverage; it does
  not itself grant margin borrowing power. `unsettled_funds: $0.00` at check time.
- Buying power ($218.84 at check time) equaled unleveraged buying power exactly — no margin was
  extended.
- `review_equity_order` returns an `order_checks` field carrying broker alerts (buying power, PDT,
  instrument halt/marketability, etc.) for any simulated order — this is the mechanism §17 item 1
  and item 5 rely on to verify settled buying power and check for restrictions before every entry.
  A test simulate (AAPL, $1 limit vs. ~$305 market) returned a price-marketability alert, not a
  funding/PDT alert, since there was no such issue on that test order.

## Relationship to other sections

- **§3 (exposure limits)**: dollar-based caps (per-position, total-deployed, cash reserve) remain
  in force; Section 4's capacity/correlation/sizing rules are additional, not a replacement.
- **§5B (Swing Entry Gate)**: items 1-7 are the authoritative entry test.
- **§16 (Locked Exit and Loss-Control Policy)**: items 6 and 8 were directly edited 2026-08-13
  (see above); items 1-5, 7, 9-11 unchanged.
- **§6 (circuit breakers)**: unaffected and independent — a market-wide circuit breaker can still
  trigger a same-day exit under Section 2 item 3 above regardless of anything else here.
