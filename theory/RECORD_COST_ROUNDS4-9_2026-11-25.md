# Record cost, rounds 4–9: can the change be derived, what selection costs, and a fixed-pure-state condition

*Wednesday 25 November 2026 (America/New_York). Side R&D, a follow-up to `theory/RECORD_COST_CHAIN_2026-11-25.md` (the "chain note"), consolidated from a private session. Status words are those at `CORE.md:169`. `THEORY.md`, `CORE.md`, locked blobs and the chain note's prereg are unchanged; the chain note only gains a pointer section at its end. Scripts and outputs are in `theory/record-cost-2026-11-25/scripts/selfref/` (files `g_round4` to `l_round9_check`). Citations were checked on Crossref (`theory/record-cost-2026-11-25/doi_check_2.out`). Nothing here derives quantum theory, general relativity, holography, or gravity.*

The hypothesis sentence is the one at `CORE.md:7`. Selecting state spaces by their cost applies that hypothesis by assumption. It is not tested here.

**Labels**, as in the chain note: **PROVED (in-model)**, **OBSERVED (numerical)**, **KNOWN**, **HYPOTHESIS**, **OPEN** and **open miss** (`CORE.md:169`). In this note, "update" means one reversible transformation of the state space applied per tick; "unknown update" means the tracker does not know which one.

## 1. What this adds, in one paragraph

The chain note assumes premise CD (continuous drift). Rounds 4–9 tried to derive the change instead, and to test whether selection, inflow, or a self-consistency condition can stand in for CD. Plainly: CD is not derived. Round 4 trades it for a premise of similar strength ("tracking never finishes"). Selection and inflow do not separate the geometries. A fixed-pure-state condition does separate them among continuous-group state spaces, but it needs an infinite reversible group, heredity over faces, and a cost step, and inside the Jordan class it lands where Barnum, Müller and Ududec's energy postulate already lands.

## 2. Round 4: "the world changes" from self-tracking

- **B1, PROVED (in-model).** Take a closed world that is one finite-dimensional state space with one reversible map per tick (discrete time allowed). If the state space is a polytope, every trajectory is periodic and the total information any internal tracker can extract is at most log₂ of the period, so at most log₂|Aut|. If some trajectory never repeats, the state space has infinitely many extreme points, the closure of the dynamics contains a torus that moves a state, and the copy ban S1 of the chain note applies. Continuous time and premise CD are not used.
- **Novelty equals destruction, PROVED (in-model).** In a stationary finite-state world, H(X₁|X₀) = H(X₀|X₁): learning at a positive rate destroys old information at the same rate, in every state space. OBSERVED (numerical): largest deviation 4.8e-15 over 2000 random chains (`g_round4.stdout`).
- **Reversible worlds learn without limit only at zero rate.** OBSERVED (numerical): a 64-state permutation world shows 7 distinct observation windows at every length; an irrational rotation shows 2L windows of length L (`g_round4.stdout`).
- **Reads are world changes.** In a closed reversible boxworld no reversible map writes a record (Gross, Müller, Colbeck, Dahlsten 2010, KNOWN; 0 of 128 symmetries, chain note's composition run). At zero outside change the remaining rival is the classical record, which still beats the ball (J = 2.00 against 2.16 at q = 4, from `f_selfdrift.stdout`).
- **open miss.** "Tracking never finishes" (call it U) is not derived from self-tracking. The self-reference bound (A0) says no part finishes; a finite world with a long cycle satisfies that. Infinite-extent reversible cellular automata learn one bit per tick with finite local symmetry. Under reversibility, U is close to "infinitely many pure states", the same family as Pfister and Wehner's non-discreteness and weaker than Hardy's continuity axiom.

## 3. Round 5: what selection costs, and the NA4 amendment

- **Selection cost, PROVED (in-model) for classical and quantum records.** The minimum destruction that raises a feature's share from its base rate p₀ in the invariant state to s is the binary relative entropy D(s‖p₀) (data processing on S(μ) − S(ω) = D(ω‖μ); equality attained). At s = 0.8 and p₀ = ½: classical bit, qubit, square and disk all 0.2781 bits; the square and disk rows use measurement entropy (`h_round5.stdout`). This is the far-from-equilibrium Landauer bound (Esposito and Van den Broeck 2011, KNOWN).
- **Long-run selection needs many-to-one dynamics.** Under reversible, measure-preserving dynamics no feature's long-run share grows (finite permutations PROVED (in-model); rotations KNOWN, Weyl 1916). OBSERVED (numerical): permutation share fixed at 0.7143, rotation at 0.2500, a contracting map's share rises to 0.9998 (`g_round4.stdout`).
- **Holding a share against unknown drift** costs h((1+cb)/2) − h(s) per tick, b = 2s − 1, set only by how much the drift contracts the bias c, equal across the worlds tested (PROVED (in-model)). Known drift costs nothing anywhere. Drift never lowers the cost of selection.
- **Closed finite worlds select only finitely often.** With reversible global dynamics, total selection is at most log K of the world minus its initial entropy, whatever the geometry (PROVED (in-model)). This is in tension with B1's closed-world premise.
- **Proposed amendment to NA4** (the chain note's §5 line is not edited; this text is offered for it): *NA4 (amended). "The disk pays 0" is a definition, and only for tracking. Σ = 0 for a deterministic invertible flow, so following a drift costs nothing. Selection, meaning any long-run growth in the share of a feature, needs a many-to-one map and costs at least D(s‖p₀) bits, plus h((1+cb)/2) − h(s) per tick to hold the share against unknown drift. That cost is the same for the disk, the polygons and classical records at a matched base rate, so it is a common term that does not change S3's ranking. In a closed finite world it can be paid only finitely often.* In short: "pays 0" means **pays 0 in tracking**.

## 4. Round 6: an open part with priced inflow

- **Frontier, PROVED (in-model) for classical and quantum records.** One reversible step on a part R and k inflow cells, with L the classical information about the inflow kept in R (Holevo quantity) and Δ the entropy drop of R: **L + Δ ≤ k·log₂N**, reached by a swap in both. OBSERVED (numerical): 4000 random unitaries, largest slack −0.378 (`i_round6.stdout`).
- **The square.** Over all 128 boxworld maps, L + Δ reaches 2.00 with measurement entropy and 1.47 with decomposition entropy, both above capacity (OBSERVED (numerical), `i_round6.stdout`). That is the known lack of a consistent entropy in these theories (Short and Wehner 2010; Barnum et al. 2010), linked to a violation of the second law by Hänggi and Wehner 2013; it is not a better frontier.
- **Caveat.** Counting quantum mutual information with an entangled reference gives the ball 2 per qubit; that correlation is not a copyable record, so it does not count under the record definition.
- **Prior art.** The setting is already known: L + Δ ≤ k is the information-ratchet bound with the tape budget split into a learning part and a selection part (Mandal and Jarzynski 2012; Boyd, Mandal and Crutchfield 2016; Barato and Seifert 2013, 2014; Deffner and Jarzynski 2013; quantum versions Deffner 2013, Chapman and Miyake 2015).
- **Result.** With Shannon or von Neumann entropy, selection and inflow do not separate the geometries; only drift does.

## 5. Rounds 7–8: deleting selection, relational time, and a fixed-pure-state condition

- **Deleting selection changes no ranking.** The zero-drift comparisons never used selection: classical 2.00, square 2.00 plus one destroyed bit once, ball 2.16. Static classical and square worlds were viable because nothing changes.
- **open miss: "no outside frame" does not force drift.** Zero drift is well defined relationally (the relative configuration of tracker and tracked is invariant). A closed two-bit classical world whose inside record is complete and then never changes is a counterexample. Page–Wootters relational time allows change but does not force it (a product clock-system state has none), and it has a classical analogue, so it does not pick a geometry.
- **SFP (HYPOTHESIS as a premise).** Every reversible transformation of the state space fixes at least one pure state. In quantum theory this is the spectral theorem for unitaries.
- **SFP criterion, PROVED (in-model) via KNOWN theorems** (the general criterion and the classification are not formalized; the Lean cases are listed in §10). For a compact connected group G transitive on pure states with stabilizer H, SFP holds iff H contains a maximal torus of G, iff the pure-state manifold has non-zero Euler characteristic (maximal torus theorem; Hopf and Samelson 1941). A transitive group on finitely many pure states always has an element that fixes none (Jordan; Serre 2003), so simplices and the square fail. Pass: complex quantum theory (all d), quaternionic (all d), octonionic d = 3, real quantum theory with odd d, balls of odd dimension with SO(n). Fail: the disk, balls of even dimension (any transitive group), real quantum theory with even d. OBSERVED (numerical) sampling agrees (`j_round7.stdout`, `k_round8.stdout`).
- **In affine dimension at most 3**, transitivity, at least two pure states and SFP leave the qubit ball with group SO(3), under the SO(3) subgroup classification (the chain note's NA1). No drift premise is used.
- **The "every update" premise is not derived from the self-reference step.** The order "one pattern fixed by every update consistent with finite records" leaves only the centre in any continuous transitive world (PROVED (in-model); OBSERVED (numerical): 0 of 1000 pairs of SO(3) rotations 1e-3 apart share a fixed pure state, `k_round8.stdout`). The self-reference bound limits a tracker's knowledge of its own state, not of a fixed update; a finite group's update can be learned exactly.
- **Cost motivation, only for infinite groups.** With the update known to precision δ, a ball record at the estimated axis stays within 2 sin δ for every number of steps, while the disk's compensated record error after t steps is exactly 2|sin(tδ/2)|: at least (2/π)tδ while tδ ≤ π, growing until it saturates at 2 (PROVED (in-model), `SelfRef/Precision.lean` `ball_record_bound`, `disk_record_error`, `disk_error_linear`, `disk_exceeds_ball`; OBSERVED (numerical) values in `k_round8.stdout`, for example 1.918 = 2|sin 5| at t = 10⁴, δ = 10⁻³). For finite groups the update is learned exactly, so the polytope exclusion by SFP is not motivated without U.
- **Sharp records.** Copyable records are jointly perfectly distinguishable (no-broadcasting, Barnum, Barrett, Leifer and Wilce 2007, KNOWN, with S1). Only a linear core of this is checked in Lean (`no_copy_mixture`: a linear map that copies two records and their equal mixture forces the two to coincide when effects separate them); the full step to pairwise perfect distinguishability is not formalized, so in Lean it is partial. Purity is not derived; see counterexample C2.

## 6. Round 9: energy observability, the price of an unknown update, and non-Jordan orbitopes

- **Hereditary SFP against energy observability (EO).** Inside the Jordan class (Barnum, Müller and Ududec 2014), EO leaves exactly complex quantum theory, which satisfies SFP on every face, so EO implies hereditary SFP. The converse fails: the quaternionic qubit, quaternionic and octonionic theories and odd balls satisfy hereditary SFP but not EO. No proof without the classification was found.
- **open miss: pricing the memory for an unknown update favours polytopes.** Standing memory plus re-learning, in bits, to keep a one-bit record readable at error ε under an unknown non-trivial update acting on the tracked system relative to the tracker (OBSERVED (numerical), `l_round9.stdout`): polytopes 0.50–0.875, exact and independent of ε; ball 3.3–13.3 (the reader stores the axis); disk 6.8–12.8. The ball beats the disk only down to ε ≈ 1e-3 in this model. No exclusion without drift follows; this restates U.
- **Non-Jordan orbitopes in affine dimension 4–8** (orbitopes as in Sanyal, Sottile and Sturmfels 2011). SFP passes for the SO(3) spin-3 sphere orbitope (dimension 7), the spin-1+2 sphere orbitope (dimension 8) and the SU(3) flag orbitope (dimension 8); it fails for the SO(2) (Carathéodory) and torus orbitopes and a generic spin-2 orbit. Capacities found: 2, 4 and 2 (`l_round9.stdout`, `l_round9_check.stdout`; the capacity 4 is PROVED (in-model), see C1).

## 7. Counterexamples

- **C1, PROVED (in-model).** The spin-1+2 sphere orbitope (the convex hull of the image n ↦ (n, nnᵀ − I/3) of the sphere, all non-negative affine effects) has four perfectly distinguishable pure states at affine dimension 8: on a regular tetrahedron t₁..t₄ the effects pᵢ(n) = (1 + 3 n·tᵢ)²/16 are non-negative, pᵢ(tⱼ) = δᵢⱼ, and Σpᵢ = 1 because the tetrahedron is a spherical 2-design (grid check: minimum 1.5e-12, |Σ − 1| ≤ 9e-16, `l_round9_check.stdout`). It satisfies SFP, so SFP plus minimal dimension does not pick quantum theory (complex quantum theory needs dimension 15 for capacity 4). Its faces are images of circles, on which the circle's stabilizer acts by rotation with no fixed pure state, so it fails hereditary SFP.
- **C2, PROVED (in-model).** The tetrahedron with the transitive Klein four-group: every non-identity element fixes a perfectly distinguishable pair of mixed states (the averages of its two 2-cycles) and no vertex. Mixed-record SFP under transitivity alone does not exclude it; strong symmetry does.
- **C3, PROVED (in-model).** Quantifier order: requiring one pure state fixed by every update consistent with finite records leaves only the centre in any continuous transitive world (§5).

## 8. Remark (HYPOTHESIS, offered as a remark and not a claim)

Inside the Jordan class, hereditary SFP plus "the cheapest bit" (minimal affine dimension at capacity 2, the chain note's S5 pricing) leaves complex quantum theory in every dimension, the same set that Barnum, Müller and Ududec obtain from observability of energy, without a time-evolution premise. Hereditary SFP is strictly weaker than EO there, and the route rests on an infinite reversible group (close to U), heredity over faces, the Jordan class (or strong symmetry, Barnum and Hilgert, arXiv:1904.03753, no Crossref DOI found), and the cost step. Outside the Jordan class the two are very likely independent: C1 plausibly satisfies EO and fails hereditary SFP (not checked against the formal definition). Whether SFP is an independent reading or a reformulation of EO is OPEN.

## 9. Open misses and open items added by rounds 4–9

1. **open miss.** "Tracking never finishes" (U) is not derived from self-tracking (§2).
2. **open miss.** Selection and inflow do not separate the geometries (§3, §4).
3. **open miss.** Without drift, pricing the memory for an unknown update favours polytopes (§6).
4. **open miss.** "No outside frame" does not force drift (§5).
5. **OPEN.** The "every update" premise of SFP is not derived, and purity of records is not derived (§5).
6. **OPEN.** A proof relating EO and hereditary SFP without the classification; a wider search of non-Jordan transitive bodies in dimensions 4–8 (§6, §8).

## 10. Lean

Two modules, `formal/lean/GTAO/Rnd/SelfRef/SFP.lean` and `formal/lean/GTAO/Rnd/SelfRef/Precision.lean` (namespace `GTAORnd.SelfRef.R78`), moved from the side session's Lake project with only the header, the module lines and doc-comment wording changed. 19 theorems; `formal/lean/scripts/RndAxioms.lean` prints their axioms, and each depends only on `propext`, `Classical.choice` and `Quot.sound`. The definition is `SFP G X := ∀ g : G, ∃ x : X, g • x = x`; the ball model is the unit sphere of ℝⁿ with `specialOrthogonalGroup (Fin n) ℝ` acting by `mulVec`.

| item | statement | Lean | status |
|---|---|---|---|
| L1 | Jordan: a finite group acting transitively on a finite set with at least two points has an element with no fixed point; so finite transitive groups fail SFP (simplex with Sₙ, the square's quarter turn) | `jordan_derangement`, `finite_transitive_not_SFP`, `simplex_not_SFP`, `square_rotation_moves_all`, `square_not_SFP` | PROVED (in-model) |
| L2 | every element of SO(2m+1) fixes a unit vector and its antipode; odd balls with SO(2m+1), including the qubit ball, satisfy SFP | `SO_odd_fixes_unit`, `SO_odd_fixes_poles`, `SO3_fixes_poles`, `odd_ball_SFP` | PROVED (in-model) |
| L3 | a non-identity element of SO(2) fixes no non-zero vector, so the disk fails SFP; −1 ∈ SO(2m) fixes no unit vector, so even balls fail SFP | `SO2_nonid_no_fixed`, `disk_not_SFP`, `even_ball_not_SFP` | PROVED (in-model) |
| L4 | finite precision: ball record within 2 sin δ for every number of steps; disk record error exactly 2\|sin(kε/2)\|, at least (2/π)k\|ε\| while k\|ε\| ≤ π, and above 2 sin δ once π sin δ < kδ ≤ π | `ball_record_bound`, `chord`, `disk_record_error`, `disk_error_linear`, `disk_exceeds_ball` | PROVED (in-model) |
| L5 | copyable records are distinguishable: only the linear core (no linear copy of two distinct records and their equal mixture, with separating effects) | `mixture_copy_core`, `no_copy_mixture` | partial: the full no-broadcasting step is not formalized |

Not formalized: the criterion "SFP iff the stabilizer contains a maximal torus" (maximal torus theorem, Hopf and Samelson), the closed-subgroup classification of O(3) used for the dimension-3 statement, other transitive groups (G₂ on the 7-ball, real and quaternionic quantum theory), the orbitope results of §6–§7, and the selection-cost and inflow statements of §3–§4. Lean covers only the full SO(n) on balls and finite transitive groups.

## 11. Sources (Crossref-checked; `doi_check_2.out`)

- Barato, Seifert 2013, EPL 101:60001, `10.1209/0295-5075/101/60001`
- Barato, Seifert 2014, PRL 112:090601, `10.1103/PhysRevLett.112.090601`
- Barnum, Barrett, Clark, Leifer, Spekkens et al. 2010, NJP 12:033024, `10.1088/1367-2630/12/3/033024`
- Barnum, Barrett, Leifer, Wilce 2007, PRL 99:240501, `10.1103/PhysRevLett.99.240501`
- Barnum, Hilgert, arXiv:1904.03753 (no Crossref DOI found; cited by arXiv identifier)
- Barnum, Müller, Ududec 2014, NJP 16:123029, `10.1088/1367-2630/16/12/123029`
- Bartlett, Rudolph, Spekkens 2007, RMP 79:555–609, `10.1103/RevModPhys.79.555`
- Bennett 1973, IBM J. Res. Dev. 17:525–532, `10.1147/rd.176.0525`
- Boyd, Mandal, Crutchfield 2016, NJP 18:023049, `10.1088/1367-2630/18/2/023049`
- Chapman, Miyake 2015, PRE 92:062125, `10.1103/PhysRevE.92.062125`
- Chiribella, D'Ariano, Perinotti 2010, PRA 81:062348, `10.1103/PhysRevA.81.062348`
- Deffner 2013, PRE 88:062128, `10.1103/PhysRevE.88.062128`
- Deffner, Jarzynski 2013, PRX 3:041003, `10.1103/PhysRevX.3.041003`
- del Rio, Åberg, Renner, Dahlsten, Vedral 2011, Nature 474:61–63, `10.1038/nature10123`
- Deutsch 1991, PRD 44:3197–3217, `10.1103/PhysRevD.44.3197`
- England 2013, J. Chem. Phys. 139:121923, `10.1063/1.4818538`
- England 2015, Nat. Nanotechnol. 10:919–923, `10.1038/nnano.2015.250`
- Esposito, Van den Broeck 2011, EPL 95:40004, `10.1209/0295-5075/95/40004`
- Giovannetti, Lloyd, Maccone 2015, PRD 92:045033, `10.1103/PhysRevD.92.045033`
- Gross, Müller, Colbeck, Dahlsten 2010, PRL 104:080402, `10.1103/PhysRevLett.104.080402`
- Hänggi, Wehner 2013, Nat. Commun. 4:1670, `10.1038/ncomms2665`
- Hopf, Samelson 1941 (Crossref year 1940), Comment. Math. Helv. 13:240–251, `10.1007/BF01378063`
- Landauer 1961, IBM J. Res. Dev. 5:183–191, `10.1147/rd.53.0183`
- Mandal, Jarzynski 2012, PNAS 109:11641–11645, `10.1073/pnas.1204263109`
- Montgomery, Samelson 1943, Ann. Math. 44:454, `10.2307/1968975`
- Müller, Ududec 2012, PRL 108:130401, `10.1103/PhysRevLett.108.130401`
- Page, Wootters 1983, PRD 27:2885–2892, `10.1103/PhysRevD.27.2885`
- Perunov, Marsland, England 2016, PRX 6:021036, `10.1103/PhysRevX.6.021036`
- Pfister, Wehner 2013, Nat. Commun. 4:1851, `10.1038/ncomms2821`
- Sanyal, Sottile, Sturmfels 2011, Mathematika 57:275–314, `10.1112/S002557931100132X`
- Serre 2003, Bull. AMS 40:429–440, `10.1090/S0273-0979-03-00992-3`
- Short, Wehner 2010, NJP 12:033023, `10.1088/1367-2630/12/3/033023`
- Still, Sivak, Bell, Crooks 2012, PRL 109:120604, `10.1103/PhysRevLett.109.120604`
- Weyl 1916, Math. Ann. 77:313–352, `10.1007/BF01475864`

Hardy 2001 (continuity axiom) is cited as in the chain note (DataCite, `10.48550/arXiv.quant-ph/0101012`).

## 12. Reproduce

From `theory/record-cost-2026-11-25/scripts/selfref/`, run `python3 <script>.py` for `g_round4`, `h_round5`, `i_round6` (about 80 s), `j_round7`, `k_round8`, `l_round9`, `l_round9_check` (numpy, scipy ≥ 1.15 for `sph_harm_y`). Outputs are the `.stdout` files beside them. The repository copy of `l_round9.py` tries every combination of distinct permutations as its diagonal candidate sets; the session copy repeated entries and under-reported the CP² capacity as 2. The repository run gives 3 for CP² (its known value), 2 for the flag orbitope, and the other rows as in the session. Lean: `tools/check_lean.sh` in the dedicated Lean checkout, then `lake env lean scripts/RndAxioms.lean` in `formal/lean/`.

## 13. Round 10 (pointer, appended)

Round 10 tests whether U follows from more basic premises: `theory/RECORD_COST_ROUND10_2026-11-25.md`.

## 14. Errata (pointer, appended 26 November 2026)

The §8 phrase "without a time-evolution premise" overstates the remark; corrected wording, the fact that SFP plus transitivity already implies U, and the SO(3)-versus-O(3) group rule are in `theory/RECORD_COST_ERRATA_2026-11-26.md` §1. The text above is unchanged.
