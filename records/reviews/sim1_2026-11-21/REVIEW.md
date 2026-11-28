# Independent hostile review: PR #125 (T28 SIM-1 rehearsal test)

**Reviewer:** independent (wrote none of the PR, MODEL.md, PILOT.md, PREREG.md, predictions, runner, library, official run, RESULTS, OPEN_WORK edits, math_checks, or the SIM-1 package).
**Date:** Saturday 21 November 2026, started 12:59 AM ET, finished 1:10 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/125
**Clone:** fresh `/tmp/gtao-rev125` at head `41d79060299d3a1c6d5d1315db0c8ecf16046149`, base `17277348dd0f3492489400fca3c76c8e9bd46e43` (merge-base equals base). Current `origin/main` is `d63ac233b3e7fb3622732303dae2adb2200615ed` (PR #124, after this base). Clean tree at review start. Nothing pushed or merged. `/workspace/looper` was not touched. Compute at nice 19. Author workdir `/workspace/gtao-sim1/core/sim1_2026-11-21/` was read only as corroboration of timestamps; every packaged file compared there is byte-identical to this head.

**Verdict: READY-WITH-FIXES**

The official gates recompute exactly from the locked predictions, the stored outputs, and an independent re-run of the committed runner. The prereg, predictions, runner, and library were SHA-256 locked at 12:54:44 AM EST, before any official world was evaluated (official JSON/log written 12:55:00 AM EST; 12.0 s). Official seeds 20261122000–02 do not collide with prior test sets. P1–P3 pass 3/3 as exact discrete checks of theorems on this model; P4 passes 3/3 numerically. The official verdict is PASS and must stand as an in-model result; no rescue is registered, and none is needed. CORE.md and the law-of-adaptive-organization sentence are unchanged. The SIM-1 hypothesis sentence is unchanged except for a pointer to this run. Checkers pass; `pytest tools/` is 127 passed. None of the issues below flip a gate or the PASSED verdict. They should be fixed before merge, without touching the locked prereg, the predictions file, the runner, the library, or the official numbers.

---

## What was checked

- Fresh clone at the stated head/base; diff `1727734..41d7906` (one commit, 19 files). Package `core/sim1_2026-11-21/` plus the `OPEN_WORK.md` and `tools/test_sim1_checks.py` diffs.
- Mergeability against current `origin/main` `d63ac23`: GitHub `mergeable: true`, `rebaseable: true`, `mergeable_state: clean`. A local `git merge --no-commit` of `origin/main` into the head completed with no conflicts. `#124` does not touch this package; it also did not edit `OPEN_WORK.md`, so a clean merge will still leave T1 and the as-of line stale (S3).
- SHA-256 of `PREREG.md`, `predictions.json`, `run_sim1.py`, and `sim1_lib.py` against `LOCK.txt`, the four sidecar files, `run_sim1.json`, and `RESULTS.md`. Author-workdir birth/mtimes used only as corroboration of lock/start order.
- Independent regeneration of the three official worlds from the locked generator; recomputation of every P1–P3 ladder and threshold, joint CT33 diagnostics, exact Boltzmann, and P4 occupation statistics from the stored occupation vectors (no official number moved).
- Independent re-run of committed `run_sim1.py` at nice 19 in a copy of the tree (12.05 s): `run_sim1.json` matches the official file exactly except the wall-clock `seconds` field. Official artifacts in the review clone were not overwritten.
- Seed non-collision of official, chain, and pilot blocks against S5 rng 1000–1119, convexity_search 0–119, wide 5000–5119, named seeds 20261120 / 2026112020, T27 official 2026112100–2115, and T27 chain block 20261121500–21999, plus a repo-wide literal scan. Intra-test overlap is a separate finding (S2).
- Math: Topkis / increasing differences of −J; relation to CT4, CT10, CT12, CT20, CT22, CT33; the error-production assumptions; the ruin-slack booking; whether P1–P3 can fail; P4 bar slack against exact Boltzmann and the official occupation.
- Tightened-box pilots 20261122800–19 and all 16 corners of the locked box, plus the disclosed untightened I0=1 corner. First-scan `pilot_explore.json` checked against PILOT.md.
- Prior art: Daw, Niv & Dayan 2005 and Keramati, Dezfouli & Piray 2011 re-queried on the Crossref API this review; Topkis 1978 and Sutton 1990 also resolved. The T28 package cites none of the RL / mental-simulation papers.
- `python3 tools/check_open_work.py`; `python3 tools/check_consistency.py`; `python3 -m pytest tools/ -q`.
- Wording: in-model only, law not proved, CORE claims, hypothesis sentence, rediscovery of CT20/CT33, ruin-binding caveat.

---

## Integrity

- `PREREG.md` SHA-256 `f24d54271875a326947c7a17fc6114a0d8b0a7864c5ff17dc0eca2300260de8c`. Matches LOCK.txt, PREREG.sha256, run_sim1.json, RESULTS.md, and a re-hash of the file on disk. Bytes 11540, as recorded.
- `predictions.json` SHA-256 `40c14cb4f991bee864b8bf74ab7f4583766cfb2ccab6aaf712deb692d2f33b09`. Matches LOCK.txt, PREDICTIONS.sha256, run_sim1.json, RESULTS.md, and a re-hash. Bytes 3876, as recorded.
- `run_sim1.py` SHA-256 `9f3f41700aee9335f5f50f6612712fb87dee95b7a56fc732b418df917641181f`. Matches LOCK.txt, RUN_SIM1.sha256, run_sim1.json, RESULTS.md, and a re-hash. Bytes 11715, as recorded.
- `sim1_lib.py` SHA-256 `2f20672665503aa6b0d48ef907ae3f24edded5ac935d191474b42ee383846559`. Matches LOCK.txt, SIM1_LIB.sha256, run_sim1.json, RESULTS.md, and a re-hash. Bytes 15962, as recorded.
- The T27 standing rule was followed: runner and library were hash-locked with the prereg and the predictions. The official runner printed `LOCK ok` before evaluating any official world. Locked-file mtimes in the author workdir are earlier than the lock and unchanged after it. There is no mid-run rewrite of the kind that marked T27.

Author-workdir file order, byte-identical to this head (America/New_York):

- `sim1_lib.py` last write 12:51:31 AM EST (birth 12:47:43 AM EST)
- `run_sim1.py` birth/mtime 12:52:15 AM EST
- `predictions.json` birth/mtime 12:52:30 AM EST
- `MODEL.md` mtime 12:52:55 AM EST (not hash-locked; before lock)
- `PREREG.md` birth/mtime 12:53:38 AM EST
- `PILOT.md` mtime 12:53:55 AM EST (not hash-locked; before lock)
- `math_checks.py` mtime 12:54:25 AM EST (not hash-locked; before lock)
- `LOCK.txt`, PREREG.sha256, PREDICTIONS.sha256, RUN_SIM1.sha256, SIM1_LIB.sha256 birth/mtime 12:54:44 AM EST
- `run_sim1.json` / `run_sim1.log` birth/mtime 12:55:00 AM EST (official finish; 11.996 s; RESULTS.md’s “12:55:09 AM EST” is nine seconds later than the artifact timestamp, a nit)
- `RESULTS.md` birth/mtime 12:55:41 AM EST
- Commit `41d7906` at 12:58:25 AM EST

The lock is genuinely before any official world. Pre-lock design work used only pilot seeds `20261122800..20261122819` and closed-form box-corner probes. Official candidate seeds were not evaluated before lock. Criteria in `predictions.json` match PREREG.md §5.

### T27 lesson on gates, shown before lock

Exact / analytic gate values were computed on the published pilots *before* lock, in three places:

1. `pilot_explore.json` (first, untightened-I0 scan, written 12:48:30 AM EST): P1–P3 held 80/80 K-rows; at provisional P4 stake w=5, two of 20 pilots had joint m\* = 0 (seeds 20261122806 and 20261122807); at w=20, all 20 had joint m\* in {4,…,14}. The discarded mixing probe at w=5, β ∈ {8, 10, 12} is in that JSON (one joint-mode miss; mass at the argmin as low as ~5–10%), which is why the official P4 cell is w=20, β=40, and why official clauses use the marginal on m plus a mean tolerance.
2. PILOT.md (12:53:55 AM EST, before lock) records the I0 tightening, the 16-corner probe, the tightened-box exact Boltzmann max 0.767, and the locked-count mixing probe (TV ≤ 0.054, empirical |m̄−m\*| ≤ 0.752 on five first-box pilots). The locked-count mixing probe is disclosed in prose only; it is not in the JSON. This review independently recomputed the tightened-box exact gates: P1–P3 20/20, joint m\* in {4,…,14}, exact |E[m]−m\*| max **0.766998** (claimed 0.767). All 16 locked-box corners have joint m\* ≥ 3 at w=20 and satisfy every P2 clause at every K. The disclosed untightened corner (min e_base, max γ, min φ, I0=1) has joint (K\*,m\*) = (3, 0) at w=20, which is why I0 was tightened.
3. `math_checks.py` (12:54:25 AM EST, before lock) re-runs the tightened-box exact P1–P3 and exact-Boltzmann P4 screens, increasing-difference identities, CT33 diagnostics, seed hygiene against *prior* sets, and lock-hash checks. `tools/test_sim1_checks.py` wraps that script.

This is the right response to T27’s ill-posed P3 bar. The I0 tightening and the move of the P4 cell from w=5 to w=20 happened before lock, and are disclosed.

`core/bridge_2026-11-21/bridge_lib.py` is imported unmodified (SHA-256 `4e779b3dd4754dfa29a4ef74836a8986837f31a92c55601ae32579911e4b8fd2`, identical to base `1727734`).

Official rng seeds 20261122000, 20261122001, 20261122002 (candidates through 20261122015) do not collide with the locked *prior-set* exclusion list, and a broader scan did not find those literals used as generator seeds elsewhere. See S2 for an intra-test overlap with the pilot block.

---

## Official gates (recomputed from stored data, and by re-running committed code)

Worlds regenerate from the locked generator. Every P1–P3 ladder and every W_th value in `run_sim1.json` recomputes exactly. Unique joint argmin, 2 ≤ m\* < 40, graph connectivity, and exact-Boltzmann P4 screens all recompute. Mixing SANITY holds on every official cell (TV 0.0266–0.0422, bar 0.20). An independent nice-19 re-run of committed `run_sim1.py` reproduced `run_sim1.json` exactly except `seconds`.

| Gate | Criterion | Independent result | Verdict |
|---|---|---|---|
| P1 | at each locked K ∈ {0,1,2,3}, least discrete m\*(w) nondecreasing on the W-ladder, and m\*(λ) at w=1 nondecreasing on the λ-ladder; all three official worlds | 3/3 worlds, 24/24 K-ladder clauses. Example, world 0 at K=0: m\*(w) = 0,0,0,0,0,3,5,9,14,21 | **PASS** |
| P2 | at each locked K, m\*(0.02)=0, m\*(20)≥1, and W_th(K) strictly between those rungs | 3/3 worlds, 36/36 clauses. W_th at K=0,1,2,3: world 0: 0.711017, 1.910108, 3.109199, 4.308290; world 1: 0.769131, 1.271165, 1.773199, 2.275233; world 2: 0.329835, 0.502539, 0.675243, 0.847947. RESULTS.md rounding is correct (world 2’s last rung 0.848 from 0.847947) | **PASS** |
| P3 | at each locked K, at w=5, λ=0, least discrete m\*(c) nonincreasing on the c-ladder | 3/3 worlds, 12/12 K-rows. World 0 at K=0: m\*(c)=23,16,9,6,3,1,0 as claimed | **PASS** |
| P4 | pooled Moran occupation, β=40: marginal mode on m equals unique joint m\*, and \|m̄−m\*\| ≤ 1.5 | 3/3. World 0: (K\*,m\*)=(3,7), TV=0.040174, emp m̄=7.328640 (exact 7.206241), \|m̄−m\*|=0.328640, mode=7. World 1: (3,8), TV=0.042182, emp 8.258406 (exact 8.377779), err=0.258406, mode=8. World 2: (3,11), TV=0.026614, emp 11.880869 (exact 11.783333), err=0.880869, mode=11 | **PASS** |
| Overall | PASS iff three official-valid worlds and P1∧P2∧P3∧P4 on every one | First three candidates official-valid; none rejected. All four gates pass | **PASS** |

Every RESULTS.md figure checked against `run_sim1.json` agrees, including the diagnostic that joint (K\*,m\*) had nondecreasing m, nondecreasing spend, and nonincreasing error on these three official W-ladders. Joint monotone m was correctly *not* a gate.

No gate was changed after seeing the data. The PASSED verdict stands as the official in-model record of this prereg.

### P4 bars

The locked bars are TV ≤ 0.20 (validity, not a prediction) and \|m̄−m\*\| ≤ 1.5 (official clause). They are conservative, but not empty.

- Exact Boltzmann \|E[m]−m\*\| on the 20 tightened-box pilots has maximum 0.766998, as claimed. Official exact values are 0.206, 0.378, and **0.783** (world 2 is already slightly above the pilot max). Official empirical errors are 0.329, 0.258, and **0.881**.
- A bar of 1.0 would still have passed all three official worlds. A bar of 0.80 would have failed world 2 (0.881). So 1.5 is roughly twice the pre-lock exact maximum, with room that world 2 actually used.
- Official-valid already requires the *exact* Boltzmann weights to meet both P4 clauses, including the 1.5 mean bar, and TV ≤ 0.20. Observed TVs (0.027–0.042 official; 0.025–0.054 on the disclosed locked-count probe) sit far under 0.20. Once a world passes those screens, official P4 is a finite-sample check that Moran occupation stays close to an already-passing π, not an independent test that evolution finds m\*. That is legitimate, and it is disclosed (PREREG §3.4 and §5.4; RESULTS.md). It is also why a 3/3 P4 pass is a weak numerical result. It does not make the pass a cheat, and it is not a reason to tighten a locked bar after the fact.

---

## The hardest question: do P1–P3 hold by construction?

Short answer: **P1 and P3 are theorems on this model and cannot fail on any official world unless the implementation is wrong. P2 is not implied by monotonicity alone, but the locked price/world box was designed, and pre-checked on every corner and every published pilot, so that it would hold. Official P1–P3 are implementation-and-box checks, not stochastic evidence. The package mostly says this; a reader of “PASS 3/3” could still miss it (S4).**

### What is assumed

Stated in MODEL.md, PREREG §1, and `sim1_lib.py`, and reasonable as a *minimal mechanism*, not as a derived production function:

- Simulation reduces real-trial error toward a fidelity floor, with diminishing returns: \(E(K,m)=e_0(K)\bigl(1-\varphi+\varphi/(1+\varphi m)\bigr)\), \(e_0(K)=e_{\mathrm{base}}/(1+\gamma K)\), \(\varphi\in(0.35,0.80]\). This form is a convenient schematic (error falls in m; layers shrink the residual, not \(\varphi\)). It is not derived from a named generative model of rehearsal. For \(\varphi>0\) and \(e_0>0\), \(E\) is strictly decreasing in m.
- Model memory is a fixed cost \(\kappa I_0\), paid iff \(m\ge 1\), booked as the existing \(\kappa I_{\mathrm{mem}}\) term. Rollout count does not enlarge the model; fidelity is not chosen jointly with I.
- Compute is linear, \(cm\), booked in \(A(\mathcal D)\).
- Ruin enters only as additive exposure \(\lambda\chi E\). The Lundberg cap is kept slack by construction. When the cap binds, CT33 (and CT20(ii)) can fail; this is stated in MODEL.md, the library docstring, PREREG, and RESULTS.md, and is the right caveat (CT22). \(\lambda\chi E\) is a stand-in for L, not the constraint.

Increasing differences are **not** assumed as a primitive. They are derived from those bookings: for m′ > m,

\[
J(m',w)-J(m,w)=\kappa\Delta I+c(m'-m)+w\bigl(E(m')-E(m)\bigr),
\]

and the w-difference of that increment is \((w'-w)(E(m')-E(m))\le 0\). So −J has increasing differences in (m, w) and, because W = w + λχ, in (m, λ). The same increment is nondecreasing in c, so −J has increasing differences in (m, −c). The fixed cost \(\kappa I_0\) does not depend on w or c and does not break the argument, including at the 0-versus-1 margin.

### What is a theorem from those assumptions

- **P1 / P3 (Topkis).** At fixed K, with the cap slack, the least and greatest selections of m\* are nondecreasing in w and in λ, and nonincreasing in c (Topkis 1978; the same argument as CT10 and as CT20(ii) for a single instrument). This holds on the whole discrete grid, not only inside the locked box. This review checked increasing differences on the official worlds and ran 200 draws from a *wider* box (200 × 4 K-rows): P1 failures 0, P3 failures 0. At φ = 0, m\* is identically 0, which still satisfies P1 and P3 and fails P2. The official λ clause is not an independent prediction: with χ = 1, raising λ at w = 1 is the same comparative static as raising the effective stake W, on a slightly different ladder.
- **P2 (extensive margin).** Monotonicity alone does not put a crossing between W_LOW and W_HIGH. P2 is the CT4-style claim that the first model and the first rollout must pay, *and* that the locked ladders sit on both sides of that threshold at every locked K. The true discrete threshold is weakly larger than the FOC value \(W=c/(e_0\varphi^2)\) because of \(\kappa I_0\); official W_th is a bisection on the discrete grid (80 steps on [0, 10^6], effectively exact). This *can* fail: 151 of 800 wider-box K-rows failed P2. Inside the locked box it did not fail, on any of the 16 corners or the 20 pilots, and that was known before lock. Official-valid further requires joint m\* ∈ [2, 40) at the P4 cell.
- **Not theorems, and correctly not gated:** joint m\* once K is also chosen (K and m are substitutes; CT20’s referee example / B.9 is the ancestor). The continuous interior formula m_cont is a diagnostic only. The Lundberg-binding regime is out of scope.
- **P4** is numerical, not a theorem about Moran trajectories. Under m = −αJ, equal edge clocks, and the locked graph (including the pre-locked adopt/drop edges, justified by the fixed-cost valley in m), the stationary law is still π ∝ e^{−βJ}. Official P4 simulates that process; it does not sample π.

So P1 and P3 could not have failed on official data except by a coding error. P2 could have failed only if a drawn world left the pre-checked box property, which the corner probe and official-valid screen were built to prevent. That does not make the exact discrete checks worthless — they are the right way to confirm that the implemented J is the stated J — and the package already labels them “analytic theorem, exact discrete check.” It does mean the 3/3 official pass should not be read as confirmation that “systems simulate more when stakes rise,” beyond the theorem already implied by the mechanism.

---

## Proof correctness, CT10 / CT33, and prior art

The Topkis argument is correct, including the use of the least discrete argmin (row-major packing matches lexicographic least (K, m); least and greatest selections are both monotone). CT33 is correctly applied as a *diagnostic* on total spend and error, with the cap-slack hypothesis stated, and was checked on the official worlds and the published pilots (spend nondecreasing, E nonincreasing). The package does not rediscover CT20 or CT33, and it does not claim joint monotone m.

The closest in-repo ancestor of P1 and P3 is **CT10** (G4: with J(f; w) = c·f + w·A(λ/f), the minimizing check frequency is nondecreasing in w — the same decreasing-differences proof), together with CT12’s read-rate rule and the single-instrument clause of CT20(ii). The package cites CT20 / CT33 / CT4 / CT22 and “Topkis,” and it correctly holds K fixed “in the same spirit as CT20(ii).” It never names CT10. That is a citation miss, not a rediscovery claim. It should be fixed in MODEL.md (S1).

The mechanism is a legitimate booking of rehearsal inside the existing terms of J, not a new term, and CORE.md is untouched. What is new is the parametric rollout model and the preregistered test of its comparative statics.

**Prior art outside the repo is not credited, and it is relevant (S1).** The hypothesis that a system should “simulate more when stakes or ruin risk are high and an internal model is cheap, and simulate zero when stakes are near the model’s cost” is the same qualitative arbitration as uncertainty-based / value-of-information competition between a costly model-based (goal-directed) controller and a cheap model-free (habitual) one. Crossref, this review:

- Daw, Niv & Dayan 2005, “Uncertainty-based competition between prefrontal and dorsolateral striatal systems for behavioral control,” *Nature Neuroscience*, https://doi.org/10.1038/nn1560
- Keramati, Dezfouli & Piray 2011, “Speed/Accuracy Trade-Off between the Habitual and the Goal-Directed Processes,” *PLoS Computational Biology*, https://doi.org/10.1371/journal.pcbi.1002055

Sutton 1990, “Integrated Architectures for Learning, Planning, and Reacting Based on Approximating Dynamic Programming,” https://doi.org/10.1016/b978-1-55860-141-3.50030-4 (Dyna; planning by simulated experience) is also on point as a mechanism, if not as the comparative-static result. Topkis 1978 is correctly the lattice paper, https://doi.org/10.1287/opre.26.2.305 (Operations Research 26:305). None of the RL / mental-simulation papers appears in the T28 package, nor in a new litmap entry. Given this repository’s prior-art standard, that is a should-fix, not a blocker: the package does not claim the qualitative idea as a discovery about nature, but “already inside J” still owes the credit.

---

## Overclaim, CORE, OPEN_WORK

- CORE.md, THEORY.md, STATUS.md, and CLAIM_MAP are not in the diff. The law sentence in CORE.md §3 is unchanged. The SIM-1 hypothesis text is unchanged except for adding that T28 has been run and passed in-model, and moving the gate to “needs reviewer (with T28).” That is the right status.
- RESULTS.md, MODEL.md, and PREREG.md stay inside “in-model,” “analytic / numerical,” “not a field test,” “nothing here is PROVED about nature.” The ruin-binding case and the joint-m substitute caveat are acknowledged. No wording claims the law is proved, or that T28 is evidence in the world.
- OPEN_WORK’s as-of line and the new T28 / updated SIM-1 rows correctly report an in-model PASS awaiting review, and they record the four lock hashes. Accuracy nits on that page are S3.

---

## Checkers and tests

- `python3 tools/check_open_work.py`: PASS (union missing from OPEN_WORK.md: 0).
- `python3 tools/check_consistency.py`: RESULT: PASS (0 FAILs; the usual soft length warnings on THEORY.md and README.md).
- `python3 -m pytest tools/ -q`: **127 passed** in 111 s. The as-of line’s “127 tests” matches this branch (base `1727734` had 126; this PR adds `tools/test_sim1_checks.py`). Current `main` (`d63ac23`) still has 126 before this merge.

`math_checks.py` itself exits ALL OK. One cosmetic lapse in `check_graph_connected`: an earlier `assert … or True` is a no-op, then a real adjacency check follows. Harmless.

---

## Issues (none flip a gate; fix before merge; do not touch locked files or official numbers)

### S1 — Credit the simulation / arbitration prior art, and name CT10

Add a short prior-art paragraph to MODEL.md (unlocked): Daw, Niv & Dayan 2005, DOI `10.1038/nn1560`; Keramati, Dezfouli & Piray 2011, DOI `10.1371/journal.pcbi.1002055`; and, as the in-repo ancestor of P1/P3, CT10 (and CT12 / CT20(ii)), not only CT20/CT33. Sutton 1990 (Dyna) is optional. Do not present the qualitative “simulate when stakes are high and the model is cheap” prediction as if it first appeared in this package. Do not edit the locked prereg.

### S2 — Official world-0 chain seeds collide with the pilot world seeds

CHAIN_SEED_BASE + 10·β + c with β=40 gives official world 0 the chain seeds **20261122800–20261122807**, which are exactly the first eight pilot *world* seeds. PILOT.md’s claim that “Pilot seeds do not collide with … the reserved official/chain blocks of this test” is false. `seed_collides` and `check_official_seeds_clean` only test prior-set lists; they never check intra-test disjointness of pilots and chains.

This is a hygiene miss, not a scoring miss. The integers are used for different RNGs (draw_world versus Moran jumps), official worlds are not the pilot worlds, and the official numbers are reproducible from the committed runner. Correct the PILOT.md sentence; record the overlap in an unlocked hygiene note if the page is touched. Future preregs should treat the test’s own pilot and chain blocks as reserved in the collision check.

### S3 — OPEN_WORK is stale in ways this PR already touched

This PR rewrote the as-of line and the SIM-1 / T28 rows, so the following should be cleaned up in the same file:

- W13 still says “needs reviewer (confirm of the fixes)” and “Branch `thermo-bridge-2026-11-21`, off `4398bbd`,” although the new as-of line itself says PR #122 merged as `1727734`.
- The as-of line attributes “127 tests” to `main` at `1727734`. That commit had 126 tests; 127 is this branch.
- Current `main` is now `d63ac23` (PR #124, E. coli qualification NOT ESTABLISHED). T1 still says the qualification check is “Not started.” `#124` did not update OPEN_WORK, so a clean merge of this PR will not fix T1 by itself. Refresh the as-of line and the T1 pointer when landing.

None of this is a merge conflict.

### S4 — One sentence so “PASS 3/3” is not read as a stochastic test of P1–P3

RESULTS.md already calls P1–P3 theorems and the official numbers an exact implementation check. Add one explicit sentence, there or in the T28 OPEN_WORK row, that official P1 and P3 could not have failed under the stated model (P2 was pre-verified on all 16 locked-box corners and the 20 published pilots), so the 3/3 is not independent empirical support for the comparative statics. Leave the official PASS in place. This is wording, not a re-score.

---

## Conclusion

The official in-model result is PASS, and that is correctly scored. Lock integrity, including the T27 runner-and-library rule and pre-lock exact gate checks, holds. The Topkis theorem is right; the ruin-binding and substitute caveats are right; CORE and the law sentence are untouched. P1–P3 are not a tautology in the cheap sense of “we assumed increasing differences,” but they are theorems, and the official 3/3 does not add empirical weight beyond the implementation check. P4 is an honest, somewhat soft numerical test after a validity screen that already requires exact π to pass the same bars. The fixes above are citation, seed-hygiene, OPEN_WORK accuracy, and wording. Fix them without touching locked files or official numbers, then this is ready to merge.
