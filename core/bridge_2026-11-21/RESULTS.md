# T27 official results: FAILED (P1 pass, P2 pass, P3 fail)

*Scored Saturday 21 November 2026, 12:08 AM EST (America/New_York), after the lock at 12:05:31 AM EST. In-model, numerical. Not a field test. Predictions were not patched.*

**OVERALL: FAIL.** Three official-valid worlds (the first three candidates; none rejected). P1 passed 3/3, P2 passed 3/3, P3 failed 3/3. A fail on any locked gate is a fail of the prereg. No rescue is registered.

Lock (unchanged):

- `PREREG.md` sha256 `25955df4ffb825254100568c9b9d1e751b9d5e0e533146a5d438414c8d5ba994`
- `predictions.json` sha256 `6715777ca45d02ad443a3e5003f19849331a9e60dba900aa6f6c68c93e7adfe3`

These match `LOCK.txt` and the hashes recorded in `run_t27.json`. The official runner printed `LOCK ok` before evaluating any official world. Raw output: `run_t27.json`, `run_t27.log`. Run time 127.2 s at nice 19.

Official rng seeds: 2026112100, 2026112101, 2026112102. All three were 3-mode Model S worlds at the locked \(R=100\), with a unique interior coarse \(K^\star=2\). Mixing SANITY passed on every official cell (TV to exact Boltzmann \(\le 0.20\); high-\(\beta\) TV was typically \(0.002\)–\(0.04\) on the coarse grid and \(0.09\)–\(0.13\) on the fine lattice; low-\(\beta\) TV \(0.11\)–\(0.15\)).

---

## P1 — PASS, 3/3 worlds, all three high \(\beta\)

At \(\beta\in\{8,10,12\}\), on the coarse \(K=0..3\) grid, the mode of the pooled Moran occupation equalled the unique grid \(\arg\min J\) in every cell.

| world | seed | \(J^\star_{\mathrm{coarse}}\) | TV at \(\beta=8,10,12\) | mode = argmin |
|---|---|---|---|---|
| 0 | 2026112100 | 102.0796 | 0.0089, 0.0014, 0.0389 | yes, all three |
| 1 | 2026112101 | 102.2958 | 0.0160, 0.0195, 0.0029 | yes, all three |
| 2 | 2026112102 | 102.4445 | 0.0422, 0.0110, 0.0195 | yes, all three |

## P2 — PASS, 3/3 worlds, all three high \(\beta\)

On the whitened \(K=2\) lattice (\(d=2\), target \(\beta(\bar J-J^\star)=1\), official bar 20%), every official cell was inside the bar. Empirical \(\beta\)-excess ranged from 0.922 to 1.065. The exact Boltzmann values on the same lattices were 1.004–1.011, reported as a diagnostic only.

| world | \(\beta=8\) emp (exact) | \(\beta=10\) | \(\beta=12\) | max rel. err. |
|---|---|---|---|---|
| 0 | 1.049 (1.011) | 1.028 (1.009) | 1.065 (1.007) | 6.5% |
| 1 | 0.968 (1.006) | 1.019 (1.005) | 0.955 (1.004) | 4.5% |
| 2 | 0.999 (1.009) | 0.922 (1.007) | 0.991 (1.006) | 7.8% |

## P3 — FAIL, 0/3 worlds

The locked low-\(\beta\) gate (\(\beta=0.5\), coarse grid) required all three of: mean \(J>J^\star\); at least two layer counts \(K\) with occupation mass \(\ge 0.10\); and low-\(\beta\) excess at least twice the mean high-\(\beta\) coarse excess.

Clauses 1 and 3 held on every official world (means about 104.8–104.9 against \(J^\star\approx 102.1\)–\(102.4\); excess ratios 59–168). Clause 2 failed on every official world: almost all the mass sat in the \(K=3\) slice.

| world | mean \(J>J^\star\) | masses \(K=0,1,2,3\) | # \(K\ge 0.10\) | excess ratio | pass |
|---|---|---|---|---|---|
| 0 | yes (excess 2.825) | 0.000, 0.001, 0.085, 0.913 | 1 | 168 | no |
| 1 | yes (excess 2.584) | 0.000, 0.001, 0.066, 0.933 | 1 | 105 | no |
| 2 | yes (excess 2.383) | 0.000, 0.000, 0.066, 0.934 | 1 | 59 | no |

This is not a mixing miss, and it is not a scoring bug. The exact Boltzmann weights on the same grids show the same pattern: at \(\beta=0.5\), mass on \(K=2\) is 0.071–0.079 (also under the 0.10 floor) and mass on \(K=3\) is the remainder. The \(K=3\) slice has many more designs (1,330 against 210 at \(K=2\)) and each is only about one unit more expensive in the reduced \(J\) (the locked layer-cost term). At \(\beta=0.5\) that entropy wins, so the mass piles on \(K=3\) rather than splitting 10% / 10% across two values of \(K\). The mean still sits above \(J^\star\), as the first clause required.

The locked operationalization of “designs spread” was the two-\(K\) mass floor. It failed. A different spread statistic would be a new prereg, not a rescue of P3. The official 0/3 stands.

---

## What this does and does not establish

Established in-model, in these three Model S worlds, under the locked linear map \(m=-\alpha J\) and haploid Moran search: at high \(\beta\), the modal design is the grid minimum (P1), and the mean excess on a local quadratic chart is consistent with equipartition at \(d=2\) to well inside 20% (P2). Those two gates support the quantitative “low-temperature / predicted lag” reading in `SELECTION.md`.

Not established: the particular low-\(\beta\) spread gate as written (P3). The broader claim that “at low selection strength the mean stays above \(J^\star\)” did hold here; it was not sufficient for a pass.

Nothing here is a field result, and nothing is proved about nature. The official record is FAIL.

World parameters, Hessians, occupation, and exact Boltzmann diagnostics are in `run_t27.json`. No DEVIATIONS file was required: the run followed the prereg.
