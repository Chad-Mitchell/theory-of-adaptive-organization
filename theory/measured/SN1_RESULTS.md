# SN1 results: Model S+ on new systems (rule locked at `d99eade`), and the follow-up SN1-F1 (locked at `fc83d62`)

Friday 20 November 2026, Grok Bot executor for Chad Mitchell. Open sources only; no sign-ins. Self-checked, not reviewed.
The locked rule needs s (store-noise exponent), λ and τ **on the same store**, plus a premise check that the store's
own noise is ≥ 50% of the noise. Systems were checked in the locked order.

## Verdicts: no system is scorable (0 of 7). This is not a pass and not a fail.
| # | System | τ found? | λ found? | s found? | Premise check | Verdict |
|---|---|---|---|---|---|---|
| 1 | Dictyostelium cAMP (Ras adaptation) | yes (Ras returns to baseline in ~30 s) | no in-habitat input statistics | **no**: no source reports Ras-noise amplitude across adaptation times | not checkable | **UNTESTED** |
| 2 | B. subtilis chemotaxis | partial (behavioural adaptation < 1 min; remethylation ~20 min) | no | **no**: no single-cell noise measurement found | not checkable | **UNTESTED** |
| 3 | Yeast Hog1 osmo-adaptation | yes (single-cell adaptation times) | no | **no**: variability of adaptation times is reported, not noise amplitude vs τ | not checkable | **UNTESTED** |
| 4 | Drosophila photoreceptor light adaptation | yes (bump duration 50 → 10 ms with background; Juusola & Hardie 2001, doi 10.1085/jgp.117.1.3) | no | confounded: bump size and duration change together with a 10⁴-fold change in photon rate | **fails**: photon shot noise (exogenous) is the noise source; bumps are its filtered copy | **INVALID** (proxy mismatch) |
| 5 | C. elegans AWC | yes (τ ≈ 17 s, Levy & Bargmann 2020, from a search summary only) | no | **no** | not checkable | **UNTESTED** |
| 6 | Marine run-reverse-flick bacteria (V. ordalii) | borrowed: 1.3 s quoted from V. alginolyticus (Xie, Lu & Wu 2015, doi 10.1016/j.bpj.2014.11.3479) | not in the main text | **no** | see SN1-F1 | **UNTESTED** |
| 7 | Human scale (forecast revision memory) | no | no | no | no | **UNTESTED** |

**What this means.** SN1 is a sound test that cannot yet be run. Its binding input, how a store's own noise scales with
its memory, has been measured (as far as I found) only in E. coli, which is excluded. No verdict, so no diagnosis of a
miss is owed. What SN1 needs is one new measurement per system: noise amplitude and adaptation time in the same cells
across a manipulation of the adaptation enzymes, the design Park et al. 2010 used in E. coli.

## SN1-F1 (the discriminating follow-up, locked at `fc83d62` before looking up V. ordalii's swimming statistics)
**Verdict: INVALID (premise fails, as the locked rule requires).** Brumley et al. 2019 (PNAS 116:10792, doi
10.1073/pnas.1816621116; read via arXiv 1905.07774) fit a "precision factor" Π = 6.6 (range 3–13 under other model
choices; 4.2–8.4 across their variants): the cells' gradient-estimate SD is 6.6× the molecule-counting bound. So counting
noise is about 1/Π² ≈ 2% of the noise variance (0.6–11%), and it is **not** the dominant noise. Also, their adaptation
time (1.3 s) is quoted from V. alginolyticus, a second proxy mismatch. λ was not looked up after this.
**What the INVALID says (diagnosis, not a verdict):** the one counting-noise-limited relative I expected turns out, in its
own authors' fit, to carry noise several times the physical floor, the same qualitative signature as E. coli (noise
beyond counting). Π lumps all noise beyond counting, so this is consistent with store noise but does not show it.
**Next (not preregistered here because it needs a new measurement, not data I could look at):** for V. ordalii, a noise
split (adaptation knockout or CheR/CheB titration with single-cell noise), which would make it SN1-scorable.
