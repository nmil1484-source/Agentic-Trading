# Technical Analysis Playbook

Reference methodology for the FTA scorecard (CLAUDE.md Section 5) and for computing entries,
invalidation/stop levels, and targets on every trade. This is standard technical-analysis
methodology, not a proprietary FTA definition — if the FTA sources define any of these
differently, that definition wins; reconcile this file against FTA Research Hub when reachable.

## Fibonacci retracement

- Draw from the most recent significant swing low to swing high (uptrend context — this system
  only takes long positions).
- Standard levels: 23.6%, 38.2%, 50%, 61.8%, 78.6%.
- The 38.2%–61.8% band ("golden zone") is the primary pullback-entry area. A retracement past
  78.6% generally signals the prior swing has failed, not a deeper buy-the-dip opportunity.
- **Entry condition:** price pulls back into the golden zone, holds (does not close below the
  zone on a closing basis), and prints a bullish reversal signal (hammer, bullish engulfing, or
  similar) with volume confirmation on the bounce.
- **Invalidation/stop:** place just below the next fibonacci level down from the entry level, or
  below the most recent swing low, whichever is tighter and better matches actual chart
  structure. A daily close below that level invalidates the setup.
- **Do not enter** if price is still in free-fall through the golden zone with no reversal signal
  — that is a "catching a falling knife" situation, not a valid pullback entry.

## 9/20 EMA pullback

- In a confirmed uptrend (price above both EMAs, 9 EMA above 20 EMA), a pullback to either EMA
  that holds with a bullish reversal candle and rising volume is a valid continuation entry.
- **Invalidation/stop:** a daily close below the 20 EMA, or below the most recent swing low,
  whichever is tighter.
- A cross of the 9 EMA below the 20 EMA on rising volume is a trend-break signal — treat as
  invalidation for any position relying on this setup.

## Market structure: higher highs / higher lows (HH/HL)

- An uptrend is defined by a sequence of higher highs and higher lows. This is the baseline
  structural filter — do not treat a setup as bullish if the most recent swing broke this
  pattern (i.e., made a lower low).
- **Break of structure (BOS):** a lower low after a HH/HL sequence invalidates the uptrend
  thesis for any position sized against it — this should trigger the Section 6 circuit-breaker
  posture for that position (exit, don't average in).

## Consolidation / basing patterns

- A sideways range (support and resistance roughly flat) following a prior uptrend or after a
  downtrend has stabilized. Often precedes a breakout.
- **Entry condition:** a breakout above range resistance, on volume meaningfully above the
  recent average (not a low-volume drift through the level).
- **Invalidation/stop:** back below the breakout level, or below range support if entry was
  taken inside the range.
- A breakout on thin volume is a low-confidence signal — treat as inconclusive, not a green
  light on its own.

## Cup and handle

- A rounded consolidation ("cup") that retraces roughly a third to a half of the prior advance,
  followed by a smaller, shallower pullback near the prior high ("handle") — typically well
  under half the cup's depth.
- **Entry condition:** breakout above the handle's resistance (which sits near the cup's prior
  high), on rising volume.
- **Invalidation/stop:** back below the handle's low.
- A handle that retraces too deep (more than roughly half the cup's depth) weakens the pattern
  — treat it as a basing/consolidation setup instead, not a clean cup and handle.

## How this feeds the required trade fields

Every candidate that reaches a Trade Card / TRADE EXECUTED record must have, derived from the
applicable pattern(s) above:
- **Entry limit price** — at or near the confirmed reversal/breakout, not chased after an
  extended move.
- **Invalidation/stop level** — the tightest structurally valid level from whichever pattern(s)
  applied (fib level, EMA, swing low, range/handle low — take the nearest one that still makes
  structural sense, not an arbitrary percentage).
- **Reward-to-risk** — computed from entry to a reasonable target (prior swing high, next fib
  extension, or measured move for cup-and-handle) versus entry to the invalidation level.

A candidate with no clean invalidation level under this framework does not clear the research
gate — regardless of how compelling the catalyst is on its own (CLAUDE.md Section 9).
