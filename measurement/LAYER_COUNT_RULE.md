# Layer-counting rule for real systems

*Saturday 21 November 2026, evening, America/New_York. Branch `layer-count-rule-2026-11-21`, draft PR #150, merged with `origin/main` at `b16193d` (PR #148, CLAIM_MAP v2.75). Revised after the independent review `reviews/layer_count_rule_2026-11-21/REVIEW.md` and the confirm should-fixes in `reviews/layer_count_rule_2026-11-21/CONFIRM.md`; revisions are a self-check, not yet re-reviewed. Addresses OPEN_WORK T15. Code: `tools/layer_count_rule.py` (pytest `tools/test_layer_count_rule.py`). No locked prereg or hash file is touched, and the Part 2 hypothesis sentence is unchanged. N56 and CX1 stay OPEN.*

This note finalizes the operational counting rule that THEORY §3 and `figures/face_placements.md` §4 still marked as proposed, so that a later N56 test has a fixed way to count layers and a fixed way to predict the cheapest count from measurable inputs. It builds on PR #145 (`theory/LAYER_CONVEXITY.md`, CLAIM_MAP N64) and does not repeat that proof.

## 0. Bottom line

A system's layers are the distinct memory time constants in its response, counted by degree: a real pole counts 1 and a rhythm (a complex-conjugate pair) counts 2 (the exponential-sum fitter has no pole-at-0 integrator basis; a bounded-rate two-pole adaptation-plus-filter kernel counts 2 as two real poles when both rates lie in the band and pass the resolution merge). Org-chart levels count only if they hold such a state. A level that only relays a read is not a layer (CT16).

**To count the layers a real system has (K_obs),** fix the input/output pair and the time-scale band before any data, measure the response kernel on that band, fit sums of exponentials (complex pairs allowed) across degrees 0 through K_max (degree 0 always eligible, accepting K > 0 only if it lowers BIC by at least 10 against every lower degree and selecting the largest such degree), drop poles outside the band, classify local versus shared *before* merging, merge only within a class when time constants differ by less than a factor of 3 (the default resolution; a class may preregister another factor), and use the bypass/delay test to label whether a candidate level is a layer or a relay (a relay holds no pole of its own, so it does not change K_obs). Report a bootstrap interval when the record is noisy. This side of the rule never sees prices, the world's spectrum, or argmin J.

**To predict the cheapest count (K*) from a measured world,** form the excess-error curve ε_K = E_K/E_∞ − 1 at each degree K (in the model's store library) and the stake ratio R = w E_∞ / h. K* is always the leftmost minimizer of J(K) ∝ K + R(1 + ε_K). That minimizer always sits on the lower convex hull of {(K, ε_K)}, and the hull increment test of `core/KEYSTONE_NOTE.md` §4 returns it. This is an identity, not a new rule. On a finite domain, the from-0 count K*_0(R) = #{K ≥ 1 : R(ε_{K−1} − ε_K) > 1} **equals the leftmost argmin for all R ≥ 0 if the decrements of ε_K are non-increasing** (Fox 1966; L1 of PR #145, CLAIM_MAP N64); the converse holds under positive, pairwise distinct decrements (distinctness with the threshold decrement positive is enough; see theory/LAYER_CONVEXITY.md; without those side conditions, d = (−2, −1) is a counterexample to a bare biconditional). When the decrements are non-increasing, use K*_0(R). When they are not — the typical case when S/N has a peak, which is what a rhythm is — do **not** use the adjacent count. Use the hull (equivalently, argmin J). A pair-count shortcut and the failed IMP-N60 rule are not substitutes. A predictive shortcut from poles and stakes alone, without computing ε_K, remains OPEN (T18).

**To compare the two in a later N56 test,** do not treat a raw K_obs ≠ K* as a miss by itself. THEORY §3 already places the miss in cost space: the observed design lies in the predicted band only if J_obs ≤ (1 + ε + δ_meas) J*, with ε the selection resolution 10/(σ N_e) and δ_meas the propagated measurement error. A count difference is a miss only if the observed design's J lies outside that band. This note implements the band; it does not run N56 and does not score any real system. No system has yet been counted by this rule.

## 1. Inputs

**Observation (a measured system).**

| Input | What it is | When it is fixed |
|---|---|---|
| Input/output pair | The drive and the read-out (table in `figures/face_placements.md` §4) | Before any data, per class |
| Time-scale band | The interval of memory time constants that count | Before any data, per class |
| Response kernel | Impulse, step, or white-noise response on that band, isolated-unit and pooled | By a protocol fixed in advance |
| BIC gate | Default ΔBIC ≥ 10 (precommitted penalty threshold; numerical scale from Kass & Raftery 1995, not a regular Bayes-factor theorem here) | Before any data; a class may preregister another gate |
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

These steps are implemented and tested in `tools/layer_count_rule.py`. A class preregisters them before any N56 test; counting is never redone after a comparison.

1. **Fix the pair and the band** before any data (`figures/face_placements.md` §4).
2. **Measure the response kernel** over that band, on isolated units and pooled, by a protocol fixed in advance.
3. **Fit sums of exponentials** (complex-conjugate pairs allowed) by variable projection (Golub & Pereyra 1973) seeded with the matrix pencil (Hua & Sarkar 1990). Fit degrees 0 through K_max. Degree 0 is always eligible. Accept degree K>0 only if it lowers BIC by at least 10 against every lower degree, and select the largest such degree. A rhythm may enter as a jump of 2. Parameter count in the BIC is 2K (a time constant and a linear weight per degree; a pair has four parameters and degree 2). Locked default fitter constants (unless a class preregisters others): `K_MAX = 5`; uniform record decimated by integer stride `ceil(n / 800)` to at most `MAX_FIT_PTS = 800` samples for variable projection and BIC; matrix pencil on at most `PENCIL_MAX_PTS = 1500` samples with window `floor(n / 3)` and rate clip `[0.05/T, 3/Δt]`; variable projection (`least_squares`, `"trf"`) rate bounds `[0.02/T, 4/Δt]`, keeping the seed if the optimizer raises an exception; the same pencil clip and the same variable-projection bounds apply to both nonlinear parameters (the decay and the angular frequency); candidate starts at degree K are the pencil fit (when `n_real + 2 n_pair = K`), an all-real log-spaced grid on `[1/T, 1/Δt]`, and for `K ≥ 2` one pair seeded at decay `3/T` and period `T/5` plus `K − 2` log-spaced real poles (a second rhythm enters only if proposed by the pencil). Band cut: a real pole is in-band if its time constant τ = 1/b lies in the band; a complex pair is in-band if both its decay time τ = 1/d and its period 2π/ω lie in the band. Poles outside the band are not counted.
4. **Classify, then merge.** Classify each in-band pole as local or shared *before* any merging, on both the pooled record and each unit record: within each unit, match isolated-unit in-band poles to same-kind pooled in-band poles by a *maximum-cardinality matching under the factor* (an edge exists when the time-constant ratio is `< factor`; for a complex pair, both the decay time and the period must lie within the factor). Among maximum-cardinality matchings, the rule takes the one with the smallest sum of log-ratios; remaining ties are broken by the smaller pooled time constant. A pooled pole is local if it matches in every unit (or, fixed in advance, in the per-unit response to unit-specific drives), and shared otherwise. Then merge only within a class, and only among poles that the unit records matched to the same partners: two poles of the same class, the same match-set, and the same kind (real with real, pair with pair) whose time constants differ by less than the resolution factor (ratio `< factor`, default 3; for a pair, both decay time and period) count as one. Two pooled poles stay unmerged when different units match them to different partners. A local and a shared pole are never merged, and a rhythm is never merged with a real pole, so "both" and "a rhythm plus a store" stay observable.
5. **Count by degree.** A real pole counts 1; a complex pair counts 2. (There is no integrator basis and the rate bounds exclude a pole at 0; a finite-rate two-pole kernel counts 2 as two real poles when both are in band and separated.)
6. **Relay-only test.** Bypass the candidate level or replace it with a pure delay of the same latency, and refit. The level is a layer only if an in-band pole disappears or moves by at least the resolution factor (ratio `≥ factor`). If only a delay disappears, it is a relay (CT16). Because a relay holds no pole of its own, a relay finding labels the candidate level without changing K_obs.
7. **Uncertainty.** A parametric bootstrap of steps 3–5, when reported, gives a 5–95% interval on K_obs. The loop resamples the pooled record and each unit record and percentiles the same classify-then-merge count, not the single-record merged degree. Until that is the interval, it is not an interval on K_obs. The point count is the selected degree on the original record.
8. **Assignment to map dots** is unchanged (`figures/face_placements.md` §4, steps 7–9), including the frozen prediction SHA-256 of `figures/face_systems.py`. Only degree-1 components are scored against B.11, because B.11 covers one store per design; degree-2 components are counted and reported.

## 3. Prediction procedure

1. Compute ε_K at K = 0, 1, …, K_max in the preregistered library.
2. Test whether the decrements d_K = ε_{K−1} − ε_K are non-increasing (convexity of ε, up to a preregistered numerical tolerance).
3. If they are, **K* = K*_0(R)** = #{K ≥ 1 : R d_K > 1}. This equals the leftmost argmin of J for all R ≥ 0 (L1 / N64). Include K = 0: N60 as written, which starts at 1, has a known hole and returns 1 when the first increment does not pay.
4. If they are not, **K* is the leftmost hull increment** (KEYSTONE_NOTE §4): walk the lower-hull vertices k_i and jump to k_{i+1} iff R(ε_{k_i} − ε_{k_{i+1}}) > (k_{i+1} − k_i). Equivalently, take argmin_K [K + R(1 + ε_K)]. Record that the adjacent count was not used, and record the adjacent count as a diagnostic.
5. The predicted **count band** is {K : J(K) ≤ (1 + ε + δ_meas) J*}.

**Rhythmic (peaked) worlds.** A peak in S/N can break convexity. The minimal example, from PR #145 (`theory/LAYER_CONVEXITY.md` §5), is three frequency cells with Wiener gain W = (0, 1, 0) and weights (2, 1, 1). Here E_∞ = 0 (since W ∈ {0, 1}), so ε_K = E_K/E_∞ − 1 and R = w E_∞ / h are undefined; working directly with the excess E_K − E_∞ = (1, 2/3, 0) (decrements 1/3 then 2/3) at multiplier w/h = 3, the adjacent count returns 1 and the argmin of K + (w/h)(E_K − E_∞) is 2. That is the same complementarity as "a rhythm is two layers by degree" (CT21) and the two-oscillator counterexample in KEYSTONE_NOTE §2 (R = 3, adjacent count 2, argmin 3). In every such case the procedure of steps 4–5 applies: count observed rhythms by degree, and predict K* with the hull, not with the adjacent formula, not with a pair-count cap, and not with IMP-N60 (which failed; KEYSTONE_NOTE §5).

Convexity *does* hold, and so K*_0 is exact, in the band model 𝓑 of PR #145 whenever S/N is non-increasing in frequency (Theorem B, any number of time scales), and in Model S with at most two OU modes at lead 0 (Theorem S2). Model S with three or more modes stays numerical (144/144 convex in PR #145, 120/120 in the S5 rerun, 24/24 fresh J = 5); N60 on main therefore keeps its status, **PROVED (in-model) given convexity (numerical)**. This note uses that status and does not upgrade it.

## 4. Exact versus approximate

| Claim | Status | Scope |
|---|---|---|
| K* = argmin_K [K + R(1 + ε_K)] | Definition | Any ε sequence, any R > 0 |
| Hull increment = leftmost argmin | PROVED (identity) | Any real sequence ε_K (KEYSTONE_NOTE §4); tested here on 400 random sequences and on the peaked example |
| K*_0(R) = leftmost argmin for all R ≥ 0 | PROVED if decrements are non-increasing; converse under positive, pairwise distinct decrements (distinctness with the threshold decrement positive is enough; see theory/LAYER_CONVEXITY.md) | L1 / N64 (PR #145), restated and tested here; without those side conditions the bare iff fails, e.g. d = (−2, −1) |
| N60 as written (starts at 1) | Exact on that set except the K* = 0 hole | When the first increment does not pay, the formula returns 1 and the argmin is 0 |
| Convexity when S/N is non-increasing, band model 𝓑 | PROVED in PR #145 (N64, Theorem B) | Ideal low-pass layers, zero-phase; not Model S |
| Convexity in Model S, J ≤ 2 modes, lead 0 | PROVED in PR #145 (N64, Theorem S2) | Not repeated here |
| Convexity in Model S, J ≥ 3 | OPEN (numerical, no counterexample) | S5; PR #145 |
| A peak in S/N can break convexity | PROVED by example | PR #145 (N64); the peaked example is a regression test here |
| Predictive rhythm rule from poles and stakes alone | OPEN (T18) | IMP-N60 failed; no new candidate is registered |
| Observation recovers the true degree of a finite exponential sum | Exact in the noiseless, well-separated case; approximate otherwise | Finite Prony / pencil identifiability is classical (Hua & Sarkar 1990). Exponential-sum recovery is ill-posed for close time constants depending on SNR and sample size (Istratov & Vyvenko 1999); poles closer than the precommitted resolution factor (default 3) are merged by construction. With noise, ΔBIC ≥ 10 is a precommitted penalty choice (general noisy under-counting behavior is untested beyond the synthetic checks at 10⁻³ and 3×10⁻²). Out-of-band poles are dropped by construction. Nonlinear, non-stationary, or unmodelled kernels are outside the fit class. Isolation and bypass records, when missing, leave local/shared classification and the relay test unused, and the count is of the pooled kernel only. |

The observation rule can disagree with K* when the system is not at the minimum: that is required, not a defect. The synthetic tautology check builds under-built and over-built kernels in a two-mode Model S world and confirms that step 1 recovers the system's degree, while those designs sit outside the cost band of the two-store minimum.

## 5. Derivation, within the model

**Prediction, exactness (L1; Fox 1966; PR #145, N64).** Write d_K = ε_{K−1} − ε_K and J(K) ∝ K + R(1 + ε_K). If the decrements are non-increasing, J(K)−J(K−1)=1−R d_K is non-decreasing, so K*_0(R) is the leftmost minimizer for every R≥0. Conversely, if the decrements are positive and pairwise distinct and some d_m<d_{m+1}, order them d_(1)>⋯>d_(n)>0. For R in (1/d_(m), 1/d_(m+1)) the from-0 count equals m. The point (m, ε_m) lies strictly above the chord from m−1 to m+1, so m is never a minimizer. Without those side conditions the biconditional is false: d=(−2,−1), ε=(−3,−1,0), is not convex, and K*_0(R)=0 is the unique minimizer for every R≥0. The count used in the procedure is K*_0, not N60 as written. The general rule, with or without convexity, is the hull test, whose short proof is already in KEYSTONE_NOTE §4 and is not repeated.

**Observation, degree of a linear kernel.** In the linear time-invariant class the causal memory is a convolution kernel. A finite-dimensional realization has a rational transfer function whose McMillan degree is the number of poles, counted with multiplicity, which is the number of states the system holds. A complex-conjugate pair is two states (CT21). The matrix pencil recovers those poles from uniformly sampled impulse data in the noiseless case (Hua & Sarkar 1990). With noise, ΔBIC ≥ 10 is a heuristic precommitted penalty choice (already in the v2.5.2 placeholder, borrowing the numerical threshold from Kass & Raftery 1995); it is not a regular Bayes-factor theorem here, because close poles make the information matrix singular, 800 samples of a smooth kernel are not iid, and a bounded or failed `least_squares` run need not attain the maximum likelihood. Exponential analysis is ill-posed for close time constants depending on SNR and sample size (Istratov & Vyvenko 1999); the factor-3 merge is a precommitted resolution choice (already in that placeholder, not their limit and not derived from J), and a class may preregister a different factor. The relay test is the operational form of CT16. None of this uses the world's spectrum or the prices, which is what keeps the observation from being a tautology of argmin J.

**Comparison.** THEORY §3 maps the cost band {𝒟 : J(𝒟) ≤ (1 + ε + δ_meas) J*} into design space and already says that a discrete count differs from the predicted one as a miss only if the counted design's J lies outside the band. The functions `cost_band` and `in_cost_band` are that clause.

## 6. Prior art

DOIs below were resolved on Crossref this session (21 November 2026, ET).

- Fox 1966, *Management Science* 13:210, discrete optimization via marginal analysis, doi [10.1287/mnsc.13.3.210](https://doi.org/10.1287/mnsc.13.3.210). The exactness of the adjacent count under non-increasing decrements is this argument. Credit is as an application, not a new tool. (Also the prior-art credit in PR #145.)
- Hua & Sarkar 1990, *IEEE Transactions on Acoustics, Speech, and Signal Processing* 38:814, matrix pencil for exponentially damped sinusoids, doi [10.1109/29.56027](https://doi.org/10.1109/29.56027).
- Golub & Pereyra 1973, *SIAM Journal on Numerical Analysis* 10:413, variable projection for separable nonlinear least squares, doi [10.1137/0710036](https://doi.org/10.1137/0710036).
- Kass & Raftery 1995, *Journal of the American Statistical Association* 90:773, Bayes factors, doi [10.1080/01621459.1995.10476572](https://doi.org/10.1080/01621459.1995.10476572) (also JSTOR 10.2307/2291091). The ΔBIC ≥ 10 gate borrows their numerical threshold as a precommitted penalty choice (already in `figures/face_placements.md`), not a regular Bayes-factor theorem here (§4–§5).
- Istratov & Vyvenko 1999, *Review of Scientific Instruments* 70:1233, exponential analysis in physical phenomena, doi [10.1063/1.1149581](https://doi.org/10.1063/1.1149581). Ill-posedness of recovering close time constants.
- Gavish & Donoho 2014, *IEEE Transactions on Information Theory* 60:5040, hard threshold for singular values, doi [10.1109/TIT.2014.2323359](https://doi.org/10.1109/TIT.2014.2323359). Used only as a heuristic Hankel cross-check, not as K_obs (a Hankel matrix does not have independent noise entries).

The hull identity is already in this repository (`core/KEYSTONE_NOTE.md` §4). The convexity theorems and the peaked failure class are on `main` via PR #145 (`theory/LAYER_CONVEXITY.md`, CLAIM_MAP N64); this note refers to them and does not claim them.

**What is new here, as an assembly of known parts** (a limited search of this repository and of the citations above found no earlier statement of the assembled operational rule; not checked by a specialist): fixing the v2.5.2 placeholder as a testable procedure with a coded observation path, a coded prediction path that branches on the L1 premise rather than always using N60, a cost-band comparison that matches THEORY §3, and synthetic checks that the observation is not a tautology of argmin J. Nothing here is claimed as a new theorem about nature. N56 stays OPEN and untested.

## 7. Code

- `tools/layer_count_rule.py` — `select_bic_degree`, `detect`, `count_layers`, `max_cardinality_match`, `merge_close_states`, `merge_classified`, `classify_local_shared`, `relay_test` on the observation side; `n60_from`, `n60_as_written`, `hull_increment`, `predict_count`, `cost_band`, `in_cost_band` on the prediction side.
- `tools/test_layer_count_rule.py` — exactness and the peaked example; the hull identity on random sequences; merge, classify, and relay helpers; a few well-separated / rhythmic / out-of-band / close-pole detections; the tautology check.
- A short self-check writes `measurement/layer_count/RESULTS.json`.

## 8. Open after this note

- N56 remains OPEN: no qualifying system has had its world, prices, and design measured and counted by this rule.
- T18, a predictive rhythm rule from poles and stakes without first computing ε_K, remains OPEN and deprioritized.
- Model S convexity for J ≥ 3 remains OPEN (numerical only); that is N64 / PR #145, not this note.
- The default resolution factor 3 is a choice, not a derived constant.
- E. coli's published two-pole kernel (Mattingly et al. 2021) is degree 2 and was not selected by this rule; it is still reported, not scored against B.11.
