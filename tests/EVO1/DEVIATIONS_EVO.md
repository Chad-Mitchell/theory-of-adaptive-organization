# EVO1 deviations log

Every departure from `PREREG_EVO.md` after the lock is recorded here with its time (America/New_York, ET), before the
affected result is read where possible. None yet.

## D1 (Fri 20 Nov 2026, 1:53 PM ET): diagnostics for W4b and W3, added after their runs finished; the locked verdicts stand

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
