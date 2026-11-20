# A Theory of Adaptive Organization

*Chad Mitchell ([@torusflow](https://x.com/torusflow)). Public working draft, CC0. Not peer reviewed; the new math is not yet independently reviewed.*

Anything that must stay alive in a changing world has to act before the world arrives, and that judgment has a price: memory to hold, errors and lateness to absorb, information to buy and share. **The claim is that one cost under the second law sets how adaptive systems should be built at every scale: layered, with the layers at the world's time scales.** One layer for each separated time scale the world changes on that the stakes can pay for, each with a memory set by that scale and the sensing noise.

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

$$
\min_{\mathcal D}\; \kappa\, I_{\text{mem}} + h\,K \;+\; w\,\mathbb E[\ell_{\mathcal D}] \;+\; A(\mathcal D) + L(\mathcal D) \quad \text{subject to}\quad P(\text{ruin}) \le \varepsilon_r
$$

Choose the design (layers, what each tracks, how it senses, what it shares) that makes holding memory, being wrong or late, and acquiring and sharing information cheapest without going broke. The world is a measured input.

**What follows** (proved in a model; the layer results are linear-Gaussian):
- One time scale needs one layer, even a self-similar random walk; J separated time scales need J layers once stakes outweigh upkeep.
- In every world, layers never fall as stakes rise relative to upkeep.
- A shared layer forms once enough members face a common driver; cheap lookup dissolves layers that only hold facts.
- Lateness caps how far one tracker reaches, so large systems federate.
- Survival is free above a buffer and decides the design below it. The buffer a unit needs grows as shock × τ^H, with H = ½ (√time to fix) for a random-walk error, so faster correction raises the shock it survives.
- At the optimum a tracker spends α − 1 on looking for every 1 it loses to being wrong, in any currency: written in a system's own units the equation is the same at every scale, though not with the same numbers.

- Whether to centralize is an output of the same cost: a shared level pays above a group size, lateness caps its reach, and parts merge when the gain over competing exceeds the cost of linking; free-riding parties capture only about half the pooling gain (proved in a toy, open in general).

![Illustrative phase diagram](theory/meq_checks/phase.png)

*One picture, in one made-up model world:* the best design on dimensionless axes (stakes over upkeep, latency over the fast time scale), with dotted contours of a measurable, currency-free share of cost. No real system is placed on it.

**How it dies.** Measure strongly selected systems' worlds and costs. If, at two or more scales, their layers sit away from the minimum (and a named rival fits better), or a system needs a cost the equation cannot book, the hypothesis is dead. A wrong picture of the world only means re-measuring. The bet is untested, not refuted: no field test has yet measured its quantities validly, so every result so far is "passed / failed on proxy". The parts are known and credited; the claim is new. Open: what happens when a system and the world it reshapes co-adapt as coupled levels.

**[`THEORY.md`](THEORY.md) is the one canonical statement of the theory (v2.3 draft, 19 November 2026, America/New_York).** Claim statuses: `measurement/CLAIM_MAP_v2.md` (v2.52). Where the work stands: [`STATUS.md`](STATUS.md).

```
THEORY.md         The theory, v2.3 draft (start here; §5 the theorem, §7 uses, §8 tests)
theory/           Derivations and code checks (MASTER_EQUATION.md, LAYERS.md)
measurement/      Validity gates and one status per claim
tests/, reviews/  Preregistered tests and reviews
reference/        Earlier versions and the changelog
```

AI agents helped draft, compute and review these files under the author's direction. License: [CC0 1.0](LICENSE.md).
