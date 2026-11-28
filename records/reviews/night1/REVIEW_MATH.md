# Referee report (mathematics): GTAO FORMAL/AXIOMS.md + THEOREMS.md

Sunday 2026-11-15, written about 03:20 ET. Independent hostile referee (a Grok Bot executor that did not write the work). Private. Nothing was posted, sent or committed, and no FORMAL file was edited.
**Anchoring control:** FIXES.md and CLAIM_MAP.md were not opened until §1–§5 below were written. §6 was added afterwards.

Reproduce: `cd REVIEW/math && nice -n 19 /tmp/rv/bin/python mN_*.py`. The outputs are in `mN.out` / `mN.log`. All scripts are mine. I compared against FORMAL/checks only where noted.

| Script | What it re-derives |
|---|---|
| m1_lemma_T1_T2.py | Lemma 1 rows (i)–(iv) symbolically; T1.2 closed form and the T3a identity; T1.3 Π\*; T1.4 elasticity (40-digit checks). All OK |
| m2_T1_T3_T5_numeric.py | T1.5 upkeep dichotomy; **T1.8 mixed-technology sign flip**; T3 random signs; **T5 exact V(N\*) at finite ρ**; R1 fBm V; per-read broadcast V |
| m3_T4_bundled.py | T4 exact (no expansion) joint optimization under bundled \|e\|^p, R1 and A₁ |
| m4_T5_T6_T7_T8.py | T5.2 "iff"; T6 brute-force submodularity, lattice, Topkis in h, accretion (common and mixed degree); T7 ordering; T7(c) "iff"; T8 symbolic |
| m5_T5_exact_closed_form.py | **New exact finite-ρ closed form for V(N\*) at γ = ½** with upkeep and prices |
| m6_P11_readability.py | Monte Carlo of P11's shared-error term |

---

## 1. Overall verdict

**Recommendation: major revision.** Do not reject.

The algebraic core is correct, and I re-derived all of it independently: the onset formula, the small-share exponent −(1−b)/(1−a), the upkeep dichotomy, the T3 signs for a common technology, T4's bundling exponent (confirmed by exact optimization without expansion), the T6 Topkis/lattice structure, the T7 ordering, and the T8 edges. My numbers match theirs to 3–4 digits wherever we overlap.

There are three real problems:

1. **The headline vigilance bound "V ≥ 2 at onset in the read-based class, whatever the costs" (T5.6) is a ρ → 0 limit, not a bound.** At finite ρ with free upkeep, the exact value is V(N\*) = 1 + (1+ρ)^{−1/2}. That is **strictly below 2** for every ρ > 0, so 2 is a *supremum* at h = 0, not a floor. Under R1 with fBm drift (H > ½), which falls under Axiom 3's R1, even the limit is below 2: 1.84 at H = 0.75.
2. **T1.8's claim that T3's opposite signs survive under mixed technologies whenever b_m, b_L < 1 is false away from small ρ.** If b_L > b_m, then ∂N\*/∂q_g > 0 at large ρ. Shared volatility then *delays* the level.
3. **Several "iff"s and the blanket "every statement below is an exact iff" are overstated.** These are T5.2, T7(c), Cor 4.1 and the 𝒜₁ preamble. Some statements are asymptotic (T1.3, T5.3, T5.6) and some are only sufficient.

On novelty: most results are elementary consequences of a power-law cost function, and several have obvious ancestors that are not cited. Details are in §5.

---

## 2. Per-result verdicts

| Result | Verdict | Notes |
|---|---|---|
| Axioms | Acceptable with fixes | "Class R" is used in T5.6 but never defined. R1 is defined for fBm, which matters for T5.6 (Issue 2). Axiom 6's "costs add exactly" is fine for quadratic loss with independent errors. |
| L1 (i)–(v) | **Correct** | Every row re-derived in sympy (m1). Spend shares are correct. Duncan: info rate P/(2r) with P = √(qr) gives P = q/(2ι). Correct. |
| L1 (vi)–(ix) | Correct, minor wording | (vii): Jensen covers deterministic schedules at fixed n. Adaptive schedules can't help because the post-read error variance is deterministic, but that should be said. (viii): in A_θ, "effort" = r^{−θ}, not precision 1/r, unless θ = 1. V's ρ^{−θ} depends on this convention. |
| T1.1 single crossing | Correct, minor | At a = 0, G(0) = −B − h′, not −h′. Harmless. |
| T1.2 exact onset | **Correct** | (m1) |
| T1.3 small-share law | **Correct** | It's asymptotic, so it isn't an "exact iff". |
| T1.4 elasticity | **Correct** | Checked to 40 digits at random points. The sign proof reduces to (1+ρ)^{b−1} < 1. |
| T1.5 upkeep dichotomy | **Correct** | I made the proof rigorous with N = N₀y, which gives N₀^aB(y − y^a) = h′. Numerics: slopes −1.0000/−2.0000/−4.0000/−0.9988 match. |
| T1.6 prices | Correct (understated) | N\* ∝ p_g/p holds **exactly** at h = 0, not just to first order. |
| T1.7 scale effects | Correct with fix | "N\* strictly decreases in stakes when h > 0" fails at a = 0, which the hypotheses allow: G is stakes-invariant there. |
| T1.8 mixed technologies | **Correct only as ρ → 0; the last sentence is wrong** | See Issue 3 and counterexample C2. |
| T1.9 | Correct | |
| T2(a), T2(b) | **Correct** | Re-derived: boundary √(tρ) + 1 = √(1+ρ) gives ρ = 4t/(1−t)². |
| T3 (common technology) | **Correct**, technicality | Proof is valid (IFT, with G_N > 0 by convexity, and the bracket argument at N₀ ≤ N\*). m2: 0/3,191 sign violations. One edge case: if p_g < p and the root is < 1, N\* is pinned at 1 and the derivatives are 0, not strict. |
| Cor 3.1 | Interpretive | Fine as a contrast. The literature attributions are marked [M]. |
| T4 bundling | **Correct with fixes (rigor)** | Exact joint optimization (m3) confirms −1 for R1 under \|e\|^{0.5,1,2,4} (local slopes −1.018, −1.003, −1.000, −1.000 at ρ → 10⁻⁴) and −2 for A₁. The proof is a sketch (Issue 6). New observation: in A_θ (and R2), N\* is **exactly loss-independent**. m3 gives identical N\* for \|e\|¹ and e², because with deterministic variances everything reduces to the cost of reaching a total variance, K/V². This is a cleaner proof route for the Kalman technologies. |
| Cor 4.1 | Overstated "iff" | The "only if" direction holds only generically. |
| Cor 4.2 | Plausible; it's a modeling statement, not a theorem | |
| T5.1, T5.3, T5.4, T5.5 | **Correct** | T5.4 price invariance is exact at h = 0, including per-read broadcast, because N\*/r(N\*) = (B/A)^{1/(1−a)} whatever r depends on. |
| T5.2 | **Correct as "uniformly in (ρ, h, r)", wrong as a pointwise iff** | With a < b, V(N\*) > 1 is possible: a = ⅓, b = ⅔, ρ = 0.01, h′ = 100 gives V = 1.14 (m4). |
| T5.6 "V ≥ 2 for every upkeep and price" | **Wrong as stated outside ρ → 0; the closed form is only first-order** | See Issues 1–2 and counterexamples C1 and C3. The exact closed form is in §4. |
| T6 (a)–(c) | **Correct** | Textbook: concave∘modular is submodular, plus Topkis. m4: 0 violations of submodularity, lattice and Topkis-in-h over 300 random models with lookup caps. The (b) left-derivative inequality is right. |
| T6 (d) | Correct under its hypothesis | That hypothesis (a common degree a) excludes the mixed technologies that T1.8 promotes. With a level degree of a + 0.3, I found 167 accretion failures (m4). State this. |
| T7 (a) | **Correct** | The mean-of-ψ′ exchange argument is valid and neat. m4: 0 non-upper sets in 84 predicted-upper cases, 0 non-lower in 131. |
| T7 (b) | Correct with fix | "κ = 0.7 builds bottom-up with averaging sensing" holds only at h = 0. With h > 0, κ\* = ½ < 0.7 < 1, which falls in the gap where T7(a) says nothing. |
| T7 (c) | **Overstated "iff"** | It assumes members share the level's b, which (a) says isn't needed, so the extra assumption should be stated. With R evaluated at R(∅) it's only sufficient: 25/113 mismatches (m4), and the paper's own P7.1 is a counterexample. With R = R(L\*) it's a self-consistency condition that matched 113/113 in my small-share tests, but it can admit several self-consistent sets when shares aren't small (concavity gap between ψ′(q_u)q_s and Δψ). Calling it "T6(b)'s rule" is wrong, since T6(b) is sufficient only. |
| P7.1 | Numerical, labeled as such | Plausible (complementarity). Prior art: Milgrom & Roberts (1990) on complementarity-driven jumps. |
| T8 1–6 | **Correct** | m4 sympy reproduces every edge, the factorization, N² and 1/b. Wording: "holding any drifting item pays only if…" refers to the *interior* band. Freezing (the corner) can still beat lookup. Whether a frozen item pays h is not specified. |
| T8 Poisson | Not re-derived (carried over) | |
| P9 | Correct | This is the classic joint-replenishment bound. |
| P10 | Correct | Bernoulli bound checked. 0.0203 and 0.108 are correct. |
| P11 | Numerical, plausible | My Monte Carlo (m6) confirms the shared term → T_g as T_g/T_u → 0 (0.0100 at ratio 0.01) and is 0.667·T_u at T_g = T_u. Costs are no longer separable here, so "Π\* → 8" needs the joint optimization, which they say they did. |

---

## 3. Issues, ranked by severity

**Issue 1 (high). T5.6 "V ≥ 2 for every upkeep and price" is a leading-order statement, and at h = 0 the inequality goes the other way.** (THEOREMS.md T5 item 6; the summary table row T5 says "2 at γ = ½".)
- Exact result at a = b = ½, equal prices and h = 0: N\* = (√(1+ρ)+1)²/ρ, so **V(N\*) = 1 + (1+ρ)^{−1/2} ∈ (1, 2)**. Values: 1.995 (ρ = 0.01), 1.953 (0.1), 1.817 (0.5), 1.707 (1), 1.30 (10) (m2).
- Random draws with ρ ∈ [10⁻³, 10], h′ ∈ [10⁻⁴, 10] and r ∈ [0.1, 10]: V(N\*) < 2 in **10,792/20,000** (m2).
- Their own check s11 only sampled ρ ∈ [10⁻⁷, 10⁻⁵], so it couldn't see this.
- From the exact closed form (§4), **V ≥ 2 requires h′/r ≳ ρ/2**: h′/r ≥ 0.005, 0.050, 0.485 and 3.56 at ρ = 0.01, 0.1, 1 and 10 (m5).
- The per-read broadcast case is the same: V(N\*) = 1.59 at t = 0.2, ρ = 1.5ρ_b (m2). T5.4's check used t = 10⁻³, where ρ is tiny.
- **Consequence:** "the theory proves the new level checks its driver at least twice as often as members, whatever the costs" is not a theorem. The correct statement: at h = 0, V(N\*) ∈ (1, 2) and tends to 2 as ρ → 0. Upkeep raises it, and V ≥ 2 iff h′/r exceeds the threshold in §4. This weakens, and partly removes, the stated tension with the field data (1.15 survey ratio). That data still doesn't match, but the theory's floor at finite shared share is 1, not 2.

**Issue 2 (high, interpretation). The "read-based class" isn't defined, and R1 as axiomatized gives V < 2 even as ρ → 0.** Axiom 3 defines R1 for fBm. At H, γ = 1/(1+2H) and V → γ^{−γ/(1−γ)}: 2.25 (H = ¼), 2 (H = ½), **1.842 (H = ¾), 1.772 (H = 0.9)** (m2). The "2" is specific to Brownian drift (or R2). T5.6 must say "R1 with H = ½, or R2".

**Issue 3 (high). T1.8's "opposite signs of T3 survive whenever b_m < 1 and b_L < 1" is false at large ρ when b_L > b_m.** With a level in P(a_L, b_L) and members in P(a_m, b_m), at h = 0, N\*^{1−a_L} ∝ q_g^{b_L}/((q_g+q_u)^{b_m} − q_u^{b_m}) ~ q_g^{b_L−b_m} as ρ → ∞. Counterexample C2 (m2): level (½, ½) over members (⅔, ⅓) gives e_g = −1.000, −0.616, **+0.159, +0.301** at ρ = 10⁻⁴, 1, 10², 10⁴. Level (0.4, 0.8) over members (½, ½) gives +0.417 at ρ = 10². The private-drift sign does survive at every ρ (G_{q_u} < 0 always). Any claim that "shared change always lowers the onset group size" must be restricted to a common technology (T3 as proved) or to small ρ.

**Issue 4 (medium). "Within 𝒜₁ every statement below is an exact 'iff'" (preamble to T1) is false.** T1.3, T1.5, T5.3, T5.6, T4 and T7(c) are asymptotic or first-order, and T5.2, T7(c) and Cor 4.1 aren't iffs pointwise. Specifically:
- T5.2 "born more vigilant iff a ≥ b" holds only as "V(N\*) > 1 for all (ρ, h, r) iff a ≥ b". Counterexample: a < b with V = 1.14 (m4).
- T7(c) "kept iff": see the verdict table above.
- Cor 4.1: "iff" should be "if, and generically only if".

**Issue 5 (medium). Upkeep normalization hides q_u-dependence.** h′ = h/(k p^{1−a} w^a q_u^b) depends on q_u. With h > 0, therefore, e_u ≠ −e_g, and statements like "N\* depends on (q_g, q_u) only through ρ" (used in T1.3 for e_u) hold only at h = 0. T1 is careful about this, but T5.6's "V(N\*) = 1 + √(1 + 2h′/r)" quietly makes V depend on q_u. If T5.6 is ever used for field predictions, state this explicitly.

**Issue 6 (medium, rigor). T4's proof is a sketch.**
- "+ o(q_g)" is the wrong bookkeeping. The level term φ₂(Nwκ_ℓ, q_g)/N is O(q_g^{b₂}) ≫ O(q_g). The real small parameter is ρ at fixed Nρ: the relative remainder is O(ρ^{p/2}) at the onset scale, where V_g ~ ρV_u.
- The step "the private tracker's re-optimization is second order" and the passage from the linearized level problem to the exact optimum (an envelope/Γ-convergence argument) are asserted, not proved.
- The remainder estimate for 0 < p < 2 is the right idea but is done on a time-varying V_g as if it were constant.
- The conclusion is nonetheless right: my independent exact optimization (m3) gives −1.0322 → −1.0176 for p = ½, the same slow O(ρ^{p/2}) convergence they report.
- Suggested fix: write the theorem as lim_{ρ→0} d ln N\*/d ln ρ = −(1−b₂)/(1−a₂) and prove it with explicit two-sided bounds. For the Kalman technologies (R2, A_θ), use the exact loss-independence argument in §2.

**Issue 7 (medium, novelty and attribution).** See §5. As written, the "NEW" labels on T1's closed form, T5 and T6 will not survive a referee familiar with inventory pooling, EOQ and lattice programming.

**Issue 8 (low). Edge cases allowed by the hypotheses.**
- a = 0 in T1.1 and T1.7.
- The N ≥ 1 boundary in T3 when p_g < p.
- Integer N throughout: N\* is treated as continuous, which is fine for the exponents but means "iff N > N\*" should be read on the reals.

**Issue 9 (low). T7(b) at h > 0.** The class-dependence example (κ = 0.7, averaging, bottom-up) falls in the gap κ\* < κ < 1, where T7(a) is silent.

**Issue 10 (low). V's comparator.** V divides the level's effort by a *flat* member's effort, a member in a different architecture. It doesn't compare the lead with its own members in the levelled organization. Those members track only u_i at a rate ∝ q_u^b, and they don't sample g at all. Field tests that compare supervisors with the people they supervise measure something else unless ρ is small. This should be flagged in T5's "field tests" paragraph.

---

## 4. My counterexamples and new exact results

- **C1 (T5.6).** a = b = ½, h = 0, equal prices, ρ = 1: N\* = 5.828 and V(N\*) = 1.707 < 2.
- **Exact finite-ρ formula** (m5; verified symbolically and against root-finding to 3×10⁻¹⁰ over 20,000 draws):
  **V(N\*) = ½·(1 + (1+ρ)^{−1/2})·(1 + √(1 + 4h′(√(1+ρ) − 1)/(rρ))).**
  It reduces to T5.6 as ρ → 0 and to 1 + (1+ρ)^{−1/2} at h′ = 0.
- **C2 (T1.8).** Level (½, ½), members (⅔, ⅓), h = 0: ∂ln N\*/∂ln q_g = +0.159 at ρ = 100.
- **C3 (T5.6 "read-based").** R1 with fBm H = ¾: lim V(N\*) = 0.4^{−2/3} = 1.842.
- **C4 (T5.2 pointwise iff).** a = ⅓, b = ⅔, ρ = 0.01, h′ = 100: V(N\*) = 1.142 > 1 with a < b.
- **C5 (T6(d) with mixed degrees).** Level degree a + 0.3 versus member degree a: the largest optimal set *shrinks* as stakes rise in 167 of the step comparisons over 300 random models (m4).
- **C6 (T7(c) with R(∅)).** 25/113 random h = 0 trees where the first-order rule disagrees with the exact optimum.
- **Failed attempts (evidence for correctness).**
  - T3 for a common technology: 0/3,191 violations.
  - T6: 0 violations of submodularity, lattice or Topkis.
  - T7(a): 0/215 violations of the upper/lower-set ordering.
  - T4: tried p = 0.5, 1, 2 and 4 for R1, and A₁; all converge to the predicted exponent.
  - T1.5: all four (a, b) regimes match.

---

## 5. Novelty (where the prior art is obvious)

- **L1 (i)–(iii) and T8 1–2:** EOQ (Harris 1913) and its square-root form. The hold-versus-lookup break-even is the logic of Gray & Putzolu's (1987) "five-minute rule". Freshness/refresh is Cho & Garcia-Molina (cited).
- **T1, T5:** Pooling a concave-cost activity across N users is the inventory-centralization / risk-pooling literature: the square-root law (Maister 1976), Eppen (1979), and Wilson (1975) on informational economies of scale (cited). At γ = ½, "V = level effort / member effort ∝ N^{1/2}" is the statement that a centralized EOQ orders √N times as often. The general-(a, b) closed form is a one-line extension. "NEW as far as we know" should become "elementary extension of known pooling results".
- **T6:** Concave∘modular submodularity and Topkis monotone comparative statics are textbook (Topkis 1998 book; Milgrom & Shannon 1994). "Complementarity ⇒ jumps/avalanches" (P7.1) is Milgrom & Roberts (1990, AER; 1995). Cite these. The lookup-dissolves-levels counterexample is a nice touch but not deep.
- **P9:** This is the joint-replenishment problem; Roundy (1985) power-of-two policies is the right citation (they mark it as unverified).
- **T7(a):** A standard exchange argument. The κ\* = 1/|e_g| framing is a reasonable contribution of presentation.
- **T4:** The cleanest genuinely interesting result: for Gaussian bundled losses, the shared-error cost is variance-linear to first order, so the technology sets the exponent. The Gaussian-closure-plus-linearization idea is standard, but I don't know this application.
- **T3 signed at all ρ:** Elementary IFT. The sign itself is the old "centralize common, decentralize local" (Hayek; Alonso, Dessein & Matouschek 2008).

---

## 6. After writing §1–§5: comparison with FIXES.md and CLAIM_MAP.md

I opened FIXES.md and CLAIM_MAP.md only after §1–§5 were written.

- **The adversarial pass and I independently agree on the following:** the T7 swap argument, T4's O(ρ^{p/2}) remainder rate, T6(H1) bundling, T1.9/F17, F19, F20 and F22's circularity labels. I find their §C "checked hard" list correct.
- **F15 is wrong as an inference, and it propagates to CLAIM_MAP T5.** F15 says "VIGIL's ≈ 1.15 cannot come from upkeep or prices in class R". That holds only as ρ → 0. At h = 0 the exact V(N\*) = 1 + (1+ρ)^{−1/2} equals 1.15 at ρ ≈ 43. That is a large shared share, maybe implausible for the VIGIL setting, but it is a channel the pass wrongly excluded. More importantly, CLAIM_MAP T5's "≥ 2 for every upkeep and price in R" is false at finite ρ (Issue 1). It should read "→ 2 as ρ → 0 at h = 0; ≥ 2 iff h′/r exceeds the §4 threshold (≈ ρ/2 for small ρ)". The "size ≈ 2 missed" verdict should then be restated as a miss against the small-ρ value, not against a floor.
- **F12 is incomplete.** "The opposite signs of T3 survive" under mixed classes holds only for small ρ (or b_L ≤ b_m). See C2. CLAIM_MAP T1 ("mixed classes (level's class sets e_g)") is fine as written, but any downstream sentence saying "shared change always lowers the onset size" needs the common-class or small-ρ qualifier.
- **F16 overstates the result:** "V > 1 iff a ≥ b" holds only uniformly over (ρ, h, r), not pointwise. See C4.
- **CLAIM_MAP T7 "top-down iff κ < κ\*"** is correct at h = 0. At h > 0 the gap κ\* < κ < 1 (or 1 < κ < κ\*) is undetermined. CLAIM_MAP omits the h qualifier that THEOREMS T7(a) has.
- **D4 / T7(c):** The explicit constant is right, but the rule is still mislabeled "iff". See the T7(c) verdict.
- **CLAIM_MAP N2 "upgraded: an exact iff within 𝒜₁"** is fine for T1.2 itself (h = 0, equal prices, a common technology).
- **Nothing in FIXES addresses** Issue 2 (R1 with fBm gives V < 2), Issue 5 (h′ depends on q_u), Issue 10 (V's flat comparator versus supervisor/supervisee field measures), or the prior art in §5.

**Bottom line for the claim map.** T1–T3 (common technology), T4, T6, T7(a) and T8 can stay **PROVED**, with the wording fixes listed. Mark T5.6 / "V ≥ 2" **WRONG as stated**, replaced by the exact formula in §4. Restrict T1.8's sign claim to small ρ. Downgrade the "NEW" labels per §5.
