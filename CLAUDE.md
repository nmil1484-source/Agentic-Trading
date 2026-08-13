# AGENTIC TRADING OPERATING RULES

## 1. Account and authority
- Use Robinhood MCP only with the separate Agentic Account. Never access, transfer, or trade in my existing retail brokerage account.
- Operating mode is OBSERVE_AND_PROPOSE for all manually-requested activity in this chat.
- Do not place, cancel, replace, or modify any order unless I provide this exact confirmation in the current chat:
  CONFIRM ORDER: [BUY/SELL] [EXACT WHOLE SHARE QUANTITY] [TICKER] LIMIT [PRICE]
- Do not treat "yes," "looks good," "go," or similar language as trade authorization.
- Never initiate a deposit, withdrawal, transfer, margin borrowing, or account-setting change.
- **Exception — Autonomous Execution Mode (see Section 14):** the scheduled hourly Routine
  authorized in Section 14 may place, but not cancel or replace, orders without a live per-trade
  CONFIRM ORDER message, strictly within the scope defined there. This exception applies only to
  that Routine acting on its own schedule — every trade requested in this chat by the user still
  requires the exact CONFIRM ORDER phrase, with no exception.

## 2. Permitted instruments — initial phase
- Long common stocks and non-leveraged ETFs only.
- No options, crypto, leveraged or inverse ETFs, short selling, margin, naked options, 0DTE, spreads, or multi-leg orders.
- Do not use fractional-share limit orders. Every equity limit order must use an exact whole-share quantity and an explicit limit price.
- Do not hard-code a ticker list. A proposed ticker must have: (a) verified LUC GREEN status or, if LUC is unavailable, strict FTA A-grade status; and (b) a verified catalyst/source.

## 3. Initial exposure limits
- Before the Agentic Account has a separately approved funding budget, do not propose executable orders.
- Once funded, maximum new position: 80% of Agentic Account equity. (Raised 2026-08-13 from
  "lower of $100 or 5%" at explicit user instruction — see Section 12 change log.)
- Maximum total deployed capital: 80% of Agentic Account equity. Maintain at least 20% cash.
  (Raised 2026-08-13 from 50%/50% at explicit user instruction — see Section 12 change log.)
- Maximum one new position per day and three new positions per calendar week.
- Do not average down. Add only after a position is profitable or has reclaimed its technical trigger with renewed confirmation.
- Do not increase risk after a daily realized loss of 2% or a weekly realized loss of 5% of Agentic Account equity.

## 4. Timing and market-event rules
- Do not open new positions during the first 15 minutes or final 15 minutes of regular U.S. market hours.
- Stop-loss, risk-reduction, and exit orders are exempt when a documented invalidation level is hit.
- Do not open a new position within 30 minutes before or after a high-impact scheduled event, including CPI, FOMC decisions, major employment data, or the company's earnings report.

## 5. Required research gate
Before every proposal, verify and log:
1. Current FTA Regime Dashboard classification — reference input only (changed 2026-08-13, see
   §6); log it every time, but its unavailability alone does not block a proposal.
2. Current LUC status. If the LUC sheet fails, returns 403, or cannot render, mark LUC as UNKNOWN; log the failed URL and timestamp; then require strict FTA A-grade technical evidence.
3. FTA scorecard: market-structure break, 9/20 EMA pullback, bullish reversal at support, volume confirmation, RSI/MACD alignment, and Fibonacci/support-zone context.
4. Catalyst from a primary or reputable source, including URL and date.
5. Exact entry limit, exact whole-share quantity, invalidation/stop level, target or review date, reward-to-risk, and portfolio-concentration check.

## 6. Circuit breakers and integrity checks
- If Agentic Account equity declines more than 3% in one day, immediately enter HARD_OBSERVE_MODE: no new orders; provide an urgent incident report.
- If Robinhood MCP returns three consecutive errors or reported positions do not match the account, cease trading until reconciliation is verified.
- If data is stale, incomplete, contradictory, or unavailable, do not infer a bullish signal and do not propose execution. **Exception (2026-08-13, user instruction): the FTA Regime Dashboard is a reference input, not a blocking gate** — if it is UNKNOWN/unavailable, log that and proceed on the remaining required evidence (LUC status, or strict FTA A-grade technical evidence on the specific ticker per §5.2 if LUC is unavailable, plus the §13 technical scorecard and a verified catalyst). This unavailable-data rule still fully applies, with no exception, to LUC data, Robinhood account/position data, and a specific ticker's own technical or catalyst data.
- Flag potential wash-sale risk when a loss sale may be followed by repurchase of the same or substantially identical security within 30 calendar days in a taxable account. This is a flag, not tax advice.

## 7. Required trade-card format
Every proposal must be presented before any confirmation request:
- Ticker and instrument
- Regime / LUC status / FTA score
- Catalyst and source link
- Exact whole-share quantity and limit price
- Invalidation or stop level
- Target or review date
- Reward-to-risk and concentration impact
- Reason to wait or not trade, if applicable
- Final status: OBSERVE, PROPOSE, or AWAITING EXACT CONFIRMATION

## 8. Approved live research sources
Use these sources in this order. Log the source URL and access timestamp in every Trade Card.

1. LUC Buy Zones (primary deployment map)
   https://docs.google.com/spreadsheets/d/1tZRKLjYJlxswxF3vJsFYGt5v70Ds2n1P6wdYbAjY0CU/edit

2. FTA Regime Dashboard (macro risk gate)
   https://fta-regime-dashboard.onrender.com/

3. FTA Research Hub (fundamental and thesis research)
   https://marileegrace.github.io/fta-research-hub/

4. FTA Trade Tracker
   https://fta-trade-tracker.onrender.com/

5. Robinhood MCP account data (positions, buying power, open orders, and supported order capabilities)
   https://agent.robinhood.com/mcp/trading

6. User Watchlist (candidate ticker pool — see `watchlist.md`; not pre-approved, every symbol
   still requires full LUC/FTA verification and a catalyst per Section 2)
   https://www.tradingview.com/watchlists/190302653/

## 9. Source integrity rule
- Do not treat YouTube titles, social-media posts, or prediction-market odds as a primary trade signal.
- Use them only as context after checking the approved sources, price/volume data, and a verifiable catalyst.
- If LUC or Robinhood data cannot be accessed, mark that source UNKNOWN, log the failed URL and timestamp, and do not place or propose an executable trade unless the remaining FTA evidence is A-grade. The FTA Regime Dashboard specifically is excluded from this block per the §6 exception (2026-08-13) — its unavailability is logged but does not by itself prevent a proposal.

## 10. Funding approval log
- 2026-08-13: User approved a funding budget equal to the full current equity of the Agentic
  Account (Robinhood MCP `get_portfolio`, account ••••8058), re-checked at proposal time rather
  than a fixed dollar figure. As of this date, Agentic Account equity = $200.00 (100% cash, no
  open positions). This satisfies the Section 3 funding-budget gate — executable order proposals
  may be generated, subject to all other Section 3 limits (max new position = lesser of $100 or 5%
  of current equity; max 50% total deployed capital; max 1 new position/day, 3/week; no averaging
  down; loss-based risk throttles).
- Any future re-approval or change to the funding budget must be logged here with date and
  amount/method.

## 11. Primary interaction channel
- This chat (this session/repo) is the user's primary point of control for the Agentic Account.
  All manually-requested research, Trade Card proposals, and order confirmations happen here, on
  demand, when the user is present in the conversation.
- Exception (added 2026-08-13, see Section 14): a scheduled hourly Routine now also runs
  research and, when every gate clears, execution — autonomously, without the user present. This
  is a deliberate, explicitly-confirmed exception to "not a background or scheduled process," not
  a reversal of it for manually-requested activity.
- The user may add tickers to `watchlist.md` at any time; every addition still requires full
  LUC/FTA verification and a verified catalyst per Section 2 before it can appear on a Trade Card.
- Claude may proactively rank/prioritize watchlist candidates and suggest which to pursue first,
  but this is advisory only. "Good"/"looks fine" on a priority suggestion is not trade
  authorization — Section 1's exact `CONFIRM ORDER: ...` phrase is still required before any order
  is placed, cancelled, replaced, or modified.

## 12. Risk-parameter change log
- 2026-08-13: User instructed raising Section 3's per-position cap from "lower of $100 or 5% of
  equity" to 80% of equity, and the total-deployed cap from 50% (min 50% cash) to 80% (min 20%
  cash). Flagged at the time that this removes most of the diversification/cash-reserve
  protection the original limits provided, and that at the current ~$200 equity a single position
  can consume nearly the full total-deployed ceiling, leaving little room for the "3 new
  positions/week" allowance to matter in practice. User confirmed proceeding anyway.
- Any future change to Section 3's exposure limits must be logged here with date and the specific
  before/after values.

## 13. Technical entry & stop-loss methodology (required for every proposal)
Added 2026-08-13 at user instruction — every future Trade Card's entry, invalidation/stop, and
market-structure read must be derived from this methodology, not eyeballed. This expands on the
§5.3 FTA scorecard and the §7 "Invalidation or stop level" / "Reward-to-risk" fields — those
fields must show the actual computed number and which rule below produced it.

### A. Stop-loss is mandatory, always
- No proposal reaches PROPOSE status without a specific, computed stop-loss price. "Watch
  closely" or an unstated level is not acceptable.
- Reward-to-risk must be at least 1:2 (distance to target ≥ 2x distance to stop). If the math
  doesn't clear that bar, the status stays OBSERVE.
- Stop-loss orders are risk-reduction/exit orders and remain exempt from the §4 timing windows
  once a documented invalidation level is actually hit — placing the *initial* stop when a new
  position is opened is not exempt and follows normal timing rules.

### B. 9/20 EMA (or SMA) trend and pullback rules
- Only propose a long entry when the 9-period average is above the 20-period average on the daily
  chart ("green zone"). If 9 is below 20, status stays OBSERVE regardless of other signals — this
  is the same 9/20 check already required by §5.3, made a hard gate rather than one input among
  many.
- Entry trigger: a bullish daily candle closing back above the 9-average after a pullback —
  don't enter blind mid-pullback before that close confirms.
- Stop-loss: below the swing low of the pullback, or below the 20-average, whichever is tighter.
- Once in a position, the stop may trail just under the rising 20-average — re-evaluated at each
  check-in, never moved automatically without being stated in that day's log.
- If the 9/20 flips bearish (9 crosses below 20) while holding a position, that is a documented
  invalidation event per §4, independent of the original stop price.

### C. Fibonacci retracement entries
- Only applies within a confirmed uptrend (higher highs / higher lows on the daily chart).
  Retracement levels in a downtrend or a directionless range are not reliable signals and must
  not be used to justify an entry.
- Preferred entry zones: 38.2%–50% retracement of the most recent impulse leg in a strong trend,
  or 61.8% in a weaker/deeper pullback. Cross-check the computed Fib level against LUC's own buy
  zones (LUC's zone structure is effectively a Fib/wave-based framework) before treating a price
  as "in zone."
- A price merely touching a Fib level is not by itself an entry signal — require one confirmation:
  a bullish reversal candle, RSI turning up from neutral/oversold, or a volume pickup.
- Stop-loss: placed just beyond the next Fibonacci level below entry — e.g. enter at 38.2%, stop
  below 50%; enter at 61.8%, stop below 78.6%.

### D. Chart-pattern confirmation
- Higher-highs/higher-lows structure is the baseline definition of the §5.3 "market-structure
  break" criterion. A series of lower highs/lower lows is a downtrend and disqualifies a long
  entry regardless of LUC/FTA status.
- Cup and handle: enter only on a breakout above the handle's resistance on rising volume; stop
  goes below the handle's low (or the handle's midpoint for a tighter stop).
- Consolidation/range: a name still inside a multi-week consolidation with no breakout stays
  OBSERVE — do not anticipate the breakout before it happens.

### References consulted 2026-08-13
- [Fibonacci Retracement Strategy — QuantifiedStrategies](https://www.quantifiedstrategies.com/fibonacci-trading-strategy/)
- [Fibonacci Pullback Strategy — SwingFolio](https://swingfolio.com/blog/fibonacci-pullback-trading-strategy)
- [EMA Pullback Trading Strategy — SwingFolio](https://swingfolio.com/blog/ema-pullback-trading-strategy-guide)
- [Cup and Handle Pattern — TrendSpider](https://trendspider.com/learning-center/chart-patterns-cup-and-handle/)
- [Cup and Handle Pattern: Breakout, Stop-Loss, and Targets — XS](https://www.xs.com/en/blog/cup-and-handle-pattern/)

## 14. Autonomous execution authorization
- **2026-08-13**: User issued the exact confirmation phrase **"CONFIRM AUTONOMOUS EXECUTION"**
  after being explicitly warned this removes the live per-trade CONFIRM ORDER requirement for a
  scheduled process. This authorizes an hourly automated Routine (see below) to research and,
  when every existing gate clears, place equity orders without the user present.
- **Scope — everything else in this document still applies unchanged** to the autonomous
  Routine: permitted instruments (§2), exposure limits (§3, including the 1/day and 3/week new-
  position caps — count across BOTH manual and autonomous trades, tracked via `trades_log.md`),
  timing rules (§4), the full research gate (§5, including the FTA Regime Dashboard check — if
  it's UNKNOWN, the Routine must fall back to strict FTA A-grade evidence exactly like a manual
  proposal, and if that's not met either, it logs OBSERVE and does not trade), circuit breakers
  (§6), and the §13 technical/stop-loss methodology (mandatory stop-loss, ≥1:2 reward-to-risk).
  The Routine has no authority to cancel or replace orders, deposit/withdraw funds, or change
  account settings — those still require the user directly, per §1.
- **Reality check flagged to the user at authorization time**: the FTA Regime Dashboard has
  returned UNKNOWN (JS-rendered, loading placeholders to automated fetch) every time it's been
  checked in this session. Until that changes, the Routine will likely log OBSERVE most/all
  cycles rather than trade — that is correct, rule-following behavior, not a malfunction.
- **Logging (mandatory, every cycle)**: the Routine appends one entry to `trades_log.md` per
  cycle — timestamp, tickers reviewed, gate results, and either "OBSERVE, no trade" with reasons
  or full trade detail (ticker, qty, limit, stop, target, reward-to-risk, sources). Every actual
  order additionally triggers a push+email notification to the user.
- **Kill switch**: the user can say "STOP AUTONOMOUS EXECUTION" in this chat, or disable/delete
  the Routine directly, at any time. On that instruction, Claude disables the Routine immediately
  and reverts the Section 1 exception to inactive (the exception text stays as a historical
  record; a new dated entry here notes the revocation).
- **Status: OPERATIONAL (2026-08-13), self-bound.** The first attempt (fresh session per firing)
  failed tool-access verification and was deleted — see `trades_log.md` history for the record of
  that failure. A second Routine was created **self-bound to the user's primary session**
  (fires into the existing conversation instead of spawning a new one), which sidesteps the
  connector-passing problem because that session's Robinhood MCP and GitHub tools are already
  connected. Test-fired successfully 2026-08-13 08:17 UTC — correctly checked the account,
  circuit breakers, position caps, and FTA Regime Dashboard, logged an OBSERVE outcome to
  `trades_log.md`, and committed/pushed. Schedule: hourly at :30 past the hour, 14:30-19:30 UTC
  (~10:30am-3:30pm ET), weekdays — will drift one hour when U.S. DST ends in November unless
  updated. Trade-off versus the fresh-session design: no push/email notification support (self-
  bound Routines can't use that parameter), so a placed trade is only visible by checking this
  chat or `trades_log.md` — and this session's context grows with every firing over time.
