# Independent review: Theorem P for drifting worlds

Reviewed head `12cf955` on `theorem-p-drift-2026-11-21`, against `c92886a` (draft PR #149). 22 November 2026. The note is a self-check; this file is the independent check. The only edit is this file.

## Verdict

**READY-WITH-FIXES.**

PD1a, the PD5 closed form, its continuous-time limit, PD1b’s algebra, PD7’s sampled limit, and PD6’s Gaussian stock divergence all rederive. CX1 should stay **OPEN**. One proved sentence is false outside the linear class (blocker 1). The open-work summary overstates what that divergence requires of the master equation (should-fix 1).

## Rederivations that hold

### PD1a

`r_t = I(X_t; M_t | M^{t-1})` is a per-step conditional mutual information (nats). It is at most the directed-information increment `I(X^t; M_t | M^{t-1})`, because `h(M_t | X^t, M^{t-1}) ≤ h(M_t | X_t, M^{t-1})`. Every floor written in `\bar r` remains a floor if `\bar r` is replaced by the directed-information rate: that rate is at least `\bar r`, and the floor falls as the rate rises.

The proof uses four steps, and none of them needs Gaussian shocks or a Markov world.

1. PD-A at time `t−1`: given `X^{t-1}`, `M^{t-1}` is independent of `X_t`, so `h(X_t | X^{t-1}, M^{t-1}) = h(X_t | X^{t-1})`. Conditioning then gives `h(X_t | M^{t-1}) ≥ h(X_t | X^{t-1}) ≥ h_inn`. The past in that identity is the whole past, so a non-Markov world (fBm included) is covered.
2. Chain rule: `h(X_t | M^t) = h(X_t | M^{t-1}) − r_t ≥ h_inn − r_t`, whenever the conditional entropies are finite. A joint density plus PD-B is what the note assumes. If the innovation entropy is `+∞`, the entropy power is infinite and finite MSE is already impossible by the maximum-entropy bound, so the floor is the right triviality.
3. L1 is the Shannon lower bound. It holds for any density: `h(X | M) = h(X − f(M) | M) ≤ h(X − f(M)) ≤ (n/2) log(2πe E‖error‖² / n)`. Equality needs a Gaussian error. The inequality direction is what PD1a uses.
4. `e^{−2r/n}` is convex, so the time average of the error is at least `n N_inn exp(−2 R_T / n)`, where `R_T` is the average of `r_t`. With `\bar r = limsup R_T`, every large `T` has `R_T ≤ \bar r + ε`, and the liminf of the average error is at least `n N_inn e^{−2\bar r/n}`. The limsup is the aggregate that makes this true.

L2, the conditional EPI, is used only in PD1(b). The conditional form is valid: Stam’s EPI at each value of `M`, then Jensen on `s ↦ (n/2) log(e^{2s/n} + e^{2h(W)/n})`, which is convex. The fixed point `N^*(r) = N_W e^{−2r/n} / (1 − α e^{−2r/n})` matches the rate display in §0, the scalar form `D ≥ q / (e^{2r} − a²)`, and the Kalman identity `e^{2r} = a² + q/P`. The threshold `r ≤ log|det A|` is weaker than the data-rate theorem when `A` has stable eigenvalues. The note says so. The bound stays a lower bound there; it does not claim achievability.

### PD5 closed form and the continuous limit

For the scalar random walk, minimize `wq / (e^{2r} − 1) + c r`. Set `z = e^{2r}` and `x = wq/c`. The critical-point equation is `2 w q z = c (z − 1)²`, hence `z² − 2(1+x) z + 1 = 0`, hence

`z = 1 + x ± √(x² + 2x)`.

The root above 1 is `1 + x + √(x² + 2x)`. The minus root lies in `(0, 1)`. Both ends `r ↓ 0` and `r → ∞` send the cost to infinity, so the critical point is the minimum. Residuals of the first-order equation on the note’s four price settings are at most about `10^{−14}`. The Kalman filter with a Gaussian read meets `D = q / (e^{2r} − 1)` at every `r > 0`, so the bound is attained.

Continuous-time accounting that matches the code and CT7: one step of length `dt` has innovation variance `q = σ² dt` and inflow `r = ρ dt`. The mean squared error tends to `σ² / (2ρ)`. The cost **per unit time** is `w D + c ρ`, because `c` prices the `ρ dt` nats of that step. Minimizing gives `ρ = σ √(w / (2c))` and

`J^* = σ √(2 w c)`,

at `D^* = σ √(c / (2w))`. With `c = kT` this is CT7’s `σ √(2 kT w)` and CT7’s `D^*`. Thermodynamics is the choice `c = kT`. The `\sqrt2` is the informative coefficient, as CT7 already says. The sampled OU expansion `a = e^{−θ dt}`, `q = σ² (1 − a²) / (2θ)` gives `(1/(2 dt)) log(a² + q/D) → σ²/(2D) − θ`. Duncan’s Kalman–Bucy rate `P / (2s)` equals that expression by the Riccati identity. Non-sampled continuous designs are marked SKETCH. That label is accurate.

### PD6

For a Gaussian coordinate with `‖u‖ = 1` and `E‖A_t − X_t‖² ≤ D` at that `t`,

`I(M_t; X_t) ≥ I(M_t; u^⊤ X_t) = h(u^⊤ X_t) − h(u^⊤ X_t | M_t) ≥ (1/2) log(Var(u^⊤ X_t) / D)`.

Data processing gives the first step. The entropy of a Gaussian gives the first term. L1 in one dimension, and `(u^⊤ error)² ≤ ‖error‖²`, gives the second. If `Var(u^⊤ X_t) → ∞` and the same finite `D` bounds the mean squared error at every `t`, then `I(M_t; X_t) → ∞` for every such design. The argument does not need PD-A. It does need Gaussianity for the entropy of `X`, which is how PD6 is stated.

Checked edges:

- **Uniform `D`.** The limit holds, including a design whose action is a function of `M` (data processing the other way) and a design that is biased (the second moment dominates the variance).
- **Only a long-run average `D`.** Instantaneous mutual information need not tend to infinity: erasing the memory on a sparse set makes `I = 0` at those instants, and the spikes in error can stay sparse enough that the Cesàro mean of the error stays finite. For a Gaussian random walk the time average of the stock still diverges. The pointwise bound rearranges to `E[(error_t)²] ≥ q t e^{−2 I_t}`, so a bounded average of `I_t` forces the average error to infinity.
- **Stationary OU.** Variance converges to `σ² / (2θ)`, and a steady filter has finite `I(M_t; X_t) = (1/2) log(Var / P)`. One numerical point: `θ = 0.7`, `σ² = 1`, observation intensity `0.5` gives `Var = 0.714`, `P = 0.439`, `I = 0.243` nats, constant. PD6 is scoped to `Var → ∞`. A stationary world keeps the stock finite. A non-stationary world whose variance stays bounded is outside the hypothesis as well.

The Kalman numbers in CE1 are `(1/2) log(t / P)` at the steady posterior `P = (√5 − 1)/2`, with inflow `0.481` nat/step. They match.

## Blockers

1. **`theory/THEOREM_P_DRIFT.md:90` — “every persistent design has `\bar r > 0`” is false for a world that only has `Var(u^⊤ X_t) → ∞`.** The blind half is proved: if `M` is independent of `X` and `‖u‖ = 1`, the mean squared error is at least `Var(u^⊤ X_t)`, which is unbounded, so no finite income covers a blind design. The rate half does not follow. “Not blind” is a statement about `I(M_t; X_t)`, and `\bar r` is the limsup of the average inflow. The proof’s rate sentence cites PD1(b), which is the linear class PD-C. fBm is named in the same sentence and is not in PD-C; a sharp fBm rate is PD8. CLAIM_MAP PD3 (`measurement/CLAIM_MAP_v2.md:618`) already confines the rate claim to the linear tier. The note’s sentence is wider, and the wider sentence is false.

   Counterexample, exogenous and with a density. Let `Z ~ N(0,1)`, `G_t` i.i.d. `N(0,1)`, and `X_t = t Z + G_t`. Then `Var(X_t) = t² + 1 → ∞`, and the one-step innovation variance is at least 1, so PD-B holds with `N_inn ≥ 1`. Observe `Y = X + N(0,1)` only at `t = 2^k`, and between looks act with `A_t = t E[Z | looks so far]`. Through `T = 2^{16}` the mean squared error stays at most `7.00`, the total inflow is `16.8` nats over 17 looks, and the mean inflow is `2.56 × 10^{−4}` nat/step, so `\bar r = 0`. Blind mean squared error at that `T` is `4.29 × 10^9`. The stock still diverges: `I(M_T; X_T) = 10.63` nats. PD1a is untouched, because at `\bar r = 0` it only requires `D ≥ N_inn`. PD1(b) is untouched, because this world is not `X ↦ A X + W` with i.i.d. `W`.

   **Fix.** On line 90, keep the blind-loss sentence. Delete “and every persistent design has `\bar r > 0`” as a consequence of `Var → ∞`. State the rate claim only under PD-C: bounded mean squared error forces `\bar r > log|det A|` (PD1(b)); for a random walk that threshold is 0. Add the construction above as a counterexample, next to CE2, so the retracted sentence stays visible. Leave CLAIM_MAP line 618 as it stands. Line 7’s plain-words rate requirement belongs with the linear display that follows it (nit 1).

## Should-fixes

1. **`OPEN_WORK.md:58` — “so κ must price a flow” is stronger than PD6 and stronger than the mathematics.** PD6 and CLAIM_MAP PD6 (`measurement/CLAIM_MAP_v2.md:621`) say a flow **or** a renormalized stock, and they leave the renormalization **OPEN**. The counterexample in blocker 1 has bounded error, `\bar r = 0`, and `I(M_t; X_t) → ∞`. A rule that the information term must be the inflow would price that design at zero inflow while the stock diverges. **Fix.** Use the note’s disjunction: the stationary stock `I(M_t; X_t)` cannot be the viability term; book a flow, as `theory/INTERNAL_MODEL.md:176` and Theorem S1’s `c·r` already do for the random-walk problem, or a renormalized stock, which stays open.

## Nits

1. **`theory/THEOREM_P_DRIFT.md:7`.** “The system has to take in new information at least as fast as the drift wears the old information away” is the linear-shock story. The linear hypothesis is the next sentence. The world in blocker 1 keeps a bounded error with mean inflow going to 0. Attach the rate sentence to that linear display.
2. **`theory/THEOREM_P_DRIFT.md:104–106`.** The limit `min_ρ {w σ²/(2ρ) + c ρ} = σ √(2wc)` is the right continuous cost. The per-step objective is `w D + c r` with `r = ρ dt`, so the cost per unit time is `w D + c ρ`. The code implements this by calling `price_optimum_rw(σ² dt, w, c/dt)` (`tools/theorem_p_drift_checks.py:190`). One clause in the proof should say that. The displayed minimum and the numerical limit (0.7267, 0.7696, 0.7741, 0.7746 → 0.7746) are already right.
3. **`theory/THEOREM_P_DRIFT.md:108`, “it cannot rank designs”.** At each finite `t`, `κ I(M_t; X_t) = (κ/2) log Var(u^⊤ X_t) − (κ/2) log D` for a Gaussian equality case. The first term is common to every uniformly accurate design and diverges. The second term still ranks designs. What fails is comparing the unregularized cost with a finite income. Say that.
4. **`OPEN_WORK.md:58`.** “`D ≥ N_inn e^{−2\bar r}` for any exogenous world” is the scalar floor. The general floor is `D ≥ n N_inn e^{−2\bar r/n}` (`theory/THEOREM_P_DRIFT.md:58`, CLAIM_MAP PD1a).

## Master equation

The master equation does not need a new left-hand side for drifting worlds.

THEORY §3 writes `J = κ I_mem + h K + w E[ℓ] + A + L` (`THEORY.md:26`). `κ` is already a price per nat held per unit time (`THEORY.md:30`), and `I_mem` is “nats held” (`THEORY.md:244`). Theorem S1 instantiates `I_mem = I(M_t; X^t)` under standing assumption A2, joint stationarity (`theory/SHANNON_2026-11-21.md:29`), and it already charges a separate inflow term `A ≥ c·r`. On that domain both terms are finite. CT4’s threshold `κ < 2 ln 2 · a² · Var` is the same stationary stock. CT6’s upkeep inequality is empty for an unconstrained Gaussian kernel (`η = 1`); the note’s replacement by the linear rate is the right scope statement.

For a Gaussian world with `Var(u^⊤ X_t) → ∞` and mean squared error uniformly bounded, PD6 is right: `I(M_t; X_t) → ∞`, so dropping that mutual information into the `I_mem` slot makes the holding-cost **rate** unbounded for every competent design. The divergent piece `(κ/2) log Var(X_t)` does not depend on the design (nit 3). Viability against a finite income fails for the raw stock. Ranking at a fixed time survives in the finite piece `−(κ/2) log D`.

Booking the information price on a rate is already how this repository treats the random-walk problem, and it is consistent with those definitions:

- `theory/INTERNAL_MODEL.md:176` prices each random-walk mode as `κ · ½ log₂(1 + q_i/P_i)` per step. That logarithm is the inflow, not `I(M_t; X_t)`.
- CT7 (`THEORY.md:294`) lower-bounds dissipation by `kT · σ²/(2D)`, the information rate of a Brownian tracker, and minimizes `w D` plus that rate. PD5 recovers the same square root with `c` in place of `kT`.
- Theorem S1’s `c·r` is that rate term. Under A2 it sits beside a finite `κ I_mem`. It does not replace `κ I_mem` inside the stationary theory.

The repair is to stop instantiating `I_mem` as `I(M_t; X_t)` when that mutual information diverges. For the linear random walk, the finite, design-ranking information cost is the inflow (priced as `c·r`, or as `κ` times that rate, which is what §4 of the internal-model note already does). A renormalized stock such as `I(M_t; X_t) − ½ log Var(X_t)` is finite for the Kalman filter and would let `κ` keep a stock reading; which renormalization is the right one is open, and the note says so. Blocker 1’s world shows why “must price a flow” is too strong: the inflow rate can vanish while the raw stock still diverges. Both the flow and a renormalized stock are live options. The equation’s other terms (`h K`, `w E[ℓ]`, `A`, `L`) are untouched.

A stationary world stays on the old definition. For the OU filter above, `I(M_t; X_t)` is a finite constant, and `κ I_mem` still ranks designs. PD6 does not ask for a change on A2.

CX1 should remain **OPEN** (`measurement/CLAIM_MAP_v2.md:506`). The flow forms of CT1–CT4 are proved for the classes named in section T. The stationary stock does not extend. A renormalized stock, a sharp non-Markov floor, almost-sure ruin without ergodicity, and controlled worlds are PD8. That is a partial resolution, which is what the row now says.

## Status, sentence, locks, credit

- CX1’s status cell is still **OPEN**. No existing row changes status. R1 stays **PRIOR ART**; the edit is credit text. New rows: PD1a and PD2–PD6 **PROVED (in-model)**, PD1b and PD7 **PRIOR ART**, PD8 **OPEN**. The tally movement 330 → 339 is `+6` proved, `+2` prior art, `+1` open. `check_consistency.py` counts 339.
- The Part 2 sentence is present once in each of `THEORY.md`, `CORE.md`, `README.md`, and `theory/SELECTION_AXIOMS.md`, and once in each of those files at `c92886a`: `The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`
- The new note’s two uses of “law” are “shock law” (line 7) and “stationary law” (line 92). Neither calls the theory a law. Maintained-doc wording failures: 0.
- `git diff --name-only c92886a HEAD` before this review was 13 paths: `CORE.md`, `OPEN_WORK.md`, `README.md`, `STATUS.md`, `THEORY.md`, `measurement/CLAIM_MAP_v2.md`, `theory/README.md`, `theory/SELECTION_AXIOMS.md`, `theory/THEOREM_P_DRIFT.md`, `theory/theorem_p_drift_checks/results_full.json`, `tools/test_brief.py`, `tools/test_theorem_p_drift_checks.py`, `tools/theorem_p_drift_checks.py`. None is a preregistration, a hash file, a LOCK file, or a file under `tests/`.

R1’s new citations resolve on Crossref (22 November 2026), and the load claims match the texts.

| DOI | Crossref | What was checked in the text |
|---|---|---|
| 10.1023/a:1017071901530 | Hartl & Taubes 1998, *Genetica* 102–103:525–533, “Towards a theory of evolutionary adaptation” | Cited by Tenaillon and by Held as the drift-load paper. Title, year, pages match the note. |
| 10.1111/j.0014-3820.2000.tb00693.x | Poon & Otto 2000, *Evolution* 54:1467–1479, “Compensating for our load of mutations: freezing the meltdown of small populations” | Tenaillon credits them with the linear-fitness approximation `F_eq ≈ 2 N_e / (2 N_e + n_e)` and, with Hartl & Taubes, with the load–complexity link. |
| 10.1371/journal.pone.0000217 | Tenaillon, Silander, Uzan & Chao 2007, *PLoS ONE* 2:e217 | For `f(d) = exp(−d^Q)` they obtain `F_eq = (1 − (2 N_e − 1)^{−1})^{n_e/Q}`, i.e. `(1 − ν^{−1})^{n_e/Q}` at their diploid `ν = 2 N_e − 1`. At `Q = 2`, `−log F_eq ≈ n_e / (2ν)`. They derive it from the Sella–Hirsh weight. |
| 10.1088/1742-5468/2014/09/P09029 | Held, Nourmohammad & Lässig 2014, *J. Stat. Mech.* P09029 | arXiv:1403.1803 states `2 N L_eq ≃ d/2` and cites the same three papers as [42–44], as an equipartition analogue. |

Spot-checks of the control DOIs also resolve to the titles the note uses: Tatikonda, Sahai & Mitter 2004, *IEEE TAC* 49:1549–1561; Kostina & Hassibi 2019, *IEEE TAC* 64:4525–4540; Duncan 1970, *SIAM J. Appl. Math.* 19:215–220; Tatikonda & Mitter 2004, *IEEE TAC* 49:1056–1068; Nair & Evans 2004, *SIAM J. Control Optim.* 43:413–436.

## Commands

All of these were run from the repo root at nice 19, on head `12cf955` plus this review file only after the runs. `scipy`, `numpy`, `sympy`, and `pytest` were installed in the environment so the suite could import; no project file was changed for that.

| Command | Result |
|---|---|
| `python3 tools/check_fresh.py` | PASS. STATUS main is `2eeab30`, inside the origin/main window `2eeab30 c04cedd d34df95 a97887e 0726423`. |
| `python3 tools/check_open_work.py` | PASS. items.json not-DONE 62; QUEUE.md not-DONE 90; missing from OPEN_WORK.md: 0. |
| `python3 tools/check_consistency.py` | PASS. THEORY v2.9; CLAIM_MAP latest note v2.73; pointers agree; wording FAILs 0; section N 63 rows, 0 mismatches; tally 339 = 339; core index 74 = 74; process-rule FAILs 0; core-rule FAILs 0. Length warnings are the pre-existing advisory ones (THEORY main text 10569 words, README 1468). |
| `python3 tools/theorem_p_drift_checks.py` | PASS. `ALL PD CHECKS PASS`. Kalman relative gap `2.23×10^{−15}`. |
| `python3 tools/theorem_p_drift_checks.py --full` | PASS. `ALL PD CHECKS PASS`. Quantizer ratios match the note’s table: random walk 1.75, 2.05, 2.49; `a = 0.9` 1.65, 2.04, 2.41. fBm minima 1.03–1.62. CE1 stocks 1.392, 2.543, 3.694, 4.846; inflow 0.4812. PD5 limit 0.72674, 0.76962, 0.77410, 0.77455 against 0.77460. CE5 ratios 1.2, 5.5, 50.5, 500.5. The rewritten `results_full.json` differed from the committed file only in fBm floats at about `10^{−15}` (last-bit noise). That file was restored; it is not part of this review. |
| `python3 -m pytest -q tools` | `179 passed, 1 skipped` in 258 s. |

Quick mode uses a shorter quantizer horizon than `--full`, so its ratios (1.69, 2.01, 2.41 and 1.63, 2.00, 2.54) differ from the table. The note attributes the table to the full run. That is what the full run prints.
