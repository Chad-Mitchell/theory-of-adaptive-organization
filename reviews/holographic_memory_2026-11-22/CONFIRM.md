# Confirm: holographic memory, 22 November 2026

CONFIRM: READY

Verdict: READY. Every item in the hostile review is fixed at `819b240`, and the capacity-limited claims recompute. The limits recorded below are the definition of a copy, the failure law behind the printed chances, and the git record of the prediction.

Independent read of draft PR #186 at head `819b24093175331127940d567d9ce285bd64439f` on `holographic-memory-2026-11-22`. The base of that pull request is `main` `6340b177bae94074d90bdbb3a2bfaad0e4915d90`. That branch was not edited. This file is the only change against current `main` `65f8703ccc514686cb9623e9dc765558e4f71e24`. The text reviewed is `theory/HOLOGRAPHIC_MEMORY_2026-11-22.md` at `819b240`, together with `OPEN_WORK.md` row T41, `theory/holographic_memory_checks/memory_checks.py`, and `theory/holographic_memory_checks/crossref.out`. The repair answers `reviews/holographic_memory_2026-11-22/HOSTILE_REVIEW.md` on `review-holographic-memory-2026-11-22` (PR #187, head `80afe9acecd7f19285d3ff2a749ae5d6736d8236`), which read the earlier head `bd2bfd76ab6cc78fdc0ef0b8185cc3706181862c`.

The capacity arithmetic below was recomputed in a separate script. It does not import `theory/holographic_memory_checks`. Closed forms are exact fractions. Failure masks were enumerated. This pass did not re-fetch the Crossref records; the revision drops the one unused reference and leaves the others as the review checked them.

## Protected files

`git diff origin/main 819b240 -- THEORY.md CORE.md README.md` is empty, and the same diff against the pull request's base `6340b177` is empty. The three files are byte-identical to current `main` and to that base: 165741, 18262, and 9061 bytes. The hypothesis sentence is present once in each file, with the same bytes, including the bold markers:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

The same bytes appear once in the note. The note does not edit `THEORY.md`.

## Hostile-review items

**B1.** Fixed. Section 4 puts the copy next to the split at the note's heat and upkeep. With \(V=4\), installed precision \(\mu=3\), failure probability \(0.2\), upkeep \(0.5\), and stake \(1\), heat charged once:

| Design | Count | \(P(\mathrm{error}>1.5)\) | Expected error | Cost |
|---|---|---|---|---|
| Copies of one full memory | 2 | \(0.04\) | \(1.12=28/25\) | \(5.12=128/25\) |
| Copies of that memory | 7 | \(1.280\times 10^{-5}\) | \(1.000038\) | \(7.500038\) |
| Split, cheapest feasible count in \(1,\ldots,20\) | 7 | \(0.033344\) | \(1.200585\) | \(7.700585\) |
| Two trackers, each paying \(\mu=5/3\) | 2 | \(0.04\) | \(1.6\) | \(5.933333=89/15\) |

On a draw with \(i\) units up, the split keeps precision \((i/n)\mu\) and the copy keeps \(\mu\) whenever \(i\ge 1\). The copy error is at most the split error on every such draw, so the same count, precision, failure probability, upkeep, and stake give the copy a cost at most the split's. The degradation identity stays: at \(V=4\), \(\varepsilon=1\), \(f=1/4\), the split error is \(16/13\) and item erasure is \(7/4\). On the heat grid \(D\in\{1,2,4,8,16\}\) and \(\mu=0.5\times 1.12^{n}\) for \(n=0,\ldots,47\), stake weight \(1.5\), the split-only minimum moves from heat \(1.391420\) to heat \(2.189426\). A one-memory copy on that heat rule, expected heat \(\mu(1-p^{n})\), meets the cap at \(n=2\) and \(\mu=5/3\) with expected heat \(1.6\) and cost \(4\). The note labels the reading that the cap selects the split as **FAILS**.

Both degradation curves increase in the failed fraction. Inside the Gaussian mean-square class, removing a positive semidefinite piece of precision raises the posterior covariance in the Loewner order, and the mean-square loss does not fall. An error that falls when a part is lost is labeled **CONJECTURE**, outside that class. The split's cost as a function of the failed fraction has positive second derivative \(2wV\mu^{2}/(1+(1-f)\mu)^{3}\). At stake weight \(1.5\) and \(V=4\) the healthy minimizer is \(\mu=\sqrt{6}-1=1.449490\), cost \(2\sqrt{6}-1=3.898979\).

**S1.** Fixed. The opening and the geometry paragraph say the alignment is what any separable precision cost does on an isotropic Gaussian, that the factor-\(s\) window is that shared counting shape, and that the heat is the price whose error falls as \(w^{-1/2}\), rises as \(\sqrt{a}\), and whose minimized cost grows like \(\sqrt{w}\). The nat price falls as \(w^{-1}\), misses the drift, and has minimized cost \((\kappa/2)(1+\log(2wV/\kappa))\).

**S2.** Fixed. The expected error of one random coordinate at heat \(4\) on \(K=20\) is \(K-4/5=19.2\). The mean of \(400\) draws at seed \(2\) is printed as \(19.2291\), and the sentence calls it the sample. At full support, seed \(4\) is one matrix at \(3.942262\), and the mean over \(2000\) codebooks is \(4.079182\).

**S3.** Fixed. The two-slot sentence points at the ordering in Proposition M-task. At weights \((4,3,0.2,0.1)\) and stake \(1\), the item-aligned cost is \(5.764102\), the all-ones axis is \(7.176851\), and the two-heavy axis \(u=(1,1,0,0)/\sqrt{2}\) is \(2\sqrt{3.5}+2.8=6.541657\). Both shared axes sit above the item-aligned cost. The **FAILS** bullet names both axes.

**S4.** Fixed. The opening, §5, and T41 call \(4.141947\times 10^{-12}\,\mathrm{W}\) the floor at drift \(1\) per second, rank \(10^{9}\), \((v-\varepsilon)/\varepsilon=1\), and temperature \(300\,\mathrm{K}\). Boltzmann's constant times \(300\,\mathrm{K}\) is \(4.141947\times 10^{-21}\,\mathrm{J}\). A finite-rate memory sits above the floor; the two springs at rate \(10^{5}\) have heat \(5.39980915\) against static rate \(5.40000000\). T41 does not say the geometry matches superposition and compressed sensing as one claim. It says the alignment is the separable-precision fact and that the heat is distinguished by the two slopes.

**S5.** Fixed. Burak and Fiete are not in §9. The crossref log keeps the fetched record and says it is not cited. Next to the chances \(0.200000\), \(0.180800\), and \(7.003561\times 10^{-3}\), the note says the chance is not monotone in the count: \(8\) units give \(0.056282\) and miss the cap, and the cheapest feasible count on this cap is \(7\).

## Capacity-limited units

The new class, stated before the printed costs: each unit installs a precision \(\varphi\in(0,c]\) and pays that precision as heat, plus upkeep \(h\). Units fail independently with probability \(p\). A common shock of probability \(\beta\) downs every unit and otherwise leaves the independent failures. The cost is heat plus upkeep plus \(w\) times expected error. The cap is \(P(\mathrm{error}>\varepsilon_{\mathrm{cap}})\le\varepsilon_{r}\). A copy reader uses the best surviving unit. A pool adds the survivors' precisions.

The worked scalar point is \(V=4\), \(\varepsilon_{\mathrm{cap}}=3/2\), \(\varepsilon_{r}=1/20\), \(p=1/5\), \(h=1/2\), \(w=1\). The four-item point uses the same \(p\), \(h\), and \(w\), with cap level \(2\) and \(c=1/2\). Those three parameters are the ones that reproduce the printed chance \(0.027200\).

**Pool against the non-pooling reader, same units.** On a draw, the pool's precision is the sum of the survivors and the copy's precision is the largest survivor, or zero if none survive. The sum is at least the largest term, so the pool's error is at most the copy's on every mask. Heat and upkeep are charges on the installed units, so they match. The pool's cost is therefore at most the copy's, at every stake and every failure law. Enumerating every mask for equal precisions in \(\{1/10,1/2,5/3,3\}\) at counts \(1,2,4,7\), and for three unequal lists, gave \(636\) masks and no reversal.

At \(\varphi=5/3\), two units: the copy costs \(89/15=5.933333\) and the pool costs \(217/39=5.564103\), with expected errors \(8/5\) and \(16/13\).

**One-unit copy.** The up-state error is \(V/(1+c)\). This is at most \(\varepsilon_{\mathrm{cap}}\) exactly when \(c\ge V/\varepsilon_{\mathrm{cap}}-1\). At the worked cap that bound is \(5/3\), and the up-state error equals \(3/2\). The cap is a strict exceedance, so equality meets the level, and the ruin probability is then the probability that every unit is down. At \(c=1/2\) the up-state error is \(8/3>3/2\), and the all-down error is \(4\). Every draw exceeds \(3/2\), at every count, under every joint law of failures. No number of non-pooling copies meets the cap.

A pool can. Three units at \(c=1/2\) still have error \(8/5>3/2\). Four have error \(4/3\). Under independent failures the smallest count with \(P(I<4)\le 1/20\) is \(7\), at chance \(0.033344\).

**Common shock.** On the shock draw every unit is down, both errors equal \(V\), and the pathwise bound holds with equality. If \(\beta>\varepsilon_{r}\), every design of these units has ruin probability at least \(\beta\). At \(\beta=0.06\) and two units with failure probability \(0.2\), both the copy and the pool have ruin probability \(0.097600\).

**Sum of four items.** Aimed at the sum, total precision \(\Phi\) has error \(4/(1+\Phi)\). Spread across the items, the minimum sum of item errors is \(16/(4+\Phi)\). The aimed error is the smaller one at \(\Phi\in\{1/2,1,4,8\}\). All-up item error is at most \(2\) only for \(\Phi\ge 4\). At \(c=1/2\) that needs at least \(8\) units. With heat equal to precision and upkeep \(1/2\), every feasible item design pays heat plus upkeep at least \(8\). This floor does not use the failure law: an all-up error above \(2\) leaves the error above \(2\) on every draw.

The aligned pool of \(4\) units, each at precision \(1/2\), first meets the independent-failure cap: ruin when fewer than two are up, chance \(17/625=0.027200\), expected error \(4948/3125=1.583360\), cost \(17448/3125=5.583360\). That full cost sits under the item floor of \(8\).

Four units pooled on each item: \(16\) units, the same expected error \(4948/3125\), because four times the expected error of one item with four units equals the expected error of four units aimed at the sum. Cost \(54948/3125=17.583360\). The ruin probability is \(1893887937/152587890625=0.012411784\), which rounds to the printed \(0.012412\). On one through twelve units per item, this is the cheapest symmetric design that meets the cap.

## What is distributed, and what is replicated

A pool and a non-pooling copy, in this section, are two readers of one installation. Distributed means the survivors' precisions add: each unit observes the same functional, and the posterior precision is the sum. Replicated means the reader keeps the best survivor and discards the others. Those are different readers. The comparison is not two names for one design.

A copy that is allowed to add precisions inside itself is a pool. Calling that object a copy and then comparing it with a pool would be a relabeling. The note's definition does not do that. If several such pools are built and the outer reader keeps only the best pool, the grand pool of the same units still holds at least as much precision on every mask, because the sum of every survivor is at least the sum inside the best subpool. Under this error model, replication of pools does not beat one pool of the same units.

The \(17.583360\) design is four units pooled on each item. The note calls it that. T41 calls the same design "item copies." A non-pooling reader on each item, at \(c=1/2\), has all-up sum error \(8/3>2\) and meets cap level \(2\) at no count. The number \(17.583360\) is the pooled item design.

The pathwise bound is decoder dominance on a matched installation. It is genuine, and it is the statement that a reader who may use every survivor is at least as accurate as a reader who keeps one, at the same heat and the same upkeep.

## Correlation, and a per-unit cost other than the floor

The pathwise bound and the matched-installation cost bound do not use independence. They hold for every joint law of the failure masks.

The printed chances and the costs \(5.583360\) and \(17.583360\) are independent-failure numbers. A common shock of probability \(1/25=0.04\), with idiosyncratic failure probability \(1/6\) so that the marginal failure rate stays \(1/5\), raises the four-unit aligned ruin probability from \(17/625\) to \(1/18=0.055556\). Five units then meet the cap, at cost \(10942/1701=6.432687\), which is still under the item floor of \(8\). A shock above \(0.05\) leaves both designs infeasible, as the note says. The sentence that the four-unit pool meets the cap is the independent-failure sentence.

The one-unit threshold and the \(c=1/2\) impossibility are statements about the up-state error. They do not use the cost, and they do not use the dependence.

Any installation charge \(u\) per unit, the same for both readers, preserves pool against copy on a matched installation, whether or not \(u\) equals the floor \(\varphi+h\). The item floor becomes \(8u\). The four-unit aligned cost \(4u+4948/3125\) stays under that floor whenever \(u>4948/12500\), about \(0.395840\). The stated charge \(u=1\), a charge above the floor at \(u=3/2\), and upkeep alone at \(u=1/2\) are all in that region. At \(u=1/5\) the four-unit full cost sits above \(8u\); re-optimizing the count, the aligned design still costs less than the symmetric item design (\(2.369051\) against \(4.783360\)). The same direction holds at \(u=1/10\).

A meter that charges the precision the reader admits, and still charges upkeep on every installed unit, is a different accounting. At the two-unit point \(\varphi=5/3\) that meter gives the copy cost \(4.2\) and the pool cost \(191/39=4.897436\). The note charges every installed precision. Under that charge the same pair stays at \(5.933333\) and \(5.564103\).

Adding precisions assumes independent observation noise. With correlated noise the optimal pool can still discard units, so its error remains at most the best single unit's. A numerical pair with noise correlation \(0.9\) has optimal-pool variance \(0.767677\) against the best single unit at \(0.8\), while the sum of the two precisions overstates the joint information (\(1.052632\) against a nominal \(2\)). The worked error \(1.583360\) is the independent-noise figure.

## Prediction and the git record

`bd2bfd7` (2026-11-22 19:02:36 +0000) has neither the capacity section nor the search. `819b240` (2026-11-22 19:40:42 +0000) introduces both. There is no commit between them. The prediction paragraph in the note stands above the costs the checks print. The checker comment stands above the search. That is source order inside one commit. It is not a prediction recorded in an earlier commit. Section 6 says nothing in the note is a preregistration. The inequality named in the prediction is the sum-versus-max argument in that same paragraph, so the result does not rest on the timing.

## Labels and wording

The proved propositions name the class and carry the algebra the checks recompute. The capacity bound is that short argument; the note presents it as a prediction and then prints the costs, and the reverse sentences are labeled **FAILS** with the worked numbers on the page. The conjecture label for an error that falls under part loss matches the Gaussian bound. The phone sentence is **METAPHOR**, and the watt figure is the floor under the assumptions in §5. GTAO is named as the theory in this repository.

A word search of the note and of the T41 row finds no "bill," "kill," or "verdict," and no "theory of everything." The two substrings of "bill" in the note are the word "billion."

## Checks at `819b240`

| Command | Result |
|---|---|
| `nice -n 19 python3 theory/holographic_memory_checks/memory_checks.py` | PASS 96, FAIL 0. Prints `CAPALIGN N=4 P=0.027200 E=1.583360 J=5.583360` and `ITEM n_per=4 P=0.012412 E=1.583360 J=17.583360` |
| `nice -n 19 python3 tools/check_consistency.py` | PASS, wording FAILs 0 |
| `nice -n 19 python3 tools/check_open_work.py` | PASS, 0 missing |
| `nice -n 19 python3 -m pytest -q tools` | 256 passed, 1 skipped (`tools/test_lean.py:101`, Lean 4 / lake is not installed), 310.69 s |

No lake build was run. The suite ran with NumPy 2.5.5, SciPy 1.18.1, SymPy 1.14.0, and pytest 9.2.0. The memory-check script on that NumPy prints the same 96 passes and the same capacity line.

CONFIRM: READY
