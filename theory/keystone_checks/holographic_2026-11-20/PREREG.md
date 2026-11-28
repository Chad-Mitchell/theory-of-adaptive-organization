# Preregistration: a fair fractal / holographic layer test (T20)

**Locked:** Friday 20 November 2026, 9:18 PM ET (America/New_York), in `/workspace/gtao-t20` on branch `t20-holographic-2026-11-20`, beside commit `aa6ab29` (the reviewed one-page core, PR #119 branch `core-page-2026-11-20`). Written *before* any optimization of store rates, any evaluation of E_K for K ≥ 1 on the worlds of this test, and any scoring. A SHA-256 of this file and of `predictions.json` will be recorded at lock time. Neither file is edited after lock except to correct a typo that does not change a criterion, which would itself be a dated deviation.

**This is a new prereg, not a re-score.** The 15 scale-free worlds of `RHYTHM_PREREG.md` §9 (N = 0.05, R ≤ 300, per_decade = 1, scalar only) are not reused, not re-fit, and not re-scored at a new R or N. That test **FAILED** its locked gates (3/24 cells at R = 100 and 300; equal-value CV failed; N60-from-0 matched). The independent review (`reviews/rhythm_2026-11-20/REVIEW.md`, item 2 of the follow-up list / Q4) asked for a *fairer* check: much smaller N, R high enough that a last-band decrement can pay (R up to 10^3–10^8), denser modes per decade, and/or a many-site / higher-dimensional construction. This file is that check.

**Hypothesis under test (may be wrong).** Under 1/f-like change — a sum of many log-spaced OU modes over several decades, or a many-channel bank of the same kind — a strongly selected design builds layers matched to the *scale bands* of the world, as many as the stakes can pay for. Concretely:

- (A) The argmin layer count K* grows roughly linearly in log R as R runs from 1 to 10^8: layers are added as stakes pay for each further scale band, not all at one threshold and not as one store that already sits on the causal floor.
- (B) At a layer count equal to the number of scale decades, the optimal store time scales are themselves log-spaced and match those bands, not a tight cluster at one rate.
- (C) N60-from-0 matches that argmin whenever ε_K is convex.

Status labels used later: `in-model`, `numerical`. Nothing in this test is `PROVED`. Field-untested.

**Prior art (verified 20 Nov 2026, same Crossref checks as `RHYTHM_PREREG.md` §9).** Vidal 2007, "Entanglement Renormalization," *Phys. Rev. Lett.* 99, 220405, doi 10.1103/physrevlett.99.220405. Swingle 2012, "Entanglement renormalization and holography," *Phys. Rev. D* 86, 065007, doi 10.1103/physrevd.86.065007. Mehta & Schwab 2014, "An exact mapping between the Variational Renormalization Group and Deep Learning," arXiv:1410.3831 (no Crossref DOI; not a journal article). The physical picture is a stack of coarse-grainings, each summarizing the layer below at a coarser scale. In a scale-free world the number of layers should grow with the log of the scale range, with each paid-for band represented by a layer. This test is an *in-model numerical analogue* in the GTAO cost J, not a test of AdS/CFT or of quantum MERA.

---

## 0. What is already on disk (readable, not a result of this test)

- Merged solver: `theory/layers_checks/stores.py` (Jacobi-scaled truncated inverse, v2.67 / PR #116). Not modified.
- Reviewer-style multi-start: `core/keystone_checks/s5_rerun.py` (`optimize_K`, `informed_inits`, `safe_log_rates` at 2% separation, Nelder–Mead, L-BFGS-B, optional differential evolution; MSE re-evaluated at the returned rates). The optimizer is reused; the worlds, N, R, and gates of S5 are not.
- Local pre-#116 `core/keystone_checks/stores.py` is not used.
- `RHYTHM_PREREG.md` §9, `RHYTHM_RESULTS.md` §8, `reviews/rhythm_2026-11-20/REVIEW.md` Q4, and `core/KEYSTONE_NOTE.md` §5 are diagnosis of the *previous* test. They justify the new N, R, density, and multi-channel arm. They are not results of this test.

No file in `core/keystone_checks/holographic_2026-11-20/` other than this prereg, the predictions file, and the runner (no E_K, no RESULTS) exists at lock time.

---

## 1. Tautology and circular-scoring check (stated up front)

A result here is only evidence for the holographic / scale-band picture if it could have failed, and if the predicted structure is not read off the same fitted curve it is tested against.

1. **Prediction C is not evidence for holography.** Given convexity of ε_K, N60-from-0 *equals* argmin_K [K + R(1+ε_K)] by a one-line argument (the same identity recorded in `core/KEYSTONE_NOTE.md` §4). A PASS on C, when every world is convex, confirms the solver and the arithmetic; it does not confirm (A) or (B). A FAIL on C, when ε is convex at the stated tolerance, is a bug or a knife-edge and is reported as such. C is scored and reported; it is not a support-for-holography gate.

2. **Predictions for (A) and (B) are not read from ε_K or from fitted rates.** Scale-band centres, the R grid, the slope window, jump caps, coverage floors, and the K at which rates are tested are computed from the *world* (τ_min, Γ, α, N, M) only, and are written into `predictions.json` before any optimize_K call. The official scoring code path does not re-estimate band centres from fitted stores, does not fit a slope and then pass a world for having "some" slope, and does not choose K after seeing which K makes the rates look log-spaced.

3. **Negative controls must not pass (A).** On a one-scale world, CT21 says K* ∈ {0, 1}. If the official (A) gate (linear growth of many layers in log R) nevertheless PASSES on NC_single or NC_narrow, the test of (A) is **INVALID** and no family is declared a pass of the holographic picture. That is the specificity check: (A) must not fire when there are no scale bands to pay for.

4. **The previous 15 worlds are not re-scored.** Changing N or R on those locked worlds after seeing their ε curves would be a rescue, not a new test.

5. **No patching after data.** If (A) or (B) fail, the fail stands. Process deviations (optimizer budget, a numerical guard, a seed typo) go in a dated `DEVIATIONS_YYYY-MM-DD.md` *before* the affected cells are treated as scored, when that is still possible. Changing a numeric gate, a band definition, or the K at which rates are tested after seeing argmin is not a deviation; it is a new, unregistered rule.

---

## 2. Cost, solver, and notation

The reduced N60 objective is used:

    J(K) = K + R (1 + ε_K),    ε_K = E_K / E_∞ − 1,    R = w E_∞ / h.

E_0 = total signal variance (act blind). E_K is the MSE of the best design with K first-order real stores from the library below. E_∞ is the causal MMSE (Yovits–Jackson on a scalar observation; the sum of exact single-OU Kalman errors on the multi-channel arm). A design with E < E_∞ − 10^{-9} and a relative gap (E_∞ − E)/max(E_∞, 10^{-18}) > 10^{-8} is a **bug**, not a result: the cell is unsecured and the SANITY gate fails.

**Scalar library (Family S).** The merged `stores.py` agent: K parallel exponential stores on one scalar observation y = s + white noise of density N, s = sum of OU modes. Gains in closed form by the guarded inverse; rates by the S5 multi-start.

**Multi-channel library (Family M).** M independent channels, each a single OU observed in its own white noise of the same density N. A K-layer design is *K shared rates* b_1, …, b_K: each channel is filtered by the bank of K first-order stores at those rates, with that channel's own optimal gains (merged `mse_given_b` on that channel's (a_m, v_m)). Copies of a layer across channels do not add to K: K is the number of distinct scale-trackers (design complexity), not M K. E_K = Σ_m MSE_m(b); E_∞ = Σ_m P_m with P_m = N (√(a_m² + 2 a_m v_m / N) − a_m). This is a many-channel scale bank, honestly scoped: it is *not* a spatially coupled MERA of a many-site field, and it is not claimed to be one. It is the tractable higher-dimensional / multi-channel variant requested by the review.

**Argmin.** Leftmost minimizer of J(K) on K = 0, …, K_cap. Two designs are co-minima if |J_a − J_b| ≤ 10^{-9} max(1, |J_a|). N60-from-0 is

    K*_N60 = #{ k ≥ 1 : R (ε_{k−1} − ε_k) > 1 }

(strict; a tie at equality is left out). It counts the 0 → 1 step and can return 0. This is *not* N60 as written in CLAIM_MAP, which starts at K = 1 and cannot return 0.

**K_cap.** K_cap = min(J, max(8, n_dec + 6)), where J is the number of modes (Family S) or channels (Family M) and n_dec = log10(Γ). For every primary world below, n_dec = 4 and J ≥ 16, so K_cap = 10. If at R = 10^8 the last computed increment still pays (R (ε_{K_cap−1} − ε_{K_cap}) > 1) and E_{K_cap} > E_∞ + 10^{-8}, the world is flagged **CENSORED** at the top of the R range; K*(10^8) is recorded as K_cap for the shape fit and the flag is reported. Censoring is not a patch and is not treated as a pass of "K* reached the number of bands."

**Convexity.** As in `s5_rerun.py`, tolerance TOL = 10^{-4} on adjacent decrements of ε (a later decrement may not exceed an earlier one by more than TOL; a decrement may not be < −TOL). Official convexity is on K = 0..K_cap.

**Optimizer seeds.** BASE_SEED = 2026112020. For world index i (0-based in the locked world table of `predictions.json`) and layer count K, seed = BASE_SEED + 1000 i + 17 K. Worlds themselves are deterministic functions of (α, Γ, per_decade, τ_min, N) or (α, Γ, M, τ_min, N); no world-level RNG.

**Solver details, Family S (and the shared-rate search of Family M).** `optimize_K` as in `s5_rerun.py`: informed grids at mode rates and log-spaced starts, 2% store-rate separation, Nelder–Mead, L-BFGS-B polish of the best starts, differential evolution with `de_maxiter=25` for K ≤ 6 and omitted for K > 6 (budget, locked here). Continuation: the K-start list also includes the (K−1)-optimum with one extra log-spaced rate inserted. Official E_K is the merged `mse_given_b` (or its channel-sum) at the returned rates. No `minimum.accumulate`.

**R grid (official).** R_i = 10^{i/2} for i = 0, 1, …, 16 (17 points, R = 1 … 10^8). This is the scoring grid for (A) and (C). A denser diagnostic grid may be written to the run file; it is not scored.

**Compute.** `nice 19`, up to 4 worker processes, wall cap about 3 hours. Order: write and hash predictions, SANITY (single-OU Kalman identity and E_0), negative controls, Family S primary, Family M primary, then secondary arms if time remains. Unfinished cells are unfinished, not passes. Partial JSON is flushed after every world.

---

## 3. Worlds

τ_min = 1 in every world. Variance is normalized to 1 (sum of mode or channel variances).

### 3.1 Family S — scalar 1/f-like OU sums (primary)

Construction: `stores.scalefree_world(alpha, span=Γ, per_decade, tau_min=1)` in the *merged* solver. τ is log-spaced in [1, Γ], v ∝ τ^{α−1}, J = max(2, round(per_decade log10 Γ) + 1), a = 1/τ. Spectrum ~ f^{−α} inside the band. All primary worlds use Γ = 10^4 (≥ 4 decades) and per_decade = 4, hence J = 17, n_dec = 4, K_cap = 10, n_bands = 4.

| id | α | N | role |
|---|---|---|---|
| S_a05_N1e-4 | 0.5 | 10^{-4} | primary |
| S_a05_N1e-6 | 0.5 | 10^{-6} | primary |
| S_a10_N1e-4 | 1.0 | 10^{-4} | primary, B-strict |
| S_a10_N1e-6 | 1.0 | 10^{-6} | primary, B-strict |
| S_a15_N1e-4 | 1.5 | 10^{-4} | primary |
| S_a15_N1e-6 | 1.5 | 10^{-6} | primary |

These are new (N, density, span) relative to §9. α = 1 is the flat-per-decade case; α ≠ 1 tilts the spectrum and is expected to shift rates toward the heavier bands.

### 3.2 Family M — multi-channel / higher-dimensional variant (primary)

M = 16 independent channels. Channel rates are log-spaced over the same four decades: τ_m = 10^{4 (m−1)/(M−1)} for m = 1..16, a_m = 1/τ_m, v_m ∝ τ_m^{α−1}, Σ v_m = 1. n_dec = 4, J = 16, K_cap = 10, n_bands = 4.

| id | α | N | role |
|---|---|---|---|
| M_a05_N1e-4 | 0.5 | 10^{-4} | primary |
| M_a05_N1e-6 | 0.5 | 10^{-6} | primary |
| M_a10_N1e-4 | 1.0 | 10^{-4} | primary, B-strict |
| M_a10_N1e-6 | 1.0 | 10^{-6} | primary, B-strict |
| M_a15_N1e-4 | 1.5 | 10^{-4} | primary |
| M_a15_N1e-6 | 1.5 | 10^{-6} | primary |

### 3.3 Negative controls (validity)

| id | construction | N | predicted |
|---|---|---|---|
| NC_single_N1e-4 | one OU, a = 1, v = 1 | 10^{-4} | K* ∈ {0, 1} for every official R; (A) must not pass; (B) is NOT A TEST; (C) scored |
| NC_single_N1e-6 | one OU, a = 1, v = 1 | 10^{-6} | same |
| NC_narrow_N1e-4 | two OU, τ = 1 and τ = 10^{0.1} ≈ 1.2589, v = 1/2 each | 10^{-4} | K* ∈ {0, 1, 2} for every official R; (A) must not pass (there are not four scale bands); (B) is NOT A TEST; (C) scored |

### 3.4 Secondary arms (reported, not in family gates)

Run if the wall cap allows, after all primary and NC cells. Same solver, same official R grid, same numeric gates applied *descriptively*.

| id | construction |
|---|---|
| S_a10_N1e-3 | Family S, α = 1, Γ = 10^4, per_decade = 4, N = 10^{-3} (intermediate noise) |
| S_a10_N1e-4_G5 | Family S, α = 1, Γ = 10^5 (five decades), per_decade = 4, J = 21, n_dec = 5, n_bands = 5, K_cap = 11, N = 10^{-4} |
| S_a10_N1e-4_pd8 | Family S, α = 1, Γ = 10^4, per_decade = 8, J = 33, n_dec = 4, n_bands = 4, K_cap = 10, N = 10^{-4} (dense packing; tests "bands, not modes") |

---

## 4. Band centres (locked from the world, before any fit)

For a world with n_dec = log10(Γ) and n_bands = n_dec (an integer in every official world):

- Mid-decade centres: c_d = τ_min · 10^{d + 1/2} for d = 0, …, n_bands − 1. With τ_min = 1 and n_bands = 4: 10^{0.5}, 10^{1.5}, 10^{2.5}, 10^{3.5}.
- Span grid at K = n_bands: g_k = τ_min · 10^{n_dec (k−1)/(n_bands−1)} for k = 1..n_bands. With n_bands = 4, Γ = 10^4: 1, 10^{4/3}, 10^{8/3}, 10^4.

Both lists are stored in `predictions.json`. Official (B) may match either list; it may not invent a third list from the fit.

---

## 5. Numeric pass / fail gates

### 5.1 Prediction (A): K* vs log R

On the 17 official R points, let k_i = argmin K at R_i (leftmost; co-minima allowed as in §2). A primary world **passes (A)** if and only if all of the following hold:

1. **Monotone.** k_{i+1} ≥ k_i for all i (non-decreasing).
2. **Growth.** k_{16} − k_0 ≥ 3 (at least three additional layers between R = 1 and R = 10^8).
3. **Gradualism.** The set {k_i} has at least 4 distinct values, and the largest step k_{i+1} − k_i is ≤ 2. (A single jump from, say, 1 to 8 is not linear growth in log R. Equal additive decrements would produce such a jump; this clause is what distinguishes "bands paid for one after another as R climbs" from "all bands pay at once.")
4. **Slope window.** Ordinary least squares of k_i on log10(R_i) yields slope b with 0.25 ≤ b ≤ 2.0 (one added layer every four decades of R, up to two layers per decade of R).
5. **Fit quality.** Mean absolute residual (1/17) Σ |k_i − (a + b log10 R_i)| ≤ 1.0, where a, b are the OLS estimates.

If a required E_K is missing (unfinished), (A) is unfinished for that world, not a pass. Censoring at K_cap is scored as written in §2; it does not relax (1)–(5).

**Family S (A) PASS:** at least 5 of the 6 primary Family S worlds pass (A).
**Family M (A) PASS:** at least 5 of the 6 primary Family M worlds pass (A).

### 5.2 Prediction (B): log-spaced rates matching scale bands

Evaluated at **K = n_bands only** (4 for every primary world), on the official fitted rates of that K, converted to time scales τ_k = 1/b_k and sorted increasing. A world **passes B-strict** if and only if all of the following hold:

1. **Log-spacing.** The spacings δ_j = log10(τ_{j+1} / τ_j) have coefficient of variation (sample std / mean, ddof = 0, over the n_bands − 1 spacings) ≤ 0.5, and the mean spacing is in [0.5 Δ, 2.0 Δ] where Δ = n_dec / (n_bands − 1) (= 4/3 for primary worlds).
2. **Coverage.** log10(τ_{n_bands} / τ_1) ≥ n_dec − 1.5 (= 2.5 for primary worlds). Stores must cover most of the world's scale range, not a tight cluster.
3. **Band match.** Let H(X, Y) be the Hausdorff distance in log10-τ between two finite sets. H({τ_k}, {c_d}) ≤ 0.75 **or** H({τ_k}, {g_k}) ≤ 0.50. (The mid-decade list and the span grid already differ by 0.5 at the ends; a design may sit on either.)

**B-tilted** (used only as a descriptive secondary on α ≠ 1 worlds): same as B-strict except CV ≤ 0.75 and Hausdorff slack 1.00 to mid-decade *or* 0.75 to the span grid. Coverage is unchanged.

**Family S (B) PASS:** both α = 1 primary worlds pass B-strict, and at least 4 of the 6 primary Family S worlds pass B-strict (α ≠ 1 is scored against B-strict for this count, not B-tilted).
**Family M (B) PASS:** both α = 1 primary worlds pass B-strict, and at least 4 of the 6 primary Family M worlds pass B-strict.

B-tilted numbers are reported and do not move a family gate. Rates at K other than n_bands, including at K*(R = 10^8), may be reported as diagnosis; they are not a gate.

### 5.3 Prediction (C): N60-from-0 matches argmin

For each world and each official R, if ε is convex on K = 0..K_cap at TOL = 10^{-4}, then K*_N60 equals the leftmost argmin, or equals the C of any co-minimizer. A world **passes (C)** if every official-R cell on which convexity holds is a match. If ε is not convex, (C) is **NOT A TEST** for that world and the non-convexity is flagged (unexpected in Model S / independent OU channels; not a holographic confirmation).

**Family S (C) / Family M (C) PASS:** every *convex* primary world in the family passes (C), and at least 5 of 6 primary worlds are convex. A C FAIL on a convex world is a flag (identity violation or solver issue), not a refutation of (A) or (B).

### 5.4 SANITY (kills the run, not the hypothesis)

- On each NC_single world, the K = 1 official E_1 agrees with the Kalman formula P = N (√(a² + 2 a v / N) − a) to absolute 10^{-8} or relative 10^{-8}, whichever is looser, and E_∞ agrees with the same P to the same tolerance (YJ vs Kalman on one OU).
- No official design has E < E_∞ under the bug rule of §2.
- E_0 equals the total variance (1.0) to 10^{-12} on every world.

If SANITY fails, results are unsecured until a process deviation records a fix, the affected cells are re-run, and scoring is repeated against the *same* locked predictions.

### 5.5 VALIDITY (negative controls)

VALIDITY **passes** if and only if:

- Both NC_single worlds have K* ∈ {0, 1} at every official R, and neither passes the (A) gate of §5.1.
- NC_narrow has K* ∈ {0, 1, 2} at every official R, and does not pass the (A) gate of §5.1.
- SANITY passed.
- (C) on the three NC worlds is a pass or NOT A TEST, not a silent fail.

If VALIDITY fails, the test of (A) is **INVALID**. Family (A)/(B) labels may still be computed and reported as numbers, but they are not declared a confirmation of the holographic picture.

### 5.6 Overall holographic result (in-model, numerical)

The holographic / scale-band picture is **SUPPORTED (in-model, numerical)** only if VALIDITY passes and Family S (A), Family S (B), Family M (A), and Family M (B) all pass.

It is **NOT SUPPORTED** if VALIDITY passes and any of those four family gates fails. Fails are diagnosed; the rule is not patched.

It is **INVALID** if VALIDITY fails.

Family (C) is reported alongside, as a consistency check.

---

## 6. Outputs (after the run)

- `predictions.json` and its SHA-256, written before any optimize_K on these worlds.
- SHA-256 of this `PREREG.md`, recorded in the results and at lock time.
- `run_holo.json` (or split checkpoints) with per-world a, v, N, E_0, E_∞, E_K, rates, methods, ε, official (A)(B)(C) numbers, censor flags.
- `RESULTS.md` — verdict vs this prereg, no new gates, honest labels.
- A dated `DEVIATIONS_*.md` only if a process deviation is required before scoring.

No push, no pull request, no edit of `CORE.md` or `KEYSTONE_NOTE.md` as part of this task (those wait on the result and on review). `/workspace/looper` is not touched.

---

## 7. What would count as the old failure mode, honestly

If, even at N ∈ {10^{-4}, 10^{-6}} and R up to 10^8, a single well-placed store still takes almost all of (E_0 − E_∞) and later decrements do not pay on the official grid, then (A) and likely (B) fail. That would be a structural finding about this problem class (scalar or independent-channel Kalman in white noise), not a reason to raise R or lower N again on the same worlds. The review already recorded that pattern at N = 0.05 and R ≤ 300; this test asks whether it was an artifact of those locked numbers and of a sparse, scalar construction.
