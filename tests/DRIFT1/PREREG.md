# DRIFT1 preregistration: is drift scale-free? (T7's condition, plan item 6)

Written Sat 2026-11-14 ~11:05 PM ET, before any NEW data was pulled. Already on the box and NOT yet examined for
rate distributions by this agent: C3 GitHub issues (`../C3/data/issues.jsonl`, commit counts in `screen.jsonl`)
and the Looper store journal. Analysis functions: `drift_stats.py` (committed with this file, checked on synthetic
log-uniform / lognormal / bimodal / narrow / power-law data and synthetic 1/f^beta count series before any real data).

## Why
T7b: optimal levels are geometric ("fractal") only if the rates of what a system tracks are spread scale-free
(no characteristic time). This test measures that condition per domain instead of assuming it.

## Domains, items and rates (scale label in brackets)
- PERSON  Looper store: item = atom id; rate = (versions - 1) / (last - first version time), atoms with >= 2 versions.
          Small n; descriptive only, verdict labelled "small n".
- PROJECT GitHub (C3 sample): item = repo; rate = issues opened per day over [first issue, pull end]; >= 5 issues.
          Second measure: 2021 commit count per repo from screen.jsonl (commits/year, > 0).
- KNOWLEDGE Wikipedia (en): item = random main-namespace article (list=random, target 3000); rate = revisions per day over
          [creation, pull time]; >= 5 revisions. Revisions capped at the 5000 most recent (rate from their window if capped).
- FIRM    SEC EDGAR: item = company (random 2000 CIKs from company_tickers.json); rate = filings per day over the
          window of the filings listed in the submissions JSON (recent block, up to ~1000); >= 5 filings.
- CITY    NYC 311 (Socrata erm2-nwe9): item = (complaint_type, community_board) for calendar 2025; rate = requests/day; >= 5.
Sensitivity (all domains): minimum-count thresholds 2 and 20 instead of 5.

## Per-domain decision rule on log10(rate) across items (rate_tests)
1. span = q95 - q05. If span < 2 decades -> NARROW.
2. Else BUNCHED if: dip test p < 0.01 AND the BIC-best Gaussian mixture (k=1..6) has k >= 2 AND two components of
   weight >= 0.10 are separated by Ashman D >= 2.
3. Else BROAD_PEAKED (one characteristic scale) if, over the central 90%, a quadratic log-density beats linear by
   dBIC > 10, has a vertex >= 0.5 decade inside both edges, and the fitted density falls >= 2x from vertex to each edge.
4. Else SCALE_FREE (log-uniform or power law over the central span).
T7's condition is met only by SCALE_FREE. BROAD_PEAKED means nested levels are useful but not evenly spaced
(denser near the characteristic scale); BUNCHED means a few natural levels set by the world; NARROW means one level.

## Time-series check (spectrum_tests), aggregate event counts per domain
PROJECT (hourly issue openings), KNOWLEDGE (hourly revisions of sampled articles), CITY (hourly 311 requests 2020-2025),
FIRM (daily filings of sampled firms). Calendar cycles (day, week, year; for FIRM also quarter, 2191.5 h) are removed by
phase-folded mean subtraction and their harmonics masked; they are astronomical/institutional, not evidence.
Fit only where binned power >= 3x the Poisson shot-noise floor. Verdict: SINGLE_POWER_LAW if a broken power law does
not win (dBIC <= 10 or slope change < 0.3); BROKEN_SCALE otherwise; "+PEAKS" if any non-calendar periodogram ordinate
exceeds its local median-based level at Bonferroni p = 0.001. Scale-free in time = SINGLE_POWER_LAW, no peaks, fit range
>= 2 decades of frequency; otherwise not shown scale-free (if fit range < 2 decades: INSUFFICIENT RANGE).

## Predictions (my priors, stated so they can be wrong)
- Q1: no domain will be cleanly SCALE_FREE by the rate rule; most will be BROAD_PEAKED (lognormal-like), because
  rates are products of many factors. Confidence low-moderate.
- Q2: spans will be >= 2 decades in PROJECT, KNOWLEDGE and CITY; FIRM may be NARROW (filing is regulated: 10-Q/10-K cadence).
- Q3: aggregate spectra will show 1/f^beta segments with beta in [0.3, 1.5] but often a break (BROKEN_SCALE).
Kill reading for the "fractal" claim: if no domain passes SCALE_FREE (rate rule) and none is SINGLE_POWER_LAW over >= 2 decades,
the fractal (geometric-levels) claim has no empirical support at these scales; nesting would then follow the world's
characteristic scales instead (T7: "the architecture inherits whatever scale structure the world has").

## Caveats fixed in advance
- Left truncation: requiring >= 5 events removes slow items and can create an artificial low-side peak (hence the
  sensitivity thresholds and the reported fraction excluded).
- Rate = events / window is a noisy estimate (sd ~ 0.43/sqrt(n) decades).
- "Change rate" is proxied by event rate (issue openings, edits, filings, requests), not the drift variance of a
  tracked quantity; T7 is stated in terms of natural review intervals, which these proxy.
