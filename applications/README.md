# Applications

A Theory of Adaptive Organization is the general claim. Applications are how it is used in a particular system. They are not evidence for the theory unless a test says so, and they are not the theory itself.

## AI memory (`adaptive-memory-levels`)

Public repository: https://github.com/Chad-Mitchell/adaptive-memory-levels

Math and a toy simulation for one application: how an AI assistant's memory should be organized by how fast things drift and which facts share a cause. The public README already states the limits: the math is mostly known results restated; the simulation is a single toy world built with the structure the nested design assumes; several preregistered predictions failed or were null; there is no real-data test in that repo.

This theory repository does not duplicate that tree. The theorem note used there is included here under `theory/THEOREMS.md`, and the independent review is under `reviews/independent-sim/`.

## Grok Bot memory

One application of the hold and refresh rules to a long-chat assistant. The observed failure is a length-triggered summary that cuts working notes, after which dropped items stay out of view even though the transcript remains searchable. At least three instances were caught on 20–22 November 2026 (information bottleneck, axiom work, one-pager). The write-up, including the posted challenge, the cost, the two derived rules, and the scope of the refresh formula, is [`GROK_BOT_MEMORY_2026-11-23.md`](GROK_BOT_MEMORY_2026-11-23.md). This is an application, not a test of the hypothesis.

## Cancer as defection

One application of the hold-or-stop rule (CT9) and the alignment clause of CT29 to a cell lineage inside a tissue. The condition for following the tissue is \(\lambda s c < w\Phi\): how fast the tissue's instructions change, times the cell's share of the cost of following, must stay below its private stake in following (which carries the enforcement) times what the signal is worth to it. The reading of CT9 onto cells is an interpretation, not a proof. The write-up, with the five levers, the alignment rule \(s=w/W\), the APL and reversion record, prior art (Aktipis, Levin, Archetti and others), and a preregistrable reversion-contour test with its conditions, is [`CANCER_DEFECTION_2026-11-23.md`](CANCER_DEFECTION_2026-11-23.md). This is an application, not a test of the hypothesis.

## Looper

Looper is a personal-assistant application of the same hypothesis: memory that is supposed to come back before it is needed, with corrections that stick and a store that can be inspected. It is developed in a separate, private codebase.

**This repository does not include Looper source, the Looper store, calendars, or any personal data.** Mentions of Looper in the theory and review notes are about the application as a design, not about any person's records. One test (DRIFT1) had a person-scale arm that used a private journal; that arm is withheld (see `tests/DRIFT1/REDACTION.md`).

## Ants

Two pieces, neither established as a *new* empirical claim:

- **BIO1** reviews the ant-pheromone literature (layered lifetimes; the √N trail-fade rule (THEORY §1 N1) has no adequate field dataset).
- **ANTS1** is a code-ant simulation of the √N and drift-matched-evaporation claims. The preregistration is locked and the run finished on 15 Nov 2026; the write-up is `reviews/night1/ANTS1_WRITEUP.md` (passes mostly by construction, CLAIM_MAP G13–G14 NOT EVIDENCE; three locked in-model failures, G15–G17 SIM-FAIL, which limit the √N pooling claim to linear readouts). A simulation does not speak for real colonies.
