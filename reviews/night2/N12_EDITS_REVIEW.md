# Independent review of PR #18 (THEORY v1.4.2 / CLAIM_MAP v2.5: N12 scoping)

15 Nov 2026, about 10:15 AM ET (America/New_York). Independent reviewer executor (for Ace; Chad t1916: "be extra, extra sure before you do a full rewrite of the theory ... causal first principles"). Private repo; nothing posted or sent. The author's account was not trusted; every check below was done against `origin/main` (c0e648f), `reviews/night2/N12_REFEREE.md` and `reviews/night2/V14_REVIEW.md` §3–§4, with my own code.

## Verdict: CLEAN after trivial fixes. Merge.

The edits do exactly what the referee's §5 narrowed text and V14_REVIEW Fix 1 call for, and nothing else. One author commit (2118dc8) on merge base `c0e648f`. While this review ran, main moved (PR #19 queue pick 4, ledger 26–28; PR #20 README/STATUS restamp to v1.4.1, ledger 29), so the branch was rebased onto `a8bb006`. Only STATUS.md conflicted (one paragraph): resolved by keeping main's v1.4.1 paragraph (Regime C, J16 sentences) and replacing only its N12 sentence with this PR's narrowed sentence. The ledger conflict was resolved by keeping main's entries 0–29 byte-identical and appending this review as entry 30. Files: THEORY.md, measurement/CLAIM_MAP_v2.md, STATUS.md.

## 1. Line-by-line diff vs origin/main

| Location | Change | Source | OK? |
|---|---|---|---|
| THEORY header | v1.4.1 → v1.4.2; date line | changelog | yes |
| Status block, "Proved inside the model" | "exponents ... only their constants do" → pooling-onset exponent α-free under premises; vigilance growth, mixed-technology exponent, constants depend on α | C4; V14 Fix 1 | yes |
| "What changed" item 5 | same narrowing | C4; V14 Fix 1 | yes |
| §2.5 N12 bullet | rewritten to referee §5 text: −1 (exact reset reads, rescaling-closed predictors, information-rate pricing), −(1+θ) every α > 1; homogeneity reason; premises (i) same α (C2), (ii) exact reads at the level (C1), (iii) 𝒜₁, no broadcast cost (Theorem 2), h = 0 or a ≥ b, small ρ; finite-ρ fits −0.93/−1.86; vigilance units (C3); α-dependent exponents and constants (C4); "1 < α < 3" → "α > 1"; "in-model only; untested in the field" | C1–C4, referee §1 | yes |
| §8b candidates note | onset exponents technology-set under §2.5 premises; vigilance-growth and mixed-technology exponents depend on α | C4 | yes |
| §9 sink condition | adds same-technology incl. read noise, same α for shared/private drift | C1, C2, referee §6 | yes |
| §13 changelog | v1.4.2 entry | — | yes |
| CLAIM_MAP v2.5 note + N12 row | PROVED (in-model) → MATH-CORRECTED with narrowed text and premises | referee §5 | yes; the status table counts only the 167 v2 rows, so no tally change is due |
| STATUS paragraph | N12 sentence narrowed | C1, C2, C4 | yes |

Every number checked against the referee: Π\* 3.38/4/4.61; onset vigilance value 2.25/2/1.84; e_u = θ + 1 − 1/α; fits −0.93/−1.86; a, b formulas. No locked prediction, result or proof file touched.

## 2. "Only through constants" leftovers

Repo-wide grep (`only through constants`, `only their constants`, `exponents do not depend on the spectrum`, `formal exponents do not`, `spectrum drops out`, `1 < α < 3` in N12 context). No live statement remains in THEORY.md, STATUS.md, README.md, QUEUE.md or CLAIM_MAP_v2.md. Remaining hits are quotations inside frozen review/history files (`V14_REVIEW.md` rows 3/10/34 and Fix 1, `V141_REVIEW.md`, `V141_CHANGES.md`, `N12_REFEREE.md` §1 quoting the claim, THEORY §13 v1.4 changelog entry describing what v1.4 said). Those are history and correctly left alone. "1 < α < 3" elsewhere in THEORY §2.2 refers to the fBm read-rate and Afterman rows, not N12, and is correct there.

## 3. Scope vs evidence: trivial fixes applied (commit on this branch)

1. **C2 Δ > 1 formula stated as fact.** The referee (§7) says it is an asymptotic argument confirmed numerically within 3%, not proved. Added "by an asymptotic argument that matches numerics to within about 3% but is not proved" (THEORY §2.5) and "asymptotic, numerically within ~3%, not proved" (CLAIM_MAP N12).
2. **C1 noisy-reads knife-edge stated without its evidence level.** Added "(shown numerically, not proved; the crossover's closed form is not derived)" (THEORY §2.5) and "numerical, not proved" (CLAIM_MAP). The knife-edge itself was already stated, correctly.
3. **Price premise dropped.** Referee §5 lists "equal or fixed price ratio"; added to premise (iii).
4. THEORY header pointed to CLAIM_MAP v2.4; now v2.5.
5. "PR open for review" / "PR left open for independent review" in the changelog and v2.5 note would go stale on merge; now point to this review.
6. STATUS: "; An elementary" → "; an elementary".

7. After the rebase, version pointers moved to the merged state: STATUS stamp and canonical-files list (v1.4.1 → v1.4.2; CLAIM_MAP v2.4 → v2.5) and README's four version pointers (lines 11, 37, 54, 90). README's dated "Update, 15 Nov 2026 (v1.4.1)" heading and content were left as is (README carries no N12 wording).

Not changed (outside this PR's scope; noted): CLAIM_MAP A5 ("effort elasticities = (a, b)") is affected by C3 (holds only at θ = 1); that is queued as EFFORT-UNITS-ERRATUM and was not part of Fix 1. V14 Fix 1 also suggested naming the ordering threshold κ\* = 1/|e_g| as α-free; optional, not added.

## 4. Independent numerical spot-check (`N12_EDITS_REVIEW_checks/`)

My own code, from the cost model rather than the (a, b) closed form: N members; flat = each tracks shared + private drift alone; pooled = one level tracks the shared drift with stakes N·w, members track private drift; onset N\* by root-finding of the cost equality; local slope d ln N\*/d ln ρ.

- **Priced precision** (MMSE ∝ q^{1/α} r^{1−1/α}, price ∝ r^{−θ}), α = 1.2, 1.5, 2, 2.5, 3.5: −1.4999 (θ = ½), −1.9999 (θ = 1), −2.9985 (θ = 2, at ρ = 10⁻³), identical across α. **Confirms −(1+θ), every α > 1 tested (incl. 3.5).**
- **Exact reset reads** (hold-last-value, fBm increment variance ∝ q τ^{α−1}), α = 1.2–2.9: −0.9999; at ρ = 0.1: −0.953/−0.953/−0.954. **Confirms −1 and the finite-ρ figure.**
- **Noisy reads**, optimal Gaussian-conditioning estimator on 120 past periodic reads, α = 1.5, 2, 2.5:
  - σ² = 10⁻³: slopes at ρ = 10⁻¹…10⁻⁴: (−0.97, −1.16, −1.76, −2.03), (−0.98, −1.24, −1.91, −2.00), (−1.00, −1.39, −1.97, −2.08). Shift toward −2 with an α-dependent crossover (mid-window −1.16/−1.24/−1.39). **Confirms C1.** (The ρ = 10⁻⁵ column in `check.out` drifts back up; that is a truncation artifact of using only 120 past reads when the level needs to average over more, shown by the exact check below.)
  - **Second noise level** σ² = 10⁻⁶ (the referee used one): slopes −0.95, −1.00, −1.16/−1.25/−1.39 (at ρ = 10⁻⁵), −2.03/−2.00/−2.08 (ρ = 10⁻⁷): the same pattern with the crossover moved to smaller ρ, as σ² ≪ q_g T\*^{α−1} predicts.
  - **Exact α = 2 steady-state Kalman** (`kalman2.py`, no truncation): σ² = 10⁻³: −0.98, −1.24, −1.91, −2.00, −2.00, −2.00 (ρ = 10⁻¹…10⁻⁷); σ² = 10⁻⁶: −0.95, −1.00, −1.00, −1.03, −1.25, −2.00; σ² = 0: −1.00 throughout.

So the knife-edge is real at two noise levels, but its crossover is still only numerical; the wording above keeps it that way.

## 5. Citations (Crossref, this session)

- Veldkamp & Wolfers, "Aggregate shocks or aggregate information? Costly information and business cycle comovement", J. Monetary Economics 54, 37–55 (2007), DOI 10.1016/j.jmoneco.2007.06.001. Real; matches (Crossref does not list the S1 supplement number; NBER w12557 and SSRN 937378 are the working-paper versions).
- Wilson, "Informational Economies of Scale", Bell J. Econ. 6(1), first page 184 (1975), DOI 10.2307/3003221. Real; matches.
Neither citation is newly introduced by PR #18 (they are in the merged referee); the PR adds no citation.

## 6. Labels

No "law"; no field claim (the N12 text says "in-model only; untested in the field"; the §9 condition says "in-model result, refereed"). Field results stay "passed / failed on proxy X"; "Vigilance is **OPEN**" unchanged in THEORY's status block.

## 7. Process

The PR author did not log a ledger entry for the edit itself; ledger entry 30 (maintenance, unscored, out of cycle) records both the edit and this review.
