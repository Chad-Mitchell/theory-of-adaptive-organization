# MATCH1 predictions: does memory's decay exponent match need's, in the same system?

Written Sat 2026-11-14 ~22:58 ET, BEFORE computing any outcome below. Hashed + committed first.

## Disclosures (seen before writing)
- COLLAPSE1 results: code need exponents numpy/django/rails = 0.65/0.59/0.65 (commits >100 files
  removed), 0.61/0.37/0.63 unfiltered. Those 3 repos are IN-SAMPLE; the new repos are out of sample.
- Anderson & Schooler 1991 need exponents 0.73 (NYT), 0.77 (CHILDES), 0.83 (email); Saha 2025
  antibody m 0.36-0.43; Amanna measles half-life 3014 y.
- Data structures inspected (column names, first ~30 raw rows only, no aggregates): Meeter, Murre &
  Janssen 2005 retention data (neuromod.org data.zip: Q_ID, Q_TYPE, SESS_ID, SCORE, Q_AGE days);
  Antia 2018 S1 Data (FigS1_data: indiv, age, titer, infection). ABC "million news headlines"
  dataset exists on HuggingFace (not yet downloaded).
- Candia 2019 raw data are NOT public (on request only); replaced by an OpenAlex reference-age curve.
- Steering note from the literature map: T1/T1b and Lee, Flack & Krakauer 2024 give memory ∝ tau_E^(1/2)
  for single-timescale worlds; a scale-invariant (power-law) memory gives slope 1. My COLLAPSE1
  digitization of Wark 2009 already gave 0.53/0.76 (luminance) and 1.87 (contrast): seen, post hoc.

## Common method: Anderson-Schooler need odds
For an item stream (word in headlines / file in commits / Wikipedia page in edits): for each item
and day d, "needed" = item occurs on day d; lag L = days since its previous occurrence. Need odds
at L = needed/(at risk - needed). Fit log odds vs log L (power) and vs L (exponential) by
count-weighted least squares on lags 1..Lmax. Exponent a = -slope.
Memory exponent: recall odds p/(1-p) vs retention interval, same fit.

## M-A. News: need (headlines) vs human memory of news (same system, same odds scale)
- Need: ABC News headlines (English, HuggingFace DeveloperOats/Million_News_Headlines). Tokens:
  lowercase alphabetic, length ≥ 3, minus a fixed English stopword list; words with ≥ 20
  occurrences. Primary window 2003-2006 (overlaps the Meeter questions), Lmax = 730 d.
  Secondary: full corpus, Lmax = 730.
- Memory: Meeter et al. data, each experiment file separately, each Q_TYPE separately; primary =
  Q_TYPE 0 pooled over experiments 1-2 (open recall assumed; if the paper says otherwise, the
  open-recall type is primary). Recall odds per retention-interval bin (log-spaced, ≥ 200 answers per
  bin), days 1..730.
- **A1 (match):** a_mem / a_need in [0.5, 2] SUPPORTS; strong if |a_mem - a_need| ≤ 0.15.
  **Fails if outside [0.5, 2]; kill if outside [1/3, 3].**
- **A2 (form):** power beats exponential for memory (lower weighted SSE). Kill if exponential wins.
- **A3 (redness, exploratory):** spectral exponent beta of daily word-count series (mean log-log
  periodogram slope, frequencies 1/730..1/2 per day, words with ≥ 200 occurrences). Reported with
  a_need and a_mem; no kill (the beta-to-exponent mapping is not yet derived).

## M-B. Measles: re-exposure need vs antibody memory (freeze-or-hold test)
- Need: pre-vaccine measles incidence series for English/Welsh towns if obtainable (tsiR package
  data, CRAN). Per town, "needed" = reported cases in a biweek above 0; A&S need odds vs biweeks
  since last nonzero biweek. Memory: Antia 2018 S1 measles titers vs time since infection,
  approximated as age - 5 y (assumption: childhood infection at ~5); power-law exponent from a
  mixed fit (per-individual intercepts, shared exponent).
- **B1:** freeze-or-hold predicts a frozen memory: m_mem / a_need < 0.5. Pure drift matching
  predicts ratio in [0.5, 2]. Whichever holds is reported; if the need data cannot be obtained, B is
  reported as not run.

## M-C. Layer count vs span (T7b)
Model: f(t) = sum_{k=1..K} A_k exp(-t/tau_k), tau_k = tau_1 r^(k-1), A_k ≥ 0 (NNLS), tau_1 and r on a
grid (r in 2..30). Curves: (1) news need odds; (2) code need odds pooled over repos, Lmax 3650 d;
(3) Wikipedia edit need odds; (4) Meeter recall odds; (5) OpenAlex reference-age curve (share of
references from age-a years, divided by the number of works published that year), a = 1..100 y;
(6) antibody viral titers vs age (descriptive only, < 1 decade).
Each curve is reduced to 10 log-spaced bins per decade (equal weight per bin, so data volume
cannot drive K). For spans of 1, 1.5, 2, 2.5, 3 decades (as available from each curve's start),
K* = smallest K with weighted RMS error in log10 f ≤ 0.02.
- **C1 (T7b):** K* increases with log span (Spearman > 0 and K* at the longest span > K* at the
  shortest) in ≥ 3 of the curves spanning ≥ 1.5 decades. **Kill if K* stays ≤ 2 at all spans in ≥ 3
  such curves** (finite-layer null, e.g. Candia's two stores).

## M-D. Code recurrence, 20+ repos across languages (out of sample)
Repos (blob-less clones): flask, requests, scikit-learn, pandas, react, vuejs/core, express,
TypeScript, golang/go, hugo, ripgrep, tokio, spring-framework, guava, redis, curl, git,
laravel/framework, symfony, pandoc, phoenix, Alamofire, jekyll (+ numpy, django, rails in-sample).
Primary: commits touching ≤ 100 files, no merges, Lmax 365. Secondary: unfiltered.
- **D1:** exponent in [0.5, 0.85] for ≥ 80% of out-of-sample repos. **Kill if < 50%.**
- **D2:** power beats exponential (lower SSE) in ≥ 90% of repos.
- **D3 (exploratory):** per-repo spectral exponent beta of the daily per-file edit series
  (averaged periodogram of files with ≥ 50 edit days); Spearman(beta, a_need) reported, predicted
  sign negative (redder → slower need decay), no kill.

## M-E. Wikipedia edits
Random main-namespace articles (API list=random) until 400 with ≥ 30 revisions; all revision
timestamps. Primary excludes users whose names end in "bot" (case-insensitive); secondary keeps
all. Need = page edited on day d; Lmax 365.
- **E1:** pooled exponent in [0.5, 0.85]. **Kill if outside [0.35, 1.0].**
- **E2:** power beats exponential.

## M-F. Retina 1/2 vs 1 (no new preregistrable data)
Wark 2009 stimuli switch with one period per condition (single-timescale world). T1/LFK 2024 predict
slope 1/2; scale-free memory predicts 1. Re-check Fairhall 2001 text/figures for stated values and
report alongside COLLAPSE1's digitized 0.53/0.76/1.87, labelled post hoc.

## Prior art to search and cite
Software re-edit power laws ("Anderson Schooler software", "file change recurrence power law",
"temporal locality code churn"); Lee, Flack & Krakauer 2024 Proc R Soc B 291:20241606; Shankar &
Howard 2013; Fusi, Drew & Abbott 2005; Benna & Fusi 2016; Meeter et al. 2005.
