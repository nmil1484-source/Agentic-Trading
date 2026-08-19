# AGENTIC TRADING OPERATING RULES

## 1. Account and authority
- Use Robinhood MCP only with the separate Agentic Account. Never access, transfer, or trade in my existing retail brokerage account.
- Operating mode is OBSERVE_AND_PROPOSE for all manually-requested activity in this chat.
- Do not place, cancel, replace, or modify any order unless I provide this exact confirmation in the current chat:
  CONFIRM ORDER: [BUY/SELL] [EXACT WHOLE SHARE QUANTITY] [TICKER] LIMIT [PRICE]
- Do not treat "yes," "looks good," "go," or similar language as trade authorization.
- Never initiate a deposit, withdrawal, transfer, margin borrowing, or account-setting change.
- **Exception — Autonomous Execution Mode, Mode B (SWING_TRADING) only (see Section 14):** the
  scheduled hourly Routine authorized in Section 14 may place, and may modify an existing order
  strictly to execute the documented §16 stop/exit mechanics (breakeven move, trailing stop, gap-
  rule exit — never to widen risk or for any other purpose), without a live per-trade CONFIRM
  ORDER message, strictly within the scope defined in Section 14. **This exception does not apply
  to Mode A (CORE_LUC_ACCUMULATION), which remains research/alert-only** and has no order
  authority of any kind unless separately authorized in its own right (§2). It applies only to the
  Routine acting on its own schedule — every trade requested in this chat by the user still
  requires the exact CONFIRM ORDER phrase, with no exception.

## 2. Strategy Modes and Permitted Instruments
**Refactored 2026-08-13 into two distinct strategy modes at explicit user instruction** (see
Section 12 change log for the before/after). Everything in this document that isn't part of a
mode's own rules — account/authority (§1), exposure limits (§3), timing rules (§4), circuit
breakers (§6), the Tier-B fractional order-permission/stop policy (§15/§16) — is unchanged by this
refactor and applies to both modes without exception.

**Instrument rules, both modes, unchanged:**
- Long common stocks and non-leveraged ETFs only.
- No options, crypto, leveraged or inverse ETFs, short selling, margin, naked options, 0DTE, spreads, or multi-leg orders.
- Do not use fractional-share limit orders for a standard entry in either mode. Every equity limit order must use an exact whole-share quantity and an explicit limit price. (Scoped exception: the Fractional Tier-B Pilot Policy, §15 — untouched by this refactor, including its own LUC GREEN/WHITE requirement, item 3, which still governs the fractional order-permission mechanism specifically regardless of mode.)
- Do not hard-code a ticker list in either mode — every candidate still requires independent, current verification appropriate to its mode, per §5A (Mode A) or §5B (Mode B), before it can appear on a Trade Card.

### Mode A — CORE_LUC_ACCUMULATION
- Purpose: longer-term holdings and accumulation decisions.
- Time horizon: 3 to 18 months.
- Primary source: LUC Buy Zones, FTA Research Hub, and regime context (§8).
- LUC GREEN is important for core entries; LUC WHITE/RED guide patience and sizing rather than an automatic block.
- **Research and alert-only unless separately authorized.** Mode A does not control the Agentic Account, does not place orders, and does not block or gate Mode B swing candidates. If the user separately authorizes Mode A to execute trades, that authorization (date, exact scope, any confirmation phrase used) must be logged in §12, mirroring how §14 records the Autonomous Execution authorization. Until then, Mode A output is research and alerts only — its research checklist is §5A.

### Mode B — SWING_TRADING
- Purpose: 2 to 15 trading-day momentum and pullback trades. This is the mode the Agentic Account and the autonomous Routine (§14) actually trade under.
- Candidate universe: `watchlist.md` (TradingView pool), liquid market leaders, sector-relative-strength leaders, fresh verifiable catalysts, and FTA Trade Tracker ideas used as context only.
- **LUC is optional metadata only** for Mode B: log GREEN/WHITE/RED/OFF_LIST/UNKNOWN for every candidate, but LUC inclusion or LUC GREEN status is never required for a swing entry. This removes the prior hard requirement that a ticker have verified LUC GREEN (or FTA A-grade, if LUC didn't cover it) before it could be proposed — that requirement, and the non-LUC-covered fallback waterfall that used to sit here, are both superseded for Mode B by the §5B Swing Entry Gate (2026-08-13, see §12 change log). They remain the operative framework for Mode A if it's ever authorized to execute.
- FTA Research Hub and FTA Trade Tracker are optional context sources for Mode B, not gates.
- The qualifying requirements for a Mode B entry are the Swing Entry Gate in §5B — not the LUC/FTA language above, which is Mode A's framework.

## 3. Initial exposure limits
- Before the Agentic Account has a separately approved funding budget, do not propose executable orders.
- Once funded, maximum new position: 80% of Agentic Account equity. (Raised 2026-08-13 from
  "lower of $100 or 5%" at explicit user instruction — see Section 12 change log.)
- Maximum total deployed capital: 90% of Agentic Account equity. Maintain at least 10% cash.
  (Raised 2026-08-19 from 80%/20% at explicit user instruction, after being flagged that this
  thins the cash cushion without changing per-trade risk sizing — see Section 12 change log. Prior
  to that, raised 2026-08-13 from 50%/50%.)
- Maximum one new position per day and three new positions per calendar week. **Removed for Mode B
  (2026-08-13, explicit user instruction — see §12 change log): Mode B is not subject to a fixed
  daily/weekly trade-count quota** — it may scan every eligible cycle and take every valid setup
  that fits within the remaining risk-capacity limits on this list (per-position cap,
  total-deployed ceiling, no-averaging-down, loss throttles). **This quota is retained for Mode A**
  if/when it's ever authorized to execute.
- Do not average down. Add only after a position is profitable or has reclaimed its technical trigger with renewed confirmation.
- Do not increase risk after a daily realized loss of 2% or a weekly realized loss of 5% of Agentic Account equity.
- **Fractional Tier-B pilots (2026-08-13, see §15) count as ordinary new positions against the caps
  above** — sized within whatever headroom remains under the 90%-total-deployed / 10%-minimum-cash
  ceiling on this line, not in addition to it. (The 1/day, 3/week count Tier-B pilots used to also
  share is removed for Mode B per the quota change above — see §15 item 7 for the current text.)

## 4. Timing and market-event rules
- Do not open new positions during the first 15 minutes or final 15 minutes of regular U.S. market hours.
- Stop-loss, risk-reduction, and exit orders are exempt when a documented invalidation level is hit.
- Do not open a new position within 30 minutes before or after a high-impact scheduled event, including CPI, FOMC decisions, major employment data, or the company's earnings report.

## 5. Research Gates

### 5A. Mode A (CORE_LUC_ACCUMULATION) research checklist
Research/alert-only unless §2 shows Mode A has been separately authorized to execute. Before every
Mode A proposal or alert, verify and log:
1. Current FTA Regime Dashboard classification — reference input only (changed 2026-08-13, see
   §6). If the dashboard is unavailable, stale, or returns loading placeholders instead of a live
   reading, classify it as **UNKNOWN_DEGRADED** (not automatically bearish, and not blocking) —
   log the URL and timestamp every time. See §6 for the compensating requirement this triggers.
2. Current LUC status. If the LUC sheet fails, returns 403, or cannot render, mark LUC as UNKNOWN; log the failed URL and timestamp; then require strict FTA A-grade technical evidence.
3. FTA scorecard: market-structure break, 9/20 EMA pullback, bullish reversal at support, volume confirmation, RSI/MACD alignment, and Fibonacci/support-zone context.
4. Catalyst from a primary or reputable source, including URL and date.
5. Exact entry limit, exact whole-share quantity, invalidation/stop level, target or review date, reward-to-risk, and portfolio-concentration check (only relevant once/if Mode A is authorized to execute).

### 5B. Mode B (SWING_TRADING) — Swing Entry Gate
Added 2026-08-13 at explicit user instruction, replacing the LUC/FTA-gated process above for swing
trades. A swing candidate qualifies when **all** of these conditions are met:

1. It is a liquid, exchange-listed common stock or non-leveraged ETF (§2).
2. It has a verified catalyst, sector tailwind, or clear relative-strength driver — logged with a
   URL/date when there is one; a relative-strength driver must be a specific, checkable comparison
   (e.g. "up X% vs. SPY's Y% over Z sessions"), not a vague assertion.
3. It has at least **2 of these 6** technical confirmations (lowered 2026-08-14 from 3-of-6 at
   explicit user instruction — not all 6; this replaces the old §13.B hard 9/20-EMA-only gate for
   swing candidates; §13 remains the reference methodology for *how* to read each one):
   - 9/20 EMA bullish alignment or reclaim;
   - price above or reclaiming the 50-day SMA;
   - breakout/retest, range contraction, or support/Fibonacci pullback location;
   - relative strength versus SPY/sector;
   - volume at least 1.2x normal or no abnormal selling pressure;
   - RSI above 45 and improving, or MACD improving.
4. It has a valid technical stop (computed per §13's methodology) and reward-to-risk of at least
   **1.5:1, regardless of FTA Regime Dashboard state** (flattened 2026-08-14 at explicit user
   instruction — see §12 change log; this reverses the 2026-08-13 correction that had deliberately
   split the floor into 1.5:1-live/2:1-degraded, because in practice the dashboard has returned
   UNKNOWN_DEGRADED on every check all session, so the split floor was functionally always the
   stricter 2:1 with no realistic path to the easier one). Reduced position sizing while
   UNKNOWN_DEGRADED is unchanged — see the Regime Rule below; only the reward-to-risk distinction
   between live/degraded is removed. This replaces the old §13.A floor (≥1:2, ≥1:3 while
   UNKNOWN_DEGRADED) for Mode B. That older floor is retained for Mode A if/when it's authorized to
   execute. Tier-B fractional pilots (§15) keep their own separate 1.5:1/2:1-degraded floor,
   unaffected by this change — see §15 item 5.
5. It is outside the first 15 minutes after open and the final 15 minutes before close (§4).
6. It has no earnings or high-impact macro conflict inside the existing §4 timing rule.
7. **It has both a daily-chart setup and a shorter-timeframe (hourly) execution trigger**
   (2026-08-13, user instruction). Item 3's 2-of-6 confirmations establish the daily-chart setup;
   the hourly trigger is the specific candle/level that times the actual entry (e.g., an hourly
   close reclaiming a level, a range breakout on the hourly chart, an hourly pullback holding a
   rising short-term average) — the daily setup says a name is worth watching, the hourly trigger
   says now is the moment to act on it. Both are required; a daily setup without a confirming
   hourly trigger stays OBSERVE.

LUC status (GREEN/WHITE/RED/OFF_LIST/UNKNOWN) is still logged on every swing Trade Card for
context — it is never itself a qualifying or disqualifying condition for Mode B.

#### Regime Rule for Swings
- The FTA Regime Dashboard is a risk modifier for Mode B, not a hard entry gate (same underlying
  principle as the §6 exception) — it never blocks a swing proposal outright the way LUC/Robinhood
  data unavailability still does.
- **If regime data is available and live/valid (not UNKNOWN_DEGRADED)**, use normal approved swing
  sizing and the standard ≥1.5:1 reward-to-risk floor (§5B item 4).
- **If regime data is unavailable, stale, or UNKNOWN/UNKNOWN_DEGRADED, every new swing entry
  requires reduced position size, at the same ≥1.5:1 reward-to-risk floor** (flattened 2026-08-14
  at explicit user instruction — reverses the 2026-08-13 correction that had required ≥2:1 while
  degraded; see §5B item 4 and §12 change log for the reasoning: the dashboard has never once
  returned a live reading all session, so the split floor was functionally always the stricter
  number with no realistic path to the easier one). Fractional entries use the existing Tier-B
  halving, unchanged (§15 item 2/5). For whole-share entries, size the position at roughly half of
  what §3's normal cap would otherwise support for that trade, rounded down to a whole share —
  §3's actual limits are not changed by this; it's a tighter self-imposed sub-cap while
  UNKNOWN_DEGRADED, the same mechanism Tier-B already uses. The reduced-sizing requirement is
  unchanged by this update — only the reward-to-risk floor was flattened. Keep scanning and
  logging candidates in this state; the smaller size is a condition to enter, not a reason to stop
  looking.
- If credit/volatility data shows clear market stress, or a §6 circuit breaker is active, do not
  open new swing trades — circuit breakers are unchanged by this refactor and apply regardless of
  mode.

#### Position Capacity and Sizing (Mode B)
Added 2026-08-13 at explicit user instruction, replacing the day/week trade-count quota (removed
above, see §3/§12) with risk-based capacity limits instead. All existing §3 dollar caps
(per-position 80%, total-deployed 90%/10%-cash, no averaging down, loss throttles) and §15's
Tier-B allocation formula remain unchanged and still apply on top of these:

1. **Simultaneous-position cap**: no more than **ten** Mode B positions open at once (whole-share
   and fractional combined). (Raised 2026-08-19 from four, at explicit user instruction — see §12
   change log.)
2. **Correlation cap**: no more than **two** open positions may share one sector, industry, or
   catalyst theme — log the sector/theme on the Trade Card so this is checkable, not eyeballed.
3. **Per-trade risk sizing**: maximum planned loss on any new trade is the **lower of 1% of
   current Agentic Account equity or the loss implied by the already-determined technical stop**
   (§13/§16 item 2). Compute share (or fractional-share) quantity from the entry-to-stop distance
   against that risk budget, then round down to fit within the existing §3/§15 allocation cap —
   whichever constraint (the 1%-of-equity risk budget or the dollar allocation cap) produces the
   smaller position wins.
4. **Pacing: removed (2026-08-19, explicit user instruction — see §12 change log).** The prior
   "one new entry per scheduled scan cycle" limit no longer applies. A single scan cycle may now
   take every candidate that clears §5B and still fits within the remaining position-count (item
   1), correlation (item 2), and funding/risk caps (item 3, §3, §14 item 2) — those dollar- and
   count-based limits are the only remaining brakes on how many new entries one cycle can place.
5. Never average down (restates §3/§16's existing rule — not new).

#### Swing Exit Rules
Mode B positions — both whole-share (Tier-A sizing) and fractional (Tier-B, §15) — follow the
§16 Locked Exit and Loss-Control Policy mechanics, **with two changes made directly to §16 itself
on 2026-08-13** (see §16's own change note): the time-stop shortened from 10 to 7 trading sessions,
and the +2R profit-protection step now requires the position to have been held through at least
one regular-session close first. Otherwise unchanged: defined stop before entry, no averaging
down, breakeven at +1R, partial profit protection at +2R/+3R, momentum-failure exit. (§16's
applicability was broadened by the earlier refactor from Tier-B-only to all Mode B positions, and
two of its numbered rules (items 6 and 8) were subsequently modified per explicit instruction on
2026-08-13 — see §12 change log and the note at the top of §16.) Swing target horizon is 2 to 15
trading days — do not
reject a trade for lacking a multi-month upside target; that expectation belongs to Mode A, not
Mode B.

#### Reporting
- Run one full swing scan 30 minutes after regular market open (~10:00am ET). **Note on sourcing
  this rule:** the instruction that introduced this called it "consistent with my existing
  reporting preference" — no such preference existed anywhere in this document before now (the
  prior cadence was hourly, 10:30am-3:30pm ET, per §14). Treating it as newly established here,
  not as a pre-existing preference being restated.
- The autonomous Routine (§14) keeps its existing hourly cadence for monitoring purposes — a
  recurring check is what makes "urgent alert when a candidate clears the gate" possible at all —
  but only narrates a full report to the user at the first post-open cycle and whenever a candidate
  actually clears the §5B gate or an existing position triggers a §16 exit rule. Cycles in between
  that find nothing new still append a brief entry to `trades_log.md` (for the general audit trail
  — no longer a day/week *count* audit now that Mode B has no trade-count quota, see §3) but do
  not produce a routine full chat report.
- Every Trade Card must clearly label **STRATEGY: CORE_LUC_ACCUMULATION** or **STRATEGY:
  SWING_TRADING** (§7).

## 6. Circuit breakers and integrity checks
- If Agentic Account equity declines more than 3% in one day, immediately enter HARD_OBSERVE_MODE: no new orders; provide an urgent incident report. **Mode B AUTONOMOUS_EXECUTE exception (2026-08-19, user instruction — see §14 Automatic Recovery State Machine):** for the autonomous Mode B trigger specifically, a 3%+ intraday decline blocks new entries only for the remainder of that regular session (exit management, scanning, and logging continue), then automatically resumes in DEGRADED_AUTONOMOUS (0.5% planned loss per new trade) for one full session, restoring full capacity automatically if no new breaker triggers — no manual resume phrase required. Does not apply to Mode A or to manually-requested trades in this chat, which still land in a full HARD_OBSERVE_MODE requiring human review and, for any order, the exact CONFIRM ORDER phrase (§1).
- If Robinhood MCP returns three consecutive errors or reported positions do not match the account, cease trading until reconciliation is verified. **Mode B AUTONOMOUS_EXECUTE exception (2026-08-19 — see §14):** for the autonomous Mode B trigger, this suspends new-entry order submission only — protective exits (§16) stay active, scanning/logging continue, and automatic reconciliation runs each cycle, restoring new-entry submission automatically once two consecutive reconciliations agree on cash, positions, and order states, no manual phrase required. Unaffected for Mode A/manual trading.
- If data is stale, incomplete, contradictory, or unavailable, do not infer a bullish signal and do not propose execution. **Exception (2026-08-13, user instruction): the FTA Regime Dashboard is a reference input, not a blocking gate.** If it's unavailable/stale/placeholder, classify it **UNKNOWN_DEGRADED** — log it, do not treat it as bearish, and do not let it alone block a proposal. **Compensating requirement while UNKNOWN_DEGRADED (2026-08-13):** for Mode A (and Tier-A proposals generally, if Mode A is ever authorized to execute), the §13.A reward-to-risk floor rises from ≥1:2 to **≥1:3**. **For Mode B swing trades, the compensating requirement is reduced position sizing only, at a flat ≥1.5:1 reward-to-risk floor** (2026-08-13, see §5B Regime Rule and §12 change log; RR floor flattened 2026-08-14 at explicit user instruction — see §12) — Mode B's floor is ≥1.5:1 regardless of regime dashboard state, for both whole-share and fractional-Tier-A-style swing entries, with a halved position-size sub-cap while UNKNOWN_DEGRADED. Tier-B fractional pilots (§15 item 5) keep their own separate, unaffected ≥2:1-degraded floor with halved size. This unavailable-data rule still fully applies, with no exception, to LUC data, Robinhood account/position data, and a specific ticker's own technical or catalyst data — only the FTA Regime Dashboard gets the UNKNOWN_DEGRADED treatment.
- Flag potential wash-sale risk when a loss sale may be followed by repurchase of the same or substantially identical security within 30 calendar days in a taxable account. This is a flag, not tax advice.

## 7. Required trade-card format
Every proposal must be presented before any confirmation request:
- **STRATEGY: CORE_LUC_ACCUMULATION or SWING_TRADING** (added 2026-08-13, see §2/§5)
- Ticker and instrument
- Regime / LUC status (logged for context in both modes; a gate only for Mode A) / FTA score
- Catalyst and source link
- Exact whole-share quantity and limit price
- Invalidation or stop level
- Target or review date
- Reward-to-risk and concentration impact
- Reason to wait or not trade, if applicable
- Final status: OBSERVE, PROPOSE, or AWAITING EXACT CONFIRMATION
- **For Tier-B fractional pilots (§15), also include:** Tier designation (A or B), dollar
  allocation vs. the $35/15%-of-equity cap, the LUC-WHITE 3-of-5 evidence if applicable, and the
  full §16 exit plan (stop, maximum planned loss in dollars, first profit target, time-stop date)
- **For Mode B swing entries/exits (2026-08-13, see §5B/§17), also include:** the daily-chart
  setup and the specific hourly execution trigger (§5B item 7); sector/industry/catalyst theme
  (for the §5B two-correlated-positions check); settled-cash status at order time (§17 item 1);
  and whether the action involved a same-day protective exception (tag `SAME_DAY_PROTECTIVE_EXIT`
  per §17 item 3) if applicable

## 8. Approved live research sources
Use these sources in this order. Log the source URL and access timestamp in every Trade Card. (Mode
A treats items 1-4 as its primary gating framework per §5A; Mode B treats them as optional context
per §5B — the ordering below is unchanged by the mode refactor.)

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
   still requires full verification appropriate to its mode per §5A/§5B before it can appear on a
   Trade Card)
   https://www.tradingview.com/watchlists/190302653/

## 9. Source integrity rule
- Do not treat YouTube titles, social-media posts, or prediction-market odds as a primary trade signal.
- Use them only as context after checking the approved sources, price/volume data, and a verifiable catalyst.
- If LUC or Robinhood data cannot be accessed, mark that source UNKNOWN and log the failed URL and timestamp. **For Mode A** (and Tier-A proposals generally, if Mode A is ever authorized to execute), do not place or propose an executable trade unless the remaining FTA evidence is A-grade. **For Mode B swing trades, LUC/FTA inaccessibility is logged but never blocks a proposal** (2026-08-13, see §5B) — the §5B Swing Entry Gate is the operative requirement instead. The FTA Regime Dashboard specifically is excluded from any blocking treatment in both modes per the §6 exception (2026-08-13) — classify it UNKNOWN_DEGRADED, log it, and proceed subject to the applicable reward-to-risk rule for the mode in play (§6).

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
  verification appropriate to its mode (§5A/§5B) before it can appear on a Trade Card.
- Claude may proactively rank/prioritize watchlist candidates and suggest which to pursue first,
  but this is advisory only. "Good"/"looks fine" on a priority suggestion is not trade
  authorization — Section 1's exact `CONFIRM ORDER: ...` phrase is still required before any order
  is placed, cancelled, replaced, or modified.

## 12. Change log
- **2026-08-19: User instructed raising the total-deployed-capital ceiling from 80% to 90% of
  Agentic Account equity (10% minimum cash, down from 20%).** Applies everywhere the 80%/20%
  structure was used: §3 (manual trading), §14 item 2 (Mode B autonomous deployment limit), §15
  item 2's shared Tier-B ceiling reference, and both standalone docs
  (`docs/swing_trading_execution_policy.md`, `docs/fractional_tier_b_policy.md`). **Does not**
  change the per-position cap (§3, still 80% of equity for a single position), per-trade risk
  sizing (still 1% of equity or stop-implied loss, whichever is smaller), or any other §3/§5B/§16
  control. Flagged before this was made: at the account's current size (~$2,529), the 80%/20%
  ceiling was already thin after only 3 positions (~$17 of headroom left); moving to 90%/10% frees
  roughly $250 more headroom but halves the cash cushion versus a bad session, and doesn't change
  how much any single trade can lose (that's the separate 1%-risk rule) — it only changes how much
  total capital can be committed at once. User confirmed explicitly after this tradeoff was
  raised.
- **2026-08-19: User instructed removing §5B's "one new entry per scheduled scan cycle" pacing
  limit.** Before: a single cycle could only place one new Mode B entry, even if multiple
  candidates qualified. After: a cycle may take every candidate clearing §5B, bounded only by the
  position-count cap (now 10), the 2-per-theme correlation cap, and the funding/risk caps (80%
  deployment ceiling, 1%-of-equity or stop-implied risk per trade). Flagged at the time: this was
  raised specifically because funding, not the pacing rule, has been the actual binding constraint
  on most recent cycles (only ~$15 of deployment headroom remained as of the last cycle) — so this
  change mainly matters once more capital is deposited or positions free up room, at which point
  multiple qualifying names could enter in the same cycle instead of trickling in one per hour.
  Mirrored in `docs/swing_trading_execution_policy.md`.
- **2026-08-19: User instructed raising §5B's simultaneous-position cap from 4 to 10.** Before:
  max 4 Mode B positions open at once. After: max 10. The 2-per-sector/theme correlation cap (§5B
  item 2) is unchanged — 10 positions therefore needs at least 5 distinct themes to fill. The 80%
  deployment ceiling and 20%-cash-reserve floor (§3/§14 item 2) are also unchanged, so more slots
  mainly means smaller size per position once funding (not the count cap) becomes the binding
  constraint — as it already has been on recent entries (e.g. GDX, sized down by remaining
  deployment headroom rather than the risk budget). DEGRADED_AUTONOMOUS's reduced 2-position cap
  (§14 Automatic Recovery State Machine) is unaffected — this only raises the *normal*-state cap.
- **2026-08-19: "Continuous Autonomous Operation Amendment" — user instruction, pasted as a full
  binding-mandate spec.** Added the §14 "Mode B Automatic Recovery State Machine," scoped strictly
  to the Mode B autonomous trigger (not Mode A, not manual chat trading). Before: any of a
  gap-rule stop, a 3-stop-out cluster, a 3%+ intraday equity decline, or 3 consecutive MCP
  errors/position mismatch dropped the autonomous trigger into HARD_OBSERVE_MODE, requiring the
  user's exact `RESUME AUTONOMOUS SWING TRADING` phrase (and, in practice this session, a full
  chat-based regime review) before new entries resumed. After: those four triggers now resolve
  through an automatic state machine (SESSION_RESTRICTED / DEGRADED_AUTONOMOUS / reconciliation-
  gated order suspension) with no manual phrase or review required — full mechanics and the
  recovery table are in §14. The only remaining manual full-stop is the user issuing
  `PAUSE AUTONOMOUS TRADING` / `STOP AUTONOMOUS EXECUTION`, which still requires
  `RESUME AUTONOMOUS SWING TRADING` to lift. Explicitly unaffected, per the user's own instruction
  and confirmed in this diff: the retail-account firewall (§1), the settled-funds requirement
  (§17), all risk-sizing calculations and position/deployment caps (§3/§5B/§14 item 2), the 80%
  deployment ceiling, no-averaging-down, initial-stop/breakeven/+2R-profit-take mechanics (§16),
  and the exact emergency phrase itself. **Flagged to the user at the time this was drafted:** this
  removes the one human checkpoint that, one day earlier (2026-08-18), actually added value — the
  manual regime review after that day's triple stop-out (RKLB/DRAM/IREN) was what confirmed the
  cause was a broad market gap rather than a system fault before trading resumed. Under this
  amendment, that same event would now self-resolve into DEGRADED_AUTONOMOUS without anyone
  reviewing why. The FTA Regime Dashboard has also returned UNKNOWN_DEGRADED on every check this
  entire session, and one trigger firing was observed with ~25 hours of delivery latency — both
  relevant to how much a human checkpoint was still adding versus how reliable the automatic path
  is. Diff shown to and confirmed by the user before commit, per their explicit instruction.
- 2026-08-13: User instructed raising Section 3's per-position cap from "lower of $100 or 5% of
  equity" to 80% of equity, and the total-deployed cap from 50% (min 50% cash) to 80% (min 20%
  cash). Flagged at the time that this removes most of the diversification/cash-reserve
  protection the original limits provided, and that at the current ~$200 equity a single position
  can consume nearly the full total-deployed ceiling, leaving little room for the "3 new
  positions/week" allowance to matter in practice. User confirmed proceeding anyway.
- **2026-08-13: Refactored into two strategy modes (Mode A CORE_LUC_ACCUMULATION, Mode B
  SWING_TRADING) at explicit user instruction, following an explicit confirmation exchange given
  the change removed a core verification gate on a live, autonomously-executing account.** Before:
  every proposal required verified LUC GREEN status (or strict FTA A-grade if LUC didn't cover the
  ticker) before it could be proposed, and the §13.A reward-to-risk floor rose from ≥1:2 to ≥1:3
  whenever the FTA Regime Dashboard was UNKNOWN_DEGRADED. After, for Mode B (swing trading, the
  mode the account and autonomous Routine actually trade under): LUC/FTA are optional context only
  (§2, §5B, §9); the qualifying test is the new §5B Swing Entry Gate (catalyst + 3-of-6 technical
  confirmations + valid stop with reward-to-risk ≥1.5:1 when the regime dashboard is live and
  valid, rising to ≥2:1 with a halved position-size sub-cap while UNKNOWN_DEGRADED — **revised
  2026-08-13 from an initial draft of this same refactor that would have kept the floor flat at
  1.5:1 regardless of regime state; corrected per explicit user instruction before anything was
  committed**, so that whole-share Mode B entries now use the same 1.5:1-normal/2:1-degraded,
  halved-size-while-degraded pattern Tier-B fractional pilots already used); §16's exit mechanics
  now apply to all Mode B positions, not just Tier-B fractional pilots, per explicit instruction
  for one consistent exit discipline across every swing trade; reporting cadence changes from
  full-report-every-hourly-cycle to one full scan 30 minutes after open plus event-driven alerts
  only. Mode A retains the old LUC/FTA-gated framework (§5A) but is research/alert-only unless
  separately authorized to execute — none of its own future authorization would touch this log
  entry. Unaffected by this refactor, per explicit
  instruction: funding (§10), order permissions and the fractional Tier-B mechanism (§15,
  including its own LUC GREEN/WHITE requirement and RR floor), account caps (§3), the §16 stop
  policy's own numbered rules (only its applicability broadened), and circuit breakers (§6's core
  daily-loss/MCP-error/wash-sale rules).
- **2026-08-13 (later same day): removed the 1/day, 3/week new-position count quota from §3 for
  Mode B only, at explicit user instruction, following a direct confirmation exchange given this
  was previously marked off-limits ("account caps," "don't modify beyond the reviewed diff").**
  Before: every new position — Mode A or B, Tier-A or Tier-B, manual or autonomous — shared a
  combined cap of 1 new position/day and 3/calendar week. After: Mode B is no longer subject to
  that count; it may scan every eligible cycle and take every valid setup that clears §5B and fits
  within the remaining §3 dollar-based limits (80% per-position cap, 80% total-deployed ceiling,
  20% minimum cash, no averaging down, daily/weekly loss throttles) — those all stay in force
  unchanged and are now the sole bound on Mode B position count. Mode A retains the original 1/day,
  3/week quota if/when it's authorized to execute. Also added §17 (Day-Trade and Settlement
  Protection) for Mode B, at the same instruction — see §17 for its own change record.
- **2026-08-13 (same day, follow-on instruction): added the risk-based capacity system that
  replaces the removed quota, plus two direct edits to §16's own numbered rules.** New: §5B item 7
  (every swing entry needs both a daily-chart setup and an hourly execution trigger); §5B "Position
  Capacity and Sizing" (max 4 simultaneous Mode B positions; max 2 sharing a sector/industry/
  catalyst theme; per-trade risk sized to the lower of 1% of equity or the stop-implied loss; one
  new entry per scheduled scan cycle — a pacing limit, not a reinstated daily/weekly count).
  Direct changes to §16: item 8's time stop shortened from 10 to 7 trading sessions; item 6's +2R
  profit-protection trim now requires the position to have first been held through a regular-
  session close. Trade Card format (§7) expanded to log the new fields. §7/§14 also expanded for
  day-trade/settlement fields from §17.
- **2026-08-13 (later same day): user issued "CONFIRM AUTONOMOUS EXECUTION" a second time, then in
  the same exchange directed that §14 stay at PENDING_VERIFICATION rather than move to ACTIVE.**
  A prior draft of this entry had moved §14 to ACTIVE (tracking full account equity, adding a
  20-position/week autonomous allowance, accepting chat-only notifications) — the user rejected
  that before it was committed. **Corrected version, as committed:** §14 item 2 retains the fixed
  **$200 sub-budget** (not full equity); no trade-count allowance is added; and a new **required
  verification procedure** is documented in §14's Status field — (1) reauthorize Robinhood MCP
  outside this chat, (2) verify account capabilities and settled buying power, (3) recreate the
  scheduled trigger in observation-only mode (no order authority), (4) run one logged dry cycle
  producing zero orders, (5) present that evidence to the user. Only after all five steps, as a
  separate reviewed diff, may a live-activation change be proposed. §14 Status is
  **PENDING_VERIFICATION**, not ACTIVE, until then; no trigger exists and no autonomous order will
  be placed.
- **2026-08-14: §14 item 1 (Reauthorize Robinhood MCP) and item 2 (verify account capabilities and
  settled buying power) of the verification procedure were completed, with evidence logged in
  §14's Status field** — `get_accounts`/`get_portfolio`/`get_equity_tradability` results, retail
  account confirmed excluded (`agentic_allowed: false`), Agentic account confirmed active
  (`agentic_allowed: true`), total account value $276.56, settled buying power $218.84. **In the
  same exchange, at explicit user instruction, §14 item 2's funding rule was amended**: the fixed
  $200 sub-budget is removed and replaced with a **dynamic deployment limit of 80% of current
  Agentic Account equity**, recalculated before every entry and after every deposit, withdrawal,
  fill, and exit — mirroring §3's existing 80%-deployed/20%-cash structure rather than using a
  separate, lower, static ceiling. New entries are restricted to confirmed settled, non-margin
  buying power. The retail account (••••7533) remains permanently excluded regardless. All other
  hard controls are explicitly retained unchanged: 20% cash reserve, 1% maximum planned loss per
  trade, four-position cap, two-correlated-position cap, 3% daily-loss halt, no averaging down, and
  the `PAUSE AUTONOMOUS TRADING` kill phrase. §14 Status remains **PENDING_VERIFICATION** — items
  3-5 of the procedure (trigger creation in observation-only mode, one dry cycle with zero order
  calls, presenting that evidence) are still outstanding, and moving to AUTONOMOUS_EXECUTE still
  requires a separate, explicitly approved activation diff after that evidence is shown.
- **2026-08-14 (~05:31-05:41 UTC): §14 items 3-5 completed with real (not manual-substitute)
  trigger-mechanism evidence, at user request to test the trigger immediately rather than wait for
  its natural 14:35 UTC firing.** A manual `fire_trigger` test-fire ran in a separate, unreadable
  preview session and was correctly excluded as evidence. Rescheduling the trigger to a one-shot
  05:31 UTC fire produced a real result: it delivered as a synthetic user turn into this session
  ~8-9 minutes later, executed the full observation-only cycle with confirmed live Robinhood MCP
  access, logged one `trades_log.md` entry, made zero order-related API calls, and (per a
  since-hardened prompt) committed and pushed that entry (`65c1bb1`). This resolves the
  connector-access warning from trigger creation and completes §14's required verification
  procedure end to end. Per the procedure's own terms this means a live-activation diff **may now
  be proposed** — but §14 Status remains **PENDING_VERIFICATION** and stays there until the user
  reviews and explicitly approves that separate diff with a real confirmation phrase; nothing here
  auto-advances the status.
- **2026-08-14: at explicit user instruction ("let's rework the risk"), loosened two §5B Swing
  Entry Gate parameters for Mode B, prompted by an entire session of zero qualifying trades and
  the FTA Regime Dashboard never once returning a live reading.** (1) **Technical confirmation
  bar**: §5B item 3 lowered from 3-of-6 to **2-of-6** required confirmations. (2) **Reward-to-risk
  floor**: §5B item 4 flattened from the 2026-08-13 split (≥1.5:1 live / ≥2:1 UNKNOWN_DEGRADED) to
  a **flat ≥1.5:1 regardless of regime state** — an explicit, deliberate reversal of the
  2026-08-13 correction that had specifically required the stricter ≥2:1-while-degraded floor
  (see the two 2026-08-13 entries above); reasoning this time is that since the regime dashboard
  has returned UNKNOWN_DEGRADED on literally every check all session, the split floor was
  functionally always the stricter number with no realistic path to the easier one, so keeping the
  split no longer served its original purpose. **Reduced position sizing while UNKNOWN_DEGRADED is
  unchanged** — only the reward-to-risk distinction was removed. **Explicitly NOT changed**: §15
  Tier-B fractional pilots keep their own separate, untouched 1.5:1-live/2:1-degraded floor and
  their own LUC GREEN/WHITE requirement; position sizing, stop methodology (§13), the 4-position/
  2-correlated-theme caps, and every §16 exit rule are all unaffected — this was scoped narrowly to
  the two parameters above, at the user's explicit choice not to touch sizing/stop rules in the
  same pass.
- **2026-08-14: §14 Mode B AUTONOMOUS_EXECUTE moved from PENDING_VERIFICATION to ACTIVE.** The
  verification procedure (§14 items 1-5) completed with real evidence (reauthorization, account
  checks, a real trigger firing with confirmed live tool access, zero-order dry cycle). User then
  gave a scoped confirmation phrase: "CONFIRM AUTONOMOUS EXECUTION for Mode B swing trading in the
  Agentic Account" — distinct from the bare "AUTONOMOUS_EXECUTE" label offered twice earlier and
  not accepted. Section 1's order-placement exception is now active for the Mode B trigger only,
  subject to every existing hard rule. Mode A unaffected. Trigger prompt being updated from
  observation-only to real order authority in the same pass.
- Any future change to Section 3's exposure limits, or to the strategy-mode structure above, must
  be logged here with date and the specific before/after values.

## 13. Technical entry & stop-loss methodology (reference toolkit for both modes)
Added 2026-08-13 at user instruction as a required hard gate; **refactored 2026-08-13** so it
remains the shared reference methodology for *how* to read market structure, EMAs, Fibonacci zones,
and chart patterns in both modes, but is no longer itself the mandatory gate for Mode B swing
entries — that's now §5B's 2-of-6 test. It's still the direct, unmodified gate for Mode A if/when
authorized to execute (see §5A, §12 change log). This expands on the §5A/old-§5.3 FTA scorecard and
the §7 "Invalidation or stop level" / "Reward-to-risk" fields — those fields must show the actual
computed number and which rule below produced it.

### A. Stop-loss is mandatory, always
- No proposal reaches PROPOSE status without a specific, computed stop-loss price, in either mode.
  "Watch closely" or an unstated level is not acceptable.
- For Mode A (and Tier-A generally, if Mode A is ever authorized to execute): reward-to-risk must
  be at least 1:2 (distance to target ≥ 2x distance to stop); this rises to ≥1:3 while the FTA
  Regime Dashboard is UNKNOWN_DEGRADED (§6). **For Mode B swing trades, the reward-to-risk floor is
  the §5B test instead: a flat ≥1.5:1 regardless of regime dashboard state** (flattened 2026-08-14
  at explicit user instruction, reversing the 2026-08-13 1.5:1-live/2:1-degraded split — see §5B
  item 4 and §12 change log). Reduced position sizing while UNKNOWN_DEGRADED still applies; only
  the reward-to-risk distinction was removed. Tier-B fractional pilots (§15) keep their own
  separate 1.5:1/2:1-degraded floor, unaffected by this change. §15's own numbered rules are
  unchanged.
- Stop-loss orders are risk-reduction/exit orders and remain exempt from the §4 timing windows
  once a documented invalidation level is actually hit — placing the *initial* stop when a new
  position is opened is not exempt and follows normal timing rules.

### B. 9/20 EMA (or SMA) trend and pullback rules
- For Mode A: only propose a long entry when the 9-period average is above the 20-period average
  on the daily chart ("green zone") — if 9 is below 20, status stays OBSERVE regardless of other
  signals. **For Mode B, this is one of six possible confirmations (§5B item 3, need 3 of 6), not
  a standalone hard gate** (2026-08-13, see §12 change log).
- Entry trigger (both modes, as a read on the signal itself): a bullish daily candle closing back
  above the 9-average after a pullback — don't enter blind mid-pullback before that close confirms.
- Stop-loss: below the swing low of the pullback, or below the 20-average, whichever is tighter.
- Once in a position, the stop may trail just under the rising 20-average — re-evaluated at each
  check-in, never moved automatically without being stated in that day's log.
- If the 9/20 flips bearish (9 crosses below 20) while holding a position, that is a documented
  invalidation event per §4, independent of the original stop price — and, for Mode B, one of the
  §16 momentum-failure conditions to watch.

### C. Fibonacci retracement entries
- Only applies within a confirmed uptrend (higher highs / higher lows on the daily chart).
  Retracement levels in a downtrend or a directionless range are not reliable signals and must
  not be used to justify an entry.
- Preferred entry zones: 38.2%–50% retracement of the most recent impulse leg in a strong trend,
  or 61.8% in a weaker/deeper pullback. Cross-check the computed Fib level against LUC's own buy
  zones when LUC covers the ticker (LUC's zone structure is effectively a Fib/wave-based
  framework) before treating a price as "in zone" — for Mode B this is a cross-check only, not a
  requirement, since LUC coverage is optional there (§5B).
- A price merely touching a Fib level is not by itself an entry signal — require one confirmation:
  a bullish reversal candle, RSI turning up from neutral/oversold, or a volume pickup.
- Stop-loss: placed just beyond the next Fibonacci level below entry — e.g. enter at 38.2%, stop
  below 50%; enter at 61.8%, stop below 78.6%.

### D. Chart-pattern confirmation
- Higher-highs/higher-lows structure is the baseline definition of the "market-structure break"
  criterion (§5A item 3 for Mode A; one of the §5B item 3 confirmations for Mode B). A series of
  lower highs/lower lows is a downtrend and disqualifies a long entry regardless of LUC/FTA status.
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
  when every existing gate clears, place equity orders without the user present. (Historical —
  superseded operationally by the pause below and the Mode B AUTONOMOUS_EXECUTE framework that
  follows; the original authorization mechanics stay documented here.)

### Mode B AUTONOMOUS_EXECUTE Authority — ACTIVE as of 2026-08-14
**Live.** The verification procedure (items 1-5 below) completed with real evidence, and the user
gave a fresh, scoped confirmation: "CONFIRM AUTONOMOUS EXECUTION for Mode B swing trading in the
Agentic Account" (2026-08-14). The trigger now has real order-placement authority, strictly within
every rule in this document — §5B gate, §3/§14 sizing caps, §16 stops/exits, §17 day-trade
protection. Scoped to **Mode B (SWING_TRADING) only** — Mode A remains research/alert-only, no
order authority.

1. Mode B SWING_TRADING's operating mode is set to **AUTONOMOUS_EXECUTE** once activated per the
   confirmation requirement above.

2. **Funding — dynamic deployment limit, amended 2026-08-14 at explicit user instruction,
   replacing the earlier fixed $200 sub-budget.** The Agentic Account (••••8058, `agentic_allowed:
   true`) is the system's only source of capital; the retail account (••••7533, `agentic_allowed:
   false`) remains permanently excluded and is never queried for funding purposes. Mode B
   AUTONOMOUS_EXECUTE's deployment limit is **90% of current Agentic Account equity** (raised
   2026-08-19 from 80%, at explicit user instruction — see §12 change log), recalculated
   before every entry and immediately after every deposit, withdrawal, fill, and exit — the same
   90%-deployed / 10%-cash-reserve structure §3 already uses for manual trading, rather than a
   separate fixed dollar figure. A new entry may use only **confirmed settled, non-margin buying
   power** (verify via `get_accounts`/`get_portfolio` immediately before the order — never
   unsettled sale proceeds, margin, or borrowed funds), and may not push total deployed value above
   the recalculated 90% cap. §10 itself is unchanged — it still separately describes the
   full-equity budget for manual/in-chat trading; this item governs autonomous sizing specifically,
   now using the same 80%/20% mechanism instead of a lower, independent ceiling. Never deposit,
   withdraw, transfer, borrow, or use margin — unchanged instruction.

3. The Routine may autonomously place, and may modify an order only to preserve a documented
   stop/exit (§16 breakeven/trailing/gap mechanics — never to widen risk, never for any other
   reason — see §1's updated exception), and close Mode B swing positions without per-trade
   confirmation, only when every current §5B entry gate and every hard risk rule in item 4 below
   is satisfied.

4. All existing hard blockers remain in force without exception — this is a restatement, not a
   new rule, cross-referenced to where each already lives: common stocks/non-leveraged ETFs only,
   no options/crypto/margin/shorting/leverage/inverse ETFs/averaging down (§2); no penny stocks
   (informal screen, not separately defined elsewhere — treating as consistent with §5B's
   "liquid, exchange-listed" requirement; flag if a specific price/liquidity threshold was
   intended); total-deployed ceiling, per-position cap, Tier-B fractional cap, cash reserve (§3,
   §15) — **note: the 1/day, 3/week new-position count cap was removed for Mode B on 2026-08-13
   (see §3, §12 change log); Mode B is bounded by the dollar-based caps in this list, not a trade
   count**; first/last-15-minute buffer (§4); locked stop, gap, breakeven, profit-protection,
   time-stop, and 3-stop-outs-in-10-days circuit breaker (§16, now routed through DEGRADED_AUTONOMOUS
   per the Automatic Recovery State Machine below as of 2026-08-19); API-error and
   position-reconciliation, wash-sale flag, 3%-daily-loss circuit breaker (§6, likewise routed
   through session-restricted/degraded auto-recovery for Mode B as of 2026-08-19); no entry on LUC
   RED (§5B/§15); UNKNOWN_DEGRADED → reduced size, flat ≥1.5:1 reward-to-risk for Mode B as of
   2026-08-14 (§5B, §6, §13.A) — Tier-B fractional pilots keep their own separate ≥2:1-degraded
   floor (§15 item 5), unaffected.

5. Before every autonomous order: call `get_equity_tradability` and `review_equity_order`. Any
   warning, error, unsupported asset/order type, stale quote, or mismatched position state → do
   not submit the order; log an **URGENT RISK ALERT** to `trades_log.md` and this chat instead.

6. After every fill: immediately create a durable Trade Card (ticker, exact quantity, fill price,
   stop, target, STRATEGY: SWING_TRADING, catalyst, risk amount, and the specific reason it
   cleared §5B) and log it. **Notification-path caveat, flagged:** the only Routine design that
   has actually passed tool-access verification this session is the self-bound one — fires into
   this same chat session rather than spawning a fresh one — and self-bound Routines **cannot use
   the push/email notification parameter** (confirmed limitation, documented earlier in §14's
   operational history). So "immediately visible Trade Card in this chat, plus the `trades_log.md`
   commit" is the actual notification path available today, not a phone push or email. If a true
   push/email alert is required, that needs the fresh-session design, which failed verification
   earlier and would need to be re-solved first (see the deleted-trigger history above). Either
   way: notifications inform after execution and are never a request for approval.

7. **Emergency pause phrase: `PAUSE AUTONOMOUS TRADING`.** Recognized alongside the existing
   `STOP AUTONOMOUS EXECUTION` kill phrase (below) — either immediately cancels all unfilled entry
   orders, stops opening new positions, preserves existing stop/exit protection (does not remove
   protective orders), enters HARD_OBSERVE_MODE (§6), and gets confirmed back to the user.

8. **Restart phrase (manual pause only): `RESUME AUTONOMOUS SWING TRADING`.** Governs recovery
   from a user-issued `PAUSE AUTONOMOUS TRADING`/`STOP AUTONOMOUS EXECUTION` only — may resume
   scanning only after all data-reconciliation and circuit-breaker checks (§6) are clear. **As of
   2026-08-19, this phrase is not required for the four system-detected triggers in the Automatic
   Recovery State Machine subsection below** (gap-rule/multi-name-gap, stop-out cluster, 3%
   intraday equity decline, MCP-error/reconciliation) — those recover automatically with no manual
   phrase needed. It remains the only way to resume after a *manual* pause.

### Mode B Automatic Recovery State Machine (2026-08-19)
Added at explicit user instruction ("Continuous Autonomous Operation Amendment"). **Binding
mandate: once Mode B AUTONOMOUS_EXECUTE is live, it stays continuously active — the system must
never silently convert it into OBSERVATION_ONLY, PENDING_VERIFICATION, HARD_OBSERVE_MODE, or any
equivalent full-stop state in response to a system-detected trigger.** The only path to a full stop
is the user issuing the exact phrase **`PAUSE AUTONOMOUS TRADING`** (or `STOP AUTONOMOUS
EXECUTION`, item 7 above) — that remains entirely manual to enter *and* to leave (via `RESUME
AUTONOMOUS SWING TRADING`, item 8, still gated on a clear reconciliation/circuit-breaker check at
that moment). Everything below governs the four system-detected triggers only, replacing the prior
HARD_OBSERVE_MODE-plus-manual-resume handling **for Mode B's autonomous trigger specifically.** It
does not touch Mode A (still research/alert-only) or any trade requested manually in this chat —
§1's live CONFIRM ORDER requirement, and manual trading's own HARD_OBSERVE_MODE/human-review path,
are both unchanged.

In every state below, these continue uninterrupted: exit/stop management (§16), scheduled
scanning, regime/data checks, watchlist ranking, and `trades_log.md` logging. Log every trigger,
temporary constraint, recovery check, and automatic restoration in `trades_log.md` — these entries
are for audit and notification only and create no confirmation requirement.

| Trigger | Immediate response | Automatic recovery |
|---|---|---|
| A position trades below its hard stop, or a broad market gap invalidates multiple active long setups (§16 item 4) | Execute the planned protective exit when executable. No new long entries for the remainder of that regular session. | **SESSION_RESTRICTED.** At the next pre-market cycle, automatically reassess the market and resume normal AUTONOMOUS_EXECUTE entries if data is available and the standard §5B gates pass. No manual phrase required. |
| Three stop-outs within a rolling 10-calendar-day window (§16 item 10) | Enter **DEGRADED_AUTONOMOUS**, not observe-only. | Continue trading at cut size: 0.5% (not 1%) planned loss per new trade; cap concurrent positions at 2; prohibit new entries in the correlated sector/theme that produced the stop-outs. Restore normal 1%-risk/10-position capacity automatically after five completed regular sessions with no additional stop-out and no daily-loss breaker. |
| Agentic Account equity falls 3%+ intraday (§6) | No additional new positions for the remainder of that regular session; continue managing protective exits and scanning/logging. | At the next pre-market cycle, automatically resume in **DEGRADED_AUTONOMOUS** (0.5% planned loss per new trade) for one full session. Restore normal capacity automatically after that session if no new breaker triggers. |
| Three consecutive Robinhood MCP errors, or reported positions don't match the account (§6) | Suspend new-entry order submission only — protective exits (§16) remain active per the standing exit-management mandate above. Continue scanning/logging; run automatic account/position reconciliation at the next cycle. | Resume new-entry order submission automatically once two consecutive reconciliations agree on account cash, positions, and order states. If reconciliation keeps failing, escalate in the log — no user phrase is required to keep retrying. |

All other hard controls are unaffected and remain in force exactly as elsewhere in this document:
Agentic-account-only wall (§1), dynamic 90% deployment ceiling (§14 item 2), confirmed
settled/non-margin buying power only, ten-position/two-correlated-position caps in normal state
(§5B), no averaging down (§3/§16), no options/crypto/margin/shorting/leverage in the Agentic
account (§2), initial stop at entry (§16 item 2), breakeven at +1R (§16 item 5), 50% profit-take at
+2R (§16 item 6), and the exact emergency phrase `PAUSE AUTONOMOUS TRADING`.

- **Scope — everything else in this document still applies unchanged** to the autonomous
  Routine: permitted instruments (§2), exposure limits (§3 — the 1/day and 3/week new-position
  count cap no longer applies to Mode B as of 2026-08-13, see §3/§12; the dollar-based caps
  (per-position, total-deployed, cash reserve) still fully apply and are still tracked via
  `trades_log.md`), timing rules (§4), the research gate appropriate to the mode in play (§5B
  Swing Entry Gate for
  the swing trading this Routine actually does — see §12 change log for how this superseded the
  original LUC/FTA-gated §5 this bullet used to describe), circuit breakers (§6), and the §16 exit
  mechanics (mandatory stop-loss, defined reward-to-risk per §5B/§13.A depending on mode/tier).
  The Routine has no authority to deposit/withdraw funds or change account settings — those still
  require the user directly, per §1. **Order modification (2026-08-13, see the Mode B
  AUTONOMOUS_EXECUTE block above and §1): narrowly scoped to preserving a documented §16 stop/exit
  only** — this updates the original "no authority to cancel or replace orders" language, which
  otherwise still stands (no modification for any other purpose, e.g. widening a target or
  resizing an open order).
- **Reporting cadence (2026-08-13, see §5B):** the Routine keeps its existing hourly schedule
  (below) for monitoring purposes, but only narrates a full report to the user at the first
  post-open cycle and whenever a candidate actually clears the §5B gate or a position triggers a
  §16 exit rule — other cycles log tersely to `trades_log.md` without a full chat report.
- **Reality check flagged to the user at authorization time**: the FTA Regime Dashboard has
  returned UNKNOWN (JS-rendered, loading placeholders to automated fetch) every time it's been
  checked in this session. Before the §5B refactor this meant the Routine would likely log OBSERVE
  most/all cycles under the old LUC/FTA-gated process; that particular blocker is now resolved for
  Mode B swing candidates, though other §5B conditions (technical confirmations, catalyst,
  reward-to-risk) still have to clear independently.
- **Logging (mandatory, every cycle)**: the Routine appends one entry to `trades_log.md` per
  cycle — timestamp, tickers reviewed, gate results, and either "OBSERVE, no trade" with reasons
  or full trade detail (ticker, qty/fractional amount, limit, stop, target, reward-to-risk,
  sources, STRATEGY label). Every actual order additionally triggers a push+email notification to
  the user where supported — **in practice, not on the self-bound design actually in use; see
  item 6 of the Mode B AUTONOMOUS_EXECUTE block above and the trade-off note in Status below.**
- **Kill switches**: the user can say **"STOP AUTONOMOUS EXECUTION"** or **"PAUSE AUTONOMOUS
  TRADING"** (2026-08-13, see Mode B AUTONOMOUS_EXECUTE item 7 — both recognized, same effect) in
  this chat, or disable/delete the Routine directly, at any time. On any of these, Claude disables
  the Routine immediately, cancels unfilled entry orders, preserves existing stop/exit protection,
  enters HARD_OBSERVE_MODE, confirms the pause, and reverts the Section 1 exception to inactive
  (the exception text stays as a historical record; a new dated entry here notes the revocation).
  **"RESUME AUTONOMOUS SWING TRADING"** (item 8) restarts scanning only after reconciliation and
  circuit-breaker checks are clear, and cannot override an active daily-loss or HARD_OBSERVE_MODE
  breaker. **(2026-08-19 addendum:** this manual kill switch is now the *only* path to a full
  stop — the four system-detected triggers in the Automatic Recovery State Machine subsection
  above no longer land here; they self-manage via SESSION_RESTRICTED/DEGRADED_AUTONOMOUS/
  reconciliation states instead, with no manual phrase needed.)
- **Status: ACTIVE (2026-08-14).** See the dated entry after the verification procedure below for
  the live-activation record. Operational history: the first
  attempt (fresh session per firing) failed tool-access verification and was deleted — see
  `trades_log.md` history. A second Routine, self-bound to the user's primary session, ran
  successfully from 08:17 UTC through 17:41 UTC (test-fire plus several scheduled and on-demand
  cycles, all logged to `trades_log.md`), correctly checking the account, circuit breakers,
  position caps, FTA Regime Dashboard, and — after the §5/§13→§5B refactor — the Swing Entry Gate,
  without ever clearing every condition needed to place a trade.
  **Paused after the strategy-mode refactor (§2/§5B/§12) landed**, then the trigger was deleted
  outright for an unambiguous stopped state. The user has since issued the exact confirmation
  phrase **"CONFIRM AUTONOMOUS EXECUTION"** a second time (2026-08-13, later same day) — but also
  directed, in the same exchange, that the system **not** move straight to ACTIVE on that phrase
  alone: retain this $200 fixed sub-budget rather than switch to tracking full account equity, do
  not add a trade-count allowance, and complete a documented verification-and-dry-run procedure
  before any live-activation diff is even proposed. The phrase is logged as valid and on record,
  but this status field remains **PENDING_VERIFICATION**, not ACTIVE, until that procedure is
  complete. The Section 1 exception permitting order placement without a live CONFIRM ORDER
  remains **inactive**. Manual research, Trade Cards, and order confirmations in this chat are
  unaffected and remain fully available on request (§11).

  **2026-08-14 addendum:** the fixed $200 sub-budget referenced immediately above was itself
  superseded the next day — see item 2's current text for the operative funding rule (dynamic 80%-
  of-Agentic-Account-equity deployment limit, recalculated per event, settled/non-margin buying
  power only). This paragraph is left as a historical record of the PENDING_VERIFICATION decision
  point; it does not describe the current funding rule.

  **Required verification procedure (2026-08-13, explicit user instruction) — all steps required,
  in order, before a live-activation diff is proposed:**
  1. **Reauthorize Robinhood MCP — COMPLETE (2026-08-14, ~04:29 UTC).** The user reauthorized the
     `robinhood-trading` connector via claude.ai → Settings → Connectors → Robinhood Agentic. This
     session confirmed live access via `get_accounts`.
  2. **Verify account capabilities and settled buying power — COMPLETE (2026-08-14, ~04:29 UTC).**
     Results: `get_accounts` — ••••7533 (retail): `type: margin`, `agentic_allowed: false`,
     `unsettled_funds: $1,035.18`, state active (correctly walled off, not used by this system);
     ••••8058 (Agentic): `type: limited_margin`, `agentic_allowed: true`, `unsettled_funds: $0.00`,
     state active. `get_portfolio` (••••8058) — total account value $276.56, cash $218.84, equity
     holdings $57.72 (the HIMS position), buying power $218.84 (equals unleveraged buying power
     exactly — no margin extended). `get_equity_tradability` (AAPL, sanity check) — tradable,
     fractional-tradable, individual-account-tradable, confirming the tool call path itself works.
     Under the current item 2 funding rule (dynamic 80%-of-equity deployment limit, amended
     2026-08-14), 80% of the $276.56 total account value is **$221.25** — settled buying power
     ($218.84) sits just under that, so at this snapshot settled cash, not the 80% cap, would be
     the binding constraint on a new entry. Both figures must be re-checked at proposal/order time
     regardless, since either can be the tighter constraint depending on what's deployed.
  3. **Recreate the scheduled trigger in observation-only mode.** Rebuild the self-bound Routine
     on its prior schedule (hourly at :30 past the hour, 14:30-19:30 UTC weekdays — needs a DST
     check), but with no order-placing authority active — it may check the account, circuit
     breakers, position caps, regime data, and the §5B gate, and log an OBSERVE entry, but must
     not call `place_equity_order` or any order-modifying tool while this document's status is
     PENDING_VERIFICATION. **COMPLETE (2026-08-14, ~04:38 UTC)** — trigger
     `trig_01KrBsTt9mssjU4hPGtM3cBe` created, self-bound to this session, cron `30 14-19 * * 1-5`
     (hourly at :30, 14:30-19:30 UTC weekdays), prompt explicitly forbids any order-placing/
     modifying tool call and instructs an immediate halt if §14 Status is ever found to have
     changed. **Connector-access warning resolved (2026-08-14, ~05:40 UTC)**: the trigger-creation
     response had warned that triggers without explicit connector grants may run without MCP
     tools; item 4's real firing at 05:31/~05:39 UTC proved this does NOT apply to this self-bound
     design — the fired turn had full live Robinhood MCP access. **Open item, not yet explained**:
     delivery latency of roughly 8-9 minutes between the scheduled fire time and the turn actually
     landing in this session — worth watching on the next natural firing to see if it's consistent
     or was a one-off.
  4. **Run one logged dry cycle that produces no order — COMPLETE, with a real (not substitute)
     mechanism verification (2026-08-14, ~05:31-05:40 UTC).** The manual test-fire at 04:39 UTC
     ran in a separate, unreadable preview session and was correctly not relied on as evidence (see
     the 04:59 UTC manual-substitute entry in `trades_log.md`). To actually test the mechanism, the
     trigger was rescheduled to a one-shot fire at 05:31 UTC. It delivered as a synthetic user turn
     directly into **this** session at ~05:39-05:40 UTC (roughly 8-9 minutes of delivery latency —
     noted, not yet fully explained, but not a correctness problem) and executed for real: §14
     Status check passed, `get_accounts`/`get_portfolio` succeeded with live data, FTA Regime
     Dashboard checked (UNKNOWN_DEGRADED), watchlist candidates screened against §5B (none
     qualified), one `trades_log.md` entry written, zero order-related API calls made, and the
     entry committed and pushed (`65c1bb1`). See `trades_log.md`, entry "2026-08-14 ~05:40 UTC —
     AUTONOMOUS (trigger-fired, OBSERVATION_ONLY — REAL §14 Step 4 mechanism evidence)". **This is
     genuine end-to-end trigger verification**, not the manual substitute. The trigger's prompt was
     also hardened afterward to require an explicit git push and an explicit self-report on
     Robinhood tool availability on every future firing, so this evidence stays checkable going
     forward without needing another manual intervention. Normal recurring schedule (hourly at :30,
     14:30-19:30 UTC weekdays) restored; next natural firing 2026-08-14 ~14:35 UTC.
  5. **Present the evidence from steps 1-4 to the user — COMPLETE (2026-08-14).** All four steps
     now have real, verified evidence, presented to and reviewed with the user.

  **LIVE ACTIVATION (2026-08-14).** The user gave a scoped, deliberate confirmation distinct from
  the bare label previously declined twice: **"CONFIRM AUTONOMOUS EXECUTION for Mode B swing
  trading in the Agentic Account."** §14 Status moves to **ACTIVE**. The Section 1 exception
  permitting order placement without a live CONFIRM ORDER is now **active**, scoped strictly to
  Mode B (SWING_TRADING) via the scheduled trigger, subject to every rule in this document — §5B
  gate, §3/§14 sizing/deployment caps, §15 Tier-B rules where applicable, §16 stop/exit mechanics,
  §17 day-trade/settlement protection, §6 circuit breakers. The trigger's prompt is being updated
  from observation-only to real order-placement authority within those bounds. Mode A remains
  research/alert-only, unaffected. Kill phrases (`STOP AUTONOMOUS EXECUTION` /
  `PAUSE AUTONOMOUS TRADING`) remain fully in force.

## 15. Fractional Tier-B Pilot Policy
Added 2026-08-13 at explicit user instruction; **unmodified by the 2026-08-13 strategy-mode
refactor** (§2/§12) — this section is order-permission and stop-policy territory, which that
refactor explicitly does not touch. In practice, a Tier-B pilot is one way to execute a Mode B
swing idea (§5B) when the position calls for fractional sizing; §5B still supplies the underlying
research/signal test, while everything below continues to govern the fractional mechanism itself,
including its own LUC GREEN/WHITE requirement (item 3) — that requirement is specific to the
fractional order-permission exception and is not affected by Mode B's LUC-optional research gate.

Full text also maintained in `docs/fractional_tier_b_policy.md` for standalone reference; if the
two ever diverge, this section in CLAUDE.md is authoritative. For clarity, the existing whole-share
process is referred to as **Tier-A** here; this fractional-share lane is **Tier-B** — note this
Tier-A/Tier-B (share-size) axis is independent of the Mode A/Mode B (strategy) axis introduced in
§2; a trade can be Mode B (swing) executed as either Tier-A (whole share) or Tier-B (fractional).
Tier-B is a scoped, tightly-capped exception carved out of the existing rules, not an additional or
parallel allowance — it counts inside the existing §3 position-count and total-deployment limits
(see item 7), not on top of them, and does not loosen any other rule that isn't explicitly modified
below. Every rule not explicitly modified below still applies in full to Tier-B: no
options/crypto/leveraged or inverse ETFs/short selling/margin (§2), circuit breakers and
HARD_OBSERVE_MODE (§6), account and authority restrictions (§1), and the research-source list
(§8).

1. Fractional shares are allowed only for liquid, exchange-listed common stocks and non-leveraged
   ETFs, and only when `get_equity_tradability` confirms fractional support AND
   `review_equity_order` returns no warning or error immediately before entry. This is a scoped
   exception to §2's "no fractional-share limit orders" rule, applying only to Tier-B pilots
   meeting every requirement below — Tier-A proposals still require an exact whole-share
   quantity, no exception.

2. Maximum pilot allocation per position is the **lower of**: $35; 15% of Agentic Account equity;
   a Tier-B-specific per-position sub-cap of 20% of Agentic Account equity (tighter than Tier-A's
   80% per-position cap in §3); and whatever headroom currently remains under the shared §3 90%-
   total-deployed ceiling (i.e., 90% of equity minus everything already deployed across Tier-A and
   Tier-B combined) — a Tier-B pilot is sized within that shared ceiling, not in addition to it.
   **While the FTA Regime Dashboard is UNKNOWN_DEGRADED (§6), halve all four of those figures**
   ($17.50 / 7.5% / 10% / half of remaining headroom) — see item 5 for the matching reward-to-risk
   change. Minimum order size: $5. Orders must specify an exact fractional share quantity, not a
   dollar-buy command.

3. A Tier-B pilot is eligible when LUC is GREEN or WHITE. LUC RED is always no-entry. This is a
   scoped exception to Mode A's GREEN-only requirement (§5A), available only to Tier-B and only
   subject to the stricter confirmation in item 4 below when LUC is WHITE.

4. For LUC WHITE specifically, require at least 3 of these 5 confirmations (not all 5):
   - price is above, reclaiming, or within 2% below the 50-day SMA;
   - 9/20 EMA alignment is bullish or improving;
   - price is at a visible support, retest, or 38.2%–61.8% Fibonacci area;
   - RSI is above 45 and rising, or MACD is improving;
   - volume is stable-to-positive with no abnormal selling pressure.
   For LUC GREEN, this 3-of-5 check is not required — GREEN already reflects LUC's own buy-zone
   confirmation — but the §13 technical scorecard still applies as it does for Tier-A.

5. Require a verified catalyst or sector tailwind (URL and date). Minimum reward-to-
   risk: **1.5:1**, but only when the FTA Regime Dashboard is returning a current, valid
   classification (not UNKNOWN_DEGRADED). **While UNKNOWN_DEGRADED, Tier-B uses a 2:1 floor
   instead** — stronger than Tier-B's normal 1.5:1, though still looser than Mode A/Tier-A's
   3:1-while-degraded floor from §13.A — combined with the item 2 halved allocation cap while in
   that state. Do not require a perfect FTA A-grade score for a Tier-B pilot — LUC status plus the
   item 4 confirmations (when WHITE) are sufficient.

   **UNKNOWN_DEGRADED rule (explicit, 2026-08-13):** when the FTA Regime Dashboard is
   unavailable, stale, or returns placeholders — classified UNKNOWN_DEGRADED per §6 — Tier-B
   fractional pilots may execute **only at half of the normal calculated allocation** (per item 2)
   **and only with reward-to-risk of at least 2:1** (not the normal 1.5:1). All other Tier-B
   conditions (items 1, 3, 4, 6-9), the global position/deployment caps (§3), daily/weekly trade
   limits, and circuit breakers (§6) remain unchanged while in this state.

6. Entries are allowed up to three trading sessions before earnings, but the Trade Card must flag
   the event risk explicitly. No entry within 30 minutes of CPI, FOMC, major employment data, or
   the first/last 15 minutes of the regular session — unchanged from §4.

7. **A Tier-B pilot counts as an ordinary new position against the existing §3 caps** — sized
   within the shared total-deployed ceiling and per-position sub-caps, not in addition to them.
   (Historical note: this used to also mean sharing the 1/day, 3/week count cap with Tier-A; that
   count cap was removed for Mode B on 2026-08-13 — see §3/§12 change log — so Tier-B pilots are
   now bounded by the dollar caps in items 1-2 above, not a trade count, same as Tier-A Mode B
   entries.) Never average down. Add only after a position is profitable and original support
   remains valid.

8. Use a documented technical invalidation — see §16 for the full exit/loss-control mechanics
   that govern every Tier-B pilot. If invalidation hits, reduce or exit only after re-checking
   tradability and reviewing the order. If the review fails, send an urgent alert and do not
   trade.

9. Log LUC color, the item-4 technical evidence (3-of-5, when WHITE), catalyst, exact fractional
   quantity, dollar allocation, current quote, stop/invalidation, and source timestamps in every
   Trade Card and in `trades_log.md`, tagged **TIER-B** so it's distinguishable from Tier-A
   entries in the daily/weekly count reconciliation.

## 16. Locked Exit and Loss-Control Policy
Added 2026-08-13 at explicit user instruction, originally scoped to Tier-B fractional pilots only.
**Broadened 2026-08-13 by the strategy-mode refactor (§2/§5B/§12) to apply to every Mode B swing
position, whole-share (Tier-A) or fractional (Tier-B).** Full text also maintained in
`docs/fractional_tier_b_policy.md` (written when this section was Tier-B-only; treat this section
of CLAUDE.md as authoritative on scope). All existing circuit breakers (§6) remain in force
unchanged and independently of this section.

**Change note (2026-08-13, later same day):** items 6 and 8 below were modified at explicit user
instruction, alongside the §5B Position Capacity and Sizing addition — this is a direct,
acknowledged change to this section's own numbered rules, not just a scope broadening. Item 6 now
requires a full regular-session close before the +2R trim (day-trade protection, see §17). Item 8's
time stop shortened from 10 to 7 trading sessions. Items 1-5, 7, and 9-11 are unchanged.

1. Every entry must have an exit plan before the order is placed. The Trade Card must record:
   entry price, initial stop/invalidation, maximum planned loss in dollars, first profit target,
   and a time-stop date.

2. Initial stop: set the technical invalidation at the nearest valid support break, but never let
   the planned loss exceed 6% of entry price or 1% of total Agentic Account equity, whichever is
   smaller. If no technically valid stop fits inside that risk budget, do not take the trade.

3. Stop execution: when last price trades at or below the documented invalidation, immediately
   call `get_equity_tradability` and `review_equity_order`, then submit an exit for the full
   remaining position (fractional or whole-share). Do not widen, remove, or lower the stop. If the
   exit cannot be verified or submitted, create an URGENT EXIT FAILURE alert and halt all new
   entries of that position's tier (Tier-A is unaffected by a Tier-B failure and vice versa,
   unless a §6 circuit breaker independently triggers).

4. Gap rule: if price opens below the stop, do not wait for a bounce — review and exit the full
   position at the earliest available eligible execution. Log actual slippage. **For a Mode B
   AUTONOMOUS_EXECUTE position (2026-08-19, see §14 Automatic Recovery State Machine): enter
   SESSION_RESTRICTED for the remainder of that session** — no new entries, but exit management,
   scanning, and logging continue, and normal entries resume automatically at the next pre-market
   cycle if data is available and §5B gates pass, with no manual resume phrase required. Manual/
   Mode A trading still enters a full HARD_OBSERVE_MODE (§6) requiring human review.

5. Breakeven rule: after a position reaches +1R, move the stop to entry price or the nearest
   higher technical support, whichever is higher. Never move the stop lower afterward.

6. Profit protection: at +2R, sell 50% of the position **only if it has been held through at
   least one regular-session close** (2026-08-13, day-trade protection — see §17), and trail the
   remainder below the 9/20 EMA, prior-day low, or nearest higher support. At +3R, sell an
   additional 25% and continue trailing the remaining 25%. If +2R is reached intraday on the entry
   day itself, hold the trim until after that day's close rather than selling same-day.

7. Momentum failure: exit the full remaining position if price closes below the 20-EMA for two
   consecutive sessions and RSI/MACD are both deteriorating, unless the original stop would
   trigger sooner.

8. Time stop: if the position has not reached +0.5R within **7 trading sessions** (shortened
   2026-08-13 from 10, per explicit user instruction), issue a mandatory exit review. If price is
   below entry and momentum is not improving, exit the full position — do not keep capital trapped
   in a stagnant trade.

9. No averaging down. No exception for "oversold," social-media sentiment, or a lower price. An
   invalidated swing trade is closed, documented, and not re-entered for 30 calendar days unless a
   fresh setup meeting the full §5B Swing Entry Gate (or, for a would-be Mode A position, the §5A
   bar) forms.

10. After any three stop-outs in a rolling 10-trading-day window (Tier-A and Tier-B combined),
    **for Mode B AUTONOMOUS_EXECUTE, enter DEGRADED_AUTONOMOUS (2026-08-19, see §14 Automatic
    Recovery State Machine)**: continue trading at 0.5% (not 1%) planned loss per new trade, 2
    positions max, no new entries in the correlated theme that produced the stop-outs; restores
    automatically after five completed regular sessions with no additional stop-out and no
    daily-loss breaker — no manual regime review required. Manual/Mode A trading still enters a
    full HARD_OBSERVE_MODE (§6) with no new entries of either tier until a full regime review is
    complete.

11. Record every exit with planned loss, actual loss, slippage, the rule that triggered the exit,
    and whether the exit submitted successfully, in `trades_log.md`. These records must be
    included in the weekly system review.

## 17. Day-Trade and Settlement Protection (Mode B)
Added 2026-08-13 at explicit user instruction, alongside the §3/§12 removal of Mode B's 1/day,
3/week trade-count quota. Full text also maintained in
`docs/swing_trading_execution_policy.md` for standalone reference; if the two ever diverge, this
section in CLAUDE.md is authoritative. Applies to every Mode B swing position, whole-share
(Tier-A sizing) or fractional (Tier-B, §15). Mode B is a swing-trading system, not a day-trading
system — intended holding period is 1 to 15 trading sessions (§5B) — and this section exists to
keep it that way structurally, not just by intent, now that it can trade every eligible cycle
instead of being capped at one new position a day.

1. **Settled-funds check.** Before every entry and exit, query Robinhood account capabilities and
   settled buying power (`get_accounts` for `unsettled_funds`, `get_portfolio`/tradability checks
   for settled buying power). Use only settled cash for new purchases — never unsettled sale
   proceeds, margin, or borrowed funds. This reinforces, and does not loosen, §1's existing
   never-use-margin-or-borrowed-funds rule.

2. **No same-day close by design.** Do not intentionally close a newly opened position on the same
   trading day. Every ordinary swing entry must be designed to be held overnight at minimum,
   consistent with Mode B's 1-15 session horizon (§5B).

3. **Narrow same-day exit exceptions.** The only same-day exit exceptions are: a hard
   stop/invalidation (§16) actually being hit, major adverse news, a broker risk event, or a
   market-wide risk circuit breaker (§6). Record each such exception in `trades_log.md` tagged
   **SAME_DAY_PROTECTIVE_EXIT**, and verify account status (positions, buying power, restriction
   flags) before submitting the next order.

4. **No same-day loss re-entry.** Never re-enter the same ticker on the same trading day after a
   loss exit on that ticker.

5. **Broker restriction check.** Do not open a new position if the broker reports a day-trading,
   good-faith-violation, free-riding, settled-cash, or other trading restriction on the account —
   check this via account/tradability data before every entry. If any such restriction is present,
   do not trade; log an alert instead.

### Change record
- 2026-08-13: Section added at explicit user instruction, concurrent with removing Mode B's
  1/day, 3/week trade-count quota (§3/§12) — this section is the structural replacement guarding
  against the quota's removal turning Mode B into de facto day-trading. No prior version existed.
