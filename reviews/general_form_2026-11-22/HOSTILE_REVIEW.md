# Hostile review of draft PR #182

Sunday 22 November 2026. Independent review of https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/182. Head `5eecc3b841a6f647d461d328aeee1f2dc0c9629e`, base `6ca6b452895056372ba5f98f324baf46e196b2bf` (`main` after `git fetch origin main`). The diff against that base is four files: `theory/GENERAL_FORM_PHYSICS_2026-11-22.md` (new), `theory/DERIVATION_CHAIN.md`, `OPEN_WORK.md`, `theory/README.md`. This review edits none of them. No lake build.

The note is a consolidation. Most of the arithmetic it reprints is the arithmetic in the merged notes, and it recomputes. Two statements do not. One is a formula. One is the sentence the note proposes to put in `THEORY.md`.

## BLOCKING

### B1. The telegraph information flow is written as the heat

`theory/GENERAL_FORM_PHYSICS_2026-11-22.md:66`

> At Hamming error \(\varepsilon\) the heat is \(kT\,\gamma(1-2\varepsilon)\ln\rho\) for every rate ratio \(\rho>(1-\varepsilon)/\varepsilon\), and the information flow is \(kT\,\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\). The infimum of the heat is the flow, approached as the memory rates diverge at the minimal affinity.

The merged formula, `theory/INFO_PHYSICS.md:290`, keeps the two quantities apart:

> At fixed error, \(\dot Q=kT\,\gamma(1-2\varepsilon)\ln\rho\) and \(\dot I=\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\), for every \(\rho>(1-\varepsilon)/\varepsilon\).

The heat line matches. The flow line does not. The information flow has no \(kT\).

The same slip is in the note's own statement of the bound, `theory/GENERAL_FORM_PHYSICS_2026-11-22.md:29`, two paragraphs after line 21 has stated \(\dot Q\ge kT\) times the learning rate:

> The information flow, and the Kalman rate where that rate is the learning-rate floor, are lower bounds on \(\dot Q\). They are the price only on the designs that meet the bound.

\(kT\,\dot I\) is a lower bound on the heat. \(\dot I\) is a rate in nats per time. The Kalman rate in the attainability note is \(R(\varepsilon)=a(v-\varepsilon)/\varepsilon\), and the heat floor is \(kT\,R(\varepsilon)\).

Independent check of the closed form, from the four-state chain. With \(\rho=\alpha_c/\alpha_e\) and \(\alpha_e=\gamma(1-2\varepsilon)/(\varepsilon(\rho+1)-1)\), the stationary Hamming error is \(\varepsilon\), and

\[
\dot Q=kT\,\gamma(1-2\varepsilon)\ln\rho,
\qquad
\dot I=\gamma(1-2\varepsilon)\ln\frac{1-\varepsilon}{\varepsilon}.
\]

Swept over \(\rho\in\{8,64,e^{40}\}\), \(\varepsilon\in\{0.2,0.45\}\), \(\gamma\in\{0.3,1,7\}\), and \(kT\in\{1,2.5\}\) (the pairs with \(\alpha_e>0\)), the largest relative residual was \(3.7\times 10^{-16}\) on the heat and \(1.7\times 10^{-15}\) on the flow. At \(\varepsilon=0.2\), \(\gamma=1\), \(kT=1\), both the flow and the heat infimum equal \(0.6\ln 4=0.831776616671934\), which prints as \(0.831776616672\). At \(kT=2.5\) the heat infimum is \(2.5\) times the flow. The note's formula for the flow is the heat infimum.

The number at \(kT=1\) hides it. The symbolic line does not.

**Fix.** Write the information flow as \(\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\). Write the infimum of the heat as \(kT\) times that flow. On line 29, write the lower bound on \(\dot Q\) as \(kT\) times the information flow and \(kT\) times the Kalman rate, and say that this bound equals the heat on the designs that meet it. The cost remains that heat plus the stake.

### B2. The proposed THEORY sentences say the second law sets the memory cost equal to the heat

`theory/GENERAL_FORM_PHYSICS_2026-11-22.md:248` and `:254`. OPEN_WORK T40 (`OPEN_WORK.md:90`) names §9 as the text to adopt.

The §1 replacement:

> Inside the class in §3, the second law sets the memory cost equal to the heat of the memory's bath, and that heat has a floor.

The §2 replacement:

> *Physics*, inside the class in §3, sets the memory cost to the heat of the memory's bath.

The second law, as the note states it on line 21 and as Horowitz and Esposito state it, is an inequality: in steady state the learning subsystem's bath satisfies \(\dot S_r\ge\dot I\) (their equation (11) is the subsystem balance \(\dot S_i=d_t S+\dot S_r-\dot I\ge 0\); the steady state drops \(d_t S\)). The note's own §8 says equality of the heat with the floor is a limit, and that \(w\), a separate \(A\), \(L\), and the ruin cap stay assumed. Identifying the memory term with the bath heat is the proposal's definition of that term. The heat on a finite-rate design sits above the floor: the shrunk spring at rate \(10^6\) and decision error \(0.2\) has heat \(4.0000200001\) against \(R=4\).

Hunk 1 is in better shape. Its class paragraph says the heat is at least \(kT\) times the learning rate, keeps the five-term display for everything outside the class, and says the theorems after the section remain theorems about that display. The hypothesis sentence is in neither hunk. The removed lines of hunk 1 match `THEORY.md` lines 21–39 byte for byte, and the next line of `THEORY.md` is the blank line before the hypothesis. `git diff origin/main -- THEORY.md` is empty.

**Fix.** Replace those two sentences with the distinction hunk 1 already uses. Inside the class, the memory term is the heat of the memory's bath, the second law puts the floor \(kT\) times the learning rate under that heat, and the cost is that heat plus the stake. Outside the class, physics enters as a floor under the prices. The §2 sentence in `THEORY.md:19` currently ends ", not about thermodynamics, and the second law does no further work in it." The replacement ends at "the economics of judgment." If that clause is dropped, say so in the instruction, and keep the claim restricted to the outside of the class.

## SHOULD-FIX

### S1. The opening states the floor for any mean-reverting signal, and says a fast memory reaches it

`theory/GENERAL_FORM_PHYSICS_2026-11-22.md:11` and `:13`

> For a signal that relaxes back toward a mean, that rate is the Kalman rate, and a fast linear memory reaches the floor while the heat stays finite. For a signal that flips between two states, the floor is a different formula, and a fast memory reaches that floor too.

> Several independent relaxing signals, each scored on its own, add their floors. ... When the loss is only the error in the sum, one memory, with one weight on each signal, meets the floor.

§3 and §8 of the same note give the class and the limit. The proved signal is an exogenous equilibrium Ornstein–Uhlenbeck process, an independent collection of those, or the two-state telegraph. A signal that relaxes toward a mean and is neither of those is the open row on line 166. The heat at a finite rate is strictly above the floor. For the shrunk spring, Proposition AT-attain gives

\[
\frac{\dot Q}{kT\,R(\varepsilon)}=\frac{\rho\varepsilon}{\rho(v+\varepsilon)-v}>1,
\qquad\rho=\frac{\lambda}{a+\lambda}.
\]

At \(a=v=kT=1\), \(\varepsilon=0.2\), \(\lambda=10^6\), \(\rho=10^6/1000001\) and the heat is \(800000/199999=4.00002000010000\ldots\), which prints as \(4.000020\) against \(R=4\). The telegraph infimum is the limit of diverging memory rates at the minimal affinity. "Reaches" and "meets" are the wrong verbs for a limit the note's own open list still names.

**Fix.** In §0, name the equilibrium OU and the telegraph, and say the heat approaches the floor as the memory rate diverges, at a finite value. Leave the precise statements in §3–§5 as they are.

### S2. The rank-one spring's heat is printed under the floor at the only error in the sentence

`theory/GENERAL_FORM_PHYSICS_2026-11-22.md:76`

> At rates \((1,100)\), variances \((1,1)\), and sum-error \(0.5\), \(\mu=103.887732673340\); the spring at rate \(10^6\) has heat \(103.877719\); separate memories have heat \(141\), ratio \(1.357234\).

\(\mu(0.5)\) is right. Separate heat \(141\) is right. The spring heat is the heat at a different error.

Solve \(\varepsilon=\sum_k a_k v_k/(a_k+\mu)\). For these rates the quadratic is \(\mu^2-101\mu-300=0\), so

\[
\mu=\frac{101+\sqrt{11401}}{2}=103.88773267333986,
\]

which prints as \(103.887732673340\). The fast-spring parameters of Proposition G-fast, \(g_k=1/(a_k+\mu)\) and \(\sigma^2=\sum a_k v_k g_k^2/\mu\), at \(\lambda=10^6\) give heat \(103.877719377\), learning rate \(103.856919702\), and sum-error \(0.500076936\). Those print as \(103.877719\), \(103.856920\), and \(0.500077\), which is what `theory/INFO_PHYSICS_GENERAL.md:207` prints and what `general_checks.py` prints beside the check name "sum-error 0.5". At the spring's own error the floor is \(\mu(0.500076936)=103.856919445\), and the heat sits \(0.0208\) above it. At sum-error \(0.5\) the same heat sits \(0.0100\) below \(\mu\).

Separate memories at errors \(1/22\) and \(5/11\) have heat \(21+120=141\) exactly. \(141/\mu=1.357234356\), which prints as \(1.357234\).

**Fix.** Put the spring's sum-error \(0.500077\) and its learning rate \(103.856920\) in the sentence, next to the heat. Keep \(\mu=103.887732673340\) as the floor at sum-error \(0.5\).

### S3. The shrunk-spring factor uses a \(\rho\) the note has already defined twice, as something else

`theory/GENERAL_FORM_PHYSICS_2026-11-22.md:140`

> a finite memory rate, the factor \(\rho\varepsilon/(\rho(v+\varepsilon)-v)\) on the shrunk spring, above \(1\);

In this note \(\rho\) is the telegraph rate ratio (line 66) and the ladder ratio (line 95). The factor equals \(\dot Q/(kT\,R)\) when \(\rho=\lambda/(a+\lambda)\), which is the definition in `theory/INFO_PHYSICS_ATTAINABILITY.md:163` and is not stated here. At \(a=v=1\), \(\varepsilon=0.2\), \(\lambda=6\), that factor is exactly \(6\), and the regression gain \(C_{XM}/C_{MM}\) is exactly \(1.2\), which is the "gain" on line 171. The telegraph's minimal ratio at the same error is \(4\). Substituting that \(4\) into the factor gives \(0.8/3.8<1\), which is the wrong object and the wrong side of \(1\).

Line 144 then uses \(\rho/\rho_\star\) for the telegraph excess. \(\rho_\star=(1-\varepsilon)/\varepsilon\) is recoverable from line 66 and is not written down.

**Fix.** Write the spring factor as \(\lambda\varepsilon/((\lambda/(a+\lambda))(v+\varepsilon)-v)\), or define a different symbol as \(\lambda/(a+\lambda)\) at the bullet. Write \(\rho_\star=(1-\varepsilon)/\varepsilon\) once, next to the telegraph excess.

## NIT

### N1. Sensory capacity is printed one digit short of the source

`theory/GENERAL_FORM_PHYSICS_2026-11-22.md:78`

> At rate \(10^6\) and decision error \(0.2\) the path rate is \(999.503125\) and the sensory capacity is \(0.004\).

The path rate matches. On the shrunk spring the Riccati path rate is \(999.503125010\) and the learning rate is \(4.000000000020\), so the capacity \(L/\mathcal T\) is \(0.004001987\). `theory/INFO_PHYSICS_ATTAINABILITY.md:39` prints \(0.004002\). The same note's sequence at \(\lambda=10^6\) prints \(0.0040\).

**Fix.** Print \(0.004002\).

### N2. The proposed class paragraph says the fast memory attains the floor

`theory/GENERAL_FORM_PHYSICS_2026-11-22.md:239`, inside hunk 1:

> A fast linear memory attains the OU floors at finite heat. A fast memory attains the telegraph floor in the same kind of limit.

"The same kind of limit" is what keeps the pair from saying equality at a finite rate. §8 says the equality is open and the infimum is a limit, and the heat at rate \(10^6\) is \(4.000020\) against \(4\). The telegraph sentence in the same paragraph correctly writes the learning rate as \(\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\), without the extra \(kT\) of line 66.

**Fix.** Write "approaches" in both sentences.

## What was checked and holds

### The numbers the note reprints

Recomputed from the Lyapunov moments and the closed forms, then again by rerunning the three check scripts. The printed values below are the note's digits. The exact values sit under them where the print is a rounding.

| Claim | Recomputation | Result |
|---|---|---|
| Shrunk spring, \(a=v=kT=1\), \(\varepsilon=0.2\), \(\lambda=10^6\) | \(800000/199999=4.00002000010000\ldots\) against \(R=4\) | prints as \(4.000020\) |
| Centered spring, raw error \(0.25\), same rate | heat \(4.000012000036\), decision error \(0.200000319999\), gain \(0.800000480000\) | prints as \(4.000012\), \(0.20000032\) |
| Centered spring, raw error \(0.2\), same rate | heat \(5.00002000008\) | prints as \(5.000020\) |
| Second shrunk spring, \((a,v,\varepsilon)=(4,0.5,0.1)\) | heat \(16.0003200064\) against \(R=16\) | prints as \(16.000320\) |
| Telegraph floor | \(0.6\ln 4=0.831776616671934\) | prints as \(0.831776616672\) |
| Scalar frontier at stake \(2\) | \(2\sqrt{2}-1=1.828427124746190\) | prints as \(1.828427124746\) |
| Blind stake | \(kT a/v\) | matches |
| Three-mode ladder, rates \((1,10,100)\), stake \(2\) | count \(\lfloor\log_{10} 2\rfloor+1=1\), cost \(5.828427124746\) | matches |
| Ladder count | \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\) once the slowest pays | matches |
| Rank-one gains | \(g_k=1/(a_k+\mu)\), heat floor \(kT\mu\) | matches the stationarity argument in G-sum |
| Identical modes | \(K\) separate memories, each at error \(\varepsilon/K\), cost exactly \(K\) times the scalar floor of variance \(Kv\). At \(K=2\), \(a=v=1\), \(\varepsilon=0.8\): joint \(1.5\), separate \(3\) | matches |
| \(\mu\) at sum-error \(0.5\), separate heat, ratio | \(103.887732673340\), \(141\), \(1.357234\) | match; see S2 for the spring heat |
| Four-mode blind stake | \(1000/1111\) | exact |
| Half-tracked count versus per-mode count | at stakes \(2\) and \(200\), the counts are \((0,1)\) and \((2,3)\) | "not the same integer at every stake" holds |
| Capacity-1 design at decision error \(0.2\) | \(\nu=9\), \(B=\nu^2/(\nu^2-1)\), heat \(8=2R(0.2)\) exactly | matches |
| Shrunk-spring gain at rate \(6\) | \(C_{XM}/C_{MM}=1.2\) exactly | matches |
| Soft 64-bin learning rate | the attainability script prints \(4.022937\) at MMSE \(0.200000\) | matches |
| Coupled spring, rate \(10^5\), noise \(0.25\) | heat \(7.999912968\), learning rate \(7.999489967\), static rate \(\operatorname{tr}(D)/0.25=8\) | prints as \(7.999913\) against \(8\) |

`nice -n 19 python3 theory/info_physics_checks/info_physics_checks.py`: PASS 61, FAIL 0. `attainability_checks.py`: PASS 31, FAIL 0. `general_checks.py`: PASS 33, FAIL 0. The same 31 and 33, and the same printed heats, came back after NumPy moved from 1.26.4 to 2.5.5. The note's count "61, 31, and 33 checks, FAILS 0" is the count these scripts print.

### Scope, once past the opening

§3 names the exogenous equilibrium OU, independent collections, and the telegraph, and it says the memory does not move the signal. The centered spring at raw coordinate error is kept as the family the reviews of PR #175 scored, with the constant \(kT a\) called a scoring gap. §7's map says \(\kappa I_{\mathrm{mem}}\) is replaced by the bath heat inside the class, \(hK\) is excess above the floor, \(w\) stays assumed, \(A\) stays assumed as a separate summand, \(L\) stays assumed and outside, and the ruin cap stays outside. §8 lists the same assumptions and does not move IP10, IP14, N65, T15, T18, T35, or T36. The derivation-chain edit keeps weakest link 1, says the derived object supplies none of the term list, the currency, the prices, the cap, \(w\), a separate acquisition summand, or linking, and records IP5 as **FALSE**. That matches CLAIM_MAP IP5. Link 7 of the chain is the Shannon joint-achievability gap, and the new sentence says the heat floor is a different object. T40 says the rewrite is not applied and that the five-term theorems are not re-proved under \(J_{\mathrm{phys}}\).

The cited merges are the merges. `2dd04fa` is PR #161, `01e4415` is the confirm #164, `f18f21f` is #175, `5fbf525` and `c9f02df` are reviews #176 and #177, `b46bf9f` is #178, `74e02e7` is review #179, `d1d6ea5` is #180, `fbf03b7` is review #181.

### The hypothesis sentence, and `THEORY.md`

`git diff origin/main...HEAD -- THEORY.md` is empty. The sentence

> The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

is one copy each in `THEORY.md:41`, `CORE.md:9`, and `README.md:9`, and two copies in the note (lines 31 and 186), each with the same bold markers. It is not inside either proposed hunk.

### Prior art

Crossref, this session, HTTP 200 unless noted. The attributions the note repeats are the right papers.

| Claim in the note | What Crossref, or the paper, returned |
|---|---|
| Horowitz and Esposito 2014, equation (11) | doi 10.1103/PhysRevX.4.031015, *Thermodynamics with Continuous Information Flow*, Horowitz and Esposito. In the arXiv text, equation (11) is \(\dot S_i^X=d_t S^X+\dot S_r^X-\dot I^X\ge 0\) and the same line for \(Y\). The steady state is \(\dot S_r\ge\dot I\). The note's compression matches that consequence. |
| Barato and Seifert 2015, unicyclic theorem, the sensor a 4-cycle of affinity \(\ln 64\) | doi 10.1103/PhysRevLett.114.158101, *Thermodynamic Uncertainty Relation for Biomolecular Processes*, Barato and Seifert. The affinity \(\ln 64\) is the note's sensor at \((\alpha_c,\alpha_e)=(4,0.5)\), which is one cycle. The paper is the unicyclic theorem. Gingrich, Horowitz, Perunov, and England 2016 remains the general jump-process theorem. |
| Sandberg, Delvenne, Newton, and Mitter 2014, equation (46), and the Allerton paper as the port-Hamiltonian account | PRE doi 10.1103/PhysRevE.90.042119, *Maximum work extraction and implementation costs for nonequilibrium Maxwell's demons*, those four authors. Allerton doi 10.1109/ALLERTON.2014.7028503, pages 550–555, same authors, title *Thermodynamic costs in implementing Kalman-Bucy filters*. The abstract says the class is linear port-Hamiltonian systems and that the filter itself is port-Hamiltonian. The factor \(2\) above a Landauer comparison is the account those authors give of a state that keeps the path. |
| Hartich, Barato, and Seifert, capacity 1 forces a factor \(2\) | doi 10.1103/PhysRevE.93.022116, *Sensory capacity*, those three authors. The note's \(\nu=9\) design has heat \(8=2R(0.2)\). |
| Tanaka, Skoglund, and Ugrinovskii, CDC 2017, doi 10.1109/CDC.2017.8264246, trace constraint, no bath heat | Crossref: *Optimal sensor design and zero-delay source coding for continuous-time vector Gauss-Markov processes*, pages 3992–3997, Tanaka, Skoglund, Ugrinovskii. The arXiv (1709.03026) minimizes the Duncan rate subject to the time average of \(\operatorname{Tr}(P_t)\le D\), which is the sum of the marginal mean squares. A search of that text finds no heat, temperature, bath, or dissipation. It is not \(1^\top P 1\). |
| Stavrou, Charalambous, Charalambous, Loyka, and Skoglund, CDC 2018, the nonanticipative \(\tfrac12\log\) rate | doi 10.1109/CDC.2018.8619725, pages 14–20, that author order, title *Asymptotic Reverse-Waterfilling Characterization of Nonanticipative Rate Distortion Function of Vector-Valued Gauss-Markov Processes with MSE Distortion*. |
| Gorbunov and Pinsker, 1973 and 1974, no Crossref work record | A query on author Pinsker plus "Nonanticipatory epsilon entropies and message generation rates" returned eight works, none of them the 1973 or 1974 translation. A query on author Gorbunov in *Problems of Information Transmission* returned later Gorbunov and Lyubetsky papers. No work record for either translation turned up here either. |
| Bo, Del Giudice, and Celani, Crossref families Bo, Giudice, and Celani | doi 10.1088/1742-5468/2015/01/P01014. Crossref author families: Bo, Giudice, Celani. |

The note says nothing in that list is claimed as new, and that the combination it names (the telegraph closed form, the two springs, the reading of \(kT a\), the frontiers and the geometric counts, the comparison with N65) is the combination the three merged notes already list. The proposal adds the map and the unapplied rewrite. Tanaka's program is a \(\tfrac12\log\) Duncan minimization under a trace constraint, with no bath heat, which is the distinction the note draws. I did not find that combination stated as a new bound.

### Wording

The note, the new derivation-chain paragraph, and the T39/T40 rows say cost. They do not say "bill", "kill", "honest kill", "verdict", or "theory of everything".

### Repo checks

| Command | Result |
|---|---|
| `python3 tools/check_consistency.py` | PASS. 392 CLAIM_MAP rows, tally 392, FAIL 0. Two advisory word-count warnings (THEORY.md, README.md), not failures. |
| `python3 tools/check_open_work.py` | PASS |
| `python3 tools/check_fresh.py` | PASS. STATUS points at `fbf03b7`; the window includes `6ca6b45`. |
| `nice -n 19 python3 -m pytest -q tools` | 255 passed, 1 skipped, 312.22 s, exit 0. The skip is `tools/test_lean.py`, "Lean 4 / lake is not installed". `lake` is not on `PATH`. |

Pytest was run after installing pytest 9.2.0, SciPy 1.18.1, and SymPy 1.14.0, which pulled NumPy 2.5.5. The closed-form recomputation above was done before that upgrade. The check scripts were run on both NumPy versions. No lake build.

VERDICT: NEEDS-FIXES
