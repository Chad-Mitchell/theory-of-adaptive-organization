# GITHUB-UPSTREAM — prereg ADDENDUM (theory provenance + regime split)
Written after the main lock (71281cf) and after a parent HOLD message, **before any outcome statistic was computed** (the run pull was still in progress; nothing in data/runs.json had been analysed). Lock time = git commit time of this file. Main PREREG predictions are unchanged; this adds a regime-conditional reading required by current THEORY.md v1.1 §2.2.

## Provenance of each locked prediction (current THEORY.md, commit b13f734)
- P1 b = ½ and P2 a = ½: THEORY.md §2.2 **Regime A** (lines 80–83): "T* = √(2c/(wσ²))", i.e. read rate ∝ (w·σ²)^½ → a = b = ½. **Assumes Regime A (single characteristic pace).** Labelled KNOWN (EOQ; Lee, Flack & Krakauer 2024) — this tests calibration, not novelty.
- Current THEORY.md §2.2 **Regime B** (lines 85–87): scale-free drift → "adaptation time scales linearly with the environment's switching time (slope 1)" → read rate ∝ change rate, **b = 1**. The main PREREG did not register this; it is added below.
- P3 a = b: follows from the Regime A formula (line 82). Regime B states no stakes exponent.
- P6 vigilance floor 1+(1+ρ)^−½, growth N^a: THEORY.md §6 lines 193–197 and §9 line 288 ("units measured to be reset-type (class R)"). Regime-agnostic in the formal model (one-source, reset sensing).
- ρ (shared/private drift ratio): THEORY.md §1 N2 line 55 and §6.
- κ and P5 rank gradient â − κ̂b̂: **not in current THEORY.md** (THEORY mentions only the ordering threshold κ* line 266). P5's relation is from night2/MEASUREMENT/FRAMEWORK.md §3.9 "[DERIVED HERE]", unreviewed → **flag: possibly outdated / not in current theory.** κ itself is a measurement only.
- Sensing class (a,b) as a construct: THEORY.md lines 19, 55, 263; operational definitions only in FRAMEWORK §3.4 and night1 FORMAL (not current THEORY text) → flag.

## Added regime-conditional rule (P1-R)
Regime diagnostic (computed on the weekly state series of flat units, pooled; independent of read rates): durations (weeks) of uncensored spells of constant state. Fit geometric (single pace) vs discrete power law (zeta, s ≥ 1, x_min = 1) by maximum likelihood; ΔAIC = AIC_geom − AIC_zeta.
- ΔAIC > 10 → Regime B: P1-R band for b̂ = [0.75, 1.25] (same PASS/KILL rules as P1).
- ΔAIC < −10 → Regime A: P1-R = P1 as locked ([0.35, 0.65]).
- Otherwise → INCONCLUSIVE-regime; both bands reported, no verdict.
Declared confound: a mixture of units with different single paces also produces heavy-tailed pooled spells (FRAMEWORK §4.9 / SCALEFREE S1), so a "Regime B" diagnosis is weak. A per-unit check (share of units whose own spells reject geometric at p<0.05, KS on ≥8 spells) is reported descriptively.
Code: code/addendum.py (hashed below). Same SEED and bootstrap as main (b̂ CI is taken from the locked main analysis).
