# GRID-3 preregistration: replication and the scope premise

Written Friday 20 November 2026, after GRID-2, **before downloading any 2024 GB data or any 2026 German data**.

**G3a, replication of the GB world finding (new data).** Same code (`grid2_run.py`), same rules, GB 2024, weeks
Monday–Sunday 8–14 Jan, 8–14 Apr, 8–14 Jul, 7–13 Oct 2024, with the 2024 response products (DC/DM/DR) and MFR.
Prediction from GRID-2: power law chosen, γ ∈ [1.7, 2.3] (G1 FAIL replicates). If instead a Lorentzian model is
chosen with K_sep ≥ 2, GRID-2's G1 result is called sample-specific and is reported as NEITHER overall.

**G3b, premise rule for any future layer test (applies from now on).** A system qualifies for (iii) only if
(1) read noise is non-negligible: the measured read-noise variance is ≥ 10 % of the tracked signal's variance at
the layer's own time scale; and (2) ruin is slack: no layer is triggered only by a deviation threshold. Layers
that fail (2) are excluded from the count before scoring. Grid frequency fails (1) (sensor noise ≪ 1 mHz
against tens of mHz of deviation), so grids are out of scope for (iii) under this rule from now on; the GRID-2
FAIL stands as recorded and is not reclassified.

**G3c = GRID-S S2 (locked `8b0ef50`), unchanged,** to run when Chad provides the 2026 German files.


## Dated clarification of G3b's scope (20 Nov 2026, v2.61, review 27 M4; the locked text above is unchanged)
G3b applies only to tests **locked after `b7f69e8`**. G3a was specified as a replication of GRID-2 under the scope in
force when GRID-2 was locked (`36416d2`), so it is scored under that old scope, and its PROXY-FAIL (CLAIM_MAP P21) stands.
G3b's statement that grids fail criterion 1 (read noise ≥ 10 %) was asserted, not measured. Any future use of it to
exclude a grid must measure the read-noise share first.
