# Step-back investigation (Thu 26 Nov 2026, from 06:16 ET). Private R&D notes; nothing here is committed to the repo.

Labels: **PIM** proved in model · **OBS** observed (numerical or in our own records) · **HYP** hypothesis · **KNOWN** published, DOI checked on Crossref this session (`crossref_stepback*.txt`) · **CHOSEN** an input put in by hand · **open miss**.
Sources read: fresh public clone of the fork branch at 04c8309 (`/workspace/stepback-src`, read only), THEORY.md, CORE.md, README.md, measurement/CLAIM_MAP_v2.md, theory/*, commit 4741761, and the notes in `/workspace/gtao-notes/rnd/*`. No repo commit, no email, no edits to THEORY.md, CORE.md or any locked file.

Why this exists: Chad (t136u) said the misses look counterintuitive, that temperature was already shown via an economics paper, that we "have entanglement", and that the hunt is a search problem. The brief: take seriously that the misses may hide a modelling error, but use judgment.

---

## 1. What was actually claimed before

### 1a. Temperature: there are three different "temperatures" in the record, and H3 tested a fourth thing

| # | object | where | status | what it is |
|---|---|---|---|---|
| T1 | **CT18 "temperature" z⁻¹ = σ√τ/B** (shock over buffer) | THEORY.md B.6 (:392), CLAIM_MAP CT18, CT25 | **PIM** (Buckingham-π; hazard ν = F(z)/τ) | A dimensionless stress ratio. THEORY.md :195 credits Drăgulescu & Yakovenko 2000 "Statistical mechanics of money" (EPJ B 17:723, 10.1007/s100510070114, KNOWN) **as an analogy only**. Real-system lead prediction K4 is PROXY-FAIL. |
| T2 | **Selection temperature 1/β in π ∝ e^{−βJ}** | CLAIM_MAP R1 (SA1), U1 (CA1); G2 | **PIM** in the stated classes | The Boltzmann/logit form. Same formula as rational-inattention logit: p(a∣s) ∝ p(a)·e^{u(a,s)/λ}, where λ = price of one nat of information (Sims 2003, 10.1016/S0304-3932(03)00029-1; Matějka & McKay 2015, AER, 10.1257/aer.20130047; Ortega & Braun 2013, 10.1098/rspa.2012.0683; all KNOWN). **This is the "temperature = price of information" identity, and it is established** (prior art plus our in-model versions). |
| T3 | **Gibbs variational identity** F_K(ρ′) − F_K(ρ) = T·D(ρ′‖ρ) | G3-2 (rnd/forces-gravity) | **PIM, KNOWN** (Gibbs variational principle; Jaynes 1957, 10.1103/PhysRev.106.620) | At first order this is the "first law of entanglement" δS = δ⟨K⟩. |
| — | **H3 (G4/G5): does a capacity price κ set a *physical* modular temperature T_c(κ) ∝ κ^{1/2} in a lattice vacuum?** | NOTE.md G4-1 :381, G5 :461–530 | **open miss** as preregistered | A test of a *geometric* (Bisognano–Wichmann / Unruh-type) temperature, not of T1–T3. |

**Answer to "is the formula identity already shown?"** Yes, in the sense of T2/T3: the inverse temperature in a Boltzmann/logit/Gibbs form is the shadow price of information (or of whatever constraint the entropy is traded against). That is KNOWN in economics and physics and proved in our model classes. It proves a *form*: optimal choice under a per-nat information price is exponential in the cost, with temperature equal to the price. It does **not** fix the *value* of any physical temperature (no ħ, c, acceleration), and it does not by itself say anything about horizons.

**Why H3 was scored an open miss, and did we test the wrong thing?** Partly, yes:
1. **Different object.** H3 asked whether the storage price per site, κ, sets the vacuum's modular temperature with a ½ exponent. The identity in T2/T3 says the multipliers of the *read constraints* are the coefficients of the modular Hamiltonian (Jaynes MaxEnt: ρ = e^{−Σλ_i O_i}/Z, so K = Σλ_i O_i). So the matching comparator for "same formula" is the shadow price of the local energy read at distance x, β(x) = λ(x), not the storage price κ. In the vacuum, BW says β(x) = 2πx/v: the Unruh profile is a **price profile** in this language [HYP reading; the profile itself is the vacuum's, an input]. H3 compared κ with T_c through two steps (κ → radius R → BW temperature), and the second step belongs to the vacuum (E-G3G5-1).
2. **Setup, not world.** The m = 0 run stopped on a wrong reference ring (zero modes; tolerance unattainable), and 60 digits were too few. Post hoc, on the exact chain at 150 digits, the critical case gives slope 0.465 (halves 7.7% apart) and T_c·R_eff within 4–7% of 2/π [OBS, post hoc, unscored]. Had those been the scored numbers, P5a/P5b would have passed.
3. **Wrong comparator for the gapped case.** A gapped vacuum has a length ξ, so a pure power-function scaling was never expected; the prereg said so (P5c "expected fail").
Net: the "miss" is a setup miss plus an expected fail. A clean re-run would very likely be a hit, and **even a hit would show only that the cost places the boundary while the vacuum sets the temperature**. Plain reading: temperature-as-price is real and shown; temperature-as-Unruh-from-the-cost is not shown, and H3 was never able to show it.

### 1b. Entanglement: what is established in model, and the real gap
- **PIM (E1, elementary):** in a causal GPT with local tomography (LT), no-restriction on A (NR), reversible maps (RV), a **pure product start** and tracking (a correlated pair appears), the evolution is a reversible entangling map. Existential form: entanglement ⇔ ∃ pure start + reversible history with tracking. So "reversible record-making from a pure start entangles" is proved. This is the sense in which "we have entanglement": **entanglement is what reversible record-making from a pure start looks like.**
- **PIM (M11′, M12, M12ₙ, disk lemma, cuboctahedron² certificate):** in large polytope classes, no reversible map entangles. So entanglement needs parts outside those classes (Conjecture C says: outside all polytopes).
- **Real gap (unchanged):** (i) **P**, the pure start, is interpretive and not cost-selected (PREREG_P miss: the existing costs cannot see *where* randomness sits); (ii) **Conjecture C** beyond the proved classes (ico²/dodeca² ♦, non-locally-symmetric composites, balls); (iii) the premise that an entangling map exists is re-expressed (as tracking under P), not derived from the cost. So we do not have "the cost forces entanglement".

---

## 2. Miss audit: real obstruction or modelling choice?

Important framing point found in the audit: several items reported overnight as "misses" or "fails" are **not evidence against the theory at all**.

| item | what it actually was | real obstruction? | hidden assumption that, if dropped, could flip it |
|---|---|---|---|
| **U(2)/Sp(1)² search, dims 4–8** | A *counterexample* search. "MISS" = **no rival body beat quantum theory**. That is the outcome the selection chain wanted. | No obstruction; outcome fixed by Hopf–Samelson 1940 (10.1007/BF01378063) + weights, so low evidential value (CONSISTENCY_CHECK). | **Fixed prereg target / wrong comparator:** the group was fixed to U(2)/Sp(1)² (already complex structure, U enters via P4), and the price was single-system affine dimension. A composite price (parameters of a two-part record, Hardy/Wootters K_AB = K_A·K_B) is what separates real/complex/quaternionic; dimension at N = 2 cannot. |
| **H3 temperature** | Setup miss (m = 0) + expected fail (m = 0.3) | No for the scaling; yes for "the cost sets T" (the R → T step is the vacuum's) | **Wrong comparator** (storage price κ vs energy shadow price, §1a), **fixed vacuum** (the world was held fixed; only the tracker varied). |
| **Round 13 H2 value** | Sub-prediction that max Φ on dodeca² sits at zero marginals (−0.4446); observed −0.233 at nonzero marginals | No: ♦ (Φ < 0) still held on what was found; full enumeration did not finish (not tested) | **Symmetric-maximizer assumption** (the maximizer was assumed to be the most symmetric point). |
| **G5 gravity "inputs"** | Not a test result; the honest list of what the model was given | Structural, by construction | **The world was fixed.** Every gravity round held the Hamiltonian, the lattice and Lorentz invariance fixed and varied only the tracker's price. A design like that cannot derive relativity or the vacuum, whatever the result. To derive them the *rules* must be the thing the cost selects (route C4/C6 below). |
| **qm-selection-2 gate fail** | Pre-run method review failed (non-exposed faces not reached, one-pair bit face, local N_LB, undisclosed TIE→TARGET relabel, scope) | Method fault; the review worked as designed | Search **reach** (a search that cannot reach part of the space would print "no counterexample", the predicted outcome). |
| **G4 scheme B H3**, **R14 H3**, **R14 H1/H2** | B could take ≤ 3 values by construction (K* ≤ 5); R14 H3 printed "no automorphism" from non-canonical classes; H1/H2 timed out | Instrument limits | **Resolution/canonical form.** |

**Single failure mode (OBS, across our own records).** Most overnight non-hits share one of two shapes:
- **(F1) instrument limit that can print the predicted negative:** a cap (K* ≤ 5), a wrong reference (zero modes), a non-canonical form (radsimp in Q(√5) → 413 classes for 20 values), unreachable faces, a timeout. Each would have produced "nothing found" whether or not the world had the thing. This is what the 4741761 rule ("a validity check for any step whose failure could print the predicted outcome") now guards.
- **(F2) fixed target or fixed world:** the group fixed in advance (U(2)), the vacuum fixed in advance (gravity), the maximizer assumed symmetric (H2 value), the comparator chosen as one-system dimension.
Neither shape is a refutation. F1 says "re-measure"; F2 says "we asked a question whose answer was set by our inputs". Chad's instinct that "we are missing something" is right about F2 for gravity: **we never let the cost choose the world's rules**, so the inputs came out as inputs.

---

## 3. Patterns in 4741761 (R13–16 errata + process rule), checked as a lead, not a fact

What the commit says (read in full): M1, the run tree's lock came from a local working copy, so "pushed before the run" holds by timestamps (to 1 s for R16); M2, the "box clock stepped" story is withdrawn: wall clock agreed with GitHub, the uptime (monotonic) clock lagged ~6.6 min, consistent with a pause (HYP); L1–L2, a re-made commit changed a "written at" line, and box file times were rewritten when the box was replaced, so only the WORKLOG line dates the R13 lock; L3, one exact method carried two labels; L5–L6, a value and a validity gate were not independent of earlier data; process rule: push → ls-remote → clone from GitHub → verify → run.

Patterns, with labels:
1. **Order is only as good as the durable, shared record (OBS in our process).** Local records (mtimes) were reset at a "blank memory" event (box replacement); only records copied to a durable, append-only log, or to a third party (GitHub), kept the order. Two clocks diverged because one stopped *recording* during a pause, not because it ran at a different rate. Theory link: G1's PIM (Page–Wootters record formation orders clock ticks; direction comes from the blank-memory boundary) and Lamport's happens-before (1978, 10.1145/359545.359563, KNOWN). **Label: analogy, plus an instance of a known PIM; no new physics.**
2. **Too-fine (non-canonical) records hide symmetries (OBS) ↔ G1's PIM that the minimal record is gauge-invariant (holonomies only).** The R14 H3 fault is a concrete case: the same number in different symbolic "gauges" looked like different numbers, and the search reported no symmetry. A canonical form is a quotient by redundancy, i.e. a gauge-invariant record. **Label: OBS instance of a PIM; useful as a method rule (always canonicalize before symmetry search), not a physics result.**
3. **Validity gates.** Same as F1 above.
4. **Is there a real route from record cost to time?** Checked in §5, candidates C3, C4, C10. Short answer: record cost gives an *order* and an *arrow* (both from existing PIM + KNOWN results, the arrow needing a blank-memory/pure-start boundary), and it sets clock *precision* (in-model, below). It does **not** give a clock *rate* difference (proper time / dilation): **open miss**, breaking at the point where a rate needs a second, shared reference (an energy/redshift input or a metric).

**In-model check run this session (`clock_cost.py`, `clock_cost.out`; PIM + KNOWN):** a record-count clock as a biased tick walk (entropy per net tick σ, heat kTσ per tick; relative timing variance coth(σ/2)/N, Monte-Carlo-checked to <0.3%). Minimizing CORE's J = heat + w·(timing variance) gives the many-weak-ticks optimum with total entropy Σ* = √(2w/kT), relative variance √(2kT/w), J* = 2√(2wkT); it saturates the thermodynamic uncertainty relation (Barato & Seifert 2016, 10.1103/PhysRevX.6.041053; Erker et al. 2017, 10.1103/PhysRevX.7.031022; Pearson et al. 2021, 10.1103/PhysRevX.11.021029; KNOWN). Consequence: two cost-optimal clocks with different stakes w diverge **diffusively** (variance), never in mean rate. That is where the "clocks diverge by what they record" idea stops being physics: **open miss for a rate/proper-time effect from record cost alone.**

**One structural observation worth keeping (HYP, assembled from PIMs):** the premise P ("the closed whole starts pure") does two jobs. It is the blank-memory boundary that gives the arrow of record order (G1), and it is the premise under which reversible tracking forces entanglement (E1). In a classical or M11′-class world that starts pure, reversible dynamics keep every part definite, so no informative record sequence (no novel bit to record) can ever arise; in QM it can (PREREG_P Pr1: classical needs 1 bit of start entropy, QM 0). So, under P: **an informative event log exists ⇔ a reversible entangling map exists** (⇐ by E1's existential form, ⇒ because an entangling map from a pure product start gives mixed marginals), and an *unbounded* one needs an infinite reversible group (RC7/RC11). This re-reads E1 + RC7 + RC11; it does not remove P. Its value is that "time as sequence" is not an extra input: it is entanglement under P. Candidate C3 tests it.

---

## 4. Search map (needle in a haystack)

- **Hypothesis space:** routes = (premise set removed or merged) × (which object the cost is allowed to choose: tracker, records, composite rules, dynamics, world). Overnight we searched almost only the "tracker varies, world fixed" slice (F2).
- **Oracle:** a route is certified only if (a) a preregistered, blind, validity-gated test hits, (b) a hostile review passes, and (c) the premise graph shows an input **removed or merged**, not renamed. An oracle that can print the predicted negative is invalid (F1).
- **Priors:** subjective, stated in §5. Prior art lowers priors for anything a classification theorem already fixes (U(2) search), raises them where a known reconstruction needs exactly one axiom the cost might supply.
- **Amplification (Grover as a model, not as physics):** Grover/amplitude amplification raises the weight of marked items by repeated reflection about the mean; the analogue is to re-weight routes by their oracle results and re-test only the top of the list, and to **fix the oracle first** (a broken oracle amplifies noise). Grover's optimality (Bennett–Bernstein–Brassard–Vazirani 1997, 10.1137/S0097539796300933; Zalka 1999, 10.1103/PhysRevA.60.2746) says unstructured search costs ~√N queries; the lesson is to **add structure** (premise-graph neighbours of known reconstructions) rather than enumerate.
- **Quantum algorithms as a structural source (checked honestly):** Grover's speed-up needs only **real** amplitudes (oracle and diffusion are real orthogonal maps), so a query-cost argument **cannot** select complex over real QM. At best it separates interference theories from classical ones, which RC1 already does under the drift premise. Lee & Selby 2016 derive Grover's lower bound in GPTs from physical principles (NJP 18:093047, 10.1088/1367-2630/18/9/093047) and the phase-kickback structure (NJP 18:033023, 10.1088/1367-2630/18/3/033023); Lee & Barrett 2015 (10.1088/1367-2630/17/8/083001). Use: a **consistency oracle** (a cost-selected theory must not beat Grover), not a derivation of U(n). The idea "each query can write at most O(1/√N) amplitude into the marked record (the BBBV hybrid argument) = a record-formation speed limit" is a HYP reading, not a result.
- **Known routes, and what GTAO's cost would have to supply:**

| route | gets | from | GTAO would need to supply, to remove an input |
|---|---|---|---|
| Hardy 2001 (arXiv quant-ph/0101012; no DOI checked) | finite-dim QM | 5 axioms incl. continuity, K = N^r | continuity (RC1 gives it only under drift CD) |
| Chiribella–D'Ariano–Perinotti 2010/2011 (10.1103/PhysRevA.81.062348; 10.1103/PhysRevA.84.012311) | finite-dim complex QM | causality, LT, pure conditioning, compression, purification | **purification** ≈ P plus "every mixed state is a marginal of a pure one"; the C3 observation touches it |
| Masanes–Müller 2011 (10.1088/1367-2630/13/6/063001) | complex QM | finite dim, LT, subspace equivalence, continuous reversibility, all measurements | **LT** (route C2) and continuity |
| Jacobson 1995 (10.1103/PhysRevLett.75.1260) | Einstein eq. as equation of state | δQ = T dS on local Rindler horizons, T = Unruh, S = ηA with universal η | Clausius form (T2/T3 give the form), **universal η** (route C1), not T or horizons |
| Jacobson 2016 (10.1103/PhysRevLett.116.201101) | Einstein eq. from entanglement equilibrium | max vacuum entanglement at fixed volume; first law δS = δ⟨K⟩; small-ball BW | the **extremum** (a cost minimum is an extremum principle) and the first law (= T3 at first order); not the QFT vacuum or BW |
| Lashkari–McDermott–Van Raamsdonk 2014 (10.1007/JHEP04(2014)195) | linearized Einstein | entanglement first law **in holography** | needs AdS/CFT; out of scope |
| Verlinde 2011 (10.1007/JHEP04(2011)029) | Newton's inverse-square force, Einstein eq. | holographic screens, entropy change per displacement, equipartition, Unruh T | screens and the Bekenstein step; heavy inputs |
| Padmanabhan 2010 (10.1088/0034-4885/73/4/046901) | field eqs. from a horizon entropy functional | horizon entropy density, Unruh–Davies T | same as Jacobson |
| Unruh 1976 (10.1103/PhysRevD.14.870), Bisognano–Wichmann 1976 (10.1063/1.522898), Hislop–Longo 1982 (10.1007/BF01208372) | T = a/2π; modular flow = boosts | Lorentz invariance + spectrum condition | relativity itself (route C4/QCA) |
| D'Ariano–Perinotti 2014 (10.1103/PhysRevA.90.062106); Bisio–D'Ariano–Tosini 2015 (10.1016/j.aop.2014.12.016) | Weyl/Dirac from a quantum cellular automaton; Lorentz covariance emerges at low momentum | locality, homogeneity, isotropy, unitarity of the automaton | **the selection of those rules** by a cost (the "let the cost choose the world" fix for F2) |
| Causal sets: Bombelli–Lee–Meyer–Sorkin 1987 (10.1103/PhysRevLett.59.521); Malament 1977 (10.1063/1.523436); Hawking–King–McCarthy 1976 (10.1063/1.522874); Brightwell–Gregory 1991 (10.1103/PhysRevLett.66.260); Rideout–Sorkin 1999 (10.1103/PhysRevD.61.024002); Logan–Shepp 1977 (10.1016/0001-8708(77)90030-5); Kleitman–Rothschild 1975 (10.1090/S0002-9947-1975-0369090-9) | order + counting ≈ Lorentzian geometry (for Poisson sprinkling); longest chain ≈ proper time | **Lorentz invariance enters through Poisson sprinkling into a Lorentzian manifold**; almost all finite posets are 3-layer (KR), not spacetime-like | a reason the record poset is sprinkling-like (route C4) |
| Page–Wootters 1983 (10.1103/PhysRevD.27.2885); Connes–Rovelli 1994 (10.1088/0264-9381/11/12/007); Rovelli 1993 (10.1088/0264-9381/10/8/015); Rovelli–Smerlak 2011 (10.1088/0264-9381/28/7/075007); Giovannetti–Lloyd–Maccone 2015 (10.1103/PhysRevD.92.045033) | time as correlation with a clock; time from the state's modular flow; "temperature as the speed of time" (Tolman–Ehrenfest) | a global stationary state; equilibrium; the metric for Tolman | the state and the metric stay inputs; C10 |

Which derive gravity from thermodynamics plus entanglement: Jacobson 1995 (thermodynamics + horizon entropy ∝ area, with entanglement as its suggested origin), Jacobson 2016 (explicitly entanglement equilibrium), Lashkari et al. 2014 (entanglement first law, holographic). None derives QM; all take Lorentz invariance / Unruh–BW as given. Susskind–Uglum 1994 (10.1103/PhysRevD.50.2700) is the species issue: entanglement's area coefficient scales with the number of fields, like 1/G's renormalization.

---

## 5. Ranking by CORE's own method

**CORE §1–2 applied to the choice of route.** Cost of judgment J = (attention + compute spent) + w·E[ℓ], with a ruin cap. Decision: which route to fund next and what we may tell Chad/Ace the theory derives. Loss ℓ: a missed derivation (a true route not found) or a misclaim (a claim later withdrawn). Ruin: a public overclaim (e.g. "derives gravity"); cap ε small, so any route whose *hit* invites overclaim must pre-state what a hit does not mean. Method: estimate, per route, p(hit), the value of a hit and of a clean miss (both data), cost; rank by EIV/cost. CORE item 3 ("higher stakes buy more judgment") says: where w is higher (Chad marks Lean as bedrock), spend more review, not necessarily more routes.

Value scale (stake points, 0–10): 10 = removes or merges a named input in the premise graph and survives hostile review; 5 = makes one input sharper or reduces it to a smaller one; 2 = consistency check whose outcome a known theorem largely fixes; a clean miss that localizes an input also counts. Priors are mine, subjective, and written before any run. EIV = p_hit·V_hit + p_miss·V_miss (+ 0 for inconclusive). Cost in agent-hours (attention + compute).

| id | route | p_hit | V_hit | p_miss | V_miss | EIV | cost (h) | EIV/cost | result that would move it |
|---|---|---|---|---|---|---|---|---|---|
| **C11** | **Judgment-first boundary**: price records by *predictive* value for a stake region's future at lead time k (not static I(T:R)); does the cost-optimal record end at the dynamics' signal front, R*(κ,k) ≈ v·k + O(k^{1/3}), with only weak (log) κ dependence? (§8) | 0.60 | 5 | 0.35 | 4 | **4.4** | 2.5 | **1.76** | a front at v·k with weak κ dependence → the "cut put in by hand" becomes lead time + local dynamics; strong κ dependence or no front → predictive pricing does not give a causal boundary, logged as an open miss |
| **C2** | **LT from read cost** (chain α → Masanes–Müller): does a local-read tracker pay a strictly positive cost premium in non-LT composites (real-QM rebits, K_AB = 10 > 9) *even when joint reads are priced the same as local ones*? | 0.30 | 6 | 0.60 | 4 | **4.2** | 3 | **1.40** | a hit with equal read prices → top; if the premium exists only with a joint-read surcharge, LT is CHOSEN under another name (drop to 0.3) |
| **C3** | **P does two jobs** (arrow + entanglement): catalog check that, from a pure start, an informative event log exists ⇔ an entangling map exists, and is unbounded ⇔ infinite group | 0.90 | 2 | 0.03 | 9 | 2.07 | 1.5 | **1.38** | any M11′-class composite producing a novel bit from a pure start (contradicts M11′ → stop all runs, recheck); otherwise it is a clarity note, value capped |
| C8 | qm-selection-3 (rank-2 groups to dim 15), already locked | 0.20 | 2 | 0.70 | 1.5 | 1.45 | 1 (sunk lock) | 1.45* | *largely fixed by the maximal-torus criterion; keep only because the lock is sunk; a counterexample at dims 8 or 15 would raise it sharply |
| C4 | **Record-dependency poset** on a fixed 1+1 lattice with cost-optimal (Poisson-like, TUR) clocks: are longest-chain level sets hyperbolic (Lorentz-like)? | 0.10 | 8 | 0.85 | 2 | 2.5 | 2.5 | 1.00 | a hyperbolic shape on a fixed lattice → very high (re-check for a sprinkling smuggled in); a non-hyperbolic shape localizes the break at the memory lattice (preferred frame) |
| C1 | **η as a shadow price** (Jacobson 2016 bridge): in 2D lattice vacua, is the cost boundary sharp and isotropic, with per-layer marginal information per boundary site within 20% of κ in critical and gapped vacua and for 1–3 species? | 0.20 | 6 | 0.70 | 3 | 3.3 | 4 | 0.83 | isotropy on a square lattice → raises (area-law input becomes "price"); anisotropy → isotropy/Lorentz named as the input. Note: for independent species the marginal = κ holds **by the first-order condition** (trivially universal), so the species part is not a test; only shape and sharpness are |
| C6 | Clean re-score of critical H3 | 0.85 | 1 | 0.10 | 2 | 1.05 | 1.5 | 0.70 | a miss would mean the post-hoc numbers were wrong (worth knowing); a hit adds little |
| C9 | Lean M11′ polytope assembly (running FOR-27) | 0.50 | 4 | 0.40 | 1 | 2.4 | 6 | 0.40 (×w) | stake-weighted: if Chad's w for Lean is 3× the rest, it rises to ~1.2 |
| C7 | More Conjecture C cases (ico²/dodeca² exact ♦) | 0.60 | 3 | 0.25 | 3 | 2.55 | 6 | 0.43 | a fast exact enumeration (canonical forms in Q(√5)) cuts the cost by 3× |
| C10 | Clock rate / proper time from record cost | 0.05 | 8 | 0.90 | 1 | 1.3 | 2 | 0.65 | already an open miss in model (§3); would move only with a new mechanism for a shared reference |
| C5 | Grover/query cost selects complex amplitudes | 0.02 | 7 | 0.95 | 0.5 | 0.62 | 2 | 0.31 | stays low: Grover works with real amplitudes (fact); kept only as a consistency oracle |

**Pick by score (updated 06:31 after the judgment-first reframe, §8):** C11 first, C2 second, C3 third (C8 continues only because its lock is sunk; C4 is the next new route). Who suggested a route plays no role in the score.

**Where CORE's method is underspecified for this use (data):**
1. **w is not set by the theory** (CORE §1: "w stays assumed", "Temperature does not set w"). The ranking moves with stake weights (Lean ×3 lifts C9 to the top three). We need Chad's stakes per output type.
2. **The loss is undefined for research.** CORE's E[ℓ] is a decision loss; "information value of a route" needs a decision it feeds. I used "what we fund and what we claim"; another choice changes V.
3. **Priors are outside the method.** THEORY says the world's pattern of change is the only world input; here there is no such data, so priors are judgment.
4. **The value of information is non-concave** (Radner & Stiglitz 1984, credited in THEORY.md): routes that need a large first investment (C7, C9) score badly per hour even when their total value is high. EIV/cost biases against them.
5. **The ruin cap is not priced into EIV.** I handled overclaim risk as a constraint (pre-stated "a hit does not mean"), which is CORE's form, but ε is unchosen.
6. **The CORE hypothesis applies to strongly selected systems** (CORE §5's four conditions). One night of research is not strongly selected, so this use is normative, not a prediction.

---

## 6. Prereg sketches (DRAFTS; not locked, not pushed, not run; exploratory runs deliberately not done so they can stay blind)

### Draft A (C2): is local tomography selected by read cost, with no read-price asymmetry?
- **Question.** For two-part records, does a tracker that reads each part locally (and may combine results) pay a strictly larger minimum cost J = (read cost) + w·E[ℓ] in a non-LT composite than in an LT composite, **when a joint read costs exactly what a local read costs**?
- **Composites (fixed in advance):** real QM 2 rebits (K = 10, not LT); complex QM 2 qubits (K = 16 = 4·4, LT); quaternionic 2-system as defined in the literature, if a standard composite is available (otherwise excluded, declared); classical bit² (LT); square² min and max (LT).
- **Task family:** stakes on a binary event whose value depends on a randomly drawn state from a fixed, invariant ensemble on each composite (Haar-like under the composite's reversible group; ensemble declared in advance). Loss = 0/1 error; read cost = c per read regardless of locality.
- **Prediction (HYP):** at every w and c on a declared grid, min J(real) > min J(complex) by at least the cost of resolving the non-local parameter, *only if* stakes load on that parameter with positive weight under the invariant ensemble.
- **Oracle / success criterion:** HIT if the premium is > 0 at all grid points with equal read prices; MISS if the premium vanishes when read prices are equal (then LT is CHOSEN, via read pricing). Validity gate: the LT composites must show zero premium, and real QM must show a premium when joint reads are forbidden (positive control).
- **What a hit would not mean:** not a derivation of QM; Masanes–Müller still needs finite dimension, subspace equivalence, continuous reversibility (RC1 only under CD) and all measurements.

### Draft B (C3): a pure start gives an informative event log iff its reversible maps can entangle
- **Question.** From a pure product start, how many bits of novelty (marginal entropy of a part that a later record can track) can reversible histories produce, and is the sequence bounded?
- **Catalog (fixed in advance):** classical bit²; square² min/max; hexagon² max; octahedron² max (M11′ classes); stabilizer 2-qubit (finite group, restricted reads); QM 2-qubit (one-parameter entangling family).
- **Prediction (PIM-derived; a consistency check, low evidential value):** novelty = 0 exactly for classical and M11′-class composites; > 0 and with a sequence that recurs within the group order for stabilizer; > 0 and with no exact recurrence for a generic one-parameter QM family.
- **Oracle:** exact (rational or symbolic) computation, canonical forms checked by a validity gate (the R14 lesson). Falsifier: any M11′-class composite with novelty > 1e−12 (contradicts M11′; would trigger a full recheck), or stabilizer at 0.
- **What it shows if it holds:** "time as a sequence of informative records" is not an extra input; under P it is the same thing as entanglement, and unbounded sequence is the same thing as a continuous symmetry. P itself remains assumed.

### Draft C (C4, next new route; short): record-order geometry on a fixed lattice
- World: L = 401 sites in 1D, each with an independent Poisson record clock (rate 1; the cost-optimal TUR clock in the many-weak-ticks limit is stochastic). A record at site i depends on the latest records at i−1, i, i+1. Poset = transitive closure.
- Prediction (HYP): the longest-chain length between the origin and events (x, t) has level sets that are **not** hyperbolas; the fitted exponent of chain length vs √(t² − x²/v²), with v the measured front speed, differs between x/t = 0 and x/t = 0.5v by > 10%. Expected fail of Lorentz-likeness; a hit would be surprising and must be re-checked for a hidden sprinkling.
- Control: Poisson sprinkling in 1+1 Minkowski light-cone coordinates must reproduce the Logan–Shepp/Brightwell–Gregory 2√(ρ·uv) scaling (validity gate).
- Breaks where: fixed memory sites = a preferred frame; Lorentz invariance would have to come from the cost choosing *where* records live, which this model does not allow.

---

## 7. Bottom line
- Temperature-as-price-of-information is shown (KNOWN + PIM). H3 tested something else (a physical modular temperature), failed on setup, and could not have derived T from the cost even if it hit.
- Entanglement: proved in model that reversible record-making from a pure start entangles (E1) and that large polytope classes cannot (M11′/M12). Not shown: that the cost selects the pure start or Conjecture C in general.
- The overnight misses split into instrument limits (F1) and fixed targets/worlds (F2). None refutes the theory; F2 is the real "missing something": we never let the cost choose the world's rules.
- Ranked by CORE's own J with stated priors: C11 (judgment-first, lead-time boundary), then C2 (LT from read cost), then C3 (P's two jobs), with C4 next. Gravity routes (C1, Jacobson 2016) rank lower per hour, because their key step (horizons, isotropy, Lorentz) is the part a fixed lattice cannot give.

---

## 8. Reframe test: "judgment is key; memory exists to predict the future" (added 06:31 ET, after Chad's clarification)

**Does the repo's framing already encode prediction/judgment? Yes, at the core; no, in the overnight physics thread.**
- CORE.md's object is "the cost of judgment: being wrong or late plus the cost of holding, acquiring, and sharing information" (J = Q̇ + w·E[ℓ]); its converse (Theorem S1) is "every design pays at least for the **predictive** information it holds"; CORE :96 uses the predictive information-bottleneck curve (CT4: the first bit pays only if its price is below the loss it saves). THEORY.md :36 already prices "kT·(I_mem − I_pred) for memory that does not predict" (Still, Sivak, Bell & Crooks 2012, PRL 109:120604, 10.1103/PhysRevLett.109.120604, KNOWN). So the core is judgment-first already. "Physics is the universe's way of keeping track of itself" is a gloss on the R&D thread, not the core's wording.
- **The drift is in the R&D physics rounds (OBS, from our own preregs).** G4/G5 valued a record by static mutual information I(T : R) at one time; PREREG_P priced "records, capacity and errors"; the composition and Conjecture C rounds price state-space structure with no stake on a future loss. That is bookkeeping, not prediction. This is a third failure shape, **F3: static value instead of predictive value.** Related prior art for the sharper core, all KNOWN: Bialek–Nemenman–Tishby 2001 predictive information (10.1162/089976601753195969); Creutzig–Globerson–Tishby 2009 past–future information bottleneck (10.1103/PhysRevE.79.041925); rational inattention (Sims 2003; Matějka–McKay 2015); free-energy principle (Friston 2010, 10.1038/nrn2787; a looser, variational framing).

**Is one of these a sharper core?** Not a replacement: CORE already is the predictive bottleneck plus a heat floor plus a stake plus a ruin cap; Still et al. supply the heat price of the non-predictive part; rational inattention supplies the logit form (T2). The sharpening is a **rule for the physics rounds**: value every record by its predictive information about the stake region's *future* at a stated lead time k (THEORY's k), net of what the tracker already holds, never by static correlation.

**Would it change any miss or route?**
- **H3 / G4 / G5 (changes):** with value = information about T's future at lead k given T now, only sites that can influence T within k matter. For a local Hamiltonian the influence of site j on T after time k is bounded outside a front |j| ≈ v·k (Lieb–Robinson 1972, 10.1007/BF01645779, KNOWN; for the hopping chain the propagator is a Bessel function J_{|j|}(2k), front at |j| = 2k with an Airy-width ~k^{1/3}). So the cost-optimal record would end at the **signal front set by the lead time**, not at a κ^{−1/2} radius. That addresses the G3 open miss "why reads end at a causal horizon" in part: the horizon becomes "how far ahead you must predict × how fast influence travels". What stays input: locality of the dynamics and the speed v (relativity's light cone is the Lorentz-invariant case of this front). **HYP; route C11; draft prereg below.**
- **RC2 (zero drift, no selection of quantum-like records):** expected under the reframe: with nothing to predict, nothing is selected. Consistent; no flip.
- **PREREG_P (P not cost-selected):** no change found. A judgment-first value does not obviously favour a pure start (a classical world's pre-stored random bit is, if anything, more predictable in principle).
- **U(2) search, R13 H2 value, qm-selection gates:** no change (mathematics, not valuation).
- **Temperature:** Still et al. make the relevant temperature the bath's (kT per nat of non-predictive memory); it is not derived either way.

**New, testable prediction (HYP; draft prereg D, not locked, not run):**
- World: infinite half-filled hopping chain (as G5), stake region T = 5 sites; Heisenberg-picture propagator U(k) (exact, Bessel).
- Value of a site j at lead k: its weight in T's future operators beyond T's present ones, w_j(k) = Σ_{t∈T} |U_{tj}(k)|² for j ∉ T (a declared, basis-free proxy for predictive value; the quantum two-time information question is sidestepped and declared as such). Greedy record: add sites by w_j until the next marginal < κ.
- Grid: k ∈ {2, 4, 8, 16, 32}, κ ∈ {10⁻², 10⁻³, 10⁻⁴, 10⁻⁶}.
- Prediction: R*(κ,k) − v·k (v = 2) grows no faster than c·k^{1/3}·log(1/κ) with one fitted c; at fixed k, R* changes by < 25% across the four κ values for k ≥ 8 (weak κ dependence), unlike G4's static R ∝ κ^{−0.49}.
- Validity gate: propagator unitarity to 1e−12; the k = 0 case must return R* = the stake region (no outside value).
- Falsifier: κ dependence at fixed k ≥ 8 above 25%, or R* − v·k growing like k (no front).
- What a hit would not mean: not a derivation of relativity, the light cone, or v; it shows only that *predictive* pricing puts the record's edge at the dynamics' own signal front, so the boundary stops being a hand-placed cut.

**Score:** added as C11 in the §5 table: EIV 4.4 for 2.5 h (1.76), the highest per hour. Caveat for the hostile reviewer: the front itself is Lieb–Robinson/Bessel mathematics (KNOWN); the in-model content is only that the cost's stopping rule lands on it with weak price dependence, and the hit probability is high because of that.

---

## 9. Corrections after GATE_READ_STEPBACK.md (appended 26 Nov 2026, after 06:35 ET; the text above stands as written, and where it conflicts with this section, this section governs)

Gate read of the 06:31 version (sha256 d163a280…5c86): Draft D (C11) **FAIL**, Draft A (C2) **FAIL**; nothing was locked, pushed or run. Corrections:

**C9-1 (T2 overstated; gate T4-2).** §1a row T2 and the sentence "This is the 'temperature = price of information' identity, and it is established (prior art plus our in-model versions)" are corrected to: *the identity λ = temperature (the price of one nat of information is the temperature of a logit/Boltzmann choice rule) is KNOWN (Sims 2003; Matějka–McKay 2015; Ortega–Braun 2013). GTAO's rows R1 (CLAIM_MAP_v2 :651, status PRIOR ART, Sella & Hirsh in substance) and U1 (:692, PROVED (in-model)) give the same Boltzmann form π ∝ e^{−βJ}, but there β is a **selection strength** (β = αν from population size; β_i in a Moran chain), not a price per nat of information. The link between the two is **form-level only**.* "G2" in that row meant the forces-gravity round G2 (rnd/forces-gravity/NOTE.md), not CLAIM_MAP's G2 row (POOLSIM, an unrelated row). The "economics paper" temperature in THEORY.md is CT18's shock/buffer ratio with Drăgulescu & Yakovenko 2000 credited **as an analogy only**; it is not the same formula as any physical temperature. So for Chad: "temperature was already proven" holds for CT18 (a proved in-model scaling identity for ruin hazard) and for the logit form as prior art; neither is a physical temperature.

**C9-2 (K4 status; gate T4-1).** §1a row T1 says "Real-system lead prediction K4 is PROXY-FAIL". K4's current status in CLAIM_MAP_v2 (:409) is **NOT A TEST (qualification not established; proxy: failed)**. PROXY-FAIL is its history.

**C9-3 (re-run claim; gate T4-3).** "A clean re-run would very likely be a hit" (§1a, end of point 3) is a **HYP** resting on post-hoc, unscored numbers (NOTE.md G5 post-hoc block). It is route C6 and has not been run.

**C9-4 (E1 status and conditions; gate E4-1..3).** The E1 in §1b is the R&D-notes theorem (rnd/entangle/NOTE.md, THREAD_SUMMARY.md, hostile-reviewed in HOSTILE_REVIEW_E1.md). **It is not a CLAIM_MAP_v2 row**; CLAIM_MAP's "E1" is an unrelated row. Renamed here **Ent-E1**; status: PIM in R&D notes, hostile-reviewed, not yet in CLAIM_MAP_v2. Full hypothesis list: causal GPT; two-part closed world A⊗B; local tomography (LT, used in ⇒ of the existential form); no-restriction on A (NR, conditional states are states); product effects valid; reversible maps (RV); **pure product start**; **tracking** (a correlated pair appears). Tracking from a pure product start **is the entangling premise re-expressed**. So the §1b sentences "reversible record-making from a pure start entangles is proved" and "This is the sense in which 'we have entanglement'" read, with their conditions: *given LT, NR, RV, valid product effects, a pure product start and tracking (which is the entangling premise re-expressed), the evolution is a reversible entangling map (Ent-E1).* The cost does not give entanglement (item (iii) stands).

**C9-5 (wording).** Read "first law (of entanglement)" as **"the first-order relation δS = δ⟨K⟩"** (§1a T3, §4 table rows Jacobson 2016 and Lashkari et al.), and "area-law" as **"area scaling"** (§5 row C1). Low severity in notes; required for anything carried into the repo.

**C9-6 (rescored ranking; gate §3).** C11's scores broke the scale's own rule (a hit fixed by a known theorem is worth 2). Rescored: C11 p_hit 0.85, V_hit 2, p_miss 0.10, V_miss 1 → EIV 1.8, **0.72 per hour** (was 1.76). C2 as drafted has a definitional hit (V_hit ≈ 2); C2 redesigned per A1–A7: p 0.15, V_hit 6, p_miss 0.75, V_miss 3 → 3.15/3 = **1.05 per hour** (was 1.40). The V_miss values were set without a rule; from here, V_miss = 2 for a miss that locates nothing, 3 for a miss that names an input, unless stated.

| rank | route | EIV/cost | note |
|---|---|---|---|
| (sunk) | C8 qm-selection-3 | 1.45 | only because its lock is sunk; outcome largely fixed by the maximal-torus criterion |
| **1 (new)** | **C3 pure start, two jobs** | **1.38** | cheap consistency check under P, value capped (V_hit 2) |
| 2 | C2 redesigned (A1–A7) | 1.05 | needs a fresh gate read |
| 3 | C4 record-order geometry | 1.00 | |
| 4 | C1 η as shadow price | 0.83 | |
| 5 | C11 lead-time boundary | 0.72 | now a lemma (PIM_LEMMA.md), not a test |
| 6 | C6 clean H3 re-score | 0.70 | |
| — | C9 Lean M11′ assembly | 0.40 (≈1.2 with Lean stake ×3) | enters the top three under Chad's "bedrock" weight; report both ways |
| — | C10, C7, C5 | 0.65, 0.43, 0.31 | unchanged |

**C9-7 (D reclassified).** Draft D is withdrawn as a test. Its content is the lemma in `PIM_LEMMA.md` (PIM, an application of KNOWN mathematics, V ≤ 2). D5 applies to every reading of §8: the boundary moves from a chosen κ to a chosen lead time k and stake region T; it is **not removed** unless k is selected by the cost. The §8 claim that predictive pricing "addresses the G3 open miss in part" is withdrawn to: *it re-expresses the cut as (k, T, v), all inputs*. F3 (static instead of predictive value) stands as a diagnosis of the physics rounds. The gate read's Airy table (its §1.3) is prior knowledge for any successor of D and must be cited in its §0.

**C9-8 (A).** Draft A is withdrawn; a redesign per A1–A7 is in `PREREG_DRAFT_A2.md` (draft only, if written).

---

## 10. Candidate C12: the stake threshold (from Ace, added for alignment; scored like the other routes)

**Hypothesis (HYP), suggested wording:** "physics is the zero-stake floor of the cost of judgment". At w = 0, CORE's J = Q̇ + w·E[ℓ] is minimized by holding no memory; life/judgment-like structure appears only when w is large enough.

**Is the threshold guaranteed by construction? Yes, for the basic version.** CORE :96 / THEORY B.1 (CT4): on the predictive information-bottleneck curve the first bit pays only if its price is below the loss it saves. So "a predicting memory becomes cost-optimal past a stake threshold w₁ = (price of the first nat)/(loss saved per nat at zero information)" is already PROVED (in-model) in the repo. Re-deriving it is V_hit = 2 with no new information; it needs no run. One correction to the framing: the G4/G5 physics rounds were not at w = 0 (they had a stake q = 1 on I(T : R)); they were at a *static* stake (F3). The zero-stake reading fits CORE's heat-floor term alone.

**Is there a real prediction inside it? Possibly: the order of two transitions.** "Self-maintaining" adds a second cost the repo has: T63's repair floor 4kTΓ(ln2 − h(ε)) per record per unit time for carriers that leak at rate Γ (PR #240, independently reviewed). Two thresholds: w₁ (prediction pays) and w₂ (actively repairing a record beats letting it decay and re-learning it). Expected structure (HYP, not computed): if the world drifts faster than records leak (r > Γ), records go stale before they decay, re-learning dominates and w₂ may not exist; if Γ > r, w₂ exists and w₂/w₁ is a function of Γ/r. A numeric ratio w₂/w₁(Γ/r) and the regime boundary would be a real, falsifiable in-model statement. It is still a calculation inside chosen classes (telegraph world, RF carriers), so it is a PIM-to-be rather than a test of nature, and "life appears" would be an overclaim (ruin cap): a hit means "a repair-paying memory is optimal past w₂ in this class", nothing more.

**Score (corrected scale, V_miss = 3 because a miss names the regime where maintenance never pays):**

| id | route | p_hit | V_hit | p_miss | V_miss | EIV | cost (h) | EIV/cost | moves if |
|---|---|---|---|---|---|---|---|---|---|
| C12a | basic stake threshold | 0.97 | 2 | 0.02 | 3 | 2.0 | (already CT4) | — | nothing to run; cite CT4 |
| C12b | order of transitions w₁ < w₂ with a numeric w₂/w₁(Γ/r) | 0.50 | 3 | 0.40 | 3 | 2.7 | 3 | **0.90** | a closed form for w₂/w₁ found on paper → cost halves (≈1.8); if w₂ always equals w₁ the route is empty |

**Rank:** C12b sits after C2-redesigned (1.05) and C4 (1.00), ahead of C1 (0.83). Not in the top two, so no prereg here; the open-miss condition from the brief ("no threshold") cannot occur for C12a, because CT4 already guarantees it.

---

## 11. Temperature, separated (appended after Ace's alignment note; each item checked against the repo at 04c8309; governs §1a and §9 C9-1 where they differ)

| # | temperature | what it is | repo status (checked) | decides |
|---|---|---|---|---|
| **1** | **Ruin temperature** σ√τ/B (= 1/z; shock × √(fix time) ÷ buffer) | CT18 (hazard ν = F(z)/τ) and **CT25** (per-window chance constraint: per-window ruin erfc(z/√2) ≤ ε ⇔ B ≥ z_ε·σ√τ; z_ε = 2.576, 3.291, 4.892 for ε = 10⁻², 10⁻³, 10⁻⁶) | CT18 and CT25 **PROVED (in-model)** (THEORY.md :392, :402; CLAIM_MAP CT18, CT25). Per-window first passage = Lemma B8 / CL4, Black & Cox 1976 (**PRIOR ART**). The τ^H form (CT18-H) is **simulated (OBS)**, not proved. Credits: the ratio is the inventory safety factor (CT18 row). Merton 1974 appears only in CL4, as the terminal-default version that is off by a factor of 2, so "Merton distance-to-default" is a family resemblance, not the repo's formula. **Lundberg is CT22's lifetime-ruin bound, which THEORY says is a different constraint from CT25** (THEORY :82, :186, :402). | survival under the ruin cap, per fixing window |
| **2** | **Physical kT** | the heat floor on remembering: Q̇ ≥ kT × learning rate (CORE.md :19; Horowitz & Esposito 2014, KNOWN for bipartite chains and additive-noise diffusions) | CORE.md :29: "w converts the loss into the currency of the heat. **Temperature does not set w.**" | the price of memory |
| **3** | **Selection temperature** 1/β | π ∝ e^{−βJ} with β = αν, a selection strength set by population size | R1 (CLAIM_MAP :651) **PRIOR ART** (Sella & Hirsh's ν); U1 (:692) PROVED (in-model) for exact-potential games | how close selection sits to the minimum (d/(2β)) |
| — | money-gas "temperature" | Drăgulescu & Yakovenko 2000 | **analogy only** (THEORY.md :195) | nothing |
| — | logit / rational-inattention λ | price of a nat of attention | KNOWN (Sims 2003; Matějka–McKay 2015); same exponential form as #3, link form-level only (§9 C9-1) | choice spread |

**What H3 tested:** a kT-type / horizon (modular, Bisognano–Wichmann) temperature of a lattice vacuum, scaled by a storage price κ. It did **not** test the ruin temperature. **CT25 stands, untouched by any overnight result.** So, for Chad: the temperature that THEORY proves (the ruin temperature, CT18/CT25) is proved in-model and was never in question; the overnight open miss was about a different, physical temperature.

**Link to C12 (stake threshold): the ruin side of judgment.** THEORY (iv) / CT22: on the scalar diffusion path, below B_min no design is certified, above B_slack the ruin cap is slack and the expected-cost rules are optimal, and in between the cap binds with a multiplier μ_s > 0, "the price of survival". So judgment can be switched on by two separate things:
- the **stake** (CT4: the first bit pays when w × loss saved > its price), and
- the **survival constraint** (when the ruin cap binds, μ_s > 0 forces fixing/tracking even at w → 0).
**C12c (HYP, a corollary-to-be of CT4 + CT22 on the same path):** the region of the (w, B) plane where the optimal design holds a non-zero memory is the union of a stake region (w > w₁) and a survival region (B < B_slack(w)). At zero stake, judgment is absent **iff** the ruin cap is slack. This sharpens C12's wording: "physics is the zero-stake floor of the cost of judgment" (HYP) holds only with "and slack ruin"; a world with a binding ruin cap needs memory at zero stake. It is not "the stake turning on is exactly where ruin binds": the two thresholds are set by different parameters (w versus B, ε) and coincide only on a curve.
Score (scale rule: largely fixed by our own proved CT4 + CT22, so V_hit = 2): p 0.7, V_hit 2, p_miss 0.25, V_miss 2 → EIV 1.9 for 2 h → **0.95 per hour**. It does sharpen C12 (it replaces the w-only threshold with a (w, B) onset boundary and says which side survival is on), so it supersedes C12b's framing; C12b's order-of-transitions question (repair vs prediction) remains a separate 0.90 item. Neither enters the top two.

**Ranking after §§9–11 (corrected scale; C3 rescored in PREREG_DRAFT_C3.md §7):** C8 1.45 (sunk) · C2-redesigned 1.05 · C4 1.00 · C12c 0.95 · C12b 0.90 · C3 0.84 · C1 0.83 · C11 0.72 (now a lemma) · C6 0.70; Lean C9 0.40, or about 1.2 with Chad's ×3 stake.

---

## 12. Note after drafting A2 and C3 (appended)
- PREREG_DRAFT_A2.md: C2's useful content is a KNOWN counting theorem (K_AB ≥ K_A·K_B, equality iff LT; Barrett 2007) plus a premise-graph question (does P6's dimension price extend to composites? If so, LT merges into P6). At fixed rebit parts LT and an interaction cannot both hold (MMPA 2014; de la Torre et al. 2012), so the fixed-parts question is tied to premise I. Residual test ≈ 0.53 per hour.
- PREREG_DRAFT_C3.md: own rescore ≈ 0.84 per hour; mostly a restatement of Ent-E1, E-L0, M11′ and PREREG_P; the informative arm is a rigidity count adjacent to Conjecture C.
- **Ranking now (corrected scale, new routes only, sunk C8 aside):** C4 1.00 · C12c 0.95 · C12b 0.90 · C3 0.84 · C1 0.83 · C11 0.72 (lemma) · C6 0.70 · C2 residual 0.53; plus two cheap paper items that are bookkeeping rather than evidence: the A2 §1 merge note and PIM_LEMMA.md. With Chad's Lean stake ×3, C9 (≈1.2) leads.
- Honest reading: after the gate read, no new route scores above about 1 per hour on this scale. The highest-value next steps are paper merges (LT into P6; the P/arrow/entanglement synthesis) and the Lean M11′ assembly if Lean carries the stake Chad gave it.

---

## 13. Corrections after GATE_READ_STEPBACK2.md (appended 26 Nov 2026, after 06:51 ET; earlier text stands; this section governs where they conflict)

Gate read 2 outcomes: A2 §1 FAIL as stated (relabelling, not reduction); PIM_LEMMA bound PASS, reading FAIL; PREREG_DRAFT_C3 FAIL (amend); A2 §2 residual test FAIL. Matching appended sections are in PIM_LEMMA.md ("Amendments after gate read 2") and PREREG_DRAFT_A2.md ("Corrections after gate read 2"). C3 is redrafted as PREREG_DRAFT_C3v2.md.

**C13-1 (A2 §1; amendments 1a–1f).**
- 1a: the counting K_AB ≥ K_A·K_B is **Hardy 2001 §6.15** (arXiv quant-ph/0101012v4, text read this session; no DOI claimed), not Barrett 2007. Barrett 2007 (10.1103/PhysRevA.75.032304) stays as the source for LT *as an assumption* (his Assumption 5) and for real QM violating it.
- 1b: three-line proof, with hypotheses (finite dimension; product states exist with factorising probabilities; product effects valid): the K_A·K_B product effects are linearly independent functionals on the composite's state space; LT ⇔ they separate states ⇔ they span the K_AB-dimensional effect space ⇔ K_AB = K_A·K_B. Quaternionic QM fails the factorising hypothesis and lies outside the statement.
- 1c: renamed. **KNOWN equivalence: at fixed parts, LT ⇔ minimal K_AB. Adopting P6′ (a dimension price on composites of fixed parts) is equivalent to LT when no interaction is required. P6′ is a new clause; P6 itself is CHOSEN (qm-selection PREREG :26); the premise count is unchanged.** §12's and the report's "merge" / "LT stops being a separate premise" are withdrawn: this is a reformulation, not a merge.
- 1d (finding): **P6′ plus the interaction premise I selects the non-LT real-QM composite at disk parts** (K = 10, the least integer above 9 with a continuous interaction), because no LT composite of disks has one (MMPA 2014). In the chain, disks are removed by P5 (hSFP), not by LT or P6′. For 3-ball parts, P6′ + I lands on the LT slice (QM attains K = 16 with interaction), and then de la Torre et al. 2012 gives QM.
- 1e: credit: Hardy 2001 motivates his composite rule (Axiom 4, K = K_A·K_B) by "we do not expect there to be more entanglement than necessary" and keeps it as its own axiom beside Axiom 2 (simplicity); Hardy & Wootters 2011/2012, "Limited holism and real-vector-space quantum theory", Found. Phys. 42:454, 10.1007/s10701-011-9616-6 (Crossref OK this session; not read) for the holism count K_AB − K_A·K_B.
- 1f: the disk statement is **MMPA 2014** (10.1063/1.4903510), not de la Torre et al. 2012 (which is the d = 3 classification).
- Value: a reformulation note, V ≤ 2, no premise-graph merge.

**C13-2 (PIM_LEMMA; amendments 2a–2d).** Only an upper bound is proved: the record **never extends past** the front plus an Airy edge (R* < d* = 2k + O(k^{1/3}(ln(|T|/κ))^{2/3})). It does not "end at" the front: the largest weight near the front is ≈ 0.29·|T|·k^{−2/3}, so for fixed κ the record is **empty once κ ≳ c·k^{−2/3}** (c ≈ 0.29|T|), and reaches the front only for κ ≲ c·k^{−2/3}; no lower bound is proved. |J_{−n}| = |J_n| is used; the asymptotic step is leading order only. Status: PIM (application of KNOWN mathematics), V ≤ 2.

**C13-3 (A2 §2).** Dropped as a test. Check requested in the brief: **BGW 2020 does contain a non-LT composite of complex qubits** (arXiv 1606.09331v3, abstract and p. 44, saved as `bgw2020_arxiv1606.09331v3.txt`: in InvQM "the composite of two complex quantum systems is a direct sum of two copies of their standard composite — equivalently, is the standard composite, combined with a classical bit", and "composites in InvQM are not locally tomographic"). So the world set is not empty, but the gate read's other finding stands: the outcome is set by a CHOSEN drift rate of the holistic parameter. Here that parameter is the extra classical bit, which continuous reversible drift cannot move; under the chain's continuous-drift premise it carries no extra tracking cost, and only discrete swaps (rate CHOSEN) would. Recorded as an open question, "what sets the drift rate of holistic parameters?", not a test.

**C13-4 (C3).** PREREG_DRAFT_C3 is superseded by PREREG_DRAFT_C3v2.md (amendments 3a–3j). One finding of gate read 2 is itself corrected there with a proof: in a regular pentagon or heptagon with all effects, **non-adjacent vertex pairs are perfectly distinguishable** (5 pairs in the pentagon, 7 in the heptagon), so "no two vertices are perfectly distinguishable" (gate read 2 §3.1) is false. The start search is widened anyway (3d).

**C13-5 (C12c wording, gate §5).** "Judgment absent iff ruin cap slack at w = 0" needs CT22's B_slack definition to show that a zero-memory design meets the cap whenever the cap is slack; until that is cited line by line, read "iff" as "if (HYP), converse unproved".

**C13-6 (ranking, corrected scale; C3 from C3v2 §8):**
C4 1.00 · C12c 0.95 · C12b 0.90 · C1 0.83 · C11 0.72 (lemma, not a test) · C6 0.70 · C3v2 ≈ 0.55 (full) / ≈ 0.75 (pentagon² cut) · A2 residual: not a test. With Chad's Lean stake ×3, C9 (≈1.2) leads. No new route scores above about 1 per hour; the reformulation notes (LT ⇔ minimal K_AB; P's two jobs) are bookkeeping value only.

**C13-7 (addendum, same day).** PREREG_DRAFT_C3v2.md computes its scores as 0.54 per hour (full) and 0.81 per hour (P5² cut); these replace the ≈0.55/≈0.75 estimates in the C13 ranking. The draft also discloses a paper argument (HYP "Lemma R": automorphisms that preserve products send rows/columns to rows/columns, giving local⋊swap for polygon parts with n ≥ 4, subject to an unproved affine-dimension step). If Lemma R holds, C3v2's open arm is settled without a run. The paper step scores ≈1.7 per hour and is ranked above the C3v2 run.

## 14. Simplest-route check (HYP only; no new runs; 26 Nov 2026)
Prompt: "The answer is simple but not easy." Two questions, answered against the record. All of it is HYP unless marked otherwise.

**(a) The simplest single statement that explains the most past misses.**
- **Candidate F2: "the world or rules were fixed first and never chosen by the cost."** Checked against the record:
  - **Fits:** gravity (vacuum fixed), the U(2) group fixed in advance, the H2 maximizer assumed symmetric, and A2 §2 (outcome set by the chosen drift rate).
  - **Does not fit:**
    - (i) RECORD-COST-U §14: the cost *was* given a choice of world (polygon vs disk). It chose the odd polygon at every finite horizon tested (OBS, T = 2–12, 16, 20).
    - (ii) PREREG_P: K0, K1 and K3 were asked to select the start premise P, and they tie.
    - (iii) LEMMA_R.md (today): in polygon worlds the reversible rules are forced by the state space (Aut = local ⋊ swap, PROVED (in-model) conditional on RC15). There is nothing left for a cost to choose once the parts are fixed.
  - So F2 explains about 4 misses and fails on 3. In each of the 3, the cost was allowed to choose and still did not select a QM-like world.
- **Sharper candidate FH (HYP): "Every cost tried so far is evaluated at a finite horizon or a fixed task, and at any finite horizon a finite (polytope or classical) design is at least as cheap. A continuum is selected only by a requirement over all horizons, which is U itself."**
  - FH explains (i) directly; ROUND10 §14 already says the disk wins only if one design must serve every horizon.
  - It explains (ii): K3 ties at 2T for finite T.
  - It explains (iii): polytope parts are rigid at any horizon, so the only escape is a non-polytope part.
  - It explains the U(2) case of F2 (the continuum was put in by hand).
  - It does not explain gravity, H3 (kT/horizon modular temperature) or H2.
  - Count: FH covers about 5 of the 7 misses I can check, and F2 about 4. They overlap on U(2).
- **Simplest combined reading (HYP):** "the cost has never been shown an unbounded horizon." Both F2 and FH are instances of it: the rules were fixed, or the horizon was. It is a diagnosis, not a test. Nothing here shows that an unbounded horizon *would* select QM.

**(b) A minimal blank-slate setup cheap enough to sketch on paper.**
- **Smallest version:**
  - one part, with design n ∈ {3, 4, …} ∪ {disk} (state space = n-gon or disk);
  - horizon T drawn from a geometric distribution p(T) = (1 − q)qᵀ, unbounded support, mean q/(1 − q);
  - choose n to minimise E_T[J(n, T)] + price(n), using J as defined in ROUND10 §14.
  - The composite rules are then not free: by Lemma R + RC15 they are forced (rigid) for n ≥ 4 polygons. The only "blank-slate" freedom left is n and q.
- **Outcome logic:** the disk is selected for some q < 1 iff the polygon's cost beyond its design horizon (T > (n − 1)/2) grows faster than price(n) saves.
  - J(n, T) for T > (n − 1)/2 is not in the repository record as far as I can see; I have not checked this further.
  - §14 already notes that a linear price c·d reverses the ranking toward the classical jump, so the outcome is set by price(n), an input. That is F2 again, one level up.
- **Honest limit:** a horizon distribution with unbounded support is itself an assumption (a soft U). A "disk wins" result would select the continuum from that distribution; it would not derive it from the cost alone.

**Scored (same CORE-method table and scale as §13).**

| route | prior p | V hit | V miss | EIV | cost | per hour | what would update it |
|---|---|---|---|---|---|---|---|
| SR-a: F2/FH diagnosis | — | — | — | NOT A TEST (classification of past misses) | 0.5 h (done) | — | a miss where the cost saw an unbounded horizon and still failed |
| SR-b: horizon-mixture selection of n, paper sketch | 0.3 (judgment, not derived: 15/15 finite horizons chose a polygon, but the out-of-design-horizon J is unknown) | 4 | 2 (the miss names price(n), which §14 already names) | 0.3·4 + 0.7·2 = 2.6 | ≈ 3 h | **≈ 0.87** | J(n, T) beyond the design horizon; a price(n) fixed in advance |

**Placement:** SR-b at ≈ 0.87 ranks below C4 1.00, C12c 0.95 and C12b 0.90, and just above C1 0.83 (Lean C9 ≈ 1.2 with its ×3 stake stays first). **Not promoted.** SR-a is a useful frame for reading the misses, but it is not a test.

**Corrected ranking after LEMMA_R.md:** C3v2 Arm 2 is now theorem-fixed conditional on RC15 (≈ 0.47 per hour full, ≈ 0.78 per hour for the P5² cut), so it drops below SR-b. Lemma R itself is written (LEMMA_R.md).

**C14-1 (appended after the hostile review of LEMMA_R.md and §14; §14 above is left as written).**
- **The tally (M4).** The "5/7" for FH is not supported by §14's own text.
  - Assignments, item by item, as one reader's classification:

    | miss | F2 | FH |
    |---|---|---|
    | gravity | yes | no |
    | U(2) | yes | yes |
    | H2 | yes | no |
    | A2 §2 | yes | not classified |
    | (i) RECORD-COST-U §14 | no | yes |
    | (ii) PREREG_P | doubtful, since the theories and N = 2 were fixed by hand | yes |
    | (iii) LEMMA_R | doubtful | yes |

  - **Corrected count: FH 4/7**, not 5/7.
  - Counting (iii) is doubtful: LEMMA_R is a proved result, not a test miss, and its content ("the rules are forced once the parts are fixed") arguably fits F2, because the parts were fixed by hand.
  - H3 is an eighth item that neither list classifies.
  - With class boundaries this flexible, either candidate can be fitted after the fact. The counts are not evidence. SR-a stays NOT A TEST.
- **The prior (L2).** "15/15 finite horizons chose a polygon" is corrected to **13 strict wins + 1 tie (T = 1) out of 14 horizons** (ROUND10 §14).
  - The SR-b prior of 0.3 is a judgment. With the weaker tally, 0.2 is defensible, which gives 0.2·4 + 0.8·2 = 2.4, so 2.4/3 h ≈ 0.80 per hour.
  - The ranking conclusion is unchanged: not promoted.
- **Wording (L6).** "Same CORE-method table" is corrected to **"the same §13 table and scale"**. CORE.md has no EIV table.

## 15. C12c after its paper derivation and hostile review (appended 26 Nov 2026, after 08:11 ET; governs §10, §11, §13-6 for C12c)
- **Sources:**
  - C12C_ONSET.md §§0–10 (derivation) and §11 (corrections after HOSTILE_REVIEW_C12C.md, PASS-WITH-FIXES);
  - C12C_LEAN_SPEC.md.
- **§11's C12c HYP, corrected:**
  - "Union of a stake region and a survival region" and "at zero stake, absent iff the cap is slack" are PIM for **stake-free** (accuracy or chance) caps only (Theorem O; class A's corner holds over all memories).
  - For CT22-type caps (stake-carrying, a Lundberg certificate) they are **inapplicable at w = 0**: the cap never binds there, and the band collapses as w → 0.
  - The split is CT33/V3/CT24's existing scope condition applied to onset (credit AUDIT 2026-11-19 Candidate 2).
  - C13-5 is answered in the stake-free classes only.
- **Rescore (reviews and sunk cost not scored):** C12c 0.95 → best forward item 0.78 (C12c-L Lean finite Theorem O, ≈ 2.35 with Lean ×3; C12c-G′ lockable redesign, 0.78; C12c-G as drafted is not lockable).
- **New-route rank:** C4 1.00 · C12b 0.90 · SR-b ≈ 0.87 · C1 0.83 · C12c-L 0.78 · C12c-G′ 0.78 · C3v2 P5² cut ≈ 0.78 · C11 0.72 · C6 0.70.
- **With Lean ×3:** C12c-L ≈ 2.35 and C9 ≈ 1.2. C12c-L goes in as a cheap add-on inside the next Lean round, not as a replacement for C9.

## 16. C4 after its paper step and hostile review (appended 26 Nov 2026, about 09:20 ET; governs §6 Draft C and the C4 rows of §5/§13)
- **Sources:** C4_RECORD_ORDER.md §§1–4 (paper step), §5 (corrections after HOSTILE_REVIEW_C4.md, PASS-WITH-FIXES) and §6 (C4′ one-pager).
- **Draft C:** its design is an **open miss**, because it uses the wrong observable (an exponent rather than the shape ratio R(s)). As written it would read a false Lorentz-like hit. Do not run it. Any future C4 test must use R(s) with a sprinkling control, must state that it is non-blind, and must cite the review.
- **C4 core:** PROVED (in-model) for flat homogeneous 1+1. Light-like chains are long, so the lattice is a preferred frame. Novelty is low.
- **C4′:** **open miss.** No repository cost is boost-invariant in a way that acts on placement. Three CHOSEN inputs would be needed: (I1) a boost-invariant price, (I2) a max-entropy/independence premise, and (I3) records off fixed sites.
- **Rescore:** C4 corrected run ≈ 0.8 (a non-blind check, not recommended); further C4′ work ≈ 0.58.
- **New-route rank (corrected scale, Lean aside):** C12b 0.90 · SR-b ≈ 0.87 (0.80 at prior 0.2) · C1 0.83 · C4 corrected run ≈ 0.8 · C12c-L 0.78 · C12c-G′ 0.78 · C3v2 P5² cut ≈ 0.78 · C11 0.72 · C6 0.70 · C4′ 0.58.
- **With Lean ×3:** C12c-L ≈ 2.35, then C9 ≈ 1.2. The Lemma R spec, a finite statement with no analysis, is a cheap add-on in the same Lean round.

**§16 addendum: a pattern C4′ surfaced (HYP clue only; appended 26 Nov 2026, about 09:15 ET).**
- **The pattern, "placement-blind costs" (PB):** the repo's record costs depend on how many records there are and on their heat rate, not on where or when the records sit. C4′ §6 (F-b, F-c) shows this by inspection for the count terms and the frozen corner.
- **The question:** is PB a single missing input behind several open misses, a specific form of F2?
- **The criterion, written before assigning:** an item counts *yes* only if its own text names the position, arrangement or timing of records as an input that is fixed by hand or missing from the cost. Being "fixed world" alone does not count, and neither does a rate the cost already sees.
- **Assignments, one reader:**

  | item | PB |
  |---|---|
  | gravity | yes (its own text names the lattice as fixed by hand) |
  | U(2) | no |
  | H2 | no |
  | A2 §2 | no (a drift rate, which the cost sees) |
  | (i) RECORD-COST-U §14 | no (the horizon is a parameter the cost already depends on) |
  | (ii) PREREG_P | no |
  | (iii) LEMMA_R | no |
  | H3 | doubtful (set in a lattice vacuum, but its text does not name the lattice as an input) |

  Outside that list:
  - T63 RF-cap: yes. Its text says "the area comes from the heat-shed input, not from the cost".
  - C4′: yes, but it is the source of the pattern, so it is not independent.
  - The frozen corner and the count-only terms: yes, but they are not misses (they are a stated boundary and a property). They are also not independent of C4′.
  - C12b (C12B_ORDER.md): no. Its obstructions are a leak that cancels and a missing continuous-carrier floor, neither of which is about placement.
- **Tally:**
  - PB covers 1 of the 8 earlier items (2 if H3 counts), and independently only 2–3 items in all (gravity, RF-cap), all about spacetime or storage geometry.
  - F2 covered 4 of the 7.
  - So PB is **not** a single cause behind the earlier open misses. At most it is a candidate common input for a small spacetime-structure cluster (gravity, RF-cap area, C4′).
- **Caution:**
  - The criterion was written by a reader who already knew the items, so the count is weak evidence.
  - ROUND10 §14's transport term c·d² is a distance cost, but it sits in design space, not on record positions (C4_RECORD_ORDER §6).
  - **A test that would make PB more than a clue:** add one placement-dependent price (for example a read cost growing with record–reader distance) and check, before running, whether it changes any of the three cluster items while leaving the other five as they are. That is not scored or run here.
- **C12b update** (C12B_ORDER.md §7, governs §10's C12b row):
  - The repair-vs-relearn version is empty at the floor, because the leak cancels while the source is live (T59, PIM, two-state).
  - The track-vs-keep version gives w₁ = kT r/v (PIM) and w₂ ≥ kTΓ/Var on a HYP Gaussian keep floor, so w₂/w₁ ≥ Γ/r at equal variance. In the binary class both thresholds are 0.
  - New row: C12b-G ≈ 1.25.
- **Rank:** C12b-G ≈ 1.25 · SR-b ≈ 0.87 · C1 0.83 · C4 corrected run ≈ 0.8 · C12c-L / C12c-G′ / C3v2 P5² cut ≈ 0.78. With Lean ×3: C12c-L ≈ 2.35, then C9 ≈ 1.2.

**§16 addendum 2: scoring the PB firming test (appended 26 Nov 2026, about 09:45 ET; §13 scale; nothing locked or run).**
- **The test as proposed:** add one placement-dependent price, for example a read cost rising with record-to-reader distance. Predict, before running, that it changes the cluster items (gravity, T63 area cap, C4′) and leaves the other five alone (U(2), H2, A2 §2, RECORD-COST-U §14, PREREG_P).
- **Version 1, as worded ("changes / leaves alone"):**
  - It is close to built in. A placement price changes placement-dependent derivations by construction, and the other five never involve placement. A hit therefore confirms the classification, not the input.
  - Score: p_hit 0.8, V_hit 1; p_miss 0.2, V_miss 3 (a cluster item the price fails to move would show that its missing input is something else). EIV = 0.8 + 0.6 = 1.4.
  - Cost ≈ 4 h, because gravity and C4′ must be re-derived on paper. That gives **≈ 0.35 per hour**.
- **Version 2, sharpened:** predict a specific change, for example "with a distance-priced read, the RF-cap's area scaling follows from the cost without the heat-shed input".
  - Score: p_hit 0.1, V_hit 8; p_miss 0.9, V_miss 2. EIV = 0.8 + 1.8 = 2.6.
  - Cost ≈ 5 h, which gives **≈ 0.52 per hour**.
- **Both score below C1 (0.83).** No design sketch is written, per the brief. PB stays a HYP clue.
- **After C12B_ORDER §8** (the Gaussian keep floor is PIM in class G-keep, conditional on a chosen second-moment cap and a start-before-write premise), the rank is:
  - SR-b ≈ 0.87 · C1 0.83 · C4 corrected run ≈ 0.8 · C12c-L / C12c-G′ / C3v2 P5² cut ≈ 0.78 · C12b-A ≈ 0.77 · PB test ≤ 0.52;
  - with Lean ×3: C12c-L ≈ 2.35, C9 ≈ 1.2, C12b-Lean ≈ 1.0.

**§16 addendum 3: corrections after HOSTILE_REVIEW_C12B.md (PASS-WITH-FIXES; appended 26 Nov 2026, about 09:50 ET; governs addenda 1–2 where they conflict; details in C12B_ORDER.md §9).**
- **C12b ordering.** Addendum 1's "w₂/w₁ ≥ Γ/r at equal variance" and addendum 2's reliance on it are withdrawn. The two thresholds came from different leak models: same-channel for track (CORE.md:90–91, T59) and separate-leak for keep (P1, T63).
  - In one separate-leak world, the track onset is itself ≥ kT·max(r, Γ)/v (PIM lower bound, C12B §9.1). Two lower bounds cannot be ordered.
  - **The C12b ordering is OPEN, an open miss in the stated form**, in both the binary and the Gaussian class.
- **Repair vs relearn empty:** PIM in the same-channel class only. In the separate-leak class Γ does not cancel.
- **What stands:** Proposition G-keep (PIM, separate-leak carriers, chosen cap (A), (W), P3 only after the write), w₂ ≥ kTΓ/Var, and the credit to Horowitz & England 2017 (10.3390/e19070333) for its Steps 1–1′. Novelty is lowered to ELEMENTARY.
- **Pattern tally (L6).** T63 RF-cap is corrected from "yes" to **"doubtful"**. Its input is a boundary heat flux per area, which is region geometry, not record position or timing under the rule as written. PB then covers 1 of the 8 earlier items (2 if H3 counts), and independently 1–2 items in all (gravity; RF-cap doubtful). The conclusion is unchanged and stronger: PB is not a common cause. C12b stays "no": its obstruction is a channel-modeling input (S1), not placement.
- **Rescore:** C12b-A 0.77 → **≈ 0.67 per hour** (V_hit 3 → 2; EIV 0.3·2 + 0.7·2 = 2.0; ≈ 3 h).
- **Rank (Lean aside):** **SR-b ≈ 0.87** (0.80 at prior 0.2) · C1 0.83 · C4 corrected run ≈ 0.8 · C12c-L / C12c-G′ / C3v2 P5² cut ≈ 0.78 · C12b-A ≈ 0.67 · PB test ≤ 0.52. **With Lean ×3:** C12c-L ≈ 2.35 · C9 ≈ 1.2 · C12b-Lean ≈ 1.0.
- **Next:** SR-b (top without Lean, even at prior 0.2) is started in SR_B.md.

**§16 addendum 4: after HOSTILE_REVIEW_SRB.md (PASS-WITH-FIXES; appended 26 Nov 2026, about 10:40 ET; governs addenda 1–3 where they conflict; details in SR_B.md §8 and C12B_ORDER.md §9.7).**
- **C12b.** Addendum 3's "the track onset is itself ≥ kT·max(r, Γ)/v (PIM lower bound)" holds **under the premises of C12B §9.1**: P1–P5 with a live source, (A), (W)/(P3′), IP11's class, and τ → ∞. It is an ELEMENTARY composition (G-keep live + IP11), and attainment is not shown. The ordering stays OPEN, an open miss in the stated form.
- **SR-b.** The miss names a **uniform ratio (competitive) requirement over horizons**, not "worst case over horizons" in general. Additive minimax regret selects a polygon, and minimax cost ties. SR-b1 proves only the "if" direction.
  - With n up to 99,186, a polygon beats the disk at every geometric q ≤ 0.999 (OBSERVED, best n interior), with n* ≈ 0.06–0.1/(1−q)². "Every proper mixture" stays HYP.
  - The (2T+2)-gon beats the disk at every T ≥ 2 under M3h's target rule (PIM, ELEMENTARY). ROUND10's two target rules are flagged for Ace's Friday cleanup.
  - FH (§14) is sharpened from "Bayes versus worst case over horizons" to "Bayes versus **scale-invariant (ratio)** over horizons".
- **Rescore:** SR-b2 0.62 → **≈ 0.67 per hour** (p_hit 0.5).
- **Rank (Lean aside):** C1 0.83 · C4 corrected run ≈ 0.8 · C12c-L / C12c-G′ / C3v2 P5² cut ≈ 0.78 · SR-b2 ≈ 0.67 · C12b-A ≈ 0.67 · PB test ≤ 0.52. **With Lean ×3:** C12c-L ≈ 2.35 · C9 ≈ 1.2 · C12b-Lean ≈ 1.0 · SR-b-Lean ≈ 1.0.

**§16 addendum 5: rank after the C1 first work unit and the C4R prereg draft (appended 26 Nov 2026, about 10:55 ET; §13 scale; details in C1.md §§2–7, which is under fresh review, and c4run/PREREG_DRAFT_C4R.md, a draft that is not locked; governs addendum 4's rank where they conflict).**
- **C1 as stated is resolved by its first unit.**
  - The layer-level shadow-price test is an **open miss** in all four vacua, both critical and gapped (OBSERVED).
  - The single-site first-order bracket and the species identity record(κ, n) = record(κ/n, 1) are ELEMENTARY.
  - Shape: sharp and isotropic in the π-flux (Dirac) vacua; sublattice-ragged and diagonal-elongated in the NN vacua (OBSERVED). That isotropy tracks the vacuum's low-energy symmetry is HYP.
  - Remaining route value as stated is ≈ 0. The follow-up, C1′ (ellipse test on anisotropic π-flux), scores p 0.45, V_hit 3, p_miss 0.45, V_miss 2, EIV 2.25 over ≈ 3 h → **≈ 0.75 per hour**.
- **C4 corrected run (C4R):**
  - The prereg is drafted. The planted-effect gate-read shows that R(s) against the Poisson control detects any plant with ΔR(0.9) ≳ 0.25 in 10/10 batches, and the null reads MISS 10/10.
  - The toy lattice already reads HIT (R(0.9) ≈ 2.03), so the run is a registered check with a known outcome (C5-9). The score stays **≈ 0.8 per hour nominal**, and the run is still "not recommended" beyond the check.
  - New descriptive clue, OBSERVED toy: lattice R(s) for s ≤ 0.9 fits a sprinkling with light speed c′ ≈ 1.96 to within 0.01. That is C4″; it is not scored here.
- **Rank (Lean aside):** C4R ≈ 0.8 (check, pending gate) · C12c-L / C12c-G′ / C3v2 P5² cut ≈ 0.78 · C1′ ≈ 0.75 · SR-b2 ≈ 0.67 · C12b-A ≈ 0.67 · PB test ≤ 0.52.
- **With Lean ×3:** C12c-L ≈ 2.35 · C9 ≈ 1.2 · C12b-Lean ≈ 1.0 · SR-b-Lean ≈ 1.0.

**§16 addendum 6: C1 corrections after HOSTILE_REVIEW_C1.md (PASS-WITH-FIXES; appended 26 Nov 2026, 10:39 ET; details in C1.md §8, which governs C1.md §§1–7; governs addendum 5's C1 bullets and rank where they conflict).**
- **Scored outcomes unchanged.** SP layer test open miss 4/4. V3/V4 pass H1-2D and ISO. V1/V2 open miss on both. The numerics were reproduced independently.
- **Readings corrected:**
  - V1/V2 records are sharp-edged, non-convex X shapes with diagonal arms, not "sublattice-ragged". The checkerboard reading is withdrawn.
  - The first-order bracket holds on the addition side only. The final record is not deletion-stable (4/4), so "stationarity" is withdrawn from the Jacobson 2016 analogy.
  - "Isotropy tracks Lorentz-like symmetry" is not separable: a non-relativistic NN μ = −2 control passes ISO and fill. Kept as OBSERVED: V3/V4 correlations are isotropic within 3–13% at r = 8–24.
- **Also:** the H1-2D radial weight drifted from G4-1 (no score change); ISO is coarse (a 1.25:1 ellipse passes); post hoc, ρ_out < 1 < ρ_in holds 16/16 but pins no price; prior art added (Guestrin–Krause–Singh 2005, Nemhauser–Wolsey–Fisher 1978, Chen–Vidal 2014 and others).
- **C1′ rescored ≈ 0.75 → ≈ 0.5 per hour.** The continuum aspect is already seen in single-site contours (1.68 → 1.97 vs 2.0). A run needs a pre-fixed estimator, a tolerance, a target size, a t_y = 1 control and a correlation-only baseline.
- **Rank (Lean aside):** C4R ≈ 0.8 (check, pending gate) · C12c-L / C12c-G′ / C3v2 P5² cut ≈ 0.78 · SR-b2 ≈ 0.67 · C12b-A ≈ 0.67 · C1′ ≈ 0.5 · PB test ≤ 0.52.
- **With Lean ×3:** unchanged (C12c-L ≈ 2.35 · C9 ≈ 1.2 · C12b-Lean ≈ 1.0 · SR-b-Lean ≈ 1.0).

**§16 addendum 5, continued: C4R shelved (appended about 10:40 ET; decision by the parent, using the theory's own method).**
- **Shelved:** C4R is not locked. Its outcome is known, so the expected information is near zero, while locking and review carry a real cost.
- **Rescore as a check:** ≈ 0.2 per hour.
- **Kept:** the draft, the code and the toy outputs in `c4run/` stay as a ready-made registered check for Ace (PREREG_DRAFT_C4R.md §11).
- **C4″ logged as a HYP:** one c′ ≈ 1.962 fits lattice R(s) for s ≤ 0.9 to within 0.01 (OBSERVED, toy). A quick prior-art search found the nearest relatives in Poisson-line and corner-growth LPP (Seppäläinen 1996, 1998; Martin 2004). It found no exact shape for this symmetric lazy variant and no causal-set "effective light speed" result. Novelty unknown.
- **Rank (Lean aside):** C12c-G′ / C3v2 P5² cut ≈ 0.78 · C1′ ≈ 0.75 (waits for the C1 review) · SR-b2 ≈ 0.67 · C12b-A ≈ 0.67 · PB ≤ 0.52 · C4R ≈ 0.2. C12c-G′ is taken next (C12CG.md).
