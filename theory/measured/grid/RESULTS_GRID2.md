# GRID-2 (Great Britain) and GRID-S results

Locks: GRID-2 prereg `36416d2` (`PREREG_GRID2.md`, 9:56:21 AM ET), GRID-S `8b0ef50` (10:03:29 AM ET),
DV-GB1 `50502a0` (10:06:05 AM ET; its text says "about 10:15 AM", which was wrong: the commit time is the record).
**Erratum (v2.61, review 27 M3):** an earlier version of this line said DV-GB1 came "before any GB series was
downloaded". That was false. Correct statement (refined v2.62, review 27 R2-3): DV-GB1 came **before any frequency value or outcome statistic was
inspected or computed**. Some GB values had been seen, as DV-GB1's own "Seen" list says: the first 3 rows of the EAC
results (April 2026 DRH volumes), the first 3 rows per month of the MFR workbook, and one day of BOALF/PN. The MFR holding
workbooks (about 10:04 AM ET) and the BOALF/PN format day (about 10:05 AM ET) were fetched before it, and dataset
metadata (field names) was read. The frequency, inertia and EAC files were fetched right after it (about 10:06–10:07 AM
ET), and the BM days from about 10:07 AM ET. These fetch times are reconstructed from the session's command order,
not logged. Code `grid2_run.py`
(main sample, robustness, S1) and `grid2_fast12m` mode; outputs `grid2_results.json`, `grid2_fast12m.json`.
Diagnosis after the verdicts: `grid2_diag.py`, `grid2_diag.json`. Implementation fixes during the run (no rule
changes): duplicate inertia timestamps between the two yearly files; mixed date formats in the Aug–Oct
frequency files.

Premise: frequency coverage 1.00, inertia 1.00 (28-day main sample); mean inertia 168 GVA·s; mean DC-low
1,270 MW, DR-low 480 MW, MFR primary 72 MW; BM net delta s.d. 868 MW.

## Per-arm verdicts
| Arm | Verdict | Numbers |
|---|---|---|
| **G1 count by degree (2 s–4 h)** | **FAIL on proxy** | BIC chooses power law + white over every Lorentzian model (ΔBIC 6.9 over L2); γ = 2.09, inside [1.7, 2.3]: a random walk in band, which caps the layers at one (L1); GB runs four |
| G1 robustness (DV-GB1.4) | not INVALID | MFR ×0.5/×1.5, L ×0.5/×1.5, lags τ = FAT: power law chosen every time, γ 2.08–2.18. (B dropped, reported only: L2, one corner at 1,011 s, the closed-loop artifact DV1 warned about) |
| G2 interlacing, four corners | **not scored** | Scored only if the count passes; no separated corner exists |
| Fast-band robustness (12 months, no BM, 2–120 s) | consistent | Power law chosen (ΔBIC 0.2 over one Lorentzian: a tie) |
| Rival R1 "set at" | not scored | No corners |
| **GRID-S S1 (market-step account M: GB corner in [1,300, 2,900] s)** | **M-S1 FAIL** | 15-min means, 30 min–12 h: one Lorentzian (ΔBIC 0.4 over power law, weak), corner 10,148 s, bootstrap CI 4,939 s to the 30-day bound; no CI overlaps the window |
| GRID-S S2 (Germany 2026, 15-min products) | **BLOCKED** | 2026 German 1-s aFRR setpoint is a form button on https://www.netztransparenz.de/de-de/Regelenergie/Daten-Regelreserve/Sekündliche-Daten ("SRL-Sollwert" download, Jan–Jun 2026), plus the mFRR quality-assured CSV for Jan–Jun 2026 from the "Aktivierte Regelleistung" page |

**Kill condition (GRID-1/GRID-2):** not reached. It needs G1 to fail also in CE with open-loop seconds data
(INVALID there) and the speed-price diagnosis to fail. The GB half of that diagnosis does fail (below).

## Diagnosis (causal; does not change any verdict)
- **Where the f⁻² comes from (`grid2_diag.json`):** BM deltas carry 90 % of the reconstructed variance and
  have slope 2.1 at 15 min–4 h; the response term carries 9 %; the inertia term ≈ 0. Full-series local slopes:
  1.5 (2–60 s), 2.1 (1–15 min), 2.0 (15 min–4 h). So the random walk is the slow imbalance that NESO's BM
  instructions follow: accumulated forecast error and schedule steps. Below a minute the series is shallower
  (1.5), not a separated mode.
- **Proxy:** NESO trades on interconnectors and non-BM reserve are missing; these are also step-like, so adding
  them would not create corners. The minute BM data are interpolated, which steepens < 2 min only.
- **Model / scope (main diagnosis):** Master Theorem (iii) is a theorem about *sensing-limited* trackers (memory
  traded against read noise and upkeep). Grid frequency is read with negligible noise; GB's layers differ by
  **actuator** limits (speed of delivery, energy duration: DC 15 min, DM 30 min, DR 60 min) and by **deviation
  magnitude** (DC acts at 0.2–0.5 Hz, post-fault: a ruin product; DM at 0.1–0.2 Hz; DR from 0.015 Hz), not by
  time scale of the world. (iii) is stated "with sensing fixed and ruin not binding"; the prereg did not check
  either premise. With DC and DM set aside as ruin tiers, DR + BM still give two time-scale layers against a
  one-layer prediction, so the miss is reduced, not removed.
- **Speed price (the preregistered kill diagnosis):** faster products are **not** dearer in GB
  (volume-weighted clearing prices, Nov 2025–Oct 2026, £/MW/h: DC-low 3.20, DM-low 7.00, DR-low 16.31;
  DC-high 2.04, DM-high 0.06, DR-high −8.03). The Model S+ speed-price escape fails here.
- **World:** at 1 min–4 h the GB imbalance is self-similar (γ ≈ 2). For a random walk the theory's single
  tracker is the answer; the grid's extra layers are explained above by actuation and ruin, which Model S omits.
- **S1:** GB shows no 30-min mode, as the market-step account required; this disfavours that account of the
  German 65-min mode but does not confirm the world account (which gave no GB window). S2 would decide it.

**Candid note on timing (added 20 Nov 2026, 10:55 AM ET).** Both the reading of DC and DM as ruin tiers and the
sensing-limited scope premise were formulated **after** the G1 miss was seen. Neither was in PREREG_GRID2.md or
its deviation. They are a diagnosis to be tested (GRID-4, `PREREG_GRID4.md`), not a rescue: the GRID-2 G1 verdict
is and stays **FAIL on proxy**, and the G3b premise rule applies only to tests preregistered after it, never
retroactively to GRID-1 or GRID-2.

**Next tests (preregistered before looking):** `PREREG_GRID3.md`.


## Caveat on the GB reconstruction (added v2.61, review 27 S-11)
The balancing-mechanism term B carries about 90 % of the reconstructed imbalance's variance. B is built from discrete
acceptances (BOAL − PN), and a step-like input gives an f⁻² spectrum on its own. The γ ≈ 2 random-walk reading may
therefore partly reflect how dispatch is represented rather than the world. There is no positive control (a synthetic
two-mode world passed through the same reconstruction), so the proxy's power to detect separated modes is unknown.
G3a's margin (ΔBIC 1.0 between the power law and a Lorentzian) is not decisive. The G1 FAIL stands as locked; this
caveat limits what it says about GB's world.

## Dated note (GRID-DX Part A, 20 Nov 2026, after prereg `5d0c11a`)

A qualification audit against the operational definition in force at the GRID-2 lock (first on main at `b311a40`; also on PR #110 head `36416d2`, squash-merged as `e1be66e`) found the GB balancing system **NOT QUALIFIED** as "strongly selected" (`QUALIFICATION.md`). The locked G1 arm score above, **FAIL on proxy**, is not deleted and is not rewritten. The headline status, after the independent review of PR #113, is **NOT A TEST OF THE HYPOTHESIS (qualification not established)**. GB is not qualified: N_e = 1, so the band cannot exclude a rival, and measured outturn inertia changed from 229 GVA·s (2019/20) to 168 GVA·s (2026); T_red was never defined. Item (a) is not established (Ofgem BSIS made σ computable; it was not computed). The measured mismatch (γ = 2.09 random-walk imbalance; four operational layers) stands as a diagnosis of a system examined to prescribe; no inefficiency is shown. The qualification check required at lock should have been done before scoring and was not.

**Sample note (pre-existing GRID-2 issue).** Slow Reserve went live on 31 March 2026 (https://www.neso.energy/document/378736/download), partway through this file's November 2025–October 2026 sample, so the locked four-layer count includes a product that was not in force for the whole sample.
