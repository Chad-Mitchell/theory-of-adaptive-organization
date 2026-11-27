# TRACKING_FIRST (FOR-41): can a cost of the heat form come out of tracking, instead of being put in?

*26 Nov 2026, written about 18:50–19:05 ET. Local note only (not committed or pushed). New file, append-only from here on. Repo text read at today's main `8b553c641a33` in a fresh clone (`git ls-remote` main = 8b553c6). CORE.md and THEORY.md were read, not edited. Labels: **PIM** = proved in-model; **ELEMENTARY**; **KNOWN** = published and credited; **HYP** = hypothesis; **OBSERVED** = numerical output. An "open miss" is a prediction that did not come out. Nothing in this file is a pre-statement of a scored run, and no route below has been run. Before this file was written, two things were done: a Crossref check of every DOI cited here (`trackfirst/crossref_tf.txt`; 36 DOIs checked, all OK, 35 of them cited here; the 36th, Strasberg et al. 2013, is not used, plus one search showing that the 1999 information-bottleneck paper has no Crossref DOI, `trackfirst/crossref_ib_search.txt`), and a sympy check of the two short algebra items in §3.1 (`trackfirst/tf_paper_checks.py` → `.out`).*

*Target (the owner's message pt168u, in the parent's words): the core "sits on top of thermodynamics". CORE.md:27's J = Q̇ + w·E[ℓ] is priced in kT, with Landauer and learning-rate floors (CORE.md:19–21, :70), so heat and temperature are premises. The aim is to drop that premise and test whether the theory's judgment concept, with the HYP that physical record-keeping is "the universe's way of keeping track of itself", can show how a cost of the heat form arises at all. This file does **not** claim to derive physics, heat, temperature, QM, GR, holography or gravity. It states what a tracking-first result would have to show, what is already known, where the theory already stands without kT, and which small models could test it.*

## 0. Result

1. **Requirements (§1).** A tracking-first result must keep J's structure and drop four premises: kT, Landauer's bound in energy units, a heat bath, and an energy function. It must produce an **exchange rate θ between record nats and the task's currency** that:
   - comes out of the model (a multiplier or shadow price), with no price per nat put in by us;
   - is intensive;
   - is shared, transitively, by trackers coupled only through the record medium's own exchange (Z0), not through a planner we add;
   - obeys a Clausius-type inequality (C1);
   - reduces to kT, with CORE.md:21's floor, when the medium is given an energy and a bath (a consistency check, not a derivation);
   - makes at least one prediction the prior art in §2 does not already make.

   Ten requirements are deleted as ours rather than the target's (§1.5): among them the numerical value of k or T, an energy function as such, one universal temperature for every task, and zero chosen inputs.
2. **Prior art (§2).** Almost every single piece is KNOWN:
   - temperature as a Lagrange multiplier (Jaynes);
   - β as the distortion–rate slope (Shannon, Berger, Blahut, Rose, Tishby);
   - bounded rationality as free energy, with 1/β as the price of information (Ortega & Braun);
   - nats of information ≤ nats of log-growth (Kelly; Rivoire & Leibler);
   - counting forms of Landauer's bound (Bennett; Sagawa & Ueda; Parrondo et al.);
   - a selection temperature (Sella & Hirsh);
   - information paid for in selective deaths (Haldane; Kimura);
   - temperature from a non-physical conserved quantity (Drăgulescu & Yakovenko; Creutz);
   - temperature from order axioms alone (Lieb & Yngvason).

   **A HIT made only of "a multiplier appears and is equal across subsystems that share a budget" would be a relabel.** The gap left (§2.3), as far as found: an exchange rate between record nats and **persistence** (growth or survival), set endogenously by a finite shared **low-entropy medium**, shared or not shared under **selection** rather than a planner. Its failure points (the non-concave "first nat" region, and competitive exclusion) would be part of the content.
3. **Mapping (§3).** Most of the theory's selecting structure and today's positive findings **already sit on the tracking side**. They need a price per nat κ, not kT. These include:
   - R1's priced-sum representation (CORE.md:52);
   - keep/check/fade (CT8, CT9, CT11);
   - CT18's "temperature" z;
   - the selection temperature (CORE.md:122);
   - n_c (P1), P3, P4, P5/P15, P13 (Claim W), P11 (C12CG), P12, P14, P16, P17.

   **kT does structural work only in the floors' class premises** (local detailed balance, the Einstein relation; CORE.md:70) and in T63's repair floor. Everywhere else it is a unit for the per-nat price. One new elementary restatement (PIM, sympy-checked): in the OU class the master-curve variable x = wv/(kT·a) equals θ_task(0)/kT, where θ_task(0) = w·|dε/dİ| at İ = 0 is the task's exchange rate for its first nat. At the optimum, θ_task(İ*) = kT. So x is a **ratio of two exchange rates**, the task's and the medium's.
4. **Routes (§4), ranked by value per hour:**
   - **T1 BLANK-PRICE** (the top route, with a 2 h paper audit T0 as its step 0) is **ready for a pre-statement**: 0.49/h, with T0 at 1.0/h.
   - T3 RUIN-EXCHANGE: 0.39/h.
   - T2 SELECTION-PRICE: 0.30/h.
   - T4 SELF-TRACK: 0.09/h, the long shot and the closest to the "universe keeps track of itself" HYP.

   None is run.
5. **Self hostile review (§5): PASS-WITH-FIXES.** The main finding is the circularity risk. Any constrained optimum has a multiplier, and any shared budget equalizes it, so Z0 "by planner" is automatic. T1's HIT therefore requires Z0 **under selection** or local exchange. The second main finding: a tracking-first route **cannot remove the need for a low-entropy source** (the blank inflow R). It removes energy and kT, not the arrow. That premise stays, disclosed.

## 1. Requirements for a tracking-first result

### 1.1 The target, stated precisely (HYP to be tested, not a claim)

> **TF.** There is a class of models built only from §1.3's primitives, with no energy function, no bath and no kT, in which (a) the cost of holding records against a changing world takes the form θ × (nats per unit time), where θ is an exchange rate that the model determines; (b) θ has the formal properties §1.4 lists; and (c) when the medium is additionally given an energy and a bath at temperature T, θ maps to kT, and CORE.md:21's floor Q̇ ≥ kT × learning rate is recovered as a special case.

"Of the heat form" means exactly (a): **linear in nats, with one intensive coefficient**. It does not mean energy.

### 1.2 Premises that must be dropped (and where each enters today)

| premise | where it enters today | drop? |
|---|---|---|
| kT as the price of a nat | CORE.md:21, :70, :74, :76, :90–:94; README.md:13's x = wv/(kT·a); SELF_HORIZON §8.2's x = w/kT; WORLD_TRACK §1.2 (all costs in kT units) | **Drop.** Replace it by an exchange rate θ that the model must produce |
| Landauer's bound in energy units (kT ln 2 per erased bit) | SH-heat read cost; WORLD_TRACK §1.2 item 2 (Sagawa & Ueda 2009) | **Drop the energy form. Keep the counting form** (a bijection cannot reduce total entropy; §1.3 P-rev). That is a statement about counting, not about heat |
| A heat bath at temperature T | CORE.md:19 (Horowitz & Esposito 2014), :70 (local detailed balance, Einstein relation) | **Drop** |
| An energy function | implicit in "heat" and in every floor's class premise | **Drop.** An additive budgeted quantity may appear only if the model produces it (§1.4 O5) |
| The stake currency "of the heat" (CORE.md:29: "w converts the loss into the currency of the heat") | CORE.md:29 | **Replace** the target currency by persistence (log-growth or survival probability), measured in nats where possible. w may stay as a task input (CORE.md:23); only its "heat" currency goes |

### 1.3 Allowed primitives (minimal)

- **P-world:** a tracked process with given statistics (a Markov chain, OU, or telegraph). This is the theory's only world input (THEORY.md:197).
- **P-rec:** records, meaning finite registers whose state carries mutual information with the world. The memory coordinate is mutual information (CORE.md:52, R1/A6).
- **P-cap:** bounded judgment. This is a finite record capacity, a finite read rate, or a finite medium of cells.
- **P-pers:** persistence/selection. Records or their carriers persist or replicate according to how well they track (CORE.md:122; THEORY §3's selection).
- **P-leak:** a medium leak Γ. Cells randomize at a rate. This is a medium property (REQUIREMENTS_FIRST §5.3).
- **P-rev (optional):** reversibility. Global updates are bijections on the joint state of world, records and medium. Only counting is used.
- **P-count:** counting. Entropies and nats; logarithms of state counts.
- **P-src (forced; see §5 H2):** a supply of low-entropy cells ("blanks") at rate R. Without it, P-rev and P-leak make every record decay. This is the one premise with physical content that cannot be dropped. It is the arrow, not the energy.

### 1.4 What output counts (all six needed for a HIT on TF)

- **O1. Endogenous exchange rate.** θ = −∂(minimized task cost)/∂(nats of record supply), or the multiplier on the medium's constraint. It is computed, not chosen.
- **O2. Intensive.** θ is unchanged when the system is replicated and the medium scaled with it (degree-0 homogeneity).
- **O3. Z0, transitive equilibrium.** Trackers A, B and C, coupled **only through the medium's own exchange of cells or records**, reach a stationary state with θ_A = θ_B = θ_C. Coupling A–B and B–C fixes A–C. **Equalization imposed by a joint optimizer that we write down does not count** (§5 H1).
- **O4. C1, Clausius-type inequality.** For a cyclic change of the world's statistics, the integral of (nats drawn from the medium) is at least the integral of (task-currency change)/θ, with equality only for quasi-static changes. In its envelope form, dJ*/dθ = İ* holds (Shephard type).
- **O5. Reduction.** Give each cell an energy and connect the medium to a bath at T. Then θ maps to kT (up to the conversion between the task currency and energy, which must be named), and CORE.md:21 is recovered. This is a consistency check. It does not derive kT.
- **O6. Non-relabel.** At least one prediction that §2's prior art does not already make. Candidates: where θ fails to exist (the non-concave region), and whether Z0 survives selection (competitive exclusion).

### 1.5 Requirement ledger (Musk algorithm: question each one, delete what is ours)

| # | requirement | source | kept or deleted, and why |
|---|---|---|---|
| 1 | No kT, Landauer (energy form), bath or energy in the premises | target (pt168u) | **Kept** (§1.2) |
| 2 | Primitives limited to §1.3 | target | **Kept** |
| 3 | O1–O6 | target, made operational | **Kept** |
| 4 | Derive the numerical value of k, or of any T | us | **Deleted.** k is a unit conversion. The target is the form and the properties, not a number |
| 5 | Derive energy as such | us | **Deleted.** The target needs an additive budgeted quantity with a multiplier (O1, O5). Energy is one instance |
| 6 | One universal temperature for every task | us | **Deleted.** Physics has one T per bath, not per universe. Z0 is needed only among trackers that share a medium. CORE.md:29: "Temperature does not set w" |
| 7 | Zero chosen inputs | us (REQUIREMENTS_FIRST row 15) | **Deleted.** World statistics, w, ε, Γ and R stay as world or medium inputs (CORE.md:23) |
| 8 | Equilibrium (detailed balance) | us, by analogy with thermodynamics | **Deleted.** Tracking is a non-equilibrium steady state. Z0 is needed only at the stationary state |
| 9 | Tightness of the floor in every class | us | **Deleted.** CORE.md:70 claims tightness only in named classes |
| 10 | Every part new | us | **Deleted.** As THEORY.md:197 says, the parts may be known and the package new. O6 asks for one non-relabelled prediction |
| 11 | A time or dynamics derived from tracking (Caticha-type) | us | **Deleted.** It is not needed for a heat-form cost, and it borders on the banned claims |
| 12 | Recovering T63's factor 4 | us | **Deleted.** The factor is specific to class RF |
| 13 | Removing the low-entropy source | us (an over-reading of "remove thermodynamics") | **Deleted as impossible within P-rev + P-leak.** Kept as the disclosed premise P-src (§5 H2) |
| 14 | A unique design | us (REQUIREMENTS_FIRST row 14) | **Deleted.** The target is a price, not a point |

**Count:** 14 rows. 10 deleted (4–13 are ours; 14 is a carry-over). 3 kept (1–3), plus P-src kept as a disclosed premise.

## 2. Prior art: what is already known, so that it is not relabelled

Every DOI below was checked on Crossref this session (`trackfirst/crossref_tf.txt`, all OK). Items without a DOI are marked as such.

### 2.1 What each source already establishes

| source | what it already establishes | what it covers in TF |
|---|---|---|
| Jaynes 1957a,b, *Phys. Rev.* 106:620, 10.1103/PhysRev.106.620; 108:171, 10.1103/PhysRev.108.171 | Maximum entropy subject to a given expectation constraint gives the Boltzmann form, with β the Lagrange multiplier. Temperature is the multiplier of a conserved quantity **that is given** | O1 and O3 for any budgeted additive quantity. **A HIT that is only "a multiplier appears" is Jaynes** |
| Landauer 1961, *IBM J. Res. Dev.* 5:183, 10.1147/rd.53.0183; Bennett 1982, *Int. J. Theor. Phys.* 21:905, 10.1007/BF02084158; Bennett 2003, *Stud. Hist. Phil. Mod. Phys.* 34:501, 10.1016/S1355-2198(03)00039-X | Logically irreversible erasure must raise the entropy of the rest by at least ln 2 per bit. In counting form this is a property of bijections. kT ln 2 follows once the rest is a bath at T | The counting form of P-rev, and O5's reduction. **The "nats out" half of the heat form is KNOWN** |
| Sagawa & Ueda 2009, *PRL* 102:250602, 10.1103/PhysRevLett.102.250602 | Measurement plus erasure together cost at least kT × the mutual information | O5 in the measurement setting |
| Parrondo, Horowitz & Sagawa 2015, *Nat. Phys.* 11:131, 10.1038/nphys3230 | Review. Information is a thermodynamic resource; mutual information enters the second-principle inequality with a kT exchange rate | The Clausius-type inequality with information (O4), **given a bath** |
| Horowitz & Esposito 2014, *PRX* 4:031015, 10.1103/PhysRevX.4.031015 | Bipartite learning rate; heat ≥ kT × learning rate | CORE.md:21 itself. O5's target |
| Still, Sivak, Bell & Crooks 2012, *PRL* 109:120604, 10.1103/PhysRevLett.109.120604 | Dissipation in a driven system is bounded below by kT × its **non-predictive** information (memory minus predictive power) | The tie between prediction and heat, **given a bath**. The tracking-side analogue (non-predictive nats are waste) is in its form |
| Kolchinsky & Wolpert 2018, *Interface Focus* 8:20180041, 10.1098/rsfs.2018.0041 | Semantic information is the information about the environment that is causally necessary for a system to **keep existing** (its viability), defined by interventions. Thermodynamic accounting is attached | The closest prior art to P-pers: "information valued by persistence". It defines **which** nats matter. It does not give an endogenous exchange rate shared across systems |
| Shannon 1959, rate–distortion with a fidelity criterion (IRE Nat. Conv. Rec.; **no DOI**); Berger 1971, *Rate Distortion Theory* (book; **no DOI**); Blahut 1972, *IEEE TIT* 18:460, 10.1109/TIT.1972.1054855 | The minimizer of distortion + (1/β)·rate has the Boltzmann form p(y\|x) ∝ q(y)·e^{−β d(x,y)}. β is the (negative) slope of the convex R(D) curve | O1 for a capacity constraint: **β is the exchange rate between distortion and nats** |
| Rose, Gurewitz & Fox 1990, *PRL* 65:945, 10.1103/PhysRevLett.65.945; Rose 1998, *Proc. IEEE* 86:2210, 10.1109/5.726788 | Deterministic annealing. β behaves as an inverse temperature, with **phase transitions** (cluster splits) at critical β | Temperature-like behaviour of the RD multiplier, including critical points. **Partial cover of the gap in §2.3 G3** |
| Tishby, Pereira & Bialek 1999, *The information bottleneck method* (Allerton; arXiv:physics/0004057; **no Crossref DOI**, `crossref_ib_search.txt`); Bialek, Nemenman & Tishby 2001, *Neural Comput.* 13:2409, 10.1162/089976601753195969 | β trades compression against relevant (predictive) information. Predictive information I(past; future) is the relevant quantity | O1 for predictive tracking. The B11 bound's quantity (THEORY.md:408) |
| Ortega & Braun 2013, *Proc. R. Soc. A* 469:20120683, 10.1098/rspa.2012.0683 | Bounded rationality is free-energy minimization: utility − (1/β)·KL(posterior‖prior). 1/β is the **price of information processing**, and the formalism is "thermodynamics as a theory of decision-making". β is a **given** resource parameter | **The strongest relabel risk.** "A decision-maker with an information cost looks thermodynamic" is theirs. They do not derive β from a shared medium or from persistence |
| Sims 2003, *J. Monet. Econ.* 50:665, 10.1016/S0304-3932(03)00029-1 | Rational inattention: a capacity or price on mutual information. The shadow price of capacity | O1 in economics |
| Todorov 2009, *PNAS* 106:11478, 10.1073/pnas.0710743106; Kappen 2005, *J. Stat. Mech.* P11011, 10.1088/1742-5468/2005/11/P11011 | KL-control and path-integral control. The control cost in nats, with a temperature λ, gives linear Bellman equations | The control analogue of O1, with λ given |
| Friston 2010, *Nat. Rev. Neurosci.* 11:127, 10.1038/nrn2787 | Variational free energy bounds surprise. Self-maintaining systems are described as minimizing it | The "persistence ↔ free energy" story at the level of description. It gives no endogenous exchange rate, Z0 or C1 test, and its "free energy" carries no kT |
| Caticha 2011, *J. Phys. A* 44:225303, 10.1088/1751-8113/44/22/225303 | Entropic dynamics: dynamics obtained from maximum-entropy inference with constraints | The idea that physics comes from inference with constraints. Not used here, and no claim is built on it (§1.5 row 11) |
| Wheeler 1992, *Ann. N.Y. Acad. Sci.* (Crossref title: "Recent Thinking about the Nature of the Physical World: It from Bit"), 10.1111/j.1749-6632.1992.tb17083.x | "It from bit". A program statement, not a model | The motivating HYP. Nothing testable to relabel |
| Kelly 1956, *BSTJ* 35:917, 10.1002/j.1538-7305.1956.tb03809.x; Rivoire & Leibler 2011, *J. Stat. Phys.* 142:1124, 10.1007/s10955-011-0166-2 | Under proportional betting, side information raises log-growth by at most the mutual information. **One nat of information is worth at most one nat of growth.** For populations: the value of information ≤ information | A **native, kT-free exchange rate (≤ 1) between information and persistence**. It does not include the cost of holding records in a finite medium |
| Sella & Hirsh 2005, *PNAS* 102:9541, 10.1073/pnas.0501865102 | Weak-mutation selection gives a Boltzmann stationary distribution in fitness, with 1/(effective population size) playing temperature | CORE.md:122's selection temperature (π ∝ e^{−βJ}, excess d/(2β), equipartition in form) |
| Haldane 1957, *J. Genet.* 55:511, 10.1007/BF02984069; Kimura 1961, *Genet. Res.* 2:127, 10.1017/S0016672300000616; Eigen 1971, *Naturwiss.* 58:465, 10.1007/BF00623322; Frank 2012, *J. Evol. Biol.* 25:2377, 10.1111/jeb.12010 | The cost of selection in selective deaths. Kimura reads adaptive evolution as accumulating genetic information, paid for in that cost. Eigen's error threshold caps the information that mutation–selection can keep. Frank reads selection equations as information | **A price per nat paid in persistence (deaths), with no kT**, and a persistence cap from counting. T2's relabel risk |
| Drăgulescu & Yakovenko 2000, *EPJ B* 17:723, 10.1007/s100510070114; Creutz 1983, *PRL* 50:1411, 10.1103/PhysRevLett.50.1411 | A conserved non-physical quantity (money) exchanged at random gives a Boltzmann–Gibbs distribution, with "temperature" = mean holding. Creutz: a demon exchanging a conserved quantity with a closed system measures its temperature by counting | O1–O3 from **any** conserved exchanged quantity. **T4's relabel risk.** THEORY already credits DY2000 as an analogy for CT18 |
| Lieb & Yngvason 1999, *Phys. Rep.* 310:1, 10.1016/S0370-1573(98)00082-9 | Entropy and temperature follow from order axioms on adiabatic accessibility, with no statistical mechanics | An axiomatic route to O1–O4 that **does not need counting either**. A tracking-first axiomatics would have to say what it adds beyond this |
| Baez, Fritz & Leinster 2011, *Entropy* 13:1945, 10.3390/e13111945 | Up to a constant, Shannon entropy difference is the unique functorial, convex-linear measure of information loss | **Why the cost is linear in nats with one coefficient** (the "heat form", §1.1 (a)) is KNOWN in kind. Compare CORE.md:52 (R1), which gets the additive price sum from preference axioms |
| Wolpert 2019, *J. Phys. A* 52:193001, 10.1088/1751-8121/ab0850 | Review of the stochastic thermodynamics of computation | Context for O5 |
| Gish & Pierce 1968, *IEEE TIT* 14:676, 10.1109/TIT.1968.1054193 | Entropy-coded quantizer sizing | n_c-type scales (P1) |
| Jacobson 1995, *PRL* 75:1260, 10.1103/PhysRevLett.75.1260 | (Cited by PHYSICS_CHAIN.) | **Not used. No gravity claim is made or implied** |

### 2.2 Compressed: what is already covered

- **The form.** "Cost linear in nats with one coefficient" is covered by Baez–Fritz–Leinster in kind, and by CORE.md:52's R1 for the theory's own cost.
- **The multiplier.** "The coefficient is a Lagrange multiplier or shadow price, and behaves like an inverse temperature" is covered by Jaynes, Shannon/Berger/Blahut, Rose, Tishby, Sims, Ortega–Braun and Todorov/Kappen.
- **Z0 under a shared budget.** "Subsystems sharing one budget equalize the multiplier" is KKT, Jaynes, reverse water-filling, and competitive equilibrium. It is KNOWN and automatic.
- **Counting Landauer.** "Getting nats into records costs nats out elsewhere" is covered by Landauer, Bennett, Sagawa–Ueda and Parrondo et al.
- **Persistence currency.** "Nats of information ↔ nats of growth, with rate ≤ 1" is covered by Kelly and Rivoire–Leibler. "Price per nat in selective deaths" is covered by Haldane, Kimura and Eigen. "Information that matters is what keeps the system existing" is covered by Kolchinsky–Wolpert.
- **Temperature without physics.** This is covered by Drăgulescu–Yakovenko, Creutz, Sella–Hirsh and Lieb–Yngvason.

### 2.3 The gap: what is not covered (as far as found; the search is not exhaustive)

- **G1. An endogenous per-nat price from a finite shared record medium, valued in persistence.**
  - None of the sources above has, in one model: the price of a record nat set as the shadow price of a finite low-entropy supply (blanks, P-src); valued in persistence (log-growth or survival, not a given utility); and tested for Z0 **under selection among lineages** rather than a planner.
  - Ortega–Braun and Todorov take β as given. Kelly and Rivoire–Leibler have no medium cost. Kolchinsky–Wolpert do not form a shared exchange rate. Jaynes and DY2000 need the conserved quantity given.
  - **Ecological prior art not yet searched:** resource-competition theory (R*, competitive exclusion). It may cover the selection arm's MISS mode. To be searched before any pre-statement of T1.
- **G2. Tie between the selection temperature and the medium price.** At a selected stationary state, what relates CORE.md:122's 1/β_sel to the per-nat price of the record medium? Sella–Hirsh have no information medium, and Kimura has no medium price.
- **G3. Where an exchange rate exists at all.**
  - **Partial cover:** rate–distortion has known critical β (Rose 1990), and the non-concave value of information is credited in THEORY (Radner & Stiglitz 1984; no DOI checked here).
  - What is not found: CORE.md:91's threshold (x = 1) read as "the medium's rate exceeds the task's first-nat rate", and whether Z0 fails below it.
- **G4. An upkeep floor in nats from counting under a leak.** T63's informational factor Γ·(ln 2 − h(ε)) written as a blank-consumption floor with no kT. The principle is KNOWN (Landauer/Bennett). The specific floor may be in the error-correction literature, which was **not searched**. OPEN.

## 3. Mapping: which results already sit on the tracking side

### 3.1 Two short algebra items (PIM, ELEMENTARY; sympy-checked in `trackfirst/tf_paper_checks.out`; self-checked only)

- **M-x (the master curve as a ratio of exchange rates).** In CORE.md:90–91's OU class:
  - The heat infimum kT·a(v − ε)/ε gives a learning rate İ(ε) = a(v − ε)/ε, so ε(İ) = av/(İ + a).
  - Define the task's exchange rate θ_task(İ) := w·|dε/dİ|.
  - Then θ_task(0) = wv/a, so **x = wv/(kT·a) = θ_task(0)/kT**.
  - The interior minimizer of kT·İ + w·ε(İ) satisfies **θ_task(İ*) = kT**, and J* = 2√(kT·a·v·w) − kT·a.
  - The envelope relation dJ*/d(kT) = İ* holds (O4's Shephard form).
  - **Reading:** "memory pays" (x > 1) means the task values its first nat above the medium's price per nat. At the optimum the two rates are equal. kT enters only as the medium's rate. This is a restatement (marginal analysis, KNOWN in kind: Sims 2003; Shephard as credited in THEORY), not a new result.
- **M-tel (no threshold on the telegraph's continuous infimum).** On the telegraph floor (CORE.md:74), J(ε) = kT·r·L(ε) + w·ε with L = (1 − 2ε)·ln((1 − ε)/ε).
  - dL/dε = 0 at ε = ½, so dJ/dε = w > 0 at chance. Any w > 0 makes some memory pay. Equivalently, θ_task(0) = ∞.
  - So the x = 1 threshold of the OU class is **not** a generic feature of the continuous infimum. The "first bit must pay" threshold (CT4; README.md:36) applies to discrete memories with a per-bit price.
  - **Caveat:** the infimum is approached, not attained (CORE.md:74), and T59/T60 may already state this. That was not checked.

### 3.2 Mapping table

"Tracking side" means: the result holds with a generic price κ per nat (or no price at all) in place of kT, and no premise of the result uses a bath, an energy function or detailed balance.

| result | where | side | why |
|---|---|---|---|
| R1: the cost is an additive price sum, with mutual information as the memory coordinate | CORE.md:52; `theory/REPRESENTATION.md` | **tracking** | It comes from preference axioms A1–A7. The price κ is free |
| THEORY §3's five-term sum, with κ per nat | THEORY.md:26; CORE.md:33–:47 | **tracking** | κ is a price per nat. kT is only its floor in the physical class (CORE.md:39 row 1) |
| The information floor: memory pays for the predictive information it holds (S1, CT1, CT4) | CORE.md:48; `theory/SHANNON_2026-11-21.md` | **tracking** | It is in nats. The price is generic |
| B11: forecast miss = predictive information not carried | THEORY.md:408 | **tracking** | Pure information |
| CT8 (staleness is monotone), CT9 (hold or fade: λc < Φ), CT10, CT11 (freeze/hold/look up) | THEORY.md:305–:328 | **tracking** | Priced in a read price c, an upkeep h and the stake. No kT |
| CT18/CT18-H "temperature identity" z = B/(σ·τ^H); CT25 | THEORY.md:392–:402 | **tracking** | A dimensionless group (Buckingham π). It is a "temperature" by analogy only (DY2000, as credited) |
| Selection temperature: π ∝ e^{−βJ}, excess d/(2β) | CORE.md:122 | **tracking** | β comes from selection strength (Sella–Hirsh). Equipartition in form |
| Worked-class minimizers in x (layer count ⌊log(wv/(kT·a))/log ρ⌋ + 1, J*) | CORE.md:90–:93; README.md:13 | **tracking up to unit** | kT appears only inside x, as the medium's price per nat (M-x). The same algebra holds with κ |
| P1: n_c ≈ 4/(σ√(2 ln(1/σ))) | REQUIREMENTS_FIRST §4 | **tracking** | Medium noise against resolution. KNOWN in form (Gish–Pierce) |
| P3: the keep edge n_b, nearly x-free | same | **tracking** (location); its existence uses the keep floor (below) | — |
| P4: a read price removes the check band | same | **tracking** | A world price. No kT |
| P5/P15: on a geometric loss a polygon never beats the disk (weak domination) | REQUIREMENTS_FIRST §10 | **tracking** | Geometry of effects. No cost of the heat form at all |
| P14, SR-b3: reach losses select polygons | SR_B | **tracking** | A move cost d² or g(d). No kT |
| P13: Claim W counterexamples (target rule, quantifier order) | SELF_HORIZON §11.6 | **tracking** | They hold at absent w |
| P11: the C12CG gap (unsupported Pareto points) | C12CG §§3, 9, 11 | **tracking** | Lemma G is a fact about menus (Everett 1963, as credited) |
| P12: the pentagon carries ≈ 1.02 bits | C12CG §11(d) | **tracking** | A capacity of a state space |
| P16: no symmetry breaking in #292 | branch RESULTS | **tracking** | — |
| P17: EVO1, selection reaches argmin J | CLAIM_MAP_v2 | **tracking** | A search on any J |
| WORLD_TRACK Step 0 (one switch α*) | WORLD_TRACK §0.9 | **tracking** | A geometric versus operational loss mix |
| P2: the keep-or-fade band T = 2/x, n* ≈ 4/x + 2 | SELF_HORIZON §9 | **tracking up to unit, plus the keep floor's class** | x = w/kT is a unit ratio. The band's existence uses the keep floor c_K·Γ·I (next row) |
| WORLD_TRACK Step 1 (pre-stated, not run) | WORLD_TRACK §1.2 | **tracking up to unit, plus the keep floor's class** | Every cost is in nats × kT. Replacing kT by κ changes nothing in the algebra |
| **The learning-rate floor Q̇ ≥ kT × İ (KNOWN/PIM in classes)** | CORE.md:19–21, :70; T57–T61 | **needs kT** | Its premises are local detailed balance or the Einstein relation, which are physics. The **informational** content (İ, Φ(d), the T60 KL-flux identity) is tracking-side. Only "price per nat ≥ kT" is physical |
| Telegraph and OU floors' tightness, and the factor 2 (Kalman versus fast spring) | CORE.md:74–:76 | **needs kT** for "heat". The İ-level statements are tracking-side | — |
| T63: repair floor 4kTΓ(ln 2 − h(ε)) | PHYSICS_CHAIN Link 3; `RECORD_REPAIR_FLOOR` | **mixed** | Γ·(ln 2 − h(ε)) is a counting rate (G4). kT and the 4 come from class RF's physics |
| The keep floor c_K·Γ·I (G-keep; C12B §9) | C12B_ORDER | **mixed** | Same as T63 |
| "Frozen worlds allow zero ongoing heat" | CORE.md:78 | **tracking** in substance | A disconnected or frozen world needs no learning rate. The "heat" is the kT image |

**Reading (OBSERVED, from the table; a judgment about the text, not a theorem).** The theory's selecting structure is on the tracking side. It needs a per-nat price, and the price's **value** is where kT enters. kT does structural work only in the floor classes' physical premises and in the repair or keep floors' coefficients. So "the core sits on top of thermodynamics" is true of CORE's **display** (CORE.md:27 and §3), and much less true of its **structure**: THEORY.md:19 already says that above the cell the floors are slack and the claim is about the economics of judgment, not about thermodynamics. What tracking-first must supply is narrow: **where the per-nat price comes from, and whether it behaves like a temperature.**

## 4. Routes (ranked; none run)

*The scale is as in REQUIREMENTS_FIRST §7: EIV = p·V_HIT + (1 − p)·V_MISS; value per hour = EIV/cost. Scores are judgments.*

### Step 0 for T1. T0 CURRENCY AUDIT (paper)

- **Question.** In every worked class of CORE §§3–4 and today's SH-*/WORLD_TRACK models, does kT enter **only** through the ratio (task rate)/(medium rate), i.e. through x-type groups, once the floors are written as κ × (nats)?
- **Method.** Substitute κ for kT and check, line by line, that every minimizer and every threshold depends on kT only through θ_task/κ. List every exception.
- **HIT:** no exception outside the floor premises (§3.2's "needs kT" rows).
- **MISS:** some selecting result uses kT structurally. That would be very informative: it would be a place where thermodynamics does real work in the design.
- **OPEN:** a class where the floor and the design cannot be separated.
- **Triviality:** if it HITs, it is ELEMENTARY (dimensional analysis; THEORY.md B12's S1 already gives currency covariance). Its value is a precise map for the owner of where thermodynamics enters.
- **Score:** p 0.85, V_HIT 2, V_MISS 2.5. EIV 2.08, about 2 h → **1.0/h**.

### T1. BLANK-PRICE (**top route; ready for a pre-statement**, not run)

- **Question.** In a medium with no energy, does an exchange rate θ between record nats and persistence nats emerge? Is it intensive? Does it satisfy Z0 among trackers coupled only through the medium, **under selection and not only under a planner**? Does it reduce to kT when the cells are thermal?
- **Minimal model (primitives P-world, P-rec, P-cap, P-pers, P-leak, P-rev, P-count, P-src only).**
  - **Worlds:** K = 3 telegraph worlds with rates r_k (P-world).
  - **Trackers:** each world has a two-state record at error ε_k. Its learning rate is İ_k = r_k·L(ε_k) nats per unit time, the information-theoretic content of CORE.md:74, with no kT.
  - **Medium:** a pool of N binary cells, each blank or used. Writing İ nats needs at least İ/ln 2 blanks per unit time to become used, the counting Landauer form under P-rev. That is a lemma to prove in-model as part of the run. Used cells return to blank only through the inflow R. Cells leak at rate Γ.
  - **Currency:** persistence. Each tracker's carrier is a lineage betting Kelly-style on its world (fair odds 2). Its log-growth is G_k = ν·(ln 2 − h(ε_k)) (Kelly; Rivoire–Leibler). All quantities are in nats; nothing is in energy.
  - **Arm P (planner, the gate):** one organism carries all K trackers and maximizes Σ G_k subject to Σ İ_k/ln 2 ≤ R. Expected: θ := ∂(Σ G*)/∂R is equal across k by KKT. This arm is a **reproduction gate, not evidence**.
  - **Arm S (selection, scored):** K lineages share the pool. Uptake is local: each lineage takes blanks in proportion to a heritable demand d_k. Weak-mutation selection runs on d_k and ε_k, with fitness = its own G_k minus the growth forgone while waiting for blanks. Measure each lineage's marginal rate θ_k = ∂G_k/∂(blank rate) at the stationary state.
  - **Arm L (local exchange, scored):** pools per tracker, linked by random cell swaps at rate g, with no agency. This tests Z0 by diffusion (the Jaynes/Creutz analogue), with the counting multiplier β_pool = ln((1 − ρ)/ρ) at blank density ρ.
  - **Reduction arm (O5):** give each cell energy E_c and a bath at T. Check that θ × (growth-to-energy yield) maps to kT ln 2 per bit. **The yield is a chosen conversion and is disclosed.**
- **HIT (all needed):**
  1. Arm P reproduces KKT equalization (the gate).
  2. In Arm S or Arm L, the stationary θ_k are equal within 5% across coexisting trackers, and transitive (A–B, B–C ⇒ A–C) over all 3 pairs.
  3. θ is intensive under N → 2N, R → 2R.
  4. C1: over a slow cycle of r_k, (blanks used) ≥ ∮dG/θ, with equality approached as the cycle slows.
  5. O5 maps to kT ln 2 per bit up to the disclosed yield.
  6. **O6:** a non-relabelled prediction. The pre-stated candidate: θ is undefined, or Z0 fails, in the non-concave or threshold region (G3), at a location set by the world's statistics.
- **MISS:**
  - In Arm S, competitive exclusion: only one lineage persists on the single pool, so Z0 cannot even be posed. This is a likely failure mode, and the ecological prior art is unsearched (G1).
  - Or θ is not equal or not transitive.
  - Or C1 fails.
- **OPEN:** Arm S equalizes only with an added rule (a price signal) that we chose.
- **Triviality test (stated now).**
  - Arm P equalization is KKT/Jaynes: **trivial by construction**.
  - Arm L equalization with a conserved blank count is Jaynes/Creutz/DY2000 with blanks in place of energy or money: **a relabel unless** the conserved quantity emerges from tracking rather than being put in.
  - Only Arm S Z0, G3's threshold structure, and G2's tie (θ against β_sel) count as non-trivial.
  - O5 is a consistency check and is never cited as a derivation.
- **What a HIT would and would not show.**
  - It **would** show that a heat-form cost (θ × nats) with Z0 and C1 arises in a tracking-only medium valued in persistence. That is a proved-in-model or observed statement in one class.
  - It would **not** show that physical temperature "is" this θ, and nothing about physics follows.
  - The low-entropy inflow R remains a premise (§5 H2).
- **Prior art to cite (Crossref OK):** Jaynes 1957; Landauer 1961; Bennett 1982; Kelly 1956; Rivoire & Leibler 2011; Ortega & Braun 2013; Kolchinsky & Wolpert 2018; Creutz 1983; Drăgulescu & Yakovenko 2000; Sella & Hirsh 2005; Rose et al. 1990.
- **Score:** p 0.45, V_HIT 3.5 (a heat-form cost with Z0 under selection, kT-free), V_MISS 2.5 (a clean structural miss, such as competitive exclusion, is informative for the owner's HYP). EIV 2.95, about 6 h → **0.49/h**. With T0 first: about 8 h in total.

### T3. RUIN-EXCHANGE (persistence sets the rate)

- **Question.** With survival under a ruin cap as the only objective (no w), is the exchange rate θ_ruin := −∂ln P(ruin)/∂(nats of record) a function of the CT18 group z and the world alone? Does pooling two trackers on one reserve move θ as CT25's pooling rule z′ = z·√(N/(1 + (N − 1)ρ)) predicts?
- **Model.** An OU world. The tracker's error sets the reserve drift. Fixes act on scale τ. The cost is the record nats drawn from the reserve at the Kelly rate (nats of growth). The reserve follows CT18/Lemma B8.
- **HIT:** θ_ruin collapses on z within 5% across (σ, τ, B) at fixed z, for each fixing mechanism; the pooled θ follows z′ within 10%.
- **MISS:** no collapse.
- **OPEN:** a collapse only at one H.
- **Triviality:** the collapse on z is Buckingham π (CT18 already proves the hazard is F(z)/τ). Only a θ–z map with a stated form, and the pooling test, are content. Under Kelly, θ ≤ 1 is KNOWN.
- **Score:** p 0.45, V_HIT 2.5, V_MISS 1.5. EIV 1.95, about 5 h → **0.39/h**.

### T2. SELECTION-PRICE (price per nat in persistence)

- **Question.** In a Wright–Fisher population tracking a telegraph world, define the price per nat κ_sel = (selective deaths per generation) / (nats about the world kept by the population per generation). Is κ_sel intensive? Is it equal across loci tracking different worlds in one population (Z0 through a shared load)? Does it relate to CORE.md:122's β_sel = 2N_e·s-type scale as a temperature would (G2)?
- **HIT:** κ_sel is equal across loci within 10% at stationarity; κ_sel·β_sel is constant across N_e; Kimura's 1961 bound is reproduced as the gate.
- **MISS:** loci do not equalize (no shared constraint), or the β_sel relation fails.
- **Triviality:** Kimura 1961 and Haldane 1957 already price information in deaths, so the gate reproduction is KNOWN. Only the β_sel tie (G2) and Z0 across loci would be new.
- **Score:** p 0.4, V_HIT 3, V_MISS 1.5. EIV 2.1, about 7 h → **0.30/h**.

### T4. SELF-TRACK (the closest to the owner's HYP; the long shot)

- **Question.** In a closed, reversible network of records with **no external world**, where each record tracks its neighbours under bounded capacity and a leak (a lattice or ring; heterogeneous rates; P16's mirror setting made heterogeneous), does:
  - an additive conserved quantity **emerge** (be identifiable from the dynamics, not put in), and
  - a single exchange rate appear with Z0 and C1, with no planner and no inflow other than the network's own low-entropy initial condition?
- **HIT:** O1–O4 with the conserved quantity found, not imposed.
- **MISS:** no conserved additive quantity beyond those we built in; or no common rate; or, as in P16, no structure.
- **Triviality:** if the conserved quantity is the bijection's total entropy or a cell count we put in, it is Creutz/DY2000/Jaynes. That is a relabel.
- **Score:** p 0.1, V_HIT 5, V_MISS 1.5. EIV 1.85, about 20 h → **0.09/h**.

### Ranking

- By value per hour: **T0 (1.0) > T1 (0.49) > T3 (0.39) > T2 (0.30) > T4 (0.09).**
- **Recommended:** T1, with T0 as its step 0, **ready for a pre-statement**. Before the pre-statement is written, search the resource-competition literature (R*, competitive exclusion) and lock Arm S's uptake rule. Then T3, then T2. T4 waits for a T1 HIT.

## 5. Self hostile review: **PASS-WITH-FIXES**

- **H1, high: circularity.** Any constrained optimum has a multiplier, and any budget shared by a planner equalizes it.
  - So O1 and O3 "by planner" are true by construction. A HIT built on them would relabel Jaynes and Ortega–Braun.
  - **Fix (applied):** Arm P is a gate only. Z0 counts only under selection (Arm S) or agentless exchange (Arm L). Arm L also counts as a relabel unless its conserved quantity is produced by the tracking dynamics.
- **H2, high: the low-entropy source is physics in disguise.** P-src (blank inflow R) is the arrow of time / a low-entropy environment.
  - Under P-rev and P-leak, no record persists without it. That follows from counting and is the content of Landauer/Bennett.
  - **So tracking-first can remove kT, the bath and energy, but not the need for a low-entropy supply.** This answers part of the owner's question directly: the "second-principle" part of thermodynamics stays as a premise, and only its energy and temperature dress can go.
  - **Fix:** this is stated in §0 and §1.3 and must be carried into any summary.
- **H3, medium: relabelling the master curve.** M-x is a restatement (marginal analysis). It must not be quoted as a derivation of kT or as new.
- **H4, medium: the persistence currency is chosen.** Kelly fair-odds betting makes log-growth native nats. It is a modelling choice (REQUIREMENTS_FIRST row 24 kept it as a candidate objective).
  - A different persistence measure, such as the survival probability in T3, gives a different θ scale.
  - **Fix:** T1 reports results as conditional on the Kelly currency. T3 is the cross-check.
- **H5, medium: P-rev is a physical premise** (Liouville/unitarity in physics). The brief allows it as a primitive. It is the source of the counting Landauer form, which must be disclosed wherever O5 is quoted.
- **H6, medium: the prior-art search is not exhaustive.** Not searched: resource competition (R*), error-correction upkeep floors (G4), and economic general equilibrium for the shared-price form. Any of these could cover G1 or G4. **Fix:** search before T1's pre-statement.
- **H7, low: M-tel is self-checked only.** It may already be in T59/T60. Not cited as new.
- **H8, low: route scores are judgments,** on the stepback scale, not measurements.
- **H9, low: wording.** The word for a rule of nature is avoided; "Z0" and "C1" name the thermodynamic properties instead. No claim to derive physics, QM, GR, holography or gravity is made. Jacobson is listed only to say it is not used. Banned words were checked by search.
- **H10, low: line citations.** CORE and THEORY line numbers were read at `8b553c6`, and the WORLD_TRACK and REQUIREMENTS_FIRST sections at their current local state.
- **Outcome: PASS-WITH-FIXES.** Fixes: H1 (Arm P as gate; Z0 counts only in Arms S and L), H2 (P-src carried into summaries), H3 (M-x as a restatement), H6 (the literature search before T1's pre-statement).

## 6. Labels (summary)

| claim | label |
|---|---|
| TF (a heat-form cost with temperature-like θ arises from tracking alone) | **HYP**, untested |
| M-x: x = θ_task(0)/kT and θ_task(İ*) = kT in the OU class | PIM (ELEMENTARY; a restatement; sympy-checked) |
| M-tel: no threshold on the telegraph's continuous infimum | PIM (ELEMENTARY; self-checked; possibly already in T59/T60) |
| "Most selecting results need a per-nat price, not kT" (§3.2) | OBSERVED (a reading of the text); T0 would make it exact |
| A tracking-first route cannot remove the low-entropy source under P-rev and P-leak | ELEMENTARY (counting; KNOWN in substance: Landauer, Bennett) |
| Routes T0–T4, their scores and rankings | judgments, not results |

---

## 7. T0 CURRENCY AUDIT: pre-statement (appended 26 Nov 2026, about 19:12 ET, before the audit was done)

*Brief: the parent's 19:06 message (T0, then T1). A paper audit. Nothing is computed except algebra.*

### 7.1 Question and method

- **Question.** In each audited class, once every floor is written as (a coefficient) × (nats or nats per unit time) × kT, does kT enter the **minimizer** (the design) and every **threshold** only through dimensionless ratios of kT to the other prices (w, c, h, the probe price, B, 1/β_sel)? Or does it do other work?
- **Method.** Replace kT by a generic price κ per nat. For each item, write the design as a function of the inputs and check that the dependence on κ is through ratios only. Separately, list every place where a **physical coefficient** (not kT itself) or a **physical tie between two medium numbers** is used.
- **Audit list, fixed now:**
  - A1, the OU minimum (CORE.md:90–91);
  - A2, the geometric ladder count (:92);
  - A3, the sum of modes (:93);
  - A4, the telegraph (:94, :74);
  - A5, the drifting spring and the Kalman factor 2 (:76);
  - A6, frozen worlds (:78);
  - A7, the first bit / threshold (:96);
  - A8, the holographic field (:102);
  - A9, acting with a probe price (:116, :118);
  - A10, concavity in volatility (:108);
  - A11, the ruin cap with reserve B (CORE.md:27; THEORY CT22, CT25);
  - A12, the selection route π ∝ e^{−βJ} (:122);
  - A13, the keep floor c_K·Γ·I (C12B) and T63's 4kTΓ(ln 2 − h(ε));
  - A14, SH-heat / SH-read (x = w/kT; y);
  - A15, WORLD_TRACK Steps 1–2;
  - A16, THEORY's five-term sum (κ, h, A, L);
  - A17, CT9, CT11, CT18, CT25;
  - A18, T57's conservative-trap loophole ("vanishing ongoing heat at a Boltzmann residual", CORE.md:80).

### 7.2 Score (fixed now)

- **HIT:** in every item, kT enters the design and the thresholds only through price ratios. Every other use of physics falls in a floor's class premise (local detailed balance, the Einstein relation, class RF).
- **MISS:** at least one item where kT does structural work outside the floor premises.
- **OPEN:** an item whose design cannot be written without the heat expression.
- **Expected:** HIT, p 0.85. The one place I expect kT to do more than price is A18, where T may set a **noise level** (a Boltzmann residual), not a price. If so, it is reported as a second role of kT, inside the floor premises (the Einstein relation ties the medium's noise to its price).
- **Triviality:** a HIT is ELEMENTARY: currency covariance, THEORY B12 S1 (THEORY.md:420). Its value is the map.

## 8. T0 results (done after §7's hash was logged at 19:10 ET; algebra in `trackfirst/t0_audit.py` → `.out`)

*Timing note: §7's header says "about 19:12". The hash was actually logged at 19:10, before any audit step.*

### 8.1 Item by item

| item | how κ (in place of kT) enters the design or threshold | physics used beyond the price |
|---|---|---|
| A1 OU (CORE.md:90–91) | İ* = √(avw/κ) − a, invariant under (κ, w) → λ(κ, w) (sympy) | the class premise of the floor (Einstein relation, local detailed balance) |
| A2 ladder (:92) | the count depends on wv/(κa) only | same |
| A3 sum of modes (:93) | the first-order condition in μ depends on κ only through w/κ (sympy) | same |
| A4 telegraph (:74, :94) | ε* depends on w/(κr) only | same |
| A5 drifting spring (:76) | ε* = σ√(cκ/(2w)): a ratio. **c = 1 (fast spring) or 2 (Kalman) is a physical implementation coefficient** | the factor 2 comes from the Einstein-relation accounting (Sandberg et al.; Hartich et al., as credited in CORE) |
| A6 frozen worlds (:78) | a corner at zero ongoing cost; no κ dependence | — |
| A7 first bit (:96) | price per bit against loss saved: a ratio | — |
| A8 holographic field (:102) | 13.61 per cut site, in units of κ | the class premise |
| A9 acting (:116–118) | two ratios, w/κ and (probe price)/κ | — |
| A10 concavity in volatility (:108) | ∂²J*/∂v² < 0 for every κ > 0 (sympy) | — |
| A11 ruin cap | homogeneous of degree 1 if B is in the same currency (B12 S1) | — |
| A12 selection (:122) | βJ = (βκ)·(İ + (w/κ)·ε) exactly (sympy). The selection temperature enters only as βκ | — |
| A13 keep floor c_K·Γ·I; T63's 4κΓ(ln 2 − h(ε)) | κ is a unit. **c_K = 2 (or 4) and the factor 4 are physical coefficients**, and they set the **relative** price of holding a nat against writing one | class RF / C12B premises |
| A14 SH-heat / SH-read | through x = w/κ and y only | as A13 |
| A15 WORLD_TRACK Steps 1–2 | every cost is nats × κ; the designs depend on x only | as A13 (keep), plus the sensor's tick (W2) |
| A16 five-term sum | no kT at all | — |
| A17 CT9, CT11, CT18, CT25 | no kT at all | — |
| A18 T57's conservative trap (:80) | **kT is not a price here.** A passive record at equilibrium in a trap holds information through its Boltzmann residual ∝ e^{−U/kT}, so T sets the record's **noise** (its precision is stiffness/kT) | the equilibrium Boltzmann form itself |

### 8.2 Score: **HIT** (as predicted, p 0.85)

- **In every item,** kT enters designs and thresholds only through price ratios. This is PIM (ELEMENTARY), sympy-checked for A1, A3, A5, A10 and A12. The rest is by inspection of linear-in-κ costs.
- **Physics beyond the price** appears in two forms, both inside floor premises:
  1. **Relative coefficients between nat-prices:** the Kalman factor 2 (A5), c_K (A13) and T63's 4. These set the ratio of the price of **holding** a nat to the price of **learning** one, and the ratio between implementations.
  2. **A noise role (A18):** T sets a passive record's equilibrium noise. Through the Einstein relation, the same T sets both the medium's **noise** and its **price per nat**. **That tie (fluctuation–dissipation) is the one structural thing thermodynamics adds to the core.**
- **What tracking-first must therefore supply:**
  - (i) a price per nat, which is T1;
  - (ii) a relative price of holding against learning, which is what the parent's 19:09 steer asks T1 to price: stored nats;
  - (iii) optionally, a tie between the medium's noise and its price. Nothing in T1 provides (iii). It is listed as **open**.
- **Triviality:** ELEMENTARY (currency covariance, THEORY B12 S1). The new content is only the map, and the identification of the noise–price tie as the single structural input.
- **Labels:** the per-item rows are PIM (ELEMENTARY) or inspection. "The fluctuation–dissipation tie is the only structural input" is OBSERVED, as a reading of 18 items. It is not proved for classes not audited.

## 9. T1 prerequisites (appended about 19:20 ET, before T1's pre-statement)

### 9.1 Literature search (every DOI checked on Crossref this session: `trackfirst/crossref_t1.txt`, 21/21 OK; one arXiv-only item checked on arXiv: `trackfirst/arxiv_abin.txt`)

**Competitive exclusion, R\*, resource competition.**

| source | what it establishes | consequence for T1 |
|---|---|---|
| Hardin 1960, *Science* 131:1292, 10.1126/science.131.3409.1292; Levin 1970, *Am. Nat.* 104:413, 10.1086/282676 | Competitive exclusion: at most as many species persist at equilibrium as there are limiting factors | **One blank pool and no niches ⇒ at most one tracker lineage persists. Pre-stated (Arm S1)** |
| Armstrong & McGehee 1980, *Am. Nat.* 115:151, 10.1086/283553 | Exclusion holds at equilibrium. Non-equilibrium (oscillating) coexistence on fewer resources is possible | T1 checks for stationarity. Oscillations would be an OPEN case |
| Tilman 1980, *Am. Nat.* 116:362, 10.1086/283633 | R\*: on one resource, the species that persists at the lowest resource level wins | **Predicts which lineage wins in S1: the lowest B\***, where B\*_k solves max_n g_k(n; B) = 0 (§10.4). PIM in-model by the same argument** |
| MacArthur 1969, *PNAS* 64:1369, 10.1073/pnas.64.4.1369; MacArthur 1970, *Theor. Pop. Biol.* 1:1, 10.1016/0040-5809(70)90039-0; Marsland, Cui & Mehta 2020, *Am. Nat.* 196:291, 10.1086/710093 | The equilibria of consumer–resource models **minimize a function** (MacArthur's minimization principle; the minimum environmental perturbation principle). The competitive outcome is a constrained optimum | **A severe relabel risk for Arm S's "selection, not a planner".** The ecological equilibrium may itself be a hidden planner's optimum. This must be disclosed in any Z0 claim |
| Chesson 2000, *Annu. Rev. Ecol. Syst.* 31:343, 10.1146/annurev.ecolsys.31.1.343 | Coexistence needs stabilizing niche differences (for example self-limitation) that are larger than fitness differences | **The coexistence arm (S2) uses per-lineage self-limitation s_k as the niche.** This is the standard minimal stabilizing mechanism, and it is a chosen input |
| Posfai, Taillefumier & Wingreen 2017, *PRL* 118:028103, 10.1103/PhysRevLett.118.028103; Tikhonov & Monasson 2017, *PRL* 118:048103, 10.1103/PhysRevLett.118.048103 | Statistical-physics treatments of resource competition. Coexistence beyond exclusion under budget trade-offs; collective phases | Prior art for "temperature-like" collective behaviour in resource competition |
| Charnov 1976, *Theor. Pop. Biol.* 9:129, 10.1016/0040-5809(76)90040-X | Marginal value theorem: a forager equalizes its marginal gain with the habitat's average | **"Marginal gain equals a shared environmental rate" is KNOWN** |
| Geritz, Kisdi, Meszéna & Metz 1998, *Evol. Ecol.* 12:35, 10.1023/A:1006554906681 | Adaptive dynamics: singular strategies, convergence stability, branching | Used for the ESS reading, and for branching when the payoff in n is not concave |

**Error correction and upkeep floors (G4).**

| source | what it establishes | consequence |
|---|---|---|
| von Neumann 1956, *Automata Studies* 43–98, 10.1515/9781400882618-003; Gács 1983, *STOC* 32–41, 10.1145/800061.808730; Evans & Schulman 1999, *IEEE TIT* 45:2367, 10.1109/18.796377 | Reliable storage and computation from noisy parts need redundancy and active repair. Without fresh input, information in noisy circuits decays with depth (Evans–Schulman) | Redundant cells against a leak: T1's design variable n (cells held) is this classical object |
| Bennett & Grinstein 1985, *PRL* 55:657, 10.1103/PhysRevLett.55.657 | Stabilizing non-ergodic (memory-holding) behaviour in locally interacting systems against noise needs **irreversibility**, meaning dissipation | Holding a record against a leak needs an entropy sink. **This covers H2's "the low-entropy source cannot be dropped" in kind** |
| Aharonov, Ben-Or, Impagliazzo & Nisan 1996, *Limitations of noisy reversible computation*, arXiv:quant-ph/9611028 (**no Crossref DOI found**; checked on arXiv) | Noisy **reversible** computation without a supply of fresh bits loses all information in logarithmic time | **The P-src premise is a theorem in kind**: under reversibility plus noise, fresh blanks are necessary. KNOWN |
| Hopfield 1974, *PNAS* 71:4135, 10.1073/pnas.71.10.4135; Sartori & Pigolotti 2015, *PRX* 5:041039, 10.1103/PhysRevX.5.041039; Lang, Fisher, Mora & Mehta 2014, *PRL* 113:148103, 10.1103/PhysRevLett.113.148103 | Error reduction costs dissipation (proofreading; the speed–error–dissipation trade-off); the cost of cellular inference | Physical (kT) versions of an upkeep floor |
| Dennis, Kitaev, Landahl & Preskill 2002, *J. Math. Phys.* 43:4452, 10.1063/1.1499754 | Topological memory with active error correction; entropy is removed through syndrome measurement and fresh ancillas | The quantum analogue. Not used |
| Wolpert 2020, *New J. Phys.* 22:113013, 10.1088/1367-2630/abc5c6 | The minimal entropy production of interacting systems | Context |

**G4 status after the search:**
- **Partly covered.** That holding information against noise needs a steady inflow of fresh bits is KNOWN (Aharonov et al. 1996; Bennett & Grinstein 1985; von Neumann 1956).
- **Not found:** a counting floor of the specific form Γ·(ln 2 − h(ε)) blank-nats per unit time. It may exist in the coding literature on storage with refresh. G4 stays OPEN, with a lower novelty prior.

### 9.2 The selection arm's uptake rule (**locked now**)

- **What is priced (the parent's 19:09 steer, after INFO-BUDGET).** The **stored record**, meaning cells held, not look events.
  - Each held cell is reset to a random bit at the medium's leak rate Γ. A reset cell is returned to the pool as used and replaced by a blank.
  - So an individual holding n cells needs **Γ·n blanks per unit time**. This is the counting form of the keep floor: c_K·Γ·I with I ≤ n·ln 2, priced per cell held.
  - Looks (rewrites at rate f) are **not** priced. The look rate f is a **disclosed sensor input**, as INFO-BUDGET found it to be.
- **Uptake (mass action).**
  - Blanks are found at rate α·B per unit search effort, where B is the free-blank stock. α = 1 sets the unit of B.
  - The effort needed is Γ·n/B per unit time. Effort costs c_k growth-nats per unit effort.
  - **Uptake cost = c_k·Γ·n/B** growth-nats per unit time.
- **Heritable trait:** n, the number of cells held, an integer in [0, 40]. Selection acts only through growth. There is no planner and no price signal; the only shared variable is B.
- **Chosen inputs in the rule:** the mass-action form, α = 1, the effort cost c_k, and the rent "Γ per held cell". These are listed again in §10.6.

## 10. T1 BLANK-PRICE: pre-statement (written before any T1 number is computed)

### 10.1 Question

- In a medium with no energy, where a record's only cost is the blanks needed to hold it, and persistence (Kelly log-growth) is the only currency:
  - Do tracker lineages that share one blank pool settle on a common **price of a held cell / nat** (Z0), under selection dynamics?
  - Is the exclusion outcome where they cannot coexist the one predicted in advance?
  - What **information budget** does each lineage select?
- **Folded in from WORLD_TRACK (Steps 1–2).** The selected object is the stored information I* (with n* cells as its realisation). The look rate is a sensor input.

### 10.2 Model (locked)

- **Worlds.** Three lineages k = 1, 2, 3 track telegraph worlds X^k ∈ {0, 1} with symmetric flip rates **r = (0.05, 0.2, 0.8)**. Worlds are independent.
- **Record.** An individual holds n cells.
  - Looks arrive as a Poisson process at rate f (the sensor input). At a look, every cell is overwritten with the current X (perfect sensor).
  - Each cell is independently reset to a uniform random bit at rate Γ (the leak).
- **Bets (the persistence currency).** Bets arrive at Poisson rate ν = 1. At a bet the individual bets Kelly-style at fair odds 2, using the posterior P(X | K), where K = the number of cells reading 1.
  - The log-growth gain per bet is **I_n := I(K; X)** at the stationary age u ~ Exp(f) since the last look (Kelly 1956).
  - With P(W ≠ X | u) = (1 − e^{−2ru})/2 for the value W written at the last look, and the per-cell P(cell = W | u) = (1 + e^{−Γu})/2:
    - P(K = k | X = x) = ∫ f·e^{−fu} Σ_W P(W | x, u)·Binom(k; n, P(cell = 1 | W, u)) du;
    - X is uniform, and I_0 = 0.
  - Computed by Gauss–Laguerre quadrature (200 nodes), checked against adaptive quadrature at n = 1, 7, 40 to 1e−8.
- **Fitness (growth-nats per unit time):** g_k(n; B) = ν·I_n(r_k, f, Γ) − m − c_k·Γ·n/B − s_k·N_k, with **m = 0.02**.
- **Dynamics:**
  - dN_{k,n}/dt = N_{k,n}·g_k(n; B) + μ·(N_{k,n−1} + N_{k,n+1} − 2N_{k,n}), with reflecting ends at n = 0 and n = 40 and **μ = 1e−4**.
  - dB/dt = R − Γ·B − Γ·Σ_{k,n} n·N_{k,n}. Free blanks also leak at Γ.
  - Initial state: N_{k,n} = 0.1/11 for n = 0 … 10, and B = R/Γ.
  - Integrate (LSODA, rtol 1e−8) to t = 2·10⁴. Stationarity check: max |d ln N/dt| < 1e−5 over classes with N > 1e−6. Otherwise the cell is OPEN (oscillation or slow transient).
  - A lineage **persists** if Σ_n N_{k,n} > 1e−6. Its **dominant** n is the mode. **Bimodal** means a second local maximum holding > 10% of N_k (branching).
- **Direct ESS solve (a check, not a planner):**
  - n\*_k(B) = argmax_n [ν·I_n − c_k·Γ·n/B];
  - N_k(B) = max(0, (ν·I_{n\*} − m − c_k·Γ·n\*/B)/s_k);
  - B\* solves R = Γ·B + Γ·Σ_k n\*_k·N_k (bisection).
  - At s = 0, the S1 rule (§10.4) is used instead.

### 10.3 Arms and grids (fixed now)

- **Gate P (planner, a reproduction gate, not evidence).** One organism holds all three trackers and maximizes Σ_k ν·I_k(n_k) subject to Σ n_k ≤ M, for M = 1 … 60, by exact DP. Check that a common price bracket exists: the intersection over k of [ν·ΔI_k(n_k + 1), ν·ΔI_k(n_k)] is non-empty whenever every n_k ≥ 1. Expected to pass in every M where each I_k is concave at its n_k.
- **Arm S1 (one pool, no niches, s = 0, c = 1).** Γ ∈ {0.05, 0.2}, R ∈ {0.5, 1, 2, 5}, f ∈ {1, 4}: 16 cells.
- **Arm S2 (one pool, niches, c = 1).** s_k = s ∈ {0.01, 0.1}, with Γ, R, f as in S1: 32 cells.
- **Arm S3 (as S2, with heterogeneous uptake costs c = (0.5, 1, 2)).** 32 cells.
- **Arm L (two pools linked by blank exchange D·(B₂ − B₁)).**
  - One lineage per pool, both with r = 0.2 and s = 0.1, f = 1, R₁ = 2, R₂ = 0.5;
  - Γ ∈ {0.05, 0.2}, D ∈ {0, 0.01, 0.1, 1, 10}: 10 cells.
- **Intensive check.** Every S2 cell is rerun with R → 2R and s → s/2.

### 10.4 Paper predictions (stated before computing)

- **S1 (PIM, by the R\* argument).** Growth depends on the shared state only through B, so generically exactly one lineage persists at stationarity. It is the one with the **smallest B\*_k**, where B\*_k = the least B with max_n [ν·I_n − m − Γ·n/B] ≥ 0.
  - HYP: the winner is the slowest world (r = 0.05), whose cells keep their information longest.
  - **This exclusion is a pre-stated outcome, not a surprise.**
- **S2/S3 (PIM at any interior stationary state).** If a lineage persists with dominant n\*, local stability of the mode under mutation requires g_k(n\*) ≥ g_k(n\* ± 1). That gives the bracket **ν·ΔI_k(n\* + 1) ≤ c_k·Γ/B ≤ ν·ΔI_k(n\*)**.
  - So every persisting lineage's marginal growth per held cell, divided by its own c_k, brackets the **same** medium variable Γ/B.
  - **Z0 therefore holds by the algebra of the uptake rule once B is shared.** The run tests only whether the dynamics reach such a state (the ESS), whether coexistence happens, and whether a non-concave I_n causes branching or bracket failures.
- **Information budget (HYP).** n\* and I\* are nonincreasing in r_k (fast worlds gain little from redundancy), and the price Γ/B\* falls as R rises.
- **Intensive (PIM, by scaling).** R → 2R with s → s/2 gives N → 2N with B\*, n\* and the price unchanged.
- **Arm L (ELEMENTARY).** |ln(B₁/B₂)| decreases as D increases, and blank flux runs from the high-B (cheap) pool to the low-B (dear) pool by construction.

### 10.5 Score (fixed now)

**Gate:**
- Gate P passes (bracket non-empty in every M with concave I_k at n_k).
- The quadrature check passes.
- The dynamics reach the direct-ESS n\* in ≥ 95% of persisting lineages over S2 and S3.
- If the gate fails, the run stops and is reported.

**S1 (a pre-stated outcome):**
- **As predicted:** one survivor in ≥ 15 of 16 cells, and it is the smallest-B\* lineage in all of them.
- **Prediction missed:** otherwise. That would be an open miss of the R\* prediction, informative about the model.

**Z0 (scored on S2 and S3):**
- **HIT:** coexistence of ≥ 2 lineages in ≥ 50% of the cells; the bracket holds for every persisting lineage in ≥ 95% of coexisting cells (one shared Γ/B, after dividing by c_k); the intensive check moves the price by < 1% in all cells; and Arm L's |ln(B₁/B₂)| is monotone in D and < 0.05 at D = 10.
- **MISS:** the bracket fails in > 5% of coexisting cells, or the dynamics settle away from the ESS.
- **OPEN:** coexistence in < 50% of the cells (Z0 not posable), or non-stationary cells exceed 10%.

**Branching** (bimodal lineages) is reported separately. Per mode, the bracket is checked against that mode.

### 10.6 Triviality, relabel test and chosen inputs (stated now)

**The relabel call, pre-stated.**
- If Z0 holds through the §10.4 algebra (a shared B and a mass-action uptake cost), T1 is a **RELABEL**. The "temperature" is the pool's scarcity Γ/B, and its equality across lineages is:
  - Charnov's marginal value / Tilman's R\* (ecology);
  - KKT / Jaynes (one shared constraint);
  - Kelly (nats are the currency).
- MacArthur's and Marsland–Cui–Mehta's minimization principles further imply that the S2 equilibrium may be a hidden planner's optimum. Ortega–Braun's 1/β is then the pool's Γ/B, with the only addition being that it is set endogenously by R, Γ and the community.
- **Genuine content would need** one of:
  - (a) a systematic, world-set failure of the bracket (for example non-concave I_n producing branching with a pattern in r_k, Γ or f);
  - (b) dynamics selecting something other than the ESS;
  - (c) an information budget I\* with a form not given by a fixed price per held cell.
- **Prior that the call is genuine:** 0.15.

**Chosen inputs (all disclosed):**
- ν = 1, with Kelly fair odds 2 (the persistence currency; H4 of §5);
- m = 0.02;
- c_k (uptake effort cost);
- the mass-action uptake form and α = 1;
- the rent of Γ per held cell (a blank replaces each leaked cell);
- free blanks leaking at Γ;
- s_k (the niche; Chesson's stabilizing mechanism);
- f (the look rate: a sensor input);
- perfect writes at a look;
- μ, n_max = 40, and the initial state.

**World inputs:** r_k. **Medium inputs:** Γ and R.

**Not tested:**
- a tie between the medium's noise and its price (T0's open item (iii));
- any energy;
- any claim about physics.

**Labels planned:**
- quadrature and dynamics outputs: OBSERVED;
- S1's R\* rule and the S2 bracket: PIM;
- the relabel call: a judgment against the stated test.
