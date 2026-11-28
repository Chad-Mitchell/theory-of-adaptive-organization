# FREEZE_PROCESS: is freezing a continuous limit of holding under the cost equation?

Saturday 21 November 2026, about 10:00 AM to 11:00 AM ET (America/New_York). Written by a Grok Bot executor for Chad Mitchell. Branch `freeze-process-2026-11-21`. Derivation file only: it does **not** edit `CORE.md`, `THEORY.md`, the claim map, or the hypothesis sentence. Independent review is in `records/reviews/freeze_2026-11-21/REVIEW.md` (READY-WITH-FIXES); S1–S3 are applied on this branch. Nothing was posted or sent.

**Question (Chad, 21 Nov).** Protons and crystals were not always here. Frozen states may be held states that froze as their world cooled or slowed. Is freezing a *process* that the same cost equation describes over time, rather than only a static corner?

**Sources read first (from the files).**
- `theory/GENERAL_THEOREM.md` §3 (G1–G4; G2 hold iff λc < Φ; G3 rise-then-fall).
- `theory/axioms/THEOREMS.md` Theorem 8, which is `THEORY.md` CT11 (freeze, hold or look up).
- `theory/SCALE_ENDS.md` §0 and §2 (E1–E4, the class table, black holes as the extreme of the frozen class).
- `THEORY.md` §3's freeze-or-hold row and CT11.
- `theory/MASTER_EQUATION.md` (j) (dynamics; Dixit hysteresis; redesign record length).
- C6/H9 as `SCALE_ENDS.md` quotes them. The longform `HYPOTHESES.md` is off-repo and was not reread.
- A grep of the repo for Kibble, Zurek, freeze-out, Dodson, closure temperature, Néel, blocking, relic, Dollo, annealing and cooling schedule found **none** of these. Hysteresis appears only as the Dixit line in MASTER_EQUATION (j)3 and the widenet scan. Relaxed selection appears only as a litmap pointer (BIO_PRIORART).

**Labels.**
- **PROVED (in-model):** proved here inside the stated model and checked by code.
- **NUMERICAL:** shown only by computation.
- **ANALOGY:** a shared mathematical form with physics, not a derivation of physics.
- **KNOWN:** prior art, with the citation checked.
- **OPEN:** not done.

None of the results is claimed as new. Each is elementary. Labels that originally read "UNCONFIRMED novelty" were downgraded in review (S3) to KNOWN / novelty 0 or 0–1; see §8.

**Checks.** `theory/freeze_process_checks/freeze_process.py`, with its output saved as `freeze_process.out` (numpy 2.5.5, scipy 1.18.1; about 2 s at nice 19). All checks pass. One first-run prediction failed and is kept as data (§6.4).

---

## 0. Bottom line, in plain words

1. **Yes: in the cost equation, frozen is the slow-world limit of held.** As drift q falls, the cost-optimal refresh effort falls smoothly, and the minimizer slides continuously into the frozen corner. There, the system reads once at formation and then persists blind. No jump occurs at the freeze edge. The cost J\* is continuous with a continuous slope; only its curvature jumps. This is in contrast to the opposite (fast) edge, where Theorem 8 already has a cliff to lookup. **PROVED (in-model).**
2. **G2's threshold is not the freeze edge.** G2's λ_c = Φ/c is the *high*-drift edge, where tracking stops paying and the system goes blind because the world is too fast. At the low-drift end, G3 already gives effort → 0 as √λ, smoothly. So "does upkeep jump at the G2 threshold as the world cools" has a clean answer: cooling never crosses G2. It approaches the freeze corner. **PROVED (in-model)**, re-checked.
3. **Freezing becomes discontinuous only under specific conditions:**
   - **(a) A fixed cost h_m for the tracking machinery itself**, which only fully frozen designs avoid. The switch then becomes first order: upkeep jumps h_m → 0, and refresh effort jumps by exactly √(h_m/(cH)). **PROVED (in-model).**
   - **(b) A binding ruin cap**, which makes the frozen design infeasible above q_r = Q_ε/H. Melting is then forced there and J\* jumps. **PROVED (in-model).**

   With neither condition, the transition is continuous.
4. **Freezing as a process over time is the known freeze-out criterion.** In a world whose drift decays with an e-folding time τ_c, the exactly optimal read schedule tracks the static optimum, √(Wq/2c) reads per unit time, while reads are frequent. Tracking breaks down where the optimal read interval reaches the cooling time, at q_fo ≈ 2c/(Wτ_c²). That is Theorem 8's freeze edge with the lifetime replaced by the cooling time. After that point, the read count N saturates with only O(1) more reads (2–3 across tested horizons up to 20,000), governed by the exact Euler–Lagrange condition u(t_k) − u(t_{k−1}) = q(t_k)(t_{k+1} − t_k). **PROVED (in-model) for the Euler–Lagrange optimality and freeze-out form; NUMERICAL for the onset constant (0.46–0.70 × q_fo in the table, up to ~1.03 × q_fo at Hor = 5000) and O(1) post-onset count.**

   The criterion "update rate falls below the rate at which the world changes" is **KNOWN**. It is cosmological freeze-out (interaction rate Γ below the expansion rate H; Hayashi 1950; Lee & Weinberg 1977), Dodson's 1973 closure temperature in geochronology, and Zurek's adiabatic–impulse rule in Kibble–Zurek. **We reinvented that criterion; credit is theirs.** The GTAO-specific part is narrow: the update rate is the *cost-optimal* rate, so the freeze-out point and the relic error are set by the price ratio c/W and the cooling time.
5. **The design itself freezes out too, leaving a relic.** If selection or learning needs longer to re-tune a design as the world slows (τ_a ∝ q^{−ζ}), a cooling world leaves a permanent relic design. That relic spends more on upkeep than the current world warrants. A finite relic occurs iff ∫dt/τ_a < ∞: always under exponential cooling, and iff pζ > 1 under power-law cooling q ∝ t^{−p}. The relic effort scales as τ_c^{−1/(αζ)}. **PROVED (in-model), NUMERICAL to 4 digits.** This is structurally Kibble–Zurek-like (a power law in the quench time), but the freeze is at the q → 0 end, not at a critical point. That makes it the cosmological-freeze-out type. **ANALOGY.**
6. **Hysteresis.** Once frozen, does a system re-melt at the same q?
   - **The static equation has no hysteresis**, even in the first-order case: the optimum is single-valued, so re-melting happens at the same q\*.
   - **Hysteresis needs one of three things:**
     - a switching cost (a build cost C_b or a dismantle cost C_d), which gives a Dixit band (KNOWN);
     - adaptation lag, which gives rate-dependent hysteresis that is non-monotone in the rate and vanishes quasi-statically (NUMERICAL);
     - or irreversible loss of the machinery, as in relaxed selection and Dollo-type loss (OPEN; prior art in biology).

   Physics' metastability of first-order transitions (nucleation barriers) has no counterpart in the static equation. Its analogue is the switching cost. **ANALOGY.**
7. **Temperature.** If the store's own decay is thermally activated (q_s = ν₀e^{−E_a/kT}), the freeze temperature is T_f = E_a / (k·ln(ν₀WH²/(2c))). This is the Néel/Brown blocking-temperature form, with the price ratio inside the logarithm. So prices barely matter: a 1000× change in c/W moves T_f by about 10%. **PROVED (in-model); the form is KNOWN.**

**What this means for Chad's intuition.** It is right, and physics already has the process half of it. Frozen states really were held states that froze out as their world's rates fell below its cooling rate. That is literally how the neutron-to-proton ratio and the light-element abundances were fixed in the first minutes. What the cost equation adds is not the freeze-out criterion. It adds the claim that, for *selected* systems, the same freeze-out happens to *chosen* update rates, with chosen relics. That claim is testable (§8). It does not extend GTAO's design predictions to protons: E1 still holds, so nothing selects a proton's response, and that part is ANALOGY only.

---

## 1. Setting

The setting is Theorem 8 / CT11 throughout: one item, squared-error loss at stake W, Brownian drift at rate q (α = 2), read cost c, read interval T ≤ H (H is the lifetime or horizon), and storage upkeep h.

- **Held:** J_H(q) = min_{T≤H} [c/T + WqT/2] + h.
- **Frozen corner:** T = H. The system reads once at formation (the "record of its formation", SCALE_ENDS table) and never refreshes. The excess refresh rate f − 1/H is 0.

Effort means f = 1/T. "Upkeep" splits into the three parts that the repo already keeps separate:
- (i) **refresh effort**, c·f;
- (ii) **storage upkeep h**, the cost of keeping the record; it is 0 for barrier-protected frozen stores (SCALE_ENDS E4);
- (iii) **machinery cost h_m**, the fixed cost of keeping the ability to refresh at all (new label here, §3). It is a special case of the master equation's A or κI_mem terms, paid only while the design can refresh.

---

## 2. The static freeze edge is continuous (PROVED, in-model)

**Claim.** With h_m = 0, the minimizer is T\*(q) = min(√(2c/(Wq)), H). It is continuous in q and reaches the frozen corner exactly at q_f = 2c/(WH²). At q_f:
- J\* is continuous and C¹: both one-sided slopes equal WH/2 (envelope theorem);
- d²J\*/dq² jumps from −√(2cW)/4·q_f^{−3/2} to 0;
- the excess effort f − 1/H vanishes linearly, as (1/H)(q − q_f)/(2q_f).

In Ehrenfest's language (ANALOGY), this is a second-order transition: a kink in the slope of the "free energy" J\* along the field q, with an order parameter that vanishes continuously.

**Proof.** The interior first-order condition gives T\* = √(2c/(Wq)), which meets H at q_f. min(·, H) of a continuous function is continuous. Substituting gives J\* = √(2cWq) for q ≥ q_f and c/H + WqH/2 for q ≤ q_f. Both equal 2c/H at q_f, and both derivatives equal WH/2 there. ∎

**Checks (S1).** On a grid of 200,001 points across q_f/50 … 50q_f:
- the J jump at q_f is 4×10⁻⁶ (grid spacing) and the effort jump is 0;
- the slopes are 10.000 and 9.990 at ±50 grid steps;
- the excess effort is 4.999×10⁻⁵ against a predicted 5×10⁻⁵.

**Contrast.** The lookup edge reproduces Theorem 8 item 5's cliff: effort is 1.25 just below q_c and 0 above it. **The two edges of the hold band differ in kind.** Slowing into frozen is smooth; speeding into lookup is a jump. Theorem 8 states the cliff, and the continuity of the freeze edge is implicit in its proof. Stating the asymmetry explicitly is the only addition here; **novelty 0** (elementary corollary of Theorem 8 and Cho & Garcia-Molina 2003).

**Infinite lifetime (G3).** With H = ∞, there is no corner. Effort goes to 0 as √(λ r′(0)/(2c)) (GENERAL_THEOREM G3). Re-checked in S4 for an OU world under quadratic loss: f\*/√λ is 0.9315, 0.9788, 0.9933, 0.9979 and 0.9993 at λ = 10⁻² … 10⁻⁶, against the limit 1. **The frozen state is the q → 0 limit of the held optimum.** G2's λ_c is the high-drift fade edge, not this one.

**Scope.** The analysis covers renewal reads, one item and α = 2. For general α the interior effort is ∝ q^{1/α} and the same argument applies. Retained history (filtering) can only lower holding cost (G2's remark), which leaves continuity intact but moves q_f. That case is not computed here.

---

## 3. When freezing is discontinuous

### 3.1 Fixed machinery cost h_m (PROVED, in-model)

Suppose keeping the ability to refresh costs h_m > 0 per unit time, and only a fully frozen design (no refresh after formation) avoids it.

- Frozen: J_F = c/H + WqH/2.
- Held: J_H = √(2cWq) + h_m.

Setting J_H = J_F gives (√(WH/2)·√q − √(c/H))² = h_m, so

**q\* = 2(√(c/H) + √h_m)² / (WH).**

This reduces to q_f at h_m = 0. At q\*, the held optimum has T\* < H.

**As q falls through q\*:**
- upkeep jumps from h_m to 0;
- refresh effort jumps down by exactly **√(h_m/(cH))**;
- J\* is continuous, but its slope jumps from WT\*/2 to WH/2.

In Ehrenfest's language this is first order, with a "latent" jump that vanishes as √h_m. h_m = 0 is the continuous endpoint. **Checks (S2):** closed form against root-finding at h_m = 10⁻⁴ … 10⁻¹, matching to 10⁻⁸. For example, at h_m = 10⁻², q\* = 0.017325 and the effort jump is 0.03162. The closed form is elementary algebra (**novelty 0**).

**Reading.** Whether a system freezes gradually or abruptly as its world slows is set by whether its tracking apparatus carries a fixed cost that freezing sheds. A cell that keeps a sensing pathway expressed, a firm that keeps a monitoring department, or a genome that keeps a repair system are the h_m > 0 cases. For those, the model predicts an abrupt shutdown at a drift above q_f, not a gradual fade. This prediction is OPEN (no test is designed).

### 3.2 Binding ruin cap (PROVED, in-model)

Take a per-window ruin constraint P ≤ ε for Brownian error, so that qT ≤ Q_ε (CT25's form). The frozen design is a single window of length H, so it is feasible only for q ≤ q_r = Q_ε/H.

- **With h_m = 0**, the capped minimizer T\* = min(√(2c/(Wq)), Q_ε/q, H) is still continuous (S3: largest local gap 2×10⁻⁶).
- **With h_m > 0 and q_r < q\***, the system freezes as soon as freezing becomes feasible, at q_r, and J\* jumps there. In S3 it jumps by 0.0100, which is exactly h_m because the capped held design sits at T = H there.

Heating from frozen, melting is forced at q_r. The constraint, not the cost, decides it.

---

## 4. Freezing as a process: an exactly optimal tracker in a cooling world

**Setting.** Drift decays as q(t) = q₀e^{−t/τ_c} over a horizon Hor ≫ τ_c, with one read at formation. A read resets the error. The error variance since the last read at t_k is u(t) − u(t_k), with u(t) = ∫₀ᵗ q. The cost is cN + W∫(error variance)dt. The schedule is solved exactly by dynamic programming on a nonuniform grid of 5,000–20,000 points (S5).

**Adiabatic regime (PROVED in-model for the limit; NUMERICAL here).** While the optimal interval is much shorter than τ_c, the optimal schedule follows the static rule T(t) = √(2c/(Wq(t))). The median relative deviation is below 0.1% in every run.

**Freeze-out (PROVED for the form; NUMERICAL for the constant).** The static rule stops being self-consistent once it asks for an interval longer than the time over which q itself changes. That happens at √(2c/(Wq)) = τ_c, that is,

**q_fo = 2c/(W τ_c²)**, which is Theorem 8's q_f with H → τ_c.

**Exact optimality condition (PROVED, in-model).** Differentiating cN + W Σ_{k=0}^N ∫_{t_k}^{t_{k+1}} (u(t) − u(t_k)) dt (with t₀ = 0, t_{N+1} = Hor) with respect to each read time t_k gives:
- interior reads (1 ≤ k ≤ N − 1): u(t_k) − u(t_{k−1}) = q(t_k)(t_{k+1} − t_k);
- last read: **u(t_N) − u(t_{N−1}) = q(t_N)(Hor − t_N)**.

| τ_c | c | Hor | onset q / q_fo | reads after onset | last read: q | τ_c·q(t_{N−1})/(Hor − t_N) |
|---|---|---|---|---|---|---|
| 10 | 0.005 | 300 | 0.68 | 2 | 1.02×10⁻⁶ | 1.07×10⁻⁶ |
| 20 | 0.005 | 600 | 0.69 | 2 | 2.91×10⁻⁷ | 3.07×10⁻⁷ |
| 40 | 0.005 | 1200 | 0.70 | 2 | 7.98×10⁻⁸ | 8.53×10⁻⁸ |
| 20 | 0.02 | 600 | 0.68 | 2 | 1.02×10⁻⁶ | 1.07×10⁻⁶ |
| 20 | 0.005 | 1500 | 0.46 | 2 | 3.78×10⁻⁸ | 3.86×10⁻⁸ |
| 20 | 0.005 | 5000 | 1.03 | 3 | 6.00×10⁻⁹ | 5.99×10⁻⁹ |

"Onset" is the first gap longer than τ_c. Across these runs the optimal schedule makes O(1) more reads after onset (2 in the first five runs, 3 at Hor = 5000 and 20,000) and then stops well before the horizon.

The onset sits at 0.46–0.70 × q_fo in the first five runs (and ~1.03 × q_fo at Hor = 5000 as the late reads adjust slightly). For t_N − t_{N−1} ≫ τ_c, u(t_N) − u(t_{N−1}) ≈ τ_c q(t_{N−1}), so the exact tail condition gives **q_last ≈ τ_c q(t_{N−1})/(Hor − t_N)** (matching every row to within ~7%, and exact u(t_N) − u(t_{N−1}) = q(t_N)(Hor − t_N) holds within 1.0%). As Hor → ∞, the total read count N **saturates** (N = 403 throughout Hor ∈ [1500, 10⁶] at τ_c = 20, c = 0.005): the remaining-horizon cost after t_N is W τ_c q_last (Hor − t_N) ≈ W τ_c² q(t_{N−1}), which is independent of Hor and stays below ~c once q(t_{N−1}) ≲ c/(W τ_c²) = q_fo/2, so no further read pays back c. Meanwhile, the single last read t_N shifts logarithmically rightward as τ_c ln(Hor/τ_c), causing q(t_{N−1}) and q_last·Hor to decrease slowly as 1/ln(Hor/τ_c) rather than scaling as a fixed multiple of c/(W τ_c Hor). The frozen record then carries the world as it was at the last read, with residual error ≈ q_last·τ_c.

**Is the passage continuous?** The read *rate* falls smoothly through the adiabatic regime and crosses over to zero over about one cooling time. It is a crossover, not a sharp transition. That is the same status that cosmological freeze-out has. The count of remaining reads is discrete, so "continuous" here means the rate has no jump before onset, followed by O(1) discrete reads.

**Prior art: this criterion is KNOWN, and the credit is theirs.**
- **Cosmological freeze-out.** A species stays in equilibrium while its reaction rate Γ exceeds the expansion rate H, and its abundance freezes when Γ < H. Hayashi (1950) computed the neutron–proton ratio this way. Lee & Weinberg (1977) used the same criterion for relic heavy neutrinos. It is textbook material (Kolb & Turner, *The Early Universe*, 1990; no DOI checked). Our f\*(q) ↔ Γ and |d ln q/dt| ↔ H.
- **Dodson's closure temperature (1973).** In a cooling mineral, isotopic exchange stops (the "clock closes") when the diffusion time exceeds the cooling time constant. Closure temperature has the same log form as §7.
- **Kibble–Zurek.** Zurek (1985) gives the adiabatic–impulse criterion: freeze when the relaxation time exceeds the time over which the control parameter changes. Kibble (1976) supplies the cosmological defect setting.

- **Optimal checking, nonstationary Wiener sampling, time-varying EOQ, and rational inattention (KNOWN in substance; targeted search done in review).** The square-root optimal checking density n(t) ∝ √h(t) for time-varying hazard is Keller (1974), extending Barlow, Hunter & Proschan (1963), with finite-horizon checking schedules in Viscolani (1991). Finite-horizon optimal sampling of Wiener/OU processes is Rabi, Moustakides & Baras (2012); signal-independent AoI–MSE equivalence and threshold sampling of Wiener sources are in Sun, Polyanskiy & Uysal (2020). Algebraically, cN + W Σ ∫_{t_k}^{t_{k+1}} (u(t) − u(t_k)) dt is the time-reversed deterministic continuous-time EOQ problem with exponentially declining demand (Hollier & Mak 1983). In economics, rational inattention / costly observation models give the same √(2c/(Wq)) interval (Reis 2006; Abel, Eberly & Panageas 2007, 2013; Alvarez, Lippi & Paciello 2011).

**What is GTAO-specific (novelty 0–1).** The mathematical mechanics are **KNOWN in substance**. The narrow GTAO framing is expressing the freeze-out point q_fo = 2c/(Wτ_c²) and residual error in GTAO's (c, W) parameters and connecting them directly to CT11's q_f = 2c/(WH²) via H ↔ τ_c.

---

## 5. The design freezes out too: relic designs (PROVED in-model; NUMERICAL)

§4 assumes the tracker *knows* q(t). A selected system has to *learn* its design. MASTER_EQUATION (j)1 already shows that estimating a rate a to relative precision δ needs a record of about 2/(aδ²). So the adaptation time diverges as the world slows: τ_a ∝ q^{−1}, which is ζ = 1. If instead selection does the re-tuning, the selective difference is ∝ J\* ∝ q^{1/α}, so τ_a ∝ q^{−1/α}, which is ζ = 1/α. That second form is a modelling assumption, not derived.

**Model.** x = ln f relaxes toward x\* = (1/α) ln q + const with rate 1/τ_a(q), τ_a = τ₁(q₁/q)^ζ:

dx/dt = −(x − x\*(t)) / τ_a(q(t)).

**Claim 5.1 (finite relic iff the total relaxation is finite).** The solution is x(t) = x(0)e^{−S(t)} + ∫₀ᵗ x\*(s)e^{−(S(t)−S(s))}dS(s), with S(t) = ∫₀ᵗ ds/τ_a. If S(∞) < ∞, x converges to a finite x_∞ while x\* → −∞. The design freezes with a relic effort that the current world does not justify. If S(∞) = ∞ and x\* changes slowly in S, the lag stays bounded and the design keeps tracking.
- **Exponential cooling:** S(∞) < ∞ always.
- **Power-law cooling q ∝ (1 + t)^{−p}:** S(∞) < ∞ iff pζ > 1. At the boundary pζ = 1, S(t) = ln(1 + t)/τ₁ → ∞ (no frozen relic), yet the lag x − x\* approaches a nonzero constant pτ₁/α (in S6 with τ₁ = 1, p/α = 0.5) rather than shrinking to zero.

**PROVED (in-model)**; this is linear ODE algebra. The convergence-of-∫Γdt form of the freeze-out condition is KNOWN from cosmology.

**Checks (S6).**
- Exponential cooling: x changes by 2.8×10⁻¹¹ between 40τ_c/ζ and 80τ_c/ζ.
- Power-law cooling, pζ = 0.5: the lag falls 0.053 → 0.0016 over t = 10² → 10⁵, so the design keeps tracking.
- Power-law cooling, pζ = 1.0: the lag converges to the nonzero constant 0.5000 (no frozen relic, constant lag).
- Power-law cooling, pζ = 2: x is stuck at −0.398 while x\* → −∞, so the design freezes.

**Claim 5.2 (relic scaling; exact asymptotic form).** Under exponential cooling q(t) = q₀e^{−t/τ_c}, writing S_∞ = τ_c/(ζτ₁) and u = e^{−ζt/τ_c}, exact integration gives x_∞ − x\*(0) = (1/(αζ)) ∫₀¹ S_∞ e^{−S_∞ u} ln u du = −[ln(τ_c/(ζτ₁)) + γ_E]/(αζ) + O(e^{−S_∞}), where γ_E ≈ 0.577216 is the Euler–Mascheroni constant. Thus **f_∞ = f\*(0)·(e^{−γ_E} ζτ₁/τ_c)^{1/(αζ)}** asymptotically, matching the τ_a(q_fo) = τ_c scale (q_fo ∝ τ_c^{−1/ζ}) up to an explicit O(1) constant: the slower the world cools, the smaller the relic.
- **Checks (S6):** fitted slopes −1.0000, −0.5000 and −0.2500 at ζ = 0.5, 1 and 2 (predicted −1, −½, −¼), over τ_c = 10–1000; exact Euler–Mascheroni formula matches numerical x_∞ at τ_c = 1000 to < 10⁻¹⁰.

**ANALOGY.**
- **Kibble–Zurek:** defect density ∝ τ_Q^{−dν/(1+zν)}, a power law in quench time with exponents from the critical point. Here the exponent comes from the world's roughness α and the learning exponent ζ.
- **Annealing (Kirkpatrick, Gelatt & Vecchi 1983):** cooling slowly lands nearer the optimum. Here, slower cooling leaves less relic upkeep.

This is a mathematical parallel only. There is no critical point here. The freeze happens where the rates go to zero, as in cosmological freeze-out.

**Prediction (OPEN, not preregistered).** This extends CLAIM_MAP N35 (lines moved to a buffered medium invest less in sensing). Lines whose medium is buffered *abruptly* should keep more relic sensing or regulation investment than lines buffered *gradually* to the same end state. The relic should scale as a power of the ramp time. Loss of unused regulation under relaxed selection is already known (Lahti et al. 2009; litmap's Mitchell et al. 2009). The power-law dependence on ramp time is the Kibble–Zurek / annealing analogue (**ANALOGY**). The GTAO-specific piece is the exponents (α, ζ) and the explicit γ_E prefactor in this ODE, and it is untested.

---

## 6. Hysteresis: once frozen, does it re-melt at the same q?

1. **Static equation, no switching cost: no hysteresis (PROVED, in-model).** J\*(q) is a function of the current q only, so the frozen-or-held decision is single-valued. This holds even in the first-order h_m case (S7: band ratio exactly 1). The difference from physics is real. First-order physical transitions show supercooling and superheating because of nucleation barriers. The static cost equation has no barrier term.
2. **Switching costs: a band (KNOWN; Dixit 1989, as MASTER_EQUATION (j)3 already credits).** Use a build cost C_b, a dismantle cost C_d and discount rate ρ, with q static after the shift.
   - Freeze when J_H − J_F > ρC_d; re-melt when J_F − J_H > ρC_b. This gives a band [q_down, q_up] around q\*.
   - S7, with h_m = 0.01 and ρ = 0.05: (C_b, C_d) = (0.1, 0.1) gives 0.01497 to 0.01925, a band ratio of 1.29. (0.5, 0.1) gives a band ratio of 1.69.
   - Under uncertainty, Dixit's option value widens the band further. That case is not recomputed here.
3. **Irreversible loss (OPEN; prior art in biology).** If freezing lets the machinery decay (relaxed selection; Lahti et al. 2009), re-melting needs the machinery to be rebuilt, perhaps by re-evolution. C_b can then be very large or effectively infinite (Dollo-type irreversibility). The model gives strong hysteresis, but the size of C_b is not derived.
4. **Adaptation lag: rate-dependent hysteresis (NUMERICAL).** Cool q from 1 to 10⁻³ and reheat at the same rate 1/τ_c, with ζ = 1. The loop area in (ln q, ln f) at τ_c = 0.3, 3, 10, 30, 100, 300, 10³ and 10⁴ is 0.50, 1.93, 2.10, 1.93, 1.53, 1.06, 0.57 and 0.09.
   - **First-run prediction FAILED and is kept as data:** I predicted the area would shrink monotonically as cooling slows. It does not. It is small when cooling far outpaces adaptation (the design never moves), largest at intermediate rates, and → 0 only quasi-statically.
   - This is the standard dynamic-hysteresis dispersion shape (ANALOGY; Jung, Gray, Roy & Mandel 1990; Chakrabarti & Acharyya 1999: loop area peaks at intermediate drive rate and decays at fast rates).
   - Under cooling all the way to q → 0, the relic of §5 is permanent, with effective scale q_eff = q_fo e^{−γ_E/ζ} < q_fo (where f\*(q_eff) = f_∞). On reheating at e-folding time τ_h, adaptation resumes near τ_a(q) ~ τ_h, i.e. q_melt ~ τ_h^{−1/ζ}. That exceeds q_fo only when reheating is faster than cooling (τ_h < τ_c), and exceeds q_eff only when τ_h ≲ τ_c e^{γ_E}; slower heating unfreezes below q_eff and briefly lowers f toward f\*(q) before climbing back.

---

## 7. Temperature: freezing a store whose own decay is thermal (PROVED in-model; form KNOWN)

Suppose the error the store must fight is its own thermally activated decay, q_s(T) = ν₀e^{−E_a/kT} (Arrhenius/Kramers 1940; SCALE_ENDS E4's barrier case), against a fixed required horizon H. By §2, freezing (no repair after formation) is optimal iff q_s ≤ q_f = 2c/(WH²), that is, iff T ≤

**T_f = E_a / (k · ln(ν₀ · W H² / (2c))).**

- **This is the Néel/Brown blocking-temperature form**, T_B = E_a / (k ln(ν₀ t_obs)) (Brown 1963 for the thermal-fluctuation theory), and it matches Dodson's log form. Here H plays t_obs, and the dimensionless lifetime-stake-to-two-reads ratio W·H/(2c) (where W/c is the price ratio) sits inside the logarithm.
- **Consequence:** the elasticity of T_f with respect to c/W is 1/ln(…) ≈ 0.01–0.016 at E_a = 1 eV and ν₀ = 10¹³ s⁻¹ (S8). A 1000× change in prices moves T_f by about 10% (−9.8% in S8).
- Upkeep goes smoothly to zero as T falls: repair effort is ∝ √q_s ∝ e^{−E_a/(2kT)}, and the corner is reached continuously at T_f, with h_m = 0.

**Reading.** Where a selected system chooses between repairing and freezing a store (dormancy, spores, seeds, cryptobiosis; bet-hedging theory starts with Cohen 1966), the switch temperature should depend on prices only logarithmically. It is nearly price-free, which suits testing. OPEN, not qualified as a test.

---

## 8. What is genuinely new, and what is prior art

| Item | Status | Credit |
|---|---|---|
| Frozen = q → 0 limit of held (G3 with H = ∞; corner at q_f with finite H) | PROVED (in-model) | G3 and Theorem 8 already contain it; this file states it. Value of information → 0 as drift → 0 is standard. |
| The freeze edge is continuous (C¹ kink) while the lookup edge is a cliff | PROVED (in-model) | **KNOWN / novelty 0:** implicit in Theorem 8's proof; cliff is Cho & Garcia-Molina 2003. |
| Fixed machinery cost → first-order switch, effort jump √(h_m/(cH)), q\* closed form | PROVED (in-model) | **KNOWN / novelty 0:** elementary fixed-cost non-convexity algebra. |
| Ruin cap forces a discontinuous melt at q_r | PROVED (in-model) | **KNOWN / novelty 0:** elementary. |
| Freeze-out when optimal update interval > cooling time; q_fo = 2c/(Wτ_c²) | PROVED (EL & form); NUMERICAL (0.46–1.03) | **KNOWN in substance (novelty 0–1):** Hayashi 1950; Lee & Weinberg 1977; Dodson 1973; Zurek 1985; optimal checking/sampling/EOQ/inattention: Barlow et al. 1963; Keller 1974; Hollier & Mak 1983; Viscolani 1991; Reis 2006; Alvarez et al. 2011; Rabi et al. 2012; Abel et al. 2007, 2013; Sun et al. 2020. |
| Relic design iff ∫dt/τ_a < ∞; f_∞ ∝ τ_c^{−1/(αζ)} (exact γ_E prefactor) | PROVED (in-model); NUMERICAL | Freeze-out-integral form KNOWN (cosmology); KZ-like power law is ANALOGY; ζ is assumed, not derived. |
| No static hysteresis; Dixit band with switching costs; rate-dependent loop | PROVED / KNOWN / NUMERICAL | Dixit 1989; dynamic hysteresis Jung et al. 1990, Chakrabarti & Acharyya 1999; relaxed selection Lahti et al. 2009. |
| T_f with price inside a log | PROVED (in-model) | Néel/Brown blocking form; Dodson closure form; Kramers. |
| Protons, nuclei and crystals "froze out" of held equilibria | ANALOGY (physics KNOWN) | Weak-interaction n/p freeze-out (Hayashi 1950); the QCD transition is a crossover (Aoki et al. 2006). GTAO's design predictions do not apply (E1). |

**Honest net.** The process view Chad intuited is real, and physics already has it as freeze-out. The cost equation reproduces that criterion without being told to. That is a consistency result: the same "rate versus change-of-rate" logic falls out of minimizing judgment cost. It is not a discovery in physics. The GTAO-specific content is narrow:
- for *selected* systems the frozen-out quantities are *chosen* (read rates and designs), so the freeze-out points and relics carry the price ratio, mostly inside logs or square roots;
- three testable predictions follow: abrupt versus gradual shutdown by fixed machinery cost (§3.1), relic investment as a power of the ramp time (§5), and a nearly price-free freeze temperature (§7).

None is preregistered or qualified.

**What would change the picture.**
- A derivation of ζ from a specific selection model.
- A non-renewal (filtering) version of §2's continuity.

---

## 9. Proposed follow-ups (not started; nothing edited outside this file)

1. Independent review completed in `records/reviews/freeze_2026-11-21/REVIEW.md` (READY-WITH-FIXES; S1–S3 applied on branch).
2. If confirm passes, a one-line pointer from `theory/SCALE_ENDS.md` §2 (E4) and `THEORY.md` CT11 to this file. That would be a separate PR and needs the usual review and confirm.
3. Targeted prior-art search for §4 completed in review (see §4 and §8; downgraded to KNOWN in substance, novelty 0–1).

---

## References (each DOI resolved on Crossref, 21 Nov 2026)

- Abel AB, Eberly JC, Panageas S 2007, "Optimal inattention to the stock market," *Am Econ Rev* 97:244–249, doi 10.1257/aer.97.2.244
- Abel AB, Eberly JC, Panageas S 2013, "Optimal inattention to the stock market with information costs and transactions costs," *Econometrica* 81:1455–1481, doi 10.3982/ECTA7624
- Alpher RA, Bethe H, Gamow G 1948, "The origin of chemical elements," *Phys Rev* 73:803–804, doi 10.1103/PhysRev.73.803 (background only)
- Alvarez F, Lippi F, Paciello L 2011, "Optimal price setting with observation and menu costs," *Q J Econ* 126:1909–1960, doi 10.1093/qje/qjr043
- Aoki Y, Endrődi G, Fodor Z, Katz SD, Szabó KK 2006, "The order of the quantum chromodynamics transition predicted by the standard model of particle physics," *Nature* 443:675–678, doi 10.1038/nature05120
- Barlow RE, Hunter LC, Proschan F 1963, "Optimum checking procedures," *J Soc Ind Appl Math* 11:1078–1095, doi 10.1137/0111080
- Brown WF Jr 1963, "Thermal fluctuations of a single-domain particle," *Phys Rev* 130:1677–1686, doi 10.1103/PhysRev.130.1677
- Chakrabarti BK, Acharyya M 1999, "Dynamic transitions and hysteresis," *Rev Mod Phys* 71:847–859, doi 10.1103/RevModPhys.71.847
- Cohen D 1966, "Optimizing reproduction in a randomly varying environment," *J Theor Biol* 12:119–129, doi 10.1016/0022-5193(66)90188-3
- Dixit A 1989, "Entry and exit decisions under uncertainty," *J Polit Econ* 97:620–638, doi 10.1086/261619
- Dodson MH 1973, "Closure temperature in cooling geochronological and petrological systems," *Contrib Mineral Petrol* 40:259–274, doi 10.1007/BF00373790
- Hayashi C 1950, "Proton–neutron concentration ratio in the expanding universe at the stages preceding the formation of the elements," *Prog Theor Phys* 5:224–235, doi 10.1143/ptp/5.2.224
- Hollier RH, Mak KL 1983, "Inventory replenishment policies for deteriorating items in a declining market," *Int J Prod Res* 21:813–836, doi 10.1080/00207548308942414
- Jung P, Gray G, Roy R, Mandel P 1990, "Scaling law for dynamical hysteresis," *Phys Rev Lett* 65:1873–1876, doi 10.1103/PhysRevLett.65.1873
- Keller JB 1974, "Optimum checking schedules for systems subject to random failure," *Manage Sci* 21:256–260, doi 10.1287/mnsc.21.3.256
- Kibble TWB 1976, "Topology of cosmic domains and strings," *J Phys A* 9:1387–1398, doi 10.1088/0305-4470/9/8/029
- Kirkpatrick S, Gelatt CD, Vecchi MP 1983, "Optimization by simulated annealing," *Science* 220:671–680, doi 10.1126/science.220.4598.671
- Kramers HA 1940, "Brownian motion in a field of force and the diffusion model of chemical reactions," *Physica* 7:284–304, doi 10.1016/S0031-8914(40)90098-2
- Lahti DC et al. 2009, "Relaxed selection in the wild," *Trends Ecol Evol* 24:487–496, doi 10.1016/j.tree.2009.03.010
- Lee BW, Weinberg S 1977, "Cosmological lower bound on heavy-neutrino masses," *Phys Rev Lett* 39:165–168, doi 10.1103/PhysRevLett.39.165
- Rabi M, Moustakides GV, Baras JS 2012, "Adaptive sampling for linear state estimation," *SIAM J Control Optim* 50:672–702, doi 10.1137/090757125
- Reis R 2006, "Inattentive consumers," *J Monet Econ* 53:1761–1800, doi 10.1016/j.jmoneco.2006.03.001
- Sun Y, Polyanskiy Y, Uysal E 2020, "Sampling of the Wiener process for remote estimation over a channel with random delay," *IEEE Trans Inf Theory* 66:1118–1135, doi 10.1109/TIT.2019.2937336
- Viscolani B 1991, "A note on checking schedules with finite horizon," *RAIRO - Operations Research* 25:203–208, doi 10.1051/ro/1991250202031
- Zurek WH 1985, "Cosmological experiments in superfluid helium?" *Nature* 317:505–508, doi 10.1038/317505a0
- Not DOI-checked: Kolb EW & Turner MS 1990, *The Early Universe* (Addison-Wesley), textbook; Néel L 1949, *Ann Géophys* 5:99 (cited by form only).
- Already in the repo: Cho & Garcia-Molina 2003 (Theorem 8); Mitchell et al. 2009 (litmap).
