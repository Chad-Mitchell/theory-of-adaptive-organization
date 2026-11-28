# Rhythm / IMP-N60 results

**Scored:** Friday 20 November 2026, 8:49 PM ET (America/New_York), strictly against `RHYTHM_PREREG.md` locked 6:16 PM ET.
**Independent review:** `records/reviews/rhythm_2026-11-20/REVIEW.md` (finished 9:20 PM ET), verdict **SCORING CORRECT**. Official fail/pass gates stand. Writeup labels below are corrected after that review (ζ=1 damping, “one real store on E_∞”, SANITY collapsed-Ω disclosure, composition 51/189, IMP-N60 misspecification, CT41 as a loose analogy, fractal scope). No prereg, inclusion rule, or gate was changed.
**Run:** `rhythm_im_run.json`. Official SANITY from the first official start (6:22:50 PM ET) is kept (D1–D3). Detached resume 7:03:17 PM ET (D4); finished 8:39:30 PM ET; all sections flushed (Part A 122/122, cymatics, fractal 15/15, S5 regression, S5-extended 36/36). Unsecured pre-D3 files were discarded and are not scored.
**Integrity:** prereg SHA-256 `e0b4f2b6f31743fdffe05f0f3eeedfb3d169824136a5671bfdce28ee11fd50ce` matches the run and the predictions file. Predictions SHA-256 `b625a8ad57c3d861d5f0202b36125c4fa405b34260b9c46fdf72a9279d135bb3`, written 6:22:45 PM ET, unchanged. Formula locked: include mode *m* iff \(R(\sigma_m^2 - E_\infty^{(m)})/E_\infty > c_m\).

All findings below are **in-model, numerical**. Nothing here is **PROVED**. The inclusion rule was not patched after seeing argmin *J*. Independent rescoring of the stored designs agrees with the runner on Part A (0 discrepancies). The runner's built-in Model-S scores are **not** used: they have two post-data scoring bugs (D5). Official Model-S numbers are the independent rescore from `s5_rerun.json`, the locked predictions, and per-seed extended-library designs.

---

## Headline verdict (prereg gates)

| Gate | Criterion | Result | Verdict |
|---|---|---|---|
| SANITY (kill) | 8/8 one-oscillator worlds, one resonant layer, \(\varepsilon < 10^{-3}\) | 7/8. `1osc_z1.0_N0.04`: \(\varepsilon = 1.086\times 10^{-3}\) | **KILL / FAIL** |
| PRIMARY (Part A) | IMP-N60 \(C^*\) = extended-library argmin \(C^*\) in \(\ge 180/189\) | **58/189 = 30.7%** cost match; composition match **51/189** | **FAIL** |
| MUST (kill) | `seed2_two_light` at \(R=3\): predicted \(C^*\) = argmin \(C^*\) | predicted \(C^*=4\) (two resonators); argmin \(C^*=3\) (1 resonant + 1 first-order), \(J=6.2486\), \(E=0.041022\) | **KILL / FAIL** |
| REGRESSION (Model S) | IMP-N60 \(\ge 95\%\) of 19,320 | **5,890/19,320 = 30.5%** | **FAIL** |
| TAUTOLOGY | predictions from poles, variances, \(N\), \(R\) only; written before library opts; not an identity on \(\varepsilon_C\) | SHA match; no \(\varepsilon_C\) input; written 6:22:45 PM ET, before official start 6:22:50 PM ET | **PASS** (the rule is predictive, and it predicts badly) |
| CYMATICS (a) | light-damped worlds: median relative locking error \(< 0.05\) | median-of-world-medians **0.03986** \(< 0.05\); but 3/7 light worlds individually exceed 0.05 | **PASS** on the single aggregate statistic as written; locking is uneven (see §8) |
| CYMATICS (b) | \(C^*\) and composition piecewise constant in a continuous sweep, isolated jumps, no chatter | stakes: 2 jumps / 41 points; frequency: 1 jump / 31 points; no chatter | **PASS** (in-model, numerical) |
| HOLOGRAPHIC / FRACTAL | (1) \(K^*=J=\log_{10}\Gamma + 1\) at high \(R\); (2) CV of decrements \(< 0.5\) at \(\alpha=1\); (3) N60-from-0 = argmin when convex | (1) **3/24** primary cells at \(R=100,300\); (2) all four \(\alpha=1\) primary CVs in \(0.996\)–\(1.984\), all fail; (3) **90/90** | (1) **FAIL**, (2) **FAIL**, (3) **PASS** |

**Proposed keystone sentence (not a passed rule):** a layer matches a mode in kind as well as time scale, and is kept only when its *joint* stake increment pays for its degree. That count is N60 in simple-decay worlds (numerical, convexity unproved). For rhythms, kind-matching is sometimes the right library, but no predictive count from poles and stakes has worked; IMP-N60 is not that rule.

---

## 1. Tautology check

PASS. `imp_n60_predictions.json` was written from poles, variances, \(N\), and \(R\) only (locked note in the file). It does not call the library optimizer and does not take an \(\varepsilon_C\) sequence as input. The SHA-256 is unchanged from lock. This is the opposite of the hull-increment identity: the rule can be, and is, wrong.

---

## 2. SANITY (kill): 7/8, FAIL

One optimized resonant layer must reach \(\varepsilon = E/E_\infty - 1 < 10^{-3}\) on each of the eight one-oscillator worlds.

| World | \(\varepsilon\) | \(\Omega\) | matched-pole \(\varepsilon\) | Result |
|---|---|---|---|---|
| `1osc_z0.02_N0.04` | \(1.40\times 10^{-7}\) | 0.978 | 8.53 | PASS |
| `1osc_z0.02_N0.2` | \(8.35\times 10^{-8}\) | 0.999 | 3.29 | PASS |
| `1osc_z0.08_N0.04` | \(1.79\times 10^{-7}\) | 0.787 | 4.23 | PASS |
| `1osc_z0.08_N0.2` | \(1.48\times 10^{-7}\) | 0.985 | 1.40 | PASS |
| `1osc_z0.25_N0.04` | \(9.69\times 10^{-4}\) | \(3.0\times 10^{-5}\) (collapsed) | 2.21 | PASS (barely; not secure under D3) |
| `1osc_z0.25_N0.2` | \(2.08\times 10^{-7}\) | 0.904 | 0.604 | PASS |
| `1osc_z1.0_N0.2` | \(8.51\times 10^{-7}\) | \(1.7\times 10^{-5}\) (collapsed) | 0.100 | PASS |
| `1osc_z1.0_N0.04` | \(1.086\times 10^{-3}\) | \(1.1\times 10^{-5}\) (collapsed) | 0.631 | **FAIL** |

Lightly damped rhythms reach the causal floor to \(\sim 10^{-7}\), and the Kalman poles are *not* the process poles (matched-pole \(\varepsilon\) is \(O(1)\)–\(O(10)\), as the prereg allowed for diagnosis). The label \(\zeta=1\) does **not** mean the process is critically damped: `osc_world` places poles at \(-\zeta\omega \pm i\omega\), so at \(\zeta=1\), \(\omega=1\) the poles are \(-1\pm i\) (standard damping \(1/\sqrt{2}\approx 0.707\)), still a damped cycle. On those worlds the Kalman–Bucy observer poles are *real* and split; a conjugate-pair block cannot realize two different real rates, and \(\Omega\to 0\) is that family trying, and failing, to become a two-real-pole filter. Two real stores, not one, match Kalman and sit on \(E_\infty\). The official FAIL on `1osc_z1.0_N0.04` is robust (a bounded-\(\Omega\) probe stays on the same side of the gate). This is a kill as written. No criterion is relaxed.

**Disclosure (D3).** Official SANITY MSEs were frozen from the post-D1 / pre-D3 pass (D3: “official SANITY is kept”). Replaying the three collapsed-\(\Omega\) designs under the later D3 guard (\(\mathrm{cond}(P_{zz})>10^{10}\to\infty\)) returns \(\infty\) (cond \(\approx 1.4\times 10^{12}\), \(8.1\times 10^{10}\), \(2.9\times 10^{10}\)). Those stored \(\varepsilon\) values are therefore unsecured under the guards later adopted. The barely-PASS on `1osc_z0.25_N0.04` is not secure: a \(\Omega\ge 0.2\) probe is at \(\varepsilon=1.07\times 10^{-3}\), which would fail. The kill (need 8/8) still stands, and if anything would be harsher.

---

## 3. PRIMARY (Part A): 58/189 = 30.7%, FAIL

21 rhythm worlds \(\times\) 9 values of \(R\). Extended-library argmin includes \(C=0\), first-order designs from `rhythm_rule.json` (\(E_k\) at \(k=0,\ldots,2n+2\)), and the official resonant / mixed optimizations. Independent rescore matches the runner exactly.

Per-world matches (predicted \(C^*\) vs argmin \(C^*\)):

| World | Match |
|---|---|
| `1osc_z0.02_N0.04`, `_N0.2` | 8/9, 8/9 (miss only at \(R=0.5\), where one first-order store beats a cost-2 resonator) |
| `1osc_z0.08_N0.04`, `_N0.2` | 6/9, 7/9 |
| `1osc_z0.25_N0.04`, `_N0.2` | 4/9, 5/9 (several “matches” are cost-only: argmin is two real stores, not a resonator) |
| `1osc_z1.0_N0.04`, `_N0.2` | 0/9, 1/9 (argmin is not a resonator; one real store is *not* on \(E_\infty\); two real stores are) |
| `seed2_two_light` (MUST world) | 3/9 (only \(R\in\{20,50,100\}\), and even then the composition is 1 resonator + 2 first-order, not two resonators) |
| `2osc_sep15_*` / `2osc_close2_*` (light, light-medium, medium, heavy) | 4/9, 2/9, 0/9, 0/9 / 5/9, 2/9, 0/9, 0/9 |
| `3osc_*` (light, mixed, medium, heavy) | 3/9, 0/9, 0/9, 0/9 |

The gate is on \(C^*\) only: **58/189** cost matches, of which **51/189** also recover the predicted composition (7 are cost-only coincidences). The three MUST high-\(R\) “matches” are `nr1_nf2`, not two resonators; the four `1osc_z0.25_N0.04` high-\(R\) “matches” are two real stores, not a resonator. On one light oscillator at moderate-to-high \(R\), a single resonant layer *is* the argmin and does reach \(E_\infty\), which is the qualitative internal-model picture. That does not scale to a counting rule.

---

## 4. MUST: `seed2_two_light` at \(R=3\), FAIL

Predicted \(C^*=4\) (both rhythms included, two resonators). Extended-library argmin is \(C^*=3\): one resonant layer plus one first-order store (`nr1_nf1`), \(E=0.041022\), \(J=6.2486\). Two resonators reach \(E=0.037956\) (essentially \(E_\infty=0.037883\)) at \(C=4\), \(J=7.006\), which loses to the hybrid. The old first-order-only argmin is \(K=3\), \(J=7.105\), which already agrees with the worked example in `theory/KEYSTONE_NOTE.md` §2; it also loses to the hybrid — so kind-matching *helps*, but the isolated-mode count over-includes. (An earlier writeup, and the prior rhythm review, quoted \(J=8.105\) / \(8.10\), which is \(1+7.105\), the same off-by-one cost error class as D5a. The official MUST gate does not use that figure and does not flip. The prior review file is left unedited as a historical record.)

This is the kill even if PRIMARY had passed. It did not.

---

## 5. REGRESSION (Model S): IMP-N60 5,890/19,320 = 30.5%, FAIL

Official independent rescore from `s5_rerun.json` (120 worlds, \(K=0..J\), 161-point \(R\) grid) and the locked IMP-N60 predictions.

| Rule | Match | Notes |
|---|---|---|
| IMP-N60 (isolated \(V_m\), \(c_m=1\)) | **5,890 / 19,320 = 30.5%** | Fails the 95% gate. Predicts \(C^*=0\) in 539 cells and is right in all 379 true holes, but also predicts 0 in 160 cells where argmin \(\ge 1\), and over-includes at higher \(R\) (isolated \(V_m\) does not follow joint diminishing returns). |
| N60-from-0 | **19,320 / 19,320 = 100%** | Including the \(K^*=0\) hole. Confirms S5: convexity on all 120 worlds (numerical), and the joint-increment rule still equals argmin \(J\). |
| N60-as-written (starts at 1) | **18,941 / 19,320 = 98.04%** | The 379 misses are exactly the known hole (\(R\le 1.41\), 39 worlds). Same numbers as `S5_RESULTS.md`. |

IMP-N60 was **misspecified as a generalization of N60**. N60 walks *joint* optimized decrements of \(\varepsilon_K\); IMP-N60 uses *isolated* causal value \(V_m\) and includes modes independently. Isolated \(V_m\) is not the joint increment, already on Model S, where N60 is numerically exact and kind-matching is irrelevant. Isolated ranking disagrees with joint ranking on 105/120 S5 worlds. Isolated \(V_m\) overstates late modes and understates the first joint decrement (e.g. seed 0: \(V=(0.368,0.055,0.205)\), joint decrements \((0.645,0.0455,0.00091)\)). The rule stays **FAILED**; this is not a license to rewrite \(V_m\) after the data, and no rescue is registered.

**12-world extended-library subset.** Adding resonant modules does not change argmin relative to first-order-only on any of the 12 seeds \(\times\) 9 \(R\) values (0/108). N60 / first-order remains the Model-S argmin. The runner's built-in score (`n_worlds_with_change=1`, seed 5 at all 9 \(R\)) is a cross-world tag mix-up: it scored seed 52's design (`s5_52::nr1_nf0`, \(E=0.0445\)) against seed 5 (\(E_\infty=1.162\)). Independent per-seed scoring finds no change. See D5.

---

## 6. Diagnosis (no rule patch)

The parent hypothesis is only half right. N60's increment formula fails for rhythms in a first-order library because of a basis mismatch — that part stands, and a resonant layer is the right *module* for a lightly damped cycle (SANITY, one-oscillator PRIMARY at high \(R\), cymatics jumps). The proposed *count* — include a matched layer iff isolated \(R V_m > c_m\) — fails for three structural reasons, visible before any excuse about overlapping modes:

1. **Isolated \(V_m\) is not the joint increment.** It already fails on Model S, where the library is correctly first-order and N60 (joint decrements) is exact on this grid. Overlapping-mode crudeness is a predicted weakness of IMP-N60; it is fatal, not local to close frequencies.
2. **The rule over-charges at intermediate \(R\).** Even when both isolated rhythms “pay” for a cost-2 layer, the joint optimum is often a cheaper hybrid (MUST: \(C=3\), not \(C=4\)). At low \(R\) a single first-order store can beat any resonator on cost.
3. **Observer kind, not process kind, at the \(\zeta=1\) label.** `osc_world` at \(\zeta=1\) has poles \(-1\pm i\), not a critically damped process (standard damping \(1/\sqrt{2}\)). Kalman poles are real and split; one real store is *not* on \(E_\infty\) (\(\varepsilon\approx 6.6\times 10^{-3}\)–\(8.1\times 10^{-3}\)); two real stores are, and they match Kalman. The resonant block collapses to \(\Omega\to 0\) because it cannot realize two different real rates. IMP-N60 still wants \(C=2\).

So kind-matching is a library fact, not a counting rule. A predictive rhythm rule remains **OPEN**. No new candidate is registered here.

---

## 7. Cymatics

**(a) Frequency locking.** On every Part A world, the \(n_\mathrm{res}=n\) design is paired to world frequencies by the assignment that minimizes the sum of relative errors. For the seven light-damped worlds (every \(\zeta\le 0.08\)):

- Median of the seven world-medians: **0.03986** \(< 0.05\). **PASS** on the single aggregate statistic the prereg writes down.
- Per world, 3/7 exceed 0.05: `1osc_z0.08_N0.04` (0.213, \(\Omega=0.787\) vs \(\omega=1\)), `2osc_sep15_light_light` (0.236; the slow mode is at 0.027 vs 0.05, 46% error), `2osc_close2_light_light` (0.094). The very light one-oscillator worlds (\(\zeta=0.02\)) lock to 0.1–2.2%. `3osc_light_light_light` is 0.0399.
- Heavy-damped worlds (not a hard fail): medians typically \(0.5\)–\(1\), with \(\Omega\to 0\). On the MUST world the two-resonator design reaches \(E_\infty\), but one \(\Omega\) collapses to \(0\) and only the fast rhythm is locked. Reaching the floor is not the same as two internal clocks.

**(b) Discrete jumps.** Starting from `2osc_sep15_light_light`, two sweeps, argmin over the §6 library at each point.

- *Stakes* (\(R\) from 0.25 to 200, 41 log-spaced points, world frozen): \(C^*\) is piecewise constant with **two isolated jumps**, no chatter. \(C=1\) (one first-order store) up to \(R=1.571\); jumps to \(C=3\) (1 resonant + 1 first-order) at \(R=1.857\); jumps to \(C=4\) (two resonators) at \(R=7.071\) and stays there through \(R=200\). IMP-N60 predicted \(C^*=4\) at every point and matches only after the second jump (21/41 points).
- *Frequency* (faster \(\omega_2\) from 0.1 to 8, 31 log-spaced points, \(R=3\)): **one isolated jump**, no chatter. \(C=2\) (one resonator) up to \(\omega_2=0.322\); jumps to \(C=3\) (1 resonant + 1 first-order) at \(\omega_2=0.372\) and stays there through \(\omega_2=8\). IMP-N60 predicted \(C^*=4\) at all 31 points and never matched.

**(Relation to CT41: a loose analogy only, in-model, not a field test.)** At zero redesign cost, the composition is constant between *J*-curve crossings and jumps at a crossing, as the prereg mapped to CT41 / CL19. That piecewise-constant argmin is true of any discrete design family along a continuous parameter, not distinctive CT41 content; CT41/CL19 inaction is a positive-width band from lumpy \(k>0\), and at \(k=0\) the jump is exactly at the crossing. Calling the intervals “inaction regions” is a loose analogy, not a test of CT41. Zero-\(k\) crossings are bracketed at \(R\in(1.571, 1.857)\) and \(R\in(5.983, 7.071)\) in stakes, and at \(\omega_2\in(0.322, 0.372)\) in frequency. We do not choose a lumpy redesign cost \(k\) after seeing the gaps. Status: in-model, numerical.

Cymatics is, in Chad's words, necessary but not sufficient: the best design does jump rather than slide, and light resonators often lock, but that does not yield a predictive count.

---

## 8. Holographic / fractal check

**Preregistered** in `RHYTHM_PREREG.md` §9 (6:16 PM ET) and **run** (15 worlds; 12 primary + 3 extra `per_decade=2`). First-order library only, Model S scale-free worlds, `stores.scalefree_world`. Status: in-model, numerical.

1. **\(K^*=J\) at high stakes: FAIL.** At \(R=100\) and \(R=300\), only **3/24** primary cells have \(K^*=J=1+\log_{10}\Gamma\): the three \(\Gamma=10\) (\(J=2\)) worlds at \(R=300\) only. At \(R=100\), every primary world has \(K^*\le 2\). For \(\Gamma\ge 100\) (\(J=3,4,5\)), N60-from-0 never includes every mode on this \(R\) grid (max \(K^*=2\) or, once, 3 at \(R=300\)). The extra `per_decade=2` arm is the same: \(K^*\) is 1 or 2 at high \(R\), not \(1+2\log_{10}\Gamma\). The later decrements are tiny (the first store already sits near \(E_\infty\)), so they do not pay at \(R\le 300\).
2. **Equal value per layer: FAIL** (hard-fail on \(\alpha=1\)). Coefficient of variation of the \(J\) adjacent decrements is \(0.996\), \(1.404\), \(1.719\), \(1.984\) on the four primary \(\alpha=1\) worlds — all well above 0.5. Almost all of the error reduction is in the first layer. Tilted spectra (\(\alpha\neq 1\)) are the same or worse (CV up to 2.44 on the extra arm).
3. **N60-from-0 vs argmin: PASS.** All 15 worlds have convex \(\varepsilon_K\) on \(K=0..J\). N60-from-0 matches argmin \(J\) in **90/90** cells. Convexity itself remains unproved. This is N60 doing what it already does on Model S, not a confirmation of the renormalization / MERA counting picture.

The holographic analogy (Vidal 2007; Swingle 2012; Mehta & Schwab 2014) suggested layers growing as the log of the scale range, at roughly equal value each. In this preregistered Model-S construction — a low-dimensional scalar OU-sum in white noise, with \(N=0.05\) already large enough that one well-placed store sits near the causal floor — that picture does not hold at the stated stakes: one store takes almost all of the value, and extra modes pay only at much higher \(R\) than 300 (\(R_\mathrm{need}\sim 10^3\)–\(10^8\) for \(\Gamma\ge 100\)). The fail is honest in-model at \(N=0.05\) and the locked \(R\). It does **not** test a spatial or high-dimensional MERA / holographic picture, which is about a stack of coarse-grainings of a many-site state. A fairer check would be a new prereg (smaller \(N\), higher \(R\) or dimension), not a re-score of these 15 worlds.

---

## 9. What stands, and what is still open

- N60, given convexity, still equals argmin \(J\) in Model S (19,320/19,320 from 0, including the hole; extended-library resonators do not change it). Convexity is numerical, unproved. The \(K^*=0\) hole of N60-as-written is unchanged (379/19,320).
- A first-order-only increment count is false for rhythms (already shown; hybrid / resonant libraries change the argmin, e.g. MUST \(J=6.25\) vs first-order \(K=3\), \(J=7.105\)).
- IMP-N60, the candidate predictive rule from poles and stakes, was misspecified as a generalization of N60 (isolated \(V_m\) vs joint increments) and **FAILED** its kill, primary, and Model-S regression gates (cost match 58/189; composition match 51/189). It is not tautological; it is simply not the right count. It stays failed; no rescue is registered.
- Kind-matching (a resonant layer for a light rhythm) is a real library fact, not a counting rule. Cymatics jumps pass; locking passes only as an aggregate median (3 of 7 light worlds miss individually). The link from those jumps to CT41 is a loose analogy only.
- The holographic / log-span equal-value picture **FAILED** in-model at \(N=0.05\) on the preregistered fractal worlds at the stated \(R\). That construction does not test a spatial or high-dimensional MERA picture.
- A predictive rhythm rule (layer count from poles and stakes, without first computing the whole \(\varepsilon\) curve) remains **OPEN**. No new rule is proposed in this file. Independent review (`records/reviews/rhythm_2026-11-20/REVIEW.md`) is **SCORING CORRECT**; the official gates stand.
