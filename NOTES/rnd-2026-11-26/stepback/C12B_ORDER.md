# C12b: ordering two stake thresholds (track vs keep), on paper

*26 Nov 2026, about 09:10 ET. Local note only (not committed or pushed). Repo text read at `ac92ee2` (/workspace/lemmar-check). Labels: **PIM** = proved in-model (in a named class); **KNOWN** = published, credited for what it states; **ELEMENTARY** = direct consequence of PIM/KNOWN; **HYP** = hypothesis, not shown; **OBSERVED** = numerical output of `c12b_check.py` (→ `c12b_check.out`). A lower bound is not a derivation of the cost. Units kT = 1 in the script.*

## 0. Result

1. **C12b as first framed is empty at the floor.** "Repair a record versus let it decay and re-learn it, in one live world" gives no second threshold. While the source is present, the leak Γ cancels from the heat floor (T59: Q̇_M ≥ kT·r·L(ε) has no Γ; **PIM** for a two-state telegraph world and a two-state memory under local detailed balance). Re-learning is never more expensive at the floor than repair. In a frozen world that is still present (r = 0), a static bias holds the record at zero ongoing heat (T59 case 1; T62 AL-stock-free). Outside the two-state class, the cancellation is **HYP**.
2. **The non-empty version is track versus keep.** w₁ is the stake at which tracking a **live** source pays. w₂ is the stake at which keeping a record of a **gone** source (T63 class RF) pays.
3. **Binary class: no positive thresholds.** Both onset curves are quadratic at the blind point (L(½−δ) ≈ 8δ², 4(ln2 − h(½−δ)) ≈ 8δ²; OBSERVED (a)). So w₁ = 0 (**PIM**: CORE:74 floor is tight), and the RF lower bound only gives w₂ ≥ 0, which is vacuous. "w₂ = w₁" holds trivially at 0, so the route is empty in the binary class. What survives is a **scaling identity** for one carrier (ELEMENTARY from RF's exact one-carrier value kTΓL(ε) and CORE:74): the keep design at stake w has the same error as the track design at stake w·r/Γ (OBSERVED (b)). This holds only *if* the one-carrier floor is attained, which RF leaves open for a b-blind corrector.
4. **Gaussian class: a closed form, half of it on a HYP floor.**
   - w₁ = kT·r/v. This is **PIM** in the repo: CORE.md:91–92, an OU world at rate r and variance v at the thermal floor.
   - w₂ ≥ kT·Γ/Var. This is **HYP**. It rests on an extension of RF-general to a continuous OU carrier (§3.2), which is not proved.
   - Together: **w₂/w₁ ≥ (Γ/r)·(v/Var)**, which is Γ/r when the kept value is the source's last state (Var = v). Keeping switches on after tracking as the stake rises iff Γ > r (at least; the keep floor's attainment is open).
5. **Scope (reusing C12C §11):**
   - The closed forms are Gaussian-only.
   - Both onsets are 1-D convex problems, so Theorem O applies to the lower-bound functions. With a **stake-free** accuracy cap, each onset is a union: "on iff w > w_i or the cap is below the blind error".
   - With a **CT22-type** (stake-carrying) cap the statements are inapplicable at w = 0.
   - Lemma A(b′) needs convexity or no duality gap; the lower-bound functions here are convex, but the attained design sets are not shown to be.

## 1. Repo text used (read this session at `ac92ee2`)

- **CT4** (THEORY.md:88 row, :279; C12C §1): a model is carried iff κ < −(D∘IB)′(0⁺). With a stake w, this reads w > w₁ = κ/(−(D∘IB)′(0⁺)). Gaussian AR(1): w₁ = κ/(2 ln2·a²·Var). This is the per-bit-price form.
- **CORE.md:91–92**, OU world at rate r (the repo writes a) and variance v: the heat infimum at error ε is kT·r(v−ε)/ε. Above stake kT·r/v the minimum cost is 2√(kT r v w) − kT r; at or below it, the design is blind, at cost w·v. This is the thermal-floor form of CT4; CORE:96 reads it as "stakes-to-thermal ratio above 1".
- **CORE.md:74 / T59 §0** (FREEZE_OR_HOLD_FLOOR): Q̇_M ≥ kT r L(ε), tight at the symmetric two-state copy. "The leak rate Γ cancels: leak jumps are memory jumps, and they enter the net flow with the opposite sign to the copy." (PIM, two-state, LDB). At r = 0, a static bias costs zero ongoing heat.
- **T63 Proposition RF** (RECORD_REPAIR_FLOOR): for a fair bit whose source is gone, in carriers leaking at ≥ Γ, Q̇ ≥ kTΓg(ε) − kT S_max/τ, with g ≥ 4(ln2 − h(ε)). For one carrier the value is kTΓL(ε) exactly. **RF-general** (ELEMENTARY): for any finite medium with flip-symmetric reversible passive dynamics, Q̇ ≥ kTρ(ln2 − h(ε)) − kT S_max/τ, with ρ the modified log-Sobolev constant. Attainment for a b-blind corrector is open (RF-forget).
- **C12C_ONSET §11** (local): Theorem O (1-D convex onset; union with a stake-free cap); the M1 upgrade (class-A onset corner over all memories); the stake-free vs CT22 split; Lemma A(b′)/(b″) conditions.

## 2. Which thresholds, in which world

**World W (stated before deriving).**
- A source X is live, with drift rate r: a telegraph flipping at rate r (binary class), or an OU process at rate r and variance v (Gaussian class).
- At some time the source is gone: nothing outside the record depends on its last value.
- The record sits in carriers whose passive leak relaxes at rate Γ.
- The stake w multiplies Hamming error (binary) or squared error (Gaussian), per unit time.
- Caps are slack unless stated. The temperature is the bath's kT (the heat floor, not the ruin or selection temperature).

- **w₁ (track onset):** the infimum stake at which the cheapest live-phase design holds information about X_t, rather than staying blind.
- **w₂ (keep onset):** the infimum stake at which the cheapest gone-phase design holds information about the last value, rather than letting the record relax and paying the blind loss.
- **Not w₂:** "repair beats re-learn with the source live". §0.1 shows that version has no threshold at the floor.

## 3. Derivation

### 3.1 Binary class

- **Track.** J(ε) ≥ kT r L(ε) + wε, tight (CORE:74). L′(½) = 0 and L(½−δ) = 8δ² + O(δ⁴), so J′(½⁻) = 0 − w < 0 for every w > 0. Hence **w₁ = 0 (PIM)**. Theorem O reads this as f′(0⁺) = −∞ in information units, since δ ∝ √I.
- **Keep.** J(ε) ≥ kTΓg(ε) + wε, with g ≥ 4(ln2 − h) = 8δ² + O(δ⁴). The lower bound has zero slope at blind, so it gives only **w₂ ≥ 0**, which is vacuous. With one carrier (g = L exactly), *if* the floor is attained, w₂ = 0.
- **Scaling (ELEMENTARY, conditional on attainment).** With one carrier, kTΓL(ε) + wε = (Γ/r)·[kT r L(ε) + (w r/Γ)ε]. So ε*_keep(w) = ε*_track(w·r/Γ). OBSERVED (b) matches to 6 digits at r = 0.3, Γ = 1.7.
- **Repetition codes** (g bounded, ≈ 8–9.24, at small ε; T63 numerical) beat L(ε) → ∞ only deep in the small-ε regime. That changes the high-stake designs, not the onsets.
- **Conclusion:** in the binary class the thresholds are both 0. The route is empty there.

### 3.2 Gaussian class

- **Track (PIM, repo).** f(ε) = kT r (v−ε)/ε + wε on (0, v]. f′(v) = w − kT r/v, and f is convex. So **w₁ = kT r/v**. OBSERVED (c): ε* = v at w/w₁ = 0.99 and ε* < v at 1.01.
- **Keep (HYP floor).** The proposed floor is **Q̇ ≥ 2kTΓ·I(X;M)** (nats), for a record of a gone Gaussian value X ~ N(0, Var) in an OU carrier relaxing at rate Γ. Sketch of the extension of RF-general:
  1. The average over x of D(p_x‖π) is ≥ I(X;M) (ELEMENTARY: it equals I + D(p_M‖π)).
  2. For an OU carrier, relative entropy decays at rate ≥ 2Γ. This is the Gaussian log-Sobolev / Bakry–Émery constant, KNOWN (Gross 1975 for the Gaussian LSI). OBSERVED (h) gives a rate of 2Γ for a mean offset.
  3. RF's housekeeping step (heat ≥ kT × the entropy production a corrector must offset) is then applied as in RF.

  What is missing, so this stays HYP:
  - RF is for **finite** media. Its −kT S_max/τ term has no finite analogue for a continuous carrier.
  - Step 3 is stated in the repo for finite Markov chains only.
  - Without a bound on carrier amplitude, storing at large amplitude makes the passive information loss arbitrarily small (§3.3 F-v). So an amplitude or energy bound is a needed input. The LSI form above builds one in, through the stationary distribution π.
- **Keep cost.** Use the KNOWN Gaussian rate–distortion D(I) = Var·e^{−2I} (Cover & Thomas). The keep lower bound is F(I) = 2kTΓ·I + w·Var·e^{−2I}, which is convex. F′(0) = 2kTΓ − 2wVar. So I* > 0 iff **w > kTΓ/Var**, with I* = ½ ln(wVar/(kTΓ)). This is ELEMENTARY given the HYP floor; OBSERVED (g) agrees with the closed form.
  - Since F is a **lower** bound, the conclusion is only that keeping does not pay for w ≤ kTΓ/Var. So **w₂ ≥ kTΓ/Var**, with equality iff the floor is attained near I = 0 (open, as in RF).
- **Ratio:** **w₂/w₁ ≥ (Γ/r)(v/Var)**. If the kept value is the source's last state, Var = v and the ratio is **≥ Γ/r**.
  - The original §10 guess ("if r > Γ, w₂ may not exist") is wrong in this class. Its lower bound kTΓ/Var is finite for every Γ > 0 and lies below w₁ when Γ < r. Whether w₂ itself lies below w₁ then depends on the floor's attainment, which is open.
  - The §10 guess "w₂/w₁ is a function of Γ/r" is right here, at equal variance.

### 3.3 Where the closed form fails (stated, not hidden)

- **(F-i) Binary records:** thresholds are 0 (§3.1). There is no ordering.
- **(F-ii) Live source:** leak cancels at the floor (T59, PIM in two-state). There is no repair threshold.
- **(F-iii) Present frozen reference:** zero ongoing heat (T59/T62), so w₂ = 0.
- **(F-iv) Self-correcting media** (T63 §5, 2D/3D Ising below ordering): the effective Γ falls with block size. The ratio then uses the logical leak Γ(m), not the carrier Γ.
- **(F-v) Unbounded carrier amplitude:** no keep floor at all. Check (d) shows the loss rate 2ΓI near I = 0 under two storage conventions (noise at thermal level; total variance at thermal level). They differ at larger I (≈ 0.91 vs 1.11 × 2ΓI at I = 0.1), so only the onset slope is convention-free.
- **(F-vi) Non-Gaussian worlds:** C12C §11.2 showed Gaussian closed forms are upper bounds over all memories for chance caps (the tail-flag example). Here the cap is slack. Whether CORE:91–92's OU heat infimum holds over all (non-Gaussian) memories is **not checked in this note**; the class-A all-memories argument in C12C §11.2 is for CT4's per-bit pricing, not for the thermal-floor form. For the keep side, D(I) = Var e^{−2I} is the Gaussian-source RD bound, valid for every memory of a Gaussian X (KNOWN), so the keep lower bound is over all memories given the HYP floor.

## 4. Numerical sanity (OBSERVED; `c12b_check.py` → `c12b_check.out`)

| check | what | result |
|---|---|---|
| (a) | L(½−δ)/δ², 4(ln2−h)/δ² → 8 | 8.000011, 8.000005 at δ = 10⁻³ |
| (b) | ε*_keep(w) = ε*_track(w r/Γ), one carrier | equal to 6 digits, w = 10⁻³…10 |
| (c) | OU track onset at w₁ = kT r/v | blind at 0.99 w₁; ε* = 1.990 at 1.01 w₁ |
| (d) | OU-carrier information loss / (2ΓI) as I → 0 | 0.999 and 1.001 at I = 10⁻³ |
| (e) | keep cost with loss rate Γ(1−e^{−2I}) | onset at w₂ = kTΓ/Var (bang-bang) |
| (g) | HYP floor F(I): numerical I* vs closed form | equal (e.g. 0.549306 at 3w₂) |
| (h) | OU relative-entropy decay rate / Γ | 1.999997 |

These check algebra only. They do not test the HYP floor.

## 5. Prior art (DOIs checked on Crossref this session: `crossref_c12b.txt`)

- **Ordered onset thresholds are KNOWN in the information bottleneck.** Chechik, Globerson, Tishby & Weiss 2005, *JMLR* 6:165–188 (no DOI; JMLR page read this session). In the Gaussian IB, mode i switches on at β_i^c = 1/(1−λ_i), a cascade ordered by eigenvalue. CT4's w₁ is the one-mode case.
  - Wu, Fischer, Chuang & Tegmark 2019, *Entropy* 21:924, doi 10.3390/e21100924 (Crossref OK): an IB "learnability" threshold β₀.
- **Rate–distortion:** reverse water-filling switches Gaussian components on in order of variance. KNOWN, Cover & Thomas, *Elements of Information Theory*, doi 10.1002/047174882X (Crossref OK; 2005 record). D(I) = Var e^{−2I} is used above.
- **Rational inattention:** zero attention below a cost/stake threshold. KNOWN (Sims 2003, *J. Monetary Econ.*, doi 10.1016/S0304-3932(03)00029-1, Crossref OK; Matějka–McKay as verified earlier in C12C).
- **Thermodynamics:**
  - Still, Sivak, Bell & Crooks 2012, doi 10.1103/PhysRevLett.109.120604 (Crossref OK): no stake, no threshold.
  - Gross 1975, *Amer. J. Math.* 97:1061, doi 10.2307/2373688 (Crossref OK): Gaussian log-Sobolev, used in §3.2 step 2.
  - Chiuchiù et al. 2018 (already credited in T63): keeping one bit.
- **Found, not assessed:**
  - arXiv:2611.20248 (Nov 2026, abstract only), on the cost of keeping predictive records of a switching environment from rare observations. It has no stake threshold in the abstract.
  - Several Zenodo deposits on "maintenance thermodynamics" and memory obsolescence. These are unreviewed and not read; they are not cited as support.
- **Ordering by rate:** I found no source that orders a keep-onset against a track-onset by Γ/r. The search was short (two web queries plus the repo's T59/T63 prior-art sections), so read this as "not found", not "new". The ingredients are KNOWN, and the composition is ELEMENTARY given the HYP floor.

## 6. Labels

| claim | label |
|---|---|
| Leak cancels with the source live, so no repair-vs-relearn threshold | PIM (two-state, LDB; T59); HYP elsewhere |
| Binary: w₁ = 0 | PIM (CORE:74 tight) |
| Binary: RF gives only w₂ ≥ 0 | ELEMENTARY |
| One-carrier scaling ε*_keep(w) = ε*_track(wr/Γ) | ELEMENTARY, conditional on attainment (open) |
| Gaussian w₁ = kT r/v | PIM (repo, CORE:91–92) |
| Gaussian keep floor Q̇ ≥ 2kTΓ·I | HYP (RF-general extended to a continuous carrier; S_max step missing) |
| w₂ ≥ kTΓ/Var and w₂/w₁ ≥ (Γ/r)(v/Var) | ELEMENTARY given the HYP floor |
| Union onset under a stake-free cap | Theorem O applied to the lower-bound functions (PIM for those functions) |
| Ordered thresholds in IB/RD/RI | KNOWN (by component variance/eigenvalue, not by rate) |

## 7. Rescore (§13 scale; reviews and sunk cost not scored)

- **C12b as first framed (repair vs re-learn, live source):** empty at the floor. It is retired from the rank, and its 0.90 row is withdrawn.
- **New row C12b-G: prove the Gaussian keep floor** (RF-general for an OU carrier with a bounded-amplitude input; settle the S_max/τ analogue).
  - A hit makes w₂ ≥ kTΓ/Var and the Γ/r ordering PIM as lower bounds.
  - A likely miss is "the continuous carrier needs a finite-state or amplitude input", which RF already implies, so it locates little.
  - p_hit 0.5, V_hit 3, p_miss 0.5, V_miss 2 → EIV 2.5; cost ≈ 2 h → **≈ 1.25 per hour**.
  - Caveats: V_hit = 3 is generous given that the IB/RD ordering is KNOWN. At V_hit 2.5 the rate is ≈ 1.1.
- **Top 3 (Lean aside):** C12b-G ≈ 1.25 · SR-b ≈ 0.87 (0.80 at prior 0.2) · C1 0.83. With Lean ×3: C12c-L ≈ 2.35, then C9 ≈ 1.2.

## 8. C12b-G: the Gaussian keep floor on paper (appended 26 Nov 2026, about 09:40 ET; §§0–7 stand as written; where they conflict, this section governs)

**Status: PROVED (in-model) in class G-keep below, conditional on one chosen input (a second-moment, or amplitude, cap) plus a stated start-state premise.** Without the cap, the long-horizon statement is not shown. The rate inequality itself does not need the cap (§8.4, a correction to §3.2 and §3.3 F-v). Attainment for a corrector that does not know x is **OPEN**, as in T63. So the floor gives a lower bound on w₂, not w₂ itself.

### 8.1 Class G-keep (every premise named; the T63 counterpart in brackets)

- **(P0) Source.** X ~ N(0, Var) is written; then the source is gone. [T63: fair bit b.] The proof does not use "gone": the inequality holds even for a corrector that knows x. "Gone" matters only for attainment (§8.5).
- **(P1) Record and leak.** The record is M ∈ ℝ^d, with d finite. Coordinate i has a leak that is **a mechanism of its own**: an overdamped channel with its own bath coupling (diffusion D_i, independent noise) and force from U_L(m) = kT Σ m_i²/(2s_i²). Its stationary distribution is π = N(0, diag s_i²), and its relaxation rate is Γ_i = D_i/s_i² ≥ Γ > 0. Leak forces and noise do not depend on the corrector state c or on x ("the medium does not know x"). [T63: leak rates Γ_i ≥ Γ, fixed by the medium, not modulated.]
- **(P2) Corrector.** Any corrector C (continuous, discrete, or both) acts on M and on itself through further mechanisms: diffusive channels or jumps. Each is in local detailed balance with the same bath at T and with any work or fuel reservoirs. The joint (M, C) is a Markov process. The entropy-production accounting σ_tot = Ṡ_joint + Ṡ_res = Σ_k σ_k, with every σ_k ≥ 0, holds. [T63: same, "Schnakenberg".] This is KNOWN for diffusive channels (Seifert 2012, §§ on Langevin/Fokker–Planck stochastic thermodynamics) and for jump channels (Schnakenberg 1976). For mixed processes it is taken as a premise with the same accounting. Q̇ ≡ kT·Ṡ_res, as in T63: heat to the bath, or free energy consumed with fuel.
- **(P3) Decoder.** The decoder reads M only, and mean squared error ≤ D at every t ∈ [0, τ]. [T63: decoder D ⊂ {0,1}^n reads the record only.] If the decoder may read a non-leaking C, there is no floor: store x in C.
- **(P4) Regularity.** The conditional densities p_x(m, c, t) are smooth enough that the Fokker–Planck currents, relative Fisher information and the integrations by parts exist. Where Fisher information is infinite, the inequality holds trivially.
- **(P5) Boundary (the continuous replacement for S_max).** Let S_x(t) be the joint differential entropy of (M, C) given x, plus ln K if C has a discrete part with K states. The premise is:
  S_range := sup_t E_x S_x(t) − E_x S_x(0) < ∞.
  - **A sufficient pair** is (A) and (W).
  - **(A), CHOSEN input: a second-moment cap.** E|Z_t|² ≤ d_Z·A² for the continuous part Z = (M, C_cont) of dimension d_Z. Then E_x S_x(t) ≤ (d_Z/2) ln(2πe A²) + ln K, by the Gaussian maximum-entropy bound plus Jensen over x (KNOWN). A cap on stored energy is the physical form. It is a modeling choice, like T63's finite medium; nothing in the cost sets it.
  - **(W), premise: the horizon starts before the write**, from a state that does not depend on x and has finite entropy S_pre. The one-time write heat is then inside Q (as T59's C_write). With the carrier at π, S_pre ≥ (d/2) ln(2πe·min s_i²). If (W) is dropped, a delta-like written state has E_x S_x(0) = −∞ and the bound is vacuous at finite τ.
  - Under (A) and (W), with the corrector starting at the same scale: S_range ≤ d ln(A/s) + ln K (OBSERVED (6) gives examples).
  - A weaker sufficient form of (A): sub-exponential growth of E|Z_t|². Then S grows at most like o(t), and S_range/τ → 0.

### 8.2 Proposition G-keep and proof (each step labeled; numbers refer to `c12bg_check.out`)

**Proposition G-keep (PROVED (in-model), class G-keep).** Averaged over x and over [0, τ]:

  Q̄ ≥ 2kTΓ·(1/τ)∫₀^τ I(X; M_t) dt − kT·S_range/τ ≥ kTΓ·ln(Var/D) − kT·S_range/τ.

*Proof.* Fix x. Conditioned on x, (M, C) is a Markov process; its rates may depend on x only through the corrector, under (P0)–(P2).

- **Step 1 (per-channel entropy-production inequality; KNOWN, P2).** σ_tot[p_x] = Ṡ_x + Q̇_x/kT = σ_L[p_x] + Σ_{k≠L} σ_k ≥ σ_L[p_x]. The leak's part is
  σ_L[p] = Σ_i D_i ∫ p·(∂_{m_i} ln(p/π))² dm dc
  because the leak current on coordinate i is j_i = −D_i·p·∂_{m_i} ln(p/π), and σ = ∫ j²/(D p).
- **Step 1′ (project out the corrector; ELEMENTARY).** By Cauchy–Schwarz, ∫ a(c)²/b(c) dc ≥ (∫a)²/(∫b). Here a = π·∂_i(p/π) = ∂_i p + p·m_i/s_i² and b = p. This is linear in p, so it integrates to the same form for p_M, and ∫ a dc = π·∂_i(p_M/π). Hence σ_L[p_x] ≥ σ_L[p_{M|x}]. This needs P1: the leak force does not depend on c. It is the continuous counterpart of T63's log-sum step. OBSERVED (2): min joint/marginal ratio 1.000336 over 200 random cases.
- **Step 2 (Gaussian log-Sobolev; KNOWN, Gross 1975; Bakry–Émery 1985).** For π = N(0, diag s_i²) and any q,
  D(q‖π) ≤ ½ Σ_i s_i² ∫ q·(∂_i ln(q/π))².
  Since D_i = Γ_i s_i² ≥ Γ s_i², σ_L[q] ≥ Γ·Σ_i s_i² ∫ q(∂_i ln(q/π))² ≥ 2Γ·D(q‖π). Equality holds iff q is a shifted π. OBSERVED (1): min ratio 1.000692 over 300 random mixtures, and 1.000000 for a shifted Gaussian. Redundancy (larger d) does not raise or lower the constant 2Γ. This parallels T63 Step 3's tensorization (4Γ for bits).
- **Step 3 (ELEMENTARY).** E_x D(p_{M|x}‖π) = I(X; M) + D(p_M‖π) ≥ I(X; M). OBSERVED (3): matches to Monte Carlo error.
- **Step 4 (decoder; KNOWN).** For Gaussian X and any estimator X̂ = f(M_t), E(X − X̂)² ≥ Var·e^{−2I(X;X̂)} ≥ Var·e^{−2I(X;M_t)}. This is the Gaussian rate–distortion function plus data processing (Cover & Thomas, Thm 10.3.2 and §2.8). So MSE ≤ D implies I(X; M_t) ≥ ½ ln(Var/D). [T63 Step 4: the kl decoder bound.] For non-Gaussian X, replace Var by the entropy power N(X) ≤ Var (Shannon lower bound; KNOWN).
- **Step 5 (integrate; ELEMENTARY).** From Step 1, Q_x/kT = ∫₀^τ σ_tot dt − [S_x(τ) − S_x(0)] ≥ ∫₀^τ σ_L[p_{M|x}] dt − [S_x(τ) − S_x(0)]. Apply Steps 1′, 2, 3, average over x, and bound the bracket by S_range (P5). Divide by τ and apply Step 4. ∎

**Sanity (OBSERVED (4), (5)).** Consider a corrector that knows x, coupled through its own channel: dm = −Γm dt − κ(m − x)dt + two independent noises, with s_C = s.
- Analytic σ_L = Γa²Var/s², σ_C = κ(1−a)²Var/s², a = κ/(Γ+κ). At Γ = 1, κ = 3, Var = 2, s = 1 the total is 1.5000.
- A Langevin simulation measuring Stratonovich heat per channel gives 1.4941 ± 0.0148 (N = 20000, dt = 0.002).
- σ_L/(2ΓI) = u/ln(1+u) with u = a²Var/s². It is ≥ 1 and tends to 1 as u → 0. So in this family the floor is approached near onset, which is the only place the w₂ argument uses it. That is a corrector that knows x, the housekeeping case T63 also uses for attainment; it is not a construction for a corrector that does not know x.

### 8.3 Consequence for w₂ (C12b)

- Long-horizon keep cost ≥ kTΓ·ln(Var/D) + w·D for constant designs.
- For time-varying designs, per instant: ≥ 2kTΓ·I_t + w·Var·e^{−2I_t}. This is convex in I_t and is minimized at I_t = 0 iff w ≤ kTΓ/Var.
- So in class G-keep, for τ → ∞ (or τ ≫ S_range/Γ), keeping does not pay for w ≤ kTΓ/Var. That is **w₂ ≥ kTΓ/Var: PROVED (in-model)** as a lower bound, conditional on (A) and (W).
- With w₁ = kT r/v (PIM, CORE:91–92, OU tracking class): **w₂/w₁ ≥ (Γ/r)(v/Var)** is an ELEMENTARY composition of two PIM statements in two named classes. The §6 row "Gaussian keep floor: HYP" is upgraded to "PIM in class G-keep, conditional on (A), (W)". The §6 row for the ratio becomes "ELEMENTARY from two PIM statements".
- **What stays open:**
  - whether w₂ equals this bound (attainment by a corrector that does not know x; the counterpart of RF-forget means a fully leaky scheme decays, so only horizon-limited statements are possible);
  - whether w₂ < w₁ when Γ < r.

### 8.4 Corrections to §3.2 and §3.3 (append-only)

- **§3.2 "What is missing"**, first and third bullets:
  - The S_max counterpart is now supplied as (P5).
  - The amplitude bound is needed **only for the boundary term**, not for the rate inequality. The claim "Without a bound on carrier amplitude, storing at large amplitude makes the passive information loss arbitrarily small … So an amplitude or energy bound is a needed input" mixes two quantities. A large-amplitude record does lose information slowly *passively*, but holding it costs at least σ_L ≥ 2Γ·D(p_{M|x}‖π). That grows with amplitude, because D includes the mean-offset term (mean²/(2s²)).
  - The second bullet ("Step 3 is stated in the repo for finite Markov chains only") is answered by Step 1 above. Its continuous form is KNOWN (P2).
- **§3.3 F-v**, "Unbounded carrier amplitude: no keep floor at all": **withdrawn**. Corrected: an unbounded second moment voids only the S_range/τ term at finite τ. Under sub-exponential moment growth, the long-horizon floor stands.
- **§0.4 and §3.2 labels** are upgraded as stated in §8.3.

### 8.5 Scope limits (where the proof does not reach; for the hostile review)

- **(S1) Same-channel correction is out of class.**
  - Suppose the corrector pushes M through the *same* friction and noise as the leak. An example is an external force F_C(m, c) added to −U_L′. Then the leak is not a separate mechanism, and Step 1's split does not exist.
  - Example: F_C = U_L′(m) − V′(m − c), with a static C storing x. This gives M an equilibrium potential V(m − c) at zero ongoing heat. That is T59's static bias, in which the medium knows x through c.
  - P1 excludes it, as T63's "not modulated" premise does. Whether a physical carrier's leak is a separate channel is a **modeling choice**, and it decides whether this floor applies at all.
- **(S2) Readable non-leaky corrector.** This is excluded by P3. If C is non-leaky and readable, the floor applies to M but not to the system.
- **(S3) Non-convex leak potentials.** For U_L with Hess U_L ≥ kT/s² (Bakry–Émery), the same constant holds (ELEMENTARY, KNOWN criterion). For double wells, the LSI constant is set by the barrier, as in T63's self-correcting caveat. The floor can then be exponentially small; this is the continuous counterpart of the RF-general / §5 loophole.
- **(S4) Overdamped only.** Underdamped carriers (an inertial leak) are not treated.
- **(S5) Horizon.** For finite τ the penalty kT·S_range/τ is real. With A/s = 100 and d = 3 it is 13.8 kT/τ (OBSERVED (6)).

### 8.6 Is it known? (DOIs checked on Crossref this session; `crossref_c12bg.txt`)

- **Ingredients, all KNOWN:**
  - per-channel entropy production: Seifert 2012, *Rep. Prog. Phys.* 75:126001, 10.1088/0034-4885/75/12/126001; Schnakenberg 1976, *Rev. Mod. Phys.* 48:571, 10.1103/RevModPhys.48.571;
  - the Gaussian LSI: Gross 1975, 10.2307/2373688; Bakry & Émery 1985, *Sém. Prob. XIX* (LNM 1123):177–206, 10.1007/BFb0075847;
  - Gaussian rate–distortion: Cover & Thomas, 10.1002/047174882X.
- **Horowitz & Esposito 2014**, *PRX* 4:031015, 10.1103/PhysRevX.4.031015: bipartite information-flow inequality (the repo's JP-heat). It bounds heat by a *net information flow*. With the source gone and static, the leak makes the flow to M about X negative, so that bound gives no positive floor. It does not give a floor proportional to the stock I.
- **Still et al. 2012**, 10.1103/PhysRevLett.109.120604: dissipation ≥ kT(I_mem − I_pred). For a static gone X, I_pred = I_mem, so the bound is zero. Not this result.
- **Barato & Seifert 2015** (TUR), *PRL* 114:158101, 10.1103/PhysRevLett.114.158101; **Barato, Hartich & Seifert 2014**, *NJP* 16:103024, 10.1088/1367-2630/16/10/103024: these bound entropy production by the precision of a current, or relate the sensing cost to the learning rate. Holding a static record has no current to make precise, so the TUR route does not apply as stated. I found no keep-floor statement in these, based on the abstracts and what I know of them; I did not reread the full texts this session.
- **Sandberg, Delvenne, Newton & Mitter 2014**, *PRE* 90:042119, 10.1103/PhysRevE.90.042119 (and Allerton 2014, 10.1109/ALLERTON.2014.7028503): in linear Gaussian feedback (a Kalman–Bucy demon), the implementation cost is 2kT·İ_c, an *information flow rate*. Same factor 2kT and the same Gaussian class, but a flow-rate statement about a demon. Not the stock-times-leak floor here. This is the closest Gaussian prior art I found.
- **Hatano & Sasa 2001**, 10.1103/PhysRevLett.86.3463; **Yoshimura, Kolchinsky, Dechant & Ito 2023**, *PRR* 5:013017, 10.1103/PhysRevResearch.5.013017: housekeeping/excess decomposition. As the search summary noted, an LSI does not lower-bound the *housekeeping* EP of a whole process in general. The step here bounds the leak *channel's own* EP, which is different and needs P1.
- **Novelty:** the composition (per-channel EP → projection → Gaussian LSI → I → rate–distortion) is the continuous transcription of T63's four steps. I label it ELEMENTARY given T63 and KNOWN ingredients. I did not find it stated in the sources checked; "not found" is not "new".

### 8.7 Rescore (§13 scale)

- C12b-G is done on paper. The forward items are:
  - **C12b-G review:** already scheduled. Not scored.
  - **C12b-A, attainment near onset by a corrector that does not know x**, finite horizon: p_hit 0.3, V_hit 3, p_miss 0.7, V_miss 2 → EIV 2.3. Cost ≈ 3 h → ≈ 0.77 per hour.
  - **C12b-Lean, a Lean spec of Steps 1′, 3 and 5** (finite algebra; the LSI as an axiom): with Lean ×3, ≈ 1.0. That is below C12c-L.
- **Top 3, Lean aside:** SR-b ≈ 0.87 · C1 0.83 · C4 corrected run ≈ 0.8. Then C12b-A ≈ 0.77, C12c-L / C12c-G′ / C3v2 P5² cut ≈ 0.78.
- **With Lean ×3:** C12c-L ≈ 2.35, C9 ≈ 1.2, C12b-Lean ≈ 1.0.

## 9. Post-review corrections (appended 26 Nov 2026, about 09:45 ET, after `rnd/review_c12b/HOSTILE_REVIEW_C12B.md`, PASS-WITH-FIXES; §§0–8 stand as written; where they conflict, this section governs)

### 9.1 H1: the Γ/r ordering is OPEN (an open miss in the stated form)

- **Two leak models.**
  - The **same-channel** class: the record's only relaxation is the same mechanism that couples it to the source. Examples are T59 (one LDB pair, w(E→C|x) = Γ+μ and w(C→E|x) = Γ, `FREEZE_OR_HOLD_FLOOR`:73–85) and the CORE.md:90–91 OU class (a fast shrunk spring, `INFO_PHYSICS_GENERAL.md`:7).
  - The **separate-leak** class: P1 here, and T63 class RF ("as a mechanism of its own … not modulated").
- **§0.1 rescoped.** "Γ cancels, so repair vs re-learn has no threshold" is **PIM in the same-channel class only** (two-state, LDB; T59). §0.1's "outside the two-state class the cancellation is HYP" is withdrawn. Outside the same-channel class the cancellation is **false**: see the next bullet. Whether a repair-vs-relearn threshold exists in the separate-leak class is **OPEN**.
- **The live phase in the separate-leak class (ELEMENTARY extension of §8.2).** Steps 1–3 never use "gone" (P0). The source is exogenous, so condition on its whole path. Given the path, (M, C) is a time-inhomogeneous Markov process, and Steps 1, 1′, 2 and 3 apply with p_{·|path}. Data processing gives I(path; M_t) ≥ I(X_t; M_t). Under P1–P5 with a live source, long horizon:
  Q̄ ≥ 2kTΓ·⟨I(X_t; M_t)⟩_t.
  OBSERVED (review R4): live OU source r = 0.4, v = 2, tracker with a separate leak, fixed I = 0.05. Leak EP = 0, 0.048, 0.139, 0.561 at Γ = 0, 0.2, 1, 5, always ≥ 2ΓI.
- **Consistent-world track onset (PIM as a lower bound, in the intersection of class G-keep-live and IP11's class).**
  - IP11 (`GENERAL_FORM_PHYSICS`:56–60) gives memory-bath heat ≥ kT·L ≥ kT·r(v−ε)/ε for a regular conditional, by Horowitz–Esposito. The decoder reads M only, and the error ε_M ≥ ε of the whole memory (M, C). R is decreasing, so the bound also holds at ε_M.
  - Step 4 for Gaussian X_t gives ⟨I⟩ ≥ ½ ln(v/ε). So cost ≥ f(ε) := kT·max(Γ ln(v/ε), r(v−ε)/ε) + w·ε on (0, v].
  - Both branches are convex and vanish at ε = v. Their left slopes at v are −kTΓ/v and −kT r/v. f is convex, so blind (ε = v) minimizes the lower bound iff w ≤ kT·max(r, Γ)/v.
  - Hence **w₁ ≥ kT·max(r, Γ)/v**: PIM, lower bound only, conditional on P1–P5 (live), (A), the corrected (W) of §9.3, IP11's regular-conditional premise, and τ → ∞. That it is attained is **not shown**.
  - Numerical check of the onset: `c12b_post_check.py` (1).
- **The ordering.** In one separate-leak world, the keep lower bound kTΓ/Var with Var = v never exceeds the track lower bound kT·max(r, Γ)/v. Two lower bounds cannot be ordered.
  - In one same-channel world, the gone-phase corrector must itself be a leaky carrier that biases M, so the keep floor is RF-general's for the *joint* cooperative medium. Its constant is the joint log-Sobolev constant, not Γ, and T63 §5's loophole applies.
  - Neither reading gives Γ/r. **§0.2–§0.4, §3.2's ratio bullets, §6's ratio row and §8.3's "w₂/w₁ ≥ (Γ/r)(v/Var) … ELEMENTARY from two PIM statements" are withdrawn as statements about a world.** They are true only as arithmetic on two numbers from two different classes.
  - **C12b track-vs-keep ordering: OPEN; open miss in the stated form**, in the Gaussian class as well as the binary class (§3.1).
- **What stands.** Proposition G-keep (§8.2) as a lower bound in its class. **w₂ ≥ kTΓ/Var** in class G-keep. w₁ = kT r/v in the same-channel OU class (CORE.md:90–91).

### 9.2 M1: prior art and novelty

- **Horowitz & England 2017**, *Entropy* 19:333, doi 10.3390/e19070333 (Crossref OK, `crossref_c12b_post.txt`; full text read on arXiv:1707.00367).
  - The minimum entropy production to hold a target p* by ancillary control is the EP of the uncontrolled links at p*, which equals −k_B ∂_t^eq D(p*‖p^eq). Each control edge only adds dissipation.
  - With auxiliary states they coarse-grain over the auxiliary by monotonicity of relative entropy. The bound is saturated by fast reversible control.
  - These are §8.2 Steps 1 and 1′ and the housekeeping attainment, in the discrete setting. **Credited as the source of those steps.**
- **Chen & Limmer**, "Entropy Production Bounds the Accuracy of Computation in Markov Networks", arXiv:2608.23764 (Aug 2026; no DOI claimed). Eqs. (10)–(12) combine dD/dt = −σ with the modified log-Sobolev inequality D ≤ σ/(2α₀) for reversible chains. Read this session (HTML).
- **Novelty, lowered.** Proposition G-keep is the continuous (Fokker–Planck) transcription of KNOWN steps, namely Horowitz–England's per-channel bound and projection plus the Gaussian LSI, with an information and rate–distortion tail (Step 3 ELEMENTARY, Step 4 KNOWN). It is ELEMENTARY. No novelty is claimed beyond its use in this repo.
- **Inside the repo**, T63:17 already says that holding a record of a vanished bit against a leak Γ "costs, per unit time, what tracking a world that flips at rate Γ costs". The §3.1 one-carrier scaling identity ε*_keep(w) = ε*_track(w·r/Γ) is that sentence rewritten: ELEMENTARY, credit T63:17.
- Proposed for Friday's cleanup, not done here: credit Horowitz–England in T63 §2.

### 9.3 M2: P3 applies only after the write ends

- (P3) is replaced by (P3′): MSE ≤ D at every t ∈ [t_w, τ], with t_w the end of the write. (W) stands: the horizon starts at 0 from an x-independent state, and the write heat is in Q.
- Step 5 becomes: Q/kT ≥ ∫_{t_w}^τ σ_L dt − [S(τ) − S(0)], using σ ≥ 0 on [0, t_w]. Averaging gives
  **Q̄ ≥ kTΓ·((τ − t_w)/τ)·ln(Var/D) − kT·S_range/τ.**
- The long-horizon statement and w₂ ≥ kTΓ/Var are unchanged.

### 9.4 M3: S1 is the decisive premise; headlines restated

- **Proposition G-keep (headline):** PROVED (in-model) in class G-keep, **with the leak as a separate channel (P1)**, conditional on the chosen cap (A) and (W)/(P3′). If the corrector may act through the leak's own friction and noise (S1), the floor is zero, as with T59's static bias.
- **w₂ ≥ kTΓ/Var (headline):** PIM lower bound, **separate-leak carriers (P1)**, under (A), (W)/(P3′), τ → ∞.
- **w₁ ≥ kT·max(r, Γ)/v (headline):** PIM lower bound, **separate-leak carriers (P1)** plus IP11's class, under the same premises.
- **Repair vs relearn empty (headline):** PIM, **same-channel class only** (T59).

### 9.5 Low findings

- **L1.**
  - "CORE.md:91–92" in §0.4, §1, §3.2, §6, §8.3 and `c12b_check.py` (c) reads **CORE.md:90–91**: the heat infimum is :90, the stake and blind design are :91, and :92 is the ladder.
  - §1's "Γ cancels" quote is `FREEZE_OR_HOLD_FLOOR`:19 (T59 §0, as §1 says), not CORE.md:74. CORE:74 says only "A leak cancels and does not change the floor".
  - The review's L1 said T59:19 is "§1". That is wrong: line 19 is in T59 §0.
- **L2.** §0.4's "iff Γ > r" is withdrawn. A lower bound on w₂ never gave the converse, and with §9.1 neither direction holds.
- **L3.** §8.3's "per instant: ≥ 2kTΓ·I_t + …" is not a pointwise heat-rate bound, because Ṡ_x can be negative at an instant. It holds after time-averaging with the S_range term. The convexity/Jensen conclusion is unchanged.
- **L4.** In (P5), S_range ≤ d_Z·ln(A/s_min) + ln K, with d_Z the record plus continuous-corrector dimension. (W) includes the premise that the corrector starts at entropy scale ≥ s_min per continuous coordinate.
- **L5.** `c12b_check.py` (h) is circular: it hard-codes the e^{−Γt} mean decay. It is not a test of the LSI. The LSI tests are `c12bg_check` (1) and the review's (R1)/(R2).
- **L6.** In STEPBACK §16 addendum 1, T63 RF-cap's mark is corrected from "yes" to "doubtful": its input is boundary heat flux per area, which is region geometry, not record placement. See STEPBACK §16 addendum 3.

### 9.6 Rescore (§13 scale; reviews and sunk cost not scored)

| route | prior p | V hit | V miss | EIV | cost | per hour |
|---|---|---|---|---|---|---|
| C12b-A (attainment near onset; no longer orders thresholds, §9.1) | 0.3 | 2 | 2 | 0.6 + 1.4 = 2.0 | ≈ 3 h | **≈ 0.67** |
| C12b-Lean (Steps 1′, 3, 5 finite algebra; LSI as axiom) | unchanged | | | | | ≈ 1.0 with Lean ×3 |

- **Rank (Lean aside):** SR-b ≈ 0.87 (0.80 at prior 0.2) · C1 0.83 · C4 corrected run ≈ 0.8 · C12c-L / C12c-G′ / C3v2 P5² cut ≈ 0.78 · C12b-A ≈ 0.67 · PB test ≤ 0.52.
- **With Lean ×3:** C12c-L ≈ 2.35 · C9 ≈ 1.2 · C12b-Lean ≈ 1.0.

### 9.7 Wording fixes after `rnd/review_srb/HOSTILE_REVIEW_SRB.md` §4 (appended 26 Nov 2026, about 10:40 ET; numbered 9.7 because §9.1 already exists; governs §9.1–§9.4 where they conflict)

The review found the bound **w₁ ≥ kT·max(r, Γ)/v** (§9.1) correct as a lower bound, and its label not mislabelled. Wording fixes:

- **Same quantity.** The memory is (M, C) with all its channels. G-keep's Q = kT·Ṡ_res over those channels, fuel included, is then the memory-bath heat that IP11 bounds through Horowitz–Esposito. So both branches of f bound the same Q, and their max is a lower bound on it. If some C channel drew on a reservoir outside "memory-bath", the IP11 branch would bound only part of Q. That is still a valid lower bound, but it must then be stated as such.
- **Time-varying designs.** f(ε) as written is for a constant (steady) design, and IP11 is a steady-state statement. For a design whose error changes over time, both branches are convex in ε, so by Jensen the time-averaged cost is ≥ f(⟨ε⟩_t). The onset conclusion is unchanged. This is the same point as §9.5 L3.
- **Citation.** IP11 is `GENERAL_FORM_PHYSICS`:**56–62**, not 56–60. The Horowitz–Esposito sentence is on :62.
- **Label.** w₁ ≥ kT·max(r, Γ)/v is **PIM, lower bound only, an ELEMENTARY composition** of the G-keep live extension (§9.1) with IP11. Attainment is not shown. Provenance: the live-phase extension comes from `HOSTILE_REVIEW_C12B.md` H1(c) and has been self-checked only since then.
- **`c12b_post_check.py` (1)** is relabelled **OBSERVED (arithmetic of the onset of f only)**. It is not evidence for the premises.
- **Premises, stated in full wherever the bound is quoted:** P1–P5 with a live source, (A), (W)/(P3′) as corrected in §9.3, IP11's class (exogenous equilibrium OU signal, regular conditional, steady state), and τ → ∞.
