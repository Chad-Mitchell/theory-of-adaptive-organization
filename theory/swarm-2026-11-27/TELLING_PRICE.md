# The telling price for a part with private information

*Friday 27 November 2026 (America/New_York). Part of `theory/swarm-2026-11-27/` (index: `INDEX.md`). Branched from `863a8a8bb3e0bb46c00a9236a9b4d5192c4b9d8d`. Answers the item "a part with private information … the telling price inside this rule (CT16 for a part that tells the whole) is not derived here" (`theory/swarm/SWARM_RULE.md:90` at the branch point). Checks: `checks/swarm27_checks.py`, section B. A self-check, not an independent review.*

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

Labels as in `FOLD_INS.md`.

## 1. The cost, with named terms

**Class (named TP).** CT12's read-rate class at α = 2 (`THEORY.md:336-342`): the whole tracks a drifting target with hold-last-value reads at read rate \(f\), squared-error loss, drift intensity \(q\). The whole's cost per unit time is \(J_W(f;q)=cf+Wq/(2f)\). Part \(i\) pays the share \(s_i\) of each read and bears stake \(w_i\): \(J_i(f;q)=s_icf+w_iq/(2f)\). The whole chooses \(f\). **Only the part knows \(q\)** (it sits close to the driver); the whole has a prior on \(q\) with support \([q_{\text{lo}},q_{\text{hi}}]\), \(0<q_{\text{lo}}<q_{\text{hi}}\), and mean \(M\). The part sends a message; the whole then sets \(f\). Telling costs the whole \(d\) per unit time while the channel is open (the CT16 price, `THEORY.md:366`, in the other direction).

| Term | Meaning | Status |
|---|---|---|
| \(q\) | drift intensity of the target, known to the part only | MEASUREMENT (private) |
| prior on \(q\) | what the whole believes before it is told | MEASUREMENT |
| \(\kappa_i=s_iW/w_i\) | pricing ratio; 1 is clause 4's alignment | MEASUREMENT |
| \(d\) | price of keeping the telling channel open | MEASUREMENT |

The receiver's best response to a belief with mean \(m\) is \(f=\sqrt{Wm/(2c)}\), at cost \(\sqrt{2cWm}\). The part's preferred rate at known \(q\) is \(f_i(q)=\sqrt{w_iq/(2s_ic)}=f_W(q)/\sqrt{\kappa_i}\): **a constant multiplicative bias**, the same for every \(q\). This is Crawford and Sobel's (1982) sender–receiver game with bias set by the pricing ratio.

## 2. Results

**TP1 (aligned part: full revelation; PROVED (in-model)).** If \(\kappa_i=1\), then \(J_i(f;q)=(w_i/W)\,J_W(f;q)\) for every \(f\) and \(q\), so truthful telling followed by \(f=f_W(q)\) is an equilibrium. The whole then opens the channel iff
\[
d<V_{\text{full}}=\sqrt{2cW}\,\bigl(\sqrt{M}-\mathbb E\sqrt q\bigr),
\]
which is positive by Jensen's inequality whenever the prior is not a point mass.

*Proof.* Proportional costs give identical best responses, so no type gains by misreporting. The whole's expected cost without telling is \(\sqrt{2cWM}\) and with truthful telling \(\mathbb E\sqrt{2cWq}\). ∎

**TP2 (misaligned part: no full revelation; PROVED (in-model), an application of Crawford & Sobel 1982, Theorem 1).** If \(\kappa_i\neq1\), no equilibrium is fully revealing, and every equilibrium partitions \([q_{\text{lo}},q_{\text{hi}}]\) into finitely many intervals, each inducing one read rate.

*Proof.* Use the action \(f\) and the type \(q\). Both payoffs \(-J\) are strictly concave in \(f\) and have positive cross-partial in \((f,q)\) (\(\partial^2(-J)/\partial f\,\partial q=w/(2f^2)>0\) for either player's stake), and the two ideal actions differ at every \(q\) because their ratio is \(\sqrt{\kappa_i}\neq1\). These are the conditions of Crawford and Sobel's Theorem 1 (after a monotone relabelling of the type interval to \([0,1]\)), which gives a finite partition. Directly for full revelation: if the whole played \(f_W(q)\) on truthful messages, type \(q\) would report \(q'=q/\kappa_i\), and gain whenever \(q/\kappa_i\) lies in the support (for some interior \(q\) when \(q_{\text{lo}}/q_{\text{hi}}<\kappa_i<q_{\text{hi}}/q_{\text{lo}}\); outside that range Crawford and Sobel's theorem still applies). ∎

**The arbitrage condition.** In an \(N\)-step equilibrium with boundaries \(q_{\text{lo}}=q_0<q_1<\dots<q_N=q_{\text{hi}}\) and conditional means \(m_k=\mathbb E[q\mid q_{k-1}\le q<q_k]\), the receiver plays \(f_k=\sqrt{Wm_k/(2c)}\), and the boundary type is indifferent between \(f_k\) and \(f_{k+1}\): \(s_ic(f_{k+1}-f_k)=(w_iq_k/2)(1/f_k-1/f_{k+1})\), that is \(q_k=2s_icf_kf_{k+1}/w_i\), which is
\[
q_k=\kappa_i\sqrt{m_k\,m_{k+1}}\qquad(k=1,\dots,N-1).
\]
At \(\kappa_i=1\) every boundary is the geometric mean of the neighbouring conditional means.

**TP3 (when telling can carry any information; PROVED (in-model)).** Assume the prior satisfies the **MRR condition**: \(m_L(x)/x\) and \(m_R(x)/x\) are nonincreasing in \(x\), where \(m_L(x)=\mathbb E[q\mid q<x]\) and \(m_R(x)=\mathbb E[q\mid q\ge x]\). Then an informative equilibrium (any \(N\ge2\)) exists **iff**
\[
\sqrt{q_{\text{lo}}/M}<\kappa_i<\sqrt{q_{\text{hi}}/M}.
\]
Outside this window only babbling remains (\(N=1\)) and the telling channel is worth nothing to the whole at any price \(d>0\).

*Proof.* (If.) Let \(\phi(x)=\kappa_i\sqrt{m_L(x)m_R(x)}-x\) on \((q_{\text{lo}},q_{\text{hi}})\). As \(x\downarrow q_{\text{lo}}\), \(m_L\to q_{\text{lo}}\) and \(m_R\to M\), so \(\phi\to\kappa_i\sqrt{q_{\text{lo}}M}-q_{\text{lo}}>0\) iff \(\kappa_i>\sqrt{q_{\text{lo}}/M}\). As \(x\uparrow q_{\text{hi}}\), \(\phi\to\kappa_i\sqrt{Mq_{\text{hi}}}-q_{\text{hi}}<0\) iff \(\kappa_i<\sqrt{q_{\text{hi}}/M}\). \(\phi\) is continuous, so it has a root \(q_1\), and \(\{q_{\text{lo}},q_1,q_{\text{hi}}\}\) satisfies the arbitrage condition. Positive cross-partial makes types below \(q_1\) prefer \(f_1\) and types above prefer \(f_2\), so it is an equilibrium.
(Only if, lower edge.) Let \(\kappa_i\le\sqrt{q_{\text{lo}}/M}\) and suppose an equilibrium with \(N\ge2\) exists. Its first boundary satisfies \(q_1=\kappa_i\sqrt{m_L(q_1)\,m(q_1,q_2)}\le\kappa_i\sqrt{m_L(q_1)m_R(q_1)}\), since truncating from above lowers a mean. With \(m_L(q_1)<q_1\) and, by MRR, \(m_R(q_1)\le q_1M/q_{\text{lo}}\) (the value of \(m_R(x)/x\) at \(x=q_{\text{lo}}\) is \(M/q_{\text{lo}}\)), the right side is strictly below \(\sqrt{(q_{\text{lo}}/M)\,q_1\,q_1M/q_{\text{lo}}}=q_1\). Contradiction.
(Only if, upper edge.) Let \(\kappa_i\ge\sqrt{q_{\text{hi}}/M}\). The last boundary satisfies \(q_{N-1}=\kappa_i\sqrt{m(q_{N-2},q_{N-1})\,m_R(q_{N-1})}\ge\kappa_i\sqrt{m_L(q_{N-1})m_R(q_{N-1})}\), since truncating from below raises a mean. With \(m_R(q_{N-1})>q_{N-1}\) and, by MRR, \(m_L(q_{N-1})\ge q_{N-1}M/q_{\text{hi}}\), the right side is strictly above \(q_{N-1}\). Contradiction. ∎

**The MRR condition holds for the uniform and the log-uniform (scale-free) priors (PROVED).** Uniform: \(m_L(x)/x=\tfrac12+q_{\text{lo}}/(2x)\) and \(m_R(x)/x=\tfrac12+q_{\text{hi}}/(2x)\), both decreasing. Log-uniform: \(m_R(x)/x=(\rho-1)/\ln\rho\) with \(\rho=q_{\text{hi}}/x\), increasing in \(\rho\) because \(\ln\rho>1-1/\rho\); and \(m_L(x)/x=(1-1/\rho)/\ln\rho\) with \(\rho=x/q_{\text{lo}}\), decreasing in \(\rho\) because \(\ln\rho<\rho-1\). Both are therefore nonincreasing in \(x\).

**TP4 (the private-information telling price; PROVED (in-model)).** In any \(N\)-step equilibrium the whole's value of being told is
\[
V_N(\kappa_i)=\sqrt{2cW}\Bigl(\sqrt M-\sum_{k=1}^N P_k\sqrt{m_k}\Bigr)\ \ge 0,
\]
with \(P_k\) the prior mass of step \(k\). The whole opens a telling channel of price \(d\) iff \(d<V^*(\kappa_i)\), the value of the equilibrium it can coordinate on. \(V^*(1)=V_{\text{full}}\); \(V^*(\kappa_i)=0\) outside TP3's window (under MRR). *Proof.* The whole's expected cost on step \(k\) is \(\sqrt{2cWm_k}\); Jensen gives the sign. ∎

So CT16's rule for telling becomes, for a part that tells the whole what only it knows: **tell iff the price of the channel is below the value of the information the part's pricing lets it reveal**. Repricing the part to \(\kappa_i=1\) (clause 4) restores full revelation and the full value; mispricing beyond the window makes the part's reports worthless even when talk is free.

**Worked example (numerical; log-uniform prior on \([1,100]\), \(c=W=1\)).** The window is \(0.2157<\kappa_i<2.1568\) and the value of full revelation is \(V_{\text{full}}=1.02939\) (both by hand from the formulas above). The most informative equilibrium found by shooting at \(\kappa=1.1,1.3,1.6,2.0,2.3\), and its value, are in `checks/swarm27_checks.out` (check `tp_value_falls_with_mispricing`). Monotonicity of \(V^*\) in \(\kappa\) is not derived; the example only illustrates it. *Checks:* `tp_full_revelation_iff_aligned`, `tp_mrr_conditions_hold`, `tp_informative_iff_kappa_window` (three priors, eight \(\kappa\) each, with a brute-force check that every sender type's cheapest induced action is its own step), `tp_value_falls_with_mispricing`.

## 3. Prior art

- Crawford and Sobel 1982, *Econometrica* 50:1431, doi [10.2307/1913390](https://doi.org/10.2307/1913390): partition equilibria, finiteness under a bias (Theorem 1), and full revelation without one. TP2 is an application. Their uniform-quadratic closed forms do not carry over: here the bias is multiplicative and the loss is the CT12 read cost.
- Lindahl 1919 and Samuelson 1954, doi [10.2307/1925895](https://doi.org/10.2307/1925895), for the alignment benchmark \(\kappa=1\), as in clause 4.
- What is new, as far as found in this pass (a short search, not a review): the mapping of the swarm rule's cost share onto a constant Crawford–Sobel bias, the window \(\sqrt{q_{\text{lo}}/M}<\kappa<\sqrt{q_{\text{hi}}/M}\) under MRR, and the telling-price rule TP4.

## 4. Not derived here

- **Other classes.** TP is the α = 2 read-rate class with the part informed about \(q\). For general α the bias is still constant in \(\ln f\) (ratio \(\kappa_i^{-1/\alpha}\), `FOLD_INS.md` F1), so TP2 carries over; TP3's window was derived only at α = 2. The telegraph class of the stay clause, and a part informed about the signal itself rather than its drift, are OPEN.
- **Which equilibrium.** TP4 needs the whole to coordinate on an equilibrium; equilibrium selection is OPEN.
- **Monotonicity of \(V^*\) in \(\kappa\)**: seen in the example, not derived.
- **Misinforming while keeping a private copy** (`theory/swarm/SWARM_RULE.md:84` at the branch point) is this game with an informed part: TP2 says a mispriced part's reports are coarse, not false. Lying with a cost (verifiable or costly messages) is OPEN.
