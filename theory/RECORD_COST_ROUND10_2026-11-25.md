# Record cost, round 10: what "tracking never finishes" can come from

*Wednesday 25 November 2026 (America/New_York). Side R&D, a follow-up to `theory/RECORD_COST_ROUNDS4-9_2026-11-25.md` (the "rounds 4–9 note"), consolidated from a private session. Status words are those at `CORE.md:169`. `THEORY.md`, `CORE.md`, locked blobs and committed preregs are unchanged. Scripts and outputs: `theory/record-cost-2026-11-25/scripts/selfref/m_round10` and `n_round10b`. Citations were checked on Crossref (`doi_check_3.out`, `doi_check_3b.out`). Nothing here derives quantum theory, general relativity, holography, or gravity.*

Labels as in the rounds 4–9 note: **PROVED (in-model)**, **OBSERVED (numerical)**, **KNOWN**, **HYPOTHESIS**, **OPEN** and **open miss**. U is the premise "tracking never finishes": the reversible group of a record's state space is infinite (rounds 4–9 note, §2). The question here is whether U follows from something more basic.

## 1. Result in one paragraph

U is not derived. It follows from continuous time with change (which is the drift premise CD again), from purification (a stronger premise), or from the quantum-logic premises of irreducibility with the covering property and capacity at least 3. It does not follow from composition with local tomography, from a Lawvere-style self-reference argument, from priced inflow with finite capacity, from a no-small-subgroups condition, or from the cost J, which prefers finite groups. Every route that works rests on connectedness of the reversible group or on irreducibility with the covering property (superposition of records). Neither follows from the record-cost premises without drift.

## 2. Composition does not force U

- **PROVED (in-model) by counterexample.** Classical probability theory is locally tomographic and transitive with the finite group Sₙ (KNOWN). Two-qubit stabilizer theory, with stabilizer states and Pauli effects, adds entanglement and interacting reversible maps with finite groups. OBSERVED (numerical) (`m_round10.stdout`): Clifford groups of order 24 and 11520 (mod phase), transitive on 6 and 60 pure states. There are 24 entangled pure states, local Pauli products span all 16 dimensions, and CNOT|+0⟩ has marginal purity 0.5. These are KNOWN facts (Aaronson and Gottesman 2004).
- This is why Hardy and Masanes–Müller state a continuity or continuous-reversibility requirement: classical theory meets their other requirements (KNOWN; Masanes and Müller 2011).
- The stabilizer bit fails the fixed-pure-state condition SFP: 14 of 24 Clifford elements fix no stabilizer state, and 6784 of 11520 for two qubits. This is consistent with Jordan's theorem (rounds 4–9 note, §5).

## 3. Continuous time with change gives U, but it is the drift premise again

PROVED (in-model) (`ContinuousTime.lean`). A finite group with a T1 topology admits no non-trivial continuous one-parameter motion. So non-trivial continuous-time change forces an infinite reversible group. Polytopes have finite reversible groups (KNOWN). The chain note's S3 already has this in substance (`discrete_oneParam_trivial`). The premise "time is a continuum and something changes" is CD without the word "unknown", so it is not more basic.

## 4. Self-reference in Lawvere's form does not give U

Lawvere's fixed-point theorem (KNOWN; Lawvere 1969; Yanofsky 2003) says that a point-surjective map A → Y^A forces every endomap of Y to have a fixed point.
- Take Y to be the pure states and the endomaps to be the reversible maps. Then Lawvere would yield SFP. But its hypothesis is complete self-description, which the self-reference bound A0 forbids. For finite transitive groups the contrapositive is A0 again, since Jordan's theorem supplies a map with no fixed point.
- Take Y to be the whole convex state space. Then every affine endomap has a fixed point (Brouwer) in every geometry, so nothing is separated.

**open miss.**

## 5. Priced inflow with finite capacity gives only a global infinite order

PROVED (in-model) (`never_returns_infinite_order`). If an orbit never returns, the global reversible map has infinite order. Parts can still keep finite groups: the rounds 4–9 note's reversible cellular automaton has capacity-2 cells. The missing step is from the global map to the reversible group of a part. **open miss.**

## 6. The cost J does not prefer continuous groups

Zero drift favours the classical bit (2.00 against the ball's 2.16). An unknown update favours polytopes (rounds 4–9 note, §6). A further finite rival is the octahedron with all non-negative effects. It has capacity 2 at affine dimension 3, the same as the ball (OBSERVED (numerical), linear program, `m_round10.stdout`). It is excluded by CD and by SFP, not by cost.

## 7. Purification gives U, but it is a stronger premise

PROVED (in-model) from KNOWN steps:
1. Purification of every state is impossible in a theory whose state spaces are polytopes. Finitely many pure states cannot purify a segment of states (Winczewski et al. 2023, Theorem 7).
2. Uniqueness of purification makes the reversible group transitive on pure states (Chiribella, D'Ariano and Perinotti 2010, Lemma 20).
3. So a purifying system has infinitely many pure states under a transitive reversible group. Its closure is an infinite compact Lie group, which has positive dimension and contains a circle, so U holds there.

Circularity: Chiribella, D'Ariano and Perinotti (2011) reconstruct quantum theory with purification and no continuity axiom. This route trades U for a stronger premise.

## 8. Lattice theory

Read records as a lattice:
- sharp records are atoms;
- the join of two records is the smallest record face that contains both;
- the orthocomplement means "perfectly distinguishable from".

Copyable (drift-fixed) records are mutually compatible, so they lie in one Boolean block. Classical theory is a Boolean lattice, which is reducible.

- **Finite-geometry step, PROVED (in-model) from KNOWN theorems.** An irreducible, atomistic, orthocomplemented lattice with the covering property and at least three mutually orthogonal atoms has infinitely many atoms.
  - Rank at least 4: Piron's representation theorem (also Maeda and Maeda 1970) gives a *-division ring D with an anisotropic Hermitian form. A finite division ring is a field (Wedderburn 1905). Every form in three or more variables over a finite field has a non-zero zero (Chevalley 1935). So D is infinite.
  - Rank 3: an orthocomplementation of a projective plane is a polarity with no absolute point, and finite planes have none (Baer 1946).
  - OBSERVED (numerical) (`n_round10b.stdout`): every polarity of PG(2,q) for q = 2, 3, 4 has an absolute point (28, 468 and 3864 polarity matrices, none without). Every diagonal ternary form over GF(3), GF(5) and GF(7) has a non-zero zero.
  - With the transitivity premise already in use, the reversible group is infinite.
- **The covering property is load-bearing.** Two-qubit stabilizer theory has a third pure state inside a bit face (6 stabilizer states in span{|00⟩, |11⟩}) yet only finitely many pure states. Its lattice of stabilizer codes fails the covering property: for 1320 of 1770 pairs of distinct stabilizer states no Pauli fixes both, so their join is the whole space (OBSERVED (numerical)).
- **Solèr.** Suppose one system has an infinite family of mutually orthogonal records of equal norm. Solèr's theorem (Solèr 1995; Holland 1995, KNOWN) then gives a real, complex or quaternionic Hilbert space, whose unitary group is continuous, so U holds. Heredity of SFP over finite faces and the cheapest bit then leave the complex case, as in the rounds 4–9 note. That is PROVED (in-model) given Solèr and those results. SFP itself fails in infinite dimension, because the bilateral shift has no eigenvector, so only the hereditary form on finite faces is usable.
- **open miss.** Finite capacity with unbounded time does not give Solèr's hypothesis, because records made over time do not coexist as one orthogonal family. An infinite world of classical cells has infinite capacity but a reducible lattice.
- **Frontier.** U follows from irreducibility with the covering property and capacity at least 3. This is the standard quantum-logic route (Piron; Solèr). What is new here is only the mapping to the record-cost premises. The finite-geometry obstruction needs just a third record in every bit face, not a continuum. In the chain note, drift is what forced that third record. Without drift, irreducibility and the covering property are premises.

## 9. Hilbert's fifth problem and other fields

- **Hilbert's fifth problem.**
  - Reversible groups of finite-dimensional state spaces are closed subgroups of GL(n, ℝ), hence Lie groups (Cartan, KNOWN). Gleason (1952), Montgomery and Zippin (1952) and Yamabe (1953) add nothing in finite dimension.
  - Finite groups are Lie groups of dimension 0 and have no small subgroups, so that condition plus non-triviality never excludes them.
  - Reading the condition as "no arbitrarily cheap distinctions" points the other way. In the octahedral group every non-identity element g has ‖g − 1‖ ≥ 1.414, while a connected group has elements with ‖g − 1‖ = 10⁻⁶ (OBSERVED (numerical)).
  - What forces positive dimension is connectedness, which is the continuity axiom again.
- **Ranked by expected information value:**
  1. The finite-geometry and lattice route of §8 (high).
  2. Jordan, von Neumann and Wigner (1934) with Koecher–Vinberg (medium). The classical orthant is homogeneous and self-dual with a finite pure-state group, so U follows only for simple algebras of rank at least 2, which is the same irreducibility crux.
  3. Topos approaches (Döring and Isham 2008; Heunen, Landsman and Spitters 2009) (low). They start from operator algebras, and contextuality already occurs in finite stabilizer structures.
  4. Gleason (1957) (low). It presupposes a Hilbert space.
  5. Hilbert's fifth problem (low).
  6. o-minimality (low). Definable groups are Lie (Pillay 1988), and finite groups are definable.

## 10. Open misses added by round 10

1. **open miss.** U is not derived from composition, Lawvere-style self-reference, priced inflow with finite capacity, a no-small-subgroups condition, or the cost J (§2, §4–§6, §9).
2. **open miss.** The routes that do give U rest on connectedness (§3, §9) or on purification, or on irreducibility with the covering property (§7, §8). None of these is derived from the record-cost premises without drift.
3. **OPEN.** Whether "a part of a pure closed world is in a mixed state", read from the self-reference bound, can supply purification or irreducibility. Classical closed worlds have pure parts, so this reading is a premise, not a consequence.

## 11. Lean

`formal/lean/GTAO/Rnd/SelfRef/ContinuousTime.lean`, namespace `GTAORnd.SelfRef.R10`, contains 4 theorems; `scripts/RndAxioms.lean` lists them.

| Theorem | Statement | Label |
|---|---|---|
| `continuous_line_discrete_const` | a continuous map from ℝ to a discrete space is constant | **Faithful.** |
| `finite_group_no_continuous_motion` | in a finite group with a T1 topology, a continuous family from the identity stays at the identity | **Faithful.** |
| `continuous_change_infinite_group` | non-trivial continuous change forces an infinite group | **Faithful.** |
| `never_returns_infinite_order` | an orbit that never returns forces infinite order | **Faithful.** |

Not formalized: the finiteness of polytope reversible groups, the stabilizer counts, Piron's and Solèr's theorems, Baer's theorem, Chevalley–Warning, and the purification steps. Lean round 3 (26 November 2026; labels in `formal/lean/README.md`): `FiniteGeometry.lean` proves the algebra after Piron for §8 (a finite division ring is commutative; diagonal quadratic forms in three or more variables, and two-variable norm forms, over finite fields have a non-zero zero, from Mathlib's Chevalley–Warning), and `Transport.lean` proves the §14 comparison at T = 3 (a 7-gon path costs at most 3·(sin(π/7)/sin(3π/7))² < 0.67, while every 3-tick pure-state path in the disk costs at least 3/4). Piron's, Solèr's and Baer's theorems, the other horizons and the purification steps stay not formalized. `Modular.lean` adds the finite-height step for §8: a finite upper semimodular lattice with an orthocomplementation is modular, hence orthomodular, which is the hypothesis Piron's theorem needs; an atomistic lattice with finitely many atoms is finite. It also proves that atomistic plus covering gives upper semimodular; that orthocomplement means "perfectly distinguishable from" on the face lattice stays a premise.

## 12. Sources (Crossref-checked)

- Aaronson, Gottesman 2004, PRA 70:052328, `10.1103/PhysRevA.70.052328`
- Baer 1946, Bull. AMS 52:77–93, `10.1090/S0002-9904-1946-08506-7`
- Chevalley 1935, Abh. Math. Sem. Hamburg 11:73–75, `10.1007/BF02940714`
- Chiribella, D'Ariano, Perinotti 2010, PRA 81:062348, `10.1103/PhysRevA.81.062348`
- Chiribella, D'Ariano, Perinotti 2011, PRA 84:012311, `10.1103/PhysRevA.84.012311`
- Döring, Isham 2008, J. Math. Phys. 49, `10.1063/1.2883740`
- Gleason 1952, Ann. Math. 56:193, `10.2307/1969795`
- Gleason 1957, Indiana Univ. Math. J. 6:885–893, `10.1512/iumj.1957.6.56050`
- Heunen, Landsman, Spitters 2009, CMP 291:63–110, `10.1007/s00220-009-0865-6`
- Holland 1995, Bull. AMS 32:205–234, `10.1090/S0273-0979-1995-00593-8`
- Jordan, von Neumann, Wigner 1934, Ann. Math. 35:29, `10.2307/1968117`
- Lawvere 1969, Lecture Notes in Mathematics, pp. 134–145, `10.1007/BFb0080769`
- Maeda, Maeda 1970, Theory of Symmetric Lattices, ch. "Orthomodular Symmetric Lattices", `10.1007/978-3-642-46248-1_8`
- Masanes, Müller 2011, NJP 13:063001, `10.1088/1367-2630/13/6/063001`
- Montgomery, Zippin 1952, Ann. Math. 56:213, `10.2307/1969796`
- Pillay 1988, J. Pure Appl. Algebra 53:239–255, `10.1016/0022-4049(88)90125-9`
- Solèr 1995, Comm. Algebra 23:219–243, `10.1080/00927879508825218`
- Maclagan-Wedderburn 1905, Trans. AMS 6:349–352, `10.1090/s0002-9947-1905-1500717-7`
- Winczewski et al. 2023, Quantum 7:1159, `10.22331/q-2023-11-03-1159`
- Yamabe 1953, Ann. Math. 58:351, `10.2307/1969792`
- Yanofsky 2003, Bull. Symbolic Logic 9:362–386, `10.2178/bsl/1058448677`

Piron's representation theorem (1964) is cited by name; no DOI was checked for it.

## 13. Reproduce

From `theory/record-cost-2026-11-25/scripts/selfref/`, run `python3 m_round10.py` (2 s) and `python3 n_round10b.py` (30 s; numpy, scipy). The outputs are the `.stdout` files beside them.

## 14. Part M: priced inflow, composition and the cost J (folded in from a parallel worker)

A second worker ran these three routes in parallel. Its results refine §2, §5 and §6 above, which are left as written. Scripts: `scripts/selfref/m_round10b.py` and `m_round10b_poly.py`, with `.stdout` files beside them; the repository copies print only. Citations: `doi_check_3m.out` (17 DOIs). Hardy 2001 is cited by arXiv identifier (`quant-ph/0101012`).

**Priced inflow with finite capacity.**
- *Closed world.* In a finite-dimensional closed world the reversible group is a compact Lie group (Cartan, KNOWN). An evolution that never returns has infinite order, so the closure of the group it generates has positive dimension and contains a circle (PROVED (in-model) from KNOWN). In a finite closed world, "never returns" is therefore equivalent to a continuous symmetry. That is U restated, not derived.
- *Unbounded environment.* An infinite world of capacity-2 cells under the shift, started in a Thue–Morse configuration, feeds cell 0 an aperiodic stream forever. Every finite block keeps a finite group (PROVED (in-model) by construction; no period up to 1024, OBSERVED (numerical)). Compactness fails only because the environment is unbounded; this is the missing local-from-global step of §5.
- *Pricing inflow is geometry-blind.* Swapping an old record out is reversible and free in both worlds. Overwriting it costs the Landauer amount, which is the same for a classical bit and a qubit holding the same record. The memory for the reversible map favours the finite group: log₂ 24 ≈ 4.6 bits for the octahedral group, against roughly 3·log₂(1/ε) bits for SO(3) (OBSERVED (numerical)).
- *Inheritance.* A part that records a connected environment group covariantly and faithfully inherits a non-trivial connected group (PROVED (in-model)). Inflow passes U on from an environment that already has it; it does not create it. **open miss.**

**Composition.**
- *Stabilizer theory meets both composite rules with finite groups.* Records of composites are costed like records of parts under Hardy's rules K_AB = K_A·K_B and N_AB = N_A·N_B. Stabilizer theory meets both for n = 1, 2, 3 with finite groups: 6, 60 and 1080 pure states; affine dimensions 3, 15 and 63; capacities 2, 4 and 8 (OBSERVED (numerical); KNOWN, Aaronson and Gottesman 2004).
- *Cheapest cost then picks classical.* Hardy's own abstract says that dropping the word "continuous" leaves classical probability theory (KNOWN). **open miss.**
- *No-restriction excludes stabilizer entanglement.* If the octahedron is given all its effects, the Bell stabilizer state gives the value −0.5 on a product effect, so that state is not allowed (PROVED (in-model)).
- *Known results on no-restriction polytope parts.* With maximally non-local composites, reversible dynamics are trivial for boxworld (Gross et al. 2010; Al-Safi and Short 2014) and for most regular polytopes (Al-Safi and Richens 2015, KNOWN).

**The cost J.**
- *Finite tasks.* Every single-shot task with finitely many preparations and reads is matched by a polytope of no larger affine dimension (PROVED (in-model)).
- *Gentle transport.* The task is to move a record to a perfectly distinguishable partner over T ticks, at a cost of c·d² per tick plus κ per affine dimension. Results:
  - An even polygon never beats the disk, and the 4T-gon ties it (PROVED (in-model)).
  - Odd polygons beat it (OBSERVED (numerical)). At T = 3 the 7-gon costs 0.594 against the disk's 0.750; at T = 4 the 9-gon costs 0.483 against 0.586.
- So J does not select a continuous group at the tested horizons: an odd polygon is strictly cheaper than the disk at T = 3, 4, 5 and 8 (`m_round10b_poly.stdout`), and the (2T+1)-gon is at every T from 2 to 12 and at T = 16 and 20, with a tie at T = 1 (`m_round10b_poly_ext.stdout`, added at review; OBSERVED (numerical)). That this holds at every finite horizon is a HYPOTHESIS. The disk wins only if one design must serve every horizon, which is U again. With a linear price c·d the ranking reverses toward the classical jump. **open miss.**

**Counterexamples recorded here:**
- the Thue–Morse shift world;
- stabilizer theory up to 3 qubits;
- the 7-gon at T = 3.

**Conditional remark (HYPOTHESIS, not a claim).** U would follow from four premises together:
1. transitivity on the parts' pure states;
2. no-restriction;
3. one reversible map that entangles two parts;
4. Conjecture C: no-restriction polytope parts admit no reversible entangling map in any composite between the minimal and maximal tensor products. This extends the Al-Safi–Richens conjecture.

Conjecture C is being tested separately; its result will be added here when it is available. Two of these premises, no-restriction and entangling dynamics, are not yet in the record-cost chain.

**Not formalized:** the compact-closure step, the Thue–Morse construction, the stabilizer counts, the polytope reduction and the transport costs. Lean round 3 (26 November 2026): `formal/lean/GTAO/Rnd/SelfRef/Transport.lean` proves the transport comparison at T = 3 only (7-gon path cost < 0.67 against at least 3/4 for every 3-tick pure-state path in the disk); the other horizons stay not formalized. Lean round 4 (appended): `TransportHorizons.lean` proves the disk side exactly at T = 2 (every 2-tick pure path costs 1) and T = 4 (at least 2 − √2 ≈ 0.586, attained by equal quarters); the polygon side at T = 4 and other horizons stay not formalized.

Sources added: Al-Safi, Short 2014, J. Phys. A 47:325303, `10.1088/1751-8113/47/32/325303`; Al-Safi, Richens 2015, NJP 17:123001, `10.1088/1367-2630/17/12/123001`; Barnum, Wilce 2014, Found. Phys. 44:192–212, `10.1007/s10701-014-9777-1`; Crooks 2007, PRL 99:100602, `10.1103/PhysRevLett.99.100602`; de la Torre, Masanes, Short, Müller 2012, PRL 109:090403, `10.1103/PhysRevLett.109.090403`; Gross, Müller, Colbeck, Dahlsten 2010, PRL 104:080402, `10.1103/PhysRevLett.104.080402`; Krumm, Müller 2019, npj Quantum Inf. 5:7, `10.1038/s41534-018-0123-x`; Landauer 1961, `10.1147/rd.53.0183`; Masanes et al. 2013, PNAS, `10.1073/pnas.1304884110`; Massar, Patra 2014, PRA 89:052124, `10.1103/PhysRevA.89.052124`; Salamon, Berry 1983, PRL 51:1127, `10.1103/PhysRevLett.51.1127`.

## 15. Conjecture C: result of the separate test (round 11, part M; fills the placeholder in §14)

The test promised at the end of §14 has run; §14 is left as written. Scripts: `scripts/selfref/m_round11_lib.py` and `m_round11.py`, `m_round11_sym.py`, `m_round11_more.py`, `m_round11_lemma.py`, `m_round11_control.py`, `m_round11_pyramid.py`, with `.stdout` files beside them (the repository copies print only; the symmetric-composite copy runs the one octahedron × octahedron sample that the session run completed). Citations: `doi_check_4m.out` (6 DOIs). Extra tools needed: `lrs` and `redund` from lrslib (exact rational vertex enumeration), plus numpy, sympy and networkx; `tools/test_conjecture_c_checks.py` skips cleanly without them.

**Result in one paragraph.** No counterexample to Conjecture C was found in any composite tested, and a positive control shows the test can find an entangling map when one exists. For one class of parts, Theorem M11 below proves C in every composite that keeps the parts' own reversible maps reversible (PROVED (in-model)). This is a partial result on composites between the minimal and maximal tensor products. It is not a derivation of U or of quantum theory: C is still open for other polytopes, and the premise that a reversible entangling map exists is not derived.

**Method (exact).** States are w = (1, r) per part and Kronecker vectors for composites. The maximal composite is vertex-enumerated with `lrs`; an intermediate composite is conv(min ∪ X) with X inside max, and its extreme points come from `redund`. Every polyhedral composite between min and max has this form. Linear automorphisms of a polytope are exactly the vertex permutations that preserve K_ij = v_iᵀ(Σ_k v_k v_kᵀ)⁻¹v_j (KNOWN; Bremner et al. 2014), computed here in exact integers. Colour refinement on K gives classes that every automorphism preserves. When no entangled extreme point shares a class with a product pure state, no entangling automorphism exists: an exact certificate for that composite. Otherwise a backtracking search runs, and any map found is rebuilt as an exact linear map.

**What was tested** (△ triangle, □ square, O octahedron, each with all its effects; the hexagon is affinely regular with rational vertices):

| composites | parts | count | outcome |
|---|---|---|---|
| maximal | △△, △□, △O, □□ (24 vertices), □O (48), OO (684) | 6 | simplex cases have no entangled states; the others are certified: no entangling map |
| minimal | the same pairs | 6 | no entangled extreme points |
| min with every subset of the 8 PR boxes | □□ | 255 | certified |
| min with noisy PR boxes (λ from 3/5 to 9/10) | □□ | 12 | certified |
| min with refinement classes of max vertices, also noisy | □O, OO | 9 | certified, or no entangled points left |
| random mixtures of max vertices with noise | □O (40), OO (25) | 65 | certified, or no entangled points left |
| locally symmetric: orbit of a random max point under both parts' groups and the swap | □□ (12), □O (10), OO (1) | 23 | certified, or no entangled points left |
| maximal, more parts | hexagon², □ × hexagon, hexagon × O (1740), □ × cube, cube × O, cube² (1408) | 6 | certified |
| maximal, a reducible part (the square pyramid of Al-Safi and Richens) | pyramid × □, pyramid², pyramid × O | 3 | certified |
| **positive control:** two-qubit stabilizer polytope (octahedron parts with restricted reads, not inside max) | O, O | 1 | an entangling automorphism is found and rebuilt as an exact linear map |

All OBSERVED (numerical) as a search, and each "certified" row is an exact certificate for that composite (PROVED (in-model)). The simplex sanity case behaves as Al-Safi and Richens describe: on △ × △ the controlled shift (i, j) ↦ (i, j + i) is an exact linear automorphism, non-local and correlating, with no entangled states to create. Coverage limits: non-symmetric intermediate composites are sampled, not exhausted; non-polyhedral composites are not tested numerically; only two parts are tested.

**Theorem M11 (PROVED (in-model), pen and paper; both lemmas checked exactly on the vertices of six maximal composites).**
- *Parts.* A and B have all consistent reads, and their state spaces are centrally symmetric polytopes with centre 0. Each part's reversible group acts transitively on vertices and absolutely irreducibly on r-space (dimension m). Vertices lie at radius R, and facets are n·r ≤ 1 with |n| the same for every facet.
- *Condition (★).* R²|n|² = m. Equivalently, every vertex lies on one facet of every opposite pair (|n·v| = 1 for every facet normal n and vertex v).
- *Composite.* S is any composite with min ⊆ S ⊆ max, polyhedral or not, that is invariant under both parts' groups, so local reversible maps stay reversible.
- *Conclusion.* Every reversible map of S sends product pure states to product pure states, so S has no reversible entangling map.
- *Proof.*
  1. Write w = (1, a, b, C): the two marginals and the correlation matrix.
  2. The minimum-volume ellipsoid containing S is unique (KNOWN; John 1948). A reversible map is affine on the normalized slice and maps S onto S, so it preserves that ellipsoid and its quadratic gauge q.
  3. Invariance under both groups puts the ellipsoid's centre at (1, 0, 0, 0). Schur's lemma on the three inequivalent absolutely irreducible blocks then gives q = |a|²/β + |b|²/γ + ‖C‖²_F/δ with β, γ, δ > 0.
  4. **Lemma 1:** ‖C‖_F ≤ R_A R_B on all of max. Positivity on the four products of the facet effects (1 ± n·r)/2 and (1 ± m·s)/2 gives |nᵀCm| ≤ 1. Averaging over the facet normals, whose second moment is (|n|²/m)·I by irreducibility, gives ‖C‖²_F ≤ m_A m_B / (|n_A|²|n_B|²), which equals R_A²R_B² by (★).
  5. **Lemma 2:** a state in max with a pure marginal is a product, because the conditional states of a pure marginal must all be proportional to it. So an entangled extreme point has two non-pure marginals, and |a| < R_A, |b| < R_B (non-vertex points of an inscribed polytope lie strictly inside the sphere).
  6. A product of pure states has |a| = R_A, |b| = R_B and ‖C‖ = R_A R_B, so its q is strictly larger than that of any entangled extreme point. A reversible map preserves q, which completes the proof.
- *Exact checks.* Lemma 1 is tight: the largest ‖C‖²_F over max-composite vertices equals R_A²R_B² for □□, □O, OO, □ × cube, cube × O and cube² (4, 2, 1, 6, 3, 9). Lemma 2: no entangled max vertex has a pure marginal (0 in all six).
- *Which parts meet (★).* Hypercubes (boxworld bits with m binary measurements, including □ and the cube) and cross-polytopes (including O), in every dimension. Polygons with six or more sides, the icosahedron, the dodecahedron and the 24-cell fail it. So do balls (|n| = 1 = R, m = 3; the singlet has ‖C‖² = 3 > 1), which is where quantum theory leaves the theorem, and the stabilizer polytope, which is not inside max (§14: the Bell state gives −0.5).

**Comparison with Al-Safi and Richens 2015 (full text read).** Their Theorem 1 makes every reversible map trivial (local maps and swaps) in the maximal composite of non-classical dichotomic parts, which include balls and every regular polytope except simplices and odd polygons; their Theorem 3 covers identical odd polygons; their Theorem 2 gives non-trivial, correlating but not entangling, maps when one part is reducible. Their Conjecture 2 says no maximally non-local composite allows reversible entanglement generation, for any parts, and they name composites other than the maximal one as an open obstacle. Conjecture C is narrower in its parts (polytopes only) and broader in its composites (everything between min and max), so it is neither weaker nor stronger. On maximal composites of polytopes it is the polytope case of their Conjecture 2. Theorem M11 is a case between min and max with a weaker conclusion than their "trivial".

**What this does for U.** With transitivity, all reads allowed, a locally symmetric composite and one reversible entangling map, the parts cannot be hypercubes or cross-polytopes (PROVED (in-model)). Excluding every transitive polytope needs C for the parts that fail (★). The premise that a reversible entangling map exists is not derived from the record-cost chain. U stays an **open miss**.

**open miss (what C still lacks):** parts that fail (★) (polygons with six or more sides, odd polygons, the icosahedron and dodecahedron, non-regular vertex-transitive polytopes such as prisms); composites that are not invariant under the parts' groups (sampled only); three or more parts; and the entangling-map premise.

**Not formalized:** Theorem M11, its two lemmas and the certificates. Two Lean candidates are written up in the session notes: the square case of Lemma 1 and a finite form of Lemma 2. Lean round 3 (26 November 2026; labels in `formal/lean/README.md`): `formal/lean/GTAO/Rnd/SelfRef/Composite.lean` proves both candidates (PROVED (in-model)): Lemma 1 for hypercube parts (`cube_corr_bound`, `square_corr_bound`, `square_C_bound`, tight by `cube_corr_tight`) and Lemma 2 in a finite form (`square_pure_marginal`, `pure_marginal_finite`) plus an abstract form that takes the conditional-state property of the max composite as a hypothesis (`pure_marginal_product`, `pure_marginal_factorizes`). Theorem M11 itself, Lemma 1 for other parts and the certificates stay not formalized. `M11Prime.lean` proves the Lean-able steps of M11 with the hypotheses made explicit by a later hostile review (vertex-transitive, absolutely irreducible, 2-level parts; a locally symmetric composite between min and max): 2-level iff R²s = m, Lemma 1 in general finite form, the strictness step, averaging over a finite group in place of the Löwner ellipsoid for polytopes, and the final step. Of the Schur block step, only the scalar blocks (commutant = scalars as the hypothesis) and the vanishing of cross terms under -1 are formalized; the tensor-product block is not. Lean round 4: `M11Cube.lean` assembles M11′ for hypercube parts and for cross-polytope parts (`m11_cube`, `m11_cross`, PROVED (in-model); the finite symmetry group is a hypothesis); other parts stay not formalized. Hostile review of Lean round 3 (appended): `final_assembly` is an elementary set lemma; it takes as hypotheses the invariance of q under every reversible map and the strict separation of product pure states (the core of M11′), and the `M11Prime.lean` steps are not chained. Deriving the separation needs the tensor-product Schur block, which `M11Cube.lean` supplies for hypercube and cross-polytope parts only; for other parts no Lean theorem states M11′.

Sources added: Bremner, Dutour Sikirić, Pasechnik, Rehn, Schürmann 2014, LMS J. Comput. Math. 17:565–581, `10.1112/S1461157014000400`; Avis, Fukuda 1992, Discrete Comput. Geom. 8:295–313, `10.1007/BF02293050`; John, "Extremum problems with inequalities as subsidiary conditions" (1948), reprinted in *Traces and Emergence of Nonlinear Programming* (Birkhäuser; Crossref year 2013), 197–215, `10.1007/978-3-0348-0439-4_9`. Al-Safi and Richens 2015, Gross et al. 2010 and Al-Safi and Short 2014 are as in §14.

## 16. Conjecture C beyond (★): an orbit bound and all polygon pairs (round 12, part M)

§15 left open every part that fails (★). This section proves C for a wider class with a sharper, marginal-aware bound. Scripts and outputs: `theory/record-cost-2026-11-25/scripts/selfref/m_round12_*.py` with `.stdout` (vertex enumeration in floating point with pycddlib; LP searches with scipy). DOIs: `doi_check_5m.py` / `.out`.

**Why M11's proof stops (OBSERVED (numerical), with one exact example).** In the coordinates of §15 with R = 1, the largest ‖C‖²_F over entangled extreme points of max(P_n, P_n) is 1 + cos(2π/n) for n = 4 to 10 (1.309 for the pentagon, 1.5 for the hexagon, 1.809 for n = 10). So Lemma 1 is false for every polygon with five or more sides. Exact example: for the hexagon, a = b = 0, C = (3/4)·I lies in max and has ‖C‖² = 9/8.

**Theorem M12 (PROVED (in-model), pen and paper; checked numerically on the vertices of max for 17 part pairs).**
- *Parts.* A and B have all consistent reads. Each has a finite group of symmetries that is transitive on extreme points and absolutely irreducible on r-space (dimension m_A, m_B). Coordinates are invariant and Euclidean with extreme points at radius 1. Central symmetry is not assumed.
- *Composite.* S has min ⊆ S ⊆ max, is invariant under both parts' groups, and its reversible group has finite orbits (for example, S a polytope).
- *Condition (♦).* Φ(w) = m_A m_B (‖C‖² − 1) − m_A (1 − |a|²) − m_B (1 − |b|²) ≤ 0 at every entangled extreme point w of S. Products have Φ = 0.
- *Conclusion.* No reversible map of S sends a product pure state to an entangled state.
- *Proof.*
  1. Let T(p) = e with p a pure product state and e entangled. Let O be the orbit of p under the reversible group of S, with N points; it contains every pure product state (local transitivity) and E ≥ 1 entangled points. The products span the whole space (local tomography), so O does.
  2. Σ_O = Σ_{o∈O} o oᵀ is invariant under the reversible group, so h(o) = oᵀ Σ_O⁻¹ o is constant on O. Its sum over O is the trace of the identity, D = (1 + m_A)(1 + m_B), so h = D/N on O.
  3. O is invariant under both parts' groups, so Schur's lemma makes Σ_O block-scalar: N, (A_O/m_A)·I, (B_O/m_B)·I, (C_O/m_A m_B)·I, where A_O, B_O, C_O are the sums over O of |a|², |b|², ‖C‖².
  4. Evaluating h at a product gives m_A (1/A_O − 1/N) + m_B (1/B_O − 1/N) = m_A m_B (1/N − 1/C_O).
  5. Let u, v, t be the means over the entangled points of O of 1 − |a|², 1 − |b|², ‖C‖² − 1. Lemma 2 of §15 gives u, v > 0. The left side of step 4 is then strictly larger than (m_A u + m_B v)E/N². The right side is at most 0 if t ≤ 0 and strictly smaller than m_A m_B t E/N² if t > 0. Condition (♦), averaged, gives m_A m_B t ≤ m_A u + m_B v, so step 4 fails, which completes the proof.
- *Remarks.* Theorem M11 is the case ‖C‖ ≤ 1. Φ is convex, so (♦) holds on every S inside max as soon as it holds at the extreme points of max. Geometrically, (♦) says S lies inside the ellipsoid fixed by the second moment of the pure product states. For non-polyhedral S, the same argument with the invariant measure on the orbit is a sketch only.

**Disk lemma (PROVED (in-model), pen and paper; checked numerically).** If w = (1, a; b, C) lies in max(D, D), with D the unit disk, then ‖C‖² ≤ 2 + |b|² − 2|a|² and ‖C‖² ≤ 2 + |a|² − 2|b|². Adding them gives Φ ≤ 0 for m = 2.
- *Proof.*
  1. Write X = [[1, bᵀ], [a, C]] and J = diag(1, −1, −1). w lies in max exactly when X maps the 3-dimensional Lorentz cone into itself.
  2. By the S-lemma there is μ ≥ 0 with XᵀJX − μJ positive semidefinite. This is the Loewy–Schneider criterion (KNOWN).
  3. Evaluating that matrix at the first basis vector gives μ ≤ 1 − |a|². Taking its trace gives ‖C‖² ≤ 1 + |b|² − |a|² + μ.
  4. Combining the two gives the first inequality. Xᵀ satisfies the same condition, which gives the second.
- *Sharpness.* Equality holds at a rotation C with a = b = 0, which is a point of the disk composite and of no polygon composite. For balls of dimension m ≥ 3, the same steps leave room for Φ > 0; for example, the qubit singlet has Φ = 12.

**Corollary M12-P (PROVED (in-model)).** Take any two regular polygons P_n and P_m (n, m ≥ 3, odd or even, equal or not), inscribed in the unit circle. Then max(P_n, P_m) ⊆ max(D, D), so (♦) holds. Every locally symmetric composite between min and max with finite orbits therefore has no reversible entangling map. This covers odd polygons, which are not centrally symmetric.

Numerics (OBSERVED (numerical)):
- The largest Φ over entangled extreme points of max(P_n, P_n) is 4cos(2π/n) − 4 for n = 4 to 10.
- The mixed pairs P5×P6, □×P5, □×P6 and P3×P6 also have Φ < 0.
- Cube, octahedron and mixed products have Φ ≤ −4.875.
- Both one-sided disk inequalities hold on all vertices of max for 8 polygon pairs, with equality only at products.

KNOWN for comparison: for identical polygons and S = max, all reversible maps are trivial (Al-Safi and Richens 2015, Theorems 1 and 3), which is stronger. The cases of intermediate composites and of mixed polygon pairs are not in that paper or in Kolangatt et al. 2025 (Quantum, `10.22331/q-2025-01-20-1599`). This is "not found there", not a full literature search.

**Hanner polytopes and (★) (PROVED (in-model), a two-line induction).** For a centrally symmetric polytope, (★) in the form |n·v| = 1 says each vertex lies on one facet of every opposite pair ("centrally symmetric 2-level"). Hanner polytopes (Hanner 1956) are built from segments by products and polar duals, and both operations keep |n·v| = 1. So M11 also covers vertex-transitive Hanner polytopes whose group acts absolutely irreducibly, such as octahedron × octahedron, not only cubes and cross-polytopes.

**Parts in dimension 3 that fail (★) (OBSERVED (numerical), LP search, not exhaustive).**
- On the zero-marginal slice of max, the largest Φ found is −2.54 for icosahedron², −0.44 for dodecahedron² and −1.5 for cuboctahedron². So (♦) is not refuted there; it is not proved either.
- For icosahedron × dodecahedron the search finds Φ = +2.05 (a = b = 0, ‖C‖² = 1.894), so (♦) fails on that maximal composite and M12 says nothing about it. Al-Safi and Richens' Theorem 1 already makes that maximal composite's reversible maps trivial (KNOWN), so (♦) is sufficient for C but not necessary.

**The entangling-map premise, priced (PROVED (in-model), one direction only).** By M12, a locally symmetric composite with finite orbits can have a reversible entangling map only if it has an entangled extreme point with Φ > 0, that is, if it leaves the product ellipsoid. Quantum theory passes this test (the Bell state has Φ = 12). The converse is false: the maximal composite of two Bloch balls has Φ = 12 at C = I and only trivial reversible maps (Al-Safi and Richens Theorem 1, KNOWN). So the premise can be bounded this way but not replaced.

**open miss (what C still lacks after round 12):** parts in dimension 3 or more that fail (★) and (♦), such as balls, icosahedron × dodecahedron, and (unsettled) icosahedron², dodecahedron² and cuboctahedron²; composites that are not invariant under the parts' groups; three or more parts; a full write-up for non-polyhedral S; and the entangling-map premise itself. None of this derives tracking that never finishes or quantum theory; U stays an **open miss**.

**Not formalized:** M12, the disk lemma and the corollary. The two Lean candidates of §15 (the square case of Lemma 1 and a finite form of Lemma 2) are now written as precise statements in the session notes. The disk lemma is a third, heavier candidate, since it needs the S-lemma.

Sources added: Loewy, Schneider 1975, J. Math. Anal. Appl. 49:375–392, `10.1016/0022-247X(75)90186-9`; Pólik, Terlaky 2007, SIAM Rev. 49:371–418, `10.1137/S003614450444614X`; Hanner 1956, Math. Scand. 4, p. 65, `10.7146/math.scand.a-10456`; Kolangatt et al. 2025, Quantum 9:1599, `10.22331/q-2025-01-20-1599`.

## 17. Corrections to §15 and §16 after a hostile review (Theorem M11′)

A fresh-context hostile review of Theorem M11 (session file `HOSTILE_REVIEW_M11.md`) found no counterexample and no gap in the proof, but asked for explicit hypotheses, one wrong reason and one novelty claim to be corrected. This section supersedes the statement of Theorem M11 in §15; the earlier text is left as it was.

**Theorem M11′ (PROVED (in-model); the proof of §15 is unchanged, the hypotheses are now explicit).**
- *Parts.* A and B have all consistent effects (no restriction). Their normalized state spaces are centrally symmetric polytopes P_A ⊂ R^{m_A}, P_B ⊂ R^{m_B} centred at 0, with G_X = Aut(P_X) (linear). For X = A, B:
  1. G_X is transitive on the vertices of P_X.
  2. G_X acts absolutely irreducibly on R^{m_X}, in the representation-theoretic sense (one absolutely irreducible part suffices).
  3. (★): P_X is centrally symmetric 2-level, i.e. n·v ∈ {−1, +1} for every facet n·r ≤ 1 and every vertex v. Equivalently, in G_X-invariant Euclidean coordinates, R_X²|n_X|² = m_X.
- *Composite.* S is closed and convex in the normalized slice of V_A ⊗ V_B (local tomography), min(A,B) ⊆ S ⊆ max(A,B), and S is locally symmetric: (g⊗h)(S) = S for all g ∈ G_A, h ∈ G_B.
- *Conclusion.* Every linear bijection T with T(S) = S permutes the product pure states; S has no reversible entangling map.
- *Covered parts.* Hypercubes and cross-polytopes in every dimension, and at least octahedron × octahedron and cube ⊕ cube (free sum) in R^6 (checked exactly by the reviewer); more generally every vertex-transitive Hanner polytope with an absolutely irreducible group (§16).

**Scope (corrected).** For S = max the conclusion is already implied, in the stronger form "every reversible map is trivial", by Al-Safi and Richens 2015 Theorem 1: every centrally symmetric polytope with all effects is dichotomic, because u − e for a facet effect e is the opposite facet effect. So the sentence in §15 that leaves non-regular polytopes open on maximal composites is wrong for centrally symmetric ones, and M11′ is new only for intermediate (min ⊊ S ⊊ max) locally symmetric composites. The same applies to §16: for S = max with centrally symmetric parts (even polygons in any pairing, icosahedron × dodecahedron) the stronger "trivial" is KNOWN from Theorem 1, and for identical odd polygons from Theorem 3; Corollary M12-P is new for intermediate composites and for maximal composites with an odd polygon paired with a different polygon (as far as checked in those two theorems).

**Other corrections.**
- The reason a part fails (★) is "some |n·v| < 1" (equivalently R²|n|² < m), not "some n·v = 0": the latter is false for the octagon, the 12-gon, the icosahedron and the dodecahedron (it holds for polygons with n ≡ 2 mod 4 and the 24-cell). The exclusions in §15 stand.
- Uniqueness of the minimum-volume enclosing ellipsoid is due to Danzer, Laugwitz and Lenz 1957, Arch. Math. 8:214–219, `10.1007/BF01899996`; John 1948 does not state it explicitly. For polytope S the vertex second moment (finite Aut(S)) already gives an invariant form, so the ellipsoid is not needed.
- "Irreducible" has two meanings here. Al-Safi and Richens' "reducible" (their Theorem 2, the square pyramid in §15's table) is geometric: the cone is a direct sum. M11′ and M12 use representation-theoretic absolute irreducibility. They are unrelated conditions.
- M12 (§16) uses the same composite hypotheses as M11′: local tomography, S closed and convex, local symmetry.

**open miss (unchanged by the review):** parts that are not 2-level and fail (♦), composites that are not locally symmetric (the reviewer's involution ansatz found no entangling map for any entangled max vertex of □□, □O, OO, observed only), three or more parts, and the entangling-map premise.
