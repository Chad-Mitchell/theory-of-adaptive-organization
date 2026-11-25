# Preregistration addendum: v2 run-script fixes (appended to PREREG_2.md, before any run)

*Wednesday 25 November 2026 (America/New_York). Branch `forge-stop-copying-prereg`. Append-only update to `PREREG_2.md` (lock `7ba0d32`, sha256 `2fb5a73386211ce732b9e32c2ed9e0082bc8aec913334b274bfaf506d9f310ef`, untouched) and to `PREREG.md` (lock `cde05b9`, sha256 `c251d8aa9c38f7230b996f241d6564423386d077d559b5cca2eee7bfbcc639d9`, untouched). `checks/run_t1.py` and `checks/run_t2.py` are also untouched. It answers the 7 blocking items (B1–B7) of the independent gate read v2 of PR #292 (`gate_read_292_v2.md`), which found that the PREREG_2 text itself passed G1–G5. Gate per draft PR #263 (`process/PREREG_GATE.md` at `8c4b3c0`). Locked in its own commit with `PREREG_3.sha256`. **Nothing in T1, T2, T-form or T-acyclic runs until a fresh independent reader passes this Gate.** In-model only: no real-world data. `THEORY.md`, `CORE.md` and the locked blobs are not edited. The model, the five settings, the design box, the seeds and the scored bars \(A>0.12\) / \(A_{(5)}>0.12\) are unchanged.*

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

(Byte for byte from `CORE.md:7`.) Labels as in `PREREG.md` and `PREREG_2.md`. A break with \(A\ge0.10\) is called **asymmetric**, not "one-way": \(A=0.10\) is a copy-rate ratio of about \(1.22\).

**Scope, as in `PREREG.md`.** A hit does not give \(\hbar\), \(c\) or \(G\). Nothing here derives general relativity, quantum mechanics, holography or gravity.

## Gate

The T1, T2, T-form and T-acyclic rows of `PREREG_2.md` stand, with the script and label rules below. C1–C5 are unchanged and are not re-run. The v2 scripts are the binding implementation of those rows.

## 1. Script defects and the fixes (B1–B7)

Each item cites `gate_read_292_v2.md`. `checks/run_t1.py` and `checks/run_t2.py` stay as locked in `PREREG_2.md` and are not used for a run. The v2 scripts and `aggregate.py` replace them.

**B1. T2 settled check.** `run_t2.py:129,134` compared orientations on every edge with \(k\)-sum \(\ge 10^{-6}\), including edges with \(A_e\sim 10^{-7}\) whose signs are numerical noise. The uniform ring plus \(10^{-7}\) noise in the \(c\) values, the v2 probe's case, therefore failed `dihedral_match` and would have labeled the expected reciprocal clean miss (`odds 0.78`) `not settled`. The same script compared every start only to `packed[0]`, so two starts could differ by up to 0.02. **Fix, in `run_t2_v2.py`:** after a 16-element dihedral map, every \(A_e\) must agree within 0.01, and orientations are compared only on edges where **both** \(A_e>0.02\). Every pair of the \(\ge 3\) starts at the best value must match, not only a comparison with the first start. A unit test in `checks/test_prereg3_scripts.py` shows that the uniform ring plus \(10^{-7}\) noise counts as settled, and that a first-only comparison is not enough.

**B2. Per-setting precedence.** `run_t1.py` and `run_t2.py` returned `not settled` before testing `measurement/code` or the guard, against the order locked in `PREREG_2.md:40`. **Fix:** both v2 scripts compute every flag on the setting (the guard and the half-tolerance check are taken on the lowest-\(J\) start), then emit the highest-precedence label through `aggregate.setting_label`: `measurement/code` \(>\) `guard-hit` \(>\) `not settled` \(>\) `not run (budget)` \(>\) `inside-resolution` \(>\) {`hit`, `clean miss`}.

**B3. Relative tolerance.** The v1 scripts used \(10^{-6}\max(1,\lvert J\rvert)\), an absolute \(10^{-6}\) whenever \(\lvert J\rvert<1\). At the T1 reference \(J\approx 0.0715\) that window is 14 times the locked relative window. **Fix:** a start is at the best value iff \(\lvert J-J^\star\rvert\le 10^{-6}\,\lvert J^\star\rvert\).

**B4. `maxfun` and exit status.** SciPy's default `maxfun` is 15000, which in 24 dimensions binds at about 600 iterations, before the locked `maxiter` 5000, and a start that stopped on `maxfun` still counted toward settled. **Fix:** `maxiter` stays 5000. `maxfun` is locked at **25000** for T1 (consistent with `maxiter` at 5 evaluations per iteration; worst case at the v2-probe timing is about 7 CPU-min, under the 12-min cap) and **8000** for T2 (a value consistent with `maxiter` would be 125000 and would exceed the cap; 8000 caps a setting, if every start hits `maxfun`, at about 9.4 CPU-min at the probe timing of 0.122 ms/eval, leaving room for the half-tolerance rerun). Each start's `status`, `nit` and `nfev` are recorded. A start that stops on `maxfun` or `maxiter` (`status==1`, or `nfev>=maxfun`, or `nit>=maxiter`) does not count toward the best value or toward settled.

**B5. One broken-edge threshold.** `PREREG.md` used \(A_e\ge 0.10\) for "broken"; `PREREG_2.md` moved the T2 hit bar to \(A_{(5)}>0.12\); `run_t2.py` computed circulation at \(A_e\ge 0.10\). **Fix:** **"broken" means \(A_e>0.12\)** everywhere (the resolved side of the T2 bar), including T-acyclic's circulation (all eight edges broken, all with the same sign) and `n_broken`. The scored T2 bar itself is unchanged: a hit is still \(A_{(5)}>0.12\) at all five settings. **Odds are unchanged** (T2: hit 0.12, clean miss 0.78, mixed 0.05, not settled or guard-hit 0.05, total miss 0.88; T-acyclic, given a T2 hit: acyclic 0.70, circulation 0.30). The threshold change does not require new odds: it only aligns T-acyclic's word "broken" with the T2 hit bar already locked in `PREREG_2.md`, whose odds already took the move from \(0.10\) to \(0.12\) as a drawing from the miss mass (gate read v2, N3).

**B6. Aggregation.** The v1 scripts printed per-setting dictionaries and did not form the test-level label. **Fix:** `checks/aggregate.py` reads the v2 `.out` files and applies `PREREG_2.md:38-42`: a test is a hit only if all five settings are hits, a clean miss only if all five are clean misses, otherwise the highest-precedence label present, and `mixed` when the five settings are some combination of hits and clean misses only. T-form is a hit only if T1 is a hit and the leader's \(c<0.10\) at all five settings; T-acyclic is a hit only if T2 is a hit and every setting is acyclic (a circulation at any setting is a miss). Unit tests in `checks/test_prereg3_scripts.py` cover these rules on synthetic inputs.

**B7. CPU rule.** The v1 scripts set `OMP_NUM_THREADS=1` after importing numpy, so OpenBLAS never saw it; the half-tolerance rerun was measured after `used`; the 2 CPU-hour total was not enforced in code. **Fix:** the binding invocation, after this Gate passes, is

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 run_t1_v2.py --execute
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 run_t2_v2.py --execute
python3 aggregate.py run_t1_v2.out run_t2_v2.out
```

from `theory/stop-copying-2026-11-25/checks/`. The v2 scripts also set those three variables before importing numpy. The half-tolerance rerun is counted inside each setting's 12 CPU-minute cap. T1 writes `total_cpu` in `TOTAL_JSON`; T2 subtracts it from the 2 CPU-hour total and will label a setting that never starts `not run (budget)`. CPU is `time.process_time()`.

## 2. Non-blocking items

**T-form resolution band.** There is none. The locked rule in `PREREG_2.md:19` stands: given a T1 hit, the row hits if the leader's \(c<0.10\) at all five settings, and misses if the leader's \(c\ge 0.10\) at any of the five. No `inside-resolution` band is added on that \(c\).

**Per-setting re-seeding.** Each setting re-creates `default_rng` from the locked seed (`20261125` for T1; `20261126` and `20261127` for T2). All five settings therefore draw the same uniform starts, and T2 draws the same structured-start perturbations, with only the cost \((w,w_x)\) changing. `PREREG.md` §3 does not say otherwise; this is the intended reading, now stated.

**"Acyclic chain".** The structured-start comment in `run_t2_v2.py` is "acyclic chain with judge 0 a leader", matching `PREREG_2.md:78`. The v1 comment "one-way chain" is not repeated in the new script.

## 3. Hash-locked v2 scripts (not executed)

The scripts below are committed in the parent of this lock and are not executed in that commit or in this one. They refuse to search unless invoked with `--execute`, which is allowed only after a fresh independent reader passes this Gate. Their sha256 sums, of the blobs committed immediately before this lock:

- `checks/run_t1_v2.py`: `91f4e6e6974673715e91473bfd9593b76416b7181de1a04dec43c9de15ce40c5`
- `checks/run_t2_v2.py`: `17fab3f4191f86454f4889f6ca3c6e76d042d8faccd82b914cf8d84a8ecaef2f`
- `checks/aggregate.py`: `c065aa20b318d789dad2e8f6b3f894d28688320fe44cc4b53791f470c240d648`

Step 0 of any later run is to confirm `sha256sum -c` on those three files against this list, then invoke under the shell command in §1 B7. A change to any of them after this lock is a dated line in `DEVIATIONS.md` and a new hash; it is not a silent edit. Outputs, after a Gate pass and after the scripts have been hash-checked, are `checks/run_t1_v2.out` and `checks/run_t2_v2.out`.

## 4. Scoring

As in `PREREG_2.md` §4, applied to the labels produced by `aggregate.py`. No status change is claimed here. The BICAUSAL row changes only after an independent review of a run.

## 5. What this does not do

As in `PREREG.md` §5 and `PREREG_2.md` §5. It does not run T1, T2, T-form or T-acyclic. It does not use real data. It does not derive \(\hbar\), \(c\), \(G\), general relativity, quantum mechanics, holography or gravity. It does not move a CLAIM_MAP row.
