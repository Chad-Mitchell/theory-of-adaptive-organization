# Swarm rule completion (27 November 2026): index

*Friday 27 November 2026 (America/New_York). Branched from `863a8a8bb3e0bb46c00a9236a9b4d5192c4b9d8d` (the head of #297 at the time); #297 moved afterwards (to `5abbee7aa14e7db3f947b96afb4bfd543a499591` and later), and its merged result was brought in by a normal merge of `main`. The swarm rule (`theory/swarm/SWARM_RULE.md`) is a level-2 SYNTHESIS design: it places results proved in their own classes on one cost. This folder adds the results below, each proved in a named class and labelled for that class, each with its own row in `measurement/CLAIM_MAP_v2.md`. The rule's clauses are edited in place and list these results in its §11. A self-check, not an independent review. No Lean work was done for this folder.*

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

## Results, labels and sources

| Ledger row | Result | Class | Label | Source |
|---|---|---|---|---|
| SWARM-EXTERN | CT17 (ii) is clause 4's mispricing at full share | CT12 | PROVED (in-model) | `FOLD_INS.md:13` |
| SWARM-ONECLOCK | one enforced clock gives each mismatched part a tamper gain; gains sum to the penalty | CT17 (i), α = 2 | PROVED (in-model) | `FOLD_INS.md:21` |
| SWARM-REACH | latency enters the stay index as \(\Phi_\ell\); telegraph reach \(L<(v/2\lambda)\ln(1/\pi)\) | CT9 | PROVED (in-model) | `FOLD_INS.md:33` |
| (Lemma B3, row C1) | shared drift lowers, private drift raises the join threshold | CT14 | PROVED (in-model), cited | `FOLD_INS.md:48` |
| (Lemma B7) | √N fade, linear readouts only | CT30 | KNOWN, cited | `FOLD_INS.md:52` |
| SWARM-TELL | the private-information telling price: full revelation iff aligned; informative iff \(\kappa\) in a window; tell iff price below the revealed value | TP | PROVED (in-model) | `TELLING_PRICE.md:24`, `:32`, `:42`, `:54` |
| SWARM-STAKES | stake shares on reports reward under-reporting; Clarke is truthful, individually rational, and needs a subsidy below half the joint cost | ST | PROVED (in-model) | `STAKES.md:21`, `:23`, `:31`, `:41` |
| SWARM-NOBALANCE | no truthful, efficient, budget-balanced rule | ST | PROVED (in-model), an instance of Green & Laffont 1977 | `STAKES.md:43` |
| SWARM-OBJECTIVE | rewriting the whole's stake: no gain under a fixed true reference; gain \(D^{\text{enf}}\) under a fixed wrong one; gain from every inflation under an indexed one | OB | PROVED (in-model) | `OBJECTIVE.md:19`, `:21`, `:27` |
| SWARM-HETERO | heterogeneous error curves: not a weighted potential game; best-reply potential; best response converges | HC | PROVED (in-model) | `COUPLINGS.md:13`, `:17`, `:25` |
| SWARM-LINDAHL | the aligning share is the Lindahl share, not the stake share | HC | PROVED (in-model) | `COUPLINGS.md:29` |
| SWARM-CRED | credibility coupling: extremal equilibria, convergence from the extremes, hysteresis | CR | PROVED (in-model) | `COUPLINGS.md:43`, `:47` |
| SWARM-REPRICE | remove or reprice under the ruin cap (T53) | RR | PROVED (in-model), elementary (was CONJECTURE) | `REMOVE_OR_REPRICE.md:24`, `:34` |
| SWARM-MERGE-EXCL | excludable reads: merge iff gap ≥ coupling (grand coalition); stake shares in the core iff a per-member bound | MG | PROVED (in-model) | `MERGE.md:25`, `:39` |
| SWARM-MERGE-PUBLIC | public reads, no member holding more than half the stake: no merger is stable against a member leaving | MG | PROVED (in-model) | `MERGE.md:31` |
| SWARM-MERGE-CORE | gap above coupling with an empty core | MG | PROVED (in-model), counterexample | `MERGE.md:37` |
| SWARM-MERGE | unqualified "merge iff gap exceeds coupling" | MG | false as stated (OPEN MISS, with diagnosis) | `MERGE.md:52`, `:54` |
| SWARM-HEAT-PART | T61 applied to a part: exogenous floor untampered; no own-heat floor under tamper (shown at full tamper, and by T61 in general); at full tamper with equal couplings (\(J_S=J_M\)) zero heat with zero knowledge of the world, with unequal couplings heat with zero knowledge; the pair floor at every tamper level | FP | PROVED (in-model) | `FEEDBACK_PART.md:15`, `:29`, `:31`, `:33` |

## Not derived (open rows)

| Ledger row | Item | Why it stays open | Source |
|---|---|---|---|
| SWARM-STAKES-BAYES | a balanced Bayesian rule every part prefers to staying alone | AGV balances but need not meet the stay constraint; Mailath & Postlewaite point the other way for many parties; not worked in class ST | `STAKES.md:57` |
| SWARM-BENCHMARK | which objective to align to when the whole's preferences truly change | the cost has no term that prices the whole's preferences | `OBJECTIVE.md:48` |
| SWARM-MERGE-ENFORCE | what enforcement makes a public-read merger self-enforcing | needs a punishment or exclusion model (repeated play, an enforcer) not in class MG | `MERGE.md:54` |
| SWARM-HEAT-PARTIAL | a floor on a tampering part's own heat in terms of its error about the world, under partial tamper | P6 bounds the pair's heat; T61 rules out a bound in terms of the error about the signal; neither settles this | `FEEDBACK_PART.md:48` |
| SWARM-LOSS-CURVE | a part that rewrites the whole's loss curve (moves \(r\), not \(W\)) | not treated in class OB | `OBJECTIVE.md:49` |
| SWARM-STAKES-DYNAMIC | stakes that change over time, with repeated reports | class ST is one-shot | `STAKES.md:58` |
| SWARM-MERGE-LINK | per-link coupling costs; external stability | class MG uses a per-member coupling cost and internal stability only | `MERGE.md:63` |
| (in SWARM-MERGE-PUBLIC's scope) | a public-read merger with a member holding more than half the stake | M3 needs every share at most one half; a dominant member can make the merger stable (counterexample in `MERGE.md` §5) | `MERGE.md:64` |
| SWARM-HAZARD-RESPONSE | a ruin hazard that depends on the response | RR takes each option's hazard as given | `REMOVE_OR_REPRICE.md:51` |
| SWARM-REPRICE-STOP | responses chosen over time | a stopping problem, not a menu | `REMOVE_OR_REPRICE.md:52` |
| SWARM-CRED-SELECT | selection between CR's extremal equilibria under noise | stochastic stability is not worked in class CR | `COUPLINGS.md:60` |
| CX2 (unchanged) | general coupling | CT32's counterexamples; HC and CR are two more classes, not a general theorem | `COUPLINGS.md:57` |
| (in SWARM-TELL's scope) | the telling price outside class TP; equilibrium selection; monotone value in \(\kappa\) | TP3's window is derived at α = 2 with the part informed about the drift | `TELLING_PRICE.md:72` |

## Files

- Notes: `FOLD_INS.md`, `TELLING_PRICE.md`, `STAKES.md`, `OBJECTIVE.md`, `COUPLINGS.md`, `REMOVE_OR_REPRICE.md`, `MERGE.md`, `FEEDBACK_PART.md`.
- Process: `PREREG.md` (Gate: every check is a CONSISTENCY_CHECK), `DEVIATIONS.md` (D1; locked by `checks/SHA256SUMS_2` as of D1), `DEVIATIONS_2.md` (unlocked; any later deviation goes here), `ERRATA.md` (unlocked; where locked text says more than it shows, E1–E4).
- Checks: `checks/swarm27_checks.py` with `checks/swarm27_fix1.py` (D1); output `checks/swarm27_checks.out` (32 CHECK lines, FAILS 0), run at `nice -n 19` from a fresh clone of commit `5b8812de6624bc0ff413f70ca5d8102fd2a8fcd1`; locks `checks/SHA256SUMS`, `checks/SHA256SUMS_2`, `checks/SHA256SUMS_toy`; test `checks/test_swarm27_run.py`.
- DOIs: `checks/crossref_check.py`, output `checks/crossref.out` (31 of 31 resolved). Carroll et al. 2024 has no DOI (arXiv 2405.17713; authors and title checked on the arXiv API).
