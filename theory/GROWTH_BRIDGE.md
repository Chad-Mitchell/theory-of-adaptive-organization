# The master equation as a limit of growth selection

*Sunday 22 November 2026, America/New_York. Branch `growth-bridge-2026-11-22`. Written by one executor for Chad Mitchell. A self-check, not an independent review. It does not edit a locked preregistration, a hash, or a LOCK file. It does not change the Part 2 hypothesis sentence. THEORY.md remains the canonical statement. The equation there stays the statement of the problem.*

*The general form is on `main` (PR #161, merged; confirm PR #164). The independent review of that note is PR #163. This note starts from Lemma LY as merged. Revised after the READY-WITH-FIXES review of draft PR #166 (PR #167, reviews/growth_bridge_2026-11-22/REVIEW.md on branch `review-pr166-2026-11-22`; confirm review in `reviews/CONFIRM_PR166.md`). The repairs below are a self-check of those fixes, not an independent review of the repair.*

## 0. The result, in one statement

**On a gapped finite menu, weak selection recovers the ranking only.** The diffusion limit keeps \(\mu-\sigma^2/2\). An interior stake separates the argmaxes. The term list and the cap are inputs, so the master equation remains an assumption outside that scoped ranking. The common design minimizes a linear cost only when that cost is already the form of the offspring mean. A ruin level set is a half-space in an exponent coordinate, after a linear approximation in the Galton–Watson plane, and a bounded interval of refresh time on the published path of Lemma B9. H3, read as a partial with the other bads held fixed, holds for memory, acquisition, and attention only under a budget map with a positive price. Expected task loss fails by LY-1. A scalar ruin probability is not a pathwise coordinate. "From first principles" stays false.

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

The sentence is unchanged. "Strongly selected" in THEORY §3 is the operational definition and is not rewritten here.

The additive master equation, copied from THEORY §3, is

\[
J=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L
\qquad\text{subject to}\qquad P(\mathrm{ruin})\le\varepsilon .
\]

Lemma LY says a pure design's long-run growth is \(\lambda=\mathbb{E}[\log W]\), when that expectation is finite. GF3 says the display above is the special case of risk-neutral expected currency, linear nonnegative prices, and a half-space ruin cap. Those two clauses are the gap this note tries to close, and does not close.

## 1. Status words

**PROVED** means proved inside the stated model, which says nothing by itself about nature. **NUMERICAL** means computed, not proved. **OPEN** means not derived or not tested, not refuted. **FALSE** means the claim does not follow, and a counterexample is given. Nothing here is a field result.

## 2. What the repository already contains

Grep before any new name. The hits that bear on this limit:

- **Kelly, CT42, CT43.** `theory/DYNAMICS.md` CT42: with a shared shock, lineage growth picks the mixture \(q^\star=0.26\), and expected offspring picks the pure lean design (means \(1.235\) and \(1.0425\)). CT43(i): if every cost is a fraction of the reserve, \(W'=W\exp(-(c+w\ell))\) and the time-average log growth equals \(-J\). That identity assumes the cost. CT43(iii): a long-horizon ruin threshold fixes the sign of the time-average growth and does not fix the ranking. The worked pair is recomputed in §4. CL21 credits Kelly 1956 for the time average.
- **Gillespie.** DYNAMICS §3 records Gillespie 1974 as an \(O(1/N)\) correction from within-generation variance in offspring number. That term carries \(1/N\). The expansion in §3 does not.
- **Lundberg.** Lemma B9 and V2: on the published path, \(\tau_S=0.236207526722\) and \(\tau_E=0.316227766017\). The survival exponent and expected currency have different argmins. THEORY's correction to Theorem L: they agree in the limit where the reserve's own noise dominates. That is a limit inside one model, not an identity of the objectives.
- **PD6.** In a Gaussian world whose variance diverges, the raw stock \(I(M_t;X_t)\) diverges for every uniformly accurate design. That is a statement about which memory functional can be a viability coordinate. It is not a variance penalty on offspring.
- **Lande, and the exponential map.** SA3 in `theory/SELECTION_AXIOMS.md`: Lande's gradient of log mean fitness equals the Malthusian gradient only in the weak-selection limit. A2-L puts \(m=m_0-\alpha J\) in by assumption and says the note does not reopen the term list.
- **Lemma LY and GF3.** H1–H2 give the complete preorder \(\lambda\). H3, offspring strictly decreasing in each chosen coordinate, is an extra hypothesis. Corollary LY-c gives a nonnegative linear cost in growth units when \(\log W=-\langle c(\omega),z\rangle\). GF3(R-a) and (R-b) are still required before that cost is the master equation.

No existing row derives the master equation as a limit of \(\lambda\). This note does not derive it either.

## 3. (a) The small-noise expansion

Let \(W>0\) and write \(X=W-1\). On \(|X|\le 1/2\), Taylor's theorem with the Lagrange remainder gives

\[
\log(1+X)=X-\frac{X^2}{2}+R_2(X),
\qquad
|R_2(X)|\le\frac{8}{3}|X|^3.
\]

The third derivative of \(\log(1+x)\) is \(2/(1+x)^3\), so the remainder after two terms is \(X^3/(3(1+\xi)^3)\) for some \(\xi\) between \(0\) and \(X\). On \(|X|\le 1/2\), \(|1+\xi|\ge 1/2\), and the constant \(8/3\) follows. Taking expectations,

\[
\mathbb{E}[\log W]
=\mathbb{E}[W-1]-\frac12\mathbb{E}[(W-1)^2]+\mathbb{E}[R_2]
=\mathbb{E}[W-1]-\frac12\mathrm{Var}(W)-\frac12(\mathbb{E}[W-1])^2+\mathbb{E}[R_2].
\]

**The unscoped identity is FALSE.** The sentence "\(\mathbb{E}[\log W]=\mathbb{E}[W-1]-\mathrm{Var}(W)/2+O(\text{third moment})\)" drops \(-\frac12(\mathbb{E}[W-1])^2\). For deterministic \(W=1.2\), the variance is zero, \(\log 1.2=0.182321556794\), and \(\mathbb{E}[W-1]-\mathrm{Var}(W)/2=0.2\). The gap is \(0.017678443206\). The dropped term is \((\mathbb{E}[W-1])^2/2=0.02\), which is larger than the cubic piece of the series (\(0.2^3/3=0.002\overline{6}\)).

**Theorem GB-diff (PROVED in-model).** Diffusion scaling. Let \(Z=\pm 1\) with equal probability, \(\mu\in\mathbb{R}\), \(\sigma>0\), and

\[
W=1+\mu\,\Delta t+\sigma\sqrt{\Delta t}\,Z,
\]

with \(\Delta t>0\) small enough that \(|W-1|\le 1/2\). Then \(\mathbb{E}[W-1]=\mu\,\Delta t\). Because \(\mathbb{E}[Z]=0\) and \(\mathbb{E}[Z^2]=1\), \(\mathrm{Var}(W)=\sigma^2\Delta t\) exactly, and \((\mathbb{E}[W-1])^2=(\mu\,\Delta t)^2\). The third-moment remainder is \(O((\Delta t)^{3/2})\), which absorbs the squared-mean term. Hence

\[
\mathbb{E}[\log W]
=\mathbb{E}[W-1]-\frac12\mathrm{Var}(W)+O((\Delta t)^{3/2}),
\]

and the growth rate per unit time converges to the diffusion value

\[
\frac{\mathbb{E}[\log W]}{\Delta t}\to\mu-\frac{\sigma^2}{2}.
\]

*Proof.* Expand \(\mathbb{E}[X^2]=(\mu\Delta t)^2+\sigma^2\Delta t\). Then \(\mathrm{Var}(W)=\mathbb{E}[X^2]-(\mathbb{E}[X])^2=\sigma^2\Delta t\). The Lagrange bound gives \(|\mathbb{E}[R_2]|\le(8/3)\mathbb{E}[|X|^3]\). Each of \(|\mu\Delta t|\) and \(\sigma\sqrt{\Delta t}\) is \(O(\sqrt{\Delta t})\), so \(\mathbb{E}[|X|^3]=O((\Delta t)^{3/2})\). Dividing by \(\Delta t\) sends the remainder to zero and leaves \(\mu-\sigma^2/2\). □

**This scaling keeps the variance penalty at leading order.** Take \(\mu=0.2\) and \(\sigma^2=0.5\). The drift is positive. The limiting growth rate is \(0.2-0.25=-0.05\). At \(\Delta t=10^{-4}\) the realized rate is \(-0.049998\). Doing nothing, \(\mu=\sigma=0\), has growth rate \(0\) and drift \(0\). Expected offspring selects the risky design. Growth selects doing nothing. Sending the step to zero does not remove the disagreement: both the drift and the variance penalty are order \(\Delta t\) per step, and order \(1\) per unit time.

**Theorem GB-menu (PROVED in-model).** Weak selection on a finite menu. Let \(W_i=1+\varepsilon X_i\) with \(\varepsilon|X_i|\le 1/2\) almost surely, \(\mathbb{E}|X_i|^3\le M\), and \(\mathbb{E}[X_1]\ge\mathbb{E}[X_j]+\gamma\) for every \(j\neq 1\), with \(\gamma>0\). Then there exists \(\varepsilon_0>0\) such that for all \(\varepsilon\in(0,\varepsilon_0)\),

\[
\lambda_1(\varepsilon)>\lambda_j(\varepsilon).
\]

The expansion used in the proof is

\[
\lambda_i=\varepsilon\,\mathbb{E}[X_i]-\frac{\varepsilon^2}{2}\mathbb{E}[X_i^2]+R_i,
\qquad
|R_i|\le\frac{8}{3}\varepsilon^3 M.
\]

*Proof.* Lyapunov's inequality gives \(\mathbb{E}[X_i^2]\le(\mathbb{E}|X_i|^3)^{2/3}\le M^{2/3}\), a bound independent of \(\varepsilon\). The difference of growth rates is at least \(\varepsilon\gamma-\varepsilon^2 M^{2/3}-(16/3)\varepsilon^3 M\). Divide by \(\varepsilon>0\). What remains is \(\gamma-\varepsilon M^{2/3}-(16/3)\varepsilon^2 M\), which tends to \(\gamma\) as \(\varepsilon\to 0\). □

The leading correction on this menu is \(-\frac12\mathbb{E}[(W-1)^2]=-\frac12\mathrm{Var}(W)-\frac12(\mathbb{E}[W-1])^2\), of order \(\varepsilon^2\). It does not flip a gap of order \(\varepsilon\). It does flip a tie, and it flips a gap once \(\varepsilon\) is large enough that the second-moment gap exceeds the mean gap.

**Counterexample, a mean gap the second moment flips (PROVED in-model).** \(\varepsilon=0.2\). Design A has \(X=0\). Design B has \(X=\pm 1\) with probabilities \(0.525\) and \(0.475\), so \(\mathbb{E}[X]=0.05\), not \(0\), and \(\mathbb{E}[X^2]=1\). Then \(\mathbb{E}[W_B-1]=0.01>0=\mathbb{E}[W_A-1]\), while

\[
\lambda_B=0.525\log 1.2+0.475\log 0.8=-0.010274369557<0=\lambda_A.
\]

Expected offspring selects B. Growth selects A. The means differ: \(\mathbb{E}[X_B]=0.05\). The equal-mean case, \(X=\pm 1\) with equal probability at the same \(\varepsilon\), has growth \(\frac12\log 0.96=-0.020411\), and the mean ties. That ranking is Gillespie's 1977 principle. The first-order truncation ties that equal-mean pair and the third-moment pair below, and it ranks the mean-gap pair by the mean. The second-order truncation separates the equal-mean pair, whose second moments differ, and it ties the third-moment pair. The weak-selection menu of Theorem GB-menu is a different limit: there the gap stays fixed while \(\varepsilon\to 0\), and the second-moment term cannot flip it.

**Counterexample, equal means and equal second moments (PROVED in-model).** \(\varepsilon=0.05\). The symmetric law \(X=\pm 1\) with equal probability has mean \(0\), second moment \(1\), third moment \(0\). The law with masses \(4/9,4/9,1/9\) on \(-1,1/2,2\) has the same mean, the same second moment, and third moment \(1/2\). The growth rates differ by \(1.905984\times 10^{-5}\). The cubic prediction \((\varepsilon^3/3)\cdot(1/2)=2.083333\times 10^{-5}\) matches that difference within \(2\times 10^{-6}\). Expected offspring ties the two laws. The variance penalty ties them. Growth ranks the skewed law higher. So "expected currency plus a variance penalty" is itself only the truncation of the series.

**Counterexample, the stake inside the design (PROVED in-model).** Even-money bet, win probability \(0.6\), stake \(f\in[0,0.99]\), factor \(W=1+f\xi\) with \(\xi=\pm 1\). Then \(\mathbb{E}[W-1]=0.2f\), maximized at the right endpoint \(f=0.99\). The growth rate

\[
\lambda(f)=0.6\log(1+f)+0.4\log(1-f)
\]

has derivative \(0.6/(1+f)-0.4/(1-f)\), zero at \(f^\star=0.2\), and \(\lambda(0.2)=0.020135513551>\lambda(0.99)\). H2 applies on this interval because \(W\ge 0.01\). The two argmaxes differ by \(0.79\).

**What "per-step stakes tend to zero" adds.** Replace the factor by \(1+\varepsilon f\xi\) with \(f\in[0,1]\). The growth maximizer is \(\min(1,0.2/\varepsilon)\). For \(\varepsilon<0.2\) it sits on the corner \(f=1\), which is also the expected-offspring maximizer. The agreement is the agreement of two corner solutions: the Kelly stake \(0.2/\varepsilon\) has left the box. Restore the box to \([0,1/\varepsilon]\), so an order-1 fraction of wealth remains feasible, and the maximizers are \(0.2/\varepsilon\) and \(1/\varepsilon\) at every \(\varepsilon\). Vanishing exposure recovers expected-offspring selection only by pushing the growth maximizer out of the feasible set.

**What the penalty matches in the repository.**

- It matches Kelly, CT42, and the geometric-mean term in CT43. The coin already in CL21, factors \(1.5\) and \(0.6\) with equal probability, has \(\mathbb{E}[W-1]=0.05\) and \(\mathbb{E}[\log W]=\frac12\log 0.9=-0.052680257829\). The sign flips. \(\mathbb{E}[W-1]-\mathrm{Var}(W)/2=-0.05125\), short of the logarithm by \(0.001430257829\), which is the squared-mean piece plus the cubic remainder. The second-moment form \(\mathbb{E}[W-1]-\frac12\mathbb{E}[(W-1)^2]=-0.0525\) lands within \(2\times 10^{-4}\) of the logarithm. CT42's shared shock is the same mechanism at finite noise: factors \(1.30\) and \(0\), and \(1.05\) and \(0.90\), are outside the disk where a cubic remainder controls the ranking. The mixture \(q^\star=0.26\) stays a fact. The expansion does not erase it.
- It matches the prior art named in §7: Lewontin and Cohen 1969 for \(\mathbb{E}[\log W]\) as the growth rate, Dempster 1955 and Frank for the geometric mean, Gillespie 1977 for selection on offspring-number variance. The algebra above is Taylor's theorem. No constant is copied from those texts.
- It does not match Gillespie 1974 as DYNAMICS uses that paper. The 1974 correction is \(O(1/N)\) and vanishes for an infinite population. The penalty here is the infinite-population Lyapunov correction. It remains at infinite \(N\).
- It does not match Lundberg. On the pair \((\mu,\sigma^2)=(0.30,0.40)\) and \((0.20,0.10)\), the drift ranks the first higher (\(0.30>0.20\)), the diffusion growth rate ranks the second higher (\(0.10<0.15\)), and the Lundberg exponent \(\theta=2\mu/\sigma^2\) also ranks the second higher (\(1.5<4\)). On the pair \((0.30,0.20)\) and \((0.16,0.08)\), diffusion growth ranks the first higher (\(0.20>0.12\)) and Lundberg ranks the second higher (\(3<4\)). Same ingredients, three different rankings.
- It does not match PD6. PD6 is the divergence of a mutual-information stock. The penalty here is a moment of offspring.

**The exponential map is a different route, and it assumes the cost.** If \(W=\exp(-\varepsilon C)\) with \(\varepsilon>0\) and \(\mathbb{E}|C|<\infty\), then \(\lambda=-\varepsilon\,\mathbb{E}[C]\) exactly, at every \(\varepsilon\). There is no variance penalty because the logarithm has already been undone. Maximizing \(\lambda\) minimizes expected cost. This is A2-L when \(C=J\), and it is CT43(i) when every term in \(J\) is paid as a fraction of the reserve. Both statements put the cost into the offspring map. Neither one produces the term list. Neither one produces the cap. Corollary LY-c is the same route with a vector score: linearity is the linearity of a logarithm in a score that was supplied from outside.

## 4. (b) Extinction, a penalty, and a cap

Three classical calculations, each proved here from its generator or its probability generating function. Each one supplies a smooth function of the offspring law. Thresholding that function is a further act.

**Galton–Watson (PROVED in-model).** Let \(f(s)=\mathbb{E}[s^W]\), \(m=f'(1)\), and let \(\eta\) be the smallest root of \(s=f(s)\) in \([0,1]\). If \(m\le 1\) and the offspring law is not concentrated at \(1\), then \(\eta=1\). If \(m\downarrow 1\) with \(f''(1)\to\beta_2>0\) and a bounded third factorial moment, then the survival probability satisfies

\[
1-\eta\sim\frac{2(m-1)}{\beta_2}.
\]

*Proof of the asymptotic.* Set \(s=1-\eta\). Taylor expansion of \(f(1-s)\) about \(1\) gives

\[
f(1-s)=1-ms+\frac{\beta_2}{2}s^2+O(s^3).
\]

The fixed-point equation \(s=1-f(1-s)\) is therefore

\[
s=ms-\frac{\beta_2}{2}s^2+O(s^3),
\]

and rearranging gives the identity

\[
s(m-1)=\frac{\beta_2}{2}s^2+O(s^3).
\]

For a positive root that tends to zero as \(m\downarrow 1\), divide by \(s\): \(m-1=(\beta_2/2)s+O(s^2)\), so \(s\sim 2(m-1)/\beta_2\). At criticality \(\beta_2=\mathrm{Var}(W)\), because \(f''(1)=\mathrm{Var}(W)+m^2-m\). □

For a Poisson law, \(f''(1)=m^2\to 1\), so the limit form is \(2(m-1)\). The script's survival ratios against \(2(m-1)\) are \(0.9987\), \(0.9868\), and \(0.9370\) at \(m=1.001\), \(1.01\), and \(1.05\). The ratio moves toward \(1\) as \(m\) moves toward \(1\). The object delivered is a smooth penalty in the mean, proportional to the mean excess when the variance is held at its critical value. A threshold \(1-\eta\ge s_0\) is a half-line in the single coordinate \(m\). It becomes a half-space in the plane of \((m-1,\beta_2)\) only after the linear approximation is imposed, and that half-space is \((m-1)-c\beta_2\ge 0\).

**Haldane's establishment probability is this penalty at variance near \(1\).** The factor \(2(m-1)\) is the Poisson case of the display above. Haldane 1927 is the classical branching-process statement for a mutant. This note does not copy a displayed equation from that paper.

**Linear birth-death (PROVED in-model).** Individuals independently give birth at rate \(b\) and die at rate \(d\). From one individual the extinction probability is \(1\) when \(b\le d\), and \(d/b\) when \(b>d\). From \(z\) individuals it is \((d/b)^z\) when \(b>d\).

*Proof.* The first event is death with probability \(d/(b+d)\), or birth with probability \(b/(b+d)\). After a birth, both lineages must die. So \(\eta=d/(b+d)+(b/(b+d))\eta^2\), that is \(b\eta^2-(b+d)\eta+d=0\), which factors as \((b\eta-d)(\eta-1)=0\). The extinction probability is the smaller root. Independence across the \(z\) founders gives the power. □

At \(b/d=1.1\) and \(z=20\), the extinction probability is \(0.148643628024\). The constraint that this probability be at most \(0.05\) requires \(b/d\ge 1.161586349642\). In the coordinates \((\log b,\log d)\) that constraint is a half-space. In the coordinates \((b,d)\) it is the half-space \(b-kd\ge 0\) on one side of a line through the origin. It is a threshold on a growth ratio. It does not mention memory, an acquisition rate, a task loss, or attention.

**Feller diffusion (PROVED in-model).** Let \(dZ=\alpha Z\,dt+\sqrt{2\beta Z}\,dW\) with \(\beta>0\), \(Z(0)=z>0\). The generator is \(\alpha z\,\partial_z+\beta z\,\partial_{zz}\). The extinction probability is \(1\) when \(\alpha\le 0\), and

\[
u(z)=\exp(-\alpha z/\beta)
\]

when \(\alpha>0\).

*Proof.* For \(\alpha>0\), \(u(0)=1\), \(u(\infty)=0\), and \(u'=-(\alpha/\beta)u\), \(u''=(\alpha/\beta)^2 u\), so the generator applied to \(u\) is zero. For \(\alpha\le 0\) the constant \(1\) is the only bounded solution with \(u(0)=1\). Feller 1951 is the branching-diffusion source. The formula is the one just solved. □

The level set \(u\le\varepsilon\) is the half-space \(\alpha/\beta\ge\log(1/\varepsilon)/z\) in the coordinate \(\alpha/\beta\).

**Brownian reserve (PROVED in-model).** Let \(dX=\mu\,dt+\sigma\,dW\), \(X(0)=x>0\), absorbed at \(0\). The generator is \(\mu\,\partial+(\sigma^2/2)\partial^2\). The probability of hitting \(0\) is \(1\) when \(\mu\le 0\), and

\[
\exp(-2\mu x/\sigma^2)
\]

when \(\mu>0\).

*Proof.* The function \(e^{-2\mu x/\sigma^2}\) is in the kernel of the generator, equals \(1\) at \(0\), and tends to \(0\) at infinity when \(\mu>0\). □

Iglehart 1969 is the collective-risk diffusion approximation. Lundberg's 1903 thesis has no DOI used in this note. Cramér's survey resolves on Crossref at the 1994 collected-works DOI in §7. The exponent \(\theta=2\mu/\sigma^2\) is the one proved here. The level set is a half-space in the coordinate \(\theta\), and it is the half-space \(\mu-k\sigma^2\ge 0\) in the plane \((\mu,\sigma^2)\).

**On the published path the same level set is not a half-space in the design coordinate.** Lemma B9, as recomputed in `tools/general_form_checks.py` and again here: \(y=1\), \(c=0.05\), \(w=\sigma=1\), \(s_0=0.3\),

\[
J(\tau)=\frac{c}{\tau}+\alpha\tau,
\quad
\alpha=\frac12,
\quad
s^2=s_0^2+\beta\tau^3,
\quad
\beta=\frac13,
\quad
\theta=\frac{2(y-J)}{s^2}.
\]

The expected-cost point is \(\tau_E=\sqrt{c/\alpha}=0.316227766017\). The unique zero of \(\theta'\) on the positive-margin interval is \(\tau_S=0.236207526722\). The multiplicative diffusion criterion of §3, applied to a factor whose mean and variance rate equal this path's margin and variance rate, maximizes

\[
\phi(\tau)=(y-J(\tau))-\frac12 s^2(\tau).
\]

Its maximizer solves \(\tau^4+\tau^2-0.1=0\), so \(\tau_G=0.302668099260\). The four numbers \(\tau_S\), \(\tau_G\), \(\tau_E\), and the cap point below are distinct. \(\phi(\tau_G)>\phi(\tau_E)\). The additive reserve of Lemma B9 has drift \(y-J\), not drift minus half the variance: \(\phi\) is the diffusion limit of a multiplicative factor with those moments, which is the object §3 actually derives. It is a different reading from the additive reserve's expected drift.

**The published cap.** \(\varepsilon_r=10^{-3}\), buffer \(B=0.5\), requirement \(\theta\ge\log(1000)/B=13.815510557964\). Here \(\theta(\tau_S)=14.200588175815\) and \(\theta(\tau_E)=13.601868698785\). The superlevel set inside the positive-margin interval is the bounded interval

\[
[\tau_{\mathrm{lo}},\tau_{\mathrm{cap}}]=[0.183706411069,\,0.299049733488].
\]

A bounded interval of the real line is the intersection of two half-lines. It is not a half-line. \(\tau_E\) and \(\tau_G\) both lie to the right of \(\tau_{\mathrm{cap}}\), so both are infeasible at this buffer. \(\tau_S\) lies inside. On the feasible interval, \(J\) is still decreasing and \(\phi\) is still increasing, because both of their unconstrained maximizers lie to the right. Both constrained criteria therefore sit on the right endpoint \(\tau_{\mathrm{cap}}\). The Lundberg maximizer remains \(\tau_S\). The costs are \(J(\tau_E)=0.316227766017\), \(J(\tau_{\mathrm{cap}})=0.316721136799\), and \(J(\tau_S)=0.329782030747\). Three feasible-or-published designs, three different points. V2 recorded the pair \((\tau_S,\tau_E)\). The cap adds a third, and the diffusion growth rate adds a fourth, which this particular cap happens to push onto the same endpoint as expected cost.

**A cap that separates them.** Set the requirement at the midpoint of \(\theta(\tau_G)\) and \(\theta(\tau_E)\). The constrained expected-cost point, the right endpoint of the new superlevel set, is \(\tau_J=0.309679835108\). The diffusion-growth point \(\tau_G=0.302668099260\) remains feasible and is preferred by \(\phi\). Expected cost prefers \(\tau_J\), since \(J(\tau_J)<J(\tau_G)\). The two criteria disagree inside a binding cap. A slack cap, any requirement at most \(\theta(\tau_E)\), leaves both unconstrained points feasible and they still disagree.

**CT43(iii), recomputed, analytic part.** Designs \(A=(1.04,1.02)\) and \(B=(1.131,0.931)\), equal probabilities. Arithmetic means \(1.03\) and \(1.031\). Growth rates \(0.029511670225\) and \(0.025803097714\). Arithmetic ranks B higher. Growth ranks A higher. DYNAMICS already records that both can pass one threshold-ruin constraint. A cap that both designs pass leaves the disagreement standing. The cap fixes a sign, in the sense CT43 states for a long horizon: nonpositive time-average growth is excluded. It does not choose between the two rankings.

**When the output is a penalty, and when someone has imposed a cap.**

- The extinction probability, the survival asymptotic \(2(m-1)/\beta_2\), the Feller function \(\exp(-\alpha z/\beta)\), and the Lundberg function \(\exp(-2\mu x/\sigma^2)\) are penalties. Maximizing survival, or maximizing \(\theta\), uses the whole penalty as the objective. That objective is not expected currency. \(\tau_S\neq\tau_E\) is the witness already in V2, recomputed here.
- A constraint \(P\le\varepsilon\) for a fixed \(\varepsilon\in(0,1)\) is the penalty after a threshold has been chosen. The threshold's level set is a half-space in \(\theta\), and in \((\mu,\sigma^2)\). On the B9 path it is a bounded interval of \(\tau\). Choosing \(\varepsilon\), or equivalently choosing the required exponent, is an extra act. GF3(R-b) already names that act.
- Sending \(W\) to \(0\) on a ruin event makes \(\mathbb{E}[\log W]=-\infty\) whenever that event has positive probability, provided one extends the logarithm in the usual way. H2 assumes the expectation is finite, so this extension is outside the lemma. The resulting constraint is \(P(W=0)=0\). Every supercritical branching process with a positive chance of a zero generation fails it. That is a cap at zero. It is not a cap at a free \(\varepsilon\in(0,1)\) with a risk-neutral ranking on the surviving set.
- Finite-population absorption, in the branching-process approximation of a rare type, again returns a survival probability of order the selective excess. The ranking is by that excess. A step appears only after an extra limit of very strong selection, and the step ranks types against each other. It does not install a half-space cap in five cost coordinates and then minimize expected currency inside it.

## 5. (c) H3 on the five coordinates

H3, from Lemma LY, is a partial. For almost every environment, offspring is strictly decreasing in each coordinate of the chosen bad vector, the other coordinates held fixed, and \(W>0\). The five coordinates in the task are memory, acquisition rate, task loss, ruin, and attention. A floor that mentions a slot is not H3. GF2 already says so.

A budget map with a positive price supplies that partial for memory, acquisition, and attention, read as resources spent at fixed task loss. Copying does not supply the map. A zero price makes the partial only weak, so H3's strictness fails for a free resource. A side benefit that is not among the coordinates held fixed can reverse the total derivative. That reversal leaves the partial untouched.

| Coordinate | Partial, other bads held fixed | Total derivative, a different question |
|---|---|---|
| Memory | At a fixed loss path, \(\log W=-\kappa I-\ell\) has partial \(-\kappa\). The partial is strict when \(\kappa>0\). The map is an assumption. A free memory slot has partial \(0\) | \(W=\exp(-e^{-2I})\) rises from \(0.367879441171\) at \(I=0\) to \(0.873423018493\) at \(I=1\). The total derivative is \(2e^{-2I}>0\) because the loss falls. Holding that loss fixed, the formula has no separate memory price, and the partial in a memory slot is \(0\) |
| Acquisition rate | At fixed task loss, \(\log W=-c r-\ell\) has partial \(-c\), strict when \(c>0\) | \(\log W=-r-4e^{-r}\) has total derivative \(-1+4e^{-r}\), positive on \([0,\log 4)\). From \(r=0\) to \(r=1\), \(W\) rises from \(0.018315638889\) to \(0.084456576466\). The partial at fixed loss is \(-1\) |
| Task loss | This coordinate is the performance bad, so holding task loss fixed is not the question about it. Pathwise \(W=\exp(-w\,\ell)\) decreases in \(\ell\) by the map that was put in. Expected loss fails H3 | LY-1: resource and error \((1,0)\) with offspring \(4\) and \(0.05\) has \(\lambda=\frac12\log 0.2=-0.804718956\); \((2,0.4)\) with offspring \(1.1\) has \(\lambda=\log 1.1=0.095310180\). The smaller expected-bad vector has the smaller growth rate. Both offspring numbers are positive. The learning pair, loss \(0\) with offspring \(1.1\) against loss \(1\) with offspring \(3\), lets the loss buy a later return. It is a total derivative |
| Ruin | A scalar \(P(\mathrm{ruin})\) is a functional of the law, not a coordinate of \(W(\omega)\). Holding the ruin event fixed leaves no separate probability to differentiate. No budget model creates a pathwise strict decrease in that scalar | \(W\equiv 1.2\) at probabilities \(0.01\) and \(0.20\) does not move offspring. \(W=0\) on the ruin event sends \(\mathbb{E}[\log W]\) to \(-\infty\) and breaks \(W>0\). This witness stands. GF2 already says the cap is a modelling choice and is not H3 |
| Attention | If attention is a resource at fixed task loss, the budget partial is \(-c_a\), strict when \(c_a>0\). If attention is the currency of THEORY §3, a fifth peer repeats that currency, as GF2 says, and H3 on a peer coordinate is the wrong question | \(\log W=-4e^{-a}\) rises from \(0.018315638889\) at \(a=0\) to \(0.229576777100\) at \(a=1\). The total derivative is \(4e^{-a}>0\) through a falling loss. It does not refute the budget partial |

**FALSE.** "H3 holds for these five coordinates from first principles." The partial for memory, acquisition, and attention is the budget assumption, and it is strict only at a positive price. Expected task loss fails by LY-1. A scalar ruin probability is not a pathwise coordinate. Copying does not supply the budget map.

## 6. (d) The cleanest true theorem

**Theorem GB (PROVED in-model).** Under the hypotheses of Theorem GB-menu, weak selection makes the argmax of \(\lambda=\mathbb{E}[\log W]\) agree with the argmax of expected offspring. The expansion is \(\lambda=\varepsilon\mathbb{E}[X]-(\varepsilon^2/2)\mathbb{E}[X^2]+O(\varepsilon^3)\). Under the hypotheses of Theorem GB-diff, the growth rate per unit time converges to \(\mu-\sigma^2/2\).

That is the whole of what these two limits derive. The agreement on a gapped finite menu is an agreement of argmaxes. It is not an identity of the two objectives. The diffusion limit is a different objective, with the variance penalty kept.

**The master equation is not derived, and it is not derived in either limit.**

- The term list is an input. The exponential map and Corollary LY-c produce a linear expected cost only after the cost, or the score, has been put into \(\log W\). The selection note already refuses to reopen the term list from A1–A3. This note does not reopen it either.
- The cap is an input. Section 4 produces smooth penalties, a half-space in the Lundberg exponent, and a bounded interval of \(\tau\). The published path has \(\tau_S=0.236207526722\), \(\tau_G=0.302668099260\), \(\tau_{\mathrm{cap}}=0.299049733488\), and \(\tau_E=0.316227766017\). The split-cap point \(\tau_J=0.309679835108\) separates expected cost from diffusion growth inside a binding constraint. Thresholding the penalty at a free \(\varepsilon\in(0,1)\) is GF3(R-b).
- H3 is an input. As a partial with the other bads held fixed, it holds for memory, acquisition, and attention only under a budget map with a positive price. Expected task loss fails by LY-1. A scalar ruin probability is not a pathwise coordinate. "From first principles" stays false. Section 5.

**FALSE, as a package.** "Maximizing \(\lambda\) in a small-noise limit yields \(J=\kappa I_{\mathrm{mem}}+hK+w\mathbb{E}[\ell]+A+L\) subject to \(P(\mathrm{ruin})\le\varepsilon\)." The stake counterexample, the diffusion sign flip at \(\mu=0.2\) and \(\sigma^2=0.5\), the third-moment tie, and the four B9 points are the counterexamples. Each one is enough.

What remains assumed, in the language of GF3, is risk-neutral expected currency as the exact objective, the half-space cap in a chosen ruin coordinate, linear nonnegative prices, and H3 for each coordinate that the cost treats as a bad. The new information is where a limit gets part of the way there, and which counterexample stops it.

## 7. Prior art

Every DOI below was resolved on the Crossref API on 22 November 2026. A DOI is printed only when the returned title contains the work. The record is `theory/growth_bridge_checks/crossref.out`. Lundberg's 1903 thesis is a thesis; no DOI is used for it. The Cramér DOI below is the collected-works issue Crossref returns, year 1994.

Known, and not claimed as new:

- Kelly 1956, doi 10.1002/j.1538-7305.1956.tb03809.x. The stake counterexample is his criterion. CT42 and CL21 already use it.
- Cohen 1966, doi 10.1016/0022-5193(66)90188-3. Bet-hedging under a shared shock. Already CL20.
- Lewontin and Cohen 1969, doi 10.1073/pnas.62.4.1056. Long-run growth in a randomly varying environment is an expected logarithm.
- Dempster 1955, doi 10.1101/sqb.1955.020.01.005, "Maintenance of genetic heterogeneity." Early citation for geometric-mean fitness. This note does not re-derive his text. The expansion in §3 is Taylor's theorem.
- Gillespie 1974, doi 10.1093/genetics/76.3.601, within-generation variance in offspring number. DYNAMICS already records the \(O(1/N)\) reading.
- Gillespie 1977, doi 10.1086/283230, "Natural Selection for Variances in Offspring Numbers: A New Evolutionary Principle."
- Frank and Slatkin 1990, doi 10.1086/285094, "Evolution in a Variable Environment." Frank 2011, doi 10.1111/j.1420-9101.2011.02378.x, "Natural selection. I. Variable environments and uncertain returns on investment."
- Lande 1976, doi 10.1111/j.1558-5646.1976.tb00911.x. The weak-selection gradient. SA3 already states the limit.
- Haldane 1927, doi 10.1017/S0305004100015644, Part V. Establishment of a mutant. The factor used in §4 is the probability-generating-function expansion proved here.
- Feller 1951, doi 10.1525/9780520411586-018, "Diffusion Processes in Genetics." The extinction formula in §4 is solved from the generator.
- Iglehart 1969, doi 10.2307/3211999, "Diffusion approximations in collective risk theory."
- Cramér, "Collective risk theory: A survey of the theory from the point of view of the theory of stochastic processes," doi 10.1007/978-3-642-40607-2_17, Crossref issued year 1994.

Already in this repository, and not presented as new: Lemma LY and GF3; V2's Kelly and Lundberg numbers; CT42; CT43, including the coin and the pair \(A,B\); PD6; A2-L's refusal to derive the term list; SA3's weak-selection caveat.

**What this note adds.** The separation of the two limits as answers about this equation. On a gapped finite menu, weak selection recovers the ranking only. The diffusion limit keeps \(\mu-\sigma^2/2\). The squared-mean obstruction to the unscoped identity. The point \(\tau_G\) and the split cap on the published path, which separate diffusion growth from expected cost inside one model. The coordinate audit in §5: the partial, the budget map, and which witnesses are total derivatives. The package sentence in §6, marked false. The Kelly stake, the Taylor expansion, and the extinction and hitting formulas are the prior art in §7.

## 8. What this does not show

- It does not make the hypothesis a physical law.
- It does not replace THEORY §3's equation or the operational definition of strongly selected.
- It does not show that any real offspring map is in the weak-selection regime of Theorem GB-menu, on the master equation's coordinates, with gaps large enough that the second-moment penalty leaves the ranking alone. That is OPEN. It is not a locked prediction.
- It does not show that H3 holds for any real population. Section 5 shows where an extra map would have to be assumed.
- It does not close V4, V5, CX1, or CX2.
- It does not re-score a locked preregistration.

## 9. Checks

`tools/growth_bridge_checks.py`, run by `tools/test_growth_bridge_checks.py`. **NUMERICAL** as a check of algebra that is proved in the text: the Lagrange bound, the diffusion rates, a three-design menu with a fixed gap in \(\mathbb{E}[X]\) (the growth argmax agrees at small \(\varepsilon\) and flips at a larger \(\varepsilon\)), the mean-gap flip at \(\mathbb{E}[X]=0.05\), the equal-mean growth \(\frac12\log 0.96\), the stake derivative, the coin, the third-moment gap, the B9 points \(\tau_S\), \(\tau_E\), \(\tau_G\), \(\tau_{\mathrm{lo}}\), \(\tau_{\mathrm{cap}}\), \(\tau_J\), the Poisson ratios, the birth-death threshold, the Feller generator residual, the Brownian kernel, the budget partials \(-\kappa\), \(-c\), and \(-c_a\), and the total derivatives read against the digits in §5. Crossref output, when refreshed with `--crossref`, is `theory/growth_bridge_checks/crossref.out`. The committed copy is the resolution of 22 November 2026.

The Part 2 hypothesis sentence is the sentence in §0. It is byte-identical to the sentence in THEORY §3 and in CORE.
