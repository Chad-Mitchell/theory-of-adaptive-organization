# SENSE-CELL preregistration: the cell-scale price structure (theta) and binding ratio (beta_phys), E. coli chemotaxis adaptation

Status: LOCK FILE. Timestamp of record = git commit time of this file on branch `q-sensecell` of the private repo
`Chad-Mitchell/theory-of-adaptive-organization` (ledger 187 claims the item; `LOCK.txt` holds the sha256 of this file and of `sensecell_calc.py`).
Written before the Keegstra source data were opened, before the Lan et al. Fig. 3c/4a curves were read, and before any theta_eff or beta_phys number was computed.
Out-of-cycle, unscored (queue protocol v2; dispatched by Ace for Chad, t1919u). Base: origin/main 77dd71c, THEORY.md v1.4.17, CLAIM_MAP v2.37.
THEORY.md and CLAIM_MAP are not edited by this item.

## 0. What I had already seen before locking (disclosed)
- Lan et al. 2012 (Nat Phys 8:422, free full text PMC3378065, SI from the publisher): the error-energy relation eps ~ eps0 exp(-alpha dW) with alpha=(kR+kB)/(2kB); the speed-accuracy-energy relation Wdot ~ c0 sigma_a^2 omega_m ln(eps0/eps); text numbers: DG0 ~ 29 kT per SAM methylation cycle, "a modest 20% efficiency leads to a maximum adaptation accuracy of ~99%", ~95% accuracy in starving cells (Fig. 5c), ~10^4 receptors, adaptation time ~10 s, ~3x10^4 kT/s (~10^3 ATP/s), 5-10% of a flagellar motor's cost.
- Keegstra et al. 2017 (eLife 6:e27455, PMC5809149): definitions (adaptation precision Pi = a_adapted,i / a0,i, so eps_Lan = |1 - Pi|), and the abstract-level summary numbers in the figure legend (mean +- sd of Pi across cells 0.79 +- 0.32; CV(a0) = 0.23; CV(Pi) = 0.40; temporal noise eta = 0.44). I have NOT seen the per-cell values or the mean a0.
- A back-of-envelope with Lan's anchor (below) before locking suggested beta near 5-15 at the measured accuracies, i.e. borderline for the band in H2; I expect INCONCLUSIVE on H2 and PASS on H1, and say so now.

## 1. Theory provenance and what is tested
- THEORY §2.3 / FRAMEWORK §3.11 (Chad's physics position, made measurable): the thermodynamic floor binds tightly at the cell and constrains little at firm scale; beta_phys = actual cost / thermodynamic floor is near 1 where physics constrains design (FRAMEWORK §3.11 table: cell "measurable in principle"; "if beta_phys ~ 1-10 for a sensing system, the thermodynamically priced class should be the one selected").
- THEORY §2.5 / CLAIM_MAP N12 (refereed): the formal onset exponent is -(1+theta) for precision priced as precision^theta and -1 for exact reset reads or per-nat (information-rate / entropy) pricing; the tracking-layer effort elasticities are alpha/(2alpha-1), 1/(2alpha-1) only for theta = 1 (THEORY §2.2 precision-effort row). N12 referee C1 (`reviews/night2/N12_REFEREE.md` §6): at a cell, theta is the quantity to measure.
- Premise bridge (stated, not proved): Lan's relative adaptation error eps (|<a>-a0|/a0, a bias of the adapted state) stands in for the tracking layer's estimation error, and 1/eps (or 1/eps^2) for precision. The theory's precision is the inverse variance of read noise; eps is not that. This bridge is the weakest link; the result is labeled accordingly (§6).

## 2. Measured / literature inputs and their fixed use
| Symbol | Source | Use |
|---|---|---|
| DG0 = 29 kT per cycle | Lan 2012 text (cites their ref 26) | actual fuel free energy per methylation cycle |
| BP line eps = eps0 exp(-alpha dW), dW <= DG0 | Lan 2012 Eq. 8, Fig. 4a ("BP line agrees exactly with Eq. 8") | the floor: minimum dissipation per cycle for accuracy eps |
| alpha = 1/(2(1-a0)) | Lan: alpha=(kR+kB)/(2kB), a0=kR/(kR+kB) | a0 = mean steady-state kinase activity of Keegstra Fig. 1 cells (source data `elife-27455-fig1-data1`) |
| eps_obs = 1 - mean_i(Pi_i) | Keegstra Fig. 1d per-cell adaptation precision | measured adaptation error of E. coli cells |
| eps0 | **Method A (primary, text only):** the anchor dW = 0.20*DG0 = 5.8 kT at eps = 0.01 on the BP line, so eps0 = 0.01*exp(5.8*alpha). **Method F (sensitivity):** eps0 read from Fig. 3c/4a. | calibrates the BP line |
Caveat fixed now: under Method A, beta at eps = 0.01 is 5.0 *by construction* (1/efficiency); the test has content only through eps_obs, alpha and the shape of the line. Lan's 20% is an assumed efficiency chosen to match ~99%, not a measurement.

## 3. Loss and rival family (PREREG-LOSS-LOCK)
No estimator is scored: the outputs are deterministic ratios and exponents compared with bands, so the squared-error default is moot; stated as such. Rival family named up front for each hypothesis (below). A hypothesis whose rival cannot be reached by the inputs is labeled non-discriminating.

## 4. Hypotheses, quantities, and rules (mirrored: PASS needs the interval to clear the edge by kappa; FAIL needs it to clear the other side by kappa; kappa = 0.15)
Interval = percentile bootstrap 95% over Keegstra cells (B = 2000, rng seed 20261118) for (a0, Pi); alpha, eps_obs, eps0 recomputed per replicate (Method A). The verdict is *robust* only if Method F gives the same label; if the two methods disagree the label is INCONCLUSIVE.
`verdict_band_upper(lo, hi, edge)` (in `sensecell_calc.py`, locked, self-tested): PASS iff hi <= 0.85*edge; FAIL iff lo >= 1.15*edge; else INCONCLUSIVE.

- **H1 (class selected by the floor; the "theta" of the cell).** Quantity: theta_eff = d ln(dW) / d ln(P) at fixed adaptation speed (Lan: Wdot proportional to omega_m ln(eps0/eps)), conservative convention P = 1/eps: theta_eff = 1/ln(eps0/eps) (the P = 1/eps^2 convention halves it and is reported only). Evaluated over eps in [0.01, 0.05] (Lan: ~99% and ~95%). Claim: per-nat class, theta_eff <= 0.5 (midpoint between per-nat, theta -> 0, and the default linear precision price theta = 1). Rival: theta = 1 (linear precision pricing; the default behind THEORY §2.2 elasticities alpha/(2alpha-1), 1/(2alpha-1)). Rule: verdict_band_upper(interval of theta_eff over the range, edge 0.5). Reading: PASS on proxy "adaptation-accuracy channel, Lan BP line": N12's -1 class (not -(1+theta) with theta = 1) is what the cell's accuracy channel prices. FAIL: the default theta = 1 stands for this channel. This tests the theory's *floor assignment* against a published physical model; it does not test any cell data of effort.
- **H2 (binding at the cell).** Quantity: beta_phys = DG0 / dW_BP(eps_obs), dW_BP = ln(eps0/eps_obs)/alpha (infinite if eps_obs >= eps0). FRAMEWORK §3.11 band: beta in [1, 10]; rival: non-binding physics, beta >= 100 (neurons are recorded at ~10^5 in FRAMEWORK §3.11). Rule: verdict_band_upper(interval of beta, edge 10). beta < 1 would signal an error in inputs (second law), not a verdict.
- **H3 (cross-scale ordering).** Claim: beta_cell <= beta_neuron/100 = 10^3 (neuron value ~10^5 as recorded in FRAMEWORK §3.11 from Laughlin et al. 1998; not re-verified here). Rule: verdict_band_upper(interval of beta, edge 1000). Non-discriminating if H2 is INCONCLUSIVE with hi < 1000 (then H3 can only pass trivially; it is reported, not counted as support).
- **H4 (observed class equals selected class).** Not testable with public data: no dataset gives E. coli adaptation or sensing effort as a function of stakes (benefit of tracking) and of the drift level of the stimulus, with measured price. **Verdict fixed now: INCONCLUSIVE (data gap).** Needed: single-cell FRET or behaviour under ligand ensembles with controlled fluctuation level and recorded energy state (Keegstra-style, not found public).
- Not scored, reported: tracking-layer elasticities implied by theta_eff (a = alpha_w theta/(alpha_w(theta+1)-1), b = theta/(alpha_w(theta+1)-1), where alpha_w is the world's spectral slope, unmeasured here), and beta_Landauer = DG0/(kT ln 2) ~ 42 bits-equivalent per cycle.

## 5. What each outcome means for the cross-scale bet
No outcome changes N6 or N13 (both OPEN): this is a Tier-3, literature-value consistency check on a different substrate, not a strongly-selected-system optimality test (no effort-vs-input data; H4). PASS on H1/H2 would say only that the theory's price-class and binding statements are *consistent with the published cell physics*. FAIL on H1 or H2 would say the theory's cell-scale physics sentence (FRAMEWORK §3.11) is wrong *as written on this proxy* (no field kill).

## 6. Limits (fixed now)
L1 Lan's eps-vs-dW curve is a model result (Fig. 3c/4a, 10^4 random models), supported in cells only qualitatively (Fig. 5: speed falls with ATP, accuracy ~95% unchanged). L2 Method A inherits Lan's assumed 20% efficiency. L3 The receptor-read (Berg-Purcell) channel, whose cost is roughly linear in receptor number, is a second channel with theta ~ 1 and is not scored. L4 Keegstra's Pi comes from saturating-step FRET with substantial measurement noise; its cell-to-cell spread inflates the bootstrap interval, which is the conservative direction for PASS. L5 The cell-to-cell variation in Keegstra's data is expression noise, not selection; it is used only to put an interval on the means. L6 No paywall sign-in; Nat Phys main text read via the free PMC author manuscript.
