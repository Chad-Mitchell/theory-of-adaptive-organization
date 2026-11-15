# STATUS (current pointer; rewritten, not appended)

**As of:** Sunday 15 November 2026, about 10:12 AM ET (America/New_York). **Stamped against:** `THEORY.md` v1.4.1. If `git log -1 -- THEORY.md` is newer than this stamp, reread THEORY.md before trusting anything here.

## Where the theory stands (one paragraph)
GTAO models every adaptive organization with one budget: holding memory, prediction error (including lateness) and the reads or effort that keep memory current, plus ruin risk; only implementation and currency differ by scale. Its time-spectrum part, the map from a world's spectral slope α (with drift level q, sensing noise N and stakes) to read rate, precision effort, memory time, forgetting kernel and number of stores, is now derived, refereed and **classical**: optimal filtering and approximation theory plus a price on effort, credited (THEORY §0, §2.2, §10). It is no longer the headline. The mode-spectrum part (§2.2 Regime C: model size ∝ Q^{1/β}, an interior minimum of the model's budget share iff β < 1, a minimum viable size from unstable modes) is PROOF under stated assumptions with known tools and was not reviewed by the spectrum-map referee. **The open, falsifiable bet is empirical** (CLAIM_MAP N13, J6): real systems at every scale sit near these optima once α, q, N and stakes are measured on the same system, with the same relations (not constants) at every level. No system has had all four inputs measured, so the bet is untested. In the model, the same three costs at every level is an axiom (Axiom 5; CLAIM_MAP J16), so the model alone cannot test it. As a claim about real systems it is testable through its consequences: at each level the three costs can be measured separately, and the claim fails if a level's design needs a fourth kind of cost to be explained, or if design does not respond to the measured prices of the three as the relations require (J6). The formal layer (sensing classes, pooling onset, vigilance, ordering, freeze/hold band) is proved in-model with corrections; v1.4 adds an elementary, self-checked, not-yet-refereed result (N12): its onset exponent does not depend on α for the two sensing technologies (−1 for reset reads, −(1+θ) for precision priced ∝ precision^θ), so it measures the level's technology, not the world. No field test has measured GTAO's quantities validly: nothing is confirmed or refuted in the field; field results are "passed / failed on proxy X"; vigilance is OPEN. Every prediction states its section and regime first.

## Canonical files (read these; everything else is a derivation or history)
- `THEORY.md` — the theory (v1.4.1).
- `measurement/FRAMEWORK.md`, `measurement/CLAIM_MAP_v2.md` (v2.4; sections G, K, N) — how quantities are measured; one status per claim.
- `QUEUE.md` + `queue/` — live work, ordered by Proposition SG, with a ledger.
- `reviews/night2/SPECTRUM_MAP_REFEREE.md` — why the tracking layer was demoted.

## Frozen history (kept, not maintained)
`theory/` (older theorem notes; T1–T9 there are not the formal layer's Theorems 1–8), `reviews/night1/` (formal layer, CORE_AUDIT, ARCH_EQUATION, referee reports, CLAIM_MAP_FINAL), `reviews/night2/SPECTRUM_MAP/` (derivation; corrected by its referee), `tests/` (locked tests), `litmap/`, Ace's working folder `/workspace/gtao/` on the box. Their statements hold only as cited from THEORY.md. Some still say "slope 1" or "(log-span)^{2/3}"; those are superseded (QUEUE FROZEN-DOC-POINTERS).

## Running or in flight (15 Nov, about 10:00 AM ET)
- Queue protocol v2: post-protocol pick 1 SPECTRUM-MAP-REFEREE (DONE), pick 2 THEORY-2.2-REWRITE (DONE, rule slot; ledger 15–18). Next is pick 3, the unaided slot.
- LFK-ALPHA-SPF DONE (manual, unscored; ledger 10/19; `tests/LFK_SPF/RESULTS.md`): locked N13 probe using N11 (q from spectrum, N from SPF dispersion). Primary INCONCLUSIVE (n = 6; MV8 failed by pre-lock dry run; Tier 3); no CLAIM_MAP change. New items SPF-AQN-POWERED, SPF-NOISE-PROXY, LAB-AKLMT-TAU.
- GITHUB-UPSTREAM data pull (lock branch `prereg/github-upstream`; regime addendum `reviews/night2/GITHUB_ADDENDUM_REGIME.md`). WIKIDATA-BAND pilot (stationarity gate owed before locking).
- New items from v1.4: ONSET-SPECTRUM-FREE-REFEREE, AQN-ESTIMATORS, SAME-SYSTEM-AQN, ONSET-ACROSS-ALPHA-SIM, KERNEL-MEASURE, FROZEN-DOC-POINTERS.

## Results since v1.1 (details in THEORY §8c, CLAIM_MAP_v2 §G, §N)
- THEORY v1.4: headline demoted per `SPECTRUM_MAP_REFEREE.md` §7; §2.2 by regime with premises; K12, K13, H19, N7, N10, N11 applied; N12, N13 and G23–G29 added (no existing row changed status).
- SPECTRUM_MAP + referee: read-rate exponent 1/α holds for hold-last-value and the optimal linear predictor (rescaling-closed classes only); noisy-sensing error KNOWN (Afterman et al. 2022); effort elasticities α/(2α−1), 1/(2α−1) elementary, under linear precision pricing; kernel tail τ^{−(1+α/2)} KNOWN, survival τ^{−α/2}; store count ∝ ln(span)·ln(stakes/upkeep) prior art plus a price, one store a knife-edge at α = 2; τ_m ∝ τ_E^{1−1/α} only at fixed variance, PRIOR ART in substance (τ ∝ (N/q)^{1/α}; α = 2 in Mora & Nemenman 2019); D3's sign was a mis-derived prediction; locked D3S passed on proxy "binary daily edit series" but is non-discriminating.
- LEARNSIM (in-model, regime A): T1.8 not passed (RA arm SIM-PASS and robust; AR inconclusive on MV8); C1 downgraded; vigilance at onset (class R) locked-rule SIM-PASS.
- VIGIL_ONA: direction passed on nomination proxies, downgraded by the referee; vigilance OPEN.
- MEASURE-SELF: √ allocation failed on a statement-time proxy with its premise unmet (scope); regime not established.

## Standing rules
Private repo; no public acts without Chad's go; call GTAO a theory; field results "passed / failed on proxy X", no field kills; heavy compute at nice 19; Looper README wording needs Chad's approval.
