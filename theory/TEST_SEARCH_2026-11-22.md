# Test search: a public comparison that can fail (22 November 2026)

*Sunday 22 November 2026, morning ET (America/New_York). Written on branch `test-search-2026-11-22` beside `main` `bb6396f` (PR #172). Revised the same day after the review in PR #174 (`reviews/test_search_2026-11-22/REVIEW.md` on `review-pr173-2026-11-22`). A search note for Chad Mitchell. It is not a lock, not a preregistration, and not a run. No outcome series was opened, and no deposit file was scored. It does not edit `CORE.md`, `THEORY.md`, `measurement/CLAIM_MAP_v2.md`, or any locked file. The open-work entries are T35 and T36.*

**No scored row meets all four bars.** The first draft's two universal sentences do not hold. Graham, Smith, and Simons deposited an arithmetic-mean call against a geometric-mean call, so it is not true that every deposited design has the closest rival making the same call, and it is not true that the comparison on which expected offspring and log growth disagree is absent from public deposits. That comparison is not a test of the cost of judgment. No term in the master equation picks either dormancy fraction, or either stake on the even-money menu. With the reading already in CT43(i), a priced layer count does not separate this cost from Kelly. The closer rival is an unpriced information model, and the qualitative "buy less when the price rises" is already in priced-growth prior art.

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

The sentence is unchanged. A wording that would name the currency is parked in OPEN_WORK T36 and is not adopted.

## 0. What was read, and the question

Read on this branch's base: `theory/DERIVATION_CHAIN.md`, `CORE.md`, `theory/GENERAL_FORM.md`, `theory/GROWTH_BRIDGE.md`, `theory/DYNAMICS.md` (CT42, CT43), `theory/LAYER_CONVEXITY.md`, `measurement/FRAMEWORK.md` §9, `theory/SCALE_ENDS.md` §3.4, and `reviews/lock_2026-11-18/PROCESS.md` (P10: the bottleneck is measurement, not mathematics). `THEORY.md` §9 already says a class must name per-unit \(J\) or lineage growth before a test.

`theory/FRONTIER_REREAD_2026-11-22.md` was read on `frontier-reread-2026-11-22` (commit `8f34f53`) and is not on this `main`. `reviews/prereg_interiority_2026-11-22/REVIEW.md` is on `main` as PR #172. It found the mouse-cortex read-floor comparison not informative. This note does not reopen that deposit. GF5 already says an antitone cloud is not a test of the general form.

The question, fixed before the first draft. Does any public dataset, or a feasible experiment that needs no account, support a comparison that

- (a) can come out the other way,
- (b) has qualification decidable before the design is read, because selection strength and population size are known or set in the protocol,
- (c) has the world's statistics set or measured independently of the design,
- (d) makes a call on which this cost and the closest rival disagree?

A row qualifies only when all four are yes. Partial is not yes. (b) is scored on two bars. The operational bar is population size and selection strength set before the design is read. The five-part bar is FRAMEWORK §9 item 1. No row passes both, together with (d) for the cost of judgment.

## Currency and the real rival

### (a) Log growth and the risk-neutral clause

CT43(i) in `theory/DYNAMICS.md` §4, proved in that model: for the log-reserve map \(W'=W\exp(-(c+w\ell))\), time-average log growth equals \(-( \bar c + w\mathbb{E}[\ell] ) = -J\) almost surely. The same paragraph says this form assumes every cost, including upkeep \(hK\), is paid as a fraction of the reserve, and that this assumption is what makes "\(-J\) exactly" true. `theory/GROWTH_BRIDGE.md` §2 cites that identity and says it assumes the cost. Section 3 of the same note: if \(W=\exp(-\varepsilon C)\), then \(\lambda=-\varepsilon\,\mathbb{E}[C]\) exactly. "This is A2-L when \(C=J\), and it is CT43(i) when every term in \(J\) is paid as a fraction of the reserve. Both statements put the cost into the offspring map. Neither one produces the term list. Neither one produces the cap."

Under that map, the cost in log-growth currency is Kelly growth of a priced cost. The rankings coincide because the map was assumed. They do not coincide in general. CT42, and THEORY §9: where shocks are shared within a generation, selection on lineage growth favours a mixture, which no per-unit argmin \(J\) gives; with independent shocks and a large population the two agree; any test must name its objective first. GF3 (R-a) in `theory/GENERAL_FORM.md`: risk-neutral expected currency is an extra axiom; logarithmic utility is a von Neumann–Morgenstern index and is Kelly's criterion, a different argmin. V2 and the derivation chain record that gap. GB5 marks false the package sentence "maximizing \(\lambda\) in a small-noise limit yields \(J\)." DERIVATION_CHAIN: the term list, the cap, risk-neutral expected currency, and linear nonnegative prices are assumptions. THEORY §3 keeps the displayed equation as the statement of the problem. CORE says the equation is a definition, assembled from known parts.

Replacing the risk-neutral clause by log growth, under shared shocks, is not derived. Under shared shocks without the fractional-reserve map, the rankings differ, and the repository already tells a class to name which one it is using. Under the CT43(i) map they are the same ranking, by the assumption that puts \(J\) into the offspring. The hypothesis sentence is not the place to make that replacement. The wording that would name it, not adopted, is:

"Under a shared shock, a strongly selected lineage maximizes log growth. The risk-neutral cost gives the same ranking only when every term is paid as a fraction of the reserve."

That sentence is OPEN_WORK T36. It is not a change to the sentence at the top of this note, and it is not a new theorem. CT42, CT43(i), and GB5 already say it.

### (b) The closer rival is an unpriced information model

Once the cost is read in the CT43(i) currency, Kelly growth of that same priced cost is not a rival. It is the same ranking. The rival that can disagree is a model that does not charge the layer, the memory, or the read.

What the priced-growth papers already do, from sources opened this session, and from sentences already in the repository:

- Kussell and Leibler, doi `10.1126/science.1114383`. The Europe PMC abstract, re-read this session, says sensing followed by response, or stochastic phenotype switching, are the two routes; stochastic switching can be favored over sensing when the environment changes infrequently; the optimal switching rates then mimic the statistics of environmental changes; long-term growth is related to the information available. The Science PDF was not opened (subscription). An explicit sensing-price formula is therefore not quoted from the article body. The abstract's comparison already treats sensing as a route that can lose, in growth units. `theory/INTERNAL_MODEL.md` already reads the same paper as sensing beating switching when the environment changes fast and sensing is cheap. `theory/SCALE_ENDS.md` §3.4 already marks their result as the known phenotype-switching form of the hold band.
- Donaldson-Matasci, Bergstrom, and Lachmann, doi `10.1111/j.1600-0706.2009.17781.x`, Crossref 200, issued 2010, title "The fitness value of information." The Crossref abstract says a useful measure of the benefit is the increase in the long-term growth rate, and that in many cases the fitness value of a developmental cue, measured that way, equals the mutual information. SCALE_ENDS §3.4 already uses that bound. The PDF was not re-opened.
- Rivoire and Leibler, doi `10.1007/s10955-011-0166-2`. The preprint of that paper, arXiv `1010.5092`, was read as text. Information value and the cost of uncertainty are growth-rate quantities. When information about the future environment is common to the population, mutual information bounds the value, as in a portfolio. The word "layer" does not occur. Different phenotypes may sense differently. SCALE_ENDS already says they treat general fitness structures. This is not a new reading of a layer count.
- Fox 1966, doi `10.1287/mnsc.13.3.210`, Crossref 200, title "Discrete Optimization Via Marginal Analysis." `theory/LAYER_CONVEXITY.md` already credits the from-0 count to that marginal analysis: while decrements are non-increasing, \(J\) falls exactly while \(R\,d_K>1\). "The number of discrete items falls as the price per item rises" is that count. It is not a new comparative static.

So: "memory, or a layer count, falls as a per-layer price \(h\) rises" is Fox's marginal count once the error reductions diminish, and it is the same direction as "do not pay for a cue whose growth value is below its cost" in the papers above. Those papers do not, in the text read this session, state a stack of linear-Gaussian stores, a per-layer upkeep beside a separate memory price and a separate read price, or the ruin cap. The repository already says what the package adds, and this note does not enlarge it. DERIVATION_CHAIN, "What is ours versus known": the specific sum, memory price, upkeep per layer, stake-weighted loss with lateness counted as error, read and link costs, under a hard ruin cap, with the measured world as input. The same paragraph says the searches were not exhaustive and the honest word is "not found." THEORY §9: the ruin constraint fixes the sign of time-average growth and does not fix the ranking (CT43(iii)). GENERAL_FORM §4: attention as a fifth derived bad is false; attention as a name for the currency is THEORY §3's list ("heat, attention, money, compute"), not a new coordinate.

Nothing read this session shows Kussell and Leibler, Rivoire and Leibler, or Donaldson-Matasci stating \(K^\star_0(R)\). The formula is Fox's count on the error decrements the linear-Gaussian model supplies. Applying Fox there is a unification. It is not a new inequality.

### (c) What, if anything, still separates, and what would carry it

Against priced-growth prior art that is allowed to charge for a cue, a sensor, or a discrete item, the direction "buy less when the price rises" does not separate this cost. Against an unpriced rule, one store per environmental mode, or "take every cue whose mutual information is positive," the from-0 count can sit strictly below the number of modes when \(h\) is large. That gap is Fox's count, not a gap between this cost and priced growth.

The ruin cap is the other difference already in the repository. CT43(iii): a long-horizon ruin threshold excludes non-positive time-average growth and does not choose the ranking. V2: the Lundberg exponent and expected currency have different argmins on the published path. A deposit that carried that difference would record two designs inside a slack or binding cap, ranked one way by log growth and another way by the cap, with the world's statistics and the cap set before the ranking is read. No row below is that deposit.

No prediction in the sources read this session separates the cost from priced-growth prior art by a layer count. The prediction that separates it from an unpriced information model is the from-0 count moving with \(h\), and that prediction is Fox's. A later preregistration would have to name Fox, Kussell and Leibler, and Donaldson-Matasci as the rivals before any design is read, and it would have to say which gap is the one that can come out the other way. This note does not register that preregistration.

## 1. The even-money menu is not a test of the cost

On the menu in `theory/GROWTH_BRIDGE.md` §3, win probability 0.6, \(f\in[0,0.99]\), \(W=1+f\xi\), expected offspring is maximized at \(f=0.99\) and log growth at \(f^\star=0.2\). The argmaxes differ by 0.79. Those digits were recomputed in PR #174 and match the growth bridge. The master equation is \(\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L\) subject to a ruin cap. None of those terms depends on \(f\). Calling \(f=0.99\) "the cost" was the risk-neutral clause of GF3. It was not a value of \(\kappa\), \(h\), or \(w\). Calling \(f=0.2\) "Kelly" is right for one fortune, or for a shared coin. CT43(i) puts the cost with Kelly when every term is a fraction of the reserve. The menu therefore separates \(\mathbb{E}[W]\) from \(\mathbb{E}[\log W]\). It does not separate the cost of judgment from Kelly.

The same menu is a bad protocol for a population even as a currency question, for reasons already in the growth bridge. For \(W=1+\varepsilon f\xi\) with \(f\in[0,1]\) and \(\varepsilon<0.2\), the growth maximizer sits on the same corner as expected offspring (`theory/GROWTH_BRIDGE.md` §3). A small fitness modifier has no room to come out the other way. CT42(ii): with no shared component and a large population, lineage growth tracks the highest per-unit expected factor. A population protocol that does not say whether the coin is shared has not stated which call it is testing. The Lundberg numbers \(\tau_S\) and \(\tau_E\) are refresh times on a different path. They are not stakes on this menu.

Graham, Smith, and Simons (row S17) already deposited the arithmetic-mean call against the geometric-mean call. The even-money file \(W=1+f\xi\) was not found as a table. The comparison that file was standing in for is the one in that deposit. Weissman, Yin, Raynes, and Weinreich (row S20) say, in the preprint abstract, that stochastic variation can change the sign relative to deterministic geometric-mean fitness, and that bet hedging can be deleterious at small population size and beneficial at large population size. Identifying a population outcome with \(f^\star=0.2\) is the deterministic geometric-mean call, and their abstract says that call is not enough. Neither paper is a test of \(\kappa\), \(h\), \(w\), or \(K\).

This menu is not a GTAO protocol. It is recorded only as a currency question the repository has already split.

## 2. A priced layer count, after that reading

When decrements are non-increasing, \(K^\star_0(R)=\#\{K\ge 1: R\,d_K>1\}\) with \(R=w E_\infty/h\) is the leftmost minimizer of \(K+R(1+\varepsilon_K)\). That is Fox's marginal count, as LAYER_CONVEXITY states. A large \(h\) leaves the count below the number of positive decrements.

If offspring is a strictly decreasing function of the deterministic cost \(hK+w\mathbb{E}[\ell]\), including \(W=\exp(-J)\), Kelly and the cost share the argmin. That is CT43(i) and the growth bridge's exponential map. It is not the same sentence as "charge \(w\) merit per unit of realized tracking error." A linear penalty on the realized residual need not rank with the expected cost. Recomputed this session, \(W=6-hK-\ell\): design A with \(\ell\in\{0,3\}\) equally likely has \(J=1.5\), \(\mathbb{E}[W]=4.5\), \(\mathbb{E}[\log W]=1.445185878948082\); design B with \(hK=0.4\) and \(\ell=1.2\) certain has \(J=1.6\), \(\mathbb{E}[W]=4.4\), \(\mathbb{E}[\log W]=1.481604540924216\). The cost and \(\mathbb{E}[W]\) pick A. Log growth picks B. PR #174 gave this example; the digits match an independent recomputation. A protocol that charges the realized residual, and a protocol that puts \(\mathbb{E}[\ell]\) inside a deterministic offspring map, are two different predictions. The first draft treated them as one.

Under the deterministic reading, Kelly is the closer rival and (d) against Kelly is no. Mode-matching, one store per mode at every \(h\), is the farther call. Under the realized-residual reading, log growth can disagree with the cost, and that disagreement is again \(\mathbb{E}[\log W]\) against \(\mathbb{E}[J]\), which is the currency question, not a layer formula. Either reading, the protocol does not state one prediction on which the cost disagrees with the closer priced-growth rival.

The rival that the from-0 count does disagree with is an unpriced information model: \(K\) equal to the number of modes at every \(h\), or a cue taken whenever its mutual information is positive. Section "Currency and the real rival" says what that disagreement is, and what it is not.

## 3. Scores

"Unchecked" means a configuration figure the review could not re-read, and that this revision also did not re-open. The (d) cell does not depend on that figure. Outcome files were not opened.

| ID | What is public | (a) | (b) | (c) | (d) for the cost | Contamination | Access |
|---|---|---|---|---|---|---|---|
| S1 Acar 2008 | Two engineered switching rates, periods set by the experiment | yes | partial | yes | no | BIO1, T30 | Crossref 200. No deposit URL |
| S2 Beaumont 2009 | A regime that keeps favoring a new phenotype; the object is a switcher | yes | partial | yes | no | BIO1 | Crossref 200. No deposit URL |
| S3 Stajic 2022 | Epigenetic switcher against a non-switcher. Inoculum \(10^6\) unchecked | yes | partial | yes | no | Kussell–Leibler, from the abstract | Crossref 200. Oxford HTML not re-opened |
| S4 Lambert and Kussell 2014 | Lac memory under an imposed sugar schedule | yes | no | yes | no | Already in the literature map | Crossref 200 |
| S5 New 2014 | Catabolite repression, stable versus variable carbon | yes | partial | yes | no | Geisel; Dekel and Alon | Crossref 200 |
| S6 Dekel and Alon 2005 | One expression level | yes | partial | yes | no | T30 | Crossref 200 |
| S7 Good 2017, LTEE | Serial transfer over 60,000 generations. The transfer regime is set | yes | partial | yes | no | The columns are mutations and fitness, not a layer price | Crossref 200. Sequence files not opened |
| S8 Ketola 2023 | Evolutionary potential under fluctuation | yes | no | yes | no | None | Crossref abstract only |
| S9 Lalejini 2021, Avida | Cap 3,600, copy error 0.0025, periods of 100 updates, sensor on or off | yes | partial | yes | no | The contrast is sensing on or off | Crossref 200. OSF HTTP 200. Files not opened |
| S10 Kumawat 2024, Avida | Mutational neighborhood. Cap 22,500 and copy mutation 0.001 unchecked | yes | partial | yes | no | The object is evolvability | Journal and preprint Crossref 200. OSF HTTP 200. Files not opened |
| S11 Pontes 2020, Avida | A stored bit when the cue refers to the past | yes | partial | yes | no | The hold rule, and any learning model | Crossref 200. Dryad HTTP 200. Files not opened |
| S12 Chan 2019, Lenia | A person selects the patterns | no | no | no | no | None | Crossref 200. Author family name empty |
| S13 Faldor 2024, Lenia | Quality-diversity. Population 32,768 unchecked. The genotype includes the rule | partial | partial | no | no | None | Crossref 200. MIT Press HTML not re-opened |
| S14 NATS-Bench and NAS-Bench-101 | CIFAR-10 cells and accuracy. README: 423,624 cells | partial | no | no | no | Accuracy at a compute budget | NATS-Bench Crossref 200. README HTTP 200. No Crossref DOI for Ying et al. |
| S15 Sekajova 2025 | *C. remanei*, 20°C and 25°C, plasticity or bet-hedging by cue autocorrelation | yes | no | yes | no | The abstract states that split | Journal doi `10.1093/jeb/voaf078`, Crossref 200. Dryad HTTP 200, Crossref 404. Files not opened |
| S16 Raghu 2026 | Yeast heat shocks; persistence of a bet-hedging trait | yes | no | yes | no | Geometric-mean bet-hedging | Journal doi `10.1098/rspb.2025.1913`, Crossref 200. Dryad HTTP 200, Crossref 404. Files not opened |
| S17 Graham, Smith, and Simons 2014 | *Neurospora* dormancy. Arithmetic mean: zero dormancy when a bad year has probability below one half. Cohen: dormancy in proportion to the frequency of bad years | yes, for those two calls | no | yes | no. The two calls are \(\mathbb{E}[W]\) against \(\mathbb{E}[\log W]\). No term of the cost picks either fraction | Cohen 1966, already CL20 | Crossref 200. Dryad HTTP 200, Crossref 404. Files not opened. Article HTML 403 |
| S18 Fridman 2014 | Lag time and the duration of antibiotic exposure | yes | no. The abstract states no population size | yes | no. The call is growth-timing | A growth-optimal delay | Crossref 200. Europe PMC abstract. No supplement opened |
| S19 Bryson and Ofria 2013 | Avida, 3,600 individuals, seven task environments. Extra registers are a treatment | yes | partial | yes | no. Register count is imposed, not an evolved count against \(h\) and a spectrum | Evolutionary potential of an instruction set | Crossref 200. PLOS HTML read for the protocol. Figshare HTTP 202. Files not opened |
| S20 Weissman et al. 2025 | Stochastic phenotype, environment, and reproduction can flip the sign relative to deterministic geometric-mean fitness | yes, for that sign | partial. The preprint abstract uses population size as the parameter that flips the sign; a single \(N\) is not a set design population | yes, in the model | no. The cost has no term that equals geometric-mean fitness | Kelly, Cohen, and the deterministic geometric mean | Journal Crossref 200, abstract empty. Preprint doi `10.1101/2023.07.11.548608`, Crossref 200, abstract read. Their reanalysis was not opened |

S7's (c) cell is yes: the transfer regime is set by the experimenter, independently of which mutations fix. The missing spectrum is why (d) is no, not why (c) is no. The first draft mixed those.

S3's abstract, which Crossref returns, is enough for (d): engineered epigenetic switchers against a non-switcher, favored when the environment fluctuates at rates comparable to the switching rate. The inoculum was not re-read (Oxford HTML 403 in the review; not re-opened here). S10's cap and mutation rate were not re-read (bioRxiv HTML 429 in the review). S13's population was not re-read (MIT Press HTML 403 in the review).

S17's two calls are in the Crossref abstract, including five selection regimes and 12 genetic lineages. The review reports frequencies 0, 25, 30, 40, and 50 percent, a 100 µl aliquot into 1.5 ml, and unknown spore and generation counts. Those method sentences were not re-read here. (b) is no from the sources this pass opened: the abstract states no population size. The review's "unknown" is an additional reason, not re-verified.

S19's 3,600, the 60 by 60 grid, seven environments, and 200 replicates are from the PLOS HTML. The sentence that one treatment supplies more registers is from that same HTML. Figshare files were not opened.

## 4. Verification added in this revision

Bibliographic DOIs below returned HTTP 200 from `https://api.crossref.org/works/{doi}` on 22 November 2026, with the title and first author as printed, except where the abstract field was empty. Dataset DOIs returned Crossref 404 and DataCite 200. Landing pages were requested and the files behind them were not opened.

| DOI | Resolver | Year | First author | Title as returned |
|---|---|---:|---|---|
| 10.1098/rspb.2014.0706 | Crossref 200 | 2014 | Graham | Experimental evolution of bet hedging under manipulated environmental uncertainty in *Neurospora crassa* |
| 10.5061/dryad.8qc20 | DataCite 200, Crossref 404 | 2014 | Graham | Data from: Experimental evolution of bet hedging under manipulated environmental uncertainty in Neurospora crassa |
| 10.1038/nature13469 | Crossref 200 | 2014 | Fridman | Optimization of lag time underlies antibiotic tolerance in evolved bacterial populations |
| 10.1371/journal.pone.0083242 | Crossref 200 | 2013 | Bryson | Understanding Evolutionary Potential in Virtual CPU Instruction Set Architectures |
| 10.6084/m9.figshare.826206 | DataCite 200, Crossref 404 | 2013 | Bryson | Data from: Understanding Evolutionary Potential in Virtual CPU Instruction Set Architectures |
| 10.1086/735690 | Crossref 200 | 2025 | Weissman | Beyond the (Geometric) Mean: Stochastic Models Undermine Deterministic Predictions of Bet Hedger Evolution |
| 10.1101/2023.07.11.548608 | Crossref 200 | 2023 | Weissman | Beyond the (geometric) mean: stochastic models undermine deterministic predictions of bet hedger evolution |
| 10.1093/jeb/voaf078 | Crossref 200 | 2025 | Sekajova | Evolution of phenotypic plasticity during environmental fluctuations |
| 10.1098/rspb.2025.1913 | Crossref 200 | 2026 | Raghu | Avoiding dead ends: the experimental evolution of constraint as adaptation to environmental variation |
| 10.1111/j.1600-0706.2009.17781.x | Crossref 200 | 2010 | Donaldson-Matasci | The fitness value of information |
| 10.1287/mnsc.13.3.210 | Crossref 200 | 1966 | Fox | Discrete Optimization Via Marginal Analysis |
| 10.1016/0022-5193(66)90188-3 | Crossref 200 | 1966 | Cohen | Optimizing reproduction in a randomly varying environment |

Landings this revision: `https://datadryad.org/dataset/doi:10.5061/dryad.8qc20` HTTP 200; `https://doi.org/10.6084/m9.figshare.826206` HTTP 202, redirect to a figshare article page. The Rivoire and Leibler preprint text was read from arXiv `1010.5092` (PDF, 32 pages). The Kussell and Leibler Science PDF was not opened. The Graham article HTML returned HTTP 403. The Fridman abstract was read from Europe PMC. The Bryson and Ofria protocol sentences were read from the PLOS HTML.

The DOIs in the first draft's verification table were not re-queried one by one in this pass, except where a row changed. PR #174 reported Crossref 200 for each of them on the same day, with the printed year, family name, and title.

## 5. What this note does not do

It does not qualify a class. It does not move a CLAIM_MAP row. It does not edit the hypothesis sentence. It does not replace the risk-neutral clause. It does not register a preregistration of the from-0 count, of Fox's count, or of the ruin cap. It does not say that a future Avida run would test the hypothesis in the wild.

The Part 2 hypothesis sentence is the bold sentence under the opening answer.
