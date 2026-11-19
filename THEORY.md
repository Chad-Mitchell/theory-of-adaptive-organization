# A Theory of Adaptive Organization: judgment under the second law — v2.0 draft (19 November 2026)

Author: Chad Mitchell (X: [@torusflow](https://x.com/torusflow)). Public domain (CC0). Not peer reviewed, and not independently reviewed as a whole. **This file is the one canonical statement of the theory; where anything else in the repository disagrees, this file governs.** The main text (§0–§9) reads in about 20 minutes. Appendix A fixes the notation, Appendix B proves every numbered result, and Appendix C maps each result to its claim row and its derivation. Claim statuses: `measurement/CLAIM_MAP_v2.md` (v2.49). Earlier versions, the changelog and the full record of tests and reviews: `reference/` and the folders it indexes.

**Status words.** *Proved in-model*: a theorem inside the model of §2.1, which says nothing by itself about nature. *Known*: a published result, credited. *Open*: untested, not refuted. *Passed/failed on proxy*: a locked prediction scored on an instrument that fails at least one validity gate, which is a result about that instrument, not about the theory.

## 0. The claim

Judgment means carrying a model of the world in order to act ahead of it. This theory's claim is that judgment costs **one bill in three parts: holding memory, being wrong or late, and the reads and effort that keep the memory fresh**, plus the risk of ruin, and that this bill is priced the same way at every scale. Only the currency changes: heat in a cell, attention in a person, money in a firm. Designs that last under strong selection sit near the balance point of the three parts. That one budget yields buildable rules (when to keep, check or let go of a fact; how often to look; when to share a model; who must be in charge; how far one tracker can reach) and, at every scale, tests that can kill it.

Most of the pieces are known, and §8 credits them. What is new is the synthesis: one budget, one set of relations, and predictions across scales with inputs measured on each system. It is a theory, not a law, and not a theory of everything. It says what tracking a changing world costs, not what an organization wants. Its bet about real systems is untested, not refuted (§7).

## 1. The second law, and three ways to last

Total disorder rises; local order can grow only by exporting disorder somewhere else. That law, with gravity, the speed of light, quantum physics and the universe's low-entropy start, sets the stage. The theory adds no physics to it. Things that last do so in one of three broad ways:

| Way to last | What it pays | Does a model of the world pay? | Examples |
|---|---|---|---|
| **Keep** (frozen) | Almost nothing: it sits in a state little can knock loose | No. Nothing it does changes whether it lasts, so a model would cost and buy nothing (Result E1, Appendix B) | Atoms, crystals, a virus particle; at the extreme, a black hole |
| **Hold** (self-regulating) | A steady flow of energy | No. It **regulates itself** (in a star: self-regulating fusion, convection, magnetic dynamos, a layered composition that records its past) **but anticipates nothing outside** | Stars, flames, hurricanes |
| **Know** (tracks) | A flow of energy *and* the cost of staying matched to a world that changes and can ruin it | Yes, once acting late is costly | Cells, immune systems, colonies, people, firms, cities |

The split itself is prior art in substance (Prigogine 1978; Pross 2011). A knower cannot wait for the world to arrive. Once acting late is costly, it can pay to carry a model and act ahead. **That is judgment: not a new physical principle, but a way of staying alive under the old one.** The rest of this document prices it.

## 2. The bill

### 2.1 The model

Every result below is a theorem about this model, and each states which parts it uses.

- **World.** A state X_t that the agent does not change (exogenous). Two classes appear, and each result names its class. **(W-a)** stationary, ergodic Markov: the world fluctuates around a fixed law. **(W-b)** drifting: Gaussian with stationary increments, E(X_{t+τ} − X_t)² = q·τ^{α−1}, with **spectral slope** α = 1 + 2H between 1 and 3 (a random walk is α = 2) and **drift level** q.
- **Agent.** A memory M_t updated from observations, and actions A_t = π(M_t) committed a lead time k before they meet the world.
- **Persistence.** A reserve starts at a buffer B, earns income y and pays every cost; ruin is the first time it reaches zero.
- **Selection.** Selection keeps designs within a tolerance ε of the cheapest. That is an assumption about strongly selected systems, not a theorem (§4).
- **Φ**, the **lifetime value of a fresh reading**: how much one exact reading lowers expected loss, summed over the time until the world has drifted away from it.
- **Regime first.** Every number names its world class, its α and its premises. A result proved for α = 2 is not assumed at other α.

### 2.2 The three parts, and where every cost books

The bill has three parts, plus the risk of ruin:

1. **Holding memory:** the price κ per nat held per unit time, and the upkeep h of a store or of a shared level.
2. **Being wrong or late:** the stake-weighted loss w·ℓ. Lateness is counted as error at the moment of use, because a prediction that arrives after the moment to act buys nothing.
3. **The reads and effort that keep the memory fresh:** the price c of a read (or a price per nat acquired, or c′·r^{−θ} for precision), the price d of telling a member, the link cost κ_b of a broadcast, the price u of looking something up, and the effort g(σ₀ → σ) spent making the world drift less.

**Ruin** is not a fourth part: the failure hazard, weighted by what failure costs (Λ), enters as the persistence constraint the bill already names. **Drift reduction is a lever, not a fourth cost type.** Paying g to make the world drift less (homeostasis, buffers, contracts, niche construction) is effort spent keeping memory fresh, so it books in part 3. The optimum then chooses between watching and steadying by comparing their marginal costs. With this booking the cross-scale claim becomes checkable: **it fails at a level if that level's design needs a cost that cannot be booked as holding, error or lateness, or reads and effort (or ruin)** (CLAIM_MAP J16, open).

### 2.3 What physics prices, and where it binds

The three parts are priced by physics as floors at every scale. Erasing a bit costs at least kT ln 2 of heat (Landauer). For a driven system that meets their conditions, memory that does not predict the signal sets a floor on dissipation (Still, Sivak, Bell & Crooks 2012). Holding information is a continuing flow, not a one-time purchase (Result I5). Tracking has an exact floor with the economic form (Result O1): keeping a random walk of variance rate σ² to mean squared error D dissipates at least kT·σ²/(2D), so the cheapest total is **σ√(2kT·w)**, the same function as the inventory rule σ√(2c·w) with the read price c replaced by kT per nat. That is the precise sense of "only the currency changes": replace kT by what a nat actually costs the system, and the gap between the two is measurable.

Which floor applies to which part matters. Erasure, and the measure-and-erase cycle, never become free. The price of *holding* information about very slow drift can approach zero for quasi-static passive coupling (`theory/SCALE_ENDS.md` E3). The floors bind in cells, where sensing is measurably dissipative (Lan et al. 2012). Above the cell they are literal but slack: a chemical synapse pays about 10⁵–10⁶ times kT ln 2 per bit (Laughlin, de Ruyter van Steveninck & Anderson 1998), and a firm pays far more in salaries and attention. There the exponents come from information theory and competition, not from heat. Whether the second law does more than this above the cell is an **open disagreement**. Chad's position is that the physics is not decorative. In the proofs it supplies why upkeep exists and the floors, and nothing else. A cell in which the physical price per nat and the precision exponent are both measured would settle it.

## 3. When judgment pays

**Result 1 (Theorem P).** In a stationary world (W-a):
- **(P0)** every agent's long-run mean loss is at least D(I_pred), the least loss any action can reach with I_pred nats of predictive information about the world it will meet. If income minus other costs falls below that, ruin is certain.
- **(P1)** a model is necessary exactly when acting blind is not viable: when every blind policy's loss is at least its income minus its own other costs (strict inequality; Appendix B).
- **(P2)** there is a horizon. Nothing in memory can predict the world at lead k better than the world's own present does, so beyond some lead no model makes acting ahead viable.
- **(P3)** a model is carried only if its first bit pays: when κ is less than the loss that bit saves. In the Gaussian case, carry a model iff κ < 2 ln 2·a²·Var, and then its size is I\* = ½ log₂(2 ln 2·a²·Var/κ) bits. A model grows only with the logarithm of what is at stake.

*Why.* An action is a function of memory, so it cannot carry more information about the future than memory does (data processing). Rate–distortion then bounds the loss, and the ergodic theorem turns a negative mean margin into certain ruin. P3 is a convex trade-off whose optimum leaves zero exactly when the first bit is not worth its price.

*What it rules out.* "Every system pays for a model" is false as stated. A bet-hedging population can beat sensing in a world it never tracks (Kussell & Leibler 2005), and the claim then holds only with the population as the agent. **Open item:** P is proved for stationary worlds, but most results below use drifting worlds (W-b). Extending P to them is open (CLAIM_MAP CX1); the scalar Gaussian data-rate bound (Nair & Evans 2004; Tatikonda & Mitter 2004) is a known partial bridge.

## 4. The bet

**Where selection is strong and a choice depends on a drifting world, the designs that last sit near the cheapest way to pay the bill, and the same relations (not the same constants) hold from cells to cities once each system's inputs (α, q, sensing noise, stakes, prices) are measured on that system** (CLAIM_MAP N13 and J6, both open). The causal chain is short. The world's change destroys what the memory holds; re-buying it costs reads, precision or upkeep; error and lateness cost stakes; selection or design keeps the cheapest allocation that stays solvent.

Two limits are fixed before any test. **Strong selection only:** below the drift barrier (Lynch et al. 2016), misses are expected, and a design difference smaller than the selection tolerance cannot be selected for at all (a level is invisible to selection when ρ ≲ ε/b; Appendix B, Lemma B6). The split between strong and weak selection is set in advance and never used to explain a miss afterward. **Measured inputs only:** "optimal for some cost" is empty unless the costs are measured independently of the design they predict, and nothing guarantees that real systems sit at an optimum (Alchian 1950 makes the classic case that selection rewards relative advantage, not maximization). That is why the bet is stated in measured inputs.

## 5. How to build one

Minimizing the bill gives seven rules for an efficient self-maintaining system, whether a team, a firm, a memory for an AI agent or a sensor network. Taken one by one each rule is prior art. They are listed because one budget produces all of them, and each has a stated condition under which it fails.

| # | Rule | Follows from | Fails when |
|---|---|---|---|
| 1 | **Act early.** Return what matters while there is still time to act. Interrupt unasked only when stake × chance it matters, plus what the outcome would teach, beats the cost of interrupting | P2 (the horizon); value of information | Near-tautology; myopic interrupts are a counterexample |
| 2 | **Keep what pays, let the rest fade, recoverably** | Result 2 (G2) | The world is not Markov in the coordinates kept |
| 3 | **Move a belief by the reliability of the signal** | Known (Kalman 1960; Muth 1960) | Heavy-tailed noise (Cauchy) |
| 4 | **Keep prior versions until a correction proves out** | Near-tautology (cheap frozen history) | — |
| 5 | **Act from the current model, not a copy:** a copy's error grows with hops and with drift since the last check | Result G1 | Non-Markov observed variables (seasonality) |
| 6 | **Record whether each prediction was used, ignored or late** | Weak (information has nonnegative value) | The mechanism does not follow from the budget (§5.4) |
| 7 | **Watch more as drift × stakes rises**, and stop past a point when any cheaper fallback exists | Results 2–3, G3, G4 | The buffer sets what survival effort is worth, not the cost-optimal interval (Lemma B9) |

The six results below are the ones the rules stand on. Each is proved in Appendix B.

### 5.1 Keep, check or let it fade

**Result 2 (hold or fade; Theorem G).** For any stationary Markov world and any loss, checking a fact periodically beats letting it fade **iff λ·c < Φ**: the world's drift speed λ times the price of a check is less than the lifetime value of a fresh reading.

*Why.* Over a check cycle, the saving against acting blind is the integral of what a reading is still worth as it ages. That integral only grows with the cycle length, and its limit is Φ, so some cycle beats fading exactly when Φ exceeds the drift-scaled price of a check.

Three consequences complete rule 2 and rule 7. A copy's value only falls with age and with hops (G1, by Blackwell's garbling theorem). Watching effort rises with stakes (G4) and with drift, then stops: with any bounded fallback, such as reading the source at use, it falls off a **cliff**, not a slope (G3). And with a lookup price u, use rate μ, read price c, upkeep h and lifetime τ_life, a fact is **frozen** when drift is below q_f = 2c/(W·τ_life²), **looked up** when drift is above q_c = (μu − h)²/(2cW), and **held** in between. That holding band exists iff μu·τ_life > 2c + h·τ_life, and a store shared by N users widens it by a factor N² (Result T8). With no action whose payoff depends on the world, Φ = 0 and nothing is ever held (E1): this is why atoms are frozen. The statement is partly definitional.

### 5.2 How often to look

**Result 3 (the read-rate rule).** In a drifting world (W-b) with exact reads, holding the last value in between, under squared-error loss:

  **read rate ∝ (w·q / c)^{1/α}**

where w is the stake, q the drift level and c the price of a read. At α = 2 this is the familiar square-root rule (economic order quantity, Harris 1913; Kalman/Muth). Away from α = 2 the elasticity is 1/α, so the same rule gives different exponents in worlds with different spectra.

*Why.* After a read at age s, the error is q·s^{α−1}. Averaging over a cycle of length T and adding the read price gives c/T + w·q·T^{α−1}/α, which is minimized at T\* ∝ (c/(w·q))^{1/α}.

The rule is forgiving: misjudging an input by 2× costs 6% at α = 2, and by 10× costs 74% (Result T1c). It sits in a family of known results with the same structure (noisy-sensing error, memory time, a forgetting kernel that is exponential only at α = 2, precision effort, the number of stores), stated with credit in Appendix B (Lemma B2). The premises travel with every row: a Gaussian world or the best linear tracker (in a jump world the Bayes and linear optima differ, and jump rate and size enter separately); exact versus noisy reads; and the loss as an input (under absolute error at α = 2 the exponents are ⅔ and ⅓).

### 5.3 When to share a model

**Result 4 (when a shared level pays).** N members each track g + u_i: a driver g they share and a part u_i of their own, with ratio ρ = (shared drift)/(private drift). Compare all-local tracking with one shared tracker of g plus local trackers of each u_i, under the square-root rule and zero upkeep. Then:
- **(onset)** the shared level is cheaper **iff N > N\*(ρ) = (√(1+ρ) + 1)²/ρ**, which is about 4/ρ when the shared part is small. Since a better joint design can only do better, this is a sufficient condition for sharing, not a cutoff.
- **(telling price)** if telling a member costs d and a read costs c, sharing the common part pays **iff d/c < 1/N\*(ρ) − 1/N**. At d = 0 this is the onset.
- **(the level's technology sets the exponent)** for any technology whose cost scales as stakes^a·drift^b, the onset at small ρ scales as ρ^{−(1−b)/(1−a)}. That exponent is **−1 for exact reset reads at every α**, and −(1+θ) when precision is priced as precision^θ. It is set by how the level senses, not by the world's spectrum.

*Why.* Sharing turns N reads of the common driver into one, a saving that grows like N, while the shared tracker's cost grows only like N^a, because its stake is pooled. A convex gain that starts negative crosses zero once. The telling price adds N·d to the shared read and moves the crossing.

The onset −1 is prior art in substance (Veldkamp & Wolfers 2007; Van Zandt & Radner 2001). The exact form, the telling-price rule, and the fact that the exponent is fixed by the level's technology independently of α appear to be new; they are elementary (CLAIM_MAP N12). Related results are stated in Appendix B: shared and private drift push the onset in opposite directions; a new level's vigilance at birth is at least 1 + (1+ρ)^{−1/2} (reset reads, α = 2); separate clocks for two components save at most 29%; pooled deposits on a drifting target fade as √N.

### 5.4 Who must be in charge

**Result 5 (one clock, and who under-watches).** One clock serving several parts costs at least what the parts would pay on their own clocks, with equality **iff c_i/(w_i·σ_i²) is the same for every part** (the analogue of Gorman's 1953 condition for a representative agent). If a part counts only Λ_i of the loss Λ_whole that the whole suffers when it fails, it watches at (Λ_i/Λ_whole)^{1/α} of the whole's optimal rate. That is √ at α = 2, so a worker that shares relatedness r of its colony's fate under-watches by about 13% even in the best case (r = ¾, full sisters under single mating).

*Why.* Cauchy–Schwarz gives the first part. The read-rate rule, applied to the stake each part actually bears, gives the second.

**So:** no one *needs* to be in charge *when* keeping shared memory up is privately rewarded. Otherwise expect shared fate or enforcement, usually both (CLAIM_MAP J9, a hypothesis, open). Result 5 is the derivable half of that claim. This narrows the earlier "no one in charge"; rule 6's mechanism (use strengthens, disuse fades) does not follow from the budget.

### 5.5 How far one tracker can reach

**Result 6 (LAT-1).** A tracker that reads a target at distance L sees it late by ℓ = L/v, where v is the fastest signal path, and holds the last value. Its error is at least q·ℓ^{α−1}, however often it reads. So it can hold a target to tolerable error D\* only within

  **L_max = v · (D\*/q)^{1/(α−1)}.**

What that implies depends on shortcuts, and all three cases stand:
- **No shortcut** (v is light speed): beyond L_max a system must **federate** into separate trackers with their own reads. On Earth this is a latency cost; across space it is a hard cap.
- **A finite network of shortcuts**, each spanning at most Λ_hop at hop latency τ_hop: LAT-1 holds with v replaced by an effective speed of at most max(Λ_hop/τ_hop, light speed). Federation survives with a larger constant.
- **Open shortcuts** (any point to any other at fixed latency): there is no distance limit, and the economics of §5.3 decide the design.

The theory does not say which case holds in nature. That shortcuts exist is not claimed. The real-system form (the central share falls with q·ℓ^{α−1}) is open (CLAIM_MAP N27).

### 5.6 Buffers and failure

A system with buffer B, diffusive shocks of size σ and one fixing time scale τ has hazard F(z)/τ with **z = B/(σ√τ)**, for any fixing mechanism, by dimensional analysis. 1/z is the "temperature". The elasticities obey **ε_B = −ε_σ and ε_τ = ε_σ/2 − 1**, so slow fixing raises the hazard iff ε_σ > 2, and at a fixed observed spread ε_τ = −1 (Result R). z is the inventory safety factor, and the exact per-window ruin is Black & Cox's (1976) first-passage formula. Survival-optimal checking is faster than cost-optimal checking. The buffer does not change the best interval; it sets what extra effort to survive is worth, which peaks when the buffer is about one ruin length (Theorem L, Lemma B9). The 12 November post's lead prediction built on this index failed on proxy (§7).

## 6. Predictions, and how it dies

**The bet dies** if, in two or more strongly selected systems at different scales with inputs measured on each system, the design misses its measured-input optimum by more than measurement error allows *and* a named rival (a fixed budget share; a universal exponent of ½) fits better. It also dies if design fails to move with a measured change in its inputs by the preregistered share, or if a level needs a cost that cannot be booked in the bill (§2.2). The locks (loss, rival, adjustment lag) are in `measurement/FRAMEWORK.md`.

**Sharper predictions**, each with its kill:

| Prediction | From | Status | Dies if |
|---|---|---|---|
| Look rate at a drifting quantity has elasticity 1/α in stakes and drift | Result 3 | Open (CLAIM_MAP N51; a lab test is specified) | Elasticities at α = 1.5 and 2.5 are not separated in the predicted direction at the preregistered power |
| Watching effort rises with drift, then collapses once a bounded fallback exists | G3 | Proved in-model; known for web crawlers; untested across domains | Effort keeps rising through the top drift decile where a fallback exists |
| A shared level appears once group size exceeds N\*(ρ) | Result 4 | Proved in-model (sufficient); untested in the field | The size at which a shared layer appears does not move with ρ |
| The onset exponent tracks the level's sensing technology, not α | Result 4 | Proved in-model | Onset exponents differ across α at a fixed technology |
| A tracker's central share falls with q·ℓ^{α−1} | Result 6 | Open (CLAIM_MAP N27) | At fixed q the central share does not depend on ℓ |
| Cheap lookup removes layers that hold shared facts, not layers that enforce | T8, Result 5 | Open (CLAIM_MAP N52) | Enforcement layers shrink as fast as holding layers |

**The first tests anyone can run:** the attention-exponent lab task (N51) and a same-system test of measured-input optimality (SAME-SYSTEM-AQN, designed, not yet run). **The measurement rule:** quantities must pass validity gates MV1–MV10, fixed before any test and binding since 18 November 2026. A test on a mismatched proxy is invalid, not failed, and results are reported as passed or failed on proxy.

## 7. Where it stands

- **No field test has yet measured the theory's quantities validly, so the bet is untested, not refuted.** Every field result so far is proxy-labeled: 15 rows failed on proxy and 7 passed on proxy, and none is support or refutation (CLAIM_MAP sections H, K, N).
- **The 12 November post's lead prediction** (slow fixers fail faster where shocks are large relative to buffers, risk ∝ shock × √(time to fix) ÷ buffer) got every sign right but failed on proxy in its τ-specific structure (CLAIM_MAP K4). The open-source test (C3) excludes only a deterministic, exogenous reset clock at that proxy; with heavy-tailed or endogenous fix intervals, a hazard ratio of 1.2–3 per doubling remains compatible.
- **In-model simulations:** of the locked predictions about the authors' own simulators, six failed, three passed and three were inconclusive (CLAIM_MAP section G).
- **Review:** each theorem has been refereed at most once, always by a reviewer from the same bot family as its author, and some (the internal-model results) only self-checked. No review covers the whole theory, and no human expert has read it. The reviews are listed in `reviews/README.md`.
- **Open items of the core:** P for drifting worlds (CX1); stakes w never yet measured validly; the second-law disagreement (§2.3).

## 8. What is new, and what is not

**Known and credited:** the three ways to last (Prigogine; Pross); filtering and inattention (Kalman 1960; Muth 1960; Sims 2003; Reis 2006); the square-root rule (Harris 1913); team theory (Marschak & Radner 1972); information choice and pooling (Veldkamp & Wolfers 2007; Van Zandt & Radner 2001); cache freshness (Cho & Garcia-Molina 2003); near-decomposability (Simon 1962); thermodynamics of prediction and sensing (Landauer; Still et al. 2012; Barato, Hartich & Seifert 2014; Lan et al. 2012; Mora & Nemenman 2019; Lee, Flack & Krakauer 2024); first-passage default (Black & Cox 1976); monotone comparative statics (Topkis 1978); bet-hedging (Kussell & Leibler 2005). The full list is in `litmap/`.

**The theory's own, as far as anyone has found:**
1. **The synthesis**: one three-part bill, with ruin and a selection tolerance, priced the same way from cells to cities, with every cost term booked (§2.2). Most pieces exist; no one is known to have assembled them into one budget with one set of relations and tested it across scales with measured inputs.
2. **The bet** posed so that it can fail at every scale, with measured inputs, a fixed rival, preregistered kills and validity gates.
3. **Elementary results that appear to be new:** hold-or-fade for any Markov world and any loss (Result 2); the freeze, hold and look-up band with its N² widening (T8); the onset exponent fixed by the level's technology, independently of α, and the telling-price rule (Result 4); the vigilance floor; the exact form of LAT-1 (Result 6); the temperature identity (Result R); and when judgment pays, with the persistence operating point (Result 1).

Each is new only "as far as we know": the prior-art search is not exhaustive, and none of these is claimed as deep. The structure is the point.

## 9. Scope at the ends

Atoms are frozen because no action of theirs changes whether they last (E1). Stars regulate themselves and anticipate nothing outside. A black hole is the extreme of the frozen class: the most memory physics allows for its size, almost none of it readable from outside in time (CLAIM_MAP N26, conditional on published physics). The cosmic horizon caps memory and sets a floor on the price of erasure. A *selected* model switches on only with heredity below the error threshold, an action that depends on the world, drift inside the holding band, and a first nat that pays (N28, open). The costs are priced as floors at every scale, which is the author's scope choice; what vanishes at the ends is the *value* of a model, not the bill.

The theory does **not** derive black holes, the area law or the Page curve, and it does not claim a torus universe, dark matter or energy, that wormholes exist, or that time is fractal (N46, withdrawn as framing). Notes on viruses, the cosmic web, wormholes and a torus picture are reference material (`theory/REACH.md`).

---

## Appendix A. Notation

One symbol, one meaning, throughout this file. Files elsewhere in the repository use some symbols differently; where they do, this table governs, and the last column names the main collisions.

| Symbol | Meaning | Elsewhere it can also mean |
|---|---|---|
| X_t, M_t, A_t | world state; agent's memory; action | — |
| k | lead time (an action meets the world k later) | Boltzmann's k in kT (written kT only) |
| ℓ(a, x); w (or W for a pooled or per-user stake) | loss; stake weight on squared error | ℓ also latency in `theory/` files (here: ℓ = L/v only in §5.5 and CT19) |
| D(R), R(D) | distortion-rate and rate-distortion functions; D\* a tolerable error | — |
| I_pred | long-run predictive information I(M_t; X_{t+k}) per step | — |
| y, c̄, B | income rate; mean of the other costs (per policy); initial buffer | — |
| α, H, q | spectral slope (S ∝ \|ω\|^{−α}), α = 1 + 2H; drift level in E(ΔX_τ)² = q·τ^{α−1} | α also an α-stable index or a Pareto exponent; q also the spectral level q in S = q\|ω\|^{−α}, which differs by an α-dependent constant |
| σ² | variance rate at α = 2 (then q = σ²) | — |
| c | price of one read | the speed of light (written "light speed" here) |
| κ | price per nat held per unit time (per bit in CT4) | a sharing-decay exponent, κ_F, κ = λN/μ² (written out where used) |
| κ_b, d, u, μ | broadcast link cost; price of telling one member; price of one lookup; use rate | — |
| h | upkeep of a store or a level | hops; hazard (here: hazard is ν) |
| ν | failure hazard (per unit time) | — |
| Λ, Λ_i | loss to the whole when it fails; the share part i counts | Λ also a throat's span (here: Λ_hop) |
| λ | drift speed (time rescaling) in Results 2, G1, G3, G4 | a switching rate in `theory/` files |
| Φ | lifetime value of a fresh reading, ∫₀^∞ (r_∞ − r(u)) du | — |
| r(u), r_∞ | Bayes risk of a reading of age u; blind risk | r also relatedness (here: r_rel) and a noise variance |
| N, ρ | number of members; ρ = q_g/q_u, shared over private drift | N also a sensing-noise density (here: σ_n²) |
| a, b | stakes and drift elasticities of a technology's minimized cost, φ ∝ w^a·q^b | — |
| θ | precision-price exponent (spend ∝ precision^θ) | a Lundberg exponent (here: ϑ) and an outage mean |
| B, σ, τ, z | buffer; shock scale; fixing time scale; **z = B/(σ√τ)** (temperature = 1/z) | `theory/GENERAL_THEOREM.md` §4 writes z = σ√τ/B |
| L, v, τ_hop, Λ_hop | extent; fastest signal speed; hop latency; span of one shortcut | — |
| ε | selection tolerance | ε_X = ∂ ln ν/∂ ln X, an elasticity |

---

## Appendix B. Proofs

Each result gives its hypotheses, a statement, a proof and its known limits. **CT** marks the 19 core results, proved in full. **Lemma B*k*** marks smaller results, proved briefly or stated with a pointer. Closed forms are checked in `theory/core_checks/core_checks.py` (32 checks, a few seconds; run by the test suite), and each result names its fuller derivation and older checks. Status words follow CLAIM_MAP section O.

**Names used in the main text.** Result 1 = CT1–CT4 (Theorem P); Result 2 = CT9 (G2); Result 3 = CT12; Result 4 = CT14–CT16; Result 5 = CT17; Result 6 = CT19 (LAT-1). E1 = CT5, I5 = CT6, O1 = CT7, G1 = CT8, G4 = CT10, T8 = CT11, T1c = CT13, R = CT18 (the temperature identity), G3 = Lemma B1, Theorem L = Lemma B9, Theorem S = Lemma B12.

**Standing assumptions.** (A1) The world is exogenous: actions do not change it. (A2) In class W-a, (X, M) is jointly stationary and ergodic under the policy. (A3) A check returns a reading of fixed quality and resets the copy (renewal), unless a result says otherwise. (A4) Costs are additive in one currency. (A5) Reserve increments are bounded.

### B.1 When judgment pays

**CT1 (P0, the persistence bound).** *World W-a; A1, A2, A5.* Let D(R) be the distortion-rate function of the stationary marginal of X under ℓ, D(R) = min{E ℓ(A, X) : I(A; X) ≤ R}, and I_pred = lim (1/T) Σ_t I(M_t; X_{t+k}). Then every agent's long-run mean loss is at least D(I_pred). If y − c̄ < D(I_pred), ruin is certain.

*Proof.* A_t is a function of M_t, so I(A_t; X_{t+k}) ≤ I(M_t; X_{t+k}) (data processing). By the definition of D and because D is nonincreasing, E ℓ(A_t, X_{t+k}) ≥ D(I(A_t; X_{t+k})) ≥ D(I(M_t; X_{t+k})). D is convex, so averaging over t and applying Jensen gives mean loss ≥ D(I_pred). The reserve increments are stationary and ergodic with mean at most y − c̄ − D(I_pred) < 0, so R_t → −∞ almost surely (ergodic theorem): ruin is certain. ∎

*At equality* (mean margin exactly 0), ruin is still certain if the increments are nondegenerate (positive asymptotic variance, as for i.i.d. or mixing increments), by recurrence. A bounded coboundary is the exception. *Derivation:* `theory/GENERAL_THEOREM.md` §2; checks `theory/theorem-v2-checks/c6_persistence_bound.py`. Ingredients known (Shannon's rate–distortion; the ergodic theorem).

**CT2 (P1, when a model is necessary).** *As CT1.* Call a policy π₀ blind if I(M_t; X_{t+k}) = 0. Blind action is viable (survival with positive probability for a large enough B) iff some blind policy has D(0) < y − c̄(π₀). A model is necessary iff every blind policy has D(0) ≥ y − c̄(π₀), with nondegenerate increments at equality.

*Proof.* A blind agent's action is independent of X_{t+k}, so its mean loss is at least min_a E ℓ(a, X) = D(0). If D(0) ≥ y − c̄(π₀) for every blind π₀, CT1 (with I_pred = 0) makes ruin certain for every blind agent, so a persistent agent must have I_pred > 0. Conversely, if a blind policy using the minimizing action has margin m = y − c̄(π₀) − D(0) > 0, then R_t − B → +∞ almost surely, so inf_t (R_t − B) is finite almost surely and P(inf_t R_t > 0) → 1 as B → ∞. ∎

The inequality is strict and c̄ depends on the policy, since a blind agent pays no memory or read cost (math-attack review G3, applied 19 Nov 2026). *Counterexample* to "every self-maintaining system pays for a model": a bet-hedging lineage in an i.i.d. world grows at ln 1.5 per generation with zero predictive information (Kussell & Leibler 2005; `c7d`).

**CT3 (P2, the lead-time cap).** *As CT1, X Markov.* I(M_t; X_{t+k}) ≤ I(X_t; X_{t+k}), and the right side is nonincreasing in k. So persistence requires k ≤ k_max, the largest k with I(X_t; X_{t+k}) > R(y − c̄).

*Proof.* M_t depends on the world only through X_s, s ≤ t, and X is an exogenous Markov chain, so M_t → X_t → X_{t+k} is a Markov chain and data processing gives the first inequality. X_t → X_{t+k} → X_{t+k+1} is Markov, so I(X_t; X_{t+k+1}) ≤ I(X_t; X_{t+k}). By CT1, persistence needs D(I_pred) < y − c̄, i.e. I_pred > R(y − c̄), which is impossible once I(X_t; X_{t+k}) ≤ R(y − c̄). ∎ *Example:* a binary world flipping with probability 0.05 per step, income 0.30: k_max = 7 (`c6a`).

**CT4 (P3, the first bit must pay).** *As CT1, with memory priced κ per bit per step.* Let IB(I) = sup{I(M; X_{t+k}) : I(M; past) ≤ I}, the predictive information-bottleneck curve (concave, nondecreasing). Then L(I) = D(IB(I)) + κI is a convex lower bound on cost at memory size I, and its minimizer is positive iff κ < −(D∘IB)′(0⁺). For a Gaussian AR(1) world X_{t+1} = aX_t + noise with stationary variance Var, lead 1 and squared-error loss, a model is carried iff κ < 2 ln 2·a²·Var, and then I\* = ½ log₂(2 ln 2·a²·Var/κ).

*Proof.* D is convex and nonincreasing and IB is concave, so D∘IB is convex and L is convex on [0, ∞). A convex function's minimizer is positive iff its right derivative at 0 is negative: (D∘IB)′(0⁺) + κ < 0. In the Gaussian case the best memory is a noisy copy of X_t; with I bits about X_t the error variance of X_t is Var·2^{−2I}, so the prediction loss is Var[(1 − a²) + a²·2^{−2I}]. Its derivative at 0 is −2 ln 2·a²·Var, and setting the derivative of the total to zero gives 2^{−2I} = κ/(2 ln 2·a²·Var). ∎

The bound is tight in the Gaussian and binary-symmetric cases (`c6d`: 2.0014 vs 2.0018 bits by brute force). The Lagrangian (loss plus a price on information) is prior art (Sims 2003; Tishby & Polani 2011); the persistence operating point is the addition. In physical systems that meet Still et al.'s conditions, dissipation is at least kT(I_mem − I_pred), and deriving the information bottleneck from that bound is known (Still 2020).

**CT5 (E1, no decision, no model).** *Hypotheses of CT9.* If no action's payoff depends on the world (one effective action), then Φ = 0 and holding never beats fading, at any drift and any positive read price.

*Proof.* With one effective action, the Bayes risk of a reading of any age equals the blind risk: r(u) = r_∞ for all u, so Φ = ∫(r_∞ − r) = 0, and CT9's condition λc < 0 fails for every c > 0. ∎ Partly definitional. `theory/SCALE_ENDS.md` E1 (CLAIM_MAP N25).

**CT6 (I5, upkeep is a flow).** *World exogenous: M_{t−1} → S_{t−1} → S_t is a Markov chain for the world's causal state S; M_t is a function of (M_{t−1}, Y_t).* Let η be the strong data-processing constant of the channel S_{t−1} → S_t and I_obs = I(Y_t; S_t | M_{t−1}). In steady state, **I_obs ≥ (1 − η)·I(M; S).**

*Proof.* I(M_t; S_t) ≤ I(M_{t−1}, Y_t; S_t) = I(M_{t−1}; S_t) + I_obs (data processing, then the chain rule). By the strong data-processing inequality, I(M_{t−1}; S_t) ≤ η·I(M_{t−1}; S_{t−1}). In steady state both mutual informations equal I, so I ≤ ηI + I_obs. ∎

For a binary world flipping with probability q, η = (1 − 2q)², so I_obs ≥ 4q(1 − q)·I (Polyanskiy & Wu). For unconstrained Gaussian kernels η = 1 and the bound is empty; the jointly Gaussian contraction is used instead, and the Kalman filter meets it with equality (known: Mitter & Newton 2005; Horowitz & Sandberg 2014). `theory/INTERNAL_MODEL.md` §2, checks `i2`. Self-checked only.

**CT7 (O1, the tracking floor).** *A random walk of variance rate σ², not affected by the tracker; a tracker whose learning rate is bounded by its entropy production (Barato, Hartich & Seifert 2014).* Holding a mean squared error D dissipates heat at a rate of at least kT·σ²/(2D). With squared-error stakes w, the least total cost is **J\* = σ√(2kT·w)**, at D\* = σ√(kT/(2w)).

*Proof.* With the estimate fixed, drift destroys information about the walk at rate σ²/(2D) nats per unit time: ½ ln((Var X + σ²dt)/(D + σ²dt)) − ½ ln(Var X/D) → −σ²dt/(2D) as Var X grows. Holding D steady therefore needs a learning rate of at least σ²/(2D), and so dissipation of at least kT·σ²/(2D). Minimizing kT·σ²/(2D) + w·D over D gives D\* and J\* = 2√(kT·σ²·w/2). ∎

This is the same function as the inventory optimum σ√(2c·w) with c replaced by kT per nat. With one cost scale, one drift and one quadratic stake, dimensional analysis forces any optimum to be ∝ σ√(c·w), so only the √2 prefactor is informative. The bound needs no feedback from tracker to signal (otherwise Horowitz & Esposito 2014). `theory/MATH_ATTACK.md` §1.2; cross-checked against Duncan's theorem for the Kalman–Bucy filter (`objective_checks.out` §1).

### B.2 Keep, check or fade

*Setting for CT8–CT11 and Lemma B1.* A stationary Markov world (W-a), any loss, renewal checks (A3). r(u) is the Bayes risk of acting on a reading of age u (in drift-time units), with r(∞) = r_∞; the world's drift speed is λ (time rescaled as X_{λt}).

**CT8 (G1, staleness is monotone).** r(u) is nondecreasing in u, for every loss; a chain of copies with independent noise at each hop has risk nondecreasing in the number of hops.

*Proof.* By stationarity, r(u) is also the risk of predicting X_{u+s} from a reading at time s, while r(u + s) is the risk of predicting X_{u+s} from a reading at time 0. Since X_0 → X_s → X_{u+s} is Markov, the reading at 0 is a garbling of the reading at s with respect to X_{u+s}, and a garbling never lowers Bayes risk (Blackwell 1953). So r(u + s) ≥ r(u). A copy chain with independent hop noise is a garbling chain, so the same argument applies to hops. ∎

*Fails* for non-Markov observed coordinates: for an MA(2) signal a two-step-old reading has squared error 1.5 against 2.0 for a one-step-old one; seasonality does the same. Known in substance (Sun & Cyr, mutual-information version). CLAIM_MAP K6.

**CT9 (G2, hold or fade).** Checking every T, with s = λT, costs J(s) = λc/s + A(s) per unit time, where A(s) = (1/s)∫₀ˢ r(u) du; fading costs r_∞. **Some periodic schedule beats fading iff λ·c < Φ := ∫₀^∞ (r_∞ − r(u)) du.**

*Proof.* J(s) < r_∞ ⇔ λc < s(r_∞ − A(s)) = ∫₀ˢ (r_∞ − r(u)) du =: Ψ(s). By CT8 the integrand is nonnegative, so Ψ is nondecreasing with supremum Φ. Hence some s satisfies Ψ(s) > λc iff λc < Φ. ∎

The critical drift speed is λ_c = Φ/c. State-dependent intervals can only help (Φ/c ≤ λ_c ≤ sup_x Φ\*(x)/c), and retained history (filtering instead of renewal) only lowers holding cost, so λ < Φ/c remains sufficient. Checked: a two-state chain with 0–1 loss has Φ = ¼ and λ_c = 5 at c = 0.05, holding at 4.9 and fading at 5.1 (`core_checks.py`; `c1b`, `c1d`). Generalizes Cho & Garcia-Molina 2003; novelty unconfirmed.

**CT10 (G4, effort rises with stakes).** With check frequency f and stake w, J(f; w) = c·f + w·A(λ/f). The minimizing f is nondecreasing in w.

*Proof.* A is nondecreasing (a running average of a nondecreasing r), so A(λ/f) is nonincreasing in f. For f′ > f, J(f′; w) − J(f; w) = c(f′ − f) + w[A(λ/f′) − A(λ/f)] is nonincreasing in w: J has decreasing differences in (f, w), and the minimizer is nondecreasing in w (Topkis 1978). ∎ Known in substance; `c1c`.

**CT11 (T8, freeze, hold or look up).** *One item; squared-error loss at stake W; drift q at α = 2; read price c; upkeep h; lifetime τ_life; use rate μ; lookup price u per use, with μu > h.* Holding costs min_{T ≤ τ_life}[c/T + WqT/2] + h, freezing is the corner T = τ_life, and looking up costs μu. Then:
1. Freeze iff q ≤ q_f = 2c/(W·τ_life²).
2. Look up rather than hold iff q > q_c = (μu − h)²/(2cW).
3. A holding band exists iff μu·τ_life > 2c + h·τ_life.
4. A store shared by N users (stakes NW, lookups Nμu) multiplies q_c/q_f by N² at h = 0.
5. Effort just below q_c is (μu − h)/(2c) reads per unit time, and 0 above it: a cliff.

*Proof.* The interior optimum is T\* = √(2c/(Wq)), with cost √(2cWq) + h. (1) T\* ≥ τ_life ⇔ q ≤ 2c/(Wτ_life²). (2) √(2cWq) + h > μu ⇔ q > (μu − h)²/(2cW). (3) q_f < q_c ⇔ 4c² < τ_life²(μu − h)² ⇔ 2c < τ_life(μu − h). (4) With W → NW and μu → Nμu at h = 0, q_f is divided by N and q_c is multiplied by N. (5) The read rate 1/T\* = √(Wq/(2c)) at q = q_c equals (μu − h)/(2c). ∎

The cliff is known (Cho & Garcia-Molina 2003). The band condition and the N² widening appear to be new. If lookups return stale values or carry their own lag, the edge moves (not derived). `reviews/night1/formal/THEOREMS.md` Theorem 8; `reviews/night1/formal/checks/s5_phase.py`; CLAIM_MAP F13.

**Lemma B1 (G3, rise then fall).** Watching effort f\*(λ) rises from 0 as λ → 0 (as √(λ·r′(0)/(2c)) when r′(0) is finite), is positive on (0, λ_c) and is 0 for λ ≥ λ_c. With fallback at blind risk and r approaching r_∞ exponentially, it falls toward 0 only logarithmically (a near-cliff). With a bounded fallback F < r_∞ (read the source at use), holding stops at λ_c = Φ_F/c, with Φ_F = ∫₀^{s_F}(F − r), and effort jumps from λ_c/s_F to 0: a true cliff. If Φ = ∞ (a random walk under squared error with no fallback), effort rises without limit. *Proof:* CT9 applied with the fallback's cost in place of r_∞; `theory/GENERAL_THEOREM.md` §3, `c1e`.

### B.3 How often to look

*Setting for CT12–CT13.* A drifting world (W-b): Gaussian with stationary increments, E(X_{t+τ} − X_t)² = q·τ^{α−1}, 1 < α < 3. Exact reads at price c that reset the copy; the last value is held in between; squared-error loss at stake w.

**CT12 (the read-rate rule).** The optimal read interval is T\* = [α·c/((α − 1)·w·q)]^{1/α}, so the read rate is **∝ (w·q/c)^{1/α}**, and the minimized cost scales as c^{(α−1)/α}(w·q)^{1/α}: stakes and drift elasticities a = b = 1/α = 1/(1+2H). Equal gaps are optimal.

*Proof.* A copy of age s has squared error q·s^{α−1}. Over a cycle of length T the mean error is (1/T)∫₀^T q·s^{α−1} ds = q·T^{α−1}/α, so the cost rate is J(T) = c/T + w·q·T^{α−1}/α. J is strictly convex for α > 1, and J′(T) = −c/T² + w·q·(α − 1)·T^{α−2}/α = 0 gives T\*. Substituting gives the cost scaling. For n reads over a fixed horizon with gaps T_k, the cost nc + (w·q/α)·Σ T_k^α is minimized at equal gaps, by convexity of T^α (Jensen). ∎

At α = 2 this is T\* = √(2c/(w·σ²)): the economic order quantity (Harris 1913) and the inattention rule (Reis 2006). The exponent holds for hold-last-value and for the optimal linear predictor (any predictor class closed under time rescaling), but not for a predictor with a fixed time constant. For H ≠ ½, hold-last-value is a restricted technology (a predictor that uses the path does better). For the Bayes tracker of a non-Gaussian world, more of the world's law can enter: in a two-level switching world, jump rate and jump size enter separately (CLAIM_MAP N16). Formal Lemma 1(i); CLAIM_MAP N7.

**CT13 (T1c, robustness).** Reading at k·T\* instead of T\* raises the cost by the factor [(α − 1)/k + k^{α−1}]/α, which is (k + 1/k)/2 at α = 2. Misjudging c/(w·q) by a factor m sets k = m^{1/α}: at α = 2 that costs +6% at m = 2 and +74% at m = 10.

*Proof.* At T\* the first-order condition gives c/T\* = (α − 1)·E\* with E\* = w·q·T\*^{α−1}/α, so J\* = α·E\*. Then J(kT\*) = (α − 1)E\*/k + E\*·k^{α−1}. ∎ CLAIM_MAP M3.

**Lemma B2 (the rest of the spectrum map; known, stated with credit).** For a Gaussian world or the best linear tracker, with white observation noise of density σ_n²: the error of noisy continuous sensing is q^{1/α}σ_n^{2(1−1/α)}/sin(π/α) (Afterman et al. 2022; Kleptsyna et al. 2020); memory time ∝ (σ_n²/q)^{1/α} (Wiener/Kalman bandwidth); the optimal forgetting kernel puts weight ∝ τ^{−(1+α/2)} on an observation of age τ and is exponential only at α = 2 (Nuzman & Poor 2000; Gripenberg & Norros 1996); precision effort with a linear price ∝ w^{α/(2α−1)}q^{1/(2α−1)}; and the number of stores grows with the span of time scales and with stakes over upkeep away from α = 2 (rate conjectural). Premises and credits: `reference/THEORY_v1.4.29.md` §2.2.

### B.4 When to share a model

*Setting for CT14–CT16 (architecture class 𝒜₁).* N members, each tracking x_i = g + u_i, with g and the u_i independent and drifting with the same α at levels q_g and q_u; ρ = q_g/q_u. A sensing technology has minimized cost φ(w, q) = K·p^{1−a}w^a q^b with 0 ≤ a < 1 and 0 < b < 1 (the class P(a, b)). *Flat:* every member tracks x_i, at cost N·φ(w, q_g + q_u). *Level:* one tracker of g with the pooled stake N·w, plus a tracker of each u_i, at cost φ(Nw, q_g) + N·φ(w, q_u) + h. Equal prices unless stated.

**CT14 (pooling onset).** In units of K·p^{1−a}w^a q_u^b, the gain of the level is G(N) = N[(1+ρ)^b − 1] − N^a ρ^b − h′. G crosses zero exactly once, so the level is optimal iff N > N\*. At h = 0, **N\* = [ρ^b/((1+ρ)^b − 1)]^{1/(1−a)}**. As ρ → 0, N\*·ρ^{(1−b)/(1−a)} → b^{−1/(1−a)}, so the onset scales as ρ^{−(1−b)/(1−a)}. For the square-root technology (a = b = ½), **N\* = (√(1+ρ) + 1)²/ρ**.

*Proof.* Drift levels of independent components add, so flat costs N·K p^{1−a}w^a(q_g + q_u)^b; the pooled stake gives the level K p^{1−a}(Nw)^a q_g^b. Write A = (1+ρ)^b − 1 > 0 and C = ρ^b > 0, so G(N) = NA − N^a C − h′. Then G″ = a(1 − a)N^{a−2}C > 0 for a > 0 (G is linear if a = 0), G(0) = −h′ ≤ 0 and G → +∞. A convex function that starts at or below 0 and diverges crosses 0 exactly once from below; at h = 0 and a > 0, G < 0 near 0 because N^a dominates N. Setting G = 0 at h′ = 0 gives N^{1−a} = C/A. Since (1+ρ)^b − 1 = bρ + O(ρ²), C/A·ρ^{1−b} → 1/b. At a = b = ½, N\* = ρ/(√(1+ρ) − 1)² = (√(1+ρ) + 1)²/ρ, since (√(1+ρ) − 1)(√(1+ρ) + 1) = ρ. ∎

Within 𝒜₁ the condition is exact. A joint design outside 𝒜₁ can only do better, so for real choices **N > N\* is sufficient** for some shared design to beat flat, not a cutoff. With upkeep h > 0 the small-ρ exponent stays −(1−b)/(1−a) if a > b and becomes −1 if a ≤ b. With a cost linear in stakes (a = 1) no level ever pays. If the level and the members use different technologies, the **level's** (a_L, b_L) sets the exponent. `reviews/night1/formal/THEOREMS.md` Theorem 1; `s2_onset.py`, `s9_attack.py`; CLAIM_MAP B1–B3, B9. The onset −1 is prior art in substance (Veldkamp & Wolfers 2007, Prop. 2; Van Zandt & Radner 2001).

**CT15 (the level's technology sets the exponent, independently of α).** For exact reset reads the onset exponent is **−1 at every α**. For continuous sensing with precision priced as precision^θ it is **−(1 + θ) at every α**.

*Proof.* By CT14 the exponent is −(1−b)/(1−a). Reset reads have a = b = 1/α (CT12), so it is −1. For priced precision: with white observation noise of intensity r_n, the steady-state error of the best linear tracker is P = C_α·q^{1/α}·r_n^{(α−1)/α}. This is the form of Lemma B2; it is also forced by units, since q has units x²·t^{1−α}, r_n has units x²·t, P has units x², and the scale-free model has no other parameter. Minimizing W·C_α q^{1/α} r_n^{β} + c′·r_n^{−θ} over r_n, with β = (α − 1)/α, gives a cost ∝ (W q^{1/α})^{θ/(θ+β)} c′^{β/(θ+β)}. So a = θ/(θ + β) = αθ/(α(θ+1) − 1) and b = a/α = θ/(α(θ+1) − 1), and (1 − b)/(1 − a) = 1 + θ. ∎

*Premises:* the same α for shared and private drift; exact reads at the level (read noise steepens the exponent toward −2 at small ρ); no broadcast cost; h = 0 or a ≥ b; small ρ. What does depend on α: vigilance growth (∝ N^a), the mixed-technology private-drift exponent, and every constant. Refereed (`reviews/night2/N12_REFEREE.md`). CLAIM_MAP N12 is labelled MATH-CORRECTED because the original statement's scope claims were false; the exponent itself stands.

**CT16 (the telling price).** *𝒜₁ at a = b = ½ (square-root rule), zero latency.* A read costs c and telling one member costs d. Reading g centrally and telling all N members, plus reading each u_i locally, costs √(2(c + Nd)·N·w·q_g) + N√(2c·w·q_u). All-local costs N√(2c·w·(q_g + q_u)). **The hybrid is cheaper iff d/c < 1/N\*(ρ) − 1/N.**

*Proof.* The central tracker pays c + Nd per update for N stakes, so its cost is √(2(c + Nd)·Nw·q_g). Divide both sides of hybrid < all-local by N√(2c·w·q_u): √((1 + Nd/c)ρ/N) + 1 < √(1+ρ) ⇔ (1 + Nd/c)/N < (√(1+ρ) − 1)²/ρ = 1/N\*(ρ) ⇔ d/c < 1/N\*(ρ) − 1/N. ∎

At d = 0 this is CT14; as ρ → ∞ it becomes d/c < 1 − 1/N. Latency ℓ on the shared part adds N·w·q_g·ℓ to the hybrid. Like CT14 it compares one feasible hybrid with all-local, so it is sufficient for centralizing the shared part. It is a rule about any price of dissemination, and it is not conditional on shortcuts (CLAIM_MAP N41 is its shortcut instance; `theory/WORMHOLES.md` §2, 180/180 brute-force cases).

**Lemma B3 (shared and private drift push the onset in opposite directions).** ∂N\*/∂q_g < 0 < ∂N\*/∂q_u at every ρ, for a common technology (CLAIM_MAP C1; formal Theorem 3).

**Lemma B4 (vigilance at birth).** In the reset class at α = 2, the new level's effort over a flat member's effort at onset is V(N\*) = ½(1 + (1+ρ)^{−1/2})(1 + √(1 + 4h′(√(1+ρ) − 1)/(rρ))), where r is the level's price over a member's and h′ is upkeep in member-cost units. Its floor (h′ = 0) is **1 + (1+ρ)^{−1/2}**, strictly between 1 and 2. The earlier "V ≥ 2" is false as stated (CLAIM_MAP E5, E6, E7).

**Lemma B5 (clocks).** With K independent components read separately at additive cost, separate clocks save at most 1 − K^{−(1−γ)}: 29% for K = 2 at γ = ½. With indivisible reads they never save (formal Proposition 9; known).

**Lemma B6 (selection resolution).** In 𝒜₁ a level's largest possible fractional saving (N → ∞) is 1 − (1+ρ)^{−b} ≤ bρ (Bernoulli's inequality). So if selection resolves only relative differences larger than ε, no level is selected at any N when ρ ≤ (1 − ε)^{−1/b} − 1 ≈ ε/b: 0.020 at ε = 1% and 0.108 at ε = 5% (b = ½). Formal Proposition 10; CLAIM_MAP F15.

**Lemma B7 (√N fade).** Pooled deposits by N independent users on a drifting target fade faster as √N; on a stable target use preserves. Known (Kalman averaging), linear readouts only; an ant-like nonlinear readout failed in simulation (CLAIM_MAP K9, G15).

### B.5 Who must be in charge

**CT17 (one clock, and the externality).** (i) K parts at α = 2 with read prices c_i, stakes w_i and drifts σ_i² cost Σ σ_i√(2c_i·w_i) on their own optimal clocks, and √(2·Σc_i·Σw_iσ_i²) on one shared clock. The shared clock is never cheaper, with equality **iff c_i/(w_iσ_i²) is the same for all i**. (ii) If the whole loses Λ_whole when a part fails but the part counts only Λ_i, the part's chosen read rate is (Λ_i/Λ_whole)^{1/α} of the whole's optimum.

*Proof.* (i) One clock with interval T costs Σc_i/T + Σw_iσ_i²·T/2, minimized at √(2Σc_iΣw_iσ_i²). By Cauchy–Schwarz, (Σ√c_i·√(w_iσ_i²))² ≤ Σc_i·Σw_iσ_i², with equality iff √c_i ∝ √(w_iσ_i²). (ii) By CT12 the read rate scales as (stake)^{1/α}, and the part sets it with stake Λ_i instead of Λ_whole. ∎

With heterogeneous read prices the shared-clock penalty is unbounded (51× in random draws, 500× when cost sits in one part and drift in another). A worker sharing relatedness r_rel of its colony's fate reads at r_rel^{1/α} of the optimum; at r_rel = ¾ and α = 2 that is 0.87, so it under-watches by about 13%. The externality half holds when the failure cost is not internalized by incentives, shared fate or a controller, and it counts against "no one in charge" as a general claim. `theory/MATH_ATTACK.md` §3.4 (the analogue of Gorman's 1953 condition).

### B.6 Buffers, failure and the temperature

**CT18 (the temperature identity).** *The error accumulates as σ·W_t from each fix, and fixes act on one time scale τ (periodic resets, Poisson resets at rate 1/τ, or proportional restoring at rate 1/τ). Failure occurs when the error reaches B (one- or two-sided).* Then the hazard is **ν = F(z)/τ with z = B/(σ√τ)**, for some function F fixed by the fixing mechanism. Its elasticities satisfy **ε_B = −ε_σ and ε_τ = ε_σ/2 − 1**. Slow fixing raises the hazard iff ε_σ > 2, and at a fixed observed spread s = σ√τ, ε_τ = −1.

*Proof.* The inputs are σ (units x·t^{−1/2}), τ (t) and B (x), and ν has units 1/t. The only dimensionless group is z, so ν·τ = F(z) (Buckingham π). With g = d ln F/d ln z: ε_B = g, ε_σ = −g, and ε_τ = −g/2 − 1 = ε_σ/2 − 1. At fixed s, ν = F(B/s)/τ, so ε_τ = −1. ∎

z is the inventory safety factor (SS = z·σ·√(lead time)). The index fails once errors are biased (a second group, the Péclet number μ_b·B/σ² for a bias drift μ_b, enters), under heavy-tailed jumps (single big jumps dominate), under long memory (the group becomes σ·τ^H/B), and when fixes do not fully reset. How fixing works sets the tail of F (fixed delay e^{−z²/2}; proportional restoring e^{−z²}; Poisson fixing e^{−√2·z}; heavy-tailed fix times a power law). `theory/MATH_ATTACK.md` §2; `theory/GENERAL_THEOREM.md` R0–R5, which writes z = σ√τ/B.

**Lemma B8 (exact per-window ruin; known).** For periodic full resets and a one-sided barrier, the per-window ruin probability is P = erfc(z/√2) = 2Φ̄(z), the reflection-principle first-passage probability, which is Black & Cox's (1976) default probability at zero drift. Merton's (1974) terminal-default version is off by a factor of 2. The calendar hazard is ν = −ln(1 − P)/τ. Two-sided and biased cases have known series (`theory/GENERAL_THEOREM.md` R1–R2). DOIs: 10.1111/j.1540-6261.1976.tb01891.x; 10.1111/j.1540-6261.1974.tb03058.x.

**Lemma B9 (Theorem L, survival versus cost).** *Reserve income y with noise s₀; a check costs c every τ; squared-error loss w·e² accrues between checks; diffusion approximation, ruin checked at cycle ends.* (L1) P_ruin ≤ e^{−ϑB}, with ϑ the Lundberg root of E e^{−ϑΔ} = 1 for the cycle increment Δ. (L2) The survival-optimal interval is shorter than the cost-optimal one, because the loss variance grows like τ³; they agree when the reserve's own noise dominates. (L3) The survival-optimal interval does not depend on B, and the marginal value of raising ϑ, ∝ B·e^{−ϑB}, peaks at **ϑB = 1**. So rule 7's "watch most where shocks are large relative to buffers" holds for the value of extra effort, not for the cost-optimal interval. Cramér–Lundberg is known (Asmussen & Albrecher 2010). `theory/GENERAL_THEOREM.md` §5, `c3c`.

**Lemma B10 (finite horizon).** If a blind structure's reserve increments have conditional mean ≤ −δ < 0 and centred increments bounded by b, then P(it survives to T) ≤ exp(−(δT − B)²/(2b²T)) for T > B/δ (Azuma–Hoeffding). CLAIM_MAP N33.

**Lemma B11 (the internal-model bound).** The forecast miss of a memory equals the predictive information it fails to carry, δ = I(Past; Fut) − I(M; Fut). With causal states separated by γ_L, P(the memory's decoded state ≠ the world's causal state) ≤ √(2δ)/γ_L, and a solvent agent's memory must nearly copy the world's causal states. Parts are probably folklore (Shalizi & Crutchfield at δ = 0). `theory/INTERNAL_MODEL.md` §2. Self-checked only.

### B.7 How far one tracker reaches

**CT19 (LAT-1).** *W-b; a tracker at distance L from its target receives each reading after latency ℓ = L/v and holds the last value; reads every T.* Its mean squared error is (1/T)∫₀^T q(ℓ + s)^{α−1} ds ≥ q·ℓ^{α−1}, with the bound approached as T → 0. So a tolerable error D\* can be held only if q·ℓ^{α−1} ≤ D\*, i.e. L ≤ **L_max = v·(D\*/q)^{1/(α−1)}**.

*Proof.* At use, the held value is ℓ + s old, where s ∈ [0, T) is the time since the last arrival, so its error is q(ℓ + s)^{α−1} ≥ q·ℓ^{α−1}. Averaging preserves the bound, and reading more often only removes the s part. Inverting q(L/v)^{α−1} ≤ D\* gives L_max. ∎

*The three shortcut cases.* (a) **None:** v is light speed, and beyond L_max a system must federate. (b) **Finite shortcuts**, each spanning at most Λ_hop at hop latency at least τ_hop: a path covering distance D with n hops and light-speed travel time t_light has D ≤ n·Λ_hop + (light speed)·t_light and latency ≥ n·τ_hop + t_light, so its effective speed is at most max(Λ_hop/τ_hop, light speed), and LAT-1 holds with that v. (c) **Open shortcuts**, any point to any other at fixed latency: latency no longer grows with distance, so there is no distance limit, and CT16 decides the design. The theory does not say which case nature provides, and does not claim that shortcuts exist. Prior art in substance: Simon 1962; Tatikonda & Mitter 2004; consistency-latency trade-offs (Abadi 2012). `theory/SCALE_ENDS.md` §5; `theory/WORMHOLES.md` §4b. The real-system form is CLAIM_MAP N27 (open).

### B.8 Scale

**Lemma B12 (Theorem S, covariance and its limits).** (S1) If the objective is homogeneous of degree 1 in one currency, rescaling every cost leaves the optimum unchanged; (S2) rescaling time rescales optimal frequencies. (S3) With loss w|e|^p and self-similar drift e ∼ σ·t^H, the optimal interval is T\* = [c(pH + 1)/(pH·m_p·w·σ^p)]^{1/(1+pH)}: its exponents depend only on (p, H), not on the currency. (S4) Covariance fails when two cost components scale differently with size or currency; the optimum then shows crossovers, not one power. Proofs: S1–S2 by substitution, S3 by the first-order condition, S4 by example (a fixed plus a size-proportional read cost slides the local exponent from −1 to −½). That real systems sit in the generic class (p = 2, H = ½, by Taylor expansion and the central limit theorem) is a conjecture. `theory/GENERAL_THEOREM.md` §6, `c5a`–`c5c`.

---

## Appendix C. Claim index

Every numbered result, with its status (as in `measurement/CLAIM_MAP_v2.md` section O), the row that carries it in the tally, and where its derivation and checks live. `tools/check_consistency.py` fails if an ID here is missing from CLAIM_MAP section O or has a different status there.

| ID | Result | In the main text | Status | Counted row | Derivation; checks |
|---|---|---|---|---|---|
| CT1 | P0 persistence bound | §3, Result 1 | PROVED (in-model) | CT1 | `theory/GENERAL_THEOREM.md` §2; `theory/theorem-v2-checks/c6_persistence_bound.py` |
| CT2 | P1 when a model is necessary (strict) | §3, Result 1 | PROVED (in-model) | CT2 | GENERAL_THEOREM §2 and its 19 Nov erratum; `c7_rules_counterexamples.py` (c7d) |
| CT3 | P2 lead-time cap | §3, Result 1 | PROVED (in-model) | CT3 | GENERAL_THEOREM §2; c6a |
| CT4 | P3 the first bit must pay | §3, Result 1 | PROVED (in-model) | CT4 | GENERAL_THEOREM §2; c6d; `theory/core_checks/core_checks.py` |
| CT5 | E1 no decision, no model | §1, §5.1 | PROVED (in-model) | N25 | `theory/SCALE_ENDS.md` E1 |
| CT6 | I5 upkeep is a flow | §2.3 | PROVED (in-model) | CT6 | `theory/INTERNAL_MODEL.md` §2; `i2_maintenance_sdpi.py` |
| CT7 | O1 tracking floor | §2.3 | PROVED (in-model) | CT7 | `theory/MATH_ATTACK.md` §1.2; `objective_checks.out`; core_checks |
| CT8 | G1 staleness is monotone | §5 rule 5, §5.1 | PROVED (in-model) | K6 | GENERAL_THEOREM §3; c1a |
| CT9 | G2 hold or fade | §5.1, Result 2 | PROVED (in-model) | CT9 | GENERAL_THEOREM §3; c1b, c1d; core_checks |
| CT10 | G4 effort rises with stakes | §5.1 | PROVED (in-model) | CT10 | GENERAL_THEOREM §3; c1c |
| CT11 | T8 freeze, hold or look up | §5.1 | PROVED (in-model) | F13 | `reviews/night1/formal/THEOREMS.md` Thm 8; `reviews/night1/formal/checks/s5_phase.py`; core_checks |
| CT12 | Read-rate rule | §5.2, Result 3 | PROVED (in-model) | N7 | formal Lemma 1(i); `s1_classes.py`; core_checks |
| CT13 | T1c robustness | §5.2 | PROVED (in-model) | M3 | `measurement/FRAMEWORK.md` §3.10; core_checks |
| CT14 | Pooling onset | §5.3, Result 4 | PROVED (in-model) | B2 | formal Thm 1; `s2_onset.py`, `s9_attack.py`; core_checks |
| CT15 | The level's technology sets the exponent | §5.3, Result 4 | MATH-CORRECTED (exponent stands; scope narrowed) | N12 | `reviews/night2/N12_REFEREE.md`; core_checks |
| CT16 | Telling price | §5.3, Result 4 | PROVED (in-model) | CT16 | `theory/WORMHOLES.md` §2; `theory/reach_checks/independent_review_checks.py`; core_checks |
| CT17 | One clock, and the externality | §5.4, Result 5 | PROVED (in-model) | CT17 | `theory/MATH_ATTACK.md` §3.4; core_checks |
| CT18 | Temperature identity | §5.6 | PROVED (in-model) | CT18 | `theory/MATH_ATTACK.md` §2; GENERAL_THEOREM R0; core_checks |
| CT19 | LAT-1 and the three shortcut cases | §5.5, Result 6 | PROVED (in-model) | CT19 | `theory/SCALE_ENDS.md` §5; `theory/WORMHOLES.md` §4b; core_checks |
| CL1 | Lemma B1: G3 rise, then fall; the cliff | §5.1 | PROVED (in-model) | CL1 | GENERAL_THEOREM §3; c1e |
| CL2 | Lemma B9: Theorem L | §5.6 | PROVED (in-model) | CL2 | GENERAL_THEOREM §5; c3c |
| CL3 | Lemma B12: Theorem S | §2.3 | PROVED (in-model) | CL3 | GENERAL_THEOREM §6; c5a–c5c |
| CL4 | Lemma B8: exact per-window ruin (Black & Cox) | §5.6 | PRIOR ART | CL4 | GENERAL_THEOREM R1–R2; core_checks (Monte Carlo) |
| CL5 | Lemma B4: vigilance at birth | §5.3 | PROVED (in-model) | E7 | formal Thm 5 and its 19 Nov erratum; `s11_vclosed.py` |
| CL6 | Lemma B5: clocks | §5.3 | PRIOR ART | F14 | formal Prop 9; `s7_misc.py` |
| CL7 | Lemma B6: selection resolution | §4 | PROVED (in-model) | F15 | formal Prop 10; `s7_misc.py` |
| CL8 | Lemma B7: √N fade | §5.3 | PRIOR ART | K9 | `theory/THEOREMS.md` T4 |
| CL9 | Lemma B10: finite horizon | §3 | PROVED (in-model) | N33 | `theory/BOOKENDS.md`; `finite_horizon.py` |
| CL10 | Lemma B11: the internal-model bound | §3 | PROVED (in-model) | CL10 | `theory/INTERNAL_MODEL.md` §2; `i1_internal_model.py` |
| CL11 | Drift reduction as a lever | §2.2 | OPEN | K17 | `reference/THEORY_v1.4.29.md` §5 |
| CX1 | Theorem P for drifting worlds | §3, §7 | OPEN | CX1 | `theory/INTERNAL_MODEL.md` §4 (partial bridge) |

Lemma B3 (opposite effects of shared and private drift) is CLAIM_MAP C1, Lemma B2 (the spectrum map) is the rows of `reference/THEORY_v1.4.29.md` §2.2, and the empirical claims of §4–§6 are CLAIM_MAP N13, J6, J9, J15, J16, N27, N51, N52 and K4.
