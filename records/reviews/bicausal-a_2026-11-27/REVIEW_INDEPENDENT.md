# Independent review: PR #305 (BICAUSAL Route A follow-up, BA-T1 and BA-T2)

*Friday 27 November 2026 (America/New_York). Reviewed head `1347c64735cddccea6207e20063d8b690c618d78`, base main `a680cc58d19a2d223e12249f00c22596e7f75382`. Reader: a separate agent that did not write the PR, the prereg, the checks or `SECOND_READ.md`. Fresh clone; scored scripts re-run from the lock commit `eb0540e308e65eab06ca86c6e3d9d9d2e9a350ce` at nice 19. My own checks are `indep_review_checks.py` (no sympy, no `ba_lib.py`: exact Lyapunov over Python fractions, finite differences at 60 digits), output `indep_review_checks.out`.*

**Outcome: pass, 0 blocking.** Both claims follow from their proof or computation inside the stated classes, the lock came before the runs, and the outcomes and misses are recorded as they happened.

## 1. Claims against proof and computation

- **BA-T1** (`theory/bicausal-a-2026-11-27/RESULTS.md:14-16`). The weighted-potential condition (`PREREG.md:52-58`) is the right necessary condition: for a weighted potential \(\Psi\), \(\partial_{\theta_k}\partial_g J_m/\lambda_m=\partial_{\theta_k}\partial_g\Psi=\partial_g\partial_{\theta_k}J_w/\lambda_w\), so \(\Delta\neq0\) at a point rules out positive weights near it. The domain \(\gamma>0,\ gc<1\) is exactly the stability region (trace \(-a-\gamma<0\), determinant \(a\gamma(1-gc)>0\)) and is connected; the costs are real-analytic there, so \(\Delta\not\equiv0\) has a zero set with empty interior. Re-run: `ba_t1.py` and `ba_t1_exact.py` reproduce their committed outputs exactly (apart from file paths). Independent check: \(\Delta\) by 60-digit central differences of independently solved costs matches the four exact rationals at the scored witness (\(w_x=0.5,1,2\), and \(0\)) to \(10^{-24}\) relative, and the heats-only witness \(-28/1331\) to all printed digits.
- **BA-T2** (`RESULTS.md:24`). The comparator \(2\sqrt{kTavw}-kTa\) is the proved infimum over bipartite memories (`theory/INFO_PHYSICS_ATTAINABILITY.md:41-47`), and a direct tracker optimized in class LINK approaches it from above (exact evaluation; the float optimizer dips about \(10^{-5}\) below it at \(\ln b_1\approx24\), which is round-off, not a design). The three confirming designs, rounded to the three decimals printed in `checks/ba_t2.out` and evaluated in exact fractions, still give ratios 0.983729, 0.994268 and 0.960956, with the world's heat exactly 0 and the level's heat equal to the §3.2 closed form exactly. So the hit does not rest on the 12-digit design or on round-off. BA-C2 (`PREREG.md:92`) is sound: the two coordinates' heats bound their own flows, the flows add to the composite's learning rate, and that rate is at least \(R\) at an error no larger than \(\varepsilon_1\). Scored reruns of `ba_t2.py` and `ba_t2.py --half` from the lock commit: see §6.

## 2. Lock and record

`sha256sum -c PREREG.sha256`: 10 of 10 OK at the head. Lock commit 19:38:00 ET, gate read 19:38:29 ET; the run clone was made at 19:38:39 from GitHub and already holds the gate-read commit, so both were pushed before the first output (`ba_t1.out`, 19:38:45 ET). No locked file changed after the lock (`git diff eb0540e..1347c64` touches only new files under `checks/` and unlocked pages). The gate read is a same-agent pass and says so (`gate_read.md:3`). The `nsimplify` printing slip, the CPU overrun and the overstated odds are logged (`DEVIATIONS.md:5-7`, `process/FAILURES.md`, rows `BA-T2-ODDS` and `BICAUSAL-BRIEF-1`). No open miss is hidden; the earlier A-T2 miss and the A-T1‴ boundary-hit stay open in the README row.

## 3. Units

\(\dot Q_0=b_0^2av/((a+b_0)D_0)\): \(\mathrm{t^{-2}\cdot t^{-1}x^2/(t^{-1}\cdot x^2t^{-1})=t^{-1}}\), times \(kT\) an energy rate (`PREREG.md:85`). \(kTavw\) is (energy/time)\(^2\), so \(J_{\mathrm{dir}}\) is an energy rate (`PREREG.md:78`). Member heat \(D_0/\delta\) (`RESULTS.md:34`): \((x^2/t)/x^2\), times \(kT\). W2 costs (`PREREG.md:47-50`) are in energy units with \(kT_i=D_i\). All consistent. One notation slip, non-blocking, in a locked PAPER section: `PREREG.md:96` says \(u=D_0\) "(gain 1)", but the formula on `PREREG.md:99` and the seeds in `checks/ba_t2.py:40` use \(u=D_0/b_0^2\) (the level's noise in the coordinate whose drift has unit gain on \(X\)); with that reading the PAPER formula follows from §3.2. No scored number depends on it.

## 4. Wording and scope

No claim that GR, QM, holography or forces are derived; `PREREG.md:19` disclaims them. Both results say in-model, WORKED-CLASS-ONLY, not Lean, and BA-T2 says upper bound and "true by construction" for the heat accounting (`RESULTS.md:36`). Fixed in this review's commit: the README row read "beats direct trackers from K = 24 to 32 members", which suggests a range; it now gives the threshold per stake. `RESULTS.md:18` said S2 fails "everywhere" and used "failure" as an outcome word; it now says "on every open subset" (the proof's scope). The ledger rows BAT1, BAT2 point to this review.

## 5. Hypothesis line and currency

`CORE.md:7` is unchanged from main and byte-equal to `README.md:7` and `PREREG.md:5`. The branch contains main `a680cc5` (merge `2e6a9aa`). Against layout PR #306 (`ace-move3-2026-11-27`), a trial merge conflicts only in `process/FAILURES.md` (appended rows on both sides) and `process/PROCESS.md` (generated counts); whichever merges second keeps both rows and regenerates counts with `tools/facts.py --write`. #306 moves `NOTES/rnd-2026-11-26-late/`, which locked `PREREG.md:120` cites; a locked prereg keeps its text.

## 6. Scored reruns

From a checkout of the lock commit, at nice 19: `toy_checks.py` and `paper_approx.py` reproduce `checks/toy_checks.out` and `checks/paper_approx.out` (the latter apart from numpy overflow warnings on stderr). `ba_t2.py` reproduces `checks/ba_t2.out` byte for byte apart from the elapsed-time line (1666 s wall on a shared box): every optimized cost, design and the exact re-evaluations, \(\hat K^*=32, 24, 24\), HIT. The half-tolerance rerun was still running when this review was committed; its result is reported with the merge, not here.

## Not done here, left as next steps

The CORE §1 table pointer for \(L\) that `RESULTS.md:10` names as the update is not written by this review: a change to the governing page should be made by its author, now that the review is in. Lean formalization of either result is not attempted.
