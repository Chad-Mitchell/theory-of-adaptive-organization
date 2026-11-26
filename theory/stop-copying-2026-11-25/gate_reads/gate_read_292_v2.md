# GATE FAIL

## Gate read v2: `theory/stop-copying-2026-11-25/PREREG_2.md` (fork branch `forge-stop-copying-prereg`, head `7ba0d32`, prelock `8870982`)

*This is an independent paper read, done Wednesday 25 November 2026 at about 14:25 ET (America/New_York). The gate spec is `process/PREREG_GATE.md` at `8c4b3c0`. I worked read-only in `<local>/gate-292`: no pushes, comments, edits or email. T1 and T2 were not run. `minimize()` was never called, and neither script was run with `--execute`.*

*My probes called only the scripts' cost and label functions: `edge_A`, `dihedral_match`, `a5` and timing of `Jtot`. They are in `gate_read_292_v2_probe.py` and `.out`, next to this file. References are to `PREREG_2.md:line` unless another file is named.*

**Summary.** The PREREG_2 text fixes v1's B1 and B2 on paper. G1–G5 pass for T1, T2, T-form and T-acyclic, apart from B5 below. The hash-locked run scripts, though, do not implement the locked rules exactly. One defect (B1) would turn the most likely T2 outcome, a reciprocal clean miss with odds 0.78, into `not settled`. PREREG_2 :36 locks the settled rule "as implemented in `checks/run_t2.py`", so the defect is now part of the locked rule. Every fix needs a `PREREG_3.md` with new script hashes and a dated line in `DEVIATIONS.md`.

## 1–3. Hashes and integrity: PASS

1. **PREREG_2.md.** `sha256sum` gives `2fb5a73386211ce732b9e32c2ed9e0082bc8aec913334b274bfaf506d9f310ef`. This matches `PREREG_2.sha256` and the blob at `7ba0d32`. The lock commit `7ba0d32` (14:05:00 ET) adds only `PREREG_2.md` (+90) and `PREREG_2.sha256` (+1).
2. **PREREG.md** still hashes to `c251d8aa9c38f7230b996f241d6564423386d077d559b5cca2eee7bfbcc639d9`, ending `…cc639d9`.
   - `git diff cde05b9 7ba0d32 -- PREREG.md PREREG.sha256` is empty.
   - The blob id is `f40133d3…` at both commits.
   - PREREG_2 :3 quotes the full, correct hash. A different tail in the author's report would be an error in the report, not in the file.
3. **Run scripts.**
   - `run_t1.py` = `63669dde9293c920a5878d22791e769583031174ae0ce1f4708103ba409daa33`.
   - `run_t2.py` = `c72d8c596400446d0b8ab15235f90d586e51bf6d09d7dcc5446a4a0fd15d2b91`.
   - Both match PREREG_2 :75-76, and the blobs are the same at `8870982` and `7ba0d32`.
   - The `checks/` diff between `8870982` and `7ba0d32` is empty.
   - `gate_read_292_local.py` and `.out` are byte-identical to the copies I kept.
   - No `run_t*.out` exists, and no `--execute` run is recorded.

## 4. Do the run scripts implement PREREG + PREREG_2?

### What matches

| Item | Locked text | Script | Result |
|---|---|---|---|
| Settings | PREREG :35 | t1:20, t2:21 | match |
| Box and tolerances | PREREG :33, :41, :69; ftol 1e-12, gtol 1e-8, maxiter 5000 | t1:21, :25; t2:28, :40 | match (see B4 on maxfun) |
| Seeds | T1 `20261125`; T2 `20261126` and `20261127` | t1:22; t2:24-25 | match. Each rng is re-seeded per setting, so all five settings use the same start set. PREREG §3 does not say otherwise (N1) |
| Start counts | 256 + 4 structured; 512 + 4×16 | t1:23-24, :93-94; t2:26-27, :152-176 | match. The patterns match PREREG_2 :78 |
| Unstable cost | 1e9 (PREREG_2 :46); uniform starts redrawn | t1:26, :78-86; t2:29, :139-144 | match |
| Guard | PREREG_2 :29 | t1:138; t2:225-227 | match |
| Half-tolerance check | 0.005 on A / A_(5) | t1:127-136; t2:217-224 | match |
| Labels hit / inside / clean miss | A > 0.12, \|A − 0.10\| ≤ 0.02, A < 0.08; "no copying" counts as 0 | t1:68-75; t2:110-115 | match |
| A_(5) | fifth-largest, undefined edge = 0 (PREREG_2 :36) | t2:104-107 | match |
| Dihedral map | 8 rotations + 8 reflections; a reflection reverses edges and flips sign | t2:128-135 | the index map is correct (edge i goes to −i−1 mod 8, and k→ swaps with k←) |
| `--execute` gate | PREREG_2 :73 | t1:153; t2:247 | match |
| CPU via `process_time` | PREREG_2 :44 | t1:91, :98; t2:181, :190 | match (see B7) |

### Gaps, all treated as blockers as requested, most severe first

**B1 (severe). The T2 "settled" check compares edge orientations on edges that are not broken.**

- **Problem.** `dihedral_match` (t2:129, :134) requires `oa == roll(ob)` exactly, on every edge. `edge_A` (t2:95-100) gives every edge with k-sum ≥ 1e-6 an orientation of ±1, including edges where A_e ≈ 1e-7.
- **Probe.** I took the uniform design at (10,1) and added 1e-7 noise to the c values. That gives max A_e ≈ 4e-7 and orientations that are effectively random, for example `[1,1,1,1,-1,1,1,1]` against `[-1,1,1,1,-1,1,-1,-1]`. `dihedral_match` returns **False**.
- **Consequence.** Starts that converge to the same reciprocal minimum within optimizer noise would fail the match. That would label the expected clean miss (odds 0.78) `not settled`. The test then cannot give the result it is most likely to give.
- **A related flaw.** Starts are compared only to `packed[0]` (t2:210-215), so two starts can differ by up to 0.02. T1 uses the range instead (t1:120).
- **Fix (PREREG_3 + `run_t2` v2).**
  - Compare orientation only on edges where both A_e > 0.02.
  - Require every pair of the ≥3 starts at the best value to match: the A_e within 0.01 after dihedral matching, and the orientations on those edges.
  - Hash the new script, and add a DEVIATIONS line.

**B2. The per-setting precedence in the scripts contradicts the locked order.**

- PREREG_2 :28-34 and :40 put `measurement/code` > `guard-hit` > `not settled`. The `measurement/code` and `guard-hit` definitions (:28-29) do not require a setting to be settled.
- Both scripts return `not settled` (t1:105-123; t2:197-215) before they test `measurement/code` or the guard. A setting that both fails to settle and hits the guard comes out `not settled` instead of `guard-hit`. That changes the test label under :42, and with it the G5 "location".
- **Fix.** State in PREREG_3 that the precedence applies within a setting too. In v2 of both scripts, compute every flag (taking the guard and the half-tolerance check on the lowest-J start) and emit the highest-precedence label.

**B3. "relative 1e-6" is implemented as an absolute 1e-6 when |J| < 1.**

- t1:110 and t2:202 use `1e-6*max(1, |J|)`. Every T1 best J (0.07–0.49) and most T2 values (0.34–1.03) are below 1. At J = 0.0715 the window is 1e-6, against the locked relative window of 7.2e-8, which is 14 times looser.
- **Fix.** Use `abs(j-best) <= 1e-6*abs(best)` in v2. Or lock "absolute 1e-6 for |J| < 1" in PREREG_3 as a stated deviation.

**B4. L-BFGS-B `maxfun` is not locked, and for T2 it binds before `maxiter`.**

- SciPy's default `maxfun` is 15000. In 24 dimensions a finite-difference gradient takes 25 evaluations, so a start can take at most about 600 iterations, not the locked 5000. Starts that stop at `maxfun` return without converging, but they still count toward "best value" and "settled".
- At about 0.11 ms per T2 evaluation (probe), a start that hits `maxfun` costs about 1.7 CPU-s. If many starts do, 576 of them would be about 16 CPU-min, over the 12-min cap. A rough typical estimate is about 3 CPU-min, under it. T1 is cheap: about 0.06 ms per evaluation and about 0.2 CPU-min per setting.
- **Fix.** Lock `maxfun` explicitly, either 15000 or a value consistent with `maxiter`. Record each start's `r.status` and `r.nit`, and exclude starts that stopped on `maxfun` from the "≥3 at the best value" count, or report them.

**B5. Two definitions of a "broken" edge (a PREREG vs PREREG_2 contradiction).**

- PREREG :21 and :43 say "broken" means A_e ≥ 0.10. PREREG_2 :18 defines the T2 hit by A_e > 0.12. T-acyclic (:20) uses "broken" without saying which threshold.
- The script computes circulation with `a >= BAR` = 0.10 (t2:232, :234).
- A T2 hit with eight edges at A_e ∈ (0.10, 0.12] on some of them is a circulation under one reading and not the other.
- **Fix.** In PREREG_3, set "broken" = A_e > 0.12 (the resolved side), and match it in `run_t2` v2. Or keep 0.10 and say so explicitly.

**B6. Aggregation across settings is not implemented.**

- Neither script forms the test-level label: hit, clean miss, `mixed`, or highest precedence (PREREG_2 :42). Neither forms T-form's "leader c < 0.10 at all five" or T-acyclic's per-setting check either. `main` only prints the per-setting dictionaries (t1:159-166; t2:252-257).
- **Fix.** Add a hashed `aggregate.py` that reads both `.out` files and applies §1 :38-42, T-form and T-acyclic. Or state in PREREG_3 that aggregation is applied by hand, exactly by :38-42, and checked by the post-run reviewer.

**B7. The CPU rule is not fully enforced.**

- **Threads.** `OMP_NUM_THREADS=1` is set inside the script after `numpy` and `scipy` are imported (t1:90, :156; t2:180, :250). The BLAS here is OpenBLAS (scipy-openblas 0.3.34), which reads that variable only when it loads, so the setting has no effect. The impact is small: `process_time` counts every thread, and 2×2 and 8×8 problems hardly use BLAS threads. But "with OMP_NUM_THREADS=1" (:44) is not actually met.
- **Uncounted time.** The half-tolerance rerun runs after `used` is measured (t1:104 against :128; t2:196 against :218), so it is outside the cap.
- **No total cap in code.** The 2-hour total is not enforced in code, only by the per-setting caps.
- **Fix.** Step 0 runs `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 run_t1.py --execute`, and the same for T2. Count the rerun inside the cap, and log the total CPU of both scripts.

### Not gaps (noted)

- The cap is checked only between starts, so one start can overshoot it. The result is still labeled `not settled` (t1:105), so the rule holds.
- `not run (budget)` can never occur, because each setting gets its own cap and every setting starts.

## 5. Do B1 and B2 from v1 now meet G1–G5? Are there new contradictions?

- **v1 B1 (labels, precedence, budget): fixed in the text.**
  - The resolution band applies to hit and to miss, through `inside-resolution` (:17, :32).
  - Precedence (:40) and aggregation (:42) are stated.
  - The budget adds up: 5×12 + 5×12 = 120 minutes, measured with `process_time` (:44).
  - G1: the miss is named and the odds are 0.90 and 0.88. G5: each label has a step.
  - The scripts break part of this (B1–B3, B6, B7 above).
- **v1 B2 (Gate rows): fixed.** T-form (:19) and T-acyclic (:20) are now `TEST (conditional, 0 points)` rows with G1–G5 filled in. Both are "not applicable" unless their parent test hits, which is clean.
- **New contradictions or gate problems.**
  - B5 (the "broken" threshold).
  - PREREG_2 :36 locks the settled rule "as implemented in `checks/run_t2.py`", which makes B1 part of the locked rule.
  - Nothing else contradicts. The superseded rows and sections (T1/T2 rows, §4, +∞ → 1e9, the 30-min cap) are named as superseded or amended (:13, :44, :46, :78, :80).
- **G2.** The paper caveat is fixed (:50-59), using the KKT numbers from my v1 read. The excursion term is reworded as a penalty (:65).
- **G3.** R1 and the detailed-balance null are now the scored rival, and R2 and R3 are relabeled as our readings (:17, :69). Pass.
- **G4.** As v1, pass.

## 6. Wording (PREREG_2): PASS

- None of "theory of everything", "solved", "kill", "dead", "verdict" or "puzzle".
- "law" appears only at :5, byte-identical to `CORE.md:7` (diff empty).
- "One-way" appears only at :7, where it is reserved for T-form.
- The HYPOTHESIS and PAPER labels are kept.
- No claim to derive GR, QM, holography or gravity (:9, :90).
- The scope note "no ℏ, c or G" is at :9 and :90.

## Non-blocking

- **N1.** T1 and T2 re-seed per setting, so all five settings use the same uniform starts. That is allowed by PREREG §3, but say so in PREREG_3.
- **N2.** T-form has no resolution band on the leader's c (:19, "No further resolution band is locked"). Consider `inside-resolution` for |c − 0.10| ≤ 0.02, for symmetry with T1. It carries 0 points either way.
- **N3.** The hit was tightened from A ≥ 0.10 to A > 0.12, but the odds are "unchanged" (:17, :18). The hit odds should drop slightly. That is honest enough, since the new labels are taken from the miss mass.
- **N4.** T2 structured starts are not checked for stability, unlike the uniform starts. All four patterns at c* ≈ 0.26–0.34 with ±0.05 perturbations are stable on paper (eigenvalues 1 − c·e^{ik}, and similar), so this is harmless.
- **N5.** A comment in `run_t2.py` (t2:161) says "one-way chain". PREREG_2 :78 says "acyclic chain". This is cosmetic.

## Minimal append-only path to a pass

Write `PREREG_3.md`, locked with its own sha256 before any run. It should:

- adopt the B1–B7 fixes;
- set the "broken" threshold (B5);
- ship `run_t1` v2, `run_t2` v2 and `aggregate.py`, with hashes listed;
- add a dated `DEVIATIONS.md` line.

A fresh read of PREREG_3 and the v2 scripts only would then be enough.
