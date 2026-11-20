# GRID-2 preregistration: Great Britain, fast-band interlacing and count

Written Friday 20 November 2026, after GRID-1b, **before downloading or inspecting any GB outcome data**
(I have seen only NESO dataset names: `system-frequency-data`, `system-inertia`, `dynamic-containment-data`).

**Why GB.** GB is one synchronous area joined to its neighbours only by HVDC links on schedules, so there is
no AC tie-line term: the pre-control imbalance is ΔP(t) = (2E(t)/f₀)·df/dt + R(t) + Dₗ·Δf, with E the published
inertia (GVA·s per settlement period), R the frequency response delivered, Dₗ load damping (2 %/Hz of demand).
R is reconstructed from the procured DC, DM and DR volumes (MW per EFA block, NESO auction results) and their
published droop curves, applied to the measured 1-s frequency.

**Layers (fixed now).** Dynamic Containment/Moderation (full delivery 1 s), Dynamic Regulation (10 s),
Balancing Mechanism and Quick Reserve (≈ 60 s to full), Slow Reserve (≈ 900 s). Rates b = 1, 1/10, 1/60,
1/900 s⁻¹. DC and DM share a speed and count as one layer.

**Period.** The 12 most recent complete months with DC, DM and DR all live and 1-s frequency available,
chosen from the file list before opening any values.

**Predictions.** Band 2 s–4 h. G1: K_sep = 4 separated modes (×2.5, ≥ 5 % each). G2 (interlacing):
θ ∈ (1, 10) s, (10, 60) s, (60, 900) s and > 900 s. Rival R1 ("set at"): θ ∈ [τ/2, 2τ].

**Verdict rules, fit and bootstrap:** as GRID-1 (Lorentzian K = 0…5 + white vs power law, BIC; day-block
bootstrap 200). G1 FAIL iff K_sep ≤ 1 or a power law with γ ∈ [1.7, 2.3].

**INVALID (premise):** (a) Mandatory Frequency Response (generator droop) volumes are not published per period.
If R from DC/DM/DR alone, with MFR added at the NESO-published typical holding (to be quoted with source before
running) varied ±50 %, moves any corner by more than ×2, the fast arms are INVALID. (b) Coverage < 90 % of
seconds. (c) Inertia per settlement period missing > 10 %.

**Kill condition:** as GRID-1: G1 FAILs in GB **and** in a CE run with open-loop seconds data, and the
speed-price diagnosis fails.

**Disclosed:** GB product times; GRID-1b's 65-min slow CE mode; general knowledge that GB frequency has
strong settlement-period (30 min) structure.

---

## Deviation DV-GB1 (appended after the lock; before downloading the GB frequency, BM or response series)
Written Friday 20 November 2026, about 10:15 AM ET. Seen so far: NESO dataset and resource names; column names
of the EAC results summary (3 rows, April 2026 DRH volumes), of the inertia file and of the frequency file;
the MFR holding workbook headers and first 3 rows per month; one day (3 Mar 2026) of Elexon BOALF and PN
records, used only to learn the format (no aggregate computed). No frequency value seen.

**DV-GB1.1 Period.** Nov 2025–Oct 2026 are the 12 latest complete months of 1-s frequency (fnew-2025-11 …
fnew-2026-10). The full reconstruction needs Elexon BM acceptance levels (BOALF) and physical notifications (PN),
≈ 40 MB per day; a year is ≈ 15 GB. **Main sample:** four calendar weeks, Monday–Sunday, fixed now:
5–11 Jan, 6–12 Apr, 6–12 Jul, 5–11 Oct 2026 (28 days). **Fast-band robustness:** all 12 months without BM.

**DV-GB1.2 Reconstruction (power balance; positive = pre-control deficit, MW).**
D(t) = R(t) + B(t) − 0.02·L·Δf(t) − (2E(t)·1000/f₀)·df/dt, with
- E: NESO outturn inertia (GVA·s) per settlement period;
- R = Σₖ Qₖ(t)·lagₖ[gₖ(−Δf)] over DCL/DCH, DML/DMH, DRL/DRH (cleared volume per EFA block, NESO
  Response-Reserve results summary; "L" products for Δf < 0, "H" for Δf > 0) plus MFR: Q = daily mean of the
  published unit holdings (primary for low, high-frequency for high; MWh/24), g linear from ±0.015 to ±0.5 Hz;
- gₖ, the published curves: DC 0 % inside ±0.015 Hz, 5 % at ±0.2 Hz, 100 % at ±0.5 Hz; DM 5 % at ±0.1 Hz,
  100 % at ±0.2 Hz; DR linear to 100 % at ±0.2 Hz (NESO DC/DM/DR service descriptions, documents 187066,
  246741, 246766);
- lagₖ: first-order, τ = FAT/3 (DC, DM 1/3 s; DR and MFR 10/3 s); robustness τ = FAT;
- B = Σ over BM units of (latest accepted BOAL − PN), linearly interpolated, while an acceptance is in force;
  0 otherwise (minute data, interpolated to 1 s);
- L = 28 GW (±50 % in the robustness bucket); df/dt by central difference.
Not included (disclosed): NESO trades on interconnectors, non-BM reserve, quick/slow reserve outside BM.

**DV-GB1.3 Fit.** Welch, 4-h Hann segments, 50 % overlap, periods 2 s–4 h, 20 bins/decade, deterministic
removal as GRID-1 (mean per second-of-hour and per minute-of-day over the sample). θ bounded to
[0.5 s, 30 days]. K = 0…5 Lorentzian + white vs power law + white, BIC. Bootstrap: 200 resamples of whole days.
Separated as GRID-1 (×2.5, ≥ 5 % of band variance).

**DV-GB1.4 Arms and INVALID rules (conservative).**
- G1 and the four G2 corners scored on the main sample (full reconstruction) by the locked rules.
- **Corner-wise INVALID:** a corner (or the count) is INVALID if it moves by more than ×2, or the chosen K changes,
  under any of: MFR ×0.5 or ×1.5; L ×0.5 or ×1.5; lags τ = FAT; B dropped (for corners < 60 s only B dropped
  is allowed to change nothing; for slower corners B is essential, so dropping B is reported, not used).
- **Fast-band robustness:** the 12-month run without B, band 2–120 s; if its verdict on the (1, 10) s corner
  differs from the main run's, that arm is NEITHER.
- Coverage: ≥ 90 % of seconds with frequency, and inertia for ≥ 90 % of settlement periods, else INVALID.
- **GRID-S S1 (locked `8b0ef50`):** on the main-sample D, 15-min means, 1-day segments (not 7: only 28 days),
  periods 30 min–12 h, day-block bootstrap, same rules and windows.
- **GRID-S S2:** BLOCKED (2026 German aFRR setpoint served only by a form button on
  https://www.netztransparenz.de/de-de/Regelenergie/Daten-Regelreserve/Sekündliche-Daten).
