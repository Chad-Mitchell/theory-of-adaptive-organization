# PREREG D3S — gap-shuffle test of the renewal explanation of MATCH1 D3 (locked before any shuffle was computed)

Locked: 15 Nov 2026, about 09:25 ET, by the executor on branch `spectrum-map`. This commit's timestamp is the lock. No shuffled
spectrum had been computed for any real repo when this file was written. Already seen (post hoc, `checks/c4b_match1_renewal.out`):
the pooled-hazard renewal simulation tracks measured beta (Spearman 0.53, n = 21). The shuffle statistic below has never been computed.

## Hypothesis R (renewal)
The positive Spearman(beta, a_need) in MATCH1 D3 (+0.57) arises because both numbers are read off one inter-edit-gap distribution:
a burstier gap distribution (larger hazard exponent a) puts more power at low frequencies in the 1/730–0.5 c/d band.
Under R, the ORDER of a file's gaps carries little of the band power.

## Test
Repos (public GitHub, blobless clones, same pipeline as MATCH1 `code/run.py`: no merges, commits touching ≤ 100 files,
files with ≥ 50 edit days, band 1/730–0.5 cycles/day, `aslib.spectral_beta`): BurntSushi/ripgrep, Alamofire/Alamofire,
expressjs/express, pallets/flask, psf/requests, jekyll/jekyll, phoenixframework/phoenix, tokio-rs/tokio, redis/redis,
jgm/pandoc, laravel/framework, curl/curl (12; HEAD at clone time).
For each file, keep the first edit day and randomly permute its inter-edit gaps (seed 20261115; 5 permutations averaged).
beta_shuf = spectral_beta of the shuffled series. delta = beta_orig − beta_shuf.

- **S1 (primary).** Median delta over the 12 repos lies in [−0.03, +0.05]. **Kill R as the main explanation if median delta > 0.08**
  (gap order, i.e. slow modulation of the edit rate, then carries the low-frequency power). In-between values: "partial".
- **S2 (exploratory).** Spearman(beta_shuf, a_need) > 0 across the 12 repos (a_need recomputed with MATCH1's `fit`, Lmax 365).
- **S3 (report only).** Goh–Barabási memory coefficient M (correlation of consecutive gaps) pooled per repo.

Proxy labels: "need" = file edited on a day (proxy for "information needed"); beta = band slope of a binary daily series (proxy for redness).
