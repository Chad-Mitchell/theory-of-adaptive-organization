*Committed on 26 Nov 2026 after the hostile review of Lean round 5 (finding M3), so readers can check `formal/lean/GTAO/Rnd/SelfRef/OnsetO.lean` against its spec. The text below this note is the spec as written before the Lean, unchanged; its "nothing written in Lean" line describes that time. Ledger row RC21. KNOWN in substance; novelty not claimed.*

# Lean candidate: finite Theorem O (memory onset under a stake and an accuracy cap)

*26 Nov 2026, Forge. Spec only; nothing written in Lean, nothing committed. Source: C12C_ONSET.md §3.1 as corrected in §11.6 (L1, L2) after HOSTILE_REVIEW_C12C.md. Status of the math: PIM on paper, reviewed once; KNOWN in substance (a one-variable Everett/KKT instance). Target: a small add-on to the next Lean round, not a replacement for C9.*

## Setting (finite, all kinks)

- `n : ℕ`, with designs `k : Fin (n+1)` (units of judgment resource).
- `f : ℕ → ℚ` on `0..n` (error), with these hypotheses:
  - **nonincreasing:** `Δ k := f (k+1) - f k ≤ 0` for `k < n`;
  - **discrete convex:** `Δ k ≤ Δ (k+1)` for `k+1 < n`;
  - `0 ≤ f k`.
- `κ : ℚ` with `0 < κ`; `w : ℚ` with `0 ≤ w`; cap `D : ℚ`.
- **Strict feasibility (L2):** `f n < D`. This is `inf f < D` on the finite domain.
- `g w k := w * f k + κ * k`.
- `xD :=` the least `k` with `f k ≤ D`. It exists by strict feasibility.
- `xw :=` the least minimizer of `g w` on `0..n`.
- `xw' :=` the greatest minimizer of `g w` on `0..n`.
- Use ℚ, so `decide`/`norm_num` work on instances; ℝ also works with `linarith`.

## Statements

1. **(i) Projection.** `IsLeast {k | f k ≤ D ∧ ∀ j, f j ≤ D → g w k ≤ g w j} (max xw xD)`.
2. **(ii) Onset is a union.** `0 < max xw xD ↔ (w * (-Δ 0) > κ) ∨ (D < f 0)`, where `xw > 0 ↔ w * Δ 0 + κ < 0`.
   - Edge case: if `Δ 0 = 0`, the left disjunct is false at every w (w₁ = +∞).
3. **(iii) Least supporting stake (corrected per L1).** For `xD ≥ 1`, define `wstar := κ / (-Δ (xD - 1))`. Then `-Δ (xD - 1) > 0` from L2.
   - (a) `xD ∈ argmin (g v)` ↔ `wstar ≤ v ∧ v ≤ κ / (-Δ xD)`. The upper bound is +∞ if `xD = n` or `Δ xD = 0`. So `wstar` is the **least supporting stake**.
   - (b) At `v = wstar` exactly, `xD - 1` and `xD` tie, so `xD` is a minimizer but **not** the least one. `xD` is the least minimizer for every v strictly between the bounds. This is why the spec says "least supporting stake", not "the effective stake".
   - (c) **KKT.** If `xD > xw'`, then `μ := wstar - w > 0`, and `xD ∈ argmin (g (w + μ))`.
   - (d) If `xw ≤ xD ≤ xw'`, then `wstar ≤ w` and `μ = 0`. In all cases the optimum under the cap is a minimizer of `g (max w wstar)`.
4. **(iv) Monotone, and the corner meets.** `D ≤ D' → xD' ≤ xD`. With `xD ≥ 1` and `xD' ≥ 1`, this gives `wstar D' ≤ wstar D`. When `xD = 1`, `wstar = κ / (-Δ 0) = w₁` exactly.
5. **(v) Zero-stake floor.** At `w = 0`: `max xw xD = 0 ↔ f 0 ≤ D`.

## Proof plan

- (i): `g w` restricted to `0..n` is discrete convex, since `w Δ k + κ` is nondecreasing in k. The argmin is the interval `[xw, xw']`. The cap set is `[xD, n]` because f is nonincreasing. Then case on `xD ≤ xw'` vs `xD > xw'`: in the second case, `g` is strictly increasing on `[xw', n]` by discrete convexity.
- (ii): `xw > 0 ↔ g w 1 < g w 0` (discrete convexity: the first step decides), and `xD > 0 ↔ f 0 > D`.
- (iii): `k` minimizes `g v` iff the left step is ≤ 0 and the right step is ≥ 0 (discrete convexity: local = global). Then solve the two linear inequalities in v.
- (iv): monotonicity of `xD` in D, plus `Δ` nondecreasing.
- (v): (ii) at `w = 0`.

## Estimate and guards

- About 2.5 h. The main cost is the local-to-global lemma for discrete convex sequences, unless Mathlib's `ConvexOn` over ℕ suffices.
- No `sorry`. Standard axioms only, checked with `#print axioms`.
- Do not state (iii) as "the least minimizer at wstar", which is false at kinks (3b). Do not drop `f n < D`.
- Add a `decide`/`norm_num` instance test: f = [4, 2, 1, 0.5], κ = 1, D = 1.5 → xD = 2, wstar = 1, and supporting stakes are [1, 2].
- A failed proof is data: it names a hypothesis slip. Report it as an open miss, not a patch.
