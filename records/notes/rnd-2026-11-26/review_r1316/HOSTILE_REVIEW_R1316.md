# Hostile review: Conjecture C rounds 13–16 (part M) at 04c8309

Reviewer: Forge executor, fresh context. 2026-11-26, 06:04–06:17 ET.
Object: `mitchell-moving:forge-rnd-record-cost-2` at `04c8309`. Fresh clone `/workspace/review-r1316`
(the Lean clone was not touched). No repo commit or push.
Files: `theory/record-cost-2026-11-25/conjecture-c-round14/`, `-round15/`, `-round16/`,
`scripts/selfref/m_round13_*`, `theory/RECORD_COST_ROUND10_2026-11-25.md` §17–§19, `measurement/CLAIM_MAP_v2.md` RC17–RC19, README row.

## Summary

No high-severity findings. Every score matches its pushed lock. Round 14's H3 "not tested" is justified.
Round 16 is a real new lock: the prediction is the same one, only the code changed, and the helpers
were tested before the lock on made-up numbers only. My independent check of max(icosahedron, dodecahedron)
agrees: the automorphism group has order 14400 = 120 × 120, so all automorphisms are local.
The Al-Safi–Richens claim is accurate. Two medium findings concern how the timing record is described,
not the scores: the "fresh clone" wording plus a one-second push/run margin for round 16, and the
"clock stepped" explanation, which the evidence contradicts.

## 1. Locks and scores

| Round | lock commit, push (GitHub, ET) | PREREG.md sha256 (recomputed) | run start (box) | locked files changed after lock? |
|---|---|---|---|---|
| 14 | 4e189c6, 03:54:42 | 523dfb533dfb88ea…93d787532 ✓ | 03:55:07 (failed launch 03:54:58, no Python) | no (append-only: outputs, RESULTS, diagnostic) |
| 15 | ed1ceef, 05:09:12 | 470bd9053cb8cd56…803f8457 ✓ | 05:09:19 | no |
| 16 | c6f01f6, 05:15:41 | 236ebf1de8a0e003…f7f6ca23f326 ✓ | 05:15:41 | no |

`sha256sum -c` passes for all three `PREREG.sha256` files, covering the scripts, the round 13 copy and
the round 16 toy test. The box reflog `update by push` stamps agree to the second with GitHub's activity API.

Scores against the locks (observed):
- **R14.** H1 and H2 not tested: `timeout 120m`, exit 124, no output. The prereg rule says "a run that
  does not finish is reported as not tested". H3 not tested (see §2). H4 hit: 23/23 CERTIFIED, matching
  the prediction "none in any of the 23". H5 hit: 3/3 CERTIFIED. Total: 2 hits, 0 misses, 3 not tested. ✓
- **R15.** Not tested: crash before the search. This matches the "crash ⇒ not tested" rule. ✓
- **R16.** V1 passed (6, 4, 20). V2 is a hit: 1 + 397 pairs, 0 found, 0 undecided. V3 matches. ✓
  I re-ran `r16_h3_canonical.py` from my clone and got the same output (`r16_rerun.out`, about 2 min).

## 2. Round 14 H3 "not tested": justified

The script printed the predicted outcome ("no automorphism"), but its classes were too fine: 413 symbolic
classes against 20 true values. Even the single row candidate was filtered out ("tried 0 pairs" against
1 in round 13). Classes that are too fine can only exclude maps, so "none found" certifies nothing. Scoring
a run that printed the predicted outcome as not tested goes against the author's interest, and the
post-run diagnostic is labelled as outside the lock. ✓ One small gap: the R14 prereg had no validity
check, so this call is a judgement made after the run. It is conservative and disclosed, so acceptable.

## 3. Round 16: a new lock, not a patched prediction

- The prediction text (V2) is the same as R15's V2 and R14's H3. Only the class step of the script changed
  (diff R15→R16: header, `elt/key/fmul/tofloat`, bookkeeping). V1 adds a validity gate whose numbers
  (6/4/20) were known beforehand, and this is disclosed.
- Pre-lock toy test: `PRELOCK_toy_helpers.py` executes lines 28–36 of the locked script (`FQ` through
  `tofloat`, helpers only, no icosahedron or dodecahedron data) on six made-up numbers, then checks the
  results against a float count (12 = 12). Its output is hashed in the lock and was committed in
  c6f01f6 (05:15:09), so it existed before the lock. ✓
- The hit criterion was fixed before the run: V2 and the "not tested" conditions are in the pushed PREREG.md. ✓
- Repeating the attempts carries no forking-path risk: R14 and R15 were invalid runs, not misses, and the
  predicted direction never changed.

## 4. Independent rerun of icosahedron × dodecahedron (my own code)

`indep_aut/indep_aut.py` (1 s): exact Q(√5) arithmetic with Fractions (no sympy, no repo code); facets
found by brute force; K = E(EᵀE)⁻¹Eᵀ per factor; K_AB = K_A ⊗ K_B; then the automorphism group of the
edge-coloured complete graph on the 240 product facets, computed with nauty (`dreadnaut`).
- Per factor: 6 and 4 distinct K values. Product: 19 off-diagonal values plus 1 diagonal value = 20. All
  three match V1.
- |Aut(K_I)| = 120 and |Aut(K_D)| = 120. **|Aut(K_{I×D})| = 14400 = 120·120**, so every automorphism of
  max(I, D) is local (local maps act faithfully on facets).
- Controls: triangle × triangle (classical) gives 9! = 362880, so non-local maps are detected.
  Square × square (boxworld) gives 128 = 8·8·2, local maps plus the swap, as Gross et al. 2010 found.
- Validity of the invariant: facet effects normalized to value 1 at the centre are also max-normalized
  up to the same factor (central symmetry), so any linear automorphism permutes them without rescaling
  and preserves K. PROVED (in-model), now by two independent codes.

## 5. Timing disclosures

- **R14 H1/H2 time limit.** The wall-clock span is 03:55:07–06:01:45 (126.6 min) against `timeout 120m`.
  The scores are not affected: no output came either way, and the limit was not raised.
- **"Clock stepped" (finding M2).** The evidence does not support a wall-clock step. The box wall clock
  agreed with GitHub at 03:54:42 (before the run) and at 05:09:12, 05:15:41, 05:21:50 and 06:03:51 (after
  it). What lags is the uptime/monotonic clock: the kernel boot time reads 03:26:43, while PID 1 dates from
  03:20:07, matching the WORKLOG "03:20 restart". That is the same 6.6 min. A pause of the box (for example
  a VM suspend or migration) during the run explains every number: `timeout` counted 120 min of run time,
  and `ps` etime 1:54:50 at 05:56:33 against 121.4 wall minutes. HYPOTHESIS about the cause; OBSERVED for
  the clocks.
- **Round 13 lock on the box only.** The disclosure ("local lock only") is accurate. One extra caveat: the
  box files `rnd/selfref/PREREG_ROUND13_M.md(.sha256)` now have mtime 03:21:46, rewritten after the box
  replacement. So only WORKLOG line 72 (01:46 ET, hash prefix 35c19ee9251ac8cc) records the lock before the
  runs (02:06–02:53 ET). The content is identical to the repo copy (sha256 35c19ee9…e1b).
- **R15 time correction.** Accurate: the commit is 05:08:49 and the push 05:09:12, against "about 05:15" in
  the file. The correction is in RESULTS and the file is not edited. ✓
- **R14 written time.** Before the push, the local lock commit 89ca95f (03:28:42, PREREG sha 18f5d6af…)
  said "about 03:40". The pushed lock says "about 03:30". This is the only difference (one line), but it is
  not disclosed (L1).

## 6. §17/§18/§19 and RC17–RC19: overstatement check

- **Al-Safi–Richens Theorem 1 covers max(I, D): accurate.** DOI 10.1088/1367-2630/17/12/123001,
  Crossref-checked (NJP 17, 123001, 2015, Al-Safi and Richens). Theorem 1: "All reversible transformations
  on a max tensor product of non-classical, dichotomic systems are trivial". The Discussion states that it
  does not need identical subsystems. §4 of the paper says every regular 3-polytope except the tetrahedron
  is dichotomic. Since I ≠ D, "trivial" means local here. KNOWN.
- §17 says "every centrally symmetric polytope with all effects is dichotomic (u − e_n = e_{−n})". This is
  correct, but Theorem 1 also needs **non-classical**, and the segment is centrally symmetric and classical.
  The README row ("maximal composites of centrally symmetric parts were already covered") inherits this (L4).
- **M12ₙ (RC17).** I re-derived the n-part constant-trace identity: block-scalar Σ_O over subsets J, h = D/N
  with D = Σ_J m_J, and per-term m_J E s_J/(N(N − E s_J)) > m_J E s_J/N² for s_J ≠ 0. I also checked the
  three-square example (2 + 12·1 = 14 ≤ 26). No gap found. The claim stays "parallel worker's self-check
  plus this read, not formalized".
- **Cuboctahedron² (RC18).** I re-ran `m_round13_cert_exact.py` and got the same output (EXACT
  CERTIFICATE). This is reproduced, not re-derived independently. RC18's ledger text omits "not
  preregistered", which §18 does state (L7).
- **§19 and RC19.** Worded with care: R16 is "new only as a check of the method", ♦ on I² and D² is
  "not settled", and there is no derivation claim. ✓
- §16:254 ("mixed polygon pairs are not in that paper") is superseded by §17 for even polygons. Append-only
  handling is fine.

## 7. Wording rules

`tools/banned_words.py` against upstream main: 0 FAIL, PASS. `tools/check_claims.py`: PASS. Against the
fork's stale origin/main it shows 12 old FAILs, the same artefact as before. My grep of the diff
539ffa5..04c8309 found only "Lawvere" and the code word `solve`. There is no claim to derive QM, GR,
holography or gravity. Labels are used throughout, with one inconsistency (L3).

## 8. Findings

### High
None.

### Medium
- **M1. The run-tree provenance for R15/R16 is overstated.** RESULTS say "from a fresh clone at ed1ceef / c6f01f6".
  The run directory `/workspace/r15-check` was cloned once (05:08:49, from upstream main), and each lock
  commit was then fetched from the local working copy `/workspace/r11-fold` (FETCH_HEAD), not from GitHub.
  It was reused for R16. For R16 the push record (05:15:41) and the START line (05:15:41) fall in the same
  second. The hashes make the run tree identical to the pushed lock, and push-then-launch sequencing is
  consistent, but "pushed before the run" holds only at one-second resolution. Fix (append-only note):
  state the provenance exactly. In future, launch only after `git ls-remote` shows the lock, and clone from GitHub.
- **M2. The "box clock stepped ~6.6 min" explanation (R14 RESULTS, WORKLOG 06:03) is contradicted.**
  The wall clock matches GitHub before and after the run. The monotonic/uptime clock is the one that is
  6.6 min behind (a box pause). Fix: an append-only correction of the mechanism. Scores are unchanged.

### Low
- **L1.** The R14 "written at about" time changed from 03:40 to 03:30 between the local lock 89ca95f and the pushed lock; this is not disclosed.
- **L2.** The round 13 local-lock files on the box were rewritten at 03:21 after the box replacement. Only the WORKLOG 01:46 line dates the lock.
- **L3.** The same method (colour refinement separates products) is labelled PROVED (in-model) for H5 and
  for §18's three squares, but OBSERVED (exact, per instance) for H4 and §18's hexagon² family. Pick one
  (per-instance exact certificate = PROVED (in-model) for that instance).
- **L4.** §17 and README: add "non-classical (dimension ≥ 2)" to "centrally symmetric parts" when citing Theorem 1.
- **L5.** R14 §0 discloses the H2 look at the data. The H1 value −2.541438 was also re-observed in the
  round 13 ascent before the R14 lock (it matched R13's own prediction). Minor, and not scored.
- **L6.** R16 V1's counts were known in advance (disclosed). V1 is a gate, not a test. ✓
- **L7.** RC18 should say "not preregistered".

## 9. Safe to cite

- max(icosahedron, dodecahedron) has only local automorphisms: PROVED (in-model), an exact certificate
  (R16, confirmed by an independent nauty count of 14400). Cite Al-Safi–Richens 2015 Theorem 1 as the
  KNOWN source; the repo result is a check of the method only.
- Al-Safi–Richens Theorem 1 covers maximal composites of non-classical dichotomic parts, including
  non-identical ones (I × D, even polygons, balls). KNOWN, DOI checked.
- The Round 14 scorecard: 2 hits (H4, H5), 0 misses, 3 not tested (H1, H2, H3), against lock 523dfb53…
- R14 H4 (23 composites; the random 20 are a weak test) and H5 (3 composites): exact per-instance
  certificates that no automorphism maps a product pure state to a non-product one.
- Theorem M12ₙ: PROVED (in-model), pen and paper (self-check plus this read; not formalized).
- Cuboctahedron²: ♦ by exact rational certificate (reproduced; not preregistered) ⇒ M12 applies (RC18).
- RC19 as written (open miss).

**Not safe:** round 13 H3 as more than OBSERVED (numerical); R14 H3 as a hit; ♦ on icosahedron² or
dodecahedron² as settled; "the box clock stepped"; R15/R16 "fresh clone from the pushed lock" without the
M1 note.

## 10. qm-selection-3

Not pushed at review time. The tip is still 04c8309 at 06:17 ET, and no branch on the fork contains
`theory/qm-selection-3-2026-11-26/`. No gate read was done.

Artefacts here: `indep_aut/indep_aut.py` + `.out`, `r16_rerun.out`, `cert_exact_rerun.out`.
