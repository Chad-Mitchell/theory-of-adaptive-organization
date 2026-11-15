# ARCH_EQUATION: an attempt at GTAO's "architecture equation"

Sunday 2026-11-15, about 00:40–01:10 ET. Written by a Grok Bot executor for Chad (via Ace). Private working note.
Nothing was posted or sent. The Looper repo and the theory repo (`/workspace/theory-of-adaptive-organization`) were only read, never edited.
Checks: `arch_checks/` (scripts with matching `.out` files, one light process at a time, all under 200 MB). The LAYERS-1 lock is `arch_checks/LAYERS1_LOCK.md`, sha256 `dd718eb0…1a88`, written at 00:46 ET before its script was run (local only, no external anchor).

**Labels.** **THEOREM**: proved here under stated assumptions, with a proof sketch and a numerical check. **KNOWN**: published by others. **CONJECTURE**: plausible, not proved. **[R]** = read this session (full text or the named part), **[R-abs]** = abstract or summary page only, **[M]** = from memory, not re-read, **[PR]** = verified by an earlier reviewer in this project (file named).

---

## 0. Bottom line (plain words)

1. **The equation can be written, and most of it is a theorem.** For linear-Gaussian tracking with quadratic loss, the cost-optimal organization is a **cost-thresholded decomposition of the members' drift covariance by readable source**. A shared level is built for every source of shared drift whose loading-weighted size beats its own tracking cost plus upkeep. Each level runs at its own speed, and each item is frozen, held or looked up according to a three-region phase diagram. This is §2, Theorems 1–5, all checked numerically.
2. **The headline constants are not universal numbers. They are universal *functions* of one measurable exponent.** "About 4 for onset, about 2 for vigilance, a 29% ceiling" hold only for (i) discrete, complete reads or entropy-priced attention, (ii) Brownian drift, (iii) free upkeep, (iv) equal read costs, and (v) a small shared share.
   - With rough or persistent drift (Hurst H from ¼ to ¾), the numbers move: 4 becomes 3.4–4.6, 2 becomes 1.8–2.25, and 29% becomes 21–34%.
   - In the other big sensing class, **averaging noisy samples** (cells sensing ligands, foragers averaging readings), the onset exponent is **−2, not −1**. The invariant is N\*ρ² = 27, and the vigilance ratio is not constant at all (it grows as 1/ρ).
   - With indivisible reads (one read returns everything), a second speed layer **never** pays, so the 29% ceiling is 0.
   - CORE_AUDIT §2.5(e) is therefore **corrected**: there are no substrate-free constants. There is a substrate-free *relation* (Theorem 2).
3. **The one piece that looks genuinely new is a scaling relation, and it is elementary.** If a lone member's tracking effort scales as (stakes)^a × (drift)^b, then the group size at which a shared level appears scales as (shared share)^−(1−b)/(1−a). The constants follow as b^−1/(1−a), and they are constant across ρ only when a = b. So **you can predict the onset exponent of a new level from how single members behave, before any level exists.** I did not find this stated. It is two lines of algebra once the problem is posed, so treat it as "probably unstated", not as deep.
4. **Two structural theorems I had not seen in this setting** (both are standard lattice math once you see the structure):
   - **Levels are complements.** The total cost is submodular, so pooling one shared driver makes pooling others for the same members more valuable.
   - **Accretion.** As upkeep falls or stakes rise, the optimal set of levels only grows: levels are added, never swapped out. 76 of 300 random cases needed a level that no single-factor test would have justified.
5. **LAYERS-1 (the audit's distinctiveness test for layered memory): the kill rule as written does not fire, but the honest reading is close to a kill.**
   - P1 passes (9/12) and P3 passes (15/15): optimal layer spacing tightens as stakes ÷ upkeep rises, slope −0.10 to −0.38.
   - P2 fails (6/12; 8/12 with free rates): spacing is *not* span-invariant when there are few layers.
   - K1 and K2 do not fire.
   - But every cost effect works through one route: cost sets the accuracy tolerance, and approximation theory does the rest. **What GTAO adds to layered memory is "approximation theory plus a price".** That is known in principle. D should be demoted from the risky-prediction short list to a modest corollary.
6. **Prior art is close on every side** (§4):
   - Team theory and the economics of information own the static machinery.
   - Meagher, Orbay & Van Zandt (2001) [R-abs] already link environmental drift speed to administrative size dynamically, so "no dynamic drift-to-structure theory exists" is false.
   - Willsky's multiscale trees own the estimation side of nested levels.
   - Kashtan & Alon 2005 [R-abs], Watson et al. 2014 [R-abs] and Jones, Arnold & Bürger 2004 [R-abs] already argue, qualitatively and in simulation, that evolved structure mirrors the structure of environmental change.
7. **Verdict: partly new.**
   - The decomposition itself is **known** machinery, newly assembled.
   - **New (elementary):** the sensing-class scaling relation and its corollaries, the correction that the constants depend on that class, the complementarity and accretion theorems in this tracking setting, and the hold-band existence condition.
   - **Not achieved:** a prediction only GTAO makes. The best candidate for one is now **DP1** (§6): measure a and b from members alone, then predict the onset exponent, across sensing classes.

---

## 1. The optimization, stated precisely (task a)

### 1.1 Primitives

- **Members** i = 1…N. Each acts on a scalar target x_i(t) and pays **stakes** w_i × (estimation error)² per unit time (quadratic loss).
- **Drift as shared plus private, across a spectrum.** x_i = Σ_m B_im s_m + u_i.
  - The sources s_m (m = 1…M) are independent drivers, such as an upstream API, a price, a hormone or a food location.
  - u_i is member i's private drift.
  - Each source and each u_i is a sum of independent components across timescales j: s_m = Σ_j s_mj, with a drift "rate" q_mj per component. For Brownian components the rate is a variance rate. For fractional components it is a scale at Hurst exponent H.
  - The **member-by-member drift covariance rate** is Q = B diag(q) Bᵀ + diag(q_u). Its spectral version Q(f) adds the timescale axis.
- **Readable objects and sensing classes.** A tracker buys information about one readable object: a source s_m from the source itself, or a member target x_i. Price and technology come in three classes:
  - **Class R1, periodic complete reads.** A read costs c (or c_m) and resets the error to 0 (EOQ; THEOREMS T1a).
  - **Class R2, an entropy-priced channel.** Information rate κ at price λ per nat (continuous-time rational inattention).
  - **Class A, precision-priced averaging.** Noisy samples are averaged by a Kalman filter. Precision 1/r is bought at cost c′/r (more samples, receptors or analysts).
- **Upkeep.** Every tracker that exists (a level, a speed layer, a held copy) costs h per unit time.
- **Lookup (optional fallback).** Instead of holding x, a user reads the source at each use, at cost u per use and use rate μ.
- **Lifetime.** The architecture is used over a horizon H_l. This matters only for freezing.

### 1.2 Choice variables (the "architecture")

1. **Levels:** a set S of sources that get a shared tracker. The tracker's error on s_m enters member i's error with loading B_im, so its pooled stakes are W_m = Σ_i w_i B_im².
2. **Member trackers** for the residual r_i = x_i − Σ_{m∈S} B_im ŝ_m. Its drift rate is R_i(S) = q_ui + Σ_{m∉S} B_im² q_m.
3. **Clocks / speed layers** inside each tracker: the components (timescales) it tracks separately.
4. **Mode per item:** freeze (read once per lifetime), hold (track), or lookup.

### 1.3 Objective

Minimize the long-run cost rate

  J = Σ_{trackers} [ φ_class(stakes, drift; price) + h ] + Σ_{looked-up items} N_users μ u,

where φ_class is the minimized tracking cost of one tracker (§2.1). Errors of independent trackers are independent and zero-mean, so their quadratic losses add.

### 1.4 Maintained assumptions (each one is used somewhere below and named there)

- **A1. Quadratic loss.**
- **A2. Gaussian (or finite-variance) drift; components independent across sources and timescales.**
- **A3. Readable sources.** A level reads its source directly, at a cost that does not grow with N.
- **A4. No per-member broadcast or polling cost.** POOLING_REVIEW C4a showed that such a cost destroys the onset law.
- **A5. Separable residual tracking.** Member checks align with level checks, so the costs add (T3a's bound; POOLING_REVIEW C5 puts the optimism at about 15% at ρ = 1).
- **A6. Stationarity** over the period in which the architecture is judged.
- **A7. Selection or design finds the optimum to within its resolution** (CORE_AUDIT C4). Everything here concerns the optimum. Discoverability is a separate question (N1-A, POOLSIM).

---

## 2. Derivation (task b)

### 2.1 Lemma 1 (single-tracker cost; THEOREM, `c1_classes.out` §1)

For one tracker with stakes W and drift rate q:

| Class | Minimized cost φ | Stakes elasticity a | Drift elasticity b |
|---|---|---|---|
| R1, periodic complete reads, fBm with Hurst H | ∝ c^{2H/(1+2H)} (Wq)^{1/(1+2H)} | γ = 1/(1+2H) | γ (same) |
| R1 at H = ½ (Brownian; EOQ) | √(2cWq) | ½ | ½ |
| R2, entropy-priced channel (Brownian) | √(2λWq) | ½ | ½ |
| A, averaging of noisy samples (Kalman–Bucy, P = √(qr)) | (3/2^{2/3}) (W² q c′)^{1/3} | **⅔** | **⅓** |

*Proof sketch.*
- R1: minimize c/T + Wq T^{2H}/(1+2H) over T.
- R2: the error variance is q/(2κ); minimize Wq/(2κ) + λκ.
- A: the steady-state Riccati equation gives P = √(qr); minimize W√(qr) + c′/r over r.

All three were done in sympy. The Kalman–Bucy root and its discrete-sampling limit were checked numerically.

**In all three classes, optimal spending on information is a fixed share of φ** (½ in R1 and R2, ⅓ in A). So the effort elasticities (check rate, sampling rate, attention) equal (a, b). **That is what makes (a, b) measurable from a lone member's behavior.**

**Physical reading.** In "reset" technologies (complete reads, or channels that destroy uncertainty at a rate), error accumulates linearly in drift × time. Stakes and drift then enter only through their product, so a = b. In "averaging" technologies, the filter balances its own bias against its own variance, so stakes and drift enter differently (a = ⅔ > b = ⅓).

### 2.2 Theorem 2 (one shared source: the onset relation; THEOREM, `c1_classes.out` §2–3)

**Setting:** homogeneous members (w, q_u), one source with unit loadings and rate q_g, ρ = q_g/q_u, and power-class cost φ = k W^a q^b. Then:

- flat organization costs N k w^a (q_g + q_u)^b;
- a level costs k (Nw)^a q_g^b + N k w^a q_u^b + h.

**(i) Small-ρ onset, h = 0:**

  **N\* · ρ^{(1−b)/(1−a)} = b^{−1/(1−a)}**,

so the shared-drift elasticity is **e_g = −(1−b)/(1−a)** and the private-drift elasticity is e_u = +(1−b)/(1−a).

**(ii) Vigilance** (the level's effort ÷ a flat member's effort, at N\*): **V = N\*^a ρ^b ∝ ρ^{(b−a)/(1−a)}**. It is a constant **iff a = b**, and then **V = b^{−a/(1−a)} = Π\*^γ**, with Π\* = γ^{−1/(1−γ)}.

**(iii) With upkeep** h′ = h/(k w^a q_u^b):
- If a = b, then e_g stays at −1 for every h′, e_u falls below 1, and Π\* and V rise. At γ = ½: Π\* = (1 + √(1+2h′))², V = 2.73 at h′ = 1 and 5.58 at h′ = 10.
- If a > b, the level's own cost term N^a ρ^b eventually dominates as ρ → 0, so e_g → −(1−b)/(1−a) whatever the upkeep.

*Proof sketch.* Expand flat − level to first order in ρ: N k w^a q_u^b · bρ − k N^a w^a q_g^b > h. Set h = 0 and solve. For V, substitute N\* into the effort ratio (Lemma 1: effort ∝ φ).

*Checks.* Exact roots, without the first-order expansion, at ρ from 10⁻⁴ to 1 and h′ ∈ {0, 1, 10}, reproduce every number below. They match T3a's exact N\* = (√(1+ρ)+1)²/ρ to 4 digits.

| Class | e_g (small ρ) | Onset invariant (h = 0) | Vigilance V (h = 0, small ρ) | Two-clock ceiling (additive reads) |
|---|---|---|---|---|
| R, H = ½ (EOQ; entropy channel) | −1 | N\*ρ = **4** | **2.00** | **29.3%** |
| R, H = ¼ (rough drift) | −1 | N\*ρ = 3.375 | 2.25 | 20.6% |
| R, H = ¾ (persistent drift) | −1 | N\*ρ = 4.61 | 1.84 | 34.0% |
| A (averaging noisy samples) | **−2** | **N\*ρ² = 27** | not constant: 903 at ρ = 0.01, 9,003 at ρ = 0.001 | not derived (needs a filter-memory model; see §3) |

**What each constant needs (honest scope):**
- **Π\* ≈ 4** needs A1, A2 with Brownian drift (H = ½), an R-class technology, h = 0, ρ ≪ 1, equal read costs (it scales with c_g/c), A3, A4 and A5.
- **V ≈ 2** needs everything Π\* needs. It also holds only when shared and private checks have equal per-unit cost (V ∝ √(c/c_g)), and "effort" must be measured per unit of the driver's own drift.
- **The −1 exponent** needs a = b. That is any R-class technology at any H, and with quadratic loss any Gaussian spectrum. It also needs A3, A4 and ρ ≪ 1.
  - It fails in class A (−2).
  - It fails for absolute-error loss (−2) and for quartic loss at low upkeep (−½). These are POOLING_REVIEW's cases, now explained by the same a-vs-b rule.
- **The 29% ceiling** needs: two components; R class at H = ½; **additive per-component read cost** (each component separately observable, each read paid separately); infinite separation; and upkeep not counted. With K components the ceiling is 1 − K^{−(1−γ)}. **With indivisible reads it is 0:** one read returns every component, so a single clock always wins (`c1_classes.out` §4).

### 2.3 Theorem 3 (many sources: the architecture equation proper; THEOREM, `c2_factor.out`, `c2b_tree.out`)

Work in class R at γ = ½ (EOQ), heterogeneous members, M sources with arbitrary loadings B, read costs c_m, and upkeep h per level. The total cost of level set S is

  J(S) = Σ_{m∈S} [√(2 c_m q_m W_m) + h] + Σ_i √(2 c w_i R_i(S)),  W_m = Σ_i w_i B_im²,  R_i(S) = q_ui + Σ_{m∉S} B_im² q_m.

**(a) Complementarity.** The members' savings F(S) = Σ_i √(2cw_i)[√R_i(∅) − √R_i(S)] are **supermodular** in S, so J is **submodular**.
*Proof.* Adding source m removes the fixed amount δ_i = B_im² q_m from R_i. For concave √, the gain √R − √(R−δ) is larger at smaller R, and R_i(S) falls as S grows. The level side of J is modular.
*Check:* 0 violations in 5,520 random (S ⊂ S′, m) triples.

**(b) The first-order (separable) rule.** Define each member's shadow price of drift λ_i = ∂φ_i/∂q = √(c w_i/(2Q_ii)). Then **keep source m if**

  **q_m Σ_i λ_i B_im² − √(2 c_m q_m Σ_i w_i B_im²) > h.**  (the architecture equation, first order)

This is Theorem 2's condition with "N" replaced by the shadow-price-weighted loading mass. It is exact to first order in each source's share of each member's drift.

**(c) Inclusion.** Every source kept by (b) belongs to **every** exact optimum.
*Proof.* Concavity gives an exact marginal saving ≥ the first-order one, so the marginal is positive at ∅. Supermodularity keeps it positive at every S, and any S without m is improved by adding m.
*Check:* 0 failures in 300 brute-force cases. In 76 of the 300, the exact optimum was **strictly larger**: complementarity let levels form that no single-source test justified.

**(d) Lattice and accretion (Topkis).** The optimal sets are closed under union and intersection (0 failures in 300 cases). The largest optimal set **only grows** as h falls (0 removals in 2,400 steps). Raising every stakes w_i by a factor s is the same as dividing h by √s, because J scales as √s apart from the hK term. So it also only adds levels.
*Consequence:* cheaper memory or higher stakes never make an existing level redundant in this model. Levels accrete.
*Computation:* the optimum is a submodular minimization, so it can be found in polynomial time (Grötschel–Lovász–Schrijver; Schrijver 2000 [M]).

**(e) When the decomposition is an eigendecomposition.** If members are homogeneous and the sources' member scopes are disjoint (or the loading vectors are orthogonal), source m's loading mass q_m‖B_m‖² is exactly an eigenvalue E_m of the shared drift covariance C = B diag(q) Bᵀ. Then (b) becomes

  **the number of levels = the number of eigenvalues of C above θ, where λE − √(2c_g w E) = h. At h = 0, θ = Π\* · Q_res · (c_g/c) = 4 Q_res c_g/c.**

Here Q_res is a member's total drift rate. On the full covariance Q, the threshold is (1 + Π\*)·q_u, i.e. 5× the private floor when the share is small.
*Check:* the eigen rule was consistent with brute force in 200/200 cases (equal to the exact set, or contained in it, as (c) requires). Block-factor eigenvalues equal n_k q_k exactly.
**With overlapping scopes it is NOT an eigendecomposition.** Eigenvectors mix sources: in the check, the two eigenvectors spanned 100 and 60 members, while each source covered 70. A level on an eigenvector would have to read several sources at once. **The right decomposition is by readable source (a factor model whose factors are physical), not by principal component.** Principal components are correct only when any linear combination is equally cheap to read (rotation-invariant cost). In that case the problem becomes multivariate rational inattention, where reverse water-filling on eigenvalues is KNOWN (Sims 2003 [PR]).

**(f) Nested scopes (trees): which scales get a level.** Take groups nested at sizes n_s (branching ratio b), with shared rate q_s ∝ n_s^{−κ} (sharing thins out as scope widens).
- A scale gets a level iff n_s q_s > Π\* Q_res (first order). So n_s^{1−κ} sets the order.
- **κ < 1: broad levels form first (top-down).** **κ > 1: only narrow levels form (bottom-up).**
- κ = 1 is the knife edge where no scale is favored (`c2b_tree.out`).
- When some shares are large, complementarity and finite ρ add levels the first-order rule misses (κ = 1.5, q0 = 20: exact keeps groups of 16 and 4, first-order keeps none).
- So **the depth of a hierarchy is set by how fast shared drift thins with scope, relative to the cost threshold.** That is a statement about the environment, not about N. It is consistent with T7's "the architecture inherits the world's scale structure".

**Scope of Theorem 3:** A1–A5, class R at γ = ½, and one read per source. If one read can return several sources (indivisible bundled reads), the level side becomes submodular as well. J is then no longer submodular, and (c) and (d) can fail. **Not derived here:** Theorem 3 for class A. Theorem 2 already shows that the class-A onset is −2, and complementarity should carry over, because φ is concave in drift there too. That is a CONJECTURE.

### 2.4 The timescale axis

1. **Clocks for separately readable components (THEOREM; T3b generalized).** Splitting one tracker into K clocks saves at most 1 − K^{−(1−γ)}, and only under additive per-component read costs. The split pays iff the saving exceeds (K − 1)h. With indivisible reads it never pays. So **speed layers exist only when components can be read separately**: a slow and a fast variable with their own sources, such as a quarterly plan and daily sales, or long-lived and short-lived receptors.
2. **Filter memory for noisy reads.** Here the "layers" are the exponentials in a filter kernel. Layer count and spacing come from approximating the optimal kernel at a cost-set tolerance (§3, LAYERS-1).
3. **Cross-axis coupling (CONJECTURE).** A level's stakes are pooled (W = Nw), so its optimal check interval shrinks by N^{−γ} at a fixed driver spectrum. It therefore resolves faster components of its driver. If LAYERS-1's tolerance mechanism applies, it should also keep more temporal layers: K\* grows by about (L/α)·ln N (§3).
   - **Prediction:** at a fixed driver spectrum, a pooled level is faster and has more temporal layers than the members it serves. That is the opposite of "higher levels are slower". Real higher levels usually track slower drivers, so the test must control for the driver's spectrum.
   - Not proved, because the mapping from a substrate to "filter kernel" is not established.

### 2.5 Theorem 4 (per-item mode: freeze, hold or lookup; THEOREM, `c3_phase.out`)

Take one item in class R at γ = ½, with stakes W per user, drift q, read cost c, holding upkeep h, lifetime H_l, use rate μ and lookup cost u. Holding with interval T ≤ H_l costs c/T + WqT/2 + h; freezing is the corner T = H_l. Lookup costs μu. Then:

- **Freeze ↔ hold:** freeze iff the EOQ interval exceeds the lifetime, **Wq ≤ 2c/H_l²**.
- **Hold ↔ lookup:** look up iff √(2cWq) + h > μu, i.e. **q > q_c = (μu − h)²/(2cW)**. The edge's elasticity with respect to the lookup cost u is 2 in q and 1 in σ (T5b's cliff).
- **A hold band exists iff μ u H_l > 2c + h H_l.** Holding *any* drifting item pays only if lifetime lookup spending exceeds two reads plus lifetime upkeep. Otherwise items are either frozen or looked up.
- **Shared copy for N users** (W → NW, lookup → Nμu):
  - the freeze edge falls N-fold, so a shared store freezes less;
  - the lookup edge rises N-fold (to N·q_c when h is small);
  - **so the hold band widens by a factor N² in drift**, and a shared hold band survives until u < (2c + hH_l)/(NμH_l).

All edges match the closed forms to grid resolution (for example 0.000202 vs 0.0002, and 0.126 vs 0.125).

**Reading (human–AI).** As AI makes lookup cheap (u ↓), individuals first stop holding fast-changing facts (q_c ∝ u²). Once μuH_l < 2c + hH_l, they stop maintaining *any* changing fact: they freeze what is stable and look up the rest. Shared stores keep a hold band N times longer. This assumes quadratic staleness loss and that lookups return current values.

### 2.6 What the "architecture equation" is, in one block

Given (B, q(f), q_u, w) for the environment and (c, c_m, h, u, μ, H_l, sensing class) for the substrate:

1. **Levels:** keep source m iff q_m‖B_m‖²_λ − φ_class(W_m, q_m) > h (first order). The exact set is the submodular minimizer, which contains the first-order set. Under homogeneity with disjoint scopes, this is the number of eigenvalues of C above θ = Π\*(h′, class)·Q_res·(c_m/c)^{…}.
2. **Scope** of each level is the support of B_m. **Depth** is the number of nested scales with n_s q_s > θ.
3. **Speed** of each level: effort ∝ W_m^a q_m^b. At onset it is V times a member's effort, V = Π\*^γ in class R and ∝ ρ^{(b−a)/(1−a)} in class A.
4. **Mode** of each item comes from the phase diagram of Theorem 4, with pooled stakes and pooled lookup.
5. **Temporal layers** inside a tracker: clocks if components are separately readable (gain ≤ 1 − K^{−(1−γ)}); otherwise filter layers at a cost-set tolerance (§3).
6. **Constants:** universal functions of (a, b), and through γ of the drift's Hurst exponent. They are not universal numbers.

---

## 3. LAYERS-1 (task c)

**Lock.** `arch_checks/LAYERS1_LOCK.md` (sha256 `dd718eb0…1a88`, 00:46 ET) holds CORE_AUDIT N1-C's predictions verbatim, plus the operational choices, fixed before running:
- kernel t^{−b} on [1, 10^L];
- K exponentials with geometric rates (λ₁ and ratio optimized) and least-squares weights;
- loss ε = mean squared relative error on a log grid;
- total cost = (w/h)·ε + K;
- the "accuracy-only count" is the smallest K with max relative error ≤ 3% (SCALEFREE S3's criterion).

**Results** (`c4_layers1.out`; robustness run with free rates in `c4b_layers1_free.out`):

| Item | Result | Locked bar | Verdict |
|---|---|---|---|
| P1: K\* linear in L beats L^{2/3} | 9/12 series | ≥ 8 | **PASS** (the margins are small; R² values are 0.89–1.00 for both forms) |
| P2: r\* varies < 30% over L = 2…6 | 6/12 (free-rate run, L ∈ {2,4,6}: 8/12) | ≥ 9 | **FAIL.** Spacing widens with span when layers are few (low w/h). It is close to span-invariant only at w/h ≥ 10⁴ (spreads 0.02–0.27) |
| P3: r\* falls as w/h rises, \|slope\| > 0.05 | 15/15 (b, L) series, slopes −0.12 to −0.38 (free-rate run: −0.10 to −0.27) | ≥ 9 of 12 | **PASS.** The lock says "12 series" but the slope is naturally taken across w/h per (b, L), giving 15. Every one passes under either reading |
| K1: P3 fails AND K\* is within ±1 of the accuracy-only count everywhere | P3 passes; \|K\* − K_acc\| reaches 5 | — | **does not fire** |
| K2: r\* grows as L^{1/3} (log slope in [0.2, 0.5]) | 3/12 series; median slope ≈ 0.15, range −0.58 to 0.51 | — | **does not fire** (no consistent T7b scaling) |

**Caveat on the method:** geometric rates are suboptimal for K ≥ 4. Free rates lower ε by 2–5× at K = 5. The free-rate rerun leaves P2's failure and P3's pass unchanged.

**Honest reading (beyond the literal rule).** Any cost-optimal K\* is, by construction, the accuracy-only count at the tolerance where one more layer's error reduction × w equals h. The error falls roughly geometrically in K at a rate that decreases with span: about 0.96, 0.62 and 0.47 decades per layer at L = 2, 4 and 6 (b = 0.7). The cost-optimal tolerance ε\* is therefore the error at which one more layer lowers w·ε by exactly h (of order h/w, adjusted by the per-layer reduction rate, which depends on the span). Spacing and count then follow from approximation theory at that tolerance. **So costs change layer count and spacing only through an implied tolerance.** "Spacing tightens with stakes ÷ upkeep" is what any accuracy–cost tradeoff predicts. The literal kill rule does not fire, because its comparator is a *fixed* 3% tolerance. But the content left over beyond approximation theory is "plus a price", which is known in principle (rate–distortion; Lagrangian duality).

**Consequence for CORE_AUDIT prediction D:**
- "Spacing set by the cost ratio, not the span" is **half false**: the span matters when there are few layers (P2 fails).
- "Cost-dependent spacing" is true but generic.
- Demote D from the short list to a corollary. The only distinctive empirical bet left is against fixed-ratio accounts (Benna–Fusi's ratio 2 [M]): real layered systems should densify as stakes ÷ upkeep rises, with log-slope about −0.1 to −0.35.
- Note that the T7b clock problem (count ∝ (C·L²/h)^{1/3}) is a different problem. It too is "approximation plus price", in the cadence-penalty metric.

---

## 4. Prior art for the decomposition (task d)

| Work | Status | What it has | Overlap with §2 |
|---|---|---|---|
| Marschak & Radner 1972, *Economic Theory of Teams*; Radner 1962, *Ann Math Stat* 33:857 | [M]; Radner 1962 metadata [PR, CORE_AUDIT] | Quadratic-Gaussian teams; the value of information structures, including common observations, against their cost | The machinery of Theorems 2–3 (static) |
| Geanakoplos & Milgrom 1991, *JJIE* 5:205 | [PR, CORE_AUDIT read the DP 775R text] | Onset condition for a manager over n shops; more uncertainty → smaller spans | A static onset for a level; private uncertainty only |
| Dessein, Galeotti & Santos 2016, *AER* 106:1522 | [PR; this session I grepped `src/dgs.txt`: shocks are task-specific; "optimal scope … decreases as the environment becomes more volatile"] | Bimodal attention; plan vs feedback; volatility → smaller scope | Freeze vs hold in organizational dress; no shared drivers or level onset |
| Veldkamp & Wolfers 2007, *JME* | [PR, POOLING_REVIEW] | N × aggregate-information value ≥ fixed cost | Theorem 2 at a = b with large upkeep (static, entropy cost) |
| **Meagher, Orbay & Van Zandt 2001**, "Hierarchy Size and Environmental Uncertainty", CEPR DP 2839 | **[R-abs]** (IDEAS page) | Administrative staff size vs environmental stability: costless managers → staff rises with stability; costly managers → inverted U. The mechanism is processing delay vs drift | **A dynamic drift → structure result already exists.** It differs from §2 (one aggregate, delay mechanism, no shared/private split, no onset exponent), but CORE_AUDIT's "nobody has a dynamic drift spectrum setting structure" must be softened |
| **Vayanos 2003**, *RES* 70(3):667–695, doi 10.1111/1467-937X.00261 | **[R-abs]** (LSE page; a search summary says it uses a common systematic factor plus idiosyncratic risk) | Endogenous hierarchy for portfolio decisions; aggregation loses information | Common-plus-idiosyncratic structure in hierarchy design (static); I have not checked whether it states anything like Theorem 2 |
| Van Zandt 1999 *RES*; Radner 1993 *Econometrica*; Orbay 2002 *JET* | [R-abs] (titles via the IDEAS reference list) / [M] | Real-time decentralized information processing; hierarchy as parallel processing | A different cost (delay), same family |
| Alonso, Dessein & Matouschek 2008, *AER* 98(1):145 | [M] (located by search, not read) | Centralization vs decentralization with coordination needs and local information | The qualitative "centralize common, decentralize local" is old (Hayek lineage [M]) |
| Sims 2003, *J Monet Econ* 50:665 | [PR] | Multivariate RI: water-filling on eigenvalues | Theorem 3(e)'s eigen case under rotation-invariant cost is KNOWN |
| **Chou, Willsky & Benveniste 1994**, *IEEE TAC* 39(3):464–478, doi 10.1109/9.280746; **Willsky 2002**, *Proc IEEE* 90(8):1396, doi 10.1109/JPROC.2002.800717 | **[R-abs]** | Multiscale (tree) state-space models and Kalman filtering on trees; 1/f processes as trees | **Estimation on nested levels is KNOWN.** Willsky optimizes estimation given a tree; §2.3(f) chooses which tree nodes to *pay for*. I found no cost-thresholded tree selection there (abstracts only) |
| Dynamic factor models (Geweke 1977; Stock & Watson 2002); Chamberlain & Rothschild 1983 | [M] | Common factors with their own dynamics; "pervasive" factors have eigenvalues that grow with N | The statistical object of §2.3, with no cost threshold |
| Simon 1962, "The architecture of complexity", *Proc Am Phil Soc* 106:467; Simon & Ando 1961, *Econometrica* 29:111 | [M] | Near-decomposability: strong within-block, weak between-block interaction; aggregation of variables | The disjoint-scope case of Theorem 3(e) is the near-decomposable case; Simon is qualitative about *why* blocks form |
| Baldwin & Clark 2000, *Design Rules*; MacCormack, Baldwin & Rusnak 2012; Colfer & Baldwin 2016 (mirroring) | [M] | Modularity's option value; organization mirrors technical dependency | Mirrors *dependency* structure, not *drift* covariance weighted by stakes and thresholded by cost. This is the rival for DP3 |
| **Kashtan & Alon 2005**, *PNAS* 102(39):13773, doi 10.1073/pnas.0503610102 | **[R-abs + summary]** | **"Modularly varying goals"**: environments that change in a modular way evolve modular networks, which "learn" the problem's structure | **Qualitative prior art for "structure mirrors the structure of environmental change"** |
| **Watson, Wagner, Pavlicev, Weinreich & Mills 2014**, *Evolution* 68(4):1124, doi 10.1111/evo.12337 | **[R-abs]** | Selection on phenotypic correlations is equivalent to associative (Hebbian) learning; evolved networks store past selective environments | Prior art for "organization = a learned copy of environmental covariance" (no costs or onset) |
| **Jones, Arnold & Bürger 2004**, *Evolution* 58(8):1639 | **[R-abs]** | The G-matrix with a moving optimum: orientation stabilizes when the optimum moves along the leading eigenvector; G aligns with the selection landscape | Quantitative-genetics prior art for "the covariance of internal structure aligns with the covariance of environmental change" |
| Govern & ten Wolde 2014, *PNAS*, doi 10.1073/pnas.1411524111 | [R-abs] | Cellular sensing precision limited by receptors × time, readout molecules and energy | Supports class A (precision-priced averaging) as the cell-sensing class |
| "Principal-components org design" | **Not found.** I know of no literature by that name and cite none | — | — |

**Prior-art verdict.**
- **KNOWN:** the decomposition's machinery (team theory, VOI, multiscale estimation, water-filling), the qualitative thesis (Simon; Kashtan–Alon; Watson et al.; the G-matrix literature), and a dynamic drift → structure link (Meagher–Orbay–Van Zandt).
- **Not found in what I read:** the scaling relation e_g = −(1−b)/(1−a) with its class-dependent invariants; the a = b condition for constant vigilance; submodularity and accretion of tracking levels; cost-thresholded selection of tree levels by how sharing thins with scope; the hold-band existence condition.
- **Still owed before any public novelty claim:** Marschak–Radner chs. 4–6; Vayanos 2003 full text; Meagher–Orbay–Van Zandt full text; Veldkamp 2011 ch. 8; the 2023 JEL RI survey.

---

## 5. Theorems vs conjectures

**THEOREMS** (proof sketch here; numerically checked):
- **Lemma 1:** class exponents (a, b), and effort elasticities = cost elasticities.
- **Theorem 2:** the onset relation, the invariant, vigilance (constant iff a = b), and the upkeep behavior.
- **Theorem 3(a)–(f):** submodularity, the first-order rule, inclusion, lattice and accretion, the eigen case and its failure under overlap, and the tree-depth rule (first order, plus exact checks).
- **§2.4(1):** the K-clock ceiling 1 − K^{−(1−γ)}; zero with indivisible reads.
- **Theorem 4:** the freeze/hold/lookup phase diagram, the hold-band existence condition, and the N² widening for shared stores.

**CONJECTURES:**
- Theorem 3 in class A (complementarity there).
- The cross-axis coupling: pooled levels resolve faster and keep more temporal layers.
- That real substrates fall cleanly into classes R and A.
- That selection resolves these optima (A7; POOLSIM/N1-A tests discoverability).

**Withdrawn or corrected:**
- "Π\* ≈ 4, V ≈ 2 and 29% are the same on every substrate" (CORE_AUDIT §2.5e): **false as stated.**
- "Layer spacing is set by the cost ratio, not the span" (CORE_AUDIT D): **half false** (LAYERS-1 P2).

---

## 6. Distinctive predictions, with kill rules

Each of these is distinctive against the *native* rival in its field. None is distinctive against an economist who sets up the same model.

**DP1. The sensing-class scaling relation (the best candidate for a GTAO-only claim).**
- **Prediction:** measure, on members alone (no level present), the elasticities of tracking effort with respect to stakes (a) and drift (b). Then the shared-level onset elasticity is e_g = −(1−b)/(1−a), and the invariant is N\*ρ^{(1−b)/(1−a)} = b^{−1/(1−a)} (with free upkeep).
  - Reset-type substrates (discrete complete reads: dependency bumps, inventory counts, wiki refreshes) predict a ≈ b ≈ ½ and e_g ≈ −1.
  - Averaging-type substrates (cells, forager estimates) predict a ≈ ⅔, b ≈ ⅓ and e_g ≈ −2.
- **Rivals:** duplicated effort (−γ), size rules (0), contingency theory (total volatility → decentralize).
- **Kill rules:**
  - (i) **Designed simulation:** class-R and class-A worlds under strong selection. If the evolved e_g at ρ ≤ 0.03 lies outside [−1.2, −0.8] (R) or [−2.4, −1.6] (A), the relation fails as a *discoverable* law. Its algebra is a theorem, so only discoverability is at stake.
  - (ii) **Field:** in two substrates with independently measured (a, b), q_g and q_u, the estimated e_g CI excludes −(1−b)/(1−a) in both.
- **Warning:** the prize near onset is tiny (POOLING_REVIEW C6). In class A it should be even smaller per unit of N, which is not computed yet. Field tests need N1-A's resolution result first.

**DP2. Vigilance invariance holds only in reset substrates.**
- **Prediction:** at onset, level effort ÷ member effort, per unit of the driver's own drift, is the same constant across ρ when a = b (2.0 at H = ½ with free upkeep), and grows as ρ^{(b−a)/(1−a)} (∝ 1/ρ) in class A.
- **Rival:** "higher levels are slower" (V < 1).
- **Kill:** under strong selection in the N1-A design (class R), the evolved V is ≤ 1 in ≥ 3 of 4 small-ρ cells (this is CORE_AUDIT K3). In a class-A simulation, V does not rise as ρ falls.

**DP3. Level count = number of shared-source loading masses above threshold, not size or dependency count.**
- **Software design (to preregister):** per organization, the sources are upstream packages, the loadings are which repos use each one, and q_m is the upstream's breaking-change rate. The model predicts which upstreams get an org-wide wrapper or pin: probability increases in n_m q_m / Q_res **at fixed n_m**.
- **Rivals:**
  - n_m alone (R-size / duplicated effort);
  - the dependency or communication structure (mirroring / Conway).
- **Kill:** in a locked, out-of-sample test, adding n_m q_m / Q_res to a model with n_m and dependency-graph features does not raise AUC by ≥ 0.03, or its coefficient has the wrong sign.
- **Scope:** A3 and A4 must plausibly hold. Test the *ranking*, not the constant 4: c_g/c is unknown, and the prize is small near threshold.

**DP4. Accretion.**
- **Prediction:** when upkeep for shared memory falls (for example after a tooling change that makes shared modules cheap), organizations add levels and rarely remove ones that existed before, holding the environment fixed (Theorem 3d).
- **Rival:** reorganization as fashion or churn (additions and removals equally common).
- **Kill:** in a panel with an identifiable upkeep drop, removals of pre-existing levels are ≥ 50% as frequent as additions.
- **Confounds:** environment change, and per-member communication costs that break A4.

**DP5. The hold band and AI lookup (human–AI).**
- **Prediction:** in a controlled task, the drift above which people stop maintaining a fact rises as (lookup cost)², σ_c ∝ u. When lifetime lookup spending falls below about two refreshes, people stop maintaining any changing fact. A shared team store keeps maintaining facts N times further into drift.
- **Rivals:**
  - qualitative cost–benefit offloading (Risko & Gilbert 2016 [M]; Sparrow et al. 2011 [M]), which gives no exponent;
  - DGS bimodality, which has no fallback-cost edge.
- **Kill:** the elasticity of σ_c with respect to u lies outside [0.5, 1.5], or there is no individual-vs-shared difference that scales with N.

---

## 7. Verdict

**Partly new.**
- **Known:** the architecture equation's decomposition. It is a cost-thresholded factor model by readable source, it becomes an eigendecomposition only for disjoint scopes or rotation-invariant costs, and its estimation side is Willsky's multiscale trees. So is the qualitative thesis that structure copies the covariance of change (Simon; Kashtan–Alon; Watson et al.; the G-matrix literature) and a dynamic drift → structure link (Meagher–Orbay–Van Zandt).
- **New as far as I found (each elementary):**
  1. the sensing-class scaling relation, with the a = b condition for invariant constants;
  2. the correction that "4, 2, 29%" are class- and H-dependent, not universal;
  3. complementarity and accretion of tracking levels;
  4. the tree-depth rule by how sharing thins with scope;
  5. the hold-band existence condition.
- **Not achieved:** a prediction that only GTAO makes and that has passed. The derivation narrows the program to one sharp, cross-substrate bet (DP1), with the discoverability gate (N1-A/POOLSIM) in front of it.

**What this means for the "profound" goal.** The honest big claim is not "the same constants everywhere". It is: **"an organization's levels are a cost-thresholded copy of its environment's shared-drift structure, and the exponents of that copy are fixed by how its members sense."** That makes a falsifiable cross-substrate link from individual sensing technology to collective structure. It is worth testing. It is not yet a result.

## 8. Limits of this note

- Theorem 3 is proved only for class R at γ = ½ with one read per source.
- Cross-source correlations in drift were assumed zero (correlated sources should be rotated into independent physical drivers first, which may not be readable).
- Broadcast costs (A4) and misaligned checks (A5) were not added to the multi-source case.
- LAYERS-1 used geometric rates (free-rate robustness only at L ∈ {2, 4, 6}).
- Most prior art was read as abstracts. No independent reviewer has checked this note yet; it needs one before any claim leaves the box.
