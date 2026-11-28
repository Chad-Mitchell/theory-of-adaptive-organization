# Hostile review of SR_B.md §9 (SR-b4: a scale-free, log-uniform horizon weighting) and `rnd/stepback/sr_b4/`

*26 Nov 2026, about 11:35 ET. Independent reviewer. Local note only (not committed or pushed). SR_B.md, THEORY.md and CORE.md were not edited. Context read: SR_B.md §§0–8, `rnd/review_srb/HOSTILE_REVIEW_SRB.md`, every script and output in `sr_b4/`. Reviewer code is my own (it does not import `sr_b/` or `sr_b4/`): `rv_*.py`, `rv_dp.c`, outputs `rv_*.out`. Labels: **PIM** = proved in-model; **OBSERVED** = numerical output; **HYP** = hypothesis; **ELEMENTARY**; **KNOWN**.*

## Result: **PASS-WITH-FIXES**

- **No H findings.** Proposition SR-b4 is correct. I re-derived it by hand, and it holds at every (n, T) I checked with my own distances and DP. The (P) open miss and the (F) restatement are correct as stated. Every number in the §9.3 table reproduces to 10 digits with independent code.
- **4 M findings, 6 L findings** (below).
  - The most important one is M1, a hidden second target rule of the ROUND10 kind in the odd-only computation. It does not change any sign.
  - The most useful one is M2: the M3h-only scope is unnecessary. An odd analogue of SR-b4 (reviewer's, PIM-candidate) makes the (P) open miss and "SR-b2 for bounded support" hold under **both** target rules.

## What was checked, claim by claim

### (1) Proposition SR-b4 — re-derived by hand: correct (PIM, ELEMENTARY, M3h's rule)

- **Target.** For even n with S = n/2, d(v₀, v_{S−1}) = sin(π(S−1)/n)/cos(π/n) = cos(π/n)/cos(π/n) = 1, because k − S = −1 is odd. My breakpoint distances (below) give the target set {S−1, S, S+1} for every even n tested (`rv_check_dist.out`).
- **Path.** Let k = (S−1)/T. By dihedral symmetry each of the T jumps costs d(v₀, v_k)². Write x = π/(2T). Then πk/n = x(1 − 2/n) = y, and d(v₀, v_k) ≤ sin y / cos(π/n).
- **Concavity.** sin lies below its tangent on [0, π], so sin(x − 2x/n) ≤ sin x − (2x/n) cos x. It suffices that (1 − cos(π/n)) sin x < (2x/n) cos x, i.e. 1 − cos(π/n) < (2/n)·x cot x.
  - 1 − cos z ≤ z²/2.
  - x cot x is decreasing on (0, π/2), and x ≤ π/4 for T ≥ 2, so the right side is ≥ π/(2n).
  - π²/(2n²) < π/(2n) ⇔ n > π. ∎
- **T = 1** is a tie for every design, since any design must make one d = 1 jump.
- **The lcm family:** S − 1 = m·lcm(1..H) is divisible by every T ≤ H.
- **Independent checks** (all mine):
  - **Distances.** `rv_core.dist_row` uses d = max over θ ∈ {± edge normals} of ⟨u − w, θ⟩/width_θ. Between breakpoints of the width function the ratio is a quotient of two fixed sinusoids, which is monotone, so the maximum sits at a breakpoint. This agrees with an LP over affine effects to 1.1e−15 for n = 3…40, and with §8.6's even closed form to 5.6e−16 (`rv_check_dist.out`).
  - **DP.** The full circular DP (any vertex, no cap, no direction restriction) agrees with my forward DP to 1e−15 for n = 3…60, T ≤ 30. Both agree with brute-force enumeration for n = 6, 7, 8, 10, 13, 14, 26 at T ≤ 3.
  - **lcm family, DP** (`rv_dp.c`, breakpoint distances, no per-tick cap; their `dp4` uses the closed form and a cap): H = 2…9, m = 1, 2 (n up to 5042). Cheaper than the disk at every T ∈ [2, H]. n·(min relative margin) → 3.1416 (`rv_lcm.out` (a)).
  - **lcm family, 60 digits:** the explicit path **and each inequality in the proof chain separately**, for H = 2…60 and m = 1, 2, 3 (n up to ≈ 6·10²⁵). Zero failures (`rv_lcm.out` (b, c)).
    - Disclosure: my first run reported failures. Both were reviewer-side precision artifacts: an exact `>=` on a step that is an equality in the odd-parity case, and cancellation in 1 − cos(π/n) at n ~ 10²⁵. With a 1e−50 tolerance and 2 sin²(π/2n), there are 0 failures. Their proof is not affected.

### (2) (P) is an open miss at every H, for any J*; SR-b2 for bounded support — correct, with caveat L3

- The corollary is pointwise dominance. Σ w(T)[J(n_H, T) − J(disk, T)] < 0 for every w ≥ 0 that is positive somewhere in T ≥ 2. So any J* > 0 works, including the true infimum over the infinite menu, since J* ≥ 1/T.
- **Independent table.** I computed J(n, T) for T ≤ 400, every n = 3…1000 and spot n near the claimed H = 200, 300 and 400 winners (`rv_RH_large.out`).
  - All 17 rows of §9.3 reproduce to 10 digits: R_H(disk), best n, R_H(best), margin.
  - All robustness signs are "++++".
  - Each claimed winner (1122, 2306, 3842) is a local minimum among its computed neighbours.
  - argmin n of J*(T) = 2T + 2 at the listed T.
- **H = 2…8 independently** (`rv_RH_small.out`):
  - J*(1…8) = 1, ½, ½, 0.381966, 0.358984, 0.297093, 0.276963, 0.241230.
  - Best n = 6, 6, 6, 6, 6, 6, 14 for H = 2…8.
  - R_2(disk) = 4/3 by hand.
  - At every H ≤ 8 most n ≤ 600 dominate the disk on [2, H].

### (3) (F) is a restatement of SR-b1(e) — correct

- R_H(n) ≥ (1/L_H)·Σ_{T≤H} (4/π²) d_min(n) = (4/π²) d_min(n)·H/L_H → ∞. This uses §8.2's corrected constant.
- R_H(disk) ≤ π²/4 by SR-b1(a) and (c).
- The shape of the log-uniform weight plays no role: any weighting with divergent mass gives the same result. "Restatement" is the right label. Strictly, it uses (d) for the disk as well as (e).

### (4) The order-of-limits reading (§9.5) — agreed, with two refinements (M4, L4)

- **The reading is right.** (P) and (F) give opposite answers, and the improper prior does not choose between them.
- **M4: there is standard vocabulary for (F)** (prior art below).
  - The per-H Bayes selections n(H) have R_H(n(H)) ≥ 1, and R_H(disk) → 1 (L2). So R_H(disk) − min_D R_H(D) → 0.
  - The disk is therefore the unique **fixed** design that is ε-Bayes ("extended Bayes") along the truncated log-uniform family. Every fixed polygon has R_H → ∞.
  - That is (F) in decision-theory language, and it confirms §9.5: it is a property of the design-first quantifier order, not of the prior.
- **L4: "no built-in timescale" is a property of designs, not of this prior.**
  - The model has a built-in unit, the tick. Only the upper cut-off is sent to ∞.
  - Each polygon carries its own timescale T₀(n), beyond which it stops beating the disk (OBSERVED: ≈ 2.0–2.1·√n for even n, ≈ 1.44·√n for odd n). The disk alone has none.
  - So in this menu, the stake "no built-in timescale" is satisfied by the disk as a **design** property: bounded ρ uniformly in T, which is the competitive requirement U. It is not supplied by putting a scale-free prior on horizons. This sharpens §9.5's conclusion; it does not change it.

### (5) Observed figures

- **T₀ ≈ 2√n — reproduced.** n = 1000, 1002, 2000, 2002, 4000, 4002, 10000, 10002 give T₀/√n = 2.055, 2.053, 2.080, 2.079, 2.024, 2.023, 2.030, 2.030 (`rv_t0.out`), inside their 1.995–2.161 band.
- **Best n ≈ 0.2·H²/ln H — wrong form** (L1). Their own data give n*·ln n*/H² ≈ 0.16–0.21. The formula needs ln n*, not ln H. With ln H the coefficient is 0.167, 0.149, 0.144 at H = 100, 200, 400.
- **Margin ∝ ln H/H² — consistent.** margin·H²/ln H = 14.7, 13.6, 13.6, 13.2 at H = 50, 100, 200, 400.
- **R_H(disk) → 1 — provable** (L2, sketch below). It is not only OBSERVED.
- **Odd-only "OPEN at H ≥ 150" — superseded.**
  - With odd n up to 999 plus 1121, 2305 and 3841, an odd polygon beats the disk at H = 100, 150, 200 and 300. This holds under all five weights: M3h J*, mixed-rule J*, 1/(T·disk), 1/T and 1 (`rv_odd_robust.out`). These are existence results; at H = 150–300 the best odd n is at a sampled spot point, so "interior" is not claimed.
  - At H = 400 no odd n in my sample wins.
  - M2 makes the question moot for every H, pending its review.

### (6) Pre-statement integrity of §9.0 — hash reproduces; ordering not verifiable (M3)

- **The hash reproduces.** SHA-256 of SR_B.md lines 1–265 (all of §§0–8, with trailing newline) = `061c1d54b1a4133a5c61a9b1e2124f6cd1a7601340f8f09552398856e212a16c`, matching `061c1d54…a16c`. So §§0–8 were not changed after the hash was taken.
- **But the hash commits to the wrong bytes.** It covers the text *before* §9.0, not §9.0 itself. Nothing on the box fixes §9.0's wording before the first number.
- **File times** (ET, from `ls --full-time`):
  - `sr_b4/dp4.c` 11:04:24, the earliest SR-b4 file.
  - The first numerical output, `lcm_check.out`, 11:05:01.
  - SR_B.md last written 11:18:56, after every output. That is expected, since §§9.1–9.8 came later, but it erases any trace of when §9.0 was written.
  - The WORKLOG line for SR-b4 is at 11:19, after the results.
  - No backup copy of §9.0 exists. The executor transcript is not readable from this review.
- **No sign of post-hoc editing.** §9.0 contains no numbers, and its prediction (the lcm argument, p ≈ 0.8) is what a pre-computation paper argument would say.
- **Impact is low here,** because the (P) outcome is now a proof and does not rest on the pre-statement. The process fix matters for future preregs.

### (7) Prior-art DOIs — all seven verified on Crossref (`rv_crossref.out`)

- **All seven resolve, with matching title, authors, venue, year, volume and pages:**
  - Jeffreys 1946, 10.1098/rspa.1946.0056
  - Jaynes 1968, 10.1109/TSSC.1968.300117
  - Gott 1993, 10.1038/363315a0
  - Dawid–Stone–Zidek 1973, 10.1111/j.2517-6161.1973.tb00952.x
  - Kass–Wasserman 1996, 10.1080/01621459.1996.10477003
  - Zilberstein–Russell 1996, 10.1016/0004-3702(94)00074-3
  - Zilberstein–Charpillet–Chassaing 2003, 10.1023/A:1024412831598
- The AI Magazine DOI 10.1609/aimag.v17i3.1232 returns 404, as §9.6 says. It is correctly not cited.
- Missing prior art: M4.

## Findings

### H
- None.

### M

- **M1. Hidden second target rule in the odd-only computation** (ROUND10-type).
  - `sr_b4/odd_only.py` scores odd polygons only, whose target is rule-independent. But its J*, the denominator of ρ and so the weights of R_H, is the minimum over the **M3h even curves** (`curves_even.npy`, targets v_{S−1}, v_S) plus odd n.
  - Under the mixed convention, which is the reason for an odd-only run, even polygons have the antipode as their only target. J* is then larger at small T: T·J*(2) = 1.528 instead of 1.0 (`rv_RH_large.out`).
  - So the §9.3 odd-only R values are a hybrid of the two rules, and "Under the mixed target convention … (P) there is OBSERVED for H ≤ 100 only" was not computed under that convention.
  - Recomputed under the mixed-rule J*, every sign is unchanged for H ≤ 300, and the margins are ≈ 25% smaller.
  - **Fix:** say which J* was used, and add the mixed-rule rows, or use M2.
  - Nothing else in `sr_b4/` mixes rules: `dp4` and the `sr_b` odd curves are both M3h, and §9.3's main table is consistently M3h.

- **M2. The M3h-only scope is unnecessary. Odd analogue (reviewer's; PIM-candidate, needs its own hostile review before it counts).**
  - **Claim.** Let n be odd, n ≥ 5, S′ = (n−1)/2, and let T ≥ 2 divide S′. Then J(n, T) < T·sin²(π/2T).
  - **Proof.**
    - The target is v_{S′}. In the width direction normal to the edge (v_{S′}, v_{S′+1}), v₀ and that edge are the extreme points, so d(v₀, v_{S′}) = 1. That is the same under M3c's and M3h's rules.
    - Take T equal jumps of j = S′/T vertices.
    - d(v₀, v_j) ≤ |v₀ − v_j|/w_min with w_min = 1 + cos(π/n) (vertex to opposite edge). So d(v₀, v_j) ≤ sin(πj/n)/cos²(π/2n), with πj/n = x(1 − 1/n) and x = π/(2T).
    - By concavity, sin(x − x/n) ≤ sin x − (x/n) cos x. It suffices that sin²(π/2n) < (x/n) cot x. The left side is ≤ π²/(4n²) and the right side is ≥ π/(4n), so n > π suffices. ∎
  - **Corollaries:**
    - The (2T+1)-gon beats the disk at every T ≥ 2.
    - n = 1 + 2m·lcm(1..H) beats the disk at every T ∈ [2, H].
  - **Checks** (`rv_odd_lemma.out`):
    - Every proof step was checked with exact breakpoint distances (60 digits) for the (2T+1)-gon, T = 2…300, and the odd lcm family, H = 2…9 (distance check for n < 1000).
    - The bound-only chain holds for H = 2…60.
    - My DP on n = 1 + 2m·lcm(1..H), H = 2…9, m = 1, 2: cheaper than the disk at every T ∈ [2, H].
  - **If it passes review:**
    - The (P) open miss and "SR-b2 for bounded support" hold under **both** target rules.
    - §9.5's first weak point goes away.
    - ROUND10 §14's HYPOTHESIS "J does not select the disk at every finite horizon" becomes PIM under the mixed convention too, via the (2T+1)-gon. ROUND10 has those odd wins OBSERVED for T ≤ 20.
    - Flag this for Ace's Friday note next to §8.7. ROUND10 was not edited.

- **M3. The pre-statement integrity mechanism commits to the wrong bytes** (§(6) above).
  - The hash proves §§0–8 unchanged, not that §9.0 predates the numbers. No independent timestamp exists.
  - **Fix for future preregs:** before any computation, append a WORKLOG line with the time and the full SHA-256 of the **pre-statement block itself**. Better still, lock it to the fork as the process rule already requires for preregs.
  - Add to §9.0: "ordering not independently verifiable on the box."

- **M4. Missing prior art** (verified on Crossref this session: `rv_crossref2.out`; the two DOIs I guessed in `rv_crossref.py` for Caves and Stone resolve to *other* items and must not be used).
  - **Limits of Bayes rules / extended Bayes** (the KNOWN frame for (P) versus (F); see §(4)):
    - Blyth 1951, *Ann. Math. Stat.* 22:22–42, doi 10.1214/aoms/1177729690.
    - Heath & Sudderth 1978, *Ann. Stat.* 6:333–345, doi 10.1214/aos/1176344128, on finitely additive (improper) priors and extended admissibility.
  - **Improper-limit dependence:** Stone 1976, *JASA* 71:114–116, doi 10.1080/01621459.1976.10481490, "Strong inconsistency from uniform priors". It sits beside Dawid–Stone–Zidek.
  - **Gott's argument has a published critique:** Caves 2000, *Contemp. Phys.* 41:143–153, doi 10.1080/001075100181105. Cite it next to Gott 1993 if Gott stays.
  - **Contract scheduling:** López-Ortiz, Angelopoulos & Hamel 2014, *JAIR* 51:533–554, doi 10.1613/jair.4360, on optimal schedules and acceleration ratios. It is the modern reference for the interruptible-ratio template §9.6 cites from Zilberstein.
  - **Horizon uncertainty in online allocation:** Balseiro, Kroer & Kumar 2023, SIGMETRICS abstract, doi 10.1145/3578338.3593559 (arXiv 2206.13606).
    - KNOWN there: no algorithm has a constant competitive ratio without a bounded horizon window, and the ratio degrades with ln(τ₂/τ₁).
    - It is an analogy for "the uniform-ratio requirement needs the right design class". Only the abstract and arXiv text were read.

### L

- **L1.** "Best n ≈ 0.2·H²/ln H" should be **n* ≈ 0.2·H²/ln n*, about 0.14–0.17·H²/ln H** (OBSERVED, H = 100–400).
  - The n* sequence is irregular: 134 at H = 75, then 362 at H = 100. Call it a rough fit.
  - The 9.7 table row has the same issue.
- **L2. R_H(disk) → 1, and so (P)'s tie in the limit, is provable.** Reviewer's sketch, PIM-candidate:
  - Every polygon is inscribed in the unit circle, so width ≤ 2 and d(u, w) ≥ |u − w|/2 = sin(φ/2).
  - A d = 1 target needs |v₀ − v_k| ≥ w_min ≥ 1 + cos(π/n), so the angular gap Θ_n satisfies sin(Θ_n/2) ≥ 1 − π²/(4n²).
  - §8.3's convexity argument with π replaced by Θ ≤ π then gives J(n, T) ≥ T·sin²(Θ_n/2T). Case (ii) still works, since (Θ − φ₁)/(T−1) ≤ π − φ₁ ≤ π/2.
  - Also J(n, T) ≥ d_min ≥ sin(π/n) ≥ 2/n.
  - **Split the polygons by size.**
    - If n ≤ √T, then T·J ≥ 2√T.
    - If n > √T, then T·J ≥ T²·sin²(Θ(T)/2T) with sin(Θ(T)/2) ≥ 1 − π²/(4T).
  - Hence liminf T·J*(T) ≥ π²/4. With T·J* ≤ π²/4 this gives T·J*(T) → π²/4 and ρ(disk, T) → 1. A log-Cesàro average then gives R_H(disk) → 1, and 1 ≤ R_H(n(H)) < R_H(disk) gives the tie.
  - **Fix:** relabel the §9.7 row "R_H(disk) → 1" from OBSERVED to PIM-candidate (needs its own review).
- **L3. SR-b2 for bounded support needs p(T ≥ 2) > 0.**
  - A prior concentrated on T = 1 makes every design tie.
  - "Selects a polygon" should read "the disk is strictly beaten by some polygon". Attainment of the argmin over the infinite menu is not shown; it would follow from J(n, T) → J(disk, T) as n → ∞, for which L2 gives the lower half.
- **L4. §9.0's invariance parenthetical is unit relabeling only.**
  - The parenthetical says "a change of time unit T → cT leaves it and the measure dT/T unchanged". But the model has a tick, and J(D, cT) is not related to J(D, T) by any scaling.
  - **Fix:** say that the lower cut-off is the tick, and that a moving window, e.g. log-uniform on [H/K, H] or [H^a, H], gives the same (P) open miss by SR-b4. Any bounded window is dominated. See also §(4) on design-level scale-freeness.
- **L5.** "R_H(disk) − 1 falling like ~1.2/L_H" holds for H ≳ 50 (1.21 at H = 100, 1.22 at H = 400). At H = 2 the product is 0.5. Scope the phrase.
- **L6.** `lcm_check.py` prints 2/n as the comparison, while the text says "≈ π/n". The DP value is π/n (n·margin → 3.1416). The explicit equal-step path gives 2.8–3.14/n at small H. This is cosmetic.

## Labels (reviewer's view of §9.7)

| claim | label |
|---|---|
| Prop. SR-b4 (even n, T \| n/2 − 1), lcm family | PIM (ELEMENTARY), M3h's rule — confirmed |
| Odd analogue (odd n, T \| (n−1)/2); (2T+1)-gon; n = 1 + 2m·lcm | PIM-candidate (reviewer, M2), both rules; needs hostile review |
| (P) open miss at every H ≥ 2 | PIM, M3h's rule; both rules if M2 passes |
| SR-b2 for bounded support (with p(T ≥ 2) > 0) | PIM, M3h's rule; both rules if M2 passes |
| SR-b2 for unbounded support | HYP (unchanged) |
| (F) disk wins | PIM, restatement of SR-b1(d)–(e) |
| R_H(disk) → 1; tie in the limit | PIM-candidate (L2), was OBSERVED |
| T₀ ≈ 2.0–2.16·√n (even); T₀ ≈ 1.44·√n (odd, n = 401…6401) | OBSERVED |
| n* ≈ 0.2·H²/ln n* (≈ 0.14–0.17·H²/ln H); margin ≈ 13–15·ln H/H² | OBSERVED (rough fits, H ≤ 400) |
| Odd only: some odd n beats the disk at H ≤ 300 under five weights | OBSERVED (H = 400 not found in sample) |
| "No built-in timescale is the stake that selects the disk" | open miss for (P); for (F) a restatement of the design-first order (U) |

## Reviewer files (`rnd/review_srb4/`)

| file | content |
|---|---|
| `rv_core.py` | breakpoint distances, LP distances, circular and forward DPs |
| `rv_check_dist.py/.out` | distances vs LP vs closed form; DP vs brute force |
| `rv_dp.c` | C DP, breakpoint distances, no cap; option `a` = antipode-only target for even n |
| `rv_run_curves.py`, `rv_curves.npy`; `rv_run_mixed.py`, `rv_curves_antipode.npy` | J(n, T), T ≤ 400 |
| `rv_RH_small.py/.out` | H = 2…8 |
| `rv_RH_large.py/.out` | §9.3 table, robustness, odd-only under both J* conventions |
| `rv_odd_robust.py/.out` | odd-only under five weights |
| `rv_lcm.py/.out` | lcm family: DP, 60-digit path and proof chain |
| `rv_odd_lemma.py/.out` | M2 checks |
| `rv_t0.py/.out` | T₀ for even and odd n |
| `rv_crossref.py/.out`, `rv_crossref2.py/.out` | DOIs and prior-art search |
