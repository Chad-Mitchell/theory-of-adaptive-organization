# GRID-4 preregistration: are GB's layer times set by actuation or by the world? (natural experiment, 2019/20 vs 2026)

Written Friday 20 November 2026, about 10:58 AM ET, **before downloading or inspecting any GB data from 2019 or
2020** (and before G3a's 2024 data). This tests the post-hoc diagnosis of the GRID-2 miss (`RESULTS_GRID2.md`,
candid note), so it can fail.

**The two accounts.**
- **A (actuation-limited, the diagnosis):** product time constants are set by what the delivering technology
  can do (inverter-based batteries ≈ 1 s; governors ≈ 10 s; thermal ramps and quick-start minutes) and by
  the energy duration it can sustain. Layer times change when technology changes, whatever the world does.
- **W (world-set, Master Theorem (iii) with interlacing):** layer times sit between the world's imbalance modes
  and change when the world's spectrum changes.

**The natural experiment.** GB's fast layers changed tenfold with technology: before October 2020 the fastest
products were primary response (full in 10 s) and secondary response (30 s), from governors and the dynamic
FFR fleet; by 2026 they are DC/DM (1 s, batteries) and DR (10 s). If W were right, the world's fast imbalance
spectrum must have changed about tenfold too (fast modes ≈ 10× faster in 2026). If A is right, the 2019/20
spectrum looks like 2026's.

**Data and method (fixed now).** Two Monday–Sunday weeks before DC: 7–13 Oct 2019 and 6–12 Jan 2020 (14
days). Same reconstruction and fit as GRID-2 (`grid2_run.py`, DV-GB1), with these changes forced by the
period: no DC/DM/DR (they did not exist); response R = Q·lag₁₀/₃[g(−Δf)], g linear from ±0.015 to ±0.5 Hz,
with an assumed total holding **Q = 1,500 MW** for both directions. That figure has **no source**; it is covered
by robustness at Q × ⅓ and × 3. Inertia from NESO `system-inertia` 2019-20; BM from Elexon BOALF and PN.
Compared with 2026 (GRID-2 main: power law, γ = 2.09; local slope 1.48 at 2–60 s).

**Rules.**
- **A PASS** iff the 2019/20 main fit chooses the power law with γ ∈ [1.79, 2.39] **and** the 2–60 s local slope
  is within ±0.3 of 1.48 (spectrum unchanged while layer times changed ×10).
- **W PASS** iff the 2019/20 main fit chooses a Lorentzian model with a separated corner whose bootstrap CI lies in
  [10, 300] s (a fast mode about ten times slower than the 1–30 s scale 2026 layers face), **or** the 2–60 s
  slope differs from 1.48 by more than 0.5.
- Both or neither: NEITHER. **INVALID** if the verdict changes under Q × ⅓ or Q × 3, or coverage of frequency
  or inertia is < 90 %.
- **What fails A:** a clearly different 2019/20 fast-band spectrum (W PASS). **What fails W:** an unchanged one.

**Disclosed.** I know the product history above and the 2026 GB result. I have not seen any 2019/20 frequency,
BM or inertia values. A known confound: 2019/20 had more synchronous generation (higher inertia), which damps
frequency but is removed by the inertia term of the reconstruction; if the reconstruction is wrong, the fast
band is where it would show.
