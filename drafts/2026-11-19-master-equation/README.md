# WORKING DRAFT, unreviewed, not part of the theory text

Save point of 19 November 2026 (America/New_York). These notes are not theory text, are not reviewed as a package for merge, and do not change `main`.

## The locked claim

> the claim is that one cost under the second law sets how adaptive systems should be built at every scale: layered, with the layers at the world's time scales.

## Framing

The theory is the cost of judgment plus the layered design that minimizes it. The world's pattern of change is a measured input. A wrong picture of the world means re-measuring, and then the cost gives a new design. A wrong cost kills the theory.

## The master equation

An assembly of the repo's own terms, written as one line. It is not a new theorem.

$$\min_{\mathcal{D}} J(\mathcal{D}) = \kappa I_{mem} + hK + w\,\mathbb{E}[\ell] + \sum_k c_k f_k + g \quad \text{s.t. } P(\text{ruin}) \le \varepsilon$$

Pick the design \(\mathcal{D}\) (how many layers \(K\), what each one tracks, how often it reads, and what it shares) that makes the total cost of judgment smallest, without going broke.

- \(\kappa I_{mem}\): holding memory (price per nat held times the memory held).
- \(hK\): upkeep of \(K\) layers.
- \(w\,\mathbb{E}[\ell]\): stakes times expected error, where lateness counts as error.
- \(c_k f_k\): each layer's read price times its read rate.
- \(g\): effort to make the world drift less.
- \(P(\text{ruin}) \le \varepsilon\): staying alive.

The independent review (`review-of-master-equation/REVIEW.md`) found that the equation is a **problem statement, not a theorem**. A constrained minimization cannot be proved; the theorems are its solutions in stated classes. The draft's sentence that Theorem L makes the expected-cost rules the large-buffer limit was **misstated**: Theorem L's optimal interval does not depend on the buffer; the large-buffer slackness claim is a different lemma (see REVIEW.md). Those fixes are pending. Do not put this equation at the top of the core until they are made.

## Three special cases

- **One layer, how often to look.** \(J(T) = c/T + w\,q\,T^{\alpha-1}/\alpha\), which gives a read rate \(\propto (wq/c)^{1/\alpha}\).
- **How many layers.** \(J_K = hK + w\,E_K\). L1–L3 (one timescale gives one layer; \(J\) timescales give at most \(J\) layers, exactly \(J\) once stakes over upkeep clear a threshold; a continuum of timescales means no finite number of layers is exact) are in `PROOF_A.md` and are unreviewed as proofs.
- **The physics floor.** Tracking a random walk costs at least \(J^* = \sigma\sqrt{2kT\,w}\), the same form as the inventory rule \(\sigma\sqrt{2cw}\). Only the currency changes, from heat to money.

Everything else in the theory is this equation solved in one case, once the wording matches the review.

## Next step

Rewrite the README and the core around the locked sentence and the master equation, after the review's fixes, in as few words as are exactly right. This folder is only the save of the work toward that.

## What's in this folder

- `VERDICT.md`, `LEDGER.md`, `PROOF_A.md`, `GAPS.md`, `IMPLICATIONS.md`: layered-spine notes and the L1–L3 proofs, with `checks/`.
- `NOTES_SO_FAR.md`: sources for a layers section, read from origin/main at `5b65c1e`.
- `review-of-master-equation/`: independent review of the master equation, with `checks/`.
