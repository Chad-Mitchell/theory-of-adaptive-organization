# Results: third QM-selection search (SU(3), Sp(2), G₂ up to dimension 15; U(2), Sp(1)², Sp(1)³ and G × Sp(1)ᵏ in dimensions 9–15)

*Thursday 26 November 2026, written 08:50–09:20 ET (America/New_York). Append-only. Prereg `PREREG.md` in this directory, sha256 `6137e3a19c5df4b4e5dba34ffff0c7aafb40d70b5fb1bfade886590b5813e1b6`; script `search_qmsel3.py`, sha256 `7e49ef28654a1eb6d54ab274dea5f75d90df2e563ebc13d6e1e96a2cbcbe3345`; `list.out` `ad655d39…695a`; `toy_tests.py` `d2b71e31…8c40`; lock commit `e496428`. Gate read of the lock: PASS-WITH-FIXES (fixes F1–F4 are reporting rules, applied below). Raw output: `search_qmsel3.out` (sha256 `921332b4a11134d9f2ce6c763b49fe61761ae91c7b6a41e36b0f62504a356761`), committed as produced.*

## Launch (process rule of 2026-11-26)

- `git ls-remote` at 07:27:00 ET: `499ef043a6c45a8abb995d4d88758cb7b2dc5fdd refs/heads/forge-rnd-record-cost-2`. `499ef04` descends from the lock `e496428`, and no file in this directory changed between them.
- Fresh clone from GitHub into `/workspace/qmsel3-run`; `sha256sum -c PREREG.sha256` gave 4/4 OK there; numpy 2.5.5, scipy 1.18.1, python 3.13.5 (the pinned versions).
- The locked command (§0.9) was run once, from that clone only: started 07:27:19 ET, finished 08:48:05 ET, exit code 0. `run_launch.log` holds the ls-remote line, the clone path and both times.
- One launch, no restart. The operator's session was cut off at about 08:16 ET while the run was in progress; the run itself was not interrupted (one process tree throughout, checked with `pgrep`), and it was not relaunched. Progress was read during the run from the worker arguments with `py-spy dump` (read-only); no outcome was visible before the end, because the script prints all results at the end.
- `--run` passed its own guards: lock hashes, pinned versions, and the regenerated enumeration equal to `list.out` (927 bodies).

## Outcome: INCONCLUSIVE (0 HIT, 0 TIE, 1 TARGET, 11 OPEN, 915 MISS)

Under the overall rule of `PREREG.md` §2 G1 ("HIT if any body is HIT or TIE; else INCONCLUSIVE if any body is OPEN; else MISS"): **no body is a HIT or a TIE, and 11 bodies are OPEN, so the overall result is INCONCLUSIVE.** All 11 OPEN bodies are SU(3) adjoint orbits at the Weyl-singular directions, that is CP² orbits (see below); the script prints `RESULT: INCONCLUSIVE`. Secondary count without the bit-face clause (dimension only): 1 TIE, the TARGET body. No body reached the bit-face step.

| class (group as it acts) | bodies | MISS (cost) | MISS (SFP) | MISS (hSFP) | OPEN | TARGET |
|---|---|---|---|---|---|---|
| SU(3) on 8 (adjoint), d = 8 | 126 | 114 | – | – | 11 | 1 |
| SU(3) 8 × SO(3)ᵏ, d = 11–15 | 120 | 120 | – | – | – | – |
| Sp(2) on 5, d = 5 | 1 | 1 | – | – | – | – |
| Sp(2) on 10 (adjoint), d = 10 | 128 | 126 | 2 | – | – | – |
| Sp(2) on 14, d = 14 | 126 | 114 | – | 12 | – | – |
| Sp(2) on 5 ⊕ 10, d = 15 | 128 | – | 128 | – | – | – |
| Sp(2) 5 or 10 × SO(3)ᵏ, and Sp(2) × Sp(1) on 5 ⊗ 3, d = 8–15 | 79 | 77 | 1 | 1 | – | – |
| G₂ on 7, d = 7 (G₀ = SO(7)) | 1 | 1 | – | – | – | – |
| G₂ on 14 (adjoint), d = 14 | 132 | 132 | – | – | – | – |
| G₂ 7 × SO(3)ᵏ, d = 10–15 | 7 | 6 | – | 1 | – | – |
| U(2) through SO(3), d = 9–15 | 10 | 8 | – | 2 | – | – |
| Sp(1)² through SO(3)², d = 9–15 | 34 | 25 | – | 9 | – | – |
| Sp(1)³ through SO(3)³, d = 9–15 | 35 | 32 | – | 3 | – | – |
| **total** | **927** | **756** | **131** | **28** | **11** | **1** |

Every score above is the script's label, unchanged. Labels: each MISS on cost rests on a valid capacity upper bound (the λ-LP over orbit points, §4.3: **PROVED (in-model)** that the bound is valid; the number is **OBSERVED (numerical)**). Each hSFP MISS rests on a re-confirmed numerical failure certificate at depth 1 (**OBSERVED (numerical)**). Each SFP MISS rests on a numerical stabilizer-rank test (**OBSERVED (numerical)**), but see "Surprises" 2 and 3: 131 of them do not test what §3 intended.

### The TARGET body (F1)

| index | body | d | N_LB / N_UB | dim G₀ | Weyl points | recheck minimum | threshold |
|---|---|---|---|---|---|---|---|
| 124 | SU(3) 8 singular 270.0000° (CP² orbit) | 8 | 3 / 3 | 8 | 3 | −9.23 × 10⁻⁷ | −10⁻⁶ |

The recheck minimum is inside the threshold by 7.7 × 10⁻⁸. As the gate read (3a) showed, an accepted witness may be negative by up to 10⁻⁶ by construction, so the capacity lower bound holds to 10⁻⁶ (an ε-witness, ε = 10⁻⁶), not exactly. Its label stays **OBSERVED (numerical)**. Citing it as more than that needs an exact or tightened witness (cutting planes to 10⁻⁹, or the closed-form witness of complex QM₃), which would be a new, unregistered follow-up (A10). For this body the capacity 3 is also **KNOWN**: it is complex QM₃'s state space.

The §8 table's "exact B3 witness ≈ 0" refers to the closed-form witness in the toy test. The witness the scored path accepts for B3 sits at −7.6 × 10⁻⁷ (selftest), and for body 124 at −9.23 × 10⁻⁷.

### The 11 OPEN bodies

| indices | bodies | outcome | why |
|---|---|---|---|
| 10, 30, 50, 70, 90, 110 | SU(3) 8 angle 30°, 90°, 150°, 210°, 270°, 330° | OPEN | N_LB = 1, N_UB = 3: capacity interval straddles the threshold |
| 120, 121, 122, 123, 125 | SU(3) 8 singular 30°, 90°, 150°, 210°, 330° | OPEN | same |

- All 11 are CP² orbits: the six grid angles 30° + 60°·k coincide with the six singular directions, so the grid bodies 10–110 repeat the singular bodies 120–125. All 12 have dim G₀ = 8, 3 Weyl points (search equal to Weyl), SFP pass, hSFP pass at depth 1, N_UB = 3 (α = 0.3333) and the signature of complex QM (`jordan_type` = complex QM); only body 124 found a capacity witness.
- N_LB = 1 means the witness search accepted no pair at all, though the three Weyl points of a CP² orbit are perfectly distinguishable (KNOWN). **HYPOTHESIS:** the witness search is fragile at the acceptance tolerance: accepted witnesses sit between −6 × 10⁻⁷ and −10⁻⁶ (gate read 3a), so a witness whose cutting-plane minimum lands just below −10⁻⁶ is rejected. Not checked here; checking it would be a new, unregistered result (A10).
- They cannot become hits under G1 (a CP² orbit is complex QM itself, scored TARGET or "OPEN (TARGET-signature)"), but the prereg scores them OPEN, and the overall result is INCONCLUSIVE because of them. Settling them later does not change this prereg's result (A10).

### HIT and TIE bodies (F1, F2)

None. F2 (polarity) is therefore empty: no HIT or TIE needs the depth-≥2 condition discharged. For the record, the TARGET body is an adjoint orbitope and so polar, and by Biliotti, Ghigi and Heinzner, "Polar orbitopes", Comm. Anal. Geom. 21 (2013) 579–606, Theorem 3.2 (DOI 10.4310/cag.2013.v21.n3.a5, checked on Crossref), all its proper faces are exposed (KNOWN, cited).

### MISS bodies resting only on a not-ball face of dimension ≤ 2 (F3)

None. No body reached the bit-face step (every body was settled earlier as MISS on cost, SFP or hSFP, or as OPEN or TARGET), so no MISS rests on a bit face.

### Predeclared expectations (§5) against the outcome

- **SU(3) flag orbitope (predicted TIE at about 50%): MISS on cost.** All 114 non-singular SU(3) adjoint bodies have N_UB = 2 (α between 0.353 and 0.49994), so d = 8 > 3 and they lose on cost before any face test. The three Weyl-permuted points diag(a, b, c) are not perfectly distinguishable in the flag body by the bound. The rival G3 ("P7 is needed", predicting a HIT or TIE from the flag body) gets no support from this run. Label: **OBSERVED (numerical)** (valid bound, numerical value).
- **Weyl count:** 3 for CP² (12 of 12, as expected). The flag count 6 was not reached (MISS on cost first).
- **real QM₅ (Sp(2) 14 at its singular directions): hSFP fails** (bodies 375 and 378, plus 10 nearby grid angles 60°–72° and 240°–252°), as expected.
- **B5 (Sp(2) 5) and B7 (G₂ 7, G₀ = SO(7), dim G₀ = 21 found): MISS on cost**, as expected.
- **Products and SO(3)-only bodies in 9–15: MISS** (cost or hSFP), as expected.
- **g₀ closure:** passed for every body (largest residual 1.7 × 10⁻⁹ < 10⁻⁸). **Weyl match:** every body that reached the step matched (40 bodies). **Time budget:** no body ran out (longest 372 s; total CPU 38 393 s).

## Surprises (reported, not explained away; no score changed)

1. **The flag body loses on cost.** The prereg's main expected tie did not happen: N_UB = 2 for every generic direction.
2. **Sp(2) on 5 ⊕ 10 (128 bodies) was not the intended family.** All 128 fail SFP, 125 with stabilizer rank 0. Reading the locked enumeration (`rank2_bodies`): the 5-part `V5` and the 10-part `V10` are zero-weight vectors for two *different* random maximal tori (two separate `tfixed_space` calls), so v = (V5, w) is generically fixed by no torus. §3.1 intended v in the zero-weight space of one torus. The scores stand as MISS for the bodies the script actually built (OBSERVED (numerical)), but **the intended Sp(2) 5 ⊕ 10 zero-weight family is untested** by this run (OBSERVED, from reading the code). It has to be listed as not covered next to the A8 scope list.
3. **Three SFP MISSes contradict a known fact.** Bodies 249 and 250 (Sp(2) on 10, singular 90.5322° and 135.5322°) and 914 (Sp(2) 10 singular 226.4185° × SO(3)) report stabilizer rank 1 < 2. On the adjoint representation the zero-weight space is the Cartan subalgebra, and every Cartan element is fixed by its torus (KNOWN), so the true stabilizer rank is 2. **HYPOTHESIS:** the rank test misreads the larger stabilizer at these singular directions (the tolerance in `sfp_rank_test`). These three are false MISSes on SFP. Under §6 they stay as scored (relabels never move a miss to a hit, and a later check is a new, unregistered result); a hand check would most likely still give MISS on cost (every generic Sp(2) 10 body has N_UB ≤ 3 < 4), but that was not computed.
4. **The witness search found no pair in 11 of 12 CP² orbits** (OPEN above). This is the false-OPEN direction of the gate read's point 3a.
5. **The SU(3) grid repeats the singular directions** (6 duplicate bodies). Harmless for the score; noted for the next enumeration.

## What this does and does not show

- **Does:** within the locked family, no body other than CP² orbits passes the cost test with SFP, hSFP at depth 1 and the capacity bounds: 915 bodies are MISS and none is a HIT or a TIE. The flag body, the main candidate for a tie, loses on cost (OBSERVED (numerical)).
- **Does not:** give a MISS result: the overall result is INCONCLUSIVE because of the 11 OPEN CP² bodies (A10: settling them later is a new, unregistered result and does not change this one). It does not test the intended Sp(2) 5 ⊕ 10 zero-weight family (Surprise 2), faces of exposure depth ≥ 2 (A1), or anything outside §3.4 (SU(4) adjoint, Sp(3) on 14, Spin(7) on 8, B9–B15 outside the listed products, products of two rank-2 groups, dimensions above 15). It does not prove any capacity, face or hSFP statement; those are numerical.
- **Next (G5, INCONCLUSIVE branch):** report the OPEN bodies; no claim either way. A new prereg (not an edit of this one) should: build the 5 ⊕ 10 vectors from one torus; fix the stabilizer-rank tolerance at singular directions; make the witness search robust at the tolerance (cutting planes to 10⁻⁹ before acceptance); remove grid duplicates of singular directions; add the B3 × B3 proper-face case to the selftest (gate read 3c); and then cover the rank-3 groups.

## Timestamp note (F4, append-only)

`PREREG.md`'s header says "§0.10 and §8 added 06:47–07:00 ET". The lock commit `e496428` was committed at 06:50:23 ET, inside that window, and pushed at 07:11:45 ET. The stated end of the window (07:00) is later than the commit, so the writing of §0.10 and §8 ended by 06:50:23 ET. `PREREG.md` is not edited.

## Deviations

None during the run. See `DEVIATIONS.md` (one note, F4, appended after the run).
