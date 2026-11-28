# Preregistration: water-filling layer-count rule (WF-HSV)

**Locked:** Friday 20 November 2026, 9:55 PM ET (America/New_York), in `/workspace/gtao-wf`, beside a read-only clone of `main` at `8537f39`. Written *after* `MATH.md` and *before* any confirmation run: no reduced-order \(E_K\) optimisation on the fresh worlds, no argmin scoring, and no look at whether WF-HSV matches N60 on any multi-mode world. A one-mode implementation check against the closed-form L1 identity (MATH.md §4.4) is allowed as a unit test of the ARE / Gramian code, and is the SANITY gate below; it is not a confirmation of the rule on the test worlds.

**Hypothesis under test.** Under GTAO's keystone cost \(hK+w E_K\), the optimal layer count is discrete reverse water-filling on the joint Kalman–Bucy observer's \(H_2\) state energies (MATH.md §4.4 and §7), not Kolmogorov water-filling on peaks of \(S(\omega)\), and not isolated per-mode values (IMP-N60). The rule is stated in MATH.md §7 and repeated in §2 below.

**Status labels used later:** `in-model`, `numerical`. Nothing in this file is a result, and nothing will be marked `PROVED` unless it is actually proved.

**Excluded confirmation sets (will not be scored as evidence).** The 21 rhythm-test worlds of `theory/keystone_checks/RHYTHM_PREREG.md` / `rhythm_rule.json` (ids listed in §6); the worked example `seed2_two_light`; S5 Model S worlds with seeds 0..119 and rng stream `1000+seed` (`s5_rerun.py`); the 15 holographic/fractal worlds of the same rhythm prereg; and the 18 worlds of the later T20 fair fractal test (`/workspace/gtao-t20/core/keystone_checks/holographic_2026-11-20/`, ids `S_a05_N1e-4` … `S_a10_N1e-4_pd8`, listed in §6). Those files may be *read* only to enforce the exclusion list, to import the merged solver and the extended library, and (for T20) as a related placement diagnosis already on the record. They are not confirmation data for this rule.

---

## 0. What is already on disk at lock (readable, not a result of this test)

- `MATH.md` (this workdir), the derivation.
- Merged Model S solver: `repo/theory/layers_checks/stores.py` (guarded inversion, v2.67 / PR #116). Not modified.
- Extended library: `repo/core/keystone_checks/resonant_layers.py`. Used only after predictions are written, and only to compute argmin on fresh rhythmic and mixed worlds. Not modified.
- `repo/core/keystone_checks/s5_rerun.json`, `rhythm_rule.json`, `RHYTHM_PREREG.md`, `records/reviews/rhythm_2026-11-20/REVIEW.md`: exclusion lists and prior failed rules. Not re-scored.

No file named `RESULTS.md`, `wf_predictions.json`, or any `*DEVIATIONS*` for this test existed at lock time in `/workspace/gtao-wf` (other than this prereg and `MATH.md`).

---

## 1. Cost, library, and argmin (the thing the rule is scored against)

Cost, as in N60 / CORE.md:

\[
J(C)=C+R(E_C/E_\infty),\qquad C^*=\arg\min_C J(C),\qquad C=0\text{ allowed}.
\]

\(E_0=\mathrm{Var}(s)\). Ties (two \(C\) within \(10^{-8}\) in \(J\)) are recorded; a predicted \(C^*\) that equals either tied value counts as a match.

**Model S worlds.** Library = first-order real stores, cost \(C=K\). \(E_K\) from the merged solver `theory/layers_checks/stores.py` (`mse_given_b` / `E_K`), with the S5-style multi-start in §7 (informed grids, 2% rate separation, Nelder–Mead, L-BFGS-B, differential evolution). \(K\) ranges from \(0\) to \(J\). \(E_\infty\) from the merged Yovits–Jackson integral, also compared to the ARE value; a relative disagreement \(>10^{-3}\) is flagged, and scoring uses Yovits–Jackson (the repo's official floor) unless it exceeds a realised \(E_K\), in which case the floor is the min of the two and the flag is recorded.

**Rhythmic and mixed worlds.** Library = the extended library of `resonant_layers.py`: first-order stores at cost \(1\), resonant blocks at cost \(2\). Compositions are listed in §7. \(E_C\) from `lyapunov_mse` / `optimize_design` in that file (guards D1–D3 already in the module). \(E_\infty\) from `E_inf_YJ` in the same file, with the same floor flag as above.

The inclusion rule is not patched after seeing argmin.

---

## 2. The rule (WF-HSV)

Exactly MATH.md §7. Inputs: poles, variances, \(N\), \(R\) only, plus the unique full-order Kalman–Bucy ARE and the two Gramians of the innovations-to-\(\hat s\) map. Output: \(K^*_{\mathrm{WF}}=\#\{i:R\delta_i>1\}\), or INDETERMINATE if the numerical checks in §7 fail.

The prediction code lives at `waterfill/wf_rule.py` and must not import, call, or read any reduced-order \(E_K\) routine (`stores.E_K`, `optimize_design`, `mse_given_b` used as an optimiser, `s5_rerun.json` curves, `rhythm_rule.json` curves, T20 `run_holo.json` / `predictions.json` curves). A static check of that file is part of the tautology gate.

**Count, not placement.** WF-HSV predicts an integer \(K^*\). It does not predict the time scales (store rates) of the argmin design. In particular it does *not* predict that those rates sit on the world's process bands. (On one OU the Kalman–Bucy observer pole is at \(-b^*=-\sqrt{a^2+2av/N}\), on the fast side of the process rate \(-a\); the T20 fair fractal test found the same fast-side shift for many-mode scale-free worlds. That is a placement fact about the library, not part of this counting rule.) Observer poles may be recorded in the predictions file as a diagnostic; they are not scored.

---

## 3. Tautology checks (the test is invalid if these fail)

1. A predictions file `waterfill/wf_predictions.json` is written, and its SHA-256 recorded, *before* any reduced-order optimisation on the fresh worlds. Official start is after that write.
2. Every predicted \(K^*_{\mathrm{WF}}(R)\) in that file is a function of the world's \((A,C,Q,N)\) and \(R\) only, as recomputed by `wf_rule.predict` after lock. A full re-application must agree 100% with the file (INDETERMINATE included).
3. The prediction code's source, as hashed at lock, contains no call that computes a reduced-order \(E_K\).
4. For every determinate prediction, \(\sum\gamma_i\) agrees with \(\mathrm{Var}(s)-E_\infty^{\mathrm{ARE}}\) to the tolerance in MATH.md §7.
5. **Identity diagnostic (not a pass/fail of the rule, a pass/fail of the test's predictiveness).** After scoring, compare \(\{\delta_i\}\) (sorted decreasing) to the optimised joint decrements \(\{\varepsilon_{k-1}-\varepsilon_k\}\) on Model S worlds with \(J\ge 3\). If, on every such world, both (a) \(K^*_{\mathrm{WF}}=\) N60-from-0 at every \(R\) on the grid *and* (b) the two sequences agree entrywise to \(10^{-8}\) relative (padded with zeros if lengths differ only by trailing zeros), the rule is declared **tautological** and the confirmation gates are **NOT A TEST**. Matching *counts* without matching decrements is allowed and is a predictive success, not a tautology.

SANITY below is an L1 identity the rule is *required* to satisfy; it does not void the test.

---

## 4. Fresh worlds

All generators use `numpy` default_rng streams that are disjoint from S5's `1000+seed`. If a draw is within relative \(10^{-10}\) of any excluded world's \((a,v,N)\) (comparing sorted poles and the corresponding variances, and \(N\)), it is discarded and redrawn with a recorded bump of the stream.

### 4.1 Model S: 40 worlds, ids `ms_0000`..`ms_0039`

```
rng = numpy.random.default_rng(20261120 + 17*i)    # i = 0..39
J = int(rng.integers(3, 5))
sep = 10 ** rng.uniform(0.5, 2.0, J-1)             # factor 3 to 100
taus = numpy.cumprod(numpy.r_[10 ** rng.uniform(0, 1), sep])
v = 10 ** rng.uniform(-1.5, 1.5, J)
N = 10 ** rng.uniform(-2, 1)
a = 1/taus
```

Same *shape* as S5 (3 or 4 OU modes, separations \(\times 3\) to \(\times 100\)), new stream. R grid: `R_GRID_S = logspace(-1, 7, 161)`, the S5 grid, including the \(K^*=0\) hole. \(40\times 161=6440\) cells.

### 4.2 Rhythmic: 12 worlds, ids `rh_0000`..`rh_0011`

```
rng = numpy.random.default_rng(20261120 + 10007*(i+1))    # i = 0..11
n_osc = [1,1,1,1, 2,2,2,2, 3,3,3,3][i]
N = 10 ** rng.uniform(-1.6, -0.3)          # about 0.025 to 0.50
omegas, betas, vpoles = [], [], []
# well-separated frequencies (ratio at least 3) so the "close pair" of the
# excluded 21 is not accidentally rebuilt
omega0 = 10 ** rng.uniform(-1.5, 0.5)
omegas.append(omega0)
for k in range(1, n_osc):
    omegas.append(omegas[-1] * 10 ** rng.uniform(0.5, 1.3))
for k in range(n_osc):
    # standard damping zeta = beta / omega; light to moderately heavy, not the
    # excluded grid {0.02, 0.08, 0.25, 1.0}
    zeta = 10 ** rng.uniform(-2.0, -0.15)  # about 0.010 to 0.71
    betas.append(zeta * omegas[k])
    vpoles.append(10 ** rng.uniform(-1.2, 0.0) / 2.0)   # pole variance
# pack as conjugate pairs, repo convention (v_pole, v_pole) per oscillator
```

Ids `rh_0000`..`rh_0003` are one oscillator, `rh_0004`..`rh_0007` two, `rh_0008`..`rh_0011` three. This *regime* includes lightly damped pairs (the setting that broke N60's formula and the MUST hybrid), but the parameter draws are new.

### 4.3 Mixed: 12 worlds, ids `mx_0000`..`mx_0011`

```
rng = numpy.random.default_rng(20261120 + 20011*(i+1))    # i = 0..11
n_ou  = [1,1,1,2, 1,1,2,2, 1,2,1,2][i]
n_osc = [1,1,2,1, 1,2,1,2, 2,1,2,2][i]
N = 10 ** rng.uniform(-1.6, -0.3)
# OU modes, as in Model S but 1 or 2 of them
# oscillators, same draw as §4.2
# pack OU first (real a, v), then conjugate pairs
```

Exact pack is in `waterfill/worlds.py`, locked with this prereg.

R grid for rhythmic and mixed: `R_GRID_R = [0.5, 1, 2, 3, 5, 10, 20, 50, 100, 300, 1000]`. \(24\times 11=264\) cells. \(R=3\) is on the grid because that is the stake at which the known (excluded) counterexample failed; it is not a licence to score that counterexample.

---

## 5. Gates

All findings are `in-model`, `numerical`.

| Gate | Criterion | What a fail means |
|---|---|---|
| TAUTOLOGY (kill of the *test*) | §3 items 1–4 pass; item 5 not triggered | If 1–4 fail, stop: no confirmation is reported. If item 5 triggers, official gates are NOT A TEST. |
| SANITY (kill of the *implementation*) | On the three closed-form one-OU points in §8, WF-HSV equals N60-from-0 exactly (both \(K^*=0\) and \(K^*=1\) occur) | Code bug, not a test of the hypothesis. Fix the code, record a deviation, and only then score confirmation worlds. |
| PRIMARY Model S | Determinate predictions match argmin in \(\ge 95\%\) of the 6440 (world, \(R\)) cells. INDETERMINATE cells are excluded from the denominator and reported. | A fail means WF-HSV does not recover the class where N60 is already exact. The mapping, as translated in MATH.md §7, does not hold for the keystone. |
| PRIMARY rhythmic+mixed | Determinate predictions match extended-library argmin in \(\ge 90\%\) of the 264 cells, similarly excluding INDETERMINATE. | A fail on this gate only, with Model S a pass, means the translation works for real-pole worlds and is not the missing predictive rhythm rule. |
| COMPOSITION (report, not a kill) | On rhythmic+mixed cells that match on *cost* \(C^*\), the predicted \(C^*\) is just a count, not a module list. Report the argmin composition anyway. | — |
| HOLE | Of the Model S cells whose true argmin is \(0\), the rule predicts \(0\) in \(\ge 95\%\) of those cells. | A miss here is the N60-as-written hole repeating. |

A PRIMARY pass is not a proof. A PRIMARY fail is a fail of this rule, not a rescue opportunity. No post-data change of the threshold, of \(\delta_i\), or of the library is registered as a new result of this test.

---

## 6. Excluded world ids (rhythm test)

Rhythm-test 21: `1osc_z0.02_N0.04`, `1osc_z0.02_N0.2`, `1osc_z0.08_N0.04`, `1osc_z0.08_N0.2`, `1osc_z0.25_N0.04`, `1osc_z0.25_N0.2`, `1osc_z1.0_N0.04`, `1osc_z1.0_N0.2`, `2osc_close2_heavy_heavy`, `2osc_close2_light_light`, `2osc_close2_light_medium`, `2osc_close2_medium_medium`, `2osc_sep15_heavy_heavy`, `2osc_sep15_light_light`, `2osc_sep15_light_medium`, `2osc_sep15_medium_medium`, `3osc_heavy_heavy_heavy`, `3osc_light_light_light`, `3osc_medium_medium_medium`, `3osc_mixed`, `seed2_two_light`.

T20 fair fractal 18 (not used for confirmation): `S_a05_N1e-4`, `S_a05_N1e-6`, `S_a10_N1e-4`, `S_a10_N1e-6`, `S_a15_N1e-4`, `S_a15_N1e-6`, `M_a05_N1e-4`, `M_a05_N1e-6`, `M_a10_N1e-4`, `M_a10_N1e-6`, `M_a15_N1e-4`, `M_a15_N1e-6`, `NC_single_N1e-4`, `NC_single_N1e-6`, `NC_narrow_N1e-4`, `S_a10_N1e-3`, `S_a10_N1e-4_G5`, `S_a10_N1e-4_pd8`.

---

## 7. Solver settings (locked)

**Model S, each \(K=1..J\), each world.** Import `stores.py` from `repo/theory/layers_checks/stores.py` under a unique module name (same precaution as S5). Multi-start as in `s5_rerun.py`: informed log-grids at scales \(0.3,0.7,1.0,1.5,3.0,8.0\) of the mode rates, random starts (`n_rand=12`), 2% store-rate separation, Nelder–Mead then L-BFGS-B polish of the best, differential evolution with `de_maxiter=25` when \(K\le 4\). Seed for optimiser \(i\): `50_000 + 17*i + K`. Re-evaluate MSE at the returned rates with `mse_given_b`. No `minimum.accumulate`. Workers at nice 19.

**Rhythmic and mixed, compositions.** For a world of degree \(n\) (state dimension of the world):

- \((n_{\mathrm{res}}, n_{\mathrm{first}})=(0,0)\) (closed form, \(E_0\));
- first-order only: \((0,k)\) for \(k=1..n\);
- resonant only: \((r,0)\) for \(r=1..\lceil n/2\rceil+1\), with total cost \(2r\le n+2\);
- hybrids: \((1,1)\), \((1,2)\), and if \(n\ge 4\), \((2,1)\); if \(n\ge 6\), also \((2,2)\) and \((3,1)\).

Drop duplicates and any composition with cost \(> n+2\). Optimiser: `resonant_layers.optimize_design` with `n_rand=16`, `use_de=True`, seed `20261120 + 1000*world_index + 17*(n_res*100+n_first)` (world_index is 0..11 inside each class, plus 100 for mixed). If a composition returns non-finite \(E\), it is discarded (not used as a candidate), and the failure is recorded. Argmin is over the finite remaining compositions and \(C=0\).

---

## 8. SANITY points (analytic, one OU)

Three points, closed-form \(P=N(\sqrt{a^2+2av/N}-a)\), \(K^*=1\) iff \(R(v-P)/P>1\):

| id | \(a\) | \(v\) | \(N\) | \(R\) values |
|---|---|---|---|---|
| `sane_A` | \(0.3\) | \(1.0\) | \(0.05\) | \(0.2\), \(1.0\), \(R_*+1\) where \(R_*=P/(v-P)\) |
| `sane_B` | \(1.0\) | \(0.4\) | \(0.2\) | \(0.2\), \(1.0\), \(R_*+1\) |
| `sane_C` | \(0.02\) | \(2.0\) | \(0.1\) | \(0.2\), \(1.0\), \(R_*+1\) |

The implementation must match the closed-form \(K^*\) on all nine \((world,R)\) pairs, and must return both \(0\) and \(1\) among them (the two \(R=0.2\) points are chosen to be holes for typical \(P\); if one is not, the third \(R\) still produces a \(K^*=1\)). This may be run before lock as a unit test of the ARE code.

---

## 9. Outputs

- `waterfill/wf_predictions.json` and its SHA-256, written before official start.
- `PREREG.md` SHA-256 and timestamp, recorded in the results at lock.
- `waterfill/wf_run.json` (designs, \(E\), flags) and `RESULTS.md`: verdicts against this prereg, numbers, identity diagnostic, labels (`in-model` / `numerical`).
- A dated deviations file if and only if a solver guard, inversion, or budget change is forced during the run, written *before* official scoring of the affected cells. The inclusion rule, worlds, grids, and thresholds do not change.

No push, no merge.

A SHA-256 and timestamp of *this* file, as locked, are recorded in the results and printed at lock time. The file is not edited after lock except to correct a typo that does not change a criterion, which would itself be a dated deviation.
