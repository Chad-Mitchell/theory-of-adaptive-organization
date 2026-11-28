
## 8. SH-heat pre-statement: lifetime from the theory's keep, check or fade rule (written 26 Nov 2026, about 14:35 ET, before any SH-heat number is computed; §§0–7 stand as written)

*The SHA-256 of this block, from the "## 8." heading line through the end of §8.9, is logged in WORKLOG.md before any computing. Nothing in §8 may be edited afterwards. Results go in §9.*

*Disclosure of a switch made before writing.* §7.10 named SH-heat as "charge the keep-floor heat inside J". A redirect arrived at 14:19 ET, before any of §8 was written or hashed: make the theory's own keep-or-fade rule the **lifetime** rule, so that the lifetime comes from the theory and not from erfc noise alone. §8 is written that way. The §7.10 version, the keep heat added to J, is **not** run. It would need an exchange rate between J (dimensionless, ROUND10 §14 "c·d² per tick") and kT, which is a free parameter. It is listed in §8.8 as untested.

### 8.1 The rule, from the theory's text (read this session at `8b553c6`, today's main; CORE.md and THEORY.md are byte-identical to `ac92ee2`)

- **THEORY.md:138**, Rule 2: "Keep a fact while need × miss cost beats upkeep, which rises with drift; otherwise let it fade, recoverably", a theorem proved in a model (CT4, CT9, CT11).
- **THEORY.md:145**: "Rules 2 and 4 are one decision, what to hold (keep while the value rate beats upkeep: CT4, CT9, CT11, CT26)".
- **THEORY.md:301–313, §B.2 "Keep, check or fade"**, CT9 (G2, hold or fade): checking every s costs λc/s + A(s) per unit time, with A(s) = (1/s)∫₀ˢ r(u) du; fading costs r_∞. Some periodic schedule beats fading iff λc < Φ. CLAIM_MAP_v2.md:530 has the same row (PROVED (in-model)).
- **THEORY.md:321–330**, CT11 (freeze, hold or look up): the interior hold interval T* = √(2c/(Wq)). CLAIM_MAP_v2.md:532 (alias of F13).
- **THEORY.md:480**, CT26: keep iff the upkeep rate is below the value rate; the optimum is bang-bang. CLAIM_MAP_v2.md:559.
- **THEORY.md:279 and CLAIM_MAP_v2.md:525**, CT4 (the first bit must pay): carry memory iff its price per nat is below the marginal loss it saves.
- **CORE.md:21–23**: J = Q̇ + w·E[ℓ]. "It bounds a heat. It does not choose a stake…"; "w converts the loss into the currency of the heat. Temperature does not set w."
- **CORE.md:78**: "Frozen or disconnected worlds allow zero ongoing heat… Storage is cheap. Tracking a changing, connected world is what costs."
- **CT33** (THEORY.md:127, :495; CLAIM_MAP_v2.md:566): spend never falls and error never rises as stakes rise. This is a monotonicity in w, not a keep rule. It is used only as a check: the kept design count and the spend must be monotone in x below.
- **"Theorem O(v)": not found.** I searched for that string, "Theorem O" and "O(v)" in every file of today's main (`8b553c6`). The only nearby names are CLAIM_MAP section **O** (the v2.49 core rows, CLAIM_MAP_v2.md:154) and **O1 = CT7**, the tracking floor (CLAIM_MAP_v2.md:528). Neither is a keep or fade rule. Nothing below rests on "Theorem O(v)".

### 8.2 The model (one stake ratio x = w/kT, CORE's own input; no other new parameter)

- **Record.** The design D (an n-gon) holds one of n written symbols, uniform, as in §6. It has the same leak as the §6 primary: angular kicks θ ~ N(0, σ²) wrapped, snapped to the nearest vertex. The snapping kernel q_j(n, σ) and the leak rate Γ = σ²/2 per tick are as in §6.1.
- **Use and stake.** The record is used once per tick. A wrong symbol costs w. Per tick, everything is in kT units, with **x := w/kT**.
  - The stake cannot be removed: CORE.md:23 says temperature does not set w, and every keep rule in §8.1 compares a value, denominated in the stake, with an upkeep. So x is the theory's own input, not a new one. It is swept on a fixed grid (§8.4).
- **Three modes, the "keep, check or fade" menu of THEORY §B.2:**
  - **Keep** (continuous holding against the leak). The record stays at its written symbol, at the keep-floor heat rate (C12B_ORDER §8.2, §9.1, §9.4) of c_K·Γ·I per tick, with I = ln n nats. Primary c_K = 2 (Gaussian G-keep, floor value; its attainment is OPEN, so the floor is the value most favourable to keeping). Arm c_K = 4 (the T63 binary constant 4Γ). Cost per tick k_keep = c_K·(σ²/2)·ln n. Lifetime **τ = ∞**.
  - **Check** (CT9's periodic renewal, every s ticks). The record is written at age 0, used at ages 0 … s−1, kicked each tick, and restored after s kicks by a check that reads the world, as CT9 assumes. The restore pays the Landauer cost of erasing the leak's entropy, kT·H(K_s), where K_s is the s-step snapping kernel row (H in nats). No read price beyond that, since one would be a free parameter. Cost per tick:
    J_chk(s) = [H(K_s) + x·Σ_{u=0}^{s−1} ε(u)]/s, with ε(u) = 1 − K_u(0, 0).
    s* := the integer argmin over 1 ≤ s ≤ 4000. Lifetime **τ = s***, the life of one written state.
  - **Fade** (no upkeep). Long-run cost per tick x·(1 − 1/n). Lifetime τ = 1/p_n, the §6 primary's first-confusion time.
  - **Rule:** the mode with the smallest cost per tick. An exact tie (relative 10⁻¹²) is reported, and the shorter lifetime is used.
- **The disk.** Keeping or checking a continuum pure state exactly needs infinite information, so I = ∞ and H = ∞, and both costs are infinite (PIM, ELEMENTARY). The disk fades with τ = 1, which is vacuous as in §6. It cannot be self-consistent here (pre-decided, not a test).
- **Paper expectation for s*.** When s·p_n ≪ 1: H(K_s) ≈ s·p(1 − ln(s·p) + h̃), with h̃ the kernel's own entropy term, and Σε ≈ p·s(s−1)/2. So J_chk/p ≈ const − ln s + x(s−1)/2, minimised at **s* ≈ 2/x, independent of n and σ.** Checking beats keeping and fading there, because p·ln(1/p) ≪ σ² ln n and p ≪ x. So where s*·p ≪ 1, T is design-independent: a horizon set by the stake.

### 8.3 Fixed-point rule (as §6.3, with T from §8.2)

- **Horizon.** T(n) := ⌊τ(n)⌋; τ = ∞ for kept designs. Robustness: ⌈τ⌉.
- **J unchanged.** J is SR_B §1's, noise-free, and A(T) is §7.1's argmin set (T ≤ 400). The heat sets the lifetime only. It is not added to J (§8.8).
- **Self-consistency.** n is self-consistent iff T(n) ≥ 2 and n ∈ A(T(n)). T(n) = 1 is vacuous. 2-cycles are as §6.3.
- **Kept designs are not self-consistent (PIM).** T = ∞ > π²/(4·d_min(n)), so by SR-b1(f) the disk is strictly cheaper.
- **Range.** n ≤ 1201 for every σ. A(T ≤ 400) ⊂ [5, 802], so n ∈ (802, 1201] cannot be self-consistent at T ≤ 400.
  - A design with 400 < T < ∞ is excluded if T > π²/(4·d_min) (SR-b1(f)), and is OPEN otherwise.
  - s* = 4000, the edge of the search, counts as OPEN.
- **Configurations.** E-M3h, O, F-M3h and F-mixed are scored. E-mixed is reported, not scored: it is degenerate by §7.2's PIM, which was known before this pre-statement, and the disk ties every even polygon there.

### 8.4 Grids (fixed now)

- **σ:** §6.4's 14 values, 0.4 … 0.0035.
- **x:** 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1. So 2/x runs from 400 down to 2. For x ≥ 4/3, s* = 1 and T = 1 is vacuous, so x above 1 is not scored.
- **Arms:** c_K ∈ {2 (primary), 4}; rounding ⌊ ⌋ (primary) and ⌈ ⌉.

### 8.5 The slope test (attraction), stated now

- **Map.** Φ(n) := min A(T(n)) on the configuration's menu (n ≤ 1201), with Φ = "∞" for kept or excluded designs.
- **Crossings.** At every sign change of Φ(n) − n between consecutive menu members n₋ < n₊ with finite Φ, compute the discrete slope s_c = (Φ(n₊) − Φ(n₋))/(n₊ − n₋). If n₋ or n₊ is itself a fixed point, the crossing is taken over its two menu neighbours.
- **Attracting** iff |s_c| < 1 at the crossing containing the fixed point, **and** iterating Φ from every menu n ≤ 1201 with finite orbit, for 60 steps, ends at that fixed point.
- **Repelling** iff |s_c| > 1. Reported for every crossing.

### 8.6 HIT / MISS / OPEN

- **A cell (configuration, x, σ) is a HIT** iff (i) exactly one self-consistent polygon n*, (ii) no 2-cycle, (iii) the disk is not self-consistent, and (iv) n* is attracting (§8.5).
- **A cell is a MISS** iff it has a 2-cycle, no self-consistent polygon, two or more, or a repelling crossing next to the only fixed point.
- **A cell is OPEN** by the range rule.
- **Per x:** HIT iff every scored cell at that x is a HIT; MISS iff any is a MISS; OPEN otherwise.
- **Overall score: HIT iff HIT at every x in the grid; MISS iff MISS at some x; OPEN otherwise.** This is as strict as §6.4's "any". A HIT band in (x, σ) is reported as a map, separately from the score.
- **Selection question (asked by the parent):** at each σ, does some x give a HIT cell? Reported, not scored.

### 8.7 Triviality test and paper prediction, before computing

- **Trivial: "stake relabelling".** At a HIT cell, T(n*) = ⌊2/x⌋ or ⌈2/x⌉ and T(n) is constant over the menu members around n* (n* ± 2 for the even and odd menus). Then n* = A(⌊2/x⌋), close to 4/x + 2, with no σ-dependence. The attraction then comes from a design-independent horizon, as in R1, and the noise does no work.
- **Trivial: "resolution ≈ noise".** Fixed points only where fade sets the lifetime, which is the §7.3 crossing again.
- **Genuine** iff some HIT cell has T(n) varying across n* ± 2, the n-dependence coming from s*(n) or from a mode switch, with |s_c| < 1. That would be a stable crossing set by the theory's rule and the noise together.
- **Paper prediction.** Where x ≫ σ√(2 ln(1/σ)) (roughly x ≥ 3σ√(2 ln(1/σ))), n* ≈ 4/x + 2 is far below the §7.3 crossing n_c(σ), so s*·p ≪ 1, checking wins, s* ≈ 2/x, Φ is flat, and the cell is a trivial HIT. Elsewhere s*·p is not small, p varies steeply with n, and the cell is expected to be a MISS (repelling or empty).
  - Some grid cells (σ = 0.4, all x) lie in the second region.
  - P(overall MISS) ≈ 0.8, P(OPEN) ≈ 0.05, P(HIT) ≈ 0.15.
  - P(at least 90% of predicted-HIT cells are HITs) ≈ 0.7.
  - P(some genuine HIT cell) ≈ 0.15.
- **Arm H∞ (information lifetime; paper, PIM, pre-decided).** If the horizon is the information's lifetime instead of one written state's, keep and check both give τ = ∞. Those designs are excluded by SR-b1(f), and the self-consistent set shrinks to §7.3's fade-only set. Same outcome as §7.3: MISS.
- **Arm c_K = 0 (CORE.md:78, "storage is cheap"; paper, PIM, pre-decided).** Keep costs 0 and strictly beats check and fade, so every polygon has τ = ∞ and none is self-consistent: MISS. This is why the primary uses the G-keep floor, whose decisive premise is separate-leak carriers (C12B_ORDER §9.4 S1). Where CORE.md:78's frozen-world, cancelling-leak case holds, SH-heat has no finite lifetime at all.

### 8.8 Not tested here

- **§7.10's version:** keep heat added to J. It needs the J-to-kT exchange rate, a free parameter.
- **The interruptible reading** (§6.7).
- **A read price** in the check mode.
- **The level arm** (§6.2) for the check mode's error measure.

### 8.9 Tools, checks and labels planned

- **Tools.** `selfhorizon/sh_heat.py`, run detached with a log, reusing §7's `argmin_sets.json`.
  - Eigenvalues of the circulant kernel: 1 − λ_k is computed directly as Σ_j q_j·2 sin²(πjk/n), to avoid cancellation. Σε is in closed form, with a series when s(1 − λ) < 10⁻⁴. H(K_s) is computed by FFT of λ^s. The first-order (s·p < 10⁻⁶) formulas are used where p underflows.
  - The s search runs on a log grid of about 80 values, then a scan of ±(3 + 5%) integers around the best.
- **Checks:**
  - (a) a full integer scan of s ≤ 4000 for n ≤ 61 at all σ, against the grid search;
  - (b) the FFT H against a direct matrix power for n ≤ 15;
  - (c) the closed-form Σε against direct summation;
  - (d) the first-order regime against the exact one at its boundary.
- **Labels:** cells, fixed points, slopes and maps are OBSERVED. Kept-design exclusion, the disk status and the H∞ and c_K = 0 arms are PIM. s* ≈ 2/x is a heuristic, plus an OBSERVED check.
