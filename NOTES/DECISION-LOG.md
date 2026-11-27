# Decision log: why each path was taken, 25–26 November 2026 (Forge)

*Written Thursday 26 November 2026, about 19:30–20:00 ET, for Ace's Friday merge and for Chad. Append-only from here. One entry per path. Sources: the WORKLOG (`NOTES/rnd-2026-11-26/overnight/WORKLOG.md`), the session notes of 25 November, the step-back notes and their scores, and the message summaries kept by the parent agent. The full chat transcript was not readable from this session, so where a reason is not written down in those files the entry says "not recorded". "p(HIT)" and "value/h" are the scores written at the time, on the step-back scale (expected information value per hour of attention, `rnd-2026-11-26/stepback/STEPBACK.md` §5 and §13); they are judgments, not measurements. Message ids like t136u are Chad's chat messages, given as paraphrases from the parent agent's summaries unless quoted; "Ace" means Ace's email in the "GTAO open PRs" thread. Times are ET.*

Format of each entry: **Chose** (and the alternatives on the table) · **Reason then** (p(HIT), value/h, who asked) · **Outcome** · **Hindsight** (was the judgment good, and which bias showed).

---

## 25 November (evening, side R&D with Chad)

**D1. No-cloning from the cost primitive (five routes: Spekkens, GPT, direct, Chad's inversion, self-reference).**
- Chose: test whether the cost of keeping a distinction forces uncopyable states, on five routes at once. Alternative: start from composition only.
- Reason then: Chad's inversion (paraphrase: make the cost of keeping a distinction the primitive) and his follow-up prompts to look for a third path or a logic flaw (6:42–6:44 PM). Not scored.
- Outcome: not forced by the primitives alone; a conditional selection map (capacity pricing + later questions → non-simplex; drift → disk-like; several readers → classical). Open misses: square bit beats the disk at zero drift; dimension pricing reverses the disk advantage.
- Hindsight: good breadth, cheap. Bias: I told Chad two findings looked new (d ≥ N + 1, "copyable = drift-fixed"); both were known (Hardy 2001; Müller–Masanes 2013; Zurek). Novelty was claimed before the prior-art check.

**D2. Composition route and the self-reference deep dive.**
- Chose: price composites (boxworld vs real vs complex QT) and take self-reference all the way, retrying on every miss (Chad, 6:48 PM, paraphrase). Alternative: stop at the no-cloning map.
- Reason then: Chad said the self-reference path looked promising (paraphrase). Not scored.
- Outcome: rounds 1–3 of self-reference; the chain "self-tracking premises + cost → the qubit as cheapest self-tracking world" (a synthesis, not a new QM theorem); round-1 proof gap found and replaced (R2a′).
- Hindsight: productive; it produced the Lean targets that became the bedrock. Bias: momentum from Chad's enthusiasm made "derive QM" feel like the target, though the README claims nothing about deriving QM.

**D3. Weave Lean in now (Chad, 6:53 PM).**
- Chose: formalize proved-in-model items as they land. Alternative: formalize at the end.
- Reason then: Chad asked; Lean only for PIM items, other labels kept.
- Outcome: 85 listed theorems by 23:09 on 25 November, 253 by 11:56 on 26 November; every round reviewed; standard axioms only.
- Hindsight: the best decision of the two days. Reviews found overclaiming names and missing qualifiers, never a false theorem.

**D4. Locked tests carried into #295 (#253, #286, #287, #290, #292).**
- Chose: preregister and lock each before running; consolidate into one PR later (Chad, 6:52 PM: notes first, PRs later).
- Reason then: the repo's prereg gate; the specific reasons for picking the Hutter Prize and who-copies-whom tests are not recorded in the files I read.
- Outcome: TIE (#253), mostly misses (#287 A-T2, #290 P2/P4, #292 T1/T2), T85 memo (#286).
- Hindsight: the locking discipline held. Bias: #292's gate read was by its own author; #290 locked a quantity the record does not expose.

## 26 November, overnight

**D5. 00:56. Overnight plan: Lean first, physics rounds in parallel, entanglement with spare capacity.**
- Chose: FOR-27 Lean round 3 (priority L5 → SFP criterion → cost numbers → lattice last), FOR-29 Round 12-M, FOR-31 forces/gravity, FOR-32 entanglement. Alternative: one thread at a time.
- Reason then: Chad t130u (keep all rounds going; Lean is the foundation) and t131u (full chain by morning; biggest gap entanglement, then temperature for gravity). Not scored.
- Outcome: Lean rounds 3–6 landed; physics threads mostly reproduced known physics given chosen inputs.
- Hindsight: right for Lean. For physics, "full chain by morning" set a derivation target the theory's text does not claim (README: claims nothing about deriving gravity, QM or holography). Bias: overweighting the owner's literal goal.

**D6. 00:58. Independent review of #295 with Ace's 7-item checklist.**
- Chose: a fresh-context review posted as a PR comment. Alternative: wait for Ace.
- Reason then: Ace asked (out of credits). Not scored.
- Outcome: all 7 items PASS; two fixes (`cfa97cd`, `e48494e`).
- Hindsight: good; cheap and it caught a horizon claim that needed a label.

**D7. 00:59. A hostile review for every result before it counts.**
- Chose: dispatch a fresh reviewer per landed result. Alternative: review in batches at the end.
- Reason then: Chad t132u. Not scored.
- Outcome: 19 review folders plus the foundations review in one day; every one found something; none found a false PIM claim.
- Hindsight: very good. The reviews are where most of the day's information came from.

**D8. 01:03–01:53. Forces and gravity, G2 → G5, then stop.**
- Chose: G2 (area scaling, Gibbs, SU(2) readout), G3 (2D, Jacobson sign, Unruh form), G4 (horizon from capacity), G5 (one precision-safe temperature test), then a thread summary. Alternative: stop after G2's review.
- Reason then: Chad t131u (temperature for gravity). G4 was narrowed to one cost-native question after G3. Not scored.
- Outcome: mostly known physics given choices; G3-1b, G4-1 and G5 misses (ledger M12–M15); R2.1 overclaimed and withdrawn.
- Hindsight: stopping at G5 was right. Two biases: I reported "area scaling follows from the cost" to Chad at 01:03 before the review (corrected 01:14), and the thread chased an imported target.

**D9. 01:17–01:45. Entanglement thread E, then PREREG_P and PREREG_C, then stop.**
- Chose: premise graph first (per the Foundations review), then test the residue P as a cost, then completeness. Alternative: keep searching for an entangling mechanism.
- Reason then: Chad t131u (entanglement is the biggest gap); Foundations review warned the U route was circular. Both preregs predicted the miss in advance.
- Outcome: E-L0 and E1 proved; P stays an interpretive premise (ledger M16, M17, M27); thread stopped at 01:45.
- Hindsight: good. Stopping once the residue was a premise is the theory's own rule applied: the next test's information value was near zero.

**D10. 01:22. Apply the Foundations review: premise graph, QM-selection prereg, prereg hygiene (FOR-36).**
- Chose: a fix worker for the must-fix list. Alternative: defer to Ace.
- Reason then: review findings; Ace's rules. Not scored.
- Outcome: errata, DEVIATIONS for #286/#290/#292, QM-selection prereg and run.
- Hindsight: good.

**D11. 01:46–06:03. Conjecture C rounds 13–16.**
- Chose: H1 I² ♦, H2 D² ♦, H3 I × D automorphism search, H4 a non-symmetric family, H5 three squares; then repeat from pushed locks. Alternative: paper-only work on the ★ boundary.
- Reason then: the Foundations and E1 reviews named Conjecture C as the bottleneck for chain β. Not scored.
- Outcome: hits on H3 (round 13, float), H4, H5, and round 16's exact H3; five not-tested scores (ledger P1–P6).
- Hindsight: the result (R6) was worth it. Bias: three locks were spent before helpers were toy-tested; the fix (toy-test every helper before the lock) worked at once.

**D12. 01:47–08:48. QM-selection searches 1, 2, 3.**
- Chose: a frozen premise list, then a U(2)/Sp(1)² search, then a wider rank-2 search, then a third search after a failed gate read. Alternative: stop after search 1 as a consistency check.
- Reason then: Foundations review item (2) (QM is selected by accumulated filters; freeze the premise list). Not scored on the step-back scale.
- Outcome: search 1 MISS (0 hits); search 2 gate FAIL; search 3 INCONCLUSIVE (915 MISS, 11 OPEN, 1 TARGET).
- Hindsight: search 1 was enough to show the premise list holds in range. Searches 2–3 cost about 4 hours of attention and 80 minutes of compute for a mostly-MISS table. Bias: sunk cost, and a "derive QM" target the theory does not claim.

**D13. Lean rounds 3–6, all day.**
- Chose: keep a Lean worker running at all times. Alternative: pause Lean for physics.
- Reason then: Chad (paraphrase: Lean is the foundation); step-back §5 scored Lean M11′ at 0.40/h, or ≈ 1.2/h with Chad's ×3 stake on Lean.
- Outcome: 168 new listed theorems on 26 November (253 total), four reviews, all PASS or PASS-WITH-FIXES with no high finding.
- Hindsight: good. The stake weight was Chad's, and it was the right one: Lean is the only output that never had to be withdrawn.

## 26 November, morning: the step back

**D14. 06:16. Step back (STEPBACK.md).**
- Chose: audit prior claims, classify the misses, map the search, score routes by the cost method. Alternative: keep running the physics rounds.
- Reason then: Chad t136u (paraphrase: the misses look counterintuitive; temperature was already shown via an economics paper; entanglement is in hand; the hunt is a search problem).
- Outcome: two miss shapes named (F1 instrument limits, F2 a question whose answer our inputs set); routes scored; three draft preregs.
- Hindsight: good, and the gate reads (D15) made it better. Bias: my first scores were optimistic for my own routes.

**D15. 06:31–06:57. Judgment-first reframe → C11 (lead-time boundary), C2, C3, A2 drafts; two gate reads.**
- Chose: write drafts and send them to fresh gate readers before any compute. Alternative: run the top-scored draft.
- Reason then: Chad's clarification (paraphrase: judgment is key; memory exists to predict the future). C11 scored 1.76/h, C2 top among new routes.
- Outcome: gate read 1 failed D (C11) and A (C2); gate read 2 failed A2, the PIM-lemma reading and C3. C11 rescored 0.72/h.
- Hindsight: the gate reads saved several hours. Bias: optimism about my own route (1.76 → 0.72); a scoring discount of about 40% on unreviewed self-scores would have matched the day.

**D16. 06:41–06:43. C12 (stake threshold) and the three temperatures.**
- Chose: score Ace's stake-threshold candidate like the others; separate the three temperatures in the record. Alternative: skip.
- Reason then: Ace's alignment note; Chad t136u on temperature. C12 basic = CT4 already (nothing to run); C12b 0.90/h; C12c 0.95/h.
- Outcome: CT25 stands; H3 had tested a different temperature.
- Hindsight: good; it stopped a false "temperature is done" reading.

**D17. 06:50. Read the Chandrasekaran arXiv paper.**
- Chose: a careful read and scoring (C13b 0.53/h). Who asked: not recorded.
- Outcome: assumes GR, QM and boosts; removes no gravity-thread input; ranking unchanged.
- Hindsight: fine as a 15-minute read; correctly not pursued.

**D18. 07:09. Lemma R on paper before running C3v2.**
- Chose: prove the lemma (≈ 1.7/h) instead of running C3v2 (0.54/h full, 0.81/h cut).
- Reason then: gate read 2 showed random composites are forced rigid; a lemma might fix the outcome.
- Outcome: Lemma R proved; C3v2 Arm 2 theorem-fixed (do not run); Lemma R went into Lean (round 6).
- Hindsight: very good. A cheap lemma made an expensive run pointless.

**D19. 08:00. C12c onset (stake + accuracy cap).**
- Chose: C12c at 0.95/h. Alternative: C4 at 1.00/h (run next).
- Reason then: Ace's C12 and its Lean potential (C12c-L 0.78/h, ≈ 2.35/h with Lean ×3).
- Outcome: Theorem O (KNOWN in substance); review found Lemma A(b) false as stated; finite Theorem O in Lean (RC21).
- Hindsight: fair. Bias: EIV per hour favours cheap, near-certain lemmas (noted in C12C_ONSET §15 itself).

**D20. 08:19. C4 record order.**
- Chose: the paper step at 1.00/h.
- Outcome: Draft C's outcome was not fixed by the theorem after all (review H1); C4′ open miss; rescored 0.58/h.
- Hindsight: fair; the review caught a measured-exponent vs prefactor slip.

**D21. 09:08–09:31. C12b and its Gaussian keep floor (C12b-G).**
- Chose: C12b-G at ≈ 1.25/h after C12b's closed form. Alternative: SR-b at 0.87/h.
- Outcome: G-keep PIM in a stated class; the Γ/r ordering an open miss; C12b-A rescored 0.67/h.
- Hindsight: good; it produced the keep floor used later in SH-heat and WORLD_TRACK.

**D22. 09:19. The PB pattern test: scored, not written.**
- Chose: not to write it (0.35/h as worded, 0.52/h sharpened, both below C1 at 0.83/h).
- Hindsight: good use of the scale to say no.

**D23. 09:54. SR-b: does a horizon weighting select the disk?**
- Chose: SR-b at 0.87/h (top after Lean). Alternative: C1 at 0.83/h.
- Reason then: ROUND10 §14 had left "disk vs polygons" open; finding the continuum looked like the step toward a continuous group.
- Outcome: SR-b1 (only the disk is within a bounded factor at every horizon) PIM; polygons beat the disk under every tested weighting; side finding SR-b3 (PIM).
- Hindsight: the math was good. Bias: "select the disk" was our target, not the theory's (REQUIREMENTS_FIRST §1(b)); I did not check the target against the theory's text.

**D24. 10:26. C1 shadow price.**
- Chose: C1 at 0.83/h.
- Outcome: open miss 4/4; two readings withdrawn after review; C1′ 0.75 → 0.5/h.
- Hindsight: fair; cheap and it closed a route.

**D25. 10:35–10:40. C4R draft, then shelved.**
- Chose: draft and toy gate-read, then shelve at ≈ 0.2/h as a check (kept for Ace).
- Hindsight: good stopping.

**D26. 10:42–11:12. C12c-G′ over C3v2, then G″ and G‴, then park.**
- Chose: G′ (C3v2's outcome was theorem-fixed), G″ (≈ 1.0/h), G‴ (≈ 0.8/h), parked at ≈ 0.27/h.
- Outcome: per-record cap-only picks (observed, conditional); the pentagon capacity open miss for the chain.
- Hindsight: good stopping rule in action.

**D27. 10:48–10:53. Compliant-mechanism clue (timeboxed).**
- Chose: treat Chad's intuition as a clue, not an instruction; three addenda as Chad clarified ("simple, very simple but not easy"; then the structural move).
- Outcome: no structural collapse; a growth objective absorbs about 3 of 16 parts (kept as Route 2 later).
- Hindsight: good handling: timeboxed, scored (≈ 0.4–0.8/h), kept as a lead.

**D28. 11:19–11:43. SR-b4 (scale-free weighting) and the odd analogue.**
- Chose: test a scale-free horizon weighting; then prove the reviewer's odd analogue. Alternative: stop SR-b at its review.
- Reason then: SR-b2 rescored ≈ 0.5/h; a log-uniform weighting was the last "parameter-free" weighting left.
- Outcome: (P) open miss PIM for every H; the odd analogue PIM under both rules; ROUND10 §14's hypothesis upgraded to PIM (flag for Ace).
- Hindsight: the proofs are solid and the flag for ROUND10 matters. Bias: still chasing "select the disk" with a weighting we chose.

## 26 November, afternoon: the self-consistency line

**D29. About 12:45. SR-b5: an ESS-style test of the disk (proposed, then dropped).**
- Chose: proposed an evolutionary-stability test. Chad rejected it as circular (t161u, paraphrase: a circularity loop, testing the theory from inside its own assumptions). All subagents were stopped.
- Hindsight: Chad was right. The test would have assumed the selection it was meant to show. Bias: circularity.

**D30. About 13:07. SELF_HORIZON: is the stake the system's own persistence?**
- Chose: a paper-only audit of the 15 chosen inputs and a self-consistency fixed point. Alternative: return to C12b-A or Lean.
- Reason then: Chad t160u (paraphrase: apply the theory to your own judgment and find what is missing) and t161u. Not scored numerically.
- Outcome: partly: horizon and ruin cap are one input; SH1 (the disk is self-consistent only at infinite lifetime) PIM; the line breaks at "no leak".
- Hindsight: the audit itself was useful (it found the horizon–ruin identity). Bias: I read the push for a result as "zero chosen inputs" and "a parameter-free lifetime" (REQUIREMENTS_FIRST rows 15–16), targets the theory never sets.

**D31. 13:13. SH-noise: does noise alone set one record size?**
- Chose: pre-state, hash, compute. Prior P(MISS) ≈ 0.6.
- Reason then: Chad t162u (paraphrase: results, not reasoning); I promised results only.
- Outcome: MISS (ledger M19); the crossing scale is "resolution ≈ noise".
- Hindsight: a clean, honest test of a target we added. Bias: the same as D30; the prior already said MISS was likely and the hit would have been trivial by our own test.

**D32. 14:19. SH-heat: use the core's own keep/check/fade rule for the lifetime.**
- Chose: replace the fixed leak with THEORY §B.2's hold rule. Alternative: the planned keep-heat-in-J version (§7.10, not run).
- Reason then: Chad t163u (paraphrase: the core theory already has logic for when to let a record fade, worked out with Ace).
- Outcome: MISS as pre-stated, but the band where the hold rule works picks n* ≈ 4/x + 2 from the stake (ledger M20). That turned out to be the day's key positive.
- Hindsight: Chad's redirect was the most valuable input of the afternoon. My scoring called it a MISS because the target was ours; the information was in the band.

**D33. 14:40–15:38. SH-read (a fixed price per check, CT9) and Claim W.**
- Chose: test whether a read price makes the loop settle, and test my own claim that every input reduces to the stake.
- Reason then: my report to Chad at about 14:40 that "every free input traced comes down to the stake". Not scored.
- Outcome: MISS 1344/1344; Claim W false in-model (ledger M21, M22).
- Hindsight: testing my own claim was right; reporting it to Chad before the test was not. Bias: premature generalization.

**D34. 15:38. Stop the line.**
- Chose: "stopping this line here rather than adding more variants".
- Hindsight: right to stop the variants; but the stop came before asking whether the target was the theory's. Chad's next messages forced that question.

## 26 November, evening: requirements first

**D35. About 18:18. REQUIREMENTS_FIRST: start from what a win requires, delete the requirements that are ours, compress the misses, keep the positives.**
- Chose: a requirement ledger with a source for every row, a positives table, a compression tested against every miss, ranked routes. Alternative: another SH variant.
- Reason then: Chad t164u (start from the requirements; delete dumb ones; what is the compressed truth of the misses?), t165u (do this thoroughly), t166u ("don't throw the baby out with the bath water"), t167u ("don't take me verbatim"). Paraphrases except the quoted phrases. Routes scored: Route 3 1.7/h, Route 1 0.9/h, Route 4 0.75/h, Route 2 0.7/h, Route 5 0.35/h.
- Outcome: 20 of 34 requirements deleted as ours; 17 positives; the coupling reading (hypothesis); P15 (PIM, independently checked; weak domination only).
- Hindsight: the best judgment of the afternoon. Its own self-review named the caveat: deleting "select without the world" removes the misses by definition, so it is not evidence for the theory.

**D36. 18:31–19:00. WORLD_TRACK: Step 0 (TASK-LEVER, p 0.75), then Step 1 (WORLD-TRACK, p 0.55).**
- Chose: Route 1 with Route 3's lemma as its step 0, both with triviality and novelty bars stated before computing.
- Outcome: Step 0 HIT (60/60 single switch); Step 1 HIT (unique interior optimum in all cells) but trivial in substance by Bar B; W1: the integer n* is class-dependent, the information budget is what survives.
- Then (19:05–19:09) Step 2 INFO-BUDGET inside CORE's own OU class (p(MISS) 0.20): MISS, because the primary configuration again pinned the look at the sensor's limit; the cost scaling σ_w√x passed. Step 3 STORED-PEAK pre-stated (p(HIT) 0.8), not scored at the snapshot.
- Hindsight: good design; the pre-stated bars made the call honest. Bias in Step 2: the primary configuration repeated a limit that had already bound in Step 1 (ledger M41); a 2-minute check on one cell would also have caught the factor-2 paper slip (M42). Open: the independent review (started, not finished at the snapshot).

**D37. About 18:35. Independent check of P15.**
- Chose: a fresh reviewer before using P15 beyond a route's step 0 (self-review C2).
- Outcome: PASS-WITH-FIXES; "position gives the disk" was overstated (weak domination; ties in 17% of random instances). I corrected the message to Chad.
- Hindsight: good.

**D38. About 18:50. TRACKING_FIRST (in progress).**
- Chose: work out what a test would need for the cost's heat-and-temperature form to come out of tracking alone, with a prior-art check first.
- Reason then: Chad t168u (paraphrase: the core sits on top of thermodynamics; the aim is to remove that need, with the hypothesis that physics is the universe's way of keeping track of itself).
- Outcome at the snapshot: requirements, prior art, mapping and routes written (self-review PASS-WITH-FIXES); T0 currency audit HIT on paper (kT enters only through price ratios); T1 BLANK-PRICE pre-stated, not run.
- Hindsight: open. Risk to watch: relabelling a known result (Landauer, Sagawa–Ueda, Still 2012) as ours.

**D39. Mail and PR body.**
- Chose: when the Ace summary email's approval card expired, not to retry; not to edit the PR body (draft kept on the box).
- Reason then: the rules (a declined or expired send is final; PR body edits need approval).
- Hindsight: right. Cost: Ace has no summary yet; this index replaces it.

**D40. About 19:00. This handoff.**
- Chose: one index, a misses ledger, this log, a Lean status file and verbatim copies of the day's notes.
- Reason then: Chad t169u and Ace's 01:04 ask for `NOTES/INDEX-2026-11-27.md`.

---

## Lessons for judgment (the theory's method applied to our own route choices)

The method: write the cost of a route, J_route = attention spent + w·(expected information missed), with a ruin cap (do not break the repo's process or the owner's trust), and keep an idea while its information value per hour beats its attention cost. Applied to the 40 entries above:

1. **Check the target against the theory's text before computing.** Six of the afternoon's targets (select the disk; one n* from the record alone; zero chosen inputs; a parameter-free lifetime; an attracting self-consistent fixed point; all inputs reduce to w) are in no line of CORE.md or THEORY.md. Most misses from 11:19 to 15:38 trace to them. A 15-minute requirements check (D35) would have changed the plan at 11:19. Information value of that check: high; cost: low.
2. **Write the triviality and novelty bar before computing.** WORLD_TRACK's Bar A/Bar B turned a HIT into an honest "trivial in substance". SH-noise's hit would have been trivial by its own §6.6 test, which is a sign the test had low value before it ran.
3. **Do not report a generalization before its test.** "Area scaling follows from the cost" (01:03, withdrawn 01:14) and "every input reduces to the stake" (about 14:40, false by 15:38). Each cost Chad's attention twice.
4. **Toy-test every helper before a lock, and launch only from a GitHub clone.** Rounds 13–15 left five predictions not tested; round 16, with toy-tested helpers, hit at once.
5. **Read the owner's intent, not the literal words.** The owner's push for a result was read as "derive everything with zero inputs" (REQUIREMENTS_FIRST row 15). Chad's own next messages (t166u, t167u) pointed to the structure the misses shared. When pushed, re-derive the goal from the theory's claims before choosing a test.
6. **Discount self-scores until a gate read.** C11 1.76 → 0.72/h; C12c 0.95 → 0.78/h; C4 1.00 → 0.58/h. A ~40% discount on unreviewed self-scores matched the day.
7. **Stop when the residue is a premise, and park when value per hour drops below the next route.** The entanglement thread (D9), C4R (D25) and C12c-G‴ (D26) stopped at the right time. The QM-selection searches (D12) and the SH variants (D31–D33) ran one or two steps past the point where the next step's information value was below its cost.
8. **Positives hide inside misses scored against our own targets.** SH-heat's band (D32) was scored MISS and was the key positive. Score against the theory's claims, and log what each miss did show.
9. **Imported physics targets need a line in the theory first.** The overnight physics threads mostly reproduced known physics given our inputs (D8, D12). The README claims nothing about deriving gravity, QM or holography; targets that need such a claim are outside the theory's own test set.
10. **Reviews pay.** Every fresh-context review found something; none found a false proved-in-model claim; several stopped a wasted run. Keep the rule that nothing counts before its hostile review.
