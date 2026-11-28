# EXTENSIONS: the results at their limits, and what they imply for real systems

Written 15 Nov 2026; final revision 02:22 ET. Notation is from `AXIOMS.md`; theorem numbers are from `THEOREMS.md`. New numbers come from `checks/s10_extremes.py` / `.out`, and earlier ones from s1–s9.

**How to read the labels.**
- **DERIVED**: follows from the theorems inside the model 𝓜 (Axioms 1–8). For a real system it is **conditional on a mapping (M)**, stated in each row, of that system onto the axioms. The mapping is itself an untested hypothesis. A derived implication can fail in two ways: the mapping is wrong, or the system is not near-optimal (Axiom 7; see §3.0).
- **CONJECTURED**: a plausible consequence that needs a step not proved here, for example an unmodeled mechanism or a parameter value we cannot yet measure.
- **SPECULATIVE**: an analogy or extrapolation beyond the model.

Every row gives a concrete falsifier: a measurement and the result that would count against the implication.

---

## 1. The extremes (all inside 𝓜, all DERIVED)

### E1. N → ∞ (very large groups)
- **Onset is always passed when κ_b = 0.** The per-member cost of the level, φ(Nw, q_g)/N ∝ N^{a−1}, goes to 0, so for N > N\* the level is kept at any ρ > 0 (T1.1).
- **The saving saturates.** The fractional saving tends to 1 − (1+ρ)^{−b} ≤ bρ (Prop 10). Large groups gain a bounded share, never more than b times the shared fraction of drift.
- **With a broadcast cost the limit is a ρ threshold, not an N threshold.** If ρ ≤ ρ_b, no group is large enough (T2). Communication cost, not group size, then decides.
- **Vigilance diverges.** V(N) = V(N\*)·(N/N\*)^a (T5.5). Check: V(100N\*)/V(N\*) = 10.00 at a = ½ and 21.54 at a = ⅔ (s10 E5). The level watches ever harder in total, while its effort per unit of stakes falls as N^{a−1}.
- **Depth grows one-for-one with log N in the top-down regime** (first order, h = 0, κ < κ\*).
  - Proof: by T7(c), scale s is kept iff n_s^{(1−b)(κ\*−κ)} > C(R). The member residual R is the sum of the untracked small scales and does not depend on how many large scales exist. So the kept set is {s ≥ s_min} with s_min fixed, and depth = S − s_min + 1.
  - Check: in a binary tree, depth rose by exactly 4 for every 4 added scales at κ = 0.3 and κ = 0.7 (s10 E1).
  - For κ > κ\* the kept set does not grow with N.
  - Logarithmic depth in hierarchy models is standard in kind (Williamson 1967; Beckmann 1977 [from memory, not verified this session]). What is new here is the **condition κ < κ\* = 1/|e_g|**, which makes depth's growth with log N conditional on how sharing decays with scope.

### E2. ρ → 1 and ρ → ∞ (shared drift as large as, or larger than, private)
- **At ρ = 1, N\* = (2^b − 1)^{−1/(1−a)}.** That gives 5.83 at a = b = ½, 56.9 at (⅔, ⅓) and 13,755 at (0.8, 0.2) (s10 E2). Averaging technologies need far larger groups even when half the drift is shared.
- **As ρ → ∞, N\* → 1⁺.** Pairs pool: N\*(10⁶) = 1.002, 1.031 and 1.385 for the same classes. The −(1−b)/(1−a) law is a small-share law. At large ρ, e_g → 0 (h = 0) or ≈ −γ (large upkeep, T1.5).
- **Opposite effects hold at every ρ** (T3), so the signs of ∂N\*/∂q_g and ∂N\*/∂q_u never flip at extreme ρ.

### E3. Total drift → 0 and → ∞ (a calm or a violent world, ρ fixed)
- **h = 0:** onset does not depend on total drift (T1.7).
- **h > 0, drift → 0:** levels dissolve. G = λ^bG₀(N) − h, so **N\* ∝ λ^{−b}**. Local slopes in s10 E3 were −0.415, −0.452, −0.473 and −0.485 → −½. Before that, single items cross the **freeze edge** q ≤ q_f (T8.1): a calm world is held in frozen copies, not tracked.
- **Drift → ∞ with a bounded fallback (lookup cost u):** holding stops at q_c (T8.2). Effort drops off a **cliff** (T8.5). Levels whose saving relied on members holding the item lose that saving (T6 counterexample), while a **shared store survives up to an N^{(1−a)/b}-times-faster drift** (T8.6; N² in R1 quadratic).
- **Drift → ∞ with no fallback:** effort rises without bound (no cliff), and survival needs the inflow floors of the repo's T1/INTERNAL_MODEL (KNOWN).

### E4. Lookup cost u → 0 (the AI limit). The order of dissolution depends on lookup granularity.
This item corrects a conjecture in my own working notes ("private holding goes first, then levels"). The calculation says otherwise (s10 E4; FIXES F14).
- **Whole-item lookup** (a member can fetch its whole x_i, but not the shared part alone). As u falls:
  1. **The pooled-tracking level dissolves first.** Once μu is below the flat holding cost, the level must beat N·μu, not N·φ_flat. It needs N[μu − φ(w, q_u) − h] > φ_L + h, which fails **before** μu reaches the member's residual holding cost.
  2. **Private holding stops** once μu < φ(w, q_u) + h.
  3. In s10 E4 (N = 50, ρ = 0.1, h = 0.05, c = w = μ = 1), solving the conditions exactly: the level goes at u ≈ 1.53, private holding at u ≈ 1.46, and a shared store of a fully common item at u ≈ 0.20. The first two are close here because ρ is small. The order, not the gap, is the theorem.
- **Component lookup** (the shared part can be fetched from a store). Then the level *is* the shared store. It survives until N·μu < φ_L + h: **N^{1−a} times lower u** than a private holder of the same item, an N² wider drift band in R1 quadratic (T8.4).
- **The lookup provider is itself a level.** Its N is every user of the store, across organizations. By T1 it is far past onset, and by T5.5 its vigilance grows as N_users^a. In 𝓜, **cheap lookup does not abolish tracking. It moves tracking from many small levels into a few very large shared stores.**
- **u → 0 exactly:** nothing is held privately, and all tracking effort sits in whoever maintains the store. If no one is rewarded for maintaining it, 𝓜 says nothing: that is the commons problem (THEORY §6), outside these axioms.

### E5. Other limits
- **p_g/p → 0 (cheap central sensing):** N\* ∝ p_g/p → 0 at first order (T1.6), so levels form in small groups. Vigilance at onset is unchanged (T5.4). Vigilance at fixed N rises as (p/p_g)^a.
- **a → 1 (no concavity in stakes):** no level at any N (T1 counterexample).
- **b → 1:** e_u → 0, so private drift stops mattering (T1 counterexample).
- **θ → ∞ in A_θ:** e_g = −(1+θ) → −∞, and onset becomes extremely sensitive to the shared share.
- **ε → 0 (perfect selection):** Prop 10's floor ρ_min ≈ ε/b vanishes. With coarse selection (ε = 5%, b = ½), no level ever forms below ρ ≈ 0.108.
- **Broadcast t = c_b/c → 1:** ρ_b = 4t/(1−t)² → ∞. If pushing one update to each member costs as much as a read, a level never pays (T2b).

---

## 2. What fixes the class: the one measurement every substrate needs first

Most implications below depend on the **sensing class**, i.e. on (a, b):
- R1, periodic complete reads: a = b = ½.
- R2, information-rate priced: a = b = ½.
- A_θ, precision-priced averaging: a = 2θ/(1+2θ), b = a/2.

By T1.8 and T7(b), the **level's** class sets e_g and κ\*. **The class can be measured without measuring onset**, so the theory is not circular here:
- **The drift elasticity of sensing effort** (read rate, information rate or precision) for a lone unit equals b (Lemma 1(viii)): ½ in R and ⅓ in A₁.
- **The stakes elasticity** equals a: ½ in R and ⅔ in A₁.
- **Whether a = b** is a test of drift-invariant pricing (Lemma 1(ix)).

**Caveat (from SENSING).** Measured learner elasticities can miss the oracle values. Class R's learner gave e_g = −0.920 against the oracle's −0.991 (MISS). Class A passed (−1.970), and A2 passed (−1.483). So a measured (a, b) carries estimator bias that must be bounded before it is used to predict an exponent.

---

## 3. Implications by substrate

### 3.0 Scope that applies to every row
- **Axiom 7 (near-optimal selection).** Expect fits only under strong selection, and fix the classification **before** a test (THEORY §7). A miss under weak selection is weak evidence against the theory.
- **Not modeled:** strategic members and free-riding, endogenous drift reduction (THEORY §5), and non-Gaussian bundled losses with α-stable drift (T4, open).
- **"Level"** always means *a tracker of a shared driver whose estimate members use*. It does not mean an authority structure. Whether trackers coincide with bosses is a separate empirical question.

### 3.1 Cells
| # | Implication | Label | Mapping (M) | Falsifier |
|---|---|---|---|---|
| C1 | If receptor cost is per binding event (precision linear in spend, A₁), shared sensing such as a pooled signal or quorum-type sensing has **e_g = −2**. Onset density ∝ ρ^{−2}, against ρ^{−1} if the binding cost is information-rate priced (R2, the thermodynamic floor, THEORY §2.3). | DERIVED (given M) | M: cost is per molecule counted (Berg–Purcell-type counting; Berg & Purcell 1977 [from memory, not verified]); errors bundled; near-optimal. | Measure first the drift elasticity of receptor expression: ⅓ means A₁, ½ means R. Then, across conditions, the slope of ln(onset density) on ln(ρ) should be −2 for A₁ (or −1 for R). A measured class with the other slope falsifies C1. |
| C2 | Pathways using averaging sensing build **bottom-up** cascades when sharing decays faster than n^{−½} (κ\* = ½ for A₁). Reset-type sensing would need decay faster than n^{−1}. | DERIVED (given M) | M as C1, plus a nested sharing structure with exponent κ. | Find cases with κ between ½ and 1. A₁ predicts bottom-up and R predicts top-down. The opposite ordering falsifies. |
| C3 | Shared sensors are born **far more vigilant** than private ones when ρ is small: V ∝ ρ^{−1} in A₁, against V ≈ 2 in R. | DERIVED (given M) | M as C1. | At onset, effort per shared sensor ÷ effort per private sensor should rise as the shared share falls (A₁). If it is flat while the class is measured as A₁, C3 is falsified. |

### 3.2 Immune systems
| # | Implication | Label | Mapping (M) | Falsifier |
|---|---|---|---|---|
| I1 | **Freeze / hold / look up by antigenic drift.** Slow-drifting pathogens get frozen memory (lifelong), intermediate ones get maintained memory (boosting, turnover), and fast ones get none: each encounter is a fresh primary response, a "lookup" at cost u. The transition at q_c is a **cliff**, not a graded decline (T8.5). | DERIVED (given M) | M: memory upkeep h; the primary response is a bounded fallback cost u; antigenic drift q is measurable (e.g. antigenic-cartography distance per year). | Across pathogens, memory investment against drift rate should be **bimodal with a gap**. A smooth monotone decline through the top drift decile falsifies I1. Prior data caution: BIO1 found immune lifetime did not track drift as first read, and COLLAPSE1 traced that to a half-life measurement artifact. MATCH1's measles freeze-or-hold passed, with caveats. |
| I2 | Responses to conserved, shared epitopes act as levels. They should be favored when the conserved share ρ of antigenic variation is larger, with opposite effects of conserved and variable drift (T3). | CONJECTURED | Requires that "level" = a cross-reactive clone population and ρ = conserved share; the mapping of cost to (a, b) is unmeasured. | Across pathogen families, the share of cross-reactive memory should rise with the conserved share of variation. A null or negative relation falsifies I2. |
| I3 | Herd-level shared memory (population immunity) as a shared store whose band is N² wider than an individual's. | SPECULATIVE | No maintenance cost structure is identified. | None offered until the mapping is specified, so this is not counted as a prediction. |

### 3.3 Ant colonies
| # | Implication | Label | Mapping (M) | Falsifier |
|---|---|---|---|---|
| A1 | **Trail onset threshold.** The colony size at which trail (shared-store) foraging appears scales as **N\* ∝ 1/ρ** in the upkeep regime, if trail maintenance (evaporation, deposition) is upkeep h and the trail is R-type. Here ρ is the shared drift of food location over individual noise. | DERIVED (given M) | M: pheromone upkeep = h; a = b. Beekman et al. 2001 (trails above ≈ 600 Pharaoh's ants [as cited in THEORY.md]) shows a threshold exists, not its slope. | Across species or experimental food-patch persistence, a log–log slope of threshold N against ρ with a CI excluding −1 falsifies A1. If the threshold moves with ρ but not N (a fixed ρ cut), that indicates the broadcast break (T2) instead. |
| A2 | **√N fade of a shared trail** (repo T4) holds for averaging readouts. The **error** scaling, not the fade scaling, diagnoses independent pooling. | DERIVED and **partly tested in simulation** | ANTS1 (stochastic ant model, analysis finished 15 Nov 01:54 ET, *not yet written up by its executor*). | ANTS1 raw counts from `tests/ANTS1/analysis_output.txt`: P1 (fade exponent in [0.3, 0.7]) 10/10; P2 pass (large-gain exponent 0.205 and 0.154 < 0.3; Spearman −0.593); **P3 (MSE slope band) 5/10, failed for the MODE readout**; P4(a) 39/41 and P4(b) 54/54 (followers have the same fade but ≈ 4× the error, so the fade alone does not diagnose pooling); P5(a,b) pass; **P5(c) 36/96 fail**; **P6 154/180 (86%) fail** against the 90% bar; P7 75/75; P8 24/24. In the field, a fade rate that rises as √N while error does not fall as N^{−½} means non-independent deposits. |
| A3 | **Opposite effects:** more individual navigation noise (private drift) *raises* the colony size needed for trails, and more shared food-location change *lowers* it (T3). | DERIVED (given M) | M as A1. | Experimentally raise individual noise (e.g. by disturbing visual cues) at fixed patch dynamics. A drop in the trail threshold falsifies A3. |

### 3.4 People (individual cognition and small groups)
| # | Implication | Label | Mapping (M) | Falsifier |
|---|---|---|---|---|
| P1 | If attention is priced per bit (rational inattention, entropy cost, R2; Sims 2003 [as cited in THEORY.md]), then a = b = ½: **e_g = −1**, a newly designated group monitor is ≈ **2× as vigilant** as a member at birth, and this does not depend on how much cheaper or dearer the monitor's attention is (T5.4). | DERIVED (given M) | M: R2 pricing, bundled loss, near-optimal (weak selection in many settings; see §3.0). | In team experiments that vary the shared share ρ of task drift, the team size at which groups spontaneously designate a tracker should scale as ρ^{−1}, and monitor/member effort at that point ≈ 2. A ratio that tracks the monitor's relative cost falsifies the price invariance. |
| P2 | **Offloading by drift (the "Google effect" in 𝓜).** As lookup gets cheaper, people stop holding fast-changing facts first: q_c ∝ u^{1/b} (T8.6). Holding effort for an item class falls **discontinuously**. | DERIVED (given M). Qualitative offloading is KNOWN (Sparrow et al. 2011; Risko & Gilbert 2016 [as cited in THEOREMS]) | M: recall cost = hold; search = lookup u. | Recall effort for item classes ranked by drift, before and after a drop in search cost. If slow-drifting items are dropped first, or the decline is smooth, P2 is falsified. |
| P3 | **Forgetting exponent = need exponent** (the strong spectrum claim). | **KILLED twice** | MATCH1 A1 (memory 0.24 vs need 0.71); P1 Meeter conditional logit a_c = 0.310 < 0.35, locked KILL (`theory-v3/prereg/P1_RESULT.md`, 15 Nov 01:56 ET; CI unavailable). | — |

### 3.5 Firms
| # | Implication | Label | Mapping (M) | Falsifier |
|---|---|---|---|---|
| F1 | **Periodic reporting (R1) gives e_g = −1 and Π\* = 4** (or ≈ 7.3 under the subtract readability scheme, Prop 11). A central tracking function such as an HQ economics unit, central planning or a shared-services monitor appears at unit count N\* ≈ Π\*/ρ. | DERIVED (given M) | M: reviews are complete reads at fixed cost; units read their own residual. | Across multi-unit firms, the log–log slope of the unit count at which a central tracking function appears, against the common share of unit-level variance, with a CI excluding −1, falsifies F1. |
| F2 | **Opposite effects:** common shocks centralize tracking and idiosyncratic shocks decentralize it, at every ρ (T3). | DERIVED (given M); known in kind in organizational economics (e.g. Alonso, Dessein & Matouschek 2008 [from memory, not verified]) | M as F1. | Within firms over time, a rise in the idiosyncratic variance share followed by *more* central tracking falsifies F2. |
| F3 | **Total volatility promotes levels when upkeep is non-zero** (T1.7). At fixed ρ, more volatile industries centralize tracking at *smaller* unit counts. This is opposite to the common contingency reading that volatile environments favor decentralized, organic structure. | DERIVED (given M) | M as F1, plus a fixed upkeep h for a central function. | Hold ρ fixed and compare industries by total volatility. A higher N\* in more volatile industries falsifies F3. |
| F4 | **Vigilance:** a new central tracker spends ≈ 2× a unit's monitoring effort at birth, and the ratio grows as N^{½} as the firm grows (T5). | DERIVED (given M); **partially tested** | VIGIL (PIAAC survey, 15 Nov ≈01:41 ET): P1 direction ratio 1.14 (1.05–1.23) PASS, replication 1.19; P2 specificity fragile (post hoc 1.06, 0.98–1.16); P3 √span slope 0.036 against 0.5, **NOT PASSED**; P4 size ≈ 1.15, **not consistent with ≈ 2**. | The direction holds. The size (≈ 1.15 against ≈ 2) and the growth law (≈ 0 against 0.5) miss. Either the mapping fails (self-reported reading frequency is not tracking effort; span is not N) or T5 does not apply to supervisors. Status: **direction supported; size and growth leaning against**. In class R, upkeep and prices cannot rescue the size: at γ = ½ and small ρ, **V(N\*) = 1 + √(1 + 2h′/r) ≥ 2** for every upkeep and price ratio r = p_g/p (T5.6), and beyond onset V is larger still. So 1.15 needs a < b (T5.2), heavy measurement attenuation, or a mapping failure. As a test of T5 in firms this is **a miss on size**. |
| F5 | **AI lowers lookup cost (u ↓).** With whole-item lookup, middle relay levels (people whose job is to keep a pooled estimate that members hold) dissolve **before** members stop holding private knowledge (E4). With component lookup, the shared store survives, grows in N and in vigilance, and moves to the provider. | DERIVED in 𝓜 (E4); CONJECTURED as a description of real firms | M: relay levels exist for pooled tracking, not authority; AI = lower u. | Firms adopting retrieval tools. If middle information-relay roles shrink *after* frontline private expertise erodes (not before), or central knowledge stores shrink, F5 is falsified. |

### 3.6 Cities
| # | Implication | Label | Mapping (M) | Falsifier |
|---|---|---|---|---|
| Y1 | A city-wide tracker of a shared driver spends ∝ N^a (√N in R) at fixed per-capita drift, i.e. **sublinear** shared-monitoring spend. | DERIVED (given M) | M: R1 statistics offices; per-capita drift fixed as N varies (strong: larger cities may have larger q_g). | Central monitoring spend that scales linearly or superlinearly with population, *after* controlling for measured shared drift, falsifies Y1. Caution: THEORY §2.4 notes total city administration ≈ N^{1.0}, which mixes tracking with service delivery and does not test Y1. |
| Y2 | Where demand drift is scale-free (DRIFT1: 311 request rates log-uniform over 2.5–4 decades), service tiers are geometrically spaced (repo T7b, layers ∝ (log-span)^{2/3}). | DERIVED "if" direction (Roundy-type); the count is **inconclusive** (MATCH1 C1) | M: one service tier per memory timescale. | Equal-linear tier spacing in scale-free categories, or a flat tier count as span grows, falsifies Y2. |
| Y3 | **Depth ∝ log N** (E1) for administrative nesting (city, borough, district) when sharing decays slower than n^{−κ\*}. | CONJECTURED (mapping of κ unmeasured) | M: administrative tiers are tracking levels. | Measure κ from the variance decomposition of service demand by spatial scale. If κ < κ\* yet depth does not rise with log N across cities, Y3 is falsified. |

### 3.7 AI systems (agents and their tools)
| # | Implication | Label | Mapping (M) | Falsifier |
|---|---|---|---|---|
| AI1 | Multi-agent systems with a shared memory (a vector store, scratchpad or knowledge base) should adopt it exactly when N > N\*(ρ). Here ρ is the shared drift of the task environment over per-agent drift. N\* ∝ 1/ρ for periodic refresh. | DERIVED (given M); **testable cheaply in simulation or with real agents** | M: refresh = R1 read; agent context = private tracker. | Benchmark: vary ρ and N, let an optimizer choose shared memory or not, and fit the onset slope. A CI excluding −1 falsifies AI1 for R-type refresh. Caution: POOLSIM showed the kill rules did not fire, but that test was partly circular (the learners minimized the same cost). A non-circular test needs agents that are *not* given the cost function. |
| AI2 | **Lookup → 0 concentrates tracking.** Private caches go first; local pooled levels go even earlier with whole-item lookup; global shared stores survive N^{1−a}-fold lower u and are maximally vigilant (E4, T5.5). | DERIVED in 𝓜; CONJECTURED for the industry | M: model/retrieval providers = shared stores across organizations. | If the cost of retrieval falls and per-organization knowledge maintenance *rises* relative to provider-side maintenance, AI2 is falsified. |
| AI3 | **Cheap central sensing (p_g ↓ faster than p) centralizes tracking at small N** (T1.6). If AI cuts members' costs as much as the center's, the onset does not move. | DERIVED (given M) | M: AI changes the price ratio p_g/p. | Where AI tools cut only frontline costs (p ↓), increased centralization of tracking falsifies AI3. |
| AI4 | The theory as a whole describes "judgment" in machines, i.e. what any agent must pay to stay calibrated. | SPECULATIVE | The X-post "Judgment" framing. The free-energy identity version is **killed** (CLAIM_MAP). | — |

---

## 4. What remains unmapped or open (stated, not hidden)
1. **Bundled loss with α-stable drift** (no Gaussian closure): the exponent is not derived (T4).
2. **Strategic members.** Every result assumes a planner or selection on the whole. Free-riding on shared stores (THEORY §6) can undo onset in real commons. Not modeled.
3. **Endogenous drift** (THEORY §5): if levels reduce q_g, the onset equation has feedback. Not modeled.
4. **Readability:** Prop 11 is numerical, and vigilance under the subtract scheme is not derived.
5. **The class of every real substrate is unmeasured.** The single most valuable next measurement is the lone-unit drift elasticity of sensing effort (½ for R against ⅓ for A₁) in any one substrate where onset can also be observed.
6. **The mapping from the temporal spectrum to forgetting exponents** (THEORY §2.4, MATCH1 D3 opposite sign) is not touched by this formal layer and remains the largest gap in the spectrum hypothesis.
