# Blind confirm of PR #203

Sunday 22 November 2026. Independent confirm of `cursor/acting-derivation-2d99` at head `a79d7b6d40623794f93c2898582d64bbf6153486`. The author's transcript was not read. `reviews/acting_derivation_2026-11-22/HOSTILE_REVIEW.md` (draft PR #205, cut from `d755e2c`) was read only after the checks below were finished. This file edits none of the draft. It does not push to that branch and it does not merge. No lake build.

**VERDICT: CONFIRM.**

Discrepancies: none.

The recomputation is `reviews/acting_derivation_2026-11-22/recompute.py`. Its log is `recompute.out`. It does not import `theory/acting_derivation_checks`.

## 1. Head

`git rev-parse HEAD` is `a79d7b6d40623794f93c2898582d64bbf6153486`. The subject is "Qualify the grid score and label R1' as a representation."

## 2. What was read before the recomputation

`theory/ACTING_DERIVATION_2026-11-22.md`, `theory/THEORY_ACTING_PROPOSAL_2026-11-22.diff`, `theory/acting_derivation_checks/acting_derivation_checks.py`, the locked protocol and its results, and the T47 row in `OPEN_WORK.md`. Theorem R1, Lemmas C, P, and C\(_\mathbb{Z}\), and the five-term display were read in `theory/REPRESENTATION.md` and `THEORY.md` §3 so the wording could be checked against those sources.

## 3. Recomputation

NumPy 2.5.5, SciPy 1.18.1, SymPy 1.14.0. Every symbolic identity below simplified to zero in SymPy from the Lyapunov equation and from the Gaussian conditional score.

### The \(b=0\) reduction

At \(b=0\) the cost coordinates are the five master-equation terms \(\kappa I_{\mathrm{mem}}\), \(hK\), \(w\,\mathbb{E}[\ell]\), \(A\), and \(L\). The effort coordinate is absent. That is the same list as THEORY §3, before minimization, with the ruin probability kept as a constraint. On the linear plant the same substitution gives \(\mathbb{E}[X^2]=D/a\), \(\mathrm{Sr}_X=0\), and \(\dot I_M\) equal to the exogenous Gaussian learning rate. The variance at \(b=0\) does not depend on \(K\).

### Lemma LG

The stationary moments solved from \(A\Sigma+\Sigma A^\top+2\mathrm{diag}(D,D_M)=0\) are the closed forms in the note. The bath rates, their sum, the weighted heat \(D\,\mathrm{Sr}_X+D_M\,\mathrm{Sr}_M\), and \(\dot I_M\) each reduce to the displayed rational functions. In steady state \(\dot I_X=-\dot I_M\). At parameters \((a,b,K,\gamma,c,D,D_M)=(1,1,2,1,1,1,1)\) the memory flow is negative while the \(b=0\) learning rate stays positive.

### Corollary LG-K

The heat derivative is

\[
\frac{\partial}{\partial K}(D\,\mathrm{Sr}_X+D_M\,\mathrm{Sr}_M)=\frac{b\bigl((D+D_M)c\gamma+2 D_M b K\bigr)}{a+\gamma}.
\]

For \(b>0\) and \(K\ge 0\), with the remaining parameters positive, every factor is positive, so the weighted heat increases with the gain. The unweighted sum \(\mathrm{Sr}_X+\mathrm{Sr}_M\) increases as well. The numerator of \(v'\), after cancelling the positive factor \(a+\gamma\), is the quadratic \(D_M b^3 c\, K^2+2 D_M a b^2 K-D b c\gamma^2\). The leading coefficient is positive and the constant term is negative, so there is one positive critical point. The denominator \(\gamma(a+\gamma)(a+K b c)^2\) is positive on \(K\ge 0\). Thus \(v'(0)<0\), and that critical point is a minimum. At \(b=0\), \(\mathrm{Sr}_M-\dot I_M\) factors into a ratio of positive terms, so the memory-bath energy flow is at least \(D_M\dot I_M\).

### Stationary cubic gains

The cubic costs were minimized on a no-flux Scharfetter–Gummel grid, \(N\) points on \([-L,L]\) in each coordinate. A degree-4 fit on \(\mathbb{E}[X^2]\) for \(K\in[0.20,0.27]\):

| \(N\) | \(L\) | \(K_E\) | one-sided slope of \(J_H\) at 0, step \(0.01\) |
|---|---|---|---|
| 200 | 4 | 0.232658 | 0.599631 |
| 200 | 5 | 0.232360 | 0.596196 |
| 200 | 6 | 0.232337 | 0.596233 |

\(K_E\) at \(N=200\), \(L=4\) rounds to \(0.2327\). Widening the box to \(L=5\) rounds to \(0.2324\). \(J_H\) at that grid is \(0.782287\) at gain 0, \(0.941241\) at \(0.23\), \(1.740103\) at \(1\), and \(7.192339\) at \(4\), so the heat-aware minimum on \([0,\infty)\) is \(K_H=0\). The one-sided slope rounds to \(+0.60\). The central slope at step \(0.001\) is \(0.595302\), which rounds to the same two decimals. The exact one-dimensional quadrature of the uncontrolled cubic is \(\mathbb{E}[X^2]=0.46791992\). The same grid at \(K=0\) returns \(0.467983\).

### Locked grid and the path gate

The preregistered Euler–Maruyama rule, `Generator(PCG64(20261122+index))`, \(dt=0.0002\), burn 40, record 800, reproduces `results.out` to twelve digits. The gate rate is \(1.973637317765\) against the Lemma LG value \(2\). The relative difference is \(0.01318134\), which the note rounds to \(0.013181\). The grid argmin is \(K_E=0.25\), \(K_H=0\), difference \(0.25\).

Batch means of the official record, blocks of 2 to 50 time units, give a standard error from \(0.126\) to \(0.142\) (relative \(0.063\) to \(0.071\)). Seeds `20261122+1` through `20261122+24` produce 8 misses of the \(0.05\) gate, sample standard deviation \(0.1269\) (relative \(0.0635\)). The neighboring window, indices 0 through 23, produces 7 misses and sample standard deviation \(0.1221\) (relative \(0.0610\)). The note states 8 of 24 and a standard error \(0.12\) to \(0.14\) (relative \(0.058\) to \(0.071\)). The count 8 is the count on indices 1 through 24, and the stated band covers these sample deviations and the batch standard errors. The relative difference \(0.013181\) is about one fifth of a relative standard error in that band.

The recorded \(\mathrm{Sr}_X=0.050189309209\) at zero gain estimates a stationary value of 0. The instantaneous observable at that equilibrium has standard deviation \(4.816\), so a record of length 800 does not pin the third digit.

## 4. Wording

The four checks hold, and no overclaim turned up.

- Theorem R1′ is titled "a representation theorem." The additive form is Theorem R1 on the product A7′ names. Debreu's theorem, the von Neumann–Morgenstern index, and the Cauchy lemmas (C, P, and C\(_\mathbb{Z}\), as the representation note states them) are marked **STANDARD**. The sentence that names the step proved on the page is the \(b=0\) reduction.
- Section 5 and T47 both keep the locked score as a score of the grid. Both say the fine spacing is \(0.25\), so \(K_E-K_H\ge 0.25\) on this grid is the same statement as \(K_E>K_H\). Both put the continuous gains \(K_E=0.2327\), \(K_H=0\) beside that score and say the continuous difference is below \(0.25\).
- Section 5 says the gate was underpowered and that meeting it is weak evidence. T47 says the relative difference \(0.013181\) sits inside a relative standard error of \(0.058\) to \(0.071\).
- The header calls the page a representation theorem, and says `THEORY.md` is not edited. `git diff 459e1fd HEAD -- THEORY.md` is empty. The proposal diff applies cleanly and is not applied. The cubic ordering is labeled a conjecture in the note and in T47.

The citations that carry equation numbers were checked against the open texts. Horowitz and Esposito, equation (10), is the split of \(\mathrm d_t I\), and equation (11) is the two nonnegative entropy-production lines. For one thermal reservoir they set \(\dot S_r=-\dot Q/T\). The last section says the continuous limit of their master equation would be a bipartite Fokker–Planck equation, and they do not carry out that limit. Sagawa and Ueda 2009, equation (4), is \(W^M_{\mathrm{meas}}+W^M_{\mathrm{eras}}\ge k_B T I\). Sagawa and Ueda 2010, equation (3), is \(\langle W\rangle\ge\Delta F-k_B T\langle I\rangle\); equation (4) is \(\langle e^{-\beta(W-\Delta F)-I}\rangle=1\); equation (6) is the efficacy \(\gamma\), which is not a feedback gain.

## 5. Crossref

Every DOI in the note resolves. Titles match the note. Fetched 22 November 2026.

| DOI | Crossref |
|---|---|
| 10.1017/ccol052123736x.010 | Debreu, "Topological methods in cardinal utility theory," in *Mathematical Economics*, pp. 120–132. `issued` is `[[null]]`. Author entries: Gerard Debreu, Gerard Debreu, Werner Hildenbrand. The empty year field is what the note records |
| 10.1515/9781400829460 | von Neumann and Morgenstern, *Theory of Games and Economic Behavior (60th Anniversary Commemorative Edition)*, issued 2007-12-31 |
| 10.1103/PhysRevX.4.031015 | Horowitz and Esposito, "Thermodynamics with Continuous Information Flow," *Physical Review X* 4 (2014) |
| 10.1103/PhysRevLett.102.250602 | Sagawa and Ueda, "Minimal Energy Cost for Thermodynamic Information Processing: Measurement and Information Erasure," *Physical Review Letters* 102 (2009) |
| 10.1103/PhysRevLett.106.189901 | Erratum of that paper, *Physical Review Letters* 106 (2011) |
| 10.1103/PhysRevLett.104.090602 | Sagawa and Ueda, "Generalized Jarzynski Equality under Nonequilibrium Feedback Control," *Physical Review Letters* 104 (2010) |

## 6. Preregistration, lock, and the hypothesis sentence

The blob of `theory/acting_derivation_checks/PREREG.md` is `847dc4174cd4dfd2a5ace7ff2538f606d6cde254` at `1271eb0` and at this head. Its sha256 is `7f3b0034de4bea307c4510ade0edde7ccae94ef413d397b52cd9976edb6084a2`, the digest in `LOCK.txt`. The blob of `LOCK.txt` is `a53542f05be5102f78b1f1f610f2be3cee87f540` at `977810f` and at this head. `git diff` of both files from those commits to this head is empty. At the lock, the tree contains `PREREG.md`, `LOCK.txt`, and the algebra script. It does not contain `run_locked.py`, `RESULTS.md`, or `results.out`.

The sentence

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

is byte-identical in `THEORY.md` and in the note. In `THEORY.md` it is wrapped in bold markers. `THEORY.md` at this head is byte-identical to `459e1fd`.

## 7. House checks

All at nice 19, from this head, before this confirm was added.

| Command | Result |
|---|---|
| `python3 tools/check_consistency.py` | `RESULT: PASS`. FAIL 0. Maintained docs 31, wording FAILs 0. CLAIM_MAP rows 392, tally 392. Advisory length warnings on THEORY (11134 words) and README (1476 words) |
| `python3 tools/check_open_work.py` | `RESULT: PASS`. Union missing from `OPEN_WORK.md`: 0 |
| `python3 -m pytest -q tools` | 261 passed, 1 skipped, 321.98 s, exit 0. The skip is `tools/test_lean.py`, because Lean 4 / lake is not installed |

A repo-root `python3 -m pytest -q` stops while collecting `reviews/night2/CAUSAL_NULL_INVARIANCE/run_test.py`, which imports numba. That file is outside the maintained suite and outside this draft. The suite above is the full `tools/` run.

## 8. The seven fixes in the hostile review

The review is of `d755e2c`. This head is the following commit, `a79d7b6`. Each required fix is present here, and the recomputation agrees with the numbers the review used.

1. **Section 5.** The locked score is stated as one fine step of \(0.25\), the same statement as \(K_E>K_H\) on this grid. The continuous gains \(0.2327\) and \(0\), the widened value \(0.2324\), the path estimate, the standard-error band, the count of 8 misses, and the zero-gain \(\mathrm{Sr}_X\) are in the paragraph. The paragraph also records the slope \(+0.60\) and says the gate was underpowered. Both agree with the recomputation and with the review's own standard error \(0.1414\) (relative \(0.0707\)) and its 8 misses out of 24.
2. **T47.** The row carries the prescribed sentences: grid score \(0.25\), one step, continuous gains \(0.2327\) and \(0\), difference below \(0.25\), and the relative difference inside a relative standard error of \(0.058\) to \(0.071\).
3. **Header and Theorem R1′.** The header says "A representation theorem, not a derivation from the drift, and not an adoption." The theorem label says the additive form is carried by Debreu, the von Neumann–Morgenstern index, and the Cauchy lemmas, marked **STANDARD**, and that the step proved here is the \(b=0\) reduction.
4. **Step 1.** The feedback rule enters only as \(b\,u\). \(F_0\), both diffusion coefficients, and the memory drift do not depend on \(u\). At \(b=0\) the joint law does not depend on \(u\).
5. **Bath-rate display.** The bytes of the display are `\mathrm{Sr}_X=\mathbb{E}[F_X^2+D\,\partial_X F_X]/D`.
6. **Lemma LG.** The closed forms are described as polynomial identities that reduce to the Lyapunov solution and to \(\mathbb{E}[F^2+D\,\partial F]/D\). The check script's five floating-point comparisons, and its symbolic residual, are labeled as checks. SymPy reduces those residuals to zero.
7. **Corollary LG-K.** The unweighted sum and the weighted heat are given separate monotonicity sentences. The derivative in §3 is the derivative of the weighted heat, which is the term in \(J_H\).

The review's recommended remarks on the erratum's POVM hypothesis, on Hildenbrand's name in the Debreu author array, and on the dictionary sum in the algebra script remain as descriptions of the page. The checked numbers and labels stand as recomputed above. The Crossref author array for Debreu contains Werner Hildenbrand, as the review says, and the year field is empty, as the note says.
