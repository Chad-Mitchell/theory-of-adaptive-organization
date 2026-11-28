# MATCH1 results: does memory's decay exponent match need's, in the same system?

Sat 2026-11-14 (ET). Predictions: PREDICTIONS.md, commit 71d8306 (22:55 ET), sha256 43a07776…217cc5,
committed before any outcome was computed. The "~22:58" time written inside the file was an
estimate; the commit time is the real one. Everything below comes from fetched data (sources/,
per-test folders) and the scripts beside them. Chart: match.png.

## Bottom line
1. **The exact match fails.** In the one system where both could be measured on the same odds
   scale (English-language news), need decays about 3x faster than memory.
   - Need: words recurring in ABC headlines decay with exponent **0.71** (2003-06) and 0.78
     (2003-21). This replicates Anderson & Schooler's 0.73 for the NYT.
   - Memory: people's recall of news events (Meeter et al. 2005, about 111,000 open-recall answers)
     decays with exponent **0.24** (4-choice: 0.18; English speakers only: 0.14).
   - The ratio of 0.34 is outside the preregistered [0.5, 2] support band, so the test **fails**. It
     sits just inside the [1/3, 3] kill band (0.336), so it is not formally killed. On the full
     headline corpus the ratio is 0.31, which would be a kill.
   - What survives: memory is a power law, beating an exponential in all 12 subsets. The power-law
     form carries over; the exponent does not. That is what Anderson's own 1990 model allows:
     recall odds = C x (need odds)^d, here with d ≈ 1/3. So "memory matches need" holds only in the
     weak form (same functional form, scaled exponent), which is prior art.
2. **Freeze-or-hold passes its preregistered test (measles).**
   - Need: English/Welsh towns 1944-65 (tsiR data). The odds of measles returning fall steeply with
     time since it was last present: exponent **2.15**.
   - Memory: measles antibodies in the Antia 2018 cohort decay with exponent **0.11** (CI 0.03-0.20).
   - Ratio 0.05, below the preregistered 0.5 cutoff for "frozen". The memory is decoupled from need.
   - Caveats: town-level presence is not individual exposure; time since infection was approximated
     as age − 5; only 39 lags were informative.
3. **The software need exponent replicates across 26 repos, plus Wikipedia (preregistered band
   0.5-0.85).**
   - 21 of 23 out-of-sample repos fall in band (91%); median 0.62, range 0.46 (Alamofire) to 0.92
     (TypeScript). Power beats exponential in 26 of 26.
   - Wikipedia (400 random articles, bots excluded): **0.66**.
   - Across news (0.71-0.78), code (median 0.62) and Wikipedia (0.66), "need" in human information
     environments sits in a narrow band, roughly 0.6-0.8.
4. **The layers-vs-span test (T7b) was inconclusive at the preregistered tolerance.**
   - At the locked 2% error target, only Wikipedia was fit cleanly, and its layer count rose with
     span: 2, 3, 4, 5, 5 over 1 to 3 decades. The other curves hit a noise floor of about 2%
     (weekly and yearly cycles), so no layer count could be read off. Neither support nor kill.
   - Post hoc, at a 3% target: code, news need and Wikipedia each rise from 2 to 4 layers as the
     span grows from 1 to 2.5-3 decades. Recall memory rises from 2 to 3. That is consistent with
     T7b and against a fixed two-store model (Candia), but it is not preregistered.
   - The antibody data cover only 0.5 decades, which is untestable. Candia's raw data are not
     public, so I used an OpenAlex reference-age curve instead. It never reached even a 3% fit.
5. **Redness came out the opposite way from my prediction.** Across repos, a redder per-file edit
   series goes with STEEPER need decay (Spearman +0.57, p = 0.002; I had predicted a negative
   sign). News word series are weakly red (beta 0.36); code files run from 0.12 to 0.35. The
   mapping from beta to exponent still has to be derived, not guessed.
6. **Retina, 1/2 vs 1 (post hoc check).**
   - Fairhall 2001 (fly H1) states that decay time "scales linearly with the switching period T"
     from 4 to 40 s. The phase lag is "a fixed fraction of the modulation period" from 10 to 240 s.
     That is a scale-invariant signature: slope 1, the scale-free branch, not T1's 1/2.
   - Wark 2009 retina, as I read it off the figures: luminance 0.53 (whole-cell) and 0.76 (on-cell),
     close to or between 1/2 and 1; contrast 1.87 (with a floor).
   - So "slope ~1" is solid for fly variance adaptation, but not robust across retinal measures.
     The literature-map reading (slope 1 points to the scale-free branch, T7, not T1) holds for
     Fairhall and is mixed for Wark.

## Scorecard (locked criteria)
| ID | Prediction | Result | Verdict |
|---|---|---|---|
| A1 | a_mem/a_need in [0.5, 2]; kill outside [1/3, 3] | 0.238/0.709 = 0.336 (English 0.20; full-corpus need gives 0.31) | **FAILS** (borderline kill) |
| A2 | Memory power beats exponential | 12/12 subsets (R² 0.84-0.96 vs 0.52-0.81) | **Supported** |
| A3 | Redness reported (exploratory) | beta = 0.36 (1,459 words) | Reported |
| B1 | Freeze: m_mem/a_need < 0.5 | 0.11/2.15 = 0.05 | **Supported** (with caveats) |
| C1 | K* rises with span in ≥3 curves; kill if K* ≤ 2 at all spans in ≥3 | At tol 0.02 only Wikipedia rises; others never reach tol | **Inconclusive**; consistent post hoc at 0.03 |
| D1 | ≥80% of out-of-sample repos in [0.5, 0.85]; kill < 50% | 21/23 = 91% (unfiltered: 78%) | **Supported** |
| D2 | Power beats exponential in ≥90% | 26/26 | **Supported** |
| D3 | Spearman(beta, a) negative (exploratory) | +0.57, p = 0.002 | **Opposite sign** |
| E1 | Wikipedia exponent in [0.5, 0.85]; kill outside [0.35, 1.0] | 0.66 (with bots: 0.62) | **Supported** |
| E2 | Power beats exponential | R² 0.98 vs 0.51 | **Supported** |
| F | Retina 1/2 vs 1 (post hoc) | Fly H1: ~1 (scale-invariant); retina: mixed 0.53-1.87 | Reported |

## Prior art (search results; cite)
- **Software:**
  - Challet & Lombardoni 2008: fat-tailed times between file modifications, long memory, and files
    "ageing" with a power-law-decaying modification rate (Mozilla, Apache, BSDs, PostgreSQL).
    https://folia.unifr.ch/unifr/documents/300597
  - Wu 2006 (Waterloo thesis): self-organized criticality and long-range correlations in change
    series.
  - Skeptical re-test of power laws in commit sizes: arXiv:1905.11044.
  - Schooler & Anderson 1997 explicitly link need probability to file access on computers.
  - Not found in a quick search: an Anderson & Schooler need-odds exponent measured for code, or
    compared across code, news and Wikipedia. The power-law recurrence itself is NOT new.
- **Memory:**
  - Anderson & Schooler 1991; Anderson 1990 (recall odds = C·n^d);
  - Meeter, Murre & Janssen 2005 (their own best fits were Weibull and two-store memory-chain
    models);
  - Fusi, Drew & Abbott 2005; Benna & Fusi 2016;
  - Shankar & Howard 2013, JMLR 14:3785: log-spaced memory is optimal for power-law-correlated
    signals.
- **Optimal memory scaling:** Lee, Flack & Krakauer 2024, Proc R Soc B 291:20241606: optimal memory
  τm* ∼ τE^{1/2}, the same 1/2 as T1. Cite as prior art for T1's scaling.

## What this means for the theory
- The strong claim "efficient memory's decay exponent equals the need exponent" is **false** where
  tested (news, human recall).
- The weak claim, "memory is a power law when need is a power law", survives but is old
  (Anderson & Schooler).
- Freeze-or-hold earned a preregistered pass (measles).
- The new empirical regularity is a narrow band of need exponents (about 0.6-0.8) across news,
  code and Wikipedia.
- The layer-count prediction of T7b needs a cleaner test: detrend the weekly and yearly cycles,
  and preregister the tolerance from the measured noise floor.

## Files
- PREDICTIONS.md, PREDICTIONS.sha256; aslib.py; plot.py; match.png
- news/ (need.py, need_results.json, needodds_*.csv; headlines CSV from HuggingFace
  DeveloperOats/Million_News_Headlines)
- memory/ (meeter.py, meeter_results.json, curve_*.csv)
- code/ (run.py, results.jsonl, per-repo need-odds CSVs)
- wiki/ (fetch.py, revisions.jsonl, run.py, results.json)
- measles/ (run.py, results.json, needodds.csv)
- layers/ (layerlib.py, run.py, results.json, diag.py, diag_tolerances.txt, curve_*.csv)
- openalex/ (fetch.py, ref_years.json, volume_by_year.json)
- sources/ (Antia 2018 S1 Data, Meeter 2005 data.zip, tsiR 0.4.3 data, prior-art pages)
