# The core: the cost of judgment on one page

*Sunday 22 November 2026. Rewritten from the one-pager that stood at `65f8703`. The previous text is `history/2026-11-22_CORE_before_front.md`. The map of this page is [`figures/derivation_map.png`](figures/derivation_map.png).*

The theory has two parts, and they are different kinds of claim. **Part 1 is mathematics:** limits any memory of a world must pay, and the shape of the cheapest design inside a named class. Those limits hold by proof. **Part 2 is a hypothesis about nature:** that strongly selected systems come close to them. Only Part 2 can fail an experiment.

[`THEORY.md`](THEORY.md) is the canonical statement (v2.9 draft). It still displays the five-term priced sum. The physics cost below is the derived cost inside one class. Putting that display into THEORY §3 is open work, T40 in [`OPEN_WORK.md`](OPEN_WORK.md). It is not done. Where this page and `THEORY.md` disagree, `THEORY.md` governs.

## 1. The limit

In steady state the bath of a learning subsystem gives off heat at least equal to temperature times the rate at which the memory learns the world it acts on (Horowitz and Esposito 2014). The inequality is **KNOWN**:

$$\dot Q \ge kT \times \text{(learning rate)}.$$

It bounds a heat. It does not choose a stake, a linking price, or a ruin cap.

Inside the class below, the cost of judgment is that heat plus a stake on the decision loss. The ruin cap stays outside the sum:

$$J = \dot Q + w\,\mathbb{E}[\ell] \qquad\text{subject to}\qquad P(\text{ruin})\le\varepsilon.$$

\(w\) converts the loss into the same currency as the heat. Temperature does not set \(w\).

**The class.** An exogenous equilibrium Ornstein–Uhlenbeck signal, independent signals of that kind, or the two-state telegraph. The memory does not move the signal. The loss is the mean squared error of an action of the current memory, or Hamming error on the telegraph. A signal's own bath pays nothing in these models. Proofs: `theory/INFO_PHYSICS_ATTAINABILITY.md`, `theory/INFO_PHYSICS_GENERAL.md`, consolidated in `theory/GENERAL_FORM_PHYSICS_2026-11-22.md`. The dated correction to the earlier spring, scored on the raw coordinate rather than the decision, is `theory/INFO_PHYSICS_CORRECTION_2026-11-22.md`.

**PROVED in that class.**

- One OU signal, rate \(a\), variance \(v\), decision error \(\varepsilon\): the heat infimum is \(kT\,a(v-\varepsilon)/\varepsilon\). A fast linear memory approaches it at finite heat, in the limit of a diverging rate.
- Above the stake \(kT a/v\) the minimizing cost is \(2\sqrt{kT\,a\,v\,w}-kT\,a\). At or below that stake the design is blind: heat \(0\), error \(v\), cost \(wv\).
- Equal-variance OU modes on a geometric ladder, each scored on its own: once the slowest pays, the number tracked is \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\). There is no free constant per layer.
- The error in the sum of the modes: one rank-one memory, gains \(1/(a_k+\mu)\), heat \(kT\mu\). Separate memories of \(K\) identical modes cost \(K\) times that heat.
- The telegraph: the flow is \(\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\) nats per unit time at every temperature. The heat infimum is \(kT\) times that flow, approached as the memory rates diverge.

## 2. The hypothesis

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

"Strongly selected" is the operational definition in THEORY §3. No system has been shown to qualify. The sentence is the sentence in THEORY §3. It is not rewritten here.

## 3. The shape, and the older sum

If offspring falls in each coordinate of a chosen vector of bads, every maximizer of long-run growth is Pareto in that vector (Lemma LY, **PROVED** in-model under H1–H3, `theory/GENERAL_FORM.md`). The lemma does not choose the vector. Occupation of the front is not proved. Persistence alone, with no growth ranking, does not rank the designs that survive.

The five-term sum still printed in THEORY §3,

$$\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L \qquad\text{subject to}\qquad P(\text{ruin})\le\varepsilon,$$

is the special case in which the front is ranked by risk-neutral expected currency, the prices are linear and nonnegative, and ruin is a half-space cap. That relation is the comparison with the ideal-gas law in `theory/GENERAL_FORM.md`: extra assumptions collapse a more general relation to a linear formula. It is not a claim that judgment is a gas. Memory held, information bought, error, attention, and ruin risk are not a derived list. Attention, as a derived bad, does not follow.

| Term of the five-term sum | Inside the proved class |
|---|---|
| \(\kappa I_{\mathrm{mem}}\) | Replaced by the bath heat \(\dot Q\). Floor: \(kT\) times the learning rate. |
| \(hK\) | Not in the floor. Separate baths add their heats. A constant \(h\) still on the books is excess. |
| \(w\,\mathbb{E}[\ell]\) | Survives. \(w\) stays assumed. |
| \(A\), \(L\), the ruin cap | Stay assumed. A continuous coupling's read is inside \(\dot Q\). \(L\) and the cap stay outside \(J\). |

The theorems in THEORY that minimize the five-term sum are theorems about that sum. Adopting §9 of `theory/GENERAL_FORM_PHYSICS_2026-11-22.md` would not re-prove them under this \(J\). That adoption is T40.

## 4. A cut, and where a layer goes

The floor depends on the memory only through the conditional law of the world given the memory (**PROVED** in the class). Equilibrium coordinates that leave the conditional unchanged are free. They are not a bulk stored on a boundary.

When the decision names a cut, the minimum heat scales with that cut and does not grow with the depth behind it. In the worked square lattice the cost is about \(13.61\) per cut site against a lower bound of \(13\). That is the cost equation on the sites the decision names (**PROVED**). The same sentence, read as a holographic encoding, is a **METAPHOR**: the name adds no prediction the cost equation did not already make. When the decision charges every site, the heat scales with the volume. `theory/HOLOGRAPHIC_2026-11-22.md`.

[`figures/face.png`](figures/face.png) is the layer-placement output of the cost: each time scale is drawn at the stakes a local layer can win over its upkeep, and the stakes one shared layer can win over its upkeep, and the marker is the cheapest of local, shared, both, or neither.

## 5. Open

- Signals other than an exogenous equilibrium OU process or the telegraph, and losses other than the mean square of a current action or Hamming error on the telegraph.
- A memory that changes its world.
- Deriving the stake, attention, linking, or the ruin cap. They are absent from the heat bound. They stay assumptions.
- Whether a qualifying system sits near the floor.
- Holographic memory: [draft PR #186](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/186), under fixes. This page claims no result from it.
- T40, the edit to THEORY §3.

## 6. How it could fail

The full rule is THEORY §3, and the same essentials are on the front page. A class qualifies only with a preregistered cost-to-fitness map, a population proxy, a band selection can resolve that excludes a named rival, and a redesign time with at least ten of them in the same world. Cities, nation-states, global economies, and the biosphere do not qualify until a proxy for them is preregistered. Before measuring, the class fixes the cost terms, the world's spectrum and noise, and the prices. Misses outside the preregistered band refute the hypothesis for that class once they pass a binomial allowance fixed in advance; for a small class the allowance can be one miss. Two classes at different scales refute it across scales. A cost the list omitted is a miss, and so is a design that does not move with a measured change in its inputs, unless the gap that remains is inside the redesign band at the lower bound of the preregistered redesign cost (CT41). The bet is untested. A field result with no recorded qualification check is not a test of the hypothesis.

## Status words

**PROVED** means proved inside the stated model, which says nothing by itself about nature. **KNOWN** means published and credited. **METAPHOR** means a reading that adds no prediction the cost equation does not already make. **HYPOTHESIS** means a claim about the world. On the derivation map the same claim is colored **CONJECTURE**. **OPEN** means not derived or not measured.

Omissions from this page are compressions. The layer-count, lifetime, and local-versus-shared theorems minimize the five-term sum; they remain in `THEORY.md` and in the frozen one-pager. They are not restated as theorems about the heat.
