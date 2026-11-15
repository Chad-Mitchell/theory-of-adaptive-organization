# SPECTRUM-MAP-FIXES — SPECTRUM_MAP_REFEREE §8 items 2–8 applied as dated errata (pick 26)

Executor queue-pick26 (Grok Bot, for Chad via Ace, t1914), Sunday 15 Nov 2026, about 5:28–5:45 PM ET (America/New_York).
Branch `q-pick26`. Ledger 120 (unaided order), 121 (rule_rank), 122 (claim), 123 (outcome). Private; nothing sent or posted.
Authored none of SPECTRUM_MAP or its referee report. Item 1 was applied in the THEORY v1.4 PR.

## What was done
Dated, bracketed errata were inserted into `reviews/night2/SPECTRUM_MAP/README.md` next to each sentence they correct
(original text kept). Locked files (`PREREG_D3S.md`, `checks/d3s_shuffle.py/.out/.json`, all committed `.out`) are untouched.
THEORY.md v1.4 §2.2 already carries items 2–7. One numeric there is wrong (see item 5); that edit is a separate PR.

| §8 item | Applied | Own check (`SPECTRUM_MAP_FIXES_checks/`) |
|---|---|---|
| 2 Thm 2 citation | eq. (2.8) for pure fBm; Remark 2.6(a)/eq. (2.9) spectral form is stable case β < 0 only; Kleptsyna et al. 2020 added | **Read this session:** Afterman et al. arXiv 1911.10062 (Remark 2.6 text, as the referee said); Kleptsyna et al. arXiv 2205.09516 Remark 2.2 (minimax-rate remark) |
| 3 Cor 2′ | "under linear precision pricing" (two places) | algebra only (referee R2 re-optimised numerically) |
| 4 Prop 3 | "far steeper ⇒ not kernels" dropped; survival exponent α/2; no kernel measured | **A:** ARFIMA AR(∞) weights, d = α/2: survival slope −0.7501, −1.2503, −1.5004, −1.7505 (theory −α/2) |
| 5 Prop 4 | Jiang et al. 2017 and Benna & Fusi 2016 credited; knife-edge replaced by continuous rule; rate fit ~10–25% not 5% | **B1, B2, B3** and c3 diagnosis below. **Correction to the referee's constant.** Read: Jiang et al. arXiv 1511.03453 abstract (N_exp formula); Benna & Fusi arXiv 1507.07580 (beaker-chain passage, Fig. 1; preprint-to-journal mapping not verified) |
| 6 Prop 5 | restated as τ_m ∝ (N/q)^{1/α} (KNOWN); τ_E form only at fixed variance; Mora & Nemenman credited (on the referee's reading, not re-read) | **C** (`fixes_check2`): fixed variance slopes 0.333, 0.500, 0.597, 0.662 (theory 0.333, 0.5, 0.6, 0.667); fixed q 0.000 (α 1.5–2.5), −0.167 at α = 3.5 (theory −1/6) |
| 7 Prop 6 / D3 | "explained by renewal" withdrawn; mis-derived sign; D3S non-discriminating | **D:** own pure-Cox simulator (24 repos × 8 files, 4096 days): Spearman(β, a_need) +0.71 (p 1×10⁻⁴; referee +0.975 with different estimators); Δβ at β 0.15–0.31: 0.005–0.097, median Δβ/β 0.24 (referee 0.22–0.29) |
| 8 d3s reproducibility | `SPECTRUM_MAP/checks/d3s_shuffle_repro.py` (new file): sorted file order, per-repo seed 20261115 + crc32(name) | per-repo rows identical across repo order and PYTHONHASHSEED (1 vs 777, forward vs reversed); median Δβ 0.024, **S1 PASS reproduces**; S2 (exploratory) 0.31 vs locked 0.40 (RNG stream change); pandoc β_orig 0.258 vs 0.253 committed, still unexplained (as the referee found) |

## Item 5 in detail: the referee's 0.14 is too large
The referee measured one-store excess ≈ 0.14(α−2)² with `c3_layers.py` unchanged. That script fits K = 1 on a 5-point rate grid
(`l1 ∈ logspace(−1.5, −0.3, 5)`) and polishes only K ≥ 2. Near α = 2 the optimum rate (≈ 0.22–0.26) falls between grid points.
- **B2 (own discrete code, same model: 4 free taps + one weighted EWMA, finite span, error spectrum integrated directly):**
  c = excess/(α−2)² = 0.033, 0.039, 0.043, 0.049, 0.052, 0.060 at span 10² and 0.066–0.109 at 10⁴ (α = 1.8–2.2); excess at α = 2 is 3×10⁻⁹.
  Pass 1 (`fixes_check.py` B2) was numerically wrong (negative excess from c − w·b cancellation); pass 2 replaces it.
- **Diagnosis** (`c3_onestore_diag.py`, runs c3 unchanged plus a 1-D polish): polished c3 values match B2 to 3 digits
  (3.94×10⁻⁴ vs 3.93×10⁻⁴ at α 1.9, span 10²); the unpolished grid gives 1.45×10⁻³ (the referee's number). Overstatement 2.5–4×.
- **B1 (scale-free continuous world, one unit-gain EWMA, closed form checked by quadrature):** c = 0.16–0.21, → 0.18 at α → 2.
- The (α−2)² law holds in all three. The constant depends on model and span, so "0.14" should not be quoted as a number.
- **What survives:** "two stores at |α−2| = 0.05 once ψ ≈ 10⁴": the two-store threshold is ψ ≈ 9.8×10³ / 6.1×10³ / 5.5×10³
  (α 1.95, span 10², 10³, 10⁴) and 8.5×10³ / 5.4×10³ / 4.9×10³ (α 2.05) (`c3_twostore_diag`). Committed K\* tables at ψ = 10⁴ are unchanged;
  at span 10 one cell each moves by one store (α 1.5 ψ 10³: 2→1; α 2.5 ψ 10²: 2→1) (`c3_kstar_diag`).
- **B3:** log-decrements of committed ε_K at L = 4, α = 1.5: 2.18, 1.87, 1.75, 1.65, 1.44 vs 1.75; the first step is inflated by the
  unpolished K = 1 fit, the last nears the quadrature floor. "Within ~10–25%" stands.

**THEORY.md consequence.** THEORY v1.4.6 N4 (§1) and the §2.2 store row say "one store iff ψ·0.14(α−2)² ≲ 1". Proposed replacement:
"one store iff ψ·c(α−2)² ≲ 1, c ≈ 0.03–0.2 depending on span and store model (in-model)". This is a core-table numeric, so it is
author-only: separate PR `q-pick26-theory` (PR #51), **DO NOT MERGE without separate reviewer PASS** (Chad t1916). New item STORE-COEF-REVIEW.
CLAIM_MAP K12 gets a dated v2.24 note (no status change). SPECTRUM-BRIDGE-SIM's lock note now says not to lock 0.14.

## Labels and limits
No outcomes; no prereg; MV10 n/a. No CLAIM_MAP status change. Vigilance OPEN. Results are in-model (filters and store models),
not field results. D is an independent re-implementation with my own β and a_need estimators, not MATCH1's `aslib`; it checks
the sign and the Δβ range, not the referee's exact numbers. Mora & Nemenman 2019 and Lowen–Teich were not re-read by me.
