# Preregistration addendum: labels for incomplete run outputs (appended to PREREG_4.md, before any run)

*Wednesday 25 November 2026 (America/New_York). Branch `forge-stop-copying-prereg`. Append-only, text-only update to `PREREG_4.md` (lock `ea99183`, sha256 `db6e72e3e3e53542b8f8bd5c3e7606552576f8dc48cde0ac6896e9b11ad42e72`, untouched). `PREREG.md`, `PREREG_2.md`, `PREREG_3.md`, and every script and hash listed in `PREREG_3.md` are also untouched: no script is changed and no new script hash is added. It answers the one blocking item (D1) of the independent gate read v4 of PR #292 (`gate_read_292_v4.md`), which found C1 and C2 from v3 closed as written. Gate per draft PR #263 (`process/PREREG_GATE.md` at `8c4b3c0`). Locked in its own commit with `PREREG_5.sha256`. **Nothing in T1, T2, T-form or T-acyclic runs until a fresh independent reader passes this Gate.** In-model only: no real-world data. `THEORY.md`, `CORE.md` and the locked blobs are not edited.*

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

(Byte for byte from `CORE.md:7`.) Labels and scope as in `PREREG.md` through `PREREG_4.md`. A hit does not give \(\hbar\), \(c\) or \(G\). Nothing here derives general relativity, quantum mechanics, holography or gravity.

## Gate

The T1, T2, T-form and T-acyclic rows of `PREREG_2.md`, as amended by `PREREG_3.md` and `PREREG_4.md`, stand. This file names the test-level label when a run `.out` file is missing or incomplete, locks the one-file aggregation commands, replaces the reviewer-relabel clause of `PREREG_4.md:45`, and notes a cosmetic refusal string. C1–C5 are unchanged and are not re-run.

## 1. D1: a complete file, or `measurement/code`

A run `.out` file is **complete** if it exists, contains at least five `SETTING_JSON` lines, and contains a `TOTAL_JSON` line. Otherwise it is incomplete (missing, truncated, or finished without a total).

If a test's `.out` file is incomplete, that test is labeled `measurement/code` at the test level, and its conditional row is not applicable: T-form when the file is T1's, T-acyclic when the file is T2's. This includes the Step 0b case in `PREREG_4.md` (T1 incomplete, T2 not started): T1 and T2 are both `measurement/code`, and both conditional rows are not applicable.

Working directory remains `theory/stop-copying-2026-11-25/`. The commands below use the functions `aggregate.aggregate_settings`, `aggregate.tform` and `aggregate.tacyclic` as defined in `checks/aggregate.py` (`aggregate_settings(labels)`, `tform(t1_label, leader_cs)`, `tacyclic(t2_label, circulation_flags)`), and `aggregate._parse_out` to read the `SETTING_JSON` lines. They are not a script change.

**If only T1's file is complete** (T2 missing or incomplete):

```
python3 -c 'import sys, json; sys.path.insert(0, "checks"); import aggregate as a; rows, _ = a._parse_out("checks/run_t1_v2.out"); labs = [r["label"] for r in rows]; t1 = a.aggregate_settings(labs); form = a.tform(t1, [r.get("leader_c") for r in rows]); print(json.dumps({"T1": t1, "T-form": form, "T1_settings": labs}, default=str))' > checks/aggregate_t1_only.out
```

T2 is `measurement/code` and T-acyclic is not applicable, by the rule above, not by this command.

**If only T2's file is complete** (T1 missing or incomplete):

```
python3 -c 'import sys, json; sys.path.insert(0, "checks"); import aggregate as a; rows, _ = a._parse_out("checks/run_t2_v2.out"); labs = [r["label"] for r in rows]; t2 = a.aggregate_settings(labs); acyc = a.tacyclic(t2, [r.get("circulation", False) for r in rows]); print(json.dumps({"T2": t2, "T-acyclic": acyc, "T2_settings": labs}, default=str))' > checks/aggregate_t2_only.out
```

T1 is `measurement/code` and T-form is not applicable, by the rule above, not by this command. (Step 0b still says not to start T2 when T1 has no `TOTAL_JSON`. This command is locked for a T2 file that is complete even so.)

**`aggregate.py` is run only when both files are complete**, with the command already locked in `PREREG_4.md:36`:

```
python3 checks/aggregate.py checks/run_t1_v2.out checks/run_t2_v2.out > checks/aggregate.out
```

Unit tests of these four paths (T1 incomplete, T2 incomplete, T2 missing, both complete) are in `checks/test_prereg5_paths.py`. They use synthetic `.out` files and run the locked commands. They are not a T1 or T2 run.

## 2. Reviewer relabel, replacing `PREREG_4.md:45`

The last paragraph of `PREREG_4.md` §2 (the clause beginning "If a setting's recorded `cpu` exceeds 720 seconds by more than one rerun's measured time") is superseded. It cannot fire given the code: if the start loop's last start runs past 720 s, the scripts already label the setting `not settled`; a setting that is otherwise settled can go over 720 s only through the half-tolerance rerun, and that overshoot is at most one rerun by construction, which `PREREG_4.md` §2 already allows.

Any post-hoc relabel the reviewer still makes is recorded as a separate dated line in a new file `checks/RELABELS.md`. The reviewer never edits a run `.out` file. `RELABELS.md` is created if and when a relabel is recorded; it is not a run output and is not locked here.

## 3. Cosmetic refusal message

The v2 scripts' refusal string still says "after the PREREG_3 Gate passes". That is cosmetic. The binding condition is a pass on this Gate (`PREREG_5.md`), which this file states. The scripts and their hashes are not changed.

## 4. Scoring and what this does not do

Scoring remains `PREREG_2.md` §4 as amended by `PREREG_3.md` and `PREREG_4.md`, applied to the labels produced under §1. No status change is claimed here.

This file does not change any script or hash. It does not run T1, T2, T-form or T-acyclic. It does not use real data. It does not derive \(\hbar\), \(c\), \(G\), general relativity, quantum mechanics, holography or gravity. It does not move a CLAIM_MAP row.
