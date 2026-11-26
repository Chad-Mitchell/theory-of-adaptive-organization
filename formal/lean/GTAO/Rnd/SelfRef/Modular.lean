/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: round 10 note (`theory/RECORD_COST_ROUND10_2026-11-25.md`) §8, the lattice route: the
finite-height step that gives the orthomodularity Piron's theorem needs. Lean round 3 of the side session;
written in a private Lake project (library `GTAORnd`, same Lean and Mathlib pins) and moved here with only
this header, the module lines and the namespace changed.
-/
module

public import Mathlib

@[expose] public section

/-!
# Finite-height lemma for the lattice route (round 10 §8; hostile review (d))

In a finite lattice, upper plus lower semimodularity gives modularity (Dilworth/Birkhoff); an
orthocomplementation turns upper semimodularity into lower semimodularity; and a modular
orthocomplemented lattice is orthomodular. An atomistic lattice with finitely many atoms is finite.
-/

namespace GTAORnd.SelfRef.LR3.Modular

open Order

variable {α : Type*} [Lattice α] [Finite α]

theorem height_lt_top' (a : α) : height a < ⊤ := by
  have _ := Fintype.ofFinite α
  have : height a ≤ (Fintype.card α : ℕ∞) := by
    apply height_le
    intro p _
    have := Fintype.card_le_of_injective _ p.strictMono.injective
    simp at this
    exact_mod_cast (by omega : p.length ≤ Fintype.card α)
  exact lt_of_le_of_lt this (ENat.natCast_lt_top _)

/-- the rank `r a = height a` as a natural number -/
noncomputable def r (a : α) : ℕ := (height a).toNat

theorem r_coe (a : α) : (r a : ℕ∞) = height a := ENat.natCast_toNat (height_lt_top' a).ne

theorem r_lt {a b : α} (h : a < b) : r a < r b := by
  have := height_add_one_le h
  rw [← r_coe, ← r_coe] at this
  exact_mod_cast (by exact_mod_cast this : (r a : ℕ∞) + 1 ≤ r b)

theorem eq_of_le_of_r_eq {a b : α} (h : a ≤ b) (hr : r a = r b) : a = b := by
  rcases h.lt_or_eq with h | h
  · exact absurd hr (r_lt h).ne
  · exact h

/-- **Jordan–Dedekind** (PROVED-IN-MODEL): in a finite lattice that is upper and lower
semimodular, a cover raises the rank by exactly one. -/
theorem r_covBy [IsLowerModularLattice α] {a b : α} (hab : a ⋖ b) : r b = r a + 1 := by
  suffices H : ∀ n : ℕ, ∀ a b : α, r b = n → a ⋖ b → r b = r a + 1 from H _ a b rfl hab
  intro n
  induction n using Nat.strong_induction_on with
  | _ n IH =>
  intro a b hn hab
  have hpos : r b ≠ 0 := by have := r_lt hab.lt; omega
  obtain ⟨m, hm⟩ : ∃ m, r b = m + 1 := ⟨r b - 1, by omega⟩
  have hh : height b = (m : ℕ∞) + 1 := by rw [← r_coe, hm]; push_cast; rfl
  obtain ⟨-, ⟨c, hcb, hc⟩, hall⟩ := height_eq_coe_add_one_iff.mp hh
  have hcr : r c = m := by
    have := r_coe c; rw [hc] at this; exact_mod_cast this
  have hle : ∀ y < b, r y ≤ m := by
    intro y hy; have := hall y hy; rw [← r_coe] at this; exact_mod_cast this
  have hcov : c ⋖ b := by
    refine ⟨hcb, fun d hcd hdb => ?_⟩
    have := r_lt hcd; have := hle d hdb; omega
  by_cases hac : a = c
  · subst hac; omega
  have hsup : a ⊔ c = b := by
    have h1 : a ≤ a ⊔ c := le_sup_left
    have h2 : a ⊔ c ≤ b := sup_le hab.le hcov.le
    rcases h1.lt_or_eq with h1 | h1
    · exact (hab.eq_or_eq h1.le h2).resolve_left h1.ne'
    · exfalso
      have hca : c ≤ a := h1 ▸ le_sup_right
      rcases hca.lt_or_eq with h | h
      · exact hcov.2 h hab.lt
      · exact hac h.symm
  have h1 : a ⊓ c ⋖ c := IsLowerModularLattice.inf_covBy_of_covBy_sup (by rw [hsup]; exact hab)
  have h2 : c ⊓ a ⋖ a :=
    IsLowerModularLattice.inf_covBy_of_covBy_sup (by rw [sup_comm, hsup]; exact hcov)
  rw [inf_comm] at h2
  have e1 := IH m (by omega) _ _ hcr h1
  have e2 := IH (r a) (by have := r_lt hab.lt; omega) _ _ rfl h2
  omega

/-- generic step: if `f` raises rank by at most one along covers, then along `m ≤ a` it raises
rank by at most `r a - r m`. -/
theorem r_step_le [IsLowerModularLattice α] (f : α → α)
    (hf : ∀ c c' : α, c ⋖ c' → r (f c') ≤ r (f c) + 1) :
    ∀ m a : α, m ≤ a → r (f a) + r m ≤ r (f m) + r a := by
  suffices H : ∀ k : ℕ, ∀ m a : α, m ≤ a → r a - r m = k → r (f a) + r m ≤ r (f m) + r a from
    fun m a h => H _ m a h rfl
  intro k
  induction k with
  | zero =>
    intro m a hma hk
    have : r a ≤ r m := by omega
    have hr : r m = r a := le_antisymm (by
      rcases hma.lt_or_eq with h | h
      · exact (r_lt h).le
      · rw [h]) this
    rw [eq_of_le_of_r_eq hma hr]
  | succ k IH =>
    intro m a hma hk
    have hlt : m < a := by
      rcases hma.lt_or_eq with h | h
      · exact h
      · subst h; omega
    obtain ⟨m', hmm', hm'a⟩ := exists_covBy_le_of_lt hlt
    have e := r_covBy hmm'
    have := IH m' a hm'a (by omega)
    have := hf m m' hmm'
    omega

/-- **Dilworth/Birkhoff** (PROVED-IN-MODEL): a finite lattice that is upper and lower semimodular
is modular. -/
theorem modular_of_semimodular [IsUpperModularLattice α] [IsLowerModularLattice α] :
    IsModularLattice α := by
  -- join step (upper semimodularity)
  have hU : ∀ p : α, ∀ c c' : α, c ⋖ c' → r (p ⊔ c') ≤ r (p ⊔ c) + 1 := by
    intro p c c' hcc
    set q := p ⊔ c
    have hq : p ⊔ c' = q ⊔ c' := by
      simp only [q]; rw [sup_assoc, sup_eq_right.mpr hcc.le]
    rw [hq]
    by_cases h : c' ≤ q
    · rw [sup_eq_left.mpr h]; omega
    · have hmeet : c' ⊓ q = c := by
        have h1 : c ≤ c' ⊓ q := le_inf hcc.le le_sup_right
        rcases h1.lt_or_eq with h1 | h1
        · exfalso
          rcases (inf_le_left : c' ⊓ q ≤ c').lt_or_eq with h2 | h2
          · exact hcc.2 h1 h2
          · exact h (h2 ▸ inf_le_right)
        · exact h1.symm
      have hc : c' ⊓ q ⋖ c' := by rw [hmeet]; exact hcc
      have := r_covBy (IsUpperModularLattice.covBy_sup_of_inf_covBy hc)
      rw [sup_comm] at this; omega
  -- meet step (lower semimodularity)
  have hL : ∀ p : α, ∀ c c' : α, c ⋖ c' → r (p ⊓ c') ≤ r (p ⊓ c) + 1 := by
    intro p c c' hcc
    set q := p ⊓ c'
    have hq : p ⊓ c = q ⊓ c := by
      simp only [q]; rw [inf_assoc, inf_eq_right.mpr hcc.le]
    rw [hq]
    by_cases h : q ≤ c
    · rw [inf_eq_left.mpr h]; omega
    · have hj : c ⊔ q = c' := by
        have h1 : c ⊔ q ≤ c' := sup_le hcc.le inf_le_right
        rcases h1.lt_or_eq with h1 | h1
        · exfalso
          rcases (le_sup_left : c ≤ c ⊔ q).lt_or_eq with h2 | h2
          · exact hcc.2 h2 h1
          · exact h (h2 ▸ le_sup_right)
        · exact h1
      have hc : c ⋖ c ⊔ q := by rw [hj]; exact hcc
      have := r_covBy (IsLowerModularLattice.inf_covBy_of_covBy_sup hc)
      rw [inf_comm] at this; omega
  -- the rank identity r a + r b = r (a ⊔ b) + r (a ⊓ b)
  have hval : ∀ a b : α, r a + r b = r (a ⊔ b) + r (a ⊓ b) := by
    intro a b
    have u := r_step_le (fun x => b ⊔ x) (hU b) (a ⊓ b) a inf_le_left
    have l := r_step_le (fun x => b ⊓ x) (hL b) a (a ⊔ b) le_sup_left
    rw [show b ⊔ a ⊓ b = b from sup_eq_left.mpr inf_le_right, sup_comm] at u
    rw [show b ⊓ (a ⊔ b) = b from inf_eq_left.mpr le_sup_right, inf_comm] at l
    omega
  refine ⟨fun {x} y {z} hxz => ?_⟩
  set x' := x ⊔ y ⊓ z
  set z' := (x ⊔ y) ⊓ z
  have hle : x' ≤ z' := le_inf (sup_le_sup_left inf_le_left x) (sup_le hxz inf_le_right)
  have hj1 : x' ⊔ y = x ⊔ y := by
    simp only [x']; apply le_antisymm
    · exact sup_le (sup_le le_sup_left (inf_le_left.trans le_sup_right)) le_sup_right
    · exact sup_le (le_sup_left.trans le_sup_left) le_sup_right
  have hj2 : z' ⊔ y = x ⊔ y := by
    apply le_antisymm
    · exact sup_le inf_le_left le_sup_right
    · rw [← hj1]; exact sup_le_sup_right hle y
  have hm2 : z' ⊓ y = y ⊓ z := by
    simp only [z']; apply le_antisymm
    · exact le_inf inf_le_right (inf_le_left.trans inf_le_right)
    · exact le_inf (le_inf (inf_le_left.trans le_sup_right) inf_le_right) inf_le_left
  have hm1 : x' ⊓ y = y ⊓ z := by
    apply le_antisymm
    · rw [← hm2]; exact inf_le_inf_right y hle
    · exact le_inf le_sup_right inf_le_left
  have v1 := hval x' y
  have v2 := hval z' y
  rw [hj1, hm1] at v1; rw [hj2, hm2] at v2
  exact (eq_of_le_of_r_eq hle (by omega)).ge

/-- an orthocomplementation: an antitone involution giving a complement -/
structure Ortho (α : Type*) [Lattice α] [BoundedOrder α] where
  oc : α → α
  anti : ∀ {a b : α}, a ≤ b → oc b ≤ oc a
  invol : ∀ a, oc (oc a) = a
  inf_oc : ∀ a, a ⊓ oc a = ⊥
  sup_oc : ∀ a, a ⊔ oc a = ⊤

variable [BoundedOrder α]

omit [Finite α] in
theorem Ortho.le_iff (O : Ortho α) {a b : α} : O.oc a ≤ O.oc b ↔ b ≤ a :=
  ⟨fun h => by simpa [O.invol] using O.anti h, O.anti⟩

omit [Finite α] in
theorem Ortho.oc_sup (O : Ortho α) (a b : α) : O.oc (a ⊔ b) = O.oc a ⊓ O.oc b := by
  apply le_antisymm
  · exact le_inf (O.anti le_sup_left) (O.anti le_sup_right)
  · rw [← O.invol (O.oc a ⊓ O.oc b), O.le_iff]
    exact sup_le (by rw [← O.le_iff, O.invol]; exact inf_le_left)
      (by rw [← O.le_iff, O.invol]; exact inf_le_right)

omit [Finite α] in
theorem Ortho.oc_inf (O : Ortho α) (a b : α) : O.oc (a ⊓ b) = O.oc a ⊔ O.oc b := by
  have := O.oc_sup (O.oc a) (O.oc b)
  rw [O.invol, O.invol] at this
  rw [← this, O.invol]

omit [Finite α] in
theorem Ortho.covBy (O : Ortho α) {a b : α} (h : a ⋖ b) : O.oc b ⋖ O.oc a := by
  refine ⟨lt_of_le_of_ne (O.anti h.le) (fun e => h.lt.ne ?_), fun c h1 h2 => ?_⟩
  · simpa [O.invol] using congrArg O.oc e.symm
  · have h1' : O.oc c < b := by
      have := O.anti h1.le; rw [O.invol] at this
      exact lt_of_le_of_ne this (fun e => h1.ne (by rw [← e, O.invol]))
    have h2' : a < O.oc c := by
      have := O.anti h2.le; rw [O.invol] at this
      exact lt_of_le_of_ne this (fun e => h2.ne (by rw [e, O.invol]))
    exact h.2 h2' h1'

omit [Finite α] in
/-- **An orthocomplementation turns upper into lower semimodularity** (PROVED-IN-MODEL). -/
theorem lower_of_upper_ortho [IsUpperModularLattice α] (O : Ortho α) :
    IsLowerModularLattice α := by
  refine ⟨fun {a b} h => ?_⟩
  have h1 : O.oc a ⊓ O.oc b ⋖ O.oc a := by rw [← O.oc_sup]; exact O.covBy h
  have h2 := IsUpperModularLattice.covBy_sup_of_inf_covBy h1
  have h3 := O.covBy h2
  rw [← O.oc_inf, O.invol, O.invol] at h3
  exact h3

/-- **Finite-height lemma** (PROVED-IN-MODEL): a finite upper semimodular lattice with an
orthocomplementation is modular. -/
theorem modular_of_upper_ortho [IsUpperModularLattice α] (O : Ortho α) : IsModularLattice α := by
  have _ := lower_of_upper_ortho O
  exact modular_of_semimodular

/-- **Orthomodular law** (PROVED-IN-MODEL): in a finite upper semimodular orthocomplemented
lattice, `a ≤ b → a ⊔ (a⊥ ⊓ b) = b`, the orthomodularity Piron's theorem needs. -/
theorem orthomodular_of_upper_ortho [IsUpperModularLattice α] (O : Ortho α) {a b : α}
    (hab : a ≤ b) : a ⊔ (O.oc a ⊓ b) = b := by
  have _ := modular_of_upper_ortho O
  rw [← sup_inf_assoc_of_le (O.oc a) hab, O.sup_oc, top_inf_eq]

end GTAORnd.SelfRef.LR3.Modular

namespace GTAORnd.SelfRef.LR3.Modular

/-- **Finitely many atoms give a finite lattice** (PROVED-IN-MODEL): in an atomistic complete
lattice with finitely many atoms, there are finitely many elements. -/
theorem finite_of_atomistic {β : Type*} [CompleteLattice β] [IsAtomistic β]
    (hfin : Set.Finite {a : β | IsAtom a}) : Finite β := by
  have := hfin.to_subtype
  refine Finite.of_injective
    (fun x : β => ({a : {a : β | IsAtom a} | (a : β) ≤ x} : Set {a : β | IsAtom a})) ?_
  intro x y hxy
  rw [← sSup_atoms_le_eq x, ← sSup_atoms_le_eq y]
  congr 1
  ext a
  constructor
  · rintro ⟨ha, hax⟩
    refine ⟨ha, ?_⟩
    have := Set.ext_iff.mp hxy ⟨a, ha⟩
    exact this.mp hax
  · rintro ⟨ha, hay⟩
    refine ⟨ha, ?_⟩
    have := Set.ext_iff.mp hxy ⟨a, ha⟩
    exact this.mpr hay


/-- **Atomistic plus covering gives upper semimodular** (PROVED-IN-MODEL). In an atomistic
complete lattice with the covering property (`p` an atom, `p ≰ a` ⇒ `a ⋖ a ⊔ p`), the lattice is
upper semimodular. -/
theorem upper_of_atomistic_covering {β : Type*} [CompleteLattice β] [IsAtomistic β]
    (hcov : ∀ a p : β, IsAtom p → ¬ p ≤ a → a ⋖ a ⊔ p) : IsUpperModularLattice β := by
  refine ⟨fun {a b} h => ?_⟩
  -- an atom below `a` and not below `a ⊓ b`
  obtain ⟨p, hp, hpa, hpab⟩ : ∃ p, IsAtom p ∧ p ≤ a ∧ ¬ p ≤ a ⊓ b := by
    by_contra hcon
    push Not at hcon
    apply h.lt.ne'
    apply le_antisymm _ inf_le_left
    calc a = sSup {q | IsAtom q ∧ q ≤ a} := (sSup_atoms_le_eq a).symm
      _ ≤ a ⊓ b := sSup_le fun q ⟨hq, hqa⟩ => hcon q hq hqa
  have hjoin : a ⊓ b ⊔ p = a := by
    have h1 : a ⊓ b < a ⊓ b ⊔ p := lt_of_le_of_ne le_sup_left (fun e => hpab (e ▸ le_sup_right))
    exact (h.eq_or_eq h1.le (sup_le inf_le_left hpa)).resolve_left h1.ne'
  have hpb : ¬ p ≤ b := fun hb => hpab (le_inf hpa hb)
  have hab : a ⊔ b = b ⊔ p := by
    apply le_antisymm
    · rw [← hjoin]
      exact sup_le (sup_le (inf_le_right.trans le_sup_left) le_sup_right)
        (le_sup_left)
    · exact sup_le le_sup_right (hpa.trans le_sup_left)
  rw [hab]
  exact hcov b p hp hpb

/-- **The lattice-route step in one statement** (PROVED-IN-MODEL): an atomistic complete lattice
with finitely many atoms, the covering property and an orthocomplementation is orthomodular. -/
theorem orthomodular_of_atomistic {β : Type*} [CompleteLattice β] [IsAtomistic β]
    (hfin : Set.Finite {a : β | IsAtom a})
    (hcov : ∀ a p : β, IsAtom p → ¬ p ≤ a → a ⋖ a ⊔ p) (O : Ortho β) {a b : β} (hab : a ≤ b) :
    a ⊔ (O.oc a ⊓ b) = b := by
  have _ := finite_of_atomistic hfin
  have _ := upper_of_atomistic_covering hcov
  exact orthomodular_of_upper_ortho O hab


end GTAORnd.SelfRef.LR3.Modular
