# CAUSAL-POWER-GATE (pick 19, unaided slot; ledger 92–95), merged with KG-FEASIBILITY-GATE

15 Nov 2026, about 4:50 PM ET. Executor queue-pick19 (for Ace, Chad t1914). Process item: a lock-time rule, a reusable
tool and its checks. **THEORY.md not edited; no CLAIM_MAP status changed.** The rule lands in `measurement/FRAMEWORK.md`
§2.2 as gate **MV10** and in `QUEUE.md` rule 2; the tool is `tools/power_gate.py` (tests `tools/test_power_gate.py`).
Checks against pick 15: `reviews/night2/CAUSAL_POWER_GATE_checks/verify_caiso.py` (+ `.out`).

## 1. The problem (pick 15)
STAKES-SHIFT-CAISO locked a one-year causal contrast: D = Δlog MSE(RTD − DA) − ⅓ Δlog MSE(naive), 2026 vs 2025, predicted
D = −⅓ Δlog w = +0.138 from the clean 2024→2025 stakes change (Δlog w = −0.41). PASS iff D − 1.96·se_tot > 0 and
D ≤ band top (0.352); FAIL iff D + 1.96·se_tot < 0.05; se_tot = √(s_yr² + se_boot²) = 0.342 (s_yr 0.315 from 6 earlier
year pairs). It ended INCONCLUSIVE by gates, but it could not have ended any other way, which no pre-lock check caught.

## 2. First principles
A causal-form test reads a contrast whose expectation, if the locked optimum is right, is the locked elasticity times the
measured input change, E[D] = b·Δlog x, and whose noise is what the same contrast does when nothing changed: the
year-to-year (or unit-to-unit) sd σ, which already contains sampling noise. Nothing else enters. With K independent
contrasts of sizes d_k and a common b, the slope through the origin has se σ/S with S = √(Σ d_k²), so the only number
that matters is the signal-to-noise ratio **SNR = |b|·S/σ**.

Decision rules of the usual form, oriented so the predicted move is positive: PASS iff D − zσ > 0; FAIL iff
D + zσ < κ·bS (the data exclude κ of the predicted move), z = z_{1−α/2}. Then

- P(PASS | prediction true) = Φ(SNR − z),  P(FAIL | design does not respond, b = 0) = Φ(κ·SNR − z).

**Gate:** both ≥ π (stated in the prereg; default 0.8) ⇔

  **|b|·S ≥ (z_{1−α/2} + z_π)·σ / min(1, κ)**, i.e. the needed input change is **S_req = 2.80·σ / (|b|·min(1, κ))**
  log units (α = 0.05, π = 0.8), a factor e^{S_req}; or **K ≥ (S_req/|d|)²** contrasts of size d.

Three corollaries that the formula makes plain:
1. **An absolute FAIL margin cannot be bought with a bigger input change.** If FAIL is "D + zσ < ε" with ε fixed (pick 15:
   ε = 0.05), P(FAIL | null) = Φ(ε/σ − z) ≥ π needs σ ≤ ε/(z + z_π) whatever S is. Only more contrasts (σ/√K) help.
2. **A PASS band must be wider than the CI half-width.** "PASS iff D − zσ > 0 and D ≤ T" is empty unless T > zσ.
3. **Optimality form is the same rule.** Replace b·S by the gap Δ between the locked optimum and the nearest named rival:
   both rules reachable ⇔ Δ ≥ 2.80·σ. That is MV8(i) (SE ≤ |Δ|/2.8), now required of the FAIL side too.

The KG-FEASIBILITY-GATE flaw (WIKIDATA-BAND KG(a)) is corollary 1 in a counting form: a "moot" / known-groups upper bound
on a change rate is an absolute margin; at the best possible data (zero changes in n items over T years) its Wilson
upper limit is ln(1 + z²/n)/T, which must be ≤ the bound. That is a deterministic best-case check of the same rule
("each rule can fire at its own best-case data"), so **the two items are one rule** and are merged (ledger 95).

## 3. Verification (own code)
`tools/test_power_gate.py` (9 tests, pass): the formula gives P(PASS|true) = P(FAIL|null) = 0.800 exactly at S_req;
Monte Carlo agrees with the analytic probabilities within 0.004 in three designs; a 30-contrast panel with through-origin
LS reaches 0.80 ± 0.01 on both rules at S = S_req; WIKIDATA-BAND's 0.031/yr and n ≥ 63 are reproduced exactly; CLI exit
codes.

Pick 15, recomputed from `tests/STAKES_SHIFT_CAISO/results.json` (s_yr 0.3153, se_tot 0.3425, D_pred 0.1382 all match):

| quantity | value |
|---|---|
| PASS region as locked | **empty**: band top 0.352 < 1.96·se_tot = 0.671, so PASS could not fire at any D with σ as expected (P = 0; 0.005 when σ̂ is drawn from 6 pairs) |
| P(FAIL \| no response) as locked (ε = 0.05) | 0.035 (0.069 with σ̂ from 6 pairs); best case D = 0 does not fire (1.96·0.342 > 0.05) |
| P(PASS \| true) at the observed change, ignoring the band | 0.060 |
| stakes change for PASS to fire half the time (D_pred = 1.96·se_tot) | ×7.5 (×6.4 with s_yr alone): the item's "~7×" |
| stakes change for both rules at 0.8 (κ = 1) | **×17.8** (Δlog w ≥ 2.88); ×18.7 if σ̂ comes from 6 pairs; κ = ½: ×316 |
| σ needed for the ε = 0.05 FAIL rule | ≤ 0.018, i.e. ≈ 368 independent year contrasts at this noise |
| contrasts needed at |Δlog w| = 0.41 per contrast (STAKES-SHIFT-MULTIYEAR) | **K ≥ 49** (41 with s_yr alone); 17 at 0.70; 133 at 0.25 |

So "~7×" in the item understated the requirement: ×7.5 gives only a coin-flip PASS, the band made PASS impossible, and
the FAIL rule was unreachable at any stakes change. Labels unchanged: pick 15 remains INCONCLUSIVE on its proxy (N22).

## 4. The rule as written (FRAMEWORK MV10; QUEUE rule 2)
Before lock, every causal-form or optimality-form prereg (and every known-groups / moot / equivalence bound) states π
and shows, on its own planned data (planned n, span, input changes; σ measured before lock from comparable no-change
contrasts, with its df), by `tools/power_gate.py` or its own simulation of the locked decision code: P(PASS | locked
prediction true) ≥ π; P(FAIL | the null its FAIL rule targets) ≥ π; each rule fires at its own best-case data; a PASS
band is wider than its CI half-width. Output pasted in the prereg. A prereg that cannot meet it is not locked as decisive:
it is redesigned (more contrasts, bigger changes, a κ-relative FAIL margin) or locked as explicitly exploratory.

## 5. Audit of open preregs (the KG item's second half)
Locked and not yet run: **C3b** (locked 14 Nov, before this gate). Its own `power_output.txt` shows P(H1 CI > 0) 0.31–0.65
for the theory-sized effect at the projected n 300–500, and P(K1 fires | β_τ = 0) 0.13–0.23 (0.44 at n = 1200): it fails
MV10 on both sides. Not changed (the lock stands); new item C3B-GATE-ADDENDUM records this in a dated addendum before stage
4 so an INCONCLUSIVE is read as "gate not met at lock". All other preregs in the repo have results.

## 6. Not done / new items
- THEORY §1 N6 is not edited. A one-clause pointer ("locked tests meet FRAMEWORK MV10") would change kill-condition text,
  so it is queued (CAUSAL-POWER-GATE-N6) for a separate author and reviewer (Chad t1916). Not needed for the gate to bind:
  QUEUE rule 2 already binds every prereg made through the queue.
- Normal noise is assumed in the closed form; the tool's simulation takes σ̂ uncertainty (df) and resampled residuals. With
  only 6 CAISO pairs the resampled check is coarse (it gives 0 for every rule, consistent with the normal result).
- New items: CAUSAL-POWER-GATE-N6, C3B-GATE-ADDENDUM. STAKES-SHIFT-MULTIYEAR note gains K ≥ 49.
- Surprise read: **weak** (pick 15's PASS region was empty by construction; an absolute FAIL margin is unreachable at any
  input change).
