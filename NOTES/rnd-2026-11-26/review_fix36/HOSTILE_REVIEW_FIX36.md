# Hostile review: FOR-36 foundations-fix commits, `forge-rnd-record-cost-2` 9650bcc..539ffa5

*Thursday 26 November 2026, 03:01 ET. Reviewer: fresh-context executor for Forge. I worked from a fresh clone in `/tmp/fix36/repo` (HEAD 539ffa5) with a worktree at 9650bcc. I made no commit and no push. `THEORY.md`, `CORE.md` and the locked blobs are untouched. In-model only.*

Commits reviewed:
- 5f36cf5 errata
- 1c41dac prereg hygiene
- dc4d5a8 gate-read-290 elision
- 06f07e6 QM-selection lock (PREREG sha256 c4a529c7…, script b9bf90eb…)
- merges 43ebbb0 and 0703fd3
- 539ffa5 RESULTS (miss)
- the PR #295 body as of 2026-11-26 02:49:31 ET (API `updated_at` 07:49:31Z)

## 0. Summary by severity

**High:** none. No history was rewritten. No locked blob, committed prereg or log line was altered, except the declared gate-read copy in L2. Every lock hash verifies. The miss is mathematically correct within its stated scope.

**Medium**
- **M1.** The #292 `DEVIATIONS.md` line (01:45) and `gate_reads/README.md` say the v3 probe did not call the minimizer. That is false. The v3 probe calls `minimize(lambda v: t2.Jtot(v,w,wx), x0, method="L-BFGS-B", bounds=t2.BOUNDS, options=opts)` for 10 starts plus 2 half-tolerance reruns, with non-locked seeds 424242 and 777, and does not print J. Correct it with an appended line.
- **M2.** The lock-before-run order is attested only on the box, not on the server. The lock commit 06f07e6 (01:47:47 ET) was not pushed before the scored run (01:48:13–01:48:53 ET). GitHub's activity API shows one fast-forward push, 9650bcc→539ffa5 at 02:49:08 ET, carrying the lock and the results together. The box evidence is consistent and I found nothing wrong (§4), but an outside reader cannot check the order from GitHub.
- **M3 (gate read, conceptual).** Under P4 (G₀ connected), P2 alone already implies P3: a connected group acting transitively on a finite set of at least 2 points is impossible. So U is carried in by P4, which is premise CD in another form, and the stated "P5 + P2 imply P3 (Jordan)" understates how much P4 does. P4 is also new at this lock, chosen with the O(3) counterexample in view. That is honest (it is in the table), but it is premise accretion of exactly the kind the freeze is meant to log.
- **M4 (evidence value).** The miss is worth about zero as a preregistered test: it was not blind, the development-run outcome was seen, and by G2 the outcome is fixed by a classification theorem. Its value is the value of the proof. I re-derived the proof independently; it holds, with the gaps in L5 and L6.

**Low**
- **L1.** Timing of gate v5: "about 22:15" should be 22:11:36. That is the mtime of `gate_read_292_v5.md`; T1 started 22:11:43, 7 s later. DEVIATIONS' "22:10–22:15" is imprecise.
- **L2.** dc4d5a8 edits a committed line of `gate_read_290.md` (the 6a elision). Its header declares the change, and the line was probably unpushed when edited, but that is not strictly append-only. The elided word list is still in the 1c41dac history.
- **L3.** Errata §6 says "Not in Lean … the maximal-torus SFP criterion". That is true for the general criterion, but 80cf785, already in the base at 01:19 ET, proves the concrete cases (`ball_SFP_iff_odd`, `complex_fixes_ray`, `real_even_not_SFP`, …). Say so.
- **L4.** Errata §1 says "infinitely many pure states, i.e. U". That needs a closed (compact) group: an infinite transitive group is enough only after taking the closure.
- **L5.** PREREG and RESULTS never compute G₀(K). The pass claims need G₀(Z3) = SO(3) (Montgomery–Samelson 1943, 10.2307/1968975, Crossref-checked) and G₀(B3×B3) = SO(3)×SO(3). The fail claims are safe, because a circle face rotated by a subgroup of G₀ already fails.
- **L6.** The §3.3 normal-cone argument treats exposed faces only. Non-exposed faces need one more line: pass to the minimal exposed face containing them, which is invariant under the face's stabilizer.
- **L7.** K_θ is one body up to affine isomorphism. Scaling the spin-2 isotypic component is SO(3)-equivariant, so "family", "C1 included" and the 9 values of θ are redundant. This is harmless.
- **L8.** RESULTS should cite Hopf–Samelson inline (Comment. Math. Helv. 13:240–251 (1940), 10.1007/BF01378063, Crossref-checked). At present the DOI is only in the rounds 4–9 note (:110). The criterion also uses the maximal-torus conjugacy theorem; name it.
- **L9.** RESULTS says "Deviations: none, not repeated in a DEVIATIONS.md", while PREREG says changes go in `DEVIATIONS.md`. Create an empty `DEVIATIONS.md` that says "none", or say why it is absent.
- **L10.** RESULTS:28 says "rank-2 and rank-3 groups (SU(3), Sp(2), G₂)", but all three have rank 2.
- **L11.** The Lean paragraph of the PR body (line 63) is stale against the base:
  - "Item L5 … partial: only the linear core" — b40e87a (00:28 ET, in the base) is titled "L5 in full". I did not re-check the Lean.
  - "the maximal-torus criterion … not formalized" needs "(concrete cases in `SFPCriterion.lean`, 80cf785)".
  - Line 114, "check_lean 1628 … Lean sources are unchanged since that audit", is not true: a2a3f52, b40e87a and 80cf785 changed `formal/lean/GTAO` after the port (aac249c), and line 63 itself cites AUDIT 1679.
- **L12.** PR body line 109/113 says "banned_words PASS" at 539ffa5. I could not reproduce that. Against upstream `main` (8b553c6), `tools/banned_words.py` gives 2 FAILs: `theory/composite-contest-2026-11-24/PREREG_4.md:28` and `theory/menu3_checks/RUN_LOG.md:17`. Both are identical at 9650bcc, so they predate this range, and the range itself adds 0. Against the fork's stale `origin/main` it gives 12, all outside the range. Say which base was used, or note the 2 carried hits.
- **L13.** The errata do not address the review's PR-body items. They were fixed in the body directly ("Nothing was rebased" at line 1, #292 at line 12, the horizon wording at line 50), which is acceptable, but the errata file does not record it.

## 1. History and locks: confirmed

- The 9650bcc..539ffa5 diff has 0 deleted lines, apart from the dc4d5a8 line in L2. The merges are true merges, and nothing upstream of 9650bcc was rewritten.
- GitHub activity for the branch lists only `push` events, no `force_push`: 90ea900 → 181b9a2 → e48494e → ddf559b → 5b2043f → 9650bcc → 539ffa5.
- `tools/verify_locks.py` at 539ffa5: RESULT PASS (190 OK, 13 scrub-only, 2 declared, 2 unverifiable).
- New locks: PREREG.md c4a529c7… and the script b9bf90eb… both match `PREREG.sha256`. PREREG_5.md b7850655… matches (lock df114b6, 2026-11-25 14:57:46 ET).
- The `tests/*` lock mismatches noted earlier are identical at 9650bcc, so they predate this range.

## 2. Errata vs `rnd/HOSTILE_REVIEW_FOUNDATIONS.md`: accurate, nothing new overclaimed

§1–§8 cover every math and wording item in the review. Open items: L3, L4 and L13. No new claim is made of deriving quantum theory, general relativity, holography or gravity. The three DOIs in `doi_check_7f.out` are as stated.

## 3. DEVIATIONS: checked one by one

- **#286 (ctc-fixed-point): true.**
  - f18721fc and 3e1fcf9e are not ancestors of the branch; they are on `forge-ctc-review`.
  - Their times are 16:14:59 and 16:26:15 ET.
  - The PREREG hash 756d9f0c is unchanged.
  - The five identity bars match DEVIATIONS:43.
- **#290 (hutter) item 9: true.** RESULTS:27 and :82 and PREREG:43 confirm it. The committed `gate_read_290.md` matches the session file, apart from the declared header, the `<local>` paths and the 6a elision.
- **#292 (stop-copying): two inaccuracies.**
  - The v3-probe claim (M1).
  - The v5 time (L1).
  - Otherwise true: v1–v5 match the box copies apart from paths.

## 4. RESULTS miss: rerun and certificates

- **Rerun.** `python3 search_u2_sp1sp1.py` on the fresh clone took about 30 s. Its output is byte-identical to the committed `search_u2_sp1sp1.out` (copy in `review_fix36/search.rerun.out`).
- **The scored-run files exist on the box** in `/tmp/qmrun`:
  - start.txt reads 01:48:13 and done.txt 01:48:53.
  - The script is the locked b9bf90eb…; its output is identical to the committed file.
  - A RESULTS.md draft was written at 01:49:22 and is identical to the committed one.
- **Exclusions, checked analytically and independently:**
  - **Spin-1⊕2 (C1 / K_θ) fails hSFP.** The functional −Y20 is maximized on the equator, giving a circle face rotated by SO(2) ⊂ G₀.
  - **Real QM d=3 (Z2) fails hSFP** by the same equator face.
  - **B3×realQM fails hSFP**, because a product face contains the Z2 equator face.
  - **B4 fails SFP**, through −1 ∈ SO(4) acting with no fixed point.
- **Survivors, checked by the same route:**
  - **Z3 (spin-3, d=7).** An odd harmonic makes the body centrally symmetric, so its capacity is 2. The only SO(2)-invariant functionals are along Y30, so every face with a positive-dimensional stabilizer is a pole, and hSFP holds (given L5).
  - **B3×B3 (d=6).** It is centrally symmetric, so its capacity is 2; faces of a product are products of faces.
  - Both have d > 3 at N = 2, so the ball is cheaper and the **MISS stands**.
- **Candidate list.** It is complete for U(2) and Sp(1)² in dims 4–8:
  - U(2) needs a zero weight, so k + 2m = 0, which is SO(3) spin k/2.
  - For Sp(1)², (j1, j2) needs both entries integer.
- **Scope.** The limits are stated (RESULTS "Does not …": other groups, dims 9–15).
- **Citation.** The maximal-torus citation is correct (Hopf–Samelson 1940, DOI checked on Crossref 26 Nov 2026), but only by pointer (L8).

## 5. Timing

| Event | Time (ET) |
|---|---|
| PREREG.md and script written (`/workspace/fix-295`, birth) | 01:47:23 |
| PREREG.sha256 and lock commit 06f07e6 | 01:47:47 |
| Merge 43ebbb0 | 01:48:02 |
| Scored run | 01:48:13–01:48:53 |
| RESULTS draft | 01:49:22 |
| WORKLOG:78 at 02:22: "resumed after interrupt: nothing pushed yet"; fresh checkout `/workspace/fix-295b` | 02:22 |
| Commits 0703fd3 and 539ffa5 | 02:22:06 / 02:22:24 |
| Single push | 02:49:08 |

The worker's account (run at 01:48, interrupted, nothing pushed until later) is consistent with every file time and the server record. The lock predates the run by 26 s on the box (M2).

## 6. PR #295 body

- No closing keywords (grep for close/fix/resolve + #N: none). All six carried PRs are "not proposed for closing".
- No banned words in the body.
- The line 1 rebase correction, the line 12 #292 breach note ("an independent gate read of `PREREG_5.md` is still owed") and the line 50 "tested horizons (observed)" are accurate.
- Line 101 is accurate: miss, 0 hits, not blind, no gate reader.
- Stale: the Lean paragraph and check_lean line (L11). Not reproduced: the banned_words PASS (L12).

## 7. Independent gate read: `theory/qm-selection-2026-11-26/PREREG.md`

I read only the Gate, P1–P8 and §3, against `process/PREREG_GATE.md` at 8c4b3c0.

- **G1.** Well-posed: hit = non-Jordan, P1–P5 under P4, d < N²−1; a tie counts as a hit. The rule is fair, even generous to the rival, because a tie counts against "P1–P6 select QM". Two gaps:
  - Excluding Jordan bodies from hits is safe here, since in dims 4–8 only B4 (fails) and real QM (fails) appear. It is not neutral in general: a non-complex Jordan body that passes P1–P6 and is cheaper would also refute "P1–P6 select complex QM".
  - P6's clause that every bit face of a higher-rank body is the cheapest bit is not used in G1. State whether it is.
- **G2.** **Fails: CONSISTENCY_CHECK.** The outcome is fixed by §3, a classification the author sketched before the lock, and the development run showed the outcome. The PREREG says "close to CONSISTENCY_CHECK"; it should say CONSISTENCY_CHECK outright.
- **G3.** Pass. The rival (C1, P7 needed) is named and predicts a different outcome.
- **G4.** Level (a), with a route to (b) named. Pass.
- **G5.** Pass: the hit and miss branches differ. The miss branch should read "P7 is not needed *given P5 (hSFP)*". P5 was itself introduced after C1, so P7's work is done by a premise added for that purpose (M3).
- **Gate status:** stop as a TEST, allowed as a CONSISTENCY_CHECK. It is well-posed and its hit rule is fair. Evidence value: about 0 as a test (M4); as mathematics it is a correct in-model result once L5 and L6 are fixed.

## 8. Independent gate read: #292 `PREREG_5.md`

This read is retrospective. The runs already happened (22:11–22:41 ET, 25 Nov), but I did not open RESULTS, `run_t*_v2.out` scores or `aggregate.out` before writing it. I only counted lines: each `.out` has 5 SETTING_JSON lines and 1 TOTAL_JSON.

- **Scope.** PREREG_5 adds no new Gate table. G1–G5 come from PREREG_2 as amended by PREREG_3 and PREREG_4, which I read. Hit: A > 0.12 at all 5 settings, honest hit odds 0.12. T2 is the same with A_(5). G2: global minimization with no closed form. G3, G4 and G5 are as in PREREG_2.
- **Well-posed:** yes.
  - The completeness rule (§1) is defined.
  - The 4 paths have locked one-line commands. The functions and signatures exist in `checks/aggregate.py`, and `checks/test_prereg5_paths.py` gives 5 passed.
  - One loophole: "complete" means **at least** five SETTING_JSON lines. That should be exactly the five locked settings, distinct, plus TOTAL_JSON. Not material here.
- **Hit rule fairness:** fair to strict. All-five plus resolution, and every degenerate label (not settled, budget, guard, measurement/code, incomplete) scores as a miss, so the hypothesis cannot win on a technicality.
- **One issue: §2 relabels.** §2 replaces an unreachable clause (correctly argued so) with "any post-hoc relabel … recorded in `checks/RELABELS.md`", with no stated grounds and no rule that scoring uses the unrelabelled labels. That opens an unlocked degree of freedom after the run. Add: scoring uses the script labels; relabels are reported beside them and cannot move a miss to a hit.
- **Gate status:** pass as a TEST, with the §2 relabel caveat. The process breach stands as logged: v5 passed by the author agent, not by a fresh reader. This read can be recorded as the owed independent read, but only as retrospective.

## 9. Corrections to route (append-only)

1. #292 `DEVIATIONS.md` and `gate_reads/README.md`: append a correction. The v3 probe did call the L-BFGS-B minimizer (10 starts + 2 half-tolerance reruns, seeds 424242 and 777, J not printed). Gate v5 is timed 22:11:36 ET, 7 s before T1.
2. `RECORD_COST_ERRATA_2026-11-26.md`: append §9.
   - §6: concrete maximal-torus cases are in Lean (80cf785, `SFPCriterion.lean`); the general criterion is not.
   - §1: "i.e. U" becomes "with a closed group, U".
   - PR-body fixes recorded (L13).
3. `qm-selection-2026-11-26`: append to RESULTS or a new DEVIATIONS.md.
   - G₀(Z3) = SO(3) (Montgomery–Samelson 1943, 10.2307/1968975) and G₀(B3×B3) = SO(3)².
   - The non-exposed-face step.
   - K_θ is a single body.
   - Hopf–Samelson DOI inline, plus maximal-torus conjugacy.
   - "rank-2" in place of "rank-2 and rank-3".
   - Label: CONSISTENCY_CHECK.
   - P4 + P2 ⇒ P3 noted.
4. PR #295 body: fix the Lean paragraph (L5 status per b40e87a, re-checked; concrete SFP cases; the Lean audit count after round 3). The banned_words line should name its base and note the 2 hits carried from upstream.
5. #292: record this retrospective independent gate read, and lock a relabel rule (§8).

## 10. Next search (SU(3), Sp(2), G₂, dims ≤ 15): prereg changes needed before a blind run

Yes, changes are needed:
1. **Blind protocol.**
   - No development run on these groups.
   - Lock and **push** before running, so GitHub's push time anchors the order (M2).
   - A separate reader passes the Gate before the run.
   - Fixed script hash and seeds.
2. **State the reduction in advance.** For rank 2, zero-weight spaces are 2-dimensional, so the candidates are continuous families over a Weyl chamber, not single zonal vectors. Lock the parametrization, plus either an analytic argument for every member or a grid with declared resolution.
3. **Enumerate fully, with multiplicities and sums**, up to dim 15:
   - SU(3): adjoint 8, adjoint⊕trivial; 6 and 3 have no zero weight.
   - Sp(2): 5, 10, 5⊕5, 5⊕10 = 15, 14 (traceless Sym² of 5, which contains real QM d=5, Jordan).
   - G₂: 7, 14, 7⊕7.
   - Products with SU(2) factors.
   - Also U(2)/Sp(1)² in dims 9–15, which the proposal leaves out (spin-4 Z4 at 9, spin-1⊕3 at 10, B3×Z3 at 10, Sp(1)³ such as B3³ at 9).
4. **Compute G₀(K) for every candidate.** The symmetry group can be larger than the generating group, e.g. G₂ ⊂ SO(7) on S⁶ gives the ball B7 with G₀ = SO(7).
5. **Exact capacity.** The hit rule depends on N exactly, and grid LPs give only lower bounds. Lock an upper-bound method; central symmetry no longer applies to SU(3) adjoint orbitopes.
6. **Predeclare the likely tie.** The SU(3) generic adjoint (flag-manifold) orbitope has affine dimension 8 = 3²−1, a stabilizer that is a maximal torus (so SFP holds), and capacity plausibly 3. If hSFP holds, it is a **TIE** with complex QM at N = 3, which counts as a hit under G1. Predeclare its expected label and the tie handling. Also predeclare the Jordan test: the CP² orbit is complex QM itself.
7. **Hit rule for Jordan bodies.** Decide whether non-complex Jordan bodies (real QM d=5, quaternionic bit B5, B7) count as hits for "P1–P6 select complex QM". All lose on dimension at their capacities, but the rule should say so.
8. **Close L5 and L6 in the method:** non-exposed faces, the P6 hereditary bit-face clause, and P4 + P2 ⇒ P3 stated.
