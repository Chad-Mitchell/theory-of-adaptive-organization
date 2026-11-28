# Derivation: least action against the cost of judgment, class PATH

*Friday 27 November 2026 (America/New_York). Written after the lock (`PREREG.md`, commit `b6ed7d84a879a69187d85ffc457a063495e8a4f2`, `LOCK.txt`) and the gate read (`gate_read.md`, a same-agent pass). All bars are CONSISTENCY_CHECKs (`PREREG.md`, Gate). Checks: `checks/la_checks.py` (output `checks/la_checks.out`, RESULT PASS) and `checks/LeastAction.lean` (output `checks/LeastAction.out`: no `sorry`, axioms `propext`, `Classical.choice`, `Quot.sound` only).*

## 0. Symbols and units

| Symbol | Meaning | Units |
|---|---|---|
| \(X_t\) | the decision coordinate (one overdamped degree of freedom) | m |
| \(\gamma\) | drag coefficient of its bath | J s m\(^{-2}\) (= kg s\(^{-1}\)) |
| \(kT\) | bath temperature times Boltzmann's constant | J |
| \(D=kT/\gamma\) | noise intensity (Einstein relation, `theory/GENERALITY_2026-11-22.md:46`) | m\(^2\) s\(^{-1}\) |
| \(u\) | the design: drift (velocity) protocol | m s\(^{-1}\) |
| \(\dot Q=\gamma\,\mathbb E[u^2]+kT\,\mathbb E[\partial_xu]\) | heat rate into the bath (Sekimoto 1998, doi `10.1143/PTPS.130.17`; the repo's convention in \(kT\) units, `theory/bicausal-a-2026-11-27/PREREG.md:68`) | J s\(^{-1}\) |
| \(w\) | running stake on \((X-x_*)^2\), converting loss to the heat's currency (`CORE.md:29`) | J s\(^{-1}\) m\(^{-2}\) |
| \(w_\tau\) | one-time stake on the terminal loss \((X_\tau-x_1)^2\) | J m\(^{-2}\) |
| \(\tau\) | window length | s |
| \(J_\tau\) | window cost \(\int_0^\tau(\dot Q+w\,\mathbb E[\ell])dt+w_\tau\mathbb E[\ell_\tau]\) (`PREREG.md` §1) | J |
| \(M\), \(\omega\) | mass and angular frequency of the classical targets | kg, s\(^{-1}\) |
| \(S\) | classical action \(\int L\,dt\) | J s |

Every term of \(J_\tau\) is in joules: \(\gamma u^2\tau\): (J s m\(^{-2}\))(m\(^2\) s\(^{-2}\))(s) = J; \(w(X-x_*)^2\tau\): (J s\(^{-1}\) m\(^{-2}\))(m\(^2\))(s) = J; \(w_\tau(X_\tau-x_1)^2\): J. The action is in J s, so a match of paths can hold, but a match of values needs a time constant (§2.3). Checked symbolically in `checks/la_checks.out` item 1f.

## 1. The heat in class PATH

Open loop, \(u=u(t)\): \(\partial_xu=0\), so \(\dot Q=\gamma u(t)^2\) exactly, at any \(kT\). The mean obeys \(\dot{\bar x}=u\) and the variance is \(\mathrm{Var}(X_t)=2Dt\), whatever \(u\) is. Hence
\[
J_\tau[u]=\underbrace{\int_0^\tau\bigl(\gamma\dot{\bar x}^2+w(\bar x-x_*)^2\bigr)dt+w_\tau(\bar x_\tau-x_1)^2}_{\text{depends on the design}}+\underbrace{\int_0^\tau 2wDt\,dt+2w_\tau D\tau}_{\text{design-independent}} .
\]
The noise shifts the value of \(J_\tau\) and never the minimizing mean path. This is assumption S2 (open loop) and S3 (additive constant noise) of `PREREG.md` §2; §4 drops S2.

## 2. Free particle (\(w=0\))

**2.1 Euler–Lagrange.** The design-dependent part is \(\int_0^\tau\gamma\dot{\bar x}^2dt+w_\tau(\bar x_\tau-x_1)^2\) with \(\bar x_0=x_0\). Its Euler–Lagrange equation is \(\gamma\ddot{\bar x}=0\): the path is affine, constant velocity \(v\). Transversality at \(\tau\): \(2\gamma\dot{\bar x}(\tau)+2w_\tau(\bar x_\tau-x_1)=0\), so
\[
v^*=\frac{w_\tau(x_1-x_0)}{\gamma+w_\tau\tau},\qquad \bar x_\tau=x_0+(x_1-x_0)\frac{w_\tau\tau}{\gamma+w_\tau\tau}.
\]
Units: \(w_\tau/\gamma\) is m\(^{-2}\)J / (J s m\(^{-2}\)) = s\(^{-1}\); \(v^*\) is m s\(^{-1}\). (Check 1a.)

**2.2 It is a strict minimum, not only stationary.** Among constant velocities, \(J(v)-J(v^*)=(\gamma\tau+w_\tau\tau^2)(v-v^*)^2\) (check 1b; Lean `terminal_gap`, `terminal_min`). Among all protocols, the second variation \(\int\gamma\dot\eta^2\) is positive for every \(\eta\ne0\) with \(\eta(0)=0\), and on a time grid the drag heat of steps \(d_i\) satisfies \(n\sum d_i^2\ge(\sum d_i)^2\) with equality at equal steps (Cauchy–Schwarz; Lean `discrete_heat_ge`, `equal_steps_attain`; numerical check 1g–1h at \(N=50\)). The free action \(\int\frac12M\dot x^2\) is also a true minimum for every \(\tau\) (it has no conjugate points), so here "minimal" and "stationary" coincide and a minimum principle can match it.

**2.3 The limit, and the time constant.** As \(w_\tau\to\infty\), \(v^*\to(x_1-x_0)/\tau\) and the path is the classical free path between \(x_0\) and \(x_1\), for every \(\tau\) (check 1c). On that path the minimized heat equals \((2\gamma/M)\,S_{\mathrm{free}}\) (check 1e); \(M/\gamma\) is the momentum relaxation time of a particle of mass \(M\) in that bath, so the identification of values is \(S=\tfrac{M}{2\gamma}J_\tau\), with \(M\) a free constant: the overdamped coordinate has no mass of its own, and the minimization supplies the quadratic velocity cost that plays the role of kinetic energy.

**2.4 Order of limits.** At fixed \(D>0\) the design-independent term \(2w_\tau D\tau\) diverges as \(w_\tau\to\infty\): the minimizer converges, the minimum value does not. A finite statement needs either \(D\to0\) first, or the design-independent term subtracted. With linear feedback the same holds through the entropy term of §4 (\(\tfrac{kT}{2}\ln(V_0/V_\tau)\to\infty\) as the terminal variance \(V_\tau\to0\)): pinning a noisy coordinate to a point costs unbounded heat.

**2.5 The degenerate limit.** At \(w_\tau=0\) (and \(w=0\)), \(v^*=0\) whatever the endpoints (check 1d): with the loss switched off, the cost selects no path, only rest. So the matching limit is \(w_\tau\to\infty\) with the loss active, not \(w\to0\) (`PREREG.md` §2, NO (iv)).

## 3. Harmonic oscillator

**3.1 Euler–Lagrange with a running stake.** With \(x_*=0\) and ends fixed (\(w_\tau\to\infty\)), the design-dependent cost is \(\int_0^\tau(\gamma\dot{\bar x}^2+w\bar x^2)dt\). Euler–Lagrange: \(\gamma\ddot{\bar x}=w\,\bar x\). With \(\Omega=\sqrt{w/\gamma}\) (units s\(^{-1}\)):
\[
\bar x(t)=\frac{x_0\sinh\Omega(\tau-t)+x_1\sinh\Omega t}{\sinh\Omega\tau}\quad(w>0),
\]
an inverted, Euclidean oscillator (check 2a). The real-time oscillator path is \((x_0\sin\omega(\tau-t)+x_1\sin\omega t)/\sin\omega\tau\) (check 2b). The two satisfy different equations; at \(x_0=0\), \(x_1=1\), \(\tau=1\), \(w/\gamma=\omega^2=1\) their midpoints are 0.443409 and 0.569747 (check 2d).

**3.2 The sign.** Writing the stake as a signed number \(W\), the Euler–Lagrange equation \(\gamma\ddot x=Wx\) is the real-time oscillator iff \(W=-\gamma\omega^2<0\) (check 2c). The Lagrangian of a cost is a sum of nonnegative priced terms, \(\gamma\dot x^2+Wx^2\), which has the form kinetic plus potential: the Euclidean Lagrangian. The real-time Lagrangian is kinetic minus potential, which needs a negative price. Nonnegative prices are assumption A8 (`CORE.md:52`), and a negative \(W\) would reward being far from the target, which is not a stake on error as `CORE.md:29` uses the word.

**3.3 Stationary or minimal, including \(\tau>\pi/\omega\).** Second variation of \(\int(\gamma\dot\eta^2+W\eta^2)\), \(\eta(0)=\eta(\tau)=0\): eigenvalues \(\gamma(n\pi/\tau)^2+W\).

- \(W\ge0\): every eigenvalue is positive for every \(\tau\): the Euclidean path is always a strict minimum (check 2f).
- \(W=-\gamma\omega^2\) (\(\gamma=\omega=1\)): \(\lambda_1=(\pi/\tau)^2-1\) is \(+3.000000\), \(+0.234568\), \(-0.173554\), \(-0.750000\) at \(\tau\omega/\pi=0.5,0.9,1.1,2\) (continuum; a 400-point grid agrees to \(4\times10^{-6}\); check 2e). Past the conjugate point the classical path is a saddle, and \(J\) is unbounded below along \(\eta=\sin(\pi t/\tau)\): \(J(x_{\mathrm{cl}}+s\eta)=J(x_{\mathrm{cl}})+s^2\lambda_1\tau/2\to-\infty\). No \(J\)-minimizing design exists there, so a minimum of a cost cannot reproduce the stationary real-time path for \(\tau>\pi/\omega\), even with the sign flipped (`PREREG.md` §2, NO (iii)). This is the known "action is not least" point (Gray and Taylor 2007, doi `10.1119/1.2710480`).

## 4. Where the information heat sits (feedback; drops S2)

Linear feedback \(u=a(t)-k(t)X\) keeps \(X\) Gaussian with mean \(\mu\) and variance \(V\): \(\dot\mu=a-k\mu\), \(\dot V=2D-2kV\). With \(\partial_xu=-k\) and \(kT=\gamma D\), the heat is exactly (check 3a)
\[
\dot Q=\gamma\dot\mu^2+\frac{\gamma\dot V^2}{4V}-\frac{kT}{2}\frac{d}{dt}\ln V .
\]
The first term is the free-particle cost of §2. The second is the same drag cost for the width (the Gaussian case of the Benamou–Brenier kinetic energy, Benamou and Brenier 2000, doi `10.1007/s002110050002`). The third is \(-T\) times the rate of change of the coordinate's entropy \(\tfrac12k\ln V\): the term where information enters, since squeezing the distribution needs a controller that measures \(X\), and CORE's floor charges that controller's memory at least \(kT\) per nat learned (`CORE.md:70`). The loss \(\mathbb E[(X-x_*)^2]=(\mu-x_*)^2+V\) splits the same way, and \((a,k)\mapsto(\dot\mu,\dot V)\) is one-to-one at fixed \((\mu,V)\). So \(J_\tau\) splits into a mean problem and a width problem, and the mean problem is exactly §2–§3. The selected mean path is the same with or without feedback (certainty equivalence; Fleming and Mitter 1982, doi `10.1080/17442508208833228`). The GTAO-specific term changes how tightly the coordinate is held around the path, never the path.

## 5. Stated assumptions, and which ones the match needs

| | Assumption | Needed for the free-particle match? |
|---|---|---|
| S1 | Path computation is free: the controller knows \(x_0,x_1,\tau\) and computes and runs \(u\) at no cost; \(A\) stays assumed (`CORE.md:42`), and CORE prices nats, not computing steps (`CORE.md:70`) | **Yes.** Nothing in \(J_\tau\) pays for finding the path |
| S2 | Open loop | No (§4) |
| S3 | Additive constant noise, one temperature | Yes (otherwise the mean and the width do not decouple) |
| S4 | The window form of the cost, with a terminal stake (`PREREG.md` §1) | Yes: the stationary rate of `CORE.md:27` has no endpoints, so it cannot select a path between two points |

## 6. What counts as restating, applied

- The match of §2 is item (c) of `PREREG.md` §2: minimum mean dissipation of a finite-time overdamped protocol is the kinetic (Benamou–Brenier) action and its optimal trajectories have constant velocity (Schmiedl and Seifert 2007, doi `10.1103/PhysRevLett.98.108301`; Aurell et al. 2011, doi `10.1103/PhysRevLett.106.250601`). The small-noise most-probable path of Brownian motion is the same straight line (Schilder 1966, doi `10.1090/S0002-9947-1966-0201892-6`; Onsager and Machlup 1953, doi `10.1103/PhysRev.91.1505`; Dürr and Bach 1978, doi `10.1007/BF01609446`; Freidlin and Wentzell, doi `10.1007/978-3-642-25847-3`).
- The Euclidean form of §3 is item (e): a positive quadratic cost gives imaginary-time mechanics. The link between stochastic optimal control and Euclidean path integrals is KNOWN (Fleming and Mitter 1982; Kappen 2005, doi `10.1103/PhysRevLett.95.200201`).
- The underdamped route, where classical paths are zero-residual minimizers of \(\int(M\ddot x+V'(x))^2dt\), is item (a): Newton's equation is put into the noise model by hand. It reproduces real-time paths even past \(\tau=\pi/\omega\) (the residual is nonnegative and zero on the classical path), but only because the dynamics was assumed. It is excluded as a YES.
