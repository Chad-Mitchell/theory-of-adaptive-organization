# EVO1 deviations log

Every departure from `PREREG_EVO.md` after the lock is recorded here with its time (America/New_York, ET), before the
affected result is read where possible. None yet.

## D1 (Fri 20 Nov 2026, about 1:51 PM ET; commit cf77048 is the record): diagnostics for W4b and W3, added after their runs finished; the locked verdicts stand

Read before writing this entry: the locked scoring of the finished PC, W1, W3 and W4b seeds (W2, W4, S031, S07 still running).
- **W4b:** all 8 seeds evolved one local store and no shared store (J gap 1.04%, the "no sharing" rival's gap), so W4b will
  score FAILED under §6. Calibration (§4.2, before the lock) had already shown that the predicted design is realized-cheaper
  than local-only (paired gap 2.5% ± 0.8% per generation), so step (1) of §8 (prediction mis-specified) does not explain the
  miss, and step (2) (null-like scatter) does not apply (every seed converged to the same rival design). Two diagnostics are
  added, neither of which can change the W4b verdict:
  - **D1a, stability:** every agent starts at the predicted design (one local, one shared store, the predicted rates and
    optimal read weights); locked simulator, prices and selection; seeds 0–3; 600 generations. Fixed interpretation: if the
    consensus stays at one local plus one shared store inside the band in ≥ 3 of 4 seeds, J's minimum is selection-stable
    and the W4b miss is about reachability (a fitness valley), not about J's books; if it leaves for local-only in ≥ 3 of 4,
    the realized world does not reward the design J says is cheapest (a cost mismatch, a deeper failure).
  - **D1b, reachability:** the locked starts, with one change: a store created from nothing gets a read weight drawn from
    N(0, 0.3²) instead of 0 (the two parts of the new layer can arise together). Seeds 0–3. Fixed interpretation: if ≥ 3 of
    4 seeds reach one local plus one shared store inside the band, the valley is the barrier.
- **W3:** all 8 seeds landed inside the band with the predicted one store, but the mean final-window death fraction is
  about 13%, above the locked 10% gate, so W3 will score INVALID (ruin binding). The deaths are expected among mutants whose
  read weight is off 1, since a random walk makes that error grow without bound; the gate cannot tell these from deaths of
  near-optimal designs. **D1c:** rerun W3 with the buffer ×10 (seeds 0–7, otherwise locked), reported beside the locked
  INVALID, never in place of it; and evaluate the evolved consensus design as a fixed design with the locked ruin gate over
  40 worlds to measure its own death rate.

## D2 (Fri 20 Nov 2026, about 2:18 PM ET; the commit adding this entry is the record): a reachability diagnostic for W4

Read before writing: the locked scoring of all 8 W4 seeds. Three seeds (0, 4, 6, all one-store starts) stayed at one
local store (J gap 8.1%), so W4 will score FAILED (3 misses) under §6. The four four-store starts (1, 3, 5, 7) and one
one-store start (2) reached one local plus one shared store inside the band, so the predicted design is reachable and holds
once reached. Suspected cause, as in W4b: a shared store created from nothing starts with read weight 0, so it costs hc
(2.4% of J* in W4) before it can pay. **D2b:** D1b's change (a store created from nothing gets weight N(0, 0.3²)) applied to
W4, seeds 0, 2, 4, 6 (one-store starts), otherwise locked. Fixed interpretation: ≥ 3 of 4 reaching the band means the
weight-0 creation valley is the barrier. It cannot change the W4 verdict.

## D3 (Fri 20 Nov 2026, about 2:52 PM ET; the commit adding this entry is the record): S031 and S07 reported as PENDING, not INVALID

Read before writing this entry: the locked scoring of PC, W1, W2, W3, W4, W4b, and all D1/D2 diagnostics. The store-noise
arms are slow (about 6.7 s per generation, so roughly 67 min per run; 24 runs at 4 in parallel, about 6–7 hours from about
2:40 PM ET). `analyze_evo.py` labels a world with no runs "INVALID (only 0 converged seeds)". That label describes
missing data, not a failed gate, so `RESULTS_EVO.md` reports S031, S07, the store-noise threshold and the S031→S07 move as
**PENDING**. The runs continue unchanged (locked code, `runall.sh`, seeds 0–7 and 100–103). When they finish, the locked
`analyze_evo.py` will be rerun unchanged, and its S-arm verdicts will be added to `RESULTS_EVO.md` and `CLAIM_MAP` in a later
commit with their own time. Nothing in the scoring changes.

## D4 (Sat 21 Nov 2026, about 10:10 AM ET; the commit adding this entry is the record): S arms finished; scoring unchanged; one dependency file changed on `main`

- **Runs.** All 96 locked runs are done (8 worlds × seeds 0–7 and null seeds 100–103). The last run file was written Fri 20 Nov 2026 at 11:49 PM ET. Locked code, `runall.sh` and seeds were not changed. `D3` is closed: S031, S07, the store-noise threshold and the S031→S07 move are now scored.
- **Scoring.** `analyze_evo.py` was run unchanged (prereg hashes verified at that time) and rewrote `ANALYSIS_EVO.json`. No rule, threshold, band or seed was changed. Verdicts: PC, W1, W2 PASSED; W3 INVALID (ruin gate; raw PASSED); W4, W4b FAILED; S031, S07 INCONCLUSIVE (2/8 each, both criterion A); PC→W1 and S031→S07 moves PASSED; store-noise threshold PASSED (8/8 and 8/8); W2 interlacing PASSED 7/7. Read before writing this entry: all of these.
- **Run record, S031 seed 2.** `logs/S031_2.log` ends at g550 because the run printed every 50 generations and g599 is not a multiple of 50. The run file `runs/S031_s2.json` has G = 600, 600 logged generations (last g = 599), a consensus block and `secs` = 8492 s, so it ran to completion. The log files for several S-arm runs were interrupted and recovered (`logs_recovered/`); the run files, not the logs, are what the scorer reads.
- **Dependency drift (disclosed).** `PREREG_EVO.sha256` lists `theory/layers_checks/stores.py` at `df6b7039…`. After scoring, merging `origin/main` brought in the v2.67 numerical-guard fix to that file (PR #116), so its hash no longer matches; every other listed hash still verifies. The locked bytes are at commit `70fcbad`. To check that the change cannot move any verdict, `analyze_evo.py` was rerun unchanged on the merged tree to a scratch copy: every field matched the committed `ANALYSIS_EVO.json` to within 1e-9 (largest difference 7e-11 in a null seed's J gap). The committed analysis file is the one produced before the merge. `PREREG_EVO.sha256` is not edited.
- **Diagnostic added to the results (not scoring).** `RESULTS_EVO.md` now includes a reading of the S-arm misses (gap against rate offset, per seed). It uses only the locked scores, ran nothing new, and changes no verdict.
