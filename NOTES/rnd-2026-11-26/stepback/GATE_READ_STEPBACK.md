# Gate read: STEPBACK.md drafts D (C11) and A (C2), before lock (Thu 26 Nov 2026, 06:35 ET)

Fresh-context hostile reviewer. Read: `rnd/stepback/STEPBACK.md` (sha256 d163a280…5c86, 06:31 ET version), the read-only clone `/workspace/stepback-src` (04c8309, the fork tip before 4741761; 4741761 only changes R13–16 timing/label text, so it does not touch anything checked here), `THEORY.md`, `measurement/CLAIM_MAP_v2.md`, `rnd/entangle/THREAD_SUMMARY.md`, `rnd/forces-gravity/{NOTE,THREAD_SUMMARY,HOSTILE_REVIEW_G3G5}.md`. Nothing committed, nothing locked edited, no email sent.
Labels: OBS observed · HYP hypothesis · PIM proved in model · KNOWN published.

**Disclosure for any later lock:** this gate read contains an Airy-asymptotic estimate of Draft D's outcome (§1.3). It is not the exact Bessel run on the locked grid, but it is prior knowledge of the likely outcome. Any lock of D or a successor has to cite it in its §0.

## Outcome summary

| draft | outcome | one-line reason |
|---|---|---|
| **D (C11, lead-time boundary)** | **FAIL** (do not lock as a test) | The outcome is fixed by known Bessel/Airy and Lieb–Robinson mathematics plus two free definitions (what R* measures, the 25% threshold), and at k = 8 the threshold sits on the analytic edge. The "value" proxy does not depend on the state at all. The G4 comparator is not like for like. A hit would swap a hand-placed cut for a hand-placed lead time k and stake region T, so an input is renamed, not removed. Convert it to a short proved-in-model lemma (amendment D1). |
| **A (C2, LT from read cost)** | **FAIL** (redesign before lock) | As written, the hit is true by definition or the outcome is set by parameter count. If the tracker is local-only, "premium in non-LT" is the definition of non-LT. If joint reads are allowed at equal price, real QM (K = 10) needs fewer parameters than complex QM (K = 16), so the predicted sign is set by dimension. The prediction has no number, the stakes are free, and the positive control is the same statement as the hit. |

Neither draft is a weak prior result in disguise, and the step-back's diagnosis behind them (F1/F2/F3) is useful. Both drafts, as written, have the failure shapes the step-back names: shape 2 (target or world fixed so the answer is set by the inputs), and for D also a threshold-sensitive comparator.

---

## 1. Draft D (C11): does predictive pricing put the record edge at the signal front?

### 1.1 Would a hit mean what it claims? (no)
- **The proxy does not depend on the state.** w_j(k) = Σ_{t∈T} |U_{tj}(k)|² uses only the single-particle propagator J_{j−t}(2k). Half filling, the vacuum, and anything a tracker could be wrong about drop out. It is a property of the Hamiltonian, not "predictive information about T's future". Calling it a predictive-value proxy is a modelling choice, and the only thing linking it to CORE's predictive bottleneck is the name. [OBS from the draft's own definition]
- **It is not net of what the tracker holds.** §8 says the value is "net of what the tracker already holds", but the greedy rule adds sites by raw w_j. Sites inside the front are highly redundant with one another in any real predictive-information measure, and w_j ignores that.
- **The result follows from a known bound, so no run is needed.** For any local H with Lieb–Robinson velocity v, |U_{tj}(k)| ≤ C·e^{−μ(d(j,T) − v k)} (Lieb & Robinson 1972, 10.1007/BF01645779, Crossref OK this session). So any threshold rule on w_j gives R* ≤ v k + μ⁻¹ log(C|T|/κ), with only log dependence on κ. For nearest-neighbour hopping the edge is the Airy region, which gives R* − 2k ≈ (2k)^{1/3}·2^{−1/3}·(¾ ln(1/κ))^{2/3}. That is a **PIM-able lemma**, not an empirical test. "Weak κ dependence" holds for every operator weight with a super-exponential tail, whatever the pricing story.
- **What is new? Only the reading.** The cut used to be placed by κ (G4/G5). Under D it is placed by (k, T, v), and k and T are CHOSEN. By the step-back's own oracle (§4 (c): an input must be *removed or merged, not renamed*), a hit does not certify the route unless k is itself selected by the cost (for example k* from CORE's stake and drift). The draft's "what a hit would not mean" paragraph is honest about relativity and v. It also needs to say that the boundary moves to a chosen lead time; it does not stop being placed by hand.

### 1.2 Could an instrument limit print the predicted outcome? (shape 1)
The predicted outcome here is a *hit* (a front with weak κ dependence), so the risk runs the other way: a run can print the hit whatever the physics, because the tail is analytic. There are also gaps that could print a spurious miss or pass:
- **R* is undefined.** It could be the number of added sites, the outermost added site's distance from T's centre, or the distance from T's edge. The 25% spread changes with this choice (§1.3). Greedy-by-weight also skips interior sites near Bessel zeros, so "number of sites" and "outermost distance" differ.
- **The infinite chain must be cut to finite size.** A finite ring or open chain reflects the front. A gate is needed: L ≥ 2·(2k_max + 50) + |T|, and the result must be the same at L and 2L to 1e−12 in w.
- **Precision and underflow.** w is compared with κ down to 1e−6. Bessel values must be correct to 1e−3 relative at w ~ 1e−7. A gate is needed against an independent evaluation (mpmath at 30 digits) at every κ-crossing site.
- **Trivial gates.** The two stated gates (unitarity, and k = 0 gives T) cannot fail in a way that matters. Gates are needed that could actually catch the instrument printing the predicted pattern (amendment D4).

### 1.3 Is the target fixed so that the result says little? (shape 2: yes, and the threshold sits on the edge)
Airy-asymptotic estimate (OBS, approximation, single nearest stake site, distance from T's edge; **not** the exact locked-grid computation). This is the outermost distance beyond T's edge with w ≥ κ for κ = 1e−2, 1e−3, 1e−4, 1e−6:

| k | 2k | R* beyond edge | excess R* − 2k | spread (max−min)/min |
|---|---|---|---|---|
| 8 | 16 | 17.3, 19.2, 20.7, 23.3 | 1.3 → 7.3 | **0.35** (≈ 0.27 if T's 5 sites are counted in R*) |
| 16 | 32 | 33.0, 35.6, 37.6, 40.9 | 1.0 → 8.9 | 0.24 (≈ 0.21) |
| 32 | 64 | 64.5, 67.9, 70.5, 74.8 | 0.5 → 10.8 | 0.16 |

So the "< 25% for k ≥ 8" prediction **likely fails at k = 8 and passes at k ≥ 16**, depending on how R* is defined. The scored outcome would be set by a definition and a threshold, not by anything about predictive pricing. The other prediction ("R* − vk grows no faster than c·k^{1/3}·log(1/κ) with one fitted c") can be met by any c above the Airy constant, and its falsifier ("grows like k") cannot occur under Lieb–Robinson. That part cannot be falsified.

### 1.4 Is the comparator fair? (no)
G4's R ∝ κ^{−0.49} came from **static mutual information in the critical vacuum**, which has algebraic (~1/r) tails (E-G3G5-12). D's proxy has super-exponential tails. The contrast measures **tail shape (algebraic versus super-exponential)**, not "static versus predictive value". A gapped static vacuum would also give R ∝ ξ·log(1/κ), which is "weak κ dependence", with no prediction involved. A fair comparator holds world and rule fixed and varies only the value functional: static |C_{tj}|² (or static MI) and predictive w_j on the **same** chain, with the **same** greedy rule and the **same** R* definition, in both the critical and the gapped case.

### 1.5 Is the prediction numeric and falsifiable? Partly
The 25% spread is numeric but sits on the edge (above). The growth bound cannot be falsified (above). No world is named where the front should fail, so a hit cannot be told apart from "every local Hamiltonian does this".

### Required amendments for D (all needed before any lock)
- **D1 (reclassify).** State the lemma and prove it on paper: for local H with Lieb–Robinson constants (C, μ, v), the greedy operator-weight record satisfies R* ≤ vk + μ⁻¹ln(C|T|/κ). For nearest-neighbour hopping, add the Airy-edge two-sided estimate. Log it as PIM (an application of KNOWN mathematics), with V ≤ 2 on the step-back's scale. No prereg run is needed for this part.
- **D2 (make it informative).** If a run is still wanted, the value must depend on the state and must be net of holdings. Use a stated predictive-information functional, for example the classical-shadow or Gaussian two-time MI I(R_now ; T_{k} | T_now) for the free-fermion chain, which is computable from correlation matrices. Add the fair static arm in the same world (§1.4).
- **D3 (contrast world).** Add a world without a Lieb–Robinson front, such as long-range hopping 1/r^α with α < 1 (no linear front) or α between 1 and 2, with a prediction that the edge does **not** track vk there. Without it, a hit cannot be told apart from "true of every local H".
- **D4 (definitions and gates).** Fix R* (outermost added site, distance from T's centre, |T| = 5 stated) and the spread formula. Add a finite-size gate (L versus 2L), a precision gate (mpmath at the κ-crossings), and a negative control: a random-phase dephased propagator must change w by less than 1e−12 if the proxy really ignores the state. If it does not, the proxy definition is wrong.
- **D5 (input accounting).** In "what a hit would not mean", add: "the boundary moves from a chosen κ to a chosen lead time k and stake region T; it is not removed unless k is selected by the cost." Optionally add an arm where k* is set by CORE's own condition (the first bit must pay, CT4) for a stated drift. That arm is the only one that could take an input out.
- **D6 (disclosure).** §0 must cite this gate read's Airy table as prior knowledge.

---

## 2. Draft A (C2): is local tomography selected by read cost with equal read prices?

### 2.1 Would a hit mean what it claims? (no, as written)
There are two readings of the tracker, and both leave the test with little to say:
- **Reading 1: the tracker "reads each part locally (and may combine results)".** Then a premium in real QM, whenever stakes load on the holistic parameter (the σ_y⊗σ_y-type direction that local reads cannot see), is **what not-LT means**. The positive control ("real QM must show a premium when joint reads are forbidden") is the same statement as the hit. The clause "when a joint read costs exactly what a local read costs" does nothing, because the tracker never uses joint reads. This is shape 2.
- **Reading 2: joint reads are allowed at equal price.** Then the optimal tracker uses them, and real QM's composite has **fewer** parameters (K = 10 against 16), so full tracking is cheaper in real QM. The predicted inequality min J(real) > min J(complex) would then fail because of dimension, not because the cost does or does not select LT. The draft's MISS branch reads that as "LT is CHOSEN", which mislabels a dimension effect. This is also shape 2.
- **Comparing different state spaces with different ensembles and different stake families is not like for like.** No normalisation (per parameter, or per bit of stake-relevant information) is given, so any difference could come from size alone.

### 2.2 Instrument limits (shape 1)
- **"Read" is undefined.** It could be a single-shot measurement or an exact expectation value. With finite shots the cost of estimating a parameter depends on how the estimator scales, and a poor estimator would print "premium" or "no premium" depending on the shot budget. A gate is needed: the optimal (or Cramér–Rao bounded) estimator is used, checked against the analytic Fisher information on one composite.
- **The optimisation of min J over trackers needs a reach gate.** Reaching joint measurements in real QM needs the full real POVM set, not a parametrised subset. The qm-selection-2 lesson applies: a search that cannot reach part of the space prints the predicted outcome. Add a gate in which the optimiser recovers a known optimum (Helstrom on a stated pair) in each composite.
- **Quaternionic composite "if available".** This has to be decided before the lock, not at run time. A standard treatment exists: Barnum, Graydon & Wilce 2020, "Composites and categories of Euclidean Jordan algebras", Quantum 4:359, 10.22331/q-2020-11-08-359 (Crossref OK this session). Include it with a named composite or exclude it now.

### 2.3 Is the target fixed? (yes)
"Only if stakes load on that parameter with positive weight" makes the outcome depend on the stake family the designer picks. Choosing stakes that load on the holistic parameter gives a hit, and choosing stakes that do not gives a miss. The stakes must come from the invariant ensemble over **all** effects of the composite (for example Haar over the composite's reversible group applied to a fixed generic effect), declared before the lock, with no conditioning on the holistic direction.

### 2.4 Is the prediction numeric? (no)
"At least the cost of resolving the non-local parameter" is not defined numerically. There is no grid, no tolerance, and no effect size.

### Required amendments for A
- **A1 (pick one tracker reading and say what is being tested).** The non-trivial version of C2 is: *with joint and local reads at equal price, and stakes drawn from the invariant ensemble, is there a cost reason to prefer composites whose records can be stored part by part?* That needs a cost the theory already has, not one invented for the test. Candidate: CORE's holding price κ per record held **in each part** (records travel with their parts). A non-LT composite then has K_AB − K_A·K_B parameters that no part-wise memory can hold. If the premium comes only from such a part-wise memory price, the draft must say so up front: that is LT entering as "records live in parts", which is CHOSEN under another name unless part-wise memory comes from locality already in the premise graph. Pre-state which of the two the run can tell apart.
- **A2 (fair comparator).** Normalise by parameter count, or compare a composite with its LT completion at the same local parts (real 2-rebit against complex 2-qubit restricted to real local parts), so dimension cannot decide the sign. State the expected sign from the dimension effect alone as a baseline that the test must beat.
- **A3 (stakes).** Fix the stake ensemble invariantly (§2.3), with no conditioning clause.
- **A4 (numbers).** Give a (w, c) grid, a minimum effect size (for example premium ≥ 5% of min J after normalisation at every grid point), and a tolerance.
- **A5 (gates).** Add an estimator/Fisher gate, an optimiser-reach gate (Helstrom recovery), LT composites showing zero premium (kept), and a positive control that is **not** the hit restated: a hand-built non-LT toy with a known premium under the A1 cost.
- **A6 (quaternionic).** Decide it now (include via BGW 2020 or exclude).
- **A7 (prior).** On the evidence above, p_hit for a non-trivial A is nearer 0.15 than 0.30.

---

## 3. §5 CORE-method scores

- **Arithmetic: OK.** Every EIV and EIV/cost in the table recomputes (C11 4.4/1.76, C2 4.2/1.40, C3 2.07/1.38, C8 1.45, C4 2.5/1.00, C1 3.3/0.83, C6 1.05/0.70, C9 2.4/0.40, C7 2.55/0.43, C10 1.3/0.65, C5 0.62/0.31).
- **C11 breaks the scale's own rule.** The scale says "2 = consistency check whose outcome a known theorem largely fixes", and the C11 caveat says the front is Lieb–Robinson mathematics and the hit is likely for that reason. Yet V_hit = 5. By the scale's own rule V_hit = 2, and p_hit ≈ 0.85 (§1). V_miss = 4 is too high, because a miss would come from the k = 8 threshold or the R* definition and would locate no input, so V_miss ≈ 1. Rescored: 0.85·2 + 0.10·1 = 1.8 → **0.72 per hour** (from 1.76).
- **C2 as drafted** has a hit that is true by definition (§2), so V_hit ≈ 2. Redesigned per A1–A7: p 0.15, V_hit 6, p_miss 0.75, V_miss 3 → 3.15/3 = **1.05 per hour**.
- **The V_miss values are uneven.** C2 and C11 give 4, C1 gives 3, C4 gives 2, with no rule. Under a uniform V_miss = 2 (keeping the author's p and V_hit), C11 = 1.48, C3 = 1.24, C2 = 1.00, C4 = 1.00. C11 then stays first only because of the V_hit = 5 that breaks the scale's rule.
- **Fair reweighting (scale rule applied, V_miss uniform where nothing is located):** C8* 1.45 (sunk lock) · **C3 1.38** · C2-redesigned 1.05 · C4 1.00 · C1 0.83 · C11 0.72 · C6 0.70. With Lean stake ×3 (the step-back's own sensitivity), C9 ≈ 1.2 enters the top three.
- **Does the ranking survive?** **No for C11-first.** C2 stays in the top group only if redesigned. C3 (a cheap consistency check under P, honestly capped) becomes the top new route, then C2-redesigned and C4. The step-back's notes on where CORE's method is underspecified (w unset, research loss undefined, priors outside the method, non-concave VOI, ruin cap not priced) are sound and should stay. Point 4 (EIV/cost biases against C7/C9) matters for Lean: the ranking should be reported with and without Chad's stake weight.

## 4. Spot-check of the step-back's temperature and entanglement claims

**Temperature (§1a): mostly right, with three corrections needed.**
- OK: THEORY.md:195 credits Drăgulescu & Yakovenko 2000 "as an analogy only" (verified, and the DOI is in reviews/thermo_2026-11-21). CT18 is PROVED (in-model) (CLAIM_MAP:539). The H3/G5 record matches NOTE.md:480–522: m = 0 setup miss, not scored, with "had these been scored, P5a/P5b would pass"; m = 0.3 failed as predicted; post hoc slope 0.465 unscored. E-G3G5-1 (R → T belongs to the vacuum) is reflected.
- **T4-1 (label).** K4 is now "NOT A TEST (qualification not established; proxy: failed)" (CLAIM_MAP:409). PROXY-FAIL is its kept history, not its current status. Write the current status.
- **T4-2 (overstatement).** T2 says the temperature = price-of-information identity is "established (prior art plus our in-model versions)" and cites R1, U1, G2. But **R1 is PRIOR ART** (Sella & Hirsh), not PIM, and in both R1 and U1, β is a **selection strength** (β = αν from population size; β_i in a Moran chain), not a price per nat of information. CLAIM_MAP **G2** is an unrelated row (POOLSIM, NOT EVIDENCE). If the forces-gravity G2 is meant, the path must be named. Correct wording: "the identity λ = temperature is KNOWN (Sims 2003; Matějka–McKay 2015; Ortega–Braun 2013); GTAO's in-model rows R1 (PRIOR ART) and U1 (PIM) give the same Boltzmann form with β a selection strength; the link between the two is form-level". This matters for Chad's question: the "economics paper" temperature in THEORY is CT18/Drăgulescu–Yakovenko, which is **an analogy**, not the same formula as a physical temperature.
- **T4-3 (label).** "A clean re-run would very likely be a hit" (§1a) needs the HYP label and a pointer to C6. It rests on post hoc, unscored numbers.

**Entanglement (§1b): correct in substance, needs scope labels.**
- OK: it matches rnd/entangle/THREAD_SUMMARY (Theorem E1 proved, elementary, with the existential equivalence; "re-expressed, not derived"). Item (iii) states the gap honestly. RC13–RC19 match CLAIM_MAP:938–944.
- **E4-1 (status source).** This E1 is the R&D-notes theorem and **is not a CLAIM_MAP_v2 row**. CLAIM_MAP's E1 is an unrelated row (T5.1 V(N*)). Since CLAIM_MAP is the only status source, write "PIM in R&D notes, hostile-reviewed (HOSTILE_REVIEW_E1), not yet in CLAIM_MAP_v2" and rename it (for example "Ent-E1") to avoid the collision.
- **E4-2 (hypothesis list).** Add "product effects valid" and "LT is used in ⇒" to the E1 hypothesis list, as in THREAD_SUMMARY:15–20.
- **E4-3 (overstatement in plain words).** "This is the sense in which 'we have entanglement'" and "reversible record-making from a pure start entangles is proved" should carry the condition in the same sentence: *given LT, NR, RV, a pure product start, and tracking (a correlated pair appears), which is the entangling premise re-expressed*. Without it, a reader (including Chad, who said "I thought we have entanglement") will read it as the cost giving entanglement, which item (iii) correctly denies.

**Wording scan of STEPBACK.md.** No "verdict/solved/bill/dead/kill/puzzle/theory of everything". "law" appears at :18, :87, :88, :96 ("first law" of entanglement) and :113 ("area-law"). The repo rule allows "law" only in the CORE.md:7 sentence. For non-repo notes this is low severity, but anything carried into the repo should read "the first-order relation δS = δ⟨K⟩" and "area scaling".

## 5. Required before any lock (checklist)
1. D: do not lock as a test. Write D1 as a short PIM lemma. Any run follows D2–D6.
2. A: redesign per A1–A7, then a fresh gate read.
3. §5: rescore C11 and C2 per §3 and re-issue the ranking (C3 first among new routes; C11 below C4 unless D2/D3/D5 change it).
4. §1a/§1b: corrections T4-1…3 and E4-1…3, appended (the original text kept).
5. No lock, push or run happened during this read.
