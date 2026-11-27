
## 10. Pre-statement: the CT9 read-price arm (SH-read) and the w-reduction claim (W) (written 26 Nov 2026 before any SH-read number is computed; §§0–9 stand as written)

*The SHA-256 of this block, from the "## 10." heading line through the end of §10.9, is logged in WORKLOG.md with the clock time before any computing. Nothing in §10 may be edited afterwards. Results go in §11.*

### 10.1 Model (as §8.2, with one change to the check mode)

- **Check cost per tick, in CT9's form** (THEORY.md:311, J(s) = λc/s + A(s)), keeping §8's Landauer restore term:
  J_chk(s) = [y + H(K_s) + x·Σ_{u=0}^{s−1} ε(u)]/s,
  - y := c/kT, the read price per check;
  - x := w/kT, the stake;
  - H, ε as §8.2;
  - s* := the integer argmin over 1 ≤ s ≤ 20000.
- **Keep and fade:** as §8.2 (c_K = 2; arm c_K = 4 not run here).
- **Disk:** fades, τ = 1, vacuous (PIM, §8.2).
- **Mode:** the cheapest per tick. On a tie, the shorter lifetime.
- **Grids.**
  - σ: §6.4's 14 values.
  - x ∈ {0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1}.
  - y ∈ {0.1, 1, 10}.
- **Edge rule.** If s* = 20000, then T ≥ 20000 > π²/(4·d_min(n)) for every n ≤ 1201 (π²/(4·d_min) < 950 there). The design is then excluded by SR-b1(f) (PIM), provided J_chk is still decreasing at s = 20000. That condition is checked and reported; where it fails, the design is OPEN.

### 10.2 Two horizon readings (both scored)

- **(W) one written state's life:** τ = s* for check, ∞ for keep, 1/p_n for fade.
- **(I) the information's life:** τ = ∞ for check and keep, 1/p_n for fade.
  - Paper (PIM): under (I) the self-consistent set is contained in §7.3's primary set restricted to fading designs. Its score is therefore expected to be MISS wherever §7.3 has no fixed point, which is 12–13 of 14 σ per configuration.

### 10.3 Fixed-point rule, slope test, cells

- **As in §8.3 and §8.5:** T = ⌊τ⌋, primary; ⌈τ⌉ is an arm. A(T) is from §7.1 (T ≤ 400). Designs with 400 < T < ∞ are excluded if T > π²/(4·d_min), and OPEN otherwise.
- **Kept designs** are excluded (PIM).
- **Configurations:** E-M3h, O, F-M3h and F-mixed are scored; E-mixed is reported only.
- **Slope.** The slope at a unique fixed point n* uses its two menu neighbours where both have finite Φ.
  - **New, to close §9.3's gap:** if only one neighbour has finite Φ, use the one-sided slope. If neither does, the cell is **EDGE**.
- **Cell status:**
  - **HIT:** exactly one self-consistent polygon; no 2-cycle; disk not self-consistent; |slope| < 1; and every orbit of Φ (60 steps) that stays finite ends at n*.
  - **MISS:** none, two or more, a 2-cycle, or |slope| > 1 at the unique fixed point.
  - **EDGE:** as above; not a HIT and not a MISS.
  - **OPEN:** by the range or edge rules.
- **Per (x, y):** MISS if any cell is a MISS; HIT if all are HITs; otherwise OPEN.
- **Score per reading: HIT iff HIT at every (x, y); MISS iff MISS at some (x, y); OPEN otherwise.**

### 10.4 The key question: noise or stake (measured on every cell, HIT or not)

- **Crossing.** n_c(σ, x, y) is the first sign change of Φ(n) − n over consecutive menu members with finite Φ, ascending (midpoint). The slope across it is s_c.
- **Elasticities**, by least squares over the grid where n_c exists:
  - β := −d ln n_c/d ln σ at fixed (x, y);
  - e_x := d ln n_c/d ln x at fixed (σ, y);
  - e_y := d ln n_c/d ln y at fixed (σ, x).
- **Reading:**
  - **"set by noise":** β ∈ [0.8, 1.3] and |e_x|, |e_y| ≤ 0.25;
  - **"set by stake":** |e_x + 1| ≤ 0.25 and β ≤ 0.25 (§9's pattern was e_x = −1, β = 0);
  - **"mixed":** anything else, with the numbers reported.
- **Overshoot back** iff the median |s_c| over cells where n_c exists is > 1.
- **Paper prediction (§9.9).** n_c solves erfc(π/(√2·nσ)) ≈ 8y/(x·n²), so n_c ≈ (π/σ)/√(2 ln(x·n_c²/(8y))): **set by noise**, with x and y entering only through a logarithm (|e_x| ≈ |e_y| ≈ 1/(2a²) ≈ 0.1–0.25). Expected |s_c| ≈ a² ≈ 2–6: **overshoot back.**
  - P(MISS under (W)) ≈ 0.85. P(overshoot back) ≈ 0.8. P("set by noise") ≈ 0.6, P("mixed") ≈ 0.35, P("set by stake") ≈ 0.05.

### 10.5 Triviality test for SH-read (stated now)

- **Trivial ("resolution ≈ noise"):** "set by noise", with n_c·σ·√(2 ln(1/σ)) constant within a factor 1.5 over σ at each (x, y).
- **Trivial ("stake relabelling"):** "set by stake".
- **Genuine** iff some HIT cell exists with |s_c| < 1 whose n* is neither within a factor 1.5 of 4/(σ√(2 ln(1/σ))) nor within a factor 1.5 of 4/x + 2.

### 10.6 Structural claim W (a HYPOTHESIS, stated before its test)

- **Claim W.** Across SR-b4, SH1, SH-noise and SH-heat (§§6–9; SR_B §9), **every free input reduces to the single stake w** of CORE.md:23 (J = Q̇ + w·E[ℓ]; "w converts the loss into the currency of the heat. Temperature does not set w.").
- **"Reduces"** means: with the other inputs at their scored values, the outcome depends on that input only through a function of w (or of x = w/kT).
- **Test, one row per input.** Classify each input as one of:
  - **(R) reduces:** a derivation or computation shows the outcome depends on it only through w;
  - **(F) fails:** two values of the input at the same w give different outcomes, labelled by how that difference is established (PIM or OBSERVED);
  - **(V) vacuous:** it cancels.
- **Claim W holds iff no row is (F).**
- **Inputs and predicted rows** (written now; the test fills in the evidence in §11):
  1. Horizon T (SR-b1/b3; SH-noise via τ). Predicted: (R) only in §9's check band, where T = ⌊2/x⌋, and conditionally (H1 and H2 of §9.6). Elsewhere T comes from σ.
  2. Horizon weighting and its cap H (SR-b4's R_H; SR-b's geometric q). Predicted: (F). SR-b4 is pointwise dominance at every bounded H, and w does not enter J.
  3. Quantifier order, design before horizon scale ((F) vs (P), SR_B §8–§9). Predicted: (F). A logical structure, not a price.
  4. Target rule, M3h versus antipode. Predicted: (F), PIM by §7.2 against SR-b3.
  5. Design menu (even, odd, all). Predicted: (F).
  6. Cost exponent, c·d² versus c·d (ROUND10 §14: "With a linear price c·d the ranking reverses"). Predicted: (F).
  7. The price κ per affine dimension. Predicted: (V), since it cancels (SR_B §1).
  8. Noise σ. Predicted: (F). §9.2's edge n_b is nearly x-free.
  9. Lifetime definition (first confusion versus level δ). Predicted: (F), from §7.5.
  10. Rounding ⌊ ⌋ versus ⌈ ⌉. Predicted: (F), from §7.3's ceil rows.
  11. Keep constant c_K (2 versus 4; carrier class). Predicted: (F), from §9.3.
  12. Read price c (this unit). Predicted: (F) unless c sits at its thermodynamic floor, in which case c ∝ kT and x is the only ratio. Tested by comparing cells at equal x/y.
  13. Horizon reading (W) versus (I). Predicted: (F).
  14. Temperature kT. Predicted: (R), trivially, since it is the unit in x = w/kT.
- **Prior:** P(Claim W holds) ≈ 0.03.

### 10.7 Tools and checks planned

- `selfhorizon/sh_read_run.py`, reusing `sh_heat_core.Rec` with the read price added and SMAX = 20000, run detached with a log. `sh_read_analyse.py` does the analysis.
- **Checks:**
  - (a) a full integer scan s ≤ 20000 for n ≤ 31 against the grid search;
  - (b) J_chk decreasing at s = 20000 wherever s* = 20000;
  - (c) at y = 0, s* equals §9's (regression).

### 10.8 Labels planned

- Cells, crossings and elasticities: OBSERVED.
- The (I)-reading containment, the kept-design and edge-rule exclusions: PIM.
- Claim W's rows: labelled one by one.

### 10.9 Not tested here

- The interruptible reading.
- The heat in J (§7.10).
- The level arm for the check mode.
- c_K = 4.
