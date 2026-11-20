# A Theory of Adaptive Organization

*Chad Mitchell ([@torusflow](https://x.com/torusflow)). Public working draft, CC0. Not peer reviewed; the new math is not yet independently reviewed.*

Anything that must stay alive in a changing world has to act before the world arrives, and that judgment has a price: memory to hold, errors and lateness to absorb, information to buy and share. **The claim is that one cost sets how adaptive systems should be built at every scale: in layers, one for each separated time scale of the world that the stakes can pay for, each tuned to its scale and the sensing noise.** Each layer runs a little faster than the scale it tracks, by an amount the sensing noise sets. Physics enters only as a floor under the prices, slack above the cell.

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

$$
\min_{\mathcal D}\; \kappa\, I_{\text{mem}} + h\,K \;+\; w\,\mathbb E[\ell_{\mathcal D}] \;+\; A(\mathcal D) + L(\mathcal D) \quad \text{subject to}\quad P(\text{ruin}) \le \varepsilon_r
$$

Choose the design (layers, what each tracks, how it senses, what it shares) that makes holding memory, being wrong or late, and acquiring and sharing information cheapest without going broke. The world is a measured input.

**What follows** (proved in a model; the layer results are linear-Gaussian):
- One real time scale needs one layer (or none, when stakes are small), even a self-similar random walk; J separated real time scales need J layers once stakes outweigh upkeep, each layer a little faster than its scale; a rhythm needs two layers by degree.
- With sensing fixed, layers never fall as stakes rise relative to upkeep, in any world. With reads chosen they can, because reads substitute for layers; what never falls is total judgment spend, whatever the world or design (a two-line proof).
- A shared layer forms once enough members face a common driver; cheap lookup dissolves layers that only hold facts.
- Lateness caps how far one tracker reaches, so large systems federate.
- Survival is free above a buffer and decides the design below it. The buffer a unit needs grows as shock × τ^H, with H = ½ (√time to fix) for a random-walk error, so faster correction raises the shock it survives.
- For a tracker with negligible read noise of a power-law world, the optimum spends α − 1 on looking for every 1 it loses to being wrong, in any currency (it fails with read noise or when the world has its own time scale, and when a ruin constraint binds the shares and price elasticities differ). In a system's own units the equation is the same problem at every scale, though not with the same numbers.

- Whether to centralize is an output of the same cost: a shared level pays above a group size, lateness caps its reach, and merging pays when the gain over competing exceeds the cost of linking (a definition of the comparison, not a theorem); free-riding parties capture only about half the pooling gain (proved in a toy). Shared-driver coupling is a potential game and converges; no general convergence theorem is true; what is open is which real couplings are potential games.

![One map for every adaptive system](figures/face.png)

*One map for every adaptive system* (`figures/face.png`): the best design (layers per unit, 0 to 6+, or federate) in one made-up model world with many time scales and read effort optimized, on dimensionless axes (stakes over upkeep, which is not size, and latency over the fast scale), with **hypothesized** positions from a bacterium to the biosphere (order-of-magnitude guesses, sources where they exist, `figures/face_placements.md`). The regions are computed from J and checked by `tools/test_face_regions.py`; the positions are not measurements. There is no size ceiling and no "not viable" region in this map: the older two-scale diagram `theory/meq_checks/phase.png` has both, as artifacts of two time scales and a fixed income.

**How it dies.** "Strongly selected" is defined operationally and preregistered (turnover that would displace a rival within the record, at least 10 redesign times in the same world). For each substrate class, fix before measuring a closed list of cost terms, the world's spectrum and noise, and the prices. One miss in a qualifying system, with the layers outside the preregistered band around the minimum, refutes the hypothesis for that class; misses in two classes at different scales refute it across scales; a needed cost not on the list is a miss. Re-measuring the world is allowed once, before the comparison, never after. The bet is untested, not refuted: no field test has yet measured its quantities validly, so every result so far is "passed / failed on proxy". The parts are known and credited; the claim is new. Open: what happens when a system and the world it reshapes co-adapt as coupled levels.

**[`THEORY.md`](THEORY.md) is the one canonical statement of the theory (v2.4 draft, 20 November 2026, America/New_York).** Claim statuses: `measurement/CLAIM_MAP_v2.md` (v2.53). Where the work stands: [`STATUS.md`](STATUS.md).

```
THEORY.md         The theory, v2.4 draft (start here; §5 the theorem, §7 uses, §8 tests)
theory/           Derivations and code checks (MASTER_EQUATION.md, LAYERS.md)
measurement/      Validity gates and one status per claim
tests/, reviews/  Preregistered tests and reviews
reference/        Earlier versions and the changelog
```

AI agents helped draft, compute and review these files under the author's direction. License: [CC0 1.0](LICENSE.md).
