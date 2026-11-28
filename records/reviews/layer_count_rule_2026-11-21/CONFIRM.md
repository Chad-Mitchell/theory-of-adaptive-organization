# Blind confirm of draft PR #150

**Confirmer:** independent. Wrote none of `measurement/LAYER_COUNT_RULE.md`, `tools/layer_count_rule.py`, the tests, the claim-map row, or `REVIEW.md`. The only file added by this confirm is this one. Nothing was fixed. The branch was not merged.
**Date:** Sunday 22 November 2026.
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/150
**Head confirmed:** `0ae92a93044ffd6d4d0e48e417daba6becca857b` on `layer-count-rule-2026-11-21`. Parents `f64113d` (the NOT READY review of `ac8c2b5`) and `8e829e5` (`origin/main`, PR #145). Draft.

**Verdict: READY-WITH-FIXES**

The three blockers in `REVIEW.md` are cleared on the cases that review named. The BIC gate is one rule, the zero-noise 10-and-25 count is 2, and the exactness paragraph at `measurement/LAYER_COUNT_RULE.md:86` is the paragraph the review prescribed. Six should-fixes remain. The one that misstates a theorem is the word "only" on the converse. The one that can change \(K_\mathrm{obs}\) is the nearest-first match.

## Blockers, rechecked

**1. One BIC gate.** The sentence

`Fit degrees 0 through K_max. Degree 0 is always eligible. Accept degree K>0 only if it lowers BIC by at least 10 against every lower degree, and select the largest such degree. A rhythm may enter as a jump of 2.`

is the same 211 bytes in `THEORY.md:59`, `figures/face_placements.md:186`, and `measurement/LAYER_COUNT_RULE.md:48`. `select_bic_degree` (`tools/layer_count_rule.py:212-222`) keeps the largest \(K>0\) with \(\mathrm{BIC}(K)\le\mathrm{BIC}(j)-10\) for every \(j<K\), and `detect` calls it (`:247`). Degree 0 is the start value, so it stays eligible. On 3,000 random paths this is the same index as "largest \(K\) with \(\mathrm{BIC}(K)\le\min_{j<K}\mathrm{BIC}(j)-10\)". An accepted degree is therefore at least 10 below every simpler degree, and the largest accepted degree is the most complex model with that property. A jump of 2 is allowed because degree 1 does not have to pass.

| BIC path | Selected degree |
|---|---|
| (100, 89, 80, 75) | 1 |
| (100, 95, 80) | 2 |
| (100, 90) and (100, 90, 80), improvement exactly 10 | 1 and 2 |
| (100, 90+10⁻⁹) | 0 |
| (100, 50, 60, 40) | 3 |
| (100, 50, 60, 41) | 1 |
| (100) and (5, 5, 5, 5) | 0 |

`tools/test_layer_count_rule.py:213-223` covers the two required paths and the flat record.

**2. Classify, then merge.** `count_layers` classifies `states_in_band` from the pooled record and from each unit record (`tools/layer_count_rule.py:375-384`), matches one-to-one inside `classify_local_shared` (`:298-313`), and merges inside one class. Zero noise, band (1, 300), pooled time constants 10 and 25, two isolated records at 10: the fit returns both poles (BIC selects degree 2; the path is about −6412, −11269, −62644, …), `detect` merges them to \(\sqrt{250}\approx 15.811\) and reports \(K_\mathrm{det}=1\), and `count_layers` returns \(K_\mathrm{obs}=2\), local at 10 and shared at 25. One isolated record gives the same pair. Pooled 5 and 80 with isolated records at 5 also returns 2, local and shared. `test_classify_before_merge_10_and_25` asserts this.

**3. No bare exactness iff.** `measurement/LAYER_COUNT_RULE.md:86` is the paragraph `REVIEW.md` prescribed: non-increasing decrements make \(K^\star_0\) the leftmost minimizer; the converse is stated as an implication under positive pairwise-distinct decrements, with the order-statistic interval; \(d=(-2,-1)\), \(\varepsilon=(-3,-1,0)\), is the counterexample. Recomputed: that sequence is not convex, and the from-0 count and the argmin are 0 on 17 values of \(R\) from 0 to 80. The peaked excess \(E_K-E_\infty=(1,2/3,0)\) at multiplier \(w/h=3\) has \(J=(3,3,2)\), from-0 count 1, argmin 2, and `predict_count` takes the hull. The remaining "iff"s are definitions of the hull step (`LAYER_COUNT_RULE.md:60`, `layer_count_rule.py:481`), the cost-band predicate (`:527`), locality (`:296`), the relay label (`:332`), and `is_convex` (`:431`). None of them says the from-0 count equals the argmin if and only if the decrements are non-increasing.

## Should-fixes

**1. `THEORY.md:59`, `measurement/LAYER_COUNT_RULE.md:13`, `measurement/LAYER_COUNT_RULE.md:73`, `measurement/CLAIM_MAP_v2.md:90`, `measurement/CLAIM_MAP_v2.md:475`, `OPEN_WORK.md:62`, `tools/layer_count_rule.py:15-16`.** These say the converse holds only for, or needs, positive pairwise-distinct decrements. L1 (`theory/LAYER_CONVEXITY.md:11`, `:37-38`) and N64 say it holds under those conditions, and that distinctness with the threshold decrement positive is enough. The exclusivity is false. For \(d=(1,2,-1)\), so \(\varepsilon=(2,1,-1,0)\), the decrements are not all positive and not non-increasing. At \(R=0.75\), \(J=(2.25,2.5,2,3.75)\), the from-0 count is 1, and the argmin is 2. At \(R=0.6\) the count is 1 and the argmin is 0. `LAYER_COUNT_RULE.md:86` does not say "only", and the procedure still uses the hull whenever the decrements are not non-increasing, so this does not change a count. It does not match N64.

Replace "only for" and "needs" with "under", and add the parenthetical from L1: distinctness with the threshold decrement \(d_{(m)}>0\) is enough. Keep \(d=(-2,-1)\). Add the \((2,1,-1,0)\) sequence at \(R=0.75\) next to the existing counterexample test.

**2. `tools/layer_count_rule.py:298-321` and `measurement/LAYER_COUNT_RULE.md:49`.** Nearest-first one-to-one matching, then a within-class merge, has three failure modes the zero-noise case does not hit.

- Equal ratios follow list order. Pooled poles at 10 and 40, one unit pole at 20, both ratios exactly 2. Listed as (10, 40), 10 is local and 40 is shared. Listed as (40, 10), 40 is local and 10 is shared. Break ties by the smaller pooled time constant.
- Nearest-first is not a maximum matching. Pooled poles at 10 and 25, one unit with poles at 7 and 12. The nearest edge is 10↔12 (ratio 1.2), 25 is left shared, and the class split keeps \(K=2\). The matching 10↔7 and 25↔12 is inside the factor, both poles are then local, and the within-class merge (ratio 2.5) returns \(K=1\). State which matching the rule is, and implement that one.
- Units that disagree erase the split. Pooled poles at 10 and 25, unit poles at 10 and at 16. The unit at 16 is nearer to 25 (25/16 = 1.5625) than to 10 (1.6), so each unit matches a different pooled pole, both poles are labelled shared, and the merge returns \(K_\mathrm{obs}=1\). Both units at 10 return \(K_\mathrm{obs}=2\). Keep two pooled poles unmerged when the unit records match them to different partners.

**3. `tools/layer_count_rule.py:402-416` and `measurement/LAYER_COUNT_RULE.md:52`.** Step 7 says a parametric bootstrap of steps 3–5 is an interval on \(K_\mathrm{obs}\). The loop resamples the pooled record only and appends `detect(...)["K_det"]`, which merges before any class split and never sees `unit_records`. On the 10-and-25 case with two isolated records at 10, four draws at `seed=0` gave \(K_\mathrm{obs}=2\), bootstrap samples \([1,2,1,1]\), and interval \([1,2]\), at a residual scale of about \(10^{-17}\). Resample the pooled record and each unit record, and percentile the same classify-then-merge count. Until that is the interval, do not report it as an interval on \(K_\mathrm{obs}\).

**4. `tools/layer_count_rule.py:273`, `:304-305`, `:325` and `measurement/LAYER_COUNT_RULE.md:49`.** A complex pair is in band only when both the decay time and the period are in band (`in_band`, `:180-185`; the note's band cut at `:48`). Checked: \((\tau,\mathrm{period})=(0.01,10)\) and \((100,10^{-4})\) are outside (1, 300); (8, 12) is inside. The match and the merge then ignore the period. Two in-band pairs, decay times 10 and 12 and periods 10 and 200, merge to one pair (decay about 10.95, period about 44.7). Require both time constants of a pair to lie within the factor before a match or a merge.

**5. `THEORY.md:59` and `figures/face_placements.md:191`.** Both say a candidate level is a layer when a pole moves by more than the resolution factor. `measurement/LAYER_COUNT_RULE.md:51` and `_matched` (`layer_count_rule.py:325`) use ratio \(\ge\) factor, so a ratio of exactly 3 is a move. `relay_class` on time constants 10 and 30 returns "layer", and `merge_close_states` keeps both poles. Say "at least the resolution factor (ratio \(\ge\) factor)" in THEORY and in the face-placement steps. The relay result itself is right on the records that were run: the same kernel as baseline and bypass is "relay" and \(K_\mathrm{obs}\) stays 2; dropping one pole of a 10-and-60 kernel is "layer" and \(K_\mathrm{obs}\) stays 2.

**6. `measurement/LAYER_COUNT_RULE.md:48`, `tools/layer_count_rule.py:99-112` and `:123-124`.** The named constants match the code: \(K_\max=5\), BIC on at most 800 samples with stride \(\lceil n/800\rceil\), pencil on at most 1500 samples with window \(\lfloor n/3\rfloor\) of that series, pencil clip \([0.05/T,\,3/\Delta t]\), variable-projection bounds \([0.02/T,\,4/\Delta t]\), seed kept when `least_squares` raises, all-real grid plus one pair at decay \(3/T\) and period \(T/5\). The same clip and the same bounds are applied to the angular frequency, not only to the decay. Say that both nonlinear parameters are clipped. The in-band rule for a pair is the one in item 4, and it matches `in_band`.

**7. `README.md:31`.** The sentence still says the counting rule is a preregistered rule still to be finalized. THEORY §3 and the note call the method finalized as a draft that a class preregisters before a test. Point this sentence at `measurement/LAYER_COUNT_RULE.md` and say the method is that draft, not yet preregistered per class.

Prior art at `measurement/LAYER_COUNT_RULE.md:80` and `:88-100` is accurate. Istratov & Vyvenko are cited for ill-posedness of close time constants, and the factor 3 is a precommitted resolution rather than their limit. Kass & Raftery's 10 is a numerical threshold, and the note says it is not a regular Bayes-factor theorem here. Noisy under-counting is marked untested beyond the synthetic checks. The peaked example at `:63` and in `predict_count` is the excess \(E_K-E_\infty=(1,2/3,0)\) at multiplier \(w/h=3\).

## Merge, sentence, locks

`origin/main` is `8e829e5`. The v2.74 note is `measurement/CLAIM_MAP_v2.md:90`. N64 is unchanged from main and is **PROVED (in-model)**. S1 is **PRIOR ART**, S2 is **PROVED (in-model)**, S3 and S4 are **OPEN** (`:622-625`). N65 is **DECIDED** (`:475`). N56 and CX1 are **OPEN** and their row text matches `8e829e5`. N60 is unchanged, **PROVED (in-model) given convexity (numerical)**. Section N has 65 rows, N1 through N65. The live tally is 336 and `check_consistency` recomputed the same 336 from the rows (DECIDED 6, PROVED (in-model) 97, OPEN 87, PRIOR ART 34, and the other rows in the block at `:631-648`). The v2.74 note's 335 → 336 is the change from main's table. The v2.73 note still records the pre-merge arithmetic 330 → 331; that sentence is unchanged from `8e829e5`.

The Part 2 sentence is one copy, the same bytes, in `THEORY.md`, `CORE.md`, `README.md`, and `theory/SELECTION_AXIOMS.md`, and each copy matches `8e829e5`, bold markers included:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

The diff from `8e829e5` to this head contains no "bill", no preregistration, no lock, and no hash file. `figures/face_systems.py` is not in the diff. Its SHA-256 is `00f6f25d796bbd1862f6ad9f04ef53bd986185f1177052339632e20b15095377`.

`python3 tools/layer_count_rule.py` rewrote `measurement/layer_count/RESULTS.json` only in `runtime_s` (9.3 to 3.2). That file was restored before this confirm was committed. The prediction identities in the run were all true.

## Commands

All at nice 19, after installing NumPy 2.5.5, SciPy 1.18.1, pytest 9.2.0, and SymPy 1.14 into the user site. `origin/main` was fetched first; it is `8e829e5`.

| Command | Result |
|---|---|
| `python3 tools/check_fresh.py` | RESULT: PASS. STATUS pointer `8e829e5`; window `8e829e5 fda5557 dc7d731 c92886a 2eeab30` |
| `python3 tools/check_consistency.py` | RESULT: PASS (0 FAIL, 26 INFO). Tally 336. Section N has 65 rows, N1 through N65 |
| `python3 tools/check_open_work.py` | RESULT: PASS |
| `python3 tools/layer_count_rule.py` | prediction identities true, including the peaked pair (count 1, argmin 2) and \(d=(-2,-1)\); 3.2 s |
| `python3 -m pytest -q tools` | 209 passed, 1 skipped, 273 s |

The skip is `tools/test_lean.py:101`, Lean 4 / lake is not installed.
