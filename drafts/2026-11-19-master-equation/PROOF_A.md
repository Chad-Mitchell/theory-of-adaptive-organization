# PROOF_A: when do layers beat one flat tracker? (claims A and B)

Written 19 Nov 2026, about 10:30 PM ET, by a Grok Bot executor for Chad (via Ace). Read-only research: nothing in the theory repo was edited, committed or pushed. Repo read: `/workspace/gtao-read` at main `5b65c1e`. Scripts: `checks/` (run at nice 19). Status words follow the repo: **PROVED (in-model)**, **KNOWN**, **NUMERICAL**, **CONJECTURE**. Not reviewed by anyone else yet.

## 0. What the repo already proves, and what it does not

| Claim | Repo status | Where |
|---|---|---|
| (A) "nested beats flat" in general | **Not a theorem.** "'Nested beats flat' is not one theorem" and "There is no theorem that nested is always better" | `theory/THEOREMS.md` l.60–62, l.111 |
| (A) on the member axis: one shared level for N members with common driver | **PROVED**, exact iff in the class 𝒜₁: level pays iff N > N\*(ρ) | THEORY.md Result 4, l.110–117; `reviews/night1/formal/THEOREMS.md` Thm 1, l.56–90 |
| (A) many levels on the member axis | **PROVED**: cost submodular (levels are complements), inclusion, lattice, accretion as upkeep falls; cheaper lookup can dissolve levels | formal Thm 6, l.223–252 |
| (A) which scales of a nested tree carry a level | **PROVED**: top-down iff κ < κ\* = (1−a)/(1−b) (h = 0). Here κ is a drift-sharing exponent, not THEORY's price per nat | formal Thm 7, l.256–281 |
| (A) on the time axis, separate clocks for separately readable parts | **KNOWN**: saving ≤ 1 − K^{−(1−γ)} (29% for two levels); **zero** with indivisible reads | formal Prop 9, l.312–314; `theory/THEOREMS.md` T3b l.82–86 |
| (A) on the time axis, decoupled nesting vs flat filter | **NUMERICAL** only: nesting is near optimal when scales separate, and loses when they collapse | `theory/THEOREMS.md` T3c l.88–111 |
| (A) on the time axis, number of memory stores | **KNOWN** (one store exact iff the spectrum is first-order; finitely many iff rational) + **CONJECTURE** for the rate K\* ≈ (ln 8R/2π²)·ln(stakes/upkeep) | `reference/THEORY_v1.4.29.md` l.85, l.110–114, l.127; CLAIM_MAP K12 l.335 |
| (B) geometric levels | **PROVED** only in T7b's shared-clock model, log-uniform items, α = 2 penalty; withdrawn as unconditional; LAYERS1 P2 (span invariance of spacing) **SIM-FAIL** | `theory/THEOREMS.md` l.175–204; CLAIM_MAP G20 l.239, K12 l.335 |

So on the **time axis** (Chad's "fractal time ⇒ layers"), the repo has the pieces but no clean statement of when layers beat flat. Below is one.

## 1. Model S (time axis)

- **World.** s(t) = Σ_j s_j(t), independent stationary Gaussian components. The basic case is a sum of J Ornstein–Uhlenbeck modes, autocovariance v_j e^{−a_j|t|}, spectrum S(ω) = Σ_j 2a_j v_j/(a_j² + ω²). The random walk (spectrum q/ω², α = 2) is the a → 0 limit of one mode.
- **Sensing.** y(t) = s(t) + white noise of density N > 0 (the sensing-noise version of THEORY's read price; Lemma B2's setting).
- **Design.** A causal linear time-invariant estimator of s(t + k), with lead k ≥ 0 (acting ahead). A **K-layer design** is one whose realization has state dimension (McMillan degree) ≤ K: K separately timed stores or trackers. The numerical family is K parallel exponential trackers, H(ω) = Σ_k g_k b_k/(b_k + iω), one per timescale 1/b_k.
- **Cost.** J_K = h·K + w·E_K(k), with h the upkeep of a layer (part 1), w the stake on squared error (part 2), and the sensing cost carried by N (part 3). E_K is the least mean squared error over K-layer designs, and E_∞ is the causal MMSE.
- Define the **flat penalty** ε_K = E_K/E_∞ − 1 and **R = w·E_∞/h** (stakes × unavoidable error ÷ upkeep of one layer; THEORY's ψ).

## 2. Results

**Theorem L1 (one timescale ⇒ one layer). PROVED (in-model); the content is KNOWN (Kalman–Bucy 1961).** If the world has a single-pole spectrum (one OU mode, or a random walk), then E_1(k) = E_∞(k) at every lead k. So K\* = 1 for every w and h.
*Proof.* The Kalman–Bucy filter for a scalar first-order state is one exponential store. The best predictor at lead k is e^{−ak}·ŝ(t) for OU, and ŝ(t) for the random walk, which still has degree 1. ∎
**Consequence.** A random walk (Brownian motion) is the textbook self-similar, "fractal" process, and it needs **one** layer. So "scale-free change ⇒ layers" is false at α = 2. The one tracked series in the repo with a validated α estimate, the 10-year Treasury yield, is exactly this case: α̂ = 2.00 ± 0.03 with no corner over periods from 2 days to 37 years, on proxy (`measurement/estimators/RESULTS.md` l.12, l.78; `reviews/night2/AQN_REFEREE.md` V4).

**Theorem L2 (J timescales ⇒ at most J layers, and exactly J when stakes are high). PROVED (in-model) at k = 0; "≤ J" proved at every lead.** Let s be a sum of J OU modes with distinct rates a_j and v_j > 0.
- (i) For every lead k the MMSE estimator has degree ≤ J, so K\* ≤ J for every w and h.
- (ii) At k = 0 its degree is **exactly J**. So E_K > E_∞ for every K < J, and K\* = J once R is large enough.
- (iii) Layers beat flat (K\* ≥ 2) **iff** w(E_1 − E_K) > h(K − 1) for some 2 ≤ K ≤ J. Equivalently, R > R\* := min_K (K − 1)/(ε_1 − ε_K). A sufficient condition is R·(ε_1 − ε_2) > 1.

*Proof.*
- (i) The state (s_1, …, s_J) is a J-dimensional linear Gaussian system, so the Kalman–Bucy estimate has dimension J. The predictor is Σ_j e^{−a_j k} ŝ_j(t).
- (ii) Write S(ω) + N = P(ω²)/Π_j(ω² + a_j²), where P(x) = NΠ_j(x + a_j²) + Σ_j 2a_j v_j Π_{i≠j}(x + a_i²). At x = −a_k², P = 2a_k v_k Π_{i≠k}(a_i² − a_k²) ≠ 0, so no root of P is at −a_k². Write P(ω²) = NΠ_j(ω² + b_j²) with Re b_j > 0. The causal spectral factor is G⁺ = √N·Π(iω + b_j)/Π(iω + a_j), and the Wiener filter is H = 1 − √N/G⁺ = [Π(iω + b_j) − Π(iω + a_j)]/Π(iω + b_j). At iω = −b_k the numerator is −Π_j(a_j − b_k) ≠ 0 (no b equals an a), so there is no pole–zero cancellation, and H has degree exactly J. The causal MMSE estimator is unique (an L² projection), so any design of degree < J has strictly larger error.
- (iii) Compare J_1 with min_{K≥2} J_K. ∎

At k > 0, "exactly J" is not proved for every lead. In every case computed, K = J was exact and K = J − 1 was strictly worse (`checks/lead.out`).

**Theorem L3 (a continuum of timescales ⇒ no finite number of layers is exact). PROVED (in-model) for the strictness; the limit is CONDITIONAL.** If S is not a rational function of ω (fBm with H ≠ ½, or any continuous mixture of timescales, such as a band-limited f^{−α} with α ≠ 2), then E_K > E_∞ for every finite K. If also E_K → E_∞ (rational approximation of the Wiener filter; the repo cites Braess & Hackbusch 2005/2009 and Jiang et al. 2017 for the rate, as a CONJECTURE for this kernel), then K\*(R) → ∞ as R → ∞.
*Proof.* If H were rational, then G⁺ = √N/(1 − H) would be rational, so S + N = |G⁺|² would be rational. Contradiction. ∎
This is the clean form of the repo's "finitely many exponential stores are exact iff the spectrum is rational" (`reference/THEORY_v1.4.29.md` l.127, KNOWN).

**Proposition L4 (B in the shared-clock model holds at every α). PROVED (in-model), extending T7b.** Items have natural intervals spread log-uniformly, and K shared clocks each serve a contiguous log-band. Running an item at k·T\* costs the relative penalty p(u) = [(α−1)e^{−u} + e^{(α−1)u}]/α − 1, with u = ln k (THEORY CT13). Then **equal log-widths, i.e. geometric levels, are optimal for every α in (1, 3)**, not only α = 2.
*Proof.* p is strictly convex with its minimum p(0) = 0. One band of log-width Δ costs ψ(Δ) = min_y ∫_0^Δ p(x − y)dx. It depends only on Δ, because the penalty depends only on the ratio. At the optimum p(−y\*) = p(Δ − y\*) =: c(Δ), and by the envelope theorem ψ′(Δ) = c(Δ). For a strictly convex p, the two points where p equals c move apart as c rises, so their distance Δ is strictly increasing in c. Hence c(Δ) is increasing, ψ is strictly convex, and Jensen's inequality makes equal widths optimal for fixed K. ∎
Check: `checks/t7b_alpha.out` (optimal widths equal to 4 decimals at α = 1.2, 1.5, 2, 2.5 and 2.9; ψ convex on a grid). For small Δ, ψ ≈ C_α·Δ³, so with total base cost C and upkeep h per clock, K\* ∝ (C/h)^{1/3}·L^{2/3}. That is the withdrawn T7b count. It is **correct inside this clock model**. It was withdrawn because the memory-store model gives a different count, so the two "layer" objects must not be mixed.

## 3. Numerical results (Model S; `checks/stores.py`, `experiments.py`, `lead.py`, `maxgain.py`)

**Formula checks** (`checks/stores_checks.json`): K = 1 on one OU mode reproduces the Kalman value 0.158853 to 7 digits, and the Yovits–Jackson MMSE integral agrees (0.158853). A Monte Carlo of a two-store design on a two-mode world gives 0.3295 against the closed form 0.3256 (1.2% gap, from the dt = 0.01 discretization).

**L1 numerically.** One mode: ε_2 = ε_1 ≈ 10⁻⁶ (optimizer tolerance).

**Two modes separated by a ratio r (equal variance, k = 0).** Flat penalty ε_1, and the threshold R\* = 1/ε_1 above which two layers pay:

| r | 1.5 | 3 | 10 | 100 | 10⁴ |
|---|---|---|---|---|---|
| ε_1 | 0.002% | 0.10% | 0.96% | 3.7% | 5.8% |
| R\* | 4.2×10⁴ | 1.0×10³ | 104 | 27 | 17 |

**Cadence world (modes at τ = 1, 30, 1000).** ε_1 = 3.9%, ε_2 = 0.08% and ε_3 = 0 (L2). K\* = 1, 1, 2, 2, 3, 3 at R = 1, 10, 10², 10³, 10⁴, 10⁶. The optimal layers sit at 0.22, 5.5 and 176: one per cadence, each **faster** than its mode (the b_j of L2, shifted by the sensing noise), not at the cadences themselves.

**Scale-free band** (S ∝ f^{−α} inside the span, built as a dense Lorentzian mixture, 8 modes per decade; noise crossing at the fast edge). Flat penalty ε_1 and K\* at R = 10, 10², 10³, 10⁴:

| α | span 10 | 10² | 10³ | 10⁴ | 10⁵ | K\* at span 10⁴ |
|---|---|---|---|---|---|---|
| 0.5 | 0.28% | 1.24% | 1.87% | 2.13% | 2.21% | 1, 2, 3, 4 |
| 1.0 | 0.32% | 1.79% | 3.32% | 4.36% | 5.01% | 1, 2, 3, 4 |
| 1.5 | 0.28% | 1.26% | 2.00% | 2.32% | 2.43% | 1, 2, 3, 4 |
| 1.9 | 0.20% | 0.59% | 0.58% | 0.44% | 0.33% | 1, 1, 2, 3 |

- K\* rises with span (at R = 10⁴: 2 at span 10, 3 at 10², 4 at ≥ 10³, the cap of K ≤ 4) and with R. This is qualitatively the repo's ln(span)·ln(stakes/upkeep), but not a fit of its rate.
- Near α = 2 the penalty shrinks, as the repo's c(α−2)² knife edge says.
- Two layers pay at α = 1 once R > about 22–58 for spans of 10²–10⁵, and once R > about 300 at span 10.

**Acting ahead** (`checks/lead.out`): the penalty is largest at short leads. In the two-mode world it is 9.3% at k = 1 against 5.2% at k = 0, then it falls (the fast part is unpredictable at long leads, so only the slow tracker matters). Scale-free α = 1, span 10⁴: 4.4%, 4.8%, 2.9% and 1.2% at k = 0, 3, 30 and 300.

**How big can the flat penalty get?** (`checks/maxgain.out`; two modes at τ = 1 and 10⁴, scanning the slow share, noise and lead.) The largest penalty found was **20.4%**, at a 90% slow share, moderate noise and k = 0. Typical values were 2–10%.

**(B) in the store model** (`experiments.out` Exp3). The optimal 4-layer timescales are roughly log-spaced, each 3–20× the one below. They are **not** equally spaced: the log10 ratios widen from 0.5–0.7 to 1.1–1.3 decades toward the slow end, and they depend on span and noise. That is consistent with LAYERS1 P2's SIM-FAIL ("spacing not span-invariant at finite precision").

## 4. Plain statement of what is now proved, checked or failed

- **Proved (in-model, linear-Gaussian, noisy sensing; this note; not yet independently reviewed):**
  - L1: one timescale ⇒ one layer, **including the scale-free random walk**.
  - L2: J timescales ⇒ at most J layers, exactly J at high stakes/upkeep, with an exact iff threshold R\*.
  - L3: a continuum of timescales ⇒ no finite number of layers is exact.
  - L4: geometric clocks are optimal at every α in the shared-clock model.
- **Checked numerically only:**
  - how R\* and K\* depend on span, α, noise and lead;
  - the size of the flat penalty (≤ about 20% in the scans);
  - near-but-not-exact log spacing in the store model;
  - exact degree J at leads k > 0.
- **Not proved:**
  - a closed-form L\*(h, c, w, α) or K\*(span, R) rate (the repo's ln·ln rate stays a CONJECTURE);
  - anything for non-Gaussian (jump) worlds, nonlinear Bayes trackers or other losses;
  - that the layers must be separate **agents** rather than separate stores inside one agent.
- **What failed:** the naive claim "scale-free ⇒ layers" (L1 is a counterexample), and "layers are exactly geometric" in the memory-store model.
- **What this does not change:** on the time axis, layering buys single digits to about 20% of the error cost per tracker in these worlds. The repo's clock result caps one extra clock at 29%. The large multipliers in the theory come from the **member axis**: pooling saves about N reads for one, and the lookup cliff.

## 5. Prior art (each marked)

- **Verified** (DOI resolved via Crossref this session, `checks/cites_crossref.out`):
  - Roundy 1985 (Mgmt Sci 31:1416; geometric power-of-two clocks);
  - Benna & Fusi 2016 (Nat Neurosci, doi 10.1038/nn.4401; multi-timescale synaptic memory);
  - Fusi, Drew & Abbott 2005 (Neuron; cascade memory);
  - Willsky 2002 (Proc IEEE; multiresolution Markov models);
  - Kiebel, Daunizeau & Friston 2008 (PLoS Comput Biol; brain hierarchy of time-scales);
  - Murray et al. 2014 (Nat Neurosci; a hierarchy of intrinsic timescales across primate cortex; abstract read);
  - Shankar & Howard 2012 (Neural Comput; scale-invariant representation of time).
- **Credited in repo, not re-checked here:**
  - Simon 1962 "The Architecture of Complexity" (Proc Am Philos Soc 106:467; no DOI; THEORY §8);
  - Simon & Ando 1961;
  - Tikhonov; Borkar 1997;
  - Braess & Hackbusch 2005/2009; Jiang et al. 2017.
- **Standard results used:** Kalman–Bucy 1961, Wiener–Hopf spectral factorization and the Yovits–Jackson MMSE formula. These were checked numerically here, not re-read.
