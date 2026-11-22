# From the substitution chain to the diffusion limit

*Sunday 22 November 2026. Branch `diffusion-convexity-2026-11-21`, draft PR. Written by one executor for Chad Mitchell; a self-check, not an independent review. Revised after the independent review of PR #153 (`reviews/diffusion_convexity_2026-11-21/REVIEW.md`, verdict NOT-READY). The revision is a self-check of those fixes, not a second independent review. It does not change the Part 2 hypothesis sentence, and it does not edit a locked preregistration or hash file.*

## 0. Bottom line

DS1's excess \(\frac{d}{2\beta}\bigl(1+\frac{D}{D_m}\bigr)\) is an identity for the Langevin equation (L), already proved in `theory/DRIFT_SELECTION.md` §4. What was open is the passage from the exact chain. Two limits are in play, and they are not the same limit.

1. **Weak mutation.** In generation time, \(N\mu_{\mathrm{gen}}\to 0\) with \(\beta=\alpha(N-1)\) held fixed. This is the limit in which a haploid Moran population is the monomorphic origination–fixation chain of §2 of the drift note. It is assumed here, as it is assumed there. It is not proved in this note.
2. **Diffusion scaling of that chain.** Time is the chain's own time. Hold \(\beta>0\), the Hessian \(H\), the neutral diffusion \(D_m=\mu\delta^2/(2d)\), and the world's \((D,\gamma)\) fixed, and send the lattice spacing \(\delta\to 0\) (so the substitution rate \(\mu=2d D_m/\delta^2\to\infty\)). The small parameter is the squared fitness step at a typical lag,
   \[
   \varepsilon_{\mathrm{lat}}=\delta^2\beta\lambda_{\max}\Bigl(1+\frac{\mathrm{tr}\,Q}{d D_m}\Bigr).
   \]
   For isotropic Brownian wander, \(Q=DI\), this is \(\delta^2\beta\lambda_{\max}(1+D/D_m)\). The ratio \(D/D_m\) is held fixed: it is part of the limit formula, not a further approximation. \(\beta\) is held fixed. Closeness, the reading \(\sigma N_e\gg d(1+D/D_m)\), is the separate large-\(\beta\) corollary DS1c and is not this limit.

\(N\mu_{\mathrm{gen}}\to 0\) and \(\mu\to\infty\) do not conflict. A generation is not a substitution.

**What is proved.**

| | Statement | Status |
|---|---|---|
| CD1 | Static quadratic chain, diagonal \(H\): the stationary law is exactly Gibbs, and \(0<\frac{d}{2\beta}-\mathbb{E}[J-J^\star]\le\sum_k\frac{8\pi^2}{\beta a_k}\exp(-2\pi^2/a_k)\) whenever each \(a_k=\beta\lambda_k\delta^2\le 1\) | **PROVED** |
| CD2 | On \(\lvert Nx_\pm\rvert\le 1\), \(\lvert R(L)\rvert\le D_m\delta^2\bigl(500\,\beta h+200(\beta h)^2(1+L^2)+1000(\beta h)^3(1+L^4)\bigr)\). The linear Moran map alone leaves \(R=-a\delta^2/2\), so the constant depends on \(\beta h\) | **PROVED** |
| CD3 | One coordinate, quadratic cost, Brownian centre, \(D>0\): for each small \(\delta\) there is one stationary law; its excess equals the DS1 value plus \(O(\delta^2)\) as \(\delta\to 0\) with \(\beta,h,D_m,D\) fixed. The \(O(\delta^2)\) uses a uniform exponential moment, proved in §4 | **PROVED** |
| CD4 | The same one-dimensional Brownian lag. If the initial laws converge weakly and have a uniform second moment, the path measures converge weakly in Skorokhod space to the Langevin lag | **PROVED** |
| — | Ornstein–Uhlenbeck centre, constant velocity, non-diagonal \(H\), several coordinates | **SKETCH** |

**What stays open.** The sketches just named (the cross moment \(L\theta^\star\) is a different defect from \(R(L)\)). A non-quadratic cost. The weak-mutation limit from the full Moran population. A numerical \(C\) in CD3 with the Lyapunov moment eliminated; the runs measure the ratio, they are not that constant.

## 1. The chain, and the defect

Everything in `theory/DRIFT_SELECTION.md` §2 is kept. One coordinate is enough for CD3: \(J-J^\star=\tfrac12 h L^2\), \(L=\theta-\theta^\star\), Brownian centre \(\mathrm{d}\theta^\star=\sqrt{2D}\,\mathrm{d}B\), and
\[
r_\pm(L)=\rho\,\varphi(x_\pm),\qquad \rho=\frac{N D_m}{\delta^2},\qquad D_m=\frac{\mu\delta^2}{2},
\]
\[
x_+=\alpha h\delta L+\tfrac12\alpha h\delta^2,\qquad x_-=-\alpha h\delta L+\tfrac12\alpha h\delta^2,
\]
with \(\varphi(x)=(1-e^x)/(1-e^{Nx})\) and \(\varphi(0)=1/N\), and \(\beta=\alpha(N-1)\). The lag is Markov. Its generator on a test function \(f\) is
\[
Gf=r_+(f(L+\delta)-f)+r_-(f(L-\delta)-f)+D f''.
\]
The Langevin generator of (L), written on the lag, is
\[
\mathcal{L}f=-D_m\beta h\, L f'+ (D_m+D) f''.
\]
On \(f(L)=L^2\) both are exact polynomials in the rates, because \(L^2\) has no third derivative:
\begin{align*}
G(L^2)&=r_+(2\delta L+\delta^2)+r_-(-2\delta L+\delta^2)+2D,\\
\mathcal{L}(L^2)&=-2 a L^2+2D_m+2D,\qquad a=D_m\beta h.
\end{align*}
Write \(R=G(L^2)-\mathcal{L}(L^2)\). If a stationary law exists, \(\mathbb{E}[G(L^2)]=0\), so \(\mathbb{E}[\mathcal{L}(L^2)]=-\mathbb{E}[R]\), which is
\[
\mathbb{E}[L^2]=\frac{D_m+D}{a}+\frac{\mathbb{E}[R]}{2a}.
\]
Since \(J-J^\star=\tfrac12 h L^2\) and \(\tfrac12 h(D_m+D)/a=\frac1{2\beta}(1+D/D_m)\),
\[
\mathbb{E}[J-J^\star]-\frac1{2\beta}\Bigl(1+\frac{D}{D_m}\Bigr)=\frac{\mathbb{E}[R]}{4 D_m\beta}. \tag{I}
\]
The whole of CD3 is a bound on \(\mathbb{E}[R]\). The identity (I) is an equality whenever the stationary law has a finite second moment. The grid solver in `tools/chain_diffusion_checks.py` matches both sides to the solver's truncation error.

## 2. Theorem CD1 (static chain)

**Theorem CD1.** Let the centre be fixed, \(H=\mathrm{diag}(\lambda_1,\ldots,\lambda_d)\) with each \(\lambda_k>0\), and let the chain be the static chain of the drift note (equal clocks, steps \(\pm\delta e_k\)). Then the unique stationary law is \(\pi(\theta)\propto e^{-\beta J(\theta)}\) on \(\delta\mathbb{Z}^d\). If \(a_k=\beta\lambda_k\delta^2\le 1\) for every \(k\),
\[
0<\frac{d}{2\beta}-\mathbb{E}[J-J^\star]\le\sum_{k=1}^d\frac{8\pi^2}{\beta a_k}\exp\Bigl(-\frac{2\pi^2}{a_k}\Bigr).
\]
The leading term in coordinate \(k\) is \(\frac{4\pi^2}{\beta a_k}\exp(-2\pi^2/a_k)\). The lattice excess sits below the continuum value. As \(\delta\to 0\) the error is smaller than every positive power of \(\delta\).

*Proof.* Detailed balance is the identity \(\varphi(x)/\varphi(-x)=e^{-(N-1)x}\). A step that raises \(J\) by \(\Delta\) is slower than the reverse step by exactly \(e^{-\beta\Delta}\), and the proposal rates are symmetric, so \(\pi\propto e^{-\beta J}\). Uniqueness is irreducibility on the lattice.

Diagonal \(H\) makes the coordinates independent, so the excess is a sum of one-dimensional excesses. In one coordinate, \(a=\beta h\delta^2\) and the weight of site \(n\) is \(e^{-a n^2/2}\). Poisson summation gives, with \(q=\exp(-2\pi^2/a)\),
\[
Z=\sum_{n\in\mathbb{Z}}e^{-a n^2/2}=\sqrt{\frac{2\pi}{a}}\,\theta,\qquad\theta=\sum_{k\in\mathbb{Z}}\exp\Bigl(-\frac{2\pi^2 k^2}{a}\Bigr)=1+2q+2q^4+\cdots.
\]
Then \(\mathbb{E}[n^2]=-2\partial_a\log Z=1/a-(8\pi^2/a^2)\rho\) with
\[
\rho=\frac{q+4q^4+9q^9+\cdots}{1+2q+2q^4+\cdots}.
\]
And \(\mathbb{E}[J]=(a/(2\beta))\mathbb{E}[n^2]\), so
\[
\frac1{2\beta}-\mathbb{E}[J]=\frac{4\pi^2}{\beta a}\,\rho.
\]
For \(a\le 1\), \(q\le e^{-2\pi^2}<3\cdot 10^{-9}\). Then \(q/(1+3q)\le\rho\le q+8q^4\), and \(1+8q^3\le 2\), so
\[
0<\frac1{2\beta}-\mathbb{E}[J]\le\frac{8\pi^2}{\beta a}\,q.
\]
The leading term is the \(k=\pm 1\) summand \(\frac{4\pi^2}{\beta a}q\). Summing coordinates gives the claim. ∎

The diffusion's static excess is exactly \(d/(2\beta)\). CD1 is therefore the static case of the passage, with an explicit error, and it does not use a diffusion approximation: the chain is exactly Gibbs.

## 3. Theorem CD2 (the defect)

The fixation map extends by removing the singularity at \(0\),
\[
f(z)=N\varphi(z/N)=\frac{N\sinh(z/(2N))}{\sinh(z/2)}\exp\bigl(-(N-1)z/(2N)\bigr).
\]
Poles sit at \(z=2\pi i k\), \(k\neq 0\). Write \(f_{\mathrm{lin}}(z)=1-((N-1)/(2N))z\) and \(\varphi_{\mathrm{lin}}(x)=f_{\mathrm{lin}}(Nx)/N\).

**Lemma (Cauchy bound).** For \(N\ge 2\) and \(|z|\le 1\),
\[
\bigl|f(z)-f_{\mathrm{lin}}(z)\bigr|\le \tfrac1{12}z^2+3.4\,|z|^3,
\]
and the remainder \(r(z)\) after the quadratic Taylor polynomial of \(f\) satisfies \(|r(z)|\le 3.4|z|^3\) and \(|r'(z)|\le 10.2\, z^2\).
*Proof.* The series of \(\sinh\) has positive coefficients, so \(|\sinh(u)|\le\sinh(|u|)\). For \(|u|\le 1/2\), \(|\sinh(u)/u|\le\sinh(1/2)/(1/2)<1.043\). On \(|z|=2\) and \(N\ge 2\), \(|N\sinh(z/(2N))|\le 1.043\), \(|\sinh(z/2)|\ge\sin 1>0.841\), and the exponential factor is at most \(e\). Hence \(|f|<3.4\) on \(|z|=2\). For \(|z|\le 1\) a circle of radius \(1\) stays inside \(|w|\le 2\), so \(|f'''|\le 6\cdot 3.4=20.4\). The integral remainder after order \(2\) is at most \(20.4|z|^3/6=3.4|z|^3\), and its derivative is at most \(20.4\, z^2/2=10.2\, z^2\). The quadratic coefficient is \((N-1)(N-2)/(12N^2)\le 1/12\). ∎

**Lemma (linear defect).** Replace \(\varphi\) by \(\varphi_{\mathrm{lin}}\). Then \(R(L)=-a\delta^2/2\) for every \(L\), with \(a=D_m\beta h\).
*Proof.* Let \(u=\alpha h\delta L\) and \(c=\alpha h\delta^2/2\), so \(x_+=u+c\) and \(x_-=-u+c\). Then \(\varphi_{\mathrm{lin}}(x_+)-\varphi_{\mathrm{lin}}(x_-)=-((N-1)/N)u\) and \(\varphi_{\mathrm{lin}}(x_+)+\varphi_{\mathrm{lin}}(x_-)=2/N-((N-1)/N)c\). Multiplying by \(\rho=N D_m/\delta^2\) and by the jumps in \(L^2\) gives drift \(-a L\) exactly, because \((N-1)\alpha=\beta\), and second-moment weight \(2 D_m-a\delta^2/2\). Those are the Langevin drift \(-a L\) and the Langevin noise \(2 D_m\), except for the constant \(-a\delta^2/2\). It does not cancel. ∎

The linear piece is the first order in the drift note. It does not reproduce the Langevin generator on \(L^2\). The missing piece is \(-a\delta^2/2\), which depends on \(\beta h\).

**Theorem CD2.** Let \(N\ge 2\). On \(|Nx_\pm|\le 1\),
\[
|R(L)|\le D_m\delta^2\Bigl(500\,\beta h+200(\beta h)^2(1+L^2)+1000(\beta h)^3(1+L^4)\Bigr).
\]
Off that event, \(|\varphi|\le 1\), so
\[
|R(L)|\le \frac{2N D_m}{\delta}|L|+2N D_m+2a L^2+2 D_m.
\]
There is no factor \(h\) in the first term of the tail bound: \(|r_+-r_-|\le\rho\), and \(\delta\rho=N D_m/\delta\).

*Proof of the bulk bound.* Let \(\kappa=N/(N-1)\le 2\), \(\Delta z=z_+-z_-=2\kappa\beta h\delta L\) and \(\Sigma z=z_++z_-=\kappa\beta h\delta^2\). Split \(f-f_{\mathrm{lin}}=b_2 z^2+r\) with \(|b_2|\le 1/12\) and \(|r'|\le 10.2 z^2\). Then \(|z_+^2-z_-^2|=|\Delta z|\,|\Sigma z|\) and \(|r(z_+)-r(z_-)|\le 10.2 z_{\max}^2|\Delta z|\), with \(z_{\max}\le\kappa\beta h\delta(|L|+\delta/2)\). Multiplying by \(2(D_m/\delta)|L|\) (the prefactor of a difference of \(\psi=(f-f_{\mathrm{lin}})/N\)) produces at most
\[
\tfrac43 D_m(\beta h)^2\delta^2 L^2+653\, D_m(\beta h)^3\delta^2 L^4+164\, D_m(\beta h)^3\delta^4 L^2.
\]
The sum \(\psi_++\psi_-\), multiplied by \(D_m\), is at most \(80\, D_m(\beta h)^2\delta^2(1+L^2)\) on the same region. The term in \(\delta^4 L^2\) is at most \(200\, D_m\beta h\delta^2\), because \(\beta h\delta|L|\le 1\). Adding the linear defect \(\tfrac12 D_m\beta h\delta^2\) keeps the three coefficients under \(500\), \(200\) and \(1000\). ∎

The shape matters. A bound \(C_N D_m(\beta h\delta)^2\) with \(C_N\) depending only on \(N\) is false. At \(L=0\) the linear lemma gives \(|R|=a\delta^2/2=D_m\beta h\delta^2/2\), and \((\beta h\delta)^2\) is smaller than \(\beta h\delta^2\) by the factor \(\beta h\). Shrinking \(\beta h\) makes any \(N\)-only constant fail. The displayed bound keeps the factor \(\beta h\).

## 4. Theorem CD3 (stationary excess)

**Theorem CD3.** Fix \(N\ge 2\), \(\beta>0\), \(h>0\), \(D_m>0\) and \(D>0\). There exist \(\delta_0>0\) and a finite \(C\), depending only on those five numbers, such that for every \(\delta\in(0,\delta_0)\) the lag has a unique stationary law and
\[
\Biggl|\mathbb{E}[J-J^\star]-\frac1{2\beta}\Bigl(1+\frac{D}{D_m}\Bigr)\Biggr|\le C\delta^2.
\]
Under this law the time average of \(J-J^\star\) converges almost surely to the stationary mean.

*Proof.* The bulk is the set where \(|Nx_\pm|\le 1\). Its radius is \(L_B\asymp 1/(\beta h\delta)\), which grows like \(1/\delta\). CD2 controls \(R\) on that growing set. The parameters \(\beta,h,D_m,D,N\) stay fixed while \(\delta\) shrinks, so constants may depend on them.

**Drift inside the bulk.** The instantaneous drift is \(\mu(L)=\delta(r_+-r_-)\). The linear lemma gives \(\mu_{\mathrm{lin}}=-a L\). The error \(\mu+a L\) is built from \(\varphi-\varphi_{\mathrm{lin}}\) by the same differences of \(z_\pm\) as in CD2, multiplied by \(\delta\rho\) rather than by the weights \(2\delta L+\delta^2\). Those differences are \(O(\delta^3(1+|L|^3))\) on \(|Nx_\pm|\le 1\), and \(\delta\rho=O(1/\delta)\), so
\[
|\mu+a L|\le K_N D_m\delta^2\bigl(\beta h+(\beta h)^2(1+L^2)+(\beta h)^3(1+L^4)\bigr)(1+|L|)
\]
with a constant \(K_N\) of the same origin as the coefficients in CD2. On \(|L|\ge 1\) and \(|\beta h\delta L|\le\eta\),
\[
|\mu+a L|\le a|L|\bigl(C_1\delta+C_2\eta+C_3\eta^2\bigr),
\]
with \(C_i\) depending only on \(N\). Choose \(\eta>0\) small and then \(\delta_0\) small so that the parenthesis is at most \(1/2\). Then, for \(\delta<\delta_0\) and \(1\le|L|\le L_B\), \(\mu\) has the sign of \(-L\) and \(|\mu|\ge(a/2)|L|\).

**Outside the bulk.** Take \(L>L_B\) (the other side is the same). Then \(x_-<0<x_+\) for small \(\delta\). A fitter mutant fixes at rate at least the neutral rate, so \(\varphi(x_-)\ge 1/N\). And \(\sinh(Nt)\ge N\sinh t\) for \(t\ge 0\), because \(\cosh(Nt)-\cosh t\ge 0\), hence \(\varphi(x)\le N^{-1}\exp(-(N-1)x/2)\) for \(x>0\). The uphill step satisfies \((N-1)x_+/2\ge\eta/2\). Therefore \(\varphi(x_-)-\varphi(x_+)\ge(1-e^{-\eta/2})/N\), and the restoring speed is at least
\[
v_{\mathrm{rest}}=\frac{D_m}{\delta}\bigl(1-e^{-\eta/2}\bigr).
\]
So \(G(L^2)\le -2 v_{\mathrm{rest}} L+2N D_m+2D\).

**Uniform second moment.** On the bulk, CD2 and the choice of \(\eta\) give \(R\le(a/2)L^2+K_0\) for \(|L|\ge 1\), with \(K_0\) independent of \(\delta\) (the pieces without an \(L^2\) are \(O(\delta^2)\) or, when an edge factor \(1/(\beta h)\) appears, a constant fixed by \(\beta\) and \(h\)). Thus \(G(L^2)\le -a L^2+2(D_m+D)+K_0\) on \(1\le|L|\le L_B\). Off the bulk the restoring speed is stronger. On the fixed interval \(|L|\le 1\), pairing the jumps gives \(G(L^2)\le K_1\) with \(K_1\) independent of small \(\delta\): the crude product \(\rho\cdot\delta\) is \(O(1/\delta)\), but \(r_+-r_-=\mu/\delta=O(1)\) and \(\delta^2(r_++r_-)\le 2N D_m\). Choose \(L_0\ge 1\) so that \(a L_0^2\) beats \(2(D_m+D)+K_0+1\). Then \(G(L^2)\le -L^2+K\) on the whole line, with \(K\) independent of small \(\delta\).

Existence and uniqueness for each fixed \(\delta\), when \(D>0\), do not need this uniformity. The jump rate is finite, \(G(L^2)\le -v_{\mathrm{rest}}|L|+C_\delta\) for large \(|L|\), and the Brownian piece is strong Feller and irreducible on \(\mathbb{R}\). That is one stationary law for each \(\delta\). The uniformity is the next sentence. Cut \(L^2\) off outside \(|L|<n\), use \(\int G(\phi_n)\,d\pi=0\) for the cutoff (it is in the domain), and pass to the limit by Fatou. The negative drift produces \(\mathbb{E}[L^2]\le K\), uniformly in small \(\delta\).

**Uniform exponential moment.** Let \(V=\cosh(\lambda L)\) with \(\lambda>0\) small, fixed, to be chosen. On \(L_0\le|L|\le L_B\),
\[
GV=(r_++r_-)\cosh(\lambda L)(\cosh(\lambda\delta)-1)+(r_+-r_-)\sinh(\lambda L)\sinh(\lambda\delta)+D\lambda^2\cosh(\lambda L).
\]
Here \(\cosh u-1\le u^2\) for \(|u|\le 1\), so the first term is at most \(2N D_m\lambda^2\cosh(\lambda L)\) for small \(\delta\). And \(\sinh(\lambda\delta)\ge\lambda\delta\), while \(r_+-r_-=\mu/\delta\le-(a/(2\delta))L\) for \(L>0\). The middle term is then at most \(-(a\lambda/2) L\sinh(\lambda L)\). Choose \(L_0\) large enough that \((a\lambda/2) L\tanh(\lambda L)\) beats \(2N D_m\lambda^2+D\lambda^2+1\) for \(|L|\ge L_0\). Then \(GV\le -\cosh(\lambda L)\) on that range. Off the bulk, \(v_{\mathrm{rest}}\asymp 1/\delta\) makes the same middle term more negative still. On \(|L|<L_0\) the paired expansion bounds \(GV\) by \(K_V\cosh(\lambda L)\), with \(K_V\) independent of small \(\delta\). Hence \(GV\le -V+K_V' 1_{|L|<L_0}\). Approximating \(V\) by compactly supported functions and using the uniform second moment to pass to the limit gives \(\mathbb{E}[V]\le M\), uniformly in small \(\delta\).

**The excess.** Split \(\mathbb{E}[R]\) into the bulk and the tail \(|L|>L_B\). On the bulk, CD2 and \(\mathbb{E}[L^4]\le M_4\) (which follows from the exponential moment) give an \(O(\delta^2)\) contribution. On the tail, CD2's second bound is \(O(|L|/\delta+L^2)\), and \(\mathbb{E}[|L|1_{|L|>L_B}]\le e^{-\lambda L_B/2}M'\). Since \(L_B\asymp 1/\delta\), the product with \(1/\delta\) is \(o(\delta^2)\). Thus \(|\mathbb{E}[R]|=O(\delta^2)\), and (I) is the claim. Positive recurrence gives the almost-sure time average. ∎

The bulk grows like \(1/\delta\). The comparison that keeps the moment finite is the drift inequality inside that bulk, \(\lvert\mu+a L\rvert\le(a/2)\lvert L\rvert\) for \(1\le|L|\le L_B\), not the restoring speed outside it. The outside speed is used only for the far tail.

**Sketches, not theorems.** Three extensions are not proved.

- *Ornstein–Uhlenbeck centre.* The state is the pair \((L,\theta^\star)\). The world's generator on \(L^2\), \(L\theta^\star\) and \(\theta^{\star 2}\) is exact. The jump defect of \(L^2\) is still \(R(L)\). The jump defect of the cross moment is not: a jump changes \(L\theta^\star\) by \(\delta\theta^\star\), so the defect relative to the Langevin drift \(-a L\) is \(\bigl(\delta(r_+-r_-)+a L\bigr)\theta^\star\). That is a different function of \((L,\theta^\star)\). Calling it \(R(L)\) is wrong. The estimate is not written.
- *Constant velocity.* The same cross-term issue does not arise, because the world's drift \(-v\) is a function of \(L\) alone in the moving frame. The moment identity for \(L\) and \(L^2\) has the same shape as (I), but the Lyapunov is a piecewise-deterministic process with no Brownian piece, and the strong-Feller step used above does not apply. Not written.
- *Non-diagonal \(H\), or several coordinates.* A step on one axis changes the quadratic form through the whole row of \(H\). The defect is a sum of axis contributions, not the scalar \(R\). Not written.

## 5. Theorem CD4 (path measure)

**Theorem CD4.** Same scaling and same one-dimensional Brownian quadratic lag as CD3. Let the initial laws \(\nu_\delta\) converge weakly to a probability \(\nu\), and suppose \(\sup_\delta\int L^2\,d\nu_\delta<\infty\). Then the law of the lag in \(D([0,\infty),\mathbb{R})\) converges weakly to the law of the Langevin lag started from \(\nu\).

Tightness of the initials is not enough. Point masses at \(0\) and at \(1\), alternating in \(\delta\), are tight and have a uniform second moment, and the path laws alternate between two different Langevin laws. Convergence of the initial laws is the hypothesis.

The topology is Skorokhod's. The citation is Ethier and Kurtz, *Markov Processes: Characterization and Convergence*, Wiley 1986, doi 10.1002/9780470316658, Chapter 4, §8, Theorem 8.2 and Corollary 8.7 (cadlag paths; the proof of the corollary stops the martingale and calls Theorem 8.2). "Theorem 4.8.2" in the audit is this statement. Three hypotheses are checked, for this one-dimensional Brownian lag only.

1. **Generator convergence on \(C_c^\infty\).** Let \(f\) vanish outside a fixed compact. For small \(\delta\), \(Gf(L)=0\) whenever \(L\) is more than \(\delta\) from that compact, and the Langevin generator vanishes there too. On the remaining fixed compact, \(|Nx_\pm|=O(\delta)\to 0\). Taylor's theorem with remainder gives
   \[
   f(L\pm\delta)-f(L)=\pm\delta f'+\tfrac12\delta^2 f''+O(\delta^3),
   \]
   uniformly in \(L\). Pairing and substituting the linear lemma, the drift coefficient is \(-a L+o(1)\) and the second-moment weight is \(2 D_m-a\delta^2/2+o(1)\), uniformly on that compact. The Brownian piece \(D f''\) is exact. Therefore \(\|Gf-\mathcal{L}f\|_\infty\to 0\). This is an expansion of a general test function. It is not the bound CD2, which is only for \(L^2\).

2. **Compact containment.** Fix \(T\) and \(R\). For small \(\delta\), the interval \(|L|\le R\) lies inside the bulk, so the drift comparison of CD3 gives \(G(L^2)\le -a L^2+C_R\) there, with \(C_R\) independent of small \(\delta\). Stop at \(\tau_R=\inf\{t:|L_t|\ge R\}\). Dynkin's formula yields \(\mathbb{E}[L_{t\wedge\tau_R}^2]\le\mathbb{E}[L_0^2]+C_R t\). Hence \(\mathbb{P}(\tau_R\le T)\le(\sup\mathbb{E}[L_0^2]+C_R T)/R^2\), uniformly in small \(\delta\). That is compact containment on \([0,T]\). The \(1/\delta\) tail is not needed: the process is stopped at a fixed \(R\) that sits inside the bulk.

3. **Well-posedness.** The limit is a linear stochastic differential equation with Lipschitz coefficients. It has a unique strong solution, so its martingale problem on \(D([0,\infty),\mathbb{R})\) has one solution for each initial law.

Corollary 8.7 then gives the weak convergence. Finite-horizon convergence does not by itself give convergence of stationary means. That is CD3.

## 6. What remains open

- Ornstein–Uhlenbeck centre, constant velocity, and a non-diagonal or multi-coordinate Hessian. Sketches in §4. The cross-moment defect is not \(R(L)\).
- The weak-mutation limit \(N\mu_{\mathrm{gen}}\to 0\) from the full Moran process to the monomorphic chain.
- A non-quadratic \(J\). Several basins bring a time scale the diffusion approximation does not see.
- A numerical value of \(C\) in CD3 with the Lyapunov moment removed. Section 7 measures the ratio for one Brownian family.

## 7. Numerical check

`tools/chain_diffusion_checks.py`, quick mode under pytest, `--full` written to `theory/chain_diffusion_checks/results_full.json`. The static rows with a visible gap test CD1 against the leading term. Rows whose gap sits below float precision are computed in `decimal` at 40 places, so a \(10^{-14}\) tolerance cannot pass a bound of size \(10^{-20}\). The moving rows solve the exact forward equation. The identity check asks whether that density is stationary for \(L^2\). The comparison of the same excess to \(\frac1{2\beta}(1+D/D_m)\) is the check of the limit formula. A separate grid checks the linear defect \(-a\delta^2/2\) and the CD2 bound, including the point where a constant depending only on \(N\) fails.

The full run is 10 stationary solves. The relative error divided by \(\varepsilon_{\mathrm{lat}}\) is at most \(0.094\) (that row is \(N=5\), \(\delta=0.25\), \(D/D_m=1\)). At \(N=20\) and \(D/D_m=1\) the ratio is \(0.069\) across \(\delta\in\{0.50,0.35,0.25,0.18\}\). It is \(0.064\) at \(N=100\), and \(0.043\) and \(0.050\) at \(D/D_m=0.25\) and \(4\). The chain sits above the diffusion value. The identity (I) matches the solver's excess gap on every row. These ratios measure \(C\). They are not a substitute for CD3.

## 8. Prior art

No constant is taken from a paper. The diffusion limit as a technique is Ethier and Kurtz, already cited in the drift note (doi checked there on 21 November 2026). The stationary identity for (L) is DS1, prior art in substance (Held, Nourmohammad and Lässig 2014). Poisson summation and Cauchy's estimate are classical. What is new is the passage for this chain: the exact defect identity (I), the static exponential bound, and the \(O(\delta^2)\) stationary excess.
