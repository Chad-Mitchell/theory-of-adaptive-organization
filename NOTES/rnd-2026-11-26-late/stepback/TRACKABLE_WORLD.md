# TRACKABLE_WORLD (route A, 26 Nov 2026): what must a world be like for bounded trackers to exist at a finite cost?

*Private R&D note, append-only. Paper only (sympy allowed). Nothing committed, pushed, emailed or posted. Route source: `NEXT_ROUTES_2026-11-26.md` §2 A as corrected by §5 (R2, R3).*

**Re-grounded first (read this session, 26 Nov about 20:16 EST):** `rnd/context/WORKING_CONTEXT.md` (88 lines), `rnd/context/WALLS.md` W1–W14 and the flags table, `NEXT_ROUTES_2026-11-26.md` §2 A and §5, the two proposed walls (`forces-gravity/THREAD_SUMMARY.md:10`, :42–43: "basis-free capacity gives partner modes with ~1/r tails and no cut", "per-site pricing = locality" chosen; `composition/NOTE.md:367`: "A reversible discrete classical world is a zero-cost self-tracker"), `MEMORY_CHALLENGE.md:38` (hold rule), `SESSION_NOTES.md:21–24` (Chad's inversion), `CORE.md:7`, :19–29 at main `8b553c6`.

**Labels:** observed · hypothesis · PIM (proved in model) · known (published; DOI checked on Crossref this session) · elementary.

## PRE-STATEMENT BLOCK (locked; hashed before any derivation)

**Q.** If CORE.md:7's hypothesis is not idle, i.e. bounded trackers exist and sit near a finite minimum of the cost, which properties must the world's dynamics have? For each candidate: necessary, merely sufficient, or not implied; and is it a property physics has?

**Inputs (only these).**
- I1. CORE.md:7 (hypothesis): strongly selected systems minimize the cost of judgment \(J=\text{(upkeep of records)}+w\,\mathbb E[\ell]\) subject to \(P(\text{ruin})\le\varepsilon\) (CORE.md:25–27). The upkeep is taken abstractly as a price \(c>0\) per nat held or written; kT, energy and every physics floor are **not** inputs (W1, W4).
- I2. Bounded trackers exist at finite cost: some system with finite memory has \(J<\infty\) and beats the blind design (\(J<J_{\text{blind}}\)), with \(P(\text{ruin})\le\varepsilon<1\) over an unbounded horizon.
- The hold rule \(w p > c + 2\sqrt{k w\sigma^2/6}\) (`MEMORY_CHALLENGE.md:38`, from GROK_BOT_MEMORY §4) may be used as a consequence of I1 in its class.
- No physics premise (reversibility, locality, energy, kT, ħ, c, G) may be added. If a row needs one, the row is scored as "needs an added premise".

**Candidate rows (fixed now).**
- R1 copying is not free (cite `SESSION_NOTES.md:21`; not re-run).
- R2 a low-entropy (blank) supply (cite W7 / `TRACKING_FIRST.md:74`, :300, :324; not re-run).
- R3 stable distinguishable states (records that persist over the use horizon).
- R4 bounded rate of change / finite predictive information (cite CL10; Bialek et al. 2001).
- R5 bounded speed of influence (locality). Hypothesis going in: not necessary.
- R6 a conserved additive quantity behind a shared price. Per NEXT_ROUTES R3, counts toward HIT only if the hold rule or the ruin cap (not a shared budget) forces it.
- R7 fixed-size lossless summaries / exponential (Gibbs) families (cite W5 row; Koopman 1936, Pitman 1936; not re-run). Pre-labelled: inside W5 (form only).
- R8 (added from the ruin cap) a net positive supply into the reserve.

**Triviality bar (any one ⇒ restatement).** T1 a known theorem in cost words (incl. "trackers need a predictable world" — Bialek; "lossless fixed summaries need exponential families" — Koopman–Pitman; "trackers need a low-entropy source" — W7; "a good regulator must model the system" — Conant–Ashby; "persistence needs positive predictive information" — arXiv 2510.25883); T2 holds for every cost "price per nat + task term" (the hold rule / ruin cap do no work); T3 a form, not a value or a structural selection (W5); T4 the input moves, not removed (W13); T5 depends on a free price ratio (W2).

**Novelty bar (all needed).** N1 not in the prior art below; N2 the cost's own structure (hold rule or ruin cap) makes the property **necessary**; N3 the property is one physics has, stated price-free (holds for every admissible \(w,c,k,\varepsilon\)).

**Prior art searched (this session; Crossref results in `trackable/crossref_tw.txt` and `nextroutes/crossref_nr*.txt`).** Müller 2020 (10.22331/q-2020-07-20-301); Wheeler 1992 (10.1111/j.1749-6632.1992.tb17083.x); Bialek, Nemenman & Tishby 2001 (10.1162/089976601753195969); Still et al. 2012 (10.1103/PhysRevLett.109.120604); Creutzig, Globerson & Tishby 2009 (10.1103/PhysRevE.79.041925); Koopman 1936 (10.1090/S0002-9947-1936-1501854-3); Pitman 1936 (10.1017/S0305004100019307); Kolchinsky & Wolpert 2018 (10.1098/rsfs.2018.0041); Creutz 1983 (10.1103/PhysRevLett.50.1411); Conant & Ashby 1970 (10.1080/00207727008920220); Landauer 1961 (10.1147/rd.53.0183); Landauer 1991 (10.1063/1.881299); Bennett 1982 (10.1007/BF02084158); Lieb & Robinson 1972 (10.1007/BF01645779); Horowitz & Esposito 2014 (10.1103/PhysRevX.4.031015); Hopfield 1974 (10.1073/pnas.71.10.4135); Wolpert 2008 (10.1016/j.physd.2008.03.040); Fields 2018 (10.3390/e20100797). All OK on Crossref. arXiv 2510.25883 ("The Information-Theoretic Imperative", persistence ⇒ positive predictive-information rate): arXiv id only, no DOI, read in a web-search extract only. Two Zenodo preprints seen in search (10.5281/zenodo.19142123, 10.5281/zenodo.19023568) are DataCite DOIs, not checked on Crossref, unrefereed: not used as support. Classical ruin theory (Cramér–Lundberg) is named as a known type; no DOI given or checked.

**Scoring rules (from NEXT_ROUTES §2 A with §5 fixes; not to be loosened).**
- **HIT:** at least one row meets N1–N3, proved in a model (PIM), stated necessary-not-sufficient.
- **OPEN:** a row is necessary only under an added premise that is itself not a physics feature (e.g. a stationary world).
- **MISS:** every row is known (T1–T5) or is not a physics feature. Then write W15-reverse: "the theory constrains worlds only as information theory already does."
- **p(HIT) = 0.10** (stated; NEXT_ROUTES R2).
- **Standing limit (R2):** "bounded trackers exist" is observed of our world, so any necessary property is already true here. A cannot fail against the world; even a HIT shows **necessity, not origin**, and is not a claim that physics arises from tracking.

## END PRE-STATEMENT BLOCK

## 1. Derivation (after the lock; block hash logged in WORKLOG at 2026-11-26T20:18:37-05:00)

Paper plus one sympy/number check: `trackable/tw_check.py`, output `trackable/tw_check.out`. The model class is the hold-rule class of I1: one item, world drift rate \(\sigma^2\), re-read price \(k\), upkeep \(c\), stake × need \(wp\); cost per unit time \(J(T)=c+k/T+w\sigma^2T/6\), minimum \(J^*=c+2\sqrt{kw\sigma^2/6}\) at \(T^*=\sqrt{6k/(w\sigma^2)}\) (C1 reproduces `MEMORY_CHALLENGE.md:38`). The blind design costs \(wp\). Added for R3: the record is lost at rate \(\Gamma\); the lost fraction of an interval is \(1-(1-e^{-\Gamma T})/(\Gamma T)=\Gamma T/2-(\Gamma T)^2/6+\dots\) (C2), costing \(wp\) times that fraction.

| row | result | necessary / sufficient / not implied | label | physics feature? | bars |
|---|---|---|---|---|---|
| R1 copying not free | **Cited, not re-run** (`SESSION_NOTES.md:21`). In this route I1 already sets \(c>0\), so it is an input here, not an output | input (necessary for the hypothesis to be non-idle) | PIM-in-repo (elementary) | weaker than no-cloning (`SESSION_NOTES.md:24`) | T4 here |
| R2 low-entropy (blank) supply | **Cited, not re-run** (W7; `TRACKING_FIRST.md:74`, :300, :324; forces-gravity G1). Necessary there only under reversibility plus leak, which are physics premises this route may not add | needs an added premise, and that premise **is** physics | known (Landauer 1961; Bennett 1982) | yes | T1; W7 |
| R3 stable distinguishable states | With fixed prices, \(\min_T J\) rises with \(\Gamma\) and passes \(wp\): in the C3 cells (c 0.1, k 1, w 1, σ² 0.01, p 1) viable for Γ ≤ 0.1, not for Γ ≥ 1; as Γ→∞, \(J\to c+wp>wp\). So the tracker needs \(\Gamma<\Gamma_{\max}(c,k,w,p,\sigma^2)\). Price-free content: only "some records have nonzero lifetime" (for any finite Γ, a small enough k makes the tracker viable) | necessary (in-class) | PIM, elementary | yes (metastable records) | T5 for the threshold; T1 for the price-free part (Landauer 1991; Hopfield 1974 in kind) |
| R4 bounded rate of change | \(J^*<\infty\) iff \(\sigma^2<\infty\); \(J^*\to\infty\) as \(\sigma^2\to\infty\) (C4). Viability threshold \(\sigma^2<6(wp-c)^2/(4kw)\) is price-set; price-free part is \(\sigma^2<\infty\) for some item with positive need | necessary (in-class) | PIM, elementary | yes | T1 (Bialek et al. 2001; CL10; arXiv 2510.25883); T5 for the threshold |
| R5 bounded speed of influence | Counterexample: CORE's worked OU class (one coordinate, no space) has finite minimized cost (CORE §4); any mean-field world with a bounded-rate mean is also trackable. What R4 needs is a bounded **rate** of the tracked coordinate, i.e. summable influence on it, not a bounded **speed**. Matches the forces-gravity record ("per-site pricing = locality" chosen, `THREAD_SUMMARY.md:42–43`) | **not implied** | PIM (counterexample); "summable influence is the necessary part" is hypothesis | locality is; summability is weaker | — |
| R6 conserved quantity behind a shared price | A conserved coordinate (\(\sigma^2=0\)) is the cheapest record: \(J^*\to c\) (C4), as T68 says. The OU world has no conserved coordinate and is trackable, so not necessary. The ruin cap presupposes a reserve with a balance equation; that bookkeeping is in the cap's definition (T4), not forced on the world. A shared price would come from a shared budget, which NEXT_ROUTES R3 excludes | **sufficient for cheapest; not implied**. R3's HIT condition not met | PIM (counterexample) | yes, but not reached | T4, T1 (Creutzig et al. 2009; Creutz 1983) |
| R7 fixed-size lossless summaries / Gibbs form | **Cited, not re-run** (W5 row; NEXT_ROUTES §2 A row 4). I1 tolerates lossy records (the cost prices residual loss), so lossless sufficiency is not forced | **not implied** by the cost; necessary only for lossless i.i.d. summaries | known (Koopman 1936; Pitman 1936) | Gibbs form yes, value no | T1, T3; **re-hits W5** |
| R8 net positive supply into the reserve | Under I2's unbounded horizon and ε < 1: a reserve walk with zero net drift is recurrent, so ruin is certain (C5: from R = 5, up-probability 1/2 gives 1; 0.55 gives 0.367; 0.6 gives 0.132). So the world must give the tracker a net positive inflow. Price-free in ε | necessary (in-class) | PIM, elementary | an open, driven environment: a boundary condition, not a rule of the dynamics | T1 (classical ruin theory); W7 in kind (the supply is an input) |

**Necessary rows:** R3 and R4 (price-free parts only: finite record lifetime and finite drift), R8 (net inflow, under an unbounded horizon). R1 is an input here. R2 needs a physics premise. **Not implied:** R5 (locality), R6 (conserved quantity), R7 (exponential family, inside W5).

## 2. Score against the locked rules

- N1 fails for every necessary row: R3 and R4 are Landauer and Bialek in cost words; R8 is classical ruin theory.
- N2: the hold rule makes R3 and R4 necessary only through price-set thresholds (T5). The ruin cap makes R8 necessary price-free, but R8 fails N1. No row meets N1, N2 and N3 together.
- No row is necessary only under a non-physics added premise (the OPEN case). R2's added premise is physics, and R8's unbounded horizon is in I2.
- **Score: MISS** (prior p(HIT) 0.10). Not loosened.
- **Statement (hypothesis, from this class):** the theory constrains worlds only as information theory and ruin theory already do: finite drift, records that last, a net inflow. Locality and a conserved quantity are not implied. This is necessity only; nothing here shows physics arising.
- **Proposed W15-reverse (for `WALLS.md`; not applied here):** "Tracker existence ⇒ world features gives only known information-theory and ruin-theory conditions (finite drift, finite record lifetime, net positive inflow). The cost's own structure adds only price-set thresholds. Locality and conserved quantities are not implied (counterexample: CORE's OU class)." Source: this note §1–§2.

## 3. Hostile review (fresh pass after §1–§2; nothing above edited)

Method: re-read §1–§2 against the locked block, WALLS W1–W14, the two proposed walls, and the cited lines; hunted loosened rules, hidden inputs, overclaims and wrong citations. **Result: MISS stands; four fixes.** Where this section and §1–§2 conflict, this section governs.

- **HR1. One class only.** Every PIM row is shown in the single-item hold-rule class plus one leak term, and R5/R6 counterexamples use CORE's OU class. "Necessary" means necessary in that class. A different class could add conditions, but it could not turn the necessary rows into new ones without leaving T1. Labels stay PIM in-class.
- **HR2. W14 touched.** Acting trackers can lower the drift of what they track (CL11 open; T61). Then R4's \(\sigma^2\) depends on the design and is no longer purely a world property. R4 is stated for trackers that do not steer their world. Fix: that qualifier applies.
- **HR3. R8's necessity comes from my choice of an unbounded horizon in I2.** It was locked, so the score holds. With a finite horizon, R8 is not necessary. Fix: R8 is "necessary under I2's unbounded horizon", as written in the table. It is also W7's input in reserve form, so it moves no wall.
- **HR4. R1 is circular in this route** (I1 sets \(c>0\)). §1 says so. It must not be reported as an output.
- **HR5. "Is it a physics feature?" is my judgment.** The column only matters for HIT/OPEN, and no row passed N1, so the judgment does not change the score.
- **HR6. Citations.** arXiv 2510.25883 and Fields 2018 (10.3390/e20100797, Crossref OK) were read only as search extracts. They are cited only as prior art of the same type, not for any specific result. The Zenodo preprints are not used. C3's numbers come from one price cell and are illustration, not a test.
- **HR7. Does the limit (R2 of NEXT_ROUTES) make the MISS empty?** No. The route could not fail against the world, but it could have found a non-obvious necessary feature. It did not. The value is the W15-reverse wall.
- **Walls touched:** W1 (cleared by direction), W2/T5 (R3, R4 thresholds), W3 (partial: the system and the reserve are presupposed), W5 (R7, re-hit, cited), W7 (R2 cited; R8 in kind), W13/T4 (R1; R6's reserve), W14 (HR2). Proposed W15-candidate (locality stays input) is consistent with R5. Proposed W16-candidate (zero-cost reversible self-tracker) is not touched; no self-tracking was used.
- Banned-word scan: see WORKLOG.
