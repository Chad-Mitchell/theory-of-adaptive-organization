# Round P: is "the closed whole starts pure" (P) selected by a cost? Result: no. In this model P is an interpretive premise. (private R&D note)

Date: Thu 26 Nov 2026, 01:33–01:40 EST. Preregistration: `PREREG_P.md`, sha256 a4e02d65af9a8ab27f82791c245e2ef06f7ff6511b938d12a77fe4aa5122bb5d
(`PREREG_P.sha256`, verified unchanged after the run). Script `scripts/p1_track.py`, output `outputs/p1.txt`.
No git. No new citations this round. Superdense coding and Holevo-type bounds were already cited (Bennett–Wiesner
1992, Crossref-checked in Round E). The Holevo bound is used as standard textbook knowledge, with no DOI claimed.

## Plain summary
We asked whether the theory's own costs prefer a world that starts in a definite state over a classical world that
needs built-in randomness in order to track anything. They don't. At equal capacity, both worlds track equally well.
They cost the same under the existing terms, under the "unheld label" rule, and on capacity for repeated tracking.
Only a price put directly on global randomness separates them, and that price is premise P in another form. So P stays
an interpretive premise. This is a preregistered miss for "P cost-selected", and it matches the prediction made before
the run.

## Results vs preregistered predictions (all observed or proved in model; no falsifier triggered)
| item | prediction | result |
|---|---|---|
| Pr1 classical minimal S(W) for Θ(1, 0) | exactly 1 bit; pure infeasible | **1.000000000000 bit**, pure infeasible (n = 2: 24 perms × 5² starts; n = 3: 40320 perms × 5³; n = 2 fine grid 41²; ε = 0 and 0.01) |
| Pr1 QM / stabilizer pure start | feasible at S = 0 | CNOT\|+0⟩: P(A = 1) = 0.5, B's success 1.000000000000000. Stabilizer: 24 of 60 Clifford-reachable states are maximally entangled |
| Pr1 boxworld | infeasible | infeasible (trivial group, E1; success 1/2) |
| Pr2 U1 on product starts | 0 | 0 (classical: config read; QM: eigenbasis read, e.g. S = H = 0.881290899231) |
| Pr3 K0 | tie | tie (2c vs 2c, same success) |
| Pr4 K2 | +κ·1 bit for classical (definitional) | +κ·1 bit |
| Pr5 K3 | 2T both | classical: T = 1 needs 2 parts; T = 2 is infeasible at 3 parts (exhaustive, starts on {0, ½, 1}) and feasible at 4. QM 2T (construction + Holevo). Tie |

**Decision (rule fixed in the prereg):** K0, K1 and K3 tie, and only the definitional K2 separates. So **P is an
interpretive premise in this model.**

## Notes and limits (not deviations)
- At ε = 0.01 the classical minimum is unchanged, because the novelty condition H(A) ≥ 1 bit forces an exactly
  uniform A. A softer novelty threshold was not preregistered and was not run.
- K2 does not pick QM over stabilizer theory either: both are pure-start feasible at S = 0. So even the definitional
  price would need all reads allowed (NR) to reach QM.
- Haar-random unitaries rarely reach the task (Schmidt entropy ≥ 0.99 bit for 0.19% of 10⁴ samples; mean 0.4838 bit).
  Tracking needs a tuned interaction, not a generic one. This is observed, not used in the decision.
- Reading: the gap between the worlds is where the randomness sits, not how much it costs. Classically the randomness
  being tracked must be in the global state. In QM it can arise locally from a pure whole. The theory's current costs
  price records, capacity and errors, and none of them sees where the randomness sits. Pricing that location would
  have to be a new principle, and it would be P again.

## Consequence for the chain (PREMISE_GRAPH.md unchanged)
- Chain β (toward U) keeps P as an **assumed, interpretive** leaf. The wording for any fold is "proved in model given
  P (the closed whole starts pure; interpretive, not cost-selected: PREREG_P miss)".
- Chain α needs only Pprod (mixed allowed), so this miss does not touch it.

## Sharpest next step
Stop trying to price P, since this test shows the cost can't see it. Two options remain. (a) Accept P openly as the
"ignorance is perspectival" premise, the companion to the self-reference result that every internal description is
mixed. (b) Route around P: chain α already avoids it, at the price of B and CR. So the real bottleneck for chain β is
again Conjecture C plus P, and for chain α it is B and CR.

## DEVIATIONS
None.

*Appended 26 Nov 2026 (after the DEVIATIONS line above; not a deviation of the run, but a scope note):* the ε = 0.01 arm of the locked PREREG_P is degenerate unless reads on A are capped. The run used binary reads, so its results stand for binary reads. See `NOTE_PREREG_P_EPS.md`.
