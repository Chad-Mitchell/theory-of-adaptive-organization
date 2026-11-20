# ECOLI-MEM F2 results: how E. coli's store noise scales with its memory

Friday 20 November 2026, Grok Bot executor for Chad Mitchell. Rule locked in `PREREG_F2.md` (`f18fdfd`) before any of
these data were read. Scripts: `f2/fetch_keegstra.py`, `f2/f2_score.py` (→ `f2/f2_results.json`),
`f2/rerun_measured_s.py` (→ `f2/rerun_results.json`). Self-checked, not independently reviewed.

## Verdict: **NEITHER arm** (s ≈ 0.3, between fixed variance and fixed density)
| Source | Observable, variation | n | τ range | s = d ln σ / d ln τ | Locked band |
|---|---|---|---|---|---|
| Park et al. 2010, Fig. 4c (digitized) | CheY-P variance vs correlation time; 9 CheR-induction / CW-bias conditions; a0 reported | 9 | 0.9–14.8 s | **0.31** (RMA; OLS 0.30 / 0.33), 95% CI 0.24–0.37 (bootstrap), 0.24–0.37 (digitization jitter) | neither |
| Keegstra et al. 2017, Fig. 4 source data | single-cell FRET kinase noise η_OU vs OU timescale, natural variation in wild type; a0 not in table | 70 | 7.3–29.7 s | 0.28 (OLS), CI −0.28 to 0.88; Theil–Sen 0.38; Spearman ρ 0.14, p 0.26 | neither |
| same, time-series amplitude η_TS | as above | 70 | 7.3–29.7 s | 0.06, CI −0.44 to 0.58 | arm C (CI spans both) |

Park outranks Keegstra under the locked caveat (it reports a0, as CW bias, per condition; Keegstra's per-cell table does
not), and it is the only source with a wide τ range (×17 against ×4). **Neither arm B (fixed density, s = ½) nor arm C
(fixed variance, s = 0) is supported**; the store's noise grows with its memory, but more slowly than fixed density.
The point estimate is in the gap; the CI touches both bands' edges (0.24 < 0.25; 0.37 > 0.35).

## Hostile notes on F2
- **Park's own fit hides this.** The paper fits a line through the origin (τ ≈ 257 s/µM² × variance, R² 0.9) and reads
  "D nearly constant", i.e. arm B. A free log-log slope over the same nine points gives Var ∝ τ^0.62, not τ^1. The linear
  fit's apparent support for arm B comes from the low-τ points (i, h, f) lying right of the line. I digitized by hand from
  a JPEG; jitter of ±0.001 and ±0.3 s does not move s out of 0.24–0.37. Error bars were not digitized; a weighted fit
  could differ.
- **Observable.** Park measures CheY-P noise inferred from motor switching, downstream of the kinase; Mattingly's σn is
  kinase activity (FRET). Keegstra is kinase-level but the τ range is narrow and the slope is undetermined.
- **Not a clean manipulation.** CheR induction changes a0 (CW bias 0.02–0.55 across a–i) together with τ. A source that
  varies τ at fixed a0 would outrank both. None found.
- **Keegstra exclusions.** 70 cells have finite OU fits in the source data against 75 in the paper's text; η_OU is built
  from the fitted τ (σ = √(cτ/2)), so its slope against τ shares fit error. η_TS uses a 10 s moving average that
  attenuates short-τ cells more (biasing s up). Both are reported; neither decides.
- **Other named sources (checked at abstract level, open copies only):** Emonet & Cluzel 2008 (doi
  10.1073/pnas.0705463105) is the model behind Park's coupling, no new data; Korobkova et al. 2004 (doi 10.1038/nature02404)
  reports noise rising with CheR changes but the abstract gives no amplitude-vs-τ numbers and no open full text was read;
  Dufour et al. 2014 (doi 10.1371/journal.pcbi.1003694) is theory; Dufour et al. 2016 (doi 10.1371/journal.pcbi.1005041)
  maps tumble bias to CheR/CheB numbers, not noise vs τ; Frankel et al. 2014 (doi 10.7554/eLife.03526) checked by Crossref
  metadata only. All DOIs resolve on Crossref (`../crossref_f2.out`).

## Rerun of the main test with the measured noise model (diagnostic; cannot change P1's locked verdict)
F2 selects neither locked arm, so the rerun uses the measured exponent: store-noise variance ∝ τ^{2s},
input-referred V0 (τ2/τ)^{2−2s}, every other input as locked (`f2/rerun_measured_s.py`).

| s | optimal memory over g = 0.1–0.4 mm⁻¹ | share of the optimum's explained variance captured at 9.9 s |
|---|---|---|
| 0.24 (CI low) | 3.32–3.58 s | 0.82–0.85 |
| **0.31 (point)** | **2.43–2.57 s** | **0.70–0.73** |
| 0.37 (CI high) | 1.86–1.95 s | 0.58–0.61 |
| ½ (locked arm B) | 1.11–1.16 s | 0.36–0.37 |

Locked thresholds applied for reference: at the point estimate **FAIL** (3U = 7.7 s < 9.3 s); over the CI **NEITHER**
(M = 9.3–10.5 s lies inside [L/3, 3U] = [0.62, 10.7] but outside [L/2, 2U]). Closed form λτ\* = (1−s)/s
(`theory/STORE_NOISE.md` E1-a) reproduces every optimum within 1%.

## Status in the required form
**ECOLI-MEM failed on this proxy/setup** (P1, locked: 1.1 s predicted, 9.9 s measured). **Diagnosed cause, part 1
(confirmed in direction, measured in size):** the store makes its own noise, and that noise grows more slowly than its
memory (s = 0.31), which moves the optimum from 1.1 s to about 2.5 s and closes 37% of the log gap; the measured memory
then captures about 72% of the best single store's explained variance instead of 37%. **Part 2 (open):** the remaining
factor of about 4. Candidates, ranked by evidence: speed-priced upkeep (E2; Lan et al. 2012 measured dissipation rising
with adaptation speed; E. coli would need H/W ≈ 0.7), the objective (drift or steady-state accumulation rather than
squared error on u), slow habitat modes absent in the lab, and the lab strain (selection condition). **Next tests:**
(Y1) a kinase-level noise-vs-τ measurement at fixed a0 to pin s; (Y2) estimate H/W from Lan's dissipation and Ni et al.'s
fitness stakes; (Y3) SN1 on new systems (`../PREREG_SN1.md`). The hypothesis is not refuted: no preregistered kill
condition is met after diagnosis and rerun.
