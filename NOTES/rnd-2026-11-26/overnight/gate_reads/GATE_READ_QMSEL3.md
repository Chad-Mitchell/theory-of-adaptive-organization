# Gate read: qm-selection-3 at lock e496428

*Thursday 26 November 2026, 07:15–07:26 ET (America/New_York). Reviewer: Forge executor. Fresh GitHub clone `/workspace/gate-qmsel3` at `e496428`, which `git ls-remote` shows as the tip of `forge-rnd-record-cost-2`. The scored run was not launched; only toy tests and the published SO(3) controls were run. No repo commits.*

## Decision: PASS-WITH-FIXES

The lock is sound and can be launched as it stands. None of the fixes below touches a locked file, so none needs a new lock. They are reading and reporting rules for the results write-up (F1–F3) and one append-only timestamp note (F4). If anyone wants F1–F3 enforced in code, that needs a new lock, never an edit to this one.

## 1. Lock integrity (checked)

- `sha256sum -c PREREG.sha256`, run from the repo root, gives OK for all four files: PREREG.md `6137e3a1…`, search_qmsel3.py `7e49ef28…`, list.out `ad655d39…` and toy_tests.py `d2b71e31…`.
- Lock commit `e496428` was committed at 06:50:23 ET. The GitHub activity API shows the push (`eb8f20b → e496428`) at 12:11:45 UTC = 07:11:45 ET.
- `30f345e` is in the history; it was the local lock that §0.10 says was never pushed. Between `30f345e` and `e496428`, search_qmsel3.py and list.out are byte-identical. The only changes are PREREG §0.10, the new §8 and the header line, plus the added toy_tests.py/.out/_run1.out. The script hash `7e49ef28…` is the same in both PREREG.sha256 files.
- I searched the whole box for run output (search_qmsel3*.out, RESULTS*.md under qm-selection-3, any running search_qmsel3 process) and found none. selftest_run1.out and toy_tests_run1.out are committed outputs from before the lock (controls and toy inputs only).
- The box's pinned versions match: numpy 2.5.5, scipy 1.18.1, python 3.13.5.

## 2. Tests re-run (OBSERVED)

- Re-running `toy_tests.py` gives **38/38 PASS**, the same as the committed toy_tests.out. See `/workspace/gate-qmsel3-harness/toy_tests_rerun.out`.
- The SO(3)-controls harness (`so3_controls3.py controls`) imports the module and calls `analyse` on the five published controls with the selftest seeds. Each control gives its published outcome:
  - B3 is TARGET: cap 2/2, recheck min −7.599e-07, 2 Weyl points.
  - Z3 is MISS on cost.
  - C1 is MISS on hSFP, re-confirmed.
  - Z2 is MISS on hSFP, re-confirmed.
  - B3×B3 is MISS on cost.

  These match selftest.out.

## 3. The three points raised

### 3a. B3 recheck minimum −7.6e-7 against the −1e-6 threshold: not a defect, but it shows what the recheck does and does not test

- **What I checked (OBSERVED).** The B3 orbit is a sphere, so the exact minimum of each witness effect a + l·y is a − |l|·r. For the B3 witness that `analyse` actually accepted, the exact minima are **−7.599e-07 for both effects**. That equals the recheck value. So the recheck is not noisy: it finds the true minimum exactly.
- **Where the negativity comes from.** It belongs to the witness itself. The cutting-plane loop in `cap_lower_bound` accepts a witness once the worst local minimum is ≥ −NEG_TOL = −1e-6, so any accepted witness may be negative by up to 1e-6. I reran B3 with 8 other seeds. Every accepted witness had an exact minimum between −5.8e-07 and −9.7e-07. The seed-0 value of −9.73e-07 sits only 2.7e-8 inside the threshold.
- **Consequences.**
  - (i) The recheck can only fail when the acceptance step missed a deeper minimum. That is what A3 was written to catch, and the toy tests show it catches such cases: −0.100, and −3.98e-2 for a grid-only witness. It cannot fail through float noise on a correct witness, so the small margin does **not** create a false-OPEN risk for B3-like bodies.
  - (ii) Every N_LB is therefore an ε-witness with ε = 1e-6, not an exact one. Mixing each effect with a little of the unit effect turns it into a valid measurement that distinguishes the states with error about N·1e-6. A false HIT or TIE would need a body whose true capacity is N−1 yet which has an N-set with negativity below 1e-6. By compactness the best negativity for a false N is a positive constant, but no bound on it is proved. PREREG §4.3 already keeps N_LB OBSERVED (numerical), which is the right label.
- **F1 (reporting fix).** For every HIT, TIE or TARGET, RESULTS should print the recheck minimum beside the threshold. It should also say that the capacity witness is valid to 1e-6. Before any such body is cited as more than OBSERVED, it should get an exact or tightened witness: a re-solve with cutting planes to 1e-9, or a closed-form witness. That follow-up would be new and unregistered (A10).

### 3b. Untested faces of exposure depth ≥ 2: handled as A1 option 2, and the condition can be discharged for most bodies by a theorem

- **The code matches what is declared.** `EPS_LIST = (1.0,)`, so the ε-probe is off. A pass prints "pass at depth 1 (no failure found)", and a HIT or TIE prints "conditional on faces of exposure depth >= 2, untested" (`analyse`, line 745). The direction of the risk is a false HIT, and G1 and §4.4 state that.
- **KNOWN (cited).** Biliotti, Ghigi and Heinzner, "Polar orbitopes", Comm. Anal. Geom. 21 (2013) 579–606, DOI 10.4310/cag.2013.v21.n3.a5 (checked on Crossref; arXiv:1206.5717). Their Theorem 3.2 says all proper faces of a polar orbitope are exposed. So depth-≥2 faces cannot occur for polar bodies.
- **Which bodies are polar (HYPOTHESIS, to be checked by hand per body).** Adjoint orbitopes are polar. That covers SU(3) on 8 (126 bodies, including the predicted flag TIE and the CP² TARGETs), Sp(2) on 10 (128) and G₂ on 14 (132). Isotropy representations of symmetric spaces are polar too: Sp(2) = Spin(5) on 14 = Sym²₀R⁵ (126), and SO(3) spin 1 and spin 2 (Z2 = real QM₃ is SU(3)/SO(3)). The balls are polar, and so are products of polar factors.
- **Which bodies are not polar (HYPOTHESIS).** Sp(2) on 5⊕10 (128), any factor of SO(3) spin ≥ 3, and diagonal sums like C1. For these bodies the condition stays.
- **F2 (reading fix).** In RESULTS, mark each HIT or TIE as polar or not polar. For polar bodies the depth-≥2 condition is met by citation (KNOWN, cited). For the others it stays open. This changes no score; it narrows the stated condition. The listed polar classes need a one-line check per class against Dadok's classification before anyone cites them.

### 3c. Does the Z2 bit-face fix made before the lock bias the outcome? It can move OPEN to MISS, never to HIT or TIE

- **How the code is ordered.** `bit_face_status` returns "ball" from `face_is_ball` **before** `in_relint` is called. `in_relint` only decides between "not ball" and "undecided", and only when `isball is False`. When there are 3 dimensions but fewer than 12 points, the result is `None`, which gives undecided. The fix (an LP in affine-hull coordinates, plus a 1e-3·radius off-hull refusal) therefore cannot create a HIT or TIE. It can only turn some undecided faces (OPEN) into "not ball" faces (MISS). That pushes against the theory's hoped-for outcome, consistent with §0.4's "cautious direction".
- **Remaining risk: a false MISS.** This happens if `bitface_points` under-samples a true 3-ball face, so that its points span only 1–2 dimensions. Then m lies in the relative interior of that smaller hull, and the face is scored "not ball". Before the fix, the same case would have been OPEN.
- **The published controls never exercise the proper-face "ball" path.**
  - B3 reaches TARGET before the bit faces.
  - In the selftest bit-face block, B3's midpoint is the centre, so the normal cone is {0} and F = Y (the trivial branch).
  - Z2 is a 2-dimensional "not ball".
- **Test I added (OBSERVED).** In B3×B3 (a product of balls) I took three kinds of pair:
  - (n, a),(n, −a): the face {n}×ball, expected 3-ball;
  - (n, a),(−n, a): the face ball×{a}, expected 3-ball;
  - (n, a),(−n, −a): the whole body through the centre, expected not a ball, dimension 6.

  Across 6 random seeds, all cases came out as expected (`bitfaces.out`): ball/3, ball/3 and not ball/6. The proper-face sampling recovered the full 3-ball each time.
- **On independence.** Z2 was used to design the fix, so it is not an independent check of `in_relint`. The toy tests (triangle centroid, vertex, outside point, off-hull point, 1e-5 noise, SO(2) disc) restore that independence.
- **F3 (reporting fix).** In RESULTS, any MISS that rests only on a "not ball" face with affine dimension ≤ 2 should be flagged for a hand check, because that is the one route by which under-sampling can produce a MISS. The B3×B3 proper-face case should go into the next lock's selftest.

## 4. A1–A10 against the code

| # | status |
|---|---|
| A1 | met (option 2): `EPS_LIST=(1.0,)`; "pass at depth 1"; HIT/TIE conditional (line 745); see F2 |
| A2 | met: witness pairs plus distinguishable T-fixed pairs; not ball ⇒ MISS, undecided or none ⇒ OPEN (lines 731–745) |
| A3 | met: `recheck_witness` uses the accepted effects, 10⁵ fresh points, seed SEED+10⁶+idx, 100 starts, before HIT/TIE/TARGET; it finds the exact minimum on B3; see F1 |
| A4 | met: Weyl set compared with 300-start search, OPEN on mismatch; hSFP gaps re-confirmed with 5× starts at 1e-6·rad |
| A5 | met: TARGET only when `known_cp`; otherwise "OPEN (TARGET-signature, check by hand)" |
| A6 | met: `g0_closure` per body, OPEN above 1e-8 |
| A7 | met: `check_list` and `check_versions` (toy tests refuse a swapped order and a wrong version); 927 bodies |
| A8 | met: §3.4 / G5 scope disclosure |
| A9 | met: §0.3 |
| A10 | met: §2 G1, §6 |

## 5. Low

- **F4.** The PREREG header says "§0.10 and §8 added 06:47–07:00 ET", but `e496428` was committed at 06:50:23 ET (and pushed at 07:11:45 ET). The stated writing window ends after the commit time. This should get an append-only timestamp note (DEVIATIONS or errata), not an edit.
- In the §8 table, the `recheck_witness` row reads "exact B3 witness ≈ 0". That is true of the closed-form witness in the toy test. The witness the scored path accepts sits at −7.6e-7 (see 3a). No change is needed, but say so in RESULTS so that nobody misreads the B3 margin.

## 6. Launch conditions (unchanged from §8)

Use a fresh GitHub clone at `e496428` or a descendant, put the `ls-remote` line and the clone path at the top of the log, verify the hashes, use the pinned versions and run with nohup. Not launched by this review.

## Files

`/workspace/gate-qmsel3-harness/`: `so3_controls3.py` (harness; never calls `--run`), `controls.out`, `b3seeds.out`, `bitfaces.out`, `toy_tests_rerun.out`.
