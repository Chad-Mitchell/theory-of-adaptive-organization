# REGIME-C-GAUSSIAN-PREMISE: independent review of PR #42 (THEORY v1.4.6)

**Verdict: PASS-WITH-FIXES.** Reviewer: independent reviewer executor (for Ace, Chad t1914/t1916), 15 Nov 2026, about 4:47 PM ET
(America/New_York). Ledger outcome 99 (96–98 are held by the unmerged q-pick20). I wrote none of `REGIME_C_PREMISE.md`, its checks, `theory/INTERNAL_MODEL.md`,
`HEADLINE_PREMISE_SCOPE.md` (P9) or any Regime C text. Own derivation and own code (`REGIME_C_PREMISE_REVIEW_checks/`, nice 19);
the author's scripts were not run or reused. This is a scope narrowing with a derived widening of the stated *proof* scope for
the size exponent; no claim is widened beyond a proof, no CLAIM_MAP row or status moves, no locked prereg is affected (no file in
`tests/` mentions Regime C or Q^{1/β}), vigilance stays OPEN.

## 1. What was read
The PR in full (THEORY §0, §2.2 Regime C, §13; CLAIM_MAP v2.18 note; ledger 87–90; items), `REGIME_C_PREMISE.md`, THEORY v1.4.5
§0/§2.2/N6, `theory/INTERNAL_MODEL.md` §4–5 (the share formula share(Q) = κ(F + c(Q/κ)^{1/β})/Q).

Source: Polyanskiy & Wu, *Information Theory: From Coding to Learning*, author PDF of 16 Aug 2024 from
people.lids.mit.edu/yp/homepage/data/itbook-export.pdf, fetched by me 15 Nov 2026 about 4:37 PM ET; sha256
c76c5cd8…db83de3 (identical to the author's hash). Checked in the text: **Theorem 26.2** (Gaussian R(D) = ½ log⁺ σ²/D, scalar
and vector), **Theorem 26.3** (zero-mean, variance σ², MSE: ½ log⁺ σ²/D − D(P_S‖N(0,σ²)) ≤ R(D) ≤ ½ log⁺ σ²/D; scalar),
**Remark 26.3** (SLB asymptotically tight as D → 0 "under appropriate conditions"), **Exercise V.21(b)** (reverse water-filling
for a Gaussian vector with eigenvalues σ_i²). All four citations are accurate as used. Nothing else is credited.

## 2. Cutoff D3, re-derived in both directions
Per mode, unit-variance shape Z, slope u = (w/κ)λ_i; zero rate (X̂ ≡ 0) costs u. Since R_Z is convex and decreasing to 0 at
D_max = 1, zero rate is optimal at slope u iff u ≤ |R_Z′(1⁻)|, so the cutoff is the D_max slope.
- **(⇐)** Donsker–Varadhan per output value y with f(z) = −u(z−y)² + uz²: I + uE(Z−X̂)² ≥ u·EZ² − E log c(X̂),
  c(y) = e^{−uy²}M_Z(2uy). If c ≤ 1 everywhere the right side is ≥ u, the zero-rate cost. Correct.
- **(⇒)** For any output law Q, the Gibbs channel W_Q(y|z) ∝ Q(y)e^{−u(z−y)²} gives I + uEd ≤ E D(W_Q‖Q) + uEd =
  −E log ∫e^{−u(Z−y)²}dQ(y) (since I = min_Q′ E D(W‖Q′)). With Q = (1−ε)δ₀ + εδ_{y₀}: ≤ u − E log(1 + ε(V−1)),
  V = e^{uZ² − u(Z−y₀)²}, E V = c(y₀). Correct. **One gap, closed here:** the ε-derivative needs an interchange of limit and
  expectation, and c(y₀) may be +∞ (e.g. Student t, whose MGF is infinite off 0). ε⁻¹log(1 + ε(V−1)) increases to V − 1 as
  ε ↓ 0 and is bounded below by ε⁻¹log(1−ε) ≥ −2 for ε ≤ ½, so monotone convergence gives the limit E(V−1) = c(y₀) − 1 ∈ (0, ∞];
  zero rate is beaten in either case. The proof is complete with this line.
- c(y) ≤ 1 ∀y ⇔ M_Z(t) ≤ e^{t²/(4u)} ∀t (t = 2uy) ⇔ 1/(2u) ≥ v* ⇔ u ≤ **u* = 1/(2v*)**. Correct; v* ≥ 1 from the second-order
  expansion, so u* ≤ ½ with equality iff Z is strictly sub-Gaussian; u* = 0 iff Z is not sub-Gaussian.
- **Prior art (author Q1):** the two directions are the standard optimality (Kuhn–Tucker / Gibbs-channel) conditions of the
  rate-distortion Lagrangian applied at the one-point output law. I believe this characterization is classical (Gallager's and
  Csiszár's treatments), but I did not read those texts this session, so nothing is credited; the specific identity
  "MSE slope at D_max = 1/(2·optimal sub-Gaussian proxy)" is not found in what I read. REGIME-C-PRIORART-USTAR stays queued,
  note extended with these pointers. The PR text does not claim novelty, which is right.

**Own numerics (`rev_rd.py`; Blahut–Arimoto with an achievable point and a weak-duality lower bound).** v* by direct sup of
2 ln M(t)/t²; exact KKT test max_y c(y) at 0.98u* and 1.02u*; BA "gain" = u − L at 0.9u*, 1.1u*, 1.3u* (upper bound from
duality; achieved value from the BA point). Shapes include one the author did not use (asymmetric three-point {−1, 0, 3},
probabilities 0.3/0.6/0.1).

| shape | v* | u* = 1/(2v*) | max c at 0.98u* / 1.02u* | gain UB at 0.9u* | gain achieved at 1.1u* |
|---|---|---|---|---|---|
| Gaussian (grid) | 1.0000 | 0.5000 | 1.000 / 1.262 | 7e-7 | 0.00234 |
| uniform | 1.0000 | 0.5000 | 1.000 / 1.0005 | 3e-7 | 0.00366 |
| two-point P = 0.2 | 1.3525 | 0.3697 | 1.000 / 1.018 | 1e-14 | 0.00518 |
| three-point (new) | 1.7035 | 0.2935 | 1.000 / 1.034 | <0 (≈0) | 0.00354 |
| Laplace, truncated at 20 raw (≈14.1 sd) | 4.868 | 0.1027 | 1.000 / 1.455 | 1e-9 | not resolved (see below) |

Zero rate is optimal below u* (gain upper bound ≈ 0) and beaten above it (positive achieved gain) for every shape BA resolves;
the two-point value matches the author's 0.3697 and the closed form (1−2p)/(2 ln((1−p)/p))/(p(1−p)) = 1.3525 for a two-point law (my own arithmetic; source not cited).
Truncated Laplace: the exact KKT test crosses at u* (1.455 at 1.02u*), but the gain above u* comes from a rare edge event and is
below BA's 1e-4 convergence gap, so BA does not resolve it; the KKT test is the decisive check there. My u* = 0.103 at 14.1 sd
agrees with the author's u* ∝ 1/L (0.0722 at 20 sd × 20/14.1 = 0.102).

## 3. Exponent claims (D4) and the β < 1 consequence
Re-derived. (a) Head: G(u) ≤ L_Z(u) ≤ L_Gauss(u) = ½ ln(2u) + ½ (u ≥ ½) by Theorem 26.3's upper bound; integrable at x → 0.
(b) Tail: convexity gives R(d) ≤ |R′(d)|(1−d) ≤ u at the optimum, so G(u) ≤ u; ∫^∞ x^{−β}dx < ∞ iff β > 1. A sub-Gaussian shape
has G ≡ 0 on u ≤ u* > 0, so the tail is empty at every β. Monotone sum vs integral error ≤ G(s) = O(ln s). Hence B(s) =
s^{1/β}C_Z(β)(1 + o(1)) in exactly the two stated cases, given more than s^{1/β}/u*^{1/β} modes. Separation by mode (D1) is the
standard I(X;X̂) ≥ Σ I(X_i;X̂_i) for independent X_i with additive distortion. Correct.

Own mode sum (`rev_modesum*.py`; my BA tables, head beyond u = 60 by the Shannon slope ½ per nat of ln u, entropy cap for discrete
shapes; N = 2·10⁶ modes): local exponent d ln B/d ln s vs 1/β.

| β (1/β) | s | Gaussian | uniform | Laplace tr. | two-point | three-point |
|---|---|---|---|---|---|---|
| 0.6 (1.6667) | 10³ | 1.6667 | 1.6667 | 1.6594* | 1.6667 | 1.6667 |
| 0.6 | 10² | 1.6679 | | 1.6677 | | 1.6669 |
| 0.9 (1.1111) | 10³ | 1.1122 | 1.1122 | 1.1122 | 1.1112 | 1.1113 |
| 1.5 (0.6667) | 10⁵ | 0.6675 | | 0.6676 | | 0.6668 |
| 2.0 (0.5) | 10⁵ / 10⁶ | 0.5039 / 0.5014 | | 0.5040 / 0.5015 | | 0.5009 / 0.5003 |

(*) At s = 10³, β = 0.6 the truncated Laplace needs (s/u*)^{1/β} ≈ 4.4·10⁶ > N modes; at s = 10² it returns 1.6677. The
β = 1.5, 2 deviations at s = 10³ (0.68, 0.53; in the files) shrink as O(ln s/s^{1/β}) at larger s, as D4 says. As the author
notes, grid sources are sub-Gaussian, so numerics cannot test true heavy tails; the β > 1 heavy-tail case rests on the proof.

**β < 1 consequence.** INTERNAL_MODEL §4: share(Q) = κ(F + c(Q/κ)^{1/β})/Q has an interior minimum iff β < 1, which uses bits ∝
Q^{1/β}. So the interior minimum is derived exactly where the exponent is at β < 1 (sub-Gaussian shapes), and its "only if" half
(no interior minimum, share falling) holds for any finite-variance shape at β > 1 and for sub-Gaussian shapes at β = 1. The PR's
"interior minimum derived for sub-Gaussian shapes only" is correct and not over-broad.

**Heuristic, not a proof (author Q4).** For a not-sub-Gaussian shape the gain above zero rate comes from rare tail events. A
one-bit flag on {Z > a} costs ≈ p ln(1/p) nats and saves u·p·E[Z|Z>a]². For an exponential tail (Laplace) the break-even a is
≈ const/u, so p and hence G(u) look like e^{−Θ(1/u)}: G(u) = o(u^{1/β}) at every β, and the exponent would survive. For a
Student-t tail with ν degrees of freedom, p ~ a^{−ν} with a ~ √(ln(1/u)/u), so G(u) ≈ u^{ν/2} up to logarithms, and the tail sum
converges iff βν/2 > 1. If the matching upper bound holds, **Q^{1/β} fails at β ≤ 1 for ν ≤ 2/β** (bits then grow with the
number of modes), e.g. natural-image β ≈ 0.905 would need ν > 2.21. This is consistent with the proved β > 1, ν > 2 case. Not
quick to make rigorous (needs an upper bound on the optimal rate, not one scheme), so it is queued in REGIME-C-HEAVY-TAIL-LOWBETA's
note; it confirms that the "not derived" bullet is a real limit, not a formality.

## 4. Rulings on the author's questions
1. **D3 complete?** Yes, with the monotone-convergence line in §2 (covers infinite c(y₀)). Prior art: not credited (unread);
   item stays.
2–3. **§0 length.** Use the short form: "for Gaussian modes (wider scope and what is not derived in §2.2)". Reason: §0's
   time-spectrum sentence already uses "for a Gaussian world … (premises per row in §2.2)"; the long parenthesis was a second
   theorem statement in the headline; and "Gaussian modes" is automatically independent, so the short form is true and never
   wider than §2.2. Applied (fix F1). The survival-tax clause stays outside the scope phrase, as in the PR.
4. **Laplace small-u bound.** Not quick; heuristic recorded above and queued (REGIME-C-HEAVY-TAIL-LOWBETA note extended).
5. **Where the prereg-case rule lives.** Keep it in §2.2 Regime C (N6 cites §2.2 for Regime C, so it binds through N6), with
   "before the data" added (F2), matching N6's lock. Not moved into N6 now: a default for a prereg that states no case (e.g.
   "scored as if the premise holds", mirroring v1.4.4's linear default) is a kill-condition addition and needs its own author and
   reviewer; queued as REGIME-C-PREREG-CASE-N6.

## 5. Fixes applied (narrow; all wording, no math change)
- **F1** §0: Regime C scope parenthesis shortened to "for Gaussian modes (wider scope and what is not derived in §2.2)".
- **F2** §2.2 Not-derived bullet: "tails heavier than Gaussian" → "a shape that is not sub-Gaussian (tails heavier than any
  Gaussian, e.g. Laplace or Student t)" (u* = 0 exactly when v* = ∞; a sub-Gaussian shape with v* > 1 also has heavier tails
  than the unit Gaussian but still has a cutoff); "states, before the data, which case".
- **F3** §2.2 natural-images line: "needs the premise above with a sub-Gaussian shape (independent modes of one shape; not
  checked for image modes)", so independence is not dropped.
- **F4** §13 changelog: review record; "heavier-than-Gaussian tails" → "shapes that are not sub-Gaussian"; merge note.
  CLAIM_MAP v2.18 note: review outcome and the same wording; kept as v2.18 and placed before v2.19 (pick 15) and v2.20 (pick 19);
  the CLAIM_MAP note order was made ascending (v2.20 moved after v2.19; text unchanged). THEORY header pointer → v2.20.
- The author note `REGIME_C_PREMISE.md` is left as authored (history); its "heavier-than-Gaussian" means "not sub-Gaussian".

## 6. Goalposts and consistency
N6 text unchanged; it cites §2.2 for Regime C, which now carries the premise; consistent with v1.4.5's single-locked-optimum rule.
No locked prereg tests Regime C. No row or status change; no field result touched. Nothing widened: §0 now says less than §2.2;
§2.2's widened proof scope is backed by D3/D4 as checked here. Rebased onto main dbf016b (picks 15 and 19 merged: ledger 91–95,
CLAIM_MAP v2.19, v2.20); conflicts in ledger, items and CLAIM_MAP resolved keeping both sides.

## 7. New items
- REGIME-C-PREREG-CASE-N6 (w 1, c 0.5): default scoring for a Regime C prereg that states no case; kill-condition text,
  separate author + independent reviewer.
- Notes extended: REGIME-C-HEAVY-TAIL-LOWBETA (Student-t threshold ν ≤ 2/β heuristic; exponential-tail e^{−Θ(1/u)} heuristic),
  REGIME-C-PRIORART-USTAR (KKT/Gibbs-channel pointers, unread).

Surprise read: **moderate, untested** — the heuristic says polynomial-tailed modes at β ≤ 1 may break Q^{1/β} outright, not just
leave it underived; a candidate discriminating case for REGIME-C-HEAVY-TAIL-LOWBETA.
