# E. coli qualification measurement plan, locked before any re-score or computation

Written Saturday 21 November 2026, about 1:40 AM ET (America/New_York), on branch
`ecoli-measure-2026-11-21` off `main` at `75b58fec282c102efa31b57477301636c6f551fb`.
This file turns §8 of `QUALIFICATION_2026-11-21.md` (recommendations only, merged
in PR #124 as `d63ac23`) into a preregistered measurement plan. The commit that
adds this file is the lock. A later, separate commit on this branch may apply the
rules below to public data and record a verdict. That computation is not part of
this lock, and its numbers are not used to write these rules.

**Class under audit.** Substrate class: *E. coli* (cells and microbes), with the
motility / chemotaxis machinery as the design variable already named in
`QUALIFICATION_2026-11-21.md` and in the CLAIM_MAP qualification-prospect notes
for P1, P3, P4 and P13. Qualification is of a class, not of a single assay
(THEORY §3; FRAMEWORK §9 item 1).

**Objective (DEVIATIONS.md DV2, named before any computation under this plan).**
Selection is taken to act on per-cell growth rate through the cost-to-fitness
map σ. That is the same objective under which P1–P16 were scored and under which
the 21 November qualification check was recorded. The compared statistic is
per-cell values, not the population mean and not the distribution across cells.
Lineage growth G and bet-hedging (CT42; persisters) are not the objective of
this plan.

**Data constraint.** Only already-published public sources. No account creation,
no paywall sign-ins, no contacting labs or authors. A source that cannot be
retrieved under that constraint is unavailable, and the number is not invented.

**Already seen (disclosed; this is not a blind plan).** The writer of this file
has read `QUALIFICATION_2026-11-21.md`, the locked ECOLI-MEM files
(`PREREG.md`, `results.json`, `ecoli_calc.py`), CLAIM_MAP rows P1, P3, P4 and
P13, THEORY §3, and FRAMEWORK §9, including these already-recorded facts:

- Honda et al. 2022 report an *flhD* deletion that “increased growth rate by up
  to 18%” relative to wild type; condition-wise values in SI Appendix Fig. S2E
  were not retrieved in the qualification check.
- Species-wide published *N_e* values already quoted there are of order
  10^8–10^9; a within-host estimate of ≈500–1,700 appears in the Ghalayini
  et al. 2018 official abstract; Berg 1996 records that published *E. coli*
  *N_e* values are not one number.
- No unique σ and no measured 1 − 1/e *T_red* were obtained in that check.
- Locked ECOLI-MEM Arm B predicts τ\* ∈ [1.093, 1.171] s, and the named
  “set at the world’s time scale” rival is τ_v = 1.160 s, which already lies
  inside that range (`results.json`). Measured τ2 = 9.9 ± 0.3 s is the
  historical proxy outcome and is **not** used in any rule below except as
  the already-scored number that a later re-score would revisit.

Those facts are not hidden. They are not used to choose a proxy because it
would make qualification easier.

**Overall rule, written before any computation under this plan.** All five items
(a)–(e) must be **ESTABLISHED**, with the evidence recorded, for the class to
qualify. Vocabulary follows FRAMEWORK §2.2 and the 21 November check:

- **ESTABLISHED:** the locked estimator was applied to retrieved public sources,
  and the item holds.
- **NOT ESTABLISHED:** the item cannot be decided from public data under the
  constraints above (source missing, identification incomplete, or a required
  input not retrievable). This is not a finding that the class fails on
  substance.
- **FAILS:** the locked estimator was applied, and the item fails on substance.
  A class with any FAILS item is **NOT QUALIFIED**.

Overall verdict:

- **QUALIFIED** if and only if (a), (b), (c), (d) and (e) are each ESTABLISHED.
- **NOT QUALIFIED** if any item FAILS.
- **NOT ESTABLISHED** otherwise.

A class that is not shown to qualify “is not evidence either way” (THEORY §3).
P1, P3, P4 and P13 remain untouched in the commit that adds this file, and they
are not re-scored in any later commit on this branch (see §7).

## 1. Item (a): cost-to-fitness map σ

σ is “the fractional change in the class's growth, survival or reproduction
rate per fractional change in *J*” (THEORY §3 (a)). For cells, the parenthetical
“the measured growth-rate cost of the design variable” names the empirical
ingredient, not a substitute for the elasticity (independent review of PR #124).
Energy-budget and proteome shares are not fitness costs and are not used as σ
(QUALIFICATION §2; `figures/face_placements.md`). Schavemaker and Lynch 2022,
Honda et al.'s conversion of a proteome “saving” into a model-based 0.14 h^−1,
Mori et al. 2021 proteome shares, and Lisevich et al. 2025 as a secondary
summary are recorded only as distinct from σ and are not inputs to the
estimator.

### 1.1 Units and terms of *J* for this class (locked)

*J* is the per-cell cost of judgment of the motility / chemotaxis design, in
the currency of the master equation (THEORY §3): holding memory, upkeep, error
stake, acquisition, and sharing, subject to the ruin constraint. For this
qualification, the design variable is that motility / chemotaxis machinery, not
the methylation-layer time constant alone and not the whole-cell energy budget.
σ maps a fractional change in that *J* to a fractional change in per-cell
growth rate (or a competition-fitness equivalent, §1.3).

### 1.2 Perturbation (locked)

The perturbation is a change in investment in the motility regulon:

- **Preferred:** a published titration of *flhDC* (or of flagellar investment)
  that reports growth rate, or a competition-fitness equivalent, at more than
  two investment levels including a neighbourhood of the wild-type design.
- **Fallback, only if no such titration is retrieved:** a complete suppression
  of the motility regulon by deletion of the master regulator (*flhD*, Honda
  et al. 2022; or *flhC*, Ni et al. 2020). Identification I1, locked here in
  advance as QUALIFICATION §8 required: that complete deletion is taken as
  Δ*J*/*J* = 1 for the motility / chemotaxis design cost (the design is
  removed). This is a finite-difference elasticity at a large step, not a
  local slope, and is recorded as such if it is used.

A knockout treated as Δ*J*/*J* = 1 is not used unless I1 is this locked
fallback. I1 is not applied to a mutant that removes only part of the machinery
(*ΔfliC*, *ΔmotAB*) as if it were Δ*J*/*J* = 1.

### 1.3 “No-benefit” world for isolating cost (locked)

Honda’s and Ni’s growth-rate or competition measurements in well-mixed culture
isolate the cost of carrying the design only where motility confers little or
no benefit (Ni et al., “under conditions where motility provides little or no
benefit”). The locked “no-benefit” screen is: the measurement is in batch or
chemostat culture that is well mixed or explicitly stirred, or the paper
states that motility provided little or no benefit in that condition. Gradient,
soft-agar, or other conditions in which motility or chemotaxis is the foraging
path are not used for σ, because Δ*r* then mixes cost and benefit.

### 1.4 Estimators (locked; preferred, then fallback)

**Estimator A (preferred; local slope).** From a retrieved titration in a
no-benefit world, with *J* proxied by the paper’s own investment coordinate
(inducer level only if the paper also reports a measured investment, such as
flagellar protein or motility-gene expression; otherwise the measured
investment itself):

> σ_slope = (Δ*r* / *r*) / (Δ*J* / *J*)

evaluated as a regression slope of ln *r* on ln(investment) in a neighbourhood
of the wild-type investment, or, if only two neighbouring points exist, as the
two-point elasticity at the wild-type end. The investment coordinate is used
only as the denominator Δ*J*/*J*, never as σ itself.

**Estimator B (fallback under I1).** From a retrieved complete *flhD* or *flhC*
deletion in a no-benefit world:

> σ_fd = (*r*_KO − *r*_WT) / *r*_WT

which equals (Δ*r*/*r*) / (Δ*J*/*J*) under I1. If the paper reports a
competition assay rather than a direct growth rate (Ni et al.: 72 h coculture
fractions starting at 1:1), convert to a per-generation selection coefficient
by the paper’s own method if stated; otherwise by

> s = ln(*f*_final / *f*_initial) / *g* − ln((1−*f*_final) / (1−*f*_initial)) / *g*

with *g* the number of generations in the assay, taken from the paper, or, if
the paper does not report *g*, from the assay duration divided by the doubling
time the paper reports for that condition. Then σ_fd = *s* under I1. If the
datasets needed for this conversion are not retrieved, estimator B is not
applied to Ni et al.

**Conservative value.** If more than one valid estimate exists, the value used
for ε is the smallest positive estimate (and, where a paper reports an error
or a condition-wise range, the lower end of that range). A worse measurement
cannot make qualification easier (FRAMEWORK §9 item 1(c)). An upper bound
alone (Honda’s main-text “up to 18%”, without the unread lower end) is **not**
a conservative σ and is not used as the qualification value.

### 1.5 Locked sources for (a)

Primary, already Crossref-verified in the qualification check:

| Role | Source | DOI | What may be used |
|---|---|---|---|
| Fallback Δ*r*/*r* | Honda, Cremer, Mancini, Zhang, Pilizota and Hwa 2022, *PNAS* 119(37): e2110342119 | 10.1073/pnas.2110342119 | Main-text “up to 18%” is an upper bound only. Condition-wise Δ*r*/*r* of the *flhD* deletion, if retrieved from SI Appendix Fig. S2E or from any public SID / source-data file of this paper, may be used under estimator B, in no-benefit conditions only. |
| Fallback competition | Ni, Colin, Link, Endres and Sourjik 2020, *PNAS* 117(1): 595–601 | 10.1073/pnas.1910849117 | Datasets S1–S4 or other public source data of this paper, if retrieved, may be converted under estimator B. Figure values are not read off by eye from a non-retrieved SI PDF. |
| Not σ | Schavemaker and Lynch 2022, *eLife* 11: e77266 | 10.7554/eLife.77266 | Energy-budget shares only; not used as σ. |
| Not σ | Mori et al. 2021, *Mol. Syst. Biol.* 17: e9536 | 10.15252/msb.20209536 | Proteome shares, cited by Honda; not used as σ. |
| Not σ | Lisevich, Colin, Yang, Ni and Sourjik 2025, *Nat. Commun.* 16: 1731 | 10.1038/s41467-025-56980-x | Secondary summary only. |

**Additional public sources, under a locked search, not a free hunt after
seeing numbers.** After this file is committed, a search may add a source only
if all of the following hold: (i) it is a published paper or its public
supplement, retrievable without an account or paywall sign-in; (ii) its DOI is
verified on Crossref before any number is quoted; (iii) it reports, for
*E. coli*, a titration or complete *flhDC* (or *flhD* / *flhC*) suppression
with growth rate or competition fitness in a no-benefit world; (iv) it is
added to the result file with the same quoting rules as QUALIFICATION §9. No
other class of source may be added to σ.

### 1.6 Decision rule for (a)

- **ESTABLISHED** if a positive conservative σ, with a stated range or error,
  is obtained from estimator A, or from estimator B under I1, using only
  retrieved public numbers from the locked source list (including search-added
  sources that met the rule above).
- **NOT ESTABLISHED** if the preferred titration is not retrieved and the
  fallback lower end is not retrieved (in particular, if Honda SI Fig. S2E and
  Ni Datasets S1–S4 remain unavailable, so that only the main-text upper bound
  “up to 18%” is on record).
- **FAILS** if the locked estimators, applied to retrieved no-benefit
  measurements, yield no positive σ (every valid estimate is ≤ 0).

## 2. Item (b): population proxy *N_e*

*N_e* is “the number of independent lineages competing in the same world per
redesign time” (THEORY §3 (b)). “Cells and microbes: measured” does not mean
that any published *N_e* may be plugged in (PR #124 review). Published *E. coli*
values under the name *N_e* are not one quantity (Berg 1996). The world used
for *N_e* and the world used for *T_red* must be the same world (QUALIFICATION
§8).

### 2.1 Locked world and proxy (chosen before using a number as a verdict)

**World:** the species’ shared natural environment, over one redesign time.
The class under audit is *E. coli* as a substrate class, and the design
(motility / chemotaxis) is a species-typical trait. FRAMEWORK §9 cites the
drift barrier of Lynch et al. 2016, whose effective-population-size usage in
this literature is the species-wide diversity *N_e*.

**Proxy:** published Lynch-style species-wide effective population size of
*E. coli* from silent-site diversity or from dN/dS, as reported in the locked
source list below. This is a measured diversity *N_e*, not a direct census of
colonies in one habitat. It is locked as the class proxy because the class,
and the drift-barrier formula the band uses, are species-level. It is not
locked because it is large.

**Not the locked proxy (sensitivity only):** (i) within-host *N_e* of a
colonizing clone (Ghalayini et al. 2018, official abstract ≈500–1,700, pending
full text if publicly retrievable); (ii) Berg’s 10^5–10^8 literature range,
which mixes methods; (iii) a new habitat census, which this plan does not
take, because it would require new data. Sensitivity values are reported and
do not replace the locked proxy, and they are not used to shrink ε.

### 2.2 Locked sources and estimator for (b)

| Source | DOI | Published *N_e* already on record in the qualification check |
|---|---|---|
| Sung, Ackerman, Dillon, Platt, Fuqua, Cooper and Lynch 2016, *G3* 6(8): 2583–2591, Table 1, row *Escherichia coli* | 10.1534/g3.116.030890 | *N_e* = 1.7960 × 10^8, from θ_s = 0.071 and *u*_bs = 2.00 × 10^−10 (Lee et al. 2012, as the paper’s footnote e) |
| Bobay and Ochman 2018, *BMC Evol. Biol.* 18: 153, Additional file 1 Table S1, row “Escherichia coli” (400 strains) | 10.1186/s12862-018-1272-4 | 416,911,778.112 from the universal-gene dN/dS set (0.1 < dS < 0.3); 374,704,250.0 from the core-gene set |
| Lapierre, Blin, Lambert, Achaz and Rocha 2016, *Mol. Biol. Evol.* 33(7): 1711–1725, Table 2 | 10.1093/molbev/msw048 | 1.8 × 10^8, attributed there to Hartl, Moriyama and Sawyer 1994, doi 10.1093/genetics/138.1.227. Use this figure as Lapierre et al.’s attribution unless Hartl’s full text is publicly retrieved and quoted directly. |
| Berg 1996, *Genetics* 142(4): 1379–1382 | 10.1093/genetics/142.4.1379 | Methodological; not a locked point estimate. Full text may be retrieved if public. |
| Ghalayini et al. 2018, *Appl. Environ. Microbiol.* 84(6): e02377-17 | 10.1128/AEM.02377-17 | Sensitivity only. Confirm the ≈500–1,700 method if the full text is publicly retrieved; otherwise quote only the official abstract already recorded. |
| Lynch et al. 2016, *Nat. Rev. Genet.* 17(11): 704–714 | 10.1038/nrg.2016.104 | Drift-barrier citation for the formula; not a source of an *E. coli* *N_e* number in this plan, and not quoted if the full text is not retrieved. |

**Estimator.** The locked *N_e* is the set of species-wide point estimates in
the table above that were read from a retrieved public text (Sung, Bobay, and
Lapierre’s attribution of Hartl). The conservative value used for ε is the
**minimum** of that set. The maximum and the median are reported as the
within-proxy range. No new species-wide estimate may be added unless its DOI
is Crossref-verified, the full text or a public supplement is retrieved, and
the estimate is the paper’s own silent-site or dN/dS *N_e* for *E. coli*; if
added, it enters the min / max / median set. A newly added smaller value can
only widen ε, never narrow it relative to the pre-addition conservative min.

### 2.3 Decision rule for (b)

- **ESTABLISHED** if the locked set contains at least one published
  species-wide silent-site or dN/dS *N_e* for *E. coli*, read from a retrieved
  public text, and the conservative value is a positive number of lineages.
- **NOT ESTABLISHED** if every locked species-wide figure is unavailable
  (this should not occur, because Sung, Bobay and Lapierre were already
  retrieved in the qualification check; if a later audit finds those
  retrievals unreproducible under this plan’s data constraint, the item
  reverts to NOT ESTABLISHED).
- **FAILS** if the locked proxy, so computed, is not a population of
  competing lineages (*N_e* ≤ 1). That is not the expected outcome of the
  locked source list; it is recorded as the substance-fail threshold anyway.

## 3. Item (c): selection-resolvable band ε = 10/(σ·*N_e*)

The factor of 10 above the drift barrier *s*·*N_e* ≈ 1 is “a conservative
choice made here, not Lynch’s” (THEORY §3 (c); Lynch et al. 2016,
doi 10.1038/nrg.2016.104). Lynch et al. is not quoted unless a public full
text is retrieved; the formula used here is the THEORY / FRAMEWORK formula,
not a new reading of that paper.

**Estimator.** Once conservative σ and conservative *N_e* are both
ESTABLISHED:

> ε = 10 / (σ_conservative · *N_e*_conservative)

If a range remains after that conservative choice, the largest ε is the
qualification band width. The prediction band around argmin *J* is at least
this wide, whatever the measurement error, so a worse measurement cannot make
qualification easier.

**Uncertainty.** Report also the range obtained by inserting the within-proxy
min and max of *N_e* and the range of σ, and, as sensitivity only, the ε that
would follow if Ghalayini’s within-host *N_e* were the proxy. Sensitivity ε
does not replace the locked ε and is not used to shrink it.

**Decision rule for (c).**

- **ESTABLISHED** if (a) and (b) are ESTABLISHED and ε is computed as above
  and is positive and finite.
- **NOT ESTABLISHED** if (a) or (b) is NOT ESTABLISHED, or if σ_conservative
  or *N_e*_conservative is not a usable positive number.
- **FAILS** only if (a) and (b) are ESTABLISHED and the formula does not
  yield a positive finite ε. A large ε is not itself a fail of (c); it is
  carried into (d), where a band that cannot exclude a rival fails on
  substance.

## 4. Item (d): power against a named rival

Power requires that “the band, with the measurement error added, must exclude
the design of at least one named rival” (THEORY §3 (d); FRAMEWORK §9 items 1(d)
and 6). Named rivals in FRAMEWORK §9 item 6 are: (R1) design equals a fixed
share of budget; (R2) every read interval ∝ the world’s time scale with
exponent ½; (R3) design equals the world’s time scales with no price
dependence. ECOLI-MEM already named the last of these, as rival “R1” in that
file’s own numbering: memory = τ_v. This plan uses the FRAMEWORK numbering:
that locked rival is **R3**.

The class also preregisters the map from a fractional *J*-gap to a
design-unit band (THEORY §3, “From a cost band to a design band”):

> {𝒟 : *J*(𝒟) ≤ (1 + ε + δ_meas)·*J*\*}

with *H* from this class’s own *J*, so that a fractional gap in *J* allows
about √(2(ε+δ_meas)*J*\* / *H*_ii) in each continuous design variable.

### 4.1 What is and is not a re-score here

Comparing the theory’s **already-locked predicted designs** to a named rival
inside the design-unit band is a qualification power calculation. It does not
use the measured τ2 = 9.9 s, and it does not change P1, P3, P4 or P13. Using
those locked ECOLI-MEM numbers for this comparison is preregistered here, as
QUALIFICATION §8 said a power calculation must be, and is still not a re-score
of the historical proxy outcome.

### 4.2 Scorable rivals (locked)

- **R3, primary, already locked in ECOLI-MEM:** memory = τ_v = 1/λ = 1.160 s
  (Mattingly et al. 2021 inputs as locked). The theory’s predicted design for
  this comparison is the locked Arm B range τ\* ∈ [1.093, 1.171] s
  (`results.json`). **Model-free screen, already known and disclosed:** τ_v
  already lies inside the locked τ\* range, so R3 is not excluded at ε = 0,
  and a positive ε can only widen the band. R3 is therefore **not a rival
  this band can exclude** for the P1 / P3 memory-time prediction. That
  screen is applied as written; it is not waived.
- **R1 (fixed budget share):** scorable only if a mapping from a fixed budget
  share to a design value (a memory time, or a layer count) is already
  present in a locked ECOLI-MEM file or in a public source retrieved under
  the §1.5 search rule. No such mapping is on record in `PREREG.md` or
  `results.json`. This plan does not invent one. If none is found, R1 is
  **not scorable**.
- **R2 (read interval ∝ τ_world^{1/2}):** ECOLI-MEM did not lock a read-interval
  prediction. R2 is **not scorable** unless such a locked prediction is
  already in the ECOLI-MEM files (it is not).
- **One-store rival for P4 only:** ECOLI-MEM’s structural arm already names a
  one-store design as the rival that the two-store (degree-2) prediction
  discriminates against. This rival is scorable if, and only if, a
  comparison of *J*(one-store) and *J*(two-store) can be read from the locked
  Model S files (`PREREG.md`, `ecoli_calc.py`, `theory/LAYERS.md`) without
  introducing a new price or a new term. If that comparison requires a new
  price, the one-store rival is **not scorable**.

### 4.3 Design-unit map and δ_meas (locked)

- If *H* and *J*\* for the continuous memory variable can be computed from
  the already-locked Model S objective in the ECOLI-MEM / `theory/LAYERS.md`
  files, without any new price or term, the design-unit half-width in τ is
  √(2(ε+δ_meas)*J*\* / *H*_ττ), evaluated at the locked τ\*, and δ_meas is
  the fractional spread of *J*\* over the already-locked input box, or zero
  if *J*\* is not computed over that box, in which case the locked τ\* range
  itself is carried as the input-error band in design units.
- If *H* cannot be so computed, no new Hessian is invented, and no
  order-one substitute *J*\* / (*H* τ^{2}) = 1 is used to force a verdict.
  In that case the only design-unit band that may be used is the already-locked
  Arm B range, widened by ε only if a locked conversion exists. Without that
  conversion, power is decided solely by the model-free screen of §4.2
  (exclusion at ε = 0, which does not require *H*).

### 4.4 Decision rule for (d)

- **ESTABLISHED** if (c) is ESTABLISHED, at least one rival in §4.2 is
  scorable, and that rival’s design lies outside the design-unit band around
  the theory’s predicted design, with δ_meas included.
- **NOT ESTABLISHED** if (c) is not ESTABLISHED, or if no named rival is
  scorable under the rules above (including the case that R3 cannot be
  excluded and no other rival can be scored without inventing a price or a
  mapping).
- **FAILS** if every scorable named rival’s design lies inside the
  design-unit band (a band that contains every scorable rival “can neither
  refute nor support anything,” THEORY §3 (d)). The already-disclosed R3
  screen is not by itself a FAILS of (d), because other rivals may still be
  scorable; it becomes a FAILS only if no other scorable rival is excluded.

A FAILS or NOT ESTABLISHED on (d) does not, in this plan, rewrite the
historical P1 / P3 / P4 / P13 proxy labels.

## 5. Item (e): *T_red* and 10 *T_red* of the same world

*T_red* is “the time the class's design takes to close 1 − 1/e of the gap to
its new argmin *J* after a step change in the prices or in the world’s
statistics, measured or preregistered from the class’s turnover” (THEORY §3
(e); CL19 (d) in `theory/DYNAMICS.md`). The lineage must have faced the same
world for at least 10 *T_red*. The world is the world locked in §2.1 (the
species’ shared natural environment). The methylation-layer adaptation time
of order 10 s (Mattingly et al. 2021; already in `PREREG.md`) is the layer’s
own dynamics, not *T_red*.

### 5.1 Estimators (locked; measured first, then a sourced turnover proxy)

**Estimator E1 (preferred; measured closing time).** *T_red* is a published
1 − 1/e (or equivalently fitted exponential) closing time of *E. coli*’s
motility or chemotaxis design after a documented step change in prices or in
the world’s statistics (for example, experimental evolution of flagellar
investment after a change in nutrient or motility regime, fitted to the new
level). The paper must name the trait, the step, and the time (or generation)
coordinate. If several such measurements exist, use the longest *T_red* (a
worse, slower redesign cannot make the 10 *T_red* clause easier).

**Estimator E2 (fallback; turnover proxy, k not invented).** If E1 is not
found in public data,

> *T_red* = *k* × *T*_gen

with the following locked choices:

- *T*_gen is Gibson, Wilson, Feil and Eyre-Walker 2018, *Proc. R. Soc. B*
  285(1880): 20180789, doi 10.1098/rspb.2018.0789, Table 1, wild doubling
  time of *E. coli*: 15 h, s.e. 7.7 h. The conservative *T*_gen used for
  10 *T_red* is the upper end 15 + 2 × 7.7 = 30.4 h. The laboratory 0.33 h
  (20 min) doubling time is the wrong world and is not used. Poulsen,
  Licht, Rang, Krogfelt and Molin 1995, doi 10.1128/jb.177.20.5840-5845.1995
  (40–80 min in mucus in a streptomycin-treated mouse, official abstract)
  is not the locked world and is not used as *T*_gen; it may be reported as
  sensitivity only, and only if the full text or the official abstract is
  the source, as already recorded.
- *k* is **not chosen here as a free number**. It is taken from a published
  public source, Crossref-verified, that reports the number of generations
  for *E. coli* motility or flagellar investment to substantially readjust
  (1 − 1/e, half-change, or the paper’s own fitted timescale) after an
  environmental step. If several *k* are found, the conservative value is
  the largest. If no such published *k* is retrieved, estimator E2 is
  unavailable. In particular, this plan does not set *k* = 1, and it does
  not set *k* from a 1/*N_e* new-mutation fixation time, which is not the
  definition’s “turnover” of an already-present class design.

**Search rule for E1 and for k.** After this file is committed, a public
search may add a source only if: (i) it is published and retrievable without
an account or paywall sign-in; (ii) its DOI is verified on Crossref before
any number is quoted; (iii) it reports a timescale for *E. coli* motility,
flagellar investment, or chemotaxis-design change after a documented
environmental or price step; (iv) the number used is quoted from the
retrieved text. No laboratory outreach.

### 5.2 The 10 *T_red* clause (locked)

Once *T_red* is set by E1 or E2, the clause holds if a retrieved public
source gives a lower bound on how long *E. coli*, or the enterobacterial
motility / chemotaxis design, has occupied the locked world, and that lower
bound is ≥ 10 *T_red*. The bound must be a published time or a published
number of generations, not an informal “the species is old.” If that bound
is in generations, convert with the same conservative *T*_gen. A documented
step change of the locked world’s statistics on a scale shorter than
10 *T_red* would defeat the clause (the GRID audit’s “same world” use of a
measured world statistic is the model for this, not a source of an *E. coli*
number).

### 5.3 Decision rule for (e)

- **ESTABLISHED** if *T_red* is obtained from E1, or from E2 with a sourced
  *k*, and the 10 *T_red* clause holds from a retrieved public lower bound.
- **NOT ESTABLISHED** if no measured closing time and no sourced *k* are
  retrieved, or if *T_red* is obtained but no public lower bound can be
  shown for 10 *T_red* of the locked world.
- **FAILS** if *T_red* is obtained and a retrieved public source shows that
  the lineage has not faced the locked world for 10 *T_red*, or that that
  world’s statistics stepped on a shorter scale.

## 6. Uncertainty propagation (summary)

| Quantity | Conservative input to the next step | What is reported alongside |
|---|---|---|
| σ | Smallest positive valid estimate; lower end of any reported range | Full set of valid estimates and their sources |
| *N_e* | Minimum of the locked species-wide set | Max, median, and the within-host sensitivity |
| ε | 10 / (σ_conservative · *N_e*_conservative) | Range under the within-proxy *N_e* and σ ranges; within-host sensitivity, labelled as such |
| δ_meas | The value that widens the design-unit band, if computed from the locked box | The locked τ\* range, which already carries input-box uncertainty in design units |
| *T*_gen | 15 + 2 × 7.7 = 30.4 h | The point estimate 15 h (s.e. 7.7 h) |
| *k* | Largest published *k*, if any | The set of retrieved *k* |

No Monte Carlo is required. All combinations that matter for the conservative
ε and for 10 *T_red* are reported as a short table in the result file.

## 7. Which re-score becomes allowed, and what this branch must not do

This plan does **not** re-score P1, P3, P4 or P13. No commit on this branch
changes those rows’ statuses, replaces their historical proxy results, or
re-runs a verdict rule on measured τ2.

Once, and only once, a later audit finds that the overall verdict under this
plan is **QUALIFIED** (all five items ESTABLISHED), a **later, separately
opened pull request** may re-score only the already-locked predictions in:

- P1 (ECOLI-MEM Arm B memory versus τ\*),
- P3 (the R3 / “set at τ_v” rival, ECOLI-MEM’s own “R1”),
- P4 (degree-2 world, two-store design),
- P13 (the already-locked up-gradient uptake objective, `PREREG_D.md`).

Rules for that later re-score, locked now:

1. Locked inputs, prediction formulae, and historical proxy numbers are not
   changed. The measured τ2 = 9.9 ± 0.3 s and the locked τ\* box stay as they
   are.
2. The band used in the re-score is the already-locked verdict window,
   widened if needed so that it is at least ε wide in *J* and includes
   δ_meas, converted by the §4 map. A worse (wider) band cannot be narrowed
   after seeing the measured τ2.
3. The historical proxy pass or fail remains in the cell. The headline may
   change from `NOT A TEST (qualification not established; proxy: …)` to a
   qualification-gated status under those locked rules, including the case
   that a widened band makes the test INCONCLUSIVE or still not
   discriminating, in which case it is not converted into a test of the
   hypothesis.
4. P5, P6, P7, P10, P15, P16 and any other E. coli row are not opened by
   this plan. A new prediction (including any use of Tjalma and ten Wolde
   2024, already discussed in `PREREG_NOTES.md`) remains a new preregistration.
5. If the verdict under this plan is NOT ESTABLISHED or NOT QUALIFIED, no
   re-score of P1, P3, P4 or P13 is allowed.

## 8. Kill criteria

**Item-level and class-level (this plan).**

- An item is **NOT ESTABLISHED**, and is not forced to FAILS, when a required
  public source cannot be retrieved without an account or a paywall sign-in,
  when a number is not in the retrieved text, or when an estimator cannot be
  applied without an identification that this file did not lock.
- An item **FAILS**, and the class is **NOT QUALIFIED**, when a locked
  estimator is applied to retrieved public data and the substance threshold
  in that item’s decision rule is met (§1.6, §2.3, §3, §4.4, §5.3).
- Drift-limited misses are excluded by construction of ε and “cannot be
  invoked afterwards” (THEORY §3). This plan does not invoke them.

**Hypothesis-level (not invoked here).** FRAMEWORK §9 items 5 and 7, and
THEORY §3 “What would kill it,” apply only after the class is QUALIFIED and
a subsequent, separately preregistered test is scored. This plan does not
kill the hypothesis, and no result under this plan is treated as a miss or a
pass of P1, P3, P4 or P13.

**Coverage, *n*_min and α, locked for that later test, not used to decide
qualification now.** The class is small (one species-typical design under
audit). For any later qualification-gated test of this class: coverage
*c* = 99.9%, *n*_min = 1, α = 1%. At *n* = 1 this is the FRAMEWORK §9 item 7
example that a single miss has chance probability about 1%. These numbers do
not make the present literature measurement easier, and they do not apply
until the class is QUALIFIED.

## 9. Computation step (separate commit, after this lock)

After this file is committed, and not before, a later commit on this branch
may:

1. Re-verify every DOI used on Crossref.
2. Attempt public retrieval of Honda SI Fig. S2E, Ni Datasets S1–S4, the
   Ghalayini, Berg, Hartl, Poulsen and Lynch full texts, and any search-rule
   sources for a titration, a measured *T_red*, or a sourced *k*.
3. Apply the estimators and decision rules above, in order (a) → (e).
4. Record the values, ranges, and per-item and overall verdicts in a
   separate file, `theory/measured/ecoli/MEASURE_RESULT_2026-11-21.md`,
   clearly labelled as a computation under this lock, not as a change to
   the lock.
5. Update OPEN_WORK T1 to point at the plan and, if computed, the verdict.
   CLAIM_MAP P1, P3, P4 and P13 may gain a pointer to this plan and to the
   result file. Their statuses are not changed on this branch.

If public data do not suffice to compute a conservative σ, or *N_e*, or the
band, the result file says so and leaves the corresponding item NOT
ESTABLISHED. No number is invented to complete a table.

## 10. Sources whose DOIs this plan already relies on

Every DOI below was verified on Crossref in the 21 November qualification
check. They will be re-verified in the computation step before any number is
re-quoted. New DOIs, if added under the search rules, are verified the same
way and listed in the result file.

| Source | DOI |
|---|---|
| Honda et al. 2022 | 10.1073/pnas.2110342119 |
| Ni et al. 2020 | 10.1073/pnas.1910849117 |
| Schavemaker and Lynch 2022 | 10.7554/eLife.77266 |
| Lisevich et al. 2025 | 10.1038/s41467-025-56980-x |
| Mori et al. 2021 | 10.15252/msb.20209536 |
| Sung et al. 2016 | 10.1534/g3.116.030890 |
| Bobay and Ochman 2018 | 10.1186/s12862-018-1272-4 |
| Lapierre et al. 2016 | 10.1093/molbev/msw048 |
| Hartl, Moriyama and Sawyer 1994 | 10.1093/genetics/138.1.227 |
| Berg 1996 | 10.1093/genetics/142.4.1379 |
| Ghalayini et al. 2018 | 10.1128/AEM.02377-17 |
| Gibson, Wilson, Feil and Eyre-Walker 2018 | 10.1098/rspb.2018.0789 |
| Poulsen, Licht, Rang, Krogfelt and Molin 1995 | 10.1128/jb.177.20.5840-5845.1995 |
| Lynch et al. 2016 | 10.1038/nrg.2016.104 |
| Mattingly, Kamino, Machta and Emonet 2021 (locked ECOLI-MEM inputs only) | 10.1038/s41567-021-01380-3 |

Lee et al. 2012 is Sung et al.’s footnote source for *u*_bs and is not
re-quoted here as a new *N_e*. Rocha 2018, doi 10.1093/molbev/msy078, was
already recorded as not open access and is not used.
