# Gate reads for #292 (committed 26 November 2026)

These are the gate reads of the #292 preregs, done 25 November 2026 and kept until now only on the author's machine. They are committed byte-for-byte except that machine paths are written `<local>` (the repository's scrub convention), so an outside reader can check what each gate found. `checks/gate_read_292_local.py` and `.out` were already committed.

| file | prereg read | result | reader |
|---|---|---|---|
| `gate_read_292.md` | `PREREG.md` | GATE FAIL | separate reader |
| `gate_read_292_v2.md`, `gate_read_292_v2_probe.*` | `PREREG_2.md` and its run scripts | GATE FAIL (7 script blockers) | separate reader |
| `gate_read_292_v3.md`, `gate_read_292_v3_probe.*` | `PREREG_3.md` | GATE FAIL (B7 only) | separate reader |
| `gate_read_292_v4.md` | `PREREG_4.md` | GATE FAIL (B5 a contradiction in the text) | separate reader |
| `gate_read_292_v5.md` | `PREREG_5.md` | GATE PASS | **the author agent** (not independent; `RESULTS.md:7`, `DEVIATIONS.md` 2026-11-26 line) |

The v2 and v3 probes called the scored code's cost and label functions on designed inputs before the run (not the minimizer).

**Correction (26 November 2026, 03:10 ET).** The sentence above is wrong for v3: the v3 probe *did* call the L-BFGS-B minimizer on the locked T2 objective (10 starts plus 2 half-tolerance reruns, non-locked seeds 424242 and 777, J and A not printed). Only the v2 probe stayed at the function level. Gate read v5 was written at 22:11:36 ET, 7 s before T1 started. A retrospective independent gate read of `PREREG_5.md` (pass as a TEST, with a relabel caveat) is in `gate_read_292_retro_2026-11-26.md`.
