# GATE PASS

## Gate read v5: `theory/stop-copying-2026-11-25/PREREG_5.md` (fork branch `forge-stop-copying-prereg`, head `1816940`; lock `df114b6`, prelock `8d6de26`)

*Done Wednesday 25 November 2026, about 22:15 ET (America/New_York), as a separate reviewer pass. The gate spec is `process/PREREG_GATE.md` at `8c4b3c0`, with the same checklist as v1 to v4. Caveat: this pass was done by the same agent that wrote PREREG_5, so it is not author-independent. It was run as a separate read, starting again from the locked files and the code. It was read-only, in `<local>/tm-stopcopy6` (a fresh merge of `1816940` onto `origin/main` `93a3a66`, with no conflicts) and `/tmp/g5`. The only things run were the refusal path (no `--execute`) and the locked one-liners on synthetic files.*

## Hashes and integrity: PASS
- `PREREG_5.md` sha256 is `b7850655b46999869d9e7b628cf82930c427069419069ddb449179d82e953e07` and matches `PREREG_5.sha256`. The lock commit `df114b6` adds only `PREREG_5.md` and `PREREG_5.sha256`.
- `PREREG.md` through `PREREG_4.md` all check OK against their `.sha256` files.
- `run_t1_v2.py` (`91f4e6e6…`), `run_t2_v2.py` (`17fab3f4…`) and `aggregate.py` (`c065aa20…`) match the hashes at `PREREG_3.md:53-55`.
- `1816940` appends one dated line to `DEVIATIONS.md`, a correction to the R2/R3 wording at `PREREG.md:65`. R2 and R3 are not scored, so no prediction, threshold or locked byte changes.
- Run state: no `run_t*_v2.out`, no `aggregate*.out` and no `RELABELS.md` exist.

## D1, labels for incomplete outputs: CLOSED
- **Completeness rule (§1).** A file is complete if it exists and has at least five `SETTING_JSON` lines and a `TOTAL_JSON` line. If a file is incomplete, that test is `measurement/code` and its conditional row is not applicable. In the code, each script writes exactly one `SETTING_JSON` line per setting, including `not run (budget)` settings (t1:146-155, t2:268-278). It flushes after each setting and writes `TOTAL_JSON` last. The redirect truncates the file first. So "at least five" is the same as exactly five for any file these commands can produce, and a budget stop can never look like an incomplete file.
- **Step 0b case** (T1 incomplete, T2 not started): both tests are `measurement/code`, both conditional rows are not applicable, and no command is needed. This is now labeled.
- **One-liners.** The names and signatures match `aggregate.py`: `aggregate_settings(labels)`, `tform(t1_label, leader_cs)`, `tacyclic(t2_label, circulation_flags)` and `_parse_out(path)`. The row keys `label`, `leader_c` and `circulation` are the keys the scripts emit (t1:256/268, t2:380/393). Both commands redirect to `checks/aggregate_t1_only.out` and `checks/aggregate_t2_only.out`. I ran them from the locked working directory on synthetic files, including a T1 file with three hits and two `not run (budget)` settings. They returned rc 0 and `{"T1": "not run (budget)", "T-form": "not applicable"}`, and for a five-hit T2, `{"T2": "hit", "T-acyclic": "hit"}`. Both are correct under precedence.
- **`aggregate.py` only when both files are complete (§1, `PREREG_4.md:36`):** checked. The prelock test `checks/test_prereg5_paths.py` runs the four paths (5 passed in the full suite).

## Precedence, tolerances, budget and the 720 s cap: PASS
- **Precedence** is unchanged: measurement/code > guard-hit > not settled > not run (budget) > inside-resolution > {hit, clean miss}, and `mixed` applies to hits and clean misses only. An incomplete file falls in the top class, which matches the protocol-failure reading in `PREREG_4.md` step 0b.
- **Tolerances** are unchanged: relative best 1e-6·|J*|, the pairwise A agreement of 0.01, the half-tolerance move, and the guard. The resolution band is |A−0.10| ≤ 0.02, so a hit needs A > 0.12 and a clean miss needs A < 0.08.
- **Budget.** The cap is 12 CPU-min per setting and 2 CPU-h in total across T1 and T2. T2 reads `t1_cpu` from T1's `TOTAL_JSON`, and step 0b guarantees that line is there.
- **720 s.** The start loop breaks at the cap, and the setting is then `not settled` (t1:166-189). The rerun starts only while `used() < cap`, so any overshoot is at most one rerun, and `PREREG_4.md` §2 allows that. PREREG_5 §2 is right that the old relabel clause cannot fire, and it moves any post-hoc relabel to dated lines in a new `checks/RELABELS.md`, never into a run `.out`. It closes v4 N1.
- **Output files.** Every locked command writes its own `.out` file through a redirect: T1, T2, aggregate, t1_only and t2_only.

## G1–G5: PASS
- G1: every outcome now has a named label.
- G2–G5 are unchanged from v2 to v4.
- Wording: "law" appears only at :5, byte-identical to `CORE.md:7`. None of "one-way", "stop copying", "solved", "kill", "dead", "verdict", "puzzle" or "bill" appears. The scope line (no ℏ, c or G, no GR, QM, holography or gravity) is present.

## Non-blocking
- **N1.** When only one file is complete, the label of the other test comes from the text rule, and no locked file records it. The results write-up should state it next to the one-liner output.
- **N2.** The cosmetic "PREREG_3 Gate" refusal string is noted at §3, which closes v4 N3. The binding gate is this read of PREREG_5.
- **N3.** The maxfun probe still covers only (10,1), as stated.
- **N4.** This pass is not author-independent (see the caveat above). An outside reader may still want to re-check it.

## Result
**GATE PASS.** The locked run may proceed exactly as `PREREG_4.md` §1 and `PREREG_5.md` §1 specify.
