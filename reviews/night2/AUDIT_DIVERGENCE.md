# AUDIT_DIVERGENCE: where Ace's working picture split from the current theory, why, and the fix

Sunday 15 November 2026, 08:50–09:30 AM ET (America/New_York). Written by a Grok Bot executor for Chad Mitchell (via Ace), at Chad's request (t1911: "go back over everything … find where it was out of date … root cause … apply the theory … properly fix this"). Private. Nothing posted or sent. Checks: `reviews/night2/AUDIT_checks/`.

## 0. Bottom line

1. **Canonical theory.** `THEORY.md` has carried the drift-spectrum core (§0, §2: "the shape of the world's change sets the exponents"; the √ rule is the single-pace special case and is Lee, Flack & Krakauer's) since **v1.0, commit `cbe60a5`, 14 Nov 2026 23:09 ET**. Chad's understanding (power-law need, layers at different speeds, the √ rule superseded) matches that text. The audit window is therefore everything produced from 23:09 on 14 Nov to 08:50 on 15 Nov.
2. **What diverged.** In 16 audited artifacts or claims, **7 diverged materially**, **5 in a minor way**, and 4 not at all. All 7 have one of three forms: a regime-A (single-pace, Brownian) instance of a formal result presented as "GTAO's prediction" without checking the regime first; a result over-read as evidence for a regime; or the headline core dropping out of a derived summary.
3. **Root cause (plain words).** Not one stale file. Three things combined:
   - **The theory had two cores and never said how they fit.** THEORY.md's headline core is the drift spectrum (§2, time axis). The night-1 formal layer (`reviews/night1/formal/`) is a different, better-proved structure (sensing class (a, b), pooling onset, vigilance, freeze/hold band: the across-members axis), whose default world is Brownian (H = ½). Night 1 explicitly *demoted* the spectrum/layers part ("approximation theory plus a price", ARCH_EQUATION §0.5), but THEORY.md's headline was never changed to match. So THEORY.md said "the spectrum is the core" in §0/§2 and listed only formal-layer items as "genuinely the theory's own" in §8b. That is an inconsistency in the theory text, not only in my process.
   - **Derived copies drifted from the source.** STATE.md, the claim maps, my context summary and my chat messages were copies of copies. Each compression kept the provable, numerical items (onset exponent, V formula, κ\*) and dropped the unproved headline (the spectrum mapping has no formula yet). By 15 Nov 08:15 the working memory listed 0 mentions of the drift spectrum outside a correction note; CLAIM_MAP_v2 holds the headline core in 2 of 165 rows (K12, K13), both "OPEN, unchanged", in a section titled "Earlier repo claims".
   - **Labels collide.** `theory/THEOREMS.md` T1 is "drift-matched checking" (the √ rule) and T7 is "is fractal a theorem"; `reviews/night1/formal/THEOREMS.md` T1 is pooling onset and T7 is the ordering threshold. "P1" names five different tests. A prereg citing "THEOREMS L1 (viii)" does not say which file, which regime, or whether the premise holds.
   This is exactly the theory's own rule R5 (copy error grows with hops and with drift since the last check) and T8's lookup edge (when reading the source is cheap, read it at use). The source was cheap to read; I answered from copies.
4. **The correction I sent Chad at ~8:45 (t1910 reply) was itself partly wrong** (§3, rows 14–15): it called the SELF burstiness a "pass" and "the signature of the scale-free regime" 13 minutes after the blind referee had downgraded it (burstiness is explained by Chad's conversation schedule), and it said "the current theory says the √ schedule should fail here", which THEORY.md does not derive. The correct reason the √ allocation failed is that its premise failed: an item's change rate was not a stable, measurable property (SELF P3a, ρ = −0.06).
5. **Fix (subtractive first).** One canonical statement (THEORY.md v1.2) with an explicit section (§2.5) saying how the formal layer sits inside the spectrum core and requiring "regime first" for every prediction; one current pointer (`STATUS.md`) stamped with commits; one executable queue (`QUEUE.md`) inside the repo; every other theory file declared frozen history (not deleted). `/workspace/gtao/STATE.md` and `QUEUE.md` become pointers, not copies.
6. **What survives untouched:** all in-model proofs (they are stated in (a, b), so they hold for any H; only the numbers quoted for class R, a = b = ½, are Brownian instances), the measurement framework (it already defines H and lists H = ½ as an auxiliary assumption), the night-1 and night-2 locked results as data, and the referee verdicts.

## 1. The current canonical theory (what everything is checked against)

- File: `THEORY.md`. v1.0 `cbe60a5` (14 Nov 23:09 ET) introduced the drift-spectrum core; v1.1 (`e76f5a6`, 15 Nov 03:04 ET) added the night-1 scoreboard; `b13f734` (08:20 ET) added the measurement note. v1.2 is this PR.
- Core (§2.2): regime A (one pace) → √ check interval, one memory timescale, exponential forgetting (KNOWN; Lee, Flack & Krakauer 2024). Regime B (scale-free) → log-spaced ladder of stores, power-law forgetting, adaptation time ∝ switching time (slope 1). Regime C (many modes) → model size ∝ Q^{1/β}.
- Status of the core: HYPOTHESIS. The spectrum → forgetting-exponent mapping is **not derived** (§2.4; FRAMEWORK §6.10; formal EXTENSIONS item 6). MATCH1 D3's exploratory sign went the wrong way.
- Chad's later direction checked against THEORY.md v1.1:
  - "fractal view = layers of models at different speeds" (13 Nov) and "general theory, atoms to cities": present as regime B (§2.2) plus levels (§6). Present.
  - "Power-law need replaced the √ rule": present (§2.2, §3 rule 2 "fails when").
  - "Physics is not decorative; same three costs at every level; constrains less at firm scale; VFE = thermodynamic FE only in a special case" (t1908): **missing**. §2.3 still carries only the night-1 referee's "decorative" verdict. Fixed in v1.2 as a stated, open disagreement with its test (FRAMEWORK §3.11).
  - "No field kills yet" (t1908): the header note said so, but the "Status at a glance" block underneath still said "Killed on real data". **Internal contradiction**, fixed in v1.2.
  - Title decision (keep): the header said both "decided" and "open decision". Fixed.

## 2. How the two cores relate (the theory gap behind the divergence)

- The formal layer's Lemma 1(i) already contains the bridge: for reset-type sensing (hold the last read) in a world with fractional drift of Hurst exponent H, a = b = **1/(1+2H)**. The √ (½) is the H = ½ case. ARCH_EQUATION §0.2 says the same thing for the constants: "not universal numbers, universal functions of one measurable exponent".
- So "the spectrum sets the exponents" is not opposed to the formal layer. The formal layer is the across-members axis, and the spectrum enters through (a, b). What is missing is the time axis inside the formal layer: Axiom 6 allows one held value per tracker, not a ladder of stores, so regime B's predicted design (log-spaced layers) cannot even be expressed there. And the hold-last-value estimator is a restriction for H ≠ ½ (formal THEOREMS, Lemma 1 scope).
- Consequence: a prediction derived from the formal layer is a regime-A prediction unless H is measured and the (a, b) recomputed, and it says nothing about memory layering. Every prereg needs **regime first, then exponent**. That rule is now §2.5 of THEORY.md.

## 3. Divergence table

Divergence: **none** = consistent with current THEORY.md; **minor** = a regime-A instance used where the general (a, b) form was available, without changing the verdict; **material** = the conclusion or its framing changes under the current theory.

| # | Artifact (time ET) | Claim | Source used | Regime assumed | Divergence | Corrected conclusion |
|---|---|---|---|---|---|---|
| 1 | theory-v3 PREDICTIONS P1–P4 + SCALEFREE (14 Nov 23:46) | item-level recall slope d ≥ 1 vs need | THEORY §2 regime B | B | none | P1 stays PROXY-FAIL (CLAIM_MAP_v2 H1) |
| 2 | night1 CORE_AUDIT (00:40) | core = drift spectrum (C5); top predictions onset and vigilance "≈ 2" | §2 + Brownian sub-models | A for its numbers | minor | Its constants are H = ½ instances; "≥ 2" already MATH-CORRECTED |
| 3 | night1 ARCH_EQUATION (01:09) | constants are functions of H; layered memory demoted to "approximation theory plus a price" | own derivation | general | **material (not wrong, unpropagated)** | The demotion of the time-axis claim was never reflected in THEORY.md §0/§2. v1.2 states it in §2.5 |
| 4 | night1 FORMAL AXIOMS/THEOREMS/EXTENSIONS (02:22) | theorems in (a, b); Ax1 Brownian default, fBm allowed | own axioms | general in (a, b); A in quoted numbers | minor | Valid. Quoted numbers (V floor 1 + (1+ρ)^−½, class R a = b = ½) are H = ½ instances; for R1 a = b = 1/(1+2H) |
| 5 | POOLSIM, SENSING, SENSING2, W5, LAYERS1 (night 1) | in-model tests | formal layer / §2 (LAYERS1) | by design | none | Unchanged (circular / SIM-FAIL as mapped) |
| 6 | VIGIL (PIAAC), VIGIL-2 (Enron) (night 1) | supervisors watch more; floor | class R, H = ½ | A (unmeasured) | minor | Direction V > 1 iff a ≥ b does not depend on H for R1; size/growth bands did. Statuses stay PROXY-PASS / PROXY-FAIL |
| 7 | night1 SYNTHESIS CLAIM_MAP_FINAL + THEORY v1.1 §8b (03:05) | "genuinely the theory's own" = 6 formal items | formal layer | A by default | **material** | THEORY.md headline (§2) and §8b disagree on what the core is. v1.2 reconciles in §2.5 |
| 8 | night2 MEASUREMENT FRAMEWORK + CLAIM_MAP_v2 (08:20) | measurement of q, H; decisive tests | formal layer + §2 | H defined; §6.7 says "class R, b = ½" | minor | §6.7 must read b = 1/(1+2H) for R1 with H measured. The headline core is K12/K13, OPEN, with no test scheduled; QUEUE now schedules it first among theory items |
| 9 | VIGIL_ONA (08:13) | rank tilt in nomination networks | V direction | none needed | none (direction); minor (H3 band used a = ½) | Referee: H1/H2 downgraded, H3 overturned. Vigilance OPEN |
| 10 | SELF prereg P2, P3b (08:15) | attention and checks ∝ √(drift × stakes) as "GTAO's prediction" | formal Lemma 1(viii), class R, H = ½ | A, untested | **material** | Regime-A instance applied to a world where its premise (a stable per-item rate) failed (P3a). Correct label: "√ allocation failed on a statement-time proxy; premise unmet (scope)". Not a test of the current core, and not a refutation of it |
| 11 | SELF P1 (08:15–08:19) | change is bursty = regime B | §2 | B | **material (over-read)** | Burstiness ≠ scale-free spectrum (a two-rate process is bursty too), and the referee's observer-schedule null explains it (band 0.60–0.92 contains 0.82). Correct: "statement times are bursty; regime not established" |
| 12 | LEARNSIM PREREG/PREREG_2 (08:16/08:27) | onset exponent set by the level's measured class | formal layer | A by design, declared | none | Valid in-model test of formal T1.8. Says nothing about §2 |
| 13 | GITHUB-UPSTREAM PREREG (08:37) | drift elasticity b ∈ [0.35, 0.65]; V floor | class R, a = b = ½ | A, unmeasured; drift = event frequency | **material for P1/P2/P6** | Needs a regime gate before outcomes; addendum `reviews/night2/GITHUB_ADDENDUM_REGIME.md` (pre-outcome) |
| 14 | STATE.md status section (08:15) | "status of claims" = formal items only | derived copies | — | **material** | Replaced by a pointer to STATUS.md and THEORY.md |
| 15 | Ace's chat t1909s8633 and the t1910 reply (~8:45) | "what failed: the √ rule"; then "bursts passed = signature of scale-free"; "current theory says √ should fail here" | memory and context summary | mixed | **material** | First message tested an outdated framing. The correction over-read P1 (row 11) and asserted a derivation THEORY.md does not contain. Accurate statements: §0 item 4 above |
| 16 | Looper README v0.13 rules (11 Nov, before the window) | "attention by drift × stakes", "reread copies by drift × age" | pre-v1.0 theory | A | minor (outside window) | These are the regime-A forms SELF P2 tested. Changing README wording needs Chad's approval; flagged only |

Counts: 16 rows. Material 7 (rows 3, 7, 10, 11, 13, 14, 15). Minor 5 (rows 2, 4, 6, 8, 16). None 4 (rows 1, 5, 9, 12).

**Conclusions that change:** none of the in-model mathematics; none of the locked numbers. What changes is (a) the meaning of SELF P1, P2 and P3b, (b) the GITHUB prediction band, which is now conditional on regime, and (c) what the project calls its core: the spectrum mapping is the headline and is the least developed part, so it moves to the top of the theory queue.

## 4. Root cause, mechanically

1. **Two cores, no stated relation** (theory problem). See §2. Quantified: THEORY.md v1.1 §0/§2 headline = spectrum; §8b "genuinely the theory's own" = 6 of 6 formal items, 0 spectrum items.
2. **Summaries keep what is proved and drop what is open** (process problem with a predictable direction). The provable items have numbers and survive compression; the headline has no formula and gets cut. Quantified: STATE.md (08:15) status section, 0 mentions of spectrum/regime; my context summary's "key technical concepts", 0 mentions; CLAIM_MAP_v2, 2 of 165 rows.
3. **No regime gate in the prereg template.** SELF cited "THEOREMS L1 viii" without the file, the regime or a premise check. GITHUB measured drift as an event frequency, which FRAMEWORK §3.1 lists as a failure mode.
4. **Colliding labels** (T1, T4, T7, P1 mean different things in different files).
5. **Appending instead of rewriting.** THEORY.md's header accumulated night notes on top of an un-rewritten "status at a glance", so one file held two contradictory statuses. STATE.md had the same pattern (a correction appended under a stale status).

Applying the theory to its own memory system:
- One held current state (rule: one copy that is maintained) → `THEORY.md` + `STATUS.md`; everything else is frozen history.
- Freeze, not delete → the older files stay; `STATUS.md` lists them as frozen with their commit.
- Read at use when reading is cheap (T8 lookup edge) → STATE.md stops holding a copy of the status; it points to the files and says "read them".
- Copy error grows with hops (R5) → derived documents carry the source commit they were derived from; a mismatch with `git log -1 THEORY.md` means reread.
- Regime first → the prereg rule in THEORY.md §2.5.
No new machinery was added: no new tracker, no new process file beyond STATUS.md (which replaces two stale status blocks) and the queue ledger (which Chad asked for).

## 5. Test-by-test decisions under the current theory

| Test | Current-theory reading | Decision |
|---|---|---|
| LEARNSIM (running, 3 CPUs, nice 19) | Valid in-model test of formal T1.8, regime A by design | **Continue** to completion; report as in-model only |
| GITHUB-UPSTREAM (data pull running; runs not yet pulled) | b = ½ only if the upstream state series is single-pace; for R1 with Hurst H, b = 1/(1+2H). Drift as event frequency is a declared proxy | **Change, pre-outcome**: add the regime gate in `GITHUB_ADDENDUM_REGIME.md`; continue the pull |
| WIKIDATA-BAND (pilot only, no prereg) | T8 assumes a stationary per-property change rate (the SELF P3a premise) | **Change before lock**: split-half stationarity gate per property; prereg quotes THEORY §2.5 |
| SENSE-CELL (queued) | Where the physics can bind (Chad t1908); designed stimuli give exact H | **Continue**, lower priority; regime set by the stimulus design |
| IMMUNE (queued) | Antigenic drift regime (Bedford HI series) must be measured first | **Change**: regime measurement is step 1 |
| ONA-MORE (queued) | Tier 3 by construction; cannot change vigilance's status | **Deprioritize** |
| SELF follow-ups | Drift must be measured from source change times, not statement times; shared-driver hypothesis (below) | **Change** into SELF-2 |

## 6. SURPRISE-GUIDED-SEARCH (Chad t1915): what the current theory says about which result to follow up

**Setting (in-model).** An item (a claim, a fact, a test) changes state at the events of a renewal process. Let a = time since its last change and h(a) the hazard. A follow-up reveals the true state at cost c. If the item changed and is not followed up, the loss is w per unit time over an exposure horizon L. New evidence arrives with likelihood ratio Λ ("surprise": evidence that the item woke up) for "a change happened in the last window Δ".

**Proposition SG.** Follow up iff w·L·p > c, where the posterior odds are p/(1−p) = Λ·p₀/(1−p₀) and p₀ = P(change in (a, a+Δ] | no change by a) = 1 − S(a+Δ)/S(a).
- (i) **Regime A** (exponential, h = λ): p₀ = 1 − e^{−λΔ}, independent of a. The time since the last *change* carries no information; only the time since the last *check* and the surprise matter.
- (ii) **Regime B** (scale-free, Lomax hazard h = γ/(a + a₀)): p₀ = 1 − ((a+a₀)/(a+Δ+a₀))^γ ≈ γΔ/a for a ≫ Δ. The surprise needed to justify a follow-up is ln Λ\* = ln(c/(wL − c)) − logit p₀, which grows as **ln a with slope 1**: a dormant item needs surprise proportional to the log of its dormancy, and a recently changed item needs almost none (follow bursts).
- Check: Monte Carlo (2·10⁶ draws) matches the p₀ formulas to 3 decimals; fitted slope of ln Λ\* on ln a = 0.995 (`AUDIT_checks/sg_check.out`).
- **Status: elementary (Bayes plus a renewal hazard); novelty unlikely.** Prior art: restless bandits and the Whittle index (Whittle 1988 [classic, not re-fetched]); Whittle-index scheduling for Markov sources with uncertainty or "age of incorrect information" (e.g. arXiv 2102.06384 [search]); crawler revisit policies (Cho & Garcia-Molina 2000/2003 [search]; an RL scheduling paper on erichorvitz.com [search, authors not verified]); Bayesian surprise as a driver of attention (Itti & Baldi 2009, *Vision Research* 49:1295–1306, doi 10.1016/j.visres.2008.09.007 [search, abstract read]); information foraging (Pirolli & Card 1999 [classic, not re-fetched]); Gittins indices (for rested bandits, which do not fit a world that changes on its own). **What GTAO adds, at most:** which clock matters is set by the measured drift regime (since last change in B, since last check in A), and the log-dormancy threshold, joined to the keep rule. That is a regime-conditional statement, testable by its sign and slope.
- **Fit to the SELF finding.** Most later changes were dormant items coming back. Under (ii) the right policy for those is not a schedule at all but a surprise trigger: any evidence touching a dormant item (or its shared driver, e.g. Chad raising the topic) prompts a reread of that item and its neighbours. The schedules that lost in SELF (√, recency, geometric back-off) were all schedules.

**Verifiable form.** QUEUE.md is now ordered by this rule (`queue/sg_rank.py`, locked parameters γ = 0.4 from SELF P1b, a₀ = Δ = 1 day). Every choice is logged in `queue/LEDGER.jsonl` with Ace's unaided order written *before* the rule is run and a seeded uniform pick. Outcome per completed item: did a CLAIM_MAP status change. Score after ≥ 15 completed items: AUC of the rule's index vs Ace's unaided rank vs uniform for predicting a status change. Locked prediction: rule AUC > 0.5 and ≥ Ace's AUC. Kill: rule AUC ≤ 0.5, or below Ace's by > 0.1. One in three picks goes to Ace's top unaided choice when it differs, so both rankings get outcomes. Limits: the parameters w, v, L, c are judgments (logged, so auditable); n will be small this week.

## 7. Dream big: the most profound results within reach

1. **Derive the spectrum → design map and close the two-core gap** (SPECTRUM-MAP-DERIVE). One theorem that takes a measured spectrum S(f) ∝ f^{−α} (H = (α−1)/2 in the fractional range) and returns, jointly, the read-rate exponent (1/(1+2H) for hold-and-read; to derive for the optimal predictor), the number and spacing of memory stores (one store in regime A, a log-spaced ladder in B), and the forgetting exponent, *and* resolves MATCH1 D3's opposite sign. If it exists, it is the theory's headline made exact; if it cannot be made to give a non-trivial prediction beyond approximation theory plus a price, the headline should be demoted in THEORY.md, honestly. Either outcome is real progress. Test: math referee, then item 2.
2. **One crossover in one system** (SPECTRUM-BRIDGE-SIM, then field). The sharpest cross-scale prediction GTAO can make is a *crossover*: the same adaptive system, fed a single-pace world, should show ½ and one memory timescale; fed a scale-free world, slope 1 and layered, power-law memory. Fairhall et al. 2001 already show slope 1 in a switching world for the fly H1 neuron (THEORY §2.4). In-model first, with learners that choose their own estimator and number of stores and are never given the cost function; then a fully measured field system where H is measured from the same target and the read rate is designed (software upstream tracking with an H gate; designed chemotaxis stimuli for cells).
3. **The theory runs our own research** (SURPRISE-GUIDED-SEARCH + SELF-2). Small, fully measurable, and scored by outcome: does a regime-B, surprise-triggered rule pick better follow-ups than uniform and than unaided judgment, and does a shared-driver (topic-level) reread beat per-item schedules in Ace's memory once drift is measured from real source-change times? Not profound alone, but it is the only setting where every quantity is logged.

## 8. Limits of this audit
- One executor, about 40 minutes; not independently reviewed. Night-1 files were checked by targeted reads and greps, not line by line (CORE_AUDIT, ARCH_EQUATION §0, FORMAL axioms and Lemma 1, FRAMEWORK §3.1/§6/§7, CLAIM_MAP_v2, SELF, GITHUB, LEARNSIM preregs, the referee report).
- Chat history before this session was not readable from here; rows 14–15 rely on the parent conversation as relayed and on memory notes.
- Proposition SG's prior-art check was three web searches; a targeted search (renewal-process change detection, monitoring with decreasing hazard) is queued before any novelty claim.
