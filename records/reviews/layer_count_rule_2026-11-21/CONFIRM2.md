# Blind confirm of the should-fixes on draft PR #150

**Confirmer:** independent. Wrote none of `measurement/LAYER_COUNT_RULE.md`, `tools/layer_count_rule.py`, the tests, the claim-map row, `REVIEW.md`, or `CONFIRM.md`. The only file added by this confirm is this one. Nothing else was edited. The branch was not merged, and the draft was not marked ready.
**Date:** Sunday 22 November 2026.
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/150
**Head confirmed:** `664114bcf151452c583e5d653492315da0f0c1fa` on `layer-count-rule-2026-11-21`. The should-fix commit is `714a7eb`. `measurement/layer_count/RESULTS.json` was not used.

**Verdict: READY-WITH-FIXES**

No blockers. The seven should-fixes in `CONFIRM.md` are in the code and in the canonical note on the cases that confirm named. Three should-fixes remain. Two of them change \(K\). The third is a false sentence the fix pasted into the procedure.

## Should-fixes, rechecked

**1. Exactness converse.** Hand calculation, with \(J(K)=K+R(1+\varepsilon_K)\) and \(K^\star_0(R)=\#\{K\ge 1: R\,d_K>1\}\).

For \(d=(1,2,-1)\), so \(\varepsilon=(2,1,-1,0)\): the decrements are not all positive and not non-increasing. At \(R=3/4\), \(J=(9/4,\ 5/2,\ 2,\ 15/4)=(2.25,\ 2.5,\ 2,\ 3.75)\), the from-0 count is 1, and the leftmost argmin is 2. At \(R=3/5\), \(J=(9/5,\ 11/5,\ 2,\ 18/5)=(1.8,\ 2.2,\ 2,\ 3.6)\), the count is 1, and the argmin is 0. `n60_from` and `argmin_J` return those values.

For \(d=(-2,-1)\), so \(\varepsilon=(-3,-1,0)\): both decrements are negative, so the count is 0 for every \(R\ge 0\). \(J(0)=-2R\), \(J(1)=1\), \(J(2)=2+R\), so the argmin is 0 for every \(R\ge 0\). The sequence is not convex. The same pair of zeros holds on the integers \(R=0,\ldots,80\).

The exclusivity wording is gone. `THEORY.md:59`, `measurement/LAYER_COUNT_RULE.md:13`, `measurement/LAYER_COUNT_RULE.md:73`, the v2.76 note at `measurement/CLAIM_MAP_v2.md:86`, row N65 at `:479`, `OPEN_WORK.md:62`, and `tools/layer_count_rule.py:15-18` say the converse holds under positive, pairwise distinct decrements, with the parenthetical that distinctness and a positive threshold decrement are enough, and they keep \(d=(-2,-1)\) as the counterexample to a bare biconditional. A search of those files finds no "converse holds only" and no "converse needs". The \((2,1,-1,0)\) sequence is the test `test_l1_converse_not_only_positive_decrements` (`tools/test_layer_count_rule.py:89-102`) and the self-check at `tools/layer_count_rule.py:796-803`. `predict_count` still takes the hull whenever `is_convex` is false, so the wording change does not change a count. §5 at `measurement/LAYER_COUNT_RULE.md:86` still proves the all-positive case and the \(d=(-2,-1)\) witness; it does not claim that those side conditions are necessary.

**2. Matching rule, on the four named cases.** Executed `classify_local_shared` and `merge_classified` at factor 3. An edge exists only for the same kind and a strict ratio `< factor` (`_within_factor`, `tools/layer_count_rule.py:266-284`). The key is maximum cardinality, then the sum of log-ratios, then the sorted tuple of pooled decay times (`:326-332`).

| Case | Result |
|---|---|
| Pooled 10 and 40, unit 20, either list order | 10 local, 40 shared, \(K=2\) |
| Pooled 10 and 25, unit poles 7 and 12 | both local (the size-2 matching 10↔7 and 25↔12), merge to one pole, \(K=1\) |
| Pooled 10 and 25, units 10 and 16, either order | both shared, partner sets \(\{0\}\) and \(\{1\}\), unmerged, \(K=2\) |
| Pooled 10 and 25, both units 10 | 10 local, 25 shared, \(K=2\) |

Those four \(K\) values match the confirm. `THEORY.md:59` and `measurement/LAYER_COUNT_RULE.md:49` state the same objective. The code matches those two statements on these cases. It does not match `figures/face_placements.md:188`, and the tie-break is not a total order. Both are should-fixes below.

**3. Bootstrap.** `count_layers` (`tools/layer_count_rule.py:494-513`) draws a parametric resample of the pooled record and of each unit record, then appends `count_layers(...)["K_obs"]` with `n_boot=0`. With unit records present, that path classifies `states_in_band` and merges with `merge_classified`. It does not append `detect(...)["K_det"]`. `test_bootstrap_uses_classify_then_merge_count` passed. The procedure sentence that denies this interval is should-fix 1 below.

**4. Complex pairs.** `(τ, period)=(10, 10)` and `(12, 200)`: decay ratio 1.2, period ratio 20. `_within_factor` is false, `merge_close_states` returns both, and `max_cardinality_match` returns the empty set. The same predicate is what `merge_close_states`, `max_cardinality_match`, and `_matched` call. `THEORY.md:59`, `measurement/LAYER_COUNT_RULE.md:49`, and `figures/face_placements.md:188` require both time constants.

**5. Ratio at least the factor.** Time constants 10 and 30 at factor 3: `_within_factor` is false, `merge_close_states` keeps both poles, and `relay_class` returns `"layer"`. `THEORY.md:59`, `figures/face_placements.md:191`, and `measurement/LAYER_COUNT_RULE.md:51` say "at least the resolution factor (ratio ≥ factor)".

**6. Both nonlinear parameters.** `_theta_from_poles` clips the decay and `abs(imag)` to `[0.05/T,\ 3/\Delta t]` (`tools/layer_count_rule.py:105`, `:118`). `fit_structure` puts the same `[0.02/T,\ 4/\Delta t]` bounds on every component of `theta`, which is `log d` and `log ω` for a pair (`:129-132`). `measurement/LAYER_COUNT_RULE.md:48` says the pencil clip and the variable-projection bounds apply to the decay and the angular frequency.

**7. README.** `README.md:31` points at `measurement/LAYER_COUNT_RULE.md` and says the counting rule is that draft, which a class still has to preregister before a test.

## Should-fixes

**1. `measurement/LAYER_COUNT_RULE.md:52`.** Step 7 says the bootstrap loop percentiles the classify-then-merge count, and then says: "Until that is the interval, it is not an interval on K_obs." The loop in `tools/layer_count_rule.py:494-513` is that interval, and `out["interval"]` is what the function reports. Delete the "Until" sentence.

The same line says the point count is the selected degree. On the zero-noise pooled record with time constants 10 and 25 and no unit records, the BIC path is about \((-6412,\ -11269,\ -62644,\ -60792,\ -61569)\), `select_bic_degree` returns 2, and `count_layers` returns \(K_\mathrm{obs}=1\) because the within-factor merge runs. Say that the point count is \(K_\mathrm{obs}\) from steps 3–5 on the original record.

**2. `figures/face_placements.md:188`.** The step says a maximum-cardinality matching under the factor, then "ties broken by the smaller pooled time constant." It does not say that the rule first minimizes the sum of log-ratios. Read as written, every maximum-cardinality matching is a tie, and the smaller pooled time constant wins.

Pooled poles at 10, 14, and 30, one unit pole at 13, factor 3. The ratios are 1.3, \(14/13\approx 1.077\), and \(30/13\approx 2.308\), all below 3. The code minimizes the log-ratio, matches 14, and leaves 10 and 30 unmatched. Their ratio is exactly 3, so they stay unmerged, and \(K=3\). The face-placement reading matches 10. Then 14 and 30 are the same class with the same empty partner set and ratio \(30/14\approx 2.143<3\), so they merge, and \(K=2\).

Put the same sentence that is in `THEORY.md:59` and `measurement/LAYER_COUNT_RULE.md:49` in `figures/face_placements.md:188`: among maximum-cardinality matchings, smallest sum of log-ratios, then the smaller pooled time constant.

**3. `tools/layer_count_rule.py:326-332`, `measurement/LAYER_COUNT_RULE.md:49`, and `THEORY.md:59`.** The key `(-cardinality, sum of log-ratios, sorted pooled decay times)` does not order two matchings that share those three values. `min` then returns the first matching the depth-first enumeration emits, and that enumeration tries the skip branch before the match branch, so the later pooled index wins. Swapping the list order changes \(K\).

Pairs \((τ, \mathrm{period})=(10, 8),\ (10, 32),\ (10, 64)\), one unit pair \((10, 16)\), factor 3. The log-ratio costs of the first two against the unit are both \(\log 2\). The third has period ratio 4, so it has no edge. Order \((8, 32, 64)\) matches the period-32 pair; the unmatched periods 8 and 64 have ratio 8 and stay apart, so \(K=6\). Order \((32, 8, 64)\) matches the period-8 pair; the unmatched periods 32 and 64 have ratio 2 and the same partner set, so they merge, and \(K=4\).

After the sorted decay times, break the remaining tie by the sorted periods (a real pole has no period and sorts before any positive period). State that key in `measurement/LAYER_COUNT_RULE.md:49` and `THEORY.md:59`. Identical \((τ, \mathrm{period})\) copies stay interchangeable. The four named cases have distinct decay times, so this extra key leaves their \(K\) values as they are.

## Sentence, locks, checks

The BIC sentence

`Fit degrees 0 through K_max. Degree 0 is always eligible. Accept degree K>0 only if it lowers BIC by at least 10 against every lower degree, and select the largest such degree. A rhythm may enter as a jump of 2.`

is the same 211 bytes, once each, in `THEORY.md:59`, `figures/face_placements.md:186`, and `measurement/LAYER_COUNT_RULE.md:48`. `select_bic_degree` (`tools/layer_count_rule.py:220-230`) keeps the largest \(K>0\) with \(\mathrm{BIC}(K)\le\mathrm{BIC}(j)-10\) for every \(j<K\).

The hypothesis sentence is the same bytes, with the bold markers, in `THEORY.md:41`, `CORE.md:9`, `README.md:9`, `theory/SELECTION_AXIOMS.md:13`, and `theory/COADAPTATION.md:28`:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

The diff of those files from `b16193d` to this head does not touch that sentence.

`git diff --name-status b16193d..664114b` modifies no existing file under `reviews/` and no preregistration, lock, or hash file. It adds `reviews/layer_count_rule_2026-11-21/REVIEW.md` and `CONFIRM.md`. `figures/face_systems.py` is absent from that diff. Its SHA-256 is `00f6f25d796bbd1862f6ad9f04ef53bd986185f1177052339632e20b15095377`.

`origin/main` is `b16193d`. The live tally is 357. Section N has 65 rows, N1 through N65. N65 is **DECIDED**.

## Commands

NumPy 2.5.5, SciPy 1.18.1, pytest 9.2.0, and SymPy 1.14.0, user site. `origin/main` was fetched first; it is `b16193d`. `lake` was not run.

| Command | Result |
|---|---|
| `python3 tools/check_fresh.py` | RESULT: PASS. STATUS pointer `b16193d`; window `b16193d e88b692 8e829e5 fda5557 dc7d731` |
| `python3 tools/check_consistency.py` | RESULT: PASS (0 FAIL, 27 INFO). Tally 357. Section N has 65 rows, N1 through N65 |
| `python3 tools/check_open_work.py` | RESULT: PASS |
| `python3 -m pytest -q tools` | 243 passed, 1 skipped, 297 s |

The skip is `tools/test_lean.py:101`: Lean 4 / lake is not installed.
