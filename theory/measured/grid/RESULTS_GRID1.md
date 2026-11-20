# GRID-1 and GRID-1b results (2022, German LFC block)

Prereg `4820d91`; DV1 `6636517` (pushed 9:49:18 AM ET, 20 Nov 2026, before any outcome statistic); DV2 `a769a1f`
(9:51:54 AM ET); GRID-1 verdict + GRID-1b prereg `bef3b8c` (9:52:57 AM ET), all before any spectrum. Code:
`grid1_run.py` (run with `--grid1b`); output `grid1b_results.json`, `grid1_premise.json`. Raw data not in git
(`DATA_SOURCES.md`: SHA-256 and sources).

## Per-arm verdicts
| Arm | Verdict | Why |
|---|---|---|
| GRID-1 (all arms, as locked + DV1) | **INVALID** (premise) | mFRR 15-min coverage 0.666 < 0.90 (three TSOs report N.A. for parts of 1 Mar–30 Jun) |
| G1 count by degree, 10 s–4 h | **INVALID** (declared in advance, DV1.3) | Below 30 min the pre-control imbalance cannot be reconstructed: ACE and tie-line flows are not published, and the aFRR setpoint is the controller's output |
| G2 fast corner (30–300 s) | **INVALID** (in advance) | Same; also FCR dynamics |
| G2 middle corner (300–900 s) | **INVALID** (in advance) | At the aFRR loop's own time scale: circular |
| **GRID-1b G2-slow** (world's slowest mode slower than the slowest layer, mFRR 900 s) | **PASS on proxy** | BIC picks one Lorentzian mode + white (L1; ΔBIC 4.1 over L2, 22 over the power law). Corner θ₁ = 3,898 s (65 min), bootstrap 95 % CI 3,425–4,398 s, 82 % of band variance. Wholly above 900 s (and above the robustness bound 300 s) |
| GRID-1b R1-slow (rival "set at", θ₁ ∈ [450, 1800] s) | **does not pass** | CI wholly above 1800 s; by the locked rule this arm discriminates, in GTAO's favour |
| Robustness (locked) | passes | M dropped 3,914 s, M doubled 3,869 s (both L1; < ×2); 1 Jul–31 Dec only (full mFRR coverage): L1, 3,523 s, same verdict |

Premise: A_15 coverage 0.987; corr(setpoint, QA aFRR) 0.998; mFRR variance share 0.7 %.

## How much this is worth (honest reading)
- It is one arm, low risk, and I said in advance I expected it to pass. It is fail-able only through a white
  spectrum. The strong claims (count by degree; the fast and middle interlacing) were **not tested**.
- The slowest layer (mFRR, 15 min) runs 4.3× faster than the slowest world mode it faces (65 min). That is the
  theory's "faster than its mode, not set at it" pattern, and outside the "set at" rival's ×2 window. The
  theory's own worked case gives 7–15× faster, so the ratio is on the low side, not a quantitative match (no
  ratio was predicted).
- **Rival explanations not excluded** (diagnosis, before any further data): (1) the 65-min corner may be
  man-made: hourly and quarter-hourly schedule changes with amplitudes that vary day to day survive the
  removal of the mean daily profile, so a part of the "world" is the market's own product grid; (2) mFRR is
  rarely used in Germany (0.7 % of the variance), so calling it the slowest feedback layer is weak; aFRR is the
  layer that does the work, and its own time scale (5 min) is 13× faster than the mode. Neither changes the
  locked verdict.

## Follow-up
`PREREG_GRID2.md` (Great Britain; locked before any GB data) tests the fast and middle arms where a single
synchronous area makes the pre-control imbalance reconstructable without tie-line data.
