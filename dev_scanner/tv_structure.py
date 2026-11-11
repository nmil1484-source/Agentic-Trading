"""
Reusable structure/indicator/sizing calculations for TRADING_VIEW_2-sourced OHLCV bars.

This module exists to close a real gap found 2026-11-11: trigger prompts for the
First Scan, Fresh Candle, and Crypto 24/7 routines repeatedly reference a
"tv_structure.py" module (completed_bars/ema/rsi14/macd/atr14/volume_baseline_13h/
swing_points/pullback_depth/atr_target/risk_reward/validate_stop_distance/
position_size) as already "built and live-verified." No such file existed anywhere
in this repository, its git history, or any scratchpad before this commit — every
cycle this session actually computed stops/R:R/ATR by hand, inline, per name, via
ad-hoc Python. This module is the real implementation those trigger prompts
describe, built and tested now so future cycles can call one reviewed,
version-controlled function set instead of re-deriving the arithmetic each time.

Pure functions only: no network calls, no broker access, no file I/O, no order
placement. It only computes numbers from bars already fetched elsewhere.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence

REGULAR_SESSION_SECONDS = 23400  # 6.5h, 9:30am-4:00pm ET


@dataclass(frozen=True)
class Bar:
    t: int
    o: float
    h: float
    l: float
    c: float
    v: float = 0.0


def _as_bars(bars: Sequence[dict]) -> List[Bar]:
    return [Bar(t=b["t"], o=b["o"], h=b["h"], l=b["l"], c=b["c"], v=b.get("v", 0.0)) for b in bars]


def completed_bars(
    bars: Sequence[dict],
    interval_seconds: int,
    now_epoch: float,
    last_bar_duration_seconds: Optional[int] = None,
) -> List[Bar]:
    """
    Drop any bar that has not actually finished as of now_epoch.

    A bar at time t has finished once t + interval_seconds <= now_epoch, EXCEPT
    the single most-recently-started bar, whose true completion event may differ
    from a flat interval (e.g. a daily equity bar completes at the regular
    session's close, ~23400s after a 9:30am ET open, not a full 24h later).
    last_bar_duration_seconds overrides the interval for that one most-recent bar
    only; every earlier bar already has a later bar after it and is judged by the
    flat interval_seconds rule regardless (that later bar's own existence proves
    the earlier one closed).
    """
    parsed = sorted(_as_bars(bars), key=lambda b: b.t)
    out: List[Bar] = []
    n = len(parsed)
    for i, b in enumerate(parsed):
        is_last = i == n - 1
        dur = last_bar_duration_seconds if (is_last and last_bar_duration_seconds is not None) else interval_seconds
        if b.t + dur <= now_epoch:
            out.append(b)
    return out


def ema(closes: Sequence[float], period: int) -> Optional[float]:
    if len(closes) < period:
        return None
    k = 2 / (period + 1)
    e = sum(closes[:period]) / period
    for c in closes[period:]:
        e = c * k + e * (1 - k)
    return e


def rsi14(closes: Sequence[float], period: int = 14) -> Optional[float]:
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def macd(closes: Sequence[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Optional[dict]:
    if len(closes) < slow + signal:
        return None
    macd_series = []
    for end in range(slow, len(closes) + 1):
        window = closes[:end]
        ef = ema(window, fast)
        es = ema(window, slow)
        if ef is None or es is None:
            continue
        macd_series.append(ef - es)
    if len(macd_series) < signal:
        return None
    signal_line = ema(macd_series, signal)
    if signal_line is None:
        return None
    return {"macd": macd_series[-1], "signal": signal_line, "hist": macd_series[-1] - signal_line}


def atr14(bars: Sequence[Bar], period: int = 14) -> Optional[float]:
    if len(bars) < period + 1:
        return None
    trs = []
    for i in range(1, len(bars)):
        h, l, pc = bars[i].h, bars[i].l, bars[i - 1].c
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    if len(trs) < period:
        return None
    return sum(trs[-period:]) / period


def volume_baseline_13h(bars: Sequence[Bar], as_of_index: int, lookback: int = 3) -> Optional[dict]:
    """
    §13.H: "normal" volume for the bar at as_of_index is the average volume of the
    `lookback` (default 3) most recently COMPLETED bars immediately preceding it,
    same timeframe, no lookahead. Returns {"baseline": float, "sample_size": int}
    with sample_size < lookback flagged explicitly when fewer prior bars exist
    (minimum 1); the name is kept for continuity with the trigger prompts' own
    existing field name, not a literal "13 hour" window.
    """
    if as_of_index <= 0:
        return None
    start = max(0, as_of_index - lookback)
    prior = bars[start:as_of_index]
    if not prior:
        return None
    return {"baseline": sum(b.v for b in prior) / len(prior), "sample_size": len(prior)}


def swing_points(bars: Sequence[Bar], as_of_index: int, lookback: int = 5) -> dict:
    """
    Symmetric 5-bar (default) fractal lookback over bars[:as_of_index+1]. Returns
    the highest high and lowest low within the trailing `lookback` completed bars
    up to and including as_of_index, plus whether the as_of_index bar's own close
    broke past that prior range (for the §13.G breakout-continuation path).
    as_of_index must be the CURRENT completed-bar index — never a later one (no
    backdating a pivot to before it was actually confirmable).
    """
    if as_of_index < 0 or as_of_index >= len(bars):
        raise ValueError("as_of_index out of range")
    window_start = max(0, as_of_index - lookback + 1)
    window = bars[window_start : as_of_index + 1]
    # prior_window excludes the current bar itself — a breakout is measured
    # against what came BEFORE this bar, never including this bar's own high/low.
    prior_window = bars[max(0, as_of_index - lookback) : as_of_index] or window[:-1] or window
    swing_high = max(b.h for b in window)
    swing_low = min(b.l for b in window)
    prior_high = max(b.h for b in prior_window)
    prior_low = min(b.l for b in prior_window)
    current_close = bars[as_of_index].c
    return {
        "swing_high": swing_high,
        "swing_low": swing_low,
        "current_above_prior_swing_high": current_close > prior_high,
        "current_below_prior_swing_low": current_close < prior_low,
        "prior_swing_high": prior_high,
        "prior_swing_low": prior_low,
    }


def pullback_depth(bars: Sequence[Bar], as_of_index: int, lookback: int = 5) -> Optional[dict]:
    """
    Detects a pullback-to-swing structure (NOT breakout/retest or range
    contraction — those are checked separately via swing_points). Returns None
    when no clean impulse-then-pullback leg is identifiable in the lookback
    window; callers must not treat None as proof no other permitted entry method
    exists (per §13.G/the 2026-11-11 correction) — check swing_points() for a
    breakout/retest read before concluding "no computable entry."
    """
    if as_of_index < lookback:
        return None
    window = bars[as_of_index - lookback + 1 : as_of_index + 1]
    impulse_high = max(b.h for b in window[:-1]) if len(window) > 1 else None
    impulse_low = min(b.l for b in window[:-1]) if len(window) > 1 else None
    current = window[-1]
    if impulse_high is None or impulse_low is None or impulse_high == impulse_low:
        return None
    depth_from_high = (impulse_high - current.l) / (impulse_high - impulse_low) if impulse_high != impulse_low else None
    if depth_from_high is None or not (0 < depth_from_high < 1):
        return None
    return {
        "impulse_high": impulse_high,
        "impulse_low": impulse_low,
        "pullback_low": current.l,
        "depth_pct": depth_from_high * 100,
    }


def atr_target(entry: float, atr_value: float, direction: str, multiple: float = 1.5) -> float:
    """§13.F ATR_TARGET: entry +/- multiple*ATR, used when no real structural target exists."""
    if direction not in ("long", "short"):
        raise ValueError("direction must be 'long' or 'short'")
    return entry + multiple * atr_value if direction == "long" else entry - multiple * atr_value


def risk_reward(entry: float, stop: float, target: float, direction: str) -> Optional[float]:
    if direction == "long":
        risk = entry - stop
        reward = target - entry
    elif direction == "short":
        risk = stop - entry
        reward = entry - target
    else:
        raise ValueError("direction must be 'long' or 'short'")
    if risk <= 0:
        return None
    return reward / risk


def validate_stop_distance(entry: float, stop: float, atr_value: float, ceiling_multiple: float) -> dict:
    """
    Two independent checks, never merged into one:
    - exceeds_ceiling: the stop is genuinely too wide for the given ceiling_multiple
      of ATR (or ceiling_multiple itself can already be a flat %-of-entry when the
      caller passes atr_value as a flat distance basis instead) — a hard reject.
    - needs_structural_justification: the stop sits closer than 0.5x ATR to entry —
      a FLAG only, never an auto-reject, never a reason to widen the stop.
    """
    distance = abs(entry - stop)
    ceiling = ceiling_multiple * atr_value
    return {
        "distance": distance,
        "distance_pct_of_entry": distance / entry * 100 if entry else None,
        "ceiling": ceiling,
        "exceeds_ceiling": distance > ceiling,
        "needs_structural_justification": distance < 0.5 * atr_value,
    }


def position_size(risk_dollars: float, entry: float, stop: float, direction: str) -> Optional[float]:
    """
    Refuses (returns None) on a backwards stop rather than sizing via abs() — the
    2026-11-xx §20 item 2 bug fix this mirrors: a stop on the wrong side of entry
    must NO_TRADE, never silently size as if it were valid.
    """
    if direction == "long":
        if not (0 < stop < entry):
            return None
        stop_distance = entry - stop
    elif direction == "short":
        if not (stop > entry > 0):
            return None
        stop_distance = stop - entry
    else:
        raise ValueError("direction must be 'long' or 'short'")
    if stop_distance <= 0:
        return None
    return risk_dollars / stop_distance
