# Forces & gravity thread: one-page summary (G1–G5, 25–26 Nov 2026, private R&D, not in the repo)
Labels: **PIM** proved in model · **OBS** observed numerically · **CHOSEN** put in by hand · **MISS** open miss · **KNOWN** published, DOI checked on Crossref. Full detail is in `NOTE.md` and `ATTEMPTS.md`, and the numbers are in `outputs/`. Quantum states (TFIM, free fermions, Bloch records) are inputs throughout. Nothing here derives QM, GR, holography or gravity.

| Round | Proved-in-model / observed | Chosen (input) | Open miss |
|---|---|---|---|
| **G1** forces, area, dimension, time | PIM: repeated comparison of frames forces an edge transport variable, and minimal description depends only on holonomies (gauge-invariant). OBS: a quadratic/KL mismatch gives the Wilson plaquette, but for qubit records only the **adjoint** SU(2) one. OBS: record content of gapped or thermal states follows area; tensor-network min-cut equality (KNOWN). PIM: Page–Wootters record formation orders clock ticks; the direction comes from the blank-memory boundary. OBS: CT18's 1/z is an Arrhenius temperature for OU, not for Poisson reset. | gauge group; loss function; exp(−β·cost); the gap; the boundary condition | dynamics and matter; fundamental rep; universal η; Rindler horizons, Unruh T, equilibrium; dimension = Bloch-ball dimension (Müller–Masanes's input) |
| **G2** tracker, Jacobson 2016, selection, thermal time, coverage | KNOWN, applied: exp(−β·cost) from the selection price D(s‖p0). PIM: the JP-heat efficiency sup is g/(g+r), so equality needs fast memory. PIM: an interference read sees ½Re tr U for every SU(2) probe. KNOWN: underdamped Gibbs at kT = σ²/2γ = thermal-time T, given the symplectic split. Coverage table (ASR 2015 Thm 1, MMPA 2014). | KL as price, uniform p0; fundamental probe + linear readout; MPS format | χ* bounded in N (HYP); FNW gap (HYP); T = ħ/2π, boost K, geometric variation |
| **G3** 2D record, 2nd-order sign, centre, wedge | OBS: the MaxEnt record from local reads has perimeter mutual information even for area-entangled worlds (L ≤ 20). PIM+OBS: F_K(ρ′) − F_K(ρ) = T·D(ρ′‖ρ), so the cost minimum and the entropy maximum agree at the Gibbs step. OBS: the SU(2) centre carries stakes only for spin-½ probes plus interference reads plus stakes > cost. OBS: BW-linear modular K at a lattice cut (KNOWN result reproduced). | local two-point reads; TC as capacity; the vacuum; a cut put in by hand | why reads end at a causal horizon (needs relativity); CT18 ↔ modular T |
| **G3-1b** (prereg) | **FAILED as written** (P1 everywhere; P2/P3 Haar; P4 small N). Diagnosis: Haar local correlations fall as N^−½ | — | intensivity in a fixed price |
| **G4** (prereg) horizon from capacity; one-currency intensivity | G4-1 **primary FAILED**: basis-free capacity gives partner modes with ~1/r tails and no cut. Per-site pricing (secondary): sharp cut, R ∝ κ^−0.49 (critical) / κ^−0.28 (gapped), BW slope 0.986 at the gapped cut; H3 failed (double-precision ceiling). G4-2: Q1 r* stable in all 4 worlds; Q2 **FAILED** for W2. | per-site pricing = locality | horizon from cost alone |
| **G5** (prereg) precision-safe H3 | m = 0: **setup miss** (the reference ring had 298/600 filling, so the tolerance was unattainable). m = 0.3: **FAIL as predicted** (T_c ∝ κ^0.27). Q2-ext W2 N = 800: **PASS** (< 6%). Post hoc, unscored: critical T_c ∝ κ^0.465, T_c·R ≈ 0.60 vs 2/π. | per-site pricing; vacuum | T = a/2π; κ^½ universality |

**Preregs and locks** (all re-hash intact, 02:05 EST):
- `PREREG_G3-1b.sha256` `0575b2ea9c37942223250ceca2ba43a4d9431a2f7df9f16ea1fb4612506e2f05`
- `PREREG_G4.sha256` `504704d9c8433cc6e010b5a28c89f06523c5fb8eda3fcec128381680b39ddf8b`
- `PREREG_G5.sha256` `419a6a681ec48bf8e9371f3ae3d852d87f414dd11d99d9e3cccc7105ff61b0d6`

**Fails recorded, none patched:**
- G3-1b P1–P4.
- G4-1 H1/H2/H3 for scheme B; H1/H2 for scheme A at m = 0, κ = 0.001; H3 for scheme A.
- G4-2 Q2 for W2.
- G5 m = 0 setup miss and P5c.
- Errata: the G4-1 massless world had 298/600 filling (scores stand); the G3-4 / G4-1 double-precision ceiling.

**Hostile-review corrections applied** (`HOSTILE_REVIEW_G2.md` → NOTE "R2 errata", append-only):
1. R2.1 "forced" became "MPS format plus HYP"; FNW became HYP.
2. R2.2 now reads "same form as Jacobson 2016 eqs 14–16; β = q/λ is a free ratio".
3. The Gibbs form is forced only **given** KL, linear cost and uniform p0 (a χ² price gives a linear form). The citation was corrected to selfref R5.1/R5.5, not NA4.
4. The SU(2) interference statement holds for every probe; the representation is chosen through the probe and the readout.
5. JP-heat: the σ_M figure is restricted to dE = 1; sup efficiency g/(g+r); "equilibrium input" became HYP.
6. The circular KMS check was dropped; equipartition is reported with s.e.; CT18's hazard form holds only for γ/ω → ∞.
7. The coverage table was split by composite type, using ASR Thm 1 and the R12-M.9 Φ values.

A separate foundations review corrected §0: quantum-like records rank cheapest **only under the continuous-drift premise CD**.

**Honest bottom line:**
- **What the cost supplies:**
  - The exp(−β·cost) (Gibbs) weighting, given KL as the selection price.
  - Under per-site pricing, a boundary whose position the price sets (R ∝ κ^−0.46 critical, κ^−0.27 gapped). Through R that boundary sets the tracker's modular temperature, T_c ≈ c/R.
  - Gauge-invariant (holonomy-only) record cost once frames are compared.
  - Intensivity of the optimal record range when error and capacity are priced in one currency (bits).
- **What stays input:** locality (per-site storage, local reads), the vacuum state, relativity (light cones, boosts), the representation (fundamental vs adjoint, via the probe), the gauge group, T = a/2π (ħ, c, acceleration), and G (a universal η).
- Basis-free capacity pricing does **not** make a horizon.
- Nothing is ready to fold into a PR without a fresh-clone rerun and review. Candidates are the gauge-invariance PIM, G3-2's identity, and the G4-1 negative.

## Corrections after HOSTILE_REVIEW_G3G5 (append-only)
Everything above stands as written; where it conflicts with this section, this section governs. Detail is in `HOSTILE_REVIEW_G3G5.md`, and the errata E-G3G5-1…13 are in `NOTE.md`. No lock was broken and no prediction or threshold was changed. Every scored number reproduces from a fresh copy.
- **T_c ≈ c/R is not something the cost supplies** (E-G3G5-1).
  - Remove it from "What the cost supplies". It is a post-hoc, unscored observation. The scored G5 outcome for m = 0 is a setup miss.
  - The cost supplies only a stopping radius R(κ), where the next site's marginal mutual information falls below κ [OBS].
  - The step from R to T is the vacuum's: Bisognano–Wichmann / Hislop–Longo for an interval, an input. The κ exponent of R also comes from the vacuum's correlation decay.
  - For the gapped vacuum, c/R is withdrawn. T_c·R_eff drifts 0.544 → 0.515 over R_eff = 3.5–16.5, with ξ ≈ 6.7.
- **298 → 300** (E-G3G5-2).
  - On the periodic N = 600 ring, one of the two E = 0 modes is occupied, so the ring holds 300 particles. The density is staggered by ∓1/N, which is the logged 1.67e−3.
  - The setup-miss ruling and "tolerance unattainable at N = 600" stand. The G4-1 "scores stand" is confirmed on an antiperiodic N = 600 rerun.
  - This applies to the G5 row, the Fails list and the G4-1 erratum line above.
- **W2 intensivity is a hypothesis** (E-G3G5-4).
  - W2 is one random sample per size. κ_c(1) spans 0.58–0.79 at N = 200 across five seeds, wider than the 10% bar.
  - The G4-2 Q2 fail and the G5 Q2-ext pass are both within seed noise. The scores stand but say nothing about size dependence.
  - "W2 has nearly intensive local data" is [HYP].
- **Critical "sharp cut"** (E-G3G5-5).
  - Limit it to the gapped vacuum (sharp at every κ), or to unscored κ ≥ 0.01 in the critical vacuum (κ ≥ 0.003 on the zero-mode-free ring).
  - At the scored κ = 0.001 the critical edge is ragged and H1 fails. The κ^−0.49 exponent fits the half-width, ragged points included.
- **Timestamps** (E-G3G5-6).
  - Worker-stated clock times and run durations are not evidence. "02:05 EST" is impossible, since those files were last written at 01:52–01:53. The "~12/15/5 min" durations were really seconds.
  - File birth times and mtimes govern. By those, every lock predates its run (+30 s, +13 s, +32 s).
- **G4-2 Q1 grid gap** (E-G3G5-7). The κ grid has no point in (0.3, 1), and every κ_c at N ≥ 100 lies in (0.41, 0.996). Q1's pass is low-power: read it as "κ_c stays inside (0.3, 1)".
- **Wording fixes** (E-G3G5-8, -10).
  - T_local = v/(2πx) = a/(2πv), equal to a/(2π) only with v = 1. The script uses v = 2.
  - Read G3's "only for spin-½ probes" as "half-integer-spin probes (only spin-½ was sampled)".
  - Read "a read linear in U" as "a read of odd degree in U".
- **Also** (E-G3G5-9, -12): the G3-2 identity is the Gibbs variational principle [KNOWN], and its link to Jacobson's sign is form only. Read "power-law tail" as "algebraic (~1/r) tail".
