# Preregistration addendum: locked invocation and rerun-overshoot rule (appended to PREREG_3.md, before any run)

*Wednesday 25 November 2026 (America/New_York). Branch `forge-stop-copying-prereg`. Append-only, text-only update to `PREREG_3.md` (lock `b85e30d`, sha256 `d0d9af512a3be2d99b7f54e4b028fb1ca57e28219e8e5a79bdfd72bd1af883f0`, untouched). `PREREG.md`, `PREREG_2.md`, and every script and hash listed in `PREREG_3.md` are also untouched: no script is changed and no new script hash is added. It answers the 2 blocking items (C1, C2) of the independent gate read v3 of PR #292 (`gate_read_292_v3.md`), which found B1–B6 fixed in code as `PREREG_3.md` states, and a maxfun probe at \((w,w_x)=(10,1)\) in which 0 of 10 T2 starts hit a limit. Gate per draft PR #263 (`process/PREREG_GATE.md` at `8c4b3c0`). Locked in its own commit with `PREREG_4.sha256`. **Nothing in T1, T2, T-form or T-acyclic runs until a fresh independent reader passes this Gate.** In-model only: no real-world data. `THEORY.md`, `CORE.md` and the locked blobs are not edited.*

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

(Byte for byte from `CORE.md:7`.) Labels and scope as in `PREREG.md`, `PREREG_2.md` and `PREREG_3.md`. A hit does not give \(\hbar\), \(c\) or \(G\). Nothing here derives general relativity, quantum mechanics, holography or gravity.

## Gate

The T1, T2, T-form and T-acyclic rows of `PREREG_2.md`, as amended by `PREREG_3.md`, stand. This file changes only the invocation, the T2 start condition, and the CPU-overshoot rule. C1–C5 are unchanged and are not re-run.

## 1. C1: the locked commands, with redirections

`PREREG_3.md:34-36` named the scripts and their real arguments (`--execute`; `aggregate.py` then the two `.out` files) but did not redirect stdout. The v2 scripts print to stdout. `run_t2_v2.read_t1_cpu()` reads `checks/run_t1_v2.out` next to the script and returns 0.0 silently if that file is missing, so the cross-script 2 CPU-hour total would not be enforced. This section supersedes the un-redirected command block in `PREREG_3.md:34-36`.

Working directory: `theory/stop-copying-2026-11-25/`. After a fresh independent reader passes this Gate, and after Step 0 (`sha256sum` of the three scripts against the list in `PREREG_3.md:53-55`):

**T1.**

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 checks/run_t1_v2.py --execute > checks/run_t1_v2.out
```

**Step 0b, before T2.** Do not start T2 unless `checks/run_t1_v2.out` contains a `TOTAL_JSON` line. If that file is missing, or exists but has no `TOTAL_JSON` line, T2 is not invoked. Every T2 setting, and so the T2 test, is then labeled `measurement/code`: a missing total is a protocol or crash failure (including T1 starting and not finishing), not a CPU-budget event. `aggregate.py` is not given a missing T2 file; the T2 test label is recorded as `measurement/code` and T-acyclic is not applicable.

**T2**, only if Step 0b passes:

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 checks/run_t2_v2.py --execute > checks/run_t2_v2.out
```

**Then aggregate**, with its output redirected:

```
python3 checks/aggregate.py checks/run_t1_v2.out checks/run_t2_v2.out > checks/aggregate.out
```

The arguments are the scripts' real arguments, the same ones as `PREREG_3.md:34-36`, with paths written from this working directory. The v2 scripts also set the three thread variables before importing numpy, as already locked. CPU remains `time.process_time()`.

## 2. C2: the rerun overshoot, as the code implements it

The v2 scripts start the half-tolerance rerun only while `used() < cap` (12 CPU-minutes, 720 s) and do not re-check the cap after the rerun. The rerun may therefore push a setting's recorded `cpu` over 720 s by at most one rerun. **That overshoot is allowed and is recorded in `cpu`.** A setting is labeled `not settled` for CPU by the scripts only if the start loop reaches the cap, or if no CPU remains to start the rerun, as the code already does.

If a setting's recorded `cpu` exceeds 720 seconds by more than one rerun's measured time, the post-run reviewer relabels that setting `not settled` before running `aggregate.py`. (The v2 out files record the setting's total `cpu`, not the rerun alone; the reviewer uses the duration of that setting's half-tolerance rerun when it can be measured, and otherwise any overshoot clearly larger than one rerun.)

## 3. Non-blocking items, stated

**Status 2 counts as converged, by intent.** A start with SciPy L-BFGS-B `status==2` ("ABNORMAL" line search) is not a `maxfun` or `maxiter` stop. Under `PREREG_3.md` B4 only a limit stop (`status==1`, or `nfev>=maxfun`, or `nit>=maxiter`) is excluded from the best value and from settled. Status 2 therefore counts as converged. The v3 probe had 1 such start in 10.

**The half-tolerance check has low power.** This is inherited from `PREREG.md` §3 and is a stated limitation, not a new lock. In the v3 probe, halving `ftol` and `gtol` from the same start reproduced the same trajectory, so `measurement/code` will almost never trigger. The rerun's own exit status is not checked. A later prereg may use a perturbed start or a different finite-difference step; this file does not change the check.

**Guard and rerun start.** `PREREG_3.md:21` said "the lowest-\(J\) start". The code uses the lowest-\(J\) start among the best-value **converged** starts, and the lowest-\(J\) start overall only when there are none. A limit-stopped start with a lower \(J\) is skipped. This file adopts the code's reading.

**The maxfun probe covered only \((10,1)\).** On 10 T2 starts at that setting, with the locked options and non-locked seeds, 0 hit `maxfun` or `maxiter` (9 status 0, 1 status 2; nfev 1575–5525). That does not, by itself, speak for \((3,1)\) or \((30,1)\).

**Correction to the description of gate read v2.** `PREREG_3.md:3` and `DEVIATIONS.md:5` (the 14:24 ET line) mis-describe that read as a pass on the PREREG_2 text. Gate read v2 was a GATE FAIL. Its B5 was a contradiction in the PREREG_2 text (two definitions of a broken edge). The other v2 blockers were in the run scripts. Those two earlier lines are not edited. The correction is this paragraph and the dated line appended to `DEVIATIONS.md` in the parent of this lock.

## 4. Scoring and what this does not do

Scoring remains `PREREG_2.md` §4 as amended by `PREREG_3.md`, applied to the labels produced by `aggregate.py` after any reviewer relabel under §2. No status change is claimed here.

This file does not change any script or hash. It does not run T1, T2, T-form or T-acyclic. It does not use real data. It does not derive \(\hbar\), \(c\), \(G\), general relativity, quantum mechanics, holography or gravity. It does not move a CLAIM_MAP row.
