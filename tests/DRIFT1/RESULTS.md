# DRIFT1 results: is drift scale-free? (T7's condition)

Prereg: PREREG.md (sha256 a8880723..., git ecac666, 22:26 ET, before any new data). Code: drift_stats.py (prereg'd),
analyze.py (main), supp.py (post hoc, see DEVIATIONS.md). Raw outputs: analysis_output.txt, results.json,
supp_output.txt, supp_results.json. Data pulled Sat 2026-11-14 22:27-22:45 ET: 3,000 random en-Wikipedia articles (all
revision timestamps, 5,000 cap), 2,000 random SEC EDGAR filers from company_tickers.json (recent filings block), NYC 311
(Socrata) 2025 counts by complaint type x community board and hourly counts 2020-2025; plus C3 GitHub data. A person-scale arm was also run on a private journal; those results are withheld from this repository (see REDACTION.md).

## 1. Per-item rate distributions (T7b needs log-rates spread evenly over 2-3+ decades)

| Domain (scale) | items | prereg'd verdict | dequantized / post hoc | q05-q95 span (q01-q99) | shape |
|---|---|---|---|---|---|
| Person-scale arm | — | — | — | — | **Withheld.** A private personal journal was used; results and counts are not in this repository. See REDACTION.md. |
| Project: GitHub issues 2021 | 2,019 | NARROW (min2: BROAD_PEAKED, min20: NARROW) | NARROW, dip p=0.99 | 1.8 (2.5) | piles up at the 5-per-year detection floor, then falls steadily (log-density slope -0.33 per decade): truncated, right tail power-law-like |
| Project: GitHub commits 2021 (frame) | 8,714 (87% excluded, <5 commits) | NARROW (min2: BUNCHED) | NARROW, dip p=1.0 | 1.8 (2.4) | same: floor-truncated, falling tail (slope -0.40) |
| Knowledge: Wikipedia edits | 2,881 | NARROW | same (last-5y: NARROW, 1.3) | 1.6 (2.4) | one clear peak, about one edit per 160 days, well above the floor: **a characteristic rate** |
| Firm: EDGAR filings | 1,867 | NARROW (min2: SCALE_FREE) | same | 1.5 (2.6) | sharp peak near one filing per ~6 days, long slow tail: regulated cadence |
| City: 311 type x board | 7,545 | BUNCHED (quantization artifact) | **SCALE_FREE**, dip p=0.95 | 2.5 (3.2) | flat plateau from ~1 per 60 days to ~1 per day (slope -0.11), then falls |
| City: 311 complaint types (post hoc) | 185 | n/a | SCALE_FREE, dip p=0.72 | 3.8 (4.8) | nearly log-uniform across ~4 decades (slope +0.09); small n |

## 2. Aggregate timing spectra (calendar cycles removed)

| Domain | verdict by rule | slope(s) | fit range | flagged peaks |
|---|---|---|---|---|
| GitHub issues, hourly, 2021 | SINGLE_POWER_LAW but **INSUFFICIENT RANGE** | -0.25 | 1.6 decades | none |
| Wikipedia edits, hourly, 2016-2025 | SINGLE_POWER_LAW+PEAKS | -0.34 | 3.6 decades | one at 7.8 h: not a calendar harmonic (possibly a bot schedule; not checked) |
| EDGAR filings, daily, 2016-2025 | BROKEN_SCALE+PEAKS | -1.62 below / +0.67 above a break near 107 days | 2.7 decades | 8, all within 1 cycle/yr of weekly or quarterly harmonics (calendar leakage) |
| NYC 311, hourly, 2020-2025 | BROKEN_SCALE+PEAKS | -0.48 below / -1.49 above a break near 22 h | 3.5 decades | 6, all calendar harmonics or their seasonal sidebands (leakage, not new scales) |

## 3. Verdicts per domain (plain words)
- **City (NYC 311): yes, mostly scale-free across items.** Request rates per category spread evenly on a log scale over
  about 2.5 decades (4 decades for complaint types). That is T7's condition. In time, though, the city series has a break near one day, so it is not scale-free in time.
- **Knowledge (Wikipedia): no across items, yes-ish in time.** Articles have a characteristic edit rate (a single peak,
  90% within 1.6 decades). The aggregate edit stream is a single 1/f^0.34 power law over 3.6 decades. The one flagged
  peak (7.8 h) is not calendar.
- **Projects (GitHub): not shown.** Within a one-year window the measurable range is too short (floor at 5 events per year).
  What is visible is a steadily falling, power-law-like tail with no interior peak. That is compatible with scale-free but truncated. The rule says NARROW.
- **Firms (EDGAR): no.** Filing rates bunch at one regulated cadence, and the timing spectrum is broken, with quarterly and weekly structure.
- **Person-scale arm: withheld** from this repository (private journal). The public-domain verdicts below do not depend on it.

## 4. Predictions scored
- Q1 (no domain cleanly SCALE_FREE; most BROAD_PEAKED): **wrong in part.** 311 is SCALE_FREE (after dequantization).
  Most others are NARROW, not BROAD_PEAKED.
- Q2 (span >= 2 in projects, knowledge and city; firms maybe narrow): right for city and firms, **wrong** for projects and knowledge.
- Q3 (spectral beta in [0.3, 1.5], often broken): 311 broken (0.48 / 1.49), Wikipedia single 0.34, GitHub 0.25 (outside the band, short
  range), EDGAR broken with a positive high-frequency slope. Mixed.
- Kill reading: not triggered. One domain passes the rate rule (311), and one passes the time rule apart from a single non-calendar peak (Wikipedia).
  But **no domain passes both**, and the two domains with the most institutional structure (firms, Wikipedia items) show characteristic scales.

## 5. What this means for T7 ("fractal levels")
T7 said the optimal architecture inherits the world's scale structure, and the data say that structure differs by domain.
The fractal / geometric-levels claim has support for city service categories, and none for firm filings or for
Wikipedia articles' edit rates. Those have characteristic scales, so nesting there should follow the world's natural
cadences, not an even geometric ladder. This is evidence for T7's conditional statement, and against an unconditional "fractal at every scale".

## 6. Caveats
- Event rate (edits, filings, requests, issues) is a proxy for drift. T7 is about the natural review interval of
  what is tracked, and these proxy it.
- The count floor truncates the slow end (GitHub especially). One-year windows cap the measurable span near 2.5 decades.
- Sampling frames: GitHub is C3's sample (repos with >= 12 commits in 2021) or the Valiev package frame; EDGAR is
  currently listed tickers only (survivorship); 311 is one city and one year, with 'Unspecified' boards included.
- Dequantization (post hoc) changes the 311 verdict from BUNCHED to SCALE_FREE; the histogram shows a plateau, so
  I read BUNCHED as an artifact. A second reader should check this.
- One author; no blind review yet.
