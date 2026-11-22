/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lemmas M, Z and X of `theory/LAYER_CONVEXITY.md` §3 (PR #145): the
quadrangle (Monge) inequality for weighted 1-D clustering of a
non-increasing gain, the terminal-band lemma, and the exchange argument
giving convexity of the optimal band cost in the number of bands.
For OPEN_WORK T19.
-/
module

public import Mathlib.Basic.Real.Basic
public import Mathlib.Algebra.BigOperators.Intervals
public import Mathlib.Algebra.BigOperators.Ring.Finset
public import Mathlib.Algebra.Order.BigOperators.Group.Finset
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.FieldSimp
public import Mathlib.Tactic.Positivity
public import Mathlib.Tactic.Ring
public import Mathlib.Tactic.GCongr

/-!
# Band model 𝓑: Monge costs and convexity in the number of bands
-/

@[expose] public section

open Finset

namespace BandMonge

/-! ## The two-block algebra -/

/-- `S²/M`, the explained part of a block with mass `M` and first moment `S`. -/
noncomputable def f (S M : ℝ) : ℝ := S ^ 2 / M

/-- Merge gain: `f(X) + f(Y) - f(X ∪ Y) = M_X M_Y/(M_X+M_Y) (m_X - m_Y)²`. -/
lemma merge_gain {SX MX SY MY : ℝ} (hX : 0 < MX) (hY : 0 < MY) :
    f SX MX + f SY MY - f (SX + SY) (MX + MY) =
      MX * MY / (MX + MY) * (SX / MX - SY / MY) ^ 2 := by
  unfold f
  field_simp
  ring

lemma merge_gain_nonneg {SX MX SY MY : ℝ} (hX : 0 < MX) (hY : 0 < MY) :
    f (SX + SY) (MX + MY) ≤ f SX MX + f SY MY := by
  have := merge_gain (SX := SX) (SY := SY) hX hY
  have : 0 ≤ MX * MY / (MX + MY) * (SX / MX - SY / MY) ^ 2 := by positivity
  linarith

/-- **Core of Lemma M.**  Three consecutive blocks with positive masses and
non-increasing means `m_A ≥ m_B ≥ m_C`:
`f(A∪B∪C) + f(B) ≤ f(A∪B) + f(B∪C)`. -/
lemma quadrangle_core {SA MA SB MB SC MC : ℝ} (hA : 0 < MA) (hB : 0 < MB) (hC : 0 < MC)
    (hAB : SB / MB ≤ SA / MA) (hBC : SC / MC ≤ SB / MB) :
    f (SA + SB + SC) (MA + MB + MC) + f SB MB ≤ f (SA + SB) (MA + MB) + f (SB + SC) (MB + MC) := by
  have g1 := merge_gain (SX := SA) (SY := SB) hA hB
  have g2 := merge_gain (SX := SA) (SY := SB + SC) hA (add_pos hB hC)
  have e1 : SA + (SB + SC) = SA + SB + SC := by ring
  have e2 : MA + (MB + MC) = MA + MB + MC := by ring
  rw [e1, e2] at g2
  -- the mean of B ∪ C is at most the mean of B
  have hmBC : (SB + SC) / (MB + MC) ≤ SB / MB := by
    rw [div_le_div_iff₀ (add_pos hB hC) hB]
    rw [div_le_div_iff₀ hC hB] at hBC
    nlinarith
  have hu : 0 ≤ SA / MA - SB / MB := by linarith
  have huv : SA / MA - SB / MB ≤ SA / MA - (SB + SC) / (MB + MC) := by linarith
  have hsq : (SA / MA - SB / MB) ^ 2 ≤ (SA / MA - (SB + SC) / (MB + MC)) ^ 2 :=
    pow_le_pow_left₀ hu huv 2
  have hh : MA * MB / (MA + MB) ≤ MA * (MB + MC) / (MA + MB + MC) := by
    rw [div_le_div_iff₀ (by positivity) (by positivity)]
    nlinarith [mul_pos hA hA, mul_pos hA hC]
  have hgain : MA * MB / (MA + MB) * (SA / MA - SB / MB) ^ 2 ≤
      MA * (MB + MC) / (MA + MB + MC) * (SA / MA - (SB + SC) / (MB + MC)) ^ 2 :=
    mul_le_mul hh hsq (sq_nonneg _) (by positivity)
  linarith

/-- **Core of Lemma Z.**  With `0 ≤ m_B ≤ m_A`, merging `A` into `B` costs at
most `f(A)`: `f(A) + f(B) - f(A∪B) ≤ f(A)`. -/
lemma terminal_core {SA MA SB MB : ℝ} (hA : 0 < MA) (hB : 0 < MB)
    (hB0 : 0 ≤ SB / MB) (hAB : SB / MB ≤ SA / MA) :
    f SA MA + f SB MB - f (SA + SB) (MA + MB) ≤ f SA MA := by
  rw [merge_gain hA hB]
  have h1 : MA * MB / (MA + MB) ≤ MA := by
    rw [div_le_iff₀ (by positivity)]; nlinarith
  have h2 : (SA / MA - SB / MB) ^ 2 ≤ (SA / MA) ^ 2 := by
    apply pow_le_pow_left₀ (by linarith) (by linarith)
  have h3 : f SA MA = MA * (SA / MA) ^ 2 := by
    unfold f; field_simp
  rw [h3]
  exact mul_le_mul h1 h2 (sq_nonneg _) hA.le


/-! ## Interval aggregates of a weighted gain profile -/

section Intervals

variable (μ W : ℕ → ℝ)

/-- Mass of the cells `[a, b)`. -/
noncomputable def M (a b : ℕ) : ℝ := ∑ x ∈ Ico a b, μ x
/-- First moment `Σ μ W` over `[a, b)`. -/
noncomputable def S (a b : ℕ) : ℝ := ∑ x ∈ Ico a b, μ x * W x
/-- Second moment `Σ μ W²` over `[a, b)`. -/
noncomputable def Q (a b : ℕ) : ℝ := ∑ x ∈ Ico a b, μ x * W x ^ 2

/-- Cost of one band `[a, b)` at its optimal level (the weighted mean):
`Σ μ (W - m)² = Q - S²/M`.  An empty band costs `0`. -/
noncomputable def w (a b : ℕ) : ℝ := Q μ W a b - f (S μ W a b) (M μ a b)

/-- Cost of the terminal band `[a, n)`, whose level is pinned to `0`. -/
noncomputable def z (n a : ℕ) : ℝ := Q μ W a n

/-- The band cost as one cost on the points `0, …, n+1`: an ordinary band
`[a, b)` for `b ≤ n`, and the terminal band `[a, n)` for the last link
`a → n+1`. -/
noncomputable def linkCost (n a b : ℕ) : ℝ := if b ≤ n then w μ W a b else z μ W n a

variable {μ W}

lemma w_self (a : ℕ) : w μ W a a = 0 := by simp [w, Q, S, M, f]

lemma M_add {a b c : ℕ} (h1 : a ≤ b) (h2 : b ≤ c) : M μ a c = M μ a b + M μ b c :=
  (sum_Ico_consecutive _ h1 h2).symm
lemma S_add {a b c : ℕ} (h1 : a ≤ b) (h2 : b ≤ c) : S μ W a c = S μ W a b + S μ W b c :=
  (sum_Ico_consecutive _ h1 h2).symm
lemma Q_add {a b c : ℕ} (h1 : a ≤ b) (h2 : b ≤ c) : Q μ W a c = Q μ W a b + Q μ W b c :=
  (sum_Ico_consecutive _ h1 h2).symm

variable {n : ℕ}

lemma M_pos (hμ : ∀ x < n, 0 < μ x) {a b : ℕ} (hab : a < b) (hb : b ≤ n) : 0 < M μ a b :=
  sum_pos (fun x hx => hμ x (by simp at hx; omega)) ⟨a, by simp; omega⟩

lemma S_nonneg (hμ : ∀ x < n, 0 < μ x) (hW0 : ∀ x < n, 0 ≤ W x) {a b : ℕ} (hb : b ≤ n) :
    0 ≤ S μ W a b :=
  sum_nonneg fun x hx => by
    simp at hx; exact mul_nonneg (hμ x (by omega)).le (hW0 x (by omega))

/-- Adjacent blocks of a non-increasing profile have non-increasing means. -/
lemma mean_le (hμ : ∀ x < n, 0 < μ x) (hW : ∀ x y, x ≤ y → y < n → W y ≤ W x)
    {a b c : ℕ} (hab : a < b) (hbc : b < c) (hc : c ≤ n) :
    S μ W b c / M μ b c ≤ S μ W a b / M μ a b := by
  rw [div_le_div_iff₀ (M_pos hμ hbc hc) (M_pos hμ hab (by omega))]
  have key : S μ W a b * M μ b c - S μ W b c * M μ a b =
      ∑ x ∈ Ico a b, ∑ y ∈ Ico b c, μ x * μ y * (W x - W y) := by
    rw [S, M, S, M, sum_mul_sum, mul_comm, sum_mul_sum, ← sum_sub_distrib]
    refine sum_congr rfl fun x _ => ?_
    rw [← sum_sub_distrib]
    exact sum_congr rfl fun y _ => by ring
  have : 0 ≤ ∑ x ∈ Ico a b, ∑ y ∈ Ico b c, μ x * μ y * (W x - W y) := by
    refine sum_nonneg fun x hx => sum_nonneg fun y hy => ?_
    simp at hx hy
    have := hW x y (by omega) (by omega)
    exact mul_nonneg (mul_pos (hμ x (by omega)) (hμ y (by omega))).le (by linarith)
  linarith

/-- **Lemma M (quadrangle / Monge inequality).**  For positive weights and a
non-increasing profile, for `a ≤ b ≤ c ≤ d ≤ n`:
`w(a,c) + w(b,d) ≤ w(a,d) + w(b,c)`. -/
theorem quadrangle (hμ : ∀ x < n, 0 < μ x) (hW : ∀ x y, x ≤ y → y < n → W y ≤ W x)
    {a b c d : ℕ} (hab : a ≤ b) (hbc : b ≤ c) (hcd : c ≤ d) (hd : d ≤ n) :
    w μ W a c + w μ W b d ≤ w μ W a d + w μ W b c := by
  rcases hab.eq_or_lt with rfl | hab'
  · exact le_of_eq (add_comm _ _)
  rcases hcd.eq_or_lt with rfl | hcd'
  · exact le_rfl
  rcases hbc.eq_or_lt with rfl | hbc'
  · -- superadditivity: `w(a,b) + w(b,d) ≤ w(a,d)`
    rw [w_self, add_zero]
    simp only [w]
    rw [Q_add hab hcd, S_add hab hcd, M_add hab hcd]
    have := merge_gain_nonneg (SX := S μ W a b) (SY := S μ W b d)
      (M_pos hμ hab' (by omega)) (M_pos hμ hcd' hd)
    linarith
  have hA := M_pos hμ hab' (by omega)
  have hB := M_pos hμ hbc' (by omega)
  have hC := M_pos hμ hcd' hd
  have core := quadrangle_core hA hB hC (mean_le hμ hW hab' hbc' (by omega))
    (mean_le hμ hW hbc' hcd' hd)
  have hS1 := S_add (μ := μ) (W := W) hab hbc
  have hS2 := S_add (μ := μ) (W := W) hbc hcd
  have hS3 := S_add (μ := μ) (W := W) hab (hbc.trans hcd)
  have hM1 := M_add (μ := μ) hab hbc
  have hM2 := M_add (μ := μ) hbc hcd
  have hM3 := M_add (μ := μ) hab (hbc.trans hcd)
  have hQ1 := Q_add (μ := μ) (W := W) hab hbc
  have hQ2 := Q_add (μ := μ) (W := W) hbc hcd
  have hQ3 := Q_add (μ := μ) (W := W) hab (hbc.trans hcd)
  rw [hS2] at hS3
  rw [hM2] at hM3
  simp only [w]
  rw [hS1, hS2, hS3, hM1, hM2, hM3]
  have e1 : S μ W a b + (S μ W b c + S μ W c d) = S μ W a b + S μ W b c + S μ W c d := by ring
  have e2 : M μ a b + (M μ b c + M μ c d) = M μ a b + M μ b c + M μ c d := by ring
  rw [e1, e2]
  linarith

/-- **Lemma Z (terminal band).**  For positive weights and a non-increasing,
**non-negative** profile, for `a ≤ b ≤ c ≤ n`:
`w(a,c) + z(b) ≤ z(a) + w(b,c)`.  (Non-negativity is needed: the note's
"same hypothesis" does not supply it.) -/
theorem terminal (hμ : ∀ x < n, 0 < μ x) (hW : ∀ x y, x ≤ y → y < n → W y ≤ W x)
    (hW0 : ∀ x < n, 0 ≤ W x) {a b c : ℕ} (hab : a ≤ b) (hbc : b ≤ c) (hc : c ≤ n) :
    w μ W a c + z μ W n b ≤ z μ W n a + w μ W b c := by
  simp only [z]
  rw [Q_add hab (hbc.trans hc)]
  rcases hab.eq_or_lt with rfl | hab'
  · simp only [Q, Ico_self, sum_empty]; linarith
  rcases hbc.eq_or_lt with rfl | hbc'
  · rw [w_self]
    have : 0 ≤ f (S μ W a b) (M μ a b) :=
      div_nonneg (sq_nonneg _) (M_pos hμ hab' (by omega)).le
    simp only [w]; linarith
  have hA := M_pos hμ hab' (by omega)
  have hB := M_pos hμ hbc' hc
  have core := terminal_core hA hB (div_nonneg (S_nonneg hμ hW0 hc) hB.le)
    (mean_le hμ hW hab' hbc' hc)
  simp only [w]
  rw [Q_add hab hbc, S_add hab hbc, M_add hab hbc]
  linarith

/-- The unified link cost on `0, …, n+1` is Monge (Lemmas M and Z). -/
theorem linkCost_monge (hμ : ∀ x < n, 0 < μ x) (hW : ∀ x y, x ≤ y → y < n → W y ≤ W x)
    (hW0 : ∀ x < n, 0 ≤ W x) {a b c d : ℕ} (hab : a ≤ b) (hbc : b ≤ c) (hcd : c ≤ d) :
    linkCost μ W n a c + linkCost μ W n b d ≤ linkCost μ W n a d + linkCost μ W n b c := by
  unfold linkCost
  by_cases h1 : d ≤ n
  · simp only [hcd.trans h1, h1, ↓reduceIte]
    exact quadrangle hμ hW hab hbc hcd h1
  by_cases h2 : c ≤ n
  · simp only [h2, h1, ↓reduceIte]
    exact terminal hμ hW hW0 hab hbc h2
  simp only [h2, h1, ↓reduceIte, le_refl]

end Intervals

/-! ## Lemma X: the exchange argument for Monge `k`-link paths -/

section Exchange

variable (c : ℕ → ℕ → ℝ) (T : ℕ)

/-- A `k`-link monotone path from `0` to `T`. -/
def IsPath (k : ℕ) (x : ℕ → ℕ) : Prop := x 0 = 0 ∧ x k = T ∧ ∀ i < k, x i ≤ x (i + 1)

/-- Total cost of the first `k` links of `x`. -/
noncomputable def pathCost (k : ℕ) (x : ℕ → ℕ) : ℝ := ∑ i ∈ range k, c (x i) (x (i + 1))

/-- Monge (quadrangle) condition on the cost of a link. -/
def Monge : Prop := ∀ a b c' d, a ≤ b → b ≤ c' → c' ≤ d → c a c' + c b d ≤ c a d + c b c'

/-- Tail swap at `s`: `p₀ … pₛ, q_{s+2}, q_{s+3}, …`. -/
def swapP (s : ℕ) (p q : ℕ → ℕ) (i : ℕ) : ℕ := if i ≤ s then p i else q (i + 1)
/-- Tail swap at `s`: `q₀ … q_{s+1}, p_{s+1}, p_{s+2}, …`. -/
def swapQ (s : ℕ) (p q : ℕ → ℕ) (i : ℕ) : ℕ := if i ≤ s + 1 then q i else p (i - 1)

variable {c T}

lemma sum_split (g : ℕ → ℝ) (s r : ℕ) :
    ∑ i ∈ range (s + 1 + r), g i = ∑ i ∈ range s, g i + g s + ∑ j ∈ range r, g (s + 1 + j) := by
  rw [sum_range_add, sum_range_succ]

/-- The exchange at a crossing index `s` (paths of lengths `s+1+r` and `s+1+r+2`). -/
lemma exchange_at (hM : Monge c) {s r : ℕ} {p q : ℕ → ℕ}
    (hP : IsPath T (s + 1 + r) p) (hQ : IsPath T (s + 1 + r + 2) q)
    (hcross : q (s + 2) ≤ p (s + 1)) (hps : p s ≤ q (s + 1)) :
    IsPath T (s + 1 + r + 1) (swapP s p q) ∧ IsPath T (s + 1 + r + 1) (swapQ s p q) ∧
      pathCost c (s + 1 + r + 1) (swapP s p q) + pathCost c (s + 1 + r + 1) (swapQ s p q) ≤
        pathCost c (s + 1 + r) p + pathCost c (s + 1 + r + 2) q := by
  obtain ⟨hP0, hPT, hPm⟩ := hP
  obtain ⟨hQ0, hQT, hQm⟩ := hQ
  have hq12 : q (s + 1) ≤ q (s + 2) := hQm (s + 1) (by omega)
  refine ⟨⟨?_, ?_, ?_⟩, ⟨?_, ?_, ?_⟩, ?_⟩
  · simp [swapP, hP0]
  · simp only [swapP, show ¬ (s + 1 + r + 1 ≤ s) by omega, ↓reduceIte]
    rw [← hQT]
  · intro i hi
    simp only [swapP]
    by_cases h1 : i + 1 ≤ s
    · simp only [show i ≤ s by omega, h1, ↓reduceIte]; exact hPm i (by omega)
    by_cases h2 : i = s
    · subst h2; simp only [le_refl, h1, ↓reduceIte]; exact hps.trans hq12
    · simp only [show ¬ i ≤ s by omega, h1, ↓reduceIte]; exact hQm (i + 1) (by omega)
  · simp [swapQ, hQ0]
  · simp only [swapQ, show ¬ (s + 1 + r + 1 ≤ s + 1) by omega, ↓reduceIte]
    rw [show s + 1 + r + 1 - 1 = s + 1 + r by omega, hPT]
  · intro i hi
    simp only [swapQ]
    by_cases h1 : i + 1 ≤ s + 1
    · simp only [show i ≤ s + 1 by omega, h1, ↓reduceIte]; exact hQm i (by omega)
    by_cases h2 : i = s + 1
    · subst h2; simp only [le_refl, h1, ↓reduceIte]
      rw [show s + 1 + 1 - 1 = s + 1 by omega]; omega
    · simp only [show ¬ i ≤ s + 1 by omega, h1, ↓reduceIte]
      have := hPm (i - 1) (by omega)
      rw [show i - 1 + 1 = i by omega] at this
      rw [show i + 1 - 1 = i by omega]
      exact this
  · -- cost bookkeeping: heads and tails are shared, the crossing is Monge
    have eP : pathCost c (s + 1 + r) p = ∑ i ∈ range s, c (p i) (p (i + 1)) +
        c (p s) (p (s + 1)) + ∑ j ∈ range r, c (p (s + 1 + j)) (p (s + 1 + j + 1)) :=
      sum_split _ s r
    have eQ : pathCost c (s + 1 + r + 2) q = ∑ i ∈ range (s + 1), c (q i) (q (i + 1)) +
        c (q (s + 1)) (q (s + 2)) + ∑ j ∈ range (r + 1), c (q (s + 2 + j)) (q (s + 2 + j + 1)) := by
      rw [pathCost, show s + 1 + r + 2 = (s + 1) + 1 + (r + 1) by omega, sum_split]
    have eP' : pathCost c (s + 1 + r + 1) (swapP s p q) = ∑ i ∈ range s, c (p i) (p (i + 1)) +
        c (p s) (q (s + 2)) + ∑ j ∈ range (r + 1), c (q (s + 2 + j)) (q (s + 2 + j + 1)) := by
      rw [pathCost, show s + 1 + r + 1 = s + 1 + (r + 1) by omega, sum_split]
      congr 1
      · congr 1
        · refine sum_congr rfl fun i hi => ?_
          simp at hi
          simp only [swapP, show i ≤ s by omega, show i + 1 ≤ s by omega, ↓reduceIte]
        · simp only [swapP, le_refl, show ¬ (s + 1 ≤ s) by omega, ↓reduceIte]
      · refine sum_congr rfl fun j _ => ?_
        simp only [swapP, show ¬ (s + 1 + j ≤ s) by omega, show ¬ (s + 1 + j + 1 ≤ s) by omega,
          ↓reduceIte]
        rw [show s + 1 + j + 1 = s + 2 + j by omega, show s + 2 + j + 1 = s + 2 + j + 1 by rfl]
    have eQ' : pathCost c (s + 1 + r + 1) (swapQ s p q) = ∑ i ∈ range (s + 1), c (q i) (q (i + 1)) +
        c (q (s + 1)) (p (s + 1)) + ∑ j ∈ range r, c (p (s + 1 + j)) (p (s + 1 + j + 1)) := by
      rw [pathCost, show s + 1 + r + 1 = (s + 1) + 1 + r by omega, sum_split]
      congr 1
      · congr 1
        · refine sum_congr rfl fun i hi => ?_
          simp at hi
          simp only [swapQ, show i ≤ s + 1 by omega, show i + 1 ≤ s + 1 by omega, ↓reduceIte]
        · simp only [swapQ, le_refl, show ¬ (s + 1 + 1 ≤ s + 1) by omega, ↓reduceIte,
            Nat.add_sub_cancel]
      · refine sum_congr rfl fun j _ => ?_
        simp only [swapQ, show ¬ (s + 1 + 1 + j ≤ s + 1) by omega,
          show ¬ (s + 1 + 1 + j + 1 ≤ s + 1) by omega, ↓reduceIte]
        rw [show s + 1 + 1 + j - 1 = s + 1 + j by omega,
          show s + 1 + 1 + j + 1 - 1 = s + 1 + j + 1 by omega]
    have hmonge := hM (p s) (q (s + 1)) (q (s + 2)) (p (s + 1)) hps hq12 hcross
    rw [eP, eQ, eP', eQ']
    linarith

/-- **Lemma X (exchange).**  For a Monge link cost, any `k`-link path `P`
(`k ≥ 1`) and `(k+2)`-link path `Q` can be recombined into two `(k+1)`-link
paths of no larger total cost. -/
theorem exchange (hM : Monge c) {k : ℕ} (hk : 1 ≤ k) {p q : ℕ → ℕ}
    (hP : IsPath T k p) (hQ : IsPath T (k + 2) q) :
    ∃ p' q', IsPath T (k + 1) p' ∧ IsPath T (k + 1) q' ∧
      pathCost c (k + 1) p' + pathCost c (k + 1) q' ≤ pathCost c k p + pathCost c (k + 2) q := by
  classical
  have hex : ∃ s, s < k ∧ q (s + 2) ≤ p (s + 1) := by
    refine ⟨k - 1, by omega, ?_⟩
    rw [show k - 1 + 2 = k + 1 by omega, show k - 1 + 1 = k by omega, hP.2.1, ← hQ.2.1]
    exact hQ.2.2 (k + 1) (by omega)
  obtain ⟨s, hs, hcross, hps⟩ : ∃ s, s < k ∧ q (s + 2) ≤ p (s + 1) ∧ p s ≤ q (s + 1) := by
    refine ⟨Nat.find hex, (Nat.find_spec hex).1, (Nat.find_spec hex).2, ?_⟩
    rcases Nat.eq_zero_or_pos (Nat.find hex) with h | h
    · rw [h, hP.1]; exact Nat.zero_le _
    · have hmin := Nat.find_min hex (show Nat.find hex - 1 < Nat.find hex by omega)
      simp only [not_and, not_le] at hmin
      have := hmin (by have := (Nat.find_spec hex).1; omega)
      rw [show Nat.find hex - 1 + 2 = Nat.find hex + 1 by omega,
        show Nat.find hex - 1 + 1 = Nat.find hex by omega] at this
      exact this.le
  obtain ⟨r, rfl⟩ : ∃ r, k = s + 1 + r := ⟨k - s - 1, by omega⟩
  exact ⟨_, _, exchange_at hM hP hQ hcross hps⟩

/-- **Discrete convexity of the optimal cost.**  If `P`, `R`, `Q` are optimal
`k`-, `(k+1)`-, `(k+2)`-link paths (`k ≥ 1`) then
`2 E(k+1) ≤ E(k) + E(k+2)`. -/
theorem convex_of_monge (hM : Monge c) {k : ℕ} (hk : 1 ≤ k) {p q r : ℕ → ℕ}
    (hP : IsPath T k p) (hQ : IsPath T (k + 2) q)
    (hRopt : ∀ x, IsPath T (k + 1) x → pathCost c (k + 1) r ≤ pathCost c (k + 1) x) :
    2 * pathCost c (k + 1) r ≤ pathCost c k p + pathCost c (k + 2) q := by
  obtain ⟨p', q', hp', hq', hcost⟩ := exchange hM hk hP hQ
  linarith [hRopt p' hp', hRopt q' hq']

lemma path_le {k : ℕ} {x : ℕ → ℕ} (hx : IsPath T k x) {i : ℕ} (hi : i ≤ k) : x i ≤ T := by
  have step : ∀ j, i + j ≤ k → x i ≤ x (i + j) := by
    intro j
    induction j with
    | zero => intro _; exact le_rfl
    | succ j ih =>
      intro h
      exact (ih (by omega)).trans (hx.2.2 (i + j) (by omega))
  have := step (k - i) (by omega)
  rwa [show i + (k - i) = k by omega, hx.2.1] at this

lemma isPath_congr {k : ℕ} {x y : ℕ → ℕ} (h : ∀ i ≤ k, x i = y i) (hx : IsPath T k x) :
    IsPath T k y := by
  obtain ⟨h0, hT, hm⟩ := hx
  refine ⟨by rw [← h 0 (Nat.zero_le _), h0], by rw [← h k le_rfl, hT], fun i hi => ?_⟩
  rw [← h i hi.le, ← h (i + 1) hi]; exact hm i hi

lemma pathCost_congr {k : ℕ} {x y : ℕ → ℕ} (h : ∀ i ≤ k, x i = y i) :
    pathCost c k x = pathCost c k y :=
  sum_congr rfl fun i hi => by simp at hi; rw [h i hi.le, h (i + 1) hi]

/-- Optimal paths exist (there are finitely many paths up to their values on
`0, …, k`). -/
theorem exists_optimal {k : ℕ} (hne : ∃ x, IsPath T k x) :
    ∃ r, IsPath T k r ∧ ∀ x, IsPath T k x → pathCost c k r ≤ pathCost c k x := by
  classical
  let ext : (Fin (k + 1) → Fin (T + 1)) → ℕ → ℕ :=
    fun g i => if h : i < k + 1 then (g ⟨i, h⟩ : ℕ) else 0
  let restr : (ℕ → ℕ) → (Fin (k + 1) → Fin (T + 1)) := fun x i =>
    ⟨min (x i) T, Nat.lt_succ_of_le (min_le_right _ _)⟩
  have hagree : ∀ x, IsPath T k x → ∀ i ≤ k, x i = ext (restr x) i := by
    intro x hx i hi
    simp only [ext, restr, show i < k + 1 by omega, ↓reduceDIte]
    exact (min_eq_left (path_le hx hi)).symm
  let C := univ.filter fun g => IsPath T k (ext g)
  obtain ⟨x₀, hx₀⟩ := hne
  have hC : C.Nonempty := ⟨restr x₀, by simpa [C] using isPath_congr (hagree x₀ hx₀) hx₀⟩
  obtain ⟨g, hgC, hgmin⟩ := exists_min_image C (fun g => pathCost c k (ext g)) hC
  refine ⟨ext g, (mem_filter.1 hgC).2, fun x hx => ?_⟩
  rw [pathCost_congr (hagree x hx)]
  exact hgmin _ (by simpa [C] using isPath_congr (hagree x hx) hx)

end Exchange

/-! ## Theorem B for the band model -/

/-- **Theorem B (band model 𝓑, convexity in K).**  Positive weights, a
non-increasing non-negative gain profile on cells `0, …, n-1`.  A `k`-link
path `0 = x₀ ≤ … ≤ x_k = n+1` is a clustering into `k-1` ordinary bands
`[x_i, x_{i+1})` (empty bands allowed, cost `0`) and the terminal band
`[x_{k-1}, n)` pinned at level `0`.  The optimal cost is discretely convex in
the number of links. -/
theorem band_convex {μ W : ℕ → ℝ} {n : ℕ} (hμ : ∀ x < n, 0 < μ x)
    (hW : ∀ x y, x ≤ y → y < n → W y ≤ W x) (hW0 : ∀ x < n, 0 ≤ W x)
    {k : ℕ} (hk : 1 ≤ k) {p q r : ℕ → ℕ}
    (hP : IsPath (n + 1) k p) (hQ : IsPath (n + 1) (k + 2) q)
    (hRopt : ∀ x, IsPath (n + 1) (k + 1) x →
      pathCost (linkCost μ W n) (k + 1) r ≤ pathCost (linkCost μ W n) (k + 1) x) :
    2 * pathCost (linkCost μ W n) (k + 1) r ≤
      pathCost (linkCost μ W n) k p + pathCost (linkCost μ W n) (k + 2) q :=
  convex_of_monge (c := linkCost μ W n)
    (fun a b c' d h1 h2 h3 => linkCost_monge (a := a) (b := b) (c := c') (d := d) hμ hW hW0 h1 h2 h3)
    hk hP hQ hRopt

end BandMonge
