# CORE_AUDIT (night 1): the core causal claim, what it implies, a discriminating-predictions audit, prior-art closure, and tonight's tests

Sunday 2026-11-15, about 00:30–01:30 ET. Written by a Grok Bot executor for Chad (via Ace). Private working note.
Nothing was posted or sent. The Looper repo and the theory repo (`/workspace/theory-of-adaptive-organization`) were not touched.
New files: this document, `vigilance_check.py` with `vigilance_check.out` (a 1-second numerical check, §2.3), and `src/` (the Dessein–Galeotti–Santos PDF and its text; Geanakoplos–Milgrom was read through the fetch tool and not saved).

**Read for this audit:** the repo's `THEORY.md` (whole, including the §8 scoreboard), `theory/THEOREMS.md` §T3–T7; `theory-v3/SCALEFREE.md` and `PREDICTIONS.md`; `PROFOUND.md`; `profound/PROFOUND_v2.md`, `POOLING_REVIEW.md` and `PREREG_DRAFT.md` §0–1 plus headings; `theorem-v2/INTERNAL_MODEL_REVIEW.md` §0–1; `reviews/DECISIVE_F1_REVIEW.md` §0–2; `tests/LANG1/RESULTS.md`, `tests/MATCH1/RESULTS.md`, `tests/ANTS1/PREREG.md`, and the `theory-v3/prereg/p1_meeter_conditional.py` script. **Not re-read line by line:** BIO1, COLLAPSE1, DRIFT1, DECISIVE and F1 RESULTS (I used the repo's §8 summaries of them and the independent review), `GENERAL_THEOREM.md`, `MATH_ATTACK.md`, and the full INTERNAL_MODEL draft.

Labels: **KNOWN** (published by others), **DERIVED** (follows from the stated assumptions, with a check where noted), **HYPOTHESIS**, **POSTDICTION** (fits data already seen), **[R]** = a source I read this session, **[M]** = from memory, not re-read, **[PR]** = verified by an earlier reviewer in this project, as cited in the file named.

---

## 0. Bottom line

1. **The core claim is a mechanism, not a slogan.** Drift destroys the information an organization holds. Re-buying that information draws on a finite budget. Selection or learning keeps the ways of spending that budget that cost least overall. **So architecture (what is tracked, how fast, at which level, shared or private, frozen, held, handed to a fallback, or stabilized) is caused by the drift spectrum, the stakes, how widely each driver is shared, and the relative prices of sensing, storing and communicating. It is shaped to the resolution that selection allows.** (§1.1)
2. **None of the four kills hit that mechanism directly.** They hit sub-models (single-timescale failure rates, the √N mapping onto language, the strong news-exponent match), or they showed that failure data cannot test it. That is good news for the core and bad news for its record: **the core has not yet passed one discriminating test of its own.** Its two passes, measles freeze-or-hold and the need band, both have explanations that do not need GTAO. (§1.3)
3. **Discriminating-predictions audit, the honest result: today there is no prediction that only GTAO gets right against the best rival in every field.** In markets the best rival is the economics of information: value of information (VOI), rational inattention, team theory, EOQ. GTAO's math *is* that math, so it predicts the same numbers there. GTAO is distinctive only (a) in substrates where the native rival is non-optimizing (neutral turnover, positive-feedback self-organization, mechanistic constraint, "bigger means more levels"), and (b) in a few derived dimensionless constants that nobody has claimed hold across substrates. (§2)
4. **Short list of risky predictions, ranked** (§2.4):
   1. **The sharedness sign flip at the onset of a level.** Shared drift makes a shared level form at a *smaller* group size, with elasticity −1. Private drift makes it form at a *larger* size, with elasticity between +(1−γ) and +1. Contingency theory and "more volatility, more decentralization" predict one sign for total volatility. Fixed-size and duplicated-effort rules predict 0 and −½.
   2. **The vigilance ratio (DERIVED tonight; not found stated).** At onset, a new shared tracker samples its driver √(N\*ρ/(1+ρ)) times as often as a member did. That is always above 1, and about **2** in the small-shared-share regime with free upkeep (√Π\*; more with upkeep). "Higher levels are slower" predicts below 1. Duplicated effort predicts exactly 1.
   3. **The fallback cliff with a moving edge.** Holding effort rises with drift and then drops to zero. The edge sits at σ_c = μu/√(2cw), so it **moves in proportion to fallback cost × use rate**. This is where human–AI memory lives: as lookup gets cheaper, the drift above which people stop holding a fact falls proportionally.
   4. **Layers.** A speed layer pays only if its upkeep is below the clock saving it buys. For two components that saving is ≤ 29% of the single-clock tracking bill, and only ≈ 5% at a 2× timescale separation. The layer count should grow with decades of drift span times ln(stakes/upkeep). The spacing between adjacent layers should depend on the cost ratio, not the span. The last claim still needs a derivation check (test N1-C).
   - None of these four is GTAO-only against economics. Each is GTAO-only against the native rival outside economics. **What would make one truly GTAO-only is the "architecture equation" proposed in §2.5:** the organization is a cost-thresholded multiscale factorization of its environment's cross-member drift spectrum, with universal dimensionless constants (Π\* ≈ 4, a vigilance ratio ≈ 2, a 29% ceiling) tested across substrates. Metabolic scaling theory's ¾ is the model for that kind of claim.
5. **Prior art (§3).** Team theory and rational inattention in organizations own more than the drafts credit:
   - Geanakoplos & Milgrom 1991 [R] already have an *onset condition for a managerial level*, and a drift-to-structure prediction (more uncertainty, smaller spans).
   - Dessein, Galeotti & Santos 2016 [R] already have *bimodal attention* (focal vs non-focal tasks), "plan vs feedback" as the organizational form of freeze vs hold (quoting March & Simon 1958), and "more volatility, smaller scope".
   - Veldkamp & Wolfers 2007 [PR] already have the N × share ≥ fixed-cost condition.
   - What I did not find in what I read: a *dynamic drift spectrum* setting the number, spacing and scope of levels; the *shared-vs-private sign flip* stated with exponents; the *vigilance ratio*; and any cross-substrate claim.
   - Marschak & Radner's book text was **not accessible** (the Cowles PDF is blocked), so that gap is narrowed, not closed.
6. **Tonight's tests (§4), at most 2 light processes:**
   - **N1-A LEVELS-SIM:** onset regime map under finite selection resolution. The highest value, because it decides whether any field test of the onset can work.
   - **N1-B P1:** the already-locked item-level memory slope, Meeter data on disk, about 1 minute. It **needs a decision first**: run it now with a self-attested lock only, or wait for Chad's go to anchor the hash externally.
   - **N1-C LAYERS-1:** a derivation check with a kill rule on GTAO's own distinctiveness for layered memory.

---

## 1. The core causal claim, its first-principles implications, and every kill

### 1.1 The claim as a mechanism

**C (core mechanism).** For any system that persists by acting on a world it does not control:

- **C1. Drift destroys held information.** What the system holds about a decision-relevant variable X decays at a rate set by X's dynamics. Holding I bits against a world that mixes at rate η per step needs an inflow of at least (1−η)·I bits per step. *KNOWN* (strong data processing; Mitter & Newton 2005; Horowitz & Sandberg 2014; the project's I5).
- **C2. Re-buying information draws on one finite budget.** Sensing, storing, transmitting and acting on information cost resources from a budget that also pays for everything else (heat, attention, money). The cost of tracking is **concave in stakes × drift** for the usual loss functions: √ for diffusive drift under quadratic loss. It has **economies of sharing**: one reading of a common driver can serve many users. *KNOWN* in each piece (EOQ; Kalman/Muth; Sims 2003; Wilson 1975).
- **C3. Staleness and lateness cost at the stakes of the decisions that use the information.** Ruin happens when accumulated error outruns the buffer. *Definition plus KNOWN first-passage results.*
- **C4. Variation plus differential persistence (selection, or deliberate design and learning) favors forms with lower total cost** (upkeep + loss + ruin + drift reduction). It does so only to the resolution that selection allows: differences smaller than selection's noise are invisible (Lynch's drift barrier; noisy choice à la Matějka–McKay; §3).
- **C5. Therefore architecture is caused by the environment's statistics and the substrate's prices.** That includes the allocation of maintenance across variables, timescales and users; levels; refresh rates; memory horizons; freezing; fallbacks; buffers; and drift reduction. The design variables should covary with (drift spectrum, stakes, sharedness of drivers, relative prices), with elasticities fixed by the cost exponents, **wherever the cost differences exceed selection's resolution.** Outcomes *given* a design (failure rates given σ, τ, B) are set by the stochastic process. C does not predict them beyond that process.

**What causes what:** drift → decay of held information → a maintenance cost flow → selection on how maintenance is allocated → observable architecture. Mismatch between the allocation and the realized drift → error → failure.

**Where each piece comes from.** C1–C3 are known physics, information theory and decision theory. C4 is the selection premise that rational analysis, optimal foraging, rational inattention and Lee–Flack–Krakauer also use. GTAO's own claims are only two:

- **(U) Universality.** The same allocation law, with the same dimensionless structure, holds across substrates whose currencies differ (heat, attention, money). The only differences are the cost exponents and selection's resolution.
- **(L) Levels.** The multi-member, multi-timescale part: levels, their onset, their speed and their scope. These follow from C2's economies of sharing combined with the drift spectrum.

Everything else in GTAO is a correct application of known machinery (SCALEFREE §2.7; PROFOUND §2).

**What C is not.** It is not "systems minimize free energy". C says nothing about goals, only about what tracking costs while a system pursues them. It is not "everything is fractal": the architecture inherits whatever scale structure the world has (T7). And it is not a theory of failure rates.

### 1.2 What C implies, derived from first principles (status of each)

| # | Implication | First-principles route | Status |
|---|---|---|---|
| I1 | Maintenance effort rises sublinearly with stakes × drift: check rate ∝ √(wσ²/c) for diffusive drift under quadratic loss; memory ∝ τ_E^{1/2} | C1 + C2 + optimization (EOQ / Kalman) | KNOWN (Harris 1913; Kalman 1960; Reis 2006; Lee, Flack & Krakauer 2024) |
| I2 | **A bounded fallback creates a cliff.** Holding effort rises as σ√(w/2c), then drops to 0 at σ_c = μu/√(2cw) | Unbounded holding cost vs bounded fallback cost u per use at rate μ (T5b) | DERIVED; core case KNOWN (Cho & Garcia-Molina 2003); the qualitative regimes are KNOWN (Stephens 1991) |
| I3 | **Freeze** (keep a copy, stop refreshing) when drift × check cost < Φ | Theorem G | DERIVED; qualitative form KNOWN (Bateson 1963; March & Simon 1958's "coordination by plan" when the situation is stable [R, quoted in DGS 2016]) |
| I4 | **A shared level forms** when N·w·q_g·φ′(w q_u) − φ(N w q_g) > h; for a small shared share N\* ∝ q_g^{−1} | C2's economies of sharing (T3a; PROFOUND_v2) | DERIVED; KNOWN in substance (Veldkamp & Wolfers 2007 [PR]) |
| I5 | **Layers at different speeds** pay when drift spans timescales and the clock saving exceeds per-layer upkeep. Two-component saving ≤ 29%; the layer count grows with decades of span | T3b, T3c, T7b, SCALEFREE S3 | DERIVED; substance KNOWN (Roundy 1985 [M]; Benna & Fusi 2016; Shankar & Howard 2013; dynamic rational inattention, Afrouzi & Yang [search summary]) |
| I6 | Model size ∝ throughput^{1/(β+g)} for mode-variance exponent β and mode-timescale exponent g | Reverse water-filling with upkeep as a flow | DERIVED (INTERNAL_MODEL_REVIEW r2); untested against the fixed-budget null |
| I7 | Solvency margin δ ⇒ the system carries a near-copy of the world's causal states, with P_e ≤ 2δ/γ² | Pinsker + triangle inequality (I3) | DERIVED; probably incremental (Nayebi 2026; Richens et al. 2024/25 [PR]) |
| I8 | **Stabilize** is a substitute for tracking: paying to reduce drift lowers optimal watching | Add a control on σ to J | HYPOTHESIS (THEORY §5); qualitative prior art (Thompson 1967 [M]; Sterling 2012) |
| I9 | **Persistence trilemma:** where unmanaged loss diverges, a finite-rate system persists only by ignoring (a bounded fallback), stabilizing, or renewing; for β < 1 there is a maximum viable size Q_max | Divergent loss vs finite information rate | DERIVED (assembly); Q_max untested |
| I10 | **Fit improves with selection strength.** Deviations from I1–I9 shrink as selection resolution grows, and vanish below the drift barrier | C4 | Logic KNOWN (Lynch et al. 2016); never tested as a property of GTAO's elasticities |

**The causal reason I4 and I5 belong together** (a first-principles point the drafts do not make): a level is a tracker whose *stakes are pooled*, and a speed layer is a tracker whose *clock is separate*. Both are the same move, factoring the environment's drift into components and buying each component separately. A level factors across members. A speed layer factors across timescales. **The architecture is a factorization of the environment's drift covariance, across members and across timescales, kept only where the factor's saving beats its upkeep.** That is the seed of §2.5.

### 1.3 Every kill, accounted for honestly

| Kill | What was tested | Causal diagnosis | What it means for C |
|---|---|---|---|
| **√N in languages** (LANG1: elasticity 0.13 [0.05, 0.26], prediction 0.5) | T4's Kalman averaging, mapped to word-gain rate vs speaker population | T4 needs (i) independent deposits and (ii) a trace that is *designed to track* a drifting target under selection for tracking accuracy. Speakers copy each other, which is the FOL arm, where effective N ≪ N. Basic vocabulary is not tracking a drifting referent, and selection on it for accuracy is weak. The scale-free version of T4 (N^{1/α}) makes the miss *worse* for any α ≤ 2 (SCALEFREE §2.6). 91% of the "gains" were uncoded forms | **The mapping failed, and the failure is GTAO's fault.** C has no criterion for when an observed turnover rate is a *chosen* tracking rate rather than neutral turnover. Both premises were listed as threats in the prereg, so invoking them now is not a rescue. It is a scope rule that must be fixed *before* the next test: **C applies only to design variables under selection whose resolution exceeds the prize** (C4). Under that rule LANG1 should not have been run as a test of T4 |
| **τ in populations and glucose** (glucose −0.46 vs a literal −1, populations −0.21; the literal joint kill fired) | The single-timescale first-passage sub-model's −1 fixed-spread exponent, √τ weighting, identities and collapse | Real counts carry extra timescales (sampling step, episode rules, multiple components). These give slopes between −½ and 0 for an ordinary OU process. Own-spectrum surrogates reproduce glucose (−0.50 [−0.58, −0.42]) with zero free parameters (SCALEFREE S5). The τ weight is the Hurst exponent H. The bank identities failed because failures there were common jumps, not each unit's own diffusion | **Not a test of C.** C predicts design choices. Outcomes given (σ, τ, B) are stochastic-process physics. The kill is real for the sub-model, and it teaches a method: *failure data cannot confirm a design theory*. The F1 arm also mismeasured τ (it mostly measured operating leverage) |
| **News exponent match** (MATCH1 A1: memory 0.24 vs need 0.71, ratio 0.34) | "Efficient memory's decay exponent equals need's", on population-level curves | Per-item cost-optimal memory decays at least as steeply as need (SCALEFREE S2i). Population curves are flattened by heterogeneity, a known marginal-vs-conditional effect. Getting to 0.24 needs very large heterogeneity or a free exponent. The post-hoc "costly misses make memory outlast need" changes the horizon, not the exponent, so it is **refuted as stated** (S2v) | **The strong marginal claim is dead.** C's per-item version is **untested**: P1 is locked and not yet run (§4, N1-B). The weak form (power law follows power law) is Anderson 1990's |
| **A generic mean-reverting baseline matches the failure rates** | Whether any failure-rate result needs GTAO | No. Every sign and slope seen is produced by a stationary process with its own spectrum and a barrier (SCALEFREE §3) | **C's content is entirely in design choices.** This is the most important method result so far, and it is publishable (PROFOUND §5.1) |
| Also: MATCH1 D3, redness sign opposite (+0.57, exploratory) | Spectrum → forgetting exponent mapping | The mapping was guessed, not derived | Open gap; it does not count against C until a mapping is derived and locked |
| Also: C3, τ absent in open source; the reset-clock mechanism rejected | Failure-rate sub-model | As for τ above | Not a test of C |

**Passes, with their rivals:** measles freeze-or-hold (ratio 0.05) has a mechanistic rival (long-lived plasma cells) and data already read, so its ordinal cross-pathogen form is a POSTDICTION. The need band 0.6–0.8 is produced by heterogeneous memoryless items (S1). P2 (per-file hazards) is locked and would test that premise.

**Net:** C survives because nothing has tested it on design choices with a discriminating rival. That cuts both ways. GTAO is a theory in the sense that it makes causal, falsifiable claims, and some of its applications have already been killed. **It has no confirmed discriminating prediction of its own.** The next tests must be choice data or designed simulations, with the selection-resolution scope rule stated up front.

---

## 2. Discriminating-predictions audit

### 2.1 The rivals that matter

- **R-econ:** value of information, rational inattention, team theory, EOQ, Wiener–Kolmogorov. *This is GTAO's own math.* Wherever an economist would apply it, it predicts the same numbers. GTAO can beat R-econ only by applying it where economists have not, or by a structural combination R-econ has not made.
- **R-stat:** generic statistics, meaning heterogeneity/aggregation (fake power laws, attenuated slopes) and barrier processes (failure rates).
- **R-neutral:** neutral turnover or drift with no optimization (languages, much of culture, weakly selected traits).
- **R-mech:** mechanism-specific constraints (plasma-cell lifetimes, pheromone chemistry, regulatory floors).
- **R-sof:** positive-feedback self-organization. Thresholds come from recruitment nonlinearity (Beekman et al. 2001) and do not depend on drift.
- **R-size:** "structure follows size". Scalar stress (Johnson 1982; Perret et al. 2020), Radner 1993's log N, Keren & Levhari.
- **R-cont:** contingency theory: volatile environments call for organic, decentralized structures (Burns & Stalker 1961 [M]; Lawrence & Lorsch 1967 [M]). In the formal versions, more volatility means smaller scope or spans (Geanakoplos & Milgrom 1991 [R]; Dessein, Galeotti & Santos 2016 [R]).
- **R-dup:** the managerial rule "build the shared thing when duplicated effort exceeds its fixed cost" (Gaffney & Durek 1989 [PR]).
- **R-slow:** "higher levels are slower" (Simon 1962; Holling 2001; Allen & Starr [M]).
- **R-approx:** layer counts and spacings set by approximation accuracy alone (Beylkin & Monzón 2005 [M]; Benna & Fusi's fixed ratio 2).

### 2.2 Every surviving or derivable prediction

D = distinctiveness, the size of the gap from the *best* rival (0 means identical). T = testability with data in hand or a designed simulation. I = importance. Each is scored 0–5.

| # | Prediction | Best rival and its number | Does GTAO differ? By how much? | D | T | I | D×T×I |
|---|---|---|---|---|---|---|---|
| A | **Sharedness sign flip at level onset:** e_g = ∂ln N\*/∂ln q_g = −1 (small ρ); e_u = ∂ln N\*/∂ln q_u ∈ [1−γ, 1] | R-econ: identical. R-cont: total volatility → decentralize (one sign). R-dup: e_g = −γ ≈ −½. R-size: 0. R-sof: 0 | Same as R-econ. Against R-cont, opposite *sign* for shared volatility. Against R-dup, 0.5 in the exponent. Against R-size, 1.0. **Caveats:** only for small ρ, quadratic-like loss, a driver readable without polling members, no per-member broadcast cost. Near threshold the prize is 0.015–1.3%, so observational detection is weak | 3 | 3 (sim now; field only with q_g and q_u measured separately) | 5 | **45** |
| B | **Vigilance ratio:** a new shared tracker samples its driver √(N\*ρ/(1+ρ)) times as often as a member did. That is > 1 always, ≈ 2 at small ρ with free upkeep, and 1+√(1+2h′) with upkeep (§2.3) | R-slow: < 1. R-dup: = 1. R-econ: same if anyone derived it (I did not find it stated) | Against R-slow and R-dup: a factor of ≥ 2 in the small-ρ regime, where they say ≤ 1. **Caveats:** it assumes the shared driver's check cost equals a member's (the ratio scales as √(c/c_g)). It is the same math family as T4, which died on languages under a bad mapping. ANTS1 is testing a T4 version in simulation | 4 | 3 (ANTS1-type sim; software: an org's shared wrapper's upstream-bump rate vs member repos' bump rates; Wikipedia templates vs inline facts) | 3 | **36** |
| C | **Fallback cliff with a moving edge:** effort is bimodal against drift; the edge σ_c ∝ μu (fallback cost × use rate); for people with AI, the drift threshold for holding a fact falls in proportion to lookup cost | R-econ (Cho & Garcia-Molina; DGS bimodality from complementarity): bimodality yes, but DGS gives no fallback-cost edge. R-mono (effort rises with volatility): no cliff. Sparrow et al. 2011; Risko & Gilbert 2016 (offloading as cost–benefit, qualitative [M]) | The *location law* (elasticity 1 of σ_c in μu) separates it from DGS and from qualitative offloading accounts. Bimodality alone does not separate it from DGS | 3 | 3 (software pin/track/vendor choices; Wikipedia maintenance vs citation-only; human experiments later) | 5 | **45** |
| D | **Layers:** add a speed layer only if upkeep < s(R) × tracking bill, with s ≤ 29% for two components and ≈ 5% at R = 2; layer count ∝ decades × ln(w/h); adjacent spacing set by the cost ratio, not the span (needs N1-C) | R-approx: count ∝ decades at fixed accuracy, spacing set by accuracy. Benna–Fusi: fixed ratio 2. T7b (GTAO's own older model): K ∝ L^{2/3}, spacing growing as L^{1/3} | Against R-approx: the upkeep dependence and the 29% ceiling. Against T7b: span-invariant spacing. Sizes have not been computed yet, which is the point of N1-C | 3 | 2 (derivation tonight; empirical later) | 4 | **24** |
| E | Model size ∝ Q^{1/(β+g)} | Fixed budget share: exponent 1 | Large, if β+g ≠ 1 is measured in the environment | 4 | 1 (no dataset varies the environment at fixed organization type) | 4 | 16 |
| F | Item-level memory slope ≥ need (P1, a_c ∈ [0.5, 1.2]) | Anderson 1990 with item-level d ≈ ⅓ (a_c ≈ 0.24) | About 0.3–0.5 in slope; a clear call either way | 2 | 5 (locked; data on disk) | 2 | 20 |
| G | Fit improves with selection strength (I10) | R-neutral: no dependence | Qualitative unless selection is measured | 2 | 2 | 4 | 16 |
| H | Persistence trilemma, Q_max for β < 1 | Penrose 1959 (qualitative [M]) | A number, but β is unmeasured | 3 | 1 | 4 | 12 |
| I | Stabilize/track substitution (I8) | Thompson 1967 buffering (qualitative) | Sign only | 3 | 1 | 3 | 9 |
| J | Iso-risk buffer B ∝ σ τ^H (P3, banks) | Inventory theory: safety stock ∝ σ√L, the same law at H = ½. Regulatory floor: e_τ = 0 | None against inventory theory. Against the floor model: H. The same-series confound (B and τ both come from the capital ratio) is serious | 1 | 3 | 2 | 6 |
| K | Internal-model bound P_e ≤ 2δ/γ² | Nayebi 2026; Richens et al. | A theorem; it cannot fail empirically unless the proof is wrong | 1 | 2 | 3 | 6 |
| L | Spectrum → exponent (½, 1/α, H) | Wiener–Kolmogorov | None | 1 | 2 | 3 | 6 |
| M | Commons: staleness rises with users per maintainer; enforcement where shared memory is a public good | Olson 1965; Ostrom 1990 [M] | None in sign | 1 | 2 | 3 | 6 |
| — | Fixed-spread sign / τ in failure rates | Dimensional analysis, Rice/Siegert | None; **dead as GTAO content** | 0 | — | — | 0 |
| — | √N fade in languages | R-neutral plus copying | Killed (LANG1) | — | — | — | — |
| — | Need band 0.6–0.8 as evidence of a scale-free world | R-stat heterogeneity | None | 0 | — | — | 0 |

### 2.3 New derivation tonight: the vigilance ratio (DERIVED; check in `vigilance_check.out`)

- **Model.** T3a: EOQ tracking (γ = ½), x_i = g + u_i, and the shared driver is readable at the same check cost c.
  - A flat member checks x_i at rate ∝ √(w(q_g+q_u)/2c).
  - A shared tracker for g has stakes Nw, so it checks at rate ∝ √(Nwq_g/2c).
- **Result.** At the exact onset N\*, the ratio of the two rates is **√(N\*ρ/(1+ρ))**.
  - For small ρ this is √Π\* = 1 + √(1+2h′): **2.000 at h′ = 0, 2.73 at h′ = 1, 5.58 at h′ = 10** (the exact T3a roots agree to within 0.3% for ρ ≤ 0.01).
  - The ratio falls toward 1 as ρ grows (1.71 at ρ = 1, 1.30 at ρ = 10, with h′ = 0), and it is above 1 for every ρ.
- **Reading.** **A shared level is born more vigilant than the members it serves.** It samples its driver at least as often as a member sampled before, and about twice as often in the regime where pooling is subtle. This contradicts "higher levels are slower" *per unit of the driver's own drift*. Higher levels may still track slower drivers, so the testable quantity is sampling rate ÷ √(the driver's drift).
- **Scope.** It holds for quadratic loss with diffusive drift, a driver readable at a comparable check cost, and members' checks that can align with the level's. It breaks under the same conditions as A (POOLING_REVIEW §2).
- **Novelty.** It is the EOQ √ law applied twice, so it is elementary. I did not find it stated as a property of levels, but I searched only the sources in §3. Treat it as UNVERIFIED NOVELTY.

### 2.4 Ranking and the short list

By D×T×I: **A (45) = C (45) > B (36) > D (24)** > F (20) > E = G (16) > H (12) > the rest.

**Short list of risky predictions:**
1. **A, the sharedness sign flip at level onset.** Same direction, opposite effects of shared and private volatility. Rivals R-cont, R-dup, R-size and R-sof each predict something different.
2. **C, the fallback cliff with a proportional moving edge.** The most human-relevant (people and AI). It separates from DGS through the fallback-cost edge.
3. **B, the vigilance ratio ≥ 2 at onset in the small-ρ regime.** A dimensionless constant, and the opposite of the R-slow folk theory.
4. **D, the layer rules**, conditional on N1-C showing that spacing depends on the cost ratio and not on span.

**Are any of these "only GTAO"? No, not against economics.** All four follow from the economics of information. Nobody has stated them across substrates, and A, B and D have not been stated in this dynamic, multi-level form in what I read. What the theory can honestly claim is: **"the economics of information, extended to dynamic multi-level tracking, makes these four predictions across cells, colonies, software, firms and human–AI systems, where the native rivals predict differently."** The claim is universality, not a new optimization principle.

### 2.5 What would have to be added to get a GTAO-only prediction

**The architecture equation (HYPOTHESIS, to derive).** Let S(f) be the environment's drift cross-spectral matrix across members (who needs what) and frequencies (how fast it moves). The cost-optimal organization is the factorization S(f) ≈ Σ_levels B_ℓ S_ℓ(f) B_ℓᵀ + private residuals that minimizes Σ_ℓ [tracking cost of factor ℓ at pooled stakes + h_ℓ] + residual tracking cost. A factor is kept only if its pooled saving beats its upkeep (A), and each kept factor is sampled at its own EOQ rate (B).

It would predict, jointly and from measured environment statistics:
- (a) **how many levels**: one per factor that clears onset;
- (b) **each level's scope**: the members loading on that factor;
- (c) **each level's speed**: set by the factor's spectrum and pooled stakes;
- (d) **the minimum separation between levels**: from the clock saving vs upkeep, T3b/T3c;
- (e) **dimensionless constants that are the same on every substrate**: Π\* = γ^{−1/(1−γ)} (4 at γ = ½), vigilance ratio √Π\*, a 29% two-clock ceiling.

Why this would be GTAO-only:
- Team theory is static.
- Rational inattention in organizations is single-period or single-agent.
- The mirroring hypothesis and Conway's law say structure mirrors the *communication or task* structure, not the *environment's drift* structure weighted by stakes and thresholded by cost. Closest work [M]: MacCormack, Baldwin & Rusnak 2012 (mirroring); design structure matrices.
- Simon, Holling and panarchy say it qualitatively.

The risky, GTAO-only test: **organizational boundaries and level speeds line up with the cost-thresholded factor structure of measured environmental co-drift better than with communication structure or size alone.** A first substrate is software: co-change drift from upstream dependencies vs module, wrapper and team boundaries, and wrapper upstream-bump rates. It needs a derivation (Day 2) and a careful preregistration. **This is the "BIG" claim worth building toward: the shape of an organization is a compressed, cost-thresholded image of the shape of change in its world.** It is a hypothesis, not a result.

---

## 3. Prior-art gaps: team theory and rational inattention in organizations

**What was read this session**
- **[R] full text:** Dessein, Galeotti & Santos 2016 (intro, literature, model, propositions list; PDF from Columbia, saved in `src/dgs.pdf`).
- **[R] full text, OCR'd discussion-paper version:** Geanakoplos & Milgrom (Cowles DP 775R, 1988; the published version is JJIE 1991).
- **[R] abstracts only:** Matějka & McKay 2015; Crémer 1980.
- **[R] table of contents only:** Veldkamp 2011.
- **[R] bibliographic metadata only:** Radner 1962 (Crossref); Maćkowiak, Matějka & Wiederholt 2023.
- **Search summaries only:** Afrouzi & Yang, and Crémer, Garicano & Prat 2007.
- **Not accessible:** Marschak & Radner 1972 (Cowles PDF blocked from this box and from the fetch tool).

| Source | Status | What it has | Overlap with GTAO | Residual for GTAO |
|---|---|---|---|---|
| **Geanakoplos & Milgrom 1991**, *J Japanese & Int'l Economies* 5(3):205–225 | **[R]** (DP 775R text) | Team theory with limited managerial attention; managers choose what to know; quadratic resource allocation with normal sampling. **The savings from a manager over n shops are (n−1)Bβ/[r(n+β)], with increasing returns, and no manager is hired if the wage exceeds a threshold.** This is an onset condition for a managerial level. **Firms in more uncertain, newer industries should have abler managers or smaller spans (Props 8–9).** There is a limit to profitable unit size and to hierarchy depth | **High.** A team-theory onset condition for a level, and a drift → structure prediction (more uncertainty, smaller spans) | The variable is *total prior uncertainty* about each shop's own parameter, not shared vs private drift. No dynamics, no drift spectrum, no sign flip by sharedness, no vigilance ratio. GTAO's A predicts that shared uncertainty *raises* centralization, against GM's direction for private uncertainty. That is consistent with GM on the private side and different on the shared side |
| **Dessein, Galeotti & Santos 2016**, *AER* 106(6):1522–36, doi 10.1257/aer.20140741 | **[R]** | Quadratic team payoff (adaptation φ_i, coordination β). Attention is scarce, with concave communication success 1−e^{−λt}. **Optimal attention is bimodal:** a few "focal" tasks get all of it and adapt, and the rest follow a pre-set plan (*coordination by plan vs by feedback*, quoting March & Simon 1958: "the more stable and predictable the situation, the greater the reliance on coordination by plan"). The number of focal tasks falls with interdependence and organization size. **More volatile environments mean smaller but less focused organizations** (§III, informal). The effect of IT on size is ambiguous | **High for C and freeze/hold.** Bimodality and plan-vs-feedback are the organizational form of freeze vs hold, already in print. Rival direction to A on volatility (task-specific shocks) | DGS's bimodality comes from complementarity between attention and adaptation, not from a bounded fallback; no fallback-cost edge (C's σ_c ∝ μu). Shocks are task-specific (private). No shared driver, no level onset, no dynamics or spectrum |
| **Crémer 1980**, *Bell J Econ* 11(2):683–693 | **[R] abstract** | Grouping functions into units to get the most efficient coordination; "the organization as a reducer of uncertainty"; a simple formula | Medium: which units share a level, in team theory | Static; no drift dynamics; not read beyond the abstract |
| **Marschak & Radner 1972**, *Economic Theory of Teams* (Yale UP) | **[M]; text not accessible** | Quadratic-Gaussian teams; value of information structures (complete information, decentralized, management by exception or "emergencies", partitioned communication) weighed against their cost. Radner 1962 (*Ann Math Stat* 33:857–881, Crossref-verified) shows person-by-person-optimal linear rules are team-optimal in quadratic teams | The machinery. The value of a common observation is linear in its variance, which is where A's −1 comes from | I know of no explicit N × shared/private threshold in it, but **I could not search the text, so this gap is narrowed, not closed.** Next step: a library or scanned copy of chs. 4–6, or Radner 1962 in full |
| **Matějka & McKay 2015**, *AER* 105(1):272–98 | **[R] abstract** | Rational inattention with entropy cost gives a (generalized) multinomial logit in payoffs | Not a rival on A–D. **It formalizes C4's resolution limit:** choice probabilities are logistic in (payoff gap ÷ information cost λ), so near an onset threshold, where the prize is tiny, choices revert to the prior | Use it in N1-A as the selection-noise model, and in field tests as the reason a 0.1% prize cannot show the −1 |
| **Veldkamp 2011**, *Information Choice in Macroeconomics and Finance* (Princeton UP) | **[R] TOC only** | Ch. 8 "Returns to Scale in Information" (specialization, markets for information); ch. 9 "Information as an Aggregate Shock" (the Veldkamp–Wolfers model) | Returns to scale in information is A's mechanism. Ch. 9 is the closest known statement (Veldkamp & Wolfers 2007, Prop. 2 [PR]) | Contents not read; ch. 8 should be read before any novelty claim on A |
| **Sims 2003**, *J Monet Econ* 50:665 | [PR] (DOI; eq. 46 identified in INTERNAL_MODEL_REVIEW) | Entropy-cost tracking; multivariate attention allocation | I1, I6 (water-filling) | none |
| **Maćkowiak, Matějka & Wiederholt 2023**, "Rational Inattention: A Review", *JEL* 61(1):226–73 | metadata only | Survey | Should be read for any RI-in-organizations result on common vs idiosyncratic shocks with N | unknown |
| **Afrouzi & Yang** (dynamic rational inattention, LQG; DRIPs) | search summary only | Dynamic RI: slower components get less attention and slower belief updates; Kalman gains per component | **Prior art for I5** (multi-speed tracking under an attention cost) in economics | Layer upkeep thresholds and spacing (D) not known to be there |
| **Crémer, Garicano & Prat 2007**, *QJE* 122(1):373 | search summary only | An efficient organizational "language" uses precise terms for frequent events and vague ones for rare events | A shared code is a shared memory level tuned to frequency: a cousin of A and I5 | Static |
| Veldkamp & Wolfers 2007; Wilson 1975; Kish design effect; Garicano 2000 | [PR] (POOLING_REVIEW) | N × share ≥ fixed cost; informational scale economies; the product-form criterion; communication cost destroys the Nρ law | A is KNOWN in substance | Dynamic form, Π\* constant, the cross-substrate claim |

**Prior-art verdict**
- Team theory (Radner 1962; Marschak & Radner 1972; Crémer 1980; Geanakoplos & Milgrom 1991) already owns *static* coordination and information-structure design with quadratic payoffs. That includes an onset condition for a managerial level (GM) and the "more uncertainty, smaller spans" comparative static.
- Rational inattention in organizations (DGS 2016) already owns bimodal attention, plan vs feedback (freeze vs hold in organizational dress), and "volatility, smaller scope".
- Veldkamp–Wolfers own the N × share ≥ fixed-cost condition.
- **Not found in what I read:**
  - (i) a *shared vs private* volatility sign flip on level formation, stated with exponents;
  - (ii) the vigilance ratio;
  - (iii) a dynamic drift spectrum setting the number, spacing and scope of levels;
  - (iv) the fallback-cost edge in organizational form;
  - (v) any cross-substrate (cells, colonies, software) claim.
- **Owed before any public novelty claim:** Marschak & Radner chs. 4–6, Veldkamp 2011 ch. 8, the 2023 JEL survey, Alonso, Dessein & Matouschek 2008 (centralization vs decentralization with local vs common information [M]), and the Hayek 1945 lineage (decentralize local knowledge, qualitative [M]). The qualitative "centralize common information, decentralize local information" is probably old. Only the exponents and the cross-substrate claim are candidates.
- **Consequence for the write-up:** A should be framed as "team theory and VOI, made dynamic and tested across substrates". GM 1991 and DGS 2016 must be cited as the organizational ancestors, along with Veldkamp–Wolfers.

---

## 4. Recommended tests for tonight (CPU only; at most 2 light processes; ANTS1 holds 5 processes and about 12 GB of the 15 GB)

At 00:30 ET, free memory was about 3 GB. Each test below is single-process and stays under about 1 GB, except N1-B, which peaks near 1.5–2 GB (dense item dummies). **Run N1-B only while ANTS1 leaves at least 3 GB free, and never at the same time as N1-A.**

### N1-A. LEVELS-SIM-1: does finite-resolution selection discover the onset law, and where does it become invisible? (highest value)

**Why it matters.** It is the fair test of A named in PREREG_DRAFT §7. It also settles the question that decides every field test: at what prize-to-noise ratio does the −1 stop being visible to an adaptive process? If selection cannot see it, observational tests of A are pointless, and the onset becomes a ρ threshold. Matějka–McKay and C4 both predict that.

**Design (lock before running; commit and hash locally):**
- **World:** the T3a model with γ = ½ and EOQ periodic perfect checks. Each organization picks a mode, FLAT or LEVEL, and log check intervals.
- **Cost:** the exact expected cost per member per step (closed form) **plus selection noise**. Noise is Gaussian with SD equal to the exact standard deviation of realized loss over an evaluation horizon H. Compute it from Var(Σ_k W_k²) for random-walk segments between checks (closed form: the variance of a sum of squared Gaussian random-walk values). Scale by 1/√(#segments × n_eval members), with n_eval = min(N, 16). This keeps the run cheap and makes selection resolution an explicit knob.
- **Adaptive process:** Wright–Fisher with tournament selection. M = 200 organizations per cell, G = 200 generations; mode-flip mutation 0.02; log-interval mutation SD 0.1.
  - Outcome: P(LEVEL), the mean over the last 50 generations.
  - Fit N₅₀(q_g, q_u) per ρ bin by logistic regression in ln N within the bin.
  - Elasticities e_g and e_u come from N₅₀ across q_g and across q_u, exactly as in PREREG_DRAFT §1 and §4.
- **Grid:**
  - q_u ∈ {1, 4};
  - ρ ∈ {0.003, 0.01, 0.03, 0.1, 0.3, 1, 3, 10};
  - N ∈ {2, 4, …, 2¹⁴};
  - upkeep h′ ∈ {0, 10} (h′ computed at q_u = 1);
  - resolution H ∈ {10⁵ ("strong selection"), 10² ("weak selection")};
  - seeds: 10 per cell.
- Expected runtime is about 1 hour, single process, numpy only, with memory well under 1 GB.

**Locked predictions** (computed from T3a / PROFOUND_v2 before running):
- **P1 (strong selection, small ρ ≤ 0.03):** e_g ∈ [−1.2, −0.8] at both h′ values. e_u ∈ [0.8, 1.1] at h′ = 0, and ∈ [0.4, 0.75] at h′ = 10 (the review's +0.54 at h′ = 100 and +0.8 at h′ = 1 bracket it).
- **P2 (strong selection, large ρ ≥ 3):** e_g ∈ [−0.75, −0.25] at h′ = 10 (→ −γ), and e_g ∈ [−0.25, 0.05] at h′ = 0 (→ 0).
- **P3 (weak selection):** for ρ below a resolution threshold ρ_res, P(LEVEL) shows no identifiable 50% crossing in N inside the grid, or its fitted e_g has magnitude > 1.5. ρ_res is the point where the prize at N = 2N\* equals the selection-noise SD, and it **is computed and written into the lock before running.** Prediction: the empirical ρ_res is within a factor of 2 of the computed one.
- **P4 (vigilance, B):** in cells where LEVEL wins, the evolved shared check rate ÷ the evolved flat member check rate at the N closest to N₅₀ is within ±25% of √(N\*ρ/(1+ρ)) (≈ 2.0 at h′ = 0, ≈ 5.6 at h′ = 10, small ρ).

**Kill rules:**
- **K1 (candidate A as an empirical program):** under strong selection, the e_g CI in small ρ excludes −1 and includes −0.5 or 0. That would mean T3a's own world, searched by selection, does not produce the −1, and the field program for A is dropped.
- **K2 (the tiny-prize analysis):** the empirical ρ_res is off by more than 4× from the computed one. The detectability claims in PREREG_DRAFT §7 would then be withdrawn.
- **K3 (B):** under strong selection, the evolved vigilance ratio is ≤ 1 in ≥ 3 of the 4 small-ρ cells. B is withdrawn.

**Honest scope.** P1, P2 and P4 can fail only if realized-cost selection departs from T3a's bound (integer intervals, local optima, the sufficient-only bound). P3 is the informative part about the real world. This tests *discoverability*, not nature.

### N1-B. P1: item-level memory slope (already locked; about 1 minute)

**Lock:** `theory-v3/PREDICTIONS.md`, sha256 `f7d7cf75…9048`, local commit `fb95b62` (2026-11-14 23:46 ET). Script `prereg/p1_meeter_conditional.py`, sha256 `3e18ac48…0b4d`. Both hashes re-checked tonight and unchanged.
- **Prediction:** a_c ∈ [0.5, 1.2], lower CI > 0.35.
- **Competitor:** Anderson 1990 item-level d ≈ ⅓, giving a_c ≈ 0.24.
- **Kill:** a_c < 0.35, or upper CI < 0.5.
- **Command:** `cd /workspace/gtao/theory-v3 && .venv/bin/python prereg/p1_meeter_conditional.py`

**Decision needed before running.** PROFOUND's Day 1 plan said to run this "with Chad's go to anchor the hash" externally. **Running it first permanently gives up the external timestamp.** An anchor made after the result proves nothing. Either:
- (a) run tonight and report it as self-attested (the lock commit predates this audit), or
- (b) wait for Chad's go to post the hash (a public, externally visible act).

I recommend (b) if Chad is reachable by morning; otherwise (a), labeled plainly. It is ranked second because it is decisive for one thread ("memory mirrors need" at the item level) but not distinctive of GTAO (§2.2, F).

### N1-C. LAYERS-1: does GTAO say anything about layered memory that approximation theory does not? (a derivation check with a distinctiveness kill)

**Design:**
- **Kernel:** a power-law need/drift kernel t^{−b}, b ∈ {0.3, 0.7, 1.0}, over a span of L ∈ {2, 3, 4, 5, 6} decades.
- **Memory:** K exponential stores with free rates and weights, fitted by weighted least squares on a log grid (relative-error loss, as in SCALEFREE S3). Weights are refitted for each K, from 1 to 40.
- **Cost:** total = w·ε(K, L, b) + h·K, with w/h ∈ {10², 10³, 10⁴, 10⁵}.
- **Outputs:** K\* and the mean adjacent rate ratio r\* = geometric mean of λ_{k+1}/λ_k at K\*.
- Single process, scipy, a few minutes, memory under 200 MB.

**Locked predictions** (from SCALEFREE §2.2's sketch, K\* ≈ (L/γ)·ln(w/h)):
- **P1:** K\* rises linearly in L at fixed w/h (R² of linear > R² of L^{2/3} in ≥ 8 of 12 (b, w/h) series).
- **P2 (span invariance):** r\* varies by < 30% across L = 2…6 at fixed (b, w/h) in ≥ 9 of 12 series.
- **P3:** r\* falls as w/h rises (more stakes per unit of upkeep means denser layers), with |d ln r\*/d ln(w/h)| > 0.05 in ≥ 9 of 12 series.

**Kill rules:**
- **K1 (distinctiveness):** if r\* is insensitive to w/h (P3 fails) *and* K\* tracks the accuracy-only count from approximation theory within ±1 layer everywhere, then GTAO adds nothing to layered memory beyond approximation theory and Benna–Fusi. Prediction D is demoted to KNOWN and dropped from the short list.
- **K2:** if r\* grows with L as L^{1/3} (T7b), span invariance is false, and T7b's model stays the GTAO statement.

**Scope.** This is math, so it cannot test nature. It decides whether D is worth an empirical test. Candidate later substrates: memory-store timescales in agents or software caches, brain rhythm bands (Buzsáki & Draguhn 2004 report geometric spacing near e [M]; a POSTDICTION only), and organizational review cadences (confounded by astronomical calendars).

### Order and budget

Run N1-A first (one process, about 1 hour). Then run N1-C (minutes) at the same time or right after, since it is light. N1-B depends on the anchoring decision and on memory headroom. **Each needs its prediction block committed and hashed locally before running. Any external anchoring needs Chad's explicit go.** Every result then goes to a fresh independent reviewer. Not recommended tonight: anything on failure-rate data, P3 banks (its confound and lack of distinctiveness, §2.2 J), and any field test of A, which first needs N1-A's ρ_res.

---

## 5. What this changes in the plan (recommendations, not edits)

1. **Adopt C (§1.1) as the stated core in the next THEORY draft, with the scope rule:** C applies to design variables under selection whose resolution exceeds the cost difference. Failure rates given (σ, τ, B) are out of scope.
2. **Reframe the "profound" bet as universality plus levels:** the economics of information, made dynamic and multi-level, predicting the same dimensionless constants across substrates (§2.5). Credit Geanakoplos & Milgrom 1991, DGS 2016 and Veldkamp–Wolfers 2007 as the organizational ancestors.
3. **Put prediction A (sharedness sign flip) and prediction C (fallback cliff edge) at the front.** B (vigilance) is a new, cheap, dimensionless check that rides on the same simulations and data.
4. **Derive the architecture equation (§2.5) on Day 2.** It is the only route I can see to a prediction that is GTAO-only against economics.
5. **Close the remaining prior-art gaps** (Marschak & Radner chs. 4–6, Veldkamp ch. 8, the JEL 2023 survey, Alonso–Dessein–Matouschek 2008) before any public novelty claim.
