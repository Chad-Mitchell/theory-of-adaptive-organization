# Couplings beyond the weighted potential class (CX2)

*Friday 27 November 2026 (America/New_York). Part of `theory/swarm-2026-11-27/` (index: `INDEX.md`). Branched from `863a8a8bb3e0bb46c00a9236a9b4d5192c4b9d8d`. CX2 (`THEORY.md:179`, Appendix C `THEORY.md:579`) classifies when self-interested parts reach the joint optimum: (a) potential coupling converges (CT31, `THEORY.md:491`); (b) general convergence is false (CT32, `THEORY.md:493`); still undecided, among others, "which real couplings are potential games". This note adds two classes outside CT31 and the alignment rule that replaces clause 4 in one of them. It does not settle CX2, whose ledger status is open. Checks: `checks/swarm27_checks.py`, section E. A self-check, not an independent review.*

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

Labels as in `FOLD_INS.md`.

## 1. Heterogeneous error curves (class HC)

**Class.** CT31's shared-driver class with one change: party \(i\) bears \(w_ig_i(F)\) with its **own** curve \(g_i\), strictly decreasing and strictly convex, \(F=\sum_jf_j\), and pays \(c_if_i\). (CT31 has one \(g\) for all.) Two parties that watch the same driver but lose differently from the same error, one linearly in staleness and one sharply, are in HC and not in CT31. Let \(\hat F_i\ge0\) solve \(-w_ig_i'(\hat F_i)=c_i\) (\(\hat F_i=0\) if \(-w_ig_i'(0)\le c_i\)): the total party \(i\) would buy alone.

**HC1 (not a weighted potential game; PROVED (in-model)).** If \(g_i''/g_j''\) is not constant in \(F\) for some \(i\neq j\), no weights make HC a weighted potential game.

*Proof.* For twice-differentiable costs a weighted potential with weights \(\omega_i\) exists iff \(\omega_i^{-1}\partial^2J_i/\partial f_i\partial f_j=\omega_j^{-1}\partial^2J_j/\partial f_j\partial f_i\) for all \(i,j\) (Monderer & Shapley 1996, Theorem 4.5, applied to \(J_i/\omega_i\)). Here \(\partial^2J_i/\partial f_i\partial f_j=w_ig_i''(F)\), so the condition is \(g_i''(F)/g_j''(F)=\omega_iw_j/(\omega_jw_i)\) for every \(F\). ∎ *Check:* `hetero_curves_not_weighted_potential` (\(g_1=1/F\), \(g_2=1/F^2\): the square-cycle ratio is not constant in \(F\)).

**HC2 (best-reply equivalent to a convex potential; Nash is unique in total; PROVED (in-model), KNOWN in substance).** Party \(i\)'s best reply is \(BR_i(f_{-i})=\max(0,\hat F_i-F_{-i})\), which is also the best reply of party \(i\) when every party minimizes
\[
\tilde\Phi(f)=\sum_ie^{-\hat F_i}f_i+e^{-F}.
\]
So HC is a best-reply potential game (Voorneveld 2000) with a convex potential. Its Nash equilibria are the minimizers of \(\tilde\Phi\) on \(f\ge0\): the total is \(F=\max_i\hat F_i\), and only parties with \(\hat F_i=\max_j\hat F_j\) read. With a unique largest \(\hat F_i\), the equilibrium is unique.

*Proof.* \(J_i\) is strictly convex in \(f_i\) with stationary point \(F=\hat F_i\); projecting on \(f_i\ge0\) gives \(BR_i\). The same projection is the minimizer of \(e^{-\hat F_i}f_i+e^{-(F_{-i}+f_i)}\) over \(f_i\ge0\). \(\tilde\Phi\) is convex, so Nash points (common fixed points of the \(BR_i\)) are its KKT points: \(f_i>0\Rightarrow F=\hat F_i\), \(f_i=0\Rightarrow F\ge\hat F_i\). Hence \(F\ge\max\hat F_i\), and at least one party reads unless all \(\hat F_i=0\), so \(F=\max\hat F_i\). ∎ This is the private-provision result that only the party with the largest demand gives (Bergstrom, Blume & Varian 1986), and the best-reply potential of aggregative games (Dubey, Haimanko & Zapechelnyuk 2006; Jensen 2010).

**HC3 (round-robin best response converges; PROVED (in-model)).** Sequential best response from any \(f\ge0\) makes the total \(F\) converge to \(\max_i\hat F_i\); with a unique largest \(\hat F_i\), the profile converges to the unique equilibrium.

*Proof.* Each update is an exact coordinate minimization of \(\tilde\Phi\), so \(\tilde\Phi\) is nonincreasing. On the starting level set \(F\le\tilde\Phi(f^0)/\min_ie^{-\hat F_i}\), so the iterates stay in a compact set, on which \(e^{-F}\) has curvature at least \(\mu=e^{-F_{\max}}>0\) along each coordinate. Minimizing a \(\mu\)-strongly convex function of one variable on an interval lowers it by at least \((\mu/2)\Delta^2\), \(\Delta\) the step, so \(\sum\Delta^2<\infty\) and steps vanish. At any cluster point every \(BR_i\) (continuous) is a fixed point, so it is a Nash equilibrium; all of these have \(F=\max\hat F_i\) (HC2), so \(F\) converges, and with a unique argmax there is one cluster point. ∎ (Tseng 2001 gives block-coordinate convergence in general; the argument above is self-contained for this class.) *Check:* `hetero_curves_best_response_converges` (random games with three curve shapes).

**HC4 (alignment: Lindahl shares, not stake shares; PROVED (in-model), KNOWN: Lindahl 1919, Samuelson 1954).** Here the read price is common, \(c_i=c\) for every party (HC1–HC3 allow per-party prices \(c_i\)). Let the parties share the read cost \(cF\) in shares \(s_i\), and let \(F^*\) minimize the joint cost \(cF+\sum_iw_ig_i(F)\), so \(c=-\sum_iw_ig_i'(F^*)\). Every party's preferred total equals \(F^*\) iff
\[
s_i=\frac{-w_ig_i'(F^*)}{c},
\]
and these shares sum to 1. Stake shares \(s_i=w_i/W\) align every party iff \(g_i'(F^*)\) is the same for all \(i\), the case when the curves coincide (the CT31 class, proved-in-model) and not in general.

*Proof.* Party \(i\) minimizes \(s_icF+w_ig_i(F)\), strictly convex, with stationary point where \(s_ic=-w_ig_i'(F)\). Setting \(F=F^*\) gives the shares; summing gives Samuelson's condition. ∎ *Check:* `lindahl_shares_align_hetero` (\(w=(1,2)\), \(g_1=1/F\), \(g_2=1/F^2\)).

**Consequence for clause 4.** Clause 4 (`theory/swarm/SWARM_RULE.md`, clause 4) is the equal-curve case of HC4. With heterogeneous curves the aligning share is the party's marginal loss at the joint optimum, not its stake; that needs \(g_i'(F^*)\), which is private, so the revelation problem of `STAKES.md` reappears with marginal losses in place of stakes.

## 2. Credibility coupling (class CR)

**Class.** Parts couple through the signal's worth rather than through a shared read total: the more parts follow (and so deposit into or check the shared signal), the more informative it is. Part \(i\) follows iff \(\lambda s_ic<w_i\Phi(n_{-i})\), where \(n_{-i}\) is the number of other followers and \(\Phi\) is nondecreasing (the stay clause with \(\Phi\) depending on the others). This is not CT31's aggregative shared-driver form.

**CR1 (extremal equilibria and convergence from the extremes; PROVED (in-model), KNOWN in form: Topkis 1979, Milgrom & Roberts 1990, Vives 1990, from Tarski 1955).** The game has strategic complements on \(\{0,1\}^N\), so a largest and a smallest pure equilibrium exist. Simultaneous or round-robin best response from all-follow decreases monotonically to the largest, and from all-leave increases monotonically to the smallest, within \(N\) rounds.

*Proof.* Each best reply is a nondecreasing function of the others' profile, so the best-reply map is monotone on a finite lattice; Tarski's theorem gives the extremal fixed points. Starting from the top, the map's iterates are nonincreasing and stay above every fixed point, so they stop at the largest one; each coordinate changes at most once. Symmetrically from the bottom. ∎

**CR2 (hysteresis for identical parts; PROVED (in-model)).** With identical parts and \(\Phi(n)=\Phi_0+\Phi_1n/(N-1)\), all-follow and all-leave are both equilibria iff \(w\Phi_0\le\lambda sc<w(\Phi_0+\Phi_1)\). As the signal's rate \(\lambda\) rises past \(w(\Phi_0+\Phi_1)/(sc)\) the following swarm collapses, and it reforms only when \(\lambda\) falls below \(w\Phi_0/(sc)\). *Proof.* All-follow is an equilibrium iff \(\lambda sc<w\Phi(N-1)\); all-leave iff \(\lambda sc\ge w\Phi(0)\). ∎ This is Granovetter's (1978) threshold model with the stay index as the threshold. *Check:* `credibility_coupling_extremal_equilibria` (all profiles enumerated in random games, \(N\le8\); the window at \(\Phi_0=0.1\), \(\Phi_1=0.15\)).

**Reading.** Where credibility couples the parts, the swarm rule's stay condition has two stable answers over a band of \(\lambda\): which one holds depends on history. A whole that wants the following equilibrium should start from many followers (subsidize following until the largest equilibrium is reached), which is clause 5's subsidy lever used once rather than forever.

## 3. Prior art (all DOIs checked on Crossref, `checks/crossref.out`)

Monderer & Shapley 1996, doi [10.1006/game.1996.0044](https://doi.org/10.1006/game.1996.0044); Voorneveld 2000, doi [10.1016/S0165-1765(99)00196-2](https://doi.org/10.1016/S0165-1765(99)00196-2); Dubey, Haimanko & Zapechelnyuk 2006, doi [10.1016/j.geb.2004.10.007](https://doi.org/10.1016/j.geb.2004.10.007); Jensen 2010 (online 2008), doi [10.1007/s00199-008-0419-8](https://doi.org/10.1007/s00199-008-0419-8); Bergstrom, Blume & Varian 1986, doi [10.1016/0047-2727(86)90024-1](https://doi.org/10.1016/0047-2727(86)90024-1); Samuelson 1954, doi [10.2307/1925895](https://doi.org/10.2307/1925895); Tseng 2001, doi [10.1023/A:1017501703105](https://doi.org/10.1023/A:1017501703105); Topkis 1979, doi [10.1137/0317054](https://doi.org/10.1137/0317054); Milgrom & Roberts 1990, doi [10.2307/2938316](https://doi.org/10.2307/2938316); Vives 1990, doi [10.1016/0304-4068(90)90005-T](https://doi.org/10.1016/0304-4068(90)90005-T); Tarski 1955, doi [10.2140/pjm.1955.5.285](https://doi.org/10.2140/pjm.1955.5.285); Granovetter 1978, doi [10.1086/226707](https://doi.org/10.1086/226707); Rosen 1965, doi [10.2307/1911749](https://doi.org/10.2307/1911749) (uniqueness under diagonal strict convexity, a route not used here). HC and CR are these known results placed in the swarm rule; the new content is the identification of the classes and HC4's consequence for clause 4.

## 4. Not settled in CX2

- **General coupling.** CT32's counterexamples stand; no theorem covers arbitrary coupling. CX2's ledger status is unchanged (open).
- **Which real couplings are in which class** (CT31, HC, CR, or none) is an empirical question, unchanged.
- **Stochastic and non-aggregative coupling**, and coupling through both the read total and the signal's worth at once, are OPEN.
- **CR's selection between equilibria** under noise (stochastic stability, Young 1993) is not worked out here.
