# The heat floor with feedback, for a part (T61 applied to the swarm rule)

*Friday 27 November 2026 (America/New_York). Part of `theory/swarm-2026-11-27/` (index: `INDEX.md`). Branched from `863a8a8bb3e0bb46c00a9236a9b4d5192c4b9d8d`. The swarm rule left one item: "Applying T61 to a part that moves the whole's signal is not worked out. OPEN" (`theory/SWARM_RULE_2026-11-23.md:91` at the branch point; the same item at `theory/THEOREMS.md:171`). This note works it out in finite bipartite jump chains. Checks: `checks/swarm27_checks.py`, section H. A self-check, not an independent review.*

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

Labels as in `FOLD_INS.md`. Heats are in units of \(kT\) per unit time; \(L(\varepsilon)=(1-2\varepsilon)\ln\frac{1-\varepsilon}{\varepsilon}\) is the telegraph learning-rate floor of T60 (`theory/GENERAL_FLOOR_FINITE_2026-11-23.md:25`).

## 1. The class (named FP)

Three binary coordinates in continuous time: the **world** \(X\), a fair telegraph that flips at rate \(r\) and that nothing moves; the **whole's signal** \(S\); the **part's memory** \(M\). Every transition changes one coordinate (bipartite). \(S\) and \(M\) flip with rates that satisfy local detailed balance with energies \(E_S\) and \(E_M\) (each bath at one temperature), so the heat of a flip is the log ratio of its forward and backward rates. Untampered: \(E_S\) depends on \((s,x)\) and \(E_M\) on \((m,s)\). **Channel tamper** at level \(\tau\in[0,1]\): \(E_S=-J_S[(1-\tau)\sigma(s,x)+\tau\sigma(s,m)]\), with \(\sigma(a,b)=\pm1\) for agree or disagree, so the part's memory steers the whole's signal; \(\tau=1\) is full tamper. Write \(\varepsilon_M(Z)\) for the Bayes error of guessing \(Z\) from \(M\), and \(\varepsilon_{SM}(X)\) for guessing \(X\) from \((S,M)\).

## 2. Results

**P1 (an untampered part has the exogenous floor; PROVED (in-model), an instance of T60 and JP-heat).** If the part does not move the signal (the stay clause's condition, `theory/SWARM_RULE_2026-11-23.md:45`), then for a fair telegraph signal of rate \(\lambda\) and any finite memory with local detailed balance,
\[
\dot Q_M\ \ge\ I_{\text{alt}}\ \ge\ \lambda\,L\bigl(\varepsilon_M(S)\bigr).
\]
*Proof.* The first inequality is JP-heat (Horowitz & Esposito 2014), the second T60's telegraph reduction, both for a memory that does not move its signal. ∎ *Check:* `part_floor_exogenous_signal` (random memories with two to four states).

**P2 (the floor alone never makes leaving the part's best move; PROVED (in-model)).** Let the part pay the share \(s\) of the memory heat at price \(\eta\) per unit, and lose \(w\) per unit of error, so following at error \(\varepsilon\) costs at least \(s\eta\lambda L(\varepsilon)+w\varepsilon\) and leaving (\(\varepsilon=\tfrac12\), no memory) costs \(w/2\). Then
\[
s\eta\lambda L(\varepsilon)+w\varepsilon-\frac w2=\Bigl(\tfrac12-\varepsilon\Bigr)\Bigl[2s\eta\lambda\ln\tfrac{1-\varepsilon}{\varepsilon}-w\Bigr],
\]
which is negative for \(\varepsilon\) close enough to \(\tfrac12\), for every \(s,\eta,\lambda,w>0\). *Proof.* Expand \(L\); the bracket tends to \(-w\) as \(\varepsilon\to\tfrac12\). ∎ The floor's marginal cost vanishes at \(\varepsilon=\tfrac12\) while the loss falls linearly, so the floor never rules tracking out: whether some tracking beats none depends on how close a real memory comes to the floor and on the read price of the stay clause. (The expression above is a lower bound on what following costs, so P2 shows only that the floor cannot force leaving. The locked check's printed gloss, "< 0 means following beats leaving", says more than the check shows; see `ERRATA.md`, E1. The locked bytes are unchanged.) *Check:* `floor_alone_never_forces_leave` (code sanity on random parameters).

**P3 (the floor per read is bounded; code sanity).** With Poisson reads at rate \(f\) and a memory that copies the signal at each read, the error is \(\varepsilon=\lambda/(f+2\lambda)\) (a two-state mismatch chain: mismatch at rate \(\lambda\), repair at rate \(\lambda+f\)). The floor per read, \(\lambda L(\varepsilon)/f\), is a function of \(x=f/\lambda\) alone; its maximum over \(x\) is computed in `per_read_floor_bounded` and is below \(1\,kT\) per read. So in the stay clause the floor adds at most a fraction of \(kT\) to the read price \(c\) per read.

**P4 (a tampering part is in T61's class: no floor on its own heat in terms of what it knows about the signal; PROVED (in-model), an instance of T61, shown by P5).** With \(\tau>0\) the part's memory moves its signal, so P1 no longer applies. T61 (`theory/FEEDBACK_FLOOR_2026-11-23.md:13-35`) shows for finite bipartite chains that the net learning rate can fall below the exogenous floor and change sign, and that no design-independent lower bound on the memory's heat alone exists. In class FP this is explicit: at full tamper with \(J_S=J_M=J\), P5 gives \(\dot Q_M=0\) while the part's error about the signal is \(\varepsilon_M(S)=1/(1+e^{2J})<\tfrac12\) (the Boltzmann weight of disagreement), where an untampered part at that error would pay at least \(\lambda L(\varepsilon_M(S))>0\). ∎ *Check:* `channel_tamper_buys_heat_with_world_information` (the \(\tau\) table in the output).

**P5 (full tamper with equal couplings buys zero heat with zero knowledge of the world; with unequal couplings the part still gives off heat knowing nothing; PROVED (in-model)).** At \(\tau=1\) the rates of \((S,M)\) do not depend on \(X\) and the rates of \(X\) do not depend on \((S,M)\), so the stationary law is a product and \((S,M)\) is independent of \(X\): \(\varepsilon_M(X)=\varepsilon_{SM}(X)=\tfrac12\). If moreover \(J_S=J_M\), both flips are detailed-balanced with respect to the one energy \(-J\sigma(s,m)\), the pair is in equilibrium, and \(\dot Q_M=\dot Q_S=0\). With \(J_S\neq J_M\) the pair is not in equilibrium and the part's memory still gives off heat while knowing nothing about \(X\). *Proof.* A product generator has a product stationary law; detailed balance with respect to one energy makes every current vanish. ∎ *Check:* `channel_tamper_buys_heat_with_world_information`.

**P6 (the pair floor survives every tamper level; PROVED (in-model), T60 and JP-heat applied to the pair).** For every \(\tau\in[0,1]\) and couplings,
\[
\dot Q_S+\dot Q_M\ \ge\ l_{SM}\ \ge\ r\,L\bigl(\varepsilon_{SM}(X)\bigr)\ \ge\ r\,L\bigl(\varepsilon_M(X)\bigr),
\]
where \(l_{SM}\) is the learning rate of the pair about \(X\).
*Proof.* \(X\) is exogenous and the pair \(Y=(S,M)\) is a finite memory whose transitions satisfy local detailed balance, so JP-heat gives the first inequality and T60's telegraph reduction the second. Guessing from \((S,M)\) is at least as good as from \(M\), so \(\varepsilon_{SM}\le\varepsilon_M\), and \(L\) is decreasing on \((0,\tfrac12)\). ∎ *Check:* `pair_floor_under_tamper` (all tamper levels in the table plus random couplings and rates).

**Reading.** A part that tampers with the whole's signal can move heat off its own bath (P4, P5), even to zero, but only by giving up what the signal told it about the world (P5), and the heat of the signal and the part together keeps the exogenous floor set by what the part still knows about the world (P6). This is the thermodynamic face of the swarm rule's identity \(D^{\text{enf}}-D^{\text{ch}}=w(r_\infty-g)\): channel tampering costs the part the signal's worth.

## 3. Prior art

Horowitz & Esposito 2014, doi [10.1103/PhysRevX.4.031015](https://doi.org/10.1103/PhysRevX.4.031015) (JP-heat; information flow in bipartite systems). T60 and T61 are this repository's (`theory/GENERAL_FLOOR_FINITE_2026-11-23.md`, `theory/FEEDBACK_FLOOR_2026-11-23.md`). P1, P4 and P6 are applications; P5's product argument is elementary.

## 4. Not derived here

- **A floor on the part's own heat in terms of its error about the world, under partial tamper** (\(0<\tau<1\)): whether \(\dot Q_M\) alone has a positive lower bound in terms of \(\varepsilon_M(X)<\tfrac12\) is OPEN. P6 bounds the sum; T61 rules out a bound in terms of \(\varepsilon_M(S)\) alone.
- **Continuous (diffusion) parts** and signals other than a telegraph are not treated here.
