# MATH_ATTACK: A Theory of Adaptive Organization, attacked as physics

Written Sat 2026-11-14, about 10:15 PM to midnight ET, by a Grok Bot executor, for Chad, via Ace. **Not independently reviewed.** The author is from the same bot family as the people who wrote the theorems, so treat this as a second reader, not a blind grader.

**Sources read for this pass:**
- `X_TEXT.txt` (v9)
- `public-repo/theorems/THEOREMS.md`
- `public-repo/README.md`
- `REAUDIT_2026-11-13.md`
- `tests/C3/RESULTS.md` and `PREREG.md`
- `tests/TESTC_STAGE3_REVIEW.md`
- The toy-reversal notes in `longform/HYPOTHESES_CORE_v2_reviewed.md` and `v2/TEMPERATURE_MEASURE.md`
- The first part of `tests/C3b/PREREG.md`

**What was not done.** Nothing was posted or sent. The public repo, the Looper README and C3b were not edited.

**Checks.** Every NUMERIC or PROOF step that can be computed is checked in `checks/`. `run_all.sh` regenerates every `*.out` file; it needs numpy 2.5, scipy 1.18 and sympy 1.14, which live in a venv at `../.venv`. The C3 diagnostics read **only predictor columns** (σ, mean inflow, B, τ), never outcomes.

**Labels.**
- **KNOWN:** prior work, with each citation checked by web search this pass.
- **PROOF:** a derivation given here, with its stated assumptions.
- **NUMERIC:** a script result.
- **CONJECTURE:** not shown.

---

## 0. Bottom line

1. **One objective works.** The objective is upkeep + prediction-error loss + lateness + Λ·(failure hazard). It yields rules 2, 3, 5 and the stakes and drift parts of rule 7 as theorems. Rule 1 and the first clause of rule 4 hold only as near-tautologies. The rest of rules 1 and 4, rule 6's mechanism and "same mechanism at every level" **do not follow** (§1.4).
2. **New result: the physics floor has exactly the economic form (PROOF, conditional).** The minimal heat cost of tracking a random walk to error D is kT·σ²/(2D). That follows from the Barato–Hartich–Seifert learning-rate bound plus a Gaussian information-loss calculation. Adding quadratic loss gives total cost σ√(2kT·w), which is **exactly EOQ's σ√(2cw) with c = kT per nat**. So the "currency swap" is exact in form. The honest caveat is that dimensional analysis forces the form, so this is not evidence of a common cause (§1.2).
3. **New result: the temperature is forced by dimensions, and that gives a universal identity (PROOF).**
   - Inputs: buffer B, diffusive shock σ, one fix time scale τ.
   - The hazard must be h = F(z)/τ with z = B/(σ√τ). This holds for *any* fix mechanism.
   - Hence the elasticities obey **ε_B = −ε_σ** and **ε_τ = ε_σ/2 − 1**.
   - C3's preregistered ratio r_τ = ½ is only the z → ∞ limit (or the "discrete incident" regime). In general r_τ = ½ − 1/ε_σ, which is 0 in the hot regime.
4. **Exact failure laws (KNOWN/PROOF/NUMERIC).** The tail shape depends on *how* fixing works:
   - fixed delay: erfc-type, e^{−z²/2};
   - proportional restoring (OU/Kramers): e^{−z²};
   - fixing at a Poisson rate (Evans–Majumdar resetting): e^{−√2·z}, a fat exponential tail;
   - heavy-tailed fix times: a power law in z (leading order).

   These four cases are universality classes set by the fix mechanism, not by scale.
5. **C3's τ null is what the theory itself predicts, given how C3 measured (PROOF + diagnostics).**
   - The data fit β_σ = 0.28. In every two-sided model, ε_σ ≥ 2, which implies strong attenuation.
   - With proportional attenuation, the theory predicts β_τ in [0, 0.14). C3's CI [−0.09, 0.10] covers almost all of that range.
   - C3's B is a flow, not a stock, so z was undefined.
   - 55% of repos have Fano < 2, so σ was mostly counting noise.
   - So C3 could not have seen τ even if the term is true. That makes it uninformative, not a refutation.
6. **The toy's "reversal" was partly an artifact.** Per-window counting is wrong; the exact renewal hazard moves the crossing from 0.31 to about 0.38. The remainder is real only when fixing also erases *favourable* deviations. Reversal happens **iff ε_σ < 2**.
7. **Where τ must show up:** exogenous τ, B a stock in shock units, light-tailed shocks, and the **cold** regime z ≳ 1.5. There ε_τ is about 0.35–7 and the τ×z interaction is **positive**. In relative terms τ matters *most where shocks are small relative to buffers*.
8. **Scale invariance is half proved and half broken (§3).**
   - **Holds:** the shock part closes under coarse-graining (CLT and stable laws).
   - **Pooling cools:** z' = z·√(N/(1+(N−1)ρ)), with a ceiling z/√ρ set by correlated shocks.
   - **Weakest link heats:** z' ≈ √(z² − ln N).
   - **Breaks:**
     - heterogeneous fix speeds aggregate to long memory (Granger), and a single-τ fit mispredicts failure by 1.4–2.4× (NUMERIC);
     - the "representative agent" exists only under a Gorman-type condition, otherwise with an **unbounded** penalty;
     - parts do not internalize the whole's failure cost.
   - **Reading:** the strong claim ("a population obeying the objective is an agent obeying the same objective") is **false in general**. The conditional claim is a theorem with four explicit conditions.
9. **Red team.** None of the five objections is fatal to the conditional theory. Objection 5 is fatal to the unconditional "same at every scale". Objection 1 (the forms are forced) demotes the cross-domain recurrence evidence to near zero.
10. **Decisive tests:**
    - banks (firm scale; FFIEC + FDIC failures; competitor Boyd–Graham Z);
    - human glucose regulation (organism scale; ShanghaiT1DM/T2DM CGM; competitor static LBGI/SD);
    - animal populations (population scale; GPDD; competitor Dennis et al. density-independent diffusion).

    Each has a sign that its competitor gets differently (§5).

---

## 1. One objective (Task 1)

### 1.1 Setting and objective [definitions]

A self-maintaining unit has:
- a buffer B, a stock it can draw down;
- a deviation X_t driven by shocks (diffusive scale σ, possibly jumps);
- a fix process with time scale τ(π) that returns X toward its set point. τ includes detection delay, so it depends on the watching policy π.

It also holds a memory of facts x_i(t), each drifting at variance rate σ_i². Each fact is used at rate μ_i, with stakes w_i per unit squared error, and is checked at rate f_i for cost c_i per check, with upkeep h_i per held fact.

Policy π = {which facts to hold (M), check rates f_i, update gains K_i, an interrupt rule, the fix and watch effort}. The objective is a cost rate:

  **J(π) = Σ_{i∈M} (h_i + c_i f_i) + Σ_i μ_i E[ℓ_i(x_i − m_i)] + E[L(lateness of actions)] + Λ · h_fail(σ, B, τ(π))**

The four terms are upkeep, prediction-error loss, the cost of acting late, and the cost of losing the unit: Λ is the value of continued existence and h_fail the hazard of buffer exhaustion.

**Physics floor on the first term.** For a physical system, upkeep per unit time is at least kT times the rate of information it must acquire (§1.2). Still et al. 2012 add kT·(I_mem − I_pred) per step as the dissipation cost of memory that does not predict. In other currencies, c is the cost per check or per nat, and nothing physical fixes it.

### 1.2 Result O1: the thermodynamic floor of tracking has the EOQ form [PROOF, conditional on KNOWN bounds]

- **KNOWN.** A sensor's learning rate (the rate at which it reduces uncertainty about an external process that it does not affect) is bounded by its entropy production: l ≤ σ_y (Barato, Hartich & Seifert 2014, New J. Phys. 16, 103024).
- **PROOF.** Hold an estimate with error variance D of a random walk with variance rate σ². With the estimate fixed, drift destroys information at rate σ²/(2D) nats per unit time: ½·ln((Var x + σ²dt)/(D + σ²dt)) − ½·ln(Var x/D) → −σ²dt/(2D). Holding D steady therefore needs a learning rate ≥ σ²/(2D), hence dissipation ≥ kT·σ²/(2D).
  - *Cross-check:* for the Kalman–Bucy filter, Duncan's (1970) theorem gives an information rate P/(2r) = σ/(2√r), equal to σ²/(2P) with P = σ√r (`objective_checks.out` §1).
- **Combine with quadratic loss.** J = kT·σ²/(2D) + w·D gives D\* = σ√(kT/(2w)) and **J\* = σ√(2kT·w)**. EOQ (THEOREMS T1a) gives J\* = σ√(2cw) with mean error σ√(c/(2w)). **Both are identical under c = kT per nat** (sympy-checked).
  - Berger's (1970, IEEE Trans. Inf. Theory 16(2)) non-causal rate floor gives a looser bound, 2/π of this.
- **What it licenses.**
  - At cell scale, the economic tracking optimum and the physical one sit on the same curve. The ratio c_eff/kT is a measurable "efficiency gap" at each scale (cells may be near it, per Lan et al. 2012, Nat. Phys. 8:422; for firms and cities the ratio has no measured value, and the 10¹² once quoted here had no derivation and is withdrawn).
  - This makes "only the currency changes" a precise statement: replace kT by the cost per nat acquired.
- **What it does not license.**
  - With one cost scale, one drift σ² and one quadratic stake, dimensional analysis forces any optimum to be ∝ σ√(cw). The form match is guaranteed; only the √2 prefactor match is a (minor) coincidence.
  - The bound also inherits the no-feedback condition (the signal is unaffected by the system). Systems that act on their world need Horowitz & Esposito 2014 (PRX 4, 031015) or Sagawa–Ueda.

### 1.3 Which rules follow

| Rule (post v9) | Derivation from J | Status |
|---|---|---|
| 1. Return early; interrupt iff stake×P(relevant) + learning value > cost | One-step expected-value comparison of J with and without the interrupt (value of information, Howard 1966, IEEE TSSC 2:22). "A late prediction buys nothing" holds by definition once L puts zero value after the window. "Untried guesses can't teach" holds because the information term is positive only if the outcome is observed. | PROOF, near-tautological; the size of the learning term needs a learning model that J does not supply |
| 2. Keep while need×miss > upkeep; upkeep rises with drift; let it fade | Hold iff σ√(2cw) + h < μ·u, where u is the cost of the fallback (re-read or fade) per use. The held cost rises ∝ σ (T1a, T5b). | PROOF (T1a/T5b) |
| 2'. "...fade *recoverably*" | Needs an option value for recovery, which J does not contain | does NOT follow |
| 3. Move a belief by the signal's relative reliability | Minimizing E[e²] gives the Kalman gain K = P/(P + r); a trusted source has r → 0, so K → 1 | KNOWN (Kalman/Muth) |
| 4. Keep prior versions while P(needed)×loss > keeping cost; frozen history ≈ free | Rule 2 with σ = 0: the drift term vanishes and only storage cost remains | PROOF (trivial) |
| 4'. "A wrong overwrite usually costs more than keeping" | An empirical claim about loss sizes | does NOT follow |
| 5. Copy error grows with hops and with drift; recheck when too big | E[e²] = σ²·Σ_k T_k/2 + n·r_copy. Linear in hops and in σ² (MC within 1%, `objective_checks.out` §2). Recheck when w·E[e²] > c. | PROOF + NUMERIC |
| 6. Record used/ignored/late outcomes | μ_i, w_i and P(relevant) appear in J, and they cannot be identified from the system's own predictions without outcome data. Beliefs can be self-confirming on the path (Fudenberg & Levine 1993, Econometrica 61:523). Test C's self-confirming meso layer (N2) is an instance. | PROOF-sketch + KNOWN |
| 6'. Hebb / trails / "no one in charge" / same mechanism at every level | J says *what* must be estimated, not *by what mechanism*. T4 (√N evaporation) holds only after assuming the trail mechanism. §3.5 shows decentralized parts **under-watch** unless the whole's failure cost is internalized. | does NOT follow; partly contradicted |
| 7a. Watch more as stakes rise | f\* = 1/T\* = σ√(w/(2c)), which rises with w | PROOF |
| 7b. With drift: rise, then fall to none | Bounded loss or any bounded fallback (T5, T5b; Cho & Garcia-Molina 2003) | PROOF |
| 7c. Watch most where shock/buffer is large but not overwhelming | Watching shortens τ. The value of a faster fix is −∂h/∂ln τ = h·ε_τ = F(z)ε_τ(z)/τ. It has an **interior peak only for fixed-delay fixing** (z ≈ 1.3, i.e. σ√τ/B ≈ 0.77). For rate-type or proportional fixing it **saturates at the hot end** (1/6 and 1/3 of 1/τ). With any finite horizon or discount ρ, every model peaks where h ≈ ρ (hτ ≈ 0.02–0.03 at ρτ = 0.05; `objective_checks.out` §3). | PROOF in two cases; FAILS otherwise |

### 1.4 What does NOT follow, plainly
- The **mechanism** in rule 6 (Hebb, trails, leaderless reinforcement) and the hypothesis "same mechanism at every level".
- "Recoverably" in rule 2.
- The empirical "wrong overwrite costs more" in rule 4.
- The **size** of the learning value in rule 1.
- Rule 7c without fixed-delay fixing or a finite horizon.
- Nothing in J implies nesting, fractality or phase-locking. Those are about the world's structure (T3, T7) or are untested (T9).

---

## 2. The temperature (Task 2)

### 2.1 Dimensional theorem and identity [PROOF]

**Setting.** Diffusive shocks accumulate in X with variance σ²t. Failure happens when the buffer B is exhausted. Fixing has a single time scale τ, and there are no other time scales.

**Theorem.** B²/σ² and τ are the only time scales, so by Buckingham-π

  **h = F(z)/τ, with z = B/(σ√τ)**

for *any* fix mechanism. Write ε_y = ∂ln h/∂ln y. Then:

  **ε_σ = −z F'(z)/F(z), ε_B = −ε_σ, ε_τ = −1 + ε_σ/2.**

So r_B = ε_B/ε_σ = −1 exactly, and r_τ = ½ − 1/ε_σ. Finite differences on all three models below reproduce this to 8·10⁻⁸ (`fpt_checks.out` §1).

**Corollaries.**
- (a) Slow fixing raises the hazard (ε_τ > 0) **iff ε_σ > 2**.
- (b) If failure is diffusion-limited at small z (h → const·σ²/B², which holds in all two-sided models here), then ε_σ → 2 and ε_τ → 0. In the hot regime, τ is invisible because the unit fails before any fix arrives.
- (c) **At a fixed level spread** (the stationary SD of an OU process, s = σ√(τ/2), held fixed), z is fixed, so **ε_τ = −1 exactly**. Slower correctors with the same spread fail *less* often per unit time, because they make fewer excursions.
  - A static index (Z-score, LBGI, coefficient of variation) predicts 0.
  - This sign is model-free given one τ. It is used in §5.
- (d) **A second time scale changes the identity.** Suppose shocks arrive as discrete incidents at rate λ ≪ 1/τ, each opening a fix window. Then h = λP(z), giving ε_τ = ε_σ/2 and r_τ = ½ exactly. C3's prereg value ½ is this incident regime (or z → ∞).

### 2.2 Exact laws for three fix mechanisms (two-sided |X| ≥ B, start at the set point)

| Fix mechanism | MFPT / hazard | Large-z tail | Status |
|---|---|---|---|
| A: fixed delay (full reset every τ) | h·τ = P_w / ∫₀¹S, where S is the series survival in a strip. Per window, P_w → 2·erfc(z/√2). One-sided case: P_w = 2Φ(−z) = erfc(z/√2) (reflection principle). | e^{−z²/2} | KNOWN (reflection, strip series) + NUMERIC |
| B: fix at Poisson rate 1/τ | MFPT = τ(cosh(√2·z) − 1), so h·τ = 1/(cosh√2z − 1). One-sided case: τ(e^{√2 z} − 1) (Evans & Majumdar 2011, PRL 106:160601). | 2e^{−√2 z} | KNOWN (one-sided) / PROOF (two-sided, via the renewal formula with q̃₀(s) = (1 − sech(B√(s/D)))/s) + NUMERIC |
| C: proportional restoring (OU, rate 1/τ) | MFPT = 2τ∫₀^z e^{v²}∫₀^v e^{−u²} du dv | (2z/√π)·e^{−z²} | KNOWN (Kramers 1940, Physica 7:284; Foley 1994 in ecology) + NUMERIC |

- **Monte Carlo agreement.** The Brownian-bridge-corrected MC matches all nine checks within 0.4–2.5% (`fpt_checks.out` §3).
- **Elasticity values.**

| z | A: ε_σ / ε_τ | B: ε_σ / ε_τ | C: ε_σ / ε_τ |
|---|---|---|---|
| 0.5 | 2.02 / 0.01 | 2.08 / 0.04 | 2.18 / 0.09 |
| 1 | 2.39 / 0.20 | 2.32 / 0.16 | 2.81 / 0.41 |
| 2 | 4.89 / 1.44 | 3.18 / 0.59 | 7.02 / 2.51 |
| 3 | 9.86 / 3.93 | 4.37 / 1.18 | 16.8 / 7.42 |

- So the claim "risk is erfc(B/(σ√τ))" holds **only for deterministic delays**. Random fix times fatten the tail to exponential. More generally, if fix times have a power-law tail P(t > u) ~ u^{−κ}, failure is dominated by the slowest fixes, and at leading order P ~ P(t > B²/σ²) ~ z^{−2κ}. Then ε_σ → 2κ and ε_τ → κ − 1, which **reverses if κ < 1** [PROOF-sketch, leading order].

### 2.3 Jumps and heavy tails

- **Many small jumps** of rate λ and second moment E[J²] act as diffusion with σ² → σ² + λE[J²] [KNOWN: compound Poisson to diffusion limit]. The model is unchanged, at a hotter z. NUMERIC: ε_τ falls from 0.93 to 0.38, consistent with the hotter z.
- **Subexponential (heavy-tailed) jumps.** By the single-big-jump principle (Foss, Korshunov & Zachary, *An Introduction to Heavy-Tailed and Subexponential Distributions*, Springer), failures come increasingly from one jump larger than B. The hazard then tends to λP(J > B), **independent of τ**, so ε_τ → 0 [PROOF of the limit].
  - NUMERIC (`jumps_checks.out`): the approach is **slow**. With 82% of failures caused by single jumps, ε_τ is still 0.46, against 0.93 with no jumps. At realistic parameters, heavy tails roughly halve the τ effect; they do not erase it.
- **α-stable shocks.** Accumulation scales as τ^{1/α}, so the dimensionless group becomes B/(c·τ^{1/α}) [KNOWN scaling]. The Gaussian √τ is the α = 2 case only.

### 2.4 The earlier toy's "reversal" [NUMERIC, `toy_reversal_check.out`]

- The toy computed the hazard as P_window/τ. The exact renewal hazard is P_window/E[min(T_hit, τ)].
- In the one-sided, symmetric-reset toy, the exact hazard still reverses, but at σ/B ≈ 0.38 instead of 0.31. The reason is that full reset also erases **favourable** deviations: a slow fixer keeps its lucky streaks longer.
- In every two-sided model, ε_τ ≥ 0 everywhere.
- By the identity, reversal happens exactly where ε_σ < 2 (the one-sided model has ε_σ = 1.1–1.9 for z < 1).
- Whether real fixers erase good luck is an empirical question. Downside-only fixing should not reverse [CONJECTURE; a coupling argument is plausible but not done].
- The post's qualifier ("as long as slow fixers still usually survive a fix window") was derived from the artifact-inflated version.

### 2.5 Why C3 found τ null, ranked

1. **The prediction was misspecified [PROOF].** Prereg r_τ = ½ is the cold or incident limit. The identity gives r_τ = ½ − 1/ε_σ. The prereg band [0.25, 1] needs ε_σ ≥ 4, and its upper half (r_τ > ½) is unreachable in the continuous regime.
2. **Attenuation: the proxies barely carry the model's variables [PROOF + DATA].**
   - Observed β_σ = 0.28. Every two-sided model has ε_σ ≥ 2 (grid minimum 2.000), so the proxies attenuate by a factor of about 7 or more.
   - Under proportional attenuation a = β_σ/ε_σ, true, the prediction is β_τ = β_σ/2 − a, in [0, 0.14). C3's CI [−0.09, 0.10] covers every case with ε_σ, true ≤ 7 (`c3_diagnostics.out`). In the one-sided class the range widens to (−0.14, 0.14).
   - **C3 had essentially no power to see the τ term even if true.** Uninformative is not refuted.
   - Caveat: equal attenuation across covariates is an assumption, used only as an illustration.
3. **Units: z was undefined [DATA, predictors only].**
   - B = mean closures per month is a *flow* (capacity), not a stock that shocks deplete.
   - σ = SD of monthly inflow. Its Fano factor σ²/mean has median 1.85, with 55% of repos below 2 (near Poisson counting noise). The slope d ln σ/d ln volume is 0.68, close to the Poisson 0.5.
   - So σ largely measured √size, and corr(ln σ, ln B) = 0.79.
   - τ (KM median close time) spans 0.09–18 months between the 10th and 90th percentiles and mixes triage with fixing.
4. **Shock class [CONJECTURE].** Project death is plausibly single-jump (the maintainer leaves), and that rules out ε_τ (§2.3). This is testable: does dormancy follow an abrupt drop in the top contributor's activity?
5. **Endogeneity and selection [KNOWN mechanism; CONJECTURE here].**
   - Projects with big buffers can afford slow triage, and the optimal τ\* rises with B/σ.
   - Survivorship (alive in mid-2023) truncates away hot, slow units.
   - Both push β_τ toward 0.

### 2.6 The regime where τ MUST show up (sharper prediction)

**Necessary conditions:**
- (i) τ is exogenous, or at least not chosen in response to z;
- (ii) B is a stock in the units of accumulated shock, σ is innovation per √time, and τ uses the same clock;
- (iii) the cold regime, z ≳ 1.5 (per-window failure probability ≲ 15%);
- (iv) light-tailed shocks, checked by the share of failures preceded by one shock larger than B;
- (v) enough events: cold means rare, so large N.

**Predictions:**

| Quantity | Prediction |
|---|---|
| ε_τ, z ≈ 2 | 0.6 (rate fix) to 2.5 (OU) |
| ε_τ, z ≈ 3 | 1.2 to 7.4 |
| ε_τ, z ≲ 0.75 | ≤ 0.21 |
| r_τ = β_τ/β_σ, z ≈ 2–3 | 0.19–0.44 (continuous regime); exactly 0.5 (incident regime) |
| ln τ × z interaction on the log-hazard scale | **positive**: τ matters most where buffers are large relative to shocks |
| Absolute added failures | peak at intermediate z (fixed delay) or saturate (other fix types) |

At fixed level spread s, ε_τ = −1.

---

## 3. Scale invariance (Task 3, the core claim)

**Question.** Coarse-grain N agents, each facing (σ, τ, B, c, w, Λ). Is the result an agent facing the same problem with renormalized parameters?

### 3.1 Shocks: closure holds generically [KNOWN]
- Sums of independent finite-variance increments converge to Brownian motion (CLT). Infinite-variance sums converge to α-stable laws.
- These are the fixed points of the probabilistic renormalization group (Jona-Lasinio 1975, Nuovo Cimento B 26:99).
- So the *shock* side of the problem is scale-free in form, with σ' = σ√(N(1 + (N−1)ρ)) for pairwise correlation ρ (MC: 9.36 against theory 9.38).
- **This is universality, which is why it is cheap:** it holds for any additive system.

### 3.2 Buffers: the temperature flows, and its direction depends on fungibility [PROOF + NUMERIC]

**Pooled buffers** (fungible, with transfers faster than τ):

  **z_N = z·√(N/(1 + (N−1)ρ))**

- The unit cools with size.
- At ρ = 0, z grows as √N without limit (diversification).
- At ρ > 0, z saturates at z/√ρ. Correlated shocks set a floor temperature that no amount of size removes.

**Weakest link** (each part has its own buffer, and any part failing brings down the whole): h_N = N·h(z). In the tails this is the *same form* with:
- z' ≈ √(z² − ln N) for Gaussian tails (z = 3, N = 16: exact 2.45, rule 2.50);
- z' ≈ z − ln N/√2 for exponential tails.

The unit **heats** with size. Its maximum viable size without pooling is about N_max ~ e^{z²−1} (Gaussian class).

**CONJECTURE (testable across scales).** Large adaptive units must pool buffers (circulatory systems, treasuries, shared inventories) once N passes about e^{z²}, and units that cannot pool stay small.

### 3.3 Fix times: closure holds iff the fix-time spectrum is narrow [KNOWN + NUMERIC]
- **Identical τ.** A sum of OU parts is OU with the same τ. The single-τ first-passage prediction matches MC (ratio 1.01).
- **Heterogeneous τ.** Aggregation produces **long memory** (Granger 1980, J. Econometrics 14:227). NUMERIC: φ² ~ Beta(1, 1.2) gives a GPH estimate d = 0.44 against Granger's 0.40. Identical φ = 0.9 parts give 0.09, which is bandwidth bias.
- **Consequences:**
  - The coarse-grained unit has **no single τ**. A fitted OU's τ depends on the sampling interval: 2.0, 2.6 or 12.6 for samples every 0.05, 1 or 10 time units.
  - The single-τ hazard prediction is off by **1.36×** (τ ratio 10) and **2.39×** (τ ratio 100) (`coarse_grain_checks.out` §5).
  - The higher level faces a *multi-mode* problem: the right object is a sum over modes, as in T3b/T7b, not one (σ, τ, B).

### 3.4 Policies and costs: a representative agent exists only under a Gorman-type condition [PROOF + NUMERIC]
- The sum of the parts' optimal tracking costs is Σσ_i√(2c_iw_i). One aggregate clock costs √(2·Σc_i·Σw_iσ_i²).
- By Cauchy–Schwarz the ratio is ≥ 1, with **equality iff c_i/(w_iσ_i²) is the same for all i**. That is the analogue of Gorman's (1953, Econometrica) parallel-Engel-curve condition for a representative consumer.
- With a common c the penalty is ≤ √K (T3b). With heterogeneous c it is **unbounded**: 51× seen in random draws, and 500× when cost sits in one part and drift in another.
- **Externalities.** If the whole loses Λ_whole when one part fails, but each part counts only Λ_i < Λ_whole, then the parts' optimal watching (f\*² ∝ Λ ∂h/∂τ, §1.3 row 7c) is too low by √(Λ_i/Λ_whole). The higher level obeys the same objective only if the failure cost is internalized, by incentives, shared fate or a central controller. This counts *against* rule 6's "no one in charge" as a general claim.

### 3.5 When the temperature is scale-free
- Let B ∝ N^b, σ ∝ N^H (H = ½ for independent parts, 1 for fully shared drift) and τ ∝ N^θ, where θ captures detection and communication delay growing with size.
- Then **z ∝ N^{b − H − θ/2}**. The temperature is scale-invariant only on the critical line b = H + θ/2. Off it, the temperature is a relevant variable that flows with size.
- **Data handle [KNOWN].** Stanley et al. 1996 (Nature 379:804) find that the SD of firm growth rates falls as size^{−0.15} or so, so absolute σ ∝ S^{~0.85} (H ≈ 0.85, far from ½). With b = 1 and θ = 0, z ∝ S^{0.15}: firms cool only weakly with size [CONJECTURE: that b ≈ 1].
- Urban scaling exponents (Bettencourt et al. 2007, PNAS 104:7301: ≈ 0.8 for infrastructure, ≈ 1.15 for socioeconomic) give b for cities if buffers are infrastructure-like [CONJECTURE].

### 3.6 Reading on scale invariance

**Proved: form invariance, under four conditions.** Coarse-graining yields an agent with the same objective, with renormalized σ' (CLT), B' (pooled), τ' = τ and costs (c', w') = (Σc, Σwσ²/σ'²), **iff** all four hold:
- C1: shocks lie in a Gaussian or stable basin;
- C2: buffers are fungible, with internal transfers faster than τ;
- C3: fix times are homogeneous (narrow spectrum), or the levels are treated as explicit multi-mode;
- C4: c_i/(w_iσ_i²) is equal across parts and the whole's failure cost is internalized.

**Broken generically.** Each condition fails in real systems:
- correlated shocks (ρ > 0) cap the cooling;
- non-fungible buffers heat the unit;
- heterogeneous τ gives long memory;
- heterogeneous costs and externalities break representativeness.

The strong form (that any population of agents obeying the objective is itself such an agent) is **FALSE**.

**What survives, and is distinctive:**
- (i) the universality classes of F, set by the fix mechanism and not by scale;
- (ii) the identity ε_τ = ε_σ/2 − 1 (or ε_σ/2 for incidents) at every scale;
- (iii) the direction of the temperature flow: pooling cools, weakest link heats, correlation sets a floor.

These are falsifiable cross-scale statements. The renormalization picture is a Gaussian fixed point with no anomalous exponents. There is no deep RG here, and claiming one would be inflation.

---

## 4. Red team: the five strongest objections

| # | Objection | Reading |
|---|---|---|
| 1 | **"The forms are forced."** Dimensional analysis plus CLT universality give σ√(cw), z = B/(σ√τ) and Brownian closure for *any* system with additive noise, one cost scale and one fix time. Recurring EOQ, Kalman and Kramers forms across domains is therefore not evidence for a common principle (this pass proves it, §1.2 and §2.1). | **Answered against the theory's past evidence; fixable going forward.** The "unification" in REAUDIT §2 counts for almost nothing. Content must sit in the risky parts: the F classes, the identity's numbers, the flow directions and the competitor-distinguishing signs (§5). |
| 2 | **Still et al. do not apply.** They assume no feedback, a heat bath, Markov dynamics and an equilibrium start. Adaptive systems act on their world, and firms do not pay in heat. | **Fixable for cells** (Barato–Seifert, Horowitz–Esposito, Sagawa–Ueda handle information flow and feedback). **Fatal to "thermodynamics explains firm design"** but not to the bet: at firm scale the floor holds but does not bind, and the shaping claim rests on J in money and time. O1 makes the currency swap exact in form, which says *where* the bet lives (c_nat), not that it is true. |
| 3 | **Survivorship, endogeneity, measurement.** Observed τ and B are chosen and survivors are selected, so cross-sections mislead. "Buffer", "shock" and "fix time" have no fixed operational units, which invites post hoc fits. C3 used a flow as a buffer. | **Fixable.** Use exogenous τ (instruments, natural experiments; C3b's upstream-release shocks are the right move), frames fixed before outcomes, and preregistered dimensional consistency (B and σ√τ in the same units). Pre-commit the regime cut z ≳ 1.5 and the F class from the fix mechanism *before* seeing outcomes. |
| 4 | **Optimality presumption.** Real cells, firms and cities are not optimal. History, constraints and weak selection dominate (Alchian 1950, JPE 58:211: survivors look as if they optimize only on average). | **Partly answered.** The temperature and identity predictions (§2) are *mechanical* first-passage facts that need no optimality. The rule predictions (§1) need selection strong enough to matter, so test them as comparative statics among long-lived units, or keep them normative. |
| 5 | **"Same at every scale" fails under coarse-graining.** Heterogeneous fix speeds, non-fungible buffers, correlated shocks, heterogeneous costs and externalities each break closure (§3). | **Fatal to the unconditional claim; fixable as a conditional theory** with conditions C1–C4 and predicted flow directions. The README/T7 language "only if" is already close; the post's "every self-maintaining system... the same tradeoff" should be read as conditional. Any wording change needs Chad's OK. |

---

## 5. Decisive experiments (three scales, free data, competitor-distinguishing)

**Shared rules for all three:**
- Estimate (σ, τ, B) on the first time block and outcomes on a later block.
- Lock the code, hash it, and preregister before pulling any outcome.
- Report both the continuous (ε_σ/2 − 1) and incident (ε_σ/2) versions of the identity.
- **Joint miss condition:** at **two or more** scales, in the cold regime (z ≥ 1.5), either β_lnτ|σ,B ≤ 0 with the CI excluding +0.2, or the fixed-spread slope β_lnτ|s,B is closer to 0 than to −1. Either outcome rules out the τ term and the dynamical temperature.

### D1. Firm scale: US commercial banks, 2008–2014 failures
- **Data (free):**
  - FFIEC Central Data Repository bulk Call Reports (quarterly, 2001Q1–2007Q4), https://cdr.ffiec.gov/public/PWS/DownloadBulkData.aspx;
  - FDIC failed-bank list (CSV), https://www.fdic.gov/bank-failures/download-data.csv. Count the 2008–2014 failures from the CSV before analysis; expect several hundred.
- **Measures:**
  - B = equity/assets at 2007Q4 minus 2%, the critically-undercapitalized Prompt Corrective Action line;
  - σ = SD of quarterly ROA over 2001–2007 (the innovation to capital);
  - τ = per-bank capital-recovery time = −1/ln φ from an AR(1) on the capital-ratio deviation from the bank's own 2001–2007 mean. Flannery & Rangan 2008 (Rev. Finance 12:391) give about 53%/yr average adjustment for large BHCs, so τ ≈ 1.3 yr.
- **Competitor:** the Boyd–Graham Z-score, (E/A + μ_ROA)/σ_ROA, from Roy's 1952 safety-first. It contains no τ, so it predicts β_lnτ|Z = 0. Merton/Black–Cox structural models with a fixed 1-year horizon are a second competitor.
- **GTAO predictions:**
  - (1) β_lnτ > 0 conditional on σ and B;
  - (2) r_τ in [0.19, 0.5] in the cold tercile of z;
  - (3) a **positive** ln τ × z interaction: τ matters more in well-capitalized banks. A naive "slow banks die when weak" story predicts the opposite;
  - (4) using a bank-specific √τ_i horizon in distance-to-failure beats a fixed 1-yr horizon (ΔAIC > 10).
- **Risk:** 2008 was partly a common jump. That argues for the single-jump regime and a smaller ε_τ, so preregister the jump-share check (for example, failures preceded by one quarter with losses > B).

### D2. Organism scale: human glucose regulation (continuous glucose monitoring)
- **Data (free):**
  - ShanghaiT1DM/T2DM (Zhao et al. 2023, Sci. Data; figshare doi:10.6084/m9.figshare.20444397): 12 T1DM and 100 T2DM patients, Libre CGM every 15 min;
  - add larger free CGM sets only after checking their licences.
- **Measures:**
  - per patient, first half of the recording: detrend the daily cycle, then fit OU/AR(1). This gives τ (return time), σ (innovation), s (level SD) and B = mean − 3.9 mmol/L;
  - **outcome**, second half: count hypoglycaemia episodes (< 3.9 mmol/L for ≥ 15 min).
- **Competitor:** static risk indices that depend only on the glucose distribution: the Low Blood Glucose Index (Kovatchev et al. 1998, Diabetes Care 21:1870), SD and CV. They predict no τ effect at a fixed distribution.
- **GTAO predictions:**
  - at fixed (B, s), episode rate ∝ τ^{−1}: slope **−1** in [−1.4, −0.6] (§2.1c);
  - at fixed innovation σ, a **positive** slope that follows the identity;
  - log(rate·τ) against z = B/(s√2) collapses onto one curve across T1DM, T2DM and healthy groups (group offsets < 0.3 log units). Its tail class says whether counter-regulation acts like proportional control (Gaussian tail) or like intermittent dosing (exponential tail, the rate class).
- **Risks:**
  - small n;
  - meals and insulin are forcing, not noise (fit residuals after meal regressors);
  - 15-min sampling biases τ for fast dynamics.

### D3. Population scale: animal populations (density-dependent regulation)
- **Data (free):** Global Population Dynamics Database, about 5,000 series, KNB doi:10.5063/F1BZ63Z8. Use series with ≥ 30 annual counts.
- **Measures:**
  - first half: a state-space Gompertz fit to ln N (allowing observation error) gives φ, hence τ = −1/ln φ years, plus σ (process innovation) and s;
  - quasi-extinction line at 1/5 of the geometric mean, so B = ln 5 = 1.61 for every series, which removes one free parameter;
  - **outcome**, second half: number of downcrossings, and time to first crossing.
- **Competitors:**
  - density-independent diffusion (Dennis, Munholland & Scott 1991, Ecol. Monogr. 61:115): risk from μ and σ² only, with no return time;
  - a static CV index (predicts 0 at fixed s).
- **GTAO predictions:**
  - β_lnτ|s = **−1**;
  - β_lnτ|σ > 0 and rising with z (identity);
  - one collapse curve across taxa, with an OU (Gaussian) tail where density dependence is the "fix", and an exponential/power tail where catastrophes dominate (Lande 1993, Am. Nat. 142:911).
- **Risks:** observation error biases φ down (hence the state-space fit); short series.

**Spare at city/infrastructure scale.** Grid frequency is an engineered regulator. Use the NESO GB 1-s data (https://www.neso.energy/data-portal/system-frequency-data) and the Fingrid Nordic 10-Hz data (https://data.fingrid.fi/en/datasets/339). Sweeping the threshold B traces F(z) within one grid, and τ differs across grids. Schäfer et al. 2018 (Nature Energy 3:119) already show heavy tails, so this test predicts a *reduced* ε_τ. That makes it a check on the §2.3 correction.

---

## 6. What this changes (recommendations only; nothing was edited)

- **C3:** reframe it from "the τ term failed" to "**uninformative about τ** by construction". The specific reasons are r_τ misspecification, attenuation (β_σ = 0.28 against a model minimum of 2), and B being a flow.
- **C3b:** C3b (preregistered today, `tests/C3b/`) is in the *incident* regime. Read it with ε_τ = ε_σ/2, the regime cut z ≳ 1.5 and the jump-share check. Projects that never fix are censored on τ, which creates a survivorship trap.
- **Post v9 qualifier.** "As long as slow fixers still usually survive a fix window" rests on the one-sided, symmetric-reset toy with per-window counting. A correction belongs in a follow-up, needs an independent check and Chad's OK, and should say:
  - the τ effect is largest *in relative terms* in the cold regime;
  - it never reverses when fixing does not erase favourable deviations.
- **THEOREMS candidates** (each needs an independent review before going public):
  - O1, the thermodynamic EOQ;
  - the dimensional identity;
  - the F classes;
  - the flows under pooling and weakest-link;
  - the Gorman-type closure condition.
- **Self-limits.**
  - The MC runs are small: 3–6k paths, with discretization corrected by Brownian bridges.
  - The heavy-tailed fix-time power law is leading-order only.
  - The "no reversal under downside-only fixing" claim is a conjecture.
  - No outcome data were analysed here.
  - Not independently reviewed.
