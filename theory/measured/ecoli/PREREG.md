# ECOLI-MEM preregistration: does E. coli's slow (methylation) layer have the memory the theory says it should?

Written Friday 20 November 2026, about 8:19 AM ET (America/New_York), by a Grok Bot executor for Chad, on branch
`v2.5-measure` off `b8e8d5b`. Locked by the pushed commit that adds this file and `ecoli_calc.py`; `LOCK.txt` holds
their sha256. **`ecoli_calc.py` had not been run when this was committed** (only `python3 -m py_compile`).
Theory version: THEORY.md v2.4 draft (Model S of `theory/LAYERS.md`, L1/L2/CT21; the CT30 smoothing rule; §5 (iii)
"every layer runs faster than its mode").

## 0. What I had already seen before locking (disclosed; this is NOT a blind test of the outcome)
From Mattingly, Kamino, Machta & Emonet 2021 (Nat Phys 17:1426, doi 10.1038/s41567-021-01380-3; open copies on PMC8758097
and the Emonet lab site), main text and Supplementary Table S1: **the outcome, τ2 = 9.9 ± 0.3 s** (CheA kinase adaptation
time, FRET, n = 442 cells, 100 µM MeAsp); τ1 = 0.22 ± 0.01 s (fit, includes switching and CheY/CheZ binding) and the
literature kinase time 0.017 ± 0.004 s; G = 1.73 ± 0.03; x-velocity autocorrelation V(t) = a_v e^{−λ|t|} with
a_v = 157.1 ± 0.5 µm²/s², λ = 0.862 ± 0.005 s⁻¹ (τ_v = 1.16 s); kinase noise OU with σn = 0.092 ± 0.002,
τn = 11.75 ± 0.04 s; β = 0.225 bits/s/mm⁻²; drift χ = 4300 µm²/s; efficiency η = 0.65; gradients 0.1–0.4 mm⁻¹.
Their reading: the information relevant to climbing is about the *current* signal, and responding to signals several τ_v
in the past transmits irrelevant information.
**Back-of-envelope done before lock (in my head, not in code):** under every noise model below the optimum memory looked
to be of order 1 s or less, against the measured 9.9 s, so I expect FAIL on the timing arms, and I expect the Arm-A premise
check to fail because τn/τ2 ≈ 1.19 (already seen). I say so now. What I have **not** computed: any predicted number, the
Berg–Purcell share of the measured noise, or arm C.

## 1. Theory → proxy (causal first principles)
- **World.** Along a swimming path the cell reads x(t) = ln c(x(t)). In a shallow static gradient g, u = dx/dt = g·v_x is
  Ornstein–Uhlenbeck with rate λ and variance σ_u² = g²·a_v (Mattingly's own signal model). So x is an integrated OU: a
  world of McMillan degree 2 (poles 0 and λ).
- **Target and loss.** The decision-relevant quantity is the current u (Mattingly SI §5: the relevant bits are "how fast the
  concentration is currently changing"). Quadratic loss on the estimate of u(t); lead 0. This is the theory's Model S
  objective with the target set to the decision variable.
- **Design.** A causal linear estimator from noisy reads. The slow layer is the methylation store; its memory time is the
  slowest decay time of the design (1/τ2 is the slow pole of the measured kernel K(t) = G e^{−t/τ2}(1 − e^{−t/τ1})).
- **Theory statements tested.** (T) the slow layer's memory is the optimum of J at the measured world and noise (CT30
  rule λ\* ≈ √(q/r) is the low-SNR limit of arm A's slow pole); (S) a degree-2 world gets a 2-store design (CT21/L2).

## 2. Arms (all three computed; verdicts only for A and B)
- **Arm A — read noise at the physical floor.** y = x + white noise of density r = k_BP/(D·a·c) (Berg & Purcell 1977
  counting noise in ln c). Optimal filter = steady-state Kalman–Bucy for (x, u); slow memory τ_A\* = 1/(smallest real part
  of the filter poles), fast = 1/(largest). Checked two ways (quartic p⁴ − λ²p² + 2λσ_u²/r = 0, and Riccati integration).
- **Arm B — measured noise referred to the signal as white noise.** The kinase noise (OU, σn, τn) is referred to the
  signal s = u through the kernel's DC gain K0 = Gτ2²/(τ1+τ2): N_s = 2σn²τn/K0² (this uses τ2 only to convert units;
  disclosed). One OU mode in white noise: optimum is one store with τ_B\* = 1/(λ√(1+SNR)), SNR = 2σ_u²/(λN_s)
  (Model S, L1; Wiener).
- **Arm C — diagnostic only, no verdict.** Store noise of fixed stationary variance (so its input-referred variance scales
  as (τ2/τ)²); best single store with free gain.
- **Rival R1 ("set at", the reading the headline was reworded to avoid):** memory = the world's time scale, τ = τ_v = 1/λ.
- **Rival R0 (no relation):** not scorable with one system; reported only.

## 3. Inputs and the box of uncertainty (fixed now)
Measured inputs at ±2 s.e. (above). g ∈ {0.1, 0.2, 0.3, 0.4} mm⁻¹ (the paper's gradients); c = 100 µM. **Assumed ranges
(not from the source; stated as assumptions):** ligand diffusion D ∈ [500, 1000] µm²/s; effective sensing radius
a ∈ [0.5, 1.0] µm; counting-noise prefactor k_BP ∈ [1/(4π), 1/π] (the order-one constant differs between the
perfect-monitor and maximum-likelihood/absorber results; Berg & Purcell 1977; Endres & Wingreen 2009). Each arm's
prediction is the range [L, U] of τ\* over every corner of the box.

## 4. Verdict rules (per arm), measured interval M = τ2 ± 2 s.e. = [9.3, 10.5] s
- **PASS** iff M ⊂ [L/2, 2U] and τ_v ∉ [L/2, 2U]; **PASS-NONDISCRIMINATING** iff M ⊂ [L/2, 2U] and τ_v ∈ [L/2, 2U].
- **FAIL (on this proxy/setup)** iff M lies wholly outside [L/3, 3U].
- **INCONCLUSIVE** otherwise.
- **Rival R1:** FAIL iff τ2/τ_v ∉ [1/3, 3]; PASS iff ∈ [1/2, 2].
- **Premise checks.** Arm A assumes read noise binds. It is labelled **INVALID as a test of the claim** (reported, not
  scored) if the measured noise has the store's own time constant (|ln(τn/τ2)| ≤ ln 1.5) or if Berg–Purcell noise
  accounts for < 10% of the measured kinase-noise variance. Arm B assumes the store noise does not depend on the store's
  speed; that cannot be checked here, so arm B's verdict is **conditional** on it.
- **Structure S1:** PASS (structural) iff the measured kernel is fitted by exactly two stores and the world's degree is 2;
  it is non-discriminating against R1 (which also counts two scales) and discriminates only against a one-store design.

## 5. What a miss will and will not mean (fixed now, per Chad's guidance relayed 8:13 AM ET)
A FAIL here is "failed on this proxy/setup". Before any conclusion I will diagnose the cause among: (i) proxy (is τ2 the
slow layer's memory? is u the cell's target?), (ii) measured inputs (lab world: 100 µM, static gradient, laboratory strain),
(iii) a model assumption (world spectrum: the lab gradient lacks the habitat's slow modes; a missing cost term, e.g. the
dissipation of a fast store, Lan et al. 2012; the loss: Clark & Grant 2005 steady-state accumulation), (iv) the selection
condition (a lab strain selected in semisolid agar), or (v) the claim. The diagnosis may not change these predictions; any
new prediction is preregistered fresh in a separate file before it is computed. Kill conditions of THEORY §8 apply only to a
qualifying strongly selected system with a preregistered band and cost list; this test does not meet that bar (no closed
cost list, no fitness map), so **no outcome of this file can refute the hypothesis for the class**.

## 6. Prior art (credited)
Optimal filtering in chemotaxis is not new: Andrews, Yi & Iglesias 2006 (optimal noise filtering, cutoff frequency);
Strong, Freedman, Bialek & Koberle 1998 (adaptation and optimal strategy); Clark & Grant 2005 (response-function
compromise); Celani & Vergassola 2010 (minimax response); Becker, Mugler & ten Wolde 2015 (optimal prediction);
Mattingly et al. 2021 (information limit). DOIs are verified on Crossref in `../SOURCES.md` before results are written.
What would be new: scoring the *theory's* general rule (memory set by the world's spectrum and the noise; layers faster
than their mode) against measured inputs with a stated rival, as one entry of a cross-scale test.
