# Independent hostile review of P15 (REQUIREMENTS_FIRST.md §4 row P15 and §4.1)

*26 Nov 2026, about 18:35 ET. Reviewer did not write P15. Read: REQUIREMENTS_FIRST.md (SHA-256 `1b085838…8446`, unchanged by this review), SR_B.md §1, §8.3, §8.6, §10.5 L2, §11.1–§11.2, SELF_HORIZON.md §7.2, §8.2. Nothing outside `rnd/review_p15/` was edited. No commits, pushes or email. Labels: **PIM** = proved in-model; **OBSERVED** = output of the scripts here; **HYP**; **KNOWN**; **ELEMENTARY**.*

## 0. Outcome in four lines

1. The proof's one geometric step is correct, and the domination holds (PIM, ELEMENTARY). An independent LP check, 25,200 randomized policy comparisons and a cleaner second proof found no counterexample.
2. The **statement is imprecise** in four places: the loss must be the same function for every design; "angle" is an embedding coordinate; the result is weak domination, not selection; and the quadratic cost is not needed.
3. P15 **does not contradict** SR-b3/SR-b4. Their target, "any vertex at operational distance 1", is a design-dependent function of angle (120° for the hexagon, 144° for the pentagon, 180° for the disk), so it lies outside P15's class.
4. The headline wording "positional tracking **selects** the disk" / "position → disk" overstates the result. Ties are common (17% of random instances), and P5's antipode tie is itself a special case of P15. **PASS-WITH-FIXES**.

## 1. Is the statement precise?

As written (§4.1): "loss per tick depends only on the angular difference f(φ_record − θ_t); move cost Σ d_t²; for every polygon policy there is a disk policy with the same loss and no higher move cost; so inf over designs is attained by the disk."

| question | what P15 needs, and what it says |
|---|---|
| Which losses? | Any loss L(φ_record, world, t) that is **one function used for every design**. Rotation invariance f(φ − θ) is **not used** anywhere in the proof, so any dependence on the record's embedded angle works (absolute angle, time-varying, negative-valued, discontinuous). P15 does not state the design-independence requirement, and that requirement is the whole content (see §3). |
| What is "angle" for a polygon state? | A coordinate in the regular embedding: circumradius 1, with the dihedral group acting by rotations. Operationally the polygon is defined only up to affine maps, so the loss is a geometric (embedding) loss, not an operational one. It must be stated. |
| Which paths? | Pure-state jumps (vertices for polygons), staying put allowed, any horizon T. Deterministic or stochastic world, with policies adapted to the world history (the mirror map is pointwise, so adaptedness is preserved). Any starting vertex. |
| Which costs? | The step uses only d_disk ≤ d_poly per step. So the claim holds for **any nondecreasing per-step cost g(d)** with non-negative weight (d, d², √d, d⁴, zero…), not only Σ d². It does **not** cover design-dependent hold costs (keep floor c_K·Γ·ln n, Landauer read ln n, κ per dimension if it differed). P15's scope line already excludes the keep cost; the read cost should be named too. |
| Per-step or total? | **Per step and pointwise per path.** So it holds for the total at every T, under any horizon weighting or mixture, and in expectation under any world distribution. |
| "inf over designs is attained by the disk" | Correct as worded: the disk's value is ≤ every polygon's value, so it equals the inf over the menu. It does **not** say the disk is the *unique* minimiser (§4). |

## 2. Is every proof step valid?

- **Vertices are disk pure states at the same angles.** Valid in the regular embedding (circumradius 1, concentric). Since both sets are taken in that embedding, it is a definition, not a theorem.
- **"Angular loss is identical."** Valid exactly when the loss is one design-independent function of the embedded angle (§1, row 1).
- **d_disk = sin(φ/2).** Valid: the disk has width 2 in every direction, so d = |u − w|/2 = sin(φ/2) (SR_B §1, M3a).
- **d_poly ≥ sin(φ/2) via "width ≤ 2".** Valid: d_K(u, w) = max_θ ⟨u − w, θ⟩ / width_θ(K), and K inside the unit disk gives width ≤ 2, hence d ≥ |u − w|/2. OBSERVED check (`p15_distance.out`): LP-computed distances for regular n = 3…80, every vertex pair, give min(d_poly − d_disk) = −1.4e−15 (rounding). The SR_B §8.6 even-n closed form matches the LP with 0 mismatches. 400 random irregular inscribed polygons also give min ≥ 0.
- **A cleaner proof (PIM, ELEMENTARY; recommended to add).** Every disk effect (affine, with values in [0,1] on the disk) restricted to K ⊆ disk is a K effect. So d_disk(u, w) ≤ d_K(u, w) for all u, w ∈ K. No width computation is needed. It holds for any convex K inside the disk and any pair of points, which is the contractivity of the distinguishability norm under the inclusion map K → disk.
- **The step needs "all effects".** OBSERVED (`p15_distance.out`): the hexagon with one effect pair gives d(v₀, v₁) = 0.25 < sin(π/6) = 0.5, and the polygon then undercuts the disk. SR_B §1 says "all effects", so P15 holds in its class, but P15's own text should repeat the condition.
- **The ∎ conclusion "inf attained by the disk".** Valid, given the above.

**No invalid step found.** The gaps are in the statement's scope and in the wording of its consequence, not in the logic.

## 3. Consistency with earlier proved results

- **SR-b3 / SR-b4 (polygons strictly cheaper than the disk at every T ∈ [2, H]).** Different loss class, so there is no contradiction (PIM; OBSERVED illustration in `p15_boundary.out`).
  - The M3h target is "any vertex at **operational** distance 1 *in that design*". As a function of the embedded angle, that set changes with the design:

    | design | angles of the d = 1 targets from v₀ |
    |---|---|
    | triangle | 120°, 240° |
    | square | 90°, 180°, 270° |
    | pentagon | 144°, 216° |
    | hexagon | 120°, 180°, 240° |
    | 10-gon | 144°, 180°, 216° |
    | disk | 180° only |

    So the M3h loss is not one function of angle across designs, and P15's hypothesis fails.
  - The polygon's win comes from exactly this: its operational geometry makes a closer-in-angle vertex perfectly distinguishable. Hexagon reach cost at T = 2 is 0.5 versus the disk's 1.0 (reproduced).
  - The odd (2T+1)-gon result "under both rules" (SR_B §11) uses the M1 reading of the antipode rule, target v_{S′} at angle π − π/n. That is also design-dependent, so it is outside P15's class.
  - Under the truly positional version, "be at 180°", P15 applies. The output matches: odd polygons cannot reach 180° (cost ∞), and even polygons cost ≥ the disk, for example the 8-gon 0.843 versus the disk 0.75 at T = 3, and the hexagon 0.75 = disk at T = 3 (a tie).
- **SELF_HORIZON §7.2 / P5 (antipode rule: every even polygon ≥ disk, the 4T-gon ties).** This is a **special case of P15**: the antipode target for even n is a positional loss. REQUIREMENTS_FIRST §4.2 item 3 lists "position → disk (P15)" and "antipode → tie (P5)" as different task forms. That is inconsistent. The antipode *is* a position task, and it shows that position tasks give ties, not a strict disk selection.
- **SR_B §11.2 (mixed states → all designs tie at 1/T).** P15 is scoped to pure jumps, so it is consistent. With mixed records the "angle" of a state is undefined, and P15 says nothing there.
- **SR-b1(a)–(f), §8.3.** No conflict. P15 does not use them.
- **Route 1 (REQUIREMENTS_FIRST §7).** Route 1 has no Σd² move cost but has design-dependent keep and read costs (∝ ln n). P15's domination is about the move cost and loss only. With zero move cost it holds trivially, because the disk's action set contains every polygon's. So "the P15 domination statement is the check" is fine as a *check that excluding the disk is a cost-side exclusion*, not a loss-side one. It should be phrased that way.

## 4. Strictness: the main overstatement

- **The claim gives weak domination only** (the text says so in §4.1), but the row title and §4.2 say "selects the disk" and "position → disk".
- **Where steps are strict (PIM, ELEMENTARY, from the width formula):**
  - For odd n the width is < 2 in every direction, so every non-zero step is strictly dearer in the polygon. OBSERVED: no tie on any non-zero step for odd n ≤ 79.
  - For even n, a step ties exactly when the chord is parallel to a vertex direction (k − n/2 even). That is about half of all steps (`p15_distance.out`: 3 of 5 for the hexagon, 11 of 23 for the 24-gon), the antipode included.
- **When is the disk strictly better?**
  - *Sufficient condition (PIM):* g is strictly increasing, the weight is > 0, and every optimal polygon policy makes at least one strictly-dearer step (always true for odd n if it moves at all).
  - It fails whenever the optimal polygon policy stays put, uses only tie chords, or has zero move weight together with a loss the polygon's angles already minimise.
- **OBSERVED** (`p15_dp.out`): 24,000 deterministic-world comparisons (n ∈ {3, 4, 5, 6, 8, 9, 10, 12}; random Fourier, wrapped-square, absolute, miss-indicator, random-step and negative losses; g ∈ {d², d, √d, d⁴, 0}; λ ∈ {0.1, 1, 10}; T ≤ 8) gave 0 violations and 3,986 exact ties (17%). Odd n tied too (1,130 ties, mostly static optima).
- 1,200 Markov-world comparisons with adapted policies gave 0 violations and 85 ties.
- A constructed tie with motion: world alternating 0/π, loss 5·err², cost d², gives disk 4.000 = square 4.000 = hexagon 4.000, pentagon 7.948.
- **So "positional tracking selects the disk" is false as worded. The correct reading is "the disk is never beaten by a polygon on positional losses; ties with even polygons are common" (PIM).**
- Disclosure: the first run of `p15_dp.py` reported "violations". The cause was a bug in the reviewer's own test loss, which redrew a random constant on every call, so the loss was not one function. After the fix there were 0 violations. That bug shows, by accident, the same point as §3: when the loss differs between designs, the domination fails.

## 5. Prior art (DOIs resolved on Crossref this session: `crossref_p15.out`, 8 of 8 OK)

- **The step is a known kind of fact; the instance is ELEMENTARY.**
  - The operational distance is the gauge of K − K. For K ⊆ D, the gauge of K − K is at least the gauge of D − D, which is monotonicity of the Minkowski functional under inclusion. Schneider, *Convex Bodies: The Brunn–Minkowski Theory*, CUP 2013 (2nd ed.), doi 10.1017/CBO9781139003858. A textbook reference for gauges; the specific page was not read.
  - The same fact read operationally: distinguishability does not increase under a valid transformation. The inclusion K → disk is one, because its dual restricts disk effects to K effects. GPT distinguishability measures: Kimura, Nuida & Imai 2010, *Rep. Math. Phys.* 66:175–206, doi 10.1016/S0034-4877(10)00025-X. GPT framework: Barrett 2007, *PRA* 75:032304, doi 10.1103/PhysRevA.75.032304, and Plávala 2023, *Phys. Rep.* 1033:1–64, doi 10.1016/j.physrep.2023.09.001. Contraction of the base or trace norm under positive maps: Reeb, Kastoryano & Wolf 2011, *J. Math. Phys.* 52:082201, doi 10.1063/1.3615729.
  - **Not read this session beyond the Crossref metadata.** They are cited as the places this kind of monotonicity is treated. The two-line proof in §2 does not depend on them.
- **The polygon menu:** Janotta, Gogolin, Barrett & Brunner 2011, *NJP* 13:063024, doi 10.1088/1367-2630/13/6/063024.
- **"A richer action set at no higher cost cannot do worse":** this is ordinary decision-theoretic dominance. An analogy, not a source of the step, is Blackwell 1953, *Ann. Math. Stat.* 24:265–272, doi 10.1214/aoms/1177729032 (comparison of experiments).
- **Rotation-invariant losses, symmetrization, Hunt–Stein-type arguments:** searched for as asked. They are **not relevant**, because the proof uses no invariance of the loss. No source stating P15 itself, for polygon GPTs with transport costs, was found. "Not found" is not "new".
- Also resolved, but not needed: Chiribella, D'Ariano & Perinotti 2011, doi 10.1103/PhysRevA.84.012311.

## 6. Labels after this review

| claim | label |
|---|---|
| For every regular n-gon (all effects, regular embedding), every pure-jump policy, every loss that is one design-independent function of the embedded angle (and world, time), and every nondecreasing per-step move cost with weight ≥ 0: the disk's optimal value ≤ the polygon's | **PIM (ELEMENTARY), independently checked** (this review) |
| Same, for any convex K inside the unit disk with all effects (any states, not only vertices) | PIM (ELEMENTARY), by the effect-restriction proof (§2) |
| Strict on every non-zero step for odd n; strict exactly on edge-normal chords for even n | PIM (ELEMENTARY) + OBSERVED (n ≤ 80) |
| "Positional tracking **selects** the disk" (unique argmin) | **False as worded** (ties: OBSERVED 17%; the antipode/4T-gon tie, PIM) |
| P5 (antipode rule, even n) is a corollary of P15 | PIM (ELEMENTARY) |
| SR-b3/SR-b4 lie outside P15's class (design-dependent target) | PIM (ELEMENTARY) + OBSERVED table |
| P15 fails with restricted effect sets | OBSERVED (one explicit hexagon counterexample) |

## 7. Exact fixes needed (append-only; REQUIREMENTS_FIRST.md was not edited)

1. **Restate the claim** in an appended correction:
   - "In the class of SR_B §1 (pure-state jumps, all effects, regular polygons in the regular embedding, plus the disk), for any loss that is **one design-independent function** of the record's embedded angle (and of the world and time) …";
   - "… and any nondecreasing per-step move cost (quadratic not needed) …";
   - "… with no design-dependent hold costs (keep, read, per-dimension price) …";
   - "… the disk's optimal value is ≤ every polygon's, per step and per path, hence for any horizon, weighting or world distribution."
2. **Replace "selects the disk" with "is never beaten by a polygon (weak domination; ties occur)"** in the P15 row, §4.2 item 3, the §8 labels table, and every summary. The parent's chat line to Chad ("position scoring gives the disk") needs the same correction: "on position scoring the disk is never worse than a polygon; even polygons often tie it."
3. **Merge P5 into P15.** "Antipode → tie" is a positional task, so it is an instance of P15's weak domination, not a separate task form. In §4.2 item 3, write "position (including the antipode) → the disk, weakly; operational reach → polygon (P14)".
4. **Add the non-contradiction sentence:** SR-b3/SR-b4 and the odd (2T+1)-gon use an operational, design-dependent target (angles 120°/144°/180°… depending on the design), so P15's hypothesis fails there. The split is **geometric (embedding) loss versus operational loss**, not "position versus distinguishability" in general.
5. **Add the strictness corollary** (odd n strict on every move; even n strict only on edge-normal chords) or keep "strictness not claimed". Either way, drop the unique-selection reading.
6. **Name "all effects" in P15's own text.** With restricted effects the step fails (hexagon example).
7. **Optional:** add the effect-restriction proof (two lines, any K ⊆ disk) and credit the monotonicity-under-inclusion idea (Schneider 2013; GPT distinguishability literature above) as KNOWN in kind, with the instance ELEMENTARY.
8. **Route 3** (mixed α·position + (1 − α)·reach): its pre-statement must say how ties count at α = 1, because there the disk is only weakly best. Otherwise "the disk above α*" can't be scored. **Route 1:** phrase P15's role as "the disk's exclusion is cost-side (keep/read), not loss-side".

## 8. Files

`p15_core.py` (LP operational distance), `p15_distance.py/.out` (step check, ties, irregular polygons, restricted-effects probe), `p15_dp.py/.out` (24,000 + 1,200 policy comparisons), `p15_boundary.py/.out` (the SR-b3/SR-b4 class boundary), `crossref_p15.py/.out` and `crossref_p15_search.out` (DOI checks).

## Outcome: **PASS-WITH-FIXES**

The mathematics holds (PIM, ELEMENTARY, now independently checked). The fixes are scope and wording: the design-independent loss, weak domination rather than selection, P5 as a special case, the operational-versus-geometric split as the reason for no conflict with SR-b4, and "all effects" named. Fixes 1–4 are required before P15 is quoted outside the notes.
