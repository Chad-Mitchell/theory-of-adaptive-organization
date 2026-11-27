/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, stepback C12C: a finite Theorem O (memory onset under a stake and an accuracy cap) over ℚ,
KNOWN in substance (a one-variable Everett / KKT instance; no novelty claimed). Lean round 5 add-on
of the side session; written in a private Lake project (same Lean and Mathlib pins) and moved here
with only this header and the module lines changed.
-/
module

public import Mathlib

@[expose] public section

/-!
# Finite Theorem O: memory onset under a stake and an accuracy cap (Lean round 5 add-on)

KNOWN in substance (a one-variable Everett / KKT instance for a discrete convex error curve); no
novelty is claimed. Setting of `rnd/stepback/C12C_LEAN_SPEC.md`: designs `k = 0..n`, error
`f k` nonincreasing and discrete convex, cost `g w k = w f k + κ k` with `κ > 0`, `w ≥ 0`, cap
`f k ≤ D`.
-/

namespace GTAORnd.SelfRef.LR3.OnsetO

/-- the forward difference -/
def Δ (h : ℕ → ℚ) (k : ℕ) : ℚ := h (k + 1) - h k

/-- the cost of design `k` at stake `w` -/
def g (f : ℕ → ℚ) (κ w : ℚ) (k : ℕ) : ℚ := w * f k + κ * k

/-- `k` minimizes `h` on `0..n` -/
def IsMin (h : ℕ → ℚ) (n k : ℕ) : Prop := k ≤ n ∧ ∀ j ≤ n, h k ≤ h j

/-- steps nondecreasing on `0..n` -/
def StepMono (h : ℕ → ℚ) (n : ℕ) : Prop := ∀ k, k + 1 < n → Δ h k ≤ Δ h (k + 1)

lemma stepMono_le {h : ℕ → ℚ} {n : ℕ} (hm : StepMono h n) {a b : ℕ} (hab : a ≤ b) (hb : b < n) :
    Δ h a ≤ Δ h b := by
  induction b, hab using Nat.le_induction with
  | base => exact le_rfl
  | succ b hab ih => exact (ih (by omega)).trans (hm b hb)

/-- nonnegative steps from `a` on make `h` nondecreasing on `[a, n]` -/
lemma mono_of_steps {h : ℕ → ℚ} {n a : ℕ} (hs : ∀ k, a ≤ k → k < n → 0 ≤ Δ h k) :
    ∀ b c, a ≤ b → b ≤ c → c ≤ n → h b ≤ h c := by
  intro b c hab hbc hcn
  induction c, hbc using Nat.le_induction with
  | base => exact le_rfl
  | succ c hbc ih =>
    have := hs c (hab.trans hbc) (by omega)
    unfold Δ at this
    linarith [ih (by omega)]

/-- nonpositive steps before `a` make `h` nonincreasing on `[0, a]` -/
lemma anti_of_steps {h : ℕ → ℚ} {a : ℕ} (hs : ∀ k, k < a → Δ h k ≤ 0) :
    ∀ b c, b ≤ c → c ≤ a → h c ≤ h b := by
  intro b c hbc hca
  induction c, hbc using Nat.le_induction with
  | base => exact le_rfl
  | succ c hbc ih =>
    have := hs c (by omega)
    unfold Δ at this
    linarith [ih (by omega)]

/-- **Local = global for discrete convex sequences** (PROVED-IN-MODEL): with nondecreasing steps on
`0..n`, `k ≤ n` minimizes `h` on `0..n` iff its left step is `≤ 0` and its right step is `≥ 0`. -/
theorem isMin_iff_local {h : ℕ → ℚ} {n : ℕ} (hm : StepMono h n) {k : ℕ} (hk : k ≤ n) :
    IsMin h n k ↔ (k = 0 ∨ Δ h (k - 1) ≤ 0) ∧ (k = n ∨ 0 ≤ Δ h k) := by
  constructor
  · rintro ⟨-, hmin⟩
    refine ⟨?_, ?_⟩
    · rcases Nat.eq_zero_or_pos k with h0 | h0
      · exact Or.inl h0
      · right
        have := hmin (k - 1) (by omega)
        unfold Δ; rw [Nat.sub_add_cancel h0]; linarith
    · rcases eq_or_lt_of_le hk with h0 | h0
      · exact Or.inl h0
      · right
        have := hmin (k + 1) h0
        unfold Δ; linarith
  · rintro ⟨hl, hr⟩
    refine ⟨hk, fun j hj => ?_⟩
    rcases le_total k j with hkj | hjk
    · refine mono_of_steps (a := k) (fun i hki hin => ?_) k j le_rfl hkj hj
      rcases hr with e | e
      · omega
      · exact e.trans (stepMono_le hm hki hin)
    · refine anti_of_steps (a := k) (fun i hik => ?_) j k hjk le_rfl
      rcases hl with e | e
      · omega
      · exact (stepMono_le hm (by omega) (by omega)).trans e

/-! ### The setting -/

structure Setting where
  n : ℕ
  f : ℕ → ℚ
  κ : ℚ
  D : ℚ
  hκ : 0 < κ
  hmono : ∀ k, k < n → Δ f k ≤ 0
  hconv : StepMono f n
  hfeas : f n < D

namespace Setting

variable (S : Setting)

lemma f_anti {a b : ℕ} (hab : a ≤ b) (hb : b ≤ S.n) : S.f b ≤ S.f a :=
  anti_of_steps (a := S.n) (fun k hk => S.hmono k hk) a b hab hb

lemma g_step (w : ℚ) (k : ℕ) : Δ (g S.f S.κ w) k = w * Δ S.f k + S.κ := by
  unfold Δ g; push_cast; ring

lemma g_stepMono {w : ℚ} (hw : 0 ≤ w) : StepMono (g S.f S.κ w) S.n := fun k hk => by
  rw [g_step, g_step]
  nlinarith [S.hconv k hk]

/-- `xD` is the least design meeting the cap -/
def IsXD (xD : ℕ) : Prop := xD ≤ S.n ∧ S.f xD ≤ S.D ∧ ∀ k, S.f k ≤ S.D → xD ≤ k

/-- `xw` is the least minimizer of `g w` on `0..n` -/
def IsXW (w : ℚ) (xw : ℕ) : Prop := IsMin (g S.f S.κ w) S.n xw ∧ ∀ k, IsMin (g S.f S.κ w) S.n k → xw ≤ k

lemma exists_xD : ∃ xD, S.IsXD xD := by
  classical
  have hex : ∃ k, S.f k ≤ S.D := ⟨S.n, S.hfeas.le⟩
  refine ⟨Nat.find hex, ?_, Nat.find_spec hex, fun k hk => Nat.find_min' hex hk⟩
  exact Nat.find_min' hex S.hfeas.le

lemma exists_xw (w : ℚ) : ∃ xw, S.IsXW w xw := by
  classical
  obtain ⟨k0, hk0, hmin⟩ := (Finset.range (S.n + 1)).exists_min_image (g S.f S.κ w)
    ⟨0, by simp⟩
  have hex : ∃ k, IsMin (g S.f S.κ w) S.n k :=
    ⟨k0, by simpa [Nat.lt_succ_iff] using hk0, fun j hj => hmin j (by simpa [Nat.lt_succ_iff] using hj)⟩
  exact ⟨Nat.find hex, Nat.find_spec hex, fun k hk => Nat.find_min' hex hk⟩

/-- right of the least minimizer the steps of `g w` are nonnegative -/
lemma steps_after_min {w : ℚ} (hw : 0 ≤ w) {xw : ℕ} (hx : IsMin (g S.f S.κ w) S.n xw) :
    ∀ k, xw ≤ k → k < S.n → 0 ≤ Δ (g S.f S.κ w) k := by
  intro k hk hkn
  have := ((isMin_iff_local (S.g_stepMono hw) hx.1).1 hx).2
  rcases this with e | e
  · omega
  · exact e.trans (stepMono_le (S.g_stepMono hw) hk hkn)

/-- **(i) Projection** (PROVED-IN-MODEL; KNOWN in substance): the least optimum under the cap is
`max xw xD`. -/
theorem projection {w : ℚ} (hw : 0 ≤ w) {xw xD : ℕ} (hxw : S.IsXW w xw) (hxD : S.IsXD xD) :
    max xw xD ≤ S.n ∧ S.f (max xw xD) ≤ S.D ∧
      (∀ j ≤ S.n, S.f j ≤ S.D → g S.f S.κ w (max xw xD) ≤ g S.f S.κ w j) ∧
      ∀ k ≤ S.n, S.f k ≤ S.D → (∀ j ≤ S.n, S.f j ≤ S.D → g S.f S.κ w k ≤ g S.f S.κ w j) →
        max xw xD ≤ k := by
  obtain ⟨⟨hxwn, hmin⟩, hleast⟩ := hxw
  obtain ⟨hxDn, hfD, hDleast⟩ := hxD
  have hmn : max xw xD ≤ S.n := max_le hxwn hxDn
  have hcap : S.f (max xw xD) ≤ S.D := (S.f_anti (le_max_right _ _) hmn).trans hfD
  refine ⟨hmn, hcap, fun j hj hfj => ?_, fun k hk hfk hopt => ?_⟩
  · rcases le_total xD xw with h | h
    · rw [max_eq_left h]; exact hmin j hj
    · rw [max_eq_right h]
      exact mono_of_steps (S.steps_after_min hw ⟨hxwn, hmin⟩) xD j h (hDleast j hfj) hj
  · refine max_le ?_ (hDleast k hfk)
    rcases le_total xD xw with h | h
    · have hfxw : S.f xw ≤ S.D := (S.f_anti h hxwn).trans hfD
      have := hopt xw hxwn hfxw
      exact hleast k ⟨hk, fun j hj => this.trans (hmin j hj)⟩
    · exact h.trans (hDleast k hfk)

/-- **(ii) Onset is a union** (PROVED-IN-MODEL; KNOWN in substance), `n ≥ 1`. -/
theorem onset_union (hn : 1 ≤ S.n) {w : ℚ} (hw : 0 ≤ w) {xw xD : ℕ} (hxw : S.IsXW w xw)
    (hxD : S.IsXD xD) : 0 < max xw xD ↔ S.κ < w * (-Δ S.f 0) ∨ S.D < S.f 0 := by
  have hxw0 : 0 < xw ↔ S.κ < w * (-Δ S.f 0) := by
    have hloc := isMin_iff_local (S.g_stepMono hw) (Nat.zero_le S.n)
    constructor
    · intro hpos
      by_contra hc
      have h0 : IsMin (g S.f S.κ w) S.n 0 := hloc.2 ⟨Or.inl rfl, Or.inr (by rw [g_step]; linarith)⟩
      have := hxw.2 0 h0; omega
    · intro hlt
      by_contra hc
      have hz : xw = 0 := by omega
      have h0 := hxw.1; rw [hz] at h0
      rcases (hloc.1 h0).2 with e | e
      · omega
      · rw [g_step] at e; linarith
  have hxD0 : 0 < xD ↔ S.D < S.f 0 := by
    constructor
    · intro hpos; by_contra hc; push Not at hc; have := hxD.2.2 0 hc; omega
    · intro hlt; by_contra hc
      have hz : xD = 0 := by omega
      have := hxD.2.1; rw [hz] at this; linarith
  rw [lt_max_iff, hxw0, hxD0]

/-- the drop just before the cap is met is positive -/
lemma drop_pos {xD : ℕ} (hxD : S.IsXD xD) (h1 : 1 ≤ xD) : 0 < -Δ S.f (xD - 1) := by
  have hlt : S.D < S.f (xD - 1) := by
    by_contra hc; push Not at hc; have := hxD.2.2 _ hc; omega
  have := hxD.2.1
  unfold Δ; rw [Nat.sub_add_cancel h1]; linarith

/-- the least supporting stake -/
def wstar (xD : ℕ) : ℚ := S.κ / (-Δ S.f (xD - 1))

/-- **(iii a) Supporting stakes** (PROVED-IN-MODEL; KNOWN in substance): for `xD ≥ 1` and `v ≥ 0`,
`xD` minimizes `g v` iff `wstar ≤ v` and (`xD = n` or `v · (−Δ xD) ≤ κ`). -/
theorem supporting_iff {xD : ℕ} (hxD : S.IsXD xD) (h1 : 1 ≤ xD) {v : ℚ} (hv : 0 ≤ v) :
    IsMin (g S.f S.κ v) S.n xD ↔ S.wstar xD ≤ v ∧ (xD = S.n ∨ v * (-Δ S.f xD) ≤ S.κ) := by
  have hd := S.drop_pos hxD h1
  rw [isMin_iff_local (S.g_stepMono hv) hxD.1, g_step, g_step, wstar, div_le_iff₀ hd]
  constructor
  · rintro ⟨hl, hr⟩
    refine ⟨?_, ?_⟩
    · rcases hl with e | e
      · omega
      · linarith
    · rcases hr with e | e
      · exact Or.inl e
      · right; linarith
  · rintro ⟨hl, hr⟩
    refine ⟨Or.inr (by linarith), ?_⟩
    rcases hr with e | e
    · exact Or.inl e
    · right; linarith

/-- **(iii b) The tie at `wstar`** (PROVED-IN-MODEL): at `v = wstar`, `xD − 1` and `xD` cost the
same, so `xD` is a minimizer there (when supported) but not the least one. -/
theorem tie_at_wstar {xD : ℕ} (hxD : S.IsXD xD) (h1 : 1 ≤ xD) :
    g S.f S.κ (S.wstar xD) (xD - 1) = g S.f S.κ (S.wstar xD) xD := by
  have hd := S.drop_pos hxD h1
  have hstep := S.g_step (S.wstar xD) (xD - 1)
  have e : xD - 1 + 1 = xD := Nat.sub_add_cancel h1
  have h2 : S.wstar xD * (-Δ S.f (xD - 1)) = S.κ := by
    unfold wstar; rw [div_mul_cancel₀ _ (ne_of_gt hd)]
  unfold Δ at hstep h2; rw [e] at hstep h2; linarith

/-- **(iii c, d) The optimum under the cap is unconstrained at the raised stake** (PROVED-IN-MODEL;
KNOWN in substance: the KKT multiplier is `μ = max 0 (wstar − w)`): for `xD ≥ 1`, `max xw xD`
minimizes `g (max w wstar)` on `0..n`. -/
theorem kkt {w : ℚ} (hw : 0 ≤ w) {xw xD : ℕ} (hxw : S.IsXW w xw) (hxD : S.IsXD xD) (h1 : 1 ≤ xD) :
    IsMin (g S.f S.κ (max w (S.wstar xD))) S.n (max xw xD) := by
  have hd := S.drop_pos hxD h1
  have hws : 0 ≤ S.wstar xD := div_nonneg S.hκ.le hd.le
  have hv : 0 ≤ max w (S.wstar xD) := le_max_of_le_left hw
  rcases le_total xD xw with h | h
  · -- the cap is slack: `wstar ≤ w`
    rw [max_eq_left h]
    have hxw1 : 1 ≤ xw := h1.trans h
    have hl := ((isMin_iff_local (S.g_stepMono hw) hxw.1.1).1 hxw.1).1
    have hl' : Δ (g S.f S.κ w) (xw - 1) ≤ 0 := by rcases hl with e | e; omega; exact e
    have hmono := stepMono_le (S.g_stepMono hw) (Nat.sub_le_sub_right h 1) (by have := hxw.1.1; omega)
    have hle : S.wstar xD ≤ w := by
      simp only [g_step] at hmono hl'
      unfold wstar; rw [div_le_iff₀ hd]; linarith
    rw [max_eq_left hle]; exact hxw.1
  · rw [max_eq_right h]
    rw [S.supporting_iff hxD h1 hv]
    refine ⟨le_max_right _ _, ?_⟩
    rcases eq_or_lt_of_le hxD.1 with e | e
    · exact Or.inl e
    · right
      rcases le_total w (S.wstar xD) with hw' | hw'
      · rw [max_eq_right hw']
        have hc := stepMono_le S.hconv (Nat.sub_le xD 1) e
        have : S.wstar xD * (-Δ S.f (xD - 1)) = S.κ := by
          unfold wstar; rw [div_mul_cancel₀ _ (ne_of_gt hd)]
        nlinarith
      · rw [max_eq_left hw']
        have := S.steps_after_min hw hxw.1 xD h e
        rw [g_step] at this; linarith

/-- **(iv) Monotone in the cap, and the corner** (PROVED-IN-MODEL): a looser cap meets earlier, and
needs no larger supporting stake. -/
theorem wstar_anti {S' : Setting} (hf : S'.f = S.f) (hκ : S'.κ = S.κ)
    (hDD : S.D ≤ S'.D) {xD xD' : ℕ} (hxD : S.IsXD xD) (hxD' : S'.IsXD xD') (h1 : 1 ≤ xD)
    (h1' : 1 ≤ xD') : xD' ≤ xD ∧ S'.wstar xD' ≤ S.wstar xD := by
  have hle : xD' ≤ xD := hxD'.2.2 xD (by rw [hf]; exact hxD.2.1.trans hDD)
  refine ⟨hle, ?_⟩
  have hd := S.drop_pos hxD h1
  have hd' := S'.drop_pos hxD' h1'
  unfold wstar
  rw [hκ, hf] at *
  rw [hf] at hd'
  have hc : Δ S.f (xD' - 1) ≤ Δ S.f (xD - 1) :=
    stepMono_le S.hconv (Nat.sub_le_sub_right hle 1) (by have := hxD.1; omega)
  exact div_le_div_of_nonneg_left S.hκ.le hd (by linarith)

/-- at `xD = 1` the least supporting stake is the onset stake `κ / (−Δ 0)` -/
theorem wstar_one : S.wstar 1 = S.κ / (-Δ S.f 0) := rfl

/-- **(v) Zero-stake floor** (PROVED-IN-MODEL): at `w = 0` the least optimum under the cap is `0`
iff `f 0 ≤ D`. -/
theorem zero_stake {xw xD : ℕ} (hxw : S.IsXW 0 xw) (hxD : S.IsXD xD) :
    max xw xD = 0 ↔ S.f 0 ≤ S.D := by
  have hxw0 : xw = 0 := by
    have h0 : IsMin (g S.f S.κ 0) S.n 0 := ⟨Nat.zero_le _, fun j _ => by
      unfold g; simp; exact mul_nonneg S.hκ.le (Nat.cast_nonneg j)⟩
    have := hxw.2 0 h0; omega
  rw [hxw0, Nat.max_eq_right (Nat.zero_le _)]
  constructor
  · intro h; have := hxD.2.1; rw [h] at this; exact this
  · intro h; have := hxD.2.2 0 h; omega

end Setting

/-! ### The spec's instance: `f = [4, 2, 1, 1/2]`, `κ = 1`, `D = 3/2` -/

/-- the instance's error curve (constant `1/2` past `n = 3`) -/
def fEx : ℕ → ℚ := fun k => if k = 0 then 4 else if k = 1 then 2 else if k = 2 then 1 else 1 / 2

def SEx : Setting where
  n := 3
  f := fEx
  κ := 1
  D := 3 / 2
  hκ := by norm_num
  hmono := by intro k (hk : k < 3); interval_cases k <;> simp [Δ, fEx] <;> norm_num
  hconv := by intro k (hk : k + 1 < 3); have : k < 2 := by omega
              interval_cases k <;> simp [Δ, fEx] <;> norm_num
  hfeas := by simp [fEx]; norm_num

/-- the instance: `xD = 2`, `wstar = 1`, supporting stakes `[1, 2]` -/
theorem example_values : SEx.IsXD 2 ∧ SEx.wstar 2 = 1 ∧
    ∀ v : ℚ, 0 ≤ v → (IsMin (g SEx.f SEx.κ v) SEx.n 2 ↔ 1 ≤ v ∧ v ≤ 2) := by
  have hxD : SEx.IsXD 2 := ⟨by simp [SEx], by simp [SEx, fEx]; norm_num, fun k hk => by
    by_contra hc; push Not at hc
    interval_cases k <;> simp [SEx, fEx] at hk <;> norm_num at hk⟩
  have hw : SEx.wstar 2 = 1 := by simp [Setting.wstar, SEx, Δ, fEx]; norm_num
  refine ⟨hxD, hw, fun v hv => ?_⟩
  rw [SEx.supporting_iff hxD (by norm_num) hv, hw]
  have : Δ SEx.f 2 = -1 / 2 := by simp [SEx, Δ, fEx]; norm_num
  rw [this]
  simp only [SEx]
  constructor
  · rintro ⟨h1, h2⟩; refine ⟨h1, ?_⟩; rcases h2 with e | e; · norm_num at e
    · linarith
  · rintro ⟨h1, h2⟩; exact ⟨h1, Or.inr (by linarith)⟩

end GTAORnd.SelfRef.LR3.OnsetO
