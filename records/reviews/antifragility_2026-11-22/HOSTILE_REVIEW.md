# Hostile review of draft PR #191

**VERDICT: NEEDS-FIXES.**

Independent review of head `acff0820f17b83f04c336769524a0c5142f55a66` on `antifragility-turnover-2026-11-22`, three commits on parent `819b24093175331127940d567d9ce285bd64439f`. Sunday 22 November 2026. This review does not edit that branch, does not push to it, and does not merge. No `lake` build. Computations at nice 19.

The registration is clean, and the locked arithmetic holds. Identical stale units have an interior minimum of the mean-field cost at shock rate \(0.2646371727\), cost \(13.3545082433\), against \(16\) at no shock. The second derivative is exactly \(864/(9\sigma+1)^3\). The heterogeneous arm, with heat proportional to quality, has its minimum at rate \(0\), cost \(13\), and the heat jumps from \(5\) to \(7.6848632904\). The ruin cap rejects every unconstrained grid minimum. The comparison the cap leaves standing is the identical-unit admissible point: rate \(1\), cost \(15.473978\), ruin probability \(0.020940\), which is \(0.526022\) below the inadmissible zero at cost \(16\). The informative and uninformative admissible points sit above their zeros. The note leads with the unconstrained bowl and says the cap does not move the scores. That ranking is the repair. One sentence in §6, that a design will switch the memory off before it buys this cap, is false under the cap the note locked.

The hypothesis sentence is one copy in each of `THEORY.md`, `CORE.md`, and `README.md`, the same bytes at head, at the parent, and at `origin/main` `13eec9a`:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

SHA-256 of those three files is `91a527e4…`, `31e22703…`, and `042de9a4…` at all three commits. The turnover commits do not change them.

Recomputation did not import `theory/antifragility_checks/`. The homogeneous cost, the birth-death chain, and the ruin event \(\varepsilon>3/2\) were coded from `PREREG.md` and `ADDENDUM.md`. The committed `results.out` was then rerun from the author's script and matched byte for byte. NumPy 1.26.4. The reviewer's script is `recompute.py` in this folder.

## Registration

The history is linear and the prediction files are frozen.

| commit | committer time (UTC) | what it adds |
|---|---|---|
| `74e9b197e26a2b70d72503a3c1693f78ec7380c8` | 2026-11-22 20:03:58 | `PREREG.md` only |
| `5418177ecab32c43b143c519f6e82b84715d4d97` | 2026-11-22 20:08:28 | `ADDENDUM.md` only |
| `acff0820f17b83f04c336769524a0c5142f55a66` | 2026-11-22 20:24:39 | the script, `RESULTS.md`, `results.out`, `crossref.out`, the test, the OPEN_WORK row |

Author time equals committer time on each commit. Each parent is the commit above it. GitHub reports a valid signature on all three. The blob of `PREREG.md` is `abc87b00c7a91a113fb0c989d812b5a7c15d1716` at `74e9b19` and at the head. The blob of `ADDENDUM.md` is `270304f49a279b4dec1c53f37f39f512a7097a36` at `5418177` and at the head. No prediction text was edited after the computation. Neither file records an argmin, a grid value, or a Monte Carlo estimate. The simplified derivative \(864/(9\sigma+1)^3\) appears first in `RESULTS.md`.

P2's failure was an outcome the preregistration already named: if \(0<B<wv^2 cq/\delta\), the homogeneous lemma refutes monotonicity, and that refutation is of the control, while P1 stands or falls on its own arm. The note scores it that way and does not add a condition afterward.

## What holds

**The identical-unit minimum.** One quality \(q=1\), \(n=4\), \(c=1/2\), \(\delta=1\), \(B=\tfrac12+\tfrac12\ln 3=1.049306144334\). The threshold \(wv^2 cq/\delta\) is \(12\). Since \(0<B<12\),

\[
J'(0)=n\left(B-12\right)=-43.802775422664.
\]

The critical-point display and the derivative set to zero agree to \(6\times 10^{-17}\):

\[
u^\star=0.2092593658,\qquad \sigma^\star=0.2646371727,\qquad J(\sigma^\star)=13.3545082433.
\]

\(J(0)=16\). The one-unit replication is \(\sigma^\star=0.7939115180\), cost \(6.5158811825\), against \(8.5\). With \(B=0\) the cost falls from \(16\) at rate \(0\) to \(10.6961325967\) at rate \(20\), so the interior minimum uses a positive build cost. These are the note's digits.

**The second derivative.** At these numbers the addendum display collapses exactly:

\[
J''(\sigma)=\frac{864}{(9\sigma+1)^3}.
\]

It equals \(864\) at \(\sigma=0\) and \(864/181^3=0.000145706195\) at \(\sigma=20\), the right end of the locked log grid, which is the note's smallest value \(0.0001457062\). The display and the simplified form differ by at most \(9\times 10^{-16}\) on that grid. Every factor is positive, so the mean-field cost is strictly convex on \([0,\infty)\). The spread \(\{\sigma^\star/2,\ 3\sigma^\star/2\}\) raises the cost by \(0.2232577182\). The five Jensen gaps in the note's table match to the printed digit, including \(+0.0392014519\) for the cost on \(\{1,2\}\) and \(-0.1333333333\) for the realized flow on the same pair. A positive level of stress and a Jensen gain are different statements. The note says so, and the algebra agrees.

**The heterogeneous arm, on the locked coupling.** Informative failure, copy-with-mutation, drift. The stationary law on \(\{0,\ldots,4\}\) is independent of the scale of \(\sigma_s\). Exact balance holds. \(\mathbb{E}[k]=3.7899088603\), against \(n\pi=2\). Continuous heat is \(kT\,a\,v\,c\) times expected total quality, so the prior pays \(5\) and the selected law pays \(7.6848632904\). At rate \(0\) the cost is \(13\): heat \(5\), upkeep \(2\), mean square \(4\), stake-weighted term \(6\). At rate \(10^{-6}\) the cost is \(15.6848198582\). The jump equals the heat jump. Alignment has not moved, and the mean square is still \(4\).

On \((0,\infty)\) the smooth minimum is at rate \(0.24762\), cost \(13.162630\), which is \(0.162630\) above \(13\). The note's fine-grid point, rate \(0.25\), cost \(13.1627010412\), sits \(7\times 10^{-5}\) above that. Second differences on the step-\(1/20\) grid stay positive, smallest \(3.7\times 10^{-7}\). The grid minimum that includes rate \(0\) is at rate \(0\). P1 fails under the definition the preregistration locked. The score is the right score.

**The ruin-cap table.** \(\varepsilon>3/2\) if and only if the pool is below \(5/12=0.4166666667\). With drift and rate \(0\), alignment is \(0\), the error is \(4\), and the ruin probability is \(1\) on every such arm. An independent sample of \(400000\) draws, seed \(20261123\), agrees with the committed \(50000\)-draw table on every admissibility call:

| arm | their official grid min | their admissible point | this sample |
|---|---|---|---|
| identical units | rate \(0.3\), cost \(13.748899\), probability \(0.473560\) | rate \(1\), cost \(15.473978\), probability \(0.020940\) | rate \(0.3\), cost \(13.742993\), probability \(0.473033\); admissible rate \(1\), cost \(15.472495\), probability \(0.019800\) |
| informative | rate \(0\), cost \(13\), probability \(1\) | rate \(1\), cost \(15.566427\), probability \(0.027440\) | admissible rate \(1\), cost \(15.567875\), probability \(0.028577\) |
| uninformative | rate \(0.4\), cost \(11.262060\), probability \(0.638600\) | rate \(4\), cost \(22.311716\), probability \(0.040260\) | admissible rate \(4\), cost \(22.308924\), probability \(0.039753\) |

Rate \(0.7\) on the identical-unit arm has probability \(0.086740\) in the note and \(0.087582\) here, both above \(1/20\). Rate \(3\) on the uninformative arm has probability \(0.0567\) on both samples. The admissible argmins are stable. The identical-unit admissible point beats the inadmissible zero: \(15.473978<16\), a margin of \(0.526022\). The informative admissible point costs \(15.566427\), and the uninformative admissible point costs \(22.311716\), both above the zero-shock cost \(13\). The quality-observed row is the identical-unit chain once turnover is positive (their rate-\(1\) cost \(15.471038\), probability \(0.019980\)); its own zero is the stale binomial at cost \(13\), and \(15.471038>13\).

This admissible comparison is the load-bearing positive result. The heat result and the convexity result are the load-bearing negatives, and they hold: continuous heat stays \(8\) for identical units and \(7.6848632904\) on the selected branch, the stock rate rises, and a spread raises the cost. The unconstrained bowl at rate \(0.2646371727\) is a real minimum of the cost the preregistration told the script to score, and the cap the same file locked rejects it. Ruin probability \(0.47\) at the official grid minimum is the reason that bowl is not a design the constraint allows.

## The coupling, and the cap

The coupling is written in `PREREG.md` §1 before any number: installed precision is \(c q_i\), and a living unit pays heat \(kT\,a\,v\,c\,q_i\). Weak, in this class, means low installed precision, which means low heat. Selection that raises \(\mathbb{E}[k]\) from \(2\) to \(3.7899088603\) therefore raises the heat from \(5\) to \(7.6848632904\) at every positive stress, before alignment has moved. Section 0 names that mechanism. It is explicit. It is also what decides the unconstrained heterogeneous sign at the frozen cap.

Two diagnostics were run from the locked chain. They are not rescores of P1–P11. They are not in the author's script.

**Fixed heat.** Every unit pays the cap heat \(kT\,a\,v\,c\), total \(8\), and the stock is the stock of that installed precision. Quality scales the aim and the hazard only. The zero-shock cost is \(16\). The smooth minimum on \((0,\infty)\) is at rate \(0.236680\), cost \(13.548262\). That gain is inadmissible. The admissible grid point is rate \(1\), mean-field cost \(16.089610\), Monte Carlo cost \(16.1735\), probability \(0.02905\). It sits above \(16\), and above the identical-unit admissible cost.

**The frozen cap is where the coupled sign changes.** With the locked coupling, the mean-field gap between the positive-branch minimum and the zero-shock cost is negative for caps in \((0.06972,\ 0.44683)\) and positive outside that interval. At \(c=0.22\) the gap is \(-0.398\). At the frozen \(c=1/2\) the gap is \(+0.162630\). P1's failure is the failure at this cap. The diagnosis in §6, that precision has to be chosen with the turnover, is the right diagnosis. Arm A14 already shows why the stake, ignoring the cap and ignoring upkeep and build, installs at most \(3/32=0.093750\). That precision cannot meet the cap: four fully aligned units pool to \(0.375\), and the cap requires \(5/12=0.416667\). A diagnostic sweep under the cap, identical units, finds an admissible point the frozen cap misses. At installed precision \(1/4\) and rate \(2\), the mean-field cost is \(14.408952\) and the ruin probability on \(120000\) draws is \(0.0237\). The frozen admissible mean-field cost, precision \(1/2\) at rate \(1\), is \(15.397225\). Precision \(0.11\) has no admissible point on the locked grid.

## Citations, labels, wording

Crossref HTTP 200 for every DOI on the page, fetched again this session. Titles, years, venues, and author names match.

Taleb and Douady, *Quantitative Finance* 13 (2013) 1677–1689, DOI `10.1080/14697688.2013.800219`. Crossref has no abstract. The note's **KNOWN** sentence is limited to the title, and the concave-cost reading is attributed to `theory/ROBUSTNESS.md` §6, which is where that reading is written. Both limitations are accurate.

Calabrese and Baldwin, *Annual Review of Pharmacology and Toxicology* 43 (2003) 175–197. The Crossref abstract and the Europe PMC abstract both say hormesis is characterized by low-dose stimulation and high-dose inhibition. The **KNOWN** sentence matches that clause. Calling the cost curve hormesis is marked **METAPHOR**.

Paolicelli and coauthors, *Science* 333 (2011) 1456–1458. The Crossref abstract field is the one-line "A good brain needs a good vacuum cleaner." The scientific sentence is in Europe PMC, fetched again: microglia actively engulf synaptic material and play a major role in synaptic pruning during postnatal development in mice. The note's sentence matches that abstract, and the file says the abstract came from Europe PMC. **METAPHOR** for the name inside this class is the right label.

Kerr, Wyllie, and Currie, *British Journal of Cancer* 26 (1972) 239–257. Europe PMC: apoptosis is proposed as a mechanism of controlled cell deletion, playing a complementary but opposite role to mitosis. The note's **KNOWN** sentence keeps "controlled deletion, complementary to mitosis." See N2. **METAPHOR** for the schedule is honest: the quality-observed arm does not lower the unconstrained cost at this cap.

Perunov, Marsland, and England, *Physical Review X* 6 (2016) 021036. Crossref spells the first author Nikolay and has no abstract. The arXiv record `1412.1875` spells him Nikolai and carries the abstract the note paraphrases: a generalization of the Helmholtz free energy for the finite-time stochastic evolution of driven Newtonian matter, and a tendency toward states formed through reliable absorption and dissipation of work from the environment. The hazard is an assumption of class AF. **METAPHOR** for "their driving is why \(J\) has this shape," and **CONJECTURE** for "some generator in that literature induces both this hazard and this heat floor," are the labels the addendum required. The note uses them that way.

The new files do not use "bill." They do not use "kill." The objective is called a cost. Clean refutations are marked **FAILS**, which is the label §5 of the preregistration defined, and the heterogeneous miss is given a diagnosis. The write-up does not promote that miss to a verdict on the hypothesis sentence. The overclaim is the PR title, which names the convex bowl antifragility after §5 has said that a Jensen gain would reverse the inequality.

## Required fixes

**B1. Rebase onto current main `13eec9a` and number the row T43.** A merge of `acff082` with `origin/main` `13eec9a` conflicts in `OPEN_WORK.md`. Main's T41 is the holographic physics note and main's T42 is holographic memory. This branch, whose parent predates that split, still has the memory paragraph as T41 and adds the turnover paragraph as T42. Keep main's T41 and T42. Place the turnover paragraph after them as T43. The new directory applies cleanly. Leave `THEORY.md`, `CORE.md`, and `README.md` untouched.

**B2. Lead with the admissible comparison.** In §0, in the prose of §4, and in the PR body, give the identical-unit admissible point first among the design claims: rate \(1\), cost \(15.473978\), probability \(0.020940\), a margin of \(0.526022\) under the inadmissible zero at cost \(16\). State beside it that the informative admissible point costs \(15.566427\) and the uninformative admissible point costs \(22.311716\), both above their zero-shock cost \(13\), and that the quality-observed admissible point costs \(15.471038\) against its own zero at \(13\). Keep the unconstrained minimum, rate \(0.2646371727\), cost \(13.3545082433\), as the minimum of the cost P1–P7 score, and state its ruin probability \(0.473560\) at the official grid point rate \(0.3\) in the same paragraph. The sentence "It does not move the scores above" may remain only as a statement that those numbered predictions were scored on the unconstrained cost, which the preregistration required.

**B3. Retitle the PR.** The cost is strictly convex on \([0,\infty)\), and the spread around the minimum raises it by \(0.2232577182\). Section 5 already says this is not antifragility in the sense of `theory/ROBUSTNESS.md` §6. Rename the PR so the title names turnover, the heat, and a positive level of stress.

**B4. Replace the blank-design sentence in §6.** The note says a design that can switch the memory off will do that before it buys this cap. Under the cap the blank design has error \(4\) and ruin probability \(1\). The precision A14 would install, at most \(0.093750\), pools to \(0.375\) at full alignment, short of \(5/12\). The unconstrained comparison of the identical-unit minimum with the blind cost \(6\) is a comparison of two designs the cap rejects. Say that, and keep the sentence that the turnover result is conditional on the cap being installed.

The official digits do not change. P1 remains **FAILS** at the frozen cap. The heat and convexity scores remain **PROVED**.

## Nits

**N1.** The ruin table's row "uninformative / blind schedule" prints A4's Monte Carlo: cost \(11.262060\), probability \(0.638600\), admissible cost \(22.311716\), probability \(0.040260\). Section 3's quality-blind cost \(11.2576037038\) is A8, whose admissible point is cost \(22.311377\), probability \(0.041580\). The two policies share a mean-field curve. Name A4 on the row. Both admissible costs exceed \(13\).

**N2.** The Kerr sentence drops "but opposite." The fetched abstract says a complementary but opposite role to mitosis. Restore the word.

## Next preregistered test

One new preregistration. Do not edit `PREREG.md`, and do not rescore this run.

Freeze a grid of installed precision and turnover rate before any evaluation, and score only points with \(P(\varepsilon>3/2)\le 1/20\). Two pricings of the same hazard and the same copy-with-mutation rule:

1. Identical units. The question is whether any admissible pair beats the frozen admissible point, precision \(1/2\) at rate \(1\), mean-field cost \(15.397225\), official cost \(15.473978\). The diagnostic above found precision \(1/4\) at rate \(2\), mean-field cost \(14.408952\), probability about \(0.024\). The grid has to reach above \(5/48\), because the A14 precision \(0.093750\) cannot meet the cap at any rate.
2. Heterogeneous units, once with the locked coupling and once with heat fixed per unit and quality used only as aim and hazard. Score the admissible argmin of each. The fixed-heat diagnostic has an unconstrained minimum at rate \(0.236680\), cost \(13.548262\), against \(16\), and that minimum is inadmissible. Its admissible grid point costs about \(16.17\), above \(16\) and above the identical-unit admissible cost. An unconstrained interior minimum with ruin probability above \(1/20\) is not a pass. Write that bar into the preregistration.

Leave \(b\), \(m\), \(\eta\), \(\varepsilon_{\mathrm{cap}}\), and \(\varepsilon_r\) where this run froze them. Leave the hypothesis sentence where it is.

## Checks

On `acff082`, at nice 19:

| Command | Result |
|---|---|
| `nice -n 19 python3 theory/antifragility_checks/turnover_checks.py` | exit 0; stdout byte-identical to the committed `results.out`; machinery `FAILS 0` |
| `nice -n 19 python3 reviews/antifragility_2026-11-22/recompute.py` | the numbers in this review; does not import the author's module |
| `tools/check_open_work.py` on that head | RESULT: PASS |
| `tools/check_consistency.py` on that head | wording FAILs 0; one freshness FAIL, because `STATUS.md` names `d4de5a6` and current `origin/main` is `13eec9a`. This branch does not edit `STATUS.md`. The line is not a defect in the turnover arithmetic |

No `lake` build. The full `pytest` of `tools` was not rerun; the previous review on this main reported 255 passed and 1 skipped, and this branch adds the one test that shells the script above.

VERDICT: NEEDS-FIXES
