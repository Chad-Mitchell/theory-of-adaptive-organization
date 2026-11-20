# G3a (GB 2024 replication) and GRID-4 (actuation vs world) results

Locks: GRID-3 `b7f69e8`; GRID-4 `a3d52ca` (10:55:00 AM ET, before any 2019/20 or 2024 data). Code: `grid2_run.py`
driven by `GRID_CFG` (weeks, response inputs), `grid4_slope.py`. Outputs: `grid3a_results.json`,
`grid4_results.json`, `grid4_slope.json`. Implementation fixes during the run (no rule changes): the Oct 2019
frequency file carries UTC offsets (parsed to UTC); the 2023-24 MFR workbook uses spaced column names; the 2019/20
frequency files are zipped.

## G3a: GB 2024, weeks 8–14 Jan, 8–14 Apr, 8–14 Jul, 7–13 Oct
Premise: frequency and inertia coverage 1.00; mean inertia 187 GVA·s; DC-low 1,070 MW, DR-low 290 MW, MFR
primary 147 MW; BM delta s.d. 775 MW.

| Arm | Verdict | Numbers |
|---|---|---|
| **G3a replication (power law, γ ∈ [1.7, 2.3])** | **PASS: the GRID-2 G1 FAIL replicates** | Power law chosen, γ = 2.02. Margin over one Lorentzian is small (ΔBIC 1.0; in 2026 it was 7.9) |
| Robustness (MFR ×0.5/×1.5, L ×0.5/×1.5, lags τ = FAT) | holds | Power law every time, γ 2.01–2.04 |
| B dropped (reported only) | — | One corner at 588 s: the closed-loop artifact again |
| Unscored extra: GRID-S-style 15-min fit | — | Power law, γ = 1.74; no 30-min mode (not a locked arm for 2024) |

So GB's reconstructed pre-control imbalance is a random walk across 2 s–4 h in both 2024 and 2026. Master
Theorem (iii) then predicts one layer; GB runs four. GRID-2 G1 stays **FAIL on proxy**, now replicated.

## GRID-4: GB 2019/20 (before DC), weeks 7–13 Oct 2019 and 6–12 Jan 2020
Premise: coverage 1.00; mean inertia 229 GVA·s; BM delta s.d. 962 MW; response = assumed Q = 1,500 MW (no source).

| Quantity | 2019/20 | 2026 (GRID-2) |
|---|---|---|
| Main fit | power law, γ = 2.08 | power law, γ = 2.09 |
| Local slope, 2–60 s | **2.13** | 1.48 |
| Slope with Q × ⅓ / Q × 3 | 1.92 / 2.60 | — |

- By the locked rules at Q = 1,500 MW, A fails its slope condition (|2.13 − 1.48| = 0.65 > 0.3) and W PASSES
  (slope differs by > 0.5).
- Under Q × ⅓ the difference is 0.44: neither account passes. Under Q × 3 it is 1.12: W passes. The verdict
  changes, so **GRID-4 is INVALID** by its own rule.
- **Diagnosis.** The 2–60 s band is exactly where the unknown 2019 response holding acts, so the assumed Q decides
  the answer. The slow band agrees across 2019/20, 2024 and 2026 (γ 2.02–2.09), so the slow world did not change
  while the products changed. That fits A, but it is not GRID-4's locked criterion and is not scored.
- **Next test:** `PREREG_GRID4b.md` (sourced 2019/20 holdings), locked before looking.

## GRID-4b: UNTESTED
Rule (locked `c2ecc13`): UNTESTED if item 1 (MFR holdings for Oct 2019 and Jan 2020) or item 2 (FFR in force)
cannot be found in an open source. **Item 1:** NESO's published MFR holding volumes start with 2022-23 (MFR
page, "Frequency Response volumes"); the Monthly Balancing Services Summary gives costs, not MW holdings. No
open 2019/20 MFR holding source was found. **Item 2:** FFR post-tender reports exist (e.g. TR118 Oct-19, TR121
Jan-20), but the volume in force needs every earlier tender whose contracts span those months. Not attempted,
because item 1 already decides the verdict. Raw GB data deleted (hashes in `DATA_SOURCES_GB_2024_2019.md`).

**Where GRID-4b was searched (added v2.61, review 27 S-14).** NESO's Mandatory Frequency Response page
(https://www.neso.energy/industry-information/balancing-services/frequency-response-services/mandatory-frequency-response,
"Frequency Response volumes" documents) and the Monthly Balancing Services Summary (exact URL not recorded). The FFR
post-tender reports (TR118, TR121) were found by search, but their URLs were not recorded. The search was not exhaustive:
an FOI request to NESO or an archived copy of older MFR reports could still supply the holdings.
