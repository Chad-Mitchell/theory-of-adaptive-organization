# Second read: PR #305 (BICAUSAL Route A follow-up, BA-T1 and BA-T2)

Reviewed head `9eef004e1fd3eca3927899805924e8c115930902`, base main `9fd04514ee785521d6cdb6331d8cef39d28a888f`.

**Who read it.** The same agent that wrote the PR, in a separate hostile pass against the sources, with code written from scratch (`rev_checks.py`: no sympy, no `ba_lib.py`, its own Lyapunov solver). **This is not an independent review.** The ledger rows BAT1 and BAT2 keep "independent review pending", and CORE.md is not edited on the strength of this read.

**Date.** Friday 27 November 2026 (America/New_York).

## Checked, with different methods

1. **BA-T1 witnesses.** \(\Delta\) recomputed by central finite differences of numerically solved costs at \(\gamma=19/7\), \(c=-1/2\), \(g=3\): 18.22406, 19.20872 and 21.17804 for \(w_x=0.5,1,2\). Each matches the exact rationals in `RESULTS.md:9` to the digits printed (`rev_checks.out`).
2. **BA-T1 proof steps.** The stability domain of the drift \([[-a,ag],[\gamma c,-\gamma]]\) is \(\gamma>0\), \(gc<1\): the trace is negative, and the determinant \(a\gamma(1-gc)\) is positive. The set \(gc<1\) is star-shaped about the origin, since \(t^2gc<1\) for \(t\in[0,1]\), so the domain is connected. With player m two-dimensional and player w one-dimensional, a weighted potential needs the cross-partial vectors to be positively proportional, and \(\Delta\neq0\) rules that out. The analytic-continuation step is sound.
3. **BA-T2 designs.** For each confirmed \(\hat K^*\) row in `checks/ba_t2.out`, I rebuilt the per-member cost from the printed log-parameters: 2.424009, 5.294034 and 18.258173. These are below \(J_{\mathrm{dir}}\) = 2.464102, 5.324555 and 19.000000, and match the table. Summed per-coordinate heat equals the total entropy production \(\mathrm{tr}(F^\top D^{-1}FS)+\mathrm{tr}F\), so no heat term is missing.
4. **Level-heat closed form.** \(\dot Q_0=b_0^2av/((a+b_0)D_0)\) agrees with the Lyapunov value at three unrelated points.
5. **Scope wording.** I read RESULTS.md, the CLAIM_MAP rows BAT1 and BAT2 (`measurement/CLAIM_MAP_v2.md:960-961`) and the README row. Each says in-model, WORKED-CLASS-ONLY, an upper bound for BA-T2, and not Lean. None claims a field result, and none touches GR, QM, holography or forces.

## Findings (non-blocking)

- N1. In `RESULTS.md`, BA-T1's "fails S2 everywhere" is a little stronger than the proof. The proof shows \(\Delta\neq0\) on an open dense set and no weighted potential on any open set. The Limits paragraph already says this. A later edit could say "on every open set".
- N2. BA-T2's information is low: the exact optimum agrees with the PAPER approximation. This is already logged as process miss `BA-T2-ODDS`.
- N3. The comparator is the direct-tracker infimum only. A design with two levels, or with members that also read X, is not compared. That fits the stated scope and is not a defect.

## Blocking

None found by this pass. Merge is allowed under the repo procedure. The results stay marked pending independent review.

Blockers remaining: 0
