# Hostile review of draft PR #206

**VERDICT: NEEDS-FIXES.**

Reviewed head `9cf615f622d617da202ffe5b3c05fc205c22d887` on `front-refresh-2-2026-11-22`. That is the head of draft PR #206. `origin/main` at review time is `81fd1a1`, the parent of this commit. This review does not edit that branch, does not push to it, and does not merge.

The page was checked sentence by sentence against `OPEN_WORK.md` T41–T46, `measurement/CLAIM_MAP_v2.md` v2.88, `THEORY.md` v2.9, the notes and reviews those rows cite, and draft PR #203 at head `a79d7b6d40623794f93c2898582d64bbf6153486`. #203 is open, draft, and not merged. #192 is open, draft, and not merged.

Six fixes. The hypothesis sentence, the worked-class formulas, the five remaining-work items, both DOIs, and the links hold.

## What holds

The hypothesis sentence is byte-identical in `README.md`, `CORE.md`, and `THEORY.md`:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

On the map the same bytes are split after the colon. Joined with one space, they match. Each maintained file has one copy. The sentence is labeled a hypothesis. The checker accepts that labeling.

`README.md` is 1330 words. The advisory reference is 900. That warning is not a failure, and this review does not ask for a cut. The judgment below is about what a reader can hold.

Wording on the three front-page files: cost, throughout. No "bill". No "theory of everything". No "kill". No field verdict. The only "law" of this project is inside the hypothesis sentence. "Conditional law" in the boundary paragraph is a probability law. `tools/check_consistency.py` reports wording FAILs 0.

These claims match the record and should stay:

- The heat-plus-stake cost with the ruin cap beside the sum, in the class the formula paragraph names.
- One OU signal: floor \(kT\,a(v-\varepsilon)/\varepsilon\), approached in a limit; minimizing cost \(2\sqrt{kT\,a\,v\,w}-kT\,a\) above the blind stake \(kT a/v\).
- Geometric ladder, each mode scored on its own: \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\), with no per-layer \(h\). Sum of modes: one rank-one memory. Telegraph: the heat infimum is \(kT\) times the flow \(\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\).
- T41: the per-site heat floor scales with the volume; a named cut costs about \(13.61\) per cut site against a lower bound of \(13\); the name "holographic" adds no prediction. T42: a shared memory costs less when the decision is a sum, and it ties or costs more when every item is read on its own.
- T43: identical units at rate 1 cost \(15.473978\) with ruin probability \(0.020940\), against the inadmissible zero at cost \(16\). The heterogeneous arm's grid minimum stays at no shock, cost \(13\). That comparison is a puzzle at this cap. Heat is proportional to precision, and the admissible points keep the more precise units.
- T44: in an equilibrium Gaussian field, the conditional law given the region and the blanket equals the law given the blanket; the interior is not sufficient; the matching channel costs at most the Schur trace more. The integer \(5\%\) radius is \(2\) at \(\tau=1/2\) and at \(\tau=1\), ratio \(1\), because both crossings of the level \(0.05\) fall in \((1,2)\). The path of \(61\), the next test that preregistration named, returned \(2\) and \(2\). The smooth crossing is a separate statistic, ratio \(2.067863694520\), inside \([1.7,2.3]\).
- T45: \(J^*(8)=4.998066177768\). \(C(1/2)=5\) is the heat plus the sign loss at the frozen fraction, above \(\inf C=4.966383544211\). The crossing is near \(\theta=7.5267\). The next lock, if written, is a new preregistration scored against that floor. The drop along the minimizing probe is the price of a fraction falling as \(1/\theta\).
- T46 arithmetic, as arithmetic: unpriced gap \((q-2aP(a))\theta\), equal to \(0.171572875254\) at unit stake, unit drift, and unit variance; priced gap negative at every fraction at stake \(1\); at stake \(4\) the gap at the minimizing fraction is \(0.033889928154\). Feedback shrinks the stock and leaves the learning-rate heat fixed. The acting-loop run contained no prediction that could miss. The page does not call those decimals a risky test. `reviews/acting_loop_2026-11-22/CONFIRM.md` recomputed them.
- Optionality and antifragility as convex payoffs are credited to Taleb and Douady and to `theory/ROBUSTNESS.md`. A search of the repository finds the two routes side by side in `theory/ACTING_MEMORY_2026-11-22.md` and finds no theorem that makes the learning heat and an option one object. The note calls the financial name for the sign bet a metaphor. That paragraph is not a novelty claim.
- Both DOIs resolve on the Crossref API, fetched again for this review. `10.1103/PhysRevX.4.031015` is Horowitz and Esposito, "Thermodynamics with Continuous Information Flow", Physical Review X, 2014. `10.1080/14697688.2013.800219` is Taleb and Douady, "Mathematical definition, mapping, and detection of (anti)fragility", Quantitative Finance, 2013. The second record has no abstract. The convexity reading is the one `theory/ROBUSTNESS.md` §6 already uses.
- Every relative link in `README.md` and `CORE.md` resolves to a file on this head, including `figures/derivation_map.png`, `figures/face.png`, `LICENSE.md`, and both history copies. The cited sections exist: THEORY §3, `theory/GENERAL_FORM_PHYSICS_2026-11-22.md` §9, `theory/ACTING_LOOP_2026-11-22.md` §8, `theory/DYNAMICS.md` §2. The GitHub links for #203 and #192, and `https://x.com/torusflow`, return HTTP 200.
- The map's open box and its in-review chip match the page: non-Gaussian case, a real-data test, pull request 192, adopt the derivation after review, the \(5\%\) radius puzzle, \(J^*(8)\) just under \(5\), and #203 in review. #192's title is "Fractal world: cost tracks the named sites, not the dimension". This page uses none of its numbers. T40, adopting the physics display, is named in the cost section and again in CORE §6. The master equation is unchanged.
- Where the page and `THEORY.md` disagree, the page says `THEORY.md` governs. That sentence is the right one. Keep it.

T42, T43, T44, T45, and T46 are "not adopted" in `OPEN_WORK.md`. "Not adopted" means not copied into `THEORY.md`. The page's word **PROVED** can mean proved inside the named class, which is the sense CORE § "Status words" gives it, provided the sentence stays inside that class. The fixes below are the sentences that leave the class.

## F1. "Effectively complete" is wider than the worked class

`README.md` line 7 and `CORE.md` line 9 say: "Inside the Gaussian and linear class the mathematical core is effectively complete." The map's cost card says "Gaussian and linear class".

The proved class is narrower, and it is not only Gaussian. `theory/GENERAL_FORM_PHYSICS_2026-11-22.md` §3: an exogenous equilibrium Ornstein–Uhlenbeck signal, independent signals of that kind, or the two-state telegraph; mean-square loss, or Hamming error on the telegraph; the memory does not move the signal. The telegraph is in the class and is not a Gauss–Markov signal. A memory that moves its world is CX2 and is open. The closed-loop multi-rate plant is unsolved (`theory/ACTING_LOOP_2026-11-22.md` §8; CORE already says so). Equality at a finite memory rate is a limit. T40 is not applied, so the canonical equation is still the five-term display. "Effectively complete" covers that open ground.

The formula paragraph lower on the README already names the worked class. Keep that paragraph. Replace the opening claim so it names the same class.

README, replace the two sentences that begin "Inside the Gaussian and linear class":

```
The heat floor and its minimizers are proved in one class: an exogenous equilibrium Ornstein–Uhlenbeck signal, independent signals of that kind, or the two-state telegraph; a mean-square loss, or Hamming error on the telegraph; a memory that does not move the signal. The telegraph is in that class. Other Gaussian systems stay open, and other linear systems stay open, including a memory that moves its world. No system has been shown to qualify, so nothing on this page is a test from a real system.
```

CORE, replace the three sentences that begin "Inside the Gaussian and linear class" (the completeness claim, the pointer to §6, and "Evidence from real systems is thin."):

```
The heat floor and its minimizers are proved in the class named in §1. The telegraph is in that class. Other Gaussian systems stay open, and other linear systems stay open. The list of what stays open is §6. No system has been shown to qualify.
```

Map, in `figures/derivation_map.py`, replace the cost-card subtitle:

```
"Gaussian and linear class",
```

with:

```
"OU, independent OU, telegraph",
```

Then regenerate with `nice -n 19 python3 figures/derivation_map.py`.

"Evidence from real systems is thin" goes out with the same sentences. The record is that no system has qualified (THEORY §3; OPEN_WORK T35). A later paragraph already says a field result with no recorded qualification check is not a test. The opening should say that.

## F2. The five-term display is not the heat-plus-stake cost

README: "When the prices are linear, that cost is the five-term sum still printed as the canonical equation." The map: "Five terms, linear prices. Same cost."

CORE: "The five-term sum still printed in THEORY §3 is the same object when a growth maximizer is ranked by risk-neutral expected currency, the prices are linear and nonnegative, and ruin is a half-space cap (Lemma LY, **PROVED** in-model under H1–H3, `theory/GENERAL_FORM.md`)."

Lemma LY says a maximizer of \(\lambda=\mathbb{E}[\log W]\) is Pareto in a chosen bad vector, under H1–H3. It does not choose the vector. `theory/GENERAL_FORM.md` §0 and the paragraph after corollary LY-c say the corollary is a nonnegative linear cost in growth units for a score supplied from outside, and that this is not the master equation. GF3, which is proved in-model, says the nonnegative five-term sum with a half-space cap is the special case in which a Pareto front is ranked by risk-neutral expected currency. Growth and that currency have different argmins (V2, stated in the same §0). The ideal-gas comparison is that list of extra assumptions. It is a comparison with the Pareto front, not a derivation of \(J_{\mathrm{phys}}\).

`theory/GENERAL_FORM_PHYSICS_2026-11-22.md` §2: the heat-plus-stake sum is not corollary LY-c and is not the five-term master equation. IP5, "the master equation is the Lagrangian of the physical frontier", is **FALSE** in CLAIM_MAP section Y. §7 of that note replaces \(\kappa I_{\mathrm{mem}}\) with the bath heat, leaves \(hK\) off the floor, keeps \(w\,\mathbb{E}[\ell]\), leaves a separate read price assumed, and leaves \(L\) and the ruin cap outside \(J_{\mathrm{phys}}\).

CORE's table then puts "\(L\), the ruin cap" in one cell and says both "stay outside this \(J\)", under a display that still contains \(L\). \(L\) is outside the heat-plus-stake sum and inside the five-term display. The ruin cap is outside both.

README, replace the sentence "When the prices are linear..." and the five sentences that follow the five-term display, through "stay assumed.":

```
THEORY §3 still prints that five-term sum. The sum is a different object. The bath heat replaces \(\kappa I_{\mathrm{mem}}\). The floor on the heat is \(kT\) times the learning rate (Horowitz and Esposito 2014, doi 10.1103/PhysRevX.4.031015, checked on Crossref 22 November 2026). \(hK\) sits outside that floor. \(w\,\mathbb{E}[\ell]\) survives, and temperature does not set the stake \(w\). A continuous sensor's read is already inside the heat. A separate read price \(A\) stays assumed. The link price \(L\) stays assumed and stays outside the heat-plus-stake sum. The ruin cap stays assumed and stays beside the sum.
```

Leave the displayed five-term equation in place, introduced as the display THEORY still prints.

CORE, replace the paragraph that begins "The five-term sum still printed in THEORY §3 is the same object":

```
The five-term sum is the display THEORY §3 still prints. It is a different object from the heat-plus-stake sum. Lemma LY, proved in-model under H1–H3 (`theory/GENERAL_FORM.md`), says a growth maximizer is Pareto in a chosen bad vector. It does not choose the vector. The five-term sum is the special case in which a Pareto front is ranked by risk-neutral expected currency, the prices are linear and nonnegative, and ruin is a half-space cap. Growth and that currency have different argmins. The ideal-gas comparison in that note is this list of extra assumptions. Occupation of the front is open. IP5, the claim that the master equation is the physical frontier, is false (`theory/GENERAL_FORM_PHYSICS_2026-11-22.md` §2).
```

CORE, replace the table row that begins `\(\kappa I_{\mathrm{mem}}\)` through the row that begins `\(L\)`:

```
| Term | Inside the proved class |
|---|---|
| \(\kappa I_{\mathrm{mem}}\) | Replaced by the bath heat \(\dot Q\). Floor: \(kT\) times the learning rate. The stock rental is not the coordinate. |
| \(hK\) | Outside the floor. A constant \(h\) still on the books is excess over the heat. |
| \(w\,\mathbb{E}[\ell]\) | Survives. \(w\) stays assumed. |
| \(A\) | Stays assumed as a separate summand. A continuous coupling's read is inside \(\dot Q\). |
| \(L\) | Stays assumed, and stays outside the heat-plus-stake sum. The five-term display still prints it. |
| Ruin cap | Stays assumed, and stays outside both. |
```

Map, replace:

```
"Five terms, linear prices. Same cost.",
```

with:

```
"THEORY still prints five terms. A different object.",
```

Regenerate the png with the same command as in F1.

## F3. One store per time scale contradicts the rank-one sum

README, cost paragraph: "a sum of modes is carried by one rank-one memory." README, layers: "One real time scale needs one store, or none when the stake is small."

The second sentence is the per-mode ladder, and only when each mode is scored on its own (`theory/INFO_PHYSICS_GENERAL.md`, OPEN_WORK T39). On the sum loss the heat-optimal memory has one coordinate for every mode. The map card "One store for each time scale the stake can pay" repeats the wide sentence and drops "or none".

CORE already says "each scored on its own" and already says the closed-loop spacing, reversion \(a+bK\), is a conjecture and that the multi-rate plant is not solved. README never says the second thing. A reader of README alone will take the ladder count as the count under feedback.

README, replace the layers paragraph:

```
**Layers, along time.** When each mode is scored on its own, one real time scale needs one store, or none when the stake is small. On the geometric ladder the count is the formula above. When the loss is the error in the sum, one rank-one memory carries the modes. [`figures/face.png`](figures/face.png) is the placement: for each time scale, local, shared, both, or neither. Spacing those stores under a closed loop is unsolved.
```

Map, replace the layers line:

```
("LAYERS", "One store for each time scale the stake can pay."),
```

with:

```
("LAYERS", "Per mode: one store for a paid scale, or none."),
```

## F4. The unpriced gap is an amount, and the priced gap at stake 4 is one fraction

README: "closed-loop regulation is cheaper than sensing alone by the factor \(0.171572875254\) at unit stake and unit drift."

`theory/ACTING_LOOP_2026-11-22.md` §0: the gap is \((q-2aP(a))\theta\). At \(q=a=1\) the coefficient is \(0.171572875254\). Sensing alone costs \(q\theta\). At unit variance that cost is \(1\), and the closed loop is cheaper by \(0.171572875254\). "By the factor" reads as a multiplier. CORE states the product \((q-2aP(a))\theta\) and then the coefficient. That CORE sentence can stay.

README also says the priced gap "equals \(0.033889928154\) at stake \(4\)". CORE says the gap "is \(0.033889928154\) at stake \(4\)". The note's figure is the gap at the minimizing fraction \(0.856768708291\). At stake \(1\) the priced gap is negative at every fraction. Those are different quantifiers.

README, replace the acting paragraph's first two sentences:

```
**Acting.** With the channel unpriced, closed-loop regulation is cheaper than sensing alone by \((q-2aP(a))\theta\). At unit stake, unit drift, and unit variance that gap is \(0.171572875254\), against a sensing-alone cost of \(1\). With the heat and the probe charged, the gap is negative at every fraction at stake \(1\). At stake \(4\) the gap at the minimizing fraction is \(0.033889928154\).
```

Keep the rest of the paragraph, from "Feedback shrinks".

CORE, in the acting paragraph, replace "and is \(0.033889928154\) at stake \(4\)" with:

```
and at stake \(4\) the gap at the minimizing fraction is \(0.033889928154\)
```

Map, replace the acting line. The card states the priced case as the whole theorem, and "the look" is not a term on the page.

```
("ACTING", "Close the loop when the stake covers the look."),
```

with:

```
("ACTING", "Priced channel: only if the stake covers the probe."),
```

## F5. Three cards state a wider theorem than the text

The legend says PROVED means "inside the named class". The yield cards do not name a class. Three of the sentences are wider than the prose above them.

**Boundary.** The text restricts the claim to an equilibrium Gaussian field. CORE also records the negative result: a continuous-time heat kernel is positive at every distance, so no finite shell screens (`theory/BOUNDARY_SUFFICIENCY_2026-11-22.md`). The card says "The blanket screens a decision made outside."

Replace:

```
("BOUNDARY", "The blanket screens a decision made outside."),
```

with:

```
("BOUNDARY", "Gaussian field: the blanket suffices outside."),
```

**Rebuild.** §8 of the acting-loop note lists "replaces the part when holding it is dearer than the failure" among the clauses that are conjectures, or theorems from a class that did not contain the action. The proved comparison is the identical-unit arm. The heterogeneous arm is the puzzle: the grid minimum stays at no shock. The card states the general rule and marks it PROVED. That is a synthesis presented as a theorem.

Replace:

```
("REBUILD", "Replace a part when holding it costs more."),
```

with:

```
("REBUILD", "Identical units can cost less under the cap."),
```

**Spread** can stay: "One shared memory when the decision is a sum." The "when" is the proved case. The prose already adds the opposite case, every item read on its own.

**Option line.** The prose says a search finds no theorem that makes the learning heat and an option one object, and that the sentence is the hypothesis in another shape. The synthesis card says "Learning and an option, same cost." The first synthesis line, "The five sit on one cost.", matches the page's own status word and can stay. Replace the second line:

```
"Learning and an option, same cost.",
```

with:

```
"No theorem joins the learning heat and an option.",
```

Regenerate the png once, after F1, F2, F3, F4, and F5.

## F6. PR #203 is described as a proved result

#203 must be described only as in review. Head `a79d7b6` is right, the branch name is right, and the page says the pull request is not merged. The sentences after that treat the draft as a result: "Theorem R1′ is a representation theorem. The step proved on that branch is the \(b=0\) reduction... The risky prediction was met by one grid step... continuous gains \(0.23\) against \(0\). The gate was underpowered."

Those sentences track the draft's own abstract. They do not belong on this page. On `main`, `theory/ACTING_LOOP_2026-11-22.md` §8 still calls the extended cost a conjecture and says the scalar reduction is not Theorem R1 applied at \(b=0\). A front page that reports #203's step as proved has adopted the draft it says it has not adopted.

README, replace the whole "In review" section after the heading:

```
The acting derivation is in review: [PR #203](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/203), branch `cursor/acting-derivation-2d99`, head `a79d7b6`. This page does not adopt it, and it does not treat the pull request as merged.
```

CORE, replace the paragraph in "4. In review, and not adopted":

```
[PR #203](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/203) (branch `cursor/acting-derivation-2d99`, head `a79d7b6`) is in review. This page does not adopt it. The proposal diff is on that branch. It is not applied. This page does not treat the pull request as merged.
```

The map chip "IN REVIEW · acting derivation, #203" is the right grain. Leave it.

## Clarity

A reader who has not opened the notes can hold three things from the README, and then loses the thread.

What holds in the head: the hypothesis; one cost, heat of the memory's bath plus a stake on the decision loss, with a cap on the chance of ruin beside the sum; five uses of a minimum, joined as a reading rather than as one theorem; no qualifying system has been measured. The five names (layers, spread, boundary, rebuild, acting) are the right five, and the "what remains" list is the right list.

Where the page loses that reader:

- The opening says the mathematics is effectively complete in "the Gaussian and linear class" before the class is defined, and before the reader is told that THEORY still prints a different equation. F1 and F2 remove that.
- The five-term symbols arrive as an equation. \(\kappa\), \(h\), \(K\), \(A\), and \(L\) are not yet words. CORE's table is the right repair, once F2 splits \(L\) from the ruin cap. README's replacement in F2 does the same in prose.
- "Cheaper by the factor \(0.171572875254\)" will be read as a multiplier. The comparison is an additive gap of that size against a sensing-alone cost of \(1\). F4 says so.
- The rebuild decimals and the two puzzles are dense, and they should stay. The ordinary-language sentence is already in front of the digits: identical units under the cap can cost less than an inadmissible zero; both crossings of the level \(0.05\) fall in one bin, so the integer ratio is \(1\); \(5\) is the cost at a frozen fraction and the floor is lower, so \(J^*(8)\) can sit under \(5\). A reader can hold those three sentences without holding the field.
- The #203 paragraph, with R1′, \(b=0\), one grid step, and \(0.23\), is intelligible only after the derivation draft. F6 removes it. The in-review chip on the map is what the README should say.

CORE is the page a reader can finish. It separates a mathematical part from the hypothesis, defines the class before the formulas, and labels the closed-loop layer spacing as unsolved. Its failures are F1, F2, the stake-4 quantifier, and F6. After those, CORE can carry a reader who found the README's digits too thick.

## Checks

Run at `nice -n 19` from the repo root on head `9cf615f`, before this file existed. No lake build. NumPy \(2.5.5\), SciPy \(1.18.1\), SymPy \(1.14.0\).

| Command | Result |
|---|---|
| `python3 tools/check_consistency.py` | `RESULT: PASS`. FAIL 0. INFO on frozen records 29. README 1330 words, advisory reference 900. THEORY main text 11134 words, advisory reference 5500. Neither warning is a failure. |
| `python3 tools/check_open_work.py` | `RESULT: PASS`. Union missing from `OPEN_WORK.md`: 0 |
| `python3 -m pytest -q tools` | 261 passed, 1 skipped, 316.56 s, exit 0. The skip is `tools/test_lean.py:101`, "Lean 4 / lake is not installed". |

This file is not a maintained document. The wording fixes above stay inside the rules the checker enforces on `README.md` and `CORE.md`: cost, the hypothesis sentence left byte-identical, and no field verdict.
