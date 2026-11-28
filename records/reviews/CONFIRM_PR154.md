# Confirm review of draft PR #154

**Verdict: CONFIRMED-WITH-NITS**

**Head reviewed:** `45140779553ca6df8a2d572f9cec6f47059c30e3` on `representation-2026-11-21`.
**Base used for the sentence check:** `d1a6de4`.
**Blockers:** none.
**Nits:** five, listed at the end. None of them falsifies a status row or a recomputed number.

This review reads the files at that head. It does not treat `reviews/representation_2026-11-21/REVIEW.md`, or any earlier confirm, as authority. `lake build` was not run.

## What was checked, and what holds

### V1, narrowed, is what is proved

`theory/REPRESENTATION.md` §0 and §3, the status table in §9, and CLAIM_MAP row V1 state the same narrowed theorem, and the proof matches that statement.

- Nonnegative prices are not a consequence of A1–A7. A8 (each concatenating coordinate is a bad) is a separate axiom. Lemma M is the sign step, and it is invoked only after A8 (`REPRESENTATION.md` §2, §3 step 3). A price of either sign is still linear once the Cauchy equation is solved.
- Debreu is applied only to a product of intervals, at least three of them essential, with upper and lower contour sets closed in the product topology (`REPRESENTATION.md` §1 A3, §3). The two-coordinate case is explicitly not claimed, because the Thomsen condition is not assumed.
- Layer count is not a Debreu factor. Lemma C_ℤ gives `f(K) = hK` on the nonnegative integers from `f(m+n) = f(m)+f(n)` alone (`f(0) = 0`, then induction). Putting `hK` into the same sum is named as an extra preferential-independence assumption, and the note says the cited theorem does not prove the mixed product (`REPRESENTATION.md` §3, lines 92 and 110).

Row V1 is **PROVED (in-model)** for that statement. CORE.md and THEORY.md §3 say the same thing: the interval product forces an additive cost up to one positive affine map; nonnegative prices need the further bad-coordinate assumption; discrete `K` is outside the cited theorem.

The affine arithmetic in §4 was recomputed independently. With `β = 2`, `d = 1`, `a = 3`, `b = 5`, `J* = 4`: absolute excess of `J` is `0.25 = d/(2β)`; excess of `aJ+b` is `0.75`, which equals `d/(2β)` only at scale 1. The fraction is `0.0625` at `b = 0` and `0.04412` at `b = 5`. That matches §4.

### V2, narrowed, is what is proved

Row V2 and §5 claim that Kelly growth and the Lundberg objective have different argmins from expected currency cost, so the four verbs do not force `J`. They do not claim a one-axiom witness for each of A1–A8. F1, CT34, CT36, S4, `c·r+wD`, and F3 are reclassified as staying inside an additive cost or dropping more than one clause. Still is stated as dropping the information choice and separability together.

Independent recomputation, not by importing `binding_multiplier.py`:

| Quantity | Claim | Recomputation |
|---|---|---|
| Kelly weight | `q* = 0.26` | `β a₁/(a₁−b₁) = 0.05×1.30/(1.30−1.05) = 13/50 = 0.26` exactly. First derivative of `G(q) = β ln(q b₀) + (1−β) ln(q b₁+(1−q)a₁)` is `0` at `0.26` and changes sign there. A grid on `(0,1)` maximizes at `0.26`. `G(0.26) = 0.12790` (DYNAMICS rounds this to `0.128`). |
| Per-unit means | `1.235` and `1.0425` | Lean, shock factor 0: `(1−0.05)×1.30 = 247/200 = 1.235`. Robust: `0.95×1.05 + 0.05×0.90 = 417/400 = 1.0425`. Lean wins the linear expectation; Kelly's argmax is interior. |
| Lundberg vs expected cost | `τ_S = 0.2362`, `τ_E = 0.3162` | On `y=1`, `c=0.05`, `w=σ=1`, `s₀=0.3`, `α=1/2`, `β=1/3`: `τ_E = √(c/α) = √0.1 = 0.316227766`. The unique zero of `θ'` on `{m>0}` is `τ_S = 0.236207527`. Both round to the printed four decimals. One sign change of `θ'` on a 2000-point grid. `φ' < 0` on that grid (maximum about `−0.036`). |

The lean shock factor of 0, which the representation note does not restate, is the hypothesis of the CT42 formula it cites (`theory/DYNAMICS.md`). The displayed product `0.95×1.30` uses it. The formula does not depend on `b₀` as long as `b₀>0`.

### Section 7

- **Attained scores.** F-0 assumes `Z₀(W)` is compact (the image of a nonempty compact design set, and then asserted compact). On a nonempty compact set the continuous sum of coordinates attains its minimum, and a minimizer of the sum is Pareto: a distinct coordinatewise-smaller score would have a strictly smaller sum. That argument is correct given compactness. See nit 4 for the missing continuity hypothesis in the first sentence of F-0.
- **Free disposal is a different set.** `Z = Z₀ + ℝ₊⁵` is closed when `Z₀` is compact, and it is unbounded. In `ℝ⁵` no nonempty set is both compact and closed under adding an arbitrary positive increment. So the hull is not `Z₀`. Existence of a Pareto point is charged to F-0, not to compactness of the hull. The note says this.
- **F3.** `J_s = ½(x−θ)²` and `J_w = ½(θ−gx)²` (`theory/COADAPTATION.md`). Both are 0 at `(x,θ)=(0,0)` and nonnegative everywhere, so the origin dominates every other cost vector and is Pareto. A grid for `g=2.5` found no other undominated score. The potential's saddle for `g>1` is a different fact, and the note treats it as one.
- **Coordinate cap.** If `Z` is convex and `ρ` is a coordinate, `Z ∩ {ρ ≤ ε}` is an intersection of convex sets, hence convex. On the CT22 path, strict unimodality makes `{θ ≥ θ_req}` a closed interval (one zero of `θ'`, `φ'<0`), so that cap preserves convexity too.
- **A nonconvex surviving set can break it.** Explicit example, not in the note: uncapped scores the closed unit disk (convex). Keep a point only when `xy ≥ 0.3`. Then `(0.6,0.6)` and `(−0.6,−0.6)` survive (`0.6²+0.6²=0.72≤1`, product `0.36`), and their midpoint `(0,0)` is in the disk and does not survive. The surviving score set is not convex. A cap on one coordinate of a convex score set does not do this. The note's distinction holds.
- **V5** is **OPEN** in §9 and in row V5. Hypothesis F is not stated as a conclusion and does not replace the Part 2 sentence.
- **V6** is **PROVED (in-model)** for the scope list that is actually proved: the front is antitone by definition; positive-price weighted sums land on the front without convexity (F1(i)); a convex free-disposal set has every Pareto point as a nonnegative weighted-sum minimum (separating hyperplane, F1(ii)); without convexity the three-point dent is Pareto and is the minimum of no nonnegative weight. V6 does not say a selected system sits on the five-bad front. That is V5, and it stays open.

### Dent, 4/9, all nonnegative weights

`A=(0,1)`, `B=(1,0)`, `C=(0.6,0.6)`. For `p₁>0`, `p₂>0`:

- `⟨p,C⟩ ≤ ⟨p,A⟩` rearranges to `0.6 p₁ ≤ 0.4 p₂`, so `p₁/p₂ ≤ 2/3`.
- `⟨p,C⟩ ≤ ⟨p,B⟩` rearranges to `p₂/p₁ ≤ 2/3`.

The product of the two bounds is `(2/3)×(2/3) = 4/9 < 1`, which is impossible. On an axis, `p=(0,1)` gives scores `(1, 0, 0.6)` and `B` wins; `p=(1,0)` gives `(0, 1, 0.6)` and `A` wins. So `C` minimizes `⟨p,·⟩` for no `p ≥ 0`, `p ≠ 0`. The mixture `(0.5,0.5)` dominates `C`. A direct check of 15,007 nonnegative weights (the unit simplex at spacing `10⁻⁴`, the two axes, and 5,000 random positive pairs up to `10⁶`) found no weight that makes `C` a minimizer. `frontier_scalarization` in `binding_multiplier.py` records the `4/9` identity, and `tools/test_representation_checks.py` checks 21 rays of the simplex including both axes.

### Constraint qualification at B = 0.49, 0.50, 0.505

Independent bisection on the diffusion formulas, `ε_r = 10⁻³`:

| B | τ* | θ'(τ*) | binding? |
|---|---|---|---|
| 0.49 | 0.267416 | −6.326936 | yes, θ' ≠ 0 |
| 0.50 | 0.299050 | −11.29607 | yes, θ' ≠ 0 |
| 0.505 | 0.310392 | −12.80299 | yes, θ' ≠ 0 |

`B_min = 0.486441`, `B_slack = 0.507853`, so all three buffers are strictly between the endpoints. `μ(0.5) = 0.005231`, which rounds to the published `0.0052`. `dJ*/dB` at `B=0.5` is `−0.144543`, which rounds to the `−0.145` in `theory/MASTER_EQUATION.md`. The script's loop is `(0.49, 0.50, 0.505)` and its PASS lines give these same derivatives. See nit 5 for the printed label of the third point.

## Cited theorems, against their hypotheses

**Debreu 1960** ("Topological methods in cardinal utility theory"; reprint doi `10.1017/ccol052123736x.010`). The additive theorem needs a product of connected separable spaces, a complete preorder with closed contour sets, preferential independence for every subset of coordinates, and at least three essential factors. Intervals are connected and separable. The note uses exactly that list, keeps the common positive scale and the per-coordinate constants, and does not apply the theorem to a discrete factor or to fewer than three essential intervals. Debreu 1954 is the ordinal representation theorem (a continuous complete preorder on a second-countable space has a continuous utility; the product of intervals is second countable, and closed contour sets are the continuity hypothesis). The note does not cite 1954 for the additive step. The cited work is the 1960 essay. Crossref `issued` for the reprint is `[[null]]`, which is what the note means by an empty year field. Title matches. The author array is Debreu, Debreu, and Hildenbrand; Debreu is the author of the essay.

**Aczél, Forte, and Ng 1974** (doi `10.2307/1426210`). Symmetry, expansibility, additivity, and subadditivity characterize nonnegative linear combinations of Shannon and Hartley entropy. The same postulates plus continuity for `n=2` isolate Shannon up to a positive factor (Csiszár 2008, doi `10.3390/e10030261`, the survey the note cites). Step 4 of the proof uses the finite-law conclusion that is actually true: the memory coordinate is Shannon mutual information in nats, the positive constant sits in `κ`, and a Gaussian differential mutual information is named as an extension rather than a corollary. The gloss of the four axioms is wider than the theorem. See nit 2. Faddeev's grouping axiom is a different characterization (recursivity, 3-symmetry, and continuity). It does isolate Shannon, but it is not the extra hypothesis in the Aczél–Forte–Ng paper, and grouping without continuity is not enough.

**Pexider.** Lemma P is the specialization `f(x+y) = f(x)+f(y)+c`. Setting `g = f+c` reduces it to Cauchy's equation, and the algebra checks. Lemma C proves the monotone case in both directions on `(0,∞)`, which covers a negative price (the cost component is nonincreasing). A5's "no capacity ceiling" is what keeps sums inside the domain. The continuous, non-monotone route is asserted rather than written. See nit 3.

**Lundberg.** On Brownian motion with drift `m>0` and variance rate `s²`, the adjustment coefficient is `θ = 2m/s²`, and the ruin probability is `e^{−θu}`. The note maximizes that certificate on the published diffusion path, on `{m>0}`. It does not claim that the classical compound-Poisson Lundberg equation reduces to `2m/s²` for a general claim size. THEORY B.9 states that "infeasible" means not certified by the bound. The two argmins differ, as recomputed above.

**Kelly 1956** (doi `10.1002/j.1538-7305.1956.tb03809.x`, title "A New Interpretation of Information Rate"). Kelly maximizes expected log growth. CT42's lineage growth `G` is that criterion. The number `0.26` is CT42's mixture under a shared shock that wipes out the lean design, not a formula from the 1956 paper. The note attributes the criterion to Kelly and the number to CT42. That is the right split. Log utility is a von Neumann–Morgenstern index and is not risk-neutral expected currency. The argmins differ.

**Still, Sivak, Bell, and Crooks 2012** (doi `10.1103/PhysRevLett.109.120604`, "Thermodynamics of Prediction"). Under their hypotheses (no feedback onto the signal, discrete-time Markov relaxation, a heat bath, dissipation defined with their nonequilibrium free energy), the per-step identity is `β⟨W_diss⟩ = I[s_t;x_t] − I[s_t;x_{t+1}]`. An independent rerun of the two-state enumeration in `theory/theorems-checks/check_all.py` (`β=1`, `ε=1.5`, flip `0.1`, `κ=0.4`, 40 steps) has maximum absolute gap `3.6×10⁻¹⁶`, inside six decimals. The functional is not `κ I_mem`. The note's "under their hypotheses" points at T6, which states the no-feedback condition and the factor `β`.

**Other DOIs in §10.** All 24 were resolved on the Crossref API on this review. Titles match the works named in the note, including Farrell 1957, Debreu 1951 (Econometrica 19:273, page field `273`, volume `19`), Shoval et al. 2012 (the nine authors named in the note, title "Evolutionary Trade-Offs, Pareto Optimality, and the Geometry of Phenotype Space"), and the Shannon IEEE reprint (2009, author list empty, as the note says). von Neumann and Morgenstern resolve to the 2007 commemorative edition, which the note discloses.

## Status labels

Rows V1, V2, V3, and V6 are **PROVED (in-model)**. Rows V4 and V5 are **OPEN**. CT22 stays **PROVED (in-model)** and the row text now limits the claim to the scalar diffusion path, with constraint qualification `θ' ≠ 0` off the survival endpoint. That matches THEORY B.9. V3 restates the already-proved scopes of CT33 (any `S+wE` on a stake-independent menu), CT24 (price-independent feasible set), CT20(ii) (sensing fixed, ruin slack), and CT1 (a bound, not a priced minimizer). It does not add an inequality. The tally arithmetic 114→118 proved, 89→91 open, 357→363 is what `check_consistency.py` recomputes (363 rows, 0 mismatches).

The status column does not overstate the repaired theorems. The version-note preamble does, and then retracts it. See nit 1.

## Hypothesis sentence

Byte-identical to `d1a6de4`, one copy each, in `THEORY.md`, `CORE.md`, `README.md`, and `theory/SELECTION_AXIOMS.md`:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

`theory/REPRESENTATION.md` does not restate it. The diffs in those four files do not touch the sentence.

## Wording

`git diff d1a6de4...HEAD` contains no `bill`, no `kill`, and no `honest kill`. `theory/REPRESENTATION.md` and `theory/representation_checks/` use cost, not bill.

## Commands and results

1. Independent recomputation, `nice -n 19 python3` (script written for this review, not the repo script). Kelly `q*=13/50`, means `247/200` and `417/400`, `G'(0.26)=0`. Lundberg `τ_S=0.236207527`, `τ_E=0.316227766`. CQ derivatives `−6.327`, `−11.296`, `−12.803` at `B=0.49, 0.50, 0.505`. Dent: `4/9` algebra, and 0 failures in 15,007 nonnegative weights.
2. Still two-state enumeration, same parameters as `check_all.py`, rerun independently. Maximum gap `3.6×10⁻¹⁶`.
3. Crossref `GET https://api.crossref.org/works/<doi>` for all 24 DOIs in §10. All 24 returned. Titles match. Debreu reprint `issued.date-parts = [[null]]`. Eleven of the calls had to be retried after HTTP 429; the retries succeeded.
4. `python3 tools/check_consistency.py` → `RESULT: PASS`, exit 0. Wording FAILs 0. CLAIM_MAP rows 363, tally 363. (Advisory length warnings on THEORY.md and README.md, not failures.)
5. `git fetch origin main` (the snapshot's `origin/main` was `2eeab30`; after fetch it is `b421b22`). Then `python3 tools/check_fresh.py` → `STATUS.md main is d1a6de4; window: b421b22 98ff384 d1a6de4 b16193d e88b692` → `RESULT: PASS`, exit 0.
6. `python3 tools/check_open_work.py` → `RESULT: PASS`, exit 0. Union missing from `OPEN_WORK.md`: 0.
7. `nice -n 19 python3 -m pytest -q tools`. First attempt: exit 1, `No module named pytest` (sympy was also absent). After `pip3 install --user pytest numpy scipy sympy`: **248 passed, 1 skipped**, 299.71 s, exit 0.
8. `nice -n 19 python3 theory/representation_checks/binding_multiplier.py` → 44 checks, 0 FAIL, `RESULT: PASS`. CQ lines: `B=0.49` `th'=-6.326936e+00`; `B=0.50` `th'=-1.129607e+01`; the third PASS line is labeled `B=0.51` and carries `th'=-1.280299e+01`, which is the `B=0.505` value (nit 5).
9. `lake build` was not run.

## Nits

1. **`measurement/CLAIM_MAP_v2.md` line 88, the v2.77 note, opening sentences.** In the present tense, before the revision clause, V1 is still described as proved with nonnegative prices and with `hK` inside the sum forced by A1–A7, and V2 is still described as a one-axiom ablation (F1, CT34, CT36, S4, Still, F3). The same paragraph then says V1 no longer takes nonnegative prices from A1–A7, that Debreu is only applied to interval factors, and that V2 no longer claims a one-axiom ablation. The status column is the narrowed claim. A reader who stops at the opening sentence is told a false theorem. Counterexample to that opening sentence: on three interval coordinates, `I + A − 𝔼[ℓ]` is continuous, additive, concatenating, Shannon in the memory coordinate, affine in the loss, and exogenous, and its error price is negative.

2. **`theory/REPRESENTATION.md` line 58.** "Linear combinations" of Shannon and Hartley is wider than Aczél–Forte–Ng. Counterexample: `−H` is a linear combination, and it is symmetric and expansible, but it fails subadditivity whenever `H(X,Y) < H(X)+H(Y)`. The theorem is the nonnegative cone. The same sentence names Faddeev's grouping axiom as the further hypothesis "as stated by" Aczél, Forte, and Ng. Csiszár, cited on that line, isolates Shannon by continuity for `n=2`, and treats Faddeev as a separate theorem that also needs continuity. The proof's step 4 does not use the false direction: it takes finite-law Shannon up to a positive constant and marks the Gaussian formula as an extension.

3. **`theory/REPRESENTATION.md` lines 72 and 108.** Lemma C is proved for monotone `f`, both directions. Step 3 also cites "Debreu continuity" for a price that has not been assumed monotone. A continuous additive function on `(0,∞)` is linear, and the rational step `f(q)=q f(1)` is already in the proof of Lemma C, but the density sentence is not written. The negative-price case is covered by the monotone proof once the cost component is known to be monotone; continuity is the route only when that is not assumed.

4. **`theory/REPRESENTATION.md` lines 64 and 88, and line 246.** The negative-price witness is written `I_mem+K−𝔼[ℓ]`. A3's domain is a product of intervals, and `K` is the discrete coordinate the repair just removed from the Debreu step. The sign claim is true for `I+A−𝔼[ℓ]` on three intervals. Separately, F-0's first sentence says the attained scores are the image of a nonempty compact design set, and the next sentence says that image is compact. Without continuity of the score that deduction is false: on `[0,1]`, `f(0)=0` and `f(x)=1/x` for `x>0` has image `{0}∪[1,∞)`. The later arguments use compactness as an assumption (the second sentence), and those arguments are fine given the assumption.

5. **`theory/representation_checks/binding_multiplier.py` lines 202–207.** The loop checks `B ∈ {0.49, 0.50, 0.505}`, but the check name uses `%.2f`, so `0.505` is printed as `0.51`. The derivative on that PASS line equals the derivative at `B=0.505` (`−1.280299×10¹`), not a separate solve at `0.51` (which is above `B_slack` and is slack). The qualification check itself is at the three stated buffers.

## Bottom line

The narrowed V1, the narrowed V2, the section 7 separation of the compact attained set from its unbounded free-disposal hull, F3's Pareto point at the origin, the coordinate cap, V5 open, V6 proved in-model, the `4/9` dent for every nonnegative weight, and constraint qualification at `0.49`, `0.50`, and `0.505` are true and are what the status rows say. The cited applications of Debreu, Pexider, Lundberg, Kelly, and Still stay inside the hypotheses that those theorems actually have, with the Aczél–Forte–Ng gloss in nit 2. The hypothesis sentence is unchanged. The new text does not say bill, and it does not use kill as a verdict.
