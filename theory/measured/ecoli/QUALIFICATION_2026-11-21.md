# E. coli qualification under THEORY §3 / FRAMEWORK §9, recorded before any re-score

Written Saturday 21 November 2026, about 12:30 AM ET (America/New_York), on branch
`ecoli-qual-2026-11-21` off `main` at `4398bbdc434b766d4b761aa86d8b8836b0ef8c4c`.
The commit time of this file is the record that the check was written **before any
re-score** of CLAIM_MAP rows P1, P3, P4 or P13. This file does not re-score those
rows, does not change their status, and does not open their locked calculations
for a new verdict.

Landing note (historical header unchanged): this file was written on branch
`ecoli-qual-2026-11-21` off `main` at `4398bbd`, as recorded above. It was later
rebased onto `1727734` and merged in PR #124 as `d63ac23` (confirm review READY).
Current `main` at the time of this note is `fba2827`. No re-score.

**Class under audit.** Substrate class: *E. coli* (cells and microbes), with the
motility / chemotaxis machinery as the design variable named in the CLAIM_MAP
qualification-prospect notes for P1, P3, P4 and P13. Qualification is of a class,
not of a single assay (THEORY §3; FRAMEWORK §9 item 1).

**Objective (DEVIATIONS.md DV2, named before this literature was used for
qualification).** Selection is taken to act on per-cell growth rate through the
cost-to-fitness map σ. That is the same objective under which P1–P16 were scored
(per-cell J; DV2). The compared statistic is not used here: this file does not
score a design. Lineage growth G and bet-hedging (CT42) are not the objective of
this record.

**Selection-temperature extension.** The σ and N_e values recorded below would
also feed a selection-temperature extension (stationary weight exp(−β J), spread
of order 1/(σ·N_e)) being developed on branch `thermo-bridge-2026-11-21`. That
extension is not used in any verdict here.

**Overall verdict: NOT ESTABLISHED.** All five items must hold, with the evidence
recorded, for the class to qualify. Items (a)–(e) are each **NOT ESTABLISHED** as
defined below. This is not a finding that the class fails on substance
(NOT QUALIFIED). A class that is not shown to qualify “is not evidence either
way” (THEORY §3). P1, P3, P4 and P13 remain **NOT A TEST (qualification not
established; …)** as already written. No status is changed.

## 1. What the definition required

Quoted from THEORY.md §3 at `4398bbd`. FRAMEWORK.md §9 item 1 (about line 705)
is the same protocol, not the same wording. Every item had to be recorded before any
measurement, and here before any re-score:

> (a) *a cost-to-fitness map:* σ, the fractional change in the class's growth,
> survival or reproduction rate per fractional change in J (for cells, the
> measured growth-rate cost of the design variable …); no map, no qualification;
> (b) *a population proxy:* N_e, the number of independent lineages competing in
> the same world per redesign time (cells and microbes: measured; …);
> (c) *selection resolves the band:* ε = 10/(σ·N_e) … (the drift barrier is
> s·N_e ≈ 1, with s = σ·ε, Lynch et al. 2016, doi 10.1038/nrg.2016.104; the
> factor of 10 above it is a conservative choice made here, not Lynch's);
> (d) *power:* the band, with the measurement error added, must exclude the
> design of at least one named rival (R1–R3, FRAMEWORK §9);
> (e) *a defined redesign time:* T_red is the time the class's design takes to
> close 1 − 1/e of the gap to its new argmin J after a step change in the prices
> or in the world's statistics, measured or preregistered from the class's
> turnover …; the lineage must have faced the same world for at least 10 T_red.

Named rivals for (d) are FRAMEWORK §9 item 6: (R1) design equals a fixed share of
budget; (R2) every read interval ∝ the world's time scale with exponent ½;
(R3) design equals the world's time scales with no price dependence. The ECOLI-MEM
preregistration (`PREREG.md`) named the last of these as rival R1 in that file's
own numbering (memory = τ_v). That locked test is not re-scored here.

Numbers below are quoted from sources whose DOIs were verified on Crossref in
this work. Where a full text could not be retrieved, that is stated and the
number is not invented.

## 2. Item (a): cost-to-fitness map σ — NOT ESTABLISHED

σ is defined as the fractional change in growth, survival or reproduction rate
**per fractional change in J**. For cells, THEORY §3 points to “the measured
growth-rate cost of the design variable.” A measured growth-rate cost of the
motility regulon exists in the literature, but a unique numerical σ (an
elasticity to J) is not reported, and is not computed here, because that would
require a preregistered identification of J's units and of ΔJ/J for the same
perturbation. Energy-budget and proteome shares are not fitness costs
(`figures/face_placements.md` already notes this) and are not used as σ.

**Measured growth-rate cost of the motility design variable.** Honda, Cremer,
Mancini, Zhang, Pilizota and Hwa 2022, *Proc. Natl Acad. Sci. U.S.A.* 119(37):
e2110342119, doi 10.1073/pnas.2110342119 (Crossref-verified; full text retrieved
as Europe PMC JATS XML, PMC9478672), main-text Results:

> “Particularly, a deletion of the master regulator flhD, which results in the
> complete suppression of motility gene expression, increased growth rate by up
> to 18% compared to the WT strain, with larger increases realized in slower
> growth conditions where motility expression in the WT was higher (SI Appendix,
> Fig. S2E).”

The “up to 18%” figure is therefore a measured finite-difference growth-rate
cost of turning the motility regulon off. The per-condition values sit in SI
Appendix Fig. S2E, which was not retrieved (the journal SI PDF returned 403).
The lower end of the cost, in faster growth conditions, is therefore
unavailable here and is not invented.

**Direct competition fitness, not a single growth-rate percentage in the main
text.** Ni, Colin, Link, Endres and Sourjik 2020 (PNAS issue date 7 January 2020;
article issued 23 December 2019), *Proc. Natl Acad. Sci. U.S.A.* 117(1): 595–601,
doi 10.1073/pnas.1910849117 (Crossref-verified; full text retrieved as Europe PMC
JATS XML, PMC6955288). The paper measures relative reproductive fitness as the
fraction of each strain after 72 h of coculture starting at 1:1 (Results,
“Relative Fitness Cost of Motility Depends on Carbon Source”). Quoted:

> “When the wild type (WT) was cocultured with ΔflhC, a knockout of the master
> transcription activator required for expression of all motility genes, ΔflhC
> consistently outgrew the WT cells, both without (Fig. 1C and SI Appendix,
> Fig. S2 A and B) and with (SI Appendix, Fig. S2D) stirring of the culture.
> Moreover, the fraction of WT cells decreased steadily as the N-value became
> lower (Fig. 1C and SI Appendix, Fig. S2D), which means that the relative
> fitness cost of motility, i.e., growth disadvantage of WT relative to ΔflhC
> cells in the coculture, becomes increasingly high at lower nutrient quality.
> A nearly identical result was obtained for the competition of the WT with
> ΔfliC mutant that lacks only flagellin (SI Appendix, Fig. S2E), demonstrating
> that the fitness cost of motility is primarily due to the biosynthesis of
> flagella (11). Nevertheless, flagellar rotation is also apparently costly
> since the WT was outcompeted by flagellated but nonmotile ΔmotAB cells
> (SI Appendix, Fig. S2F).”

And in the Discussion:

> “The relative fitness cost of motility, i.e., growth disadvantage of motile
> cells under conditions where motility provides little or no benefit, was also
> proportionally higher at lower growth rates. This increasing cost was
> primarily a consequence of higher investment into the biosynthesis of
> flagella, whereas the cost of swimming was also measurable but lower and only
> weakly dependent on the growth rate, and the cost the chemotactic signaling
> was negligible.”

No single numerical growth-rate cost or selection coefficient is stated in the
main text; the values are in Fig. 1C–E and the SI figures. The source data
(Datasets S1–S4 and the SI PDF) were not retrieved (publisher pages returned
403 / challenge pages). Those figure values are therefore not read off here.

**Energy and proteome shares, recorded only as distinct from σ.**

Schavemaker and Lynch 2022, *eLife* 11: e77266, doi 10.7554/eLife.77266
(Crossref-verified; full text retrieved as Europe PMC JATS XML, PMC9323006),
Results (“Bacteria – cost of the E. coli flagellum”) and Table 1:

> “For E. coli, the construction (or growth) and operating (or maintenance)
> costs of the cell are estimated to be 1.57 × 10^10 and 2.13 × 10^8 ATP hr–1,
> respectively (Lynch and Marinov, 2015), and assuming a cell division time of
> 1 hr implies a total cell energy cost of 1.59 × 10^10 ATP. Thus, the costs of
> constructing and operating flagella relative to the whole-cell energy budget
> are 5.0% and 5.2%, respectively.”

Table 1 gives the same relative construction cost 5.0%, relative operating cost
5.2%, and relative total cost 10.2% for *E. coli*, with construction of all
flagella 7.88 × 10^8 ATP cell^–1 and operating cost per cell cycle 8.08 × 10^8
ATP, against a total cell cost of 1.59 × 10^10 ATP (division time 1.0 h; 3.4
flagella per cell). These are calculated energy-budget fractions, not measured
growth-rate costs. The authors themselves note a mismatch between flagellar
operating cost and the cell operating cost (3.8-fold), which they say “could be
due to the variability of E. coli cell volume … or the fact that the flagella
are not continuously rotating.”

Honda et al. 2022 (same paper as above), Discussion, quoting proteome data from
their reference 11 (Mori et al. 2021, *Mol. Syst. Biol.* 17: e9536, doi
10.15252/msb.20209536; that paper was not retrieved here):

> “Quantitatively, flagella proteins comprise ∼3.0% of the total protein mass in
> slow carbon-limited conditions and ∼0.7% in RDM (11).”

They then convert a 2.3% proteome “saving” into a model-based growth-rate gain
of “∼0.14 1/h” using “every percent-of-proteome added to the protein synthesis
machinery results in an ∼0.06 1/h increase in growth rate.” That 0.14 h^–1
figure is not a direct growth-rate measurement of a motility knockout and is
not used as σ.

Lisevich, Colin, Yang, Ni and Sourjik 2025, *Nat. Commun.* 16: 1731, doi
10.1038/s41467-025-56980-x (Crossref-verified; full text retrieved as Europe PMC
JATS XML, PMC11836070), Introduction, is a secondary summary, not a new
measurement:

> “The biosynthesis of the motility apparatus (primarily flagellar filaments)
> consumes several percent of the total cellular protein budget in E. coli and
> other bacteria (2–8% in E. coli, depending on growth conditions)^2,17–20,
> imposing a major burden on cell growth.”

**Verdict (a): NOT ESTABLISHED.** A measured growth-rate cost of the design
variable is on record (Honda et al.: up to 18% when *flhD* is deleted; exact
condition-wise values unread in SI Fig. S2E). A unique σ = (Δ growth rate /
growth rate) / (ΔJ / J) is not given in the literature retrieved here, and is
not invented. “No map, no qualification.”

## 3. Item (b): population proxy N_e — NOT ESTABLISHED

N_e in the definition is “the number of independent lineages competing in the
same world per redesign time.” The literature reports more than one quantity
under the name N_e.

**Species-wide diversity N_e (silent sites or dN/dS), of order 10^8–10^9.**

Sung, Ackerman, Dillon, Platt, Fuqua, Cooper and Lynch 2016, *G3* 6(8): 2583–2591,
doi 10.1534/g3.116.030890 (Crossref-verified; full text retrieved as Europe PMC
JATS XML, PMC4978911), Table 1, row *Escherichia coli* (label Ec):

> θ_s or π_s = 0.071; N_e (× 10^6) = 179.60.

That is N_e = 1.7960 × 10^8, from θ_s = 2 N_e u_bs with u_bs = 2.00 × 10^−10
per site per generation (footnote e: Lee et al. 2012). Pages 2583–2591
(Crossref; fpage 2583 confirmed in the XML).

Bobay and Ochman 2018, *BMC Evol. Biol.* 18: 153, doi 10.1186/s12862-018-1272-4
(Crossref-verified; full text retrieved as Europe PMC JATS XML, PMC6186134;
Additional file 1 / Table S1 retrieved as the journal's ESM xlsx). Main text:

> “Both methods for estimating effective population size yielded similar values
> and indicated that Ne of most bacterial species is on the order of 10^8–10^9.
> (Additional file 1: Table S1).”

(The JATS text runs the superscripts as “108–109”; the values in Table S1 are
of order 10^8–10^9.) Additional file 1, Table S1, row “Escherichia coli”
(400 strains; lifestyle “commensal”):

- N_e from the universal-gene dN/dS set (0.1 < dS < 0.3): 416,911,778.112
  (4.169 × 10^8);
- N_e from the core-gene set: 374,704,250.0 (3.747 × 10^8).

Lapierre, Blin, Lambert, Achaz and Rocha 2016, *Mol. Biol. Evol.* 33(7): 1711–1725,
doi 10.1093/molbev/msw048 (Crossref-verified; full text retrieved as Europe PMC
JATS XML, PMC4915353), Table 2 (“Parameters for E. coli Populations Used in the
Simulations”):

> “Effective population size (Ne)  1.8 × 10^8  Hartl et al. (1994)”

and in the text:

> “The effective population size of the species is estimated at >10^8 (Hartl et
> al. 1994; Lynch 2006).”

Hartl, Moriyama and Sawyer 1994, *Genetics* 138(1): 227–234, doi
10.1093/genetics/138.1.227 (Crossref-verified; PMC1206133). The publisher did
not allow full-text XML, and the PDF was not retrieved (PMC/publisher challenge
pages). The 1.8 × 10^8 figure is therefore cited here only as Lapierre et al.
Table 2 attribute it to that paper, not as a number read from Hartl's own
Table 2. Lynch 2006 was not retrieved.

**The literature already records that published N_e values are not one number.**

Berg 1996, *Genetics* 142(4): 1379–1382, doi 10.1093/genetics/142.4.1379
(Crossref-verified; PMC1207134). Full text was not retrieved; the official
abstract (Europe PMC) is:

> “The selection intensity for codon bias and the synonymous diversity have been
> used in the recent literature to estimate the effective population size of
> Escherichia coli. The results have varied between (10)5 and (10)8. It is
> suggested here that most of this disparity can be explained by a model that
> accounts for the population structure of the species. … the effective
> population size that enters expressions for the codon bias will be that of an
> individual colony, which, if hitchhiking effects are considered, can be a very
> small number. The effective population size that appears together with the
> mutation rate in expressions for the synonymous diversity, on the other hand,
> will be related to the total number of colonies that make up the species and
> can be a very large number.”

**Within-host N_e of a dominant gut clone, much smaller.**

Ghalayini et al. 2018, *Appl. Environ. Microbiol.* 84(6): e02377-17, doi
10.1128/AEM.02377-17 (Crossref-verified; PMC5835743). Full text XML was not
allowed by the publisher; the official abstract (NCBI/Europe PMC front matter)
is:

> “We therefore suggest that ED1a, being well adapted to the healthy human gut,
> evolves mostly neutrally with a low effective population size (Ne of ≈500 to
> 1,700).”

and:

> “These observations support a neutral evolution of E. coli in the human gut,
> compatible with a very limited effective population size that deviates
> drastically with the observations made previously in experimental evolution.”

That within-host range is closer in wording to “independent lineages competing
in the same world” than is a species-wide diversity N_e, but it is one clone in
one host, not a preregistered class proxy, and the full text was not retrieved.

**Verdict (b): NOT ESTABLISHED.** Measured N_e estimates exist, but they are not
a single operational proxy for “independent lineages competing in the same world
per redesign time.” Species-wide values cluster near 10^8–10^9; published
ranges include 10^5–10^8 (Berg abstract); a within-host estimate for one
dominant clone is ≈500–1,700 (Ghalayini abstract). No class-specific choice
among these was preregistered.

## 4. Item (c): selection-resolvable band ε = 10/(σ·N_e) — NOT ESTABLISHED

ε cannot be computed without a unique σ and a unique N_e. The factor of 10
above the drift barrier is “a conservative choice made here, not Lynch's”
(THEORY §3). Lynch et al. 2016, *Nat. Rev. Genet.* 17(11): 704–714, doi
10.1038/nrg.2016.104, was Crossref-verified but is not open access and was not
retrieved; no sentence from that paper is quoted here.

For orientation only, **not as a qualification value, and not by taking Honda's
0.18 growth-rate effect as σ:** if one inserted 0.18 in place of σ in
ε = 10/(σ·N_e) purely to sketch the scale (which would be the identification
ΔJ/J = 1 for a complete motility knockout, which this file does not adopt) with
a species-wide N_e of order 10^8, the arithmetic would be of order 10^−6; with
a within-host N_e of order 10^3, of order 0.06. If the unread lower end of
Honda's SI Fig. S2E is substantially smaller than 18% and N_e is ~500, that
same illustration can be of order 1. Those illustrations are not a band, and
0.18 is not used as σ.

**Verdict (c): NOT ESTABLISHED.**

## 5. Item (d): power against a named rival — NOT ESTABLISHED

Power requires that “the band, with the measurement error added, must exclude
the design of at least one named rival” (THEORY §3 (d); FRAMEWORK §9 items 1(d)
and 6). THEORY §3 also requires the class to preregister the map from a
fractional gap in J to a design-unit band (“the class preregisters this band in
design units, with H from its own J”). No such design-unit band, and no
propagated δ_meas, is recorded for this class in this file. Because (c) is not
established, a band that can be shown to exclude R1, R2 or R3 is not
established either. This file does not convert the locked ECOLI-MEM numbers
into a power calculation that would amount to a re-score.

**Verdict (d): NOT ESTABLISHED.**

## 6. Item (e): redesign time T_red and 10 T_red of the same world — NOT ESTABLISHED

T_red is “the time the class's design takes to close 1 − 1/e of the gap to its
new argmin J after a step change in the prices or in the world's statistics,
measured or preregistered from the class's turnover.” No measured value of that
1 − 1/e closing time for *E. coli*'s motility or chemotaxis design was found.
Generation times, which could later be used to *preregister* T_red from
turnover, are recorded below. They are not themselves T_red until so
preregistered. Item (e) is therefore not established, and the 10 T_red
requirement is not shown.

**Laboratory and wild doubling times.** Gibson, Wilson, Feil and Eyre-Walker
2018, *Proc. R. Soc. B* 285(1880): 20180789, doi 10.1098/rspb.2018.0789
(Crossref-verified; full text retrieved as Europe PMC JATS XML, PMC6015860),
Table 1, row *Escherichia coli*:

> accumulation rate per site per year = 1.44 × 10^−7;
> mutation rate per site per generation = 2.54 × 10^−10;
> DT (h) (s.e.) = 15 (7.7);
> laboratory DT (h) = 0.33;
> ratio = 45.

And in the Results:

> “For example, E. coli can double every 20 min in the laboratory but we
> estimate that it only doubles every 15 h in the wild.”

The Introduction also states: “The bacterium Escherichia coli can divide every
20 min in the laboratory under aerobic, nutrient-rich conditions.” The 0.33 h
laboratory DT in Table 1 is 20 min. The wild estimate is an average over the
natural environment inferred from mutation accumulation, and “may include
quiescence” is not a quote from this paper; the paper's own caveats are the
assumptions that the mutation rate per generation is the same in the wild and
in the laboratory, and that all mutations in the wild are neutral (the authors
argue the second “is not very important”).

**Intestinal generation times (one animal model).** Poulsen, Licht, Rang,
Krogfelt and Molin 1995, *J. Bacteriol.* 177(20): 5840–5845, doi
10.1128/jb.177.20.5840-5845.1995 (Crossref-verified; PMC177407; pmid 7592332).
Full text XML was not allowed by the publisher; the official abstract (Europe
PMC) is:

> “Growth rates of Escherichia coli BJ4 colonizing the large intestine of
> streptomycin-treated mice were estimated by quantitative hybridization with
> rRNA target probes and by epifluorescence microscopy. … we suggest that
> E. coli BJ4 in the intestine consists of two populations, one in the mucus
> which has an apparent generation time of 40 to 80 min and one in the luminal
> contents which is static.”

This is a streptomycin-treated mouse model, strain BJ4, not a general wild
generation time, and the full text was not retrieved.

Physiological adaptation times of the methylation layer (order 10 s in
Mattingly et al. 2021, already in `PREREG.md`) are the layer's own dynamics,
not T_red.

**Verdict (e): NOT ESTABLISHED.** Generation times are recorded and could later
support a preregistered T_red from turnover; the 1 − 1/e redesign time itself
is not measured, and 10 T_red of the same world is not shown.

## 7. Overall, and what this file does not do

All five items are **NOT ESTABLISHED**. The class is not qualified under
THEORY §3 / FRAMEWORK §9. That does not re-score P1, P3, P4 or P13 and does
not convert their historical proxy results into evidence either way.

What is now on record, and can be used later (including by the
selection-temperature extension on `thermo-bridge-2026-11-21`), is the
literature itself: a measured growth-rate cost of the motility regulon of up
to 18% in one study (condition-wise values still unread); species-wide N_e
estimates near 10^8–10^9 alongside a within-host estimate of ≈500–1,700 and a
published 10^5–10^8 range; and generation times of 20 min (rich laboratory
medium), 15 ± 7.7 h (Gibson wild estimate), and 40–80 min in mucus in one
mouse model (luminal cells static).

## 8. Path to establish (recommendations only; to be locked before any re-score)

These are not verdicts and do not qualify the class. They summarise a reviewer's
recommended path to later establish each item, if the evidence supports it. All
of them must be locked before any re-score of P1, P3, P4 or P13.

1. **σ (item a).** Preregister (i) the units and terms of J for this class, (ii)
   the perturbation whose growth-rate (or competition-fitness) change will be
   used, and (iii) how ΔJ/J is measured for that same perturbation. Then retrieve
   Honda SI Fig. S2E for the condition-wise Δr/r of the *flhD* deletion, and/or
   Ni Datasets S1–S4 to convert 72 h coculture fractions into a selection
   coefficient per generation. The honest estimator is a slope near the wild-type
   design (a titration of *flhDC* or of flagellar investment), not a single
   knockout treated as ΔJ/J = 1 unless that identification is locked in advance.
   Do not use Schavemaker energy shares or proteome fractions as σ. Record one
   map, with error, and its source.

2. **N_e (item b).** Preregister, before choosing a number, which operational
   meaning of “independent lineages competing in the same world per redesign
   time” will be used, and name that world. Three live options, which are not
   interchangeable (Berg 1996): (i) species-wide silent-site / dN/dS N_e (Sung,
   Bobay, Lapierre/Hartl: order 10^8–10^9) if the world is the species’ shared
   environment over T_red; (ii) within-host N_e of a colonizing clone, after
   retrieving Ghalayini’s full text to confirm the ≈500–1,700 method, if the
   relevant competition is inside one host; (iii) a new census: the number of
   independently founded, co-circulating lineages in a named habitat over one
   T_red. Lock one proxy, and report the others only as sensitivity. The N_e
   world and the T_red world must be the same world.

3. **ε (item c).** Once unique σ and N_e are locked, compute ε = 10/(σ·N_e). If
   a range remains, take the largest ε (the FRAMEWORK rule that a worse
   measurement cannot make qualification easier). That number is then the
   minimum width of the prediction band.

4. **Power (item d).** Preregister the map from a fractional J-gap to a
   design-unit band, {𝒟 : J(𝒟) ≤ (1 + ε + δ_meas)·J*}, with H from this class’s
   own J (THEORY §3, “From a cost band to a design band”). Name at least one
   rival among R1–R3 (ECOLI-MEM already named memory = τ_v, which is R3). Show
   that the band plus δ_meas excludes that rival’s design. Any use of the locked
   ECOLI-MEM numbers for this comparison is a separately preregistered re-score,
   not an addendum to the present file.

5. **T_red and 10 T_red (item e).** Either measure the 1 − 1/e closing time of
   the motility / chemotaxis design after a documented step change in prices or
   in the world’s statistics (for example, experimental evolution of flagellar
   investment after a change in nutrient regime, fitted to the new argmin), or
   preregister a turnover proxy T_red = k × (a named generation time), with k
   fixed in advance. Name which generation time — laboratory 20 min, Gibson’s
   wild 15 (s.e. 7.7) h, Poulsen’s 40–80 min in mucus, or a new measurement in
   the habitat used for N_e — and then show that the lineage faced that same
   world for at least 10 T_red. Do not use the methylation-layer adaptation time
   (~10 s) as T_red.

## 9. Sources (DOIs verified on Crossref, 21 November 2026)

| Source | Crossref record | Retrieved here as |
|---|---|---|
| Honda et al. 2022 | 10.1073/pnas.2110342119; *PNAS* 119(37): e2110342119 | Europe PMC JATS XML, PMC9478672 (full text) |
| Ni et al. 2020 | 10.1073/pnas.1910849117; *PNAS* 117(1): 595–601 | Europe PMC JATS XML, PMC6955288 (full text). SI / datasets not retrieved |
| Schavemaker & Lynch 2022 | 10.7554/eLife.77266; *eLife* 11: e77266 | Europe PMC JATS XML, PMC9323006 (full text) |
| Lisevich et al. 2025 | 10.1038/s41467-025-56980-x; *Nat. Commun.* 16: 1731 | Europe PMC JATS XML, PMC11836070 (full text); used only as a secondary summary |
| Sung et al. 2016 | 10.1534/g3.116.030890; *G3* 6(8): 2583–2591 | Europe PMC JATS XML, PMC4978911 (full text), Table 1 |
| Bobay & Ochman 2018 | 10.1186/s12862-018-1272-4; *BMC Evol. Biol.* 18: 153 | Europe PMC JATS XML, PMC6186134 (full text); Additional file 1 / Table S1 as the journal ESM xlsx |
| Lapierre et al. 2016 | 10.1093/molbev/msw048; *Mol. Biol. Evol.* 33(7): 1711–1725 | Europe PMC JATS XML, PMC4915353 (full text), Table 2 |
| Hartl, Moriyama & Sawyer 1994 | 10.1093/genetics/138.1.227; *Genetics* 138(1): 227–234 | DOI and bibliographic record only; full text not retrieved. The 1.8 × 10^8 figure is quoted from Lapierre et al. Table 2, which cites this paper |
| Berg 1996 | 10.1093/genetics/142.4.1379; *Genetics* 142(4): 1379–1382 | Official abstract (Europe PMC); full text not retrieved |
| Ghalayini et al. 2018 | 10.1128/AEM.02377-17; *Appl. Environ. Microbiol.* 84(6): e02377-17 | Official abstract (NCBI / Europe PMC front matter, PMC5835743); full text not retrieved |
| Gibson, Wilson, Feil & Eyre-Walker 2018 | 10.1098/rspb.2018.0789; *Proc. R. Soc. B* 285(1880): 20180789 | Europe PMC JATS XML, PMC6015860 (full text), Table 1 |
| Poulsen, Licht, Rang, Krogfelt & Molin 1995 | 10.1128/jb.177.20.5840-5845.1995; *J. Bacteriol.* 177(20): 5840–5845 | Official abstract (Europe PMC, PMC177407); full text not retrieved |
| Lynch et al. 2016 | 10.1038/nrg.2016.104; *Nat. Rev. Genet.* 17(11): 704–714 | DOI verified; full text not retrieved; not quoted |
| Mori et al. 2021 | 10.15252/msb.20209536; *Mol. Syst. Biol.* 17: e9536 | Cited only as Honda et al.'s reference 11 for the 3.0% / 0.7% proteome shares; not retrieved |

**Sought and not used as evidence, or not retrieved.** Rocha 2018,
doi 10.1093/molbev/msy078, was Crossref-verified but is not open access and was
not retrieved. Honda et al. SI Appendix Fig. S2E and Ni et al. SI / Datasets
S1–S4 were not retrieved. No measured T_red (1 − 1/e closing time of a design
gap) was found in the sources above. No unique σ was computed.
