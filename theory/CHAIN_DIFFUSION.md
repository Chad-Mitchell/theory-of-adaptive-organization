# From the substitution chain to the diffusion limit

*Sunday 22 November 2026. Branch `diffusion-convexity-2026-11-21`, draft PR. Written by one executor for Chad Mitchell; a self-check, not an independent review. Closes the passage that `theory/DRIFT_SELECTION.md` §3 left open for a quadratic cost: the exact weak-mutation chain's stationary excess converges to the excess of the Langevin limit (L), including the factor \(1+D/D_m\). It does not change the Part 2 hypothesis sentence, and it does not edit a locked preregistration or hash file.*

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
| CD2 | Generator of the chain on a quadratic cost equals the Langevin generator plus a defect \(R\) controlled by the nonlinearity of the Moran fixation map | **PROVED** |
| CD3 | One coordinate, quadratic, Brownian centre: the lag has a unique stationary law, and its excess is the DS1 value plus an error \(O(\delta^2)=O(\varepsilon_{\mathrm{lat}}/\beta)\) | **PROVED** |
| CD3d | The same limit and the same order, summed over coordinates, when \(H\) and the world's noise are diagonal in the lattice basis (curvature still cancels in the limit). OU and constant velocity: the world's generator is exact, and the same defect \(R\) is the only error | **PROVED** |
| CD4 | In that scaling the lag converges weakly in Skorokhod space on \([0,\infty)\) to the Langevin diffusion, in the sense of Ethier and Kurtz, Chapter 4, §8 | **PROVED**, by the generator theorem once CD2 and the Lyapunov compact-containment are granted |

**What stays open.** A non-quadratic cost (several basins, SA4). A moving Hessian. The weak-mutation limit from the full Moran population down to the monomorphic chain. A numerical value of the \(O(\delta^2)\) constant that does not depend on the Lyapunov moment (the proof shows the constant is finite; the runs below measure it). Anisotropic mutation that is not diagonal in the lattice basis is the same argument with \(D_m I\) replaced by \(M\), and is not written out.

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

The fixation map extends to an entire function of \(z=Nx\) by the removable definition
\[
N\varphi(x)=\frac{N\sinh(x/2)}{\sinh(Nx/2)}\exp\bigl(-(N-1)x/2\bigr).
\]
Call this \(f(z)\). Its poles are at \(z=2\pi i k\), \(k\neq 0\).

**Lemma (Cauchy bound).** For \(N\ge 2\) and \(|z|\le 1\),
\[
\bigl|f(z)-\bigl(1+f'(0)z\bigr)\bigr|\le \tfrac1{12}z^2+3.4\,|z|^3.
\]
*Proof.* The power series of \(\sinh\) has positive coefficients, so \(|\sinh(u)|\le\sinh(|u|)\). Thus for \(|u|\le 1/2\), \(|\sinh(u)/u|\le\sinh(|u|)/|u|\le\sinh(1/2)/(1/2)<1.043\), since \(t\mapsto\sinh t/t\) increases on \((0,\infty)\). On \(|z|=2\) and \(N\ge 2\), \(|z/(2N)|\le 1/2\), so \(|N\sinh(z/(2N))|\le 1.043\). Also \(|\sinh(z/2)|\ge\sin 1>0.841\) (the only zero of \(\sinh\) near the origin is the origin, inside the circle), and \(|\exp(-(N-1)z/(2N))|\le e\). Hence \(|f|<3.4\) on \(|z|=2\). For \(|z|\le 1\) the circle of radius 1 about \(z\) stays inside \(|w|\le 2\), so \(|f'''|\le 6\cdot 3.4\). The remainder after the quadratic Taylor polynomial is at most \(3.4|z|^3\). The quadratic coefficient satisfies \(|f''(0)/2|=(N-1)(N-2)/(12N^2)\le 1/12\), and \(f_{\mathrm{lin}}\) drops that quadratic piece, so \(|f-f_{\mathrm{lin}}|\le\tfrac1{12}z^2+3.4|z|^3\). ∎

The linear piece \(f_{\mathrm{lin}}(z)=1-((N-1)/(2N))z\) is exactly the first order used in the drift note. Substituting it for \(\varphi\) produces, after pairing \(+\) with \(-\), the Langevin drift \(-a L\) and the neutral diffusion \(2D_m\) on \(L^2\), with no remainder: the algebra is the one in `theory/DRIFT_SELECTION.md` §3, and every \(N\) cancels into \(\beta=\alpha(N-1)\) and \(D_m=\mu\delta^2/2\). The defect \(R\) is what the lemma bounds.

**Theorem CD2.** On the event \(|Nx_\pm|\le 1\),
\[
|R(L)|\le C_N D_m\,(\beta h\delta)^2\bigl(1+(\beta h) L^2\bigr)\bigl(1+L^2\bigr)
\]
for a constant \(C_N\) that depends only on \(N\) (the lemma gives a value; any larger constant is allowed). Off that event, \(|\varphi|\le 1\), so \(|R(L)|\le (2N D_m h/\delta)|L|+2N D_m+2a L^2+2D_m\).

The first bound is \(O(\delta^2(1+L^4))\) on any region \(|L|\le \eta/(\beta h\delta)\) with \(\eta\) fixed. The second bound is large, and is only used on a far tail.

## 4. Theorem CD3 (stationary excess)

**Theorem CD3.** Fix \(N\ge 2\), \(\beta>0\), \(h>0\), \(D_m>0\), \(D>0\). There exist \(\delta_0>0\) and a finite \(C\), depending only on those parameters, such that for every \(\delta\in(0,\delta_0)\) the lag has a unique stationary law and
\[
\Biggl|\mathbb{E}[J-J^\star]-\frac1{2\beta}\Bigl(1+\frac{D}{D_m}\Bigr)\Biggr|\le C\delta^2.
\]
Equivalently the error is \(O(\varepsilon_{\mathrm{lat}}/\beta)\), since \(\varepsilon_{\mathrm{lat}}=\delta^2\beta h(1+D/D_m)\) with \(h\) and \(D/D_m\) fixed. Under this law the time average of \(J-J^\star\) converges almost surely to the stationary mean, because the lag is positive recurrent.

*Proof.* Choose \(\eta\in(0,1)\) small enough that the bulk bound of CD2 satisfies \(|R(L)|\le (a/2) L^2\) whenever \(|\beta h\delta L|\le\eta\) and \(|L|\ge 1\). Such an \(\eta\) exists because the prefactor of CD2 carries \((\beta h\delta L)^2\le\eta^2\), and \(\eta^2\) can be made smaller than any fixed multiple of \(a\). Let \(L_B=\eta/(\beta h\delta)\). Call \(|L|\le L_B\) the bulk.

On the bulk, \(G(L^2)=\mathcal{L}(L^2)+R\le -2a L^2+2(D_m+D)+(a/2)L^2\le -(a/2)L^2+2(D_m+D)\) once \(|L|\ge 1\), up to adjusting \(\eta\) to absorb the compact piece \(|L|<1\) into the constant. Off the bulk, take \(L>L_B\) (the negative side is the same). Write \(y=\alpha h\delta L\) and \(c=\alpha h\delta^2/2\), so \(x_+=y+c\) and \(x_-=-y+c\). For \(\delta\) small, \(L_B>\delta\) and \(y>c\), hence \(x_-<0<x_+\). A fitter mutant fixes with probability at least the neutral value, so \(\varphi(x_-)\ge 1/N\). For the uphill step, \(\sinh(Nt)\ge N\sinh t\) for \(t\ge 0\) because \(t\mapsto\cosh(Nt)-\cosh t\) is nonnegative (\(Nt\ge t\) and \(\cosh\) increases on \([0,\infty)\)), so \(\varphi(x)\le N^{-1}\exp(-(N-1)x/2)\) for \(x>0\). And \((N-1)x_+/2=\beta h\delta L/2+\beta h\delta^2/4\ge\eta/2\), the quadratic piece only adding. Therefore
\[
\varphi(x_-)-\varphi(x_+)\ge\frac{1-e^{-\eta/2}}{N},
\]
and the restoring speed is at least
\[
v_{\mathrm{rest}}=\delta\cdot\rho\cdot\frac{1-e^{-\eta/2}}{N}=\frac{D_m}{\delta}\bigl(1-e^{-\eta/2}\bigr).
\]
Hence \(G(L^2)\le -2 v_{\mathrm{rest}} L+2N D_m+2D\), and in particular \(G(L^2)\le -v_{\mathrm{rest}} L+C_1\) off the bulk.

The same drift beats a multiple of \(\cosh(\lambda L)\) for \(\lambda>0\) fixed and \(\delta\) small: the jump variance rate is at most \(2N D_m\) and the world's variance rate is \(2D\), while \(v_{\mathrm{rest}}\to\infty\), so the first-derivative term dominates the second-derivative term outside a fixed compact. Foster's criterion gives a unique stationary law (the Brownian piece makes the process strong Feller and irreducible on \(\mathbb{R}\)) and a uniform exponential moment: \(\mathbb{E}[\cosh(\lambda L)]\le M\) for some \(M<\infty\) and all small \(\delta\). Every polynomial moment is therefore bounded uniformly in small \(\delta\). In particular \(\mathbb{E}[L^4]\le M_4<\infty\).

Split \(\mathbb{E}[R]=\mathbb{E}[R\,1_{\mathrm{bulk}}]+\mathbb{E}[R\,1_{\mathrm{tail}}]\). The bulk bound and \(\mathbb{E}[L^4]\le M_4\) give \(|\mathbb{E}[R\,1_{\mathrm{bulk}}]|\le C_b\delta^2\). On the tail, \(|R|\le (2N D_m h/\delta)|L|+C_2(1+L^2)\) and \(\mathbb{E}[|L|1_{|L|>L_B}]\) is \(O(\exp(-c/\delta))\) by the exponential moment, since \(L_B\propto 1/\delta\). That product is \(o(\delta^2)\). Hence \(|\mathbb{E}[R]|\le C'\delta^2\) for small \(\delta\), and (I) is the claim.

Positive recurrence gives the almost-sure convergence of time averages of \(J-J^\star\), which is integrable. ∎

The original gap in the drift note was uniform integrability of the stationary excess. For this quadratic Brownian lag it is the exponential moment above: \(\mathbb{E}[L^2]\) stays bounded as \(\delta\to 0\), so the family is uniformly integrable, and the means converge.

**Diagonal coordinates (CD3d).** If \(H=\mathrm{diag}(h_1,\ldots,h_d)\) and the centre is Brownian with independent coordinates of variance rates \(2D_k\), a step along axis \(k\) changes only coordinate \(k\), and the coordinates of the lag are independent copies of the one-dimensional process. CD3 applies to each, and the errors add. With \(D_k=D\) the limit is \(\frac{d}{2\beta}(1+D/D_m)\), independent of the \(h_k\). Curvature cancels in the limit. It does not cancel in the rate: coordinate \(k\) contributes \(O(\delta^2 h_k)\).

**OU and constant velocity.** The world is exogenous, so its generator is exact. For an OU centre the state is the pair \((L,\theta^\star)\), the world's piece of the generator of \(L^2\), \(L\theta^\star\) and \(\theta^{\star 2}\) has no \(\varphi\) in it, and the only defect is the same \(R(L)\) from the jumps. The Lyapunov algebra of DS1(a) therefore holds with an extra \(\mathbb{E}[R]\), and the same bulk/tail bound gives an \(O(\delta^2)\) error on the DS1 trace. For a constant velocity the same is true of the test functions \(L\) and \(L^2\): the mean lag is \(-v/a\) plus \(O(\delta^2)\), and the excess is DS1(c) plus \(O(\delta^2)\), provided \(|v|\) is small enough that a stationary lag exists, which is DS2's regime \(|v|<v_{\max}\) and, for the linearisation, the drift note's \(|v|\ll D_m/\delta\). The condition \(|v|\ll D_m/\delta\) becomes automatic as \(\delta\to 0\) with \(v\) fixed. The equality case \(|v|=v_{\max}\) stays outside, as in DS2.

**Non-diagonal \(H\).** The same pairing along each lattice axis produces the drift \(-D_m\beta H L\) and diffusion \(2D_m I\), and the defect on the quadratic form \(\tfrac12 L^\top H L\) is a sum of one-dimensional defects of the kind bounded in CD2, with \(|HL|\) in place of \(h|L|\). The Lyapunov function \(L^\top H L\) gives the same uniform moments. The limit is DS1(b), with an \(O(\delta^2)\) error. This is the same proof; the bookkeeping is the matrix trace already written in the drift note.

## 5. Theorem CD4 (path measure)

**Theorem CD4.** Under the scaling of §0, with \(N,\beta,H,D_m,D\) fixed and \(H\) positive definite, the law of the lag on \(D([0,\infty),\mathbb{R}^d)\) converges weakly to the law of the Langevin lag, for any tight sequence of initial conditions with a uniform second moment.

The topology is the Skorokhod topology. The argument is the generator-convergence theorem in Ethier and Kurtz, *Markov Processes: Characterization and Convergence*, Wiley 1986, doi 10.1002/9780470316658, Chapter 4, §8: Theorem 8.2, and Corollary 8.7 for processes with paths in \(D([0,\infty))\). (The audit's "Theorem 4.8.2" is this theorem. The section number was read from the book's contents and from the text of §8; the hypotheses used below are the ones the corollary states: generator convergence on a core, compact containment, and well-posedness of the limit.)

Three inputs, each checked:

1. **Generator convergence on a core.** On any fixed compact, \(\varepsilon_{\mathrm{lat}}\to 0\) forces \(|Nx_e|\to 0\) uniformly, so CD2 gives \(\|G_\delta f-\mathcal{L}f\|_\infty\to 0\) for every \(f\in C_c^\infty\). Linear growth of the coefficients is cut off by the compact, which is what the corollary's stopped convergence uses.
2. **Compact containment.** The Lyapunov function of CD3 bounds \(\mathbb{E}[\sup_{t\le T}|L_t|^2]\) uniformly in small \(\delta\), by the same drift inequality integrated up to time \(T\).
3. **Well-posedness.** The limit is a linear stochastic differential equation with Lipschitz coefficients. It has a unique strong solution, so its martingale problem is well-posed.

Finite-horizon convergence does not by itself give convergence of stationary means. That is CD3, and it uses the identity (I) rather than an extra tightness argument on path space. The two theorems meet: every weak limit point of the stationary laws is invariant for (L), and (L) has one invariant law, the Gaussian whose excess is DS1.

## 6. What remains open

- The weak-mutation limit \(N\mu_{\mathrm{gen}}\to 0\) from the full Moran process to the monomorphic chain. Standard, and not re-proved.
- A non-quadratic \(J\). Several basins bring metastability on a time scale the diffusion approximation does not see. SA4 stays as it was.
- A moving Hessian, frequency dependence, clonal interference, and a world the lineage moves (CX2).
- A fully numerical \(C\) in CD3 with no moment left inside it. The runs give the ratio \(|\mathrm{rel.\ error}|/\varepsilon_{\mathrm{lat}}\) directly.

## 7. Numerical check

`tools/chain_diffusion_checks.py`, quick mode under pytest, `--full` written to `theory/chain_diffusion_checks/results_full.json`. The static rows test CD1's bound and its leading term. The moving rows solve the exact forward equation of the lag and compare with DS1.

The full run is 10 stationary solves. The relative error divided by \(\varepsilon_{\mathrm{lat}}\) is at most \(0.094\) (that row is \(N=5\), \(\delta=0.25\), \(D/D_m=1\)). At \(N=20\) and \(D/D_m=1\) the ratio is \(0.069\) across \(\delta\in\{0.50,0.35,0.25,0.18\}\). It is \(0.064\) at \(N=100\), and \(0.043\) and \(0.050\) at \(D/D_m=0.25\) and \(4\). The chain sits above the diffusion value. The identity (I) matches the solver's excess gap on every row. These ratios measure \(C\). They are not a substitute for CD3.

## 8. Prior art

No constant is taken from a paper. The diffusion limit as a technique is Ethier and Kurtz, already cited in the drift note (doi checked there on 21 November 2026). The stationary identity for (L) is DS1, prior art in substance (Held, Nourmohammad and Lässig 2014). Poisson summation and Cauchy's estimate are classical. What is new is the passage for this chain: the exact defect identity (I), the static exponential bound, and the \(O(\delta^2)\) stationary excess.
