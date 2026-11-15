# ONSET-NOISY-READS-REVIEW: separate review of PR #60 (THEORY v1.4.11, CLAIM_MAP v2.29)

Sunday 15 November 2026, about 6:20–6:30 PM ET (America/New_York). QUEUE ONSET-NOISY-READS-REVIEW, pick 30, rule slot (ledger 140 unaided order, 141 rule_rank, 142 claim; outcome on branch q-pick30). Grok Bot executor for Chad Mitchell, via Ace (t1914/t1916). The reviewer authored none of ONSET-NOISY-READS, PR #60, the N12 referee or their code. Private; nothing posted or sent. In-model only (formal layer); no field claim.

**Own code:** `reviews/night2/ONSET_NOISY_READS_REVIEW_checks/` (`rv_f.py`, `rv_onset.py`, `rv_f0M.py`; nothing imported from `ONSET_NOISY_READS_checks/` or `N12_REFEREE_checks/`; run at nice 19). Two independent routes to f_α(z): Gaussian conditioning on M past reads with fBm anchored at 0 (as the author, but own implementation), and a **truncation-free** Kolmogorov–Szegő formula for the error just before a read (differenced reads d_k = y_k + ε_k − ε_{k−1}; S_d = S_y + 4z sin²(λ/2); S_y the aliased fGn spectrum).

## Verdict: **PASS-WITH-FIXES.** PR #60 merged as THEORY v1.4.11 / CLAIM_MAP v2.29 after the fixes below.

Every number in the THEORY clause reproduces with own code:

| Quantity | Author | Reviewer |
|---|---|---|
| Collapse N\*ρ at s = 10 across σ² = 10⁻⁵…10⁻³ (α = 2) | 191.03–191.14 | 191.066, 191.068, 191.080 (X(10) = 191.066) |
| X₀ = α^{α/(α−1)} | 3.375, 4, 4.605 | X(10⁻⁶) = 3.37501, 4.00001, 4.60506 |
| C_α (α = 1.5, 2, 2.5) | 9.247, 19.09, 38.87 | 9.260, 19.092, 38.868 (closed form with own f_α(0)); N\*ρ²/σ² at s = 100 directly: 9.15, 19.09, 38.95 |
| ρ_c/σ² | 2.74, 4.77, 8.44 | 2.744, 4.773 (= 27√2/8), 8.440 |
| z_L at ρ_c | 0.17–0.47 (α 2.75…1.25) | 0.45, 0.41, 0.29 at α = 1.5, 2, 2.5 (THEORY's "about 0.3–0.45" holds) |
| s at local slope −1.5 | 0.41, 0.24, 0.14 | 0.410, 0.245, 0.140 |
| Referee c3 slopes (σ² = 10⁻³, ρ 10⁻²→10^{−2.5}), full equation incl. noisy members | −1.277, −1.401, −1.583 | −1.277, −1.401, −1.583 |
| Local slope at s = 100 | −2.000 ± 0.003 | −2.001, −2.000, −1.998 |

Minor discrepancies (REPORT only, not in THEORY): f_{1.5}(0) converges to 0.59072 (M = 600…3600: 0.590757 → 0.590725), not 0.5910, so C_{1.5} = 9.260 not 9.247 (0.14%; ρ_c rounds the same). The two-asymptote sum X₀ + C_α s is off by 14%, 19%, 21% at s_c (α = 1.5, 2, 2.5), not "13–18%".

## Answers to the five questions

**Q1. Dense-sampling asymptote f_α(z) ~ g_α z^{1−1/α}, g_α = (Γ(α) sin(π(α−1)/2))^{1/α}/sin(π/α): correct for every 1 < α < 3, including 1.25.** Derivation (reviewer's sketch, closes the author's one assumed input). With unit spacing and q = 1, the error just before a read from the infinite past is P₁ = exp((1/2π)∫ ln S_d) − z. Since (1/2π)∫ ln(4 sin²(λ/2)) = 0, P₁ = z(e^J − 1) with J = (1/2π)∫_{−π}^{π} ln(1 + h(λ)/z), h(λ) = C Σ_k |λ + 2πk|^{−α}, C = Γ(α) sin(π(α−1)/2). As z → ∞ the integral is dominated by |λ| ~ z^{−1/α}, where h = C|λ|^{−α}(1 + O(λ^α)); so J = (C/z)^{1/α}/sin(π/α) · (1 + o(1)) (using ∫₀^∞ ln(1 + u^{−α})du = π/sin(π/α)), and P₁ = zJ(1 + O(J)) = g_α z^{1−1/α}(1 + o(1)). Within a read interval the error moves by at most one drift-per-read unit in root-mean-square (Minkowski: |√P(u) − √P₁| ≤ 1), so the time average f_α(z) has the same leading term, with relative correction O(z^{−(α−1)/(2α)}). Numerically (`rv_f.out`), Szegő P₁/(g z^β) = 1.0069, 1.0012, 1.0002, 1.00004, 1.00001 at α = 1.25 for z = 10²…10⁶; 1.00004 at α = 1.5, 1.0005 at α = 2, 1.002 at α = 2.5 and 1.003 at α = 2.75 at z = 10⁶ (slower convergence as α → 3, as the O(J) term predicts). The author's α = 1.25 discrepancy at z ≥ 10³ is M-truncation: conditioning u = 1 error over Szegő = 1.063 at M = 1200, z = 10³. At α = 2 conditioning equals the closed Kalman form P² + P = z, f = P + ½ (to 10⁻⁸). Status: derived at physicist's rigour (dominated-convergence and the O(1) aliasing remainder not written out), not merely assumed.

**Q2. ρ_c as the asymptote crossing vs the −1.5 point: the crossing is the right definition.** It is closed form and both points sit together: the local slope at s_c is −1.464, −1.448, −1.443 (α = 1.5, 2, 2.5), and s(−1.5)/s_c = 1.12, 1.17, 1.18. THEORY should keep the crossing and may quote the slope there (added: "about −1.45 at ρ_c").

**Q3. Uniform-convergence step: monotonicity is enough, but the argument needs two facts made explicit.** (a) A lower bound on f: f(z) ≥ f(0) > 0 (true because extra read noise cannot lower the MMSE; this is what monotonicity buys). Then for read intervals where z is not large, z ≤ Z₀ means T ≥ (s/Z₀)^{1/(α−1)}, so the drift term x T^{α−1} f ≥ x s f(0)/Z₀ ~ s², far above Ψ_∞ ~ s; the minimiser lies in the large-z region, where f = g z^β(1 + o(1)) gives Ψ = Ψ_∞(1 + o(1)) uniformly on x ∈ [s/K, Ks]. (b) Uniqueness of the root: Ψ(·, s) is a minimum of functions linear in x, hence concave, with Ψ(0, s) = 0, so xD − Ψ has at most one positive root; with the limiting root C_α s this gives X(s)/s → C_α. This proves N\*ρ²/σ² → C_α (so the average slope over any fixed number of decades tends to −2). The pointwise local slope → −2 additionally needs z f′(z)/f(z) → 1 − 1/α; it follows from the Szegő form by differentiating J under the integral (not written out) and holds numerically (−2.000 at s = 100). Fix F2.

**Q4. Is the curvature classification over-stated for finite windows? Slightly; qualified.** In-model, over one decade of ρ centred on ρ_c the local slope runs from −1.19/−1.17/−1.17 to −1.80/−1.82/−1.83 (α = 1.5, 2, 2.5); over half a decade from about −1.29 to −1.65. That curvature is large enough to see with a well-measured onset, but only on windows that straddle ρ_c; on a window well above or below ρ_c noisy reset reads look straight at −1 or −2, the same as exact reset reads or θ = 1 priced precision. The clause already tells a test to measure the level's read noise relative to its drift per read or to check the collapse; fix F3 adds the window condition.

**Q5. Numbering vs PR #58.** PR #58 merged first (main 0c8f390, THEORY v1.4.10, CLAIM_MAP v2.28, ledger 139), so v1.4.11 / v2.29 are now sequential: no renumbering. Merge of origin/main into the PR branch resolved two header/changelog conflicts (version list now "v1.4.9, v1.4.10 and v1.4.11"; changelog keeps both entries, newest first).

## Fixes applied (reviewer, in PR #60 before merge)

- **F1** Constants scoped: they take the members' own read noise as negligible (own check: member marginal cost D moves by < 1% for σ² ≤ 0.1 in member units: 1.002, 1.004, 1.009 at α = 1.5, 2, 2.5); otherwise use the members' measured D (as REPORT §4.4).
- **F2** "Assumed input … not refereed" replaced: the asymptote is derived (Kolmogorov–Szegő sketch above); "tends to −2" stated as proved in the ratio sense, local-slope limit numerical.
- **F3** Curvature test limited to ρ windows that straddle ρ_c, with the in-model slopes across one decade.
- **F4** Changelog and CLAIM_MAP v2.29 note: review recorded; N12 row evidence says refereed.

No headline, kill condition, locked prediction, result or CLAIM_MAP status changes; N12 stays MATH-CORRECTED. No locked prereg cites ρ_c. Vigilance stays OPEN. Prior art: none read for this review; none credited. The Yovits–Jackson and Kolmogorov–Szegő formulas are used as standard results, not re-read here.
