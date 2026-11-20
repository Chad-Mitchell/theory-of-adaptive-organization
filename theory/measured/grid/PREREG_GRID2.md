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
