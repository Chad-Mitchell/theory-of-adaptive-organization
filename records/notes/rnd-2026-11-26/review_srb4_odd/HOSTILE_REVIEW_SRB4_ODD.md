# Hostile review of the odd analogue of SR-b4 (finding M2 of `rnd/review_srb4/HOSTILE_REVIEW_SRB4.md`; SR_B.md §10.2)

*26 Nov 2026, about 11:40 ET. Independent reviewer. Local note only (not committed or pushed). SR_B.md, THEORY.md and CORE.md were not edited. Read: SR_B.md §§1–10 (§8.3 disk optimum, §9 SR-b4, §10.2 the claim), `sr_b4/`, the M2 text and `rv_odd_lemma.py/.out`, and ROUND10's `m_round10b.py` (M3c) and `m_round10b_poly.py` (M3h) at fork head a57f1f7 (`/workspace/srbrev-clone`). Reviewer code is my own; it imports nothing from `sr_b/`, `sr_b4/` or `review_srb4/`. Labels: **PIM** = proved in-model; **OBSERVED** = numerical output; **HYP** = hypothesis; **ELEMENTARY**; **KNOWN**.*

## Result: **PASS-WITH-FIXES**

- **No H findings.** The claim is correct. I wrote the proof out in full (§2) and found no gap. Every step holds separately at 80 digits on the checked families. My own exact distances, a DP with no step cap and brute force agree with it at every checked (n, T).
- **2 M findings, 5 L findings.** Both M findings are about scope and wording, not about the mathematics:
  - M1: "the antipode rule" is undefined for odd n. "Both rules" needs an explicit reading of it.
  - M2: the pure-state jump rule carries the whole comparison. It is stated in SR_B §1, so it is not hidden, but every "both rules" sentence should carry it.
- **If the fixes are applied, these can be upgraded to PIM (ELEMENTARY) under both target rules:** the claim, the (2T+1)-gon corollary, the odd lcm family, the (P) open miss for every H ≥ 2, and "SR-b2 for bounded support with p(T ≥ 2) > 0: the disk is strictly beaten by some polygon".

## 1. Which target rule odd polygons use, and is the disk comparison right?

- **Odd polygons (any-vertex rule, M3h).** The d = 1 vertices from v₀ are exactly {v_{S′}, v_{S′+1}}, with S′ = (n−1)/2.
  - Proof. d(a,b) = 1 iff a and b are support points of K in opposite directions (§2, step 1). v₀ is a support point only for directions within π/n of 0. For odd n, the opposite direction then lies within π/n of π, where the minimizer is v_{S′} or v_{S′+1}, or both only at direction exactly 0.
  - OBSERVED: exactly this set for every odd n = 3…61 (`od_checks.out` (1)).
  - The two targets are mirror images under the reflection that fixes v₀, so they cost the same.
- **Odd polygons ("antipode" rule, M3c).** ROUND10's M3c code scores `best[n//2]`, and was only ever run on even n. For odd n, n//2 = S′, a d = 1 vertex. "The vertex farthest from v₀" gives the same pair.
  - The literal antipode −v₀ is the midpoint of the edge (v_{S′}, v_{S′+1}). That is a mixed state, so under the pure-jump rule it is not an admissible target.
  - So both readings that make sense give the same cost, and the literal reading is empty. That is finding M1.
  - OBSERVED: DP to {S′, S′+1} equals DP to {S′} to 50 digits at every checked (n, T) (`od_checks.out` (3), `od_lcm.out`).
- **Disk.** Its width is 2 in every direction, so d = sin(φ/2), and the only pure state at d = 1 is the antipode. So the disk's target is the same under both rules.
  - J(disk, T) = T·sin²(π/2T) is the optimum, not just the cost of one path. That is SR_B §8.3 (PIM). I re-derived it independently (Jensen on [0, π/2], plus monotonicity of the one-large-step family). It is also OBSERVED: no tested split goes below it, T = 2…60, to 5e−51 (`od_checks.out` (2)).
  - So T·sin²(π/2T) is the right comparison under each rule.
- **No rule mixing in the claim.** It is a pointwise comparison of odd polygons against the disk. Both sides are rule-independent, and no even polygon or J* enters.
  - J* depends on the rule, but it only enters R_H through the positive weights w(T) = 1/(T·J*(T)). Pointwise dominance on [2, H], strict somewhere, fixes the sign for every positive weight (SR_B §9 corollary).
  - So the (P) corollary holds under either rule, and under the mixed convention (even polygons at the antipode, odd polygons at a d = 1 vertex).

## 2. Full paper proof (PIM, ELEMENTARY)

**Claim.** n odd, n ≥ 5, S′ = (n−1)/2, and T ≥ 2 with T | S′. Then J(n, T) < T·sin²(π/2T) = J(disk, T).

The model is the regular n-gon K inscribed in the unit circle, with all effects. Each tick jumps to a vertex, and staying put is allowed. The cost is Σ d_t² over exactly T ticks.

1. **The distance formula.** An effect is e(x) = c + ⟨t, x⟩ with 0 ≤ e ≤ 1 on K. For a given t, a constant c exists iff |t|·w(t̂) ≤ 1, where w(θ) = max_K⟨θ,·⟩ − min_K⟨θ,·⟩ is the width.
   - So d(a, b) = max over unit θ of ⟨θ, a−b⟩/w(θ).
   - Equality d = 1 means a and b are extreme in opposite directions.
   - Equivalently, d is the gauge of a − b in the difference body K − K.
2. **Minimum width.** For odd n, the direction θ+π is offset from its nearest vertex direction by π/n − α when θ is offset by α. So w = cos α + cos(π/n − α) for α ∈ [0, π/n].
   - This is concave in α, so it is smallest at the endpoints: w_min = 1 + cos(π/n) = 2cos²(π/2n).
3. **Upper bound on one jump.** ⟨θ, a−b⟩ ≤ |a−b| and w ≥ w_min. With |v₀ − v_j| = 2sin(πj/n), this gives d(v₀, v_j) ≤ sin(πj/n)/cos²(π/2n).
4. **Target.** Take the direction θ = (1, 0). v₀ attains max ⟨θ,·⟩ = 1, and the edge (v_{S′}, v_{S′+1}) attains min = −cos(π/n). So ⟨θ, v₀ − v_{S′}⟩ = w(θ), and d(v₀, v_{S′}) = 1.
5. **Path.** Let j = S′/T. The path v₀ → v_j → v_{2j} → … → v_{S′} has T jumps. Rotation by 2πij/n is a symmetry of K, so each jump costs d(v₀, v_j)². Hence J(n, T) ≤ T·d(v₀, v_j)².
6. **Inequality.** Let x = π/(2T) ∈ (0, π/4] and y = πj/n = x(1 − 1/n).
   - It suffices that sin y < sin x·cos²(π/2n) = sin x − sin x·sin²(π/2n).
   - sin is strictly concave on [0, π], so sin(x − x/n) < sin x − (x/n)cos x.
   - So it suffices that sin²(π/2n) ≤ (x/n)·cot x.
   - The right side: x cot x decreases on (0, π/2), so x cot x ≥ (π/4)·cot(π/4) = π/4, and the right side is ≥ π/(4n).
   - The left side is < π²/(4n²).
   - π²/(4n²) ≤ π/(4n) ⇔ n ≥ π, which holds for n ≥ 5. ∎
7. **Corollaries.** T = S′ gives the (2T+1)-gon at every T ≥ 2. n = 1 + 2m·lcm(1..H) is odd, n ≥ 5, and S′ = m·lcm(1..H) is divisible by every T ≤ H. At T = 1 every design costs exactly 1, a tie.

The M2 text is correct as written, steps included. Two remarks:
- Its "n > π suffices" is right. The strictness comes from the concavity step.
- Its bound is loose. It gives n·(relative margin) ≥ 0.777 for the (2T+1)-gon, while the exact path gives ≥ 1.18 (`od_chain.out`). That is harmless.

## 3. Independent numerics (my code: `od_core.py`, `od_checks.py`, `od_lcm.py`, `od_chain.py`)

- **Distances.** The gauge in K − K is computed over the ± normals of all 2n edges, with each width computed directly as max − min over the vertices, at 50 digits. It agrees with a float LP over affine effects to 1.7e−15 for n = 3…61 and all k (`od_checks.out` (1)).
- **DP.** Exactly T ticks, any vertex to any vertex, with no step cap or direction restriction. Run at 50 digits, under both target readings.
  - Odd n = 5…61, every T ≥ 2 dividing S′: 81 (n, T) pairs, 0 failures. J under the any-vertex rule = J at the antipode index to 1e−40.
  - min n·(relative margin) = 1.18 (n = 5) (`od_checks.out` (3)).
  - OBSERVED: at every checked pair the DP optimum equals the equal-step path.
- **Brute force** over all vertex sequences, n = 5, 7, 9, 11, 13, T ≤ 4–5: 23 cases, 0 mismatches with the DP (`od_checks.out` (4)).
- **lcm family, H = 2…8, m = 1, 2, 3** (n up to 5041). The 60-digit explicit path, with directly computed widths, is cheaper than the disk at every T ∈ [2, H].
  - The float DP (n ≤ 3361, both rules, no cap) agrees: it wins at every T, its optimum equals the equal-step path, and J(1) = 1.
  - OBSERVED: n·(min relative margin) rises toward ≈ 1.570 (π/2 ≈ 1.5708). The even family's value is π. So odd polygons win by about half the even margin (`od_lcm.out`).
- **Proof chain at 80 digits**, each step separately: the (2T+1)-gon for T = 2…300, with exact distances for n ≤ 201, and the odd lcm family for H = 2…40, m = 1…3 (2,340 cases). 0 failures (`od_chain.out`).
- **Beyond the claim** (OBSERVED, `od_checks.out` (5)): odd n also wins at many T that do not divide S′, for example n = 61 at T = 2–11, 14–16, 29 and 30. It loses at some others, for example n = 61 at T = 12, 13 and 17–28. This is consistent with each polygon having its own horizon T₀(n), SR_B §10.5 L4.

## 4. Findings

### H
- None.

### M
- **M1. "Both rules" needs a stated reading of "antipode" for odd n.**
  - Odd polygons have no antipodal vertex. M3c's code was only run on even n, and `best[n//2]` would give v_{S′}.
  - The literal −v₀ is an edge midpoint, a mixed state, which the pure-jump rule makes inadmissible.
  - **Fix.** In SR_B and in the Friday note on ROUND10 §14, write: "for odd n the antipode rule is read as 'a vertex at d = 1 from v₀', namely v_{S′} or v_{S′+1}, the farthest vertices (the index `n//2` of M3c's code). The any-vertex rule gives the same set (§1). For the disk, both rules pick the antipode, the unique pure state at d = 1."
  - Without this sentence, "under both rules" is ambiguous for odd n.
- **M2. The pure-state jump rule carries the comparison; say so wherever "both rules" appears.**
  - If intermediate states may be mixed, the straight chord in T equal pieces costs exactly 1/T in every design, because d is a gauge and so homogeneous. With SR-b1(a), J ≥ 1/T, every design then ties at every T (PIM, ELEMENTARY; `od_chain.out`).
  - So the polygon-versus-disk ranking exists only under ROUND10 §14's pure-jump rule. That rule is a chosen input. It is stated in SR_B §1, so it is not hidden.
  - The quadratic price c·d² is the second chosen input: ROUND10 already notes that a linear price reverses the ranking. Others are all effects (no restriction) and a menu of regular polygons plus the disk.
  - **Fix.** Label the upgraded rows "PIM in the class of SR_B §1 (pure-state jumps, all effects, cost Σd²), under both target rules".

### L
- **L1.** For odd n, the any-vertex target set is exactly {S′, S′+1} (§1 proof). Add this sentence; it is what makes the odd case rule-independent.
- **L2.** The odd margin is about π/(2n), against π/n for the even family (OBSERVED, lcm family H ≤ 8 and n ≤ 61). The M2 bound proves ≥ about 0.78/n for the (2T+1)-gon. If a margin rate is quoted, quote these, not the even π/n.
- **L3.** The DP optimum equals the equal-step path at every divisor case checked. That is OBSERVED only; the claim needs just the upper bound.
- **L4.** The corollary for R_H is independent of J* and of the rule used for J*, by pointwise dominance (§1). Say this explicitly. It closes the M1-type rule-mixing worry of the earlier review for (P).
- **L5 (prior art, verified on Crossref this session, `od_crossref.out`).** None of these anticipates the claim; I found no prior statement of it. The search covered Crossref title queries only, and I did not read these papers in full.
  - **Regular polygon state spaces with all effects** (definitional source of the menu): Janotta, Gogolin, Barrett & Brunner 2011, *New J. Phys.* 13:063024, doi 10.1088/1367-2630/13/6/063024. Also Massar & Patra 2014, *Phys. Rev. A* 89:052124, doi 10.1103/PhysRevA.89.052124.
  - **Distinguishability distance in GPTs** (step 1 is the standard base-norm/gauge identity): Kimura, Nuida & Imai 2010, *Rep. Math. Phys.*, doi 10.1016/s0034-4877(10)00025-x. Disclosure: my first guessed DOI, 10.1016/S0034-4877(10)80044-8, does not resolve and must not be used. Also Lami, Palazuelos & Winter 2018, *Commun. Math. Phys.*, doi 10.1007/s00220-018-3154-4.
  - **Analogy for the disk branch:** Aharonov & Vardi 1980, *Phys. Rev. D* 21:2235, doi 10.1103/PhysRevD.21.2235 (dragging a state with a sequence of measurements, Zeno-type). T·sin²(π/2T) has the form of a sum of per-step disturbances there. This is the reviewer's reading only, an analogy and not a citation for the claim.

## 5. Labels (reviewer's view, conditional on the M1 and M2 fixes)

| claim | label |
|---|---|
| Odd analogue: n odd ≥ 5, T ≥ 2, T \| (n−1)/2 ⇒ J(n,T) < T·sin²(π/2T) | **PIM (ELEMENTARY)**, both target rules (M1 reading), class of SR_B §1 (M2) |
| (2T+1)-gon beats the disk at every T ≥ 2; n = 1 + 2m·lcm(1..H) beats it at every T ∈ [2, H] | PIM (corollary) |
| (P) open miss at every H ≥ 2, any J* | PIM, both rules and the mixed convention |
| SR-b2 for bounded support with p(T ≥ 2) > 0: the disk is strictly beaten by some polygon | PIM, both rules |
| ROUND10 §14 HYP "J does not select the disk at every finite horizon" | PIM under both rules via the (2T+1)-gon. Flag for Ace's Friday note; ROUND10 not edited |
| With mixed intermediate states every design ties at 1/T | PIM (ELEMENTARY) |
| Odd margin ≈ π/(2n); DP optimum = equal-step path; odd wins at some non-divisor T | OBSERVED |
| SR-b2 for unbounded support | HYP (unchanged) |
| "No built-in timescale selects the disk" | **open miss** (unchanged) |

## Files (`rnd/review_srb4_odd/`)

| file | content |
|---|---|
| `od_core.py` | gauge distances (direct widths), LP distances, exact DP (no cap), numpy DP, brute force |
| `od_checks.py/.out` | target sets, disk optimum check, odd n ≤ 61 DP under both rules, brute force, non-divisor T |
| `od_lcm.py/.out` | odd lcm family H = 2…8, m = 1…3: 60-digit path and float DP |
| `od_chain.py/.out` | each proof step at 80 digits; the chord remark |
| `od_crossref.py/.out` | prior-art DOIs on Crossref |
