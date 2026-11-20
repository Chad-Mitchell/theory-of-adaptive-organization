# GRID-1 deviations log
- **DV1** (20 Nov 2026, before any outcome statistic): data substitution (aFRR setpoint 1 s + mFRR 15 min
  instead of second-wise NRV), circularity, arms G1, G2-fast and G2-mid declared INVALID in advance,
  G2-slow and R1-slow scorable at ≥ 30 min, adjusted INVALID rules. Full text appended to `PREREG_GRID1.md`.
- **DV2** (before any spectrum): parsing fixes; Germany = sum of four TSO columns (identical where both exist).
- **DV2 erratum**: TSO columns not complete; GRID-1 INVALID by premise (mFRR coverage 0.666). Follow-up GRID-1b locked in `PREREG_GRID1b.md`.
- GRID-1b run (code fix: H2 date filter offset, rule unchanged); results in RESULTS_GRID1.md. GRID-2 (GB) preregistered.
- **DV-GB1** (GRID-2, before downloading GB series): 4-week main sample with BM, 12-month fast robustness, reconstruction, corner-wise INVALID rules; S1 adapted; S2 BLOCKED.
- GRID-2 run; RESULTS_GRID2.md; follow-up PREREG_GRID3.md (before any 2024 GB or 2026 DE data).
- GRID-4 (test of the GRID-2 diagnosis) preregistered before any 2019/20 or 2024 GB data; candid timing note added to RESULTS_GRID2.
- **DV-S2** (before computing on 2026 German files): operational aFRR for the premise check only; method fixed; comparability check with the GRID-1b method.
- G3a run (replicates G1 FAIL); GRID-4 INVALID (verdict depends on assumed Q); GRID-4b preregistered before any 2019/20 response source.
- **Erratum (v2.61, review 27 M3):** RESULTS_GRID2 and CLAIM_MAP P19 said DV-GB1 preceded any GB download. False: the MFR workbooks and one BOALF/PN day (format check) were fetched 10:04–10:05 AM ET, before DV-GB1 (10:06:05); the frequency, inertia, EAC and BM series after it. No GB value was inspected or computed before DV-GB1. Corrected in both places.
- **Refinement (v2.62, review 27 R2-3):** "no GB value" was too strong. DV-GB1's "Seen" list includes the first 3 rows of the EAC results, the first 3 rows per month of the MFR workbook, and one BOALF/PN day. The correct claim is that no frequency value or outcome statistic was inspected or computed before DV-GB1. The 10:04–10:07 AM ET fetch times are reconstructions from command order, not logs.
- **v2.61 (review 27 M4):** dated clarification appended to `PREREG_GRID3.md`. G3b applies only to tests locked after it. G3a was locked under the old scope, so P21 stays PROXY-FAIL. The claim that grids fail G3b criterion 1 is an assertion, not a measurement. Wording elsewhere changed from "refuted on proxy outside its premises" to the locked "FAILED on proxy".
