# Hostile review of forces-gravity rounds G3, G4 and G5

Date: Thu 26 Nov 2026, 01:54–02:25 EST (box clock, America/New_York). Reviewer: fresh-context hostile referee. Private R&D note, not in the repo. No git, no posting, no email. The worker's files were not edited, apart from append-only erratum lines at the end of `NOTE.md`. THEORY.md and CORE.md were not touched. I also added one line to `WORKLOG.md`.

Material reviewed: `THREAD_SUMMARY.md`; `NOTE.md` (Round G3, R2 errata, G3-1b, G4, G5); `PREREG_G3-1b.sha256`, `PREREG_G4.sha256`, `PREREG_G5.sha256`; `scripts/g3_*`, `g4_*`, `g5_*`; `outputs/`; `ATTEMPTS.md`; `WORKLOG.md`. For the standard expected I used `HOSTILE_REVIEW_G2.md` and `../HOSTILE_REVIEW_FOUNDATIONS.md`.

My files are in `review_g3g5/`:
- `zero_mode_check.py` / `zero_mode_check_out.txt`: filling and density of the N = 600 reference ring.
- `g4_1_anti.py` / `g4_1_anti.txt`: G4-1 rerun unchanged, except that the world is the antiperiodic N = 600 ring (exactly 300 particles, no zero modes).
- `q2_seed_noise.py` / `q2_seed_noise_out.txt`: the spread of κ_c(r) from one W2 sample to the next.
- `reruns/`: fresh-copy reruns of the worker's scripts, which I ran from `/tmp`.

Labels: **[OBS]** observed numerically · **[HYP]** hypothesis · **[PIM]** proved in model · **[KNOWN]** published, DOI checked on Crossref.

## 0. Bottom line of this review
The thread's bottom line mostly survives. It has the following parts:
- Basis-free capacity pricing gives no horizon. This was preregistered, it failed honestly, and it reproduces.
- Per-site pricing places a boundary whose size the price sets.
- The BW/Unruh form at that boundary comes from the vacuum and relativity, which are inputs.
- The κ^½ temperature scaling is not established by any scored test.

I found no changed prediction, no changed threshold and no broken lock. Every scored number reproduces from a fresh copy.

Three things need errata:
1. **The summary's "what the cost supplies" list includes T_c ≈ c/R as if it were a result.** It is a post-hoc, unscored observation, and the step from R to T is supplied by the vacuum (BW for an interval), not by the cost.
2. **The G5 setup-miss diagnosis gives the wrong particle count.** The zero-mode mechanism is confirmed, but the ring holds 300 particles with a staggered density, not 298.
3. **The worker's stated clock times and run durations are unreliable.** "02:05 EST" is impossible. Run lengths were overstated about 100× against the file times. Box file times and WORKLOG are self-consistent, and they show every lock predating its run.

## 1. Integrity checks

### 1a. Lock hashes [confirmed intact]
I recomputed sha256 over each declared span of `NOTE.md`, from the heading line up to the line before the lock line, joined with `\n` (each span ends with the blank line before its lock line); re-checked again after my errata were appended:

| lock | declared span | recomputed | match |
|---|---|---|---|
| `PREREG_G3-1b.sha256` | `# G3-1b PREREGISTRATION` … the line before `**Lock:**` | `0575b2ea9c37942223250ceca2ba43a4d9431a2f7df9f16ea1fb4612506e2f05` | yes |
| `PREREG_G4.sha256` | `## G4-1 PREREGISTRATION` … the line before `**G4 lock:**` | `504704d9c8433cc6e010b5a28c89f06523c5fb8eda3fcec128381680b39ddf8b` | yes |
| `PREREG_G5.sha256` | `## G5 PREREGISTRATION` … the line before `**G5 lock:**` | `419a6a681ec48bf8e9371f3ae3d852d87f414dd11d99d9e3cccc7105ff61b0d6` | yes |

So the prereg text has not changed since each `.sha256` file was written.

### 1b. Did each lock predate its run? [confirmed, from file birth times]
| lock file written | first script / output of that round created | gap |
|---|---|---|
| G3-1b 01:15:11 | `g3_1b_prereg.py` and `outputs/g3_1b.txt` born 01:15:41; `g3_1b_p4_qubit.py` 01:15:58 | +30 s |
| G4 01:31:37 | `g4_2_intensivity.py` / `g4_2.txt` born 01:31:50; `g4_1_horizon.py` / `g4_1.txt` 01:32:28 | +13 s |
| G5 01:40:11 | `g5_h3.py`, `g5_q2ext.py` and their outputs born 01:40:43 | +32 s |

No other copy of these scripts or outputs exists anywhere on the box, so the runs were not done elsewhere and copied in. WORKLOG lines 38, 52 and 61 record the locks at 01:15, 01:31 and 01:40, which agrees.
- **Caveat:** mtimes are not tamper-proof, and WORKLOG records "locked" without the hash. ATTEMPTS.md gives 8-hex prefixes.
- **Recommendation:** put the full hash in the WORKLOG line at lock time from now on.

### 1c. No prediction or threshold changed after a run [confirmed]
- Every scored table in NOTE uses the locked thresholds:
  - G3-1b: 5% / same r* / ±15% / χ* ≤ 4.
  - G4-1: r99 − r90 ≤ 3, fill ≥ 80%, ±15% and R² ≥ 0.98, halves within 20%.
  - G4-2: Q1 same r*, Q2 < 10%.
  - G5: [0.35, 0.65], 20%, ±15%, 1e−6, 1e−10.
- Fails are recorded as fails. The post-hoc material is labelled "not scored" in NOTE.
- The G5 setup-check failure stopped the m = 0 branch, as the prereg's rule requires.

### 1d. Fresh-copy reruns [confirmed: every number reproduces]
I copied the folder to `/tmp/hr/fg` and ran the scripts unchanged on a box loaded to 30–70.

| script | result |
|---|---|
| `g3_second_order.py`, `g3_centre.py`, `g3_wedge.py`, `g4_1_horizon.py`, `g3_1b_p4_qubit.py`, `g5_h3_posthoc_m0_hiprec.py` | byte-identical (apart from the per-row `secs` field) |
| `g3_1b_prereg.py`, `g4_2_intensivity.py` | SUMMARY blocks byte-identical. The per-job JSON lines are identical as a set (pool order differs), and the original files also hold stderr warnings |
| `g5_q2ext.py` | identical |
| `g5_h3_posthoc_m0.py` | identical apart from a captured stderr warning |
| `g5_h3.py` | setup-check lines identical (1.67e−3 → miss; m = 0.3 2.28e−15). m = 0.3 rows identical as far as the run got (it was slowed about 8× by box load; see `reruns/`) |
| `g3_2d_record.py 20` | identical as far as the run got (Slater world complete; eigenstate world in progress) |
| `g3_2d_record.py 14` | **differs**; see finding L4 |

## 2. Findings, ranked by severity

### H1 [HIGH, confirmed]: the summary lists a post-hoc, unscored T_c ≈ c/R under "What the cost supplies"
- **Where it appears:**
  - `THREAD_SUMMARY.md:39`: "Under per-site pricing, a boundary whose position the price sets (R ∝ κ^−0.46 critical, κ^−0.27 gapped). Through R that boundary sets the tracker's modular temperature, T_c ≈ c/R."
  - The NOTE heading "What G5 establishes" and its last bullets: "So the cost places the boundary, and the boundary sets a modular temperature."
- **Problems:**
  1. The critical T_c ≈ c/R numbers come only from `g5_h3_posthoc_m0*.py`, which NOTE itself labels "NOT preregistered, NOT scored". The scored G5 outcome for m = 0 is a setup miss. In the summary's bottom line the label is gone. That breaks the rule that an unscored rerun is not a result.
  2. Even as an observation, the R → T step is not supplied by the cost. T_c·R = 2/π is the Bisognano–Wichmann / Hislop–Longo centre value for an interval in the critical Dirac vacuum (Hislop & Longo 1982, Commun. Math. Phys. 84, 71, DOI 10.1007/BF01208372, verified on Crossref by me), i.e. a property of the vacuum (an input).
  3. The R ∝ κ^−½ step is a vacuum property too. The greedy rule stops when the marginal mutual information of the next site drops below κ, and in the critical chain that gain falls with distance at the rate set by the vacuum's correlation decay.

  So the only cost-supplied element is "a stopping radius where marginal information falls below the price". That restatement is what NOTE's G5 bullet "the exponent comes from the vacuum's correlations, not from the cost" already concedes.
- **Gapped case:** the reach is small. T_c·R_eff drifts monotonically, 0.544 → 0.515 (5% drift), over R_eff = 3.5–16.5 sites, against a correlation length of ξ ≈ v/m ≈ 6.7 sites. "T_c ≈ c/R in both vacua" generalises from about 2.5 decades of κ but only 1.4 decades of R.
- **Erratum text:** E-G3G5-1 below.

### H2 [MEDIUM-HIGH, confirmed]: the G5 setup-miss diagnosis is right in mechanism but wrong in fact; the ring holds 300 particles, not 298
- **Claim** (NOTE G5 diagnosis; ATTEMPTS G5; THREAD_SUMMARY G5 row and its "Fails" list; WORKLOG line 74): "The rule 'occupy E < 0' leaves both [E = 0 modes] empty, so the ring holds 298 particles, not 300."
- **Check** (`review_g3g5/zero_mode_check_out.txt`, with the exact `ground()` / `ring_C()` code):
  - The two zero modes come back from `eigh` as −7.1e−17 and +5.5e−16.
  - `e < 0` occupies **one** of them, so the trace is C = **300.000000000**.
  - The occupied zero mode is a real standing wave, so the density is staggered: C_ii − ½ = −1/600, +1/600, −1/600, … (±1.667e−3).
  - In exact arithmetic, "E < 0" would give **299** (n = −149…149) and two empty zero modes. **298 does not occur on either count.**
- **The worker's own number refutes 298.** A uniform 298/600 filling gives C_ii − ½ = −2/600 = −3.3e−3. The logged max|dC| = 1.67e−3 = 1/N exactly matches the ±1/N staggering (or a 299 filling), not 298.
- **What stands [confirmed]:**
  - The cause is the degenerate E = 0 pair on a periodic ring with N divisible by 4, which breaks translation invariance at O(1/N).
  - The antiperiodic N = 600 ring has 300 particles and max|dC| = 7.27e−6, so it also misses 1e−6. That confirms "the tolerance against N = 600 was unattainable for a gapless world".
  - At N = 6000 the post-hoc reference gives 7.27e−8.
  - G3-4 (open chain, N + 1 = 801 odd) has no zero mode and is unaffected. The W1/W2 worlds of G3-1b/G4-2 use random occupations and are not affected by this rule.
- **Erratum text:** E-G3G5-2.

### H3 [CONFIRMED, no erratum beyond one wording item]: the G4-1 erratum "scores stand" holds
I reran `g4_1_horizon.py` unchanged except that the world is the antiperiodic N = 600 ring (exactly 300 particles, translation-invariant): `review_g3g5/g4_1_anti.txt`.
- **Scheme B, m = 0:** H1 fails at every κ (r90 = 6–8, r99 = 50–76; tail 0.329, 0.120, 0.059, 0.029, 0.014, 0.0056 ≈ 1/r). H3 fails (R takes only the values 6 and 8). This is identical to the original.
- **Scheme A, m = 0:**
  - H1 fails at the scored κ = 0.001 (fill 0.960, r99 − r90 = 7). H2 is not evaluable (edge sites missing). H3 fails: R = 3, 5, 9, 15, 28, 50 (six values), T_c strictly increasing, but the halves of α disagree as before.
  - **The scores stand.**
  - **One descriptive change:** H1 at κ = 0.003 now passes (fill 0.965, r99 − r90 = 3), where the original world failed it (fill 0.966, r99 − r90 = 4). So "passes for κ ≥ 0.01" becomes "κ ≥ 0.003" on the correct world. This κ is unscored.
  - The original partner-mode values 0.7849 / 0.7608 become a degenerate pair, 0.7728 / 0.7728. The split was an artefact of the staggered density.
- **m = 0.3:** unaffected to four digits. H2 passes at both edges, slope/(2π/v) = 0.986.
- **Erratum text:** E-G3G5-3 (wording only).

### M1 [MEDIUM, confirmed]: W2 is one random sample per size; the sample-to-sample spread is larger than the 10% Q2 threshold
- **Setup:** W2 occupies each hopping eigenmode at random with Fermi weights at β = 1, one draw per size (`rng` seeded by size).
- **Check:** I reran W2 1D with five seeds per size (`review_g3g5/q2_seed_noise_out.txt`).
  - At fixed N = 200, κ_c(1) ranges over 0.58–0.79 and κ_c(2) over 0.61–0.73.
  - At N = 400, κ_c(1) ranges over 0.54–0.76.
  - TC/site of the r = 1 record ranges over 0.20–0.34 from sample to sample at fixed N.
- **Run status:** the N = 800 seeds had not finished when I wrote this; 10 of 15 rows are in the file. The offset-0 N = 400 row reproduces G4-2's world to 0.1–0.3% in κ_c. That residue is fit and threading noise, far below the spread.
- **Consequences:**
  - G4-2's Q2 FAIL for W2 (31%, 25%) and G5's Q2-ext PASS (N = 400 → 800: 0.96%, 4.1%, 5.6%) are both inside seed noise. Neither tells us whether κ_c depends on size. The scores stand as preregistered, since the prereg said "one world per size", but they carry little information.
  - The same goes for G3-1b's post-hoc diagnosis "the physical eigenstate world W2 has nearly intensive local data" and for G3-1b's restated condition (iv), "a world whose local data are intensive (W2 type)". On a single sample W2 is not intensive.
  - The Q2-ext run itself shows it: per-site TC of the r = 1 record moves +21% and r = 0 error/site +18% from N = 400 to 800.
- **Erratum text:** E-G3G5-4.

### M2 [MEDIUM, confirmed]: "sharp cut" under per-site pricing is claimed for the critical vacuum, where the scored H1 failed
- **Claims:**
  - `THREAD_SUMMARY.md:10`: "Per-site pricing (secondary): sharp cut, R ∝ κ^−0.49 (critical) / κ^−0.28 (gapped)".
  - NOTE G4-1 "What this says": "[OBS] With capacity priced per site, a sharp cut does appear, its location set by the price: R ∝ κ^−0.49 in the critical vacuum".
- **What the record shows:** at the scored κ = 0.001 the critical cut is ragged (fill 0.979; 0.960 on the correct world; r99 − r90 = 5 or 7). H1 fails there and H2 is not evaluable.
  - The cut is sharp only at unscored κ ≥ 0.01 (κ ≥ 0.003 on the correct world).
  - In the gapped vacuum it is sharp at every κ.
  - The exponent −0.49 is a fit of the hull half-width, ragged edge included.
- **Erratum text:** E-G3G5-5.

### M3 [MEDIUM, confirmed]: the worker's stated clock times and run durations are wrong; box times are not
The box clock is correct: `date` read 01:54:09 EST at the start of this review, in agreement with WORKLOG's neighbouring lines.

| worker statement | file evidence | finding |
|---|---|---|
| NOTE G5 RESULTS heading "checked 02:05 EST"; ATTEMPTS "## G5 (02:05 EST)"; THREAD_SUMMARY "re-hash intact, 02:05 EST" | `NOTE.md` and `ATTEMPTS.md` last written 01:52:47, `THREAD_SUMMARY.md` 01:53:19; WORKLOG 74–75 at 01:52/01:53 | **impossible** (12 min in the future) |
| NOTE G4-1 RESULTS heading "checked 01:48 EST" | `g4_1.txt` final 01:32:38; WORKLOG "G4 done" 01:38 | either a later re-check written into an earlier heading, or wrong; cannot be resolved from the files |
| NOTE "Erratum to §0 (~01:40 ET)", placed between the G3-1b lock and the G3-1b RESULTS | WORKLOG 54: FOR-36 appended its forces-gravity NOTE errata at 01:33; WORKLOG 46: G3-1b scored at 01:29 | the time is wrong by ~7 min, or the block was inserted mid-file; it is outside every hashed span |
| ATTEMPTS "g3_1b_prereg.py … ~12 min", "g4_2 … ~15 min", "g4_1 … ~5 min", NOTE "Ran in under 20 min" | output birth → last write: 4 s, 3 s, 10 s, 6 s; my reruns under load 30–70: 21 s, 28 s, 130 s, 28 s | durations overstated by 30–200× |
| ATTEMPTS "01:16 G3-1b prereg written and hashed" | lock file 01:15:11 | 1 min, harmless |

- **Impact:**
  - No integrity breach. The locks predate the runs (§1b) and the hashes re-verify now (§1a).
  - But self-reported times in the notes cannot be used as evidence. Only file times and the parent's WORKLOG lines can.
- **Erratum text:** E-G3G5-6.

### M4 [MEDIUM-LOW, confirmed]: G4-2 Q1 ("r* the same at every size") has little power
- The κ grid {3, 1, 0.3, 0.1, 0.03, 0.01} has no point between 0.3 and 1. Every κ_c(r) observed at N ≥ 100 lies in (0.41, 0.996).
- In practice the record family is all-or-nothing: r* ∈ {0, 3}, and r = 1 or 2 is never optimal at N ≥ 100.
- So Q1 passes whenever κ_c stays inside (0.3, 1). For the Haar world κ_c(0) = 0.9956 sits 0.4% below the grid point κ = 1.
- Q1's pass is real but nearly built in. The informative test was Q2.
- **Erratum text:** E-G3G5-7.

### L1 [LOW, confirmed]: Unruh/BW wording in G3-4 and G3.0
- **Heading:** "Cost-side route to the Unruh value" is contradicted by the section's own conclusion ("no cost-side derivation"; "lab note only").
- **"Exactly":** G3.0 says "a temperature of exactly 1/(2π) per unit of boost". On the lattice the slope ratio is 0.9976 (massless) and holds only for x ≤ 3 bonds, before precision saturates. "Exactly" belongs to the continuum BW theorem [KNOWN], not to this computation.
- **Dropped factor:** NOTE writes "T_local = v/(2πx) = a/(2π) in units ħ = k_B = 1, c = v". With a = v²/x it is a/(2πv), as the script itself prints. It reduces to a/(2π) only if one also sets v = 1, but the computation uses v = 2.
- **Erratum text:** E-G3G5-8.

### L2 [LOW, confirmed]: G3-2's Jacobson link is form-level, and the identity is textbook
- F_K(ρ′) − F_K(ρ) = T·D(ρ′‖ρ) is the Gibbs variational principle. Its second-order sign is Klein's inequality (D ≥ 0). It should be labelled [KNOWN] rather than [PIM].
- "So the sign Jacobson's maximum needs is the sign our D-term carries" is true but trivial: every relative entropy carries that sign.
- Lashkari et al. 2016 (10.1093/ptep/ptw139, re-verified on Crossref) is about canonical energy in holographic CFTs, and nothing here touches its content.
- The NOTE already flags the geometric part as an open miss.
- **Erratum text:** E-G3G5-9.

### L3 [LOW, confirmed]: G3-3 "forced iff (i) spin-½ probes" is narrower than its own PIM line
- Only spin-½ and spin-1 were sampled. The PIM line says correctly that the centre is visible to half-integer probes, so spin-3/2 also sees it.
- "Visible only to a read linear in U" should be "a read of odd degree in U". A cubic read also sees s = −1.
- THREAD_SUMMARY's "only for spin-½ probes" inherits the narrowing.
- The number 0.2030 bits/shot reproduces byte-for-byte.
- **Erratum text:** E-G3G5-10.

### L4 [LOW, confirmed]: `outputs/g3_2d.txt` (L = 14) is stale against the current script, and one fit residual is omitted
- **Stale file:**
  - `outputs/g3_2d.txt` was last written 01:05:03. `g3_2d_record.py` was re-saved at 01:05:46, adding the 4-offset block average and the joint fit.
  - Rerunning the current script at L = 14 gives different numbers.
  - In the eigenstate world at L = 14 the joint fit also has **positive** area parts: +0.82, +0.33 and +0.32 at l = 7, against perimeter parts of 5.8, 7.6 and 9.9.
  - At L = 20 the eigenstate area parts are negative, as NOTE says (−0.19, −0.29, −0.45). So the sign of the small area term is not stable in L.
- **Omitted residual:** in the L = 20 Slater world NOTE reports only the R = 3 residual (+0.27 vs 1.80). The R = 2 fit leaves +0.19 vs a perimeter part of 0.49, which is relatively larger.
- **What survives:** the headline "I/(4l) roughly flat" [OBS].
- **Erratum text:** E-G3G5-11.

### L5 [LOW, confirmed]: banned-word scan
- **Clean words:** in THREAD_SUMMARY, ATTEMPTS and NOTE from G3 on, there is no "solved", "bill", "kill", "dead", "verdict", "puzzle" or "theory of everything". "Derive" appears only in negations.
- **"Law":** it occurs only inside "power-law":
  - NOTE G4-1 prereg, "Stated expectations": this is locked text and must not be edited.
  - NOTE G4-1 RESULTS, "has a power-law tail".
- Under the house rule ("law" only in the CORE.md:7 sentence) these should read "algebraic tail".
- **Erratum text:** E-G3G5-12 (it does not touch the locked line).

### L6 [LOW, confirmed]: smaller items
- **Gapped T_c·R_eff:** "15–19% below 2/π" is 14.6–19.1%.
- **Exponents:** THREAD_SUMMARY gives R ∝ κ^−0.46 / −0.27 in its bottom line (G5 R_eff = hull/2: post-hoc for m = 0, scored for m = 0.3), but κ^−0.49 / −0.28 in its G4 row (G4-1 max half-width). Both are right for their definitions; the source should be named.
- **Scheme B H3 was nearly a fail by construction:** K* ≤ |T| = 5 modes, and the mode values cluster at {2, 0.78, 0.76, 0.05, 0.05}, so R(κ) can take at most about 3 values. The primary negative rests on H1, which is robust (H3 above).
- **Missing "chosen" items:** THREAD_SUMMARY's G4/G5 rows omit the greedy selection rule, the 5-site stake region and the centre-bond metric. Each is a design choice.

## 3. Overreach check: Bisognano–Wichmann, Unruh, Jacobson [mostly refuted as overreach; items H1, L1, L2]
- **Inputs are declared:**
  - The vacuum is named as an input in G3-4, in the G4-1 prereg ("Declared inputs") and in G5 ("a pass would not supply relativity, the vacuum, T = a/2π … or G").
  - THREAD_SUMMARY:2 says that nothing derives QM, GR, holography or gravity.
- **Not claimed:** nowhere does the thread claim to derive gravity, GR, holography or the Unruh temperature.
- **Remaining overreach:**
  - H1: "the boundary sets T" listed as cost-supplied, unlabelled.
  - L1: "exactly", the heading, and the dropped factor of v.
  - L2: the Jacobson sign sentence.
- **Jacobson items:** the R2 errata already reduce these to "same form as eqs. 14–16" and HYP. G3/G4/G5 add nothing that reopens them.

## 4. Forced-vs-chosen labels in THREAD_SUMMARY
| row | label issue | status |
|---|---|---|
| G3 | "PIM+OBS: F_K identity": textbook → KNOWN | L2 |
| G3 | "centre carries stakes only for spin-½": half-integer, odd degree | L3 |
| G3-1b | "FAILED as written", diagnosis "Haar … N^−½": the diagnosis is HYP in NOTE but unlabelled in the summary; the W2 contrast is single-sample | M1 |
| G4 | "Per-site pricing: sharp cut … (critical)": the scored critical H1 failed | M2 |
| G4 | "Q2 FAILED for W2": correct as scored; within seed noise | M1 |
| G5 | "298/600 filling": wrong count | H2 |
| G5 | "Post hoc, unscored: …": correctly labelled in the row | OK |
| Bottom line | "T_c ≈ c/R" under "What the cost supplies": unlabelled post-hoc result; the step is the vacuum's | H1 |
| Fails list | "G4-1 massless world had 298/600 filling (scores stand)": scores stand (confirmed), count wrong | H2/H3 |

Elsewhere the observed / hypothesis / proved-in-model labels match what the scripts do.

## 5. Does the thread's bottom line survive?
**Yes, with errata.** These parts survive:
- "Basis-free capacity pricing does not make a horizon." This is the preregistered primary result, reproduced, and robust to the zero-mode fix.
- "What stays input": locality, the vacuum, relativity, the representation, the gauge group, T = a/2π, G.
- "Nothing is ready to fold without a fresh-clone rerun and review."

These are corrected:
- The "what the cost supplies" item on the temperature: per H1, the cost supplies only a stopping radius, and T_c ≈ c/R is a post-hoc observation whose R → T step is the vacuum's.
- The G5 diagnosis and the summary's "298".
- The W2 single-sample reading.
- The critical "sharp cut".
- The timestamps.

No preregistered outcome changes.

## 6. Erratum texts (applied append-only to NOTE.md under "Errata from HOSTILE_REVIEW_G3G5")
- **E-G3G5-1 (H1).** THREAD_SUMMARY bottom line, "Through R that boundary sets the tracker's modular temperature, T_c ≈ c/R", and NOTE "What G5 establishes" are corrected to: "Under per-site pricing the price sets a stopping radius R(κ), where the marginal mutual information of the next site falls below κ [OBS]. Post hoc and unscored, the critical vacuum gives T_c·R_eff ≈ 0.60 against the BW interval value 2/π [OBS, post hoc only]. That R → T step is the vacuum's (BW/Hislop–Longo for an interval, an input), and the κ exponent of R comes from the vacuum's correlation decay. The cost supplies only where the stop falls. 'What G5 establishes' reads 'What G5 scored (P5c fail, setup miss, Q2-ext pass) and what it suggests post hoc'. In the gapped vacuum, T_c·R_eff drifts 0.544 → 0.515 over R_eff = 3.5–16.5 (ξ ≈ 6.7), so 'T_c ≈ c/R in both vacua' is withdrawn for the gapped case."
- **E-G3G5-2 (H2).** "So the ring holds 298 particles, not 300" is withdrawn. Corrected: "On the periodic N = 600 ring the two E = 0 modes come back from eigh with eigenvalues of order ±1e−16. 'E < 0' occupies one of them, so the ring holds 300 particles, but the occupied zero mode is a standing wave, giving a staggered density C_ii − ½ = ∓1/N and broken translation invariance at O(1/N). That is the 1.67e−3 = 1/N in the setup check. (In exact arithmetic 'E < 0' would give 299.) The setup-miss ruling and 'tolerance unattainable at N = 600' stand: the antiperiodic N = 600 ring, with exactly 300 particles, still differs by 7.3e−6." The same correction applies to ATTEMPTS G5, THREAD_SUMMARY's G5 row and Fails list, and WORKLOG 01:52.
- **E-G3G5-3 (H3).** The G4-1 erratum "scores stand" is confirmed by a full rerun on the antiperiodic N = 600 world (`review_g3g5/g4_1_anti.txt`). All scored outcomes are unchanged. Descriptive changes: scheme A m = 0 H1 passes for κ ≥ 0.003 (not κ ≥ 0.01) on the correct world, and at κ = 0.001 it gives fill 0.960 and r99 − r90 = 7. The scheme B partner-mode values 0.7849/0.7608 are a degenerate 0.7728 pair on the correct world.
- **E-G3G5-4 (M1).** W2 is one random Fermi-weighted occupation per size. Across five seeds, κ_c(1) spans 0.58–0.79 at N = 200 and 0.54–0.76 at N = 400, and TC/site (r = 1) spans 0.20–0.34 (`review_g3g5/q2_seed_noise_out.txt`). So the G4-2 Q2 W2 FAIL and the G5 Q2-ext PASS are both within sample noise; the scores stand but say nothing about size dependence. G3-1b's "W2 has nearly intensive local data" and condition (iv) "(W2 type)" are downgraded to [HYP], untested per sample. A seed-averaged test would need a new prereg.
- **E-G3G5-5 (M2).** "With capacity priced per site, a sharp cut does appear … R ∝ κ^−0.49 in the critical vacuum" is corrected to: "a sharp cut appears in the gapped vacuum at every κ, and in the critical vacuum only at unscored κ ≥ 0.01 (κ ≥ 0.003 on the zero-mode-free world). At the scored κ = 0.001 the critical edge is ragged and H1 fails. The −0.49 is a fit of the hull half-width, including the ragged points." The same applies to THREAD_SUMMARY's G4 row.
- **E-G3G5-6 (M3).** The times "02:05 EST" (NOTE G5 RESULTS heading, ATTEMPTS G5 heading, THREAD_SUMMARY locks line) are wrong. Those files were last written at 01:52:47 and 01:53:19, so the re-hash check happened at or before 01:53 (and the reviewer re-verified all three hashes at ~01:57). "checked 01:48 EST" (G4-1 heading) cannot be verified. The Erratum §0 time "~01:40" conflicts with WORKLOG 01:33. The run durations in ATTEMPTS ("~12 min", "~15 min", "~5 min") and NOTE ("under 20 min") are overstated: the file times give 4 s, 3 s, 10 s and 6 s. For timing evidence, use file birth/mtimes and WORKLOG lines, not the worker's stated times.
- **E-G3G5-7 (M4).** G4-2 Q1's pass is low-power. The κ grid has no point in (0.3, 1), every κ_c at N ≥ 100 lies in (0.41, 0.996), and r* ∈ {0, 3} only. Read Q1 as "κ_c stays inside (0.3, 1)".
- **E-G3G5-8 (L1).** G3-4 heading: read "Restricted-vacuum check of the BW/Unruh form (no cost-side input)". G3.0: "exactly 1/(2π)" → "1/(2π) to 0.2–0.8% at the cut (x ≤ 3 bonds), the KNOWN BW value". Reading line: "T_local = v/(2πx) = a/(2πv) (= a/(2π) only in units with v = 1)".
- **E-G3G5-9 (L2).** G3-2: the identity is the Gibbs variational principle [KNOWN], not [PIM]. "So the sign Jacobson's maximum needs is the sign our D-term carries" → "both signs are the positivity of a relative entropy (Klein's inequality). The link to Lashkari et al. 2016 is one of form only."
- **E-G3G5-10 (L3).** G3-3 (i): "spin-½ probes" → "half-integer-spin probes (only spin-½ was sampled)". "A read linear in U" → "a read of odd degree in U". The same applies to THREAD_SUMMARY's G3 row ("only for spin-½").
- **E-G3G5-11 (L4).** `outputs/g3_2d.txt` (L = 14) predates the current `g3_2d_record.py`, and the current script gives different L = 14 numbers, with positive area parts in the eigenstate joint fit (+0.82/+0.33/+0.32 at l = 7). The fit numbers in NOTE are L = 20 only, and the sign of the small area term is not stable in L. The L = 20 Slater R = 2 fit leaves +0.19 vs perimeter 0.49 (not reported earlier). The headline "I/(4l) roughly flat" [OBS] stands.
- **E-G3G5-12 (L5).** In non-locked text read "power-law tail" as "algebraic (~1/r) tail". The phrase in the locked G4-1 prereg stays as written.
- **E-G3G5-13 (L6).** Gapped T_c·R_eff is 14.6–19.1% below 2/π. R exponents are quoted per definition: G4-1 hull half-width κ^−0.49 (m = 0) and κ^−0.28 (m = 0.3); G5 R_eff κ^−0.46 (m = 0, post hoc) and κ^−0.26 (m = 0.3, scored). Scheme B's H3 could take at most ~3 R values by construction (K* ≤ 5). Chosen inputs to add for G4/G5: the greedy rule, the 5-site stake region and the centre-bond metric.

## 7. What I did not do
- I did not rerun G3-1 at L = 20 or G5 m = 0.3 to completion. Box load slowed them about 8×. Every row that finished matched exactly. See `review_g3g5/reruns/` for whatever had completed when I wrote this.
- I did not recheck the Round G1/G2 items or the Round 12-M fold.
- One DOI was added: Hislop–Longo 1982 (10.1007/BF01208372), verified on Crossref. Lashkari et al., Rauch et al., Werner et al. and Peschel were re-queried on Crossref and resolve to the cited papers.

## 8. Addendum, 02:45 EST: the slow reruns finished, no change to any finding
- `g5_h3.py` (full) and `g3_2d_record.py 20` (both worlds) finish byte-identical to the worker's outputs (apart from the `secs` field).
- The seed run is complete, 15 of 15 rows: κ_c(1) ranges 0.58–0.79 (N = 200), 0.54–0.76 (N = 400) and 0.62–0.73 (N = 800). TC/site (r = 1) ranges 0.20–0.34 over the same samples. Relative sd of κ_c(1), κ_c(2) is 7–15% at every size. So M1 stands as written.
- Side observation, not a finding: the 5-seed means of κ_c(1) are 0.68, 0.66, 0.68 at N = 200, 400, 800. A seed-averaged test might therefore show size-stability, but nothing here tests it. It would need a new prereg.
- Also done: `THREAD_SUMMARY.md` has an appended corrections section ("Corrections after HOSTILE_REVIEW_G3G5 (append-only)"). The text above it is unchanged.
