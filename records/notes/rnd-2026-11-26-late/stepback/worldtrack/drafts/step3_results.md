
## Step 3. STORED-PEAK: results (computed after the Step 3 pre-statement hash was logged; appended 26 Nov 2026, 2026-11-26T20:01:48-05:00)

*Timing note:* the §3 pre-statement header says "19:1x". The WORKLOG entry is 19:09, and the hash after it is `084ea69e…b473`. The Gaussian run and the register run (`worldtrack/sp_gauss.py`, `worldtrack/sp_reg.py`) were started after that entry. The register run finished at about 20:00 ET (`sp_reg.log`, "ALL DONE").

### 3.6 Results per configuration (OBSERVED, in-model, numerical)

Files: `worldtrack/sp_gauss_analyse.out` and `worldtrack/sp_reg_analyse.out`, made by `sp_analyse.py`. A "blind" cell is one whose optimum is never to look (I = 0); U1 is not scored on blind cells. Each configuration has 432 cells.

**G: CORE's class (Gaussian looks)**

| s_min | c | U1 fails | U2 holds | edge |
|---|---|---|---|---|
| 1 | 0 (keep charged on write, primary) | **52** (12.0%) | 432/432 | 0 |
| 1 | 0 (cycle-averaged keep arm) | **130** (30.1%) | 432/432 | 0 |
| 0.1 | 0 | **133** (30.8%) | 432/432 | 0 |
| 0.01 | 0 | **223** (51.6%) | 432/432 | 0 |
| any | 0.1 | 0 | 432/432 | 0 |
| any | 1 | 0 | 432/432 | 0 |
| any | 10 | 0 | **422/432** (97.7%) | 0 |

**Reg: Step 1's register (primary timing a = 0, c_K = 2)**

| s_min | c = 0 | c = 0.1 | c = 1 | c = 10 |
|---|---|---|---|---|
| 1 | U1 0; U2 422 (97.7%) | **U1 6 (1.39%)**; U2 418 (96.8%) | U1 0; U2 430 | U1 0; U2 431; 1 blind |
| 0.1 | U1 0; U2 427 (98.8%) | U1 4 (0.93%); U2 422 (97.7%) | U1 0; U2 430 | U1 0; U2 427; 1 blind |
| 0.01 | U1 0; U2 422 (97.7%) | U1 0; U2 430 | U1 0; U2 432 | U1 0; U2 432; 1 blind |

There are no edge cells in either class. The three blind register cells are all at σ_w = 0.3, x = 1, Γ = 0.1, c = 10.

### 3.7 Score: **MISS** (by the rule fixed in §3.3)

U1 fails in more than 1% of cells in five configurations:
- G at c = 0, in all four of its c = 0 configurations (12–52%);
- Reg at s_min = 1, c = 0.1 (6 of 432 = 1.39%).

U2 alone would have given OPEN, not MISS: its worst configuration is 96.8%, which is at least 95% but below 99%. My pre-stated p(HIT) = 0.8 was wrong.

As fixed in §3.4, **the template claim of §3.4 is not stated.**

### 3.8 What the failing cells are (OBSERVED; diagnostic, post hoc, not a rescoring)

- **G, U1 failures at c = 0: flat in the look interval, not in stored information.**
  - Across all 583 competing minima, none differs from the global one by more than a factor 1.2 in P₊. The largest P₊ ratio is 1.118, which is ΔI ≤ 0.056 nats (`sp_diag.out`).
  - Each failure is a second minimum more than 1.2× away in s, within 1e−3 of J_min.
  - Example: σ_w = 0.001, s_min = 1, x = 100, Γ = 0. Here J(s_min) = 0.0100034 and J(s = 10) = 0.0100052, a relative difference of 2e−4.
  - With no per-look price, the cost is nearly flat in s once looks are cheap enough. This is the same fact Step 2 found: the look rate is not set by the world.
- **Reg, U1 failures at c = 0.1: adjacent integer look intervals.**
  - All 10 failures are a second minimum at the neighbouring integer s (3 against 4), with n within a factor 1.09. The largest gap is ΔI ≤ 0.091 nats.
  - The 1.2× rule trips on s (4/3 > 1.2), not on the design.
- **G, U2 failures at c = 10 (30 cells, all σ_w = 0.3, x ∈ {1, 3}): two local minima in the profile.**
  - One minimum is at the blind end (I = 0); the other is interior.
  - The global minimum is always the interior one. For example, at x = 1, Γ = 1e−5: J = 0.933 at I = 2.09, against 1.645 at I = 0 (`sp_diag2.out`).
  - This is a genuine second local minimum, created by a high per-look price at a weak stake.
- **Reg, U2 failures (61 cells): double minima in the profile from integer s.**
  - Six cells were checked in `sp_diag3.out`. All six keep two minima with an all-integer s grid up to 1e5, and their relative gaps are ≤ 7.1e−4 (e.g. n = 906 against 920, J differing by 7.6e−5 relative).
  - The other 55 cells were not checked one by one. That they share this cause is HYP.

### 3.9 Paper part (PIM, ELEMENTARY; as pre-stated in §3.3)

- **Model.** In the continuous-look limit of class G, take the keep floor as charged on the decision error ε, with I = ½ ln(v/ε). The cost rate is
  J(ε) = kT·a(v − ε)/ε + (c_K·Γ/2)·ln(v/ε) + w·ε.
  - The first and last terms are the source formula of `theory/INFO_PHYSICS_ATTAINABILITY.md`: the Kalman rate at :30, the heat infimum at :35, and J at :44–47.
  - The middle term is the keep floor added by this note (a chosen class element, §2.11).
- **Proof.** J''(ε) = 2kT·a·v/ε³ + c_K·Γ/(2ε²) > 0 on (0, v]. This was checked symbolically with sympy: (c_K·Γ·ε + 4kT·a·v)/(2ε³), with kT = k. So J is strictly convex, and its minimiser ε*, and hence I*, is unique. It is either interior or at the blind end ε = v (I* = 0).
  - At Γ = 0 this reproduces the source's unique ε* (:44–47).
- **Scope.** This covers the continuous-look limit only. With discrete looks and a per-look price, §3.8 shows a second local minimum can appear (G, c = 10). The convexity does not extend there.

### 3.10 The stored-information claim, as it may be quoted

The claim must not contradict review point 4 (REVIEW_WORLDTRACK §6): across classes only the σ_w√x cost scaling is supported, and it is KNOWN (Berger 1970). The pre-registered template is not quoted (§3.7). What may be quoted:

> **(PIM, ELEMENTARY; in-model, Part 1 only.)** *In the continuous-look limit of CORE's OU class, with look heat at its floor and a keep floor proportional to the stored information, the cost rate is strictly convex in the decision error, so the stored-information optimum I\* is unique: interior, or zero (do not look).*
>
> **(KNOWN, Berger 1970 via Kipnis–Goldsmith–Eldar 2019, eq. 4.)** *Across classes, only the cost scaling J ∝ σ_w√x is supported.*
>
> **(OBSERVED, in-model, numerical; post hoc, not a test result.)** *With discrete looks, uniqueness of the joint (design, look-interval) optimum failed the pre-stated test (MISS): without a per-look price the cost is flat in the look interval, and integer look intervals give near-ties. Even so, in every failing cell the competing optima agreed in stored information to within 0.06 nats (Gaussian) and 0.09 nats (register). With a high per-look price and a weak stake, a second local optimum at "do not look" appears; it was never the global one in the grid.*

Not claimed:
- that the value of I*, or its exponents in x, σ_w and Γ, carry across classes. The ¼ ln x − ½ ln σ_w form restates the σ_w√x scaling (§4.4 below), and it is class-dependent in its constant;
- anything about a real system. The claim also covers no QM, GR or gravity.

### 3.11 Inputs (as found)

No new chosen inputs. These carry over unchanged:
- the class choices in §1.11 and §2.11;
- the keep floor charged on the stored information;
- the grids of §3.2;
- the time rescaling for sub-tick sensors in the register (§3.2; exact for that model, every cost being per tick).

### 3.12 Labels (Step 3)

| Statement | Label |
|---|---|
| Score MISS; the counts in §3.6 | OBSERVED (in-model, numerical) |
| Causes of the failures (§3.8) | OBSERVED for the diagnosed cells; HYP for the 55 register U2 cells not checked one by one |
| Strict convexity and a unique I* in the continuous-look limit | PIM (ELEMENTARY) |
| J ∝ σ_w√x across classes | KNOWN (Berger 1970; KGE 2019 eq. 4) |
| The stored-information coordinate agrees within 0.06 / 0.09 nats | OBSERVED, post hoc |
| I* is class-independent | Not claimed |

### 3.13 Hostile self-review of Step 3: **PASS-WITH-FIXES**

1. **Was the test too strict?** Possibly: U1 counts a near-tie in s as non-uniqueness even when the stored information agrees. But it was fixed before computing, and it is the rule Step 1 passed with. Loosening it now to get HIT would be rescoring after the fact, so it is not done. **Fix (proposed for any rerun, pre-stated anew):** score uniqueness in I separately from uniqueness in s.
2. **Sub-1% U1 in Reg at s_min = 0.1, c = 0.1 (0.93%).** This is below the MISS threshold but still not HIT. It is reported, not hidden.
3. **The register's U2 causes are only partly checked** (6 of 61 cells). That they are integer artefacts is stated as HYP.
4. **The paper part charges the keep floor on ε, not on the posterior variance just after a look.** In the continuous-look limit the two coincide, so this is consistent with Step 2's "write" arm only in that limit. Stated in §3.9.
5. **The c = 10 blind-end minimum is real, not a grid artefact.** It shows the profile in I is not unimodal in general with discrete, priced looks. The quotable claim confines uniqueness to the continuous limit for this reason.
6. **The §3.4 template's cross-class exponents would have contradicted review point 4.** They are withdrawn in §3.10 whatever the score.
7. **Wording scan** for the banned words: done before hashing (WORKLOG).

### 3.14 Next step (proposed; nothing run)

- Re-pose STORED-PEAK with a fresh pre-statement that scores uniqueness in I (the profile) separately from s.
- Add an event-triggered read arm, following the §4.9 prior art (Åström–Bernhardsson; Rabi–Moustakides–Baras), after reading those papers' content.
