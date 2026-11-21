# Does GTAO layer count map onto rate-distortion reverse water-filling?

*20 November 2026, first written about 9:55 PM ET (America/New_York), before any confirmation run of the water-filling layer-count rule. Beside a read-only clone of `main` at `8537f39`. Workdir: `/workspace/gtao-wf`. This note is the math; the locked test is `PREREG.md`; results go in `RESULTS.md`. Nothing here is a field claim, and nothing is marked PROVED unless it is actually proved.*

**Question.** Does GTAO's layer-count problem — cost \(J=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb E[\ell]+\cdots\), stakes \(R=w E_\infty/h\), Model S as a sum of OU modes, and rhythmic worlds where N60's increment formula fails (e.g. two oscillators at \(R=3\), argmin \(3\)) — map onto rate-distortion reverse water-filling for Gaussian processes (Kolmogorov 1956; Berger 1971; Sims 2003)?

**Short answer.** The mapping holds for one term in \(J\) and fails for the term the keystone actually uses, unless it is rewritten. Reverse water-filling is the right allocation when the holding cost is a *price per nat* (\(\kappa I_{\mathrm{mem}}\)). That case is already in the theory (P3; `theory/INTERNAL_MODEL.md`). The keystone counts *states* (McMillan degree \(K\)), paying a fixed upkeep \(h\) per layer. That is a different regularizer. Identifying \(K^*\) with the number of frequency-axis peaks of \(S(\omega)\) above a water level is false already in Model S, where the keystone works: every OU mode is a Lorentzian peaked at \(\omega=0\), so the set \(\{S>\theta\}\) is a single interval, while \(K^*\) can be as large as the number of scales. Isolated per-mode water-filling is the same idea as IMP-N60, which already failed because isolated values are not joint increments. What remains, and is tested in `PREREG.md`, is a discrete water-filling on the *joint Kalman–Bucy estimate's* Hankel / \(H_2\) state energies, computed from the unique full-order filter (innovations form). That is the natural translation of reverse water-filling from a Shannon rate to a state *count*. It is a hypothesis, not a theorem. The rule does not predict that reduced-order store rates sit on the world's process bands: in this linear-Gaussian class they sit on the fast, observer-pole side (Kalman–Bucy shift \(b^*=\sqrt{a^2+2av/N}\) on one OU; a related fair fractal test, not used for confirmation here, found the same placement fail).

---

## 1. Two holding costs that are easy to confuse

GTAO's objective (CORE.md, THEORY) is

\[
J(\mathcal D)=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb E[\ell_{\mathcal D}]+A(\mathcal D)+L(\mathcal D)
\quad\text{subject to}\quad P(\mathrm{ruin})\le\varepsilon.
\]

- \(\kappa I_{\mathrm{mem}}\) prices *nats held* per unit time.
- \(hK\) prices *upkeep per layer*, a layer being a tracking store (a state, not an org-chart level).
- The keystone and N60 drop \(A\), \(L\), the ruin cap, and \(\kappa I_{\mathrm{mem}}\), and study

\[
J_K=hK+w E_K,\qquad
\varepsilon_K=E_K/E_\infty-1,\qquad
R=w E_\infty/h,\qquad
K^*=\arg\min_K\bigl[K+R(1+\varepsilon_K)\bigr],
\]

with \(K=0\) allowed (act blind, \(E_0=\mathrm{Var}(s)\)). If \(\varepsilon_K\) is convex, this is the increment test N60: add a layer iff its joint decrement beats \(1/R\). In Model S that count is numerically exact, once started from \(K=0\). With rhythms and first-order real stores it is false (two oscillators, \(R=3\): argmin \(3\), formula \(2\); `core/KEYSTONE_NOTE.md`).

Rate-distortion reverse water-filling is derived from a *linear price on mutual information* (or on Shannon rate), i.e. from a Lagrangian of the form \(w D+\kappa R(D)\). That matches \(\kappa I_{\mathrm{mem}}+w\mathbb E[\ell]\). It does not, by itself, match \(hK+w E_K\).

The rest of the note treats the two cases separately, then lists the breaks.

---

## 2. Reverse water-filling, as Kolmogorov and Berger stated it

Let \(s(t)\) be a zero-mean stationary Gaussian process with two-sided power spectral density \(S(\omega)\), normalised so that \(\mathrm{Var}(s)=(1/2\pi)\int S(\omega)\,d\omega\). For mean-square distortion, the *noncausal* rate-distortion function (Kolmogorov 1956; the standard book treatment is Berger 1971, ch. 4) is given parametrically by reverse water-filling at a water level \(\theta>0\):

\[
D(\theta)=\frac{1}{2\pi}\int_{-\infty}^{\infty}\min\bigl(\theta,\,S(\omega)\bigr)\,d\omega,
\qquad
R(\theta)=\frac{1}{4\pi}\int_{-\infty}^{\infty}\max\bigl(0,\,\log\tfrac{S(\omega)}{\theta}\bigr)\,d\omega
\]

(in nats per unit time). Frequencies with \(S(\omega)\le\theta\) are not encoded: their contribution to distortion is the whole of \(S(\omega)\). Frequencies with \(S(\omega)>\theta\) are encoded down to residual \(\theta\), at rate \(\tfrac12\log(S/\theta)\) (per radian, with the \(1/2\pi\) factor). The Lagrangian \(\min(w D+\kappa R)\) chooses \(\theta\) proportional to \(\kappa/w\) (the constant depends on nats-versus-bits and on one-sided versus two-sided conventions). The same allocation, for a Gaussian vector with eigenvalues \(\lambda_i\), is the discrete rule: spend rate on coordinate \(i\) iff \(\lambda_i>\theta\). That is the form Sims (2003) uses as rational inattention, and the form already used in GTAO for *model size* (P3; INTERNAL_MODEL §5: water level \(\theta=\kappa/(2\ln 2\cdot w)\), \(n^*=\theta^{-1/\beta}\)).

This is exact for Gaussian sources with MSE loss (and is the worst-case allocation among sources with a given spectrum). It is a statement about *rate*, not about the McMillan degree of a filter.

---

## 3. Case A: the cost is \(\kappa I_{\mathrm{mem}}+w D\)

### 3.1 Noncausal, no observation noise

The optimal allocation *is* reverse water-filling. This is Kolmogorov–Berger, and it is already credited in the theory. The scalar Gaussian closed form in P3,

\[
I^*=\tfrac12\log_2\bigl(2\ln 2\cdot a^2\cdot\mathrm{Var}/\kappa\bigr)
\]

when the first nat pays, is the one-mode case of the same formula. Mapping holds. It is not new.

### 3.2 Observation noise, still noncausal

If \(s\) is seen in additive independent Gaussian noise of two-sided density \(N\), the noncausal Wiener error is

\[
E_{\mathrm{nc}}=\frac{1}{2\pi}\int\frac{S(\omega)\,N}{S(\omega)+N}\,d\omega.
\]

A further information constraint on the estimate is equivalent to raising the noise floor, or to water-filling \(S\) against a level \(\theta\ge N\). Still water-filling, still a rate, still not a layer count.

### 3.3 Causality, the first real break

GTAO requires a *causal* estimate: the system must act ahead of a world it does not control. The causal MMSE in white observation noise is the Yovits–Jackson / Kalman–Bucy value used throughout the repo,

\[
E_\infty=\frac{N}{\pi}\int_0^{\infty}\log\bigl(1+S(\omega)/N\bigr)\,d\omega,
\]

which equals \(CPC^\top\) for the Kalman–Bucy error covariance \(P\). This is not the noncausal integral of \(\min(\theta,S)\) or of \(SN/(S+N)\).

The *causal* (sequential, directed-information) rate-distortion function for Gaussian processes is a different object (Tatikonda & Mitter 2004; Tanaka, Kim, Parrilo & Mitter 2017). For Gauss–Markov sources the optimum is a Kalman-like filter plus a Gaussian test channel on the innovations. There is a water-filling-like allocation, but it is over the eigenvalues of a Riccati / state-covariance object, not over \(\{S(\omega)>\theta\}\) in the Kolmogorov sense. Using noncausal water-filling on \(S(\omega)\) as if it were the causal problem is an approximation, and can be wrong about which bands are worth paying for when phase / lead time matters.

So even for the \(\kappa I_{\mathrm{mem}}\) term, the mapping to *Kolmogorov's* frequency-axis formula already breaks under GTAO's causality constraint. A causal version of the mapping can still hold, in the sequential-RD sense, for *rate*, not for \(K\).

---

## 4. Case B: the cost is \(hK+w E_K\) (the keystone)

Here \(K\) is the state dimension of a causal linear filter (degree of a rational transfer function). \(E_K\) is the least MSE in that class. This is model-order selection, not a Shannon-rate constraint.

### 4.1 Why frequency-axis peak counting fails in Model S

Model S has spectrum

\[
S(\omega)=\sum_{j=1}^J\frac{2 a_j v_j}{a_j^2+\omega^2},
\]

a sum of Lorentzians *all peaked at \(\omega=0\)*. For any water level \(\theta\), the set \(\{\omega:S(\omega)>\theta\}\) is a single interval \([-W,W]\) (or empty). The number of frequency-axis peaks above water is \(0\) or \(1\). Theorem L2 / N60 say that well-separated scales can each pay for a layer, and \(K^*\) can equal \(J\). A random walk (one Lorentzian in the \(a\to 0\) limit, textbook \(1/f^2\)) needs at most one layer (L1, CT21). A continuum of scales can need many (L3). The thing that counts layers is *scale bands* (poles on the real axis), not the number of bumps of \(S(\omega)\) on the frequency axis.

A second, independent break, which is the rhythm problem in these units: Shannon rate cares about *bandwidth × log height*. A lightly damped oscillator is a narrow peak at \(\pm\Omega\). It can be cheap in rate and still cost *two states*. A broad OU mode can be expensive in rate and cost *one* state. Ranking bands by Kolmogorov rate is not ranking them by degree. The pair-rule rescue ("a rhythm is two layers, so \(K^*\) is even") was already false: at \(R=3\) the confirmed argmin is \(3\).

### 4.2 Isolated per-mode water-filling is IMP-N60, already failed

The discrete Gaussian / Sims rule, applied to the world's own modes, is: include mode \(m\) of state-cost \(c_m\in\{1,2\}\) iff

\[
R\cdot\frac{\sigma_m^2-E_\infty^{(m)}}{E_\infty}>c_m.
\]

That is exactly IMP-N60 (`core/keystone_checks/RHYTHM_PREREG.md`). It failed its gates (PRIMARY 58/189, Model S 5,890/19,320), and the independent review explained why: isolated values are not joint decrements (seed 0: isolated \(V=(0.368,0.055,0.205)\) against joint decrements \((0.645,0.0455,0.00091)\)). The first store filters the *sum*, not one mode; late isolated values overstate the last joint decrement by orders of magnitude. This note does not rescue or re-test that rule.

### 4.3 Water-filling on joint decrements is N60, not a new prediction

If \(\delta_k=\varepsilon_{k-1}-\varepsilon_k\) are the decrements of the *optimised* degree-\(K\) curve, the rule "add layer \(k\) iff \(R\delta_k>1\)" is N60, and on the lower convex hull it is an identity with \(\arg\min_K[K+R(1+\varepsilon_K)]\). CORE.md already says so. It is the right *definition* of the increment test. It is not a prediction from the world's poles and stakes without first computing the \(\varepsilon_K\) curve. A predictive rule cannot take those decrements as input.

### 4.4 What a correct translation would have to be

Under the cost \(hK+w E_K\), a state is worth keeping if the MSE it removes, times \(w\), exceeds \(h\). That *is* a water-filling threshold, with water level \(h/w=E_\infty/R\) in absolute MSE, or \(1/R\) in units of \(\varepsilon\). The question is: *which* "energies" get compared to the water?

They have to be *joint* (shared observation, one scalar \(y\)). They have to be available from the world and the stakes *without* a reduced-order library search, or the rule is the hull identity. The unique object that already knows about the joint observation and about causality is the full-order Kalman–Bucy *estimate* (degree \(n=\) the world's degree; L2). In innovations form it obeys \(d\hat x = A\hat x\,dt + K\,d\nu\), with \(\nu\) white of intensity \(N\) and \(K=PC^\top/N\). The generator \(A\) appears because that is the innovations realisation of \(\hat x\); the gain \(K\) and the error \(P\) are those of the observer. For one OU the *observer* pole is at \(-b^*=-\sqrt{a^2+2av/N}\), not at the process pole \(-a\). The input–output Hankel operator of this innovations map ranks states by energy in \(\hat s=C\hat x\) (Moore 1981; Glover 1984; for stochastic realizations, Desai & Pal 1984). In balanced coordinates the \(H_2\) variance of \(\hat s\) splits as a sum of per-state contributions \(\gamma_i\) with

\[
\sum_i\gamma_i=\mathrm{Var}(s)-E_\infty.
\]

The discrete water-filling rule at price \(h\) per state is then

\[
K^*_{\mathrm{WF}}=\#\{i:\ R\gamma_i/E_\infty>1\}.
\]

This is the derived rule. It is not Kolmogorov's integral over \(\{\omega:S(\omega)>\theta\}\). It is reverse water-filling on the joint observer's state energies, which is the object that could actually be analogous to \(K\).

**Reduction on one OU (L1).** The filter has one state, \(\gamma_1=v-P\), \(E_\infty=P=N(\sqrt{a^2+2av/N}-a)\). The rule says \(K^*=1\) iff \(R(v-P)/P>1\), else \(0\). That is exactly N60-from-0, and exactly the comparison of \(J_0=R v/P\) with \(J_1=1+R\). So the rule is consistent with the one theorem that fixes \(K^*\) in closed form.

**Not an identity for \(J>1\).** Balanced \(H_2\) contributions are not the decrements of the *optimised* degree-\(K\) library. Balanced truncation is generally suboptimal for \(H_2\); the \(H_2\)-optimal reduced filter is a different object, and GTAO's library (parallel first-order stores, plus resonant blocks) is a further restriction. If the predicted \(K^*\) equals N60-from-0 on every multi-mode world *and* the \(\gamma_i/E_\infty\) equal the optimised decrements to numerical identity, the rule was tautological and the test is void. That check is in the prereg.

**The tautology trap, stated up front.** Computing the Riccati already solves the *full-order* filter (the rhythm review's warning). The rule may use that unique object. It may not use any reduced-order \(E_K\), any library optimiser, or the \(\varepsilon_K\) curve. Relative to the quantity it is scored against (argmin over a finite library), it is a prediction. Relative to "solving the filter," it is cheaper than the \(\varepsilon_K\) curve (one ARE, not a search at every \(K\)) but not a closed form in the poles alone.

### 4.5 Finite-order filters, another break with classical RD

Classical reverse water-filling produces a *residual spectrum* \(\min(\theta,S(\omega))\), which is not a rational function of finite degree (except in special cuts). A \(K\)-state causal filter can realise only a rational error spectrum of degree \(O(K)\). Even if one wanted Kolmogorov's residual, a finite-\(K\) design can only *approximate* it. That approximation problem is rational \(H_2\) / Wiener-filter approximation (the repo already cites Braess & Hackbusch and Jiang et al. for rates, as a conjecture, in LAYERS.md L3). Water-filling tells you the target residual; it does not tell you the degree needed to approximate that target. The HSV rule above is one standard answer to "what degree is needed," coming from model reduction rather than from Shannon theory.

---

## 5. Where the mapping breaks (summary)

| Break | What goes wrong | Consequence for \(K^*\) |
|---|---|---|
| **Per-state cost \(h\) versus per-nat cost \(\kappa\)** | Reverse water-filling is derived from a linear price on rate. \(h\) is a fixed price on McMillan degree (a \(0\)-norm on poles). A narrow rhythm is cheap in rate, dear in states; a broad OU mode is the opposite. | Ranking by Kolmogorov rate is not ranking by layer cost. The even-\(K\) pair rule is the rate-style count and is already false. |
| **Frequency axis versus scale / pole axis** | Model S is unimodal at \(\omega=0\). Layers track *scales* (real poles), and rhythms add peaks at \(\pm\Omega\). Fractal \(1/f\) is a continuum of scales sharing one frequency bump. | \(\#\{\text{peaks of }S>\theta\}\) is \(0\) or \(1\) in Model S, where N60 can return \(K^*\) up to \(J\). The holographic picture, if it works, is water-filling on *scale* bands, not on \(\omega\). |
| **Causal filtering versus noncausal RD** | Kolmogorov–Berger residual is \(\min(\theta,S)\). GTAO's \(E_\infty\) is Yovits–Jackson / Kalman–Bucy. Sequential RD water-fills a Riccati object. | Noncausal peak lists can mis-rank bands that matter only causally (lead time, phase). |
| **Finite-order filters** | The RD-optimal residual is generally infinite-dimensional. \(K\)-state designs are rational of degree \(K\). | Water-filling does not produce a layer count; one still needs a degree-selection rule (HSV, or the \(\varepsilon_K\) curve itself). |
| **Shared observation (joint versus isolated)** | Modes are not parallel Shannon sources. One scalar \(y\) couples them. Isolated \(\sigma_m^2-E_\infty^{(m)}\) is not the joint increment. | IMP-N60 fails, including in Model S, where kind-matching is irrelevant. |
| **Gaussian assumption** | Reverse water-filling is exact for Gaussians with MSE (and a bound otherwise). Model S and \(\mathcal M_{\mathrm{LG}}\) are Gaussian; the law hypothesis is not restricted to that class. | In-model the Gaussian step is fine. It is not a reason to export the count to non-Gaussian worlds without a new argument. |
| **Tautology** | Any rule that needs the whole \(\varepsilon_K\) curve, or that is algebraically the hull test, is not a prediction from the world's time scales. Using the full-order ARE is an intermediate: disclosed, and checked in the prereg. | A pass of a tautological rule would not settle the open predictive count. |

---

## 6. Prior art, checked on Crossref 20 Nov 2026

Verified on the Crossref API (`/workspace/gtao-wf/crossref_dois.json`):

| Work | Crossref record | Role here |
|---|---|---|
| Kolmogorov 1956, "On the Shannon theory of information transmission in the case of continuous signals," *IRE Trans. Inf. Theory* 2:102–108 | [10.1109/TIT.1956.1056823](https://doi.org/10.1109/TIT.1956.1056823) | Reverse water-filling / \(\varepsilon\)-entropy of Gaussian processes. |
| Sims 2003, "Implications of rational inattention," *J. Monetary Econ.* 50:665–690 | [10.1016/S0304-3932(03)00029-1](https://doi.org/10.1016/S0304-3932(03)00029-1) | Attention as a rate; already credited in THEORY and LITMAP for the \(\kappa I_{\mathrm{mem}}\) Lagrangian. |
| Maćkowiak & Wiederholt 2009, "Optimal sticky prices under rational inattention," *AER* 99:769–803 | [10.1257/aer.99.3.769](https://doi.org/10.1257/aer.99.3.769) | Multi-source rational inattention (already in LITMAP). |
| Tatikonda & Mitter 2004, "Control under communication constraints," *IEEE TAC* 49:1056–1068 | [10.1109/TAC.2004.831187](https://doi.org/10.1109/TAC.2004.831187) | Causal / sequential information constraints in control; already in INTERNAL_MODEL §9. |
| Tanaka, Kim, Parrilo & Mitter 2017, "Semidefinite programming approach to Gaussian sequential rate-distortion trade-offs," *IEEE TAC* 62:1896–1910 | [10.1109/TAC.2016.2601148](https://doi.org/10.1109/TAC.2016.2601148) | Causal RD for Gaussians: a Riccati / SDP object, not Kolmogorov's \(S(\omega)\) integral. |
| Kalman & Bucy 1961, "New results in linear filtering and prediction theory," *J. Basic Eng.* 83:95–108 | [10.1115/1.3658902](https://doi.org/10.1115/1.3658902) | The unique full-order causal filter used below. |
| Moore 1981, "Principal component analysis in linear systems," *IEEE TAC* 26:17–32 | [10.1109/TAC.1981.1102568](https://doi.org/10.1109/TAC.1981.1102568) | Hankel singular values and balanced truncation (degree selection). |
| Glover 1984, "All optimal Hankel-norm approximations of linear multivariable systems," *Int. J. Control* 39:1115–1193 | [10.1080/00207178408933239](https://doi.org/10.1080/00207178408933239) | Hankel-norm reduction and error bounds. |
| Desai & Pal 1984, "A transformation approach to stochastic model reduction," *IEEE TAC* 29:1097–1100 | [10.1109/TAC.1984.1103438](https://doi.org/10.1109/TAC.1984.1103438) | Stochastic balancing of a realization. |
| Francis & Wonham 1976, "The internal model principle of control theory," *Automatica* 12:457–465 | [10.1016/0005-1098(76)90006-6](https://doi.org/10.1016/0005-1098(76)90006-6) | Kind-matching of a regulator; already used in the rhythm prereg, and not a counting rule. |

**No Crossref DOI found**, and not claimed:

- Berger 1971, *Rate Distortion Theory: A Mathematical Basis for Data Compression*, Prentice-Hall, Englewood Cliffs, NJ. ISBN 0-13-753103-6. Book. Searched on Crossref 20 Nov 2026; no DOI record for this title. Cited as a book.
- Shannon 1959, "Coding theorems for a discrete source with a fidelity criterion," *IRE Nat. Conv. Rec.* 7(4):142–163. Convention record; no DOI sought as confirmed.
- Yovits & Jackson 1955, "Linear filter optimization with game theory considerations," *IRE Nat. Conv. Rec.* 3(4):193–199. The repo's \(E_\infty\) formula; convention record, no Crossref DOI found.

**Honesty about novelty.** Applying reverse water-filling to \(\kappa I_{\mathrm{mem}}\) is known, and is already in GTAO. Applying it naively to \(K^*\) via peaks of \(S(\omega)\) is a mistake, not a contribution. The HSV / \(H_2\)-energy rule is standard model reduction, applied to the Kalman–Bucy observer, with GTAO's threshold \(1/R\). If it predicts \(K^*\), the novelty is the threshold and the package (one priced objective, this degree rule, a kill criterion), not the balanced-truncation machinery. If it does not, the mapping of the keystone to reverse water-filling does not hold in any form worth keeping, and the predictive rhythm count stays open.

---

## 7. The derived rule (WF-HSV)

**Inputs (and only these):** the world's state-space realisation \((A,C,Q)\) from its poles and variances, the observation-noise density \(N\), and the stakes \(R\). The realisation convention is the one already used in `core/keystone_checks/resonant_layers.py`: an OU mode \((a,v)\) is \(A=(-a)\), \(Q=(2av)\), \(C=(1)\); a rhythm with poles \(-\beta\pm i\Omega\) and pole-variance \(v_r\) is the block \(A=\begin{pmatrix}-\beta&-\Omega\\ \Omega&-\beta\end{pmatrix}\), state covariance \(P_x=2v_r\,I\), \(Q=-(AP_x+P_x A^\top)\), \(C=(1,0)\).

**Computation.**

1. Solve the Kalman–Bucy ARE \(AP+PA^\top-PC^\top N^{-1}CP+Q=0\) for the unique positive-semidefinite \(P\). Set \(E_\infty^{\mathrm{ARE}}=CPC^\top\) and \(K_g=PC^\top/N\). If the ARE fails, or \(E_\infty^{\mathrm{ARE}}\) is not positive and finite, the prediction is **INDETERMINATE**.
2. Form the Kalman gain \(K_g=PC^\top/N\) and, as a diagnostic only, the observer \(A_f=A-K_g C\). The rule does not use the observer poles as a placement prediction. If the process generator \(A\) is not Hurwitz, the stationary Lyapunov equations below fail and the prediction is **INDETERMINATE**.
3. Solve the Gramians of the *innovations* realisation of the estimate, \(d\hat x=A\hat x\,dt+K_g\,d\nu\), \(\hat s=C\hat x\): \(A W_c+W_c A^\top+N K_g K_g^\top=0\) and \(A^\top W_o+W_o A+C^\top C=0\). (The \(y\to\hat s\) realisation uses \(A_f\), but its white-input \(H_2\) is *not* \(\mathrm{Var}(\hat s)\). Using \(A_f\) here would break the one-OU identity of §4.4.) These Gramians satisfy \(W_c=\Pi-P\) with \(\Pi\) the prior state covariance, and \(C W_c C^\top=\mathrm{Var}(s)-E_\infty\).
4. Compute Hankel singular values and the balanced output row by the square-root algorithm: Cholesky (or eigendecomposition, if a Gramian is only semidefinite) \(W_c=L_c L_c^\top\), \(W_o=L_o L_o^\top\); SVD \(L_o^\top L_c=U\Sigma V^\top\); \(\sigma_i=\Sigma_{ii}\); \(T=L_c V\Sigma^{-1/2}\) on the positive \(\sigma_i\). The balanced output row is \(C_{\mathrm{bal}}=C T\). Per-state \(H_2\) contributions are \(\gamma_i=C_{\mathrm{bal},i}^2\,\sigma_i\).
5. Consistency: \(\lvert\sum\gamma_i-(\mathrm{Var}(s)-E_\infty^{\mathrm{ARE}})\rvert\) must be \(\le 10^{-6}\max(\mathrm{Var}(s),1)\) and \(\le 10^{-4}E_\infty^{\mathrm{ARE}}\), else **INDETERMINATE**.
6. Relative energies \(\delta_i=\gamma_i/E_\infty^{\mathrm{ARE}}\). The prediction is
   \[
   K^*_{\mathrm{WF}}=\#\{i:\ R\delta_i>1\}.
   \]
   Empty (all below water, or \(n=0\)) is \(K^*=0\).

**What this is not.** It is not N60, not IMP-N60, not a count of peaks of \(S(\omega)\), and not a pair rule. It does not use a reduced-order optimiser. **It does not predict process-band placement.** The output is a state count \(K^*_{\mathrm{WF}}\). Optimal store rates in the first-order library sit on the fast (observer) side of the process bands, already in closed form on one OU (\(b^*=\sqrt{a^2+2av/N}\)) and, in a related fair fractal test on scale-free Model-S worlds (T20, `/workspace/gtao-t20/.../holographic_2026-11-20/RESULTS.md`, Family S/M prediction (B) fail; those worlds are not used for confirmation here), in the many-mode fits as well. A rule that placed layers on the world's process scale bands would be a different, already failed, claim.

**Scoring, not part of the rule.** On Model S, \(K^*_{\mathrm{WF}}\) is compared to \(\arg\min_{K=0..J}[K+R(1+\varepsilon_K)]\) with \(E_K\) from the merged solver `theory/layers_checks/stores.py`. On rhythmic and mixed worlds, the same comparison is against the extended library in `resonant_layers.py` (first-order stores at cost \(1\), resonant blocks at cost \(2\)), with \(C\) the total state cost. Worlds used to confirm are fresh, and in particular are not the 21 rhythm-test worlds of `RHYTHM_PREREG.md` / `rhythm_rule.json`.

---

## 8. What would mean that "the mapping holds"

- **Holds for \(\kappa I_{\mathrm{mem}}\).** Already yes, as P3 / INTERNAL_MODEL, for the noncausal or scalar-Gaussian form; with the causal caveat of §3.3. Not re-tested here.
- **Holds as "\(K^*\) equals the number of frequency peaks of \(S\) above water."** No. False in Model S (§4.1). Not tested as a primary rule.
- **Holds as isolated per-mode water-filling.** No. That is IMP-N60, already failed.
- **Holds as joint-increment water-filling.** Yes, but only as the hull identity (N60-from-0). Not a predictive mapping.
- **Holds as WF-HSV (§7).** Open. A pass on fresh Model S worlds (where N60 is already exact) would mean the Kalman *estimate's* Hankel energies are a good *predictive* surrogate for the joint decrements, as a *count*. A pass on fresh rhythmic and mixed worlds would be the first predictive count that might survive the case that killed N60's formula and IMP-N60. A fail on Model S would mean even this translation of water-filling does not recover the case the keystone already has. A fail only on rhythms would keep the predictive rhythm count open, and would say the mapping is not the missing piece for that case.

The prereg locks these gates before any confirmation run.
