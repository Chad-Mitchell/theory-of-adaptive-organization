# Preregistration: who copies whom, symmetry breaking in two-judge closure (physics; not run)

*Wednesday 25 November 2026 (America/New_York). Branch `forge-stop-copying-prereg`, from `main` `1eed183`. Locked in its own commit with `PREREG.sha256`. Gate per draft PR #263 (`process/PREREG_GATE.md` at `8c4b3c0`). **Nothing in T1 or T2 runs until a fresh independent reader passes this Gate.** In-model only: no real-world data is used, opened or cited as evidence. `THEORY.md`, `CORE.md` and the locked blobs are not edited. The paper scripts in `checks/` were committed before this lock; git proves order only.*

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

(Byte for byte from `CORE.md:7`.) Labels: **HYPOTHESIS** is a bet locked here. **OBSERVED** is on `main`, or in PR #287 and logged there. **PAPER** is a value computed by hand, by a closed form, or by a local check at one named point, before any run.

**Scope, stated up front.** This is a toy model we built (two and eight linear judges with thermal baths). A hit does not give \(\hbar\), \(c\) or \(G\). Nothing here derives general relativity, quantum mechanics, holography or gravity. A hit or a miss is about this model family only, at the locked settings.

## Gate

| ID | Label | G1 miss (honest odds) | G2 not an identity (paper attempt) | G3 rival: same quantity, its value, gap, resolution | G4 reach | G5 next step |
|---|---|---|---|---|---|---|
| C1 | **CONSISTENCY_CHECK** | — | Fails G2: with equal bath temperatures, the linear pair is in detailed balance iff \(\mathcal D^{-1}A\) is symmetric, i.e. \(\gamma_Ac_A=\gamma_Bc_B\) (`PREREG_2.md` §1.2 of `theory/two-route-2026-11-25/`, PR #287). On that set \(\dot Q_A=\dot Q_B=0\) | — | — | Logged only |
| C2 | **CONSISTENCY_CHECK** | — | Fails G2: at equal temperature \(kT=D\), \(\dot Q_A+\dot Q_B=kT\,\dot S_{\rm tot}\ge0\), equal to 0 iff C1 holds (nonnegative entropy production of the joint steady state) | — | — | Logged only |
| C3 | **CONSISTENCY_CHECK** | — | Fails G2: \(J_{\rm tot}\) is invariant under exchanging the judges (and under ring rotation and reflection for eight), so a broken minimum comes with its mirror images; the label "copier" is assigned from the result | — | — | Logged only |
| C4 | **CONSISTENCY_CHECK** | — | Fails G2: in this classical model a read does not disturb the read state, so \(P_D=0\) and the \(q\kappa P_D\) term of \(J=\kappa I+q\kappa P_D+wL\) is zero for every \(q\). The \(\kappa I\) term is carried by the bath heat (`CORE.md:39`) | — | — | Logged only; a model with \(P_D>0\) is a later prereg |
| C5 | **CONSISTENCY_CHECK** | — | Fails G2: on the symmetric set, \(\Sigma=\frac{D}{\gamma(1-c^2)}\bigl(\begin{smallmatrix}1&c\\c&1\end{smallmatrix}\bigr)\), heat 0, and \(J_{\rm tot}=\frac{D}{\gamma}\bigl[\tfrac{4w}{1+c}+\tfrac{2w_x}{1-c^2}\bigr]\). So the best symmetric design has \(\gamma\) at the capacity cap (cost \(\propto1/\gamma\): **the cost does not force a finite capacity; the cap is an input**) and \(c^*\) solving \(w(1-c)^2=w_xc\): 0.8000, 0.7298, 0.6417, 0.5657, 0.8333 at the five settings (`checks/paper_two_judge.out:1-5`). Stake elasticity of \(c^*\) is nonzero; a fixed-noise linear filter's gain has stake elasticity 0. The rational-inattention rival (no heat, MI rate priced) puts its symmetric best at \(c\approx0.0002\)–\(0.0036\) for \(\lambda\in\{4,1,0.25\}\) (`:6-8`) | Heat-priced \(c^*=0.73\) vs RI \(c\approx0\) at the reference; this separation is fixed by the closed form on the symmetric set, so it is not scored | — | Logged only; becomes scored only if T1 shows the joint minimum is off the symmetric set |
| **T1** | **TEST** | **HYPOTHESIS:** at the global joint minimum of \(J_{\rm tot}\) the copy flow is one-way: \(A\ge0.10\) at **all five** settings. Miss if \(A<0.10\) at all five (clean miss), mixed (`sensitivity-dependent` open miss), `not settled`, or `guard-hit` (§3). Odds: hit 0.10; clean miss 0.80; mixed 0.05; not settled or guard-hit 0.05. **Total miss odds 0.90** | The global minimum of a 4-parameter non-convex cost (stability-constrained, non-equilibrium designs allowed). PAPER (§2.2): the symmetric point is a local minimum in the antisymmetric directions at all five settings (smallest eigenvalue 0.105 at \(w=3\)); no global search was done. A one-way basin far from the symmetric point is not excluded by any formula | **R1, rational inattention without heat** (Sims 2003, doi 10.1016/S0304-3932(03)00029-1), cost \(\lambda\dot I(x_A;x_B)+wL+w_x\mathbb E[x_i^2]\): \(A=0\) (exchange-symmetric; paper local check at \(\lambda\in\{0.25,1,4\}\), `checks/paper_two_judge.out:6-8`). **R2, predictive information** (Bialek, Nemenman and Tishby 2001, doi 10.1162/089976601753195969): no heat term, symmetric functional, stated value \(A=0\) (both keep copying each other). **R3, fixed-noise linear filter** (Kalman and Bucy 1961, doi 10.1115/1.3658902): symmetric gains, \(A=0\), stake elasticity 0. Gap to our bar: 0.10. Resolution: 0.01 (resolved iff \(\lvert A-0.10\rvert>0.02\) at all five) | (b) `CORE.md:80` (memory steers the world; net learning rate under feedback) and the BICAUSAL row (`OPEN_WORK.md:147`, `:247`; `measurement/CLAIM_MAP_v2.md:894`) | Hit: BICAUSAL gets a counterexample to symmetric closure: with the heat term, the joint minimum of two identical judges is one-way, the work order's "conditions for one object" must name it, and the predicted form (§1.3) is checked. Clean miss: in this family, closure with the heat term settles on the reciprocal, detailed-balance set (C1); the heat term then separates from RI by copy level (C5), not by direction, and the next prereg looks for a break from an asymmetric ingredient (unequal temperatures, delay, \(P_D>0\)). Mixed/not settled/guard-hit: logged as open misses with location |
| **T2** | **TEST** | **HYPOTHESIS:** on the eight-judge ring, at the global joint minimum, at least 5 of 8 edges have \(A_e\ge0.10\), at **all five** settings; and (secondary, scored separately) the broken edges are **acyclic** (not all eight oriented the same way round the ring). Miss categories as T1. Odds: hit 0.12; clean miss 0.78; mixed 0.05; not settled or guard-hit 0.05. **Total miss odds 0.88.** Secondary, given a hit: acyclic 0.70, circulation 0.30 | Global minimum of a 24-parameter non-convex cost on a ring with stability constraint. PAPER (§2.3): the uniform ring design is a local minimum in the 16 copy-gain directions at all five settings (smallest eigenvalue 0.095 at \(w=3\)), with \(\gamma\) on the cap | Same rivals: R1, R2, R3 each give \(A_e=0\) on every edge (rotation- and reflection-symmetric costs, no heat term). Gap 0.10 per edge; resolution 0.01 | (b) as T1 | Hit: a one-way ordering among identical judges from the cost alone; the secondary says whether it is a chain-like ordering or a circulation. Clean miss: reciprocal closure scales to eight in this family. Others: open misses with location |

## 1. Model

### 1.1 Two judges

Each judge is the other's world. \(dx_A=-\gamma_A(x_A-c_Ax_B)\,dt+\sqrt{2D}\,dW_A\), \(dx_B=-\gamma_B(x_B-c_Bx_A)\,dt+\sqrt{2D}\,dW_B\), independent baths, both at \(kT=D=1\). Heat into judge \(i\)'s bath (Sekimoto, as in `PREREG_2.md` §1.1 of PR #287): \(\dot Q_i=\gamma_i^2\,\mathbb E[(x_i-c_ix_j)^2]-D\gamma_i\). Identical costs:

\[J_i=\dot Q_i+w\,\mathbb E[(x_i-x_j)^2]+w_x\,\mathbb E[x_i^2],\qquad J_{\rm tot}=J_A+J_B.\]

\(\dot Q_i\) is the \(\kappa I\) term (`CORE.md:39`), \(w\mathbb E[(x_i-x_j)^2]\) is \(wL\), and \(q\kappa P_D=0\) (C4). The excursion term \(w_x\mathbb E[x_i^2]\) is a **modeling choice**, the same one as `PREREG_4.md` of PR #287 (a variance cap standing in for confinement), not derived from `CORE.md`. Without it the symmetric pair at \(c\to1\) has no steady state.

**Design box (all points attainable, the lesson of the #287 open miss).** \(\ln\gamma_i\in[-3,5]\) (the upper end is a **capacity cap**, a modeling input; C5 shows the cost pushes \(\gamma\) to it), \(c_i\in[0,0.999]\), and the drift matrix must be stable. \(c_i=0\) ("stop copying") is an attainable design.

**Settings (five, all scored):** \((w,w_x)\in\{(10,0.5),(10,1),(10,2),(3,1),(30,1)\}\). Reference \((10,1)\). The \(w\) arm is the stake term; the heat term is \(\dot Q_i\).

**Measured quantity (T1).** Copy rates \(k_i=\gamma_ic_i\). One-way index \(A=\lvert k_A-k_B\rvert/(k_A+k_B)\). If \(k_A+k_B<10^{-6}\) (neither copies), \(A\) is undefined and the outcome is a clean miss labeled `no copying`. \(A=0\) is exactly the detailed-balance set (C1).

### 1.2 Eight judges

Ring \(i=0,\dots,7\). \(dx_i=-\gamma_i(x_i-c_i^+x_{i+1}-c_i^-x_{i-1})\,dt+\sqrt{2D}\,dW_i\). \(\dot Q_i=\gamma_i^2\mathbb E[(x_i-c_i^+x_{i+1}-c_i^-x_{i-1})^2]-D\gamma_i\). \(J_i=\dot Q_i+\tfrac w2\bigl(\mathbb E[(x_i-x_{i+1})^2]+\mathbb E[(x_i-x_{i-1})^2]\bigr)+w_x\mathbb E[x_i^2]\), \(J_{\rm tot}=\sum_iJ_i\). Box: \(\ln\gamma_i\in[-3,5]\), \(c_i^\pm\in[0,0.999]\), all drift eigenvalues with positive real part. Same five settings.

**Measured quantity (T2).** Edge \((i,i+1)\): \(k^{\to}=\gamma_ic_i^+\), \(k^{\leftarrow}=\gamma_{i+1}c_{i+1}^-\), \(A_e=\lvert k^{\to}-k^{\leftarrow}\rvert/(k^{\to}+k^{\leftarrow})\) (undefined if the sum is \(<10^{-6}\); counted as not broken). Orientation of a broken edge: sign of \(k^{\to}-k^{\leftarrow}\). **Circulation** iff all eight edges are broken with the same sign; otherwise **acyclic**.

### 1.3 Predicted form of a break (HYPOTHESIS, scored only after a T1 hit)

The leader stops copying: in a T1 hit, the judge with the smaller \(k\) has \(c<0.10\) at all five settings. Reason (paper): a judge with \(c=0\) is an equilibrium Ornstein–Uhlenbeck process and pays zero heat, so a one-way break lets the leader's heat vanish and puts all heat on the copier. This is the "stop copying" lead from the PR #287 A-T1‴ open miss. Odds given a hit: 0.6.

## 2. Paper attempts (before any run)

### 2.1 Symmetric set (C5)

Closed form above; checked numerically by `checks/paper_two_judge.py` (symmetric designs only): \(\ln\gamma=5.000\) and \(c^*\) as in C5 at all five settings; \(J^*_{\rm sym}=0.16845,\,0.18464,\,0.20999,\,0.07146,\,0.48513\).

### 2.2 Two judges, local check

At each best symmetric design, the \(2\times2\) Hessian of \(J_{\rm tot}\) in the antisymmetric directions \((\delta\ln\gamma_A,\delta c_A)=-(\delta\ln\gamma_B,\delta c_B)\) has eigenvalues \(\{0.468, 973.7\}\), \(\{0.395, 909.9\}\), \(\{0.357, 838.1\}\), \(\{0.105, 783.6\}\), \(\{1.586, 1006.3\}\) (`checks/paper_two_judge.out:1-5`). All positive. Caveat: \(\ln\gamma\) sits on the cap, so the \(\ln\gamma\)-antisymmetric difference uses the smooth extension one step past the cap; the feasible one-sided moves lower \(\gamma\), and \(\partial J/\partial\ln\gamma<0\) there (cost rises). This is local only. It does not exclude a distant one-way basin, for example a fast leader at \(c=0\) and a copier at lower \(\gamma\). That residual is the hit odds (0.10).

### 2.3 Eight judges, local check

Uniform design (\(\ln\gamma_i=5\), \(c_i^\pm=c\)): best \(c=0.3351,\,0.3161,\,0.2879,\,0.2603,\,0.3426\); \(J=0.92945,\,0.96497,\,1.03256,\,0.33554,\,2.75165\). The 16-dimensional copy-gain Hessian has smallest eigenvalue \(0.2598,\,0.2753,\,0.2953,\,0.0947,\,0.7567\), and every one-sided \(\partial J/\partial\ln\gamma_i\) on the cap is negative (`checks/paper_ring.out:1-5`). Local only. Hit odds 0.12 (slightly above T1: more ways to pattern a break on a ring).

### 2.4 Rivals

R1 (RI, no heat): replace \(\dot Q_A+\dot Q_B\) by \(2\lambda\dot I\), with \(\dot I=-\frac1{2\pi}\int_0^\infty\ln(1-\lvert C_{AB}(\omega)\rvert^2)\,d\omega\) the Gaussian mutual-information rate. Symmetric best \(\ln\gamma=5\), \(c=0.0036,\,0.0009,\,0.0002\) at \(\lambda=0.25,1,4\); antisymmetric eigenvalues all positive (`:6-8`). Prediction \(A=0\). R2 and R3 are exchange-symmetric functionals with no heat term; their stated prediction is \(A=0\) (both keep copying, symmetrically). They are not computed here; they are not scored against each other, only as the \(A=0\) reading.

## 3. Run protocol (locked; not run)

- **Search, T1.** Multi-start L-BFGS-B on \((\ln\gamma_A,c_A,\ln\gamma_B,c_B)\) in the box; 256 starts uniform in the box (unstable starts redrawn), NumPy `default_rng(20261125)`; plus 4 structured starts per setting: \((5,0,\ln\gamma,c)\) with \((\ln\gamma,c)\in\{(5,0.7),(3,0.9),(1,0.9),(0,0.5)\}\). `ftol=1e-12`, `gtol=1e-8`, `maxiter=5000`. Unstable designs cost \(+\infty\).
- **Search, T2.** 512 starts uniform, `default_rng(20261126)`; plus 64 structured starts per setting (16 each near: one-way chain, alternating sources and sinks, full circulation, uniform), perturbation \(\pm0.05\), `default_rng(20261127)`. Same tolerances.
- **Settled.** The best value is reached (relative \(10^{-6}\)) by at least 3 starts, and those starts agree on \(A\) (or every \(A_e\)) within 0.01 up to the symmetries of C3. Otherwise `not settled` (open miss, 0).
- **Guard-hit.** The minimizer has any \(c\) within \(10^{-3}\) of 0.999, or the smallest real part of the drift eigenvalues below \(10^{-3}\). Open miss, 0. The cap \(\ln\gamma=5\) and \(c=0\) are attainable designs, not guards.
- **Tolerance check.** Re-run the best start at half tolerances; if \(A\) moves by more than 0.005, flag `measurement/code`, not resolved (0).
- **Budget and stop rule.** At most 2 CPU-hours in total. T1 first, then T2. If T1 exceeds 30 CPU-minutes at any setting, stop that setting and log `not settled`. Nothing is re-run with new seeds or settings after a result is seen; any change is a dated line in `DEVIATIONS.md`, appended.
- **Outputs.** `checks/run_t1.py`, `checks/run_t2.py` and their `.out` files, written and committed after the gate read passes and before any run.

## 4. Scoring (§6 style)

- T1 resolved (hit, or clean miss with \(\lvert A-0.10\rvert>0.02\) at all five settings): 1 point. Mixed, `not settled`, `guard-hit`, `measurement/code`: 0. The §1.3 form is reported as hit or miss and does not add a point.
- T2 resolved, same rule per edge count: 1 point. The acyclic secondary is reported as hit or miss and does not add a point.
- The BICAUSAL row (`measurement/CLAIM_MAP_v2.md:894`) changes only after an independent review of the run: 0 until then. No status change is claimed here.
- Each scored line is written as an eight-field row in `RESULTS.md` (prediction, outcome, hit or miss, size, location, information, row moved, next step), appended only.

## 5. What this does not do

It does not use real data. It does not derive \(\hbar\), \(c\), \(G\), general relativity, quantum mechanics, holography or gravity. It does not show that any real pair of systems breaks or keeps symmetry. It does not test the hypothesis sentence on a qualified system. It does not move a CLAIM_MAP row.
