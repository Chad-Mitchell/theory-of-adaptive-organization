# Preregistration: is least action a special case or limit of minimizing the cost of judgment?

*Friday 27 November 2026 (America/New_York). Branch `least-action-2026-11-27`, cut from `main` `52898e7e77ddb4c33df3d646a890e3af1dc524a4`. Written and pushed before any derivation or computation on the scored question; the only script run before this lock is `checks/crossref.py`, a DOI lookup (`crossref.out`). `CORE.md` and `THEORY.md` are not edited. No real-world data. Deviations go in `DEVIATIONS.md` in this folder, appended lines only. Direction: Chad, 27 November 2026 (the physics and the math should meet; test whether least action falls out of the cost).*

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

(Byte for byte from `CORE.md:7`.) Labels: **OBSERVED** is on `main` at `52898e7`, with a file and line. **PAPER** is an expectation written here before the derivation. **KNOWN** is published and credited (DOIs checked on Crossref, `crossref.out`).

## 0. The question and the sources

**Question.** Is the principle of least action an exact special case, or a precisely stated limit, of minimizing the cost of judgment \(J=\dot Q+w\,\mathbb E[\ell]\) subject to \(P(\text{ruin})\le\varepsilon\), as `CORE.md` defines each symbol, units checked? Worked for one free particle, then one harmonic oscillator.

- OBSERVED. The cost: `CORE.md:27` (and `:66`). \(w\) converts the loss into the currency of the heat; temperature does not set it (`CORE.md:29`). Nonnegative prices are assumption A8 (`CORE.md:52`). The heat floor \(\dot Q_M\ge kT\,\dot I_M\) for bipartite chains and additive-noise diffusions (`CORE.md:70`). The read price \(A\) stays assumed as a separate summand (`CORE.md:42`). Selection's stationary law \(\pi\propto e^{-\beta J}\) over designs (`CORE.md:124`).
- OBSERVED. The heat of an additive-noise coordinate with drift \(f\) and noise \(D\) is \(\dot Q=\mathbb E[f^2]/D+\mathbb E[\partial f]\) in units of \(kT\) (the convention cited at `theory/bicausal-a-2026-11-27/PREREG.md:68`; the Stratonovich power at `theory/INFO_PHYSICS_ATTAINABILITY.md:127`; Einstein relation \(kT=D\gamma\) as in `theory/GENERALITY_2026-11-22.md:46`). In SI units, with drag \(\gamma\) and \(D=kT/\gamma\): \(\dot Q=\gamma\,\mathbb E[f^2]+kT\,\mathbb E[\partial_x f]\) (Sekimoto 1998, doi `10.1143/PTPS.130.17`; Seifert 2012, doi `10.1088/0034-4885/75/12/126001`).
- OBSERVED. In-repo context: least action named as the model of a compressed objective (`theory/MASTER_EQUATION.md:9`), with the warning that "minimize some cost" fits any behavior (`theory/MASTER_EQUATION.md:11`). A dynamics from inference (Caticha-type) was deleted from an earlier plan as unneeded and close to the banned claims (`NOTES/rnd-2026-11-26/stepback/TRACKING_FIRST.md:99`). Wording: `process/PROCESS.md:38-41`.

**What this prereg does not promise.** No derivation of mechanics, quantum theory, gravity or any force. One classical-limit match, if found, is one worked case. No real system. No statement about \(w\) or the ruin cap beyond their role here.

## 1. The class PATH and the exact claim

**Class PATH.** One overdamped coordinate \(X\) (the decision variable) with drag \(\gamma\) in a bath at temperature \(T_b\): \(dX=u\,dt+\sqrt{2D}\,dW\), \(D=kT_b/\gamma\), on a window \([0,\tau]\), \(X_0=x_0\). The design is the protocol \(u\). Primary: open loop, \(u=u(t)\). Reported, not scored: linear feedback \(u=-k(t)(X-c(t))\).

**The cost on the window.** CORE's cost is a long-run rate (`CORE.md:27`). Here it is integrated over a finite window, with the loss split into a running part and a terminal part:
\[
J_\tau[u]=\int_0^\tau\bigl(\dot Q(t)+w\,\mathbb E[(X_t-x_*)^2]\bigr)\,dt+w_\tau\,\mathbb E[(X_\tau-x_1)^2],\qquad \dot Q=\gamma\,\mathbb E[u^2]+kT_b\,\mathbb E[\partial_x u].
\]
This is a modeling choice, stated as a deviation from CORE's object (a window total, not a stationary rate), not a CORE definition. The ruin cap is slack (no ruin event is defined in PATH).

**Units.** \(\gamma\): \(\mathrm{J\,s\,m^{-2}}\). \(u\): \(\mathrm{m\,s^{-1}}\). \(\dot Q\): \(\mathrm{J\,s^{-1}}\). \(w\): \(\mathrm{J\,s^{-1}\,m^{-2}}\) (a rate stake, as `CORE.md:29`). \(w_\tau\): \(\mathrm{J\,m^{-2}}\) (a one-time stake). \(J_\tau\): \(\mathrm J\). Action \(S\): \(\mathrm{J\,s}\). Any identification of \(J_\tau\) with \(S\) needs one time constant, to be named.

**Classical targets.** Free particle: \(S=\int_0^\tau\tfrac12M\dot x^2dt\), ends fixed, path \(x_{\mathrm{cl}}(t)=x_0+(x_1-x_0)t/\tau\). Harmonic oscillator (real time): \(S=\int_0^\tau(\tfrac12M\dot x^2-\tfrac12M\omega^2x^2)dt\), \(\ddot x=-\omega^2x\). Its action is stationary, not always minimal: past the first conjugate point, \(\tau>\pi/\omega\), the classical path is a saddle of \(S\) (Gray and Taylor 2007, doi `10.1119/1.2710480`).

**Exact claim (C).** There is a limit, stated in the parameters \((w,w_\tau,kT_b,\gamma)\) and keeping \(\mathbb E[\ell]\) active, in which the mean path of the \(J_\tau\)-minimizing design equals the classical path: (C-FP) for the free particle, for all \(\tau>0\); (C-HO) for the real-time harmonic oscillator, for \(\tau<\pi/\omega\) and for \(\tau>\pi/\omega\).

## 2. Criteria, fixed before the derivation

Each system gets one label.

- **YES.** A limit with \(w\ge0\), \(w_\tau\ge0\) (A8, `CORE.md:52`), \(\mathbb E[\ell]\) active (a nonzero stake that changes the selected path), in which the \(J_\tau\)-minimizing mean path equals the classical path exactly (or converges to it uniformly on \([0,\tau]\)); for C-HO this must include \(\tau>\pi/\omega\); and the GTAO-specific term, the information heat bounded by \(kT\,\dot I\) (`CORE.md:70`), is nonzero before the limit and shapes the selected path.
- **NO.** Any of: (i) no admissible limit gives the classical path; (ii) the match needs a negative stake or price; (iii) the match exists for \(\tau<\pi/\omega\) only, because a minimum cannot sit at a saddle; (iv) the limit is degenerate: if \(w,w_\tau\to0\) removes the loss and \(J_\tau\) then selects \(u\equiv0\) whatever the endpoints, that is a NO, not a YES.
- **RESTATES-KNOWN.** A match exists, but every step is a published theorem and the GTAO-specific term is idle (zero, or without effect on the selected path). In particular, these do not count as a YES: (a) a "world" whose drift is already Newton's equation, so that classical paths minimize a squared residual such as \(\int(M\ddot x+V'(x))^2dt\) (the underdamped Onsager–Machlup functional; the dynamics is put in by hand); (b) a memory copying, at \(w\to\infty\), a world that already moves classically; (c) the proportionality of mean drag heat to kinetic action (Benamou and Brenier 2000, doi `10.1007/s002110050002`; Schmiedl and Seifert 2007, doi `10.1103/PhysRevLett.98.108301`; Aurell et al. 2011, doi `10.1103/PhysRevLett.106.250601`); (d) small-noise most-probable paths (Onsager and Machlup 1953, doi `10.1103/PhysRev.91.1505`; Dürr and Bach 1978, doi `10.1007/BF01609446`; Schilder 1966, doi `10.1090/S0002-9947-1966-0201892-6`; Freidlin and Wentzell, doi `10.1007/978-3-642-25847-3`); (e) a Wick rotation \(t\to-i t\) of a positive cost, which gives Euclidean, not real-time, mechanics.
- **Stationary or minimal.** For C-HO, the derivation states whether the \(J_\tau\) optimum is a minimum or only stationary, from the sign of the second variation, at \(\tau\omega/\pi\in\{0.5,0.9,1.1,2\}\).

**Stated assumptions, counted in RESULTS.** (S1) Path computation is free: the protocol \(u\) is computed and run at no cost; the read and computation price \(A\) stays assumed (`CORE.md:42`), and CORE's floor prices nats learned, not computing steps (`CORE.md:70`). (S2) Open loop: the primary design uses no information about \(X\), so the floor \(kT\,\dot I\) is not exercised. (S3) Additive constant noise and one temperature. (S4) The window form of the cost (§1). RESULTS states which of these the bridge needs.

## 3. PAPER expectations (written before the derivation)

- C-FP: the open-loop optimum has constant velocity for every \(D\) (noise only adds a design-independent variance), with end point \(x_0+(x_1-x_0)\,w_\tau\tau/(\gamma+w_\tau\tau)\to x_1\) as \(w_\tau\to\infty\); the minimized heat is \(2\gamma/M\) times the free action on the mean path. Expected label RESTATES-KNOWN (probability 0.85), because the GTAO-specific information term is idle and item (c) covers it.
- C-HO: a positive running stake gives \(\gamma\ddot{\bar x}=w(\bar x-x_*)\), an inverted (Euclidean) oscillator; the real-time oscillator needs \(w=-\gamma\omega^2<0\), and then a minimum exists only for \(\tau<\pi/\omega\). Expected label NO (probability 0.85).
- Overall: probability of YES about 0.03. A YES would need a term with the opposite sign to a cost, which `CORE.md:52` excludes.

## Gate

| ID | Label | G1 miss (honest odds) | G2 not an identity | G3 rival: same quantity, its value | G4 reach | G5 next step |
|---|---|---|---|---|---|---|
| LA-FP | **CONSISTENCY_CHECK** | — | Fails G2: the open-loop optimum is fixed by the cited known results (§2 (c)); PAPER in §3 | — | (b) `CORE.md:27`, `:70` | Logged; answers the direction question on paper |
| LA-HO | **CONSISTENCY_CHECK** | — | Fails G2: the sign of the effective potential follows from `CORE.md:52` and the Euler–Lagrange equation by hand | — | (b) `CORE.md:52` | Logged; if NO, the bridge is not pursued through PATH |
| LA-INFO | **CONSISTENCY_CHECK** (reported) | — | Fails G2: with linear feedback, certainty equivalence fixes the mean path (Fleming and Mitter 1982, doi `10.1080/17442508208833228`) | — | (b) `CORE.md:70` | Logged; says whether information changes the selected path |

**Gate summary (self-check).** No bar here is a TEST: each outcome is fixed on paper by known results. This file is a labeled paper derivation that answers a direction question, with information about 0 in the sense of `process/PREREG_GATE.md` §3. A same-agent separate gate read is committed as `gate_read.md` before the derivation; it is not an independent reader.

## 4. Deliverables and order

(0) This file is committed and pushed; `LOCK.txt` records its sha256 and the lock commit. (1) `gate_read.md` committed. (2) `DERIVATION.md`: every symbol defined, units checked; sympy checks in `checks/` with committed outputs; Lean in `/tmp/gtao-lean` if feasible (no `sorry`; axioms printed). (3) `RESULTS.md`: one eight-field row per bar (`process/MISS_LOG_TEMPLATE.md`), a label from §2, the stated assumptions used, scope limits, the literature (Onsager–Machlup, Freidlin–Wentzell, Schrödinger bridges (Léonard 2014, doi `10.3934/dcds.2014.34.1533`), Nelson 1966 (doi `10.1103/PhysRev.150.1079`) and Guerra–Morato 1983 (doi `10.1103/PhysRevD.27.1774`), max caliber (Pressé et al. 2013, doi `10.1103/RevModPhys.85.1115`), entropic dynamics (Caticha 2011, doi `10.1088/1751-8113/44/22/225303`), stochastic thermodynamics, and the free energy principle read critically (Friston 2010, doi `10.1038/nrn2787`; Aguilera et al. 2022, doi `10.1016/j.plrev.2021.11.001`)), one scope-limited paragraph on whether the path integral (Feynman 1948, doi `10.1103/RevModPhys.20.367`) has a \(J\) analog (no claims), and the next measurement. Any miss of ours gets a FAILURES row, without new rules. Nothing is merged by the author.
