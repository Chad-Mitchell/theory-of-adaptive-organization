# Deviations

`PREREG.md` and `PREREG.sha256` are unchanged. No prediction, bar, stake list, or ensemble was edited after the run.

## D1. Post-hoc window, not a rescore

The locked run is `record_ratio_reframes_checks.out` (FAILS 4). C1 returned no interior stake and C2 returned one. After that output existed, `posthoc_windows.py` was written to locate the stake band those lists skipped and to repeat the locked inversion inside that band only. Its stdout is `posthoc_windows.out`. It does not change FAILS. It does not replace C1 or C2. The stakes `{0.2, 0.3}` named in `PREREG.md` as the next C1 step were evaluated there and left at the corner; they were not added to the locked list.

## D2. How G5 was scored

`PREREG.md` G5 says the minimized costs differ by \(P_\chi(0)\) within \(10^{-9}\), and the same sentence's parenthesis says the difference is the added coefficient times the constant ledger. Those two descriptions are not the same number. The locked check uses the symbol \(P_\chi(0)\). The parenthesis is printed as `DIAGNOSTIC` and is not a locked check. The sentence was not rewritten.
