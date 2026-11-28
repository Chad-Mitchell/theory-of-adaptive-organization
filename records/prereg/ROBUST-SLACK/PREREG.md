# ROBUST-SLACK preregistration: reserves and copies above the fitted-model minimum

Status: LOCK FILE. Timestamp of record = git commit time of this file on branch `v2.7-robust` (off `main` at
`45a70cf`). Written by one executor for Chad (parent instruction relaying Chad's t2007 question), before any data
for this item were opened, downloaded or looked at. No dataset has been chosen; §6 only lists candidates.
Theory source: `theory/ROBUSTNESS.md` (same branch), results CT37–CT40 (in-model, self-checked, not independently
reviewed). This file is not edited after its lock commit; corrections go in a dated `DEVIATIONS.md` beside it.

## 0. What is predicted, in one line
Strongly selected systems carry a reserve (buffer, or copy count) **above** the minimum computed from a fitted
(plug-in) model of their world, and the excess grows with the uncertainty the system faces about that world (short
record, heavy or uncertain tail), as CT38 derives in-model. This is a consequence of the master equation's chance
constraint evaluated under parameter uncertainty; it is not the hypothesis sentence and it does not test it.

## 1. Qualification (THEORY §3, items (a)–(e))
A class is scored only if all five items of "Strongly selected" are recorded, with sources, in a file committed
**before** any reserve or shock data of that class are opened. A class that does not qualify is labeled
**NOT APPLICABLE (system not qualified)**; its numbers, if computed, are a diagnosis, not a test (the GRID-DX lesson,
PR #113). Classes where a regulator sets the reserve are scored only on systems whose reserve exceeds the regulatory
minimum by more than 5%; the rest are recorded and excluded as regulation-set, not selection-set.

## 2. Quantities (per system i in one class; estimators fixed now)
- **Window τ_i**: the class's fixing (refill / recapitalization / repair) time, preregistered per class with source.
- **Shocks**: the system's per-window net outflows over the record it had before the measurement date.
- **n_i**: the number of non-overlapping windows in that record (the system's own record, not the analyst's).
- **σ̂_i**: sample standard deviation of the shocks (ddof = 1). **ν̂_i**: Hill tail index on the upper 10% of
  shocks (reported; used only in RS-2b).
- **ε**: the class's realized per-window failure frequency, pooled over all scored systems and windows, with a
  Jeffreys 95% interval; if zero failures are observed, ε is the Jeffreys upper bound and RS-1 is INCONCLUSIVE.
- **Plug-in buffer** B_plug,i = z_ε·σ̂_i (z_ε = Φ̄⁻¹(ε), one-sided Gaussian, the CT25 form at H = ½ with the window
  as the unit). **Predictive factor** F_i = t_{n_i−1, 1−ε}·√(1 + 1/n_i) / z_ε (R2-b).
- **B_obs,i**: the reserve held at the measurement date, in the shocks' currency.
- **Ratio** r_i = B_obs,i / B_plug,i.
- **Copies** (only where a class has countable parallel units of one function): n_obs,i; per-unit failure record
  k_i failures in m_i unit-windows; n_plug,i = ⌈ln ε / ln p̄_i⌉ with p̄_i = (k_i + 1)/(m_i + 2).

## 3. Predictions and rules (bootstrap over systems, B = 4000, rng seed 20261120; κ = 0.10 margins)
- **RS-1 (level).** median r_i > 1. PASS iff the 95% interval of the median lies above 1 + κ; FAIL iff it lies
  below 1 − κ; else INCONCLUSIVE. RS-1 alone cannot support the theory over the rival R-fixed below.
- **RS-2a (scaling with record length).** Spearman ρ(ln r_i, ln F_i) > 0. PASS iff the 95% interval lies above
  +0.10; FAIL iff it lies below −0.10; else INCONCLUSIVE. Requires ≥ 20 qualifying systems with n_i spanning at
  least a factor of 4; otherwise UNTESTED.
- **RS-2b (scaling with tail).** Spearman ρ(ln r_i, 1/ν̂_i) > 0, same rule. Reported separately; a PASS here with
  RS-2a FAIL is not support (heavier tails raise the plug-in error even with no uncertainty).
- **RS-3 (copies).** n_obs,i ≥ n_plug,i in at least 80% of scored systems, and the excess n_obs,i − n_plug,i has
  Spearman ρ > 0 with the posterior spread of p_i (Beta(k_i+1, m_i−k_i+1) standard deviation). Same interval rule.
- **RS-4 (common mode, qualitative).** Where a single common cause can take all copies of a function down with
  per-window chance above ε, the theory predicts diverse designs (different mechanisms), not more identical copies
  (R1-c). Scored only if a class has a documented common-cause rate; otherwise UNTESTED.

**Rivals (named now).** R-plug: systems sit at the plug-in buffer (r ≈ 1, no slope). R-fixed: a fixed safety factor
(r constant, no slope in F). R-reg: reserves equal the regulatory minimum. **Support** needs RS-2a PASS (it beats
R-plug and R-fixed); RS-1 PASS alone beats only R-plug.

**What a FAIL means.** RS-1 or RS-2a FAIL in a qualifying class counts against CT38's reading of the chance
constraint for that class (the claim that selection prices parameter uncertainty), not against the hypothesis
sentence by itself. It is recorded as a field result on the instrument used (PROXY-FAIL unless the instrument passes
MV1–MV8). Re-measuring is allowed once before the comparison, never after.

## 4. Known overlap with prior art (stated before data)
Precautionary cash holdings rise with cash-flow risk (Opler, Pinkowitz, Stulz & Williamson 1999, doi
10.1016/S0304-405X(99)00003-3; Bates, Kahle & Stulz 2009, doi 10.1111/j.1540-6261.2009.01492.x). That is risk, not
estimation uncertainty: RS-2a's distinct content is the dependence on the system's own record length at a given
estimated risk. Duplicate genes buffer null mutations (Gu et al. 2003, doi 10.1038/nature01198): that is RS-3's
direction, known; the quantitative ε-based count is what would be new.

## 5. Implication for the GRID diagnosis (stated now; not a test, no grid data opened for this item)
PR #113 labels GB's balancing system NOT APPLICABLE (not qualified) and records a diagnostic gap K_obs − K\* = 3
computed **with ruin slack** (GRID-DX B1). In-model, CT37 and CT38 produce **more copies within a layer and larger
buffers**, at one time constant; neither produces extra **distinct-time-constant** layers (R1 copies sit at one time
constant, as in STORE_NOISE E1-c). So robustness as proved here does **not** explain the three extra layers; at most
it says the GB reserve *volumes* may exceed a plug-in minimum for a reason other than waste. A candidate that could
explain extra speed layers is a cost missing from J's list (a speed–endurance trade-off of actuators: fast units
that cannot run long), which is not in the theory and would have to be added publicly before any future grid test.
Calling part of the gap "robustness" is therefore a hypothesis, untested and, in-model, unsupported for the count.

## 6. Candidate datasets (none opened; access to be checked before any lock of a class)
| Class | Reserve | Shocks / record | Access (unverified) | Caveat |
|---|---|---|---|---|
| US banks | equity capital above the regulatory minimum | quarterly net charge-offs and income; bank age | FDIC BankFind Suite / call reports, public | regulation sets floors (exclusion rule §1) |
| US listed firms | cash and equivalents | operating cash-flow shocks; years listed | SEC EDGAR XBRL financial statement data sets, public | precautionary-cash prior art (§4) |
| Power grids | operating reserve and response volumes (MW) | frequency deviations, imbalance; years of market operation | GB ESO / NESO data portal, Fingrid open data, ERCOT reports, NERC reliability assessments (public PDFs) | GB not qualified (PR #113); few systems |
| Yeast genes | paralog copy number of a function | deletion fitness, per-gene mutation rate | SGD and published deletion screens | copies may be retained for dosage, not failure |
| Insurers | surplus above model-required capital | loss-ratio shocks; years written | aggregates may be paywalled; check before use | regulation (R-reg) |
