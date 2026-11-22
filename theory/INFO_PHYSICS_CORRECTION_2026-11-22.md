# Correction to `theory/INFO_PHYSICS.md`

*22 November 2026. Dated record, after the review of draft PR #178 (`reviews/attainability_2026-11-22/REVIEW.md`). The merged note is not rewritten. The sentences below stay in that file as the text the reviews of PR #175 scored. This record says which of them are superseded, and for which loss.*

## What stays

The centered spring \(dM=-\lambda(M-X)\,dt+\sqrt{2D}\,dB\), scored by the raw coordinate error \(\mathbb{E}[(M-X)^2]\), is unchanged. At fixed raw error below the signal variance, the heat falls toward \(kT\,av/\varepsilon\) and the flow rises from the Kalman rate \(a(v-\varepsilon)/\varepsilon\) to the same value. The raw-coordinate heat objective is blind at stake 2, cost 2. The stake table in §8a is the table of that coordinate. `reviews/info_physics_2026-11-22/REVIEW.md` and `reviews/info_physics_2026-11-22_round2/REVIEW.md` remain correct for that family and that loss.

## What is superseded

Four passages state, for a continuous signal, that no coupling attains the Kalman rate at finite heat. For an exogenous equilibrium Ornstein–Uhlenbeck signal, when the loss is the mean squared error of an action of the current memory state, those passages are superseded by `theory/INFO_PHYSICS_ATTAINABILITY.md`.

The passages, as they stand in the merged note:

- The opening answer: the bound "is not tight on the linear spring" and "\(kT\) times the flow is not, in general, the tangent of the physical frontier."
- Section 8a, the same claim for \(J_{\mathrm{phys}}\).
- Section 8a: "They do not exhibit a coupling that attains the Kalman rate at finite heat equal to that bound. This note does not construct one either. Whether a nonlinear potential, or a different bath, closes the gap is **OPEN**."
- The close of §8a, and §11: "Whether any coupling attains the Kalman rate at finite heat equal to \(kT\) times that rate is **OPEN**. The spring does not."

## What replaces them, for this signal and this loss

The decision error is \(\mathbb{E}[(g(M)-X)^2]\), with \(g\) a function of the current memory state. The infimum of the memory-bath heat at decision error \(\varepsilon\) is the Kalman rate \(kT\,a(v-\varepsilon)/\varepsilon\).

Two linear designs approach it at finite heat. A spring with rest point \(cX\), \(c=1-\varepsilon/v\), has Sekimoto heat \(4.000020\) at \(a=v=kT=1\), \(\varepsilon=0.2\), rate \(10^6\). The centered spring, with raw coordinate error held at \(0.25\), has conditional variance \(0.20000032\), heat \(4.00001200\), and regression gain \(0.80000048\). The action \(g(M)=\mathbb{E}[X\mid M]\) meets that decision error at that heat. The constant \(kT\,a\) is the gap from charging the centered coordinate's raw error instead of the decision.

The master equation and the hypothesis sentence are unchanged.
