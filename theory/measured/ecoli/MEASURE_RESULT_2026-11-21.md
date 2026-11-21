# E. coli qualification computation under the locked 21 November 2026 measurement plan

Written Saturday 21 November 2026, about 1:50 AM ET (America/New_York), on branch
`ecoli-measure-2026-11-21`. This file is the computation step of
`MEASURE_PLAN_2026-11-21.md`. It is a separate commit after the plan lock
(`6667afd9e89ec0b03cdafe070dadead4b407d37a`, off `main` at `75b58fe`). It does
not change the lock, and it does not re-score P1, P3, P4 or P13.

**Overall verdict, under the locked rule: NOT ESTABLISHED.**

| Item | Verdict | Why |
|---|---|---|
| (a) σ | **NOT ESTABLISHED** | Published Honda SI Appendix Fig. S2E and Ni Datasets S1–S4 were not retrieved (publisher pages returned Cloudflare 403). A bioRxiv submitted version of Honda et al. contains three printed *flhD* knockout growth rates (Fig. S1D), reported below, but that is not the published S2E and is not used as a conservative lower end. No titration slope (estimator A) was obtained as numbers. |
| (b) *N_e* | **ESTABLISHED** | Locked Lynch-style species-wide set, already retrieved in the 21 November qualification check and reused here: conservative *N_e* = 1.7960 × 10^8 (Sung et al. 2016). Range in the locked set: 1.7960 × 10^8 to 4.169 × 10^8. |
| (c) ε | **NOT ESTABLISHED** | Requires (a) and (b); (a) is not established. No qualification band is computed. |
| (d) power | **NOT ESTABLISHED** | (c) is not established. Independently, the locked R3 rival τ_v = 1.160 s already lies inside the locked Arm B τ\* range [1.093, 1.171] s, so R3 cannot be excluded at ε = 0. No other named rival was scorable without inventing a price or a mapping. |
| (e) *T_red* and 10 *T_red* | **NOT ESTABLISHED** | No published 1 − 1/e closing time was found. No sourced *k* meeting the locked definition (1 − 1/e, half-change, or the paper’s own fitted closing timescale of the design) was obtained. One experimental-evolution paper was retrieved under the search rule and is recorded below; it is not used as *k*. |

This is not a finding of **NOT QUALIFIED**. No item FAILS on substance. P1, P3, P4 and P13 are not re-scored.

Post-computation clarification (Saturday 21 November 2026, about 2:13 AM ET, after the independent review of PR #127; disclosed as such, official verdict unchanged): as specified, P1 and P3 cannot discriminate against rival R3 (τ_v = 1.160 s inside the τ\* box [1.093, 1.171] s). So once σ and ε are established, (d) is expected to FAIL unless another scorable rival is excluded, which would make E. coli NOT QUALIFIED under this plan. The present overall verdict stays **NOT ESTABLISHED**. The locked plan’s §4.4 is not edited; the FAILS versus NOT ESTABLISHED collision for the case “R3 inside the box and no other rival scorable” is resolved in `DEVIATIONS_2026-11-21.md`.

The objective remains per-cell *J* through σ, with per-cell values as the compared statistic (DV2), as locked in the plan.

## 0. What was retrieved, and what was not

Every DOI in the plan’s §10 was re-verified on Crossref in this step (all 15 OK; records in the table at the end). Two further DOIs used below were also verified before any number was quoted: Honda et al.’s bioRxiv preprint, 10.1101/2021.05.12.443892, and Plague et al. 2017, 10.1007/s00239-017-9797-5.

**Retrieved in this step, under the plan’s public-data constraint (no account, no paywall sign-in):**

- Honda, Cremer, Mancini, Zhang, Pilizota and Hwa, bioRxiv, posted 12 May 2021, doi 10.1101/2021.05.12.443892 (Crossref type `posted-content`; OpenAlex lists it as the submitted version of Honda et al. 2022). The full PDF was retrieved from `https://www.biorxiv.org/content/biorxiv/early/2021/05/12/2021.05.12.443892.full.pdf` (2,463,587 bytes, `%PDF-1.4`, 27 pages). The published PNAS SI Appendix was not in this file’s figure numbering; the preprint’s corresponding knockout panel is Fig. S1D.
- Ghalayini et al. 2018 full text as PMC HTML, `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5835743/` (PMC5835743). The official abstract’s *N_e* ≈ 500–1,700 and its method are confirmed below. Sensitivity only; not the locked proxy.
- Plague, Boodram, Dougherty, Bregg, Gilbert, Bakshi and Costa 2017, *J. Mol. Evol.* 84(5–6): 279–284, doi 10.1007/s00239-017-9797-5, accepted manuscript as PMC HTML, PMC6002858. Search-rule source for a possible *k*; not used as *k* (see §5).
- Honda et al. 2022 and Ni et al. 2020 main-text JATS XML, already used in the qualification check, were re-retrieved via NCBI eutils (`PMC9478672`, `PMC6955288`). They still do not contain the condition-wise SI numbers or the datasets.

**Sought and not retrieved (Cloudflare 403, 429, challenge pages, or front-matter-only XML):**

- Honda et al. 2022 published SI Appendix Fig. S2E and any PNAS SID file (`pnas.org` supplement URLs returned “Just a moment…” 403; Europe PMC supplement render 403; later bioRxiv supplement URLs 429 after the main PDF had already been fetched).
- Ni et al. 2020 Datasets S1–S4 and SI PDF (same PNAS / Europe PMC 403).
- Hartl, Moriyama and Sawyer 1994 full text (PMC HTML is abstract plus “full text is available as a PDF”; the PDF URL returned an 1817-byte HTML page, not a PDF; eutils XML is front matter only). The 1.8 × 10^8 figure remains Lapierre et al. 2016 Table 2’s attribution, as in the qualification check.
- Berg 1996 full text (PMC HTML and eutils are the official abstract, already quoted). The PDF URL failed in the same way as Hartl’s.
- Poulsen et al. 1995 full text (PMC HTML hit a reCAPTCHA page; eutils front matter only). The official abstract already on record is unused as *T*_gen (wrong world).
- Lynch et al. 2016 full text (Unpaywall `is_oa=False`; not quoted).
- Edinburgh Research Explorer copies of Honda et al. 2022 (Cloudflare 403).
- Mori et al. 2021 and Schavemaker and Lynch 2022 were not re-used as σ, as locked.

No source was added that failed the plan’s search rules. No number was read off a figure that did not print the number, except that preprint Fig. S1D prints the three growth rates in the figure itself; those printed rates are transcribed below and are not used as the qualification σ.

## 1. Item (a): σ — NOT ESTABLISHED

Estimator A (local slope from a titration) was not applied. The retrieved Honda preprint describes a *flhDC* titration (Ptet, cTc inducer) and reports swimming speed, motile fraction, and flagellar number against expression, not a numeric growth-rate series against investment near wild type that could be used as Δ*r*/*r* over Δ*J*/*J*.

Estimator B (complete *flhD* / *flhC* deletion under identification I1) could not be applied to the **published** Honda SI Fig. S2E or to Ni Datasets S1–S4, because those files were not retrieved. The published main text still supplies only the upper bound already recorded: “increased growth rate by up to 18%.” Under the locked rule, an upper bound alone is not a conservative σ.

**Preprint Fig. S1D, reported and not used as the qualification value.** In the 12 May 2021 bioRxiv PDF, Fig. S1D is captioned “Growth rates of motility knockouts lacking the central regulator flhD (flhD-). The increases of growth rate relative to the WT (native flhD) are shown for different carbon sources (11 mM mannose, 20 mM fructose, 20 mM glucose). Growth rates for both, the WT (HE204) and the flhD- (HE275) strain are listed below. Growth measurements were repeated twice per condition and the averages are shown.” The figure itself prints:

| Carbon source | *r*_WT (h^−1) | *r*_flhD− (h^−1) | σ_fd = (*r*_KO − *r*_WT) / *r*_WT |
|---|---|---|---|
| mannose (11 mM) | 0.49 | 0.58 | 0.184 |
| fructose (20 mM) | 0.66 | 0.76 | 0.152 |
| glucose (20 mM) | 0.89 | 0.97 | 0.0899 |

The three finite-difference values are 18.4%, 15.2% and 9.0%, computed from the printed two-decimal rates (mannose 0.09/0.49, fructose 0.10/0.66, glucose 0.08/0.89). The published main-text “up to 18%” is the same study’s wording; 0.184 versus “18%” is a rounding difference at the precision of the printed rates. The paper does not print a standard deviation; it says the averages of two repeats are shown. These measurements are in balanced growth on defined carbon sources, which meets the plan’s no-benefit screen (not a gradient or soft-agar foraging assay).

They are **not** used as conservative σ, for two reasons written into the lock: (i) they are from the submitted preprint’s Fig. S1D, not from the published SI Appendix Fig. S2E, whose numbering and condition set may differ; (ii) the published main text, and the preprint’s own main figures, discuss a broader condition range (including rich defined medium and slower substrates such as aspartate) than the three carbons in S1D, so the smallest of these three (glucose, 0.0899) is not established as the lower end of the published set. Using 0.0899 would risk a σ that is too large and an ε that is too small.

**Verdict (a): NOT ESTABLISHED.**

## 2. Item (b): *N_e* — ESTABLISHED

The locked world is the species’ shared natural environment over one redesign time. The locked proxy is published Lynch-style species-wide silent-site or dN/dS *N_e* for *E. coli*, from the source list in the plan. The qualification check already retrieved the three primary papers; those numbers are reused, not invented.

Locked set:

| Source | *N_e* |
|---|---|
| Sung et al. 2016, *G3* 6(8): 2583–2591, doi 10.1534/g3.116.030890, Table 1, row Ec | 1.7960 × 10^8 (table reports *N_e* × 10^6 = 179.60; θ_s = 0.071, *u*_bs = 2.00 × 10^−10) |
| Bobay and Ochman 2018, *BMC Evol. Biol.* 18: 153, doi 10.1186/s12862-018-1272-4, Table S1, *E. coli*, universal-gene dN/dS set | 416,911,778.112 (4.169 × 10^8) |
| Bobay and Ochman 2018, same table, core-gene set | 374,704,250.0 (3.747 × 10^8) |
| Lapierre et al. 2016, *Mol. Biol. Evol.* 33(7): 1711–1725, doi 10.1093/molbev/msw048, Table 2, attributed to Hartl et al. 1994 | 1.8 × 10^8 (Hartl’s own full text was again not retrieved) |

**Conservative *N_e* (minimum of the locked set): 1.7960 × 10^8.**

Within-proxy range: minimum 1.7960 × 10^8, maximum 4.169 × 10^8, median of the four values 2.774 × 10^8.

**Sensitivity, not used to shrink or replace the locked value.** Ghalayini et al. 2018 full text (PMC5835743) confirms the official abstract. Method: Watterson’s θ_w from chromosomal point polymorphisms, with θ_w = 2 *N_e* *L* μ_g; θ_w = 1.93 ± 1.13, 1.54 ± 0.96 and 1.15 ± 0.78 at days 0, 211 and 315; μ_g in 0.89 × 10^−10 to 3.12 × 10^−10 per base per generation; “we estimated a range of effective population size (*N_e*) between 500 and 1,700.” This is one dominant clone (ED1a) in one healthy human gut, “equivalent to an idealized population of constant size *N_e* of ≈500 to 1,700 individuals.” Berg 1996 full text was not retrieved; the official abstract already on record stands (published *E. coli* *N_e* values are not one number).

**Verdict (b): ESTABLISHED.** The conservative proxy is a positive number of lineages, read from retrieved public texts, under the world and meaning locked before this computation.

## 3. Item (c): ε — NOT ESTABLISHED

ε = 10/(σ_conservative · *N_e*_conservative) is not computed as a qualification value, because (a) is not established. A worse (too-large) σ cannot be plugged in to finish the table. No orientation arithmetic that treats 0.18 or 0.0899 as σ is used as a band.

**Verdict (c): NOT ESTABLISHED.**

## 4. Item (d): power — NOT ESTABLISHED

(c) is not established, so a design-unit band of width ε + δ_meas was not formed.

The plan’s model-free screen, already disclosed at lock from `results.json`, still holds: the locked R3 rival τ_v = 1.160 s lies inside the locked Arm B prediction range τ\* ∈ [1.093, 1.171] s. R3 cannot be excluded at ε = 0, and a positive ε would only widen the band. *H* and *J*\* were not computed from the locked Model S files, because that would have required a new price or term not present in those files; none was invented. R1 and R2 remain not scorable (no locked mapping). The one-store rival for P4 remains not scorable without a *J*(one-store) versus *J*(two-store) comparison already in the locked files.

Because no scorable rival can be shown to lie outside a constructed band, and because (c) is not established, (d) is **NOT ESTABLISHED**, not FAILS. A FAILS would require every scorable rival to have been tested and found inside the band; here the other rivals were not scorable, as the plan allowed.

As specified, P1 and P3 cannot discriminate against rival R3 (τ_v = 1.160 s inside the τ\* box [1.093, 1.171] s). So once σ and ε are established, (d) is expected to FAIL unless another scorable rival is excluded, which would make E. coli NOT QUALIFIED under this plan. That is a consequence of the lock, not a change to the present verdict. The official verdict on (d) stays **NOT ESTABLISHED**. See `DEVIATIONS_2026-11-21.md` (a clarification made after this computation and disclosed as such; the locked plan’s §4.4 is not edited).

**Verdict (d): NOT ESTABLISHED.** This is not a re-score of P1, P3 or P4.

## 5. Item (e): *T_red* and 10 *T_red* — NOT ESTABLISHED

Estimator E1 (measured 1 − 1/e closing time of the motility or chemotaxis design) was not found in the locked sources or in the public search.

Estimator E2 (turnover proxy *T_red* = *k* × *T*_gen) was not applied, because no published *k* meeting the locked definition was obtained. Gibson et al. 2018’s wild doubling time, 15 h (s.e. 7.7 h), conservative *T*_gen = 30.4 h, remains the locked *T*_gen and is unused until a *k* exists. *k* was not set to 1 and was not set from a 1/*N_e* fixation time.

**Search-rule paper retrieved and not used as *k*.** Plague et al. 2017, doi 10.1007/s00239-017-9797-5 (Crossref-verified; PMC6002858 accepted manuscript). In a 4,000-generation shaking-culture experiment, a 274 bp deletion that inactivates *flhDC* (non-motile) was first found at generation 303 at 2% frequency and “became fixed by generation 1305.” From generation 303 to 1200 the wild type’s fitness was 0.991 relative to the mutant, “so this mutation conferred ~1% fitness advantage.” That is a trajectory of one knockout allele toward fixation, not a 1 − 1/e, half-change, or fitted closing time of the class’s typical design after a step change. Under the lock, it is not *k*, and it is not E1.

Without *T_red*, the 10 *T_red* clause is not shown.

**Verdict (e): NOT ESTABLISHED.**

## 6. Re-score and CLAIM_MAP

No re-score is allowed. The overall verdict is not QUALIFIED. P1, P3, P4 and P13 keep their statuses. A later re-score remains possible only if a future computation, under this plan or a new locked plan, finds all five items ESTABLISHED, in a separately opened pull request, as the plan’s §7 already stated.

## 7. Crossref re-verification (21 November 2026, this step)

All of the following returned HTTP-successful Crossref works records (`OK`):

| DOI | Year (Crossref issued) | Used as |
|---|---|---|
| 10.1073/pnas.2110342119 | 2022 | Honda et al. published paper; SI not retrieved |
| 10.1073/pnas.1910849117 | 2019 | Ni et al.; datasets not retrieved |
| 10.7554/eLife.77266 | 2022 | Not used as σ |
| 10.1038/s41467-025-56980-x | 2025 | Not used as σ |
| 10.15252/msb.20209536 | 2021 | Not used as σ |
| 10.1534/g3.116.030890 | 2016 | Locked *N_e* (Sung) |
| 10.1186/s12862-018-1272-4 | 2018 | Locked *N_e* (Bobay) |
| 10.1093/molbev/msw048 | 2016 | Locked *N_e* (Lapierre / Hartl attribution) |
| 10.1093/genetics/138.1.227 | 1994 | Hartl; full text not retrieved |
| 10.1093/genetics/142.4.1379 | 1996 | Berg; abstract only |
| 10.1128/AEM.02377-17 | 2018 | Ghalayini; sensitivity *N_e* |
| 10.1098/rspb.2018.0789 | 2018 | Gibson; locked *T*_gen, unused without *k* |
| 10.1128/jb.177.20.5840-5845.1995 | 1995 | Poulsen; full text not retrieved; not *T*_gen |
| 10.1038/nrg.2016.104 | 2016 | Lynch et al.; formula citation; not quoted |
| 10.1038/s41567-021-01380-3 | 2021 | Mattingly; locked ECOLI-MEM inputs only |
| 10.1101/2021.05.12.443892 | 2021 | Honda preprint; Fig. S1D reported, not used as qualification σ |
| 10.1007/s00239-017-9797-5 | 2017 | Plague et al.; retrieved, not used as *k* |

Ni et al.’s Crossref issued year is 2019; the qualification check already recorded the 23 December 2019 article date and the 7 January 2020 PNAS issue date. No DOI failed verification.
