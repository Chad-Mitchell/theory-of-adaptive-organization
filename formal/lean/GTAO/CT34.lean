/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of THEORY CT34, for OPEN_WORK T19.
-/
module

public import Mathlib.Algebra.Order.Archimedean.Real.Basic
public import Mathlib.Data.Set.Finite.Lemmas
public import Mathlib.Tactic.FieldSimp
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.Ring
public import Mathlib.Tactic.Abel

/-!
# CT34: exact nesting, and the error when coupling is weak

From THEORY.md Appendix B.10 (CT34):

> Parent design \(x\), team design \(y\); \(J(x,y)=F(x)+G(y;\theta(x))\),
> where \(\theta\) is what the parent passes the team;
> \(J_T^*(\theta)=\min_y G(y;\theta)\).
>
> (i) **Exactness (partial minimization):**
> \(\min_{x,y} J=\min_x[F(x)+J_T^*(\theta(x))]\), and the minimizers agree.
>
> (ii) \(J_T^*\) is a constant (an upkeep \(h\)) if \(\theta\) does not depend
> on \(x\); then the parent's argmin ignores the team entirely.
>
> (iii) **Error bound when the team is only weakly coupled.**
> \(J=F(x)+G(y)+\varepsilon\cdot\Phi(x,y)\) with \(G\) \(\mu\)-strongly convex
> and \(\Phi\) \(L\)-Lipschitz in \(y\), \(y^0=\arg\min G\).  Freezing the
> team at \(y^0\) costs at most \((\varepsilon L)^2/(2\mu)\), and the parent's
> regret from optimizing the frozen cost is at most that same bound.

Part (iv) of CT34 is a numerical illustration of pooling (CT14), not formalized
here.  Existence of the minima is granted by taking the parent and team design
sets finite and nonempty.
-/

@[expose] public section

open Set

variable {X Y Θ : Type*} [Fintype X] [Nonempty X] [Fintype Y] [Nonempty Y]

/-- Joint cost: parent term plus team term at the parameter the parent passes. -/
def parentTeamJ (F : X → ℝ) (G : Y → Θ → ℝ) (θ : X → Θ) (x : X) (y : Y) : ℝ :=
  F x + G y (θ x)

/-- A team design that attains `min_y G(y; t)`. -/
def IsTeamMin (G : Y → Θ → ℝ) (t : Θ) (y : Y) : Prop :=
  ∀ y' : Y, G y t ≤ G y' t

lemma exists_teamMin (G : Y → Θ → ℝ) (t : Θ) : ∃ y : Y, IsTeamMin G t y := by
  obtain ⟨y, _, hy⟩ :=
    exists_min_image (univ : Set Y) (fun y => G y t) finite_univ univ_nonempty
  exact ⟨y, fun y' => hy y' (mem_univ y')⟩

/-- The team's optimized cost as a function of the parameter the parent passes. -/
noncomputable def JstarT (G : Y → Θ → ℝ) (t : Θ) : ℝ :=
  G (Classical.choose (exists_teamMin G t)) t

lemma isTeamMin_choose (G : Y → Θ → ℝ) (t : Θ) :
    IsTeamMin G t (Classical.choose (exists_teamMin G t)) :=
  Classical.choose_spec (exists_teamMin G t)

lemma JstarT_le (G : Y → Θ → ℝ) (t : Θ) (y : Y) : JstarT G t ≤ G y t :=
  isTeamMin_choose G t y

lemma IsTeamMin.JstarT_eq {G : Y → Θ → ℝ} {t : Θ} {y : Y} (hy : IsTeamMin G t y) :
    JstarT G t = G y t :=
  le_antisymm (JstarT_le G t y) (hy _)

/-- The pair `(x,y)` minimizes the joint cost. -/
def JointOptimal (F : X → ℝ) (G : Y → Θ → ℝ) (θ : X → Θ) (x : X) (y : Y) : Prop :=
  ∀ x' : X, ∀ y' : Y, parentTeamJ F G θ x y ≤ parentTeamJ F G θ x' y'

/-- The parent, seeing only the team's optimized cost, is optimal. -/
def ParentOptimal (F : X → ℝ) (G : Y → Θ → ℝ) (θ : X → Θ) (x : X) : Prop :=
  ∀ x' : X, F x + JstarT G (θ x) ≤ F x' + JstarT G (θ x')

/-- The reduced parent cost \(F(x)+J_T^*(\theta(x))\). -/
noncomputable def parentReduced (F : X → ℝ) (G : Y → Θ → ℝ) (θ : X → Θ) (x : X) : ℝ :=
  F x + JstarT G (θ x)

omit [Fintype X] [Nonempty X] in
lemma parentReduced_le (F : X → ℝ) (G : Y → Θ → ℝ) (θ : X → Θ) (x : X) (y : Y) :
    parentReduced F G θ x ≤ parentTeamJ F G θ x y := by
  simp only [parentReduced, parentTeamJ]
  linarith [JstarT_le G (θ x) y]

omit [Fintype X] [Nonempty X] in
/-- CT34 (i), exactness: a joint minimizer is a parent minimizer of the reduced
cost together with a team minimizer at the parameter the parent passed, and
conversely. -/
theorem jointOptimal_iff (F : X → ℝ) (G : Y → Θ → ℝ) (θ : X → Θ) (x : X) (y : Y) :
    JointOptimal F G θ x y ↔ ParentOptimal F G θ x ∧ IsTeamMin G (θ x) y := by
  constructor
  · intro h
    have hT : IsTeamMin G (θ x) y := by
      intro y'
      have hyy := h x y'
      simp only [parentTeamJ] at hyy
      linarith
    refine ⟨?_, hT⟩
    intro x'
    let y' : Y := Classical.choose (exists_teamMin G (θ x'))
    have hy' : IsTeamMin G (θ x') y' := isTeamMin_choose G (θ x')
    have hxy := h x' y'
    simp only [parentTeamJ] at hxy
    rw [hT.JstarT_eq, hy'.JstarT_eq]
    exact hxy
  · rintro ⟨hP, hT⟩
    intro x' y'
    calc
      parentTeamJ F G θ x y = parentReduced F G θ x := by
        simp [parentTeamJ, parentReduced, hT.JstarT_eq]
      _ ≤ parentReduced F G θ x' := hP x'
      _ ≤ parentTeamJ F G θ x' y' := parentReduced_le F G θ x' y'

omit [Fintype X] [Nonempty X] in
/-- CT34 (i), values: the joint minimum equals the reduced parent minimum. -/
theorem exact_nesting_value (F : X → ℝ) (G : Y → Θ → ℝ) (θ : X → Θ) (x : X) (y : Y)
    (h : JointOptimal F G θ x y) :
    parentTeamJ F G θ x y = parentReduced F G θ x := by
  have hT : IsTeamMin G (θ x) y := ((jointOptimal_iff F G θ x y).mp h).2
  simp only [parentTeamJ, parentReduced, hT.JstarT_eq]

omit [Fintype X] [Nonempty X] in
/-- CT34 (ii): if the parent passes a parameter that does not depend on its
own design, the team's optimized cost is a constant (an upkeep), and the
parent's argmin is the argmin of `F` alone. -/
theorem parentOptimal_of_constant_theta (F : X → ℝ) (G : Y → Θ → ℝ) (θ : X → Θ)
    (hθ : ∀ x x' : X, θ x = θ x') (x : X) :
    ParentOptimal F G θ x ↔ ∀ x' : X, F x ≤ F x' := by
  constructor
  · intro h x'
    have hx := h x'
    have : JstarT G (θ x) = JstarT G (θ x') := by rw [hθ x x']
    linarith
  · intro h x'
    have : JstarT G (θ x) = JstarT G (θ x') := by rw [hθ x x']
    linarith [h x']

/-! ## CT34 (iii): weak-coupling error bound

The next lemmas take the strong-convexity and Lipschitz inequalities as
hypotheses, matching the written proof in THEORY.md.  The coupling
coefficient `ε` is taken nonnegative, so the Lipschitz lower bound on `Φ`
keeps its direction when multiplied by `ε`.
-/

/-- Completing the square: \((\mu/2)d^2-\varepsilon L d\ge -(\varepsilon L)^2/(2\mu)\). -/
lemma strongConvex_lipschitz_nonneg (μ ε L d : ℝ) (hμ : 0 < μ) :
    0 ≤ μ / 2 * d ^ 2 - ε * L * d + (ε * L) ^ 2 / (2 * μ) := by
  have hident :
      μ / 2 * d ^ 2 - ε * L * d + (ε * L) ^ 2 / (2 * μ)
        = μ / 2 * (d - ε * L / μ) ^ 2 := by
    field_simp [hμ.ne']
    ring
  have hsq : 0 ≤ μ / 2 * (d - ε * L / μ) ^ 2 :=
    mul_nonneg (by linarith) (sq_nonneg _)
  rwa [hident]

lemma strongConvex_lipschitz_gap (μ ε L d : ℝ) (hμ : 0 < μ) :
    -(ε * L) ^ 2 / (2 * μ) ≤ μ / 2 * d ^ 2 - ε * L * d := by
  have hident :
      μ / 2 * d ^ 2 - ε * L * d + (ε * L) ^ 2 / (2 * μ)
        = μ / 2 * (d - ε * L / μ) ^ 2 := by
    field_simp [hμ.ne']
    ring
  have hsq : 0 ≤ μ / 2 * (d - ε * L / μ) ^ 2 :=
    mul_nonneg (by linarith) (sq_nonneg _)
  have hsum :
      0 ≤ μ / 2 * d ^ 2 - ε * L * d + (ε * L) ^ 2 / (2 * μ) := by
    rwa [hident]
  -- `-b ≤ a` iff `0 ≤ a + b`.
  have hiff : -(ε * L) ^ 2 / (2 * μ) ≤ μ / 2 * d ^ 2 - ε * L * d ↔
      0 ≤ μ / 2 * d ^ 2 - ε * L * d + (ε * L) ^ 2 / (2 * μ) := by
    constructor
    · intro h
      have := add_le_add_right h ((ε * L) ^ 2 / (2 * μ))
      ring_nf at this ⊢
      exact this
    · intro h
      have := add_le_add_right h (-((ε * L) ^ 2 / (2 * μ)))
      ring_nf at this ⊢
      exact this
  exact hiff.mpr hsum

variable {X Y : Type*}

/-- Frozen (parent-only) cost, team held at `y₀`. -/
def frozenCost (F : X → ℝ) (G : Y → ℝ) (Φ : X → Y → ℝ) (ε : ℝ) (y0 : Y) (x : X) : ℝ :=
  F x + G y0 + ε * Φ x y0

/-- Coupled joint cost. -/
def coupledJ (F : X → ℝ) (G : Y → ℝ) (Φ : X → Y → ℝ) (ε : ℝ) (x : X) (y : Y) : ℝ :=
  F x + G y + ε * Φ x y

/-- Pointwise bound: every team design is at most \((\varepsilon L)^2/(2\mu)\)
cheaper than freezing at `y₀`. -/
theorem weak_coupling_pointwise (F : X → ℝ) (G : Y → ℝ) (Φ : X → Y → ℝ)
    (ε μ L : ℝ) (y0 : Y) (dist : Y → ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε)
    (hstrong : ∀ y : Y, G y0 + μ / 2 * (dist y) ^ 2 ≤ G y)
    (hlip : ∀ x : X, ∀ y : Y, Φ x y0 - L * dist y ≤ Φ x y)
    (x : X) (y : Y) :
    frozenCost F G Φ ε y0 x - (ε * L) ^ 2 / (2 * μ) ≤ coupledJ F G Φ ε x y := by
  have h1 := hstrong y
  have h2 := hlip x y
  have hΦ : ε * (Φ x y0 - L * dist y) ≤ ε * Φ x y :=
    mul_le_mul_of_nonneg_left h2 hε
  -- Expand the target as a chain of lower bounds.
  have hnn := strongConvex_lipschitz_nonneg μ ε L (dist y) hμ
  have hleft :
      frozenCost F G Φ ε y0 x - (ε * L) ^ 2 / (2 * μ)
        ≤ F x + (G y0 + μ / 2 * dist y ^ 2) + ε * (Φ x y0 - L * dist y) := by
    have hdiff :
        F x + (G y0 + μ / 2 * dist y ^ 2) + ε * (Φ x y0 - L * dist y)
          - (frozenCost F G Φ ε y0 x - (ε * L) ^ 2 / (2 * μ))
          = μ / 2 * dist y ^ 2 - ε * L * dist y + (ε * L) ^ 2 / (2 * μ) := by
      simp only [frozenCost]
      ring
    exact sub_nonneg.mp (hdiff ▸ hnn)
  have hright :
      F x + (G y0 + μ / 2 * dist y ^ 2) + ε * (Φ x y0 - L * dist y)
        ≤ coupledJ F G Φ ε x y := by
    simp only [coupledJ]
    linarith [h1, hΦ]
  exact hleft.trans hright

/-- `y₀` is always feasible, so the frozen cost is an upper bound on the
`y`-minimum. -/
theorem frozen_ge_min (F : X → ℝ) (G : Y → ℝ) (Φ : X → Y → ℝ) (ε : ℝ)
    (y0 : Y) (x : X) (yMin : Y)
    (hMin : ∀ y' : Y, coupledJ F G Φ ε x yMin ≤ coupledJ F G Φ ε x y') :
    coupledJ F G Φ ε x yMin ≤ frozenCost F G Φ ε y0 x :=
  hMin y0

/-- Gap between the frozen cost and the `y`-minimum: at most
\((\varepsilon L)^2/(2\mu)\). -/
theorem weak_coupling_gap (F : X → ℝ) (G : Y → ℝ) (Φ : X → Y → ℝ)
    (ε μ L : ℝ) (y0 yMin : Y) (dist : Y → ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε)
    (hstrong : ∀ y : Y, G y0 + μ / 2 * (dist y) ^ 2 ≤ G y)
    (hlip : ∀ x : X, ∀ y : Y, Φ x y0 - L * dist y ≤ Φ x y)
    (x : X)
    (hMin : ∀ y' : Y, coupledJ F G Φ ε x yMin ≤ coupledJ F G Φ ε x y') :
    coupledJ F G Φ ε x yMin ≤ frozenCost F G Φ ε y0 x ∧
      frozenCost F G Φ ε y0 x - coupledJ F G Φ ε x yMin ≤ (ε * L) ^ 2 / (2 * μ) := by
  have hU : coupledJ F G Φ ε x yMin ≤ frozenCost F G Φ ε y0 x :=
    frozen_ge_min F G Φ ε y0 x yMin hMin
  have hL := weak_coupling_pointwise F G Φ ε μ L y0 dist hμ hε hstrong hlip x yMin
  exact ⟨hU, by linarith⟩

/-- Parent regret from optimizing the frozen cost: if `x₀` minimizes the
frozen cost, the joint-cost gap to any comparison design `xStar` is at
most `(ε L) ^ 2 / (2 μ)`.  The intended CT34 (iii) reading takes `xStar`
to be a joint minimizer of the true cost; the same bound holds for an
arbitrary comparison point, so that hypothesis is not required. -/
theorem weak_coupling_parent_regret (F : X → ℝ) (G : Y → ℝ) (Φ : X → Y → ℝ)
    (ε μ L : ℝ) (y0 : Y) (dist : Y → ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε)
    (hstrong : ∀ y : Y, G y0 + μ / 2 * (dist y) ^ 2 ≤ G y)
    (hlip : ∀ x : X, ∀ y : Y, Φ x y0 - L * dist y ≤ Φ x y)
    (ymin : X → Y)
    (hymin : ∀ x : X, ∀ y' : Y,
      coupledJ F G Φ ε x (ymin x) ≤ coupledJ F G Φ ε x y')
    (x0 xStar : X)
    (hx0 : ∀ x' : X, frozenCost F G Φ ε y0 x0 ≤ frozenCost F G Φ ε y0 x') :
    coupledJ F G Φ ε x0 (ymin x0) - coupledJ F G Φ ε xStar (ymin xStar)
      ≤ (ε * L) ^ 2 / (2 * μ) := by
  have h_x0_le : coupledJ F G Φ ε x0 (ymin x0) ≤ frozenCost F G Φ ε y0 x0 :=
    frozen_ge_min F G Φ ε y0 x0 (ymin x0) (hymin x0)
  have h_frozen : frozenCost F G Φ ε y0 x0 ≤ frozenCost F G Φ ε y0 xStar :=
    hx0 xStar
  have h_gap :=
    weak_coupling_gap F G Φ ε μ L y0 (ymin xStar) dist hμ hε hstrong hlip
      xStar (hymin xStar)
  linarith [h_gap.2]
