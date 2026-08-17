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
AVAV, TSM, NOW, ORCL, PURR, BMNR, CVX, KEEL, DRAM, DELL, UBER, HPE, NBIS, CRWV, ZS, SOFI, FIG, GDX,
IGV, CRCL, CBRS

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

**Note on DRAM, DELL, UBER, HPE, NBIS, CRWV, ZS, SOFI, FIG:** added 2026-08-14 per explicit user
instruction, sourced from an investment-group market call the user shared as context (per §9,
used only as a starting pool — never a signal; every name here still needs its own independent
§5B verification same as everything else). All nine confirmed as real, tradable Robinhood
instruments via `search`:
- **DRAM** = Roundhill Memory ETF (non-leveraged, rule-permitted). Not to be confused with **RAM**
  (Roundhill T-REX 2X Long DRAM Daily Target ETF) or **RAML** (Leverage Shares 2X Long Memory
  Daily ETF) — both leveraged, both excluded per Section 2.
- **DELL** = Dell Technologies Inc. common stock. Not **DLLL** (2x leveraged), excluded.
- **UBER** = Uber Technologies, Inc. common stock. Not **UBEW** or **UBRL** (leveraged/derivative
  products on UBER), excluded.
- **HPE** = Hewlett Packard Enterprise Company common stock. Not **HPEL** (2x leveraged), excluded.
- **NBIS** = Nebius Group N.V. Class A common stock. Not **NEBX/NBIL/NBIZ/NBIG/NBIC** (all
  leveraged or inverse ETFs on NBIS), excluded.
- **CRWV** = CoreWeave, Inc. Class A common stock. The source material referred to this as "CORE"
  informally — CoreWeave's actual ticker is CRWV, not a literal "CORE" symbol. Not
  **CRWG/CORD/CRWU/CWVX/CRWX/CWY** (all leveraged, inverse, or derivative-income ETFs on CRWV),
  excluded.
- **ZS** = Zscaler, Inc. common stock. Single unambiguous match.
- **SOFI** = SoFi Technologies, Inc. common stock. Not **SOFX/SOFA/SOFC** (all 2x leveraged ETFs
  on SOFI), excluded.
- **FIG** = Figma, Inc. common stock. Not **FIGG** (2x leveraged), excluded.

None of these nine have been verified yet — same as everything else in this pool, all still
require full §5B (or §5A, for Mode A) verification and a catalyst before appearing on a Trade
Card. Two other ideas from the same source material — an IAU LEAPS call option and a CVX call
option — were excluded outright and never considered for this list, since §2 prohibits options
entirely regardless of setup quality.

**Note on GDX, IGV, CRCL, CBRS:** added 2026-08-17 per explicit user instruction, sourced from an
investment-group market call the user shared as context (per §9, context only — never a signal;
each still needs its own independent §5B verification). Confirmed via `search`:
- **GDX** = VanEck Gold Miners ETF (non-leveraged). Not **GDXU** (3x leveraged) or **GDXD** (3x
  inverse), excluded.
- **IGV** = iShares Expanded Tech-Software Sector ETF (non-leveraged). Single unambiguous match.
- **CRCL** = Circle Internet Group, Inc. common stock ("Circle" in the call notes). Single
  unambiguous match.
- **CBRS** = Cerebras Systems Inc. Class A common stock ("Cerebris" in the call notes — resolved
  to Cerebras). Not **CBRG/CBRX/CBRZ** (all leveraged/inverse ETFs on CBRS), excluded.

**TBT excluded, not added:** ProShares UltraShort 20+ Year Treasury — a 2x inverse ETF, prohibited
by §2.

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
