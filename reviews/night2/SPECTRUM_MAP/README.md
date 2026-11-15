# SPECTRUM_MAP: from a measured drift spectrum to read rate, memory stores and forgetting (QUEUE Q2; Q1 gap-fill)

Executor, 15 Nov 2026, 09:05–09:45 AM ET, branch `spectrum-map`. Status: **derived and numerically checked; NOT yet refereed.**
A hostile math referee is queued (QUEUE, SPECTRUM-MAP-REFEREE). Labels: KNOWN = in the literature (cited, verified this
session); ELEMENTARY = a short corollary of known results that we state here; NEW? = not found in the sources searched;
POST HOC = fitted after seeing the data; LOCKED = predicted in a committed file before the computation.

## 0. Plain-words result

1. **The read-rate exponent 1/(1+2H) holds, and not only for hold-last-value.** A tracker that reads a fractional-Brownian
   world every T and predicts in between makes average error ∝ T^{2H}, *whatever linear predictor it uses*, because fBm is
   self-similar. So the optimal read rate scales as (stakes × drift / read price)^{1/(1+2H)} = (…)^{1/α} with α = 1+2H the
   spectral slope. The best predictor only lowers the constant (by 11% at H = 0.25 and 19% at H = 0.75). Checked by exact
   Gaussian conditioning and Davies–Harte simulation (`checks/c1`). This closes the item that AUDIT_REFEREE listed as owed.
2. **With noisy continuous sensing the exponents change** (the error is q^{1/α}N^{1−1/α}/sin(π/α), a KNOWN result of
   Afterman et al. 2022). If the agent buys precision, the stakes elasticity of effort is α/(2α−1) and the drift elasticity
   is 1/(2α−1): 2/3 and 1/3 in a Brownian world, not ½ and ½. So "a = b" is a property of reset reads, not of tracking in general.
3. **The optimal forgetting kernel's tail is τ^{−(1+α/2)}**: steeper, not shallower, in a redder world; exponential only at
   α = 2 (Brownian / Markov); for 2 < α < 4 the old weights turn **negative** (the tracker extrapolates the trend). Checked
   to ±0.02 in the exponent for α = 0.4–3.5 (`checks/c2`). The noiseless version of this tail is KNOWN (fBm predictor,
   Nuzman & Poor 2000; the "Volatility is rough" forecast formula; ARFIMA AR(∞) weights).
4. **Consequence for §2.2:** the optimal tracking kernel's exponent is 1.5–2.5 for every fBm world, far steeper than the
   0.2–0.8 forgetting/need exponents measured in MATCH1/COLLAPSE1. So those power-law curves are **not** optimal tracking
   kernels of a power-law world. They are hazards of re-occurrence (Anderson–Schooler need odds), a different object.
   §2.2's "power-law world → power-law forgetting with matching exponent" conflates the two.
5. **Number of memory stores:** finite and exact iff the spectrum is rational (KNOWN, realization theory). Brownian/OU plus
   noise needs exactly **one** store at any span. A power law over a span R approximated by K exponential stores leaves a
   relative excess error ≈ C·exp(−2π²K/ln 8R) (the Braess–Hackbusch exponential-sum rate, squared; our numerics match the
   rate to within 5%). With per-store upkeep h and stakes W: **K\* ≈ (ln 8R / 2π²)·ln(W·e/h)**, linear in log-span and in
   log stakes/upkeep (`checks/c3`). This is **approximation theory plus a price**, as night 1 suspected. §2.2's
   "(log-span)^{2/3}" is model-specific and should be replaced.
6. **Lee–Flack–Krakauer's ½ is the α = 2 case of τ_m\* ∝ τ_E^{1−1/α}** (= τ_E^{2H/(1+2H)}); an agent limited to one
   exponential store has exponent min(1−1/α, 2/3). Checked to ±0.01 (`checks/c5`). Regime A in §2.2 is really "α = 2
   (Markov)", not "one pace": a world with one corner time but a different slope above it gives a different exponent.
   This is the one prediction here that a named rival (LFK's universal ½) does not make. NEW? (ELEMENTARY given the
   filtering asymptotics; prior-art search for it was one query, not a sweep.)
7. **MATCH1 D3's "opposite sign" is explained, and a locked follow-up passed.** In event data the need exponent a and the
   band spectral slope β are both read off one inter-edit-gap distribution: burstier gaps raise both, so they correlate
   **positively** (simulation: +0.75). Simulating each MATCH1 repo as a pure renewal process with its own hazard reproduces
   its measured β (Spearman 0.53, p = 0.013, n = 21; median gap 0.015) — POST HOC. Then the LOCKED gap-shuffle test
   (`PREREG_D3S.md`, commit 6636f02, 09:19 ET, run 09:20 ET): shuffling each file's gaps changes β by a median 0.024
   (12 repos), inside the locked [−0.03, +0.05] band → **S1 PASSED on proxy "binary daily edit series, band 1/730–0.5 c/d"**.
   Gap order carries ~10% of the band slope; successive gaps are correlated (M ≈ 0.27), so the world is not a pure renewal.
   The original negative sign assumed a modulated-rate (Cox) world, where a Tauberian link makes the need decay
   exponent 1−β. Event worlds need **two exponents** (spectrum and hazard); §2.2's single "redness" is under-specified.

**Verdict on the headline (Q2 kill/pass).** The map is mostly KNOWN filtering and approximation theory, assembled. It
passes the letter of Q2 (it makes predictions the named rivals do not: the LFK exponent 1−1/α, kernel sign flip at α = 2,
effort elasticities α/(2α−1) ≠ ½), but against a rival who sets up the same filtering model it is not distinctive.
**Recommendation: demote "central new bet" to "a precise map, mostly known pieces, whose new content is the assembly, the
LFK generalization and the two-exponent split for event worlds".** Applied minimally in THEORY.md (pointer + changelog,
pending the referee); the §2.2 rewrite is a queued decision (THEORY-2.2-REWRITE).

## 1. Setting and notation

World x(t) with two-sided spectral density S(ω) = q|ω|^{−α} (dω/2π convention) on the band of interest. For 1 < α < 3 this
is fBm with H = (α−1)/2, and E(x_t − x_0)² = q t^{α−1}/(Γ(α) sin(π(α−1)/2)). Observation: either exact reads every T
(price c per read), or continuous y = x + white noise of density N (precision 1/N priced c′/N per unit time). Loss: W × mean
squared error per unit time. Memory: K exponential stores (EWMA with rates λ_j) plus free short-lag taps, upkeep h per store.

## 2. Results

**Theorem 1 (read rate under exact reads; ELEMENTARY, extends formal Lemma 1(i)).** Let x be fBm(H), read exactly at
times kT, and let ê be any predictor in the class P_T = {linear functions of the reads}, used optimally. Then the
time-averaged MSE is ē(T) = κ_P(H)·q·T^{2H} with κ_hold = 1/(1+2H) for hold-last-value and κ_opt ≤ κ_hold for the optimal
linear predictor; the cost c/T + W ē(T) is minimized at T\* = [c/(2H κ W q)]^{1/(1+2H)}, so the read rate has elasticity
1/(1+2H) = 1/α in W and in q for both estimators.
*Proof.* B(λt) =_d λ^H B(t). The optimal linear predictor of B(kT+s) from {B(jT)}_{j≤k} maps under t ↦ t/T to the
predictor of B(k+s/T) from {B(j)}, so its error is T^{2H}g(s/T) with g independent of T. Averaging over s ∈ [0,T) gives
T^{2H}∫_0^1 g = κ T^{2H}. The first-order condition gives T\*. ∎ (Periodic reading is assumed, not proved optimal, for H ≠ ½.)
*Check (`checks/c1_readrate.out`).* Brute-force T\* over 5 decades of W: elasticities 0.670/0.670 (H = 0.25, theory 0.667),
0.499/0.499 (0.5), 0.398/0.398 (0.75) for hold/optimal; κ_opt/κ_hold = 0.887, 1.000, 0.809, constant in T; Davies–Harte
Monte Carlo (3,000 paths) matches the analytic errors within 2%.

**Theorem 2 (noisy continuous sensing; KNOWN, constant included).** For 1 < α < 3, the stationary causal MMSE is
e\* = q^{1/α}N^{1−1/α}/sin(π/α). KNOWN: Afterman, Chigansky, Kleptsyna & Marushkevych, SIAM J. Control Optim. 60(3):1463–1487
(2022), Thm 2.5 eq. (2.8) (their κ(H) = Γ(2H+1)sin(πH) normalization), with the spectral formula in their Remark 2.6:
e = (N/2π)∫ln(1+S/N)dω, and ∫_0^∞ ln(1+u^{−α})du = π/sin(π/α). α = 2 gives the Kalman √(qN).
*Check (`checks/c2_filter.out`).* Discrete-time Kolmogorov–Szegő at dt = 10^{−4}: 1.1495 vs 1.1547 (α = 1.5), 0.9967 vs 1
(α = 2), 1.0473 vs 1.0515 (2.5), 1.1497 vs 1.1547 (3); direct time-domain conditioning (dt = 0.01, n = 3000): 1.1500 and 1.0481.
**Corollary 2′ (ELEMENTARY).** Minimizing c′/N + W e\*(N): effort 1/N\* ∝ W^{α/(2α−1)} q^{1/(2α−1)}. At α = 2: (2/3, 1/3).

**Proposition 3 (kernel tail; proof sketch; noiseless case KNOWN).** With S_y = S + N factorized S_y = Φ₊Φ₋, the causal
Wiener filter for white noise is K = 1 − √N/Φ₊ (Kailath, Sayed & Hassibi 2000). For S = q|ω|^{−α}(1 + (|ω|/ω_c)^α),
ω_c = (q/N)^{1/α}, Φ₊ = √q (iω)^{−α/2}Ψ₊ with Ψ₊ = 1 + O(|ω|^α), so 1 − K(ω) = (iω/ω_c)^{α/2}(1 + O(|ω|^α)) near 0. The
leading non-analytic term (iω)^{α/2} transforms to an impulse-response tail τ^{−1−α/2}/(Γ(−α/2)ω_c^{α/2}) for τ ≫ 1/ω_c.
Hence the weight on an observation of age τ falls as τ^{−(1+α/2)}; its sign is that of −1/Γ(−α/2): positive for 0 < α < 2,
negative for 2 < α < 4; when α/2 is an integer the term is analytic and the tail is exponential (α = 2: the Kalman EWMA at
rate ω_c). *Check.* Fitted tails −1.164 (α = 0.4, theory −1.2; local slope still converging, −1.18 at 8k–20k), −1.405
(0.8; −1.4), −1.761 (1.5; −1.75), −2.262 (2.5; −2.25), −2.766 (3.5; −2.75); signs +,+,+,−,−; α = 2 exponential at rate
0.100 = 1/τ_c. *Prior art.* Noiseless fBm prediction kernel (t−s)^{−(H+1/2)}/(t−s+Δ), tail exponent H+3/2 = 1+α/2:
Nuzman & Poor 2000 (J. Appl. Prob. 37(2):429–452), used in Gatheral, Jaisson & Rosenbaum 2018 (Quant. Finance 18(6):933–949);
Gripenberg & Norros 1996 for H > ½; ARFIMA(0,d,0) AR(∞) weights ∝ k^{−1−d} (Hosking 1981, Biometrika 68:165–176; Granger
& Joyeux 1980, J. Time Ser. Anal. 1:15–29), d = α/2.

**Proposition 4 (store count; rate conjectural, numerically supported).** (a) KNOWN: the Wiener filter is a finite sum of
exponentials iff the spectrum is rational; OU/Brownian plus white noise needs exactly one store. (b) CONJECTURE: for a power
law over span R = τ_max/τ_c, the best K-store approximation has relative excess error ε_K ≈ C·exp(−2π²K/ln 8R). Basis: the
uniform error of the best K-term exponential sum for 1/x on [1,R] is ≤ 16 exp(−π²K/ln 8R) (Braess & Hackbusch 2009,
"On the efficient computation of high-dimensional integrals and the approximation by exponential sums", MPI MIS preprint
3/2009; infinite-interval rate exp(−c√K): Braess & Hackbusch 2005, IMA J. Numer. Anal. 25(4):685–697), and MSE is quadratic
in the kernel error. *Check (`checks/c3_layers_*.out`, α = 1.5):* log-decrement of ε from K = 2 to 3 is 2.8, 2.2, 1.87 at
L = log₁₀R = 2, 3, 4 vs 2π²/ln(8R) = 2.9, 2.2, 1.78. α = 2: K\* = 1 at every span and every price (excess 4×10^{−6}).
(c) ELEMENTARY: then K\* ≈ (ln 8R/2π²)·ln(ψ·C·2π²/ln 8R), ψ = W·e_opt/h. Measured K\* at ψ = 10^4 for L = 1–4: 2,3,3,4
(α = 1.5) and 2,3,4,4 (α = 2.5). Rate ratios between adjacent stores shrink as precision rises (α = 1.5, L = 4: 11.1, 6.5,
5.2 at ψ = 10³, 10⁴, 10⁵), so spacing is not span-invariant at finite precision (consistent with LAYERS1 P2 failing 6/12).
For α > 2, two stores at nearly equal rates appear (a second-order section, needed for the negative tail).
Related: Carmona & Coutin 1998 (fBm as a superposition of OU processes); Bayer & Breneis 2023 (Markovian approximation of the
fractional kernel, Quant. Finance 23(1):53–70); Beylkin & Monzón 2010 (ACHA 28(2):131–149).

**Proposition 5 (LFK generalization; ELEMENTARY, NEW? as a stated prediction).** Let S_x = c_α σ² τ_E (1+(ωτ_E)²)^{−α/2}
(unit variance σ² = 1, corner 1/τ_E, slope α > 1 above it), white noise N. For τ_c ≪ τ_E the filter sees only the
high-frequency part, S ≈ c_α τ_E^{1−α}|ω|^{−α}, so q ∝ τ_E^{1−α} and τ_c = (N/q)^{1/α} ∝ τ_E^{1−1/α}; the optimal MSE
scales as τ_E^{(1−α)/α}. An EWMA tracker has bias dominated by the corner when α > 3, giving τ_m ∝ τ_E^{2/3}; so its
exponent is min(1−1/α, 2/3). *Check (`checks/c5_lfk.out`, τ_E to 10^8):* EWMA local slopes at the largest τ_E 0.334, 0.500,
0.598, 0.666, 0.666 for α = 1.5, 2, 2.5, 3.5, 4 (theory 0.333, 0.5, 0.6, 0.667, 0.667); optimal-filter half-weight age
slopes 0.365, 0.496, 0.600, 0.713, 0.746 (theory 0.333, 0.5, 0.6, 0.714, 0.75); MSE slopes −0.319 … −0.733 converging to
(1−α)/α. *Caveat:* LFK (Proc. R. Soc. B 291:20241606, 2024; arXiv 2209.00476) use a KL/log cost on a binary telegraph
environment, not MSE; the α = 2 agreement is of exponents, not of models.

**Proposition 6 (event worlds need two exponents; numerical + POST HOC + one LOCKED pass).** For a renewal process with
need odds ∝ L^{−a} (a < 1: stretched-exponential gaps), the apparent band slope β of the binary daily series rises with a
(controlled sweep a = 0.2 → 0.95: β = 0.15 → 0.39; 24 random synthetic repos: Spearman(β, â) = +0.75, p = 2×10^{−5};
`checks/c4_d3_renewal.out`). In a Cox process whose intensity has autocorrelation ∝ L^{−(1−β)}, the excess need probability
decays as L^{−(1−β)}, the negative relation D3 had locked. MATCH1 data side with renewal: `checks/c4b_match1_renewal.out`
(POST HOC) and the LOCKED D3S gap-shuffle (`checks/d3s_shuffle.out`; S1 PASS, median Δβ = 0.024; S2 Spearman(β_shuf, a) =
+0.40, n = 12; Spearman(β_orig, β_shuf) = 0.71; median Goh–Barabási memory M = 0.27). Supporting prior art: Lowen & Teich
1993 (fractal renewal processes, IEEE Trans. Inf. Theory, doi 10.1109/18.259653); Goh & Barabási 2008 (EPL 81:48002,
burstiness vs memory as separate measures). Proxy labels: "need" = file edited that day; β = band slope of a binary series.

## 3. Known vs new

| Piece | Status |
|---|---|
| Read-rate elasticity 1/(1+2H) for hold-last-value | KNOWN-type (EOQ calculus; formal Lemma 1(i); AUDIT_REFEREE confirmed) |
| Same exponent for the optimal linear predictor (Thm 1) | ELEMENTARY (self-similarity); stated here; constant ratios new numbers |
| Noisy MMSE q^{1/α}N^{1−1/α}/sin(π/α) | KNOWN (Afterman et al. 2022) |
| Effort elasticities α/(2α−1), 1/(2α−1) with priced precision | ELEMENTARY; not found stated |
| Kernel tail τ^{−(1+α/2)}, sign flip at α = 2 | KNOWN noiseless (Nuzman & Poor; Hosking); noisy-filter form assembled here |
| Finite store count iff rational spectrum | KNOWN |
| K\* linear in ln(span) × ln(stakes/upkeep) | approximation theory (Braess–Hackbusch) plus a price; the rate is a CONJECTURE checked numerically |
| LFK ½ → 1−1/α; EWMA cap 2/3 | NEW? (elementary) |
| Two-exponent split for event worlds; D3 resolved | assembled from Lowen–Teich / Goh–Barabási ideas; D3S locked pass is a new result on proxy |

## 4. The prediction to test (crisp, falsifiable, cross-scale)

**P-LFKα.** For any adaptive tracker whose world has a measured corner time τ_E and a measured spectral slope α just above
its own crossover, log(memory time) vs log(τ_E) across environments has slope **1 − 1/α** (single-store trackers: min(1−1/α, 2/3)).
Rivals: LFK's universal ½; §2.2 regime B's slope 1. Kill: slope CI excludes 1 − 1/α while including ½ (or 1).
Public-data tests available today (each needs a prereg with regime measured first):
1. **Professional forecasters across variables** (Philadelphia Fed SPF: CPI, unemployment, T-bill, GDP growth). Memory time
   from the Coibion & Gorodnichenko (2015, AER 105(8):2644–2678) revision-on-error gain; τ_E and α from each variable's own
   spectrum (FRED). Several variables with different α → a cross-variable slope test.
2. **Implied vs realized variance** (CBOE VIX vs S&P 500 realized variance). Log-variance is rough (H ≈ 0.1 per Gatheral et
   al. 2018, α ≈ 1.2): Prop. 3 predicts positive kernel weights with tail ≈ τ^{−1.6} on past log realized variance.
3. **Wikipedia pageviews vs editing** (public dumps) and **GitHub upstream/downstream** (QUEUE GITHUB-UPSTREAM) as event
   worlds: test the two-exponent split out of sample.
Cross-scale candidates without verified public data: bacterial chemotaxis adaptation time vs ligand correlation time;
retinal adaptation under designed α stimuli (a new lab dataset would be needed). Fairhall et al. 2001's slope 1 under
deterministic periodic switching is outside this map (a predictable periodic world is not a stationary random spectrum).

## 5. Q1 gap-fill (prior-art sweep)
Night-1 already swept forward citations of M&R 1972, VZR 2001, Eppen, Reis 2006, V&W 2007 and Veldkamp 2011
(`/workspace/gtao/night1/REVIEW/priorart/SWEEP.md`, not in this repo; summarized in `priorart/NOTES.md`). This run filled
the two missing seeds and SG's prior art; see `priorart/NOTES.md`. Google Scholar remains unswept.

## 6. Files
`checks/fgn.py` (Davies–Harte), `c1_readrate`, `c2_filter`, `c3_layers` (per-α outputs), `c4_d3_renewal`,
`c4b_match1_renewal`, `c5_lfk`, `d3s_shuffle` (+ `.out`/`.json`); `PREREG_D3S.md`; `priorart/`. Run with
`nice -n 19 python3 checks/<file>.py` (numpy, scipy). `d3s_shuffle.py` needs blobless clones of the 12 repos as arguments.
