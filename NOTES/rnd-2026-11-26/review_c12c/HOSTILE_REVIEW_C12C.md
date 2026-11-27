# Hostile review: C12C_ONSET.md (memory onset vs stake and buffer)

*26 Nov 2026, from 08:02 ET. Independent hostile reviewer, not the note's author. Local notes only: no commits, no pushes, no email. THEORY.md and CORE.md were read, not edited.*

**Reviewed (sha256 prefixes):**
- `rnd/stepback/C12C_ONSET.md` c31f37c1b9bdbb34
- `c12c_check.py` 2043b9ae1107418d
- `c12c_check.out` 0bef57accf694561
- `crossref_c12c.txt` 829b0af05ce00662

**Repo text:** read at `499ef04` in the fresh clone `/workspace/qmsel3-run` (branch `forge-rnd-record-cost-2`):
- THEORY.md:279–281 (CT4), :392 (CT18), :402 (CT25), :440–464 (CT22), :495 (CT33), :186, :101 (CT24)
- CLAIM_MAP_v2.md:713 (V3), :716 (V6)
- CORE.md:29
- theory/RECORD_COST_CHAIN_2026-11-25.md:26, :54–62, :92
- reviews/audit_2026-11-19/AUDIT.md:102–105

**Paper read:** Still 2020, arXiv 1705.00612v3 (`still2020.pdf`, c943689722b01828; text in `still2020.txt`).

**Independent checks:** `review_c12c_check.py` → `review_c12c_check.out`. The script is written from scratch and does not import the author's script.

**DOIs:** all 12 re-verified on Crossref this session (`crossref_review_c12c.txt`). That includes the two that hit HTTP 429 in the author's first pass.

## Overall: **PASS-WITH-FIXES**

The 1-D core (Theorem O) is correct, apart from one hypothesis slip in (iii). So is the CT22 limit argument in §4.3. The numbers reproduce independently. Three things must change before any of it counts:
1. Lemma A(b) is **false as stated** (high).
2. The class-A closed forms are **not optimal outside Gaussian memories**. A concrete non-Gaussian memory beats them by about 4.8× in bits (med). The onset *location*, by contrast, survives for all memories, so that part can be upgraded.
3. The note's novelty claims overlook prior art inside the repo (med).

Nothing here is a breakthrough, and the note says so itself.

---

## High

**H1. Lemma A(b) is false with the stated hypothesis (§2). It is labeled KNOWN and attributed to Everett.**

The hypothesis is that d\* lies on the lower convex hull of the attained points. That does not ensure a multiplier μ ≥ 0 with μ(E\* − D) = 0.

*Counterexample* (R1 in the `.out` file):
- Menu (E, S): A = (0, 1) and B = (1, 0). Cap D = 0.5, stake w ∈ {0.25, 0.5, 0.9}.
- The constrained optimum is A. A is a vertex of the lower hull, and E\* = 0 < D.
- Complementary slackness therefore forces μ = 0. But at stake w with no cap, B beats A (cost w < 1).
- So no KKT multiplier exists. A stake does select A, but only w + μ ≥ 1, and that violates complementary slackness.

*Where the proof breaks:* "E\* minimizes h(E) + wE over E ≤ D" does not follow from constrained optimality. The envelope h on [E\*, D] is built from mixtures with infeasible points (E > D). Those mixtures are not available when mixing is not allowed.

*Correct statement:*
- (b′) If the attained set's free-disposal hull is convex (mixtures allowed, or the menu is convex), then strong duality holds. In that case a μ ≥ 0 with complementary slackness exists.
- (b″) Without convexity, a sufficient condition is that the constrained value function v(D) = min{S + wE : E ≤ D} agrees with its convex envelope at D (no duality gap at D).
- The hull-vertex condition alone is enough only when the cap binds (E\* = D).

*Attribution:* Everett 1963 is the sufficiency direction, Lemma A(a). The converse is standard Lagrangian strong duality under convexity, not Everett's Theorem 1. I am going from general knowledge here and did not re-read Everett this session, so this should be checked before the citation is reworded.

*Impact:* §0's headline wording, "a required accuracy acts as a stake on the convex hull of the menu", stays right if it is read as "when mixtures are allowed". It matters because C12c-G (§7) is exactly the non-convex case, so a wrong (b) would mislead that run.

*Fix:* replace (b) with (b′)/(b″) and keep (a). Theorem O is 1-D and convex, so it does not depend on (b).

## Medium

**M1. The class-A closed forms are not optimal over all memories. The onset location is.**

*Counterexample* (R5): a non-Gaussian memory beats the Gaussian closed form by about 4.8× in bits.
- Setting: a = 0.8, Var = 1, ε = 10⁻³, B = 0.99·B₀ = 3.2576.
- The Gaussian memory needs I_req = 0.0228 bits.
- A deterministic three-state tail flag meets the same chance cap with H(M) = 0.00479 bits. It records sign(X) only when |X| > 3.58 and predicts ±4.01 in that case.
- Quadrature gives ruin 9.95×10⁻⁴. Monte Carlo with 2×10⁷ draws gives 9.93×10⁻⁴, against 1.12×10⁻³ blind.

What follows:
- I_req(B), w\*(B) and B_slack(w) are **upper bounds** on the cheapest design, and I\* = max(I_w, I_req) is not the optimum over all memories.
- A chance cap prices a tail-indicator loss, not the squared error the stake weights. "Cap = effective stake on the same loss" holds only after the restriction to Gaussian memories. Theorem O needs the cap and the stake on the same f.

What survives, and can be upgraded:
- The **L-shaped onset boundary holds over all memories**, at B₀ = z_ε√Var and w₁ = κ/(2 ln 2·a²Var).
- Below B₀, every zero-bit predictor has error N(0, Var) and misses the cap.
- At B ≥ B₀, the blind design meets the cap. CT4's IB curve then makes it the unconstrained optimum for w ≤ w₁, because the Gaussian IB is optimal for squared error.
- So: memory is on ⇔ w > w₁ or B < B₀. This is PIM for all memories, and the note currently labels it Gaussian-only.

I recomputed B₀ = 3.29053, B_fl = 1.97432 and w₁ = 0.056355. Independent root-finding for I_req and w\* matches the closed forms to 6 digits at B = 2.1, 2.6, 3.0 and 3.25 (R4).

**M2. Prior art inside the repo is not credited, so the "what is ours" claims are overstated (§0.4, §4, §9).**
- `reviews/audit_2026-11-19/AUDIT.md:102–105` (Candidate 2) already states that "the stakes w are the reciprocal of the shadow price of that budget". It includes a check, says "the survival price μ_s is already a multiplier of this kind", and gives the convexity caveat ("duality can fail at fixed costs"). That is the budget-dual form of Lemma A, in this repo.
- The "stake-free vs stake-carrying" split is CT33's own scope condition ("the design set must not depend on w", THEORY:495). It is also V3's "stake-independent menu" (CLAIM_MAP:713) and CT24's "feasible set does not depend on the prices" (THEORY:101).
- The note's real addition is applying that existing condition to the onset and the zero-stake floor, plus the two class computations. Its "new framing (HYP until reviewed)" row in §3.4 should say so.
- Still 2020 itself says the temperature ratio α "can also be interpreted as a Lagrange multiplier" (p. 4). Its Eq. (7), −Q ≥ kT·I_irrel ≥ 0 at T′ = T, is already the "zero-stake floor at a single temperature".

**M3. §4.3 and §4.4: the CT22 proof is right, but "false" and "cannot force memory" are stated loosely.**
- *Proof checked* (not just the numerics):
  - θ(τ) ≤ 2(y − c/τ)/s₀² < 2y/s₀² for every τ, so B_min(w) > L·s₀²/(2y).
  - J(τ_E) = √(2cwσ²) and βτ_E³ = (σ⁴/3)(2c/σ²)^{3/2}·√w both tend to 0.
  - B_min ≤ B_slack sandwiches both at the limit, 0.310849 (R6).
- *At w = 0 the statement holds by construction.* A stake-carrying cap sees the loss only through w·loss, so at w = 0 the cap cannot reward judgment. On CT22's path at w = 0 the cap is never *binding*: it is either slack or infeasible. The STEPBACK clause "a world with a binding ruin cap needs memory at zero stake" is therefore **vacuous** for CT22-type caps, not shown false. Say "inapplicable (the cap never binds at w = 0), and in the limit the band collapses".
- *For every w > 0* there is a band where the cap does force more checking than the stake optimum. The note's claim is true per fixed B. The stronger uniform statement it needs, which I checked, is that even the survival-optimal design checks at a vanishing rate:
  - τ_S·√w → 0.2197, flat from w = 10⁻⁶ to 10⁻³ (R6), so the forced check rate is O(√w).
  - The proof sketch: θ_w → θ₀ uniformly on compacts, and θ₀ is increasing, so τ_S → ∞.
  - Add this as PIM (limit) plus OBS (the constant).
- *§4.4 conflation:* "This is exactly CT22's B_slack definition evaluated at 𝒟_E, because for w ≤ w₁, 𝒟_E is the blind design" mixes two models. CT22's path has no w₁: checking is on at every w > 0, as in class B, so w₁ = 0. And CT22's B_slack is a Lundberg certificate, not class A's chance cap. C13-5 is answered by Theorem O(v) in the stake-free classes only. Say that, and drop the CT22 sentence.

**M4. The C12c-G prereg sketch (§7) is not lockable as written.**
- The outcome is not fixed by any theorem for a finite, non-convex menu. I agree with the note on that point.
- *The reading is unstated.*
  - Under the locked **total** reading (RECORD_COST_CHAIN:64), the stake row is "—", meaning no q-flip at zero drift.
  - So the q-dependence the sketch leans on exists only under the per-record reading. Under the total reading the question may come out trivially as "no gap" (one winner at every q and every D).
  - The prereg must name the reading and the drift setting.
- *Blinding:*
  - The chain already publishes J at q = 4 and the crossover stakes (7.7 pairs; 12.4–17.6 singles). With J_W(q) = S_W + q·E_W, the (S, E) points of many worlds can be backed out from committed numbers. The author has seen those.
  - The pairs comparison has only two points (quantum, boxworld), and a two-point menu can never have a gap.
  - The gate needs a statement of what is already computable from committed numbers, and the pairs case should be dropped.
- *Mixing:* "mixtures not allowed" must say whether it covers *within-world* time-sharing of designs as well as mixing across worlds. Within-world mixing convexifies each C_W.
- *Prior 0.6 for no gap:* not reasoned. With 6 single-system worlds as points, a non-hull Pareto point is not unlikely a priori. Either give the reason or move it nearer 0.5.
- *The "frontier C_W(D)":* the sketch assumes the chain's scripts expose a spend–error frontier per world. That is not shown. If each world is one point at locked settings, say so, because then the run is a 10-minute table read, not 2 h.

## Low

- **L1. Theorem O(iii) hypothesis.**
  - "If x_D > x_w … μ > 0" is wrong when g_w has a flat minimizing segment.
  - Example (R3): f with slope −1 on [0.5, 1.5], w = κ = 1. Then argmin g_w = [0.5, 1.5]. A cap with x_D = 1 > x_w gives μ = 0.
  - The proof itself already uses x_D > x_w′, so state (iii) with x_w′ (or assume f strictly convex).
  - w_eff = max(w, w\*(D)) still holds, because w\* = w there.
  - At a kink of f, every stake in [κ/|f′(x_D⁻)|, κ/|f′(x_D⁺)|] supports x_D. So w\*(D) is the **least** supporting stake, not "the" effective stake. That matters for the planned finite Lean version, where every point is a kink.
- **L2. f′(x_D⁻) < 0.** The stated reason, "f > D to the left", is not sufficient on its own. It also needs inf f < D, which is assumed. With f′(x_D⁻) = 0, x_D would be a global minimum of f with f(x_D) = D. Cite the hypothesis.
- **L3. Class B lies outside Theorem O's hypotheses.** f(x) = σ²/(2x) has f(0) = +∞. Either extend Theorem O to f : (0, ∞) → [0, ∞) with f(0⁺) = ∞ (then x_w > 0 for every w > 0; the proof goes through), or say class B is handled by direct calculation. That calculation is right: w\*(B) = 2c·z_ε⁴σ²/B⁴ is recomputed by root-finding in 3 cases.
- **L4. Units in CT25.** The scaling *is* forced by units, but only within the H = ½ reset path whose inputs are just c, σ, B and ε. There are four quantities in three dimensions (cost, x, t), so one group, w·B⁴/(cσ²), times G(ε). Check: rescaling x by λ = 3.7 multiplies w\* by λ⁻² exactly (R7). With CT18-H (H ≠ ½) or an added scale such as CT22's y or s₀, the exponent is not −4. The note's "not an informative prediction" is correct and does not overclaim. Add "for H = ½" to the statement.
- **L5. §4.2 monotonicity is provable, not just OBS.** θ(τ_E(w)) = 2(y − √(2cwσ²)) / (s₀² + (σ⁴/3)(2c/σ²)^{3/2}·√w). The numerator falls and the denominator rises in w, so B_slack(w) is strictly increasing wherever m(τ_E) > 0. That is PIM on CT22's path, matching the closed form to 6 digits at 13 stakes (R6). The width ∝ √w is OBS (log–log slope 0.5005).
- **L6. The record-cost chain (§1).**
  - The quotes are exact: "The stake q = 4 is the session's convention, not derived" (:62) and "above q≈7.7 (pairs) and q≈12.4–17.6 (single systems)" (:60).
  - But "the selected world depends on it" holds only under the per-record reading. The locked total reading shows no flip at zero drift ("—" in the stake row). Add "under the per-record reading".
- **L7. §6, the Still reading.**
  - The math is right. sup_s I_rel/I_mem = ρ² (R8), so net work T′I_rel − T·I_mem > 0 is possible iff T′/T > 1/ρ². That is Still's own efficiency condition I_rel/I_mem ≥ T/T′ (Eq. 11 text) applied to a scalar Gaussian. The quotes and Eq. (8) are as the note states.
  - Where it overreaches:
    - (a) α multiplies a *benefit* (relevant information turned into work at T′), not a weight on loss. "Stake = temperature ratio" is an **analogy in form**, like the earlier "temperature = price of information" note, and should be labeled that way.
    - (b) Still's protocol uses discrete memory states. The Gaussian case is a statement about the bound's objective, not about an engine. The note says this, so keep that wording.
    - (c) The ratio is set by an engine design choice (α = V/V′, adiabatic compression), so the "stake" here is supplied by a second bath plus a compression step. That is not bare physics.
    - (d) The "zero-stake floor at a single temperature" is Still's Eq. (7). Label it KNOWN, not PIM.
  - CORE:29 is not contradicted.
- **L8. Scores (§8).**
  - The arithmetic is right in every row: 2.06, 0.824, 1.88/0.94/2.82, 2.4/1.2, 1.8/1.2.
  - Inconsistent figures: §0 says ≈ 2.0 per hour, §10 says ≈ 2.1 (it is 2.06).
  - "Above C1 0.83 within noise" is wrong: 0.82 < 0.83. Say "level with C1".
  - The C12c-G row labels the gap as p_hit = 0.4, while §7's prediction is no gap. Swap the labels or rename the columns.
  - Scoring this hostile review as an EIV item (V = 2) treats quality control as evidence. STEPBACK §12 keeps bookkeeping out of the ranking, so do the same here.
  - The "sunk included" rate is retrospective only and must not drive the next pick.
  - After this review, the residual C12c item is done except for the fixes.
- **L9. Prior art.** All 12 DOIs resolve on Crossref with matching title, author, venue, year and pages. Two further notes:
  - Chechik et al. 2005 (no DOI) is correctly marked as not verified.
  - "Gaussian IB critical β = 1/ρ² in the scalar case" is re-derived (R8) and consistent with the note.
  - Nothing claimed as ours is a known *theorem* beyond what §9 already concedes. The over-claim is about GTAO-level novelty (M2), not mathematics.

## Recommended labels

| piece | label |
|---|---|
| Lemma A(a) | KNOWN (Everett 1963) |
| Lemma A(b) | KNOWN (Lagrangian strong duality), **only** as restated in H1 |
| Theorem O (i), (ii), (iv), (v) | PIM (paper, reviewed here); KNOWN in substance |
| Theorem O (iii) | PIM after the L1 fix; w\* = the least supporting stake |
| Class A onset: L-shaped, corner (w₁, B₀) | **PIM over all memories** (upgrade, M1) |
| Class A I_req, w\*(B), B_slack(w), I\* = max(I_w, I_req) | PIM **within linear-Gaussian memories only**; OBS: not optimal over all memories (tail-flag example, R5) |
| Class B w\*(B) = 2cz_ε⁴σ²/B⁴ | PIM (H = ½); exponent fixed by units; not a prediction |
| CT22 band collapse as w → 0 | PIM (limit); "vacuous at w = 0", not "false" (M3) |
| CT22 B_slack(w) increasing | PIM on CT22's path (closed form, L5) |
| Width ∝ √w; τ_S√w → 0.22 | OBS |
| Stake-free vs stake-carrying split | CT33/V3 scope condition applied to onset; credit AUDIT 2026-11-19 Candidate 2 (M2) |
| §6 Still reading | KNOWN bound and threshold; "stake = T′/T" is HYP, an **analogy in form** |
| C12c-G | DRAFT; not lockable until M4 is fixed |
| Overall C12c HYP (STEPBACK §11) | Corrected: PIM for stake-free caps; inapplicable/vacuous for CT22-type caps at w = 0 |

## Open misses logged by this review
- **Open miss (class A, closed forms):** the Gaussian-memory formulas are beaten by a tail-flag memory at B = 0.99·B₀. The true minimal-bit design under a chance cap is open. It names the input: the cap's loss differs from the stake's loss.
- **Open miss (Lemma A(b)):** the hull-point condition is insufficient. The two-point menu at D = 0.5 is the witness.
