# C12c: memory onset as a function of stake and buffer (paper derivation)

*26 Nov 2026, Forge. Local notes only; nothing committed or pushed. Repo text read at `499ef04` (fresh clone `/workspace/qmsel3-run`). Checks: `c12c_check.py` → `c12c_check.out`; DOIs: `crossref_c12c.py` → `crossref_c12c.txt` (all 12 found on Crossref this session). Self-checked by the author only; it needs a hostile review before any of it counts.*

Labels: **KNOWN** (published), **PIM** (proved in-model, here or in the repo), **OBS** (numerical observation), **HYP** (hypothesis/reading). Nothing here is a claim about real physics or living systems.

---

## 0. Bottom line

1. **Ace's sentence holds in-model, with one condition.** A stake-free accuracy cap E ≤ D is priced by its Lagrange multiplier μ, and the constrained design is the unconstrained design at stake w + μ (PIM, §2). The condition is convexity: when the menu is non-convex (discrete worlds, discrete layer counts) and mixtures aren't allowed, a cap can select a design that no stake selects (the duality gap). The repo already has the three-point example (CLAIM_MAP V6). So the honest wording is "a required accuracy acts as a stake on the convex hull of the menu".
2. **Onset is a union, and the effective stake is a max** (PIM, Theorem O, §3). Memory is on iff w > w₁ (CT4's threshold) **or** the cap is tighter than the blind error. The memory held is max(x_w, x_D), and the effective stake is max(w, w\*(D)).
3. **The C12c HYP in STEPBACK §11 is half wrong, and this is the main correction.** There are two kinds of ruin cap in the repo, and they behave in opposite ways:
   - **Stake-free caps** (CT25 type: ruin when the tracked error reaches the buffer) inject an effective stake even at w = 0. At zero stake, memory is absent **iff** the blind design meets the cap (PIM). This answers gate C13-5 in this class.
   - **Stake-carrying caps** (CT22 type: a Lundberg cap on a reserve that pays w·loss). These cannot force memory at w = 0. On CT22's path the binding band [B_min, B_slack] shrinks to zero width as w → 0 (PIM, limit argument §4.3; OBS width ≈ √w). So "a world with a binding ruin cap needs memory at zero stake" (STEPBACK §11) is **false** for CT22's cap and true only for stake-free caps.
4. **The core is KNOWN mathematics:** Everett 1963 (generalized Lagrange multipliers), KKT, the rate–distortion slope parametrization (Blahut 1972), IB learnability thresholds (Wu et al. 2019), and chance-constrained programming (Charnes & Cooper 1959). What is ours is only where it lands in GTAO: the split into stake-free vs stake-carrying caps, the corrected zero-stake floor, and closed forms in CT4's and CT25's classes.
5. **A lead on "what plays the stake for bare physics" (HYP reading of KNOWN results, §6).** In Still 2020's two-temperature information engine, the bound is −Q ≥ k(T·I_mem − T′·I_rel). That is an IB Lagrangian whose stake is the temperature ratio T′/T. For a scalar Gaussian signal, a memory can show net gain only if T′/T > 1/ρ² ≥ 1 (PIM on paper, from Still's bound). At a single temperature it never pays: the zero-stake floor. This is a reading, not a derivation of anything physical.
6. **This is not a breakthrough.** It is a clean, cheap sharpening. C12c rescored (§8): the residual step, a hostile review, is ≈ 2.0 per hour. The whole route, including the sunk paper work, is ≈ 0.8 per hour. The recommended next step is a hostile review, then a small Lean lemma (§5).

---

## 1. Repo text used (quoted from `499ef04`, not paraphrased)

- **CT4** (THEORY.md:279; CLAIM_MAP_v2.md:525, PROVED (in-model)): "Let IB(I) = sup{I(M; X_{t+k}) : I(M; past) ≤ I}, the predictive information-bottleneck curve (concave, nondecreasing). Then L(I) = D(IB(I)) + κI is a convex lower bound on cost at memory size I, and its minimizer is positive iff κ < −(D∘IB)′(0⁺). For a Gaussian AR(1) world … a model is carried iff κ < 2 ln 2·a²·Var, and then I\* = ½ log₂(2 ln 2·a²·Var/κ)." The proof (:281) uses "the best memory is a noisy copy of X_t", so prediction loss is Var[(1 − a²) + a²·2^{−2I}].
  - CT4 carries no explicit w; the loss has unit weight. With a stake w on the loss, the condition reads w > w₁ := κ/(−(D∘IB)′(0⁺)), which in the Gaussian case is w₁ = κ/(2 ln 2·a²·Var). This is the same statement rescaled (κ → κ/w).
- **CT18** (THEORY.md:392; CLAIM_MAP:539): "the hazard is ν = F(z)/τ with z = B/(σ√τ), for some function F fixed by the fixing mechanism" (Buckingham π).
- **CT22** (THEORY.md:440–460; CLAIM_MAP:555, PROVED (in-model) on the scalar diffusion path):
  - "B_min = ln(1/ε_r)/max_𝒟 θ and B_slack = ln(1/ε_r)/θ(𝒟_E)".
  - The path is J(τ) = c/τ + ατ with α = wσ²/2, margin m = y − J, variance rate s² = s₀² + βτ³ with β = w²σ⁴/3, and θ = 2m/s².
  - "For B ≥ B_slack the constraint is slack and 𝒟_E is optimal (multiplier μ_s = 0)"; in between, "μ_s = −m′/θ′ > 0".
  - Its hypotheses include α > 0 and β > 0, so **CT22 does not cover w = 0 itself**.
- **CT25** (THEORY.md:402; CLAIM_MAP:558): "per-window ruin P = erfc(z/√2) (Lemma B8), P ≤ ε_r iff z ≥ z_ε := Φ̄⁻¹(ε_r/2), which is 2.576, 3.291 and 4.892 for ε_r = 10⁻², 10⁻³ and 10⁻⁶. So, for each fixing window, the buffer must satisfy B ≥ z_ε·σ√τ". THEORY:186 says it "is not" CT22's lifetime-ruin constraint.
- **CT33** (THEORY.md:495; CLAIM_MAP:566): monotone comparative statics hold if "the design set must not depend on w: the ruin constraint must be slack at the stakes compared (B ≥ B_slack, CT22) or absent". It fails under CT22 because "the reserve pays J and the variance of realized loss scales with w²".
- **V6** (CLAIM_MAP:716): "If the set is convex, every Pareto point minimizes some nonnegative weighted sum … Without convexity the three-point set A=(0,1), B=(1,0), C=(0.6,0.6) is Pareto and is the minimum of no nonnegative weight".
- **CORE.md:27, :29**: J = Q̇ + w·E[ℓ] subject to P(ruin) ≤ ε; "w converts the loss into the currency of the heat. Temperature does not set w."
- **Record-cost chain** (theory/RECORD_COST_CHAIN_2026-11-25.md:62): "The stake q = 4 is the session's convention, not derived". Line 60: rivals win again "above q ≈ 7.7 (pairs) and q ≈ 12.4–17.6 (single systems)".
  - So in that round the stake was named, not hidden. It was chosen by hand, and the selected world depends on it.
  - Ace's point applies with a small edit: the stake was never set by the theory. Under §2, a required tracking accuracy would set it, as w\*(D).

## 2. Task 1: an accuracy cap is an effective stake (Lagrange dual)

**Setting (general).** A design set 𝒟, spend S(d) ≥ 0 and error E(d) ≥ 0, stake w ≥ 0, and a **stake-free** cap E(d) ≤ D. Stake-free means the feasible set {E ≤ D} does not depend on w.

**Lemma A (KNOWN; Everett 1963, Thm 1; restated).**
- (a) If d° minimizes S + λE over 𝒟 for some λ ≥ 0, then d° minimizes S over {E ≤ E(d°)}.
- (b) Conversely, let d\* minimize S + wE over {E ≤ D}. Suppose the point (E(d\*), S(d\*) + wE(d\*)) lies on the lower convex hull of the attained set {(E, S + wE)}, which always holds when the attained set's free-disposal hull is convex (V6, S3(ii)). Then there is μ ≥ 0 with μ(E(d\*) − D) = 0 such that d\* minimizes S + (w + μ)E over 𝒟 with no cap.

*Proof.*
- (a) If E(d) ≤ E(d°) and S(d) < S(d°), then S(d) + λE(d) < S(d°) + λE(d°), a contradiction.
- (b) Let h(E) be the lower convex envelope of the attained points {(E(d), S(d))}. Write E\* = E(d\*). Constrained optimality, with d\* on the envelope, means E\* minimizes the convex function h(E) + wE over E ≤ D. The 1-D KKT argument (as in Theorem O(iii), §3.1) gives a subgradient −(w + μ) of h at E\* with μ ≥ 0 and μ(E\* − D) = 0. If E\* < D, then μ = 0. The line with that slope through (E\*, S(d\*)) supports every attained point, so d\* minimizes S + (w + μ)E over 𝒟.
- ∎ (The textbook KKT/separating-hyperplane argument; V6 already proves the scalarization half in the repo.)

**Reading.** The required accuracy D is priced at μ\*(D). The constrained design is the one an unconstrained optimizer picks at the **effective stake w_eff = w + μ\*(D)**. That is Ace's sentence. *Condition:* it holds on the lower convex hull. With a non-convex menu, for example a discrete set of worlds or layer counts with no mixing, a cap can select a design no stake selects; V6's point C is that case. **PIM** (as an application of KNOWN mathematics).

**Consequence for CT33 (PIM, already covered by V3).** The cap is stake-free, so the menu {E ≤ D} doesn't depend on w, and CT33 holds on it as is. The ruin-cap caveat in CT33 is needed only for **stake-carrying** caps such as CT22's.

## 3. Task 2 and 3: the onset surface, and Theorem O

### 3.1 Theorem O (1-D onset; PIM on paper here; KNOWN in substance)

Let f : [0, ∞) → [0, ∞) be convex, nonincreasing and continuous. f(x) is the error at judgment resource x (bits held, or check rate). Let κ > 0 be the price per unit x, w ≥ 0 the stake, and the cap f(x) ≤ D with inf f < D. Define:
- x_w := the least minimizer of g_w(x) = w·f(x) + κx on [0, ∞). It exists because κ > 0 and f ≥ 0 make g_w coercive.
- x_D := min{x : f(x) ≤ D}. It exists because f is continuous and nonincreasing, so {f ≤ D} = [x_D, ∞).
- w₁ := κ/(−f′(0⁺)), read as +∞ if f′(0⁺) = 0 and as 0 if f′(0⁺) = −∞.

Then:
- **(i) Projection.** The least minimizer of g_w on {f ≤ D} is **x\* = max(x_w, x_D)**.
- **(ii) Onset is a union.** **x\* > 0 ⇔ w > w₁ or D < f(0).**
- **(iii) Effective stake.** If x_D > x_w, the cap binds and μ = κ/|f′(x_D⁻)| − w > 0 is a KKT multiplier. Then x_D minimizes g at stake w\*(D) := κ/|f′(x_D⁻)| with no cap (it is the least minimizer if f is strictly convex). So **w_eff = max(w, w\*(D))**.
- **(iv) Monotone, and the corner meets.** w\*(D) is nonincreasing in D, and w\*(D) → w₁ as D ↑ f(0).
- **(v) Zero-stake floor, stake-free cap.** At w = 0, x\* = 0 ⇔ D ≥ f(0): memory is absent **iff the cap is slack at the blind design**.

*Proof.*
- **(i)** The argmin of the convex coercive g_w on [0, ∞) is a compact interval [x_w, x_w′]. If x_D ≤ x_w′, the least feasible global minimizer is max(x_w, x_D). If x_D > x_w′: for x_w′ < x < y, convexity gives g(x) ≤ λg(x_w′) + (1−λ)g(y) < λg(x) + (1−λ)g(y), so g(x) < g(y). So g is strictly increasing on (x_w′, ∞), and x\* = x_D = max(x_w, x_D).
- **(ii)** x_w = 0 ⇔ 0 ∈ ∂g_w(0) ⇔ w·f′(0⁺) + κ ≥ 0 ⇔ w ≤ w₁. And x_D > 0 ⇔ f(0) > D. Combine with (i).
- **(iii)** x_D > x_w′ ≥ 0, so x_D is interior and g_w′(x_D⁻) > 0. If it were 0, then 0 ∈ ∂g_w(x_D) and x_D would be a global minimizer, against x_D > x_w′. So κ > w·|f′(x_D⁻)|, and f′(x_D⁻) < 0 because f > D to the left of x_D.
  - Take μ := κ/|f′(x_D⁻)| − w > 0. Then (w + μ)·f′(x_D⁻) + κ = 0, so 0 ∈ ∂[(w + μ)f + κx](x_D). That is stationarity, plus binding complementary slackness.
  - The same subgradient shows x_D is an unconstrained minimizer at stake w + μ.
- **(iv)** x_D is nonincreasing in D. f′(·⁻) is nondecreasing in x, so |f′(x_D⁻)| is nondecreasing as D rises, and w\* is nonincreasing. As D ↑ f(0), x_D ↓ 0 and f′(x_D⁻) → f′(0⁺), because convex left derivatives converge to the right derivative from the right. So w\* → w₁.
- **(v)** This is (ii) at w = 0. ∎

**What is new vs proved.** (ii) generalizes CT4's iff by adding the cap. CT4 is the case D ≥ f(0). The whole statement is a 1-D instance of Everett/KKT, so it is **KNOWN in substance**. Its role in GTAO is new: it turns STEPBACK's C12c HYP into a theorem for stake-free caps, and shows the HYP fails for CT22-type caps (§4.3).

### 3.2 Class A: CT4's Gaussian AR(1) with a per-step chance cap (PIM within linear-Gaussian memories)

The world is X_{t+1} = aX_t + η, with stationary Var, innovation variance σ_η² = (1 − a²)Var, κ per bit, and stake w on squared error. Ruin is one prediction error with |e| ≥ B, capped at ε per step.
- The memory is a Gaussian noisy copy of X_t (CT4's optimal memory), so the error is Gaussian with variance D(I) = Var[(1 − a²) + a²2^{−2I}].
- Then the chance cap is equivalent to D(I) ≤ D_B := (B/z_ε)², with z_ε = Φ̄⁻¹(ε/2). This is the same z_ε as CT25's per-window value (two-sided Gaussian = 2Φ̄, which matches erfc(z/√2) as a number).

Apply Theorem O with f = D(·):
- **Blind buffer B₀ = z_ε·√Var.** The blind design meets the cap iff B ≥ B₀.
- **Floor B_fl = z_ε·σ_η.** No design meets the cap below it; this is the analogue of B_min.
- **I_req(B) = ½ log₂( a²Var·z_ε² / (B² − z_ε²σ_η²) )** for B_fl < B < B₀.
- **w\*(B) = κ·z_ε² / (2 ln 2·(B² − z_ε²σ_η²))**. In terms of excess error Δ = D − σ_η², this is w\* = κ/(2 ln 2·Δ). It satisfies w\*(B₀) = w₁ = κ/(2 ln 2·a²Var), the CT4 threshold.
- **Onset surface:** memory is on iff w > w₁ or B < B₀. So **w_c(B) = w₁ for B ≥ B₀, and w_c(B) = 0 for B < B₀** (memory at every stake). The boundary is L-shaped with its corner at (w₁, B₀). The amount I\* = max(I_w, I_req) is continuous across it.
- **B_slack(w) = z_ε·√(σ_η² + κ/(2 ln 2·w))** for w ≥ w₁ (the regime line w = w\*(B)). It equals B₀ at w₁, is **decreasing** in w, and tends to B_fl as w → ∞.

*Checks* (OBS, `c12c_check.out` §1–2, a = 0.8, Var = 1, κ = 0.05, ε = 10⁻³):
- Brute force over I matches max(I_w, I_req) to 6×10⁻⁶ on a 1e-5 grid, in 42 (w, D) cases.
- The KKT w + μ equals w\*(D) to 10⁻⁴.
- w\*(D) is nonincreasing in D.
- Monte Carlo with 2×10⁶ draws gives per-step ruin 0.99–1.01×10⁻³ at I_req.
- z_ε = 3.291, matching CT25's 3.291.

*Scope (HYP):* the reduction from chance cap to MSE cap uses Gaussian errors, which hold for CT4's linear-Gaussian memory. Whether some non-Gaussian memory meets the **chance** cap with fewer bits is not shown, so the class-A closed forms are PIM only within linear-Gaussian memories.

### 3.3 Class B: CT18/CT25's reset path (random-walk error; PIM)

J(τ) = c/τ + wσ²τ/2, with the cap B ≥ z_ε·σ√τ ⇔ τ ≤ τ_max = B²/(z_ε²σ²). With x = 1/τ (check rate) this is Theorem O, with f(x) = σ²/(2x) convex and decreasing and f′(0⁺) = −∞, so **w₁ = 0**. Results:
- **τ\* = min(√(2c/(wσ²)), B²/(z_ε²σ²))**. Checking is on at every w > 0 (PD5's "no threshold"), and at w = 0 whenever B < ∞.
- **w\*(B) = 2c·z_ε⁴·σ²/B⁴.** Its form c·σ²·B⁻⁴·G(ε) is forced by dimensions (w has units cost/(time·x²)), exactly as in CT18. Only G(ε) = 2z_ε⁴ depends on the fix mechanism, so ε_B(w\*) = −4 **is not an informative prediction**.
- Check (OBS, §4): numerical τ\* matches the formula in 5 (w, B) cases.

So in class B, B₀ = ∞ and the onset surface is degenerate: memory is on everywhere except (w = 0, B = ∞).

### 3.4 Pieces: proved vs new

| piece | status | where |
|---|---|---|
| first-bit threshold w₁ (CT4) | PIM, repo | THEORY:279 |
| buffer as a z-cap; z_ε values (CT18, CT25) | PIM, repo | THEORY:392, :402 |
| CT22 band, B_min < B_slack, μ_s | PIM, repo (w > 0 only) | THEORY:440–460 |
| cap ⇔ effective stake (Lemma A) | KNOWN (Everett 1963); scalarization half already V6 | §2 |
| Theorem O (projection, union onset, w_eff = max, corner) | PIM here on paper; KNOWN in substance | §3.1 |
| class-A closed forms (B₀, B_fl, I_req, w\*, B_slack(w)) | PIM here, within linear-Gaussian memories | §3.2 |
| class-B w\*(B) = 2cz⁴σ²/B⁴ | PIM here; exponent forced by dimensions | §3.3 |
| CT22 band collapses as w → 0 | PIM here (limit; §4.3); width ≈ √w OBS | §4.3 |
| B_slack(w) rises with w on CT22's path | OBS at the published point only (7 stakes) | §4.3 |
| stake-free vs stake-carrying caps as the split for the zero-stake floor | new framing (HYP until reviewed) | §4 |

## 4. The split that matters: stake-free vs stake-carrying caps

### 4.1 Stake-free caps (CT25 type)
Ruin is decided by the tracked error against a buffer. The cap does not involve w. Theorem O applies: a binding cap supplies w\*(D) > 0 even at w = 0, so **memory can be forced at zero stake**. The zero-stake floor holds iff B ≥ B₀.

### 4.2 Stake-carrying caps (CT22 type)
Ruin is decided by a reserve that pays J, including w·loss, and whose variance scales with w² (THEORY:495). The cap tightens with w. More stake makes the cap bind **sooner** (OBS: B_slack(w) = 0.312, 0.315, 0.325, 0.336, 0.358, 0.400, 0.508 at w = 10⁻⁴ … 1, `c12c_check.out` §3). Under stake-free caps, more stake makes the cap slack sooner (§3.2, B_slack decreasing). **The two cap types have opposite monotonicity in w.**

### 4.3 CT22's band collapses at zero stake (PIM, limit argument)
On CT22's path, for every τ, θ(τ) = 2(y − c/τ − ατ)/(s₀² + βτ³) ≤ 2(y − c/τ)/s₀² < 2y/s₀². So θ(τ_S) < 2y/s₀² and B_min(w) > ln(1/ε_r)·s₀²/(2y).

At τ_E = √(2c/(wσ²)):
- J(τ_E) = 2√(cα) = O(√w).
- βτ_E³ = (w²σ⁴/3)(2c/(wσ²))^{3/2} = O(√w).
- So θ(τ_E) → 2y/s₀², and B_slack(w) → ln(1/ε_r)·s₀²/(2y).

Hence **B_slack(w) − B_min(w) → 0 as w → 0**.

At w = 0 exactly (outside CT22's hypotheses), θ(τ) = 2(y − c/τ)/s₀² is increasing in τ, so not checking at all maximizes survival. Judgment cannot raise survival, and the cap is met or missed regardless of design.

OBS at the published point (y = 1, c = 1/20, σ = 1, s₀² = 0.09, ε_r = 10⁻³): w = 1 reproduces THEORY's B_min = 0.486 and B_slack = 0.508. The band width is 2.1×10⁻², 5.9×10⁻³, 5.6×10⁻⁴ and 1.8×10⁻⁴ at w = 1, 0.1, 10⁻³ and 10⁻⁴, a slope of about ½ in log–log. The limit is 0.31085.

### 4.4 Correction to STEPBACK §11 (C12c HYP) and gate C13-5
- "The region where memory is non-zero is the union of a stake region and a survival region": **PIM for stake-free caps** (Theorem O(ii)). For CT22's cap it is **not right as stated**: the survival region is the thin band (B_min(w), B_slack(w)), which exists only at w > 0 and shrinks to nothing as w → 0.
- "At zero stake, judgment is absent iff the ruin cap is slack": **PIM for stake-free caps**, with "slack" meaning slack at the blind design (Theorem O(v)). This is exactly CT22's B_slack definition evaluated at 𝒟_E, because for w ≤ w₁, 𝒟_E is the blind design. That answers C13-5's "iff" in this class. For CT22's cap at w → 0, judgment is absent for every B (in the limit).
- "A world with a binding ruin cap needs memory at zero stake": **false for stake-carrying caps; true for stake-free caps.**
- So the C12 wording "physics is the zero-stake floor of the cost of judgment" (HYP) needs "and no binding stake-free cap" rather than "and slack ruin". A stake-free cap is a required accuracy, which is Ace's point: it is a stake.

## 5. Task 3: the single cleanest theorem candidate, and Lean cost

**Candidate (Theorem O, §3.1):** for a convex, nonincreasing error curve, a linear price and a stake-free accuracy cap,
- memory is on iff (stake > first-bit threshold) or (cap tighter than the blind error);
- the optimal memory is max(x_w, x_D);
- the cap acts as the stake max(w, w\*(D)), with w\* nonincreasing in D and meeting w₁ at the corner.

- **Paper:** done above (half a page). It is an instance of Everett/KKT, so it is **not a new theorem in mathematics**. It is a new PIM row for GTAO, if a hostile review passes it.
- **Lean:** cheap.
  - *Finite version:* x ∈ {0, …, n}, f a discrete-convex nonincreasing sequence, statements (i), (ii) and (v). Pure order arguments, about 1–2 h.
  - *1-D real version:* Mathlib's `ConvexOn`, with one-sided derivatives avoided by stating (iii) with difference quotients. About 3–4 h.
  - Recommendation: the finite version first, as a small addition to a Lean round (bedrock, low risk). The real version only if the review wants (iii) formal.
- **Not in Lean:** the class-A Gaussian closed forms (routine calculus; the existing check scripts cover them).

## 6. Side lead: what plays the stake for bare physics? (HYP reading of KNOWN results)

Still 2020 (PRL 124:050601, 10.1103/PhysRevLett.124.050601; abstract and Eq. (8) read this session on arXiv 1705.00612v3):
- For a partially observable information engine that may use two temperatures, −Q ≥ k(T·I_mem − T′·I_rel).
- Minimizing that bound "leads to a compression method that maximally retains relevant, predictive, information". That is the IB with tradeoff **β = T′/T**.

Paper step (PIM about Still's **bound**, not about any engine):
- Take a scalar Gaussian X, relevant variable Y with correlation ρ, and a Gaussian channel M = X + N with s = 1/(1 + n).
- Then I_mem = ½ ln(1/(1 − s)) and I_rel = −½ ln(1 − ρ²s). The derivative of I_mem − β·I_rel at s = 0 is ½(1 − βρ²).
- So **a non-trivial memory lowers the bound iff T′/T > 1/ρ²**. OBS: inf_s I_mem/I_rel = 1/ρ² to 6 digits, `c12c_check.out` §5.
- For CT4's AR(1) at lead 1, ρ = a, so T′/T > 1/a².
- At T′ = T, β = 1 ≤ 1/ρ², and memory never shows a net gain: a zero-stake floor at a single temperature.
- The general threshold is the IB learnability threshold (Wu, Fischer, Chuang & Tegmark 2019, 10.3390/e21100924). The Gaussian IB critical β = 1/(1 − λ) is Chechik, Globerson, Tishby & Weiss 2005 (JMLR 6:165; no DOI, not Crossref-checked; the scalar case is re-derived above).

**Reading (HYP):** in this one KNOWN bound, the stake on a memory is a temperature ratio, a free-energy gradient, and onset needs it above a world-set threshold. That fits Ace's caution and his "life is where the stake gets large and self-maintaining". It does **not** show what sets the stake for bare physics in general. It does not derive anything physical, and CORE:29 ("temperature does not set w") stays true for the single-bath heat floor. It is an open question with one candidate answer from prior art.

## 7. Task 4: falsifiable prediction and prereg sketch (DRAFT; not locked, not run)

Most of §3 is fixed by theorem, so a run testing it would score V = 2. The one open, data-dependent question is whether Ace's sentence holds on **our own physics rounds**, where the menu is discrete.

**Draft C12c-G (duality gap in the record-cost chain).**
- **Question.** In the record-cost chain's world menu (RECORD_COST_CHAIN §4 worlds), does some world win under a stake-free accuracy cap D (minimum spend subject to error ≤ D) while winning under **no** stake q?
- **Prediction (HYP, prior 0.6):** **no gap**. Every world selected by some cap is selected by some q. That would make the accuracy-as-stake reading exact there.
- **Miss:** a world with a cap-only window. Then "a required accuracy is a stake in disguise" is false for that menu, and the sentence needs "on the convex hull" (logged as an open miss with the window).
- **Method sketch.** Use each world's spend–error frontier C_W(D) from the chain's own scripts at its locked settings (no new physics). Compute the lower convex hull of ∪_W C_W, and list worlds that are pointwise-minimal on some D-interval but never on the hull.
- **Gates:** frontier computed from committed code only; D grid and worlds fixed before looking; mixtures **not** allowed, stated up front (with mixtures the gap is empty by Lemma A); a tie tolerance fixed in advance.
- **Does not mean:** anything about real physics. A hit or a miss is about the chain's toy cost.
- **Score:** p_gap 0.4, V 3 (names where the sentence needs its condition); p_no-gap 0.6, V 2. EIV ≈ 2.4 over ≈ 2 h → ≈ 1.2 per hour.

**Secondary, in-model, not informative (listed so no one runs it as a test):** class B's ε_B(w\*) = −4 is dimensional. The class-A formulas are fixed by Theorem O.

## 8. Task 6: C12c rescored on the §13 scale

Scale (STEPBACK §5, §9 C9-6): a hit fixed by a known theorem scores V = 2; V_miss = 2 if it locates nothing, 3 if it names an input.

| item | p_hit | V_hit | p_miss | V_miss | EIV | cost | per hour | note |
|---|---|---|---|---|---|---|---|---|
| C12c, whole route as first scored (§11: 0.95) | — | — | — | — | — | — | — | paper work now done (≈ 1.5 h sunk) |
| C12c residual: hostile review of this note | 0.85 | 2 | 0.12 | 3 (a found error names the cap type or class that breaks) | 2.06 | 1 h | **≈ 2.1** | cheap; required before anything counts |
| C12c whole route, sunk included | 0.85 | 2 | 0.12 | 3 | 2.06 | 2.5 h | ≈ 0.82 | below C4 1.00; above C1 0.83 within noise |
| C12c-L: Lean finite Theorem O | 0.9 | 2 | 0.08 | 1 | 1.88 | 2 h | 0.94 (≈ 2.8 with Chad's Lean ×3) | small, bedrock |
| C12c-G: duality-gap check (§7) | 0.4 | 3 | 0.6 | 2 | 2.4 | 2 h | ≈ 1.2 | the only data-dependent piece |
| C12d: Still-temperature-ratio note (§6) | 0.6 | 2 | 0.3 | 2 | 1.8 | 1.5 h | ≈ 1.2 | V capped at 2: known math |

C12b (order of thresholds w₁ < w₂, repair vs prediction) is untouched by this note and stays at 0.90. Theorem O gives it a frame: if repair is a second resource with its own convex curve, then its onset is also a union/max, and w₂ is the T63 version of w₁.

## 9. Task 5: prior art (DOIs verified on Crossref this session; `crossref_c12c.txt`)

- **Everett 1963**, *Generalized Lagrange multiplier method for solving problems of optimum allocation of resources*, Operations Research 11:399–417, 10.1287/opre.11.3.399. **Lemma A is this.**
- **Blahut 1972**, *Computation of channel capacity and rate-distortion functions*, IEEE Trans. IT 18:460–473, 10.1109/TIT.1972.1054855. Parametrizes R(D) by the slope s, where the distortion constraint's multiplier is the slope. This is the rate–distortion form of §2.
- **Sims 2003**, *Implications of rational inattention*, J. Monetary Econ. 50:665–690, 10.1016/S0304-3932(03)00029-1. Uses a **capacity constraint**. The price-per-bit form (Matějka & McKay 2015, AER 105:272–298, 10.1257/aer.20130047) is its Lagrangian dual. Same duality, with information and error swapped.
- **Still, Sivak, Bell & Crooks 2012**, *Thermodynamics of prediction*, PRL 109:120604, 10.1103/PhysRevLett.109.120604. Dissipation ≥ kT·(I_mem − I_pred), already credited in the repo (IP2, LITMAP). It has no stake and no cap, so no onset statement.
- **Still 2014**, *Information bottleneck approach to predictive inference*, Entropy 16:968–989, 10.3390/e16020968. The predictive IB used by CT4.
- **Still 2020**, *Thermodynamic cost and benefit of memory*, PRL 124:050601, 10.1103/PhysRevLett.124.050601. Two-temperature bound giving IB with β = T′/T (§6).
- **Creutzig, Globerson & Tishby 2009**, *Past-future information bottleneck in dynamical systems*, PRE 79:041925, 10.1103/PhysRevE.79.041925. Predictive IB for dynamical systems, including Gaussian cases.
- **Tishby & Polani 2010/2011**, *Information theory of decisions and actions*, in Perception-Action Cycle, pp. 601–636, 10.1007/978-1-4419-1452-1_19 (Crossref lists 2010). Already credited in CT4.
- **Wu, Fischer, Chuang & Tegmark 2019**, *Learnability for the information bottleneck*, Entropy 21:924, 10.3390/e21100924. The trivial-representation threshold β₀, which is CT4's first-bit threshold in IB form.
- **Charnes & Cooper 1959**, *Chance-constrained programming*, Management Science 6:73–79, 10.1287/mnsc.6.1.73. The chance cap → deterministic cap step in §3.2.
- **Black & Cox 1976**, J. Finance 31:351–367, 10.1111/j.1540-6261.1976.tb01891.x. Already the source for Lemma B8.
- Not Crossref-checked and not cited as verified: Chechik et al. 2005 (JMLR, no DOI); the inventory-theory notion of an "imputed shortage cost" of a service-level constraint, which I believe is standard but did not verify this session.

**Plain statement:** the core is already known.
- "An accuracy constraint is a price" is Everett/KKT/rate–distortion duality.
- "Memory pays past a threshold" is CT4, which is the IB learnability threshold.
- "Onset is a union, and the stake is a max" follows in one line.

What is not in that prior art, as far as I found, is the GTAO-specific point:
- the zero-stake floor depends on the **type** of ruin cap;
- stake-free caps force memory at w = 0, while CT22's reserve cap cannot;
- the two cap types have opposite monotonicity in w.

That point is modest and must pass review.

## 10. Recommended next step
1. A fresh **hostile review** of this note (≈ 1 h, ≈ 2.1 per hour). Focus on: Theorem O(iii) with subgradients; the §4.3 limit argument; the class-A Gaussian-memory scope; whether §6's reading overreaches.
2. If it passes, a **finite Theorem O in Lean** as a small add-on to the next Lean round (≈ 0.9 per hour, or ≈ 2.8 per hour with Chad's ×3).
3. Park C12c-G (≈ 1.2 per hour) and C12d (≈ 1.2 per hour) in the queue. C12c-G is the only piece whose outcome is not fixed by a theorem.
4. Carry into Ace's Friday wording note, as a suggestion only, without editing anything: "a required accuracy acts as a stake (on the convex hull of the designs); a reserve-type ruin cap does not force memory at zero stake".

---

## 11. Corrections after HOSTILE_REVIEW_C12C.md (appended 26 Nov 2026, after 08:11 ET; the text above stands as written; where it conflicts with this section, this section governs)

Review: `rnd/review_c12c/HOSTILE_REVIEW_C12C.md` (reviewer independent of the author), checks `review_c12c_check.py` → `.out`. Outcome **PASS-WITH-FIXES**: one high, four mediums, eight lows. Every fix is applied below. No earlier line was edited.

### 11.1 H1: Lemma A(b) is false as stated

**The counterexample, R1, is accepted.**
- Menu (E, S): A = (0, 1) and B = (1, 0). Cap D = 0.5, stake w < 1.
- The capped optimum is A. A is a lower-hull vertex and E\* = 0 < D, so complementary slackness forces μ = 0.
- But at stake w with no cap, B wins. No multiplier with complementary slackness exists. Stakes w + μ ≥ 1 select A, but they break complementary slackness.
- The proof step "E\* minimizes h(E) + wE over E ≤ D" fails because the envelope on (E\*, D] uses mixtures with infeasible points.

**Restated Lemma A** (§2's (b) is withdrawn; (a) stands):
- **(a) KNOWN (Everett 1963, Theorem 1).** If d° minimizes S + λE over 𝒟 for some λ ≥ 0, then d° minimizes S over {E ≤ E(d°)}.
- **(b′) KNOWN (Lagrangian strong duality).** Assume the attained set's free-disposal hull is convex, meaning mixtures are allowed or the menu is convex. Assume also strict feasibility, inf E < D. Then for any capped optimum d\* there is μ ≥ 0 with μ(E(d\*) − D) = 0 such that d\* minimizes S + (w + μ)E with no cap.
- **(b″) KNOWN (sufficient condition without convexity).** Let v(D′) = min{S + wE : E ≤ D′} be the capped value function. If v agrees with its lower convex envelope at D (no duality gap at D), the same μ exists.
- **(b‴)** On a non-convex menu, the hull-vertex condition alone is enough only when the cap binds (E\* = D).

**Everett attribution, re-checked by me.** I could not read the paper's full text this session (it's paywalled, and I didn't try any non-public route).
- Crossref confirms the bibliographic data: Operations Research 11(3):399–417, 10.1287/opre.11.3.399.
- A secondary source read this session (Säljö 2004, Chalmers MSc thesis, §2 on Lagrangian relaxation) and Wikipedia's summary ("relates the Lagrangian bidual to the primal problem") both describe Everett's theorem as the **sufficiency** direction: a Lagrangian maximizer is optimal for the constraint level it attains.
- My recollection is that Everett discusses resource levels no multiplier reaches ("gaps"). I did not verify that this session, so it is not cited.

**Citation as reworded:** Lemma A(a) is "Everett 1963 (Theorem 1)". Lemma A(b′)/(b″) is "standard Lagrangian strong duality", with no Everett attribution.

**Headline wording (§0.1), restated:** "a required accuracy acts as a stake when the menu is convex (mixtures allowed) or there is no duality gap at the required accuracy". §0.1's "on the convex hull of the menu" is withdrawn as too loose.

**Consequence for C12c-G (§7).** C12c-G disallows mixtures, so it is the non-convex case, where (b) gives no help. Its question is also a different one from (b).
- C12c-G asks whether **some** stake selects each cap-selected world. By V6, a cap-selected design is stake-selectable iff it is a vertex of the lower convex hull of the attained points. A Pareto point off the hull is the gap.
- (b) asks for a multiplier with complementary slackness **at a given w**. R1 shows that this can fail even for a hull vertex: A is stake-selectable at w ≥ 1, just not at the given w.
- So C12c-G must define "gap" as "Pareto-optimal under some cap and a vertex of no lower hull" (the V6 test). It must not use "no KKT multiplier", and it must not use Lemma A(b) as its theory. See §11.5 for the lockability list.

Theorem O is one-dimensional and convex, so it is unaffected by H1.

### 11.2 M1: class-A closed forms are upper bounds; the onset corner holds over all memories

**Accepted (R5).** At a = 0.8, Var = 1, ε = 10⁻³, B = 0.99·B₀:
- Gaussian I_req = 0.0228 bits.
- A deterministic three-state tail-flag memory meets the same chance cap with H(M) = I(M; X_t) = 0.00479 bits. It records sign(X_t) only when |X_t| > 3.58 and predicts ±4.01.
- Monte Carlo with 2×10⁷ draws gives ruin 9.93×10⁻⁴, against 1.12×10⁻³ blind.

So:
- I_req(B), w\*(B), B_slack(w) and I\* = max(I_w, I_req) from §3.2 are **upper bounds** on the cheapest design over all memories. They are exact only within linear-Gaussian memories.
- The reason: a chance cap prices a tail-indicator loss, while the stake prices squared error. Theorem O needs the cap and the stake on the same f, and over all memories they aren't.

**Upgrade (PIM over all memories): the L-shaped onset holds for every memory.** In CT4's Gaussian AR(1), lead 1, κ per bit, stake w on squared error, and per-step cap P(|e| ≥ B) ≤ ε: **a memory with I(M; past) > 0 is held ⇔ w > w₁ = κ/(2 ln 2·a²Var) or B < B₀ = z_ε√Var.**

*Proof.*
- **(⇐, cap part).** A zero-information memory gives a prediction ĉ independent of X_{t+1} ~ N(0, Var). The distribution N(−ĉ, Var) is a shift of a symmetric unimodal distribution (condition on ĉ if it is random), so P(|X_{t+1} − ĉ| ≥ B) ≥ P(|X_{t+1}| ≥ B) = 2Φ̄(B/√Var) (Anderson's inequality, scalar case). That exceeds ε iff B < B₀. So below B₀ every feasible design holds information.
- **(⇐, stake part).** Let w > w₁ and B ≥ B₀.
  - By CT4, the Gaussian design at I_w > 0 costs strictly less than blind.
  - Its error is N(0, D(I_w)) with D(I_w) < Var, so its ruin is 2Φ̄(B/√D(I_w)) < 2Φ̄(B/√Var) ≤ ε. It is feasible.
  - The blind design is therefore not optimal, and any optimum holds information.
- **(⇒).** Let w ≤ w₁ and B ≥ B₀.
  - The blind design (ĉ = 0) meets the cap.
  - CT4's convex lower bound L(I) = w·D(IB(I)) + κI holds over all memories, including the tail flag. Its minimizer is I = 0 when w ≤ w₁, and blind attains L(0) = w·Var.
  - So blind is optimal with no cap, hence optimal with the cap.
  - At w = w₁ exactly, blind is among the optima, and the least-information optimum is blind.
- ∎

**Open miss logged:** *the minimum bits under a chance cap over all memories (class A).* The true minimal-information design for P(|e| ≥ B) ≤ ε is open, with 0.00479 ≤ (the best known, the tail flag) and the Gaussian 0.0228 as an upper bound at B = 0.99·B₀. It names the input: the cap's loss (a tail indicator) differs from the stake's loss (squared error). A rate–distortion problem with a probability-of-excess distortion is the natural frame. Prior art there was not searched this session.

### 11.3 M2: prior art inside the repo, credited

- **`reviews/audit_2026-11-19/AUDIT.md:102–105` (Candidate 2)**, read this session. It already states that "the stakes w are the reciprocal of the shadow price of that budget". It checks λ·w = 1.000000 for a read-cost budget, notes "the survival price μ_s is already a multiplier of this kind", and gives the caveat "duality can fail at fixed costs". That is Lemma A's budget-dual form inside the repo, a week before this note. §2's Lemma A is a restatement for an error cap, not a new step.
- **The stake-free vs stake-carrying split** is the repo's existing scope condition:
  - CT33: "the design set must not depend on w" (THEORY:495);
  - V3: "stake-independent menu" (CLAIM_MAP:713);
  - CT24: "whose feasible set does not depend on the prices" (THEORY:101).
- §3.4's row "stake-free vs stake-carrying caps as the split for the zero-stake floor: new framing (HYP until reviewed)" is corrected to: **"the CT33/V3/CT24 scope condition applied to onset and the zero-stake floor; the addition is the application plus the two class computations"**.
- §0.4's and §9's "what is ours" are narrowed the same way.
- **Still 2020** (arXiv 1705.00612v3, text read this session in the reviewer's copy):
  - Still says the temperature ratio α "can also be interpreted as a Lagrange multiplier that controls the" tradeoff (p. 4).
  - Her Eq. (7), −Q ≥ kT·I_irrel ≥ 0 at T′ = T, is already the single-temperature floor.
  - Both are credited to her. See §11.8.

### 11.4 M3: CT22 at w = 0 is inapplicable, not false; the Lundberg certificate is separated from the chance cap

- **Reworded.** §0.3, §4.4 and §8 said "false for CT22's cap" and "cannot force memory at w = 0". These now read: **"inapplicable at w = 0: a stake-carrying cap sees the loss only through w·loss, so at w = 0 it is either slack or infeasible and never binding; in the limit w → 0 the binding band collapses."** The STEPBACK §11 clause "a world with a binding ruin cap needs memory at zero stake" is **vacuous** for CT22-type caps, not shown false. It is PIM-true for stake-free caps (Theorem O(v)).
- **Uniform version (added).** For every w > 0, CT22's band forces more checking than the stake optimum. The uniform statement is that even the survival-optimal design checks at a vanishing rate:
  - θ_w → θ₀ = 2(y − c/τ)/s₀² uniformly on compacts as w → 0, and θ₀ is increasing, so τ_S(w) → ∞. **PIM (limit).**
  - τ_S·√w → 0.2197, flat from w = 10⁻⁶ to 10⁻³ (reviewer R6). **OBS.** The forced check rate is O(√w).
- **Separation.** CT22's B_min and B_slack come from a **Lundberg certificate** on a reserve (lifetime ruin, a sufficient bound). Class A's B₀ comes from a **per-step chance cap** on the tracking error, and class B's from CT25's per-window cap. These are different constraints (THEORY:186).
  - §4.4's sentence "This is exactly CT22's B_slack definition evaluated at 𝒟_E, because for w ≤ w₁, 𝒟_E is the blind design" is **withdrawn**. CT22's path has w₁ = 0 (checking is on at every w > 0, as in class B), and its B_slack is a Lundberg quantity.
  - **Gate C13-5 is answered by Theorem O(v) in the stake-free classes only** (class A; class B by direct calculation). Nothing is claimed for CT22.

### 11.5 M4: C12c-G is not lockable; what a lockable version needs (no lock written)

1. **Reading and drift setting named.**
   - Under the locked **total** reading (RECORD_COST_CHAIN:64), the stake row is "—", with no q-flip at zero drift. The q-dependence exists only under the **per-record** reading.
   - The prereg must name one reading and one drift setting. If it is the total reading at zero drift, it must say in advance that "no gap" may be trivial (one winner at every q and D).
2. **Blinding.**
   - The chain publishes J at q = 4 and the crossover stakes (7.7 for pairs; 12.4–17.6 for single systems). With J_W(q) = S_W + q·E_W, many worlds' (S, E) points can be backed out of committed numbers, and the author has seen them.
   - The prereg must list what is already computable from committed numbers and either compute it openly as a non-test, or restrict the test to quantities not yet computed.
3. **At least 3 worlds.** The pairs comparison has two points (quantum, boxworld), and a two-point menu can never have a gap. Drop it and keep only menus with ≥ 3 worlds.
4. **Mixing rule, both levels.** State whether mixing is disallowed **across** worlds, **within** a world (time-sharing of designs), or both. Within-world time-sharing convexifies each C_W, and mixing across worlds removes the gap entirely (Lemma A(b′)).
5. **Frontier or point.** Show whether the chain's scripts give a spend–error frontier per world, or one (S, E) point per world at locked settings. If they give one point, the run is a short table read, not 2 h, and with point (2) it may be fully pre-computable, so not a test.
6. **Gap defined by V6**, as Pareto-optimal under some cap and on no lower hull (§11.1), not by KKT multipliers.
7. **A reasoned prior.** The 0.6 for "no gap" was not reasoned. With ~6 single-system worlds as points, an off-hull Pareto point is not unlikely a priori. With no argument either way, the prior is moved to **0.5**.

### 11.6 Lows

- **L1. Theorem O(iii), corrected statement.**
  - If **x_D > x_w′** (the cap excludes every unconstrained minimizer; this is automatic if f is strictly convex and x_D > x_w), then μ := κ/|f′(x_D⁻)| − w > 0 is a KKT multiplier.
  - The set of stakes at which x_D is an unconstrained minimizer is the interval [κ/|f′(x_D⁻)|, κ/|f′(x_D⁺)|] (upper end +∞ if f′(x_D⁺) = 0).
  - **w\*(D) := κ/|f′(x_D⁻)| is the least supporting stake.** It is "the" effective stake only where f is differentiable at x_D.
  - If x_w ≤ x_D ≤ x_w′, then μ = 0 and w_eff = w. The formula w_eff = max(w, w\*(D)) still holds, since w\* ≤ w there.
  - R3's flat-segment example (f slope −1 on [0.5, 1.5], w = κ = 1, x_D = 1) gives μ = 0, as corrected.
  - §3.1(iii)'s "If x_D > x_w" is superseded.
- **L2. f′(x_D⁻) < 0 uses inf f < D.** If f′(x_D⁻) = 0 with x_D > 0, then convexity and monotonicity force f ≡ f(x_D) = D on [x_D, ∞), so inf f = D, contradicting the hypothesis. The proof now cites inf f < D at this step.
- **L3. Class B lies outside Theorem O's hypotheses**, since f(x) = σ²/(2x) has f(0) = +∞. Class B is handled **by direct calculation** (§3.3), confirmed by the reviewer's root-finding in 3 cases (R7). §3.3's "this is Theorem O" is withdrawn. An extension of Theorem O to f : (0, ∞) → [0, ∞) with f(0⁺) = ∞ is plausible but not written.
- **L4. Class B scaling.** w\*(B) = 2c·z_ε⁴σ²/B⁴ is stated **for H = ½** (the reset path with inputs c, σ, B, ε only). With CT18-H (H ≠ ½), or an added scale such as y or s₀, the exponent is not −4. It is still not an informative prediction.
- **L5. CT22 B_slack(w) is increasing: upgraded to PIM on CT22's path.** θ(τ_E(w)) = 2(y − √(2cwσ²)) / (s₀² + (σ⁴/3)(2c/σ²)^{3/2}·√w). The numerator falls and the denominator rises in w, so B_slack(w) = ln(1/ε_r)/θ(τ_E(w)) is strictly increasing wherever m(τ_E) > 0.
  - At w = 1: θ = 1.367544/0.100541 = 13.6019, so B_slack = 0.50785, matching THEORY's 0.508.
  - The reviewer matched it to 6 digits at 13 stakes.
  - The band width ∝ √w stays **OBS** (log–log slope 0.5005).
- **L6. Record-cost chain (§1, §0).** "The selected world depends on it [q]" holds **under the per-record reading only**. Under the locked total reading there is no flip at zero drift.
- **L7. Still reading (§6).**
  - "Stake = T′/T" is an **analogy in form**, like "temperature = price of information". α multiplies a benefit (relevant information turned into work at T′), not a weight on loss.
  - The ratio is supplied by a second bath plus an engine design step (α = V/V′, adiabatic compression), so it is not bare physics.
  - The Gaussian computation is about the bound's objective, not an engine. Still's protocol uses discrete memory states.
  - **The single-temperature floor is Still's Eq. (7): KNOWN, not PIM.** The T′/T > 1/ρ² threshold is Still's efficiency condition I_rel/I_mem ≥ T/T′ applied to a scalar Gaussian (sup_s I_rel/I_mem = ρ²). It is an application of KNOWN results.
- **L8. Scores.**
  - The residual figure is 2.06 (§0 said ≈ 2.0, §10 said ≈ 2.1).
  - 0.82 is **below** C1's 0.83 (level with it), not above.
  - The C12c-G columns were swapped relative to §7's prediction.
  - Reviews are quality control, not evidence, so they are no longer scored as EIV items (STEPBACK §12 keeps bookkeeping out of the ranking).
  - Sunk-cost rates are retrospective only and do not drive the pick.
  - §8's table is superseded by §11.9.
- **L9.** All 12 DOIs were re-verified by the reviewer. Chechik et al. 2005 stays marked unverified.

### 11.7 Labels (set exactly as the review's table)

| piece | label |
|---|---|
| Lemma A(a) | KNOWN (Everett 1963) |
| Lemma A(b) | KNOWN (Lagrangian strong duality), **only** as restated in H1 |
| Theorem O (i), (ii), (iv), (v) | PIM (paper, reviewed here); KNOWN in substance |
| Theorem O (iii) | PIM after the L1 fix; w\* = the least supporting stake |
| Class A onset: L-shaped, corner (w₁, B₀) | **PIM over all memories** (upgrade, M1) |
| Class A I_req, w\*(B), B_slack(w), I\* = max(I_w, I_req) | PIM **within linear-Gaussian memories only**; OBS: not optimal over all memories (tail-flag example, R5) |
| Class B w\*(B) = 2cz_ε⁴σ²/B⁴ | PIM (H = ½); exponent fixed by units; not a prediction |
| CT22 band collapse as w → 0 | PIM (limit); "vacuous at w = 0", not "false" (M3) |
| CT22 B_slack(w) increasing | PIM on CT22's path (closed form, L5) |
| Width ∝ √w; τ_S√w → 0.22 | OBS |
| Stake-free vs stake-carrying split | CT33/V3 scope condition applied to onset; credit AUDIT 2026-11-19 Candidate 2 (M2) |
| §6 Still reading | KNOWN bound and threshold; "stake = T′/T" is HYP, an **analogy in form** |
| C12c-G | DRAFT; not lockable until M4 is fixed |
| Overall C12c HYP (STEPBACK §11) | Corrected: PIM for stake-free caps; inapplicable/vacuous for CT22-type caps at w = 0 |

Open misses: (1) minimum bits under a chance cap over all memories (§11.2); (2) Lemma A(b)'s hull-point condition is insufficient, witness the two-point menu at D = 0.5 (§11.1).

### 11.8 Plain restatement of what this note adds, after the review

- One reviewed 1-D theorem, Theorem O. It is KNOWN in substance and a candidate for a small Lean lemma.
- The CT33/V3/CT24 scope condition applied to the zero-stake floor: stake-free caps can force memory at w = 0; CT22-type caps are inapplicable there.
- An all-memories onset corner in CT4's class.
- One open miss with a named input (tail loss ≠ squared loss).
- The Still link is an analogy in form, and its zero-stake floor is Still's own Eq. (7).

Nothing here derives any physics.

### 11.9 Rescore (§13 scale; reviews and sunk cost not scored)

Scale: V = 2 for a hit fixed by a known theorem; V_miss = 2 if it locates nothing, 3 if it names an input. Only forward items are scored.

| item | p_hit | V_hit | p_miss | V_miss | EIV | cost | per hour | note |
|---|---|---|---|---|---|---|---|---|
| C12c-L: finite Theorem O in Lean (spec: `C12C_LEAN_SPEC.md`) | 0.90 | 2 | 0.08 | 2 (a failed proof names a hypothesis slip) | 1.96 | 2.5 h (discrete kinks add ~0.5 h to the earlier 2 h) | **0.78** (≈ 2.35 with Chad's Lean ×3) | KNOWN math, so V capped at 2 |
| C12c-G′: lockable redesign per §11.5, run on per-world frontiers | 0.45 (gap found) | 3 (names where accuracy ≠ stake in our own rounds) | 0.50 (no gap) | 2 | 2.35 | ≈ 3 h (new frontier computation + lock + gate read) | **0.78** | if each world is one committed point, it is pre-computable and **not a test**: bookkeeping, unscored |
| C12d: Still credit / analogy note | — | — | — | — | — | ≈ 0.5 h | not ranked | bookkeeping (credit Eq. 7 and the multiplier remark in the open-question list) |
| class-A open miss: min bits under a chance cap | 0.3 (closed form or tight bound found) | 3 | 0.6 | 2 | 2.1 | ≈ 4 h (literature + math) | 0.53 | low; listed for completeness |

**C12c route, new rank.** The best forward item is **0.78 per hour** (C12c-L and C12c-G′ tie). That is down from C12c's 0.95. On the corrected new-route list:

**C4 1.00 · C12b 0.90 · SR-b ≈ 0.87 · C1 0.83 · C12c-L 0.78 · C12c-G′ 0.78 · C3v2 P5² cut ≈ 0.78 · C11 0.72 (lemma) · C6 0.70 · class-A open miss 0.53.**

With Chad's Lean stake ×3, C12c-L (≈ 2.35) scores above C9 (≈ 1.2). That ordering is an artefact of EIV per hour favouring cheap, near-certain items (STEPBACK §5 point 4, non-concave value). C12c-L is a low-value lemma, and C9 carries more value per success, so I would treat C12c-L as a **cheap add-on inside the next Lean round**, not a replacement for C9.
