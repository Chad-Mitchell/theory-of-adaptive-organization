# Forces, gravity, dimension and time: does the record-cost principle reach them? (exploratory round, private R&D note, not a PR)

Date: Thu 26 Nov 2026, 00:42–00:55 EST. For Chad. Nothing pushed, posted or emailed; no git operations; no repo files edited. Repo read at `/workspace/fresh-11` (`78dde34`): THEORY.md B.6 (CT18, CT18-H, CT25), `theory/GENERALITY_2026-11-22.md` (JP-heat), `theory/GENERAL_FLOOR_FINITE_2026-11-23.md`.
Scripts `scripts/*.py`; outputs `outputs/*.txt`; citations `crossref_forces_gravity.txt` (every DOI below returned OK; one guessed DOI, 10.1103/PhysRevD.24.2208, returned 404 and is not used); abstracts `mm2013_abstract.txt`.

Labels: **[OBS]** numerically observed in the stated toy; **[HYP]** hypothesis; **[PIM]** proved in model; **[KNOWN]** published, DOI verified; **[MISS]** open miss.
The hypothesis sentence is unchanged: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." Nothing here derives QM, GR, holography or gravity. At most it says which inputs of a known route the framework supplies.
Wording: "law" appears only in the CORE.md:7 sentence above; boundary vs volume scaling of entropy is called "area scaling" here.

## 0. Plain-language summary
We asked whether the record-cost idea, which already points toward quantum structure, also points toward forces and gravity. For forces the answer is a qualified yes: if neighbouring parts keep records in their own frames and compare them often, it is cheaper to keep a "translation" record on each link, and the mismatch you get carrying a record around a small loop is exactly the standard lattice formula for electromagnetism-type forces. Whether that mismatch is ever non-zero, and how the links change over time, still has to be put in by hand. For gravity, the record cost of a region does scale with its boundary in natural low-energy states (not in random ones), which is the ingredient Jacobson's 1995 argument uses, but the other ingredients (horizons, the Unruh temperature, equilibrium) are not supplied; the theory's own "temperature" (CT18) is a real Arrhenius temperature only in one special case and has no route to the Unruh temperature.

## Q1 Forces: does comparing frames force a connection and a Wilson-type cost?
Toy: sites on a ring or square lattice, each holding a record (a disk/U(1), Z_n or Bloch-ball/SU(2) record) in its own frame g_i. Comparing neighbours needs the relative frame on the edge. `scripts/q1_gauge.py`, `outputs/q1.txt`.

| item | label | result |
|---|---|---|
| Edge record vs re-learning | [PIM, trivial] | Comparing M times per drift period costs M·log2 n bits if the offset is re-learned each time, log2 n if it is kept on the edge (n=6, M=10: 25.85 vs 2.58 bits). **A connection is forced once comparisons per drift period exceed 1.** It is chosen (a tie) at M = 1. |
| What the edge record must hold | [PIM; OBS exhaustive] | Up to relabelling local frames, only n^(E−V+1) classes exist (ring N=4, n=3: 3 of 81; 2×2 torus, n=3: 243 of 6561). The cheapest edge record keeps only loop holonomies: **gauge invariance comes out of cost minimisation** (redundant frame bits are free to drop). |
| Loop mismatch = Wilson term | [PIM; checked to 1e-14] | Carrying a disk record round a plaquette of holonomy F: squared error = 2(1−cos F); log-loss (KL, von Mises record of concentration κ) = κ·A(κ)·(1−cos F) with A = I1/I0. Both equal the **U(1) Wilson plaquette action** (Wilson 1974). Z_n gives the Z_n clock-model gauge action. Weak field: (1−cos F) ≈ F²/2, the lattice Maxwell term. |
| Form depends on the loss | [PIM] | Absolute-error loss gives 2|sin(F/2)|, which is not Wilson. Wilson form is forced given quadratic or log loss, chosen otherwise. |
| SU(2) frames on a qubit record | [OBS, 2e5 samples] | Mismatch = (4/3)(1−cos θ) = (2/3)(3 − tr_adj R): the **adjoint** Wilson action, not the fundamental 1 − ½Re tr U (e.g. θ=1.969: 1.852 vs adjoint 1.850, fundamental 0.447). **[MISS]** Copyable records are Bloch vectors, so they only see SO(3); the fundamental action (spinor matter, centre Z2) needs amplitudes, which are not records. |
| Curvature | [PIM] | Misaligned frames alone give pure-gauge edges and zero plaquette cost exactly (outputs: [0,0,0,0]). **Non-zero field strength is an input** (the world's transports are not integrable). Not forced. |
| Dynamics | [MISS] | Weighting configurations by exp(−β·cost) (max-entropy at fixed mean cost) gives exactly Wilson lattice gauge theory, but that weighting, the coupling β, the time direction/kinetic term and the gauge group itself are put in. Matter charges and why U(1)×SU(2)×SU(3) are untouched. |

Forced vs chosen, as Ace asked: **forced** in model are the edge variable (when M > 1), gauge invariance (cost of redundant frame bits), and the Wilson functional form (given quadratic/log loss and plaquettes as the smallest compared loops). **Chosen** are the loss, locality (which loops are compared), non-zero curvature, the Gibbs weighting and β, and the group.
Analogy check: information value high (the cost reproduces Wilson exactly). Keep. It breaks at the fundamental representation and at dynamics; both logged [MISS].

## Q2 Gravity/holography: area scaling, Jacobson inputs, minimal cuts
Record cost of region A used: for a pure global state, the maximal copyable correlation J(A|Ā) = S(A) [KNOWN, Henderson–Vedral 2001]; for thermal states, I(A:Ā) (upper bound on any shared record); also I_zz, records read in one fixed local basis.

| test | label | numbers |
|---|---|---|
| 1D transverse Ising ring, N=18 (`q2_arealaw.py`) | [OBS] | Gapped g=2: S saturates at 0.256 bits from l=4 (I_zz 0.101). g=0.5: 1.008 (the 1-bit cat term plus a constant). Critical g=1: 0.683 → 1.110, slow log growth. **Random state: S = l up to Page's 8.279 at l=9 (volume scaling).** |
| 2D free fermions, 24×24 torus, l×l block | [OBS] | Gapped (staggered potential): S/(4l) → 0.186 flat from l=6–12 (**area scaling**). Metal: S/(4l) grows 0.364 → 0.722 (l log l, Fermi surface). Thermal metal β=2: I/(4l) → 0.426 flat (**mutual-information area scaling**, matches Wolf et al. 2008). |
| 4×4 random state | [OBS] | S = 1.000, 3.997, 6.819 for |A| = 1, 4, 9: volume. |
| Boundary rate (`q2_boundary_rate.py`, random brickwork, N=16) | [PIM bound + OBS] | Records about Ā can only enter A through boundary gates: ≤ 2 bits per crossing gate (half-chain: 6.785 ≤ 24 after 24 layers). But at late times S saturates to volume (4-site block → 3.968 of 4). **Locality gives a boundary-limited record rate, not an area scaling.** The area scaling needs a gap or finite correlation length (an input). |
| Perfect tensor ([[5,1,3]], HaPPY building block) (`q2_tensornet.py`) | [OBS] | S(A) = |A| for every |A| ≤ 3, error 1.3e-15: record cost = minimal cut exactly. |
| Random tree tensor network | [OBS] | S/log2 D tends to the min cut as D grows: interval of 2 non-siblings 1.546 → 1.709 → 1.913 for D = 2, 4, 8 (cut 2); three spread leaves 1.881 → 2.659 (cut 3). As in Hayden et al. 2016. |

Hypothesis [HYP]: the cost principle may *prefer* area-scaling states, since a tracker with capacity cost κ·log N can only hold states with bounded bond dimension (MPS/PEPS), and those obey area scaling. Not tested this round.

**Jacobson 1995 inputs (δQ = T dS with S = η·A on every local Rindler horizon):**

| input | supplied by our framework? |
|---|---|
| Lorentzian spacetime, local Rindler horizons at every point and null direction | No [MISS]. Nothing here has a metric or light cones. |
| Unruh temperature T = ħa/(2πck_B) (Unruh 1976; Bisognano–Wichmann 1976 KMS state of the vacuum) | No [MISS]; see Q4a. |
| Local equilibrium (vanishing expansion/shear at p, vacuum state) | No [MISS]. JP-heat gives δQ ≥ kT·İ (inequality); Jacobson needs equality, i.e. the reversible, quasi-static limit. |
| S ∝ area with a universal η (=1/4Għ) | Partly. The area-scaling scaling holds [OBS] for gapped/thermal states, but its coefficient depends on the cutoff (0.186 vs 0.426 bits per boundary bond above), so η is not universal [MISS]. |
| δQ as boost-energy flux of a conserved T_ab; Raychaudhuri equation | No [MISS]; geometry inputs. |

Ryu–Takayanagi analogue: in tensor networks our record cost equals the minimal cut [OBS], because for pure states it is S(A). That is a known property of the networks, not a consequence of the cost principle. A cleaner later route is Jacobson 2016 ("entanglement equilibrium": stationarity of S in small balls at fixed volume), since a first-order stationarity condition is sign-agnostic and could be read as stationarity of record cost [HYP]. It still needs the QFT vacuum and conformal fields as inputs.

## Q3 Dimension: lead only
- [PIM, Round 1/selfref R3] A state space with zero-cost continuous drift and a copyable one-bit record through the drift needs affine dimension d ≥ 3; the qubit ball meets it with equality.
- [KNOWN] Masanes, Müller, Pérez-García & Augusiak 2014 (J. Math. Phys. 55, 122203): ball state spaces of dimension d with continuous reversible dynamics and local tomography contain entanglement **only for d = 3** (two qubits). Müller & Masanes 2013 (NJP 15, 053040) add the input that the systems carry "minimal direction information" in d spatial dimensions, and get d = 3 with two-qubit quantum theory.
- Combined reading [HYP]: our cost gives d ≥ 3 for the record, MMPA give d = 3 for a reversibly entangling ball, and Round 11 gives "polytope parts with every read allowed don't entangle reversibly" for the proved family. So "entangling + reversible + cheap records" would pick the 3-dimensional ball among balls and the covered polytopes.
- **[MISS]** Identifying the Bloch-ball dimension with the number of space dimensions is Müller–Masanes's own input (direction-carrying systems), not supplied by us. The rebit (d = 2) is excluded only via local tomography. Value check: high (it plugs straight into Round 11). Keep.

## Q4 Time's arrow, relational time, and the CT18 temperature
**Q4a. Is CT18's 1/z a temperature?** (`q4_temperature_time.py`, `outputs/q4.txt`)
- [PIM + OBS] For proportional restoring (OU, dx = −x/τ dt + σ dW), the stationary distribution is Gibbs in U = x²/(2τ) at kT_eff = D = σ²/2, and U(B)/kT_eff = B²/(σ²τ) = **z² exactly**. The exact mean first-passage time follows Arrhenius/Kramers (Kramers 1940): d ln MFPT/d z² = 0.995 once the 1/z prefactor is removed (z ≥ 3). The FDT holds: simulated X = D/T_FDT = 0.99. So **in this case z² = barrier/temperature, and 1/z = √(kT_eff/E_B) is a genuine fluctuation–dissipation temperature ratio.** It is effective, in the units of the error variable; it is physical only if σ² comes from a real bath (then it is JP-heat's T via the Einstein relation).
- [OBS + PIM] For Poisson reset (the other CT18 mechanism) the FDT fails: X = 0.47 simulated, 1/2 exactly (variance σ²τ, susceptibility τ). The stationary distribution is Laplace with tail e^{−√2 z}, and resetting is a non-equilibrium steady state. **[MISS] No temperature there; THEORY.md's "analogy only" wording for D–Y stays right, and the FDT link holds only for proportional restoring.**
- (a) Mapping onto Unruh: **[MISS]**. T_U = ħa/(2πck_B) needs ħ, c, an acceleration and the Minkowski vacuum's KMS property on a wedge. CT18 has none, and JP-heat's T is any bath's T. One concrete bridge is noted, as an input: an accelerated Unruh–DeWitt detector used as the memory sees up/down rates in exact detailed balance at T_U. Then JP-heat's local detailed balance holds at T = T_U, and the record-update rate at the horizon is set by T_U. That puts the horizon and the vacuum in; it does not derive them.
- (b) KMS/thermal-time link: the stationary OU density defines a modular "Hamiltonian" K = −ln p = U/kT_eff. But a 1D overdamped process has no Hamiltonian flow, so Connes–Rovelli thermal time is not defined there [MISS]. It needs an underdamped (phase-space) error model, which CT18 doesn't have. Keep the analogy as a written pointer only; its attention cost is now higher than its expected value.

**Q4b. Relational order from records.**
- [PIM + OBS] Page–Wootters toy (clock with 6 ticks; a qubit rotated each tick; 5 memory bits filled by CNOT copies): the record content H_z(M | clock = t) = 0, 0.979, 1.958, 2.937, 3.916, 4.895 bits is strictly monotone. **Reversible record formation alone supplies an order** (more records = later). **Its sign is set by the blank-memory boundary**: read in the opposite clock order it decreases. That boundary is a low-record initial condition, put in by hand (a past-hypothesis-type input) [MISS for deriving the sign].
- [PIM, Landauer 1961] With finite memory, every later record overwrites a bit, at ≥ kT ln2·H per overwrite (H = 0.796, 0.218, 0.970, … bits per tick here). That is the cost's arrow, and it points the same way as the thermodynamic arrow, **by construction**, since Landauer is thermodynamic and needs a bath at T. Jacobson's equilibrium/temperature inputs are not supplied by this; record formation is the non-equilibrium side.
- Thermal time (Connes & Rovelli 1994): the state picks the flow, and the temperature is the ratio of that flow to a clock's time. For the OU case the state's flow would carry kT_eff (the CT18 ratio). Defining that flow needs a phase-space dynamics, and comparing it with proper time needs a clock and, for Unruh, a wedge. **[HYP] at best; not tested.**

## Ready to fold into a PR?
As a future append, not now: Q1's "loop mismatch = Wilson action (U(1)/Z_n, quadratic or KL loss) and gauge invariance from cost; adjoint-only for qubit records; curvature and dynamics are inputs". It is small, exact and reproducible (`q1_gauge.py`). Also Q4a's "z² = Arrhenius barrier/temperature for proportional restoring; FDT fails (X = 1/2) for Poisson reset". It sharpens CT18's "analogy only" wording without editing THEORY.md, and could go as a note under `theory/`. Q2 and Q3 are mapping/inputs tables. They are useful in a lab note, but carry no new result. Needs Ace's review and a fresh-clone rerun before any fold.

## Sharpest next tests
- Q1: derive the Gibbs weighting exp(−β·cost) and β from the theory's own selection term (NA4 destruction cost) rather than MaxEnt. Test whether record amplitudes (non-copyable) can be priced at all, to reach the fundamental representation.
- Q2: test the [HYP] directly. Minimise κ·log(bond dim) + q·(tracking error) for a tracker of a local Hamiltonian's state and see if the optimum is area-scaling even when the true state is volume-scaling (records cheaper than the state). Then try "cost stationarity" in place of Jacobson 2016's entanglement equilibrium on a lattice free field.
- Q3: check whether Round 11's proof family plus MMPA 2014 together cover every "ball or polytope" part, and state precisely what the rebit escape needs.
- Q4: an underdamped CT18 (phase-space error), where thermal time is defined, to test whether the modular-flow temperature equals kT_eff.

---

# Round 2 (Thu 26 Nov 2026, 00:55–01:02 EST): tracker test, entanglement equilibrium, selection weighting, thermal time, coverage
Same labels and rules. Scripts `scripts/r2_*.py`; outputs `outputs/r2_*.txt`, `outputs/q5_platonic_lp_rerun.txt`. New DOIs, all OK on Crossref: Fannes–Nachtergaele–Werner 1992 (10.1007/BF02099178), Osterwalder–Seiler 1978 (10.1016/0003-4916(78)90039-8), Casini–Huerta–Myers 2011 (10.1007/JHEP05(2011)036), Hislop–Longo 1982 (10.1007/BF01208372). Jacobson 2016 (10.1103/PhysRevLett.116.201101) was verified in round 1 and read in full this round (`j2016.txt`). Masanes et al. 2014 was read in full (`mmpa2014.txt`).

## R2.0 Plain-language summary
A tracker that pays for memory, and is only asked local questions, settles on a record that grows with a region's boundary even when the world itself is volume-like. So the boundary scaling and a finite correlation length come out of the cost; they no longer have to be assumed. But that is a property of the record, not the world, and it fails if readers ask global questions. The theory's own selection cost reproduces the exp(−β·cost) weighting exactly and the first-order Clausius form (δS = β δ⟨cost⟩) that Jacobson 2016 uses, and JP-heat's inequality becomes an equality only in the limit where the memory is infinitely faster than the world. Horizons, the Unruh value ħ/2π and the gravitational coupling are still inputs. Carrying a "superposed" record around a loop and reading the interference gives the full SU(2) force term, centre included. A phase-space version of CT18 has a genuine thermal-time temperature equal to σ²/(2γ). The shapes coverage still has named holes.

## R2.1 Tracker test: does the optimal record have area scaling? (`r2_tracker.py`, `r2_tracker_scaling.py`)
Record = MPS with bond cap χ (truncated SVD). J = κ·Σ_bonds log2 χ_b + q·err, q = 1. Two reader tasks: global (1 − fidelity) and local (mean trace distance of adjacent 2-site marginals).
- [OBS, N=12] Volume-scaling world (Haar random, true S = 1.0/2.99/5.28 for l = 1/3/6). The local error at χ = 2/4/8/16/32 is 0.428/0.229/0.091/0.039/0.006, while the global error stays 0.986/0.944/0.817/0.516/0.108. At κ = 0.01 the local task picks χ* = 32 (record S(6) = 4.84); at κ = 0.1 it picks χ* = 1.
- [OBS, N = 8…14] **At fixed χ the local error stops growing with N** (Haar world, χ = 2: 0.357, 0.415, 0.415, 0.414; χ = 4: 0.150, 0.196, 0.205, 0.204). **The global error goes to 1** (χ = 4: 0.506, 0.818, 0.941, 0.983). Thermalizing quench: the same pattern, weaker. χ = 8 is still finite-size limited at these N.
- [PIM] For a local task the cost per site, κ·log2 χ + q·ε_loc(χ), does not depend on N, so χ* doesn't either. Any tensor-network record then has S_rec(A) ≤ |∂A|·log2 χ*: **area scaling of the record is forced by (per-bond capacity cost + local reads)**, with a coefficient set by κ/q.
- [KNOWN, FNW 1992] A finitely correlated (injective MPS) record has a finite correlation length and is the unique ground state of a gapped local parent Hamiltonian (translation-invariant injective case). So **the gap comes out for the record**: the cost-optimal model of the world is a gapped-ground-state-like object.
- **Chosen:** the reads are local, capacity is priced per bond (local record channels), and the record format is a local network. **[MISS]** With global reads, χ* must grow exponentially in N and the record follows volume scaling. The world's own state is not forced to have a gap. The coefficient is cost-set, not universal (it does not give Jacobson's η).
- A side check failed: random-tensor MPS records with the same χ had local error 0.31–0.70, so the cost optimum depends on a fitted record, not just its size. Logged in ATTEMPTS.

## R2.2 Jacobson 2016 read as stationarity of record cost (`r2_jpheat_equality.py`, `r2_selection_gibbs.py`)
Jacobson 2016's route, from the text: the maximal vacuum entanglement hypothesis (MVEH) says S in small geodesic balls is maximal at fixed volume in a maximally symmetric vacuum. Then δS = η δA + δS_IR. Here δS_IR = (2π/ħ) δ⟨K⟩ follows from ρ = e^{−K/T}/Z minimising the modular free energy ⟨K⟩ − TS with T = ħ/2π. K = H_ζ, the conformal-boost Hamiltonian, is local only for CFTs (Hislop–Longo; Casini–Huerta–Myers). First-order variations at fixed volume give the Einstein equation; nonconformal fields need an extra conjecture.

| Jacobson 2016 input | supplied? |
|---|---|
| Gibbs / first-order Clausius structure (stationary point of a free-energy-type functional; δS = β δ⟨K⟩) | **Yes, in form [PIM].** The theory's selection cost E_s[q·cost] + λ·D(s‖p0) has its unique minimum at s = p0·e^{−(q/λ)·cost}/Z: Z_3 plaquette, max deviation 2.4e−6, J_opt = −λ ln Z = 0.750020. At the optimum, first-order δE[cost] = (λ/q)·δS_Shannon (three random directions agree to 1e−6). It is the same identity Jacobson uses as δS = 2π δ⟨K⟩/ħ. |
| Equilibrium (equality in the Clausius relation) | **Only in a limit [PIM + OBS].** Telegraph world with a two-state memory under local detailed balance: I_alt = r·L(ε) exactly (repo T59), and efficiency kT·I/Q̇ = 0.237, 0.547, 0.855, 0.983, 0.998, 0.9998 for memory rate g = 0.5 … 10⁴ (dE = kT). The gap σ_M ≈ 0.79/g. At the cost optimum of J = q·ε + λ·Q̇/kT + c·g, efficiency is 1.0000 at c = 0 (optimum at the grid edge, g → ∞), and 0.985, 0.956, 0.872, 0.652 at c = 1e−4, 1e−3, 1e−2, 0.1. **Equality ⇔ the record relaxes infinitely faster than the world drifts.** Any positive price on speed keeps JP-heat strict. So the framework supplies "equilibrium" exactly as a timescale-separation limit, not as a default. |
| Area term η δA with a universal η | Scaling yes (R2.1, cost-set coefficient); universality no [MISS] |
| T = ħ/2π; K = local boost generator; vacuum of a QFT; geodesic balls in a Lorentzian geometry; fixed-volume variation | No [MISS] |
| Sign: MVEH maximises S; our cost is minimised | First order only needs stationarity, so no clash at first order. At second order the sign could clash [MISS, untested]. |

## R2.3 Weighting from selection cost, and pricing amplitudes (`r2_selection_gibbs.py`)
- [PIM, Gibbs/Donsker–Varadhan variational principle] Replacing max-entropy by the theory's own destruction cost D(s‖p0) (NA4) gives exactly exp(−β·cost) with **β = q/λ** (stake per unit mismatch ÷ price per bit of selection). With the round-1 loop cost this is the Wilson lattice gauge weighting. **Forced:** the exponential form and the meaning of β. **Chosen:** p0 = uniform (Haar) reference, and that selection acts on link configurations. Osterwalder–Seiler 1978 (KNOWN) gives reflection positivity for the Wilson action, i.e. the route to a Hamiltonian. That is a known add-on, not supplied by us.
- [PIM + OBS, 1e5 Haar states] For SU(2) holonomy U and a spinor carried round the loop:
  - The copyable (fidelity) readout costs (3 − χ_adj)/6, the adjoint form (e.g. 0.5365 vs 0.5367 predicted).
  - **An interference readout** costs 1 − ½ Re tr U, **the fundamental Wilson action**, exact to the sampled digits (0.5585, 1.8975, 0.7032). Here an ancilla controls whether the record goes round, and only the ancilla's outcome, which is copyable, is recorded.
  - At the centre, U = −1, fidelity cost is 0 and interference cost is 2: only the interference readout sees the centre.
- So non-copyable amplitudes can be priced through a copyable readout of a coherent probe. **Chosen [HYP]:** that the cost uses that readout. It pays off only if centre-valued holonomies carry stakes, which is a value-of-information condition we haven't derived.

## R2.4 Underdamped CT18 and thermal time (`r2_underdamped.py`)
- [PIM, textbook Langevin] dx = v dt, dv = (−γv − ω²x)dt + σ dW has the stationary state ρ ∝ e^{−βH}, with H = v²/2 + ω²x²/2 and β = 2γ/σ².
  - So K = −ln ρ = βH, and the K-flow is the H-flow with t = β·s: **thermal-time temperature = σ²/(2γ)**.
  - The overdamped reduction (τ = γ/ω², σ_x = σ/γ) gives CT18's z² = B²/(σ_x²τ) = U(B)/kT exactly, and kT_eff = σ²/2 at γ = 1. **Match: yes.**
- [OBS, Euler sims of 6e6 steps]: 1/β = 0.488, 1.067, 0.373 against σ²/(2γ) = 0.500, 1.067, 0.375 (batch s.e. 0.010, 0.030, 0.003). Classical KMS ⟨{x,v}⟩ = β⟨v²⟩ holds within those errors, and Σ⁻¹ is diagonal (|Σ⁻¹_xv| ≤ 0.002).
- **Chosen:** inertia (a phase-space error model). CT18 itself has none, and this temperature is in error units.
- **[MISS]** Unruh: Connes–Rovelli temperature = ratio of thermal time to a clock's time. Getting ħa/2π needs the Minkowski vacuum on a wedge (Bisognano–Wichmann) and an accelerated clock, neither supplied. Poisson-reset CT18 stays non-thermal (round 1, X = 1/2).

## R2.5 Coverage: Round 11/12 + Masanes et al. 2014 for ball and polytope parts
Masanes et al. 2014 assumptions (from the text): two parts with the **same-dimension** Euclidean ball state space, local groups transitive on the sphere, a **continuous** reversible global group, local tomography. Only two-qubit QT has interacting dynamics. They name as open: balls of different dimensions, and multipartite entanglement.

| part pair | covered? |
|---|---|
| ball(d) × ball(d), d ≠ 3 | Yes, KNOWN (MMPA 2014; continuous dynamics + local tomography) |
| ball(3) × ball(3) | QM is the one entangling case (the target) |
| ball(d) × ball(d′), d ≠ d′ | **No [MISS]**, open in MMPA themselves |
| ball × polytope | **No [MISS]**: neither covers it |
| simplex × anything | Yes, trivial (no entangled states) |
| regular polygon × regular polygon (any n, m), locally symmetric, finite orbits | Yes, PIM (R12 Cor. M12-P) |
| hypercube, cross-polytope, Hanner polytopes with absolutely irreducible transitive groups | Yes, PIM (M11, Hanner ⇒ (★)) |
| icosahedron, dodecahedron, cuboctahedron (same-type pairs) | **Not certified.** Rerun of the R12 LP search (3000 random objectives): best Φ = 0 for I×I, D×D, CO×CO (and Q×Q, O×O). That is a lower bound only [OBS], not a proof of ♦. |
| icosahedron × dodecahedron | **♦ fails**: an extreme point with Φ = +2.05 (‖C‖² = 1.894, a = b = 0) [OBS]. M12 is silent there [MISS]; not evidence for an entangling map. |
| non-transitive polytopes; composites that are not locally symmetric; 3+ parts | No [MISS] |
| premise mismatch | MMPA need a *continuous* reversible group; M12 excludes *any* reversible entangling map for finite orbits. The ball case with a discrete entangling map (and the rebit without local tomography) is not covered [MISS] |

## R2.6 Foldable (future append only, after review and a fresh-clone rerun)
- **Strongest:** "Selection cost ⇒ Gibbs weighting with β = q/λ, and loop cost ⇒ Wilson action. Copyable readout ⇒ adjoint, interference readout ⇒ fundamental." Exact and small (`q1_gauge.py`, `r2_selection_gibbs.py`).
- "JP-heat equality ⇔ memory/world rate → ∞; any rate price keeps it strict", with the efficiency table. This connects to the repo's T59 telegraph identity. It is a theory/ note candidate.
- "CT18 has a thermal-time temperature σ²/(2γ) in the phase-space model and an Arrhenius reading for proportional restoring; Poisson reset has none." A theory/ note candidate; it would not edit THEORY.md.
- The R2.1 record area-scaling result is a lab-note item until a 2D (PEPS) or larger-N check exists. The R2.5 table belongs in the Conjecture C open-miss entry.

## R2.7 Sharpest next tests
1. Certify or refute ♦ for I×I and D×D exactly (lrs vertex enumeration of max), and decide I×D by a direct automorphism search.
2. A 2D record test (small PEPS or a free-fermion Gaussian record with a mode cap) of the forced area scaling.
3. A second-order sign check: is the cost optimum a minimum where MVEH needs a maximum?
4. Derive when centre holonomies carry stakes (value of information), which would make the fundamental action forced rather than chosen.

---

# R2 corrections (append-only, from the hostile reviewer's partial checks in `review_g2/hr_checks_out.txt`, 01:06 EST; HOSTILE_REVIEW_G2.md had not yet appeared)
- **R2.1 normalisation error (fixed by relabel).** `r2_tracker.py` summed capacity over bonds but **averaged** the local error, so its "χ* by κ" table mixes an extensive and an intensive term. That table is withdrawn. Rescored consistently (`outputs/r2_tracker_renorm.txt`: both summed, N = 12), truncated-SVD records pick χ* = 32 to 64 for a Haar world at κ ≤ 0.1. So **at N = 12 the SVD data alone do not show a bounded χ*.**
- **The [PIM] argument is restated with its real premise.** χ* stays bounded as N grows iff some fixed-χ record has a per-pair local error that doesn't grow with N. The reviewer exhibits one: next-nearest Bell pairs with χ ≤ 4 have local error 0.097, 0.026, 0.0063 at N = 8, 12, 16, equal to the distance of the true marginals from I/4. So that premise holds for Haar worlds [OBS]. Truncated SVD is a poor local record, so the observed SVD numbers are not the optimum. The record area-scaling claim in R2.1 stands on the PIM argument plus this record, and now on the 2D test (G3-1). It does not stand on the SVD table.
- **R2.2 JP-heat**, a reviewer check [OBS]: at fixed memory rate g, efficiency tends to g/(g + r) as dE → 0 (0.3333, 0.6667, 0.9091 for g = 0.5, 2, 10). So efficiency < 1 at any finite g. This tightens "equality only as g → ∞".
- **R2.3 Gibbs form**: with a χ² divergence in place of KL, the optimum weights are linear in cost, not exponential (reviewer, Z_3 plaquette). **Relabel:** exp(−β·cost) is forced *given NA4's KL destruction cost*. The choice of KL is what forces it. NA4 does price destruction in KL bits, so the claim holds within the repo's definitions, but it is not divergence-independent.
- **R2.3 SU(2) interference**: for SU(2), Re⟨ψ|U|ψ⟩ = ½ Re tr U for *every* ψ, exactly (U = cos θ·1 + i sin θ n·σ), so no Haar average is needed. For SU(3) it depends on the state, and only its average is the fundamental character. General rule (reviewer): a readout linear in U averages to the fundamental character, and one bilinear in U and U* gives adjoint + trivial.

# Round G3 (Thu 26 Nov 2026, 01:05–01:25 EST): 2D record scaling, second-order sign, centre stakes, wedge temperature
Scripts `scripts/g3_*.py`; outputs `outputs/g3_*.txt`. New DOIs OK on Crossref: Lashkari–Lin–Ooguri–Stoica–Van Raamsdonk 2016 (10.1093/ptep/ptw139); Rauch et al. 1975 (10.1016/0375-9601(75)90798-7); Werner et al. 1975 (10.1103/PhysRevLett.35.1053); Peschel 2003 (10.1088/0305-4470/36/14/101). A DOI I tried for Eisler–Peschel 2017 resolved to a different paper (Bridgeman–Chubb), so it is **not cited**.

## G3.0 Plain summary
In a 2D world whose own entanglement grows with area, the cheapest record that still answers every local question holds correlations that grow only with the perimeter. That now holds in 2D, not just 1D. The theory's selection-cost minimum and Jacobson's entropy maximum agree in sign once record cost is read as a free energy, and they clash if it is read as entanglement itself. The full SU(2) force term is forced only when the world has spin-½ probes *and* someone bets on two-path interference. A tracker that can read only half of space sees a temperature of exactly 1/(2π) per unit of boost, the Unruh form. But that comes from the vacuum and relativity, which are inputs, not from the cost.

## G3-1 2D record scaling with local reads (`g3_2d_record.py`; `outputs/g3_2d.txt` L=14, `outputs/g3_2d_L20.txt` L=20)
- **Setup.** Gaussian fermion worlds on a 20×20 torus. A random Slater determinant and a typical excited eigenstate (β = 1) of nearest-neighbour hopping. Reads are all two-point functions within range R = 1, 2, 3.
  - Record capacity cost = total correlation (Σ site entropies − global entropy). With the site marginals fixed by the reads, minimising it = maximising global entropy [PIM, one line].
  - Under two-point constraints the maximiser is the Gaussian state ρ ∝ exp(−c†hc), with h supported on the read pattern [KNOWN]. It is fitted by the convex dual. Every read is reproduced to ≤ 7e−5.
- [OBS] **The world grows with area**: S(A) for l×l blocks at l = 2…10 is 3.97 → 80.06 (Slater) and 3.25 → 52.62 (eigenstate).
- [OBS] **The record grows with perimeter**: I(A:Ā)/(4l), averaged over 4 block positions.
  - Eigenstate world: flat at 0.219–0.226 (R=1), 0.231–0.242 (R=2), 0.256–0.274 (R=3) for l = 2…10.
  - Joint fit a·4l + b·l² + c at l = 10: area part −0.19, −0.29, −0.45 vs perimeter part 9.2, 10.0, 11.5.
  - Slater world, much weaker correlations: /4l is flat at 0.0034–0.0044 (R=1) and 0.042–0.052 (R=3). The R=3 fit leaves a small positive area part, 0.27 vs 1.80 at l = 10. That may be finite size (R comparable to l), and I log it as a residual, not a claim.
- [KNOWN → PIM here] The record is a Gibbs state of a Hamiltonian with range R. So Wolf–Verstraete–Hastings–Cirac 2008 gives I(A:Ā) ≤ 2β‖h‖·|∂A|: **a proved perimeter bound for the cost-optimal record.**
- **Forced:** perimeter scaling of the record, given (local reads + total-correlation capacity cost). **Chosen:** that capacity is priced as total correlation, and that reads are local and two-point. **[MISS]:** the world's own state is unconstrained, and the coefficient grows with read range R, so it isn't universal.

## G3-2 Second-order sign: our minimum vs Jacobson's maximum (`g3_second_order.py`)
- [PIM, exact identity; checked to 1e−10] For ρ = e^{−K/T}/Z: F_K(ρ′) − F_K(ρ) = T·D(ρ′‖ρ) ≥ 0, with F_K = ⟨K⟩ − TS.
  - Second variations at ρ, in directions scaled to keep states positive: δ²F = +17.4, +2.2, +66.8 (a minimum); δ²S at fixed ⟨K⟩ = −68.9, −3.9, −65.4 (a maximum).
  - **So "free-energy minimum" and "entropy maximum at fixed ⟨K⟩" are one second-order statement.** The positive term is D(ρ′‖ρ), the same relative entropy as our selection cost D(s‖p0).
- [KNOWN] In holography, second-order positivity of exactly this relative entropy is equivalent to positivity of canonical energy (Lashkari et al. 2016). So the sign Jacobson's maximum needs is the sign our D-term carries.
- **Clash reading [PIM, trivial]:** if record cost is read as the entanglement S(A) of a pure record (I(A:B) = 2S(A)), capacity cost is minimised by products (θ = 0, S = 0), while MVEH wants maximal S (θ = π/4, S = 1 bit). **So the consistent reading is record cost ↔ modular free energy, not record cost ↔ entanglement [HYP].**
- **[MISS]:** Jacobson's maximum also varies geometry (the η δ²A term), and his own second-order argument is qualitative. We say nothing about the geometric part.

## G3-3 When does the centre carry stakes? (`g3_centre.py`; 2×10⁴ samples per row)
Value of the centre bit s = ±1 (U = s·U0), as I(outcome; s | U0, probe, read) in bits per shot:

| probe | one-path read (copyable record) | two-path interference read |
|---|---|---|
| spin-½ | 0.0000 | **0.2030** |
| spin-1 | 0.0000 | 0.0000 |

- [PIM] The centre is invisible to any read bilinear in U and U*, and to any integer-spin probe. It is visible only to a read linear in U, i.e. coherent interference with an arm that did not go round, on a half-integer probe.
- **The fundamental action is forced iff** (i) the world has spin-½ probes, (ii) readers bet on two-path interference, and (iii) the stake beats the cost of one extra bit per holonomy (single shot: q·0.203 > κ·1 bit).
- Otherwise the cost principle drops the centre bit and the adjoint/SO(3) action is the cheaper record.
- [KNOWN] Nature has (i) and (ii): the 4π sign change of neutron spinors seen in interferometers (Rauch et al. 1975; Werner et al. 1975).
- [HYP] Inside the framework, (i) holds if the world's continuous drift acts on qubits as SU(2), which is the qubit-ball route of rounds 1–9. Whether readers bet on interference is a stake assumption, not derived.

## G3-4 Cost-side route to the Unruh value: a tracker whose reads stop at a boundary (`g3_wedge.py`)
- **Setup.** Ground state of a free-fermion chain, N = 800 (massless, and gapped with staggered mass 0.1 and 0.3). The tracker can read only the right half, and its state is ρ_R.
  - Its modular Hamiltonian K = −ln ρ_R has single-particle matrix ln((1−C)/C) (Peschel 2003, KNOWN).
- [OBS] The coefficients of K on the bonds next to the cut are 3.142, 6.283, 9.423, 12.542, against the Bisognano–Wichmann prediction 2π(x+1)/v = 3.142, 6.283, 9.425, 12.566 (v = 2).
  - Fitted slope ÷ (2π/v) = 0.9976 (massless), 0.9966 (m = 0.1), 0.9920 (m = 0.3).
  - Beyond x ≥ 4, double precision saturates (C eigenvalues within 1e−15 of 0 or 1), so those entries are not evidence.
- **Reading.** The thermal-time (modular) flow of the tracker's state is the local boost with KMS period 2π per unit rapidity. A static observer at distance x has a = v²/x, so T_local = v/(2πx) = a/(2π) in units ħ = k_B = 1, c = v. **The Unruh form does come out of the restricted state, as the KNOWN Bisognano–Wichmann result reproduced on a lattice.**
- **Where it comes from:**
  - **Inputs:** the vacuum (ground state of a local Hamiltonian), a Lorentz-invariant low-energy limit (an invariant speed v), and a sharp read boundary.
  - **The cost side supplies only "the tracker's state is the restricted state"**, which is ordinary quantum mechanics, plus the G2 Gibbs reading in which the record is weighted e^{−β·cost}. Under that reading, β·cost = K would identify the record's cost operator with 2π × the boost generator [HYP]. That is an identification, not a derivation.
  - **[MISS]:** why a cost-limited tracker's reads end at a causal horizon. That needs light cones, i.e. relativity, as an input.
  - **[MISS]:** no link between this temperature and CT18's σ²/(2γ). They live in different units and on different flows.

## G3 foldable (future append only, after the hostile review and a fresh-clone rerun)
- The best candidate: G3-1 2D record perimeter scaling, with the WVHC bound. It is exact, small and reproducible, with the "chosen" list attached.
- G3-2: the free-energy identity and the sign reading. A short note.
- G3-3: the centre-stakes table, as a refinement of the R2.3 claim from "chosen" to "forced iff (i)–(iii)".
- G3-4: a lab note only (it reproduces a known result; no cost-side derivation).

## G3 sharpest next tests
1. A 2D qubit (non-Gaussian) record with plaquette reads, e.g. a MaxEnt fit on a 4×4 system by exact enumeration, to check that perimeter scaling isn't a Gaussian artefact.
2. Derive (ii), betting on interference, from the round-1 result that uncopyable distinctions are the ones drift moves: is there a task family where interference reads beat copyable ones on value per bit?
3. In the wedge model, check whether a *cost-optimal* finite-capacity tracker of the half chain (bounded modes) keeps the 2π slope near the cut and loses it far away. That would turn "reads stop at a boundary" into "capacity cuts reads off", a cost-side horizon [HYP].

---

# R2 errata (append-only; applies the seven corrections in HOSTILE_REVIEW_G2.md, read at 01:14 EST)
The earlier R2 text stands as written; where it conflicts with this section, this section governs. It supersedes the shorter "R2 corrections" block above where they overlap.

1. **R2.1 / R2.0, record area scaling.** "Forced by (per-bond capacity cost + local reads)" is withdrawn.
   - Corrected: **S_rec(A) ≤ |∂A|·log2 χ is a property of the chosen MPS format [PIM, trivial: the Schmidt-rank bound]. That χ* stays bounded as N grows is a [HYP].**
     - It is observed only for Haar worlds at χ ≤ 4 and N ≤ 16.
     - `r2_tracker.py`'s own J (summed capacity, averaged error) sends χ* → 1 at large N.
   - "Any tensor-network record" is false: a MERA or non-local network graph breaks the bound, so a local network is a second choice.
   - "The gap comes out for the record" (FNW) → [HYP]: FNW needs translation invariance and injectivity, neither present nor checked.
   - "Boundary scaling and a finite correlation length come out of the cost" (R2.0) → "follow from the chosen format plus a hypothesis".
   - One consistent J, χ*-against-N and non-SVD records are done in G3-1b below.
2. **R2.2 row 1.** It now reads: "same form as Jacobson 2016 eqs. 14–16 (the first-order identity of a Gibbs state); β = q/λ is a free price ratio".
   - The second-order sign item is **closed for the Gibbs step**: both are minima of a free energy, equivalently entropy maxima at a fixed constraint (confirmed in G3-2).
   - It stays an open miss for the fixed-volume geometric variation and the UV area term.
3. **R2.3 labels and citation.** The label becomes "[KNOWN] Gibbs/Donsker–Varadhan variational principle, applied; exp(−β·cost) forced **given** (KL as the selection price, a cost linear in s, a uniform base p0)". Under a χ² price the optimum is linear in cost, not exponential (reviewer D).
   - **Citation fix:** the KL selection cost is selfref **R5.1** (minimum destruction D(s‖p0), Esposito–Van den Broeck lower bound) and the **R5.5** amendment text. It is not "NA4". Repo NA4 is "the disk pays 0", amended to "pays 0 in tracking".
4. **R2.3 (c), interference readout.**
   - For SU(2), Re⟨ψ|U|ψ⟩ = ½ Re tr U holds **exactly for every probe state**; no Haar average is needed. For SU(N ≥ 3) only the Haar-averaged probe gives the fundamental character.
   - The Hadamard-test outcome probability is (1 + Re⟨ψ|U|ψ⟩)/2, which is where the ½ comes from.
   - R2.0/R2.6 now read "**given** a coherent fundamental probe and a readout linear in U": the representation is chosen through the probe and the readout's degree in U.
   - G3-3 states when that choice carries stakes.
5. **R2.2 row 2, JP-heat.**
   - "σ_M ≈ 0.79/g" holds at dE = 1 only (≈ 17/g at dE = 3).
   - Added [OBS]: the supremum over dE of the efficiency is g/(g + r) (0.3333, 0.6667, 0.9091 at g = 0.5, 2, 10). So equality needs g/r → ∞ [PIM in this two-state model].
   - The link "this is Jacobson's equilibrium input" → **[HYP]**.
6. **R2.4, underdamped CT18.**
   - The "classical KMS ⟨{x,v}⟩ = β⟨v²⟩" check is **dropped**: it is circular, since the estimator set β = 1/⟨v²⟩.
   - Non-circular check, equipartition ω²⟨x²⟩ = ⟨v²⟩ (the static FDT). Worker's numbers: 0.4938/0.4878, 1.0623/1.0669, 0.3633/0.3732. The reviewer's 400 independent chains give 0.4978±0.0042 / 0.4985±0.0029, 1.0722±0.0111 / 1.0716±0.0109, 0.3842±0.0079 / 0.3789±0.0013 against σ²/(2γ) = 0.5, 1.0667, 0.375. Consistent at ~1%; the last ⟨v²⟩ is 2.9 s.e. high, possibly integrator bias (unverified).
   - "Match: yes" → "**z² = U(B)/kT identically [PIM, an identity of definitions]; CT18's hazard form ν = F(z)/τ holds only for γ/ω → ∞ [OBS, reviewer]**: ν·τ = 0.0074, 0.0427, 0.1261, 0.1880 at γ/ω = 0.25, 1, 4, 16 with z² = 2 fixed. A second group γ/ω enters at finite friction (consistent with Kramers 1940)."
   - Thermal-time temperature = σ²/(2γ) → "[KNOWN] Einstein relation; equal to the thermal-time temperature **given** the chosen symplectic structure (x, v canonical, unit mass, drift split into H-flow plus friction)".
7. **R2.5 coverage table, corrected and split by composite.** Al-Safi–Richens 2015, NJP 17, 123001, DOI 10.1088/1367-2630/17/12/123001 (verified on Crossref by me this round). Its Thm 1 says all reversible transformations on a **max** tensor product of non-classical **dichotomic** systems are trivial, for N parts, not necessarily identical. Dichotomic includes all balls, even polygons, cubes, cross-polytopes, and the regular 3- and 4-polytopes except simplices.

| part pair | S = max | intermediate composite min ⊊ S ⊊ max |
|---|---|---|
| ball(d) × ball(d′), any d, d′ (incl. d ≠ d′) | covered, KNOWN (ASR Thm 1) | d = d′ ≠ 3: covered **under continuous reversibility + local tomography** (MMPA 2014). Discrete maps and d ≠ d′: **[MISS]** |
| ball × dichotomic polytope | covered, KNOWN (ASR Thm 1) | **[MISS]** |
| icosahedron × dodecahedron | covered, KNOWN (ASR Thm 1); ♦ fails there (Φ = +2.05), so M12 is silent, but it isn't needed | **[MISS]** |
| I×I, D×D, CO×CO | I×I, D×D covered (ASR Thm 1). CO is not dichotomic. Entangled-point search: I² −2.54, D² −0.44, CO² −1.5 (selfref R12-M.9; search, not proof) | not certified **[MISS]** |
| regular polygons (any n, m), locally symmetric, finite orbits | covered (ASR Thms 1, 3; R12 M12-P) | covered, PIM (M12-P) |
| vertex-transitive Hanner polytopes, absolutely irreducible groups | covered | covered, PIM (M11 + Hanner ⇒ (★)); a small family; products of different factors are not covered |
| 3+ dichotomic parts | covered, KNOWN (ASR Thm 1) | **[MISS]** |
| non-dichotomic parts (odd polygons with other parts, cuboctahedron, reducible parts) | partly (ASR Thm 3 for identical odd polygons) | **[MISS]** |

   - The round-2 row "best Φ = 0 for I×I, D×D, CO×CO" was misreported: those optima are pure product states (|a|² = |b|² = ‖C‖² = 1), where Φ = 0 by definition. It is withdrawn.
   - Open miss, restated: **intermediate composites and non-dichotomic parts.**

Foldable list (R2.6), corrected: R2.1 is dropped. The R2.3 lines become conditionals ("given KL", "given a fundamental probe and a linear readout"). The JP-heat line keeps "[PIM] in the two-state model; Jacobson link [HYP]".

---

# G3-1b PREREGISTRATION (written before running; locked by the sha256 recorded below)
**Question.** Under ONE consistent cost, does the optimal record's complexity stay bounded as system size grows, with no format imposed beyond what the reads fix?

**Worlds.** Gaussian fermions, both volume-scaling: (W1) a Haar-random real Slater determinant at half filling; (W2) a typical eigenstate of nearest-neighbour hopping at β = 1 occupation.
- 1D periodic chains, N ∈ {50, 100, 200, 400}.
- 2D tori, L ∈ {6, 10, 14, 20} (N = L²).
- Seed fixed per size; one world per size.

**Reads.** All two-point functions ⟨c_i†c_j⟩ with graph distance ≤ 3 (onsite included).

**Record family.** For each range r ∈ {0, 1, 2, 3}, the max-entropy Gaussian state whose two-point functions match the world's exactly within distance r. It is fitted by the convex dual. These are optimised (variational), not SVD records.
- At fixed exact range-r data it is the total-correlation-minimal state [PIM, from G3-1].
- r is the capacity knob, the analogue of χ.

**Cost (one J, both terms summed over the system).** J = κ·TC(record) + q·Σ_{reads}|C_rec − C_world|, with q = 1.
- TC = Σ_i h2(C_ii) − S(record), in bits.
- κ ∈ {3, 1, 0.3, 0.1, 0.03, 0.01}.

**Predictions.**
- **P1:** the per-site TC(r) and per-site error(r) change by < 5% between the two largest sizes, in each world and dimension.
- **P2:** r*(κ) is the same at every size N ≥ 100 (1D) and L ≥ 10 (2D), for every κ in the grid.
- **P3:** for the r* = 3 record (where r* = 3 occurs), I(A:Ā)/|∂A| over blocks (1D: lengths 4…N/4; 2D: l = 2…L/2) varies by < ±15% around its mean.
- **P4 (qubit check, non-Gaussian; Haar worlds, N ∈ {8, 10, 12, 14, 16}):**
  - Records: product (χ = 1); next-nearest Bell pairs (χ ≤ 4, the reviewer's construction); truncated SVD (χ = 2, 4, 8).
  - J = κ·Σ_b log2 χ_b + q·Σ_pairs trace-distance error.
  - Prediction: χ* ≤ 4 at every N for κ ∈ {0.3, 0.1, 0.03}. χ* = 1 for κ ≥ 1 at every N.

**Falsifier.** Any r* or χ* that rises with N at fixed κ, or per-site TC growing > 5% between the largest sizes.

**What a pass would and would not show.** A pass means the cost trade-off is intensive, so the optimal record has bounded complexity and, by WVHC, perimeter-bounded correlations. The capacity price (total correlation) and local reads are still choices. A pass says nothing about the world's own state.

**Lock:** sha256 of the section above (from its heading to the line before this one) = `0575b2ea9c37942223250ceca2ba43a4d9431a2f7df9f16ea1fb4612506e2f05`, written to `PREREG_G3-1b.sha256` before any G3-1b run.

## Erratum to §0 (hostile foundations review, 2026-11-26 ~01:40 ET; line 11 left as written)
`:11` "the record-cost idea, which already points toward quantum structure" overstates it. Corrected: "the record-cost idea, which ranks quantum-like records cheapest in toy models *only under the continuous-drift premise CD*; without drift it ranks classical or polytope records cheapest." The forces and gravity rounds also take quantum mechanics as an input (TFIM and free-fermion states, Henderson–Vedral, Bloch records, Bisognano–Wichmann), so nothing here derives QM or gravity. This NOTE is not in the repo.

## G3-1b RESULTS (run after the lock; the prereg section re-hashes to the locked sha256, checked 01:29 EST)
Files: `scripts/g3_1b_prereg.py` → `outputs/g3_1b.txt`, `outputs/g3_1b_raw.json`; `scripts/g3_1b_p4_qubit.py` → `outputs/g3_1b_p4.txt`. Sizes run as preregistered: 1D N = 50…400 and 2D L = 6…20 (N = 400 modes). Every exact-range fit reproduces its constraints to ≤ 7e−6. There were overflow warnings in exp for strongly fitted h; the fit residuals stay small.

**Scored strictly against the prereg [OBS]:**

| prediction | W1 (Haar Slater) 1D | W1 2D | W2 (typical eigenstate) 1D | W2 2D |
|---|---|---|---|---|
| P1: per-site TC and error change < 5% between the two largest sizes | **FAIL** (TC 50–53%, err 32–69%) | **FAIL** (TC 53–54%, err 9–31%) | **FAIL** (TC 32%, err 10–13%) | **FAIL** (TC 3–10%, err 6–33%) |
| P2: r*(κ) the same at all N ≥ 100 / L ≥ 10 | **FAIL**: at κ = 3, r* = 0 (N=100) → 3 (N=200, 400). That rises with N, so **the falsifier is triggered** | **FAIL**: κ = 3, r* = 0 (L=10) → 3 (L=14, 20); **falsifier triggered** | PASS: [0,0,3,3,3,3] at N = 100, 200, 400 | PASS: [0,3,3,3,3,3] at L = 10, 14, 20 |
| P3: r = 3 record I/∣∂A∣ within ±15% | FAIL (max dev 214%; values 0.003–0.043) | FAIL (31%) | FAIL, marginal (15.7%) | PASS (6.5%) |
| P4 (qubit, Haar): χ* ≤ 4 at every N for κ ∈ {0.3, 0.1, 0.03}; χ* = 1 for κ ≥ 1 | — | — | — | **FAIL at κ = 0.03, N = 8, 10** (χ* = SVD χ=8). Passes for N = 12, 14, 16 and for every other κ; χ* = 1 at κ ≥ 1 at all N. The falsifier (χ* rising with N) is **not** triggered: χ* falls from 8 to ≤ 4 |

**Prereg outcome: FAILED as written.** P1 fails everywhere, P2 and P3 fail for the Haar world, and P4 fails at small N. This is logged as data. The predictions are not patched.

**What the numbers show (post hoc, labelled; not a rescue of the prereg):**
- [OBS] **Per-site record cost never grows with size.** TC/site for the exact r = 3 record:
  - W1 1D: 0.084, 0.047, 0.024, 0.011.
  - W1 2D: 0.70, 0.20, 0.096, 0.045.
  - W2 1D: 0.18, 0.31, 0.34, 0.23.
  - W2 2D: 0.97, 0.59, 0.51, 0.46.
  - The world's own entropy grows with volume throughout (2D, largest block: W1 79.75 bits for 100 sites, W2 49.41).
- [HYP, diagnosis] The Haar world fails P1/P2 because its local correlations are not intensive. Per-site read error of the r = 0 record falls by about 1/√2 per doubling (0.165, 0.124, 0.089, 0.061). So "κ fixed" means a different relative price at each N, and r* moves. The physical eigenstate world W2 has nearly intensive local data, and there r* is stable (P2 pass) and the record's perimeter profile is flat in 2D (P3 pass, 6.5%).
- **Built into the design (reviewer-style caveat):** the record family is capped at r ≤ 3 = read range, so "bounded complexity" in r is automatic. What the test could decide is intensivity, and that is what failed.

**Restated claim, with every choice named:**
- Given (i) local two-point reads of range R, (ii) capacity priced as total correlation, (iii) records from the max-entropy family fitted to those reads, and (iv) a world whose local data are intensive (W2 type):
  - the optimal range r* is size-independent [OBS, 1D N ≤ 400, 2D L ≤ 20];
  - and the record's mutual information follows the perimeter [OBS; WVHC bound, KNOWN].
- For a Haar world, (iv) fails and the preregistered stability fails with it. **[MISS]:** a version that prices relative to the world's own correlation scale would need a new prereg.

---

# G3 status after the hostile review (01:30 EST)
- G3-1 (2D perimeter scaling of the MaxEnt record) stands as [OBS] with its choices listed. It answers the format objection in part: here the record's locality comes from the read pattern, as Lagrange multipliers on the reads, not from an imposed bond structure.
- G3-1b's preregistered stability test **failed as written**; see above.
- G3-2, G3-3 and G3-4 already name their choices. G3-3's "forced iff (i)–(iii)" rests on the chosen bet set, (ii) interference reads, and on a probe in the fundamental representation, (i).

---

# Round G4 (Thu 26 Nov 2026, from 01:30 EST): does pricing capacity alone produce a horizon?

## G4-1 PREREGISTRATION (primary; written before any G4 code was run; hash-locked below)
**Question.** A tracker has stakes on its own small region and may read any part of the world. Its only restriction is a priced capacity. Does its optimal record end at an effective read boundary that behaves like a horizon?

**Declared inputs (not tested):** the vacuum, i.e. the ground state of the half-filled nearest-neighbour hopping chain (a lattice Dirac fermion; relativity enters as its low-energy Lorentz invariance with v = 2); Gaussian records; the stake region.

**World.** Periodic chain, N = 600 sites. Variants: massless (m = 0), and gapped with a staggered mass m = 0.3.

**Tracker.** Stake region T = 5 consecutive sites centred at site 300. Value of a record R = q·I(T : R) in bits, q = 1.

**Capacity pricing, two schemes (both declared now):**
- **Scheme B (PRIMARY, basis-free):** the record holds K single-particle modes supported outside T, at cost κ·K. Family: the K partner modes of T with the largest mode-wise entanglement (Botero–Reznik mode-wise decomposition of a pure Gaussian state). That this family is the optimum for I(T:R) at fixed K is a [HYP] that I am not testing. K* = the number of partner modes whose marginal value 2·h(ν_k) exceeds κ.
- **Scheme A (SECONDARY, per-site pricing, a locality choice):** the record holds the world's reduced state on a site set S outside T, at cost κ·|S|. S is built greedily: at each step, add the site within distance 150 of the centre with the largest gain in I(T : S); stop when the best gain < κ. The tracker's state is the reduced state on T∪S.

**κ grid (bits):** {0.3, 0.1, 0.03, 0.01, 0.003, 0.001}.

**Horizon criteria, fixed in advance:**
- **H1 (sharp cut).**
  - The weight profile is w(x): the indicator of T∪S in scheme A, and the indicator of T plus Σ_k |φ_k(x)|² over the record modes in scheme B.
  - r90 and r99 are the smallest radii about the centre holding 90% and 99% of Σw.
  - **Pass iff r99 − r90 ≤ 3 sites**, and, in scheme A only, T∪S fills ≥ 80% of its hull. Evaluated at κ = 0.001 (largest records).
- **H2 (modular Hamiltonian linear in distance near the cut).** Evaluated only where H1 passes.
  - Take the single-particle modular Hamiltonian k = ln((1−C)/C) of the tracker's state.
  - Read the nearest-neighbour coefficients |k_{e−d, e−d−1}| at d = 0, 1, 2 bonds inward from the hull edge e, and fit them linearly in (d+1).
  - **Pass iff the slope is within ±15% of 2π/v (v = 2) and R² ≥ 0.98**, at κ = 0.001 and at both hull edges.
- **H3 (temperature tied to the capacity price).**
  - The hull half-width R(κ) must be non-increasing in κ and take ≥ 3 distinct values over the grid.
  - The centre modular temperature T_c(κ) = 1/|k_{c,c+1}| (c = centre bond) must strictly increase with κ over ≥ 3 consecutive grid steps.
  - The log–log slope α of T_c against κ, fitted on the lower and the upper halves of the grid, must agree within 20%.
  - In scheme B, R(κ) is the r90 of the record profile.

**Outcome rule (no rescue):**
- **Horizon-like from capacity alone = H1 ∧ H2 ∧ H3 in scheme B, for m = 0.**
- If any of them fails, it is an open miss for "the cost supplies a horizon".
- Scheme A results are reported, but **cannot** turn a miss into a pass, because per-site pricing is a locality choice.
- For m = 0.3 the same criteria are scored and reported. Saturation of R(κ) there is scored as an H3 fail, not explained away.

**Stated expectations (for honesty, not as tests):** I expect scheme B to fail H1, since partner modes of a critical vacuum have power-law tails. I expect scheme A to pass H1 and H2 roughly, and H3 for m = 0 only. If so, the sharp cut comes from per-site pricing (a choice), not from capacity as such.

## G4-2 PREREGISTRATION (secondary): intensivity with cost in one currency
**Declared up front: this choice was made after G3-1b failed.** G3-1b's J added total correlation, in bits, to the absolute amplitude error |ΔC| of the reads, which has no informational unit.

**First-principles justification (not a fit).** The theory prices judgment in one currency: the capacity term κ·I is in bits, so the error term must also be the information lost, in bits. The read-error term becomes the relative entropy D(ρ_world,read ‖ ρ_record,read) of each read's reduced state, summed over reads. This is the stake measured as the log-loss excess of a reader who uses the record in place of the world, the standard operational meaning of KL. It makes J invariant to rescaling the observable's units, which |ΔC| is not. Neither the data nor the G3-1b outcome enters the choice of KL over |ΔC| beyond exposing the unit mismatch.

**Setup.** As G3-1b: same worlds W1 and W2, seeds, sizes (1D N = 50…400; 2D L = 6…20), reads (two-point, distance ≤ 3) and MaxEnt record family r ∈ {0, 1, 2, 3}.
- **Change:** each read pair (i, j), and each onsite i, contributes the relative entropy (bits) between the world's and the record's Gaussian reduced states on {i, j} (on {i}).
- J = κ·TC + q·Σ_reads D, with q = 1. κ grid {3, 1, 0.3, 0.1, 0.03, 0.01}.

**Predictions.**
- **Q1:** r*(κ) is identical at every size with N ≥ 100 (1D) and L ≥ 10 (2D), in both worlds and for every κ.
- **Q2:** the crossover prices κ_c(r) = (D_r − D_3)/(TC_3 − TC_r) for r = 0, 1, 2 change by < 10% between the two largest sizes, in both worlds and dimensions.

**Falsifier:** any r* that changes with N at fixed κ (in either direction), or any κ_c(r) changing by ≥ 10%.

**Caveat declared now:** the record family is capped at r = 3 = read range, so bounded r is built in. Only intensivity, the size-independence of the trade-off, is tested.

**G4 lock:** sha256 = `504704d9c8433cc6e010b5a28c89f06523c5fb8eda3fcec128381680b39ddf8b` (G4-1 and G4-2 together), in `PREREG_G4.sha256`, written before any G4 run.

## G4-1 RESULTS (run after the lock; the lock re-hashes intact, checked 01:48 EST)
Files: `scripts/g4_1_horizon.py` → `outputs/g4_1.txt`, `outputs/g4_1_raw.json`. Scored strictly against the prereg [OBS].

**Scheme B (PRIMARY: capacity priced per mode, basis-free), m = 0:**
- Mode values 2h(ν) = 1.9999, 0.785, 0.761, 0.049, 0.046 bits.
- **H1 FAILS at every κ**: r90 = 6–8 sites but r99 = 50–76 sites. The top partner mode has a power-law tail: weight beyond r = 5, 10, 20, 40, 80, 160 is 0.33, 0.12, 0.059, 0.029, 0.014, 0.0056, halving per doubling, i.e. ~1/r.
- H2 is not evaluable, so it fails.
- **H3 FAILS**: R(κ) takes only 2 values (6, 8), because K* is capped at |T| = 5 modes, and T_c takes 2 values.
- **Outcome by the prereg's rule: open miss.** Pricing capacity alone, in a basis-free way, does **not** give the tracker a read boundary. The cheapest record is a handful of partner modes spread over the whole vacuum with ~1/r tails.
- Massive (m = 0.3): H1 also fails (r99 − r90 = 4–6, with exponential tails 0.18, 0.015, 0.0004, 0 beyond r = 5, 10, 20, 40). H3 fails the same way.

**Scheme A (SECONDARY: capacity priced per site, a locality choice; cannot turn the miss into a pass):**
- **H1, m = 0:** passes for κ ≥ 0.01, with filled hulls (half-widths 3, 5, 9, 15) and r99 − r90 ≤ 1. It **fails at the scored κ = 0.001**: the greedy edge is ragged (fill 0.979, r99 − r90 = 5). The greedy adds sites in ± pairs (first sites +3, −3, −4, +4, …). At large radius it skips some, a parity effect of half filling (C_{0,2k} = 0) [HYP].
- **H1, m = 0.3:** passes at every κ (fill 1.0).
- **H2, m = 0:** not evaluable at κ = 0.001 (edge sites missing), so it fails.
- **H2, m = 0.3: PASSES at both edges.** Coefficients 3.124, 6.240, 9.321; slope/(2π/v) = 0.986; R² = 0.99999. This is the Bisognano–Wichmann form at a cut the tracker chose by pricing.
- **H3, both masses:** R(κ) is monotone with 6 distinct values (m = 0: 3 → 48, R ∝ κ^−0.49; m = 0.3: 3 → 16, R ∝ κ^−0.28), and T_c strictly increases with κ. But the log–log slopes of T_c disagree between halves: α = 0.45 vs 0.04 (m = 0) and 0.35 vs 0.04 (m = 0.3). **H3 FAILS.**
  - Post-hoc diagnosis [HYP]: the centre coefficient saturates near 21 (1/T_c → 0.046). That is the same double-precision ceiling of ln((1−C)/C) seen in G3-4, so T_c as defined is not a sound metric at large R. That is a design flaw of the prereg, logged rather than repaired here.

**What this says, with choices named:**
- [OBS] With capacity priced basis-free (modes), the cost supplies **no** horizon. That is the cost-native answer and it is negative.
- [OBS] With capacity priced per site, a sharp cut does appear, its location set by the price: R ∝ κ^−0.49 in the critical vacuum, and in the gapped vacuum the modular Hamiltonian at the cut matches BW to 1.4%.
  - The cut rests on per-site pricing, i.e. storage localized in space.
  - The linear-in-distance modular form rests on the vacuum (an input), as in G3-4.
  - So **the cost supplies where the boundary sits (a length set by κ); locality and the vacuum supply that it looks like a horizon.**
- The temperature–price link is not established (H3 fail). A cleaner test is below.

## G4-2 RESULTS (same lock)
Files: `scripts/g4_2_intensivity.py` → `outputs/g4_2.txt`, `outputs/g4_2_raw.json`.

| | W1 (Haar) 1D | W1 2D | W2 (eigenstate) 1D | W2 2D |
|---|---|---|---|---|
| Q1: r* the same at N ≥ 100 / L ≥ 10 | **PASS** [0,0,3,3,3,3] | **PASS** | **PASS** | **PASS** |
| Q2: κ_c(r) change < 10% (two largest sizes) | **PASS** (0.45%, 0.59%, 0.83%) | **PASS** (2.3%, 2.8%, 3.7%) | **FAIL** (4.3%, **31%**, **25%**) | **FAIL** (5.9%, 1.3%, **11.4%**) |

- **Outcome: Q1 passes everywhere; Q2 fails for W2, so the falsifier is triggered.** With error priced in bits, the record's optimal range is size-stable in all four cases, including the Haar world that failed G3-1b. But the crossover prices are not fully size-stable for the physical eigenstate world at these sizes.
- Post-hoc observation [OBS → HYP]: for the Haar world κ_c → 1.00 bit per bit (0.996, 0.994, 0.992 in 1D; 0.98 in 2D). With weak correlations, the bits lost by dropping a correlation equal the bits of total correlation saved, so in one currency the crossover price is ≈ 1. That would make the trade-off unit-free [HYP]. W2's lower and drifting κ_c (0.49–0.94) shows it does not hold for strong correlations.

## G4 status
- Non-Gaussian record: skipped (not cheap).
- Next tests:
  1. A precision-safe H3, e.g. mpmath at 50 digits, or edge-referenced coefficients, as a new prereg: is the centre modular temperature of the per-site record ∝ κ^{1/2}, as BW for an interval of half-width R ∝ κ^{−1/2} would imply? [HYP]
  2. Is there any basis-free capacity price under which a cut emerges, e.g. pricing the *spatial spread* of a mode? That would be a locality choice under another name; it should be named as such.
  3. Larger sizes for W2 Q2.

---

# Round G5 (Thu 26 Nov 2026, from 01:40 EST): precision-safe H3

## G5 PREREGISTRATION (written before any G5 code was run; hash-locked below)
**Question.** Under per-site capacity pricing (scheme A of G4-1, a declared locality choice), does the tracker's centre modular temperature scale as κ^{1/2}?

**Changes from G4-1, declared:**
- (i) The world is the **infinite** chain, so C is known in closed form to arbitrary precision.
  - Massless: C_ij = ½δ_ij + sin(π(i−j)/2)/(π(i−j)), with the sign convention fixed by the half-filled ground state of H = −Σ(c_i†c_{i+1} + h.c.).
  - Gapped (staggered mass m = 0.3): C = ½(1 − H·(H²)^{−1/2}), with (H²)^{−1/2} translation-invariant of symbol (4cos²k + m²)^{−1/2}, evaluated by mpmath quadrature.
  - Both are checked against double-precision C on the N = 600 ring at distances ≤ 5, with agreement required to 1e−6. If the check fails, the run stops and that counts as a miss of the setup, not a result.
- (ii) Site selection: the same greedy rule as G4-1 scheme A (stake region T = 5 sites, candidates within 150 sites, gain in I(T : S) in bits). It runs in double precision, since the gains are ≥ 1e−3 and not precision-limited. The C used is the infinite-chain closed form.
- (iii) **Metric:** the modular Hamiltonian k = ln((1−C_U)/C_U) of the tracker's state on U = T∪S, computed with mpmath at **60 digits**. Precision control: the largest U is recomputed at 90 digits, and the centre coefficients must agree to 1e−10.
  - β_c = |k_{c,c+1}| at the centre bond (sites 0 and 1 of T, centred at 0).
  - T_c = 1/β_c.
  - R_eff = (hull length of U)/2.

**κ grid:** {0.3, 0.1, 0.03, 0.01, 0.003, 0.001} bits per site, as in G4-1.

**Predictions:**
- **P5a (critical, m = 0):** the log–log slope of T_c against κ over the full grid lies in [0.35, 0.65], and the lower-half and upper-half slopes agree within 20%.
- **P5b (critical, BW-interval consistency):** for κ ≤ 0.03, T_c·R_eff lies within ±15% of v/π = 2/π. This is the Bisognano–Wichmann/Casini–Huerta centre value for an interval, β(centre) = π·R_eff/v.
- **P5c (gapped, m = 0.3):** the same test as P5a. **Stated expectation:** fail, because the gapped R(κ) grew only as κ^−0.28 in G4-1 and the centre temperature of a gapped interval need not follow BW. A pass would be reported as unexpected.

**Falsifiers:** a slope outside [0.35, 0.65]; half-slopes differing by ≥ 20%; P5b off by more than 15% at any κ ≤ 0.03; a failed precision control (the run counts as a miss).

**Optional, only if cheap (≤ 20 min wall):**
- **Q2-ext:** the G4-2 eigenstate world W2 in 1D at N = 800, compared with N = 400. κ_c(r) must change by < 10% for r = 0, 1, 2.
- If it doesn't finish in 20 min, it is recorded as "not run".

**What a pass would and would not mean:** a pass ties the tracker's modular temperature to its capacity price (T_c ∝ κ^{1/2}) *given* per-site pricing and the critical vacuum. It would not supply relativity, the vacuum, T = a/2π as a physical temperature, or G.

**G5 lock:** sha256 = `419a6a681ec48bf8e9371f3ae3d852d87f414dd11d99d9e3cccc7105ff61b0d6`, in `PREREG_G5.sha256`, written before any G5 run.

## G5 RESULTS (run after the lock; all three locks re-hash intact, checked 02:05 EST: G3-1b `0575b2ea…`, G4 `504704d9…`, G5 `419a6a68…`)
Files:
- `scripts/g5_h3.py` → `outputs/g5_h3.txt`, `outputs/g5_h3_raw.json` (preregistered run)
- `scripts/g5_q2ext.py` → `outputs/g5_q2ext.txt` (optional Q2-ext)
- Post-hoc, unscored: `scripts/g5_h3_posthoc_m0.py`, `scripts/g5_h3_posthoc_m0_hiprec.py` → `outputs/g5_h3_posthoc_m0*.txt`

**Scored strictly against the prereg [OBS]:**

| prediction | outcome |
|---|---|
| Setup check, m = 0 (closed form vs N = 600 ring, ≤ 1e−6) | **FAILED: max dC = 1.67e−3.** By the prereg's rule the run stopped: **P5a and P5b are a setup miss, not scored.** |
| Setup check, m = 0.3 | passes (2.3e−15) |
| Precision control, m = 0.3 (90 vs 60 digits) | passes (difference below double resolution) |
| **P5c (gapped): slope in [0.35, 0.65], halves within 20%** | **FAIL, as stated in advance.** Full slope 0.271; upper half 0.348, lower half 0.198 (55% apart). R_eff ∝ κ^−0.263. |
| **Q2-ext (W2 1D, N = 400 → 800): κ_c(r) change < 10%** | **PASS:** 0.96%, 4.1%, 5.6% (r = 0, 1, 2). Ran in under 20 min. |

**Diagnosis of the setup miss** [OBS + KNOWN], post hoc:
- The reference was the wrong one, not the closed form. On a periodic ring with N = 600, the modes k = ±π/2 sit at exactly E = 0. The rule "occupy E < 0" leaves both empty, so the ring holds 298 particles, not 300, which gives a 1/N difference.
- An antiperiodic ring (no zero modes) agrees with the closed form to 7.3e−6 at N = 600 and 7.3e−8 at N = 6000 (1/N² finite size).
- So the prereg's 1e−6 tolerance against N = 600 was unattainable for a gapless world. That is a design flaw, logged.
- **Erratum to G4-1 (append only):** G4-1's massless world was this 298/600 ring. The centre values hardly move: T_c at κ = 0.03 is 0.06292 in G4-1 against 0.06298 on the exact chain. The ragged κ = 0.001 edge recurs on the exact chain (|U| = 95 in a hull of 97). So the G4-1 m = 0 scores stand.
- Second design flaw: 60 digits are too few for the massless κ = 0.001 set. The eigenvalues come within 1e−71 of 0 or 1, and at 60 digits one goes negative. The preregistered precision control would have failed there too.

**Post-hoc massless diagnostic (NOT preregistered, NOT scored):**
- Setup: exact infinite chain, antiperiodic N = 6000 reference, 150 digits, control at 200 digits.
- [OBS] T_c = 0.1779, 0.1104, 0.0630, 0.0384, 0.0217, 0.0125 for κ = 0.3 … 0.001.
- [OBS] Log–log slope 0.465; halves 0.451 and 0.487 (7.7% apart).
- [OBS] T_c·R_eff = 0.623, 0.607, 0.598, 0.595, 0.617, 0.606, against the BW-interval value 2/π = 0.637 (within 4–7%).
- Had these been the scored numbers, P5a and P5b would pass. They are not scored, and the prereg is not patched.
- [OBS] Gapped: T_c·R_eff stays at 0.515–0.544, near-constant but 15–19% below 2/π. So in both vacua **T_c ≈ c/R_eff**: the price sets R, and R sets T. In the gapped chain the exponent is R's own (≈ 0.27), not ½.

**What G5 establishes, with choices named:**
- Under per-site pricing (a locality choice) in the critical free-fermion vacuum (an input), the tracker's centre modular temperature follows its price as T_c ∝ κ^{≈0.47}. The mechanism is T_c ≈ (2/π)·v/(2·R_eff) with R_eff ∝ κ^{−0.46} [OBS, post hoc only].
- The κ^{1/2} is not universal. In the gapped vacuum it is κ^{0.27} [OBS, scored fail as predicted].
- So the cost places the boundary, and the boundary sets a modular temperature. The exponent comes from the vacuum's correlations, not from the cost.
- None of this is T = a/2π: there is no acceleration, no clock and no ħ/c, and the "temperature" is the modular one of the tracker's own state [MISS].
- **H3 status:** an open miss as preregistered (setup miss plus gapped fail). Post-hoc evidence favours the critical-case scaling, and that needs a clean new prereg if anyone wants it scored.

---

# Errata from HOSTILE_REVIEW_G3G5 (append-only; review written 26 Nov 2026, ~02:25 EST; earlier text stands as written, and where it conflicts with this section, this section governs; locked prereg spans untouched)
- **E-G3G5-1 (H1).** The THREAD_SUMMARY bottom-line item "Through R that boundary sets the tracker's modular temperature, T_c ≈ c/R" and the NOTE heading "What G5 establishes" are corrected.
  - Under per-site pricing the price sets a stopping radius R(κ), where the marginal mutual information of the next site falls below κ [OBS].
  - Post hoc and unscored, the critical vacuum gives T_c·R_eff ≈ 0.60 against the BW interval value 2/π [OBS, post hoc only].
  - The R → T step is the vacuum's (BW/Hislop–Longo for an interval, an input; Hislop & Longo 1982, DOI 10.1007/BF01208372, Crossref-verified). The κ exponent of R comes from the vacuum's correlation decay. The cost supplies only where the stop falls.
  - Read "What G5 establishes" as "What G5 scored (P5c fail, m = 0 setup miss, Q2-ext pass) and what it suggests post hoc".
  - "T_c ≈ c/R in both vacua" is withdrawn for the gapped case: T_c·R_eff drifts 0.544 → 0.515 over R_eff = 3.5–16.5, with ξ ≈ 6.7.
- **E-G3G5-2 (H2).** "So the ring holds 298 particles, not 300" is withdrawn.
  - On the periodic N = 600 ring, eigh returns the two E = 0 modes at about ±1e−16. "E < 0" occupies one of them, so the ring holds 300 particles. The occupied zero mode is a standing wave, which gives a staggered density C_ii − ½ = ∓1/N and broken translation invariance at O(1/N). That is the logged 1.67e−3 = 1/N. In exact arithmetic "E < 0" would give 299.
  - The setup-miss ruling and "tolerance unattainable at N = 600" stand: an antiperiodic N = 600 ring with exactly 300 particles still differs by 7.3e−6.
  - This applies equally to the "298/600" in ATTEMPTS (G5), THREAD_SUMMARY (G5 row and Fails list) and WORKLOG (01:52).
  - Evidence: `review_g3g5/zero_mode_check_out.txt`.
- **E-G3G5-3 (H3).** The G4-1 erratum "scores stand" is confirmed by a full rerun on the antiperiodic N = 600 world (`review_g3g5/g4_1_anti.txt`). All scored outcomes are unchanged. Descriptive changes:
  - Scheme A m = 0 H1 passes for κ ≥ 0.003, not only κ ≥ 0.01. At κ = 0.001 it gives fill 0.960 and r99 − r90 = 7, still a fail.
  - The scheme B partner-mode values 0.7849/0.7608 become a degenerate 0.7728 pair.
- **E-G3G5-4 (M1).** W2 is one random Fermi-weighted occupation per size.
  - Across 5 seeds (W2 1D), κ_c(1) spans 0.58–0.79 at N = 200 and 0.54–0.76 at N = 400, and TC/site (r = 1) spans 0.20–0.34 (`review_g3g5/q2_seed_noise_out.txt`).
  - So the G4-2 Q2 W2 FAIL and the G5 Q2-ext PASS both lie within sample noise. The scores stand as preregistered but say nothing about size dependence.
  - G3-1b's diagnosis "W2 has nearly intensive local data" and restated condition (iv) "(W2 type)" are downgraded to [HYP], untested per sample. A seed-averaged test needs a new prereg.
- **E-G3G5-5 (M2).** "With capacity priced per site, a sharp cut does appear … R ∝ κ^−0.49 in the critical vacuum" is corrected.
  - The cut is sharp in the gapped vacuum at every κ. In the critical vacuum it is sharp only at unscored κ ≥ 0.01 (κ ≥ 0.003 on the zero-mode-free world). At the scored κ = 0.001 the critical edge is ragged and H1 fails.
  - The −0.49 fits the hull half-width, ragged points included.
  - The same correction applies to THREAD_SUMMARY's G4 row ("sharp cut … (critical)").
- **E-G3G5-6 (M3).** The stated time "02:05 EST" is wrong. It appears in the G5 RESULTS heading above, in the ATTEMPTS G5 heading and in the THREAD_SUMMARY locks line.
  - Those files were last written at 01:52:47 and 01:53:19, so the re-hash check happened at or before 01:53. The reviewer re-verified all three hashes at ~01:57.
  - "checked 01:48 EST" in the G4-1 RESULTS heading cannot be verified.
  - "~01:40" in the Erratum §0 heading conflicts with WORKLOG's 01:33.
  - The run durations in ATTEMPTS ("~12 min", "~15 min", "~5 min") and here ("under 20 min") are overstated. File times give 4 s, 3 s, 10 s and 6 s.
  - For timing evidence use file birth/mtimes and WORKLOG lines. Every lock predates its run by file birth time (+30 s, +13 s, +32 s).
- **E-G3G5-7 (M4).** G4-2 Q1's pass is low-power.
  - The κ grid has no point in (0.3, 1). Every κ_c at N ≥ 100 lies in (0.41, 0.996), and r* ∈ {0, 3} only.
  - Read Q1 as "κ_c stays inside (0.3, 1)". For W1, κ_c(0) = 0.9956 is 0.4% from the grid point κ = 1.
- **E-G3G5-8 (L1).** Three wording fixes in G3-4 and G3.0:
  - The G3-4 heading reads "Restricted-vacuum check of the BW/Unruh form (no cost-side input)".
  - In G3.0, "exactly 1/(2π)" becomes "1/(2π) to 0.2–0.8% at the cut (x ≤ 3 bonds), the KNOWN BW value".
  - In the G3-4 Reading line, "T_local = v/(2πx) = a/(2πv)", which equals a/(2π) only in units with v = 1. The script uses v = 2.
- **E-G3G5-9 (L2).** In G3-2, the identity F_K(ρ′) − F_K(ρ) = T·D(ρ′‖ρ) is the Gibbs variational principle [KNOWN], not [PIM].
  - "So the sign Jacobson's maximum needs is the sign our D-term carries" becomes "both signs are the positivity of a relative entropy (Klein's inequality)".
  - The link to Lashkari et al. 2016 is one of form only.
- **E-G3G5-10 (L3).** Two narrowings in G3-3:
  - In (i), "spin-½ probes" becomes "half-integer-spin probes (only spin-½ was sampled)".
  - In the PIM line, "a read linear in U" becomes "a read of odd degree in U".
  - The same applies to THREAD_SUMMARY's G3 row ("only for spin-½ probes").
- **E-G3G5-11 (L4).** `outputs/g3_2d.txt` (L = 14, written 01:05:03) predates the current `g3_2d_record.py` (saved 01:05:46).
  - The current script gives different L = 14 numbers, with positive area parts in the eigenstate joint fit (+0.82, +0.33, +0.32 at l = 7 against perimeter parts of 5.8, 7.6 and 9.9). So the sign of the small area term is not stable in L.
  - The L = 20 Slater R = 2 fit leaves +0.19 against a perimeter part of 0.49, which was not reported above.
  - The headline "I/(4l) roughly flat" [OBS] stands.
- **E-G3G5-12 (L5).** In non-locked text, read "power-law tail" as "algebraic (~1/r) tail". The phrase in the locked G4-1 prereg stays as written.
- **E-G3G5-13 (L6).** Smaller corrections:
  - Gapped T_c·R_eff is 14.6–19.1% below 2/π.
  - R exponents, by definition: G4-1 hull half-width κ^−0.49 (m = 0) and κ^−0.28 (m = 0.3); G5 R_eff κ^−0.46 (m = 0, post hoc) and κ^−0.26 (m = 0.3, scored).
  - Scheme B's H3 could take at most ~3 R values by construction (K* ≤ |T| = 5).
  - Chosen inputs to add for G4/G5: the greedy selection rule, the 5-site stake region and the centre-bond T_c metric.
- **Review bottom line:** no lock is broken and no prediction or threshold was changed. All scored numbers reproduce from a fresh copy. The thread's preregistered outcomes all stand.
- **Reruns completed, no change (02:45 EST).** The full `g5_h3.py`, `g3_2d_record.py 20` and the 15-row W2 seed run all finished. The first two are identical to the worker's outputs. The seed run supports E-G3G5-4 (κ_c(1) spans 0.62–0.73 at N = 800, relative sd 7–15% at every size). No finding or erratum changes. See HOSTILE_REVIEW_G3G5.md §8.
