# WF-HSV results

**Scored:** Friday 20 November 2026, 11:17 PM ET (America/New_York), strictly against `PREREG.md` locked 20 November 2026, 9:54:48 PM ET.
**Integrity:** prereg SHA-256 `9592042bc2932acec025315c5f34d401ad896a76f16940ee12c43d4be5a7bb05` (re-hashed at scoring; matches the lock). Predictions SHA-256 `ba66cef743bec29d0c2292f9b4d25c0596726623d52a05b8d881d3420fe612d1`, written before official start 9:57:06 PM ET (`START.txt`), re-hashed and matched. Deviation D1 (exclusion parser, before start) in `DEVIATIONS_2026-11-20.md`. The run finished 11:17:54 PM ET, 64/64 worlds, no restart. T20 holographic worlds and the 21 rhythm-test worlds were not scored. No push of results was made from the workdir; this file is the official writeup.
**Rule:** \(K^*_{\mathrm{WF}}=\#\{i:R\delta_i>1\}\), with \(\delta_i\) the \(H_2\) split of the unique Kalman–Bucy estimate (innovations form). A *count* only; not a process-band placement prediction.
**Run:** `wf_run.json`. Official start 9:57:06 PM ET, finished 11:17:54 PM ET, 4 workers at nice 19. All 40 Model S, 12 rhythmic, and 12 mixed worlds completed; 0 errors; 0 \(E_\infty\) floor flags; 0 INDETERMINATE predictions.

All findings below are **in-model, numerical**. Nothing here is **PROVED**.

---

## Headline verdict (prereg gates)

| Gate | Criterion | Result | Verdict |
|---|---|---|---|
| TAUTOLOGY (test validity) | §3 items 1–4; item 5 not triggered | Re-application agrees on every cell of all 64 worlds (0 mismatches). Identity diagnostic **not** triggered: 0/40 Model S worlds have \(K^*_{\mathrm{WF}}=\) N60-from-0 at every \(R\); 0/40 have \(\delta_i\) equal to the joint decrements to \(10^{-8}\) (median relative discrepancy \(1.4\times 10^{4}\), max \(2.1\times 10^{7}\)) | **PASS** (the rule is predictive, and it predicts badly) |
| SANITY (implementation) | 9 one-OU cells match L1; both \(K^*=0\) and \(1\) occur | 9/9; both values occur | **PASS** |
| PRIMARY Model S | \(\ge 95\%\) of determinate cells | **1882/6440 = 29.22%** (0 INDETERMINATE of 6440) | **FAIL** |
| PRIMARY rhythmic+mixed | \(\ge 90\%\) of determinate cells | **87/264 = 32.95%** (rhythm 47/132 = 35.61%, mixed 40/132 = 30.30%; 0 INDETERMINATE of 264) | **FAIL** |
| HOLE | \(\ge 95\%\) of Model S cells with true argmin \(0\) predicted \(0\) | **70/70 = 100%** | **PASS** |

No gate was changed after seeing the data. No rescue is registered.

---

## Does the mapping hold?

As `MATH.md` distinguished the cases:

- **\(\kappa I_{\mathrm{mem}}+w D\).** Reverse water-filling remains the right allocation for a price on nats. That was already in the theory (P3). Not re-tested here.
- **Frequency-axis peaks of \(S(\omega)\).** Already false in Model S by the math (a single Lorentzian bump at \(\omega=0\), while \(K^*\) can equal \(J\)). Not the rule under test.
- **Isolated per-mode water-filling.** That was IMP-N60, already failed. Not re-tested.
- **Joint-increment water-filling.** That is N60-from-0, an identity with argmin once \(\varepsilon_K\) is in hand. On this fresh Model S set it agreed with argmin in **6440/6440** cells, and all 40 worlds were convex on \(K=0..J\) at \(10^{-4}\). That confirms the solver, not the new rule.
- **WF-HSV (`MATH.md` §7), the candidate translation to a *state count*.** It **does not hold**. It fails the class where the keystone is already exact (29.22% on Model S), and it fails the fresh rhythmic and mixed worlds (32.95%). The predictive rhythm count stays **OPEN**. The law and the equation do not need a closed-form count: \(K^*\) is computed by optimising \(J\), and N60-from-0 is an identity given \(\varepsilon_K\).

The failure is a real miss, not a tautology and not an implementation bug: SANITY holds, the test is predictive (item 5 not triggered), and N60-from-0 still matches argmin perfectly on the same \(E_K\) curves.

---

## How it misses

On Model S the miss is almost entirely **over-inclusion**: 4527 cells predict a larger \(K^*\) than argmin, 31 predict smaller, 1882 match. Typical patterns (predicted, argmin): (4, 3) 965 cells, (2, 1) 925, (3, 1) 837, (3, 2) 749, (4, 2) 643, (4, 1) 408. The 31 under-inclusions are all predicted \(0\) against argmin \(1\). No Model S world is a perfect match (best 66.5% of its 161 \(R\)-cells, median 27.0%, worst 0%).

The Hankel / \(H_2\) split spreads reducible variance across several states. The optimised joint decrements do not. On `ms_0000`, for example,

- WF-HSV \(\delta = (19.07,\ 10.76,\ 0.307,\ 0.0075)\)
- joint decrements \(= (30.14,\ 7.8\times 10^{-5},\ 4.8\times 10^{-5},\ 9.7\times 10^{-7})\)

The first store already captures almost all of the value; the later Hankel energies are not small, so at moderate-to-high \(R\) the rule keeps paying for states that no longer buy a decrement above \(1/R\). That is the same *kind* of mis-allocation that killed IMP-N60 (late isolated values overstated the last joint increments), even though the object here is joint — the unique full-order estimate — rather than isolated modes. Sharing the observation in the Riccati is not enough: ranking the estimate's Hankel states still does not recover the decrements of a reduced-order library.

On the 12 rhythmic worlds, match rates are uneven and poor as a gate (1/11 on four worlds, 9/11 on two one-oscillator worlds). Over- and under-inclusion both occur (33 over, 52 under). On the 12 mixed worlds the rate is 40/132; three worlds (`mx_0006`, `mx_0007`, `mx_0011`) match 0/11, all by over-inclusion. Mixed over/under is 84/8. Combined rhythmic+mixed: 87 matches, 117 over, 60 under.

---

## Identity diagnostic (Model S)

Worlds in which \(K^*_{\mathrm{WF}}=\) N60-from-0 at every \(R\): **0/40**.
Worlds in which sorted \(\delta_i\) equal the optimised joint decrements to \(10^{-8}\) relative: **0/40**.
Max relative discrepancy: \(2.066\times 10^{7}\); median \(1.404\times 10^{4}\); minimum still \(19.85\). The official confirmation is a test, not an identity, and the test is a fail.

---

## Deviations

**D1** (9:56 PM ET, before official start, before any reduced-order \(E_K\)): exclusion parser in `worlds.py` was updated to read `rhythm_rule.json` poles stored as \([\mathrm{re},\mathrm{im}]\) pairs. Generator streams, the inclusion rule, grids, and `PREREG.md` were not changed. Details in `DEVIATIONS_2026-11-20.md`.

No in-run deviation of the solver, the rule, or the gates.

---

## Suspicious points

- The qualitative miss (late states over-weighted relative to joint decrements) is close in spirit to IMP-N60, despite using a joint object. That is a reason not to treat a mild re-weighting of \(\delta_i\) as a new result of this test.
- Two `RuntimeWarning`s from SciPy's Lyapunov solver appeared early in the rhythm phase ("eigenvalue pair whose sum is very close to or exactly zero"). No world was flagged, no \(E\) fell below the floor, and all 64 worlds have empty `flags`. Still a numerical caveat, not a gate change.
- No INDETERMINATE predictions and no \(E_{\infty}\) floor flags. That is unusually clean and is reported, not hidden.

Related, not confirmation: the T20 fair fractal test (`core/keystone_checks/holographic_2026-11-20/RESULTS.md`) found \(K^*\) growing roughly linearly in \(\log R\) and store rates on the *observer* (fast) side, not on process bands. Those worlds were not scored here, and this rule did not predict placement.

---

## Files

- This folder: `MATH.md`, `PREREG.md`, `RESULTS.md`, `LOCK.txt`, `START.txt`, `PREDICTIONS.sha256`, `wf_predictions.json`, `DEVIATIONS_2026-11-20.md`, `wf_rule.py`, `worlds.py`, `build_predictions.py`, `run_wf.py`, `wf_run.json`, `wf_score.json`, `run_wf.log`.
- The confirmation run was done in a local workdir beside a read-only clone at `8537f39`; this writeup is committed later, off later `main`.
