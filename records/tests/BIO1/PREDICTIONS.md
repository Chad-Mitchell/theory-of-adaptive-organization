# BIO1 predictions: A Theory of Adaptive Organization at biological scales

Written Saturday 2026-11-14 (ET), BEFORE any numbers were extracted from the sources below.
Committed and sha256-hashed before extraction (see PREDICTIONS.sha256 and git log).

## Honesty note on blindness
This is a literature test, not a blind experiment. The author already knows the outline of
several cited works (Kussell & Leibler 2005, Acar et al. 2008, Lan et al. 2012, Amanna et al.
2007, Fairhall et al. 2001, Robinson et al. 2008, Mayer et al. 2019). Predictions are fixed here
anyway, with pass/fail criteria, so the reading cannot be bent after the fact. Where a source
already states the result, it is prior art and is credited, not counted as a new confirmation.
Numbers recorded in RESULTS.md must come from a fetched paper, abstract or supplement, with a link.

## Theory content being tested (from X_TEXT.txt v9 and THEOREMS.md)
- T1/T1b (drift matching): optimal memory decay / adaptation rate tracks environmental drift.
  Kalman form: gain K ~ sqrt(q/r) (memory time ~ q^-1/2) for diffusive drift; for
  Poisson-switching worlds the optimal switching/forgetting rate ~ the switching rate (exponent ~1).
- Rule 2: keep memory while P(needed) x miss cost > upkeep that rises with drift.
- Rule 7 / T5: watching (and memory) effort rises then falls with drift; none past a cutoff.
- Physics: sensing/remembering accuracy costs free energy in cells (Landauer, Still et al. 2012).
- T4: a shared trace fed by N independent depositors should fade ~sqrt(N) faster.
- Layering (Simon 1962, Kiebel 2008, T3c/T7): multiple memories at different speeds when
  the world has causes at separated timescales.

## Predictions and pass/fail criteria

### P1. Cells: bacterial chemotaxis
- P1a. Energy-accuracy: adaptation accuracy (and/or speed) in E. coli chemotaxis rises with free
  energy dissipated (measured or theory checked against data). SUPPORTS if a primary source
  reports adaptation error falling with dissipation per cycle, with data on the real system.
  CONTRADICTS if accuracy is shown to be independent of energy input.
- P1b. Adaptation time tracks environmental timescales: E. coli adaptation time (or its
  distribution across cells/strains) is of the order of, and tuned to, the timescale of signal
  changes the cell experiences, and fitness/information is maximized where they match.
  SUPPORTS if a source shows performance peaks when adaptation time matches the environment's
  timescale, or adaptation time shifting with environment. CONTRADICTS if performance is
  monotone in adaptation time across realistic environments (no matching).
### P2. Cells: phenotype switching / bet hedging / memory of past environments
- P2a. Switching rates track environment switching rates (Kussell & Leibler 2005 predicts this;
  that is prior art). SUPPORTS if an experiment (e.g. Acar et al. 2008) shows fast switchers win
  in fast-changing environments and slow switchers win in slow ones. CONTRADICTS if the ranking
  does not flip with environment speed.
- P2b. Cellular memory of a past environment persists on a timescale related to how long such
  environments recur, and is lost (faded) when it stops paying. SUPPORTS if a source reports
  memory duration and a fitness benefit that depends on the gap between environments.
  INSUFFICIENT if no measured link to environment timescale.
### P3. Immune memory
- P3a. (direct naive test) Across pathogens/antigens with published antibody half-lives, memory is
  longer for antigenically stable pathogens than for fast-drifting ones. Criterion: the
  stable-antigen group's median half-life exceeds the fast-drifting group's by >= 3x, AND
  half-life is not better explained by a non-drift factor (e.g. replicating vs non-replicating
  antigen). If stable non-replicating antigens (e.g. tetanus/diphtheria toxoids) show half-lives
  as short as drifting ones, record CONTRADICTS-or-CONFOUNDED for the naive form.
- P3b. (rule 2/7 shape) The value of keeping immune memory falls with pathogen drift, and optimal
  memory investment is highest at slow-to-intermediate drift and absent for very fast drift.
  Theory sources (Mayer et al.) are prior art; SUPPORTS only if data (e.g. reinfection intervals
  for seasonal coronaviruses / influenza vs measles) are consistent; reinfection for fast-drifting
  viruses should be driven by antigenic change, with protection to the homologous strain lasting
  longer than protection to drifted strains.
### P4. Ants
- P4a. Layered memories: species using pheromones of different lifetimes use the short-lived one
  for short-lived information (current food, exploitation decisions) and the long-lived one for
  persistent structure (trail network, routes to stable resources). SUPPORTS if a primary source
  measures >= 2 pheromone lifetimes differing by >= 3x with distinct functions matching this
  ordering. CONTRADICTS if the long-lived signal marks ephemeral information.
- P4b. Across species, trail persistence tracks resource persistence (long-lasting trails for
  stable resources such as honeydew/aphids, trees; short trails for ephemeral prey).
  SUPPORTS if a comparative source with measured lifetimes shows this; INSUFFICIENT if only
  anecdotal/qualitative.
- P4c. T4 sqrt(N): evaporation (or trail decay) faster in larger colonies with independent
  depositors. Expected result: INSUFFICIENT (no clean data known); recorded either way.
### P5. Optional: neurons
- P5. Sensory adaptation timescale scales with the timescale of stimulus-statistics changes.
  SUPPORTS if measured adaptation time constants increase with the environment's switching period.
  Secondary (quantitative): log-log slope of memory time vs environment timescale in [0.5, 1.0]
  (T1b diffusive -> 0.5; jump-switching -> ~1). Outside [0.3, 1.2] counts against the T1b form.

## Global kill criterion for this test
If at >= 2 of the 3 required scales (cells, immune, ants) the primary prediction is CONTRADICTS,
record that the biological evidence counts against the theory's drift-matching core.
