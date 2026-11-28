# PREREG DRAFT C4R: the corrected C4 run (shape ratio R(s) against a Poisson-sprinkling control)

*Draft, 26 Nov 2026, written about 10:30–10:50 EST. Local only: not locked, not committed, not pushed. A separate reviewer gates it. Locking means pushing this file, the code and the hashes to the fork. Nothing in §§1–6 may change after the lock. Toy runs on non-scored seeds (1–999) were made while drafting and are reported in §8. No scored seed (≥ 10001) has been run.*

Labels: PROVED (in-model) · HYP · KNOWN · OBSERVED (toy, non-scored) · CHOSEN.

## 0. Blindness statement (required by C4_RECORD_ORDER.md §5, C5-2, and STEPBACK §16)
- **This test is NOT blind.** The review (`rnd/review_c4/HOSTILE_REVIEW_C4.md`) simulated this world and reported R ≈ 1.12 at s = 0.5 and R ≈ 2.04 at s = 0.9.
- My own toy runs (§8) reproduced R(0.9) ≈ 2.03 on non-scored seeds before any scored seed was drawn.
- The outcome near the cone is also fixed on paper by C4-4 (PROVED in-model, as narrowed in C5-4).
- So this run is a **registered check**: the code, the control and the decision rule are fixed in public before the scored seeds. It is not a discovery test. This follows C5-1/C5-9, which also say a run is "not recommended" (see §9).

## 1. Hypothesis
- **H (from C4-4, PROVED in-model, flat homogeneous 1+1 only):** record order on the fixed lattice (per-site rate-1 Poisson clocks; a record depends on the latest records at i−1, i, i+1; order = transitive closure) is not Lorentz-like in chain-length shape. With c fixed by the front speed v = λa = 1 (C4-1), the ratio R(s) exceeds 1 and grows towards the cone.
- **Null shape (KNOWN, Brightwell–Gregory 1991):** a uniform Poisson sprinkling of 1+1 Minkowski with light speed 1 has longest chain ∝ proper time, so R ≡ 1 asymptotically. Finite-size (Tracy–Widom-type) corrections are of order N^(−1/3).

## 2. Observable and metrics
- **L(x, t):**
  - *Lattice:* the longest chain from the origin record (0, 0) to the latest reachable record at site x by time t, counting the origin.
  - *Sprinkling:* the longest chain from the origin to the event (x, t), computed as the strict 2D longest increasing subsequence in light-cone coordinates of an independent Poisson sprinkling of that causal diamond, plus 1.
- **Per seed:** R_j(s) = L(⌊sT⌋, T) / (L(0, T)·√(1 − s²)) for s ∈ {0.25, 0.5, 0.75, 0.9}, using c = 1 (C4-1).
- **Primary metric:** ΔR(s) = mean_lattice R(s) − mean_control R(s), with Welch standard error and z = ΔR/SE.
- **Secondary (reported, not scored):**
  - (a) R with the measured front speed ĉ = front/T in place of 1;
  - (b) lattice T = 4000 vs T = 16000 (finite size);
  - (c) the best-fit "chain-length light speed" c′, which minimises Σ_s [R_lat(s) − √(1 − s²/c′²)/√(1 − s²)]², with residuals (the C4″ question; descriptive only);
  - (d) the Draft C exponent at s = 0, 0.5, 0.9, to show it is blind.

## 3. Worlds, sizes, seeds (CHOSEN)
- **Lattice (treatment):** `c4r_lattice.c`, my independent rewrite of the model, with a window of ±(1.2T + 200) sites (the run aborts if the front gets within 5 sites of the edge).
  - Scored: **T = 16000, seeds 10001–10016** (16 seeds).
  - Secondary: T = 4000, seeds 10101–10116.
- **Control:** `c4r_sprinkle.c`, light speed cp = 1, T = 1, density ρ = 3.2×10⁷, so about 1.6×10⁷ points in the s = 0 diamond. **Seeds 20001–20016** (16 seeds). Each ray is sprinkled independently.
- **RNG:** xoshiro256** with splitmix64 seeding (offsets are in the code). Seeds 1–999 are toy only and never scored.
- **Disclosed:** the review used seeds 1–8 and 11–14 with its own code. They are disjoint from these seeds, and this code is different.

## 4. Decision rule (code: `c4r_decide.py`, function `decide`)
- **Control validity (V):** |mean_control R(s) − 1| ≤ 0.02 at every s ∈ {0.25, 0.5, 0.75, 0.9}. If V fails → **OPEN (control invalid)**, and nothing is read from the lattice.
- **HIT:** V holds, ΔR(0.9) ≥ 0.20 with z ≥ 5, and ΔR(s) > 0 with z ≥ 3 at each of s = 0.5, 0.75, 0.9.
  - Meaning: the lattice's chain-length shape is distinguishable from Lorentz-like at c = front speed, as C4-4 predicts.
- **MISS:** V holds and |ΔR(s)| ≤ 0.02 at all four rays.
  - Meaning: the lattice is indistinguishable from the sprinkling. This would be an **open miss** for C4-4 as narrowed (or a code error), and would trigger a code audit before anything else.
- **OPEN:** any other outcome. For example, a positive effect below the 0.20 threshold, or mixed signs.
- **Threshold reasoning (CHOSEN, disclosed as non-blind):** 0.20 at s = 0.9 corresponds to a sprinkling with a light speed about 7% off (cp ≈ 1.07). That is well above the control's finite-size bias (≈ −0.006 at toy size) and below the expected lattice value (≈ 1.0).

## 5. Analysis plan
1. Run the 16 + 16 scored seeds once.
2. Apply `decide` once and report all four rays, plus secondaries (a)–(d).
3. No reruns, no extra seeds, no change of rays or thresholds.
4. A crash or window abort is reported as-is and leaves that seed out. If more than 2 of the 16 seeds in either arm are left out, the outcome is OPEN.

## 6. Files to hash at lock (SHA-256; recomputed at lock, values in §10 are provisional)
`PREREG_DRAFT_C4R.md` (this file), `c4r_lattice.c`, `c4r_sprinkle.c`, `c4r_decide.py`, and the scored driver `run_scored.sh` (to be written at lock: two `xargs` lines over the seeds in §3 writing `scored/lattice_T16000.txt`, `scored/lattice_T4000.txt` and `scored/control.txt`, then one `decide` call).

## 7. Prior art (all DOIs verified on Crossref earlier, in `../crossref_c4.txt` and `rnd/review_c4/crossref_review_c4.txt`; none added here)
- Brightwell & Gregory 1991: the longest-chain ∝ proper-time benchmark. Cited as in C4_RECORD_ORDER; this draft adds no DOI.
- Bombelli–Henson–Sorkin 2009 (10.1142/S0217732309031958) and Dowker–Henson–Sorkin 2004 (10.1142/S0217732304015026), framed as in C5-6.
- Kingman 1968 (10.1111/j.2517-6161.1968.tb00749.x) for the existence of γ(s).

## 8. Self gate-read for blindness: can the test detect the effect against the Poisson control? (OBSERVED, toy seeds only)
Files: `toy_power.sh`, `toy_analyze.py` → `toy/toy_analyze.out`, `toy_exponent.py` → `toy/toy_exponent.out`.

**Planted effect.** A Poisson sprinkling whose true light speed is cp, analysed with c = 1. This plants a known R(s) = √(1 − s²/cp²)/√(1 − s²) > 1 that grows towards the cone, the same shape of effect as H.
- Toy size: N0 = 10⁶ points (16× smaller than scored).
- 10 batches of 16 planted seeds were each compared against 10 disjoint batches of 16 Poisson-control seeds.

| cp | planted R−1 at s = 0.5 / 0.75 / 0.9 | measured ΔR(0.9) (mean of 10) | median z(0.9) | decisions (10 batches) |
|---|---|---|---|---|
| 1.00 (null) | 0 / 0 / 0 | 0.000 | 0 | MISS 10 |
| 1.02 | 0.006 / 0.025 / 0.080 | 0.080 | 25 | OPEN 10 |
| 1.05 | 0.015 / 0.058 / 0.182 | 0.183 | 58 | OPEN 10 |
| 1.10 | 0.029 / 0.106 / 0.319 | 0.320 | 95 | HIT 10 |
| 1.20 | 0.050 / 0.180 / 0.517 | 0.520 | 152 | HIT 10 |
| 1.96 | 0.116 / 0.397 / 1.038 | 1.042 | 306 | HIT 10 |

- **Control alone** (160 seeds): mean R = 0.9997, 0.9994, 0.9972, 0.9939 at s = 0.25, 0.5, 0.75, 0.9; per-seed sd 0.006–0.009. V passes with room, and the bias shrinks as N^(−1/3) at scored size.
- **Reading:**
  - The planted ΔR is recovered to ±0.003 at every plant.
  - The null never reads HIT and always reads MISS, so MISS is reachable.
  - Plants below the threshold read OPEN; plants above it read HIT, 10/10.
  - Noise is negligible against the thresholds, so **the decision is set by the effect-size thresholds, not by power**. Power is ≈ 1 for any plant with ΔR(0.9) ≥ 0.25.
- **Old observable is blind (confirms C5-1).** The Draft C exponent of L against τ at c = 1 is 1.013 / 1.013 / 1.005 (s = 0, 0.5, 0.9) for the control and 1.007 / 1.010 / 1.007 for the cp = 1.96 plant. That observable cannot tell a 2× planted light-speed error from the null. R(s) separates them at z ≈ 300.
- **Toy lattice** (T = 4000, toy seeds 1–16) against control batch 1 reads **HIT**: R = 1.025, 1.123, 1.407, 2.033 at s = 0.25, 0.5, 0.75, 0.9. This shows again that the outcome is known in advance (§0).
- **Secondary (c) at toy size (OBSERVED):** the best-fit chain-length light speed is c′ = 1.962, with residuals ≤ 0.010 at all four rays. So for |s| ≤ 0.9, lattice chain lengths look like those of a sprinkling with light speed ≈ 1.96, while the order's light speed is 1 (C4-1). This is the C4″ question; see §9.

## 9. Doubts (for the gate reviewer)
1. **Value.** The outcome is known (paper, review, toy). A HIT adds a public, code-fixed check and nothing new. The C5-9 rescore (≈ 0.8/h) already said "not recommended". The run itself is cheap (minutes of CPU), but the lock and review cost is not.
2. **Thresholds set after seeing data.** The 0.20 threshold and the 0.02 bands were chosen knowing R(0.9) ≈ 2.04. They are disclosed, and are far from the expected value, but they are not blind.
3. **What a HIT means.** R(s) against c = 1 detects a mismatch between the order's light speed (front, 1) and the chain-length "light speed" (c′ ≈ 1.96). That is exactly C4-4's content, but it does not exclude, on its own data, a Lorentzian description with c′ ≈ 2 for lengths alone. Excluding that needs the order (C4-4(a)), not this run.
4. **C4″ observation (OBSERVED toy, novelty unknown).** A single c′ fits lattice R(s) to within 0.01 for s ≤ 0.9. Residuals are small but systematic (+0.006, +0.010 at s = 0.5, 0.75). Whether γ(s) is exactly a hyperbola in a rescaled cone is open, and no prior art was searched for it here. It is scored as a descriptive secondary only.
5. **L-definition match.** The lattice endpoint is the latest record at site x by time t, while the control endpoint is the event (x, t) itself. Both are "longest chain from the origin to (x, t)" because chains are monotone in the endpoint. The lattice may slightly undercount relative to an exact event; this effect is O(1) records and negligible at L ≈ 6×10⁴.
6. **Independent rays in the control.** Sprinkling each diamond independently makes the control's R(s) noisier than a single shared sprinkling would. That is conservative for z, and irrelevant at these z values.
7. **Lattice code independence.** `c4r_lattice.c` is a rewrite with the same update rule as the review's `c4_lpp.c`, not a different algorithm. A shared misunderstanding of the rule would not be caught. The rule itself was brute-force checked by the review (0 mismatches).

## 10. Provisional hashes (will change if the gate requests edits)
See `hashes_draft.txt` (sha256sum of the files in §6 that exist now; `run_scored.sh` not yet written).

## 11. Shelved (appended 26 Nov 2026, about 10:40 EST; decision by the parent, using the theory's own scoring method; §§0–10 are left as written)
- **Not locked, not run on scored seeds.** The outcome is already known (C4-4 on paper, the review's simulation, and the §8 toy lattice, which reads HIT). So the expected information is near zero, while locking and gating carry a real cost.
- **Rescore as a check:** p_hit ≈ 0.99, V ≈ 0.5 (a public, code-fixed check of a known outcome), cost ≈ 2.5 h (lock + gate read + run + write-up) → **≈ 0.2 per hour**.
- **Kept as a ready-made registered check for Ace, if he wants one.** This draft, `c4r_lattice.c`, `c4r_sprinkle.c`, `c4r_decide.py`, `toy_power.sh`, `toy_analyze.py`, `toy_exponent.py`, `toy/*.out` and `hashes_draft.txt` stay as they are. To use it: write `run_scored.sh` (§6), have it gate-read, then lock.
- **C4″ clue logged as a HYP.** One chain-length light speed, c′ ≈ 1.962, fits the lattice R(s) for s ≤ 0.9 with residuals ≤ 0.010 (toy, T = 4000, 16 seeds; OBSERVED). HYP: the lattice time constant γ(s) is close to a Lorentzian hyperbola γ(0)·√(1 − s²/c′²) with c′ ≈ 2, about twice the order's front speed v = 1.
  - It cannot be exact up to the cone without checking the front: L at the front site/t ≈ 3.38 (review) vs γ(0)·√(1 − 1/c′²) ≈ 3.49.
  - **Quick prior-art search** (web search, 26 Nov 2026; DOIs checked on Crossref, in `../c12cg/crossref_c12cg.txt`):
    - The model is a last-passage percolation on ℤ × ℝ with Poisson points on lattice lines and steps of −1, 0 or +1 sites. The closest exactly solved relatives are Seppäläinen 1996 (EJP 1:5, 10.1214/ejp.v1-5; Poisson points on lattice lines, Hammersley-type, with up-right paths) and the corner-growth/LPP shape theory (Seppäläinen 1998, AoP 26:1232, 10.1214/aop/1022855751; Martin 2004, AoP 32:2908, 10.1214/009117904000000838, shape-function continuity and boundary asymptotics).
    - In those totally asymmetric models the exact shapes are of the (√x + √y)² type, which is a hyperbola in light-cone variables only for the Poisson (Hammersley) case.
    - I found no exact shape for this symmetric, lazy, three-step variant, and no causal-set paper giving an "effective light-cone speed" for a regular lattice. Dowker–Henson–Sorkin 2004 (10.1142/S0217732304015026) argue that a lattice cannot be Lorentz-invariant, which is consistent with but does not address c′.
    - So novelty is unknown, and the search was quick, not exhaustive.
  - **The test that would settle it:** compute γ(s) more precisely (larger T, the s → 1 limit) and compare it with the hyperbola, plus a literature check of LPP with symmetric nearest-neighbour steps. Not scored here (it sits under C4″, which C4_RECORD_ORDER §3 rated low value).
