# Premarket Shortlist — 2026-11-16

**CONTEXT/PRIORITIZATION ONLY — NEVER A GATE.** Off-watchlist names are research-only. Every
candidate still requires fresh same-cycle data and the FULL current §5B/Bearish-Mirror-Gate/§20
gate before any trade, exactly as if this file didn't exist.

- Generated: 2026-11-16T14:08:40Z (UTC) / 2026-11-16 06:08:40 (America/Los_Angeles)
- Trigger: Premarket Preparation Scan (`trig_01FRC5Yt8UVcGH8GxcAURYXX`), read-only, no order authority
- Liquidity floor used: regular-session `volume >= 500,000` shares (applied to both the watchlist
  batch and the screener results)
- **SPY freshness-check note:** the designated `get_ohlcv(AMEX:SPY, 5m)` check returned only
  Friday 2026-11-13's regular-session bars (that tool is documented "regular session only" and
  structurally cannot see premarket bars at all during premarket hours) — so it could not confirm
  freshness the way the trigger's own instructions anticipated. Treated as **EVALUATED, not
  DATA_STALE**, on the strength of the `premarket_*` fields themselves: 74 watchlist names plus
  the screener pull all returned rich, highly differentiated, internally consistent premarket
  reads (a coherent broad tech/AI-compute/crypto-adjacent selloff — SPY -0.63%, QQQ -1.31%,
  AMD -5.0%, NVDA -3.3%, NBIS -8.5%, CRWV -7.5%, INTC -5.0%, TSM -4.7% premarket, etc.), which is
  not the signature of frozen/placeholder data. Flagging this gap in the check's own method for
  the record rather than silently treating it as passed.

## Shortlist (ranked by |premarket % change| among liquid names)

| # | Ticker | Watchlist status | Premarket % chg | Premarket volume | Prior regular close | Catalyst |
|---|---|---|---|---|---|---|
| 1 | **CGON** | OFF-WATCHLIST (RESEARCH-ONLY) | **+31.92%** | n/a (screener row) | $74.40 → pm $98.15 | **Verified**: Phase 3 PIVOT-006 trial reports 68% lower recurrence risk (bladder cancer immunotherapy, cretostimogene) — Reuters/GlobeNewswire, published today ~06:04 UTC |
| 2 | **TU** (Telus) | OFF-WATCHLIST (RESEARCH-ONLY) | **+20.05%** | n/a (screener row) | $8.53 → pm $10.24 (NYSE ADR) | **Verified**: Quebecor made an unsolicited C$31B takeover proposal for Telus, ~60% premium to Telus's Nov 13 TSX close — Reuters/DJ Newswires, published today |
| 3 | **PURR** (Hyperliquid Strategies) | ON-WATCHLIST | **-9.31%** | 441,706 | $8.70 → pm $7.89 | **Unverified** — no same-day dated catalyst found; most recent news is Nov 10-13 (Q1 earnings, HYPE treasury). Likely correlated with broader crypto-adjacent weakness this morning, not confirmed |
| 4 | **NBIS** | ON-WATCHLIST | **-8.52%** | 1,838,494 | $115.88 → pm $106.01 | **Verified**: ongoing AI-datacenter capacity-increase delays and customer-prepayment concerns — "Weekly Recap: Capacity increase delayed..." and "Why Is NBIS Down Nearly 5% Overnight?", both published today; name is on its 6th straight weekly loss per recent coverage |
| 5 | **CRCL** | ON-WATCHLIST | **-7.77%** | 454,812 | $62.20 → pm $57.37 | **Unverified** — no same-day dated catalyst found explaining today's drop specifically; today's own headline is a generic "Weekly Recap" (price-target raises, partnership news), not a bearish driver. Likely correlated with broader crypto/stablecoin-sector weakness this morning, not confirmed |

## Other notable premarket movers this cycle (not in the top-5 shortlist, logged for completeness)
On-watchlist, liquid (volume ≥500k), |premarket change| ≥5%: BMNR -7.74%, CRWV -7.55%, ETHA -7.52%
(crypto-tracking ETF, not a crypto pair — see watchlist.md note), IBIT -6.96% (same), BE -6.03%,
HOOD -5.74%, DRAM -5.61%, HPE -5.57%, MU -5.71%, KEEL -5.38% (volume 327,881, below the 500k
floor — included here only as a note, not the shortlist), INTC -4.99%. AMDG showed the single
largest % move on the watchlist (-10.51% premarket, on top of -17.47% the prior regular session)
but its volume (132,890) is well below the 500k liquidity floor — excluded from the shortlist on
liquidity grounds alone, not on the size of the move.

## Quiet names
Most of the watchlist traded in line with the broad market move (roughly -1% to -5% premarket,
consistent with a broad risk-off tech morning) with nothing standing out as an idiosyncratic,
name-specific move beyond the five shortlisted above and the "other notable movers" list.
