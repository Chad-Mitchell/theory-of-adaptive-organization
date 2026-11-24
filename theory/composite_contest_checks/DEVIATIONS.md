# Deviations, composite contest

`theory/PREREG.md` is unchanged. Predictions P1–P8 were not edited after the run.

- **D1.** Headline moved off the ε = 0 slice. Reason: checkpoint 1 in `theory/PREREG_R2.md`, committed before any scoring run. P1 stays as a check of an identity.
- **D2.** Classical-direction control added, same price. Reason: the same checkpoint. Proved there, then checked in `control.out`.
- **D3.** Implementation, after the run was already specified. The rebit state step uses the analytic gradient of the loss on the Cholesky factor and a golden-section line search, and it stops when the factor stops moving, instead of a fixed 2000 finite-difference steps. The loss it returned equals the proved floor 1/25 (`decisions.out` line 2, `L_rebit`). The early stop did not leave a lower loss unfound. No prediction was changed.
