# PREREG: the predict-act-correct loop

Written Sunday 22 November 2026, before any script in this directory and before any numerical evaluation of a cost below. The only file this commit adds is this preregistration. The decimals are the values of the expressions written here. No design was searched to produce them. A later script may only evaluate these expressions.

This file does not edit `theory/acting_memory_checks/PREREG.md`. That lock stands. T45 is the open-loop probe. This row, when it is written, is T46. The hypothesis sentence is not changed. `THEORY.md`, `CORE.md`, and `README.md` are not edited.

The hypothesis under test is a hypothesis, not a specification. The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

## 1. Two scores, kept apart

The stressor is the stationary variance \(\theta\) of the uncontrolled equilibrium. It is not the reversion \(a\).

- **Level.** A cost is level-decreasing on an interval when it is strictly decreasing there.
- **Variability.** A cost is variation-antifragile at a point when it is strictly concave there. This is the reading already in `theory/ROBUSTNESS.md` §6: the payoff is convex in the stressor, so a mean-preserving spread of \(\theta\) lowers the expected cost. A strictly convex cost is fragile to that spread. A falling cost and a concave cost are not the same score.

## 2. Class AL

**AL-X.** The world depends on the action. With \(a>0\), \(\theta>0\), \(b\ge 0\),
\[
dX=-aX\,dt+b u_a\,dt+\sqrt{2a\theta}\,dW.
\]
The uncontrolled equilibrium variance is \(\theta\). The case \(b=0\) is the exogenous world of class AM. A constant action shifts the mean and does not change the variance.

**AL-Y.** The observation intensity is \(u_o\ge 0\). For \(u_o>0\), \(dY=X\,dt+u_o^{-1/2}\,dV\), with \(V\) independent of \(W\). The steady error \(p=\mathbb{E}[(X-m)^2]\) of the conditional mean \(m\) solves the exogenous Riccati
\[
u_o p^2+2ap-2a\theta=0,
\]
so \(p=(-a+\sqrt{a^2+2a\theta u_o})/u_o\) and \(r=p/\theta\). The control cancels in the error equation and does not appear. At \(u_o=0\), \(p=\theta\) and \(m=0\).

**AL-K.** On \(u_o>0\) the feedback is linear, \(u_a=-Km\) with \(K\ge 0\). The closed-loop rate is \(a_c=a+bK\). The estimate variance and the state variance are
\[
s=\frac{a(\theta-p)}{a_c},\qquad v=p+s.
\]
At \(K=0\), \(v=\theta\). As \(K\) rises, \(v\) falls toward \(p\) and no further. The learning rate of the Gaussian conditional is
\[
L=a\Bigl(\frac{\theta}{p}-1\Bigr)=\frac{u_o p}{2},
\]
and it does not depend on \(K\).

**AL-H.** The heat is the floor \(kT\,L\), plus a gap, plus the finite-rate factor below. The shape \(\dot Q\ge kT\) times the learning rate is Horowitz and Esposito, as already used here, and it is not re-proved. The finite-rate factor is the shrunk-spring ratio already proved for an exogenous equilibrium Ornstein–Uhlenbeck signal at memory rate \(\lambda\): with \(\rho_\lambda=\lambda/(a+\lambda)\) and \(r=p/\theta\),
\[
Q_{\mathrm{fin}}=a(1-r)\frac{\rho_\lambda}{\rho_\lambda(1+r)-1},
\]
charged only when \(\rho_\lambda>1/(1+r)\). At \(r=1/2\) and \(\lambda=20\), \(a=1\), this equals \(10/9\). The gap is frozen as \(\gamma(\theta)=\gamma_1\theta\), and, in one witness only, as \(\gamma_2\theta^2\). Every other cost charges \(\gamma_2=0\).

**AL-R (regulation).** The loss rate is \(q\,\mathbb{E}[X^2]+\rho\,\mathbb{E}[u_a^2]\), with \(q>0\) and \(\rho>0\). The probe price is \(\alpha u_o\). The scored regulation cost is
\[
J=kT\,L+\gamma(\theta)+\alpha u_o+q v+\rho K^2 s.
\]
In the master equation the heat stands where the memory term stands, the probe price stands where the read term stands, the actuation price stands where effort on the world's drift stands, and the state penalty is the stake term. Layer upkeep and the link term are zero. That placement is this file's. It does not edit the equation in THEORY.

**AL-CE.** With no chance constraint, the gain that minimizes \(q v+\rho K^2 s\) at fixed \(p\) is
\[
K^\star=\frac{-a+\sqrt{a^2+q b^2/\rho}}{b}\qquad(b>0),
\]
and the regulation piece equals \(2a\theta P+\rho (K^\star)^2 p\) with \(P=\rho K^\star/b\). This \(K^\star\) does not depend on \(p\), on \(u_o\), or on \(\theta\).

**AL-S.** The sign loss of class AM, \(w\psi(r)\) with \(\psi(r)=\arccos\sqrt{1-r}/\pi\), is scored only as stated in §5. Feedback changes the correlation to \(\sqrt{s/v}\). It is not added into \(J\) of AL-R.

**AL-Cox.** One failure time, with \(X\) drawn once from \(\mathcal N(0,v)\) and held. The intensity is \(\lambda(x)=\lambda_0+\beta x^2\). The independent arm uses a constant intensity equal to \(\mathbb{E}[\lambda(X)]\), and its failure time is independent of \(X\).

**Ruin.** A design is admissible when \(P(q X^2>B)\le\varepsilon_r\). For a centered Gaussian this is a cap on \(v\). The operating point below is scored against \(B=16\). A second, tighter cap \(v\le 3/5\) is the separation witness. It is not a replacement of \(B\).

## 3. Frozen point

| symbol | value |
|---|---|
| \(a\), \(kT\), \(\theta_0\), \(b\), \(\rho\) | \(1\), \(1\), \(1\), \(1\), \(1\) |
| stakes \(q\) | \(1\) and \(4\) |
| \(w\), \(\alpha\) | \(16\), \((4-\pi)/(6\pi)\) |
| \(B\), \(\varepsilon_r\) | \(16\), \(1/20\) |
| tight variance cap | \(3/5\) |
| \(\gamma_1\), \(\gamma_2\) witness | \(1/10\), \(1\) |
| memory rate \(\lambda\) | \(20\) |
| passive intensity | \(u_o=4\) |
| Cox \((v,\lambda_0,\beta,t)\) | \((1,1,1,1)\) |
| spread half-width \(\delta\) | \(1/10\) |
| sign grid | \(\{1/8,1/4,1/2,1,2,4,8\}\) |
| floor used for that grid | \(4.966383544211\) |

\(\alpha\) is the price already fixed by the acting-memory lock. It is not refit.

## 4. Locked algebra

**Full information, channel not priced.** \(P=-a+\sqrt{a^2+q}\) at \(\rho=b=1\), and the full-information cost is \(2a\theta P\). The sensing-alone cost, and the action-alone cost, both equal \(q\theta\): a constant action cannot cut a zero-mean variance, and an observation that is not acted on cannot either. The gap is
\[
\Delta_{\mathrm{full}}(\theta,a)=(q-2aP(a))\,\theta.
\]
At \(q=1\), \(q-2aP(a)=1-2a/(a+\sqrt{a^2+1})\). At \(a=1\) this factor equals \(3-2\sqrt{2}\). At \(a=1/2\) it equals \((3-\sqrt{5})/2\). At \(a=2\) it equals \(1-4/(2+\sqrt{5})\). Each factor is positive. The gap is strictly positive for every \(\theta>0\) and every \(a>0\).

**Priced channel.** With \(kT=1\) and fraction \(r\),
\[
\Delta(\theta,a,r)=(1-r)\Bigl[(q-2aP(a))\,\theta-\frac{a}{r}-\frac{2\alpha a}{\theta r^2}\Bigr],
\]
where \(\Delta\) is the sensing-alone cost minus the closed-loop cost, and \(\gamma_1\theta\) cancels. Closed-loop acting is strictly cheaper at a fraction \(r\) when \(\Delta>0\).

At \(q=a=\theta=1\), the bracket is \(3-2\sqrt{2}-1/r-2\alpha/r^2\). Its derivative in \(r\) is positive, so the bracket is largest as \(r\to 1\), where it equals \(3-2\sqrt{2}-1-2\alpha<0\). Therefore \(\Delta<0\) for every \(r\in(0,1)\). At \(r=1/2\),
\[
\Delta=\frac12\bigl(3-2\sqrt{2}-2-8\alpha\bigr).
\]
The closed loop is strictly dearer than sensing alone at this stake. The two costs meet only at \(u_o=0\), which is not a closed loop.

At \(q=4\), \(a=\theta=1\), \(K^2=(\sqrt{5}-1)^2\), and the bracket at \(r\to 1\) equals \(K^2-1-2\alpha>0\). The stationary point of \(\Delta\) in \(r\) solves
\[
K^2 r^3+(2\alpha-1)r-4\alpha=0.
\]
There is one root in \((0,1)\), because the cubic is negative at \(0\), positive at \(1\), and has one turning point. At that root \(\Delta>0\).

**Acting and the memory.** At fixed \(p\),
\[
v(K)-p=\frac{a}{a+bK}(\theta-p).
\]
For \(bK>0\) this is strictly smaller than \(\theta-p\). The mutual-information stock \(\tfrac12\log(v/p)\) falls with \(K\). The learning rate \(L\) does not. The finite-rate heat \(Q_{\mathrm{fin}}\) is a function of \(r\) and \(\lambda\) and does not contain \(K\). Control reduces the variance that is carried in the state, and the stock of mutual information, and it does not reduce the heat charged here.

At \(a=b=1\), \(p=\theta=1/2\), \(K=\sqrt{2}-1\), one has \(a_c=\sqrt{2}\), \(s=\sqrt{2}/4\), and \(v=(2+\sqrt{2})/4\). The uncontrolled stock is \(\tfrac12\log 2\). The controlled stock is \(\tfrac12\log(1+2^{-1/2})\).

**Separation.** \(K^\star\) in AL-CE does not depend on \(p\). At the tight cap \(v\le 3/5\), with \(p=1/2\), \(\theta=a=b=1\), the smallest gain that meets the cap is
\[
K_{\mathrm{cap}}=\frac{\theta-p}{3/5-p}-1=4.
\]
The quadratic gain at \(q=1\) is \(\sqrt{2}-1\). The cap selects \(4\), so the gain depends on the constraint. Certainty equivalence, read as "the gain is the unconstrained Riccati gain," does not survive this cap.

The operating point \(v=(2+\sqrt{2})/4\) against \(B=16\) and \(q=1\) has \(P(X^2>16)\) far below \(1/20\), because \(4/\sqrt{v}>4\). That reserve cap does not bind. The break is the tight cap, not this \(B\).

**Capped loss.** Let \(\varphi(v)=\mathbb{E}[\min(X^2,1)]\) for \(X\sim\mathcal N(0,v)\), and let \(z=v^{-1/2}\). Then
\[
\varphi'(v)=(2\Phi(z)-1)-2z\,\phi(z),
\]
with \(\phi\) the standard normal density. At fixed \(p=1/2\) and \(q=1\), the derivative of \(\varphi(v(K))+K^2 s(K)\) at \(K=\sqrt{2}-1\) equals
\[
\frac14\bigl(1-\varphi'(v)\bigr),\qquad v=(2+\sqrt{2})/4.
\]
The unconstrained quadratic derivative at the same gain is \(0\). A nonzero derivative means this gain is not stationary for the capped loss.

**Level and variability of the closed loop at fixed \(u_o=4\), \(q=1\), \(\gamma_2=0\).** Write \(s_\theta=\sqrt{a^2+2a u_o\theta}\). Then \(p=(-a+s_\theta)/u_o\) and \(L=(-a+s_\theta)/2\), both concave in \(\theta\). At \(a=1\), \(\theta=1\),
\[
\frac{\mathrm d J}{\mathrm d\theta}=\frac{4\sqrt{2}-1}{3}+\gamma_1,\qquad
\frac{\mathrm d^2 J}{\mathrm d\theta^2}=\frac{4(2\sqrt{2}-5)}{27}.
\]
The second derivative is negative. A gap \(\gamma_1\theta\) does not change it. A gap \(\gamma_2\theta^2\) adds \(2\gamma_2\). The second derivative changes sign when \(\gamma_2>2(5-2\sqrt{2})/27\). The witness \(\gamma_2=1\) lies above that threshold, so the second derivative at the witness is positive.

The fixed-intensity spread at half-width \(1/10\) has the sign of the second derivative: negative at \(\gamma_2=0\).

**Sign grid.** On class AM the minimized capped-sign cost is \(J^\star(\theta)=A(r^\star(\theta))/\theta+C(r^\star(\theta))\), with \(C\) the heat floor plus the sign loss, and \(A(r)>0\) for \(r\in(0,1)\). Therefore \(J^\star(\theta)>\inf C\) at every finite \(\theta\). The comparison value is the published floor \(4.966383544211\). The published cost at \(\theta=8\) is \(4.998066177768\), and the difference is \(0.031682633557\).

**Sign loss under feedback.** At the same \(p=1/2\), \(\theta=1\), and \(K=\sqrt{2}-1\), the correlation is \(\sqrt{\sqrt{2}-1}\), which is strictly less than \(1/\sqrt{2}\). The sign loss \(16\psi\) is strictly larger than \(4\).

**Cox.** At the frozen Cox point the Gaussian integral gives posterior variance
\[
\sigma^2=\frac13,\qquad
\mathrm{Var}(X\mid T=t)=\sigma^2\frac{\lambda_0+3\beta\sigma^2}{\lambda_0+\beta\sigma^2}=\frac12.
\]
The independent arm leaves the variance at \(1\). The mean intensity is \(\mathbb{E}[\lambda]=2\). The mean lifetime is
\[
\mathbb{E}[T]=\sqrt{\frac{\pi}{2}}\,e^{1/2}\,\mathrm{erfc}\bigl(2^{-1/2}\bigr),
\]
which is strictly larger than \(1/2\).

**Heat gap on the old sign slope.** The acting-memory envelope slope at the frozen sign point is \(2/3-8/(3\pi)\). Adding \(\gamma_1\theta\) adds \(\gamma_1\). At \(\gamma_1=1/10\) the slope stays negative. At \(\gamma_1=1/2\) it is positive. The second derivative of that sign cost is unchanged by a linear gap.

## 5. Predictions

Scored after the script, in this order. A later line does not edit an earlier score. Absolute tolerance \(10^{-9}\) on a closed form against the expression in §4, unless a line says \(10^{-12}\).

**P1. Full-information gap.** At \(q=1\), \(\Delta_{\mathrm{full}}/\theta\) equals \(0.171572875254\) at \(a=1\), \(0.381966011250\) at \(a=1/2\), and \(0.055728090001\) at \(a=2\). Each is positive. Sensing alone and action alone both cost \(q\theta\).

**P2. Priced closed loop at stake \(1\).** At \(q=a=\theta=1\) and \(r=1/2\), \(\Delta=-1.096373258863\). The closed loop is strictly dearer. The bracket at \(r\to 1\) is negative, so no fraction in \((0,1)\) is cheaper.

**P3. Priced closed loop at stake \(4\).** The root in \((0,1)\) equals \(0.856768708291\), and \(\Delta\) there equals \(0.033889928154>0\). Closed-loop acting is strictly cheaper than sensing alone by that amount.

**P4. Acting leaves the heat and cuts the stock.** At the frozen feedback, \(v=0.853553390593\). The learning rate is \(1\) with and without the gain. The finite-rate heat is \(10/9\) with and without the gain. The stock falls from \(0.346573590280\) to \(0.267399998370\).

**P5. Separation.** The Riccati gain at \(q=1\) equals \(\sqrt{2}-1\) and does not depend on \(p\). The tight cap selects gain \(4\). The capped-loss derivative at the Riccati gain equals \(0.189957517375\), and the quadratic derivative there equals \(0\). The reserve \(B=16\) does not bind at \(v=(2+\sqrt{2})/4\).

**P6. Level and variability of the closed loop.** At \(u_o=4\), \(q=1\), \(\gamma_1=0\), the slope equals \(1.552284749831>0\) and the second derivative equals \(-0.321714500038<0\). The spread at half-width \(1/10\) equals \(-0.001612560843\). The threshold for a convex gap is \(0.160857250019\). At \(\gamma_2=1\) the second derivative is positive.

**P7. The sign grid against the floor.** On the seven-point grid, each minimized sign cost is strictly above \(4.966383544211\). The gap at \(\theta=8\) equals \(0.031682633557\).

**P8. Feedback raises the sign loss.** At the frozen feedback the sign loss equals \(4.439079197657\), above \(4\) by \(0.439079197657\).

**P9. Cox against an independent failure.** The posterior variance equals \(1/2\). The independent variance equals \(1\). \(\mathbb{E}[T]=0.655679542419>1/2\).

**P10. A linear heat gap and the old slope.** The sign slope plus \(1/10\) equals \(-0.082159696490<0\). The sign slope plus \(1/2\) equals \(0.317840303510>0\).

## 6. What would count as a miss

- Any equality or sign in P1–P10 that the script's evaluation of §4 contradicts, beyond the tolerance in §5.
- A coding error in the Riccati residual, worse than \(10^{-12}\), or in the hash of this file against `LOCK.txt`. The formulas are then fixed in a dated deviation that does not change this file.

A miss is a puzzle. The note keeps the numbers, names the clause, and does not rewrite this file. The word for the objective remains cost.

## 7. What the computation is allowed to be

One script, `theory/acting_loop_checks/acting_loop_checks.py`, run after this file is committed and after `LOCK.txt` records its sha256. The script checks that hash before it evaluates a cost. It may print the quantities in §4 and §5, the Riccati residual, and the hash check.

Prior art to be fetched with the results, not used as a premise of the algebra: Kalman; the LQG separation theorem; Todorov and Jordan on optimal feedback control; Sagawa and Ueda on the thermodynamics of feedback; Horowitz and Esposito; Friston and coauthors only as related work. A DOI is cited only if Crossref returns it.
