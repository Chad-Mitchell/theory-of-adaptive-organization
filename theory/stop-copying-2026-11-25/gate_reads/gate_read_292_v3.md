# GATE FAIL

## Gate read v3: `theory/stop-copying-2026-11-25/PREREG_3.md` (fork branch `forge-stop-copying-prereg`, head `b85e30d`, prelock `3ca15f7`)

*This is an independent read, done Wednesday 25 November 2026 at about 14:50 ET (America/New_York). The gate spec is `process/PREREG_GATE.md` at `8c4b3c0`. I worked read-only in `<local>/gate-292`: no pushes, comments, edits or email. Nothing was run with `--execute`, and no `run_setting()` or labeling path was called.*

*What I did run:*
- *the unit tests (`pytest test_prereg3_scripts.py`: 10 passed);*
- *label-function checks on synthetic inputs;*
- *a minimizer diagnostic of 10 single T2 starts at (10,1), with non-locked seeds and with J and A not printed. It used 6.8 CPU-s. The script and output are `gate_read_292_v3_probe.py` and `.out`, next to this file.*

*References are to `PREREG_3.md:line`, `run_t1_v2.py` (t1), `run_t2_v2.py` (t2) and `aggregate.py` (agg).*

**Summary.** B1–B6 from v2 are fixed in code as PREREG_3 states, and the maxfun worry does not hold up: no probe start stopped on `maxfun`. Two gaps remain, both in the B7 CPU and output rule. Each is a small mismatch between the locked text and the code. Both can be fixed with a text-only `PREREG_4.md`, with no script change and no new hashes.

## Hashes and integrity: PASS

| File | sha256 | Result |
|---|---|---|
| `PREREG_3.md` | `d0d9af512a3be2d99b7f54e4b028fb1ca57e28219e8e5a79bdfd72bd1af883f0` | matches `PREREG_3.sha256`. Lock `b85e30d` adds only `PREREG_3.md` (+65) and `.sha256` (+1) |
| `run_t1_v2.py` | `91f4e6e6974673715e91473bfd9593b76416b7181de1a04dec43c9de15ce40c5` | matches :53 |
| `run_t2_v2.py` | `17fab3f4191f86454f4889f6ca3c6e76d042d8faccd82b914cf8d84a8ecaef2f` | matches :54 |
| `aggregate.py` | `c065aa20b318d789dad2e8f6b3f894d28688320fe44cc4b53791f470c240d648` | matches :55 |
| `PREREG.md` | `c251d8aa…cc639d9` | `git diff cde05b9 b85e30d` is empty |
| `PREREG_2.md` | `2fb5a733…f310ef` | `git diff 7ba0d32 b85e30d` is empty, and the same holds for both `.sha256` files |

Other integrity checks:
- The `checks/` diff between `3ca15f7` and `b85e30d` is empty.
- The v1 scripts are untouched.
- No `run_t*_v2.out` exists.
- `DEVIATIONS.md:5` records the supersession and "no scored number has been seen".

## B1–B7 from v2: are they fixed in code as PREREG_3 states?

| v2 item | PREREG_3 states | Code | Result |
|---|---|---|---|
| **B1** T2 settled | :19. After a dihedral map, A_e must agree within 0.01. Orientations are compared only where both A_e > 0.02. Every pair of starts must match | t2:163-192 (`dihedral_match`, `pairwise_settled`), :325-326 | **Fixed.** Five copies of the reciprocal ring with 1e-7 noise now count as settled (`pairwise_settled` gives True). That is the case that failed in v2 |
| **B2** per-setting precedence | :21. Compute every flag, then return the highest-precedence label | agg:15-21, :35-76. Flags are built at t1:167-174 and t2:371-378 | **Fixed.** Example: not settled + guard-hit + hit returns `guard-hit`. The guard and half-tolerance checks use the lowest-J start among the best-value converged starts, or the lowest-J start overall if there are none (t1:131-132, t2:334-335). See N4 |
| **B3** relative tolerance | :23. \|J − J\*\| ≤ 1e-6·\|J\*\| | t1:23-25, t2:195-196 | **Fixed** |
| **B4** maxfun and exit status | :25. maxfun 25000 for T1 and 8000 for T2. Record status, nit and nfev. A start that stops on the limit is excluded | t1:44, :84, :34-39, :96-104; t2:50, :287, :199-204, :299-307 | **Fixed.** SciPy stops when `sf.nfev > maxfun`, and `sf.nfev` counts finite-difference evaluations (confirmed in the probe: nfev ≈ 37 × nit). Status 2 ("ABNORMAL" line search) still counts as usable, which follows the lock (N2) |
| **B5** one "broken" threshold | :27. Broken means A_e > 0.12 | agg:26, :135-145; t2:63, :369, :392 | **Fixed** |
| **B6** aggregation | :29 | agg:79-132, :160-184; 10 unit tests pass | **Fixed.** Example: four hits and one clean miss give `mixed`, and four clean misses and one not settled give `not settled` |
| **B7** CPU rule | :31-39 | t1:16-17, t2:16-17 (thread variables set before numpy); per-setting cap t1:57-58, t2:258-259; rerun t1:136-152, t2:339-354; total t1:216-223, t2:419-430 | **Partly fixed.** See blockers C1 and C2 |

## The point you asked me to press: can most T2 starts hit maxfun 8000?

On this probe, no.

- **Setup.** At (10,1) I ran 8 uniform starts (seed 424242, not a locked seed) and 2 near-uniform starts (seed 777). They used the exact v2 options: `ftol` 1e-12, `gtol` 1e-8, `maxiter` 5000, `maxfun` 8000. I also ran the half-tolerance rerun on two of them.
- **Exit statuses.**
  - 9 of 10 stopped with status 0 ("CONVERGENCE: RELATIVE REDUCTION OF F").
  - 1 of 10 stopped with status 2 ("ABNORMAL"), which counts as usable.
  - **None stopped on `maxfun` or `maxiter`.**
- **How close to the limit.** nfev ranged from 1575 to 5525 (20–69% of 8000), and nit from 47 to 153. CPU per start was 0.21–0.80 s, mean about 0.59 s.
- **Projected CPU per setting.** That is about 576 × 0.59 s ≈ 5.7 CPU-min, under the 12-min cap. Even if every start hit `maxfun`, the setting would take about 8000 × 0.14 ms × 576 ≈ 10.8 CPU-min. The 0.14 ms per evaluation is what I measured; PREREG_3 assumed 0.122 ms, giving 9.4 min. Either way it is under the cap, but the margin depends on the machine.
- **Conclusion.** A "not settled by construction" result is not supported at (10,1). This is 10 starts at one setting. (3,1) and (30,1) were not probed (N1).

## The 2 CPU-hour total in code vs the lock

- **What is locked.** At most 2 CPU-hours in total, and 12 CPU-min per setting (PREREG_2 :44, PREREG_3 :39).
- **What the code does.**
  - T1 sets `remaining = 7200 − total` (t1:217-223).
  - T2 sets `remaining = 7200 − t1_cpu − total` (t2:424-430), and each setting's cap is `min(720, remaining)`.
  - Because 10 × 720 = 7200, the total cap never binds before the per-setting caps do, so `not run (budget)` is effectively unreachable. That matches the lock.
- **But.** `t1_cpu` comes from `run_t1_v2.out` (t2:65-67, :247-255), and the locked command never writes that file (C1). The cap check also allows an unflagged overshoot by the rerun (C2).

## BLOCKING

**C1. The locked invocation does not produce the files that the protocol and the code read.**

- **What is missing.** PREREG_3 :34-36 runs `python3 run_t1_v2.py --execute` and `python3 run_t2_v2.py --execute` with no output redirection. Both scripts print to stdout.
- **What reads those files.**
  - PREREG_3 :57 names the outputs as `checks/run_t1_v2.out` and `checks/run_t2_v2.out`.
  - `aggregate.py run_t1_v2.out run_t2_v2.out` (:36) needs both files to exist.
  - `run_t2_v2.read_t1_cpu()` returns **0.0 silently** if `run_t1_v2.out` is missing (t2:255). T2 then assumes the full 2 hours remain, and the cross-script total is not enforced.
- **Fix (text only, `PREREG_4.md`).** Lock the commands as:
  - `… python3 run_t1_v2.py --execute > run_t1_v2.out`
  - `… python3 run_t2_v2.py --execute > run_t2_v2.out`
  - plus a step 0b: before T2 starts, confirm that `run_t1_v2.out` contains a `TOTAL_JSON` line; if not, do not start T2.

**C2. The rerun's CPU overshoot is never flagged, contrary to the locked text.**

- **What the lock says.** PREREG_3 :39 says "The half-tolerance rerun is counted inside each setting's 12 CPU-minute cap". PREREG_2 :44 says "A setting that goes over the cap is `not settled`".
- **What the code does.** It starts the rerun only if `used() < cap` (t1:136, t2:339), and never checks `used()` again afterwards. If the start loop ends just under 720 s, the rerun (about 0.2–1.1 s for T2) pushes the setting's `cpu` over 720 s. The setting still gets its hit or clean-miss label. The impact is small, but the code differs from the locked rule.
- **Fix (text only, `PREREG_4.md`).** Restate the rule to match the code:
  - "The rerun is started only while CPU remains under the cap. Its own overshoot, at most one rerun, is allowed and recorded in `cpu`. A setting is `not settled` for CPU only if the start loop reaches the cap or no CPU remains for the rerun."
  - Alternatively: if the reported `cpu` is over 720 s, the post-run reviewer relabels that setting `not settled` before running `aggregate.py`.

## G1–G5 after PREREG_3

The Gate rows of PREREG_2 stand unchanged (:13).

- **G1:** passes. The new route to `not settled` (starts that stop on a limit) does not, on the probe, make that label likely, so the odds of 0.05 are still plausible.
- **G2–G5:** pass, as in v2.
- **Wording:** passes.
  - None of "theory of everything", "solved", "kill", "dead", "verdict" or "puzzle".
  - "law" appears only at :5, byte-identical to `CORE.md:7`.
  - "one-way" appears at :7, where it is reserved, and at :47, which quotes the old comment.
  - The scope note "no ℏ, c or G" and the no-GR/QM/holography/gravity line are at :9 and :65.

## Non-blocking

- **N1.** The maxfun probe covers only (10,1). The other settings probably need a similar number of iterations, but this is not shown. An optional 5-start check at (3,1) and (30,1), the same way, would cost about 10 CPU-s.
- **N2.** Status 2 ("ABNORMAL" line search) counts as converged, which follows the lock (only status 1 or a limit stop is excluded). It was 1 in 10 in the probe. It would be good to say in PREREG_4 that this is intended.
- **N3.** The half-tolerance check has almost no power. In both probe reruns, halving `ftol` and `gtol` from the same start reproduced the same trajectory (identical nit and nfev), so `measurement/code` will almost never trigger. This is inherited from PREREG §3 and not a lock defect. A later prereg could use a perturbed start or a different finite-difference `eps`. The rerun's own exit status is not checked either.
- **N4.** PREREG_3 :21 says the guard and half-tolerance checks use "the lowest-J start". The code uses the lowest-J start among the best-value converged starts, and the lowest-J start overall only when there are none. A limit-stopped start with a lower J would be skipped. PREREG_4 can state the code's reading.
- **N5.** PREREG_3 :3 and `DEVIATIONS.md:5` describe v2 as passing the PREREG_2 text (a "GATE PASS on the PREREG_2 text"). v2 was a GATE FAIL overall, and its B5 was a contradiction in the text. An appended line could correct this.
- **N6.** `test_prereg3_scripts.py` (`8d461f4a…`) is not hash-listed. That is fine, since it is not binding.

## Minimal path to a pass

Write a text-only `PREREG_4.md`, locked with its own sha256. It should lock the redirections and step 0b (C1), and restate the rerun overshoot rule (C2). N2 and N4 can be folded in as stated readings. No script changes and no new hashes are needed. A fresh read of PREREG_4 alone would then be enough.
