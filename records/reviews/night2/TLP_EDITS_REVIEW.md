# TLP-EDITS-REVIEW — independent review and application of THEORY edits E2′, E4, E5, E6 (THEORY v1.4.3)

Executor queue-pick9 (for Ace; Chad t1914, t1916), Sunday 15 Nov 2026, 12:33 PM to about 12:45 PM ET (America/New_York). Queue pick 9, rule slot (ledger 49 unaided order, 50 rule_rank, 51 pick, 52 outcome). Private repo; nothing posted or sent. **I authored none of the proposed texts** (E2′, E4–E6 are from `reviews/night2/TELEGRAPH_LINEAR_PREMISE/REPORT.md`; corrections from `reviews/night2/TELEGRAPH_REFEREE/REPORT.md` §4). Chad's rule (t1916): be extra careful, causal first principles, no headline or core rewrite. §0, §1 and the §2.1 setting were **not** edited.

## Pass 1: review and application (sentence by sentence against the sources)

| THEORY location | Edit | Source | Check |
|---|---|---|---|
| Header | v1.4.2 → v1.4.3; CLAIM_MAP pointer v2.5 → v2.11 (it was stale: the map was at v2.10) | — | pointer only |
| §2.2 Regime A, examples | parenthetical: same spectrum need not give the same Bayes optimum | TLP §What this establishes 1; referee V1–V4 | yes |
| §2.2 Regime A, memory-time bullet | "Premise: Gaussian world, or the best linear tracker" | E2′ | yes |
| §2.2 Regime A, new premise bullet | E2′ text with the referee's changes: t_A = (N/2μ²)[ln(2μ²/λN) − γ − 1] + o(1) (V5); exact MSE μ²·2K₀/(K₀+K₁) ≈ 2λN[ln(2μ²/λN) − γ] (V7); elasticities 1/ℓ, 1 − 1/ℓ, −2 + 2/ℓ, ≈ 0.17, 0.83, −1.67 at κ = 10⁻³ (V12); error elasticity 0.85–0.89 at κ = 10⁻³…10⁻⁴ (V7; recomputed here 0.852, 0.879, 0.892); q alone does not set them (E2′(d)); credits per referee §3 with read/not-read labels; Bessel form and γ + 1 "derived in this repository, likely classical", γ + 1 not rigorously proved (referee §2, §6); reset reads unaffected (V10); only the symmetric two-state case (referee §6) | E2′, referee §4 E2′(a)–(d) | yes, numbers re-derived (below) |
| §2.2 Regime B table, premises column | "Gaussian world, or the best linear tracker" on error, precision effort, memory time, kernel rows; read-rate row: hold-last-value and optimal-linear errors depend only on second moments; a Bayes predictor can differ, not for two-state switching at α = 2 | E4 (referee: accept, kernel wording per E5) | yes; see change C1 |
| §2.2 kernel row | own-observations regression kernel = linear; a kernel on the true driver need not be | E5 as corrected (V11) | yes |
| §2.5 rule, premise list | adds "linear vs Bayes optimum for non-Gaussian worlds"; kernel sentence "regressed on its own observations"; driver kernel and jump transients can discriminate, stated as one in-model case (V11, κ = 1/60) with the κ → 0 gap not derived (referee §6) | E5 as corrected | yes |
| §2.5 N12 bullet | homogeneity caveat: holds for linear trackers; Bayes jump-world error μ²·f(λN/μ²) is degree-1 homogeneous under (N, μ²) scaling, not under (N, λ); onset exponent not derived (JUMP-WORLD-ONSET) | E5 part 2; the (N, μ²) vs (N, λ) split is mine, from the closed form (check below); consistent with TLP §5's sketch | yes |
| §2.4 D3 row | one-line pointer to N17 (pure renewal failed on proxy, 27/27 and 5/5; locked, not refereed; Cox/Hawkes/trend not separated) | CLAIM_MAP N17 (v2.10), `tests/D3_OOS/RESULTS.md` | yes, text matches the N17 row |
| §10 | new "Switching (jump) worlds" block: Conti & Mora 2022 with the eq. (20) Itô omission, ln² (eq. 36) and eqs. (41)–(42) caveat; Khasminskii & Zeitouni 1996; Golubev 2000; Chigansky 2005; Wonham 1964; Liptser & Shiryaev; Shiryaev 1963; Baron & Tartakovsky 2006; Tartakovsky & Veeravalli 2005; Tartakovsky & Moustakides 2010 | E6 as corrected; referee §3 | yes; labels below |
| §13 | v1.4.3 changelog entry | — | yes |

**Changes I made to the proposed texts (pass 1).**
- C1. E4's read-rate premise said "exact reads: hold-last-value depends only on the variogram ... for the optimal predictor, also in Markov worlds whose conditional mean is linear in the last read (e.g. two-state switching)". The Regime B row is for α ≠ 2, where a Markov world with linear conditional mean does not live. Rewritten: both hold-last-value and the optimal **linear** predictor depend only on second moments (so the row holds in any world with them); only a nonlinear Bayes predictor can differ; two-state switching (α = 2) is pointed to the Regime A bullet.
- C2. E2′ said reset reads are "unaffected"; the Regime A read-interval bullet is the √ rule for a random walk. Worded as "the optimum is the same as for the mean-reverting world with the same covariance" (referee V10), not "the √ rule holds".
- C3. Kept the jump-world result as a separate premise bullet after "All KNOWN", so that bullet stays true; the new bullet carries its own labels.
- C4. C&M eqs. (41)–(42): THEORY says they "inherit the same omission" and points to referee V13 for the exact forms, instead of quoting the forms (their P_wrong is a soft error, (1 − ⟨x⟩₊)/2, which a reader could confuse with a sign-error probability).
- C5. Did not touch the store-count row (premise "K exponential stores"), §0, §2.1 or §1 N6; see Unresolved.

**Citation checks (this session).** Crossref resolved: Shiryaev 1963, *Theory Probab Appl* 8:22–46, doi 10.1137/1108002; Conti & Mora 2022, *PRE* 106:054404, doi 10.1103/PhysRevE.106.054404, title "Nonequilibrium dynamics of adaptation in sensory systems"; Khasminskii & Zeitouni 1996, *SPA* 63:1–10, doi 10.1016/0304-4149(96)00060-9; Wonham 1964, *SIAM J Control* 2:347–369, doi 10.1137/0302028. arXiv API: math/0508446 is P. Chigansky, "On filtering of Markov chains in strong noise", journal ref *IEEE Trans Inf Theory* 52(9):4267–4272 (2006). Golubev 2000 not resolved by Crossref here (cited as the referee gives it, labelled). I read none of these texts myself; THEORY labels each by what the referee read (Chigansky read; C&M read by the TELEGRAPH author and referee; the rest not read or excerpts only).

**Independent numerics (`TLP_EDITS_REVIEW_checks/check.py` → `check.out`; my code, not the referee's).**
- MSE closed form vs 2κ[ln(2/κ) − γ]: ratio 0.993, 0.998, 0.999 at κ = 10⁻³, 2.5·10⁻⁴, 10⁻⁴; vs 2κ ln(2/κ): 0.918–0.941 (TLP P2c's 0.92–0.96). Elasticity in κ: 0.852, 0.879, 0.892 (TLP 0.854/0.879/0.891).
- ℓ at κ = 10⁻³: 6.024; 1/ℓ = 0.166, 1 − 1/ℓ = 0.834, −2 + 2/ℓ = −1.668.
- γ + 1: direct quadrature of the referee's first-passage integral with the quasi-stationary start gives implied constants 1.569 (κ = 10⁻³) and 1.5771 (κ = 10⁻⁵) vs γ + 1 = 1.5772.
- Homogeneity: scaling N and μ² by 3 multiplies the error by 3.000; scaling N and λ by 3 multiplies it by 5.97.

**Pass 1 verdict:** E2′, E4, E5, E6 apply as the referee corrected them, with C1–C5. No novelty claimed beyond "derived in this repository, likely classical".

## Pass 2: fresh hostile re-read of the full diff (same executor, separate pass after pass 1 was written)

Not a different agent: no second reviewer was available to this executor. I re-read `git diff origin/main` word by word against the two source reports, looking for overclaims, wrong labels, scope creep and contradictions. Found and fixed:
- H1. "Shiryaev 1963; Tartakovsky & Veeravalli 2005; not read in full" understated: neither was read (only search excerpts of later papers). Fixed.
- H2. "derived here" for the Bessel form and γ + 1 omitted that γ + 1 rests on a leading-order argument confirmed by quadrature, not a proof (referee §2, §6). Fixed.
- H3. The kernel sentence said a driver kernel "can" discriminate, generalising one numerical case. Now "in the one in-model case computed ... the gap as κ → 0 is not derived". Fixed.
- H4. t_A was not defined; now "mean time for its estimate to cross zero" (the referee's first-passage definition).
- H5. The N12 caveat's homogeneity split is mine; now labelled with this review's check path.
- H6. C&M marked "[read]" though I did not read it; now "read by the TELEGRAPH authors and referee".
- H7. The changelog said "independently reviewed and second-checked", which overstated pass 2; now says what was done.
- H8. Regime A parenthetical "same spectrum does not mean same optimum" sharpened to "need not give the same Bayes optimum".
- H9. Chigansky's title says "strong noise"; added that the paper treats weak noise as the same limit (referee §3).
Checked and left: the elasticity signs and units; "q = 4λμ²" (TLP §1); "exact reset reads unaffected" (V10); no change to §0, §1, §2.1, §2.3, §3–§9; no locked file, result or proof touched; no "law"; vigilance still OPEN.

**Pass 2 verdict:** CLEAN after H1–H9. Both passes pass; merge.

## Unresolved (queued as HEADLINE-PREMISE-SCOPE unless noted)
- §0 ("classical optimal filtering ... give the design exponents ... memory time ∝ (noise/drift level)^{1/α}"), the status block and §2.1 ("three quantities set the tracking optimum") state the noisy-sensing exponents without the premise "Gaussian world, or the best linear tracker"; §1 N6 and CLAIM_MAP N13 list α, q, N, stakes as the inputs, which are incomplete for a Bayes tracker of a jump world. Fixing that touches the headline, so per Chad t1916 it needs its own independent review (new item HEADLINE-PREMISE-SCOPE).
- Store-count row: under Bayes tracking the "store count" is a sufficient-statistic dimension (JUMP-STORES); the row's premise "K exponential stores" already restricts it to linear architectures, so no edit now.
- Originals of Khasminskii & Zeitouni, Golubev, Wonham, Liptser–Shiryaev, Shiryaev not read (WONHAM-PRIORART-FULLTEXT).
- E1/E3 (Bialek, Callan & Strong credits) are a separate item (PRIORART-CREDIT-EDITS), not applied here.
