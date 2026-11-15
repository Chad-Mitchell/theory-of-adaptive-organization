# Referee report: physics and statistics. "A Theory of Adaptive Organization" (GTAO), night-1 package

Sunday 15 Nov 2026, written 02:45–03:10 ET by an independent referee (Grok Bot executor), acting as a theoretical physicist (stat mech / complex systems) and an empirical statistician. Private. Nothing was posted, sent or committed, and no one else's files were edited. My own code and outputs are in `REVIEW/physstat/rerun/`. `CLAIM_MAP.md` and `FIXES.md` were **not** read until §1–§6 below were written. §7 compares against them afterwards.

Read: FORMAL/AXIOMS, THEOREMS, EXTENSIONS; POOLSIM; SENSING (incl. W5_CHECK); VIGIL and VIGIL/v2; arch_checks/LAYERS1*; theory-v3/PREDICTIONS.md and prereg/P1_*; tests/ANTS1 (no write-up existed, so I wrote one: `ANTS1_WRITEUP.md`).

Re-run independently from raw outputs (all at nice 19, peak RSS < 1 GB):
1. **P1 (Meeter), primary conditional logit.** I wrote my own exact-likelihood implementation (DP over elementary symmetric polynomials, analytic gradient checked against finite differences, FD Hessian). It gives **a_c = 0.321, SE 0.016, 95% CI [0.289, 0.352]**, against the locked run's 0.310 with CI "unavailable".
2. **Enron (VIGIL-2)**, from `custodian_table.csv`: reproduced exactly, plus robustness checks and power.
3. **ANTS1**, from `results.pkl`: reproduced exactly, plus a determinism check of the post-crash resume.
4. **POOLSIM W1/W2/W5/W6**: the onset slope taken directly from the raw realized episode costs and the simulator's expected costs, with no learners.

---

## 0. Verdict in one paragraph

Inside its stated model class, the mathematics is mostly correct and honestly scoped. I spot-checked T1.2–T1.3, T5.3 and T5.6 by hand. **As physics it is not a law.** The headline exponents are not universal: they are a continuous function of an unmeasured technology parameter, and the "−1" is a homogeneity identity, not a universality class. The "energy" framing does no work. **As empirical science, nothing GTAO-specific is supported.** The three real-data tests tonight came out:
- P1 recall slope: valid fail, robust to my re-fit.
- Enron vigilance: valid fail of a weak but adequately powered operationalization.
- PIAAC: a pass only on a direction that was already prior art. The one discriminating contrast vanished once correctly specified.

Every simulation "pass" is either circular (a Monte Carlo of the cost algebra) or a check of the authors' own approximation of their own simulator. I found no evidence of tampering in the locks, but every lock is self-attested and several contain dated-text inconsistencies. What survives is a coherent, well-organized **design calculus** (EOQ, team theory and rational inattention, assembled), with a few clean in-model results (T3 sign theorem, T4 bundling, T5 price invariance) awaiting any external test.

---

## 1. Severity-ranked issues

| # | Severity | Issue | Evidence | What fixes it |
|---|---|---|---|---|
| 1 | **Critical** | **No GTAO-distinctive prediction has real-data support.** All real-data tests failed or tested only prior-art direction. | P1: a_c = 0.31–0.32 vs locked band [0.5, 1.2]. Enron: RR/level 0.93 (share), 1.00 (rate). PIAAC: P1 ≈ 1.14 = Mintzberg's monitor role; P2 null when correctly specified (1.06, CI 0.98–1.16); P3 span slope 0.036 vs 0.5. | A distinctive, pre-specified test on data the theory has not seen, run by someone else (see §6). |
| 2 | **Critical** | **Simulation passes are circular.** Learners minimize the same expected cost whose boundary is the theorem, so the onset slope is fixed before any learner exists. | My re-run: the slope from the simulator's own expected-cost crossing is −0.994 (W1), −0.997 (W2), −0.976 (W5), −0.482 (W6). From raw realized means it is −0.991, −0.996, −1.003, −0.483. The sign of realized vs expected gain agrees in 99.6–100% of groups (`rerun/poolsim_rerun.out`). SENSING's "measured (a, b)" has R² = 1.000 and se = 0.0000 because it reads back the trackers' own local cost rule on a grid, not a measurement. ANTS1 P1-MEAN = Kalman K* exponent to 3 decimals. | Agents that are *not* given the cost function (RL, evolved, LLM agents, real organisms), with sensing that is not hand-specified. |
| 3 | **Critical (physics)** | **The exponents are not universal; they are a parameter family that can fit any negative number.** e_g = −(1−b)/(1−a) with (a, b) ∈ [0,1)×(0,1) covers all of (−∞, 0). Tonight's documents already use −1, −1.5, −2, −4, −(1+θ), −γ, −½, and "a ρ threshold" (T2). κ* = 1/\|e_g\| likewise. With (a, b) unmeasured in **every** real substrate (EXTENSIONS §4.5), the exponent predictions are unfalsifiable as stated. The "−1" is not a universality class in the RG sense. It is a Buckingham-Π identity: if cost depends on (W, q) only through Wq ("drift-invariant pricing", L1(ix)) and pooled stakes are Nw, then N\*q_g/q_u is the only small-ρ invariant. Any concave cost of Wq gives it. | THEOREMS L1, T1.3, T1.8, T4, T7; EXTENSIONS §2. | State the theory's real empirical content as a **scaling relation between two measured exponents** (onset exponent vs the *level's* effort elasticities), and test it where both can be measured independently. |
| 4 | **High (physics)** | **The "energy / second law" framing is decorative.** The axioms explicitly drop thermodynamics (AXIOMS: "not assumed… that thermodynamics binds above the cell"; Ax5 "one currency (heat, attention, money, compute)"). No conserved quantity, entropy production, fluctuation theorem or Landauer-type bound enters any proof. "Entropy-priced" R2 is rational-inattention pricing with a free price λ. EXTENSIONS C1 calls R2 "the thermodynamic floor" for cells without derivation. My understanding, from memory and unverified this session, is that the cellular-sensing energetics literature (Mehta & Schwab 2012; Govern & ten Wolde 2014) finds several separate resource limits (receptors, time, energy) and no single per-nat price. | AXIOMS §1, EXTENSIONS 3.1. | Either drop "energy/second law" from public language or derive a bound with physical units for one substrate (e.g. molecules of ATP per nat for a specific receptor network) and show it sets (a, b). |
| 5 | **High** | **The theory shields its distinctive regime from observation.** The small-ρ law has a prize ≤ bρ (Prop 10). POOLSIM shows it is invisible at decision noise ≳ 1% and biases slopes steeper. Add Axiom 7's escape ("a miss under weak selection is weak evidence") and the per-row mapping escape ("the mapping may be wrong"), and there is no pre-declared observation that would count against GTAO in a firm. The VIGIL-2 write-up says this itself: "the theory has so far not specified an instrument it would accept as a fair kill." | THEOREMS P10; POOLSIM §4; EXTENSIONS §3.0; VIGIL-2 verdict. | Before the next field test, publish the measurement-validity criteria (what counts as "the level", "the driver", "effort") and the selection-strength criterion, with a kill that cannot be rescued post hoc. |
| 6 | **High (provenance)** | **All locks are self-attested, and stated times in file bodies contradict the lock records.** ANTS1 body "~10:45 PM" vs commit 22:21:16. theory-v3 PREDICTIONS body "~23:55" vs commit 23:46:35. POOLSIM body "about 00:45" vs lock 00:42:14. Also: SCALEFREE derivations committed *after* the PREDICTIONS lock (23:52). POOLSIM's PREREG.sha256 sidecar rewritten at 01:16, after all outputs. VIGIL-2 code edited 6 s after the original lock (01:51:23 → code 01:51:29 → dry run → amended lock 01:51:40), with the pre-edit file not retained, so "dry-run-only edit" cannot be verified. LAYERS1 lock does not hash its code (same mtime as the lock). ANTS1 mtimes were reset by the VM restore. | §3 table. | Third-party timestamps (OSF / Zenodo / public gist) for every lock, retained pre-amendment files, a blind analyst. |
| 7 | **Medium** | **Locked estimators with errors that could have been caught.** VIGIL P2 stacked model forced common control effects. The locked "pass" (1.19) is an artifact, and the correct contrast is null (post hoc, disclosed). The P1 "CI unavailable" is a statsmodels artifact of near-separation and an unidentified direction in 800 item dummies: my FD Hessian has min eig ≈ −8e−13, max 1.8e4, and a_c's SE is well determined at 0.016. ETC + two-parameter logistic has an adoption floor bias (POOLSIM §5.2, SENSING class-R MISS). LAYERS1's lock counts P3 over "12 (b, w/h) series", but the slope is over w/h, so the series are (b, L) = 15, and the bar was rescaled after the fact. ANTS1 P1 says "12 tests" where the design gives 10. | Files cited. | Dry-run every estimator on simulated data with known truth (including floors/ceilings) before locking. |
| 8 | **Medium** | **Construct validity of the field measures is low, and the theory had not said what would be valid.** PIAAC: five-point self-report, top-coded (15–45% of leads at "every day"), no "whose driver", no meetings. Enron: *received* mail is not a sampling choice, the mail is not specific to shared drivers, assistants filter executive mail, and the rank list is coarse. Neither compares the *same driver per unit drift*, which is what T5 is about. | VIGIL PREREG §7, VIGIL-2 §6. | Diary or calendar data with outsider meetings (Bandiera et al.), or an experiment. |
| 9 | **Medium** | **Multiplicity and selective summary.** About 40 locked sub-predictions tonight across 7 tests, with count thresholds and no family-wise accounting. Conversation summaries foreground trivial passes ("ants forget faster when the world changes faster, 21 of 21" = ANTS1 P7, which holds for any filter) and omit locked fails (ANTS1 P3-MODE, P5(c), P6; LAYERS1 P2). | ANTS1_WRITEUP; LAYERS1 out. | Report every locked prediction with pass/fail in one table, and flag the by-construction ones. |
| 10 | **Medium** | **Most structure is prior art.** EOQ (Harris 1913), Kalman–Bucy/Duncan, rational inattention (Sims), team theory, Veldkamp & Wolfers 2007, Topkis 1978, Cho & Garcia-Molina 2003, and Mintzberg's monitor role are KNOWN. K\* ∝ L layers is standard exponential-sum approximation of power-law kernels (Beylkin & Monzón; Braess & Hackbusch, from memory, unverified). theory-v3/PREDICTIONS itself notes K ∝ L vs L^{2/3} "cannot be told apart over ≤ 4 decades". | THEOREMS status lines (largely candid). | A prior-art pass by a domain economist and an applied mathematician. |
| 11 | **Low** | Reproducibility on the box: the VIGIL PIAAC data folder is now empty, so the PIAAC analysis cannot be re-run here. The P1 "backup fit 0.29–0.32 entirely below the kill line" quoted to Chad is the secondary s1 fit. The primary's CI, by my re-fit, reaches 0.352 and just touches the 0.35 line, though the locked point rule still kills. | `VIGIL/data/` empty; `rerun/p1_clogit*.out`. | Keep raw data (or checksummed download scripts). |

---

## 2. Physics

### 2.1 Are the axioms physically sensible across substrates?
- **Ax1 (Brownian / stationary-increment drift, independent sources).**
  - Reasonable for prices over short horizons, and for food-patch location as a random walk.
  - Poor for many cell targets, such as ligand concentrations, which are mean-reverting. There tracking variance saturates, the power-class cost φ ∝ (Wq)^γ breaks at long intervals, and onset is set by the stationary variance, not q.
  - Independence of sources is a strong assumption for firms, where drivers are correlated.
- **Ax3 (sensing classes).** R1 "complete exact read" is impossible for cells and ants, which are Berg–Purcell/averaging limited, i.e. A_θ. It is plausible only for record lookup in firms and AI. So class R, whose −1, "2× vigilance" and Π\* = 4 dominate the narrative, applies mainly to firms and software.
- **Ax4 (component readability).** A cell reads total ligand, and a worker reads their whole situation. Neither can read "the shared part" separately. P11 shows the constant then moves (4 → ≈ 7.3) while the exponent survives (numerical only). That is honest, but it means every constant quoted (4, 2, 29%) is mapping-dependent.
- **Ax5 (one currency).** Defensible within one organism or firm. It is the right move, and it correctly disclaims cross-substrate exchange rates. But it removes the only route by which "the same law across cells, ants, firms" could mean the same numbers.
- **Ax6 (independent errors, random phases, additive costs).** Additivity is what makes the theorems exact. Real hierarchies have correlated errors: the level's estimate feeds members, as Prop 11 admits.
- **Ax7 (near-optimal selection).** This is the load-bearing empirical assumption, and Prop 10 shows the distinctive regime needs resolution ε < bρ. For ρ ~ 0.01 that means ε < 0.5% of tracking cost. That is plausible for large-population microbes and implausible for firms.
- **AI systems** are the cleanest mapping, because sensing price structure is designable and selection can be run. But there GTAO is an engineering design rule, not a law of nature.

### 2.2 Energy / second law: earned or decorative?
Decorative (§1 #4). The formal layer is careful and does not claim thermodynamics. The narrative layer, in conversation and earlier posts ("change destroys knowledge, re-buying knowledge costs energy"), does. Shannon/Duncan information rate appears only as a price unit. The one place physics could earn its keep is cells, and there A_θ and R2 give different exponents (−2 vs −1), so the "thermodynamic floor" assignment is exactly what decides the prediction. It is asserted, not derived.

### 2.3 Universality or parameter dependence?
Parameter dependence (§1 #3). What *is* robust and physically meaningful:
- (i) the **sign** results (T3: shared drift lowers N\*, private raises it, at every ρ, needing only concavity in stakes and in drift);
- (ii) **T4's** result that under bundled Gaussian errors the *loss shape* drops out at small ρ, so the level's quadratic-loss technology exponents set e_g. This is a genuine "irrelevant-variable" statement, the closest thing here to universality. It is restricted to Gaussian closure, with α-stable open;
- (iii) **T5.4 price invariance** of vigilance at onset;
- (iv) the existence of a ρ threshold under broadcast costs (T2).

These are the claims a physicist would take seriously, because they do not depend on knowing (a, b).

### 2.4 Which extensions are derived and which are hand-waving?
- **Derived inside 𝓜:** E1–E5 (extremes), E4's dissolution order, and T8's band and N² widening. The algebra is elementary and checked.
- **Derived only "given a mapping" that is itself unmeasured:** almost every substrate row (C1–C3, A1–A3, P1–P2, F1–F5, Y1, AI1–AI3). The labels say so, which is honest, but it means none of these is yet a prediction in the testable sense.
- **Hand-waving or speculative:** I2, I3, Y3, AI2 (industry), AI4, and "depth avalanches" (P7.1, numerical, not proved). F5's claim about AI and middle managers rests on "relay levels exist for pooled tracking, not authority", which is unsupported.
- **One internal tension worth flagging:** F4 says that in class R, V(N\*) ≥ 2 for *any* upkeep and price, so the field 1.15 "needs a < b, heavy attenuation or a mapping failure". That is right, and it means the field results are either a real miss for T5-in-firms or a demonstration that firms are not class R. Either way the class-R firm mapping, which carries the "CEO checks twice as often" story, is in trouble.

---

## 3. Statistics and test design: lock audit (hash and time checks I ran)

| Test | Hash re-verified | Lock time vs first outcome | Deviations / flags |
|---|---|---|---|
| POOLSIM | ✓ body (head −n −3) e8bced…; code hashes ✓ | Lock 00:42:14. W1 ran 324 s and finished 00:47:39, so it started ≈ 00:42:15 | Body says "about 00:45". PREREG.sha256 sidecar mtime 01:16 (after outputs). run_analysis.py unlocked and edited 01:04 (disclosed). **Oracle slopes known before the lock (disclosed), so not a test.** |
| SENSING | ✓ PREREG d4c032…, MEASURED_AB 71f847…, code ✓ | PREREG 01:28:27 → (a, b) 01:28:31–01:29:59 → MEASURED lock 01:29:59 → R run 01:30:16 | Sequence clean. (a, b) are a formula readback. Class R learner **MISS** under the locked rule (CI [−0.957, −0.882] excludes −1), honestly reported. |
| VIGIL (PIAAC) | ✓ PREREG 7fa31b…, analyze fb6afb… | Lock 01:40:35 → primary results 01:40:55 | Dry run with randomized outcomes before the lock (good practice). PRIOR_ART.md not hashed. Prereg says replication runs "only after primary is written up", but RESULTS.md (01:44:30) post-dates the replication output (01:42:37). **Raw data now deleted.** |
| VIGIL-2 (Enron) | ✓ amended 30fe86…/1c0e3e… (original hashes no longer match, as expected) | Lock 01:51:23; code edit 01:51:29; dry run 01:51:30; amended lock 01:51:40; real 01:51:41 | Pre-edit code not retained, so the "dry-run-only" claim is unverifiable. The dry run exposed total volume by rank, which is close to P2 under permutation (disclosed). |
| LAYERS1 | ✓ lock dd718e… | Lock 00:46:05; output 00:47:58 | Code **not hashed** (same mtime as the lock). P3 series count inconsistent in the lock and rescaled post hoc. |
| theory-v3 P1 | ✓ PREDICTIONS f7d7cf…, script 3e18ac… (git commit fb95b62, 23:46:35) | Runs from 00:55 | Body "~23:55" post-dates the commit. Derivations committed after the lock. Memory-only runner changes, with code identity checked on a 388-row slice (weak, but the estimator is standard). Dataset previously analysed marginally (disclosed). |
| ANTS1 | ✓ PREREG 38224f… (git d38ff12, 22:21:16) | Run 22:24:05; analysis code committed 22:33 (disclosed) | Body time inconsistent. Bootstrap 200 → 1000 fix (verified as the only diff). **Resume verified deterministic: 1,201/1,201 pre-crash results identical; 3/3 re-run jobs bit-identical.** |

**Summary:** no sign that any outcome was seen before a lock, and the sequences that can be checked are clean. The self-reported times are unreliable, and nothing is third-party verifiable.

---

## 4. Per-test verdicts

| Test / prediction | Verdict | Notes |
|---|---|---|
| POOLSIM W1, W2 (−1), W6 (−½), W7 (0), W8 (−½), W9, W3 (ρ threshold) | **Circular** (valid as a code and estimator check) | Expected-cost crossing reproduces each slope with no learners (§1 #2). The useful parts: the estimator separates −1, −½ and 0, and the simulator matches the algebra. |
| POOLSIM W5 (bundled absolute loss −1, not −2) | **Valid in-model computation** (not a test of nature) | Genuinely not pre-computed, independently reimplemented (W5_CHECK −0.978 / −1.001), and later proved as T4. A real theoretical finding about the model. |
| POOLSIM vigilance V ≈ 2 | **Circular** in W1/W2/W8 (stated); descriptive in W3/W5 | |
| POOLSIM findability sweep | **Valid and informative** (negative for field testability) | The most important simulation result of the night. |
| SENSING class A (−1.97 vs −2), A2 (−1.48 vs −1.5) | **Circular** | (a, b) = readback; onset = cost boundary; oracle = theorem. |
| SENSING class R | **Valid fail of the locked discoverability criterion** (not of the algebra) | Locked rival-kill did not fire. More importantly, the claim "*members'* sensing predicts onset" is superseded by T1.8 and T4: the *level's* technology sets e_g. SENSING could not separate the two, because level and members shared the technology. So "the theory's one unique prediction" as stated to Chad was mis-stated. |
| LAYERS1 P1 (K\* linear in L) | **Pass, uninformative** | R² differences 0.01–0.02 over 5 integer points. The project's own SCALEFREE note says these cannot be told apart. |
| LAYERS1 P2 (span invariance) | **Valid fail** (6/12 vs ≥ 9) | |
| LAYERS1 P3 (r\* falls with w/h) | **Pass, by construction** | More weight on accuracy forces finer spacing in any approximation problem. |
| LAYERS1 overall | **Valid partial fail; not GTAO-specific** (approximation theory) | |
| ANTS1 | See `ANTS1_WRITEUP.md`. P1-MEAN, P3-MEAN, P7 circular or trivial; P1-MODE, P2, P4, P5(a,b), P8 valid in-model passes; **P3-MODE, P5(c), P6 valid fails** | No write-up existed; written by me. |
| theory-v3 P1 (Meeter conditional slope) | **Valid fail** | Locked, real data, competitor named. My independent re-fit: 0.321 [0.289, 0.352]. The competitor C1's 0.24 is *also* excluded, so the data reject both. Construct threats (never-encoded floor; need exponent from headline words) were stated before the run, with "a kill under these threats still counts". |
| VIGIL P1 (direction) | **Valid pass of a non-distinctive (prior-art) prediction** | n ≈ 10k; any non-zero gap is "significant". |
| VIGIL P2 (specificity) | **Invalid as locked** (misspecified); correct contrast is **null** | 1.06 (0.98–1.16) primary; 1.03 replication. |
| VIGIL P3 (√span) | **Weak test; null** | Top-coding and no same-driver measure; but 0.036 vs 0.5 is far apart. |
| VIGIL P4 (≈ 2) | **Invalid test** (declared non-decisive by its own prereg) | 1.15. |
| VIGIL-2 Enron P1/P2/P3 | **Valid fail of the operationalization; low construct validity** | My re-run (`rerun/enron_rerun.out`): Poisson P1 0.932 [0.821, 1.058], P2 1.001 [0.837, 1.198] (exact reproduction). Equal-weight OLS: 0.955 and 0.968. Leave-one-out P2 range 0.96–1.08. Permutation MDE ≈ RR 1.21 per level at 80% power, against the √-law's 1.41 (k = 2) to 2.45 (k = 6). **Adequately powered; not an underpowered null.** |

---

## 5. What survives as an empirically supported claim (given P1 killed, Enron killed, OECD partial)

- **Supported by real data, but not GTAO's:** people who supervise report reading external information about 14–19% more often than comparable non-supervisors, in 9 countries and both sectors (PIAAC). This is Mintzberg's monitor role, and it is generic: supervisors also read more own-task material.
- **Supported by real data, against GTAO:**
  - Within-item, within-person news forgetting has slope ≈ 0.31–0.32, not ≈ 0.7. The "forgetting exponent = need exponent" claim is dead at the item level too.
  - In Enron email, external sampling does not rise with rank.
- **Supported only inside the model (proved, and checkable by anyone):** T1 closed form; T3 opposite signs; T4 loss-shape irrelevance under bundled Gaussian errors; T5 a ≥ b ⇒ V > 1, and price invariance; T6 lattice (given indivisible reads); T7 ordering; T8 bands; P10 resolution floor.
- **Empirically supported GTAO-specific claims: none.** The theory is at the stage of "internally consistent, externally untested where distinctive, and failed where tested".

---

## 6. What would make each claim credible to a skeptical physicist

| Claim | Minimum credible evidence |
|---|---|
| Onset scaling relation e_g = −(1−b_L)/(1−a_L) | One substrate where the **level's** effort elasticities (a_L, b_L) are measured on the level itself, and the onset group size is measured under an *experimentally manipulated* shared share ρ spanning ≥ 1.5 decades in a regime with prize ≫ decision noise. Run by agents not given the cost function. Candidates: evolved or RL multi-agent systems with sensing costs implemented physically (compute or tokens) rather than as a formula; microbial public-goods sensing; ant colonies with manipulated patch persistence. The prediction should be locked by a third party. |
| T3 opposite signs | The cleanest distinctive bet. A factorial experiment varying shared and private volatility independently (lab teams, agent systems, colonies) and predicting opposite signs on centralization of tracking. Rival contingency theory predicts the same sign. |
| T5 vigilance (V ≥ 2 in class R; ∝ N^a beyond onset; price invariance) | Same-driver, all-channel sampling rates for leads vs members (diary or calendar data), with drift per driver measured. Pre-declare that a ratio < 1.5 on such data kills the class-R firm mapping. Test price invariance by exploiting variation in the lead's monitoring cost. |
| T4 (loss shape irrelevant) | Already credible as mathematics. Physically interesting if shown in a system with measurably non-quadratic loss. |
| T8 / E4 (lookup dissolves levels before private holding, whole-item case) | A natural experiment: firms adopting retrieval tools, with roles coded *before* outcomes. The authors' own falsifier in F5 is fine; it needs an external coder. |
| "Energy / second law" | Derive one bound in physical units for one biological sensing system, and show it fixes the class. Otherwise remove the language. |
| Cross-substrate "law" | The same *relation* (not the same numbers) confirmed in at least two substrates with independently measured classes. Until then, call it a design calculus. |
| Process | Third-party timestamps; retained pre-amendment files; an estimator dry-run on synthetic truth before every lock; one master table of every locked prediction with by-construction ones flagged; an independent analyst for real-data tests. |

---

## 7. Comparison with CLAIM_MAP.md and FIXES.md (read only after §1–§6 were written)

Read at about 03:05 ET. Both files are candid, and on most points they agree with this report: POOLSIM is labelled CIRCULAR, DP1 is killed, the size miss in T5 is called a miss, and the X1 identity is "withdrawn". Points where the map is **stale, incomplete, or where I disagree**:

1. **T5 row: the field status is stale.** It cites only PIAAC ("direction PASSED"). The Enron test (01:51 ET) fired KILL-1 on direction (0.93 per level), so field direction is **mixed**, not passed. Status should read "OPEN, field tests: PIAAC generic direction only; Enron direction killed; size and growth missed".
2. **SENSING has no row.** This is the claim that was presented to Chad as possibly "uniquely the theory's own" (members' sensing predicts group exponent). It should appear as: class A and A2 **CIRCULAR** pass; class R **MISS** under the locked rule. As a claim about *members* it is superseded by T1.8 (the *level's* class sets e_g; members' b sets only e_u). There is also an internal tension. EXTENSIONS §2 and FIXES F22(iii) prescribe measuring the class from **lone-unit** effort elasticities. That identifies the *members'* class, which equals the level's only under a common technology, the very assumption F12 says was hidden.
3. **N1 (ANTS1): incomplete.** It lists the P3-MODE failure but not the **P5(c) (36/96) and P6 (154/180) failures**. It does not flag that P1-MEAN and P3-MEAN are by construction (Kalman). The P1 "10/10" should carry that qualifier. The full scoring is now in `ANTS1_WRITEUP.md`.
4. **N6 (P1): "CI unavailable" can be resolved.** My independent conditional-logit fit gives 0.321 [0.289, 0.352]. Still KILLED on the locked point rule. Add that the named competitor C1 (0.24) is **also excluded**, so "closer to the rival" should not be read as support for the rival.
5. **N4 (LAYERS1):** fine as stated, but add that the code was not hashed, that the P3 series count was rescaled, and that P3 passes by construction.
6. **The CLAIM_MAP has no provenance column.** Every PASSED/KILLED here rests on self-attested locks with inconsistent in-text times (§3). A skeptical reader needs that stated on the map itself.
7. **FIXES §C "checked hard and found correct".** I independently re-derived T1.2/T1.3 and T5.3/T5.6 (x = √(Nρ), x²/2 − √r·x − h′ = 0, V = x/√r) and agree. I did not re-check T6, T7 or T8. FIXES' own limit statement stands: the adversarial pass was by the same executor and is not an independent review. This report is independent only for the statistics, the simulations and the physics framing, not a line-by-line proof audit (the math referee covers that).

Files from this review: `REPORT.md`, `ANTS1_WRITEUP.md`, `rerun/{ants_rerun,ants_determinism,enron_rerun,poolsim_rerun,p1_load,p1_clogit,p1_clogit_newton}.py` and their `.out` / `.json` outputs.
