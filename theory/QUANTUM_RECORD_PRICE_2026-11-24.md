# Quantum record price: the minimum does not name it

*24 November 2026 (UTC). Desk note. No script. Self-check, not an independent review. `THEORY.md` is unchanged. Open-work row T74. Status words are those at `CORE.md:169`. Nothing here derives general relativity, quantum mechanics, or holography.*

## Answer

**Blocked by A6's naming step.** The minimum of a cost under A1–A8, subject to the ruin cap, does not pick a unique quantum-record price. R1 prices a coordinate A6 has already named, and A6 names classical mutual information only (`CORE.md:52`). A published uniqueness theorem for von Neumann entropy, or for Umegaki relative entropy, fixes that entropy under its own axioms. It does not fix which contraction is the record price. The price is not filed as KNOWN. The entropies are.

## Where a quantum price is already assumed

On this main (`0f37918`):

- `CORE.md:52` and `theory/REPRESENTATION.md:58` name the memory coordinate as Shannon mutual information, or the Gelfand–Yaglom–Dobrushin supremum when that mutual information is finite. Both are classical. `theory/REPRESENTATION.md:60` says the Aczél–Forte–Ng uniqueness is not extended to differential entropy.
- `theory/DIRECTIONS_2026-11-22.md:58` parks a conjecture that the frontier carries over with a Holevo bound, quantum channel capacities, and a quantum Landauer cost, with a different price on copying. That sentence assumes those floors. It does not derive which functional the record pays. The file says its references are to be checked before any canonical use, so they are not cited here.
- `theory/RECORD_REPAIR_FLOOR_2026-11-23.md:114` and `:174`, and `theory/PHYSICS_CHAIN_2026-11-23.md:18`, leave the repair heat of a quantum record in three dimensions open. They do not choose among mutual information, a pinch divergence, and dimension.

Off this main, the two drafts that hinge on the choice:

- Draft PR #252, head `bd63638`, `theory/pointer-basis-stakes-2026-11-24/PREREG.md:24`. A6 does not fix a quantum price. The note then chooses the mean Umegaki divergence of the pinch, \(P_D=\mathbb{E}[D(\rho\|\Phi_\theta(\rho))]\) (`PREREG.md:28`). Beside it, \(P_\chi=I(W;M_\theta)\) is the Shannon mutual information of the classical outcome (`PREREG.md:34`). The Holevo quantity of the ensemble before the measurement does not depend on \(\theta\) and is not used. Ruin is slack (`PREREG.md:36`). The memo's reading (`MEMO.md:9`, `MEMO.md:62`) is that \(P_\chi\) is the coordinate A6 already names once the outcome is classical, and \(P_D\) is the entropy produced by writing.
- Draft PR #253, head `fd69ec3`, `theory/COMPOSITE_CONTEST_2026-11-24.md:46` and `:56`. The headline price is \(\lambda\ln K_{AB}\). On a protocol whose settings are drawn after the record, the A6 coordinate is 0 for every contestant (`:96`, `:154`). The draft records that mutual information and the dimension price rank one control in opposite directions (`:154`). It does not choose which charge is paid.

## The block

**PROVED (in-model).** Let the axioms be A1–A8 as stated in `theory/REPRESENTATION.md:39-64`, and let the ruin cap be the feasible-set restriction in A2.

1. **The minimum takes the coordinate as given.** Under A1–A7, on at least three essential intervals, a continuous cost is \(C=a\sum_i p_i z_i+b\) with one \(a>0\) (`theory/REPRESENTATION.md:84-92`). Step 4 of that proof puts Shannon mutual information, in A6's scope, into the memory slot (`:114`). `CORE.md:52` says R1 does not choose the coordinate list. On a menu that does not depend on the numerical cost, \(C\mapsto aC+b\) preserves the argmin (`theory/REPRESENTATION.md:126`). The argmin returns a design. Returning a design leaves the functional unnamed. Theorem S3 (`CORE.md:48`) runs the other way: an undominated design is a minimizer at some nonzero nonnegative prices. Many prices share one minimizer.

2. **A6 is the step that stops.** A6 names finite-law Shannon information, and the Gelfand–Yaglom–Dobrushin supremum for classical random variables on standard Borel spaces with finite mutual information (`theory/REPRESENTATION.md:58-60`). A state on a Hilbert space is not that pair. Until a measurement has produced a classical outcome, A6 assigns no real value, and the linearity step does not fire. The classical uniqueness R1 uses is this naming step plus linearity. It is not a property of the argmin. A1–A8 contain no quantum substitute for the naming step.

3. **A5, A8, and the ruin cap do not supply the missing name.** A5 makes a concatenating coordinate linear once that coordinate is the one in the sum. It does not choose which additive functional is placed there. Holevo information of a product ensemble, Umegaki relative entropy of a product pair, and von Neumann entropy of a product state are all additive. A8 signs a coefficient that is already in the sum (`theory/REPRESENTATION.md:64`). The ruin cap is not produced by the representation (`theory/REPRESENTATION.md:96`). A constraint on the feasible set does not choose the objective. Draft #252 leaves the cap slack (`PREREG.md:36`), so that draft's split is not a cap effect.

4. **The candidates are not one coordinate up to \(a>0\).** Two classical designs on one fixed alphabet, both diagonal in one basis. Copy: \(M\) is a non-degenerate perfect copy of \(W\), so \(I(W;M)>0\). Noise: \(M\) is independent of \(W\), so \(I(W;M)=0\).

   - Pinch in that basis: \(\Phi(\rho)=\rho\), so \(D(\rho\|\Phi(\rho))=0\) on both designs. A map \(z\mapsto az+b\) with \(a>0\) cannot send a positive number and zero to one and the same value. The pinch price is not R1's image of \(I(W;M)\).
   - Dimension of one system does not change between the two designs. \(\lambda\ln K\) is constant on that menu. The same arithmetic shows it is not R1's image of \(I(W;M)\). A constant coordinate is not essential (`theory/REPRESENTATION.md:80`, Lemma M).
   - Once the outcome is classical and the states commute, the Holevo quantity of that outcome equals \(I(W;M)\). **ELEMENTARY**, from \(S(\rho)=-\mathrm{Tr}\,\rho\ln\rho\) on a diagonal state. That is A6's coordinate. The Holevo quantity of the ensemble before the measurement is a different functional. Draft #252 does not use it (`PREREG.md:34`).

   A positive scale preserves order. On the complete-dephasing slice of draft #252, \(P_D\) is minimized at the dephasing axis and \(P_\chi\) is minimized at the complementary axis when the stake is zero (their closed form, `PREREG.md:72` on that branch). The two argmins are different designs, so the two prices are not one R1 cost. On that ensemble their sum does not depend on the angle (`MEMO.md:60-62` there). That relation is a sign flip, and \(a>0\) does not include a sign flip.

## What the known uniqueness theorems fix

Each DOI below was resolved on the Crossref API on 24 November 2026. The returned title, authors, and pages match the work. A DOI is printed only in that case.

**KNOWN. von Neumann entropy, as dispersion.** Ochs, "A new axiomatic characterization of the von Neumann entropy," *Reports on Mathematical Physics* 8:109–120 (1975), doi `10.1016/0034-4877(75)90022-1`. The publisher abstract states that the postulates determine \(S(W)=-k\,\mathrm{Tr}(W\ln W)\) up to a scaling factor, as a measure of intrinsic dispersion, and that the postulates have no direct bearing on phenomenological thermodynamics or information theory. The postulate list inside the article was not re-read. The abstract's sentence is why this theorem does not name a record price. Building Holevo information, or a pinch divergence, out of \(S\) is a further choice of contraction.

**KNOWN. Umegaki relative entropy of a pair.** Wilming, Gallego, and Eisert, "Axiomatic Characterization of the Quantum Relative Entropy and Free Energy," *Entropy* 19:241 (2017), doi `10.3390/e19060241`. Their Theorem 1: a function of pairs of states on a finite-dimensional space, second argument full rank, is a positive multiple of \(D(\rho\|\sigma)=\mathrm{Tr}\,\rho(\ln\rho-\ln\sigma)\) if it is continuous in the first argument at fixed second argument, obeys data processing, is additive on tensor products, and is superadditive. They state that no subset of the four properties is enough, and that Rényi divergences meet the first three. The pinch price sets the second argument equal to \(\Phi(\rho)\), a function of the first. A complete pinch of a pure pointer is not full rank, so the hypothesis of the theorem is not met. Holevo information of an ensemble is an average of divergences to the barycenter, \(\sum_x p_x D(\rho_x\|\bar\rho)\), a different contraction of the same \(D\). The free-energy reading in that paper is athermality relative to a Gibbs state, not a record of an arbitrary world variable. Their abstract attributes a prior form to Matsumoto. That manuscript had no Crossref DOI in this check, so it is not used as a source.

**KNOWN. In a general probabilistic theory the entropy is not one functional.** Barnum, Barrett, Clark, Leifer, Spekkens, Stepanik, Wilce, and Wilke, "Entropy and information causality in general probabilistic theories," *New Journal of Physics* 12:033024 (2010), doi `10.1088/1367-2630/12/3/033024`. Measurement entropy and mixing entropy coincide in classical and quantum theory, where they are Shannon entropy and von Neumann entropy. They differ in general. In their firefly example a pure state has mixing entropy 0 and measurement entropy 1, and a mixture has mixing entropy 1 and measurement entropy 0. Equality of the two is an extra constraint (their word: monoentropic). Short and Wehner, "Entropy in general physical theories," *New Journal of Physics* 12:033023 (2010), doi `10.1088/1367-2630/12/3/033023`, give one measure that reduces to Shannon entropy and to von Neumann entropy, and show that in a theory with non-local boxes no conditional entropy that is reasonable in their sense is subadditive. Neither paper selects a record price inside quantum theory.

Shannon's classical uniqueness, the one A6 uses, remains the Aczél–Forte–Ng theorem (doi `10.2307/1426210`, re-checked on Crossref this date; `theory/REPRESENTATION.md:58`). It is a theorem about finite-law entropy.

## Model implications

- **Model implication.** If a quantum coordinate is required to extend A6, then on classical diagonal records it matches \(I(W;M)\) up to the one scale \(a>0\). The pinch price and a pure dimension price fail that match. A quantum record can still carry a pinch term beside the mutual information. Whether that term is in the sum is the coordinate-list choice R1 does not make (`CORE.md:52`).
- **Model implication.** For a classical-quantum state \(\rho_{XB}=\sum_x p_x |x\rangle\langle x|\otimes\rho_x\), the quantum mutual information built from von Neumann entropy equals the Holevo quantity of the ensemble. **ELEMENTARY** given \(S\). That identity is not a consequence of A1–A8. It is what the memory coordinate would be under a new axiom that names quantum mutual information and requires agreement with A6 on classical records. Draft #252's \(P_\chi\) is the mutual information after the measurement (`PREREG.md:34`).
- **Model implication.** On draft #253's singlet menu the A6 coordinate is identically zero (`theory/COMPOSITE_CONTEST_2026-11-24.md:56` on that branch). The minimum on that menu cannot see the coordinate, and it cannot promote \(\lambda\ln K\) into the coordinate A6 names. Charging dimension adds an essential coordinate. R1 does not choose the list.

## Why there is no script

A computation can show that two named functionals differ. Drafts #252 and #253 already did that. It cannot show that A1–A8 name one of them. The two-point menu above is an identity, and it is the cheaper test. A grid would leave the naming-step block where it is. No preregistration and no run.

## Puzzle

The missing statement is a naming axiom for the quantum coordinate: which contraction of the entropy is the memory term, and whether the pinch, or dimension, is a second essential coordinate. A1–A8 and the ruin cap do not state it. The known uniqueness theorems name \(S\), or \(D(\rho\|\sigma)\), and stop there.
