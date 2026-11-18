# THREATS: what could sink, shrink, or embarrass GTAO

Sat 2026-11-14 ET. These are ranked by danger. Citations and DOIs are in `LITMAP.md` and `PRIOR_ART.md`. Items marked *(my reading)* are my analysis, not a published result.

## A. Prior-art threats (novelty)

### A1. Lee, Flack & Krakauer 2024 and the SFI collective-computation program. THE biggest threat.
- **The paper:** Lee, Flack & Krakauer 2024, Proc R Soc B 291:20241606, doi 10.1098/rspb.2024.1606; preprint arXiv 2209.00476, read in full. It derives:
  - a **universal optimal memory scaling τ_m\* ∼ τ_E^{1/2}** for agents tracking a changing environment, with an explicit metabolic memory cost. That is the core of T1 and rule 2;
  - **stigmergy and niche construction as "outsourced memory"**: rule 6 and T4's territory;
  - **environment stabilization as a public good that free riders invade unless it is monopolized**. That cuts against rule 6's "no one in charge".
- **Around it:** Flack 2012 and 2017 (slow variables, coarse-graining, levels from collective estimation) and Krakauer et al. 2020 (the information theory of individuality). Together these cover much of "levels as shared slow memory".
- **Exposure:** a referee from SFI would say GTAO's √ law, cost of memory, outsourced memory and level story are already published.
- **What survives** (see PRIOR_ART):
  - the √N fade with N depositors (T4);
  - the T3a threshold;
  - the temperature identity, the fix-mechanism classes and the fixed-spread sign;
  - T7b (geometric levels iff drift is scale-free; K ∝ L^{2/3});
  - the rise-then-cliff of watching effort (T5);
  - the cross-scale claim made *with tests*.
- **Action:** cite Lee 2024 and Flack prominently, and reframe T1 as "agrees with". Any wording change needs Chad's approval.

### A2. The temperature is the inventory safety factor, turned upside down.
- z = B/(σ√L) is the textbook safety-stock factor (Silver, Pyke & Thomas 2017).
- Merton 1974's distance to default is the same shape.
- Galbraith 1974 and Thompson 1967 made slack-vs-speed a core design tradeoff.
- **What is new:** the elasticity identity (ε_τ = ε_σ/2 − 1), the fixed-spread sign and the fix-mechanism classes.
- **Threat:** presenting the ratio itself as new.

### A3. T1 is a repeated rediscovery.
The same √(2·fixed cost / (flow cost × variance)) form appears in:
- EOQ (Harris 1913; classic, as already cited in THEOREMS, not re-verified here);
- Baumol-Tobin (classic; not re-verified here);
- menu costs and inattention (Reis 2006, d\* = √(2K/G); Alvarez, Lippi & Paciello 2011);
- Kalman (K ≈ √(q/r));
- Lee 2024.

THEOREMS already says this. The threat is any outward claim that implies otherwise.

### A4. Nested levels.
These already say "fast learns, slow remembers" and give geometric spacing:
- Brand 1994/2018 pace layers;
- Holling's panarchy ("remember/revolt") and lumps;
- Simon 1962 (near-decomposability);
- Beer's VSM;
- Benna & Fusi 2016 and Drew & Abbott 2006 (geometric cascades);
- Shankar & Howard 2013 (log-spaced bins optimal for power-law signals: the closest to T7b);
- Murray 2014 (cortical timescale hierarchy).

**T7b's iff, and the 2/3 law, are the only new parts.** Shankar & Howard is a near-miss threat to the "iff" direction.

### A5. Freeze-or-hold and judgment.
- Freeze-or-hold: Bateson 1963 (somatic vs genetic change economy); Waddington 1953 (genetic assimilation); Ashby's ultrastability; Hannan & Freeman 1984; Kirkpatrick 2017 and Dohare 2024 (plasticity loss).
- Judgment ≈ Rosen 1985 anticipatory systems, Richens, Everitt & Abel 2025 (general agents must contain world models) and Still 2012.

## B. Empirical threats (the theory could be wrong)

### B1. The neural slope of about 1 does not fit T1. *(my reading; needs an independent check)*
- BIO1 P5 reads the adaptation slope of about 1 (Fairhall/Wark) as fitting T1's jump-switching form.
- T1's own jump formula gives a check rate ∝ √λ, i.e. an interval ∝ τ_E^{1/2}. Lee 2024 also predicts ½.
- **Slope 1 is an anomaly for single-timescale theories**, and points to scale-free memory (LEFT_ON_THE_TABLE #1).
- If confirmed, P5's wording should change. It does not count against GTAO overall if T7's scale-free branch absorbs it, but that rescue must be preregistered, not used after the fact.

### B2. Observed elasticity to lead time is far below ½.
- Rumyantsev & Netessine 2007 find inventory elasticity to lead time of about 0.11–0.13 in US public firms, against the ½ that the safety-stock square root predicts.
- **Partial excuses:** a cycle/safety-stock mix, measurement in lead-time variability.
- If the temperature's τ exponent fails in its *home* field, cross-scale claims lose credibility.

### B3. Collective forgetting may have a universal form unrelated to drift.
- Candia et al. 2019 fit a universal biexponential to collective attention across media.
- If the decay parameters do not vary with each topic's drift, rule 2's "match drift" fails at the cultural scale.

### B4. Fast fixers are not always safer.
- Hannan & Freeman 1984: selection favours *inertia* (reliability and accountability), and reorganizing raises mortality.
- This cuts against the temperature's "more speed = safer" reading unless the cost of change is modelled.
- Relatedly, lock-in (Arthur 1989; North 1990) means past choices, not current drift, can set memory.

### B5. The drift barrier: optimality has a ceiling.
- Lynch et al. 2016: below a selection-strength threshold, traits drift away from optimum.
- Any test of "efficient design" in weakly selected systems (small populations, protected firms, bureaucracies) should *expect* misses.
- GTAO needs to say where its optimality claims apply, or every miss becomes ammunition.

### B6. Other explanations for "memory" patterns.
- **Immune memory longevity:** Slifka & Amanna 2019 explain antibody durability by antigen multivalency and structure, not by matching pathogen drift.
- **LSM-tree and storage levels** are geometric for pure write-cost reasons, with no drift.
- **Dissipative adaptation** (England 2015, *Nat Nanotechnol* 10:919, doi 10.1038/nnano.2015.250; Perunov, Marsland & England 2016, *PRX* 6:021036; England 2013, *J Chem Phys* 139:121923, is the self-replication heat bound, not the adaptation work; corrected 18 Nov 2026): matter organizes to absorb work from drives without any internal model. That threatens "atoms as agents" if read as requiring prediction.

## C. Structural and methodological threats

### C1. The free-energy-principle trap (unfalsifiability).
- Aguilera et al. 2022 and Bruineberg et al. 2022 argue the FEP is either trivially true or ill-defined at scale.
- A theory of "ANY adaptive organization" with literal physics invites the same charge.
- **Defence:** keep every claim tied to an exponent, a sign or a threshold with a named competitor (MATH_ATTACK's closure conditions C1–C4).

### C2. "Forms are forced".
- MATH_ATTACK already notes that √ forms come from dimensional analysis plus a convex tradeoff.
- Agreement with a √ law is therefore weak evidence. Only the *iffs*, signs and thresholds are diagnostic.

### C3. "No one in charge at every level" overreaches.
Against it:
- the externality result (parts under-watch shared memory; MATH_ATTACK);
- Lee 2024's free-rider result;
- Ostrom (commons need institutions);
- Beer's VSM System 3/5.

Hierarchy and enforcement appear exactly where shared memory is a public good. **Suggest:** "no one *needs* to be in charge *when* shared memory is privately rewarded; otherwise expect enforcement" (needs Chad's approval).

### C4. A missing lever invites easy counterexamples.
- Organizations reduce drift (contracts, homeostasis, niche construction; Thompson's buffering and smoothing; Lee 2024; Lenton 2018).
- Any system that is "under-watching" relative to GTAO may simply have lowered its σ.
- Without a drift-reduction term, misses look like failures.

### C5. Literal physics claims.
- c = kT·(per nat) is a floor. Real systems sit orders of magnitude above it: Kempes et al. 2017 report cells near Landauer within about a few tens ×, and computers and firms far above.
- **Claiming the physics literally:** fine for floors; risky for point predictions.

## D. Short list: what to change (all require Chad's approval for any public wording)
1. **Shrink the novelty claims** for T1, the temperature ratio and the nested levels. Cite Lee/Flack/Krakauer, Reis, safety stock/Galbraith, Brand/Holling, Shankar & Howard, Rosen and Anderson & Schooler.
2. **Add a drift-reduction lever** to the objective.
3. **Condition "no one in charge"** on shared memory being privately rewarded.
4. **Reconcile exponents.** Predict ½ for single-timescale worlds and power-law kernels (slope → 1) for scale-free worlds. Fix the BIO1 P5 reading.
5. **Scope optimality** with a drift-barrier or selection-strength condition.
6. **Lead with what is new:** T4 √N, T3a, the fixed-spread sign, T7b and the T5 cliff.
