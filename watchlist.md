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
AVAV, TSM, NOW, ORCL, PURR, BMNR

**Note on PURR:** listed on the source watchlist as `NASDAQ:PURR`. This could not be independently
verified as a real Nasdaq-listed equity as of import — it may be mislabeled (e.g. a crypto token
ticker). Included per explicit user instruction. Before any proposal, confirm it resolves to a
real, tradable Robinhood equity via `get_equity_tradability` / `search` — if it doesn't, treat it
as invalid and drop it, don't guess.

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
