# GRID-CROSS results

Lock: `LOCK.txt`, Saturday 21 November 2026, 1:55:05 AM EST (America/New_York), beside `main` `54a4562`. Prereg, runner and library hashes are recorded there. This file is not a locked file.

**Official comparison: not run.** After the lock, public data without accounts are **not sufficient** for n ≥ 5 complete (S, d1) pairs under the locked rule. Runtime is not the constraint. No official Pass 1 score and no official Pass 2 distance has been recorded. P25 is not re-scored.

## Diagnostic and hypothesis-test status

- Gradient diagnostic (PREREG §8): **UNTESTED** (n = 1 complete d1 already on disk, GB only, as in GRID-DX; no new d1).
- Test of the hypothesis: **NOT A TEST** until the class qualification record required by PREREG §2 is written, before any new distance is used in that verdict. GRID-DX already found GB not qualified; this prereg does not change that finding and does not invent a qualifying class.

## Exactly what data are missing for Pass 2 / d1

d1 requires an official *open-loop or pre-control imbalance* spectrum, in a band of at least two decades that includes 1 min–1 h, or a reconstruction with the same ingredients as GRID-2 DV-GB1.2 (frequency, inertia, delivered response, and dispatch). Closed-loop frequency is not enough.

Missing, by grid, after the reachability pass (`DATA_SOURCES_REACHABILITY.md`):

- **Great Britain:** already has a complete d1 in the repository (d1 = 3 under B1 ruin-slack; tagged BINDING-RUIN). Not missing; not recomputed.
- **Australia NEM:** no pre-control imbalance series fetched. AEMO 4-s annual frequency files were listed on a landing page but direct file URLs were not successfully fetched (guessed paths failed). Quarterly monitoring PDFs were fetched and are reports, not a verified 4-s series. Even a 4-s *frequency* series would still be closed-loop and not sufficient for d1.
- **ERCOT:** high-resolution frequency and regulation series sit behind a Public API that requires registration; excluded. No no-account pre-control imbalance or reconstruction kit was fetched.
- **Ireland / Northern Ireland:** EirGrid System Services PDFs are now reachable (HTTP 200) for institutional scoring, but no official pre-control imbalance series was fetched. The real-time system-information page returned 200; a historical CSV or API for 5-s frequency was not verified and, if only frequency, would still be closed-loop.
- **Nordic:** Fingrid 10 Hz frequency archives are reachable without an API key (HEAD only in this pass). They are closed-loop frequency. No official inertia-plus-activation reconstruction kit, and no official open-loop imbalance series, was fetched as a no-key static file.
- **Continental Europe:** the Netztransparenz 2022 1-s frequency zip is reachable (closed-loop). The 1-s aFRR setpoint download remains form-gated. ENTSO-E Transparency API/SFTP require registration; the public web app did not yield a data table without a form or account. Typical published imbalance at 15 min cannot include 1 min in the locked band.
- **Hawaii (first-choice island):** homepage and RSWG reports page reached; no public high-resolution frequency or imbalance CSV was fetched. Transpower (NZ) quarterly-report page and TSOC (Cyprus) homepage reached; no frequency CSV was fetched.

Also missing for a *hypothesis* test, independently of spectra: a class with real competing design lineages, with σ computed, N_e large enough that the band excludes a named rival, T_red defined, and at least 10 T_red of the same world, recorded before distances are measured (FRAMEWORK §9 / PREREG §2). S is not qualification.

## What could still be done under this lock, later

Pass 1 (selection-pressure scores from the institutional sources that were fetched, including the now-reachable AEMC reliability-settings PDF and EirGrid System Services PDFs) can be completed after this file, without opening evaluation distances, and must be committed before any Pass 2. That would not, by itself, make the rank test scorable.

No numbers in this file are official S or d scores.
