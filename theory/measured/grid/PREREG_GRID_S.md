# GRID-S preregistration: is the German 65-minute mode the world's, or the market's hourly schedule step?

Written Friday 20 November 2026, about 10:05 AM ET, **before downloading or inspecting any GB data and any German
data after 2022**. Known: GRID-1b found one slow mode in the 2022 German imbalance, θ_DE = 3,898 s (CI 3,425–4,398 s),
when German day-ahead and most scheduling ran on **hourly** products.

**Two accounts.**
- **W (world, the theory's reading):** the mode is a property of the imbalance's physical drivers (load and
  renewable forecast errors). Its correlation time does not follow the market's product period.
- **M (market schedule step):** the mode is produced by schedule changes at product boundaries, so its time
  scale scales with the product period P: θ = c·P with c = θ_DE / 3600 s = 1.08 (CI 0.95–1.22).

**S1, Great Britain (half-hour settlement, P = 1800 s), run with GRID-2 on the same reconstructed GB imbalance,
on 15-min means of it, with the GRID-1b fit (Lorentzian K = 0…5 + white vs power law, BIC, periods 1 h–3.5 days)
extended to periods 30 min–3.5 days (1-s data allow it).**
- M predicts a separated corner in [1,300, 2,900] s (1.08 × 1800 s, ×/1.5 for the CI and fit error).
- W predicts the slowest separated corner lies outside that window, with no tie to 1800 s; W gives no window
  of its own, so S1 can support M or disfavour it, not confirm W.
- **M-S1 PASS** iff a separated corner's bootstrap CI lies wholly inside [1,300, 2,900] s; **M-S1 FAIL** iff no
  separated corner's CI overlaps it; otherwise NEITHER.

**S2, Germany after the 15-minute day-ahead products (SDAC 15-min market time unit, from 1 October 2025):**
first half of 2026, same reconstruction and code as GRID-1b (aFRR setpoint, 15-min means, plus mFRR), same rules.
- W predicts θ_2026 ∈ [2,600, 5,850] s (θ_DE ×/1.5) and no new separated corner in [650, 1,460] s.
- M predicts the hourly step's mode weakens and a corner in [650, 1,460] s (1.08 × 900 s ×/1.5) appears and
  carries more variance than any corner in [2,600, 5,850] s.
- **W-S2 PASS** iff the dominant (largest-share) separated corner's CI lies in [2,600, 5,850] s and no separated
  corner's CI lies wholly in [650, 1,460] s. **M-S2 PASS** iff the dominant corner's CI lies wholly in
  [650, 1,460] s. Otherwise NEITHER for both. Resolution: with 15-min means the corner floor is 900 s, so for S2
  the fit uses 1-min means of the setpoint (periods 5 min–3.5 days) and aFRR alone (mFRR at 15 min only
  enters as a robustness run).
- **Premise / INVALID:** S2 needs the 2026 German aFRR setpoint at 1 s, which is not yet on the box; if it cannot
  be fetched without a browser form, S2 is BLOCKED and the exact URL is reported.

**Disclosed risks:** schedule changes also happen at quarter hours in 2022 (intraday 15-min products existed),
and GB's settlement-period ramps are well known; a corner near 30 min in GB was a plausible prior.

---

## Deviation DV-S2 (appended after the lock; before computing anything on the 2026 German files)
Written Friday 20 November 2026, about 11:00 AM ET. Chad downloaded (browser, no login) to
`/workspace/gtao-grid-data/de2026/`: six monthly 1-s aFRR setpoint files, Jan–Jun 2026; the **operational**
("betrieblich") activated aFRR at 15 min; the quality-assured activated mFRR at 15 min. Seen: names, sizes,
SHA-256, headers and the first one or two rows of each file.

- **aFRR operational, not quality-assured.** It enters only the premise check corr(A₁₅, activated aFRR) ≥ 0.9
  (as GRID-1b). The threshold is kept; operational data can only make this check harder to pass. Below 0.9:
  INVALID.
- **mFRR** enters only the robustness run (as locked). Gaps are treated as in GRID-1b (zero where missing, if its
  variance share where present is < 5 %; else the robustness run is reported as not available).
- **Method fixed here (the lock said "1-min means, periods 5 min–3.5 days" and "same rules"):** 1-min means of
  the setpoint (≥ 54 of 60 s present); remove the mean per minute-of-day (1,440 slots) over Jan–Jun; Welch with
  7-day Hann segments, 50 % overlap, gaps ≤ 10 min filled, longer gaps split segments; log-binned, periods
  5 min–3.5 days; Lorentzian K = 0…5 + white vs power law + white by BIC; θ ∈ [60 s, 30 days] (the shortest
  corner resolvable at 1-min sampling); separated ×2.5, ≥ 5 % of band variance; bootstrap of whole 7-day
  segments, 200 resamples. Coverage ≥ 90 % of minutes, else INVALID.
- **Comparability check (added, conservative):** the 2026 data are also scored with the exact GRID-1b method
  (15-min means, periods 1 h–3.5 days, θ ≥ 900 s). That method cannot resolve the M window [650, 1,460] s, so it
  can only test W's window. If the two methods disagree on W-S2, the result is NEITHER.
- Verdicts as locked: W-S2 PASS iff the dominant separated corner's CI lies in [2,600, 5,850] s and no separated
  corner's CI lies wholly in [650, 1,460] s; M-S2 PASS iff the dominant corner's CI lies wholly in
  [650, 1,460] s; otherwise NEITHER.
