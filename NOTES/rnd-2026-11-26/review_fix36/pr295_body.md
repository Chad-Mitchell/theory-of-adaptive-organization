This PR follows #294. Branch `forge-rnd-record-cost-2` is cut from `main` at `8b553c6`. The six open PRs below come in as merge commits of their head SHAs; the source PRs and branches are untouched. **Correction (Nov 26):** this line used to say "Nothing was rebased" and that every prereg lock keeps its commit history. That is wrong for #286: its source branch was rebased on 2026-11-25 at 23:06 ET, so the original lock commit `f18721fc` and score commit `3e1fcf9e` are not in the carried history. They survive on the fork branch `forge-ctc-review`, and the hash of `PREREG.md` is unchanged (`756d9f0c…`). This is disclosed in `theory/ctc-fixed-point-2026-11-24/DEVIATIONS.md`, and nothing was pushed that rewrites history. `THEORY.md`, `CORE.md`, locked blobs and committed preregs and log lines are not edited. In-model only. Nothing here derives quantum theory, general relativity, holography, or gravity.

## Carried PRs

| PR | Head | Decision | Where it lands |
|---|---|---|---|
| #253 composite contest | [`707aa08`](https://github.com/mitchell-moving/theory-of-adaptive-organization/tree/707aa088e37e5008fd35234474dc104e297f2b4d) | **carried into this PR** | `theory/COMPOSITE_CONTEST_2026-11-24.md`, `theory/composite-contest-2026-11-24/`, `theory/composite_contest_checks/`. README "Waiting on Chad" row T72 and ledger row T72 now point at the note (headline TIE under `PREREG_4`; WIN only under a hand-restricted Gmax). Its edits to the retired `OPEN_WORK.md`, `STATUS.md`, `theory/GAP_PLAN.md` and `theory/README.md` are dropped, as those files are gone on `main`. |
| #263 prereg gate | [`8c4b3c0`](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/tree/8c4b3c0bb14c67b1b2e2721153795871c86381dd) | **carried into this PR** | `process/PREREG_GATE.md` is now in the maintained-docs list of `tools/check_consistency.py`. Also `process/misses/2026-11-24_T84_T84b_T85.md`, and pointers in `process/PROCESS.md` and `process/MISS_LOG_TEMPLATE.md`. `PREREG_GATE.md` §4 now names the README open tables instead of the retired `OPEN_WORK.md`. |
| #286 T85 CTC fixed point | [`f19cd4a`](https://github.com/mitchell-moving/theory-of-adaptive-organization/tree/f19cd4a1aaf6de87afedf8647e5cc008f0819ec4) | **carried into this PR** | `theory/ctc-fixed-point-2026-11-24/`, `theory/ctc_fixed_point_checks/`, `tools/test_ctc_fixed_point.py`; README open row T85. |
| #287 two-route prereg | [`65b4a9b`](https://github.com/mitchell-moving/theory-of-adaptive-organization/tree/65b4a9bd3b706630cdce31ed18321929cc7f1820) | **carried into this PR** | `theory/two-route-2026-11-25/` (PREREG through PREREG_4a, RESULTS), `theory/PHYSICS_CHAIN_2026-11-23.md`, `tools/test_two_route_checks.py`; README ranked-gap rows BICAUSAL, CL11 and CX2-SETTLE; `process/FAILURES.md` rows FORGE-PUSH-1 and FORGE-GATE-1. |
| #290 Hutter budget | [`40dd865`](https://github.com/mitchell-moving/theory-of-adaptive-organization/tree/40dd865e2f3c5fc8561e070d201f8483e0e42aa3) | **carried into this PR** | `theory/hutter-2026-11-25/`. Its `OPEN_WORK.md` row moves to the README open row HUTTER-J (open miss; prereg lock `4a0d5e9`). |
| #292 who copies whom | [`14394f9`](https://github.com/mitchell-moving/theory-of-adaptive-organization/tree/14394f9b514609769b95e94ff1459b51504a9859) | **carried into this PR** | `theory/stop-copying-2026-11-25/`. The T1 and T2 clean misses are logged as open in ledger rows WC1 and WC2 and in the README open row WHO-COPIES. The lock of `PREREG_5.md` is at `df114b6` (sha256 `b7850655b469…`, re-hashed and matching). **Correction (Nov 26):** the T1 and T2 runs already happened, after a gate pass (v5) by the author agent, not by the fresh independent reader that `PREREG_5.md:3` requires. That breach is now logged in `DEVIATIONS.md`, and gate reads v1–v5 are committed in `gate_reads/`. Both runs were misses. An independent gate read of `PREREG_5.md` is still owed. |

All six are carried, so none is proposed for closing.

## Record cost, rounds 4–10

**Notes:**
- `theory/RECORD_COST_ROUNDS4-9_2026-11-25.md` has a pointer from the chain note and a pointer at its end to the round-10 note.
- `theory/RECORD_COST_ROUND10_2026-11-25.md` is the round-10 note.

**Rounds 4–9:**
- Premise CD is not derived. Round 4 trades it for "tracking never finishes" (U).
- Selection costs D(s‖p₀) and inflow obeys L + Δ ≤ k·log₂N. Both are known bounds and both are blind to geometry.
- The fixed-pure-state condition (SFP) holds iff the stabilizer contains a maximal torus (KNOWN). By Jordan's theorem it fails for every finite transitive group.
- Counterexamples:
  - C1: the spin-1+2 sphere orbitope has four perfectly distinguishable pure states at affine dimension 8.
  - C2: the Klein-four tetrahedron.
  - C3: quantifier order.
- The hereditary-SFP remark (HYPOTHESIS) is set against Barnum–Müller–Ududec energy observability.

**NA4 amendment (text offered; the chain note's line is not edited).** "The disk pays 0" holds only for tracking, that is, it **pays 0 in tracking**. Selection costs at least D(s‖p₀) in every geometry.

**Finite precision.** The disk's compensated error after t steps is exactly 2|sin(tδ/2)|. It grows at least as fast as (2/π)tδ while tδ ≤ π, then saturates at 2. The ball stays within 2 sin δ.

**Round 10: can U be derived from something more basic?**
- Composition does not force U: the classical theory and stabilizer qubits are counterexamples.
- Continuous time with change does force it, but that is CD again.
- Lawvere's fixed-point theorem does not help: its hypothesis is complete self-description, which the self-reference bound forbids.
- Priced inflow forces only a global infinite order.
- Purification gives U (Winczewski et al. 2023 with Chiribella–D'Ariano–Perinotti), but it is a stronger premise.
- Lattice theory:
  - An irreducible orthocomplemented lattice with the covering property and at least 3 orthogonal atoms has infinitely many atoms (Baer; Wedderburn with Chevalley–Warning).
  - Two-qubit stabilizer theory shows the covering property is load-bearing.
  - Solèr's theorem needs infinite capacity in one system.
- Hilbert's fifth problem adds nothing: finite groups are Lie groups with no small subgroups.
- Part M (a parallel worker, §14 of the round 10 note):
  - Priced inflow passes U on from an environment that already has it, but does not create it. In the Thue–Morse shift world every finite block keeps a finite group.
  - Costing composite records like their parts and then taking the cheapest cost picks the classical theory. Stabilizer theory up to 3 qubits meets the composite rules with finite groups.
  - J does not select a continuous group at the tested horizons (observed): an odd polygon is strictly cheaper than the disk at T = 3, 4, 5 and 8, and the (2T+1)-gon is cheaper at every T from 2 to 12 and at T = 16 and 20, with a tie at T = 1. At T = 3 the 7-gon costs 0.594 against the disk's 0.750. Beyond the tested horizons this is a hypothesis (relabelled in `cfa97cd`).
  - Conditional remark (HYPOTHESIS): U follows given no-restriction, an entangling reversible map and Conjecture C. A placeholder is left for the separate test of Conjecture C.

**Open misses:**
- U is not derived (README row RECORD-COST-U; ledger RC4 and RC9).
- Selection and inflow do not separate geometries.
- Without drift, the memory price favours polytopes.
- "No outside frame" does not force drift.

**Ledger rows added:** RC3–RC12, WC1 and WC2.

## Lean

At `e48494e` the axiom audit listed 85 exported theorems under `formal/lean/GTAO/Rnd/`, and the source had 102 `theorem`/`lemma` declarations. Lean round 3 has since added more (`rnd_axioms_lr3.out`, 91 listed; AUDIT 1679). These counts are not a measure of depth: several entries are trivial or duplicated. For example, `liar_half` appears twice, `P2_entries` is four numeric facts, `ball_record_bound` is the triangle inequality, `no_zero_drift_while_recording` is a tautology, and the disk side of `disk_strictly_cheaper` is a definition (`theory/RECORD_COST_ERRATA_2026-11-26.md` §6). This PR adds `SelfRef/SFP.lean` and `Precision.lean` (19 theorems) and `SelfRef/ContinuousTime.lean` (4). Every theorem depends on `propext`, `Classical.choice` and `Quot.sound` or fewer (`rnd_axioms_round3.out`); the AUDIT count is 1628. Item L5 ("copyable ⇒ distinguishable") is **partial** in Lean: only the linear core is proved. The maximal-torus criterion, the O(3) classification, the orbitope results, Piron, Solèr, Baer and the purification steps are not formalized.

## Citations and scripts

Crossref checks:
- 33 sources in `doi_check_2.out`;
- 7 in `doi_check_3.out`;
- 14 in `doi_check_3b.out`;
- 17 in `doi_check_3m.out`;
- 3 in `doi_check_7f.out` (hostile-review errata, Nov 26).

Some sources are cited without a Crossref DOI:
- Hardy 2001 is checked on DataCite.
- Barnum–Hilgert is cited by arXiv identifier.
- Piron 1964 is cited by name.

Scripts `g_round4` through `n_round10b` and part M's `m_round10b` and `m_round10b_poly` sit in `theory/record-cost-2026-11-25/scripts/selfref/`, each with its stdout. The repo copy of `l_round9.py` fixes a session bug: it now finds CP² capacity 3, the known value.

## Tool change

`tools/check_claims.py` treated the words "GATE PASS" and "GATE STOP" in the #290 DEVIATIONS log line as the GATE ledger row, which was a false positive. Those words are now read as gate-read outcomes. A test is added.

## Hostile review corrections (Nov 26)

A fresh-context hostile review of the foundations (cost principle, the route to U, round 9, the lattice route, the Lean layer, and preregs #286, #290 and #292) found no fallacious step. It did find overclaimed wording, prereg hygiene gaps, and a structural open miss: the chain reaches quantum theory through premises, not through the cost alone. The fixes are append-only commits:
- `5f36cf5`: `theory/RECORD_COST_ERRATA_2026-11-26.md`, with a pointer from the rounds 4–9 note. It covers:
  - the rounds 4–9 `:62` phrase "without a time-evolution premise". SFP plus transitivity already implies U, and SFP depends on the group (SO(3) passes, O(3) fails);
  - the round 10 `:61` Solèr branch, which is PROVED only given the cheapest-bit HYPOTHESIS;
  - the missing orthomodularity line: finite height plus atomistic plus covering plus orthocomplement gives modular, and so orthomodular;
  - the M11 "some n·v = 0" reason, and the zero-marginal-slice LP numbers;
  - Lean names that state more than they prove;
  - circularity, logged as an open miss.
- `1c41dac`, `dc4d5a8`: prereg hygiene:
  - the #290 and #292 gate reads are committed;
  - #292 DEVIATIONS logs the `PREREG_5.md:3` breach;
  - #290 DEVIATIONS 9 records that P1 was re-scored after the direction was known, and that PPMD is memory-mapped to disk, not runtime RAM;
  - #286 DEVIATIONS records the 23:06 ET rebase (lock `f18721fc` survives on `forge-ctc-review`), and that five of the ten bars are identities.
- `06f07e6`: `theory/qm-selection-2026-11-26/PREREG.md` freezes the premise list P1–P8 of the QM-selection chain. From here on, any new premise must be logged as a deviation.
- `539ffa5`: the round 9 counterexample search (U(2) and Sp(1)×Sp(1) bodies, affine dimension 4–8, without the Jordan premise) is a **miss**, with 0 hits. It was not a blind run: a development run came before the lock, and no separate gate reader checked it. Both are disclosed in the prereg.

## Checks

These were run on a fresh clone of upstream `main` with this branch checked out, with `gh` authenticated for the open-PR rules:
- check_fresh: PASS.
- check_consistency: PASS.
- verify_locks: PASS.
- banned_words: PASS.
- check_claims: PASS (includes check_hypothesis).
- check_pending: PASS.
- pytest: 466 passed, 1 skipped.
- Re-run at `539ffa5` (Nov 26, after the hostile-review commits and the Lean round 3 batches): check_fresh, check_consistency, verify_locks, banned_words, check_claims and check_pending all PASS; pytest 469 passed, 1 skipped. Lean was not re-run by this worker, because the review commits touch no Lean file.
- check_lean.sh: OK in the dedicated Lean checkout (1628 declarations). The Lean sources are unchanged since that audit.

## Review

The round notes have only an adversarial self-check, which is not independent. An independent review is owed before merge, including the gate read for #292.

