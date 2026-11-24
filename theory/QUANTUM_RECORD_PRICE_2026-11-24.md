# Quantum record price: four routes, none names it

*24 November 2026 (UTC). Desk note, second pass. No script. Self-check, not an independent review. `THEORY.md` is unchanged. Open-work row T74. Status words are those at `CORE.md:169`. Nothing here derives general relativity, quantum mechanics, or holography.*

*Each route below states what it assumes, where it stops, and a status label. A route that would name a price only by adopting a known entropy theorem is marked KNOWN and is not counted as a derivation.*

## Answer

No unique quantum-record price. Four routes, each a different question.

- **Route 1** stops at A6's naming step. **PROVED (in-model).**
- **Route A** (minimum over admissible prices) stops on a tie, including a tie with the zero price A8 allows. **PROVED (in-model).**
- **Route B** (selection under the ruin cap) stops because the cap does not rank price functionals. **PROVED (in-model).**
- **Route C** (R1's axioms on a GPT state space) stops because the operational entropies are not one functional. That separation is **KNOWN**. Adopting von Neumann entropy or Umegaki relative entropy is also **KNOWN**, and it still does not choose the record contraction.

## Where a quantum price is already assumed

On this main (`0f37918`):

- `CORE.md:52` and `theory/REPRESENTATION.md:58` name the memory coordinate as Shannon mutual information, or the Gelfand–Yaglom–Dobrushin supremum when that mutual information is finite. Both are classical. `theory/REPRESENTATION.md:60` says the Aczél–Forte–Ng uniqueness is not extended to differential entropy.
- `theory/DIRECTIONS_2026-11-22.md:58` parks a conjecture that the frontier carries over with a Holevo bound, quantum channel capacities, and a quantum Landauer cost, with a different price on copying. That sentence assumes those floors. It does not derive which functional the record pays. The file says its references are to be checked before any canonical use, so they are not cited here.
- `theory/RECORD_REPAIR_FLOOR_2026-11-23.md:114` and `:174`, and `theory/PHYSICS_CHAIN_2026-11-23.md:18`, leave the repair heat of a quantum record in three dimensions open. They do not choose among mutual information, a pinch divergence, and dimension.

Off this main:

- Draft PR #252, head `bd63638`, `theory/pointer-basis-stakes-2026-11-24/PREREG.md:24`. A6 does not fix a quantum price. The note then chooses the mean Umegaki divergence of the pinch, \(P_D=\mathbb{E}[D(\rho\|\Phi_\theta(\rho))]\) (`PREREG.md:28`). Beside it, \(P_\chi=I(W;M_\theta)\) is the Shannon mutual information of the classical outcome (`PREREG.md:34`). The Holevo quantity of the ensemble before the measurement does not depend on \(\theta\) and is not used. Ruin is slack (`PREREG.md:36`).
- Draft PR #253, head `fd69ec3`. `theory/COMPOSITE_CONTEST_2026-11-24.md:46` names the choice of headline price and does not make it. `:56` sets that price to \(\lambda\ln K_{AB}\). On a protocol whose settings are drawn after the record, the A6 coordinate is 0 for every contestant (`:56`, `:96`, `:154`). Mutual information and the dimension price rank one control in opposite directions (`:154`).

DOIs below were resolved on the Crossref API on 24 November 2026. Title, authors, and pages match. A DOI is printed only in that case.

## Route 1. The representation minimum

**Route.** Ask whether the minimum of a cost under A1–A8, subject to the ruin cap, names one quantum-record functional, in the way R1 names the classical memory coordinate.

**Assumes.** A1–A8 as stated in `theory/REPRESENTATION.md:39-64`. The ruin cap is the feasible-set restriction in A2.

**Where it stops.** A6 names the coordinate before any minimum is taken. The minimum then returns a design, not a functional.

**Status. PROVED (in-model).** Under A1–A7, on at least three essential intervals, a continuous cost is \(C=a\sum_i p_i z_i+b\) with one \(a>0\) (`theory/REPRESENTATION.md:84-92`). Step 4 puts Shannon mutual information, in A6's scope, into the memory slot (`:114`). `CORE.md:52` says R1 does not choose the coordinate list. On a menu that does not depend on the numerical cost, \(C\mapsto aC+b\) preserves the argmin (`theory/REPRESENTATION.md:126`). Theorem S3 (`CORE.md:48`) runs the other way: an undominated design is a minimizer at some nonzero nonnegative prices. A6's input is a finite alphabet, or a pair of classical random variables on standard Borel spaces with finite mutual information (`theory/REPRESENTATION.md:58-60`). A state on a Hilbert space is not that pair, so the linearity step does not fire. A5 makes a concatenating coordinate linear once it is the coordinate in the sum; it does not choose which additive functional is placed there. A8 only signs a coefficient already in the sum (`:64`). The ruin cap is not produced by the representation (`:96`).

The candidates are not one coordinate up to \(a>0\). On one fixed classical alphabet, a non-degenerate perfect copy has \(I(W;M)>0\) and a pinch in that basis has \(D(\rho\|\Phi(\rho))=0\). An independent record has both equal to 0. No \(a>0\) carries one pair of values onto the other. Dimension \(\lambda\ln K\) is constant on that menu and is not essential (`theory/REPRESENTATION.md:80`, Lemma M). The Holevo quantity of an already classical outcome equals \(I(W;M)\). **ELEMENTARY**, from \(S(\rho)=-\mathrm{Tr}\,\rho\ln\rho\) on a diagonal state. That is A6's coordinate. The pre-measurement Holevo quantity is a different functional, and draft #252 does not use it (`PREREG.md:34`).

## Route A. Minimum over admissible prices

**Route.** Treat the price functional as chosen with the design. Minimize the cost over the set of admissible quantum record prices, and over the record.

**Assumes.** The cost at a named price \(P\) and a record \(x\) is \(J(P,x)=P(x)+w L(x)\), with \(w\ge 0\) and \(L\) the decision loss. "Admissible" is either every nonnegative functional (the A8 orthant, `theory/REPRESENTATION.md:120`) or the two-element menu \(\{P_D,P_\chi\}\) from draft #252. The comparison that uses that menu takes the locked complete-dephasing form (`PREREG.md:64`): for Bloch radius \(r\in(0,1)\) and angle \(\theta\in[0,\pi/2]\),

\[
P_D(\theta)=\tfrac12\Big[h\Big(\tfrac{1+r|\cos\theta|}{2}\Big)-h\Big(\tfrac{1+r}{2}\Big)\Big],\qquad
P_\chi(\theta)=\tfrac12\Big[\ln 2-h\Big(\tfrac{1+r|\cos\theta|}{2}\Big)\Big],
\]

\[
L(\theta)=\tfrac{r^2}{2}-\tfrac{r^4\cos^2\phi\,\cos^2\theta}{4},
\]

with \(h\) the binary entropy in nats. No new grid is run. The monotonicity used below is the derivative \(h'(p)=\ln((1-p)/p)\), which is negative for \(p>1/2\) and zero only at \(p=1/2\). **ELEMENTARY.**

**Where it stops.** The minimum is not a single price.

**Status. PROVED (in-model).** Three stops, in order.

1. **The support function takes the prices as given.** Theorem S2 (`CORE.md:48`) says the minimum cost is the support function of the feasible set. The argument of a support function is a price vector in a coordinate space that has already been named. Changing the coordinates changes the argument. The minimum does not choose the coordinates.

2. **The A8 orthant minimizes at zero, tied with anything that vanishes.** A8 makes each concatenating coordinate a bad (`theory/REPRESENTATION.md:64`). Under A8 the price on that coordinate is nonnegative (`:92`), and a coordinate that is not essential has price zero (`:80`, Lemma M). The zero functional meets both. At stake \(w\), it scores \(w\min L\) on a loss-minimizing record. Any admissible price that is zero on that same record scores the same number. On the menu of stop 3 the pinch is zero at the loss minimizer, so its minimized cost equals the zero price at every stake. The copy-versus-noise pair in Route 1 shows that this pinch is not \(I(W;M)\). The minimum therefore does not separate "charge the pinch" from "charge nothing." Charging nothing is not a quantum record price.

3. **On the hand-listed menu the minimum ties on a large set.** Restrict, by hand, to \(\{P_D,P_\chi\}\) and the closed form above. Then \(P_D(0)=0\), \(P_D(\theta)>0\) for \(\theta\in(0,\pi/2]\), and \(P_\chi(\pi/2)=0\), \(P_\chi(\theta)>0\) otherwise. Also \(L(\theta)-L(0)=(r^4\cos^2\phi/4)\sin^2\theta\ge 0\). Hence \(\min_\theta J(P_D,\cdot)=w L(0)\), attained at \(\theta=0\). And \(\min_\theta J(P_\chi,\cdot)=w L(0)\) if and only if \(w=0\) or \(\cos\phi=0\), because equality needs \(P_\chi(\theta)=0\) and \(L(\theta)=L(0)\) together, which is \(\theta=\pi/2\) and \(\cos\phi=0\) when \(w>0\). So at stake 0, and for every stake when the observable is fully complementary, both prices attain the same minimum. The price is not unique. When \(w>0\) and \(\cos\phi\neq 0\), this two-element menu does pick \(P_D\). That pick is a fact about a menu that excluded the zero price. Stop 2 puts the zero price back, and the pick ties again.

**KNOWN, not a derivation.** If "admissible" is strengthened by the four axioms of Wilming, Gallego, and Eisert, *Entropy* 19:241 (2017), doi `10.3390/e19060241`, the functional of a pair with full-rank second argument is a positive multiple of Umegaki \(D(\rho\|\sigma)\). They state that no subset of the four axioms is enough, and that Rényi divergences meet the first three. The stopping rule applies: that uniqueness is adopted, not derived from the minimum. It still does not choose the second argument. The pinch sets it to \(\Phi(\rho)\). Holevo information of an ensemble averages \(D(\rho_x\|\bar\rho)\) to the barycenter. A Gibbs reference is their free-energy reading. Three contractions, one divergence.

## Route B. Selection under the ruin cap

**Route.** Let lineages carry different quantum record prices. Eliminate a price when the design that minimizes it misses the ruin cap. Ask whether one price remains.

**Assumes.** Copying favors lower cost once a cost is named (`theory/SELECTION_AXIOMS.md:23-27`): a design that cannot cover the named \(J\) shrinks or is eliminated, and A2-L is the map \(m=m_0-\alpha J\) for that same \(J\). The ruin cap is \(P(\mathrm{ruin})\le\varepsilon\), outside the sum (`theory/REPRESENTATION.md:96`). Ruin, when it is a tail of the currency reserve, depends on the loss and the reserve. It does not depend on which information functional is written beside the loss.

**Where it stops.** The cap removes designs. It does not rank the functionals those designs were minimizing.

**Status. PROVED (in-model).** If the feasible set \(F=\{x:P(\mathrm{ruin})(x)\le\varepsilon\}\) does not depend on the price, and \(F\) is nonempty, then every price whose minimizer over \(F\) exists is still feasible. Nothing has been eliminated. Draft #252 sets the cap slack (`PREREG.md:36`), so neither \(P_D\) nor \(P_\chi\) is removed there. Selection among the survivors needs a common \(J\). `theory/SELECTION_AXIOMS.md:23` uses \(J\) as already defined and does not reopen the term list. Two functionals are two maps \(m=m_0-\alpha P\). There is no shared \(\alpha\) until one of them is the currency. Revealed costs recover price ratios of an observed design (`theory/REVEALED_PRICES_2026-11-21.md:7-8`). A ratio is a ratio of coordinates the cost already contains. It does not name a coordinate that was never in the sum. Theorem R2 is the same shape of obstruction, already proved for classical objectives: Kelly growth and the Lundberg objective both stay solvent, and their argmins differ (`theory/REPRESENTATION.md:157-162`). A solvency filter does not leave one objective.

Forcing a common currency and then dropping the price with the higher minimized cost is Route A again. Route A ties.

## Route C. R1's axioms on a GPT state space

**Route.** Replace the classical sample space in A6 by a general probabilistic theory, and take the operational limit of the same axioms: the entropy defined by measurements, the entropy defined by decompositions into pure states, and the large-copy properties (additivity, subadditivity) that A5 and A6 use.

**Assumes.** A1–A5, A7, and A8 are unchanged. A6's classical hypotheses are dropped, and the state is a GPT state. No quantum entropy is added as an axiom at the start.

**Where it stops.** The operational constructions do not return one functional. The step that would make the entropy unique inside quantum theory is a known theorem, and it still does not name the record price.

**Status.** The separation is **KNOWN**. Barnum, Barrett, Clark, Leifer, Spekkens, Stepanik, Wilce, and Wilke, *New Journal of Physics* 12:033024 (2010), doi `10.1088/1367-2630/12/3/033024`: measurement entropy is the minimum Shannon entropy over tests; mixing entropy is the infimum of Shannon entropies over decompositions into pure states. They coincide in classical and quantum theory, where they are Shannon entropy and von Neumann entropy. They differ in general. In their firefly example a pure state has mixing entropy 0 and measurement entropy 1, and a mixture has mixing entropy 1 and measurement entropy 0. Equality of the two (their word: monoentropic) is an extra constraint. Short and Wehner, *New Journal of Physics* 12:033023 (2010), doi `10.1088/1367-2630/12/3/033023`, give one measure that reduces to Shannon entropy and to von Neumann entropy, and show that in a theory with non-local boxes no conditional entropy that is reasonable in their sense is subadditive. A5's additivity and A6's subadditivity therefore do not extend together off the classical case. Debreu still needs the coordinates to be intervals before it prices them (`theory/REPRESENTATION.md:84`). A GPT state does not supply those intervals.

**KNOWN, not a derivation.** Restricting the GPT to quantum theory and adopting Ochs, *Reports on Mathematical Physics* 8:109–120 (1975), doi `10.1016/0034-4877(75)90022-1`, fixes von Neumann entropy up to scale as a measure of dispersion. The publisher abstract says the postulates have no direct bearing on information theory. The postulate list inside the article was not re-read. Adopting Wilming, Gallego, and Eisert, cited in Route A, fixes Umegaki relative entropy of a pair. The stopping rule applies to both: they are adopted axioms, not a consequence of R1. After either adoption the record contraction is still open, by the copy-versus-noise pair in Route 1. Shannon's classical uniqueness, the one A6 uses, remains Aczél, Forte, and Ng (doi `10.2307/1426210`, re-checked on Crossref this date; `theory/REPRESENTATION.md:58`). It is a theorem about finite alphabets.

## Model implications

- **Model implication.** If a quantum coordinate is required to extend A6, then on classical diagonal records it matches \(I(W;M)\) up to one scale \(a>0\). The pinch and a pure dimension price fail that match. A pinch term can still sit beside the mutual information. Whether it is in the sum is the coordinate-list choice R1 does not make (`CORE.md:52`).
- **Model implication.** On draft #252's complete-dephasing menu, restricted by hand to \(\{P_D,P_\chi\}\), with \(w>0\) and \(\cos\phi\neq 0\), the joint minimum is the pinch price (Route A, stop 3). With the zero price put back, that design is also optimal at price zero. The price is not identified.
- **Model implication.** For a classical-quantum state \(\rho_{XB}=\sum_x p_x |x\rangle\langle x|\otimes\rho_x\), the quantum mutual information built from von Neumann entropy equals the Holevo quantity of the ensemble. **ELEMENTARY** given \(S\). It is not a consequence of A1–A8. Draft #252's \(P_\chi\) is the mutual information after the measurement (`PREREG.md:34`).
- **Model implication.** On draft #253's singlet menu the A6 coordinate is identically zero (`theory/COMPOSITE_CONTEST_2026-11-24.md:56` on that branch). Selection under a slack or silent cap cannot see it (Route B). Charging \(\lambda\ln K\) adds an essential coordinate. R1 does not choose the list.

## Why there is no script

Route A's comparison is the sign of \(h'\) and the closed form already locked on draft #252. A grid would re-check that sign. It would not define the admissible set, and it would not turn the tie at stake 0 into a unique price. Route B is a feasibility split: the cap does not read the functional. Route C is the published separation of two GPT entropies. None of the three fails by a draw from a seed, and none is cheaper than the identity above. No preregistration and no run.

## Puzzle

Route 1 is missing a naming axiom. Route A is missing a definition of "admissible" that excludes the zero price without already naming the functional, and the natural strengthening (Wilming's four axioms) is KNOWN and still leaves the contraction open. Route B is missing a fitness that is not the disputed functional. Route C is missing an operational property that measurement entropy and mixing entropy share on a general state space; the papers above show they do not share one. A1–A8 and the ruin cap do not state any of those missing sentences.
