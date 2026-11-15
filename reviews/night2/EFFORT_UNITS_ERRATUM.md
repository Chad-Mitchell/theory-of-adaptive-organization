# EFFORT-UNITS-ERRATUM (QUEUE pick 25, rule slot)

Sunday 15 November 2026, about 5:40 PM ET. Grok Bot executor (queue-pick25) for Chad Mitchell, via Ace. Private; nothing posted or sent. Ledger 116 (unaided order), 117 (rule_rank), 118 (claim), outcome entry after this file.

## What was claimed to be wrong
`reviews/night2/N12_REFEREE.md` C3: formal Lemma 1(viii) (`reviews/night1/formal/THEOREMS.md`) says information effort "(read rate, information rate, precision) equals spend/price", so effort elasticities are (a, b). In A_θ (precision priced as c·precision^θ) that holds only at θ = 1; precision elasticities are (a/θ, b/θ), and small-share onset vigilance is ∝ ρ^{−θ} in spend units but ∝ ρ^{−1} in precision units.

## First-principles check (own code; imports nothing from the repo)
`EFFORT_UNITS_ERRATUM_checks/units_check.py` → `units_check.out` (seed 20261126).
- **Mechanism.** A_θ cost W·√(q r) + c·r^{−θ} (Kalman–Bucy steady error √(qr), r = noise intensity, precision 1/r). Spend is a constant share 1/(1+2θ) of φ, so spend/price = r^{−θ} = precision^θ carries φ's elasticities (a, b) = (2θ/(1+2θ), θ/(1+2θ)). Precision is (spend/price)^{1/θ}, so its elasticities are (a/θ, b/θ) = (2/(1+2θ), 1/(1+2θ)) (sympy: exact). Finite differences on the numerically optimized scalar control at 6 random (θ, W, q, c) agree to 4 decimals.
- **Vigilance.** From first principles (N members; drift = shared ρq + private q; flat members track (1+ρ)q; a level tracks ρq at pooled stakes NW; onset N* where pooling stops costing; h = 0, equal prices), small-ρ log-slopes of V(N*): θ = 0.5: −0.500 spend, −1.000 precision; θ = 1: −1.000, −1.000; θ = 2: −1.997, −0.998. V_prec = V_spend^{1/θ} to 1e−6.
- **Invariants.** Every elasticity sign, the ratio b/a, the a = b test, "V > 1 iff a ≥ b" and h = 0 price invariance are the same in both units (V^{1/θ} > 1 iff V > 1).
- **Unaffected rows.** R1 (read rate = spend/c), R2 (information rate = spend/λ), rows (iv), (v) and A₁ (θ = 1): spend is linear in effort, so the two units coincide.

**Verdict on C3: confirmed** (in-model, own derivation).

## Changes (minimal, dated; proofs left as written)
- `reviews/night1/formal/THEOREMS.md`: erratum notes under Lemma 1(viii) and under the T5 Definition (items 3 and 5 in precision units; items 2 and 4 unchanged).
- `reviews/night1/formal/FIXES.md`: new section G, row G1.
- `measurement/CLAIM_MAP_v2.md`: v2.23 note; unit qualifiers on A5, E9, E10. **No status change**: A5's night-1 scope (`reviews/night1/CLAIM_MAP_FINAL.md`) already said "in A_θ, effort means r^{−θ}", and E10 is true in T5's own spend/price units; N12 already named both units.
- THEORY.md: **not edited** and needs no edit. Its §2.2 precision-effort row is already scoped to linear pricing (θ = 1), its §2.5 N12 bullet already gives ρ^{−θ} in spend units and ρ^{−1} in precision units, and its §8b/§9 vigilance tests use reset-type (class R) units. FRAMEWORK §3.4 already warns that effort in A_θ means r^{−θ}.

## Locked preregs
None move. SELF P2/P3b cite L1(viii) for R1 reset reads (read rate = spend/price exactly). STAKES-SHIFT-CAISO locks θ = 1 (units coincide) and already cites this item. STAKES-EXOGENOUS draws no verdict from precision. Vigilance tests (VIGIL_ONA, FRAMEWORK §6.3) are in class R units. H8 vigilance stays **OPEN**.

## Not done / limits
In-model only; A_θ at α = 2 (the formal row). The α-general precision row of THEORY §2.2 under non-linear pricing was not re-derived here (THEORY already says any other price exponent changes both elasticities). No prior art read or credited. Not independently reviewed: this is a dated erratum confirming an independent referee's finding, with no status change and no THEORY edit.
