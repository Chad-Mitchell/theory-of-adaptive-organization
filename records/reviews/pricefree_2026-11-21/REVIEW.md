# Independent hostile review: PR #131 (price-free classification, no lock)

**Reviewer:** independent (wrote none of the PR, `theory/PRICE_FREE_2026-11-21.md`, or the OPEN_WORK §8 pointer).
**Date:** Saturday 21 November 2026, started 4:17 AM ET, finished 4:30 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/131
**Clone:** fresh `/tmp/gtao-rev131/repo` at head `0be10b36b69a1becbb7ff0809063db258e65fc03` (branch `pricefree-2026-11-21`), merge-base `d42220dff45e11cf238b58faa3cd016e4c7a536c`. `origin/main` at review is the same `d42220d` (PR #130 merged). Clean tree at review start. Nothing merged. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Compute at nice 19.

**Verdict: READY-WITH-FIXES**

The note is a classification of existing theorems, not a lock, not a new law, and not a re-score. The three-bin cut is faithfully drawn from the cited results, conjectures are labeled, and the bottom line is honest: dropping the demand for absolute fitness-unit prices does not, by itself, produce a field test. `CORE.md` is byte-identical to `origin/main`. The law-of-adaptive-organization hypothesis sentence is unchanged. No locked row is touched.

Two should-fixes belong in this PR before merge. Neither moves a theorem, a lock, or a field verdict. S1 is an algebraic slip in how PF8 states S3's exponents (interval exponents are attributed to the refresh rate, with the wrong signs). S2 is missing prior art for the qualitative phenomenon behind the "distinctive" ruin-binding sign flip (Stephens 1981 / Caraco energy-budget rule, and more closely Dall & Johnstone 2002 on information as a luxury under starvation risk). Credit is required so "distinctive to *J*'s structure" is not overread. The scoped in-model claim can stand once that literature is named and the remainder is stated.

---

## What was checked

- Fresh clone at the stated head/base; diff `d42220d..0be10b3` (one commit, 2 files, +173 / −1): new `theory/PRICE_FREE_2026-11-21.md` and a one-sentence pointer in `OPEN_WORK.md` §8. No other path is touched.
- Every theorem citation and line in §§0–1 against current `CORE.md`, `THEORY.md`, `theory/GENERAL_THEOREM.md`, `theory/LAYERS.md`, `theory/MASTER_EQUATION.md`, `theory/STORE_NOISE.md`, `core/bridge_2026-11-21/SELECTION.md` and `RESULTS.md`, `measurement/FRAMEWORK.md` §§1.4, 5, 6.3–6.7 and 9 item 6, and `theory/meq_checks/scope_checks.py` §1b. A few price-invariance claims were re-derived algebraically (CT12 / CT13 / S3).
- Distinctiveness of the named three against the named rivals R1–R3, and a short prior-art search for PF2 (risk-sensitive foraging / energy-budget rule; state-dependent information under starvation) and for PF7 (Senders, general-power EOQ / fBm sampling).
- Whether anything is presented as new that is already in the repository.
- Beekman 2001 and Dornhaus 2006 numbers against opened full texts; all five DOIs queried on `https://api.crossref.org/works/{doi}` this session. InventoryBench page, GitHub API, and a sample `test.csv` LFS pointer were re-fetched.
- CORE.md / law sentence / re-score: `CORE.md` SHA-256 `aee235cb2a9b7d46a0e82c97825984eb3f5dcb160bdd283c90df552616284a7a` is identical on this branch and on `origin/main`. The two-file diff does not touch `CORE.md`, `THEORY.md`, `CLAIM_MAP_v2.md`, or any locked results file.
- `python3 tools/check_open_work.py` PASS. `python3 tools/check_consistency.py` PASS (0 FAIL; frozen-record INFO hits only; soft length WARNs already on main). `python3 -m pytest tools/ -q`, with `~/.elan/bin` on `PATH`, at nice 19: **146 passed** in 2:36. Full `tools/check_lean.sh` (`lake build`) was not re-run; the PR does not touch `formal/lean/`, and the Lean source tests are inside that 146.

---

## 1. Citations, line numbers, and algebra

Almost every pointer is accurate. Master Theorem (ii) at `THEORY.md` line 80 is already called "a robust, price-free prediction." `CORE.md` line 20 is the free-price sentence the note quotes. S1 / S3 sit at `theory/GENERAL_THEOREM.md` lines 303 and 310–316, and S3 already labels the "real systems sit in the generic class" claim a conjecture. CT12's `T* = [α·c/((α−1)·w·q)]^{1/α}` is at line 337, proved at 339. CT14's closed form and CT15's heading ("the level's technology sets the exponent, independently of α"; −1 and −(1+θ), each at every α) are at lines 353 and 359–361. Lemma B3's opposite signs are at line 371, scoped to a common technology. Lemma B4's floor is at 373. CT33 and the ruin-binding failure, including the "adding the two optimality inequalities" proof and the numerical counterexample, are at lines 80, 126, and 470, which is inside Appendix B.10 (heading at 451). `scope_checks.py` documents §1b in its header and checks `ruin-binding counterexample: S falls and E rises`. L1–L3, N60, L4 / CL12, and the cadence-world numeric match the cited lines, and the note correctly flags that LAYERS L1's older "*K* = 1 for every *w* and *h*" is governed by THEORY's *K* ∈ {0, 1}. FRAMEWORK §6.3's exact phrase is "price invariance (*h* ≈ 0 only)"; §1.4 is relations between independently measured quantities, not universal constants; §9 item 6 is R1–R3 as named. T27's official record is FAIL because P3 failed 0/3 (PR #122); the note says only that, which is right. Convexity remains unproved (`CORE.md` line 36). The CT13 corollary is algebraically correct: with *u* = ln(`T`/`T*`), ψ(0) = 1, ψ′(0) = 0, and ψ″(0) = α − 1. It is labeled a corollary, and the exact spread ratio under a nonlinear map *m*(*J*) is labeled a conjecture.

Price invariance of the PF7 elasticity follows from the cited formula: the look rate is ∝ (*w q*/*c*)^{1/α}, so the elasticities in *q* and in *w*/*c* are 1/α and the prices cancel. Currency invariance (PF19 / S1) is the usual homogeneity fact, with the feasible-set caveat correctly taken from CT24. The onset exponent −(1−*b*)/(1−*a*) at *h* = 0 does not involve *h* or *w*. With *h* > 0, THEORY line 357 says the small-ρ exponent stays −(1−*b*)/(1−*a*) if *a* > *b* and becomes −1 if *a* ≤ *b*; either way it remains price-free. The note's "stays price-free" is true; it does not spell out the case split (Nit 3).

**S1 (should-fix).** PF8, and the §0 bullet on S3, call S3's exponents "**refresh-rate** exponents" and then quote the numbers from `theory/GENERAL_THEOREM.md` line 313: −*p*/(1+*pH*) on σ and 1/(1+*pH*) on *c*/*w*. Those are the exponents of the interval `T*`, not of the refresh rate 1/`T*`. S3's displayed formula is `T*` = [*c*(*pH*+1)/(*pH* · *m_p* · *w* σ^*p*)]^{1/(1+*pH*)}, and the worked values (−1, −⅔, −⅘) are `T*` exponents on σ. The refresh-rate exponents would be the negatives: +*p*/(1+*pH*) on σ and −1/(1+*pH*) on *c*/*w*. PF7 states look-rate elasticities with the correct sign; PF8, bundled with it as distinctive item 2, does not. Fix the wording to interval / `T*`, or flip both signs. Do not leave a sign error in a "distinctive" row.

Two citation slips are nits, not should-fixes: PF7 points at THEORY line 101 for "does not hold with read noise or for a world with its own time scale," but line 101 is the CT24 *share* failure (the 0.89, 0.62, 0.50 figures), not a demonstrated failure of the 1/α look-rate elasticity. The CT12 setting is exact reset reads, so the elasticity is not claimed outside that setting; cite that restriction, not the share numbers. PR10 cites `theory/LAYERS.md` line 53 for *K** ∝ (*C*/*h*)^{1/3} *L*^{2/3} and for the withdrawn-as-store-count remark; both are at line 57 (line 53 is a leftover sentence about rational spectra).

---

## 2. Are the three "distinctive" claims actually distinctive?

Against the *named* rivals R1–R3, the cut is fair, and the note is already blunt that most of §1.1 is Topkis / Kalman–Wiener / Harris / Lee–Flack–Krakauer / Sella–Hirsh / homogeneity.

**PF7 / PF8 against R2.** R2, as locked in FRAMEWORK §9 item 6, is a universal exponent of ½. At a locked α = 1.5 or 2.5, 1/α is 0.667 or 0.400, and that is a real discriminator against R2, R1, and R3, in the CT12 setting only. The note correctly says it is not distinctive at α = 2, and not proved for continuous filters (Lemma B2 gives different exponents, including precision effort ∝ *w*^{α/(2α−1)}). A short search did not turn up a prior statement of this exact look-rate elasticity for general self-similar α that would collapse the claim against R2. Senders 1964 is Nyquist (sampling rate linear in bandwidth), not 1/α. The √ law at α = 2 is already credited (Harris, Barro, Dixit, Senders, Lee–Flack–Krakauer doi 10.1098/rspb.2024.1606). The repo's own `litmap/PRIOR_ART.md` already flags "predicting exponents by regime" as a possible add, not as a kill of the 1/α-versus-½ contrast. N51 remains OPEN and is not re-scored; "lab humans are not a strongly selected class" is a standing qualification point, not a new official verdict. This item can stand.

**PF6 / PF10.** Lemma B3's opposite signs against a single-sign total-volatility rival are already the FRAMEWORK §6.4 (T3) contrast with contingency theory. CT15's technology-not-α exponent, with the −1 reset-read case already credited to Veldkamp & Wolfers 2007 and Van Zandt & Radner 2001, is carefully scoped. Existence of a sharing threshold is correctly declared not distinctive. No fix required.

**PF2 (the ruin-binding sign flip) — S2, should-fix.** The in-model claim is accurately stated as a possibility, proved by a numerical counterexample, not as a theorem that spend always falls when ruin binds. "Expected-cost optimizers without a feasibility set that depends on *w* never predict spend falling as stakes rise" is correct as scoped. The mechanism (the reserve pays *J*; realized-loss variance scales with *w*²; a costlier design can become uncertified) is specific to this *J*.

It is not, however, without relevant prior art, and the review brief named the first place to look. Stephens 1981 (*Anim. Behav.*, the energy-budget rule) and Caraco, Martindale & Whittam 1980 already predict a *sign flip* in comparative statics when a survival / starvation threshold binds: risk-averse above the threshold, risk-prone below it. That is a flip in risk preference over reward variance, not a theorem about judgment spend in *S* + *w E* as *w* rises, and in the CT33 counterexample the uncertified design is the *higher*-variance one, so the forced switch is toward lower variance, closer to a chance constraint than to risk-proneness. Closer still is Dall & Johnstone 2002, *Phil. Trans. R. Soc. B* 357:1519–1526, doi 10.1098/rstb.2002.1061: under starvation risk, "gathering information is a luxury while insurance is a necessity," and sampling declines as reserves fall and as the bout runs late. That is prior art for information *effort* falling when a survival constraint binds. The repository already cites Stephens 1991 and McNamara & Houston 1987 in `litmap/`, but not this energy-budget / information-as-luxury line in connection with CT33.

Require credit in §2 item 1 and in §3.1. State plainly that survival-constrained models already predict reversals of monotone effort or risk comparative statics, name Stephens 1981, Caraco et al. 1980, and Dall & Johnstone 2002, and then state what remains distinctive: the comparative static in the stake *w* of an expected-cost objective *S* + *w E*, with this reserve-pays-*J* / *w*²-variance mechanism. Do not leave "distinctive to *J*'s structure" unqualified. After that credit, the item can remain on the short list of distinctive price-free predictions.

Items 4 and 5 in §2 (reads replacing layers; α − 1 curvature and jump order) are correctly marked weaker, and are not sold as field predictions. Fine.

---

## 3. Nothing presented as new that is already in the repository

The tree search in §0 is real: free prices, Master Theorem (ii) as price-free, diagnosis from signs and ratios, S1 / S3, CT24, CT12, CT14–CT15, L1–L3, the Sella–Hirsh lag, OPEN_WORK §8, R1–R3, and Topkis / Milgrom–Shannon are already on the record. The note presents a classification, not a new law. The CT13 curvature identity is labeled a corollary of results already in `THEORY.md` line 343 and `theory/MASTER_EQUATION.md` line 179. T27's P3 failure is already official. The Beekman / Dornhaus re-verification is of numbers the shortlist had left unchecked, not a new empirical claim. No existing claim is re-labeled as new.

---

## 4. Beekman, Dornhaus, DOIs, and fetched sources

All five DOIs returned a Crossref works record this session:

| DOI | Crossref issued | Title / bibliographic check |
|---|---|---|
| 10.1073/pnas.161285298 | 2001-08-07 | Beekman, Sumpter & Ratnieks, *PNAS* 98:9703–9706, *Phase transition between disordered and ordered foraging in Pharaoh's ants* — matches |
| 10.1093/beheco/arj036 | 2006-01-18 | Dornhaus, Klügl, Oechslein, Puppe & Chittka, *Behav. Ecol.* 17:336–344 — matches |
| 10.1534/g3.116.030890 | 2016-08-01 | Sung et al., *G3* — matches; PDF not re-opened (the note does not re-copy the table) |
| 10.1073/pnas.0501865102 | 2005-06-24 | Sella & Hirsh, *The application of statistical physics to evolutionary biology* — matches |
| 10.1098/rspb.2024.1606 | 2024-10 | Lee, Flack & Krakauer, *Constructing stability: optimal learning in noisy ecological niches*, vol. 291 — matches |

Beekman: PMC HTML at `https://pmc.ncbi.nlm.nih.gov/articles/PMC55516/` opened this session. The quoted sentences are in the text: "colonies of 600 ants or fewer cannot form a trail toward a feeder, whereas larger colonies can"; "The independent discovery rate (α) was only 0.0052 per ant per min."; Fig. 1 illustrative rates α = 0.021 and 0.0045, β = 0.00015, *s* = 10; for colonies of 100–600 ants, pooled mean ± variance 0.6 ± 1.36; hysteresis tested at 300 and 700 ants. (The paper's Fig. 1 prose says "α = 0.021 ants per min," while the model section defines α as "the probability per min per individual"; the note uses the model unit. Not a wrong number.) The conclusion drawn — existence of a threshold is not a result for CT14, and Beekman's own model already predicts one — is right.

Dornhaus: author PDF fetched from the cited URL, 338,189 bytes, SHA-256 `e741fb3333d441fc59079774183c67198da05562c96e1b832dcc33a0506a098e`, matching the note. Abstract: "Colony size, a factor often suspected to influence recruitment evolution, had no significant effect." Results: simulations with 10, 100, 1000, and 10,000 bees; "no significant correlation between foraging success/bee and colony size … without recruitment (all *r*² < .03, all *p* > .26) or with recruitment (all *r*² < .06, all *p* > .13; all *n* = 40)." Discussion: "Colony size, however, did not affect foraging success per individual or the benefits of recruitment in our model." The reading — a model, not a field series, not a score of Lemma B3 or CT15, and a problem for treating raw worker count as *N* — is right.

InventoryBench: dataset page HTTP 200; "five weekly observations" for real-article training context is on the page; GitHub API lists 200 directories under `benchmark/real_trajectory/lead_time_0`; sample `test.csv` is the stated Git LFS pointer (`oid sha256:c20af82a247266903aee0965a0a0c6570b04aa0c5ebc145e7487540f55cf1c0b`, size 7183). SE(α̂) ≈ 1/√*M* and *M* ≈ 400 for a ±0.1 interval are in `measurement/estimators/RESULTS.md`. The conclusion that this is not a test of CT12 (assigned costs, no observed selected `T*`) is right. No qualifying public dataset was found; that report is not overclaimed.

---

## 5. Bottom line, CORE, law sentence, locked rows

The bottom line is honest and not overclaimed. "The law is testable in the field without absolute (*h*, *w*) **in principle**, and only on a short list" is immediately qualified: no qualifying system with public no-account data scores one of the distinctive claims, the bottleneck has narrowed but has not been cleared, and "the law is not shown to be field-testable, with or without absolute prices." E. coli remains the best qualification prospect and still lacks a sourced σ and *T*_red; the Ni et al. 2020 collapse risk is left in place. Stakes *w* have never been measured validly; the note does not change that. The file is not a lock, not a prereg, and not a kill or a pass.

`CORE.md` is unchanged (SHA-256 above). The law sentence is unchanged, in `CORE.md` line 24 and `THEORY.md` line 41: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." No locked row is re-scored. OPEN_WORK §8 only adds a pointer to this file.

---

## 6. Checkers and pytest

`python3 tools/check_open_work.py` PASS (union missing from OPEN_WORK.md: 0). `python3 tools/check_consistency.py` PASS (0 FAIL; 23 frozen-record INFO hits; soft length WARNs on THEORY.md and README.md already present on `main`). `python3 -m pytest tools/ -q` at nice 19: **146 passed** in 2:36.

---

## Issues

**Should-fix before merge**

1. **S1 — PF8 / §0 state S3's `T*` exponents as refresh-rate exponents, with the wrong signs.** `theory/GENERAL_THEOREM.md` line 313 gives −*p*/(1+*pH*) on σ and 1/(1+*pH*) on *c*/*w* for the interval `T*`. Refresh-rate exponents are the negatives. Fix the wording to interval / `T*`, or flip both signs. PF7's look-rate signs are already correct; do not leave PF8 inconsistent with them.

2. **S2 — Credit prior art for the qualitative ruin-binding reversal, then state the remainder.** In §2 item 1 and §3.1, name Stephens 1981 and Caraco, Martindale & Whittam 1980 (energy-budget rule: risk preferences flip when a starvation threshold binds) and Dall & Johnstone 2002, doi 10.1098/rstb.2002.1061 (information gathering is a luxury under starvation risk; sampling falls as reserves fall). Then state what remains distinctive: the comparative static in the stake *w* of *S* + *w E*, with the reserve-pays-*J* / *w*²-variance mechanism. The scoped "expected-cost optimizers without a *w*-dependent feasible set" sentence can stay. Verify the new DOI on Crossref when added.

**Nits (fix if touching the file; not merge-blocking alone)**

3. PF7 cites THEORY line 101 for failure of the 1/α *elasticity* with read noise or a world that has its own time scale. Line 101 is the CT24 *share* failure. Cite the CT12 exact-reset-read setting instead.

4. PR10 cites `theory/LAYERS.md` line 53; the (*C*/*h*)^{1/3} *L*^{2/3} scaling and the withdrawn-as-store-count remark are at line 57.

5. PF10's "small-ρ exponent stays price-free" with *h* > 0 is true, but THEORY line 357 has a case split (stays −(1−*b*)/(1−*a*) if *a* > *b*; becomes −1 if *a* ≤ *b*). A half-sentence would be more precise.

6. PR11 calls "real internal prices equal multipliers" a conjecture (CX5). THEORY line 101 says that identity is a definition, and that the testable content is that real systems allocate so as to satisfy the *K* − 1 equalities. Align the wording.

---

This review does not merge the PR.
