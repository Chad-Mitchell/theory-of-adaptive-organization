# Deviations: T27 thermodynamic / selection bridge, 21 November 2026

These are post-result housekeeping notes. They do not change any official number, gate, or locked file. The official record remains **FAILED** (P1 PASS 3/3, P2 PASS 3/3, P3 FAIL 0/3). `PREREG.md`, `predictions.json`, `LOCK.txt`, and the official `run_t27.json` / `run_t27.log` bytes are not edited.

## Committed runner and library hashes

Recorded from the files on this branch after the official run (the library hash is the post-rewrite committed file; see D1):

| File | SHA-256 |
|---|---|
| `run_t27.py` | `26039b3c81862f36e01ac516d17aa91ab6fd50e4b36cebfd0aafeaa0ccbdb19a` |
| `bridge_lib.py` | `4e779b3dd4754dfa29a4ef74836a8986837f31a92c55601ae32579911e4b8fd2` |

The locked prereg and predictions hashes, unchanged, remain those in `LOCK.txt`:

| File | SHA-256 |
|---|---|
| `PREREG.md` | `25955df4ffb825254100568c9b9d1e751b9d5e0e533146a5d438414c8d5ba994` |
| `predictions.json` | `6715777ca45d02ad443a3e5003f19849331a9e60dba900aa6f6c68c93e7adfe3` |

### Standing rule (future tests)

Future tests must hash-lock the runner and the library at lock time, the same way the prereg and the predictions are locked: write their SHA-256 into `LOCK.txt` (or an equivalent lock record) before any official world is evaluated, and do not edit those files during the official run. A mid-run rewrite of library code, even one that is numerically equivalent, is a protocol lapse.

## D1 (during the official run): mid-run rewrite of `moran_fixation`

This is a protocol lapse. It is stated plainly. It is not a rule change, and it is not a rescoring.

**Times (America/New_York, EST, UTC−5):**

- Lock (`LOCK.txt`): Saturday 21 November 2026, 12:05:31 AM EST.
- Official run start (`run_t27.log` birth): 12:05:33 AM EST.
- `bridge_lib.py` rewrite written to disk: 12:06:26 AM EST (mtime), about 53 seconds after the official process started and while it was still running.
- Official finish (`run_t27.json` / log): 12:07:41 AM EST (127.2 s wall clock).

**What changed.** During the official run, `moran_fixation` in `bridge_lib.py` was rewritten from a form that computed `gN = gamma ** N_pop` (which overflows for deleterious mutants at \(N=201\)) to a log-stable form that uses `N log γ` and never raises `gamma ** N` to overflow. The identity \((1-\gamma)/(1-\gamma^N)\) is unchanged. The official log records the overflow on the first official world, at the pre-rewrite line 180:

```
bridge_lib.py:180: RuntimeWarning: overflow encountered in scalar power
  gN = gamma ** N_pop
```

The warning fired during official seed 2026112100 (the first world finished at 42.4 s, about 12:06:15 AM EST, shortly before the rewrite landed on disk). The official Python process had already imported the pre-rewrite function at start; the disk rewrite did not change the in-memory code. All three official worlds were therefore scored with the overflowing formula.

The pre-rewrite function was:

```python
def moran_fixation(r_mut, r_wt, N_pop):
    if r_mut <= 0 or r_wt <= 0 or not np.isfinite(r_mut) or not np.isfinite(r_wt):
        return 0.0
    if abs(r_mut - r_wt) < 1e-15 * max(r_mut, r_wt):
        return 1.0 / N_pop
    gamma = r_wt / r_mut
    gN = gamma ** N_pop
    if abs(1.0 - gN) < 1e-18:
        return 1.0 / N_pop
    return float((1.0 - gamma) / (1.0 - gN))
```

The committed function uses logs: `nlog = N_pop * log(γ)`; if `nlog > 700` it returns 0; if `nlog < -700` it returns \(1-\gamma\); otherwise it evaluates the same identity in a stable way. See `bridge_lib.py` as committed.

**Why the two formulas are numerically equivalent.** When \(\gamma>1\) and \(\gamma^N\) overflows to \(+\infty\) (the deleterious limit at \(N=201\)), the old expression evaluates to \((1-\gamma)/(1-\infty)=0\), which is the correct fixation probability in that limit. The committed rewrite returns 0 when \(N\log\gamma>700\), the same limit. When \(\gamma^N\) underflows, both recover \(1-\gamma\). A direct comparison of the two formulas at \(N=201\) on a 2,001-point log-\(\gamma\) grid (\(\log\gamma\in[-20,20]\)) and on 5,000 random birth-rate pairs agreed to machine precision (maximum absolute difference \(1.7\times 10^{-15}\)).

**Committed-code re-run.** On Saturday 21 November 2026, starting at 12:27:51 AM EST, the committed runner `run_t27.py` (hash above) was re-run at `nice 19` against the committed library (hash above), with the official `run_t27.json` and `run_t27.log` copied aside and later restored byte-for-byte. The re-run finished in 123.841 s. Its JSON matched the official `run_t27.json` exactly except for the wall-clock `seconds` fields (official total 127.169 s; per-world official 42.437 / 42.158 / 42.572 s; re-run 41.327 / 41.337 / 41.175 s). Every seed, validity flag, gate, occupation mass, \(\beta\)-excess, and exact-Boltzmann diagnostic was identical. The official JSON bytes (SHA-256 `daf2ac2d446a457a74e14c555db3fe689561c54c7871d4086b6f0e3c5919927a`) were restored after the comparison.

This confirms that the mid-run rewrite did not change the official numbers. It does not excuse the lapse: the library on disk at lock time is not the library that was later committed, and a hash-lock of the runner and library at 12:05:31 AM EST would have made that visible immediately.

## D2 (documented only): PREREG header day mismatch

**Time of the mismatch.** The locked `PREREG.md` header says “Friday 20 November 2026, late evening ET.” The lock timestamp in `LOCK.txt` is Saturday 21 November 2026, 12:05:31 AM EST. The body of the prereg was written Friday evening and the lock crossed midnight.

The locked `PREREG.md` is not edited. This note records the mismatch only.
