# Fractal structure and design: which property of a world's records sets K\*? (ht-index as one candidate)

*20 Nov 2026, about 2:40 PM ET; revised about 4:00 PM ET after independent review of PR #116 (reading NOT-READY: three blockers, ten should-fixes; every one addressed below), and confirmed READY. Branch `v2.8-htindex`, PR #116, rebased on `main` at `b12af70` (PR #117 merged as CLAIM_MAP v2.67), CLAIM_MAP v2.68 (rows N58–N63). Written by one executor on Chad's prompt (t2009u: "maybe the records themselves can be viewed as fractal"). Everything below is in-model: simulated worlds and the repo's own optimizer. Nothing here is a claim about nature, and no real data was opened. Status words follow the repo: PROVED (in-model), PRIOR ART, OPEN, MATH-CORRECTED.*

## 0. The answer in five lines

1. **The information that sets the layer count K\* lives in how variance is spread across time scales (the spectrum, relative to the read noise) together with stakes over upkeep R. It does not live in the shape of a record's value distribution.** In the theory's linear-Gaussian class this is exact (§2, N59, N60).
2. **The ht-index of a 1-D record does not estimate K\* or the number of separated scales.** For Gaussian records it is 1 whatever the world under head/tail breaks 1.0 at Jiang's 40% threshold; under the 2.0 rule (Jiang 2019) it is 1 or grows as ln n depending on how that rule is read. For heavy-tailed or exponential records it grows like ln n, the log of the record length (§1, N58); Jiang (2016) treats that growth as intended (ht counts the scales the data resolve). In 108 simulated records with known answers (54 at each length) it matched K\* only where K\* = 1 happened to equal ht = 1 (§3).
3. **A spectral fit fed to the cost does better than any record-shape statistic, but only modestly better than the plain pole count.** Fit the world's spectrum (Whittle likelihood with thresholds borrowed from the counting rule: ΔBIC ≥ 10, factor-3 merge), then run the repo's optimizer on the fit. In the 54 records at n = 2·10⁵ this "plug-in" recovered K\* exactly in 100%, 100%, 96%, 78% and 50% of records at R = 10, 10², 10³, 10⁴ and 10⁶. Against the baselines (§3): the best constant guess gets 100%, 56%, 72%, 56% and 33%, and the raw pole count 13%, 50%, 82%, 78% and 50%. So the plug-in beats the raw pole count only at R ≤ 10³ and ties it at 10⁴ and 10⁶; 100% at R = 10 is trivial (every true K\* is 1). It is also favoured: its model class is exactly the generating class, and it is given the true R. Every miss at high R was an undercount from a record too short for its slowest scale, or modes closer than the factor-3 resolution. These numbers are after the optimizer fix of this revision (§3, `layers_checks/stores.py`); before it they read 94% and 76% at 10³ and 10⁴ and 52% at 10⁶, one of them for the wrong reason.
4. **The Hurst/DFA exponent matters only in scale-free worlds, and only jointly with the span and R.** It sets how much each extra layer is worth there (zero at the random walk, L1). In separated worlds it is about 1 whatever the count. The true multifractal spectrum of a Gaussian process is degenerate, but the MF-DFA width measured here is not zero: it is a crossover-induced bias of the estimator (about 0.08 for one mode, 0.04 for four, at n = 2·10⁶), it does not shrink with n, it depends on the world, and it does not count modes (§3).
5. **Nested agents (Chad's "records are traces of agents").** A record written by an optimized sub-agent mostly shows the *world's* modes, not the agent's K\*: its pole count matched the count of the agent's own input in 67 of 72 optimized records over 12 independent worlds, and the agent's K in only 22 of 72. Reading input and output together (the counting rule's I/O pair) identifies the agent's K, but just as well for random designs as for optimized ones (§5, arm D2), so it identifies a design, not optimization. Interlacing (store j between modes j − 1 and j) holds for every optimized K = 3 design, as CT21/B.9 requires, but that is a theorem, read from the design's parameters; a random design interlaces about 11% of the time by chance, and one random design within 0.31% of the optimum does not interlace. Read from data (I/O-fitted stores against modes fitted from the input), interlacing agreed with the parameters in every case where both fits found three scales (15 of 15), but that was only 15 of 52 K = 3 records. The first version's "I/O recovered K in 11 of 12" and "interlacing 4 of 4 against 0 of 9" were pseudo-replicated (three designs, one world, near-noiseless records) and are withdrawn as evidence (§5, N63 stays OPEN).

**Reading on the idea:** the ht-index, as a count of levels in one record, is **not** a route to K\*. The confound the brief suspected is real, and it is worse than suspected. The deeper intuition behind it does survive in corrected form. K\* *is* a count of "levels that matter", but the levels are spectral modes, and the cut is set by the cost (marginal value of a layer > its upkeep), not by a 40% head rule (§2, N60). No prereg is written: nothing here earns a new field prediction beyond the existing discriminating test N56 and counting rule (§6). N60, the cost-thresholded count, is proved given a convexity premise that is checked numerically only.

## 1. What the ht-index measures

**Definition** (Jiang 2013; Jiang & Yin 2014; "head/tail breaks 1.0"). Split the values at their mean. If the head (values above the mean) is a minority, at most 40% (the threshold of Jiang, Liu & Jia 2013), recurse on the head. ht = 1 + the number of such splits. Head/tail breaks 2.0 (Jiang 2019) applies the 40% threshold to the *average* head fraction of all splits so far instead of to each one; its effect is in (c) below. The code reproduces Jiang & Ma's worked example (Zipf 1, ½, …, 1/10 gives 3).

**Result N58 (PROVED (in-model); the mean-excess facts are PRIOR ART).**
- (a) *Pareto tail, index α > 1.* E[X | X > t] = α t/(α − 1), so each split keeps the exact fraction p(α) = P(X > αt/(α−1) | X > t) = (1 − 1/α)^α, whatever the level. After k splits about n·p^k values remain, so to leading order **ht ≈ 1 + ln n / ln(1/p(α)) + O(1)**. It grows without bound in n, at a slope set by the tail index alone.
- (b) *Exponential, and the deep-tail limit in general.* By the generalized-Pareto limit of excesses (Balkema & de Haan 1974; Pickands 1975), the head fraction at deep splits tends to p = (1 − ξ)^{1/ξ}: e^{−1} ≈ 0.368 for ξ = 0 (the Gumbel domain; exact at every level for the exponential, by memorylessness), the Pareto value for ξ = 1/α ∈ (0, 1), and, for the Weibull domain (ξ < 0, bounded tails), a value that is ½ or more for ξ ≤ −1 (the uniform, ξ = −1, gives ½), so ht = 1 there. This is a limiting deep-tail fraction only. ht grows as ln n only if every earlier split also stays at or below the threshold; the Gaussian (c) is in the Gumbel domain, yet its first split exceeds 0.40, so its ht is 1. For the exponential every split sits at e^{−1}, just below the 40% threshold, so its ht grows as ln n, with a large spread because each fraction lies close to the threshold.
- (c) *Gaussian magnitudes.* The first split of |Z| keeps P(|Z| > √(2/π)) = 2Φ̄(0.798) = **0.4249 > 0.40**, so ht = 1 for every large n. At threshold 0.5 the later fractions fall toward e^{−1} (0.405, 0.396, 0.389, …), and ht then grows as ln n. Whether a Gaussian record has "one level" or "fourteen" is decided by where the threshold sits relative to 0.425. *Head/tail breaks 2.0* (Jiang 2019) does not settle it, because its rule ("while the average head ≤ 40%") can be read two ways (`htlib.ht_index_v2`, `ht_checks/arm_H2.json`, 20 replicates). Checked after every split, the running average starts at 0.425 > 0.40, so ht = 1 at every n. Taken as the longest run of splits whose average is ≤ 0.40 (the running mean 0.425, 0.415, 0.408, 0.404, 0.400, … drops below 0.40 after about five splits), ht grows as ln n: 5.4, 8.7, 11.9 and 14.4 at n = 10³…10⁶. So "ht = 1 for Gaussians" is specific to head/tail breaks 1.0 (and to the step-by-step reading of 2.0). For the exponential and Pareto α = 2, 2.0 adds about 1–1.5 and 0.1–0.5 levels and keeps the same ln n growth.

*Checks* (`ht_checks/arm_A.json`; 30 replicates per cell, n = 10²…10⁶). Measured slopes per decade, against ln 10 / ln(1/p):

| Distribution | p (theory) | slope measured | slope predicted |
|---|---|---|---|
| Pareto α = 1.5 | 0.192 | 1.48 | 1.40 |
| Pareto α = 2 | 0.250 | 1.63 | 1.66 |
| Pareto α = 2.5 | 0.279 | 1.95 | 1.80 |
| Pareto α = 3 | 0.296 | 1.78 | 1.89 |
| exponential | 0.368 | 2.21 | 2.30 |
| lognormal σ = 1 | — | 2.17 | — |
| half-normal | (0.425 first) | 0.00 (ht = 1) | 0 |

The measured slopes are not monotone in α (1.95 at α = 2.5 against 1.78 at α = 3); with 30 replicates per cell and the O(1) term still moving at n ≤ 10⁶, that is within replicate noise, and the predicted values are monotone. The test's tolerance (0.45 per decade) is loose: it checks the order of magnitude of the slope, not its third digit.

**The case head/tail breaks is built for** (`arm_A.json` "cascade"): K size levels 10^k with counts falling as 5^{−k}. With tight levels (within-level lognormal spread σ = 0.1), ht = K for K ≤ 3, and it undercounts at K = 4 (3) and K = 5 (4.3 ± 0.6). With σ = 0.5 or 1, ht no longer tracks K and grows with n (σ = 1: K = 3 gives 5.3, 6.6 and 8.7 at base sizes 10³, 10⁴ and 10⁵). So ht counts levels only when each level is a tight cluster in *value* and the clusters thin out geometrically. Records of change in the theory's worlds are not of that kind (§2).

**What this says about "fractal dimension".** Jiang & Yin's ht is a count, not an exponent. For a pure power law it carries the tail index (through p) and ln n. "Scale-free data have an ht that grows with sample size" is the honest reading. Jiang treats that growth as intended, not as a confound: for the Sierpinski carpet, "If we added 512 squares of the smaller size 1/81, the Ht-index would increase by one, but the fractal dimension would remain unchanged" (Jiang 2016). ht counts the scales the data resolve, by design. For the purpose here, counting the time scales a design should track, that design choice makes it a measure of sample size. The same n-dependence is known for empirical-mode decomposition, which yields about log₂ n modes on fractional Gaussian noise (Flandrin, Rilling & Gonçalvès 2004).

## 2. First principles: what K\* depends on

The setting is Model S (`theory/LAYERS.md`; THEORY CT21): world s = a stationary Gaussian process, read y = s + white noise of density N, and K stores. The cost is J_K = h·K + w·E_K. Write ε_K = E_K/E_∞ − 1 and R = w·E_∞/h.

**Result N59 (Gaussian marginal blindness; PROVED (in-model), elementary; narrow).** Fix one linear read-out of the record: y(t), an increment y(t+δ) − y(t) at one fixed δ, or any other fixed linear functional applied at every time. In this class its one-time distribution is a centred Gaussian, and only its variance depends on the world. The ht-index and the head fractions are invariant to rescaling (ht(cx) = ht(x)). For an ergodic record, the empirical distribution of n such values converges to that marginal. So **every head fraction of that read-out converges to a number that is the same for every world in the class** (0.4249 at the first split of |·|), and ht of |y|, |Δy| or any one linear read-out converges to the same value for every world: 1 at Jiang's threshold. The same holds for any *scale-invariant shape statistic* of that one marginal (tail index, kurtosis, head fractions). It does **not** hold for scale-dependent statistics across several read-outs: the variances of Δ_δ y across δ form the structure function, which carries all the time-scale information. The periodogram ordinates and the mean-crossing durations are non-linear read-outs outside N59, and their failure in §3 is empirical only. Beyond the limit, the world enters through finite-sample fluctuations (how correlated the n values are, an effective sample size); that this channel carries no usable count of modes is **asserted, not proved** here. A sum of separated Gaussian modes is Gaussian. *Proof (of the limit statement only):* linear functionals of a Gaussian process are Gaussian; scale invariance removes the variance; ergodicity (true for sums of OU modes) gives convergence of the empirical head fractions. ∎ The information about time scales is in the two-time structure: the autocovariance, or equivalently the spectrum S(f), which for a stationary Gaussian process determines the law.

**Result N60 (K\* is a cost-thresholded count; PROVED (in-model) given convexity, which is numerical only).** K\* = argmin_K [K + R(1 + ε_K)].
- (i) ε_K depends on the world only through S/N, because it is invariant under (S, N) → (cS, cN).
- (ii) If ε_K is convex and decreasing in K (true in every world computed here, in `layers_checks/` and in the 300 random worlds of `figures/face_collapse_v23.py` V2 within the optimizer's tolerance; the independent review found 39 of 40 further random worlds convex, the fortieth being the optimizer bug fixed in this revision; not proved in general), then **K\* = 1 + #{k ≥ 2 : R·(ε_{k−1} − ε_k) > 1}**: the number of layers whose marginal value exceeds their upkeep.
- (iii) For J separated OU modes ε_J = 0 (L2), so K\* ≤ J, with equality once R passes the last threshold. Each threshold depends on that mode's variance share, its separation from its neighbours, and the signal-to-noise. A count of modes is therefore a ceiling, not an estimate.
- (iv) In a scale-free band, ε_K > 0 for all K (L3), so K\*(R) keeps rising with R and the span. The size of each step is set by α (zero at α = 2, L1; the c(α−2)² knife edge).

*Proof of (ii):* for a convex decreasing sequence the decrements are non-increasing, so K + Rε_K falls while R·(decrement) > 1 and rises afterwards. ∎ This is CX4's "predictive-state dimensions whose marginal value exceeds upkeep" stated concretely inside the linear-Gaussian class. Placement (the store rates b_j) is fixed by the spectral factorization of S + N (L2's proof), so it too is a functional of S/N.

**Correction (N64 / `theory/LAYER_CONVEXITY.md`, `core/KEYSTONE_NOTE.md`).** The from-1 cardinality in (ii), \(K^* = 1 + \#\{k \ge 2 : R\cdot(\varepsilon_{k-1} - \varepsilon_k) > 1\}\), cannot return 0: when the from-0 count \(K^*_0(R) = 0\) it returns 1 (the \(K^*=0\) hole). The from-0 count \(K^*_0(R) = \#\{K \ge 1 : R(\varepsilon_{K-1} - \varepsilon_K) > 1\}\) equals the leftmost argmin of \(K + R(1+\varepsilon_K)\) when the decrements are non-increasing, with a converse under positive distinct decrements. Use \(K^*_0\) when the decrements are non-increasing, and the lower-hull walk otherwise (N65). N60's identity \(K^* = \arg\min_K [K + R(1 + \varepsilon_K)]\) is unchanged.

**So, to the first-principles question.** The property that determines K\* and placement is the noise-normalized spectrum on the band that pays, read through the cost: how much variance sits at each separated scale, how far apart the scales are, and how loud they are against the read noise. Scalar fractal summaries compress this away:
- ht keeps ln n and a tail index;
- H keeps a slope;
- the MF-DFA width keeps an estimator bias set by the crossovers (§3), not a count.

Each can carry information only where the world's structure collapses onto that one number. H in a scale-free band, combined with the span and R, is the one case found here.

## 3. Head to head on 1-D records (arm B)

**Worlds** (`ht_checks/arm_B.json`, `arm_K.json`, `summary.json`). Sums of J = 1–4 OU modes, time constants 1 to 10³, separations ×3, ×10 and ×100, equal variances, read noise sd 0.3 or 1, record lengths n = 2·10⁴ and 2·10⁵ at dt = 0.1, 3 seeds each (108 records: 54 at each length; the K\* and plug-in accuracies below use the 54 at n = 2·10⁵). Scale-free controls: fGn with H = 0.3, 0.5, 0.7 and 0.9, and the repo's dense Lorentzian band with α = 1 and 1.5 over a span of 10³. The true K\*(R) comes from the repo's optimizer (`layers_checks/stores.py`) on the true world.

**Optimizer fix (review S1).** `stores.E_K` minimized an MSE computed with `np.linalg.solve` on the store covariance matrix, with near-coincident stores held apart only by a 10⁻⁹ jitter. When two stores share a rate that matrix is singular, and the solve could return a spuriously low MSE, below the causal minimum E_∞ (reproduced: ε₄ = −1.1·10⁻⁴ in one random world, and ε₄ = −0.19% in one plug-in fit at R = 10⁴). `mse_given_b` now inverts the Jacobi-scaled matrix on its well-conditioned eigen-subspace only, so every value it returns is the MSE of a realizable filter, and `E_K` returns the MSE re-evaluated at the rates it returns. Regression test: `tools/test_ht_index.py::test_store_optimizer_never_below_causal_minimum`. Effect: no plug-in ε is negative now (`summary.json` `plugin_negative_eps` = 0); the plug-in accuracies move from 94/76/52% to 96/78/50% at R = 10³/10⁴/10⁶; `arm_K.json` (the true K\*) is unchanged to every printed digit. Merged results that use the same optimizer were rerun with old and new code: `layers_checks/experiments.py` (LAYERS.md) changes only in a redundant fourth store's placement (excess 0.000% either way) and one store time constant in the fourth digit, so `experiments.out`/`.json` are refreshed and no LAYERS number changes; `face_collapse_v23.py` V2 (300 worlds) gives identical convexity flags and failure count (0.973 convex, 1.000 within tolerance), with one world's E moving by 1.5·10⁻⁵; `meq_checks2.py` and `meq_checks/part2.py` change in the eighth digit only. No merged result relied on the bug.

**Estimators:**
- ht of |Δy|, of |y|, of the periodogram ordinates and of the mean-crossing durations (threshold 0.4, and 0.5 for |Δy|);
- the Whittle pole count of the **world's spectrum** (a one-record spectral fit that borrows the counting rule's thresholds: ΔBIC ≥ 10, band dt to T/10, factor-3 merge). It is not the counting rule: the rule fits a system's I/O response kernel (`figures/face_placements.md` §4), and this fit also differs in using real poles only (no complex pairs or degree counting) and greedy forward ΔBIC. Only arm D's I/O fit is a counting-rule analogue;
- peaks of f·S(f) (`spectral_peak_count` with prominence 0.1 against the function's default 0.15; no record survives of whether 0.1 was fixed before the results were seen, so treat it as possibly tuned);
- the DFA exponent (Peng et al. 1994) and the MF-DFA width h(−3) − h(5) (Kantelhardt et al. 2002);
- the plug-in K\*: the Whittle fit fed to the repo's optimizer, that is, the *prediction* half of N56 (measured spectrum → argmin J), with the true R supplied.

| Estimator (n = 2·10⁵, 54 records) | exact = J | Spearman with J | exact = K\* at R = 10², 10³, 10⁴, 10⁶ |
|---|---|---|---|
| *Best constant guess (modal K\*, chosen with hindsight)* | — | — | *56%, 72%, 56%, 33%* (100% at R = 10) |
| ht \|Δy\|, ht \|y\| (0.4) | 11% (J = 1 only) | — (always 1) | 44%, 17%, 11%, 11% (only where K\* = 1) |
| ht \|Δy\| (0.5) | 0% | 0.12 | 0% (values 10–14, +2.3 per decade of n) |
| ht periodogram | 0% | 0.03 | 0% (values 5–9) |
| ht crossing durations | 0% | 0.05 | 0% |
| Peaks of f·S(f) | 19% | −0.08 | 37%, 44%, 26%, 19% |
| DFA exponent | — | 0.23 | — (≈ 0.7–1.05 in every OU world) |
| MF-DFA width | — | −0.35 | — (−0.04 to 0.10 across these records; a crossover bias of the estimator, see below) |
| Whittle pole count | 50% | 0.68 | 50%, 82%, 78%, 50% (13% at R = 10) |
| **Plug-in K\*** | — | — | **100%, 96%, 78%, 50%** (100% at R = 10, trivially) |

True K\* at n = 2·10⁵ (counts of the 54 records): R = 10, all 1; R = 10², 24 ones and 30 twos; R = 10³, 9/39/6 for K\* = 1/2/3; R = 10⁴, 6/30/15/3 for 1–4; R = 10⁶, 6/18/18/12. **Fairness.** The plug-in is favoured three ways: its Whittle model class (OU modes plus white noise) is exactly the generating class, which no rival gets; R is given, not estimated; and its thresholds (ΔBIC ≥ 10, factor-3 merge, band) are inherited from the counting rule, not tuned on these records (that last point is fair, but stated). Even so, it beats the raw pole count only where K\* is small (R ≤ 10³).

**MF-DFA width does not vanish** (`ht_checks/arm_M.json`, noise 0.3, 3 seeds; reproduces the review's table): one mode (τ = 10), width 0.03–0.06, 0.08–0.09 and 0.07–0.08 at n = 2·10⁴, 2·10⁵ and 2·10⁶; four modes (1–10³), 0.03–0.08, 0.01–0.03 and 0.04 at the same lengths. The spread of segment variances depends on s/τ, and one log-log fit across the crossovers turns that into a q-dependence. So the −0.35 correlation with J is plausibly a real crossover signature, not noise; it still does not count modes.

At n = 2·10⁴ the pole count's Spearman correlation with J falls to 0.42. All its misses are undercounts: the slowest scale is unresolved (T/τ_max ≈ 20 for τ = 10³), or modes are closer than the factor-3 resolution (×3 worlds), which the counting rule merges by design. The plug-in's misses are the same undercounts, appearing at high R where K\* reaches for those scales.

**Scale-free controls** (median of 3 seeds, n = 2·10⁴ → 2·10⁵). The pole count stays at 0 for fGn with H = 0.3 and 0.5. It is 2 → 2 for H = 0.7 (seeds [2, 2, 2] → [2, 3, 2]), 2 → 3 for H = 0.9, 2 → 3 for the α = 1 band and 2 → 2 for the α = 1.5 band. It grows with record length, as L3 says it must: no finite count is exact, and the data decide how many poles are affordable statistically. This is the same n-dependence as ht, but for a reason the theory predicts (L3) and can price (K\*(R) also climbs).

## 4. Many coupled records (arm C; Chad's "the world is many signals")

**Setup** (`ht_checks/arm_C.json`). Six records, n = 2·10⁵, noise 0.3, 3 seeds per world (so each cell below is n = 3, and "8 of 12" is 4 worlds × 3 seeds). True components, as the map counts them (class × scale):
- C1, independent drivers at τ = 1, 10, 100 in every record: 3 local;
- C2, local τ = 1 and 10 plus one common-mode τ = 100: 2 local + 1 shared;
- C3, local τ = 1 plus local *and* shared at τ = 10: 3, with "both" at τ = 10;
- C4, three common-mode drivers: 3 shared;
- C5, each record with its own rates spread within a factor 2.4: no clean truth.

| Count | C1 (3) | C2 (3) | C3 (3) | C4 (3) | Failure mode |
|---|---|---|---|---|---|
| (a) median per-record ht \|y\| / ht periodogram | 1 / 7–8 | 1 / 6–8 | 1 / 7 | 1 / 6–8 | blind (N59) / ln n |
| (b1) sum of per-record pole counts | 17–18 | 17–18 | 12 | 15–18 | **double counting** (about ×M) |
| (b2) per-record counts, union merged within factor 3 | 3, 3, 4 | 4, 4, 3 | 2, 2, 2 | 3, 3, 3 | **misses "both"** (C3); per-record τ scatter across the merge boundary adds one |
| (b3) classify (cross-record coherence) then merge, the counting rule | 3, 3, 4 | 5, 5, 3 | 3, 3, 2 | 3, 3, 3 | best: right in 8 of 12; spurious "both" where one mode's fits straddle the boundary |
| (c1) pole count of the pooled (mean) record | 3 | 2 | 2 | 3, 3, 2 | **misses local structure** (local modes average down as 1/M) |
| (c2) multivariate Hankel-DMD (Schmid 2010), Gavish–Donoho rank | rank 37–39, 0–1 real rates | 37–39, 1–2 | 35–36, 1 | 32–36, 0–2 | as implemented here it fails: fits noise and complex modes. A reading on this implementation, not on DMD or ERA |
| (c3) ht of DMD singular values | 3 | 4 | 4–5 | 4–5 | does not track the components (3) or the state dimension (18, 13, 13, 3) |

**Reading.** The count that tracks the map's truth is the repo's own rule: per-record fits, classify each scale as local or shared, then merge only within a class. Summing per-record counts double-counts shared and repeated structure. Merging without classifying, or pooling, misses structure (the "both" case, or local modes). The ht-index of anything tried here does not track the truth. An integrated multivariate fit is the right idea in principle (one realization, its poles and their sharing pattern). A version that works needs a covariance-based ERA with model-order selection (Ho–Kalman lineage), which is not built here. That stays OPEN (N62).

**Prior art for the multivariate and spatial side.** Jiang's spatial uses of head/tail breaks (natural cities, Jiang & Miao 2015; city structure, Jiang 2015) apply the 1-D method to an attribute of 2-D objects (patch sizes, densities). I found no multivariate head/tail breaks for coupled time series. Eigen-mode time-scale detection: exponential analysis and its ill-conditioning (Istratov & Vyvenko 1999); DMD (Schmid 2010); optimal SVD truncation (Gavish & Donoho 2014, used here). The Ho–Kalman/ERA realization line is credited from general knowledge, and its DOIs were not checked this session.

## 5. Records made by nested agents (arms D and D2; a hypothesis, not a framing)

**Hypothesis tested.** The hierarchy in a layer's record is the footprint of the nested, cost-optimized sub-agents that wrote it (CT34: a team's optimized cost is its parent's upkeep).

**First run, arm D (`ht_checks/arm_D.json`; kept as run, now read as a pilot).** One world (OU modes at τ = 1, 30 and 900, input noise sd 0.5, dt = 0.25, n = 4·10⁵), the optimizer's K = 1, 2, 3 designs (store time constants 0.38; 0.29 and 6.7; 0.29, 5.6 and 167), each repeated over 4 noise seeds, record noise sd 0.01 (near noiseless), and 24 random designs. The first version reported "I/O recovered K in 11 of 12 optimized agents" and "interlacing 4 of 4 optimized against 0 of 9 random at K = 3". The independent review showed both are pseudo-replicated and not measured from data: the 12 are 3 designs × 4 seeds in one world; the interlacing flag was computed from the design's true rates and the true modes, so "4 of 4" is one design whose outcome the CT21/B.9 theorem fixes; under the null's log-uniform rates a random K = 3 design interlaces with probability about 0.10, so 0 of 9 has probability about 0.37 with no effect; and one random K = 3 design (τ 0.41, 1.07, 4.65) is within 0.74% of E_∞ and does not interlace. **Those two numbers are withdrawn as evidence.** Arm D's other columns (ht blind; record-only pole count 3 for every optimized design) stand as a pilot.

**Redo, arm D2 (`ht_checks/arm_D2.json`, `arms.py D2`).** 12 independent worlds, each three OU modes with time constants log-uniform in 0.5–500 (neighbours at least ×4 apart) and Dirichlet(2) variance shares, input noise sd 0.5, dt = 0.25, n = 2·10⁵. Per world: the optimizer's K = 1, 2 and 3 designs (36 distinct optimized designs) and 3 random designs (K uniform on 1–3, rates log-uniform over the band, weights tuned; excess error 0.3% to 890%). Each design is run at two record-noise levels, sd 0.1 and 0.3 of the clean record's sd (144 records). Everything below is read from data: record-only and input-only Whittle counts, the I/O fit of (input, record), and interlacing computed from the I/O-fitted store time constants against the modes fitted from the input record, whenever both fits find three scales.

| Measure (D2) | Optimized designs | Random designs | Reading |
|---|---|---|---|
| Record-only pole count = count of the agent's own input | 67 of 72 | 15 of 72 | an optimized record reports its **world** (as the input's fit sees it) |
| Record-only pole count = agent's K | 22 of 72 | 27 of 72 | does not read the agent |
| I/O fit recovers the agent's K, record noise 0.1 / 0.3 | 31 of 36 / 25 of 36 (K = 3: 9 / 3 of 12) | 31 of 36 / 28 of 36 | identifies **a design**, optimized or not; degrades with record noise, worst for three stores |
| Interlacing from the design's parameters, K = 3 | 12 of 12 (the CT21/B.9 theorem) | 2 of 14 (chance about 0.11 per design) | a property of the optimum, not a test |
| Near-optimal random design | — | one K = 3 design at 0.31% excess does not interlace | interlacing does not mark near-optimal designs |
| Interlacing from data (I/O stores vs input modes), when both fits find 3 | 9 of 9 interlaced (6 at noise 0.1, 3 at 0.3) | 0 of 6 | agrees with the parameter value in 15 of 15 cases; computable in only 15 of 52 K = 3 records |

**Reading.** In this model the hierarchy in a record does **not** match the K\* of the agent that wrote it; read alone, an optimized agent's record reports its world. An I/O fit reads the agent's design, but it reads random designs as well as optimized ones, so it is a measurement of a design, not a signature of optimization. Interlacing is the candidate signature, and it can be read from data, but here only in a minority of records (the fits must resolve all three scales on both sides), the sample is small (9 optimized against 6 random designs where it was computable), and a near-optimal design can fail it. So the data support "interlacing from I/O pairs is recoverable when the fits resolve every scale"; they do not yet show that it separates selected from unselected designs in practice. This still supports the counting rule's insistence on a fixed input/output pair (`figures/face_placements.md` §4 step 1) and argues against inferring layers from output records alone. Not done: a second nesting level (a parent tracking the team's record with its own optimized design), non-Gaussian or jump records (where N59 does not apply), and enough near-optimal random designs to estimate how often near-optimal means interlaced. Status OPEN (N63), exploratory and not locked.

## 6. Why there is no prereg, and what variant might work

A field prediction "the ht-index of a system's record equals its layer count" is ruled out in the linear-Gaussian class by N59 before any data, and for heavy-tailed records it would mostly measure ln n (N58). So **N61 is MATH-CORRECTED**, with the replacement below. Variants worth keeping, none preregistered:
- **The plug-in K\*** (fit the spectrum on the class's band, then run the optimizer). This is the prediction half of N56 (measured spectrum → argmin J), with thresholds borrowed from the counting rule, not a new prediction. §3 measures how long a record it needs: about 200 times the slowest time constant to count it reliably.
- **Interlacing from I/O pairs** as a candidate signature of optimization, distinct from counting. Arm D2 shows it can be read from data when the fits resolve every scale, not that it separates selected from unselected designs (one near-optimal random design fails it). It could become a prereg only after a sim with many near-optimal non-optimized designs and a class with measured I/O kernels that passes MV1–MV10. It would sharpen N56; that is OPEN.
- **Event records, not signals.** Where a system's record really is a cascade of tight size classes (§1 cascade), ht can count levels. Whether any strongly selected system writes such records, and whether those levels are layers in the theory's sense rather than member-axis levels (pooling), is unexamined.
- **Heavy-tailed, non-Gaussian worlds** (jumps, Lévy, CT18-H with H = 1/α_s). N59 does not apply there, and the tail index enters the survival buffer (CT25). The ht-index then estimates the tail index (through p(α) and n, N58), which matters for **buffers**, not for layer counts. This links to the robustness work (PR #115, merged as `1998a2d`), but only as an estimator of α_s with a known n-bias. Clauset, Shalizi & Newman's (2009) maximum-likelihood estimator does the same job without that bias.

## 7. Prior art (each DOI checked on Crossref, 20 Nov 2026; Jiang 2016 and 2019 added in the review revision)

- Jiang, B. (2013). Head/tail breaks: a new classification scheme for data with a heavy-tailed distribution. *Prof. Geogr.* 65:482–494. 10.1080/00330124.2012.700499
- Jiang, B., Liu, X. & Jia, T. (2013). Scaling of geographic space as a universal rule for map generalization. *Ann. AAG* 103:844–855. 10.1080/00045608.2013.765773 (the 40% threshold, as cited by the classInt vignette)
- Jiang, B. & Yin, J. (2014; online 2013). Ht-index for quantifying the fractal or scaling structure of geographic features. *Ann. AAG* 104:530–540. 10.1080/00045608.2013.834239
- Jiang, B. (2015). Head/tail breaks for visualization of city structure and dynamics. *Cities* 43:69–77. 10.1016/j.cities.2014.11.013
- Jiang, B. (2015; online 2014). Geospatial analysis requires a different way of thinking: the problem of spatial heterogeneity. *GeoJournal* 80:1–13. 10.1007/s10708-014-9537-y ("third definition of fractal": ht ≥ 3)
- Jiang, B. & Miao, Y. (2015; online 2014). The evolution of natural cities from the perspective of location-based social media. *Prof. Geogr.* 67:295–306. 10.1080/00330124.2014.968886
- Jiang, B. (2016). Head/tail breaks for visualization of city structure and dynamics. In *European Handbook of Crowdsourced Geographic Information*, Ubiquity Press. 10.5334/bax.m (ht grows by one per added smaller scale, by design; quoted in §1)
- Jiang, B. (2019). A recursive definition of goodness of space for bridging the concepts of space and place for sustainability. *Sustainability* 11:4091. 10.3390/su11154091 (head/tail breaks 2.0: the 40% threshold on the average head)
- Jiang, B. & Ma, D. (2018). How complex is a fractal? Head/tail breaks and fractional hierarchy. *J. Geovis. Spat. Anal.* 2. 10.1007/s41651-017-0009-z (fractional ht; Zipf example used as a code check)
- Balkema, A. A. & de Haan, L. (1974). Residual life time at great age. *Ann. Probab.* 2:792–804. 10.1214/aop/1176996548
- Pickands, J. III (1975). Statistical inference using extreme order statistics. *Ann. Stat.* 3:119–131. 10.1214/aos/1176343003
- Embrechts, P., Klüppelberg, C. & Mikosch, T. (1997). *Modelling Extremal Events.* Springer. 10.1007/978-3-642-33483-2 (mean-excess functions)
- Clauset, A., Shalizi, C. R. & Newman, M. E. J. (2009). Power-law distributions in empirical data. *SIAM Rev.* 51:661–703. 10.1137/070710111
- Hurst, H. E. (1951). Long-term storage capacity of reservoirs. *Trans. ASCE* 116:770–799. 10.1061/TACEAT.0006518
- Mandelbrot, B. B. & Van Ness, J. W. (1968). Fractional Brownian motions, fractional noises and applications. *SIAM Rev.* 10:422–437. 10.1137/1010093
- Peng, C.-K. et al. (1994). Mosaic organization of DNA nucleotides. *Phys. Rev. E* 49:1685–1689. 10.1103/PhysRevE.49.1685 (DFA)
- Kantelhardt, J. W. et al. (2001). Detecting long-range correlations with detrended fluctuation analysis. *Physica A* 295:441–454. 10.1016/S0378-4371(01)00144-3 (crossovers)
- Kantelhardt, J. W. et al. (2002). Multifractal detrended fluctuation analysis of nonstationary time series. *Physica A* 316:87–114. 10.1016/S0378-4371(02)01383-3
- Huang, N. E. et al. (1998). The empirical mode decomposition and the Hilbert spectrum… *Proc. R. Soc. A* 454:903–995. 10.1098/rspa.1998.0193
- Flandrin, P., Rilling, G. & Gonçalvès, P. (2004). Empirical mode decomposition as a filter bank. *IEEE SPL* 11:112–114. 10.1109/LSP.2003.821662
- Istratov, A. A. & Vyvenko, O. F. (1999). Exponential analysis in physical phenomena. *Rev. Sci. Instrum.* 70:1233–1257. 10.1063/1.1149581
- Schmid, P. J. (2010). Dynamic mode decomposition of numerical and experimental data. *J. Fluid Mech.* 656:5–28. 10.1017/S0022112010001217
- Gavish, M. & Donoho, D. L. (2014). The optimal hard threshold for singular values is 4/√3. *IEEE Trans. Inf. Theory* 60:5040–5053. 10.1109/TIT.2014.2323359
- Whittle likelihood, Kalman–Bucy and Wiener–Hopf factorization: standard, used as in `theory/LAYERS.md`, not re-read here.

**Novelty.** I found no published derivation of ht ≈ 1 + ln n/ln(1/p(α)), nor of the Gaussian ht = 1 knife edge at 0.4249 (the independent review's search found none either). Both are elementary consequences of the mean-excess facts above, and may exist somewhere. N60 is a restatement of CX4 inside the linear-Gaussian class. Nothing here is claimed as new beyond that.

## 8. Files and how to rerun

`theory/ht_checks/`:
- `htlib.py`: ht-index (1.0, and 2.0 in two readings), worlds, Whittle counter, DFA/MF-DFA, peaks, Hankel-DMD;
- `arms.py`: arms A, B, K, C and D (first run), and the review-revision arms D2 (nested agents redone), M (MF-DFA width against n) and H2 (head/tail breaks 2.0); `nice -n 19 python3 arms.py A B K C D D2 M H2`, about 40 min on 6 cores;
- `analyse.py`: writes `summary.json`;
- `arm_*.json`, `summary.json`: the saved outputs.

Test: `tools/test_ht_index.py` (fast checks of N58 and N59, the optimizer regression, ht 2.0, and the saved headline numbers). Seeds are fixed. Whittle fits use multi-start Nelder–Mead, so a rerun can differ by a seed or two in the counts.
