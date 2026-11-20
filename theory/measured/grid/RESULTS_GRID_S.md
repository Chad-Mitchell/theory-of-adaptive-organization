# GRID-S results: is the German 65-min mode the world's or the market's hourly step?

Locks: GRID-S `8b0ef50`; DV-S2 `d5ccf03` (10:57:36 AM ET, before computing on the 2026 files). Code `grid_s2.py`;
output `grid_s2_results.json`. Fix during the run (no rule change): the robustness call without bootstrap crashed
on an empty interval list; the run was repeated with the same seed, and the main numbers did not change.

| Arm | Verdict | Numbers |
|---|---|---|
| S1 (GB, M's 30-min window [1,300, 2,900] s) | **M-S1 FAIL** | See `RESULTS_GRID2.md`: corner 10,148 s, CI 4,939 s to the bound |
| S2 premise | valid | 1-min coverage 0.9998; corr(setpoint, operational aFRR) 0.995; mFRR variance share 0.3 % |
| **S2 main (1-min means, 5 min–3.5 days)** | **W-S2 PASS; M-S2 not PASS** | BIC picks two Lorentzians (ΔBIC 4.3 over three). Corners 246 s (CI 226–268 s, 42 % of variance) and **2,956 s (CI 2,626–3,352 s, 58 %, dominant)**. The dominant CI is inside W's [2,600, 5,850] s, with a thin margin at the lower edge (2,626 vs 2,600). No corner lies in M's [650, 1,460] s |
| S2 comparability (GRID-1b method, 15 min) | agrees | One Lorentzian, 3,319 s (CI 2,794–3,919 s), inside W's window |
| S2 robustness (with mFRR) | agrees | 244 s and 2,983 s |

**Reading.** After German day-ahead moved from hourly to 15-min products (Oct 2025), the slow mode did not move
to about 16 min as the market-step account required. It stayed near 50–55 min, compared with 65 min in 2022
(×0.76–0.85, inside W's ×1.5 window). Together with S1, the "hourly schedule step" account fails twice, and the
world account of the mode passes its one discriminating arm.

**Caveats.**
- The 246-s corner sits at the aFRR loop's own time scale (5 min). DV1 declared that band closed-loop, so it is
  not read as a world mode.
- W passes by a thin margin at the lower edge of its window.
- This supports GRID-1b's reading of the slow mode. It does not test the layer count.
- **Added v2.61 (review 27 S-3 to S-5).** The CI is conditional on the BIC-chosen K = 2; it does not include model
  uncertainty over K. The day-block bootstrap resamples Welch segments that overlap by 50 % as if independent, so the
  CI is likely too narrow. The 26-s margin (2,626 vs 2,600 s) is smaller than that understatement plausibly is, so the
  PASS is indistinguishable from the window's edge. The verdict is as locked, but it should be read as weak.
- The 246-s corner was declared closed-loop in DV1 for the 2022 data. The GRID-S lock does not restate that
  exclusion for 2026. The verdict does not depend on it: the dominant corner decides W-S2, and 246 s is outside M's window.
- The like-for-like ratio (2026 vs 2022, the GRID-1b method) is 3,319/3,900 ≈ 0.85. The two samples come from
  different seasons and years, which confounds the ratio.
- **What S2 shows:** it rejects one named rival (the hourly market-step account). It does not show that the mode
  belongs to the world rather than to some other non-market cause.
