# GATE FAIL

## Gate read v4: `theory/stop-copying-2026-11-25/PREREG_4.md` (fork branch `forge-stop-copying-prereg`, head `ea99183`, prelock `7b6986f`)

*This is an independent read, done Wednesday 25 November 2026 at about 15:00 ET (America/New_York). The gate spec is `process/PREREG_GATE.md` at `8c4b3c0`. I worked read-only in `<local>/gate-292`: no pushes, comments, edits or email. Nothing was run with `--execute`.*

*What I did run:*
- *both run scripts without arguments, which only prints the refusal;*
- *`--help` on the scripts;*
- *`aggregate.py` on synthetic `.out` files in `/tmp/agg`, which are not run outputs.*

*References are to `PREREG_4.md:line` unless another file is named.*

**Summary.** C1 and C2 from v3 are closed as written: the commands, redirections, paths, argparse arguments and overshoot rule all check out. One new gap is in the branch that step 0b itself creates. When T1's output is incomplete, step 0b labels T2 but not T1, and the locked `aggregate.py` command cannot then produce a T1 label. A missing or truncated T2 file has the same problem. The fix is text-only and needs no script change.

## Hashes and integrity: PASS

| Item | Result |
|---|---|
| `PREREG_4.md` | sha256 `db6e72e3e3e53542b8f8bd5c3e7606552576f8dc48cde0ac6896e9b11ad42e72`, matching `PREREG_4.sha256`. The lock `ea99183` adds only `PREREG_4.md` (+63) and `.sha256` (+1) |
| Earlier preregs and v2 scripts | `PREREG.md` `c251d8aa…cc639d9`, `PREREG_2.md` `2fb5a733…f310ef`, `PREREG_3.md` `d0d9af51…f883f0`, `run_t1_v2.py` `91f4e6e6…`, `run_t2_v2.py` `17fab3f4…` and `aggregate.py` `c065aa20…` are all unchanged. `git diff b85e30d ea99183` over those files, their `.sha256` files and `checks/` is empty |
| Prelock `7b6986f` | Adds one line to `DEVIATIONS.md` (line 6), dated 14:42 ET. It correctly describes v2 as a GATE FAIL, with B5 as a contradiction in the text. Line 5 is kept, so the file is append-only |
| Run state | No `run_t*_v2.out` or `aggregate.out` exists |

## C1: commands, redirections and working directory. CLOSED

- **Working directory** is `theory/stop-copying-2026-11-25/` (:17). The commands are :22, :30 and :36. They redirect to `checks/run_t1_v2.out`, `checks/run_t2_v2.out` and `checks/aggregate.out`. They supersede `PREREG_3.md:34-36` (:15).
- **The arguments match argparse.**
  - `run_t1_v2.py` and `run_t2_v2.py` take only `[-h] [--execute]`. Without the flag they print the refusal and exit with code 2 (checked).
  - `aggregate.py` takes two positional arguments, `t1_out` and `t2_out` (checked).
- **The paths work from that directory.**
  - Running `python3 checks/run_t2_v2.py` puts `checks/` first on `sys.path`, so `import aggregate` resolves.
  - `run_t2_v2.T1_TOTAL_PATHS` resolves through `os.path.dirname(__file__)` to `…/checks/run_t1_v2.out`, the same file T1 writes to (checked).
- **Thread variables** come before `python3` in the command, and the scripts also set them before importing numpy.
- **Step 0** uses the hash list at `PREREG_3.md:53-55`, and those lines are the three script hashes.
- **Step 0b (:25).** T2 is not started unless `checks/run_t1_v2.out` has a `TOTAL_JSON` line. If it lacks one, every T2 setting, and so the T2 test, is labeled `measurement/code`, and T-acyclic is not applicable. `measurement/code` is the top of the precedence list, and labeling this case as a protocol failure rather than a budget event is consistent with the lock. This closes the silent `t1_cpu = 0.0` path (t2:255; with the file absent it returns 0.0, as checked), as long as step 0b is followed.

## C2: rerun overshoot and reviewer relabel. CLOSED

- **The rule matches the code.** :43 restates exactly what the code does: the rerun starts only while `used() < cap` (t1:136, t2:339), its overshoot is allowed and recorded in `cpu`, and `not settled` for CPU comes from the start loop reaching the cap or from no CPU being left to start the rerun.
- **The reviewer relabel (:45).** It fires when `cpu` exceeds 720 s by more than one rerun. In practice it is vacuous, which is harmless. If the loop's last start runs past 720 s, the code already labels the setting `not settled` (t1:109, t2:312). So a setting that is otherwise settled can only go over 720 s through the rerun, and that overshoot is at most one rerun by construction. See N1.

## BLOCKING

**D1 (G1, outcome labels): incomplete run outputs leave T1, or T2, without a label.**

- **T1 incomplete.** Step 0b applies exactly when `run_t1_v2.out` is missing or has no `TOTAL_JSON` line, that is, when T1 did not finish. It then labels T2 `measurement/code`, but it gives **no label for T1 itself**.
  - It also says "`aggregate.py` is not given a missing T2 file". The only locked aggregation command (:36) needs both files, so no locked step produces a T1 label at all.
  - With a T1 file of 3 rows and no `TOTAL_JSON`, `aggregate.py` raises `ValueError: need five setting labels, got 3`. With T2 missing, it raises `FileNotFoundError`. Both were checked on synthetic files.
- **T2 incomplete.** If T1 finishes and T2 crashes partway, `aggregate.py` fails on the T2 file, and T1's label from a complete file is never printed. Nothing in the lock covers this case.
- **Why it blocks.** This repeats v1 B1(iii): an outcome with no named label. The case is unlikely, since it needs a crash, but the label is undefined.
- **Fix (text only, `PREREG_5.md`, no script change):**
  - (i) A test is labeled `measurement/code` at the test level if its `.out` file is missing, has fewer than five `SETTING_JSON` lines, or has no `TOTAL_JSON` line. Its conditional row (T-form or T-acyclic) is then not applicable.
  - (ii) If only one file is complete, the label for that test comes from `aggregate.aggregate_settings` on its five `SETTING_JSON` labels, plus `aggregate.tform` or `aggregate.tacyclic`. Lock one command for this, for example `python3 -c "import sys,json; sys.path.insert(0,'checks'); import aggregate as a; rows,_=a._parse_out('checks/run_t1_v2.out'); print(a.aggregate_settings([r['label'] for r in rows]), a.tform(a.aggregate_settings([r['label'] for r in rows]), [r.get('leader_c') for r in rows]))" > checks/aggregate.out`, and the same for T2 with `tacyclic` and `circulation`.
  - (iii) `aggregate.py` (:36) is run only when both files are complete.

## G1–G5 after PREREG_4

- The Gate rows of PREREG_2 and PREREG_3 stand (:11), and PREREG_4 changes only how the run is invoked.
- **G1:** passes apart from D1.
- **G2–G5:** pass, as in v2 and v3.
- **The stated readings** (:49-55) match the code and my v3 notes: status 2 counts as converged by intent, the low power of the half-tolerance check is stated, the guard and rerun use the lowest-J converged start, and the maxfun probe covered only (10,1).
- **Wording: PASS.**
  - None of "theory of everything", "solved", "kill", "dead", "verdict" or "puzzle".
  - "law" appears only at :5, byte-identical to `CORE.md:7`.
  - "one-way" does not appear.
  - The scope note "no ℏ, c or G" and the no-GR/QM/holography/gravity line are at :7 and :63.

## Non-blocking

- **N1.** The relabel clause at :45 is vacuous, and its fallback ("any overshoot clearly larger than one rerun") is not mechanical. Also, "relabel … before running `aggregate.py`" implies editing a run `.out` file. Better to record a relabel as a separate dated line in `RESULTS.md` or `DEVIATIONS.md` than to edit an output file.
- **N2.** The redirect `> checks/run_t1_v2.out` creates or truncates the file before T1 starts. So a crashed T1 leaves a partial file without `TOTAL_JSON`, which step 0b catches correctly. D1 covers the label for that case.
- **N3.** The scripts' refusal message still says "after the PREREG_3 Gate passes". This is cosmetic, because the binding condition is a pass on PREREG_4, which PREREG_4 :3 states.
- **N4.** The maxfun probe still covers only (10,1). This is stated at :55.

## Minimal path to a pass

Write a text-only `PREREG_5.md`, locked with its own sha256, containing D1 (i)–(iii). No script or hash changes are needed. A fresh read of PREREG_5 alone would then be enough.
