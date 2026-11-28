# Independent review 2 of PR #93 (REACH open items, THEORY v1.4.25, CLAIM_MAP v2.44)

Wednesday 18 November 2026, night ET (America/New_York). Reviewer: a Grok Bot executor acting as an independent, hostile-but-fair reviewer. I wrote none of PR #93. I reviewed main at 41c0140 in a fresh clone. Everything was re-derived with my own code, in `review2_checks/`: `my_n47_n49.py` (+`.out`), `hub_nulls_hm.py` (+`.out`), and `hub_nulls_v2.py` (+`.out`, a lognormal attempt that diverged, kept as evidence). File:line references are to 41c0140. Nothing was posted or sent.

## Verdict: READY-WITH-FIXES

The new math (N47, N49) is right as algebra. I re-derived every closed form and my code agrees. The prior-art calls are fair, apart from one misread phase diagram. One claim drawn from the SDSS data check was not supported, because the null behind it had failed its own validation. That is the blocker. All fixes below are applied in this PR (THEORY v1.4.26, CLAIM_MAP v2.45). No status label changes.

## BLOCKERS

**B1. "Nearest-neighbour in-degree is matched by a two-point-matched null" rests on a null that failed its own check.**
- Where: `theory/COSMIC_WEB.md:93` and `:160`; `measurement/CLAIM_MAP_v2.md:389` (N39), `:398` (N48), and the `:77` note; the `THEORY.md:529` changelog.
- The problem: the same lognormal null is called INCONCLUSIVE for the radius graph, because it over-clusters by 1.2 to 1.6 at 2 to 7 Mpc/h and by 2.5 at 0.6 Mpc/h. At this density (n̄ = 0.030 h³/Mpc³) the k = 20 neighbours span about 5 Mpc/h, which is inside the over-clustered range. So the agreement (2.50 against 2.52 ± 0.06) cannot be evidence that "two-point clustering alone gives" Coutinho et al.'s broad in-degree.
- With my better null the same statistic ranges from 2.33 ± 0.12 to 2.88 ± 0.17 across members that share one two-point function.
- Under the repo's own rule (a mismatched proxy is INVALID, not a result), this is INCONCLUSIVE.
- **Fix (applied):** reworded to INCONCLUSIVE in COSMIC_WEB §0 item 3, §2b item 2 and §7, in N39 and N48, and in BRIEF. Coutinho et al.'s observation stays PRIOR ART.

## SHOULD-FIX (all applied)

**S1. The §8 prereg spec is not sound as written** (`COSMIC_WEB.md:168–170`).
- (a) Radius-graph degree is counts-in-spheres around galaxies. Its mean is a two-point quantity, but its variance and the top-1% share depend on the three-point function and higher. So a "two-point-matched" null does not determine S1. The branch "exceeds two-point clustering (higher-order gravitational structure)" therefore reads a property of the chosen null as a property of the web.
- Evidence (§2c of COSMIC_WEB, my run): three members of one null family, at the same ξ, give S1 at ⟨k⟩ = 4 of 0.069 ± 0.015, 0.092 ± 0.014 and 0.157 ± 0.044.
- (b) The "Gaussian-field-based mock" gate looks infeasible at ℓ ≈ 1.4 Mpc/h. To reach ξ_s ≈ 16 at 0.6 Mpc/h, a fine-grid lognormal (512³, cell 0.375 Mpc/h, cell-averaged zero lag) needs a Gaussian variance of about 6.5. Calibration then diverged: variance 6.5 → 15.3 → 22.6 in three passes, and the final mock was too clustered to tune ⟨k⟩ = 4 (`review2_checks/hub_nulls_v2.out`).
- (c) No treatment of redshift-space anisotropy or fibre collisions in the nulls.
- **Fix:** §8 item 3 now makes N-body-based halo-occupation mocks the primary null, with RSD and fibre collisions handled alike in data and mocks. Secondary nulls must be named with their free parameters fixed in advance. Item 5's interpretation now refers to the named null.

**S2. N49: "interior and continuous iff |μ| ≤ σ" mislabels the criterion, and assumptions are missing** (`TORUS.md:61–62`, `:81`; CLAIM_MAP `:395`, `:399`; `REACH.md:190`; `price_maps.py:8`).
- For |μ| > σ the optimum after the jump is interior too. The criterion is about concavity and continuity in price.
- The optimum is 0 for c ≥ c₀(μ) = 2Vφ(μ/σ)/σ.
- A1's "locked iff |Ω| < εZ" needs a symmetric phase-response curve, Z_max = −Z_min. Otherwise the window's centre, −ε(Z_max + Z_min)/2, moves with ε. My check with an asymmetric curve: locked range [−0.0334, 0.0200] against predicted [−0.0333, 0.0200].
- Reading "fixed point exists" as "locked" needs an invertible map, 1 + εZ′ > 0 (K < 1 for the sine curve).
- **Fix:** reworded, with assumption A0 added in TORUS §4b, N45, N49, REACH and `price_maps.py`. The math itself checks: closed form at μ = 0 to four decimals (2.4477, 1.1774, 0.3203); largest jumps 0.03, 0.04 and 0.09 at μ = 0, 0.5 and 0.9, against 0.98 and 2.04 at 1.1 and 1.5; and a fourth-root cusp at μ = σ, with a*/(c₀ − c)^{1/4} = 2.256, 2.239 and 2.234 as c₀ − c falls from 10⁻³ to 10⁻⁵.

**S3. N47: the reach exponent was stated without scope** (`WORMHOLES.md:98`, `:119`; CLAIM_MAP `:397`).
- L ∝ m^{1−β/(α−1)} assumes the shortcut acts as a uniform medium of speed m·c, which is the finite tube map of §4b. It also assumes D* and α are unchanged.
- With open throats the reach is unbounded whatever β is. With stations one hop away (§4), reach is a coverage fraction.
- **Fix:** scope added. Everything else in N47 re-derived and agrees:
  - mean age T(2 − s)/(2s): own simulation 0.6097, 1.5079 and 3.5267 against 0.6111, 1.5000 and 3.5000;
  - both thresholds: brentq roots of the brute-force cost against 1/g − 1/N and s(1 − 1/N), 0 disagreements in 40 cases;
  - the outage term: renewal argument re-derived; my own simulation within 0.4% for exponential, gamma and constant laws, and 2.0% low for a lognormal with CV² = 3.2 (heavy-tail sampling, matching PR #93's 1.8%);
  - ℓ_crit·√q constant (0.3536 at q = 0.25, 1 and 16; brute force equals the closed form);
  - reach exponents for α = 2, 3 and β = 0.5 to 2.

**S4. Ferrer i Cancho & Solé 2003 phase boundaries misassigned** (`COSMIC_WEB.md:115`).
- The paper (arXiv text) puts the exponential and truncated scale-free networks both below λ*₁ ≈ 0.25 (Fig. 3: λ = 0.01 and 0.08), the star phase at λ*₁ < λ < λ*₂ ≈ 0.80, and dense to clique-like networks above λ*₃ ≈ 0.95.
- The row implied the star phase came after 0.80.
- **Fix:** corrected.

## NITS (applied where cheap)

- `WORMHOLES.md:90` says newest-first, while the script header (`wormhole_reliability.py:10`) says FIFO. Only the newest update matters for the age, so the mean is the same either way. The telling price is charged every cycle. Both now stated.
- `REACH.md:103`: Bull, Koelle & Antia 2025 is a perspective with a model ("we argue that"), not an empirical test; now labelled. The sign call (faster waning goes with more antigenic evolution) is fair.
- `REACH.md:104`: the Muñoz-Alía et al. 2021 primary abstract is open on Europe PMC. It agrees with the Greaney preview ("severely constrained by the existence of numerous co-dominant H glycoprotein antigenic sites"). Cited; reference added.
- `COSMIC_WEB.md:116`: the Gastner & Newman 2006 arXiv full text is open. It shows the MST (shortest total length) and the star (route factor 1) as the extremes, with real networks close to optimal on both. The row is reworded and the read level updated.
- Not fixed (left as is): the "formula" column of `wormhole_reliability.out` part B uses the realised A, so it reads 0.8318, not 0.8333. Harmless.

## Item-by-item record

**1. N47 (wormhole reliability):** correct in-model; scope fix S3. Labels PROVED (in-model) and CONDITIONAL are fair.

**2. N49 (price-to-K map):** correct, with A0 added (S2). K = 2π·Z·ε is exact for the sine curve. A1 to A3 are stated; with A0 they are sufficient for the stated results. Label PROVED (in-model), CONDITIONAL on A0 to A3, is fair.

**3. SDSS data check.**
- *Reproduced.* I re-pulled the public SkyServer DR17 data (no sign-in; 35,697 rows) and re-ran `web_hubs_sdss.py`. The output matched the saved `.out` exactly: N = 16,535; var/mean 6.67; top-1% share 0.0849 at ⟨k⟩ = 4; Poisson 1.14 and 0.0268; kNN k = 20 var/mean 2.50 against 2.52 ± 0.06.
- *Better null.* Lognormal fixes failed (S1b). So I built a halo-model-style null: points trace a lognormal field smoothed at 1.5 Mpc/h (Gaussian variance about 1.5), plus Gaussian groups (0.3 to 1.2 Mpc/h) fitted to the small-scale excess. I ran three occupancies (m = 15, 30, 60; group fraction F = 0.68, 0.34, 0.17), with 30 fresh mocks each.
  - ξ_s is matched within 11% at 0.6 to 3.3 Mpc/h, the scales that set degree, but is 9 to 26% high at 5 to 11 Mpc/h. So every member **fails** the §8 ξ gate.
  - The degree-scatter gate passes (15 to 21%).
  - S1 data against null: at ⟨k⟩ = 4, 0.0849 against 0.069 ± 0.015 (z = +1.1), 0.092 ± 0.014 (z = −0.5) and 0.157 ± 0.044 (z = −1.6); at ⟨k⟩ = 10, 0.0774 against 0.060 ± 0.018 (z = +1.0), 0.065 ± 0.016 (z = +0.8) and 0.082 ± 0.017 (z = −0.3).
  - Under §8's rule: "within" for all members, so **the hub statistic does not exceed this null**. Because the null fails its gate, that is a DATA CHECK, not a test: N48 stays OPEN.
- *N48 prereg:* not sound as written; revised (S1).
- *N48 label OPEN:* fair.

**4. Prior art (spot checks, texts opened this session):**
- *Yang & Yu 2023:* the arXiv text confirms tree graphs linking each subhalo to its least massive host, in-degree P ∝ N^−2, in FIRE2 (hydrodynamic), TNG50-1-Dark and Bolshoi (dark-matter-only). The journal reference is Phys Rev Research 5:043187. Fair.
- *Bull, Koelle & Antia 2025 (PMC12121555):* "the rapid rate of waning immunity in the respiratory tract is a key driver of antigenic evolution". Fair (nit above).
- *Greaney 2021 and Muñoz-Alía 2021:* fair.
- *Ferrer i Cancho & Solé 2003:* E(λ) = λd + (1 − λ)ρ confirmed; phases fixed (S4).
- *Gastner & Newman 2006:* fair (nit).
- *Benner 2010 (PMC3005285):* the sentence "entities can be alive (a cell, virus, or a single rabbit) without themselves individually exemplifying life" is verbatim. Fair.
- *Bull, Sanjuán & Wilke 2007 (PMC1865999):* "a sufficient condition for lethal mutagenesis in the absence of an error catastrophe: (3)", with the threshold also including "an ecological component". The equation is an image in the HTML; the surrounding text fits R_max·e^{−U_d} < 1. Fair.
- *K-V3 withdrawal and N38 → PRIOR ART:* fair. Each ingredient is published, two with the opposite sign on the cross-reactive reading, and the wording withdrawal is not a refutation.
- *N40 OPEN:* fair.
- *N38 label:* fair.

## Still open

- The N48 matched-null test needs N-body halo mocks (TNG or similar; the TNG downloads need an account, which I did not create) and a second survey.
- W in the price-to-λ map (N50) is still unmeasured.
- A real system with a measured phase-response curve for N45 and N49 is still needed.
