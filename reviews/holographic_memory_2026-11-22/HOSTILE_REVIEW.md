# Hostile review of draft PR #186

Sunday 22 November 2026. Independent review of https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/186. Head `bd2bfd76ab6cc78fdc0ef0b8185cc3706181862c`, base `6340b177bae94074d90bdbb3a2bfaad0e4915d90` (`main`). The diff against that base is five files: `theory/HOLOGRAPHIC_MEMORY_2026-11-22.md`, `theory/holographic_memory_checks/memory_checks.py`, `theory/holographic_memory_checks/crossref.out`, `tools/test_holographic_memory_checks.py`, and one row, T41, in `OPEN_WORK.md`. This review edits none of them. No lake build.

The arithmetic in §§3–5 recomputes. The degradation identity recomputes. The ruin-cap numbers recompute on the grid the note states. What does not hold is the selection those numbers are doing. A cap on the chance of a large error, at the note's own heat and upkeep, selects replicated copies of one local memory. It does not select the distributed split.

## Verdict

**NEEDS-FIXES**

## Blocking

### B1. The ruin cap selects copies, and the split is the costlier way to buy the same tail

`theory/HOLOGRAPHIC_MEMORY_2026-11-22.md:151` and `:153`, the degradation and ruin-cap claim in §4.

The note compares a precision budget split across units that all observe the same sum with a coarser split of that same budget, and with item erasure. The existing copy result is a third design, and it is the one the cap has already been proved to select. R1 in `theory/ROBUSTNESS.md:60` is n independent copies of one layer, upkeep h each, loss E₁ if at least one copy is up and E₀ if all are down:

\[
J(n)=n h+w E_1+w(E_0-E_1)p^n.
\]

Put the note's sum on that layer. E₁ is the full-precision error ε=V/(1+μ), E₀ is the prior V, and the heat of the precision is charged once, which is the charge the note's upkeep paragraph already uses (`heat_fixed`, the same μ at every D). Upkeep stays h per unit. That is equal heat and equal upkeep.

On every failure draw the copy error is at most the split error. With i units up out of n,

\[
\varepsilon_{\mathrm{split}}(i)=\frac{V}{1+(i/n)\mu},
\qquad
\varepsilon_{\mathrm{copy}}(i)=
\begin{cases}
V/(1+\mu) & i\ge 1,\\
V & i=0.
\end{cases}
\]

For 1≤i≤n the split's surviving precision (i/n)μ is at most μ, so its error is at least the copy's. The two agree at i=0 and at i=n. The same n, the same installed μ, the same p, the same h, and the same stake therefore give the copy a cost at most the split's. If the full-precision error sits at or under the cap and the prior sits over it, the copy ruins only on i=0, and the split ruins on i=0 and on every thinner tail the cap still cuts. Every cap the split meets, the copy meets, at a cost no higher. No failure rate, no cap level, and no upkeep reverses this. It is the same ordering at every point, not a feature of the worked numbers.

At the worked point V=4, μ=3, ε=1, p=0.2, h=0.5, w=1, and P(error>1.5)≤0.05:

| Design | n | P(ruin) | E[error] | cost |
|---|---|---|---|---|
| One unit, either packaging | 1 | 0.200000 | 1.600000 | 5.100000 |
| R1 copies | 2 | 0.040000 | 1.120000 | 5.120000 |
| R1 copies at the split's n | 7 | 1.280×10⁻⁵ | 1.000038 | 7.500038 |
| Split, cheapest feasible D in 1…20 | 7 | 0.033344 | 1.200585 | 7.700585 |

The copy meets the cap at n=2 because 0.2²=0.04. The split meets it at n=7. The gap is the upkeep on five extra units plus a worse error. R1-a's own test says copies do not pay on expected cost here: w(V−ε)p(1−p)=0.48, which is under h=0.5, so n_E=1 and the cap is what lifts the copy count from 1 to 2. That is R1-b. The note's sentence that the cap selects the costlier design is this fact, already proved for copies, and the split is a strictly costlier instrument for it.

Charging every copy its own floor, which is more heat than R1 charges, still does not save the split at this point. The smallest full tracker whose up-state clears 1.5 has μ=V/1.5−1=5/3. Two such trackers have total heat 10/3, expected error 1.6, and cost 5.933, against the split's 7.701. The split's extra upkeep is larger than the heat it saves.

The heat-cap grid is the same comparison with the upkeep turned off and with expected heat E[ρ]μ. The printed minimum is real: on D∈{1,2,4,8,16} and μ=0.5×1.12^n for n=0,…,47, expected cost picks heat 1.391420 (D=16, μ=1.739275, chance 0.971853) and the cap P≤0.05 picks heat 2.189426 (same D, μ=2.736783, chance 0.026657, cost 4.085295). An R1 copy on that same objective, heat μ(1−p^n) for one live memory, meets P≤0.05 at n=2 and μ=5/3 with expected heat 1.6, expected error 1.6, and cost 4. The cap does not raise that design's heat from 1.391 to 2.189. A slice that freezes expected heat at 2.189 and compares D=16 with n=2 gives the split the lower error (1.264 against 1.330), because the split installed μ=2.737 while the copy, up 96 percent of the time rather than 80, installed 2.281. That slice is not the minimizer. The minimizer under the cap is the copy.

Two readings are easy to confuse with this, and neither is R1.

- Fragments that do not pool. Each of n units holds precision μ/n and the reader keeps one survivor. Pooling, which is the split, has the lower error on every draw. At the worked budget μ=3 a single fragment clears error 1.5 only for n=1. For n≥2 the one-fragment error is at least 4/(1+3/2)=1.6, so the non-pooling package cannot meet the cap at all. Beating that package is the split compared with a reader who discards surviving fragments.
- Item erasure, (1−f)ε+fV. That is a different code, proved smoother than the split is not. It is not a local memory plus spare copies of the decision.

The identity itself stands. At V=4, ε=1, f=1/4 the split error is 16/13=1.230769230769 and the item error is 7/4=1.75. The slopes at f=0 are 3/4 and 3. The note already says the ordering under a cap is the shape of R1 and CT37, and that the new piece is the identity. That disclaimer is the right scope for the identity. It does not put the copy baseline into the worked cap, and without that baseline the cap paragraph reads as a reason to distribute. T41 repeats the heat rise 1.391420 to 2.189426 with no copy next to it.

**Fix.** In §4, at the worked cap, give the R1 cost at the same installed μ and the same h. State the pathwise bound, and that it leaves no (p, cap, h) on which the split is cheaper. Keep the degradation identity as the new piece. On the heat-cap grid, put the one-memory copy next to 2.189426: under that heat rule the cap is met at expected heat 1.6. If a revision wants each copy to dissipate its own floor, label that as a different accounting and recompute; at the worked upkeep point the two-tracker cost 5.933 is still below the split.

**Antifragility, reported as a conjecture and not as a result.** Nothing in §4 shows performance improving when a part is lost.

The split error and the item error are both strictly increasing in the failed fraction f, for ε∈(0,V). At the worked point the derivatives at f=0 are 0.75 and 3, and the split's second derivative is 1.125. Inside M-C and M-L the same monotonicity is structural. Removing a unit subtracts a positive semidefinite update from Φ. The posterior covariance rises in the Loewner order, and tr(U S) does not fall for a positive semidefinite loss U. Re-optimizing the decoder on the remaining channel cannot undercut the error the larger channel had already achieved. Forced compression would need a code whose error is not monotone in that order: interference, a nonlinear cleanup, or an added constraint that forces precision onto a direction the cost equation would have left at zero. The optimum in §3 is allowed to put zero precision on a direction. That test is outside this class. Label it **CONJECTURE**. Do not treat it as a prediction this note has earned.

The repository's own definition is a different stressor. `theory/ROBUSTNESS.md:198` uses Taleb and Douady: antifragile when the cost is concave in the stressor. The split's cost as a function of f,

\[
J(f)=(1-f)\mu+w\frac{V}{1+(1-f)\mu},
\]

has second derivative 2 w V μ² / (1+(1−f)μ)³, which is positive. Under that definition the split is fragile to variation in f. R4's stressor is the variance scale of one Ornstein–Uhlenbeck mode, and this note does not compute it.

A small certain loss can lower one draw's cost when the installed μ sits past the unconstrained minimizer of heat plus stake. At the cap-selected μ=2.736783 and stake weight 1.5, the derivative of ρμ + 1.5 V/(1+ρμ) at ρ=1 is 1.561, so moving from ρ=1 to ρ=0.8 lowers that draw's cost from 4.342 to 4.071 while the error rises from 1.070 to 1.254. The healthy minimizer at this stake is μ=√6−1=1.449490, cost 3.898979, below the damaged draw. The cap bought the extra precision for the tail. Shedding it on a mild draw is surplus heat coming off. It is not an error that improved, and it is not a gain over the design that was healthy at the lower precision.

**Fix, one sentence.** After the identity, say that both curves increase in f, that a mean-square Gaussian channel cannot lower its error by losing a unit, and that an error which falls under part loss is a conjecture outside M-C and M-L.

## Suggested

### S1. The shared eigen-allocation is what a separable precision cost does, and the factor-s window is shared with a nat price

`theory/HOLOGRAPHIC_MEMORY_2026-11-22.md:15` and `:110`.

For identical modes the heat floor is kT a v tr Φ. On an isotropic prior the quadratic loss tr(U S) is minimized, at fixed eigenvalues of Φ, by aligning the smallest posterior variances with the largest eigenvalues of U. Each direction then separates into a scalar problem. Any cost that is an increasing separable function of those precisions has the same alignment and the same "keep the directions above a threshold" shape. Kolmogorov's ½ log and the heat functional a(v−σ)/σ are two such costs. Landing on the alignment is the algebra of the class. The merged sum-loss theorem had already done it for the all-ones task (`theory/INFO_PHYSICS_GENERAL.md`, Proposition G-sum). The note's own hedge, "not a new geometric law," is the accurate half of the paragraph. "Independent convergence" and "it is support" are the half that overreaches. Support for the heat functional would be a measurement that a ½ log price does not also pass.

The factor-s stake window is one of those shared predictions. A direction of weight λ is tracked when the stake times λ clears a constant. For the heat price the constant is kT a/v. For the nat price κ·½ log(v/σ)+w λ σ the constant is κ/(2v). The ratio of the local threshold to the spike threshold is s for both, because both constants sit in front of 1/λ. The predictions that do separate the prices are the ones §5 already computes, plus the cost's dependence on the stake. The heat-optimal error is √(kT a V/w) and the minimized cost is 2√(kT a V w)−kT a. The nat-priced error is κ/(2w) and the minimized cost is (κ/2)(1+log(2 w V/κ)). Log-log slopes on stakes 2, 4, 8, 16, 32 are −1/2 and −1 exactly, and raising a from 1 to 5 multiplies the heat-optimal error by √5=2.236068 and leaves the nat-priced error where it was.

**Fix.** In the opening and in the "where this sits" paragraph, say that the alignment is the optimum of a separable precision cost on an isotropic Gaussian, and that the heat functional is distinguished by the slope −1/2, by √a, and by a cost that grows like √w. Say the factor-s window is the counting shape of any threshold proportional to 1/λ. Keep the follow-up as the measurement.

### S2. Three printed Monte Carlo means have closed forms, or a mean over codebooks, underneath them

`theory/HOLOGRAPHIC_MEMORY_2026-11-22.md:98` and `:104`.

A uniform unit vector g in R^K has E[(1·g)²]=1. At heat 4 the posterior variance of the sum is K − 4(1·g)²/5, so the expected error on K=20 is exactly 19.2. The aligned coordinate at that heat has error K/(4+1)=4. The 400 draws at seed 2 average 19.229058, with a standard error of the mean of 0.050. The proposition says "on average over 400 draws." The line in "what is new," and the PR description, print 19.229 against 4 as the gap.

The Haar energy E[‖P 1‖²]=D is exact. The 2000 draws average 5.045757 with standard error 0.0583, against D=5. The proposition states the expectation and then the sample. That one is in the right order.

At K=s=D=8 the support is the whole space, so the 80 draws in the checker are one Gaussian matrix, repeated. Seed 4 gives 3.942262. Across 2000 independent codebooks the mean error is 4.079182 (standard error 0.0045), and the tenth percentile is 3.824. The local code's error 8/3=2.666667 stays below that whole range. The claim's direction holds. The printed 3.942262 is one draw, on the low side of the distribution.

The known-support triple at K=32, s=4, D=8, heat 16 is in better shape. The local error 10/3=3.333333 and the ideal 4/5=0.8 are exact. The projection mean 1.204911 is 300 supports of one codebook, standard error 0.011.

**Fix.** Print 19.2 as the expected error, and keep 19.229 as the seed-2 mean if a sample is wanted. For the full-support line, print a mean over codebooks, or say that 3.942262 is the seed-4 matrix.

### S3. The per-item proof does not cover the rank cap used in the example, and 7.177 is one shared axis

`theory/HOLOGRAPHIC_MEMORY_2026-11-22.md:44` and `:118`.

Zeroing the off-diagonal entries of Φ holds the trace fixed and weakly lowers every marginal variance, because S_kk≥1/P_kk. That proves a diagonal optimum when there is no rank cap. The diagonal of a rank-D matrix can have more than D nonzeros, so the same replacement can raise the rank. The two-slot claim needs the ordering argument already written in Proposition M-task: at fixed eigenvalues of Φ, tr(diag(c) S) is minimized by putting the smallest posterior variances on the largest weights. The claim is true. The proof as written discharges the uncapped sentence and the trace gaps, which are exact (4/(4−ρ²)−1 equals 0.010101, 1/15, and 4/21 at ρ=0.2, 0.5, 0.8).

The number 7.176851 is the best precision on the all-ones unit vector, φ=√1.825−1. The item-aligned cost is 2√3+2.3=5.764102: the weight-4 slot costs 3, the weight-3 slot costs 2√3−1, and the two light items add 0.3. A shared axis on the two heavy items, u=(1,1,0,0)/√2, has cost √3.5+3.8+√3.5−1=6.541657. Still above 5.764102, and still the wrong object for the sentence "the shared axis costs 7.177." The FAILS bullet is right that unequal per-item weights make a shared axis worse. It names the wrong axis's cost.

**Fix.** Point the two-slot sentence at the ordering argument in M-task. In the FAILS bullet, say an all-ones axis, and if a second number is wanted put the two-heavy-item axis next to it.

### S4. The opening's watt figure is the floor, and T41 flattens two identifications §6 rejects

`theory/HOLOGRAPHIC_MEMORY_2026-11-22.md:19` and `:169`. OPEN_WORK T41.

Boltzmann's constant times 300 K is 1.380649×10⁻²³ × 300 = 4.141947×10⁻²¹ J. At drift 1 per second, (v−ε)/ε=1, and 10⁹ modes, the floor is 4.141947×10⁻¹² W. The opening's 4.142×10⁻¹² is that floor, rounded. The signal-to-error ratio of two is v/ε=2, which is the same (v−ε)/ε=1. The second figure, drift 10⁹ per second and rank 10¹², is 4.141947 W, and §5 says the theorem does not license it. The assumptions that do license the picowatt figure are: the memory-bath floor, not heat plus stake; the fast-memory infimum, not a finite-rate spring; equilibrium cancellation of the signal bath; one second⁻¹ drift; rank 10⁹; temperature 300 K. "Sit at" is the verb the floor has not earned. A finite-rate memory sits above it. The note's own two springs at rate 10⁵ have heat 5.39980915 against a static learning rate 5.40000000.

T41 says the geometry matches water-filling, superposition, and compressed sensing. Section 6 labels the identification of Elhage's phase change with the stake window as FAILS, and it refuses to restate the Candès–Tao and Donoho bounds because those abstracts were not in the records. The known-support calculation is the part that sits next to sparse features. The flat sentence in T41 drops that distinction. Elhage and coauthors, the arXiv abstract, and the sixteen names match the arXiv API. The DOI 10.48550/arXiv.2209.10652 returns HTTP 404, in both casings, and the note does not cite it.

**Fix.** In the opening, in §5, and in T41, call 4.141947×10⁻¹² W the floor under those assumptions. In T41, keep the water-filling sentence in the form S1 asks for, and do not say the geometry matches superposition and compressed sensing as a single claim.

### S5. One reference is unused, and the cap probability is not monotone in the number of units

Burak and Fiete, doi 10.1371/journal.pcbi.1000291, is in §9 and in no sentence of the note. The Europe PMC abstract is a path-integration result (on the order of 10–100 m and 1–10 min). The crossref log already says it is not used as a heat result. The reference line does not say that.

The chances 0.200000, 0.180800, and 7.003561×10⁻³ at 1, 4, and 16 units are right (binomial, success probability 0.8, ruin when the up-count is below 5/9 of D). The chance is not monotone in D. At D=8 it is 0.056282, which misses the 0.05 cap, while D=7 meets it at 0.033344. The upkeep search over D=1,…,20 finds 7. A reader who steps only through powers of two will think D=8 is the first feasible split and will be wrong.

**Fix.** Drop the Burak line, or name the sentence it supports. Next to the triple, say the chance is not monotone in D and that the cheapest feasible count on this cap is 7.

## What was checked and holds

### Wording, and the three files that must not move

Searched the note and the T41 row for "bill," "kill," and "verdict." None are there. The falsifier headings say "what would refute it." That is a future measurement, and the misses in the note are labeled FAILS. GTAO is named as the theory in this repository. The hypothesis sentence quoted in the note is the sentence at `THEORY.md:41`, `CORE.md:9`, and `README.md:9`:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

`git diff 6340b177bae94074d90bdbb3a2bfaad0e4915d90 -- THEORY.md CORE.md README.md` is empty.

### The proved arithmetic

Recomputed from the closed forms, the Lyapunov equation, and an independent grid, then again by rerunning `theory/holographic_memory_checks/memory_checks.py`. The note's digits are on the left.

| Claim | Independent value | Result |
|---|---|---|
| s identical modes, matched sum-error, heat ratio | exactly s, because Z is the scalar OU of rate a and variance s v, and the symmetric local split s_k=ε/s is optimal | holds, and the note marks s=K as the merged theorem |
| Rates (1, 100), variances (1, 1), sum-error 0.5 | μ=(101+√11401)/2=103.887732673340, separate heat 21+120=141, ratio 1.357234356 | prints as 103.887732673340 and 141 |
| Rate ratio 1 and 4, same error | ratios 2 and 13/μ with μ=(5+√73)/2, i.e. 1.919668695 | prints as 2 and 1.919669 |
| Per-item costs, weights (4, 3, 0.2, 0.1) | item-aligned 5.764101615, all-ones 7.176851217 | prints as 5.764102 and 7.176852 |
| Pure sum, K=4, stakes 0.1, 0.5, 4, 100 | costs (0.4, 0.4), (1.828427124746, 2), (7, 12), (39, 76), ratio 76/39=1.948717949 | prints match, including 1.948718 |
| Subset spectrum and high-stake ratios at K=12, w=10⁶ | 1, 1.00821847, 1.05445423, 1.13501808, 3.46286939; limits 1, 1.008208, 1.054405, 1.134910, √12=3.464102 | table matches; s=12 is the finite-w value, and the prose says the limit is √12 |
| Disjoint groups m=3, s=4, stake 10⁸ | ratio 239988/119997=1.999950000 | prints as 1.999950 |
| Degradation at V=4, ε=1, f=1/4 | 16/13 and 7/4 | prints as 1.230769230769 and 1.750000000000 |
| Upkeep cap | D=1 cost 5.100000; D=7 cost 7.700585, chance 0.033344 | matches |
| Heat-cap grid | 1.391420 → 2.189426 | matches, as a minimum on that grid |
| Rank-2 task, K=100, stake 4 | cost 6, two directions | exact |
| Heat per tracked mode | r kT a(v−ε)/ε | the scalar floor, r times, for orthonormal readouts |
| Slopes | −1/2 and −1; √5=2.236067977 | exact |
| Picowatt floor | 4.141947×10⁻¹² W | exact under the assumptions in S4 |
| Two springs, rate 10⁵ | heat 5.399809150 against learning rate 5.400000000 | matches |

The rank sentence that a local code holding all K items at marginal error ε pays K/r times the heat of r readouts at error ε is the heat of those two designs. A unit readout of conditionally independent items held at marginal error ε has readout error ε, so the task errors match. It prices the code that stores every item, which is the wasteful one when the task has rank r.

### Labels that are fair, including the ones that look harsh

Proposition M-item's FAIL, "a shared memory always costs less," is the right label inside the class. Unequal per-item weights make a diagonal allocation better, and S3 only corrects which shared axis was priced. An isotropic per-item loss ties, which the note says.

"Sparse queries favor a shared memory" fails as a high-stake claim at the printed ratio 1.008218. That is a different object from Elhage's phase change. The note says so, and it labels the identification FAILS while leaving the phase change KNOWN. The known-support calculation is the place a random codebook wins, 1.204911 against 3.333333 against 0.800, and it is reported as a positive result. The class did not bury it.

"Random distributed storage is the holographic optimum" fails for a known sum because the class contains the matched channel. The aligned coordinate is feasible, and a random coordinate is a mismatched one. The expected errors are 19.2 and 4. The note says Plate's construction and Kanerva's title are a different design problem, a query that is not one known functional. Scoped that way, the FAIL is fair. It is not a result about the problem those constructions solve.

The phone sentence is a metaphor in the note's own sense: the name adds no prediction the cost equation does not already make. The proved substitute is on the same page. The heat depends on the rank of the decision and on the drift of those modes. At fixed per-readout error the floor is proportional to r, and the ambient dimension drops out once the eigenvalues of U are fixed. The K=100 example costs 6, the same as two modes. The dismissal is that a frontier model on a phone does not follow from this floor. That is the right strength. The floor is not a parameter count, and §5 says so, including the stock ½ log(v/ε) and the heat kT a(e^{2I}−1) at stock I.

The Gaussian linear class is the class in which a known combination is cheapest to share and a random code is dearest. The note's positive theorems are in that direction, and the open complement (a loss that is not a mean square, a conditional that is not Gaussian) is named. The FAIL labels are boundaries inside the class, not a verdict on holographic storage outside it.

### Citations

Every DOI in §9 was fetched from `https://api.crossref.org/works/<doi>` on 22 November 2026. Each returned HTTP 200 with the title, year, and author list the note prints. 10.48550/arXiv.2209.10652 returned HTTP 404 in both casings. Amit, Gutfreund, and Sompolinsky, doi 10.1103/PhysRevLett.55.1530, returned 200, title "Storing Infinite Numbers of Patterns in a Spin-Glass Model of Neural Networks," no abstract. The note does not cite it. That matches the reason given in §7.

Abstracts that the note uses were read from Europe PMC, and from Crossref where Crossref had one.

- Hopfield's abstract gives a content-addressable memory that yields an entire memory from any subpart of sufficient size, and collective properties only weakly sensitive to the failure of individual devices. Both sentences the note uses are in it.
- Plate's Europe PMC abstract represents bindings in a fixed-width vector.
- Caron's abstract: each of 200 traced Kenyon cells integrates an apparently random combination of glomeruli, with no discernible organization by odour tuning, anatomy, or developmental origin. The note's paraphrase matches, and it does not import the count 200.
- Dasgupta, Stevens, and Navlakha, Europe PMC: similarity search by a variant of locality-sensitive hashing, and three computational strategies that the abstract does not name. The Crossref abstract field on this DOI is a *Science* issue blurb and does not contain the hashing sentence. The note attributes the abstract to Europe PMC.
- Hafting and coauthors: a triangular lattice, neighbours sharing orientation and spacing and differing in phase.
- Sreenivasan and Fiete: accuracy under noise outside the class of the sensory and motor population codes they compare.
- Mathis, Herz, and Stemmler: place cells at one location, grid cells on a hexagonal lattice, Fisher information, a resolution-versus-range tradeoff. The nested-module predictions in that abstract are not imported.
- Olshausen and Field: localized, oriented, bandpass fields from maximizing sparseness, and greater statistical independence.
- Heanue, Bashaw, and Hesselink: error-correcting encoding for bit-error rate. The degradation identity is not in that abstract, and the note does not say it is.
- O'Keefe and Dostrovsky: Crossref has no abstract, and Europe PMC returned no record. The note cites the title only.
- van Heerden, Kanerva, Candès and Tao, Donoho, Kolmogorov, Sims, Gabor: Crossref returned no abstract. The note cites titles, or, for Kolmogorov and Sims, the water-filling description already booked in `theory/INFO_PHYSICS_GENERAL.md`. No new extraction is claimed, and none was found in an abstract.
- Horowitz and Esposito: title, year, and authors match. Neither Crossref nor Europe PMC returned an abstract. The shape Q̇≥kT times the learning rate is the one the heat notes already attribute to them. This note does not re-prove it.
- Elhage and coauthors: the arXiv abstract and the sixteen names, in order, match the arXiv API, including the phase change. The note does not import the polytopes or the adversarial-examples sentence.

### Scripts

All four at `nice -n 19`, from the repo root, on head `bd2bfd76`. No lake build.

- `python3 theory/holographic_memory_checks/memory_checks.py`: 84 checks, FAIL 0, exit 0.
- `python3 tools/check_consistency.py`: RESULT PASS, wording FAILs 0.
- `python3 tools/check_open_work.py`: RESULT PASS.
- `python3 -m pytest -q tools`: 256 passed, 1 skipped.

## What would make this READY

B1 is the block. The degradation identity, the grid numbers, and the sentence that redundancy under a cap is already R1 can stay. The worked cap has to show the copy baseline at the same heat and the same upkeep, and it has to say that the split does not win that comparison. One sentence has to keep antifragility outside the class, as a conjecture. S1–S5 are the wording and the Monte Carlo prints. None of them is the selection error in §4.
