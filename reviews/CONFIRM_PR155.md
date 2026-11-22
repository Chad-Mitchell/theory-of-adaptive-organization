# Blind confirm: PR #155 at 32c17dd

**Confirmer:** independent. Wrote none of the PR, the `formal/lean/` library, the OPEN_WORK T19 edit, the fix commit `32c17dd`, or `reviews/lean_batch2_2026-11-21/REVIEW.md`.
**Date:** Sunday 22 November 2026.
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/155
**Head confirmed:** `32c17dd10bb5b1eb403d91587c95e68ac32f10ab` on `lean-batch2-2026-11-21`. Parent of the fix is the merge of main (`71f4747`); the formalization commit under review against `REVIEW.md` (`d3803be`, head `d549e60`, verdict READY-WITH-FIXES) is `32c17dd`. This confirm does not merge.

**Verdict: CONFIRMED-WITH-NITS**

No blocker. The branch builds. The axiom audit reports 745 `GTAO` declarations, and every one of them depends only on `propext`, `Classical.choice`, and `Quot.sound`. The theorems README and OPEN_WORK T19 label Faithful have types that match the sentences they are mapped to, with hypotheses that are satisfiable and conclusions that are real equalities or inequalities. The four WEAKER labels name the missing parts. One clause in the Faithful CA7 (4) cell describes a static-regret recovery whose declaration is a narrower arithmetic identity; that is a nit, recorded below, and the negative finding itself is a theorem on the note's s8b datum.

---

## What was checked

- `git show 32c17dd` and a line reading of `GTAO/DriftSpeed.lean`, `GTAO/CoadaptationUnique.lean`, `GTAO/CoadaptationExcess.lean`, `GTAO/CoadaptationDrift.lean`, `GTAO/Equipartition.lean` (`gibbs_excess_quadratic`), `formal/lean/README.md` rows 123–128 and the not-formalized bullets those rows rely on, and the T19 row of `OPEN_WORK.md`.
- Each Faithful statement against DS2 (`theory/DRIFT_SELECTION.md` §6), CA1 (`theory/COADAPTATION.md` §3), CA1b (`:63-73`), CA1c (`:75-79`), CA7 (`:216-230`), and CLAIM_MAP S2, U1, U2, U11.
- Whether a hypothesis restates the conclusion, and whether a README "what is proved" cell is the type of the declaration it names.
- An independent exact-rational solution of the s8b Lyapunov equation and of the party regrets, static regrets, and naive values (Python `fractions`, below).
- Whole-token scan of `formal/lean/GTAO.lean` and `formal/lean/GTAO/*.lean` for `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `implemented_by`, same boundary regex as `tools/check_lean.sh`. Result: **0 hits**.
- Build, from this tree, toolchain `leanprover/lean4:v4.37.0-rc1`, Mathlib `31ce06eaadf4a200c0e1407c5f10953cf606b8f8`: `nice -n 19 tools/check_lean.sh`. There is no `tools/check_lean.py`; the shell script is the checker, and `tools/test_lean.py` calls it. `lake build`: 5857 jobs, "Build completed successfully". `AxiomAudit: OK (745 GTAO declarations; only propext, Classical.choice, Quot.sound)`. `check_lean.sh: OK`. `formal/lean/README.md:42` and OPEN_WORK T19 both say 745. That matches this run.
- `python3 tools/check_fresh.py`, `python3 tools/check_consistency.py`, `python3 tools/check_open_work.py`, and `nice -n 19 python3 -m pytest -q tools`. Results in the last section.

The Part 2 hypothesis sentence is present once, byte-identical, bold markers included, in `CORE.md:9`, `THEORY.md:41`, `README.md:9`, and `theory/SELECTION_AXIOMS.md:13`. The same 103 bytes appear once in `theory/COADAPTATION.md:28`. This confirm does not edit that sentence.

---

## Declaration count

`formal/lean/scripts/AxiomAudit.lean` walks every constant whose module name has prefix `GTAO`, collects axioms, and rejects any axiom outside `propext`, `Classical.choice`, and `Quot.sound`. A `sorry` would appear as `sorryAx` and fail the script. The run on this head printed:

```
AxiomAudit: OK (745 GTAO declarations; only propext, Classical.choice, Quot.sound)
```

The author's count is the audit's count.

---

## Faithful theorems

Labels below are the Lean conclusion against the sentence in the theory note, read at the declaration, and checked against the README cell and the T19 clause that cite it.

### CA1 uniqueness — Faithful

`unique_stationary_prob` (`CoadaptationUnique.lean:102-104`) concludes that two stationary probabilities of a finite irreducible row-stochastic matrix are equal, by the max-ratio argument. Existence of a stationary probability for a chain that is not handed a potential is the half a spectral Perron–Frobenius theorem would add. The README cell (`formal/lean/README.md:124`) says "at most one", and it records that Mathlib has no spectral Perron–Frobenius theorem. OPEN_WORK T19 (j) names the same method.

`unique_global_balance` (`:395-401`) transfers that uniqueness across uniformization at a rate strictly above every exit rate.

`joint_connected` (`:435-438`) concatenates single-party paths over a finite set of parties. That is the connectedness of the Cartesian product the note uses.

`unique_gibbs_stationary` (`:546-555`) concludes that any global-balance probability equals `gibbsProb Ψ`, defined at `:467-469` as `exp(−Ψ) / ∑ exp(−Ψ)`. The right-hand side does not depend on `q`. `detailedBalance_gibbsProb` (`:494-507`) is the exported fact that this weight satisfies detailed balance when `Ψ` is an exact potential, so the clocks cancel in the usual way. The hypothesis is a stationary probability plus `LogLinearChain` plus the potential. It does not assume equality with the Gibbs weight.

**Witness.** One party, states `{0,1}`, both directed edges present, `β = 1`, `J = 0`, `Ψ = 0`, off-diagonal rate `1` in each direction. `LogLinearChain.ratio` holds because both sides equal `1`. `IsExactPotential` holds because both sides of `ΔΨ = β ΔJ` are `0`. The party graph is connected. `gibbsProb` is `(1/2, 1/2)`. A different probability, for example `(1/3, 2/3)`, fails global balance on this rate matrix, so the conclusion excludes it. The hypotheses do not contain the conclusion.

### CA7 (1) — Faithful

`virial_trace` (`CoadaptationDrift.lean:74-77`) takes the note's Lyapunov equation `V K Σ + Σ Kᵀ V = 2V + 2Q` (`theory/COADAPTATION.md:228`), with `V` invertible and `Σ` symmetric, and concludes `Tr(K Σ) = d + Tr(V⁻¹ Q)`.

`ca7_potential_excess` (`:133-147`) sets `K = S + A` with `Aᵀ = −A`, identifies the excess by `ePsi = ½ Tr(S Σ)`, and concludes `ePsi = ½(d + Tr(V⁻¹ Q))`. The trace of the antisymmetric part against a symmetric covariance is `trace_antisymm_symm` (`:56-69`). That is the note's proof of CA7 (1)'s excess, in matrix form. For the note's party-speed diagonal `V = diag(v_i I)`, `Tr(V⁻¹ Q)` is `∑_i Tr Q_{ii} / v_i`. The README cell states the matrix form and the Lyapunov input. It does not claim the Hurwitz sentence of CA7 (1); see nits.

`hexcess` names the quadratic-moment identification the note takes from `Ψ = ½ zᵀ S z`. It is not the conclusion `½(d + Tr(V⁻¹ Q))`.

**Witness.** Dimension `1`, `V = (1)`, `S = (1)`, `A = (0)`, `K = (1)`, `Q = (3)`, `Σ = (4)`. The Lyapunov equation is `2 · 4 = 2 · 1 + 2 · 3`. The excess input is `½ · 1 · 4 = 2`. The conclusion is `½(1 + 3) = 2`. Both sides meet because of the equation, and the input `2` is `½ Tr(S Σ)`, which is a different expression from `½(d + Tr(V⁻¹ Q))` until the trace identity is applied.

### CA1b shift, conditional Boltzmann, Gibbs excess — Faithful

`potential_shift_independent` (`CoadaptationExcess.lean:56-60`) is the exact-potential equality rearranged: `Ψ − β_i J_i` is unchanged by a unilateral update. That is CA1b (1)'s algebraic half (`theory/COADAPTATION.md:65`).

`conditional_boltzmann` (`:65-72`) concludes that the unnormalized weight `exp(−Ψ)` multiplies by `exp(−β_i ΔJ_i)` on that update. Together with the shift, the weight in party `i`'s coordinate is the Boltzmann factor of `J_i`. The conditional probability is that statement read on `π ∝ exp(−Ψ)`.

**Witness.** One party, states `{0,1}`, `β = 1`, `J(0) = 0`, `J(1) = 3`, `Ψ = J`. The potential equality on `0 → 1` is `3 = 1 · 3`. The Boltzmann conclusion is `exp(−3) = exp(−3) · exp(0)`.

`ca1b_potential_excess` (`:83-90`) is `Equipartition.gibbs_excess_quadratic` (`Equipartition.lean:319-326`) at `β = 1`, by a direct application with `(1 : ℝ)` and `norm_num` for `0 < 1`. The integrand is `Ψ exp(−(1 · Ψ))` over `exp(−(1 · Ψ))`, and the conclusion is `(d : ℝ) / (2 * 1)`. `gibbs_excess_quadratic` states `E[J] − J* = d / (2β)` for `J(x) = J* + ½ (x − x*)ᵀ H (x − x*)`, `H` positive definite, `d ≥ 1`, on Lebesgue measure. At `β = 1` that is CA1b (2): `E[Ψ] − Ψ* = d/2`, which the note calls "SA1b for `Ψ` at `β = 1`" (`theory/COADAPTATION.md:73`). The positive-definite quadratic is the hypothesis. The value `d/2` is the conclusion.

**Witness.** `d = 1`, `H = (1)`, which is positive definite (`x² > 0` for `x ≠ 0`), `Ψ* = 0`, `x* = 0`. The conclusion is `1/2`.

### CA1c potential and summed cost — Faithful

`ca1c_potential` (`:114-126`) concludes that `γ J_T` is an exact potential when `J_i = s_i J_T + h_i` with `h_i` invariant under party `i`'s own update and `β_i s_i = γ` for every party. The exponent potential in CA1 is `γ J_T`. The README states that, and it does not claim the note's further sentence that Nash points are the stationary points of `J_T`.

**Witness.** Two parties, `s_i = 1`, `β_i = 2`, `γ = 2`, `h_i = 0`, `J_T` any function of the joint state. A unilateral change of party `i` changes `γ J_T` by `2 ΔJ_T` and changes `β_i J_i` by `2 · 1 · ΔJ_T`.

`ca1c_summed_cost` (`:130-136`) concludes `(∑_i J_i)(x) = J_T(x)` at every state, from `h_i = 0` and `∑_i s_i = 1`. That is the note's sentence "the parties' summed cost is `J_T`" (`theory/COADAPTATION.md:75`). The sum of the shares is a hypothesis. The identity at a general state is the conclusion.

**Witness.** Shares `(1/2, 1/2)`, `J_T(x) = 4`, so `J = (2, 2)` and the sum is `4`. Replacing the share sum by `2` would make the sum `8`, so the hypothesis is doing the work.

### CA7 (4) / s8b negative finding — Faithful

The datum in `CoadaptationDrift.lean:161-199` is the datum in `tools/coadaptation_checks.py:901-918`:

- `S = [[2, 9/10], [9/10, 1]]`
- `w = [1, 2]`, `γ = 5`, so `β = γ/w = [5, 5/2]`
- `V = diag(1, 2/5)`, `Q = diag(3/10, 3/10)`
- `M_{ij} = S_{ij} w_i / γ`
- regret of party `i` is `½ (g_iᵀ P g_i) / M_{ii}` with `g_i` the `i`-th row of `M`
- naive value is `½ β_i⁻¹ (1 + Q_{ii}/V_{ii})`, which is the note's `d_i/(2β_i) (1 + Tr Q_{ii}/(v_i d_i))` at `d_i = 1`

`s8b_lyapunov` (`:203-207`) proves `V S P + P S V = 2V + 2Q` at every entry of

```
P = [[2323/1904, −603/476], [−603/476, 13757/4760]]
```

`mul2` (`:151-152`) is the ordinary 2×2 product, so the four entries are the matrix equation. `s8b_regret_party0` (`:209`) is `10643/80000`. `s8b_regret_party1` (`:212`) is `2557/8000`. `s8b_naive_party0` (`:215`) is `13/100`. `s8b_naive_party1` (`:218`) is `7/20`. `ca7_regret_not_naive` (`:232-235`) concludes

```
s8bRegret 0 ≠ s8bNaive 0 ∧ s8bRegret 1 ≠ s8bNaive 1
```

by rewriting to those four rationals. The Lyapunov certificate and the inequality are separate theorems. Neither assumes the other. The inequality is the note's negative finding (`theory/COADAPTATION.md:226` and the s8b sentence at `:230`) on this covariance.

**Independent recomputation** (exact rationals, symmetric Lyapunov solution of `V S P + P S V = 2V + 2Q`, unique because the 3×3 system on `(P_{00}, P_{01}, P_{11})` is nonsingular):

| Quantity | Value |
|---|---|
| `P_{00}`, `P_{01}`, `P_{11}` | `2323/1904`, `−603/476`, `13757/4760` |
| drift regret, party 0 and 1 | `10643/80000`, `2557/8000` |
| naive, party 0 and 1 | `13/100`, `7/20` |
| differences | `243/80000`, `−243/8000` |
| `1/(2β_0)`, `1/(2β_1)` | `1/10`, `1/5` |

The claimed `P` is the solution, and its residual against `2V + 2Q` is the zero matrix. `10643/80000 = 0.1330375` and `2557/8000 = 0.319625` are the note's printed `0.1330` and `0.3196`. The naive values are the note's `0.1300` and `0.3500`.

**Static regrets, recomputed and only partly formalized.** With `Q = 0` the same equation has unique symmetric solution `P_0 = S⁻¹ = [[100/119, −90/119], [−90/119, 200/119]]`. The quadratic-form regrets on `P_0` are exactly `1/10` and `1/5`, that is `1/(2β_i)`. That is the checker's `static_regret` against `static_pred` (`tools/coadaptation_checks.py:917-918`). See nit 1 for the Lean type.

**Witness for the negative finding.** The datum above. Both regrets differ from the naive values (`243/80000` and `−243/8000`). The definitions are the note's quadratic regret and the note's naive formula. No extra hypothesis is required.

---

## WEAKER labels

### DS2 — the label matches

`meanLag_abs` (`DriftSpeed.lean:128-133`) concludes `B ≤ |meanLag|` from `|θt − θ0| < v_max t`, with `B = (|v_k| − v_max) t − |L_k(0)|`. If `θt` is a mean position and the optimum is the deterministic ray `θ*(0) + v_k t`, then `meanLag` is `E[L]`. S2's lag sentence (`theory/DRIFT_SELECTION.md:120`, CLAIM_MAP S2) is `E[|L|]`. `vMax` (`DriftSpeed.lean:39`) is `N μ δ / (2d)` and is not an argument of the lag theorem. The speed bound is a free `vmax`.

`ds2_excess` (`:176-185`) takes `hAbs : |meanLag| ≤ eAbs`, `hSq : eAbs² ≤ eSq`, and `hCost : ½ λ_min eSq ≤ eCost`, with `0 < λ_min`, and concludes `½ λ_min B² ≤ eCost`. Those three comparisons are Jensen, Cauchy–Schwarz, and the Rayleigh bound, each on a real the caller supplies. `eCost` is not `E[J − J*]`.

`halfWindow_diverges` (`:208-209`) concludes that `(c/2) (α T/2 − β)²` tends to infinity for `α, c > 0`. The excess, the window, and the time average are not in the type. The scalar is the lower bound one would get by restricting the average to `[T/2, T]` if the excess were at least `c (α t − β)²` there. That reading stays in the comment.

README `:123` and OPEN_WORK T19 (i) say: the types bound `|E[L]|`; the cost bound is Rayleigh on a free quadratic; there is no time-average statement; `v_max` is a free parameter. That is what the three types are.

**Witness.** `θ0 = θ*(0) = 0`, `θt = 1`, `v_k = 3`, `v_max = 1`, `t = 2`. Then `|θt − θ0| = 1 < 2`, `B = 4`, and `meanLag = −5`, so `|meanLag| = 5 ≥ 4`. The conclusion is a bound on the absolute mean. S2's `E[|L|]` is a further step, supplied later as `hAbs` if the caller wants the cost inequality.

### `ca1b_team_split` — the label matches

`ca1b_team_split` (`CoadaptationExcess.lean:96-109`) takes the entrywise contraction `eJT = jTpsi + ½ ∑_{i,j} (H_T)_{ij} P_{ji}` and `HΨ P = I`, and concludes `P = HΨ⁻¹` together with

```
eJT − jTmin = (jTpsi − jTmin) + ½ Tr(H_T HΨ⁻¹)
```

The inverse step and the trace rewrite are proved. The Gaussian identification `E[½ δᵀ H_T δ] = ½ ∑ (H_T)_{ij} P_{ji}` is `hquad`, an input. README `:125` calls that input the reason the theorem is WEAKER, and the assumptions cell also records `HΨ P = I`. The conclusion is the trace form. It is not a copy of `hquad`.

**Witness.** `d = 1`, `H_T = (2)`, `HΨ = (4)`, `P = (1/4)`, `jTpsi = 3`, `jTmin = 1`, `eJT = 13/4`. Then `HΨ P = 1` and the contraction hypothesis is `3 + ½ · 2 · 1/4 = 13/4`. The conclusion is `P = 1/4` and `13/4 − 1 = (3 − 1) + ½ · 2 · 1/4`.

### `ca1c_gap_zero` — the label matches

`ca1c_gap_zero` (`:141-148`) calls `ca1c_summed_cost` and takes `hmin : J_T(xΨ) = jTmin`. The conclusion is `(∑_i J_i)(xΨ) − jTmin = 0`. The note's reason the potential-to-team gap vanishes is that the potential `γ J_T` shares its minimizer with `J_T` when `γ > 0`. That coincidence is `hmin`, an input. README `:126` says so. The summed-cost identity itself is the separate Faithful theorem, at every state.

**Witness.** Shares `(1/2, 1/2)`, `J_T(xΨ) = 4 = jTmin`, so each `J_i(xΨ) = 2` and the sum minus the minimum is `0`. Dropping `hmin` leaves the sum equal to `J_T(xΨ)`, which may sit above the team minimum.

### `ca1c_fraction` — the label matches

`ca1c_fraction` (`:154-169`) takes `E[J_T] − J_T* = d/(2γ)` and `γ = σ N_e / J_T*`, with `0 < J_T*`, and concludes `(E[J_T] − J_T*) / J_T* = d / (2 σ N_e)`. The proof cancels `J_T*`. A2-L and the excess `d/(2γ)` are inputs. README `:126` says that, and the not-formalized list (`:157`) names the same two missing derivations, including equal `σ N_e`.

**Witness.** `d = 2`, `J_T* = 4`, `σ N_e = 2`, so `γ = 1/2` and `E[J_T] − J_T* = 2`. Then `(6 − 4)/4 = 1/2` and `2 / (2 · 2) = 1/2`.

Nothing in the Faithful list above is one of these four weakenings. The per-party regret `E[R_i] = d_i/(2β_i)` and `E[Φ] − Φ* = d/(2γ)` are listed as absent (`formal/lean/README.md:125-126` and `:157`). They are absent from the declarations.

---

## Nits

1. **`CoadaptationDrift.lean:221-227` and `formal/lean/README.md:128`.** `s8b_static_regret` concludes `(1/2) β_0⁻¹ = 1/10` and `(1/2) β_1⁻¹ = 1/5`. The docstring calls this the recovery of the static (no-drift) regrets, and the README proved cell says "static regrets recover `1/(2β_i)`". The quadratic form `½ (g_iᵀ P_0 g_i) / M_{ii}` at `Q = 0` is not a declaration. The recomputation above shows that form equals `1/(2β_i)`, with `P_0 = S⁻¹`. The negative finding `ca7_regret_not_naive` does not use this clause. The comment at `:177` also calls `s8bP` the unique symmetric solution; uniqueness is the nonsingular 3×3 fact above, and it is not a Lean lemma. The equation for this `P` is a theorem.

2. **`DriftSpeed.lean:25-26`.** The module comment says a half-window lower bound on the time-averaged excess diverges. `halfWindow_diverges` is the limit of the scalar `(c/2)(α T/2 − β)²`. README `:123` and OPEN_WORK T19 (i) describe the scalar limit and say there is no time-average statement.

3. **`CoadaptationDrift.lean:149-150`.** The comment says matrix multiplication is not exposed as a function in Lean 4.37. `virial_trace` multiplies matrices. `mul2` is an entrywise encoding of the same product, and `s8b_lyapunov` proves all four entries.

4. **Small disclosure leftovers.** README `:127` lists symmetry of `S` among the hypotheses of CA7 (1). `ca7_potential_excess` does not take `Sᵀ = S`; with `Σ` symmetric the trace identity still holds for the excess defined as `½ Tr(S Σ)`. The Hurwitz claim in CA7 (1) (`theory/COADAPTATION.md:217`) is neither a theorem nor a line in the not-formalized list; the proved cell states the excess. `ca1c_fraction` (`CoadaptationExcess.lean:155`) takes `_hσ : 0 < σ N_e` and the section turns the unused-variable linter off, so the hypothesis is unused. The WEAKER description of the fraction does not depend on it.

---

## Prose

The hypothesis sentence, 103 bytes, one copy, wrapped in `**` on both sides:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

`CORE.md:9`, `THEORY.md:41`, `README.md:9`, `theory/SELECTION_AXIOMS.md:13`, and `theory/COADAPTATION.md:28` each match that line. T19 calls it a claim about the real world and lists it among the things Lean does not formalize (`OPEN_WORK.md:66`, and `formal/lean/README.md:135`).

The batch-2 README rows, the Lean sources under `formal/lean/`, and the T19 row use "cost". A whole-word search of `formal/lean/**/*.lean` and `formal/lean/README.md` finds neither "bill" nor "kill". T19's own text contains neither word. Older OPEN_WORK rows keep the repository's existing test-protocol vocabulary; this confirm's verdict does not use it.

---

## Commands and results

| Command | Result |
|---|---|
| `nice -n 19 tools/check_lean.sh` | exit 0. `lake exe cache get`, then `lake build`: "Build completed successfully (5857 jobs)". `AxiomAudit: OK (745 GTAO declarations; only propext, Classical.choice, Quot.sound)`. `check_lean.sh: OK`. |
| Whole-token scan of `GTAO.lean` and `GTAO/*.lean` | 0 hits |
| Exact-rational s8b solve | `P`, both drift regrets, both naive values, and both static quadratic-form regrets match the table above. Lyapunov residual of the claimed `P` is `0`. |
| `python3 tools/check_fresh.py` | First run, against the snapshot's `origin/main` `2eeab30`: FAIL (`STATUS.md` main `b16193d` outside that window). After `git fetch origin main` (tip `b421b22`): **PASS**. Window `b421b22 98ff384 d1a6de4 b16193d e88b692`. |
| `python3 tools/check_consistency.py` | **PASS** (`FAIL: 0`). Wording failures in maintained docs: 0. Advisory length warnings only (THEORY main text 10948 words, README 1476). |
| `python3 tools/check_open_work.py` | **PASS**. `items.json` not-DONE 62, `QUEUE.md` not-DONE 90, missing from OPEN_WORK: 0. |
| `nice -n 19 python3 -m pytest -q tools` | **246 passed** in 306.84s. `tools/test_lean.py` re-runs `check_lean.sh`. |

---

## Conclusion

CONFIRMED-WITH-NITS. Uniqueness is the max-ratio argument plus uniformization, and the normalized Gibbs law when a potential is present. CA7 (1) is the Lyapunov trace with the antisymmetric part removed. CA1b's shift, Boltzmann factor, and Gibbs excess are the note's statements, and the excess is `Equipartition.gibbs_excess_quadratic` at `β = 1`. CA1c's potential and the summed-cost identity at every state match the note. CA7 (4) is the s8b negative finding on the checker's covariance, with the rationals recomputed independently. DS2, the team split, the gap, and the fraction are WEAKER for the reasons the README and T19 give. The static-regret sentence in the CA7 (4) cell is ahead of `s8b_static_regret`'s type. 745 declarations, standard axioms only. This confirm does not merge the draft.
