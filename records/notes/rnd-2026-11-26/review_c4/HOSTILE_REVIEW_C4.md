# Hostile review: C4_RECORD_ORDER.md (record-dependency order on a fixed lattice)

*Independent hostile review, 26 Nov 2026, 08:58 ET. Local only: no commit, no push, no edits to THEORY.md, CORE.md or the target note.*
Target: `rnd/stepback/C4_RECORD_ORDER.md` (sha256 prefix 00a29c3d6efb82d4). There were no scripts beside it; its only artefact is `crossref_c4.txt`.
Reviewer artefacts in this folder: `c4_lpp.c` (independent simulation in C), `run_T*_s*.out` (raw output), `brute_check.py` with `brute_check.out` (brute-force check of the order built from the literal rule), and `crossref_review_c4.txt`.
Labels: OBSERVED (simulation in this review) · PROVED (in-model) · HYP · KNOWN.

## Overall: **PASS-WITH-FIXES**
- The mathematical core holds: C4-1, C4-2, C4-3 and C4-4 (restricted as in M2), and the "light-like chains are long" break. My simulation agrees with it, and with a much larger margin than the bounds show.
- The headline process claim does not hold: **"Draft C's outcome is fixed by theorem"** (H1). Draft C as written measures a fitted *exponent*. C4-4 constrains a *prefactor* (the shape function γ(s)). In the model both fitted exponents tend to 1, so Draft C's stated prediction would come out as a false "Lorentz-like" reading, not the predicted fail.
- "Do not run Draft C" still stands, but for a different reason: as written, the measurement cannot tell the two cases apart.
- Treat this as an open miss in the Draft C design, not of C4-4.

## Independent checks run
1. **Order = nearest-neighbour increasing paths (§1).** I built the order from the literal rule ("depends on the latest earlier record at i−1, i, i+1", then transitive closure) on 40 random instances (7 sites, t ≤ 4). I compared it pairwise with the path characterisation, and compared the longest-chain DP with the closure. **0 mismatches** (`brute_check.out`). OBSERVED.
2. **Simulation** (`c4_lpp.c`): rate-1 clocks, window 2.6T+121 sites, 8 seeds at T = 4000 and 4 seeds at T = 16000. Means at the final time, OBSERVED:

| quantity | T = 4000 | T = 16000 |
|---|---|---|
| front / t | 1.006 | 0.998 |
| γ(0) = L(0,t)/t | 4.039 | 4.047 |
| γ(0.5) | 3.929 | 3.937 |
| γ(0.9) | 3.584 | 3.598 |
| γ(0.95) | 3.503 | 3.512 |
| L at the front site / t | 3.33 | 3.38 |
| Draft C fitted exponent, s = 0 | 1.0065 | 1.0043 |
| Draft C fitted exponent, s = 0.5 | 1.0082 | 1.0043 |
| γ(s)/√(1−s²) at s = 0, 0.5, 0.9 | 4.04, 4.54, 8.22 | 4.05, 4.55, 8.26 |

γ(0) is still rising slowly with t, roughly as expected for KPZ-type finite-size corrections. My estimate is γ(0) ≈ 4.05–4.07, which is inside [3, 3e ≈ 8.15]. This is an estimate, not an exact value.

## HIGH

**H1. Draft C's stated measurement does not test what C4-4 rules out, so "fixed by theorem" is false.**
- STEPBACK §6 Draft C predicts: "the fitted exponent of chain length vs √(t² − x²/v²) … differs between x/t = 0 and x/t = 0.5v by > 10%."
- In the model, L(st, t) ≈ γ(s)·t and τ = t√(1−s²). Along any ray the exponent of L against τ is **1** at every |s| < 1. Only the prefactor γ(s)/√(1−s²) depends on s.
- C4-4 is a statement about that prefactor: its divergence as |s| → 1. It says nothing that would make the exponents differ.
- OBSERVED: the fitted exponents at s = 0 and s = 0.5 agree to < 0.2% at T = 16000, and to < 0.2 points at T = 4000.
- Draft C's HYP prediction (> 10% exponent difference) would therefore *not* come true. Read literally, the run would be a "hit" for Lorentz-likeness by its own criterion, which is the opposite of what C4 says is fixed.
- At L = 401 sites, finite-size corrections could still move the exponents by a few percent, so even a "miss" there would reflect corrections and not the theorem.
- **Fix:**
  - Withdraw "Draft C's predicted fail is fixed by theorem."
  - Log the Draft C design as an open miss: the observable is wrong (exponent instead of shape ratio).
  - If C4 is ever run, the observable must be the ratio R(s) = γ(s)/(γ(0)√(1−s²)) (OBSERVED here ≈ 1.12 at s = 0.5 and ≈ 2.04 at s = 0.9), or the level-set shape. A Poisson-sprinkling control must give R ≡ 1.
  - Keep "do not run Draft C as written", with this reason.

**H2. (Process) The Draft C world has now been simulated.**
- This review looked at simulated data for the exact Draft C model. Any future C4 prereg is therefore not blind to these numbers (γ(s), exponents, front speed).
- **Fix:** state this in any future C4 prereg and cite this file. The C4 note itself said "no simulation was run". That was true when it was written; it should get an appended pointer here rather than a rewrite.

## MEDIUM

**M1. C4-1 "exactly 1": true only as an almost-sure limit, in lattice units.**
- The proof (first passage = greedy, iid Exp(1) waits by the strong Markov property, then the SLLN) is correct, and I agree with it.
- T(x) ~ Gamma(x, 1), so the front is fuzzy by about √t. P(T(x) < x) → 1/2, so pairs with x slightly greater than t *are* related about half the time. C4-4(a)'s "events with |x/t| > 1 are not related" holds only for |x/t| > 1 + ε, w.p. → 1.
- In general units v = λ·a (clock rate × site spacing), not "1".
- For Draft C's 401 sites and t ≈ 200, the measured v has roughly ±7% scatter, which would also feed the τ used in its fit.
- **Fix:** write "v = λa, asymptotically and almost surely", and state the √t width of the front.

**M2. C4-4 "no Lorentzian geometry" is proved only against flat, homogeneous 1+1 Minkowski with uniform Poisson sprinkling.**
- Brightwell–Gregory 1991 (10.1103/PhysRevLett.66.260, verified) is a flat-space result.
- To reach "no Lorentzian geometry", the note must add two steps:
  - (i) The poset is statistically translation-invariant, so a matching metric must be homogeneous. In 1+1 every metric is conformally flat, and the order fixes the conformal class.
  - (ii) A position-dependent conformal factor cannot produce the *direction*-dependence of γ(s) from one base point.
- Also, "longest chain ≈ proper time" for curved-space sprinklings is not covered by the cited flat result.
- **Fix:** restate C4-4 as "no flat 1+1 Lorentzian metric with uniform sprinkling", or add (i)–(ii) as a written step and label it.
- On like-for-like scaling, the comparison passes. In a continuum limit with c = λa fixed, density ρ = c/a². Then sprinkled chains scale as √(2ρ)·τ ∝ τ/a, and lattice chains as γ(s)·c·t/a ∝ t/a. Both are linear in the scale, with the same 1/a, so the shape-function comparison is the right one.

**M3. C4-5 (general lattices) is a sketch, not a proof.**
- "L ≥ |x|/r on the reachable region" is right.
- "Front speed finite" is asserted, not shown. It follows from the same counting bound: at most (2r+1)^N·t^N/N! paths, times rate bounds. It needs uniformly bounded per-site rates, which the note does not state.
- In d ≥ 2 the reachable set is a first-passage-type limit shape, generally not a round ball. That breaks isotropy before chain length enters, and C4-5 does not mention it.
- "Any fixed lattice" should read "periodic lattice with finite-range dependencies and rates bounded above and below". Disordered fixed graphs are not covered as written.
- **Fix:** relabel it "PROVED-sketch (in-model)". Add the counting bound for the front, and add the anisotropy remark.

**M4. Prior-art attribution overstates Bombelli–Henson–Sorkin 2009.**
- BHS 2009 (10.1142/S0217732309031958, verified; arXiv gr-qc/0605006 abstract read) proves that a *Poisson sprinkling* admits no equivariant measurable map to spacetime directions. That is sufficiency: random placement does not pick a frame.
- It does not prove that discreteness *needs* random placement. That necessity is argued, not proved, in Dowker–Henson–Sorkin 2004 (10.1142/S0217732304015026, verified) and in BHS's own introduction ("the only known possibility").
- The general point that a regular lattice picks out a frame is standard background in causal-set work. So C4's located break is KNOWN in substance. What is new here is only its specific realisation for the record-dependency rule.
- **Fix:** write "consistent with the causal-set view (DHS 2004) that Lorentz invariance with discreteness needs random placement; BHS 2009 proves the Poisson case does not break it." Label novelty as low.

**M5. C4′ (cost picks Poisson placement only if the price is boost-invariant) is fair in spirit but overreaches in two places.**
- The note already labels it CHOSEN unless the price is derived. That is honest.
- (a) Boost invariance does not single out Poisson. Mixed-Poisson (Cox) processes with a random overall density, and Poisson thinnings or superpositions, are also invariant. Poisson needs a *further* premise, such as maximum entropy at fixed density or independence. Max entropy is itself a chosen cost term.
- (b) A "price on spacetime locations" changes the model. Records on per-site clocks have fixed spatial positions, so no per-site price can make them a sprinkling. Also, in a sprinkling the order comes from the metric, not from a "latest neighbour record" dependency, so the dependency rule would have to be replaced as well.
- **Fix:** state C4′ as a HYP with three named inputs: boost invariance, a max-entropy/independence premise, and records not tied to fixed memory sites. It then reads as a relabelling unless one of those is derived, which is consistent with failure shape F2.

## LOW

- **L1. C4-3 bounds are correct and conservative.**
  - Lower bound 3: the greedy rate-3 walk plus a return step with t^{2/3} slack. I checked it; the slack is ample, since the return takes O(√t).
  - Upper bound 3e: E[#chains of N records within time t] ≤ 3^N·t^N/N!. This uses the Poisson factorial-moment measure, so repeated sites are fine. Borel–Cantelli over integer t works because L is monotone in t.
  - The simulation gives γ(0) ≈ 4.05, so the interval is about 2× wide. A trivial improvement is also available: the two-site zigzag gives only 2, so greedy at 3 is the best quick bound.
  - I found no exact time constant for this lazy, symmetric, semi-discrete Poissonian last-passage model in a short search. The model sits in the well-studied Poissonian last-passage class, but I cite nothing specific beyond what is verified below. Prior art for the exact constant: open.
- **L2. Existence of γ(s) "by Kingman" needs a sentence.** L is −∞ (undefined) when (x, t) is unreachable, so integrability fails as stated. The usual fixes are a point-to-point variant from a record to the first record at x after time t, or a bounded-holes argument. C4-4 does not need existence: liminf L/t ≥ |s| is enough. Kingman 1968 (10.1111/j.2517-6161.1968.tb00749.x, verified) should be cited if the limit is kept.
- **L3. C4-2 is much weaker than the truth.** L ≥ |x| gives γ(1⁻) ≥ 1. The simulation gives L/t ≈ 3.3–3.4 at the front site. The break is therefore stronger than stated, which strengthens the C4-4 conclusion and does not change it.
- **L4. §3 rescore.** Its "V = 2 check" premise assumed that the Draft C outcome was known. Under H1 the run is not informative as designed, not "known", so the EIV line should be recomputed. The conclusion (do not run) is unchanged.
- **L5. Wording check.** The target avoids the banned words and labels claims PROVED (in-model), HYP or KNOWN. "Located break" is acceptable. It makes no claim to derive GR or gravity, and this review makes none.

## Citations (all verified on Crossref this review; `crossref_review_c4.txt`)
- Bombelli, Henson, Sorkin 2009, MPLA 24, 10.1142/S0217732309031958
- Dowker, Henson, Sorkin 2004, MPLA 19, 10.1142/S0217732304015026
- Brightwell, Gregory 1991, PRL 66, 10.1103/PhysRevLett.66.260
- Malament 1977, JMP 18, 10.1063/1.523436
- Bombelli, Lee, Meyer, Sorkin 1987, PRL 59, 10.1103/PhysRevLett.59.521
- Kingman 1968, JRSS B 30, 10.1111/j.2517-6161.1968.tb00749.x

All five DOIs in the target's `crossref_c4.txt` match Crossref.

## Status after review
| claim | status |
|---|---|
| §1 order = increasing nearest-neighbour paths | PROVED (in-model), brute-force OBSERVED 0 mismatches |
| C4-1 front speed | PROVED (in-model) as an a.s. limit, v = λa (M1) |
| C4-2 L ≥ \|x\| | PROVED (in-model); loose (L3) |
| C4-3 γ(0) ∈ [3, 3e] | PROVED (in-model); OBSERVED ≈ 4.05 |
| C4-4 | PROVED (in-model) for flat homogeneous 1+1 with uniform sprinkling; wider claim needs M2 |
| C4-5 | PROVED-sketch (M3) |
| Draft C fixed by theorem | **does not hold** (H1): open miss in the Draft C design |
| C4′ | HYP; needs three named inputs (M5) |
