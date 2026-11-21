# GRID-CROSS deviations, 21 November 2026

Written Saturday 21 November 2026, 2:18 AM EST (America/New_York), on branch `grid-cross-2026-11-21`, **before any official Pass 1 selection-pressure score and before any Pass 2**. No official S score and no non-GB distance have been computed. The official comparison remains not run, and the gradient diagnostic remains **UNTESTED** (n = 1 complete d1, GB only). These notes do not invent an official score, do not relax ρ ≤ −0.5, α = 0.10, or n_min = 5, and do not re-score P25.

`PREREG.md`, `run_grid_cross.py`, and `grid_cross_lib.py` are not edited. Their hashes remain those in `LOCK.txt`:

| File | SHA-256 | Bytes |
|---|---|---|
| `PREREG.md` | `1cd856331b968e369b9b97f8ac675186140b040ae2c14e1792147489a3d4d763` | 28105 |
| `run_grid_cross.py` | `eb4bf7d42e71db961fc73d778547bcd9dde548be6babdf939917c35825d8bd89` | 4795 |
| `grid_cross_lib.py` | `d9086f8a09a91e8bb7133bdd012c3adcc94f7726800f04409439a119279dc9b4` | 12732 |

This file resolves independent-review issues S1–S3 of [PR #128](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/128) (`reviews/grid_cross_2026-11-21/REVIEW.md`). S4–S5 are disclosed in unlocked `RESULTS.md`. S6 is recorded in unlocked `DATA_SOURCES_REACHABILITY.md`. S7 is covered by tests in `tools/test_grid_cross.py`.

---

## D1 (review S1). Typo in the informational n = 9 no-tie table

The locked PREREG §8 table, and the locked constant `NO_TIE_CRIT_RHO[9]`, list −0.466667 with p = 0.096900 (35163/362880).

Exact enumeration of mid-rank Spearman on distinct ranks 1…n, over all n! permutations, was repeated for this note (the same procedure the independent review used). Official one-sided p is the share of permutations with ρ ≤ ρ_obs. The n = 5–8 rows are correct. At n = 9 (9! = 362880):

| ρ (no ties) | exact one-sided p | Role |
|---|---|---|
| **−0.483333** | 0.096900 (35163/362880) | Maximum attainable ρ with p ≤ 0.10 |
| −0.466667 | 0.106261 (38560/362880) | Next attainable value; p is *above* α = 0.10 |

The hit count 35163 and the p-value 0.096900 belong to ρ = −0.483333, not to −0.466667.

**What is unchanged.** The table is informational. The official permutation p is computed by the locked code (`permutation_p` in `grid_cross_lib.py`) on the observed, possibly tied, values. That procedure is unchanged. The locked sentence that for n ≥ 9 the effect-size floor ρ ≤ −0.5 is the stricter of the two remains true, because the correct no-tie critical value −0.483333 is still weaker than −0.5. The locked constant and the PREREG table are not silently rewritten. This is the typo-that-does-not-change-a-criterion the prereg already contemplates.

---

## D2 (review S2). UNTESTED-fill set: the prereg's {0, max} governs

**Discrepancy.** PREREG §8 says the robustness sweep assigns every UNTESTED grid the most extreme d in {0, max observed complete d} in either direction. The locked `robustness_tables` fills with `min(complete d)` and `max(complete d)`, still as a single common fill for all untested grids. If every complete d1 is ≥ 1, the two procedures differ. No official robustness table has been computed.

**Which governs:** the locked prereg clause, {0, max observed complete d}.

**Why.** d1 is defined as max(0, K_obs − K*), so 0 is the definitional floor, not an extrapolation past the design space. Filling with the observed minimum, when that minimum is not 0, never asks whether the untested grids could sit at the cost minimum. That is a weaker check than the text that was locked, and it can fail to mark a PASS as INCONCLUSIVE when the written clause would. The locked {min, max} fill is treated as an implementation slip, not as an amendment of the clause.

The locked library is not edited. The governing fill is implemented in a new, separately hashed file, written with this note and before any official score:

| File | SHA-256 | Bytes |
|---|---|---|
| `grid_cross_robustness_dev_20261121.py` | `f189de0e6d53deb42ab9c850c7e9a37e1f25e136bbb455d7981349e4c3f01a57` | 2898 |

Official Pass 2 robustness for the UNTESTED-fill sweep will use that file (`robustness_tables_prereg`). Leave-one-out, the lower-bound 0/8 sweep, and the BINDING-RUIN sensitivity remain those of the locked library; the headline is recomputed with the governing fill under the same scored-label rule. A worked example, asserted in `tools/test_grid_cross.py`: five anti-aligned complete pairs with d ∈ {2, 3, 4, 5, 6} plus an UNTESTED grid at S = 2 is PASS and robust under the locked {min, max} fill, and INCONCLUSIVE under {0, max}, because filling d = 0 yields NEITHER.

---

## D3 (review S3). All-BINDING-RUIN: the §6 / §8 sensitivity rule governs

**Tension.** §6 and the §8 robustness bullet say that if the BINDING-RUIN sensitivity leaves n < 5, that sensitivity is **UNTESTED** and the official headline follows the main §8 rule. The locked code does this: it does not flip a scored headline when the sensitivity drops below n_min, and it sets the headline to INCONCLUSIVE only if the sensitivity leaves n ≥ 5 and changes the label. A later sentence, "Not applicable, as a gradient diagnostic," lists "every complete d1 is BINDING-RUIN and dropping them leaves n < 5" as if the *headline* were **NOT APPLICABLE**. Those cannot both be executed as written.

**Which governs:** the more specific §6 / §8 sensitivity rule, as implemented in the locked library.

**Why.** That rule was written as the operational procedure and was coded that way at lock. The "not applicable, as a gradient diagnostic" list also names "n < 5", which the official diagnostic verdict already labels UNTESTED, not NOT APPLICABLE. That list is read as a narrative summary of when the diagnostic cannot be used as a scored gradient, not as a headline override. If every complete d1 is BINDING-RUIN and dropping them leaves n < 5, the sensitivity is reported as UNTESTED and the official headline follows the main §8 rule on the full complete set. Today's official result (n = 1, UNTESTED) is unaffected either reading.

No new code file is required. The locked library is not edited.
