# CAUSAL-KILL-INPUTS — author note (pick 17, rule slot; ledger 83–85)

**Outcome: authored, awaiting independent review.** Author: executor queue-pick17 (for Ace, Chad t1914), 15 Nov 2026 about 4:05 PM ET.
This edits the theory's kill conditions (THEORY §1 N6 causal form, §9 causal bullet), so per Chad t1916 a separate reviewer, who did not
write it, judges it and alone may merge it. Source: proposal R2 in `reviews/night2/HEADLINE_PREMISE_REVIEW.md` §2 and §4 (pick-14 reviewer);
this author did not write R2 or any earlier N6/§9 text. THEORY v1.4.4 → v1.4.5. No CLAIM_MAP status change; no locked prediction, result or
proof changed; vigilance stays OPEN.

## 1. Causal first principles

The causal kill is a comparative-statics test. The theory says design is set by the world's inputs through a cost-minimising optimum. Change an
input, and the design should follow the optimum's change, in sign, once the system has had time to adjust. Three things make the test
well posed, and each matches one hole R2 found.

1. **The trigger is any input of the optimum that is scored.** Since v1.4.4, each prereg locks exactly one optimum before the data. A linear-locked
   optimum needs α, q, N and stakes. The Bayes optimum of a non-Gaussian world needs more: for the two-state switching world, jump rate λ and jump
   size μ separately (N16). If the trigger list names only α, q, N and stakes, a change in λ and μ at fixed q moves the Bayes optimum but cannot
   trigger the kill. A design that ignores it escapes (hole a). Author's check (`CAUSAL_KILL_INPUTS_checks/holes.py`, `.out`): at fixed
   q = λμ², halving or doubling λ moves the Bayes adaptation time t_A by −36% or +46%.
2. **The prediction is the sign of the locked optimum's change, not "some change".** When inputs move together, the predicted direction comes from
   the locked optimum evaluated at the measured inputs before and after the change. A single input's sign does not decide it. Old §9 ("stays put
   while ... change") fails both ways. It misses a design that moves the *wrong* way. It also fires on a design that correctly stays put when the
   optimum does not move (hole b). Check: q doubled, split as λ ×2.65 and μ² ×0.75, leaves the Bayes t_A unchanged (to 1e-16). A linear-locked
   optimum would predict a move here, which is why the comparison must be against the locked optimum.
3. **The lag is a number fixed before the data.** "After its adjustment lag", left open, allows the rescue "we did not wait long enough"
   (V141_REVIEW §3 note). A number in the prereg removes it.

Consistency with v1.4.4: the premise ("for a Gaussian world, or for the best linear tracker in any world") makes the linear inputs the default.
The further inputs enter only when the prereg locked a Bayes optimum. The one-locked-optimum rule supplies "the locked optimum" that the new
wording refers to, including for preregs that name none (scored against the best linear one). No new axiom, constant, regime or claim.

## 2. What each changed sentence does

| Where | Change | Effect |
|---|---|---|
| §1 N6, kill column, causal sentence | adds "(or, for a Bayes-locked prereg, the further inputs that optimum needs)" to the trigger list | closes hole (a); widens the kill |
| same | "the predicted direction" → "the direction the locked optimum predicts from the measured inputs before and after the change" | ties the sign to the locked optimum and to joint input changes; sharpens (no single-input sign picking). Author's tightening beyond R2's literal text, in R2's sense |
| same | "after its adjustment lag" + "(a number fixed in the prereg; `reviews/night2/V141_REVIEW.md` §3)" | closes the lag rescue; sharpens |
| §9 causal bullet | "stays put while" → "does not move in the direction its locked optimum predicts (§1 N6), after the adjustment lag fixed in its prereg, while"; trigger list gains "(or, for a Bayes-locked test, the further inputs of §1 N6)" | aligns §9 with N6. Widens (catches wrong-way moves, Bayes inputs) and removes one mis-fire (below) |
| Header, draft dates, §13 | v1.4.5 and changelog entry | bookkeeping |

**Declared narrowing (one case).** Old §9, read literally, killed a design that stays put when the locked optimum predicts no move. That design is
optimal, so the old firing was an error. N6 already said "predicted direction". The edit removes the mis-fire. It narrows §9's literal text only
there and opens no escape for a design that is not optimal.

**Effect on tests in flight.** STAKES-SHIFT-CAISO (pick 15, q-pick15, locked) is linear-locked, lists its inputs, and fixes its lag at
12 months under this item's interim rule. Its verdict is unchanged in both directions. No Bayes-locked test exists.

## 3. Open questions for the reviewer

1. **Null predictions.** If the locked optimum predicts no move (within measurement error) and the design moves, is that a causal miss? The
   new wording ("direction") does not score it, and neither did N6 before. Should the theory say so explicitly (e.g. "a change whose predicted move
   is within measurement error is not scored in the causal form"), or score a move beyond error as a miss? The author left this out to stay
   minimal.
2. **Prices.** The §2.2 optima also take the effort price (e.g. read rate ∝ (stakes·drift/price)^{1/α}). Neither N6's causal list nor §9 names
   price; J6 in §0 covers price response separately. Should "stakes" read "stakes or prices", or should the list become "any input of the locked
   optimum"? That is a wider change than R2, so it was not made.
3. **The "before and after" tightening** goes beyond R2's literal text. Keep it or drop it?
4. **Magnitude.** The kill is sign-only. A move in the right direction but far too small passes the causal form (the optimality form may still
   catch it). Intended?
5. **Lag uncertainty.** A fixed number may sit in the wrong place, which hurts power, not validity. Should a prereg be allowed a pre-fixed *set*
   of lags with a multiplicity rule? The author kept a single number, as R2 and V141 asked.
6. **Pointer.** V141_REVIEW's lag note is in its §3 ("Causal core"). Check that the pointer resolves.

## 4. Checks run by the author (own, not independent)

- `CAUSAL_KILL_INPUTS_checks/holes.py` (nice 19): uses N16's asymptotic t_A. The validity ratio 2μ²/(λN) is 800 and 227 at the points used.
  q = λμ² is up to a constant factor, which does not affect either hole.
- Each replaced string occurs exactly once in THEORY.md (asserted). No other N6/§9 text, headline, status block or CLAIM_MAP row changed.
- No use of "law" was added.
