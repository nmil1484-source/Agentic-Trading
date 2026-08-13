# Watchlist

Source: TradingView — https://www.tradingview.com/watchlists/190302653/
Imported: 2026-08-13

This is a **candidate ticker pool**, not a pre-approved trading list. Per `CLAUDE.md` Section 2
("Do not hard-code a ticker list"), every symbol below still requires independent, current LUC/FTA
verification and a verified catalyst before it can appear on a Trade Card. Inclusion here means
"eligible to be checked," not "eligible to be bought."

## Eligible candidate pool
(long common stocks / non-leveraged ETFs — matches Section 2 instrument rules)

TTD, ONDS, RKLB, AMD, TSLA, IREN, AMZN, SHOP, LMND, PATH, ARKG, NFLX, RGTI, AAPL, VRT, PLAB, HIMS,
GOOG, RUN, MU, RDW, ASTS, KTOS, AVA, STM, SPY, DUOL, PLTR, OSCR, QQQ, NVDA, OKLO, ZETA, HOOD, TEM,
AVAV, TSM, NOW, ORCL, PURR, BMNR, CVX, KEEL

**Note on CVX and KEEL:** added 2026-08-13 per explicit user instruction. Both confirmed as real,
tradable Robinhood equity instruments (CVX = Chevron Corporation; KEEL = Keel Infrastructure Corp.
Common Stock — not to be confused with KEEX, a 2x leveraged ETF on KEEL, which is excluded per
Section 2's no-leveraged-ETF rule). KEEL also appears in LUC's "Stock Watchlist" section
(Bitcoin Mining + AI Data Storage + HPC) without buy-zone thresholds, so it currently falls under
the non-LUC-covered fallback in Section 2 rather than a GREEN/WHITE/RED rating. Neither has been
verified yet — same as everything else in this pool, both still require full LUC/FTA verification
and a catalyst before appearing on a Trade Card.

**Note on PURR:** listed on the source watchlist as `NASDAQ:PURR`. Resolved 2026-08-13 as a real,
tradable Robinhood equity instrument (added successfully to the synced "TradingView Pool"
watchlist via Robinhood MCP) — the earlier concern about mislabeling did not hold up. Still
requires full LUC/FTA verification and a catalyst per Section 2 before it can appear on a Trade
Card, same as everything else in the pool.

## Excluded — instrument type not permitted (Section 2: no crypto, no leveraged/inverse ETFs)
- Crypto pairs: ETHUSD, SOL, XRPUSD, LINK, BTCUSD, BTC.D, PYRUSDC
- Leveraged ETFs: SOXL (3x semiconductors), UCO (2x crude oil)
- Futures/FX (not a stock or ETF, not a permitted instrument at all): GOLD, USOIL, SILVER, USDJPY, US10Y

## Excluded — user call
- BLOK (ETF, crypto/blockchain-themed)
- CPER (commodity-linked ETF — copper)
- BMOOF (OTC-listed)

These three are rule-permitted instrument types (stock/ETF) but were excluded at the user's
discretion rather than by rule. Revisit if priorities change.

**Note on BMNR:** equity, crypto-adjacent (Bitmine Immersion Technologies). Rule-permitted as a
long common stock; included per explicit user instruction despite the crypto-adjacent theme.
