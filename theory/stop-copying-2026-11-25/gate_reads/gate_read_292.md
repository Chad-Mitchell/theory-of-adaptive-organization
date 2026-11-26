# Gate read: `theory/stop-copying-2026-11-25/PREREG.md` (fork branch `forge-stop-copying-prereg`, head `cde05b9`)

*This is an independent paper read, done Wednesday 25 November 2026 at about 13:58 ET (America/New_York). The gate spec is `process/PREREG_GATE.md` at `8c4b3c0` (draft PR #263), applied as written. I worked in a fresh clone at `<local>/gate-292`. Nothing was pushed, edited, commented or emailed. I ran no global search, and I did not run T1 or T2. I made only paper and one-point checks: the paper scripts in `checks/`, a KKT check at the best symmetric design, and a closed-form leader–copier slice on the cap. The script and output are `gate_read_292_local.py` and `.out`, next to this file.*

References are to `PREREG.md:line` unless another file is named.

## GATE FAIL

There are two blocking items, B1 and B2 below. Both are about scoring and labels, not physics, and each is fixed with a short append-only `PREREG_2.md`. The model, the paper attempts and the rival gap would pass. Once B1 and B2 are fixed, a fresh read of `PREREG_2.md` only should be enough.

### Integrity checks (all PASS)

- **Hash.** `sha256sum PREREG.md` = `c251d8aa9c38f7230b996f241d6564423386d077d559b5cca2eee7bfbcc639d9`. This matches `PREREG.sha256`, and the blob at `cde05b9` hashes the same.
- **Lock commit.** `cde05b9` (13:13:52 ET) adds only `PREREG.md` (+86 lines) and `PREREG.sha256` (+1). The `checks/` files are in the parent `078413e` (also 13:13:52 ET), and there is no diff to `checks/` between the two. There is no `run_t1.py` or `run_t2.py` and no run output. Git proves order only (:3).
- **Paper scripts re-run.** NumPy 2.5.4 and SciPy 1.18.1 on the box. `python3 paper_two_judge_sweep.py` matches `paper_two_judge.out` byte for byte, and `python3 paper_ring.py` matches `paper_ring.out` byte for byte. Note: `paper_two_judge.out` is the output of `paper_two_judge_sweep.py`, not of `paper_two_judge.py`. The latter's own `__main__` (w=10 only, heat and RI at λ=1) prints different lines, and those are not committed.
- **Closed form (C5).** I checked by hand that Σ_sym = D/(γ(1−c²))[[1,c],[c,1]], L = 2D/(γ(1+c)), and J_tot = (D/γ)[4w/(1+c) + 2w_x/(1−c²)], so the condition is w(1−c)² = w_x·c. The root at (10,2) is 0.64174. That gives 0.6417 at :19 and 0.6418 in `.out:3`; this is rounding, not an error. J at (10,1) is 0.18464, which matches.
- **C1 (detailed balance).** With D·I noise, detailed balance holds iff the drift is symmetric, i.e. γ_A·c_A = γ_B·c_B. This agrees with PR #287 `PREREG_2.md:36`, and A = 0 there exactly (:37).

## G1. Miss: PASS on miss named and odds; FAIL on locking (see B1)

- **T1 (:20).** The hit is A ≥ 0.10 at all five settings. The miss is A < 0.10 at all five, or a mixed result, or `not settled`, or `guard-hit`. The odds 0.10 / 0.80 / 0.05 / 0.05 sum to 1.00, so the total miss odds are 0.90.
- **T2 (:21).** The hit is at least 5 of 8 edges with A_e ≥ 0.10, at all five settings. The odds 0.12 / 0.78 / 0.05 / 0.05 sum to 1.00, so the miss odds are 0.88. Neither is near 0, so the G1 stop condition ("odds of a miss about 0") is not met.
- **Paper support for the miss odds (my one-point check).** I took the obvious one-way corner: both judges on the cap, leader at c_A = 0, copier at c_B. In closed form, J = γc²/2 + (1/γ)[2w(2 − c + c²/2) + w_x(2 + c²/2)]. Its best value is 0.2829 at (10,1), against 0.1846 symmetric, and 0.0943 at (3,1), against 0.0715. Away from detailed balance, the heat grows like γ·(asymmetry)², while the rest of the cost falls like 1/γ. So a one-way basin has to pay off at a low γ. This makes 0.90 / 0.88 look honest, and the hit odds of 0.10 / 0.12 look generous rather than low. It is not a proof, so G2 still holds.
- **Locking: FAIL (B1).**
  - (i) :20 and :79 disagree on whether a near-bar hit (0.10 ≤ A ≤ 0.12) is "resolved".
  - (ii) There is no precedence rule when the five settings land in different categories, and the G5 next step depends on which category is chosen.
  - (iii) The budget-exhaustion outcome is not defined for T2, and the budget numbers do not add up (5 × 30 CPU-min = 150 > 120).
  - Details are under B1.

## G2. Not an identity: PASS for T1 and T2; C1–C5 correctly fenced as CONSISTENCY_CHECK

- **C1–C5 (:15-19).** Each is an identity, labeled `CONSISTENCY_CHECK` in its row and logged only:
  - C1: detailed balance.
  - C2: nonnegative entropy production.
  - C3: exchange and dihedral symmetry.
  - C4: P_D = 0 in a classical model.
  - C5: closed form on the symmetric set.
- **T1 and T2 (:20, :21).** These are global minima of 4- and 24-parameter non-convex, stability-constrained costs with no closed form. The paper attempts are §2.2 (:55-57) and §2.3 (:59-61).
- **(a) Is the "one step past the cap" caveat (:57) adequate? Partly.**
  - The conclusion holds: the symmetric design is a strict local minimum.
  - The quoted evidence does not hold up. `antiH` (`paper_two_judge.py:33-40`, h = 1e-3) evaluates lnγ_A = 5.001, which is outside the box. The small eigenvector there is mostly the lnγ-antisymmetric direction: (δlnγ, δc) ≈ (−0.81, 0.59) at (10,1) and (−0.87, 0.49) at (3,1). So the "smallest eigenvalue 0.105 at w=3" cited in the G2 cell (:20) and at :57 is the curvature of a direction you cannot move in.
  - The correct check at a corner is KKT:
    - First, the one-sided ∂J/∂lnγ_i must be strictly negative for each judge. I get −0.0890, −0.0963, −0.1081, −0.0381 and −0.2477 at the five settings. :57 claims this, but no committed `.out` shows it for two judges.
    - Second, the Hessian must be positive on the critical cone, which here is the (c_A, c_B) block with lnγ held on the cap. Its eigenvalues are {0.468, 297.1}, {0.395, 297.0}, {0.357, 297.0}, {0.105, 296.9} and {1.588, 297.9}. The small one is the symmetric c direction (J_sym''/2). The antisymmetric c curvature is about 594 along (δ, −δ).
  - So the result is a strict local minimum at all five settings, more robustly than stated. The caveat gives the right direction of the argument, but it reports the wrong numbers as evidence and leaves the gradient claim without committed output. Non-blocking: N1.
- **(b) Ring (:61).**
  - Checking only the 16 copy-gain directions is the correct second-order check, not a gap. All eight lnγ_i sit on the cap with strictly negative one-sided gradients (`paper_ring.out:1-5`, max −0.043 to −0.346). With strict complementarity, the critical cone is exactly the c-block. I reproduced its smallest eigenvalues: 0.2598, 0.2753, 0.2953, 0.0947, 0.7567.
  - The miss odds of 0.88 do not rest on that check. The check is local, and the 0.12 hit odds ("more ways to pattern a break", :61) are a guess. That is stated honestly as "Local only", so it is acceptable under G1. The G1 stop condition is about miss odds near 0, not about grounding. See N2.

## G3. Named rival: PASS (on R1 and the A = 0 null); R2 and R3 are readings, not derived

- **What passes.** Every rival predicts A = 0 (:20, :65). The bar is 0.10, the resolution 0.01, and the resolved threshold |A − 0.10| > 0.02. That passes, carried by R1 together with the simplest null: the detailed-balance set, on which A = 0 exactly (:37, C1).
- **(e) Do the rival values follow from the stated models?**
  - **The common reason is wrong.** The reason given for A = 0 is "exchange-symmetric" (:20, :21). It does not follow, and the prereg's own C3 (:17) says why: a symmetric cost can have a broken minimum that comes with its mirror image. Exchange symmetry gives a symmetric set of minimizers, not a symmetric minimizer.
  - **R1 (RI, Sims 2003).** Its A = 0 rests on the same kind of local check as ours: a symmetric best at c = 0.0036 / 0.0009 / 0.0002 with positive antisymmetric eigenvalues (`.out:6-8`). That check uses the same past-cap h step, and its two-judge cap-side gradient is not shown either. As a rival it is a local reading, with the same status as our own 0.10 residual. It is acceptable as a "simplest null"-level rival.
  - **R2 (Bialek, Nemenman and Tishby 2001).** Predictive information is the mutual information between the past and future of one time series. The prereg gives no two-judge design problem built from it. "Stated value A = 0 (both keep copying each other)" (:20) is not stated by BNT and is not computed (:65 admits "not computed here"). It is our reading, not their prediction.
  - **R3 (Kalman–Bucy 1961).** The KB filter is the MMSE estimator for a given linear-Gaussian plant. Here each judge's "plant" is the other judge's closed loop, which is not the KB setting. Symmetric gains would follow only if a unique symmetric fixed point were shown, and the prereg does not show one. "Stake elasticity 0" does hold, because the MMSE gain does not depend on the scale of a quadratic loss.
  - These problems do not stop G3, because R1 and the null carry it. The wording should change: N3.
- **DOIs (Crossref api.crossref.org, checked this session). All three resolve with matching metadata:**
  - 10.1016/S0304-3932(03)00029-1: Sims, "Implications of rational inattention", *J. Monetary Econ.* 50(3):665–690, 2003.
  - 10.1162/089976601753195969: Bialek, Nemenman, Tishby, "Predictability, Complexity, and Learning", *Neural Computation* 13(11):2409–2463, 2001.
  - 10.1115/1.3658902: Kalman, Bucy, "New Results in Linear Filtering and Prediction Theory", *J. Basic Eng.* 83(1):95–108, 1961.

## G4. Reach: PASS

- **Level and route.** The outcome is a toy setup (level (a), :9), with a route to level (b) through cited lines that exist and fit:
  - `CORE.md:80` ("When the memory also steers the world …").
  - `OPEN_WORK.md:147` (the BICAUSAL row).
  - `OPEN_WORK.md:247` (the work order asks for "conditions for treating those as one object, and a counterexample where they are not").
  - `measurement/CLAIM_MAP_v2.md:894` (BICAUSAL, open).
- **The framing is a little loose.** The work order's counterexample is about joining the heat account, the design response and the boundary into one object. "Symmetric closure" is a reading of it. Acceptable.
- **Row status.** No row moves before an independent review of the run (:81, :86).

## G5. Next step: PASS

- **Hit (:20):** BICAUSAL gets a counterexample, and §1.3 is checked.
- **Clean miss:** closure in this family is reciprocal, heat separates from RI by copy level, and the next prereg tries an asymmetric ingredient (unequal T, delay, P_D > 0).
- **Open misses:** logged with their location.
- **T2 (:21):** a hit gives an ordering and the secondary result; a miss means reciprocal closure scales to eight judges.
- The steps differ, so G5 passes, but only once B1 fixes which category a mixed-setting outcome lands in.

## Point-by-point on (a)–(g)

- **(a)** See G2: the conclusion holds and the evidence is mislabeled (N1).
- **(b)** See G2: the c-block is the correct critical cone, and the 0.88 is an honest but ungrounded prior (N2).
- **(c)** Yes, stated at :31 ("a **modeling choice** … not derived from `CORE.md`"), as in PR #287 `PREREG_4.md:39`. Two small slips:
  - It is a quadratic *penalty* standing in for CORE's variance/ruin *cap*. :31 calls it "a variance cap".
  - "Without it the symmetric pair at c → 1 has no steady state" is imprecise. Without it the symmetric optimum runs to the c = 0.999 guard, because J_sym falls monotonically in c.
  - Also, the clean-miss reading at :20 G5 should carry "with this excursion term". See N4.
- **(d)** Not fully locked. See B1. The "settled" rule (:71) is nearly complete. One gap: "those starts agree" can mean the 3 starts that reach the best value or all starts that do (N5). Guard-hit (:72) is clear. The lower box edge lnγ = −3 is covered as attainable by :33. Precedence between guard-hit, not settled, `measurement/code` and clean miss across settings is missing (B1). The 2 CPU-hour rule cannot be enforced as written (B1(iii)).
- **(e)** See G3: R1 is a local reading, R2 and R3 are not derived, and all three DOIs are correct.
- **(f)** §1.3 (:45-47) is conditional, has a threshold (leader c < 0.10 at all five), odds 0.6, and adds no point (:79). That much is clean. But it is "reported as hit or miss" with no Gate row: no label, no G3 rival, no G5. The T2 acyclic secondary (:21, :43, :80) is the same. See B2. The "Reason (paper)" claim that a leader at c = 0 pays zero heat is an identity (x_A is an autonomous OU process with variance D/γ, so γ²·D/γ − Dγ = 0). It is correctly presented as a reason, not as a test.
- **(g)** Wording: PASS.
  - None of "theory of everything", "solved" (it appears only inside "resolved"), "kill", "dead", "verdict" or "puzzle".
  - "law" appears only at :5, byte-identical to `CORE.md:7` (diff empty).
  - The HYPOTHESIS and PAPER labels are used (:7, :20, :21, :45). No item is labeled OBSERVED. The PR #287 facts at :33 and :47 could carry it (N6).
  - No claim to derive GR, QM, holography or gravity (:9, :86).
  - The scope note "A hit does not give ℏ, c or G" is at :9 and repeated at :86.

## BLOCKING

**B1 (G1 and G5): the outcome labels contradict each other and do not cover every case.**

- (i) **The resolution band is contradictory.** :20 (G3 cell) says "resolved iff |A − 0.10| > 0.02 at all five". :79 says "T1 resolved (hit, or clean miss with |A − 0.10| > 0.02 at all five)", which reads as any hit (A ≥ 0.10) being resolved. A = 0.11 at all five is a resolved hit worth 1 point under :79 and unresolved under :20. Values in [0.08, 0.10) have no named label either.
- (ii) **Precedence across settings is missing.** Take 4 settings with a clean miss and 1 that is `not settled`, or 1 guard-hit and 4 hits. Nothing says which category the test gets, and G5 gives different next steps for each.
- (iii) **The budget rule is incomplete.** At :74, 5 × 30 CPU-min per T1 setting is 150 min, more than the 120 total. T2 has no per-setting cap. There is no label for "budget ran out before or during T2". "CPU-hour" is not defined (process time or wall time, and BLAS threads).

**Minimal fix in `PREREG_2.md`**, append-only and locked with its own sha256 before any run:

1. "Resolved" means |A − 0.10| > 0.02 at all five settings, for both hit and miss (for T2, the same rule per edge). Any setting inside the band is labeled `inside-resolution` (open miss, 0).
2. Label each setting first, then aggregate with this precedence: `measurement/code` > `guard-hit` > `not settled` > `inside-resolution` > {hit, clean miss}. A test is a hit (or clean miss) only if all five settings are; otherwise it takes the highest-precedence label present, and `mixed` is used when only hit and clean-miss settings are present.
3. Budget per setting: T1 ≤ 12 CPU-min and T2 ≤ 12 CPU-min (5 × 24 = 120). Measure CPU with `time.process_time()` summed over processes, with `OMP_NUM_THREADS=1`. A setting that goes over is `not settled`. A setting not reached is `not run (budget)` (open miss, 0).

**B2 (gate coverage): §1.3 and the T2 acyclic secondary are reported as hit or miss without a Gate row.**

`PREREG_GATE.md` §2–3 (`8c4b3c0`:13-28) admits a hit/miss outcome only as a `TEST` that passed G1–G5. §1.3 (:45-47, :79) and the acyclic secondary (:21, :80) have G1 content (threshold and odds) but no label, no named rival (G3) and no next step (G5).

**Minimal fix in `PREREG_2.md`.** Add two Gate rows labeled `TEST (conditional, 0 points)`.

- **§1.3 row:**
  - G1: miss if leader c ≥ 0.10 at any of the five, given a T1 hit; odds 0.4.
  - G2: "global minimizer; not fixed by the zero-heat identity".
  - G3: the rival "both copy, unequally" (leader c ≥ 0.10).
  - G4: as T1.
  - G5: a hit means BICAUSAL names "stop copying" as the form; a miss means the break is a graded asymmetry.
- **Acyclic row:**
  - G3: the rival is circulation (all eight same sign).
  - G5: a hit means a chain or source/sink order; a miss means a circulating order, followed by a prereg on the circulation current.
- **Alternative:** relabel both as "described, not scored" and drop the words "hit or miss".

## NON-BLOCKING

- **N1 (a).** In the addendum, replace the two-judge local evidence with the KKT form: the per-judge one-sided ∂J/∂lnγ_i and the (c_A, c_B) block with lnγ held on the cap (numbers in G2 above). Commit a `.out` for it. Say that the eigenvalues at :20 and :57 come from a smooth extension past the cap and are not feasible curvatures. Apply the same fix to the R1 local check (`.out:6-8`).
- **N2 (b).** The 0.12 vs 0.10 hit odds have no grounding beyond intuition. My on-cap leader–copier slice (G1) suggests that, if anything, the hit odds are generous. Consider a one-line paper estimate, for example the best one-way chain on the cap against the uniform design.
- **N3 (e).** Reword R1–R3: "our A = 0 reading; exchange symmetry alone does not imply it (C3)". Mark R2 and R3 as not computed and not stated by their authors. Keep R1 and the detailed-balance null as the scored rival.
- **N4 (c).** Wording at :31: w_x·E[x²] is a penalty standing in for a variance cap, not a cap. Fix the "no steady state" sentence. Add "with this excursion term" to the clean-miss reading.
- **N5 (d).** "Settled" (:71): say "every start within 1e-6 of the best agrees on A within 0.01". For T2, name the 16-element dihedral matching. "Unstable designs cost +∞" (:69) can break L-BFGS-B line searches. The paper scripts use 1e9; lock one.
- **N6 (g).** Label the PR #287 open-miss facts (:33, :47) as OBSERVED. Also, "one-way" for A ≥ 0.10 overstates: A = 0.10 means k_B/k_A ≈ 1.22, so both judges still copy. Use "asymmetric (A ≥ 0.10)" in T1, T2 and G5, and keep "one-way / stop copying" for §1.3.
- **N7.** File naming: `paper_two_judge.out` comes from `paper_two_judge_sweep.py`. Say so in a header line, or rename the file in a new commit.
- **N8.** The run scripts are written after the gate (:75). The gate is a paper read, so this is allowed, but step 0 of the run should be a hash-lock of `run_t1.py` and `run_t2.py` before they execute.
