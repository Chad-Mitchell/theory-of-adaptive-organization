# Is there a holographic structure in the cost of judgment?

*Sunday 22 November 2026. Draft. A self-check, not an independent review. The hypothesis sentence is unchanged. The master equation in THEORY is unchanged. No locked preregistration file is edited. Checks: `theory/holographic_checks/holographic_checks.py`, run at `nice -n 19` (142 checks, FAILS 0). DOIs resolved on the Crossref API on 22 November 2026, and the abstracts used below, are listed in `theory/holographic_checks/crossref.out`.*

Labels: **PROVED** (a proof is on this page, in the class named with it, and the arithmetic is in the checks), **KNOWN** (published, fetched this session, not claimed here), **FAILS** (a counterexample is on this page), **METAPHOR** (the reading adds no prediction the cost equation does not already make). Nothing here is a conjecture. GTAO is the theory in this repository.

The sentence of the hypothesis is unchanged, byte for byte:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

## 0. The answer

No non-metaphorical holographic structure shows up in the physics-derived cost, inside the class already proved.

What holds is narrower than a holographic principle. The memory-bath heat is bounded by \(kT\) times the learning rate, and that rate is the information flow of the signal current across the cut between world and memory. At a fixed decision error the floor depends on that conditional law and on the signal. It does not depend on extra equilibrium coordinates that leave the conditional unchanged. That is the cost equation. It does not encode a bulk on a boundary, and it does not cap how much irrelevant state the memory may carry.

What does not hold:

- At fixed per-site error, on a lattice of equilibrium Ornstein–Uhlenbeck modes, the minimum heat scales with the volume. The exponent in the volume is \(1\), not the area exponent.
- A memory that sees only a surface cannot hold a fixed per-site gap once the cube is large. The variance it can remove is at most \((\text{surface size})/\alpha\).
- The geometric ladder plus the rank-one sum-loss memory is not a renormalization-group layering. The heat added per octave grows by the scale factor. On a sum loss the optimal memory has one coordinate at every stake.

Where a holographic reading predicts a number the cost equation does not — area scaling of that heat, a cap on bulk memory, an equal cost per layer, a layered reconstruction of the bulk — the check does not support it. Where the two readings agree, the number was already the cost equation, and the holographic name is a metaphor.

## 1. Already in the repository

None of the following is a result of this note.

- The heat floor itself. For one exogenous equilibrium Ornstein–Uhlenbeck signal and a mean-squared decision loss, the infimum of the memory-bath heat is \(kT\,a(v-\varepsilon)/\varepsilon\) (`theory/INFO_PHYSICS_ATTAINABILITY.md`, IP11). For independent modes it is the sum of those rates, and on a sum loss it is \(kT\mu\) with gains \(1/(a_k+\mu)\) (`theory/INFO_PHYSICS_GENERAL.md`, IP12, IP13). The geometric count \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\) is IP12. The factor \(K\) for identical modes remembered separately is IP13.
- The shape \(\dot Q\ge kT\) times the learning rate is Horowitz and Esposito. The factor \(2\) for a state that keeps the path is Hartich, Barato, and Seifert. The raw-coordinate gap \(kT a\) is the centered spring scored by \(\mathbb{E}[(M-X)^2]\). The telegraph ray, heat unbounded at fixed stock, is INFO_PHYSICS §4.
- Earlier holographic checks in this repository were about layer counts in Model S, not about this heat. The keystone run at \(N=0.05\) scored \(3/24\) on \(K^*=J\) and failed the equal-value check (CVs \(0.996\)–\(1.984\)); that writeup says it does not test a spatial MERA picture (`core/KEYSTONE_NOTE.md` §5). T20 is **NOT SUPPORTED**: (A) passed with the world's scale range held fixed, (B) failed (`reviews/t20_2026-11-20/REVIEW.md`). `theory/REVEALED_PRICES_2026-11-21.md` §5 already says the CT34 recursion is an analogy to holography, not a physical claim. `theory/SCALE_ENDS.md` and `theory/WORMHOLES.md` use the holographic bound as a capacity cap that does not bind a design.
- Draft PR #182, branch `general-form-physics-2026-11-22`, is a consolidation of the same heat floor. It is open and under fix. This note does not edit that branch and does not use its OPEN_WORK id.

## 2. Boundary and bulk

**Class.** A-X, A-E, A-R, A-L of the attainability note: an exogenous equilibrium Ornstein–Uhlenbeck signal, a regular conditional, and a mean-squared error of an action of the current memory state. The vector form is G-X through G-L, restricted to \(D\) a multiple of the identity when a lattice is diagonalized below. The signal bath's medium heat is zero. A memory that moves \(X\) is outside.

**Proposition H-iface (PROVED, in that class).** The learning rate depends on the memory only through the conditional law of \(X\) given the memory state.

The identity in the attainability note is \(L=a(v\,\mathbb{E}[F(X\mid M)]-1)\), with \(F\) the Fisher information of \(p(x\mid m)\). An added coordinate \(Z\) that is independent of \(X\) given \(M\) does not change \(p(x\mid m,z)\). The marginal entropy of the memory does not appear. Horowitz and Esposito identify this \(L\), in steady state, with the information flow of the signal current across the cut. The mutual-information stock is constant, so the memory's transitions supply \(L\), but the lower bound is the flow.

**Proposition H-floor (already IP11; the independence is the reading).** The infimum of the memory-bath heat at decision error \(\varepsilon\in(0,v)\) is \(kT\,a(v-\varepsilon)/\varepsilon\). It is a function of the signal \((a,v)\) and of \(\varepsilon\). For a Gaussian conditional with that variance, \(\varepsilon=v\,e^{-2I}\) with \(I=I(M;X)=\tfrac12\log(v/\varepsilon)\), so the same floor is \(kT\,a(e^{2I}-1)\). The relevant mutual information of the present is in the floor. The irrelevant bulk is not.

**Check, irrelevant bulk.** An equilibrium coordinate \(dZ=-\lambda Z\,dt+\sqrt{2\lambda\,\mathrm{Var}}\,dB\) has Sekimoto heat \(0\) at every variance, by the cancellation already in INFO_PHYSICS. Its differential entropy \(\tfrac12\log(2\pi e\,\mathrm{Var})\) at variance \(10^{6}\) exceeds the entropy at variance \(1\) by \(\tfrac12\log(10^{6})=6.907755\). The decision error and \(L\) are unchanged if the action ignores \(Z\).

**Where "independent of the stored state" does not hold.**

1. **Path-keeping. FAILS** as a claim that the paid heat ignores the bulk. A state that is a sufficient statistic of the path has sensory capacity \(1\), and Hartich, Barato, and Seifert put the heat at least at twice the learning rate. Recomputed on their locus: memory rate \(9\), noise \(B=\nu^{2}/(\nu^{2}-1)\), conditional error \(0.200000000000\), learning rate \(4\), heat \(8\). The fast shrunk spring at the same conditional error has heat \(4.000020000100\) and the same Gaussian stock \(I=0.804718956217\). Same stock of the present, twice the heat. The decision loss does not ask for capacity \(1\). The attaining design has path rate \(999.503125\) and capacity \(0.004002\), so the path rate is \(249.874532\) times the heat. The interface flow does not cap the path information.

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

**Sweep, exact floor.** Eighteen cells, \(d\in\{1,2,3\}\), \(\alpha\in\{0.3,1,3\}\), \(\beta\in\{0.25,1\}\), \(\varepsilon\) half the smallest prior variance, sizes up to \(n=256\) (\(d=1\)), \(32\) (\(d=2\)), and \(16\) (\(d=3\)). Every volume slope is \(1.000000000000\). The ordinary-least-squares standard errors are at most \(8.1\times 10^{-16}\). The standard deviation of the eighteen slopes is \(1.6\times 10^{-16}\). Every \(d=2\) cross-section slope is \(2.000000000000\), and every \(d=3\) cross-section slope is \(1.500000000000\), with standard errors at most \(1.4\times 10^{-15}\).

**Half the prior mean, water-fill.** Modes whose prior variance lies below the water level stay blind. The heat is still extensive. At \(\alpha=\beta=1\):

| \(d\) | slope in \(\log V\) | standard error | sizes |
|---|---|---|---|
| 1 | \(1.000676\) | \(3.76\times 10^{-4}\) | 6 |
| 2 | \(1.016876\) | \(8.07\times 10^{-3}\) | 7 |
| 3 | \(1.011036\) | \(4.46\times 10^{-3}\) | 6 |

The tracked fraction stays a positive density (at least \(0.63\) on these grids). A fixed fraction of the prior mean does not collapse onto a surface.

**One global mode. PROVED, exponent \(0\).** The normalized zero mode has rate \(\alpha\) and variance \(1/\alpha\). Its heat at modal error \(s\) is \((1-\alpha s)/s\), with no \(V\) in it. At \(s=1/(2\alpha)\) the heat is \(1\) at every volume. The slope against \(\log V\) is \(0\), standard error \(0\), five sizes. An area exponent \(d-1\) would grow. This observable does not.

**Disordered mass. PROVED, exponent \(1\).** On-site masses of mean \(1\), periodic \(d=2\), \(\beta=1\), and one fixed \(\varepsilon=0.5/9.5\) below every prior in the draw. The floor is \(V/\varepsilon-\operatorname{tr}(Q)\), and \(\operatorname{tr}(Q)=\sum\alpha_i+4V\). The heat per site is \(14\) at every size from \(n=4\) to \(n=16\). The slope is \(1.000000000000\), standard error \(8.5\times 10^{-16}\). Spatial disorder of the mass does not turn the floor into an area.

**Proposition H-surface (PROVED).** Let a memory's observation be any coordinate set \(B\) of size \(A\), and let \(Q\succeq\alpha I\). Perfect observation of \(B\) removes at most \(A/\alpha\) from the total variance \(\operatorname{tr}(\Sigma)\). A noisy observation removes less.

*Proof.* \(\Sigma=Q^{-1}\preceq\alpha^{-1}I\), so \(\Sigma^{2}\preceq\alpha^{-1}\Sigma\). The removed variance is \(\operatorname{tr}\big((H\Sigma H^{\top})^{-1}H\Sigma^{2}H^{\top}\big)\). The congruence \(H\Sigma^{2}H^{\top}\preceq\alpha^{-1}H\Sigma H^{\top}\) gives the trace at most \(A/\alpha\). ∎

A per-site gap \(\delta>0\) needs a removal of at least \(\delta V\). A surface has \(V/A\to\infty\), so past a finite size the cap lies below the gap. For a \(10\%\) cut of the total variance the bound first fails the surface at \(n=44\) in \(d=1\) (\(\alpha=\beta=1\), cap \(2\), need \(2.0077\)), at \(n=156\) in \(d=2\) (cap \(620\), need \(622.92\), \(V=24336\)), and at \(n=212\) in \(d=3\) with \(\beta=0.5\) (cap \(267128\), need \(269747.52\), \(V=9528128\)). The cap is sufficient. The realized removal is smaller: four random subsets in the checks sit strictly under the cap.

**Open cubes, the removal that is actually achieved.** Perfect observation of the geometric surface, conditional covariance of the interior equal to the interior precision block.

- In \(d=1\), \(\alpha=\beta=1\), the removed variance is \(1.447214\) at every length from \(16\) to \(192\). The slope against \(\log V\) is \(0\) within \(4\times 10^{-13}\). The per-site gap has slope \(-1.000000000000\), standard error \(3.9\times 10^{-13}\). The fractional gap falls from \(0.1915\) to \(0.0168\).
- In \(d=2\), \(n=8\) to \(24\), the removal against the surface size has slope \(0.979510\), standard error \(1.98\times 10^{-3}\). The fractional gap falls from \(0.5403\) to \(0.2122\).
- In \(d=3\), \(\beta=0.5\), \(n=4\) to \(10\), the removal against the surface size has slope \(0.963462\), standard error \(4.38\times 10^{-3}\). The fractional gap falls from \(0.9084\) to \(0.5430\). The surface is still half the cube at \(n=10\) (\(A/V=0.488\)), which is why the fraction is still large. The cap above is what carries the large-\(n\) statement.

**Open-cube bulk floor.** With one fixed \(\varepsilon\), the heat splits exactly into a volume piece and a surface piece,

\[
\dot Q=\;V\Big(\frac1\varepsilon-\alpha-2d\beta\Big)+2d\beta\,\frac{V}{n}.
\]

The second piece is the missing degree on the boundary. Its share of the heat falls with \(n\): from \(0.0175\) to \(0.0011\) in \(d=1\), from \(0.0371\) to \(0.0096\) in \(d=2\), and from \(0.0747\) to \(0.0262\) in \(d=3\). Ordinary-least-squares slopes on these short cubes sit slightly below \(1\) because that share is shrinking: \(0.994254\pm 0.001269\) (\(d=1\)), \(0.989972\pm 0.001163\) (\(d=2\)), \(0.984548\pm 0.001792\) (\(d=3\)). The leading term is the volume.

**The field's own mutual information is a different quantity. KNOWN, and the heat does not follow it.** Wolf, Verstraete, Hastings, and Cirac state that the information in part of a thermal system scales with the area of the cut. On this Gaussian field the check is numerical, not a new theorem. In \(d=1\), \(I(\text{half};\text{half})\) is \(0.157705\) from \(n=16\) through \(n=96\). In \(d=2\), \(I\) against the cut length \(2n\) has slope \(0.922298\), standard error \(0.02994\), six sizes, and \(I/\text{cut}\) has settled at \(0.032174\). On those same lattices the per-site heat against linear size has slope \(2.000000000000\), standard error \(5.6\times 10^{-16}\). The field's mutual information tracks the cut. The heat of holding every site tracks the volume.

**Holographic reading. FAILS.** The reading that says the minimum heat at fixed per-site error scales with the boundary is the volume exponent above. The reading that says a surface memory can hold the bulk error at an area cost is the cap \(A/\alpha\). The area scaling that does occur — the learning rate of a channel that reads \(A\) sites in noise \(\sigma^{2}\) is \(A/\sigma^{2}\), and the variance such a channel can remove is \(O(A)\) — is the cost equation applied to the sites that are actually read. **METAPHOR** if that channel is called holographic.

## 4. The ladder and MERA

Vidal's entanglement renormalization coarse-grains a block after a transformation that reduces its entanglement, and the multi-scale entanglement renormalization ansatz is a circuit of logarithmic depth with a causal structure. Evenbly and Vidal insert disentanglers and isometries and recover scale invariance at a critical point. Swingle reads that scale organization as a discrete geometry, anti-de Sitter at a critical point. Nishioka reviews entanglement entropy, holography, and the renormalization group as one subject. None of those papers is a heat floor for a memory.

**What matches a formula already proved. METAPHOR if it is called a layer of MERA.**

- On the infinite equal-variance ladder, \(w(\rho\mu)=\rho\,w(\mu)\). That is G-scale. Recomputed on a truncation \(k\in[-80,80]\) at \((\rho,\mu)=(2,4)\) and \((10,10)\): each of four successive stake ratios equals \(\rho\) to the printed \(10^{-12}\).
- The per-mode tracked count is \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\) once the slowest mode pays. That is IP12. A MERA depth is also a logarithm of a scale range. The count was not produced by a coarse-graining map.

**What does not match.**

**Proposition H-octave (PROVED, from G-scale).** On the sum loss the heat is \(kT\mu\). Passing to the next octave, \(\mu\to\rho\mu\), adds heat \(kT\mu(\rho-1)\). The next octave adds \(\rho\) times that increment. The increment is not constant.

Checked at both \(\rho=2\) and \(\rho=10\): three successive increment ratios equal \(\rho\).

**Proposition H-share (PROVED, algebra on the sum-loss gains).** The modal share of the learning rate is \(a_k v/(a_k+\mu)^{2}\). At \(a=\mu\) and at \(a=\mu\rho^{2}\),

\[
\frac{\mathrm{share}(\mu)}{\mathrm{share}(\mu\rho^{2})}=\frac{(\rho^{2}+1)^{2}}{4\rho^{2}}.
\]

This equals \(1.562500\) at \(\rho=2\) and \(25.502500\) at \(\rho=10\). A flat cost per octave would give \(1\). The checks match both numbers.

**Per-mode heats are not equal either.** At the stake where mode \(K=10\) of a ladder \(a\rho^{k-1}\) with \(\rho=2\) is just at threshold, the heat of mode \(j<K\) is \(a\rho^{j-1}(\rho^{(K-j)/2}-1)\). The smallest is \(21.627417\) and the largest is \(128\). The ratio is \(5.918414\).

**The sum-loss memory does not add a layer per octave. FAILS** as a MERA depth. IP13 already says the heat-optimal memory on the sum loss has one coordinate. A depth that counted octaves would be \(2\), \(4\), and \(8\) at \(K=2,4,8\) modes. The degree stays \(1\). There is no disentangler, no isometry, and no causal cone. The gain \(g_k=1/(a_k+\mu)\) is one linear functional of every mode.

Stoudenmire's multi-scale tensor network, and the Glasser, Pancotti, and Cirac generalized tensor networks, are classifiers trained on data. The abstracts describe coarse-graining and supervised training. They do not give a bath heat, and this note does not import one.

## 5. The metaphor check

For each correspondence, the question is whether the holographic reading predicts a measurement the cost equation does not.

| Correspondence | Extra prediction | Cost equation | Label |
|---|---|---|---|
| The floor is the interface flow | none: this is Horowitz–Esposito plus IP11 | the same floor | **METAPHOR** as a name; the floor statement is **PROVED** |
| Bulk degrees of freedom are bounded by that flow | a cap on equilibrium bulk entropy, or on the path rate | entropy of an equilibrium coordinate is free at heat \(0\); path rate \(999.503\) at heat \(4.000020\) | **FAILS** |
| Minimum heat at fixed per-site error scales with area | exponent \(1\) in the surface size | exponent \(1\) in the volume, \(d/(d-1)\) in the cross-section | **FAILS** |
| A surface memory holds the bulk error at an area cost | per-site gap stays fixed as \(V\) grows | removal at most \(A/\alpha\); the gap falls | **FAILS** |
| The learning rate of a boundary channel scales with the number of sites read | none | \(A/\sigma^{2}\) | **METAPHOR** |
| The field's mutual information scales with the cut | this is Wolf, Verstraete, Hastings, and Cirac, about the field | the heat on the same lattices scales with volume | **KNOWN** for the field; **METAPHOR** if read as the cost |
| Equal heat per octave | increment independent of the octave | increment scales by \(\rho\) | **FAILS** |
| MERA depth equals the octave count, as a memory degree | degree grows as \(\log(w)\) | sum-loss degree is \(1\); the half-tracked count is already G-scale | degree claim **FAILS**; the count is **METAPHOR** |

No row is a holographic prediction that is both extra and true.

## 6. What this note does not do

It does not edit `THEORY.md`, `CORE.md`, or `README.md`. It does not adopt \(J_{\mathrm{phys}}\) into the master equation. It does not close IP14, and it does not treat a diffusion whose noise does not share the eigenbasis of \(\Sigma\). It does not give an equilibrium floor for a massless field on the torus: \(\alpha>0\) is what keeps the variance finite, and \(\alpha\to 0\) leaves G-E. It does not rerun T20 or the keystone holographic check. Ruin, linking, the stake \(w\), and H3 stay where the heat notes left them.

## 7. Checks

`theory/holographic_checks/holographic_checks.py`. 142 checks, FAILS 0. The numbers in §§2–4 are the numbers it prints.

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
