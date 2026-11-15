# HEADLINE-PREMISE-APPLY — applying P1–P8 (HEADLINE-PREMISE-SCOPE) to THEORY.md v1.4.4 and CLAIM_MAP v2.14

Executor queue-pick13 (for Ace; Chad t1914, t1916), Sunday 15 Nov 2026, about 2:46–2:58 PM ET (America/New_York). Queue pick 13, **rule slot** (ledger 66 unaided order, 67 rule_rank, 68 pick; outcome entry after the PR is ready). Private repo; nothing posted or sent.

**Independence and merge rule.** This executor authored none of `reviews/night2/HEADLINE_PREMISE_SCOPE.md` (pick 10) and none of the texts it builds on. Its source check (§2) and second hostile pass (§3) are **its own** and are recorded as such; they do **not** satisfy Chad's t1916 rule. The PR stays **unmerged** until a separate independent reviewer (new item HEADLINE-PREMISE-REVIEW) passes it. GTAO is a theory; no "law". Vigilance stays OPEN. No locked prediction, result, proof or CLAIM_MAP status changed.

## 1. What was applied (THEORY.md at origin/main `7a17230`, v1.4.3a, re-read at use)

| Proposal | Where | Applied as |
|---|---|---|
| P1 | status block, "tracking layer is classical" bullet | applied, tightened (T1, T2) |
| P2 | §0 exponent sentence + one sentence after "assembled" | applied; "(premises per row in §2.2)" added (T1) |
| P3 | §0 open bet | applied, reworded (T3) |
| P4 | §1 N6 claim / number / how-it-dies | applied, reworded (T3), default added (T4) |
| P5 | §2.1 last sentence | applied; "more of the world's law enters" → "can enter" (T5) |
| P6 | §2.4 Net, §2.5 rule, §9 first bullet | applied; §2.4 conditioned as in T3; §9 with default (T4) |
| P7 | CLAIM_MAP N13 row text + v2.14 note | applied with T3/T4; status stays OPEN |
| P8 | §13 changelog v1.4.4 | applied |
| V143 F2 | "What changed in v1.4" item 2; §10 LFK entry | same learner-class sentence as the §2.2 F2 fix |
| line 6 | header CLAIM_MAP pointer | v2.11 (stale; main was v2.13) → v2.14 |
| header | title / draft dates | v1.4.3a → v1.4.4 |

Not applied: P9 (Regime C), which the proposal itself excludes (REGIME-C-GAUSSIAN-PREMISE stays open). §0's Regime C sentence is untouched.

### Applier's tightenings (each makes the premise exact; none adds a mechanism or a parameter)
- **T1 (do not weaken a confirmed result).** The reset-read exponent is PROOF for hold-last-value (formal Lemma 1(i)) and holds for it in any world with the given second moments (§2.2 Regime B premises column). "For the best linear tracker" alone would read as excluding it. Status block: "(only second moments enter; the reset-read exponent also holds for hold-last-value; premises per row in §2.2)"; §0: "(premises per row in §2.2)".
- **T2 (do not over-generalise one case).** P1 said, for a jump world, "the noisy-sensing exponents differ". Only the adaptation-time and error elasticities are derived (N16); a kernel regressed on the tracker's own observations equals the linear one in any stationary world (§2.5; TELEGRAPH-REFEREE narrowing), and the precision-effort exponent of a Bayes jump tracker is not derived. Now: "in the one jump world derived (two-state switching) ... the adaptation-time and error exponents under noisy sensing differ, while exact reset reads are unaffected and a kernel regressed on the tracker's own observations is the linear one". §0's sentence keeps "can differ" and names only the derived adaptation time.
- **T3 (condition on the optimum compared, not on the system).** P3 said "where the world is not Gaussian and the system's tracker may not be linear"; P4/P7 said "where the world is not Gaussian". If the locked optimum is the best linear one, α, q, N and stakes are a complete input list in any world, so extra inputs are needed only when the optimum compared is the Bayes optimum of a non-Gaussian world. "The system's tracker may not be linear" is a judgement about the system that invites the escape hatch the proposal warned about. All three now say "where the optimum compared is the Bayes optimum of a non-Gaussian world", and §0 states the lock itself.
- **T4 (close the escape hatch for tests already locked).** P4/P6 required the prereg to fix the optimum. Tests locked before v1.4.4 did not name one, so a strict reading could excuse any of them from the §9 sink. Added: "exactly one optimum ... is locked ... and it is the one scored; a prereg that names none is scored against the best linear optimum, the one §2.2 states", and in how-it-dies "in the causal form too". This is the optimum every §2.2 row was derived for, so earlier tests are scored as they were derived.
- **T5.** §2.1: "more of the world's law enters" → "can enter" (the Bayes tracker of a non-Gaussian world need not use more than second moments in every case; for exact reset reads in the two-state world it does not).

## 2. Source check (every changed sentence)

| Changed sentence | Source | Check |
|---|---|---|
| Exponents hold for a Gaussian world or the best linear tracker; only second moments enter | THEORY §2.2 Regime A premise bullet and Regime B premises column (v1.4.3; TLP-EDITS-REVIEW, V143 review) | ✔ same wording as the refereed §2.2 text |
| Reset-read exponent also for hold-last-value | §2.2 Regime B read-rate row; formal Lemma 1(i) | ✔ |
| Jump rate and size enter separately; q alone does not set them | N16 (MATH-CORRECTED, refereed), `TELEGRAPH_REFEREE/REPORT.md` §§1–4 | ✔; reproduced here (below) |
| Adaptation-time and error exponents under noisy sensing differ | §2.2 premise bullet: t_A elasticities 1/ℓ, 1−1/ℓ, −2+2/ℓ vs ½, ½, −1; error elasticity 0.85–0.89 vs ½ | ✔ |
| Exact reset reads unaffected | §2.2 premise bullet ("Unaffected: exact reset reads ...") | ✔; reproduced (below, check c) |
| Regression kernel on own observations is the linear one | §2.5 rule (iterated projections); TELEGRAPH-REFEREE V11 narrowing | ✔ |
| Adaptation time grows only logarithmically with the switching time | t_A = (N/2μ²)[ln(2μ²/λN) − γ − 1]; switching time 1/λ | ✔ |
| LFK √ form belongs to their learner class, not the Bayes optimum | `PRIORART_LFK_ALPHA/REPORT.md` §4; V143 fix F2 (§2.2 sentence) | ✔ same claim, same pointer; no new characterisation of LFK's learner added |
| CLAIM_MAP pointer v2.14 | `measurement/CLAIM_MAP_v2.md` v2.14 note (this PR) | ✔ |

**Independent numerical check** (`HEADLINE_PREMISE_APPLY_checks/check.py`, own code, output `check.out`; nice 19). At q = N = 1 fixed, λ = 10⁻⁵ … 10⁻²: best linear (Kalman, same covariance) error 0.980–1.000 (spread 1.020×); Bayes error by my own quadrature of the Wonham stationary density (substitution s = 1/(1−u²) = 1 + t²) equals the Bessel closed form μ²·2K₀/(K₀+K₁) to < 10⁻³⁰ relative and spreads **363.8×** (4.35·10⁻⁴ to 0.158). Reproduces the proposal's 2% / 364×. (c) Two-state world: E[x(t+s) | x(t)] = x(t)e^{−2λs} exactly (linear in the last exact read), so the reset-read optimum depends on second moments only.

## 3. Second hostile pass (same executor; fresh re-read of the full diff after §1–§2)

1. **Does any edit weaken a confirmed claim?** The only PROOF/KNOWN results touched are scoped, not withdrawn; T1 and T2 keep the hold-last-value reset-read result and the regression-kernel result in force. No status changes. ✔
2. **Does any edit protect a claim from failing?** Without T4, "a locked test whose prereg fixed the optimum" would have excused every test locked before v1.4.4. Fixed. Choosing the optimum after the data, or changing the world model, is forbidden in N6, in the causal form too. Requiring extra inputs only applies to a Bayes-locked prereg, which the tester chooses before the data; a linear-locked prereg needs only α, q, N and stakes. ✔
3. **Is the premise exact, not merely sufficient?** It is stated as the scope of the stated exponents, with "need not hold" / "can differ" outside it and the one derived case named. It does not claim failure outside the class (for exact reset reads in the two-state world the Bayes and linear optima agree). ✔
4. **Headline meaning.** No §0 sentence removed; the bet (measured-input optimality; same relations, not constants, across levels; J16 consequence tests) unchanged. §0 gains about 95 words. ✔
5. **Numbers quoted.** None new in THEORY; 2% / 364× stay in the review files. ✔
6. **Credits / citations.** None added or removed; LFK qualifier repeats the reviewed F2 sentence. ✔
7. **Labels.** No "law"; vigilance not touched; results unaffected. ✔
8. **Residual issues (not fixed here; for the reviewer).** (a) The status block's heading time ("about 10:00 AM ET") predates several edits; left as is. (b) Regime C's Q^{1/β} in §0 still lacks any Gaussian scope (REGIME-C-GAUSSIAN-PREMISE). (c) §0's parenthesis in the bet is long; a reviewer may prefer moving the lock sentence to N6 only. (d) The causal kill names α, q, N, stakes; for a Bayes-locked jump-world prereg the predicted direction of a change in q depends on how it splits into λ and μ, which the prereg must then state. (e) If q-pick12 (STAKES-EXOGENOUS) also writes a CLAIM_MAP v2.14 note, one of the two must be renumbered at merge.

## 4. Outcome for the queue
- HEADLINE-PREMISE-APPLY: DONE (applied in PR, not merged). `status_changed` false.
- New: **HEADLINE-PREMISE-REVIEW** (separate independent reviewer: re-derive, check sources, second hostile pass, then merge or request changes; Chad t1916).
