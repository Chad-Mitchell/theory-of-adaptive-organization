# SR-b: does an unbounded horizon mixture select the disk? First work unit, on paper plus numerics

*26 Nov 2026, about 10:45 ET. Local note only (not committed or pushed). Repo text read at fork head `ac92ee2` (`/workspace/lemmar-check`). Self-checked only; it needs a hostile review before it counts. Labels: **PIM** = proved in-model; **KNOWN**; **ELEMENTARY**; **HYP**; **OBSERVED** = numerical output of the scripts in `sr_b/`. Units: the cost J of ROUND10 §14, dimensionless.*

## 0. Result

1. **Every design pays at least 1/T at horizon T. The disk is within a factor π²/4 of that at every horizon, and every polygon is worse than the best by a factor that grows without bound** (PIM, §3).
   - So if one design must stay within a bounded factor of the best at *every* horizon, only the disk qualifies in this menu.
   - This turns ROUND10 §14's sentence "the disk wins only if one design must serve every horizon" into a proof. That requirement is a worst case over all horizons, a U-like input. Unbounded support of the horizon alone does not do it.
2. **A proper horizon mixture does not select the disk at any tested setting** (OBSERVED, §4).
   - Geometric horizons: some polygon is strictly cheaper than the disk at every q ≤ 0.995 (mean horizon up to 200). Uniform horizons on 1..H: the same for every H ≤ 200.
   - The relative margin shrinks, roughly like (1−q)²: +17% at q = 0.5, +0.05% at q = 0.995.
   - At q = 0.996 and 0.997 the best polygon found is the largest one computed (n = 2400), so the computation is not conclusive there.
   - The best n grows roughly like 10/(1−q), and T·J*(T) → π²/4, the disk's constant.
   - **HYP:** for every proper horizon distribution, some polygon beats the disk, and the disk is the *limit* of the selected designs as the mean horizon → ∞, but never the selection itself.
3. **The SR-b prediction "the disk is selected for some q < 1" is an open miss at every tested q** (OBSERVED, not proved for all q).
   - What the miss names: the continuum needs a uniform requirement over horizons (a minimax or competitive criterion), not a Bayes mixture over them. That sharpens FH (STEPBACK §14) from "finite horizon" to "Bayes versus worst-case over horizons".
   - It is still a diagnosis, not a derivation. The uniform requirement is a CHOSEN input, a form of U.
4. **A side finding about ROUND10 §14's own record** (OBSERVED; flag for Friday's cleanup, nothing edited):
   - "An even polygon never beats the disk" (M3c) uses the **antipode** as the target. The odd-polygon wins (M3h) use **any perfectly distinguishable vertex** as the target.
   - Under M3h's rule, even polygons also beat the disk. The hexagon costs 0.5 at T = 2 and 3, against the disk's 1.0 and 0.75, because hexagon vertices 0 and 2 are at operational distance 1 with all effects.
   - The "13 strict wins + 1 tie" therefore understates polygon wins. The direction of the conclusion is unchanged.

## 1. Definition (from STEPBACK §14(b) and the C14-1 correction; ROUND10 §14 "gentle transport")

- **Designs.** A regular n-gon state space with all effects (n ≥ 3), or the disk. ROUND10 §14's price is κ per affine dimension. That is the same for every n-gon and the disk (all are planar sections), so it cancels. "Price-free" below means exactly that.
- **Task.** Move a record from a pure state to a perfectly distinguishable partner (operational distance 1) in T ticks. At each tick the state jumps to a pure state (a vertex, for polygons); staying put is allowed. The cost is J = Σ_t d_t², with d the operational distance max_e [e(a) − e(b)] over all effects. This is M3h (`m_round10b_poly.py`).
- **Disk.** Pure states at angle φ are at distance sin(φ/2) (ROUND10 `m_round10b.py` M3a). The equal-step path costs T·sin²(π/2T).
- **Horizon mixtures.** Geometric: p(T) = (1−q)q^{T−1} for T ≥ 1, shifted so that T = 0, an impossible task, is excluded. STEPBACK §14 wrote (1−q)qᵀ; this is the T ≥ 1 version. Also uniform on 1..H.
- **Question.** Is the disk argmin over designs of E_T J(design, T) + price, for some q < 1?

## 2. Prior art (DOIs resolved on Crossref this session: `sr_b/crossref_srb.txt`)

- **Bayes versus minimax.** Wald 1949, *Ann. Math. Stat.* 20:165–205, doi 10.1214/aoms/1177730030. KNOWN: a Bayes rule under a proper prior and a minimax rule are different criteria and can pick different decisions. §0.1 versus §0.2 is an instance; nothing general is claimed.
- **One policy for all long horizons.** Blackwell 1962, *Ann. Math. Stat.* 33:719–726, doi 10.1214/aoms/1177704593. KNOWN: in a *finite* MDP one policy is optimal for all discount factors close to 1, and a geometric horizon is equivalent to discounting. Here the design menu is infinite, and the observed best n keeps growing as q → 1, so no single polygon is optimal near q = 1. That is consistent with finiteness being essential to Blackwell's result; it is not a new result about MDPs.
- **Strategies for an unknown horizon.** Luby, Sinclair & Zuckerman 1993, *Inf. Process. Lett.* 47:173–180, doi 10.1016/0020-0190(93)90029-9. KNOWN: a universal schedule is within a log factor of optimal for every unknown distribution. This is the competitive (all-horizons) criterion in another setting, cited as an analogy only.
- **The 1/T floor.** Salamon & Berry 1983, *PRL* 51:1127–1130, doi 10.1103/PhysRevLett.51.1127, and Crooks 2007, *PRL* 99:100602, doi 10.1103/PhysRevLett.99.100602. KNOWN: the cost of a T-step path of length L is ≥ L²/T (thermodynamic length/divergence, by Cauchy–Schwarz). §3(a) is that inequality with L ≥ 1, read in the operational metric. Already in ROUND10's source list.
- **Not found:** a statement that Bayes horizon mixtures select polygons while the all-horizon criterion selects the disk, in GPT selection. "Not found" is not "new". The search was the repo (ROUND10 §§6, 14; STEPBACK §14) plus the sources above. The composition is ELEMENTARY.

## 3. The core step (PIM in the class of §1)

**Proposition SR-b1.** For every design D in the menu and every T ≥ 1:
- (a) J(D, T) ≥ 1/T.
- (b) For an n-gon, J(n, T) ≥ d_min(n) := d(v₀, v₁) > 0.
- (c) J(disk, T) ≤ T·sin²(π/2T) ≤ π²/(4T).

Hence:
- (d) J(disk, T) ≤ (π²/4)·inf_D J(D, T) at every T.
- (e) For every n-gon, J(n, T)/inf_D J(D, T) ≥ d_min(n)·T → ∞.
- (f) Every fixed n-gon is strictly worse than the disk for all T > π²/(4·d_min(n)).

*Proof.*
- **Metric.** The operational distance is a metric on states. It is symmetric because e ↦ 1 − e maps the all-effects set to itself, and it satisfies the triangle inequality as a supremum of differences of linear functionals.
- **(a)** A path with k ≤ T non-zero steps from v₀ to a partner at distance 1 has Σd_t ≥ 1 by the triangle inequality. Cauchy–Schwarz then gives Σd_t² ≥ (Σd_t)²/k ≥ 1/T.
- **(b)** Define d_min(n) := min_{j≠0} d(v₀, v_j). It is > 0 because distinct extreme points are separated by some effect, and by dihedral symmetry every non-zero step has d_t ≥ d_min. OBSERVED: the minimum is at the neighbour j = 1 for every n tested. So Σd_t² ≥ d_min·Σd_t ≥ d_min.
- **(c)** The explicit equal-step path, with sin x ≤ x.
- **(d)** follows from (a) and (c). **(e)** follows from (a)'s infimum bound together with (c) ≤ π²/(4T), and (b). **(f)** follows from (b) and (c). ∎

**Reading.** Under the requirement "within a bounded factor of the best design at every horizon", the disk is the only design in the menu that qualifies, and the factor is at most π²/4 ≈ 2.47. This requirement quantifies over all horizons uniformly. It is a CHOSEN input of the same kind as U, not something the cost supplies.

**Not shown:** that the disk's equal-step path is optimal for the disk at every T. ROUND10 proves T = 2 and T = 4 in Lean, and M3b checks it numerically. Nothing above needs it.

## 4. Numerics (OBSERVED; `sr_b/*.py` → `.out`)

- **Reproduction.** `srb_J.py` reproduces ROUND10's M3h values: 7-gon 0.5942 at T = 3, 9-gon 0.4825 at T = 4.
- **Coverage.** J(n, T) was computed for every n = 3…401 to saturation, and for selected n up to 2400 (`srb_all.py`, `srb_big.py`, `srb_huge.py`).
- **(G) check of SR-b1 (a)–(b):** J(n, T) ≥ max(1/T, d_min) at every computed (n, T) in a sample of 57 n-values: 0 violations.
- **Beyond the design horizon** (`srb_J.out`, `srb_mix.out` (A)). J(n, T) is flat beyond saturation (T ≈ n/2) at J(n, ∞) ≈ π²/(2n). The disk drops below it from T ≈ n/2 + 1 on (e.g. n = 201: J(∞) = 0.02443; the disk is lower from T = 101).
  - For large n the polygon beats the disk at only some T ≤ n/2, not all: 30 of 100 for n = 201, 69 of 503 for n = 1001. The wins follow how the vertex grid lines up with the disk's equal steps.
- **Best polygon at each horizon** (`srb_analysis.out` (C)). J*(T)/disk(T) = 0.50 at T = 2, 0.65 at T = 4, 0.83 at T = 10, 0.91 at T = 20, 0.961 at T = 50, 0.980 at T = 100, 0.995 at T = 200. T·J*(T) → π²/4 from below, with n* ≈ 2T. The best polygon at T is even at every listed T from 2 to 150 (see §0.4). At T = 200 the best found is n = 401, the largest n in that sweep.
- **Mixtures** (`srb_analysis.out` (D), (F); `srb_tail.out`):

  | geometric q | mean T | disk | best n | best polygon | margin |
  |---|---|---|---|---|---|
  | 0.5 | 2 | 0.9064 | 6 | 0.7500 | +17.3% |
  | 0.9 | 10 | 0.4529 | 30 | 0.4305 | +4.9% |
  | 0.95 | 20 | 0.2982 | 74 | 0.2920 | +2.1% |
  | 0.98 | 50 | 0.16024 | 290 | 0.15936 | +0.55% |
  | 0.99 | 100 | 0.096322 | 1000 | 0.096155 | +0.17% |
  | 0.995 | 200 | 0.056446 | 2400 (edge; a larger n can only lower the polygon cost) | 0.056421 | +0.046% |
  | 0.996 | 250 | 0.047312 | 2400 (edge of the computed range) | 0.047313 | −0.002%, not conclusive |
  | 0.997 | 333 | 0.037576 | 2400 (edge) | 0.037614 | −0.10%, not conclusive |

  Uniform on 1..H: polygons are cheaper at every H ≤ 200 (+21% at H = 5 down to +0.09% at H = 200).
- **Reading.** Wherever the best n lies inside the computed range, a polygon wins. The two negative rows have their best n at the edge of that range (n = 2400), so they do not show the disk winning.
- **A price fixed in advance.** A description price λ·log₂|G| (dihedral group |G| = 2n; the disk's group is continuous) only adds to the disk's cost, so it cannot make the disk win. With ROUND10's own price (κ per affine dimension) the comparison is the price-free one above. **No price in the repository selects the disk.**

## 5. Labels

| claim | label |
|---|---|
| SR-b1 (a) J ≥ 1/T for every design | PIM (KNOWN form: Salamon–Berry / Cauchy–Schwarz) |
| SR-b1 (b) polygon floor d_min(n) > 0; (f) every fixed polygon loses to the disk beyond π²/(4d_min) | PIM |
| SR-b1 (d)–(e) only the disk is within a bounded factor of the best at every horizon (factor ≤ π²/4) | PIM |
| A proper mixture selects a polygon (geometric q ≤ 0.995; uniform H ≤ 200) | OBSERVED |
| A polygon beats the disk under every proper horizon distribution; the disk is the limit, never the selection | HYP |
| Margin ∝ (1−q)², best n ≈ 10/(1−q), T·J*(T) → π²/4 | OBSERVED (fits by eye, not fitted) |
| ROUND10 M3c/M3h target-rule mismatch | OBSERVED (code read; values reproduced) |
| "The continuum needs a uniform-over-horizons requirement" as the diagnosis behind FH | HYP (diagnosis; consistent with SR-b1, not derived from the cost) |

## 6. What is still open

- **The all-q statement.** Prove that for every q < 1 (or every proper p(T)) some polygon beats the disk. Bound (a) is a factor π²/4 too loose to settle it, so it needs an upper bound on J*(T) sharp to o(1/T) plus control of the loss beyond saturation. Alternatively, find q < 1 where the disk wins; that needs n > 2400 at q ≥ 0.996.
- **Sanity of the menu.** Only regular polygons and the disk were compared. Irregular polygons and other planar convex bodies were not. Non-planar parts (3-ball, polytopes) are outside SR-b's one-part menu.
- **The hostile review** of this note.

## 7. Rescore (§13 scale; reviews and sunk cost not scored)

- **SR-b (paper sketch):** done. The outcome is the V_miss branch with a PIM theorem attached: the miss names "a uniform-over-horizons requirement", which FH/§14 had only half-named.
- **New row SR-b2, the all-q analytic statement:** p_hit 0.35, V_hit 2.5 (it would turn "never the selection" into PIM); p_miss 0.65, V_miss 1.5 (a disk win at some q, or a bound that fails to close). EIV 0.875 + 0.975 = 1.85; cost ≈ 3 h → **≈ 0.62 per hour**.
- **New row SR-b-Lean, SR-b1 (a)–(f):** finite metric and Cauchy–Schwarz facts plus one LP-free distance bound. Cheap. With Lean ×3 it is ≈ 1.0, as a side item in the next Lean round.
- **Rank (Lean aside):** C1 0.83 · C4 corrected run ≈ 0.8 · C12c-L / C12c-G′ / C3v2 P5² cut ≈ 0.78 · C12b-A ≈ 0.67 · SR-b2 ≈ 0.62 · PB test ≤ 0.52.
- **With Lean ×3:** C12c-L ≈ 2.35 · C9 ≈ 1.2 · C12b-Lean ≈ 1.0 · SR-b-Lean ≈ 1.0.
- **Next top-ranked route without Lean:** C1 (0.83).

## 8. Post-review corrections (appended 26 Nov 2026, about 10:35 ET, after `rnd/review_srb/HOSTILE_REVIEW_SRB.md`, PASS-WITH-FIXES; §§0–7 stand as written; where they conflict, this section governs)

Reviewer scripts and outputs are in `rnd/review_srb/`. The fork head read for the review is `a57f1f7`. ROUND10, its `selfref/` scripts and CORE.md are unchanged from `ac92ee2`.

### 8.1 H1: the diagnosis is narrowed to a uniform ratio requirement

- **What selects the disk is a uniform multiplicative (competitive-ratio) requirement over all horizons**: one design within a bounded *factor* of the best at every T. This is SR-b1(d)–(e). §0.1, §0.3, the §3 "Reading", the last row of §5 and §7 said "a uniform requirement over horizons (minimax or competitive)". That wording is withdrawn.
- **Minimax additive regret selects a polygon.** The criterion is max_T [J(D,T) − J*(T)] (Savage 1951).
  - The disk's regret is ≥ disk(2) − J*(2) = 1 − ½ = ½. J*(2) = ½ exactly: SR-b1(a) gives J* ≥ 1/T, and the hexagon attains ½.
  - For any n-gon the regret is ≤ max_T [J(n,T) − 1/T], computed from the exact curves (`review_srb/regret_check.out`). This gives ≤ 0.382 for the 10-gon, ≤ 0.358 for the 22-gon and ≤ 0.4987 for the 2400-gon. All are strictly below ½.
  - Label: **PIM**, a rigorous bound from SR-b1(a) plus exact finite DP values.
- **Minimax cost ties everything.** max_T J(D,T) = J(D,1) = 1 for every design, so it selects nothing (ELEMENTARY).
- **Direction.** SR-b1 proves only the **"if" direction** of ROUND10 §14's sentence, and only for the ratio criterion: under the ratio requirement, the disk is the only design that qualifies. It does not prove "only if", that no other criterion selects the disk. §0.1's "turns … into a proof" is withdrawn in favour of this.
- **Diagnosis (HYP, narrowed).** The continuum needs a chosen **scale-invariance across horizons**, the ratio form, not a worst case over horizons as such. It is a CHOSEN input, a form of U, not something the cost supplies.

### 8.2 M1: the constant in SR-b1(e)

- inf_D J(D,T) ≤ J(disk,T) ≤ π²/(4T), so **(e) J(n,T)/inf_D J(D,T) ≥ (4/π²)·d_min(n)·T → ∞**.
- The earlier "≥ d_min·T" would need inf_D J ≤ 1/T, which is the wrong direction. The conclusion that the ratio grows without bound is unchanged.

### 8.3 M2: the disk's equal-step path is optimal at every T (PIM, ELEMENTARY)

§3's "Not shown … Nothing above needs it" is withdrawn. §0.2, §4, §0.3 and the HYP all use T·sin²(π/2T) as the disk's cost, so they need it.

*Proof.*
- **Setup.** A T-tick pure path in the disk has angular steps φ_t ∈ [0, π] with Σφ_t ≥ π (circle metric), and it costs Σ g(φ_t), with g(φ) = sin²(φ/2) (M3a). g increases on [0, π], so shrinking steps lowers the cost; take Σφ_t = π.
- **(i) Every φ_t ≤ π/2.** g″ = (cos φ)/2 ≥ 0 there, so Jensen over the T slots (zeros allowed) gives Σg ≥ T·g(π/T).
- **(ii) Otherwise exactly one step φ₁ > π/2.** Jensen on the other T−1 steps gives cost ≥ h(φ₁) := g(φ₁) + (T−1)·g((π−φ₁)/(T−1)).
  - h′(φ₁) = ½[sin φ₁ − sin((π−φ₁)/(T−1))] ≥ 0 on [π/2, π], because (π−φ₁)/(T−1) ≤ π−φ₁ ≤ π/2 and sin is increasing on [0, π/2].
  - So h ≥ h(π/2), which is a configuration of case (i).
- **Hence** the disk optimum is exactly T·sin²(π/2T) for every T ≥ 1. ∎
- Consistent with ROUND10 M3b (numerical, T ≤ 10) and Lean `TransportHorizons` (T = 2, 4).

### 8.4 M3: extended sweep and corrected n-scaling

- **The grid.** §4's tail rows used, above n = 1001, only n ∈ {1400, 1600, 1800, 2000, 2001, 2400}. All are ≡ 0 mod 4 except 2001, yet the winners are almost always n ≡ 2 mod 4.
- **The rerun** (`review_srb/dpmix.c` → `mix_raw.txt` → `mix_analyze.out`) covers 1,497 even n from 400 to 99,186.
  - **Distance.** Closed form for even n: d(v₀,v_k) = sin(πk/n), divided by cos(π/n) when k − n/2 is odd.
  - **DP.** An exact monotone DP with the step at tick t capped at ⌊S/t⌋. The cap is exact by reordering steps from largest to smallest.
  - **Match.** It agrees with the LP-based `sr_b` curves for n = 6…2400 to < 1e−15.
  - **Sums.** The disk sums run to T = 4·10⁷.

| geometric q | disk | best n (interior?) | relative margin (polygon cheaper if +) |
|---|---|---|---|
| 0.99 | 0.0963215 | 962 (yes) | +1.76e−3 |
| 0.995 | 0.0564463 | 3366 (yes) | +5.33e−4 |
| 0.996 | 0.0473121 | 5042 (yes) | +3.62e−4 |
| 0.997 | 0.0375763 | 8058 (yes) | +2.19e−4 |
| 0.998 | 0.0270253 | 17278 (yes) | +1.07e−4 |
| 0.999 | 0.0152084 | 58788 (yes) | +3.07e−5 |
| 0.9995 | 0.0084553 | 99186 (edge) | −2.5e−6, not conclusive |

- **Uniform on 1..H:** a polygon is cheaper at H = 200, 500, 1000 (best n interior) and at H = 2000 (edge).
- **Restated results (OBSERVED):**
  - A polygon beats the disk at every geometric q ≤ 0.999 and every uniform H ≤ 1000 tested, with the best n inside the computed range.
  - The §4 rows at q = 0.996 and 0.997 ("not conclusive") are now polygon wins.
  - q = 0.9995 is the not-conclusive row.
  - **The SR-b prediction "the disk is selected for some q < 1" stays an open miss at every tested q.**
- **Withdrawn:** "best n ≈ 10/(1−q)" (§0.2, §5), a grid artifact. Observed n*·(1−q)² = 0.096, 0.084, 0.081, 0.073, 0.069 and 0.059 at q = 0.99 … 0.999. So **n* ≈ 0.06–0.1/(1−q)²** (OBSERVED).
- **Margin.** "∝ (1−q)²" is replaced by ≈ 4.3·(1−q)²·ln(1/(1−q)) (OBSERVED, fitted by eye; the coefficient of (1−q)² grows from 17.6 to 30.7 over the range).
- **HYP kept:** for every proper horizon distribution some polygon beats the disk; the disk is the limit of the selected designs, never the selection.
- **Heuristic scaling argument for the HYP** (not a proof):
  - From the exact curves (n = 8002), an even n-gon is cheaper than the disk by a relative ≈ 4/n at T ≲ 2√n, because its target sits 2π/n short of the antipode (§8.6).
  - It is more expensive by ≈ frac(1−frac)·4T²/n² at larger T, the cost of mixing step sizes, up to +12% near T ≈ 3n/8.
  - Take n ≈ α/(1−q)² and M = 1/(1−q). Against p(T), the gain integrates to ≈ 4·ln M/(αM²) and the loss to ≈ 2/(3αM²). The loss beyond saturation carries weight ≈ e^{−αM/2}. So the gain wins for every large M.
  - This matches n* ∝ M² and margin ∝ (1−q)²·ln M above.
- **Route to SR-b2.** Make the heuristic rigorous: an upper bound on J(n,T) from near-equal steps of the cheap parity, summed against p(T).

### 8.5 M4: the result depends on the target rule

- §1's task is M3h's rule: the target is **any perfectly distinguishable vertex** (d = 1). Every best polygon in §4 and §8.4 is even and uses a **non-antipodal** target (v_{n/2±1}), which this rule allows.
- ROUND10's M3c uses the antipode for even n.
- **Odd polygons only** (`review_srb/odd_only.out`; their targets are the same under both rules): a polygon still beats the disk at q = 0.5 … 0.99, with margins about 4× smaller (+5.5% at q = 0.5, +0.04% at q = 0.99; n ≤ 401 plus 601, 801, 1001, 2001).
- So the qualitative result does not depend on the rule for q ≤ 0.99; the numbers do. Beyond q = 0.99 only the M3h rule has been tested.

### 8.6 The (2T+2)-gon beats the disk at every T ≥ 2 (PIM, ELEMENTARY; under M3h's target rule only)

**Proposition SR-b3.** With all effects, cost J = Σd_t², and the target any perfectly distinguishable vertex: for every T ≥ 2, the regular (2T+2)-gon has J < T·sin²(π/2T), the disk's optimum (§8.3).

*Proof.*
- **Distances in an even n-gon (ELEMENTARY).** d(u,w) = max_θ ⟨u−w, θ⟩ / width_θ(P). For a regular n-gon of circumradius 1 and even n, the width is 2·cos(angle from θ to the nearest vertex direction).
  - So d(v₀,v_k) = sin(πk/n) when the chord v₀v_k is parallel to a vertex direction (k − n/2 even), and sin(πk/n)/cos(π/n) when it is parallel to an edge normal (k − n/2 odd).
  - Also checked: these closed forms reproduce the LP-based curves exactly (§8.4) and M3g's ratios (1.1547, 1.0824, 1.0515).
- **Target.** Let n = 2T+2. For k = n/2 − 1 = T, the chord has length 2cos(π/n) and is parallel to an edge normal, so d(v₀,v_T) = 1. v_T is perfectly distinguishable from v₀.
- **Path.** T unit steps v₀ → v₁ → … → v_T cost T·u², with u = sin(π/n) if n/2 is odd and u = tan(π/n) if n/2 is even. In both cases u ≤ tan x with x = π/(2T+2).
- **Comparison.** Let y = π/(2T) > x. Use tan x ≤ x/(1 − x²/2) and sin y ≥ y − y³/6. Then tan x < sin y follows from T/(T+1) < (1 − y²/6)(1 − y²/2), which holds if π²(T+1) < 6T². That is true for every T ≥ 3. At T = 2 the hexagon gives 0.5 < 1. ∎
- **Exact check:** 40-digit arithmetic for T = 2…200,000 (`review_srb/thm_2T2.py`). The relative margin is ≈ 2/T.
- **Scope.** This turns ROUND10 §14's HYPOTHESIS "J does not select the disk at every finite horizon" into PIM **under M3h's rule only**. Under the mixed convention (antipode for even n, any distinguishable vertex for odd n) it stays HYP, resting on the (2T+1)-gon (OBSERVED, T ≤ 20).
- It also explains §4's observations n* ≈ 2T and "the best polygon at T is even".
- **Is it known?** The polygon GPT models are KNOWN (Janotta et al. 2011, below). I did not find this transport comparison stated; "not found" is not "new". ELEMENTARY.

### 8.7 Friday-cleanup note for Ace: ROUND10 §14's two target rules (flag only; ROUND10 not edited)

- **The text.** ROUND10 §14 "Gentle transport" says "An even polygon never beats the disk, and the 4T-gon ties it (PROVED (in-model))". It also says "Odd polygons beat it (OBSERVED (numerical))".
- **The code uses different targets.** `m_round10b.py` `poly_opt` (M3c) scores the **antipode only** (`best[n//2]`; n ≤ 24, T ≤ 5). `m_round10b_poly.py` and `m_round10b_poly_ext.py` (M3h) score **any vertex with d = 1**, odd n only.
- **Under the task as worded** ("move a record to a perfectly distinguishable partner"), the even-polygon statement is false at T = 2. The hexagon's v₀ → v₁ → v₂ costs ¼ + ¼ = 0.5 against the disk's 1.0, and 0.5 against 0.75 at T = 3.
- **"PROVED (in-model)" for the even-polygon statement.** The M3c support visible in the repo is numerical for n ≤ 24, T ≤ 5, and §14's "Not formalized" list includes the transport costs.
- **Under M3h's rule,** §8.6 makes "J does not select the disk at every finite horizon" PIM.
- **Decision for Ace:** which target rule is intended, and the matching wording and label for that bullet.
- The phrase "13 strict wins + 1 tie" (§0.4) was this note's paraphrase of ROUND10's sentence, not repo text.

### 8.8 M5: prior art (DOIs resolved on Crossref this session: `review_srb/crossref_review.txt`)

- **Closest: contract versus interruptible (anytime) algorithms.**
  - Zilberstein & Russell 1996, *Artificial Intelligence* 82:181–213, doi 10.1016/0004-3702(94)00074-3.
  - Zilberstein, Charpillet & Chassaing 2003, *Ann. Math. Artif. Intell.* 39:1–18, doi 10.1023/A:1024412831598.
  - KNOWN: a contract algorithm needs its horizon fixed in advance, and an interruptible one must serve every horizon. Doubling schedules reach a constant acceleration ratio of 4 at every deadline, and 4 is optimal. The 2003 paper treats the deadline with or without stochastic information.
  - That is the template for §8.1's split: a worst-case *ratio* over horizons versus a Bayes prior over the horizon. It replaces Luby–Sinclair–Zuckerman as the closest analogy.
  - Read: the IJCAI 1999 text and summaries; the AI 1996 full text was not read.
- **Savage 1951**, *JASA* 46:55–67, doi 10.1080/01621459.1951.10500768: minimax regret, the criterion in §8.1 that selects a polygon.
- **Nulton, Salamon, Andresen & Anmin 1985**, *J. Chem. Phys.* 83:334–338, doi 10.1063/1.449774, "Quasistatic processes as step equilibrations": the K-step (discrete) counterpart of the L²/τ bound. It is the closer credit for SR-b1(a)'s discrete Cauchy–Schwarz form. Its exact constant was not reread; read it before quoting the form.
- **Janotta, Gogolin, Barrett & Brunner 2011**, *NJP* 13:063024, doi 10.1088/1367-2630/13/6/063024: regular-polygon GPT models, with the disk as their limit (the menu).
- The five DOIs in §2 re-resolve.

### 8.9 Low findings

- **L1.** The repo head in the header was `ac92ee2`. The review read `a57f1f7`, and the relevant files are unchanged.
- **L2.** SR-b1(b): d_min(n) := min_{j≠0} d(v₀,v_j), as in the proof. For even n the minimum is at j = 1 (closed form, §8.6: tan(π/n) < sin(2π/n) for n > 4). For odd n this is OBSERVED.
- **L3.** §0.4's "understates polygon wins" is reworded. The horizon count does not change: T = 1 is a tie for every design, and T = 2…12, 16, 20 were already wins. What changes is the margin and which polygon wins (even, the (2T+2)-gon).
- **L4.** In the §4 table, "a larger n can only lower the polygon cost" is reworded: the minimum over a *larger set* of n can only be lower. A single larger n can be more expensive.
- **L5.** "No price in the repository selects the disk" is scoped to the two prices in ROUND10 §14: κ per affine dimension and the log₂|G| map memory.

### 8.10 Labels (governs §5 where they conflict)

| claim | label |
|---|---|
| SR-b1(a), (b), (c), (f) | PIM (unchanged; (b) with d_min = min_{j≠0}; (a) discrete credit Nulton et al. 1985) |
| SR-b1(d)–(e), only the disk is within a bounded factor at every horizon | PIM, with (e)'s constant 4/π² |
| Disk equal-step path optimal at every T | PIM (ELEMENTARY, §8.3) |
| Additive minimax regret selects a polygon; minimax cost ties | PIM (rigorous bound from exact DP values); ELEMENTARY |
| SR-b1 versus ROUND10's sentence | PIM for the "if" direction, ratio criterion only |
| Diagnosis: the continuum needs a uniform ratio (scale-invariant) requirement over horizons | HYP (narrowed; a chosen input, a form of U) |
| A polygon beats the disk under geometric q ≤ 0.999 and uniform H ≤ 1000 (M3h's rule) | OBSERVED (best n interior); q = 0.9995 not conclusive |
| The same with odd polygons only, q ≤ 0.99 | OBSERVED |
| A polygon beats the disk under every proper horizon distribution | HYP (heuristic scaling argument, §8.4) |
| n* ≈ 0.06–0.1/(1−q)²; margin ≈ 4.3(1−q)²ln(1/(1−q)) | OBSERVED (by eye); "n* ≈ 10/(1−q)" withdrawn |
| Proposition SR-b3: the (2T+2)-gon beats the disk at every T ≥ 2 | PIM (ELEMENTARY), M3h's rule only |
| ROUND10 M3c/M3h target-rule mismatch | OBSERVED (text and code); flagged for Ace (§8.7) |
| "The disk is selected for some q < 1" | open miss at every tested q |

### 8.11 Rescore (§13 scale; reviews and sunk cost not scored)

- **SR-b2, the all-q analytic statement.**
  - The disk did not win at any interior q up to 0.999, and §8.4 gives a concrete route.
  - p_hit 0.35 → **0.5**, V_hit 2.5 (it would turn "never the selection" into PIM). p_miss 0.5, V_miss 1.5 (a bound that fails to close, or a disk win at q > 0.999).
  - EIV = 1.25 + 0.75 = 2.0. Cost ≈ 3 h → **≈ 0.67 per hour** (was 0.62).
- **SR-b-Lean**: SR-b1(a)–(f) plus §8.3 and SR-b3. These are finite trigonometric and Cauchy–Schwarz facts, still cheap. ≈ 1.0 with Lean ×3, as a side item in the next Lean round.
- **Rank (Lean aside):** C1 0.83 · C4 corrected run ≈ 0.8 · C12c-L / C12c-G′ / C3v2 P5² cut ≈ 0.78 · SR-b2 ≈ 0.67 · C12b-A ≈ 0.67 · PB test ≤ 0.52.
- **With Lean ×3:** C12c-L ≈ 2.35 · C9 ≈ 1.2 · C12b-Lean ≈ 1.0 · SR-b-Lean ≈ 1.0.
- **Next top-ranked route without Lean:** C1 (0.83), in progress in `C1.md` by another worker.

## 9. SR-b4: a scale-free (log-uniform) horizon weighting (appended 26 Nov 2026, about 11:05 ET; §§0–8 stand; local note only, not committed)

### 9.0 SR-b4 pre-statement (written before any SR-b4 number was computed; hash of SR_B.md before this section: `061c1d54…a16c`)

**Hypothesis under test (HYP, from the parent brief).** The "stake" for a record is having no built-in timescale. Formally: a scale-free horizon weighting, equal weight per doubling of T (density ∝ 1/T), which is improper on [1, ∞). Question: does the disk win under it? Same menu, task, cost and target rule as §1 (M3h's rule: any perfectly distinguishable vertex).

**Definitions.**
- J*(T) := inf over the menu of J(D, T). Known: 1/T ≤ J*(T) ≤ J(disk, T) = T·sin²(π/2T) (SR-b1(a), §8.3).
- ρ(D, T) := J(D, T)/J*(T) ≥ 1, the per-horizon competitive ratio (dimensionless, so a change of time unit T → cT leaves it and the measure dT/T unchanged).
- L_H := Σ_{T=1}^{H} 1/T.
- **Primary quantity:** R_H(D) := (1/L_H) Σ_{T=1}^{H} ρ(D, T)/T, the log-uniform average of the competitive ratio over T ∈ [1, H], studied as H → ∞.
- Regret form: S_H(D) := L_H·(R_H(D) − 1) = Σ_{T≤H} (ρ(D,T) − 1)/T. At each H it has the same argmin as R_H, so it is a reporting variant, not a second criterion.
- Secondaries (reported, not decisive): (S1) raw log-uniform cost C_H(D) := Σ_{T≤H} J(D,T)/T; (S2) disk-referenced ratio, ρ replaced by J(D,T)/J(disk,T).

**Why this primary.** SR-b1(d)–(e) selected the disk with sup_T ρ(D,T), the worst case of this same ratio. Averaging ρ with the scale-invariant measure dT/T is the Bayes (averaged) counterpart of exactly that criterion, so R_H isolates the question "is it the *ratio* plus *scale-freeness* that selects the disk, or the *worst case*?" The raw cost J is not scale-free (J ~ 1/T), so (S1) weights the first few horizons far more than later doublings and is not the hypothesis as stated.

**Two ways to take the improper limit, fixed in advance.**
- **(F) fixed design, then H → ∞:** compare lim_H R_H(D) across fixed designs D.
- **(P) per-H selection, the primary:** at each H, the selected design is argmin_D R_H(D) over the menu (the truncated log-uniform prior on [1, H] is proper); then ask what happens as H → ∞. Polygon families n(H) chosen per H are allowed, as the brief says.

**Triviality check, done on paper before computing.**
- **(F) is decided by SR-b1(e) and is trivial.** For a fixed n-gon, ρ(n,T) ≥ (4/π²)·d_min(n)·T (§8.2), so R_H(n) ≥ (4/π²)·d_min(n)·(H/L_H) → ∞. The disk has ρ ≤ π²/4 at every T, so R_H(disk) ≤ π²/4. The disk therefore beats every fixed polygon in (F). This is the polygon floor d_min > 0 again; scale-freeness does no work. (A uniform weighting on 1..H, or geometric with q → 1 at fixed n, gives the same: a fixed polygon's average tends to J(n, ∞) > 0 while the disk's tends to 0.) (F) is reported as a restatement, not as a test.
- **(P) is the non-trivial version and the one tested.**

**Rules for (P).**
- **HIT:** there is H₀ with R_H(disk) < R_H(n) for every polygon n and every H ≥ H₀ (the disk strictly best at every large H), or a proof of that.
- **MISS:** for every H ≥ 2 (proved), or for every tested H with the best n strictly inside the computed range (observed), some polygon n(H) has R_H(n(H)) < R_H(disk).
- **OPEN:** neither, including any tested H whose best n is at the edge of the computed range or whose sign is not stable under the convergence checks below.
- In (P) both R_H(disk) and R_H(n(H)) may tend to the same limit; a tie in the limit is not a HIT (the HIT needs strict per-H preference).

**Convergence and robustness criteria for (P).**
1. J*(T) is only computable as a minimum over a finite design set, an upper bound on the true J*. The sign of R_H(disk) − R_H(n) is a positively weighted sum Σ w(T)[J(n,T) − J(disk,T)] with w(T) = 1/(T·J*(T)). A reported sign counts only if it is unchanged under (i) doubling the n-set used for J*, and (ii) replacing w by each of the two bracketing weights 1/(T·J(disk,T)) and 1 (from 1/T ≤ J* ≤ J(disk,T)). If J(n,T) ≤ J(disk,T) at every T ≤ H with strict inequality somewhere, the sign is fixed for every positive weight and the J* issue is moot.
2. The best n must be interior to the computed n-range for an observed MISS.
3. Disk values are closed form (§8.3), exact at every finite H.

**Prediction stated before computing (so the outcome is not a surprise claimed later).** A paper argument, not yet checked: if n is even with n/2 − 1 divisible by every T ≤ H, the equal-step path to the target v_{n/2−1} is cheaper than the disk at every T in [2, H], which would make (P) a MISS for every H by pointwise dominance, independent of the weighting. I expect MISS with probability ≈ 0.8. **Not known beforehand:** whether the argument survives an exact check, whether a *generic* n (not an lcm construction) also dominates, the best n and margin scaling with H, and whether (S1)/(S2) agree. If the dominance holds, (P) is decided for **every** horizon prior with bounded support, so its MISS is again close to trivial; that will be said plainly.

### 9.1 Result (computed after §9.0 was written; scripts and outputs in `sr_b4/`)

**Short answer: no. Under the scale-free weighting the disk is not selected at any finite horizon cut-off H. It wins only if the design is fixed before H → ∞, and that version is decided by SR-b1(e) alone.**

- **(P), the primary: MISS, proved in-model for every H ≥ 2** (under M3h's target rule), by Proposition SR-b4 below. It is a pointwise-dominance result, so it holds for the log-uniform R_H, the regret S_H, both secondaries, and in fact **every** horizon weighting with bounded support. The scale-free weighting does no work at finite H.
- **(F), fixed design then H → ∞: the disk wins, trivially** (§9.0: R_H(n) ≥ (4/π²)·d_min(n)·H/L_H → ∞, R_H(disk) ≤ π²/4). The same holds for a uniform weighting or geometric q → 1 at fixed n, so this is not a property of scale-freeness either.
- **In the limit both tie.** R_H(disk) → 1 is observed (R_H(disk) − 1 = 0.33 at H = 2, 0.19 at H = 400, falling like ~1.2/L_H), and the per-H winners n(H) → ∞ have R_H(n(H)) < R_H(disk). The strict-HIT rule of §9.0 is not met.
- So the SR-b4 hypothesis "no built-in timescale selects the disk" is an **open miss** for (P). What the miss names is the same as §8.1: the disk appears only when **one design must be fixed before the horizon scale is known**, the quantifier order "design, then all scales", which is the uniform-over-horizons requirement again.

### 9.2 Proposition SR-b4 (PIM, ELEMENTARY; M3h's rule; generalizes SR-b3)

**Statement.** Let n be even, S = n/2, and let T ≥ 2 divide S − 1. Then J(n, T) < T·sin²(π/2T) = J(disk, T). Hence for every H ≥ 2 and m ≥ 1, the even n-gon with **n = 2(1 + m·lcm(1, …, H))** is strictly cheaper than the disk at every T ∈ [2, H] and ties it at T = 1 (all designs cost 1 there).

*Proof.*
- **Target.** d(v₀, v_{S−1}) = sin(π(S−1)/n)/cos(π/n) = cos(π/n)/cos(π/n) = 1 (closed form of §8.6, k − S = −1 odd). So v_{S−1} is a valid target.
- **Path.** Let k = (S−1)/T. T equal jumps of k vertices reach v_{S−1}; by rotation symmetry each costs d(v₀, v_k)². With x = π/(2T) and y = πk/n = x(1 − 2/n), d(v₀, v_k) ≤ sin(y)/cos(π/n) (the worse parity).
- **Comparison.** sin is concave on [0, π], so sin(y) = sin(x − 2x/n) ≤ sin x − (2x/n)·cos x. It suffices that sin x − (2x/n) cos x < cos(π/n)·sin x, i.e. 1 − cos(π/n) < (2/n)·x·cot x.
  - Left side ≤ π²/(2n²). For T ≥ 2, x ≤ π/4, and x·cot x is decreasing on (0, π/2), so the right side ≥ (2/n)(π/4) = π/(2n).
  - π²/(2n²) < π/(2n) ⇔ n > π, true for every even n ≥ 6 (the smallest case, S − 1 = 1·T, T = 2, is n = 6). ∎
- **Corollary (PIM).** For any weights w(T) ≥ 0 on T ∈ [1, H] with some w(T) > 0 at T ≥ 2, Σ w(T)·J(n_H, T) < Σ w(T)·J(disk, T). This covers R_H and S_H for any value of J* (they are such sums with w(T) = 1/(T·J*(T))), C_H, the disk-referenced ratio, uniform-on-1..H, and truncated geometric mixtures.
- **What it settles in SR-b2.** The §8.4 HYP "every proper horizon distribution selects a polygon" is now **PIM for every distribution with bounded support** (M3h's rule). It is **still HYP for unbounded support** (geometric), because each polygon loses to the disk beyond saturation (SR-b1(f)); the OBSERVED rows of §8.4 stand.
- **Checks.**
  - Exact DP (`sr_b4/dp4.c`, the §8.4 DP) for H = 2…12, m = 1, 2 (n up to 110,882): cheaper at every T ∈ [2, H]; minimum relative margin ≈ π/n, at T = 2 (`lcm_check.out` (A1)).
  - The explicit path cost in 50-digit arithmetic for H = 2…40, 50, 60, 70, 80 (n up to ≈ 6.5·10³⁴): cheaper at every T; n·(min relative margin) → 3.1416 (`lcm_check.out` (A2)).
  - **By hand / independent:** LP-computed distances (no closed form) and brute-force enumeration of every vertex sequence (no DP, no step cap) for n = 6, 14, 26 at T ≤ 2, 3, 4. They agree with the DP to 1e−15 (`hand_check.out`). Example, n = 14: J = 0.77748 and 0.59419 at T = 2, 3, against the disk's 1 and 0.75. H = 2 by hand: J*(1) = 1, J*(2) = ½, so R_2(disk) = (1 + 2/2)/(3/2) = 4/3 and R_2(hexagon) = 1.
- **The lcm is not needed (OBSERVED).** For generic even n, the polygon is cheaper than the disk at every T ∈ [2, T₀(n)] with T₀(n)/√n between 1.995 and 2.161 for all 96 tested n from 1,000 to 40,000 (both residues mod 4; `t0_scan.out`). So n ≈ H²/4 already dominates on [2, H]. This matches §8.4's heuristic gain region T ≲ 2√n.

### 9.3 Numerics for (P): best n and margins (OBSERVED; `sr_b4/srb4_analyze.out`)

- **Data.** Exact J(n, T), T ≤ 400, for every even n ≤ 4000 and a ~2% grid of even n to 64,000 (2,279 curves, `curves_even.npy`), plus the odd n ≤ 401 of `sr_b/srb_all.json`.
- **J*.** The minimum over all of these and the disk. Checks: min_T T·J*(T) = 1.000 (SR-b1(a) holds); T·J* = 2.418 at T = 100 and 2.455 at T = 400 (→ π²/4 = 2.467 from below, as §4); argmin n = 2T + 2 at every listed T. **Convergence:** halving the n-set used for J* (even n ≤ 2000) changes J* by 0.0 at every T ≤ 400.

| H | R_H(disk) | best n | R_H(best) | margin (polygon cheaper if +) | interior |
|---|---|---|---|---|---|
| 2 | 1.3333 | 6 | 1.0000 | +0.333 | yes |
| 10 | 1.3540 | 14 | 1.1899 | +0.164 | yes |
| 50 | 1.2635 | 86 | 1.2405 | +2.30e−2 | yes |
| 100 | 1.2323 | 362 | 1.2261 | +6.27e−3 | yes |
| 200 | 1.2067 | 1122 | 1.2049 | +1.80e−3 | yes |
| 400 | 1.1857 | 3842 | 1.1852 | +4.95e−4 | yes |

- **Robustness (criterion 1 of §9.0).** At all 17 H values from 2 to 400 the sign is "polygon cheaper" under J* from the halved n-set, under w = 1/(T·J(disk,T)) (S2), under w = 1/T (raw log-uniform, S1) and under w = 1 (uniform). All best n are interior.
- **The per-H winner is not the dominating polygon.** At H = 5, 6 and every tested H ≥ 10 the best n does not beat the disk at every T ≤ H; it trades a small loss at large T for a gain at small T. n*/H² falls from 0.14 (H = 10) to ≈ 0.024–0.028 (H = 200–400), and n*·ln n*/H² ≈ 0.16–0.21 for H ≥ 100. So n* ≈ 0.2·H²/ln H (fitted by eye). Margin·H² grows slowly, 16 → 79 over H = 10 … 400. Compare §8.4, geometric: n* ≈ 0.06–0.1/(1−q)².
- **Odd polygons only** (`odd_only.out`; their target is the same under M3c's and M3h's rules): a polygon wins at H = 2…100 (best n interior). At H = 150 and 200 the best odd n is at or near the top of the computed range (401), where the disk is cheaper. **Not conclusive (OPEN)**; it needs odd n in the thousands. Under the mixed target convention, SR-b4's proof does not apply, so (P) there is OBSERVED for H ≤ 100 only.

### 9.4 Short analytic picture (heuristic, not a proof)

- With w(T) ≈ 1/(T·J*(T)) ≈ (4/π²) for large T, R_H(disk) − R_H(n) ≈ (1/L_H)·Σ_T (relative gain or loss at T)/T.
- Gain: ≈ 4/n relative (π/n at T = 2) for T ≲ 2√n, contributing ≈ (c/n)·ln n.
- Loss: from mixing step sizes, ≈ (2/3)T²/n² relative for 2√n ≲ T ≤ H (§8.4), contributing ≈ H²/(3n²).
- Optimizing c·ln n/n − H²/(3n²) gives n* ∝ H²/ln n* and a margin ∝ ln H/H², positive at every H. This agrees in form with §9.3, which is all that is claimed.
- The heuristic says why scale-freeness does not help. Equal weight per doubling still puts finite total weight on the region where the polygon is cheaper, and at any finite H a large enough polygon is cheaper there and everywhere else up to H.

### 9.5 Hostile self-review: genuine selection or restatement?

- **(P) is close to trivial.** Its MISS follows from a pointwise statement (SR-b4), so the scale-free weighting is irrelevant at every finite H. The test could not have come out as a HIT under any bounded-support weighting once SR-b4 holds. The pre-statement predicted this (p ≈ 0.8) from the same paper argument, so the computed outcome is confirmation, not discovery. The genuinely new item is SR-b4 itself, which closes SR-b2 for bounded support.
- **(F) is a restatement.** Its HIT for the disk uses only d_min(n) > 0. It holds for uniform weighting as H → ∞ and for geometric q → 1 at fixed n too, so it is not a property of scale-freeness. In this menu, "the design is fixed before the horizon scale" picks the same design as SR-b1's sup-ratio criterion (the only design with bounded ρ). It is the competitive requirement in another form, not an independent selection. It is not proved equivalent to it outside this menu.
- **The improper prior itself decides nothing.** The two orders of limit, (P) and (F), give opposite answers. The answer is set by which limit one chooses, which is a chosen input (KNOWN in kind for improper priors: Dawid, Stone & Zidek 1973; Kass & Wasserman 1996, below). The choice "design first" is the uniform requirement U again.
- **Weak points.**
  - Everything is under M3h's target rule. Under the antipode rule for even n, SR-b4's path does not exist (its gain comes from the target sitting 2π/n short of the antipode), and only the odd-only rows apply (OBSERVED, H ≤ 100).
  - Only regular polygons and the disk are in the menu (§6).
  - J*(T) is the minimum over the computed set. The sign does not depend on it (§9.2 corollary; §9.3 robustness), but the R_H values do.
  - R_H(disk) → 1 rests on T·J*(T) → π²/4, which is OBSERVED, not proved (SR-b1 gives only 1 ≤ T·J* ≤ π²/4).
  - n* and margin scalings are fits by eye over H ≤ 400.
- **What would change the result.** A natural criterion in which the design must be chosen before H, but is still Bayesian (for example, a single design scored by lim sup_H of its R_H regret relative to the per-H best). It would select the disk iff it is not dominated in the limit, and that is again (F)'s quantifier order. No such criterion is supplied by the cost.

### 9.6 Prior art (DOIs resolved on Crossref this session: `sr_b4/crossref_srb4.txt`)

- **Scale-invariant priors.**
  - Jeffreys 1946, *Proc. R. Soc. A* 186:453–461, doi 10.1098/rspa.1946.0056: the invariant prior, which for a scale parameter is ∝ 1/σ.
  - Jaynes 1968, *IEEE Trans. Syst. Sci. Cybern.* 4:227–241, doi 10.1109/TSSC.1968.300117: transformation-group arguments for the same 1/σ prior.
  - KNOWN: dT/T is the standard "no built-in scale" prior, and it is improper. §9.0 uses it as such and claims nothing new about it.
- **Unknown durations.** Gott 1993, *Nature* 363:315–319, doi 10.1038/363315a0: reasoning about a duration with no preferred scale (the Copernican "delta t" argument). Cited as the nearest use of a scale-free prior on a horizon-like quantity, an analogy only.
- **Improper priors and limits.**
  - Dawid, Stone & Zidek 1973, *JRSS B* 35:189–213, doi 10.1111/j.2517-6161.1973.tb00952.x: conclusions from improper priors can depend on how the limit is taken (marginalization paradoxes).
  - Kass & Wasserman 1996, *JASA* 91:1343–1370, doi 10.1080/01621459.1996.10477003: a review of formal-rule priors, including improper ones as limits of proper ones and their pitfalls.
  - These are the KNOWN background for §9.5's "the order of limits decides"; the particular (P)/(F) split here is ELEMENTARY.
- **Anytime algorithms (deadlines with no fixed scale).**
  - Zilberstein & Russell 1996, *Artificial Intelligence* 82:181–213, doi 10.1016/0004-3702(94)00074-3, and Zilberstein, Charpillet & Chassaing 2003, *Ann. Math. Artif. Intell.* 39:1–18, doi 10.1023/A:1024412831598 (both already in §8.8).
  - KNOWN there: the interruptible (every-deadline) guarantee is a worst-case ratio over deadlines met by doubling schedules (ratio 4); the 2003 paper treats deadlines with and without a distribution. In that template, "no built-in timescale" is enforced by the every-deadline ratio, not by a scale-free prior. This matches §9.5. Their full texts were not reread this session.
  - Not cited: a Zilberstein 1996 *AI Magazine* DOI (10.1609/aimag.v17i3.1232) that did **not** resolve on Crossref.
- **Not found:** the SR-b4 dominance construction in the GPT literature (Janotta et al. 2011, §8.8, is the menu). "Not found" is not "new"; it is ELEMENTARY.

### 9.7 Labels (SR-b4)

| claim | label |
|---|---|
| (F): the disk beats every fixed polygon under the log-uniform ratio as H → ∞ | PIM (from SR-b1(e)); trivial, a restatement of the fixed-design / uniform requirement |
| Proposition SR-b4: n = 2(1 + m·lcm(1..H)) beats the disk at every T ∈ [2, H] | PIM (ELEMENTARY), M3h's rule only; checked exactly (DP, 50-digit, brute force) |
| (P): a polygon beats the disk under R_H at every H ≥ 2 | PIM (corollary of SR-b4), M3h's rule |
| Every bounded-support horizon distribution selects a polygon (SR-b2 for bounded support) | PIM, M3h's rule |
| The same for unbounded support (geometric) | HYP (unchanged; §8.4 OBSERVED rows stand) |
| Generic even n dominates on [2, T₀], T₀ ≈ 2.0–2.16·√n | OBSERVED (n = 1,000…40,000) |
| Per-H best n ≈ 0.2·H²/ln H; margin ∝ ~ln H/H² | OBSERVED (fits by eye, H ≤ 400) + heuristic (§9.4) |
| R_H(disk) → 1, so (P)'s limit is a tie | OBSERVED (rests on T·J* → π²/4, OBSERVED) |
| Odd polygons only: polygon wins under R_H for H ≤ 100 | OBSERVED; H ≥ 150 OPEN (range edge) |
| "No built-in timescale is the stake that selects the disk" | **open miss** for (P); for (F) it holds only as a restatement of the design-first quantifier order (a form of U) |

### 9.8 Rescore (§13 scale)

- SR-b4 is done: the V_miss branch, with one PIM proposition. SR-b2 shrinks to the **unbounded-support** case only (geometric and other heavy-tailed mixtures). There, the loss beyond saturation must be bounded against a tail weight; §8.4's route is unchanged.
- SR-b2 (unbounded support): p_hit 0.5, V_hit 2.0 (smaller than before, since bounded support is now closed). p_miss 0.5, V_miss 1.0. EIV 1.5 over ≈ 3 h → **≈ 0.5 per hour** (was 0.67).
- SR-b-Lean gains SR-b4, which is concavity plus closed-form distances and cheap; still ≈ 1.0 with Lean ×3.
- No change to the other ranks in §8.11.

## 10. Review fixes (governs §9)

*Appended 26 Nov 2026, about 11:36 ET, after `rnd/review_srb4/HOSTILE_REVIEW_SRB4.md`, PASS-WITH-FIXES, no H findings. §§0–9 stand as written; where they conflict, this section governs. Reviewer scripts and outputs are in `rnd/review_srb4/`. SR-b4's own scripts were not edited. The six new DOIs in §10.4 were re-resolved on Crossref this session: `sr_b4/crossref_srb4_review.txt`.*

The review re-derived Proposition SR-b4 by hand, checked each step of the proof chain at 60 digits, reproduced the §9.3 table to 10 digits with independent distances and DP, and confirmed the (P) open miss and the (F) restatement. Four M findings and six L findings follow.

### 10.1 M1: the odd-only rows of §9.3 mix two target rules

- `sr_b4/odd_only.py` scores odd polygons only, whose target is the same under both rules. But its J*, the denominator of ρ and so the weights of R_H, is the minimum over the **M3h even curves** (`curves_even.npy`, targets v_{S−1} and v_S) plus odd n.
- Under the mixed convention, which is the reason for an odd-only run, even polygons have the antipode as their only target, and J* is then larger at small T: T·J*(2) = 1.528 instead of 1.0 (`rv_RH_large.out`).
- So the §9.3 odd-only R values are a hybrid, and the sentence "Under the mixed target convention … (P) there is OBSERVED for H ≤ 100 only" was not computed under that convention. Nothing else in `sr_b4/` mixes the rules: the main §9.3 table is consistently M3h.
- **Recomputed under the mixed-rule J*** (`rv_RH_large.out`; odd n ≤ 999 plus 1121, 2305, 3841). Every sign is unchanged for H ≤ 300, and the margins are about 25% smaller:

  | H | R_H(disk), mixed J* | best odd n | mixed-rule margin | M3h-J* margin (same sample) |
  |---|---|---|---|---|
  | 2 | 1.1030 | 5 | +1.03e−1 | +1.57e−1 |
  | 10 | 1.1405 | 17 | +4.59e−2 | +6.15e−2 |
  | 50 | 1.1078 | 181 | +4.08e−3 | +5.39e−3 |
  | 100 | 1.0954 | 757 | +1.20e−3 | +1.55e−3 |
  | 150 | 1.0891 | 1121 | +5.27e−4 | +7.14e−4 |
  | 200 | 1.0850 | 2305 | +3.47e−4 | +4.36e−4 |
  | 300 | 1.0798 | 3841 | +1.31e−4 | +1.81e−4 |
  | 400 | 1.0765 | 3841 | −6.54e−5 | −1.81e−5 |

- **§9.3's OPEN rows at H ≥ 150 are superseded.** Those used odd n ≤ 401, with the best n at the edge of that range and the disk cheaper. In the reviewer's larger sample an odd polygon beats the disk at H = 150, 200 and 300. This holds under all five weights: mixed-rule J*, M3h J*, 1/(T·J(disk,T)), 1/T and 1 (`rv_odd_robust.out`). These are existence results; at H = 150–300 the best odd n is a sampled spot point, so "interior" is not claimed. At H = 400 no odd n in that sample wins under the primary weights (OPEN for that H).
- Under the mixed rule, even polygons scored at the antipode do not beat the disk (margins zero or negative at every listed H ≥ 2).

### 10.2 M2: odd analogue of SR-b4 (reviewer's; PIM-candidate)

- **Claim.** Let n be odd, n ≥ 5, S′ = (n−1)/2, and let T ≥ 2 divide S′. Then J(n, T) < T·sin²(π/2T). The target v_{S′} has d = 1 under both M3c's and M3h's rules.
- **Corollaries claimed:** the (2T+1)-gon beats the disk at every T ≥ 2; n = 1 + 2m·lcm(1..H) beats the disk at every T ∈ [2, H].
- The proof and the checks (breakpoint distances at 60 digits, DP for H = 2…9) are in the review, §M2 and `rv_odd_lemma.out`. They are **not** adopted here.
- **Label: PIM-candidate**, under its own separate review (`rnd/review_srb4_odd/`, running now). **No label in §9.7 or below is upgraded until that review passes.** If it passes, the (P) open miss and "SR-b2 for bounded support" would hold under both target rules, and the first weak point of §9.5 would go away. That is recorded as a prospect only.

### 10.3 M3: §9.0's ordering is not independently verifiable

- The hash `061c1d54…a16c` reproduces as the SHA-256 of SR_B.md lines 1–265 (all of §§0–8, with trailing newline). So §§0–8 were not changed after the hash was taken. It does not commit to the wording of §9.0 itself, and no backup copy or independent timestamp of §9.0 exists on the box (SR_B.md was last written after every numerical output, which is expected for §§9.1–9.8 but erases when §9.0 was written). The WORKLOG line for SR-b4 is at 11:19 ET, after the results.
- There is no sign of post-hoc editing: §9.0 contains no numbers, and its prediction is the lcm argument that the proof later confirmed. The (P) outcome is now a proof and does not rest on the pre-statement.
- **Addendum to §9.0:** the ordering is not independently verifiable on the box.
- **Process fix, adopted from here on:** before any computation, log the pre-statement block's own full SHA-256 and the time in the WORKLOG. Better still, lock the block to the fork, as the process rule already requires for preregs.

### 10.4 M4: added prior art, and the near-Bayes reading of (F)

DOIs re-resolved on Crossref this session (`sr_b4/crossref_srb4_review.txt`); titles, authors, venues, years, volumes and pages match. The review noted that two other DOIs, guessed earlier for Caves and Stone, resolve to different items and must not be used; they are not used here.

- **Limits of Bayes rules / extended Bayes** (the KNOWN frame for (P) versus (F)):
  - Blyth 1951, *Ann. Math. Stat.* 22:22–42, doi 10.1214/aoms/1177729690.
  - Heath & Sudderth 1978, *Ann. Stat.* 6:333–345, doi 10.1214/aos/1176344128, on finitely additive (improper) priors and extended admissibility.
- **Improper-limit dependence:** Stone 1976, *JASA* 71:114–116, doi 10.1080/01621459.1976.10481490, "Strong inconsistency from uniform priors". It sits beside Dawid, Stone & Zidek 1973 (§9.6).
- **Gott's argument has a published critique:** Caves 2000, *Contemp. Phys.* 41:143–153, doi 10.1080/001075100181105. Cited next to Gott 1993, which stays as an analogy only.
- **Contract scheduling:** López-Ortiz, Angelopoulos & Hamel 2014, *JAIR* 51:533–554, doi 10.1613/jair.4360, on optimal schedules and acceleration ratios. It is the modern reference for the interruptible-ratio template §9.6 cites from Zilberstein.
- **Horizon uncertainty in online allocation:** Balseiro, Kroer & Kumar 2023, SIGMETRICS abstract, doi 10.1145/3578338.3593559 (arXiv 2206.13606).
  - KNOWN there: no algorithm has a constant competitive ratio without a bounded horizon window, and the ratio degrades with ln(τ₂/τ₁).
  - An analogy for "the uniform-ratio requirement needs the right design class". Only the abstract and arXiv text were read (by the reviewer).

**Near-Bayes reading of (F) (KNOWN vocabulary; the instance is ELEMENTARY).** The per-H Bayes selections n(H) have R_H(n(H)) ≥ 1, and R_H(disk) → 1 is a PIM-candidate (L2). So R_H(disk) − min_D R_H(D) → 0. The disk is therefore the unique **fixed** design that is ε-Bayes ("extended Bayes") along the truncated log-uniform family; every fixed polygon has R_H → ∞. That is (F) in decision-theory language, and it confirms §9.5: it is a property of the design-first quantifier order, not of the prior.

### 10.5 L1–L6

- **L1.** "Best n ≈ 0.2·H²/ln H" is the wrong form. The data give n*·ln n*/H² ≈ 0.16–0.21, so **n* ≈ 0.2·H²/ln n*, about 0.14–0.17·H²/ln H** (OBSERVED, a rough fit, H = 100–400). The n* sequence is irregular: 134 at H = 75, then 362 at H = 100. Margin·H²/ln H = 14.7, 13.6, 13.6, 13.2 at H = 50, 100, 200, 400, consistent with ≈ 13–15·ln H/H².
- **L2.** R_H(disk) → 1, and so (P)'s tie in the limit, is a **PIM-candidate** (reviewer's sketch, below). It is no longer labelled only OBSERVED. The sketch needs its own review before the label is upgraded.
  - Every polygon is inscribed in the unit circle, so width ≤ 2 and d(u, w) ≥ |u − w|/2 = sin(φ/2).
  - A d = 1 target needs |v₀ − v_k| ≥ w_min. The review uses w_min ≥ 1 + cos(π/n), which is the odd-n width (vertex to opposite edge). For even n the width is 2·cos(π/n), which is smaller, so the angular-gap bound needs a separate check on even n. Under the review's bound, sin(Θ_n/2) ≥ 1 − π²/(4n²).
  - §8.3's convexity argument with π replaced by Θ ≤ π then gives J(n, T) ≥ T·sin²(Θ_n/2T). Also J(n, T) ≥ d_min ≥ sin(π/n) ≥ 2/n.
  - Split by size: if n ≤ √T then T·J ≥ 2√T; if n > √T then T·J ≥ T²·sin²(Θ(T)/2T) with sin(Θ(T)/2) ≥ 1 − π²/(4T). Hence liminf T·J*(T) ≥ π²/4. With T·J* ≤ π²/4 this gives T·J*(T) → π²/4 and ρ(disk, T) → 1. A log-Cesàro average then gives R_H(disk) → 1, and 1 ≤ R_H(n(H)) < R_H(disk) gives the tie.
- **L3.** SR-b2 for bounded support needs p(T ≥ 2) > 0. A prior concentrated on T = 1 makes every design tie. "Selects a polygon" should read **"the disk is strictly beaten by some polygon"**. Attainment of the argmin over the infinite menu is not shown.
- **L4.** §9.0's invariance parenthetical is unit relabeling only. The model has a tick, and J(D, cT) is not related to J(D, T) by any scaling. The lower cut-off is the tick. A moving window, e.g. log-uniform on [H/K, H] or [H^a, H], still gives the (P) open miss, by SR-b4: any bounded window is dominated.
  - **"No built-in timescale" is a property of designs, not of this prior.** Only the upper cut-off is sent to ∞. Each polygon carries its own timescale T₀(n), beyond which it stops beating the disk (OBSERVED: ≈ 2.0–2.16·√n for even n, already in §9.3; ≈ 1.44·√n for odd n with n = 401…6401, `rv_t0.out`). The disk alone has none. So in this menu the stake "no built-in timescale" is satisfied by the disk as a **design** property: bounded ρ uniformly in T, which is the competitive requirement U. It is not supplied by putting a scale-free prior on horizons. This sharpens §9.5; it does not change it.
- **L5.** "R_H(disk) − 1 falling like ~1.2/L_H" holds for H ≳ 50 (1.21 at H = 100, 1.22 at H = 400). At H = 2 the product is 0.5. The phrase is scoped to H ≳ 50.
- **L6 (cosmetic).** `lcm_check.py` prints 2/n as the comparison, while §9.2 says "≈ π/n". The DP value is π/n (n·margin → 3.1416). The explicit equal-step path gives 2.8–3.14/n at small H.

### 10.6 Labels (governs §9.7 where they conflict)

| claim | label |
|---|---|
| Prop. SR-b4 (even n, T \| n/2 − 1), lcm family | PIM (ELEMENTARY), M3h's rule — confirmed by the review |
| Odd analogue (odd n, T \| (n−1)/2); (2T+1)-gon; n = 1 + 2m·lcm | PIM-candidate (reviewer, M2), both rules; awaiting `rnd/review_srb4_odd/` |
| (P) open miss at every H ≥ 2 | PIM, M3h's rule; both rules only if M2 passes (not upgraded) |
| SR-b2 for bounded support, with p(T ≥ 2) > 0: the disk is strictly beaten by some polygon | PIM, M3h's rule; both rules only if M2 passes (not upgraded) |
| SR-b2 for unbounded support | HYP (unchanged) |
| (F) disk wins; unique fixed ε-Bayes design along the truncated log-uniform family | PIM, a restatement of SR-b1(d)–(e); near-Bayes reading is KNOWN vocabulary |
| R_H(disk) → 1; tie in the limit | PIM-candidate (L2); was OBSERVED |
| T₀ ≈ 2.0–2.16·√n (even); T₀ ≈ 1.44·√n (odd, n = 401…6401) | OBSERVED |
| n* ≈ 0.2·H²/ln n* (≈ 0.14–0.17·H²/ln H); margin ≈ 13–15·ln H/H² | OBSERVED (rough fits, H ≤ 400) |
| Odd only, mixed-rule J*: some odd n beats the disk at H ≤ 300 under five weights | OBSERVED (H = 150–300 existence at spot points; H = 400 not found in sample). §9.3's OPEN at H ≥ 150 is superseded |
| "No built-in timescale is the stake that selects the disk" | **open miss** for (P); for (F) a restatement of the design-first order (U). "No built-in timescale" is a design property of the disk (L4), not a property of the prior |

### 10.7 Friday-cleanup note for Ace (ROUND10 §14; flag only, conditional on M2; ROUND10 not edited)

- If the odd analogue (M2) passes its review, ROUND10 §14's HYPOTHESIS "J does not select the disk at every finite horizon" would become PIM under the mixed convention too, via the (2T+1)-gon. ROUND10 has those odd wins OBSERVED for T ≤ 20.
- Flag this next to §8.7, which already asks Ace which target rule is intended. Nothing is to be edited until M2's review is in, and nothing in ROUND10 has been edited.

## 11. Odd analogue: review fixes and label upgrades (governs §§9–10 where they differ)

*Appended 26 Nov 2026, about 11:43 ET, after `rnd/review_srb4_odd/HOSTILE_REVIEW_SRB4_ODD.md`, PASS-WITH-FIXES, no H findings. §§0–10 stand as written; where they differ, this section governs. Reviewer scripts and outputs are in `rnd/review_srb4_odd/`. SR-b4's own scripts were not edited. Prior-art DOIs are those of `od_crossref.out`.*

The review wrote the proof out in full (its §2), found no gap, and checked every step separately at 80 digits. Independent distances, a DP with no step cap, and brute force agree at every checked (n, T). With the M1 and M2 wording below, the claim and its corollaries are upgraded as in §11.4.

**Claim (now PIM, ELEMENTARY), in the class of SR_B §1, under both target rules (reading in §11.1).** Let n be odd, n ≥ 5, S′ = (n−1)/2, and let T ≥ 2 divide S′. Then J(n, T) < T·sin²(π/2T) = J(disk, T).

**Corollaries (PIM).** The (2T+1)-gon beats the disk at every T ≥ 2. The odd lcm family n = 1 + 2m·lcm(1..H) beats the disk at every T ∈ [2, H] (and ties it at T = 1).

The proof is the review's §2: gauge distance in K − K, w_min = 1 + cos(π/n) = 2cos²(π/2n), the bound d(v₀, v_j) ≤ sin(πj/n)/cos²(π/2n), T equal jumps to the d = 1 vertex v_{S′}, and strict concavity of sin. The bound n ≥ π suffices; strictness comes from the concavity step. Checks: 81 divisor pairs for odd n = 5…61, 0 failures; brute force on 23 small cases; the lcm family for H = 2…8, m = 1…3; the proof chain at 80 digits on 2,340 cases, 0 failures (`od_checks.out`, `od_lcm.out`, `od_chain.out`).

### 11.1 M1: the odd target reading

Odd polygons have no antipodal vertex, so "the antipode rule" needs an explicit reading.

- **Any-vertex rule (M3h).** The distance-1 vertices from v₀ are exactly {v_{S′}, v_{S′+1}}, with S′ = (n−1)/2. Proof: d(a, b) = 1 iff a and b are support points of K in opposite directions. v₀ is a support point only for directions within π/n of 0; for odd n the opposite direction then lies within π/n of π, where the minimizer is v_{S′} or v_{S′+1}, or both only at direction exactly 0. The two targets are mirror images under the reflection that fixes v₀, so they cost the same. OBSERVED: exactly this set for every odd n = 3…61 (`od_checks.out`).
- **Antipode rule (M3c), the reading used here.** ROUND10's M3c code scores `best[n//2]`, and was only ever run on even n. For odd n, n//2 = S′, a d = 1 vertex. "The vertex farthest from v₀" gives the same pair. OBSERVED: DP to {S′, S′+1} equals DP to {S′} to 50 digits at every checked (n, T).
- **The literal −v₀** is the midpoint of the edge (v_{S′}, v_{S′+1}). That is a mixed state, so under the pure-jump rule of §1 it is not an admissible target. The literal reading is empty.
- **The disk.** Its width is 2 in every direction, so the only pure state at d = 1 is the antipode. The disk's target, and J(disk, T) = T·sin²(π/2T) (§8.3, PIM), are the same under both rules.
- So both readings that make sense give the same cost for odd polygons against the disk. The claim is a pointwise comparison; no even polygon and no J* enters. Without this sentence, "under both rules" is ambiguous for odd n.

### 11.2 M2: every upgraded label is scoped to the class of SR_B §1

- The class is: **pure-state jumps**, quadratic price J = Σ d_t², all effects, and a menu of regular polygons plus the disk. That rule is stated in §1; it is a chosen input, not hidden.
- **If mixed intermediate states are allowed, every design ties at 1/T** (PIM, ELEMENTARY). The straight chord in T equal pieces costs exactly 1/T in every design, because d is a gauge and so homogeneous; with SR-b1(a), J ≥ 1/T. Checked in `od_chain.out`. So the polygon-versus-disk ranking exists only under the pure-jump rule.
- The quadratic price is a second chosen input: ROUND10 already notes that a linear price reverses the ranking.
- **Every upgraded row below is "PIM in the class of SR_B §1, under both target rules"** (with the M1 reading). They are not upgraded outside that class.

### 11.3 L1–L5

- **L1.** For odd n, the any-vertex target set is exactly {v_{S′}, v_{S′+1}} (§11.1). That is what makes the odd case rule-independent.
- **L2.** The odd margin is about **π/(2n)** (OBSERVED: lcm family H ≤ 8 and n ≤ 61; n·(min relative margin) rises toward ≈ 1.570, and π/2 ≈ 1.5708), against π/n for the even family. The proof bound gives ≥ about 0.78/n for the (2T+1)-gon. If a margin rate is quoted, quote these, not the even π/n.
- **L3.** At every checked divisor case the DP optimum equals the equal-step path. That is **OBSERVED only**. The claim needs just the upper bound from that path.
- **L4.** The corollary for R_H is **independent of J* and of the rule used for J***, by pointwise dominance (the §9 corollary: a strict inequality on [2, H] and a tie at T = 1 fix the sign for every weight that is positive somewhere in T ≥ 2). This holds under either target rule and under the mixed convention (even polygons at the antipode, odd polygons at a d = 1 vertex). It closes the M1-type rule-mixing worry of the earlier review for (P).
- **L5. Prior art** (verified on Crossref in the review: `rnd/review_srb4_odd/od_crossref.out`). None of these anticipates the claim; the search was Crossref title queries only, and the papers were not read in full.
  - **Regular polygon state spaces with all effects** (the menu): Janotta, Gogolin, Barrett & Brunner 2011, *New J. Phys.* 13:063024, doi 10.1088/1367-2630/13/6/063024. Also Massar & Patra 2014, *Phys. Rev. A* 89:052124, doi 10.1103/PhysRevA.89.052124.
  - **Distinguishability distance in GPTs** (the gauge identity): Kimura, Nuida & Imai 2010, *Rep. Math. Phys.*, doi 10.1016/s0034-4877(10)00025-x. A first guessed DOI, 10.1016/S0034-4877(10)80044-8, does not resolve and is not used. Also Lami, Palazuelos & Winter 2018, *Commun. Math. Phys.*, doi 10.1007/s00220-018-3154-4.
  - **Analogy for the disk branch only:** Aharonov & Vardi 1980, *Phys. Rev. D* 21:2235, doi 10.1103/PhysRevD.21.2235 (dragging a state with a sequence of measurements, Zeno-type). T·sin²(π/2T) has the form of a sum of per-step disturbances there. This is the reviewer's reading, an analogy, not a citation for the claim.

### 11.4 Labels (governs §§9.7 and 10.6 where they conflict)

| claim | label |
|---|---|
| Odd analogue: n odd ≥ 5, T ≥ 2, T \| (n−1)/2 ⇒ J(n,T) < T·sin²(π/2T) | **PIM (ELEMENTARY)**, both target rules (M1 reading), class of SR_B §1 (M2) |
| (2T+1)-gon beats the disk at every T ≥ 2; odd lcm family n = 1 + 2m·lcm(1..H) beats it at every T ∈ [2, H] | PIM (corollary), same scope |
| Prop. SR-b4 (even n, T \| n/2 − 1), even lcm family | PIM (ELEMENTARY), M3h's rule, class of SR_B §1 (unchanged) |
| (P) open miss at every H ≥ 2, any J* | **PIM**, both rules and the mixed convention, class of SR_B §1 |
| SR-b2 for bounded support with p(T ≥ 2) > 0: the disk is strictly beaten by some polygon | **PIM**, both rules, class of SR_B §1 |
| With mixed intermediate states, every design ties at 1/T | PIM (ELEMENTARY) |
| Odd margin ≈ π/(2n); DP optimum = equal-step path; odd wins at some non-divisor T | OBSERVED |
| SR-b2 for unbounded support | HYP (unchanged) |
| (F) disk wins; unique fixed ε-Bayes design along the truncated log-uniform family | PIM, a restatement of SR-b1(d)–(e) (unchanged) |
| R_H(disk) → 1; tie in the limit | PIM-candidate (L2 of §10; not upgraded here) |
| "No built-in timescale selects the disk" | **open miss** (unchanged) for (P); for (F) a restatement of the design-first order (U) |

### 11.5 Update to the §10.7 Ace note (ROUND10 §14; flag only; ROUND10 not edited)

§10.7 was written as conditional on M2. That review has now passed, with the M1 and M2 fixes above.

- ROUND10 §14's HYPOTHESIS "J does not select the disk at every finite horizon" is **PIM under both target rules**, in the class of SR_B §1, via the (2T+1)-gon. ROUND10 has those odd wins OBSERVED for T ≤ 20.
- For Friday, also write the odd target reading of §11.1 into that note, next to §8.7: for odd n the antipode rule is read as "a vertex at d = 1 from v₀", namely v_{S′} or v_{S′+1}, the farthest vertices (the index `n//2` of M3c's code). The any-vertex rule gives the same set. For the disk, both rules pick the antipode, the unique pure state at d = 1. The literal −v₀ is a mixed edge midpoint and is not allowed.
- The sentence "An even polygon never beats the disk … (PROVED (in-model))" stays false as the task is worded, as §8.7 already said. Nothing in ROUND10 has been edited.
