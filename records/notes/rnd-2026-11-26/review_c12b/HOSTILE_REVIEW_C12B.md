# Hostile review: C12B_ORDER.md (§§0–8, §8 governs) and STEPBACK.md §16 (both addenda)

*26 Nov 2026, about 09:30 ET. Independent reviewer; local note only (no commit, no push, no email). Repo text read at fork branch `forge-rnd-record-cost-2` head `ac92ee2` (confirmed with `git ls-remote` against the fork; local clone `/workspace/lemmar-check` is at the same commit). Labels as in the target: PIM = proved in-model, KNOWN, ELEMENTARY, HYP, OBSERVED. Reviewer numerics: `review_c12b_check.py` → `review_c12b_check.out` (written fresh; it reuses no code from the target). DOIs re-resolved: `crossref_review.txt`.*

## Overall: PASS-WITH-FIXES

- **Proposition G-keep (§8.2), Steps 1–5: the math holds in its class.** Constants, the OU generator normalization and the Cauchy–Schwarz projection all check out, analytically and numerically. One premise clash (M2) needs a one-line fix.
- **The headline that C12b is non-empty, "w₂/w₁ ≥ Γ/r, keeping switches on after tracking iff Γ > r", does not hold as a statement about one world.** It combines a track threshold from a class with no separate leak with a keep threshold from a class where the leak must be a separate channel (H1). With the fix, the C12b ordering becomes an **open miss** in the Gaussian class too (it already was in the binary class). The proposition survives; the ordering does not.
- The repair-vs-relearn emptiness (§0.1) holds only in T59's same-channel class. In the class where §8 proves its floor, the leak does not cancel (H1, part b).
- The closest prior art for Steps 1–1′ is missing: Horowitz & England 2017 (M1).

## HIGH

**H1. The ratio w₂/w₁ is formed across two incompatible leak models, so "ordering by Γ/r" is not established in any one world W.**
- (a) **Where w₁ comes from.** CORE.md:90–91 (§4 worked class) and its source `theory/INFO_PHYSICS_GENERAL.md:7` take the memory to be a fast shrunk spring coupled to the present signal. There is no separate passive leak: the record's only relaxation is its coupling to X. That is the same-channel case. T59's Γ-cancellation (`FREEZE_OR_HOLD_FLOOR`:19, :73–85) is also same-channel: copy and leak are one LDB pair, w(E→C|x) = Γ+μ and w(C→E|x) = Γ.
- (b) **Where w₂ comes from.** §8 P1 *requires* the leak to be "a mechanism of its own", with forces independent of c and x, as T63 does ("acts through its own mechanisms and leaves the carriers' energies and leak rates alone", RECORD_REPAIR_FLOOR:17, :57). The note itself says (§8.5 S1) that the same-channel case is out of class and gives zero ongoing heat.
- (c) **Steps 1–3 do not use "gone"** (P0 says so). Apply them to the *live* phase in the P1 class: condition on the source path, and the leak channel's EP is ≥ 2Γ·E D(p_{M|path}‖π) ≥ 2Γ·I(X_t;M_t). So a tracker in a P1-type carrier pays at least 2kTΓ·I on top of the learning-rate floor. Near onset that is ≈ 2kT·r·I, since r(v−ε)/ε ≈ 2rI. In a consistent P1 world, therefore, the track onset is at least kT·max(r, Γ)/v, a lower bound and not shown to be attained. The keep onset's lower bound kTΓ/v never exceeds it. Two lower bounds cannot be ordered, so "keep switches on after track iff Γ > r" does not follow. OBSERVED (R4): live OU source, r = 0.4, v = 2, tracker with a separate leak, at fixed I(X_t;M_t) = 0.05. Leak EP = 0, 0.048, 0.139, 0.561 at Γ = 0, 0.2, 1, 5, always ≥ 2ΓI. The leak does not cancel.
- (d) **The other consistent reading.** Read both phases same-channel: the live source may bias the carrier, and in the gone phase the corrector C may bias M but must itself be a leaky carrier. Then the keep floor is RF-general's for the *joint* cooperative medium. Its constant is the joint log-Sobolev constant, not Γ, and T63 §5's cooperative loophole applies. Again there is no Γ/r.
- (e) **Consequences.**
  - The §0.4 / §6 / §8.3 statement "w₂/w₁ ≥ (Γ/r)(v/Var) is an ELEMENTARY composition of two PIM statements" is arithmetically true of two numbers from two classes, but it says nothing about one world. Relabel it: the ordering is **OPEN; open miss in the stated form**.
  - The §0.1 emptiness should read: "PIM in T59's same-channel class (two-state, LDB). In a separate-leak (P1/T63) class, Γ does not cancel (by §8 Steps 1–3 with a live source), and whether a repair-vs-relearn threshold exists there is OPEN."
  - The §0.1 sentence "Outside the two-state class, the cancellation is HYP" is too generous. Outside the same-channel class the cancellation is false.
  - STEPBACK §16 addendum 1 ("so w₂/w₁ ≥ Γ/r at equal variance") and the §16 addendum 2 rank need the same append-only correction.
  - **Rescore:** C12b-A (attainment near onset, 0.77/h) is valued as making w₂ exact so that the ordering bites. With the ordering gone, its V_hit should drop (about 2 rather than 3, giving ≈ 0.67/h). C12b-Lean (the finite algebra of Steps 1′, 3, 5) is unaffected.

## MED

**M1. Prior art missed: Horowitz & England 2017**, *Entropy* 19:333, doi 10.3390/e19070333 (Crossref OK). Full text read on arXiv (1707.00367).
- They prove that maintaining a target distribution p* by ancillary control costs at least the EP of the *uncontrolled* links at p*. That equals −k_B ∂_t^eq D(p*‖p^eq). Each control edge only adds dissipation, and the bound is saturated by fast reversible control. With auxiliary states, they coarse-grain over the auxiliary using monotonicity of relative entropy.
- That is Step 1 (per-channel split, leak part kept) plus Step 1′ (projecting out the corrector) plus the attainment construction, in the discrete setting. Composing it with a (modified) log-Sobolev inequality to get "maintenance EP ≥ 2α·D" is also in print: Chen & Limmer, arXiv:2608.23764 (Aug 2026), eqs. (10)–(12), read this session; it has no DOI, so it is cited by arXiv number only.
- Neither T63 nor C12B cites Horowitz–England. A repo search finds it nowhere; only Gingrich–Horowitz–Perunov–England 2016 is cited.
- Fix: credit it in §8.6 as the source of Steps 1–1′ and of the housekeeping attainment. Lower the novelty of G-keep to "continuous transcription of KNOWN steps plus an I and rate–distortion tail". The same credit should be proposed for T63 in Friday's cleanup; this review does not edit T63.

**M2. (W) contradicts (P3).** (W) starts the horizon before the write, from an x-independent state. That forces I(X;M_0) = 0 and MSE = Var > D at t = 0, but P3 demands MSE ≤ D at *every* t ∈ [0, τ]. Fix: impose P3 on [t_w, τ], with t_w the end of the write, and integrate Step 4 over [t_w, τ]. Step 1's EP ≥ 0 on [0, t_w] keeps the bound valid. The result becomes Q̄ ≥ kTΓ·((τ−t_w)/τ)·ln(Var/D) − kT·S_range/τ, and the long-horizon statement is unchanged.

**M3. S1 is the result's decisive premise and must sit in every headline that quotes the floor.**
- The inequality itself is near-structural: if the leak is its own channel, its EP alone bounds the heat, and the Gaussian LSI turns that into 2Γ·D.
- All the physics is in P1's ban on the corrector acting through the leak's own friction and noise. That is the textbook single-friction Langevin picture, in which a conservative interaction V(m − c) acts on M. S1 discloses this and labels it a modeling choice, which is honest. But §8's status line and §8.3's "w₂ ≥ kTΓ/Var: PROVED (in-model)" omit it.
- Add "with the leak as a separate channel (P1)" wherever the floor or w₂ is quoted. P0–P5 are not hiding the result, but P1 *is* the result.

## LOW

- **L1. Line references.** The OU heat infimum kT·a(v−ε)/ε is CORE.md:**90**, the stake kT·a/v and the blind design are CORE.md:**91**, and CORE.md:92 is the geometric ladder. "CORE.md:91–92" in §0.4, §1, §3.2, §6, §8.3 and `c12b_check.py` (c) should read :90–91. The "Γ cancels" quote in §1 is T59 line 19 (§1), not CORE.md:74. CORE:74 says only "A leak cancels and does not change the floor."
- **L2. "iff".** §0.4's "iff Γ > r" was never supported, even before H1: a lower bound on w₂ gives at most the "if" direction. §8.3 lists "whether w₂ < w₁ when Γ < r" as open, so §8 governs. Add an explicit correction line anyway.
- **L3. "Per instant".** §8.3 "per instant: ≥ 2kTΓ·I_t + …" is not a pointwise heat-rate bound, because the Ṡ_x term can be negative at an instant. It holds after time-averaging with the S_range boundary term. The convexity/Jensen conclusion is unaffected.
- **L4. Dimension.** In (P5), "S_range ≤ d ln(A/s) + ln K" should use d_Z (record plus continuous corrector dimensions) and s_min, with the corrector's initial entropy at scale ≥ s stated as part of (W).
- **L5. Check (h) is circular.** `c12b_check.py` (h) hard-codes the OU mean decay e^{−Γt} in D(t) and so returns 2Γ by construction. It does not test the LSI. The `c12bg_check` (1) and the reviewer's (R1)/(R2) do.
- **L6. Pattern tally.** Under the rule as written ("names the position, arrangement or timing of *records*"), T63 RF-cap's input is a boundary heat flux per unit area. That is region geometry, not record placement, so "doubtful" is the honest mark, not "yes". The independent PB cluster is then 1–2 items, not 2–3. This strengthens the §16 conclusion that PB is not a common cause. The rule does precede the table in the text. The single-reader caveat is stated and stands. With H1, C12b's own obstruction is a channel-modeling input chosen by hand (S1), not placement, so "C12b: no" stays.

## What was checked and holds

1. **Repair vs relearn (§0.1).** T59:19 and :73–85 read directly. In the same-channel LDB class, I_alt = r·L(ε) and the Γ terms cancel (PIM there). The scope problem is H1(b) and (e).
2. **Step 1.** For a separate overdamped channel with force −kT·m_i/s_i² and diffusion D_i, the current is j = −D_i·p·∂ ln(p/π) and σ_L = D_i ∫ p(∂ ln(p/π))². This is correct, and Σσ_k ≥ σ_L holds channel by channel (cf. Horowitz–England's edge-by-edge positivity).
3. **Step 1′.** The identity p·(∂ ln(p/π))² = (π∂(p/π))²/p is correct, and ∫a²/b ≥ (∫a)²/∫b at fixed m needs π independent of c (P1). Correct.
4. **Step 2.** From Gross's Ent_π(f²) ≤ 2s²∫|∇f|²dπ with f² = q/π: ∫|∇f|²dπ = ¼·I(q‖π), so D ≤ (s²/2)·I(q‖π). Tensorization over diagonal π holds. With D_i = Γ_i s_i², σ_L ≥ 2Γ·D, with equality for shifted π (D = μ²/2s², I = μ²/s⁴).
   - OBSERVED (R1): direct Fokker–Planck evolution under the leak alone, four non-Gaussian starts, two (s², D) pairs. −dD/dt matches D·Fisher to ≤ 0.6% (finite-difference window), and −dD/dt ÷ (2ΓD) ranges from 1.026 to 2.93, always ≥ 1. This confirms Γ = D/s² as the relaxation rate and the 2Γ constant.
   - OBSERVED (R2): over 400 polynomially tilted (non-mixture) densities, the minimum of (s²/2)·Fisher/D is 1.00107.
5. **Step 3.** E_x D(p_{M|x}‖π) = I + D(p_M‖π). Correct.
6. **Step 4.** D(R) = Var·e^{−2R} (nats) plus data processing. Correct; the Shannon-lower-bound remark is correct.
7. **Step 5 and (P5).** The bracket is bounded by S_range. Under (A), the max-entropy and Jensen bound and the ln K term are correct. The sub-exponential remark is correct. (A) is correctly labeled CHOSEN. (W) is correctly a premise, but see M2.
8. **The §8.4 correction of F-v is right.** A large-amplitude record decays slowly passively, but holding it costs σ_L ≥ 2Γ·D ≥ 2Γ·I whatever the amplitude.
9. **Two-channel heat (analytic 1.5).** p_{M|x} = N(ax, s²) with a = κ/(Γ+κ) when s_C = s. The leak current is −Γ·μ·p, so σ_L = Γa²Var/s² = 1.125. The corrector current is κ(1−a)x·p, so σ_C = κ(1−a)²Var/s² = 0.375. Total 1.5000.
   - OBSERVED (R3): Gauss–Hermite quadrature of the per-channel EP gives 1.500000. Two further parameter sets match the analytic formula to 10⁻⁶. An Itô-form Euler heat simulation (dt = 10⁻³) gives 1.511 ± 0.015.
   - σ_L/(2ΓI) = u/ln(1+u) is confirmed: 1.4925 at u = 1.125.
10. **Scripts.** Both target scripts were rerun. `c12b_check.out` and `c12bg_check.out` reproduce byte-identically.
11. **CT4** (THEORY.md:88 row, :279) and the reading w₁ = κ/(2 ln2·a²·Var): correct. **T62** AL-stock-free and **T63** RF/RF-general/RF-forget: quoted faithfully.
12. **Prior art and DOIs.** All 16 DOIs cited in C12B §5 and §8.6, plus Chiuchiù et al. 2018 (17 in all), re-resolved on Crossref with titles and authors matching (`crossref_review.txt`; two needed a retry after a 429).
    - Sandberg et al. 2014 checked in the published text: Eq. (46), W_impl = 2kT·İ_c. The target's description is accurate.
    - Horowitz–Esposito 2014, Barato–Seifert 2015 and Barato–Hartich–Seifert 2014 were checked at the abstract level only. The target's descriptions are consistent with them, and none states a stock-times-leak keep floor.
    - Gaussian IB (Chechik et al. 2005) and reverse water-filling order onsets by eigenvalue or variance, not by rate.
    - **Γ/r inside the repo.** T63:17 already says, for one carrier, that "holding a record of a vanished bit against a leak Γ costs, per unit time, what tracking a world that flips at rate Γ costs". The binary scaling identity ε*_keep(w) = ε*_track(w·r/Γ) is that sentence rewritten and should credit T63:17.
    - I found no outside source ordering keep against track by Γ/r. Given H1, there is no established ordering to claim.
13. **Placement-test scores (§16 addendum 2).** The arithmetic is correct (1.4/4 h = 0.35; 2.6/5 h = 0.52). The V-values are on the same scale as the other rows. Version 1's "close to built in" diagnosis is right.

## Not reviewed

Theorem O and the Lemma A(b′) scope bullets (§0.5) were not reviewed beyond reading them. S3 (non-convex leaks) and S4 (underdamped) were taken as stated.
