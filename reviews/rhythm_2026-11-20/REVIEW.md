# Independent hostile review: GTAO rhythm / IMP-N60 test

**Reviewer:** independent (wrote none of the test, code, prereg, results, or KEYSTONE_NOTE §5).
**Date:** 2026-11-20, started 20:52 ET, finished 21:20 ET (America/New_York).
**Targets:** `/workspace/gtao-core/core/keystone_checks/` — `RHYTHM_PREREG.md`, `DEVIATIONS_2026-11-20.md`, `resonant_layers.py`, `run_rhythm_im.py`, `rhythm_im_run.json` / `.log`, `RHYTHM_RESULTS.md`, and `../KEYSTONE_NOTE.md` §5.
**Constraints honored:** no push/merge; `/workspace/looper` not touched; compute at nice 19; small reruns only (Kalman–Bucy, Lyapunov replays, bounded-Ω probes). No inclusion rule was invented or patched.

**Verdict: SCORING CORRECT**

Every preregistered headline number in `RHYTHM_RESULTS.md` independently recomputes from the stored designs and the locked predictions. The official fail/pass gates stand. Two labels in the writeup are wrong (see Q2 and §6), and the official SANITY MSEs on collapsed-Ω rows are unreproducible under the D3 guards later adopted, but those points do not flip any gate. IMP-N60 is not rescued.

---

## Integrity

- `RHYTHM_PREREG.md` SHA-256 `e0b4f2b6f31743fdffe05f0f3eeedfb3d169824136a5671bfdce28ee11fd50ce` (mtime 18:17:20 ET). Unchanged after lock. Matches results, deviations, predictions file, and KEYSTONE_NOTE §5.
- `imp_n60_predictions.json` SHA-256 `b625a8ad57c3d861d5f0202b36125c4fa405b34260b9c46fdf72a9279d135bb3` (mtime 18:22:45 ET). Official start 18:22:50 ET. The file’s locked note says poles, variances, N, R only; a re-application of `imp_n60()` agrees with every Part A cell (189/189) and a 3-point-per-world S5 sample (360/360).
- Deviations D1–D4 are dated during the run, before official scoring. D5 is explicitly post-data and discloses runner scoring bugs rather than changing the rule. Official Model-S numbers are an independent rescore, as claimed.
- D5a is exact: the runner prepended `E0` onto `s5_rerun.json`’s `E`, which already stored K=0..J. That produces 5 entries for a 3-mode world, `J(1)=J(0)+1`, runner IMP-N60 7,067/19,320, and 710 alleged holes. Independent rescore of the correct `E[k]` is 5,890/19,320 and 379 holes.
- D5b is exact: seed 5’s “extended” miss was seed 52’s design (`s5_52::nr1_nf0`, E≈0.0445) scored against seed 5 (E_∞=1.1615). Per-seed scoring: 0/108 cells in which a resonator changes argmin; 0 cases in which a resonator beats first-order E at the same cost.
- Official Part A: 122/122 planned compositions, 0 with E < E_∞ − 10^{-9}, 0 missing tags. Unsecured pre-D3 files were not scored.
- D1–D3 changed inversion, Hurwitz/parameter guards, and optimizer budget, not the inclusion rule, costs, worlds, or thresholds.

---

## Q1. Was IMP-N60 correctly specified? Counting error vs failed internal-model idea

**The prereg’s rule is not a generalization of N60. It is a different rule, and that is why it fails Model S. The internal-model library idea is not what the Model S 30.5% diagnoses. This is not a license to rewrite IMP-N60 after the data.**

N60 (merged, Model S) walks *joint* optimized decrements of ε_K:

    K* = 1 + #{k≥2: R(ε_{k−1} − ε_k) > 1}
    (from 0: count every joint increment that pays, including the 0→1 step).

IMP-N60 (prereg §2) uses *isolated* causal value and includes modes independently:

    V_m = (σ_m² − E_∞^{(m)}) / E_∞
    include m iff R V_m > c_m,    C* = Σ c_m.

The prereg calls this “the generalization of N60.” It is not. Even with every c_m = 1, isolated V_m is not the joint increment, and independent inclusion is not a walk along the joint curve. On seed 0 the contrast is already fatal:

- isolated V = (0.368, 0.055, 0.205)
- joint decrements = (0.645, 0.0455, 0.00091)

Isolated ranking disagrees with joint ranking on 105/120 S5 worlds. The largest isolated reduction is typically ~0.75 of the first joint decrement (median; range 0.38–0.99), because the first store filters the *sum*, not one mode. Late isolated values overstate the last joint decrement by orders of magnitude (seed 0: 0.189 vs 0.00084). Sum of isolated reductions is close to total reduction (median ratio 0.99), so the mass is there, but it is mis-allocated across modes.

Independent S5 rescore, 120 worlds × 161 R, E already stored as K=0..J:

| Rule | Match |
|---|---|
| IMP-N60 | **5,890 / 19,320 = 30.4865%** (results: 30.5%) |
| N60-from-0 | **19,320 / 19,320** |
| N60-as-written | **18,941 / 19,320** (379 misses = the known K*=0 hole, 39 worlds) |

IMP-N60 predicts C*=0 in all 379 true holes (success, as required) but also in 160 cells where argmin ≥ 1, and *over-includes* in 13,264 cells. The failure mode is structural over-inclusion of late isolated modes, plus a smaller under-inclusion of the first joint step. Resonators do not enter: on the 12-seed extended subset, 0/108 cells change argmin, 0 resonator E beats first-order E at the same C.

So the 30.5% is a **counting/value-specification error**: substituting isolated V_m for joint decrements, already wrong in the class where N60 is numerically exact and kind-matching is irrelevant. It is not evidence that “internal models are wrong.”

On rhythm worlds the same bad count fails again, and a second, distinct kind-assignment issue appears (see Q2–Q3). Kind-matching as a *library* fact has real support for lightly damped cycles (one resonant layer reaches E_∞ to ~10^{-7} and matches Kalman observer poles; the MUST hybrid beats first-order-only J=8.10 with J=6.25). That does not make IMP-N60 a passed or “almost right” rule. The rule as written fails PRIMARY (58/189, of which only 51 recover the predicted composition; 7 are cost-only coincidences, as the results disclosed), MUST, SANITY, and the Model S regression. Results correctly leave a predictive rhythm rule **OPEN** and register no new candidate. Agreed. Do not “fix” V_m post hoc.

---

## Q2. Resonant-layer optimizer: is Ω→0 a solver failure?

**On `1osc_z1.0_N0.04`, collapse is the true optimum inside the conjugate-pair family, and a miss of the true Kalman filter, which has two real poles. It is not a solver failure that missed a better Ω≈1 design. The writeup’s reason is wrong: the process is not critically damped.**

`osc_world` places poles at −ζω ± iω, *not* at −ζω_n ± i ω_n√(1−ζ²). At the label ζ=1, ω=1 the process poles are −1±i, standard damping ratio **1/√2 ≈ 0.707**, still a damped cycle. Results §2, §6, and KEYSTONE_NOTE §5 are incorrect in calling this “critically damped, not a cycle.”

Kalman–Bucy on the official world (signal variance C P Cᵀ; Riccati residual ~10^{-15}):

| World | Kalman poles | Kalman ε | Official resonator | Official ε | Two real stores ε |
|---|---|---|---|---|---|
| `1osc_z1.0_N0.04` | **real** −6.92, −1.47 | 1.95×10^{-7} | Ω=1.1×10^{-5}, β=4.77 | 1.086×10^{-3} (FAIL) | 1.95×10^{-7} |
| `1osc_z1.0_N0.2` | **real** −2.45, −2.00 | 2.84×10^{-7} | Ω=1.7×10^{-5}, β=2.23 | 8.51×10^{-7} (PASS) | 2.84×10^{-7} |
| `1osc_z0.25_N0.04` | **real** −3.00, −1.26 | 1.87×10^{-7} | Ω=3.0×10^{-5}, β=2.09 | 9.69×10^{-4} (barely PASS) | 1.87×10^{-7} |
| `1osc_z0.25_N0.2` | **complex** −1.063±0.904i | 2.08×10^{-7} | **locks those Kalman poles** | 2.08×10^{-7} | 9.3×10^{-3} (worse) |
| `1osc_z0.08_N0.04` | complex −1.275±0.787i | 1.79×10^{-7} | locks Kalman poles | 1.79×10^{-7} | — |
| `1osc_z0.02_N0.04` | complex −0.676±0.978i | 1.40×10^{-7} | locks Kalman poles | 1.40×10^{-7} | — |

When Kalman poles are complex, the official resonator locks to the *observer* poles, not the process poles (matched-process-pole ε is O(1)–O(10), as the prereg allowed for diagnosis). When Kalman poles are real and split, a conjugate-pair block −β±iΩ cannot realize two different real rates. Ω→0 is the family trying, and failing, to become a two-real-pole filter. A bounded-Ω probe (floor 0.2 and 0.5; not a scored SANITY rerun) stays at ε≈1.09×10^{-3}–1.14×10^{-3} on `1osc_z1.0_N0.04`, the same side of the gate as the official fail. One first-order store is *not* on E_∞ (ε=6.57×10^{-3} at N=0.04, 8.13×10^{-3} at N=0.2). Two first-order stores *are* on E_∞, and they match Kalman exactly. Results/KEYSTONE overstate “one real store already sits on E_∞.”

**D3 wrinkle.** Replaying official collapsed designs with the current `lyapunov_mse` (D3: cond(Pzz)>10^{10} → ∞) returns ∞: cond ≈ 1.4×10^{12}, 8.1×10^{10}, 2.9×10^{10} on the three collapsed SANITY rows. Official SANITY was frozen from the post-D1 / pre-D3 pass (D3: “official SANITY is kept”). Those stored E values are therefore unsecured under the guards later adopted. The FAIL on `1osc_z1.0_N0.04` is robust (bounded-Ω, better-conditioned, still misses the gate). The barely-PASS on `1osc_z0.25_N0.04` is not secure: a Ω≥0.2 probe is at ε=1.07×10^{-3}, which would fail. The kill (need 8/8) still stands, and if anything would be harsher.

---

## Q3. MUST hybrid: 1 resonator + 1 first-order store, verified

Verified. At `seed2_two_light`, R=3:

- Predicted: C*=4, two resonators (both isolated RV are 24 and 27, both ≫ 2).
- Argmin: `nr1_nf1`, C*=3, E=0.04102221379904658, J=6.248613694671359. Lyapunov replay matches to all stored digits; cond(Pzz)≈23 (clean). Resonator (β,Ω)=(0.254, 0.772) near the fast world frequency 0.825; first-order rate b=0.632.
- Two resonators: E=0.037956, J=7.006, lose. One of those two Ω collapses to 5×10^{-6}; this is not two internal clocks.
- `nr1_nf2` (C=4): E=0.037882820113 (E_∞ to 5×10^{-11}), J=7.000000166. Parameters (β,Ω)=(0.330, 0.808), first-order rates 0.0606 and 0.264.
- First-order-only K=3: E=0.05183, J=7.105, worse than the hybrid. Kind-matching helps; the isolated count still over-includes.

**Mechanism.** The 4-state Kalman–Bucy filter of this world has poles

    −0.330 ± 0.808 i,    −0.264,    −0.061

(ε=5.5×10^{-8}; residual 10^{-15}). That is *one oscillatory observer* (fast rhythm, Kalman-shifted) plus *two real observer poles*. Official `nr1_nf2` is exactly those poles and attains E_∞. Matched *process* poles as two resonators are terrible (E=0.345, ε=8.11). The slow process rhythm (ω≈0.055) is a cycle in the world, but the optimal filter tracks it with real poles, not a clock.

At R=3 the full Kalman design costs 4 and has J=7.00. The C=3 hybrid leaves a little error (E=0.04102 vs 0.03788); the J-value of that last decrement is only R ΔE/E_∞ ≈ 0.24 < 1, so the fourth state does not pay. IMP-N60 cannot see this: it charges two cost-2 process rhythms and never looks at observer kind or joint increments.

---

## Q4. Holographic / fractal: “one store takes almost all of the value,” K*=J fails 3/24

Scoring is correct. Independent rescore: **3/24** primary cells at R=100 and 300 have K*=J=1+log₁₀Γ (only the three Γ=10, J=2 worlds at R=300). All four primary α=1 CVs are 0.9955, 1.4045, 1.7186, 1.9841, all fail the 0.5 gate. N60-from-0 matches argmin in **90/90**. All 15 worlds are convex on K=0..J at the stated 10^{-4} tolerance. Construction matches `stores.scalefree_world` (merged): τ log-spaced in [1,Γ], v∝τ^{α−1}, total variance 1, J=1+per_decade·log₁₀Γ, N=0.05. E₀=1 in every row; E_J meets E_∞ to ~10^{-7} or better. CV and per-R argmins recompute with 0 discrepancies.

**Why one store takes almost all of the value.** Not a mis-construction of the spectrum recipe, and not primarily a “wrong R typo.” The first decrement is 99.36–99.93% of (E₀−E_J) on every primary world. E₁−E_∞ is 6×10^{-4} to 5.6×10^{-3}. The last layer therefore pays only at R ≳ 1/Δε_last, which is ~110–274 for Γ=10 (hence the three hits at R=300) and **10³ to 6×10⁵** for Γ≥100 (extra `per_decade=2` arm: up to 10⁸). R∈{100,300} was preregistered; the fail is honest. Equal-value (CV) is an R-independent fail of the ε curve, so this is not only a stakes artifact.

It *is* an artifact of the *problem class*: Kalman filtering of a low-dimensional scalar OU-sum in white noise, with N=0.05 already large enough that one well-placed store sits near the causal floor. MERA / holography (Vidal 2007, Swingle 2012, Mehta & Schwab 2014) is about a stack of coarse-grainings of a many-site or high-dimensional state. That picture was not given a fair arena here. per_decade=1 is also a very sparse “fractal” (2–5 modes).

**Implies:** in this preregistered Model-S construction, layers do not grow as log(Γ) at the stated R, and value is not equal per layer. N60 still equals argmin. The log-span / equal-value claim, as written, fails.

**Does not imply:** the fractal strand is refuted in general, or that scale structure never sets K* in a spatial or high-dimensional model, or at much smaller N / much larger R. That would be a new test, not a rescue of this one.

---

## Q5. Cymatics scoring, and is the CT41 mapping fair?

**Locking and jumps scoring is correct.**

- Light set (every ζ≤0.08) is the correct 7 worlds; no label mismatches. Median of world-medians **0.03985901894048349**, exact match to the stored figure, **< 0.05**, PASS on the single aggregate statistic as written. 3/7 worlds exceed 0.05 (`1osc_z0.08_N0.04` 0.213; `2osc_sep15_light_light` 0.236, slow mode 46% off; `2osc_close2_light_light` 0.094). All 21 locking tables recompute from stored (β,Ω) and world ω. Results disclosed the 3/7. The aggregate gate is weak — a single very-light world can carry the median — but that is how the prereg was written, and it was scored that way.
- Stakes sweep (41 log-spaced R, 0.25→200): C*, composition piecewise constant, **two isolated jumps**, no chatter. Brackets R∈(1.571, 1.857): (C,n_res,n_first)=(1,0,1)→(3,1,1); R∈(5.983, 7.071): (3,1,1)→(4,2,0). Exact match to the stored jumps. IMP-N60 predicted C*=4 at every point and matches only after the second jump (21/41).
- Frequency sweep (31 points, ω₂ 0.1→8, R=3): independently re-argmined from stored opts (13 designs per point, the §6 library). **One isolated jump**, no chatter, ω₂∈(0.322, 0.372): (2,1,0)→(3,1,1), stays through ω₂=8. IMP-N60 predicted C*=4 at all 31 and never matched.

**CT41 mapping is caveated honestly, and is only a loose analogy.** Prereg §8 said: at zero redesign cost, composition jumps where J curves cross, and is constant between crossings (“an inaction region in the swept coordinate”); not a field test; do not pick k after seeing the gaps. Results followed that. Two limits: (i) piecewise-constant argmin of a discrete design family along a continuous parameter is true of *any* such comparative statics, not a distinctive CT41 content; (ii) CT41/CL19 inaction is a *positive-width band* from lumpy k>0 (hysteresis). At k=0 there is no band — the jump is exactly at the crossing. Calling the intervals between crossings “inaction regions” stretches the term. They did not treat it as a field test and did not choose k post hoc. Fair as a cymatics jump check; not a test of CT41.

On the MUST / two-resonator n_res=n design, one Ω collapses and only the fast rhythm locks (errors 0.56% and 99.99%). Results correctly noted that reaching E≈E_∞ is not the same as two internal clocks.

---

## Q6. Labels

Honest on the gates, the D5 disclosures, “in-model, numerical,” “nothing PROVED,” “inclusion rule not patched,” “kind-matching is a library fact, not a counting rule,” “predictive rhythm rule remains OPEN,” and the holographic fail as stated.

**Not honest, and should be corrected in the writeup (not by changing scores):**

1. “At ζ=1 the process is critically damped, not a cycle” (RESULTS §2, §6; KEYSTONE_NOTE §5). False of `osc_world`. ζ_std=1/√2, poles −1±i.
2. “One real store already sits on E_∞” at ζ=1 (RESULTS §6; KEYSTONE_NOTE §5, “already served by one real store”). False. One store has ε≈6.6×10^{-3}–8.1×10^{-3}; two real stores sit on E_∞.
3. Official SANITY MSEs on collapsed-Ω rows are presented as ordinary successful (or barely successful) Lyapunov values. Under the D3 guards the same designs are ill-conditioned and return ∞. Disclose that, or re-run SANITY under D3. The kill stands either way.
4. PRIMARY “58/189” is a *cost* match rate, as the prereg gate specified. Results correctly warn that several of the 58 are cost coincidences. The composition match rate is **51/189**. Worth stating as a number, not only a sentence. The three MUST high-R “matches” are `nr1_nf2`, not two resonators; the four `1osc_z0.25_N0.04` high-R “matches” are two real stores, not a resonator.

No “law,” “theory of everything,” or “bill” language. Field-test language is not used for these in-model checks. CT41 is not claimed as a field test.

---

## Independent scorecard vs `RHYTHM_RESULTS.md`

| Gate | Official | Independent | Agree? |
|---|---|---|---|
| SANITY | 7/8, KILL | 7/8 on stored ε; collapsed rows unsecured under D3; kill robust | Yes on the gate |
| PRIMARY | 58/189 = 30.7% FAIL | 58/189 cost, 51/189 composition | Yes |
| MUST | C*_pred=4, argmin C*=3, J=6.2486, E=0.041022 | Exact, replay clean | Yes |
| REGRESSION IMP-N60 | 5,890/19,320 = 30.5% FAIL | 5,890/19,320 | Yes |
| N60-from-0 / as-written | 19,320 / 18,941 | Same; 379 holes | Yes |
| S5 extended | 0/12 worlds, 0/108 cells | 0/108, 0 same-C E beats | Yes |
| TAUTOLOGY | PASS (predictive, and wrong) | SHA, no ε_C input, formula replay 189+360 | Yes |
| Cymatics (a) | median 0.03986, PASS; 3/7 over | Exact | Yes |
| Cymatics (b) | 2 jumps / 41; 1 jump / 31; no chatter | Exact | Yes |
| Fractal (1)(2)(3) | 3/24 FAIL; CVs fail; 90/90 PASS | Exact | Yes |

---

## What should be preregistered next (if anything)

Do **not** register a patched IMP-N60 (fudged isolated V_m, degree tweaks, or “count a rhythm as two” again). The written rule failed; the predictive rhythm count stays OPEN until there is a new candidate written down before any run.

If a next test is worth locking, the diagnostics above suggest these as *new* preregs, not rescues:

1. **Observer kind, not process kind.** Prediction: the cheap near-optimal library is the kind of the Kalman–Bucy observer poles (conjugate pair iff those poles are complex; real stores iff they are real), paid by *joint* increments — with the tautology trap stated up front, because computing the Riccati is already solving the filter. A *predictive* version would need a closed-form criterion for when observer poles go real (damping, N, variances) that does not solve the ARE, locked before any run. The present MUST hybrid and the ζ=1 collapse are the motivating observations, so they cannot be the confirmation set.
2. **A fairer holographic check**, clearly labeled new: much smaller N and/or R high enough that the last decrement pays (R_need is in the file, 10³–10⁸), denser per_decade, and/or a many-site / high-dimensional construction. Do not re-score the present 15 worlds under a new R after seeing them.
3. **Locking primary as per-world**, not only median-of-medians, if locking is going to be used as evidence. The present aggregate PASS hides 3/7 light-world misses.
4. **Re-run SANITY under D3** (or drop vanishing-Ω designs) if SANITY numbers will be quoted. Optionally add two-real-store designs as the right library when Kalman poles are real. That is a library test, not a new count.
5. Lean formalization of the already-settled core (definition, hull identity, N60-given-convexity) remains appropriate *after* the keystone sentence is stable; it does not fix the open rhythm count.

No merge or push was made. Working notes: `/tmp/rhythm_rescore_findings.json`, `/tmp/rhythm_diag.json`.
