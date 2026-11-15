# PREREG D3-TWO-EXPONENT-OOS — out-of-sample D3S, with a calibrated renewal-vs-modulation discriminator

Queue item D3-TWO-EXPONENT-OOS (pick 8, uniform slot; ledger 45–47). Locked by the commit that adds this file (its git timestamp is the lock),
by executor queue-pick8, 15 Nov 2026, before any of the new repos was cloned or any Wikipedia revision was fetched.

## What was seen before the lock (declared)
- D3S (12 repos, `reviews/night2/SPECTRUM_MAP/checks/d3s_shuffle.json`): median Δβ 0.024; raw consecutive-log-gap correlation (S3, `M_loggaps`)
  0.28–0.47 in all 12 repos (not calibrated against a shuffle null there).
- SPECTRUM_MAP_REFEREE §6 (R6/R7): Δβ and Spearman(β, a) cannot separate renewal from Cox worlds at β ≈ 0.2.
- `power_check.py` / `power_check.out` (synthetic only, committed here): results below.
- One **in-sample** smoke test of the runner on expressjs/express (a D3S repo, not in the new sample): it reproduced D3S
  (β 0.312, a_need 0.714, M_raw 0.356) and gave M_w = 0.237 vs a shuffle-null 97.5% quantile of 0.030. So a rejection of renewal
  in the new sample is the expected outcome; the test is still out of sample and its thresholds are fixed here.

## Regime and premises (QUEUE rule 2; THEORY.md §2.4 D3 row, §2.5)
Regime: **not established** and not needed: this tests the structure of the event world (renewal vs. not), not a §2.2 optimum.
The TELEGRAPH-LINEAR-PREMISE audit (ledger 40) lists this item as OK (no linear-vs-Bayes premise involved). THEORY §2.4 states D3's sign came from a
mis-derived prediction (H19) and that D3S is a non-discriminating pass (N10). Proxies: "need" = file/article edited on a UTC day;
β = log-binned periodogram slope of binary daily series in 1/730–0.5 c/d (MATCH1 `aslib.spectral_beta`, unchanged).

## Data (fixed lists, committed with this file)
- **GitHub:** the 27 repos in `repos.txt` (none in MATCH1 or D3S; checked), reserves in `reserve.txt` used in order only if fewer than 20 repos are valid.
  Blobless full-history clones at HEAD on 15 Nov 2026 (`fetch_git.sh`). Pipeline identical to D3S: no merges, commits touching ≤ 100 files, files with ≥ 50
  edit days; a repo is valid with ≥ 5 such files.
- **Wikipedia:** 8 categories in `categories.txt`; first 40 mainspace pages by sortkey; revision timestamps via the public MediaWiki API (`fetch_wiki.py`; ≤ 10,000
  newest revisions per page); edits by users whose name ends in "bot" dropped; one "repo" per category; pages with ≥ 50 edit days; a group is valid with ≥ 5 pages.
- Seeds: GitHub repo k (0-based, list order) uses `default_rng(20261115 + k)`; Wikipedia group g uses `20261115 + 1000 + g`.

## Statistics (`d3lib.py`)
β_orig; β_shuf (each file's gaps permuted, first day kept, mean of 5); Δβ = β_orig − β_shuf; a_need (MATCH1 `fit`, Lmax 365; GitHub only);
**M_w** = pooled correlation of consecutive log gaps after subtracting each file's mean log gap; its null = 200 within-file gap shuffles (exact renewal null with each
file's own gap marginal); "exceed" = M_w above the null's 97.5% quantile. M_raw (= D3S S3) reported only (inflated by between-file scale differences; see power check).

## Predictions and decision rules (GitHub arm is primary; Wikipedia arm applies the same rules separately)
- **P1 (as the item is written; NON-DISCRIMINATING by R6 and by the power check):** Spearman(β_orig, β_shuf) > 0.3 → "passed on proxy"; else failed.
- **P2 (as written; NON-DISCRIMINATING):** median Δβ in [−0.03, 0.05] → pass; > 0.05 above band; < −0.03 below band.
- **P3 (primary, discriminating; hypothesis R = pure renewal per file):** fraction of valid repos whose M_w exceeds its null:
  **≥ 0.50 → "renewal REJECTED (failed on proxy 'within-file consecutive log-gap correlation')"; ≤ 0.15 → "renewal RETAINED"; else PARTIAL.**
- **P4 (secondary):** one-sided Wilcoxon of Δβ > 0 across valid repos: p < 0.01 and median Δβ > 0.01 → "Δβ > 0 detected (against pure renewal)"; else not detected.
- **Report only:** Spearman(β_orig, a_need) (D3 replication; positive expected under both renewal and Cox, R7), Spearman(β_shuf, a_need), medians.
- Fewer than 20 valid GitHub repos after reserves → arm reported as underpowered; no P3 verdict.

## What a verdict means (fixed in advance)
- P3 REJECTED: per-file gap order carries structure, so the edit process is not a renewal process; this is consistent with rate modulation (Cox), file life-cycle trends,
  or self-excitation (Hawkes) — P3 does **not** tell these apart (power check: all three are rejected). The "renewal explanation" of D3 (SPECTRUM_MAP v1.3 wording) is then
  not just unsupported but contradicted on proxy; H19 (MATH-CORRECTED) and N10 (PROXY-PASS, non-discriminating) keep their status; a new CLAIM_MAP row records the result.
- P3 RETAINED: renewal survives a test with power against the Cox worlds of R6 at β ≈ 0.2; record in the new row.
- No GTAO §0/§2 claim depends on this; no THEORY.md edit is made by this item.

## Power check (synthetic, committed before the lock; `power_check.out`)
20 synthetic repos per setting, 20 files each, 5000 days. P3 exceed fraction: renewal (4 settings incl. file-heterogeneous scales) 0.00–0.10 → RETAINED in all;
Cox at β ≈ 0.17–0.21 (R6 settings) 1.00 → REJECTED; weaker Cox (β 0.05–0.08) 0.75–1.00; very weak Cox (β 0.02) 0.30 (PARTIAL); life-cycle trend 1.00; Hawkes 1.00.
P4: renewal p 0.17–0.48 (not detected); Cox at β ≈ 0.2 p ~ 1e-6 (detected). P1's Spearman ranged −0.18 to 0.78 across all worlds (non-discriminating).
File-scale heterogeneity raises M_raw (0.065) but not M_w (−0.013).
