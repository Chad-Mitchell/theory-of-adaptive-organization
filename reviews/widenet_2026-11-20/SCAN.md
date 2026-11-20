# Wide-net scan: antifragility and optimal design vs GTAO (20 Nov 2026, 2:30 PM ET)

Read-only. Scanned `main` at `45a70cf` plus PR #115 (`v2.7-robust`, `6532d24`: ROBUSTNESS.md, CT37–CT40). No
ht-index/fractal branch is pushed, so that work was not reviewed. Checks: `scan_checks/scan_checks.py` → `.out`
(nice 19, ~6 s). DOIs: `scan_checks/crossref*.out`. Every DOI cited below resolved on Crossref; items marked
"no DOI checked" were not verified and must not be cited with a DOI.
Labels: KNOWN (in GTAO or prior art; nothing to add) · MISSING-TERM · CANDIDATE-THEOREM · OVERREACH.

## Top 3 (importance × confidence)

### 1. Redesign cost is missing, and without it one kill rule is wrong. MISSING-TERM, high confidence
*Claim.* J has no cost of *changing* the design. THEORY §2 counts it as a miss when "a design … fails to move with a
measured change in its inputs, by the preregistered share". T_red is defined as a smooth relaxation (closing 1 − 1/e of
the gap). With any fixed (lumpy) redesign cost k, the optimal policy is an inaction band: no change until the gap
reaches b\*. For quadratic loss and a Brownian target, b\* = (6kσ²/w)^{1/4} (Dixit 1991, doi
10.1016/0165-1889(91)90037-2; entry/exit hysteresis, Dixit 1989, doi 10.1086/261619).
*Check (C5).* Monte Carlo average cost matches kσ²/b² + wb²/6 (0.0819 vs 0.0816 at b\*). Because of the fourth root, a
redesign cost 100× smaller shrinks the band only 3.2×. Even tiny redesign costs therefore make large "non-moves" optimal.
*Why it matters.* (a) Under that rule, a qualifying system sitting correctly inside its band scores as a miss: a false
refutation. (b) Adding or removing a layer is lumpy by nature (K is an integer), so the theory should predict
**layer-count hysteresis**: K rises at a higher stake than the one where it falls. That is sharp and testable, but
the mechanism is known, so it is not novel. (c) It puts a price on CT40(c). The antifragility "option to redesign" is
worth the Jensen gain minus the redesign cost, and it pays only when regimes last longer than about the band's
crossing time. Gap 3 in ROBUSTNESS.md is this exact term.
*Counterexample/limit.* With convex (smooth) adjustment costs there is no band, only partial adjustment, and T_red
holds. So the fix is per class: preregister whether redesign is lumpy, and widen the "fails to move" threshold to b\*.
*Fix.* Add a redesign term R(Δ𝒟) to J, or state it as a dynamic problem. Change the kill rule to "fails to move
once the input change exceeds the preregistered inaction band".

### 2. Per-design J excludes bet-hedging, which is the known answer to CX7 (diversity against common mode). MISSING-TERM, high confidence
*Claim.* Selection on lineages acts on long-run (geometric) growth. When a shock hits many members at once, the
best design for the *lineage* is a mix of designs. No single-design argmin J reproduces that: J is linear in mixture
weights, and its ruin constraint is per unit (Cohen 1966, doi 10.1016/0022-5193(66)90188-3; Philippi & Seger 1989, doi
10.1016/0169-5347(89)90138-9; Kussell & Leibler 2005, doi 10.1126/science.1114383; Seger & Brockmann 1987, no DOI
checked).
*Check (C2).* Take a lean design ×1.30 in calm and wiped out by a common shock (β = 5%), and a robust design ×1.05 or
×0.90. Arithmetic expected value picks lean (1.235 vs 1.043), and a per-unit ruin constraint picks robust (G = 0.041).
The lineage optimum is 26% robust, at G = 0.128, three times the best pure design.
*Why it matters.* R1-c shows identical copies buy nothing against common mode, and CX7 leaves "the optimal form of
diversity" open. Bet-hedging answers it, as long as the objective is lifted from the unit to the lineage. Degeneracy
(Edelman & Gally 2001, doi 10.1073/pnas.231499798; Whitacre & Bender 2010, doi 10.1016/j.jtbi.2009.11.008) is the
within-individual version. **This bears directly on the next field test.** E. coli has documented phenotypic bet-hedging
(persisters). Under a per-cell J, a bet-hedging subpopulation would score as a miss. The E. coli prereg must state the
lineage growth-rate objective before any data is opened.
*Not new.* The theorem is Cohen's. What GTAO would add is placing it inside J and tying it to R1-c.
*Barbell variant (C3, C3b).* If ε is read as a *population frequency* of ruin, a two-design mix can beat the best
single design, a literal barbell (Carathéodory/LP; constrained-MDP randomization, Altman, doi 10.1201/9781315140223). In
CT22's continuous model the gain is **exactly zero** (the cost–ruin frontier is convex): OVERREACH there. With
discrete designs it is real but small: a 55/45 mix of 7 and 6 copies meets ε = 5·10⁻⁴ at 6.56 mean copies vs 7. It
holds only under the frequency reading of ε, which THEORY does not use.

### 3. Ergodicity: no structural flaw in the core; a real missing term for jump or heavy-tailed losses under multiplicative stakes. MISSING-TERM (conditional), medium confidence
*Test.* Is w·E[ℓ] an ensemble average where a time average is required (Peters 2019, doi 10.1038/s41567-019-0732-0;
Peters & Gell-Mann 2016, doi 10.1063/1.4940236)?
*Answer.* (a) Not in the core. The reserve is additive, and THEORY's A2 assumes stationarity and ergodicity, so the
time average equals the ensemble average (Birkhoff). If loss acts on log-reserve (W′ = W·e^{−wℓ}), J is exactly the
time-average growth. (b) In the linear-Gaussian squared-error class, even arithmetic multiplicative growth ranks
designs the same way, because E ln(1 − wℓ) is monotone in E[ℓ] when ℓ = σ_e²χ²₁ (C1c). (c) It bites when losses
are lumpy or heavy-tailed and act on returns (W′ = W(1 + g − wℓ)): time-average growth carries a drag of about
w²E[ℓ²]/2. In R1, a failure that costs 60% of the reserve gives n = 3 copies under J but **n = 4 under time-average
growth** (C1b). This is the same region where robustness lives (R1, R2-d).
*Does the ruin constraint fix it?* Only partly. Multiplicative wealth never hits 0, so "ruin = reserve hits 0" misses
it entirely. With ruin defined as falling below a threshold over a long horizon, it fixes the *sign*: Peters' coin
has an ensemble mean of +5% per step but a time average of −5.3%, and P(min W < 0.01 by T = 1000) = 1.00, so it is
excluded. It does not fix the *ranking* among designs that survive.
*Fix.* Per class, preregister whether stakes are additive or multiplicative. For the multiplicative case, replace
w·E[ℓ] with −E ln(1 + g − wℓ), or add the second-order drag term.

## Bode sensitivity integral ("conservation of fragility"): OVERREACH for the current theory; a needed constraint for CX2
*Test (C4).* I took the optimal steady-state tracker of two OU modes (3 and 90 time units) seen through white noise,
with S = 1 − H. Numerically, ∫₀^∞ ln|S(jω)| dω = −5.40745 = −(π/2)·lim sH(s), the identity for a relative-degree-1
filter with no right-half-plane zeros. **No band shows |S| > 1**, so there is no waterbed. In GTAO's present class
(the world is exogenous, g = 0, pure estimation), total log-suppression is paid by the filter's high-frequency gain,
meaning the sensing noise it lets in. That tradeoff is already in J. The integral is an identity that every causal
design satisfies, not a new constraint on where layers go. The waterbed (∫ln|S| ≥ π·Σ unstable poles, and worse with
delay) appears once the system *acts on* the world through a loop (Freudenberg & Looze 1985, doi
10.1109/tac.1985.1104004; Seron et al. 1997, doi 10.1007/978-1-4471-0965-5; robust-yet-fragile, Csete & Doyle 2002,
doi 10.1126/science.1069981; cellular analogue, Lestas et al. 2010, doi 10.1038/nature09333). → The CX2/CL11 work (the
drift lever g ≠ 0) must include it. There it predicts that suppressing slow-scale error forces amplification at fast
scales, which would constrain layer placement. Not shown here.

## Field-by-field (contained? contradicts? missing? new theorem?)
| Field | Verdict | Note |
|---|---|---|
| Taleb & Douady convexity (doi 10.1080/14697688.2013.800219) | KNOWN | CT40(a–c) is the convexity reading. CT40(c) needs #1's price |
| Barbell | OVERREACH (continuous) / small MISSING-TERM (discrete, frequency-ε) | C3/C3b above |
| Real options, Dixit–Pindyck; Oi (doi 10.2307/1907687), Hartman 1972, Abel 1983 (no DOI checked) | KNOWN in CT40(c) (Oi–Hartman–Abel = Jensen on J\*); MISSING-TERM: irreversibility/hysteresis | #1 |
| Ergodicity / Kelly | KNOWN in GENERAL_THEOREM (Kelly ≤ I); conditional MISSING-TERM in J | #3 |
| HOT, robust-yet-fragile (doi 10.1103/PhysRevE.60.1412) | KNOWN, in CT39 | — |
| Bow-tie (doi 10.1016/j.tibtech.2004.07.007) | KNOWN, consistent | the shared knot = shared layer, and also a common-mode point (R1-c) |
| Hormesis / adaptive stress response | MISSING (K7 open) | needs a state-dependent design plus g; not derivable now |
| Degeneracy vs redundancy | MISSING-TERM | only identical copies are in the design space; see #2 |
| Kashtan & Alon modularity (doi 10.1073/pnas.0503610102) | MISSING (no varying goals, no redesign cost) | "modularity lowers redesign cost under regime change" is a plausible theorem once #1 is in. OVERREACH today |
| Ashby / Conant–Ashby (doi 10.1080/00207727008920220) / IMP (doi 10.1016/0005-1098(76)90006-6) | KNOWN, in INTERNAL_MODEL.md | no contradiction |
| Free energy principle | KNOWN, cited | no new term |
| Stigmergy | KNOWN, CT30 | — |
| Holling panarchy (doi 10.1007/s10021-001-0101-5) | OVERREACH to claim | non-stationary and endogenous: CX2 territory |
| Bet-hedging (Cohen; Seger & Brockmann) | MISSING-TERM | #2 |
| Explore–exploit / dual control (Bar-Shalom & Tse 1974, doi 10.1109/TAC.1974.1100635) | MISSING-TERM, medium | reads also learn *parameters*, which shrinks R2's ambiguity u. R2 treats u as fixed by the record |
| Bode integral | OVERREACH now; needed for CX2 | above |
| Ostrom polycentricity (doi 10.1257/aer.100.3.641) | KNOWN, consistent with the federation results (CT26–29) | — |
| Simon near-decomposability (1962; no DOI checked) | KNOWN, CT34 exact nesting | — |

## Self-deception audit
- Two of my own candidate "big" findings died in their checks. The **barbell** gives zero gain in CT22's model. The
  **Bode conservation law across time scales** finds no waterbed in GTAO's current class.
- Ergodicity was downgraded from "structural flaw" to "conditional missing term" once the LG monotonicity check ran.
- None of the top 3 is a new theorem. All three are known results the theory has not yet included. Their value is
  that they stop false misses (#1, #2) and change predicted copy counts (#3).
- Nothing here is independently reviewed. The checks are toy models with chosen parameters (C1b, C2 numbers are
  illustrative). C5's Monte Carlo is off at small b because of discrete-time monitoring.
