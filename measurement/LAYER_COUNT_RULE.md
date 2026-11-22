# Layer-counting rule for real systems

*Saturday 21 November 2026, evening, America/New_York. Branch `layer-count-rule-2026-11-21`, draft PR, beside `main` at `c92886a`. Written by one executor for Chad; a self-check, not an independent review. Addresses OPEN_WORK T15. Code: `tools/layer_count_rule.py` (pytest `tools/test_layer_count_rule.py`). No locked prereg or hash file is touched, and the Part 2 hypothesis sentence is unchanged. CX1 stays OPEN.*

This note finalizes the operational counting rule that THEORY §3 and `figures/face_placements.md` §4 still marked as proposed, so that a later N56 test has a fixed way to count layers and a fixed way to predict the cheapest count from measurable inputs. It builds on draft PR #145 (layer convexity / the N60 premise) and does not repeat that proof.

## 0. Bottom line

A system's layers are the distinct memory time constants in its response, counted by degree: a real pole counts 1, a rhythm (a complex-conjugate pair) counts 2, an integrator with a filter counts 2. Org-chart levels count only if they hold such a state. A level that only relays a read is not a layer (CT16).

**To count the layers a real system has (K_obs),** fix the input/output pair and the time-scale band before any data, measure the response kernel on that band, fit sums of exponentials (complex pairs allowed), accept a higher degree only if it lowers BIC by at least 10, drop poles outside the band, classify local versus shared *before* merging, merge only within a class when time constants differ by less than a factor of 3 (the default resolution; a class may preregister another factor), and drop relay-only poles. Report a bootstrap interval when the record is noisy. This side of the rule never sees prices, the world's spectrum, or argmin J.

**To predict the cheapest count (K*) from a measured world,** form the excess-error curve ε_K = E_K/E_∞ − 1 at each degree K (in the model's store library) and the stake ratio R = w E_∞ / h. K* is always the leftmost minimizer of J(K) ∝ K + R(1 + ε_K). That minimizer always sits on the lower convex hull of {(K, ε_K)}, and the hull increment test of `core/KEYSTONE_NOTE.md` §4 returns it. This is an identity, not a new rule. The adjacent N60-from-0 count, K* = #{k ≥ 1 : R(ε_{k−1} − ε_k) > 1}, is **exact for every R if and only if the decrements of ε_K are non-increasing** (Fox 1966; L1 of draft PR #145). When they are, use it. When they are not — the typical case when S/N has a peak, which is what a rhythm is — do **not** use the adjacent count. Use the hull (equivalently, argmin J). A pair-count shortcut and the failed IMP-N60 rule are not substitutes. A predictive shortcut from poles and stakes alone, without computing ε_K, remains OPEN (T18).

**To compare the two in a later N56 test,** do not treat a raw K_obs ≠ K* as a miss by itself. THEORY §3 already places the miss in cost space: the observed design lies in the predicted band only if J_obs ≤ (1 + ε + δ_meas) J*, with ε the selection resolution 10/(σ N_e) and δ_meas the propagated measurement error. A count difference is a miss only if the observed design's J lies outside that band. This note implements the band; it does not run N56 and does not score any real system. No system has yet been counted by this rule.

## 1. Inputs

**Observation (a measured system).**

| Input | What it is | When it is fixed |
|---|---|---|
| Input/output pair | The drive and the read-out (table in `figures/face_placements.md` §4) | Before any data, per class |
| Time-scale band | The interval of memory time constants that count | Before any data, per class |
| Response kernel | Impulse, step, or white-noise response on that band, isolated-unit and pooled | By a protocol fixed in advance |
| BIC gate | Default ΔBIC ≥ 10 (Kass & Raftery 1995, "very strong") | Before any data; a class may preregister another gate |
| Resolution factor | Default 3 (time-constant ratio) | Before any data; a class may preregister another factor |
| Bypass / delay record | Optional, for the relay test (CT16) | Protocol fixed in advance |
| Isolation records | Optional, for local vs shared | Protocol fixed in advance, or a pre-registered substitute when isolation is impossible |

**Prediction (a measured world).**

| Input | What it is |
|---|---|
| Excess-error curve ε_K | E_K / E_∞ − 1 at each degree K, from the model's store library (Model S: first-order real stores; a richer library if that is the preregistered design set) |
| Stake ratio R | w E_∞ / h |
| Selection resolution ε | 10/(σ N_e), THEORY §3 (c) |
| Measurement error δ_meas | Fractional error in J propagated from the input errors, preregistered |

ε_K is a functional of S/N in the linear-Gaussian class (N60). Computing it still requires solving the K-store design problem at each K. That is already the definition of argmin J; the hull test is the same number, restated.

## 2. Observation procedure

The steps are the v2.5.2 rule, now implemented and tested. A class preregisters them before any N56 test; counting is never redone after a comparison.

1. **Fix the pair and the band** before any data (`figures/face_placements.md` §4).
2. **Measure the response kernel** over that band, on isolated units and pooled, by a protocol fixed in advance.
3. **Fit sums of exponentials** (complex-conjugate pairs allowed) of degree 0 … K_max, by variable projection (Golub & Pereyra 1973) seeded with the matrix pencil (Hua & Sarkar 1990). Accept a higher degree only if it lowers BIC by at least 10 against every lower degree. Poles outside the band are not counted. Parameter count in the BIC is 2K (a time constant and a linear weight per degree; a pair has four parameters and degree 2).
4. **Classify, then merge.** Classify each pole as local or shared *before* any merging: local if it appears in each unit's own isolated response (or, fixed in advance, in the per-unit response to unit-specific drives); shared if it appears only in the pooled response. Then merge only within a class: two poles of the same class and the same kind (real with real, pair with pair) whose time constants differ by less than the resolution factor count as one. A local and a shared pole are never merged, and a rhythm is never merged with a real pole, so "both" and "a rhythm plus a store" stay observable.
5. **Count by degree.** A real pole counts 1; a complex pair counts 2; an integrator with a filter counts 2.
6. **Relay-only test.** Bypass the candidate level or replace it with a pure delay of the same latency, and refit. The level is a layer only if a pole disappears or moves by more than the resolution factor. If only a delay disappears, it is a relay (CT16).
7. **Uncertainty.** A parametric bootstrap of steps 3–5, when reported, gives a 5–95% interval on K_obs. The point count is the selected degree on the original record.
8. **Assignment to map dots** is unchanged (`figures/face_placements.md` §4, steps 7–9), including the frozen prediction SHA-256 of `figures/face_systems.py`. Only degree-1 components are scored against B.11, because B.11 covers one store per design; degree-2 components are counted and reported.

## 3. Prediction procedure

1. Compute ε_K at K = 0, 1, …, K_max in the preregistered library.
2. Test whether the decrements d_K = ε_{K−1} − ε_K are non-increasing (convexity of ε, up to a preregistered numerical tolerance).
3. If they are, **K* = N60-from-0** = #{k ≥ 1 : R d_k > 1}. This equals the leftmost argmin of J for every R > 0 (L1). Include K = 0: N60 as written, which starts at 1, has a known hole and returns 1 when the first increment does not pay.
4. If they are not, **K* is the leftmost hull increment** (KEYSTONE_NOTE §4): walk the lower-hull vertices k_i and jump to k_{i+1} iff R(ε_{k_i} − ε_{k_{i+1}}) > (k_{i+1} − k_i). Equivalently, take argmin_K [K + R(1 + ε_K)]. Record that the adjacent count was not used, and record the adjacent count as a diagnostic.
5. The predicted **count band** is {K : J(K) ≤ (1 + ε + δ_meas) J*}.

**Rhythmic (peaked) worlds.** A peak in S/N can break convexity. The minimal example, from draft PR #145, is three frequency cells with Wiener gain W = (0, 1, 0) and weights (2, 1, 1), which give decrements 1/3 then 2/3 and ε = (1, 2/3, 0). At R = 3 the adjacent count returns 1 and the argmin is 2. That is the same complementarity as "a rhythm is two layers by degree" (CT21) and the two-oscillator counterexample in KEYSTONE_NOTE §2 (R = 3, adjacent count 2, argmin 3). In every such case the procedure of steps 4–5 applies: count observed rhythms by degree, and predict K* with the hull, not with the adjacent formula, not with a pair-count cap, and not with IMP-N60 (which failed; KEYSTONE_NOTE §5).

Convexity *does* hold, and so the adjacent count *is* exact, in the band model of draft PR #145 whenever S/N is non-increasing in frequency (Theorem B, any number of time scales), and in Model S with at most two OU modes at lead 0 (Theorem S2). Model S with three or more modes stays numerical (144/144 convex in that draft, 120/120 in the S5 rerun); N60 on main therefore keeps its status, **PROVED (in-model) given convexity (numerical)**. This note uses that status and does not upgrade it.

## 4. Exact versus approximate

| Claim | Status | Scope |
|---|---|---|
| K* = argmin_K [K + R(1 + ε_K)] | Definition | Any ε sequence, any R > 0 |
| Hull increment = leftmost argmin | PROVED (identity) | Any real sequence ε_K (KEYSTONE_NOTE §4); tested here on 400 random sequences and on the peaked example |
| N60-from-0 = leftmost argmin for every R | PROVED iff decrements are non-increasing | L1 of draft PR #145, restated and tested here; converse holds for distinct positive decrements |
| N60 as written (starts at 1) | Exact on that set except the K* = 0 hole | When the first increment does not pay, the formula returns 1 and the argmin is 0 |
| Convexity when S/N is non-increasing, band model 𝓑 | PROVED in draft PR #145 (Theorem B) | Ideal low-pass layers, zero-phase; not Model S |
| Convexity in Model S, J ≤ 2 modes, lead 0 | PROVED in draft PR #145 (Theorem S2) | Not repeated here |
| Convexity in Model S, J ≥ 3 | OPEN (numerical, no counterexample) | S5; draft PR #145 |
| A peak in S/N can break convexity | PROVED by example | Draft PR #145; the peaked example is a regression test here |
| Predictive rhythm rule from poles and stakes alone | OPEN (T18) | IMP-N60 failed; no new candidate is registered |
| Observation recovers the true degree of a finite exponential sum | Exact in the noiseless, well-separated case; approximate otherwise | Finite Prony / pencil identifiability is classical (Hua & Sarkar 1990). With noise, the BIC gate is conservative (tends to under-count). Time constants closer than the resolution factor are merged by construction (Istratov & Vyvenko 1999). Out-of-band poles are dropped by construction. Nonlinear, non-stationary, or unmodelled kernels are outside the fit class. Isolation and bypass records, when missing, leave local/shared classification and the relay test unused, and the count is of the pooled kernel only. |

The observation rule can disagree with K* when the system is not at the minimum: that is required, not a defect. The synthetic tautology check builds under-built and over-built kernels in a two-mode Model S world and confirms that step 1 recovers the system's degree, while those designs sit outside the cost band of the two-store minimum.

## 5. Derivation, within the model

**Prediction, exactness (L1; Fox 1966; draft PR #145).** Write d_K = ε_{K−1} − ε_K and J(K) ∝ K + R(1 + ε_K). Then J(K) − J(K−1) = 1 − R d_K. If the decrements are non-increasing, this difference is non-decreasing, so J falls exactly while R d_K > 1 and rises afterwards: N60-from-0 is the leftmost minimizer for every R > 0. Conversely, a later increase d_m < d_{m+1} puts (m, ε_m) strictly above the chord from m−1 to m+1, so J(m) > min(J(m−1), J(m+1)) for every R, and the adjacent count still returns m on an open interval of R (when the decrements are positive and distinct). The general rule, with or without convexity, is the hull test, whose short proof is already in KEYSTONE_NOTE §4 and is not repeated.

**Observation, degree of a linear kernel.** In the linear time-invariant class the causal memory is a convolution kernel. A finite-dimensional realization has a rational transfer function whose McMillan degree is the number of poles, counted with multiplicity, which is the number of states the system holds. A complex-conjugate pair is two states (CT21). The matrix pencil recovers those poles from uniformly sampled impulse data in the noiseless case (Hua & Sarkar 1990). With noise, a BIC difference of 10 is the "very strong" threshold of Kass & Raftery 1995; it is a choice, already in the v2.5.2 placeholder, not a theorem. The factor-3 merge is a resolution choice, already in that placeholder, motivated by the known ill-posedness of exponential analysis (Istratov & Vyvenko 1999) and not derived as a unique number from J. A class may preregister a different factor. The relay test is the operational form of CT16. None of this uses the world's spectrum or the prices, which is what keeps the observation from being a tautology of argmin J.

**Comparison.** THEORY §3 maps the cost band {𝒟 : J(𝒟) ≤ (1 + ε + δ_meas) J*} into design space and already says that a discrete count differs from the predicted one as a miss only if the counted design's J lies outside the band. The functions `cost_band` and `in_cost_band` are that clause.

## 6. Prior art

DOIs below were resolved on Crossref this session (21 November 2026, ET).

- Fox 1966, *Management Science* 13:210, discrete optimization via marginal analysis, doi [10.1287/mnsc.13.3.210](https://doi.org/10.1287/mnsc.13.3.210). The exactness of the adjacent count under non-increasing decrements is this argument. Credit is as an application, not a new tool. (Also the prior-art credit in draft PR #145.)
- Hua & Sarkar 1990, *IEEE Transactions on Acoustics, Speech, and Signal Processing* 38:814, matrix pencil for exponentially damped sinusoids, doi [10.1109/29.56027](https://doi.org/10.1109/29.56027).
- Golub & Pereyra 1973, *SIAM Journal on Numerical Analysis* 10:413, variable projection for separable nonlinear least squares, doi [10.1137/0710036](https://doi.org/10.1137/0710036).
- Kass & Raftery 1995, *Journal of the American Statistical Association* 90:773, Bayes factors, doi [10.1080/01621459.1995.10476572](https://doi.org/10.1080/01621459.1995.10476572) (also JSTOR 10.2307/2291091). The ΔBIC ≥ 10 gate is their "very strong" threshold; it was already in `figures/face_placements.md`.
- Istratov & Vyvenko 1999, *Review of Scientific Instruments* 70:1233, exponential analysis in physical phenomena, doi [10.1063/1.1149581](https://doi.org/10.1063/1.1149581). The resolution warning for close time constants.
- Gavish & Donoho 2014, *IEEE Transactions on Information Theory* 60:5040, hard threshold for singular values, doi [10.1109/TIT.2014.2323359](https://doi.org/10.1109/TIT.2014.2323359). Used only as a heuristic Hankel cross-check, not as K_obs (a Hankel matrix does not have independent noise entries).

The hull identity is already in this repository (`core/KEYSTONE_NOTE.md` §4). The convexity theorems and the peaked failure class are in draft PR #145 (`theory/LAYER_CONVEXITY.md`); this note refers to them and does not claim them.

**What is new here, as an assembly of known parts** (a limited search of this repository and of the citations above found no earlier statement of the assembled operational rule; not checked by a specialist): fixing the v2.5.2 placeholder as a testable procedure with a coded observation path, a coded prediction path that branches on the L1 premise rather than always using N60, a cost-band comparison that matches THEORY §3, and synthetic checks that the observation is not a tautology of argmin J. Nothing here is claimed as a new theorem about nature. N56 stays OPEN and untested.

## 7. Code

- `tools/layer_count_rule.py` — `detect`, `count_layers`, `merge_close_states`, `classify_local_shared`, `relay_test` on the observation side; `n60_from`, `n60_as_written`, `hull_increment`, `predict_count`, `cost_band`, `in_cost_band` on the prediction side.
- `tools/test_layer_count_rule.py` — exactness and the peaked example; the hull identity on random sequences; merge, classify, and relay helpers; a few well-separated / rhythmic / out-of-band / close-pole detections; the tautology check.
- A short self-check writes `measurement/layer_count/RESULTS.json`.

## 8. Open after this note

- N56 remains OPEN: no qualifying system has had its world, prices, and design measured and counted by this rule.
- T18, a predictive rhythm rule from poles and stakes without first computing ε_K, remains OPEN and deprioritized.
- Model S convexity for J ≥ 3 remains OPEN (numerical only); that is W9 / draft PR #145, not this note.
- The default resolution factor 3 is a choice, not a derived constant.
- E. coli's published two-pole kernel (Mattingly et al. 2021) is degree 2 and was not selected by this rule; it is still reported, not scored against B.11.
