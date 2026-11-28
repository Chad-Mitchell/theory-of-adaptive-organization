# Round C: self-reference + "completeness" vs P (2026-11-26, 01:44–01:50 EST). Prereg: PREREG_C.md, sha256 b4208391…7b93.

**Result (as preregistered).** Completeness is either vacuous or P under another name.
- **C1 [proved].** P ⇒ C_w. A pure state is an extreme point, so its only convex decomposition is trivial, and no label
  can select among distinct members.
- **C2 [proved, definitional].** C_w holds in every GPT model. The model's whole description of the world is its state
  ω, and there is no other variable that could carry a "further fact". So C_w constrains nothing.
- **C3 [proved in model, countermodel].** C_w ∧ SR ⇏ P. Take the classical 2-bit world, start (½δ₀+½δ₁)⊗δ₀, then CNOT.
  - C_w: read the mixed state as complete, with no hidden configuration.
  - SR: since the whole is mixed, every internal description of it is mixed.
  - P fails, yet the world tracks: I(A:B) = 1 bit (p1, E2a).
- **C4 [proved, definitional].** C_s ⇔ P. "Maximal information, not a proper mixture" is extremality. "Fixed by joint
  statistics" adds LT and nothing else.
- **Note [hypothesis].** If SR is read epistemically ("the whole is no better known than any internal description"),
  it pushes toward a *mixed* whole, i.e. against P.

**One paragraph.** The pair SR + completeness does not give P. Weak completeness is true of every GPT model by
construction and is compatible with a mixed whole: the classical countermodel tracks perfectly well. Strong
completeness ("the whole is in a state of maximal information") is P renamed. The self-reference result says what
parts can know about the whole, not what the whole is. So it cannot fix the whole's purity in either direction without
an extra ontic premise, and that premise is P. **Label: P stays an assumed, interpretive premise.** Completeness adds
no independent support. Moving on.

**DEVIATIONS.** PREREG_C.md uses the word "verdict", against the wording rules. Read it as "expected outcome". The
file is not edited, to keep the lock. Breuer 1995 DOI 10.1086/289852 is cited from the selfref round-1 Crossref check,
not re-checked this round.
