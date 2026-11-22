# Boundary sufficiency

*Sunday 22 November 2026. A self-check, not an independent review. The hypothesis sentence is unchanged. The master equation in THEORY is unchanged. `THEORY.md`, `CORE.md`, and `README.md` are not edited. The preregistration `theory/boundary_checks/PREREG.md` is commit `93084b0`, sha256 `58ba0ebaa19d126d8c47293bc82d598f4416832b1bf767c64c73e9d175de943c`, and it was not edited after the run. Checks: `theory/boundary_checks/boundary_checks.py`, run at `nice -n 19` (107 checks, FAILS 0, one radius-ratio puzzle). DOIs resolved on the Crossref API on 22 November 2026 are listed in `theory/boundary_checks/crossref.out` and in the preregistration.*

Labels: **PROVED** (a proof is on this page, in the class named with it, and the arithmetic is in the checks), **KNOWN** (published, fetched this session, and not claimed here), **FAILS** (a counterexample is on this page), **METAPHOR** (the name adds no prediction the cost equation does not already make), **OPEN** (named, not settled). GTAO is the theory in this repository.

The sentence of the hypothesis is unchanged, byte for byte:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

## 0. The answer

For decisions outside a region, yes, up to a cost that does not grow with the volume. In the equilibrium Gaussian field of the holographic note, local coupling means the precision is zero across any pair that does not share an edge. The conditional law of the exterior given the region then equals the conditional law given the region's Markov blanket, the neighbor set. The decision loss is the same. The heat of a channel that sees the whole region exceeds the heat of a channel that sees only the blanket by at most the trace of one Schur complement, and that trace stays near \(1.291\) on the gasket while the region grows from \(4\) sites to \(121\).

The strict sentence "the heat-minimizing channel is supported on the blanket coordinates alone" does not hold. On the path of three, a channel that mixes the interior site with the blanket site reaches exterior variance \(13/25\) at trace \(10.1\). The blanket-only channel that matches it has trace \(10.5\). The gap \(0.4\) sits inside the cap \(1/2\).

Decisions about the interior are not boundary-sufficient. Given the blanket, every interior variance is at least \(1/5\), and the tolerance \(1/18\) is smaller than that. On the gasket the blanket holding bound stays \(26\) at every generation, and the region holding bound runs \(54, 171, 522, 1575\).

The screening fails when the precision is not local, and when the world is not Markov. A finite-range discrete step thickens the blanket by horizon times speed. The continuous-time field does not: the heat kernel is positive at every distance for every positive time, so no finite shell screens. Its walk-kernel second moment is \(2t\), diffusive. The locked \(5\%\) radius of the conditional variance is \(2\) at both \(\tau=1/2\) and \(\tau=1\), on the path of \(31\) and again on the path of \(61\). That comparison is a puzzle. The diagnosis is in §5.

Under a precision cap of \(1\) and the ruin cap of the memory note, a one-dimensional blanket statistic is held by a pool of units, not by copies of one unit. A per-site exterior loss does not collapse onto one sum of the blanket. Those are the two different ways of being spread out.

Nothing on this page is an AdS/CFT dictionary or a black-hole entropy.

## 1. Already in the repository

None of the following is a result of this note.

- The field and the heat. \(Q=\alpha I+\beta L\), \(\alpha=\beta=kT=1\), signal \(dX=-QX\,dt+\sqrt{2}\,dW\). Because the diffusion matrix is the identity, the heat of a precision update \(\Phi\succeq 0\) is \(\operatorname{tr}(\Phi)\). Holding a designated set \(B\) to per-site variance \(\varepsilon\) costs at least \(\sum_{b\in B}(1/\varepsilon-Q_{bb})\). On the even periodic square, \(\varepsilon=1/18\), that bound is \(13\) per cut site, met by a uniform diagonal load at about \(13.61\) (`theory/HOLOGRAPHIC_2026-11-22.md`). This note uses \(\varepsilon=1/18\) and does not re-fit that load.
- The same note's surface cap: a memory whose observation is a set of size \(A\) removes at most \(A/\alpha\) from the total variance. A per-site gap in the volume is not an area cost. That is the converse direction, already proved for the bulk error. This note proves the matching positive statement for exterior decisions.
- The memory note (`theory/HOLOGRAPHIC_MEMORY_2026-11-22.md`). A shared coordinate wins when the decision is a sum. Item copies win, or tie, when every item is read alone. Under a per-unit precision cap below \(V/\varepsilon_{\mathrm{cap}}-1\), a pool of the units can meet a ruin cap that non-pooling copies miss. This note applies that comparison to a blanket statistic. It does not redo the four-item costs \(5.583360\) and \(17.583360\).

## 2. The conditional law

**Class B.** The field of §1 on a finite undirected graph. For a region \(R\), the blanket \(B\) is the set of vertices outside \(R\) adjacent to \(R\), and \(E\) is the rest. Then \(Q_{RE}=0\).

**Proposition BS-screen (PROVED; the zero pattern is KNOWN).** \(X_R\perp X_E\mid X_B\). The conditional covariance of \(X_E\) given \(X_B\) equals the conditional covariance given \(X_{R\cup B}\), and both equal \(Q_{EE}^{-1}\).

*Proof.* Order the coordinates as \(R,B,E\). The cross block \(Q_{RE}\) is zero because every edge out of \(R\) lands in \(B\). The conditional precision of \((X_R,X_E)\) given \(X_B\) is the principal block of \(Q\) on \(R\cup E\), which is block diagonal. A block-diagonal conditional precision is conditional independence, and the conditional covariance of \(X_E\) is the inverse of its diagonal block \(Q_{EE}\). Conditioning on \(X_R\) as well does not change that block. ∎

Speed and Kiiveri, abstract fetched, say that Gaussian Markov distributions are characterised by zeros in the inverse of the covariance and that those zeros are conditional independencies. Besag, abstract fetched, gives an alternative proof of the Hammersley–Clifford theorem and names Gaussian lattice schemes. The argument above is the conditional-precision step for this \(Q\). It does not quote a proof from either paper. Lauritzen's book was fetched; its abstract describes the monograph and does not state this block formula. The 1971 Hammersley–Clifford manuscript did not appear on the first page of the bibliographic query recorded in the preregistration. No formula is taken from it.

**Proposition BS-loss (PROVED).** Let \(Y\) be any channel of \(X_{R\cup B}\): given the region, \(Y\) is independent of \(X_E\). Then \(X_E\perp Y\mid X_B\), and

\[
\operatorname{Var}(X_E\mid Y)=Q_{EE}^{-1}+M\,\operatorname{Var}(X_B\mid Y)\,M^{\top},
\]

where \(M\) is the regression of \(X_E\) on \(X_B\) and does not depend on \(Y\). An exterior mean-square loss is therefore a function of the posterior of the blanket alone. Matching that posterior matches the decision loss, whether or not the channel also saw the interior.

*Proof.* \(Y\) is generated from \((X_R,X_B)\) and noise independent of \(X\). BS-screen gives \(X_E\perp(X_R,\text{noise})\mid X_B\), hence \(X_E\perp Y\mid X_B\). The usual Gaussian decomposition of the conditional variance is the display. The regression \(M=\Sigma_{EB}\Sigma_{BB}^{-1}\) is a property of the prior. ∎

On the path of three, \(R=\{0\}\), \(B=\{1\}\), \(E=\{2\}\),

\[
\Sigma=\frac18\begin{pmatrix}5&2&1\\2&4&2\\1&2&5\end{pmatrix}.
\]

\(\operatorname{Var}(X_2\mid X_1)=\operatorname{Var}(X_2\mid X_0,X_1)=1/2\). \(\operatorname{Var}(X_2\mid X_0)=3/5\), so the interior without the blanket is not enough. \(I(X_0;X_2)=\tfrac12\ln(25/24)=0.020410997260\) nat. \(I(X_0;X_2\mid X_1)=0\).

The same identity is numerical on the graphs whose inverses are not written out. On the gasket subcopy the largest entrywise gap between the two exterior conditional covariances is \(2.8\times 10^{-17}\) at generation 5. On the open square of side 8, columns \(0,1,2\) against column \(3\), the gap is \(2.8\times 10^{-17}\).

## 3. The heat, and where a pure blanket support misses

**Proposition BS-cap (PROVED).** Among channels supported on \(R\cup B\), let \(\pi_C\) be the marginal posterior precision of the blanket and let \(\pi_C(0)\) be the prior marginal precision. The blanket-only update whose added precision equals \(\pi_C-\pi_C(0)\) matches \(\pi_C\), and its trace exceeds the trace of the original channel by at most

\[
\operatorname{tr}\bigl(Q_{BI}Q_{II}^{-1}Q_{IB}\bigr).
\]

*Proof.* Write \(\Phi\) in blocks on the interior \(I=R\) and the blanket \(C=B\), with no mass on \(E\). Eliminating \(I\) and \(E\) from \(Q+\Phi\), the marginal precision of \(C\) is

\[
\pi_C=Q_{CC}+\Phi_{CC}-Q_{CE}Q_{EE}^{-1}Q_{EC}-K(\Phi),
\]

\[
K(\Phi)=(Q_{CI}+\Phi_{CI})(Q_{II}+\Phi_{II})^{-1}(Q_{IC}+\Phi_{IC}).
\]

\(K(\Phi)\) is positive semidefinite. At \(\Phi=0\) the same formula is \(\pi_C(0)\), so the increment is \(\Phi_{CC}+K(0)-K(\Phi)\). Placing that increment on the blanket alone reproduces \(\pi_C\). Its trace minus \(\operatorname{tr}(\Phi)\) equals \(\operatorname{tr}(K(0))-\operatorname{tr}(K(\Phi))-\operatorname{tr}(\Phi_{II})\), which is at most \(\operatorname{tr}(K(0))\). ∎

The cap is not zero, and the minimizer need not be supported on \(B\).

**The pure-support sentence. FAILS.** On the path of three the channel with interior diagonal \(0.1\), cross entry \(1\), and blanket diagonal \(10\) has trace \(10.1\), posterior variance of the blanket \(2/25\), and exterior variance \(13/25\). The blanket-only channel with the same blanket variance has trace \(10.5\). The excess is \(0.4\), and the cap in BS-cap is \(1/2\). Forty random channels on the same two sites stayed under the cap; the largest excess was \(0.082158737532\).

A diagonal spend does not produce that saving. Precision \(2\) on the blanket alone leaves exterior variance \(9/16\). Precision \(1\) on the blanket and \(1\) on the interior leaves \(11/19\). The gap is \(5/304\), and the blanket spend is the smaller variance. Mixing, not an interior diagonal, is what beats the pure blanket at this target.

On the gasket the cap saturates. Generations \(2\) through \(5\) give

\[
1.234848484848,\ 1.290266004092,\ 1.290954813099,\ 1.290954956476.
\]

The region grows from \(4\) to \(121\). The cap grows by less than \(0.06\) after generation \(3\). The blanket holding bound stays \(26\). The achieved uniform diagonal load on the two glue vertices is \(28.605907\), \(28.582453\), \(28.581910\), \(28.581910\). The region load at the same tolerance is \(60.427399\), \(196.372369\), \(604.222673\), \(1827.773585\). At generation \(5\) the region load is \(63.95\) times the blanket load, against a site ratio \(121/2=60.5\). The volume is in the region load. It is not in the cap, and it is not in the blanket load.

On the open square the blanket bound is \(106\) and the achieved load is \(117.184595\) (\(14.648074\) per site). The region bound is \(326\).

**What the cut row was missing.** The holographic note proved that a designated cut, held to a per-site tolerance, costs order the cut, and labeled a holographic encoding of the bulk as a metaphor. The sufficient-statistic statement is a different sentence, and it is the one BS-screen, BS-loss, and BS-cap prove. The blanket does not store the interior. It screens the exterior from the interior. The heat of that screening scales with the blanket.

## 4. The converse

**Proposition BS-interior (PROVED).** For each \(i\in R\),

\[
\operatorname{Var}(X_i\mid X_B)=(Q_{RR}^{-1})_{ii}\ge\frac1{Q_{ii}}.
\]

If every degree is at most \(4\) and \(\alpha=\beta=1\), then \(Q_{ii}\le 5\) and the conditional variance is at least \(1/5\). Since \(1/5>1/18\), a perfect observation of the blanket misses the interior tolerance. The holding bound on \(R\) is the cut bound of the holographic note and scales with \(|R|\).

*Proof.* \(B\subset V\setminus\{i\}\), so conditioning on \(B\) leaves at least the conditional variance given every other site, which is \(1/Q_{ii}\). By BS-screen, \(X_R\perp X_E\mid X_B\), so the conditional law of \(X_R\) given \(X_B\) is the conditional law given \(X_{B\cup E}\), whose covariance is \(Q_{RR}^{-1}\). The diagonal inequality \((A^{-1})_{ii}\ge 1/A_{ii}\) is the same comparison inside \(R\). ∎

On the path of three the interior variance given the blanket is \(1/2\). On the path of five, \(\operatorname{Var}(X_2\mid X_1,X_3)=1/3\). On the gasket the smallest interior conditional variance is \(0.227272727273\) at generation \(2\) and \(0.247979948223\) at generation \(5\). On the square it is \(0.234882445959\). All sit above \(1/5\), and the checks match the diagonals of \(Q_{RR}^{-1}\).

**Encoding of the interior on the boundary. FAILS, and the name is METAPHOR.** A memory that holds the blanket at any finite or perfect precision does not bring an interior site down to \(1/18\). The area law of the cut is the cost of the sites the decision names. It is not a copy of the cube behind them. That is the sentence the holographic note already filed as a metaphor. This note does not withdraw it.

## 5. Where the screening stops

**Long-range coupling. The local blanket FAILS.** On the path of three, put \(-\gamma\) in the corner entries and add \(\gamma\) to those diagonals, \(\gamma=1\). Then \(I(X_0;X_2\mid X_1)=\tfrac12\ln(9/8)=0.058891517828\), and the partial correlation is \(1/3\). At \(\gamma=0\) the conditional information is \(0\). One extra edge is enough. The blanket is the neighbor set of the precision, not the neighbor set of a drawing that omitted that edge.

**A non-Markov covariance. FAILS.** Three sites, unit variance, covariance \(1/2\) off the diagonal. The conditional information of the ends given the middle is again \(\tfrac12\ln(9/8)\), partial correlation \(1/3\). The precision of this covariance is not a path.

**A non-Markov time series. FAILS.** \(X_t=\xi_t+\xi_{t-1}\) with standard normal independent \(\xi\). The unconditional correlation of \(X_0\) and \(X_2\) is \(0\). Given \(X_1\) the conditional correlation is \(-1/3\), and the conditional information is \(\tfrac12\ln(9/8)\). The present does not screen the past from the future. A spatial boundary has nothing to screen here: the missing variable is the latent shock.

**Finite speed. PROVED, thickness equals horizon times speed.** Present sites independent and standard normal. Range \(1\), self weight \(1/2\), neighbor weight \(1/4\). The excess conditional variance of site \(0\) at horizon \(H\), from dropping the site at distance \(H\), is \(1/16\), \(1/256\), and \(1/4096\) at \(H=1,2,3\). Every coefficient beyond distance \(H\) is \(0\). Range \(2\), self \(1/2\) and weight \(1/6\) at distances \(1\) and \(2\): at horizon \(1\) the excess of dropping site \(2\) is \(1/36\), and the cutoff is distance \(2\); at horizon \(2\) the coefficient of site \(4\) is \(1/36\), the excess is \(1/1296\), and the cutoff is distance \(4\). The shell thickens by the range at each step.

**Continuous time. A finite shell FAILS. Linear thickening is not what the kernel does.** On the infinite path, \(e^{-tL}_{0,d}=e^{-2t}I_d(2t)\). The second moment is \(2t\): the series through distance \(40\) gives \(1.000000000000\) at \(t=1/2\) and \(4.000000000000\) at \(t=2\), and the mass is \(1\) at both. Doubling the root-mean-square distance takes a factor four in time, not a factor two. The regression kernel of \(Q=I+L\) is \(e^{-3\tau}I_d(2\tau)\), positive at every distance. The smallest value printed, distance \(15\) at \(\tau=1/2\), is \(5.289\times 10^{-18}\).

On the path of \(31\) sites the conditional variance \(\Delta(r)\) of the center's future mean, given the ball of radius \(r\), is positive for every \(r<15\) and zero at \(r=15\), at \(\tau=1/2\) and at \(\tau=1\). The smallest positive value is \(1.908\times 10^{-33}\) and \(1.853\times 10^{-27}\). There is no hard cutoff.

**The radius ratio. A puzzle.** The locked radius is the smallest \(r\) with \(\Delta(r)\le 0.05\,\Delta(0)\). It is \(2\) at \(\tau=1/2\) and \(2\) at \(\tau=1\). The ratio is \(1\), which is below the locked band \(1.05\). The named next test, the same definition on a path of \(61\), returns \(2\) and \(2\) again. The path length was not the cause.

The diagnosis is the size of the step. At \(\tau=1/2\), \(\Delta(1)/\Delta(0)=0.05283\) and \(\Delta(2)/\Delta(0)=0.001351\). At \(\tau=1\) the same ratios are \(0.1569\) and \(0.01365\). The level \(0.05\) sits in the gap between radius \(1\) and radius \(2\) at both times, so the integer radius cannot move. A square-root factor \(\sqrt{2}\) and a linear factor \(2\) are both smaller than that gap. The second-moment identity is the diffusive statement, and it passed. The \(5\%\) radius is too coarse to see it. A finer threshold would be a new preregistration. It is not substituted here.

## 6. Pooled or spread along the blanket

**One functional. PROVED, by the memory note's capacity comparison applied to the blanket.** On the path of three the exterior decision is a function of site \(1\). Prior variance of that site \(1/2\). Precision \(\Phi\) on it gives blanket variance \(1/(2+\Phi)\) and exterior variance \(1/2+1/(4(2+\Phi))\). The tolerance \(0.55\) needs \(\Phi\ge 3\).

Each unit installs precision at most \(c=1\), pays that as heat, and pays upkeep \(1/2\). Failures are independent with probability \(1/5\). The cap is a chance at most \(0.05\) that the exterior variance exceeds \(0.55\). Stake weight \(1\).

A copy keeps the best survivor. Its best up-state variance is \(7/12>0.55\), at every count. No copy meets the cap.

A pool adds the survivors. It needs three. At five units the chance of three or more is \(2944/3125=0.94208\), short of \(0.95\). At six units it is \(15360/15625=0.98304\). Six is the smallest count from \(1\) to \(8\). The expected decision variance is \(470459/875000=0.537667428571\). Heat plus upkeep is \(9\). The cost is \(8345459/875000=9.537667428571\).

This is the capacity-limited pool. It is not a reason to add the interior, and it is not a reason to replace the blanket by one coordinate when the decision has rank greater than one.

**Several sites. The global sum FAILS for a per-site loss, and it is sufficient for the sum.** On the path of five, \(B=\{1,3\}\), ends \(\{0,4\}\), deep site \(\{2\}\). \(\operatorname{Var}(X_0\mid X_1)=1/2\). \(\operatorname{Var}(X_0\mid X_1+X_3)=121/220\). The sum of the two end variances is \(1\) given both blanket sites and \(121/110\) given only their sum. The pooled statistic is worse by \(1/10\).

For \(Z=X_0+X_4\) the same sum of the blanket matches conditioning on both sites: both posterior variances of \(Z\) equal \(1\), to the checker. One coordinate is the sufficient statistic for the sum, as in the memory note's aligned pool. It is not the sufficient statistic for the two ends scored separately, as in that note's per-item loss.

The trace cap on this path is \(2/3\). Thirty random channels stayed under it. The largest excess was \(0.034554\).

So the boundary memory is spread in two senses, and they answer different questions. Along the blanket, a per-site exterior loss keeps the local sites; one pooled sum of those sites does not. Across units that each see the same local statistic, a precision cap below the tolerance selects the pool and leaves the copy infeasible. Both are proved. Calling either one a hologram does not add a third prediction.

## 7. Physics, not identified

The Markov property is a statement about a classical Gaussian precision. It does not build a bulk metric, a conformal boundary, or an isometry from a bulk Hilbert space onto a boundary space.

Maldacena's record was fetched again this session, the same DOI as in the holographic note. That note already says what the fetched abstract supports, a large-\(N\) limit with a supergravity sector on anti-de Sitter space inside a conformal field theory. No map of that kind is constructed here.

Bekenstein, "Black Holes and Entropy," *Phys. Rev. D* 7:2333–2346 (1973), doi `10.1103/PhysRevD.7.2333`, and Hawking, "Particle creation by black holes," *Commun. Math. Phys.* 43:199–220 (1975), doi `10.1007/BF02345020`, resolve on Crossref. Neither record contained an abstract. No entropy formula is taken from either paper. The cost in this note is \(\operatorname{tr}(\Phi)\) on the sites of a graph. It is not an entropy in Planck units, and it is not one quarter of a horizon area.

Wolf, Verstraete, Hastings, and Cirac are already **KNOWN** in the holographic note for an area law of mutual information, including the classical thermal case. The field's mutual information is not this heat. The checks here do not recompute it.

**METAPHOR** if the blanket is called a hologram, a bulk reconstruction, or a Bekenstein–Hawking bound. The proved substitute is BS-screen, BS-loss, BS-cap, and BS-interior.

## 8. Labels

| Claim | Label |
|---|---|
| Zeros of \(Q\) are the conditional independencies | **KNOWN** (Speed and Kiiveri; Besag names Hammersley–Clifford). The block proof for this \(Q\) is **PROVED** |
| Exterior conditional law given the region equals the law given the blanket | **PROVED** (BS-screen) |
| Exterior decision loss is a function of the blanket posterior | **PROVED** (BS-loss) |
| Blanket-only heat exceeds any region channel by at most \(\operatorname{tr}(K)\) | **PROVED** (BS-cap). On the gasket the trace settles at \(1.290955\) |
| The minimizer is supported on the blanket coordinates alone | **FAILS**. Path of three, traces \(10.1\) and \(10.5\), same exterior variance \(13/25\) |
| Interior decisions are boundary-sufficient | **FAILS**. Conditional variance at least \(1/5>1/18\) |
| Holding cost of the sufficient memory scales with the blanket, not the volume | **PROVED** as the bounds and the loads in §3. **METAPHOR** if that cost is called an encoding of the interior |
| Local screening survives a long-range edge, an equicorrelated covariance, or an MA(1) | **FAILS**. Each conditional information is \(\tfrac12\ln(9/8)\) |
| Discrete range-\(s\) dynamics: thickness \(=\) horizon times speed | **PROVED** |
| Continuous time: a finite shell screens | **FAILS**. The kernel is positive at every distance |
| Continuous time: the \(5\%\) radius thickens as \(\sqrt{\tau}\) or as \(\tau\) | **OPEN** as that comparison. The locked ratio is \(1\), a puzzle, on paths of \(31\) and \(61\). The walk second moment \(2t\) is **PROVED** and checked |
| One blanket functional, capacity cap, ruin cap: the pool meets and the copy does not | **PROVED**, as the memory note's comparison on this statistic. Six units, cost \(9.537667428571\) |
| One sum of several blanket sites is enough for a per-site exterior loss | **FAILS**. Path of five, gap \(1/10\) |
| This is AdS/CFT or the Bekenstein–Hawking area law | **METAPHOR**. No such map is shown |

## 9. Checks

`theory/boundary_checks/boundary_checks.py`. 107 checks, FAILS 0, one puzzle (the radius ratio). The numbers in §§2–6 are the numbers it prints.

The preregistration was not edited after commit `93084b0`.

## 10. References

Fetched 22 November 2026. Abstracts only where the line says the record contained one. Crossref HTTP 200 for every DOI.

Speed, T. P., and Kiiveri, H. T. 1986. Gaussian Markov distributions over finite graphs. *Ann. Statist.* 14:138–150. doi 10.1214/aos/1176349846. Abstract: zeros in the inverse characterise the conditional independencies.

Besag, J. 1974. Spatial interaction and the statistical analysis of lattice systems. *J. Roy. Statist. Soc. B* 36:192–225. doi 10.1111/j.2517-6161.1974.tb00999.x. Abstract: an alternative proof of the Hammersley–Clifford theorem, including Gaussian schemes.

Dempster, A. P. 1972. Covariance selection. *Biometrics* 28:157. doi 10.2307/2528966. No abstract in the record.

Lauritzen, S. L. 1996. *Graphical Models*. Oxford. doi 10.1093/oso/9780198522195.001.0001. Abstract describes the monograph. No block formula is taken from it.

Rue, H., and Held, L. 2005. *Gaussian Markov Random Fields*. Chapman and Hall. doi 10.1201/9780203492024. No abstract in the record.

Hammersley, J. M., and Clifford, P. 1971. The manuscript named by Besag. No work record on the first page of the bibliographic query in the preregistration.

Bekenstein, J. D. 1973. Black holes and entropy. *Phys. Rev. D* 7:2333–2346. doi 10.1103/PhysRevD.7.2333. No abstract in the record. Not used as a formula.

Hawking, S. W. 1975. Particle creation by black holes. *Commun. Math. Phys.* 43:199–220. doi 10.1007/BF02345020. No abstract in the record. Not used as a formula.

Maldacena, Wolf–Verstraete–Hastings–Cirac, and Bousso are the records already cited in `theory/HOLOGRAPHIC_2026-11-22.md`. They are not re-quoted.
