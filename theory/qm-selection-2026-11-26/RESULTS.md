# Results: the U(2) / Sp(1)×Sp(1) counterexample search under the frozen premise list

*Thursday 26 November 2026 (America/New_York). Append-only. Prereg `theory/qm-selection-2026-11-26/PREREG.md`, sha256 `c4a529c7a3c26923763f7bd7c231ccb243bbbbbff57cd9309becc469465a95f0`, lock commit `06f07e6`; script `search_u2_sp1sp1.py`, sha256 `b9bf90eba3a3a231fb31850eb5ef842423633104b53126ec073ccd4f7a90779a` (re-hashed before the run, matching). Scored run: 01:48:13–01:48:53 ET on the author's machine, after the lock commit; output `search_u2_sp1sp1.out`. As disclosed in `PREREG.md` §0, a development run had been made before the lock, so this is not a blind result, and no separate gate reader read the prereg before the run.*

## Outcome: MISS (no counterexample)

No U(2) or Sp(1)×Sp(1) transitive body of affine dimension 4–8 satisfies P1–P5 (under the group rule P4) and ties or beats complex quantum theory on the dimension price P6 without the Jordan premise P7. Under the HIT rule of `PREREG.md` §2: **0 hits, 0 ties.**

| body | group (acting as) | affine dim | SFP | hSFP | capacity | Jordan | outcome |
|---|---|---|---|---|---|---|---|
| B4 | U(2) or Sp(1)×Sp(1) on C² = H | 4 | fail (−1 fixes no pure state) | – | 2 | yes (spin factor) | MISS |
| Z2, spin-2 zonal | SO(3) | 5 | pass | **fail** (equator circle face) | 3 | yes (real QM d = 3) | MISS |
| Z3, spin-3 zonal | SO(3) | 7 | pass | pass | **2** | no | MISS on cost (dim 7 > 3) |
| K_θ, spin-1 ⊕ spin-2 zonal, 9 values of θ incl. C1 | SO(3) | 8 | pass | **fail** (equator circle face) | – | no | MISS |
| B3 × B3 | SO(3)×SO(3) | 6 | pass | pass | **2** | no | MISS on cost (dim 6 > 3) |
| B3 × Z2 | SO(3)×SO(3) | 8 | pass | **fail** ({a} × circle face) | ≥ 3 | no | MISS |

**Labels.**
- The reduction to this list (`PREREG.md` §3.1): **PROVED (in-model)** from the KNOWN maximal-torus criterion and the weight theory of U(2) and Sp(1)×Sp(1); the weight count is checked numerically (S1 of the output). Not formalized in Lean.
- hSFP failure of K_θ (every θ ∈ (0, π/2)), Z2 and B3 × Z2: **PROVED (in-model)**: −P2(cos ϑ) has its unique maximum on the equator, so the invariant functional (0, −Y20) exposes the convex hull of a circle of distinct pure states, on which rotations about the axis fix none. **OBSERVED (numerical)** at nine values of θ (64 distinct pure states on the circle; gap to the poles 0.075–1.496).
- hSFP pass of Z3 and B3 × B3, and capacity 2 of both: **PROVED (in-model)** by the arguments in §3.3–3.4 (normal-cone averaging; central symmetry). Numerically: +Y30 is maximized only at the pole (the largest value over latitudes |z| ≤ 0.99 is 0.9407 of the maximum); the LP found 2 but no 3 perfectly distinguishable states among 200 random grid triples for each. The central-symmetry residual 8.3e-6 printed for Z3 is the sampling error of the grid centroid, not an asymmetry: φ₃(−n) = −φ₃(n) exactly for odd degree.
- Control: for a generic spin-3 vector, 60 of 60 random rotations fix no sampled orbit point (OBSERVED (numerical)), as the criterion requires.

## What this does and does not show

- **Does:** for these two groups in dimensions 4–8, P1–P6 already exclude every non-Jordan candidate, so the Jordan premise P7 is not doing the selection there. The bodies that pass hSFP outside the Jordan class (Z3, B3 × B3) are centrally symmetric and so have capacity 2, which the 3-ball beats on dimension.
- **Does not:** say anything about other groups (SU(3), Sp(2), G₂, products with larger factors) or about dimensions 9–15, where complex QM at capacity 3 (d = 8) and 4 (d = 15) could be tied or beaten. It does not derive P1–P6, the group rule P4, or the dimension price. The chain still reaches quantum theory through premises (structural open miss, errata §7).
- **Next (G5, miss branch):** the same search for rank-2 and rank-3 groups (SU(3), Sp(2), G₂) up to dimension 15, under the same frozen list. An independent reader should check `PREREG.md` §2–§3 and this file.

## Deviations

None from the locked method. The two process deviations (development run before the lock; no separate gate reader) are disclosed in `PREREG.md` §0 and are not repeated in a `DEVIATIONS.md`.
