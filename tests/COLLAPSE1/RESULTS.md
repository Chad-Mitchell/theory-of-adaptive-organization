# COLLAPSE1 results: does memory time track world time across substrates?

Saturday 2026-11-14 (ET). Predictions were locked before extraction: PREDICTIONS.md (commit 947aa59,
22:38 ET, sha256 c702bb44…942851), amendment 1 (0805cec, 22:39 ET, exponent-space test, written after
seeing one search snippet, before reading its numbers), amendment 2 (ef12ae2, 22:43 ET, code test,
before computing). Note: the "~22:50" and "~22:45" times written inside the amendment texts were
estimates; the commit times are the real ones. Every number below comes from a fetched source in
sources/ (see sources/INDEX.md) or from code in firm/ and code_need/. Chart: collapse.png.

## Bottom line
1. **The big lead is a change of variable, from timescales to exponents.** Antibody waning is a power
   law (exponent m ≈ 0.4; Saha et al. 2025, prior art). Under a power law, a measured "half-life" is
   about (age when measured) x 0.69/m, so it grows with WHEN you measure.
   - Panel (d): once that is accounted for, 5 of the 8 Amanna antigens (tetanus, diphtheria, VZV,
     vaccinia, rubella) fall on ONE power-law line, within a factor of 1.5.
   - BIO1's headline "immune failure" (tetanus 11 y vs viruses 50-200+ y) was therefore largely a
     measurement artifact, not evidence against rule 2.
   - Measles (39x above the line), mumps (7x) and EBV (148x) stay genuinely longer-lived. The
     ages used are approximate (Saha's "typically year 8 vs year 45"), and m was fit partly on the
     same data, so this is a consistency check, not an independent test.
   - The same artifact contaminates any cross-system plot of "memory time vs world time".
2. **New measurement (not found in a quick search; may be known):** in three large codebases
   (numpy, django, rails), the chance a file is edited again falls as a power law of the time since
   its last edit. Exponent 0.61 / 0.37 / 0.63 as preregistered. With commits touching more than 100
   files removed (post hoc), it is 0.65 / 0.59 / 0.65, with R² 0.98-0.99.
   - That sits close to Anderson & Schooler's need exponents for news headlines (0.73), speech to
     children (0.77) and email (0.83).
   - Hypothesis: "need" in human information environments decays as t^-(0.6 to 0.8) with no
     characteristic timescale. That is the condition under which THEOREMS T7b says layered memory
     should be geometric ("fractal"), and a geometric layer stack sums to power-law forgetting
     (Benna & Fusi 2016 show a compartment chain gives ~t^-1/2).
3. **The timescale collapse, as specified, is not diagnostic and did not separate the classes.**
   - Held systems do sit in a band near or below the diagonal (26 of 28 points). But proportional
     scaling (N1) predicts that too, and the systems found are ones someone studied because they
     matched (selection bias).
   - Within-system slopes did not sort by class. Class S/D slopes ran 0.51-1.87. The only class-C
     system (firm inventory) gave 0.86, not the predicted 1/2.
4. **What failed:**
   - the cue model for immune durability (A1, 62.5%, below the 65% kill line);
   - inventory buffering against demand volatility (C2, slope 0.00, killed);
   - the pure square-root inventory law (no industry's CI contains 0.5).

## Scorecard (locked criteria)
| ID | Prediction | Result | Verdict |
|---|---|---|---|
| A1 | Cue model: replicating or particulate antigen → half-life > 50 y; ≥80% correct supports, <65% kills | 8 scored out of sample: HPV plateau (LONG ✓), HAV ~55 y (LONG ✓, marginal: 17/42/105), HBV 7-9 y (✗), JEV 4.3 y (✗, window includes year 1), aP 508 d (✓), SARS-CoV-2 infection 140-364 d (✗), mRNA ~60 d (✓), IIV 410-424 d (✓). 5/8 = 62.5% | **KILLED as locked.** Caveat: 4 of the 8 come from windows under 2 years, which under a power law cannot discriminate. Extras, not scored: natural pertussis 221 d and LAIV 820-1111 d (replicating, yet short; LAIV is slower than IIV) |
| A2 | Drift-only Spearman ≤ −0.5 | Drift ≈ 0 for most scored antigens | **Not scored** (untestable) |
| A3 | Severity-only Spearman ≥ +0.5 | CFRs not fetched; half-lives confounded by measurement age | **Not scored** |
| A4 | SD of log10 half-life among >50 y antigens ≥ 0.7 (descriptive) | 0.91 (Amanna, in-sample) | Descriptive; mostly the measurement-age artifact plus 3 true outliers |
| B1 | ≥80% of held points with log10(mem/world) in [−2, 0.5] | 26/28 = 93% (flu 0.6 outside) | **Passes, non-diagnostic** (N1 predicts it too) |
| B2 | Class S/D slopes 0.7-1.3; a class-C slope in 0.35-0.65 with CI excluding 1 | Retina contrast 1.87 ✗; luminance whole-cell 0.53 ✗, on-cell 0.76 ✓; hummingbird medians 0.51/0.69/0.74, modes 0.93/1.00/1.00; yeast 1.65 (engineered strains); flu 0.92. Class C (inventory) 0.86, CI 0.84-0.88 | **Theory does not beat N1.** Class split neither confirmed nor killed (C slope excludes 1 but is far from 0.5). Median vs mode, and the panel choice, are post hoc |
| B3 | Frozen class unrelated to world time | No frozen system with a measured world timescale | **Not scored** |
| C1 | Median within-industry slope in [0.5, 0.9]; kill if ≥ 0.95 | 12 industries, 1,561 firms: median 0.87; pooled within-industry 0.86 [0.84, 0.88]; 0 of 12 CIs contain 0.5 | **Passes narrowly.** Sublinear, as in the known "inventory economies of scale" literature; not a square-root law |
| C2 | log(inventory/COGS) rises with COGS volatility | 0.00 [−0.10, 0.10], p = 0.99, n = 1,302 | **KILLED** (caveat: annual COGS volatility mixes growth with shocks) |
| E1 | Power law ≥ single exponential in long-horizon memory/need data; kill if ≥2 substrates clearly exponential | Antibodies (ΔAIC 64, 38 for tetanus/diphtheria), human retention (Rubin & Wenzel; A&S), environmental need (A&S), code (this test): power wins. Collective attention (Candia): biexponential wins over exponential/lognormal; power law not compared | **Passes, weak test** (a mixture of exponentials also beats a single one) |
| E2 | Within one system, memory and need exponents within 2x | No system with both measured on the same scale | **Not tested.** This is the decisive next test |
| E3 | Cross-substrate exponents reported; no universal value predicted | Need: 0.59-0.83 (0.37 for django before removing bulk commits). Antibody memory: 0.36-0.43 | Need exponents cluster (mild surprise) |
| E4 | Antibody exponents within 2x of each other (prior-art extraction) | 0.36-0.43 | ✓ (Saha 2025) |
| E5a | Code: power beats exponential and R² ≥ 0.9 in all 3 repos; kill if exponential wins in ≥2 | Power has the lower SSE in 3/3; R² 0.94 / 0.31 / 0.96 (django hurt by bulk commits: spikes at lags 9, 14 and 365) | **Partial pass** (2/3 meet R²); kill not triggered. Post hoc excluding commits with >100 files: R² 0.98 / 0.98 / 0.99 |
| E5b | Code exponent within ±0.15 of A&S 0.73 in all 3 (surprise flag) | Preregistered: 0.61 ✓, 0.37 ✗, 0.63 ✓. Post hoc: 0.65 / 0.59 / 0.65, all ✓ | Not met as preregistered; met post hoc |

## What is genuinely new vs prior art
- **Prior art, credited:**
  - power-law antibody waning and the measurement-time artifact (Saha et al. 2025);
  - memory tracks environmental need with power-law form (Anderson & Schooler 1991);
  - compartment chains give ~t^-1/2 forgetting (Benna & Fusi 2016; Fusi, Drew & Abbott 2005 cascade);
  - biexponential collective memory (Candia 2019);
  - adaptation time tracking switching period (Wark 2009; Fairhall 2001);
  - interval timing in hummingbirds (Henderson 2006);
  - sublinear inventory scaling (operations-management literature, not re-searched here).
- **Possibly new** (quick searches only, so treat as unconfirmed):
  - (a) the A&S need-odds analysis applied to code, giving a power law with exponent ~0.6, close to
    the news/speech/email values;
  - (b) using the measurement-age artifact to reinterpret BIO1. The cross-substrate point is that
    timescale-collapse plots are invalid for multi-scale memories, and exponents are the right
    collapse variable;
  - (c) linking the scale-free need statistics, the power-law memories, and THEOREMS T7b's
    condition for geometric layering into one testable chain.
- **Practical implication for the theory** (hypothesis, no change made): rule 2's "let it fade"
  should fade as a power law with m ~0.6-0.8, not exponentially, wherever need is scale-free.

## Decisive next tests (not run)
1. **E2 in one system:** measure the need exponent and the memory exponent on the same scale in the
   same substrate. Candidates:
   - Wikipedia: pageview re-access need vs article edit/revert "memory";
   - pathogen re-exposure intervals vs antibody m, e.g. measles inter-epidemic gaps in island
     populations;
   - software: file re-edit need vs how long developers' or tools' caches keep context;
   - a person's own notes: re-use need vs fade.
2. Fit power-law vs biexponential vs layered-chain models (log-time spacing as a free parameter) to
   Candia's data and to antibody data with the same code, to test T7b's geometric-layering prediction.
3. Scorecard rule for future collapse plots: use exponents, or timescales measured at a matched age.

## Files
- PREDICTIONS.md, PREDICTIONS_AMENDMENT1.md, PREDICTIONS_AMENDMENT2.md, PREDICTIONS.sha256
- collapse.png; plot.py; collapse_data.csv (timescale pairs, how each number was obtained)
- firm/ (fetch.py, sic.py, analyze.py, industry_slopes.csv, firm_panel.csv, summary.json, raw/)
- code_need/ (need.py, need_sens.py, *_needodds*.csv, primary_results.jsonl,
  sensitivity_maxfiles100.jsonl, repo_heads.txt)
- sources/ (INDEX.md plus local copies)
