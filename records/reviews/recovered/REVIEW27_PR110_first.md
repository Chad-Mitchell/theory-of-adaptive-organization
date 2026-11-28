# Independent hostile review: GTAO PR #110 (branch v2.5-measure, head 99323e3, base main bc9a1ec)

Reviewer: outside referee; did not author. Fresh clone `/workspace/gtao-review27` at 99323e3. Nothing pushed. Run at nice 19.
Friday 20 Nov 2026 (ET). Scope: stats, preregistration discipline, physics/biology, prior art.

## VERDICT: READY-WITH-FIXES
The verdict labels follow the locked rules. No prediction was patched after the fact, and the arithmetic reproduces. The law
state in SYNTHESIS.md is mostly honest. Five items must change before merge: a banned word, one missed
directly-on-point paper, one false timing claim, two labels that break the repo's own rules, and one omission about what
the extension does to interlacing. None changes a verdict. Fixes are wording and a small CLAIM_MAP edit.

---
## 0. Mechanical checks
- `python3 -m pytest tools -q`: **73 passed** (116 s). Bare root `pytest` collects the whole archive and did not finish in 2.5 min, so "73" is the `tools/` suite.
- `python3 tools/check_consistency.py`: **RESULT: PASS** (FAIL 0, INFO 21).
- Raw data not in git: the PR diff has no zip/xlsx/parquet. The only new csv are `ecoli/f2/keegstra2017_fig4_percell.csv` and `park2010_fig4c_digitized.csv` (small, derived or digitized). OK.
- `ecoli/LOCK.txt` hashes match the blobs at 6903de9 (PREREG.md aab84ceb…, calc 818ede76…). `ecoli_calc.py` has since changed once (Riccati deviation, c402814), declared in DEVIATIONS.md.
- Added lines contain no "bill", "joule" or "theory of everything".

## 1. Preregistration order (commit times ET, `git log`)
| Lock (commit, time) | Analysis (commit, time) | Order | Notes |
|---|---|---|---|
| ECOLI PREREG+calc 6903de9 08:19:08 | run c402814 08:20:16 | OK | DEVIATIONS.md:3 says the first run was "8:22 AM", after the commit that holds its output (S-1) |
| F1 c402814 / F2 f18fdfd 08:23:03 | F2 scored 0d92c8b 09:05:02 | OK | No "Park"/"Keegstra" string in the tree at or before f18fdfd. The F2 bands were not set after seeing Park. |
| SN1 d99eade 08:59:07 | SN1 results 9f2426f 09:22 | OK | |
| D fc83d62 09:11:13, Y4 1db68db 09:15:11 | 9f2426f 09:22:24 | OK | PREREG_D discloses that its outcomes were anticipated on paper. Accurate. |
| GRID-1 4820d91 09:32:04 | DV1 6636517 09:49:18 | OK | Files downloaded 9:42–9:47. DV1 changes the data and arms after the download, before any statistic. Disclosed, and the changes make the test weaker, not stronger. |
| DV2 a769a1f 09:51:54, GRID-1b bef3b8c 09:52:57 | 1b results 36416d2 09:56:21 | OK | 1b "expected PASS" is disclosed in advance. Weak, low-risk arm. |
| GRID-S 8b0ef50 10:03:29 | S1 and S2 b7f69e8 / c2ecc13 | OK | GB fetch began 10:04, after the lock. |
| **GRID-2 DV-GB1 50502a0 10:06:05** | GB run b7f69e8 10:52:50 | **Claim contradicted** | See M3. |
| GRID-3 (G3a, G3b) b7f69e8 10:52:50 | G3a b9a8e51 11:08:45 | OK on order | The 2024 fetch time is not recorded anywhere (S-6). |
| GRID-4 a3d52ca 10:55:00 | GRID-4 results c2ecc13 11:36:49 | OK | |
| DV-S2 d5ccf03 10:57:36 | S2 code b9a8e51 11:08:45, results c2ecc13 11:36:49 | OK | DE 2026 files fetched 10:54–10:56, so DV-S2 followed the download. It says only headers and first rows were seen. The filenames' CET stamps (16-55-xx = 10:55 ET) agree. |
| GRID-4b c2ecc13 11:36:49 | search 0b9f467 11:47 | OK | The lock shares a commit with the GRID-4 results. That is harmless, since 4b ended UNTESTED. |

No prediction or rule was edited after its analysis commit. Checked with `git log --follow` and `git show` per PREREG file: every later commit touching a PREREG file only adds lines (deviations), except 0b2422a, which changes F1's written time from 8:30 to 8:20 (no content change). ecoli/PREREG.md is byte-identical to 6903de9.
Residual weakness: commit time is author-settable. The only hard ordering evidence is the parent chain, which is intact. The 12 text timestamps below do not match their commits (S-1). The GitHub PR timeline shows commit dates only, not push times.

## 2. Verdict labels against the locked rules
- **GRID-1 INVALID**: correct. mFRR coverage 0.666 < 0.90 (DV1.5).
- **GRID-1b PASS on proxy**: matches the rule (CI 3,425–4,398 s, wholly above 900 s and above 1,800 s). `tools/test_grid1.py` encodes it. It is one low-risk arm and RESULTS_GRID1 says so.
- **GRID-2 G1 FAIL on proxy**: correct. BIC picks the power law, γ = 2.086 ∈ [1.7, 2.3]. I recomputed ΔBIC 6.94 over L2 from `grid2_results.json`. Robustness rows are all PL, so the result is not INVALID.
- **G3a**: power law chosen, γ = 2.016. The prediction PASSED, meaning the GRID-2 FAIL replicates. The labelling is confusing (see M4 and S-9). ΔBIC over L1 is only 1.0 (−151.7 vs −150.7), against 7.9 in 2026.
- **GRID-4 INVALID**: correct. Main: A fails its slope clause (|2.13 − 1.48| = 0.65) and W passes (> 0.5). Q×⅓ gives slope 1.92 (difference 0.44, neither). Q×3 gives 2.60 (W). The verdict changes, so INVALID.
- **GRID-4b UNTESTED**: matches the rule ("if 1–2 cannot be found in an open source"). I checked NESO's page: the Frequency Response volumes list starts at 2022-23, so the claim holds. The search was short (about 10 min) and item 2 was not tried. Say "not found", not "none exist".
- **S1 M-S1 FAIL**: matches the rule (CI 4,939 s to the bound, no overlap with [1,300, 2,900]).
- **S2 W-S2 PASS**: matches the locked rule. Dominant corner 2,956 s (58 %), CI 2,625.8–3,351.8 s, so the lower edge is 25.8 s inside the window. No CI lies in [650, 1,460]. The 15-min comparability run agrees (3,319 s, CI 2,794–3,919). Caveats are in S-3 to S-5. The 246-s corner was declared closed-loop in advance only in a general sense (S-4).
- The status vocabulary is not applied consistently to INVALID/UNTESTED rows in CLAIM_MAP (S-8).

## 3. G3b scope rule
PREREG_GRID3.md:10–15 says "applies from now on" and "the GRID-2 FAIL stands as recorded and is not reclassified". Candid note in RESULTS_GRID2.md:51 repeats it. Forward-only holds for GRID-2's own row (P19 stays PROXY-FAIL). Two problems:
1. G3b makes grids out of scope for (iii) *and* G3a was preregistered in the same commit, yet P21 counts G3a as a PROXY-FAIL of the count claim. That is inconsistent (M4).
2. G3b criterion (1) asks for *measured* read-noise variance; PREREG_GRID3.md:14 declares grids to fail it by assertion ("sensor noise ≪ 1 mHz"), with no measurement.

## 4. E. coli math, independent recomputation
- Digitized Park Fig. 4c (9 points): log-log slope of Var on τ gives s = 0.295 (τ-on-Var 0.327), RMA **0.310**. Matches RESULTS_F2 (0.31, OLS 0.30/0.33).
- Low-SNR optimum EV ∝ τ^{2−2s}/(1+λτ)²; derivative gives **λτ\* = (1−s)/s** exactly. s = 0.31, λ = 0.862: λτ\* = 2.226, **τ\* = 2.58 s**. s = 0.24 gives 3.67 s; s = 0.37 gives 1.98 s; s = ½ gives 1.16 s. The full numerical range in the repo, 1.86–3.58 s, is consistent.
- Share of the optimum's explained variance captured at 9.9 s (low-SNR form): 0.731. The repo's full calc gives 0.70–0.73. OK.
- Log gap closed: ln(2.58/1.13)/ln(9.9/1.13) = 0.38. Repo says 37 %. OK.
- Inputs (τ2 = 9.9 ± 0.3, n = 442, λ = 0.862, a_v = 157.1, G = 1.73, σn = 0.092, τn = 11.75) match Mattingly et al. 2021 in the PMC full text.
- Input-referred noise V0(τ0/τ)^(2−2s) is consistent with arm B's K0 = Gτ2²/(τ1+τ2) ∝ τ only if the kernel gain G does not change with τ. Park's own conditions change a0 and gain with τ (F2 notes a0 but not G). Unstated assumption (S-10).
- D1: 1/λ_CV = 0.58 s and 0.375 s reproduce from λ_CV = 2σ, σ = 0.862 and from λ_CV τ_r = 8/3. D1 "×17–26 short" checks.

**Prior art, DOIs.**
- All 51 distinct DOIs in the PR's added lines resolve on Crossref with matching first author and year. I did this independently. `crossref*.out` lists all except 10.2307/2296441, which resolves (Ashenfelter & Johnson 1972) and sits in an older line.
- ten Wolde group credited: Govern & ten Wolde 2014 (two papers), Becker/Mugler/ten Wolde 2015, Tostevin & ten Wolde 2009, Malaguti & ten Wolde 2021. The characterisation of Malaguti & ten Wolde as concerning the ~100 ms receptor integration time is accurate (their text: "measured integration time, on the order of 100 ms").
- **Not credited: Tjalma & ten Wolde 2024, Phys. Rev. Research 6, 033049, doi 10.1103/PhysRevResearch.6.033049** (resolves on Crossref; the repo has no mention of "Tjalma"). Its abstract and text, as returned by search (I could not open the PDF): E. coli's *adaptation (methylation) time* has an optimum from the trade-off of sampling error against dynamical error; that optimum scales *inversely with gradient steepness*; for shallow gradients it is ≈ 10 s; τ_expt/τ_v ≈ 8. This is the same quantity the PR tests (9.9 s against τ_v = 1.16 s, ×8.5). It already gives the F1 prediction (τ_best ∝ 1/g) that CLAIM_MAP P5 and measured/README.md:15–16 describe as "no measurement found; a simulation finds slope −1". It also supplies a published account of the "remaining factor of 4" that PREREG_D/RESULTS_D never considered (finite receptor/readout sampling error with discrete molecule counts, and a predicted rather than current-u target). The PR's Model S objective (estimate current u, lead 0, one OU mode) is one choice of proxy among published ones. The "×8.5 FAIL" is therefore at least partly a proxy-choice result, and the repo's headline for the E. coli arm should say so (M2).

## 5. SYNTHESIS.md and the law state
Good: the opening disclaims independence. "Not refuted; untested in scope; two proxy failures with specific diagnoses; one diagnosis (actuation-limited layers) itself untested" (lines 54–55) is the right statement. G3b is declared forward-only (41–45). The "decisive next test" is scoped and honest about needing a lab. No hyperbole found. Problems:
- "law" appears in the heading at :47 "Honest state of the law", outside the hypothesis sentence. Also `measured/README.md:16` and `:146` ("1/g law").
- :48 "**refuted on proxy** outside its stated premises (grids: robust, replicated)" is a status word the locked vocabulary does not have ("passed/failed on proxy"). It sits two lines above "Overall: not refuted". The "stated premises" are G3b, written after the miss (SYNTHESIS itself says so at :44).
- :30–31 "where the reconstruction is open-loop, GB's imbalance has no separated time scales": per RESULTS_GRID2.md the BM term B carries about 90 % of the reconstructed variance, and B is the output of the slowest layer. With B dropped, the fit picks a 1,011 s corner holding 99.8 % (grid2_results.json). "Robust" refers only to MFR/L/lag perturbations. G3a re-runs the same pipeline. There is no positive control (no check that a known 4-mode world, passed through BM-style piecewise-constant interpolation, is recovered as K = 4). A step-like input gives f⁻² regardless of the world's time scales.
- :12 and :25 "Drift **ruled out**" / "not the drift objective": RESULTS_D says D1 is DOES NOT EXPLAIN (noiseless maximin) and D2 is **NEITHER**, and qualifies "in the linear, gain-bounded regime; a nonlinear-motor objective is untested". The qualifier is dropped.
- :38–39 "the German slow mode is not an artifact of hourly market products … about the world, as the theory reads it": only account M (market step ∝ product period) was tested. Hourly intraday products, hourly generator schedules and block ramps remain. W has no content of its own (PREREG_GRID_S: S1 "can support M or disfavour it, not confirm W").
- :51–53 groups CE's PASS ("world mode slower than the slowest layer") with E. coli's FAIL under "memory faster than its mode". But STORE_NOISE §4 itself says that under Model S+ with s < ½ (E. coli: s = 0.31) the optimal store is *slower* than its mode (λτ = 2.2), so interlacing "is a property of exogenous noise and speed-free upkeep, not of layering". The E. coli result is then closer to what S+ predicts than to the headline's rule. THEORY.md was not edited, so its interlacing statement is unchanged. SYNTHESIS never says this (M5).

## 6. CLAIM_MAP v2.60 P20–P22
- Verdict text matches the results files (P20 ↔ RESULTS_GRID_S; P21 ↔ RESULTS_GRID3_4 G3a; P22 ↔ GRID-4/4b). Tally recomputed by `check_consistency`: PASS (291 rows; PROXY-FAIL 20, PROXY-PASS 10, INCONCLUSIVE 7).
- P20 PROXY-PASS: the claim is "the mode is the world's, not the market's". That tests a nuisance account of P18's premise, not a GTAO claim. It adds a PROXY-PASS to the tally, which flatters. NOT EVIDENCE for GTAO, or a note on P18, would be more honest (S-7).
- P21 is wrongly typed under G3b (M4).
- P22 INCONCLUSIVE, whereas the same repo maps INVALID to NOT EVIDENCE (P2, P12) and to OPEN (P17). Pick one (S-8).
- The diff also rewrites old notes (v2.7, v2.9 …) to add "THEORY.md: only its CLAIM_MAP version pointer is updated". Harmless and honest, but it edits frozen text.
- DATA_SOURCES: hashes present for every file. URLs are present for GB; missing for the German files (postback buttons) and for GRID-1's setpoint. GB 2024/2019/20 fetch times missing.

---
## MUST-FIX
**M1. Remove "law" outside the hypothesis sentence.** `theory/measured/SYNTHESIS.md:47` ("Honest state of the law" → "Honest state of the hypothesis"); `theory/measured/README.md:16` and `:146` ("1/g law" → "1/g scaling"). Standing rule: "law" only in the hypothesis sentence.

**M2. Cite and engage Tjalma & ten Wolde 2024 (doi 10.1103/PhysRevResearch.6.033049).** Add to `STORE_NOISE.md:87` (Closest prior art), `ecoli/PREREG.md` §6 as a dated note (not an edit to the lock), `measured/README.md:15–16`, and CLAIM_MAP P5 (`CLAIM_MAP_v2.md:514`, "No measurement found; a data-calibrated simulation …"): its analytic optimum for the adaptation time gives ≈ 10 s and τ ∝ 1/g. Add it to the candidate list for the remaining ×4 in `RESULTS_D.md`. Read the paper in full first, because I only saw the abstract and excerpts. State that the P1 FAIL is conditional on the chosen target (current u, lead 0).

**M3. Correct the DV-GB1 timing claim.** `RESULTS_GRID2.md:4` says DV-GB1 (10:06:05) was "before any GB series was downloaded". `DATA_SOURCES_GB.md:2` says fetching ran 10:04–10:12. DV-GB1 itself lists frequency-file columns and one day of BOALF/PN as "seen" (`PREREG_GRID2.md:39–41`). It also says "about 10:15 AM", later than the commit. Replace with "before any GB value was inspected or computed; format and header files were fetched 10:04–10:06". Add an erratum in DEVIATIONS.md. The same sentence in CLAIM_MAP P19 ("DV-GB1 `50502a0` before any GB series") needs the same fix.

**M4. Fix two label problems.**
(a) `SYNTHESIS.md:48` and the CLAIM_MAP v2.60 note (`CLAIM_MAP_v2.md:77`): replace "refuted on proxy outside its stated premises" with "failed on proxy (GRID-2, locked before G3b); out of scope for new tests under G3b". "Refuted" is not a locked status word and contradicts "not refuted".
(b) P21: G3a was preregistered with G3b, which declares grids out of scope for (iii). Either retype P21 as a finding about the world spectrum (NOT EVIDENCE for (iii)) and update the tally, or drop G3b's "grids are out of scope" sentence. Keep one rule.

**M5. State what Model S+ does to interlacing.** Add to SYNTHESIS "Honest state" that (i) STORE_NOISE §4 shows interlacing and the one-mode count are premise-dependent, and (ii) the E. coli memory (λτ2 = 8.5, s = 0.31 < ½) is slower than its mode, which S+ predicts, while the headline's "faster than its mode" is unchanged in THEORY.md. Say that the CE PASS and the E. coli FAIL address different forms of the claim. Remove the single-bullet grouping at `:51–53`.

## SHOULD-FIX
**S-1. Timestamps in text.** Written times are later than their commits in at least 10 places (F1's original 8:30 was already fixed in 0b2422a). Set each to the commit time or delete it. Commit → text: 6903de9 08:19 vs 8:22 (DEVIATIONS.md:3, which also puts the run after the commit holding its output; lock to results was 68 s); CLAIM_MAP v2.54 9:10 vs 08:36; v2.55 10:00 vs 09:05; v2.56 11:00 vs 09:22; v2.57 "afternoon" vs 09:38; `PREREG_GRID_S.md:3` 10:05 vs 10:03; `:41` 11:00 vs 10:57; `PREREG_GRID2.md:39` 10:15 vs 10:06; `PREREG_GRID4.md:3` 10:58 vs 10:55; `PREREG_GRID4b.md:3` 11:40 vs 11:36. Only DV-GB1's mismatch was noted. Also note in README that commit time is author-set and record push time (`git push` log) or tag the lock commits.

**S-2. Analysis code was not committed before the GRID-2 run.** `grid2_run.py` first appears in b7f69e8 with the results (ECOLI-MEM did lock code via LOCK.txt). Add code hashes to future locks. The rules were fixed in text, but the S2 method details (segment length, gap fill, θ range) were chosen at DV-S2 after the files were downloaded.

**S-3. S2 CI is optimistic, and the margin is 26 s.** `grid_s2.py` bootstrap resamples 50 %-overlapping 7-day segments as independent, fixes K = 2 in every resample (ΔBIC 4.3 over K = 3 is thin), and takes the resampled corner nearest the original in log. The CI 2,626–3,352 s is conditional on all of that and is narrower than the real uncertainty. The decisive result (M rejected) does not depend on it. The "W-S2 PASS" label depends on a 26 s margin, so report it as "PASS, margin indistinguishable from the edge" and add a bootstrap that includes model selection. The code does not compute the verdict. Add a function.

**S-4. 246-s corner "declared beforehand".** DV1.2/1.3 (6636517, 09:49:18, before any spectrum) says a corner near 300 s in the setpoint "could be the controller's pole" and declares the 300–900 s corner circular, for the 2022 reconstruction. That predates S2. But GRID-S/DV-S2 do not restate it or say whether a closed-loop corner can be "dominant". As locked, a 246-s corner holding > 50 % would have flipped the verdict. Here it holds 42 %. Say: "declared closed-loop in DV1 for 2022; not restated in the GRID-S lock; the verdict does not depend on it".

**S-5. Like-for-like ratio.** `RESULTS_GRID_S.md` quotes ×0.76–0.85 against 2022. The like-for-like (15-min) ratio is 3,319/3,898 = 0.85 with overlapping CIs. The 2022 value comes from a full year and the 2026 value from Jan–Jun, a seasonal confound.

**S-6. DATA_SOURCES.** Add fetch times for the GB 2024 and 2019/20 files (`DATA_SOURCES_GB_2024_2019.md`), which PREREG_GRID3/4 depend on ("before downloading any 2024 GB data"). Add exact URLs or form parameters for the German setpoint files, or archive the derived 1-min and 15-min series with a licence note, so that GRID-1b and S2 can be rerun.

**S-7. P20 typing** (see §6).

**S-8. Status mapping for INVALID/UNTESTED.** P17 → OPEN, P2/P12 → NOT EVIDENCE, P22 → INCONCLUSIVE. Define one mapping in the CLAIM_MAP header.

**S-9. Label G3a clearly.** "Replication prediction PASS; (iii) count remains FAIL on proxy (GRID-2)". Call the margin "ΔBIC 1.0: a coin flip between PL and one Lorentzian" instead of "robust".

**S-10. E. coli proxy caveats.** F2's s is from CheY-P variance (Park) and cell-to-cell kinase noise (Keegstra), which include upstream noise filtered by the adaptation kernel, not purely the store's own noise. Assuming kernel gain G is independent of τ is needed for the V0(τ0/τ)^(2−2s) mapping (see §4). The slow pole as "memory of an estimator of u" is one reading. Another is the high-pass corner for baseline rejection. Say so in RESULTS_F2 "Hostile notes".

**S-11. Positive control for the GB pipeline** (see §5). Synthetic 1-, 2- and 4-mode worlds, piecewise-constant BM-style sampling, same fit and BIC, and report the recovery rate of K_sep. Until then call the GB result "failed on proxy; proxy power unknown".

**S-12. `OUTREACH_DRAFT.md` is in a public CC0 repo** with Chad's email. It is unsent and labelled so. Keep it out of the public tree (it can live in the notes store), or confirm Chad wants it public. Nothing should be sent without his go.

**S-13. "Drift ruled out"** (SYNTHESIS:12, :25): restore the "within the linear, gain-bounded regime" qualifier and the D2 verdict NEITHER.

**S-14. GRID-4b search.** Record the searched URLs, and say item 2 (FFR volumes) was not attempted.
