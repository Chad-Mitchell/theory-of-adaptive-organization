# SENSE-CELL-REFEREE: predictions written BEFORE the matched re-scoring is computed

Written by the separate referee (executor for Ace, Chad t1919u/t1920u; out of cycle, unscored). Timestamp of record = git commit time of this file on `q-sensecell-referee`.

## Disclosure (what I had already seen, so this is not a blind test)
- The author's locked outcome (H2 FAIL on proxy, beta 18 [12.5, 26.2] under Method A) and the author's post hoc table: beta 5.0 / 8.2 / 11.2 / 14.6 at eps 0.01 / 0.05 / 0.10 / 0.153 (Method A) and F results (`results_F_posthoc.json`: beta 20.9-160 at eps0 0.33).
- Lan 2012 (PMC free text, Fig 4a/4b image, Methods): eps0 is eps at gamma = 1 (equilibrium); Fig 4a plots eps/eps0; my pixel read puts the SAM x 20% marker at eps/eps0 ~ 0.03 and the BP line at dW = 5.8 kT at ~0.015-0.02; BP slope ln(1e9)/28.5 = 0.727/kT. Fig 4b (by eye): equilibrium run adapts to ~0.80 of a ~0.98 pre-step level. Lan's own whole-cell FRET (strain LJ110 delta(cheY cheZ), wild-type receptors, 50 uM MeAsp, starving cells) reports ~95% accuracy (Fig 5c). The 99% anchor is the Tar-receptor model line and is cited by Lan to Alon et al. 1999 (behavioural).
- Neumann et al. 2014 (PLoS ONE 9:e84904) Fig 1B by eye: wild-type MeAsp precision falls with concentration; ~0.80 near 0.5 mM (this is where Keegstra's 500 uM sits), ~0.9-1.0 below ~10 uM. Their stated cause is saturation of methylation sites. Meir et al. 2010 (Biophys J 99:2766; abstract only, full text not retrieved) report, in Tar-only cells, quantifiable loss of precision at MeAsp as low as 10 uM.
- I did approximate mental beta values at eps 0.05 and 0.01 for eps0 near 0.33 (about 11 and 6) before writing this; so the point predictions below are not independent of that. The interval widths and the verdict labels are not yet computed.

## The matched-measurement question
beta_phys = DG0 / dW_BP(eps). Lan's BP line is the lower envelope over about 10^4 model parameter sets *and over the background ligand s* (Fig 4a legend: log10(s/K_I) drawn from [-10, 10]); at high s the model's own error saturates at eps_c (Fig 3c dashed curves). A measured eps at a stimulus where methylation sites are scarce is therefore not the quantity the BP line bounds. A valid like-for-like reading needs (i) the receptor system the 20%/99% anchor describes (Tar, N = 1 dimer model) or Lan's own whole-cell measurement, (ii) a stimulus at which the dissipation-limited term, not site saturation, sets eps, and (iii) a measured fuel energy. No dataset found gives all three; readings below are the closest.

## Readings and predictions (premises: eps0, alpha, DG0, the eps reading, the bridge)
Intervals will come from Monte Carlo over: eps0 log-uniform [0.18, 0.70] (Fig 4a marker/text 0.33-0.67; Fig 4b 0.18), alpha uniform [0.70, 0.75] (Fig 4a slope 0.727; Keegstra a0 gives 0.717 but a0 normalisation is by response amplitude), DG0 = 29 kT fixed (Lan text, "~29 kT"; the 20% efficiency is not used), eps per reading as stated. Rule: locked mirrored band rule for 'beta <= 10': PASS iff hi <= 8.5, FAIL iff lo >= 11.5, else INCONCLUSIVE. All of this is exploratory because outcomes were known; none of it is a confirmatory re-test.

| Reading | eps used | Predicted central beta | Predicted label | Validity |
|---|---|---|---|---|
| R1 Lan Fig 5c, own whole-cell FRET, wild-type receptors, 50 uM MeAsp | 0.05 (range 0.03-0.08, my assumption: Lan gives '~95%' with no error) | 8-13 | INCONCLUSIVE (interval straddles 8.5-11.5) | closest to a matched whole-array reading; eps is read off a '~' figure |
| R2 Tar anchor, text '~99%' | 0.01 (0.005-0.02) | 5-6 | PASS or INCONCLUSIVE (hi near 8.5) | circular: the 99% / 5.8 kT point is the calibration, so it tests only the 20% efficiency assumption |
| R3 Keegstra 2017 as scored by the author (500 uM MeAsp, VS115 mixed array), ratio of means | 0.21 (bootstrap) | 15-45 | FAIL numerically | NOT a valid reading: stimulus where site saturation dominates; mixed array; the matched-measurement premise fails |
| R4 Neumann 2014 wild-type, MeAsp <= 10 uM, precision read by eye ~0.9-1.0 | 0-0.1 | beta spans <1 to ~17 | non-discriminating (eps unreadable at this resolution) | closer to dissipation-limited regime, but eps not resolved |

Predicted overall: no reading is both valid and discriminating, so H2 as a test of 'beta_phys in [1, 10] at the cell' is INCONCLUSIVE / non-discriminating, the locked FAIL is a measurement-mismatch artefact, and the plain-English answer is 'not established; the closest like-for-like numbers sit at the edge of the band, not clearly inside or outside'.
