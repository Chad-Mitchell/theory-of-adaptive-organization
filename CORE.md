# The core: the cost of judgment on one page

*Saturday 21 November 2026, afternoon ET (America/New_York). `main` is `d34df95`.*

*Status words and caveats: see the end of this page.*

The theory has two parts, and they are different kinds of claim. **Part 1 is mathematics:** limits that any system acting ahead of a world it does not control must obey, and the structure of the cheapest design. Proved limits hold by proof, like Shannon's limits, and need no experiment. Gaps without a derivation are marked **OPEN**. **Part 2 is a hypothesis about nature:** that strongly selected systems come close to those limits. Only Part 2 has odds.

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

**In five sentences.** A system that must act ahead of a world it does not control pays one cost of judgment — memory, layer upkeep, error (including lateness), reads and sharing — subject to a ruin cap. The limits on that cost are mathematics and need no experiment; that strongly selected systems come close to them is the hypothesis. A stack of layers is the cheapest design only when a layer cannot, or cannot afford to, reset the whole state (**PROVED** in that specialized model). A lumpy layer's expected lifetime is \(T^*=\sqrt{6k/(w\sigma^2)}\) (**KNOWN**, exact at zero discounting), so a lower re-form cost shortens it; that structures then behave more like swarms is a **HYPOTHESIS**. Fast-local / slow-shared tracking needs delay on the shared channel only, and a shared lump cheaper than \(N\) local ones (**PROVED** for a Brownian driver with fixed-period refreshes; **NUMERICAL** for Ornstein–Uhlenbeck).

## 1. The cost

A system that must act ahead of a world it does not control chooses its design \(\mathcal{D}\) (layers, what each tracks, how often it reads, what it shares) to minimize

$$J(\mathcal D)=\kappa I_{\text{mem}}+hK+w\,\mathbb E[\ell_{\mathcal D}]+A(\mathcal D)+L(\mathcal D)\quad\text{subject to}\quad P(\text{ruin})\le\varepsilon .$$

- \(\kappa I_{\text{mem}} + hK\): memory held at price \(\kappa\) per nat, plus upkeep \(h\) per layer (a tracking store, not an org-chart level).
- \(w\cdot\mathbb E[\ell]\): stake times expected loss at the moment of use; lateness counts as error.
- \(A\), \(L\): the cost of reading the world, and of linking, telling and lookup.
- \(P(\text{ruin})\le\varepsilon\): a reserve paying \(J\) must not hit zero more often than \(\varepsilon\). A hard cap, not a cost to average away.

The world is a measured input: its statistics, the read noise and the lead time. One currency per system. The equation is a definition, assembled from known parts (THEORY §3).

**Part 1, the limits.**

**The floor (S1, PROVED for the information terms in a stationary world the system does not affect; drifting and random-walk worlds are open, CX1).** Every design pays at least \(J_{\text{floor}}\), computed from the world's statistics and the prices alone: memory pays for the predictive information it holds (CT1, CT4), and reads pay for at least the sequential rate–distortion rate of the accuracy reached. A layer price \(h\) is not part of that floor: a memoryless read has \(K = 0\) and still carries information. Landauer floors the erasure part of \(\kappa\). Sagawa & Ueda 2009 floor the sum of measurement and erasure work, not a separate read price stacked on that floor. In a scalar Gauss–Markov world the information floor is reached exactly when memory or reads are free (**PROVED** at those edges; the edge results are **KNOWN**). On one such world (\(a = 0.9\), \(Q = 1\), lead 2), the best one-layer Kalman design on a 36-point price grid has efficiency \(J_{\text{floor}}/J = 0.9574\) (gap \(1 - J_{\text{floor}}/J = 4.26\%\); the design costs 4.45% more than the floor) at the worst point (\(\kappa = c = w = 1\), layer price left out of both sides; **NUMERICAL**). That is not a bound over worlds. Whether the true least cost equals the information floor when memory and reads are both priced, or sits strictly between the floor and this Kalman design, is **OPEN**.

**The frontier and efficiency (S2, S3, PROVED).** The world defines a price-free frontier of reachable (memory, reads, layers, accuracy). The frontier is a set, not a single number like capacity. Its dual \(J^*(p) = \inf\langle p, z\rangle\) equals \(-\sigma(-p)\), where \(\sigma\) is the support function of the frontier, and equals the operational least cost only when some minimizer has \(A = c\cdot r\) and \(L = 0\). Knowing \(J^*\) on the positive orthant recovers the free-disposal hull of the Pareto face, not the whole convex hull. **Technical efficiency** — how far resources could shrink and still give the same accuracy — needs no prices. For the input cost \(C = \kappa I + c\cdot r\), \(C_{\min}/C\) splits into technical \(\times\) allocative (Farrell 1957); that product is not true of \(J_{\text{floor}}/J\). A linear-cost minimizer at strictly positive prices has technical efficiency 1 on its feasible set. A binding ruin cap restricts that set and need not preserve convexity. A binding ruin cap can raise the information floor; no formula for that rise is derived (**OPEN**).

**Part 2 (HYPOTHESIS).** Strongly selected systems sit near the world's frontier (the technical half, which needs no prices) and at the point their prices select (the allocative half, which needs price ratios or only signs). "Strongly selected" is operational in THEORY §3. No system has yet been shown to qualify.

What is claimed as new is the package: one priced objective under a ruin cap, the world's frontier as its input, and a kill rule across scales (THEORY §10).

## 2. Why layers exist

No information argument forces a layer. A memoryless rule can still carry information, and S1's floor does not charge \(h\). A store pays upkeep \(h\). Whether it beats a memoryless rule is the comparison of that upkeep with the drop in the other terms. There is no numbered theorem in these words (the hold-or-fade results are CT4, CT9, CT11).

A stack is the cheapest design only when a layer cannot, or cannot afford to, reset the whole state (**PROVED** in that specialized model). One lumpy tracker is already optimal for a single process, including a fractal one (**PROVED**). For increment variance proportional to \(\tau^{2H}\) the refresh scales as \((k/(wC))^{1/(2H+1)}\); the square-root lifetime below is the Brownian case \(H=\tfrac12\). One layer beats two when a joint reset costs about as little as one part (**PROVED**). A joint reset that costs the sum of the part costs does not: the specialized stack is then never more expensive.

The existing layer-count converse is CT21, linear-Gaussian, squared-error, counted by degree. For finitely many real modes, layers are at most the world's predictive degree (L2). On a non-rational spectrum, \(E_K>E_\infty\) for every finite \(K\), and \(K^*\to\infty\) if also \(E_K\to E_\infty\) (L3; that limit is conditional). In Model S the fewest-stores floor remains the existing numerical \(E_K\); \(T^*\) does not compute \(E_K\). There is still no formula for "the fewest layers that reach accuracy \(D\) in this world." That floor stays **OPEN**.

## 3. How long a layer lasts

For a gap that drifts as Brownian motion with variance rate \(\sigma^2\), costs \(w\,x^2\) per unit time, and is reset at lump cost \(k\), the expected time between resets is

$$T^*=\sqrt{6k/(w\sigma^2)}.$$

This formula is **KNOWN** as an exact result at zero discounting (Chalkley 1997). Dixit 1991 is the approximation that case makes exact. It is the right refresh rule for a lumpy layer. A layer's lifetime grows as the square root of its re-forming cost: a cost 100 times lower gives layers that last 10 times shorter. If adjustment is smooth rather than lumpy, there is no discrete lifetime, only a decay time (CL19 (c)). If the gap mean-reverts on the scale of \(T^*\), the Brownian formula is quantitatively false (**NUMERICAL**: a check at \(T^*/\tau\approx 0.63\) missed by 137%).

In a specialized stack (each layer can reset only its own component; quadratic loss in the total error; equal stakes), the lifetimes stand in the exact ratio

$$T_i^*/T_j^*=\sqrt{(k_i/k_j)\,(\sigma_j^2/\sigma_i^2)}$$

(**PROVED** in that model). That is a spacing rule, not a universal geometric series: the ratios are set by the costs and the drifts, and they collapse or invert when those inputs do.

## 4. Local vs shared under delay

The same cost decides whether a fact is tracked locally or shared. The fast-local / slow-shared crossing needs latency on the shared channel only, and a shared lump cheaper than \(N\) local lumps (\(k_S<N k_L\)). It is **PROVED** for a Brownian common driver with fixed-period refreshes, and **NUMERICAL** for an Ornstein–Uhlenbeck driver. Under that same shared-only delay, the optimal barrier keeps the sign, and the variance rate where the two costs cross is the fixed-period crossing divided by 3. If local updates carry the same observation delay, the delay floors cancel. Which side is cheaper then does not depend on the drift variance, so speed does not flip the choice. \(\tau>\ell\) is not sufficient: at the prices in the checks, the OU crossing is about \(183\ell\), so shared still lost at \(\tau=40\ell\) and won at \(\tau=400\ell\).

The older nesting factor in the repository (at equal read quality, a shared layer's worth falls as \(e^{-2\ell/\tau}\)) is the Ornstein–Uhlenbeck companion of this result (CT28, CT34).

## 5. Every adaptive organization

The same cost is the theory's definition for systems that must act ahead of a changing world. THEORY §1 names cells, colonies, people, firms and cities. Firms are one class, not the point. The hypothesis is that *strongly selected* systems in a class that qualifies sit near the minimum, not that every organization already does. Cities, nation-states, global economies and the biosphere do not qualify until a class-specific population proxy is preregistered (THEORY §3).

When the cost \(k\) of re-forming a layer falls, \(T^*\) shrinks as \(\sqrt{k}\). That scaling is **KNOWN** from the formula. P1 is the untested field check of that exponent. As \(k \to 0\), groups re-form continuously and keep no lasting identity: the swarm limit (an **ANALOGY**, not a field result).

The checked qualitative precedent is Malone, Yates & Benjamin 1987 (*Communications of the ACM* 30(6):484–497, doi 10.1145/214762.214766): lower coordination costs shift activity toward markets rather than hierarchies. That is not the square-root lifetime and not the swarm limit (see also Malone 2004, *The Future of Work*, not used as evidence here).

It is a **HYPOTHESIS** that AI lowers \(k\) and that structures then behave more like swarms (that AI lowers \(k\) is unmeasured).

## 6. Assumptions (scrub these)

Each of these is a window the rest of the page looks through. If it is wrong, here is what breaks.

| Assumption | What breaks if it is wrong |
|---|---|
| Strong selection | Part 2 does not apply. Designs need not sit near the minimum. |
| Cost-covered persistence | If a system can last without covering its costs, low-\(J\) designs need not be the ones that persist, and selection need not climb toward the minimum. |
| Shared-only delay | If the same latency sits on local updates, the delay floors cancel and speed does not flip the choice. |
| Shared lump below \(N\) local lumps (\(k_S<N k_L\)) | If the shared re-forming cost is not cheaper than \(N\) local ones, the slow-shared side of the crossing is absent. |
| Equal read quality | If a shared read is systematically better or worse than a local one, fast scales need not go local. The factor \(e^{-2\ell/\tau}\) stays positive. |
| Exogenous world, stationary for the information floor | If the system shapes the world it tracks (CX2), or the world has no stationary law (CX1), S1 as proved does not apply. For drifting worlds, the flow form of the floor is in `theory/THEOREM_P_DRIFT.md` (CLAIM_MAP section T; reviewed, fixes pending confirm). |
| Read cost at least linear in the directed-information rate (S-A) | The assembled information floor can fail as a bound on operational \(J\). S-A is an assumption, not a sensor law. |
| Re-forming is lumpy | If adjustment is smooth, there is no discrete lifetime \(T^*\). |
| A layer cannot cheaply reset the whole state | If one action can rewrite the sum at little extra cost, a stack is the wrong design and the spacing rule does not apply. |

## 7. Evidence so far

- **DIR1 (TESTED: INCONCLUSIVE).** A directional, price-free test on the published record, not a test of the banded hypothesis, and not a qualification under THEORY §3. Pooled agreement is 29/42. Animals support (20/27). Firms fail the locked class gate (6/10 = 0.60; four zeros, no −1). Cells do not count (\(n = 5\)). The kill needed two class fails; it was not met. Predictions D1–D4 do not separate this cost from any other cost-benefit optimizer. D5, the local-versus-shared sign, went unscored (\(n = 2\)).
- **Karim, Carroll & Long 2016 and Girod & Whittington 2017 do not identify P2 or P3.** They measure neither the variance rate of a tracked gap, nor a re-forming cost \(k\), nor latency on a shared channel, nor a local-versus-shared contrast. They cannot count against those predictions, and they cannot support them.
- **No system has yet been shown to qualify as strongly selected.** The 30 earlier field rows are NOT A TEST (10 passed and 20 failed on proxy). In-model selection tests are mixed (EVO1). Palmer, Marre, Berry & Bialek 2015 test efficient coding of predictive information in the retina. Mattingly, Kamino, Machta & Emonet 2021 test an *E. coli* chemotaxis bound. Both are consistent with the technical half. Neither was preregistered here, and neither qualifies under THEORY §3.
- **Layer-lifetime predictions, not T27's P1–P3 and not the *E. coli* discrimination checks (OPEN, not locked; no outcome data retrieved).** T27's P3 failed in-model and is not rescued (`core/bridge_2026-11-21/`). **P1:** in a class of groups that form and dissolve, with an independent measure of re-forming cost \(k\) moved by an outside shift, the log of median lifetime against \(\log k\) has slope near \(1/2\) at fixed drift. **P2:** where a system has at least two lumpy layers with independently measured \((k_i,\sigma_i^2,w_i)\) and the stakes are equal, the lifetime ratio matches the §3 formula inside a preregistered factor. That formula is not the prediction when the stakes differ. **P3:** when a shared update has measurable latency, faster drift of the common driver shifts weight from shared to local (respecting the mid-scale warning of §4). Each needs a class that qualifies under THEORY §3.
- Every theorem has been refereed at most once, by one bot family, and no human expert has read the theory.

## 8. What is next

A note on the stationary excess, under a log-linear fitness map and weak mutation, is in `theory/SELECTION_AXIOMS.md`. Copying that favors lower cost is not enough for the excess \(d/(2\beta)\). The fractional form \(\approx d/(2\sigma N_e)\) is the bridge's formula, with \(N_e\) equal to Sella and Hirsh's \(\nu\) (haploid Moran \(\beta=\alpha(N-1)\); diploid Wright–Fisher \(\beta=\alpha(2N-1)\), an approximation). T27's P3 failed and is not rescued. The drifting-world sum adds the CL19 lag only under the extra assumptions in that note (additive costs, zero discount, the lumpy coordinate outside the substitution chain, timescale separation). The excess \(d/(2\beta)\) is derived in-model under A1, A2-L, \(N\mu\ll 1\), and SA1–SA1b, and that excess is small only when \(\sigma N_e\gg d\) (THEORY §4; `theory/SELECTION_AXIOMS.md` §10). The empirical bet is whether real systems meet those assumptions with parameters that make the remainder small, tested by SA-P1, which is not locked. The Part 2 hypothesis sentence is unchanged.

For an optimum that moves in the soft coordinates, see `theory/DRIFT_SELECTION.md` (CLAIM_MAP section S; revised after the independent review of PR #146).

## References

- Chalkley 1997, *Economics Letters* 57:189, doi 10.1016/s0165-1765(97)00222-x.
- Dixit 1991, *Review of Economic Studies* 58:141, doi 10.2307/2298051, title "Analytical Approximations in Models of Hysteresis"; *JEDC* 15:657, doi 10.1016/0165-1889(91)90037-2.
- Palmer, Marre, Berry & Bialek 2015, doi 10.1073/pnas.1506855112.
- Mattingly, Kamino, Machta & Emonet 2021, doi 10.1038/s41567-021-01380-3.

## Status words and standing caveats

**PROVED** means proved inside the stated model, which says nothing by itself about nature; **NUMERICAL** means computed, not proved; **HYPOTHESIS** means a claim about the world; **TESTED** is reported with its result; **KNOWN** means published and credited; **OPEN** means untested or not derived, not refuted; **ANALOGY** means a likeness, not a proof and not a field result.

The operational kill rule stays in force in THEORY §3. There is no Model S counterexample to N60. The rhythms counterexample (two oscillators, \(R=3\), formula 2, argmin 3) and the failed IMP-N60 rule stay in force in `core/KEYSTONE_NOTE.md`. Convexity inside Model S is numerical (120/120), not proved.

Omissions from this page are compressions, not withdrawals. The previous text is frozen at `history/2026-11-21_CORE_before_onepage.md`. The information limits (S1–S3) are in `theory/SHANNON_2026-11-21.md`; the layer-lifetime results are in `theory/LAYER_LIFETIME_2026-11-21.md`. This page was revised after the independent review of PR #142 (`reviews/core_onepage_2026-11-21/REVIEW.md`, verdict NOT READY) and the blind confirm (`reviews/core_onepage_2026-11-21/CONFIRM.md`). IDs: `measurement/CLAIM_MAP_v2.md`. `main` is `d34df95` (PR #140 live brief; also #141 layer lifetime as `a97887e`, #139 Shannon-style core as `0726423`, and #138 DIR1 as `1cb1ac2`).
