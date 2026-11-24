# Deviations

`PREREG.md` and `PREREG.sha256` are unchanged. No prediction, bar, stake list, or ensemble was edited after the run.

## D1. Post-hoc window, not a rescore

The locked run is `record_ratio_reframes_checks.out` (FAILS 4). C1 returned no interior stake and C2 returned one. After that output existed, `posthoc_windows.py` was written to locate the stake band those lists skipped and to repeat the locked inversion inside that band only. Its stdout is `posthoc_windows.out`. It does not change FAILS. It does not replace C1 or C2. The stakes `{0.2, 0.3}` named in `PREREG.md` as the next C1 step were evaluated there and left at the corner; they were not added to the locked list.

## D2. How G5 was scored

`PREREG.md` G5 says the minimized costs differ by \(P_\chi(0)\) within \(10^{-9}\), and the same sentence's parenthesis says the difference is the added coefficient times the constant ledger. Those two descriptions are not the same number. The locked check uses the symbol \(P_\chi(0)\). The parenthesis is printed as `DIAGNOSTIC` and is not a locked check. The sentence was not rewritten.

## D3. Post-hoc readout of the repeated-record miss, not a rescore

`PREREG_REPEAT_ASYMPTOTE.md` is unchanged. The locked run is `repeat_asymptote_checks.out` (FAILS 2). R-low and R-high miss. After that output existed, `repeated` was evaluated at \(n=256\) on \(\theta=0\), \(\pi/4\), \(\pi/2\), and on the two reported minimizers \(1.468258\) and \(1.005746\), to see which term carries the cost. This readout does not change FAILS and does not replace R-low or R-high.

At \(\theta=0\), \(I=1.039720\) and \(L=0\). At \(\pi/4\), \(I=1.038833\) and \(L=0.000085\). At \(\pi/2\), \(I=0\) and \(L=0.180000\). At \(1.468258\), \(I=0.196942\) and \(L=0.120771\). At \(1.005746\), \(I=1.022569\) and \(L=0.001689\). With \(q=0\), the \(w=4\) minimizer costs \(0.680025\), against \(0.720000\) at the equator and \(1.039720\) at the pointer. The \(w=10\) minimizer costs \(1.039458\), against \(1.039720\) at the pointer.

## D4. Q-coh used the dephased diagonal, not the named projectors

`PREREG_QUANTUM.md` is unchanged. The coherent block is the review instrument, projectors \(|0\rangle\langle 0|\) and \(|1\rangle\langle 1|+|2\rangle\langle 2|\), on the state with off-diagonal \(1/8\) inside that block. Those projectors fix the state, so \(P_D=0\) and the costs at \(q=0\) and \(q=1\) agree. The prediction \(P_D>0.01\) fails.

The run stored at `00e8dfa` did not apply those projectors. It subtracted the entropy of eigenvalues \((1/2,1/4,1/4)\) from the entropy of \((1/2,3/8,1/8)\) and printed `Q-coh PASS PD=0.065406 cost_gap=0.065406`, with `FAILS 1`. That number is the gap to the fully dephased diagonal. It is not the disturbance of the locked instrument. This commit replaces `quantum_record_checks.out`. The corrected line is `Q-coh FAIL PD=0.000000 cost_gap=0.000000`, and the file ends `FAILS 2`. No prediction was edited.
