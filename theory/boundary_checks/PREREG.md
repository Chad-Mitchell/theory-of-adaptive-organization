# Preregistration: boundary sufficiency

*Sunday 22 November 2026. Locked before any assembly of a precision matrix for these claims, any inversion, any heat evaluation, and any gasket build. The check script is not in this commit. Predictions below are closed forms or arithmetic on closed forms. A later note may report what the code returned. This file is not edited after that.*

The question: in the equilibrium Gaussian field of `theory/HOLOGRAPHIC_2026-11-22.md`, is the memory a region needs for decisions outside it sufficient when it holds only the region's Markov blanket, with the same conditional law, the same decision loss, and a heat that scales with the blanket rather than the volume? Are decisions about the interior itself boundary-sufficient? Where does the screening fail: long-range coupling, a finite propagation horizon, a non-Markov world? And, under the capacity limit and ruin cap of `theory/HOLOGRAPHIC_MEMORY_2026-11-22.md`, is that boundary memory best held by pooling across units?

The cut row of the holographic note is already proved as a cost on the sites the decision names, about \(13.61\) per cut site against a bound of \(13\), and it is labeled **METAPHOR** as a holographic encoding. This file does not re-score that load. It asks whether the encoding sentence can be replaced by a sufficient-statistic sentence.

The hypothesis sentence is unchanged:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

## 0. What was fetched before this lock

Crossref API, 22 November 2026, HTTP 200 unless the line says otherwise. Nothing below is quoted from a page that was not fetched. Abstracts absent from the record are not paraphrased.

- `10.1214/aos/1176349846`. Speed and Kiiveri, "Gaussian Markov Distributions over Finite Graphs," *The Annals of Statistics* 14:138–150, issued 1986-03-01. The abstract says Gaussian Markov distributions are characterised by zeros in the inverse of their covariance matrix, and that the paper describes the conditional independencies which follow from a given pattern of zeros.
- `10.1111/j.2517-6161.1974.tb00999.x`. Besag, "Spatial Interaction and the Statistical Analysis of Lattice Systems," *Journal of the Royal Statistical Society Series B* 36:192–225, issued 1974-01-01. The abstract says a simple alternative proof of the Hammersley–Clifford theorem is presented, and that the theorem is used to construct spatial schemes, including Gaussian ones.
- `10.2307/2528966`. Dempster, "Covariance Selection," *Biometrics* 28:157, issued 1972-03. No abstract in the record.
- `10.1093/oso/9780198522195.001.0001`. Lauritzen, *Graphical Models*, book, issued 1996-05-02. The abstract describes a monograph on graphical models whose origins include statistical physics, genetics, and contingency tables. It does not state a blanket formula. The book is the reference named in the question. No sentence of a proof is taken from it.
- `10.1201/9780203492024`. Rue and Held, *Gaussian Markov Random Fields*, monograph, issued 2005-02-18. No abstract in the record.
- `10.1007/978-0-387-30164-8_509`. Encyclopedia entry "Markov Blanket," issued 2011, page 639. No authors and no abstract in the record. No definition is taken from it.
- `10.1103/PhysRevD.7.2333`. Bekenstein, "Black Holes and Entropy," *Physical Review D* 7:2333–2346, issued 1973-04-15. No abstract in the record.
- `10.1007/BF02345020`. Hawking, "Particle creation by black holes," *Communications in Mathematical Physics* 43:199–220, issued 1975-08. No abstract in the record.
- `10.1103/PhysRevLett.100.070502`, `10.1023/A:1026654312961`, and `10.1103/RevModPhys.74.825` resolve to the Wolf–Verstraete–Hastings–Cirac, Maldacena, and Bousso records already used in `theory/HOLOGRAPHIC_2026-11-22.md`. No new abstract text is added here.

A bibliographic query for "Hammersley Clifford 1971 Markov fields finite graphs lattices" returned a first page that does not contain a work record for the 1971 manuscript. Besag's abstract is the fetched sentence that names the theorem. No formula is cited from the manuscript.

The cost equation this prediction uses is already in the repository: heat \(kT\) times the learning rate, and, when the diffusion matrix is the identity, heat \(\operatorname{tr}(\Phi)\) for a precision update \(\Phi\succeq 0\) (`theory/HOLOGRAPHIC_2026-11-22.md`, the cut bound). The capacity and ruin comparison is the one in `theory/HOLOGRAPHIC_MEMORY_2026-11-22.md` §4: a pool adds precisions, a non-pooling copy keeps only the best survivor, and a one-unit copy meets a cap level only when the unit's precision cap is at least \(V/\varepsilon_{\mathrm{cap}}-1\) in that note's normalization.

## 1. Class

**Class B.** The same equilibrium field as the holographic note. Undirected graph, combinatorial Laplacian \(L\), precision \(Q=\alpha I+\beta L\), \(\alpha=\beta=kT=1\). The signal is \(dX=-QX\,dt+\sqrt{2}\,dW\), so the diffusion matrix is the identity and the heat of a precision update \(\Phi\succeq 0\) is \(\operatorname{tr}(\Phi)\). Site-holding tolerance, where a holding bound is stated, is \(\varepsilon=1/18\).

**Blanket.** For a set \(R\), the blanket \(B\) is the set of vertices outside \(R\) with a neighbor in \(R\). The exterior \(E\) is the rest. On this precision, \(Q_{RE}=0\).

**What "holds" means.** A memory channel of a set \(S\) is a Gaussian precision update supported on \(S\). Perfect holding is conditioning on those coordinates. The decision loss on a set is the trace of the posterior covariance on that set, unless a line names one coordinate or one sum.

**Labels are not awarded in this file.** The results note labels each claim after the checks. This file only locks the numbers and the miss rules.

## 2. Closed forms on the path of three

Sites \(0,1,2\). \(R=\{0\}\), \(B=\{1\}\), \(E=\{2\}\).

\[
Q=\begin{pmatrix}2&-1&0\\-1&3&-1\\0&-1&2\end{pmatrix},\qquad
\Sigma=\frac18\begin{pmatrix}5&2&1\\2&4&2\\1&2&5\end{pmatrix}.
\]

**P1, required.**

| Quantity | Locked value |
|---|---|
| \(\operatorname{Var}(X_2\mid X_1)\) | \(1/2\) |
| \(\operatorname{Var}(X_2\mid X_0,X_1)\) | \(1/2\) |
| \(\operatorname{Var}(X_2\mid X_0)\) | \(3/5\) |
| \(\operatorname{Var}(X_0\mid X_1)\) | \(1/2\) |
| \(I(X_0;X_2)\), nats | \(\tfrac12\ln(25/24)\) |
| \(I(X_0;X_2\mid X_1)\) | \(0\) |

Mutual information of two scalars is \(-\tfrac12\ln(1-\rho^2)\).

**P2, required.** Precision \(\varphi\) on site 1 alone gives

\[
\operatorname{Var}(X_2)=\frac{5+2\varphi}{4(2+\varphi)}.
\]

Adding precision \(\psi\) on site 0 gives

\[
\operatorname{Var}(X_2)=\frac{5+2\varphi+3\psi+\psi\varphi}{8+4\varphi+5\psi+2\varphi\psi}.
\]

At \(\varphi=2,\psi=0\) the variance is \(9/16\). At \(\varphi=1,\psi=1\) it is \(11/19\). The gap is \(5/304\), and \(9/16<11/19\). The same trace spent on the blanket leaves a strictly smaller exterior variance than the same trace spent as an interior diagonal.

**P3, required.** The channel with interior diagonal \(0.1\), cross entry \(1\), and blanket diagonal \(10\) has trace \(10.1\), posterior variance of \(X_2\) equal to \(13/25\), and posterior variance of \(X_1\) equal to \(2/25\). The blanket-only channel that matches that blanket variance has trace \(10.5\). The pure-blanket support is therefore not the unique heat minimizer at this target.

The excess trace of the best blanket-supported channel over any channel supported on \(R\cup B\), at the same posterior precision of \(B\), is at most

\[
\operatorname{tr}\bigl(Q_{BI}Q_{II}^{-1}Q_{IB}\bigr)=\tfrac12
\]

on this path. A numerical channel whose excess over the matching blanket channel is larger than \(1/2+10^{-8}\) misses this bound.

## 3. Path of five, local versus pooled

Sites \(0,1,2,3,4\). \(R=\{2\}\), \(B=\{1,3\}\), \(E=\{0,4\}\). Leading principal minors of \(Q\) are \(1,2,5,13,34,55\). For \(i\le j\),

\[
\Sigma_{ij}=d_i\,d_{4-j}/55,
\]

with \(d_0,\ldots,d_4=1,2,5,13,34\).

**P4, required.**

| Quantity | Locked value |
|---|---|
| \(\operatorname{Var}(X_0\mid X_1)\) | \(1/2\) |
| \(\operatorname{Var}(X_0\mid X_1+X_3)\) | \(121/220\) |
| Sum of the two end variances given the two blanket sites, minus the same sum given only the sum of the blanket sites | \(-1/10\) |
| \(\operatorname{Var}(X_2\mid X_1,X_3)\) | \(1/3\) |
| \(\operatorname{tr}(Q_{BI}Q_{II}^{-1}Q_{IB})\) | \(2/3\) |

The sign on the third row is the per-site loss: the pooled sum is worse by \(1/10\). For the sum \(Z=X_0+X_4\), the statistic \(X_1+X_3\) matches conditioning on both blanket sites. The same direction is sufficient for the sum and not sufficient for the two separate ends.

The holding bounds at \(\varepsilon=1/18\) are \(30\) on \(B\) (two sites, each \(Q_{ii}=3\)) and \(15\) on the single interior site.

## 4. Where screening is predicted to fail

**P5, long-range, required.** On the path of three, add \(-\gamma\) in the \((0,2)\) and \((2,0)\) entries and add \(\gamma\) to the two diagonal corners, \(\gamma=1\). Then

\[
I(X_0;X_2\mid X_1)=\tfrac12\ln(9/8),
\]

and the partial correlation is \(1/3\). At \(\gamma=0\) the same conditional information is \(0\). The geometric middle site does not screen a direct edge.

**P6, non-Markov covariance, required.** Three sites, \(\Sigma_{ii}=1\), \(\Sigma_{ij}=1/2\) for \(i\neq j\). Conditional correlation of the ends given the middle is \(1/3\), and the conditional information is \(\tfrac12\ln(9/8)\).

**P7, non-Markov time, required.** \(X_t=\xi_t+\xi_{t-1}\) with the \(\xi\) standard normal and independent, \(t=0,1,2\). Unconditional correlation of \(X_0\) and \(X_2\) is \(0\). Conditional correlation given \(X_1\) is \(-1/3\), and the conditional information is \(\tfrac12\ln(9/8)\).

**P8, finite speed, required.** Present coordinates independent standard normal. One step of range 1:

\[
S_{ij}=\begin{cases}1/2&i=j,\\1/4&|i-j|=1,\\0&\text{otherwise.}\end{cases}
\]

Noise at each step is an independent standard normal vector. The excess conditional variance of site \(0\) at horizon \(H\), from dropping the site at distance \(H\) after conditioning on sites \(0,\ldots,H-1\), is

| \(H\) | Excess | Excess from every site beyond \(H\) |
|---|---|---|
| 1 | \(1/16\) | \(0\) |
| 2 | \(1/256\) | \(0\) |
| 3 | \(1/4096\) | \(0\) |

The thickness equals the horizon. The speed is one site per step, so the thickness equals horizon times speed.

Range 2, self \(1/2\) and weight \(1/6\) at distances 1 and 2. At horizon 1 the coefficient of site 2 is \(1/6\), the excess of dropping it is \(1/36\), and every site beyond distance 2 has coefficient 0. At horizon 2 the coefficient of site 4 is \(1/36\), the excess of dropping it is \(1/1296\), and the thickness is 4, which is horizon times speed with speed 2.

**P9, continuous time, required identities and one tolerance.** On the infinite path, \(p_d(t)=e^{-2t}I_d(2t)\) is the transition kernel of \(e^{-tL}\), and \(\sum_d d^2 p_d(t)=2t\). At \(t=1/2\) and \(t=2\) the second moments are \(1\) and \(4\). The code's series, truncated at distance 40, matches these two moments to absolute error \(10^{-10}\). The regression kernel of \(Q=I+L\) is \(e^{-3\tau}I_d(2\tau)\), which is nonzero at every distance for every \(\tau>0\).

On the finite path of 31 sites, at the center site 15, let \(w\) be row 15 of \(e^{-\tau Q}\) and let

\[
\Delta(r)=\operatorname{Var}(w\cdot X\mid X_{\{|i-15|\le r\}}),
\]

with \(X\) drawn from \(N(0,Q^{-1})\). Then \(\Delta(15)=0\), and \(\Delta(r)>0\) for every \(r<15\), at \(\tau=1/2\) and at \(\tau=1\). Let \(r_{0.05}(\tau)\) be the smallest \(r\) with \(\Delta(r)\le 0.05\,\Delta(0)\). The ratio \(r_{0.05}(1)/r_{0.05}(1/2)\) is the thickening. A square-root reading sits near \(\sqrt{2}\). A linear "horizon times speed" reading sits near \(2\).

**Tolerance, not a required failure.** If the ratio is \(\ge 1.7\) or \(\le 1.05\), that reading is a puzzle. The next test is the same definition on a path of 61 sites, centered, same two times. If either radius equals 15, the path was too short for that time; the same longer path is the next test. The strict positivity \(\Delta(r)>0\) for \(r<15\) is required. A hard cutoff at a finite radius would miss it.

## 5. Gasket and the open square

**Gasket, the construction the code must follow.** \(G_0\) is a triangle. \(G_{g+1}\) is three copies of \(G_g\), with the three pairs of corners identified exactly as in the corner-gluing used for a Sierpiński gasket: copy 0's second corner with copy 1's first, copy 1's third with copy 2's second, copy 2's first with copy 0's third. No other vertices are identified. \(N(g)=\tfrac32(3^g+1)\). Generations \(2,3,4,5\) are required. Generation 6 is not.

One subcopy of \(G_g\), excluding its two glue vertices, is the region \(R\). Those two glue vertices are the blanket \(B\). They have degree 4. \(|B|=2\) at every generation. \(|R|=N(g-1)-2\), so the four sizes are \(4,13,40,121\).

**P10, required.**

| Generation of \(G_g\) | \(\lvert R\rvert\) | Blanket holding bound | Region holding bound |
|---|---|---|---|
| 2 | 4 | 26 | 54 |
| 3 | 13 | 26 | 171 |
| 4 | 40 | 26 | 522 |
| 5 | 121 | 26 | 1575 |

The bounds are \(\sum(1/\varepsilon-Q_{ii})\) at \(\varepsilon=1/18\). Glue vertices contribute \(18-5=13\) each. Inside \(R\), one vertex has degree 2 and the rest have degree 4, so the region bound is \(13\lvert R\rvert+2\).

The conditional covariance of \(E\) given \(B\) equals the conditional covariance given \(R\cup B\), to absolute entrywise error \(10^{-8}\). Every interior variance given \(B\) equals the corresponding diagonal of \(Q_{RR}^{-1}\), to absolute error \(10^{-8}\), and each of those diagonals is at least \(1/5\). Since \(1/5>1/18\), a perfect blanket does not meet the interior tolerance.

**P11, open square, side 8, required.** Columns \(x=0,1,2\) are \(R\) (\(\lvert R\rvert=24\)). Column \(x=3\) is \(B\) (\(\lvert B\rvert=8\)). Columns \(x=4,5,6,7\) are \(E\). The holding bound on \(B\) is \(106\). The holding bound on \(R\) is \(326\). The same conditional-covariance identity as on the gasket is required, and every interior conditional variance given \(B\) is at least \(1/5\).

A uniform diagonal load is computed and printed. It is not a locked digit. It is an achieved cost, above the bound, the same construction as `uniform_diagonal_load` in `theory/holographic_checks/holographic_checks.py`.

## 6. Capacity, ruin, and pooling

The boundary statistic on the path of three is site 1. Its prior variance is \(1/2\). With precision \(\Phi\) on that site,

\[
\operatorname{Var}(X_1\mid\text{channel})=\frac1{2+\Phi},\qquad
\operatorname{Var}(X_2\mid\text{channel})=\frac12+\frac14\cdot\frac1{2+\Phi}.
\]

**P12, required.** The decision tolerance \(\operatorname{Var}(X_2)\le 0.55\) needs \(\Phi\ge 3\). Each unit may install precision at most \(c=1\), pays that precision as heat, and pays upkeep \(1/2\). Units fail independently with probability \(1/5\). The cap is \(P(\operatorname{Var}(X_2)>0.55)\le 0.05\). Stake weight is 1. The cost is heat plus upkeep plus expected decision variance.

A non-pooling copy uses the best survivor. Its best up-state decision variance is \(7/12>0.55\), at every count, so every copy design misses the cap.

A pool adds the survivors' precisions. It needs at least three survivors. At five units the chance of three or more survivors is \(2944/3125=0.94208\), which misses \(0.05\). At six units the chance is \(15360/15625=0.98304\). Six is the smallest count in \(\{1,\ldots,8\}\) that meets the cap. The expected decision variance at six units is \(470459/875000\). Heat plus upkeep is \(9\). The cost is \(8345459/875000\).

This is the capacity-limited pool of the memory note, applied to a one-dimensional blanket statistic. It is not a claim that one global sum of many blanket sites is the right store for a per-site exterior loss. P4 is that distinction: the sum of the two ends is pooled, and the two ends scored separately are not.

## 7. What a miss is

An exact fraction or an exact zero that misses by more than \(10^{-9}\) relative, or \(10^{-8}\) absolute where a line says so, fails the script. Those lines are the algebra. If a locked fraction is the line that is wrong, the results note does not edit this file. It records the returned value, the diagnosis, and the next test, and the claim stays a puzzle until that test is a new preregistration.

The radius ratio in P9 is the only tolerance. A miss there does not fail the script. The positivity of \(\Delta(r)\) does.

The encoding sentence, that the blanket stores the interior, is predicted to miss on P1's interior variance \(1/2\), on P4's interior variance \(1/3\), and on the interior floors \(\ge 1/5\) in P10 and P11. That miss is the converse. It is not a failure of the exterior screening.

The sentence "the heat-minimizing channel is supported on the blanket coordinates alone" is predicted to miss on P3, by the gap \(10.5-10.1=0.4\), inside the cap \(1/2\). The repaired sentence is the one with the trace cap. A channel that beats its matching blanket channel by more than that cap is a puzzle. The next test is to print the Schur complement of that channel and compare it with the formula in the results note.

No line here identifies this graph count with an AdS/CFT dictionary or with a black-hole entropy. Bekenstein 1973 and Hawking 1975 were fetched as titles without abstracts. They are not inputs to a prediction.
