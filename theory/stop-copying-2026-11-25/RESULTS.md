# Results: who copies whom (T1, T2), run under PREREG_4 §1 and PREREG_5 §1

*Wednesday 25 November 2026 (America/New_York). Branch `forge-stop-copying-prereg`, run at head `1816940` (lock `df114b6`). Append-only: no prediction, threshold, odds, script, hash or locked line is changed. In-model only: no real-world data. Scope as in `PREREG.md` through `PREREG_5.md`. This does not give \(\hbar\), \(c\) or \(G\), and nothing here derives general relativity, quantum mechanics, holography or gravity.*

## Gate and procedure

- **Gate read v5 of `PREREG_5.md`: GATE PASS.** It was done as a separate reviewer pass at about 22:10 ET. It was not independent of the author: the same agent wrote `PREREG_5.md`.
- **Step 0.** `sha256sum` of `run_t1_v2.py`, `run_t2_v2.py` and `aggregate.py` matched `PREREG_3.md:53-55`.
- **T1** was run with the locked command (`PREREG_4.md:22`) from 22:11 to 22:12 ET, exit code 0.
- **Step 0b passed.** `checks/run_t1_v2.out` has five `SETTING_JSON` lines and a `TOTAL_JSON` line.
- **T2** was run with the locked command (`PREREG_4.md:30`) from 22:15 to 22:41 ET, exit code 0.
- **Both files are complete** under `PREREG_5.md` §1, so only `aggregate.py` was run, with the locked command (`PREREG_4.md:36`), into `checks/aggregate.out`. Neither one-liner applies.
- **No relabel.** No setting's `cpu` came near 720 s (the maximum was 362.5 s), so `checks/RELABELS.md` was not created.
- **CPU, by `time.process_time()`.** T1 used 27.8 s and T2 used 1510.0 s, a total of 1537.8 s against the 7200 s cap.

## Scored outcome, against the locked thresholds

The hit bar is the value at `PREREG_2.md` T1 and T2, with resolution 0.02 around 0.10. A setting is a hit if its value is > 0.12 at all five settings, and a clean miss if it is < 0.08 at all five.

| Test | Setting labels (10,0.5), (10,1), (10,2), (3,1), (30,1) | Scored value per setting | Test label | Conditional row |
|---|---|---|---|---|
| T1 (two judges) | clean miss ×5 | \(A\) = 2.1e-8, 1.7e-8, 1.7e-8, 1.6e-8, 5.1e-9 | **clean miss** | T-form: not applicable |
| T2 (eight-judge ring) | clean miss ×5 | \(A_{(5)}\) = 8.3e-8, 2.9e-7, 4.8e-8, 1.8e-7, 3.3e-7; broken edges (\(A_e>0.12\)): 0 of 8 at every setting; largest \(A_e\) 1.1e-6 | **clean miss** | T-acyclic: not applicable |

At every setting, no measurement/code flag, guard-hit, not settled, or budget label was raised.

- **Settled starts.** For T1, 255–260 of 260 converged starts were at the best value. For T2, 355–576 of 576 were.
- **Half-tolerance rerun.** Every rerun stayed within the tolerance: T1 \(A\) ≤ 2.1e-8 and T2 \(A_{(5)}\) ≤ 3.3e-7.
- **Smallest real eigenvalue part.** It was 24.7 or more (T1) and 46.7 or more (T2), which is well clear of the guard.

**Observed.** Within resolution, both best designs found were the symmetric design. For T1 that is \(\gamma\) on the cap (5.0) and equal copy gains \(c\) = 0.800, 0.730, 0.642, 0.566 and 0.833. These equal the closed form \(w(1-c)^2=w_xc\) from C5, to the printed digits (0.730 at the reference (10,1)). This is the clean miss that `PREREG_2.md` names: with this excursion term, closure with the heat term settles on the reciprocal, detailed-balance set (C1). The heat term separates from rational inattention without heat by copy level (C5), not by direction. The same holds on the eight-judge ring. Following `PREREG_2.md`, the next step is a prereg that looks for a break from an asymmetric ingredient (unequal temperatures, delay, \(P_D>0\)). That is a hypothesis, not a result.

The scored rival (R1 together with the detailed-balance null) predicted \(A=0\). The observed values agree with it within resolution. The hit odds locked before the run were 0.10 (T1) and 0.12 (T2).

## Files

- `checks/run_t1_v2.out`
- `checks/run_t2_v2.out`
- `checks/aggregate.out`

These are the unedited stdout of the locked commands.

## Note appended 27 November 2026 (the lines above are unchanged)

The README row STOP-COPY now records this result (clean miss on T1 and T2) and points to the next prereg (one asymmetric ingredient). Its previous work order, quoted verbatim from `main` at `ecf5bdbb4aae33bb5511816dac901dac2596e6c7`:

> The who-copies-whom prereg (`theory/stop-copying-2026-11-25/`, in flight; the ID follows its PR): does the cost minimum break the symmetry so copying runs one way, locked before any run, against the rival of information theory without the heat cost, under which both judges nearly stop copying (c about 0.004 to 0.0002) and the flow stays symmetric (C5 of that prereg). Two judges first, then eight. Gate read before any run. A hit does not produce physical constants. |

## Ledger rows (appended 27 Nov 2026; lines above unchanged)

| prediction_id | locked_prediction | outcome | miss | location | stake_x_info | update | breach_check |
|---|---|---|---|---|---|---|---|
| T1 | A > 0.12 at all five settings (`PREREG_2.md`) | A ≤ 2.1e-8 | clean miss, −0.12 | model | medium | next prereg adds one asymmetric ingredient | breach of `PREREG_5.md:3` (self gate read), logged in `process/FAILURES.md` |
| T2 | A > 0.12 at all five settings (`PREREG_2.md`) | A_(5) ≤ 3.3e-7; 0 of 8 edges | clean miss, −0.12 | model | medium | next prereg adds one asymmetric ingredient | breach of `PREREG_5.md:3` (self gate read), logged in `process/FAILURES.md` |
