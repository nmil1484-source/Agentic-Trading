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
- Maximum total deployed capital: 80% of Agentic Account equity. Maintain at least 20% cash.
  (Raised 2026-08-13 from 50%/50% at explicit user instruction — see Section 12 change log.)
- Maximum one new position per day and three new positions per calendar week.
- Do not average down. Add only after a position is profitable or has reclaimed its technical trigger with renewed confirmation.
- Do not increase risk after a daily realized loss of 2% or a weekly realized loss of 5% of Agentic Account equity.
- **Fractional Tier-B pilots (2026-08-13, see §15) count as ordinary new positions against the caps above** — a Tier-B pilot consumes one of the same 1/day, 3/week slots as any Tier-A position, no separate or additional allowance. Tier-B allocation is also sized within whatever headroom remains under the 80%-total-deployed / 20%-minimum-cash ceiling on this line, not in addition to it.

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
3. It has at least 3 of these 6 technical confirmations (not all 6 — this replaces the old §13.B
   hard 9/20-EMA-only gate for swing candidates; §13 remains the reference methodology for *how*
   to read each one):
   - 9/20 EMA bullish alignment or reclaim;
   - price above or reclaiming the 50-day SMA;
   - breakout/retest, range contraction, or support/Fibonacci pullback location;
   - relative strength versus SPY/sector;
   - volume at least 1.2x normal or no abnormal selling pressure;
   - RSI above 45 and improving, or MACD improving.
4. It has a valid technical stop (computed per §13's methodology) and reward-to-risk of at least
   **1.5:1 when the FTA Regime Dashboard is live and valid (not UNKNOWN_DEGRADED)**. **While
   UNKNOWN_DEGRADED, every new swing entry — whole-share or fractional — requires reward-to-risk of
   at least 2:1 instead, combined with reduced position sizing** (see the Regime Rule below). This
   replaces the old §13.A floor (≥1:2, ≥1:3 while UNKNOWN_DEGRADED) for Mode B. That older floor is
   retained for Mode A if/when it's authorized to execute. This 1.5:1-normal/2:1-degraded pattern
   is the same one Tier-B fractional pilots already used before this refactor (§15 item 5) — Mode B
   now applies it consistently to whole-share entries too, rather than leaving whole-share swing
   trades on a flat floor while fractional ones flex with the regime.
5. It is outside the first 15 minutes after open and the final 15 minutes before close (§4).
6. It has no earnings or high-impact macro conflict inside the existing §4 timing rule.

LUC status (GREEN/WHITE/RED/OFF_LIST/UNKNOWN) is still logged on every swing Trade Card for
context — it is never itself a qualifying or disqualifying condition for Mode B.

#### Regime Rule for Swings
- The FTA Regime Dashboard is a risk modifier for Mode B, not a hard entry gate (same underlying
  principle as the §6 exception) — it never blocks a swing proposal outright the way LUC/Robinhood
  data unavailability still does.
- **If regime data is available and live/valid (not UNKNOWN_DEGRADED)**, use normal approved swing
  sizing and the standard ≥1.5:1 reward-to-risk floor (§5B item 4).
- **If regime data is unavailable, stale, or UNKNOWN/UNKNOWN_DEGRADED, every new swing entry
  requires reduced position size and reward-to-risk of at least 2:1** (revised 2026-08-13 from an
  earlier draft of this refactor that would have kept the floor flat at 1.5:1 regardless of regime
  state — corrected per explicit user instruction; see §12 change log). Fractional entries use the
  existing Tier-B halving, unchanged (§15 item 2/5). For whole-share entries, size the position at
  roughly half of what §3's normal cap would otherwise support for that trade, rounded down to a
  whole share — §3's actual limits are not changed by this; it's a tighter self-imposed sub-cap
  while UNKNOWN_DEGRADED, the same mechanism Tier-B already uses. Keep scanning and logging
  candidates in this state; the stronger ratio and smaller size are conditions to enter, not a
  reason to stop looking.
- If credit/volatility data shows clear market stress, or a §6 circuit breaker is active, do not
  open new swing trades — circuit breakers are unchanged by this refactor and apply regardless of
  mode.

#### Swing Exit Rules
Mode B positions — both whole-share (Tier-A sizing) and fractional (Tier-B, §15) — follow the
existing §16 Locked Exit and Loss-Control Policy mechanics unchanged: defined stop before entry, no
averaging down, breakeven at +1R, partial profit protection at +2R/+3R, momentum-failure exit, and
time-stop review after 10 sessions. (§16's applicability is broadened by this refactor from
Tier-B-only to all Mode B positions — its numbered rules themselves are not modified; see §12
change log and the note at the top of §16.) Swing target horizon is 2 to 15 trading days — do not
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
  that find nothing new still append a brief entry to `trades_log.md` (for the §3 day/week-count
  audit trail) but do not produce a routine full chat report.
- Every Trade Card must clearly label **STRATEGY: CORE_LUC_ACCUMULATION** or **STRATEGY:
  SWING_TRADING** (§7).

## 6. Circuit breakers and integrity checks
- If Agentic Account equity declines more than 3% in one day, immediately enter HARD_OBSERVE_MODE: no new orders; provide an urgent incident report.
- If Robinhood MCP returns three consecutive errors or reported positions do not match the account, cease trading until reconciliation is verified.
- If data is stale, incomplete, contradictory, or unavailable, do not infer a bullish signal and do not propose execution. **Exception (2026-08-13, user instruction): the FTA Regime Dashboard is a reference input, not a blocking gate.** If it's unavailable/stale/placeholder, classify it **UNKNOWN_DEGRADED** — log it, do not treat it as bearish, and do not let it alone block a proposal. **Compensating requirement while UNKNOWN_DEGRADED (2026-08-13):** for Mode A (and Tier-A proposals generally, if Mode A is ever authorized to execute), the §13.A reward-to-risk floor rises from ≥1:2 to **≥1:3**. **For Mode B swing trades, the compensating requirement is reward-to-risk ≥2:1 plus reduced position sizing** (2026-08-13, see §5B Regime Rule and §12 change log) — Mode B's normal floor is ≥1.5:1 when the regime dashboard is live and valid, rising to ≥2:1 with a halved position-size sub-cap while UNKNOWN_DEGRADED, for both whole-share and fractional swing entries. This matches the pattern Tier-B fractional pilots already used before this refactor (§15 item 5: halved size, ≥2:1) — now applied consistently across all of Mode B. This unavailable-data rule still fully applies, with no exception, to LUC data, Robinhood account/position data, and a specific ticker's own technical or catalyst data — only the FTA Regime Dashboard gets the UNKNOWN_DEGRADED treatment.
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
- Any future change to Section 3's exposure limits, or to the strategy-mode structure above, must
  be logged here with date and the specific before/after values.

## 13. Technical entry & stop-loss methodology (reference toolkit for both modes)
Added 2026-08-13 at user instruction as a required hard gate; **refactored 2026-08-13** so it
remains the shared reference methodology for *how* to read market structure, EMAs, Fibonacci zones,
and chart patterns in both modes, but is no longer itself the mandatory gate for Mode B swing
entries — that's now §5B's 3-of-6 test. It's still the direct, unmodified gate for Mode A if/when
authorized to execute (see §5A, §12 change log). This expands on the §5A/old-§5.3 FTA scorecard and
the §7 "Invalidation or stop level" / "Reward-to-risk" fields — those fields must show the actual
computed number and which rule below produced it.

### A. Stop-loss is mandatory, always
- No proposal reaches PROPOSE status without a specific, computed stop-loss price, in either mode.
  "Watch closely" or an unstated level is not acceptable.
- For Mode A (and Tier-A generally, if Mode A is ever authorized to execute): reward-to-risk must
  be at least 1:2 (distance to target ≥ 2x distance to stop); this rises to ≥1:3 while the FTA
  Regime Dashboard is UNKNOWN_DEGRADED (§6). **For Mode B swing trades, the reward-to-risk floor is
  the §5B test instead: ≥1.5:1 when the regime dashboard is live and valid, rising to ≥2:1 with
  reduced position sizing while UNKNOWN_DEGRADED** (2026-08-13, see §12 change log) — the same
  pattern fractional Tier-B pilots (§15) already used before this refactor, now applied
  consistently to whole-share Mode B entries too. §15's own numbered rules are unchanged by this
  refactor.
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
  when every existing gate clears, place equity orders without the user present.
- **Scope — everything else in this document still applies unchanged** to the autonomous
  Routine: permitted instruments (§2), exposure limits (§3, including the 1/day and 3/week new-
  position caps — count across BOTH manual and autonomous trades, tracked via `trades_log.md`),
  timing rules (§4), the research gate appropriate to the mode in play (§5B Swing Entry Gate for
  the swing trading this Routine actually does — see §12 change log for how this superseded the
  original LUC/FTA-gated §5 this bullet used to describe), circuit breakers (§6), and the §16 exit
  mechanics (mandatory stop-loss, defined reward-to-risk per §5B/§13.A depending on mode/tier).
  The Routine has no authority to cancel or replace orders, deposit/withdraw funds, or change
  account settings — those still require the user directly, per §1.
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
  the user where supported (see the self-bound trade-off note below).
- **Kill switch**: the user can say "STOP AUTONOMOUS EXECUTION" in this chat, or disable/delete
  the Routine directly, at any time. On that instruction, Claude disables the Routine immediately
  and reverts the Section 1 exception to inactive (the exception text stays as a historical
  record; a new dated entry here notes the revocation).
- **Status: PAUSED (2026-08-13, ~18:11 UTC).** Operational history: the first attempt (fresh
  session per firing) failed tool-access verification and was deleted — see `trades_log.md`
  history. A second Routine, self-bound to the user's primary session, ran successfully from
  08:17 UTC through 17:41 UTC (test-fire plus several scheduled and on-demand cycles, all logged
  to `trades_log.md`), correctly checking the account, circuit breakers, position caps, FTA
  Regime Dashboard, and — after the §5/§13→§5B refactor — the Swing Entry Gate, without ever
  clearing every condition needed to place a trade.
  **Paused after the strategy-mode refactor (§2/§5B/§12) landed**: the user instructed keeping the
  system in observation/alert state until autonomous execution is separately re-authorized, so the
  Routine trigger was deleted outright (not just disabled) for an unambiguous stopped state. The
  Section 1 exception permitting order placement without a live CONFIRM ORDER is **inactive** —
  this text stays as a historical record of the authorization mechanics, not a currently-active
  grant. Manual research, Trade Cards, and order confirmations in this chat are unaffected and
  remain fully available on request (§11). **Re-enabling requires**: (1) the user issuing a fresh,
  explicit authorization — the same rigor as the original "CONFIRM AUTONOMOUS EXECUTION" phrase,
  given the underlying gate has materially changed since that authorization was given — and (2)
  recreating the self-bound Routine (schedule was hourly at :30 past the hour, 14:30-19:30 UTC,
  weekdays, before this pause; will need DST adjustment after early November regardless of when
  it's re-created).

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
   80% per-position cap in §3); and whatever headroom currently remains under the shared §3 80%-
   total-deployed ceiling (i.e., 80% of equity minus everything already deployed across Tier-A and
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

7. **A Tier-B pilot counts as an ordinary new position against the existing §3 caps** — maximum
   one new position per day and three per calendar week, Tier-A and Tier-B combined. There is no
   separate or additional Tier-B allowance beyond those shared limits. Never average down. Add
   only after a position is profitable and original support remains valid.

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
position, whole-share (Tier-A) or fractional (Tier-B)** — the numbered rules below are themselves
unmodified by that refactor; only which positions they apply to changed, per explicit instruction
("apply the existing locked exit policy" to swing exits generally). Full text also maintained in
`docs/fractional_tier_b_policy.md` (written when this section was Tier-B-only; treat this section
of CLAUDE.md as authoritative on scope). All existing circuit breakers (§6) remain in force
unchanged and independently of this section.

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
   position at the earliest available eligible execution. Log actual slippage and enter
   HARD_OBSERVE_MODE (§6) for the remainder of that session.

5. Breakeven rule: after a position reaches +1R, move the stop to entry price or the nearest
   higher technical support, whichever is higher. Never move the stop lower afterward.

6. Profit protection: at +2R, sell 50% of the position and trail the remainder below the 9/20
   EMA, prior-day low, or nearest higher support. At +3R, sell an additional 25% and continue
   trailing the remaining 25%.

7. Momentum failure: exit the full remaining position if price closes below the 20-EMA for two
   consecutive sessions and RSI/MACD are both deteriorating, unless the original stop would
   trigger sooner.

8. Time stop: if the position has not reached +0.5R within 10 trading sessions, issue a mandatory
   exit review. If price is below entry and momentum is not improving, exit the full position —
   do not keep capital trapped in a stagnant trade.

9. No averaging down. No exception for "oversold," social-media sentiment, or a lower price. An
   invalidated swing trade is closed, documented, and not re-entered for 30 calendar days unless a
   fresh setup meeting the full §5B Swing Entry Gate (or, for a would-be Mode A position, the §5A
   bar) forms.

10. After any three stop-outs in a rolling 10-trading-day window (Tier-A and Tier-B combined),
    enter HARD_OBSERVE_MODE (§6). No new entries of either tier until the next full regime
    review is complete.

11. Record every exit with planned loss, actual loss, slippage, the rule that triggered the exit,
    and whether the exit submitted successfully, in `trades_log.md`. These records must be
    included in the weekly system review.
