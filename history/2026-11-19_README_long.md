# A Theory of Adaptive Organization (GTAO)

Author: Chad Mitchell — X: [@torusflow](https://x.com/torusflow). *Public working draft since 18 November 2026. Not peer reviewed, not independently reviewed as a whole, not a published paper. Public domain (CC0).*

## Judgment: staying alive under the second law

One principle runs from atoms to cities: the second law. Total disorder rises; local order can grow only by pushing disorder out somewhere else. Broadly, things last in one of three ways:

| Way to last | What it pays | Does a model of the world pay? | Examples |
|---|---|---|---|
| **Keep** (frozen) | Nothing: it sits in a state almost nothing can knock loose | **No.** Nothing it does changes whether it lasts, so a model would cost something and buy nothing (CLAIM_MAP N25, PROVED (in-model); partly definitional) | Atoms, crystals, a virus particle; at the extreme, a black hole: the most memory physics allows for its size, almost none of it readable (N26, PROVED (in-model), conditional) |
| **Hold** (self-regulating) | A steady flow of energy | **No.** It regulates itself (in a star: self-regulating fusion, convection, dynamos, layered composition) but anticipates nothing outside | Stars, flames, hurricanes |
| **Know** (tracks) | A flow of energy *and* the cost of staying matched to a world that changes and can ruin it | **Yes, once acting late is costly.** Then carrying a model and acting ahead can pay | Cells, immune systems, ant colonies, people, firms, cities |

A knower can't wait for the world to arrive. Once acting late is costly, it can pay to carry a model and act ahead. **That is judgment: not a new physical principle, but a way of staying alive under the old one.**

**The bill.** Every knower pays one budget in three parts, plus the risk of ruin: (1) holding memory, (2) being wrong, including being late, and (3) the reads and effort that keep the memory fresh. Only the currency changes: heat in a cell, attention in a person, money in a firm.

**The bet.** Where selection is strong and a choice depends on a drifting world, the designs that last sit near the cheapest way to pay that bill, and the same relations (not the same constants) hold from cells to cities once the inputs are measured on each system. From the bill come [seven design rules for building an efficient self-maintaining system](#how-to-build-one), a few formulas you can compute, and [predictions that can fail](#predictions-and-how-it-dies). The bet is **untested, not refuted**.

GTAO adds no new physics, and no proof in its formal layer depends on the second law (`THEORY.md` §2.3). Much of its mathematics is known and credited; what may be its own is the assembly, one budget priced the same way at every level, and a preregistered program to break it across scales ([status](#status-prior-art-and-evidence)). It is a theory, not a law, and **not a theory of everything**: it says nothing about what an organization wants, only what it must pay to keep tracking a world while it pursues it. The canonical statement is [`THEORY.md`](THEORY.md).

### The physics, and where it stops

That law, together with gravity, the speed of light, quantum physics and the universe's low-entropy start, sets the stage. Information has a thermodynamic floor: erasing one bit releases at least kT ln 2 of heat on average (Landauer). For a driven system that meets their conditions, memory that does not predict the driving signal sets a floor on dissipation (Still, Sivak, Bell & Crooks 2012); in information terms the memory-versus-prediction tradeoff has the form of the information bottleneck (Tishby, Pereira & Bialek 1999). For a cell these floors are a real constraint (adaptation is necessarily dissipative: Lan et al. 2012). For neurons, people and firms they are literal floors but do not bind: a chemical synapse already pays about 10⁵–10⁶ times kT ln 2 per bit (Laughlin, de Ruyter van Steveninck & Anderson 1998), and for a firm the floor sits far below what memory costs in salaries and attention. There the exponents come from information theory and competition, not from heat, and the bet is that the same tradeoff still shapes efficient design, paid in time and money (`THEORY.md` §2.3). A knower can also pay to make its world change less (homeostasis, buffers, contracts), and that substitutes for watching (`THEORY.md` §5). The full picture, from chemistry to heat death, is [`theory/BOOKENDS.md`](theory/BOOKENDS.md) §1.

## How to build one

Yes, you can design from it, inside the model. Minimizing the bill gives seven rules for an efficient self-maintaining system, whether it is a team, a firm, a memory for an AI agent or a sensor network. Taken one by one each rule is prior art; they are listed because one budget produces all of them, and because each has a stated condition under which it fails (`THEORY.md` §3; `theory/MATH_ATTACK.md` §1.4; `theory/GENERAL_THEOREM.md`).

| # | Rule, in plain words | Status (closest prior art) | Fails when |
|---|---|---|---|
| 1 | **Act early.** Return what matters while there is still time to act. Interrupt unasked only when stake × chance it's relevant, plus what the outcome would teach, beats the cost of interrupting. | Near-tautology (Howard 1966; Denrell & March 2001) | Myopic interrupts (counterexample in the Theorem G notes) |
| 2 | **Keep what pays, fade the rest, recoverably.** Keep a fact while chance it's needed × cost of missing it beats the upkeep of keeping it current, which rises with how fast it drifts. | PROOF (T1a/T5b) (Anderson & Schooler 1991; McNamara & Houston 1987; Lee, Flack & Krakauer 2024) | Where the world has α ≠ 2 the optimal forgetting kernel is not exponential (tail τ^{−(1+α/2)}, §2.2); the need hazard is a different object |
| 3 | **Move a belief by the reliability of the signal.** A trusted correction replaces it; a secondhand or inferred one moves it partway. | KNOWN (Kalman 1960; Muth 1960) | Heavy-tailed noise (Cauchy counterexample) |
| 4 | **Keep prior versions until a correction proves out.** Frozen history is nearly free; a wrong overwrite costs more than the version it saved. | Near-tautology (append-only logs; Bateson 1963) | — |
| 5 | **Act from the current model, not a copy.** A copy's error grows with its hops and with drift since the source was last checked; recheck when that is too big for the stakes. | PROOF for Markov (α = 2) states (Bailis et al. 2012; Demers et al. 1987) | Non-Markov observed variables (seasonality) |
| 6 | **Record whether each prediction was used, ignored or late.** Without outcomes nothing learns what to return; use strengthens, disuse fades. | Weak (value of information ≥ 0) (Hebb 1949; stigmergy; Lee, Flack & Krakauer 2024) | The *mechanism* does not follow from the budget; "no one in charge" is narrowed (§6) |
| 7 | **Watch more as drift × stakes rises.** Watch most where shocks are large relative to buffers but not overwhelming; slow, low-stakes facts get almost none, and with any bounded fallback, effort collapses past a point (N5 in `THEORY.md` §1). | PROOF in two cases (Reis 2006; Sims 2003; Cho & Garcia-Molina 2003) | The interior peak holds only for fixed-delay fixing |

Two more results set the edges of the rules. **Freeze or hold:** freeze (stop refreshing, keep the copy) when the world barely drifts and storage is cheap (PROOF, Theorem G; Bateson 1963; Waddington 1953). **Not everything needs a model:** "every system pays for a model" **fails** as stated, because a blind bet-hedging population can beat sensing (Kussell & Leibler 2005); it holds only with the population redefined as the agent. That is why the bet is narrowed to strongly selected systems where a choice depends on a drifting world.

### The formulas you can build with

Each is labeled with its status, its premises and where it is derived. "In-model" means proved inside the model, not shown in real systems.

- **Whether to carry a model at all:** pay for one only if the loss from acting late exceeds its upkeep. [Elementary; close to value-of-information and economic-order-quantity accounting, and may be known; `THEORY.md` §1.]
- **When to share a model (T3a):** once enough members face a common driver, a shared level pays: at zero upkeep, **N > N\*(ρ) = (√(1+ρ)+1)²/ρ** (≈ 4/ρ for small ρ) is sufficient, where ρ is shared over private drift. With a price d for telling a member and c for a read, sharing the common part pays when **d/c < 1/N\*(ρ) − 1/N**, which is T3a at d = 0. [PROOF in-model, a sufficient condition, not a cutoff; `THEORY.md` §1 N2, §6; `theory/WORMHOLES.md` §2, CLAIM_MAP N41.]
- **Freeze, hold or look up (Theorem G):** a checked copy beats letting a fact fade only when **drift × check cost < Φ**, the value the fact adds to decisions (Φ = 0 when no action's payoff depends on the world). Facts that barely drift are frozen; facts that drift fast, or are cheap to look up, are looked up when needed; checked holding pays only in the band between, and the band need not exist. [PROOF in-model; Theorem G, T8; CLAIM_MAP F13; `THEORY.md` §3, §2.5.]
- **How often to look:** for a world whose change has spectral slope α (power falls as frequency^−α), with exact reset reads and squared-error loss, **read rate ∝ (stakes·drift/price)^{1/α}**. At α = 2 (a Markov world) this is the familiar square-root rule (Kalman/Muth). Memory time ∝ (noise/drift level)^{1/α}; one memory store suffices only near α = 2, and elsewhere the number of stores grows with the span of timescales and with stakes over upkeep. The loss is an input: under absolute error at α = 2 the stakes and drift exponents are ⅔ and ⅓. [Known filtering and approximation mathematics plus a price on effort, credited; for a Gaussian world or the best linear tracker; `THEORY.md` §2.2.]
- **How far one tracker can reach (LAT-1):** with hold-last-value reads, a tracker holds a target only if q·(L/v)^{α−1} stays below its tolerable error D\*, so **L_max = v·(D\*/q)^{1/(α−1)}**, where v is the fastest signal path. With no shortcut v = c, and beyond L_max a system must federate (separate trackers, each with its own reads). If shortcuts existed the answer changes; see [Reach](#reach-from-atoms-to-the-cosmic-horizon). [Elementary bound; real-system form CLAIM_MAP N27 OPEN; `THEORY.md` §2.3; `theory/SCALE_ENDS.md` §5; `theory/WORMHOLES.md` §1, §4b.]
- **Who must be in charge:** no one, *when* keeping shared memory up is privately rewarded; otherwise expect shared fate or enforcement, usually both; shared fate is usually partial (Frank 1995; Ostrom). This narrows the earlier "no one in charge". [HYPOTHESIS; CLAIM_MAP J9 OPEN; `THEORY.md` §6.]

**A recipe, in-model:** measure the world your system tracks (α, drift level q, sensing noise, stakes, and the prices of holding, reading and telling); for each fact decide freeze, hold or look up; set read rates by the read-rate formula; share a model wherever N > N\*(ρ); federate beyond L_max; log every prediction's outcome. None of this has yet been shown to beat a simpler design in a real system: that is the open bet. One application is worked out for AI memory ([below](#applications-separate-from-the-theory)).

## Predictions, and how it dies

**The open bet:** strongly selected real systems sit near these optima once the inputs (α, drift level, sensing noise, stakes, prices) are measured on the same system, and the same relations (not the same constants) hold at every level, from cells to cities (CLAIM_MAP N13, J6, both OPEN). It dies if:
- in two or more strongly selected systems at different scales, the measured design misses its measured-input optimum by more than the measurement error allows, *and* a named rival (a fixed budget share; a universal ½) fits better; or, causally, design fails to move with a measured change in its inputs by the preregistered share (`THEORY.md` §1 N6, §9);
- a level's design needs a fourth kind of cost to be explained (J16; inside the model the same three costs at every level is an axiom, Axiom 5, so only real systems can test it);
- design does not respond to the measured prices of the three costs as the relations require (J6).

Optimality is claimed only where selection is strong. Below Lynch's drift barrier misses are expected, and that split must be fixed **before** a test, never used to explain a miss afterward (§7).

**Sharper predictions, each with its kill** (none has passed a locked, independently reviewed field test):

| Prediction | Status | How it dies |
|---|---|---|
| Look rate at a drifting quantity has stakes and drift elasticity 1/α, so it varies with the measured spectrum; the √ rule is the α = 2 case | Learned human sampling: CLAIM_MAP N51, OPEN (a lab test is specified in `reviews/lock_2026-11-18/LOOSE_ENDS.md` §1); selected systems: part of N13 | Elasticities at α = 1.5 and 2.5 not separated in the predicted direction, or both consistent with ½, at the preregistered power |
| Watching effort rises with drift, then collapses once any bounded fallback exists (a cliff, not a plateau) | PROOF in-model; core case known for web crawlers; cross-domain claim untested (`THEORY.md` §1 N5) | In a domain with a bounded fallback, update effort keeps rising through the top drift decile |
| A new shared level appears once group size exceeds N\*(ρ) | PROOF in-model, sufficient condition; the −1 case is prior art in substance (Veldkamp & Wolfers 2007; Van Zandt & Radner 2001); untested in the field (`THEORY.md` §1 N2) | Across groups, the size at which a shared layer appears does not move with ρ |
| √N fade of shared memory, with a sign flip: pooled deposits on a drifting target fade faster as √N; on a stable target, use preserves (Lieberman et al. 2007) | Mathematics prior art (Kalman averaging); application untested in the field: LANG1 failed on proxy "word-gain rate vs speaker population" (outside the theorem's domain), and an ant-like nonlinear readout failed in simulation (SIM-FAIL G15), so it is limited to linear readouts (`THEORY.md` §1 N1) | Across Austronesian languages, the log–log slope of word-gain rate on speaker population has a CI excluding 0.5 and including 0 or 1; or frequency effects on replacement do not differ in sign between drifting and stable referents |
| The central share of a tracker falls with q·ℓ^{α−1} (read lateness ℓ) | CLAIM_MAP N27, OPEN | At fixed q the central share does not depend on ℓ (`theory/SCALE_ENDS.md` §5) |
| Cheap lookup removes layers that hold shared facts, not layers that enforce; rules versus standards behave as freeze versus look up | CLAIM_MAP N52 and N53, both OPEN; partly prior art (Bloom et al. 2014; Kaplow 1992) | Kills in CLAIM_MAP |
| Stress strengthens a system up to a ceiling | CLAIM_MAP K7, OPEN | — |
| The 12 Nov post's lead prediction: slow error-fixers fail faster where shocks are large relative to buffers, risk ∝ shock × √(time to fix) ÷ buffer | Every sign right, but the τ-specific structure **failed on proxies** (CLAIM_MAP K4 PROXY-FAIL); the sign itself follows from dimensional analysis, and the exact form is Black & Cox 1976 | Already scored; kept on the board ([scoreboard](#test-scoreboard)) |

**The first real test** of the open bet (SAME-SYSTEM-AQN) is designed and not yet run (`STATUS.md`, `QUEUE.md`). Try to break it.

## Reach: from atoms to the cosmic horizon

The costs are physically priced, as floors, at every scale from atoms to the cosmic horizon. That is the author's scope choice of 18 November 2026, not a finding: no formal proof depends on it, and whether the physics does real work in the proofs is an open disagreement (`THEORY.md` §2.3). Above the cell the floors are literal but do not bind; there the exponents come from information theory and competition, not from heat. What changes along the scale is whether a model is worth carrying (`theory/SCALE_ENDS.md`, independently refereed, PASS-WITH-FIXES; CLAIM_MAP N25–N29):
- **Atoms** are frozen. A model would buy nothing (N25), though atoms still carry physical information (for example ln 4 nats of hyperfine spin).
- **Stars** are held with no model: they regulate themselves (self-regulating fusion, convection, dynamos, layered composition) but anticipate nothing outside.
- **Black holes** are the extreme of the frozen class: the most memory physics allows for their size, three readable numbers (mass, spin, charge), and, if evaporation is unitary (the Page-curve assumption; Hawking's original calculation says information never returns), the rest returned scrambled only after about the Page time, for every black hole that exists today (N26, PROVED (in-model) for such pre-Page-time holes; older holes rest on a conjecture). GTAO does not derive why black holes exist, the area law or the Page curve (N29 WITHDRAWN as framing).
- **Selected models** switch on only with heredity below Eigen's threshold, a world-dependent action, trackable drift and a first nat that pays (N28 OPEN); survival-relevant information and the simplest models (integral feedback) may come earlier.
- **Light delay, and what shortcuts would change** (`theory/WORMHOLES.md`; the shortcut cases are CONDITIONAL throughout):
  - **With no shortcut** faster than the outside light path, LAT-1 holds: L_max = c(D\*/q)^{1/(α−1)}, and beyond it large organizations federate. On Earth this is a latency cost; off-planet it is a hard cap (N27 OPEN; prior art Simon 1962, PACELC).
  - **A finite network of shortcuts** (a "tube map": throats of reach Λ, each hop costing a delay τ > 0) is a faster medium of effective speed v_eff ≤ Λ/τ. LAT-1 survives with c replaced by v_eff, so federation still happens, at a bigger size (`theory/WORMHOLES.md` §4b).
  - **Open shortcuts** (any mouth to any mouth in one hop, or zero-delay hops on a connected network) remove the distance limit. Then economics decides: with fully shared drift, central beats local at zero latency iff d/c < 1 − 1/N, so zero latency alone does not force one central tracker; throat capacity, reliability and causality also bind; private drift still federates; and if the world's drift speeds up as m^β when signals speed up by m, reach grows only if β < α − 1 (CLAIM_MAP N41, N47; PROVED (in-model) and conditional). The ceiling on any central store is the holographic bound; a store at that bound would be a black hole.
  - **Whether shortcuts exist is not something the theory predicts** (N46 WITHDRAWN as framing). The best-studied theoretical traversable wormholes, as far as their abstracts and introduction (as read for `theory/WORMHOLES.md`) show, do not beat the outside light path, and both live in anti-de Sitter space, not our universe: Gao, Jafferis & Wall (2016) find theirs "cannot be used to violate causality", and Maldacena, Stanford & Yang (2017) state that in general relativity "we cannot send a signal through the wormhole faster than we can send it through the outside". If that holds, LAT-1 is unchanged. The author's open-versus-finite split is the right first split for reach; whether to centralize turns on the further quantities above.
- **The cosmic horizon** caps memory at about 3×10¹²² nats and the price of erasing a bit at ≥ about 2×10⁻⁵³ J (Landauer's bound in a bath at the de Sitter temperature).
- **Viruses:** a virus particle is frozen and pays nothing, while an infected cell and the viral lineage are alive, so GTAO says a virus is alive as a lineage, not as a particle, and treats "alive" as a ledger of who pays for what. That is a restatement of published views (Forterre's virocell is the closest), with a common ledger (`theory/REACH.md` §1). The cosmic web, wormholes, the torus, dark matter and energy, and fractal time are worked in [`theory/REACH.md`](theory/REACH.md) and three companion notes; the theory makes no prediction that wormholes exist or about the shape of the universe.

## What changed since the 12 November post

The theory was first posted on X on 12 November 2026 ([archived copy](history/2026-11-12_X_POST.md)). The spine, the bill, the seven design rules and the locked predictions carried forward. What changed (full record: `THEORY.md` §13 and the CLAIM_MAP notes):
- **Atoms:** "nothing to maintain" is now "nothing an atom does changes whether it lasts, so a model would cost and buy nothing" (N25).
- **The bet is narrowed:** from "every self-maintaining system pays to keep a model" to strongly selected systems where a choice depends on a drifting world. The broad form fails against blind bet-hedging (Kussell & Leibler 2005).
- **The tracking math is credited as classical** (v1.4): the spectrum-to-design map is optimal filtering and approximation theory plus a price on effort, so it is no longer presented as new.
- **The ends of the scale** (atoms, stars, black holes) and the reach to the cosmic horizon are worked out, with light-delay federation stated as conditional on there being no shortcut.
- **The post's lead prediction** (risk ∝ shock × √(time to fix) ÷ buffer) got every sign right but failed on proxies in its τ-specific structure (K4 PROXY-FAIL); its exact form is Black & Cox 1976, and the post's "Merton" wording is superseded. Each design rule now carries its status and its failure condition.
- **Credit fixed:** the dissipation floor for non-predictive memory is Still, Sivak, Bell & Crooks 2012 (the post named three of the four authors).
- **Measurement first:** no field test so far measured the theory's quantities validly, so field results are "passed / failed on proxy X".

## Status, prior art and evidence

### Honest status

GTAO is a falsifiable causal theory. No Tier-1 test has run: there is no field pass and no field fail, so the theory is untested in the field, not refuted.
- No field test so far measured GTAO's quantities validly, so field results are "passed / failed on proxy X", not kills or confirmations (`measurement/`).
- The formal layer is proved in-model, with corrections ("V ≥ 2" is wrong as stated), and mostly builds on published team theory and inventory pooling. Its constants are functions of the world's drift spectrum (`THEORY.md` §2.5).
- The spectrum-to-design map is now derived and refereed (`reviews/night2/SPECTRUM_MAP_REFEREE.md`): it is classical, so it is no longer the headline. What remains open is whether real systems sit near it once its inputs are measured (`QUEUE.md`).

- **No field test so far measured the theory's quantities validly.** No Tier-1 test has run, so there is no field pass and no field fail. Field results are reported as "passed / failed on proxy X", not as kills or confirmations (`measurement/FRAMEWORK.md`).
- **The time-to-fix term (τ) failed on proxies** in the DECISIVE and F1 tests under the literal joint kill rule (CLAIM_MAP K4 PROXY-FAIL), though every sign was right; the sign itself follows from dimensional analysis, so it is not theory-specific. The scoreboard below has every test.
- **The validity gates MV1–MV10 are treated as binding** from 18 November 2026 for every new preregistration (Chad's instruction to proceed without his sign-off; CLAIM_MAP M2). MV9's external timestamp still needs the author's go for each lock.
- **The first real test** of the open bet (SAME-SYSTEM-AQN) is designed and not yet run (`STATUS.md`, `QUEUE.md`).

See `THEORY.md` (status block, §2.3, §2.5, §8b–8c) and `measurement/CLAIM_MAP_v2.md` (v2.49).

- **There is no new theorem of large scope.** Most individual rules are known results, placed side by side. The math notes label what is known, what is a calculation, and what fails. The one new proof worth keeping (a quantitative internal-model bound) is modest, and its novelty is unconfirmed.
- **This is a working hypothesis under test**, not a finding. Nothing here has been peer reviewed. An independent review of the DECISIVE and F1 tests is in `reviews/DECISIVE_F1_REVIEW.md` (14 November 2026, America/New_York); the scoreboard below follows its verdict. That review was not fully blind (the reviewer had the results and write-ups). Most other tests have not had an independent review.
- **Every review so far covered part of the work**, and every reviewer was an AI executor of the same family as the authors; `THEORY.md` has not been independently reviewed as a whole, and no human domain expert has reviewed it (`reviews/lock_2026-11-18/LOCK_AUDIT.md`, B1).
- The literature sweep (`litmap/`, 14 November 2026; not independently reviewed) is the basis for "already published" versus "looks new". It cannot rule out an obscure precursor.

### What is new, and what is not

| Layer | Status | Where |
|---|---|---|
| The spine and the keep / hold / know split | A framing. The three-class split is prior art in substance (Prigogine; Pross). Bookend rows are classifications, not predictions: no data could fail them | `theory/BOOKENDS.md`, `theory/SCALE_ENDS.md` |
| Design exponents from the world's drift spectrum | **Known mathematics**, assembled and credited. In a Markov world (α = 2) the square-root rules hold and one store suffices (Kalman/Muth; Mora & Nemenman 2019 for a sensing cell, whose world is a geometric random walk, so α = 2 holds for log-concentration; Lee, Flack & Krakauer 2024 as an application). In a scale-free world (α ≠ 2) the exponents become 1/α and its relatives, forgetting kernels have power-law tails, and the number of stores grows with log-span and log stakes/upkeep (Afterman et al. 2022; Nuzman & Poor 2000; Benna & Fusi 2016; and others). Holds for a Gaussian world or the best linear tracker; the Bayes tracker of a jump world can differ (N16) | `THEORY.md` §2.2, §10 |
| Model size across many modes (Regime C) | Model size ∝ Q^{1/β}, an interior minimum of the model's budget share iff β < 1, a minimum viable size from unstable modes: PROOF under stated assumptions with known tools; not reviewed by the spectrum-map referee | `THEORY.md` §2.2 |
| Levels, vigilance, freeze / hold / look up (the formal layer) | Proved in-model, with corrections ("V ≥ 2" is wrong as stated); mostly built on published team theory and inventory pooling | `THEORY.md` §2.5, §6, §8b |
| The ends of the scale | Atoms frozen (N25) and black holes as the frozen extreme (N26): PROVED (in-model), the first partly definitional, the second conditional on unitary evaporation and on counting lateness as error; the switch-on of selected models is a hypothesis (N28 OPEN) | `THEORY.md` §2.3 |
| A quantitative internal-model bound | PROOF; novelty unconfirmed, probably folklore | `theory/INTERNAL_MODEL.md` |
| **The open bet** | **Untested, not refuted** | CLAIM_MAP N13, J6 |

**There is no new theorem of large scope.** What may be this project's own is the assembly: one budget, priced the same way at every level, with one preregistered falsification program across scales.

### Already published (credited in `THEORY.md` §10)

- The design rules, taken one by one (decision theory, Kalman/Muth, append-only logs, stigmergy, inattention).
- **The square-root memory scaling** is Kalman/Muth filtering; for a sensing cell it is Mora & Nemenman 2019. Lee, Flack & Krakauer 2024 derive optimal memory ∝ τ_E^{1/2} with an energy cost (an application), and treat stigmergy as outsourced memory that invites free riders. The same √ form is in EOQ and inattention models (Reis 2006; Alvarez, Lippi & Paciello 2011).
- **The whole spectrum-to-design map:** fractional filtering (Afterman et al. 2022; Kleptsyna et al. 2020), fBm/ARFIMA prediction kernels (Nuzman & Poor 2000; Hosking 1981; Gatheral, Jaisson & Rosenbaum 2018), exponential-sum approximation (Jiang et al. 2017; Benna & Fusi 2016).
- **The "temperature"** (shock × √(time to fix) ÷ buffer) is the inverse of the textbook safety-stock factor (Silver, Pyke & Thomas). Its exact first-passage form is **Black & Cox's (1976)** default probability; Merton's terminal version is off by a factor of 2, and earlier "Merton" wording is superseded.
- **Layers and power-law forgetting:** Anderson & Schooler 1991; Fusi, Drew & Abbott 2005; Benna & Fusi 2016; Shankar & Howard 2013 (log-spaced memory is optimal for power-law signals); Brand's pace layers; Holling's panarchy.
- **The information and thermodynamic floors:** Mitter & Newton 2005; Horowitz & Sandberg 2014; Stratonovich's value of information; the data-rate theorems (Nair & Evans 2004; Tatikonda & Mitter 2004); Polani; Shalizi & Crutchfield 2001; Kussell & Leibler 2005.

<details>
<summary><b>What looked new in v1.0 (kept as history)</b></summary>


*This is the v1.0 list, kept as history. The current list of what looks like the theory's own is `THEORY.md` §8b; statuses are in `measurement/CLAIM_MAP_v2.md` (v2.49).*

Pending targeted searches, and none yet confirmed by a locked, reviewed test:

1. **√N fade of shared memory**, with a sign flip against Lieberman et al. 2007: pooled independent deposits make faster turnover optimal for drifting targets, while use preserves forms for stable ones. Untested.
2. **The T3a threshold** for when a new shared level pays: N > (√(1+ρ)+1)²/ρ. Untested.
3. **The fixed-spread sign:** at fixed observed spread, slower correctors cross boundaries *less* often (ε_τ = −1). The sign held; the size did not, and the literal joint kill fired. The independent review finds the sign itself follows from dimensional analysis, so it is not theory-specific.
4. **Geometric layers if and only if drift is scale-free (T7b)**, with level count ∝ (log-span)^(2/3). The locked test was inconclusive. *(Withdrawn in v1.4: replaced by a prior-art store-count form; CLAIM_MAP K12.)*
5. **Watching effort rises, then collapses** once any bounded fallback exists. Untested across domains.
6. **The spectrum-to-exponent relation** (the core hypothesis). The item-level news test P1 failed on proxy "headline-word recurrence as need" on 15 Nov 2026. *(v1.4: the relation is derived and is prior art, CLAIM_MAP K13; the open bet is measured-input optimality, N13.)*
7. **A quantitative internal-model bound** (solvent agents carry a near-copy of the world's causal states). Proved in-model and self-checked; novelty unconfirmed, probably folklore.

</details>

### Test scoreboard

Dates are America/New_York, 13–15 November 2026. For DECISIVE and F1, the verdicts below follow the independent review in `reviews/DECISIVE_F1_REVIEW.md`, not the tests' own more generous labels. Other tests follow their locked rules and have not had an independent review unless noted.

The preregistration commits for these tests lived only in local, unpushed git repos. Adding their histories to this repository (as `tests/<name>/history.bundle` where a bundle could be shipped without excluded data, and as `tests/<name>/history.txt` receipts for every test) gives them an **external timestamp only from 14 November 2026**. The author dates inside those histories are self-attested.

| Test | What it asked | Verdict (after review, where one exists) | Plain reading |
|---|---|---|---|
| **DECISIVE / banks** | Does slower correction raise failure risk at fixed shock and buffer? (7,837 banks, 2008–14) | **Sign-only, not a HIT; PROXY-FAIL (CLAIM_MAP H11)** | β = +0.20 [0.11, 0.29], ≈ 15% higher hazard per doubling; adds to the Z-score. The sign holds only for detrended τ; the specified own-mean τ is null. The exact identity, ε_B = −ε_σ and the horizon test all failed on this proxy. |
| **DECISIVE / glucose** | Fixed-spread sign (224 adults with type 1 diabetes) | **Sign right, size off; MATH_ATTACK literal joint kill fires on the full sample** | Slope −0.46 vs implied −0.82 and literal −1. Collapse across cohorts failed on proxy (CLAIM_MAP H12 PROXY-FAIL). The test's own prereg, scored against a lowered sampling-corrected target, does not kill; those targets rewrote the kill rule after MATH_ATTACK wrote it. The cold regime is not evaluable (n = 2). |
| **DECISIVE / populations** | Fixed-spread sign (274 GPDD series) | **MATH_ATTACK literal joint kill fires on any reading** | Slope −0.21 vs −0.34. Cold-regime slope has the wrong sign, where the theory says the effect should be strongest. The test's own prereg against the sampling-corrected target does not kill, but those targets rewrote the rule. The result is fragile (half the series are fur-harvest records; source fixed effects, taxon clustering, or dropping clipped series remove significance) and should not be cited as support. |
| **F1** | Same index on ≈ 4,100 US public firms | **Inconclusive; not a theory-specific hit** | All four directions held; the main link is published. τ mostly measures fixed-cost share (operating leverage), not correction speed, so construct validity fails. The novel interaction p = 0.055. Data prefer a τ weight near 1 over ½ (suggestive only). The prereg kill rules did not fire. |
| **C3** | Same index on 896 open-source projects | **Inconclusive / miss** | τ added nothing; the design could not have seen it. It rejects the reset-clock mechanism at that scale (predicted ≈ 11× per doubling, measured ≈ 1.0). |
| **BIO1** | Drift matching at biological scales (literature) | Kill not triggered; one contradiction | Holds, but almost entirely as prior art. The neural slope ≈ 1 comes from periodic switching, which v1.4 places outside the spectrum map. |
| **COLLAPSE1** | Memory time vs world time across substrates | Mixed (two proxy fails, weak passes) | The immune "contradiction" was largely a measurement-age artifact under power-law waning. Code re-edit need decays as a power law (≈ 0.6). |
| **MATCH1** | Need vs memory exponents in the same system; freeze-or-hold | Match **failed on proxy** (H2 PROXY-FAIL); freeze-or-hold **passed on proxy** "town-level measles recurrence" (H9 PROXY-PASS; substance prior art, Mayer et al. 2016); layer count inconclusive | News memory 0.24 vs need 0.71. Measles antibodies stay nearly flat (0.11) while measles-return odds fall at 2.15. Need exponents 0.6–0.8 replicate across code, Wikipedia and news. The redness correlation had the opposite sign to the prediction; v1.4: that prediction was mis-derived (CLAIM_MAP H19). |
| **DRIFT1** | Is drift scale-free? | Kill not triggered | City 311 looks scale-free; Wikipedia and filings have cadences. Supports T7 only as a conditional claim. A person-scale arm is withheld (`tests/DRIFT1/REDACTION.md`). |
| **ANTS1** | √N trail fade (simulation) | Finished 15 Nov; passes by construction (G13–G14 NOT EVIDENCE); three locked in-model failures (G15–G17 SIM-FAIL) | `reviews/night1/ANTS1_WRITEUP.md`; limits √N pooling to linear readouts |
| **C3b** | Exogenous shocks in open source | Not finished; the MV10 power gate is not met at the largest n the frame supplies, so it cannot give a verdict as preregistered (`reviews/night2/C3B_GATE_ADDENDUM.md`) | — |

**Overall (following the DECISIVE/F1 review):** the numbers reproduce and every sign is right. That is not enough. The τ (time-to-fix) term as a theory-specific claim **failed on these proxies** under MATH_ATTACK's literal joint kill rule (CLAIM_MAP K4 PROXY-FAIL): it fires for populations on any reading and for glucose on the full sample; banks are sign-only, not a hit. "Fewer crossings at fixed spread with slower correction" follows from dimensional analysis and standard first-passage results (Siegert 1951; Black–Cox 1976). The theory-specific structure — the −1 exponent, the √τ weighting, the identities, the τ-buffer interaction, and one collapse curve — failed on these proxies (H11–H15 PROXY-FAIL; out of scope for the structural core). F1's τ mostly measures fixed-cost share. The lowered sampling-corrected targets rewrote the kill rule after it was written; this scoreboard leads with the literal verdict. C3 rejected a fixed-clock version. Reading the missed exponents as "½ is the single-timescale special case of the spectrum relation" is post hoc and must be tested in its own right.

## Start here

**[`THEORY.md`](THEORY.md) is the one canonical statement of the theory (v2.0 draft, 19 November 2026, America/New_York).** Where anything else disagrees, it governs. [`STATUS.md`](STATUS.md) says where the work stands; [`QUEUE.md`](QUEUE.md) is the live work queue; [`BRIEF.md`](BRIEF.md) is a plain-words brief of the whole record, checked against the files; `measurement/FRAMEWORK.md` says how quantities are measured, and `measurement/CLAIM_MAP_v2.md` (v2.49) gives one status per claim. `python3 tools/check_consistency.py` checks versions, wording and claim statuses across these files. This README is a summary.

**Reading paths** (each about an hour):
- **Physicist:** `THEORY.md` §2.3 (where the physics is literal and where it is not) → `theory/SCALE_ENDS.md` → `theory/BOOKENDS.md` §2 → `theory/WORMHOLES.md`, `theory/COSMIC_WEB.md`. Expect classifications given published physics, not new physics.
- **Biologist:** `theory/BOOKENDS.md` §1 → `THEORY.md` §2.2 Regime A (the sensing case is Mora & Nemenman 2019) → `theory/REACH.md` §1–§2 (viruses, what counts as alive) → `prereg/SENSE-CELL/` (CLAIM_MAP N24).
- **Organization theorist or economist:** `THEORY.md` §6 (levels, shared memory, who is in charge) → §4 and §8 (failure risk, and the τ tests that failed on proxies) → §5 (reducing drift) → LAT-1 in §2.3. Closest prior art: Marschak & Radner 1972; Van Zandt & Radner 2001; Veldkamp & Wolfers 2007; Simon 1962.
- **Curious generalist:** `theory/BOOKENDS.md` §1 ("The picture in plain words") → the scoreboard below → `BRIEF.md`.
- **Skeptic:** `measurement/CLAIM_MAP_v2.md` (every WITHDRAWN and MATH-CORRECTED row) → `reviews/` → `reviews/lock_2026-11-18/LOCK_AUDIT.md`.
- **Process and loose ends:** `reviews/lock_2026-11-18/`: `LOCK_AUDIT.md` (lockable, not locked), `PROCESS.md` (how this project has worked, and its recurring mistakes), `LOOSE_ENDS.md` (second- and third-order implications, ranked; CLAIM_MAP N51–N53), `NARRATIVE.md`, and `INDEPENDENT_REVIEW.md` (same bot family).

## Repository layout

```
THEORY.md         The theory, v2.0 draft (start here)
STATUS.md         Where the work stands (rewritten, not appended)
BRIEF.md          Plain-words brief of the whole record, checked against the files
QUEUE.md, queue/  Live work queue and ledger
measurement/      FRAMEWORK (gates MV1–MV10, tiers, anti-rescue rule) and CLAIM_MAP_v2 (one status per claim)
tools/            check_consistency.py (versions, wording, statuses, tally, tables, review independence)
theory/           Theorem notes, the math attack, and their code checks
tests/            Preregistered tests: predictions, code, results (raw data excluded)
litmap/           Literature map, prior-art table, threats, and DOI verification
reviews/          Hostile and independent reviews (independence stated per file), and the lock audit
applications/     How this theory is applied (AI memory; Looper; ants) — no personal data
LICENSE.md        CC0 1.0: public domain, free for any use
```

## Applications (separate from the theory)

- **AI memory**, worked out as math and a toy simulation in the public repository [`Chad-Mitchell/adaptive-memory-levels`](https://github.com/Chad-Mitchell/adaptive-memory-levels). That repo is one application. It is not this theory, and its toy results are not evidence that the theory is true.
- **Looper** is a personal-assistant application of the same hypothesis. It is developed separately. This repository does not contain Looper code, store contents, or any personal data.
- **Video:** a new explainer is on hold while the theory is finalized. An earlier draft (v7) was removed on 18 November 2026; it is in Git history.
- **Ants:** the field-literature check is in BIO1; a code-ant simulation of the √N claim is ANTS1 (finished 15 Nov; `reviews/night1/ANTS1_WRITEUP.md`).

## How this should be read

Do not treat locked predictions as findings, and do not treat a support that is already in the literature as a new confirmation. Formal misses and inconclusives stay on the board. This repository is public as of 18 November 2026; posts and other outside acts still need the author's go.

- AI agents (Grok Bot; the author's assistant is named Ace) helped draft, compute and review these files under the author's direction. Every claim status is in `measurement/CLAIM_MAP_v2.md`.
- `tNNNN` tags are turn ids in the author's working log. Review and lock records dated before 18 November 2026 say "private" because the repository was private then.

## License

Public domain under CC0 1.0 (`LICENSE.md`): anyone may use, change and share any of this for any purpose, without asking or crediting.
