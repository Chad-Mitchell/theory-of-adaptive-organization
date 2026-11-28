# THEORY v1.4 sub-check (same executor, reread after writing; not independent)

15 Nov 2026, about 10:00 AM ET. New THEORY.md reread against `measurement/CLAIM_MAP_v2.md` (v2.3), `reviews/night2/SPECTRUM_MAP_REFEREE.md` (§§1–9) and `reviews/night2/LEARNSIM_REFEREE.md` (§§7–8). Every CLAIM_MAP row cited in THEORY.md was looked up by script and its status compared with the THEORY wording.

Inconsistencies found and fixed before merge:
1. Status block counted "four" locked in-model fails; CLAIM_MAP has six SIM-FAIL rows (G6, G9, G15–G17, G20). Fixed to six.
2. §2.2 regime-B rows lacked α ranges (read-rate result is fBm only, 1 < α < 3; bandwidth α > 1; kernel 0 < α < 4). Added per row.
3. §2.3 said the physics matters "exactly insofar as it fixes θ"; N12 only covers the onset exponent and assumes the technology is known. Narrowed.
4. §8 "special case of the spectrum relation" and §8c "spectrum core" used superseded framing. Reworded.
5. SG's label "application" (Ferragut et al. 2018) was stated as settled, but CLAIM_MAP N8 is unchanged and the relabel awaits the SG referee. Marked as pending.
6. Field-language: §4, §8 (DECISIVE glucose/populations, COLLAPSE1) and README said "falsified"/"killed" for proxy results. Relabelled "failed on proxy", citing K4/H17/H18.
7. "law" wording for the √ scaling (Kalman/LFK) replaced; remaining uses are "power law" (mathematics), "second law" (physics) and none refers to GTAO.

Checked, no change needed:
- The vigilance formula's "/(rρ)" (LEARNSIM referee §7 suspected a typo): it matches `reviews/night1/REVIEW_MATH.md` and CLAIM_MAP_FINAL E6, with r = p_g/p. THEORY §6 now defines r.
- Every citation added in §10 appears, with the same bibliographic details, in `SPECTRUM_MAP_REFEREE.md` or `SPECTRUM_MAP/README.md` / `priorart/NOTES.md`. None was added from memory.

Unresolved (queued): N12 is self-checked only (ONSET-SPECTRUM-FREE-REFEREE); SPECTRUM_MAP README items 2–8 (SPECTRUM-MAP-FIXES); frozen files still state superseded forms (FROZEN-DOC-POINTERS).
