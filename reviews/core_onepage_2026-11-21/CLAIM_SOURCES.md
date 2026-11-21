# Claim sources for the one-page CORE rewrite

Saturday 21 November 2026, about 3:15 PM ET (America/New_York). Branch `core-onepage-2026-11-21`, written against `main` `d34df95` (PR #140 merged; #141 layer lifetime merged as `a97887e`, including confirm-review defects 1–3 in `391cfbe`). This file is a claim map for the rewrite, not a review and not a lock.

The previous `CORE.md` is frozen at `history/2026-11-21_CORE_before_onepage.md`. Word count of the new `CORE.md` is 2097 by `wc -w` (computed after the page was written). The previous page at the freeze was 1888 words, plus a one-line history wrapper.

## Malone

Malone is not elsewhere in the repository (a grep hits only Juni, Gureckis & Maloney 2016, a different author). Citations used:

- Malone, T. W., Yates, J., & Benjamin, R. I. (1987). Electronic markets and electronic hierarchies. *Communications of the ACM* 30(6):484–497. DOI `10.1145/214762.214766`, resolved on the Crossref API on 21 Nov 2026: title, authors (Crossref given names: Thomas W. Malone, Joanne Yates, Robert I. Benjamin), container, volume, issue, pages, and issued date 1987-06 all match. The 1987 abstract's claim is specifically that lower coordination costs shift activity toward markets rather than hierarchies. The page credits the broader qualitative point (falling coordination costs produce new organizational forms) and does not attribute the \(\sqrt{k}\) lifetime or the swarm limit to Malone.
- Malone, T. W. (2004). *The Future of Work: How the New Order of Business Will Shape Your Organization, Your Management Style, and Your Life.* Harvard Business School Press, Boston. ISBN 978-1-59139-125-8 (also 1591391253). Confirmed from WorldCat / publisher records. Crossref filter `isbn:9781591391258` and `isbn:1591391253` returned zero works. No book-level DOI is given, and none was invented. (A later Malone book chapter titled "The Future of Work," Springer, DOI `10.1007/0-387-28918-6_2`, is a different item and was not cited.)

## Claim-to-source mapping

Claims below are in reading order. Labels on the page are those of the source unless noted.

| Page claim | Source | Label in source / notes |
|---|---|---|
| Two-part split: Part 1 mathematics / limits, Part 2 empirical closeness | Previous `CORE.md`; `theory/SHANNON_2026-11-21.md` §0 | Kept, rephrased. |
| Hypothesis sentence, byte-identical | `CORE.md`, `THEORY.md` §3, SHANNON and LAYER_LIFETIME notes | Exact match. |
| Master equation \(J=\kappa I_{\rm mem}+hK+w\mathbb E[\ell]+A+L\) s.t. \(P({\rm ruin})\le\varepsilon\) | Previous `CORE.md` §1; `THEORY.md` §3 (there \(\varepsilon_r\)) | Definition, not a theorem. Notation follows previous CORE (\(\varepsilon\), not \(\varepsilon_r\)). |
| Term glosses (layer = tracking store; lateness counts as error; ruin is a cap) | Previous `CORE.md` §1; `THEORY.md` §3 | |
| World is a measured input; one currency; assembled from known parts | Previous `CORE.md` §1; `THEORY.md` §3 | |
| S1 information floor in a stationary exogenous world; CX1 open for drifting / random-walk worlds | SHANNON §0.2, §2, Theorem S1; previous `CORE.md` §2 | **PROVED** for information terms. Ingredients **KNOWN**; assembly is the repo's. |
| No proved layer charge; memoryless \(K=0\) still carries information | SHANNON §0.2, §2; previous `CORE.md` §2 | **PROVED**. |
| Landauer floors erasure part of \(\kappa\); Sagawa & Ueda 2009 floor the sum of measurement and erasure, not a stacked read price | SHANNON §0, §2; previous `CORE.md` §2 | **KNOWN** ingredients. Sagawa & Ueda 2011 erratum is in the Shannon references. |
| Floor attained exactly when memory or reads are free, scalar Gauss–Markov | SHANNON §0.3, §3; previous `CORE.md` §2 | **PROVED** at the edges (**KNOWN** results: Tanaka et al. 2017; CT4). |
| Efficiency \(J_{\rm floor}/J=0.9574\) (gap 4.26%; design costs 4.45% more than the floor) at worst grid point \(\kappa=c=w=1\), layer price left out of both sides; one world \(a=0.9\), \(Q=1\), lead 2; 36-point grid; not a bound over worlds | SHANNON §0.3, §3; previous `CORE.md` §2 (merged in PR #139) | **NUMERICAL**. Scoping kept exact. |
| S2: frontier has no prices; \(J^*(p)=\inf\langle p,z\rangle=-\sigma(-p)\); equals operational least cost only when some minimizer has \(A=c\cdot r\) and \(L=0\); positive-orthant \(J^*\) recovers the free-disposal hull of the Pareto face, not the whole convex hull | SHANNON Theorem S2, §0.4; previous `CORE.md` §2 | **PROVED** (standard convex analysis). |
| S3: technical efficiency needs no prices; Farrell split holds for \(C=\kappa I+c\cdot r\), not for \(J_{\rm floor}/J\); linear-cost minimizer at strictly positive prices has \(\theta=1\); binding ruin cap need not preserve convexity | SHANNON Theorem S3, §0.5, §5; previous `CORE.md` §2 | **PROVED**. |
| Part 2 = technical half (near the frontier) + allocative half (at the price-selected point) | SHANNON §5; previous `CORE.md` §3 | **HYPOTHESIS**. |
| "Strongly selected" is operational in THEORY §3; no system has qualified | `THEORY.md` §3; previous `CORE.md` §3–4; `STATUS.md`; DIR1 RESULTS | STATUS: *E. coli* qualification remains NOT ESTABLISHED. |
| No information argument forces a layer | SHANNON §2 ("No information-theoretic argument forces \(K\ge 1\)") | **PROVED** (the converse does not force it). |
| A store beats a memoryless rule only when reuse saves more than upkeep \(h\) | Economic content of \(hK\) in the master equation plus S1 (a memoryless rule has \(K=0\) and still carries information); THEORY §6 rule 2 / CT4, CT9, CT11 ("keep while the value rate beats upkeep") | Not a numbered theorem under this wording. |
| A stack appears only when no part can afford to read and reset the whole state; one lumpy tracker at \(T^*\) is already optimal for a single process, including a fractal one | LAYER_LIFETIME §0.3, §3c, §4 | **PROVED**. |
| Joint reset cheaper than the parts \(\Rightarrow\) one layer beats two | LAYER_LIFETIME §4 | **PROVED**. |
| Delayed shared information is the setting in which a part cannot cheaply use the whole state's latest value | LAYER_LIFETIME §0.2, §5 | Companion of the local/shared result. |
| No fewest-layers limit recovered from \(T^*\); existing converse is CT21 (L3); in Model S the fewest-stores floor remains numerical \(E_K\); \(T^*\) does not compute \(E_K\); layer-term floor stays OPEN | LAYER_LIFETIME §0.3, §3c (confirm-review defect 3, `391cfbe`); SHANNON §2, §7; previous `CORE.md` §5; `THEORY.md` §5 (iii) | CT21 is **PROVED** in-model (linear-Gaussian, squared-error, counted by degree: THEORY §9). The confirm wording: L3 says \(E_K>E_\infty\) for every finite \(K\) on a non-rational spectrum, and \(K^*\to\infty\) only if also \(E_K\to E_\infty\); that is a statement about Model S's \(E_K\), and \(T^*\) does not compute \(E_K\). The page states the last fact and points to CT21, not the full L3 expansion. |
| \(T^*=\sqrt{6k/(w\sigma^2)}\) | `theory/FLUID_LAYERS_2026-11-21.md`; LAYER_LIFETIME §0, §2; Dixit 1991, already Crossref-verified in the layer-lifetime note (RES doi 10.2307/2298051; JEDC doi 10.1016/0165-1889(91)90037-2) | **KNOWN**. Exact at zero discounting (Chalkley 1997, credited in the note). |
| Lifetime grows as \(\sqrt{k}\); \(100\times\) lower cost \(\Rightarrow\) \(10\times\) shorter life | FLUID_LAYERS | Corollary of the formula. |
| Smooth adjustment \(\Rightarrow\) no discrete lifetime (CL19 (c)) | LAYER_LIFETIME §2, §4 | |
| OU / mean-reverting caveat: formula mis-times when \(T^*\) is not short compared with the correlation time | LAYER_LIFETIME §3b | **NUMERICAL**. |
| Spacing ratio \(T_i^*/T_j^*=\sqrt{(k_i/k_j)(\sigma_j^2/\sigma_i^2)}\) at equal stakes, specialized stack; not a universal geometric series | LAYER_LIFETIME §0.1, §3a | **PROVED** in Model LS. |
| Fast-local / slow-shared sign only with shared-only latency | LAYER_LIFETIME §0.2, §5 | **PROVED** for Brownian, fixed-period refreshes. |
| Optimal barrier under the same observation delay keeps the sign and divides that crossing by 3 | LAYER_LIFETIME §0.2, §5 (confirm-review defect 1, `391cfbe`) | The factor 3 uses both coefficients 6 and 2: barrier excess equals the fixed-period excess divided by \(\sqrt{3}\); the variance-rate crossing is the fixed-period crossing divided by 3. The page states the crossing result. |
| Equal observation delay: the floors cancel; the sign is the same at every \(\sigma^2\), so there is no switch | LAYER_LIFETIME §5 (confirm-review defect 2, `391cfbe`) | The remaining gap is \(\sqrt{\sigma^2}(\sqrt{2k_S Nw}-N\sqrt{2k_L w})\) for fixed-period refreshes, and that gap divided by \(\sqrt{3}\) for the barrier. The page states the floors-cancel / no-switch fact, not the displayed gap formula. |
| OU companion **NUMERICAL**; \(\tau>\ell\) is not sufficient; crossing about \(183\ell\); shared lost at \(40\ell\), won at \(400\ell\) | LAYER_LIFETIME §0.2, §5 | At the prices in the checks; those multiples move with the prices. The page says "at the prices in the checks." |
| Older nesting factor \(e^{-2\ell/\tau}\) at equal read quality (CT28, CT34) | THEORY B.11; LAYER_LIFETIME §5; previous `CORE.md` §2 | **PROVED** in-model in the repository. CT35 is the subadditivity map, not this factor; the page does not call it CT35. |
| Same cost applies to cells, colonies, brains, firms, teams, software agents; firms are not the point; hypothesis is about strongly selected systems, not that every organization already sits at the minimum | `THEORY.md` §1–3 (scope is strongly selected systems at every scale) | Deliberately narrower than a universal assertion. Universal overstatement is the repo's top recorded error. |
| As \(k\to 0\), continuous re-form / no lasting identity (swarm limit) | FLUID_LAYERS (ANALOGY to fission–fusion societies, Aureli et al. 2008) | Page labels it an **ANALOGY**, not a field result. AI as a candidate way \(k\) falls is a prediction, not a measurement. |
| Malone as prior evidence for the qualitative direction, not for \(\sqrt{k}\) or the swarm limit | See Malone section above | |
| Assumptions table: strong selection | `THEORY.md` §3–4, §9 | If wrong, Part 2 fails. |
| Assumptions table: cost-covered persistence | `THEORY.md` §1 ("order last only where something pays to keep it"); planned selection-proof axiom, not a numbered theorem | If wrong, selection need not climb toward min \(J\). |
| Assumptions table: shared-only delay | LAYER_LIFETIME §0.2, §5 | |
| Assumptions table: equal read quality | THEORY B.11 / CT28, CT34; previous `CORE.md` §2 | Load-bearing for the OU nesting factor. The lumpy D5 crossing is instead load-bearing in shared-only delay and \(k_S<N k_L\). |
| Assumptions table: exogenous / stationary world | SHANNON S1 setting (A1, A2); CX1, CX2 in `THEORY.md` §9 | |
| Assumptions table: S-A (\(A\ge c\cdot r\)) | SHANNON §2 | Explicitly "an assumption, not a sensor law." |
| Assumptions table: lumpy re-forming | LAYER_LIFETIME §2; CL19 (c) | |
| Assumptions table: cannot cheaply reset the whole state | LAYER_LIFETIME §0.3, §4 | |
| DIR1 INCONCLUSIVE; pooled 29/42; animals 20/27 support; firms 6/10 fail; cells \(n=5\) do not count; kill needed two class fails and was not met; D1–D4 do not discriminate vs any \(S+wE\) optimizer; D5 unscored \(n=2\) | `tests/DIR1/RESULTS_DIR1.md`; `STATUS.md` | **TESTED: INCONCLUSIVE**. QC-tier, not THEORY §3 qualification. Blind recode 19/20 and the exact binomial p-values were omitted for length; they remain in RESULTS. |
| Karim 2016 and Girod & Whittington 2017 do not identify P2 or P3; they cannot count against or for those predictions | LAYER_LIFETIME §7, wording after the #141 review should-fix and confirm (Karim, Carroll & Long 2016, doi 10.5465/amj.2012.0409; Girod & Whittington 2017, doi 10.1002/smj.2543, already Crossref-verified in the note) | Not a field result of ours. Performance stays out of the score (Girod). |
| 30 earlier field rows NOT A TEST (10 passed and 20 failed on proxy) | Previous `CORE.md` §4; `STATUS.md`; `THEORY.md` §9 | Unchanged. |
| EVO1 mixed, in-model only | Previous `CORE.md` §4; `OPEN_WORK.md` W2 / `STATUS.md` | Compressed. Full arm scores stay in `tests/EVO1/`. |
| Palmer et al. 2015; Mattingly et al. 2021: consistent with the technical half; not preregistered or qualified here | SHANNON §0.6, §6; previous `CORE.md` §4 | Context, not tests. Abstracts read, per the Shannon references. |
| P1, P2, P3 as stated | LAYER_LIFETIME §7 (P1 already dated in FLUID_LAYERS) | **OPEN**, not locked, no outcome data retrieved. These are the layer-lifetime predictions, not T27's P1–P3. |
| Every theorem refereed at most once, one bot family; no human expert has read the theory | Previous `CORE.md` §4; `STATUS.md`; `THEORY.md` §9 | Kept. |
| Next: prove closeness-to-minimum from selection axioms (persistence costs energy, copying favors what persists, the world drifts), closeness a function of selection strength | Planned after cleanup; not yet in the repo as a written proof | One line. Not claimed as started. |

The pointer line is `current to \`main\` \`d34df95\``, the same family `tools/check_fresh.py` and `tools/brief.py` accept. `STATUS.md` and `OPEN_WORK.md` were not rewritten in this PR; their pointers remain `a97887e`, which is still inside the five-commit first-parent window of `origin/main`.

## Caveats kept

- "Proved" means in-model and says nothing by itself about nature.
- Omissions are compressions, not withdrawals.
- Operational kill rule and the Model S counterexample stay in force (pointed at THEORY §3 and `core/KEYSTONE_NOTE.md`).
- S1 scoped to a stationary world the system does not affect; CX1 left open.
- No proved layer charge; Landauer / Sagawa & Ueda stacking caveat.
- 0.9574 scoped exactly (one world, 36-point grid, worst point, layer price left out of both sides, not a bound over worlds).
- \(J^*\) equals operational least cost only when \(A=c\cdot r\) and \(L=0\).
- \(J^*\) on the positive orthant recovers the free-disposal hull of the Pareto face, not the whole convex hull.
- Farrell product holds for \(C\), not for \(J_{\rm floor}/J\).
- Binding ruin cap need not preserve convexity.
- Layer-term floor still OPEN; CT21 is the existing converse; \(T^*\) does not compute \(E_K\).
- \(T^*\) exact at zero discounting; OU / long-lifetime caveat kept.
- Spacing is not a universal geometric series.
- Shared-only delay; equal observation delay cancels the floors with no switch; barrier crossing divided by 3; \(\tau>\ell\) not sufficient, with the check-price numbers.
- Hypothesis applies to strongly selected systems, not to every organization as a fact.
- Malone not credited for \(\sqrt{k}\) or the swarm limit.
- Swarm limit labelled ANALOGY; AI-lowers-\(k\) labelled a prediction.
- DIR1 numbers and "does not discriminate" caveat.
- Karim / Girod non-identification.
- No qualifying system; earlier field rows NOT A TEST.
- Palmer / Mattingly not preregistered or qualified.
- P1–P3 not locked, no outcomes retrieved.
- Single bot-family review; no human expert.

## Caveats dropped or compressed, and why

| Item on the previous `CORE.md` | Treatment | Why |
|---|---|---|
| "Directional field test is in progress; its predictions are locked before any data are scored" | **Superseded**, replaced by DIR1 INCONCLUSIVE results | DIR1 was scored, reviewed, and merged in #138; `RESULTS_DIR1.md` and `STATUS.md` are later than that sentence. |
| Dense structure table: CT20, CT33, N60 (convexity 120/120, rhythms counterexample, IMP-N60 gates, holographic count, 24 excluded worlds, cymatics 3 of 7), CT22/CT25, CT14/CT16/CT35/CT36 fluid-membership sentence, freeze limit #137, CT37–CT43, CT23, J16 | Dropped from the page; stay in force in `THEORY.md`, `core/KEYSTONE_NOTE.md`, `theory/FLUID_LAYERS_2026-11-21.md`, `theory/DYNAMICS.md` | A reader does not need the table to hold the picture (cost, why layers, \(T^*\), local/shared, swarm). The Model S / N60 counterexample is pointed at, not withdrawn. |
| Fluid-layers sentence on several memberships, \(N>N^*(\rho)\), worth falling as \(e^{-2\ell/\tau}\), superadditivity, membership in every shared layer that passes | Compressed: the \(e^{-2\ell/\tau}\) factor is kept in §4 as the smooth companion; the rest stays in `theory/FLUID_LAYERS_2026-11-21.md` and THEORY B.11 | Several-memberships remains proved in-model there. |
| Selection bridge: \(\pi\propto\exp(-\beta J)\), expected excess \(d/(2\beta)\), T27 P1/P2 passed in-model, P3 failed and is not rescued | Dropped from the page; not withdrawn. T27 P3 failure remains in `core/bridge_2026-11-21/` and the frozen previous CORE | §8 replaces a report of the existing bridge with the planned axiom-level proof. Leaning on the bridge without P3's failure would overstate. |
| Full operational definition of "strongly selected" (five items, \(\varepsilon=10/(\sigma N_e)\), 10 redesign times, CT41 non-move rule, revealed-prices amendment proposed not applied) | Compressed to a pointer at THEORY §3 plus "no system has qualified" | Needed for a test protocol, not for holding the picture. The kill rule is still pointed at, not withdrawn. |
| EVO1 arm-by-arm scores (PC, W1, W2 passed; S031/S07 inconclusive; W4/W4b failed, with D2b/D1b) | Compressed to "in-model selection tests are mixed (EVO1)" | Details stay in `tests/EVO1/`. |
| "*E. coli* is the best candidate, and its \(\sigma\), \(N_e\) and \(T_{\rm red}\) are to be sourced before any rescoring" | Dropped as a named-candidate sentence | STATUS still has this; naming a candidate on the one page could be read as almost-qualified. "No system has qualified" is the load-bearing fact. |
| Open list: achievability when both priced; floor under a binding ruin cap; convexity in Model S; predictive rhythm rule; selection law under strong mutation or nonlinear fitness | Compressed into "layer-term floor stays OPEN" and the CX1 / S-A / next-proof lines | Still open in SHANNON §7; not withdrawn. |
| Long credit paragraph (Shannon through Sella & Hirsh; Friston as nearest rival; "what is claimed as new is the package") | Compressed. Dixit and Malone are credited where used. Remaining credits stay in THEORY §10, SHANNON §6, and LAYER_LIFETIME §6 | Holdability. Novelty of the package is not withdrawn. |
| Header date/SHA pointing at pre-#139 `2c32ade` and, later, `current to main a97887e` | Replaced with `current to \`main\` \`d34df95\`` | Factual update after #140 and #141 merged. |

## Uncertainties that remain

1. **"A store beats a memoryless rule only when reuse saves more than its upkeep \(h\)."** This is the natural accounting of \(hK\) plus S1 (memoryless \(K=0\) is allowed) and the hold-or-fade theorems (CT4, CT9, CT11). The repo does not use this exact sentence as a numbered result.
2. **Cost-covered persistence** is in THEORY §1 as a physical starting point, and in the planned selection-proof axioms, but it is not a numbered, refereed axiom in the merged tree. It is on the page because the page relies on it for why selection would care about \(J\).
3. **P1–P3 numbering** already exists elsewhere (T27's in-model P1–P3, of which P3 failed). The page's P1–P3 are the layer-lifetime tests. A later CLAIM_MAP pass should keep that distinction visible.
4. **Equal read quality vs the lumpy D5 result.** The assumption table assigns equal read quality to the nesting factor, which is right; the lumpy crossing's load-bearing premises are shared-only delay and \(k_S<N k_L\). \(k_S<N k_L\) is in the note and is not in the table, because the page does not lean on the explicit \(\sigma^{2*}\) formula.
5. **Malone 1987 is narrower** than "new organizational forms" (it predicts a shift toward markets rather than hierarchies). The 2004 book is the broader "new forms" statement. Both are cited, and credit is limited to qualitative direction. The 2004 book itself was not opened, only bibliographic records, so it is not quoted.
6. **The displayed gap formula** under equal delay (confirm defect 2) and the full L3 expansion \(E_K>E_\infty\) (confirm defect 3) are in the merged note and in this map, not on the one page. A reader can hold "floors cancel, no switch," "barrier crossing divided by 3," and "\(T^*\) does not compute \(E_K\)" without the algebra.
