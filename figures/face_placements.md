# The map of designs (`figures/face.png`, "Where the cost of judgment puts layers"): theorem, placements and sources

*v2.5, Friday 20 November 2026 (America/New_York). Branch `v2.5-map`. Written by a Grok Bot executor for Chad. It checks itself
and has **not** been independently reviewed. The map replaces the v2.4 figure withdrawn in `bc9a1ec`.*

**What this map is.**
- **The regions are derived.** They are a theorem of the cost of judgment, J = upkeep + stakes × error + reading cost.
- **The dots are hypotheses.** Every input behind a dot is a guess, except E. coli's, which uses a measured proxy from PR #110.
- **A layer is a tracking store,** a memory with its own time constant. It is not an org-chart level.

Files:
- Regions: `face_map.py`.
- Store model: `face_hybrid.py`.
- Placement inputs: `face_systems.py`.
- Coordinates and uncertainty: `face_place.py`.
- Drawing: `face.py`.
- Data-collapse figure: `face_collapse.py`.
- Checks: `face_collapse_v1.py`, `face_collapse_v1b.py`, `face_collapse_v23.py`.
- Tests: `tools/test_face_map.py`.

## 1. The map theorem (THEORY B.11)

**Setup.**
- A system has n units (n = 1 is allowed).
- The world is a sum of independent components, one per time scale. Each component is read by the units through its own channel.
- For one component, there are four designs:
  - **Local:** a layer in each unit, using that unit's own reads, on time. Upkeep n·h_l; gain G_L per unit.
  - **Shared:** one layer that pools all n units' reads, which reach it a delay ℓ late. Upkeep h_c; gain G_S per unit.
  - **Both:** local layers plus a shared one. Gain G_B per unit.
  - **None.**
- "Gain" is the drop in expected loss that the layer buys per unit stake. The stake per unit is w_u.

**Coordinates.** Each axis is "stakes the layer can win ÷ its upkeep":

  X_L = w_u·G_L / h_l,    X_S = n·w_u·G_S / h_c.

**Two more numbers.**
- ν = n·h_l / h_c: how many local layers' upkeep one shared layer costs.
- κ_S = (G_B − G_L)/G_S and κ_L = (G_B − G_S)/G_L: the share of each layer's gain that the other layer does not already supply.

**Value of each design over none**, in units of n·h_l (each line is stakes won minus upkeep):
- local = X_L − 1
- shared = (X_S − 1)/ν
- both = X_L − 1 + (κ_S·X_S − 1)/ν

**Proof.** Divide each value by n·h_l. For "both", use G_B = G_L + κ_S·G_S. The identity (1 − κ_S)·G_S = (1 − κ_L)·G_L gives both − shared = κ_L·X_L − 1. With 0 ≤ κ ≤ 1:

| Where | Best design | Which numbers decide |
|---|---|---|
| X_L ≤ 1 and X_S ≤ 1 | **none** | only X_L, X_S |
| X_L > 1, X_S ≤ 1 | **local** (both − local = (κ_S X_S − 1)/ν ≤ 0) | only X_L, X_S |
| X_S > 1, X_L ≤ 1 | **shared** (both − shared = κ_L X_L − 1 ≤ 0) | only X_L, X_S |
| X_L > 1 and X_S > 1 | **both** iff κ_L X_L > 1 and κ_S X_S > 1; otherwise local iff ν(X_L − 1) > X_S − 1 | ν, κ_L, κ_S as well |

**Assumptions behind the theorem.**
- κ ≥ 0 because an added layer can be given zero gain.
- κ ≤ 1 is subadditivity, G_B ≤ G_L + G_S. This is **verified numerically, not proved**:
  - it held in every one of the 3000 + 15 random worlds tried;
  - the largest κ_S found was 0.99, and the largest κ_L was 1 − 3×10⁻¹⁰.
- Costs add across components when each component has its own read channel (the theory's 𝒜₁ class), so each component is placed on its own.

**Closed forms for an Ornstein–Uhlenbeck component.** The component has rate a = 1/τ and variance v, and is read through white noise of density N per unit. A share ρ of its variance is common to all units. Then (Kalman–Bucy; THEORY L1):
- G_L = v − P(v, a, N)
- G_S = e^(−2ℓ/τ) · (v_m − P(v_m, a, N/n)), where v_m = v·(ρ + (1 − ρ)/n)
- P(v, a, N) = N·a·(√(1 + 2v/(Na)) − 1)

Hence **X_S = ν · π · e^(−2ℓ/τ) · X_L**, where π is the pooling gain. A shared layer's worth falls as e^(−2ℓ/τ), so fast scales go local and slow scales go shared. This is the theory's nesting (CT28, CT34), now drawn.

## 2. What the axes absorb, and what a single 2-D map cannot show

**Absorbed into the coordinates:**
- **The world's spectrum.** Each component is its own dot. A rhythm or an integrated signal is one component of degree 2, so it gets 2 stores.
- **Read noise.**
- **Delay.** It enters only as e^(−2ℓ/τ).
- **Number of units, and how much of the world they share.** These enter through π and ν.
- **The reading price.**
  - With reading priced at c/N per unit and N chosen per design, the coordinates become *net* worths. The same edges then decide.
  - `face_collapse_v1b.py` checks this: 1500 random worlds, numerical optimum vs the map's reading, **100% agreement**.
  - So the reading price that review 3 found driving the v2.4 figure (C0) moves dots. It never moves edges.
- **The loss function.** Only gains in expected loss enter.

**Not on one 2-D map, by the theorem itself.**
- Inside the upper-right quadrant, the choice between local, shared and both also depends on ν, κ_L and κ_S.
- No pair of axes can absorb these, because each dot has its own values.
- So the map draws each dot with its own design (circle = local, square = shared, diamond = both).
- Panel (c) of `face_collapse.png` shows that split: both iff κ_L X_L > 1 and κ_S X_S > 1.
- **The edges X_L = 1 and X_S = 1 are universal. The split of the upper-right quadrant is per dot.**

**Survival (ruin) is a gate, not a region.**
- CT33 and the regions hold where the ruin constraint is slack.
- Where ruin binds, the cheapest feasible design can differ.
- Below the minimum reserve, no design survives.
- The v2.4 "NOT VIABLE" region came from an assumed income (η = 1.5). It covered the zero-layer region, so it is gone.
- **None** here means "react, don't model". It does not mean "not viable".

**One read stream (many scales through one channel, as in a cell's receptors).** The per-component reading is not exact here, because one store can follow two components.
- Place layers **one at a time by marginal worth.**
- `face_collapse_v23.py` (V3) tested two-scale worlds with up to 2 local and 2 shared stores (600 worlds):
  - the layer-by-layer reading matched the exact optimum in **600/600**, regret 0;
  - reading each scale as if it had its own channel matched in only **51%** (regret median 0, 90th percentile 12%), because it overstates slow layers.
- V2 (one stream, layer count): marginal worths fell layer by layer in 97% of 300 worlds, and in 99.7% within a 10⁻⁵ tolerance. The exceptions are optimizer noise.

**Data collapse** (`face_collapse.png`):
- (a) 3000 random worlds in raw inputs: the best designs overlap.
- (b) The same worlds in (X_L, X_S): the edges at 1 separate them exactly (3000/3000; closed-form gains agree with numerics to 4×10⁻¹⁴ and 5×10⁻¹¹).
- (c) The κ split.
- (d) Reading priced.

## 3. Layers are tracking stores, not management levels

**What counts as a layer.**
- A layer is a store: a state the system holds that follows the world with its own time constant.
- An org-chart level counts only if it holds such a state, with a distinct measured time constant.
- A level that only relays reads is not a layer. That is the "telling" of CT16.

**One shared level per component.**
- The map shows one shared level per component. Hierarchies arise by applying the same rule along the member axis:
  - a shared level forms once enough members face a common driver (CT14);
  - nested levels pay when their time scales separate (CT28, CT34);
  - a team's optimized cost enters its parent's problem as upkeep (CT34).
- So a firm's "management" component on the map is the firm-wide store. Its divisions would be the same map applied one level down.

## 4. An operational rule for counting a real system's layers (proposed; to be preregistered per class)

1. **Measure the response.** Measure the system's response kernel to the driving signal (impulse, step, or white-noise input) over the band of time scales in question, by a protocol fixed in advance.
2. **Fit sums of exponentials.** Fit sums of exponentials, complex-conjugate pairs allowed, of order K = 1, …, K_max. Choose K by a preregistered criterion (for example BIC, or held-out prediction error with a stated threshold).
   - Two poles closer than a preregistered resolution factor count as one.
3. **Count by degree.** The layer count is the number of poles: a complex pair (a rhythm) counts 2, and an integrator-plus-filter like E. coli's counts 2.
4. **Classify each pole.**
   - *Local:* it appears in each unit's own response, measured on isolated units.
   - *Shared:* it appears only in the pooled response, and disappears when units are isolated.
5. **Compare.** Compare this count, and the local/shared split, with the map's prediction per component.

| System | Observed by this rule | Map gives |
|---|---|---|
| E. coli | **2**, local. The kernel G·e^(−t/τ2)(1 − e^(−t/τ1)) was fitted to 442 cells (Mattingly et al. 2021; PR #110); the two-pole fit was not chosen by this rule's preregistered selection | 2 (one degree-2 component, local) |
| every other system | not yet measured by the rule | see table |

## 5. Placements (hypothesized positions, not measurements)

**How the table is built.**
- Times are given as ranges.
- Each dot is the centre of its input ranges:
  - log-uniform draws for every input except ρ, which is drawn uniformly;
  - 400 draws per dot;
  - the ellipses are the 1σ (main figure) or 2σ (`face_all.png`) covariance in log space.
- "Share of draws" is how often each design wins across the input ranges. A dot is drawn hollow or dashed when its system's selection is weak or unknown (marked *).
- A dot is called "near edge" when no design wins ≥ 65% of draws.
- `figures/face_table.py` writes this table from `face_dots.json`. `tools/test_face_map.py` checks every "map gives" against the coordinates.

<!-- TABLE -->
| System | Scale | τ | delay ℓ | units n | shared ρ | snr | stakes ÷ upkeep R | h_c ÷ h_l | X_L (centre) | X_S (centre) | map gives | share of draws | sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E. coli | gradient signal | 1.16 s | 0.039 s–0.3 s | 1 | 1 | 0.0043–0.103 | proxy 10^-0.26–10^1.89 | 1 | 6.53 | — | **local** | local 88%, none 12% | all inputs measured or proxy: PR #110 `theory/measured/measured.json` (Mattingly et al. 2021, 10.1038/s41567-021-01380-3; Ni et al. 2019, 10.1073/pnas.1910849117); X_L is a proxy (benefit / proteome share) |
| immune system | innate | 1 h–10 h | 12 h–2 d | 100–1000 | 0.1–0.5 | 1–30 | 30–3e+03 | 3–100 | 131 | 0.000388 | **local** | local 99% | lead as adaptive (Randolph et al. 2005); rest guess |
| immune system | adaptive | 5 d–4.29 wk | 12 h–2 d | 100–1000 | 0.5–1 | 0.3–10 | 3–300 | 3–100 | 7.38 | 316 | **shared** | shared 62%, both 38% | lead: dendritic-cell trafficking to lymph nodes, Randolph, Angeli & Swartz 2005 (10.1038/nri1670); rest guess |
| immune system | memory | 10 y–100 y | 1 d–1 wk | 100–1000 | 0.7–1 | 10–1e+03 | 0.3–30 | 3–100 | 2.46 | 46 | **shared** | shared 82%, both 15%, none 2%, local 1% | tau: antibody half-lives 11 to >200 y, Amanna, Carlson & Slifka 2007 (10.1056/NEJMoa066092); rest guess |
| ant colony | patch | 20 min–3 h | 15 min–45 min | 100–1000 | 0–0.3 | 0.3–10 | 3–300 | 1–30 | 7.38 | 89.4 | **both** | both 70%, local 16%, shared 13%, none 2% | tau: trail lifetime ~47 min (Lasius niger), Beckers, Deneubourg & Goss 1993 (10.1007/bf01201674); rest guess |
| ant colony | food supply | 6 h–1 wk | 15 min–45 min | 100–1000 | 0.7–1 | 0.03–1 | 0.3–30 | 1–30 | 0.12 | 107 | **shared** | shared 100% | rho: foraging regulated by return rate with no spatial information, Prabhakar, Dektar & Gordon 2012 (10.1371/journal.pcbi.1002670); rest guess |
| small team | tasks | 1 d–5 d | 2 h–12 h | 5–10 | 0.3–0.8 | 1–30 | 1–30 | 0.5–3 | 2.39 | 10.6 | **shared** | shared 56%, both 26%, local 15%, none 2% | guess |
| small team | goals | 1 mo–6 mo | 1 d–1 wk | 5–10 | 0.8–1 | 3–100 | 1–30 | 0.5–3 | 3.4 | 22.1 | **shared** | shared 88%, both 10%, local 2% | guess |
| firm | operations | 1 d–1 wk | 1 wk–1.15 mo | 10–300 | 0.1–0.5 | 1–30 | 30–3e+03 | 3–30 | 131 | 0.00322 | **local** | local 99%, both 1% | guess |
| firm | management | 1 mo–6 mo | 2 wk–1.84 mo | 10–300 | 0.5–0.9 | 1–30 | 3–300 | 3–30 | 13.1 | 50.4 | **both** | both 59%, local 28%, shared 13% | guess |
| firm | strategy | 2 y–10 y | 1 mo–3 mo | 10–300 | 0.7–1 | 1–30 | 1–100 | 3–30 | 4.36 | 40.9 | **shared** | shared 81%, both 16%, none 2%, local 1% | guess |
| city* | services | 6 h–3 d | 3 d–4.29 wk | 10–100 | 0–0.3 | 1–30 | 10–1e+03 | 3–30 | 43.6 | 1.27e-08 | **local** | local 100% | guess |
| city* | budget | 1 y–4 y | 1 mo–6 mo | 10–100 | 0.5–0.9 | 1–30 | 1–100 | 3–30 | 4.36 | 16.3 | **shared** | shared 44%, both 39%, local 10%, none 6% | guess |
| city* | land use | 10 y–50 y | 6 mo–2 y | 10–100 | 0.5–1 | 3–100 | 1–100 | 3–30 | 6.21 | 21.2 | **shared** | shared 47%, both 39%, local 11%, none 2% | guess |
| nation-state* | local | 1 d–4.29 wk | 1 mo–3 mo | 10–100 | 0–0.3 | 1–30 | 10–1e+03 | 3–100 | 43.6 | 1.02e-07 | **local** | local 100% | guess |
| nation-state* | business cycle | 2 y–8 y | 1 mo–3 mo | 10–100 | 0.5–0.9 | 1–30 | 1–300 | 3–100 | 7.55 | 17.7 | **both** | both 48%, shared 38%, local 10%, none 4% | lead: data-release lags, Giannone, Reichlin & Small 2008 (10.1016/j.jmoneco.2008.05.010); rest guess |
| nation-state* | institutions | 20 y–100 y | 3 mo–2 y | 10–100 | 0.7–1 | 3–100 | 1–100 | 3–100 | 6.21 | 14 | **shared** | shared 63%, both 23%, local 11%, none 2% | guess |
| global economy* | markets | 1 h–1 wk | 1 mo–6 mo | 50–200 | 0–0.5 | 1–30 | 10–1e+03 | 10–1e+03 | 43.6 | 3.76e-119 | **local** | local 100% | guess |
| global economy* | world cycle | 3 y–10 y | 1 mo–6 mo | 50–200 | 0.3–0.8 | 1–30 | 1–100 | 10–1e+03 | 4.36 | 4.59 | **both** | local 30%, both 30%, shared 29%, none 10% | guess |
| global economy* | climate | 30 y–300 y | 1 y–5 y | 50–200 | 0.8–1 | 1–100 | 0.3–30 | 10–1e+03 | 1.61 | 2.41 | **shared** | shared 57%, none 24%, local 15%, both 3% | guess |
<!-- /TABLE -->

**Notes on individual placements.**
- **E. coli: measured inputs (PR #110, not yet merged).**
  - The world is one OU signal (τ_v = 1.16 s) read through its integral, McMillan degree 2. It is one component, so it gets 2 stores.
  - X_L is the measured proxy of the fitness benefit of chemotaxis in poor carbon (Ni et al.) divided by the signalling machinery's proteome share:
    - log₁₀ −0.26 to 1.89, centre 0.81;
    - the benefit is the stakes the layers actually win, net of latency and reading, so it is X_L itself.
  - Latency over the fast scale: log₁₀ −0.76 (−1.47 to −0.58). snr: 0.0043–0.103. Both are already inside the measured benefit.
  - In glucose the benefit is about 0 and X_L < 1, and the map gives no layer. The cell does cut motility there (Ni et al.).
  - **Caveat:** PR #110 found that the slow store's memory (9.9 s) is 8.5× the optimum under exogenous noise. The diagnosed cause is the store's own noise. This placement uses only benefit ÷ cost, so it does not test the memory time.
- **Ant colony: not chosen to hit a region.**
  - The inputs were set from the cited biology before the coordinates were computed, and were not tuned afterward. They were not preregistered either.
  - The patch trail time is from *Lasius niger* (Beckers et al. 1993), not from the harvester ants of Prabhakar et al. 2012. Species are mixed.
  - The v2.4 placement into "federation" was circular. There is no federation region now: federation is a local layer in every unit, and it pays for lost pooling through π.
- **Order of dots.**
  - Each chain is one system's own time scales, fast to slow. Systems are not placed by size.
  - The side panel lists systems from small to large only for reading. No order is implied by the map.

## 6. What is proved, what is only numerical, what is guessed

| Item | Status |
|---|---|
| Quadrant edges X_L = 1, X_S = 1; the split rule inside the upper-right quadrant | **Proved** (algebra above), given 0 ≤ κ ≤ 1 and separate read channels |
| κ ≤ 1 (subadditivity) | **Numerically verified only** (3000 + 15 worlds) |
| OU closed forms for G_L, G_S; X_S = ν·π·e^(−2ℓ/τ)·X_L | **Proved** (Kalman–Bucy); numerically confirmed to 10⁻¹³ to 10⁻¹¹ |
| Reading price moves dots, not edges | **Proved** (the same algebra on net worths); 1500 worlds confirm |
| One stream: layer-by-layer marginal reading is exact | **Numerical only** (600/600 two-scale worlds, ≤ 2 stores per location) |
| CT33 on the map (spend never falls as stakes rise, ruin slack) | Follows from CT33; tested on 200 worlds |
| Every dot's inputs | **Guessed**, except E. coli's measured proxy and the cited time scales and delays |

## 7. Referee's list (written by the author; not an independent review)

1. **The dots are guesses.** Stakes ÷ upkeep (R) is unmeasured in every system except E. coli's proxy (GAPS G3). Shared-store upkeep h_c/h_l is a guess everywhere.
2. **κ ≤ 1 is not proved.** A world where G_B > G_L + G_S would let "both" beat "local" in the local quadrant.
3. **The model class is narrow.** Components are linear-Gaussian OU with first-order stores. Real worlds have saturation (E. coli's receptors), heavy tails and non-stationarity.
4. **The one-stream rule is only sampled.** It is verified on two scales and small store counts.
5. **9 of the 20 dots are near an edge** (no design wins ≥ 65% of draws). Their reading can flip within their input ranges.
6. **The ellipses are not posteriors.** They come from independent log-uniform ranges.
7. **Ruin is not drawn.** Systems near their reserve limit may sit off the design shown.
8. **The hierarchy above one shared level is not drawn.**
9. **E. coli's X_L is a proxy.** The fitness benefit was measured in one medium. The memory-time test in PR #110 failed on its setup.
10. **Species are mixed in the ant inputs.** City, nation-state and global economy are marked * because their selection is weak or unknown.
11. **The counting rule is proposed, not yet preregistered per class.** Only E. coli has an observed count.

## 8. History

- **The v2.4 figure** (one made-up 14-scale world, regions from assumed sensing and ruin knobs) was withdrawn in `bc9a1ec` after review 3.
- **Corrections to its notes, for the record:**
  - its federation boundary values 22, 105 and 376 (n = 3, 10, 30 at ℓ = 1) were **optimized-sensing** values; the fixed-sensing closed form gives 28.5, 128 and 414;
  - its word for the sensing spend should have been "sensing cost".
- **v2.5 replaces that figure** with the theorem above. Superseded and removed: `face_model.py`, `face_regions.py`, `face_tables.json`, `face_regions.json`, `tools/test_face_regions.py`.

## 9. Regenerate

```
nice -n 19 python3 figures/face_collapse_v1.py 3000     # about 2 min: random worlds, map vs numerical optimum
nice -n 19 python3 figures/face_collapse_v1b.py 1500    # about 3 min: reading priced
nice -n 19 python3 figures/face_collapse_v23.py         # about 4 min: one read stream
nice -n 19 python3 figures/face_place.py                # about 1 min: placements -> face_dots.json
nice -n 19 python3 figures/face_table.py                # the table above
nice -n 19 python3 figures/face.py                      # face.png (1600x1000), face_square.png (1200x1200), face_all.png
nice -n 19 python3 figures/face_collapse.py             # face_collapse.png
nice -n 19 python3 -m pytest -q tools/test_face_map.py
```
