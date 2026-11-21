# ECOLI-MEM deviations from the locked files

1. **Riccati cross-check (8:22 AM ET, first run).** The locked `arm_a_poles_riccati` integrated the filter Riccati
   equation by explicit Euler; at the box centre r ≈ 10⁻⁸ s the equation is stiff and it overflowed (NaN) before any
   output was written. Replaced by `scipy.linalg.solve_continuous_are` for the same equation. This is an independent
   check of the arm-A poles only; no prediction formula, input, range or verdict rule changed. The locked version is in
   git at commit 6903de9.

2. **DV2: objective must be named (20 Nov 2026, about 2:50 PM ET; branch `v2.9-dynamics`; THEORY CT42,
   `theory/DYNAMICS.md` §3; before any new E. coli data).** Any future E. coli qualification (THEORY §3 (a)–(e)) or
   preregistration must state, before data are opened: (i) the objective selection is taken to act on, either per-cell J
   through the cost-to-fitness map or lineage growth G (geometric across generations, arithmetic within one) with its
   shared-shock structure named; (ii) the compared statistic, which is per-cell values, the population mean, or the
   distribution across cells. Reason: where shocks are shared within a generation, the lineage optimum can be a
   distribution of designs (bet-hedging; for E. coli, persister switching is read this way by Kussell et al. 2005, doi
   10.1534/genetics.104.035352, and chemotaxis protein-level diversity is proposed as selectable by Frankel et al. 2014,
   doi 10.7554/eLife.03526). The mean of such a distribution need not equal the per-cell argmin, and per-cell J would
   read the spread as scatter or as a miss. **No locked file, prediction, range or verdict changes.** P1–P16 keep their
   statuses; they were scored under per-cell J, and that is now stated as their objective.
