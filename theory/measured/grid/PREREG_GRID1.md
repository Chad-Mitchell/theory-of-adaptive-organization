# GRID-1 preregistration: do Continental Europe's reserve layers interlace the open-loop imbalance spectrum?

Written Friday 20 November 2026, **before downloading or inspecting any outcome data** (no frequency or NRV
values from any year have been downloaded or viewed by me; only page link lists and dataset names). The commit
time is the record. Any change after this commit is a deviation, logged in `grid/DEVIATIONS.md`, and may not
alter a verdict.

## Claim under test (THEORY.md (iii), CT21, L1–L2)
In Model S, a world with J separated real time scales (sum of OU modes, rates a_1 < … < a_J) is best tracked
by exactly J layers (once stakes are large), and the layer rates interlace the world's:
a_1 < b_1 < a_2 < b_2 < … < a_J < b_J (each layer faster than its mode, slower than the next mode). A world
with one real time scale, including a random walk, needs at most one layer (L1). A continuum (power law
other than a random walk) has no exact finite design (L3).

## System and layers (fixed now, from product rules, not from data)
Continental Europe synchronous area, German LFC block (four TSOs, NRV = "Netzregelverbund"). Layers =
reserve products with distinct full-activation times (FAT), as defined by the products in 2022:
FCR 30 s, aFRR 5 min (300 s), mFRR 12.5 min (750 s) (mFRR was 15 min before MARI; in 2022 Germany still
used 15 min; **primary mapping uses the 2022 German values: FCR 30 s, aFRR 300 s, mFRR 900 s**).
Primary layer time constant τ_j = FAT_j; robustness mapping τ_j = FAT_j / 3 (first-order 95% rise). Layer
rates b_j = 1/τ_j. Intraday and day-ahead markets are excluded (schedules, not feedback layers).

## World (open-loop imbalance)
Period: calendar year 2022 (the last year with an open second-wise frequency file). Signal:
D(t) = NRV(t) + β·Δf(t), where NRV(t) is the German second-wise netted aFRR+mFRR activation (MW, sign as
published, deficits positive) and β·Δf the German share of FCR plus load self-regulation,
β = 3,450 MW/Hz (German FCR ≈ 570 MW per 200 mHz plus 1 %/Hz of ≈ 60 GW load). Inertia is ignored
(corner M/λ ≈ 3 s, below the band). Band: 10 s to 4 h.
Preprocessing (fixed): remove the daily and hourly deterministic schedule components by subtracting the
mean profile per second-of-hour and per minute-of-day computed over the year (deterministic seasonality is
not a stationary Gaussian mode, THEORY §5); gaps ≤ 60 s linearly filled, longer gaps split segments.
Spectrum: Welch, 4-h Hann segments, 50 % overlap, log-binned (20 bins/decade) over 10 s–4 h.
Fit: log-PSD fitted by (i) K Lorentzian modes Σ_k A_k/(1+(2πfθ_k)²) + white floor, K = 0…5, and (ii) a
power law A f^{−γ} + white floor. Model choice by BIC on the log-binned points. Corner CIs by a day-block
bootstrap (200 resamples).
**Separated** modes: corners pairwise ≥ ×2.5 apart (the closest product ratio, 300 s / 750 s, is 2.5, and
900/300 = 3) and each carrying ≥ 5 % of band variance; K_sep is the count of separated modes in the chosen
model. The mode count of the world is K_sep.

## Predictions (numeric, with ranges)
- **G1 count (iii):** K_sep = 3 within the band.
- **G2 interlacing (L2), primary mapping (τ = 30, 300, 900 s):** θ_3 ∈ (30, 300) s, θ_2 ∈ (300, 900) s,
  θ_1 > 900 s (θ_1 ≤ 4 h, the band edge). Robustness mapping (τ = 10, 100, 300 s): θ_3 ∈ (10, 100) s,
  θ_2 ∈ (100, 300) s, θ_1 > 300 s.
- **Rival R1 ("set at the world's scale"):** θ_j ∈ [τ_j/2, 2τ_j]: [15, 60] s, [150, 600] s, [450, 1800] s.
- **Rival R0 (engineering history; no relation):** no prediction on corners; GTAO is supported over R0 only
  if G1 and G2 both pass.

## Verdict rules
- **G1 PASS** iff K_sep = 3. **G1 FAIL** iff K_sep ≤ 1 with the Lorentzian model chosen, or the power-law
  model chosen with γ ∈ [1.7, 2.3] (a random walk in band: L1 caps the layers at one, CE runs three).
  K_sep = 2 or 4–5: NEITHER. Power law chosen with γ outside [1.7, 2.3]: **OUT OF SCOPE** (L3, continuum).
- **G2** (only if K_sep = 3): **PASS** iff each corner's bootstrap 95 % CI lies inside its interval under the
  primary mapping, or under the robustness mapping (both mappings are reported; PASS requires that the
  passing mapping also beats R1, i.e. at least one corner's CI is outside R1's interval). **FAIL** iff under
  both mappings at least two of the three corners have CIs wholly outside their intervals. Otherwise NEITHER.
- **R1** scored by the same rule (PASS iff every CI overlaps its R1 interval).
- **INVALID (premise):** NRV second-wise coverage < 90 % of 2022; or the chosen model or any corner moves by
  more than ×2 when β is changed by ±50 % (reconstruction not robust); or the residual of D(t) is dominated by
  the ACE term (variance of β·Δf > variance of NRV in the 10–300 s band would mean the FCR term, not NRV,
  carries the world, and the fixed β is the test).

## Kill condition
GTAO's layer-count claim (iii) is **refuted for engineered power grids** if G1 FAILs here **and** in the
GB replication (same rule; layers DC/DM ≈ 1 s, DR ≈ 10 s, Quick Reserve ≈ 60 s, Slow Reserve ≈ 900 s; band
2 s–4 h; open-loop GB imbalance = (2E/f0)·df/dt + response implied by procured DC/DM/DR volumes and their
published droop curves; GB is scored only after the CE verdict is written), and the one preregistered
diagnosis fails: that the extra layers are **actuator-cost tiers** (speed-priced upkeep, Model S+ E2,
outside Model S's fixed upkeep). That diagnosis predicts capacity prices fall with product speed tier
(FCR > aFRR > mFRR, €/MW/h, 2022 annual means of open regelleistung.net tender results); if FCR's price is not
above aFRR's, the diagnosis fails and the kill holds.

## What I already know (disclosed)
- Product times and that CE runs three feedback layers (FCR, aFRR, mFRR); GB's product times as listed.
- General literature: CE frequency shows deterministic jumps at hour boundaries (schedule steps) and
  heavy-tailed increments (e.g. Gorjão et al. 2020, Nature Communications, which I know from abstracts); I
  have not seen a spectrum of German NRV second-wise data and do not know whether it has corners.
- TSOs dimension aFRR+mFRR jointly from probabilistic imbalance distributions; that is a size rule, not a
  time-constant rule.
- Earlier repo results: CAISO stakes tests (STAKES_EXOGENOUS, STAKES_SHIFT_CAISO) were inconclusive; they
  did not touch layer timing.

## Data and access (as found before this commit)
- CE second-wise frequency 2012–2022: open static zips (GET) on netztransparenz.de.
- German second-wise NRV: served only by an ASP.NET postback button (`btnHiddenNrvSecondlyValueFileDownload`)
  on netztransparenz.de "Sekündliche Daten"; no static link. The netztransparenz API portal needs credentials;
  ENTSO-E Transparency API needs a token (account). No sign-in or account will be used.
- Capacity prices: regelleistung.net tender results (open download, to be checked).

---

## Deviation DV1 (appended after the lock; the text above is unchanged)

Written Friday 20 November 2026 after Chad downloaded the public 2022 files (no login) to
`/workspace/gtao-grid-data/`, **before computing any spectrum or any outcome-bearing statistic**. What I have
seen of the data: file names, sizes, column headers, and the first 3–4 rows of each file (needed to read the
formats). That is all.

### DV1.1 Data substitution
Preregistered: German second-wise NRV-Saldo (aFRR + mFRR), 2022. **Not available** (the site's picker starts
in 2026). Substitute:
- `SRL_Soll_20220101_20221231.csv`: German aFRR **setpoint**, 1 s, full year (`GERMANY_aFRR_SETPOINT_[MW]`).
- `Aktivierte aFRR/mFRR qualitaetsgesichert`: quality-assured activations, 15 min, full year, Germany,
  positive and negative columns.
- `2022_frequenz.zip`: CE frequency, 1 s, Jan, Feb, Apr–Jun (March missing).

### DV1.2 Circularity and what the substitute can and cannot show
The aFRR setpoint is the output of the TSOs' PI controller acting on the area control error, not the
pre-control imbalance. The pre-control German area imbalance is
ΔP_DE(t) = A(t) + M(t) + F_DE(t) + ACE_res(t), with A the aFRR activation, M the mFRR activation, F_DE the
German FCR + self-regulation response (≈ β·Δf) and ACE_res the part not yet corrected, which flows over the
tie lines to the rest of Continental Europe. ACE and tie-line flows are **not published** at seconds. On time
scales shorter than the aFRR loop (≲ 5–15 min), ACE_res is a large, unobserved part of ΔP_DE (a German deficit
is met ≈ 80 % by the rest of CE through the ties), and A(t) there is shaped by the controller's own roll-off,
so a corner near 300 s in A could be the controller's pole, not the world's. On time scales of **30 min or
more**, aFRR and mFRR have fully acted, frequency is restored (F_DE ≈ 0) and ACE_res is small, so
D(t) = A(t) + M(t) is an open-loop reading of the German imbalance. The frequency-implied FCR share
(β·Δf) is negligible there and is not used.

### DV1.3 Which arms stay valid (declared in advance)
- **G1 (count, band 10 s–4 h): INVALID.** The band below 30 min cannot be reconstructed open-loop (DV1.2).
- **G2 fast corner θ_3 ∈ (30, 300) s: INVALID** (needs ACE/tie flows and FCR dynamics at seconds).
- **G2 middle corner θ_2 ∈ (300, 900) s: INVALID** (sits at the aFRR loop's own time scale: circular; and
  mFRR resolves only ≥ 30 min).
- **G2-slow (the one scorable arm), with its rival:** Interlacing a_1 < b_1 requires the world's slowest mode to
  be slower than the slowest layer (mFRR, τ = 900 s; robustness 300 s). Rule on D_15 (below):
  - **PASS** iff the chosen model has a separated Lorentzian corner with bootstrap 95 % CI wholly above
    900 s.
  - **FAIL** iff the chosen model is white in band (K = 0, or power law with γ < 0.3), i.e. no world variance
    beyond the slowest layer for it to track.
  - **NEITHER** otherwise (including a corner whose CI reaches below the resolvable limit of 900 s).
  - **R1-slow** (rival "set at", θ_1 ∈ [450, 1800] s): PASS iff the slowest corner's CI overlaps
    [450, 1800] s. The arm **discriminates** only if the corner CI lies wholly above 1800 s (GTAO PASS, R1 not)
    or wholly in [900, 1800] s (both PASS: no discrimination).
  - A power law with γ ∈ [0.3, ∞) is read as variance beyond the slowest layer: PASS for G2-slow, R1-slow
    NEITHER (no corner).
  - **Risk disclosed:** I expect this arm to pass (imbalances have slow drifts), so it is a weak, low-risk
    test. It is fail-able only through a white spectrum, which the theory forbids and the "set at" rival does
    not need.
- **Kill condition:** cannot be reached in this run (G1 is INVALID). It stands as written for any future run
  with open-loop seconds data.

### DV1.4 Reconstruction (exact)
- A_15: 15-min means of the aFRR setpoint over each quarter hour [00:00, 00:15) CET/CEST as given in the files,
  requiring ≥ 90 % of the 900 s present.
- M_15: German mFRR, positive minus negative (`Deutschland (Positiv)` − `Deutschland (Negativ)`).
- D_15 = A_15 + M_15 (MW; the sign of the setpoint as published, positive = positive aFRR, i.e. deficit).
- Premise check (not an outcome): the correlation of A_15 with the QA aFRR (positive − negative). If it is
  < 0.9, the setpoint does not represent the activation, and the run is **INVALID**.
- Deterministic removal: subtract the mean per quarter-hour-of-day (96 slots) over the year; this replaces
  "per second of hour and per minute of day", which the 15-min series cannot resolve.
- Spectrum: Welch on D_15, 7-day Hann segments, 50 % overlap; gaps shorter than 1 h linearly filled, longer
  gaps split segments. Log-binned (20 bins per decade) over periods 1 h–3.5 days. The same K = 0…5
  Lorentzian + white and power-law + white fits, chosen by BIC. A corner is resolvable only for θ ≥ 900 s
  (corner frequency ≤ 1/3 of the 1/(30 min) Nyquist). Separated means ×2.5 apart and ≥ 5 % of band variance,
  as before. Bootstrap: 200 resamples of whole 7-day segments.

### DV1.5 Coverage and INVALID rules (adjusted conservatively)
- Coverage: ≥ 90 % of 2022 quarter-hours valid for A_15 **and** for M_15, or INVALID (as written, applied to
  both series).
- The β ±50 % robustness rule is replaced by: the chosen model and the slowest corner must not move by more
  than ×2 when M_15 is (a) dropped and (b) doubled; otherwise INVALID. A stricter version of "the
  reconstruction is not the test".
- The "FCR term dominates" rule is moot in this band (β·Δf is not used) and is replaced by the setpoint
  check above.
- The frequency file is not used by any valid arm; it is not opened for values.

## Deviation DV2 (implementation; before any spectrum)
Two attempted runs of `grid1_run.py` stopped at the premise step because of parsing bugs (the QA files use
"." as a thousands separator and "N.A." entries; the setpoint quarters were first aligned by position). Printed
so far: setpoint 15-min coverage 0.987 and its variance (7.8×10⁴ MW²); no spectrum, fit or corner. Fixes:
(1) quarters are joined by (date, start time, occurrence) so missing quarters and the duplicated DST hour align;
(2) the `Deutschland` column is N.A. for 1 Mar–30 Jun 2022 (11,708 quarters, 33 %), which would fail the
90 % coverage rule as written; the four TSO columns are complete and their sum equals `Deutschland` exactly
wherever both exist (max |difference| 2×10⁻¹³ MW, aFRR and mFRR, both signs), so M_15 and the QA aFRR check
use the sum of the four TSO columns. This is the same quantity, not a new proxy; no rule changes.

### DV2 erratum (before any spectrum)
DV2's statement that "the four TSO columns are complete" was wrong: I had checked only TenneT. N.A. counts per
TSO (each sign, both aFRR and mFRR files): 50Hertz 8,828, Amprion 2,880, TenneT 0, TransnetBW 2,016 quarters;
`Deutschland` is N.A. exactly when any TSO is. The TSO sum therefore adds no coverage. Premise numbers from the
third attempt (no spectrum computed): coverage A_15 0.987, coverage M_15 0.666, corr(A_15, QA aFRR) 0.998,
var(M_15)/var(A_15) = 574/77,957 = 0.7 %.

## GRID-1 verdict (as locked + DV1): INVALID by premise
M_15 coverage is 0.666 < 0.90 (DV1.5). No arm is scored. A follow-up with a stated data rule is preregistered
in `PREREG_GRID1b.md` before any spectrum is computed.
