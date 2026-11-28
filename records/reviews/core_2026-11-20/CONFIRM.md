# Confirm review: revised GTAO core drafts

Reviewer: separate executor; wrote none of `CORE.md`, `KEYSTONE_NOTE.md`, `PLAN.md`, `OPEN_WORK.md`, `CHANGES_SUMMARY.md`, or the first review (`/workspace/review-archive/core_REVIEW.md`).
Friday 20 November 2026, about 5:18 PM ET (America/New_York).
Drafts in `/workspace/gtao-core`, beside `origin/main` = `a1a98aa` (PR #116 merged as v2.68; #117 is `b12af70`, v2.67; #115 is `1998a2d`, v2.66). CLAIM_MAP tally on that commit: OPEN 84, PROVED (in-model) 94, MATH-CORRECTED 23, PRIOR ART 32, total 318, as the drafts state. Working tree is untracked relative to `a1a98aa`; nothing was edited, pushed, or merged in this pass.

First review: READY-WITH-FIXES, 2 blockers (B1 CT41 wording; B2 pair-rule rescue). This confirm is against that review, `CHANGES_SUMMARY.md`, and the revised drafts, with a mathematical check of the new rhythm "candidate" in `core/KEYSTONE_NOTE.md` §4.

## Verdict: READY-WITH-FIXES (1 new blocker)

Both original blockers are fixed, and the listed should-fixes are either applied or correctly left open (S5 rerun; S8 queue freeze). The remaining blocker is a residual overclaim in the new §4 material: the hull-increment "candidate" that matched argmin J in 189/189 is a mathematical identity, not an empirical finding and not a prediction from the world's time scales. The note already says the procedures are equal "up to ties," but still presents 189/189 as evidence for a candidate rule; `CORE.md` points the reader to that candidate. That has to be said plainly before a CORE PR merges.

## Original blockers

**B1. CT41 kill rule — FIXED.**
`CORE.md` §3 (`:26`) and §6 (`:59`) now use the merged CT41 wording, identically: a non-move is consistent only if g < Δ_R(k_lo); a miss if g > max(the static band, Δ_R(k_hi)); INDETERMINATE between; and if the predicted gap of a non-mover is ≤ Δ_R(k_hi), the move test is NOT A TEST. The loose "preregistered redesign band" / "a non-move is a miss only outside that band" language is gone. This matches CLAIM_MAP CT41 on `a1a98aa` (the map says "consistent if" rather than "consistent only if"; with the miss and INDETERMINATE clauses present, the two are equivalent). The "no measured cost ⇒ Δ_R = 0" clause is omitted; acceptable compression with the CT41 cite.

**B2. Pair-rule rescue — FIXED.**
The formula is stated as holding in Model S given a numerical convexity premise, and as **false** for rhythms with first-order real stores. A pair rule would predict even K* (0, 2 or 4 in the worked example); the independently confirmed argmin is 3, so that rescue does not recover K*. "Counted by degree" is the CT21 convention for a mode, not a block-count rule. That is the honest statement the first review required.

## New blocker

**B3. The hull "candidate" is the definition of K*, not a predictive rhythm rule.**
`CORE.md:36`, `KEYSTONE_NOTE.md` §4 (title, `:70–:78`, `:85`), and the same framing in `CHANGES_SUMMARY.md` ("Finding" / "Evidence … 189/189"), `OPEN_WORK.md` W9, and `PLAN.md` §6 and §9 piece 2.

### The identity (proved)

The reduced layer-count objective used in N60 is

J(K) = hK + w E_∞ ε_K = h [K + R(1 + ε_K)],

with R = w E_∞ / h > 0, or equivalently φ(K) = ε_K + K/R. K ranges over a finite set {0, 1, …, K_max}. No property of the world, the stores, or the optimizer is used.

**Proposition.** Every minimizer of φ (hence of J) lies on the lower convex hull of the points {(K, ε_K)}. The N60-style increment test on that hull — walk the vertices k_0 < k_1 < … and jump from k_i to k_{i+1} iff R(ε_{k_i} − ε_{k_{i+1}}) > (k_{i+1} − k_i) — returns a minimizer, and with the strict inequality returns the leftmost minimizer. Equality is exact up to ties (a hull edge of slope exactly −1/R).

**Proof.** Suppose k* minimizes φ but (k*, ε_{k*}) lies strictly above the lower hull. Then there are hull vertices k_a < k* < k_b and λ ∈ (0,1) with k* = λ k_a + (1−λ) k_b and ε_{k*} > λ ε_{k_a} + (1−λ) ε_{k_b}. Then

φ(k*) > λ φ(k_a) + (1−λ) φ(k_b) ≥ min(φ(k_a), φ(k_b)),

so k* is not a minimizer. Thus every minimizer is a hull vertex (or, in a tie, any integer point on a hull edge of slope −1/R, all of which lie on the hull).

The lower-hull edge slopes s_i = (ε_{k_{i+1}} − ε_{k_i}) / (k_{i+1} − k_i) are nondecreasing. A supporting line of slope −1/R touches at the vertices where the left slope is ≤ −1/R and the right slope is ≥ −1/R. The jump test is exactly "s_i < −1/R." Walking from the left and taking every such jump stops at the leftmost supporting point of slope −1/R, i.e. a leftmost minimizer of φ. If some s_i = −1/R, the strict test does not jump, and any point on that edge is also a minimizer. □

This is an identity for an arbitrary real sequence ε_K. It does not require convexity of ε_K, a well-optimized curve, rhythms, or Model S. The phrase in the note, "that is what the identity predicts *if the ε_K curve is well optimized*," misstates the condition: the two procedures agree whether or not the curve is optimal. Good optimization is needed only for the agreed-upon K* to be the true design optimum, not for the match itself.

I recomputed both procedures independently on the 189 stored (world, R) curves: 189/189 agree, and they agree with the stored `argmin` / `hull` fields. The same check on 2,000 random ε sequences (length 2–12, R over 10^{−1}..10^3) also matched 2,000/2,000. That is what the identity requires. It is not evidence that a rhythm rule has been found.

To evaluate either J or the hull you must already have ε_K at every K you consider — that is, you have already solved the design problem at each K. The procedure is a counting restatement of argmin J on a measured curve, not a prediction from the world's time scales (poles, damping, stakes) alone.

### What must be said plainly

`CORE.md` and `KEYSTONE_NOTE.md` (and the matching lines in OPEN_WORK W9, PLAN §6 / §9 piece 2, and CHANGES_SUMMARY) must say, without calling this a candidate rule or citing 189/189 as support for one:

- The predictive keystone — layers from the world's time scales whose stakes pay for them, counted by degree — is proved or numerically supported only in Model S, and there only given convexity, which remains unproved.
- For rhythms, the only general statement is the definitional one: K* is argmin_K [K + R(1+ε_K)], which always coincides with the supporting line to the lower convex envelope of the measured ε_K (including K = 0). That is not a new rule.
- A predictive rhythm rule (K* from the poles and the stakes, without first computing the whole ε_K curve) is **OPEN**. No pole-count or pair-count shortcut on this grid recovered it.

The empirical content of the sweep that should stay, and that I independently recounted from `rhythm_rule.json`, is real and useful:

- 21 worlds, 9 values of R, 189 comparisons; 11 worlds convex, 10 non-convex (all light or medium 2- and 3-oscillator worlds).
- N60 raw (starts at 1) = argmin in 170/189. Of 19 misses, 2 are the K* = 0 hole (convex one-oscillator worlds at R = 0.5); 17 are genuine, all in non-convex worlds (17/90). On convex worlds with argmin ≥ 1 the adjacent formula never missed (97/97).
- Even/pair argmin matches in only 66/189 (fails on every odd K*). Degree-pairs cap (K ∈ {0, 2, …, 2n}) matches in 53/189.
- K* is odd in 123/189, and K* ∈ {3, 5} in 15 comparisons. The worked example at R = 3 is one of them (argmin 3, N60 2, even/pair 4). A single lightly damped oscillator, with convex ε_K, has K* = 3 at intermediate R and K* = 4 at higher R (`1osc_z0.02_N0.04` at R = 20; `1osc_z0.02_N0.2` at R = 5, then 4). Real first-order stores can need more than the mode's degree, and the extra store need not come in a pair.
- Worked example reproduced: E_∞ = 0.03788281801526715; at R = 3, J = (7.376, 7.839, **7.105**, 7.428), argmin 3. Lyapunov gaps 10^{−16} to 1.6×10^{−6}. Scope limits in the note (designed grid, K cap 2n+2, DE only for K ≤ 4) are fair; three light oscillators end at E_8 = 0.0626 vs E_∞ = 0.0554, so some sequences had not reached the causal floor.

Including K = 0 in the envelope (and in the argmin) closes the formula's K* = 0 hole by definition. That is a correct index fix, not a further empirical discovery.

## K* = 0 hole handling

Fixed as required (S2 / S10). `CORE.md:34` now says "at most one layer for one real scale" with CT21: K* ∈ {0, 1}, and keeps the random-walk point ("scale-free ⇒ many layers" is false at α = 2). `CORE.md:36` and `KEYSTONE_NOTE.md:31` cite CT21, not L1, for the hole in the formula as written, and correctly flag LAYERS.md's Theorem L1 ("K* = 1 for every w and h") as the overstatement. The two K* = 0 cases in the sweep are the expected ones (convex one-oscillator worlds at R = 0.5). No remaining contradiction.

## Should-fixes from the first review

| ID | Status |
|---|---|
| S1 stale #117 confirmation | Applied. The leftover "await confirmation" is gone from CORE, PLAN, and OPEN_WORK W4. |
| S2 / S10 K* = 0 and CT21 vs L1 | Applied (see above). |
| S3 fast/slow IDs and latency premise | Applied. `CORE.md:46` now cites CT28 and CT34 and states equal read quality, shared upkeep in local layers, and worth falling as e^{−2ℓ/τ}. CT14, CT16, CT35, CT36 remain on the sharing / joint-value half of the row. |
| S4 #116 not on main / rebase | Obsolete, correctly updated: #116 is merged as `a1a98aa`, v2.68. PLAN no longer treats it as a pending rebase. |
| S5 120-world solver overstated | Disclosed in the note, not rerun. `core/keystone_checks/stores.py` is still the pre-#116 raw `lstsq`; the merged guarded inversion is in `theory/layers_checks/stores.py`. The rhythm sweep uses its own guarded inversion and the first reviewer's multi-start, which is the right tool for §4. A Model-S rerun with the merged solver remains owed (`OPEN_WORK` S5). Acceptable for this pass. |
| S6 adversarial climb finished | Applied: max ε₂/ε₁ = 0.4625; independent 0.461. Closest approach, not a violation. |
| S7 PLAN §3 arithmetic | Applied: section O is 74 rows (CT1–CT43 + CL1–CL21 + CX1–CX10), no double count; core total 91 of 318. |
| S8 OPEN_WORK staleness | Applied for W5 (hygiene v2.70, not W4), H1, H9 (`v2.6-evo` only). The 62 unabsorbed queue items remain, correctly gated on Chad (H6/C6). |
| S9 traceability nits | Applied: gate is THEORY §3 / FRAMEWORK §9; missing-cost kill is J16 not CT23; PLAN §0 relaxed to load-bearing sentences; "under head/tail breaks 1.0" added; Gerrard & Tsanakas booked mainly on CL18. |
| S-plan | Partially: PLAN §9 piece 2 already says "candidate hull rule … (not a law)," which is the framing B3 rejects. Update with the identity wording after B3. |

## Other checks

- Hypothesis sentence is exact and appears once on the core page. No "theory of everything," no "bill," no joules. "Law" in CORE appears in the hypothesis sentence and, newly, in "a candidate, not a law" at `:36`. If the wording rule is still "law only in the hypothesis sentence," rephrase that clause when B3 is applied (e.g. "not a predictive rule"). OPEN_WORK C3's discussion of the pending "Proposed law" label remains appropriate for a work list.
- Status headers match `a1a98aa` (v2.66 / v2.67 / v2.68; tally 318; 118 tests). I did not re-run pytest in this pass.
- Scorecard, CT20/CT33 ruin-slack qualifier, CT40's "with redesign per regime," records-as-agents and ht-index demotion, and "predicts only through price-free structure or independently measured prices" remain as the first review passed them.
- N60's Model S status is unchanged and correctly scoped: count formula proved given convexity; convexity numerical only, unproved, no counterexample found; field-untested. I did not produce a convexity proof and did not search for a new Model S counterexample.
- PLAN is still conservative on deletions, locked preregs, and Chad-gated outside acts. One stale clause: `PLAN.md:110` still says OPEN_WORK "has no §5"; §5 now exists (remaining should-fixes). Point H9 at §2, and drop "there is no §5."
- Small inconsistency in the note, not material to the counterexample: §2 still quotes the earlier draft J_4 = 7.425 and ε_4 = 0.1415; the first reviewer's confirmation and this sweep both have E_4 ≈ 0.043288, J_4 = 7.428, ε_4 ≈ 0.1427. Use the later figures in §2 as well. Argmin 3 is unaffected (E_4 would still need to be < 0.03921 to flip it).

## What would make this READY

Apply B3 in `CORE.md` and `KEYSTONE_NOTE.md` (and the matching W9 / PLAN / CHANGES lines). Do not advertise a hull "candidate" or 189/189 as evidence for a new rule. Keep the real empirical findings (pair rule fails; odd K* including 3 and 5; one oscillator can need K* > 2; N60 adjacent fails when ε_K is not convex). Then a short re-confirm of those sentences. After that, this can be the one-page core.

