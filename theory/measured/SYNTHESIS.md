# Synthesis of the measured program so far (v2.60, Friday 20 November 2026, about 11:50 AM ET)

A self-check by one executor for Chad, not an independent review. Every verdict below was scored by a rule
committed before its data were computed; deviations were committed before outcomes and are listed in each file.

## Per-test verdicts
| Test | Claim tested | Verdict | Source |
|---|---|---|---|
| E. coli memory (first placement) | Slow layer's memory = Model S optimum (1.09–1.17 s) | **FAIL on proxy** (measured 9.9 s, 8.5×); rival "set at" fails too; structure (degree 2 → two stores) weak pass | `README.md` |
| F2 (store-noise exponent) | Store noise fixed vs scaling as sensing noise | **INCONCLUSIVE** (s = 0.31, CI 0.24–0.37: neither locked model); rerun optimum 1.9–3.6 s | `ecoli/RESULTS_F2.md` |
| SN1 / SN1-F1 | λτ ≥ (1−s)/(2s) on new systems | 0/7 scorable; SN1-F1 **INVALID** (V. ordalii noise is not counting noise) | `SN1_RESULTS.md` |
| Follow-up D (E. coli gap) | Drift objective / speed price / habitat mode | Drift **ruled out**; speed price only at the box corner; habitat mode **open**; Y4 untested | `ecoli/RESULTS_D.md` |
| GRID-1 (CE 2022) | Count by degree + interlacing | **INVALID** (premise: mFRR coverage 0.666); count and fast arms INVALID in advance (closed loop) | `grid/RESULTS_GRID1.md` |
| GRID-1b (CE 2022) | Slowest world mode slower than the slowest layer, not set at it | **PASS on proxy** (65 min vs 15 min; rival fails); one low-risk arm | same |
| GRID-2 (GB 2026) | Count by degree + interlacing | **G1 FAIL on proxy**: random-walk imbalance (γ = 2.09) ⇒ one layer; GB runs four. Interlacing not scored | `grid/RESULTS_GRID2.md` |
| G3a (GB 2024) | Replication of GRID-2 | **Replicates the FAIL** (γ = 2.02; thin BIC margin) | `grid/RESULTS_GRID3_4.md` |
| GRID-4 (GB 2019/20 vs 2026) | Actuation-set vs world-set layer times | **INVALID** (verdict depends on an assumed, unsourced 2019 response holding) | same |
| GRID-4b | GRID-4 with sourced holdings | **UNTESTED** (no open 2019/20 MFR holdings) | same |
| GRID-S S1 (GB) | Market-step account predicts a 30-min mode | **M-S1 FAIL** (no corner in [1,300, 2,900] s) | `grid/RESULTS_GRID2.md` |
| GRID-S S2 (DE 2026, 15-min products) | World vs market account of the German slow mode | **W-S2 PASS** (dominant mode 2,956 s, CI 2,626–3,352 s; no 16-min mode); thin margin | `grid/RESULTS_GRID_S.md` |

## What each failure taught (causal, not rescue)
- **E. coli memory (8.5× too long):** Model S lacks a term for a store's own noise. The binding noise is
  internal (its correlation time ≈ the memory). Measuring that noise's scaling (s = 0.31) closes 37 % of the log
  gap. The remaining factor of 3–5 is not the drift objective. A slow habitat mode or speed-priced upkeep could
  close it; neither is measured.
- **GRID-1 (INVALID):** closed-loop grid data cannot show the pre-control world below the slowest loop's time
  scale without tie-line/ACE data. Any grid test needs a single synchronous area, or published area-control
  error.
- **GRID-2 / G3a (count FAIL, replicated):** where the reconstruction is open-loop, GB's imbalance has no
  separated time scales. Post-hoc diagnosis (stated after the miss, candidly): grid layers are tiered by
  actuation (delivery speed, energy duration) and by deviation size (ruin products such as DC). Frequency is
  read almost without noise, so the trade-off Model S optimizes (memory against read noise) is not what binds.
  The speed-price escape fails in GB (slower DR costs more than DC).
- **GRID-4 (INVALID) / GRID-4b (UNTESTED):** the direct test of that diagnosis needs 2019/20 response holdings that
  are not published openly. The slow band (γ 2.02–2.09 in 2019/20, 2024 and 2026) stayed the same while the
  products changed tenfold. That fits the actuation account but was not the locked criterion.
- **GRID-S:** the German slow mode is not an artifact of hourly market products (it did not move when products went
  to 15 min, and GB shows no 30-min mode). The slow-mode arm is about the world, as the theory reads it.

## Scope rule G3b (from 20 Nov 2026, forward only)
A system qualifies for Master Theorem (iii) only if (1) read noise is non-negligible (≥ 10 % of the tracked
signal's variance at the layer's time scale), and (2) ruin is slack (no layer triggered only by a deviation
threshold; such layers are excluded from the count before scoring). G3b was written after the GRID-2 miss. It is
not applied retroactively: GRID-2's FAIL stands.

## Honest state of the law
- **Layer count by degree, (iii):** **refuted on proxy outside its stated premises** (grids: robust, replicated). The
  preregistered kill condition is **not met** (it also needs an open-loop CE seconds-level FAIL). Inside its premises
  (sensing-limited, ruin slack) the count is **untested** by any qualifying test.
- **Layer timing (memory faster than its mode, interlacing):** **failed on proxy** in E. coli by 8.5× (reduced to
  3–5× by a measured store-noise term); **passed on proxy** in the grid's one low-risk slow arm (CE 2022, supported
  by S2). **Not refuted:** no test met the class's qualifying conditions (closed cost list, fitness map).
- **Overall:** not refuted; untested in scope; two proxy failures with specific diagnoses, one diagnosis
  (actuation-limited layers) itself untested.

## The single most decisive next test
**A designed-world experiment inside the scope:** an agent (human, animal, or E. coli in microfluidics) tracking a
signal whose spectrum the experimenter sets, crossed with a read-noise level the experimenter sets.
- **Conditions:** one OU mode, two separated modes, and a random walk.
- **Measurements:** read noise is measured by design, the world is known exactly (so no circularity, no
  closed-loop reconstruction), and the agent's memory kernel is estimated from its responses (number of time
  constants by degree, and their values).
- **Predictions:** one store for one mode or a random walk; two stores for two modes, each faster than its mode
  and interlaced; memory shortening as read noise falls, with the predicted λτ\*.
- **Kill:** a two-store kernel for a single-mode world, or stores slower than their modes, across noise levels.
- **What it would take:** a lab partner and ethics approval. For humans: a two-condition online tracking task, about
  100 participants, with an IRB and a recruitment account, which needs Chad and his collaborators (no account
  creation here). For E. coli: the F2/Y4 measurements at the Emonet or Cluzel/Park lab (`OUTREACH_DRAFT.md`,
  not sent).
