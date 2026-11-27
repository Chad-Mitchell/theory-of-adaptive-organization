# Conjecture C, round 16: result against the pushed lock

Lock: `PREREG.md`, sha256 `236ebf1de8a0e0037a27d7856be6c129ed1a05037b79f93f64e9f7f6ca23f326`, pushed in commit c6f01f6 at about 05:15 EST on 2026-11-26. The lock was re-checked. The run started at 05:15:41 EST from a fresh clone at c6f01f6 and finished at 05:19:10 EST (exit 0, inside the 90-minute limit).

| Check | Output (`r16_h3.stdout`) | Score |
|---|---|---|
| V1, validity | per-factor classes 6 and 4; 20 canonical distinct K values; smallest gap in floats 1.087e-3 | passed |
| V2, the test | row search: 1 pair tried, 0 automorphisms, 0 undecided; column search: 397 pairs tried, 0 automorphisms, 0 undecided | **hit** |
| V3, consistency | 1 and 397 pairs, as in round 13 | matches |

**Reading.** With exact, canonical classes, no linear automorphism of max(I, D) that fixes facet 0 sends a same-row or same-column partner to a non-partner. Because the local group is transitive on facets, every automorphism therefore preserves the 20 × 12 facet grid. By the argument of §18 it is then a product of local maps. So max(icosahedron, dodecahedron) has no entangling automorphism: PROVED (in-model), an exact certificate for this one maximal composite. It agrees with Al-Safi–Richens Theorem 1 (KNOWN), which already covers maximal composites, so it adds nothing new about C. Its value is that the facet-grid method is now exact and checked on a case where (♦) fails. Rounds 14 and 15 stay scored not tested.

- **Label (27 Nov 2026).** By `process/PREREG_GATE.md:18` (G2) V2 is a CONSISTENCY_CHECK: its outcome is implied by Al-Safi–Richens Theorem 1 (KNOWN), as `PREREG.md:20` states. The exact certificate stays PROVED (in-model); it is a method check, not a hit for C.
