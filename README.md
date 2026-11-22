# A Theory of Adaptive Organization

*Chad Mitchell ([@torusflow](https://x.com/torusflow)). Public working draft, CC0. Not peer reviewed.*

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

Until a qualifying system is measured, read that sentence as a principle: one cost of judgment, and the design is what the cost selects. Inside the Gaussian and linear class the mathematical core is effectively complete. Evidence from real systems is thin, and it is open. The one-page statement is [`CORE.md`](CORE.md).

![One cost, five yields](figures/derivation_map.png)

*One cost, five yields* (`figures/derivation_map.png`, from `figures/derivation_map.py`). The cost is at the top. The five rows are what its minimum spends it on, each proved in its own class. The join of the five is a synthesis. **IN REVIEW** is [PR #203](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/203) and is not merged. **OPEN** is not derived, or not yet measured.

## The cost

In the class where the learning rate has been worked out, the cost of judgment is the heat of the memory's bath plus a stake on the decision loss. The chance of ruin is a cap beside the sum.

$$J = \dot Q + w\,\mathbb{E}[\ell] \qquad\text{subject to}\qquad P(\text{ruin})\le\varepsilon.$$

When the prices are linear, that cost is the five-term sum still printed as the canonical equation:

$$\kappa I_{\mathrm{mem}} + hK + w\,\mathbb{E}[\ell] + A + L.$$

\(\kappa I_{\mathrm{mem}}\) is the bath heat. Its floor is \(kT\) times the learning rate (Horowitz and Esposito 2014, doi 10.1103/PhysRevX.4.031015, checked on Crossref 22 November 2026). \(hK\) sits outside that floor. \(w\,\mathbb{E}[\ell]\) survives, and temperature does not set the stake \(w\). A continuous sensor's read is already inside the heat; a separate read price \(A\), the link price \(L\), and the ruin cap stay assumed.

[`THEORY.md`](THEORY.md) is the one canonical statement of the theory (v2.9 draft). Where this page and that file disagree, that file governs. Adopting the physics display into §3 is open work, T40, proposed in `theory/GENERAL_FORM_PHYSICS_2026-11-22.md` §9.

The worked class is an exogenous equilibrium Ornstein–Uhlenbeck signal, independent signals of that kind, or the two-state telegraph. The memory does not move the signal. The loss is a mean square, or Hamming error on the telegraph. Inside that class the floor on one OU signal is \(kT\,a(v-\varepsilon)/\varepsilon\), approached in a limit; the minimizing cost above the blind stake is \(2\sqrt{kT\,a\,v\,w}-kT\,a\); a geometric ladder tracks \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\) modes, with no free constant per layer; a sum of modes is carried by one rank-one memory; the telegraph heat approaches \(kT\) times its information flow.

## Five yields of one minimum

Each line below is proved in the class named with it. The sentence that the five are one minimum is a synthesis. `theory/ACTING_LOOP_2026-11-22.md` §8 states that limit.

**Layers, along time.** One real time scale needs one store, or none when the stake is small. On the geometric ladder the count is the formula above. [`figures/face.png`](figures/face.png) is the placement: for each time scale, local, shared, both, or neither.

**Spread, across items.** One memory carries a sum. \(K\) separate memories of \(K\) identical modes cost \(K\) times the heat at the same error. A shared memory costs less when the decision is a combination of items, and it ties or costs more when every item is read on its own (`theory/HOLOGRAPHIC_MEMORY_2026-11-22.md`). The heat floor on a per-site error scales with the volume. Holding a named cut scales with the cut (`theory/HOLOGRAPHIC_2026-11-22.md`). The name "holographic" adds no prediction those equations do not already make.

**Boundary.** For a decision outside a region of an equilibrium Gaussian field, the conditional law given the region and the Markov blanket equals the law given the blanket. The interior is not sufficient for that decision. The matching blanket channel costs at most the Schur trace more than the channel it matches (`theory/BOUNDARY_SUFFICIENCY_2026-11-22.md`).

**Rebuild.** Under the ruin cap, replacement of identical capacity-limited units can lower the long-run cost: rate 1 costs 15.473978 with ruin probability 0.020940, against an inadmissible zero-shock point at cost 16 (`theory/antifragility_checks/RESULTS.md`). The heterogeneous arm's grid minimum stays at no shock. That comparison is a puzzle at this cap. Heat is proportional to precision, and the admissible grid kept the more precise units.

**Acting.** With the channel unpriced, closed-loop regulation is cheaper than sensing alone by the factor 0.171572875254 at unit stake and unit drift. With the heat and the probe charged, the gap is negative at every fraction at stake 1, and equals 0.033889928154 at stake 4. Feedback shrinks the information stock and leaves the learning-rate heat fixed (`theory/ACTING_LOOP_2026-11-22.md`). A probe can make the minimized cost fall as volatility rises. The drop is the price of a fraction falling as \(1/\theta\) (`theory/ACTING_MEMORY_2026-11-22.md`).

## Options, and the learning heat

A payoff convex in a shock gains from a spread of that shock. Antifragility is that convexity. Optionality is a convex payoff bought with a capped premium. Both are standard mathematics (Taleb and Douady 2013, doi 10.1080/14697688.2013.800219, checked on Crossref 22 November 2026), and `theory/ROBUSTNESS.md` already uses that reading. A search of this repository finds the two routes written side by side in the acting-memory note, and finds no theorem that makes them one object. The synthesis is that the learning heat and the option sit under this one cost. That sentence is the hypothesis in another shape. It is not a proof.

## In review

The acting derivation is in review: [PR #203](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/203), branch `cursor/acting-derivation-2d99`, head `a79d7b6`. Theorem R1′ is a representation theorem. The step proved on that branch is the \(b=0\) reduction, which returns the five-term cost. The risky prediction was met by one grid step. A stationary solve gives continuous gains 0.23 against 0. The gate was underpowered, so meeting it is weak evidence. This page does not adopt that derivation, and it does not treat the pull request as merged.

## What remains

- The non-Gaussian case, and a loss other than the mean square or the telegraph mismatch. A memory that changes the world it tracks.
- A real-data test: a system qualified before the measurement, then scored against the cost. No such test is on this page.
- The fractal draft, [PR #192](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/192). This page uses no result from it.
- Adopting the acting derivation into `THEORY.md` once #203 has been reviewed. The master equation is unchanged.
- The integer \(5\%\) radius. It is 2 at both \(\tau=1/2\) and \(\tau=1\), ratio 1, because both crossings of the level 0.05 fall in the bin \((1,2)\). A longer path, the next test the preregistration named, returned 2 and 2. The smooth crossing is a separate statistic, ratio 2.067863694520, inside \([1.7,2.3]\).
- \(J^*(8)\) against 5. The grid value is 4.998066177768. The number 5 is the heat plus the sign loss at the frozen fraction, above a floor of 4.966383544211. The crossing is near \(\theta=7.5267\). The next test is a new preregistration scored against that floor.

## How a miss is read

"Strongly selected" is the definition in [THEORY §3](THEORY.md). No system has been shown to qualify. Before measuring, a class fixes a cost-to-fitness map, a population proxy, a band that excludes a named rival, and a redesign time with at least ten of those times in the same world. Cities, nation-states, global economies, and the biosphere wait for a proxy. A design outside the band fixed in advance is a puzzle for that class. The diagnosis and the next test are written down beforehand. A field result with no recorded qualification check is not a test of the hypothesis. Counting layers is the draft method in [`measurement/LAYER_COUNT_RULE.md`](measurement/LAYER_COUNT_RULE.md).

## Where to read

Claim statuses: `measurement/CLAIM_MAP_v2.md` (v2.88). Where the work stands: [`STATUS.md`](STATUS.md). What is still open: [`OPEN_WORK.md`](OPEN_WORK.md). The previous front page and the previous one-pager are `history/2026-11-22_README_before_front.md` and `history/2026-11-22_CORE_before_front.md`.

```
THEORY.md         The theory, v2.9 draft (canonical statement; §3 is still the five-term cost)
CORE.md           The same argument on one page
theory/           The heat, the five yields, and the checks
measurement/      One status per claim
figures/          derivation_map.png, the one cost; face.png, the layer placement
```

AI agents helped draft, compute, and review these files under the author's direction. License: [CC0 1.0](LICENSE.md).
