# Clarification: E. coli qualification measurement plan, 21 November 2026

This is a post-computation clarification, written after the computation in
`MEASURE_RESULT_2026-11-21.md` and after the independent review of PR #127, and
disclosed as such. It does not change any official verdict, and it does not
edit the locked plan. The official record remains **NOT ESTABLISHED** (item
(b) *N_e* ESTABLISHED; items (a), (c), (d) and (e) NOT ESTABLISHED). This is
not a finding of NOT QUALIFIED, and it is not a re-score of P1, P3, P4 or P13.

The locked plan is `MEASURE_PLAN_2026-11-21.md`, locked in `6667afd` before any
computation under it (rebased onto `main` `54a4562` as `80acab7`). That file is
unchanged; its bytes still match `6667afd`.

## C1. Plan §4.4’s FAILS and NOT ESTABLISHED clauses collide for “R3 inside the box and no other rival scorable”

Plan §4.4 says (d) is **NOT ESTABLISHED** “if no named rival is scorable …
(including the case that R3 cannot be excluded and no other rival can be scored
without inventing a price or a mapping).” It also says (d) **FAILS** “if every
scorable named rival’s design lies inside the design-unit band,” and that the
already-disclosed R3 screen “becomes a FAILS only if no other scorable rival is
excluded.” After a search that finds no other scorable rival, those two
sentences point both ways.

**How the present computation labelled the case.** The computation followed the
more specific NOT ESTABLISHED clause. Item (c) is in any case not established,
so no design-unit band of width ε + δ_meas was formed. The official verdict on
(d), and overall, remains **NOT ESTABLISHED**. That label is not flipped to
FAILS, and the class is not declared NOT QUALIFIED on this branch.

**What the colliding FAILS clause implies once ε exists.** As specified, P1 and
P3 cannot discriminate against rival R3: the locked rival τ_v = 1.160 s already
lies inside the locked Arm B τ\* box [1.093, 1.171] s, so R3 cannot be excluded
even at ε = 0, and a positive ε would only widen the band. Once σ and ε are
established, if the situation is otherwise unchanged (R3 still inside the box,
and no other scorable rival excluded), (d) is expected to FAIL under the
“becomes a FAILS only if no other scorable rival is excluded” clause, and
E. coli would then be **NOT QUALIFIED** under this plan.

**What this does not do.** It does not silently edit §4.4 of the locked plan.
It does not change the official present verdict. It does not re-score P1, P3,
P4 or P13. A sharper E. coli prediction, or a different organism, is needed if
the class is to be tested against a rival that can actually be excluded.
