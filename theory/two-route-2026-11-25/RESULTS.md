# Results ledger: two-route prereg

**Lock reference:** `theory/two-route-2026-11-25/PREREG.md`, sha256 `9e42fe0a581a271f5c09a6dd7064304f8aaab43dd21ed7d509feaad13cd29e54`, lock commit `b159d0f`  
**Logged at (ET):** 2026-11-25 09:05 ET  
**Breach check:** `none` (the prereg hashes to its lock value; no prediction was edited; no data was used)

Rows are added as bars are scored. Bars not listed (A-C3, A-T1, A-T3, all of Route B) are not scored yet.

| prediction_id | locked_prediction (value/band; odds if feasible) | outcome | miss (signed size & direction, or HIT + info) | location | stake_x_info | update | breach_check |
|---|---|---|---|---|---|---|---|
| A-C1 (CONSISTENCY_CHECK) | At \(g=0\) the world-bath heat is 0 at every memory design (T61 passive plant) | max \(|\dot Q_X|=0\) over 9 designs | HIT, information about 0 (identity) | model | low | none | none |
| A-C2 (CONSISTENCY_CHECK) | Stability determinant of W2 is \(a\gamma(1-gc)\) (F3 input) | \(\det A=a\gamma(1-gc)\) by inspection of the drift matrix in `checks/route_a_w2.py` | HIT, information about 0 (identity) | model | low | none | none |
| A-T2 | \(\rho=\dot Q_M^*(0.5)/\dot Q_M^*(0)\le0.9\); RI predicts \(\rho=1\); odds of a miss 0.5 | \(\rho=1.0453\) (\(\dot Q_M^*=2.2042\) at \(g=0.5\), \(2.1086\) at \(g=0\)); tolerance check 1.0453 | **miss, \(+0.145\)** (memory heat rises with the world's copy gain instead of falling). RI's value 1 is also off, by \(+0.045\), smaller than the locked bar's error | model (no MV gate or bug fired; JP-heat \(\dot Q_M\ge kT_M l_M\) held at 2,000 random designs; A-C1 held) | medium | none yet (open miss, `CORE.md:169`) | none |

## A-T2, scaled write-up (medium)

1. **Prediction and risk.** Locked: a world that copies the memory (gain \(g=0.5\)) lowers the optimal memory heat by at least 10% at \(w=10\). RI, which treats the world as exogenous, predicts no change. Odds of a miss were set at 0.5.
2. **Miss and location.** \(\rho-0.9=+0.145\), location `model`. The cost does fall with \(g\) (\(J^*=6.281\) at \(g=0\), \(6.052\) at \(0.5\), \(5.851\) at \(0.9\)), but not through the memory bath: the world-bath heat turns negative (\(\dot Q_X^*=-0.278\) at \(g=0.5\)), the memory relaxes more slowly and copies more (\(\gamma^*\) 6.88 to 5.24, \(c^*\) 0.59 to 0.76), and the memory heat rises by 4.5%. The learning rate barely moves (1.453 to 1.448). Total heat stays positive (1.926 at \(g=0.5\)), as the second law requires at equal temperatures. All numbers: `checks/route_a_w2.out`.
3. **Update.** None yet. Diagnosis: in W2 the responding world's gain shows up as a shift of heat between the two baths, not as a free ride on the memory's heat, and RI's exogenous reading is closer than the locked bar (+0.045 against +0.145). Next test: A-T1 asks whether the two-bath account and the design-level chain are one object; the sign of \(\dot Q_X^*\) is the cross term the two-one-way null sets to 0, and it is not 0 here (reported, not a scored bar). Per the prereg's G5, the free-ride line stops here.
