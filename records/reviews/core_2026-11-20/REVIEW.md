# Independent hostile review: GTAO one-page core draft

Reviewer: separate executor, did not write `CORE.md`, `KEYSTONE_NOTE.md`, `PLAN.md`, or `OPEN_WORK.md`.
Friday 20 November 2026, about 4:26 PM ET (America/New_York).
Fresh clone of https://github.com/Chad-Mitchell/theory-of-adaptive-organization at `/workspace/rev-core`, `origin/main` = `b12af70` (PR #117). PR #116 is still open at `bc6e9c5` (confirm READY against main `1998a2d`; not merged). Compute at nice 19. Nothing was edited, pushed, or merged.

Drafts reviewed: `/workspace/gtao-core/CORE.md`, `core/KEYSTONE_NOTE.md`, `core/keystone_checks/rhythm_counterexample.py`, `PLAN.md`, `OPEN_WORK.md`.

## Verdict: READY-WITH-FIXES (2 blockers, both in the text)

The page does what it set out to do: one definition, one principle, the hypothesis sentence once, a scoped keystone, and the strands hung off J at roughly the strength the merged record earns. The two-oscillator counterexample is real. I reproduced it with my own multi-start optimizer and an independent Lyapunov MSE; at R = 3 the argmin is K* = 3 and N60's increment formula returns 2. I did not prove convexity of ε_K in Model S, and I did not find a Model S counterexample, including on the draft's tightest adversarial world (ε₂/ε₁ ≈ 0.461 < 0.5). Wording rules are clean. The plan is mostly safe.

Two claims on the core page are stronger than the record, and one of them reopens a closed review blocker. Fix both and re-confirm before a CORE PR merges.

## Blockers

**B1. The kill-rule sentence on the core page reopens PR #117's upper-bound excuse.**
`CORE.md:26`, `:58`.

#117's confirm review (`/workspace/rev117/REVIEW.md`) is **READY**. Merged CT41 is precise: a non-move is consistent only if the post-change gap g < Δ_R(k_lo); a miss if g > max(static band, Δ_R(k_hi)); INDETERMINATE between; and if the predicted gap of a non-mover is ≤ Δ_R(k_hi), the move test is NOT A TEST. CORE says "unless the post-change gap lies inside a preregistered redesign band" and, in §6, "a non-move is a miss only outside that band." That is the wording #117 was blocked for: "a preregistered band" can be read as the band at k_hi, which widens the excuse in the theory's favour. The one-page core will be the sentence people quote. It has to be the lower-bound rule.

Suggested replacement for `:26` (drop the matching loose clause at `:58`, or make both identical):

> So is a design that does not move when its inputs change: a non-move is consistent only if the post-change gap is inside the redesign band at the *lower* bound of the class's preregistered redesign cost; a miss if the gap exceeds both the static band and the band at the upper bound; between those, INDETERMINATE; and if the predicted move is no larger than the upper band, the move test is NOT A TEST (CT41).

**B2. "The informal keystone still holds if a rhythm is paid for as a pair" is a rescue, not a demonstrated rule.**
`CORE.md:36`, `KEYSTONE_NOTE.md:47, :60`.

The increment formula's failure in 𝓜_LG with real first-order stores is correctly scoped (N60 is Model S only), and the worked example is correctly computed (see Keystone, below). What does not follow is that the informal slogan still holds once a rhythm "is paid for as a pair." A pair rule would predict even K* (0, 2, or 4). In the worked example the independently confirmed argmin is **K* = 3**. My best K = 4 design (E₄ ≈ 0.04329, Lyapunov 0.04329) stays well above the threshold that would make J₄ beat J₃ (E₄ would need to be < 0.03921). The fitted stores at K = 2, 3 and 4 are tight real clusters at one rate, not two conjugate-pair allocations, so the "first half of a pair doesn't pay" story is also a gloss.

"Counted by degree" as used in CT21/THEORY (a rhythm counts as two layers; it is not a finite set of real first-order stores) is already the right counting convention, and it is testable once a layer-counting rule is finalized (OPEN_WORK T15). Using that phrase to paper over a formula miss, without a block-count rule that actually recovers this K*, is a rescue.

Suggested replacement for the last two sentences of `CORE.md:36`:

> The count formula is not to be exported to 𝓜_LG with real first-order stores. Whether a conjugate-pair (degree-2) design class restores a block-count rule is open; this example's argmin is 3, not 2 or 4, so "paid for as a pair" does not recover K* here. The formula as written also cannot return the K* = 0 that CT21 allows when stakes are small.

## Should-fix

1. **Stale #117 confirmation.** `CORE.md:58` ("review fixes await confirmation"), `PLAN.md:93`, `OPEN_WORK.md` W4 ("DONE (confirmation still open)"). The confirm is READY and #117 is merged as `b12af70`. Delete the leftover.

2. **Internal contradiction on K* = 0.** `CORE.md:34` "One real scale needs one layer, even a self-similar random walk" vs `:36` "the K* = 0 that L1 allows." CT21 is the right citation: one real pole ⇒ K* ∈ {0, 1}. LAYERS.md's Theorem L1 says "K* = 1 for every w and h," which is the overstatement. Cite CT21, say "at most one layer," and keep the random-walk point (a Brownian spectrum still needs only {0, 1}, so "scale-free ⇒ many layers" is false at α = 2).

3. **"Fast scales go local, slow ones shared" cites the wrong IDs and drops its premise.** `CORE.md:46` points at CT14, CT16, CT35, CT36. The statement in the repo is `figures/face_placements.md:98`: a shared layer's worth falls as e^{−2ℓ/τ}, so *at equal read quality and with shared upkeep measured in local layers*, fast scales go local and slow ones shared — attributed there to CT28 and CT34 (nesting), and driven by latency. Without ℓ the mechanism is not in those four theorems. Add the latency premise and the right IDs, or drop the slogan.

4. **N58–N63 are not on current main.** The header is honest that #116 is unmerged. A CORE PR that cites them must wait for #116, and #116 does **not** merge cleanly onto `b12af70` (`git merge-tree` conflicts in `README.md`, `STATUS.md`, `measurement/CLAIM_MAP_v2.md`, `reference/CHANGELOG.md`). The confirm was against `1998a2d`. `PLAN.md:94` should say: rebase onto `b12af70`, take CLAIM_MAP v2.68, then merge; it is not a fast-forward.

5. **KEYSTONE_NOTE overstates its own optimizer.** `:19` and `convexity_wide.py`'s header claim the #116 guarded inversion. The copy of `stores.py` in `core/keystone_checks/` is the *pre-fix* raw `solve`/`lstsq` (and `convexity_targeted.py` imports it; `targeted.out` has overflow / invalid-divide warnings). `rhythm_counterexample.py` has the 2% separation and a re-evaluated MSE, but not the Jacobi-scaled pseudo-inverse. The rhythm numbers still stand under the guarded inversion and under Lyapunov (below). The 120-world "0 violations" search is a weaker check than the note says. Use the #116 `stores.py` (or an equivalent guarded inversion) and rerun, or say plainly that the 120 used the older solver.

6. **Update the adversarial result.** `KEYSTONE_NOTE.md:23` says the climb was still running. `adversarial.out` is finished: max ε₂/ε₁ = 0.4625, still below 0.5. I re-optimized that world independently and got 0.461. Worth recording as the closest approach, not a violation.

7. **PLAN §3 row arithmetic is wrong.** `PLAN.md:66`: "CT1–CT43, CL1–CL21, CX1–CX10. That is 59 rows today, plus CT37–CT40 … and CT41–CT43 …" CT1–CT43 already includes CT37–CT43. Recount after excluding aliases, and don't add the same rows twice.

8. **OPEN_WORK stale bits and a missing section.** W5 still says "commit with W4" (W4 has merged; the scan should ride with hygiene v2.70, as `PLAN.md:101` already says). H1 says "after W1 merges." H9 says "only `v2.6-evo`, `v2.7-robust` are live" (robustness and dynamics are merged; live are `v2.6-evo` and `v2.8-htindex`). `PLAN.md:109` tells the owner to list branches in `OPEN_WORK.md` §5; there is no §5 (H9 is in §2). The 62 not-DONE queue items are not absorbed yet; that is acknowledged as H6/C6, but the page's own rule ("anything in flight that is not on this page is a bug in this page") is not met until the freeze happens. The v2.4-delta review still listed under STATUS "Next" is only implicit in T16.

9. **Traceability nits on the core page.**
   - `CORE.md:50` "Gate (#113)" is not a CLAIM_MAP id. Cite THEORY §3 / FRAMEWORK §9 (P23 is the GB instance of the gate, not the gate).
   - `CORE.md:49` bundles "a missing cost kills the theory" under CT23. That kill is J16 / the closed-list rule, not local regret.
   - PLAN §0 says every sentence on CORE names a row ID or a file. §1 and most of §2 do not. Either relax the plan or add the pointers (definition → the master-equation statement / J16's booking; principle → THEORY §3).
   - N58's 1.0 vs 2.0 distinction is dropped in `CORE.md:56`. Acceptable compression if "under head/tail breaks 1.0" is added in one clause.
   - Gerrard & Tsanakas 2011 is attached to CT38 at `:54`; the map books them mainly on CL18 (prediction-interval buffer). ROBUSTNESS.md also cites them as known prescription near CT38, so this is a nit, not a mis-credit.

10. **L1 vs the formula's K* = 0 hole** (`KEYSTONE_NOTE.md:30`) is a real limitation of N60 as written. Keep it, but cite CT21 rather than L1.

## (1) Traceability and labels

Checked against `measurement/CLAIM_MAP_v2.md` on `b12af70` and, for N58–N63, against `origin/v2.8-htindex` at `bc6e9c5`.

| Draft claim | Map label | Fit? |
|---|---|---|
| Hypothesis sentence (`:24`) | J3, the locked wording | Yes; appears once |
| CT20, CT33, ruin-slack spend, reads can replace layers (`:42`) | both PROVED (in-model); slack qualifier is required and is present | Yes |
| CT21 / L1–L3 (`:34`, `:43`) | PROVED (in-model); "counted by degree" is already in CT21 | Yes, except the K* = 0 slip (S2) |
| N60 (`:44`) | **PROVED (in-model) given convexity (numerical)** — #116 only | Yes, if #116 has merged; not on main today (S4) |
| CT22, CT25 (`:45`) | both PROVED (in-model) | Yes |
| CT14, CT16, CT35, CT36 (`:46`) | all PROVED (in-model) | First and third sentences yes; "fast/slow" no (S3) |
| CT37–CT40, CX7 (`:47`, `:54`) | CT37–40 PROVED (in-model); CX7 OPEN | Yes |
| CT41–CT43, CL19, CT42, CT43 (`:48`, `:58`) | CT41–43 PROVED (in-model); CL19 PRIOR ART (Dixit) | Labels yes; CT41 wording no (B1) |
| CT23 (`:49`) | PROVED (in-model), second-order regret | Regret yes; "missing cost" is J16 (S9) |
| N46 withdrawn (`:55`) | WITHDRAWN (as framing) | Yes |
| N58, N59 PROVED; N61 MATH-CORRECTED (`:56`) | those labels on #116 | Yes, and "beats a pole count only at R ≤ 10³" matches N61 (tie at 10⁴) |
| N63 OPEN, first numbers withdrawn (`:57`) | OPEN; arm D and D2 as in the #116 confirm | Yes, and honest |
| EVO1 interim (`:59`) | not yet on the map; #114 draft | Faithful to `/workspace/gtao-evo/tests/EVO1/RESULTS_EVO.md`: PC, W1, W2 PASSED; W4 FAILED 3/8; W4b FAILED 8/8 by reachability valleys; one design per genome, so no bet-hedging test. W3 INVALID and S031/S07 pending are reasonably omitted on a one-page interim line. |

Scorecard (`:63`): honest. No system has been shown to qualify (P23: GB NOT QUALIFIED; E. coli not yet checked). The 30 NOT A TEST rows are 10 proxy-passed and 20 proxy-failed (18 "qualification not established" + 2 "not qualified"), which is how the map itself groups them. "Refereed at most once, by one bot family" and "no human expert" match the record. "Untested, not refuted" is the right headline.

Stale bits other than #117 confirmation: the CORE header's versions (#115 = v2.66, #117 = v2.67, #116 next as v2.68) are right for current main.

## (2) Keystone — independent checks

**Setup.** I did not import the draft's optimizer. Code: `/workspace/rev-core-work/indep_keystone.py`. Same world as `rhythm_counterexample.py` (wide-search seed 2, two lightly damped oscillators). MSE: the #116 guarded inversion, written out, plus a continuous Lyapunov check on a real state-space realization of C(t) = Re ∑ vⱼ e^{−aⱼ|t|}. Multi-start: informed grids around both oscillator moduli, Nelder–Mead, L-BFGS-B, and differential evolution. No `minimum.accumulate` on E_K.

**Yovits–Jackson E_∞** agrees to all reported digits: 0.03788281801526715.

**Two-oscillator results** (Lyapunov in parentheses):

| K | Draft E_K | Independent E_K (Lyapunov) | Stores (indep.) |
|---|---|---|---|
| 1 | 0.08051946 | 0.08051946 (0.08051946) | 2.85351 |
| 2 | 0.07373616 | 0.07373616 (0.07373616) | 1.45139, 1.48042 |
| 3 | 0.05183294 | 0.05183293 (0.05183296) | 0.63770, 0.65046, 0.66347 |
| 4 | 0.04324429 | 0.043287 (0.043290); I did not beat the draft | tight cluster near 0.38–0.42 |

The clustered rates look like a failed optimizer. They are not. Well-separated stores at the two oscillator frequencies are *worse* (E₂ ≈ 0.08–0.18). A 2+2 allocation, a 3+1 allocation, and local polishing all returned a tight real cluster, and Lyapunov agrees with the algebraic MSE at the 10⁻⁸–10⁻⁵ level. At R = 3:

J = (7.376, 7.839, **7.105**, 7.428), argmin **3**, N60 formula **2**, decrements (0.179, **0.578**, 0.226), not monotone.

To flip the argmin to 4, E₄ would have to fall below 0.03921 (almost to E_∞). Nothing I found comes close. The counterexample stands. N60 as scoped to Model S is not refuted by it.

**Model S, no counterexample in random worlds.** I did not complete a fresh 40-world random scan in this pass (the long job was still on the rhythm K = 4 when the K = 4 grid finished). What I did: re-optimized the draft's closest adversarial world (τ = 1, 2.61, 4.06×10⁷; max reported ε₂/ε₁ = 0.4625) with the guarded solver, and got ε₂/ε₁ = 0.461, still convex. The draft's 120 + 24 real-pole worlds and the #116 review's 39/40 (the 40th was the optimizer bug) plus `face_collapse_v23.py` V2 (300 worlds, 1.000 within tolerance; rerun in the #116 confirm) all point the same way. The claim is supported, with S5's caveat on the 120-world solver. I found no Model S counterexample.

**Convexity proof.** I did not produce one, and I agree Das & Kempe 2008 (doi 10.1145/1374376.1374384) is a different problem (subset selection, not filter degree). The plausible argument is that, for a sum of real OU modes, stores act as substitutes and the decrements can be ordered by mode value, hence are nonincreasing. Shared observation couples the modes, so that is not a proof. Closest numerical approach remains ε₂/ε₁ ≈ 0.46. Status stands: numerical only, unproved, no counterexample found.

**"Counted by degree."** As a *counting convention* already in CT21, it is correct and is intended to be testable (T15). As a *generalization of N60's increment formula* that makes the informal keystone hold for rhythms, it is not yet a rule, and the worked example's K* = 3 is evidence against the "paid for as a pair" version. See B2.

## (3) Integration of the strands

Against the merged docs (and #116 at `bc6e9c5` for the fractal / ht / records strands), the page is mostly faithful and is genuinely organized as consequences of J plus the ruin cap, not as a pile of side notes.

- **Robustness / antifragility.** CT37 copies, CT38 reserve under ambiguity, CT39 zero margin when ruin binds, CT40 antifragility with redesign-per-regime and not without, CX7 open: all match `theory/ROBUSTNESS.md` and the v2.66 map. Prior art (Kettelle, Taleb & Douady) is credited; Gerrard is slightly mis-attached (S9).
- **Fractal change as spectrum.** "Enters only as the measured spectrum"; "fractal, period" withdrawn (N46); slope × stakes as the reading of N60/L3. Good, and the right demotion.
- **Head/tail breaks.** ht = 1 on Gaussian records, ln n on heavy tails, valid for heavy-tailed value data, does not count layers, plug-in beats a raw pole count only at R ≤ 10³. Matches N58–N61 after the #116 confirm. Jiang 2013, 2016, 2019 are in `HT_INDEX.md`.
- **Records as agents (N63).** Open, no support; first numbers withdrawn as pseudo-replicated; redo: a record reports its world, an I/O fit reads a design whether or not it is optimized. Matches the confirm review of arm D2. Good.
- **Dynamics.** J_R, Dixit band (CL19, correctly PRIOR ART), lineage bet-hedging (CT42, Cohen), J as time average (CT43). Faithful except B1 and the stale confirmation flag. The Bode overreach is correctly left off the one page (it is an overreach, not a positive theorem).
- **EVO1.** Interim, correctly flagged, and the pass/fail split is the reachability diagnosis in RESULTS_EVO.md, not a prereg patch. The link to complements / valleys (KEYSTONE_NOTE :49, CT36, CL13) is fair as a diagnosis, not as a new theorem.

The keystone is the right spine. The only synthesis overreach is B2.

## (4) Wording rules

- **"Law"** appears in CORE only in the hypothesis sentence at `:24` ("The law of adaptive organization (hypothesis): …"). OPEN_WORK C3 discusses the pending "Proposed law" label, which is appropriate for a work list. No other use.
- **No "theory of everything."**
- **"Cost" throughout; no "bill," no joules.**
- **Scorecard** is honest (see §1).
- Call it a theory: yes.

## (5) PLAN.md and OPEN_WORK.md

**Safety.** The plan is conservative in the ways that matter: `git mv` only, no branch or file deletion, Chad's yes for the QUEUE freeze (C6) and for any deletion (H9), locked preregs stay in one folder with their results and DEVIATIONS so relative `LOCK.txt` / `SHA256SUMS` (basename hashes, e.g. under `tests/` and `prereg/`) remain valid, frozen scripts are not edited, and a `PATHS.md` prefix table is supposed to keep old paths resolvable. Checker changes (maintained-file list, one version line, tally across the split map, new R9/R10, `FROZEN` includes `archive/`) are the right list, and the acceptance bar (pytest, `RESULT: PASS`, re-verify SHA256SUMS at the new path, link check) is the right bar. Splitting `CLAIM_MAP_v2.md` into core + history with unchanged row text is the riskiest move; doing it in the v3.0 "pure move" PR, with the checker reading both files, is acceptable if the diff is audited mechanically.

**Merge order** is sensible: #115 (done) → #117 (done) → #116 → #114 → hygiene → CORE → reorganization v3.0. Two corrections: (i) rebase #116 onto `b12af70` first (S4); (ii) drop "review fixes await confirmation" on #117 (S1). EVO1 IDs starting at N64, and not patching the EVO1 prereg with the reachability diagnosis, are right.

**OPEN_WORK completeness vs the repo.** Live work is covered: #114 (W2, W10), #116 (W3), merged #113/#115/#117, the core draft (W7–W9), hygiene H1–H9, field/math opens T1–T17 (including the 78 other OPEN rows as T17), and Chad-gated outside acts C1–C6. Open PRs on the repo are only #114 and #116. Gaps are staleness (S8) and the still-unabsorbed queue, not a silent dropped front. After the two blockers and the stale flags are fixed, this can be the one open list.

## Checks that pass (short)

- Hypothesis sentence exact and unique on the core page.
- Master equation, ruin as a cap not a term, Landauer as a floor, "one currency," operational "strongly selected" (ε = 10/(σ N_e), THEORY.md:48), and "predicts only through price-free structure or independently measured prices" all match THEORY §1–§3.
- CT20/CT33's ruin-slack qualifier is kept. CT40's "with redesign per regime … not with one fixed design" is kept.
- Records-as-agents and the ht-index demotion are not oversold.
- No locked prereg is touched by these drafts (they are beside the repo, unpushed).
- PLAN does not propose deleting branches or rewriting verdicts.

