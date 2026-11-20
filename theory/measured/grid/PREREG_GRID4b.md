# GRID-4b preregistration: GRID-4 with a sourced 2019/20 response holding

Written Friday 20 November 2026, about 11:40 AM ET, after GRID-4 came out INVALID (its answer depended on an
assumed response holding), **before searching for or opening any 2019/20 response-volume source**.

Same data (weeks of 7–13 Oct 2019 and 6–12 Jan 2020, already analysed), same rules as GRID-4, with one change:
Q is replaced by the published 2019/20 holdings, i.e. the sum of
1. MFR primary and high-frequency holdings, from NESO's published monthly MFR volumes or Monthly Balancing
   Services Summary for Oct 2019 and Jan 2020;
2. firm frequency response (dynamic and static) contracted for those months, from NESO's FFR post-tender
   reports;
3. Enhanced Frequency Response (≈ 200 MW, 1 s) if listed;

each with its own published delivery speed (lag τ = FAT/3: EFR 1 s, primary 10 s, secondary 30 s).

**Rules.** As GRID-4, using A and W at the 2–60 s local slope and the main fit. The robustness run (×0.5 and
×1.5 on the summed holding, not ×⅓ and ×3, because the holding is now sourced) must not change the verdict, or the
result is INVALID. If any of 1–2 cannot be found in an open source: **UNTESTED**.

**Known (disclosed):** the 2019/20 slope at Q = 1,500 MW is 2.13, at 500 MW 1.92 and at 4,500 MW 2.60, so the
outcome is already known to rise with Q. The test is decided by what the sourced holding turns out to be. That is
a weak test (the mapping is known; only the input is not); this is stated so that it is not over-read.
