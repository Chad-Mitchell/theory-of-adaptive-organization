# HEADLINE-PREMISE-SCOPE — proposed premise clause for §0, the status block, §2.1, §1 N6 (and CLAIM_MAP N13)

Executor queue-pick10 (for Ace; Chad t1914, t1916), Sunday 15 Nov 2026, about 12:42–12:55 PM ET (America/New_York). Queue pick 10, **rule slot** (ledger 53 unaided order, 54 rule_rank, 55 pick, 56 outcome). Private repo; nothing posted or sent.

**Scope (binding).** This file **proposes** text only. Per the item note and Chad t1916 ("be extra, extra sure before you do a full rewrite of the theory ... tread carefully"), a change that touches the headline is applied by a *separate* independent reviewer, with a second hostile pass, before merge (new item HEADLINE-PREMISE-APPLY). `THEORY.md` and the CLAIM_MAP N13 row text are **not** edited in this PR. No locked prediction, result or proof is touched. GTAO is a theory; no "law". Vigilance stays OPEN.

**Slot note.** The dispatch expected pick 10 to be the unaided slot (as QUEUE.md and ledger 51 said). The binding cycle (QUEUE.md rule 3c; `queue/sg_rank.py` docstring) is rule, rule, unaided, uniform, repeating; picks 1–9 were rule, rule, unaided, uniform, rule, rule, unaided, uniform, rule, so pick 10 is cycle position 2, the **rule slot**. The rule's top at entry 54 (I = 3.2; same at γ = 0.2, 0.8) is HEADLINE-PREMISE-SCOPE. Ace's unaided top, AQN-ESTIMATORS (rule rank 5), falls to pick 11, which is the unaided slot.

## 1. The gap, from first principles

The causal chain of §2.1 is: the world's change destroys information; re-buying it costs reads, precision or upkeep; selection keeps the cheapest allocation. *Which* features of the world's change set that cost depends on the tracker the system can run:

- A **linear** tracker (hold-last-value, the optimal linear predictor, a Kalman/Wiener filter, any sum of exponential stores) has an error that depends only on the world's second moments. So for it, the spectrum (α, q) plus the noise level N and the prices are a complete input list. In a **Gaussian** world the Bayes tracker is linear, so the same holds.
- The **Bayes** tracker of a non-Gaussian world uses more of the world's law. In the one case derived (two-state switching, CLAIM_MAP N16, refereed), jump rate λ and size μ enter separately; q = 4λμ² does not fix the optimum.

Check (`HEADLINE_PREMISE_SCOPE_checks/check.py`, output `check.out`; closed form confirmed by an independent quadrature of the Wonham stationary density to < 10⁻³): at **fixed q = 1 and N = 1**, splitting q differently between λ and μ (λ = 10⁻⁵ … 10⁻²) moves the best linear tracker's error by 2% (all near √(qN) = 1, the α = 2 row of §2.2), and moves the Bayes tracker's error by a factor of **364** (0.00044 to 0.158). So "α, q, N and stakes" are a complete input list for the linear tracker and for a Gaussian world, and are not for the Bayes tracker of a jump world. The exponents in §0 (read rate, precision effort, memory time, kernel tail, store count) are all stated for the linear class: the reset-read exponent for hold-last-value or the best linear predictor (second moments only; in the two-state world the Bayes predictor agrees, N16), the noisy-sensing rows for the linear filter, and the store count for sums of exponential stores (a linear tracker).

**Why this is not a bolt-on.** It does not add a mechanism or a free parameter to the theory. It states which tracker class the existing derivations are about, which they already assume. The risk to guard against is the opposite one: a premise clause can become an escape hatch ("the system missed the linear optimum, so it must be running a Bayes tracker"). The proposal therefore pairs the clause with a lock: **which optimum is compared (best linear, or Bayes under a stated world model) is fixed in the prereg before data, and a miss against the locked optimum counts.**

## 2. Proposed edits (exact text; old → new)

Each edit is the minimum that states the premise where the exponents or the inputs are stated. Nothing else in these sections changes.

**P1. Status block, first bullet (THEORY line 13).** After "…and almost all of it is published (§2.2, §10)." insert:
> These exponents are for a Gaussian world, or for the best linear tracker in any world; for the best (Bayes) tracker of a world that jumps, jump rate and jump size enter separately and the noisy-sensing exponents differ (§2.2 Regime A premise bullet; CLAIM_MAP N16).

**P2. §0, first exponent sentence.** Old: "…classical optimal filtering and approximation theory, plus a price on effort, give the design exponents: read rate ∝ …". New: "…classical optimal filtering and approximation theory, plus a price on effort, give the design exponents **for a Gaussian world, or for the best linear tracker in any world**: read rate ∝ …". After "These are known or elementary results, assembled." insert:
> For the Bayes tracker of a non-Gaussian world the noisy-sensing exponents can differ: in a world that switches between two levels, jump rate and jump size enter separately and the adaptation time grows only logarithmically (§2.2 Regime A premise bullet).

**P3. §0, the open bet.** Old: "…once α, the drift level q, the sensing noise N and the stakes are measured on the same system;". New: "…once α, the drift level q, the sensing noise N and the stakes are measured on the same system (and, where the world is not Gaussian and the system's tracker may not be linear, the further inputs that the optimum compared needs, such as jump rate and size separately; §1 N6);". (No other change to the bet; J16 sentence untouched.)

**P4. §1 N6.** Claim column: after "Once α, q, N and stakes are measured on one system" insert ", together with the further inputs the compared optimum needs where the world is not Gaussian (for a jump world, jump rate and size separately; §2.2 Regime A premise bullet),". Number column: append "; the optimum compared (best linear tracker, or Bayes under a stated world model) is locked in the prereg before data". How-it-dies column: append "A miss is scored against the locked optimum; switching to the other optimum after the data are seen is not allowed."

**P5. §2.1, last sentence.** Old: "Three quantities set the tracking optimum in time: the slope α, the high-frequency drift level q (S = q|ω|^−α), and the sensing noise N, together with stakes w and the prices of reads, precision and stores." New:
> For a Gaussian world, or for the best linear tracker in any world (only second moments enter), three quantities set the tracking optimum in time: the slope α, the high-frequency drift level q (S = q|ω|^−α), and the sensing noise N, together with stakes w and the prices of reads, precision and stores. For the Bayes tracker of a non-Gaussian world more of the world's law enters (in the two-state switching world, jump rate and jump size separately; §2.2 Regime A premise bullet).

**P6. Consistency pointers (same inputs listed elsewhere).**
- §2.4 "Net" (line 140): after "measured α, q, N and stakes on the same system" insert " (with the further inputs of §1 N6 where the world is not Gaussian)".
- §9 first bullet (line 316): after "with α, q, N and stakes measured on the same system and a locked test" insert " against the optimum locked in the prereg (best linear or Bayes; §1 N6)".
- §2.5 rule for every prediction (line 149): after "…jump rate and amplitude are separate inputs)" insert "; which optimum (best linear or Bayes) a prediction uses is locked before the data".

**P7. CLAIM_MAP N13 (row text; status stays OPEN).** Claim: "Measured-input optimality: with α, q, N and stakes measured on one strongly selected system (plus jump rate and size separately where the world is not Gaussian and the compared optimum is Bayes; THEORY §1 N6), its read rate, memory time and store count lie near the THEORY §2.2 optima, at ≥ 2 scales". Notes: append "Optimum compared (best linear or Bayes) locked per prereg (HEADLINE-PREMISE-SCOPE)." Add a CLAIM_MAP version note; no status change.

**P8. Changelog** (THEORY §13): a v1.4.4 entry naming P1–P7, the applier and the second pass, and stating "premise clause only; no headline or core rewrite; no status change".

**Optional, NOT part of this proposal unless checked first — P9 (Regime C).** §2.2 Regime C's model size ∝ Q^{1/β} is reverse water-filling, which is exact for Gaussian modes (`theory/INTERNAL_MODEL.md` §4 uses the Gaussian tool). For other sources a Gaussian source of the same covariance has the largest rate–distortion function (a standard rate–distortion fact; not re-read this pick), so the Gaussian answer is an upper bound on bits, and the exponent for non-Gaussian modes is not derived. §0 also states Regime C. I have not checked this beyond the textbook fact, so it is queued as a new item (REGIME-C-GAUSSIAN-PREMISE), not proposed for application here.

## 3. Hostile self-check of the proposal (same executor; not a substitute for the applier's review)

1. **Is the premise too strong anywhere?** Reset-read exponents hold for hold-last-value and the optimal linear predictor in *any* world with the given second moments (§2.2 Regime B premises column). "Gaussian world, or the best linear tracker" is a *sufficient* condition and is phrased as the scope of the stated exponents, not a claim that they fail outside it; P2's second sentence says "can differ" and names only the noisy-sensing exponents. ✔
2. **Is it too weak?** Store count assumes sums of exponential stores (linear). Kernel tail is the linear optimal filter. Precision effort uses the noisy-sensing error. All inside "best linear tracker". ✔ Regime C is not linear-tracker filtering; flagged separately (P9). ✔
3. **Escape hatch.** Guarded by the lock in P4/P6/P7. Without it, N6 would become harder to kill; with it, it becomes no easier to rescue. ✔
4. **Numbers quoted.** Only "jump rate and size enter separately" and "logarithmic adaptation time" are restated, both from N16 (refereed). The 364× / 2% figures stay in this file, reproduced by `check.py`. ✔
5. **Headline meaning.** The bet's content (measured-input optimality across scales; same relations, not constants) is unchanged. No sentence of §0 is removed. Word count added to §0: about 80. ✔
6. **Labels.** No "law"; nothing claimed new; N16 credits unchanged; vigilance not mentioned. ✔
7. **Line numbers** refer to `THEORY.md` at origin/main `e8bae15` (v1.4.3); the applier must re-read at use (QUEUE rule 1), since other workers may edit THEORY.md first.

## 4. Outcome for the queue

- HEADLINE-PREMISE-SCOPE: DONE (proposal). `status_changed` false (no CLAIM_MAP status change; no row text changed in this PR).
- New: **HEADLINE-PREMISE-APPLY** (independent reviewer applies P1–P8 with a second hostile pass; Chad t1916). **REGIME-C-GAUSSIAN-PREMISE** (check P9: is Q^{1/β} Gaussian-only; read the rate–distortion source; propose scope text).
- Surprise read (rule 4): the size of the linear–Bayes gap at fixed (q, N) in the two-state world (error ratio up to about 2,000 at κ = 4·10⁻¹⁰; 364× spread across splits of q) is not a new result (it follows from N16's closed form) but it raises the stakes of AQN-ESTIMATORS' jump-world branch: estimating q alone is useless for a Bayes optimum. Logged as weak evidence for AQN-ESTIMATORS (note added), no LR change, since that item is untested (P = 0.5 flat).
