# Independent hostile review: PR #116 (head 3fd189c, branch v2.8-htindex): HT_INDEX.md, ht_checks, CLAIM_MAP v2.67 rows N58–N63

Reviewer: independent executor. I did not write this PR. Fresh clone at /workspace/rev116, nice 19. Review date: Fri 20 Nov 2026, about 3:30 PM ET.
Nothing was pushed, commented or merged.

## Verdict: **NOT-READY** (three blockers; all can be fixed in one pass, and no rerun of the arms is needed except to recompute after S1)

The core math (N58, N59 in narrow form, N60) is right, and the code reproduces bit-for-bit. What fails is how some evidence is described. One headline claim is false (MF-DFA). One headline count is pseudo-replicated and is not measured from data (interlacing). And the branch no longer merges cleanly with main.

## What I ran

- `pytest tools/` on the PR head: **101 passed** (10m44s under a box load of about 16). `tools/check_consistency.py`: **PASS**, FAIL 0 (21 INFO frozen).
- Full rerun of arms K, B, D and C plus `analyse.py`, in a copy (/workspace/rev116_rerun). `arm_B/C/D/K.json` came out **byte-identical** to the committed files, and `summary.json` gave the same plug-in and Whittle accuracies. The numbers are reproducible from the code. Arm A was not rerun; its tests pass.
- Independent numerics (/workspace/rev116_scratch):
  - p(α), the slopes, the half-normal head fractions and the GPD limit;
  - an MF-DFA width test against n (`mfw.py`);
  - an N60 convexity scan over 40 random Model S worlds (`convex_scan.py`);
  - a check of the plug-in ε values (`plug_eps.py`).
- Crossref check of all 20 DOIs in §7, plus a prior-art search.

## Blockers

**B1. The branch conflicts with main; it needs a rebase and a renumber.** `git merge-tree origin/main pr116` gives CONFLICT in README.md, STATUS.md, THEORY.md and measurement/CLAIM_MAP_v2.md. PR #113 has merged (main 1597218, CLAIM_MAP v2.65), and PR #115 holds v2.66. On rebase:
- recompute the tally at CLAIM_MAP_v2.md (the v2.67 note, line 77, and the tally block);
- fix the pointers at README.md:31 and THEORY.md:3;
- drop "open PRs #113" from the v2.67 note and from the CHANGELOG line;
- rerun pytest and check_consistency on the rebased tree.

**B2. The interlacing evidence for N63 is misdescribed (HT_INDEX.md:11, :128; CLAIM_MAP_v2.md:455).**
- `interlaced()` (arms.py:293, called at :313) is computed from the design's true store rates `b` and the true world `D_TAUS`. It is not computed from any record or I/O fit.
- The four "optimized K=3" rows are one design (store τ 0.29, 5.62, 167) repeated over four noise seeds (arms.py:330). So "4 of 4" is n = 1, and its outcome is fixed by the CT21/B.9 theorem. It is not an empirical separation.
- Under the null's log-uniform rates, the chance that a random K=3 design interlaces is about 0.10. So 0 of 9 has a probability of about 0.37 even with no effect.
- One "random" K=3 design is within 0.74% of E_∞ (store τ 0.41, 1.07, 4.65) and is not interlaced. If anything, that is evidence that interlacing does not mark near-optimal designs, which are what selection delivers.
- Restate as: "the optimal K=3 design interlaces, as CT21/B.9 requires (one design; computed from its parameters, not from data); 0 of 9 random designs do (about 0.9 expected by chance)". Add the near-optimal non-interlaced case. To make it a data signature, compute interlacing from the I/O-fitted τ (`io_taus`), over several distinct optimized designs (different worlds).
- The same pseudo-replication caveat applies to "I/O recovered K in 11 of 12" (:11, :127). That is 3 designs × 4 seeds, with record noise 0.01, which is close to noiseless.

**B3. The MF-DFA claim is false as stated (HT_INDEX.md:10, :57, :80).** "The multifractal width is zero in principle for Gaussian worlds, so any correlation it shows is a finite-sample artefact." The width measured by `mfdfa` does not shrink with n (rows show the 3 seeds):

| World (noise 0.3) | n = 2·10⁴ | n = 2·10⁵ | n = 2·10⁶ |
|---|---|---|---|
| J = 1 | 0.03–0.06 | 0.08–0.09 | 0.074–0.082 |
| J = 4 | 0.03–0.08 | 0.007–0.03 | 0.036–0.042 |

- The width is systematic and depends on the world. It comes from the time-scale crossovers: the spread of segment variances depends on s/τ, and a single log-log fit over all scales turns that into a q-dependence.
- Asymptotic monofractality is a statement about scaling limits. It is not a statement about this finite-scale estimator. The −0.35 Spearman correlation with J is therefore plausibly real (a crossover signature), not noise.
- Restate as: "true multifractal spectrum is degenerate for Gaussian processes; the MF-DFA width here is a crossover-induced estimator bias that does not vanish with n; it does not count modes".

## Should-fix

**S1. The repo optimizer can return a non-physical E_K < E_∞, and one plug-in number depends on it.**
- The bug is in `theory/layers_checks/stores.py:39–50`. `E_K` minimizes MSE with near-coincident stores held apart only by a 1e-9 jitter. The ill-conditioned M then gives a spuriously low MSE, and `E_K` returns that value, not the MSE re-evaluated at the returned b.
- Reproduced twice:
  - Random world (τ 1.27, 1.43, 30.9, 244): ε_4 = −1.1e-4. The returned stores include 0.1837 twice. Re-evaluating at the returned b gives +5e-6, and E_∞ by quad agrees with the trapezoid value.
  - Plug-in fit of world [1, 10, 100, 1000] at noise 0.3 (n = 2·10⁵): ε_4 = −0.19%. That is the single plug-in overcount at R = 10⁴, and it makes R = 10⁶ "correct" for the wrong reason. With the bug fixed, the headline would be about 78% at 10⁴ and 50% at 10⁶ (I reasoned this from the costs; I did not rerun it), against the 76% and 52% stated.
- Fix: penalize coincident stores, or clamp to E_∞ and re-evaluate. Then recompute summary.json and N61. This is pre-existing code, so check whether LAYERS.md numerics are affected too (arm_K had no negative ε).

**S2. The head-to-head table has no base rates, and the headline overstates the plug-in (HT_INDEX.md:9, :72–82; CLAIM_MAP:453).** At n = 2·10⁵ (54 records):

| R | 10 | 10² | 10³ | 10⁴ | 10⁶ |
|---|---|---|---|---|---|
| True K\* | all 1 | 24 ones, 30 twos | 9 / 39 / 6 | 6 / 30 / 15 / 3 | 6 / 18 / 18 / 12 |
| Best constant guess | 100% | 56% | 72% | 56% | 33% |
| Raw Whittle pole count | 13% | 50% | 82% | 78% | 50% |
| Plug-in | 100% | 100% | 94% | 76% | 52% |

- So the plug-in beats the raw pole count only at R ≤ 10³, ties it at 10⁴ and 10⁶, and "100% at R = 10" is trivial.
- Add a "best constant" row and say this plainly in §0 item 3.
- Also state the fairness caveats:
  - the Whittle model class is exactly the generating class (well-specified, oracle-like), which no rival gets;
  - R is given to the plug-in, not estimated;
  - the ΔBIC ≥ 10, factor-3 and band settings are inherited from the counting rule and were not tuned on these records. This is fair, but say so.
  - the `spectral_peak_count` prominence is set to 0.1 in arms.py, against a default of 0.15, with no stated rationale. Say whether it was chosen before seeing results.

**S3. Use one denominator for the plug-in numbers.** "In 108 simulated records" (HT_INDEX.md:8; CLAIM_MAP:453) is mixed with plug-in percentages that come from the 54 records at n = 2·10⁵ only (analyse.py:32). State 54 wherever the plug-in or K\* accuracy is quoted.

**S4. Scope of N59 (HT_INDEX.md:7, :44; CLAIM_MAP:451).**
- "The same holds for any statistic of the one-time marginal" is wrong for scale-dependent statistics. The variances of Δ_δ y across δ give the structure function, which carries all the time-scale information.
- Restrict the claim to scale-invariant (shape) statistics of a single marginal, or to a single fixed linear functional.
- Say that the periodogram and crossing-duration estimators are non-linear read-outs outside N59, and that their failure here is empirical only.
- "That channel [effective sample size] carries no count of modes" is asserted, not proved. Either label it as not proved or soften it.
- What is proved is the narrow claim (ht and head fractions of linear read-outs converge to the same value in every world). Keep that.

**S5. N58(b) says too much about the Gumbel domain (HT_INDEX.md:21–22).** "The whole Gumbel domain ... ht grows as ln n" contradicts (c): the Gaussian is in the Gumbel domain, and ht = 1 at 0.40. Say that p → e^{−1} is the limiting deep-tail fraction, and that ht grows only if every earlier split is at or below the threshold. Also note the Weibull domain (ξ < 0): p = (1−ξ)^{1/ξ} ≥ ½ for ξ ≤ −1, as for the uniform, so ht = 1.

**S6. "Counting-rule proxy" conflates two objects (HT_INDEX.md:9, :67, :135).**
- The counting rule (face_placements.md:172–199) fits the system's **I/O response kernel**.
- The Whittle count in arm B fits the **world's spectrum**, with the rule's thresholds borrowed. The plug-in is therefore the *prediction* half of N56 (measured spectrum → argmin J), not "the counting rule plus N56".
- Only arm D's I/O fit is a counting-rule analogue.
- The proxy also differs from the rule: real poles only (no complex pairs or degree counting) and greedy forward ΔBIC. State both differences.

**S7. Prior art and framing of N58.**
- Missed: head/tail breaks 2.0, where the 40% bound applies to the *average* head fraction (Jiang 2019, *Sustainability* 11:4091, 10.3390/su11154091, verified on Crossref). Under it, the Gaussian knife-edge result changes (the running mean of 0.4249, 0.4048, 0.3951, 0.3893, 0.3856 drops below 0.40 after five splits). So state that "ht = 1 for Gaussians" is specific to head/tail breaks 1.0.
- Jiang treats growth of ht with added small-scale data as intended behaviour, not a confound: "If we added 512 squares of the smaller size 1/81, the Ht-index would increase by one" (Jiang 2016, European Handbook of Crowdsourced Geographic Information, 10.5334/bax.m, verified). Cite it, and frame the ln n growth as "ht counts sample-size-limited scales, by design".
- I found no published closed form ht ≈ 1 + ln n/ln(1/p(α)), so the novelty statement at :165 stands as hedged.

**S8. N60 label (CLAIM_MAP:452; HT_INDEX.md:46).** Its status is PROVED (in-model), but the result rests on a convexity premise that is numerical only. Use a conditional status, for example "PROVED (in-model) given convexity (numerical)", in the status column itself.
- My scan supports the premise, and the count formula equals the argmin wherever ε_K was valid: 39 of 40 random worlds were convex and matched for every R from 10 to 10⁸. The one exception is the S1 optimizer bug, not a real non-convexity.
- N60 is consistent with N56 (one layer per separated scale the stakes pay for), with L2 (K\* ≤ J) and L3 (no finite exact count). It is CX4 restricted to 𝓜_LG, as the PR says.

**S9. Small factual misreads.**
- HT_INDEX.md:86 says the pole count goes "2 → 3 for H = 0.7". The data give n = 2·10⁴ → [2, 2, 2] and n = 2·10⁵ → [2, 3, 2], which is 2 → 2 by median. Also report the α = 1.5 band (2 → 2).
- HT_INDEX.md:30–31: the measured slopes are non-monotone in α (1.95 at α = 2.5 against 1.78 at α = 3). Say this is within replicate noise, or add replicates. The test tolerance of 0.45 per decade (tools/test_ht_index.py) is loose.

**S10. N62 and N63 labels are OK.** Both are OPEN and described as exploratory and not locked, and arm C's "8 of 12" is reported with its failure modes. Add that each arm C world has 3 seeds (n = 3 per cell), and that the DMD verdict is about this implementation only, which is already said.

## Checks that passed

- **N58 math.** E[X | X > t] = αt/(α−1) gives p = (1−1/α)^α. Values: 0.1925, 0.25, 0.2789, 0.2963 for α = 1.5, 2, 2.5, 3, and p → e^{−1} as α → ∞. The predicted slopes per decade are 1.397, 1.661, 1.803, 1.893 and 2.303; measured 1.48, 1.63, 1.95, 1.78 and 2.21. At α = 1.5, n = 10⁶, the leading order gives 9.38 against 9.53 measured. The GPD limit (1−ξ)^{1/ξ} with ξ = 1/α matches the Pareto value exactly.
- **Gaussian first split.** 2Φ̄(√(2/π)) = 0.42494. The later fractions are 0.4048, 0.3951, 0.3893, 0.3856, matching the stated 0.405, 0.396, 0.389.
- **ht code.** It reproduces the Zipf 1…1/10 → 3 example. The ≤ thr convention is the same as classInt's.
- **Whittle likelihood.** The binned form m(log S + P̄/S) is correct. The AR(1) spectrum is the exact sampled-OU spectrum. Davies–Harte fGn is correct.
- **DFA/MF-DFA.** These follow Peng 1994 and Kantelhardt 2002. Kantelhardt's reverse-direction segments are omitted, which is minor. The objection is to how the results are read (B3), not to the code.
- **DOIs.** All 20 in §7 resolve on Crossref with matching author, year, volume and pages. Embrechts et al. is a book DOI, and it resolves via doi.org and Crossref.
- **Wording.** In the diff: no new "law" wording, no "theory of everything", no "bill" or joules. "power-law" appears only as the physics term.
- **Tally arithmetic.** The PR's +2 OPEN, +3 PROVED, +1 MATH-CORRECTED and +6 total is consistent with rows N58–N63, and check_consistency passes on the PR head. It must be recomputed after the rebase (B1).

## Confirm round (head bc6e9c5, rebased on main 1998a2d)

Reviewer: independent executor. I did not write this PR or the first review's fixes. Confirm date: Fri 20 Nov 2026, about 3:52 PM ET. Fresh checkout of `origin/v2.8-htindex` at `/workspace/rev116`, nice 19. Nothing was pushed, commented or merged.

### Verdict: **READY**

Every blocker and should-fix from the first review is resolved in the tree. The headlines I recomputed, and those I reran, match the text. CLAIM_MAP v2.67 is provisional and will need to become v2.68 when this merges after PR #117; that is already noted in the v2.67 note and is not a blocker.

### What I ran

- `git merge-tree --write-tree origin/main HEAD` is clean (tree `2ba0e93`). Head is `bc6e9c5`, merge-base is main `1998a2d`. The two commits on top of main are this PR only.
- `pytest tools/` on the PR head: **112 passed** in 12m14s. `tools/check_consistency.py`: **PASS**, FAIL 0 (21 INFO frozen). CLAIM_MAP row count 310 matches the tally; section N is N1..N63; wording FAILs 0.
- Independent rerun of arm D2 (`nice -n 19 python3 arms.py D2`) in a copy: designs, chance probabilities, and all 144 records agree with `arm_D2.json` on every headline field (`whittle_record`, `whittle_input`, `io_count`, `interlaced_data`, `interlaced_params`, `K_agent`).
- Independent recompute of the 54-record baselines from `arm_B.json` / `arm_K.json` / `summary.json`, then a full rerun of `analyse.py`: `summary.json` is bit-identical, including `plugin_detail`.
- Optimizer: reproduced the S1 bug on the review's world with `stores.py` from main (`ε_4 = −1.14·10^{-4}`, two coincident rates); the fixed code stays above `E_∞` (`ε_4 = +6.8·10^{-8}`) and treats a coincident pair as one store. Reran `layers_checks/experiments.py` (output matches the committed files), `figures/face_collapse_v23.py` V2 for 300 worlds, `meq_checks/meq_checks2.py` and `meq_checks/part2.py` with old and new `stores.py`.
- Crossref: all 23 DOIs in HT_INDEX.md §7 resolve, with matching author, year, venue and pages (Jiang 2016 is the book chapter `10.5334/bax.m`; Jiang 2019 is *Sustainability* 11:4091, `10.3390/su11154091`). Jiang 2016 quote and Jiang 2019's "~head" rule checked against the papers' text.

### Blockers

**B1. Rebase — resolved.** `git diff origin/main...HEAD` is this PR's content only (24 files). CLAIM_MAP changes are the v2.67 note, rows N58–N63, and the tally (OPEN 80→82, PROVED 88→91, MATH-CORRECTED 22→23, total 304→310). The 35 NOT A TEST lines are identical to main. The #115 rows (CT37–CT40, CL18, CX7, CX8) and the #113 rows P23–P25 are identical to main. Pointers in README.md:31, THEORY.md:3 and STATUS.md read v2.67. The v2.67 note already says the number is provisional because draft PR #117 also claims it. (PR #117 is now taking v2.67, so this branch becomes v2.68 at merge; no change is required in this tree before that step.)

**B2. Interlacing / I/O claims — resolved.** The withdrawn arm-D numbers are described as a pilot and are no longer used as evidence. Arm D2 is 12 worlds, 36 distinct optimized and 36 random designs, record noise 0.1 and 0.3 of the record sd, 144 records, everything read from data. My counts, and the rerun, match the text:

- record-only pole count equals the input's in 67 of 72 optimized records and the agent's K in 22 of 72;
- I/O recovers K in 56 of 72 optimized and 59 of 72 random (31/36 and 25/36 at noise 0.1 and 0.3 for optimized; 31/36 and 28/36 for random; K = 3 optimized: 9/12 and 3/12);
- parameter interlacing: 12 of 12 optimized K = 3, 2 of 14 random (Monte Carlo chance 0.098–0.112, mean 0.106), and one random K = 3 design at 0.31% excess does not interlace;
- data interlacing, when both fits find three scales: 15 of 15 agree with the parameters, computable in 15 of 52 K = 3 records (9 of 9 optimized interlaced, 6 at noise 0.1 and 3 at 0.3; 0 of 6 random). The two parameter-interlaced random designs are not in that computable set, which the text's small-sample caution fairly covers.

The conclusions as written are honest: I/O identifies a design, not optimization; interlacing as a data signature of optimization is unsupported so far; N63 stays OPEN.

**B3. MF-DFA — resolved.** Restated as a crossover-induced estimator bias that does not vanish with n. `arm_M.json` and `test_mfdfa_width_does_not_vanish` match the table: one mode, widths 0.03–0.06, 0.076–0.093 and 0.074–0.082 at n = 2·10⁴, 2·10⁵ and 2·10⁶; four modes, 0.033–0.083, 0.007–0.029 and 0.036–0.042. The −0.35 Spearman correlation is kept as a plausible crossover signature, not a mode count. (The prose rounds the mid-n one-mode range as 0.08–0.09 and the four-mode mid-n range as 0.01–0.03; ordinary rounding, not a residual false claim.)

### Should-fix

**S1. Optimizer — resolved.** Fix is in `theory/layers_checks/stores.py` (`mse_given_b` on the well-conditioned eigen-subspace; `E_K` returns the re-evaluated MSE). Regression test `test_store_optimizer_never_below_causal_minimum` is present and is in the 112 that passed. No merged result depended on the bug, independently checked:

- `layers_checks/experiments.py`: K* is unchanged in every cell; cadence ε values change only at 10⁻¹⁵; the only material change is the redundant K = 4 store in the three-mode cadence world (old taus started at 0.003, new at 0.22 and 0.51), with excess 0.000% either way. LAYERS.md cites ε₁ = 3.9%, ε₂ = 0.08%, ε₃ = 0, K* = 1,1,2,2,3,3 and stores at 0.22, 5.5 and 176, none of which moves. My rerun of `experiments.py` matches the committed `experiments.json` / `.out` exactly.
- `face_collapse_v23.py` V2, 300 worlds: convexity 0.9733, within-tolerance 1.000, failures 0, flags identical to the committed (old-optimizer) json; one world (seed 103) has max |ΔE| = 1.51·10⁻⁵.
- `meq_checks2.py` and `part2.py`: printed E, ε and K* are unchanged; only store time constants move, at the 8th significant digit (e.g. τ₁ 2.22469511 → 2.22469525). The committed `.out` files still reflect the old code, which is right, because no claimed number changed.

`plugin_negative_eps` is 0. Plug-in accuracies are 100/100/96/78/50% at R = 10…10⁶.

**S2 / S3. Baselines and denominator — resolved.** The table and the 54-record denominator are in §0 item 3 and §3. Recomputed and reproduced by `analyse.py`: best constant 100/56/72/56/33%, raw pole count 13/50/82/78/50%, plug-in 100/100/96/78/50% at R = 10…10⁶; true K* counts match; R = 10 is all ones (trivial); plug-in beats the pole count only at R ≤ 10³ and ties it at 10⁴ and 10⁶. Fairness caveats (well-specified class, R given, inherited thresholds, prominence 0.1 possibly tuned) are stated. (82% is 44/54 = 81.5% rounded.)

**S4. N59 narrowed — resolved.** The claim is restricted to scale-invariant shape statistics of one fixed linear read-out. Scale-dependent statistics and non-linear read-outs are excluded; the "no usable count of modes" step is marked asserted, not proved.

**S5. N58(b) — resolved.** It is now a limiting deep-tail fraction; growth requires every earlier split at or below the threshold; the Gaussian Gumbel-domain exception is named; the Weibull domain (ξ ≤ −1 ⇒ p ≥ ½, ht = 1) is named.

**S6. Naming — resolved.** The plug-in is called the prediction half of N56, not "the counting rule plus N56". Differences (real poles only, greedy forward ΔBIC) and that only arm D/D2's I/O fit is a counting-rule analogue are stated.

**S7. Jiang 2019 / 2016 — resolved.** Head/tail breaks 2.0 is credited (Jiang 2019, 10.3390/su11154091, Crossref-verified). The paper applies the 40% threshold to the average head ("~head"); the PR reports both a stepwise and a prefix reading, which the printed recursion leaves open, and `arm_H2.json` matches the stated Gaussian numbers (prefix 5.4, 8.7, 11.85, 14.4 at n = 10³…10⁶; stepwise ht = 1). "ht = 1 for Gaussians" is specific to 1.0 (and the stepwise reading of 2.0). Jiang 2016 (10.5334/bax.m) is credited, and the Sierpinski sentence is quoted verbatim from the chapter: "If we added 512 squares of the smaller size 1/81, the Ht-index would increase by one, but the fractal dimension would remain unchanged."

**S8. N60 status — resolved.** The status column is `PROVED (in-model) given convexity (numerical)`. The count formula is the first status word, so the tally treats it as PROVED, which is the intended conditional.

**S9. Small misreads — resolved.** H = 0.7 is 2 → 2 (seeds [2,2,2] → [2,3,2]); the α = 1.5 band is 2 → 2; the non-monotone α slopes are attributed to replicate noise, and the 0.45-per-decade test tolerance is disclosed as loose.

**S10. N62 / N63 labels — resolved.** Both remain OPEN, exploratory and not locked. Arm C's "8 of 12" is 4 worlds × 3 seeds (C5 has no clean truth); I re-counted 8 of 12. The DMD verdict is still this implementation only.

### Notes (not blockers)

- At merge, renumber this note and the tally to v2.68 if PR #117 has already taken v2.67, as the v2.67 note already provides for.
- The GitHub PR description still quotes the withdrawn "11/12" and "4/4 vs 0/9" figures and the old #113/#115 numbering conflict. The repo text is correct; the description should be updated when the PR is prepared to merge.
- Ordinary rounding only: H2 prefix 11.85 written 11.9; random-design excess max 891.7% written 890%; a few MF-DFA ranges rounded as above.

