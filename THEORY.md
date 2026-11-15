# A Theory of Adaptive Organization — v1.2 draft

**Author:** Chad Mitchell. **Draft dates:** v1.0 Saturday 14 November 2026; v1.2 Sunday 15 November 2026 (America/New_York). Changelog: §13.
**Status:** private working draft. **Not peer reviewed. Not independently reviewed as a whole.** Locked prediction files in `tests/` and `reviews/` are untouched; this document only interprets them.

**This file is the one canonical statement of the theory.** Every other theory file in this repository (`theory/`, `reviews/night1/formal/`, claim maps, write-ups) and in Ace's working folders is either a derivation this file cites by path and section, or frozen history. If another file disagrees with this one, this one governs until it is changed here. Current status, commits and the work queue: `STATUS.md` and `QUEUE.md`.

**What kind of claim this is.** GTAO is a **falsifiable causal theory**. It is not a law, and nothing here should be read as one. A law could emerge only if one relation held, in the same form, in at least two very different substrates whose sensing classes were measured independently. That has not happened.

**Title (decided, Chad, t1908):** the title stays. It collides with Dessein & Santos 2006, "Adaptive Organizations", *JPE* 114(5):956–985, which is cited prominently (§10).

### Status at a glance (15 November 2026, 09:02 AM ET)
- **Measurement first (Chad, t1908).** No field test so far measured GTAO's quantities validly, so no field result is a kill or a confirmation of the theory. Field results are reported as "passed / failed on proxy X" (`measurement/FRAMEWORK.md`, `measurement/CLAIM_MAP_v2.md`). Proof-level corrections and simulation failures stand as they are.
- **On real data, specific to GTAO: nothing confirmed, nothing validly refuted.** Proxy fails include the item-level news-recall slope (P1: 0.32, CI 0.29–0.35, vs a predicted 0.5–1.2; the need proxy is not drift) and rank vs external mail in Enron. The one proxy pass of night 1 (PIAAC supervisors' external reading) is Mintzberg's prior art. Night-2 nomination-network results (VIGIL_ONA) were downgraded by a blind referee; vigilance is **OPEN**.
- **Proved inside the model** (`reviews/night1/formal/`): onset exponent set by the level's sensing class; opposite effects of shared and private drift; loss-shape irrelevance under bundled decisions; an exact vigilance formula with price invariance (at zero upkeep the onset value is 1 + (1+ρ)^{−1/2}, between 1 and 2; the earlier "≥ 2" is wrong as stated); an ordering threshold; a freeze/hold/lookup band. Mostly built on published foundations (Marschak & Radner 1972; Veldkamp & Wolfers 2007; Van Zandt & Radner 2001; EOQ and inventory pooling; Topkis). How these relate to the drift-spectrum core: §2.5.
- **Simulations:** passes so far are circular; four locked in-model predictions failed (SENSING2's risky world; three in ANTS1).
- **The headline hypothesis (§2) is the least developed part.** The map from a measured spectrum to the predicted design exponents has not been derived beyond the single-tracker case (§2.5). That is now the first theory item in `QUEUE.md`.

**Labels used throughout**
- **KNOWN**: already in the literature (credited in §10).
- **PROOF**: derived in `theory/`, with a code check, under stated assumptions. Self-checked unless marked otherwise.
- **HYPOTHESIS**: a claim with predictions that has not yet passed a locked test.
- **POST HOC**: suggested by data already seen. It does not count as evidence until it is locked and tested on new data.
- **Novelty "not found"** means not found in a literature sweep of about 22 fields (`litmap/`). It does not mean proven new.

---

## 0. The claim in one paragraph

An adaptive organization (a cell, an immune system, an ant colony, a person, a firm, a city) stays alive by holding information about a world that keeps changing, while paying for that information and for every delay in acting on it. The theory says that one budget governs this at every scale. The budget covers upkeep, error, lateness and the risk of ruin. Only the currency changes: heat in a cell, attention in a person, money in a firm. The central new bet in this draft is that **the shape of the world's change sets the exponents of the organization's design.** That shape is the *drift spectrum*: how much change happens at each timescale, i.e. how "red" the world is. A world with one characteristic pace calls for a square-root law and one memory timescale. A world that drifts at every pace calls for log-spaced layers of memory, which from outside look like power-law forgetting. A world whose variation spreads across many modes sets how fast an organization's model should grow with its size. This is a **hypothesis with sharp predictions**, not a result. Some pieces are proved under assumptions, some are already published by others, and some have already failed tests. All three are listed below.

It is **not** a theory of everything. It says nothing about what an organization wants, only about what it must pay to keep tracking a world while it pursues it.

### What changed from earlier drafts
1. **Prior art is credited up front.** The square-root memory law is Lee, Flack & Krakauer's (2024). The failure "temperature" is the inverse of the textbook safety-stock factor. Its first-passage form is Black & Cox's (1976), not Merton's.
2. **The core is reorganized around the drift spectrum** (§2), which ties the ½ law, the nested layers, power-law forgetting and model-size scaling into one family of predictions.
3. **A missing lever is added:** organizations can *reduce* the world's drift, not just track it (§5).
4. **"No one in charge" is narrowed** to cases where shared memory is privately rewarded. Otherwise the theory expects enforcement (§6).
5. **Where optimality should hold is stated** (§7): strong selection only.
6. **Test results are reported as they came out** (§8), including the failed exact-exponent claims.

---

## 1. What looks new: each tied to an exponent, a sign or a threshold, with a kill condition

These are the parts that, after the sweep, do not appear in the prior art found. Each could still exist somewhere obscure, and each needs a targeted search before any public novelty claim. **None has yet passed a locked, independently reviewed test.** Night-1 results and the full current map are in §8b and `reviews/night1/CLAIM_MAP_FINAL.md`.

| # | Claim | The number | How it dies | Status |
|---|---|---|---|---|
| N1 | **√N fade of shared memory, with a sign flip.** When N independent contributors pool readings of a *drifting* target into one shared trace (a trail, a wiki line, a word), the optimal fade rate rises as √N. When the target is *stable*, more use makes a trace last longer (Lieberman et al. 2007: irregular-verb half-life ∝ √frequency). Same averaging law, opposite sign, set by drift. | K\*_shared ≈ √N · K\*_private (small-gain regime, Nq/r ≪ 1; `theory/THEOREMS.md` T4) | (a) Across Austronesian languages, log(word-gain rate) vs log(speaker population) has a CI excluding 0.5 and including 0 (neutral substitution) or 1 (per-capita innovation). (b) Frequency effects on replacement do *not* differ in sign between drifting and stable referents. | PROOF of the math (Kalman averaging, KNOWN); application HYPOTHESIS, **untested** in the field (LANG1 on languages failed on proxy "word-gain rate vs speaker population" (PROXY-FAIL): 0.13 vs 0.5). ANTS1 (simulation) finished on 15 Nov. The fade exponent passes, but by construction (a linear trail readout is a Kalman/EWMA filter). With an ant-like nonlinear readout, error pooling **failed** (slopes −0.26 to −0.40 vs −0.5), and 2 other locked predictions failed. The fade rate alone does not diagnose pooling (`reviews/night1/ANTS1_WRITEUP.md`). |
| N2 | **Threshold for a new shared level (T3a).** Modeling a shared driver is guaranteed to pay once group size exceeds a threshold set by the ratio ρ of shared to private drift. | N > N\* = (√(1+ρ)+1)²/ρ (≈ 4/ρ for small ρ). A *sufficient* condition, not a cutoff. | Across groups (repos sharing an upstream dependency; ant species by food patchiness), the size at which a shared layer appears does not move with ρ. | PROOF, now an exact iff within the one-source model and generalized to N\* = [ρ^b/((1+ρ)^b−1)]^{1/(1−a)}, with exponent −(1−b)/(1−a) set by the level's sensing class (night 1). The −1 case is **prior art** in substance (Veldkamp & Wolfers 2007; Van Zandt & Radner 2001). The simulations (POOLSIM) are **circular**. Beekman et al. 2001 show *a* trail threshold exists, not this one. **Untested in the field**, and a simulation shows the small-ρ onset is invisible under ≥ 1% decision noise. |
| N3 | **The fixed-spread sign.** Critical-slowing-down work says slower recovery means danger, because at fixed shock size the spread widens. At a *fixed observed spread*, the theory says slower correctors cross a boundary *less* often, because they make fewer excursions. | ε_τ = −1 at fixed spread (`theory/MATH_ATTACK.md` §2) | Fixed-spread slope ≥ 0, or closer to 0 than to −1, at two or more scales. | **Sign held; size failed; the literal joint kill fired** (§8). Glucose −0.46 (fires on the full sample); populations −0.21 (fires on any reading). The independent review confirms that the sign itself follows from dimensional analysis and standard first-passage results, so it is not theory-specific. The −1 exponent, the collapse, and the z-interaction all failed. |
| N4 | **Geometric layers if and only if drift is scale-free (T7b),** with a level count. | Equal log-spacing of levels; K\* ≈ (C·L²/(12h))^{1/3}, i.e. levels ∝ (log-span)^{2/3} | Geometric layering where the world has a characteristic time (breaks "only if"), or a layer count that stays flat as the span grows in scale-free curves. | PROOF of the "if" direction (Roundy-type math, known in substance; Shankar & Howard 2013 hold the closest single-agent result). Locked layer-count test (MATCH1 C1): **inconclusive**. Only a post-hoc fit supports it. LAYERS1 (model-internal, night 1): linear-in-span fits as well as or better than (log-span)^{2/3}, span invariance of spacing **failed** (6/12), and the rest is "approximation theory plus a price". |
| N5 | **Watching effort rises, then collapses.** With any bounded fallback (re-read the source, rewrite, fade), refresh effort grows with drift up to a point and then drops to zero: a cliff, not a plateau. | f\* > 0 iff λ < μW/c; under quadratic loss the cliff is at σ_c = μu/√(2cw) (T5, T5b) | In a domain with a bounded fallback (e.g. Cochrane reviews vs topic RCT rate), update effort keeps rising through the top drift decile. | PROOF; core case KNOWN for web crawlers (Cho & Garcia-Molina 2003). The cross-domain claim is **untested**. |
| N6 | **Spectrum → exponent relation** (the core hypothesis of §2). | ½ for single-timescale worlds; slope 1 and power-law forgetting for scale-free worlds; model size ∝ Q^{1/β} (stationary) or Q^{min(½, 1/β)} (drifting), with β measured from the environment | The design exponent does not move when the environment's measured spectrum moves (e.g. a constant ≈ 1 regardless of β, which favours a fixed-budget-share null). | HYPOTHESIS, **leaning against**. The pieces are PROOF or KNOWN; the assembly was not found. Every exact exponent tested has missed or been inconclusive (§2.4). The item-level news test P1 **failed on proxy "headline-word recurrence as need"** (PROXY-FAIL) on 15 Nov (a_c = 0.31 locked; independent re-fit 0.321, CI 0.289–0.352, against a predicted 0.5–1.2; the named rival's 0.24 is also excluded). |
| N7 | **A quantitative internal-model bound.** An agent that stays solvent on a strictly proper score must carry a near-copy of the world's causal-state machine, and its update rule must nearly mirror the world's. | P(model ≠ causal state) ≤ √(2δ)/γ_L with δ ≤ (margin − bit cost)/stakes (I3, `theory/INTERNAL_MODEL.md`) | A counterexample to the proof, or a prior statement of the same bound. | PROOF (Pinsker plus a triangle inequality; self-checked, not independently reviewed). **Novelty unconfirmed and probably folklore.** At zero miss it reduces to Shalizi & Crutchfield 2001. The bound is loose by about 10× in numerics. |

Also probably this project's own: the temperature *identity* ε_τ = ε_σ/2 − 1 and the universality classes set by how fixing works (§4); the cost condition for acting ahead (pay for a model only if lateness loss exceeds its upkeep); and a cross-scale, preregistered falsification program.

---

## 2. The core: the world's drift spectrum sets the exponents (HYPOTHESIS)

### 2.1 Setting

A system holds a state M about a world X. Keeping M accurate costs upkeep. Being wrong costs a loss, at stakes w. Being late costs extra, because a prediction that arrives after the moment to act buys nothing. Running out of buffer B ends the system. The draft objective is

  **J = upkeep(information held and refreshed) + w · E[error loss] + lateness cost + Λ · (failure hazard) + cost of reducing drift (§5),**

minimized subject to staying solvent (`theory/GENERAL_THEOREM.md`, Theorem P: solvency needs at least R(y − c̄) bits).

What matters about the world is not one drift rate but its **spectrum**: how much variance arrives at each timescale. The spectrum can be summarized by one exponent where it is a power law: S(f) ∝ f^(−α) in time, or, across many modes, mode variances λ_i ∝ i^(−β).

### 2.2 Three regimes, three exponent predictions

**Regime A — one characteristic pace (single timescale).**
- Example worlds: a random walk with white increments; a process that mean-reverts at one rate; switching at one rate.
- Prediction: the optimal check interval and memory length scale as the **square root** of the environment's persistence, T\* = √(2c/(wσ²)), memory ∝ τ_E^{1/2}, and forgetting is exponential at one rate.
- **This is KNOWN**: EOQ (Harris 1913), Kalman/Muth 1960, inattention (Reis 2006; Alvarez, Lippi & Paciello 2011) and, for adaptive memory with an energy cost, **Lee, Flack & Krakauer 2024**, who derive τ_m\* ∼ τ_E^{1/2} as a universal law. This theory *agrees with* that result and does not claim it.

**Regime B — no characteristic pace (scale-free drift).**
- Example worlds: power-law (1/f-type) change spread over many decades.
- Prediction: the optimal architecture is a ladder of exponential stores with **geometrically (log-) spaced** timescales (T7b). The number of rungs grows as (log-span)^{2/3}. Summed, the ladder forgets as a **power law**. Adaptation time scales **linearly** with the environment's switching time (slope 1), because the system has no internal scale of its own. Where the world does have a characteristic time, the power law should bend into an exponential near it.
- The ingredients are KNOWN in separate places. Anderson & Schooler 1991 show human memory mirrors power-law need. Fusi, Drew & Abbott 2005 and Benna & Fusi 2016 show log-spaced cascades give power-law forgetting. Shankar & Howard 2013 show log-spaced memory is optimal for power-law-correlated signals. Brand (1994; 2018) and Holling (1973; 2001) describe pace layers and panarchy qualitatively. What this theory adds is the cost condition (the "only if" and the level count), joined to a measurable condition on the world.

**Regime C — variation spread across many modes (model size).**
- Setting: the world varies along many modes with variance λ_i ∝ i^(−β); stakes scale with throughput Q (an assumption); bits have a fixed price.
- Prediction (PROOF given those assumptions, `theory/INTERNAL_MODEL.md` §4–5):
  - mean-reverting world: optimal model size ∝ **Q^{1/β}** (reverse water-filling, a KNOWN tool);
  - drifting (random-walk) world: information rate ∝ **Q^{min(½, 1/β)}**, so the square-root law returns for β ≤ 2;
  - the share of throughput spent on the model has an interior minimum **iff β < 1**;
  - unstable modes impose a stakes-independent "survival tax" F = Σ log₂|a_i| (the data-rate floor of Nair & Evans 2004 and Tatikonda & Mitter 2004), and so a **minimum viable size** Q_min = κF/μ;
  - an infinite random-walk world with β ≤ 2 and unbounded loss per ignored mode is not viable at any finite rate. A survivor there needs a bounded fallback.
- β can be read from the environment itself: a 1/f^α field in d dimensions gives β = α/d. Natural images (α ≈ 1.81, d = 2; Ruderman & Bialek 1994) give β ≈ 0.905 and a predicted exponent of about 1.10.

**The unifying statement.** The ½ law, the log-spaced layers, power-law forgetting and model-size scaling are not separate rules. They are one rule, "track what the world's spectrum makes worth tracking at the price you pay", evaluated in worlds of different redness. The ½ law is the special case of a world with one pace.

### 2.3 Where the physics is literal and where it is not

- **Literal:** floors. The minimum heat cost of tracking a random walk to error D is kT·σ²/(2D). Adding quadratic loss gives σ√(2kT·w), the EOQ form with c = kT per nat (`theory/MATH_ATTACK.md` O1). Holding I bits against a drifting world needs an inflow of at least (1 − η)·I bits per step, met with equality by the Kalman filter, consistent with Mitter & Newton 2005 and Horowitz & Sandberg 2014 (KNOWN).
- **Not literal above the cell.** kT ln 2 per bit does not bind for neurons, people or firms; synapses pay roughly 10⁵ times that (Laughlin et al. 1998). Above the cell the exponents come from information theory plus network transport costs, not from the second law. This draft says so plainly. The objection "decision theory in a lab coat" mostly survives above the cell.
- **What is the same at every scale** is one known inequality: growth ≤ disequilibrium + information − house take. It covers Szilard engines, Kelly bettors and selection (KNOWN; `theory/INTERNAL_MODEL.md` §8). In markets no-arbitrage plays the role of the second law: in an efficient environment blind persistence is impossible, so persistence requires information (PROOF, assembly; novelty unconfirmed). The constraint there is competition, not heat.
- **Night-1 physics review (15 Nov):** in the formal layer, the energy / second-law framing is **decorative**. No conserved quantity, entropy production or Landauer-type bound enters any proof, and "one currency" is only an exchange rate inside one organization. The one place physics could earn its keep is cells, where assigning entropy-priced sensing as "the thermodynamic floor" decides the predicted exponent (−1 vs −2) and is asserted, not derived. Either derive one bound in physical units for one sensing system, or keep this language out of public claims.
- **Open disagreement, stated (Chad, t1908):** the physics is not decorative. The same three costs (holding a memory, predicting, upkeep) apply at every level from atoms to cities; the thermodynamic floor binds tightly at the cell and constrains less at firm scale; variational free energy equals thermodynamic free energy only in a special case. The night-1 referee's point stands for the *proofs* (no physical quantity enters them). What would settle it: one system where the thermodynamic binding ratio is measured and the predicted sensing class is the one the floor selects (`measurement/FRAMEWORK.md` §3.11; QUEUE SENSE-CELL).
- **Scale invariance holds only if one currency dominates** (`theory/GENERAL_THEOREM.md`, Theorem S).

### 2.4 Evidence so far on the spectrum hypothesis (honest)

| Evidence | What it shows | Bearing |
|---|---|---|
| Fly motion neuron (Fairhall et al. 2001), read in BIO1 and MATCH1 | Adaptation time scales linearly with the switching period (4–40 s); phase lag is a fixed fraction of the period | **Supports Regime B** (slope 1, not ½). Reported in the source, not a new test |
| Retina (Wark et al. 2009), as read off figures | Luminance 0.53 (whole cell), 0.76 (on cell); contrast 1.87 | **Mixed**: between ½ and 1, one outlier |
| Need exponents across environments (COLLAPSE1, MATCH1) | Anderson & Schooler need-odds decay as a power law with exponent 0.6–0.8 in news headlines (0.71–0.78), code (21 of 23 out-of-sample repos in band, median 0.62) and Wikipedia (0.66) | The world side of Regime B looks scale-free in human information environments. Code recurrence as a power law is partly prior art (Challet & Lombardoni 2008; Wu 2006); the cross-environment band was not found stated |
| Same-system match (MATCH1 A1, news) | Memory of news decays with exponent 0.24 vs need 0.71: ratio 0.34, outside the locked [0.5, 2] band (borderline kill; full-corpus ratio 0.31 would be a kill) | **The strong form fails**: memory's exponent does not equal need's. The weak form (power law follows power law) survives and is Anderson 1990's model, recall odds ∝ (need odds)^d with d ≈ ⅓ here |
| Layer count vs span (MATCH1 C1) | Inconclusive at the locked 2% tolerance (weekly and yearly cycles set a noise floor). Post hoc at 3%: layers rise from 2 to 4 over 1–3 decades in code, news and Wikipedia | Consistent with T7b and against a fixed two-store model, but **post hoc only** |
| Redness vs need exponent across repos (MATCH1 D3, exploratory) | Spearman +0.57: redder edit series go with *steeper* need decay. The prediction was negative | **Opposite sign** against the locked prediction. **Referee (v1.3.1, 15 Nov 09:40 ET; `reviews/night2/SPECTRUM_MAP_REFEREE.md` §6) corrects the explanation below:** the locked negative sign was mis-derived (it used the event autocorrelation; MATCH1's a is a re-occurrence hazard), and a pure Cox world also gives a strongly positive sign (+0.975) and passes D3S (Δβ ≈ 0.045 at β ≈ 0.2), so D3S is a non-discriminating PROXY-PASS and does not show a renewal world. *Superseded v1.3 text:* **Explained (v1.3, pending referee):** in event data the need exponent and the band slope are both read off one gap distribution, so burstier gaps raise both (positive sign); a pooled-hazard renewal simulation reproduces each repo's β (POST HOC), and a LOCKED gap-shuffle test passed (median Δβ = 0.024, band [−0.03, 0.05]; `reviews/night2/SPECTRUM_MAP/` §2 Prop. 6). The locked sign assumed a modulated-rate world. Event worlds need two exponents |
| Which worlds are scale-free (DRIFT1) | NYC 311 request rates spread log-uniformly over 2.5–4 decades; Wikipedia articles and SEC filings have characteristic cadences | Supports T7 as a *conditional* claim, and cuts against "fractal at every scale" |
| τ weight in firm and glucose tests (F1, DECISIVE) | F1 likelihood prefers a τ weight near 1 over ½, but the independent review notes that this rests on 3 grid points with a log-likelihood gap of 2.9, and that F1's "τ" mostly measures fixed-cost share, not correction speed. Glucose's effect depends on the 1/e autocorrelation time; the AR(1) τ is null, so glucose is not single-timescale | Suggestive of the ½-vs-1 split only; noisy measures, and F1 does not test the construct |
| Model size vs throughput (published data, `theory/INTERNAL_MODEL.md` §6) | Brains (1.0–1.16) and city administration (≈ 1.0) are near the β ≈ 1 prediction | **Does not discriminate**: a "fixed share of the budget" null also predicts 1. β has not been measured for any organization |

**Net:** the direction (redder worlds call for longer, layered, power-law memory) has some support; every exact exponent tested so far has missed or been inconclusive; one exploratory sign went the wrong way. The hypothesis stands as the organizing bet, not as a finding.

**POST HOC, untested:** memory outlasting need (MATCH1's ratio below 1) may follow from the theory's own keep rule. Keep an item while need × miss cost exceeds upkeep. When the miss cost is high relative to upkeep, the hold horizon stretches far past where need has fallen, so memory's exponent should be *smaller* than need's, with the gap growing with miss cost ÷ upkeep. This was proposed after seeing MATCH1 and **must be locked and tested on new data before it counts.**

### 2.5 How the formal layer sits inside the spectrum core, and the rule "regime first" (added v1.2)

- **The bridge already proved.** In the formal layer (`reviews/night1/formal/THEOREMS.md`, Lemma 1(i)), a tracker that reads and then holds the last value, in a world with fractional drift of Hurst exponent H, has stakes and drift elasticities a = b = **1/(1+2H)**. The √ (½) is the H = ½ (Brownian, single-pace) case. Every formal theorem is stated in (a, b), so the onset exponent −(1−b)/(1−a), the vigilance criterion and the ordering threshold all move with the world's spectrum through (a, b). The constants quoted for "class R" (a = b = ½; the vigilance floor 1 + (1+ρ)^{−1/2}) are H = ½ instances (`reviews/night1/ARCH_EQUATION.md` §0.2: the constants are functions of H, not universal numbers).
- **Two axes, one rule.** The formal layer is the *across-members* axis (who shares a model of which driver: levels). §2.2 is the *across-timescales* axis (how many memory stores at which speeds: layers). Both are "track what the spectrum makes worth tracking at the price paid", applied to the cross-member covariance and to the temporal spectrum respectively. This is what "fractal" means here: the same cost comparison deciding levels across members and layers across time.
- **What is missing.** Axiom 6(iv) allows separately timed clocks inside a tracker, but the formal theorems do not derive the joint map from a measured spectrum to the number, spacing and forgetting exponent of those clocks; R1's hold-last-value estimator remains a restriction for H ≠ ½. The joint map from a measured spectrum to read rate, number and spacing of stores, and forgetting exponent is **not derived** (§2.4; `measurement/FRAMEWORK.md` §6.10). Night-1 found that the layering part, as far as it was derived, adds only "approximation theory plus a price" (`reviews/night1/ARCH_EQUATION.md` §0.5). Deriving the joint map, or demoting the headline if it cannot give a non-trivial prediction, is the first theory task.
- **Spectrum map derived (v1.3, 15 Nov 09:26 ET; NOT yet refereed): `reviews/night2/SPECTRUM_MAP/README.md`.** In plain words: (i) the read-rate exponent 1/(1+2H) = 1/α also holds for the optimal linear predictor (self-similarity; only the constant drops); (ii) with noisy continuous sensing the error is q^{1/α}N^{1−1/α}/sin(π/α) (KNOWN, Afterman et al. 2022) and effort elasticities become α/(2α−1) in stakes and 1/(2α−1) in drift, so a = b holds only for reset reads; (iii) the optimal forgetting kernel's tail is τ^{−(1+α/2)}, steeper in redder worlds, exponential only at α = 2, negative weights for α > 2 (noiseless form KNOWN), so the 0.2–0.8 forgetting/need exponents measured in MATCH1 are hazards of re-occurrence, not optimal tracking kernels; (iv) the store count is one for any Markov (α = 2) world and otherwise K\* ≈ (ln 8R/2π²)·ln(stakes/upkeep): approximation theory plus a price, replacing "(log-span)^{2/3}"; (v) Lee–Flack–Krakauer's ½ is the α = 2 case of τ_m\* ∝ τ_E^{1−1/α} (single store: min(1−1/α, 2/3)) — regime A is "α = 2", not "one pace"; (vi) MATCH1 D3 explained (§2.4). **Recommendation from that file: demote "central new bet" to "a precise map built mostly from known pieces; new content is the assembly, the LFK-α prediction and the two-exponent split for event worlds".** The §2.2 rewrite waits for the referee (QUEUE THEORY-2.2-REWRITE).
- **Referee of the spectrum map (v1.3.1, 15 Nov 09:40 AM ET): `reviews/night2/SPECTRUM_MAP_REFEREE.md`.** (i) confirmed (wording: it holds for rescaling-closed predictors, not for every linear predictor); (ii) confirmed, citation verified; the elasticities assume linear precision pricing; (iii) tail and sign confirmed/KNOWN, but the inference "so MATCH1's exponents are not kernels" is withdrawn (the kernel's survival decays as τ^{−α/2}, which can lie in 0.2–0.8; no kernel was measured); (iv) prior-art complexity plus a price (Jiang et al. 2017; Benna & Fusi 2016); "one store at α = 2" is a knife-edge (excess ≈ 0.14(α−2)²); (v) correct in-model, but the τ_E exponent holds only at fixed environmental variance (at fixed q it is 0); the normalisation-free law τ_m ∝ (N/q)^{1/α} is KNOWN, and the α = 2 case predates LFK (Mora & Nemenman 2019); (vi) see §2.4 D3 row. **The referee agrees with demoting "central new bet" and goes further:** the tracking layer is classical filtering and approximation theory plus a price; the open contribution is the empirical bet that real systems sit near these optima once α, q and N are measured on the same system. Proposed §0 wording is in that report §7 (applying it is THEORY-2.2-REWRITE, Chad-visible).
- **Rule for every prediction (binding).** State the regime first, measured on the same system: single-pace (A), scale-free with measured H or α (B), many modes with measured β (C), or not established. Then derive the exponent for that regime from this file, quoting the section. A formal-layer constant computed at H = ½ is a regime-A prediction and must not be presented as "GTAO's prediction" for a world whose regime is unmeasured. Premises of the cited result (for example a stable, known per-item drift rate) are checked before the result is applied.
- **Surprise-guided follow-up (Proposition SG, in-model, elementary; `reviews/night2/AUDIT_DIVERGENCE.md` §6).** With changes as a renewal process and new evidence of likelihood ratio Λ, follow an item up iff w·L·p > c. In regime A the time since the last change carries no information. In regime B, modelled (a modelling choice, not a derivation from the spectrum) as a Lomax decreasing hazard, the surprise needed rises with the item's dormancy: slope 1 on ln(dormancy) **in the large-age limit** (a ≫ Δ, a₀); the exact slope is 0.70 at a = 3Δ and 0.947 fitted over ages 3–1000. Recently changed items need almost none. Prior art is close (restless bandits and Whittle indices, crawler revisit policies, Bayesian surprise); the regime-conditional clock is the only candidate addition. It now orders `QUEUE.md`, and its choices are logged so it can be scored.

---

## 3. Design rules as consequences (mostly KNOWN)

Taken one by one these are prior art. They are listed because one budget produces most of them, and because each has a stated condition under which it fails (`theory/MATH_ATTACK.md` §1.4; `theory/GENERAL_THEOREM.md`).

| Rule | Plain form | Status | Closest prior art | Fails when |
|---|---|---|---|---|
| 1 | Act early; interrupt only if stake × P(relevant) + learning value > cost | Near-tautology | Howard 1966; Denrell & March 2001 | Myopic interrupts (counterexample in Theorem G notes) |
| 2 | Keep a fact while need × miss cost > upkeep; upkeep rises with drift; fade recoverably | PROOF (T1a/T5b) | Anderson & Schooler 1991; McNamara & Houston 1987; Lee, Flack & Krakauer 2024 | Where need is scale-free, fading should follow a power law, not an exponential |
| 3 | Move a belief by the reliability of the signal | KNOWN | Kalman 1960; Muth 1960 | Heavy-tailed noise (Cauchy counterexample) |
| 4 | Keep prior versions; frozen history is nearly free | Near-tautology | Append-only logs; Bateson 1963 | — |
| 5 | Copy error grows with hops and with drift since the last check; recheck when too big | PROOF for Markov states | Bailis et al. 2012; Demers et al. 1987 | Non-Markov observed variables (seasonality) |
| 6 | Record used / ignored / late; use strengthens, disuse fades | Weak (value of information ≥ 0) | Hebb 1949; stigmergy; Lee, Flack & Krakauer 2024 | The *mechanism* does not follow from the budget. "No one in charge" is narrowed in §6 |
| 7 | Watching effort rises with stakes and drift, then collapses (N5); watch most where shock/buffer is large but not overwhelming | PROOF in two cases | Reis 2006; Sims 2003; Cho & Garcia-Molina 2003 | The interior peak holds only for fixed-delay fixing |
| Freeze-or-hold | Freeze (stop refreshing, keep the copy) when the world barely drifts and storage is cheap | PROOF (Theorem G: a checked copy beats fading iff drift × check cost < Φ) | Bateson 1963; Waddington 1953 | — |
| Bet-hedging | "Every system pays for a model" | **FAILS** as stated: a blind bet-hedging population can beat sensing | Kussell & Leibler 2005 | Holds only with the population redefined as the agent |

---

## 4. Failure, buffers and the "temperature"

**The index.** With buffer B, diffusive shock size σ and one fixing timescale τ, the hazard must take the form h = F(z)/τ with z = B/(σ√τ). This holds for any fix mechanism, by dimensional analysis (PROOF, `theory/MATH_ATTACK.md` §2). Its inverse, σ√τ/B, is the "temperature".

**Credit.**
- z is the **inventory safety factor** in the textbook rule SS = z·σ·√(lead time) (e.g. Silver, Pyke & Thomas 2017; the formula was checked through search summaries, not the book). The ratio itself is not new.
- For diffusive errors with full resets, per-window ruin is exactly erfc(B/(σ√(2τ))). That is **Black & Cox's (1976) first-passage default probability** with zero drift (checked numerically, `theory/GENERAL_THEOREM.md` R2). Merton's (1974) terminal-default version is off by a factor of 2. Earlier wording that called this "Merton's distance to default" is superseded.
- Related: Kramers 1940; Lande 1993; Galbraith 1974 and Thompson 1967 (slack vs information-processing speed); Chevin, Lande & Mace 2010; Scheffer et al. 2009 (critical slowing down).

**What may be new.**
- **The identity** ε_B = −ε_σ and ε_τ = ε_σ/2 − 1, for every fix mechanism. Slow fixing raises the hazard iff ε_σ > 2. In the "hot" regime (small z) the unit fails before any fix arrives and τ becomes invisible. In a discrete-incident regime ε_τ = ε_σ/2.
- **The fixed-spread sign** (N3): ε_τ = −1 at fixed observed spread.
- **Universality classes set by how fixing works**, not by scale: fixed delay gives an e^{−z²/2} tail; proportional restoring (OU) e^{−z²}; fixing at a random Poisson rate a fat e^{−√2·z} tail; heavy-tailed fix times a power law in z.
- **Coarse-graining rules:** pooling cools, z′ = z·√(N/(1+(N−1)ρ)) up to a ceiling z/√ρ; the weakest link heats, z′ ≈ √(z² − ln N). Heterogeneous fix speeds aggregate to long memory, and a single-τ fit then mispredicts failure by 1.4–2.4×.

**Results.** See §8, which follows the independent review of DECISIVE and F1. Every sign was right, and the numbers reproduce, but the τ term as a theory-specific claim is falsified by MATH_ATTACK's literal joint kill rule (populations on any reading; glucose on the full sample; banks are sign-only, not a hit). "Fewer crossings at fixed spread with slower correction" follows from dimensional analysis and standard first-passage results. The theory-specific structure — the −1 exponent, the √τ weighting, the identities, the τ-buffer interaction, and one collapse curve — failed. F1's τ mostly measures fixed-cost share. C3 found no τ effect in open-source projects, and the math attack showed that test could not have seen τ as measured. C3 also ruled out the reset-clock mechanism at that scale: at C3's numbers it predicts a hazard ratio of about 11 per doubling of τ, while C3 measured about 1.0 (upper CI ≈ 1.09), so at most about 1–5% of open-source dormancy can come from diffusive error reset at issue close (`theory/GENERAL_THEOREM.md` §0 item 5). That kills the mechanism for that proxy and scale, not the index where errors really are diffusive.

---

## 5. The missing lever: reduce the world's drift

Every earlier rule treated drift σ as given. Real adaptive organizations spend heavily on *lowering* it:
- **homeostasis and allostasis** hold an internal milieu steady so fewer variables need tracking (Sterling 2012);
- **niche construction and stigmergy** reshape the environment so it changes less, which Lee, Flack & Krakauer (2022 preprint; 2024) call outsourced memory; planetary-scale versions appear in Lenton et al. 2018;
- **buffering and smoothing** protect a firm's core (Thompson 1967, *classic, not re-fetched*);
- **contracts, schedules, regulation and routines** fix parts of the future in advance (no single citation was verified for this list in the sweep; treat it as the theory's own framing).

**The change.** Add a control on σ with its own cost g(σ₀ → σ). Tracking and drift reduction then become substitutes. The draft makes three predictions (HYPOTHESIS, untested):
1. **Substitution:** at matched stakes, organizations that spend more on reducing drift spend less on watching, so "under-watching" relative to the tracking rules is expected wherever drift has been bought down. Without this lever, such cases look like failures of the theory.
2. **Who pays:** drift reduction is favoured when its benefits are private. When they are shared, it is a public good, under-supplied without enforcement (Lee, Flack & Krakauer 2024; §6).
3. **One testable form** (speculative): firms facing more demand volatility lengthen customer contracts when they can capture the benefit (SEC full-text contract terms vs sales volatility).

---

## 6. Levels, shared memory and who is in charge

**When a new level pays.** A level is a shared model of a common driver. Three gains can justify it, each with its own condition: pooling (one model serves many facts; T3a threshold, N2), per-level clocks (at most 29% saving for two levels; T3b, KNOWN via Roundy 1985), and per-level checking tiers. Against these it pays upkeep plus a decoupling error that grows as timescales collapse (T3c). There is no theorem that nested always beats flat; with no shared drift, nesting loses by its upkeep.

**Shared memory is a commons.** A trail, a price, a wiki page or a shared library is stigmergic memory. Lee, Flack & Krakauer 2024 show environmental stabilization is a public good that free riders invade unless its benefits are monopolized. The math attack shows decentralized parts under-watch shared memory unless the whole's failure cost reaches them (`theory/MATH_ATTACK.md` §3.5). Ostrom's work (Ostrom 1990, *classic, not re-fetched*; Ostrom 2010) shows that lasting commons have rules, monitoring and sanctions.

**Narrowed claim.** Earlier drafts said "no one in charge, at every level". The claim now reads:
> **No one *needs* to be in charge *when* maintaining shared memory is privately rewarded** (each contributor's own use pays for its deposits, as with ants on a trail they themselves follow). **Otherwise expect enforcement**: monitors, sanctions, owners or hierarchy, appearing exactly where shared memory is a public good.

Prediction (HYPOTHESIS, untested): the staleness of shared memory rises with users per maintainer (e.g. package dependents per active maintainer vs documentation lag after an API change), and enforcement structures appear where that ratio is high.

**Fractal vigilance (night 1).** The idea that every level has a tracker that watches what its own members share (shared and private are relative to the level) is **prior art qualitatively**: Beer's Viable System Model puts System 4 ("outside and then") at every level of recursion, and Mintzberg makes every manager the unit's "monitor". The quantitative version is the theory's own and is **untested on fair data**:
- the exact onset vigilance V(N\*) = ½(1 + (1+ρ)^{−1/2})(1 + √(1 + 4h′(√(1+ρ)−1)/(rρ))) for reset-type sensing (the level's effort over a *flat* member's effort);
- its floor 1 + (1+ρ)^{−1/2} for any upkeep and price;
- its price invariance at zero upkeep;
- its growth as N^a.

The PIAAC and Enron tests measured a different quantity (supervisors versus the people they supervise, self-report, received mail). A fair-kill specification is in `reviews/night1/CLAIM_MAP_FINAL.md` §3.2.

**The √N sign flip** (N1) lives here: pooled independent deposits make faster turnover optimal for drifting targets, while repeated use preserves forms for stable targets. Its required condition is *independent* deposits; trail-followers who deposit where the trail already is have a smaller effective N.

---

## 7. Where optimality should hold, and where it should not

The theory describes efficient design. Efficient design appears only where selection is strong enough to find it.
- **Drift barrier.** Lynch et al. 2016 (and Lynch 2010) show that below a selection-strength threshold, set by effective population size, traits such as replication fidelity drift away from their optimum because selection cannot see small gains. The same ceiling should apply to any level: small populations, protected firms, bureaucracies and monopolies should sit *further* from the rules here.
- **Inertia and lock-in.** Hannan & Freeman (1984, as cited in the sweep) argue selection can favour inertia because reorganizing raises mortality; lock-in means past choices, not current drift, can set memory.
- **Rule of use.** Expect the predictions to hold in strongly competed, high-turnover settings (bacteria under strong selection, competitive industries, sensory systems tested every second). Expect misses where selection is weak. A miss in a weakly selected system is weak evidence against the theory; a miss under strong selection is strong evidence. That split must be fixed **before** a test, never used to explain a miss afterward.
- **Speculative extension:** how close each level gets to its cost floor (c_eff/kT for cells; cost per decision-relevant bit for firms) should scale with selection strength.

---

## 8. Test results, stated as they came out

Dates America/New_York, 13–14 November 2026. For DECISIVE and F1, the verdicts below follow the independent review in `reviews/DECISIVE_F1_REVIEW.md` (not fully blind: the reviewer had the results and write-ups), not the tests' own more generous labels. Other tests follow their locked rules and, unless marked, have not had an independent review.

The preregistration commits lived only in local, unpushed git repos. Adding their histories to this private repository (as `tests/<name>/history.bundle` where a bundle could be shipped without excluded data, and as `tests/<name>/history.txt` receipts for every test) gives them an **external timestamp only from today**. The author dates inside those histories are self-attested.

| Test | Scale | Result in plain words | Verdict |
|---|---|---|---|
| **DECISIVE / banks** | Firm (7,837 US banks, 419 failures 2008–14) | Slower capital correction predicted failure at fixed shock and buffer: β = +0.20 [0.11, 0.29], about 15% higher hazard per doubling, and it adds to the standard Z-score (ΔAIC 15). The sign holds only for detrended τ; the specified own-mean τ is null. The identity, ε_B = −ε_σ and the √τ-horizon test all failed | **Sign-only, not a HIT.** Reviewed: `reviews/DECISIVE_F1_REVIEW.md` |
| **DECISIVE / glucose** | Organism (224 adults with type 1 diabetes, 27k low episodes; replication cohort 125) | At fixed glucose spread, slower correctors had fewer lows: slope −0.46 [−0.70, −0.23], vs a theory-implied −0.82 and a literal −1. Standard risk indices predict 0. Cross-cohort collapse failed; the cold regime is not evaluable (n = 2). The test's own prereg, scored against a lowered sampling-corrected target, does not kill; those targets rewrote the kill rule after MATH_ATTACK wrote it | SIGN-RIGHT, SIZE-OFF; **MATH_ATTACK literal joint kill fires on the full sample.** Reviewed |
| **DECISIVE / populations** | Population (274 GPDD series, 238 crossings) | Fixed-spread slope −0.21 [−0.37, −0.05] vs a sampling-corrected −0.34. Cold-regime slope has the wrong sign, where the theory says the effect should be strongest. τ does not beat the classic density-independent model. Half the series are fur-harvest records; source fixed effects, taxon clustering, or dropping clipped series remove significance. The test's own prereg against the sampling-corrected target does not kill, but those targets rewrote the rule | **MATH_ATTACK literal joint kill fires on any reading.** Should not be cited as support. Reviewed |
| **F1** | Firm (≈ 4,100 US public firm-cohorts, 183 bankruptcies) | All four predicted directions held. Slow cost adjusters failed more (≈ 28% per doubling), but that link is published and τ mostly measures fixed-cost share (operating leverage), not correction speed, so construct validity fails. The novel shock-by-buffer interaction missed (p = 0.055); the data prefer a τ weight near 1 over ½ (suggestive only; 3 grid points, likelihood gap 2.9). The prereg kill rules did not fire | **INCONCLUSIVE; not a theory-specific hit.** Reviewed |
| **C3** | Open-source projects (896) | τ added nothing (hazard ratio ≈ 1.00 per doubling); buffers mattered (known). The math attack shows this design could not have seen τ, so it is uninformative rather than a refutation. It does reject the reset-clock mechanism, which predicted ≈ 11 per doubling | INCONCLUSIVE (prereg text) / MISS (code as run). Only a same-executor skeptical pass (`tests/C3/REVIEW.md`), not independent |
| **BIO1** | Cells, immune systems, ants, neurons (literature) | Drift-matching holds where checked, but almost entirely as prior art. Immune *lifetime* did not track pathogen drift as first read. Neural slope ≈ 1 | Global kill not triggered; one locked contradiction (P3a). Literature check, not blind |
| **COLLAPSE1** | Many substrates | The immune "contradiction" was largely a measurement artifact: under power-law waning (Saha et al. 2025), a measured half-life grows with the age at which it is measured, and 5 of 8 antigens fall on one line once that is accounted for (a consistency check, not independent). Code re-edit need decays as a power law (exponent ≈ 0.6). The immune cue model and inventory buffering were killed; the timescale-collapse plot proved non-diagnostic | Mixed: A1 and C2 killed; E1/E5 pass (weak) |
| **MATCH1** | News, code, Wikipedia, measles | Exact need-vs-memory exponent match **failed** (0.24 vs 0.71). Freeze-or-hold **passed** on measles: towns' measles-return odds fall with exponent 2.15 while antibodies decay at 0.11 (caveats: town-level presence ≠ individual exposure; age − 5 as time since infection; 39 informative lags). Need exponents 0.6–0.8 replicate across code, Wikipedia and news. Layer count inconclusive; redness sign opposite | See §2.4. Not reviewed |
| **DRIFT1** | Wikipedia, firms, city services | City 311 looks scale-free across categories; Wikipedia and filings have characteristic cadences | Kill not triggered; supports T7 as conditional |
| **ANTS1** | Simulated ants | Finished 15 Nov; see §8b | 3 locked in-model failures; passes mostly by construction |
| **C3b** | Open-source exogenous shocks | Preregistered; not finished | — |

**Overall reading (following the independent review).** The numbers in all four DECISIVE/F1 arms reproduce exactly, and every directional sign is right. That does not support the τ term as a claim of this theory. MATH_ATTACK's literal joint kill rule **fires**: for populations on any reading, and for glucose on the full sample (the cold cell there is empty, n = 2). Banks are **sign-only, not a hit**. "Fewer crossings at fixed spread with slower correction" follows from dimensional analysis (a crossing rate has units of 1/time, so rate = τ⁻¹·f(B/s)) and standard first-passage results (Siegert 1951; Black–Cox 1976; Lande & Orzack 1988). A generic mean-reverting process with a barrier predicts the same signs. The theory-specific structure failed wherever it was tested: the −1 exponent, the √τ weighting, the identities, the τ-buffer (z) interaction, and one collapse curve. In F1, τ mostly measures fixed-cost share, so that arm does not test the construct. The lowered sampling-corrected targets (β\* = −0.82/−0.65 in glucose, −0.34 in populations) are mathematically right for a finitely sampled OU process, but they rewrote the kill rule after MATH_ATTACK wrote it; this draft leads with the literal verdict. C3 rejected the version where a fixed clock dominates risk. Reading the missed exponents as "the single-timescale (½) form is a special case of the spectrum relation in §2" is itself POST HOC and must be tested in its own right.

## 8b. Night 1 scoreboard (15 November 2026, America/New_York)

Source: `reviews/night1/CLAIM_MAP_FINAL.md` (150 claim rows; every row has exactly one status). The three hostile reviews were independent of the authors, and each wrote its verdicts before reading the project's own claim map.

Locks, applying to everything in this table:
- Every night-1 lock is **self-attested**: local commits, no third-party timestamp (Chad waived timestamping for night 1).
- The referee re-verified the hashes and found no sign that any outcome was seen before a lock.
- But several stated times inside files contradict the lock records.
- The Enron analysis code was edited 6 seconds after its first lock (amended lock; the pre-edit file was not kept).
- The LAYERS1 code was not hashed.
- The PIAAC raw data were deleted after the run.

| Test | Kind | Result in plain words | Verdict |
|---|---|---|---|
| **FORMAL** (axioms, theorems T1–T8, extensions) | Mathematics, in-model | The algebraic core re-derived independently and correct. **Wrong as stated:** "V ≥ 2 at onset for every upkeep and price" (replaced by an exact formula; at zero upkeep the value is 1 + (1+ρ)^{−1/2}, between 1 and 2); "shared change always lowers the onset size" under mixed technologies (true only at small ρ or with a common technology); several "iff" claims (T5.2, T7(c), Cor 4.1); T7(b)'s example holds only at zero upkeep. T4's proof is a sketch (the conclusion was confirmed by exact optimization). Novelty labels downgraded: the core is inventory pooling, EOQ, team theory and Topkis | **PROVED in-model, with corrections.** Says nothing about real systems |
| **P1** (theory-v3) | Real data: news recall, item level | Slope 0.31 locked (independent re-fit 0.321, 95% CI 0.289–0.352) vs predicted 0.5–1.2. The rival's 0.24 is also excluded | **Failed on proxy "headline-word recurrence as need"** (PROXY-FAIL) |
| **VIGIL** (OECD PIAAC, 9 countries) | Real data: survey | Supervisors read external material 1.14× (CI 1.05–1.23) as often as comparable members; replication 1.19. Not specific to shared external drivers once correctly specified (1.06, CI 0.98–1.16). Span gradient 0.02–0.04 vs 0.5. Size 1.15, which is no longer in conflict with a floor of 2 (there is none at finite ρ) but was never a fair test of the size | **Direction PASSED, but it is Mintzberg's prior art.** Specificity null, growth not seen; OPEN |
| **VIGIL-2** (Enron email, 98 mailboxes) | Real data: behavioural | The external share of received mail does not rise with rank (0.93 per level); external volume is flat. Adequately powered. Weak construct (received mail, assistants, no span) | **Failed on proxy "external share of received mail"** (PROXY-FAIL) on this instrument |
| **POOLSIM** | Simulation | Learners find the −1, −½ and 0 slopes, but the simulator's own expected-cost crossing gives the same slopes with no learners | **CIRCULAR.** One valid finding: the small-ρ onset is invisible when decision noise is ≥ 1% of cost |
| **W5 check** | Simulation, independent reimplementation | Under true bundled absolute loss the exponent is −1. The earlier −2 came from splitting the loss | In-model only; it led to theorem T4 |
| **SENSING** round 1 | Simulation | Classes A and A2 hit −2 and −1.5, but the "measured" (a, b) read back the code's own cost rule. Class R missed the locked criterion (−0.92) | A, A2 **CIRCULAR**; class R **KILLED** (locked criterion); the rival not killed |
| **SENSING2** | Simulation, evolved sensing | The one risky world (exponent −2.1) gave −0.49: a **locked kill**. Caveats documented post-lock: a 1.5% flat-cost bias in a world whose onset gap is a few thousandths, and a locked flat-arm bug (51–66%) that made the other worlds inconclusive. The contrast that separates "members set the exponent" from "the level's technology sets it" was not cleanly run | **KILLED** (locked), with documented caveats |
| **ANTS1** | Simulation | Fade-exponent passes are by construction. An ant-like readout does not pool error as N^{−½}; the lock-in mimic is not distinguishable in jump worlds; no interior forgetting optimum in fast jump worlds | **3 locked failures**; passes circular or self-consistency checks |
| **LAYERS1** | Mathematics, in-model | Span invariance of layer spacing failed (6/12); the other passes are uninformative or by construction | **KILLED** (P2); the rest is approximation theory plus a price |

**Candidates for the theory's own content (v1.2 wording).** All six are in-model results of the formal layer, elementary, untested on any valid real-data instrument, and not yet cleared by a targeted prior-art sweep (QUEUE Q1). Their quoted constants are regime-A (H = ½) instances (§2.5). The night-1 sweep named close prior work for item 1 (Bimpikis & Markakis 2016) and item 5 (Abolhassani 2024) [named in the sweep; not re-verified here]. The headline of this theory (§2, the spectrum → design map) is **not** on this list because it has not been derived; Proposition SG (§2.5) is at most a regime-conditional increment on restless-bandit and crawler-revisit prior art.
1. The sensing class (a, b) of the **level** sets the onset exponent, −(1−b)/(1−a), with the upkeep dichotomy and the exact closed form.
2. Under bundled decisions, the sensing technology, not the loss function, sets the exponent.
3. The exact vigilance formula, its floor, its price invariance, and the criterion "V > 1 for all costs iff a ≥ b".
4. The ordering threshold κ\* = 1/|e_g| for top-down versus bottom-up hierarchies.
5. The closed-form freeze/hold/lookup band, its N² widening for shared stores, and the dissolution order under cheap lookup.
6. The programme: measure the level's sensing technology independently, then predict the group's exponents.

**Before any public novelty claim:** forward-citation sweeps of Marschak & Radner 1972 ch. 7 §5 and of Van Zandt & Radner 2001 must be run. They are the likeliest places for an earlier statement of item 1.

**Corrections to earlier project documents:**
- "Team theory is static" (CORE_AUDIT) is false: Marschak & Radner ch. 7, Aoki 1986, Van Zandt & Radner 2001 and Radner 1993 are dynamic.
- The Alonso, Dessein & Matouschek 2008 citation for "centralize common, decentralize local" is a miscitation. Use Acemoglu et al. 2007, Van Zandt & Radner 2001 and Hayek 1945.
- "Nobody has stated these across substrates" should read "not quantitatively": Beer's Viable System Model is a qualitative cross-substrate, recursive claim.
- The immune freeze/hold/lookup application must credit Mayer et al. 2016, and the cell-sensing class must credit Mora & Nemenman 2019.
- "Volatility promotes levels" assumes zero processing delay. The delay literature (Aoki 1986; Radner 1993; Meagher, Orbay & Van Zandt 2001) and Aghion et al. 2021 point the other way.

---

### 8c. Night 2 (15 November 2026), read under §2.5
- **VIGIL_ONA** (nomination networks): blind referee downgraded the direction and the beyond-status tilt (Lazega-driven, not robust to seniority) and overturned the span test to inconclusive. Vigilance **OPEN**.
- **MEASURE-SELF** (Ace's own memory store): the √(drift × stakes) allocation it tested is the regime-A instance (§2.5), and its premise failed: an item's change rate was not a stable property (Spearman −0.06). So P3b is "failed on a statement-time proxy; premise unmet (scope)", not a test of the spectrum core. The burstiness "pass" is explained by the observer's conversation schedule (referee null band 0.60–0.92 contains 0.82); the regime is **not established**. Closed items stayed closed (0/21; non-discriminating). Most later changes were dormant items reawakening, which no schedule caught (motivates §2.5 Proposition SG). Details: `reviews/night2/SELF/`, `reviews/night2/REFEREE/REPORT.md`, `reviews/night2/AUDIT_DIVERGENCE.md`.
- **Audit:** `reviews/night2/AUDIT_DIVERGENCE.md` lists where the project's working summaries had drifted from this file and why.

---

## 9. What would sink the theory

- **The spectrum relation fails twice:** the design exponent stays constant as the environment's measured spectrum changes, at two scales with locked tests.
- **The fixed-spread sign reverses** (positive slope) at two scales in the cold regime.
- **√N fails on languages and wikis** as specified in N1, and the drift-dependent sign flip is absent.
- **New levels ignore ρ** (N2) where the threshold can be measured.
- **Strong selection, still no fit:** in strongly selected systems, designs show no relation to drift, buffers or spectra at all. Misses in weakly selected systems do not count toward this (§7), but only if the system was classified before the test.
- **Vigilance under a fair instrument:** on a pre-declared, same-driver, all-channel sampling measure against a flat comparator, in units measured to be reset-type (class R), the level's effort stays clearly below the floor 1 + (1+ρ)^{−1/2} that holds for every upkeep and price (spec: `reviews/night1/CLAIM_MAP_FINAL.md` §3.2).
- **The onset relation in agents not given the cost function:** with ρ manipulated over ≥ 1.5 decades in a regime where the prize exceeds decision noise, and the level's sensing class measured separately, the onset exponent excludes −(1−b_L)/(1−a_L).
- **Structural:** every claim must stay tied to an exponent, a sign or a threshold with a named competitor. A theory of "any adaptive organization" that drifts into unfalsifiable language should be treated as failed, as the free-energy principle has been criticized for (Aguilera et al. 2022; Bruineberg et al. 2022).

---

## 10. Prior art credited

Verification key: **[DOI]** resolved against Crossref in the sweep (`litmap/verify/VERIFIED_DOIS.txt`); **[fetched]** checked from a publisher page, abstract or full text in the sweep or a review; **[search]** checked only through search summaries; **[classic, not fetched]** standard reference not re-fetched; **[unverified]** cited from internal notes only. Full entries are in `litmap/LITMAP.md`.

**Memory scaling, outsourced memory, free riders**
- Lee, Flack & Krakauer 2024, "Constructing stability: optimal learning in noisy ecological niches", *Proc R Soc B* 291:20241606, doi 10.1098/rspb.2024.1606 [DOI]; preprint "Outsourcing memory through niche construction", arXiv 2209.00476 / bioRxiv doi 10.1101/2022.09.01.506204 [DOI; read in full]. Optimal memory τ_m\* ∼ τ_E^{1/2}; stigmergy and niche construction as outsourced memory; stabilization as a public good open to free riders. **The most important prior art.**

**Failure, buffers, temperature**
- Silver, Pyke & Thomas 2017, *Inventory and Production Management in Supply Chains*, 4th ed., CRC, doi 10.1201/9781315374406 [search: formula checked via summaries, not the book].
- Black & Cox 1976, *J Finance* 31:351 [unverified: from the theorem notes; DOI not resolved in the sweep]. Merton 1974, *J Finance* 29:449 [unverified, same].
- Galbraith 1974, *Interfaces* 4(3):28 [fetched]; Thompson 1967 [classic, not fetched]; Scheffer et al. 2009, *Nature* 461:53 [DOI].

**Memory form and layers**
- Anderson & Schooler 1991, *Psychol Sci* 2:396, doi 10.1111/j.1467-9280.1991.tb00174.x [DOI]; Anderson 1990 (recall odds = C·(need odds)^d) [cited in MATCH1; not fetched].
- Benna & Fusi 2016, *Nat Neurosci* 19:1697, doi 10.1038/nn.4401 [DOI]; Fusi, Drew & Abbott 2005, *Neuron* 45:599 [DOI].
- Shankar & Howard 2013, "Optimally fuzzy temporal memory", *JMLR* 14:3785 [fetched: JMLR page].
- Brand 1994, *How Buildings Learn* [classic, not fetched]; Brand 2018, "Pace Layering", *J Design & Science* [fetched].
- Holling 1973, *Annu Rev Ecol Syst* 4:1 [DOI]; Holling 1992, *Ecol Monogr* 62:447 [DOI]; Holling 2001, *Ecosystems* 4:390 [DOI].
- Roundy 1985 (power-of-two policies) [unverified: from the theorem notes].
- Fairhall et al. 2001, *Nature* 412:787 [fetched, BIO1]; Wark et al. 2009 [fetched, COLLAPSE1].
- Saha et al. 2025, "Quantifying the waning of humoral immunity", medRxiv doi 10.1101/2025.05.13.25327542 [fetched, COLLAPSE1].
- Meeter, Murre & Janssen 2005 (news-recall data) [data fetched, MATCH1]; Antia et al. 2018 (measles antibody cohort) [data fetched, MATCH1].
- Challet & Lombardoni 2008 (power-law file-modification ageing in software) [fetched: repository page]; Wu 2006 (Waterloo thesis) [search].

**Information, thermodynamics and control**
- Mitter & Newton 2005, *J Stat Phys* 118:145 [fetched by the math review].
- Horowitz & Sandberg 2014, *New J Phys* 16:125007 [fetched by the math review].
- Stratonovich 1965, value of information (English edition: Belavkin et al., eds., *Theory of Information and its Value*, Springer 2020) [fetched by the math review only].
- Nair & Evans 2004, *SIAM J Control Optim* 43:413 [fetched]; Tatikonda & Mitter 2004, *IEEE Trans Autom Control* 49:1056 [fetched].
- Polani 2009, "Information: currency of life?", *HFSP J* 3:307, doi 10.2976/1.3171566 [DOI]; Polani, Nehaniv, Martinetz & Kim 2006, ALife X [fetched by the math review only].
- Shalizi & Crutchfield 2001, *J Stat Phys* 104:817 [fetched].
- Still, Sivak, Bell & Crooks 2012, *PRL* 109:120604 [DOI]; Barato, Hartich & Seifert 2014, *New J Phys* 16:103024 [DOI]; Laughlin et al. 1998, *Nat Neurosci* 1:36 [fetched].
- Ruderman & Bialek 1994, *PRL* 73:814 [fetched].
- Francis & Wonham 1976, *Automatica* 12:457 [DOI]; Conant & Ashby 1970 [DOI].
- Some page numbers in `theory/INTERNAL_MODEL.md` (e.g. Kussell & Leibler, Mayer et al., Palmer et al.) were written from memory; titles and DOIs were fetched. **Check page numbers before public use.**

**Fluctuating environments**
- Kussell & Leibler 2005, *Science* 309:2075, doi 10.1126/science.1114383 [DOI].
- McNamara & Houston 1987, *J Theor Biol* 125:385 [DOI].

**Rules and attention**
- Reis 2006, *Rev Econ Stud* 73:793 [fetched]; Alvarez, Lippi & Paciello 2011, *QJE* 126:1909 [DOI]; Sims 2003, *J Monet Econ* 50:665 [DOI]; Cho & Garcia-Molina 2003 [unverified: from the theorem notes].

**Shared memory, languages, commons**
- Lieberman et al. 2007, *Nature* 449:713 [DOI]; Pagel, Atkinson & Meade 2007, *Nature* 449:717 [DOI]; Bromham et al. 2015, *PNAS* 112:2097 [DOI]; Beekman, Sumpter & Ratnieks 2001, *PNAS* 98:9703 [DOI].
- Ostrom 1990, *Governing the Commons* [classic, not fetched]; Ostrom 2010, *AER* 100:641, doi 10.1257/aer.100.3.641 [DOI].

**Drift reduction**
- Sterling 2012, "Allostasis", *Physiol Behav* 106:5 [DOI]; Lenton et al. 2018, *TREE* 33:633 [DOI].

**Limits on optimality**
- Lynch, Ackerman, Gout et al. 2016, *Nat Rev Genet* 17:704, doi 10.1038/nrg.2016.104 [DOI]; Lynch 2010, *Trends Genet* 26:345 [DOI].
- Hannan & Freeman 1984 [unverified in the sweep; Hannan & Freeman 1977 is DOI-verified].

**Credited after the night-1 prior-art review (15 Nov 2026).** The markers are the referee's: [FULL] text read; [OCR] scan read by OCR; [ABS] abstract only; [SEC] secondary source; [BIB] bibliography only; [UNVERIFIED] memory only. Details are in `reviews/night1/REVIEW_PRIORART.md`.

**Team theory and information economics**
- Marschak & Radner 1972, *Economic Theory of Teams*, ch. 7 §5, eq. 5.13 (√ recovery frequency) and ch. 7 §6 (dynamic team size) [OCR].
- Van Zandt & Radner 2001, *Economic Theory* 17:545 [FULL].
- Veldkamp & Wolfers 2007, *JME* [FULL].
- Wilson 1975 [ABS].
- Aoki 1986, *AER* 76:971 [FULL].
- Radner 1993, *Econometrica* 61:1109 [FULL].
- Meagher, Orbay & Van Zandt 2001, CEPR DP 2839 [ABS].
- Acemoglu, Aghion, Lelarge, Van Reenen & Zilibotti 2007, *QJE* 122:1759 [ABS].
- Hayek 1945, *AER* 35:519 [BIB].
- Geanakoplos & Milgrom 1991 [FULL, discussion-paper text].
- Dessein, Galeotti & Santos 2016 [FULL].
- **Dessein & Santos 2006, "Adaptive Organizations", *JPE* 114:956** [FULL] (title collision).
- Alonso, Dessein & Matouschek 2008 [FULL]: cite only for coordination versus adaptation.
- Vayanos 2003 [FULL].
- Crémer 1980 [ABS].
- Garicano 2000 [ABS].
- Bolton & Dewatripont 1994 [ABS].
- Bloom, Garicano, Sadun & Van Reenen 2014, *Mgmt Sci* 60:2859 [FULL].
- Aghion, Bloom, Lucking, Sadun & Van Reenen 2021, *AEJ: Applied* [FULL].

**Inattention and inspection sampling**
- Reis 2006 [FULL].
- Keller 1974 [ABS].
- Sheridan 1970 [ABS].
- Åström & Bernhardsson 2002 [SEC] (event-triggered sampling beats periodic when only transmission is costly).

**Pooling, lattices, caches**
- Eppen 1979 [ABS].
- Roundy 1985 [ABS].
- Maister 1976 (square-root law of inventory centralization) [named by the math referee; not verified].
- Topkis 1978 [ABS; DOI verified].
- Milgrom & Roberts 1990 [ABS].
- Gray & Putzolu 1987, the "five-minute rule" [BIB/SEC].
- Cho & Garcia-Molina 2003 [ABS/SEC].
- Wolman et al. 1999 [FULL].

**Biology and cognition**
- Mayer, Mora, Rivoire & Walczak 2016, *PNAS* 113:8630 [ABS].
- Mora & Nemenman 2019, *PRL* 123:198101 [ABS].
- Berg & Purcell 1977 [ABS].
- Rogers 1988 [FULL].
- Beckers et al. 1989 [FULL].
- Dornhaus et al. 2006 [FULL] (counter-evidence on colony size).
- Sparrow et al. 2011 [ABS].
- Sung et al. 2012 (drift barrier) [ABS].

**Cross-substrate and recursive organization**
- Beer, *What is cybernetics?* (2002 text) [FULL]; Beer 1984, *JORS* 35:7 [UNVERIFIED details].
- Galbraith 1974 [ABS].
- Simon 1962 [BIB].
- Kashtan & Alon 2005 [ABS].
- Mintzberg's monitor role [read in VIGIL's prior-art file].

**Unfalsifiability critiques**
- Aguilera et al. 2022, *Phys Life Rev* 40:24 [DOI]; Bruineberg et al. 2022, *Behav Brain Sci* 45 [DOI].

---

## 11. Next tests, in order

**The live queue is `QUEUE.md` (ordered by Proposition SG, §2.5).** The lists below are kept as history from 14–15 November.

**Updated 15 Nov 2026 after night 1.** Full specifications are in `reviews/night1/CLAIM_MAP_FINAL.md` §3.
1. **Prior-art sweeps before any public novelty claim:** forward citations of Marschak & Radner 1972 ch. 7 §5 and of Van Zandt & Radner 2001; Veldkamp 2011 ch. 8; the 2023 *JEL* rational-inattention survey; the inventory-pooling line.
2. **Process:**
   - external timestamp for every lock (needs Chad's go, because it is an outside or public act);
   - estimator dry-runs on synthetic truth before locking;
   - retained pre-amendment files;
   - hashed code;
   - kept raw data;
   - one master table of all locked predictions;
   - a blind analyst.
3. **Non-circular onset test:** agents not given the cost function, ρ manipulated over ≥ 1.5 decades, the level's sensing class measured separately, and a mixed-technology arm (level class ≠ member class).
4. **Fair vigilance test** (§3.2 of the claim map): same driver, all channels, flat comparator, class gate, kill at the floor 1 + (1+ρ)^{−1/2}.
5. **Opposite-signs factorial** (shared vs private volatility varied independently).
6. **Bundled-loss contrast** rerun with the level re-optimized and the SENSING2 flat-arm bug fixed.
7. Physics: derive one physical-unit bound for one sensing system, or drop the energy language.

**Earlier list (14 Nov), still open:**

1. **Spectrum → exponent, locked:** derive the mapping from a measured spectrum to the predicted forgetting exponent *first* (MATCH1's opposite-sign result makes this urgent), then test it on GDELT news drivers vs Wikipedia pageview response kernels, with a universal-kernel competitor.
2. **√N on Austronesian vocabulary** (ABVD): slope 0.5 vs 0 (neutral) vs 1.
3. **Lock the post-hoc "memory outlasts need" prediction** (§2.4) and test it where miss cost and upkeep can be measured.
4. **T7b layer count** with weekly and yearly cycles removed and the tolerance set from the measured noise floor before fitting.
5. **Drift-reduction substitution** (§5) and **users per maintainer vs staleness** (§6).
6. **Measure β for an organization** (e.g. PCA of demand shocks across product lines) and check whether its model exponent moves with it.
7. Finish ANTS1 and C3b. The independent review of DECISIVE and F1 is in `reviews/DECISIVE_F1_REVIEW.md`; a review of MATCH1 is still needed. The next preregistration should be pushed to a third-party-timestamped location (a public gist, OSF, or a Zenodo draft) *before* any outcome is pulled, and should include a generic OU-with-barrier competitor that GTAO must beat on the exponent, the collapse, or the interaction — not on sign alone.

## 12. Source files

- Math: `theory/THEOREMS.md`, `theory/MATH_ATTACK.md`, `theory/GENERAL_THEOREM.md`, `theory/INTERNAL_MODEL.md`, with code checks in `theory/*-checks/`.
- Tests: `tests/*/` (locked predictions with sha256, code, results; raw data excluded, see each `DATA.md`).
- Literature: `litmap/LITMAP.md`, `litmap/PRIOR_ART.md`, `litmap/THREATS.md`, `litmap/LEFT_ON_THE_TABLE.md`.
- Reviews: `reviews/`, including the DECISIVE/F1 independent review (`reviews/DECISIVE_F1_REVIEW.md`) and its checks.

## 13. Changelog
- **v1.2 (15 Nov 2026, 09:02 AM ET).** Rewrote the header and status block (it contradicted itself: "killed on real data" under a note that no field test measured validly; title "open" after Chad decided it). Added this file's canonical role. Added §2.5 (formal layer inside the spectrum core; "regime first" rule; Proposition SG). Added Chad's physics position to §2.3 as an open disagreement with its test. Added §8c (night 2). Pointed §11 to `QUEUE.md`. No locked prediction, result or proof was changed. Reason: `reviews/night2/AUDIT_DIVERGENCE.md`.
- **v1.3.1 (15 Nov 2026, 09:40 AM ET).** Pointer to `reviews/night2/SPECTRUM_MAP_REFEREE.md` added in §2.5; §2.4 D3 row corrected (explanation superseded, v1.3 text kept and marked). §0 and §2.2 text unchanged (THEORY-2.2-REWRITE). CLAIM_MAP_v2 → v2.2 (K12, K13, H19 MATH-CORRECTED; N10, N11 added). No locked prediction changed.
- **v1.3 (15 Nov 2026, 09:26 AM ET; pending referee).** Added the §2.5 pointer to `reviews/night2/SPECTRUM_MAP/` (spectrum map derived, mostly KNOWN pieces; demotion recommended, not yet applied) and updated the §2.4 D3 row (explained; locked D3S gap-shuffle passed on proxy). No locked prediction or proof changed; §2.2 text unchanged pending the referee.
- **v1.2.1 (15 Nov 2026, 09:14 AM ET).** Applied `reviews/night2/AUDIT_REFEREE.md` §6: §2.5 Axiom 6 sentence corrected; field "KILLED" in §1 and §8b replaced by "failed on proxy X"; §8b list relabelled as candidates; Proposition SG slope stated as a large-age limit with Lomax named as a modelling choice.
- v1.1 (15 Nov, 03:04 ET; measurement note 08:20 ET). Night-1 scoreboard (§8b); measurement-layer note.
- v1.0 (14 Nov, 23:09 ET, `cbe60a5`). Drift-spectrum core; prior-art credits; drift-reduction lever; narrowed "no one in charge".

