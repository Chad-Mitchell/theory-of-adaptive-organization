# Gate read: `theory/speed-cost-2026-11-27/PREREG.md`

*Friday 27 November 2026 (America/New_York). Reads the `Gate` section of `PREREG.md` (lock commit `4dabe1e96c9a12b3302f9cb19bd779777dd3b3cb`, sha256 `a74b83bae146fc517d9aab75c892518b724cd6f6b22c22d8a071eca947e7b2b1`, the first line of `LOCK.txt`) and the formulas it cites, per `process/PREREG_GATE.md` section 2. **Limit, stated up front:** this is a separate pass by the same agent that wrote the prereg, made after the lock and before any scored run. It is not an independent reader. It checks order and the five fields; it does not make the gate independent.*

| ID | G1 | G2 | G3 | G4 | G5 | Pass or stop |
|---|---|---|---|---|---|---|
| SC-B1 | Named: floor reached at some grid point, \(E\le2\times10^{-4}\); odds 0.10, not about 0 | Passes for \(n=3,4\) (searched, no closed form); \(n=2\) labeled CONSISTENCY_CHECK | Passes: two readings predict different quantities (about 0 against at least \(1.6\times10^{-3}\)); the gap is eight times \(\tau\) | (a), route to `CORE.md:74` | Different after a hit and a miss | **Pass** |
| SC-B2 | Named: \(Q_{\rm frac}>0.10\) at any point; odds 0.40 | Passes: no closed form for \(n=3,4\) at fixed error under an exit cap | Passes: the two-state reading predicts \(Q_{\rm frac}\approx0\), the artifact reading near 1; the gap is far above the search resolution | (a), route to `CORE.md:74` | Different after a hit and a miss | **Pass** |
| SC-B3 | — | Fails, as labeled: implied by B2 (paper bounds \([9.05,12.14]\) inside \([8,12.5]\)) | — | — | — | Reported only |
| SC-B4 | — | Fails, as labeled, and seen before the lock | — | — | — | Reported only |

**Outcome: PASS, 0 blocking.**

**Non-blocking notes.**

1. The search is one-sided (PREREG section 5). A hit on B1 and B2 means no better design was found among \(n\le4\) with the stated starts, not that none exists. A miss is conclusive for existence. The RESULTS must say so.
2. The cap is a cap on the total exit rate per memory state (assumption 2). With it, \(n\) redundant states do not multiply speed. A reader who prefers an edge cap gets arm B, which redundancy defeats; the result is scoped to the exit cap.
3. The reader's two-pole diffusion result (PREREG section 0) shows that a wall that holds for a one-pole memory need not hold for a multi-pole one. The telegraph test is in a different class and its Y outcome is scoped to \(n\le4\) jump memories.
4. The leak in PREREG section 7 lowers the information of B4 to about 0, and slightly lowers that of B2. B2's odds were restated with it.
