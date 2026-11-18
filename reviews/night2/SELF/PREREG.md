# MEASURE-SELF preregistration: GTAO applied to Ace's own memory (Looper store)

Locked: 2026-11-15 (America/New_York), before any outcome below was computed. Git commit time on branch
`night2-self-prereg` of the private repo is the timestamp of record.

## What the author had seen before locking (disclosed)
- Journal schema and counts only: 271 versions, 99 atom ids, version-count histogram, status counts, `from` source patterns.
- The `morning-returns` atom text (Nov 11-15), which lists surfaced atom ids in brackets. I skimmed its first lines (structure) but did NOT tabulate which atoms were surfaced or how often.
- The texts of the 32 `mistake` + 24 `correction` records in `archive/pre-graph-29cf8e4/Chad.jsonl`. **Therefore P5 (miss mechanisms) is unblinded and is labelled EXPLORATORY; it has no pass/fail.**
- No inter-version intervals, drift estimates, split-period statistics or attention regressions had been computed.
- The same agent (Ace) designed Looper (README v0.13+ is derived from GTAO) and wrote this test. That self-selection is a standing limitation: a "pass" on P2 can mean only "Ace follows its own GTAO-derived rule", not that GTAO is true of adaptive systems in general.

## System mapping (operational definitions)
- Item = a journal atom id (`<private-app-repo>/store/journal.jsonl`), excluding the meta-log atom `morning-returns`.
- Held copy = the atom's latest version. Frozen = prior versions + git history + terminal atoms (done/cancelled). Lookup = sources read live and never copied (calendars, Gmail, raw log).
- Change event (drift observation) = a version v>=2 whose `from` is NOT Ace-initiated. Ace-initiated = `from` starting with `review`, `routine`, `eval`, `research`. Versions of one atom with `at` within 60 minutes of the previous counted event are merged into one event (one message split into parts). Time stamp = `at` (when the statement behind the version was made). Timestamps without offset are America/New_York.
- Life of an atom: from its v1 `at` to the earlier of its first terminal-status (done/cancelled) version `at` or the cutoff 2026-11-15T08:00-05:00. Minimum life floored at 0.5 day.
- Drift rate lambda_i = (K_i + 0.5) / L_i, K = change events inside the life window (after v1), L = life in days.
- Stakes W_i (rule, applied to lower-cased `id` + `cues` + `why` of the latest version as of the measurement date; first matching tier wins):
  - 3 if the text matches the high-stakes keyword tier of a private personal-item classifier (bills, health, school and deadline terms; the keyword list is withheld for privacy)
  - 1 if the text matches the low-stakes keyword tier (idea, research and project-note terms; the keyword list is withheld for privacy)
  - else 2.
  Validity: face validity only (no independent rating); reported as a limitation.
- Attention (Ace-initiated pull) = number of the 5 morning-return runs (Nov 11-15) whose bracketed id list includes the atom.
- Sensing class for Ace pulls: reset-type with a per-read price (R1, a = b = 1/2): one read of the source returns the current value exactly. Hence GTAO's effort elasticities: 1/2 in drift, 1/2 in stakes (THEOREMS L1 viii), below the lookup cliff (T8).

## Predictions (locked)

### P1. Drift regime (GTAO §2 core hypothesis: human information environments are scale-free / bursty)
Atoms with >= 3 change events (incl. v1 as the first event). Statistic S = median across atoms of the coefficient of variation of inter-event intervals. Null: for each atom, keep first and last event times and the event count, place interior events uniformly at random (homogeneous Poisson conditional), 10,000 draws.
- GTAO regime B (bursty): S_obs above the null 97.5th percentile -> PASS.
- Single-pace (Poisson) rival: within the null 2.5-97.5% band -> FAIL of regime B (regime A holds).
- Scheduled/periodic rival: below 2.5th percentile -> FAIL.
- n < 8 qualifying atoms -> INCONCLUSIVE.
Secondary P1b (daily panel, all atoms): logistic regression of P(change event on day d) on log(days since last event); GTAO-adjacent band from MATCH1 (need exponents 0.6-0.8 in other human information environments): PASS if slope estimate in [-1.0, -0.5] and 95% CI excludes 0; FAIL if CI excludes [-1.0, -0.5]; else INCONCLUSIVE. Known bias: between-atom frailty makes pooled hazards look more decreasing; reported.

### P2. Attention follows sqrt(drift x stakes) (read-frequency result, prediction 1-2 of the queue item)
Population: atoms with v1 at or before 2026-11-10T23:59, not terminal as of then. Drift and stakes measured on data up to 2026-11-10T23:59 only. Poisson GLM: attention ~ log(lambda) + log(W). 95% CI by 2,000 atom-bootstrap resamples.
- PASS if the drift elasticity CI includes 0.5 and excludes 0.
- FAIL if the CI excludes 0.5.
- INCONCLUSIVE otherwise (e.g. includes both 0 and 0.5).
Rivals compared by AIC on the same rows: (U) uniform/intercept only; (D) deadline salience: indicator that the atom's window (or next repeat) falls in Nov 11-17; (R) recency: log days since last version as of Nov 10; (G) GTAO log(lambda)+log(W); (G+D). Report which wins. Expected a priori: power is low (5 runs).

### P3. Out-of-sample check allocation (normative; predictions 1 and 4)
Split at 2026-11-01T00:00-04:00. Atoms with v1 before the split and not terminal before the split. lambda_hat_i from period 1 (Oct 16 - Oct 31) only. Period-2 change events (Nov 1 - Nov 15 08:00) are the events a pull-checker would need to detect. Budget: on average one check per atom per 7 days over period 2 (sensitivity: 3 and 14 days). Each policy checks atom i periodically with interval T_i, random phase (averaged over 200 phase draws). Loss = sum over period-2 events of W_i x (lag from event to next check), divided by sum W_i over events.
Policies at equal total check count: U uniform; G f_i ∝ sqrt(lambda_hat_i W_i) (GTAO R1); L f_i ∝ lambda_hat_i W_i (linear); S f_i ∝ W_i (stakes only); R f_i ∝ 1/(days since last version at split) (recency).
- Drift persistence P3a: Spearman rho between period-1 and period-2 change rates > 0 with 95% bootstrap CI excluding 0 -> PASS (drift is a stable, predictable property, a precondition for any drift-based allocation).
- P3b: PASS if G has loss ratio G/U < 1 with 95% atom-bootstrap CI excluding 1 AND G is not beaten by L, S or R with a CI excluding 1. FAIL if G/U >= 1 (CI excluding 1 on the high side) or another policy beats G with CI excluding 1. Else INCONCLUSIVE.
Validity caveat (declared): change events are when Chad *told* Ace, not when the world changed; Ace mostly learns by push, not pull. P3 therefore evaluates a counterfactual pull policy with statement time as a lower bound on change time.

### P4. Freeze/hold split (T8 consistency, weak)
- P4a: terminal (done/cancelled) atoms should almost never change again (frozen copies drift ~0). PASS if < 5% of terminal atoms receive a later non-Ace change event; FAIL if > 15%.
- P4b: frozen history is cheap but sometimes needed (T8/R4 keep-all): report count of reverts/restores in looper git history per 100 commits; no threshold (descriptive).

### P5. Miss mechanisms (EXPLORATORY, unblinded)
Code each documented miss (Chad.jsonl `mistake`/`correction` records, plus later documented misses found in the repos) into one mechanism: S stale working copy (acted from a context/memory copy without rereading a source that had changed or could have), N never written (write omission), P promise without edit (stated change not made), C context-loss (settled fact forgotten across sessions), R return/routing (correct copy existed but not surfaced), J judgment/inference error (no memory failure), T tooling/code bug. GTAO-motivated expectation: S + C (copy older than its drift / reread skipped) is the largest memory-caused share. A deterministic keyword coder is run as a second coder; agreement (Cohen's kappa) is reported. No pass/fail.

## Reporting
Every result reported as PASS / FAIL / INCONCLUSIVE on its locked criterion, with n, CI, measurement-validity label (VALID / PARTIAL / PROXY) and limitations. Any deviation from this plan is labelled POST-LOCK.
