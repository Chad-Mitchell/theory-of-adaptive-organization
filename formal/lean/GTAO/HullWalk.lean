/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of the hull-vertex increment walk in
`core/KEYSTONE_NOTE.md` §4 (no convexity of `ε` assumed), for OPEN_WORK T19.
-/
module

public import GTAO.Hull
public import Mathlib.Tactic.LinearCombination
public import Mathlib.Order.Interval.Finset.Nat

/-!
# The lower-hull increment test equals argmin (KEYSTONE_NOTE §4)

`GTAO.Hull` proves the adjacent N60 walk only when `ε` is discrete-convex.
Here `ε` is arbitrary.  The lower convex hull of `{(K, ε_K) : 0 ≤ K ≤ n}` is
described by its vertices `v 0 < v 1 < ⋯ < v m` with `v 0 = 0`, `v m = n`:

* (`below`) every point lies on or above the hull edge over it, and
* (`convex`) the edge slopes `s_i = (ε(v(i+1)) - ε(v i))/(v(i+1) - v i)`
  are nondecreasing.

KEYSTONE_NOTE's test jumps from vertex `v i` to `v (i+1)` iff
`R (ε(v i) - ε(v(i+1))) > v(i+1) - v i`.  `hull_walk_leftmost_argmin`: if the
walk stops at vertex index `i*` (every earlier jump paid, and `i* = m` or the
jump at `i*` does not pay), then `v i*` minimizes
`φ(K) = K + R(1 + ε_K)` over `{0,…,n}` and is the leftmost minimizer.
`hull_walk_stop_exists` shows the walk always stops.  The hull vertices are
taken as given data satisfying `below` and `convex`; that every finite point
set has such a vertex list is standard and is not formalized here.
-/

@[expose] public section

namespace HullWalk

/-- Lower-hull vertex data for `ε` on `{0,…,n}`. -/
structure HullVertices (n : ℕ) (ε : ℕ → ℝ) where
  m : ℕ
  v : ℕ → ℕ
  mono : StrictMono v
  v_zero : v 0 = 0
  v_last : v m = n

variable {n : ℕ} {ε : ℕ → ℝ}

/-- Slope of hull edge `i`. -/
noncomputable def HullVertices.slope (H : HullVertices n ε) (i : ℕ) : ℝ :=
  (ε (H.v (i + 1)) - ε (H.v i)) / ((H.v (i + 1) : ℝ) - H.v i)

/-- The hull hypotheses: every point is on or above its edge, and the edge
slopes are nondecreasing. -/
structure HullVertices.IsLowerHull (H : HullVertices n ε) : Prop where
  below : ∀ i < H.m, ∀ j, H.v i ≤ j → j ≤ H.v (i + 1) →
    ε (H.v i) + H.slope i * ((j : ℝ) - H.v i) ≤ ε j
  convex : ∀ i, i + 1 < H.m → H.slope i ≤ H.slope (i + 1)

/-- KEYSTONE_NOTE's jump test on hull edge `i`. -/
def HullVertices.Pays (H : HullVertices n ε) (R : ℝ) (i : ℕ) : Prop :=
  ((H.v (i + 1) : ℝ) - H.v i) < R * (ε (H.v i) - ε (H.v (i + 1)))

variable (H : HullVertices n ε)

lemma len_pos (i : ℕ) : (0 : ℝ) < (H.v (i + 1) : ℝ) - H.v i := by
  have := H.mono (Nat.lt_succ_self i)
  have : (H.v i : ℝ) < H.v (i + 1) := by exact_mod_cast this
  linarith

lemma slope_mul_len (i : ℕ) :
    H.slope i * ((H.v (i + 1) : ℝ) - H.v i) = ε (H.v (i + 1)) - ε (H.v i) := by
  unfold HullVertices.slope
  exact div_mul_cancel₀ _ (len_pos H i).ne'

lemma phi_step (R : ℝ) (i : ℕ) :
    phi R ε (H.v (i + 1)) =
      phi R ε (H.v i) + ((H.v (i + 1) : ℝ) - H.v i) * (1 + R * H.slope i) := by
  have := slope_mul_len H i
  unfold phi
  linear_combination (-R) * this

lemma pays_iff (R : ℝ) (i : ℕ) : H.Pays R i ↔ 1 + R * H.slope i < 0 := by
  unfold HullVertices.Pays
  have hL := len_pos H i
  have hx : ((H.v (i + 1) : ℝ) - H.v i) * (1 + R * H.slope i) =
      ((H.v (i + 1) : ℝ) - H.v i) + R * (ε (H.v (i + 1)) - ε (H.v i)) := by
    rw [← slope_mul_len H i]; ring
  constructor
  · intro h
    by_contra hc
    push Not at hc
    have : 0 ≤ ((H.v (i + 1) : ℝ) - H.v i) * (1 + R * H.slope i) := mul_nonneg hL.le hc
    linarith
  · intro h
    have : ((H.v (i + 1) : ℝ) - H.v i) * (1 + R * H.slope i) < 0 := mul_neg_of_pos_of_neg hL h
    linarith

/-- The affine lower bound of `φ` on hull edge `i`. -/
lemma phi_ge_line (hH : H.IsLowerHull) {R : ℝ} (hR : 0 ≤ R) {i j : ℕ} (hi : i < H.m)
    (h1 : H.v i ≤ j) (h2 : j ≤ H.v (i + 1)) :
    phi R ε (H.v i) + ((j : ℝ) - H.v i) * (1 + R * H.slope i) ≤ phi R ε j := by
  have hb := hH.below i hi j h1 h2
  unfold phi
  nlinarith [mul_le_mul_of_nonneg_left hb hR]

lemma slope_mono (hH : H.IsLowerHull) {a b : ℕ} (hab : a ≤ b) (hb : b < H.m) :
    H.slope a ≤ H.slope b := by
  induction b, hab using Nat.le_induction with
  | base => exact le_rfl
  | succ k hak ih =>
    exact (ih (by omega)).trans (hH.convex k (by omega))

/-- Every `j ∈ [0, n)` lies in a half-open hull edge `[v i, v (i+1))` with `i < m`. -/
lemma exists_edge {j : ℕ} (hj : j < n) :
    ∃ i < H.m, H.v i ≤ j ∧ j < H.v (i + 1) := by
  have hm : 0 < H.m := by
    rcases Nat.eq_zero_or_pos H.m with h | h
    · have := H.v_last; rw [h, H.v_zero] at this; omega
    · exact h
  have hex : ∃ i, j < H.v (i + 1) := ⟨H.m - 1, by rw [Nat.sub_add_cancel hm, H.v_last]; exact hj⟩
  classical
  refine ⟨Nat.find hex, ?_, ?_, Nat.find_spec hex⟩
  · have : Nat.find hex ≤ H.m - 1 :=
      Nat.find_min' hex (by rw [Nat.sub_add_cancel hm, H.v_last]; exact hj)
    omega
  · rcases Nat.eq_zero_or_pos (Nat.find hex) with h0 | hpos
    · rw [h0, H.v_zero]; exact Nat.zero_le _
    · have hlt : Nat.find hex - 1 < Nat.find hex := Nat.sub_lt hpos one_pos
      have := Nat.find_min hex hlt
      rw [Nat.sub_add_cancel hpos] at this
      omega

/-- The walk always stops: there is a first vertex index whose jump does
not pay (or the last vertex). -/
theorem hull_walk_stop_exists (R : ℝ) :
    ∃ istar ≤ H.m, (∀ i < istar, H.Pays R i) ∧ (istar = H.m ∨ ¬ H.Pays R istar) := by
  classical
  have hex : ∃ i, i = H.m ∨ ¬ H.Pays R i := ⟨H.m, Or.inl rfl⟩
  refine ⟨Nat.find hex, Nat.find_min' hex (Or.inl rfl), fun i hi => ?_, Nat.find_spec hex⟩
  have := Nat.find_min hex hi
  push Not at this
  exact this.2

/-- **Hull increment test = argmin, leftmost.**  With `R ≥ 0` and `ε`
arbitrary, if the hull walk stops at vertex index `i*`, then `v i*` is a
minimizer of `φ(K) = K + R(1+ε_K)` over `{0,…,n}`, and every `K < v i*` has
strictly larger `φ`. -/
theorem hull_walk_leftmost_argmin (hH : H.IsLowerHull) {R : ℝ} (hR : 0 ≤ R)
    {istar : ℕ} (hle : istar ≤ H.m) (hBefore : ∀ i < istar, H.Pays R i)
    (hStop : istar = H.m ∨ ¬ H.Pays R istar) :
    (∀ j ≤ n, phi R ε (H.v istar) ≤ phi R ε j) ∧
      ∀ j < H.v istar, phi R ε (H.v istar) < phi R ε j := by
  -- strict decrease along vertices before `istar`
  have hdec : ∀ i < istar, phi R ε (H.v (i + 1)) < phi R ε (H.v i) := by
    intro i hi
    rw [phi_step H R i]
    have := (pays_iff H R i).mp (hBefore i hi)
    have := mul_neg_of_pos_of_neg (len_pos H i) this
    linarith
  have hvert_lt : ∀ i < istar, phi R ε (H.v istar) < phi R ε (H.v i) := by
    intro i hi
    have key : ∀ k, i < k → k ≤ istar → phi R ε (H.v k) < phi R ε (H.v i) := by
      intro k hik
      induction k, hik using Nat.le_induction with
      | base => intro _; exact hdec i hi
      | succ k hk ih =>
        intro hk1
        exact (hdec k (by omega)).trans (ih (by omega))
    exact key istar hi le_rfl
  -- nondecrease along vertices after `istar`
  have hvert_ge : ∀ i, istar ≤ i → i ≤ H.m → phi R ε (H.v istar) ≤ phi R ε (H.v i) := by
    intro i hi
    induction i, hi using Nat.le_induction with
    | base => intro _; exact le_rfl
    | succ k hk ih =>
      intro hk1
      have hlt : istar < H.m := by omega
      have hnp : ¬ H.Pays R istar := hStop.resolve_left (by omega)
      have h0 : 0 ≤ 1 + R * H.slope istar := by
        have := (pays_iff H R istar).not.mp hnp; push Not at this; exact this
      have hs := slope_mono H hH hk (by omega : k < H.m)
      have h1 : 0 ≤ 1 + R * H.slope k := by nlinarith [mul_le_mul_of_nonneg_left hs hR]
      rw [phi_step H R k]
      have := mul_nonneg (len_pos H k).le h1
      linarith [ih (by omega)]
  have hvert : ∀ i ≤ H.m, phi R ε (H.v istar) ≤ phi R ε (H.v i) := by
    intro i hi
    rcases lt_or_ge i istar with h | h
    · exact (hvert_lt i h).le
    · exact hvert_ge i h hi
  refine ⟨fun j hj => ?_, fun j hj => ?_⟩
  · rcases hj.lt_or_eq with hj | hjeq
    · obtain ⟨i, him, h1, h2⟩ := exists_edge H hj
      have hline := phi_ge_line H hH hR him h1 h2.le
      -- the line value is a convex combination of the two endpoint values
      have hL := len_pos H i
      set t : ℝ := ((j : ℝ) - H.v i) / ((H.v (i + 1) : ℝ) - H.v i)
      have hvj : (H.v i : ℝ) ≤ j := by exact_mod_cast h1
      have ht0 : 0 ≤ t := div_nonneg (by linarith) hL.le
      have ht1 : t ≤ 1 := by
        rw [div_le_one hL]
        have : (j : ℝ) ≤ H.v (i + 1) := by exact_mod_cast h2.le
        linarith
      have hcomb : phi R ε (H.v i) + ((j : ℝ) - H.v i) * (1 + R * H.slope i) =
          (1 - t) * phi R ε (H.v i) + t * phi R ε (H.v (i + 1)) := by
        rw [phi_step H R i]
        simp only [t]
        field_simp
        ring
      have ha := hvert i him.le
      have hb := hvert (i + 1) (by omega)
      have : phi R ε (H.v istar) ≤ (1 - t) * phi R ε (H.v i) + t * phi R ε (H.v (i + 1)) := by
        nlinarith
      linarith
    · have := hvert H.m le_rfl
      rw [H.v_last] at this
      exact hjeq ▸ this
  · have hjn : j < n := by
      have : H.v istar ≤ H.v H.m := H.mono.monotone hle
      rw [H.v_last] at this; omega
    obtain ⟨i, him, h1, h2⟩ := exists_edge H hjn
    have hii : i < istar := by
      by_contra hc; push Not at hc
      have := H.mono.monotone hc; omega
    have hline := phi_ge_line H hH hR him h1 h2.le
    have hneg := (pays_iff H R i).mp (hBefore i hii)
    -- write the line from the right endpoint
    have hstep := phi_step H R i
    have hjlt : (j : ℝ) < H.v (i + 1) := by exact_mod_cast h2
    have hright : phi R ε (H.v (i + 1)) <
        phi R ε (H.v i) + ((j : ℝ) - H.v i) * (1 + R * H.slope i) := by
      rw [hstep]
      have : 0 < ((H.v (i + 1) : ℝ) - j) * (-(1 + R * H.slope i)) :=
        mul_pos (by linarith) (by linarith)
      nlinarith
    have hvi1 : phi R ε (H.v istar) ≤ phi R ε (H.v (i + 1)) := by
      rcases (Nat.succ_le_of_lt hii).lt_or_eq with h | h
      · exact (hvert_lt (i + 1) h).le
      · have h' : i + 1 = istar := h
        rw [h']
    linarith

/-! ## Every `ε` has lower-hull vertex data (greedy minimum-slope construction) -/

section Exists

variable (n : ℕ) (ε : ℕ → ℝ)

/-- Slope of the chord from `a` to `b`. -/
noncomputable def chord (a b : ℕ) : ℝ := (ε b - ε a) / ((b : ℝ) - a)

lemma exists_next {a : ℕ} (ha : a < n) :
    ∃ b ∈ Finset.Ioc a n, ∀ c ∈ Finset.Ioc a n, chord ε a b ≤ chord ε a c :=
  Finset.exists_min_image _ _ ⟨n, Finset.mem_Ioc.mpr ⟨ha, le_rfl⟩⟩

/-- The next hull vertex: a minimum-slope chord endpoint in `(a, n]`. -/
noncomputable def next (a : ℕ) : ℕ :=
  if h : a < n then Classical.choose (exists_next n ε h) else a + 1

lemma next_spec {a : ℕ} (ha : a < n) :
    a < next n ε a ∧ next n ε a ≤ n ∧
      ∀ c, a < c → c ≤ n → chord ε a (next n ε a) ≤ chord ε a c := by
  have hnext : next n ε a = Classical.choose (exists_next n ε ha) := by
    unfold next; simp [ha]
  rw [hnext]
  obtain ⟨hmem, hmin⟩ := Classical.choose_spec (exists_next n ε ha)
  rw [Finset.mem_Ioc] at hmem
  exact ⟨hmem.1, hmem.2, fun c h1 h2 => hmin c (Finset.mem_Ioc.mpr ⟨h1, h2⟩)⟩

/-- The greedy vertex sequence (continued by `+1` past `n`). -/
noncomputable def gv : ℕ → ℕ
  | 0 => 0
  | i + 1 => if gv i < n then next n ε (gv i) else gv i + 1

lemma gv_lt_succ (i : ℕ) : gv n ε i < gv n ε (i + 1) := by
  show gv n ε i < (if gv n ε i < n then next n ε (gv n ε i) else gv n ε i + 1)
  split_ifs with h
  · exact (next_spec n ε h).1
  · exact Nat.lt_succ_self _

lemma gv_strictMono : StrictMono (gv n ε) := strictMono_nat_of_lt_succ (gv_lt_succ n ε)

lemma gv_succ_of_lt {i : ℕ} (h : gv n ε i < n) : gv n ε (i + 1) = next n ε (gv n ε i) := by
  show (if gv n ε i < n then next n ε (gv n ε i) else gv n ε i + 1) = _
  simp [h]

lemma exists_gv_ge : ∃ i, n ≤ gv n ε i :=
  ⟨n, (gv_strictMono n ε).id_le n⟩

/-- The number of hull edges. -/
noncomputable def gm : ℕ := by
  classical exact Nat.find (exists_gv_ge n ε)

lemma gv_lt_of_lt_gm {i : ℕ} (hi : i < gm n ε) : gv n ε i < n := by
  classical
  unfold gm at hi
  have := Nat.find_min (exists_gv_ge n ε) hi
  omega

lemma gv_gm : gv n ε (gm n ε) = n := by
  classical
  have hspec : n ≤ gv n ε (gm n ε) := by unfold gm; exact Nat.find_spec (exists_gv_ge n ε)
  rcases Nat.eq_zero_or_pos (gm n ε) with h0 | hpos
  · rw [h0] at hspec ⊢
    show (0 : ℕ) = n
    have : gv n ε 0 = 0 := rfl
    omega
  · have hprev := gv_lt_of_lt_gm n ε (Nat.sub_lt hpos one_pos)
    have hsucc := gv_succ_of_lt n ε hprev
    have e : gm n ε - 1 + 1 = gm n ε := by omega
    rw [e] at hsucc
    have hle := (next_spec n ε hprev).2.1
    omega

/-- Greedy hull vertices. -/
noncomputable def greedy : HullVertices n ε where
  m := gm n ε
  v := gv n ε
  mono := gv_strictMono n ε
  v_zero := rfl
  v_last := gv_gm n ε

lemma greedy_slope (i : ℕ) : (greedy n ε).slope i = chord ε (gv n ε i) (gv n ε (i + 1)) := rfl

/-- Chord additivity: `(c-a) chord(a,c) = (b-a) chord(a,b) + (c-b) chord(b,c)`. -/
lemma chord_add {a b c : ℕ} (hab : a < b) (hbc : b < c) :
    ((c : ℝ) - a) * chord ε a c = ((b : ℝ) - a) * chord ε a b + ((c : ℝ) - b) * chord ε b c := by
  have h1 : (0 : ℝ) < (b : ℝ) - a := by have : (a : ℝ) < b := (by exact_mod_cast hab); linarith
  have h2 : (0 : ℝ) < (c : ℝ) - b := by have : (b : ℝ) < c := (by exact_mod_cast hbc); linarith
  have h3 : (0 : ℝ) < (c : ℝ) - a := by linarith
  unfold chord
  rw [mul_div_cancel₀ _ h3.ne', mul_div_cancel₀ _ h1.ne', mul_div_cancel₀ _ h2.ne']
  ring

theorem greedy_isLowerHull : (greedy n ε).IsLowerHull where
  below := by
    intro i hi j h1 h2
    change gv n ε i ≤ j at h1
    change j ≤ gv n ε (i + 1) at h2
    rw [greedy_slope]
    change ε (gv n ε i) + chord ε (gv n ε i) (gv n ε (i + 1)) * ((j : ℝ) - gv n ε i) ≤ ε j
    have hlt := gv_lt_of_lt_gm n ε hi
    rcases h1.lt_or_eq with h1 | h1
    · have hsp := next_spec n ε hlt
      rw [gv_succ_of_lt n ε hlt] at h2 ⊢
      have hmin := hsp.2.2 j h1 (h2.trans hsp.2.1)
      have hpos : (0 : ℝ) < (j : ℝ) - gv n ε i := by
        have : (gv n ε i : ℝ) < j := by exact_mod_cast h1
        linarith
      have : chord ε (gv n ε i) j * ((j : ℝ) - gv n ε i) = ε j - ε (gv n ε i) := by
        unfold chord; exact div_mul_cancel₀ _ hpos.ne'
      nlinarith [mul_le_mul_of_nonneg_right hmin hpos.le]
    · rw [← h1]; simp
  convex := by
    intro i hi
    rw [greedy_slope, greedy_slope]
    have ha := gv_lt_of_lt_gm n ε (show i < gm n ε by change i + 1 < gm n ε at hi; omega)
    have hb := gv_lt_of_lt_gm n ε (show i + 1 < gm n ε from hi)
    set a := gv n ε i
    have hb' : gv n ε (i + 1) = next n ε a := gv_succ_of_lt n ε ha
    have hc' : gv n ε (i + 1 + 1) = next n ε (gv n ε (i + 1)) := gv_succ_of_lt n ε hb
    set b := gv n ε (i + 1)
    set c := gv n ε (i + 1 + 1)
    have hab : a < b := gv_lt_succ n ε i
    have hbc : b < c := gv_lt_succ n ε (i + 1)
    have hcn : c ≤ n := by rw [hc']; exact (next_spec n ε hb).2.1
    have hmin : chord ε a b ≤ chord ε a c := by
      rw [hb']; exact (next_spec n ε ha).2.2 c (hab.trans hbc) hcn
    have hadd := chord_add ε hab hbc
    have h1 : (0 : ℝ) < (b : ℝ) - a := by have : (a : ℝ) < b := (by exact_mod_cast hab); linarith
    have h2 : (0 : ℝ) < (c : ℝ) - b := by have : (b : ℝ) < c := (by exact_mod_cast hbc); linarith
    have : ((c : ℝ) - b) * chord ε a b ≤ ((c : ℝ) - b) * chord ε b c := by
      nlinarith [mul_le_mul_of_nonneg_left hmin (by linarith : (0 : ℝ) ≤ (c : ℝ) - a)]
    exact le_of_mul_le_mul_left this h2

end Exists

/-- **KEYSTONE_NOTE §4, unconditional in `ε`.**  For every `ε : ℕ → ℝ` on
`{0,…,n}` and every `R ≥ 0`, there is lower-hull vertex data for `ε`, the
hull increment walk stops, and the vertex where it stops is the leftmost
minimizer of `φ(K) = K + R(1 + ε_K)`.  No convexity of `ε` is assumed. -/
theorem hull_increment_test_eq_argmin (n : ℕ) (ε : ℕ → ℝ) {R : ℝ} (hR : 0 ≤ R) :
    ∃ H : HullVertices n ε, H.IsLowerHull ∧
      ∃ istar ≤ H.m, (∀ i < istar, H.Pays R i) ∧ (istar = H.m ∨ ¬ H.Pays R istar) ∧
        (∀ j ≤ n, phi R ε (H.v istar) ≤ phi R ε j) ∧
        ∀ j < H.v istar, phi R ε (H.v istar) < phi R ε j := by
  refine ⟨greedy n ε, greedy_isLowerHull n ε, ?_⟩
  obtain ⟨istar, hle, hB, hS⟩ := hull_walk_stop_exists (greedy n ε) R
  exact ⟨istar, hle, hB, hS, hull_walk_leftmost_argmin _ (greedy_isLowerHull n ε) hR hle hB hS⟩

end HullWalk
