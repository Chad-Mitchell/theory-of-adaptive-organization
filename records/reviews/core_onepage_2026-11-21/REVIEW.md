# Review of the one-page core (PR #142)

Read-only hostile review of `2cc8d7ea8516213b5cd1a7cfd7c616b3610957ca` on `core-onepage-2026-11-21`, base `main` `d34df95`. Saturday 21 November 2026. Computations at nice 19. The reviewer wrote none of the page, made no commit, and did not merge.

**NOT READY.** The order is the right order for holding the theory: the hypothesis, the cost, why a stack exists, layer lifetime and spacing, local versus shared under delay, who it covers, assumptions and what breaks, evidence, what is next. The sentences that carry numbers from Shannon, DIR1, and the layer-lifetime checks are mostly exact. Several sentences marked proved say more than the proof. Those are the sentences a reader would memorize.

## Blockers

1. `CORE.md:34`. Replace `One lumpy tracker, refreshing at the lifetime below, is already optimal for a single process, including a fractal one (**PROVED**).` with `One lumpy tracker is already optimal for a single process, including a fractal one (**PROVED**). For increment variance proportional to \(\tau^{2H}\) the refresh scales as \((k/(wC))^{1/(2H+1)}\); the square-root lifetime below is the Brownian case \(H=\tfrac12\).` Source: `theory/LAYER_LIFETIME_2026-11-21.md` §3c. The summary line that says "refreshing at \(T^*\)" for a fractal overstates that section.

2. `CORE.md:34`. Replace `If a joint reset is cheaper than the parts, one layer beats two (**PROVED**).` with `One layer beats two when a joint reset costs about as little as one part (**PROVED**). A joint reset that costs the sum of the part costs does not: the specialized stack is then never more expensive.` Source: `LAYER_LIFETIME` §4. Cheaper than the sum is not the theorem. With equal variance rates and part costs \(1\) and \(100\), a joint cost of \(80\) is below \(101\) and the stack is still cheaper (\(\sqrt{160}\approx 12.6\) against \(11\)).

3. `CORE.md:36`. Replace `The existing layer-count converse is CT21: layers are at most the world's predictive degree, and a continuum of time scales has no exact finite design (L3).` with `The existing layer-count converse is CT21, linear-Gaussian, squared-error, counted by degree. For finitely many real modes, layers are at most the world's predictive degree (L2). On a non-rational spectrum, \(E_K>E_\infty\) for every finite \(K\), and \(K^*\to\infty\) only if also \(E_K\to E_\infty\) (L3).` Source: `THEORY.md` CT21. The confirm review of PR #141 required the \(K^*\) clause. "No exact finite design," read with the degree clause, says a continuum has no finite optimum.

4. `CORE.md:54`. Replace the paragraph from `The fast-local / slow-shared sign` through `won at \(\tau = 400\ell\).` with `The fast-local / slow-shared crossing needs latency on the shared channel only, and a shared lump cheaper than \(N\) local lumps (\(k_S<N k_L\)). It is **PROVED** for a Brownian common driver with fixed-period refreshes, and **NUMERICAL** for an Ornstein–Uhlenbeck driver. Under that same shared-only delay, the optimal barrier keeps the sign, and the variance rate where the two costs cross is the fixed-period crossing divided by 3. If local updates carry the same observation delay, the delay floors cancel. Which side is cheaper then does not depend on the drift variance, so speed does not flip the choice. \(\tau>\ell\) is not sufficient: at the prices in the checks, the OU crossing is about \(183\ell\), so shared still lost at \(\tau=40\ell\) and won at \(\tau=400\ell\).` Source: `LAYER_LIFETIME` §0.2 and §5. The factor 3 and the \(183\ell\) figures match the confirm re-derivation. "The sign" on the page has the fast/slow sign as its antecedent, and that reading is false.

5. `CORE.md:75`. Replace `If a shared read is systematically better or worse than a local one, the nesting factor can change sign, and fast scales need not go local.` with `If a shared read is systematically better or worse than a local one, fast scales need not go local. The factor \(e^{-2\ell/\tau}\) stays positive.` Source: `THEORY.md` line 488, \(X_S=\nu\cdot\pi\cdot e^{-2\ell/\tau}\cdot X_L\) at equal read quality. Add a row: `Shared lump below \(N\) local lumps (\(k_S<N k_L\)) | If the shared re-forming cost is not cheaper than \(N\) local ones, the slow-shared side of the crossing is absent.`

6. `CORE.md:44`. Replace `This formula is **KNOWN** (Dixit 1991; the quadratic-loss case is exact at zero discounting).` with `This formula is **KNOWN** as an exact result at zero discounting (Chalkley 1997, *Economics Letters* 57:189, doi 10.1016/s0165-1765(97)00222-x). Dixit 1991 is the approximation that case makes exact (*Review of Economic Studies* 58:141, doi 10.2307/2298051, title "Analytical Approximations in Models of Hysteresis"; *JEDC* 15:657, doi 10.1016/0165-1889(91)90037-2).` Both Dixit DOIs and the Chalkley DOI resolved on Crossref on 21 Nov 2026. The repo's own credit is `theory/DYNAMICS.md` CL19 (a).

7. `CORE.md:64`. Replace the Malone sentence with `The checked qualitative precedent is Malone, Yates & Benjamin 1987 (*Communications of the ACM* 30(6):484–497, doi 10.1145/214762.214766): lower coordination costs shift activity toward markets rather than hierarchies. That is not the square-root lifetime and not the swarm limit. Malone 2004 (*The Future of Work*, Harvard Business School Press, ISBN 978-1-59139-125-8) has no Crossref DOI; the ISBN filters returned no works. Publisher copy describes decentralized forms under falling communication costs. It was not read for this page and is not evidence for \(T^*\) or the swarm limit.` The 1987 Crossref abstract is the markets-versus-hierarchies sentence. Authors, container, volume 30, issue 6, pages 484–497, and issued 1987-06 match.

8. `CORE.md:32`. Replace `A store beats a memoryless rule only when reuse of what it holds saves more than its upkeep \(h\).` with `A store pays upkeep \(h\). Whether it beats a memoryless rule is the comparison of that upkeep with the drop in the other terms. There is no numbered theorem in these words (the hold-or-fade results are CT4, CT9, CT11).` `reviews/core_onepage_2026-11-21/CLAIM_SOURCES.md` already says this sentence is not a numbered result. Printing an "only when" anyway is the repo's recorded error E1 (`reviews/lock_2026-11-18/PROCESS.md`).

9. `CORE.md:3`. Replace `the operational kill rule and the Model S counterexample stay in force in THEORY §3 and \`core/KEYSTONE_NOTE.md\`.` with `the operational kill rule stays in force in THEORY §3. There is no Model S counterexample to N60. The rhythms counterexample (two oscillators, \(R=3\), formula 2, argmin 3) and the failed IMP-N60 rule stay in force in \`core/KEYSTONE_NOTE.md\`. Convexity inside Model S is numerical (120/120), not proved.` `core/KEYSTONE_NOTE.md` §1 records no counterexample inside Model S. §2 records the rhythms counterexample outside it.

Also on `CORE.md:34`, replace `A stack of layers appears only when no single part can afford to read and reset the whole state, especially when shared information arrives late.` with `A stack is the cheapest design only when a layer cannot, or cannot afford to, reset the whole state (**PROVED** in that specialized model).` Delay is the §4 result. "Appears" reads as a fact about nature. The proof is about the minimizer.

## Should-fixes

- `CORE.md:22`. Move `in a stationary world the system does not affect; drifting and random-walk worlds are open, CX1` onto the S1 sentence. S2 and S3 are the frontier and Farrell's split.
- `CORE.md:26`. After the frontier sentence, add `The frontier is a set, not a single number like capacity.` Add `A binding ruin cap can raise the information floor; no formula for that rise is derived (**OPEN**).` Add `Whether the true least cost equals the information floor when memory and reads are both priced, or sits strictly between the floor and this Kalman design, is **OPEN**.` Sources: `theory/SHANNON_2026-11-21.md` §0.4, §3, §2.
- `CORE.md:44`. Replace `the Brownian formula mis-times the refresh (**NUMERICAL**).` with `the Brownian formula is quantitatively false (**NUMERICAL**: a check at \(T^*/\tau\approx 0.63\) missed by 137%).`
- `CORE.md:60`. Replace the class list with `The same cost is the theory's definition for systems that must act ahead of a changing world. THEORY §1 names cells, colonies, people, firms and cities. Firms are one class, not the point. The hypothesis is that *strongly selected* systems in a class that qualifies sit near the minimum, not that every organization already does. Cities, nation-states, global economies and the biosphere do not qualify until a class-specific population proxy is preregistered (THEORY §3).` Brains, teams, and software agents are not the theory's list.
- `CORE.md:62`. Delete `Cheaper coordination — including by AI — is a candidate way \(k\) falls. That is a prediction, not a measurement.` No source note contains it.
- `CORE.md:83`. Replace `Firms fail (6/10).` with `Firms fail the locked class gate (6/10 = 0.60; four zeros, no −1).` The verdict word in `tests/DIR1/RESULTS_DIR1.md` is fails. The signs did not reverse.
- `CORE.md:85`. Replace the Palmer/Mattingly sentence with `Palmer, Marre, Berry & Bialek 2015 (doi 10.1073/pnas.1506855112) test efficient coding of predictive information in the retina. Mattingly, Kamino, Machta & Emonet 2021 (doi 10.1038/s41567-021-01380-3) test an *E. coli* chemotaxis bound. Both are consistent with the technical half. Neither was preregistered here, and neither qualifies under THEORY §3.`
- `CORE.md:86`. Replace the lead-in with `**Layer-lifetime predictions, not T27's P1–P3 and not the *E. coli* discrimination checks (OPEN, not locked; no outcome data retrieved).** T27's P3 failed in-model and is not rescued (\`core/bridge_2026-11-21/\`).` In P2, replace `the lifetime ratio matches the spacing formula` with `and the stakes are equal, the lifetime ratio matches the §3 formula. That formula is not the prediction when the stakes differ.`
- `CORE.md:91`. Add `An in-model bridge already gives expected excess \(d/(2\sigma N_e)\) under weak mutation and fitness linear in \(J\). Its P3 failed and is not rescued. The proof still to write does not assume that bridge.`
- Header. Add **OPEN** and **ANALOGY** to the status-word list. The page uses both.
- End of §1. Add `What is claimed as new is the package: one priced objective under a ruin cap, the world's frontier as its input, and a kill rule across scales (THEORY §10).`

## Structure

The section order is what this page is for. Keep it.

Cut the AI sentence and the "especially when shared information arrives late" clause. Delay belongs in §4.

Keep the support-function sentence, the free-disposal hull, the pair "gap 4.26%" and "costs 4.45% more," and \(183\ell\), \(40\ell\), \(400\ell\). They are short because a false reading is short. The factor 3 stays after "crossing" has a referent.

## Caveats dropped from the previous core

Still live, and the page's pointer is wrong or missing:

- Rhythms counterexample, IMP-N60 failed, Model S convexity unproved. The header calls this "the Model S counterexample."
- The frontier is not a single number like capacity.
- Achievability when memory and reads are both priced.
- A binding ruin cap can raise the floor; the rise has no formula.
- Palmer and Mattingly test other programmes.
- T27 P3 failed and is not rescued. The new P1–P3 collide with that name.
- Chalkley 1997 is the zero-discount exactness credit.

Pointed and still in force: the kill rule, including the CT41 trichotomy, is in THEORY §3. P2 still requires independent prices, so the revealed-prices amendment remains unapplied. "No system has qualified" covers the dropped instruction to source *E. coli* \(\sigma\), \(N_e\), and \(T_{\rm red}\) before rescoring. STATUS still records \(\sigma\) and \(T_{\rm red}\) missing.

Superseded: "the directional field test is in progress; its predictions are locked before any data are scored." DIR1 is scored, reviewed, and merged.

Still true, and not a claim this page makes: cymatics (aggregate pass, 3 of 7 light worlds miss individually, `core/keystone_checks/RHYTHM_RESULTS.md`); the 24 pre-#116 worlds; N60 cannot return \(K^*=0\); the EVO1 arm scores. "Mixed (EVO1)" does not say the failed arms passed.

## Claims that match their sources

- Hypothesis sentence, byte-identical, once in `CORE.md` and once in `THEORY.md`. "bill" and "theory of everything" are absent.
- Diff against `d34df95` is three files. No prereg, `.sha256`, or lock file is among them.
- S1 scope, no layer charge in the floor, Landauer on the erasure part of \(\kappa\), Sagawa & Ueda 2009 on the sum of measurement and erasure, edge attainment, and \(J_{\rm floor}/J=0.9574\) (gap 4.26%; the design costs 4.45% more) at \(\kappa=c=w=1\), world \(a=0.9\), \(Q=1\), lead 2, layer price out of both sides. `theory/shannon_checks/shannon_checks.out` has efficiency 0.9574 at that point. \(1-0.9574=0.0426\). \(1/0.9574-1=0.0445\).
- S2 and S3: dual \(J^*=-\sigma(-p)\), operational least cost only when \(A=c\cdot r\) and \(L=0\), free-disposal hull of the Pareto face, Farrell split for \(C=\kappa I+c\cdot r\) only, technical efficiency 1 for a positive-price linear-cost minimizer on its feasible set, ruin cap need not preserve convexity.
- \(T^*=\sqrt{6k/(w\sigma^2)}\) and the equal-stake spacing ratio match `LAYER_LIFETIME` §2 and §3a, apart from the Dixit/Chalkley credit.
- DIR1: INCONCLUSIVE, pooled 29/42, animals 20/27 support, firms 6/10 fail, cells \(n=5\) do not count, two class fails required, D1–D4 do not discriminate, D5 unscored at \(n=2\). Matches `tests/DIR1/RESULTS_DIR1.md`.
- Thirty earlier field rows, 10 proxy-pass and 20 proxy-fail. Matches `THEORY.md` §9 and `STATUS.md`.
- Karim, Carroll & Long 2016 and Girod & Whittington 2017 do not identify P2 or P3. Girod's Crossref abstract is a performance regression. Karim's Crossref title is structural realignment under turbulence.
- Header SHAs: `0726423` is the #139 merge, `a97887e` the #141 merge, `1cb1ac2` the #138 merge, `d34df95` the #140 merge. All are ancestors of `origin/main`. `origin/main` is `d34df95`.
- `CORE.md` is 2097 words.

## Citations

Resolved on the Crossref API, 21 Nov 2026. Titles, authors, containers, and years match the notes unless marked.

| Item | DOI or ISBN | Result |
|---|---|---|
| Malone, Yates & Benjamin 1987 | 10.1145/214762.214766 | Resolves. Abstract: a shift toward markets rather than hierarchies. The page's "new organizational forms" overreads it. |
| Malone 2004 | ISBN 978-1-59139-125-8 | Crossref ISBN filters: 0 works. No DOI, as the page says. WorldCat and the publisher description identify the book. |
| Dixit 1991 RES | 10.2307/2298051 | Resolves. Title: "Analytical Approximations in Models of Hysteresis." Vol. 58, p. 141. |
| Dixit 1991 JEDC | 10.1016/0165-1889(91)90037-2 | Resolves. Vol. 15, pp. 657–673. |
| Chalkley 1997 | 10.1016/s0165-1765(97)00222-x | Resolves. Missing on the page. Title is the zero-discount explicit solution. |
| Farrell 1957 | 10.2307/2343100 | Resolves. *J. R. Stat. Soc. A* 120:253. |
| Sagawa & Ueda 2009 | 10.1103/PhysRevLett.102.250602 | Resolves. Measurement and information erasure. |
| Sagawa & Ueda 2011 erratum | 10.1103/PhysRevLett.106.189901 | Resolves. Not cited on the page; the note's claim already includes it. |
| Karim, Carroll & Long 2016 | 10.5465/amj.2012.0409 | Resolves. *Acad. Manage. J.* 59:791–817. |
| Girod & Whittington | 10.1002/smj.2543 | Resolves. Issued 2016-07-11; print 2017, vol. 38, pp. 1121–1133. Citing 2017 matches the note. |
| Palmer et al. 2015 | 10.1073/pnas.1506855112 | Resolves. Abstract: efficient coding of predictive information. |
| Mattingly et al. 2021 | 10.1038/s41567-021-01380-3 | Resolves. Title: "Escherichia coli chemotaxis is information limited." |

## Checks

| Command | Result |
|---|---|
| `python3 tools/check_fresh.py` | PASS. STATUS `main` is `a97887e`; window `d34df95 a97887e 0726423 1cb1ac2 2c32ade` |
| `python3 tools/check_consistency.py` | PASS (0 FAIL, 23 INFO) |
| `python3 tools/check_open_work.py` | PASS |
| `python3 -m pytest -q tools` | 169 passed, 1 skipped, 250.05 s. Skip: `tools/test_lean.py:101`, Lean 4 / lake is not installed. pytest 9.2.0, scipy 1.18.1, and sympy 1.14 were installed for this run |

`CLAIM_SOURCES.md` records the fractal lifetime, the Malone breadth, the missing \(k_S<N k_L\) premise, and the P1–P3 name collision, and the page still ships the stronger sentences. The map is not a review.
