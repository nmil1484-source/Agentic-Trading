# Premarket Shortlist — 2026-11-25

**CONTEXT/PRIORITIZATION ONLY — NEVER A GATE.** Off-watchlist names are research-only. Every
candidate still requires fresh same-cycle data and the FULL current §5B/Bearish-Mirror-Gate/§20
gate before any trade, exactly as if this file didn't exist.

- Generated: 2026-11-25T14:08:38Z (UTC) / 2026-11-25 06:08:38 (America/Los_Angeles)
- Trigger: Premarket Preparation Scan (`trig_01FRC5Yt8UVcGH8GxcAURYXX`), read-only, no order authority
- `calls_made_this_cycle`: 1

## No shortlist this cycle — TradingView quota confirmed exhausted (Step 1 call attempted, not skipped)

Step 1's SPY freshness check (`get_ohlcv(symbol="AMEX:SPY", interval="5m", count=3)`) was
**actually attempted** this cycle, not inferred from the shared state file alone — it returned
`TOOL_QUOTA_EXCEEDED` ("You've reached your daily usage limit, and a 10-minute MCP cooldown has
been enabled"). This confirms live, not just logged, exhaustion for UTC date 2026-11-25. The
shared, cross-trigger TradingView call-budget state (`dev_scanner/data_budget.py`) already showed
`status: EXHAUSTED` going into this cycle (5 prior attempts today, first exhaustion recorded
~04:38Z by a crypto cycle, confirmed as recently as the 13:38Z crypto cycle ~30 minutes before
this scan fired) — this cycle's real test call corroborates that record rather than duplicating
work, and the result was recorded back to the shared state file.

Per this trigger's own Step 1 guidance, a `TOOL_QUOTA_EXCEEDED` result on the SPY check means
premarket data cannot be trusted or gathered this cycle — no watchlist batch (Step 2) or
screener calls (Step 3) were attempted, since both would hit the same exhausted quota with no
fallback (Kraken's fallback path is crypto-only; this equities premarket trigger has no
equivalent non-TradingView data source). **This is connector/quota exhaustion, not a market
holiday or a genuine stale/degraded read** — flagged explicitly since the `coverage_state` enum
only distinguishes "stale/holiday/outage" from "evaluated," neither of which cleanly describes a
confirmed-live quota block. No shortlist can be produced this cycle.

Call budget used: 1 of 10 (the SPY check itself). Normal coverage should resume once TradingView's
daily quota next allows a successful call — recent history (see trades_log.md) shows this can
mean a clean UTC-day reset or a re-exhaustion within the same day; this file does not assume which
until a cycle actually succeeds.

## Quiet names
N/A this cycle — no data gathered.
