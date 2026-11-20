# The map of designs (`figures/face.png`, "Where the cost of judgment puts layers"): theorem, placements and sources

*v2.5.2, Friday 20 November 2026 (America/New_York). Branch `v2.5-map`. Written by a Grok Bot executor for Chad. Revised after the
independent review of PR #111 (review 26, verdict NOT READY); every blocker and should-fix is answered in §8.*

**What this map is.**
- **The shading is derived.** It shows which single layer pays on its own, which is exact in every model by definition.
- **The marker is derived.** Its shape is the cheapest design from the exact decision rule, which is right in every model.
- **When the two agree is a theorem.** They agree exactly when the layers' value is subadditive (§1).
- **The dots are hypotheses.** Every input behind a dot is a guess, apart from the cited time scales and delays.
- **E. coli is not on the map.** It is drawn beside it as a plausibility proxy.
- **A layer is a tracking store,** a memory with its own time constant. It is not an org-chart level.

Files:
- Map theorem and decision rule: `face_map.py`.
- Store model: `face_hybrid.py`.
- Which model classes are subadditive: `face_subadd.py` → `face_subadd.json`.
- Placement inputs: `face_systems.py`.
- Coordinates and uncertainty: `face_place.py`.
- Drawing: `face.py`.
- Data-collapse figure: `face_collapse.py`.
- Checks: `face_collapse_v1.py`, `face_collapse_v1b.py`, `face_collapse_v23.py`.
- Tests, including the reviewer's counterexamples: `tools/test_face_map.py`.

## 1. The map theorem (THEORY B.11)

**Setup.**
- A system has n units (n = 1 is allowed).
- For one component of the world (one time scale), there are four designs:
  - **Local:** a layer in each unit, using that unit's own reads, on time. Upkeep n·h_l; gain G_L per unit.
  - **Shared:** one layer that pools all n units' reads, which reach it a delay ℓ late. Upkeep h_c; gain G_S per unit.
  - **Both:** local layers plus a shared one. Gain G_B ≥ max(G_L, G_S) per unit.
  - **None.**
- "Gain" is the drop in expected loss that the layer buys per unit stake. The stake per unit is w_u.

**Coordinates.** Each is "stakes the layer can win ÷ its upkeep":

  X_L = w_u·G_L / h_l,   X_S = n·w_u·G_S / h_c,   and for both together  X_B = n·w_u·G_B / (n·h_l + h_c).

**Exact identities.** These hold in any model and for any loss, because they use only the definitions.
- Let ν = n·h_l / h_c, κ_S = (G_B − G_L)/G_S and κ_L = (G_B − G_S)/G_L.
- The value of each design over none, in units of n·h_l:
  - local = X_L − 1
  - shared = (X_S − 1)/ν
  - both = X_L − 1 + (κ_S·X_S − 1)/ν = (1 + 1/ν)(X_B − 1)
- So the cheapest design is the largest of (0, X_L − 1, (X_S − 1)/ν, (1 + 1/ν)(X_B − 1)). This is `decide()`, and it is always exact.
- Also (1 − κ_S)·G_S = (1 − κ_L)·G_L, so κ_S > 1 iff κ_L > 1. **Subadditivity**, G_B ≤ G_L + G_S, is κ ≤ 1.

**Map theorem (CT35).** Premises: G_L, G_S > 0 (so κ is defined), and gains that do not depend on the stake or the upkeeps. That holds when reading is fixed. It fails when reading is priced and chosen per design, because the optimized net gains then move with w_u. Fix the gains G_L, G_S, G_B. The quadrant rule below gives the cheapest design for every stake and upkeep **if and only if the
value is subadditive**, G_B ≤ G_L + G_S.

| Where | Cheapest design under subadditivity |
|---|---|
| X_L ≤ 1 and X_S ≤ 1 | **none** |
| X_L > 1 ≥ X_S | **local** (both − local = (κ_S X_S − 1)/ν ≤ 0) |
| X_S > 1 ≥ X_L | **shared** (both − shared = κ_L X_L − 1 ≤ 0) |
| X_L > 1 and X_S > 1 | **both** iff κ_L X_L > 1 and κ_S X_S > 1; otherwise local iff ν(X_L − 1) > X_S − 1 |

*Proof.*
- **If.** With κ ≤ 1, the two differences in the table are ≤ 0. In the none quadrant, X_B = (ν X_L + κ_S X_S)/(ν + 1) ≤ 1.
- **Only if.** If κ_S > 1, set X_L = X_S = 1 − ε by choice of upkeeps. Then X_B → (ν + κ_S)/(ν + 1) > 1, so both beats none in the none quadrant. Likewise, at X_S slightly below 1, both beats local in the local quadrant. ∎

**Mechanism: joint value, or a common-mode reference.**
- Superadditivity means that a layer is worth more next to the other than on its own.
- In the linear-Gaussian case at fixed rates, take two estimates with correlations r_L and r_S to the target and r_LS to each other. Then:

  (G_B − G_L − G_S)/Var = r_LS·[(r_L² + r_S²)·r_LS − 2·r_L·r_S] / (1 − r_LS²)   (`face_map.excess_fixed`, tested).

- With each estimate's sign chosen so that r_L, r_S ≥ 0 (no loss of generality), this is > 0 iff r_LS < 0 or r_LS > 2 r_L r_S/(r_L² + r_S²). Without that convention the condition is false (r_L = 0.6, r_S = −0.3, r_LS = −0.1 gives −0.032).
- That is the case when the shared store is correlated with the local estimates' *errors* more than with the target. It then works as a **common-mode reference**: subtracting it cancels noise that the local layers share.
- When the estimates are independent given the target (r_LS = r_L r_S), the excess equals r_L²r_S²(r_L² + r_S² − 2)/(1 − r_L²r_S²) ≤ 0, so the value is subadditive.
- **At optimized rates the formula is a necessary condition, not a classification.** CT35's gains are each at their own optimal rates. At the rates b* optimal for both, G_L(b*) ≤ G_L^opt and G_S(b*) ≤ G_S^opt, so G_B* − G_L^opt − G_S^opt ≤ the fixed-rate excess at b*. A positive fixed-rate excess at the joint optimum is necessary, not sufficient. Which classes are superadditive is measured below (CX6), not read off the formula.

**Prior art** (the mechanism is not new; its use for layer design is the point here):
- the suppressor variable of regression: Horst 1941 (10.1037/11521-016); Conger 1974 (10.1177/001316447403400105);
- common-mode rejection and reference channels: adaptive noise cancelling, Widrow et al. 1975 (10.1109/PROC.1975.10036);
- team theory, the value of information structures held by different members: Radner 1962 (10.1214/aoms/1177704455); Marschak & Radner 1972, *Economic Theory of Teams* (Yale University Press);
- when signals are complements: Börgers, Hernando-Veciana & Krähmer 2013, JET 148:165–195 (10.1016/j.jet.2012.12.012).

**Which model classes are subadditive** (`face_subadd.py`; sampled, not proved; 500 worlds per class):

| Class | Worlds with G_B > G_L + G_S | Largest excess (share of variance) | Status |
|---|---|---|---|
| Separate channel per component, one OU component, independent unit noise, unpriced reading (the class of every dot) | **0 / 500**; 20 adversarial maximisations: max 3×10⁻¹⁶ | 0 | subadditive, **NUMERICAL** (CX6) |
| Same, plus read noise common to all units | 28 / 500 | 0.20 | **not** subadditive |
| One read stream: a fast common part and a slow idiosyncratic part (ρ = (1, 0)) | 8 / 500 | 0.016 | **not** subadditive (counterexample B) |
| Reading priced at c/N per unit, N chosen per design (`face_collapse_v1b`; net worths) | 119 / 1500 (κ_L up to 49) | — | **not** subadditive (counterexample A; reads are paid once by both). CT35's fixed-gain premise also fails here |

- In the 1500 sampled priced worlds, none fell where the superadditivity flips the quadrant reading.
- The reviewer's counterexample A shows that such worlds exist (tested).

**Closed forms for an Ornstein–Uhlenbeck component.** The component has rate a = 1/τ and variance v, and is read through white noise of density N per unit. A share ρ of its variance is common to all units. Then (Kalman–Bucy; THEORY L1):
- G_L = v − P(v, a, N)
- G_S = e^(−2ℓ/τ) · (v_m − P(v_m, a, N/n)), where v_m = v·(ρ + (1 − ρ)/n)
- P(v, a, N) = N·a·(√(1 + 2v/(Na)) − 1)

Hence **X_S = ν · π · e^(−2ℓ/τ) · X_L**, where π is the pooling gain. A shared layer's worth falls as e^(−2ℓ/τ), so fast scales go local and slow scales go shared, *at equal read quality and with shared upkeep measured in local layers (ν)*. This is the theory's nesting (CT28, CT34), now drawn.

## 2. How the figure shows a theorem that needs three numbers

**Why this design.**
- The cheapest design depends on three values (X_L, X_S, X_B), so no 2-D picture with fixed edges is true in general.
- Three options were considered:
  - **Shading a "joint" zone.** Not principled: superadditive excess is unbounded in these coordinates.
  - **An X_B marker beside each dot.** Correct, but it adds a third number per dot to a phone-sized figure.
  - **Chosen: shade one exact fact and mark another.**
- How the chosen design works:
  - the shading says which single layer pays on its own (X_L > 1, X_S > 1). That is true by definition in every model;
  - each marker's shape and colour is the cheapest design from the full rule, which is equivalent to reading X_B;
  - the theorem says when shading and shape agree;
  - a black ring would mark a dot whose model has joint value. No dot has one (all 19 dots are in the subadditive class; the table's "joint value" column is "none" throughout).
- The footer states the general case: if a shared layer pays only as a reference for local ones, both can win below the edges.

**Axes are gross worths at the stated read quality.**
- The dots are computed at each system's stated read quality (snr), with reading unpriced.
- If reading is priced, the coordinates become net worths and the exact rule still holds. The quadrant edges do not, because value can be superadditive.

**Survival (ruin) is a gate, not a region.**
- CT33 and the regions hold where the ruin constraint is slack.
- Where ruin binds, the cheapest feasible design can differ.
- Below the minimum reserve, no design survives.
- **None** means "react, don't model". It does not mean "not viable".

**One read stream (many scales through one channel, as in a cell's receptors).**
- Per-component reading is not exact here, because one store can follow two components.
- The cheapest set of stores is found by **exhaustive search over small store counts** (`face_hybrid.best`). That is the rule.
- **Numerical guard (review 26, round 2).** Near-coincident stores make the read-out matrix ill-conditioned, and the optimizer exploited that (seed 34: a spurious error 7–75% too low). Now:
  - stores of one kind are kept ≥ 1% apart in rate;
  - a read-out matrix with condition number > 10¹⁰ is solved by a truncated pseudo-inverse, which can only understate the stores' value;
  - every reported optimum is confirmed with the Lyapunov `mse()` at rates rounded to 6 significant digits, and the larger error is reported.
  All the runs below were redone with the guard.
- Adding stores one at a time by marginal worth (greedy) is exact when marginal worths are submodular. That is not guaranteed: counterexample B has κ > 1, and greedy stops at NONE while local + shared together pay.

The earlier check (v2.5) claimed greedy 600/600. **It used ρ = 1 throughout and ≤ 2 stores per location, so it could not see this case.** The rerun (`face_collapse_v23.py`, 800 two-scale worlds, ≤ 2 local and ≤ 2 shared stores). **These numbers hold only in this tested scope.** Regret is a fraction of the optimal total cost.

| Worlds | Greedy = exact | Worst greedy regret | Greedy + pairwise look-ahead = exact | Per-component reading = exact |
|---|---|---|---|---|
| ρ = 1 (400) | 100% | 0 | 100% | 50.5% |
| ρ drawn per component (400) | 99.5% (2 misses) | 2.2×10⁻⁵ of total cost | 100% | 47% |

- **Outside the tested scope the look-ahead also misses.** Review 26 ran 92 three- and four-scale worlds with up to 3 local + 3 shared stores.
  - Seed 40 is a real miss for greedy and for greedy + look-ahead. The optimum is 2 local + 3 shared stores (cost 4280.549). Greedy goes 1 → 2 → 3 local stores, then adds shared stores to 3 + 2 (4281.731) and stops. The regret is 2.8×10⁻⁴ of total cost. This was reproduced here with the guarded optimizer (12 starts per design): the same costs to 4 significant figures, and the same greedy path.
  - Additions cannot undo the third local store, so outside the tested scope only exhaustive search is the rule.
  - Its other miss (seed 34, regret 3.04) was the ill-conditioning artifact that the guard above removes.
- V2 (one stream, layer count): marginal worths fell layer by layer in 97.3% of 300 worlds, and in 100% within a 10⁻⁵ tolerance. 0 of the 300 fits failed.
- The earlier crash (seed 139, error −∞) was a numerically unstable solve. The solver now rejects non-finite or negative errors and retries with 30 starts.
- The remaining 2.7% are rises below 10⁻⁵ of total error. They are within the optimizer's tolerance and are not evidence either way.

**Data collapse** (`face_collapse.png`):
- (a) 3000 random worlds in raw inputs: the best designs overlap.
- (b) The same worlds in (X_L, X_S). The closed forms plus the decision rule agree with brute force in 3000/3000, and κ ≤ 1 holds in all of them. The closed-form gains agree with numerics to 4×10⁻¹⁴ and 5×10⁻¹¹.
- (c) The upper-right split: both iff κ_L X_L > 1 and κ_S X_S > 1.
- (d) Reading priced: κ > 1 in 119 of 1500 worlds (circled). In this sample no circled world falls where shading ≠ best design. Counterexample A shows that one can.

## 3. Layers are tracking stores, not management levels

**What counts as a layer.**
- A layer is a store: a state the system holds that follows the world with its own time constant.
- An org-chart level counts only if it holds such a state, with a distinct measured time constant (§4).
- A level that only relays reads is not a layer. That is the "telling" of CT16.

**One shared level per component.**
- The map shows one shared level per component. Hierarchies arise by applying the same rule along the member axis:
  - a shared level forms once enough members face a common driver (CT14);
  - nested levels pay when their time scales separate (CT28, CT34);
  - a team's optimized cost enters its parent's problem as upkeep (CT34).
- So a firm's "management" component is the firm-wide store. Its divisions would be the same map applied one level down.

## 4. An operational rule for counting a real system's layers (proposed; preregister per class before use)

1. **Fix the pair and the band.** Before any data, fix per class the input/output pair and the band of time scales:

   | Class | Input (drive) | Output (read-out) | Band |
   |---|---|---|---|
   | bacterium | attractant step or noise | motor bias (CW/CCW) | 0.1 s–10 min |
   | immune system | antigen dose | antigen-specific antibody / T-cell titre | 1 h–50 y |
   | ant colony | food offered at a site | forager flow to that site; colony intake | 1 min–1 mo |
   | team, firm | demand or task arrivals | allocation of effort or spend | 1 d–10 y |
   | city, nation-state, global economy | a documented shock (price, fiscal, climate) | allocation response (spend, land use, rates) | 1 mo–50 y |

2. **Measure the response kernel** over that band (impulse, step or white-noise input), by a protocol fixed in advance.
3. **Fit sums of exponentials** (complex-conjugate pairs allowed) of order K = 1 … K_max, separately to the isolated-unit response and to the pooled response (step 6 says how each is obtained).
   - Accept order K + 1 over K only if **ΔBIC ≥ 10**.
   - Poles outside the band are not counted.
   - **Classify, then merge.** Classify each pole as local or shared (step 6) *before* any merging. Then merge only within a class: two poles of the same class whose time constants differ by less than a **factor 3** (the resolution) count as one. A local and a shared pole are never merged, however close, so "both" stays observable.
4. **Count by degree.** The layer count is the number of poles: a complex pair (a rhythm) counts 2, and an integrator-plus-filter counts 2.
5. **Relay-only test.** Remove the candidate level, or bypass it, or replace it with a pure delay of the same latency, and refit.
   - The level is a layer only if a pole disappears or moves by more than the resolution factor.
   - If only a delay disappears, it is a relay (CT16).
6. **Local vs shared** (applied in step 3, before merging).
   - *Local:* the pole appears in each unit's own response, measured on isolated units.
   - *Shared:* it appears only in the pooled response and disappears when units are isolated.
   - Where isolation is impossible, use the substitute fixed in advance: per-unit vs pooled response to unit-specific vs common drives.
7. **Assign poles to dots** (fixed in advance).
   - A pole belongs to a dot if its time constant lies inside that dot's τ range widened by a factor 3 at each end. If it fits several dots, it goes to the one whose range centre (in log τ) is nearest.
   - A dot's observed design is **none** (no pole), **local** (local poles only), **shared** (shared poles only) or **both** (at least one of each).
   - A pole that matches no dot is a **miss** (an unpredicted layer).
   - **Only degree-1 components are compared.** B.11 is proved for one store per design per component. Degree-2 components (rhythms, integrator + filter, as in E. coli) are counted and reported but not scored until B.11 is extended.
8. **Compare with the map, with a miss rule against the per-dot share of draws.**
   - It is a **pass** if the observed design has ≥ 50% of that dot's draws.
   - It is a **miss** if the observed design has < 10% of draws.
   - Between 10% and 50% is inconclusive.
   - A system misses if any of its components misses.
9. **The prediction is frozen.**
   - The input ranges in `figures/face_systems.py` are the preregistered prediction, frozen on 20 Nov 2026 (ET) with SHA-256 `00f6f25d796bbd1862f6ad9f04ef53bd986185f1177052339632e20b15095377`.
   - `tools/test_face_map.py` fails if the file changes.
   - Any later change to a class's ranges voids the comparison for that class. A new prediction needs a new freeze date before any data.

| System | Observed by this rule | Map gives |
|---|---|---|
| E. coli | not counted by this rule (degree 2: reported, not scored). A two-pole kernel G·e^(−t/τ2)(1 − e^(−t/τ1)) was fitted to 442 cells (Mattingly et al. 2021; PR #110), but not with this rule's ΔBIC selection or relay test | off the map (one cell; proxy only) |
| every other system | not yet measured by the rule | see table |

## 5. Placements (hypothesized positions, not measurements)

**How the table is built.**
- Times are given as ranges.
- Each dot is the centre of its input ranges:
  - log-uniform draws for every input except ρ, which is drawn uniformly;
  - 400 draws per dot;
  - the ellipses are the 1σ (main figure) or 2σ (`face_all.png`) covariance in log space.
- "Share of draws" is how often each design wins across the input ranges.
- A dot is drawn **hollow** when no design wins ≥ 65% of its input draws. Solid dots can also change design within their ranges, just less often (the share column gives the numbers).
- Systems whose selection is weak or unknown are starred (*).
- "Joint value" is the share of draws with G_B > G_L + G_S. It is none for every dot.
- `figures/face_table.py` writes this table from `face_dots.json`. `tools/test_face_map.py` checks every design and X_B against the coordinates.

<!-- TABLE -->
| System | Scale | τ | delay ℓ | units n | shared ρ | snr | stakes ÷ upkeep R | h_c ÷ h_l | X_L (centre) | X_S (centre) | X_B (centre) | κ_L, κ_S | cheapest design | share of draws | joint value | sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E. coli | gradient signal | 1.16 s | 0.039 s–0.3 s | 1 | 1 | 0.0043–0.103 | proxy 10^-0.26–10^1.89 | 1 | 6.53 | — | — | — | **off the map (proxy)** | proxy > 1 in 88% | — | plausibility proxy, not on the map: PR #110 `theory/measured/measured.json` (Mattingly et al. 2021, 10.1038/s41567-021-01380-3; Ni et al. 2019, PNAS, issued 23 Dec 2019, 10.1073/pnas.1910849117); the ratio is motility benefit ÷ signalling proteome share, not X_L; degree 2, outside B.11; do not merge before PR #110 |
| immune system | innate | 1 h–10 h | 12 h–2 d | 100–1000 | 0.1–0.5 | 1–30 | 30–3e+03 | 3–100 | 131 | 0.000388 | 124 | 1.00, 0.00 | **local** | local 99% | none | lead as adaptive (Randolph et al. 2005); rest guess |
| immune system | adaptive | 5 d–4.29 wk | 12 h–2 d | 100–1000 | 0.5–1 | 0.3–10 | 3–300 | 3–100 | 7.38 | 316 | 17.1 | 0.10, 0.62 | **shared** | shared 62%, both 38% | none | lead: dendritic-cell trafficking to lymph nodes, Randolph, Angeli & Swartz 2005 (10.1038/nri1670); rest guess |
| immune system | memory | 10 y–100 y | 1 d–1 wk | 100–1000 | 0.7–1 | 10–1e+03 | 0.3–30 | 3–100 | 2.46 | 46 | 2.57 | 0.08, 0.10 | **shared** | shared 82%, both 15%, none 2%, local 1% | none | tau: antibody half-lives 11 y (tetanus) to >200 y (measles, mumps), Amanna, Carlson & Slifka 2007 (10.1056/NEJMoa066092); rest guess |
| ant colony | patch | 20 min–3 h | 15 min–45 min | 100–1000 | 0–0.3 | 0.3–10 | 3–300 | 1–30 | 7.38 | 89.4 | 7.71 | 0.85, 0.30 | **both** | both 70%, local 16%, shared 13%, none 2% | none | Lasius niger. Shared store = the pheromone trail; tau: trail lifetime ~47 min, Beckers, Deneubourg & Goss 1993 (10.1007/bf01201674; figure from secondary citations, full text not checked). Local store = private route memory, Grüter, Czaczkes & Ratnieks 2011, online 2010 (10.1007/s00265-010-1020-2). rho 0–0.3 (v2.5 range; v2.5.1 had raised it, reverted): a trail serves only the foragers working that patch (guess); rest guess |
| ant colony | food supply | 6 h–1 wk | 15 min–45 min | 100–1000 | 0.7–1 | 0.03–1 | 0.3–30 | 1–30 | 0.12 | 107 | 1.83 | 0.03, 0.94 | **shared** | shared 100% | none | Lasius niger. Hypothesized shared store = crop food passed by trophallaxis (the colony's stomach, which every worker's hunger reads); rho 0.7–1 because colony-wide hunger is common to all workers (guess); rest guess |
| small team | tasks | 1 d–5 d | 2 h–12 h | 5–10 | 0.3–0.8 | 1–30 | 1–30 | 0.5–3 | 2.39 | 10.6 | 2.27 | 0.34, 0.15 | **shared** | shared 56%, both 26%, local 15%, none 2% | none | guess |
| small team | goals | 1 mo–6 mo | 1 d–1 wk | 5–10 | 0.8–1 | 3–100 | 1–30 | 0.5–3 | 3.4 | 22.1 | 3.42 | 0.05, 0.16 | **shared** | shared 88%, both 10%, local 2% | none | guess |
| firm | operations | 1 d–1 wk | 1 wk–1.15 mo | 10–300 | 0.1–0.5 | 1–30 | 30–3e+03 | 3–30 | 131 | 0.00322 | 112 | 1.00, 0.00 | **local** | local 99%, both 1% | none | guess |
| firm | management | 1 mo–6 mo | 2 wk–1.84 mo | 10–300 | 0.5–0.9 | 1–30 | 3–300 | 3–30 | 13.1 | 50.4 | 12.2 | 0.42, 0.14 | **both** | both 59%, local 28%, shared 13% | none | guess |
| firm | strategy | 2 y–10 y | 1 mo–3 mo | 10–300 | 0.7–1 | 1–30 | 1–100 | 3–30 | 4.36 | 40.9 | 6.2 | 0.05, 0.41 | **shared** | shared 81%, both 16%, none 2%, local 1% | none | guess |
| city* | services | 6 h–3 d | 3 d–4.29 wk | 10–100 | 0–0.3 | 1–30 | 10–1e+03 | 3–30 | 43.6 | 1.27e-08 | 33.6 | 1.00, 0.00 | **local** | local 100% | none | guess |
| city* | budget | 1 y–4 y | 1 mo–6 mo | 10–100 | 0.5–0.9 | 1–30 | 1–100 | 3–30 | 4.36 | 16.3 | 4.41 | 0.20, 0.28 | **shared** | shared 44%, both 39%, local 10%, none 6% | none | guess |
| city* | land use | 10 y–50 y | 6 mo–2 y | 10–100 | 0.5–1 | 3–100 | 1–100 | 3–30 | 6.21 | 21.2 | 5.59 | 0.16, 0.17 | **shared** | shared 47%, both 39%, local 11%, none 2% | none | guess |
| nation-state* | local | 1 d–4.29 wk | 1 mo–3 mo | 10–100 | 0–0.3 | 1–30 | 10–1e+03 | 3–100 | 43.6 | 1.02e-07 | 28.3 | 1.00, 0.00 | **local** | local 100% | none | guess |
| nation-state* | business cycle | 2 y–8 y | 1 mo–3 mo | 10–100 | 0.5–0.9 | 1–30 | 1–300 | 3–100 | 7.55 | 17.7 | 6.98 | 0.16, 0.34 | **both** | both 48%, shared 38%, local 10%, none 4% | none | lead: data-release lags, Giannone, Reichlin & Small 2008 (10.1016/j.jmoneco.2008.05.010); rest guess |
| nation-state* | institutions | 20 y–100 y | 3 mo–2 y | 10–100 | 0.7–1 | 3–100 | 1–100 | 3–100 | 6.21 | 14 | 5.15 | 0.06, 0.23 | **shared** | shared 63%, both 23%, local 11%, none 2% | none | guess |
| global economy* | markets | 1 h–1 wk | 1 mo–6 mo | 50–200 | 0–0.5 | 1–30 | 10–1e+03 | 10–1e+03 | 43.6 | 3.76e-119 | 21.8 | 1.00, 0.00 | **local** | local 100% | none | guess |
| global economy* | world cycle | 3 y–10 y | 1 mo–6 mo | 50–200 | 0.3–0.8 | 1–30 | 1–100 | 10–1e+03 | 4.36 | 4.59 | 2.94 | 0.30, 0.33 | **both** | local 30%, both 30%, shared 29%, none 10% | none | guess |
| global economy* | climate | 30 y–300 y | 1 y–5 y | 50–200 | 0.8–1 | 1–100 | 0.3–30 | 10–1e+03 | 1.61 | 2.41 | 1.23 | 0.03, 0.35 | **shared** | shared 57%, none 24%, local 15%, both 3% | none | guess |
<!-- /TABLE -->

**Notes on individual placements.**
- **E. coli is a plausibility proxy, not a placement (PR #110 inputs; do not merge before PR #110).**
  - The ratio is the fitness benefit of chemotaxis in poor carbon (Ni et al. 2019, PNAS, issued 23 Dec 2019) divided by the signalling machinery's proteome share: log₁₀ −0.26 to 1.89.
  - It is **not X_L**, for three reasons:
    - the benefit includes motility, while the denominator counts only signalling;
    - a proteome share is not a fitness cost;
    - the component is degree 2, which is outside B.11's one-store-per-layer setup.
  - It is therefore drawn in its own strip beside the map, not on the "≈ 0" band.
  - It says only that the measured benefit is plausibly larger than the signalling proteome share; neither is X_L. In glucose the benefit is about 0, and the cell does cut motility there (Ni et al.).
  - **Caveat:** PR #110 found that the slow store's memory (9.9 s) is 8.5× the optimum under exogenous noise. This proxy does not test the memory time.
- **Ant colony: one species, *Lasius niger*, with named stores.**
  - *Patch.*
    - The shared store is the pheromone trail. Its lifetime is ~47 min (Beckers, Deneubourg & Goss 1993). That figure is taken from secondary citations; the full text was not checked.
    - The local store is each forager's private route memory (Grüter, Czaczkes & Ratnieks 2011, online 2010).
    - ρ = 0–0.3, the v2.5 range. A trail marks one route and serves only the foragers working that patch, so little of what one forager meets is met by all. This is a guess.
  - *Food supply.*
    - The hypothesized shared store is crop food passed by trophallaxis (the colony's "social stomach"), which every worker's hunger reads.
    - ρ = 0.7–1 because colony hunger is common to all workers. This is a guess.
  - The v2.5 citation of Prabhakar et al. 2012 (a harvester ant) was dropped so that the species are no longer mixed.
  - **Disclosure: a post-review change, now reverted.**
    - v2.5.1 raised the patch's ρ from 0–0.3 to 0.3–0.9 after the coordinates had been computed. The reason it gave (a trail serves only that patch's foragers) argues for a *lower* common share, not a higher one.
    - Review 26 (round 2) caught this, and the v2.5 range is restored: inputs are frozen (§4, step 9).
    - Effect on the pick: the pick is **both** either way. With ρ = 0.3–0.9 the shares were both 70%, shared 27%, local 2%. With ρ = 0–0.3 restored they are both 70%, local 16%, shared 13%, none 2%, as in v2.5. X_S at the centre falls from 392 to 89, X_L is unchanged at 7.4, and the dot stays solid.
  - Apart from this change, the inputs were set from the biology before the coordinates were computed. They were not preregistered until the freeze in §4.
- **Immune memory:** antibody half-lives run from 11 y (tetanus) and 19 y (diphtheria) to about 50 y (varicella-zoster) and >200 y (measles, mumps) (Amanna, Carlson & Slifka 2007, abstract checked).
- **Order.** Systems are numbered 1–7 from small to large for reading only. Each dot's code (e.g. 2b) gives its system and scale, and no order is implied by position.

## 6. What is proved, what is only numerical, what is guessed

| Item | Status |
|---|---|
| Exact rule: cheapest = argmax(0, X_L − 1, (X_S − 1)/ν, (1 + 1/ν)(X_B − 1)) | **Proved** (identity; any model, any loss) |
| Map theorem: quadrant edges decide outside the upper-right quadrant for all stakes and upkeeps iff G_B ≤ G_L + G_S | **Proved** (in-model; CT35) |
| Joint value as a common-mode reference; fixed-rate excess formula | **Proved** (linear-Gaussian, fixed rates; CT36); prior art credited |
| κ ≤ 1 in the separate-channel, independent-noise, unpriced OU class | **Numerical only** (CX6: 500 + 3000 worlds, 20 adversarial runs) |
| κ ≤ 1 with priced reading, common read noise, or mixed-rate one stream | **False** (counterexamples A and B; counts above) |
| OU closed forms for G_L, G_S; X_S = ν·π·e^(−2ℓ/τ)·X_L | **Proved** (Kalman–Bucy); numerically confirmed to 10⁻¹³ to 10⁻¹¹ |
| One stream: greedy store-by-store | **False in general** (counterexample B). In the tested scope (2 scales, ≤ 2 + 2 stores) greedy matched in 99.5–100% of samples and the pairwise look-ahead in 800/800 (numerical). Outside it the look-ahead misses too (review 26, 3 scales, seed 40) |
| CT33 on the map (spend never falls as stakes rise, ruin slack) | Follows from CT33; tested on 200 worlds |
| Every dot's inputs | **Guessed**, except the cited time scales and delays |

## 7. Referee's list (written by the author; not an independent review)

1. **The dots are guesses.** Stakes ÷ upkeep (R) is unmeasured everywhere (GAPS G3). Shared-store upkeep h_c/h_l is a guess everywhere.
2. **Subadditivity is sampled, not proved,** even in the class of the dots (CX6). Outside it, the shading is not the design. The markers still are.
3. **The model class is narrow.** Components are linear-Gaussian OU with first-order stores. Real worlds have saturation, heavy tails and non-stationarity.
4. **The one-stream rule is sampled** on two scales and ≤ 2 stores per location.
5. **9 of the 19 mapped dots are hollow** (no design wins ≥ 65% of draws).
6. **The ellipses are not posteriors.** They come from independent ranges.
7. **Ruin is not drawn.**
8. **The hierarchy above one shared level is not drawn.**
9. **E. coli is a proxy off the map.** It depends on PR #110, which is not yet merged.
10. **City, nation-state and global economy are starred** because their selection is weak or unknown.
11. **The counting rule is proposed.** It has not been preregistered per class, and no system has been counted by it yet.
12. **Beckers' 47 min** is not checked against the full text.

## 8. History

- **The v2.4 figure** (one made-up 14-scale world, regions from assumed sensing and ruin knobs) was withdrawn in `bc9a1ec` after review 3.
  - Its federation boundary values 22, 105 and 376 (n = 3, 10, 30 at ℓ = 1) were **optimized-sensing** values. The fixed-sensing closed form gives 28.5, 128 and 414.
  - Its word for the sensing spend should have been "sensing cost".
- **v2.5** introduced the map theorem.
- **v2.5.1 answers review 26 (NOT READY):**
  1. **False universality of the edges.**
     - The theorem is now stated as an iff on subadditivity.
     - The classes are measured (`face_subadd.py`).
     - The mechanism is named, and prior art is credited.
  2. **Reading price "moves dots, never edges".** Withdrawn. Counterexample A is a regression test, and v1b is relabelled as an identity check.
  3. **Greedy one-stream rule.** Withdrawn as a rule.
     - The old check used ρ = 1 and ≤ 2 stores.
     - The new V3 draws ρ per component in half of its worlds.
     - Counterexample B is a test.
     - The stated rule is exhaustive search, with a pairwise look-ahead.
  4. **"BOTH PAY" label.** Replaced: the regions now say which single layer pays on its own, and the shape gives the pick.
  5. **Axis "net of reading" while the dots are gross.** The axes now say "at the stated read quality".
  6. **E. coli as measured X_L.** Now a plausibility proxy, off the map. Do not merge before PR #110.
  7. **B.11 in the claim index.** Added to THEORY Appendix C and CLAIM_MAP §O as CT35, CT36 and CX6.
  8. **Tests.**
     - The quadrant vs decide disagreement at κ > 1 is now tested.
     - Counterexamples A and B are tests.
     - The 100% greedy assertion is dropped.
  9. **V2 crash.** Fixed. The "optimizer noise" wording is replaced by the tolerance statement.
  10. **Missing systems in the side panel.** All 7 multi-unit systems are listed and numbered, and E. coli has its own strip.
  11. **Clutter.**
      - Dot codes replace the chains.
      - Labels are placed deterministically.
      - `face_all` is now dpi 120 with font ≥ 9.
  12. **face_collapse titles.** Retitled; the clipped note is readable.
  13. **Citations.**
      - Ni et al. is dated 2019.
      - Amanna's half-lives are corrected per the abstract.
      - Beckers' 47 min is marked unchecked.
  14. **Counting rule.** Made numeric:
      - ΔBIC ≥ 10 and resolution factor 3;
      - the I/O pair and band per class;
      - a relay-only test;
      - the miss rule.
  15. **Ant stores.** The ant stores are named, ρ is justified, and the species are *Lasius* only.
  16. **One-stream check and F1.**
      - The one-stream check now states ρ and store limits.
      - F1 now says ν and "at equal read quality".

- **v2.5.2 answers review 26, round 2 (READY-WITH-FIXES):**
  - **Must-fixes.**
    1. Hollow legend: "no design wins ≥ 65% of its input draws".
    2. The shading sentence is limited to outside the top-right.
    3. The ν gloss is fixed: all local layers' upkeep ÷ the shared layer's upkeep.
    4. 1b/2a in `face.png`: the two no longer overlap, because 2a moved once its input was restored (item 5).
    5. The ant patch ρ is reverted to 0–0.3 and the change is disclosed (§5 notes). The pick stays **both**.
    6. CT36: the sign convention is added, and the formula is stated as necessary, not sufficient, at optimized rates.
  - **Should-fixes.**
    7. Counting rule:
       - classify, then merge (so "both" is observable);
       - pole-to-dot assignment;
       - degree-1 scoring only;
       - inputs frozen by SHA-256 and date, with a test.
    8. Conditioning guard (rates ≥ 1% apart, truncated solve above cond 10¹⁰, Lyapunov confirmation of each optimum). V1, V1b, CX6 and V3 were rerun with it.
    9. The one-stream claims are scoped to what was tested, and the three-scale miss (seed 40) is reported.
    10. "Of total cost" replaces "of value".
    11. The E. coli inset no longer shows shading or an edge, and is captioned "the map's edges do not apply".
    12. CT35's premises are stated.
    13. Grüter et al. 2011 (online 2010).
  - Every sentence on the four PNGs was reread against the code and data. Changes made on that pass:
    - E. coli's denominator now says "signalling proteome share", not "cost";
    - collapse panel (d) now says "quadrant rule ≠ best design";
    - the clipping note was corrected;
    - `face_all.png` gained its own legend.

## 9. Regenerate

```
nice -n 19 python3 figures/face_collapse_v1.py 3000     # about 2 min: random worlds, exact rule vs brute force
nice -n 19 python3 figures/face_collapse_v1b.py 1500    # about 3 min: reading priced (identity check)
nice -n 19 python3 figures/face_collapse_v23.py 300 800 # about 8 min: one read stream (V2 300, V3 800 worlds)
nice -n 19 python3 figures/face_subadd.py 1500          # about 4 min: which classes are subadditive
nice -n 19 python3 figures/face_place.py                # about 1 min: placements -> face_dots.json
nice -n 19 python3 figures/face_table.py                # the table above
nice -n 19 python3 figures/face.py                      # face.png (1600x1000), face_square.png (1200x1200), face_all.png
nice -n 19 python3 figures/face_collapse.py             # face_collapse.png
nice -n 19 python3 -m pytest -q tools/test_face_map.py
```
