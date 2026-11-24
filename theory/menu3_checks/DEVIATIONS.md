# Deviations, tilted menu

`theory/PREREG_3.md` is not edited. `decisions.out` is not edited. Logged after `theory/reviews/COMPOSITE_CONTEST_REVIEW_2_2026-11-24.md` (commit `4f04415`).

- **D1.** The official rebit loss is the minimum over 243 single readouts (`PREREG_3.md:51`). A shared classical bit is outside that list. On the real singlet, weight `√(2/3)` on the sharp `xz` projections and the rest on `y → +I` on one wing and `−I` on the other: mean loss `2.3045076783754708e-32`. One averaged readout gives `3.5918405131962310e-03`. `PREREG.md:55` does not grant the bit. Charged, `K = 20`. Uncharged, the same behavior sits at `K = 10`. The label is DEPENDS ON PRICING SHARED RANDOMNESS, not WIN.
- **D2.** Inside the implemented list the positive-price WIN is the count `16 < 17 < 36` after the `ε = 0` gate (`run_menu3.py:314`). The loss `0.00215` is a gate, not a term in `J`.
- **D3.** G's loss is C's loss (`run_menu3.py:300`). No holistic coordinate is built.
- **D4.** The odd-momentum witness returns `0.5 * ((-1)·1 + 1·(-1))`, which is `−1` (`run_menu3.py:240`). It is not computed from a phase-space model.
- **D5.** Gmin and Gmax are one function, `product_loss` (`run_menu3.py:194`, `:298`).
- **D6.** `I_A6` and Holevo are the constants 0 (`run_menu3.py:302`). Every feasible information cost is then 0 (`:346`). The TIE is that identity, not a computed mutual information.
- **D7.** `PREREG_3.md:29` leaves the smallest singular value as `(√3 − √(4/3)?)`. The printed value is `3.3673504811214609e-02`. The formula is unfinished.
