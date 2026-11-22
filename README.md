# A Theory of Adaptive Organization

*Chad Mitchell ([@torusflow](https://x.com/torusflow)). Public working draft, CC0. Not peer reviewed.*

A system that must act before its world arrives pays to remember. The limits on that cost are mathematics. That strongly selected systems come close to those limits is a hypothesis. The one-page statement is [`CORE.md`](CORE.md).

![How the derivation sits](figures/derivation_map.png)

*How the derivation sits* (`figures/derivation_map.png`, from `figures/derivation_map.py`). Read top to bottom. **KNOWN** is published and credited. **PROVED** means proved inside the class named with it. **CONJECTURE** is the hypothesis about nature. **OPEN** is not derived, or not yet measured.

## Limits

In steady state, the bath that holds a memory gives off heat at least equal to temperature times the rate at which that memory learns the world it acts on:

$$\dot Q \ge kT \times \text{(learning rate)}.$$

That inequality is Horowitz and Esposito 2014. It is **KNOWN**. It bounds a heat. It does not list the terms of a cost.

Inside the class where that rate has been worked out, the cost of judgment is that heat plus a stake on the decision loss. A cap on the chance of ruin stands beside the sum. It is not a term inside the sum.

$$J = \dot Q + w\,\mathbb{E}[\ell] \qquad\text{subject to}\qquad P(\text{ruin})\le\varepsilon.$$

The stake \(w\) is supplied. Temperature does not set it.

The floors below are **PROVED** in one class, and not beyond it. The signal is an exogenous equilibrium Ornstein–Uhlenbeck process (a stationary scalar Gauss–Markov diffusion), or independent signals of that kind, or a two-state telegraph. The memory does not move the signal. The loss is the mean squared error of an action of the current memory, or, on the telegraph, the fraction of mismatches. Sources: `theory/INFO_PHYSICS.md`, `theory/INFO_PHYSICS_ATTAINABILITY.md`, `theory/INFO_PHYSICS_GENERAL.md`, `theory/GENERAL_FORM_PHYSICS_2026-11-22.md`. A lower bound is not, by itself, every term of a cost.

- **One OU signal**, rate \(a\), variance \(v\), decision error \(\varepsilon\). The heat is at least \(kT\,a(v-\varepsilon)/\varepsilon\). A fast linear memory approaches that floor while the heat stays finite. The approach is a limit of a diverging internal rate.
- **The frontier** of that floor plus the stake. The design is blind when \(w\le kT a/v\): heat zero, error the signal variance, cost \(wv\). Above that stake the cost is \(2\sqrt{kT\,a\,v\,w}-kT\,a\).
- **How many modes are tracked.** On a geometric ladder of equal-variance OU modes, each scored on its own, once the slowest pays and until the ladder runs out, the count is \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\). No constant per layer is free to set. Multiplying the stake by the ladder ratio \(\rho\) adds one mode.
- **One memory for a sum.** When the loss is the error in the sum of the modes, one memory, with weight \(1/(a_k+\mu)\) on mode \(k\), approaches the floor. The channel is rank one. \(K\) separate memories of \(K\) identical modes cost exactly \(K\) times the heat at the same error.
- **The telegraph.** At Hamming error \(\varepsilon\) the information flow is \(\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\) nats per unit time, at every temperature. The heat is at least \(kT\) times that flow, and a fast memory approaches the bound.

## Hypothesis

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

The limits above need no experiment. This sentence does. "Strongly selected" is the five-part definition in [THEORY §3](THEORY.md). No system has yet been shown to qualify.

## What follows

**The shape.** If offspring falls in each coordinate of a chosen vector of bads, every maximizer of long-run growth is Pareto in that vector (Lemma LY, **PROVED** in-model, `theory/GENERAL_FORM.md`). The lemma does not choose the vector. It is not proved that one copying process occupies the whole front. The additive sum

$$\kappa\, I_{\mathrm{mem}} + hK + w\,\mathbb{E}[\ell] + A + L$$

is the special case in which that front is ranked by risk-neutral expected currency, the prices are linear, and ruin is a half-space cap. The comparison in that note is with the ideal-gas law: a named list of extra assumptions collapses a more general relation to a linear formula. It is not a claim that judgment is a gas. Memory, information, error, attention, and ruin are not a derived list of bads. Attention is not a derived bad.

**What the older terms become, inside the proved class** (`theory/GENERAL_FORM_PHYSICS_2026-11-22.md` §7).

| Older term | Inside the proved class |
|---|---|
| \(\kappa I_{\mathrm{mem}}\) | Replaced by the memory-bath heat. The floor on that heat is \(kT\) times the learning rate. |
| \(hK\) | Not a term of the floor. A constant per layer, if the books still carry one, sits above the heat. |
| \(w\,\mathbb{E}[\ell]\) | Survives. The stake \(w\) stays assumed. |
| \(A\) | Stays assumed as a separate summand. For a sensor coupled continuously to its bath, the read is already inside the heat. |
| \(L\) | Stays assumed, and stays outside this \(J\). |
| \(P(\mathrm{ruin})\le\varepsilon\) | Stays outside the sum. Stays assumed. |

[`THEORY.md`](THEORY.md) is the one canonical statement of the theory (v2.9 draft). It still states the five-term sum, and the theorems there minimize that sum. They are not re-proved for the heat. Adopting the physics display into THEORY §3 is open work, item T40 in [`OPEN_WORK.md`](OPEN_WORK.md). The proposed text is `theory/GENERAL_FORM_PHYSICS_2026-11-22.md` §9. It is not applied on this page.

**A cut.** At a fixed decision error the heat floor depends on the memory only through the conditional law of the world given the memory. Equilibrium coordinates that leave that conditional unchanged do not raise the floor. That is **PROVED** in the class. When the decision names a cut rather than every site, the minimum heat scales with the cut and does not grow with the depth behind it. In the worked square lattice that cost is about \(13.61\) per cut site, against a lower bound of \(13\). This is the cost equation on the sites the decision names (**PROVED**). Calling the same fact a holographic encoding adds no prediction the equation did not already make (**METAPHOR**). When the decision is every site, the heat scales with the volume. Record: `theory/HOLOGRAPHIC_2026-11-22.md`.

**Where a layer goes.** [`figures/face.png`](figures/face.png) is the layer-placement output of the cost: for each time scale, whether the cheapest design is a local store, a shared store, both, or neither.

## Open

- A signal that is not an equilibrium Ornstein–Uhlenbeck process and not the telegraph, and a loss that is not the mean square or the telegraph's Hamming mismatch.
- A memory that changes the world it tracks.
- The stake, attention, linking, and the ruin cap. They are not derived. They remain assumptions. The physics did not come close enough to call them nearly finished.
- Whether a real system that qualifies sits near the floor. Nothing on this page has measured that.
- Holographic memory, the question of when a shared store is the design the cost selects: [draft PR #186](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/186), under fixes. No result from that draft is used here.
- Writing this cost into THEORY §3. That is T40. It is not done.

## How it could fail

The full rule is [THEORY §3](THEORY.md). A class qualifies only when five things are fixed before any measurement: a cost-to-fitness map; a population proxy (cities, nation-states, global economies, and the biosphere stay out until a class-specific proxy exists); a band that selection can resolve and that excludes a named rival; and a redesign time, with the lineage in the same world for at least ten of those times. The closed list of cost terms, the world's spectrum and noise, and the prices are fixed before the comparison, and each is measured independently of the design it is used to predict.

A miss is a qualifying system's design outside the preregistered band around the minimum. Misses refute the hypothesis for that class once they exceed a binomial allowance fixed in advance from the class's preregistered coverage and its minimum number of systems. For a small class that allowance can be a single miss. Misses in two classes at different scales refute the hypothesis across scales. A needed cost that is not on the list is a miss. So is a design that does not move with a measured change in its inputs, unless the gap after the change sits inside the redesign band at the lower bound of the class's preregistered redesign cost (CT41, `theory/DYNAMICS.md` §2). A band exists only where adjustment is lumpy, and only if the redesign cost, the curvature, and the input process are preregistered before data. Re-measuring the world is allowed once, before the comparison.

The bet is untested. A field result with no recorded pre-test qualification check is not a test of the hypothesis. How a real system's layers are counted is the draft method in [`measurement/LAYER_COUNT_RULE.md`](measurement/LAYER_COUNT_RULE.md). A class still has to preregister that method before a test.

## Where to read

Claim statuses: `measurement/CLAIM_MAP_v2.md` (v2.88). Where the work stands: [`STATUS.md`](STATUS.md). What is still open: [`OPEN_WORK.md`](OPEN_WORK.md). The previous front page and the previous one-pager are `history/2026-11-22_README_before_front.md` and `history/2026-11-22_CORE_before_front.md`.

```
THEORY.md         The theory, v2.9 draft (canonical statement; §3 is still the five-term cost)
CORE.md           The same argument on one page
theory/           Physics notes, the general form, the holographic note, and the checks
measurement/      One status per claim
figures/          derivation_map.png, and face.png, the layer placement
```

AI agents helped draft, compute, and review these files under the author's direction. License: [CC0 1.0](LICENSE.md).
