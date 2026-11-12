# Premarket Shortlist — 2026-11-12

**CONTEXT/PRIORITIZATION ONLY — NEVER A GATE.** Off-watchlist names are research-only. Every
candidate still requires fresh same-cycle data and the FULL current §5B/Bearish-Mirror-Gate/§20
gate before any trade, exactly as if this file didn't exist. This file is overwritten each
weekday premarket cycle by the read-only Premarket Preparation Scan trigger (`trig_01FRC5Yt8UVcGH8GxcAURYXX`)
— it places no order, modifies no position, and grants no authority of any kind.

**Cycle**: 2026-11-12T14:11:25Z UTC / 2026-11-12 06:11:25 America/Los_Angeles (6:00am PT fire,
~4 min scheduler delay).

**SPY freshness basis**: The documented check (`get_ohlcv(AMEX:SPY, interval="5m", count=3)`)
returned a bar ~17.3 hours stale (last bar 2026-11-11 20:55 UTC, carrying the "regular session
only" notice this tool attaches to every response) — that tool does not serve premarket 5m bars
at all, as a structural/documented limitation, not a sign of a holiday or outage today. Corroborated
directly instead via the Step 2 watchlist batch pull itself: every name returned real, non-null,
non-zero `premarket_volume` and `premarket_change` figures with `update_mode: "streaming"` (e.g.
SPY premarket_volume 1,479,725, NVDA 48,384,161) — this is genuinely live premarket data this
cycle, not stale. Logged as `coverage_state: "EVALUATED"`, not `DATA_STALE_LIKELY_HOLIDAY_OR_OUTAGE`,
on this corroborating basis.

**Liquidity floor used**: `volume: [500000, null]` (today's running regular-session volume) for
the Step 3 off-watchlist screener. At this floor the "liquid movers" screener returned almost
entirely penny stocks and leveraged single-stock NVDA ETNs (NVDL/NVDS/NVDU/NVDX/NVDG/NVDQ/NVD) —
none of these are genuine quality candidates; none were advanced to the shortlist below. The
watchlist pool itself (Step 2) provided a far higher-quality candidate set given today's dominant
catalyst (see below), so the final shortlist is drawn entirely from on-watchlist names.

## Dominant catalyst this cycle, found via Step 5 — flagged prominently

**Nvidia CEO Jensen Huang has resigned (WSJ-reported, Dow Jones Newswires, published ~2026-11-12
~17:17 UTC equivalent per headline timestamps).** This is a major, verified, same-day catalyst
driving NVDA itself sharply lower premarket and appears to be the dominant driver behind a broad
AI/semiconductor/datacenter-infrastructure selloff this morning (NBIS, CRWV, DELL, IREN all moving
sharply, several explicitly tied back to NVDA-related concern in their own headlines). This also
lines up with the broad crypto market-wide decline observed across the parallel Crypto 24/7
trigger's last several hourly cycles today — consistent with one shared macro/AI-sector shock
rather than unrelated coincidences.

## Shortlist (top 5 by |premarket_change|, liquidity-floor-cleared)

| Ticker | Watchlist status | Premarket % chg | Premarket volume | Catalyst | Prior regular-session close |
|---|---|---|---|---|---|
| NBIS | On-watchlist | **-19.45%** | 10,257,322 | **Verified**: "Nebius Lowers Fiscal Year Outlook, Addresses Worries Over Financing AI Buildout" (Dow Jones) + "Nebius Stock Falls as Capacity Delays Push Revenue Into 2027" (GuruFocus) — Q3 earnings-driven guidance cut, capacity/financing concerns | $154.69 |
| CRWV | On-watchlist | **-13.63%** | 8,768,082 | **Verified**: "CoreWeave Price Target Cut to $100 from $150 by Argus Research"; "Why CoreWeave Stock Is in the Nvidia Danger Zone" (Barron's); 3Q26 10-Q showed revenue $3.66B, EPS -$1.27 — earnings/guidance-driven, explicitly linked to NVDA concerns | $60.77 |
| NVDA | On-watchlist | **-11.51%** | 48,384,161 | **Verified**: Jensen Huang (CEO) resignation (WSJ/Dow Jones) — the dominant catalyst of the morning, see above | $173.73 |
| IREN | On-watchlist | **-8.40%** | 4,729,018 | **Unverified for today specifically** — most recent headlines found (top 5) are dated Nov 9-11 (JPMorgan price-target cut to $55, ARR-target-slip rating cut, a bullish neocloud-sector piece from Nov 11) — no distinct same-day IREN catalyst found; most likely swept up in the broader NVDA/AI-infra selloff rather than its own news | $20.84 |
| DELL | On-watchlist | **-7.89%** | 218,883 (premarket); 9,306,208 (regular session, clears liquidity floor) | **Unverified for a negative catalyst** — most recent headlines are from Nov 11 and explicitly *bullish* ("Dell Stocks Jump 11.42% as CoreWeave's Bigger Spending Plan Revives AI Server Bets") — today's premarket decline reads as giving back yesterday's AI-server-spending rally amid the broader NVDA-driven risk-off, not a fresh negative DELL-specific catalyst | $373.68 |

## Other notable watchlist premarket moves this cycle (not in the top-5 shortlist, logged for context)

BE -6.74%, BMNR -6.70%, KEEL -6.76%, HIMS -5.72%, MU -5.69%, TEM -5.39%, CORZ -5.28%, ASTS -5.02%,
OKLO -5.56%, HOOD -4.81%, ORCL -4.74%, TSM -4.58%, VRT -4.98%, HPE -4.48%, INTC -4.83%, CRCL -4.92%,
PURR -7.10% — broad-based red across almost the entire watchlist this morning, consistent with the
single dominant NVDA/AI-infrastructure shock above rather than many independent stories.
