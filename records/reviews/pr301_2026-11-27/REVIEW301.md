# Independent hostile review of PR #301 (head 43c4c81acb0417512dfa30aba0c5b2c7c17818d5)

*Copied unchanged from the reviewer's box folder `/workspace/units-memrule/` on 27 Nov 2026, except that the companion file `VERDICT.md` is renamed `UNITS_REVIEW.md` (wording rule) and the references to it follow.*

Scope: formal/lean/GTAO/MemoryRule.lean read in full (411 lines), plus the PR's README section,
CLAIM_MAP rows MEM-RULE and CT17, miss M45, AUDIT.json. Sources checked: GROK_BOT_MEMORY §4–§5,
LAYER_LIFETIME §2, THEORY.md:87 (CT12), :384 (CT17), MATH_ATTACK §3.4. Units findings: UNITS_REVIEW.md.

## Build (in /tmp/gtao-lean2, nice 19; packages copied read-only from /tmp/gtao-lean, author's tree untouched)

- `lake build GTAO.MemoryRule`: success, no warnings for MemoryRule. Full `lake build`: success (18437 jobs).
- `#print axioms` on all 22 theorems/lemmas in MemoryRule: every one depends only on
  [propext, Classical.choice, Quot.sound]. No sorry/admit/axiom/native_decide/opaque in the file.
- scripts/AxiomAudit.lean: "OK (2333 GTAO declarations; only propext, Classical.choice, Quot.sound)";
  matches AUDIT.json audit_count 2333.

## Statement vs claim

| Declaration | Check | Label in PR | Agree? |
|---|---|---|---|
| held_min | unique minimizer √(6k/(aσ²)), min c + 2√(kaσ²/6), for k,a,σ² > 0 | Faithful | yes |
| hold_strictly_better_iff / drop_optimal_iff / joint_min | strict and weak hold rule, joint min = min(holdMin, L) | Faithful | yes; the remark that "hold iff" needs the strict sign is right |
| doc_hold_rule | specialization a = w, L = wp | Faithful | faithful to the text as printed; that text is dimensionally inconsistent (UNITS_REVIEW §1–2) |
| doc_example | §4:57 arithmetic, a = w | Faithful | faithful to the arithmetic; under §4's own definitions (a = wp/g²) the example's conclusion reverses (hold) |
| band_rule, band_sq | algebra of b* = (6kσ²/a)^{1/4} | WEAKER | yes, honest |
| occupation_integrals, barrier_cost_from_occupation | integrals of b − abs(x); density (b − abs(x))/σ² is the correct Green's function of BM from 0 absorbed at ±b (mass b²/σ², second moment b⁴/(6σ²)) | WEAKER | yes, honest; density and barrier optimality are inputs, stated |
| barrier_cheaper_than_fixed | 2√(kaσ²/6) < √(2kaσ²) | Faithful | yes |
| part_rate_ratio | rate with weight Λᵢu is √(Λᵢ/Λ) × rate with Λu | Faithful | yes; holds for any a, so it survives the units correction |
| watch_sq_prop | takes f² = κΛ as hypothesis | WEAKER | yes, honest (pure algebra given the proportionality) |
| ct12Cost/ct12Tstar/ct12_min/bern | c/T + wqT^{α−1}/α (matches THEORY.md:87), unique minimizer (αc/((α−1)wq))^{1/α} | Faithful (minimizer only) | yes |
| ct17_part_rate, ct17_alpha_two | (Λᵢ/Λ)^{1/α}, √ at α = 2 | Faithful (ii) only | yes; (i) correctly listed as not formalized |

Vacuous hypotheses: none found. All positivity hypotheses (k, a, σ², Λ, Λᵢ, c, q > 0; α > 1) are
satisfiable and used or harmless; no contradictory pair; c, L, p are unconstrained where the
statement holds for any value. doc_example is closed (no hypotheses).

## BLOCKERS

B1 (text, not Lean). M45 (NOTES/MISSES-LEDGER.md), the README MEMORY-RULE paragraph and the
CLAIM_MAP MEM-RULE row understate the units miss:
- They say the consistent reading "may be" a = pw/g² and "which reading the application means is
  open". Under §4's printed definitions (w = stake when needed, p = need rate) no consistent reading
  has a = w (UNITS_REVIEW §2); the drift weight is forced to w p/g² unless §4 redefines w.
- M45 says "no theorem changed" and "the form of both rules ... unchanged". True of the Lean
  theorems in general a, but the application's numbers change: the §4:57 worked example reverses
  (1.82 < 2: hold, not drop), T* and b* gain the need rate, and the public reply's root and band
  lines are dimensionally wrong as stated. The row should say so.
- doc_example and doc_hold_rule are labelled Faithful with no note; add "faithful to the printed
  text in the a = w reading, which M45 records as dimensionally inconsistent".
Minimal fix: reword those three places; optionally add a `consistent_example` theorem
(a = wp/g² = 2, L = 2: holding strictly beats dropping, holdMin = 1 + 2√(1/6)) via
hold_strictly_better_iff — a few lines.

No Lean blockers: every statement matches its labelled claim, labels are honest, build and axioms clean.

## NON-BLOCKERS

N1. MEM-RULE row status column says "not independently reviewed"; update after this review.
N2. README: say explicitly that `held_min` etc. take T as the barrier's *mean* interval
    (§5:69), not a fixed clock; the cost form k/T + aσ²T/6 is only valid in that parametrization.
N3. part_rate_ratio assumes the part and whole share k and σ²; say it in the label (the √ share
    also applies only to items the part still holds — its own hold threshold is stricter).
N4. Range of validity (b* ≤ g once the need rate is in, i.e. wp ≥ 6kσ²/g²) is not in the README;
    worth one line beside the Brownian/OU caveat.
N5. The same inconsistent formula appears in applications/MEMORY_MISS_COST_BOUNDS_2026-11-24.md:52–54,
    NOTES/rnd-2026-11-26-late/stepback/TRACKABLE_WORLD.md:46, NOTES/rnd-2026-11-26-late/context/MEMORY_CHALLENGE.md:38;
    M45's "where" should list them (fix belongs to the doc PR, not this one).
N6. AUDIT.json "how" names /tmp/gtao-lean; reproduced here in /tmp/gtao-lean2 with the same count.

Not edited, not merged.
