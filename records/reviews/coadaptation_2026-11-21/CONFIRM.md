# Blind confirm: PR #148 (co-adaptation)

**Confirmer:** independent. Wrote none of the note, the checks, or `REVIEW.md`. Part A was checked against the files at `c098e45` after reading the review. Part B was rederived from the generators and from Itô's formula, then compared with `tools/coadaptation_checks.py`.
**Date:** Sunday 22 November 2026 (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/148
**Head confirmed:** `c098e456d5b9226e2c3ec9d988eb23ecfee20527` on `coadaptation-2026-11-21`. Merge-base with current `origin/main` is `c92886af97425102878241740b093983885a0106`. Current `origin/main` is `dc7d731e465e24507b84de9e7b553675ebbf1312` (PR #147). Draft. Not merged.

**Verdict: READY-WITH-FIXES**

No blockers. The three blockers, the should-fix, and the three nits in `REVIEW.md` are fixed at `c098e45`. The new statements CA5, CA5′, CA6(a)(b), P1, P2, P3, the 2×2 refutation, CA7, and P4/F6 rederive, and the rerun matches the printed figures. One displayed limit does not: the 2×m family ratio is not the expression in `theory/COADAPTATION.md:170`, and with the barrier held at 10 it stays bounded as m grows. The bracket is still false without that display. The Part 2 sentence is byte-identical. No locked file moves. CX1 and CX2 stay OPEN.

## A. Prior review, item by item

`REVIEW.md` reviewed `6038f4f`, verdict NOT READY. This confirm is of `c098e45`.

1. **Fixed.** `theory/COADAPTATION.md:13`–`:15`. The display is reversibility (detailed balance with a positive π) if and only if the unilateral difference identity, and then, uniquely, π ∝ e^{−Ψ}. Line 51 states the same theorem. Line 57 says why π ∝ e^{−Ψ} alone is the wrong left-hand side, and names matching pennies. `THEORY.md:178` says the chain is reversible, and then uniquely Boltzmann, if and only if the β-scaled game is an exact potential game.
2. **Fixed.** `theory/COADAPTATION.md:67`–`:71`. The first term is the absolute gap J_T(x^Ψ) − min J_T. The parenthetical says CT31's price of anarchy is the ratio, bounded by (N+1)/(2√N) in that class, and that the absolute gap is (ratio − 1) J_T^⋆. S2 (`measurement/CLAIM_MAP_v2.md:616`) says the same.
3. **Fixed.** `THEORY.md:178`. The sentence now has four separate pieces. Reversibility is the iff. The excess d_i/(2β_i) is stated only when a confining quadratic potential exists, and the sentence points at F3 (g > 1, e^{−Ψ} not integrable) as the case where that fails. The excess is small relative to operating cost only when σ N_e ≫ d. Strongly monotone non-potential games are stable at every speed, with the excess controlled by the radial part of the split (CA2, CA5), which is a different case from the potential iff. Which real couplings are β-potential stays open, and the sentence says CX2 stays OPEN.
4. **Fixed (should-fix).** `STATUS.md:3`. v2.71 merged with PR #144 at `c92886a`. v2.72 is this draft. CX2 is still OPEN. The pointer `main` is `c92886a` sits in `check_fresh.py`'s five-commit window of current `origin/main` (`dc7d731 c92886a 2eeab30 c04cedd d34df95`).
5. **Fixed (nit).** `theory/COADAPTATION.md:242`. F2 is an unstable focus: trajectories spiral outward. The line says the linear model has no periodic orbit.
6. **Fixed (nit).** `theory/COADAPTATION.md:244` and S6 (`measurement/CLAIM_MAP_v2.md:620`). Asymptotically stable if and only if kτ is strictly below the Hayes number. Equality is a neutral oscillation.
7. **Fixed (nit).** `theory/COADAPTATION.md:315`. Fat-Hy O. Rajab, Olugbenga M. Anubi, Marcos M. Vasconcelos.

## B. New material

**CA5 / CA5′.** For dx = −V F(x) dt + √(2V) dW with F m-strongly monotone, F(x^⋆) = 0, and V = diag(v_i I_{d_i}) ≻ 0, the Lyapunov function ½(x−x^⋆)^⊤ V^{−1}(x−x^⋆) has generator −(x−x^⋆)·F(x) + d. The speed matrix cancels. Foster–Lyapunov gives a unique stationary law with finite second moments, the virial E[(x−x^⋆)·F(x)] = d, and E|x−x^⋆|^2 ≤ d/m. For a split F = ∇Ψ + R with Ψ convex and ∇Ψ(x^⋆) = 0, convexity gives E[Ψ]−Ψ^⋆ ≤ d(1 + ρ_in/m). When Ψ is quadratic, Ψ−Ψ^⋆ = ½(x−x^⋆)·∇Ψ, so

E[Ψ]−Ψ^⋆ = d/2 − ½ E[(x−x^⋆)·R(x)],

and the radial moduli give (d/2)(1 − ρ_out/m) ≤ E[Ψ]−Ψ^⋆ ≤ (d/2)(1 + ρ_in/m). A purely tangential remainder, including a linear antisymmetric field, leaves the excess at d/2. An independent Lyapunov solve with S = [[2, 0.3], [0.3, 1]] and a rotation of size 1.5 gave excess 1 at V = I and excess 1 at speeds (10^{−3}, 50), while E|x|^2 moved from 1.442 to 2.019. Both sit under d/m. Per-party regret ≤ L_i^2 d / (2 μ_i m) is the standard strong-convexity bound |∇_i J_i|^2/(2μ_i) plus the Lipschitz bound and E|x−x^⋆|^2 ≤ d/m. Under translation drift with covariance 2Q dt the generator trace is d + Tr(V^{−1} Q), and every bound keeps its form with that replacement. The s6b rerun: virial 2.815 against 2.8, E|z|^2 = 2.113 ≤ 4.677, E[Ψ] = 1.412 inside [1.128, 1.672].

**CA6(a)(b).** Each directed tree has |S|−1 edges. Edgewise factors in [e^{−η}, e^η] put every tree weight, and therefore every W(x), in [e^{−a}, e^a] with a = (|S|−1)η. Normalizing costs another factor and gives e^{−2a} ≤ π_1/π_0 ≤ e^{2a}, and the same factor on the excess. The worst two-point weight ratio puts mass 1/(e^a+1) on the heavy value and yields total variation (e^a−1)/(e^a+1) = tanh(a/2). Three-point draws stayed under that value. CA6(b): a unique strict unilateral local minimum on a finite connected product is the global minimum, because every other state has a strictly lower neighbor and descent cannot cycle. Downhill edges have resistance 0, so the stochastic potential of that state is 0 and every other root pays a positive exit. Hence π_λ(x^⋆) → 1. The rerun goes from 0.144 at λ = 2 to 0.99993 at λ = 128.

**P1.** Differentiating π^⊤ L = 0 and the edge detailed balance gives ∂E[J]/∂γ_i = −a_i at a matched strength, with Σ a_i = Var_π0(J). The bracket holds to first order for every small mismatch if and only if every a_i ≥ 0. Commuting reversible generators are simultaneously diagonalizable and nonnegative, so each a_i ≥ 0; a separable cost is the example, and on a 3×3 separable well both coefficients were positive (0.168 and 0.082). A centered finite difference on the printed local landscape, using an independent Moran generator, matched −a_i to relative 4×10^{−11} and 3×10^{−9}. Raising γ_2 lifts E[J] above E_Gibbs(γ) by 1.560×10^{−7}, 1.566×10^{−6}, and 7.960×10^{−6} at ε = 0.01, 0.1, 0.5.

**The 2×2 bracket is false.** J = [[0.2487, 1], [0, 0.0161]] has one unilateral local minimum, at (1, 0). With c = (6.23, 60), N = 10, and clocks (1, 105.142), an independent least-squares stationary vector and the script's GTH vector agree to 1.5×10^{−15}. E_π[J] = 0.03728700. The matched Gibbs values are 0.00443848 at γ = 60 and 0.03272942 at γ = 6.23. The expectation sits 0.00455758 above the upper end, 16.11% of the bracket width. The note's 16.1% is that ratio.

**P2 and P3.** A beneficial Moran fixation probability is at least 1/N, so the steepest downhill edge contributes at least u_min θ (J−J^⋆)/N_max to the negative part of the generator. Uphill edges contribute U(x). Stationarity of J−J^⋆ gives the flux bound. The rerun: 400/400, 0 violations, median tightness 0.0579, max 0.4903. The parenthetical Nβκ → sup_{y>0} y^2/(e^y−1) equals 0.6476, so the note's ≈ 0.648 is that supremum. On a tree the cycle criterion is empty, clocks cancel in every edge ratio, and π ∝ e^{−Ψ_c}. The rerun's total variation is 6×10^{−17}.

**CA7.** The stationary covariance solves VKΣ + Σ K^⊤ V = 2V + 2Q. The trace, using Tr(AΣ) = 0 for antisymmetric A, is E[Ψ]−Ψ^⋆ = ½(d + Σ_i Tr Q_ii / v_i). The same identity on diagonal blocks needs V constant on each party's coordinates; antisymmetry of the similar matrix V^{1/2} A V^{1/2} makes the block traces match. Forty independent draws with two parties of dimension 2 and a full drift covariance had maximum absolute error 6×10^{−14} on both block virials and the potential excess. The mismatch bracket is CA3 applied to the Loewner bounds q_min V ≼ Q ≼ q_max V. The rerun: 2,000 trials, relative error 1.1×10^{−14}, 0 bracket violations. The negative finding is one counterexample, and one is enough: static regrets 0.1000 and 0.2000, and with this drift 0.1330 and 0.3196 against the uncoupled values 0.1300 and 0.3500.

**P4 / F6.** Resistances r = c_i (ΔJ)_+ are the logarithmic rates of the Moran fixation as λ → ∞: an uphill step is Θ(e^{−λ c_i ΔJ}) and a downhill step tends to 1, so clocks are Θ(1) and drop out of λ^{−1} log. The concentration on argmin SP_c is the Markov-chain tree theorem. The note credits it as an application of Young 1993 and Freidlin–Wentzell, in the bottom line (`:9`, `:24`), in the proof (`:246`), in the plain-words reading (`:255`), in the prior-art table (`:265`, `:282`), and in S12. It is not stated as a new method and not stated as a field result. For the printed 2×2, escape from A = (0, 0) costs c_1 · 1 and escape from B = (1, 1) costs c_2 · 0.7, and the third node attaches downhill, so the min-tree costs equal those escapes. At c = (1, 3), SP(A) = 2.1 and SP(B) = 1.0. The worse basin B is selected when 0.7 c_2 > c_1, i.e. c_2/c_1 > 1/0.7 = 1.42857…, printed 1.4286. The rerun slope λ^{−1} log(π_B/π_A) is 1.1000000000000001 at λ = 20 and 40 for clock ratios 1, 50, and 1/50. The threshold scan is π_B = 0.0266, 0.310, 0.707, 0.992 at c_2/c_1 = 1.3, 1.4, 1.46, 1.6.

**What the row statuses say.** S1–S6 and S8–S12 are PROVED (in-model). S7 is OPEN (`measurement/CLAIM_MAP_v2.md:621`). S7's open list is the complement of what CA5–CA7 and P1–P4 close: non-monotone games, tight finite-γ bounds, non-Brownian drift, dual control, Bode on argmin J. CX1 (`:506`) and CX2 (`:530`) are OPEN. The v2.72 note says no existing row changes status. The tally block is OPEN 86, PROVED (in-model) 106, total 342. `check_consistency.py` counted 342 rows against tally total 342. From the v2.71 baseline (OPEN 85, PROVED 95, total 330) the twelve new rows are eleven proved and one open.

**Wording.** Nothing in the new note calls a measured coupling a potential game or calls the hypothesis a law outside the required sentence. `check_consistency.py` reported 0 wording FAILs on 30 maintained documents. The count 1,155 is a report of exploratory draws and is not in the check script; this pass did not recompute it. The false-bracket claim does not use that count.

## Blockers

None.

## Should-fixes

1. `theory/COADAPTATION.md:169`–`:172`, repeated in S9 (`measurement/CLAIM_MAP_v2.md:623`). The display says that under γ_1 ε ≪ 1 ≪ γ_2 ε the ratio E_π[J] / E_Gibbs(γ_1) tends to (m + e^{−γ_1 Δ}) / (1 + e^{−γ_1 Δ}), and that this is unbounded in m.

   The states (0, j>0) at cost 10 remain in the weak Gibbs sum. With ε → 0 and γ_2 → ∞ at fixed γ_1, Δ, and barrier B = 10,

   E_π[J] → Δ e^{−γ_1 Δ} / (1 + e^{−γ_1 Δ}),

   E_Gibbs(γ_1) → [Δ e^{−γ_1 Δ} + 10(m−1)e^{−10 γ_1}] / [m + e^{−γ_1 Δ} + (m−1)e^{−10 γ_1}].

   At γ_1 = 1 and Δ = 0.5 the ratio of those two tends to 415.8 as m → ∞. The printed expression at m = 10^6 is 6.22×10^5. At the reported point m = 64 the finite chain (ε = 10^{−5}, c_2 = 10^6) has ratio 34.635, the ideal barrier-aware ratio is 36.75, and the printed expression is 40.215. The check line that says 34.64 is the finite-chain value. The arrow is a different claim.

   The bracket is false without this display. The 2×2 counterexample and the negative derivative already put E[J] above E_Gibbs(γ_min), and 34.6 > 1 does too. Suggested fix: put the barrier states into the Gibbs denominator, and state unboundedness only in the limit where those states are deleted or B → ∞ with m B e^{−γ_1 B} kept negligible against Δ e^{−γ_1 Δ}. In that limit the printed expression is the ratio, and it does grow with m.

## Nits

1. `theory/COADAPTATION.md:162` and `:198`. The printed sensitivity is a_2/Var = −0.0121. The check's own coefficients give a_2/Var = −0.01130 (a_2 = −1.559×10^{−5}, Var = 1.380×10^{−3}). The sign is what the argument uses, and the three excesses at ε = 0.01, 0.1, 0.5 match the note to the printed digits.
2. `measurement/CLAIM_MAP_v2.md:623`, the Why cell of S9. It names Candogan, Ozdaglar, and Parrilo 2013 as the tree theorem. Their paper is the near-potential comparison. The tree sum in the proof (`theory/COADAPTATION.md:154`) is Freidlin–Wentzell, Chapter 6, which is where the note points. The caveat on `:155` already says "compare" Candogan for near-potential Markov comparisons. The Why cell should say that.
3. `measurement/CLAIM_MAP_v2.md:625`. S11 writes the refuted per-party factor as (1 + D_i/v_i). The symbol D_i is not defined. The note's factor (`theory/COADAPTATION.md:218`) is 1 + Tr(Q_ii)/(v_i d_i).

## Hypothesis sentence and locked files

The Part 2 sentence is byte-identical, one copy each, bold markers included:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

`THEORY.md:41`, `CORE.md:9`, `README.md:9`, `theory/SELECTION_AXIOMS.md:13`, and the new copy at `theory/COADAPTATION.md:28`. The four canonical lines match `c92886a` byte for byte. `git diff --name-only c92886a...HEAD` is the twelve PR paths. A filter for prereg, lock, hash, and results names is empty. `core/bridge_2026-11-21/PREREG.md`, `core/bridge_2026-11-21/LOCK.txt`, `prereg/WIKIDATA-BAND/LOCK.txt`, `prereg/WIKIDATA-BAND/PREREG.md`, and `tests/EVO1/PREREG_EVO.md` match the blobs at `c92886a` and at `origin/main`.

## Merge with current main

No merge conflicts. `git merge-tree --write-tree HEAD origin/main` returned a tree. Since `c92886a`, `origin/main` has moved by the lean-core merge `dc7d731`. The only path both sides edit is `OPEN_WORK.md`: this branch rewrites the T12 row, and main rewrites the T19 row. Git auto-merges them. The merged file contains the T12 text (S1–S12, CX2 stays OPEN) and the lean-core T19 extension, with no conflict markers. Main's other paths (`formal/lean/**`, `reviews/lean_core_2026-11-21/**`, `tools/check_lean.sh`) are untouched by this PR.

## DOIs on Crossref, 22 November 2026

The three sources added for the new sections resolve. Titles, years, and containers match the reference list.

| Item | DOI | Result |
|---|---|---|
| Young 1993 | 10.2307/2951778 | H. Peyton Young, "The Evolution of Conventions." *Econometrica* 61, issue 1, January 1993. Crossref records page 57, the start page. The note prints 57–84. |
| Freidlin & Wentzell 1984 | 10.1007/978-1-4684-0176-9 | M. I. Freidlin and A. D. Wentzell, *Random Perturbations of Dynamical Systems*, 1984. |
| Freidlin & Wentzell 2012 | 10.1007/978-3-642-25847-3 | Mark I. Freidlin and Alexander D. Wentzell, same title, 2012 (3rd ed.). Chapter 6 is "Markov Perturbations on Large Time Intervals," which contains the invariant-measure argument the proof cites. |
| Candogan, Ozdaglar & Parrilo 2013 | 10.1016/j.geb.2013.07.001 | Ozan Candogan, Asuman Ozdaglar, and Pablo A. Parrilo, "Dynamics in near-potential games." *Games and Economic Behavior* 82:66–90, November 2013. |

## Commands and results

All repository commands were run from the repo root on `c098e45`, with `nice -n 19`. `python3 -m pip install --user pytest scipy sympy` pulled NumPy 2.5.5, SciPy 1.18.1, and pytest 9.2.0 (the image's NumPy was 1.26.4). Python 3.12.

- `git fetch origin main`. `origin/main` moved `2eeab30..dc7d731`.
- `git merge-tree --write-tree HEAD origin/main`. Clean tree. Auto-merged `OPEN_WORK.md`.
- Hypothesis bytes compared with `git show c92886a:PATH`. Equal on the four canonical lines. The new copy matches those bytes.
- Locked-blob comparison against `c92886a` and `origin/main`, five paths above. Equal.
- Independent recomputation (NumPy/SciPy, separate Moran rates and a least-squares stationary solve): 2×2 expectation, bracket, and 16.11% width; P1 finite differences; separable a_i > 0; entropic ratios at m = 2…10^6; sup y^2/(e^y−1) = 0.6476; total-variation probe under tanh(a/2); CA7 block traces at party dimension 2; pure-rotation excess 1 at two speed ratios. P4 slopes were read back from the script's GTH output to 16 digits. A least-squares solve of the λ = 40 balance equations is ill-conditioned in float64 and did not return a probability vector; GTH is the stable solver, and the pytest assertion is |slope − 1.1| < 10^{−9}.
- Crossref `GET /works/{doi}` for the four DOIs above.
- `nice -n 19 python3 tools/check_fresh.py`. `STATUS.md main is c92886a; window: dc7d731 c92886a 2eeab30 c04cedd d34df95`. `RESULT: PASS`. Exit 0.
- `nice -n 19 python3 tools/check_consistency.py`. THEORY v2.9; CLAIM_MAP v2.72; wording FAILs 0 on 30 maintained documents; rows counted 342, tally total 342. `RESULT: PASS`. Exit 0. Two advisory length warnings (THEORY main text 10703 words, README 1468), not failures.
- `nice -n 19 python3 tools/check_open_work.py`. `union missing from OPEN_WORK.md: 0`. `RESULT: PASS`. Exit 0.
- `nice -n 19 python3 tools/coadaptation_checks.py`. Exit 0 in 16.8 s. The figures quoted above are that run.
- `nice -n 19 python3 -m pytest -q tools`. 198 passed, 1 skipped, in 269.92 s. Exit 0. The skip is `tools/test_lean.py:101`, Lean 4 / lake is not installed. The note's 23 co-adaptation tests are inside the 198. The count 198 is 188 at the previous review plus the 10 tests added in `c098e45`.
