# Is there a holographic structure in the cost of judgment?

*Sunday 22 November 2026. Draft. A self-check, not an independent review. Repaired after the review of draft PR #184 (`records/reviews/holographic_2026-11-22/HOSTILE_REVIEW.md` is on the review branch; this note is the repair). The hypothesis sentence is unchanged. The master equation in THEORY is unchanged. No locked preregistration file is edited. Checks: `theory/holographic_checks/holographic_checks.py`, run at `nice -n 19`. DOIs resolved on the Crossref API on 22 November 2026, and the abstracts used below, are listed in `theory/holographic_checks/crossref.out`.*

Labels: **PROVED** (a proof is on this page, in the class named with it, and the arithmetic is in the checks), **KNOWN** (published, fetched this session, not claimed here), **FAILS** (a counterexample is on this page), **METAPHOR** (the reading adds no prediction the cost equation does not already make). Nothing here is a conjecture. GTAO is the theory in this repository.

The sentence of the hypothesis is unchanged, byte for byte:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

## 0. The answer

For bulk per-site error, the physics-derived cost is not a holographic encoding.

The memory-bath heat is bounded by \(kT\) times the learning rate, and that rate is the information flow of the signal current across the cut between world and memory. At a fixed decision error the floor depends on that conditional law and on the signal. It does not depend on extra equilibrium coordinates that leave the conditional unchanged. That is the cost equation. It does not encode a bulk on a boundary, and it does not cap how much irrelevant state the memory may carry.

What the same equation does show, once the decision is a designated cut rather than every site: the minimum heat scales with the cut, at about \(13.61\) per cut site against a lower bound of \(13\), and that cost does not grow with the depth behind the cut. That is the cost equation applied to the sites the decision names. It is not a bulk stored on a boundary. The cube behind the cut stays at its prior, up to the cap \(A/\alpha\).

What does not hold for the bulk decision:

- At fixed per-site error on every site, the minimum heat scales with the volume. On even grids the slope \(1\) is the identity \(V(1/\varepsilon-\alpha-2d\beta)\). Odd sides, where the stiffest rate still moves, give slope \(1.016\).
- A memory that sees only a surface cannot hold a fixed per-site gap in the cube once the cube is large.
- The geometric ladder plus the rank-one sum-loss memory is not a renormalization-group layering. The heat added per octave grows by the scale factor. On a sum loss the optimal memory has one coordinate at every stake.

Where a holographic reading predicts a bulk encoding the cost equation does not — a cap on bulk memory, equal cost per layer, a layered reconstruction — the check does not support it. Where the two readings agree, including the cut, the number was already the cost equation, and the holographic name is a metaphor.

## 1. Already in the repository

None of the following is a result of this note.

- The heat floor itself. For one exogenous equilibrium Ornstein–Uhlenbeck signal and a mean-squared decision loss, the infimum of the memory-bath heat is \(kT\,a(v-\varepsilon)/\varepsilon\) (`theory/INFO_PHYSICS_ATTAINABILITY.md`, IP11). For independent modes it is the sum of those rates, and on a sum loss it is \(kT\mu\) with gains \(1/(a_k+\mu)\) (`theory/INFO_PHYSICS_GENERAL.md`, IP12, IP13). The geometric count \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\) is IP12. The factor \(K\) for identical modes remembered separately is IP13.
- The shape \(\dot Q\ge kT\) times the learning rate is Horowitz and Esposito. The factor \(2\) for a state that keeps the path is Hartich, Barato, and Seifert. The raw-coordinate gap \(kT a\) is the centered spring scored by \(\mathbb{E}[(M-X)^2]\). The telegraph ray, heat unbounded at fixed stock, is INFO_PHYSICS §4.
- Earlier holographic checks in this repository were about layer counts in Model S, not about this heat. The keystone run at \(N=0.05\) scored \(3/24\) on \(K^*=J\) and failed the equal-value check (CVs \(0.996\)–\(1.984\)); that writeup says it does not test a spatial MERA picture (`theory/KEYSTONE_NOTE.md` §5). T20 is **NOT SUPPORTED**: (A) passed with the world's scale range held fixed, (B) failed (`records/reviews/t20_2026-11-20/REVIEW.md`). `theory/REVEALED_PRICES_2026-11-21.md` §5 already says the CT34 recursion is an analogy to holography, not a physical claim. `theory/SCALE_ENDS.md` and `theory/WORMHOLES.md` use the holographic bound as a capacity cap that does not bind a design.
- PR #182 has merged. T40 is the adoption item for that consolidation, and it is not applied. This note does not adopt the proposal and does not edit `THEORY.md`.

## 2. Boundary and bulk

**Class.** A-X, A-E, A-R, A-L of the attainability note: an exogenous equilibrium Ornstein–Uhlenbeck signal, a regular conditional, and a mean-squared error of an action of the current memory state. The vector form is G-X through G-L, restricted to \(D\) a multiple of the identity when a lattice is diagonalized below. The signal bath's medium heat is zero. A memory that moves \(X\) is outside.

**Proposition H-iface (PROVED, in that class).** The learning rate depends on the memory only through the conditional law of \(X\) given the memory state.

The identity in the attainability note is \(L=a(v\,\mathbb{E}[F(X\mid M)]-1)\), with \(F\) the Fisher information of \(p(x\mid m)\). An added coordinate \(Z\) that is independent of \(X\) given \(M\) does not change \(p(x\mid m,z)\). The marginal entropy of the memory does not appear. Horowitz and Esposito identify this \(L\), in steady state, with the information flow of the signal current across the cut. The mutual-information stock is constant, so the memory's transitions supply \(L\), but the lower bound is the flow.

**Proposition H-floor (already IP11; the independence is the reading).** The infimum of the memory-bath heat at decision error \(\varepsilon\in(0,v)\) is \(kT\,a(v-\varepsilon)/\varepsilon\). It is a function of the signal \((a,v)\) and of \(\varepsilon\). For a Gaussian conditional with that variance, \(\varepsilon=v\,e^{-2I}\) with \(I=I(M;X)=\tfrac12\log(v/\varepsilon)\), so the same floor is \(kT\,a(e^{2I}-1)\). The relevant mutual information of the present is in the floor. The irrelevant bulk is not.

**Check, irrelevant bulk.** An equilibrium coordinate \(dZ=-\lambda Z\,dt+\sqrt{2\lambda\,\mathrm{Var}}\,dB\) has Sekimoto heat \(0\) at every variance, by the cancellation already in INFO_PHYSICS. Its differential entropy \(\tfrac12\log(2\pi e\,\mathrm{Var})\) at variance \(10^{6}\) exceeds the entropy at variance \(1\) by \(\tfrac12\log(10^{6})=6.907755\). The decision error and \(L\) are unchanged if the action ignores \(Z\).

**Where "independent of the stored state" does not hold.**

1. **Path-keeping. FAILS** as a claim that the paid heat ignores the bulk. A state that is a sufficient statistic of the path has sensory capacity \(1\), and Hartich, Barato, and Seifert put the heat at least at twice the learning rate. Recomputed on their locus: memory rate \(9\), noise \(B=\nu^{2}/(\nu^{2}-1)\), conditional error \(0.200000000000\), learning rate \(4\), heat \(8\). The fast shrunk spring at the same conditional error has heat \(4.000020000100\) and stock \(I=0.804718956219\). The capacity-1 stock is \(0.804718956217=\tfrac12\ln 5\). The two stocks differ by \(2\times 10^{-12}\). Same stock of the present at that precision, twice the heat. The decision loss does not ask for capacity \(1\). The attaining design has path rate \(999.503125\) and capacity \(0.004002\), so the path rate is \(249.874532\) times the heat. The interface flow does not cap the path information.

2. **Raw coordinate. FAILS** for that loss, as already proved. The fast centered spring held at raw error \(0.2\) has heat \(5.000020000080\). The conditional error is \(0.166666944444\). The gap from \(R(0.2)=4\) is \(1.000020\), which is \(kT a\). The loss charged a mismatch the conditional-mean action does not use.

3. **Futile affinity. FAILS** as a claim that the paid heat is the flow. On the telegraph at Hamming error \(0.2\), the stock \(I(M;X)=0.192744757022\) is fixed by the error, the flow is \(0.831776616672\), and the heat is \(0.6\ln\rho\). At the minimal affinity the heat equals the flow. At \(\ln\rho=40\) the heat is \(24\). The floor is the flow. A non-minimizing machine pays more, and the excess is an internal cycle, not a change in the interface information.

So the floor is a function of the interface conditional, in the proved class, and it is independent of equilibrium coordinates that do not change that conditional. It is not independent of a bulk constraint that changes the task (keep the path) or the loss (score the raw coordinate), and the heat of a non-minimizing machine is not the floor.

**Holographic reading of the same facts. METAPHOR, and the extra predictions FAIL.** Susskind's abstract, fetched this session, says the three-dimensional world is an image of data stored on a two-dimensional projection, one discrete degree of freedom per Planck area. Bousso's abstract says the area of any surface limits the information content of adjacent regions, at \(10^{69}\) bits per square metre. Pastawski, Yoshida, Harlow, and Preskill build an isometry from a bulk Hilbert space to a boundary Hilbert space. Those statements bound or encode bulk degrees of freedom by a boundary.

The cost equation does not. It leaves the number of equilibrium bulk coordinates free at heat \(0\), and it leaves the path rate free to sit far above the heat. A holographic reading that added "bulk dimension is bounded by the interface flow" or "path information is bounded by the learning rate" is the pair of counterexamples above. A reading that only restates "the floor is the interface flow" adds no prediction.

## 3. Area and volume

**Model.** A \(d\)-dimensional cubic lattice, \(V=n^{d}\) sites. The precision is \(Q=\alpha I+\beta L\) with \(L\) the combinatorial Laplacian, \(\alpha>0\), \(\beta\ge 0\). The signal is the equilibrium diffusion \(dX=-QX\,dt+\sqrt{2}\,dW\). Then \(D=I\) and \(\Sigma=Q^{-1}\), which is G-E. The signal bath cancels by G-signal. Because \(D\) is a multiple of the identity, the eigenbasis of \(Q\) is a product of independent equilibrium Ornstein–Uhlenbeck modes, rates \(\lambda_k\), variances \(1/\lambda_k\). Attainment of a modal error list is IP12, not a new theorem, and it does not close IP14: IP14 is the case where \(D\) and \(\Sigma\) do not share an eigenbasis.

On the periodic lattice every degree is \(2d\), so \(\operatorname{tr}(L)=2d\,V\) and \(\operatorname{tr}(Q)=V(\alpha+2d\beta)\). The rows of \(L\) sum to \(0\). The trace does not. The zero mode has rate \(\alpha\), not zero.

**Proposition H-volume (PROVED, by IP12 plus this trace).** Fix a conditional variance \(\varepsilon\) on every mode, with \(0<\varepsilon\le 1/\lambda_{\max}(Q)\). The heat infimum is

\[
kT\sum_k\Big(\frac1\varepsilon-\lambda_k\Big)=kT\,V\Big(\frac1\varepsilon-\alpha-2d\beta\Big).
\]

The exponent in the volume is \(1\). The exponent in a cross-section \(n^{d-1}\) is \(d/(d-1)\), which is \(2\) in \(d=2\) and \(3/2\) in \(d=3\).

*Proof.* IP12 gives the sum of the scalar Kalman rates. The trace evaluation is the display. Feasibility \(\varepsilon\le 1/\lambda_{\max}\) is the requirement that \(\varepsilon I\preceq\Sigma\). The constant assignment meets the trace constraint on the conditional covariance with equality in \(\operatorname{tr}(S^{-1})\ge V^{2}/\operatorname{tr}(S)\), so no other conditional covariance of the same trace has a lower learning-rate bound. ∎

**Sweep, the even-grid identity.** Eighteen cells, \(d\in\{1,2,3\}\), \(\alpha\in\{0.3,1,3\}\), \(\beta\in\{0.25,1\}\), \(\varepsilon\) half the smallest prior variance, and every side even, so the Brillouin zone contains \(k=\pi\) and \(\lambda_{\max}=\alpha+4d\beta\) does not depend on \(n\). The heat is then exactly \(V(1/\varepsilon-\alpha-2d\beta)\). A regression of that identity returns slope \(1.000000000000\), with ordinary-least-squares standard error at most \(8.1\times 10^{-16}\) and a standard deviation of the eighteen slopes of \(1.6\times 10^{-16}\). Those digits are roundoff. The cross-section slopes are the same identity written against \(n^{d-1}\): \(2.000000000000\) in \(d=2\) and \(1.500000000000\) in \(d=3\), standard error at most \(1.4\times 10^{-15}\).

On odd sides \(\lambda_{\max}=\alpha+2d\beta(1+\cos(\pi/n))\) still moves, and \(\varepsilon=\tfrac12/\lambda_{\max}\) moves with it. For \(d=1\), \(\alpha=\beta=1\), and \(n\in\{9,15,21,31,45,63\}\), heat per site runs from \(6.758770\) to \(6.995028\), toward the even-grid value \(7\), and the slope is \(1.016062\) with standard error \(4.3\times 10^{-3}\).

**Half the prior mean, water-fill.** Modes whose prior variance lies below the water level stay blind. The heat is still extensive. At \(\alpha=\beta=1\):

| \(d\) | slope in \(\log V\) | standard error | sizes |
|---|---|---|---|
| 1 | \(1.000676\) | \(3.76\times 10^{-4}\) | 6 |
| 2 | \(1.016876\) | \(8.07\times 10^{-3}\) | 7 |
| 3 | \(1.011036\) | \(4.46\times 10^{-3}\) | 6 |

The tracked fraction stays a positive density. On the \(\alpha=\beta=1\) grids the smallest fraction is \(0.625\), the first \(d=1\) point. A fixed fraction of the prior mean does not collapse onto a surface.

**One global mode. PROVED, exponent \(0\).** The normalized zero mode has rate \(\alpha\) and variance \(1/\alpha\). Its heat at modal error \(s\) is \((1-\alpha s)/s\), with no \(V\) in it. At \(s=1/(2\alpha)\) the heat is \(1\) at every volume. The slope against \(\log V\) is \(0\), standard error \(0\), five sizes. An area exponent \(d-1\) would grow. This observable does not.

**Disordered mass. PROVED, exponent \(1\).** On-site masses of mean \(1\), periodic \(d=2\), \(\beta=1\), and one fixed \(\varepsilon=0.5/9.5\). The floor is \(V/\varepsilon-\operatorname{tr}(Q)\), and \(\operatorname{tr}(Q)=\sum\alpha_i+4V\), so only the mean mass enters. A uniform draw recentered to mean \(1\) and a linspace with the same mean both give heat per site \(14\) at every size from \(n=4\) to \(n=16\). The arrangement does not enter the heat. The slope is \(1\), and the regression standard error \(8.5\times 10^{-16}\) is roundoff on that constant.

**Proposition H-surface (PROVED).** Let a memory's observation be any coordinate set \(B\) of size \(A\), and let \(Q\succeq\alpha I\). Perfect observation of \(B\) removes at most \(A/\alpha\) from the total variance \(\operatorname{tr}(\Sigma)\). A noisy observation removes less.

*Proof.* \(\Sigma=Q^{-1}\preceq\alpha^{-1}I\), so \(\Sigma^{2}\preceq\alpha^{-1}\Sigma\). The removed variance is \(\operatorname{tr}\big((H\Sigma H^{\top})^{-1}H\Sigma^{2}H^{\top}\big)\). The congruence \(H\Sigma^{2}H^{\top}\preceq\alpha^{-1}H\Sigma H^{\top}\) gives the trace at most \(A/\alpha\). ∎

A per-site gap \(\delta>0\) needs a removal of at least \(\delta V\). A surface has \(V/A\to\infty\), so past a finite size the cap lies below the gap. For a \(10\%\) cut of the total variance the bound first fails the surface at \(n=44\) in \(d=1\) (\(\alpha=\beta=1\), cap \(2\), need \(2.0077\); \(n=43\) still fits), at \(n=156\) in \(d=2\) (cap \(620\), need \(622.92\), \(V=24336\); \(n=155\) still fits), and at \(n=210\) in \(d=3\) with \(\beta=0.5\) (need \(262195.96\), cap \(262088\), \(A=262088\), \(V=9261000\); \(n=209\) still has need \(258473.61\) under cap \(259586\)). Side \(212\) is the first multiple of \(4\) past that crossing, not the first side. The cap is sufficient. The realized removal is smaller: four random subsets in the checks sit strictly under the cap.

**Open cubes, the removal that is actually achieved.** Perfect observation of the geometric surface, conditional covariance of the interior equal to the interior precision block.

- In \(d=1\), \(\alpha=\beta=1\), the removed variance is \(1+1/\sqrt{5}=1.447213595500\). From \(n=32\) the computed removal matches that constant. The slope against \(\log V\) is \(0\) within \(4\times 10^{-13}\). The per-site gap has slope \(-1\), standard error \(3.9\times 10^{-13}\). The fractional gap falls from \(0.1915\) to \(0.0168\).
- In \(d=2\), \(n=8\) to \(24\), the removal against the surface size has slope \(0.979510\), standard error \(1.98\times 10^{-3}\). The fractional gap falls from \(0.5403\) to \(0.2122\).
- In \(d=3\), \(\beta=0.5\), \(n=4\) to \(10\), the removal against the surface size has slope \(0.963462\), standard error \(4.38\times 10^{-3}\). The fractional gap falls from \(0.9084\) to \(0.5430\). The surface is still half the cube at \(n=10\) (\(A/V=0.488\)), which is why the fraction is still large. The cap above is what carries the large-\(n\) statement.

**Open-cube bulk floor.** With one fixed \(\varepsilon\), the heat splits exactly into a volume piece and a surface piece,

\[
\dot Q=\;V\Big(\frac1\varepsilon-\alpha-2d\beta\Big)+2d\beta\,\frac{V}{n}.
\]

The second piece is the missing degree on the boundary. Its share of the heat falls with \(n\): from \(0.0175\) to \(0.0011\) in \(d=1\), from \(0.0371\) to \(0.0096\) in \(d=2\), and from \(0.0747\) to \(0.0262\) in \(d=3\). Ordinary-least-squares slopes on these short cubes sit slightly below \(1\) because that share is shrinking: \(0.994254\pm 0.001269\) (\(d=1\)), \(0.989972\pm 0.001163\) (\(d=2\)), \(0.984548\pm 0.001792\) (\(d=3\)). The leading term is the volume.

**The field's own mutual information is a different quantity. KNOWN, and the bulk heat does not follow it.** Wolf, Verstraete, Hastings, and Cirac state that the information in part of a thermal system scales with the area of the cut. Eisert, Cramer, and Plenio review the same shape for the entanglement entropy of ground states. On this Gaussian field the check is numerical, not a new theorem. In \(d=1\), \(I(\text{half};\text{half})\) is \(0.157705\) from \(n=16\) through \(n=96\). In \(d=2\), the fit that still contains \(n=4\) (sizes \(4\) through \(16\)) has slope \(0.922298\), standard error \(0.02994\). From \(n=8\) through \(n=24\) the slope is \(0.998901\), standard error \(5.4\times 10^{-4}\), and \(I/\text{cut}\) stays \(0.032174\). On those same lattices the per-site heat of holding every site, against linear size, has slope \(2\). The field's mutual information tracks the cut. The heat of holding every site tracks the volume.

**Holding the cut, not the cube. PROVED as the cost equation on those sites; METAPHOR as a holographic encoding.** Take the same \(\varepsilon=\tfrac12/\lambda_{\max}\) and charge it only on a designated set \(B\). For \(M=Q+\Phi\) with \(\Phi\succeq 0\),

\[
S_{bb}=e_b^\top M^{-1}e_b\ge\frac1{Q_{bb}+\Phi_{bb}},
\]

so a conditional variance \(S_{bb}\le\varepsilon\) forces \(\Phi_{bb}\ge 1/\varepsilon-Q_{bb}\) whenever that quantity is positive. Summing the designated sites and using \(\sum_{b\in B}\Phi_{bb}\le\operatorname{tr}(\Phi)\) gives

\[
L=\operatorname{tr}(\Phi)\ge\sum_{b\in B}\Big(\frac1\varepsilon-Q_{bb}\Big).
\]

On the periodic lattice \(Q_{ii}=\alpha+2d\beta\). For \(\alpha=\beta=1\) and \(d=2\), even \(n\), \(\lambda_{\max}=9\), \(\varepsilon=1/18\), and the bound is \(13\) per cut site. The bulk floor at the same \(\varepsilon\) is \(13\) per bulk site, hence \(13V\) for the cube. A uniform diagonal load on one column meets the cut tolerance from above: the cost per cut site is \(13.6104\), \(13.6063\), \(13.6059\), \(13.6058\), \(13.6058\) at \(n=6,8,10,12,16\). At \(n=16\) the total is \(217.693\) against the bound \(208\), and against a bulk floor of \(3328\). The exponent in the cut length is \(0.999690\), standard error \(1.4\times 10^{-4}\).

On a strip that is periodic of length \(8\) and open of width \(W\in\{4,6,8,12\}\), the middle row has \(Q_{ii}=5\) at every width, so the lower bound stays \(104\). The achieved cost moves from \(109.374\) at width \(4\) to \(108.847\) at width \(12\). Depth behind the cut is not a coordinate of this cost. The same load does not buy a per-site gap in the cube: the surface cap above still applies to any memory whose observation is only that cut.

**Holographic reading. FAILS.** The reading that says the minimum heat at fixed per-site error scales with the boundary is the volume exponent above. The reading that says a surface memory can hold the bulk error at an area cost is the cap \(A/\alpha\). The area scaling that does occur — the learning rate of a channel that reads \(A\) sites in noise \(\sigma^{2}\) is \(A/\sigma^{2}\), and the variance such a channel can remove is \(O(A)\) — is the cost equation applied to the sites that are actually read. **METAPHOR** if that channel is called holographic.

## 4. The ladder and MERA

Vidal's entanglement renormalization coarse-grains a block after a transformation that reduces its entanglement, and the multi-scale entanglement renormalization ansatz is a circuit of logarithmic depth with a causal structure. Evenbly and Vidal insert disentanglers and isometries and recover scale invariance at a critical point. Swingle reads that scale organization as a discrete geometry, anti-de Sitter at a critical point. Nishioka reviews entanglement entropy, holography, and the renormalization group as one subject. None of those papers is a heat floor for a memory.

**What matches a formula already proved. METAPHOR if it is called a layer of MERA.**

- On the infinite equal-variance ladder, \(w(\rho\mu)=\rho\,w(\mu)\). That is G-scale. Recomputed on a truncation \(k\in[-80,80]\) at \((\rho,\mu)=(2,4)\) and \((10,10)\): each of four successive stake ratios equals \(\rho\) to the printed \(10^{-12}\).
- The per-mode tracked count is \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\) once the slowest mode pays. That is IP12. A MERA depth is also a logarithm of a scale range. The count was not produced by a coarse-graining map.

**What does not match.**

**Proposition H-octave (PROVED, from G-scale).** On the sum loss the heat is \(kT\mu\). Passing to the next octave, \(\mu\to\rho\mu\), adds heat \(kT\mu(\rho-1)\). The next octave adds \(\rho\) times that increment. The increment is not constant.

Checked at both \(\rho=2\) and \(\rho=10\): three successive increment ratios equal \(\rho\).

**Proposition H-share (PROVED, algebra on the sum-loss gains).** G-sum sets \(g_k=1/(a_k+\mu)\) and \(\sigma^{2}=\sum_k a_k v_k g_k^{2}/\mu\). The learning rate of the channel is \(\sum_k a_k v_k g_k^{2}/\sigma^{2}=\mu\). The summand, the learning-rate share, is

\[
\frac{a_k v_k}{(a_k+\mu)^{2}\,\sigma^{2}}.
\]

The weight \(a_k v_k/(a_k+\mu)^{2}\) is the numerator. On the truncation \(k\in[-80,80]\) at \((\rho,\mu)=(2,4)\) those weights sum to \(0.360674\), not to \(\mu=4\). Dividing by \(\sigma^{2}=0.090168\) makes the shares sum to \(4\). At \((10,10)\) the weights sum to \(0.043711\), \(\sigma^{2}=0.004371\), and the shares sum to \(10\). The ratio of two shares equals the ratio of two weights. At \(a=\mu\) and at \(a=\mu\rho^{2}\),

\[
\frac{\mathrm{share}(\mu)}{\mathrm{share}(\mu\rho^{2})}=\frac{(\rho^{2}+1)^{2}}{4\rho^{2}}.
\]

This equals \(1.562500\) at \(\rho=2\) and \(25.502500\) at \(\rho=10\). A flat cost per octave would give \(1\). The checks compare the weights and the shares; both ratios match.

**Per-mode heats are not equal either.** At the stake where mode \(K=10\) of a ladder \(a\rho^{k-1}\) with \(\rho=2\) is just at threshold, the heat of mode \(j<K\) is \(a\rho^{j-1}(\rho^{(K-j)/2}-1)\). The smallest is \(21.627417\) and the largest is \(128\). The ratio is \(5.918414\).

**The sum-loss memory does not add a layer per octave. FAILS** as a MERA depth. The precision update of the sum-loss channel is the rank-one matrix \(gg^{\top}\). At \(K=2,4,8\) modes the rank is \(1\), while an octave count would be \(2\), \(4\), and \(8\). IP13 already says the heat-optimal memory on the sum loss has one coordinate. There is no disentangler, no isometry, and no causal cone. The gain \(g_k=1/(a_k+\mu)\) is one linear functional of every mode.

Stoudenmire's multi-scale tensor network, and the Glasser, Pancotti, and Cirac generalized tensor networks, are classifiers trained on data. The abstracts describe coarse-graining and supervised training. They do not give a bath heat, and this note does not import one.

Maldacena's large-\(N\) limit puts a supergravity sector on anti-de Sitter space inside a conformal field theory. Ryu and Takayanagi read entanglement entropy as the area of a minimal surface. Almheiri, Dong, and Harlow read bulk locality as a quantum error-correcting code. Pastawski, Yoshida, Harlow, and Preskill build an isometry from a bulk space onto a boundary space. Hayden, Nezami, Qi, Thomas, Walter, and Yang derive a Ryu–Takayanagi formula for random tensor networks. Those are encoding statements about a bulk and a boundary. None of them is this bath heat, and none of them is the cut cost above.

## 5. The metaphor check

For each correspondence, the question is whether the holographic reading predicts a measurement the cost equation does not.

| Correspondence | Extra prediction | Cost equation | Label |
|---|---|---|---|
| The floor is the interface flow | none: this is Horowitz–Esposito plus IP11 | the same floor | **METAPHOR** as a name; the floor statement is **PROVED** |
| Bulk degrees of freedom are bounded by that flow | a cap on equilibrium bulk entropy, or on the path rate | entropy of an equilibrium coordinate is free at heat \(0\); path rate \(999.503\) at heat \(4.000020\) | **FAILS** |
| Minimum heat at fixed per-site error on every site scales with area | exponent \(1\) in the surface size | even-grid identity \(V(1/\varepsilon-\alpha-2d\beta)\), exponent \(1\) in the volume; odd sides give slope \(1.016\) | **FAILS** |
| A surface memory holds the bulk error at an area cost | per-site gap stays fixed as \(V\) grows | removal at most \(A/\alpha\); first failure of a \(10\%\) cut at sides \(44\), \(156\), \(210\) | **FAILS** |
| Minimum heat at fixed per-site error on a designated cut scales with the cut | a bulk stored on that cut, including the depth behind it | at least \(\lvert B\rvert(1/\varepsilon-Q_{ii})\), here \(13\) per cut site, met at about \(13.61\); the strip cost stays near \(109\) as the depth runs from \(4\) to \(12\). The bulk floor at the same \(\varepsilon\) is \(13\) per bulk site | **PROVED** as the cost equation on the sites the decision names; **METAPHOR** as a holographic encoding. Depth is not in the cost |
| The field's mutual information scales with the cut | this is Wolf, Verstraete, Hastings, and Cirac, about the field | the heat on the same lattices scales with volume | **KNOWN** for the field; **METAPHOR** if read as the cost |
| Equal heat per octave | increment independent of the octave | increment scales by \(\rho\) | **FAILS** |
| MERA depth equals the octave count, as a memory degree | degree grows as \(\log(w)\) | sum-loss degree is \(1\); the half-tracked count is already G-scale | degree claim **FAILS**; the count is **METAPHOR** |

No row is a holographic prediction that is both extra and true. The cut row is area scaling of the heat, and it is the cost equation on the sites the decision names. The bulk per-site floor on the same tolerance scales with the volume.

## 6. What this note does not do

It does not edit `THEORY.md`, `CORE.md`, or `README.md`. It does not adopt \(J_{\mathrm{phys}}\) into the master equation. It does not close IP14, and it does not treat a diffusion whose noise does not share the eigenbasis of \(\Sigma\). It does not give an equilibrium floor for a massless field on the torus: \(\alpha>0\) is what keeps the variance finite, and \(\alpha\to 0\) leaves G-E. It does not rerun T20 or the keystone holographic check. Ruin, linking, the stake \(w\), and H3 stay where the heat notes left them.

A follow-up on Sierpiński graphs is `theory/FRACTAL_WORLD_2026-11-22.md`. On those graphs the heat floor tracks the sites the decision names, not the Hausdorff or spectral dimension. That note is a self-check, not an independent review (OPEN_WORK T54). This page does not treat that review as done.

## 7. Checks

`theory/holographic_checks/holographic_checks.py`. 175 checks, FAILS 0. The numbers in §§2–5 are the numbers it prints.

## 8. References

Fetched this session. Abstracts from the arXiv API unless the line says otherwise. Crossref HTTP 200 for every DOI.

Horowitz, J. M., and Esposito, M. 2014. Thermodynamics with continuous information flow. *Phys. Rev. X* 4:031015. doi 10.1103/PhysRevX.4.031015.

Hartich, D., Barato, A. C., and Seifert, U. 2016. Sensory capacity: an information theoretical measure of the performance of a sensor. *Phys. Rev. E* 93:022116. doi 10.1103/PhysRevE.93.022116.

't Hooft, G. 1993. Dimensional reduction in quantum gravity. arXiv gr-qc/9310026. Crossref returned no work record for this essay on 22 November 2026. Already recorded that way in `theory/REVEALED_PRICES_2026-11-21.md`.

Susskind, L. 1995. The world as a hologram. *J. Math. Phys.* 36:6377. doi 10.1063/1.531249.

Bousso, R. 2002. The holographic principle. *Rev. Mod. Phys.* 74:825. doi 10.1103/RevModPhys.74.825.

Maldacena, J. 1999. The large-\(N\) limit of superconformal field theories and supergravity. *Int. J. Theor. Phys.* 38:1113. doi 10.1023/A:1026654312961.

Ryu, S., and Takayanagi, T. 2006. Holographic derivation of entanglement entropy from the anti–de Sitter space/conformal field theory correspondence. *Phys. Rev. Lett.* 96:181602. doi 10.1103/PhysRevLett.96.181602.

Almheiri, A., Dong, X., and Harlow, D. 2015. Bulk locality and quantum error correction in AdS/CFT. *J. High Energy Phys.* 04:163. doi 10.1007/JHEP04(2015)163.

Pastawski, F., Yoshida, B., Harlow, D., and Preskill, J. 2015. Holographic quantum error-correcting codes: toy models for the bulk/boundary correspondence. *J. High Energy Phys.* 06:149. doi 10.1007/JHEP06(2015)149.

Hayden, P., Nezami, S., Qi, X.-L., Thomas, N., Walter, M., and Yang, Z. 2016. Holographic duality from random tensor networks. *J. High Energy Phys.* 11:009. doi 10.1007/JHEP11(2016)009.

Vidal, G. 2007. Entanglement renormalization. *Phys. Rev. Lett.* 99:220405. doi 10.1103/PhysRevLett.99.220405.

Vidal, G. 2008. Class of quantum many-body states that can be efficiently simulated. *Phys. Rev. Lett.* 101:110501. doi 10.1103/PhysRevLett.101.110501.

Swingle, B. 2012. Entanglement renormalization and holography. *Phys. Rev. D* 86:065007. doi 10.1103/PhysRevD.86.065007.

Evenbly, G., and Vidal, G. 2015. Tensor network renormalization. *Phys. Rev. Lett.* 115:180405. doi 10.1103/PhysRevLett.115.180405.

Wolf, M. M., Verstraete, F., Hastings, M. B., and Cirac, J. I. 2008. Area laws in quantum systems: mutual information and correlations. *Phys. Rev. Lett.* 100:070502. doi 10.1103/PhysRevLett.100.070502.

Eisert, J., Cramer, M., and Plenio, M. B. 2010. Colloquium: Area laws for the entanglement entropy. *Rev. Mod. Phys.* 82:277. doi 10.1103/RevModPhys.82.277.

Nishioka, T. 2018. Entanglement entropy: holography and renormalization group. *Rev. Mod. Phys.* 90:035007. doi 10.1103/RevModPhys.90.035007.

Stoudenmire, E. M. 2018. Learning relevant features of data with multi-scale tensor networks. *Quantum Sci. Technol.* 3:034003. doi 10.1088/2058-9565/aaba1a.

Glasser, I., Pancotti, N., and Cirac, J. I. 2020. From probabilistic graphical models to generalized tensor networks for supervised learning. *IEEE Access* 8:68169. doi 10.1109/ACCESS.2020.2986279.
