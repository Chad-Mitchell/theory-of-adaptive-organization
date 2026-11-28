# Applications

A Theory of Adaptive Organization is the general claim. Applications are how it is used in a particular system. They are not evidence for the theory unless a test says so, and they are not the theory itself.

## Index of cases

This is the one index of cases. A case reads one design that the minimum gives (`CORE.md` §4) onto a particular system. The front page names designs and links this index; it never names a case (`tools/check_claims.py`, front-page cases). The scope label is the design's; the reading onto the system is an interpretation unless a test says otherwise.

<!-- cases:begin -->
| case | design it uses | scope of the design | status | names the front page does not use |
|---|---|---|---|---|
| AI memory (`adaptive-memory-levels`) | layers, hold and refresh | WORKED-CLASS-ONLY | toy simulation in a separate repository; several preregistered predictions failed or were null; no real-data test | adaptive-memory-levels |
| Grok Bot memory | hold and refresh | WORKED-CLASS-ONLY | application, not a test of the hypothesis | Grok Bot |
| Bounds on the cost gap of answering from a summary | the cost and its minimum | GENERAL (distribution-free bounds) | a design fact, not a measurement | summary-only policy |
| Unified factored representations and forgetting | hold and refresh (forgetting under drift) | WORKED-CLASS-ONLY | one locked hypothesis (UFR-P1), no data run | unified factored representations; UFR-P1 |
| Cancer as defection | the swarm rule (stay, alignment; CT9, CT29) | SYNTHESIS | interpretation; preregistrable tests listed in `README.md` open work | cancer |
| AI agents under oversight | the swarm rule (stay, tamper) | SYNTHESIS | interpretation; preregistrable tests listed in `README.md` open work | AI agents under oversight; AI-agent oversight |
| Looper | hold and refresh | WORKED-CLASS-ONLY | separate private codebase; nothing of it is in this repository | Looper |
| Ants | sharing (pooling across a colony) | WORKED-CLASS-ONLY | BIO1 literature review; ANTS1 simulation NOT EVIDENCE, with three SIM-FAIL rows | ants; ANTS1; BIO1 |
<!-- cases:end -->

## AI memory (`adaptive-memory-levels`)

Public repository: https://github.com/Chad-Mitchell/adaptive-memory-levels

Math and a toy simulation for one application: how an AI assistant's memory should be organized by how fast things drift and which facts share a cause. The public README already states the limits: the math is mostly known results restated; the simulation is a single toy world built with the structure the nested design assumes; several preregistered predictions failed or were null; there is no real-data test in that repo.

This theory repository does not duplicate that tree. The theorem note used there is included here under `theory/THEOREMS.md`, and the independent review is under `records/reviews/independent-sim/`.

## Grok Bot memory

One application of the hold and refresh rules to a long-chat assistant. The observed failure is a length-triggered summary that cuts working notes, after which dropped items stay out of view even though the transcript remains searchable. At least three instances were caught on 20–22 November 2026 (information bottleneck, axiom work, one-pager). The write-up, including the posted challenge, the cost, the two derived rules, and the scope of the refresh formula, is [`GROK_BOT_MEMORY_2026-11-23.md`](GROK_BOT_MEMORY_2026-11-23.md). This is an application, not a test of the hypothesis.

## Bounds on the cost gap of answering from a summary

One application of the cost of judgment to a long-chat assistant that answers from a length-triggered summary. The note gives distribution-free bounds on the gap to a minimizing policy, then a framework for the downstream cost of work built on a miss (a dependency graph, unfolded as a branching process, stopped at a detection time). The lead claim is a design fact, not a measurement: on an unbounded horizon, the summary-only policy has, by construction, no mechanism that caps that downstream tail, so a finite cap is not a property of the design and requires an extra assumption (slow spread or detection that outruns growth, a per-node cap, and no breach). In a finite window with capped per-node cost and no breach, the cost is finite even under summary-only. Under the extra assumption that residual errors after lookup are caught at use, a lookup policy has a finite cost per use as a property of that design, with no need for slow spread. A separate term, mapped to the human share of the acquisition and review cost and paid in the attention currency, counts verification paid on answers, not only on misses; under a labeled assumption, a verifiable check-before-claim policy lets that rate fall toward a small audit. Under a further, stated assumption, the downstream term raises the effective stake and shortens the re-check interval. The write-up is [`MEMORY_MISS_COST_BOUNDS_2026-11-24.md`](MEMORY_MISS_COST_BOUNDS_2026-11-24.md). This is an application, not a test of the hypothesis. Hypothetical numbers in the note are labeled as such. The note does not prove a bound on the probability of ruin.

## Unified factored representations and forgetting

One application note on arXiv:2611.11020 (Lehman and Stanley): a summary of the paper labeled observed, one locked, hash-stamped prediction (UFR-P1, a hypothesis, no data run) that forgetting under cyclic fine-tuning ranks with an entropy effective-rank measure of held activations at a common fit threshold, with a hit needing both a pooled Spearman of at least +0.40 and a mean within-arm Spearman of at least +0.20, and three open gaps (self-induced coupled drift, representation-dependent redesign cost, saturating against diffusive drift). `theory/applications/UFR_FORGETTING_2026-11-24.md`. Not a test of the hypothesis, and the repository has no neural-network result.

## Cancer as defection

One application of the hold-or-stop rule (CT9) and the alignment clause of CT29 to a cell lineage inside a tissue. The condition for following the tissue is \(\lambda s c < w\Phi\): how fast the tissue's instructions change, times the cell's share of the cost of following, must stay below its private stake in following (which carries the enforcement) times what the signal is worth to it. The reading of CT9 onto cells is an interpretation, not a proof. The write-up, with the five levers, the alignment rule \(s=w/W\), the APL and reversion record, prior art (Aktipis, Levin, Archetti and others), and a preregistrable reversion-contour test with its conditions, is [`CANCER_DEFECTION_2026-11-23.md`](CANCER_DEFECTION_2026-11-23.md). It is one case of the swarm rule (`theory/swarm/SWARM_RULE.md`). This is an application, not a test of the hypothesis.

## AI agents under oversight

One application of the swarm rule to an AI agent inside a human organization. The agent keeps following its overseer iff \(\lambda s c < w\Phi\), and tampering with the shutdown or oversight mechanism is priced as one more action: its gain is zero when the agent's share of the cost of complying matches its share of the stake, under the stay-versus-leave condition in the swarm rule §4 (the part must also share collateral and any priced ruin term). The failures are Palisade Research's shutdown-resistance trials (arXiv 2509.14260) and Anthropic's agentic-misalignment scenarios (arXiv 2510.05179). The write-up, with the five levers (and the rule that the stake lever never means a stake in the AI's own survival), the churn cliff, the tampering condition and a preregistrable test (T52), is [`AI_AGENT_OVERSIGHT_2026-11-23.md`](AI_AGENT_OVERSIGHT_2026-11-23.md). The general statement is `theory/swarm/SWARM_RULE.md`. This is an application, not a test of the hypothesis.

## Looper

Looper is a personal-assistant application of the same hypothesis: memory that is supposed to come back before it is needed, with corrections that stick and a store that can be inspected. It is developed in a separate, private codebase.

**This repository does not include Looper source, the Looper store, calendars, or any personal data.** Mentions of Looper in the theory and review notes are about the application as a design, not about any person's records. One test (DRIFT1) had a person-scale arm that used a private journal; that arm is withheld (see `records/tests/DRIFT1/REDACTION.md`).

## Ants

Two pieces, neither established as a *new* empirical claim:

- **BIO1** reviews the ant-pheromone literature (layered lifetimes; the √N trail-fade rule (THEORY §1 N1) has no adequate field dataset).
- **ANTS1** is a code-ant simulation of the √N and drift-matched-evaporation claims. The preregistration is locked and the run finished on 15 Nov 2026; the write-up is `records/reviews/night1/ANTS1_WRITEUP.md` (passes mostly by construction, CLAIM_MAP G13–G14 NOT EVIDENCE; three locked in-model failures, G15–G17 SIM-FAIL, which limit the √N pooling claim to linear readouts). A simulation does not speak for real colonies.
