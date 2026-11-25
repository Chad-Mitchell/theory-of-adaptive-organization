# Deviations from `PREREG.md` (append-only)

*Wednesday 25 November 2026 (America/New_York). Prereg lock `4a0d5e9`, sha256 `501a82ded728e6616393ca88d2bf92114287061e219ecd25cd58680893771a77`. The locked file is not edited.*

1. **No separate gate check before scoring P1–P4.** Disclosed in `PREREG.md` §4 before scoring. P1–P4 are readings of published sources, not runs, and the work order directed scoring right after the lock. Draft PR #263 asks a separate reader to check the `Gate` section before a run. A reader should still check §3 on paper; if the reader stops an item, that item's score here is withdrawn by an appended line, not edited.
2. **E1 not run.** E1 is a run, so it waits for a separate gate check, as locked. Its premise ("not used by the record") was checked after the lock and is half false (`RESULTS.md`, E1). The gate reader should see that before deciding whether E1 is worth running.
3. **P1 not scorable.** As the locked rule allows. No allocation-based value is substituted for the locked runtime-RAM share.
4. **Version scored.** Sizes are the 24 July 2026 record row (LTCB `.0969`). Source files are from the record's GitHub home at `83f2603` (moved there 2 September 2026, after an Intel crash fix on 21 August that changed the archive by 2,010 bytes and the compressor by 1,832 bytes). The weight file size (2,930,652 bytes) is read at `83f2603`. The record's own text gives the same 2.9 MB per binary for the July submission.
5. **Name.** The prize page's "fx2-cmix-T" is LTCB's and GitHub's "fx2-cmix-transformer". Same author, date and total size.
6. **Gate placement (non-blocking).** `PREREG.md` places the `Gate` section at §3 rather than at the very top as `process/PREREG_GATE.md` §2 requests. `PREREG.md` is kept untouched.
7. **P1 re-scored under the lock's fallback (`RESULTS.md` addendum, 12:30 ET).** Line 3 above is superseded by the appended P1 re-score (`hit`, `f_max = 0.709` by allocation constants; `≥ 0.41–0.46` in RAM with residency caveat).
8. **E1 withdrawn (`RESULTS.md` addendum, 12:30 ET).** Line 2 above is superseded: the independent gate read returned **GATE STOP** on E1 (G3 fails because the record already uses an inaction band in live `fxcmv1.cpp:506` and `mixer.cpp:75-77`; stop rule and implementation underspecified). E1 is withdrawn and never run; the new-design result is `none found`.
