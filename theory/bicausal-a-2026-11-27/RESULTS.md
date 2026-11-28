# Results ledger: BICAUSAL Route A follow-up

**Lock reference:** `theory/bicausal-a-2026-11-27/PREREG.md`, sha256 `b69b92a13a68f04ea9120f13ba65ea8a55aaa5a09ec8ad9b6c67f5a6dc26bf29`, lock commit `eb0540e308e65eab06ca86c6e3d9d9d2e9a350ce` (pushed and shown by `git ls-remote` before any run). **Gate read:** `gate_read.md`, commit `dee86152ad91f35a56cad62ced79c0c163dd1d2d`, PASS with 0 blocking; a same-agent separate pass, not an independent reader (stated in the file). **Runs:** fresh GitHub clone at the lock commit, `sha256sum -c PREREG.sha256` 10 of 10 OK, nice 19. **Breach check:** `none` (no locked text or prediction edited; deviations in `DEVIATIONS.md`). Every number below is OBSERVED in-model. Nothing is a field result. No single test is decisive.

| prediction_id | locked_prediction (value/band; odds) | outcome (OBSERVED) | miss (signed size & direction, or HIT + info) | location | stake_x_info | update | breach_check |
|---|---|---|---|---|---|---|---|
| BA-C1 (CONSISTENCY_CHECK) | A-T1‴ with the stop-copying limit added: values fixed by logged numbers | Not run, as locked. PAPER: \(G=0.4991\) (\(w_x=0.5\)), \(0.3649\) (\(w_x=1\)), \(0.0654\) (\(w_x=2\)) | information about 0 (identity) | — | low | none | none |
| BA-C2 (CONSISTENCY_CHECK, code gate) | At \(K=1\) no design beats the direct infimum | Optimized \(K=1\) costs 3.0000086, 10.0000086, 43.372 against 2.4641, 5.3246, 19.0 | HIT, information about 0; gate passed, BA-T2 scored | measurement/code | low | none | none |
| BA-T1 | HYPOTHESIS `no-weighted-potential` at all three \(w_x\in\{0.5,1,2\}\) (\(a=D=D_M=1\), \(w=w_w=10\)); odds of a miss 0.15 | `no-weighted-potential` at all three: exact \(\Delta=27462244677/1506922300\), \(5789210497/301384460\), \(31913668101/1506922300\) at \(\gamma=19/7\), \(c=-1/2\), \(g=3\); also nonzero at \(\gamma=13/2\), \(c=1/2\), \(g=3/4\) inside the region the A-T1‴ runs visited | **HIT.** Rival (one-object reading) excluded exactly | model | medium | BICAUSAL row narrowed by a counterexample, after independent review | none |
| BA-T2 | HYPOTHESIS \(\hat K^*(w)\in[12,48]\) at \(w\in\{3,10,100\}\); rivals free-link \(\hat K^*=2\), copy-costs-a-read null none up to 128; odds of a miss 0.60 | \(\hat K^*=32,\,24,\,24\), each confirmed in exact rational arithmetic (margin-adjusted differences \(-0.0376\), \(-0.0252\), \(-0.723\)). Half-tolerance rerun (`checks/ba_t2_half.out`): the same \(\hat K^*\) at all three \(w\), costs equal to \(10^{-9}\) | **HIT** (resolved). Both rivals excluded by more than one grid step. Information lower than the locked odds implied: the exact optima sit at the fast-copy box edge and match the PAPER approximation to about \(10^{-4}\) (process miss `BA-T2-ODDS`) | model | medium | CORE §1 table, row \(L\): pointer to the class result, after independent review | none |

## BA-T1: W2 with both bath heats is not one object

**Statement (PROVED (in-model), computer algebra; not formalized in Lean).** In W2 (`theory/two-route-2026-11-25/PREREG.md:55-59`) with the costs of `PREREG_4.md:31-35`, at \(a=D=D_M=1\), \(w=w_w=10\) and \(w_x\in\{0,0.5,1,2\}\), and also with heats only (\(w=w_w=w_x=0\)), no positive weights make the design game a weighted potential game on any open subset of the domain \(\{\gamma>0,\ gc<1\}\).

*Proof.* \(\Sigma\)'s entries are rational with denominator \(a\gamma(a+\gamma)(cg-1)\) (`checks/ba_t1_sym.py`), nonzero on the domain, so the costs, their cross-partials and \(\Delta=P_{m,1}P_{w,2}-P_{m,2}P_{w,1}\) are real-analytic there. The domain is connected (\(\gamma>0\) times the set \(gc<1\), which is star-shaped about the origin). \(\Delta\) is nonzero at an exact rational point for each setting (`checks/ba_t1_exact.out`). A real-analytic function that vanished on an open set would vanish on the whole connected domain, so \(\Delta\neq0\) on an open dense set and no open set carries a weighted potential (Monderer and Shapley 1996, doi `10.1006/game.1996.0044`). ∎

**What it means for BICAUSAL.** Under the CA1 substitution chain the design distribution is \(\propto e^{-\Psi}\) iff the beta-scaled game is an exact potential (`CORE.md:127`; A-C4 in `theory/two-route-2026-11-25/PREREG_2.md:37`). So W2 is the counterexample the BICAUSAL work order asked for: it meets confinement (S3, \(gc<1\)), no delay (S4) and a non-binding capacity (S5), takes time-scale separation (S1) as given, and is still not one object, because it fails S2 everywhere. The failure is not caused by the stakes: the heats-only game fails too. At \(\gamma=13/2\), \(c=1/2\), \(g=3/4\) the ratio \(P_w/P_m\) of the \(\gamma\)-components is about \(-4\), so the two parties' marginal incentives move in opposite directions there, the opposed-coupling case in which CT32 / COAD-F1 show cycling is possible. Whether W2 settles has to be shown another way, for example by strong monotonicity (CA5), not by a potential. Read for the hypothesis: in W2 there is no single cost that both parties' selection minimizes, so the hypothesis can be read only per party, against each party's best reply, as `theory/two-route-2026-11-25/PREREG.md` §3.4 proposed.

**Limits.** One model family (linear, two baths, the world's design is \(g\) only). A potential on a measure-zero set is not excluded and is not asked for. The proof is computer algebra with exact rationals, not Lean.

## BA-T2: a link paid as heat, and the member count at which a shared level pays

**Statement (PROVED (in-model), by exact rational evaluation of found designs; an upper bound).** In class LINK (linear additive-noise diffusions at one temperature, each memory's mobility free; an exogenous equilibrium OU world with \(a=v=kT=1\); one level reads the world and \(K\) members read only the level, each member deciding from its own state), there are designs whose per-member cost \(\dot Q_0/K+\dot Q_1+w\varepsilon_1\) is below the proved infimum of any direct tracker, \(2\sqrt{kTavw}-kTa\), at \(K=32\) for \(w=3\) and at \(K=24\) for \(w=10\) and \(w=100\). At \(K=1\) no design can (BA-C2). Between, no design was found below the infimum, which is not a proof that none exists.

| \(w\) | \(J_{\mathrm{dir}}\) | per-member ratio at \(K=8\) | at \(\hat K^*\) | at \(K=128\) |
|---|---|---|---|---|
| 3 | 2.4641 | 1.2175 (blind) | 0.9837 (\(K=32\)) | 0.7375 |
| 10 | 5.3246 | 1.2812 | 0.9943 (\(K=24\)) | 0.6686 |
| 100 | 19.0000 | 1.2851 | 0.9610 (\(K=24\)) | 0.6250 |

All numbers: `checks/ba_t2.out`.

**Mechanism, as the optima show it.** The level pays heat \(\dot Q_0=b_0^2av/((a+b_0)D_0)\) (PREREG §3.2, checked against the Lyapunov value), which grows as its noise \(D_0\) falls: a quiet level is expensive. A quiet level is cheap to copy: each member sits at the fast-copy edge of the box (\(\ln b_1=12\) in every row) and pays about \(D_0/\delta\) for extra error \(\delta\). As \(K\) grows the optimum buys a quieter level (\(\ln D_0\) falls from \(-0.79\) at \(K=2\) to \(-2.56\) at \(K=128\), \(w=10\)), and each member's error falls with it.

**What this deletes, and what it does not.** In this class the link price \(L\) of the five-term display (\(\kappa_b\) per member link, \(d\) per member told, `THEORY.md:33`) is not an input: a link is the member's bath heat plus the level's extra heat for being copyable, and the member count at which sharing pays follows from heats and the stake alone. That all costs in class LINK are heats is true by construction; the content is the threshold, which a free link price leaves undetermined (the five-term display with \(L=0\) gives 2, and any value up to infinity with \(L\) free). It does not derive \(w\) or the ruin cap. It does not touch the read price \(A\) beyond what `CORE.md:42` already says (a continuous read is heat). It holds in a free-mobility class; with mobility fixed the level could not be made quiet and the threshold could differ or vanish (gate read note 2).

**Prior art.** That copying generates correlations whose upkeep costs dissipation, and that repeated copies from one source each cost a small nonzero amount, is KNOWN (Ouldridge, Govern and ten Wolde 2017, *Phys. Rev. X* 7:021004, doi `10.1103/PhysRevX.7.021004`, checked on Crossref and read at the abstract level, 27 Nov 2026). That a slow or frozen signal is cheap to track is the in-repo loophole of `CORE.md:78`. BA-T2 adds a threshold in one linear class, not a mechanism.

**Limits.** \(\hat K^*\) is an upper bound found by a local optimizer with box edges on the member rate; a larger box could only lower it. Three stakes, one world. Not formalized in Lean.

## Route A items as asked

- **A-T1** (one object): answered in W2 by BA-T1, negatively for the one-object reading. The unscored deliverables of `PREREG_2.md` §2 now have their counterexample; the bipartite statement is the W2 model with both baths as locked.
- **A-T3** (CL11 cold-bath lever): not run. It was retired before any run on 25 November as ill-posed (`theory/two-route-2026-11-25/PREREG_2.md:41-47`, `:107`); a CL11 test needs a world whose noise is not thermal, which this prereg does not propose.
- **The brief's premise** that Route A turns \(L\) and \(A\) into heat was not in the record (process miss `BICAUSAL-BRIEF-1`). BA-T2 is the bar that addresses \(L\).

**Run cost.** Primary run 2411 s wall, under 60 CPU-minutes; half-tolerance run 3953 s wall, about 100 CPU-minutes on a shared box (over the 60-minute figure in `PREREG.md` §5, which named no consequence; `DEVIATIONS.md`).
