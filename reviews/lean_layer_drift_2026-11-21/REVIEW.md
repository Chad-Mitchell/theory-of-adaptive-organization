# Independent hostile review: PR #152 (L1, DS1, band model, CA1)

**Reviewer:** independent (wrote none of the PR, the `formal/lean/` library, or the OPEN_WORK T19 edit).
**Date:** Sunday 22 November 2026.
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/152
**Head:** `f8a55df159313e8fe084b733c349ad691e8fcc63` on `lean-layer-drift-2026-11-21` (two commits: `488ea51`, `f8a55df`).
**Base:** `d1a6de448bbaca2e2e0f18d4dc2ce9c3972308a5` (`main`). Diff is 8 files, +1593/−8.
**Verdict: READY-WITH-FIXES**

No blocker. The new theorems are not shells whose hypotheses already are the conclusion, and the two heavy inputs (the stationary moment equations of (L), the log-linear rate ratio) are named as inputs in `formal/lean/README.md`. Four mapped statements are weaker than the sentence in the note they cite, and the README repeats two of those weakenings as the claim. `Coadaptation.gibbs_form` is a tautology. `elan` and `lake` are not installed in this environment, so `tools/check_lean.sh` was not re-run and the reported count of 622 declarations was not regenerated.

---

## What was checked

- `git diff --stat d1a6de4..f8a55df` and a line-by-line reading of `GTAO/N60Exact.lean`, `GTAO/DriftSelection.lean`, `GTAO/BandMonge.lean`, `GTAO/BandCounterexample.lean`, `GTAO/Coadaptation.lean`, `scripts/AxiomAudit.lean`, `GTAO.lean`, and the README rows those files add.
- Each headline statement against `theory/LAYER_CONVEXITY.md` (L1, Lemmas M, Z, X, Theorem B, §5), `theory/DRIFT_SELECTION.md` Theorem DS1, `theory/COADAPTATION.md` CA1 and CA1a, `THEORY.md` §3 (the from-0 count paragraph) and §4, and CLAIM_MAP rows N64, S1, and U1.
- A whole-token scan of `formal/lean/GTAO.lean` and `formal/lean/GTAO/*.lean` for `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `implemented_by`, using the same boundary regex as `tools/check_lean.sh`. Result: **0 hits** in 18 files.
- Whether each hypothesis package is the paper’s input or a restatement of the conclusion, and whether a one-dimensional witness makes the DS1 moment structures satisfiable.
- `elan`, `lake`, and `lean` are absent (`command -v` empty; no `~/.elan`). The build, the axiom audit, and the number 622 were not re-executed.

Labels below are the Lean conclusion against the prose sentence it is mapped to. “Disclosed” means the README’s “what is assumed” cell says the same thing the Lean hypothesis says.

---

## Faithfulness

### L1 forward: `N60Exact.count_isLeftmostArgmin` — FAITHFUL

Lean (`formal/lean/GTAO/N60Exact.lean:56-57`), with `phi` from `GTAO/Hull.lean:34-35` (`φ(K) = K + R(1+ε_K)`) and `DiscreteConvexOn` from `Hull.lean:160-161` (first differences of `ε` nondecreasing on `{0,…,n}`, i.e. decrements `d_K = ε_{K-1}−ε_K` nonincreasing):

```lean
theorem count_isLeftmostArgmin {n : ℕ} {ε : ℕ → ℝ} {R : ℝ} (hR : 0 ≤ R)
    (hconv : DiscreteConvexOn n ε) : IsLeftmostArgmin R ε n (count R ε n)
```

`count` (`N60Exact.lean:47-48`) is `#{i < n : 1 < R(ε_i − ε_{i+1})}`. `IsLeftmostArgmin` (`:51-52`) is: the index is at most `n`, `φ` there is ≤ `φ` at every index ≤ `n`, and `φ` there is < `φ` at every smaller index.

Paper (`theory/LAYER_CONVEXITY.md:37`, and the same sentence in `THEORY.md:59` and CLAIM_MAP N64): on a finite domain, if the decrements are non-increasing, then `K*_0(R) = #{K ≥ 1 : R d_K > 1}` equals the leftmost argmin of `J(K) ∝ K + R(1+ε_K)` for all `R ≥ 0`.

The strict test `R d_K > 1`, the domain `{0,…,n}`, and “leftmost” (strictly better than everything to the left, ≤ everything else) match. `R = 0` is included: no step pays, and `φ(K) = K` is minimized at `0`.

### L1 converse and iff — WEAKER

Paper (`theory/LAYER_CONVEXITY.md:37`): if the decrements are positive and pairwise distinct (distinctness with the threshold decrement `d_{(m)} > 0` suffices) and some `d_m < d_{m+1}`, there is an **open interval** of `R > 0` on which `K*_0(R) = m` is not a minimizer. The iff used by N64 is: under those positivity and distinctness hypotheses, the count equals the leftmost argmin for every `R ≥ 0` if and only if the decrements are non-increasing.

Lean (`N60Exact.lean:159-163`):

```lean
theorem exists_R_count_not_argmin ...
    ∃ R, 0 < R ∧ ∃ k ≤ n, phi R ε k < phi R ε (count R ε n)
```

under pairwise distinct step decrements, a rise `ε_j − ε_{j+1} < ε_{j+1} − ε_{j+2}`, and at least `j+1` positive decrements. `count_exact_iff_convex` (`:284-287`) is the iff for every `R > 0`, under all-positive distinct decrements.

The proof at `:249-262` does set `count (1/rinv) = j+1` at one constructed `R`, and `not_min_of_rise` says index `j+1` is never minimal, so that one witness really is “the count equals `m` and misses.” The theorem exports neither the equality nor an interval. Any threshold strictly between the two consecutive order statistics `g_{(m+1)}` and `g_{(m)}` works the same way, so the interval is sitting in the proof and is not a conclusion. The `R > 0` range in the iff is the paper’s `R ≥ 0` on the nose only because `R = 0` is the trivial case already covered by the forward theorem; that part is not a gap.

The positivity threshold is the right one. `threshold_pos` (`:138-141`) is “at least `m` positive decrements ⇒ the `m`-th largest is positive,” which is the note’s `d_{(m)} > 0` once distinctness picks a unique order statistic. All-positive is the special case `exists_R_count_not_argmin_of_pos`. The hypotheses are satisfiable (`d = (3,1,2)` on `{0,1,2,3}`).

README `:105` says “some `R > 0` makes the count differ from every minimizer” and “for all `R > 0`.” That matches the Lean statements. It does not match L1’s open interval or the equality `K*_0(R) = m`.

### `d = (−2,−1)` — WEAKER on uniqueness

Paper (`theory/LAYER_CONVEXITY.md:40`): `d = (−2,−1)` (`ε = (−3,−1,0)`) is not convex, yet `R d_K > 1` never holds, so `K*_0(R) = 0` equals the **unique** minimizer for every `R ≥ 0`.

Lean (`N60Exact.lean:338-344`):

```lean
theorem exists_nonconvex_count_exact :
    ¬ DiscreteConvexOn 2 epsCE ∧
      ∀ R, 0 ≤ R → IsLeftmostArgmin R epsCE 2 (count R epsCE 2)
```

`epsCE_not_convex` and `epsCE_count_zero` are the right two facts (`d_1 = 2 > 1 = d_2` fails discrete convexity; both steps have `R d ≤ 0 < 1`). `IsLeftmostArgmin` at `0` says `0` is a minimizer. The third conjunct (“strictly better than every smaller index”) is vacuous at `0`, and `epsCE_zero_min` (`:327-334`) only discharges `φ(0) ≤ φ(j)`.

The values are `φ(0) = −2R`, `φ(1) = 1`, `φ(2) = 2+R`, so the inequality is strict for every `R ≥ 0` and the minimizer is unique. The theorem does not say so. README `:106` does: “equals the unique minimizer.”

### Lemma M, `BandMonge.quadrangle` — FAITHFUL

Paper (`theory/LAYER_CONVEXITY.md:60`): if `W` is non-increasing, `w(i,k)+w(j,l) ≤ w(i,l)+w(j,k)` for `i ≤ j ≤ k ≤ l`, with `w` the weighted within-band variance.

Lean (`BandMonge.lean:161-163`): for `a ≤ b ≤ c ≤ d ≤ n`, every cell mass `μ > 0`, and `W` nonincreasing on `x < n`,

```lean
w μ W a c + w μ W b d ≤ w μ W a d + w μ W b c
```

`w = Q − S²/M` (`:109`) is `Σ μ(W−m)²`, and an empty band is `0` (`w_self`). Positive cell masses are what the merge-gain division needs; the note’s zero-mass side cases are outside this statement, and the README says `μ > 0`. The three-block core (`quadrangle_core`, `:53-55`) is the note’s identity `f(X)+f(Y)−f(X∪Y) = M_X M_Y/(M_X+M_Y)(m_X−m_Y)²` plus nonincreasing block means.

### Lemma Z, `BandMonge.terminal` — FAITHFUL

Paper (`theory/LAYER_CONVEXITY.md:63`): if `W ≥ 0` and `W` is non-increasing, `w(i,k)−w(j,k) ≤ z(i)−z(j)` for `i ≤ j ≤ k`.

Lean (`BandMonge.lean:203-205`): `w(a,c) + z(n,b) ≤ z(n,a) + w(b,c)` for `a ≤ b ≤ c ≤ n`, with `z(n,a) = Σ_{a ≤ x < n} μ W²` (`:112`). That is the same inequality on a finite grid whose terminal runs to the last cell. `W ≥ 0` is a hypothesis and is used (`S_nonneg`, `terminal_core`).

### `W ≥ 0` is necessary, `terminal_needs_nonneg` — FAITHFUL

Paper (`theory/LAYER_CONVEXITY.md:64`): `W = (0,−1)` with equal weights gives `w(AB)−w(B) = 1/2` while `z(0)−z(1) = 0`.

Lean (`BandMonge.lean:443-448`):

```lean
theorem terminal_needs_nonneg :
    ... w μ W 0 2 + z μ W 2 1 = (3 / 2 : ℝ) ∧
        z μ W 2 0 + w μ W 1 2 = 1 ∧
        ¬ (w μ W 0 2 + z μ W 2 1 ≤ z μ W 2 0 + w μ W 1 2)
```

with `μ ≡ 1` and `W(0) = 0`, `W(1) = −1`. Rearrangement is the note’s pair: `w(0,2)−w(1,2) = 1/2` and `z(0)−z(1) = 0`. The profile is nonincreasing and the weights are positive, so the failed hypothesis is `W ≥ 0`. README `:109` states these two numbers.

### Lemma X and Theorem B, `exchange` / `band_convex` — WEAKER

Paper, Lemma X (`theory/LAYER_CONVEXITY.md:66`): on a finite grid, if M and Z hold, then `2 E_K ≤ E_{K−1} + E_{K+1}` for `K ≥ 1`, for the optimal band costs. Theorem B (`:69`): if `S/N` is non-increasing in `|ω|`, then `E^B_K` is convex in `K ≥ 0`, so in 𝓑 the from-0 count equals the leftmost argmin for every `R ≥ 0`. The proof needs `W = 1/(1+N/S) ≥ 0` nonincreasing. Finite grids are M, Z, and X; a continuous measure is a limit of grids.

Lean (`BandMonge.lean:426-433`):

```lean
theorem band_convex ... (hk : 1 ≤ k)
    (hP : IsPath (n + 1) k p) (hQ : IsPath (n + 1) (k + 2) q)
    (hRopt : ∀ x, IsPath (n + 1) (k + 1) x →
      pathCost (linkCost μ W n) (k + 1) r ≤ pathCost (linkCost μ W n) (k + 1) x) :
    2 * pathCost (linkCost μ W n) (k + 1) r ≤
      pathCost (linkCost μ W n) k p + pathCost (linkCost μ W n) (k + 2) q
```

A `k`-link path ends at the sentinel `n+1`, so it is `k−1` free bands plus one terminal band (`:420-425`). The shape `2 E_k ≤ E_{k−1} + E_{k+1}` is what this becomes when `p` and `q` are themselves optimal. The theorem states the inequality for an optimal middle path against **arbitrary** outer paths. `exists_optimal` (`:397-398`) is “if some path exists, an optimal one exists.” No declaration builds a path, and no declaration defines `E_K` as that minimum and states the second difference.

Two further pieces of Theorem B are absent, and the README’s not-formalized list already names two of them (continuous measure; `W = 1/(1+N/S)`):

- The sentence “so `K*_0(R)` equals the leftmost argmin” is not a theorem. It would be L1 applied to the optimal costs, which needs those costs defined.
- Convexity is proved for the clustering cost `w`/`z`. The note defines `E^B_K` as the minimum of `∫(|1−H|² S + H² N)` over staircases `H = Σ g_k 1_{|ω|<b_k}`. The reduction to within-band variance is not a theorem. `BandCounterexample.cost` is that staircase, and nothing identifies its minimum with `pathCost` of `linkCost`.

README `:110` says the proved content is “`2E_K ≤ E_{K−1}+E_{K+1}` for the band model.” That sentence is the missing corollary, not `band_convex`’s type.

The exchange itself (`exchange`, `:342-345`) is the note’s tail swap: a `k`-link path and a `(k+2)`-link path become two `(k+1)`-link paths, crossing index the first `q_{t+1} ≤ p_t`, cost not increased, by `Monge`. `linkCost_monge` (`:224-226`) is M on finite right endpoints and Z when the right endpoint is the sentinel. That half matches Lemma X’s argument.

### Peak counterexample, `BandCounterexample.not_convex` — FAITHFUL

Paper (`theory/LAYER_CONVEXITY.md:85`): three cells, `W = (0,1,0)`, weights `(2,1,1)`, optimal excesses `E^B − E^B_∞ = (1, 2/3, 0)` for `K = 0,1,2`, decrements `1/3 < 2/3`.

Lean (`BandCounterexample.lean:131-135`):

```lean
theorem not_convex :
    (∀ b g, cost (K := 0) b g = 1) ∧
    (∀ b g, 2 / 3 ≤ cost (K := 1) b g) ∧ (∃ b g, cost (K := 1) b g = 2 / 3) ∧
    (∀ b g, 0 ≤ cost (K := 2) b g) ∧ (∃ b g, cost (K := 2) b g = 0) ∧
    (1 : ℝ) - 2 / 3 < 2 / 3 - 0
```

`cost` (`:90-91`) is `Σ_{c<3} μ_c (H(c)−W(c))²` with `H(c) = Σ_{k<K} g_k 1_{c < b_k}` (`:86-87`), free real weights, cutoffs in `ℕ`. `K = 0` is identically `1` (`bandE0`). Every one-layer design is at least `2/3`, and cutoff `2` with weight `1/3` attains it. Cutoffs `2,1` and weights `1,−1` give `H = (0,1,0)` and cost `0`, and every two-layer cost is ≥ `0` because it is a sum of squares. The minima are therefore `(1, 2/3, 0)`. `clusterE_values` (`:76-77`) is the same triple for the rational clustering enumeration, by `decide +kernel` (kernel `decide`, not `native_decide`). This is the note’s example for the staircase `H`, independent of the missing clustering equivalence above.

### DS1(a), `DriftSelection.ou_excess` — FAITHFUL to the disclosed identity

Paper (`theory/DRIFT_SELECTION.md:70-74`, CLAIM_MAP S1): under DS-A, DS-B, and the Langevin equation (L), the lag has a unique stationary law, the long-run time average of `J−J*` equals the stationary mean, and

```
J−J* bar = d/(2β) + ½ Tr[ H (D_m β H + γ I)^{-1} Q ].
```

Lean (`DriftSelection.lean:166-172`):

```lean
theorem ou_excess ...
    (hM : OUMoments Dm β γ H Q P C S) :
    (1 / 2) * trace (H * P) =
      (d : ℝ) / (2 * β)
        + (1 / 2) * trace (H * (driftMatrix Dm β H + γ • 1)⁻¹ * Q)
```

with `driftMatrix = (D_m β) • H` (`:56-58`), `H` positive definite, `Q` Hermitian, `D_m, β, γ > 0`, `d ≥ 1`.

`OUMoments` (`:73-84`) is the note’s Itô system at stationarity (`:82-84` of the note), not the trace formula:

- `γ S = Q`
- `0 = −(A+γI) C + γ S − 2 Q`
- `0 = −A P − P A + γ (C+Cᵀ) + 2 D_m I + 2 Q`

`ou_C_eq` then gives `C = −(A+γI)^{-1} Q`, which is the note’s next line, and the trace calculation is the rest of the proof of (a). Existence of the stationary law, the ergodic theorem, and “time average = stationary mean” are not hypotheses and not conclusions. README `:111` and the not-formalized list at `:143` say that. S1’s “PRIOR ART / diffusion limit of the Moran chain” is not what this theorem claims.

The moment equations do not assume the scalar identity. They are satisfiable: for `d = 1`, `H = Q = D_m = β = γ = 1`, one solution is `S = 1`, `C = −1/2`, `P = 3/2`, and both sides of the identity equal `3/4`. No Lean declaration records a witness (nit 6).

### DS1(b) and the `Q = 0` case — FAITHFUL for what is stated

Paper (`theory/DRIFT_SELECTION.md:76`): Brownian, `γ = 0`, excess `d/(2β) + Tr(Q)/(2 β D_m)`, independent of `H`; with `Q = D I`, `d/(2β)(1+D/D_m)`; with a general mutation matrix `M`, `d/(2β) + Tr(M^{-1} Q)/(2β)`. `Q = 0` is SA1b (`:80`).

Lean:

- `bm_excess` (`:259-263`): under `BMMoments` (`:87-92`, the `γ = 0` Lyapunov equation), `½ Tr(H P) = d/(2β) + Tr(Q)/(2 β D_m)`.
- `bm_excess_isotropic` (`:287-290`): `Q = D • I` gives `(d/(2β))(1 + D/D_m)`.
- `bm_excess_static` (`:298-302`): `Q = 0` gives `d/(2β)`.

`BMMoments.lag` is the note’s equation with the `C` terms removed. The isotropic algebra is `Tr(D I) = D d`, so the second term is `(d/(2β))(D/D_m)`. README `:112` states these three and does not claim general `M`. General `M` is part of S1 and of DS1(b), and it is missing from the not-formalized list (should-fix 4).

`H.PosDef` is unused in `bm_excess` (`_hH`). The identity is algebraic in `A = D_m β H` and does not need definiteness once the Lyapunov equation is granted. Harmless.

### DS1(c), `velocity_mean_excess` — WEAKER

Paper (`theory/DRIFT_SELECTION.md:78`): constant velocity, excess `d/(2β) + vᵀ H^{-1} v / (2 β² D_m²)`.

Lean (`DriftSelection.lean:309-313`):

```lean
theorem velocity_mean_excess ...
    (hmean : driftMatrix Dm β H *ᵥ μ = -v) :
    (1 / 2) * (μ ⬝ᵥ (H *ᵥ μ)) =
      (v ⬝ᵥ (H⁻¹ *ᵥ v)) / (2 * β ^ 2 * Dm ^ 2)
```

If `A μ = −v` and `A = D_m β H`, then `½ μᵀ H μ = vᵀ H^{-1} v / (2 β² D_m²)`. That is the mean-lag term in the note’s proof (`:88`). The fluctuation `d/(2β)` is not a hypothesis and not a conclusion. README `:113` says it “is added outside this identity.” Adding it is prose: there is no velocity-moment structure whose trace is `d/(2β)`, and `Equipartition.gibbs_excess_quadratic` is a different model (a Gibbs measure on `ℝ^d`, not the fluctuation around `−A^{-1} v`). CLAIM_MAP S1 states one sum. The summed formula is not a Lean theorem.

The scaling itself matches: `μ = −A^{-1} v = −(D_m β)^{-1} H^{-1} v`, and `½ μᵀ H μ` is the displayed quotient. `A` is invertible because `H` is positive definite and `D_m β > 0`, so `A μ = −v` is the note’s “mean lag is `−A^{-1} v`” written as an equation. The SDE that produces that mean is an input, as with (a).

### DS1(d), `ou_excess_fast_remainder` — WEAKER, and the README says so

Paper (`theory/DRIFT_SELECTION.md:80`): as `γ → ∞` at fixed `Q/γ`, the tracking term tends to `½ Tr(H Q/γ)`.

Lean (`DriftSelection.lean:371-377`) is the algebraic identity

```
½ Tr[H (A+γI)^{-1} Q] − ½ Tr[H (Q/γ)]
  = −½ Tr[H (A+γI)^{-1} A (Q/γ)]
```

for `γ > 0`. The limit is not a conclusion. README `:114` calls this “the exact remainder to the fast-`γ` floor” and `:143` lists the topological limit as not formalized. The identity is the right remainder: `(A+γI)(Q/γ) = A(Q/γ) + Q`, so `(A+γI)^{-1} Q − Q/γ = −(A+γI)^{-1} A (Q/γ)`.

### CA1, `ca1_iff` — FAITHFUL for detailed balance; uniqueness disclosed as absent

Paper (`theory/COADAPTATION.md:53`, CLAIM_MAP U1): on connected party graphs, under CA-A, CA-B, CA-C, CA-E, the joint chain has a unique stationary `π > 0`. It is reversible iff `(β_i J_i)` is an exact potential game, and then `π ∝ e^{−Ψ}`, whatever the clocks.

Lean (`Coadaptation.lean:136-139`):

```lean
theorem ca1_iff (hC : LogLinearChain G β J q)
    (hconn : ∀ i a b, Relation.ReflTransGen (G i) a b) :
    (∃ π, (∀ x, 0 < π x) ∧ DetailedBalance q π) ↔ ∃ Ψ, IsExactPotential β J Ψ
```

`LogLinearChain` (`:59-65`) assumes symmetric graphs, `q = 0` off single-party moves, `q > 0` on moves, and

```
q(x → update x i s) = exp(−β_i (J_i(update) − J_i(x))) · q(update → x).
```

That ratio is the note’s Moran / logit ratio (`COADAPTATION.md:45-47`). It is not the existence of `Ψ`. Clocks sit inside `q` and cancel in the ratio, which is the note’s “whatever the clocks.” Connectedness is a path between every pair of designs of each party. `IsExactPotential` (`:68-69`) is the note’s equality on every unilateral change, and `potential_of_detailedBalance` (`:102-105`) extends the edge equality along `ReflTransGen`, which is the telescoping paragraph of the proof.

`detailedBalance_of_potential` (`:87-88`) says `π = exp(−Ψ)` satisfies detailed balance. `potential_of_detailedBalance` says `Ψ = −log π` is an exact potential. Together those are “`π ∝ e^{−Ψ}`” for the `π` that is in detailed balance. `ca1_iff` itself only says existence on each side.

Uniqueness is not a theorem. `stationary_of_detailedBalance` (`:155-158`) says detailed balance implies `Σ_y π_y q_{y x} = Σ_y π_x q_{x y}` on a finite product. That is global balance for a measure, not “the stationary distribution is unique” and not “`π` is a probability.” README `:116` and the not-formalized list at `:144` say uniqueness (Perron–Frobenius) is not formalized, and that the formalized reading is “some positive `π` satisfies detailed balance.” U1’s “then uniquely” is the missing half. The disclosure matches the theorem.

Finiteness is not a hypothesis of `ca1_iff`. README `:116` lists “finite product state space” as assumed. It is assumed only for the balance-sum theorem.

The ratio hypothesis is satisfiable (constant `J`, any positive symmetric `q` on a connected symmetric graph). A potential game gives the left side via `exp(−Ψ)`; the theorem does not force every `LogLinearChain` to be a potential game.

### `gibbs_form` — VACUOUS

```lean
lemma gibbs_form {π} (hπ : ∀ x, 0 < π x) (x) :
    π x = exp (−(−log (π x)))
```

(`Coadaptation.lean:148-150`.) This is `exp_log`. It does not mention `q`, `J`, `Ψ` as a potential, or detailed balance. The module comment (`:147`) calls it “the Gibbs form: the reversible `π` is exactly `exp(−Ψ)`.” README `:116` lists `gibbs_form` among the CA1 declarations and glosses “`Ψ = −log π` up to a constant.” The constant is not in the lemma; the lemma is the identity `π = exp(log π)` for any positive function. The Gibbs correspondence that CA1 actually needs is the pair `detailedBalance_of_potential` and `potential_of_detailedBalance`.

### CA1a — FAITHFUL

Paper (`theory/COADAPTATION.md:59`): if `Δ_i J_i = ω_i Δ_i Φ` and `β_i ω_i = γ` for every `i`, then `π ∝ e^{−γ Φ}`. If `β_i ω_i ≠ β_j ω_j` and `Φ` has a nonzero mixed difference, the chain is not reversible.

Lean `ca1a_weighted` (`:163-167`): those two hypotheses give `IsExactPotential β J (γ Φ)`. `detailedBalance_of_potential` then supplies `π = exp(−γ Φ)`. README `:117` states the potential conclusion, which is the theorem.

`ca1a_square` (`:175-179`): for any exact potential of `(β_i J_i)`,

```
(β_i ω_i − β_j ω_j) · (Φ(x[i↦a][j↦b]) − Φ(x[i↦a]) − Φ(x[j↦b]) + Φ(x)) = 0.
```

That is the note’s square obstruction (the Kolmogorov sum around the square). The contrapositive “unequal products and a nonzero mixed difference rule out a potential, hence rule out detailed balance” is one step from this identity plus `ca1_iff`. README `:117` says that step in parentheses. The identity is what the proof in the note computes.

`ω_i > 0` is not required. The note assumes it. The algebra does not, and dropping it does not weaken the conclusion.

---

## Inputs versus conclusions

| Piece | Taken as a hypothesis | Proved | Assumes the conclusion? |
|---|---|---|---|
| L1 | Discrete convexity (nonincreasing decrements); for the converse, distinctness and a positive threshold decrement | Count equals leftmost argmin; a rise produces an `R` at which the count is not minimal; iff under all-positive distinct decrements; `(−2,−1)` is not convex and the count is a leftmost minimizer | No. Convexity is the decrement hypothesis, not “count = argmin.” The bare iff is false, and `exists_nonconvex_count_exact` is the witness. |
| Band M, Z, X, B | `μ > 0`, `W` nonincreasing, and for Z also `W ≥ 0` | Quadrangle, terminal inequality, Monge for `linkCost`, exchange, the outer-path form of the second difference | No. `terminal_needs_nonneg` shows Z’s conclusion fails for `W = (0,−1)`. |
| Peak | The three-cell `W` and `μ` | Minima `(1, 2/3, 0)`, so the decrements rise | No. Both the lower bounds and the attaining designs are proved. |
| DS1 | `OUMoments` / `BMMoments` / `A μ = −v`, i.e. the note’s stationary moment equations | The trace identities, the isotropic special case, the mean-lag quadratic form, the fast-`γ` remainder | No. The moment equations are matrix Lyapunov equations. The scalar excess is derived. A 1-d solution exists (above). |
| CA1 | The log-linear rate ratio, symmetric connected graphs, positive rates on moves | Detailed balance with a positive `π` iff an exact `β`-scaled potential; balance sums on a finite space; CA1a | No. The ratio is the Moran input. Existence of `Ψ` is the conclusion. |

README `:111-117` and `:143-144` describe these inputs in those words. OPEN_WORK T19 on this branch says the same for DS1 (“taking the stationary moment equations of the Langevin limit (L) as inputs”). THEORY §4 does not restate DS1; it points at the selection note. THEORY `:59` states L1, including the converse and the `(−2,−1)` counterexample, which is the sentence judged above.

---

## README, the audit script, and the count 622

`GTAO.lean:14-19` imports `DriftSelection`, `N60Exact`, `BandCounterexample`, `BandMonge`, and `Coadaptation`, so an audit that imports `GTAO` sees all five modules.

`scripts/AxiomAudit.lean:20-33` walks `env.constants`, keeps those whose defining module has name-prefix `GTAO` (`Name.isPrefixOf`, so `GTAOExtra` would not match), rejects an empty count, and rejects any constant whose `collectAxioms` list is not exactly `propext`, `Classical.choice`, `Quot.sound`. A `sorry` in a proof would be `sorryAx`. `native_decide` would be `Lean.ofReduceBool`. The script is the one already reviewed on PR #147. This PR does not change it.

`tools/check_lean.sh:36-62` token-scans only `GTAO.lean` and `GTAO/*.lean`, then builds, then runs the audit. The scan here matches that regex and is clean. `scripts/AxiomAudit.lean:10` still contains the word `` `sorry` `` in a comment. That file is outside the scan. `decide +kernel` in `clusterE_values` is not `native_decide`.

README `:37`: “Last run (21 November 2026, this branch): 622 declarations, OK.” That number is the author’s. It was not regenerated here. The five new files contain 98 source-level declarations (`theorem` / `lemma` / `def` / `structure`: N60Exact 14, DriftSelection 17, BandMonge 36, BandCounterexample 19, Coadaptation 12). The audit counts every environment constant in those modules, including generated auxiliaries, so 622 is a different count from 98 and is not checked by arithmetic on the sources. PR #147’s review recorded 312 constants before these files existed; this diff adds only these modules on top of that library. Plausible, unchecked.

README claims that are ahead of the declarations:

- `:106` “unique minimizer” for `d = (−2,−1)`. The theorem proves `IsLeftmostArgmin`.
- `:110` “`2E_K ≤ E_{K−1}+E_{K+1}` for the band model.” No declaration defines that `E_K`.
- `:116` lists `gibbs_form` as part of the CA1 Gibbs correspondence.

README claims that match:

- L1 forward, the single-`R` converse, and the `R > 0` iff (`:104-105`).
- Lemma Z’s necessity with the numbers `3/2` and `1` (`:109`).
- DS1(a)(b) as trace identities from the moment equations, DS1(c) as the mean term only, DS1(d) as a remainder rather than a limit (`:111-114`, `:143`).
- CA1 as “some positive `π`” rather than “the unique stationary law” (`:116`, `:144`).

---

## Issues

**Blockers:** none.

**Should-fixes (documentation, plus the one-line strengthenings that make the documentation true):**

1. **`formal/lean/GTAO/N60Exact.lean:327-344` and `formal/lean/README.md:106`.** The counterexample theorem proves that `0` is a leftmost minimizer. At index `0` that predicate does not exclude a tie. The README says “unique.” The values `φ = (−2R, 1, 2+R)` are strictly ordered for every `R ≥ 0`. Fix: in `epsCE_zero_min`, prove `φ(0) < φ(j)` for `0 < j ≤ 2`, and put that conjunct on `exists_nonconvex_count_exact`. The alternative is to change the README and the module comment (`N60Exact.lean:34-36`) from “unique” to “leftmost.”

2. **`formal/lean/GTAO/N60Exact.lean:159-163` and `formal/lean/README.md:105`.** L1’s converse is an open interval of `R > 0` on which `K*_0(R) = m`. The theorem is one `R` at which the count is not minimal. The proof already has `count = j+1` (`:249-262`); the set of thresholds strictly between the consecutive order statistics is an open interval. Fix: export `∃ R₀ > 0, ∃ ε > 0, ∀ R, |R−R₀| < ε → count R ε n = j+1 ∧ ∃ k ≤ n, φ(k) < φ(count)`, and point the README row at that statement. Until then, the README should say that the formal converse is a single `R` and does not record `K*_0(R) = m`.

3. **`formal/lean/GTAO/BandMonge.lean:397-436` and `formal/lean/README.md:110`.** `band_convex` bounds the optimal `(k+1)`-link clustering cost by the sum of two arbitrary paths. Theorem B’s inequality is about the optimal costs. `exists_optimal` still needs a path; `fun i => if i = 0 then 0 else n+1` is one for `k ≥ 1`. Fix: define `E k` as the minimum of `pathCost (linkCost μ W n) k` and prove `2 E (k+1) ≤ E k + E (k+2)` for `k ≥ 1`. In the not-formalized list (`README.md:142`), add the two missing halves of Theorem B: the identification of that minimum with the staircase cost `BandCounterexample.cost`, and the consequence that `K*_0` equals the leftmost argmin in 𝓑.

4. **`formal/lean/README.md:143` (and `:113`).** The not-formalized DS1 list omits two clauses that S1 states and that no theorem proves. Add: DS1(b) for a general mutation matrix `M` (`d/(2β) + Tr(M^{-1} Q)/(2β)`); DS1(c) as the single excess `d/(2β) + vᵀ H^{-1} v / (2 β² D_m²)`. Keep `velocity_mean_excess` described as the mean-lag term. The fluctuation is not supplied by `Equipartition`.

5. **`formal/lean/GTAO/Coadaptation.lean:146-150` and `formal/lean/README.md:116`.** Drop `gibbs_form` from the CA1 row. It is `π = exp(log π)` for an arbitrary positive function. The Gibbs correspondence is `detailedBalance_of_potential` (`:87`) and `potential_of_detailedBalance` (`:102`). If a named lemma is wanted, state that the `π` from the first and the `Ψ = −log π` from the second satisfy `π x = exp(−Ψ x) * c` only when that is what was proved, which for these two theorems is `c = 1` with `Ψ = −log π`.

**Nits:**

6. **`formal/lean/GTAO/DriftSelection.lean:73` and `:87`.** No declaration shows `OUMoments` or `BMMoments` inhabited. The 1-d matrices in the DS1(a) paragraph above are a witness. A `example` would lock the non-vacuity in the build. `bm_excess` (`:261`) takes `H.PosDef` and does not use it.

7. **`formal/lean/README.md:116`.** “Finite product state space” is a hypothesis of `stationary_of_detailedBalance` only. `ca1_iff` does not assume it.

8. **Count 622.** Re-run `tools/check_lean.sh` where `lake` exists and quote the audit line. This review did not.

---

## Conclusion

The branch does what a finite-cell, moment-equation formalization can honestly do. L1’s forward direction is the from-0 count. The `(−2,−1)` sequence is a real counterexample to a bare iff, short of the word “unique.” Lemmas M and Z, the necessity of `W ≥ 0`, and the peak costs `(1, 2/3, 0)` match `theory/LAYER_CONVEXITY.md`. The DS1 trace identities match the note’s Lyapunov arithmetic once the Itô equations are granted, and the README says they are granted. CA1 is the detailed-balance / exact-potential equivalence for a log-linear rate ratio, with uniqueness left out on purpose. The mapping table should stop calling the band second difference and the unique minimizer “proved” until those conclusions are the types of the theorems, should stop listing `gibbs_form` as the Gibbs form, and should name the general-`M` clause and the summed DS1(c) formula as not formalized. None of that is a hole in a proof that typechecks. `tools/check_lean.sh` was not run here.
