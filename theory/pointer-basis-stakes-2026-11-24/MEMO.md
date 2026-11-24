# T73: a stake on a dephased qubit, and the record basis

*Tuesday 24 November 2026. Self-check, not an independent review. Preregistered in `PREREG.md` (commit `6418237`, 2026-11-24 05:19:13 +0000) before this derivation. Run gate `RUN_LOG.md` (commit `bfd88ab`). `THEORY.md` is unchanged. The qubit and the dephasing channel are inputs. Nothing here derives general relativity, quantum mechanics, or holography.*

## Why this approach

Theorem R1 fixes Shannon mutual information for a classical record and does not fix a quantum record price (`CORE.md:52`). A8, in that same sentence, only requires the price to be nonnegative. The predictability sieve picks states by entropy production, with no stake (Zurek, *Progress of Theoretical Physics* 89:281, 1993, doi `10.1143/ptp/89.2.281`). Quantum Darwinism says the redundant classical record is the pointer record, again with no stake in the sum (Zurek, *Nature Physics* 5:181, 2009, doi `10.1038/nphys1202`). The cheapest question is whether putting a stake into \(J=P+wL\) moves the record basis, and whether the answer depends on which nonnegative \(P\) is used. The duel priced the quantum record by Holevo \(\chi\) (`duel/PREREG.md:27` on `ace-probe-memos-2026-11-23` at `e3e0e70`). This note prices the pinch by its relative entropy, \(P_D\), and scores Holevo \(P_\chi=I(W;M)\) beside it (`PREREG.md:30`, `PREREG.md:38`). PRL 70:1187 is Zurek, Habib, and Paz, "Coherent states via decoherence" (doi `10.1103/PhysRevLett.70.1187`), the minimal-entropy criterion, not the paper that names the sieve (`PREREG.md:124`). This is not the record-count headwind at `WALLS_REVIEW.md:65` on that branch: dimension is fixed at one qubit.

The excluded comparison is not scored. At Bloch radius \(0.6\), the relative entropy of a right-angle Bloch rotation is \(0.415888308336\) and \(r^2=0.360000000000\) (`pointer_basis_stakes_checks.out:2`). The stated \(0.416\) is that relative entropy at three decimals.

## Results

Class PB, \(r=0.6\), grid as locked. Complete dephasing is \(\gamma=0\). Partial is \(\gamma=1/2\). \(\theta=0\) is the dephasing axis. \(\phi=0\) is \(\sigma_z\). \(\phi=\pi/2\) is \(\sigma_x\).

| Slice | Price | Minimizer | Reading |
|---|---|---|---|
| \(\gamma=0\), every \(\phi\), every \(w\) | \(P_D\) | \(\theta=0\), unique | **PROVED (in-model).** Relabel of the sieve on this slice |
| \(\gamma=0\), \(\phi=0\) or \(\pi/4\) | \(P_\chi\) | \(\pi/2\) for \(w\le 1\); \(0\) for \(w\ge 10\) | **PROVED (in-model).** Not the sieve at low stake |
| \(\gamma=0\), \(\phi=\pi/2\) | \(P_\chi\) | \(\pi/2\) at every \(w\), through \(w=100\) | **PROVED (in-model).** `pointer_basis_stakes_checks.out:34`–`:39` |
| \(\gamma=1/2\), \(\phi=0\), every \(w\) | \(P_D\) | \(\theta=0\) | **NUMERICAL.** Commuting stake does not move it |
| \(\gamma=1/2\), \(\phi=\pi/4\) | \(P_D\) | \(0\) at \(w=0\); \(0.449422\) at \(w=100\); cost gap \(3.89538721\times 10^{-1}\) | **NUMERICAL.** Stake moves \(\theta\). `pointer_basis_stakes_checks.out:57`, `:77` |
| \(\gamma=1/2\), \(\phi=\pi/2\) | \(P_D\) | \(0\) through \(w=1\); \(\pi/2\) at \(w=10\) and \(w=100\) | **NUMERICAL.** `pointer_basis_stakes_checks.out:68` |
| \(\gamma=1/2\), \(\phi=\pi/4\) | \(P_\chi\) | \(\pi/2\) at \(w=0\); \(0.479966\) at \(w=100\) | **NUMERICAL.** Also moves. `:81` |
| Locked headline | both | (A) flips across prices; (B) does not | **PRICING_ARTIFACT** |

Closed form against the grid at \(\gamma=0\): max absolute error \(5.551\times 10^{-17}\) (`pointer_basis_stakes_checks.out:3`). Checks C0–C7 pass, `FAILS 0` (`:76`–`:85`).

### Complete dephasing, from the closed form

`PREREG.md:64` and `pointer_basis_stakes_checks.py:70`. For \(r\in(0,1)\), \(h((1+u)/2)\) is strictly decreasing in \(u\in[0,1]\), so \(P_D\) is strictly increasing on \([0,\pi/2]\) and zero only at \(\theta=0\). The loss satisfies \(L(\theta)-L(0)=(r^4\cos^2\phi/4)\sin^2\theta\ge 0\). Hence
\[
J_D(\theta)-J_D(0)=P_D(\theta)+w\big(L(\theta)-L(0)\big)>0
\]
for every \(\theta\in(0,\pi/2]\), every \(w\ge 0\), and every \(\phi\). The unique minimizer is the sieve basis. A stake scales the loss and does not move \(\theta\).

\(P_\chi\) is the same binary entropy with the opposite sign, so it is largest at \(\theta=0\) and zero at \(\theta=\pi/2\). The endpoint gap is
\[
J_\chi(0)-J_\chi(\pi/2)=P_\chi(0)-w\,r^4\cos^2\phi/4,
\]
with \(P_\chi(0)=0.096372378511\). The sieve endpoint wins only for \(w>2.974456126879\) at \(\phi=0\) and \(w>5.948912253758\) at \(\phi=\pi/4\). At \(\phi=\pi/2\) the gap equals \(P_\chi(0)>0\) at every \(w\), so \(\theta=\pi/2\) is strictly cheaper (at \(w=100\), \(J=18\) against \(J(0)=18.09637238\), `:39`). The grid sits on the predicted side of both thresholds (`:10`–`:15`). Predicate (A), "\(\theta=0\) for every stake at complete dephasing," is true for \(P_D\) and false for \(P_\chi\).

### Partial dephasing

At \(\gamma=0\) the formulas already forbid a move under \(P_D\), so a grid is informative only for \(\gamma>0\), where \(P_D\) and \(L\) need not share a minimizer. That grid is the scored run. Under \(P_D\), a commuting stake stays at \(0\) (`:78`). A stake at \(\pi/4\) moves from \(0\) to \(0.449422\) between \(w=0\) and \(w=100\), past the \(0.2\) rad bar, with cost gap \(0.389538721\) (`:77`). The first visible step, \(0.008727\) at \(w=0.1\) (`:54`), is below that bar. Holevo on the same slice also moves, from \(\pi/2\) to \(0.479966\) (`:81`). The tilt boolean does not flip. The always-sieve boolean does.

## Conclusions

**Result.** The locked headline is `PRICING_ARTIFACT` (`PREREG.md:92`, `pointer_basis_stakes_checks.py:217`, `pointer_basis_stakes_checks.out:83`). On this ensemble the answer to "is the best basis the sieve basis for every stake?" is yes under the relative-entropy price at complete dephasing, and no under Holevo \(\chi\). That is the failure mode the preregistration named. It is not a price-independent consequence of the cost.

**Model implication.** Conditional on \(P_D\): once dephasing is complete, the cost-minimizing record basis is the dephasing axis for every stake on this grid, a relabel of the sieve; a stake moves \(\theta\) only while a transverse component survives, and only if the staked observable does not commute with the axis. That sentence is the modeling choice. R1 does not force it. A8 does not either: both prices are nonnegative, and they disagree.

**Puzzle.** \(P_D\) charges the disturbance of writing the record. \(P_\chi\) charges the information the classical outcome holds. Complete dephasing makes the least disturbing basis and the most informative basis the same axis, so one price stays there for every stake and the other leaves as soon as the information costs more than the loss it saves. Which of those two costs is the memory coordinate is not fixed. The next piece of work is an argument that picks one quantum price, not a larger grid.

**Conjecture, not a result.** If the quantum record price is fixed as the entropy production of the record-making map, complete pure dephasing keeps the sieve basis for every stake. Holevo \(\chi\), the price the duel used, does not say that. Quantum Darwinism's redundancy plateau was not computed here, and this grid does not extend it.

## Deviations

The preregistration reserved open-work id T70 (`PREREG.md:5`) because each open fork branch then printed a T69 row and none printed a higher id. Those four questions are assigned T69 through T72: layer fixed point, constants as exchange rates, information causality, composite records. This row is **T73**. The model, the grid, the prices, the predictions, and the headline rule are unchanged. `PREREG.md:107` named the pass line `ALL T70 CHECKS PASS`. The script prints `ALL T73 CHECKS PASS` (`pointer_basis_stakes_checks.out:85`). Same checks, corrected id.

No other deviation. The criteria were not edited after `6418237`. The scratch named in `PREREG.md` §5.3 was not kept and is not a number above.
