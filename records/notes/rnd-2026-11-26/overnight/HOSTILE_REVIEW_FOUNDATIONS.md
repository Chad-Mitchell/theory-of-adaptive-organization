# Hostile review of the foundations under PR #295 and tonight's rounds

*Thursday 26 November 2026, about 01:04–01:20 ET (America/New_York). Fresh-context referee pass, read-only: no commits, pushes, comments or email. I did not write any of the audited material.*

**What I read.**
- PR #295 at `e48494e`, as instructed: a read-only clone in `/workspace/audit-295`. The live PR head has since moved to `ddf559b` (updated 01:01 ET). That commit adds §15 of the round-10 note, the Theorem M11 text. I read §15 from `ddf559b` (`git show ddf559b:theory/RECORD_COST_ROUND10_2026-11-25.md`, lines 169–207).
- The repository copy in `/workspace/fresh-11`, used for `CORE.md`.
- The lab notes: `rnd/selfref/NOTE.md` rounds 4–12, `rnd/forces-gravity/NOTE.md`, `rnd/entangle/`, `rnd/lean/`, and `WORKLOG.md`.
- The gate reads in `/workspace/gtao-notes/`.

**What I re-ran.** I rebuilt the Lean layer at `e48494e` in a scratch copy (`/workspace/lean-audit-295`), using Lean `v4.37.0-rc1` with the pinned Mathlib (same manifest revs).
- `lake build GTAO` finished with exit 0.
- `lake env lean scripts/RndAxioms.lean` printed 85 lines. 84 of them list only `propext`, `Classical.choice` and `Quot.sound`, or a subset. `SelfRefRun.no_zero_drift_while_recording` depends on no axioms.
- There is no `sorry`, no `axiom` declaration and no `admit` under `GTAO/Rnd/`.
- The source has 102 `theorem`/`lemma` declarations, of which 85 are exported.

Status words: **SOUND**, **SOUND-WITH-CAVEAT**, **OVERCLAIMED** (corrected wording given), **OPEN MISS / UNSUPPORTED**. Paths are relative to the repo root at `e48494e` unless they start with `/workspace`.

---

## Summary table

| item | status | one-line reason |
|---|---|---|
| (a) cost principle and selection | SOUND-WITH-CAVEAT | Honestly scoped in the chain note. Every no-drift comparison favours classical or polytope records. Quantum-like records win only under the assumed premise CD and the definitional NA4 ("disk pays 0"). One downstream note overstates it. |
| (b) Conjecture C and the route to U | SOUND-WITH-CAVEAT (logic). Conjecture C itself is OPEN. | The conditional remark is valid. It *assumes* a reversible entangling map and no-restriction. M11 is correct but covers only hypercube and cross-polytope parts in locally symmetric composites. |
| (c) Round 9, hSFP + cheapest bit | OVERCLAIMED in two sentences; the logic holds | Most of the answer comes from the Jordan-class premise. Given transitivity, SFP already implies U (by Jordan's theorem). The SFP outcome depends on which group is called "reversible": the qubit ball passes with SO(3) and fails with its full symmetry group O(3). |
| (d) Round 10 lattice route | SOUND-WITH-CAVEAT | The finite-geometry step is correct. Orthomodularity, which Piron's theorem needs, is not listed, but it follows in finite height (one line, given below). The "records as an orthocomplemented lattice" reading, irreducibility and covering are premises, and they amount to the superposition principle. |
| (e) Lean layer | SOUND-WITH-CAVEAT | Builds clean with standard axioms only. Several "headline" names prove much less than their names suggest: `disk_strictly_cheaper` only shows the ring's Σ > 0; `ball_record_bound` is the triangle inequality; `no_zero_drift_while_recording` is a tautology. `odd_ball_SFP` at m = 0 is SFP with the trivial group. The load-bearing steps (NA1, the maximal-torus criterion, Piron, Solèr, Baer, M11) are not in Lean. |
| (f) Prereg #286 | SOUND-WITH-CAVEAT | The lock content and hash hold. The lock commit `f18721fc` is **not in the carried history**: the source branch was rebased 2026-11-25 23:06 ET. The PR body says "Nothing was rebased". Five of the ten "locked bars" are self-labelled consistency checks. |
| (f) Prereg #290 | SOUND-WITH-CAVEAT, bordering OVERCLAIMED | P1 was re-scored from "not scorable" to "hit" after the scorer had seen which way it leaned. The re-score cites a box-only gate read. As a *runtime-RAM* share, the hit rests on a grouping choice and residency assumptions. The overall outcome (open miss) is unchanged. |
| (f) Prereg #292 | SOUND-WITH-CAVEAT | All five locks precede the runs, and the script hashes match. But `PREREG_5.md:3` requires a *fresh independent* gate reader. The run followed gate read v5, which `RESULTS.md:7` says was done by the author agent. That breach is not logged in `DEVIATIONS.md`. Both results were misses, so no favourable bias followed. |
| (g) circularity across (a)–(d) | OPEN MISS (structural) | Complex numbers are not secretly built into steps S1–S4. Three loops do exist, though. The U route assumes entangling dynamics. Quantum mechanics is the selected answer from a hand-picked menu, guarded by premises added after counterexamples. The forces and gravity rounds take quantum mechanics as an input. |

---

## (a) The cost principle: records cost resources, and the selection that results

**What holds.**
- `theory/RECORD_COST_CHAIN_2026-11-25.md:5` and `:27` say outright that selection is the hypothesis at `CORE.md:7`, applied by assumption: **"The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."**
- `:13` narrows the claim to "cost selects quantum-like records under drift", and `:11` states premise CD as not derived.
- `:66` and open miss 1 at `:92` record that without drift the square and boxworld are cheaper.
- The memory-coordinate definition was locked before the runs (`:64`). That is good discipline.

**Caveats.**
1. **Every drift-free comparison goes against quantum records.** Zero drift favours the classical bit (2.00 vs 2.16) and the square (round 10 `:35`, rounds 4–9 `:18`). An unknown update favours polytopes (rounds 4–9 `:51`). J at a finite horizon favours odd polygons (round 10 `:147-150`). Inflow and selection are blind to geometry (rounds 4–9 `:35`). So the cost itself never selects a continuous group. The quantum-like ranking comes from CD (`:11`) together with NA4 (`:75`: "the disk pays 0" is *a definition*). The polygon tracker's Σ > 0 is computed, while the disk's Σ is set to 0. That asymmetry is what CD buys.
2. **The "cheapest" steps need a dimension price that is not derived.** The chain note says so itself (`:98`: "uses a dimension price inside the transitive class, which additivity alone does not fix"). The stake q = 4 is a convention (`:62`).
3. **Downstream overstatement.** `/workspace/gtao-notes/rnd/forces-gravity/NOTE.md:11` says "the record-cost idea, which already points toward quantum structure".
   - **Corrected wording:** "the record-cost idea, which ranks quantum-like records cheapest in toy models *only under the continuous-drift premise CD*; without drift it ranks classical or polytope records cheapest."

**Status: SOUND-WITH-CAVEAT.**

## (b) Conjecture C and the route to a continuous reversible group U

**What the route says** (`theory/RECORD_COST_ROUND10_2026-11-25.md:157-163`). U follows from four premises together: transitivity, no-restriction, one reversible entangling map, and Conjecture C.

**Logic: valid.** C plus an entangling map means the parts are not no-restriction polytopes, so they have infinitely many extreme points. Transitivity then makes the group infinite. The closure of an infinite compact subgroup of GL has positive dimension (Cartan, `:68`).

**Caveats.**
1. **Premise 3 is entanglement dynamics, assumed.** The route to U consumes the existence of a reversible entangling map. Any later "derivation of entanglement" that uses U, or the ball parts that U leads to, is circular. This is risk 1 below.
2. **No-restriction is doing selective work.** The one finite theory with reversible entangling dynamics, stabilizer theory, is excluded only by no-restriction (`:142`: the Bell state scores −0.5 on a product effect). The note flags that no-restriction is not in the record-cost chain (`:163`).
3. **M11 is correct but narrow.** I checked the proof step by step (`ddf559b` round-10 note `:194-207`; `rnd/selfref/NOTE.md:1065-1089`):
   - The Löwner ellipsoid is preserved, by uniqueness and because the map preserves volume.
   - The centre is fixed, since irreducible blocks have no fixed vectors.
   - Schur's lemma applies: the three blocks are pairwise inequivalent, and ρ_A⊗ρ_B is irreducible for G_A×G_B.
   - Lemma 1 follows: the four sign-product effects give |nᵀCm| ≤ 1, and the second moment of the facet normals is scalar by absolute irreducibility. Facet transitivity is not needed.
   - Lemma 2 follows by the standard conditional-state argument.
   - The strict q gap follows because |a| < R_A for non-vertices of an inscribed polytope.

   The scope is narrow. (★) plus *absolute irreducibility* leaves hypercubes and cross-polytopes. Mixed Hanner polytopes satisfy (★), but their symmetry groups are reducible. Those parts are dichotomic, so for the **max** composite M11 adds nothing beyond Al-Safi–Richens Thm 1 (Al-Safi, Richens 2015, NJP 17:123001, `10.1088/1367-2630/17/12/123001`, Crossref-checked today). The new content is *locally symmetric intermediate* composites. The prose at `:173` states the class restriction correctly.
4. **Small factual slips.**
   - `rnd/selfref/NOTE.md:1096` says regular polygons with six or more sides fail (★) because "some n·v = 0". That is false for the octagon and the 12-gon: `hostile_m11_outputs.txt` gives min |n·v| = 0.414 and 0.268. They fail because R²|n|² ≠ m. The same wording is in `ddf559b` `:207`.
   - `rnd/selfref/NOTE.md:1320-1323` reports "icosahedron² best Φ = −2.54 … dodecahedron² −0.44" next to "random-objective LP over all of max". Those negative numbers are from the **zero-marginal slice**. Over all of max the LP best is 0, attained at products (`outputs_m.txt:538-549`; `forces-gravity/outputs/q5_platonic_lp_rerun.txt`). State which search each number comes from.
5. **Coverage.** Composites are bipartite only. Non-symmetric intermediate composites were sampled, not exhausted. One symmetric octahedron × octahedron sample was stopped by hand. Exact enumeration of cuboctahedron × cuboctahedron did not finish. Icosahedron × dodecahedron fails (♦) (Φ = +2.05), so M12 says nothing there.

**Status:** the logic of the route is SOUND-WITH-CAVEAT. **Conjecture C is OPEN**: proved for one class, with observed certificates for about 400 composites. U is **not derived** from the record-cost premises; README row RECORD-COST-U already says so.

## (c) Round 9: complex QM selected within the Jordan class by hereditary SFP plus a cheapest-bit cost. Is the answer assumed?

**The claim.** `theory/RECORD_COST_ROUNDS4-9_2026-11-25.md:62` and `rnd/selfref/NOTE.md:641,700` say: inside the Jordan class, hereditary SFP plus "the cheapest bit" (minimal affine dimension at capacity 2) leaves complex quantum theory in every dimension, "without a time-evolution premise".

**What each premise actually does.**
- **The Jordan class supplies almost everything.** The simple Euclidean Jordan algebras are real, complex and quaternionic Hermitian matrices, spin factors, and the 3×3 octonionic algebra (Jordan, von Neumann, Wigner 1934). Their rank-2 faces are balls of dimension k+1 for k = 1, 2, 4, 8. Within that menu, "the bit is the 3-ball" already singles out complex quantum theory. That is the usual endpoint of reconstruction arguments (Barnum, Müller, Ududec 2014, NJP 16:123029, `10.1088/1367-2630/16/12/123029`, Crossref-checked).
- **hSFP only filters by parity.** It removes real quantum theory (its bit faces are disks), even balls, and direct sums (a swap fixes no pure state).
- **The cheapest bit removes the rest.** It picks the 3-ball over the 5-ball (quaternionic), the 9-ball (octonionic) and odd balls of dimension 5 and up. That requires a further implicit premise: every bit face of a higher-rank system must be the cheapest bit. The dimension price itself is not derived (chain note `:98`).
- **So both premises work, but only after the Jordan premise has done most of the selection.** The Jordan class carries homogeneity, self-duality and spectrality, and those are what make the menu quantum-like.

**Hidden strength of SFP (new point).**
1. **SFP plus transitivity already implies U.** A transitive group on finitely many pure states (at least 2) has a fixed-point-free element (Jordan; `SFP.lean:41`). So any chain that uses SFP on a transitive state space has assumed infinitely many pure states, which is U. The notes concede the motivation side ("not motivated without U", rounds 4–9 `:45`). They should also state this implication.
2. **SFP is a property of (state space, group) pairs, not of state spaces.** The qubit ball passes with SO(3) (`odd_ball_SFP`). With its full affine symmetry group O(3), the point reflection −I fixes no pure state, so it fails. In Hilbert-space terms this is the qubit time reversal iσ_yK, whose square is −1, so it has no eigen-ray. Lean's `odd_ball_SFP 0` shows that the 1-ball, which is the classical bit, satisfies SFP under the trivial group SO(1). So "SFP selects the ball" depends on a rule for which maps count as reversible. That rule is either connectedness (CD again) or extension to composites, i.e. complete positivity (a composition premise). Polytopes, by contrast, are tested with their full finite groups. The group rule has to be stated once and applied to every candidate.

**Overclaims and corrected wording.**
- Rounds 4–9 `:62`, "without a time-evolution premise". **Corrected:** "without naming a Hamiltonian or energy observable, but with an infinite transitive reversible group (which, with SFP, is equivalent to U in the transitive class) and with the reversible group restricted to the identity component or to completely positive maps."
- Round 10 `:61` labels the Solèr branch "PROVED (in-model) given Solèr and those results", but "the cheapest bit" is a selection HYPOTHESIS. **Corrected:** "PROVED (in-model) given Solèr's theorem, hereditary SFP on finite faces, and the cheapest-bit selection premise (HYPOTHESIS; its dimension price is not derived, chain note `:98`)."

**What holds.**
- Round 9's own "Assumed" list is honest: `rnd/selfref/NOTE.md:680-684` lists an infinite group, heredity, the Jordan class and the cheapest bit.
- The label at rounds 4–9 `:62` is "HYPOTHESIS, offered as a remark".
- C1, the spin-1+2 orbitope, checks out: Σᵢ(1+3n·tᵢ)²/16 = (4 + 0 + 9·4/3)/16 = 1, and pᵢ(tⱼ) = δᵢⱼ. It is a genuine counterexample to "SFP plus minimal dimension".

**Status: OVERCLAIMED in two sentences; the logic holds.** The answer is substantially assumed through the Jordan class, and the cheapest bit then does the final selection.

## (d) Round 10: the lattice route (covering plus at least 3 orthogonal atoms gives infinitely many atoms)

**The claim** (round 10 `:55-59`). An irreducible, atomistic, orthocomplemented lattice with the covering property and at least three mutually orthogonal atoms has infinitely many atoms. For rank 4 and up the note uses Piron, then Wedderburn and Chevalley. For rank 3 it uses Baer: finite planes have absolute points (Baer 1946, `10.1090/S0002-9904-1946-08506-7`, Crossref-checked).

**Check.** Suppose there were finitely many atoms. Then:
- The lattice has finite height.
- Atomistic plus covering gives upper semimodular.
- An orthocomplementation is a dual automorphism, so the lattice is also lower semimodular.
- Finite length with both upper and lower semimodularity gives **modular**. A modular orthocomplemented lattice is orthomodular.

So the orthomodularity that Piron's theorem needs, and the "projective plane" structure that the rank-3 case needs, both follow. **But the note never says this. It invokes Piron on a lattice it has not shown to be orthomodular.** Add the one line above. The rest also holds:
- An anisotropic Hermitian form diagonalizes in any characteristic, because ⟨v,v⟩ ≠ 0 for v ≠ 0. So `diag_form_isotropic` and `norm_form_isotropic` in `rnd/lean/GTAORnd/R11/FiniteGeometry.lean` cover the general case once Piron is granted.
- A finite plane's orthocomplementation would be a polarity with no absolute point, which Baer's theorem rules out.

**Caveats.**
1. **The lattice reading is a premise.** "Orthocomplement = perfectly distinguishable from" (`:51`) is not an orthocomplementation on the face lattice of a general GPT. It holds in special classes, such as spectral or Jordan-type state spaces.
2. **Irreducibility plus covering is the quantum-logic superposition principle.** The route works because it assumes it. The note says this candidly at `:63` and `:83`.
3. **Infinitely many atoms is not U.** It gives an infinite group only with transitivity (`:59`, which says so).
4. **The stabilizer control does real work.** It shows that the covering property is load-bearing (`:60`), and that is a genuine contribution.

**Status: SOUND-WITH-CAVEAT.** Add the finite-height modularity line, and label the lattice reading as a premise.

## (e) The Lean layer: formal statements against the prose claims

Build and axioms: as above. **No `sorry`, no extra axioms, no `False`-deriving hypothesis found.**

The hypotheses of the substantive theorems are satisfiable:
- `R3_full`, `dim_bound`: the Bloch ball with rotations about z, fixing the poles.
- `lemmaB1`: `squareModel`, `square_B1_hypotheses` (`SquareBit.lean:68,189`).
- `no_linear_clone_gpt`: any circle orbit with a visible top Fourier mode.

| theorem (file:line) | prose claim | what Lean proves | gap |
|---|---|---|---|
| `jordan_derangement`, `finite_transitive_not_SFP` (`SelfRef/SFP.lean:41,79`) | finite transitive groups fail SFP | exactly that, via Burnside | none: real content |
| `odd_ball_SFP` (`SFP.lean:172`) | odd balls, including the qubit, satisfy SFP | SFP for **SO**(2m+1) on the sphere | the group choice is load-bearing: O(2m+1) fails (−I). At m = 0 it is SFP of the **trivial** group on a 2-point set, i.e. the classical bit passes. The `SFP` definition (`:34`) has no transitivity. Add an `O(3)`-fails control and a transitivity hypothesis to any "selection" corollary. |
| `even_ball_not_SFP` (`SFP.lean:225`) | even balls fail | correct; m = 0 is the empty sphere, so vacuous | docstring admits it; harmless |
| `disk_not_SFP` (`SFP.lean:211`) | the rebit fails | correct (−1 ∈ SO(2)) | none |
| `ball_record_bound` (`SelfRef/Precision.lean:36`) | the ball record stays within 2 sin δ for all time | ‖Rᵏp − p‖ ≤ 2‖p‖ for any isometry fixing u (triangle inequality) | trivial. The content is the model. |
| `disk_exceeds_ball` (`Precision.lean:119`) | the disk falls behind the ball at finite precision | compares 2 sin δ (ball, a **static axis-angle** error δ) with the disk error under a **per-step rate** error δ | the same symbol stands for two different quantities. "The ball beats the disk" holds only under that identification; say so in rounds 4–9 `:45`. |
| `no_copy_mixture` (`Precision.lean:145`) | L5, partial | the linear core only | labelled partial (`:83`); OK |
| `disk_strictly_cheaper` (`PolygonDrift.lean:195`) | S3: the disk is strictly cheaper than any polygon | `lam*0 < lam*ringSigma`, i.e. the ring's Σ > 0. The disk is the literal 0. | **the name overstates.** The disk's 0 is NA4's definition (chain `:75`). Rename it or add a docstring line saying the disk side is definitional. |
| `ring_bound`, `factor_ge_two` (`PolygonDrift.lean:150,160`) | the TUR-type polygon bound | correct for the defined `ringV` and `ringSigma` | the definitions are NA3, not derived from a path measure (declared) |
| `R3_full` / `dim_bound` (`SelfRef/R34.lean:116`, `DimBound.lean:66`) | S2: d ≥ N+1 | faithful, under the declared `hinv` (NA2) | five hypotheses are unused (declared); not vacuous |
| `fourier_core`, `no_linear_clone_gpt` (`R34.lean:42,66`) | S1: no linear cloner on a circle orbit | faithful for one effect f and the product effect ℓ | the Lie setting is NA5 (declared) |
| `normal_fixer_bot` (`SelfRef/Ball.lean:44`) | S4 group step | generic: a normal subgroup fixing a point is trivial under a faithful transitive action | "Ω is a ball" is NA1, not formalized (declared). The prose is OK. |
| `no_zero_drift_while_recording` (`SelfRefRun/Round2.lean:28`) | S8: zero drift only for a tracker that acquires nothing | if w d x ≠ w d' x for every x, then no x is fixed by both writes (a tautology; no axioms) | the prose conclusion is modelling, not Lean. Label it "elementary". |
| `liar_half` (`SelfRef/Liar.lean:30`, also `SelfRefRun/Basic.lean:32`) | S9 | e(w) = 1 − e(w) gives ½ | one line, and **duplicated** in two namespaces, so it inflates the count |
| `perm_periodic` (`SelfRefRun/Basic.lean:79`) | S7 | `orderOf` exists | trivial |
| `P1` (`Composition.lean:36`) | S5 price = c log count | real content (monotone and completely additive gives log) | none |
| `log_additive_iff`, `P2_entries` (`Composition.lean:101,115`) | additivity iff N_AB = N_A N_B | arithmetic; `P2_entries` is four numeric facts | the link to local tomography is prose. `P2_entries` should not count as a theorem in headline tallies. |
| `Jdial_stationary_iff` (`SelfRef/CostDial.lean:55`) | S10 stationarity | faithful | global minimum OPEN (declared); the refresh term is NA6 |
| `continuous_change_infinite_group`, `never_returns_infinite_order` (`SelfRef/ContinuousTime.lean:40,47`) | round 10 §3, §5 | faithful and elementary | "polytopes have finite groups" is not formalized (declared, `:97`) |

**Not in Lean, and load-bearing:**
- NA1 (the SO(3) classification, hence "ball");
- the maximal-torus SFP criterion;
- the Jordan-class classification;
- Piron, Solèr and Baer;
- M11 and M12;
- purification;
- the whole cost-selection step.

The overnight batch in `rnd/lean/GTAORnd/R11/` is not part of #295 and was not rebuilt by me. In it, `pure_marginal_product` takes the max-composite conditional states as a hypothesis (`hcone`), as `WORKLOG.md` says, and `FiniteGeometry.lean:20-23` lists what is not formalized.

**The direct answer to Chad's question.** The Lean is clean but thin. It certifies the algebraic cores. It does **not** certify the premises or the selection steps that carry the physics. It does not replace hostile review.

**Status: SOUND-WITH-CAVEAT.** Change the names and labels noted above, and stop quoting raw theorem counts as evidence of depth.

## (f) Prereg discipline in #286, #290 and #292

### #286 (T85 CTC fixed point)

**What holds.**
- The original lock commit `f18721fc` (committed 2026-11-24 16:14:59 ET) adds only `PREREG.md`, with the sha256 in its message.
- The score commit `3e1fcf9e` follows 11 min later (16:26:15 ET).
- The hash of `PREREG.md` today equals `756d9f0c…` at both commits.
- So the content was locked before the data. The earlier "hash timing" doubt resolves: the `.sha256` *file* arrived with the results, but the hash was in the lock commit message.

**Caveats.**
1. **The carried history is rebased.** The carried commits are `aaaa72c` and `74a6532`: same author dates, committer date 2026-11-25 23:06:20 ET. `f18721fc` is **not an ancestor** of the carried head `f19cd4a`. It survives only on `origin/forge-ctc-review`. `RUN_LOG.md:5` and `PREREG.sha256:2` cite `f18721fc`, and `DEVIATIONS.md` cites the scored commit `3e1fcf9e`; neither commit is in #295. The PR body line 1 says "Nothing was rebased … every prereg lock keeps its commit history". That is inaccurate for #286.
   - **Fix:** amend the PR body to say that #286's source branch was rebased on 2026-11-25 23:06 ET, that the original lock `f18721fc` is preserved on `forge-ctc-review`, and that the content hash is unchanged. Optionally merge or tag `forge-ctc-review` so the lock stays reachable.
2. **Five of the ten "locked bars" are consistency checks that could not miss** (`DEVIATIONS.md` bar-by-bar labels). The one substantive identification, route A, missed and was withdrawn. "Ten locked bars hit" should always be quoted as "five bars that could have missed hit; five were identities".

**Status: SOUND-WITH-CAVEAT.**

### #290 (Hutter budget)

**What holds.**
- Lock `4a0d5e9` at 11:29:09 ET; scoring `66640ab` at 11:35:11 ET. The scores are readings of published sources.
- The missing gate before scoring is disclosed (`DEVIATIONS.md:5`).

**The P1 re-score** (`RESULTS.md:93-108`, `DEVIATIONS.md:11`) followed the gate read's blocking item 4. The fallback "summed from allocation constants in its source" is in the lock (`PREREG.md:43`), so the re-score is **defensible from the lock text**. Problems:
1. **It was done after the direction was known.** `RESULTS.md:27` had already noted that an allocation share "would very likely be above 0.40".
2. **It flipped condition (i) of the overall rule to "met".**
3. **Allocation is not runtime RAM.** PPMD is disk-mapped (`mmap_to_disk = true`), and the locked quantity is a share of *runtime RAM* (`PREREG.md:43`). The RAM-side bound (≥ 0.41–0.46) needs `fxcm` to count as "one named model or table family" and needs residency assumptions. Both are choices made after the data.
4. **`DEVIATIONS.md:7` now contradicts `:3`** ("No allocation-based value is substituted"). It says it supersedes `:3`, which is acceptable for an append-only log.
5. **The trigger is not in the repo.** The gate read that triggered the re-score is cited by a **box path**, `/workspace/gtao-notes/gate_read_290.md` (`RESULTS.md:82`), which no outside reader can open.

**Corrected wording for P1:** "hit under the locked allocation-constant fallback (`PREREG.md:43`), re-scored after an independent gate read. As a runtime-RAM share it is not measured, because PPMD is disk-mapped; the RAM bound ≥ 0.41 assumes fxcm is one family and its tables are resident."

**Fix:** commit `gate_read_290.md` into `theory/hutter-2026-11-25/` and cite that path. The overall result (open miss) is unaffected.

**Status: SOUND-WITH-CAVEAT, bordering OVERCLAIMED.**

### #292 (who copies whom)

**What holds.**
- Five locks were made: `cde05b9` at 13:13:52, `7ba0d32` at 14:05:00, `b85e30d` at 14:24:15, `ea99183` at 14:42:56 and `df114b6` at 14:57:46 ET. The hashes of all five match today.
- The run scripts `run_t1_v2.py`, `run_t2_v2.py` and `aggregate.py` match the hashes locked in `PREREG_3.md`.
- T1 ran 22:11–22:12 and T2 22:15–22:41 on the box (`/workspace/gtao-notes/run292_*`). Both runs came after the last lock and were committed at 22:46 (`14394f9`).
- Both are clean misses, so no re-score favoured a hit.

**Caveats.**
1. **The run breached the lock's own condition.** `PREREG_5.md:3` reads: "**Nothing in T1, T2, T-form or T-acyclic runs until a fresh independent reader passes this Gate.**" Gate read v5 (`/workspace/gtao-notes/gate_read_292_v5.md:5`, and `RESULTS.md:7`) was done by **the same agent that wrote PREREG_5**. `RESULTS.md:7` discloses that. `DEVIATIONS.md` does **not** log it as a deviation from `PREREG_5.md:3`. **Fix:** append a dated DEVIATIONS line.
2. **Gate probes ran the scored code's cost and label functions on designed inputs before the run** (gate read v2 `:5-7`). The minimizer was not called, so the leak is small, but it is worth stating.
3. **Gate reads v1–v5 are box-only**, except `checks/gate_read_292_local.*`. Commit them or cite them by commit.
4. **The PR body line 12 says "The independent gate read is owed at review".** It should say the run already happened under a non-independent gate pass.

**Status: SOUND-WITH-CAVEAT.**

## (g) Circularity across (a)–(d)

- **Complex numbers.** I found none smuggled into S1–S4. The GPT frame is real-linear. Lean's use of ℂ in `Precision.lean` is only a coordinate for the circle.
- **Entanglement assumed, then used.** The route to U (round 10 `:157-163`) assumes a reversible entangling map. Masanes et al. 2014 (J. Math. Phys. 55:122203, `10.1063/1.4903510`, Crossref-checked) assume a *continuous* reversible group with non-trivial interaction, plus local tomography. A chain that runs "entangling map ⇒ U ⇒ ball parts ⇒ (MMPA) only the 3-ball entangles ⇒ entanglement derived" is a loop. `rnd/entangle/scripts/e1_interaction.py` tests premise I ("some non-trivial reversible interaction exists") in polytope composites. That is a test of the premise's *absence* in polytopes. It is not a derivation of its presence.
- **Menu and filter accretion.** The selection runs over a hand-picked menu: simplex, polygons, disk, ball, boxworld, QM pairs, then Jordan algebras. Each counterexample that beat quantum theory was met with a new premise:
  - the octahedron with all effects (capacity 2 at d = 3, round 10 `:35`) was excluded "by CD and by SFP, not by cost";
  - C1 (the spin-1+2 orbitope) was excluded by heredity;
  - stabilizer theory was excluded by no-restriction;
  - real QM was excluded by hSFP;
  - quaternionic QM is still open (chain `:94`).

  Every addition is labelled honestly. Together they mean quantum theory is reached **by construction of the filters**, not by the cost.
- **The forces and gravity rounds use quantum mechanics as input.** They use the TFIM and free-fermion states, Henderson–Vedral J(A|Ā) = S(A), the qubit Bloch records, and Bisognano–Wichmann. The Gibbs form is forced only given KL as the selection price (forces NOTE `:161`, `:244`, already relabelled after the G2 review).

**Status: OPEN MISS (structural).** No single step is fallacious. The *chain* has to carry a dependency graph showing which premises each "derived" item consumes.

---

## Top 5 risks to tonight's work, with fixes

1. **Circular entanglement derivation.** Highest risk.
   - **Where:** the entanglement thread, `rnd/entangle/`, and any use of the round-10 conditional remark or of Masanes et al. 2014.
   - **Risk:** entanglement, or entangling dynamics, appears as a premise upstream of U and again as a conclusion downstream.
   - **Fix and check:** before any "entanglement derived" line is folded, write the premise graph: a list of nodes such as CD, U, transitivity, no-restriction, existence of interaction I, local tomography and Conjecture C, with an edge for each use. Check mechanically that I is not an ancestor of the conclusion. Otherwise label the result "form of entanglement derived *given* that some interaction exists".

2. **Premise accretion that selects quantum theory by filter.**
   - **Where:** rounds 8–12 and the M11 extension.
   - **Fix and check:** freeze the premise list now in a short dated prereg, before more results. Then run the counterexample search that round 9 named (`rnd/selfref/NOTE.md:691`: other compact groups, e.g. U(2) and Sp(1)×Sp(1) transitive bodies in dimensions 4–8) under the **frozen** list. Any later premise must be logged as a deviation, together with the counterexample that prompted it.

3. **SFP depends on the choice of group, and SFP implies U.**
   - **Where:** Lean round 3 (the maximal-torus SFP criterion), round 9, and the Solèr branch.
   - **Fix and check:**
     - State once which maps count as reversible: the identity component, or the maps that extend to composites (CP). Apply that rule to polytopes and balls alike.
     - Add a Lean control `¬ SFP (O(3)) (sphere 3)` via −I, and a transitivity hypothesis on any SFP "selection" corollary.
     - In the notes, state "SFP + transitivity ⇒ U" (Jordan) so that SFP is never presented as independent of U.
     - Apply the two wording fixes under (c).

4. **Scope creep in the M11 extension.**
   - **Where:** round 12, ledger RC13–RC16, and any claim about "Conjecture C".
   - **Fix and check:**
     - Keep the wording "C proved for (★) parts with absolutely irreducible transitive groups in locally symmetric composites, and for regular-polygon pairs under (♦)". State that M11 adds nothing over Al-Safi–Richens Thm 1 for max products.
     - Correct `NOTE.md:1096` (octagon) and `:1320-1323` (slice versus full max).
     - Finish an exact enumeration (lrs) for I×I and D×D, and do a direct automorphism search on I×D, where (♦) fails.
     - Test at least one non-locally-symmetric composite family exhaustively, and one tripartite case.

5. **The forces and gravity "forced" labels, and their QM inputs.**
   - **Where:** `rnd/forces-gravity/NOTE.md` G2 and G3.
   - **Fix and check:**
     - Every "forced" claim carries its "given" list (loss, KL, local reads, per-bond capacity price, QM state class).
     - Replace `NOTE.md:11` as worded under (a).
     - Treat all G-round numbers as exploratory, since nothing was preregistered (`WORKLOG.md` 01:03 and 01:04 entries). No G result is folded before its hostile review (FOR-34) and a fresh-clone rerun.
     - The area-scaling claim was already withdrawn (`NOTE.md:233`). Do not let it come back without a 2D test locked in advance.

## Must fix before tonight's results can be trusted

1. **Circularity guard** (risk 1): write the premise graph, and check that the interaction premise does not feed its own derivation.
2. **SFP group rule** (risk 3): state it once and add the O(3) control. Without it, SFP-based selection is under-specified.
3. **Wording fixes:**
   - rounds 4–9 `:62` ("without a time-evolution premise");
   - round 10 `:61` (Solèr branch "PROVED" despite the cheapest-bit hypothesis);
   - live PR body line 50 ("at any finite horizon" is still there, although `cfa97cd` relabelled the note);
   - PR body line 1 ("Nothing was rebased");
   - `forces-gravity/NOTE.md:11`.
4. **Prereg hygiene:**
   - commit `gate_read_290.md` and the #292 gate reads into the repo;
   - append a #292 DEVIATIONS line for the `PREREG_5.md:3` breach;
   - make the #286 lock commit `f18721fc` reachable (or disclose it in the PR body).

**What is solid and can be relied on:**
- Lemma B1, S1, S2 (under NA2), the polygon bound (under NA3), Jordan's derangement theorem, P1 additivity, and the finite-geometry algebra.
- Theorem M11 within its class.
- The C1 counterexample.
- The clean misses in #292.
- The honesty of the chain note's scope sentence (`RECORD_COST_CHAIN_2026-11-25.md:13`).

*Sources cited with DOIs were checked on the Crossref API today (about 01:15 ET): `10.1088/1367-2630/16/12/123029`, `10.1088/1367-2630/17/12/123001`, `10.1090/S0002-9904-1946-08506-7`, `10.1063/1.4903510`; also checked, not cited above: `10.1080/00927879508825218`, `10.1103/PhysRevA.84.012311`, `10.1088/1367-2630/13/6/063001`. Jordan, von Neumann and Wigner 1934 are cited as in round 10 `:111`. Scratch Lean outputs: `/workspace/lean-audit-295/build.log` and `/workspace/lean-audit-295/rndaxioms.out`.*
