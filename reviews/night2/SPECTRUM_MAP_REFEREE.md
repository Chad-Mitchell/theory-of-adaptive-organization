# SPECTRUM_MAP — hostile independent referee report

Referee: executor `spectrum-map-referee` (Grok Bot, for Chad via Ace), Sunday 15 Nov 2026, 09:27–09:55 AM ET (America/New_York).
Object: `reviews/night2/SPECTRUM_MAP/` at merge `2c0c56e` (PR #9): README, PREREG_D3S, all of `checks/`; THEORY.md v1.3 §2 and §2.5.
Standard: physicist/mathematician; summaries not trusted; every load-bearing number re-derived or re-run. Referee scripts and
outputs: `reviews/night2/SPECTRUM_MAP_REFEREE_checks/` (r1–r7, run at nice 19; numpy/scipy only). Private; nothing sent or posted.
Every citation below was opened or resolved this session (Crossref/OpenAlex/arXiv); none is from memory.

## 0. Verdicts in one table

| # | Claim | Verdict | One line |
|---|---|---|---|
| 1 | Read-rate exponent 1/(1+2H) holds for the optimal fBm predictor; constant drops 11–19% | **CONFIRMED** (one wording correction) | Self-similarity proof is right; κ_opt/κ_hold = 0.886 (H=¼), 0.808 (H=¾), stable in P; but "whatever linear predictor" is false for fixed-timescale predictors |
| 2 | Noisy sensing: e\* = q^{1/α}N^{1−1/α}/sin(π/α) (Afterman et al. 2022); elasticities α/(2α−1), 1/(2α−1) | **CONFIRMED** (citation real and says it; elasticities are the executor's elementary corollary, not the paper's) | One caveat on the paper's Remark 2.6 |
| 3 | Kernel tail τ^{−(1+α/2)}, negative weights for α > 2 (Nuzman & Poor 2000; Hosking 1981) | **CONFIRMED / PRIOR ART** for the tail and the sign; **CORRECTED** for the inference drawn in §2.5(iii) | The "hazards, not kernels" conclusion compares a density exponent with retention curves; the survival of the kernel decays as τ^{−α/2}, which can fall in 0.2–0.8 |
| 4 | K\* ≈ (ln 8R/2π²)·ln(stakes/upkeep); exactly one store at α = 2 | **PRIOR ART + price** (rate conjectural, numerically supported); **CORRECTED** for "exactly one store at α = 2" as a usable prediction | α = 2 is a knife-edge: one-store excess ≈ 0.14(α−2)², so K\* > 1 at |α−2| = 0.05 once ψ ≳ 10⁴ |
| 5 | τ_m ∝ τ_E^{1−1/α}; LFK's ½ at α = 2; single store min(1−1/α, 2/3) | **CONFIRMED in-model** (re-derived; two independent numerics agree) but **CORRECTED in scope** and **PRIOR ART in substance** | Exponent holds only when the environment's variance is held fixed while τ_E moves; at fixed high-frequency level q it is 0. The underlying scaling τ ∝ (N/q)^{1/α} is published (Afterman et al. 2022; Kleptsyna et al. 2020; nonparametric bandwidth theory). The α = 2 case predates LFK (Mora & Nemenman 2019) |
| 6 | D3 explained by renewal; locked D3S pass | Lock **VERIFIED** (git), pass **REPRODUCED** (median Δβ 0.021–0.024), explanation **WRONG as stated**, test **NON-DISCRIMINATING** | A pure Cox (rate-modulated) world also gives a strongly positive Spearman(β, a) (+0.975, n = 24) and Δβ ≈ 0.045–0.05 at β ≈ 0.2, inside the pass band. D3's negative sign was mis-derived (autocorrelation vs hazard), not a sign of a renewal world |

**Headline:** demotion is right, and it should go further than the executor proposed (§7).

## 1. Theorem 1 (read rate under exact reads; optimal predictor)

*Re-derivation.* B(λt) =_d λ^H B(t). Under t ↦ t/T the read grid {jT} maps to {j}, and the linear span of past reads maps onto itself, so the
optimal linear predictor's error is T^{2H}·g(s/T). Averaging gives κ·T^{2H}; cost c/T + Wqκ T^{2H} has T\* ∝ (c/Wqκ)^{1/(1+2H)}. Correct for
any predictor class that is **closed under time rescaling** (hold-last-value, optimal linear on all past reads, optimal on the last P reads).
It does **not** hold for a predictor with a fixed time constant. R1: an EWMA of reads with τ = 50 time units has local error slopes
0.002 → 0.57 (H = ¼) and 0.004 → 0.92 (H = ¾) over T = 1–128, nowhere near 2H. **Correction:** README §0.1's "whatever linear predictor it uses"
must read "for hold-last-value and for the optimal linear predictor (any rescaling-closed class)". The theorem statement itself is fine.

*Numbers.* Re-run of `c1_readrate.py` reproduces its output. R1 (continuum average over s, P = 8…1024): κ_opt/κ_hold = 0.8904/0.8866/0.8862/0.8861
(H = ¼) and 0.8123/0.8085/0.8081/0.8079 (H = ¾). P = 64 is converged to 4×10⁻⁴. So "drops 11% and 19%" is right (11.4%, 19.2%).
Minor: the Davies–Harte check is "within 2%" for H = ¼ and ¾ (1.4%, 1.9%) but 2.6% at H = ½ (15.09 vs 15.5); that is within Monte Carlo error
for 3,000 paths and is not a defect. The README also states correctly that periodic reading is assumed, not proved optimal, for H ≠ ½. Keep that.

## 2. Theorem 2 and Corollary 2′ (noisy continuous sensing)

*Citation verified.* Afterman, Chigansky, Kleptsyna & Marushkevych, "Linear filtering with fractional noises: large time and small noise
asymptotics", SIAM J. Control Optim. 60(3):1463–1487 (2022), doi 10.1137/20M1360359, arXiv 1911.10062. I read Theorem 2.5 and eq. (2.8) in the
arXiv PDF: for H ∈ (0,1)\{½} with white observation noise, P_T ≍ κ(H)^{1/(2H+1)}/sin(π/(2H+1)) · (ε/μ²)^{2H/(2H+1)}, with κ(H) = Γ(2H+1)sin(πH)
(eq. 2.4). With α = 2H+1 and q = κ(H) (the fBm spectral constant in the dω/2π convention), this is exactly e\* = q^{1/α}N^{1−1/α}/sin(π/α). The README's
attribution is accurate. **Caveat:** their Remark 2.6(a) gives the spectral (log-integral) formula only in the *stable* case β < 0 (fractional OU), and
says explicitly that it does not apply for β ≥ 0. The README cites the spectral formula as if it covered the pure-fBm case. The leading small-noise term
agrees anyway, so the result stands; the attribution sentence should say "eq. (2.8); the spectral form in Remark 2.6(a) is for the stable case".
A second, earlier statement of the same rate: Kleptsyna, Marushkevych & Chigansky, "Asymptotic accuracy in estimation of a fractional signal in a small
white noise", Automation and Remote Control 81(3):411–429 (2020), doi 10.1134/S0005117920030030. Its Remark 2.2 notes that the rate ε^{2H/(1+2H)} coincides
with the minimax rate for estimating H-Hölder signals in white noise. That makes the whole family of scalings in this map **classical bias–variance
bandwidth theory**.

*Independent check.* ∫₀^∞ ln(1+u^{−α})du = α∫₀^∞(1+u^α)^{−1}du = π/sin(π/α) (by parts). Quadrature (R2) matches to 6 digits at α = 1.5, 2, 2.5, 3.
`c2_filter.out` reproduces as stated.

*Corollary 2′.* Minimizing c′P + W q^{1/α}P^{−(1−1/α)} over precision P = 1/N gives P\* ∝ W^{α/(2α−1)} q^{1/(2α−1)}. Numerical optimisation (R2):
0.75/0.50 (α = 1.5), 0.6667/0.3333 (2), 0.625/0.25 (2.5), 0.60/0.20 (3), exactly the formula. **CONFIRMED.** Scope: this assumes precision is priced
**linearly**. Any other price exponent changes both elasticities, so "a = b is a property of reset reads" is right as a counterexample, but
"2/3 and 1/3 in a Brownian world" is a statement about linear precision pricing, not about Brownian worlds. Prior art: not found in one search; the closest is
Davies, "Learning about a changing state" (arXiv 2401.03607, 2024), which studies costly precision for a changing state. I did not verify
whether it states these elasticities. Label: ELEMENTARY, not found stated.

## 3. Proposition 3 (kernel tail and sign)

*Re-derivation.* For white observation noise, 1 − K = √N/Φ₊, so near ω = 0, 1 − K ≈ (iω/ω_c)^{α/2}. The Fourier pair (iω)^ν ↔ t^{−1−ν}/Γ(−ν)
gives a weight tail −τ^{−1−α/2}/(Γ(−α/2)ω_c^{α/2}). Γ(−α/2) < 0 for 0 < α < 2 (positive weights) and > 0 for 2 < α < 4 (negative weights). At integer
α/2 the term is analytic, so the tail is exponential. **CONFIRMED.** `c2_filter.out` agrees (fitted −1.164…−2.766; signs +,+,+,−,−; at α = 2 the kernel
hits the 3×10⁻¹² numerical floor, i.e. exponential).

*Citations verified* (Crossref): Nuzman & Poor, "Linear estimation of self-similar processes via Lamperti's transformation", J. Appl. Prob.
37(2):429–452 (2000); Gripenberg & Norros, "On the prediction of fractional Brownian motion", J. Appl. Prob. 33(2):400–410 (1996); Hosking,
"Fractional differencing", Biometrika 68(1):165–176 (1981); Granger & Joyeux, J. Time Ser. Anal. 1(1):15–29 (1980); Gatheral, Jaisson & Rosenbaum,
"Volatility is rough", Quant. Finance 18(6):933–949 (2018). The GJR predictor formula has weight cos(Hπ)/π·Δ^{H+½}/((τ+Δ)τ^{H+½}) on past levels: tail
τ^{−(H+3/2)} = τ^{−(1+α/2)}, sign cos(Hπ), which is negative for H > ½ ⇔ α > 2. ARFIMA(0,d,0) AR(∞) weights −π_k ~ −k^{−1−d}/Γ(−d) with d = α/2 give the
same sign rule. Note that Hosking's paper is about |d| < ½, so α < 1. The weight formula extends algebraically to the d ∈ (½, 3/2) the README uses.
Say so. The noisy-filter version is an assembly, not found stated. Related prior art the README omits: Lundstrom, Higgs, Spain & Fairhall,
"Fractional differentiation by neocortical pyramidal neurons", Nat. Neurosci. 11(11):1335–1342 (2008), the empirical case for power-law kernels
matched to power-law stimuli.

*Correction to the inference (README §0.4, THEORY §2.5(iii)).* The tail exponent 1+α/2 ∈ (1.5, 2.5) is the exponent of the **weight density** h(τ).
A retention or forgetting curve, meaning how much of an item's trace still influences the estimate at age τ or later, is ∫_τ^∞ h, which decays as τ^{−α/2}:
0.5–1.5 for fBm worlds and 0–0.5 for stationary α < 1. That **overlaps** the measured 0.2–0.8 band. Separately, MATCH1's 0.6–0.8 "need exponents" are
hazards of re-occurrence (verified in `tests/MATCH1/aslib.py: need_counts`: gaps of length L over gaps ≥ L), which are neither the kernel nor its
survival. So the correct statement is: *need hazards are a different object from tracking kernels, and no kernel was measured.* "Far steeper,
therefore not optimal kernels" does not follow. §2.2's conflation charge stands; the steepness argument should be dropped.

## 4. Proposition 4 (store count)

*(a) One store iff rational, OU/Brownian + white noise needs one.* KNOWN (finite-dimensional realization / Kalman). **CONFIRMED.**

*(b) Rate.* Braess–Hackbusch bound verified: E ≤ 16 exp(−π²n/log 8R) for 1/x on [1,R] (Braess & Hackbusch 2009, "On the efficient computation of
high-dimensional integrals and the approximation by exponential sums", in *Multiscale, Nonlinear and Adaptive Approximation*, Springer, doi
10.1007/978-3-642-03413-8_3; MPI MIS preprint 3/2009); the [1,∞) paper is IMA J. Numer. Anal. 25(4):685–697 (2005), doi 10.1093/imanum/dri015. The
kernel being approximated is not 1/x, and the README correctly labels the squared rate a CONJECTURE. Its "within 5%" uses one K-step (2→3). Over all
K-steps in `c3_layers_1.5.out`, the log-decrements at L = 4 are 2.21, 1.87, 1.74, 1.65 vs 1.75 predicted (within ~7–26%, drifting down toward the
3×10⁻⁷ quadrature floor). That supports the rate within ~10–25%, not 5%.

*(c) K\* formula.* The full form K\* ≈ (ln 8R/2π²)·ln(ψ·C·2π²/ln 8R) is right given (b). The "ln(stakes/upkeep)" short form drops an O(ln ln R) term.
The measured K\* (2,3,3,4 over L = 1–4) is too coarse to establish linearity in ln R. **Prior art for the product form:** the sum-of-exponentials
complexity for power-law kernels, N_exp = O(log(1/ε)(log log(1/ε) + log(T/Δt)) + …), is Jiang, Zhang, Zhang & Zhang, Commun. Comput. Phys. 21(3):650–678
(2017), doi 10.4208/cicp.OA-2016-0136. With ε set by the price (ε ~ upkeep/(stakes·e)) this *is* K\* ∝ ln(span)·ln(stakes/upkeep). "Number of
variables ∝ log of memory lifetime" is Benna & Fusi, Nat. Neurosci. 19(12):1697–1706 (2016). Log-spaced Laplace memory is Shankar & Howard, Neural
Comput. 24(1):134–193 (2012). THEORY.md's "Shankar & Howard 2013" (optimality for power-law signals) is presumably their "Optimally fuzzy temporal
memory" (arXiv 2012); I did not verify its journal details. Verdict: **approximation theory plus a price**, as night 1 said,
now with the exact prior-art pointer. Bayer & Breneis is real: Quant. Finance 23(1):53–70 (2023), doi 10.1080/14697688.2022.2139193. Beylkin & Monzón,
ACHA 28(2):131–149 (2010), and Carmona & Coutin, Electron. Commun. Probab. 3:95–107 (1998), are also verified.

*Knife-edge at α = 2 (new check R4, executor's own c3 code imported unchanged).* Best one-store relative excess: 5.1×10⁻³ (α = 1.8), 1.45×10⁻³ (1.9),
4.1×10⁻⁴ (1.95), 4×10⁻⁶ (2.0, quadrature floor), 3.2×10⁻⁴ (2.05), 1.4×10⁻³ (2.1), 6.4×10⁻³ (2.2) at L = 2, similar at L = 4. That is ≈ 0.14(α−2)².
K\* = 2 already at |α−2| = 0.05 when ψ = 10⁴. So "exactly one store at α = 2 at every span and price" is true but **measure-zero**. The usable
prediction is continuous: **one store suffices iff ψ·0.14(α−2)² ≲ 1** (in this model). That replaces the knife-edge in any test.

## 5. Proposition 5 — the candidate new prediction τ_m ∝ τ_E^{1−1/α}

*Independent re-derivation.* S_x = c_α σ²τ_E(1+(ωτ_E)²)^{−α/2} has high-frequency level q = c_α σ² τ_E^{1−α}. The causal filter's crossover is set by
S = N: ω_c = (q/N)^{1/α}, so τ_c ∝ (N/q)^{1/α} ∝ (N/σ²)^{1/α} τ_E^{1−1/α}, valid while ω_cτ_E ∝ τ_E^{1/α} → ∞ (α > 1). EWMA with time constant τ: bias
∝ qτ^{α−1} for 1 < α < 3, so τ\* ∝ (N/q)^{1/α}, same exponent. For α > 3 the bias is τ²·Var(ẋ) ∝ τ²σ²/τ_E², and minimizing τ²/τ_E² + N/τ gives τ ∝ τ_E^{2/3}.
Hence min(1−1/α, 2/3). **CONFIRMED.**

*Independent numerics (R5, continuous time, adaptive quadrature; different code path from `c5_lfk.py`'s discrete FFT).* At unit variance, the EWMA slopes
at τ_E = 10⁸–10¹⁰ are 0.333, 0.500, 0.599, 0.665 (α = 1.5, 2, 2.5, 3.5; theory 0.333, 0.5, 0.6, 0.667). The optimal-MSE slopes are −0.333, −0.500, −0.600,
−0.714 (theory (1−α)/α). `c5_lfk.out` reproduces as stated.

*Scope correction (decisive for the "new prediction").* R5 repeated at **fixed high-frequency level q** (the corner moves; local volatility does not)
gives slope **0.000** for every α (EWMA at α = 3.5: −0.167). The τ_E exponent is therefore not a property of α alone. It is the exponent of
(N/q)^{1/α} combined with the assumption that **variance is held fixed** as τ_E varies (q ∝ τ_E^{1−α}). LFK's telegraph model has fixed switching
amplitude, so it is in the fixed-variance class. Real cross-environment comparisons (SPF variables, species) will not hold variance or N fixed.
**The testable, normalisation-free statement is τ_m ∝ (N/q)^{1/α}**, which is the Wiener/Kalman bandwidth and is KNOWN (Afterman et al. 2022 eq. 2.8;
Kleptsyna et al. 2020; the H-Hölder minimax bandwidth in nonparametric statistics). LFK-ALPHA-SPF must measure q and N per variable, or it tests a
normalisation and not the theory.

*Prior-art search (also discharges most of PRIORART-LFK-ALPHA).*
- LFK verified: arXiv 2209.00476 "Outsourcing memory through niche construction", whose eq. (11) is τ_m\* ∼ τ_E^{1/2} from a KL/log-gain trade-off
  (C τ_m²/τ_E − G log τ_m). The **published** version has a different title: Lee, Flack & Krakauer, "Constructing stability: optimal learning in noisy
  ecological niches", Proc. R. Soc. B 291(2033):20241606 (2024), doi 10.1098/rspb.2024.1606. The README's citation numbers are right but give no
  title; add it.
- **The α = 2 law predates LFK:** Mora & Nemenman, "Physical limit to concentration sensing in a changing environment", PRL 123:198101 (2019),
  arXiv 1908.04057. The optimal integration time is the geometric mean √(τ/(4Dac)) of the fluctuation time and the inter-binding time. That is τ_m ∝ τ_E^{1/2}.
  Malaguti & ten Wolde, eLife 10:e62574 (2021), give the Markovian bias–variance decomposition. THEORY §0/§2.2 credit "the square-root memory law" to LFK;
  they should credit Kalman/Wiener and Mora & Nemenman and cite LFK as an application.
- Forward citations of LFK (OpenAlex: 6 works across both DOIs, read by title: "Decoding the architecture of living systems"; chess strategic tension;
  "An Information Framework of Intelligence"; bacterial externalized memory; C. elegans forgetting; "Playing it safe"). None, by title, generalises the
  exponent. I did not read their full texts.
- Fractional filtering (Afterman et al. 2022; Kleptsyna et al. 2020) state the noise-intensity scaling, not a τ_E re-parameterisation.
- Shankar & Howard 2012, Benna & Fusi 2016 and Mora & Nemenman 2019 are as cited above. None states τ_m ∝ τ_E^{1−1/α}.
- Not swept: Google Scholar (still blocked), full texts of citers, the PLL/clock-steering literature (optimal loop bandwidth for f^{−α} oscillator
  noise is the same calculation in engineering form; one search found the α = 2 case worked as an optimum-bandwidth trade-off in "Jitter-Power Trade-Offs in PLLs"
  (IEEE TCAS, 2021, UCLA), but no statement in τ_E form).
**Verdict on 5:** the formula is correct. As a statement it was not found, but it is a one-line corollary of a published scaling, and its τ_E form holds
only under fixed variance. **Label: ELEMENTARY corollary; PRIOR ART in substance; the τ_E form is new only as a re-parameterisation.**
It is not a "named rival does not make it" discriminator unless the test controls q and N.

## 6. Proposition 6, D3 and the locked D3S

*Lock order (git).* `6636f02` (09:19:07 ET, PREREG only, 1 file) precedes `dbd3255` (09:25:49 ET), which added `d3s_shuffle.py/.out/.json`. Between
them, the PREREG changed in one line only: the lock-time text went from "about 09:25 ET" to "09:19 ET (commit 6636f02)". No hypothesis, band or rule
changed. Limits: commit times are self-reported, the analysis script was not locked (the PREREG specifies the pipeline in words), and git cannot prove
no shuffle was computed earlier. On the record as committed, **the lock preceded the result.**

*Rerun.* Same 12 clones (`/workspace/collapse_repos/`, unchanged since 14 Nov 22:55 ET). Median Δβ = 0.021 (PREREG order) and 0.023 (alphabetical
order, as the original ran) vs 0.024 committed. S1 PASS reproduces. It is **not bit-reproducible**: (i) one RNG stream is shared across repos, so repo
order matters; (ii) the order of files in `ed.values()` depends on PYTHONHASHSEED; (iii) pandoc's β_orig came out 0.258 in both reruns vs 0.253 committed,
which I could not explain from the code. None of these changes the verdict. S2 (exploratory) Spearman(β_shuf, a) = +0.40, p = 0.20, n = 12: not
significant. Wilcoxon on the 12 Δ's: p = 0.096 (8 of 12 positive).

*Power (R6, new).* With the same estimator and shuffle on synthetic data: renewal worlds give Δβ = −0.002 to 0.004 (good negative control). **Pure Cox
worlds** (daily edit probability modulated by a 1/f^γ log-rate, no renewal structure) give Δβ = 0.045 (β_orig 0.20), 0.049 (0.17), 0.096 (0.38),
0.012–0.015 (β ≈ 0.04–0.08). At the β ≈ 0.2–0.25 of the real repos, a pure Cox world lands **inside the locked pass band [−0.03, 0.05]**. The kill
threshold 0.08 is reachable only by much redder Cox worlds. **D3S cannot distinguish renewal from Cox at the observed β.** A better statistic is
Δβ/β_orig: real repos 0.11 (median); my Cox settings 0.22–0.29; renewal ≈ 0. That points to a mixture, but my Cox settings are arbitrary, so this is
not evidence.

*The explanation of D3 (R7, new).* 24 random pure-Cox repos (γ, s, r drawn at random) give Spearman(β, a_need) = **+0.975** (p = 7×10⁻¹⁶). So the positive
sign does **not** need a renewal world. The original negative prediction was mis-derived. It used the Tauberian link for the **excess event
autocorrelation** (∝ L^{−(1−β)}), but MATCH1's a_need is the exponent of the **re-occurrence hazard** (need odds given no event since the last one). In any
world, more low-frequency modulation means both more red power and a more steeply falling hazard (dynamic selection on the rate), so a and β co-move
positively under renewal *and* under Cox. **Correct statement:** D3's opposite sign came from an estimator mismatch in the locked prediction, not from
the world's type. "Event worlds need two exponents" remains true in the trivial sense that hazard and spectrum are different functionals. The renewal
hypothesis R is neither supported nor refuted by D3S (PROXY-PASS, non-discriminating). The c4b "renewal from each repo's empirical hazard reproduces β"
result (POST HOC) is the same non-discriminating fact: the shuffle shows the gap marginal carries most of β, and Cox gap marginals carry it too.

## 7. The headline (the recommendation to demote "central new bet")

**Agree, and go further.** After this review the tracking map is: Wiener–Kolmogorov/Kalman filtering (Yovits–Jackson; Afterman et al.; Kleptsyna et
al.), plus exponential-sum approximation complexity (Braess–Hackbusch; Jiang et al.; Benna & Fusi), plus a price. The pieces the executor called new
reduce as follows:
- **LFK-α:** a re-parameterisation of a published bandwidth law, valid only at fixed variance.
- **Kernel sign flip at α = 2:** published (GJR's cos(Hπ); ARFIMA weights).
- **Two-exponent split:** the D3 resolution is an estimator mismatch, not world structure.
- **Effort elasticities α/(2α−1):** correct and not found stated, but elementary and dependent on linear precision pricing.
Against a rival who sets up the same filtering model, nothing here is distinctive. The executor said this too, but then still listed three "new
contents"; only the fourth survives, and as an elementary corollary.

**Honest headline (proposed for THEORY §0, for THEORY-2.2-REWRITE; wording is Chad-visible):**
> *GTAO's tracking layer is classical optimal filtering and approximation theory plus a price. For a world with spectral slope α, it gives the design
> exponents: read rate ∝ (stakes·drift/price)^{1/α} for reset reads; precision effort ∝ stakes^{α/(2α−1)} drift^{1/(2α−1)} under linear precision
> pricing; memory time ∝ (noise/drift-level)^{1/α}; a kernel with tail τ^{−(1+α/2)} that is exponential only at α = 2; and a store count ∝ ln(span)·
> ln(stakes/upkeep) away from α = 2. These are known or elementary results, assembled. GTAO's open empirical bet is that real adaptive systems at many
> scales sit near these optima once α, q and N are measured on the same system. That is untested.*

Drop "the central new bet" and "the shape of the world's change sets the exponents" as a *novelty* claim. Keep it as the organising frame, credited.
Regime A should read "α = 2 (Markov)", and its ½ should be credited to Kalman/Muth, Mora & Nemenman 2019 and LFK 2024 (as an application). Regime B's
"slope 1" contradicts this map: stationary random worlds give 1−1/α < 1 at fixed variance, and 0 at fixed q. Fairhall's slope 1 (periodic switching)
is outside the map, as the README says.

## 8. Required changes (for THEORY-2.2-REWRITE and the SPECTRUM_MAP README; not applied to the README here)
1. README §0.1: "whatever linear predictor" → "hold-last-value and the optimal linear predictor (rescaling-closed classes)".
2. Thm 2: cite Afterman et al. eq. (2.8); note that Remark 2.6(a)'s spectral form is for the stable case. Add Kleptsyna et al. 2020.
3. Cor 2′: say "under linear precision pricing".
4. Prop 3 / §2.5(iii): drop "far steeper ⇒ not kernels". The kernel survival exponent is α/2. Need hazards are a different object, and no kernel has been measured.
5. Prop 4: credit Jiang et al. 2017 and Benna & Fusi 2016 for the ln·ln form. Replace "exactly one store at α = 2" with "one store iff ψ·0.14(α−2)² ≲ 1 (in-model)". The rate fit is within ~10–25%, not 5%.
6. Prop 5 / P-LFKα: restate as τ_m ∝ (N/q)^{1/α} (KNOWN) with the τ_E form valid at fixed variance. Credit Mora & Nemenman 2019 for α = 2. LFK-ALPHA-SPF must measure q and N.
7. Prop 6 / §2.4 D3 row: replace "explained by renewal; locked D3S passed" with "the locked sign was mis-derived (autocorrelation vs hazard); positive sign arises under renewal and Cox (R7); D3S passed on proxy but has no power against Cox at β ≈ 0.2 (R6)".
8. `d3s_shuffle.py`: sort file lists and use a per-repo seed for bit-reproducibility (any future lock should commit the script with the PREREG).

## 9. CLAIM_MAP_v2 status changes applied by this referee (section N note in that file)
- **K13** (spectrum → exponent relation): OPEN → **MATH-CORRECTED**. The stated predictions (½ for one pace; slope 1 and power-law forgetting for scale-free worlds) are superseded by SPECTRUM_MAP Props 1–5 as corrected here (exponents 1/α, 1−1/α at fixed variance, kernel tail 1+α/2). The replacement is mostly PRIOR ART; the field relation is untested.
- **K12** (geometric layers; level count): OPEN → **MATH-CORRECTED**. One store iff rational (knife-edge at α = 2); K\* ∝ ln span·ln(stakes/upkeep) is prior-art approximation complexity plus a price; (log-span)^{2/3} is withdrawn.
- **H19** (MATCH1 D3 sign): PROXY-FAIL → **MATH-CORRECTED**. The locked negative sign was derived for the wrong estimator. D3S is a PROXY-PASS, non-discriminating.
- **N7**: unchanged (PROVED in-model); extension to the optimal linear predictor confirmed (§1).

## 10. Files
`SPECTRUM_MAP_REFEREE_checks/`: `r1_pastlen` (Thm 1 P-sensitivity, fixed-EWMA counterexample), `r2_elasticities` (integral, Cor 2′),
`r4_near2` (store knife-edge, imports c3 unchanged), `r5_lfk_continuous` (Prop 5 independent numerics, variance vs q normalisation),
`r6_d3s_power` (D3S positive/negative controls), `r7_cox_sign` (Cox sign of Spearman(β, a)), each with `.out`/`.json`. D3S reruns: see §6 (not
committed as outputs, to keep the locked result file unchanged).
