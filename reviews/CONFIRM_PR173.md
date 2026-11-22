# Confirm of draft PR #173

**Verdict: CONFIRM.**

**Confirmer:** independent of the note and of the review. The note and OPEN_WORK T35/T36 were read at `d0abadc` before `reviews/test_search_2026-11-22/REVIEW.md`. Cloud transcripts were not read. This file does not edit the note, `CORE.md`, `THEORY.md`, or any locked file.
**Date:** Sunday 22 November 2026.
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/173
**Head confirmed:** `d0abadce3b62a7b7efe45462d441825ff77112c8` on `test-search-2026-11-22`. The re-review read `2ae8486`. The repair is `d0abadc`.
**Review read afterwards:** `reviews/test_search_2026-11-22/REVIEW.md` at `a3d7051` on `review-pr173-2026-11-22`.

The answer at `d0abadc` holds. No scored row meets all four bars. The even-money menu is a currency question, not a test of the cost. Under the reading already in CT43(i), the closer rival of a priced layer count is an unpriced information model.

## 1. Numbers

Recomputed in Decimal at 80 places, from the menu in `theory/GROWTH_BRIDGE.md` §3: win probability 0.6, \(\xi=\pm 1\), \(W=1+f\xi\), \(f\in[0,0.99]\),

\[
\lambda(f)=0.6\log(1+f)+0.4\log(1-f).
\]

1. \(\mathbb{E}[W-1]=0.2f\) is strictly increasing on the interval, so expected offspring has a unique maximizer at the right endpoint \(f=0.99\).
2. \(\lambda'(f)=0.6/(1+f)-0.4/(1-f)\) is zero only at \(f^\star=0.2\). \(\lambda(0.19)\) and \(\lambda(0.21)\) are both smaller, so the critical point is a maximum. On \([0,0.99]\) the unique growth maximizer is \(f^\star=0.2\).
3. The argmaxes differ by \(0.99-0.2=0.79\).
4. \(\lambda(0.2)=0.02013551355068887\ldots\). Rounded half-up at twelve decimal places this is \(0.020135513551\), the value printed in the growth bridge. The next digit is 6.
5. \(\lambda(0.99)=-1.42918729115339593\ldots\), which is less than \(\lambda(0.2)\). The growth bridge prints the inequality and does not print this second value. The note cites the argmaxes, not these two growth rates.
6. For \(W=1+\varepsilon f\xi\) with \(f\in[0,1]\), the growth maximizer is \(\min(1,0.2/\varepsilon)\). For \(\varepsilon<0.2\) that corner is \(f=1\), the same corner as expected offspring. That is the sentence in §3 of the growth bridge.
7. The realized-residual pair: \(W=6-hK-\ell\). Design A with \(hK=0\) and \(\ell\in\{0,3\}\) equally likely has \(J=1.5\), \(\mathbb{E}[W]=4.5\), and \(\mathbb{E}[\log W]=\tfrac12\log 18=1.445185878948082\). Design B with \(hK=0.4\) and \(\ell=1.2\) certain has \(J=1.6\), \(\mathbb{E}[W]=4.4\), and \(\mathbb{E}[\log W]=\log 4.4=1.481604540924216\). The cost and \(\mathbb{E}[W]\) pick A. Log growth picks B. The printed digits are the float values of those logarithms.

Other printed counts that the note states as read, re-read here: Good's Crossref title includes 60,000 generations. Lalejini's Frontiers HTML states a population cap of 3,600, a per-instruction copy error of 0.0025, and periods of 100 updates. The NAS-Bench README states 423,624 unique networks. Bryson and Ofria's PLOS HTML states 3,600 individuals, a 60 by 60 grid, seven environments, and 200 replicate populations, and states that one treatment supplies more registers. Graham's Crossref abstract states five selection regimes and 12 genetic lineages. The frequencies and the aliquot volume are attributed to the review and are marked not re-read; they were not re-opened here. S3's inoculum, S10's cap, and S13's population are marked unchecked.

## 2. DOIs

Each bibliographic DOI in the note's verification table returned HTTP 200 from `https://api.crossref.org/works/{doi}` on 22 November 2026. Year and first author match the printed cells. Titles match the printed titles. Graham's returned title is the same words, with a newline and `<i>Neurospora crassa</i>` where the note prints markdown italics.

The two dataset DOIs returned Crossref 404. DataCite returned HTTP 200 with the printed titles and first authors: Graham 2014 for `10.5061/dryad.8qc20`, Bryson 2013 for `10.6084/m9.figshare.826206`. The Dryad landing returned HTTP 200. `https://doi.org/10.6084/m9.figshare.826206` returned 302 and then HTTP 202 on the figshare article page. The Graham article HTML returned HTTP 403.

Body DOIs not repeated as table rows also resolved. `10.1126/science.1114383` is Kussell and Leibler, 2005, "Phenotypic Diversity, Population Growth, and Information in Fluctuating Environments." `10.1007/s10955-011-0166-2` is Rivoire and Leibler, 2011, "The Value of Information for Populations in Varying Environments." The Europe PMC abstract for Kussell and Leibler states the four clauses the note uses: sensing followed by response, or stochastic switching; switching favored when the environment changes infrequently; optimal rates mimic the environmental statistics; a relation between long-term growth and the information available. The Donaldson-Matasci abstract states that a useful measure of the benefit is the increase in the long-term growth rate, and that in many cases the fitness value of a developmental cue, measured that way, equals the mutual information.

The access column still says Crossref 200 for S1–S14. Those DOIs are the first draft's table. Each one returned Crossref 200 on this pass, with the year, family name, and title printed in that draft. Chan's record, doi `10.25088/ComplexSystems.28.3.251`, has two author objects marked first: one has `"name": "Hong Kong"` and no family field; the other has family Chan. The note's "Author family name empty" matches the first object. S12's four cells stay no either way.

The arXiv PDF `1010.5092` is 32 pages. The string "layer" does not occur. The portfolio sentence says mutual information sets a fundamental limit on the value of information, and the next sentence says that bound can be violated when accounting for features such as the stochasticity present at the individual level. Information value and the cost of uncertainty are defined there as differences of long-term growth rates. A later sentence allows different phenotypes to sense differently.

## 3. Repo cross-references

1. **THEORY.md §9** (the dynamics bullet): "Where shocks are shared within a generation, selection on lineage growth favours a mixture of designs (bet-hedging, Cohen 1966), which no per-unit argmin J gives; with independent shocks the two agree (CT42); any E. coli test must name its objective first." The quoted sentence in the note is those words. The same bullet says a ruin threshold fixes the sign of growth but not the ranking (CT43). CT43(iii) is the clause that fixes the sign of time-average growth and does not fix the ranking. The words "large population" are not in that THEORY sentence.
2. **DYNAMICS.md CT42(ii):** with no shared component and a large population, lineage growth tracks the highest per-unit expected factor, so the two objectives agree. CT42(iii) is the shared-shock mixture. CT43(i): for \(W'=W\exp(-(c+w\ell))\), time-average log growth equals \(-(\bar c+w\mathbb{E}[\ell])=-J\) almost surely, and that form assumes every cost, including upkeep \(hK\), is paid as a fraction of the reserve. That assumption is what makes "\(-J\) exactly" true.
3. **GROWTH_BRIDGE.md §2** cites that identity and says it assumes the cost. **§3** states the even-money argmaxes, the difference 0.79, \(\lambda(0.2)=0.020135513551>\lambda(0.99)\), the \(\varepsilon<0.2\) corner, and the exponential map: if \(W=\exp(-\varepsilon C)\), then \(\lambda=-\varepsilon\,\mathbb{E}[C]\) exactly; "This is A2-L when \(C=J\), and it is CT43(i) when every term in \(J\) is paid as a fraction of the reserve. Both statements put the cost into the offspring map. Neither one produces the term list. Neither one produces the cap." **§6** states Theorem GB: under the weak-selection menu, the argmax of \(\lambda\) agrees with the argmax of expected offspring, and that agreement is an agreement of argmaxes, not an identity of the two objectives. The same section marks false: "Maximizing \(\lambda\) in a small-noise limit yields \(J=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L\) subject to \(P(\mathrm{ruin})\le\varepsilon\)." The note's shorter quotation is the opening of that sentence. The same section prints \(\tau_S=0.236207526722\) and \(\tau_E=0.316227766017\) as refresh times on the published path.
4. **GENERAL_FORM.md GF3 (R-a):** risk-neutral expected currency is the extra clause; logarithmic utility is a von Neumann–Morgenstern index and is Kelly's criterion, a different argmin. **§4** says attention as a derived coordinate is false, and quotes THEORY §3's currency list "heat, attention, money, compute." **§7** says an antitone cloud of selected designs does not test the general form. That is the GF5 sentence the note cites.
5. **LAYER_CONVEXITY.md** L1: if decrements are non-increasing, \(K^\star_0(R)=\#\{K\ge 1: R\,d_K>1\}\) is the leftmost minimizer of \(J(K)\propto K+R(1+\varepsilon_K)\), because \(J\) strictly falls while \(R\,d_K>1\) and does not fall afterwards. The citation is Fox 1966. \(R=w E_\infty/h\) is the definition in `theory/LAYERS.md` and in GENERAL_FORM's layer row.
6. **DERIVATION_CHAIN.md** states that the term list, the cap, risk-neutral expected currency, and linear nonnegative prices are assumptions. The section "What is ours versus known" describes the specific sum the note lists, and it says the prior-art search is not exhaustive and that "Not found" is the honest word. Those two clauses sit in the section opener and in the specific-sum bullet, not in one paragraph. Both are in the section the note names. The note does not enlarge the package. V2, in `theory/REPRESENTATION.md`, records that Kelly and Lundberg have different argmins from expected currency on the published path.
7. **CORE.md** line 24: the equation is a definition, assembled from known parts. **THEORY.md §3** keeps the displayed equation as the statement of the problem, not a theorem. **FRAMEWORK.md §9** item 1 is the five-part qualification bar. **PROCESS.md** P10: "The bottleneck is measurement, not mathematics." `theory/FRONTIER_REREAD_2026-11-22.md` is at `8f34f53` and is not on this main. The interiority review on main is headed NOT-INFORMATIVE for the mouse-cortex read-floor comparison. **SCALE_ENDS.md §3.4** marks Kussell and Leibler as the known phenotype-switching form of the hold band, uses the Donaldson-Matasci bound, and says Rivoire and Leibler treat general fitness structures. **INTERNAL_MODEL.md** reads Kussell and Leibler as sensing beating switching when the environment changes fast and sensing is cheap.

The hypothesis line in the note is byte-identical to `THEORY.md` line 41:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

## 4. The three conclusions

1. **No scored row meets all four bars.** A row needs (a), (b), (c), and (d) all yes. In the table at `d0abadc`, (d) for the cost is no on every row, and (b) is never an unqualified yes. Partial is not yes. S17's two calls are the arithmetic-mean call and Cohen's proportional call, which the abstract states, and no term of \(\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L\) picks either dormancy fraction. The other rows are switching rates, one expression level, mutations and fitness, sensing on or off, a stored bit, a person selecting patterns, or accuracy at a compute budget. None of those is a priced layer count against an unpriced information model, with selection set before the design is read.
2. **D1 is a currency question, not a test of the cost.** In the first draft, D1 is the even-money stake menu. The revised note no longer uses the label; T35 still does, for that menu. None of the master-equation terms depends on \(f\). Calling \(f=0.99\) the cost was the risk-neutral clause. Calling \(f=0.2\) Kelly is the growth rate of one fortune, or of a shared coin. CT43(i) puts the cost with Kelly when every term is a fraction of the reserve. The menu separates \(\mathbb{E}[W]\) from \(\mathbb{E}[\log W]\). It does not separate the cost from Kelly.
3. **The closer rival of a priced layer count is an unpriced information model.** Once offspring is a strictly decreasing function of the deterministic cost, including \(W=\exp(-J)\), Kelly and the cost share the argmin. That is CT43(i) and the exponential map. "Buy less when the price rises" is Fox's count once decrements diminish, and it is the same direction as not paying for a cue whose growth value is below its cost. The from-0 count can sit strictly below the number of modes when \(h\) is large, against a rule that keeps one store per mode at every \(h\), or that takes every cue with positive mutual information. The note does not say those papers state \(K^\star_0(R)\), and it does not say the package is new beyond the repository's own "not found."

No claim checked here is stronger than the source it cites. The parked currency sentence does not say the fractional-reserve map is the only case of agreement. CT42(ii) and Theorem GB give agreement of argmaxes without that map. CT43(i) makes the map sufficient for equality.

## 5. Re-review fixes

The re-review at `2ae8486` left four local repairs. All four are in `d0abadc`.

1. THEORY §9 is quoted as "any E. coli test must name its objective first." The large-population clause is named as CT42(ii), not as part of that sentence. The earlier blend "any test must name its objective first" and "with independent shocks and a large population" is gone.
2. The parked wording stops at "Under a shared shock, a strongly selected lineage maximizes log growth." The "only when every term is paid as a fraction of the reserve" sentence is gone from the note and from T36. The next sentences cite CT42(ii) and Theorem GB for agreement without the map, and they say CT43(i) is sufficient for equality and is not the only case.
3. The package sentence is cited from `theory/GROWTH_BRIDGE.md` §6, in the note and in T36. It is no longer cited as GB5.
4. The Rivoire bullet states the portfolio case, the mutual-information limit, and the preprint's next sentence on individual stochasticity. It no longer treats "common to the population" as the hypothesis of the bound.

The preprint author list on `10.1101/2023.07.11.548608` is Weissman, Raynes, and Weinreich. Yin is on the journal record `10.1086/735690`. The note names all four and then the preprint abstract. The abstract sentences the row uses are in that preprint. The re-review recorded the author-list split and did not make it one of the repairs. S20's (d) cell does not depend on Yin.
