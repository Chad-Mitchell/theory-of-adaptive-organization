# Hostile review: SR_B.md (with `sr_b/`) and C12B_ORDER.md §9 (with `c12b_post_check.*` and STEPBACK.md §16 addendum 3)

*26 Nov 2026, about 10:26 ET. I am an independent reviewer. This is a local note only: no commit, no push, no email. I read the repo text from a fresh clone of fork branch `forge-rnd-record-cost-2` at head `a57f1f7`, checked with `git ls-remote`. SR_B.md says it read `ac92ee2`. `git diff ac92ee2 a57f1f7` shows no change to `theory/RECORD_COST_ROUND10_2026-11-25.md`, `theory/record-cost-2026-11-25/scripts/selfref/` or `CORE.md`, so the quotes are compared against the same text. The labels are the targets' own: PIM = proved in-model, KNOWN, ELEMENTARY, HYP, OBSERVED. My scripts, all in this folder, are:*
- *`dpeven.c` and `dpfast.c`: an exact even-n DP using a closed-form distance;*
- *`dpmix.c`, `run_mix.sh` → `mix_raw.txt`, and `mix_analyze.py` → `mix_analyze.out`;*
- *`mix_review.py` → `mix_review.out`;*
- *`thm_2T2.py`, `regret_check.py` → `regret_check.out`, and `odd_only.py` → `odd_only.out`;*
- *`crossref_review.py` → `crossref_review.txt`.*

*I also reran `sr_b/srb_tail.py` and `sr_b/srb_analysis.py` on a copy. Both outputs are byte-identical to the committed `.out` files.*

## Overall: PASS-WITH-FIXES

- **SR-b1 holds in its class**, apart from one wrong constant in (e) (M1). Statements (a), (b), (c), (d) and (f) check out. d_min(n) > 0 is uniform in T, and the disk is ≤ π²/(4T).
- **The headline diagnosis is too broad (H1).** "A uniform requirement over horizons (a minimax or competitive criterion)" does not select the disk:
  - Under **minimax additive regret**, a polygon beats the disk. The 10-gon's worst-case regret is ≤ 0.382. The disk's is ≥ 0.5.
  - Under **minimax cost**, every design ties at 1, because every design costs 1 at T = 1.
  - Only the **scale-invariant (ratio) criterion** selects the disk. The open miss names that, not "uniform over horizons".
- **The q-sweep's direction is right. Its tail rows and fits were limited by the n-grid (M2, M3).**
  - With exact curves for even n up to 99,186, a polygon is strictly cheaper at every geometric q up to 0.999, with the best n inside the computed range. That includes q = 0.996 and 0.997, which SR_B lists as "not conclusive".
  - The best n grows like 0.06–0.1/(1−q)², not 10/(1−q).
  - At q = 0.9995 the result is again at the edge of the computed range, so it is not conclusive.
- **The ROUND10 side finding is confirmed** in the text, in the code and in my own numbers. A stronger fact also falls out (§3 below): under M3h's target rule, the (2T+2)-gon is strictly cheaper than the disk at **every** T ≥ 2. ROUND10 labels that HYPOTHESIS. The proof is elementary.
- **C12B §9's new bound w₁ ≥ kT·max(r, Γ)/v is correct as a lower bound.** Its label is acceptable. It needs three wording fixes (L8–L10).
- **No DOI failed.** I found four missed prior-art items (M5).

## HIGH

**H1. "Uniform over horizons" is not what selects the disk. The selecting input is a uniform *ratio* (competitive) requirement.**
- **What SR_B claims.** §0.1, §0.3, the §3 "Reading", the last row of §5 and §7 say the continuum needs "a uniform requirement over horizons (a minimax or competitive criterion), not a Bayes mixture".
- **Counter-example 1: minimax additive regret** (Savage 1951), max_T [J(D,T) − J*(T)].
  - For the disk, this is ≥ disk(2) − J*(2) = 1 − 1/2 = 1/2. Here J*(2) = 1/2 exactly: SR-b1(a) gives ≥ 1/2, and the hexagon attains it.
  - For an n-gon, SR-b1(a) gives J* ≥ 1/T, so its regret is ≤ max_T [J(n,T) − 1/T]. That is a rigorous upper bound from the exact curves.
  - Results (`regret_check.out`): 10-gon ≤ 0.382, 22-gon ≤ 0.358, 201-gon ≤ 0.492, 2400-gon ≤ 0.4987. All are strictly below the disk's 1/2.
  - So a uniform-over-horizons requirement in additive form selects a polygon.
- **Counter-example 2: minimax cost**, max_T J(D,T). It equals 1 for every design (T = 1), so it selects nothing.
- **What SR-b1 actually proves.** Under the requirement "within a bounded *factor* of the best at every horizon", only the disk qualifies. That criterion is scale-invariant across horizons. This is the competitive-ratio form, the same notion as the acceleration ratio for contract versus interruptible algorithms (M5).
- **ROUND10's direction.** ROUND10 §14 says "The disk wins only if one design must serve every horizon". SR-b1 proves the *if* direction for the ratio criterion only. It does not prove the *only if*: that no other criterion selects the disk. The phrase "turns ROUND10 §14's sentence into a proof" overstates this.
- **Fix** (append-only):
  - Replace "uniform requirement over horizons (minimax or competitive)" with "a uniform **multiplicative (competitive-ratio)** requirement over all horizons. Additive minimax regret selects a polygon, and minimax cost ties."
  - Replace "turns … into a proof" with "proves the *if* direction for the ratio criterion".
  - The diagnosis stays HYP. It is sharper: the chosen input is a scale-invariance over horizons, a form of U.

## MED

**M1. SR-b1(e) has the wrong constant.**
- inf_D J(D,T) ≤ J(disk,T) ≤ π²/(4T), so J(n,T)/inf_D J ≥ d_min·4T/π² ≈ 0.405·d_min·T.
- "≥ d_min·T" would need inf_D J ≤ 1/T. That is the wrong direction, since (a) gives inf_D J ≥ 1/T.
- The conclusion, that the ratio grows without bound, is unchanged.
- **Fix:** "(e) J(n,T)/inf_D J(D,T) ≥ (4/π²)·d_min(n)·T → ∞."

**M2. "Not shown: the disk's equal-step path is optimal. Nothing above needs it." The second sentence is false. A short proof closes the gap.**
- **Why it is needed.** §0.2, the §4 table, §0.3's open miss and the HYP all use T·sin²(π/2T) as *the disk's cost*. If the disk had a cheaper path, every mixture margin would be biased against the disk. (SR-b1(d) needs only the upper bound, so it is unaffected.)
- **Proof** (ELEMENTARY; my addition):
  - A T-tick pure path has angular steps φ_t ∈ [0, π] with Σφ_t ≥ π, and it costs Σg(φ_t), where g(φ) = sin²(φ/2) increases on [0, π]. Shrinking steps lowers the cost, so take Σφ_t = π.
  - **If every φ_t ≤ π/2:** g is convex there (g″ = cos φ/2 ≥ 0), so Jensen over the T slots (zeros allowed) gives ≥ T·g(π/T).
  - **Otherwise exactly one step φ₁ > π/2.** Jensen on the rest gives cost ≥ h(φ₁) := g(φ₁) + (T−1)·g((π−φ₁)/(T−1)).
  - h′ = ½[sin φ₁ − sin((π−φ₁)/(T−1))] ≥ 0 on [π/2, π], because (π−φ₁)/(T−1) ≤ π−φ₁ ≤ π/2. So h ≥ h(π/2), which is a configuration of the first case.
  - Hence the disk optimum is exactly T·sin²(π/2T) for every T ≥ 1. ∎
- This agrees with M3b (T = 1, 2, 3, 4, 6, 10) and with Lean `TransportHorizons` (T = 2, 4).
- **Fix:** replace "Not shown … nothing needs it" with this proof, labelled PIM (ELEMENTARY). The mixture rows then rest on exact disk values.

**M3. The q-sweep's tail rows and fits come from a sparse n-grid.**
- **The grid.** Above n = 401, SR_B computed only n ∈ {300, 301, 400, 401, 600, 601, 800, 801, 1000, 1001, 1400, 1600, 1800, 2000, 2001, 2400}. Every value above 1001 is ≡ 0 mod 4 except 2001, yet the winners are almost always n ≡ 2 mod 4.
- **How I reran it.** I computed exact curves with a closed-form distance and a monotone DP (`dpeven.c`, `dpfast.c`).
  - **Distance.** For even n, d(v₀,v_k) = sin(πk/n), divided by cos(π/n) when k − n/2 is odd. This follows from a width argument: d(u,w) = max_θ ⟨u−w, θ⟩ / width_θ(P), and the width of the polygon is 2·cos(angle from θ to the nearest vertex direction).
  - **Exactness.** The curves match the LP-based `sr_b` curves for n = 6…2400 to < 1e−15. `dpfast` caps the step at tick t at ⌊S/t⌋. That is exact because the steps can be reordered from largest to smallest, the t-th largest is ≤ S/t, and the cost does not depend on order.
  - **Range.** 1,497 even n from 400 to 99,186: all n ≡ 2 mod 4 up to 2002, then n ≡ 2 mod 4 at 0.5–1% spacing and n ≡ 0 mod 4 at 2% spacing.
- **Results** (`mix_analyze.out`):

  | geometric q | disk | best n (interior?) | rel. margin |
  |---|---|---|---|
  | 0.99 | 0.0963215 | 962 (yes) | +1.76e−3 |
  | 0.995 | 0.0564463 | 3366 (yes) | +5.33e−4 |
  | 0.996 | 0.0473121 | 5042 (yes) | **+3.62e−4** (SR_B: −0.002%, "not conclusive") |
  | 0.997 | 0.0375763 | 8058 (yes) | **+2.19e−4** (SR_B: −0.10%, "not conclusive") |
  | 0.998 | 0.0270253 | 17278 (yes) | +1.07e−4 |
  | 0.999 | 0.0152084 | 58788 (yes) | +3.07e−5 |
  | 0.9995 | 0.0084553 | 99186 (**edge**) | −2.5e−6, not conclusive |

  - **Uniform horizons on 1..H:** a polygon is cheaper at H = 200, 500, 1000 (interior; +1.28e−3, +2.45e−4, +6.9e−5) and at H = 2000 (edge; +1.9e−5).
- **Convergence.** The disk sums run to T = 4·10⁷ (q^T negligible). Polygon curves are flat beyond saturation, and the sums add the q^L tail exactly. The SR_B outputs reproduce. The n = 1002 value matches between `dpmix.c` and Python.
- **The fits are wrong.**
  - "Best n ≈ 10/(1−q)" is a grid artifact. Observed n*·(1−q)² = 0.096, 0.084, 0.081, 0.073, 0.069 and 0.059 at q = 0.99 … 0.999, so n* grows like 0.06–0.1/(1−q)².
  - "Margin ∝ (1−q)²" is close, but the coefficient grows: 17.6 → 30.7. A better description is ≈ 4.3·(1−q)²·ln(1/(1−q)) (OBSERVED, fitted by eye).
- **Is the HYP plausible? Yes. Here is a heuristic, not a proof:**
  - From the exact curves (n = 8002), an even n-gon beats the disk by a relative 4/n at T ≲ 2√n, because its target sits 2π/n short of the antipode.
  - It loses about frac(1−frac)·4T²/n² at larger T, where frac is the fractional part of the mean vertex step. That is the cost of mixing step sizes, up to +12% near T ≈ 3n/8.
  - With n ≈ α/(1−q)², the gain integrates to about 4·ln M/(αM²) and the loss to about 2/(3αM²) (M = 1/(1−q)). The gain wins for every large M.
  - This matches the observed n* ∝ M² and margin ∝ (1−q)²·ln M.
- **The counter-argument I looked for, and why it fails.** One worry was that the loss beyond saturation (flat J(n,∞) against a falling disk) would beat the gain. At n ∝ M², that loss carries weight e^{−αM/2} and is negligible. What really competes is the step-mixing loss at T ~ √n … n/2. It is O(1/M²) and loses to the gain's log factor.
- **SR-b2's route.** A rigorous all-q proof looks reachable along exactly this path: an upper bound on J(n,T) from near-equal unit-parity steps, summed against p(T). I would raise SR-b2's p_hit above 0.35.
- **Fix:**
  - Append the rerun table.
  - Withdraw "best n ≈ 10/(1−q)" and replace it with "n* ≈ 0.06–0.1/(1−q)² (OBSERVED)".
  - Mark q = 0.996 and 0.997 as polygon wins (OBSERVED). q = 0.9995 is the new not-conclusive row.

**M4. The mixture result depends on which target rule is used. State that.**
- Every best polygon in the reruns is even and uses a **non-antipodal** distinguishable target, as allowed by M3h's rule.
- ROUND10's M3c uses the antipode for even n.
- Restricted to **odd** polygons, whose targets are the same under both rules, a polygon still beats the disk at q = 0.5 … 0.99, with margins about 4 times smaller: +5.5% at q = 0.5, +0.04% at q = 0.99 (`odd_only.out`; n ≤ 401 plus 601, 801, 1001, 2001).
- So the qualitative result does not depend on the rule for q ≤ 0.99. The numbers do.
- **Fix:** add one line to §1 naming M3h's rule, plus the odd-only check.

**M5. Missed prior art** (all DOIs Crossref OK this session, in `crossref_review.txt`):
- **Contract versus interruptible (anytime) algorithms:**
  - Zilberstein & Russell 1996, *Artificial Intelligence* 82:181–213, doi 10.1016/0004-3702(94)00074-3. A contract algorithm needs its horizon fixed in advance; an interruptible one must serve every horizon. Doubling schedules give an interruptible algorithm within a constant **acceleration ratio** (4) of the contract optimum at every deadline.
  - Zilberstein, Charpillet & Chassaing 2003, *Ann. Math. Artif. Intell.* 39:1–18, doi 10.1023/A:1024412831598. Proves 4 is optimal and treats the deadline "with or without stochastic information".
  - Together these are the KNOWN template for SR-b's split: a worst-case ratio over all horizons versus a Bayes prior over the horizon. This is closer than Luby–Sinclair–Zuckerman.
  - The search snippet and the IJCAI 1999 text were read. The AI 1996 full text was not.
- **Savage 1951**, *JASA* 46:55–67, doi 10.1080/01621459.1951.10500768. The minimax-regret criterion, which is what H1's counter-example uses.
- **Nulton, Salamon, Andresen & Anmin 1985**, *J. Chem. Phys.* 83:334–338, doi 10.1063/1.449774, "Quasistatic processes as step equilibrations". This is the **K-step** (discrete) counterpart of the L²/τ bound, so it is the closer credit for SR-b1(a)'s discrete Cauchy–Schwarz than the continuous Salamon–Berry or Crooks. I did not reread its constant this session; read it before citing the exact form.
- **Janotta, Gogolin, Barrett & Brunner 2011**, *NJP* 13:063024, doi 10.1088/1367-2630/13/6/063024. The regular-polygon GPT models, with the disk as their limit; KNOWN prior art for the menu.
- **SR_B's five DOIs re-resolve** correctly: Wald 1949, Blackwell 1962, Luby–Sinclair–Zuckerman 1993, Salamon–Berry 1983, Crooks 2007. Salamon–Berry and Crooks are in ROUND10's source list (verified).

## LOW

- **L1.** SR_B's repo head is stale (`ac92ee2`; the fork head is `a57f1f7`). The relevant files are unchanged, so no content is affected. Cite the head actually read.
- **L2.** SR-b1(b) *defines* d_min := d(v₀,v₁) but the proof uses min_{j≠0}. Use min_{j≠0} in the statement. For even n the closed form shows the minimum is at j = 1, because tan(π/n) < sin(2π/n) for n > 4. For odd n this is OBSERVED only.
- **L3.** The side finding says "'13 strict wins + 1 tie' understates polygon wins". The *horizon count* does not change: T = 1 is a tie for every design (all cost 1), and T = 2…12, 16, 20 were already wins. What changes is the margin and which polygon wins, which is even, the (2T+2)-gon. Also, "13 + 1" is SR_B's paraphrase of ROUND10 §14's sentence, not text that appears in the repo. Reword.
- **L4.** In the §4 table, "2400 (edge; a larger n can only lower the polygon cost)" is wrong. A single larger n does not lower the cost. Only the minimum over a larger set of n can be lower. Reword.
- **L5.** "No price in the repository selects the disk" was checked against ROUND10 §14's two prices only: κ per affine dimension and the log₂|G| map memory. Scope it to those two.
- **L6.** The (G) check uses 57 values of n (range(3, 402, 7)), as stated. That is fine.

## 3. Task 3: the ROUND10 two-target-rules side finding, verified against the text and code

- **Text.** ROUND10 §14, "Gentle transport", has both statements in one bullet group: "An even polygon never beats the disk, and the 4T-gon ties it (PROVED (in-model))" and "Odd polygons beat it (OBSERVED (numerical))". It then says "(2T+1)-gon … at every T from 2 to 12 and at T = 16 and 20, with a tie at T = 1 … That this holds at every finite horizon is a HYPOTHESIS."
- **Code.**
  - `m_round10b.py` `poly_opt` (M3c) returns `best[n//2]`, the **antipode only**. It runs for n ∈ {4, 6, 8, 12, 16, 20, 24} and T = 2…5.
  - `m_round10b_poly.py` (M3h) and `m_round10b_poly_ext.py` use `targets=[j for j … if d[j]>1-1e-9]`, **any perfectly distinguishable vertex**. Only odd n are run.
  - M3g in the same stdout prints the hexagon's d(v₀,v₂)/sin(π/3) = 1.1547, which is d = 1.
- **The hexagon at T = 2 and 3 is real.**
  - d(v₀,v₂) = 1: the effect is 1 on edge v₅v₀ and 0 on the parallel edge v₂v₃.
  - d(v₀,v₁) = ½.
  - The path v₀→v₁→v₂ costs ¼ + ¼ = **0.5** at T = 2 and at T = 3 (staying put is free). The disk costs 1.0 and 0.75, exact by M2.
  - `srb_J.out` agrees (n = 6: J = 1, 0.5, 0.5, …).
  - Under the antipode rule the hexagon gives 1.0 and 0.75, which ties the disk. That is why M3c's statement holds only under its own rule.
- **Stronger, PIM (ELEMENTARY):** under M3h's rule, **the (2T+2)-gon is strictly cheaper than the disk at every T ≥ 2.**
  - Let n = 2T+2. v_{n/2−1} = v_T is perfectly distinguishable from v₀: the chord is parallel to an edge normal, so d = 2cos(π/n)/(2cos(π/n)) = 1.
  - T unit steps cost T·u², with u = sin(π/n) if n/2 is odd and u = tan(π/n) if n/2 is even.
  - Using tan x ≤ x/(1−x²/2) and sin y ≥ y − y³/6, with x = π/(2T+2) < y = π/(2T), the inequality T·tan²x < T·sin²y reduces to π²(T+1) < 6T². That holds for every T ≥ 3. At T = 2 the hexagon gives 0.5 < 1.
  - The disk side is exact by M2.
  - Checked exactly (mpmath, 40 digits) for T = 2…200,000 (`thm_2T2.py`). The relative margin is ≈ 2/T.
  - This turns ROUND10's "at every finite horizon" HYPOTHESIS into PIM, **under M3h's rule only**. Under the mixed convention (antipode for even n, distinguishable vertex for odd n) it stays HYP.
- **For Friday's cleanup**, flagged and not edited:
  - ROUND10's "An even polygon never beats the disk (PROVED (in-model))" is true only for the antipode target. For the task as worded ("a perfectly distinguishable partner") it is false at T = 2.
  - It was also checked only for n ≤ 24 and T ≤ 5 in M3c. Whether "PROVED" was ever earned for all even n and T is not visible in the repo text: the M3c code is numerical, and §14's "Not formalized" list includes "the transport costs".
  - Ace should decide which target rule is intended.

## 4. Task 4: C12B §9's bound w₁ ≥ kT·max(r, Γ)/v

- **The proof checks.**
  - Both branches vanish at ε = v. Γ·ln(v/ε) and r(v−ε)/ε = rv/ε − r are convex, so their max is convex, and f = kT·max(…) + wε is convex.
  - Their left slopes at v are −kTΓ/v and −kTr/v, so the max has left slope −kT·max(r, Γ)/v.
  - On (0, v], the blind point minimizes f iff f′(v⁻) ≤ 0, that is, iff w ≤ kT·max(r, Γ)/v. Then every design costs ≥ f(ε) ≥ f(v) = wv, which is the blind cost. So tracking does not pay strictly, which gives w₁ ≥ the bound.
  - The direction of the IP11 step is right: ε_M ≥ ε_{MC} and R is decreasing, so R(ε_{MC}) ≥ R(ε_M).
- **Premises.**
  - The Γ-branch needs P1 (separate leak), P2, P3/P3′ (the decoder reads M only), P5 with (A) and the corrected (W), and τ → ∞.
  - The IP11 branch needs IP11's class: an exogenous equilibrium OU signal, a regular conditional, the HE bipartite step, and a steady state.
  - Conditioning on the whole source path is legitimate: the source is exogenous, so (M,C) given the path is time-inhomogeneous Markov. Steps 1–3 and the (A)-based entropy cap go through with x replaced by the path. Data processing then gives I(path; M_t) ≥ I(X_t; M_t).
  - The review's R4 numbers quoted in §9.1 match.
- **Was it mislabelled? No.** "PIM, lower bound only, attainment not shown" is accurate. It is an ELEMENTARY composition of the G-keep live extension with IP11. Low fixes:
  - **L7.** The max needs both branches to bound the **same** quantity. G-keep's Q is kT·Ṡ_res over all (M,C) channels, fuel included; IP11's is the memory-bath heat of the memory's transitions. Say once that the memory is (M,C) with all its channels, so the two coincide. If any C channel used a reservoir outside "memory-bath", the IP11 branch would bound only part of Q, which is still a valid lower bound but should be stated.
  - **L8.** f(ε) is written for a constant (steady) design. IP11 is a steady-state statement. For time-varying designs, add the Jensen line: both branches are convex in ε, so the time-averaged cost is ≥ f(⟨ε⟩). This is the same point as §9.5 L3.
  - **L9.** The IP11 citation `GENERAL_FORM_PHYSICS`:56–60 should be **:56–62**. The Horowitz–Esposito sentence is on :62.
  - **L10.** STEPBACK §16 addendum 3 states the bound without its premises. Add "under the premises of C12B §9.1: P1–P5 live, (A), (W)/(P3′), IP11's class, τ → ∞".
  - **Provenance.** The live-phase extension comes from the previous review's H1(c) and has been self-checked only since. That is fine for its label, but say so.
- **`c12b_post_check.py` (1)** checks only the arithmetic of f's onset. It is not evidence for the premises. Label it "OBSERVED (arithmetic of the onset)".
- **Horowitz & England 2017** (10.3390/e19070333) re-resolves on Crossref (OK).
- **Rest of §9** (H1 rescoping, the M1 novelty change, the M2 change to (P3′), §9.5): consistent with the previous review. The "two lower bounds cannot be ordered" logic is right.

## 5. Corrected labels

| claim | SR_B / §9 label | corrected label |
|---|---|---|
| SR-b1(a) J ≥ 1/T for every design | PIM (KNOWN form) | PIM (KNOWN form; discrete credit Nulton et al. 1985) |
| SR-b1(b), (f) polygon floor d_min > 0, uniform in T; each polygon loses beyond π²/(4d_min) | PIM | PIM (define d_min as min_{j≠0}) |
| SR-b1(c) disk ≤ π²/(4T) | PIM | PIM |
| Disk equal-step path optimal at every T | "not shown" | **PIM (ELEMENTARY; M2 proof)** |
| SR-b1(d)–(e) only the disk is within a bounded factor at every horizon | PIM | PIM, with (e)'s constant 4/π² |
| "The continuum needs a uniform-over-horizons requirement" | HYP (diagnosis) | **HYP, narrowed: a uniform *ratio* requirement. Additive minimax regret selects a polygon (OBSERVED + rigorous bound); minimax cost ties** |
| SR-b1 proves ROUND10's "disk wins only if one design must serve every horizon" | (implied PIM) | **PIM for the *if* direction, ratio criterion only** |
| A polygon beats the disk under geometric mixtures | OBSERVED, q ≤ 0.995 | **OBSERVED, q ≤ 0.999** (best n interior); q = 0.9995 not conclusive (edge n = 99,186) |
| … under uniform mixtures | OBSERVED, H ≤ 200 | OBSERVED, H ≤ 1000 interior; H = 2000 at the edge |
| A polygon beats the disk for every proper horizon distribution | HYP | HYP, now with a heuristic scaling argument (M3) in its favour |
| Best n ≈ 10/(1−q); margin ∝ (1−q)² | OBSERVED | **withdrawn (grid artifact).** n* ≈ 0.06–0.1/(1−q)²; margin ≈ 4.3(1−q)²ln(1/(1−q)) (OBSERVED, by eye) |
| ROUND10 M3c/M3h target-rule mismatch | OBSERVED | OBSERVED (confirmed in text and code); the hexagon's 0.5 at T = 2, 3 is exact |
| Under M3h's rule, some polygon beats the disk at every finite T ≥ 2 | (ROUND10: HYPOTHESIS) | **PIM (ELEMENTARY; the (2T+2)-gon), under M3h's rule only** |
| C12B §9 w₁ ≥ kT·max(r, Γ)/v | PIM lower bound | PIM lower bound, an ELEMENTARY composition (G-keep live + IP11); add the L7–L10 wording |
| c12b_post_check (1) | OBSERVED | OBSERVED (arithmetic of the onset only) |
| C12b track-vs-keep ordering | OPEN, open miss | unchanged |

## 6. Rescore note (not binding)

- SR-b2, the all-q statement: the M3 heuristic gives a concrete route, so p_hit is plausibly about 0.5 rather than 0.35.
- The V_miss story changes, because the disk did not win at any interior q tested.
- The diagnosis to carry forward is "scale-invariance over horizons (ratio), a chosen form of U", not "worst case over horizons".
