# Errata to the locked swarm-completion files

*Friday 27 November 2026 (America/New_York). Written after the independent review of #298. This file is not hash-locked and may be appended. Locked bytes (`checks/SHA256SUMS`, `checks/SHA256SUMS_2`, `checks/SHA256SUMS_toy`) are never edited; where a locked file says more than it shows, the correction is recorded here.*

| id | locked file and line | what it says | correction |
|---|---|---|---|
| E1 | `checks/swarm27_checks.py:843`, printed at `checks/swarm27_checks.out:37` (`floor_alone_never_forces_leave`) | "(< 0 means following beats leaving)" | The checked quantity, \(\min_\varepsilon[s\eta\lambda L(\varepsilon)+w\varepsilon]-w/2\), uses a lower bound on what following costs. A negative value shows that the heat floor cannot force leaving (P2). It does not show that any real memory follows for less than \(w/2\). See `FEEDBACK_PART.md`, P2. |
| E2 | `checks/swarm27_checks.py:406`, printed at `checks/swarm27_checks.out:13` (`clarke_truth_dominant`) | "others' reports arbitrary=true" | The check tests misreports against truthful others only. ST1's proof (`STAKES.md:23`) covers arbitrary reports by the others; the check does not. |
| E3 | commit `13f478d26c2f7d3452b44b15edb57abb177f973b` (message, not a locked file) | "35 CHECK PASS" | `checks/swarm27_checks.out` has 32 CHECK lines, all PASS, FAILS 0 (`INDEX.md` gives 32). The commit message is not rewritten. |
| E4 | `PREREG.md` step 1 and `DEVIATIONS.md` (D1) | the lock was "pushed and seen with `git ls-remote`" before each run | True as run, but not checkable by a third party: only commit order and commit timestamps can be verified (review of #298, N17). |

Future deviations from `PREREG.md` go in `DEVIATIONS_2.md`, not in `DEVIATIONS.md`, which lock 2 covers as of D1.
