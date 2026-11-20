# Premarket Shortlist — 2026-11-20

**CONTEXT/PRIORITIZATION ONLY — NEVER A GATE.** Off-watchlist names are research-only. Every
candidate still requires fresh same-cycle data and the FULL current §5B/Bearish-Mirror-Gate/§20
gate before any trade, exactly as if this file didn't exist.

- Generated: 2026-11-20T14:08:35Z (UTC) / 2026-11-20 06:08:35 (America/Los_Angeles)
- Trigger: Premarket Preparation Scan (`trig_01FRC5Yt8UVcGH8GxcAURYXX`), read-only, no order authority
- `calls_made_this_cycle`: 0

## No shortlist this cycle — TradingView quota exhausted for the day (already re-exhausted after this morning's reset)

This cycle's SPY freshness check (Step 1) was **not attempted**. The shared, cross-trigger
TradingView call-budget state (`dev_scanner/data_budget.py`) shows `status: EXHAUSTED` for UTC
date 2026-11-20 — `attempts: 3`, `exhausted_at`/`last_success_at` both already logged by earlier
crypto cycles today. **Unlike yesterday's instance of this note, today's quota did reset cleanly
at the 2026-11-20T00:00Z UTC boundary** — the 00:38:00Z Crypto 24/7 cycle ran a full 17-call
TradingView pass successfully with zero issues — but the daily allowance was then consumed again
within about an hour (the 01:37:57Z cycle re-exhausted it after only ~4 more calls), and it has
stayed exhausted through every subsequent hourly crypto cycle since, confirmed as recently as the
13:37:49Z crypto cycle, ~30 minutes before this scan fired.

Attempting the SPY check or the watchlist/screener batch calls this cycle would only return
`TOOL_QUOTA_EXCEEDED` — the same connector degradation this trigger's own Step 1 instructs to
treat as a stale/degraded read, not a real data point. Rather than spend a call to re-confirm an
already-known-dead quota (same discipline applied yesterday and by the Crypto 24/7 trigger's own
protocol against this identical shared quota), this cycle skipped straight to reporting the gap.

**This is a connector/quota exhaustion, not a market holiday** — flagged explicitly since the
`coverage_state` enum only distinguishes "stale/holiday/outage" from "evaluated." No watchlist
or screener data was pulled this cycle; no shortlist can be produced. Normal coverage should
resume once TradingView's daily quota next resets — though today's own reset-then-immediate-
re-exhaustion pattern shows a bare UTC-day reset is not, by itself, a reliable guarantee of
usable headroom; this is worth a look if the pattern repeats on subsequent days.

## Quiet names
N/A this cycle — no data gathered.
