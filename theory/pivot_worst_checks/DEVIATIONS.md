# Deviations for the worst-question pivot

`theory/PREREG_2.md` is not edited.

- **D1, before any result.** The classical model is the exact minimax over the local polytope, solved by HiGHS, not the M=1, M=2 and Frank–Wolfe search named in `PREREG_2.md`. Reason: `RUN_LOG.md`, question (b). This loss is at most the loss any point of that search could return. A loss to it is a loss to a real behavior. A win against it is a win against every local behavior at that error. `K` is the number of weights above `10^{-10}` in the solver's solution, an upper bound on the smallest support at that error.
- The rebit and product searches are not run. On this grid their floors already decide every comparison with C. A search cannot make a rebit feasible below `1/9`, and it cannot make a rebit's loss smaller than `1/9`, which is already enough for C to win the pair at every positive `λ` here.
- **D2, after the first solver solution, before the memo.** HiGHS's basic solution used 11 positive weights. At the same error, atoms can be dropped. The cost uses the minimum support, which is 6 (`decisions.out` line 1). Using 11 would have reported a win at `λ = 0.1` that a 6-state record does not allow. Reason: `K` is in the cost, so an oversized support is not a fair classical contestant.
