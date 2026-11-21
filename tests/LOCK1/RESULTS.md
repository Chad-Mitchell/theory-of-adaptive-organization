# LOCK1 results (in-model, numerical)

*Saturday 21 November 2026, about 1:40 PM ET (America/New_York). Prereg `PREREG.md`, locked in commit `5f9f5be` (sha256 in `PREREG.sha256`) before `lock1.py` existed. Output: `lock1.out`, `lock1.json`. Nothing here is about nature.*

| Row | Verdict | Numbers |
|---|---|---|
| A1, A2 (rational-ratio rhythm worlds: layers at the world's frequencies and ratio) | **FAIL** | layer frequencies off by 3–66%; ratio errors 0.31–1.37 (N = 0.01) |
| B1 (phase layers: optimal ratios farther from p/q, q ≤ 4, than r0) | **FAIL** | mean distance 0.046 / 0.034 / 0.031 vs 0.049 for r0 at Kc = 0.3 / 0.6 / 0.9: the optimum moves *closer* to low-order rationals |
| B2 (≥ 10% more badly approximable) | **FAIL** | +22%, +7%, +37%; fails at Kc = 0.6 |
| B3 (golden/noble selected) | **FAIL** (expected before the run) | golden share 0.093 / 0.113 / 0.000 vs 0.24 needed |
| B4 (linear class: no rational structure) | **PASS** | roughness ratio 1.09, 1.05 |
| D1 (mixed world: resonant layer at the rhythm) | **FAIL** | layer frequency 0.70 vs world 1.00 |
| D2 | **FAIL** | scored as B1 at Kc = 0.6 |

No rescue; the rows stay as scored.

**What the numbers say, in plain words.**
- Where the cost penalizes inter-layer locking (phase model, case b), the cheapest ratio moves just far enough to leave the tongue it would sit in and stops at the tongue's edge. Tongue edges lie near low-order rationals, so the optimal ratios end up *nearer* to simple fractions than the unpenalized ones, not farther. The golden mean is not selected. Anti-locking excludes the tongues; it does not pick badly approximable numbers at any finite coupling tested. That golden-mean tori are the last to break at critical coupling is KNOWN (KAM; Greene 1979; Shenker 1982), and nothing here reaches that limit. Labels: NUMERICAL, in a toy whose redundancy term is an ASSUMPTION.
- In the linear class there is no locking mechanism at all (B4 PASS), so "irrational spacing" cannot come from J there.
- Case (a)'s miss (layers not at the world's frequencies at N = 0.01) was not diagnosed. It is consistent with the repository's known result that reduced-order optimal stores sit on the fast observer-pole side, not on the world's poles (`core/keystone_checks/waterfill_2026-11-20/MATH.md`; PF20 in `theory/PRICE_FREE_2026-11-21.md`), but an optimizer shortfall was not ruled out. OPEN; a diagnostic was started and stopped.

**Scope note.** After the run, the coordinating agent withdrew cases (a) and (c) as unable to fail informatively and asked for a could-it-fail check before (b). The prereg had already been locked and run; the results are reported, not withdrawn. The could-it-fail answer for (b): yes, it could fail and it did. The failure changes one claim: "badly approximable spacing falls out of the cost minimum" is not supported in-model.

Prior art: Kuramoto (1975); Arnold tongues and the sine circle map (Arnold 1965; Pikovsky, Rosenblum & Kurths 2001); KAM and golden-mean robustness (Greene 1979, J. Math. Phys. 20:1183; Shenker 1982, Physica D 5:405); phyllotaxis golden angle (Douady & Couder 1992, Phys. Rev. Lett. 68:2098). The repo's own torus work is `theory/TORUS.md` (N43 PRIOR ART, N45 OPEN, N49 PROVED in-model): there locking to an *outside* cycle is the benefit; LOCK1 is the opposite sign, locking *between* layers as a cost.
