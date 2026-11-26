# Record cost: errata after a hostile review of the foundations

*Thursday 26 November 2026 (America/New_York). Written after a fresh-context hostile review of the record-cost notes, Lean layer and preregs carried in PR #295 (session file `HOSTILE_REVIEW_FOUNDATIONS.md`). Append-only: the notes below are corrected here, and their earlier text is left as committed. `THEORY.md`, `CORE.md`, locked blobs and committed preregs are unchanged. Labels as in the rounds 4–9 note: **PROVED (in-model)**, **OBSERVED (numerical)**, **KNOWN**, **HYPOTHESIS**, **OPEN** and **open miss**.*

## 1. Rounds 4–9 note, `theory/RECORD_COST_ROUNDS4-9_2026-11-25.md:62` (§8 remark)

**Overclaimed:** "… without a time-evolution premise."

**Corrected (HYPOTHESIS, still offered as a remark):** inside the Jordan class, hereditary SFP plus the cheapest bit leaves complex quantum theory *without naming a Hamiltonian or energy observable, but with an infinite transitive reversible group (which, with SFP, is equivalent to U in the transitive class) and with the reversible group restricted to the identity component or to completely positive maps.*

Two facts the note should have stated:
- **SFP plus transitivity already implies U (PROVED (in-model), KNOWN ingredient).** A group acting transitively on finitely many (≥ 2) pure states has an element with no fixed point (Jordan's theorem; Lean `jordan_derangement`, `finite_transitive_not_SFP` in `formal/lean/GTAO/Rnd/SelfRef/SFP.lean`). So any step that uses SFP on a transitive state space has assumed infinitely many pure states, i.e. U. SFP is not independent of U.
- **SFP is a property of a (state space, group) pair.** The qubit ball passes with SO(3) (`odd_ball_SFP`) and fails with its full affine symmetry group O(3): the point reflection −I fixes no pure state (in Hilbert-space terms, qubit time reversal, whose square is −1). At m = 0, `odd_ball_SFP` is SFP of the trivial group on the classical bit. "SFP selects the ball" therefore depends on a rule for which maps count as reversible: connectedness (premise CD again) or extension to composites (complete positivity, a composition premise). Polytopes were tested with their full finite groups. The rule is stated once in the frozen premise list `theory/qm-selection-2026-11-26/PREREG.md` (added by a later commit of this PR).

**What most of the selection does (KNOWN).** Within the Jordan class (Jordan, von Neumann and Wigner 1934), bit faces are balls of dimension k+1 for k = 1, 2, 4, 8; "the bit is the 3-ball" already singles out complex quantum theory, the usual endpoint of reconstruction arguments (Barnum, Müller, Ududec 2014, NJP 16:123029, `10.1088/1367-2630/16/12/123029`). hSFP removes real quantum theory, even balls and direct sums; the cheapest bit removes the quaternionic and octonionic cases and odd balls of dimension ≥ 5, and needs the further premise that every bit face of a higher-rank system is the cheapest bit. The dimension price is not derived (chain note `:98`).

## 2. Round 10 note, `theory/RECORD_COST_ROUND10_2026-11-25.md:61` (Solèr branch)

**Overclaimed:** "That is PROVED (in-model) given Solèr and those results."

**Corrected:** PROVED (in-model) given Solèr's theorem, hereditary SFP on finite faces, and the cheapest-bit selection premise (HYPOTHESIS; its dimension price is not derived, chain note `:98`).

## 3. Round 10 note, `:55-59` (finite-geometry step): the orthomodularity line that was missing

The note applies Piron's representation theorem (rank ≥ 4) and the projective-plane argument (rank 3) to a lattice it had not shown to be orthomodular. The step holds, with this dependency (PROVED (in-model), standard lattice theory):

- Suppose the lattice had finitely many atoms. Then it has finite height.
- Atomistic plus the covering property gives **upper semimodular**.
- An orthocomplementation is an order-reversing involution, i.e. a dual automorphism, so the lattice is also **lower semimodular**.
- A lattice of finite length that is both upper and lower semimodular is **modular**; a modular orthocomplemented lattice is **orthomodular**.

So orthomodularity, which Piron's theorem needs, and the projective-geometry structure the rank-3 case needs, follow **from finite height plus atomistic plus covering plus the orthocomplementation**, which is exactly the situation of the proof by contradiction. Caveats that stay: the reading "orthocomplement = perfectly distinguishable from" (`:51`) is a premise and is not an orthocomplementation on the face lattice of a general GPT; irreducibility plus covering is the quantum-logic superposition principle, assumed, not derived (`:63`, `:83`); infinitely many atoms gives an infinite group only with transitivity (`:59`).

## 4. Round 10 note §15 and the session notes on Conjecture C

- The reason a regular polygon with ≥ 6 sides fails (★) was given as "some n·v = 0". That is false for the octagon and the 12-gon (minimum |n·v| = 0.414 and 0.268, OBSERVED (numerical) in the reviewer's rerun) and for the icosahedron and dodecahedron. The correct reason is some |n·v| < 1, i.e. R²|n|² ≠ m. The exclusions stand. (Also corrected in §17 of the round 10 note by the M11 review worker.)
- In the session notes, the LP values "icosahedron² Φ = −2.54, dodecahedron² −0.44, cuboctahedron² −1.5" were printed next to a description of a random-objective LP over all of max. Those values come from the **zero-marginal slice** search. Over all of max the random-objective LP best is 0, attained at products (OBSERVED (numerical), search not proof). These numbers are not quoted in any repository note; recorded here so that no later fold quotes them as full-max values.

## 5. Session note on forces and gravity (not in the repository)

The session note's summary called the record-cost idea one "which already points toward quantum structure". Corrected: the record-cost idea ranks quantum-like records cheapest in toy models *only under the continuous-drift premise CD*; without drift it ranks classical or polytope records cheapest. Nothing in the forces and gravity rounds is folded yet; they take quantum mechanics as an input.

## 6. Lean headline names and counts

The Lean layer builds with the standard axioms only and has no `sorry`. But several names state more than the theorem proves, and the raw count is not a measure of depth:
- `disk_strictly_cheaper` proves the polygon ring's Σ > 0; the disk side is the literal 0 of NA4 (a definition, chain note `:75`).
- `ball_record_bound` is the triangle inequality for an isometry; the content is the model.
- `no_zero_drift_while_recording` is a tautology with no axioms; the prose conclusion is modelling.
- `liar_half` appears in two namespaces; `P2_entries` is four numeric facts.
- `disk_exceeds_ball` uses one symbol δ for a static axis-angle error (ball) and a per-step rate error (disk); "the ball beats the disk" holds only under that identification.
- Not in Lean and load-bearing: NA1 (the SO(3) classification), the maximal-torus SFP criterion, the Jordan-class classification, Piron, Solèr, Baer, M11/M12, purification, and the cost-selection step.

At `e48494e` the source under `formal/lean/GTAO/Rnd/` has 102 `theorem`/`lemma` declarations, of which 85 are exported to the axiom audit (reviewer's rebuild).

## 7. Structural open miss: circularity across the chain

No single step is fallacious, and no complex numbers are hidden in steps S1–S4. Three loops are recorded as an **open miss**:
1. The route to U (round 10 `:157-163`) assumes a reversible entangling map. Any derivation of entanglement that passes through U, or through the ball parts U leads to, is circular.
2. Quantum theory is selected from a hand-picked menu with premises added after counterexamples (octahedron: CD and SFP; C1: heredity; stabilizer theory: no-restriction; real QM: hSFP; quaternionic QM: still OPEN). The premise list is frozen in `theory/qm-selection-2026-11-26/PREREG.md` (a later commit of this PR); any later premise must be logged there as a deviation with the counterexample that prompted it.
3. The forces and gravity rounds use quantum mechanics as input.

Sources: Barnum, Müller, Ududec 2014, `10.1088/1367-2630/16/12/123029`; Al-Safi, Richens 2015, NJP 17:123001, `10.1088/1367-2630/17/12/123001`; Baer 1946, Bull. AMS 52:77–93, `10.1090/S0002-9904-1946-08506-7` (Crossref-checked 26 November 2026, `theory/record-cost-2026-11-25/doi_check_7f.out`).

## 8. Frozen premise list and the round 9 search (appended)

The premise list is frozen in `theory/qm-selection-2026-11-26/PREREG.md` (lock commit `06f07e6`). The search that round 9 named (U(2) and Sp(1)×Sp(1) transitive bodies, affine dimension 4–8) is a **miss**: no counterexample. The non-Jordan bodies that pass hSFP there (the spin-3 zonal orbitope and B3 × B3) are centrally symmetric, so their capacity is 2 and the 3-ball beats them on dimension. The spin-1 ⊕ spin-2 family, C1 included, fails hSFP through an equatorial circle face (`RESULTS.md` there). This does not cover other groups or dimensions 9–15, and it was not a blind run (disclosed in the prereg).

## 9. Corrections to this file (appended after a hostile review of the errata commits)

- **§6, "Not in Lean … the maximal-torus SFP criterion".** The general criterion is not in Lean. Its concrete cases are: `ball_SFP_iff_odd`, `complex_fixes_ray`, `unitary_fixes_ray`, `real_odd_fixes_ray` and `real_even_not_SFP` in `formal/lean/GTAO/Rnd/SelfRef/SFPCriterion.lean` (commit `80cf785`, Lean round 3, already on the branch before this file was written).
- **§1, "assumed infinitely many pure states, i.e. U".** Read: "assumed infinitely many pure states, hence, **with a closed (compact) group**, U". An infinite transitive group gives a continuous group only after taking its closure.
- **PR-body items of the foundations review** are fixed in the PR #295 body itself, not in a repository note: line 1 ("Nothing was rebased" replaced by the #286 rebase disclosure), the #292 row (the run followed a gate pass by the author agent), and the horizon wording ("at the tested horizons (observed)", matching `cfa97cd`).
- **§4, the M11 reason** is unchanged. §8: the search is relabelled **`CONSISTENCY_CHECK`**, and "P7 is not needed" reads "P7 is not needed given P5 (hSFP)" (`theory/qm-selection-2026-11-26/DEVIATIONS.md`).
