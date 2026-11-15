# CAUSAL-KILL-INPUTS — independent review of PR #41 (THEORY v1.4.4 → v1.4.5)

**Verdict: PASS-WITH-FIXES.** The fixes touch only the v1.4.5 changelog entry and the CLAIM_MAP pointer. The N6 and §9 kill text is merged as authored.
Reviewer: a separate executor (for Ace, Chad t1914/t1916), 15 Nov 2026, about 4:10 PM ET. I wrote none of R2 (`HEADLINE_PREMISE_REVIEW.md` §2, §4),
the author note, `holes.py`, or any earlier N6/§9 text. Ledger 86. No CLAIM_MAP status change. Vigilance stays OPEN. Nothing was posted or sent.

## 1. What I read
- THEORY.md before (origin/main 66d68aa, v1.4.4) and after (q-pick17 848e043, v1.4.5): §1 N6, §2.2 Regime A premise bullet, §9, §13.
- `CAUSAL_KILL_INPUTS_AUTHOR.md`; `HEADLINE_PREMISE_REVIEW.md` §2 (escape-hatch audit) and §4 (R2 text); `V141_REVIEW.md` §3; CLAIM_MAP N16.
- The STAKES-SHIFT-CAISO prereg at its lock (q-pick15, 874576f).

Note on sources: R2 is in `HEADLINE_PREMISE_REVIEW.md` §4, not in V141_REVIEW. V141_REVIEW §3 holds only the lag note, and the new N6 pointer
cites it correctly.

## 2. Independent re-derivation (`CAUSAL_KILL_INPUTS_REVIEW_checks/rev_holes.py`, `.json`; nice 19)
These are my own code and routes. I did not use or read holes.py's method. The model is a telegraph world with levels ±μ, rate λ and white noise N
(here N = 1), with q = λμ² up to a constant. The base point is λ = 0.01 and μ = 2 (2μ²/λN = 800).

| Case | N16 t_A (leading order) | Wonham MC t_A (exact filter, 1000 paths, ≈ 2,950 switches) | Bayes MSE (Bessel, exact) | Linear (Kalman) time constant |
|---|---|---|---|---|
| base | 0.638 | 0.645 ± 0.007 | 0.120 | 2.50 |
| (a) q fixed, λ ×½ | −36.4% | −36.7% | −38.0% | +0.1% |
| (a) q fixed, λ ×2 | +45.7% | +43.3% | +49.9% | −0.4% |
| (b) q ×2, λ ×2.6546, μ² ×0.7534 (my root find) | 0.0% (1e-12) | −1.0% (≈ 1.4 SE) | **+105%** | **−29.5%** |

The MC estimates mean first passage of the posterior log-odds to 0 after a switch, using Euler steps with dt = 2·10⁻³.
- **Hole (a) is confirmed.** At fixed q the Bayes optimum moves by tens of percent, and the linear optimum barely moves. A trigger list of only α, q, N
  and stakes cannot fire on this change. Without the new clause, a Bayes-locked design that ignored λ and μ would escape.
- **Hole (b) is confirmed for the memory-time quantity.** The split leaves Bayes t_A fixed (the MC agrees within 1%), so old §9's "stays put"
  would have killed an optimal design. The linear optimum predicts −29.5% at the same point. This is why the scored direction must come from the
  *locked* optimum.
- **New finding 1 (scope of a "null").** At the same point (b), the Bayes MSE changes by +105%. A null prediction belongs to a design quantity, not
  to a change in the world. The new wording ("the design quantity does not move in the direction its locked optimum predicts") is already
  per-quantity, so no text fix is needed.
- **New finding 2 (correction to R2).** R2 said that for linear-locked tests "any change in α, q, N or stakes moves the optimum". That holds only
  for single-input changes. Under joint changes the linear optimum can also stay fixed (stakes ×2 with q ×½ leaves read rate ∝ (w·q/c)^{1/α}
  unchanged). So the declared narrowing of §9 (no kill when the optimum predicts no move) also covers linear-locked tests. That is still correct
  from first principles, because staying put is then optimal. I recorded it in the changelog (fix F2).

## 3. Judgment of each change
| Change | Minimal? | Widens kills beyond what's justified? | Consistent with v1.4.4 premise and one-locked-optimum rule? | Ruling |
|---|---|---|---|---|
| N6 trigger "+ (or, for a Bayes-locked prereg, the further inputs that optimum needs)" | yes; R2's text | widens only to inputs the locked optimum itself uses (hole a, reproduced) | yes: the extra inputs enter only under a Bayes lock, and the linear stays the default | keep |
| N6 "direction the locked optimum predicts from the measured inputs before and after the change" | one clause beyond R2's literal N6 text, in R2's own §9 sense | no: it sharpens; joint changes need a joint prediction (hole b) | yes: "locked optimum" is defined by the one-optimum rule, including for preregs that name none | keep (Q3) |
| N6 lag "(a number fixed in the prereg; V141 §3)" | yes | it removes the waiting rescue; no prereg that has already run is affected | yes | keep; the pointer resolves (Q6) |
| §9 "stays put" → aligned with N6 | yes | widens to wrong-way moves and Bayes inputs; narrows only where the old literal text was wrong (the optimum predicts no move) | yes; N6 governed already | keep |
| §13 v1.4.5 entry | needed fixes F1–F2 | n/a | n/a | fixed |

**Goalposts.** Before this PR, the only locked prereg in causal form is STAKES-SHIFT-CAISO (pick 15, in flight). It is linear-locked and lists
its inputs (w, q, N, α; no jump inputs). Its lag is fixed at 12 months. Its FAILED rule is "precision did not move in the predicted direction
after the lag". It reads the same under v1.4.4 N6 and v1.4.5 N6/§9, so it is **unaffected** in both directions. Every other locked test is in the
optimality form or concerns no N6 input change. The only other mention is the unlocked STAKES-EXOGENOUS observation, which was never a verdict.
No result changes.

## 4. Fixes applied (narrow)
- **F1.** The v1.4.5 changelog said "authored, awaiting independent review". It now points to this review and records the outcome, following the
  v1.4.4 precedent.
- **F2.** The changelog now records new finding 2: under joint input changes, the narrowing also applies to linear-locked tests, and R2's
  "special case" remark holds only for single-input changes.
- **F3.** The THEORY header pointer for CLAIM_MAP goes from v2.16 to v2.17. v2.17 has been on main since pick 16, so the old pointer was stale.
  I did not write a v2.18 note, because no row or status changed and q-pick15 may take v2.18.

## 5. Rulings on the author's six questions
1. **Null predictions: no text change.** A change whose locked optimum predicts no move, or a move inside the prereg's measurement error, has no
   direction, so the causal form does not score it. That follows from the wording. Scoring a move beyond error as a miss would add a new
   *invariance* claim, which widens the theory's claims. That goes to a queue item instead: **CAUSAL-NULL-INVARIANCE**. Point (b) suggests the
   item is worth doing: Bayes predicts no change in memory time, while linear predicts −29.5%. That makes it a Bayes-vs-linear discriminator.
2. **Prices: no change here.** The effort price is an input of the linear optimum too, so this is not part of R2's Bayes hole. Adding it widens the
   kill. A related point: "from the measured inputs" means an unmeasured price change is a confounder, which a prereg must hold fixed or measure.
   Queued as **CAUSAL-KILL-PRICE**.
3. **"Before and after": keep it.** It is R2's own §9 sense, and it is required from first principles. The numerics in §2 show that single-input
   signs cannot decide a joint change, for both the Bayes and the linear optimum.
4. **Magnitude: sign-only is intended, so no change.** The optimality form catches levels, and a prereg may lock a size band as a pass condition
   (STAKES-SHIFT-CAISO does). A magnitude kill in the causal form would widen the kill set. Queued as **CAUSAL-KILL-MAGNITUDE**.
5. **Lag set: keep a single number.** A badly placed lag costs power, not validity. A prereg may report other lags without a verdict (CAISO
   reports lag 0 that way). A locked set with a multiplicity rule changes both the kill and its error rate, so it is a protocol question for a
   future prereg, not a theory edit. No item.
6. **Pointer: it resolves.** `V141_REVIEW.md` §3 ("Causal core and internal consistency") contains the note that "after its adjustment lag" must
   be fixed numerically in each locked test.

## 6. Hostile pass on the final diff (origin/main..q-pick17 after fixes)
- I ran the diff through these checks:
  - Only the N6 kill cell, the §9 causal bullet, the title, the dates, the CLAIM_MAP pointer and the §13 entry changed.
  - The headline, the status block, §0, §2 and the CLAIM_MAP rows are unchanged.
  - No added line uses "law".
  - Vigilance is not touched.
  - No locked file under `tests/` or `prereg/` changed.
- Independence caveat: F1–F3 are this reviewer's own. They are bookkeeping and a factual changelog note, and they do not change kill text. The same
  reviewer checked them (recorded here).
