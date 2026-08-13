# Trades & Autonomous Cycle Log

Append-only log for the Agentic Account (••••8058). Every autonomous Routine cycle (CLAUDE.md
§14) logs one entry here, whether or not it results in a trade. Manually-confirmed trades from
this chat should also be logged here at the time they're placed, for a single source of truth on
the 1/day and 3/week new-position caps (§3) and the daily/weekly realized-loss circuit breakers
(§6).

Format per entry:

```
## YYYY-MM-DD HH:MM UTC — [AUTONOMOUS | MANUAL]
- Tickers reviewed:
- Gate results (LUC/FTA/technical/catalyst):
- Outcome: OBSERVE (reason) | TRADE (ticker, qty, limit, stop, target, RR, source links)
- Account state after: equity, cash, open positions, today's/this week's new-position count
```

---

(No entries yet.)
