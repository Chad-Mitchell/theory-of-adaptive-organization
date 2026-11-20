# GRID-1b preregistration: the G2-slow arm on the aFRR-dominated reconstruction

Written Friday 20 November 2026, after GRID-1 came out INVALID by premise (mFRR coverage 0.666) and
**before any spectrum, fit or corner of any 2022 series has been computed**. Same predictions and rules as
GRID-1 DV1 (`PREREG_GRID1.md`, DV1.3–DV1.4); only the data rule changes.

**Known before writing (disclosed):** coverage A_15 0.987; M_15 0.666 (gaps 1 Mar–30 Jun from three TSOs);
corr(A_15, QA aFRR) 0.998; var(M_15) / var(A_15) = 0.7 %.

**Data rule.** Main series D_15 = A_15 + M_15 where M_15 exists, and D_15 = A_15 where it does not
(mFRR contributes < 1 % of variance where measured, so setting it to zero in the gap is a small, stated
approximation). Coverage rule: A_15 ≥ 90 % (as before); the M_15 rule is replaced by: var(M_15)/var(A_15)
< 5 % where measured, else INVALID. Robustness (as DV1.5, kept): the chosen model and slowest corner must
not move by more than ×2 when M_15 is dropped or doubled, else INVALID. Plus one new robustness run: the
same fit on 1 Jul–31 Dec 2022 only (full M_15 coverage); if its chosen model's verdict on G2-slow differs from
the main run's, the result is NEITHER.

**Arms.** G1, G2-fast, G2-mid INVALID in advance (DV1.3). G2-slow and R1-slow as DV1.3: PASS iff a separated
corner with bootstrap CI wholly above 900 s; FAIL iff white in band (K = 0, or power law γ < 0.3); otherwise
NEITHER. R1-slow PASS iff the slowest corner's CI overlaps [450, 1800] s. Discrimination only if the CI lies
wholly above 1800 s. Expected: PASS (low risk; disclosed in DV1.3).
