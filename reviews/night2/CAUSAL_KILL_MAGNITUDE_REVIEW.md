# CAUSAL-KILL-MAGNITUDE-REVIEW — independent review of PR #48 (THEORY v1.4.7, N6 / §9 causal kill share)

**Queue:** CAUSAL-KILL-MAGNITUDE-REVIEW. **Out-of-cycle, unscored** (continuation of pick 24's author PR, under Chad's t1916
independent-review rule; no rank or pick logged; outcome ledger 124). 15 Nov 2026, about 5:25–5:50 PM ET (America/New_York).
**By:** independent reviewer executor (for Ace, Chad t1914/t1916). **Exposure:** I authored none of
`CAUSAL_KILL_MAGNITUDE.md`, its checks (`band_mc.py`, `kappa_grid.py`), PR #48's text, N6, §9, R2, the pick-17 note or
review, or `tools/power_gate.py` before this review. I did not import or run the author's checks to produce my numbers;
my code (`CAUSAL_KILL_MAGNITUDE_REVIEW_checks/`) only takes the author's scenario parameters so that the tables can be compared.
**Scope:** THEORY §1 N6 causal cell, §9 causal bullet, changelog/header; FRAMEWORK MV10 pointer; `tools/power_gate.py`
defaults. No CLAIM_MAP row status changes. Vigilance stays OPEN. Results are in-model (Gaussian contrasts) unless labelled otherwise.

## Verdict: **PASS-WITH-FIXES**
The clause is right from first principles and its table reproduces. The fixes are wording and tooling only. None of them
changes the clause's meaning except F3, which closes a loophole, and F4, which writes down the one case v1.4.5 already left
unscored. That keeps the kill no weaker than the author intended.

## 1. First principles (re-derived, not read off the note)
A causal contrast reads the slope b̂ of the log design quantity's move on the measured log input change. Write the true
input change d, the measured one d + u, and the design's realised share s at lag L (first-order: s = 1 − e^{−L/τ}). Then
E[b̂ | data] ≈ b·s·λ, with λ = var d / (var d + var u). Neither s nor λ can flip a sign, but both shrink the slope.
So:
- **A sign rule** (kill iff b̂ + z·se < 0) cannot be fooled by s, λ, or a smaller-but-same-sign Bayes elasticity. But under
  b = 0 its kill rate is its size, whatever the data. N6's own named rival (fixed share, b = 0) therefore survives a
  sign-only causal kill about 95% of the time. **Confirmed** (§2: 0.057 at z = 1.645, 0.029 at z = 1.96).
- **A one-sided share rule** (kill iff b̂ + z·se < κ·b\*·s·λ) holds its size on a true design whenever the scaled
  prediction overstates the truth by less than 1/κ. κ is therefore the multiplicative bias the kill tolerates: estimation
  error in s, λ, α̂, or a different optimum's smaller elasticity. κ = 1 tolerates none, while κ = ½ tolerates up to 2×.
  That is the first-principles reason for the cap ½ (the author's §5(ii)), and §2–3 confirm it numerically.
- **Over-response** (b > b\*) is never a causal kill under this rule. That is correct: an over-response is a size miss,
  and the optimality form scores it.

## 2. Q3 — Does the table reproduce? **Yes**, within Monte Carlo error.
I wrote my own vectorised code (20,000 studies per cell vs the author's 4,000; seeds 101/202), with K = 30, sd(Δx) = 0.5,
σ_y = 0.15, b\* = ½, OLS through the origin. The author's kill rates are in brackets wherever they differ by more than 0.01.

| scenario (z = 1.645, as the author) | sign | sym. band | κ=¼ | κ=½ | κ=1 | κ=½ s·λ | κ=1 s·λ |
|---|---|---|---|---|---|---|---|
| true, clean | 0.00 | 0.06 | 0.00 | 0.00 | 0.056 | 0.00 | 0.056 |
| true, s = 0.63 | 0.00 | 0.89 [0.85] | 0.00 | 0.003 | 0.94 | 0.00 | 0.055 |
| true, s = 0.39 | 0.00 | 1.00 | 0.002 | 0.255 | 1.00 | 0.001 | 0.055 |
| true, λ = 0.5 | 0.00 | 0.97 | 0.00 | 0.056 | 0.99 | 0.00 | 0.056 |
| true, s = 0.63 & λ = 0.5 | 0.00 | 1.00 | 0.011 | 0.60 | 1.00 | 0.001 | 0.059 |
| true, α̂ se 0.3 (new row) | 0.00 | 0.26 | 0.00 | 0.00 | **0.20** | 0.00 | **0.20** |
| Bayes switching (κ_N16 = 10⁻³, b = 1/ℓ = 0.166) vs linear lock | 0.00 | 1.00 | 0.010 | 0.458 | 1.00 | 0.458 | 1.00 |
| false b = 0 | 0.057 | 1.00 | 0.73 | 0.993 | 1.00 | 0.993 | 1.00 |
| false b = b\*/4 | 0.00 | 1.00 | 0.057 | 0.726 | 1.00 | 0.726 | 1.00 |
| false b = −b\*/2 | 0.993 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| false b = 0, s = 0.63, λ = 0.5 | 0.054 | 1.00 | 0.92 | 1.00 | 1.00 | 0.648 | 0.981 |

At MV10's two-sided z = 1.96 (the tool's rule) the rates fall as expected. True clean κ=1: 0.032; b = 0: sign 0.029,
κ=¼ 0.615, κ=½ 0.987; scaled b = 0 with nuisances: κ=½ 0.525; Bayes vs linear lock κ=½: 0.347 (`reviewer_mc.out`). ℓ =
ln(2/κ_N16) − γ − 1 = 6.024 at 10⁻³, as in `V143_INDEPENDENT_REVIEW.md`. The note's "κ=½, true s=0.63: 0.00" is 0.003 here
and 0.002 in its own `band_mc.out`, so it is rounding, not an error. The new α̂ row is a third, independent reason against κ = 1:
the elasticity is 1/α, and an α̂ se of 0.3 alone kills a true design 20% of the time at κ = 1 and 0% at κ = ½.

## 3. Q2 — Extra wrong kills from estimating s and λ (simulated)
Model (`reviewer_mc.py` q2, `reviewer_stress.py`): τ is measured with lognormal error, sd(log τ̂) ∈ {0.1, 0.25, 0.5, 1.0}.
λ̂ = 1 − σ̂_u²/var(Δx_obs), with σ̂_u² from m duplicate input measurements (m ∈ {10, 20, 50, 200}). I compared two rules:
"plug" uses ŝ·λ̂ as if known; "prop" adds the delta-method variance of κ·b\*·ŝ·λ̂ to se² before deciding. Below, a true
design is b = b\*.

| setting | κ ≤ ½, plug-in, extra false kills vs known s, λ | κ = 1, plug-in | with propagation |
|---|---|---|---|
| author's regime: s ∈ {0.39, 0.63}, λ ∈ {1, 0.5}, sd log τ ≤ 0.5, m ≥ 20 | **≤ +0.010** (z 1.645), ≤ +0.006 (z 1.96) | 6–19% (nominal 5.5%) | κ ≤ ½: at or below known; κ = 1: 4–7% |
| stress: s ∈ {0.10, 0.22}, λ ∈ {1, 0.3}, sd log τ up to 1.0 (τ known only within a factor e), m ≥ 10 | up to **+0.07** at κ = ½, +0.016 at κ = ¼ | up to 26% | κ ≤ ½: ≤ +0.009 |

Cost of propagation: power against b = 0 drops by up to 0.25 at κ = ½ (e.g. 0.53 → 0.28 at s = 0.63, λ = 0.5, sd log τ = 0.5,
m = 20). Plug-in costs at most 0.06. **Ruling:** at κ ≤ ½, estimating s and λ adds at most about one percentage point of
wrong kills in realistic settings. It adds up to seven points only when the lag is short relative to a poorly known τ, and
carrying the estimation error into the decision removes that. At κ = 1, plug-in estimation alone pushes wrong kills to
2–5× nominal. So the cap holds, and the text should say the errors of s and λ count in the measurement error (fix F2). The
power gate has to simulate the propagated rule, because propagation costs power.

## 4. Q1 — Should κ be capped lower (≤ ¼) for linear-locked tests while the premise test is jump-blind? **No.**
Reasons, from §1 and `reviewer_mc.out` (q1, analytic):
1. **A cap does not fix the problem; it moves it.** Score a Bayes-optimal switching design against the linear lock. The
   scaled prediction then overstates its move by ℓ/2, so with enough data it is killed whenever κ > 2/ℓ, and ℓ grows with
   ln(1/κ_N16). At K = 30 and κ = ¼ the kill rate rises with κ_N16 from 0.00 (10⁻²) to 0.06 (10⁻⁴) and 0.22 (10⁻⁶). At K
   = 120 it reaches 0.54 (10⁻⁶). No fixed cap is safe for every switching world, and κ = ⅛ only postpones the same limit.
2. **It is costly against the theory's own rival.** At K = 30, power against b = 0 is 0.74 at κ = ¼ against 0.998 at
   κ = ½. Under MV10, halving κ doubles S_req, which means about 4× the contrasts.
3. **The kill is legitimate under the lock rule (v1.4.4).** A linear-locked test that kills a system which is actually a
   Bayes-switching tracker has found exactly what N6 risks: its default prediction is wrong for that system. N6 already
   says the premise cannot excuse a locked miss afterwards. A cap written in would partly undo that rule for linear locks.
4. What *is* missing is information at lock time. Make every linear-locked causal prereg report, at its chosen κ_F and on
   its own planned data, the kill probability under the Bayes-switching alternative at its measured jump inputs. If it
   cannot measure them, it should report a stated κ_N16 range, or show a validated jump screen. That is a prereg reporting
   rule, not theory text. **New item LOCK-SENSITIVITY-REPORT** (FRAMEWORK MV10 addition plus a `power_gate.py` option;
   joins PREMISE-TEST-WIDEN).

## 5. Q4 — Versioning: **v1.4.7**, set by this review
The clause widens the kill and changes no headline, core, row or status. That makes it a patch, as were v1.4.5 and v1.4.6.
The header now says v1.4.7 and the changelog entry is rewritten as merged, with this review recorded. The author's entry was
stamped "about 5:40 PM ET", but both of its commits are 5:19–5:20 PM ET. I corrected the stamp to the commit time and left
`CAUSAL_KILL_MAGNITUDE.md` (frozen, on main) as written. The header's CLAIM_MAP pointer was stale (v2.20; main has v2.23) and
now reads v2.25.

## 6. Fixes applied (narrow)
- **F1 Symbol.** "κ" is already used in THEORY for N16's λN/μ² (§2.2 Regime A premise bullet), for Regime C's price of a
  nat and Q_min = κF/μ (§2.2), and for the κ\* ordering threshold (§8b); FRAMEWORK MV3 also lists a κ input. N6 and §9 now say **κ_F**, glossed as "FRAMEWORK MV10's κ, not the
  other κ's of this file".
- **F2 "excludes" → "falls short, in the predicted direction and beyond measurement error, of a share κ_F of the move …"**,
  with "their errors counted in the measurement error" for s and λ. A measured move does not "exclude" anything; its
  interval does. This reading is one-sided, which is the rule the author simulated, and matches the optimality form's
  "beyond measurement error". It also makes the Q2 result binding.
- **F3 Identification loophole.** If s is estimated from the design's own response to the changing inputs, a non-responder
  gives ŝ ≈ 0, the scaled prediction ≈ 0, and the kill falls back to the sign rule's 5% power against b = 0, which is the hole
  the clause closes. N6 now says s and λ are measured before the data **and not from the design's response to the inputs
  under test**. They can come instead from the design's own relaxation after other perturbations, from a documented
  adjustment mechanism, or by choosing a lag long enough that s ≈ 1 at the upper bound of τ.
- **F4 Zero predicted move.** For a joint input change that leaves the locked optimum fixed (v1.4.5's case), the new
  wording would have had no defined direction. "A predicted move of zero is not scored by this form" keeps v1.4.5's
  behaviour; CAUSAL-NULL-INVARIANCE stays the place for a null kill. "A move of the wrong sign is the case of any κ" now
  reads "a clear move of the wrong sign is therefore a kill at any κ_F".
- **F5 Tooling.** `tools/power_gate.py` now defaults to κ = ½ everywhere (`required`, `analytic`, `simulate`, `gate`), and
  `--scale s·λ` was added. A κ-relative gate with κ outside (0, ½] is **not met** (`kappa_in_N6_range: false`). An absolute
  ε margin is flagged as not N6's form. Historical κ = 1 numbers (pick 15's ×17.8, K ≥ 49) are kept in the tests with
  κ = 1 passed explicitly. New tests cover the default, the range, the CLI scale, and κ=1-vs-½ under partial adjustment. At κ = ½ the STAKES-SHIFT-MULTIYEAR requirement becomes **K ≥ 193** contrasts of |Δlog w| = 0.41
  (×317 for one contrast), against K ≥ 49 at κ = 1. The QUEUE note is updated.
- **F5b Optimality form kept at κ = 1.** MV10's optimality form ("gap Δ ≥ 2.80σ") is κ = 1 and is not governed by N6's
  causal bound. `gate()` / `contrast` therefore take `form = causal | optimality`: causal is the default, with κ = ½ and the
  range check; optimality keeps κ = 1 and has no range check. Two existing scripts relied on the old default. I added
  `form="optimality"` to `tests/SPF_RIGIDITY_OOS/power.py` and an explicit `kappa=1.0` to
  `reviews/night2/CAUSAL_POWER_GATE_checks/verify_caiso.py`. Both are compatibility edits, and both reproduce their
  recorded outputs: a new test checks `power.json`, and `verify_caiso.out` is byte-identical on re-run. 19 tests pass.
- **F6 FRAMEWORK MV10** gains the pointer the author proposed: κ ≤ ½ per THEORY §1 N6, with the prediction scaled by s·λ and
  their errors propagated.

Re-read after the fixes in a second hostile pass. The N6 cell and §9 bullet say the same thing; §9 keeps "beyond measurement
error" and the bound but defers the scaling details to N6, as it does for inputs. No other THEORY text paraphrases the causal
kill (grep for "does not move in the direction" / "stays put" outside `reviews/` and the changelog: none).

## 7. Goalposts: no locked prereg moves
I checked every prereg file on main and on every `origin/` branch (no prereg exists only on a branch, except earlier
versions of merged ones).
- **Locked under N6's causal form: one, STAKES-SHIFT-CAISO** (lock 874576f; linear-locked; 12-month lag). Its own FAIL rule
  (absolute ε = 0.05) governs, and the result was INCONCLUSIVE on its proxy with a validity limit breached. Under the new
  wording it still could not fail: D = −0.088, and D + 1.96·0.342 = 0.583 > κ_F·0.138 ≤ 0.069 for any κ_F ≤ ½. **Unchanged.**
- **C3b** (locked 14 Nov, not run): it tests the shock × √(time to fix) relation (C3/F1 line), not N6. Its MISS rule
  (H1 β_τ CI upper < 0.15 against a theory-sized 0.25) is its own locked magnitude rule. **Unaffected**; it still fails MV10
  at lock (CAUSAL_POWER_GATE §5), and C3B-GATE-ADDENDUM stays open.
- **N6 optimality form or N13 probes**, untouched by this clause: LFK-ALPHA-SPF (INCONCLUSIVE), SPF-NOISE-PROXY
  (measurement), STAKES-EXOGENOUS (measurement, no N6 verdict). **Unchanged.**
- **Other locked tests** (not N6): ANTS1, BIO1, C3, COLLAPSE1, D3-OOS, DRIFT1, F1, LEARNSIM, MATCH1, GITHUB-UPSTREAM,
  WIKIDATA-BAND, VIGIL-ONA (vigilance OPEN). **Unchanged.** SPF-RIGIDITY-OOS was never locked (MV10 not met; at κ = ½ it
  is further from the gate, with no result change).

## 8. Limits
Gaussian contrasts; OLS through the origin; one SNR family (K = 30, 120 analytic); first-order partial adjustment, so a
dead-time design needs s measured differently; the delta-method se for ŝ, λ̂ assumes the analyst reports them. N16's 1/ℓ is
taken from its refereed closed form, not re-derived. No prior art read; nothing credited.

## 9. New items
- **LOCK-SENSITIVITY-REPORT** (w 1, c 0.5): MV10 reporting line plus a `power_gate.py` option, giving each linear-locked
  causal prereg's kill probability under the Bayes-switching alternative at its κ_F (§4).
- No other new items. The F3 identification guidance is in N6 already; CAUSAL-POWER-GATE-N6 stays open (pointer from N6 to MV10).

## 10. Surprise (queue rule 4)
Weak to moderate. The cap's justification turned out to be a bias tolerance (1/κ), which unifies three separate threats
(estimated s and λ, α̂ error, a different optimum). And a lower cap cannot protect linear locks from switching worlds at
any fixed value.
