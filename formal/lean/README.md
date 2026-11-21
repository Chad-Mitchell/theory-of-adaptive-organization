# Lean 4 formalization of the GTAO core (OPEN_WORK T19)

This directory is a Lean 4 + Mathlib project.  It machine-checks a
finite-menu fragment of the core in `THEORY.md` (canonical) and `CORE.md`.
Formalization cannot establish the hypothesis in CORE §3, which is a claim
about the real world.

- Toolchain: `lean-toolchain` pins `leanprover/lean4:v4.37.0-rc1`.
- Mathlib: `lakefile.toml` and `lake-manifest.json` pin `v4.37.0-rc1`.
- Build: from the repo root, `tools/check_lean.sh` (or, in this
  directory, `lake exe cache get` then `lake build`).
- There is no `sorry` in this tree.  Anything not listed as proved below
  is **not formalized**, not “proved with a hole.”

## How to build

Lean 4 is installed with [elan](https://github.com/leanprover/elan).
Then, from this directory:

```bash
lake exe cache get   # cached Mathlib oleans; do not compile Mathlib from source
lake build
```

`tools/check_lean.sh` does the same and also rejects any `sorry`.
A pytest wrapper, `tools/test_lean.py`, skips cleanly if Lean is not
installed.

## Mapping: Lean declarations to THEORY CT numbers

Hypotheses are part of the claim.  A finite nonempty design set, and a
stake-independent menu (ruin slack or absent), are standing hypotheses
wherever `FiniteDesignMenu` is used.

| Lean name | THEORY / source | What is assumed | What is proved |
|---|---|---|---|
| `FiniteDesignMenu.J` | CORE §1, THEORY §3 | Finite menu; `J = S + w E`; ruin slack or absent, so the menu does not depend on `w` | Definition of the split cost |
| `FiniteDesignMenu.exists_minimizer` | CT20 (i), finite case | `𝒟` nonempty and finite | A minimizer exists at every stake |
| `FiniteDesignMenu.Jstar`, `Jstar_concave`, `IsOptimal.Jstar_eq`, `Jstar_le_affine` | CT33 envelope | Same finite menu | `J*` is the min of affine functions of `w`, hence concave on `ℝ`, with supporting slope `E` at an optimum |
| `FiniteDesignMenu.optimality_inequalities`, `error_diff_sign` | CT33 | Same; two optima at `w₁`, `w₂` | The two revealed-preference inequalities, and `(w₂−w₁)(E₂−E₁) ≤ 0` |
| `FiniteDesignMenu.error_nonincreasing` | CT33 | `w₁ < w₂` (strict: at a tie, two optima may differ in error) | `E*` is nonincreasing |
| `FiniteDesignMenu.spend_nondecreasing` | CT33 | `0 ≤ w₁ < w₂`; ruin slack or absent | `S*` is nondecreasing |
| `FiniteDesignMenu.spend_nondecreasing_in_R` | CT33 | `h > 0` and the same stake hypotheses | `S*/h` is nondecreasing in `w` (equivalently in `R = w/h` at fixed `h`) |
| `FiniteDesignMenu.layer_count_bound` | CT20 (i) bound | `h > 0`, `h K ≤ S`, `0 ≤ w E` (so `J ≥ h K`) | Any design matching or beating a reference `d₁` has `K ≤ J(d₁;w)/h` |
| `FiniteDesignMenu.layer_count_nondecreasing` | CT20 (ii), sensing fixed | Spend is exactly `h K` with `h > 0`; `0 ≤ w₁ < w₂`; menu independent of `w` | The layer count itself is nondecreasing.  This fails once reads are also chosen (THEORY's counterexample); total spend still obeys CT33 |
| `effortJ_decreasing_differences`, `effort_nondecreasing` | CT10 | Error is nonincreasing along a frequency coordinate; check price `c > 0`; `w₁ < w₂` | Decreasing differences, and the discrete Topkis conclusion: optimal effort does not fall as stakes rise |
| `jointOptimal_iff`, `exact_nesting_value` | CT34 (i) | Parent and team design sets finite and nonempty; `J(x,y)=F(x)+G(y;θ(x))` | Partial minimization is exact, and the minimizers agree |
| `parentOptimal_of_constant_theta` | CT34 (ii) | `θ` does not depend on the parent's design | The team's optimized cost is a constant (an upkeep); the parent's argmin is the argmin of `F` alone |
| `strongConvex_lipschitz_gap`, `weak_coupling_pointwise`, `weak_coupling_gap`, `weak_coupling_parent_regret` | CT34 (iii) | `μ > 0`, `ε ≥ 0`; `G` satisfies the strong-convexity inequality in a distance `dist`; `Φ` is `L`-Lipschitz in `y` in the one-sided sense used in THEORY | Freezing the team at a `G`-minimizer overshoots by at most `(ε L)²/(2μ)`, and the parent's regret from optimizing the frozen cost is at most that bound.  The coupling sign `ε ≥ 0` is stated (needed to keep the Lipschitz bound's direction) |
| `D_comp_IB_convex`, `L_convex` | CT4, convex lower bound | `D` convex and nonincreasing on the image of `IB`; `IB` concave on `s` | `D ∘ IB` is convex, and `L(I)=D(IB(I))+κ I` is convex (the `κ I` term is affine at every sign of `κ`) |
| `zero_isMinOn_iff`, `first_bit_pays_iff`, `convexOn_pos_min_of_neg_right_slope`, `exists_neg_right_slope_of_not_min` | CT4, first-bit sign | Stated with right slopes from `0` on `[0, ∞)`, not a two-sided derivative | `0` is a minimizer iff every right slope from `0` is nonnegative; hence `0` fails to minimize iff some right slope is negative, and any minimizer is then strictly positive |
| `not_certified_below_Bmin` | CT22, certified `B_min` | `0 < ε < 1`, `0 < max θ`, `0 ≤ B < B_min` | No design is Lundberg-certified (THEORY's wording: the bound is sufficient, not that every design ruins) |
| `certified_at_Bslack` | CT22, `B_slack` | `θ(d_E) > 0`, `B ≥ B_slack` | The expected-cost optimum is certified |
| `expected_cost_opt_is_constrained_opt` | CT22, slack case | `d_E` minimizes `J` over all designs and is certified | `d_E` is optimal among certified designs; the cap is slack.  No KKT is used |
| `Bmin_le_Bslack` | CT22 | `0 < ε < 1`, `0 < θ(d_E)` (hence `0 < max θ`) | `B_min ≤ B_slack` |
| `minimizer_on_lower_hull` | KEYSTONE_NOTE §4, first sentence | `R ≥ 0`; `φ(K)=K+R(1+ε_K)` on `{0,…,n}` | Every minimizer of `φ` lies on the lower convex hull of `{(K, ε_K)}` |
| `n60_from_zero_leftmost` | KEYSTONE_NOTE §4, adjacent test | `R ≥ 0` and discrete convexity of `ε` (first differences nondecreasing) | Walking from `0` and taking every paying adjacent step returns a leftmost minimizer of `φ` |
| `n60_as_written_zero_hole` | N60 as written; the `K*=0` hole | Same, and the first step does not pay | No later step pays; the true leftmost minimizer is `0`; N60 as written (`1 + #{k ≥ 2 : step k−1 pays}`) equals `1` |

## What is not formalized

None of the following is claimed as proved in Lean.

- The hypothesis in CORE §3 (a claim about the real world).
- Convexity of `ε_K` in Model S, still unproved on paper (CORE §4, KEYSTONE_NOTE).  The increment *formula* in N60 is formalized only as a consequence of discrete convexity, which is an assumption here.
- The full hull-vertex walk on a non-convex `ε` curve (KEYSTONE_NOTE §4's increment test on hull edges that skip integers).  What is proved is that every minimizer lies on the lower hull, and that the adjacent test works once `ε` is discrete-convex.
- CT4's Gaussian AR(1) closed form `I* = ½ log₂(2 ln 2 · a² · Var / κ)`.
- CT20 (i) in a continuous parameter set (Weierstrass on a compact rate set).  Only the finite-menu existence result and the `K ≤ J(d₁)/h` bound are formalized.
- CT21 (L1–L3): Kalman–Bucy, Wiener spectral factorization, interlacing, degree.
- CT22's in-between binding region, the multiplier `μ_s = −m'/θ'`, and the quasiconvexity / uniqueness hypotheses that justify it.
- CT1–CT3 (rate–distortion, ergodic theorem, lead-time cap).
- CT5, CT8, CT9 (Blackwell/garbling, hold-or-fade as an integral test).
- CT11–CT19, CT23, CT25, CT26–CT32, CT35–CT43, and the Master Theorem in the class `𝓜_LG`.
- Any information-theoretic construction of `D` or `IB`; they enter CT4 as functions with the stated convexity and monotonicity.

## Layout

```
formal/lean/
  lakefile.toml         # package `gtao`, library `GTAO`, Mathlib pin
  lean-toolchain
  lake-manifest.json
  GTAO.lean             # root import
  GTAO/Cost.lean        # J, argmin, J*
  GTAO/CT33.lean
  GTAO/CT20.lean
  GTAO/CT10.lean
  GTAO/CT34.lean
  GTAO/CT4.lean
  GTAO/CT22.lean
  GTAO/Hull.lean
```

Build artifacts under `.lake/` are gitignored.
