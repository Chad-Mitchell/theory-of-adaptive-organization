# ONSET-ACROSS-ALPHA-SIM results (pick 32, uniform slot; ledger 151 claim)

Private. Sunday 15 Nov 2026, about 7:05 PM ET. Lock: commit `2921bb2` on q-pick32 (PREREG.md + PREREG.sha256 + code + α = 2 pilot), pushed before any α = 1.5 or 2.5 cell ran. No post-lock code change. In-model only; not evidence about nature.

## Verdict
**PASSED in-model, on proxy "learned reset-read pooling onset in simulated fBm worlds"** (THEORY v1.4.11 §2.5 / CLAIM_MAP N12, narrowed form: same α for shared and private drift, exact reads, ρ ∈ [0.01, 0.32], one level, no broadcast cost, h = 0).

| | ê (95% CI) | theory window value | per-α rule |
|---|---|---|---|
| α = 1.5 (H = 0.25) | −0.950 [−1.053, −0.874], SE 0.048 | −0.962 | PASS |
| α = 2.5 (H = 0.75) | −0.937 [−0.974, −0.904], SE 0.018 | −0.963 | PASS |
| α = 2 (pilot, pre-lock, outside contrast) | −0.935 [−1.009, −0.871], SE 0.035 | −0.963 | (pilot) |
| **Δ = ê(2.5) − ê(1.5)** | **+0.013 [−0.072, +0.118]**, SE 0.051 | −0.0002 | **PASS** (CI inside ±0.267; not exploratory, SE < 0.095) |

All 12 design cells valid (crossing in ≥ 90% of bootstrap replicates). The rival (exponent moves with α by 0.267, as vigilance growth and the mixed private-drift exponent do over this pair) is excluded: the CI's far edge is 0.118 from the prediction. Learned lone-member intervals: median T 36 (α 1.5) and 39 (α 2.5), as the unit choice of C intended.

## Post hoc (declared after the verdict; `posthoc.py`, `POSTHOC.json`; decides nothing)
- **The constants move with α, as §2.5 says they should.** Mean ln N̂\*(2.5) − ln N̂\*(1.5) over ρ = 0.342 vs the closed form's 0.311 (= ln(4.605/3.375) at small ρ). So the simulation sees α through the level (×1.36 in N\*), but not through the slope. N̂\*/N\*_theory per cell 0.85–1.12.
- Drop-one-ρ: Δ ranges −0.066 … +0.042; per-α exponents −0.91 … −0.98. No single ρ carries the result (unlike LEARNSIM's C1).
- Noise is largest at ρ = 0.01 (sd ln N̂\* 0.22 at α = 1.5): the onset gap there is smallest; still valid.

## What this does and does not show
- Shows: in a discrete, learned world with no cost formula anywhere, selection on realized payoffs reproduces an α-independent reset-read onset exponent at α = 1.5 and 2.5 to ±0.12 (95%), with the α-dependent constant the theory names. This is the comparison §9 names as the in-model sink for N12, run once, for one technology.
- Does not show: anything about real organizations; the precision-priced class (−(1+θ)), noisy reads, different α for shared and private drift, broadcast cost or upkeep; learners noisier than population selection (LEARNSIM's ES). Remaining circularity as in LEARNSIM: any learner that minimizes realized cost approaches the world's optimum.
- Surprise (SG scale): **none** (the locked prediction held; the risk was discreteness and long-memory paths at H = 0.75 and 0.25).

## Files
`world.py`, `run.py`, `theory.py` (closed form; asymptote check N\*ρ → α^{α/(α−1)}: 3.37500 at α 1.5, 4.60504 at α 2.5), `analyze.py`, `verdict.py`, `runpilot.sh`, `runmain.sh`, `pilot_alpha2.jsonl`, `results.jsonl`, `VERDICT.json`, `POWER_GATE.json`, `posthoc.py`, `POSTHOC.json`.
