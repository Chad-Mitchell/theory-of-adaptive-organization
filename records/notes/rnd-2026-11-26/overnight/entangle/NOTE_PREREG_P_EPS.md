# Note on PREREG_P's ε = 0.01 arm: degenerate without a cap on read outcomes

*Appended note, 26 Nov 2026. PREREG_P.md is locked (sha256 a4e02d65…bb5d, re-verified today) and is NOT edited. This note is the record. Source: M1 of `rnd/review_lemma_r/HOSTILE_REVIEW_LEMMA_R.md`.*

1. **The definition.** PREREG_P defines Θ(h, ε) as follows: a read r_A whose outcome has Shannon entropy ≥ h = 1 bit, and some read on B that predicts it with success ≥ 1 − ε. It puts no cap on the number M of outcomes of r_A.
2. **Why the ε = 0.01 arm is degenerate.** With all effects, take the state-ignoring read {0.99·u, 0.01·u/(M − 1) repeated M − 1 times}. Its entropy is h(0.99) + 0.01·log₂(M − 1), which is ≥ 1 bit once M − 1 ≥ 2^91.92. B's constant guess succeeds with probability 0.99. So with unbounded reads, Θ(1, 0.01) is met in every theory, from every state, with no correlation, and the ε = 0.01 arm tests nothing.
3. **Why the run's results are unaffected.** The run used reads for which "H(A) ≥ 1 bit forces an exactly uniform A" (NOTE_P.md line 31). In effect these were binary reads, M = 2. For M = 2, H ≥ 1 forces a uniform outcome, and the reported ε = 0.01 numbers stand as results for binary reads. At ε = 0 no cap is needed.
4. **The general cap.** At ε = 0.01, a product state can meet Θ only if M − 1 ≥ 2^91.92. So every claim of "infeasible from a product start at ε = 0.01" holds for reads with M − 1 < 2^91.92 outcomes, and only for those.
5. **Going forward.** Any later prereg using Θ at ε > 0 must state a read cap before its lock. PREREG_DRAFT_C3v2 now does (binary reads on A).
