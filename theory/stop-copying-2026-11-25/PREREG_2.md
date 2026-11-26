# Preregistration addendum: scoring, labels, and paper-caveat fixes (appended to PREREG.md, before any run)

*Wednesday 25 November 2026 (America/New_York). Branch `forge-stop-copying-prereg`. Append-only update to `PREREG.md` (lock `cde05b9`, sha256 `c251d8aa9c38f7230b996f241d6564423386d077d559b5cca2eee7bfbcc639d9`, untouched). It answers the 2 blocking items (B1, B2) and the requested non-blocking items (a, c, e, g) of the independent gate read of PR #292 (`gate_read_292.md`). Gate per draft PR #263 (`process/PREREG_GATE.md` at `8c4b3c0`). Locked in its own commit with `PREREG_2.sha256`. **Nothing in T1, T2, T-form or T-acyclic runs until a fresh independent reader passes this Gate.** In-model only: no real-world data. `THEORY.md`, `CORE.md` and the locked blobs are not edited. The model, the five settings, the design box, the seeds and the hit bar \(A=0.10\) are unchanged.*

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

(Byte for byte from `CORE.md:7`.) Labels as in `PREREG.md`. In the new text below, a break with \(A\ge0.10\) is called **asymmetric**, not "one-way": \(A=0.10\) is a copy-rate ratio of about \(1.22\), so both judges still copy. "One-way" and "stop copying" are reserved for the §1.3 form (T-form).

**Scope, as in `PREREG.md`.** A hit does not give \(\hbar\), \(c\) or \(G\). Nothing here derives general relativity, quantum mechanics, holography or gravity.

## Gate

This table **supersedes** the T1 and T2 rows of `PREREG.md` and **adds** T-form and T-acyclic. C1–C5 are unchanged and are not re-run.

| ID | Label | G1 miss (honest odds) | G2 not an identity (paper attempt) | G3 rival: same quantity, its value, gap, resolution | G4 reach | G5 next step |
|---|---|---|---|---|---|---|
| **T1** (supersedes `PREREG.md`) | **TEST** | **HYPOTHESIS:** at the global joint minimum of \(J_{\rm tot}\) the copy flow is **asymmetric**: \(A>0.12\) at **all five** settings (that is \(A\ge0.10\) and \(\lvert A-0.10\rvert>0.02\)). Miss if \(A<0.08\) at all five (clean miss), or `inside-resolution`, `mixed`, `not settled`, `not run (budget)`, `guard-hit`, or `measurement/code` (§1). Odds unchanged from `PREREG.md`: hit 0.10; clean miss 0.80; mixed 0.05; not settled or guard-hit 0.05. **Total miss odds 0.90.** The new labels `inside-resolution`, `not run (budget)` and `measurement/code` are open misses taken from that miss mass; they are not given new odds | The global minimum of a 4-parameter non-convex cost (stability-constrained, non-equilibrium designs allowed). PAPER: the symmetric point is a **strict local minimum** at all five settings, by the on-cap KKT check in §2.1 (not by the past-cap eigenvalues quoted in `PREREG.md`). No global search was done. A distant asymmetric basin is not excluded by any formula | **Scored rival: R1 together with the detailed-balance null (C1).** **R1, rational inattention without heat** (Sims 2003, doi 10.1016/S0304-3932(03)00029-1): \(A=0\), resting on a **local check** at \(\lambda\in\{0.25,1,4\}\) (`checks/paper_two_judge.out:6-8`; that check uses the same past-cap step as `PREREG.md` §2.2, so it has the same status as our own residual). Exchange symmetry alone does not imply \(A=0\) (C3). On the detailed-balance set, \(A=0\) exactly (C1). **R2 and R3 are our readings of those papers, not derived from them, not computed here, and not stated by their authors**; they are not scored. Gap to our bar: 0.10. Resolution: 0.01. A setting or a test is **resolved**, for a hit and for a clean miss alike, iff \(\lvert A-0.10\rvert>0.02\); values with \(\lvert A-0.10\rvert\le0.02\) are `inside-resolution` (open miss, 0) | (b) as in `PREREG.md`: `CORE.md:80` and the BICAUSAL row (`OPEN_WORK.md:147`, `:247`; `measurement/CLAIM_MAP_v2.md:894`) | Hit: BICAUSAL gets a counterexample to symmetric closure: with the heat term, the joint minimum of two identical judges is asymmetric, the work order's "conditions for one object" must name it, and T-form is checked. Clean miss, **with this excursion term**: in this family, closure with the heat term settles on the reciprocal, detailed-balance set (C1); the heat term then separates from RI by copy level (C5), not by direction, and the next prereg looks for a break from an asymmetric ingredient (unequal temperatures, delay, \(P_D>0\)). Other labels: logged as open misses with location, under the precedence in §1 |
| **T2** (supersedes `PREREG.md`) | **TEST** | **HYPOTHESIS:** on the eight-judge ring, at the global joint minimum, the fifth-largest edge index \(A_{(5)}\) satisfies \(A_{(5)}>0.12\) at **all five** settings (equivalently, at least 5 of 8 edges have \(A_e>0.12\)). Miss categories as T1, with \(A\) replaced by \(A_{(5)}\). Odds unchanged from `PREREG.md`: hit 0.12; clean miss 0.78; mixed 0.05; not settled or guard-hit 0.05. **Total miss odds 0.88** | Global minimum of a 24-parameter non-convex cost on a ring with a stability constraint. PAPER: the uniform ring design is a strict local minimum in the 16 copy-gain directions at all five settings (`PREREG.md` §2.3; the c-block is the critical cone, gate read G2(b)), with \(\gamma\) on the cap | Same scored rival as T1 (R1 and the detailed-balance null): \(A_e=0\) and so \(A_{(5)}=0\). R2 and R3 are our readings, not scored, as in T1. Gap 0.10; resolution 0.01; resolved iff \(\lvert A_{(5)}-0.10\rvert>0.02\) | (b) as T1 | Hit: an asymmetric ordering among identical judges from the cost alone, and T-acyclic is checked. Clean miss, with this excursion term: reciprocal closure scales to eight in this family. Other labels: open misses with location, under §1 |
| **T-form** (§1.3 of `PREREG.md`) | **TEST (conditional, 0 points)** | Given a T1 hit, **HYPOTHESIS:** the judge with the smaller copy rate has \(c<0.10\) at all five settings ("stop copying"). Miss if the leader's \(c\ge0.10\) at any of the five. Odds, given a T1 hit: hit 0.60, miss 0.40. If T1 is not a hit, this row is not applicable and is not scored | The location of the global minimizer. The reason that a leader at \(c=0\) pays zero heat is an identity (an autonomous Ornstein–Uhlenbeck process), and is not the test; whether the minimizer sits there is not fixed by that identity | Rival: **both copy unequally** (a T1-style break with the leader's \(c\ge0.10\)). Gap: 0.10 in the leader's \(c\). No further resolution band is locked | (b) as T1 | Hit: BICAUSAL names "stop copying" as the form of the break. Miss: the break is a graded asymmetry, both sides still copying. Either way, 0 points |
| **T-acyclic** (T2 secondary) | **TEST (conditional, 0 points)** | Given a T2 hit, **HYPOTHESIS:** the broken edges are acyclic (not all eight oriented the same way around the ring). Miss if they form a **circulation** (all eight edges broken, all with the same sign). Odds, given a T2 hit: acyclic 0.70, circulation 0.30. If T2 is not a hit, this row is not applicable and is not scored. A T2 hit with fewer than eight broken edges cannot be a circulation and is an automatic acyclic hit | The orientation pattern of the global minimizer, not an identity of the cost (C3 only supplies the mirror images) | Rival: **circulation** (all eight edges broken, same sign). The two values are exclusive given a T2 hit | (b) as T2 | Hit: a chain or source/sink order. Miss: a circulating order, followed by a prereg on the circulation current. Either way, 0 points |

## 1. Outcome labels, precedence, budget, settled (B1)

Label each setting first, then aggregate.

**Per setting, T1.** Let \(A\) be the copy-rate index of `PREREG.md` §1.1 (\(A\) undefined, "no copying", is scored as \(A=0\)).

- `measurement/code`: the half-tolerance rerun moves \(A\) by more than 0.005.
- `guard-hit`: any \(c\) within \(10^{-3}\) of 0.999, or the smallest real part of the drift eigenvalues below \(10^{-3}\). The cap \(\ln\gamma=5\) and \(c=0\) remain attainable, not guards.
- `not settled`: fewer than 3 starts reach the best value (relative \(10^{-6}\)), or those starts that do (the \(\ge3\) starts at the best value) disagree on \(A\) by more than 0.01. \(A\) is already invariant under exchange (C3). Going over the CPU cap also yields `not settled`.
- `not run (budget)`: the setting was never started.
- `inside-resolution`: settled, not a guard-hit, not `measurement/code`, and \(\lvert A-0.10\rvert\le0.02\). Open miss, 0 points.
- `hit`: settled, not a guard-hit, not `measurement/code`, and \(A>0.12\).
- `clean miss`: settled, not a guard-hit, not `measurement/code`, and \(A<0.08\) (including `no copying`).

**Per setting, T2.** The scored quantity is the fifth-largest edge index \(A_{(5)}\), with an undefined edge (no copying on that edge) treated as 0. This is the same as "at least 5 of 8 edges have \(A_e\ge0.10\)" applied with the resolution rule per edge. Labels are as T1 with \(A\) replaced by \(A_{(5)}\). "Settled" means the \(\ge3\) starts at the best value agree on every \(A_e\) within 0.01 up to a **16-element dihedral matching** (8 rotations and 8 reflections; a reflection reverses the edge cycle and flips orientation signs), as implemented in `checks/run_t2.py`. The half-tolerance check is on \(A_{(5)}\).

**Aggregation, fixed precedence:**

`measurement/code` \(>\) `guard-hit` \(>\) `not settled` \(>\) `not run (budget)` \(>\) `inside-resolution` \(>\) {`hit`, `clean miss`}.

A test is a hit only if all five settings are hits, and a clean miss only if all five are clean misses. Otherwise it takes the highest-precedence label present. When the five settings are some combination of hits and clean misses only, the test is `mixed` (`sensitivity-dependent` open miss, 0). **Resolved** applies to a hit and to a clean miss alike: 1 point if the test is a hit or a clean miss under this rule, 0 otherwise. T-form and T-acyclic add no point.

**Budget.** At most 2 CPU-hours in total, T1 first, then T2. Each setting of T1 and of T2 is capped at 12 CPU-minutes (`5×12+5×12=120`). CPU is `time.process_time()` in the search process, with `OMP_NUM_THREADS=1`. A setting that goes over the cap is `not settled`. A setting never started is `not run (budget)` (open miss, 0). Nothing is re-run with new seeds or settings after a result is seen; any change is a dated line in `DEVIATIONS.md`, appended.

**Unstable designs.** The cost of an unstable design is the finite value \(10^9\) (the paper scripts' value), not \(+\infty\), so that L-BFGS-B line searches remain defined. Unstable uniform starts are redrawn, as in `PREREG.md`.

## 2. Paper caveat (a, c) and rivals (e)

### 2.1 On-cap KKT check (replaces the evidence, not the conclusion, of `PREREG.md` §2.2)

The conclusion stands: the best symmetric design is a strict local minimum at all five settings. The eigenvalues quoted in `PREREG.md` at the T1 G2 cell and at §2.2 (\(\{0.468,973.7\}\) and the rest, including "smallest eigenvalue 0.105 at \(w=3\)") come from `antiH` evaluated one step past the cap (\(\ln\gamma=5.001\)) and are **not feasible curvatures**. The small eigenvector there is mostly the \(\ln\gamma\)-antisymmetric direction.

The correct check at the corner is KKT, computed by the #292 gate reader in `checks/gate_read_292_local.py` and recorded in `checks/gate_read_292_local.out` (the reader's work, copied here before this lock; not a T1 or T2 run):

- One-sided \(\partial J/\partial\ln\gamma_i\) on the cap, each judge, at the five settings: \(-0.0890\), \(-0.0963\), \(-0.1081\), \(-0.0381\), \(-0.2477\) (the range \(-0.038\) to \(-0.248\)). All strictly negative, so a feasible decrease of \(\ln\gamma\) raises the cost.
- The Hessian in the \((c_A,c_B)\) block with \(\ln\gamma\) held on the cap (the critical cone): eigenvalues \(\{0.468, 297.1\}\), \(\{0.395, 297.0\}\), \(\{0.357, 297.0\}\), \(\{0.105, 296.9\}\), \(\{1.588, 297.9\}\). The small one is the symmetric \(c\) direction (\(J_{\rm sym}''/2\)). The antisymmetric \(c\) curvature along \((\delta,-\delta)\) is about 594.

So the symmetric point is a strict local minimum at all five settings, more robustly than `PREREG.md` stated. The check remains local. It does not exclude a distant asymmetric basin; that residual is the hit odds 0.10.

`checks/paper_two_judge.out` is the output of `checks/paper_two_judge_sweep.py`, not of `checks/paper_two_judge.py`.

### 2.2 Excursion term (c)

The term \(w_x\mathbb E[x_i^2]\) is a **quadratic penalty standing in for a variance cap**, the same modeling choice as `PREREG_4.md` of PR #287, not itself a cap and not derived from `CORE.md`. Without it, the symmetric optimum runs to the \(c=0.999\) guard, because \(J_{\rm tot}\) on the symmetric set falls monotonically in \(c\). (The sentence in `PREREG.md` §1.1, "Without it the symmetric pair at \(c\to1\) has no steady state", is imprecise and is replaced by this one.) The clean-miss reading in the Gate above is **with this excursion term**.

### 2.3 Rivals (e)

R1's \(A=0\) is a local reading, as in §2.1. R2 (Bialek, Nemenman and Tishby 2001) and R3 (Kalman and Bucy 1961) are our readings of those papers: they are not derived from them, not computed here, and not stated by their authors. Exchange symmetry of a cost does not imply a symmetric minimizer (C3). The scored rival is R1 together with the detailed-balance null.

## 3. Run scripts, hash-locked before they execute (N8)

The scripts `checks/run_t1.py` and `checks/run_t2.py` are committed in the parent of this lock and are not executed in that commit or in this one. They refuse to search unless invoked with `--execute`, which is allowed only after a fresh independent reader passes this Gate. Their sha256 sums, of the blobs committed immediately before this lock:

- `checks/run_t1.py`: `63669dde9293c920a5878d22791e769583031174ae0ce1f4708103ba409daa33`
- `checks/run_t2.py`: `c72d8c596400446d0b8ab15235f90d586e51bf6d09d7dcc5446a4a0fd15d2b91`

Step 0 of any later run is to confirm `sha256sum -c` on those two files against this list, then invoke with `--execute`. A change to either script after this lock is a dated line in `DEVIATIONS.md` and a new hash; it is not a silent edit. Seeds, structured starts, tolerances, the finite unstable cost \(10^9\), and the CPU caps are those of `PREREG.md` §3 as amended by §1 above. T2 structured starts (16 each, perturbation \(\pm0.05\), seed `20261127`) are: the uniform (reciprocal) design at the paper \(c^*\); a clockwise circulation; an acyclic chain with judge 0 a leader; and alternating sources and sinks. Outputs, after a Gate pass and after the scripts have been hash-checked, are `checks/run_t1.out` and `checks/run_t2.out`.

## 4. Scoring (§6 style), superseding `PREREG.md` §4

- T1 resolved (hit or clean miss, under §1): 1 point. `mixed`, `inside-resolution`, `not settled`, `not run (budget)`, `guard-hit`, `measurement/code`: 0.
- T2 resolved, same rule on \(A_{(5)}\): 1 point.
- T-form and T-acyclic are reported as hit or miss when applicable and add no point.
- The BICAUSAL row (`measurement/CLAIM_MAP_v2.md:894`) changes only after an independent review of the run: 0 until then. No status change is claimed here.
- Each scored line is written as an eight-field row in `RESULTS.md` (prediction, outcome, hit or miss, size, location, information, row moved, next step), appended only.

## 5. What this does not do

As in `PREREG.md` §5. It does not run T1, T2, T-form or T-acyclic. It does not use real data. It does not derive \(\hbar\), \(c\), \(G\), general relativity, quantum mechanics, holography or gravity. It does not move a CLAIM_MAP row.
