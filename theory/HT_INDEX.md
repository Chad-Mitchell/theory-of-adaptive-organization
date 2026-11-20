# Fractal structure and design: which property of a world's records sets K\*? (ht-index as one candidate)

*20 Nov 2026, about 2:40 PM ET. Branch `v2.8-htindex`, draft PR, CLAIM_MAP v2.67 (rows N58–N63). Written by one executor on Chad's prompt (t2009u: "maybe the records themselves can be viewed as fractal"), a self-check, **not independently reviewed**. Everything below is in-model: simulated worlds and the repo's own optimizer. Nothing here is a claim about nature, and no real data was opened. Status words follow the repo: PROVED (in-model), PRIOR ART, OPEN, MATH-CORRECTED.*

## 0. The answer in five lines

1. **The information that sets the layer count K\* lives in how variance is spread across time scales (the spectrum, relative to the read noise) together with stakes over upkeep R. It does not live in the shape of a record's value distribution.** In the theory's linear-Gaussian class this is exact (§2, N59, N60).
2. **The ht-index of a 1-D record does not estimate K\* or the number of separated scales.** For Gaussian records it is 1 whatever the world, at Jiang's 40% threshold. For heavy-tailed or exponential records it grows like ln n, the log of the record length (§1, N58). In 108 simulated records with known answers (54 at each length) it matched K\* only where K\* = 1 happened to equal ht = 1 (§3).
3. **What works is a spectral fit fed to the cost.** Fit the spectrum (Whittle likelihood, the counting rule's ΔBIC ≥ 10 and factor-3 merge), then run the repo's optimizer on the fit. This "plug-in" recovered K\* exactly in 100% of records at R ≤ 100, 94% at R = 10³, 76% at 10⁴ and 52% at 10⁶. Every miss at high R was an undercount from a record too short for its slowest scale, or modes closer than the factor-3 resolution. The plain pole count is only a ceiling (K\* ≤ J, L2).
4. **The Hurst/DFA exponent matters only in scale-free worlds, and only jointly with the span and R.** It sets how much each extra layer is worth there (zero at the random walk, L1). In separated worlds it is about 1 whatever the count. The multifractal width is zero in principle for Gaussian worlds, so any correlation it shows is a finite-sample artefact.
5. **Nested agents (Chad's "records are traces of agents").** A record written by an optimized sub-agent shows the *world's* modes, not the agent's K\*. Optimized agents with K = 1, 2 and 3 all left records with three poles. The agent's footprint shows up only when its input and output are read together (the counting rule's I/O pair): the I/O fit recovered K in 11 of 12 optimized agents, and the interlacing signature separated optimized agents from random ones, 4 of 4 against 0 of 9 at K = 3 (§5, N63).

**Verdict on the idea:** the ht-index, as a count of levels in one record, is **not** a route to K\*. The confound the brief suspected is real, and it is worse than suspected. The deeper intuition behind it does survive in corrected form. K\* *is* a count of "levels that matter", but the levels are spectral modes, and the cut is set by the cost (marginal value of a layer > its upkeep), not by a 40% head rule (§2, N60). No prereg is written: nothing here earns a new field prediction beyond the existing killing test N56 and counting rule (§6).

## 1. What the ht-index measures

**Definition** (Jiang 2013; Jiang & Yin 2014). Split the values at their mean. If the head (values above the mean) is a minority, at most 40% (the threshold of Jiang, Liu & Jia 2013), recurse on the head. ht = 1 + the number of such splits. The code reproduces Jiang & Ma's worked example (Zipf 1, ½, …, 1/10 gives 3).

**Result N58 (PROVED (in-model); the mean-excess facts are PRIOR ART).**
- (a) *Pareto tail, index α > 1.* E[X | X > t] = α t/(α − 1), so each split keeps the exact fraction p(α) = P(X > αt/(α−1) | X > t) = (1 − 1/α)^α, whatever the level. After k splits about n·p^k values remain, so to leading order **ht ≈ 1 + ln n / ln(1/p(α)) + O(1)**. It grows without bound in n, at a slope set by the tail index alone.
- (b) *Exponential and the whole Gumbel domain.* Memorylessness (exponential), or the generalized-Pareto limit of excesses (Balkema & de Haan 1974; Pickands 1975), gives p → e^{−1} ≈ 0.368 (shape ξ = 0), and p → (1 − ξ)^{1/ξ} for ξ = 1/α ∈ (0, 1). The 40% threshold sits just above e^{−1}. So exponential-like data are counted as "heavy-tailed" and their ht grows as ln n, with a large spread because each split's fraction lies close to the threshold.
- (c) *Gaussian magnitudes.* The first split of |Z| keeps P(|Z| > √(2/π)) = 2Φ̄(0.798) = **0.4249 > 0.40**, so ht = 1 for every large n. At threshold 0.5 the later fractions fall toward e^{−1} (0.405, 0.396, 0.389, …), and ht then grows as ln n. Whether a Gaussian record has "one level" or "fourteen" is decided by where the threshold sits relative to 0.425.

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

**The case head/tail breaks is built for** (`arm_A.json` "cascade"): K size levels 10^k with counts falling as 5^{−k}. With tight levels (within-level lognormal spread σ = 0.1), ht = K for K ≤ 3, and it undercounts at K = 4 (3) and K = 5 (4.3 ± 0.6). With σ = 0.5 or 1, ht no longer tracks K and grows with n (σ = 1: K = 3 gives 5.3, 6.6 and 8.7 at base sizes 10³, 10⁴ and 10⁵). So ht counts levels only when each level is a tight cluster in *value* and the clusters thin out geometrically. Records of change in the theory's worlds are not of that kind (§2).

**What this says about "fractal dimension".** Jiang & Yin's ht is a count, not an exponent. For a pure power law it carries the tail index (through p) and ln n. "Scale-free data have an ht that grows with sample size" is the honest reading. This is the same confound known for empirical-mode decomposition, which yields about log₂ n modes on fractional Gaussian noise (Flandrin, Rilling & Gonçalvès 2004).

## 2. First principles: what K\* depends on

The setting is Model S (`theory/LAYERS.md`; THEORY CT21): world s = a stationary Gaussian process, read y = s + white noise of density N, and K stores. The cost is J_K = h·K + w·E_K. Write ε_K = E_K/E_∞ − 1 and R = w·E_∞/h.

**Result N59 (Gaussian marginal blindness; PROVED (in-model), elementary).** In this class the one-time distribution of y(t), of an increment y(t+δ) − y(t), or of any fixed linear functional of the record is a centred Gaussian, and only its variance depends on the world. The ht-index and the head fractions are invariant to rescaling (ht(cx) = ht(x)). For an ergodic record, the empirical distribution of n such values converges to that marginal. So **every head fraction converges to a number that is the same for every world in the class** (0.4249 at the first split of |·|), and ht of |y|, |Δy| or any linear read-out converges to the same value for every world: 1 at Jiang's threshold. The world (J, rates, noise, K\*) can enter only through finite-sample fluctuations, that is, through how correlated the n values are (an effective sample size). That channel carries no count of modes. The same holds for any statistic of the one-time marginal (tail index, kurtosis). A sum of separated Gaussian modes is Gaussian. *Proof:* linear functionals of a Gaussian process are Gaussian; scale invariance removes the variance; ergodicity (true for sums of OU modes) gives convergence of the empirical head fractions. ∎ The information about time scales is in the two-time structure: the autocovariance, or equivalently the spectrum S(f), which for a stationary Gaussian process determines the law.

**Result N60 (K\* is a cost-thresholded count; PROVED (in-model), elementary; the convexity premise is numerical).** K\* = argmin_K [K + R(1 + ε_K)].
- (i) ε_K depends on the world only through S/N, because it is invariant under (S, N) → (cS, cN).
- (ii) If ε_K is convex and decreasing in K (true in every world computed here and in `layers_checks/`, not proved in general), then **K\* = 1 + #{k ≥ 2 : R·(ε_{k−1} − ε_k) > 1}**: the number of layers whose marginal value exceeds their upkeep.
- (iii) For J separated OU modes ε_J = 0 (L2), so K\* ≤ J, with equality once R passes the last threshold. Each threshold depends on that mode's variance share, its separation from its neighbours, and the signal-to-noise. A count of modes is therefore a ceiling, not an estimate.
- (iv) In a scale-free band, ε_K > 0 for all K (L3), so K\*(R) keeps rising with R and the span. The size of each step is set by α (zero at α = 2, L1; the c(α−2)² knife edge).

*Proof of (ii):* for a convex decreasing sequence the decrements are non-increasing, so K + Rε_K falls while R·(decrement) > 1 and rises afterwards. ∎ This is CX4's "predictive-state dimensions whose marginal value exceeds upkeep" stated concretely inside the linear-Gaussian class. Placement (the store rates b_j) is fixed by the spectral factorization of S + N (L2's proof), so it too is a functional of S/N.

**So, to the first-principles question.** The property that determines K\* and placement is the noise-normalized spectrum on the band that pays, read through the cost: how much variance sits at each separated scale, how far apart the scales are, and how loud they are against the read noise. Scalar fractal summaries compress this away:
- ht keeps ln n and a tail index;
- H keeps a slope;
- the multifractal width keeps nothing in Gaussian worlds.

Each can carry information only where the world's structure collapses onto that one number. H in a scale-free band, combined with the span and R, is the one case found here.

## 3. Head to head on 1-D records (arm B)

**Worlds** (`ht_checks/arm_B.json`, `arm_K.json`, `summary.json`). Sums of J = 1–4 OU modes, time constants 1 to 10³, separations ×3, ×10 and ×100, equal variances, read noise sd 0.3 or 1, record lengths n = 2·10⁴ and 2·10⁵ at dt = 0.1, 3 seeds each (108 records). Scale-free controls: fGn with H = 0.3, 0.5, 0.7 and 0.9, and the repo's dense Lorentzian band with α = 1 and 1.5 over a span of 10³. The true K\*(R) comes from the repo's optimizer (`layers_checks/stores.py`) on the true world.

**Estimators:**
- ht of |Δy|, of |y|, of the periodogram ordinates and of the mean-crossing durations (threshold 0.4, and 0.5 for |Δy|);
- the Whittle pole count (counting-rule proxy: ΔBIC ≥ 10, band dt to T/10, factor-3 merge);
- peaks of f·S(f);
- the DFA exponent (Peng et al. 1994) and the MF-DFA width h(−3) − h(5) (Kantelhardt et al. 2002);
- the plug-in K\*: the Whittle fit fed to the repo's optimizer.

| Estimator (n = 2·10⁵) | exact = J | Spearman with J | exact = K\* at R = 10², 10³, 10⁴, 10⁶ |
|---|---|---|---|
| ht \|Δy\|, ht \|y\| (0.4) | 11% (J = 1 only) | — (always 1) | 44%, 17%, 11%, 11% (only where K\* = 1) |
| ht \|Δy\| (0.5) | 0% | 0.12 | 0% (values 10–14, +2.3 per decade of n) |
| ht periodogram | 0% | 0.03 | 0% (values 5–9) |
| ht crossing durations | 0% | 0.05 | 0% |
| Peaks of f·S(f) | 19% | −0.08 | 37%, 44%, 26%, 19% |
| DFA exponent | — | 0.23 | — (≈ 0.7–1.05 in every OU world) |
| MF-DFA width | — | −0.35 | — (≈ 0; correlation is a finite-sample artefact) |
| Whittle pole count | 50% | 0.68 | 50%, 82%, 78%, 50% |
| **Plug-in K\*** | — | — | **100%, 94%, 76%, 52%** (100% at R = 10) |

At n = 2·10⁴ the pole count's Spearman correlation with J falls to 0.42. All its misses are undercounts: the slowest scale is unresolved (T/τ_max ≈ 20 for τ = 10³), or modes are closer than the factor-3 resolution (×3 worlds), which the counting rule merges by design. The plug-in's misses are the same undercounts, appearing at high R where K\* reaches for those scales.

**Scale-free controls.** The pole count stays at 0 for fGn with H = 0.3 and 0.5. It is 2 → 3 (n = 2·10⁴ → 2·10⁵) for H = 0.7 and 0.9, and 2 → 3 for the α = 1 band. It grows with record length, as L3 says it must: no finite count is exact, and the data decide how many poles are affordable statistically. This is the same n-dependence as ht, but for a reason the theory predicts (L3) and can price (K\*(R) also climbs).

## 4. Many coupled records (arm C; Chad's "the world is many signals")

**Setup** (`ht_checks/arm_C.json`). Six records, n = 2·10⁵, noise 0.3, 3 seeds. True components, as the map counts them (class × scale):
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
| (c2) multivariate Hankel-DMD (Schmid 2010), Gavish–Donoho rank | rank 37–39, 0–1 real rates | 37–39, 1–2 | 35–36, 1 | 32–36, 0–2 | as implemented here it fails: fits noise and complex modes. A verdict on this implementation, not on DMD or ERA |
| (c3) ht of DMD singular values | 3 | 4 | 4–5 | 4–5 | does not track the components (3) or the state dimension (18, 13, 13, 3) |

**Reading.** The count that tracks the map's truth is the repo's own rule: per-record fits, classify each scale as local or shared, then merge only within a class. Summing per-record counts double-counts shared and repeated structure. Merging without classifying, or pooling, misses structure (the "both" case, or local modes). The ht-index of anything tried here does not track the truth. An integrated multivariate fit is the right idea in principle (one realization, its poles and their sharing pattern). A version that works needs a covariance-based ERA with model-order selection (Ho–Kalman lineage), which is not built here. That stays OPEN (N62).

**Prior art for the multivariate and spatial side.** Jiang's spatial uses of head/tail breaks (natural cities, Jiang & Miao 2015; city structure, Jiang 2015) apply the 1-D method to an attribute of 2-D objects (patch sizes, densities). I found no multivariate head/tail breaks for coupled time series. Eigen-mode time-scale detection: exponential analysis and its ill-conditioning (Istratov & Vyvenko 1999); DMD (Schmid 2010); optimal SVD truncation (Gavish & Donoho 2014, used here). The Ho–Kalman/ERA realization line is credited from general knowledge, and its DOIs were not checked this session.

## 5. Records made by nested agents (arm D; a hypothesis, not a framing)

**Hypothesis tested.** The hierarchy in a layer's record is the footprint of the nested, cost-optimized sub-agents that wrote it (CT34: a team's optimized cost is its parent's upkeep).

**Setup** (`ht_checks/arm_D.json`). World: three OU modes at τ = 1, 30 and 900, noise sd 0.5, dt = 0.25, n = 4·10⁵. The sub-agents' optimal designs come from the repo's optimizer:
- K\*(R) = 1, 1, 2, 3, 3, 3 at R = 1, 10, 10², 10³, 10⁴, 10⁶;
- store time constants 0.38 (K = 1); 0.29 and 6.7 (K = 2); 0.29, 5.6 and 167 (K = 3).

The record is the agent's output, Σ g_k·(exponential store k of y). Null: 24 random designs (K uniform on 1–3, rates log-uniform over the band, weights tuned to those rates); their excess error ranges from 0.7% to 383%.

| Measured on | Optimized K = 1 / 2 / 3 (4 seeds each) | Random | Tracks agent K? |
|---|---|---|---|
| ht \|Δrecord\|, ht \|record\| | 1 / 1 / 1 | 1 | no (N59) |
| ht periodogram / crossings | 6–8 / 7–10 | 4–8 / 2–9 | no |
| Whittle pole count of the record alone | **3 / 3 / 3** (the world's modes, about 1, 30, 600–1600) | 0–3, often fewer | no: optimized records show the *world*, because optimal stores are fast and pass the modes through |
| DFA exponent of the record | 1.0 / 1.0 / 1.0 | 1.02–1.62 | no; it separates "faithful" from "smoothing" designs, not K |
| **I/O identification** (input y and record) | **1 / 2 (one seed 3) / 3**, rates recovered (0.38; 0.29, 6.7; 0.29, 5.6, 166) | noisy where stores nearly coincide | **yes**, 11 of 12 optimized |
| Interlacing (CT21/B.9: store j faster than mode j, slower than mode j − 1) at K = J = 3 | 4 of 4 | 0 of 9 | separates optimized from random |

**Reading.** In this model the hierarchy in a record does **not** match the K\* of the agents that wrote it. Read alone, the record of an optimized agent reports its world. Optimization leaves its mark in two places only: the agent's transfer function, readable from its I/O pair, and where its poles sit (interlacing). That supports the counting rule's insistence on a fixed input/output pair (`figures/face_placements.md` §4 step 1). It argues against inferring layers from output records alone. Not done: a second nesting level (a parent tracking the team's record with its own optimized design), and non-Gaussian or jump records, where N59 does not apply. Status OPEN (N63), exploratory and not locked.

## 6. Why there is no prereg, and what variant might work

A field prediction "the ht-index of a system's record equals its layer count" is ruled out in the linear-Gaussian class by N59 before any data, and for heavy-tailed records it would mostly measure ln n (N58). So **N61 is MATH-CORRECTED**, with the replacement below. Variants worth keeping, none preregistered:
- **The plug-in K\*** (fit the spectrum on the class's band, then run the optimizer). This is the counting rule plus N56's killing test, not a new prediction. §3 measures how long a record it needs: about 200 times the slowest time constant to count it reliably.
- **Interlacing from I/O pairs** as a signature of optimization, distinct from counting. It could become a prereg once a class with measured I/O kernels passes MV1–MV10. It would sharpen N56; that is OPEN.
- **Event records, not signals.** Where a system's record really is a cascade of tight size classes (§1 cascade), ht can count levels. Whether any strongly selected system writes such records, and whether those levels are layers in the theory's sense rather than member-axis levels (pooling), is unexamined.
- **Heavy-tailed, non-Gaussian worlds** (jumps, Lévy, CT18-H with H = 1/α_s). N59 does not apply there, and the tail index enters the survival buffer (CT25). The ht-index then estimates the tail index (through p(α) and n, N58), which matters for **buffers**, not for layer counts. This links to the robustness work on open PR #115, but only as an estimator of α_s with a known n-bias. Clauset, Shalizi & Newman's (2009) maximum-likelihood estimator does the same job without that bias.

## 7. Prior art (each DOI checked on Crossref this session, 20 Nov 2026)

- Jiang, B. (2013). Head/tail breaks: a new classification scheme for data with a heavy-tailed distribution. *Prof. Geogr.* 65:482–494. 10.1080/00330124.2012.700499
- Jiang, B., Liu, X. & Jia, T. (2013). Scaling of geographic space as a universal rule for map generalization. *Ann. AAG* 103:844–855. 10.1080/00045608.2013.765773 (the 40% threshold, as cited by the classInt vignette)
- Jiang, B. & Yin, J. (2014; online 2013). Ht-index for quantifying the fractal or scaling structure of geographic features. *Ann. AAG* 104:530–540. 10.1080/00045608.2013.834239
- Jiang, B. (2015). Head/tail breaks for visualization of city structure and dynamics. *Cities* 43:69–77. 10.1016/j.cities.2014.11.013
- Jiang, B. (2015; online 2014). Geospatial analysis requires a different way of thinking: the problem of spatial heterogeneity. *GeoJournal* 80:1–13. 10.1007/s10708-014-9537-y ("third definition of fractal": ht ≥ 3)
- Jiang, B. & Miao, Y. (2015; online 2014). The evolution of natural cities from the perspective of location-based social media. *Prof. Geogr.* 67:295–306. 10.1080/00330124.2014.968886
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

**Novelty.** I found no published derivation of ht ≈ 1 + ln n/ln(1/p(α)), nor of the Gaussian ht = 1 knife edge at 0.4249. Both are elementary consequences of the mean-excess facts above, and may exist somewhere. N60 is a restatement of CX4 inside the linear-Gaussian class. Nothing here is claimed as new beyond that.

## 8. Files and how to rerun

`theory/ht_checks/`:
- `htlib.py`: ht-index, worlds, Whittle counter, DFA/MF-DFA, peaks, Hankel-DMD;
- `arms.py`: arms A, B, K, C and D; `nice -n 19 python3 arms.py A B K C D`, about 15 min on 6 cores;
- `analyse.py`: writes `summary.json`;
- `arm_*.json`, `summary.json`: the saved outputs.

Test: `tools/test_ht_index.py` (fast checks of N58 and N59, and the saved headline numbers). Seeds are fixed. Whittle fits use multi-start Nelder–Mead, so a rerun can differ by a seed or two in the counts.
