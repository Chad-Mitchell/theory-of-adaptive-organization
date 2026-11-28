# Independent hostile review of draft PR #150

Read-only review of commit `ac8c2b5` on `layer-count-rule-2026-11-21`, parent `c92886a`. Sunday 22 November 2026. Computations at nice 19. The six DOIs in `measurement/LAYER_COUNT_RULE.md` §6 were resolved on the Crossref API on 22 Nov 2026; all six match the note, and the JSTOR alias for Kass & Raftery resolves to the same article. The reviewer wrote none of the draft, made no commit on the draft's files, and did not merge.

**NOT READY.** Three blockers. The hull identity and the peaked arithmetic are right. The observation procedure is not one procedure, and the exactness sentence copied into `THEORY.md` is the bare biconditional that the corrected statement of L1 on `layer-convexity-2026-11-21` (`9070f20`) withdraws.

## What was re-derived

**Forward direction.** Write \(d_K=\varepsilon_{K-1}-\varepsilon_K\) and \(J(K)=K+R(1+\varepsilon_K)\) for \(R\ge 0\). Then \(J(K)-J(K-1)=1-R d_K\). If the decrements are non-increasing, this difference is non-decreasing, so \(J\) strictly falls on exactly the steps with \(R d_K>1\) and does not fall after the first step that fails that test. The from-0 count \(K^\star_0(R)=\#\{K\ge 1: R d_K>1\}\) is that prefix, and it is the leftmost minimizer. A tie \(R d_K=1\) leaves \(J\) flat; the strict inequality keeps the leftmost index, which is what `argmin_J` and `hull_increment` return. Checked on 400 random non-increasing decrement sequences, seven values of \(R\) including 0, and on \(\varepsilon=(1,0.5,0)\) at \(R=2\), where \(J=(4,4,4)\), the count is 0, and the leftmost argmin is 0. The \(K^*=0\) hole is real: on \(\varepsilon=(1,0.4,0.15,0.05,0)\) at \(R=0.5\), \(R d_1=0.3<1\), the from-0 count and the argmin are 0, and N60 as written returns 1.

**Converse.** The bare "iff" is false. For \(d=(-2,-1)\), so \(\varepsilon=(-3,-1,0)\), the decrements increase, \(R d_K>1\) never holds, \(K^\star_0(R)=0\), and \(J(0)=-2R\) is the unique minimizer for every \(R\ge 0\). That is the counterexample in the corrected L1. The code does not mis-count it: `is_convex` is false, so `predict_count` takes the hull, which also returns 0. The procedure is safe. The sentence that exactness holds if and only if the decrements are non-increasing is not.

Under positive pairwise-distinct decrements the converse is true, and it is the order-statistic argument, not the adjacent interval. If \(d_m<d_{m+1}\), then \((m,\varepsilon_m)\) lies strictly above the chord from \(m-1\) to \(m+1\), so \(J(m)>\min(J(m-1),J(m+1))\) for every \(R>0\) and \(m\) is never a minimizer. Order the decrements \(d_{(1)}>\cdots>d_{(n)}>0\). For \(R\in(1/d_{(m)},1/d_{(m+1)})\) the count equals \(m\). That \(m\) is not a minimizer. Checked on \((1/3,2/3)\), \((0.1,0.2,5,6)\), \((10,9,8,0.1,0.2)\), and \((0.2,0.05,0.1,3)\): on each order-statistic interval the count equalled the ascent index and the argmin was a different index.

**Hull.** The lower-hull walk with the strict inequality returns the leftmost argmin for an arbitrary real sequence. A non-vertex lies strictly above a chord, so its \(J\) is strictly above the corresponding convex combination of the endpoints. Hull slopes are non-decreasing, so the first edge that fails \(R(\varepsilon_{k_i}-\varepsilon_{k_{i+1}})>(k_{i+1}-k_i)\) is the stopping edge, and equality keeps the left vertex. Checked on 3,000 random sequences (lengths 1–15, \(R\) up to 80) and on three constant or collinear ties: 0 disagreements with `argmin_J`.

**Peaked example.** Cells \(W=(0,1,0)\) with weights \((2,1,1)\). The \(K=0\) excess is \(\sum\mu W^2=1\). The best one-band design covers the first two cells at level \(1/3\), cost \(2(1/3)^2+(2/3)^2=2/3\), terminal cost 0. Two bands isolate the peak and the excess is 0. Decrements \(1/3\) then \(2/3\). At multiplier 3 the reduced costs are \((3,3,2)\): the from-0 count is 1 (only the second step has product strictly above 1) and the argmin is 2. `predict_count` returns that pair and the hull. \(E_\infty=\sum\mu W(1-W)/2=0\) on these cells, so this curve is the excess \(E_K-E_\infty\), and the multiplier is \(w/h\), not \(R=w E_\infty/h\). Putting the same numbers in as \(\varepsilon\) shifts \(J\) by the additive constant 3 and does not change the argmin or the differences. The reported 1 and 2 are the right pair for \(w/h=3\). The symbols in the note are the wrong names (should-fix 4).

**Observation versus prediction.** `detect` and `count_layers` take the record, the band, and fit settings. They do not call `predict_count`, `J_factory`, or `argmin_J`. The words "price", "argmin", and "spectrum" occur in those functions only in the docstring that denies them. `RESULTS.json` is the synthetic self-check. N56's row text, N60's row text, and CX1's row text are identical to `c92886a`. No sentence in the diff says a real system has been counted. The E. coli sentence says the published kernel was not selected by this rule.

**DECIDED.** The status vocabulary is "a naming or method decision, not a claim about the world." N65 is that decision. The row says no system has been counted and that N56 stays OPEN. DECIDED is the right word. The identities are not a new claim about nature; the false biconditional is a wording error inside the method note, not a reason to mark the row PROVED or OPEN.

**Sentence and locks.** The Part 2 sentence is one copy, the same bytes, in `THEORY.md`, `CORE.md`, `README.md`, and `theory/SELECTION_AXIOMS.md`:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

`CORE.md` and `theory/SELECTION_AXIOMS.md` are identical to `c92886a`. The diff does not touch a preregistration, a lock, a hash file, or `figures/face_systems.py`. That file's SHA-256 is still `00f6f25d796bbd1862f6ad9f04ef53bd986185f1177052339632e20b15095377`.

**DOIs (Crossref, 22 Nov 2026).** Fox 1966, *Management Science* 13(3):210–216, Bennett Fox. Hua & Sarkar 1990, *IEEE Trans. Acoustics, Speech, and Signal Processing* 38(5):814–824. Golub & Pereyra 1973, *SIAM J. Numerical Analysis* 10(2):413–432. Kass & Raftery 1995, *JASA* 90(430):773–795, both `10.1080/01621459.1995.10476572` and `10.2307/2291091`. Istratov & Vyvenko 1999, *Review of Scientific Instruments* 70(2):1233–1257. Gavish & Donoho 2014, *IEEE Trans. Information Theory* 60(8):5040–5053. Titles, years, volumes, and start pages match §6.

**Merge with current `main` (`dc7d731`).** `git merge-tree --write-tree HEAD origin/main` exits 0. The only file both sides edit is `OPEN_WORK.md` (this branch's T15, main's T19 from PR #147). It auto-merges: both rows are present, and there are no conflict markers. `THEORY.md`, `CLAIM_MAP`, `STATUS.md`, `README.md`, and `tools/test_brief.py` are untouched on `main` since `c92886a`.

## Blockers

**1. `measurement/LAYER_COUNT_RULE.md:48`, `THEORY.md:59`, `figures/face_placements.md:186`, `tools/layer_count_rule.py:220-224`.** Three selection rules. The note selects the largest degree that lowers BIC by at least 10 against every lower degree, and it starts at degree 0. THEORY §3 and the face-placement steps, which the note calls the unchanged v2.5.2 rule (`LAYER_COUNT_RULE.md:44`, `figures/face_placements.md:172`), accept \(K+1\) over \(K\) only, and they start at \(K=1\). The code selects the smallest \(K\) such that every higher degree has BIC strictly above \(\mathrm{BIC}(K)-10\).

On BIC \((100,89,80,75)\) the sequential rule and the note's rule return 1, and the code returns 2. On \((100,95,80)\) the sequential rule returns 0, and the note's rule and the code return 2. A class cannot preregister "the" gate. Degree 0 matters: a flat record has a count, and the canonical sentence has no degree 0.

Replace the selection sentence in all three documents with:

```markdown
Fit degrees 0 through K_max. Degree 0 is always eligible. Accept degree K>0 only if it lowers BIC by at least 10 against every lower degree, and select the largest such degree. A rhythm may enter as a jump of 2.
```

Change `detect` to that rule (largest \(K\) with \(\mathrm{BIC}(K)\le\mathrm{BIC}(j)-10\) for every \(j<K\)). Delete "the observation steps below are unchanged" at `figures/face_placements.md:172`, and delete "The steps are the v2.5.2 rule" at `measurement/LAYER_COUNT_RULE.md:44`. Add a unit test on the two BIC paths above.

**2. `tools/layer_count_rule.py:226-228` and `:331-343`; the rule those lines contradict is `measurement/LAYER_COUNT_RULE.md:49`, `THEORY.md:59`, and `figures/face_placements.md:188`.** `detect` merges in-band poles before it returns. `count_layers` classifies `states_merged`, including each unit record. Close local and shared poles are one pole before the class split, and the second merge has nothing left to keep apart.

Zero noise, band \((1,300)\), pooled time constants 10 and 25 (ratio 2.5). `detect` recovers both poles and merges them to \(\sqrt{250}\approx 15.811\). `count_layers` with two isolated records at time constant 10 returns \(K_\mathrm{obs}=1\), class local. The same path on 5 and 80 returns \(K_\mathrm{obs}=2\), local and shared. "Both" survives only when the ratio is already past the merge. `tools/test_layer_count_rule.py` calls `classify_local_shared` on hand-built states and never calls `count_layers` with `unit_records`.

Classify `states` after the band cut and before `merge_close_states`, on the pooled record and on each unit record. Merge only inside a class. Add the 10-and-25 case as a test that expects one local pole and one shared pole.

**3. `THEORY.md:59`, `measurement/LAYER_COUNT_RULE.md:13`, `measurement/LAYER_COUNT_RULE.md:73`, `measurement/CLAIM_MAP_v2.md:88`, `OPEN_WORK.md:62`.** These say the from-0 count is exact for every \(R\) if and only if the decrements are non-increasing. Corrected L1 (`theory/LAYER_CONVEXITY.md` on `9070f20`, §1) says the forward direction, and says the converse needs positive pairwise-distinct decrements (distinctness with the threshold decrement positive is enough). It gives \(d=(-2,-1)\) as a non-convex sequence on which the count still matches. Line 86 of the note has the qualified converse's conclusion and does not construct the interval. The order-statistic step is the part that shows the count equals \(m\).

Replace the exactness sentences with L1's statement, including the counterexample, and replace the converse sentence at `measurement/LAYER_COUNT_RULE.md:86` with:

```markdown
If the decrements are non-increasing, J(K)−J(K−1)=1−R d_K is non-decreasing, so K*_0(R) is the leftmost minimizer for every R≥0. Conversely, if the decrements are positive and pairwise distinct and some d_m<d_{m+1}, order them d_(1)>⋯>d_(n)>0. For R in (1/d_(m), 1/d_(m+1)) the from-0 count equals m. The point (m, ε_m) lies strictly above the chord from m−1 to m+1, so m is never a minimizer. Without those side conditions the biconditional is false: d=(−2,−1), ε=(−3,−1,0), is not convex, and K*_0(R)=0 is the unique minimizer for every R≥0. The count used in the procedure is K*_0, not N60 as written.
```

The procedural sentence in row N65 ("the procedure uses the from-0 count when the decrements are non-increasing, otherwise the hull") can stay. It describes the branch in `predict_count`, which is safe on the counterexample.

## Should-fixes

**`measurement/LAYER_COUNT_RULE.md:11` and `tools/layer_count_rule.py:347-353`.** A relay finding does not change \(K_\mathrm{obs}\). `relay_class` returns "relay" only when every baseline pole matches the bypass set. `relay_test` then labels every matched pole "layer", and the filter keeps those poles. On a one-pole record passed as both baseline and bypass, the class is "relay" and the kept degree is the baseline degree. The count is a pole count, so a level with no pole of its own was never going to be added. Say that, and delete the filter, or name a pole the bypass record is supposed to remove. The sentence "drop relay-only poles" describes a step the code does not perform.

**`tools/layer_count_rule.py:33`, `:64-68`, `:92`, `:116-128`, `:133-149`, `:170-174`, and `measurement/LAYER_COUNT_RULE.md:50`.** Several choices that change the count are not in the procedure. \(K_\max=5\). The BIC is computed after decimation to 800 samples. The pencil uses window \(n/3\) and clips rates to \([0.05/T,\,3/\Delta t]\); the variable projection uses \([0.02/T,\,4/\Delta t]\). An optimizer exception keeps the seed. The non-pencil starts are an all-real grid and one pair seeded at period \(T/5\); a second rhythm is present only if the pencil returns it. `in_band` counts a pair when the decay time or the period lies in the band, so a decay of 0.01 with period 10 is in band \((1,300)\), and so is a decay of 100 with period \(10^{-4}\). There is no integrator basis, and the rate bounds exclude a pole at 0, so "an integrator with a filter counts 2" is not an operation of this fitter. Name each of these as a locked constant, or drop the claim. State the band test for a pair (both time constants, or one named one).

**`measurement/LAYER_COUNT_RULE.md:80` and `:88`.** The ill-conditioning is named, the factor 3 is called a choice, and the Hankel matrix is correctly kept out of \(K_\mathrm{obs}\) because its entries are dependent. The parenthetical at line 80 still cites Istratov & Vyvenko as the source of the merge. Their paper shows that the resolvable ratio of two decay constants depends on the signal-to-noise ratio and the sample size; it does not give the factor 3. Kass & Raftery's "very strong" grade is a grade for \(2\ln B_{10}\) under regularity. Close poles make the information matrix singular, a smooth kernel sampled at 800 points is not an iid sample of size 800, and a failed `least_squares` call is not the maximum likelihood. "Tends to under-count" is not a result in this note: the detection tests use relative noise \(10^{-3}\), or one pair at ratio 1.5 that the merge forces to one. Move the citation to the ill-posedness sentence, say the factor is a precommitted resolution rather than their limit, and delete the Bayes-factor identification and the under-count sentence, or mark both as untested.

**`measurement/LAYER_COUNT_RULE.md:63`.** Call \((1,\,2/3,\,0)\) the excess \(E_K-E_\infty\), and call 3 the ratio \(w/h\). \(E_\infty=0\) for \(W\in\{0,1\}\), so \(\varepsilon_K=E_K/E_\infty-1\) and \(R=w E_\infty/h\) are not defined. The from-0 count is still 1 and the argmin is still 2 at \(w/h=3\).

**`STATUS.md:3`.** The clause "CLAIM_MAP v2.71 (this branch, not yet merged)" is false on this branch. `c92886a` is the merge of that note, and it is the parent of this commit and an ancestor of `origin/main`. `check_fresh` still passes, because `2eeab30` is inside the five-commit window (`dc7d731 c92886a 2eeab30 c04cedd d34df95`). Replace the clause with the merged SHA.

## Nits

- `fit_degree` takes `rng` and does not use it. Passing `seed` does not change the fit.
- The merge uses a time-constant ratio strictly below the factor (`layer_count_rule.py:250`). The relay match uses `<=` (`:286`). A ratio of exactly 3 is two poles in the merge and one pole in the relay test.
- "Rises afterwards" at `measurement/LAYER_COUNT_RULE.md:86` fails on the flat tie above. \(J\) stays level when \(R d_K=1\). The leftmost count is still right.
- This run of `pytest -q tools` is 193 passed and 1 skipped (`tools/test_lean.py:101`, Lean 4 / lake is not installed), not 194 passed. The skip is the pre-existing Lean test.

## Commands

All at nice 19, after installing NumPy 2.5.5, SciPy 1.18.1, pytest 9.2.0, and SymPy 1.14 into the user site. The tree was left clean apart from this review.

| Command | Result |
|---|---|
| `python3 tools/check_fresh.py` | RESULT: PASS. STATUS pointer `2eeab30`; window `dc7d731 c92886a 2eeab30 c04cedd d34df95` |
| `python3 tools/check_consistency.py` | RESULT: PASS (0 FAIL, 26 INFO). Tally 331. Section N has 64 rows, N1 through N65 |
| `python3 tools/check_open_work.py` | RESULT: PASS |
| `python3 -m pytest -q tools` | 193 passed, 1 skipped, 254 s |
| `git merge-tree --write-tree HEAD origin/main` | exit 0; `OPEN_WORK.md` auto-merged; no conflict markers |

Independent recomputation: forward direction 0 failures on 400 sequences; hull 0 failures on 3,000 sequences; from-0 count 1 and argmin 2 on the peaked excess at multiplier 3; \(d=(-2,-1)\) matches for every \(R\) tried and is not convex; the 10-and-25 pooled kernel is counted as one local pole.
