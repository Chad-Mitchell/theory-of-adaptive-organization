# PREREG_C: does "self-reference (SR) + completeness (C)" give P? Written 2026-11-26 01:44 EST, before checking. Lock: PREREG_C.sha256.
Statements (fixed):
- SR (selfref NOTE.md:269; Breuer 1995, 10.1086/289852, Crossref-checked in selfref round 1): no part of a closed world
  holds a complete (pure) description of the whole. Every internal description of the whole is mixed.
- C_w (completeness, weak): the closed whole has no further fact beyond the state fixed by its parts' joint
  statistics. No hidden label selects a member of a convex decomposition of that state.
- C_s (completeness, strong): the closed whole is in a state of maximal information, i.e. not a proper mixture, fixed
  by its parts' joint statistics.
- P: the closed whole is (starts) in a pure state.
Expected claim:
- P ⇒ C_w;
- C_w ∧ SR ⇏ P (classical mixed-world countermodel);
- C_w holds in every GPT model by construction (the state is the complete description), so it adds no constraint;
- C_s ⇔ P (∧ LT for "fixed by joint statistics").
Verdict expected: completeness is either vacuous (C_w) or P renamed (C_s). Falsifier: a model of C_w ∧ SR with a mixed
whole that is shown inconsistent, or a C_w-forced purity step.
