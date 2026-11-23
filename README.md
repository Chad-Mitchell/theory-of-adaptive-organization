# A Theory of Adaptive Organization

*Chad Mitchell ([@torusflow](https://x.com/torusflow)). Public working draft, CC0. Not peer reviewed.*

A one-page account is in [`ONE_PAGER.md`](ONE_PAGER.md).

Thermodynamics tells an engineer two things about any engine: the best it could possibly do, and how far a real one falls short. This theory aims to do the same for adaptive systems: cells, colonies, brains, teams, firms, AI and robot systems, anything that must act before its world arrives. Its object is the cost of judgment: the heat a system spends remembering its world, plus the stake on being wrong, under a cap on the chance of ruin. In worked classes, minimizing that cost yields the best design: how many layers, what to share, where a boundary is enough, when a shock should strengthen a system rather than harm it. If the hypothesis below holds, any adaptive system can be measured against its minimum, and the gap says where it wastes and what would close it.

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

The theory has two parts. Part 1 is mathematics: the cost, a heat floor no design can beat inside the classes where it is proved, and the designs that reach the minimum inside named classes. Those hold by proof. Part 2 is the hypothesis about nature, and only Part 2 can miss a measurement. No real system has yet been shown to sit at the minimum. The same argument in full, with every number, is [`CORE.md`](CORE.md).

![One cost of judgment, in time and in space](figures/master_curve.png)

*One cost of judgment, in time and in space* (`figures/master_curve.png`; every claim and its source is in `figures/master_curve.md`). In the worked class every time scale lands on one curve in the stake ratio \(x=wv/(kT\,a)\): below \(x=1\) no memory pays, and above it a memory pays and its error falls as \(v/\sqrt{x}\). The space panels are holographic memory and the field and boundary results. Where real systems sit on the curve is the hypothesis.

## The cost

$$J = \dot Q + w\,\mathbb{E}[\ell] \qquad\text{subject to}\qquad P(\text{ruin})\le\varepsilon.$$

\(\dot Q\) is the heat the memory's bath gives off, \(w\) is the stake that converts loss into that currency, \(\mathbb{E}[\ell]\) is the expected loss of the decision, and \(\varepsilon\) caps the chance of ruin. The cost is defined for any adaptive system: each has a memory that dissipates, a stake on error, and a chance of ruin. Physics sets the floor on the first term: for bipartite chains and additive-noise diffusions the heat is at least \(kT\) times the rate at which the memory learns its world (Horowitz and Esposito 2014, doi 10.1103/PhysRevX.4.031015). Temperature does not set the stake, and the stake and the ruin cap stay assumptions. [`THEORY.md`](THEORY.md) is the canonical statement of the theory (v2.9 draft) and still prints an older five-term sum; adopting this display there is open work T40 ([`OPEN_WORK.md`](OPEN_WORK.md)), and the relation between the two is set out in `CORE.md` §1.

## What holds in general

These need no Gaussian or linear step (`theory/REPRESENTATION.md`, `theory/GENERALITY_2026-11-22.md`; exact conditions in `CORE.md` §2).

1. **The cost is a priced sum.** For any system meeting axioms A1–A7 on at least three essential coordinates, a continuous cost that represents its preferences is an additive price sum, and its memory coordinate is finite-law Shannon information (Theorem R1). R1 does not choose which coordinates appear.
2. **Memory costs heat.** A bipartite memory's bath gives off at least \(kT\) times the information flow of its own transitions, for bipartite chains and for additive-noise diffusions.
3. **Higher stakes buy more judgment.** On a fixed menu with the ruin cap slack, judgment spend does not fall as the stake rises.
4. **A boundary can be enough.** A joint law that factorizes across a cut screens the two sides, so a decision scored on the outside needs only the blanket.
5. **Convex payoffs gain from shocks, and caps can reverse it.**
6. **Zero-gain control drops out.** A control that enters only as an additive drift, at zero gain, leaves the world as it was.

## What the minimum buys

In the worked class (equilibrium Ornstein–Uhlenbeck signals or the two-state telegraph, a memory that does not move its signal, mean-square or Hamming loss) the minimum is computed in closed form (`theory/GENERAL_FORM_PHYSICS_2026-11-22.md`). Each result below is proved in its named model; that all five are one minimum of one cost is the synthesis the hypothesis asserts (`theory/ACTING_LOOP_2026-11-22.md` §8).

- **When memory pays.** Below the stake ratio \(x=1\) the cheapest design is blind. Above it the minimum cost is \(2\sqrt{kT\,a\,v\,w}-kT\,a\). The same threshold appears for discrete memories as "the first bit must pay" (`THEORY.md` CT4, `core/bridge_2026-11-21/FLOOR.md`).
- **Layers.** On a ladder of time scales, each scale past the threshold gets a store, and the count follows from the stake with no free constant per layer.
- **Holographic memory.** When a decision combines many items, one shared memory is cheaper than separate copies; when each item is read on its own, it is not (`theory/HOLOGRAPHIC_MEMORY_2026-11-22.md`).
- **Boundary.** For a decision outside a region, the boundary is sufficient and the interior adds nothing (`theory/BOUNDARY_SUFFICIENCY_2026-11-22.md`).
- **Rebuild and gaining from shocks.** The cost predicts when a system gains from disorder and when it does not. Under the ruin cap, replacing identical units can lower the long-run cost. In the linear-Gaussian class, with the ruin cap slack, a spread of volatility lowers expected cost if the system can redesign per regime. In an open-loop probe class the minimized sign cost can fall as volatility rises; at the scored point a spread of volatility raises that same cost. A general gain from closing the loop is an open conjecture (`theory/antifragility_checks/RESULTS.md`, `theory/ROBUSTNESS.md`, `theory/ACTING_MEMORY_2026-11-22.md`, `theory/ANTIFRAGILITY_CONJECTURE_2026-11-23.md`).
- **Acting.** Closed-loop control beats sensing alone when the channel is free. Once its heat and probe are charged, it loses at unit stake and wins by a small margin at stake 4 (`theory/ACTING_LOOP_2026-11-22.md`).

## Where this is going

1. **The cost is universal.** It is defined for any adaptive system.
2. **The method is general.** Write the cost, find its minimum, read off the design. No single closed-form design exists for every system, any more than thermodynamics has one engine for every job; each class gets its own exact answer, and a team's minimized cost folds exactly into its parent's problem, so the method nests (`THEORY.md` CT34).
3. **The floor spreads class by class.** The heat floor is proved for bipartite chains and additive-noise diffusions. Beyond those classes it is open. A draft awaiting re-confirmation gives an information-flow bound for linear drifting worlds (`theory/THEOREM_P_DRIFT.md`). Next in the work list are the continuous-information A6 extension (T48), non-Gaussian closed forms (T49), and the open Kalman–Bucy factor-of-2 question. The goal is a floor for every adaptive system.
4. **Selection finds the minimum where no closed form exists.** A search scored by the cost, natural selection or an evolutionary algorithm, settles near the minimum; near a quadratic minimum the predicted excess is \(d/(2\beta)\), which shrinks as selection strengthens (`core/bridge_2026-11-21/BRIDGE.md`). That holds only under three conditions, each with a counterexample in our own runs: strong selection, a minimum the search can reach, and a cost that includes everything that matters (`CORE.md` §5).
5. **Antifragility.** The cost predicts when a system gains from disorder and when it does not (`theory/ANTIFRAGILITY_CONJECTURE_2026-11-23.md`). The option and learning routes are proved in their own classes; a general gain from closing the loop is an open theorem.
6. **The real-world test.** Qualify a strongly selected system, preregister the prediction, and measure.

## Where the evidence stands

In simulations of our own worlds, selection converged to the predicted minimum in clean worlds and stalled where the world added an obstacle such as a valley, a ruin gate, or store noise; several locked in-model predictions also missed (`CORE.md` §5, `measurement/CLAIM_MAP_v2.md`). No real-data result yet counts as a test: every scored field row is NOT A TEST or INCONCLUSIVE, because no system has been qualified under THEORY §3 ([`STATUS.md`](STATUS.md)).

## How a miss is read

"Strongly selected" is the definition in [THEORY §3](THEORY.md). Before measuring, a class fixes a cost-to-fitness map, a population proxy, a band that excludes a named rival, and a redesign time with at least ten of those times in the same world. A design outside the band fixed in advance is a puzzle for that class, with its diagnosis and next test written beforehand. A field result with no recorded qualification check is not a test of the hypothesis.

## What remains

Math first, then the real-world test (`OPEN_WORK.md` §3): the continuous A6 extension (T48), non-Gaussian closed forms (T49), and the decisive test on one qualified system. Smaller open items and two written puzzles are listed in `CORE.md` §7.

## Where to read

Claim statuses: `measurement/CLAIM_MAP_v2.md` (v2.88). Where the work stands: [`STATUS.md`](STATUS.md). What is still open: [`OPEN_WORK.md`](OPEN_WORK.md). Earlier front pages are in `history/`, most recently `history/2026-11-22_README_before_synthesis.md`.

```
THEORY.md         The theory, v2.9 draft (canonical statement; §3 is still the five-term cost)
CORE.md           The same argument in full, with every number
theory/           The heat, the five yields, and the checks
measurement/      One status per claim
figures/          master_curve.png, the master picture; derivation_map.png and face.png, earlier views
```

AI agents helped draft, compute, and review these files under the author's direction. License: [CC0 1.0](LICENSE.md).
