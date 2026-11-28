# Confirm review: Shannon core (PR #139) at e59fd20

**Reviewer:** blind confirm pass. Wrote none of `CORE.md`, `theory/SHANNON_2026-11-21.md`, `theory/FLUID_LAYERS_2026-11-21.md`, `tests/LOCK1/`, `theory/shannon_checks/`, the first review (`reviews/shannon_2026-11-21/REVIEW.md` at `7d8690c`), or the fix commit. Same bot family.
**Date:** Saturday 21 November 2026 (afternoon ET).
**Target:** PR #139, branch `shannon-core-2026-11-21`, head `e59fd2039de3d8355e780dce4d72b2eccf226cab`, parent `7d8690ce9d58992a27c838f31fdaf61965118474`.
**Scope:** read only. Nothing edited, committed, pushed, or merged. Compute at nice 19. Every DOI in `theory/SHANNON_2026-11-21.md` was resolved on Crossref in this session.

## Verdict: READY-WITH-FIXES

B1–B4 and S1–S6 from the NOT READY review are applied. S1, the support-function identity in S2, and the undominated / supporting-hyperplane statement in S3 re-derive, and the K=0 and Farrell checks pass. Two sentences are still false as written, so this is not READY.

1. The information-only gap is efficiency 0.9574, which is 4.26% on \(1-J_{\mathrm{floor}}/J\) and 4.45% above the floor. “Within 4.2%” was the old figure with \(h=0.1\) on both sides (efficiency 0.9585, gap 4.15%). Leaving \(h\) out of both sides is right. The numeral was not updated. `CORE.md:22`, `theory/SHANNON_2026-11-21.md:9`, `:21`, `:55`.
2. Theorem S2 defines \(J^*(p)=\inf\langle p,z\rangle\) and then says equality \(J^*=\min\langle p,z\rangle\) needs \(A=c\cdot r\) and \(L=0\). Those conditions are when the operational least cost equals that dual. `theory/SHANNON_2026-11-21.md:62`, with the same identification at `:10` and `CORE.md:24`.

## S1

Under S-A, \(L\ge 0\), and \(hK\ge 0\), \(J\ge\kappa I_{\mathrm{mem}}+c\,r+wD\). No layer term. For squared error on a scalar Gauss–Markov source, \(I_{\mathrm{mem}}\ge\tfrac12\ln(V/P)\), \(r\ge\tfrac12\ln(a^2+Q/P)\), and \(D=a^{2k}P+V(1-a^{2k})\). The closed form is that sum, minimized over \(P\). It is a lower bound whether or not one design meets both information bounds at the same \(P\).

Independent K=0 replay (\(a=0.9\), \(Q=1\), \(s^2=0.2\), \(\kappa=c=0.1\), \(w=1\), \(h=1\)): \(P=0.192678\), \(I=1.653732\), \(r=0.950225\), lead-2 \(D=1.936416\), \(J=2.196812<3.186825\) (retracted floor). Corrected floor \(2.186825\le J\). Lead 0: \(J=0.453074<1.417121\), corrected floor \(0.417121\). The script’s §7 and `tools/test_shannon_checks.py` match the review’s printed 2.197, 3.187, 0.453, and 1.417.

## S2

\(J^*(p)=-\sigma_{\mathcal F_W}(-p)\). Concave, positively homogeneous. On \(F=\{(1,1),(3,3)\}\) and on \(\{(1,1)\}\), \(J^*(p)=p_1+p_2\) for \(p>0\), so positive prices recover the free-disposal hull of the Pareto face. The envelope claim is the standard one where the derivative exists. A separate check of \(J_{\mathrm{floor}}\) at one interior \(w\) matched \(D^*\) to \(10^{-12}\). The committed §3 check is of \(J_{\mathrm{floor}}\), which the code header already says.

Exact fix for the false clause in `theory/SHANNON_2026-11-21.md:62`:

> \(J^*\) is that infimum. The operational least cost \(\min(\kappa I_{\mathrm{mem}}+hK+wD+A+L)\) equals \(J^*\) only if some minimizer has \(A=c\cdot r\) and \(L=0\). S-A gives only \(A\ge c\cdot r\), so the operational minimum can sit strictly above \(J^*\).

Use the same proviso where `CORE.md:24` and `theory/SHANNON_2026-11-21.md:10` call \(J^*\) the least cost.

## S3

(i) A linear-cost minimizer at strictly positive prices is undominated on the feasible set, hence \(\theta=1\) there. (ii) If that set is convex, every undominated point has a nonzero supporting price \(p\ge 0\). The note scopes both statements to the ruin-feasible set, says the cap need not preserve convexity, and says ruin is not determined by mean loss. `CORE.md:24` keeps that qualifier.

Farrell on \(C=\kappa I+c\,r\): independent values \(\theta=0.697879\), \(J_{\mathrm{floor}}/J=0.985378\), product \(0.693916\neq 0.985378\), \(C_{\mathrm{act}}=0.568034\), \(C_{\mathrm{min}}=0.389207\), \(\eta_A=0.981808\), \(C_{\mathrm{min}}/C=0.685183\). The script and the unit test pass.

## Deviations from the reviewer’s replacement text

1. **Accepted in scope.** The 4.2% comparison is information-only, \(h\) left out of both sides. Charging \(h\) only to the design gives efficiency 0.9325 at the same prices and is a different number. **The retained words “within 4.2%” are the defect above.** Exact fix: write efficiency \(J_{\mathrm{floor}}/J=0.9574\) (gap \(1-J_{\mathrm{floor}}/J=4.26\%\); the design costs 4.45% more than the floor).
2. **Accepted.** The ratio 1.0000 is claimed on the six simulated \(\kappa=0\), \(c>0\) prices. An independent grid gives 1.00000000 on all six. The three \(c=0\) points remain assigned.

## Store versus memoryless

No store-versus-memoryless condition, and no \(\Delta P(r)\) sufficient condition, is in the note or the checks.

## Other checks against the first review

- Hypothesis sentence, verbatim, in `CORE.md` and `history/2026-11-21_CORE_before_shannon.md`.
- Theory text uses “cost”.
- S4 caveats are back on `CORE.md`, including cymatics. The CT41 trichotomy matches the frozen page (“at most” for \(\le\)).
- `tests/LOCK1/PREREG.md` sha256 `2f9dd21891abe4a32200876c5c12f03dc5135bb52d4ec0aba2bc2ff587e58935` matches `PREREG.sha256` and is unchanged since `5f9f5be`. The fix commit does not touch a prereg.
- `RESULTS.md` says frequencies off by 2.6–66% (smallest relative error 0.0255). `lock1.json` minimum is 0.02554. D2 is marked as the same statistic as B1 at \(K_c=0.6\).
- Fluid-layer paragraph matches the S5 replacement. \(\tau=b^{*2}/\sigma^2=\sqrt{6k/(w\sigma^2)}\) matches CL19.
- Prior-art sentences for Palmer and Mattingly match S6. Palmer’s Crossref abstract and Mattingly’s abstract (Europe PMC; Crossref has no abstract) support those sentences. Mattingly is a chemotaxis bound.

Nits, not part of the verdict: “jointly tight curve” at `theory/SHANNON_2026-11-21.md:37` should say the two bounds are written in the same \(P\); the envelope parenthetical should say \(J_{\mathrm{floor}}\); the worked \(\theta=0.698\) is the factor to the information bounds, and joint reachability is still open in §3.

## Checkers

| Command | Result |
|---|---|
| `nice -n 19 python3 theory/shannon_checks/shannon_checks.py` | exit 0; stdout byte-identical to `shannon_checks.out`; `ALL PASS`; min efficiency 0.9574. Python 3.12.3, numpy 1.26.4. |
| `nice -n 19 python3 tools/check_consistency.py` | `RESULT: PASS` (0 fails; 23 frozen-record INFO) |
| `nice -n 19 python3 tools/check_open_work.py` | `RESULT: PASS` (union missing from `OPEN_WORK.md`: 0) |
| `nice -n 19 python3 -m pytest -q tools` | 149 passed, 1 skipped (`tools/test_lean.py:101`, Lean 4 / lake absent). Scipy 1.18.1 and sympy 1.14.0 installed for this run. The two tests added in the fix are why this is 149 rather than the first review’s 147. |

## DOIs

Crossref this session: Tatikonda, Sahai & Mitter 2004, 10.1109/TAC.2004.834430. Tanaka, Kim, Parrilo & Mitter 2017, 10.1109/TAC.2016.2601148. Kostina & Hassibi 2019, 10.1109/TAC.2019.2912256. Stavrou, Tanaka & Tatikonda 2020, 10.1109/TAC.2019.2941444. Sagawa & Ueda 2009, 10.1103/PhysRevLett.102.250602. Sagawa & Ueda erratum 2011, 10.1103/PhysRevLett.106.189901. Bialek, Nemenman & Tishby 2001, 10.1162/089976601753195969. Creutzig, Globerson & Tishby 2009, 10.1103/PhysRevE.79.041925. Sims 2003, 10.1016/S0304-3932(03)00029-1. Friston 2010, 10.1038/nrn2787. Farrell 1957, 10.2307/2343100. Shoval et al. 2012, 10.1126/science.1217405. Palmer, Marre, Berry & Bialek 2015, 10.1073/pnas.1506855112. Mattingly, Kamino, Machta & Emonet 2021, 10.1038/s41567-021-01380-3. Laughlin, de Ruyter van Steveninck & Anderson 1998, 10.1038/236. Bibliographic fields match the note.

The two defects and three nits were applied in the next commit.
