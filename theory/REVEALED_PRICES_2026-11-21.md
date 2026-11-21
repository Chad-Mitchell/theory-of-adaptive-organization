# Revealed prices: what a fair test of the law actually requires (21 November 2026)

*Saturday 21 November 2026, written about 9:00–10:00 AM ET (America/New_York), beside `main` `a65b64e` (through PR #132). Not a lock, not a prereg, not a result, and not a change to the kill rule: §8 **proposes** a dated amendment and leaves the canonical wording untouched until it is reviewed and adopted. The hypothesis sentence is unchanged: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." Line numbers cite `THEORY.md` at `a65b64e` unless another file is named. "Proved" means proved in a model, which is not a claim about nature.*

## 0. What is already in the repository (not presented as new)

- **Revealed costs are already allowed in one sentence.** THEORY line 153: "Prices can also be inferred from an observed design (revealed costs), a test and not a circle only when observed features outnumber the free price ratios: several exogenous drift levels, several items under one clock, or one technology across layers."
- **Only price ratios matter.** CT24 (optimal cost shares are currency-free); THEORY line 43 ("only dimensionless ratios matter"); `theory/PRICE_FREE_2026-11-21.md` §1 (price-free, price-ratio-only and absolute-price bins).
- **Layers are linked.** CT34 (line 472): a team's optimized cost enters the parent exactly as upkeep when the parent sees it only through quantities fixed before the team optimizes, with a second-order error bound when coupling is weak and a counterexample when the driver is shared.
- **Selection band.** §3 (c), line 48: ε = 10/(σN_e), crediting the drift barrier (Lynch et al. 2016). PF17 in `PRICE_FREE` and `core/bridge_2026-11-21/SELECTION.md`: typical fractional excess ≈ d/(2σN_e) (Sella & Hirsh 2005 applied to J). Its official in-model test T27 **FAILED** on P3 (PR #122; an ill-posed gate, see `history/2026-11-21_NIGHT.md`).
- **Overidentification has been used once.** `tests/SPF_NOISE_PROXY/PREREG.md` item 3 (a horizon-overidentification statistic).
- **The holographic reading tested so far** is T20 (`reviews/t20_2026-11-20/REVIEW.md`): the "layer count grows with the log of the scale range" part (A) passed 12/12 primary gates; the "where each layer's rate sits" part (B) failed 0/12. That was the surface analogy, not the boundary argument in §5 below.
- **The obstacle.** `OPEN_WORK.md` §8: sourcing fitness-unit prices (h, w) independently may be the binding obstacle for most field tests. T30 (`history/2026-11-21_NIGHT.md`) proposed experimenter-set prices as a way round it.

What this note adds is narrower than a new idea: it says that the requirement behind the obstacle is not needed for a fair test, states what is needed instead, gives a counting rule that uses CT34 to cut the number of free prices, and proposes the wording change. The method is standard (§6).

## 1. Diagnosis: which requirement stalled the field tests

Every field attempt from 18 to 21 November (E. coli, the grids, VIS-1F, the shortlist) stopped at the same gate: prices measured **independently of the design, in fitness units**. The gate is written in four places: THEORY line 53 item (1), line 111 (Rule 7), line 159 (the killing test), and `measurement/FRAMEWORK.md` §9 item 2 ("price each independently of the design predicted (no price fitted to the design)"); `CORE.md` §2 says the principle "predicts only through price-free structure or independently measured prices". Line 153 permits the opposite, and nothing reconciles the two.

Two facts show the gate asks for more than the comparison needs.

1. **Units drop out of the comparison.** For any c > 0, argmin_𝒟 c·J(𝒟) = argmin_𝒟 J(𝒟). The design the law predicts depends on price *ratios* only (CT24). Fitness units, a common currency across scales and an absolute scale for prices therefore play no part in the comparison of an observed design with argmin J. (The ruin constraint is also in ratios: the reserve B and income y are measured in the same currency as J.)
2. **Fitness units enter in one place only:** the absolute qualification band ε = 10/(σN_e), where σ maps a fractional change in J to a fractional change in fitness. That is a statement about *how close* selection can push a design, not about *where* the optimum is. §4 offers an ordinal substitute.

So the absolute-price demand came from merging two different jobs (locating the optimum; saying how close selection should get) into one gate.

## 2. The four requirements of a fair test

A test of the law in a system is fair when all four hold, each fixed in writing before the scored data are seen.

| | Requirement | Why it is needed | How it is checked |
|---|---|---|---|
| R1 | **Locked first.** The prediction, the fitting procedure, the split, the scoring rule and the pass and fail thresholds are hash-locked before the scored data are opened. | Otherwise the test can be steered. | Existing practice: prereg, hash-lock of runner and library, exact gate values computed on pilots before locking (T27 lesson), DEVIATIONS files, no patching. |
| R2 | **Can fail.** Some outcome that the data could show is excluded by the prediction at every admissible price. | Otherwise any data fit. | The **reachable-set check** (§3.3), computed before data. |
| R3 | **Differs from a named rival.** The prediction and a preregistered rival, each fitted the same way on the same fit set, give different held-out predictions by more than the error budget. | Otherwise a pass supports the rival as much as the law. Generic cost-benefit optimizers (for example Dekel & Alon's) are rivals of this kind when the law's prediction is the same as theirs. | Rival list fixed before data, at least one of FRAMEWORK §9 item 6 (R1 fixed share; R2 exponent ½; R3 set-at) plus the most specific prior-art model for the system. Separation computed on pilots. |
| R4 | **Prices fitted off the scored data.** Any price ratio that is not measured is fitted on data disjoint from the data that score the prediction. | Fitting and scoring on the same numbers is the circle line 153 warns about. | The split is part of the lock; fitted values are written down before the held-out data are opened. |

**Dropped, as not required for a fair test:** prices in fitness units; a common currency across scales; independent measurement of every price; costs set by an experimenter (Avida and similar platforms are one way to meet R4, not a requirement); absolute qualification as a precondition for *support* (it remains a precondition for a *kill*; §8). Independent measurement of a price is still welcome: a measured price simply removes one free ratio from the count in §3.

## 3. Identification: the counting rule

### 3.1 The count

Before data, the prereg states:

- **n_fit**: the number of independent design observables in the fit set (one observable = one design feature, such as a read interval, a memory, a layer count, in one exogenous condition or one item);
- **n_score**: the number in the scored (held-out) set;
- **p**: the number of free quantities fitted from design data: price ratios **after** CT34 linking (§3.2) and after removing any ratio measured independently, plus every nuisance quantity (noise, exponent, offset) that is fitted from design data rather than measured from the world.

The test is valid only if **n_fit ≥ p** (the fitted quantities are identified from the fit set) and **n_score ≥ 1**; its overidentifying degrees of freedom are **n_fit + n_score − p**, and only the n_score held-out observables are scored. A quantity added after data is opened counts as a miss, as an unlisted cost already does (line 53). This is the overidentification logic of instrumental-variable and moment estimation (Sargan 1958; Hansen 1982) applied to argmin J; a held-out split is used instead of a pooled J-statistic so that R4 is visible.

### 3.2 Linking cuts p (CT34)

Unlinked, a design with K layers has up to two free ratios per layer (an upkeep and a stake), so p grows with K. CT34 (i)–(ii) removes most of them where it applies: the parent's problem is F(x) + J\*_T(θ(x)), so the upkeep of a child layer is the child's own optimized cost, and the child's stake and noise are what the parent passes down. Composing partial minimization level by level (by induction on CT34 (i)), the free prices of an exactly nested system are those at its **edges**: the unit prices of the bottom layer (read, hold, link) in its own currency, the stake at the top (set by what ruin or selection costs the whole), and the world's spectrum, which is measured, not fitted. Then p is the number of bottom unit-price ratios plus one, whatever K is.

This holds only where CT34's exactness or weak-coupling bound holds. A shared driver breaks it (CT34 (iv)); layers with their own interests break it (CX2); in both cases the prereg must count the unlinked prices. Whether a real nest satisfies CT34 is not shown (CT34, "Not shown").

### 3.3 Reachable-set check (R2) and rival separation (R3), before data

On a pilot or on the design's admissible ranges, compute the set of held-out outcomes the law can produce for **any** admissible value of the fitted quantities (fitted on any admissible fit-set outcome). The test is valid only if that set excludes a preregistered share of the outcome range, and the rival's best-fit held-out prediction lies outside the law's prediction interval (and the reverse). If prices can go to a degenerate value (for example w → 0, which rationalizes doing nothing), the admissible set must exclude it in advance; this is the inverse-reinforcement-learning degeneracy (Ng & Russell 2000), and the reason R2 is a computed check, not a promise.

### 3.4 A worked count (CT12)

For exact reset reads of a self-similar world (CT12; PF7), T\* = [α c / ((α − 1) w q)]^{1/α}. One reader with one read technology looking at m items with independently measured drift q_i and common α has p = 1 (the ratio c/w). Fit c/w on one item; predict ln T\*\_j for the other m − 1 items, level and slope: ln T\*\_j − ln T\*\_i = −(1/α)·ln(q_j/q_i). Overidentifying degrees of freedom m − 1. Rival R2 (exponent ½) has the same p = 1 and differs only when α ≠ 2, so R3 requires a world with α measured away from 2 by more than its error. With two read technologies p = 2, and with items read at different stakes but one technology p stays 1 if the stakes are measured, 2 if not.

The worked count shows the general point: the revealed-price route does not create distinctiveness. It turns a distinctive price-free relation (PF2, PF7, PF10, PF6; `PRICE_FREE` §4) into a sharper test, because the *level* is predicted as well as the slope. Where the law's prediction coincides with generic optimization, revealed prices make the test fair but not discriminating.

## 4. The selection-gradient test (an ordinal substitute for the absolute band)

PF17 says the typical fractional excess of J over its minimum is about d/(2σN_e). Its testable, unit-free content is ordinal: **among members of one class in comparable worlds, the held-out gap from the fitted optimum falls as selection strength rises.**

Protocol: before data, fix (a) the members, (b) an ordinal ranking of selection strength from a source independent of the design (for example N_e from neutral diversity, competitors per niche, generations or redesign cycles under the same world), (c) the gap measure (held-out |ln design − ln predicted design|, or the J-excess where J is computable), with prices fitted under §3 on data disjoint from the scored gap, and (d) a one-sided trend test with its threshold. Ranks are never reassigned after a miss. A power check is part of the lock: if the ranked members span too little selection strength for the predicted trend to exceed noise, the test is NOT A TEST.

Three cautions. (1) The ordinal logic is the drift-barrier and nearly-neutral argument (Ohta 1973; Lynch et al. 2016; for mutation rate, Sung et al. 2012), and the Boltzmann form is Sella & Hirsh 2005; what is specific to this repository is only that the quantity is J. A gradient found in a trait that is not a judgment design is evidence for those theories, not for this one. (2) T27 P3 failed in-model, so the constant in d/(2σN_e) is not relied on; only the direction is. (3) Stronger selection can correlate with a different world; the gap must be measured against each member's own fitted optimum, not a shared one.

## 5. The recursion and the boundary ("holographic") reading

Read carefully, CT34 says each layer is an agent solving the same problem with its own currency: its upkeep is the optimized cost of what it runs, and its stakes are what its parent loses when it is wrong. Then:

- **Cost is relative to the layer.** Each layer's J is in its own units (heat for a cell, attention for an animal, money for a firm); the child's optimized cost, expressed in the parent's units, is the exchange rate between neighbours. Energy is needed only at the bottom edge (the Landauer and Still floors), and above the cell that floor is slack (line 11), so carrying thermodynamics through every layer would add no predictive content where it is slack.
- **The edges fix the interior.** In an exactly nested system the interior prices are not free (§3.2): bottom unit prices, top stake and the side input (the world's spectrum) determine every layer's optimum by dynamic programming. That is a boundary-value structure.
- **What this is not.** The holographic principle in physics ('t Hooft 1993, arXiv gr-qc/9310026, no DOI; Susskind 1995) bounds the degrees of freedom of a region by its boundary area. The statement here is the ordinary one that partial minimization composes (Bellman; Dantzig & Wolfe 1960; Geoffrion 1970, already credited at CT34). It is an analogy to holography, useful because it says where to look for free parameters, not a physical claim. West, Brown & Enquist (1997) is a prior example of the same shape in biology: an invariant terminal unit (bottom edge) plus network optimization fixes interior scaling.
- **Where it breaks.** When layers have their own interests (CX2) or share a driver (CT34 (iv)), the interior is not fixed by the edges and the count reverts to unlinked prices. This is also where the theory says ants and firms differ.

## 6. Prior art (DOIs checked on Crossref this session unless noted)

- Revealed preference: Samuelson 1938, *Economica* 5:61, doi 10.2307/2548836; Samuelson 1948, *Economica* 15:243, doi 10.2307/2549561; Afriat 1967, *Int. Econ. Rev.* 8:67, doi 10.2307/2525382; Varian 1982, *Econometrica* 50:945, doi 10.2307/1912771 (nonparametric tests that a choice set can be rationalized at all: the R2 of revealed preference).
- Inverse optimization and inverse optimal control: Ahuja & Orlin 2001, *Oper. Res.* 49:771, doi 10.1287/opre.49.5.771.10607; Kalman 1964, *J. Basic Eng.* 86:51, doi 10.1115/1.3653115. Inverse reinforcement learning: Ng & Russell 2000, ICML proceedings (no DOI; credited by title, not Crossref-checked).
- Structural estimation: Rust 1987, *Econometrica* 55:999, doi 10.2307/1911259. Overidentification tests: Sargan 1958, *Econometrica* 26:393, doi 10.2307/1907619; Hansen 1982, *Econometrica* 50:1029, doi 10.2307/1912775.
- Selection gradient: Ohta 1973, *Nature* 246:96, doi 10.1038/246096a0; Sung et al. 2012, *PNAS* 109:18488, doi 10.1073/pnas.1216223109; Lynch et al. 2016, *Nat. Rev. Genet.*, doi 10.1038/nrg.2016.104; Sella & Hirsh 2005, *PNAS* 102:9541, doi 10.1073/pnas.0501865102.
- Cross-level structure: West, Brown & Enquist 1997, *Science* 276:122, doi 10.1126/science.276.5309.122. Holography: Susskind 1995, *J. Math. Phys.* 36:6377, doi 10.1063/1.531249.

None of the method is new. The application to J, the CT34-based count (§3.2) and the ordinal gate (§4) are this repository's; whether they are new was not surveyed beyond the items above.

## 7. What this cannot show

- A pass shows that **some** admissible prices rationalize the design and predict held-out designs; it does not show those prices are the system's true ones.
- A pass where the law's prediction equals a generic optimizer's (Dekel & Alon-type cost-benefit, the classic sampling model, Kalman–Wiener) supports optimization in general, not this theory (R3).
- It does not establish qualification. A held-out miss in a system not shown to be strongly selected is not a kill (§8).
- Linked counting (§3.2) is only as good as CT34's premises in the system; nothing here shows real nests satisfy them.
- It does not supply data. §9 records that no public dataset found today meets R1–R4 with a distinctive prediction.

## 8. Proposed amendment (dated 21 November 2026; not applied)

Hypothesis sentence untouched. Proposed replacements, to be applied only after review and adoption:

1. THEORY line 53, item (1): "… and the prices, each measured independently of the design they predict, …" → "… and the prices, each either measured independently of the design they predict or revealed from a disjoint part of the observed design under the counting rule of `theory/REVEALED_PRICES_2026-11-21.md` (more scored observables than free price ratios after CT34 linking, counted before data), …". The same change at line 111 ("with inputs measured independently of the design" → "… measured independently of the design, or revealed under that rule") and line 159 ("measure … the prices, independently of the design" → "… the prices, independently of the design or revealed under that rule").
2. `measurement/FRAMEWORK.md` §9 item 2: "(no price fitted to the design)" → "(no price fitted to the **scored** design; prices revealed from a disjoint fit set are allowed under the counting rule of `theory/REVEALED_PRICES_2026-11-21.md`)". Item 3 likewise.
3. `CORE.md` §2: "predicts only through price-free structure or independently measured prices" → "… price-free structure, independently measured prices, or prices revealed on held-out-disjoint data and overidentified".
4. Qualification, added as an alternative for **support and for counting against**, not for a kill: a preregistered selection-gradient test (§4) may stand in for the absolute band ε = 10/(σN_e). A kill still requires the absolute qualification of §3, because a single miss in a weakly selected member is expected.

## 9. Dataset search (task B) and decision (task C)

Searched this session for public, no-account data in which one system class shows its design under several exogenous conditions, ideally with a selection ranking. Assessed against R1–R4, the count, and distinctiveness (`PRICE_FREE` §4).

| Candidate | Data | Count | R3 (distinctive?) | Verdict |
|---|---|---|---|---|
| Bumblebee sampling under 4 persistence × 3 error-cost levels (Dunlap, Papaj & Dornhaus 2017, *Interface Focus*, doi 10.1098/rsfs.2016.0149; data figshare doi 10.6084/m9.figshare.4769539, DataCite, resolves) | Open | 12 cells, ≤ 2 free ratios (error costs are set in sugar units) | **No.** A two-state switching world, where the law's optimum is the classic sampling model the authors already tested; their finding (sampling rises with change rate; tracking often suboptimal) would be reproduced, not discriminated. A lab task outside the bees' evolved world; no selection ranking | Best-formed, not discriminating |
| Mutation rate against N_e (Sung et al. 2012; Lynch et al. 2016 tables) | Open (PMC supplements) | Many species | **No.** It is the drift-barrier hypothesis itself; N_e is estimated as π_s / (k·u), which shares u with the design (Sung et al. discuss the induced correlation), so R4 is weak too | Prior art for §4, not a test |
| Tetrahymena genotypes across thermal-fluctuation periods (Dryad doi 10.5061/dryad.z612jm6k7) | Open | 15 genotypes × periods | **No.** Observes growth (an outcome), not a design feature per condition | Not a test |
| Chipmunks sampling renewing patches (Hall, Humphries & Kramer 2007, *Can. J. Zool.*, doi 10.1139/Z07-030) | No public deposit found in this search | — | Sampling did not track renewal rate, a potential miss, but world spectrum not measured and no public data | Not usable |
| Wolf territory revisits (Dryad doi 10.5061/dryad.2j125) | Open | 6 animals | World's drift spectrum (scent decay, prey) not measured; p exceeds n_fit | Not identified |

Earlier candidates (E. coli, grids, VIS-1F, SPF, InventoryBench, Beekman and Dornhaus) are assessed in `PRICE_FREE` §3 and `DISCRIMINATING_CANDIDATES`; the change of rule does not rescue them, because their blocker was distinctiveness or an unmeasured world, not only absolute prices (see `theory/VIS1F_DROP_2026-11-21.md` for VIS-1F's second blocker, L3).

**Decision: no candidate qualifies, so nothing is locked or run.** The binding constraint is now R3 together with a measured world, not prices. **The single dataset that would qualify:** one strongly selected reader (or a set of readers ranked by selection strength in advance) whose read intervals are observed on at least three items or conditions whose drift is measured independently and is self-similar with α measured away from 2 (ideally two distinct α); one read technology across items (p = 1); a second design feature on the same items (a memory or smoothing time) for a cross-feature overidentifying check. Fit c/w on one item, predict the rest, rivals R2 (½) and R3 (set-at). Plausible sources: pollinator trapline revisit intervals to plants with measured nectar-secretion autocorrelation; animal patrol or scent-mark renewal intervals with measured decay; or the N51 lab task, which meets R1–R4 but not qualification.

## 10. Effect on the odds

None. This note removes an assumed requirement and states a fair-test standard; it adds no evidence. It also makes two things clearer that cut against novelty, not truth: the revealed-price method is standard, and the selection-gradient test is the drift-barrier argument applied to J.
