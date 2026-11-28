# LEDGER: every load-bearing result, placed on the locked claim

> **Repository copy (added 19 Nov 2026 with THEORY v2.1).** A dated working record, copied from the working directory with paths updated: `checks/` now means `theory/layers_checks/` (layer scripts) or `theory/meq_checks/` (master-equation scripts). Not edited otherwise. THEORY v2.1 governs where they disagree; its framing supersedes this file's on novelty (known parts, new claim), applicability (general; the bottleneck is measurement) and responsive worlds (an open theorem, CX2, not a scope limit). Message ids such as t1973u are the author's chat references.


Written 19 Nov 2026, about 10:45 PM ET. Read-only. Repo: a working clone at main `5b65c1e`. Line numbers refer to that commit. New results from this pass are in `PROOF_A.md` (marked NEW, not yet independently reviewed).

## The locked claim (Chad, t1969, wording updated t1971; verbatim)

> "the claim is that one cost under the second law sets how adaptive systems should be built at every scale: layered, with the layers at the world's time scales."

The claim splits into six parts. Every row below names the part it carries.

| Part | Words | What it needs |
|---|---|---|
| **C1** | "one cost" | one total cost of judgment in three additive parts (holding, error or lateness, reads and effort, plus ruin) with every cost booked |
| **C2** | "under the second law" | knowers must pay to stay matched, and acting ahead can pay; physics prices the floors |
| **C3** | "sets how adaptive systems should be built" | design rules derived as optima of the cost (normative: proved in-model). Whether real systems *are* built so is the separate bet |
| **C4** | "at every scale" | the same relations (not constants) at cells, people, firms, cities; scope at the ends |
| **C5** | "layered" | multi-tracker designs beat one flat tracker, and the conditions under which they do |
| **C6** | "with the layers at the world's time scales" | the layers' number, timescales and spacing follow the world's spectrum |

Status words: PROVED (in-model), KNOWN, NUMERICAL, CONJECTURE, OPEN (untested, not refuted), PROXY-FAIL/PASS, SIM-FAIL, WITHDRAWN.

## 1. Second law → knowers must act ahead (C2)

| # | Result | Status | Source | Part | Contribution |
|---|---|---|---|---|---|
| 1.1 | Three ways to last: Keep (frozen), Hold (self-regulating), Know (tracks) | PRIOR ART in substance (Prigogine; Pross) | THEORY.md l.13–23 | C2, C4 | Sets who the claim is about: knowers only |
| 1.2 | E1: with no world-dependent action, Φ = 0 and nothing is held (atoms frozen) | PROVED, partly definitional | THEORY.md l.94; CT5 | C2, C4 | The bottom end: no layers, no model |
| 1.3 | Theorem P (P0–P3): persistence bound D(I_pred); a model is necessary iff blind action is not viable; a horizon; a model only if its first bit pays, with size ∝ log stakes | PROVED, **stationary worlds only** | THEORY.md l.56–64; Appendix B CT1–CT4 l.231–241; `theory/GENERAL_THEOREM.md` §2 | C2 | "Once acting late is costly, it can pay to carry a model": the X-post sentence, proved for W-a |
| 1.4 | CX1: P for drifting worlds | **OPEN** (partial bridge: Nair & Evans 2004) | THEORY.md l.64; CLAIM_MAP CX1 l.451 | C2 | The gap between the P results and every layer result (which use drifting worlds) |
| 1.5 | Physical floors: Landauer; Still et al. 2012; O1 tracking floor kT·σ²/(2D), cheapest total σ√(2kT·w) | KNOWN + PROVED (O1 conditional on known bounds) | THEORY.md l.48–52; `theory/MATH_ATTACK.md` §1.2 | C1, C2 | "Under the second law": the cost has a physical floor at every scale |
| 1.6 | Above the cell the floors are slack; whether the second law does more than set floors is an **open disagreement** | OPEN | THEORY.md l.52 | C2 | The weakest link of "under the second law" above the cell |
| 1.7 | Internal-model results (stochastic IMP bound) | PROVED, self-checked only | `theory/INTERNAL_MODEL.md` §2; THEORY CL10 | C2 | A regulator must model its disturbance; several timescales need models of each (Francis & Wonham, `theory/THEOREMS.md` T8 l.208–210) |

## 2. Judgment has one cost (C1)

| # | Result | Status | Source | Part | Contribution |
|---|---|---|---|---|---|
| 2.1 | The cost: holding (κ, h), error and lateness (w·ℓ), reads and effort (c, d, κ_b, u, g); ruin Λ as the constraint; drift reduction books in part 3 | Model definition; the cross-scale sufficiency claim J16 is **OPEN** | THEORY.md l.38–46; CLAIM_MAP J16 l.317 | C1 | The "one cost". Kill rule: a level needs a cost that cannot be booked |
| 2.2 | Result 3 read-rate rule: rate ∝ (wq/c)^{1/α} | PROVED (hold-last-value; any rescaling-closed predictor) | THEORY.md l.98–104; CT12 | C1, C6 | Couples effort to the world's spectral slope α |
| 2.3 | T1c robustness: 2× misjudgment costs 6%, 10× costs 74% | PROVED | THEORY.md l.106; CT13 l.312–314 | C3 | Why near-optimal designs are easy to find and hard to distinguish |
| 2.4 | Lemma B2 spectrum map: noisy-sensing error, memory time ∝ (N/q)^{1/α}, forgetting kernel ∝ τ^{−(1+α/2)} (exponential only at α = 2) | KNOWN, assembled | THEORY.md l.316; v1.4.29 l.120–127 | C6 | **The bridge from the world's time scales to memory design** |
| 2.5 | Result 2 (Theorem G): check vs fade iff λc < Φ; G1 copies decay; G3 cliff; T8 freeze/hold/lookup band, N² widening | PROVED | THEORY.md l.88–94; formal Thm 8 l.285–308 | C3 | Per-fact rules. The cliff and lookup edge also **dissolve layers** (2.10) |
| 2.6 | Result R temperature z = B/(σ√τ); Theorem L | PROVED; the lead X-post prediction (K4) PROXY-FAIL | THEORY.md l.140–142; CLAIM_MAP K4 l.327 | C1 (ruin) | Ruin channel. Not on the layer spine; kept as the ruin term |

## 3. In a multi-timescale world, the cost is paid most cheaply by layers (C5)

| # | Result | Status | Source | Part | Contribution |
|---|---|---|---|---|---|
| 3.1 | "Nested beats flat is not one theorem"; no general theorem | Repo's own statement | `theory/THEOREMS.md` l.60–62, l.111 | C5 | The gap that PROOF_A fills on the time axis |
| 3.2 | **NEW L1:** one timescale (one OU mode or a random walk) ⇒ one layer is exact at every stake. **The scale-free random walk needs one layer** | PROVED (in-model; KNOWN content) | `PROOF_A.md` §2 | C5, C6 | Boundary: layering is about *how many* timescales, not "fractal" per se |
| 3.3 | **NEW L2:** J modes ⇒ at most J layers, exactly J at high R; layers pay iff R > R\* = min_K (K−1)/(ε_1 − ε_K) | PROVED (in-model) at lead 0; ≤ J at all leads | `PROOF_A.md` §2 | C5, C6 | **The iff for "layered"** on the time axis |
| 3.4 | **NEW L3:** a non-rational spectrum (continuum of timescales, fBm H ≠ ½) ⇒ no finite K is exact; K\* → ∞ as R → ∞ (the limit is conditional) | PROVED (strictness) | `PROOF_A.md` §2 | C5 | In a scale-free world, layers keep paying as stakes rise |
| 3.5 | Store count K\* ≈ (ln 8R/2π²)·ln(stakes/upkeep); one store iff ψ·c(α−2)² ≲ 1 | Exactness iff rational KNOWN; **rate CONJECTURE** | v1.4.29 l.85, l.127; CLAIM_MAP K12 l.335 | C5, C6 | How many layers. **In v2.0 only as one clause** (THEORY.md l.316) |
| 3.6 | Numerics: flat penalty 0.2–5% in scale-free bands, ≤ about 20% max found; R\* ≈ 17–10⁴ (two modes), 22–58 (α = 1, spans 10²–10⁵); K\* rises with span and R | NUMERICAL | `checks/experiments.out`, `lead.out`, `maxgain.out` | C5 | Size of the time-axis gain: real but modest |
| 3.7 | T3b / Prop 9: separate clocks save ≤ 1 − K^{−(1−γ)} (29% for two); **zero with indivisible reads** | KNOWN | `theory/THEOREMS.md` l.82–86; formal l.312–314 | C5 | "Layered" needs separately readable parts |
| 3.8 | T3c: decoupled nesting is near optimal when scales separate; it loses when they collapse | NUMERICAL; principle KNOWN (Simon–Ando, Tikhonov, Borkar) | `theory/THEOREMS.md` l.88–109 | C5, C6 | Layers must sit at *separated* scales |
| 3.9 | Result 4 / formal Thm 1: a shared level pays iff N > N\*(ρ) = [ρ^b/((1+ρ)^b−1)]^{1/(1−a)} (≈ 4/ρ); telling-price rule; exponent set by the level's technology | PROVED | THEORY.md l.108–117; formal l.56–90 | C5 (member axis) | Layers **across members**: when a shared layer forms |
| 3.10 | Formal Thm 6: levels are complements (submodular), inclusion, lattice, accretion as upkeep falls; **cheaper lookup can dissolve levels** | PROVED | formal l.223–252 | C5 | Layers accrete together; lookup removes them. **Dropped from v2.0** |
| 3.11 | Formal Thm 2: broadcast break, onset a threshold in ρ | PROVED | formal l.94–108 | C5 | Communication cost limits layering (Garicano). v2.0 keeps only the booking |
| 3.12 | Formal Thm 5: vigilance at birth ≥ 1 + (1+ρ)^{−1/2} (errata) | PROVED | formal l.188–219; THEORY CL5 | C5 | A new layer starts more watchful |
| 3.13 | Rule 6 mechanism (use strengthens, disuse fades; "no one in charge") | Does NOT follow from the cost | THEORY.md l.84, l.125 | — | **Off-spine.** Keep as a hypothesis |

## 4. Which layers, at what timescales, how many, who is in charge, how far each reaches, when to federate (C5, C6)

| # | Result | Status | Source | Part | Contribution |
|---|---|---|---|---|---|
| 4.1 | T7: architecture is self-similar if drift is scale-free, costs are power laws and the loss is the same at every level (sufficient; necessity not proved); "the optimal architecture inherits whatever scale structure the world has" | PROVED (conditional); unconditional FAILS | `theory/THEOREMS.md` l.175–204 | **C6** | The repo's own form of "layers at the world's time scales". **Dropped from v2.0** (only a withdrawn "time is fractal" line, l.184) |
| 4.2 | T7b: log-uniform items + shared clocks ⇒ equal log-widths, geometric levels (α = 2) | PROVED; Roundy-type, KNOWN in substance | l.181–185 | C6 | Spacing in scale-free worlds |
| 4.3 | **NEW L4:** T7b's geometric optimum holds at every α in (1, 3) | PROVED (in-model) + numeric | `PROOF_A.md` §2; `checks/t7b_alpha.out` | C6 | Removes T7b's unstated α = 2 premise |
| 4.4 | Store model: optimal layers are roughly log-spaced (3–20× apart), widening toward the slow end, not span-invariant; LAYERS1 P2 | NUMERICAL; LAYERS1 P2 **SIM-FAIL** | `checks/experiments.out` Exp3; CLAIM_MAP G20 l.239 | C6 | "Geometric" is approximate in memory stores |
| 4.5 | Cadence world: one layer per cadence, each **faster** than its mode (spectral-factor roots b_j, shifted by sensing noise) | PROVED (L2) + numeric | `PROOF_A.md` §3 | C6 | "At the world's time scales" holds as "one per scale", not "at exactly the same period" |
| 4.6 | T7c closure and scaling law T\*(n) ∝ n^{(γ−δ)/2 − H} | PROVED (elementary) | `theory/THEOREMS.md` l.188–192 | C4, C6 | The same rule at the next level up |
| 4.7 | Formal Thm 7: which scales of a nested tree carry a level; top-down iff κ < κ\* = (1−a)/(1−b) (κ here is a drift-sharing exponent, **not** THEORY's κ) | PROVED; depth avalanches NUMERICAL (F6 OPEN) | formal l.256–281; CLAIM_MAP F6–F11 | C5, C6 | Which levels, filled from which end. **Dropped from v2.0** |
| 4.8 | "Two axes, one rule": levels across members, stores across timescales, the same cost comparison; "the only sense in which GTAO is fractal" | Framing, correct | v1.4.29 l.182 | C5, C6 | The unifying sentence for layers. **Dropped from v2.0** |
| 4.9 | Result 5: one clock costs ≥ separate clocks (equal iff Gorman-type condition); a part that bears Λ_i/Λ_whole watches at (Λ_i/Λ)^{1/α} | PROVED | THEORY.md l.119–125; CT17 | C5 | Who must be in charge: shared fate or enforcement, unless upkeep is privately rewarded (J9 OPEN) |
| 4.10 | Result 6 LAT-1: L_max = v(D\*/q)^{1/(α−1)}; federate beyond it (three shortcut cases) | PROVED (elementary); real-system form N27 OPEN | THEORY.md l.127–138; `theory/SCALE_ENDS.md` §5 | C5, C4 | How far one layer reaches; when to federate |
| 4.11 | ARCH_EQUATION: levels = cost-thresholded copy of the shared-drift covariance; eigenvalue rule for disjoint scopes | PROVED in class R; framing "partly new" | `reviews/night1/ARCH_EQUATION.md` l.11–36, l.147–176, l.349–361 | C5, C6 | "An organization's levels are a cost-thresholded copy of its environment's shared-drift structure" |

## 5. Predictions and how it dies (all parts)

| # | Item | Status | Source | Part |
|---|---|---|---|---|
| 5.1 | The bet: strongly selected designs sit near the measured-input optimum, with the same relations across scales (N13, J6) | **OPEN** | THEORY.md l.66–70; CLAIM_MAP N13 l.373, J6 l.306 | C3, C4 |
| 5.2 | Store count tracks measured span and stakes/upkeep where α ≠ 2 (the N4 kill) | OPEN | v1.4.29 l.85 | C5, C6 |
| 5.3 | Shared layer appears at N\*(ρ); onset exponent set by technology, not α | PROVED in-model; untested in the field | THEORY.md l.154–155 | C5 |
| 5.4 | Cheap lookup removes holding layers, not enforcement layers (N52) | OPEN | THEORY.md l.157 | C5 |
| 5.5 | Attention exponent 1/α (N51) | OPEN; lab test specified | THEORY.md l.152 | C6 |
| 5.6 | Field record: 15 proxy-fails, 7 proxy-passes; in-model locked sims 6 fail, 3 pass, 3 inconclusive | as stated | THEORY.md l.163–165 | all |
| 5.7 | DRIFT1: 311 scale-free **across categories** (post hoc dequantized), hourly series broken near 22 h; Wikipedia items have a characteristic rate, aggregate 1/f^0.34; SEC bunched at cadences | OPEN (fails MV2: event rates, not drift q) | `tests/DRIFT1/RESULTS.md` l.9–37; CLAIM_MAP H20 l.273 | C6 (premise) |
| 5.8 | DGS10 α̂ = 2.00 ± 0.03 (random walk, one layer by L1); log VIX corner about 3 years, no single slope | on proxy | `measurement/estimators/RESULTS.md` l.12, l.78–79 | C6 (premise) |

## 6. Off the spine (flagged)

- **Temperature and buffers (Result R, K4):** they belong to the ruin term of C1, not to layering. Keep them short.
- **REACH material** (torus T9, cosmic web, wormholes, dark sector) and black holes as maximal frozen memory: scope notes for C4's ends, not load-bearing. N46 withdraws "time is fractal" as framing. The *conditional* statement about the tracked world's spectrum stands (CLAIM_MAP l.406).
- **Rule 6 mechanism** (Hebbian use and fade): not derived from the cost.
- **Kussell & Leibler bet-hedging:** a counterexample that limits C2 ("a model always pays") and does not hurt C5.
- **The physics above the cell (1.6):** the claim's "under the second law" is literal only as floors there.

## 7. Load-bearing items that v2.0 dropped or shrank

1. **T7, conditional self-similarity, "the architecture inherits the world's scale structure"** (`theory/THEOREMS.md` l.175–204). This is C6 itself. v2.0 has only "time is fractal (withdrawn)".
2. **"Two axes, one rule"** (v1.4.29 l.182): the one sentence that unifies the layers.
3. **The store count** and the one-store knife edge (v1.4.29 l.85, l.110–114, l.127): v2.0 has one clause, "rate conjectural" (l.316).
4. **Formal Theorem 7** (which scales carry a level; top-down iff κ < κ\*).
5. **Formal Theorem 6** (complements, accretion, lookup dissolves levels).
6. **Formal Theorem 2** (broadcast threshold): only its cost booking survived.
7. **T3c / time-scale separation** and **T3b**: the clock cap is in v2.0 only as "separate clocks save at most 29%" (l.117).
8. **The ARCH_EQUATION framing** ("levels are a cost-thresholded copy of the environment's shared-drift structure, with exponents fixed by how members sense").
9. **Simon 1962 and Kiebel et al. 2008**, which the X post itself used under "How it scales": v2.0 credits Simon only in a list (l.171).
