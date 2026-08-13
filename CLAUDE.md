# AGENTIC TRADING OPERATING RULES

## 1. Account and authority
- Use Robinhood MCP only with the separate Agentic Account. Never access, transfer, or trade in my existing retail brokerage account.
- Operating mode is AUTONOMOUS_EXECUTE: orders may be placed automatically, without per-trade confirmation, whenever a candidate clears every required gate in Sections 2–6 during an automated scan (Section 10).
- For any trade discussed manually in chat, outside an automated scan, still require this exact confirmation string before placing, cancelling, replacing, or modifying an order:
  CONFIRM ORDER: [BUY/SELL] [EXACT WHOLE SHARE QUANTITY] [TICKER] LIMIT [PRICE]
- Do not treat "yes," "looks good," "go," or similar unstructured language as authorization for a manually discussed trade.
- Never initiate a deposit, withdrawal, transfer, margin borrowing, or account-setting change.

## 2. Permitted instruments — initial phase
- Long common stocks and non-leveraged ETFs only.
- No options, crypto, leveraged or inverse ETFs, short selling, margin, naked options, 0DTE, spreads, or multi-leg orders.
- Do not use fractional-share limit orders. Every equity limit order must use an exact whole-share quantity and an explicit limit price.
- Do not hard-code a ticker list. A proposed ticker must have: (a) verified LUC GREEN status or, if LUC is unavailable, strict FTA A-grade status; and (b) a verified catalyst/source.

## 3. Exposure limits
- The Agentic Account's own funded balance is the trading budget — no separate budget-approval step is required. Do not place any order if the account is unfunded or its balance is effectively zero.
- No fixed dollar or percentage ceiling on individual position size — a position may be sized as large as needed to act on a qualifying setup.
- Always maintain a minimum cash reserve of 20% of Agentic Account equity, to preserve room for new positions and rotations. Never let a purchase bring cash below this floor.
- Maximum one new position per day and three new positions per calendar week.
- Do not average down (add to a losing position). Selling an existing position to redeploy into a higher-conviction, fully gated candidate is allowed, subject to the full research gate and every other rule in this document applying to the new position as if it were a fresh buy.
- Do not increase risk after a daily realized loss of 2% or a weekly realized loss of 5% of Agentic Account equity.
- Every position must carry a live protective stop. Immediately after any buy fills, place a
  resting GTC stop order (stop_limit preferred; stop_market if a limit stop isn't practical) at
  the position's invalidation level from `technical-analysis-playbook.md`, sized to the full
  filled quantity. Never leave a filled position without an active stop order at the broker —
  this is in addition to, not instead of, the hourly scan re-checking invalidation levels.

## 4. Timing and market-event rules
- Do not open new positions during the first 15 minutes or final 15 minutes of regular U.S. market hours.
- Stop-loss, risk-reduction, and exit orders are exempt when a documented invalidation level is hit.
- Do not open a new position within 30 minutes before or after a high-impact scheduled event, including CPI, FOMC decisions, major employment data, or the company's earnings report.

## 5. Required research gate
Before every proposal, verify and log:
1. Current FTA Regime Dashboard classification.
2. Current LUC status. If the LUC sheet fails, returns 403, or cannot render, mark LUC as UNKNOWN; log the failed URL and timestamp; then require strict FTA A-grade technical evidence.
3. FTA scorecard: market-structure break, 9/20 EMA pullback, bullish reversal at support, volume confirmation, RSI/MACD alignment, and Fibonacci/support-zone context. See `technical-analysis-playbook.md` for the entry/invalidation methodology behind each of these (fib retracement zones, 9/20 EMA pullback rules, HH/HL structure, consolidation, cup and handle).
4. Catalyst from a primary or reputable source, including URL and date.
5. Exact entry limit, exact whole-share quantity, invalidation/stop level, target or review date, reward-to-risk, and portfolio-concentration check.

## 6. Circuit breakers and integrity checks
- If Agentic Account equity declines more than 3% in one day, immediately enter HARD_OBSERVE_MODE: no new orders; provide an urgent incident report.
- If Robinhood MCP returns three consecutive errors or reported positions do not match the account, cease trading until reconciliation is verified.
- If data is stale, incomplete, contradictory, or unavailable, do not infer a bullish signal and do not propose execution.
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
- If LUC, FTA, or Robinhood data cannot be accessed, mark that source UNKNOWN, log the failed URL and timestamp, and do not place or propose an executable trade unless the remaining FTA evidence is A-grade.

## 10. Automated Scanning and Execution (AUTONOMOUS_EXECUTE mode)
- Run an observation-and-execution scan hourly during regular U.S. market hours, in Pacific Time, only from 6:45 AM through 12:15 PM on U.S. trading days (approximating the requested 30-minute cadence within this environment's 1-hour minimum scheduling interval). Do not evaluate new entries during the first 15 minutes after open or the final 15 minutes before close (Section 4 still applies).
- When, and only when, a candidate clears every required gate in Sections 2–6, place the order immediately — no per-trade confirmation required.
- Immediately after any automated order placement, create a TRADE EXECUTED record: deliver it through the most reliable notification channel available in the current environment, and also create a GitHub Issue labeled `trade-alert` on this repository as a durable record. Use this exact structure:

  ```
  TRADE EXECUTED
  Ticker / instrument:
  Regime and LUC status:
  FTA score and technical evidence:
  Catalyst with source URL and timestamp:
  Exact whole-share quantity:
  Limit price:
  Invalidation / stop level:
  Reward-to-risk:
  Portfolio concentration impact:
  Order status (filled / pending / rejected):
  ```

- On a circuit breaker trip, data mismatch, market-data failure, or material uncertainty, create an URGENT RISK ALERT through the same channels and take no automated action beyond what Section 6 explicitly allows (e.g. an exit/stop order on a hit invalidation level).
- Do not configure a new external notification service (e.g. email, Telegram, webhook) or change any Robinhood account setting to support this without asking first.
- Notification channels verified available in this environment (as of 2026-08-13): Claude push notification (phone delivery depends on Remote Control being connected) and GitHub Issue creation. Email, Telegram, and generic webhook delivery are not currently configured — do not assume they exist.

The objective is disciplined compounding and capital preservation, not maximum trade frequency or "get rich quick" behavior.
