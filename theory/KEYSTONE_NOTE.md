# Keystone note: the diminishing-returns premise of N60

*20 Nov 2026, first written about 4:10 PM ET, revised after independent review (READY-WITH-FIXES) beginning 4:35 PM ET, results filled about 5:15 PM ET, revised again after the confirm review (B3) about 5:25 PM ET, revised after the S5 Model-S rerun about 5:31 PM ET, and revised after the IMP-N60 / cymatics / fractal scoring about 8:49 PM ET (America/New_York). Beside `main` at `ff14a87` (PR #117 merged as v2.67, PR #116 merged as v2.68, PR #118 hygiene as `ff14a87`). The first review is at `records/reviews/core_2026-11-20/REVIEW.md`; the confirm review is at `records/reviews/core_2026-11-20/CONFIRM.md`; the re-confirm is at `records/reviews/core_2026-11-20/RECONFIRM.md`. Independent review of the IMP-N60 run: `records/reviews/rhythm_2026-11-20/REVIEW.md` (SCORING CORRECT). Code: `theory/keystone_checks/`. Rhythm test: `RHYTHM_PREREG.md`, `RHYTHM_RESULTS.md`.*

**Pointer (21 Nov 2026):** `theory/LAYER_CONVEXITY.md` (CLAIM_MAP N64) proves convexity for Model S with J ≤ 2 and for every monotone-SNR world in the band model 𝓑; Model S with J ≥ 3 is still numerical.

N60 (PR #116, CLAIM_MAP: **PROVED (in-model) given convexity, which is numerical only**) states, in Model S,

$$K^*=\arg\min_K\bigl[K+R(1+\varepsilon_K)\bigr],$$

and, if ε_K is convex and decreasing in K,

$$K^*=1+\#\{k\ge 2:\ R(\varepsilon_{k-1}-\varepsilon_k)>1\}.$$

The count formula is a one-line argument once convexity is granted (decrements are then non-increasing, so the cost falls while the marginal value exceeds upkeep and rises afterwards). The question is whether that premise holds in the model class.

**Model S, as defined in `theory/LAYERS.md` and THEORY CT21, is a sum of Ornstein–Uhlenbeck modes** (real poles), read through white noise, tracked by first-order real stores. Rhythms are in the broader linear-Gaussian class 𝓜_LG, and THEORY already treats a rhythm as a two-state mode. That degree convention is the right *counting of a mode*. It is not, by itself, a counting *rule* that recovers argmin J when stores are first-order and real.

## 1. Inside Model S: no counterexample found; still unproved

After the #116 optimizer fix (store rates kept at least 2% apart; MSE re-evaluated at the returned rates, so E_K is never below the causal minimum):

- 120 random OU worlds, 3 or 4 modes, separations ×3 to ×100, rerun with the merged #116 solver and the reviewer multi-start (`theory/keystone_checks/s5_rerun.py`, OPEN_WORK S5): **120 / 120** convex on K = 1..J at both 10⁻⁴ and 10⁻⁶, and also on K = 0..J at 10⁻⁴. No E_K fell below E_∞; no increasing E_K. For every 3-mode world with ε_1 > 10⁻³, ε_2/ε_1 ranged from 6.6×10⁻⁶ to 0.3147 (convexity needs ≤ 0.5). N60 matched argmin J in 18,941 / 18,941 comparisons with argmin ≥ 1; the only disagreements were the known K* = 0 hole (379 comparisons, 39 worlds, R ≤ 1.41). No counterexample. Full writeup: `theory/keystone_checks/S5_RESULTS.md`.
- The earlier 120-world search (`convexity_targeted.py`) used the pre-#116 raw `solve`/`lstsq` in this folder and recorded “0 non-convex beyond 10⁻⁴,” but seed 24 had overflowed to ε = [−1, NaN, NaN, NaN] and was counted as no violation only because a NaN fails the test. Under the merged solver that world is clean and convex. Of the other 119, 116 agree with the new ε sequence to tight tolerance; three differ only at 10⁻⁷–10⁻⁸ on an already-flat tail. The #116 review (39/40; the 40th was the optimizer bug) and `face_collapse_v23.py` V2 (300 worlds: 0.973 strictly convex, 1.000 within tolerance) remain supporting Model S evidence.
- 24 further worlds in the wide search with only real poles (classes A clustered OU, D smooth/low-pass, E large variance contrast): **0** violations, still on the older solver (not part of the S5 rerun).
- The adversarial climb maximizing ε₂/ε₁ over 3-mode OU worlds has finished (`adversarial.out`): max ε₂/ε₁ = 0.4625 (τ = 1, 2.61, 4.06×10⁷), still below 0.5. The independent core reviewer re-optimized that world with the guarded solver and got 0.461. Closest approach found, not a violation.
- This agrees with the #116 review (39 of 40 random worlds convex; the 40th was the optimizer bug) and with `face_collapse_v23.py` V2.

An earlier un-fixed search (`convexity_search.py`, 60 worlds) produced 6 apparent non-convexities and 9 formula mismatches; all were tiny negative ε or optimizer residuals of the kind the #116 review diagnosed. They are not counterexamples.

**What a proof would need.** In Model S, E_J = E_∞ exactly (the causal Wiener filter has J real poles, L2). Convexity of (E_1, …, E_J) is a statement about how the MSE of the best degree-K rational filter falls as K rises on a positive combination of Lorentzians. Closest prior art found: Das & Kempe, STOC 2008 (doi 10.1145/1374376.1374384), on the diminishing returns of subset selection in linear regression — a different problem (subset, not degree of a causal filter). I did not find, and did not produce, a proof.

A small scope note, even when convexity holds: the formula as written starts at K = 1, so it cannot return the K* = 0 (act blind) that CT21 allows when stakes are small. (LAYERS.md's Theorem L1 used to say "K* = 1 for every w and h"; it now matches CT21: one real pole ⇒ K* ∈ {0, 1}.)

## 2. Outside Model S, inside 𝓜_LG: the increment formula is false

When the world has **rhythms** (complex conjugate poles) and the stores remain first-order and real, ε_K need not be convex, and the count formula can return the wrong K*. This is the setting THEORY already flags: a lightly damped oscillation is a two-state mode, and real first-order stores only approximate it.

In 40 worlds of a wider class (`convexity_wide.py`, 2% separation and re-evaluated MSE, but not the Jacobi-scaled pseudo-inverse), all 6 non-convex cases had at least one rhythm (3 of 8 two-rhythm worlds, 3 of 8 rhythm-plus-OU worlds). None of the 24 real-pole worlds failed.

**Worked example** (`rhythm_counterexample.py`; two oscillators, seed 2 of the wide search). Independently confirmed by the core reviewer with the guarded inversion, a Lyapunov MSE, and a multi-start of informed grids, Nelder–Mead, L-BFGS-B and differential evolution (no `minimum.accumulate` on E_K). Decrements of ε_K:

| K | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| ε_K | 1.1255 | 0.9464 | 0.3682 | 0.1427 |
| ε_{K−1} − ε_K | — | 0.1791 | **0.5782** | 0.2256 |

The second store buys less than the third. At R = 3, J_K = K + R(1+ε_K) is 7.376, 7.839, **7.105**, 7.428, so the argmin is K* = 3. The reviewer's best K = 4 design (E₄ ≈ 0.04329, Lyapunov 0.04329) stays above the threshold that would make J₄ beat J₃ (E₄ would need to be < 0.03921). The fitted stores at K = 2, 3 and 4 are tight real clusters at one rate, not two conjugate-pair allocations. The N60 formula, which adds a layer whenever that layer's own decrement exceeds 1/R, adds only K = 3's decrement and returns 2. The two disagree.

That is not a refutation of N60 as written: N60 is scoped to Model S. It is a reason not to export the count formula to 𝓜_LG with real first-order stores.

**The informal keystone does not hold by paying for a rhythm as a pair.** A pair rule predicts even K* (0, 2 or 4 in this example). The independently confirmed argmin is 3, not 2 or 4. "Counted by degree" remains the right convention for a mode in CT21; it is not a block-count rule that recovers this K*. A predictive rhythm rule (K* from the poles and the stakes, without first computing the whole ε_K curve) is OPEN. §4 records the definitional identity and the sweep's empirical findings.

The same non-convexity is the fitness valley EVO1 found when layers are complements (W4, W4b; CT36, CL13; W4's creation valley met the D2b bar (4/4); W4b's D1b bar was not met (2/4)): a step that adds only half of a pair can fail to pay. That diagnosis still fits the non-monotone decrement; it does not restore a pair-count rule, because the argmin here is not a completed pair.

## 3. Honest status

| Claim | Status |
|---|---|
| Count formula given convexity | Proved (elementary) |
| Convexity in Model S (OU sums) | Proved for \(J\le 2\) at lead 0 (N64). For \(J\ge 3\), numerical only, still unproved (S5 120/120 convex at 10⁻⁴ and 10⁻⁶, plus 24 fresh \(J=5\) worlds; N60 matches argmin on every comparison with argmin ≥ 1). The from-1 formula's \(K^\star=0\) hole remains. See `theory/keystone_checks/S5_RESULTS.md` |
| Convexity, and the increment formula, in 𝓜_LG with first-order real stores | **False.** Counterexample: two rhythms, R = 3, formula 2 vs argmin 3. A pair-rule rescue also fails (predicts even K*, argmin is 3) |
| Predictive rhythm rule (K* from the poles and the stakes, without the whole ε_K curve) | **OPEN.** The candidate IMP-N60 rule (include a matched layer iff isolated \(R V_m > c_m\)) was misspecified as a generalization of N60 (isolated \(V_m\) vs joint increments) and **FAILED** its preregistered gates: SANITY 7/8 (kill), PRIMARY 58/189 cost / 51/189 composition, MUST (`seed2_two_light` at \(R=3\): predicted \(C^*=4\), argmin \(C^*=3\)), Model-S regression 5,890/19,320. It is predictive, not tautological, and it is the wrong count. It stays failed; no rescue is registered. Independent review (`records/reviews/rhythm_2026-11-20/REVIEW.md`) is SCORING CORRECT. See `theory/keystone_checks/RHYTHM_RESULTS.md` |
| Field test of either | None |

The predictive keystone in `CORE.md` — layers from the world's time scales whose stakes pay for them, counted by degree — is therefore proved for \(J\le 2\) at lead 0 (N64) and numerically supported for \(J\ge 3\) only in Model S, and there only given convexity, which remains unproved for \(J\ge 3\). The single-store count formula is used only where diminishing returns have been checked, which so far is Model S, in-model, unproved. For rhythms the first-order increment formula is false, and the isolated-mode internal-model count (IMP-N60) is also false. A predictive rhythm rule is still OPEN.

## 4. Rhythms: the definitional identity; a predictive rule is OPEN

The N60 increment rule equals argmin_K [K + R(1+ε_K)] *when ε_K is convex*, because decrements are then monotone and the first unprofitable adjacent step is the last. Without convexity the adjacent count is not the argmin: it can skip a later step that more than pays for an earlier loss, as in the worked example.

The predictive keystone — layers from the world's time scales whose stakes pay for them, counted by degree — is proved (\(J\le 2\) at lead 0, N64) or numerically supported (\(J\ge 3\)) only in Model S, and there only given convexity, which remains unproved for \(J\ge 3\).

For rhythms, the only general statement is the definitional one: \(K^*\) is \(\arg\min_K\bigl[K+R(1+\varepsilon_K)\bigr]\), which always coincides with the supporting line to the lower convex envelope of the measured ε_K (including K = 0). That is not a new rule. To evaluate either J or the hull you must already have ε_K at every K you consider — that is, you have already solved the design problem at each K. The procedure is a counting restatement of argmin J on a measured curve, not a prediction from the world's time scales (poles, damping, stakes) alone.

The reduced layer-count objective used in N60 is

$$J(K)=hK+w E_K=h\bigl[K+R(1+\varepsilon_K)\bigr],$$

with \(R=w E_\infty/h>0\), or equivalently \(\varphi(K)=\varepsilon_K+K/R\). \(K\) ranges over a finite set \(\{0,1,\ldots,K_{\max}\}\). No property of the world, the stores, or the optimizer is used.

**Proposition.** Every minimizer of φ (hence of J) lies on the lower convex hull of the points {(K, ε_K)}. The N60-style increment test on that hull — walk the vertices \(k_0<k_1<\cdots\) and jump from \(k_i\) to \(k_{i+1}\) iff \(R(\varepsilon_{k_i}-\varepsilon_{k_{i+1}})>(k_{i+1}-k_i)\) — returns a minimizer, and with the strict inequality returns the leftmost minimizer. Equality is exact up to ties (a hull edge of slope exactly −1/R).

**Proof.** Suppose \(k^*\) minimizes φ but \((k^*,\varepsilon_{k^*})\) lies strictly above the lower hull. Then there are hull vertices \(k_a<k^*<k_b\) and \(\lambda\in(0,1)\) with \(k^*=\lambda k_a+(1-\lambda)k_b\) and \(\varepsilon_{k^*}>\lambda\varepsilon_{k_a}+(1-\lambda)\varepsilon_{k_b}\). Then

$$\varphi(k^*)>\lambda\varphi(k_a)+(1-\lambda)\varphi(k_b)\ge\min\bigl(\varphi(k_a),\varphi(k_b)\bigr),$$

so \(k^*\) is not a minimizer. Thus every minimizer is a hull vertex (or, in a tie, any integer point on a hull edge of slope −1/R, all of which lie on the hull).

The lower-hull edge slopes \(s_i=(\varepsilon_{k_{i+1}}-\varepsilon_{k_i})/(k_{i+1}-k_i)\) are nondecreasing. A supporting line of slope −1/R touches at the vertices where the left slope is ≤ −1/R and the right slope is ≥ −1/R. The jump test is exactly "\(s_i<-1/R\)." Walking from the left and taking every such jump stops at the leftmost supporting point of slope −1/R, i.e. a leftmost minimizer of φ. If some \(s_i=-1/R\), the strict test does not jump, and any point on that edge is also a minimizer. □

This is an identity for an arbitrary real sequence ε_K. It does not require convexity of ε_K, a well-optimized curve, rhythms, or Model S. The two procedures agree whether or not the curve is optimal. Good optimization is needed only for the agreed-upon K* to be the true design optimum, not for the match itself. Including K = 0 in the envelope (and in the argmin) closes the formula's K* = 0 hole by definition. That is a correct index fix, not a further empirical discovery.

A predictive rhythm rule (K* from the poles and the stakes, without first computing the whole ε_K curve) is **OPEN**.

**Sweep** (`theory/keystone_checks/rhythm_rule.py`; nice 19, 7 workers, 29 minutes; first aborted start discarded). 21 designed worlds: 1–3 oscillators × damping (light / medium / heavy, and mixed) × two frequency separations for n = 2, plus the worked example; R ∈ {0.5, 1, 2, 3, 5, 10, 20, 50, 100}; K = 0 … 2n+2. First-order real stores. Optimizer: the reviewer's multi-start (informed grids around oscillator moduli; Nelder–Mead, L-BFGS-B polish, differential evolution for K ≤ 4) with the #116 guarded inversion, 2% separation, MSE re-evaluated at the returned rates, no `minimum.accumulate`. Lyapunov MSE checked the worked example and any E sequence flagged as increasing. Compared against argmin J (including K = 0): N60 raw, N60 adjacent from K = 0, the hull increment, an even/pair argmin, and a degree-pairs rule (K ∈ {0, 2, …, 2n}). Data: `rhythm_rule.json`, short log `rhythm_rule.out`.

**Results** (189 comparisons; independently recounted in the confirm review from `rhythm_rule.json`). These are the empirical findings of the sweep. The hull increment matching argmin J is the identity above, not evidence for a new rule. The confirm review also recomputed both procedures on the 189 stored curves (189/189) and on 2,000 random ε sequences of length 2–12 (2,000/2,000); that is what the identity requires.

- 21 worlds, 9 values of R, 189 comparisons; 11 worlds convex, 10 non-convex (all light or medium 2- and 3-oscillator worlds).
- **N60 raw (starts at 1) = argmin in 170/189.** Of the 19 misses, 2 are the known K* = 0 hole (convex one-oscillator worlds at R = 0.5). The other 17 are genuine formula failures, all in non-convex worlds (17/90). On convex worlds with argmin ≥ 1 the adjacent formula never missed (97/97).
- **A pair rule fails, repeatedly.** Restricting the argmin to even K matches in only 66/189 (fails on every odd K*). A degree-pairs cap (K ∈ {0, 2, …, 2n}) matches in 53/189. At high R, K* can exceed 2n (the worked example wants 6, not 4, at R = 50 and 100).
- **K* is odd in 123/189**, and K* ∈ {3, 5} in 15 comparisons. The worked example at R = 3 is one of them (argmin 3, N60 2, even/pair 4). A single lightly damped oscillator, with convex ε_K, has K* = 3 at intermediate R and K* = 4 at higher R (`1osc_z0.02_N0.04` at R = 20; `1osc_z0.02_N0.2` at R = 5, then 4). Real first-order stores can need more than the mode's degree, and the extra store need not come in a pair.

The worked example was reproduced: E_∞ = 0.03788281801526715 (agrees with the reviewer to all reported digits); (E_1,…,E_4) = (0.08051946, 0.07373616, 0.05183293, 0.043288), Lyapunov gaps 10⁻¹⁶ to 1.6×10⁻⁶; at R = 3, J = (7.376, 7.839, **7.105**, 7.428), argmin 3, N60 2, even/pair 4. Four "increasing E" flags in the sweep were 10⁻⁸ to 10⁻⁶ residuals on already-flat tails, not optimizer failures. No E_K fell below E_∞.

**What this is not.** A predictive rhythm rule is **OPEN**. No pole-count or pair-count shortcut on this grid recovered it. It is not a license to export N60's adjacent count to 𝓜_LG. The grid is designed, not a random sample; K was capped at 2n+2, so some E_K sequences (notably three light oscillators: E_8 = 0.0626 vs E_∞ = 0.0554) had not yet reached the causal floor; DE was used only for K ≤ 4. Status stands: the increment formula in N60 is the right special case when ε_K is convex — which in this sweep was every one-oscillator world and the heavy-damped two- and three-oscillator worlds, and which is proved for \(J\le 2\) at lead 0 (N64) and remains unproved for \(J\ge 3\), with no counterexample, in Model S (now including the merged-solver 120-world rerun, S5). For rhythms, the only general statement is the definitional identity above.


## 5. IMP-N60, cymatics, and the holographic check (20 Nov, 8:49 PM ET)

Prereg locked 6:16 PM ET in `theory/keystone_checks/RHYTHM_PREREG.md` (SHA-256 `e0b4f2b6f31743fdffe05f0f3eeedfb3d169824136a5671bfdce28ee11fd50ce`); predictions locked 6:22:45 PM ET (`imp_n60_predictions.json`); official run finished 8:39:30 PM ET. Scored in `theory/keystone_checks/RHYTHM_RESULTS.md`. Status: in-model, numerical. Nothing in this section is PROVED. The inclusion rule was not patched after seeing argmin *J*.

**Hypothesis.** N60 fails for rhythms because the library is only first-order stores, while a rhythm is a complex pole pair (internal model principle, Francis & Wonham 1976). The candidate rule IMP-N60 predicts \(C^*\) from poles, variances, \(N\), and stakes alone: include mode *m*'s matched layer (resonant, cost 2, or first-order, cost 1) iff \(R V_m > c_m\), with \(V_m = (\sigma_m^2 - E_\infty^{(m)})/E_\infty\).

**Verdict: IMP-N60 failed.** It was misspecified as a generalization of N60: isolated \(V_m\) is not the joint increment, already on Model S. SANITY 7/8 (kill: `1osc_z1.0_N0.04`, official \(\varepsilon=1.086\times 10^{-3}\), \(\Omega\to 0\); collapsed-Ω SANITY MSEs are ill-conditioned and unsecured under the later D3 guards; the barely-PASS on `1osc_z0.25_N0.04` is not secure; the kill stands). PRIMARY 58/189 cost match, 51/189 composition match (need \(\ge 180\) on cost). MUST failed: at \(R=3\) on the worked example, predicted \(C^*=4\), argmin \(C^*=3\) (one resonator + one first-order store, \(J=6.2486\)). Model-S regression 5,890/19,320 = 30.5% (need \(\ge 95\%\)). The tautology check passed: the predictions were from poles and stakes only, written before the library run, and are not an identity on \(\varepsilon_C\). The rule is predictive, and it predicts badly. It stays **FAILED**; no rescue is registered. Independent review (`records/reviews/rhythm_2026-11-20/REVIEW.md`, SCORING CORRECT) confirms the gates and these label corrections.

**What still holds in Model S (S5, and the 12-world extended subset).** N60-from-0 matches argmin *J* in 19,320/19,320, including the \(K^*=0\) hole. N60-as-written matches 18,941/19,320; the 379 misses are exactly that hole. Adding resonant modules does not change argmin on any of the 12-seed \(\times\) 9-\(R\) cells (0/108). Isolated \(V_m\) is not a generalization of N60; joint increments still are.

**Kind-matching is a library fact, not a count.** A resonant layer reaches \(E_\infty\) to \(\sim 10^{-7}\) on lightly damped one-oscillator worlds and is the argmin at moderate-to-high \(R\). That is the internal-model picture qualitatively. It does not yield IMP-N60's count: isolated \(V_m\) is not the joint increment (already on Model S), and the rule over-includes at intermediate \(R\) (the MUST hybrid). At the label \(\zeta=1\), `osc_world` has poles \(-1\pm i\), not a critically damped process (standard damping \(1/\sqrt{2}\)); Kalman observer poles are real and split. One real store is *not* on \(E_\infty\); two real stores are, and they match Kalman. A conjugate-pair block collapses to \(\Omega\to 0\) because it cannot realize two different real rates.

**Cymatics (same prereg §8).** Frequency locking: the median of the seven light-damped world-medians is 0.03986 \(< 0.05\) (PASS on the aggregate statistic as written); 3/7 light worlds individually exceed 0.05. Discrete jumps under a continuous sweep: PASS — stakes, two isolated jumps in 41 points, \(C=1\to 3\to 4\); frequency at \(R=3\), one isolated jump in 31 points, \(C=2\to 3\); no chatter. The link to CT41 is a loose analogy only: piecewise-constant argmin along a continuous parameter is true of any such comparative statics, and CT41/CL19 inaction is a positive-width band from lumpy \(k>0\). At \(k=0\) the jump is exactly at the crossing. Not a test of CT41.

**Holographic / fractal check (same prereg §9; this *was* preregistered and run).** 15 scale-free Model-S worlds (scalar OU-sum, \(N=0.05\)). (1) \(K^*=J=1+\log_{10}\Gamma\) at \(R=100\) and \(R=300\): FAIL, 3/24 primary cells (only \(\Gamma=10\), \(J=2\), at \(R=300\)). (2) Equal value per layer, CV of decrements \(< 0.5\) at \(\alpha=1\): FAIL (CVs 0.996–1.984). (3) N60-from-0 equals argmin whenever \(\varepsilon\) is convex: PASS, 90/90; all 15 worlds convex, unproved. One store takes almost all of the value; extra modes do not pay at \(R\le 300\). The fail is honest in-model at \(N=0.05\) and the locked \(R\). It does not test a spatial or high-dimensional MERA / holographic picture (a stack of coarse-grainings of a many-site state). A fairer check would be a new prereg, not a re-score of these 15 worlds.

A predictive rhythm rule remains **OPEN**. No new candidate is registered. IMP-N60 stays **FAILED**; no rescue.
