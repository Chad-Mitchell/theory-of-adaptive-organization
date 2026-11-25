# Deviations from `PREREG.md` (append-only)

*Wednesday 25 November 2026 (America/New_York). Prereg lock `4a0d5e9`, sha256 `501a82ded728e6616393ca88d2bf92114287061e219ecd25cd58680893771a77`. The locked file is not edited.*

1. **No separate gate check before scoring P1–P4.** Disclosed in `PREREG.md` §4 before scoring. P1–P4 are readings of published sources, not runs, and the work order directed scoring right after the lock. Draft PR #263 asks a separate reader to check the `Gate` section before a run. A reader should still check §3 on paper; if the reader stops an item, that item's score here is withdrawn by an appended line, not edited.
2. **E1 not run.** E1 is a run, so it waits for a separate gate check, as locked. Its premise ("not used by the record") was checked after the lock and is half false (`RESULTS.md`, E1). The gate reader should see that before deciding whether E1 is worth running.
3. **P1 not scorable.** As the locked rule allows. No allocation-based value is substituted for the locked runtime-RAM share.
4. **Version scored.** Sizes are the 24 July 2026 record row (LTCB `.0969`). Source files are from the record's GitHub home at `83f2603` (moved there 2 September 2026, after an Intel crash fix on 21 August that changed the archive by 2,010 bytes and the compressor by 1,832 bytes). The weight file size (2,930,652 bytes) is read at `83f2603`. The record's own text gives the same 2.9 MB per binary for the July submission.
5. **Name.** The prize page's "fx2-cmix-T" is LTCB's and GitHub's "fx2-cmix-transformer". Same author, date and total size.
