# REVIEW_WORLDTRACK: independent hostile review of WORLD_TRACK.md (FOR-40)

*26 Nov 2026, about 19:05–19:25 ET. Reviewer did not write the target. Local note only: no commits, no pushes, no email. WORLD_TRACK.md and every locked file were read only. Labels: **PIM** = proved in-model; **ELEMENTARY**; **KNOWN**; **HYP**; **OBSERVED** = numerical output of the scripts in this folder. "Open miss" marks a prediction that did not come out. DOIs below were checked on Crossref this session (`rv_crossref_dois.txt`, 10 of 10 OK).*

Target: `rnd/stepback/WORLD_TRACK.md` (final SHA-256 `568eff32…6ed9`, 34 236 bytes), scripts and outputs in `rnd/stepback/worldtrack/`. Context read: `REQUIREMENTS_FIRST.md` (§7 Route 1, §10), `rnd/review_p15/REVIEW_P15.md`.

## 0. Outcome in five lines

1. **Process holds.** All four logged hashes match exact byte-prefixes of the file, and each prefix ends where the WORKLOG says. Every scored output's mtime falls after its pre-statement hash time. One gap: Step 0 shares the minute 18:31 with its first scripts, so the order can't be checked at the seconds level.
2. **Both scores follow the hashed criteria literally, and both reproduce in my own code.** Step 0 gives 60 of 60 single crossings. Step 1 matches n* within 0.18%, s* exactly and J* within 1e−5 in all 432 primary cells. H-a through H-d pass.
3. **Step 0's α\* values come from the menu cap.** The single-crossing count survives larger menus, but α\* does not. With 3× the menu, α\* triples at λ = 1000. At N = 1440, α\* reaches 0.9975 at λ = 30, against 0.325 in the scored menu. The reported α\*(T, λ), "α\* falls with λ" and "α\*·λ → 12" describe the menu, not the class.
4. **Step 1's R-regime numbers are one elementary scaling identity.** Every pre-stated R-regime fit follows in closed form at leading order: ρ\* = 0.607, H\* = 1.107 nats, s\*σ_w√x = 1.746, n\*x^{−1/4}σ_w^{1/2} = 2.888, an equal read/loss split, and J\* ∝ σ_w√x. "Beyond Gish–Pierce" is true only because Gish–Pierce has no time in it. The Kipnis–Goldsmith–Eldar attribution is misstated: they show finite bits per sample is always suboptimal, so they predict no interior ≈ 1.1 nats per read.
5. The claim that the integer n\* exists only for a noiseless register is **overstated**. Within the class, "integer" holds by construction. "Only noiseless" and "a continuous noisy memory beats every finite register" were not tested, and they rest on a HYP mapping. The proposed "information budget survives a change of class" is contradicted by KGE's result for ideal coding (hypothesis-level). **PASS-WITH-FIXES.**

## 1. Were the pre-statements hashed before computing?

Method: SHA-256 of every byte-prefix of the current WORLD_TRACK.md was compared with the WORKLOG hashes (WORKLOG.md lines 280–290). File mtimes come from `stat`, in ET.

| WORKLOG entry (ET) | hash | matches prefix ending at | first dependent output (mtime, ET) | order |
|---|---|---|---|---|
| 18:31 Step 0 pre-statement | `645e5857…b105` | byte 5491, line 56 (end of §0.6) | tl_core/tl_gate 18:31:37; **tl_run.py 18:31:51**; tl_run.json 18:32:29 | consistent; **not checkable within the minute** |
| 18:41 Step 0 results + §0.7 | `f3563199…576f` | byte 12 313, line 123 (end of §0.11) | (results) | OK |
| 18:42 Step 1 pre-statement | `ab799c39…0e64` | byte 22 550, line 217 (end of §1.7) | wt_core.py 18:43:34; wt_check.out 18:43:37; wt_run.jsonl 18:56:30 | OK (later minute) |
| 19:01 Step 1 results | `ef29a393…b210` | byte 33 092, line 311 | wt_post.out 19:00:10, wt_berger.out 19:00:35 | OK |
| 19:01 §2 next steps | `568eff32…6ed9` | whole file | — | OK |

- **OBSERVED:** the file is append-only across the four hashes; each earlier prefix is intact.
- **Gap (low–medium):** the Step 0 hash time has minute resolution (18:31), and the gate and run scripts were also created in minute 18:31. The scored run (`tl_run.py`, written 18:31:51 and finished 18:32:28) could, in principle, have started before the hash was logged. Nothing suggests it did. The gate is a reproduction check, not a scored number.
- **Disclosed and acceptable:** the header says "started 18:35" against an actual 18:31 (WORKLOG 280). §0.7 was added after hashing (fix 8 of REVIEW_P15), and its rule (ties are not in W) was already fixed by the hashed definition of W. No earlier Step 1 computation exists: `reqfirst/` holds only Crossref files, and `trackfirst/` files all postdate 18:58.
- **Disclosure gap (medium):** §1.5 says it "keeps REQUIREMENTS_FIRST §7 Route 1's criteria, made operational". Route 1's HIT required "no corner solutions", with corners at n = 3 or the range edge. The hashed Step 1 text redefines s\* = 1 (the tick) and n\* = 1 as "stated regimes, not corners". That change came before computing, so it is legitimate. But s\* = 1 binds in **150 of 432 cells (35%)**. Under Route 1's wording those cells would arguably be corners, and H-d would fail in more than 5% of cells (OPEN). The relaxation must be stated as a change, not as "kept".

## 2. Do the scores follow the hashed criteria literally?

**Step 0 (§0.4).**
- HIT needs ≥ 95% of proper-W cells with W = [0, α\*). Observed 60 of 60, with 0 ambiguous and 0 empty or full. `tl_analyse.py` implements exactly W = {Δ > 1e−12}, ties > 10% → ambiguous, single = W[0] and one change.
- The P15 check passes with 0 endpoint violations.
- The triviality test was applied as written: argmins move in 60 of 60 cells, so the result is "not trivial" by that test.
- The secondary prediction is correctly scored as an open miss (0 of 24).
- **Literal score: HIT. Confirmed.**

**Step 1 (§1.5).**
- H-a: 0 of 432. H-b: 56 pairs, median 0.454, 98.2% in the window. H-c: 180 pairs, median 0.968, 85.0% in the window. H-d: 0 edges.
- S1 pass, S2 pass, S3 fail (5 of 8 rows). Bar A: A1 yes, A2 no. Bar B: trivial.
- Each is computed in `wt_analyse.py` / `wt_post.py` as the hashed text defines it.
- **Literal score: HIT. Confirmed.** The S3 open miss is correctly kept and not rescored. The "s\* ≥ 3: 8 of 8" reading is marked post hoc.

## 3. Independent reruns (own code; nothing imported from `worldtrack/`)

### 3.1 Step 0 (`rv_tl.py`, `rv_tl2.py`, `rv_tl_bigmenu.py`)

Own implementation:
- distances from the width breakpoints, using a superset of directions (edge normals and vertex directions);
- circulant min-plus DP;
- disk optimum on a 20 001-point grid with bounded scalar refinement;
- an α grid of 2001 points (step 0.0005).

Results:
- **Gate:** 0.5000, 0.5942 and 0.4825 reproduced.
- **Scored menu N(T) = max(60, 6T + 10):** **60 of 60 single-crossing** (`rv_tl2_1.json`). The largest |α\*(mine) − α\*(author)| is 4.96e−4, which is within my grid step. The largest Δ(1) is −6.1e−6. OBSERVED, and it matches.
- **Numerical fragility (low):** a first run of mine evaluated the disk on a grid with no refinement, so its values were upper bounds within about 1e−9. That run showed 3 spurious extra crossings (`rv_tl_menu.out`, superseded). With exact refinement they vanish (`rv_tl_zoom.py`). The 1e−12 threshold in W is far below the 1e−6 to 1e−4 size of Δ, so the score depends on the disk optimizer being accurate to about 1e−10. The author's golden refinement achieves this.
- **Menu cap: the main Step 0 finding** (`rv_tl2_3.json`, `rv_tl_bigmenu.json`, `rv_tl_probe.out`).
  - The best polygon at α\* lies within 10% of the cap N(T) in **22 of 60** cells of the scored menu, and in **17 of 30** cells with λ ≥ 30.
  - With the menu tripled (3N(T)), single crossings are 59 of 60, so HIT still holds. The one exception is T = 4, λ = 2, with 3 crossings and a re-entry of size 2.6e−7. But α\* moves a lot:

| T, λ | α\* at N(T) | α\* at 3N(T) | α\* at N = 720 | α\* at N = 1440 |
|---|---|---|---|---|
| 8, 30 | 0.325 | 0.8745 | 0.9975 | 0.9975 |
| 8, 1000 | 0.011 | 0.0415 | 0.1575 | 0.300 |
| 20, 30 | 0.3355 | 0.7925 | 0.990 | 0.9975 |
| 20, 1000 | 0.0115 | 0.035 | 0.065 | 0.130 |

  - At λ = 1000, α\* grows roughly in proportion to N, and the polygon at α\* always sits near the cap (n = 1425 at N = 1440). At λ = 30, α\* is already within one grid step of 1.
  - **OBSERVED:** the scored α\* values, "α\* decreases with λ" and "α\*·λ → ≈ 12 for T ≥ 8" are properties of the truncated menu.
  - **HYP:** over all regular polygons (the unbounded SR_B class), α\* → 1. That would mean some polygon is strictly cheaper at every α < 1, and the disk is only weakly best at the pure positional loss. The single-switch shape itself appears robust: one crossing in 8 of 8 big-menu cells.
  - The margins are tiny (|Δ| ≈ 1e−7 to 1e−4), so "polygons win" means "win by a hair".

### 3.2 Step 1 (`rv_wt.py`, `rv_wt_score.py`)

Own implementation:
- read entropy H(R′|R) from the closed-form integral of Φ̄ over the uniform cell offset (G(−y) = φ(y) − yΦ̄(y), folded mod n);
- a wrapped-normal entropy by direct numerical integration for ρ > 40;
- the same loss L as the target;
- a coarse grid of n up to 1e7 and s up to 1e9 (wider than the author's), followed by integer refinement with exact H.

Results:
- **All 432 primary cells:** n\* agrees within |Δ ln n| ≤ 0.0018 (median 0), s\* is identical in every cell, and J\* agrees within a relative 1.1e−5. My run gives 0 far near-minima and 0 edge cells. OBSERVED.
- **My rescoring of the hashed criteria:** H-b 56 pairs, median 0.454, 98.2% in the window. H-c 180 pairs, median 0.968, 85.0% in the window. H-a 0. H-d 0. **HIT reproduced.**
- **Scaling identity (reviewer argument; PIM to leading order in σ_w → 0, s ≫ 1, Γ = 0, wrapping ignored).**
  - With L ≈ π²/(6n²) + σ_w²s/4 and the unwrapped read entropy depending only on ρ = σ_w√s·n/(2π), substituting n = 2πρ/(σ_w√s) gives J = h(ρ)/s + xσ_w²s·g(ρ), where g = 1/(24ρ²) + 1/4.
  - Minimizing over s gives s\* = √(h/(g x σ_w²)) and J = 2σ_w√x·√(h(ρ)g(ρ)), then one minimization over ρ. So:
    - ρ\* and H\* are pure numbers;
    - s\* ∝ 1/(σ_w√x) and n\* ∝ x^{1/4}σ_w^{−1/2} hold exactly;
    - read cost = loss cost at the optimum (the A/s + Bs split).
  - Numerically (`rv_wt_score.out`):

| quantity | identity | target's fit |
|---|---|---|
| ρ\* | 0.607 | 0.604 |
| H\* | 1.107 nats | 1.10 |
| s\*σ_w√x | 1.746 | 1.75 |
| n\*x^{−1/4}σ_w^{1/2} | 2.888 | 2.89 |
| J\*/(σ_w√x) | **1.2675** | 1.244 |

  - The 1.244 is a median pulled down by small-s cells, where the a = 0 timing makes the mean age (s − 1)/2. Cells with σ_w ≤ 0.01 and s\* ≥ 30 give 1.253–1.267.
  - So S1, S2, the R-regime half of H-c, the "equal split" and the σ_w√x cost scaling are **one ELEMENTARY identity, not separate observations**. The K regime is Gish–Pierce with a keep price (A2, already conceded), and the composition n\*^{−2} = n_K^{−2} + n_R^{−2} is additive marginal prices (already conceded).

## 4. Do the HITs come from grid edges, the menu cap, the tick or rounding?

| source | Step 0 | Step 1 |
|---|---|---|
| grid edges | no (my α grid of step 0.0005 agrees) | no: 0 edges in both runs; my grid reaches n = 1e7 and s = 1e9 |
| menu cap | **the single-crossing count: no (59–60/60 at 3N; 8/8 at N = 720 and 1440). α\* values: yes** | no |
| tick limit | n/a | H-c excludes s\* < 3 by its own rule. H-b restricted to s\* ≥ 3 gives 53 pairs, median 0.459, 98.1%; s\* ≥ 10 gives 40 pairs, median 0.475, 97.5%. H-a passes in the 150 tick-bound cells, but there the optimum sits at the lower bound s = 1, so calling it "interior" is false in 35% of cells |
| rounding | no | H-c with s\* ≥ 10: median 0.976, 81.0% in the window; s\* ≥ 30: 0.982, 77.9%. The pass holds but thins, and the misses come mostly from the σ_w = 0.1 → 0.3 pair (median 0.834), where wrapping matters, not from rounding |

## 5. Novelty: is "beyond Gish–Pierce" right?

- **Literal Bar A: met (A1).** n\* depends on σ_w. This tells us little: Gish–Pierce (static quantization, no time) is the wrong comparator for a tracking problem. Any rate-priced tracking of a Wiener process has the drift in its design scale. Berger (1970) gives D(R) = 2σ²/(π²R) per unit time (R in nats). Pricing rate against a stake gives J_B = 2σ_w√x/π, the same σ_w√x scaling. §3.2 shows the register's whole R-regime design follows from scaling.
- **The Berger formula is now checked, not only recalled (W4).** KGE (arXiv 1608.04679, eq. at line 87 of `kge_excerpt.txt`, citing Berger) state D_W(R) = 2σ²/(π² ln 2)·R^{−1} with R in bits. That is the target's formula in nats. So J_B and the "J\*/J_B ≥ 1" check move from HYP to KNOWN. The register's limit ratio is 1.2675/(2/π) = 1.99, against the observed maximum of 1.990.
- **The KGE attribution in §1.6 and §1.10 is misstated (medium).** KGE show that the ratio D(f_s, R)/D_W(R) is governed by bits per sample. They also show D_W is reached "only as the sampling rate goes to infinity, implying that encoding with a finite number of bits per sample always leads to sub-optimal performance" (`kge_excerpt.txt`). Under ideal block coding there is therefore **no interior optimum** in bits per sample: it runs to 0. The interior ≈ 1.1 nats per read here is a property of the chosen class: scalar register, renewal reads, and a read price H(R′|R) with no block coding. It is not "KGE's finding in a read-floor version". Bar B's overall call (trivial in substance) stands, but the reason must change: it is the §3.2 scaling identity (ELEMENTARY), not KGE.
- **Prior art to name as related.** Metadata was verified on Crossref this session, but I **did not read** the content of these papers, so no specific result from them is claimed: Åström & Bernhardsson 2002 (periodic against event-based sampling, 10.1109/cdc.2002.1184824); Rabi, Moustakides & Baras 2012 (10.1137/090757125); Sun, Polyanskiy & Uysal 2020 (sampling the Wiener process for remote estimation, 10.1109/tit.2019.2937336); Neuhoff & Gilbert 1982 (causal source codes, 10.1109/tit.1982.1056552); Tatikonda, Sahai & Mitter 2004 (10.1109/tac.2004.834430). Whether the exact constants (ρ\* = 0.607, H\* = 1.107) appear in that literature is OPEN.
- **The wording sent to Chad needs qualifying.** "That goes beyond the standard quantizer result, because the design depends on the world's drift" is true only against static quantizer sizing. It should say the drift dependence is the expected scaling for sampled Wiener tracking (Berger 1970; KGE 2019), and that its constants follow from an elementary identity in the chosen class.

## 6. Is "the whole-number n\* exists only for a noiseless register" right?

**Partly; overstated as worded.**
- **Right (PIM for this class):** in the n-level register class, n is an integer by construction. A finite optimum is forced because noiseless writes make each read write about ln n − O(1) nats, and holding costs c_KΓ ln n. So the continuum is excluded on the cost side (§1.2, consistent with REVIEW_P15 fix 8).
- **Not shown:**
  1. *"Only" noiseless.* No noisy-register run exists. A register with write noise has bounded information per read for any n. Whether its optimum over n is then finite, an integer, or runs to the continuum is untested (OPEN).
  2. *"Inside the theory's proved class, a continuous noisy memory beats every finite register here"* (W1). This rests on the author's own HYP mapping of CORE.md:91 to σ_w√x. It compares two heat accountings, the learning-rate floor for a linear memory and H(R′|R) per renewal read, that were not shown to be commensurable. It also covers only periodic renewal reads. Event-triggered reads were not tested. It must carry the HYP label and drop "every".
  3. *"What survives a change of class is the information budget, ≈ 1.1 nats per read"* (W1 and the §2 INFO-BUDGET proposal). §5 suggests the opposite. Under ideal coding (KGE) the per-look information runs to 0 and the look rate to its maximum. In this register, H\* = 1.107 comes from the register's own h(ρ) (§3.2). What the evidence supports as class-robust is the **cost scaling σ_w√x**, which is Berger's and KNOWN, not the per-read budget (HYP).
- **Better wording:** "In the noiseless discrete-register class the design is an integer n\* by construction, and the class fixes H\* ≈ 1.1 nats per read. Across classes, only the σ_w√x cost scaling is supported, and it is KNOWN (Berger 1970). Whether any discrete design is optimal among all memories is OPEN."

## 7. Other errors found

- **(low)** §1.9: "a = 1: n\* changes by 1 in 73 cells" is false as worded. From `wt_run.jsonl`, n\* changes in **72** cells. Only 34 change by 1, the largest change is 41 (σ_w = 0.3, x = 1e6: 1814 → 1773), and the largest relative change is 5.9%. s\* changes in 2 cells. The calls and summary statistics are indeed unchanged.
- **(low)** §1.10 and §1.12: "J\* ≈ 1.244·σ_w√x … 24% above CORE". The leading-order constant is 1.2675, so about 27% above under the HYP mapping. 1.244 is a grid median biased by small s.
- **(low)** §1.12 row 1: "select a unique interior (n\*, s\*) in all 432 × 3 cells". s\* is at the lower bound s = 1 in 150 primary cells, so "interior" holds for n\* only.
- **(medium)** §0.10 rows 1 and 3: the α\* values, the λ-dependence and α\*·λ → 12 hold for the truncated menu only (§3.1). §0.11 R3 called the rise of α\* with N a "HYP". It is now OBSERVED, and large.
- **(low)** The Step 0 message to Chad, "Below it polygons win, above it the disk does", needs "for polygons up to N(T) vertices; with larger menus the switch moves toward α = 1, and the margins are 1e−7 to 1e−4".

## 8. Labels after this review

| claim | label |
|---|---|
| Step 0: one switch α\* in all 60 cells, scored menu | OBSERVED (reproduced) |
| Step 0: one switch with menus up to 3N(T), N = 720, N = 1440 | OBSERVED (59/60; 8/8 subset) |
| Step 0: α\*(T, λ) values, α\* ↓ in λ, α\*λ → 12 | OBSERVED **for the truncated menu only**; menu-set |
| Step 0: α\* → 1 over all regular polygons | HYP (trend observed to N = 1440) |
| Step 1 HIT (H-a to H-d) | OBSERVED (reproduced, independent code) |
| R-regime constants and exponents, equal split, J ∝ σ_w√x | PIM to leading order (scaling identity, §3.2), ELEMENTARY; numerically confirmed |
| Berger D(R) = 2σ²/(π²R), J_B = 2σ_w√x/π | KNOWN (read in KGE, citing Berger) |
| "Beyond GP" (Bar A) | met literally; not informative (GP has no time) |
| Bar B "trivial in substance" | stands; reason is the scaling identity, not KGE |
| Integer n\* only for noiseless registers; continuous memory beats every register; information budget class-robust | HYP / OPEN (overstated as written) |

## 9. Exact fixes needed (append-only; WORLD_TRACK.md is not edited by this review)

Append a dated "Review fixes (REVIEW_WORLDTRACK)" section to WORLD_TRACK.md, hash it in the WORKLOG, and change no locked text. It should contain:

1. **Step 0, menu.** State that α\* is set by the menu cap: give the §3.1 table, and say the polygon at α\* lies within 10% of N(T) in 22 of 60 cells. Relabel the α\*-value, λ-trend and α\*λ → 12 claims "OBSERVED for n ≤ N(T) only". Record "α\* → 1 over all regular polygons" as HYP, and the single-switch shape as robust to N = 1440 (OBSERVED, subset). Upgrade R3 from HYP to OBSERVED.
2. **Step 0, the message to Chad.** Correct "below it polygons win, above it the disk does" with the menu qualifier and the size of the margins.
3. **Step 1, the corner rule.** Disclose that the hashed §1.5 relaxed Route 1's "no corner solutions" by treating s\* = 1 as a regime, and that the tick binds in 35% of cells. Drop "interior" for s\* in §1.12.
4. **Step 1, the scaling identity.** Add §3.2's identity. Relabel S1, S2, the R-half of H-c, the equal split and J ∝ σ_w√x as one ELEMENTARY result (PIM to leading order), and quote J\*/(σ_w√x) → 1.2675 (≈ 27% above the HYP CORE mapping), not 1.244 / 24%.
5. **Novelty.** Replace "the read-floor version of KGE's finding … KNOWN in substance" with: KGE show finite bits per sample is always suboptimal under block coding, so the interior ≈ 1.1 nats per read is a property of the chosen register class, and Bar B is trivial because of the scaling identity. Move the Berger formula from HYP to KNOWN, citing KGE's equation. Add "beyond GP is uninformative because GP has no time" next to the Bar A call.
6. **Class claim (W1).** Reword it to the §6 wording. Label "continuous noisy memory beats every finite register" as HYP and drop "every". Label "the information budget survives a change of class" as HYP, contradicted under ideal coding (KGE). Change INFO-BUDGET's HIT criterion so it doesn't assume the per-read budget carries over: test the look rate and per-look information as outcomes, and include the possibility that the look rate runs to the fastest sensor rate.
7. **a = 1 arm.** Correct "n\* changes by 1 in 73 cells" to "72 cells; 34 by 1; at most 41 (5.9%)".
8. **Process.** Log WORKLOG hash times to the second (for example `date -Iseconds`) so a hash can be ordered against same-minute script times. Note that Step 0's order within 18:31 can't be verified after the fact.
9. **Prior art.** Name Åström & Bernhardsson 2002, Rabi et al. 2012, Sun et al. 2020, Neuhoff & Gilbert 1982 and Tatikonda et al. 2004 as related (DOIs in §5), with "content not yet read", before any novelty claim about the constants.

## 10. Files (this folder)

- Step 0: `rv_tl.py`; `rv_tl2.py` → `rv_tl2_1.json` / `.out` (scored menu), `rv_tl2_3.json` / `.out` (3× menu); `rv_tl_bigmenu.py` → `rv_tl_bigmenu.json` / `.out`; `rv_tl_probe.py` → `rv_tl_probe.out`; `rv_tl_zoom.py`.
  - `rv_tl_menu.*` and `rv_tl_3.*` are superseded first runs that used the disk with no refinement. They are kept for transparency.
- Step 1: `rv_wt.py` → `rv_wt.jsonl`; `rv_wt_score.py` → `rv_wt_score.out`.
- Citations: `rv_crossref.py` → `rv_crossref_dois.txt`, `rv_crossref_q2.txt`; `kge_excerpt.txt`.

## 11. Addendum: later appends to the target (seen 19:21 ET; outside this review's scope)

- While this review ran, another agent appended Step 2 (INFO-BUDGET) and a Step 3 (STORED-PEAK) pre-statement to WORLD_TRACK.md. The WORKLOG hashes them at 19:05, 19:08 and 19:09 (`ed403d82…`, `267f6433…`, `084ea69e…`). I checked that each matches a byte-prefix (ending at lines 436 and 541, and the whole file), and that the reviewed prefix `568eff32…` is intact. These steps were **not** reviewed here.
- Step 2 has already done part of fix 5: it reads the Berger formula from KGE eq. (4) and moves it to KNOWN. Its MISS supports §6 point 3. With no per-look price, the look rate sits at the sensor limit, and the nats per look follow s_min·σ_w√x. So the per-read budget is not class-robust, as §6 argued. Fix 6's INFO-BUDGET wording therefore applies only to whatever text still states the budget as class-robust, mainly W1 in §1.13 and the summary sent to Chad. Fixes 1–4 and 7–9 are untouched by Steps 2 and 3.

## Outcome: **PASS-WITH-FIXES**

Both HITs are honest. They were hashed before computing (with the Step 0 timing caveat), scored literally, and reproduced independently. The fixes are to their interpretation:
- Step 0's α\* values come from the menu cap.
- Step 1's content is one elementary scaling identity, with drift dependence that is KNOWN in kind.
- The KGE attribution and the class claim are overstated.

All fixes are append-only and listed in §9.
