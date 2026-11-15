# NOISE-PROXY-REFEREE: independent hostile referee of SPF-NOISE-PROXY (and an audit of dispersion-based N in the repo)

**Verdict: PASS-WITH-FIXES on proxy "SPF within-forecaster nowcast dispersion, latest-vintage environment".**
Referee: executor queue-pick22 (for Ace, Chad t1914), Sunday 15 Nov 2026, about 5:20 PM ET (America/New_York). Queue pick 22,
rule slot (ledger 104 unaided order, 105 rule_rank, 106 claim, outcome 111). I authored none of `tests/SPF_NOISE_PROXY/`,
`tests/LFK_SPF/` or `tests/SPF_RIGIDITY_OOS/`. Every check reported as independent uses my own code in
`NOISE_PROXY_REFEREE_checks/` (time-domain Matérn autocovariance via Bessel K_ν, Toeplitz normal equations; it imports nothing
from `tests/`, and reads only the micro csv files and the environment fits/var_x recorded in `results/analysis.json`, which I take
as inputs and did not re-fit). Run at nice 19. **No CLAIM_MAP status changes; N13 stays OPEN; vigilance stays OPEN; THEORY.md not
edited.** Prior art: none newly read; nothing is credited here. (SPF survey timing, i.e. that forecasters see part of the current
quarter by the deadline, is used below only as a modelling alternative, not as a sourced fact.)

## 1. Results of the independent checks
| # | Check (own code) | Result |
|---|---|---|
| R0 | In-model formulas: β^G (consensus CG, h = 3, finite n) and D(K) = K(1−1/n)Σa² re-derived in the time domain (Bessel autocovariance, 600-lag Toeplitz) instead of the authors' FFT/cepstral Wiener filter | β^G at K̂_L0w reproduced to 3 decimals for all 7 variables (e.g. UNEMP 0.325, HOUSING 0.352, TBILL 0.095, BOND 0.555, TBOND 0.087, RSLGOV 0.151, INDPROD 0.360) |
| R1 | K̂_L0w re-estimated from `data/micro_*.csv` with my own pandas pipeline and my own level curve | identical to the pipeline for all 7 (e.g. 0.0077, 0.0303, 0.0039, 0.0108, 0.0016, 0.172, 0.286) |
| R2 | **Branch identification** (the level curve D(K) is not monotone; the authors take the lower branch by rule). Discriminator: the consensus nowcast's sample variance / var_x, predicted at each branch root (expected sample variance over the T surveys) vs observed | Lower branch clearly favoured for UNEMP (obs 0.91; lower 0.89, upper 0.0002), HOUSING (0.92; 0.87, 0.001), TBILL (0.89; 0.75, 0.0001), BOND (0.68; 0.48, 0.0001), TBOND (0.22; 0.45, 0.00002), INDPROD (0.46; 0.63, 0.05). **RSLGOV is not identified and leans upper**: obs 0.125 vs lower 0.67, upper 0.038 (log distance 1.7 vs 1.2); its level is 0.55 of the curve's peak. On the upper root K ≈ 10, β^G ≈ 7.0 (β̂ 0.60) |
| R3 | **Validated range.** The dry run drew K from [0.01, 1]; UNEMP (0.0077), TBILL (0.0039) and TBOND (0.0016) lie below it. Own Monte Carlo of the L0w estimator (pure noise, SPF-like spells, 30 panels per cell, environment held at the recorded fit) at K = 0.001–0.03 | median ln(K̂/K) −0.06 to −0.10 at K ≤ 0.003, −0.12 to −0.21 at 0.03 (UNEMP, TBILL, TBOND, HOUSING). The estimator extrapolates fine; the environment-refit part of the dry run was not extended below 0.01 (not done here) |
| R4 | **Public-signal confound.** Alternative world: white private noise K plus a common public signal z = x + u (var K_c), no individual bias. Grid K ∈ [0.001, 1] × K_c ∈ [0.001, 10]; each world's h = 0 and h = 3 dispersion inverted exactly as SPF-NOISE-PROXY does (single-signal lower branch) | A public signal gives **G ≤ 0** for UNEMP, HOUSING, TBILL (down to −1.2) and G ≤ +0.47 for RSLGOV, against observed G = +1.26, +2.11, +2.50, +2.97. It also makes the true consensus β **smaller** than β^G(K̂_0) (ratio 0.17–1.0) for UNEMP, HOUSING, TBILL, at most 1.55 for RSLGOV, against the post hoc β̂/β^G of 2.5–6. So this alternative explains neither the T1 rejections nor S-1; if present it would make S-1 an under-statement |
| R5 | Reporting granularity (rounding variance Δ²/12 vs measured D_within) | UNEMP ~90% of nowcasts on a 0.1 grid: rounding ≈ 5% of D (≈ −0.05 in ln K); TBILL/BOND/TBOND mostly 0.01–0.1 grid: ≤ 5%; RSLGOV/INDPROD derived growth rates: none. Negligible |
| R6 | G-test numbers recomputed from `analysis.json` | (G − null mean)/null sd = 2.36 (UNEMP), 5.11, 10.59, 6.77, 9.69, 4.13 (RSLGOV), 1.13 (INDPROD). **Erratum:** RESULTS says "≥ 3 null SDs in 6 of 7"; it is **5 of 7** (UNEMP 2.4). UNEMP raw p 0.010 (2/201); Holm 0.035 for all six (floor of NSIM 200); the T1 verdicts stand |

## 2. Referee findings on the items listed in QUEUE
1. **Finite-sample variance bias of D/vf** (`common.moments_T`): the Fejér identity E[sample var] = mean(S(1−F_T)) is the standard
   one and is consistent with my time-domain expected sample variance (used in R2). The P0/P0T gap (3.8× BOND, 4.5× TBOND) is
   correctly attributed. **Holds.**
2. **Level-normalised lower-branch inversion:** sound where the level is far below the peak (5 variables at 0.8–10% of the peak),
   and the consensus-variance check (R2) confirms the lower branch there and for INDPROD. **Fix F1:** RSLGOV's K̂_L0w and β^G are
   not identified (R2); it must leave S-1's list. S-1 ("2.5–6× on UNEMP, HOUSING, TBILL, RSLGOV") becomes **2.5–6× on UNEMP,
   HOUSING, TBILL; RSLGOV branch-ambiguous** (post hoc either way).
3. **L0w selection rule:** locked before real data, applied as stated; admissibility margins are thin (arm a 0.33 vs threshold
   0.35; L0 was admissible too and gives the same answers within its CI). Three of the seven K̂ lie below the validated range;
   R3 shows the estimator itself still recovers K there. **Fix F2 (wording):** RESULTS should say the instrument was validated on
   K ∈ [0.01, 1] and extrapolated (estimator checked to K = 0.001 by this referee, environment refit not).
4. **Parametric-bootstrap G test:** calibrated under the right null (single white private signal, environment re-fitted in every
   simulation); size 0/30 in the dry run means conservative, so rejections are safe. The test rejects the *whole* single-signal
   white-noise model at h = 3 vs h = 0; it does not identify the cause. R4 rules out one named alternative (a common public
   signal with history). Long-horizon individual heterogeneity (the authors' reading, and Patton & Timmermann 2010, which the
   prereg says it read in abstract) remains the leading candidate but is not shown here. **Fix F3:** the erratum in R6.
5. **Environment-variance uncertainty for slow yields:** K̂ scales ~1/var_x on the lower branch, so var_x error passes through
   one-for-one. The CI already cycles 100 parametric environment draws (code read: `analysis.py` lines 66–77). The consensus-
   variance mismatch for TBOND (obs 0.22 vs 0.45 predicted on the lower branch) suggests var_x for TBOND is off by up to ~2×;
   TBOND's CI [≤ 0.0001, 0.0089] is already wide. No change to any verdict; noted.

## 3. Audit of other dispersion-based N in the repo
| Where | Use of dispersion | Status after this referee |
|---|---|---|
| `tests/LFK_SPF/` (P0: h = 3 dispersion / sample var of consensus) | N for N11/N13 probe | already superseded by SPF-NOISE-PROXY (biased + premise failed); its RESULTS points there. No action |
| `tests/SPF_RIGIDITY_OOS/prelock.py` (L0w on 9 unseen variables) | planned β^G for the power gate | gate already NOT MET, so no outcome depends on it. RFEDGOV correctly flagged above the noise max. **Inherited risks for any rerun:** PGDP K CI [0.0007, 4.25] and CPI [0.0008, 0.21] reach far below the validated range; no branch check was run there |
| `measurement/estimators/aqn.py` ("overdispersion"), `tests/LEARNSIM/run_levelclass.py` (dispersion of efforts), `reviews/night2/REFEREE/self_ref.py` (Pearson dispersion), FRAMEWORK §3.10 (dispersion of designs) | not N (count overdispersion; selection resolution ε) | out of scope; no action |
No THEORY.md or CLAIM_MAP row uses a dispersion-based N (grep of THEORY.md for SPF/LFK-ALPHA/dispersion: none).

## 4. On the proposed edits in SPF-NOISE-PROXY RESULTS (for SPF-NOTE-EDITS; not applied here)
- **Edit 1 (THEORY §2.4/§8c LFK-ALPHA-SPF line):** THEORY v1.4.6 has no LFK-ALPHA-SPF line and no S-a statement, so there is
  nothing to correct. **Recommend: drop**, or, if Ace wants the post hoc pattern in THEORY at all, route it as an author PR marked
  DO NOT MERGE without separate reviewer PASS, with F1's three-variable wording and "post hoc".
- **Edit 2 (FRAMEWORK §3, measuring N):** **endorse with two additions**: (a) the level-normalised inversion needs a branch check
  (consensus nowcast variance against both roots; R2) and a stated validated K range; (b) the horizon-overidentification check is
  a necessary premise check, not a diagnosis of the cause. FRAMEWORK has no "measuring N" subsection; §3.4 (sensing) is the
  natural home.

## 5. Consequences
- No CLAIM_MAP status change (measurement-validity item). S-1 stays post hoc and is narrowed to three variables; R4 removes one
  alternative explanation (public signal), which makes S-1 slightly more credible as a pattern to test, not more evidential.
- SPF-RIGIDITY-LIVINGSTON's instrument step should include the R2 branch check and a validated K range that covers the estimates.
- Surprise read (QUEUE rule 4): **weak** (RSLGOV's branch; the public-signal alternative pushes the other way). New item: none.

## Files
`NOISE_PROXY_REFEREE_checks/`: `ref_model.py` (own model), `reproduce.py` (R0–R2), `mc_range.py` (R3), `confound.py` (R4);
outputs in `results/`. Run: `nice -n 19 python3 reproduce.py; nice -n 19 python3 mc_range.py; nice -n 19 python3 confound.py UNEMP` (etc.).
