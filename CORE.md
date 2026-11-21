# The core: the cost of judgment on one page

*Restructured Saturday 21 November 2026, about 2:00 PM ET (America/New_York), first written beside `main` `2c32ade`, after Chad's point (t2061) that Shannon proved limits without experiments; revised the same afternoon after the independent review of PR #139 (`reviews/shannon_2026-11-21/REVIEW.md`, verdict NOT READY) and the confirm review (`reviews/shannon_2026-11-21/CONFIRM.md`); current to `main` `a97887e` (PR #139 merged as `0726423`; also #138 DIR1 as `1cb1ac2` and #141 layer lifetime as `a97887e`). The previous text is frozen at `history/2026-11-21_CORE_before_shannon.md`. Omissions from this page are compressions, not withdrawals; the operational kill rule and the Model S counterexample stay in force in the files cited below. The new results (S1–S3) are in `theory/SHANNON_2026-11-21.md`. Status words: **proved** means proved inside the stated model, which says nothing by itself about nature; **open** means untested, not refuted. IDs: `measurement/CLAIM_MAP_v2.md`.*

The theory has two parts, and they are different kinds of claim. **Part 1 is mathematics:** limits that any system acting ahead of a world it does not control must obey, and the structure of the cheapest design. These hold by proof, like Shannon's limits, and need no experiment. **Part 2 is a hypothesis about nature:** that strongly selected systems come close to those limits. Only Part 2 has odds.

## 1. Definition

A system that must act ahead of a world it does not control chooses its design 𝒟 (layers, what each tracks, how often it reads, what it shares) to minimize

$$J(\mathcal D)=\kappa I_{\text{mem}}+hK+w\,\mathbb E[\ell_{\mathcal D}]+A(\mathcal D)+L(\mathcal D)\quad\text{subject to}\quad P(\text{ruin})\le\varepsilon .$$

- κI_mem + hK: memory held at price κ per nat, plus upkeep h per layer (a tracking store, not an org-chart level).
- w·E[ℓ]: stake times expected loss at the moment of use; lateness counts as error.
- A, L: the cost of reading the world, and of linking, telling and lookup.
- P(ruin) ≤ ε: a reserve paying J must not hit zero more often than ε. A hard cap, not a cost to average away.

The world is a measured input: its statistics (spectrum or Markov kernel), the read noise and the lead time. One currency per system. The equation is a definition, assembled from known parts (THEORY §3).

## 2. Part 1: the limits (proved in-model)

**The floor (S1).** In a stationary world the system does not affect (drifting, random-walk worlds are open, CX1), every design pays at least J_floor, computed from the world's statistics and the prices alone: memory pays for the predictive information it holds (CT1, CT4), and reads pay for at least the sequential rate–distortion rate of the accuracy reached. A layer price h is not part of that floor: a memoryless read has K = 0 and still carries information. Landauer floors the erasure part of κ. Sagawa & Ueda 2009 floor the sum of measurement and erasure work, not a separate read price stacked on that floor. In a scalar Gauss–Markov world the information floor is reached exactly when memory or reads are free. On one scalar Gauss–Markov world (a = 0.9, Q = 1, lead 2), the best one-layer Kalman design on a 36-point price grid has efficiency J_floor/J = 0.9574 (gap 1 − J_floor/J = 4.26%; the design costs 4.45% more than the floor) at the worst point (κ = c = w = 1, layer price left out of both sides; numerical). That is not a bound over worlds.

**The frontier and efficiency (S2, S3).** The world defines a frontier: every combination of memory, reads, layers and accuracy that some design can reach. It contains no prices. The inner-product dual J*(p) = inf ⟨p, z⟩ equals −σ(−p), where σ is the support function of the frontier. It equals the operational least cost only when some minimizer has read cost A = c·r and linking cost L = 0. The frontier is the theory's analogue of Shannon's capacity: a curve, as for rate–distortion, not a single number. Knowing J* on the positive orthant recovers the free-disposal hull of the Pareto face, not the whole convex hull. A system's **technical efficiency** is how far its resources could shrink and still give its accuracy; it needs no prices. For the input cost C = κI + c·r, cost efficiency C_min/C splits into technical × allocative (Farrell 1957); that product is not true of J_floor/J. Minimizing the linear cost at strictly positive prices implies radial technical efficiency 1 on the feasible set. Under a binding ruin cap that set is the ruin-feasible set, and the cap need not preserve convexity.

**The structure of the cheapest design.**

| ID | Result |
|---|---|
| CT20, CT33 | A best design exists. With ruin slack, more at stake never means less spent on judgment and never more error. Reads can replace layers. |
| CT21 (L1–L3) | Layers ≤ the world's predictive degree. At most one layer for one real scale (K\* ∈ {0, 1}). Layers beat one tracker iff R > R\*. |
| N60 | In Model S, if ε_K is convex, K\* = 1 + #{k ≥ 2 : R(ε_{k−1} − ε_k) > 1}: layers equal the world's time scales whose stakes pay for them, counted by degree. Convexity is numerical (120/120 Model S worlds), not proved. With rhythms the formula is false and no predictive rule exists (`core/KEYSTONE_NOTE.md`; IMP-N60 failed its gates; the holographic count failed in-model). Worked rhythms counterexample: two oscillators at R = 3, argmin 3, formula 2; paying for a rhythm as a pair does not restore K\* (`core/KEYSTONE_NOTE.md`). The formula cannot return the K\* = 0 that CT21 allows. The 120/120 convexity count excludes 24 wide-search worlds still on the pre-#116 solver. IMP-N60 failed its gates (PRIMARY 58/189 cost, 51/189 composition) and is not rescued. Cymatics: discrete jumps pass; frequency locking passes on the aggregate statistic, but 3 of 7 worlds fail it individually (`core/KEYSTONE_NOTE.md`). |
| CT22, CT25 | Nothing survives below B_min; above B_slack the expected-cost rules are exact. Buffer grows as shock × τ^H. |
| CT14, CT16, CT35, CT36 | A shared layer pays once N > N\*(ρ). At equal read quality, with shared upkeep measured in local layers, a shared layer's worth falls as e^{−2ℓ/τ}, so fast scales go local and slow ones shared (CT28, CT34). Joint value can be superadditive. A member belongs to every shared layer whose test it passes, one per shared driver, and layers form and dissolve as the best grouping moves past the redesign band (`theory/FLUID_LAYERS_2026-11-21.md`). |
| Freeze limit (#137) | Frozen is the slow-world limit of held: optimal tracking falls smoothly to zero and the design reads once, then persists blind. Over time this is the known freeze-out rule, with the cost-optimal read rate in place of an interaction rate. |
| CT37–CT43 | Robustness from cost plus the ruin cap; redesign cost gives an inaction band; J is already the time average (`THEORY.md` B.10–B.11; `theory/DYNAMICS.md`). |
| CT23, J16 | A wrong picture of the world costs second-order regret. A needed cost missing from the closed list is a miss. |

**The selection bridge.** Under weak mutation and fitness linear in J, selection is a thermal search: designs are distributed as π ∝ exp(−βJ), with β set by population size times the fitness scale (Sella & Hirsh 2005, applied to J; `core/bridge_2026-11-21/SELECTION.md`). Near a quadratic minimum the expected excess is d/(2β), so the expected fractional distance from the floor's minimizer falls as d/(2σN_e). Strong selection is low temperature. In T27, P1 and P2 passed in-model; P3 failed and is not rescued.

## 3. Part 2: the hypothesis

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

By S3 it has two halves. The **technical** half, which needs no prices: such systems sit near their world's frontier. The **allocative** half, which needs price ratios or only signs: they sit at the frontier point their prices select, so their designs move in the directions Part 1 proves when stakes, drift or prices change.

"Strongly selected" is operational (THEORY §3): a cost-to-fitness map σ, a population N_e, a band ε = 10/(σN_e) that excludes a named rival, and at least 10 redesign times in one world. Earned when qualifying systems in two classes at different scales fall inside their preregistered bands and beat a named rival. Killed by misses beyond the class's preregistered binomial allowance (for a small class, one). A needed cost missing from the closed list is a miss (J16). So is a design that does not move when its inputs change: a non-move is consistent only if the post-change gap g < Δ_R(k_lo); a miss if g > max(the static band, Δ_R(k_hi)); INDETERMINATE between; and if the predicted gap of a non-mover is at most Δ_R(k_hi), the move test is NOT A TEST (CT41). The revealed-prices amendment to the "independently measured prices" requirement is proposed, not applied (`theory/REVEALED_PRICES_2026-11-21.md`).

## 4. Evidence so far

- **Mechanism, in silico (EVO1, #114).** Blind selection found the cost minimum where small steps lead to it: PC, W1 and W2 passed; S031 and S07 were inconclusive (2/8 misses each, just over the band); W4 and W4b failed, W4 on a creation valley that met the diagnostic's bar (D2b, 4/4), W4b's valley diagnostic missing its bar (D1b, 2/4). In-model only.
- **Outside evidence for the technical half (context, not tests).** Retinal ganglion cells carry predictive information close to the limit set by their input (Palmer et al. 2015); E. coli climbs gradients within a factor of two of the bound set by the information it acquires (Mattingly et al. 2021). These test the efficient-coding programme (Barlow; Bialek), are consistent with the hypothesis, and were not preregistered or qualified here.
- **Field tests of the hypothesis.** None valid yet. The 30 earlier field rows are NOT A TEST (10 passed and 20 failed on proxy). The directional field test (allocative half, signs only) is in progress; its predictions are locked before any data are scored. Every theorem has been refereed at most once, by one bot family, and no human expert has read the theory. No system has yet been shown to qualify. E. coli is the best candidate, and its σ, N_e and T_red are to be sourced before any rescoring.

## 5. What is open

- **A limit for the layer term.** The part of J that is the theory's own, the price per layer, has no formula for its floor: "the fewest layers that reach accuracy D in this world." In Model S it is computable numerically (E_K); with rhythms it is not predicted. Without it, efficiency can be measured for the information part but not for the layer part.
- Achievability when memory and reads are both priced; the floor under a binding ruin cap; convexity in Model S; a predictive rhythm rule; the selection law under strong mutation or nonlinear fitness.

## 6. Credit

The parts are known: Shannon (rate–distortion and its converse), sequential rate–distortion (Tatikonda, Sahai & Mitter; Tanaka et al.), predictive information and its bottleneck (Bialek, Nemenman & Tishby; Still et al.), rational inattention (Sims), Farrell efficiency, Wiener–Kalman, Lundberg, Harris, Landauer, Samuelson, Coase, Topkis, Lynch, Kettelle, Dixit, Cohen, Jiang, Taleb & Douady, Sella & Hirsh (`litmap/`, THEORY §10). Friston's free energy is the nearest single-objective rival; J differs by explicit free prices, a price per layer and a ruin cap. What is claimed as new is the package: one priced objective under a ruin cap, the world's frontier as its only input, the structure of its minimizer, and a kill rule across scales.
