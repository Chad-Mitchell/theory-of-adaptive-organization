# A Theory of Adaptive Organization: the cost of judgment — v2.2 draft (19 November 2026)

Author: Chad Mitchell (X: [@torusflow](https://x.com/torusflow)). Public domain (CC0). Not peer reviewed, and not independently reviewed as a whole. **This file is the one canonical statement of the theory; where anything else in the repository disagrees, this file governs.** The main text (§1–§10) reads in about 15 minutes. Appendix A fixes the model and notation, Appendix B proves every numbered result, and Appendix C maps each result to its claim row and its derivation. Claim statuses: `measurement/CLAIM_MAP_v2.md` (v2.51). The previous core is frozen at `reference/THEORY_v2.0.md`; the changelog and the full record of tests and reviews are in `reference/` and the folders it indexes.

**Status words.** *Proved in-model*: a theorem inside the stated model, which says nothing by itself about nature. *Known*: a published result, credited. *Open*: untested, not refuted. *Passed/failed on proxy*: a locked prediction scored on an instrument that fails at least one validity gate, which is a result about that instrument, not about the theory.

## 1. Judgment under the second law

Everything runs down. The second law lets order last only where something pays to keep it, exporting disorder as it goes. An atom or a crystal pays almost nothing: nothing it does changes whether it lasts, so a model of the world would buy it nothing. A star or a flame pays a steady flow of energy and regulates itself, but anticipates nothing. Cells, colonies, people, firms and cities are different. They must stay far from equilibrium in a world that keeps changing and can ruin them, and they cannot wait for that world to arrive. Once acting late is costly, it pays to carry a model and act ahead.

That is **judgment**, and judgment has one cost: holding memory, being wrong or late, and buying and sharing the information that keeps memory fresh, all without going broke. The theory adds no physics to the second law. It prices what staying alive under it takes, and says the price sets the design: where the world changes on several time scales, build in layers, one for each time scale the stakes can pay for. The same cost decides when a model should be shared, who must be in charge, and how far one tracker can reach.

The bet is that strongly selected systems, at every scale, sit at that cost's minimum. It dies the first time such a system, with its world and its costs measured, puts its layers somewhere else or needs a cost the equation cannot book.

## 2. The claim

**The claim is that one cost under the second law sets how adaptive systems should be built at every scale: layered, with the layers at the world's time scales.**

*At the world's time scales* means: one layer for each separated time scale the world changes on that the stakes can pay for, each with a memory set by that scale and the sensing noise (usually much shorter than the scale itself: in one worked case a 90-day mode gets a 6–12-day store). *Under the second law* means that physics supplies the reason upkeep exists and a floor under every price; above the cell those floors are slack (§9).

## 3. The master equation

A system that must act ahead of a world it does not control chooses its design 𝒟 to

$$
\min_{\mathcal D}\; J(\mathcal D) \;=\; \underbrace{\kappa\, I_{\text{mem}} + h\,K}_{\text{holding memory}} \;+\; \underbrace{w\,\mathbb E[\ell_{\mathcal D}]}_{\text{being wrong or late}} \;+\; \underbrace{A(\mathcal D) + L(\mathcal D)}_{\text{acquiring and sharing information}} \qquad \text{subject to}\quad P(\text{ruin}) \le \varepsilon_r .
$$

- **𝒟**, the design: the number of layers K, what each tracks, how and how often it senses, and what it shares.
- **κ·I_mem + h·K**: the price κ per nat held per unit time, and the upkeep h of each layer, store or shared level.
- **w·E[ℓ]**: the stake times the expected loss at the moment of use. Lateness counts as error, because a prediction that arrives after the moment to act buys nothing.
- **A(𝒟)**: information-acquisition spend, priced per read (Σ c_k f_k, read price times read rate), per nat acquired (λ), or per unit of precision (c′·r^{−θ}).
- **L(𝒟)**: link, telling and lookup costs: κ_b per member–level link, d per member told, u per lookup at use rate μ. This is what puts pooling and sharing inside J.
- **Ruin**: a reserve that starts at buffer B, earns income y and pays J hits zero; ε_r is the tolerated chance.
- **The world** is exogenous and enters only through its measured pattern of change: its spectrum or Markov kernel, the sensing noise N and the lead k at which actions meet it. The drift level q and spectral slope α are the scale-free special case.
- **One currency per system** (heat, attention, money, compute). Physics sets floors on the prices (at least kT per nat acquired or erased by a measuring tracker, and kT·(I_mem − I_pred) for memory that does not predict: Landauer 1961, Still et al. 2012), not exchange rates between systems. Written in each system's own units the equation is the same problem at every scale: only dimensionless ratios matter and the cost shares at the optimum are currency-free numbers (CT24); the distance of a price from its floor is one measured number per system, not predicted by the theory.
- **Open lever.** Effort g spent making the world drift less (homeostasis, buffers, contracts) belongs in the problem, but it makes the world depend on the design, so every theorem below holds the world fixed, g = 0; the coupled case is the open theorem of §9 (CX2, CL11).

The equation is assembled from known parts; the repository already wrote it as Axiom 5 of `reviews/night1/formal/AXIOMS.md`. It is the theory's statement of the problem, not a theorem.

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

Here *minimize* means: sit near the minimum of J, given their measured world. This is a bet, untested and not yet earned. Tests that would make it a law: (1) in strongly selected systems at two or more scales, the layers (count, memories, read rates) match the minimum of J computed from each world's measured drift spectrum, sensing noise and prices, better than a named rival (N56, N13); (2) designs move with measured changes in their inputs as predicted, such as read rate with elasticity 1/α in drift (N51) and layers added as stakes rise relative to upkeep; (3) no level at any scale needs a cost J cannot book (J16). Any of these failing as preregistered kills it (§8). Until then, what is established is a principle (§4), theorems proved in-model (§5), and field results passed or failed on proxy.

## 4. What kind of theory this is

The theory has three parts. A **definition**: the cost J. A **principle**: strongly selected, persistent adaptive systems sit near the design that minimizes J, to within the tolerance ε their selection can resolve. That has the form of a variational principle, as least action does, with one difference that matters: least action has no free prices and J does, so the principle says something only through structure that holds for every price (§5 (ii)–(iii)) and through prices measured independently of the design they predict. Whether real systems obey it is untested, not refuted. If strongly selected systems across scales are found near the cost's minimum, that cross-system regularity would earn the hypothesis of §3 its name in the scientific sense; until then what is established is a principle. **Theorems**: what minimizing J implies, proved in stated classes (§5).

The world's pattern of change is a **measured input**, not part of the theory, so there are two kinds of wrong. **A wrong picture of the world** means re-measuring and getting a new design; it costs little, because regret is second order in the picture error (CT23: misjudging drift 2× costs about 4–6%), except near cliffs such as the viability edge or the lookup cliff, where a small error can flip survival. **A wrong or missing cost kills the theory**: no regret bound covers a cost J cannot book.

## 5. The theorem

**Master Theorem** (proved in-model in the linear-Gaussian class 𝓜_LG, Appendix B.9: exogenous Gaussian world, stationary or with stationary increments, sensed through white noise or read exactly; layers are first-order stores with rates in a compact set; squared error at lead k; ruin imposed through the Lundberg bound. New, and not yet independently reviewed as a whole.)

- **(i) Existence** (CT20). If any design survives, a best design exists, and its layer count is at most J(𝒟₁)/h for any surviving one-layer design 𝒟₁.
- **(ii) Monotone in every world** (CT20). The best layer count never falls as stakes rise relative to upkeep (w/h), and a single layer's best read rate never falls as w/c rises. This part holds for every world and every loss.
- **(iii) The world caps the layers** (CT21). The best layer count is at most the number of dimensions of the world's optimal predictor (its McMillan degree). A world with one time scale needs exactly one layer, **including the self-similar random walk** (L1). A world with J separated time scales needs at most J, exactly J (at zero lead) once R = w·E_∞/h is large enough, and layers beat one flat tracker iff R > R\* = min_K (K−1)/(Δ₁ − Δ_K), with Δ_K the relative excess error of K layers (L2). A continuum of time scales has no exact finite design (L3).
- **(iv) The price of survival.** Below a minimum buffer B_min no design survives. Above B_slack the ruin constraint is slack and the expected-cost rules are exactly optimal. In between it binds with a multiplier μ_s > 0, the price of survival, which moves the design from the expected-cost optimum (μ_s = 0) toward Theorem L's survival-optimal design (the μ_s → ∞ end) (CT22). In the diffusive-reset class the constraint is the temperature: per-window ruin erfc(z/√2) ≤ ε_r means z = B/(σ√τ) ≥ z_ε, so the buffer needed grows as shock × √(time to fix), and the largest shock a unit survives falls as τ^{−1/2}, which is why faster correction raises the ceiling (CT25, proved in a model; first passage is Black & Cox 1976, not Merton's terminal default). The √time spread is all this shares with Drăgulescu & Yakovenko's (2000) money-gas "temperature": an analogy only, since nothing physical sets it here. That stress *strengthens* a system is not implied; it needs an adaptation rule and stops at B_min (K7, open).
- **(v) Special cases.** Each named result is J under a stated restriction, and `theory/meq_checks/meq_derive.py` checks each derivation:

| Result | J restricted to | Gives |
|---|---|---|
| Read-rate rule (CT12, CT13) | one layer, exact reset reads, A = c/T | J(T) = c/T + w·q·T^{α−1}/α: read rate ∝ (w·q/c)^{1/α}; a 2× input error costs ≈ 6% at α = 2 |
| First bit must pay (CT4; Theorem P, CT1–CT3) | κ·I_mem + w·E only | carry a model iff κ < 2 ln 2·a²·Var (Gaussian); size grows with log stakes; when acting blind is not viable a model is necessary |
| Layers (L1–L3, CT21) | J_K = h·K + w·E_K, sensing fixed by noise N | (iii) above |
| Sharing (Result 4: B2, CT16, B12) | L = telling or link cost, pooled stakes | a shared level pays iff N > N\*(ρ) = (√(1+ρ)+1)²/ρ; telling pays iff d/c < 1/N\* − 1/N; with per-read broadcast, never unless ρ > 4t/(1−t)², t = c_b/c |
| Freeze, hold or look up (T8, CT11) | L = μ·u | a fact is frozen, held or looked up by its drift; the band widens N² when shared |
| One clock for many (CT17) | several parts, one A | one clock costs more unless c_i/(w_i·σ_i²) is equal |
| Reach (LAT-1, CT19) | E at latency ℓ = L/v | error ≥ q·ℓ^{α−1}, so L_max = v·(D\*/q)^{1/(α−1)} |
| Survival (CT22; Theorem L, CL2) | the ruin constraint | (iv) above |
| Physics floor (CT7) | A priced at λ ≥ kT per nat | J\* ≥ σ√(2kT·w): **a floor on J, not a solution of it** |

![Illustrative phase diagram](theory/meq_checks/phase.png)

*Illustrative only:* the best design in one made-up model world (two time scales, `theory/meq_checks/phase.py`). As stakes over upkeep rise the regions run no model → one layer → two layers → not viable; at high latency, federation. The **order** follows from (ii) and Theorem P in every world; the **positions** are this world's. No real system has been placed: none has valid measured stakes.

**Theorem L, stated correctly.** Theorem L maximizes the survival exponent. Its best interval does not depend on the buffer, and it reduces to the expected-cost rule when the reserve's own noise dominates, not when the buffer is large. The large-buffer statement is (iv).

**Scale-free cost shares (CT24, proved in a model; the setting is CT12's single tracker).** J is homogeneous of degree 1 in its prices, so by the envelope theorem and Euler's theorem each term's share of the optimal cost equals the elasticity of J\* in that price, and the shares sum to 1. For one tracker the sensing share is (α−1)/α and the share lost to being wrong is 1/α: **looking costs α − 1 for every 1 lost to being wrong, in any currency, at any scale** (α = 2 is the classical equal costs of the order-quantity rule). This is a currency-free, cross-scale prediction (N57, open); it needs the stakes w to price error, so it inherits the measurement gap G3. The same homogeneity makes w, h and c a system's own shadow prices when it allocates a binding budget: the multiplier of a read budget is 1/w, and a K-way allocation gives K − 1 testable equalities of marginal value (KKT, convex single-tracker class); that real internal prices equal multipliers is conjecture CX5. With the floor priced at β·kT per nat, J\* rises by β^{(α−1)/α} and the shares do not move: the gap to the floor changes the size of a system's cost, not the shape of its trade-off.

## 6. The spine

1. Judgment has one total cost, holding memory plus being wrong or late plus acquiring and sharing information, with the risk of ruin as a constraint, and physics puts a price floor under each part at every scale.
2. The theory is that cost and the design that minimizes it; how the world changes is an input, measured on each system, never assumed.
3. A world that changes on one time scale is tracked best by one layer, even when that change is a self-similar random walk.
4. A world with several separated time scales is tracked best by one layer per scale once the stakes outweigh a layer's upkeep (R > R\*), each layer's memory set by its scale and the sensing noise, and with a continuum of scales the count keeps rising with stakes over upkeep.
5. The architecture inherits the world's scale structure: where change is scale-free the layers come out roughly log-spaced (exactly geometric for shared clocks, CL12), and where it has rhythms (days, quarters, seasons) there is one layer per rhythm.
6. Across members the same cost decides: a shared level forms once enough members face a common driver (N > N\*(ρ)) and telling or broadcasting is cheap enough (CL17); levels are complements that accrete as upkeep falls, and cheap lookup dissolves levels that only hold facts.
7. Unless keeping shared memory up is privately rewarded, expect someone in charge, through shared fate or enforcement, because a part that bears only Λ_i of the whole's loss watches at (Λ_i/Λ_whole)^{1/α} of the right rate.
8. Lateness caps how far one layer can reach, so beyond L_max a system federates into separate trackers (when no faster shortcut exists).
9. A wrong picture of the world costs second-order regret and is fixed by re-measuring, but the theory dies if strongly selected systems, with inputs measured, do not put their layers where the cost says, or if some level needs a cost that J cannot book.

**Two axes, one rule.** Stores lie across time scales and levels lie across members; both come from the same comparison of a layer's saving with its upkeep, applied once to the world's spectrum and once to its shared-drift structure. The set of levels is a copy of the world's shared-drift structure, one level per shared driver whose pooled stakes pay (Axioms 5–6; CL13, CL14), as the stores are a copy of its time scales. In a nested tree, levels fill from the broadest scope down iff shared drift falls slowly enough with scope (χ < χ\* = (1−a)/(1−b), formal Theorem 7; CL15). A pooled level faces the same problem as a member (closure under coarse-graining, T7c), which is the precise sense of "every scale"; that the architecture inherits whatever scale structure the world has is T7 (CL16). Decoupled layers are nearly optimal only when their time scales separate, and lose to one flat tracker when the scales collapse (`theory/THEOREMS.md` T3c, numerical). The idea that loosely coupled parts give fast dynamics inside and slow dynamics between is Simon's (1962); that higher brain levels track slower causes is Kiebel, Daunizeau & Friston's (2008).

**Sizes.** On the time axis a layer buys modest gains: 0.2–5% of the error cost in scale-free bands, about 20% at most in the scans, and at most 29% for one extra clock. The large gains come from pooling (about N reads saved for one), the lookup cliff and ruin margins.

## 7. Uses: design and diagnosis

**Design.** Measure the world's pattern of change, price the reads, upkeep and stakes, and solve J for the number of layers, their memories, the read rates and what to share. For monitors, caches, sensor fleets, inventory and forecasting this is a calculator today (worked example: `theory/MASTER_EQUATION.md` §2). The seven design rules of the 12 November post (archived in `history/`) are listed below with their status in v2.1. An earlier sentence called all seven solutions of J; that was too strong for rules 1, 4 and 6.

| # | Rule | Status | Where | Fails when |
|---|---|---|---|---|
| 1 | Act early; interrupt unasked only if stake × chance it matters, plus what the outcome would teach, beats the cost of interrupting | partly derived | lateness is error (§3), CT19; the learning value is not a term of J | myopic interrupts; near-tautology |
| 2 | Keep a fact while need × miss cost beats upkeep, which rises with drift; otherwise let it fade, recoverably | theorem (proved in a model) | CT4, CT9, CT11 | the world is not Markov in the coordinates kept |
| 3 | Move a belief by the reliability of the signal | theorem (known: Kalman 1960, Muth 1960) | CT21 (L1) | heavy-tailed noise; non-Gaussian worlds |
| 4 | Keep prior versions until a correction proves out | heuristic | outside J (symmetric loss, no recoverability term) | never derived; near-tautology |
| 5 | Act from the current model, not a copy; a copy's error grows with hops and with drift since the last check | theorem (proved in a model) | CT8, CT19 | seasonality or other non-Markov observed variables |
| 6 | Record whether each prediction was used, ignored or late | hypothesis | not derived; it supplies the inputs of redesign (N54) and of stakes (G3); the Hebbian and ant-trail form, one mechanism at every level, is untested (Hebb 1949; stigmergy) | the mechanism does not follow from the cost |
| 7 | Watch more as drift × stakes rises, and stop past a point when a cheaper fallback exists | theorem (proved in a model) | CT10, CT12, Lemma B1, CT22 | the buffer sets the value of survival effort through μ_s, not the cost-optimal interval |

**Diagnosis.** The same equation reads an existing organization (a firm, a team, a city, a cell) against its costs:
- which layers the costs say should exist, given the time scales its world changes on;
- layers that do not pay their upkeep;
- layers that cheap lookup should have dissolved;
- missing layers for time scales the stakes can afford;
- reads that are mistimed for the drift and stakes they face, and parts that under-watch because they bear little of the whole's loss.

Much of this works from signs and ratios, without exact stakes: the comparative statics of §5 (ii) hold in every world, and only price ratios (w/c, h/w) are identified. Prices can also be inferred backward from an observed design (revealed costs, as in Afriat and Varian's revealed preference and Kalman's inverse-optimality question). That is a test, not a circle, only when observed features outnumber the free price ratios: one system seen at several exogenous drift levels, several items under one clock, or one read technology across layers.

**Applicability is general; the bottleneck is measurement.** Firms, teams and cities fall under the theory exactly as machines do. What differs is how hard stakes and upkeep are to measure, not whether the theory applies, within the scope of §9.

## 8. Predictions, and how it dies

**The killing test** (preregistrable): in a strongly selected system, measure the world's drift spectrum and the sensing noise, then compare the system's layers (count, memories, read rates) with argmin J. The theory dies if, in two or more such systems at different scales, the design misses its optimum by more than measurement error allows *and* a named rival (a fixed budget share; a universal exponent of ½) fits better; if design fails to move with a measured change in its inputs by the preregistered share; or if a level needs a cost J cannot book (CLAIM_MAP N13, J6, J16, N56; locks in `measurement/FRAMEWORK.md`).

| Prediction | From | Status | Dies if |
|---|---|---|---|
| Layer count and memories match the measured spectrum where R is large | §5 (iii) | Open (N56) | Count does not rise with separated time scales or with stakes over upkeep |
| Look rate at a drifting quantity has elasticity 1/α in stakes and drift (needs no stakes measure within one system) | CT12 | Open (N51; a lab test is specified) | Elasticities at α = 1.5 and 2.5 are not separated in the predicted direction |
| Redesign runs 10–100× slower than the slowest tracked time scale, because the world's pattern must be learned first | Learning the world's pattern takes tens of its slowest time scale (B.9) | Open (N54) | Redesign cadence is comparable to the slowest layer's |
| Design scatter across a population scales like 1/√(α−1): rough worlds give widely scattered cadences | curvature α − 1 of J, B.9 | Open (N55) | Scatter does not fall as α rises at fixed selection strength |
| Watching effort rises with drift, then collapses once a bounded fallback exists | G3 | Proved in-model; known for web crawlers | Effort keeps rising through the top drift decile where a fallback exists |
| At the optimum a tracker spends α − 1 on looking for every 1 it loses to being wrong, in any currency | CT24 | Open (N57) | Across systems of known α with measured stakes, the sensing share does not follow (α−1)/α |
| At fixed shock and buffer, slower fixing raises failure risk iff the shock elasticity exceeds 2, and at a fixed observed spread it lowers it (ε_τ = −1); the buffer needed grows as shock × √(time to fix) | CT18, CT25 | Open (K4); five field tests (H11–H15) fail or are inconclusive on proxy, none with a valid measured fix time | With a measured fix time, risk is flat in it, or the sign reverses at fixed spread |
| A unit's survivable shock falls as τ^{−1/2}, so faster correction raises the stress ceiling; stress strengthening itself is a hypothesis | CT25; K7 | Open (K7); the ceiling is proved in a model, strengthening is not derived | Faster correction does not raise the survivable shock, or exposure does not raise tolerance |
| A shared level appears once group size exceeds N\*(ρ); its onset exponent tracks the level's sensing technology, not α | Result 4 | Proved in-model; untested in the field | The onset does not move with ρ |
| A tracker's central share falls with q·ℓ^{α−1} | LAT-1 | Open (N27) | At fixed q the central share does not depend on ℓ |
| Cheap lookup removes layers that hold shared facts, not layers that enforce | T8, CT17 | Open (N52) | Enforcement layers shrink as fast as holding layers |

**The first tests anyone can run:** the attention-exponent lab task (N51) and a same-system test of measured-input optimality (SAME-SYSTEM-AQN, designed, not yet run). Quantities must pass validity gates MV1–MV10, binding since 18 November 2026. A test on a mismatched proxy is invalid, not failed, and results are reported as passed or failed on proxy.

## 9. Scope and caveats

- **Worlds that respond: the most important open theorem.** A system that reshapes its world (a market that reacts, an adversary, a firm or city that changes its own demand) is the same structure one level up: the system and its world are coupled layers of a larger, nested system. That is inside the theory; what is open is the math. Every proof so far holds the outer level fixed (g = 0). Whether co-adapting levels settle at a joint minimum, cycle, or race (predator and prey, arms races) is the key open theorem (CX2); drift reduction g is one case of it (CL11).
- **The layer results (L1–L3, CT21) are linear-Gaussian, squared-error, and not yet independently reviewed.** Nothing is proved for jump worlds, Bayes trackers or other losses. Whether layers must be separate *agents* or can be stores inside one agent is open.
- **One currency per system.** "Every scale" means the same problem solved with each system's own measured inputs and prices, not one exchange rate. Physics sets only price floors (kT per nat); in a synapse the price is about 10⁵–10⁶ times the floor (Laughlin et al. 1998), and in a firm far more. Whether the second law does more than set floors above the cell is an open disagreement; Chad's position is that the physics is not decorative.
- **Further limits.** Not covered: regime shifts, where the world's pattern changes and must be re-measured or modelled as switching (N16); goals beyond tracking (exploration, play), because J prices staying matched, not what is worth wanting; indivisible reads, which gain no clock saving (formal Prop 9); and costs that do not add or that scale differently with size, where covariance fails and crossovers appear (S4, Lemma B12). **Conjectures, not proved:** federation pays iff Σᵢ Jᵢ\* + J_coupling < J\* of one flat tracker (CX3); beyond the linear-Gaussian class the layers are the components of the world's predictive state that are worth their upkeep, capped by its statistical complexity (Crutchfield & Young 1989) or predictive information (Bialek, Nemenman & Tishby 2001), with a two-state switching world the first test (CX4).
- **"Should be built", not "are built",** until a same-system test exists. That selection holds designs near the optimum is assumed (Alchian 1950), and below the drift barrier misses are expected (Lynch et al. 2016).
- **Theorem P** (when judgment pays) is proved for stationary worlds; most results use drifting ones (CX1, open).
- **No valid measurement of a tracked world's drift spectrum exists yet** (GAPS G1). The NYC 311 data are scale-free across complaint categories, after post hoc dequantization; in time the hourly series breaks near 22 hours. The 10-year Treasury yield (DGS10) is a random walk on proxy (α = 2.00 ± 0.03), so it needs one layer.
- **Change is not "fractal, period".** The theory does not say physical time is fractal; that framing is withdrawn (N46). What it says is about inputs: whether the world a system tracks changes self-similarly over a band is measured, and if it is, the layers come out roughly log-spaced. The literature shows broad scale-free bands broken by cycles and cadences, a mixed spectrum, which is what multi-layer design needs.
- **Where it stands.** No field test has yet measured the theory's quantities validly, so the bet is untested, not refuted: 15 field rows failed on proxy and 7 passed on proxy, none support or refutation. The 12 November post's lead prediction got every sign right but failed on proxy in its τ-specific structure (K4). Of the locked predictions about the authors' own simulators, six failed, three passed and three were inconclusive. Each theorem has been refereed at most once, by the same bot family, and no human expert has read the theory.
- **Ends of the scale.** Atoms are frozen because nothing they do changes whether they last (E1); stars regulate themselves and anticipate nothing outside; the cosmic horizon caps memory. The theory does not derive black holes, does not claim a torus universe, dark matter or energy, or that wormholes exist (`theory/REACH.md`).

## 10. Known parts, new claim

**Known and credited.** The split between things that keep, things that regulate themselves and things that track is prior art in substance (Prigogine 1978; Pross 2011). The cost-plus-information form is textbook: rational inattention (Sims 2003), information-theoretic bounded rationality (Ortega & Braun 2013), hierarchies that arise from information-processing costs (Genewein, Leibfried, Grau-Moya & Braun 2015), sensing cost inside LQG control (Meier, Peschon & Dressler 1967), Kalman filtering (Kalman 1960). The time-scale hierarchy is Simon's (1962) and Kiebel, Daunizeau & Friston's (2008); multiresolution estimation, Willsky (2002); geometric clocks, Roundy (1985). The physics: Landauer (1961), the thermodynamics of prediction (Still, Sivak, Bell & Crooks 2012), sensing costs (Barato, Hartich & Seifert 2014; Lan et al. 2012). Ruin and growth: Kelly (1956), chance constraints (Roy 1952; Charnes & Cooper 1959), first-passage default (Black & Cox 1976), Cramér–Lundberg. Two-time-scale learning: Borkar (1997). Switching under uncertainty and hysteresis: Dixit (1989). Monotone comparative statics: Topkis (1978); Milgrom & Shannon (1994). Pooling: Veldkamp & Wolfers (2007); Van Zandt & Radner (2001). The square-root rule: Harris (1913). The temperature (typical shock over buffer, spread growing as √time) is analogous to the money-gas "temperature" of Drăgulescu & Yakovenko (2000), credited as an analogy only; first passage is Black & Cox (1976) and the ratio z is the inventory safety factor. A nat of information is worth at most a nat of log-growth under proportional betting (Kelly 1956; Donaldson-Matasci, Bergstrom & Lachmann 2010; Vinkler, Permuter & Merhav 2016). DOIs were checked on Crossref in `theory/meq_checks/crossref.out` (Simon 1962 by its JSTOR record); the remaining credits are carried from v2.0, and the full list is in `litmap/`.

**The theory's own, as far as anyone has found:** the package. A layer count priced inside one objective; the world's measured pattern of change as the only world input, with its predictive dimension capping the layers; a ruin constraint whose slack end recovers the expected-cost rules; one booking rule across substrates with a kill condition; and predictions across scales, posed so that they can fail. The parts are known and the claim built from them is new. Several elementary results also appear to be new (hold-or-fade for any Markov world; the freeze, hold and look-up band; the onset exponent fixed by the level's technology; the telling and broadcast thresholds; LAT-1's form; the temperature identity; L2's iff threshold R\*). The prior-art search is not exhaustive. If the bet holds when tested, its weight will come from what it explains, not from new ingredients.

---

## Appendix A. The model and notation

### A.1 The model

Every result in Appendix B is a theorem about this model (the Master Theorem's class 𝓜_LG, B.9, narrows it), and each states which parts it uses.

- **World.** A state X_t that the agent does not change (exogenous). Two classes appear, and each result names its class. **(W-a)** stationary, ergodic Markov: the world fluctuates around a fixed law. **(W-b)** drifting: Gaussian with stationary increments, E(X_{t+τ} − X_t)² = q·τ^{α−1}, with **spectral slope** α = 1 + 2H between 1 and 3 (a random walk is α = 2) and **drift level** q.
- **Agent.** A memory M_t updated from observations, and actions A_t = π(M_t) committed a lead time k before they meet the world.
- **Persistence.** A reserve starts at a buffer B, earns income y and pays every cost; ruin is the first time it reaches zero.
- **Selection.** Selection keeps designs within a tolerance ε of the cheapest. That is an assumption about strongly selected systems, not a theorem (§4).
- **Φ**, the **lifetime value of a fresh reading**: how much one exact reading lowers expected loss, summed over the time until the world has drifted away from it.
- **Regime first.** Every number names its world class, its α and its premises. A result proved for α = 2 is not assumed at other α.

### A.2 Notation

One symbol, one meaning, throughout this file. Files elsewhere in the repository use some symbols differently; where they do, this table governs, and the last column names the main collisions.

| Symbol | Meaning | Elsewhere it can also mean |
|---|---|---|
| X_t, M_t, A_t | world state; agent's memory; action | — |
| k | lead time (an action meets the world k later) | Boltzmann's k in kT (written kT only) |
| ℓ(a, x); w (or W for a pooled or per-user stake) | loss; stake weight on squared error | ℓ also latency in `theory/` files (here: ℓ = L/v only in LAT-1, CT19) |
| D(R), R(D) | distortion-rate and rate-distortion functions; D\* a tolerable error | — |
| I_pred | long-run predictive information I(M_t; X_{t+k}) per step | — |
| y, c̄, B | income rate; mean of the other costs (per policy); initial buffer | — |
| α, H, q | spectral slope (S ∝ \|ω\|^{−α}), α = 1 + 2H; drift level in E(ΔX_τ)² = q·τ^{α−1} | α also an α-stable index or a Pareto exponent; q also the spectral level q in S = q\|ω\|^{−α}, which differs by an α-dependent constant |
| σ² | variance rate at α = 2 (then q = σ²) | — |
| c | price of one read | the speed of light (written "light speed" here) |
| κ | price per nat held per unit time (per bit in CT4) | a sharing-decay exponent, κ_F, κ = λN/μ² (written out where used); formal Theorem 7's drift-sharing exponent is written **χ** here (χ\* = (1−a)/(1−b)) |
| κ_b, d, u, μ | broadcast link cost; price of telling one member; price of one lookup; use rate | μ_s is the survival multiplier (CT22) |
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
| τ_life | lifetime of a fact (T8) | — |
| ε; ε_r | selection tolerance; tolerated ruin probability in the master equation | ε_X = ∂ ln ν/∂ ln X, an elasticity; ε_K in `theory/LAYERS.md` is Δ_K here |
| 𝒟, J(𝒟) | a design; the master equation's total cost (§3) | J also a number of modes in CT21 (context makes it clear) |
| K, I_mem | number of layers (stores or levels); nats held | K also a number of clocks (CL12) |
| A(𝒟), L(𝒟), g | acquisition spend; link, telling and lookup costs; effort to reduce drift (set to 0 in every theorem) | — |
| E_K, E_∞, Δ_K, R, R\* | least error with K layers; causal MMSE; Δ_K = E_K/E_∞ − 1; R = w·E_∞/h; R\* = min_K (K−1)/(Δ₁ − Δ_K) | R also a span in `theory/` files |
| B_min, B_slack, μ_s | feasibility and slack edges of the buffer; the price of survival (CT22) | — |
| χ | drift-sharing exponent of a nested tree, q_s ∝ n_s^{−χ} (formal Theorem 7, where it is written κ) | — |

---

## Appendix B. Proofs

Each result gives its hypotheses, a statement, a proof and its known limits. **CT** marks the 19 core results, proved in full. **Lemma B*k*** marks smaller results, proved briefly or stated with a pointer. Closed forms are checked in `theory/core_checks/core_checks.py` (32 checks, a few seconds; run by the test suite), and each result names its fuller derivation and older checks. Status words follow CLAIM_MAP section O.

**Names used in the main text.** Result 1 = CT1–CT4 (Theorem P); Result 2 = CT9 (G2); Result 3 = CT12; Result 4 = CT14–CT16; Result 5 = CT17; Result 6 = CT19 (LAT-1); Master Theorem = CT20–CT22 with CT23; L1–L3 = CT21, L4 = CL12. E1 = CT5, I5 = CT6, O1 = CT7, G1 = CT8, G4 = CT10, T8 = CT11, T1c = CT13, R = CT18 (the temperature identity), G3 = Lemma B1, Theorem L = Lemma B9, Theorem S = Lemma B12.

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

**Lemma B4 (vigilance at birth).** In the reset class at α = 2, the new level's effort over a flat member's effort at onset is V(N\*) = ½(1 + (1+ρ)^{−1/2})(1 + √(1 + 4h′(√(1+ρ) − 1)/(r_pρ))), where r_p is the level's read price over a member's and h′ is upkeep in member-cost units. Its floor (h′ = 0) is **1 + (1+ρ)^{−1/2}**, strictly between 1 and 2. The earlier "V ≥ 2" is false as stated (CLAIM_MAP E5, E6, E7).

**Lemma B5 (clocks).** With K independent components read separately at additive cost, in the technology class P(γ, γ), separate clocks save at most 1 − K^{−(1−γ)}: 29% for K = 2 at γ = ½. With indivisible reads they never save (formal Proposition 9; known).

**Lemma B6 (selection resolution).** In 𝒜₁ a level's largest possible fractional saving (N → ∞) is 1 − (1+ρ)^{−b} ≤ bρ (Bernoulli's inequality). So if selection resolves only relative differences larger than ε, no level is selected at any N when ρ ≤ (1 − ε)^{−1/b} − 1 ≈ ε/b: 0.020 at ε = 1% and 0.108 at ε = 5% (b = ½). Formal Proposition 10; CLAIM_MAP F15.

**Lemma B7 (√N fade).** Pooled deposits by N independent users on a drifting target fade faster as √N; on a stable target use preserves. Known (Kalman averaging), linear readouts only; an ant-like nonlinear readout failed in simulation (CLAIM_MAP K9, G15).

### B.5 Who must be in charge

**CT17 (one clock, and the externality).** (i) K parts at α = 2 with read prices c_i, stakes w_i and drifts σ_i² cost Σ σ_i√(2c_i·w_i) on their own optimal clocks, and √(2·Σc_i·Σw_iσ_i²) on one shared clock. The shared clock is never cheaper, with equality **iff c_i/(w_iσ_i²) is the same for all i**. (ii) If the whole loses Λ_whole when a part fails but the part counts only Λ_i, the part's chosen read rate is (Λ_i/Λ_whole)^{1/α} of the whole's optimum.

*Proof.* (i) One clock with interval T costs Σc_i/T + Σw_iσ_i²·T/2, minimized at √(2Σc_iΣw_iσ_i²). By Cauchy–Schwarz, (Σ√c_i·√(w_iσ_i²))² ≤ Σc_i·Σw_iσ_i², with equality iff √c_i ∝ √(w_iσ_i²). (ii) By CT12 the read rate scales as (stake)^{1/α}, and the part sets it with stake Λ_i instead of Λ_whole. ∎

With heterogeneous read prices the shared-clock penalty is unbounded (51× in random draws, 500× when cost sits in one part and drift in another). A worker sharing relatedness r_rel of its colony's fate reads at r_rel^{1/α} of the optimum; at r_rel = ¾ and α = 2 that is 0.87, so it under-watches by about 13%. The externality half holds when the failure cost is not internalized by incentives, shared fate or a controller, and it counts against "no one in charge" as a general claim. `theory/MATH_ATTACK.md` §3.4 (the analogue of Gorman's 1953 condition).

### B.6 Buffers, failure and the temperature

**CT18 (the temperature identity).** *The error accumulates from each fix as σ times a standard Brownian motion, and fixes act on one time scale τ (periodic resets, Poisson resets at rate 1/τ, or proportional restoring at rate 1/τ). Failure occurs when the error reaches B (one- or two-sided).* Then the hazard is **ν = F(z)/τ with z = B/(σ√τ)**, for some function F fixed by the fixing mechanism. Its elasticities satisfy **ε_B = −ε_σ and ε_τ = ε_σ/2 − 1**. Slow fixing raises the hazard iff ε_σ > 2, and at a fixed observed spread s = σ√τ, ε_τ = −1.

*Proof.* The inputs are σ (units x·t^{−1/2}), τ (t) and B (x), and ν has units 1/t. The only dimensionless group is z, so ν·τ = F(z) (Buckingham π). With g = d ln F/d ln z: ε_B = g, ε_σ = −g, and ε_τ = −g/2 − 1 = ε_σ/2 − 1. At fixed s, ν = F(B/s)/τ, so ε_τ = −1. ∎

z is the inventory safety factor (SS = z·σ·√(lead time)). The index fails once errors are biased (a second group, the Péclet number μ_b·B/σ² for a bias drift μ_b, enters), under heavy-tailed jumps (single big jumps dominate), under long memory (the group becomes σ·τ^H/B), and when fixes do not fully reset. How fixing works sets the tail of F (fixed delay e^{−z²/2}; proportional restoring e^{−z²}; Poisson fixing e^{−√2·z}; heavy-tailed fix times a power law). `theory/MATH_ATTACK.md` §2; `theory/GENERAL_THEOREM.md` R0–R5, which writes z = σ√τ/B.

**Lemma B8 (exact per-window ruin; known).** For periodic full resets and a one-sided barrier, the per-window ruin probability is P = erfc(z/√2) = 2Φ̄(z), the reflection-principle first-passage probability, which is Black & Cox's (1976) default probability at zero drift. Merton's (1974) terminal-default version is off by a factor of 2. The calendar hazard is ν = −ln(1 − P)/τ. Two-sided and biased cases have known series (`theory/GENERAL_THEOREM.md` R1–R2). DOIs: 10.1111/j.1540-6261.1976.tb01891.x; 10.1111/j.1540-6261.1974.tb03058.x.

**CT25 (temperature as the ruin constraint; proved in a model).** In CT18's setting with per-window ruin P = erfc(z/√2) (Lemma B8), P ≤ ε_r iff z ≥ z_ε := Φ̄⁻¹(ε_r/2), which is 2.576, 3.291 and 4.892 for ε_r = 10⁻², 10⁻³ and 10⁻⁶. So the buffer must satisfy B ≥ z_ε·σ√τ: it grows as shock × √(time to fix). With B and ε_r fixed, the largest survivable shock is σ_max = B/(z_ε√τ) ∝ τ^{−1/2}, so faster correction raises the ceiling. *Proof:* erfc is strictly decreasing; Monte Carlo of the closed form within 5% (`theory/meq_checks/scale_free_checks.py`, §6). Not implied: that stress strengthens a system, which needs an adaptation rule (redesign runs on tens of the slowest scale, B.9) and stops at B_min (CT22); that is K7, open. Coarse-graining rules (pooling cools, z′ = z√(N/(1+(N−1)ρ)) up to z/√ρ; the weakest link heats, z′ ≈ √(z² − ln N)) are in `theory/MATH_ATTACK.md`, numerical, not proved here.

**Lemma B9 (Theorem L, survival versus cost).** *Reserve income y with noise s₀; a check costs c every τ; squared-error loss w·e² accrues between checks; diffusion approximation, ruin checked at cycle ends.* (L1) P_ruin ≤ e^{−ϑB}, with ϑ the Lundberg root of E e^{−ϑΔ} = 1 for the cycle increment Δ. (L2) The survival-optimal interval is shorter than the cost-optimal one, because the loss variance grows like τ³; they agree when the reserve's own noise dominates. (L3) The survival-optimal interval does not depend on B, and the marginal value of raising ϑ, ∝ B·e^{−ϑB}, peaks at **ϑB = 1**. So rule 7's "watch most where shocks are large relative to buffers" holds for the value of extra effort, not for the cost-optimal interval. **Correction (v2.1):** the survival-optimal interval reduces to the cost-optimal (EOQ) one when the reserve's own noise dominates (policy-insensitive variance; checked: 0.314 against 0.316), not when the buffer is large. That the expected-cost rules are exact for a large enough buffer is a different statement, CT22. Cramér–Lundberg is known (Asmussen & Albrecher 2010). `theory/GENERAL_THEOREM.md` §5, `c3c`.

**Lemma B10 (finite horizon).** If a blind structure's reserve increments have conditional mean ≤ −δ < 0 and centred increments bounded by b, then P(it survives to T) ≤ exp(−(δT − B)²/(2b²T)) for T > B/δ (Azuma–Hoeffding). CLAIM_MAP N33.

**Lemma B11 (the internal-model bound).** The forecast miss of a memory equals the predictive information it fails to carry, δ = I(Past; Fut) − I(M; Fut). With causal states separated by γ_L, P(the memory's decoded state ≠ the world's causal state) ≤ √(2δ)/γ_L, and a solvent agent's memory must nearly copy the world's causal states. Parts are probably folklore (Shalizi & Crutchfield at δ = 0). `theory/INTERNAL_MODEL.md` §2. Self-checked only.

### B.7 How far one tracker reaches

**CT19 (LAT-1).** *W-b; a tracker at distance L from its target receives each reading after latency ℓ = L/v and holds the last value; reads every T.* Its mean squared error is (1/T)∫₀^T q(ℓ + s)^{α−1} ds ≥ q·ℓ^{α−1}, with the bound approached as T → 0. So a tolerable error D\* can be held only if q·ℓ^{α−1} ≤ D\*, i.e. L ≤ **L_max = v·(D\*/q)^{1/(α−1)}**.

*Proof.* At use, the held value is ℓ + s old, where s ∈ [0, T) is the time since the last arrival, so its error is q(ℓ + s)^{α−1} ≥ q·ℓ^{α−1}. Averaging preserves the bound, and reading more often only removes the s part. Inverting q(L/v)^{α−1} ≤ D\* gives L_max. ∎

*The three shortcut cases.* (a) **None:** v is light speed, and beyond L_max a system must federate. (b) **Finite shortcuts**, each spanning at most Λ_hop at hop latency at least τ_hop: a path covering distance D with n hops and light-speed travel time t_light has D ≤ n·Λ_hop + (light speed)·t_light and latency ≥ n·τ_hop + t_light, so its effective speed is at most max(Λ_hop/τ_hop, light speed), and LAT-1 holds with that v. (c) **Open shortcuts**, any point to any other at fixed latency: latency no longer grows with distance, so there is no distance limit, and CT16 decides the design. The theory does not say which case nature provides, and does not claim that shortcuts exist. Prior art in substance: Simon 1962; Tatikonda & Mitter 2004; consistency-latency trade-offs (Abadi 2012). `theory/SCALE_ENDS.md` §5; `theory/WORMHOLES.md` §4b. The real-system form is CLAIM_MAP N27 (open).

### B.8 Scale

**Lemma B12 (Theorem S, covariance and its limits).** (S1) If the objective is homogeneous of degree 1 in one currency, rescaling every cost leaves the optimum unchanged; (S2) rescaling time rescales optimal frequencies. (S3) With loss w|e|^p and self-similar drift e ∼ σ·t^H, the optimal interval is T\* = [c(pH + 1)/(pH·m_p·w·σ^p)]^{1/(1+pH)}: its exponents depend only on (p, H), not on the currency. (S4) Covariance fails when two cost components scale differently with size or currency; the optimum then shows crossovers, not one power. Proofs: S1–S2 by substitution, S3 by the first-order condition, S4 by example (a fixed plus a size-proportional read cost slides the local exponent from −1 to −½). That real systems sit in the generic class (p = 2, H = ½, by Taylor expansion and the central limit theorem) is a conjecture. `theory/GENERAL_THEOREM.md` §6, `c5a`–`c5c`.

### B.9 The master equation: the Master Theorem

The derivations, checks and worked example are in `theory/MASTER_EQUATION.md`; the review that produced them (a separate executor, same bot family) is `reviews/master-equation_2026-11-19/REVIEW.md`. **New, proved here or in the cited notes; not yet independently reviewed as a whole. CT24 and CT25 are new in v2.2 and likewise unreviewed.**

*Setting 𝓜_LG.* World exogenous (g = 0): a zero-mean Gaussian process, stationary with spectral density S(ω) or with stationary increments, observed through white noise of density N > 0 or read exactly at price c. Design 𝒟 = (K; an LTI estimator realizable with K first-order stores whose rates lie in a compact set [b_min, b_max]; read rates f_k ∈ [0, F]; a sharing graph). Costs h > 0, c_k ≥ 0, κ ≥ 0, w > 0 in one currency; squared error at lead k ≥ 0. Ruin as in Lemma B9's diffusion reserve, imposed through the Lundberg bound θ(𝒟) ≥ ln(1/ε_r)/B, a sufficient condition.

**CT20 (existence; monotone comparative statics).** (i) If any design is feasible, a minimizer exists, and K\* ≤ J(𝒟₁)/h for any feasible one-layer 𝒟₁. (ii) For every world and every loss, with E_K the least expected loss over nested design classes, K\* is nondecreasing in w/h; for one layer whose error grows with the age of its reading, f\* is nondecreasing in w/c.

*Proof.* (i) J ≥ h·K, so only finitely many K can beat 𝒟₁; for each K, J is continuous on a compact parameter set (Weierstrass). Without the compact rate set the infimum may only be approached. (ii) −J = −h·K − w·E_K has increasing differences in (K, w/h) because E_K is nonincreasing in K; Topkis (1978) and Milgrom & Shannon (1994) apply. Likewise −J(f) = −c·f − w·Ē(1/f) with Ē(1/f) decreasing in f. ∎ Check: K\* = 1, 1, 1, 2, 2, 2 at R = 1 … 1000 (`meq_derive.py`).

**CT21 (layers; L1–L3).** *Model S: s = Σ_j independent OU modes (rates a_j, variances v_j), the random walk as the a → 0 limit; noisy sensing; J_K = h·K + w·E_K; R = w·E_∞/h; Δ_K = E_K/E_∞ − 1.* (L1) One pole (one OU mode or a random walk): E_1 = E_∞ at every lead, so K\* = 1 at every w, h. (L2) J modes with distinct rates: the MMSE predictor has degree ≤ J at every lead, so K\* ≤ J; at k = 0 its degree is exactly J, so K\* = J for R large enough; layers beat flat iff R > R\* = min_K (K−1)/(Δ₁ − Δ_K). (L3) A non-rational spectrum (fBm with H ≠ ½, a continuous mixture of time scales) has E_K > E_∞ for every finite K; if also E_K → E_∞, K\*(R) → ∞.

*Proof.* (L1) The Kalman–Bucy filter of a scalar first-order state is one exponential store. (L2) Factor S + N = N·Π(ω² + b_j²)/Π(ω² + a_j²); P(−a_k²) ≠ 0, so no b equals an a, and the Wiener filter H = 1 − √N/G⁺ has no pole–zero cancellation: degree exactly J; the causal MMSE estimator is unique. (L3) If H were rational, G⁺ and so S + N would be rational. Full proofs and numerics: `theory/LAYERS.md` §2. ∎ The content of L1 is KNOWN (Kalman–Bucy 1961); L3 restates "finitely many stores are exact iff the spectrum is rational" (KNOWN). Each layer's time constant is 1/b_j, set by its mode **and** the noise, and faster than the mode.

**CL12 (L4, geometric clocks at every α).** Items with natural intervals log-uniform, K shared clocks over contiguous log-bands, penalty p(u) = [(α−1)e^{−u} + e^{(α−1)u}]/α − 1 (CT13): equal log-widths are optimal for every α in (1, 3). *Proof:* p is strictly convex, so a band's cost ψ(Δ) is strictly convex in its width (envelope theorem), and Jensen gives equal widths. `theory/LAYERS.md` Proposition L4; `theory/layers_checks/t7b_alpha.out`. Not the store model, where spacing is only roughly logarithmic.

**CT22 (survival; the price of survival).** Let θ(𝒟) be the Lundberg exponent, B_min = ln(1/ε_r)/max_𝒟 θ and B_slack = ln(1/ε_r)/θ(𝒟_E), with 𝒟_E the expected-cost optimum. For B < B_min no design is feasible. For B ≥ B_slack the constraint is slack and 𝒟_E is optimal (multiplier μ_s = 0). In between the constraint binds with μ_s = −m′/θ′ > 0, the marginal expected cost of survival exponent, and the design lies between 𝒟_E and the survival-optimal design of Lemma B9 (the μ_s → ∞ end). *Proof:* the constraint set grows with B; KKT. Check (Lemma B9 setting, ε_r = 10⁻³): B_min = 0.486, B_slack = 0.508, and τ\* moves 0.267 → 0.299 → 0.310 → EOQ 0.316 as B goes 0.49 → 0.508; μ_s = 0.0052 per unit θ at B = 0.5. μ_s carries the system's own units. Risk-sensitive control has the same direction (Jacobson 1973).

**CT23 (local regret).** If J is C² in log design variables with a nondegenerate minimum and the design is computed from a picture of the world off by δ in log parameters, the design error is O(δ) and the regret is ½δᵀHδ + o(δ²). For one layer, misjudging drift by a factor m costs exactly [(α−1)m^{−1/α} + m^{(α−1)/α}]/α − 1 ≈ (α−1)(ln m)²/(2α²): 3.8% at α = 1.3 and 6.1% at α = 2 for m = 2. *Proof:* implicit-function and envelope theorems. **Exceptions:** a wrong layered design can be worse than no layering (7.0% against 2.2%); fitting α far from the decision's scales (up to 29%); and near feasibility edges (B_min, the lookup cliff) regret is not smooth, so a picture error can flip survival. A missing cost term is not a perturbation and has no such bound.

**Dynamics (elementary; predictions N54, N55).** Estimating the slowest rate a to relative precision δ needs a record of about 2/(aδ²) of that time scale (Monte Carlo: records of 10, 30, 100 slowest time constants give 0.55, 0.30, 0.15), so redesign runs on tens of the slowest tracked scale (two-time-scale learning, Borkar 1997). The relative curvature of J in ln T at the optimum is exactly α − 1, so under noisy selection balanced against it the spread of ln(read interval) scales as 1/√(α − 1); that premise is standard for stabilizing selection and not derived for a specific selection model. Rates re-tune smoothly; K changes only at thresholds, with hysteresis under switching costs (Dixit 1989).

**Dimensionless groups.** Scaling time by T₀ = (c/(w·q))^{1/α} and cost by J₁ = c^{(α−1)/α}(w·q)^{1/α}, a parametric world's design is fixed by about 5–7 groups: the spectrum's shape, h/J₁, ℓ/T₀, μu/J₁, y/J₁, θB, and (N, ρ). Equal groups give the same design up to units (Theorem S); a general world's shape is a whole function. `theory/meq_checks/part2.out`. With the same R and mode ratio but a noise share of 0.005, 0.05 and 0.5, R\* is 135, 45 and 21, so the shape carries extra groups.

**CT24 (cost shares and the currency-free accounting; proved in a model).** *Setting of CT12 (hold-last-value, exact reset reads, J(T) = c/T + w·q·T^{α−1}/α, 1 < α < 3).* The optimum is T\* = T₀(α/(α−1))^{1/α} and J\*/J₁ = (α/(α−1))^{1−1/α}, functions of α alone. J is degree-1 homogeneous in (c, w), so the optimum is invariant under any rescaling of the currency, and by the envelope theorem ∂ ln J\*/∂ ln c = (c/T\*)/J\* = (α−1)/α and ∂ ln J\*/∂ ln w = 1/α; they sum to 1 (Euler). Hence (spend on reads) : (cost of error) = α − 1. *Shadow price:* minimizing mean error subject to c/T ≤ B gives T = c/B; its multiplier λ = −de\*/dB satisfies λ·w = 1 when w is the stake that makes T\* = c/B optimal, and with several trackers under one budget the marginal error saved per currency unit is equal across them (KKT). *Floor:* with c = β·kT per nat, J\*(β)/J\*(1) = β^{(α−1)/α} (σ√(2βkT·w) at α = 2) and the shares are independent of β; J\* is nondecreasing in every price (envelope), so any actual price ≥ kT gives J\* ≥ the CT7 floor. Checked to 10⁻⁷ across 18 decades of currency (`theory/meq_checks/scale_free_checks.py`). It does not give the same numbers across systems (the world's shape and S4 still differ), and it makes no claim that any system pays in joules.

---

## Appendix C. Claim index

Every numbered result, with its status (as in `measurement/CLAIM_MAP_v2.md` section O), the row that carries it in the tally, and where its derivation and checks live. `tools/check_consistency.py` fails if an ID here is missing from CLAIM_MAP section O or has a different status there.

| ID | Result | In the main text | Status | Counted row | Derivation; checks |
|---|---|---|---|---|---|
| CT1 | P0 persistence bound | §5, Result 1 | PROVED (in-model) | CT1 | `theory/GENERAL_THEOREM.md` §2; `theory/theorem-v2-checks/c6_persistence_bound.py` |
| CT2 | P1 when a model is necessary (strict) | §5, Result 1 | PROVED (in-model) | CT2 | GENERAL_THEOREM §2 and its 19 Nov erratum; `c7_rules_counterexamples.py` (c7d) |
| CT3 | P2 lead-time cap | §5, Result 1 | PROVED (in-model) | CT3 | GENERAL_THEOREM §2; c6a |
| CT4 | P3 the first bit must pay | §5, Result 1 | PROVED (in-model) | CT4 | GENERAL_THEOREM §2; c6d; `theory/core_checks/core_checks.py` |
| CT5 | E1 no decision, no model | §1, §5 | PROVED (in-model) | N25 | `theory/SCALE_ENDS.md` E1 |
| CT6 | I5 upkeep is a flow | §3 | PROVED (in-model) | CT6 | `theory/INTERNAL_MODEL.md` §2; `i2_maintenance_sdpi.py` |
| CT7 | O1 tracking floor | §3 | PROVED (in-model) | CT7 | `theory/MATH_ATTACK.md` §1.2; `objective_checks.out`; core_checks |
| CT8 | G1 staleness is monotone | §7 | PROVED (in-model) | K6 | GENERAL_THEOREM §3; c1a |
| CT9 | G2 hold or fade | §5, Result 2 | PROVED (in-model) | CT9 | GENERAL_THEOREM §3; c1b, c1d; core_checks |
| CT10 | G4 effort rises with stakes | §5 | PROVED (in-model) | CT10 | GENERAL_THEOREM §3; c1c |
| CT11 | T8 freeze, hold or look up | §5 | PROVED (in-model) | F13 | `reviews/night1/formal/THEOREMS.md` Thm 8; `reviews/night1/formal/checks/s5_phase.py`; core_checks |
| CT12 | Read-rate rule | §5, Result 3 | PROVED (in-model) | N7 | formal Lemma 1(i); `s1_classes.py`; core_checks |
| CT13 | T1c robustness | §5 | PROVED (in-model) | M3 | `measurement/FRAMEWORK.md` §3.10; core_checks |
| CT14 | Pooling onset | §6, Result 4 | PROVED (in-model) | B2 | formal Thm 1; `s2_onset.py`, `s9_attack.py`; core_checks |
| CT15 | The level's technology sets the exponent | §6, Result 4 | MATH-CORRECTED (exponent stands; scope narrowed) | N12 | `reviews/night2/N12_REFEREE.md`; core_checks |
| CT16 | Telling price | §6, Result 4 | PROVED (in-model) | CT16 | `theory/WORMHOLES.md` §2; `theory/reach_checks/independent_review_checks.py`; core_checks |
| CT17 | One clock, and the externality | §6, Result 5 | PROVED (in-model) | CT17 | `theory/MATH_ATTACK.md` §3.4; core_checks |
| CT18 | Temperature identity | §5 | PROVED (in-model) | CT18 | `theory/MATH_ATTACK.md` §2; GENERAL_THEOREM R0; core_checks |
| CT19 | LAT-1 and the three shortcut cases | §6, Result 6 | PROVED (in-model) | CT19 | `theory/SCALE_ENDS.md` §5; `theory/WORMHOLES.md` §4b; core_checks |
| CL1 | Lemma B1: G3 rise, then fall; the cliff | §5 | PROVED (in-model) | CL1 | GENERAL_THEOREM §3; c1e |
| CL2 | Lemma B9: Theorem L | §5 | PROVED (in-model) | CL2 | GENERAL_THEOREM §5; c3c |
| CL3 | Lemma B12: Theorem S | §3 | PROVED (in-model) | CL3 | GENERAL_THEOREM §6; c5a–c5c |
| CL4 | Lemma B8: exact per-window ruin (Black & Cox) | §5 | PRIOR ART | CL4 | GENERAL_THEOREM R1–R2; core_checks (Monte Carlo) |
| CL5 | Lemma B4: vigilance at birth | §6 | PROVED (in-model) | E7 | formal Thm 5 and its 19 Nov erratum; `s11_vclosed.py` |
| CL6 | Lemma B5: clocks | §6 | PRIOR ART | F14 | formal Prop 9; `s7_misc.py` |
| CL7 | Lemma B6: selection resolution | §4 | PROVED (in-model) | F15 | formal Prop 10; `s7_misc.py` |
| CL8 | Lemma B7: √N fade | §6 | PRIOR ART | K9 | `theory/THEOREMS.md` T4 |
| CL9 | Lemma B10: finite horizon | §5 | PROVED (in-model) | N33 | `theory/BOOKENDS.md`; `finite_horizon.py` |
| CL10 | Lemma B11: the internal-model bound | §5 | PROVED (in-model) | CL10 | `theory/INTERNAL_MODEL.md` §2; `i1_internal_model.py` |
| CL11 | Drift reduction as a lever | §3 | OPEN | K17 | `reference/THEORY_v1.4.29.md` §5 |
| CX1 | Theorem P for drifting worlds | §5, §8 | OPEN | CX1 | `theory/INTERNAL_MODEL.md` §4 (partial bridge) |
| CT20 | Master Theorem (i)–(ii): existence; K\* nondecreasing in w/h and f\* in w/c in every world | §5 | PROVED (in-model) | CT20 | B.9; `theory/MASTER_EQUATION.md` §1; `theory/meq_checks/meq_derive.py` |
| CT21 | L1–L3: one pole ⇒ one layer; J modes ⇒ at most J, exactly J past R\*; no finite design for a continuum | §5, §6 | PROVED (in-model) | CT21 | `theory/LAYERS.md` §2; `theory/layers_checks/`; meq_derive |
| CT22 | Survival lemma: B_min, B_slack, the price of survival μ_s | §5 | PROVED (in-model) | CT22 | B.9; `theory/meq_checks/meq_checks.py` S4; meq_derive |
| CT23 | Local regret: picture errors cost second-order regret, except near cliffs | §4 | PROVED (in-model) | CT23 | B.9; `theory/meq_checks/part2.py` (k); meq_derive |
| CT24 | Cost shares equal price elasticities and sum to 1; one tracker: reads : error = α − 1; shadow-price reading; floor multiplier β^{(α−1)/α} | §3, §5 | PROVED (in-model) | CT24 | B.9; `theory/meq_checks/scale_free_checks.py` |
| CT25 | Temperature as the ruin constraint: B ≥ z_ε·σ√τ; survivable shock ∝ τ^{−1/2} | §5 | PROVED (in-model) | CT25 | B.6; `theory/meq_checks/scale_free_checks.py` §6 |
| CL12 | L4: geometric clocks optimal at every α (shared-clock model) | §6 | PROVED (in-model) | CL12 | `theory/LAYERS.md` L4; `theory/layers_checks/t7b_alpha.py` |
| CL13 | Formal Theorem 6: levels are complements, a lattice, accrete as upkeep falls | §6 | PROVED (in-model) | F1 | `reviews/night1/formal/THEOREMS.md` Thm 6; `s4_lattice.out` |
| CL14 | Cheap lookup can dissolve levels (Theorem 6 counterexample) | §6 | PROVED (in-model) | F3 | formal Thm 6; `s4_lattice.out` |
| CL15 | Formal Theorem 7: levels fill top-down iff χ < χ\* (h = 0) | §6 | PROVED (in-model) | F7 | formal Thm 7; `s6_depth.out` |
| CL16 | T7: the architecture inherits the world's scale structure; the store count | §6 | MATH-CORRECTED | K12 | `theory/THEOREMS.md` T7; `reference/THEORY_v1.4.29.md` §2.2 |
| CL17 | Broadcast threshold (formal Theorem 2) | §5, §6 | PROVED (in-model) | B12 | formal Thm 2; `s8_broadcast.out`; meq_derive |
| CX2 | Coupled levels: when system and world co-adapt, do they settle at a joint minimum, cycle or race | §3, §9 | OPEN | CX2 | `reviews/master-equation_2026-11-19/REVIEW.md` §4 |
| CX3 | Federation pays iff Σᵢ Jᵢ\* + J_coupling < J\* of one flat tracker | §9 | OPEN | CX3 | `reviews/audit_2026-11-19/AUDIT.md` §1 |
| CX4 | Beyond linear-Gaussian, layers are the components of the world's predictive state worth their upkeep | §9 | OPEN | CX4 | `reviews/audit_2026-11-19/AUDIT.md` §1 |
| CX5 | A system's internal prices (w, h, c) equal the multipliers of its own binding budgets | §5 | OPEN | CX5 | `reviews/audit_2026-11-19/AUDIT.md` §2 |

Lemma B3 (opposite effects of shared and private drift) is CLAIM_MAP C1, Lemma B2 (the spectrum map) is the rows of `reference/THEORY_v1.4.29.md` §2.2, and the empirical claims of §4 and §6–§8 are CLAIM_MAP N13, J6, J9, J15, J16, N27, N51, N52, N57, K4 and K7.
