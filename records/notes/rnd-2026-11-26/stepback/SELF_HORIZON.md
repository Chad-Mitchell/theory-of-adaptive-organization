# SELF_HORIZON: is the stake the record-keeper's own persistence? A paper-only check of the self-consistency reframe

*26 Nov 2026, about 13:05–13:40 ET. Local note only (not committed or pushed). Paper only: no new numerical computing; the only arithmetic is the hand checks shown inline. Self-checked only; it needs a hostile review before it counts. Repo text read at the local clone `/workspace/theory-of-adaptive-organization` (`40c4060`); CORE.md and THEORY.md read, not edited. Labels: **PIM** = proved in-model (class named); **KNOWN**; **ELEMENTARY**; **HYP**; **OBSERVED** = a number already in the notes (file and section given), not recomputed here. Crossref checks for every DOI below: `selfhorizon/crossref_sh.txt` (script `selfhorizon/crossref_sh.py`).*

## 0. Result in five lines

1. **Audit (§1): 15 route inputs, A = 5, B = 8, C = 2.** The five A items are only **two independent inputs**: the horizon of the SR_B §1 class (SR-b1, SR-b2, SR-b4 and the compliant clue's growth objective are the same object four times) and CORE's ruin cap (C12c). The eight B items are structural conventions (channel class, mixing, target rule, pure jumps, menu, lattice, start, price extension) and are not stakes or horizons. So "ten routes, one input, CORE's own claim recurring" holds for about a third of the inputs, not all of them.
2. **Fixed point (§2): in the SR_B §1 class, τ(D) cannot be defined from the class's own objects without one of three things.** (a) A tautology: with τ = the design's own saturation time, every per-horizon optimum satisfies the condition, so it selects nothing (the hexagon is a PIM fixed point, and so are the square and triangle in a weak sense). (b) A reference rival: with τ = the crossover T₀ against the disk, the condition is non-trivial but uses the disk as the yardstick, which is the competitive requirement U again. (c) A new parameter: an error level, a noise strength, a buffer and ruin level, or an upkeep price. The class has no mechanism by which a record decays or costs anything to hold, so "the lifetime its records sustain" is ∞ for every design. That turns the fixed point into the design-first limit (F).
3. **What does come out clean (PIM, corollary of SR-b3/SR-b4 and the odd analogue): the disk is self-consistent only if its own lifetime is infinite.** For any lifetime map with τ(disk) finite and ≥ 2, or any bounded lifetime distribution with mass on T ≥ 2, the disk is not self-consistent. The input U becomes a property claim, "continuous records never degrade". That is a restatement with a sharper meaning, not a removal of the input.
4. **Circularity (§3):** the input moves; it is not removed. It goes into τ's definition (a rival set, a level, a noise, or a buffer), or it becomes the index of a family of fixed points. Existence is guaranteed only in the tautological version. Uniqueness holds (at most one) when τ(n) is nonincreasing in n, by monotonicity. Stability is not shown.
5. **Conclusion (§5): partly.** It holds as a unification: the horizon is CORE's ruin cap, which THEORY CT25 already writes as one parameter ε_r/T_h. It breaks at one point: in the SR_B §1 class, J(D, T) is nonincreasing in T and a static record costs nothing to hold (CORE.md:78), so the only parameter-free lifetime is τ ≡ ∞, and the fixed point is (F) restated. One checkable prediction for the version with physical degradation is stated in §5.

## 1. Audit: the chosen input of each route, classified

**Criterion, written before assigning.** (A) The input is a horizon or survival requirement on the record-keeper itself (how long it must stay useful, or how unlikely its ruin must be), so the reframe applies to it. (B) It is a modelling convention unrelated to persistence. (C) Unclear or mixed. A fit that needs a story beyond the input's own text counts as C or B. Whether an A input can actually be made endogenous is §2's question, not this one.

| # | route | chosen input that decides the outcome | where | class |
|---|---|---|---|---|
| 1 | C12b ordering (track vs keep) | the leak-channel class S1 (same-channel vs separate-leak). The two thresholds came from different classes, so they cannot be ordered | C12B_ORDER §9.1, §9.4 | **B** |
| 2 | C12b keep floor (G-keep) | the chosen second-moment cap (A), the write-first premise (W)/(P3′), and the keep horizon τ in Q̄ ≥ kTΓ((τ−t_w)/τ)ln(Var/D) − kT·S_range/τ. τ is a keep horizon in form, but the floor is used at τ → ∞ and the decisive premise is S1 | C12B_ORDER §8.1, §9.3, §9.4 | **C** (mixed: τ is persistence-shaped, while (A), (W) and S1 are conventions) |
| 3 | C12c onset at zero stake | the type and level of the ruin/accuracy cap. A stake-free cap (CT25 type: ruin when the tracked error reaches the buffer) forces memory at w = 0; a CT22-type cap does not apply there | C12C_ONSET §0.3, §4; STEPBACK §15 | **A** (ruin is non-persistence; the level B, ε_r stays free, and CORE.md:23, :44 lists the ruin cap as assumed) |
| 4 | C12CG cap-only worlds | the no-mixing rule, the per-record reading (outside the lock), and the polygons' non-convex (S, E) arrangement. The selecting knob is q or D, but the open miss comes from the first three | C12CG §2, §4, §11(a) | **B** |
| 5 | SR-b1 | a uniform competitive-ratio requirement: one design within a bounded factor of the best at every horizon (U) | SR_B §3, §8.1 | **A** |
| 6 | SR-b2 (mixtures) | the horizon distribution: geometric q, or uniform on 1..H | SR_B §1, §4, §8.4 | **A** |
| 7 | SR-b3 and the ROUND10 note | the target rule: M3h (any perfectly distinguishable vertex) vs M3c (antipode) | SR_B §8.5–§8.7 | **B** |
| 8 | SR-b4 | the order of limits: (P), per-H selection, vs (F), design fixed and then H → ∞ ("design first") | SR_B §9.5, §10.4 L4 | **A** (it says whether the design is committed before its horizon is known) |
| 9 | SR-b4 odd analogue | the pure-jump rule: every tick lands on a pure state. With mixed intermediate states every design ties at 1/T | SR_B §11, §11.4 | **B** |
| 10 | C1 | the per-site price κ (locality), the stake region T (2×2 plaquette), the vacuum, the greedy rule | C1 §1, §8.1 | **B** |
| 11 | C4 / C4′ | a fixed lattice frame; (I1) a boost-invariant price, (I2) a max-entropy premise, (I3) records off fixed sites; the bath temperature picks the frame (F-a) | C4_RECORD_ORDER §6; STEPBACK §16 | **B** |
| 12 | PIM Lemma D1 | the lead time k, the stake region T and the threshold κ ("the cut moves from κ to k and T") | PIM_LEMMA "Does not", amendment 2c | **C** (k is a usefulness horizon in words, but it is the task's look-ahead, and the class has no record decay; T and κ are conventions) |
| 13 | A2 | extending the dimension price P6 from parts to composites, and the interaction premise I at fixed parts | PREREG_DRAFT_A2 §1.2–§1.3 | **B** |
| 14 | C3v2 / Lemma R | a product (pure) start, the read cap M ≤ 2, and RC15 | PREREG_DRAFT_C3v2 §1, corrections; LEMMA_R | **B** |
| 15 | Compliant clue, one-piece objective | the long-run growth rate, t → ∞ (the "soft U"); C-flex additionally picks the same-channel class | CLUE_COMPLIANT addendum 3 §2 caveats; addendum 1 caveat | **A** (growth horizon); the C-flex channel choice is B and is counted in row 1's kind |

Not counted (no selection input): C12c-G‴ (encoder optimality; C12CG §12) and the Lean round-6 work on Lemma R (a proof under stated premises).

**Count: A = 5, B = 8, C = 2 (15 inputs).**
- **Independent A inputs: 2.** Rows 5, 6, 8 and 15 are one object, the horizon of the SR_B §1 class. Row 15 is the t → ∞ version of row 8's (F), and CLUE_COMPLIANT §3(i) uses SR-b1(f) for it. Row 3 is CORE's ruin cap.
- **The B items are not stakes.** CORE.md:23 says the heat bound "does not choose a stake, a link price, or a ruin cap". The B items are none of these. They are structure: which world, which channels, which moves, which start, which reading. This is STEPBACK §14's F2 pattern ("the world or rules were fixed first"), not the zero-stake pattern.
- **A wording correction for the brief.** CORE has no theorem named "zero-stake theorem". The nearest statements are CORE.md:23 (the heat bound does not choose w, a price or ε), CT33 (THEORY.md:495; the stake orders spend and error but is not chosen by them), and C12C_ONSET Theorem O(v) (at w = 0 memory is absent iff a stake-free cap is slack at the blind design; PIM in its class). "Nothing is selected without a stake" is a fair paraphrase of O(v) together with CORE.md:23 for stake-free classes, not a named CORE result.
- **Caution.** One reader assigned these classes, knowing the hoped-for answer. The count is weak evidence (as in STEPBACK C14-1). What it does show firmly is the B column: those inputs are visibly structural in their own text.

## 2. The fixed point in the SR_B §1 class

### 2.1 Objects available (nothing new added)

Designs D ∈ {n-gon, n ≥ 3} ∪ {disk}; the cost J(D, T) of SR_B §1 (pure jumps, Σd_t², target at d = 1); J*(T) = inf_D J(D, T); ρ = J/J*; d_min(n); and these facts:
- SR-b1(a)–(f) and §8.2–§8.3 (PIM): J ≥ 1/T; J(n, T) ≥ d_min(n); J(disk, T) = T·sin²(π/2T); every fixed n-gon loses to the disk for T > π²/(4·d_min(n)).
- SR-b3 (PIM, M3h rule): the (2T+2)-gon beats the disk at every T ≥ 2. The odd analogue (PIM, both rules, SR_B §11.4): the (2T+1)-gon beats it at every T ≥ 2. SR-b4 and the odd lcm family (PIM): for every H, some polygon beats the disk at every T ∈ [2, H].
- OBSERVED: the argmin at T is n = 2T + 2 at every listed T (SR_B §9.3); T₀(n) ≈ 2.0–2.16·√n for even n in 1,000–40,000 and ≈ 1.44·√n for odd n in 401–6,401 (SR_B §9.2, §10.4 L4); J(n, T) is flat beyond saturation (SR_B §4).

Two more facts, ELEMENTARY, proved here by hand:
- **(M) Monotonicity.** J(D, T+1) ≤ J(D, T), because staying put is allowed and costs 0 (SR_B §1), so a T-path padded with one zero step is a (T+1)-path at the same cost.
- **(Sat) Every polygon saturates.** An optimal path uses m non-zero steps, each costing ≥ d_min², and its cost is ≤ J(n, 1) = 1, so m ≤ 1/d_min(n)². Hence J(n, T) = J(n, ⌊1/d_min²⌋) for every T ≥ ⌊1/d_min²⌋. Define T_sat(n) := min{T : J(n, T′) = J(n, T) for all T′ ≥ T} ≤ 1/d_min(n)². For the disk, T·sin²(π/2T) is strictly decreasing for T ≥ 2 (J = 1 at T = 1 and T = 2, then 0.75, 0.586, …), so T_sat(disk) = ∞.

**Self-consistency, as specified.** D* is self-consistent under a lifetime map τ if D* ∈ argmin_D J(D, τ(D*)). Where τ(D*) = ∞ this is read as D* ∈ argmin_D lim_T J(D, T), the only reading available.

### 2.2 Candidate τ's, each checked for a new free parameter

**(τ1) Intrinsic: τ(D) = T_sat(D), the horizon at which the design's own cost stops improving.** No parameter and no rival: this is the design's own "design horizon" (STEPBACK §14(b)'s (n−1)/2, made exact by (Sat)).
- **Hexagon: a PIM fixed point.** d(v₀, v₁) = sin(π/6) = ½ (k − n/2 = −2, even); d(v₀, v₂) = sin(π/3)/cos(π/6) = 1 (odd). Each non-zero step has d ≥ ½, and Σd ≥ 1. So either one step with d = 1 (cost 1) or ≥ 2 steps with d² ≥ ¼ (cost ≥ ½). Hence J(6, 1) = 1 and J(6, T) = ½ for T ≥ 2, so T_sat(6) = 2. SR-b1(a) gives J*(2) ≥ ½, and the hexagon attains it. So the hexagon is optimal at its own τ.
- **Square and triangle: weak fixed points.** d_min = 1 (square: sin(π/4)/cos(π/4) = 1; triangle: the classical simplex), so J ≡ 1 and T_sat = 1. At T = 1 every design costs exactly 1 (J ≥ 1/T, and the direct jump costs 1). So they tie for optimal at their own τ (PIM, ELEMENTARY).
- **Disk.** T_sat = ∞, and lim_T J(disk, T) = 0 < d_min(n) ≤ J(n, ∞) for every n (SR-b1(b),(c)). So the disk is the unique minimizer of the limit cost: it is a fixed point in the limit reading. That is exactly (F) (SR_B §9.5).
- **Every (2T+2)-gon (HYP, from OBSERVED).** If the observed argmin rule n*(T) = 2T+2 holds, and the (2T+2)-gon saturates at T (its path is T unit steps to v_T), then every even n ≥ 6 is a fixed point. Hand check at n = 10: d(v₀, v₁)² = sin²(π/10) = 0.0955, and v₄ is at d = sin(2π/5)/cos(π/10) = 1. J(10, T) = 4·0.0955 = 0.382 for T ≥ 4, and the larger single steps (0.382 or 0.654 each) are worse, so T_sat(10) = 4 = (10 − 2)/2, as the rule needs.
- **What τ1 selects: nothing.** Its fixed-point set contains {triangle, square (weak), hexagon, disk (limit)}, PIM, and very likely every even n ≥ 6 (HYP). The reason is structural: n ↦ T_sat(n) is the inverse of T ↦ n*(T), so the condition holds identically along the per-horizon selection curve. **The old input T is not removed; it has become the label of the fixed point.** The family runs from classical designs (τ = 1) to the disk (τ = ∞).

**(τ2) Rival-referenced: τ(n) = T₀(n), the last T up to which n beats the disk at every T ∈ [2, T].** No new number, but it needs a chosen reference rival, the disk. With every rival in play (J* instead of the disk), τ(n) = {T : n is optimal at T}, and the condition is a tautology again, like τ1.
- **Hand checks** (closed-form distances, SR_B §8.6; disk values T·sin²(π/2T)). T₀(6) = 4 (0.5 < 0.586 at T = 4; 0.5 > 0.477 at T = 5). T₀(10) = 6 (0.382 < 0.402 at T = 6; > 0.347 at T = 7). T₀(14) = 8: J(14, ∞) = 6·sin²(π/14) = 0.297, against 0.3045 at T = 8 and 0.2714 at T = 9; checked by hand at T = 4, 5 (0.495 < 0.586; 0.396 < 0.477) and taken from SR_B §9.2 at T = 2, 3.
- **The map** Φ(n) := n*(T₀(n)) = 2T₀(n) + 2 (OBSERVED argmin rule). By hand: Φ(6) = 10, Φ(10) = 14, Φ(14) = 18, so Φ(n) > n for small n. If T₀ ≈ 2√n persists, Φ(n) ≈ 4√n + 2 < n for n ≳ 20. A fixed point means T₀(n) = n/2 − 1 = T_sat(n): **the polygon stops beating the disk exactly when it saturates.** At n = 6, 10, 14, T₀ − T_sat = +2.
- **Existence: HYP.** On a bracket [n_a, n_b] with Φ(n_a) > n_a and Φ(n_b) < n_b, a fixed point exists if Φ is nondecreasing there (Tarski 1955, KNOWN). Monotonicity of T₀ is not shown, and SR_B §4 says the wins "follow how the vertex grid lines up", so it may fail. The crossing lies in n ≈ 14–30, where no T₀ is in the record. Not computed here (paper-only unit).
- **Reading.** Even if it exists, τ2 selects "the polygon whose lead over the disk lasts exactly its own design horizon". The disk enters as the privileged yardstick only because it is the one design with bounded ρ at every T, SR-b1(d)–(e). **That is the competitive requirement U in another form.** It also depends on the target rule, because T₀ differs by parity (≈ 2√n even, ≈ 1.44√n odd).

**(τ3) Time until the tracking error exceeds a level.** The SR_B §1 class has no drift, no noise and no decay, so there is no tracking error. This needs a new noise model plus a level ℓ: **two new parameters.** The input moves.

**(τ4) CT22/CT25 ruin time.** It needs a reserve or buffer B, a noise σ, a ruin level ε_r (and H for CT25). None exists in the class. **New parameters (B, σ, ε_r).** The input moves, into exactly the object CORE.md:23 and :44 list as assumed.

**(τ5) Budget lifetime, τ = 1/J (forced; listed so it is not reached for later).** It looks parameter-free because J is dimensionless. But it equates one tick with one unit of cost, a unit convention: the tick is a model convention (SR_B §10.4 L4). Its fixed points satisfy T·J(D, T) = 1, which is equality in SR-b1(a): T = 1 for every design, and the hexagon at T = 2. The disk satisfies T·sin(π/2T) = 1 only at T = 1, since T·sin(π/2T) increases toward π/2 (PIM, ELEMENTARY). There is no physical reason a lifetime should be an inverse transport cost, so this counts as a forced fit and is not used.

**(τ6) Self-chosen horizon, the parameter-free reading of "the lifetime its records sustain".** In this class a record never decays, and by CORE.md:78 a static record in a frozen world costs zero ongoing heat after the write. So every design sustains its records forever: τ ≡ ∞, with no parameter. By (M), a design that may pick its own horizon picks T → ∞. The fixed point is then the disk, the unique minimizer of the limit cost, and **that is (F), the design-first limit, restated** (SR_B §9.5, §10.4). The limit is also not attained by any history: no finite path of the disk completes the move at cost 0. What is "selected" is the infimum of a never-finished task.

### 2.3 What the fixed point selects

- **With a parameter-free τ (τ1, τ6): nothing new.** τ1 gives a family of fixed points (the old horizon as its label). τ6 gives the disk via (F).
- **With τ2: possibly one polygon near n ≈ 14–30 (HYP),** but only with the disk chosen as the reference rival, which is U.
- **With τ3 or τ4: something, at the price of new parameters.**
- **A clean statement that does follow (PIM, corollary).**

  **Proposition SH1.** In the class of SR_B §1, let τ assign each design a finite lifetime, or a lifetime distribution with bounded support. If τ(disk) ∈ [2, ∞), or τ(disk)'s distribution puts mass on T ≥ 2, then the disk is not self-consistent.

  *Proof.* At a finite T ≥ 2 the (2T+1)-gon is strictly cheaper than the disk under both target rules (SR_B §11.4), and the (2T+2)-gon is cheaper under M3h's rule (SR-b3). For a bounded distribution with mass on T ≥ 2, use the lcm family (SR-b4 corollary and its odd analogue): one polygon strictly beats the disk at every T in the support's range [2, H], and ties at T = 1. ∎

  **Consequence.** The disk is self-consistent only if τ(disk) = ∞ (read as (F)) or τ(disk) = 1 (where every design ties). So in this class, **"the continuum is selected" is equivalent to "the continuum's own records never degrade"**, plus the (F) reading of an infinite lifetime. This turns the U input into a property claim about the design. The claim is sharper, but it is still a claim the cost does not supply. Unbounded-support lifetimes (geometric) stay as in SR_B: a polygon wins at every tested q ≤ 0.999 (OBSERVED), and all q is HYP.

## 3. Circularity check on the reframe itself

- **Does the fixed point remove the chosen input? No.** It goes to one of three places:
  - into the **label** of a family of fixed points (τ1: every per-horizon optimum is self-consistent);
  - into τ's **definition**: a reference rival (τ2, which is U), or a level, noise, buffer or ruin cap (τ3, τ4, which is CORE's ε);
  - into the **order of limits** (τ6, which is (F)).
- **Is it the competitive ratio or (F) restated?** τ2 is the competitive requirement with the disk as yardstick. τ6 is (F) exactly. τ1 is the per-horizon selection read backwards. None is independent of the routes it was meant to replace.
- **Guaranteed?** Only τ1, trivially; every T has a fixed point. For τ2, existence is HYP (Tarski would give it if Φ is monotone; not shown). For a noise-based τ, see the next point.
- **Unique?** τ1: no, a whole family. For any τ(n) that is **nonincreasing** in n (finer designs, smaller d_min, shorter-lived), combined with the OBSERVED increasing rule n*(T) = 2T + 2: Φ = n*∘τ is nonincreasing. **A nonincreasing map on the integers has at most one fixed point** (if Φ(a) = a and Φ(b) = b with a < b, then b = Φ(b) ≤ Φ(a) = a). It may have none, giving a 2-cycle instead. ELEMENTARY.
- **Stable?** τ1 is neutral: every point is fixed and nothing attracts. τ2: if T₀ ≈ 2√n holds near the crossing, Φ′ ≈ 2/√n ≈ 0.45 < 1 there, so it would be locally attracting (HYP, from an OBSERVED large-n fit used outside its range). A nonincreasing Φ (noise-based τ) iterates by oscillating; it is stable iff |slope| < 1 at the crossing, which is not shown.
- **Hidden-input test, applied to the strongest form.** The most natural non-trivial lifetime is physical: records degrade because neighbouring pure states get confused under noise, so τ(n) falls as d_min(n) falls. That needs a noise strength σ. σ is a **world** parameter, of the same kind as r, v, Γ and kT that the theory already takes as given (A2 §2's drift rate "the cost sees"). It is not a weighting chosen by the modeller. So the strongest version moves the input **from the modeller's choice to a measurable property of the substrate.** That is a real change of kind. It is still a new parameter in the SR_B §1 class, so by the brief's own test the reframe "just moves the input" there.

## 4. Prior art (every DOI checked on Crossref this session; `selfhorizon/crossref_sh.txt`)

- **Autopoiesis.** Varela, Maturana & Uribe 1974, *BioSystems* 5:187–196, doi 10.1016/0303-2647(74)90031-8. Maturana & Varela 1980, *Autopoiesis and Cognition* (Boston Studies in the Philosophy of Science), doi 10.1007/978-94-009-8947-4. KNOWN: a living system is defined by the network that produces its own components and boundary, so persistence is the organizing condition, not an external goal. Credit: the reframe's slogan "the stake is the system's own persistence" is theirs in substance. They give no cost and no lifetime scale. Nothing here formalizes autopoiesis.
- **Free-energy principle and self-evidencing.** Friston 2010, *Nat. Rev. Neurosci.* 11:127–138, doi 10.1038/nrn2787. Friston 2013, "Life as we know it", *J. R. Soc. Interface* 10:20130475, doi 10.1098/rsif.2013.0475. Hohwy 2016 (issued online 2014 per Crossref), "The self-evidencing brain", *Noûs* 50:259–285, doi 10.1111/nous.12062. KNOWN: a system that persists (stays within a bounded set of states) can be read as minimizing a bound on surprise about its own states; its "preferences" are its own characteristic states. That is the closest published form of "the stake is set by the system's own continued existence". It needs a generative model and a characteristic set, both specified. In our terms that is a level, which is τ3's input.
- **Viability theory.** Aubin 2009, *Viability Theory* (2nd ed., Birkhäuser), doi 10.1007/978-0-8176-4910-4; Aubin, Bayen & Saint-Pierre 2011, *Viability Theory: New Directions*, doi 10.1007/978-3-642-16684-6. KNOWN: the viability kernel is the set of states from which some control keeps the system inside a constraint set K for all time (or until a capture time). Persistence is a constraint, not a weight. The analogue here is the CT25 cap, and K is given, which is the τ3/τ4 input. The infinite-time kernel is the τ6 reading.
- **Semantic information.** Kolchinsky & Wolpert 2018, *Interface Focus* 8:20180041, doi 10.1098/rsfs.2018.0041 (text read this session on arXiv 1806.08053). KNOWN and directly on point: semantic information is the information causally necessary for a system to keep its viability (negative entropy) at a time τ. Their definition depends on three choices they list explicitly: "the system/environment decomposition", "the timescale τ" and "the initial distribution". In §VI they propose fixing τ "objectively" by maximizing the value of information over τ. That is an outside rule, not a self-consistency, and it is the move this note checks. **Their framework already carries τ as a declared input.** This is published support for §3: making persistence the stake leaves a timescale to fix.
- **Closure to efficient causation (Rosen).** Rosen 1958, "A relational theory of biological systems", *Bull. Math. Biophys.* 20:245–260, doi 10.1007/BF02478302 ((M,R)-systems). Letelier, Soto-Andrade, Guíñez Abarzúa, Cornish-Bowden & Cárdenas 2006, *J. Theor. Biol.* 238:949–961, doi 10.1016/j.jtbi.2005.07.007 (organizational invariance and metabolic closure in (M,R) terms; Crossref's title field drops "(M,R)"). Rosen's *Life Itself* (1991) is cited without a DOI; none was checked. KNOWN: an organism is closed to efficient causation, since every catalyst is produced inside. The fixed-point form "D* optimal at τ(D*)" has the shape of such a closure. Rosen's closure is a structural condition and fixes no timescale.
- **Fixed points.** Tarski 1955, *Pacific J. Math.* 5:285–309, doi 10.2140/pjm.1955.5.285 (monotone maps on complete lattices have fixed points), used for τ2's conditional existence.
- **Already in the notes and reused:** Kelly 1956 (10.1002/j.1538-7305.1956.tb03809.x) and Peters 2019 (10.1038/s41567-019-0732-0), for the growth-objective reading (row 15); Zilberstein, Charpillet & Chassaing 2003 (10.1023/A:1024412831598), for contract vs interruptible horizons (see §5's caveat). All three were re-checked on Crossref this session.
- **Checked but not needed:** England 2013, *J. Chem. Phys.* 139:121923, doi 10.1063/1.4818538 (statistical physics of self-replication; persistence-weighted dissipation bounds). It is recorded in the Crossref file only.
- **Not found:** a statement that, in a GPT-design selection problem, the continuum is self-consistent iff its records last forever (SH1). "Not found" is not "new". SH1 is an ELEMENTARY corollary of SR-b3, SR-b4 and the odd analogue.

## 5. Conclusion: does it hold together on paper? Partly.

**What holds.**
- The horizon cluster (rows 5, 6, 8, 15) and CORE's ruin cap (row 3) are one input. THEORY CT25 (THEORY.md:402) already writes a horizon and a ruin level as one parameter: over a horizon T_h the buffer must satisfy B ≥ σ·τ^H·z(ε_r·τ/T_h), so T_h and ε_r enter only through ε_r/T_h (ELEMENTARY reading of a PIM statement).
- "The stake is persistence" is therefore literally the ruin cap, which CORE places outside the sum as an assumed input (CORE.md:23, :27, :44).
- In the SR_B §1 class the fixed-point form gives SH1 (PIM): the disk is self-consistent only if its own records never degrade.

**Where it breaks: one specific point.**
- In the SR_B §1 class, J(D, T) is nonincreasing in T (M), and a static record costs nothing to hold (CORE.md:78). So the only lifetime definable from the class's own objects without a new parameter is τ ≡ ∞ (or the design's saturation time, which makes every per-horizon optimum self-consistent).
- With τ ≡ ∞ the fixed point is the design-first limit (F) restated, and its "selection" is the infimum of a move that never completes.
- A non-trivial self-consistency needs something that makes persistence cost or fail, such as a decay, an upkeep or a noise. The class has none, and adding one adds its parameter.
- So the reframe does not remove the input. At best it moves it from a chosen weighting to a physical degradation rate. That is a change of kind worth keeping, but it is not a derivation.
- Eight of the fifteen inputs (B) are untouched by the reframe in any version.

**The one checkable prediction (for the version with physical degradation; HYP until computed).**
- Add to the SR_B §1 class a per-tick vertex-confusion noise of strength σ > 0. Finer designs then have shorter record lifetimes, so τ(n) is nonincreasing in n, and the disk's lifetime is finite. Score each design at its own lifetime (contract reading, horizon known in advance).
- **Prediction:**
  - (i) the disk is not self-consistent at any σ > 0 (this part follows from SH1 once τ(disk) < ∞);
  - (ii) there is **at most one** self-consistent polygon (ELEMENTARY, from monotonicity);
  - (iii) the checkable part: one exists, rather than a 2-cycle, at each tested σ, and its size grows without bound as σ → 0.
- **A miss** would be a 2-cycle at some σ, or a self-consistent size that stays bounded as σ → 0. Either would show that the self-consistency condition does not fix the design even when persistence is made physical.
- **Caveat stated now:** a faithful persistence model is interruptible (the record does not know when it will be lost), not a contract with a known horizon. The interruptible version is not in the record (SR_B §8.8 cites contract vs interruptible), and it could change (ii).
- This would be a computation and is not run here.

**Rescore (§13 scale, one line).** "SH-noise" (the prediction above): p(exists, unique, grows) 0.5, V 2 (a physical-degradation reading of U, still with σ as an input); p(2-cycle or bounded) 0.5, V 2.5 (it would show that self-consistency does not fix the design). EIV 2.25 over ≈ 3 h → **≈ 0.75 per hour**, below the Lean items and about level with C-flex. Not promoted by this note; for the parent to rank.

## 6. SH-noise pre-statement (written 26 Nov 2026, about 13:15 ET, before any SH-noise number is computed; §§0–5 stand as written)

*The SHA-256 of this block, the bytes from the "## 6." heading line through the end of §6.9, is logged in WORKLOG.md before any computing. Nothing in §6 may be edited afterwards. Results go in §7.*

### 6.1 Why a leak, and which one (primary and robustness arm)

- **Premise taken from the theory.** The keep floor (C12B_ORDER §8.2, §9.1, §9.4: Q̄ ≥ 2kTΓ·I, separate-leak carriers) says a physical record relaxes toward its equilibrium unless it is paid for. The SR_B §1 class has no such leak, which is §5's break point. SH-noise adds one, with one physical rate.
- **Primary: angular diffusion plus snapping ("vertex confusion").**
  - Each tick, the stored pure state at angle φ is kicked to φ + θ, with θ ~ N(0, σ²) wrapped on the circle.
  - The record is then held at a pure state of its design, as SR_B §1's pure-jump rule requires. A polygon snaps to the nearest vertex. The disk keeps φ + θ, since every angle is pure.
  - A polygon record is **confused** in a tick iff θ (wrapped) lands outside its own arc (−π/n, π/n). Per-tick confusion probability: p_n(σ) = P(|θ|_wrapped > π/n).
  - Why primary: the keep floor is derived for continuous carriers (an OU memory, Fokker–Planck, log-Sobolev). Its leak consists of small continuous kicks. On the circle of pure states the analogue is rotational diffusion. Its ensemble mean decays toward the centre (the maximally mixed state) by the factor e^{−σ²/2} per tick, so it is a leak toward the centre with rate Γ = σ²/2 per tick.
- **Robustness arm R1: depolarizing replacement.** Each tick, with probability r the record is replaced by a uniformly random pure state of its design. Matched to the same ensemble leak rate: r := 1 − e^{−σ²/2}. Confusion probability: r(1 − 1/n) for an n-gon, r for the disk. Same σ grid.
- **What noise does not touch.** The transport cost J(D, T) stays exactly SR_B §1's, computed noise-free. The noise sets only the lifetime, the horizon at which the design is scored. The heat of holding the record against the leak (the keep floor itself) is **not** added to J. That is a stated limit: SH-noise tests the self-consistency rule, not the full cost.

### 6.2 Lifetime τ(D, σ): no level parameter in the primary

- **Primary (level-free): the mean time to the first change of the held record.** τ(n, σ) := 1/p_n(σ) (geometric first-confusion time). The disk's held state changes in every tick with probability 1 (θ ≠ 0 almost surely, and there is no snapping), so τ(disk, σ) = 1.
- **Horizon used:** T(D) := ⌊τ(D, σ)⌋, integer ticks. Robustness: ⌈τ⌉.
- **Level arm L (for the disk, and as a check).** "Any change" is level-free for polygons but strict for the disk. So a second lifetime is reported: τ_δ(D, σ) := the mean exit time of the held record from {states at operational distance < δ from the start}. Here δ ∈ {0.1, 0.2, 0.3, 0.5} is dimensionless (operational distance ∈ [0, 1]).
  - Polygons: an exact Markov chain on the vertices, with snapping kernel q_j = P(θ ∈ arc of v_j); mean exit time by a linear solve.
  - Disk: the discrete-tick Gaussian walk exiting the arc {|φ| < φ_δ}, sin(φ_δ/2) = δ, computed by a Nyström discretization. For δ < d_min(n), τ_δ(n) = 1/p_n, the primary.
  - **Insensitivity criterion, fixed now:** the qualitative items of §6.4 (exists, unique, no 2-cycle, disk status, monotone growth) must be the same at every δ in the set. Prefactors and exponents are reported, not scored.

### 6.3 Fixed-point rule

- **Menus.** (E) even n ∈ [4, N_E] plus the disk; (O) odd n ∈ [3, N_O] plus the disk; (F) all n plus the disk.
- **Target rules.** M3h (any vertex at d = 1) and the mixed rule (antipode for even n, the farthest vertices for odd n). For odd n both rules give the same targets. So there are five configurations: E-M3h, E-mixed, O, F-M3h, F-mixed.
- **Definitions.**
  - A(T) := argmin over the menu of J(·, T), with ties counted within relative 10⁻¹².
  - **n is self-consistent** iff T(n) ≥ 2 and n ∈ A(T(n)).
  - T(n) = 1 is **vacuous**: every design costs exactly 1 at T = 1, so nothing is selected. It is reported, not counted.
  - **The disk is self-consistent** iff T(disk) ≥ 2 and disk ∈ A(T(disk)).
- **2-cycle:** a ≠ b, both with T ≥ 2, b ∈ A(T(a)) and a ∈ A(T(b)), neither self-consistent.
- **Also reported:** the map Φ(n) := min A(T(n)); the continuous crossing n_c where Φ(n) − n changes sign; and the discrete slope |ΔΦ/Δn| across it (stability: < 1 attracting, > 1 repelling).
- **Range.** J(n, T) is computed exactly for T ≤ 400 for every n ≤ 4001 (even and odd), plus sparse grids (even to 64,000, odd to 16,001).
  - A polygon with T(n) > 400 is excluded as **proved not self-consistent** if T(n) > π²/(4·d_min(n)), by SR-b1(f) (the disk is strictly cheaper there). Otherwise it is **OPEN** at that σ.
  - A σ whose candidate needs T > 400, or whose argmin sits at the edge of the computed n-range, is **OPEN** at that σ.
- **The disk is decided by SH1 (§2.3, PIM), not by the computation.** Wherever T(disk) ≥ 2, some polygon is strictly cheaper, so the disk is not self-consistent. In the primary, T(disk) = 1, which is vacuous. This HIT item is pre-decided and is not a test.

### 6.4 HIT / MISS / OPEN (scored on the primary; σ grid fixed now)

- **σ grid:** 0.4, 0.3, 0.2, 0.15, 0.1, 0.07, 0.05, 0.035, 0.025, 0.018, 0.012, 0.008, 0.005, 0.0035.
- **HIT:** in all five configurations and at every σ in the grid, (i) exactly one self-consistent polygon n*(σ), (ii) no 2-cycle, (iii) the disk is not self-consistent, and (iv) n*(σ) is nondecreasing as σ falls and grows over the grid. A fitted log-log exponent n* ∝ σ^{−β} is reported.
- **MISS:** in any configuration, at any σ in the grid: a 2-cycle, no self-consistent polygon, two or more, n* bounded (no growth over the grid), or the disk self-consistent at some σ > 0.
- **OPEN:** neither of the above, including any σ that is OPEN by the range rule. Also OPEN if the level arm L changes a qualitative item.
- R1 and the ⌈τ⌉ rounding are reported as robustness and are not scored. If either changes a qualitative item, that is said plainly.

### 6.5 Expected outcome, from paper, before computing

- **Continuous crossing.** If the OBSERVED argmin rule n*(T) = 2T + 2 holds (E-M3h), the crossing solves n ≈ 2/p_n(σ) + 2, with p_n ≈ erfc(x) and x = π/(√2·nσ).
  - Asymptotically x² ≈ ln(1/σ) + O(ln ln), so **n_c ≈ (π/σ)/√(2 ln(1/σ))**. Hand check: σ = 0.01 gives n_c ≈ 125–130 (x ≈ 1.7).
- **Stability.** dτ/dn = −2x²τ/n, so |Φ′| ≈ 2x² ≈ 6 at σ = 0.01, which is > 1. **The crossing is expected to be repelling.**
- **Integer existence.** On the integers, Φ(n) − n changes by about 2x² per step near the crossing, so it can step over 0. **Expected: at some grid σ there is no exact self-consistent polygon**, with an oscillating orbit or a 2-cycle instead.
  - Uniqueness, when a fixed point exists, is ELEMENTARY: Φ is nonincreasing, by τ nonincreasing in n and A(T) nondecreasing in T. Both are to be checked numerically.
- **Prior for the scored outcome:** P(MISS) ≈ 0.6 (mostly "no exact fixed point" or a 2-cycle at some σ), P(HIT) ≈ 0.25, P(OPEN) ≈ 0.15.
- **R1 expectation.** τ ≈ 1/r is nearly design-independent, so n* ≈ 2/r + 2 ≈ 4/σ². A pure horizon relabelling (β = 2), with |Φ′| ≈ 0, so it is stable.
- **L expectation.** For δ ≫ d_min, τ_δ ≈ φ_δ²/σ², nearly design-independent, so n* ≈ 2φ_δ²/σ² (β = 2, prefactor ∝ φ_δ²).

### 6.6 Triviality checks, stated now

- **Trivial ("resolution ≈ noise"):** the primary fitted β ∈ [0.8, 1.3] **and** n*·σ·√(2 ln(1/σ)) constant within a factor 1.5 over the grid.
  - This is the known fact that a constellation or quantizer resolves about range/σ points under noise σ (Shannon 1949; optimal quantizer size under noise). The cost J would be doing no work beyond the argmin rule 2T + 2.
- **Trivial ("horizon relabelling"):** β = 2 with n* ≈ 2τ + 2 and τ design-independent (R1, L).
- **Non-trivial:** β outside [0.8, 1.3] in the primary, or a prefactor traced to J's geometry (for example π²/4, or the d_min structure) rather than to the confusion threshold, or a qualitative difference between the even and odd menus or between the two target rules.

### 6.7 The interruptible version (not computed)

- Here the horizon is known in advance (contract reading). In the interruptible reading the record's end time is random (geometric, mean τ) and the path cannot use it.
- Expected effect: horizon averaging favours finer designs. In the Bayes contract-mixture of SR_B §8.4, n* ≈ 0.06–0.1/(1−q)² (OBSERVED), which would give β ≈ 2 in p_n, not ≈ 1.
- An interruptible path must also be good at every stop time, which pushes toward the competitive (U-like) criterion. That is exactly the input under study.
- So the interruptible version **could change β and the stability**. It is named as the main untested alternative, not run here.

### 6.8 Computation plan (tools)

- An exact forward DP with the SR_B §8.4 step cap, in C. Distances come from the closed form for even n (SR_B §8.6) and from the breakpoint method (review_srb4 `rv_core.dist_row`) for odd n.
- Cross-checks: `sr_b4/curves_even.npy` (M3h), and `rv_core.J_circ` (full circular DP, no cap) on a sample.
- p_n(σ) in mpmath (wrapped normal, 50 digits).
- Argmin gaps below 10⁻⁹ relative are rechecked in mpmath.
- Scripts and outputs in `selfhorizon/`.

### 6.9 Labels planned

- Fixed points, cycles, n*(σ), β: OBSERVED.
- Disk status: PIM (SH1).
- The exclusion of polygons with T > π²/(4d_min): PIM (SR-b1(f)).
- Uniqueness given monotonicity: ELEMENTARY.
- Any scaling law: OBSERVED fit, plus the §6.5 heuristic.

## 7. SH-noise results (computed after §6; §6's hash is logged in WORKLOG at 13:13 ET; scripts and outputs in `selfhorizon/`)

*Appended in parts, as results land. A tool abort interrupted the level-arm run at about 13:50 ET. After it: §6 was present, its SHA-256 still matched the logged 917f7849…83f4, and nothing in §6 had changed. Every computation below ran after the hash was logged: curves at 13:14, the primary/ceil/R1 arms at 13:15–13:22, and the level arm restarted detached at about 14:00. The WORKLOG line stamped "13:40" for §§0–5 was really written at about 13:07; a correction line is logged.*

### 7.1 Tools and checks (OBSERVED)

- **Curves.** `shdp.c` computes exact J(n, T), T ≤ 400, under both target rules: every n from 3 to 4001, plus 34 odd n from 4,003 to 16,001. The even M3h grid to 64,000 comes from `sr_b4/curves_even.npy`. Run: `run_curves.py` → `curves_sh.npz`.
- **Cross-checks** (`xcheck.out`):
  - against `sr_b4/curves_even.npy`: max difference 6.7e−16;
  - against the reviewer's full circular DP (`rv_core.J_circ`, no step cap; n ≤ 31, T ≤ 12): 9.4e−16;
  - closed-form distances (even: SR_B §8.6; odd: d(v₀, v_k) = sin(πk/n)/cos(π/2n)) against the breakpoint method: 2.2e−16.
- **Argmin sets** (`argmin_sets.out`).
  - For T ≥ 2, A(T) is a single design in E-M3h, O, F-M3h and F-mixed. The smallest relative gap to the runner-up is 1.25e−3, so no high-precision recheck was needed.
  - The largest polygon in any A(T) is 802 (M3h) or 801 (odd). That is far inside the computed range: no edge hits at T ≥ 2.
  - A(T) = {6, 6, 10, 12, 22, 42, 102, 202, 402, 802} at T = 2, 3, 4, 5, 10, 20, 50, 100, 200, 400 (M3h), and {5, 7, 9, 11, 21, 41, …, 801} (odd, = 2T + 1).
- **Noise.** p_n(σ) is the wrapped normal computed in mpmath at 50 digits (`sh_noise.py`).

### 7.2 A correction to §6.3, found on reading the E-mixed data (PIM, ELEMENTARY)

- **Claim.** Under the antipode rule, every even polygon costs at least the disk: J(n, T) ≥ T·sin²(π/2T) for every even n and T.
- *Proof.* The polygon is inscribed in the unit circle, so its width is ≤ 2 and d(u, w) ≥ |u − w|/2 = sin(φ/2). This is the review's bound, SR_B §10.5 L2. A pure path from v₀ to the antipode has angular steps summing to ≥ π. SR_B §8.3's convexity step then gives Σ sin²(φ_t/2) ≥ T·sin²(π/2T). ∎
- **Numerical check:** the minimum over even n of J_mix − disk is −3.3e−16.
- **Consequence.** In the E-mixed menu (even polygons with the antipode target, plus the disk), the disk is co-optimal at every T, and the 4T-gon multiples tie it. §6.3's sentence "the disk is decided by SH1" is **wrong for E-mixed**. SH1 needs odd polygons or M3h's even targets.
- So in E-mixed **the disk is self-consistent whenever T(disk) ≥ 2.** That never happens in the primary (T(disk) = 1). It does happen in R1 and in the level arm. E-mixed is a degenerate configuration, with every cost tied to the disk's at the argmin. It is reported as such, and §6.4's rules are applied to it unchanged.

### 7.3 Primary arm (scored): angular kicks, level-free lifetime τ = 1/p_n, T = ⌊τ⌋ (`sh_noise.out`, `fit_cross.out`)

| σ | self-consistent polygons: E-M3h · O · F-M3h · F-mixed | continuous crossing n_c (F-M3h) | discrete slope at the crossing, F-M3h (ΔΦ/Δn) |
|---|---|---|---|
| 0.4 | none · 7 · none · 7 | 6.5 | (12 → 6 over 6 → 7) |
| 0.3 | none · 9 · none · 9 | 9.5 | |
| 0.2 | 12 · none · 12 · none | 11.5 | |
| 0.15 | none · none · none · none | 14.5 | 2 |
| 0.1 | none ×4 | 19.5 | 4 |
| 0.07 | none ×4 | 25.5 | 4 |
| 0.05 | none ×4 | 33.5 | 4 |
| 0.035 | none ×4 | 44.5 | 6 |
| 0.025 | none ×4 | 59.5 | 6 |
| 0.018 | none ×4 | 78.5 | 6 |
| 0.012 | none ×4 | 110.5 | 6 |
| 0.008 | none ×4 | 157.5 | 6 |
| 0.005 | none ×4 | 238.5 | 8 |
| 0.0035 | none ×4 | 327.5 | 8 |

- **No 2-cycles** in E-M3h, O, F-M3h or F-mixed at any σ.
- **The disk:** T(disk) = 1 at every σ, which is vacuous.
- **Polygons with T > 400:** all excluded by SR-b1(f), PIM. None is OPEN.
- **Vacuous designs (T = 1):** large n at every σ.
- **E-mixed (degenerate, §7.2):**
  - Several tied self-consistent polygons at every σ: 1, 2, 3, 6, 8, 11, 16, 23, 33, 49, 73, 106, 169 and 244 as σ falls.
  - 2-cycles from σ ≤ 0.05 on: 2, 6, 9, 15, 26, 62, 164 and 312 pairs.
- **What happens.** At every σ the map Φ(n) = argmin at the design's own lifetime crosses the diagonal (Φ − n changes sign). It crosses with a steep negative slope, |ΔΦ/Δn| = 2–8 (median 5–6), so it **jumps over** the diagonal. The integer equation n ∈ A(T(n)) then has no solution at 12 of 14 grid σ (M3h) and 12 of 14 (odd).
  - §6.5 predicted this before computing: a repelling crossing with |Φ′| ≈ 2x², about 6 at σ = 0.01; Φ − n steps over 0.
  - The slope grows slowly as σ falls (2 → 8), as 2x² ∝ ln(1/σ) predicts.
- **Scaling of the crossing (OBSERVED).**
  - Fitted n_c ∝ σ^(−β): β = 0.81 over the whole grid, 0.86 for σ ≤ 0.05 (all four non-degenerate configurations agree within 0.02).
  - n_c·σ·√(2 ln(1/σ)) = 3.3–4.4 over the grid, against §6.5's paper estimate π.
  - So **n_c ≈ (4 ± 0.5)/(σ·√(2 ln(1/σ)))**.
- **Robustness: ⌈τ⌉ instead of ⌊τ⌋.**
  - Exact self-consistent polygons appear at a few more σ: E-M3h and F-M3h at 0.3, 0.1, 0.07, 0.05 and 0.008 (10, 20, 26, 34, 158); O and F-mixed at 0.15, 0.035 and 0.012 (15, 45, 111).
  - 2-cycles appear at large σ: (6, 14), (6, 28) and (6, 230) in E-M3h and F-M3h; (5, 19), (7, 9) and (5, 57) in O and F-mixed.
  - Most σ still have no fixed point.
  - The crossing and its scaling are unchanged: β = 0.78–0.79 over the grid, 0.86 for σ ≤ 0.05.
  - The rounding moves where the integer hits happen. It does not change the picture.

### 7.4 Robustness arm R1: depolarizing replacement at the matched leak rate (OBSERVED)

- **Crossing:** n_c = 27, 47, 103, 179 and 403 at σ = 0.4, 0.3, 0.2, 0.15 and 0.1. That is n_c·σ² = 4.0–4.4 and β ≈ 1.95, i.e. n_c ≈ 2/r + 2 ≈ 4/σ². This is a **pure horizon relabelling**, as §6.5 expected: τ is almost design-independent.
- **Slope** |ΔΦ/Δn| = 0–2. Self-consistent polygons at 0.4, 0.3 and 0.15 (28, 48, 180 for M3h; 27, 47, 179 odd).
- **Integer 2-cycles** at 0.2 and 0.1: (102, 104) and (402, 404) for M3h; (101, 103) and (401, 403) odd. They come from τ crossing an integer between neighbours.
- **σ ≤ 0.07:** the crossing needs T > 400, so it is OPEN by the range rule.
- **E-mixed:** the disk has T(disk) = 13–200 at σ ≥ 0.1, and **it is self-consistent there** (§7.2). At σ ≤ 0.07, T(disk) > 400. The disk is still co-optimal by §7.2's PIM bound, so it is self-consistent at every grid σ in this configuration (PIM, given T(disk) ≥ 2).

*(The level arm L follows in §7.5 when its run finishes.)*

### 7.5 Level arm L: lifetime = mean exit time from {d < δ}, δ ∈ {0.1, 0.2, 0.3, 0.5}, n ≤ 1201 (OBSERVED; `level_arm.py` → `level_tau.json`, `level_analyse.out`, `level_fit.out`, `level_monotone.out`)

- **Range.** Exact Markov-chain exit times for every n ≤ 1201 and every grid σ. Candidates lie in A(T ≤ 400) ⊂ [5, 802], so n > 1201 can matter only at T > 400. Where the crossing needs T > 400 it is OPEN by the range rule: δ = 0.1 at σ ≤ 0.008, δ = 0.2 at σ ≤ 0.018, δ = 0.3 at σ ≤ 0.025, δ = 0.5 at σ ≤ 0.05.
- **Disk lifetime.** Gaussian-walk exit from |φ| < 2·arcsin δ, by Nyström. For a/σ > 40 the Siegmund-corrected formula (a + 0.5826σ)²/σ² is used; the two agree to 0.1% at the three overlap checks. T(disk) = 1–89,869 over the grid. It is ≥ 2 everywhere except δ = 0.1 at σ ≥ 0.3.
- **Disk status.**
  - **Not self-consistent at any (σ, δ)** in E-M3h, O, F-M3h and F-mixed, as SH1 says.
  - **Self-consistent at 12–14 of 14 σ in E-mixed** (§7.2's degenerate tie). That is a MISS item in that configuration.
- **Polygons (non-degenerate configurations).** The number of self-consistent polygons per σ is 0, 1, 2 or 3. For F-M3h at δ = 0.3 it is 0, 0, 2, 0, 1, 1, 1, 1 at σ = 0.4 … 0.035. 2-cycles appear at some σ for every δ.
- **Why there are several fixed points.** τ_δ is not monotone in n: it rises at 6–33% of consecutive steps, whenever a new vertex enters the set {d < δ}. So §6.5's "at most one" argument (it needs τ nonincreasing) does not apply.
- **Crossing scaling.** For δ ≥ 0.2, n_c·σ² is constant: 0.30–0.34 (δ = 0.2), 0.78–0.87 (δ = 0.3), 2.4–2.5 (δ = 0.5); β = 1.9–2.1. This matches the diffusive relabelling n_c ≈ 2φ_δ²/σ² of §6.5: 2φ_δ² = 0.32, 0.74 and 2.19. At δ = 0.1, β = 1.4, a crossover between the primary regime (any confusion counts) and the diffusive one.
- **Insensitivity test of §6.2.**
  - The qualitative outcome is the same at every δ: no unique fixed point at most σ, and 2-cycles at some σ.
  - The **exponent and prefactor are not insensitive**: β ≈ 0.8–0.86 at δ → 0⁺ (the primary), ≈ 2 for δ ≥ 0.2, with the prefactor ∝ φ_δ².
  - So the level matters for the **scale** n_c, not for the **failure to select**.

### 7.6 Score under §6.4: **MISS**

- **Primary, every configuration.** There is no self-consistent polygon at most σ (each configuration has one at only 1–2 grid σ), so the MISS condition "no fixed point" holds.
  - E-M3h and F-M3h: none at 13 of 14 σ (only n = 12 at σ = 0.2).
  - O and F-mixed: none at 12 of 14 (only 7 and 9 at σ = 0.4 and 0.3).
  - E-mixed: several tied fixed points and 2-cycles.
- **Not a level artifact.** The OPEN-if-level-sensitive clause does not apply: every arm (⌈τ⌉, R1, L at four δ) also shows no fixed point, multiple fixed points or 2-cycles at some σ.
- **Disk.** It is never self-consistent at σ > 0 in the four non-degenerate configurations (PIM via SH1, and observed in every arm). It is self-consistent in the degenerate E-mixed menu whenever its lifetime is ≥ 2 ticks (PIM, §7.2).
- **n*(σ).** There is no n*(σ) to report: the self-consistent set is mostly empty. What does grow monotonically as σ falls is the **continuous crossing** n_c(σ):
  - primary: n_c ≈ (4 ± 0.5)/(σ·√(2 ln(1/σ))), from 6.5 at σ = 0.4 to 327.5 at σ = 0.0035; β = 0.81 (all σ), 0.86 (σ ≤ 0.05);
  - R1: ≈ 4/σ²;
  - L: ≈ 2φ_δ²/σ².
- **Prior check.** §6.5 put P(MISS) ≈ 0.6 and named this mechanism (a repelling crossing that steps over the diagonal). The outcome matches the paper prediction, so it is a confirmation, not a discovery.

### 7.7 Trivial or genuine?

- **The crossing is trivial,** by §6.6's own rule. The primary β is in [0.8, 1.3], and n_c·σ·√(2 ln(1/σ)) varies by a factor 1.34 (< 1.5). That is "resolution ≈ noise": a circle resolves about 2π/σ·(log factor) pure states under kicks of size σ (Shannon 1949; PSK and quantizer sizing, §7.8). R1 and L are horizon relabellings (β ≈ 2), as predicted. In none of the three does the cost J do work beyond the argmin rule (2T + 2, or 2T + 1 odd).
- **The failure to select is genuine, but elementary.**
  - A discrete record's lifetime under small kicks is exponentially steep in its resolution: τ = 1/erfc(π/(√2nσ)), Kramers/Arrhenius-like.
  - So the self-consistency map has slope ≈ −2x² ≈ −2 ln(1/σ) at the crossing: |ΔΦ/Δn| = 2–8 observed, growing as σ falls. It repels, and on the integers it steps over the diagonal.
  - **Self-consistency picks a scale, n_c, and not a design.** Choosing a design at that scale needs a further rule: a rounding, a mixture or a tie-break. That is a chosen input again. This is the specific, checkable content of §5's break point, now with a physical rate in place of a weighting.
- **What the leak does buy.** With any finite lifetime the disk is not self-consistent (SH1; observed in every arm outside the degenerate E-mixed menu). The continuum then appears only as the σ → 0 limit of the crossing scale. That is (F) again, now indexed by σ instead of by T.

### 7.8 Prior art (DOIs checked on Crossref this session: `selfhorizon/crossref_shn.txt`)

- **Shannon 1949**, "Communication in the presence of noise", *Proc. IRE* 37:10–21, doi 10.1109/JRPROC.1949.232969. Packing signal points under noise: the number of reliably distinguishable signals grows like (signal range/noise)^dimension. The primary's n_c ∝ 1/σ (up to a log) is the one-dimensional circle case in substance. KNOWN; this is the main reason the crossing is called trivial.
- **Phase-shift codes on the circle:** Slepian 1968, "Group codes for the Gaussian channel", *Bell Syst. Tech. J.* 47:575–602, doi 10.1002/j.1538-7305.1968.tb02486.x; Wyner 1966, "Bounds on communication with polyphase coding", *Bell Syst. Tech. J.* 45:523–559, doi 10.1002/j.1538-7305.1966.tb01043.x. A guessed DOI, 10.1002/j.1538-7305.1966.tb00031.x, returned 404 and is not used. KNOWN: the error rate of n-point PSK is governed by erfc of (half-spacing/noise), the same p_n used here.
- **Quantizer size under noise:** Max 1960, *IRE Trans. Inf. Theory* 6:7–12, doi 10.1109/TIT.1960.1057548; Lloyd 1982, *IEEE Trans. Inf. Theory* 28:129–137, doi 10.1109/TIT.1982.1056489; Farvardin & Vaishampayan 1987, "Optimal quantizer design for noisy channels", *IEEE Trans. Inf. Theory* 33:827–838, doi 10.1109/TIT.1987.1057373. KNOWN: under channel noise a finer quantizer stops paying, and the useful resolution is set by the noise. This is the closest analogue of n_c.
- **Exponentially steep lifetimes:** Kramers 1940, *Physica* 7:284–304, doi 10.1016/S0031-8914(40)90098-2 (escape over a barrier). The polygon's first-confusion time 1/erfc(x) has the same exponential-in-barrier form, with x² as the barrier. That steepness is what makes the crossing repel.
- **Overshoot constant:** Siegmund 1979, *Adv. Appl. Probab.* 11:701–719, doi 10.2307/1426855, for the corrected diffusion approximation (ρ ≈ 0.5826) in the disk's level-arm lifetime.
- **Not checked, so not cited:** a specific rate–distortion paper for noisy angle codes. I found no DOI for one this session; the PSK and quantizer entries above are the cited background.
- **Not found:** a statement that a self-consistency between a record's lifetime and its optimal transport horizon fails to select a design because of exponential lifetime steepness. "Not found" is not "new"; it is ELEMENTARY given the above.

### 7.9 Labels

| claim | label |
|---|---|
| Under the antipode rule every even polygon costs ≥ the disk; the E-mixed menu is degenerate | **PIM (ELEMENTARY)**, class of SR_B §1 |
| Disk not self-consistent at σ > 0 in E-M3h, O, F-M3h, F-mixed, for any finite lifetime ≥ 2 | **PIM** (SH1); observed in every arm |
| Disk self-consistent in E-mixed whenever T(disk) ≥ 2 | **PIM** (§7.2) |
| Polygons with T > 400 not self-consistent where T > π²/(4d_min) | **PIM** (SR-b1(f)); all such cases in the primary |
| Primary: no self-consistent polygon at 12–13 of 14 σ per configuration; no 2-cycles (non-degenerate) | OBSERVED |
| Repelling crossing, \|ΔΦ/Δn\| = 2–8, growing as σ falls; paper form −2x² | OBSERVED + heuristic (§6.5) |
| n_c ≈ (4 ± 0.5)/(σ√(2 ln(1/σ))), β = 0.81–0.86 | OBSERVED (fit) |
| R1: n_c ≈ 4/σ²; L: n_c ≈ 2φ_δ²/σ² | OBSERVED (fit) + heuristic |
| Level arm: several fixed points at some σ, because τ_δ is non-monotone in n | OBSERVED |
| SH-noise (§6.4) | **MISS** in every configuration and arm |
| "Self-consistency of lifetime and horizon selects one design under a physical leak" | **open miss**; it selects a scale n_c(σ), trivial in form (resolution ≈ noise) |

### 7.10 What this changes in §5

- §5's conclusion **partly** stands. The leak does replace the modeller's horizon weighting with one physical rate σ.
- With the rate in place, self-consistency still does not pick a design. It picks the resolution scale n_c(σ) ~ 1/σ (up to a log), which is known in substance, plus a rounding or tie-break rule to get a design. That rule is a chosen input.
- The one-point break of §5 is sharpened: **the record's lifetime is exponentially steep in its resolution, so the self-consistency map repels.** That is checkable and checked.
- Not tested, and still the main alternative (§6.7): the interruptible reading, and charging the keep-floor heat of holding against the leak inside J. The second would add a cost growing with lifetime, kT·Γ per nat per tick. It could change the slope of Φ, so it is the natural next arm. It needs its own pre-statement.
- **Rescore (§13 scale).** "SH-heat" (charge the keep floor inside J, with a pre-statement): p(an attracting, unique fixed point) 0.25, V 3; p(still repelling or degenerate) 0.75, V 1.5. EIV 1.9 over ≈ 3 h → **≈ 0.63 per hour**. For the parent to rank.

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

## 9. SH-heat results (computed after §8; §8's SHA-256 5011235d…a5f38b is logged in WORKLOG at 14:25 ET; scripts and outputs in `selfhorizon/`)

*Order of events (ET, box clock):*
- §8 appended and hashed at 14:25. §8's header says "about 14:35"; that is wrong, and a WORKLOG correction is logged.
- First run started at about 14:26. I stopped it after about 20 s: λ_k ≤ 0 at large σ broke a log1p, a coding bug. None of its output is used.
- Fixed run: 14:27–14:29, detached, log in `sh_heat_run.log`. Checks: `sh_heat_checks.out`. Analysis: about 14:30–14:34.

### 9.1 Checks (OBSERVED; `sh_heat_checks.out`)

- Kernel normalisation: |Σq − 1| ≤ 1.7e−15.
- (b) FFT entropy against direct matrix powers (n ≤ 15, 8 σ, t ≤ 60): max relative error 4.3e−10.
- (c) The closed-form Σε against direct summation: 4.7e−9.
- (d) First-order against exact at the regime boundary: agreement to 5–6 digits.
- (a) Full integer scan of s ≤ 4000 against the grid search (n ≤ 61, all σ, all x; 6608 cases): **0 mismatches**.

### 9.2 What the rule does (OBSERVED; `sh_heat_summary.out`)

- **Mode structure, c_K = 2.** At every (σ, x), the designs in check mode form one contiguous block of small n, n ≤ n_b(σ). Above n_b, keep wins, so τ = ∞. Fade wins only at large σ with small x.
- **The edge n_b scales as resolution ≈ noise.** n_b·σ·√(4 ln(1/σ)) = 3.2–3.3 for σ ≤ 0.07, and n_b barely depends on x: at σ = 0.0035, n_b = 198 at x = 0.05 and 196 at x = 1.
- **Check interval.** In 4801 of 5151 check-mode designs, s* = ⌊2/x⌋ or ⌈2/x⌉ exactly, as §8.2 predicted.
  - The other 350 lie where s*·p is not small: the large-σ end, or near the edge. Their s* exceeds 2/x by up to a factor 20.
  - None of them sits next to a HIT cell's n*.
- **Monotone in x (CT33 check).** The number of kept designs never falls as x rises at σ = 0.05 and 0.012 (0 → 1183 and 1134 → 1137).
- **The disk** fades, with τ = 1, which is vacuous (pre-decided).

### 9.3 Cells and score (scored: E-M3h, O, F-M3h, F-mixed; 14 σ × 8 x × 4 = 448 cells per arm)

| arm | HIT | MISS | OPEN | not classified by §8.6 |
|---|---|---|---|---|
| c_K = 2, ⌊τ⌋ (primary) | 141 | 294 | 6 | 7 |
| c_K = 2, ⌈τ⌉ | 141 | 297 | 3 | 7 |
| c_K = 4, ⌊τ⌋ | 150 | 275 | 15 | 8 |
| c_K = 4, ⌈τ⌉ | 150 | 282 | 8 | 8 |

- **Score under §8.6: MISS.** There are MISS cells at every x in the grid, in every arm. Pre-stated P(MISS) was 0.8.
- **What the MISS cells are (primary).**
  - 156 have no self-consistent polygon because A(⌊2/x⌋) lies above n_b. That design is kept, so its τ = ∞, and SR-b1(f) excludes it.
  - 104 have none on the fade branch, the §7.3 mechanism.
  - 34 have a unique fixed point that **repels**, |slope| = 2–3, all at large σ.
- **HIT band: a cell is a HIT iff A(⌊2/x⌋) ≤ n_b(σ).** In every HIT cell:
  - n* = A(⌊2/x⌋): 4/x + 2 for the even menus, 4/x + 1 for the odd ones (82/81 at x = 0.05; 42/41 at 0.1; 22/21 at 0.2; 10/9 at 0.5; 6/5 at 1);
  - T(n*) = 2/x exactly;
  - the slope is **0**, and every orbit that starts in the check block ends at n*.
  - Pre-stated prediction: cells with x ≥ 3σ√(2 ln(1/σ)) are HITs. Observed: 119 of 120 (the exception is "not classified", below).
- **"Not classified by §8.6."** These are 7 primary cells where n* is unique and self-consistent but is the top of the check block. Its upper neighbour is kept, so §8.5's slope is undefined. §8.6 gives no status for this, so they are counted as not-HIT. That does not change the score.
- **OPEN.** Six primary cells, each with one design at T in (400, π²/(4·d_min)].
- **E-mixed** (reported, not scored): mostly several fixed points, as the §7.2 degeneracy predicts.

### 9.4 The parent's two questions

- **Does the keep, check or fade rule remove the overshoot (|slope| < 1)?** Yes, inside the HIT band: the slope is exactly 0. It does so by making the horizon **design-independent** on the check branch, T = ⌊2/x⌋, so Φ is flat there. It does not tame the exponentially steep lifetime of §7.7; it replaces it with a horizon the stake sets. Outside the band, the failures are an escape to τ = ∞ (keep) or the old repelling crossing (fade, |slope| = 2–3).
- **Does it select one design at each noise level?** Not at every σ.
  - At σ ≥ 0.2 (σ ≥ 0.3 for c_K = 4), no x on the grid gives a HIT in all four configurations.
  - At smaller σ, every x down to about 1.7σ√(2 ln(1/σ)) does.
  - Where it selects, the design is set by **x alone**: n* ≈ 4/x + 2, the same at every σ in the band. So it selects one design per stake, not one per noise level. Noise only sets the band edge n_b ∝ 1/(σ√(ln(1/σ))).

### 9.5 Trivial or genuine (the §8.7 test)

- **Trivial ("stake relabelling").** 138 of the 141 primary HIT cells meet §8.7's literal triviality test: T is constant on n* ± 2 and equal to ⌊2/x⌋.
- **The other 3 trip the "genuine" clause by the letter of §8.7:** F-M3h at x = 1, σ = 0.15; F-mixed at x = 0.5, σ = 0.1; F-mixed at x = 1, σ = 0.2.
  - In each, n* + 2 is across the keep edge (τ = ∞), while n* − 2 … n* + 1 all have T = 2/x.
  - The "mode switch" is the edge, not an n-dependent s*. The attraction there is still the flat branch (slope 0), and the orbits leave through the edge.
  - **Call: trivial in substance.** §8.7's wording lets this edge case count as genuine; I flag that as a defect of the test, not a finding.
- **Prior art for each trivial part:**
  - s* ≈ 2/x is CT9/CT11's renewal optimum with the read price replaced by the Landauer restore cost (Landauer 1961; Bennett 1982), and the square-root EOQ form of CT11 (Harris 1913, reprinted 1990) degenerates to 2/x here because that restore cost grows only like log s.
  - n_b is resolution ≈ noise, as in §7.7: Shannon 1949; PSK; quantizer sizing.
  - Periodic refresh against staleness is Cho & Garcia-Molina 2003, which THEORY CT9 already credits.
- **What is genuine but elementary.** There are two failure routes outside the band: designs above n_b are kept forever (τ = ∞, never self-consistent), and the fade branch repels. So the keep, check or fade rule turns §7's repelling crossing into an **edge** (n_b) plus a **flat map** below it. Self-consistency then selects A(⌊2/x⌋) when it fits under the edge, and nothing otherwise.

### 9.6 Hostile review of §§8–9 (self-review; it does not replace an independent one)

- **H1, the horizon reading (decisive).**
  - The HIT band exists only because the horizon is read as **one written state's life**, the check interval s*.
  - Under a check schedule the record, as information, lives forever. Under that reading (§8.7 arm H∞, pre-decided) every check or keep design has τ = ∞ and is excluded, and the score is the §7.3 MISS.
  - Neither reading is forced by the theory's text. CT9 prices a schedule; it does not define a record's lifetime.
  - **Severity: high.** The band is conditional on a CHOSEN reading.
- **H2, the restore cost.**
  - s* ≈ 2/x comes from pricing the check at the Landauer cost of the leak's entropy, which grows only like log s for small s·p.
  - With any fixed read price c (CT9's λc; THEORY.md:311), the interval becomes the CT11 form s* ≈ √(2c/(x·p_n)), not computed here.
  - That depends on n through p_n. Paper estimate: |d ln s*/d ln n| ≈ x_a² with x_a = π/(√2·nσ), so near the edge the slope is about ln(1/σ)/… ≥ 1. The overshoot would likely return. **HYP, not computed.**
  - §8 excluded the read price because it would be a free parameter. That exclusion is also what makes the map flat. **Severity: high.**
- **H3, keep floor attainment is OPEN** (C12B §8). The floor is the cost most favourable to keeping. A real, higher keep cost moves n_b up and widens the band: c_K = 4 gives 150 HITs against 141. The direction is known; the size is not. **Medium.**
- **H4, the disk is excluded by construction.** Exact keeping or checking of a continuum pure state costs ∞ by §8.2's information count. This agrees with SH1, but it is an input: the record is taken to be an exact pure state. With a level δ (as in §6.2) the disk would get a finite cost. That is not computed. **Medium.**
- **H5, the stake x is not fixed by the theory** (CORE.md:23). The selected design is a function of x alone. This is consistent with CT33 (spend rises with the stake), but it means self-consistency adds nothing a fixed horizon T = 2/x would not give. **Medium; this is the triviality call.**
- **H6, numerics.**
  - The grid s-search was checked exhaustively only for n ≤ 61.
  - For larger n, the T* values in the HIT cells equal 2/x exactly, which matches the analytic first-order optimum. So an error there would have to lie in the 350 n-dependent designs, which are not next to any HIT n*.
  - Arg-min sets are §7.1's (T ≤ 400).
  - **Low.**
- **H7, scope.** J is unchanged (heat sets the lifetime only), and §7.10's heat-in-J version is not run (it needs an exchange rate). The interruptible reading is not run either. **Stated limits.**
- **H8, timing.** §8's header time is wrong ("about 14:35"; appended at 14:25), corrected in WORKLOG. Every computation postdates the hash.
- **H9, "Theorem O(v)".** Not found on today's main (`8b553c6`). The keep rule used is THEORY.md:138, :145, §B.2 (:301–:330), CT26 (:480), and CLAIM_MAP_v2.md:525, :530, :532, :559. Nothing rests on "Theorem O(v)".
- **Review result: the MISS stands.** Triviality is stated, and H1 and H2 are the conditions the band depends on. **Net: PASS-WITH-FIXES** for the note: the §8.7 edge-case wording, and the H1/H2 conditions carried into any summary.

### 9.7 Prior art (DOIs checked on Crossref this session: `selfhorizon/crossref_heat.txt`, 4/4 OK)

- Landauer 1961, *IBM J. Res. Dev.* 5:183–191, doi 10.1147/rd.53.0183: the erasure cost kT per nat, used for the restore cost.
- Bennett 1982, *Int. J. Theor. Phys.* 21:905–940, doi 10.1007/BF02084158: the review of the same accounting.
- Cho & Garcia-Molina 2003, *ACM Trans. Database Syst.* 28:390–426, doi 10.1145/958942.958945: refresh policies against staleness, credited by THEORY CT9.
- Harris 1913, reprinted as "How many parts to make at once", *Oper. Res.* 38:947–950 (1990), doi 10.1287/opre.38.6.947: the square-root (EOQ) interval of CT11.
- Plus §7.8's list for resolution ≈ noise: Shannon 1949; Slepian 1968; Wyner 1966; Max 1960; Lloyd 1982; Farvardin & Vaishampayan 1987.
- **Not found:** a statement that a keep, check or fade rule makes a lifetime/design self-consistency map flat below a noise-set edge. "Not found" is not "new"; it is ELEMENTARY given the above.

### 9.8 Labels

| claim | label |
|---|---|
| Kept designs (τ = ∞) are not self-consistent; the disk fades with τ = 1 | **PIM** (SR-b1(f); §8.2) |
| Arms H∞ and c_K = 0 give MISS | **PIM** (pre-decided, §8.7) |
| s* ≈ 2/x when s*·p ≪ 1 | heuristic (first-order) + OBSERVED (4801 of 5151) |
| Check block contiguous, n_b ≈ 3.3/(σ√(4 ln(1/σ))), nearly x-free | OBSERVED (fit) |
| 141 HIT, 294 MISS, 6 OPEN, 7 not classified (primary); slope 0 in every HIT; n* = A(⌊2/x⌋) | OBSERVED |
| SH-heat (§8.6) | **MISS** in every arm |
| "With the theory's keep, check or fade rule, self-consistency selects one design per noise level" | **open miss**: it selects one design per stake, n* ≈ 4/x + 2, inside a band set by the noise |
| A fixed read price brings the overshoot back | HYP (H2), not computed |

### 9.9 Correction to §9.6 H2: the slope sentence (appended 26 Nov 2026; §9.6 stands as written; where they conflict, this governs)

- §9.6 H2 reads "|d ln s*/d ln n| ≈ x_a² with x_a = π/(√2·nσ), so near the edge the slope is about ln(1/σ)/… ≥ 1". The "ln(1/σ)/…" is garbled, and the step from the interval to the map's slope is missing. The corrected paper estimate (HYP, heuristic; tested in §10–§11) follows.
- **Interval.** With a fixed read price c (y := c/kT), and s·p small, J_chk(s) ≈ y/s + x·p_n·s/2, so **s* ≈ √(2y/(x·p_n))** (CT11's square-root form).
- **Elasticity.** p_n ≈ erfc(a) with a = π/(√2·nσ). For a ≳ 1, d ln p_n/d ln n ≈ 2a², so **d ln s*/d ln n ≈ −a²**.
- **Slope.** Φ(n) ≈ 2·s*(n) + 2. At a crossing n ≈ 2s*, dΦ/dn ≈ 2(s*/n)·(−a²) ≈ **−a²**. That is half the SH-noise value −2a² (§6.5), because of the square root.
- **At the crossing,** p_n ≈ 8y/(x·n²), so a² ≈ ln(x·n²/(8y)) to leading order. The map repels (|slope| > 1) once a² > 1, roughly p_n < erfc(1) ≈ 0.16. That is the expected case whenever x·n² ≫ y.

## 10. Pre-statement: the CT9 read-price arm (SH-read) and the w-reduction claim (W) (written 26 Nov 2026 before any SH-read number is computed; §§0–9 stand as written)

*The SHA-256 of this block, from the "## 10." heading line through the end of §10.9, is logged in WORKLOG.md with the clock time before any computing. Nothing in §10 may be edited afterwards. Results go in §11.*

### 10.1 Model (as §8.2, with one change to the check mode)

- **Check cost per tick, in CT9's form** (THEORY.md:311, J(s) = λc/s + A(s)), keeping §8's Landauer restore term:
  J_chk(s) = [y + H(K_s) + x·Σ_{u=0}^{s−1} ε(u)]/s,
  - y := c/kT, the read price per check;
  - x := w/kT, the stake;
  - H, ε as §8.2;
  - s* := the integer argmin over 1 ≤ s ≤ 20000.
- **Keep and fade:** as §8.2 (c_K = 2; arm c_K = 4 not run here).
- **Disk:** fades, τ = 1, vacuous (PIM, §8.2).
- **Mode:** the cheapest per tick. On a tie, the shorter lifetime.
- **Grids.**
  - σ: §6.4's 14 values.
  - x ∈ {0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1}.
  - y ∈ {0.1, 1, 10}.
- **Edge rule.** If s* = 20000, then T ≥ 20000 > π²/(4·d_min(n)) for every n ≤ 1201 (π²/(4·d_min) < 950 there). The design is then excluded by SR-b1(f) (PIM), provided J_chk is still decreasing at s = 20000. That condition is checked and reported; where it fails, the design is OPEN.

### 10.2 Two horizon readings (both scored)

- **(W) one written state's life:** τ = s* for check, ∞ for keep, 1/p_n for fade.
- **(I) the information's life:** τ = ∞ for check and keep, 1/p_n for fade.
  - Paper (PIM): under (I) the self-consistent set is contained in §7.3's primary set restricted to fading designs. Its score is therefore expected to be MISS wherever §7.3 has no fixed point, which is 12–13 of 14 σ per configuration.

### 10.3 Fixed-point rule, slope test, cells

- **As in §8.3 and §8.5:** T = ⌊τ⌋, primary; ⌈τ⌉ is an arm. A(T) is from §7.1 (T ≤ 400). Designs with 400 < T < ∞ are excluded if T > π²/(4·d_min), and OPEN otherwise.
- **Kept designs** are excluded (PIM).
- **Configurations:** E-M3h, O, F-M3h and F-mixed are scored; E-mixed is reported only.
- **Slope.** The slope at a unique fixed point n* uses its two menu neighbours where both have finite Φ.
  - **New, to close §9.3's gap:** if only one neighbour has finite Φ, use the one-sided slope. If neither does, the cell is **EDGE**.
- **Cell status:**
  - **HIT:** exactly one self-consistent polygon; no 2-cycle; disk not self-consistent; |slope| < 1; and every orbit of Φ (60 steps) that stays finite ends at n*.
  - **MISS:** none, two or more, a 2-cycle, or |slope| > 1 at the unique fixed point.
  - **EDGE:** as above; not a HIT and not a MISS.
  - **OPEN:** by the range or edge rules.
- **Per (x, y):** MISS if any cell is a MISS; HIT if all are HITs; otherwise OPEN.
- **Score per reading: HIT iff HIT at every (x, y); MISS iff MISS at some (x, y); OPEN otherwise.**

### 10.4 The key question: noise or stake (measured on every cell, HIT or not)

- **Crossing.** n_c(σ, x, y) is the first sign change of Φ(n) − n over consecutive menu members with finite Φ, ascending (midpoint). The slope across it is s_c.
- **Elasticities**, by least squares over the grid where n_c exists:
  - β := −d ln n_c/d ln σ at fixed (x, y);
  - e_x := d ln n_c/d ln x at fixed (σ, y);
  - e_y := d ln n_c/d ln y at fixed (σ, x).
- **Reading:**
  - **"set by noise":** β ∈ [0.8, 1.3] and |e_x|, |e_y| ≤ 0.25;
  - **"set by stake":** |e_x + 1| ≤ 0.25 and β ≤ 0.25 (§9's pattern was e_x = −1, β = 0);
  - **"mixed":** anything else, with the numbers reported.
- **Overshoot back** iff the median |s_c| over cells where n_c exists is > 1.
- **Paper prediction (§9.9).** n_c solves erfc(π/(√2·nσ)) ≈ 8y/(x·n²), so n_c ≈ (π/σ)/√(2 ln(x·n_c²/(8y))): **set by noise**, with x and y entering only through a logarithm (|e_x| ≈ |e_y| ≈ 1/(2a²) ≈ 0.1–0.25). Expected |s_c| ≈ a² ≈ 2–6: **overshoot back.**
  - P(MISS under (W)) ≈ 0.85. P(overshoot back) ≈ 0.8. P("set by noise") ≈ 0.6, P("mixed") ≈ 0.35, P("set by stake") ≈ 0.05.

### 10.5 Triviality test for SH-read (stated now)

- **Trivial ("resolution ≈ noise"):** "set by noise", with n_c·σ·√(2 ln(1/σ)) constant within a factor 1.5 over σ at each (x, y).
- **Trivial ("stake relabelling"):** "set by stake".
- **Genuine** iff some HIT cell exists with |s_c| < 1 whose n* is neither within a factor 1.5 of 4/(σ√(2 ln(1/σ))) nor within a factor 1.5 of 4/x + 2.

### 10.6 Structural claim W (a HYPOTHESIS, stated before its test)

- **Claim W.** Across SR-b4, SH1, SH-noise and SH-heat (§§6–9; SR_B §9), **every free input reduces to the single stake w** of CORE.md:23 (J = Q̇ + w·E[ℓ]; "w converts the loss into the currency of the heat. Temperature does not set w.").
- **"Reduces"** means: with the other inputs at their scored values, the outcome depends on that input only through a function of w (or of x = w/kT).
- **Test, one row per input.** Classify each input as one of:
  - **(R) reduces:** a derivation or computation shows the outcome depends on it only through w;
  - **(F) fails:** two values of the input at the same w give different outcomes, labelled by how that difference is established (PIM or OBSERVED);
  - **(V) vacuous:** it cancels.
- **Claim W holds iff no row is (F).**
- **Inputs and predicted rows** (written now; the test fills in the evidence in §11):
  1. Horizon T (SR-b1/b3; SH-noise via τ). Predicted: (R) only in §9's check band, where T = ⌊2/x⌋, and conditionally (H1 and H2 of §9.6). Elsewhere T comes from σ.
  2. Horizon weighting and its cap H (SR-b4's R_H; SR-b's geometric q). Predicted: (F). SR-b4 is pointwise dominance at every bounded H, and w does not enter J.
  3. Quantifier order, design before horizon scale ((F) vs (P), SR_B §8–§9). Predicted: (F). A logical structure, not a price.
  4. Target rule, M3h versus antipode. Predicted: (F), PIM by §7.2 against SR-b3.
  5. Design menu (even, odd, all). Predicted: (F).
  6. Cost exponent, c·d² versus c·d (ROUND10 §14: "With a linear price c·d the ranking reverses"). Predicted: (F).
  7. The price κ per affine dimension. Predicted: (V), since it cancels (SR_B §1).
  8. Noise σ. Predicted: (F). §9.2's edge n_b is nearly x-free.
  9. Lifetime definition (first confusion versus level δ). Predicted: (F), from §7.5.
  10. Rounding ⌊ ⌋ versus ⌈ ⌉. Predicted: (F), from §7.3's ceil rows.
  11. Keep constant c_K (2 versus 4; carrier class). Predicted: (F), from §9.3.
  12. Read price c (this unit). Predicted: (F) unless c sits at its thermodynamic floor, in which case c ∝ kT and x is the only ratio. Tested by comparing cells at equal x/y.
  13. Horizon reading (W) versus (I). Predicted: (F).
  14. Temperature kT. Predicted: (R), trivially, since it is the unit in x = w/kT.
- **Prior:** P(Claim W holds) ≈ 0.03.

### 10.7 Tools and checks planned

- `selfhorizon/sh_read_run.py`, reusing `sh_heat_core.Rec` with the read price added and SMAX = 20000, run detached with a log. `sh_read_analyse.py` does the analysis.
- **Checks:**
  - (a) a full integer scan s ≤ 20000 for n ≤ 31 against the grid search;
  - (b) J_chk decreasing at s = 20000 wherever s* = 20000;
  - (c) at y = 0, s* equals §9's (regression).

### 10.8 Labels planned

- Cells, crossings and elasticities: OBSERVED.
- The (I)-reading containment, the kept-design and edge-rule exclusions: PIM.
- Claim W's rows: labelled one by one.

### 10.9 Not tested here

- The interruptible reading.
- The heat in J (§7.10).
- The level arm for the check mode.
- c_K = 4.

## 11. SH-read results and the Claim W test (computed after §10; §10's SHA-256 f1b738cb…ab74 was logged in WORKLOG at 14:40 ET, before any computing; scripts and outputs in `selfhorizon/sh_read_*`)

*Order of events (ET):*
- 14:40: §9.9 and §10 appended; hash logged.
- About 14:41: run 1 started. It crashed at about 14:48 (overflow in the s-grid hint when p_n is denormal).
- Run 2 crashed at the final file write at about 15:05 (numpy bool in JSON).
- Run 3 ran 15:06–15:29, detached (`sh_read_run.log`), and is the only one used.
- A tool interruption at about 15:28 lost nothing: at 15:29 §9.9 and §10 were intact, the hash matched, and run 3 was still running. A WORKLOG line records this check.
- Analysis and checks, detached, 15:30–15:40.
- No output from runs 1 or 2 is used.

### 11.1 Checks (OBSERVED; `sh_read_checks.out`, `sh_read_key.out`, `sh_read_extra.out`)

- **(a) Full integer scan, s ≤ 20000,** n ≤ 31: 2256 cases, **0 mismatches**.
  - Scope reduced from §10.7, disclosed: σ ∈ {0.4, 0.1, 0.025, 0.0035} only, because the full σ grid was too slow alongside the main run.
- **(b) Edge rule.** 7160 check-mode designs have s* = 20000, and J_chk is still decreasing at the edge in all 7160. So the edge exclusion of §10.1 applies to every one of them, and no design is OPEN by this rule.
- **(c) Regression at y = 0 against §9** (n ≤ 61): 2 mismatches, both near-ties: n = 50, σ = 0.035, x = 0.05 gives s* = 2487 against 2489, and n = 52, σ = 0.025, x = 0.02 gives 1635 against 1636. J differs by about 1e−9 relative. Benign: a flat minimum and a different grid.

### 11.2 What the read price does (OBSERVED)

- **Every check-mode design now has s* > π²/(4·d_min(n)).** That holds for all 8851 check-mode (design, σ, x, y) combinations; the smallest ratio is 1.8. By SR-b1(f), no check-mode design can be self-consistent (PIM, given the observed s*).
  - Reason: check wins only where p_n is small, and there s* ≈ √(2y/(x·p_n)) is far longer than any horizon the design can serve.
- **So the (W) and (I) readings give identical cells.** Check and keep designs both drop out, and only the fade branch remains, which is §7.3's mechanism restricted to the (σ, x) where fade wins (large σ, small x).
- **§9's HIT band disappears at every grid read price** (y = 0.1, 1, 10). At y = 0 it is present (§9 and regression (c)). The crossover y_c in (0, 0.1) was not located. A paper estimate gives y_c of order p_n/x, which is tiny (HYP).

### 11.3 Score (scored: E-M3h, O, F-M3h, F-mixed; 14 σ × 8 x × 3 y = 336 cells per configuration, 1344 per reading)

| reading, rounding | HIT | MISS | OPEN | EDGE |
|---|---|---|---|---|
| (W), ⌊τ⌋ | 0 | 1344 | 0 | 0 |
| (W), ⌈τ⌉ | 0 | 1344 | 0 | 0 |
| (I), ⌊τ⌋ | 0 | 1344 | 0 | 0 |
| (I), ⌈τ⌉ | 0 | 1344 | 0 | 0 |

- **Score: MISS under both readings.** Pre-stated P(MISS under (W)) was 0.85.
- Nearly every cell has no self-consistent polygon. The few with one, e.g. F-M3h n = 12 at σ = 0.2, x ≤ 0.1, are the §7.3 fade-branch points, and their slope repels.

### 11.4 The key question: overshoot back, and set by noise or by stake? (§10.4)

- **Crossings exist only on the fade branch:** 81 per configuration (F-M3h, O), all at σ ≥ 0.07. The values are §7.3's: n_c = 6.5, 9.5, 12, 14.5, 19.5, 25.5, 33.5 (F-M3h).
- **Elasticities (least squares over all crossings):**
  - F-M3h: β = 0.757, e_x = 0.005, e_y = 0.000;
  - O: β = 0.743, e_x = 0.001, e_y = 0.000.
  - Per (x, y): β = 0.71–0.86, and n_c·σ·√(2 ln(1/σ)) = 3.5–4.4 (factor 1.26).
- **Overshoot back: yes, by §10.4's rule** (median |s_c| = 2.67 for F-M3h and 3.00 for O; |s_c| > 1 in 100% of crossings).
  - But it does **not** come from the n-dependent check interval, as §9.9 expected. **There is no crossing on the check branch at all**: the check interval is too long for any design (§11.2). The overshoot is §7.3's, from the fade branch.
- **Noise or stake:**
  - By §10.4's letter: **"mixed".** β is 0.74–0.76 overall, just below the [0.8, 1.3] window, while |e_x| and |e_y| ≤ 0.01.
  - In substance: **set by noise, with no stake dependence at all.** The crossings are §7.3's, whose full-range β is 0.81 (σ ≤ 0.05: 0.86). The window is missed because crossings survive only at σ ≥ 0.07, a truncated range.
  - It is not set by the stake: e_x ≈ 0, against §9's −1.
- **Correction to §9.9's expectation** (HYP there; it does not change §9.9's arithmetic). §9.9 predicted a repelling crossing on the check branch with |slope| ≈ a². No such crossing exists on the grid. The missed step: wherever check wins, s* ∝ p_n^{−1/2} exceeds π²/(4·d_min), so the check branch never reaches the diagonal.

### 11.5 Trivial or genuine (§10.5)

- **No HIT cell exists, so the "genuine" clause cannot apply.**
- **Not "set by stake".**
- **"Resolution ≈ noise" is missed by the letter** (β just under 0.8). In substance it is met: n_c·σ√(2 ln(1/σ)) is constant within 1.26, and the crossings are §7.3's.
- **Call: trivial in substance.** The read-price arm reproduces the §7.3 crossing on the fade branch and removes everything else.

### 11.6 Claim W, row by row (§10.6). "Same w" means the stake is held fixed or does not enter the unit's cost at all.

| # | input (unit) | row | evidence | label |
|---|---|---|---|---|
| 1 | horizon T (SR-b1/b3; SH-noise; SH-heat) | **F** | On the fade branch, T comes from σ: §7.3, and e_x ≈ 0 in §11.4. Only in §9's check band is T = ⌊2/x⌋, and that band vanishes at any grid read price (§11.2) | OBSERVED |
| 2 | horizon weighting and cap (SR-b4 R_H, H; SR-b geometric q) | **F** | SR-b's best n grows like 10/(1−q) with no w in J (SR_B §0.2); SR-b4's dominance holds at every bounded H | OBSERVED (q); PIM (SR-b4) |
| 3 | quantifier order, (F) versus (P) (SR_B §9) | **F** | Same J, no w: (F) selects the disk, (P) a polygon at every H ≥ 2 | **PIM** |
| 4 | target rule, M3h versus antipode | **F** | Antipode: the disk is co-optimal at every T (§7.2). M3h: the (2T+2)-gon is strictly cheaper at every T ≥ 2 (SR-b3). No w | **PIM** |
| 5 | design menu (even, odd, all) | **F** | §7.3 at σ = 0.2: E-M3h has n* = 12, O has none; at σ = 0.4: O has 7, E-M3h none | OBSERVED |
| 6 | cost exponent, c·d² versus c·d | **F** | ROUND10 §14: "With a linear price c·d the ranking reverses toward the classical jump" | OBSERVED (repo text; not recomputed here) |
| 7 | price κ per affine dimension | **V** | The same for every design, so it cancels (SR_B §1) | PIM |
| 8 | noise σ | **F** | §9.2: n_b is nearly x-free (198 against 196 across x = 0.05…1 at σ = 0.0035); §11.4: e_x ≈ 0, β ≈ 0.75 | OBSERVED |
| 9 | lifetime definition (first confusion versus level δ) | **F** | §7.5: β ≈ 0.8 against ≈ 2, at the same everything else | OBSERVED |
| 10 | rounding ⌊ ⌋ versus ⌈ ⌉ | **F** | §7.3: ceil adds exact hits and 2-cycles; §9.3: 294 against 297 MISS cells | OBSERVED |
| 11 | keep constant c_K (2 versus 4) | **F** | §9.3: 141 against 150 HITs at the same x and σ | OBSERVED |
| 12 | read price c (y = c/kT) | **F** | At the same x: y = 0 gives the §9 band, any y ≥ 0.1 gives none. At the same x/y = 0.1, σ = 0.4: (x, y) = (0.01, 0.1) gives n_c = 6.5, (1, 10) gives none. So the outcome is a function neither of x alone nor of x/y alone | OBSERVED |
| 13 | horizon reading, (W) versus (I) | **F** | At y = 0: (W) has §9's 141 HIT cells; (I) is MISS everywhere (§8.7 arm H∞, PIM) | PIM + OBSERVED |
| 14 | temperature kT | **R** | It is the unit in x = w/kT and y = c/kT | ELEMENTARY |

- **Result: Claim W fails.** 11 rows are F, 1 is V and 1 is R.
  - Rows 3 and 4 are counterexamples proved in the model: the outcome changes while w is fixed, and indeed absent.
  - So **"every free input reduces to w" is false in-model (PIM)** across these four units. The remaining F rows are OBSERVED.
  - Pre-stated P(Claim W holds) was 0.03.
- **What reduces to w, and where.** Only the horizon (row 1), and only conditionally: in §9's check band, with a Landauer-only restore cost and reading (W). There, T = ⌊2/x⌋. **(OBSERVED, conditional; not robust to a read price, §11.2.)**
- **A weaker reading, recorded so it is not used later as a rescue.** One could ask only whether each input *can be generated* by some stake-priced mechanism. Rows 3–6 still fail:
  - each changes the task (the target, the menu, the cost geometry, the quantifier), not a price;
  - CORE.md:23's w "converts the loss into the currency of the heat" and cannot change which loss is scored.

  Row 8 also fails: σ is a property of the medium. **HYP** (an argument, not a theorem).

### 11.7 Hostile self-review of §§10–11 (it does not replace an independent review)

- **R1 (medium): the y grid starts at 0.1.** The claim "a read price removes §9's band" is shown only for y ∈ {0.1, 1, 10}. y_c in (0, 0.1) is not located; the paper estimate y_c ~ p_n/x is HYP. Any summary should say "at the grid read prices".
- **R2 (medium): the §10.4 β window is missed narrowly.** That is because crossings exist only at σ ≥ 0.07, a truncated range. I report the letter ("mixed") and the substance (noise-set, stake-free) separately. I do not re-score.
- **R3 (medium): §9.9's prediction was wrong.** It expected a check-branch crossing with |slope| ≈ a², and the check branch never reaches the diagonal. Logged in §11.4. The pre-registered "overshoot back" item is met only through the fade branch, and §11.4 says so plainly.
- **R4 (low): checks.** Check (a) ran on a σ subset (disclosed). Regression (c) has two near-ties. Check (b) is clean.
- **R5 (medium): Claim W's rows are partly automatic.** w does not appear in SR-b's J at all, so any input that changes an SR-b outcome is F by construction. The weaker reading in §11.6 is the fairer test, and it also fails on rows 3–6 (HYP). The PIM label applies to the stated, strong form only.
- **R6 (low): two runs crashed;** disclosed, and their output is not used. All computing postdates the §10 hash.
- **R7 (scope):** c_K = 4, the level arm, the interruptible reading and heat in J were not run.
- **Review result: PASS-WITH-FIXES.** Carry R1 and R2 into any summary. The scores stand.

### 11.8 Prior art

No new sources. The read-price interval is CT11's square-root form, Harris 1913 (reprint doi 10.1287/opre.38.6.947), and the refresh setting is Cho & Garcia-Molina 2003 (doi 10.1145/958942.958945). Both were checked on Crossref this session (`crossref_heat.txt`, 4/4 OK). No new DOI is cited, so no new Crossref check was needed.

### 11.9 Labels

| claim | label |
|---|---|
| All check-mode designs have s* > π²/(4·d_min), so they are never self-consistent | OBSERVED (s*) + PIM (SR-b1(f)) |
| (W) and (I) readings coincide at y ∈ {0.1, 1, 10} | OBSERVED (follows from the row above) |
| SH-read (§10.3) | **MISS** under both readings; 1344 of 1344 scored cells |
| Overshoot back | yes, via the fade branch only (median \|s_c\| 2.7–3.0); not from the check interval |
| n_c set by noise, not by stake (e_x, e_y ≈ 0; β ≈ 0.75 on σ ≥ 0.07) | OBSERVED; "mixed" by §10.4's letter |
| §9's band survives a read price | open miss at y ≥ 0.1 (OBSERVED); y_c in (0, 0.1) OPEN |
| Claim W: every free input reduces to w | **false in-model (PIM: rows 3, 4)**; 9 further F rows OBSERVED; the weaker form also fails (HYP) |
