# C4 paper step: is record-dependency order on a fixed lattice Lorentz-like?

*R&D note, 26 Nov 2026, local only (no repo change). Route C4 from STEPBACK §6 Draft C and the §5/§13 tables, ranked 1.00. No simulation was run. The Draft C prereg is not locked, and nothing here looks at simulated data.*
Labels: PROVED (in-model) = written proof, self-check, not reviewed · HYP · KNOWN.

## 1. Model (as in Draft C)
- **Sites and records.** Sites i ∈ ℤ, each with an independent Poisson record clock of rate 1. Records are the points (i, t).
- **Dependency.** A record at site i depends on the latest earlier records at i − 1, i and i + 1. The order ≺ is the transitive closure of this dependency.
- **Causal paths.** Unwinding the closure, e ≺ e′ iff there is a sequence of records e = r_0, r_1, …, r_N = e′ with strictly increasing times and |site(r_{k+1}) − site(r_k)| ≤ 1.
  - *Proof:* a latest-record dependency at a neighbour site, together with same-site dependencies, links any earlier record at a neighbour site through that site's chain. Each link moves by at most one site.
- **Chain length.** L(x, t) is the longest chain from the origin record (put at (0, 0)) to a record at site x with time ≤ t. It is defined when (x, t) is causally reachable from the origin.

## 2. Results
**C4-1 (front speed). PROVED (in-model).**
- Let T(x) be the earliest time at which a record at site x > 0 is reachable. Then T(x) = Σ_{k=1}^{x} E_k, with E_k iid Exp(1). So T(x)/x → 1 a.s., and the causal front moves at **v = 1 site per unit time**.
- *Proof:*
  - A path reaching site k for the first time must come from site k − 1 and needs a record at k after its arrival time at k − 1.
  - By induction, the arrival time at k is ≥ the first record at k after T(k − 1). The greedy path attains this.
  - By memorylessness, the waits are iid Exp(1). Almost-sure averaging (SLLN) finishes the proof. ∎

**C4-2 (chains on the cone are long). PROVED (in-model).**
- If (x, t) is reachable, then L(x, t) ≥ |x|. Every causal path changes site by at most 1 per record, so it contains at least |x| records after the origin.
- Near the front (|x| ≈ t), chains therefore have length about t, not about 0.

**C4-3 (bounds on the time constant). PROVED (in-model).**
By superadditivity (Kingman), L(⌊st⌋, t)/t → γ(s) a.s. for |s| < 1. Here γ is concave and symmetric.
- **Lower bound, γ(0) ≥ 3.**
  - Greedy: from site i at time τ, take the first record after τ on {i − 1, i, i + 1}. The gaps are iid Exp(3) and the steps are iid uniform on {−1, 0, 1}.
  - So by time t − t^{2/3}, the path has about 3t records and a displacement of O(√t).
  - Returning to site 0 takes O(√t) hops of Exp(1) each, which fits in the remaining t^{2/3} time with probability → 1.
- **Upper bound, γ(s) ≤ 3e.**
  - The expected number of chains with N records from the origin within time t is ≤ 3^N·t^N/N!.
  - This is summable once N ≥ 3e(1 + ε)t, and Borel–Cantelli gives the bound.
- **Concavity.** γ(s) ≥ (1 − |s|)·γ(0) + |s|·1 ≥ 3 − 2|s| on [−1, 1], using γ(±1⁻) ≥ 1 from C4-2.

**C4-4 (no Lorentzian geometry matches both order and chain length). PROVED (in-model, asymptotic, a.s.).**
- In a 1+1 Minkowski causal set (Poisson sprinkling), the longest chain is asymptotically ∝ the proper time √(t² − x²/c²), which → 0 on the light cone. This is KNOWN: Brightwell–Gregory 1991.
- Here:
  - (a) A metric whose causal order matches ≺ asymptotically must have c = v = 1 (C4-1). Events with |x/t| > 1 are not related, so a larger c would order events the poset leaves unordered; a smaller c would leave unordered events the poset orders.
  - (b) With c = 1, L/τ ≥ |s|/√(1 − s²) → ∞ as |s| → 1 (C4-2).
- So **no hyperbolic level sets with the causal cone as asymptote**, and Draft C's predicted "fail" is fixed by theorem, not by a run.

**C4-5 (generality). PROVED (in-model).**
- The same argument holds for any fixed spatial lattice with dependency range r and positive per-site record rate.
- Each spatial hop costs at least one record, so L ≥ |x|/r on the reachable region, while the front speed is finite. Chains along the cone stay Θ(t).
- The break is the lattice itself: a preferred frame, in which "light-like" chains carry Θ(t) records.

## 3. What this means
- **Located break (PROVED (in-model)):** record order on a fixed memory lattice is causal (it gives an order and a finite front) but not Lorentzian.
  - This matches the causal-set result that Lorentz invariance with discreteness needs **random** placement of elements. That result is KNOWN: Bombelli–Henson–Sorkin 2009, MPLA 24, 10.1142/S0217732309031958, "Discreteness without symmetry breaking: a theorem"; Dowker–Henson–Sorkin 2004, MPLA 19, 10.1142/S0217732304015026.
  - Bombelli–Lee–Meyer–Sorkin 1987 (10.1103/PhysRevLett.59.521) and Malament 1977 (10.1063/1.523436) supply the order → conformal-geometry link.
  - DOIs verified on Crossref (`crossref_c4.txt`).
- **For C4 as a route:** its informative outcome was "a hyperbolic shape on a fixed lattice", and that is excluded by C4-4. The miss branch ("localizes the break at the memory lattice") is now delivered on paper.
  - Rescore: a run would be a V = 2 check. EIV ≈ 0.98·2 + 0.02·8 ≈ 2.1 over 2.5 h ≈ **0.85 per hour**, and falling, because the content is already on paper. **Do not run Draft C.**
- **What remains open (HYP), and is the real C4 question now:**
  - **C4′ (cost places records).** Lorentz-like order needs records at Poisson-random spacetime locations (a sprinkling) rather than on per-site clocks. Does the record cost choose the placement? That is, among record-placement rules with a given mean density, is the rule that minimises a stated cost Poisson in spacetime?
    - This is F2 again: the cost would have to choose where records live.
    - A candidate paper argument (HYP): with no preferred location or frame in the cost (translation and boost invariance of the price), the max-entropy placement at fixed density is Poisson. That would only restate the Bombelli–Henson–Sorkin symmetry premise as a "cost premise". It is CHOSEN, not derived, unless the price itself is derived to be boost-invariant.
  - **C4″ (free fit).** Can γ(s), for |s| < 1 only, be fitted by γ(0)·√(1 − s²/c′²) with c′ ≠ 1? C4-3 only bounds this. It would need γ, numerically or exactly. It is of little value, because C4-4 already excludes Lorentz-compatible order.
- **Next step proposed:** a one-page check of whether any record-placement cost in the repository (RECORD-COST J, transport costs) is boost-invariant. If none is, C4′ is CHOSEN by construction and should be logged as an open miss with that input named.

## 4. For a reviewer
Points to check:
- the C4-1 induction (first-passage = greedy);
- the C4-3 return step, which uses t^{2/3} slack;
- C4-4 (a), the argument that the order fixes c, which leans on Malament/HKM-type reasoning applied asymptotically rather than to an exact continuum;
- whether "longest chain ∝ proper time" (Brightwell–Gregory) is the right Lorentzian benchmark in 1+1 dimensions.

---

## 5. Corrections after the hostile review (appended; §§0–4 above are left as written)
Source: `rnd/review_c4/HOSTILE_REVIEW_C4.md` (PASS-WITH-FIXES), with `c4_lpp.c`, `brute_check.py`/`.out` and the `run_T*_s*.out` files. Where this section disagrees with §§1–4, this section holds.

**C5-1 (H1): "Draft C's predicted fail is fixed by theorem" is withdrawn.**
- Draft C measures the fitted *exponent* of chain length against √(t² − x²/v²). In this model L(st, t) ≈ γ(s)·t and τ = t√(1 − s²), so the exponent is 1 along every ray with |s| < 1.
  - The review observed that the exponents at s = 0 and s = 0.5 agree to within 0.2% at T = 16000 (OBSERVED).
- C4-4 is about the *prefactor* γ(s)/√(1 − s²), not the exponent.
- **Draft C as written would therefore read a false "Lorentz-like" hit.** This is logged as an **open miss in the Draft C design**: the wrong observable. It is not an open miss of C4-4.
- **Rule for any future C4 test:**
  - the observable is the ratio R(s) = γ(s)/(γ(0)·√(1 − s²)), or the level-set shape itself;
  - a Poisson-sprinkling control in 1+1 Minkowski must give R ≡ 1 within its stated error;
  - for reference, the review observed R ≈ 1.12 at s = 0.5 and R ≈ 2.04 at s = 0.9.
- "Do not run Draft C" stands, now for this reason: as written, it cannot tell the cases apart.

**C5-2 (H2): blindness.** The Draft C world has now been simulated (by the review). §0's "No simulation was run" was true when written. **Any future C4 prereg is not blind to γ(s), the exponents or the front speed, must say so, and must cite `rnd/review_c4/HOSTILE_REVIEW_C4.md`.**

**C5-3 (M1): front speed.**
- C4-1's "exactly 1" means v = λ·a (clock rate × site spacing). It is an almost-sure long-run limit, here λ = a = 1.
- T(x) ~ Gamma(x, 1), so the front has width of order √t, and P(T(x) < x) → 1/2.
- C4-4(a)'s "events with |x/t| > 1 are not related" holds for |x/t| > 1 + ε, with probability → 1.

**C5-4 (M2): scope of C4-4.** C4-4 is narrowed to: **no flat, homogeneous 1+1 Minkowski metric with uniform Poisson sprinkling matches both the order and the chain lengths.** PROVED (in-model), asymptotic, a.s.
- Reaching "no Lorentzian geometry at all" would need two further steps, both HYP and not written:
  - (i) statistical translation invariance forces a homogeneous metric, and in 1+1 the order fixes the conformal class;
  - (ii) no position-dependent conformal factor yields the direction-dependence of γ(s) from one base point.
- The curved-space "longest chain ≈ proper time" relation is not covered by Brightwell–Gregory 1991.
- The like-for-like scaling check (both chain lengths ∝ 1/a at fixed c = λa) passes, per the review.

**C5-5 (M3): C4-5 is a PROVED-sketch (in-model).**
- Its scope is narrowed to a **periodic lattice with finite-range dependencies and per-site rates bounded above and below.**
- Finite front speed follows from the same counting bound: at most (2r + 1)^N·(λ_max·t)^N/N! paths.
- In d ≥ 2 the reachable set is a first-passage-type limit shape, generally not round. Isotropy fails there before chain length enters.
- Disordered fixed graphs are not covered.

**C5-6 (M4): prior art and novelty.**
- §3's sentence "Lorentz invariance with discreteness needs **random** placement … KNOWN: Bombelli–Henson–Sorkin 2009" is replaced by:
  - the result is **consistent with the causal-set view (Dowker–Henson–Sorkin 2004) that Lorentz invariance with discreteness needs random placement**;
  - **BHS 2009 proves that Poisson placement picks no frame** (sufficiency);
  - **necessity is argued, not proved.**
- That a regular lattice picks out a frame is standard background, so the located break is KNOWN in substance. **Novelty is low:** only its realisation for the record-dependency rule is specific to this note.

**C5-7 (M5): C4′ restated** as a HYP with three named inputs:
- (I1) a boost-invariant price;
- (I2) a max-entropy or independence premise, since boost invariance alone also admits Cox processes, thinnings and superpositions;
- (I3) records no longer tied to fixed memory sites, with the order taken from the metric rather than from "latest neighbour record".

Without a derivation of one of these, C4′ is a relabelling, which is failure shape F2. The C4′ one-pager is §6 below.

**C5-8 (lows).**
- **L1:** C4-3's bounds are correct and conservative. The review's estimate is γ(0) ≈ 4.05–4.07 (OBSERVED). The exact constant has no known prior art, so it stays open.
- **L2:** the existence of γ(s) needs a point-to-point variant because of unreachable pairs. C4-4 needs only liminf L/t ≥ |s|. Kingman 1968 (10.1111/j.2517-6161.1968.tb00749.x, verified by the review) is the citation if the limit is kept.
- **L3:** C4-2 is loose. At the front site, L/t ≈ 3.3–3.4 (OBSERVED), so the break is stronger than stated.

**C5-9 (L4): §3 rescore.**
- Draft C as written is uninformative, not "known", so it scores ≈ 0 and should not be run.
- A corrected run (the ratio R(s) plus a sprinkling control) has an outcome already fixed by C4-4 near the cone and already seen at s = 0.5 and 0.9, and it is no longer blind. EIV ≈ 0.97·2 + 0.03·3 ≈ 2.0 over 2.5 h ≈ 0.8 per hour, and it adds nothing beyond a check. **Not recommended.**

**C5-10: labels (as in the review's table).**

| claim | status |
|---|---|
| §1 order = increasing nearest-neighbour paths | PROVED (in-model); brute-force OBSERVED, 0 mismatches |
| C4-1 front speed | PROVED (in-model) as an a.s. limit, v = λa |
| C4-2 L ≥ \|x\| | PROVED (in-model); loose |
| C4-3 γ(0) ∈ [3, 3e] | PROVED (in-model); OBSERVED ≈ 4.05 |
| C4-4 | PROVED (in-model) for flat homogeneous 1+1 with uniform sprinkling; the wider claim needs (i)–(ii) |
| C4-5 | PROVED-sketch |
| Draft C fixed by theorem | **does not hold**: open miss in the Draft C design |
| C4′ | HYP; needs three named inputs (I1–I3) |

## 6. C4′ one-pager: is any cost in the repository boost-invariant, or could it be without a chosen input? (26 Nov 2026, local)
**Costs read** (repository at ac92ee2, read only):
1. **The cost of judgment, `CORE.md:27, 66`.** J = Q̇_M + w·E[ℓ], subject to P(ruin) ≤ ε. Q̇_M is a heat **rate**, with floor kT·İ_M (`CORE.md:70`): a temperature times a learning rate per unit time.
2. **The five-term display, `CORE.md:35`.** κ·I_mem + h·K + w·E[ℓ] + A + L: a price per nat of memory, per layer, per read and per link, plus a stake.
3. **The record-cost J, `theory/RECORD_COST_ROUND10_2026-11-25.md:145–149`.** Gentle transport: c·d² per tick plus κ per affine dimension, over T ticks of the system's own clock. There is no spatial structure.
4. **The clock-term J, `theory/CLOCK_TERM_2026-11-23.md:20`.** κkT·ω′²/D + c·f + w·E[ℓ]: clock heat, looks per unit time, and the stake. These are rates in the world's frame (ω is the world's phase rate).

**Findings:**
- **F-a (heat-rate terms pick a frame).** Terms 1 and 4, and the heat part of the others, are rates per unit time at a temperature T of a bath in a steady state. That is the bath's rest frame.
  - A thermal bath at T > 0 is not boost-invariant. That is standard background, not a repository result, and I cite nothing new for it.
  - The only boost-invariant choice is the vacuum (T = 0 for inertial observers), which sets the heat floor to zero. That choice is itself an input (I1), not a consequence of the cost.
  - **Label:** HYP-level reading of the definitions; no theorem claimed.
- **F-b (count terms are invariant but indifferent).** κ·I_mem, h·K, A per read and L per link are prices per count (nats, layers, reads, links). Counts of events are frame-independent, but these terms do not depend on *where* records sit.
  - Any two placements with the same counts cost the same: **PROVED (in-model)**, by inspection of the definitions.
  - So they cannot choose Poisson over a lattice; they tie. Breaking the tie needs (I2), a max-entropy or independence premise, which is a chosen term.
- **F-c (the frozen corner points the other way).** `CORE.md:78`: a static record in a frozen world costs no ongoing heat after a one-time write.
  - A fixed lattice of memory sites is such a static structure, so the repository's own accounting does not penalise the lattice.
  - Whether a κ-price on stored structure would favour the more random placement depends on whether structure or randomness is priced. The repository fixes neither for placements: **open, HYP.**
- **F-d (where records can sit).** In every model in the repository, records live in fixed parts or memory sites: the parts of a composite, lattice sites in the gravity rounds, and the memory in CORE. No cost term moves a record in spacetime. (I3) is therefore a **model change**, not a parameter the cost could set.

**Result:**
- **No cost in the repository is boost-invariant in a way that acts on record placement.**
  - The heat-rate terms pick the bath frame.
  - The count terms are invariant but indifferent to placement.
  - No model lets the cost place records off fixed sites.
- **Logged as an open miss: "C4′ (cost chooses a Lorentz-compatible record placement) — open miss; would need (I1) a boost-invariant price (in the repository, only by setting the bath to the vacuum and dropping the heat term), (I2) a max-entropy/independence premise, and (I3) records not tied to fixed memory sites, with the order from the metric."**
- None of the three is derived. Each is CHOSEN, which is failure shape F2 again.

**Score (§13 table and scale):**
- The paper miss is now in hand, so what is scored is further work: an attempt to *derive* one of I1–I3 from an existing cost.
- p(a derivation of any one input) ≈ 0.05. This is a judgment: no repository cost even has a spacetime-placement variable.
- V_hit = 8 (the C4 high branch); V_miss = 2 (the inputs are already named).
- EIV = 0.05·8 + 0.95·2 = 2.3, over ≈ 4 h ≈ **0.58 per hour**. Not promoted.
- The open-miss entry itself is done, at a cost of about 0.5 h.
