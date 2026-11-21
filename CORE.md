# The core: the cost of judgment on one page

*Draft, 20 Nov 2026, first written about 4:20 PM ET, revised after independent review (READY-WITH-FIXES; B1 and B2 applied) beginning 4:35 PM ET, results filled about 5:15 PM ET, revised again after the confirm review (B3 applied) about 5:25 PM ET, and revised after the IMP-N60 / cymatics / fractal scoring about 8:49 PM ET (America/New_York). Beside `main` `ff14a87` (PR #115 merged as v2.66, #117 as v2.67, #116 as v2.68, #118 hygiene as `ff14a87`; CLAIM_MAP tally OPEN 84, PROVED (in-model) 94, MATH-CORRECTED 23, PRIOR ART 32, total 318; 125 tests). The first review is at `reviews/core_2026-11-20/REVIEW.md`; the confirm review is at `reviews/core_2026-11-20/CONFIRM.md`; the re-confirm is at `reviews/core_2026-11-20/RECONFIRM.md`. Independent review of the IMP-N60 run: `reviews/rhythm_2026-11-20/REVIEW.md` (SCORING CORRECT). Remaining should-fixes are listed in `OPEN_WORK.md`. Proved (in-model) is not a claim about nature; open means untested, not refuted. IDs: `measurement/CLAIM_MAP_v2.md`.*

## 1. Definition

A system that must act ahead of a world it does not control chooses its design 𝒟 (layers, what each tracks, how often it reads, what it shares) to minimize

$$J(\mathcal D)=\kappa I_{\text{mem}}+hK+w\,\mathbb E[\ell_{\mathcal D}]+A(\mathcal D)+L(\mathcal D)\quad\text{subject to}\quad P(\text{ruin})\le\varepsilon .$$

- κI_mem + hK: memory held at price κ per nat, plus upkeep h per layer (a tracking store, not an org-chart level).
- w·E[ℓ]: stake times expected loss at the moment of use; lateness counts as error.
- A, L: the cost of reading the world, and of linking, telling and lookup.
- P(ruin) ≤ ε: a reserve paying J must not hit zero more often than ε. A hard cap, not a cost to average away.

The world is a measured input: how its variance spreads across time scales (its spectrum), plus read noise. One currency per system. Physics sets only floors on the prices (Landauer). The equation is a definition, built from known parts (the master-equation statement; J16's closed term list).

## 2. Principle

Strongly selected, persistent systems sit near argmin J, within the band their selection can resolve. This has the form of least action, but J has free prices, so it predicts only through price-free structure or independently measured prices. "Strongly selected" is operational (THEORY §3): a cost-to-fitness map σ, a population N_e, a band ε = 10/(σN_e) that excludes a named rival, and at least 10 redesign times in one world.

## 3. The hypothesis

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

Earned when qualifying systems in two classes at different scales fall inside their preregistered bands and beat a named rival. Killed by misses beyond the class's preregistered binomial allowance (for a small class, one). A needed cost missing from the closed list is a miss (J16). So is a design that does not move when its inputs change: a non-move is consistent only if the post-change gap g < Δ_R(k_lo); a miss if g > max(the static band, Δ_R(k_hi)); INDETERMINATE between; and if the predicted gap of a non-mover is ≤ Δ_R(k_hi), the move test is NOT A TEST (CT41).

## 4. The keystone candidate

Let ε_K = E_K/E_∞ − 1 and R = w·E_∞/h. In Model S (sums of OU modes), if ε_K is convex in K,

$$K^*=1+\#\{k\ge 2:\ R(\varepsilon_{k-1}-\varepsilon_k)>1\}.$$

**In Model S, layers equal the world's time scales whose stakes pay for them, counted by degree** (N60, #116; CT21, L1–L3). At most one layer for one real scale, even a self-similar random walk (CT21: K* ∈ {0, 1}; "scale-free ⇒ many layers" is false at α = 2). J separated real scales cap K* at J. A scale-free continuum has no finite end, so K* climbs with stakes and span.

**Conditional, and scoped.** The predictive keystone — layers from the world's time scales whose stakes pay for them, counted by degree — is proved or numerically supported only in Model S, and there only given convexity, which remains unproved. In Model S that convexity is numerical, in-model and field-untested: it held in every non-buggy world checked (39/40 in the #116 review; 120/120 Model S worlds rerun with the merged solver, `core/keystone_checks/S5_RESULTS.md`; a further 24 wide-search real-pole worlds still rest on the pre-#116 solver and are not counted). With rhythms and first-order real stores the increment formula is **false** (two oscillators, R = 3: argmin 3, formula 2; `core/KEYSTONE_NOTE.md`). A pair rule (a rhythm paid for as two layers) would predict even K* — 0, 2 or 4 in that example — but the independently confirmed argmin is 3, so that rescue does not recover K*. For rhythms, the only general statement is definitional: K* is argmin_K [K + R(1+ε_K)], which always coincides with the lower-convex-hull increment test on the measured ε_K curve, including K = 0 (`core/KEYSTONE_NOTE.md` §4, with the short proof). That is not a new rule, and it is not a prediction from the world's time scales alone. A preregistered internal-model count (IMP-N60: include a matched layer iff the isolated stake \(R V_m\) exceeds its cost) was misspecified as a generalization of N60 (isolated \(V_m\) vs joint increments) and **FAILED** its preregistered gates (PRIMARY 58/189 cost match, 51/189 composition match; also SANITY, MUST, and the Model-S regression; the tautology check passed, so this is a real miss, not an identity). It stays failed; no rescue is registered. Cymatics: discrete jumps **PASS** (the link to CT41 is a loose analogy only); frequency locking **PASS** on the aggregate statistic, but 3 of 7 worlds fail it individually. A holographic / fractal prediction (layers growing with the log of the scale range, at roughly equal value each) **FAILED** in-model at \(N=0.05\) (15 scale-free worlds; one layer took almost all the value); that construction does not test a spatial or high-dimensional MERA picture. An independent review of that run (`reviews/rhythm_2026-11-20/REVIEW.md`) is **SCORING CORRECT**; the official gates stand (`core/keystone_checks/RHYTHM_RESULTS.md`, `core/KEYSTONE_NOTE.md` §5). A predictive rhythm rule (K* from the poles and the stakes, without first computing the whole ε_K curve) remains **OPEN**. The formula as written also cannot return the K* = 0 that CT21 allows when stakes are small.

## 5. Load-bearing theorems (proved in-model)

| ID | Result |
|---|---|
| CT20, CT33 | A best design exists. With ruin slack, more at stake never means less spent on judgment. Reads can replace layers. |
| CT21 (L1–L3) | Layers ≤ the world's predictive degree. At most one layer for one real scale (K* ∈ {0, 1}). Layers beat one tracker iff R > R\*. |
| N60 | The keystone count, conditional on convexity, in Model S. |
| CT22, CT25 | Nothing survives below B_min; above B_slack the expected-cost rules are exact. Buffer grows as shock × τ^H. |
| CT14, CT16, CT35, CT36, CT28, CT34 | A shared layer pays once N > N\*(ρ). At equal read quality and with shared upkeep measured in local layers, a shared layer's worth falls as e^{−2ℓ/τ}, so fast scales go local and slow ones shared. Joint value can be superadditive. |
| CT37–CT40 (#115) | Robustness from cost plus the ruin cap (§6). |
| CT41–CT43 (#117) | Redesign cost, lineage objective, time average (§6). |
| CT23 | A wrong picture of the world costs second-order regret. |
| J16 | A missing cost on the closed list kills the theory. |
| THEORY §3, FRAMEWORK §9 | Field results count only after a recorded qualification check. |

## 6. Strands, each a reading of J

- **Robustness** (#115). Failure in 𝒟 buys copies (CT37; Kettelle 1962). Model uncertainty buys reserve above the fitted optimum (CT38; prediction-interval buffer, Gerrard & Tsanakas 2011, mainly CL18). Where ruin binds, the optimum has zero margin against risks outside the model (CT39). With redesign per regime, judgment's edge is convex in volatility, antifragile in Taleb & Douady's (2013) sense (CT40). Robust layer count is open (CX7).
- **Fractal change.** It enters only as the measured spectrum. The slope sets what each extra layer is worth; the stakes set where the count stops. "Fractal, period" is withdrawn (N46).
- **Head/tail breaks.** Tried as the fractal proxy, the ht-index under head/tail breaks 1.0 reads 1 on Gaussian records whatever the world, and tracks ln n on heavy tails (N58, N59; N61 math-corrected). Jiang (2016) treats that growth as intended. It remains a valid tool for heavy-tailed value data (Jiang 2013, 2019), but it does not count layers. The spectrum does, and a plug-in fit beats a plain pole count only at R ≤ 10³.
- **Records as agents** (N63). The idea that a record's hierarchy is the footprint of the sub-agents that wrote it. Open, with no support yet. The first #116 numbers were withdrawn as pseudo-replicated and at chance; the redo found that a record reports its world, not the agent's K, and an I/O fit reads a design, optimized or not.
- **Dynamics** (#117). J_R prices redesign: a lump cost gives an inaction band (CL19, Dixit 1991). A non-move is consistent only if the post-change gap g < Δ_R(k_lo); a miss if g > max(the static band, Δ_R(k_hi)); INDETERMINATE between; and if the predicted gap of a non-mover is ≤ Δ_R(k_hi), the move test is NOT A TEST (CT41). Shared shocks favour bet-hedging mixtures at the lineage (CT42; Cohen 1966). J is already the time average for additive or log-reserve stakes (CT43).
- **Evolution in silico** (EVO1, interim, #114). Evolution reached argmin J where small steps lead there (PC, W1, W2 passed) and stalled where a shared layer pays only jointly (W4, W4b failed). It cannot test bet-hedging: each genome carries one design.

## 7. Scorecard

Untested, not refuted. No system has yet been shown to qualify. The best candidate is E. coli; its σ, N_e and T_red are to be sourced before any rescoring. The 30 earlier field rows are NOT A TEST (10 passed and 20 failed on proxy). Every theorem has been refereed at most once, by one bot family. No human expert has read the theory.

## 8. Credit

The parts are known (Wiener–Kalman, Lundberg, Harris, Landauer, Samuelson, Coase, Topkis, Lynch, Kettelle, Dixit, Cohen, Jiang, Taleb & Douady; `litmap/`, THEORY §10). What is claimed as new is the package: one priced objective under a ruin cap, the measured world as its only input, and a kill rule across scales.
