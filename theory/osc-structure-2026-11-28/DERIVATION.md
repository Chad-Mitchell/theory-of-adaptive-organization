# Derivation: oscillation from structure, every price positive

*Saturday 28 November 2026 (America/New_York). Written after the lock (`PREREG.md`, commit `edddf236f176218ea41e76179a691e0effdff334`, `LOCK.txt`). Checks: `checks/osc_checks.py`, output `checks/osc_checks.out` (run at nice 19, one thread per process, about 3 s). Two locked checks miss (B3-ii, C1 (iii-b)); every other check passes. Deviations: `DEVIATIONS.md`. Same-agent work, not an independent review.*

## 0. Symbols, units and the two questions

The heat of an actuation \(u\) is drag heat \(r\,\mathbb E[u^2]\) (#309 class PATH, open loop); stakes \(w,p\ge0\) (A8, `CORE.md:52`); noise intensity \(\sigma^2\). Sensing is free and noiseless except in A1 (assumption S-INFO, `PREREG.md` §1). **Q-path** asks which path between fixed ends a window cost selects (#309). **Q-loop** asks what the cost-minimizing policy does when run forward under noise; CORE's \(J\) is a long-run rate (`CORE.md:27`), so Q-loop is CORE's own object.

| Class | Variables (units) | Prices (units) | Dimensionless groups |
|---|---|---|---|
| A1 | \(Z\) (any unit \(z\)); \(a,\omega_0\) (s\(^{-1}\)) | stake on \(\mathbb E|Z-M|^2\) | \(\omega_0/a\), \(\sigma/(a\sigma_o)\) |
| A2, C1 | \(x\) (m), \(u\) (m s\(^{-1}\)), lag \(\tau\) (s), gain \(k\) (s\(^{-1}\)) | \(r\) (J s m\(^{-2}\)), \(w\) (J s\(^{-1}\) m\(^{-2}\)) | \(k\tau\); \(\rho=w\tau^2/r\) |
| B2 | \(x\) (m), \(y=\dot x\) (m s\(^{-1}\)), \(u\) (m s\(^{-2}\)) | \(r\) (J s\(^3\) m\(^{-2}\)), \(w\) (J s\(^{-1}\) m\(^{-2}\)), \(p\) (J s m\(^{-2}\)) | \(p/\sqrt{wr}\); \(c_0=\sqrt{w/r}\) in s\(^{-2}\) |
| C2 | \(x\) (m), drain \(d\) (m s\(^{-1}\)) | \(k_a\) (J per reset), \(w\) (J s\(^{-1}\) m\(^{-2}\)) | \(T^*\) in s: \((k_a/(wd^2))^{1/3}\) has units s |

## 1. Arm A: a memory tracking a periodic or lagged world

**A1 (rotating world).** For \(dZ=(-a+i\omega_0)Z\,dt+\sigma\,d\xi\) seen as \(dY=Z\,dt+\sigma_o\,d\eta\), the stationary Kalman–Bucy variance solves \(0=-2aP+\sigma^2-P^2/\sigma_o^2\), so \(P=\sigma_o(\sqrt{a^2\sigma_o^2+\sigma^2}-a\sigma_o)\), gain \(K=P/\sigma_o^2\), and the memory runs \(dM=(-a+i\omega_0-K)M\,dt+K\,dY\). Its free dynamics decay at \(a+K\) and rotate at exactly \(\omega_0\), for every \(\sigma_o\), hence for every precision the stake buys (check A1a symbolically; A1b on 200 random 2-D draws, deviation \(9\times10^{-16}\)). At \(\omega_0=0\) the memory does not rotate (A1c). The \(J\)-optimal memory copies the world's rhythm and creates none: the internal model principle (Francis and Wonham 1976) inside the Kalman filter (Kalman and Bucy 1961). The copy is not free: keeping a phase between looks needs a clock whose heat the TUR prices (T68, `theory/CLOCK_TERM_2026-11-23.md:11`), so an oscillating memory is a dissipative oscillator.

**A2 (lagged world, any causal policy).** World \(dx=u\,dt+\sigma\,dW\), state seen with lag \(\tau\), past actions known. The least-squares estimate of the present is \(\hat x(t)=x(t-\tau)+\int_{t-\tau}^tu\), and \(x-\hat x=\sigma(W_t-W_{t-\tau})\) is independent of \(\hat x\). By certainty equivalence the optimal policy is \(u=-k\hat x\); over that family \(J=rk\sigma^2/2+w(\sigma^2/2k+\sigma^2\tau)\), minimized at \(k^*=\sqrt{w/r}\) (A2b), the delay-free gain. In Fourier variables the closed loop is (A2a)
\[
H(\nu)=\sigma\,\frac{k+i\nu-k\,e^{-i\nu\tau}}{i\nu\,(k+i\nu)},\qquad S_x(0^+)=\sigma^2\frac{(1+k\tau)^2}{k^2}.
\]
**The global maximum is at \(\nu=0\) for every \(k\tau\)**, by a one-line bound found after the run: \(|i\nu+k(1-e^{-i\nu\tau})|\le\nu+2k|\sin(\nu\tau/2)|\le\nu(1+k\tau)\), so \(S_x(\nu)\le\sigma^2(1+k\tau)^2/(k^2+\nu^2)<S_x(0^+)\). The grid agrees at all six locked \(k\tau\) (A2d). There are small ripples near \(\nu\tau\approx2\pi m\) (at most 3.6% of \(S_x(0^+)\) at \(k\tau=10\)), never a resonance. Optimal anticipation removes the ringing a lag would otherwise cause. The bound makes OS-A2 an identity after the fact; it was not known to the author at the lock.

## 2. Arm B: two or more stores, all prices positive

**B1 (cost side: integrating out a store never makes a negative stake).** For a quadratic window cost with Fourier symbol \(H(\nu)\), Hermitian and positive semidefinite at every real \(\nu\), minimizing over the other stores at fixed \(x\) leaves the Schur complement \(h_{11}-|h_{12}|^2/h_{22}=\det H/h_{22}\ge0\). Worked case, \(H=\begin{pmatrix}\gamma_1\nu^2+w_1+c&-c\\-c&\gamma_2\nu^2+w_2+c\end{pmatrix}\):
\[
W_{\mathrm{eff}}(\nu)=w_1+\frac{c\,(\gamma_2\nu^2+w_2)}{\gamma_2\nu^2+w_2+c}>0\quad(\nu\ \text{real}),
\]
(check B1a), and with a gyroscopic coupling \(g(x\dot y-y\dot x)\) the reduced symbol stays \(\ge0\) on 2000 random PSD draws (B1c, minimum 0.057). Continued to imaginary frequency \(\nu=i\omega\) (the Wick reading), \(W_{\mathrm{eff}}(i\omega)\) is negative on a band inside \((\sqrt{w_2/\gamma_2},\sqrt{(w_2+c)/\gamma_2})\); at \(\gamma_1=\gamma_2=1\), \(w_1=0.1\), \(w_2=1\), \(c=2\) it is \([1.0466,1.7320]\) (B1b). So a negative stake in the cost appears only after a Wick rotation, never from structure.

**B2 (dynamics side: the restoring sign appears with two stores).** Level \(x\) fed by a reserve flow \(y\): \(\dot x=y\), \(dy=u\,dt+\sigma\,dW\), cost rate \(r\,\mathbb E[u^2]+w\,\mathbb E[x^2]+p\,\mathbb E[y^2]\). The algebraic Riccati equation gives \(u=-c_0x-c_1y\) with
\[
c_0=\sqrt{w/r},\qquad c_1=\sqrt{p/r+2\sqrt{w/r}},\qquad \zeta=\frac{c_1}{2\sqrt{c_0}}=\sqrt{\tfrac12+\frac{p}{4\sqrt{wr}}}\ \ge\ \tfrac1{\sqrt2}
\]
(B2a on 500 random draws, deviation \(2\times10^{-14}\)). With \(y\) integrated out, the level obeys
\[
\ddot x+c_1\dot x+c_0x=\sigma\xi,
\]
a damped real-time oscillator: in #309's convention \(\gamma\ddot x=Wx\) per unit inertia, \(W_{\mathrm{dyn}}=-c_0<0\), with every price positive (B2b). The minus sign that #309 found only at a negative stake is here the sign of the closed-loop restoring term. Its source is structure: two integrations in series, closed by a feedback that pays to shrink the first store. One store (#309's class) cannot show it: its closed loop \(\dot x=-kx\) gives \(\ddot x=+k^2x\), the Euclidean sign (B2c). At \(p\ge0\), \(\zeta\ge1/\sqrt2\), so \(S_x\) has no peak at \(\nu>0\) (B2b). The level rings and does not resonate.

The same split shows on the path side. With \(u=\ddot x\), the window cost \(\int(r\ddot x^2+wx^2)\) has Euler–Lagrange equation \(r\,x''''+wx=0\), that is \((\partial_t^2+i\Omega^2)(\partial_t^2-i\Omega^2)x=0\) with \(\Omega^2=\sqrt{w/r}\): exponents \(\Omega e^{i(\pi/4+m\pi/2)}\). Each factor is an oscillator with a complex spring constant, halfway between the Euclidean (\(-\Omega^2\)) and real-time (\(+\Omega^2\)) signs.

**B3 (n stores in series).** \(\dot x_1=x_2,\dots,dx_n=u\,dt+\sigma\,dW\), cost rate \(r\,\mathbb E[u^2]+w\,\mathbb E[x_1^2]\). Kalman's spectral factorization (the symmetric root locus) gives the closed-loop polynomial \(p(s)\) with
\[
p(s)\,p(-s)=(-1)^ns^{2n}+w/r,\qquad |p(i\nu)|^2=\nu^{2n}+w/r .
\]
The poles are the left-half Butterworth pattern of radius \((w/r)^{1/2n}\); the least-damped pair has \(\zeta_n=\sin(\pi/2n)\): 1, 0.7071068, 0.5, 0.3826834 at \(n=1,\dots,4\) and 0.1950903 at \(n=8\) (B3-i, exact to \(10^{-7}\) at two stake ratios). The slowest mode sits at angle \(\pi/2-\pi/2n\) from the decay axis: 0° for one store (Euclidean), 45° for two, 78.75° for eight, approaching 90° (an undamped swing) only as \(n\to\infty\).

**The locked peak rule misses (B3-ii).** The output spectrum is \(S_{x_1}(\nu)=\sigma^2/(\nu^{2n}+w/r)\), maximally flat and monotone at every \(n\) (diagnostic: deviation \(2.5\times10^{-12}\)). No \(n\) gives a resonance. The prediction applied the second-order rule (a peak iff \(\zeta<1/\sqrt2\)) to an \(n\)-th-order loop, where the other poles fill the dip. With full information and no lag, the \(J\)-optimal loop's modes ring, but its output never resonates. This is the Butterworth property and the frequency-domain face of Kalman 1964 (return difference at least 1).

## 3. Arm C: lags, lumpy prices, limit cycles

**C1 (lagged reading, memoryless gain).** For \(dx=-k\,x(t-\tau)\,dt+\sigma\,dW\) with \(z=k\tau<\pi/2\), the stationary variance is \(\sigma^2(1+\sin z)/(2k\cos z)\) (Küchler and Mensch 1992; spectral integral agrees to \(10^{-4}\) relative, C1a). Then
\[
J(z)=\frac{\sigma^2r}{2\tau}\,\frac{(z^2+\rho)(1+\sin z)}{z\cos z},\qquad \rho=\frac{w\tau^2}{r}.
\]
\(J\to\infty\) at \(z\to\pi/2\), so the optimum never sits at the Hopf point (C1 (i)). As \(\rho\to\infty\), \(z^*\) minimizes \((1+\sin z)/(z\cos z)\), and the stationarity condition \(\tfrac{\cos z}{1+\sin z}+\tan z=\tfrac1z\) reduces to \(\tfrac1{\cos z}=\tfrac1z\), that is, **\(z=\cos z\)**: \(z_\infty=0.739085\), the fixed point of the cosine (C1 (ii)). With \(D(\nu)=\nu^2-2k\nu\sin\nu\tau+k^2\), \(S_x=\sigma^2/D\) and \(D''(0)=2-4k\tau\), so \(S_x\) peaks at \(\nu>0\) iff \(z>1/2\) (C1 (iii-a), confirmed globally on 8 values). That rule was reasoned before the lock (`DEVIATIONS.md`, `OSC-DISCLOSE-1`). **The stake at which the \(J\)-optimal loop starts to resonate is \(\rho_c=0.912107\)**, just below the locked band \([1,30]\) (C1 (iii-b): a miss). At \(z_\infty\) the peak sits at \(\nu\tau=1.02495\), period \(6.1302\,\tau\), height 1.81 times \(S_x(0)\) (C1 (iv), inside \([5\tau,9\tau]\)). The dominant root of \(\lambda=-z\,e^{-\lambda}\) is \(\lambda\tau=W_0(-z_\infty)=-0.5275+1.1361i\): free ringing period \(5.53\tau\), damping ratio 0.42. Against A2: the same lag gives a noise-sustained oscillation (a quasi-cycle) at the optimum of a restricted, memoryless design, and none at the optimum of the full design.

**C2 (fixed price per action, steady drain).** Between resets \(\dot x=-d\); a cycle from \(U\) down to \(L\) lasts \((U-L)/d\) and has cost rate \(k_ad/(U-L)+w(U^2+UL+L^2)/3\). At fixed span the loss is least at \(U=-L=A\); then \(k_ad/(2A)+wA^2/3\) is least at \(A^3=3k_ad/(4w)\), so
\[
T^*=\frac{2A}{d}=2\Big(\frac{3k_a}{4wd^2}\Big)^{1/3}=\Big(\frac{6k_a}{wd^2}\Big)^{1/3}
\]
(C2a at three parameter sets; C2b an independent numeric optimum over \((U,L)\), symmetric to \(10^{-6}\)). The cycle is self-sustained by the drain, restored in amplitude at the next reset, and neutral in phase; as \(d\to0\), \(T^*\propto d^{-2/3}\to\infty\) (C2c): no throughput, no cycle. This is the economic-order-quantity sawtooth (Harris 1913, reprinted 1990) and the deterministic analog of CORE's lumpy store (`CORE.md:100`; the Brownian version has \(T^*=\sqrt{6k/(w\sigma^2)}\)).

**C3 (delayed adaptation toward a minimum).** \(\dot x=-\eta\tanh(x(t-\tau))\), \(\mu=\eta\tau\). Linearized, \(\dot x=-\mu x(t-\tau)\) loses stability at \(\mu=\pi/2\) with frequency \(\pi/(2\tau)\), period \(4\tau\) (Hayes 1950). Euler integration (\(dt=10^{-3}\tau\), 400\(\tau\)): at \(0.9\times\) onset the late amplitude is below \(10^{-5}\); at \(1.1\times\) onset the same cycle is reached from \(x_0=0.1\) and \(x_0=2\), amplitude 0.6475, period \(4.002\tau\), mean excess \(\mathbb E[x^2]/2=0.103>0\) (C3). A stable limit cycle (a supercritical Hopf, as for Wright's and Hutchinson's equations) does appear, but it belongs to the adaptation process, and it costs more than \(J^*\): it is a miss of the minimum, the oscillating face of COAD-F4 (`theory/COADAPTATION.md:252`).

## 4. Conservative against dissipative (OS-D)

At strictly positive prices with full information and no lag, \(|p(i\nu)|^2=\nu^{2n}+w/r>0\), so no closed-loop eigenvalue lies on the imaginary axis (300 random draws with positive prices on every store, \(n\le8\): minimum \(-\mathrm{Re}\,\lambda=0.092\)). More generally, the Hamiltonian matrix of a linear-quadratic problem with \(R>0\) and a detectable, nonnegative state price has no imaginary-axis eigenvalues (Kalman 1964): the optimal-control Hamiltonian is hyperbolic, with growing and decaying halves, and the closed loop is its decaying half. Real-time conservative mechanics is elliptic: its eigenvalues sit on the imaginary axis. Positive prices exclude exactly that, at any finite number of stores. So a conservative swing is never \(J\)-optimal here. Oscillation that is \(J\)-optimal, or that \(J\)-driven adaptation produces, is dissipative: decaying ringing (B2, B3), a noise-sustained quasi-cycle (C1), a relaxation cycle sustained by a drain (C2), a copied rhythm paid for by clock heat (A1), or a limit cycle of delayed adaptation (C3).

## 5. Stated assumptions

S-INFO (free, noiseless sensing in A2, B, C1) favors the designs. Information heat and the TUR clock heat would add dissipation and damping and would not create a restoring term. Linear-Gaussian classes throughout, except C2 (deterministic) and C3 (a saturating step). The ruin cap is slack. CORE's long-run rate is used for A, B2, B3 and C; the window form of #309 only in B1 and the B2 path remark.
