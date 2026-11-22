# Independent hostile review: PR #155 (DS2, CA1 uniqueness, CA1b–c, CA7)

**Reviewer:** independent (wrote none of the PR, the `formal/lean/` library, or the OPEN_WORK T19 edit).
**Date:** Sunday 22 November 2026.
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/155
**Head:** `d549e60b0b3790384c8fc58cb5b7cf101bb451f4` on `lean-batch2-2026-11-21` (one commit on top of PR #152).
**Base:** `678c6d8713d2fb393286f760a401aa6c59872035` (`lean-layer-drift-2026-11-21`). Diff is 7 files, +1168/−8.
**Verdict: READY-WITH-FIXES**

No blocker. The branch builds. The new modules have no `sorry`. CA1 uniqueness is the paper’s statement. The other headline rows are weaker than the sentences they are mapped to, two of them are rearrangements, and every batch-2 README row except the uniqueness row calls itself Faithful.

`THEORY.md` does not restate DS2, CA1, CA1b, CA1c, or CA7. §4 points at the selection note’s excess and does not give these formulas. The sentences below are `theory/DRIFT_SELECTION.md`, `theory/COADAPTATION.md`, and CLAIM_MAP rows S2, U1, U2, and U11.

---

## What was checked

- `git diff --stat 678c6d8..d549e60` and a line-by-line reading of `GTAO/DriftSpeed.lean`, `GTAO/CoadaptationUnique.lean`, `GTAO/CoadaptationExcess.lean`, `GTAO/CoadaptationDrift.lean`, the README rows those files add, and the not-formalized bullets those rows rely on.
- Each headline statement against DS2 (`theory/DRIFT_SELECTION.md:120-122`), CA1 (`theory/COADAPTATION.md:53-55`), CA1b (`:63-73`), CA1c (`:75-79`), CA7 (`:216-226`), and CLAIM_MAP S2 (`measurement/CLAIM_MAP_v2.md:627`), U1 (`:653`), U2 (`:654`), U11 (`:663`).
- Whether a hypothesis is the paper’s input or a renaming of the conclusion, and whether a README “what is proved” cell is the type of the declaration it names.
- Whole-token scan of `formal/lean/GTAO.lean` and `formal/lean/GTAO/*.lean` (22 files) for `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `implemented_by`, with the same boundary regex as `tools/check_lean.sh`. Result: **0 hits**.
- Build, from this tree, after installing elan with toolchain `leanprover/lean4:v4.37.0-rc1`: `nice -n 19 tools/check_lean.sh` (the script also runs `lake` at `nice -n 19`). Mathlib `31ce06eaadf4a200c0e1407c5f10953cf606b8f8`. `lake build`: 5857 jobs, “Build completed successfully”. `AxiomAudit: OK (712 GTAO declarations; only propext, Classical.choice, Quot.sound)`. `check_lean.sh: OK`. The README’s 712 (`formal/lean/README.md:41`) matches that line.

The Part 2 hypothesis sentence is present once, byte-identical, in `CORE.md`, `THEORY.md`, `README.md`, and `theory/SELECTION_AXIOMS.md` at this head. This review does not edit it. `pytest` and the prose checkers were not re-run; the diff adds Lean and the mapping table.

Labels are the Lean conclusion against the prose sentence it is mapped to.

---

## Faithfulness

| Theorem | Mapped sentence | Label | Reason |
|---|---|---|---|
| `DriftSpeed.meanLag_abs` (`DriftSpeed.lean:128-133`) | DS2 / S2, `E[\|L_k\|] ≥ (\|v_k\|−v_max)t − \|L_k(0)\|` | **WEAKER** | From `\|θt−θ0\| < v_max t` the proof gets `\|meanLag\| ≥ B`. That is `\|E[L]\|` once `θt` is a mean. S2 states `E[\|L\|]`. `vMax` (`:39`) is never that `v_max`. |
| `DriftSpeed.ds2_excess` (`:176-185`) | DS2 / S2, `E[J−J*] ≥ ½ λ_min B²` | **WEAKER** | `hAbs`, `hSq`, and `hCost` (`:180-183`) are the three comparisons in the note’s proof, on free reals. `hCost` is `½ λ eSq ≤ eCost`, not a statement about `J`. |
| `DriftSpeed.halfWindow_diverges` (`:208-209`) | DS2 / S2, the time-averaged excess grows without bound | **WEAKER** | `(c/2)(α T/2 − β)² → ∞` for `α, c > 0`. The excess, the window, and the average are not in the type. |
| `Coadaptation.unique_stationary_prob` (`CoadaptationUnique.lean:102-104`) | CA1 / U1, uniqueness for an irreducible finite chain | **FAITHFUL** | Two stationary probabilities of a finite irreducible row-stochastic matrix coincide, by the max-ratio argument. |
| `Coadaptation.unique_global_balance` (`:395-400`) | same, continuous time | **FAITHFUL** | Uniformization at a rate above every exit rate transfers that uniqueness to global balance. |
| `Coadaptation.joint_connected` (`:435-438`) | CA1, the product of connected party graphs is connected | **FAITHFUL** | Single-party paths concatenate over a finite set of parties. |
| `Coadaptation.unique_gibbs_stationary` (`:546-555`) | CA1 / U1, uniquely `π ∝ e^{−Ψ}`, clocks cancel | **FAITHFUL** | Any global-balance probability equals `exp(−Ψ)/∑ exp(−Ψ)`. The right-hand side does not depend on `q`. |
| `Coadaptation.potential_shift_independent` (`CoadaptationExcess.lean:54-56`) | CA1b (1), `Ψ − β_i J_i` ignores `x_i` | **FAITHFUL** | The exact-potential equality, rearranged. |
| `Coadaptation.conditional_boltzmann` (`:63-66`) | CA1b (1), `π(x_i\|x_{−i}) ∝ e^{−β_i J_i}` | **FAITHFUL** | The unnormalized weight multiplies by `e^{−β_i ΔJ_i}` on a unilateral move. That is the identity the note cites. |
| `Coadaptation.ca1b_potential_excess` (`:80-84`) | CA1b (2), `E[Ψ]−Ψ* = d/2` | **WEAKER** | Assumes `ePsi = ½ Tr(H P)` and `H P = I`, and rewrites `Tr(I) = d`. |
| `Coadaptation.ca1b_team_split` (`:91-96`) | CA1b (3), gap plus `½ Tr(H_T (∇²Ψ)^{−1})` | **VACUOUS** | `hquad` and `hsc` already name the two summands. `_hcov` (`:94`) is unused, so `P = (∇²Ψ)^{−1}` is not in the conclusion. |
| `Coadaptation.ca1c_potential` (`:103-108`) | CA1c, `γ J_T` is an exact potential when `β_i s_i = γ` | **FAITHFUL** | `h_i` independent of party `i`’s own design is the hypothesis the algebra uses. |
| `Coadaptation.ca1c_gap_zero` (`:120-126`) | CA1c, the potential-to-team gap vanishes | **WEAKER** | `hmin` assumes `J_T(xPsi) = min J_T`. The summed-cost identity is exported only at `xPsi`. |
| `Coadaptation.ca1c_fraction` (`:136-140`) | CA1c, `(E[J_T]−J_T*)/J_T* = d/(2σ N_e)` | **WEAKER** | Assumes the absolute excess `d/(2γ)` and `γ = σ N_e / J_T*`, and cancels `J_T*`. |
| `CoadaptationDrift.virial_trace` (`CoadaptationDrift.lean:72-75`) | CA7 (1), the Lyapunov trace | **FAITHFUL** | From `V K Σ + Σ Kᵀ V = 2V + 2Q`, with `V` invertible and `Σ` symmetric, `Tr(K Σ) = d + Tr(V^{−1} Q)`. |
| `CoadaptationDrift.ca7_potential_excess` (`:131-140`) | CA7 (1), `E[Ψ]−Ψ* = ½(d + ∑_i Tr Q_{ii}/v_i)` | **FAITHFUL** | `trace_antisymm_symm` gives `Tr(A Σ) = 0`, and the excess is identified with `½ Tr(S Σ)` by `hexcess`. The conclusion is the matrix form `½(d + Tr(V^{−1} Q))`, which is the note’s sum when `V` is the party-speed diagonal. |
| `CoadaptationDrift.cex_party1_factor` (`:165-167`) | CA7 (4), `β_1 E[R_1]` | **WEAKER** | `Σ_{00} + Σ_{01} + Σ_{11}/4 = 15/16` for the stated matrix. The cost, the expectation, and `β` are not in the type. |
| `CoadaptationDrift.cex_party2_factor` (`:173-175`) | CA7 (4), `β_2 E[R_2]` | **WEAKER** | The same, for `9/16`. |
| `CoadaptationDrift.ca7_regret_not_naive` (`:181-183`) | CA7 (4) / U11, regret is not the naive scaling | **VACUOUS** | The type is `15/16 ≠ 1 ∧ 9/16 ≠ 1/2`. It does not mention `Σ`, `J`, `β`, or the naive formula. |

`ca1c_potential` does not state the note’s further sentence that the Nash points are the stationary points of `J_T` (`theory/COADAPTATION.md:75`). The README row does not claim that sentence.

CA1b (1)’s regret `E[R_i] = d_i/(2β_i)` (`theory/COADAPTATION.md:65`, CLAIM_MAP U2) is not a declaration. CA1b (2)’s companion `E[Φ]−Φ* = d/(2γ)` is not a declaration. CA7 (2) and CA7 (3) are absent, and `formal/lean/README.md:155` says so.

---

## Where an input restates the conclusion

- **`ca1b_potential_excess`** (`CoadaptationExcess.lean:82-83`). `hexcess` says the excess equals `½ Tr(H P)`. `hcov` says `H P = I`. The conclusion is `½ Tr(I) = d/2`. The Gaussian integral that CA1b (2) cites (`theory/COADAPTATION.md:73`, “SA1b for `Ψ` at `β = 1`”) is the hypothesis.
- **`ca1b_team_split`** (`:93-95`). `hquad` is `E[J_T] = J_T(x^Ψ) + ½ Tr(H_T P)` and `hsc` defines `scatter` as that same trace term. The conclusion is those two names added. `_hcov` would have been the identification `P = (∇²Ψ)^{−1}`, and it is unused.
- **`ca1c_gap_zero`** (`:125`). `hmin : J_T xPsi = jTmin` is the potential-to-team gap set to zero. The conclusion is the summed party cost at that one state.
- **`ca1c_fraction`** (`:138-139`). `hexcess` is `E[J_T]−J_T* = d/(2γ)` and `hγ` is `γ = σ N_e / J_T*`. The displayed ratio is that pair with `J_T*` cancelled. `_hσ : 0 < σNe` (`:137`) is unused.
- **`ds2_excess`** (`DriftSpeed.lean:180-183`). `hAbs`, `hSq`, and `hCost` are Jensen, Cauchy–Schwarz, and the Rayleigh comparison, each on a real the caller supplies. `hCost` is not the literal conclusion `½ λ B² ≤ eCost`; the three together are the note’s proof with the expectations erased. `0 ≤ lamMin` allows the bound `0`.

`ca7_potential_excess` does not do this. `hexcess` identifies the excess with `½ Tr(S Σ)`, which the note takes from `Ψ = ½ zᵀ S z`, and `virial_trace` derives the rest from the Lyapunov equation. That is the DS1 pattern. `_hS` (`CoadaptationDrift.lean:136`) is unused; symmetry of `S` is not required for the trace split.

`meanLag_abs` does not do this. The speed bound is the note’s first sentence, taken as an input, and the lag inequality is derived. The derived inequality is the absolute value of the mean, which is the step before Jensen in `theory/DRIFT_SELECTION.md:122`.

---

## README cells that are stronger than the type

`formal/lean/README.md:121` ends “Faithful with disclosed inputs” for all three DS2 declarations. The proved cell is right about `\|E[L]\|` and about the algebraic half-window limit. It is ahead of the types when it says the excess is `≥ ½ λ_min B²` as if `eCost` were `E[J−J*]`, and when it attaches that row to S2. `formal/lean/README.md:154` then says “the lag, cost, and half-window divergence from that bound are formalized.” The time average of the excess is not a theorem.

`formal/lean/README.md:122` matches the uniqueness types, including “at most one” for a chain that is not handed a potential. Existence of some stationary law with no potential is the half the max-ratio argument does not give, and the row does not claim it. This cell can keep “Faithful”.

`formal/lean/README.md:123` says the Gibbs law “is conditionally Boltzmann”, that `E[Ψ]−Ψ* = d/2`, and that the team excess “is the potential-to-team gap + scatter”, and ends “Faithful”. The conditional sentence is `potential_shift_independent` plus `conditional_boltzmann`. The `d/2` line is the rewrite above. The team line is `ca1b_team_split`. U2’s regret `d_i/(2β_i)` is not mentioned, and `formal/lean/README.md:155` says CA1b is formalized.

`formal/lean/README.md:124` says the potential-to-team gap “vanishes” and states the fractional excess, and ends “Faithful with A2-L disclosed”. The gap vanishes in the type only because `hmin` assumes the minimizer equality. The fraction is the cancellation above. The note’s “equal `σ N_e`” derivation (`theory/COADAPTATION.md:75`) is not a theorem.

`formal/lean/README.md:125` states `E[Ψ]−Ψ* = ½(d + Tr(V^{−1} Q))` and the Lyapunov input. That matches `ca7_potential_excess`. The note’s displayed sum `∑_i Tr Q_{ii}/v_i` and the Hurwitz claim are not the type; the row does not pretend they are. “Faithful” fits this row.

`formal/lean/README.md:126` says `β₁ E[R₁] = 15/16 ≠ 1` and `β₂ E[R₂] = 9/16 ≠ 1/2`, “Faithful for the negative finding on the stated covariance”, and calls `Σ = [[5/4, −1/2], [−1/2, 3/4]]` “the note’s example”, with the Lyapunov check “the 2×2 arithmetic in the note”. None of that is a type:

- `cex_party1_factor` and `cex_party2_factor` are entry arithmetic on `cexCov`. The comment at `CoadaptationDrift.lean:163-164` is where `J_1` and `β₁ E[R₁]` appear.
- `ca7_regret_not_naive` does not refer to those lemmas.
- The note’s negative finding is `theory/COADAPTATION.md:230`: regrets `0.1330` and `0.3196` against the naive `0.1300` and `0.3500`. The datum is `tools/coadaptation_checks.py:903-916` (`S = [[2, 0.9], [0.9, 1]]`, `V = diag(1, 0.4)`, `Q = diag(0.3, 0.3)`). The Lean matrix is a different example.
- The parenthetical “Matrix application is not exposed in Lean 4.37” is not a description of this file. `virial_trace` (`:72-75`) multiplies matrices.

The expansion in the comment is the right one for that cost: `β₁ R₁ = (z₁ + z₂/2)²` gives `Σ_{00} + Σ_{01} + Σ_{11}/4`. By hand, with `V = I`, `K = S`, `Q = diag(1, 0)`, and this `Σ`, `SΣ + ΣS = [[4, 0], [0, 2]] = 2I + 2Q`. So the datum is a stationary covariance for that choice. Lean does not record the equality, and the note does not contain the datum.

---

## Issues

**Blockers:** none.

**Should-fixes:**

1. **`formal/lean/README.md:121` and `:154`; `formal/lean/GTAO/DriftSpeed.lean:128`, `:176-183`, `:208`.** S2’s lag is `E[\|L\|]`, its cost is `E[J−J*]`, and its last clause is the time average. Lean proves `\|E[L]\|` from a speed bound, chains three caller-supplied comparisons to a free real `eCost`, and proves that `(c/2)(αT/2−β)²` tends to infinity. Drop “Faithful”. In the proved cell, keep `\|E[L]\|`, name `hAbs`, `hSq`, and `hCost` as the cost inputs, and describe `halfWindow_diverges` as the limit of that expression. In `:154`, replace “the lag, cost, and half-window divergence from that bound are formalized” with the three statements that are actually types. `vMax` (`DriftSpeed.lean:39`) is unused by those types; either thread `Nμδ/(2d)` into the lag theorem or leave it out of the DS2 claim.

2. **`formal/lean/README.md:123` and `:155`; `formal/lean/GTAO/CoadaptationExcess.lean:80-96`.** `ca1b_potential_excess` specializes an assumed trace. `ca1b_team_split` renames its hypotheses, and `_hcov` (`:94`) is unused. U2 still contains `E[R_i] = d_i/(2β_i)` (`theory/COADAPTATION.md:65`), which is not a declaration and not in the not-formalized list, while `:155` says CA1b is formalized. Fix: state the `d/2` line as `Tr(I) = d` under those two inputs; either use `_hcov` in the team split or stop describing it as `½ Tr(H_T (∇²Ψ)^{−1})`; add the per-party regret, and `E[Φ]−Φ* = d/(2γ)`, to the not-formalized list. `potential_shift_independent` (`:54`) and `conditional_boltzmann` (`:63`) can stay as the conditional-Boltzmann sentence.

3. **`formal/lean/README.md:124`; `formal/lean/GTAO/CoadaptationExcess.lean:120-151`.** `ca1c_gap_zero` assumes the minimizer equality it is mapped to, and exports `∑_i J_i = J_T` only at `xPsi`. `ca1c_fraction` cancels `J_T*` between two inputs; `_hσ` (`:137`) is unused. The note’s equal-`σ N_e` condition (`theory/COADAPTATION.md:75`) is not a theorem. Fix: export the summed-cost identity for every state, say in the row that the gap-zero theorem assumes `J_T(xPsi) = min`, and describe the fraction as that cancellation. `ca1c_potential` (`:103`) is the clause that matches the note.

4. **`formal/lean/README.md:126` and `:155`; `formal/lean/GTAO/CoadaptationDrift.lean:148-183`.** The negative finding, as a type, is `15/16 ≠ 1` and `9/16 ≠ 1/2`. The covariance is not the note’s s8b datum (`theory/COADAPTATION.md:230`, `tools/coadaptation_checks.py:903`). Fix: prove `SΣ + ΣS = 2I + 2Q` for this `V = I`, `K = S`, `Q`, and `Σ`; define `β_i E[R_i]` as the quadratic forms in `cex_party1_factor` and `cex_party2_factor`; put `≠ 1` and `≠ 1/2` on those values. Until that is the type, the row should say that two entry polynomials equal `15/16` and `9/16`, that those rationals differ from `1` and `1/2`, and that the Lyapunov check and the regret reading are comments. Drop “the note’s example” and “Faithful for the negative finding”. `:155` should not call CA7 (4) formalized until that link is a theorem.

**Nits:**

5. **`formal/lean/GTAO/CoadaptationDrift.lean:136`.** `_hS` is unused. Symmetry of `S` is not used in `ca7_potential_excess`.

6. **`formal/lean/GTAO/DriftSpeed.lean:176`.** `hlam : 0 ≤ lamMin` includes the zero eigenvalue. DS2 takes `H` positive definite, so `λ_min > 0`.

---

## Conclusion

READY-WITH-FIXES. `unique_gibbs_stationary` is CA1’s uniqueness and the normalized Gibbs law, clocks included only through `q` and absent from the right-hand side. `virial_trace` and `ca7_potential_excess` are the Lyapunov calculation for CA7 (1), with the quadratic identification disclosed. `ca1c_potential` is the aligned-share potential. The DS2 row proves a mean-lag bound and two algebraic consequences, and the README calls the package S2. CA1b’s `d/2` and team split are renamings, and the per-party regret is missing from the not-formalized list. CA7 (4) is a pair of rational inequalities plus two matrix-entry evaluations, attributed to an example the note does not contain. `tools/check_lean.sh` exits 0, with 712 declarations. This review does not merge the draft.
