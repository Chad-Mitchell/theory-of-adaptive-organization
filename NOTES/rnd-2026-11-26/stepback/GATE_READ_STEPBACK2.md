# Gate read 2: STEPBACK §§9–12, PIM_LEMMA.md, PREREG_DRAFT_C3.md, PREREG_DRAFT_A2.md (Thu 26 Nov 2026, 06:51 ET)

Fresh hostile reviewer. Files read (sha256 prefixes): STEPBACK.md dd85e340…, PIM_LEMMA.md e0348f0c…, PREREG_DRAFT_C3.md 85ea269c…, PREREG_DRAFT_A2.md 45b77b22…. Repo text read from the read-only clone `/workspace/stepback-src` (04c8309). Primary sources read this session: Barrett 2007 (arXiv quant-ph/0508211v3, full text) and Hardy 2001 (arXiv quant-ph/0101012v4, full text), plus the MMPA 2014 text already in `rnd/forces-gravity/mmpa2014.txt`. DOIs were checked on Crossref this session (`crossref_gate2.txt`). Nothing committed, nothing locked edited, no email sent.
Labels: OBS observed · HYP hypothesis · PIM proved in model · KNOWN published · CHOSEN input.

## Outcome summary

| item | outcome |
|---|---|
| **A2 §1, "LT merges into P6, so it stops being a separate premise"** | **FAIL as stated.** The counting fact is real, but it is attributed to the wrong paper. "P6 on composites of fixed parts" is a new clause, not P6. Under the chain's own interaction premise I it selects the **non-LT** real-QM composite for disk parts. An outside reader would see a known equivalence relabelled, not a reduction in premises. Keep it as a reformulation note (amendments 1a–1f). |
| **PIM_LEMMA.md (D1)** | **PASS for the bound**, which is correct. **FAIL for the reading** "ends at the signal front": only an upper bound is proved, and for fixed κ and large k the record does not reach the front (it becomes empty). Amendments 2a–2d. |
| **PREREG_DRAFT_C3** | **FAIL (amend, then gate again).** Arm 2's "≥ 36/40 rigid, 0/40 free" outcome is close to forced by the random symmetry-breaking construction (shape 2). For the pentagon × heptagon family the start search cannot reach the starts Θ(1,0) needs in odd polygons, so it could print "rigid" whatever the world is (shape 1). The RV rule conflicts with gate G4 (Aut versus CP-Aut). There is no timeout rule, and cuboctahedron² is wrongly listed as theorem-fixed. Amendments 3a–3j. |
| **A2 §2 residual test** | **FAIL (do not lock).** The world set may be empty. The outcome is set by a CHOSEN holistic drift rate and by isotropy. Two of the four gates do not guard any step in the pipeline. The draft's own recommendation not to lock is right. |
| §§9–12 bookkeeping | Spot-checks pass (details in §5). |

---

## 1. A2 §1: does the composite dimension price make LT cost-optimal, and does LT stop being a premise?

### 1.1 Is K_AB ≥ K_A·K_B, with equality iff LT, Barrett's result? (no; it is Hardy's counting, and the equivalence is standard)
- **Barrett 2007 assumes LT; it does not prove the inequality.** Its Assumption 5, "The Global State Assumption", says the global state is "completely determined by specifying joint probabilities of outcomes for fiducial measurements performed simultaneously on each subsystem". It then notes this "is not true in the case of quantum theory defined over a real Hilbert space… So this assumption has significant content" (arXiv v3, lines ~514–524 of the text). Barrett is a fine citation for LT as an assumption, and for real QM violating it. He is **not** the source for K_AB ≥ K_A·K_B with equality iff LT. [OBS, read this session]
- **The counting is in Hardy 2001, §6.15.** If pure states give factorising joint probabilities, the K_A·K_B product fiducial states are linearly independent, so "to describe convex combinations of the separable states requires K_A K_B degrees of freedom". Hardy then gets K = K_A·K_B from a second assumption: the composite has "not greater" degrees of freedom "than… the separable states… since we do not expect there to be more entanglement than necessary". He also notes that real-Hilbert-space composites "have more degrees of freedom than the product", and that quaternionic composites "would have to have less", which violates the factorising assumption. [OBS, read this session]
- **"Equality iff LT" is standard and needs only three lines.** In finite dimension, with product states present and product effects valid, the K_A·K_B product effects are linearly independent functionals on the composite's state space. LT means the product effects separate states, which means they span the K_AB-dimensional effect space, which means K_AB = K_A·K_B. Write this proof into the note, and state the hypotheses: finite dimension; product states exist with factorising probabilities; product effects valid. Quaternionic QM fails the second, so it lies outside the inequality's scope (consistent with A2's A6 exclusion).
- **Prior art for the "minimum dimension" reading:** Hardy 2001 motivates his composite axiom with exactly this minimality argument ("not more entanglement than necessary"), and he **still states it as a separate axiom (Axiom 4)** next to his own dimension-minimality axiom (Axiom 2, Simplicity: "for any given N, K takes the minimum value consistent with the axioms"). So minimality inside a theory has already been used to motivate LT, and the composite rule was still kept as its own axiom. Hardy & Wootters 2012, "Limited holism and real-vector-space quantum theory", Found. Phys. 42:454 (10.1007/s10701-011-9616-6, Crossref OK, title and metadata only, not read), is the natural further credit for the K_AB − K_A·K_B "holism" count.

### 1.2 What P6 is in the repo, and whether the composite extension follows
- **P6 as frozen** (`theory/qm-selection-2026-11-26/PREREG.md:26`): "Among bodies that satisfy P1–P5, with capacity N…, a smaller affine dimension d is cheaper. Every bit face of a higher-rank body is the cheapest bit. **The dimension price is not derived from additivity** (chain note `:98`)." So P6 is **CHOSEN**, and it orders **single bodies at fixed capacity N**.
- **The extension does not follow from P6.** A composite is a body, so P6 as written already applies to it. But it compares the composite with **every** P1–P5 body of capacity N_A·N_B, not with other composites of the same parts. Applied literally, P6 would pick whatever P1–P5 body of that capacity is smallest, which need not be a composite of the given parts at all. "Among composites **of fixed parts**, smaller K_AB is cheaper" (call it **P6′**) adds a new ordering: a new domain (composites of given parts) and a new fixed quantity (the parts, not the capacity). **P6′ is a new premise.** Replacing LT by P6′ leaves the premise count unchanged.

### 1.3 Does the optimum exist within the allowed class? (yes without I; with I, the answer is not LT for disk parts)
- **Without the interaction premise I:** min, max and every composite between them are LT and tie at K_A·K_B. So P6′ picks out the LT slice, and the optimum exists. Here P6′ and LT are the same statement in different words.
- **With I (chain α assumes it):** for disk (rebit) parts, no LT composite has a continuous reversible interaction (MMPA 2014, JMP 55:122203, 10.1063/1.4903510, Crossref OK; the abstract says for d-ball parts with LT and continuous reversible dynamics "except for the quantum two-qubit state space, none of them contains entangled states… interacting dynamics is impossible"). So the interacting class at disk parts has K_AB ≥ 10. Real QM has K = 10 (the least integer above 9) and has continuous interactions, so **P6′ + I selects the non-LT real-QM composite.** P6′ does not imply LT under the chain's premises; at disk parts it selects against it.
- **What actually removes disks in the chain is P5** (hSFP; P5's row lists "real QM (disk faces), even balls"), not LT or P6′. For 3-ball parts, P6′ + I does land on the LT slice, because QM attains K = 16 with interaction, and then de la Torre et al. 2012 (PRL 109:090403, 10.1103/PhysRevLett.109.090403, Crossref OK) gives QM. Small attribution fix: A2 §1.3 cites de la Torre et al. for the disk statement, but de la Torre is the d = 3 classification (Thm 2 in `rnd/entangle/NOTE.md:33`). The disk statement is MMPA's.

### 1.4 Real reduction or relabelling? (relabelling)
An outside reader would see LT ⇔ K_AB = K_A·K_B ⇔ "the composite has the smallest dimension its parts allow" as a known equivalence (Hardy 2001 §6.15), with the dimension price itself chosen. Swapping LT for P6′ changes the wording but not the premise count. The most that can honestly be said is HYP: *if* one cost principle priced the dimension of single bodies and of composites alike, with no separate fixed-parts clause, the chain would have one premise where it now has two. That needs P6 to be derived from the cost, and the repo says it is not. Within chain α it also only works after P5 has removed disk parts.

### 1.5 DOIs (Crossref, this session; `crossref_gate2.txt`)
Barrett 2007 10.1103/PhysRevA.75.032304 OK · MMPA 2014 10.1063/1.4903510 OK · de la Torre, Masanes, Short, Müller 2012 10.1103/PhysRevLett.109.090403 OK · Barnum, Graydon & Wilce 2020 10.22331/q-2020-11-08-359 OK · Hardy & Wootters 10.1007/s10701-011-9616-6 OK (online 2011; Found. Phys. 42, 2012) · Masanes–Müller 2011 10.1088/1367-2630/13/6/063001 OK. Hardy 2001 is arXiv only (no DOI claimed; text read).

### Amendments to A2 §1
- **1a.** Replace "Barrett 2007" as the source of the counting with **Hardy 2001 §6.15**. Keep Barrett for "LT as an assumption (Assumption 5); real QM violates it".
- **1b.** Write out the three-line proof of "equality iff LT" with its hypotheses (finite dimension; product states with factorising probabilities; product effects valid), and say quaternionic falls outside them.
- **1c.** Rename the claim. Do not write "LT merges into P6" or "LT stops being a separate premise". Write: "*KNOWN equivalence: at fixed parts, LT ⇔ minimal K_AB. Adopting P6′ (a dimension price on composites at fixed parts) is equivalent to LT when no interaction is required. P6′ is a new clause; P6 itself is CHOSEN; premise count unchanged.*"
- **1d.** State the I clash as a finding: P6′ + I selects real QM at disk parts, and it is P5 that removes disks in the chain.
- **1e.** Credit Hardy 2001 (and Hardy & Wootters 2012) for the minimality motivation, and note that Hardy keeps the composite rule as a separate axiom.
- **1f.** Fix the attribution of the disk result (MMPA 2014, not de la Torre 2012).
- **Value:** a reformulation note. V ≤ 2, and no merge in the premise graph.

---

## 2. PIM_LEMMA.md (D1)

### 2.1 The proof: correct
- **Kapteyn (DLMF 10.14.8):** |J_n(nz)| ≤ |z^n e^{n√(1−z²)}| / |1+√(1−z²)|^n for n ≥ 0 and |z| ≤ 1. With z = 2k/n = sech α (integer n ≥ 2k, so z ≤ 1): √(1−z²) = tanh α, and z·e^{tanh α}/(1+tanh α) = e^{tanh α}/(cosh α + sinh α) = e^{tanh α − α}. ✓ So |J_n(2k)| ≤ e^{−n(α − tanh α)}. The bound uses |J_{−n}| = |J_n|, which the note should state since j − t can be negative. ✓
- **g increasing:** φ(α) = α − tanh α has φ′ = tanh² α ≥ 0, and α(n) is increasing, so n·φ(α(n)) is increasing. ✓
- **Steps 3–4:** for d(j,T) ≥ 2k, every |j − t| ≥ d, so w_j ≤ |T|e^{−2g(d)}. For d ≥ d\*, 2g(d) ≥ 2g(d\*) > ln(|T|/κ), so w_j < κ. Sites with d < 2k are not bounded, but d\* > 2k (because g(2k) = 0 and ln(|T|/κ) > 0), so **R\* < d\*** holds. ✓
- **Asymptotic:** cosh α = 1 + ε/2k gives α ≈ (ε/k)^{1/2} and φ ≈ α³/3, so 2g ≈ (4/3)k^{−1/2}ε^{3/2} and ε ≈ k^{1/3}(¾ ln(|T|/κ))^{2/3}. That equals the stated (2k)^{1/3}2^{−1/3}(…)^{2/3}. ✓ It matches the Airy exponent (4/3)s^{3/2} with s = k^{−1/3}ε, so the exponent is tight. The bound drops the Airy prefactor (about k^{−2/3}), which is why d\* runs 4–8 sites above the observed R\* in `lemma_check2.out` (reproduced: 15/15, and 0 Kapteyn violations).
- **The general form is fine as PIM given KNOWN**, but it is only as precise as the stated Lieb–Robinson form ("up to the bound's own form"). A fermionic or free-particle version is needed for the hopping chain. Cite which version is used.

### 2.2 Scope: an overstatement to fix
- **Only an upper bound is proved.** The title ("…ends at the signal front"), the "Does" bullet ("ends the record at the dynamics' signal front plus an O(…) edge") and the asymptotic sentence ("the record ends within O(k^{1/3}…) of the front") all read as two-sided.
- **For fixed κ and k → ∞ the record does not reach the front at all.** The largest single-term weight near the front is max_n |J_n(2k)|² ≈ 0.29·k^{−2/3}. Computed this session with mpmath: 0.074 at k = 8, 0.029 at 32, 0.011 at 128, 0.0045 at 512, 0.0018 at 2048. So w_j ≤ |T|·0.29·k^{−2/3}·(1 + o(1)) everywhere, and the record becomes **empty** once k^{2/3} ≳ 0.29|T|/κ. The asymptotic statement about d\* is true, but as a statement about R\* it says nothing there. A lower bound (R\* ≥ 2k − O(k^{1/3}) or similar) holds only when κ ≲ c·k^{−2/3}, and it is not proved.
- **Amendments:**
  - **2a.** Retitle to "…never extends past the signal front (upper bound)".
  - **2b.** Reword "Does" as "R\* < d\* = 2k + O(k^{1/3}(ln(|T|/κ))^{2/3}); the record never extends past the front plus an Airy edge".
  - **2c.** Add the regime note: the record reaches the front only for κ ≲ c·k^{−2/3}, and for fixed κ and large k it is empty. A lower bound is unproved.
  - **2d.** State |J_{−n}| = |J_n|, and say that step 5 is a leading-order expansion (error terms not bounded).
- With 2a–2d the lemma passes as PIM, an application of KNOWN mathematics, V ≤ 2.

---

## 3. PREREG_DRAFT_C3

### 3.1 Arm 2: are "≥ 36/40 rigid" and "0/40 free" principled? (no; they are nearly forced by the construction)
- **Shape 2.** S = conv(min ∪ R) with R a *random* k-subset of max's non-product extreme points generically breaks the local symmetry. Aut(S) then tends to sit inside the stabiliser of R in the local group (D5 × D7, order 140, for pentagon × heptagon, with no swap; for cube × octahedron, the local group of order 48·48 with no swap, as the parts differ). Every element of that stabiliser is a product map, so it preserves products, so the class is "rigid" by E-L0. Rigidity follows from the randomisation, not from anything the theory says. The draft's own prior (0.6 for ≥ 36 rigid) is far too low for this argument (≥ 0.9 is more honest), and the cut at 36 has no derivation.
- **These worlds also leave the premise set.** In non-locally-symmetric S, most local reversible maps are **not** automorphisms of S, so the premise "local reversible maps stay reversible", used by M12 and RC13–RC19, fails by construction. A "rigid" result there says nothing about Conjecture C in the classes the theory cares about. RC14 does list such composites as open, so they are in scope as a question, but the draft must say this outright.
- **Shape 1 (start-search reach) for odd polygons.** In a regular pentagon or heptagon with all effects, **no two vertices are perfectly distinguishable**: a vertex's perfectly distinguishable partner is a point on the opposite edge, which is a mixture. §3.3 searches only (a) pure product starts and (b) uniform mixtures of **two vertices** on one part. So a Θ(1, 0) start in the pentagon × heptagon family that needs an edge-point partner, or more than one bit of start entropy, cannot be reached, and the classifier prints "infeasible" = **rigid, the predicted outcome**. The positive control G3 (pyramid × square) has distinguishable vertex pairs and does not exercise this. This must be fixed before any lock.
- **The informative version** is the open part of RC14/RC16: **locally symmetric** intermediates of odd-polygon parts. Take R = a union of local-group orbits of max's non-product extreme points for pentagon × heptagon (or pentagon²). Odd polygons fail ★ and are explicitly open. That keeps the theory's premises, tests Conjecture C where it is open, and does not hand the outcome to the randomisation.

### 3.2 Gates G1–G8
- **G1 (group reach): good in kind, but incomplete.** The listed orders match the notes (`rnd/entangle/THREAD_SUMMARY.md:28–37`, R16: 120² = 14400). Triangle² = 9! is a real test of reaching non-local automorphisms. **Missing:** a known-order case **in the same number field** as Arm 2, Q(cos 2π/5, cos 2π/7), of degree 6. For example, pentagon × heptagon min should have order 140 (no swap), and pentagon² min/max should have the local group ⋊ swap. Without it, G1 says nothing about the exact arithmetic Arm 2 relies on.
- **G2 (canonical forms): needed (the R14 lesson), but specify it.** In a degree-6 field, require exact reduction to a fixed Q-basis (or minimal polynomials) for every value used in colour refinement, and compare the exact class count with the float class count on **the same quantities**. A count match at 1e−9 is necessary, not sufficient. Also require that one hand-checked pair of algebraically equal expressions in different forms lands in one class.
- **G3 (fuel-needing positive control): right idea, wrong parts.** Add an **odd-polygon** control where Θ(1,0) is known to be feasible only with a non-vertex partner, or else prove that no such start exists in these families and record that proof. Without it, §3.1's reach gap stays open.
- **G4 (free positive control): inconsistent with §3.1 of the draft.** The method sets "reversible maps = Aut(S)", but G4 expects 11520 ("under RV"). The notes give **|Aut(S)| = 23040** for the 2-qubit stabilizer polytope, with 11520 the CP-restricted group (HOSTILE_REVIEW_E1 row 4b; THREAD_SUMMARY:37). Fix one RV rule (Aut(S) or CP-Aut) for every arm and state the expected order under it. Otherwise G4 fails, or passes, for the wrong reason.
- **G5 (negative control):** OK.
- **G6 (estimator):** OK. Helstrom ½(1 + 1/√2) for |0⟩ versus |+⟩ is correct. **Define S_min's entropy**: GPT mixed states have many pure decompositions, so use the minimum over decompositions, and state that measurement entropy and decomposition entropy differ in general GPTs.
- **G7 (hypotheses): replace the "+ …".** Every S between min and max is LT automatically (same span), so G7 should state K_S = K_A·K_B exactly and check it, not a formula with an ellipsis.
- **G8 (exact re-verification):** OK.
- **Missing G9 (time limits, the R14 H1/H2 lesson):** set a per-composite time limit for vertex enumeration of max (cube × octahedron max and pentagon × heptagon max can be large), a rule that a timeout counts as "not tested", and a minimum number of completed composites (for example ≥ 32/40) for Arm 2 to be scored. State predictions as fractions of the completed composites.

### 3.3 Arms 1 and 3
- **Cuboctahedron² max is not theorem-fixed as "rigid".** RC18 plus M12 exclude *entangling* maps in locally symmetric composites. "Rigid" also needs no *correlating non-entangling* map, which needs Aut(S) ⊆ local ⋊ swap, and no Aut order for cuboctahedron² is recorded in the notes or the repo. Either compute it in G1 before the run, or move it to the open arm.
- **Arm 3, QM:** to avoid round-off building up over 10⁶ steps, compute U^n by eigendecomposition (e^{−inθE}) rather than repeated multiplication. Also state that a quasi-periodic orbit comes arbitrarily close to its start, so "> 1e−12 in 10⁶ steps" is a numeric threshold, not "no recurrence".

### 3.4 Score
With p(as predicted) ≈ 0.9 for the random arm, EIV ≈ 0.9·2 + 0.01·9 + 0.09·3 ≈ 2.2 over 3 h, about **0.72 per hour** (draft: 0.84). The orbit-union redesign (3c) moves C3 toward C7 territory (V_hit about 3, V_free 9), at the cost of the Q-extension enumeration time.

### Amendments to C3
- **3a.** Declare Arm 2's random composites as worlds outside the local-reversibility premise, and give the honest prior (≥ 0.9 rigid).
- **3b.** Derive or drop the 36/40 cut.
- **3c.** Add (or substitute) an orbit-union arm of locally symmetric odd-polygon intermediates.
- **3d.** Widen the start search to starts with non-vertex partners and more than one bit, or prove for these families that such starts never help.
- **3e.** Add an odd-polygon positive control for G3.
- **3f.** Add a same-field order control to G1 (pentagon × heptagon min, 140; pentagon² min/max).
- **3g.** Fix one RV rule and correct G4's expected order (23040 for Aut(S), 11520 for CP-Aut).
- **3h.** Define S_min as the minimum over decompositions (G6), and give G7's exact K_S formula.
- **3i.** Add G9: time limits, the not-tested rule, and a minimum completed count.
- **3j.** Remove cuboctahedron² from the theorem-fixed list unless its Aut order is computed first. Use the eigendecomposition for Arm 3.

---

## 4. A2 §2 residual test: FAIL (do not lock)
- **The world set may be empty.** It needs non-LT composites of **complex qubit** parts in the BGW 2020 category. As far as I know from BGW's construction, composites of complex parts there are the standard (LT) tensor product, and non-LT arises with real (and quaternionic) parts. I have not verified this on BGW's text. The draft already makes the lock conditional on confirming such a composite, and that condition must be checked against BGW's text first.
- **The outcome is set by a CHOSEN constant (shape 2).** Normalising the drift so that every *local marginal* moves at the same rate leaves the holistic coordinates' drift rate **free**. Any "premium beyond dimension" is then a function of that chosen rate, and G4's positive control literally declares it. With isotropic invariant drift and squared-error stakes on the full state, the minimal learning rate is additive over coordinates, so "per-dimension agreement within ±5%" follows from isotropy. The test decides only whether the CHOSEN holistic rate equals the local one.
- **The gates don't fit the pipeline.** G1 compares SU(2) Brownian drift on the Bloch sphere with a "Gaussian-channel tracker analytic value", but drift on a sphere is not Gaussian, and no analytic value is named. G2 (Helstrom) checks a discrimination optimiser that the §2 pipeline never uses. G3 and G4 are fine in kind.
- **No amendment makes it informative without a cost-derived holistic drift rate.** Record it as an open question ("what sets the drift rate of holistic parameters?"), not as a test.

---

## 5. §§9–12 spot-checks (pass)
- §9 C9-1…C9-8 correctly carry out the first gate read's T4/E4/D/A items. C9-1's R1 PRIOR ART at :651, U1 PIM at :692, and the remark that G2 is the forces-gravity round all check out.
- §10: CT4 is PROVED (in-model) (CLAIM_MAP:525). T63 is PROVED (in-model) (CLAIM_MAP:901). C12c's "judgment absent iff ruin cap slack at w = 0" is correctly labelled HYP, but "iff" is strong: it needs a proof that a zero-memory design meets the cap whenever the cap is slack (CT22's B_slack definition), and that fact should be cited.
- §11: CT25's z_ε = 2.576, 3.291, 4.892 match THEORY.md:402 and erfc(z/√2) = 10⁻², 10⁻³, 10⁻⁶. "Lundberg is CT22's lifetime ruin, a different constraint" matches THEORY.md:186. CORE.md:19 (Horowitz & Esposito 2014, KNOWN in those classes) and CORE.md:29 ("Temperature does not set w") are quoted correctly.
- §12: its reading ("no new route scores above about 1 per hour; the highest-value steps are paper merges") should drop "merge" for LT per §1 of this read: it is a reformulation, not a merge. With this read's C3 rescore (about 0.72), the new-route ranking is C4 1.00 · C12c 0.95 · C12b 0.90 · C1 0.83 · C3 0.72 · C11 0.72 (lemma) · C6 0.70 · A2 residual (not lockable). With Chad's Lean stake ×3, C9 (about 1.2) leads.
- Wording: no banned words in §§9–12, the lemma or the two drafts, beyond what §9 C9-5 already handles.
