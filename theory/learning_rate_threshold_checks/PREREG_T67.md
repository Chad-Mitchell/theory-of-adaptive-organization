# T67 preregistration: the threshold test (learning rate vs mutual information)

*Written Monday 23 November 2026, America/New_York, against `main` `f4ec246`, BEFORE any T67 number was computed. Locked by sha256 in `PREREG_T67.sha256` (with timestamp). Specified by the independent review `HUNT_MEMO.md` section 6 (box memo, folded into `theory/LEARNING_RATE_THRESHOLD_2026-11-23.md`). Misses are puzzles to diagnose; predictions are never patched after the lock.*

> "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." (`CORE.md:7`)

## Question

Does the judge's learning rate (Horowitz-Esposito information flow into a region A, with the judge = A inside the world) lose its area form at the same power-law threshold p_c as the mutual information I(A;B), or at a different one?

## Prior exposure (disclosed)

1. The independent reviewer of the hunt memo ran an EXPLORATORY 1D check (not preregistered): ring n=600, Kac-normalised couplings r^-p, alpha=0.5, hot judge T_A=2, T_B=1, intervals L=16,32,64,128, p in {0.8,1.2,1.6,2.0,3.0}. Log-log slopes of I vs L: 0.533, 0.155, 0.02, 0.002, 0.0; of |Idot_A|: 0.443, 0.098, 0.009, 0.001, 0.0. So the 1D result is partly known in advance: both look similar and both break below p near 1. The 2D arm, the COLD drive, the larger sizes and the threshold estimator below are not exposed.
2. The writer's informal expectation before locking (reasoning only, no T67 number): for Gaussian systems I(A;B) scales like the crossing sum of P_ab^2, giving (d+1)/2; at equilibrium the gross learning term equals minus the gross forgetting term (the review's +-17.8894), which suggests the learning term inherits the (d+1)/2 tail rather than the crossing-|K| bound d+1. So the writer leans toward EQUAL. This is stated so the reader can discount it.
3. Kim, Kuwahara and Saito 2025 (PRL 134, 020402) give alpha_c=(D+1)/2 for the thermal MI area law (under power-law clustering). That is the source of P-a.

## Model (fixed)

- Lattice: periodic, d=1 ring of n sites, or d=2 torus n x n. Distance r(x,y) = minimum-image Euclidean distance.
- Couplings: J_xy = r^-p / Z(n,p) for x != y, with Z(n,p) = sum_{z != 0} r(0,z)^-p on the same torus (Kac normalisation, row sum 1). Drift matrix K = (alpha+1) I - J, alpha = 0.5 (gap: lambda_min(K) = alpha). K is symmetric and translation invariant.
- Dynamics: dx = -K x dt + sqrt(2D) dW with D diagonal (D_AB = 0, bipartite noise across every cut). kT units.
- Judge = region A; world B = rest. 1D: A = sites 0..L-1. 2D: A = L x L square at the origin.
- Drives (temperatures, diagonal D):
  - EQ: T = 1 everywhere (reference; Idot_A must be 0).
  - HOT: T_A = 2, T_B = 1 (judge hotter than world).
  - COLD: T_A = 1, T_B = 2 (judge colder than world).
  - Both non-EQ drives sit at the cut and do not cancel by symmetry.
- Steady covariance Sigma solves K Sigma + Sigma K = 2D (computed in Fourier space because K is circulant; validated against scipy, gate G1).
- Quantities, per (d, n, p, drive, L):
  - I = I(A;B) = 1/2 [ln det Sigma_AA + ln det P_AA], P = Sigma^-1 (equals 1/2[ln det Sigma_AA + ln det Sigma_BB - ln det Sigma]).
  - Idot_A = t1 + t2, with t1 = -tr(Sigma_AA^-1 K_AB Sigma_BA) (gross learning term) and t2 = -tr(D_AA M), M = P_AA - Sigma_AA^-1 = P_AB P_BB^-1 P_BA (gross forgetting term). This is the reviewed boundary-layer identity.
  - Boundary size |dA| = 2 (1D) and 4L (2D); per-boundary density y = Y/|dA|.

## Sizes and grid (fixed)

- 1D: n in {1024, 2048}. L in {8,16,32,64,128} at n=1024; {16,32,64,128,256} at n=2048 (L <= n/8).
- 2D: n in {48, 64}. L in {2,3,4,6,8,12} at n=48; {3,4,6,8,12,16} at n=64 (L <= n/4).
- p grid: 1D p = 0.6, 0.7, ..., 3.0 (25 values); 2D p = 1.1, 1.2, ..., 4.0 (30 values). Lower edge d/2+0.1 keeps out of the volume regime p < d/2; upper edge >= d+1+0.9 covers the learning-term bound threshold d+1.
- Several disorder-free "seeds of p": the grid itself. No randomness anywhere in the main run.

## Estimator for p_c (exact)

For a quantity Y in {I_EQ, I_HOT, I_COLD, |Idot_HOT|, |Idot_COLD|} (secondary, descriptive: |t1|, |t2| per drive):

1. Approach exponent on a doubling ladder (L, 2L, 4L): with y_k = Y(L_k)/|dA(L_k)|, s = log2[(y_3 - y_2)/(y_2 - y_1)]. This is the exact exponent s of y(L) = c + b L^s through three geometric points. Area form (finite boundary density) <=> s < 0; break (density grows) <=> s >= 0. For the known Gaussian MI form the expectation is s = d+1-2p on both sides of the threshold, so s has no rounding at p_c. If (y_3-y_2)/(y_2-y_1) <= 0 the ladder is non-monotone: s is undefined at that p and this is flagged (a puzzle, reported).
2. p_c = the zero crossing of s(p) by linear interpolation between consecutive grid points p_i < p_{i+1} with s(p_i) >= 0 > s(p_{i+1}). If several crossings exist, the LARGEST is p_c and all are reported. If s < 0 at every grid p, p_c is censored below (p_c < p_min). If s >= 0 at p_max, p_c is censored above (p_c > p_max). Undefined points are skipped for interpolation (neighbours bridged) and listed.
3. Ladders:
   - Primary: largest ladder at the largest n: 1D (64,128,256) at n=2048; 2D (4,8,16) at n=64.
   - Variants: 1D (32,64,128) and (16,32,64) at n=2048, (32,64,128) at n=1024; 2D (3,6,12) at n=64, (3,6,12) and (2,4,8) at n=48.
4. Error bar sigma(p_c) = half the range (max - min)/2 of p_c over primary + variants (4 values per cell). Central value = primary.
5. Descriptive only (not used for any decision): the "naive" threshold where the log-log slope of y over the primary ladder, by OLS, crosses 0.05.

## Predictions (locked)

- **P-a (primary).** p_c(I_EQ) = (d+1)/2 +- 0.15 in each d (1D window [0.85, 1.15]; 2D [1.35, 1.65]).
- **P-a' (secondary).** p_c(I_HOT) and p_c(I_COLD) in the same windows.
- **P-b.** For each d and each drive: p_c(Idot) >= p_c(I) - 0.15 (same drive, NESS I) and p_c(Idot) <= d+1+0.15 (the learning-term bound threshold).
- **P-c (no faster-than-boundary growth above threshold).** For every grid p >= d+1+0.2 the primary s for |Idot| is < 0.05, for both drives.

## Failure conditions (each is a puzzle to diagnose, not a verdict)

- F1: any p_c outside its window in P-a / P-a' / P-b (including censoring outside the window).
- F2: P-c fails (|Idot| density grows at some p above d+1+0.2).
- F3: a non-monotone ladder at the primary ladder for a decisive quantity at a grid p within 0.5 of its p_c.

## Decision rules (outcomes)

Per d and per drive, Delta = p_c(Idot) - p_c(I), sigma_Delta = sqrt(sigma_I^2 + sigma_Idot^2):
- **EQUAL**: |Delta| <= 0.15.
- **DIFFERENT**: Delta > max(0.15, 2 sigma_Delta).
- **UNRESOLVED**: 0.15 < Delta <= 2 sigma_Delta.
- **P-b MISS**: Delta < -0.15.

Global reading:
- EQUAL in all four cells (2 d x 2 drives): this route's learning-rate area form is the known mutual-information area law relabeled. Say so plainly; the angle adds bookkeeping only; stop pouring effort into it.
- DIFFERENT in both drives of at least one d, and no P-b miss: the flow of judgment's cost has its own locality class in that d (its own object). Modest odds move only; nothing here bears on G, QM or holography.
- Anything else: mixed; reported per cell with the diagnosis.

## Validation gates (code correctness; a failing gate means a code bug, fixed and logged, predictions unchanged)

- G1: Fourier Lyapunov solver vs scipy.linalg.solve_continuous_lyapunov, 1D n=64 and 2D n=8, p in {0.8, 2.5}, HOT drive: max abs difference < 1e-10.
- G2: identity t1+t2 vs central finite difference (h=1e-5) of I(A;B) along A-only dynamics dSigma = -(Pi K Sigma + Sigma K Pi) + 2 Pi D Pi: relative difference < 1e-5, same small cases.
- G3: EQ drive Idot_A: |Idot_A| < 1e-9 at every (n, p, L) in the main run.
- G4: residual max|K Sigma + Sigma K - 2D| over 8 sampled columns < 1e-9 for every solve.
- G5: Cholesky of Sigma succeeds for every solve.

## Compute

nice 19; working dir /workspace/gtao-t67 with TMPDIR there. Scripts: `run_t67.py` (main run, writes `t67_results.json` and `t67_run.out`), `learning_rate_threshold_checks.py` (fast checks for the test suite). THEORY.md is not touched.
