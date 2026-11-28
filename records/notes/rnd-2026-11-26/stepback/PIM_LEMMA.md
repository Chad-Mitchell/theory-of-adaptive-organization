# Lemma D1: a greedy operator-weight record ends at the signal front (PROVED (in-model); an application of KNOWN mathematics; not a test)

*26 Nov 2026, after GATE_READ_STEPBACK.md (amendment D1). Private R&D note; nothing committed. This replaces Draft D (route C11) as a test. Value on the step-back scale: V ≤ 2 (a consequence of known bounds).*

## Setting (all inputs, CHOSEN)
- Infinite chain, single-particle nearest-neighbour hopping h_{ij} = −(δ_{i,j+1} + δ_{i+1,j}), propagator U(k) = e^{−ihk}. Then |U_{tj}(k)| = |J_{j−t}(2k)| (standard; Bessel generating function).
- Stake region T, a set of |T| consecutive sites; lead time k > 0; price κ ∈ (0, 1).
- **Operator weight** of a site j ∉ T: w_j(k) = Σ_{t∈T} |U_{tj}(k)|². This is the weight of the present mode c_j in T's future modes c_t(k) = Σ_j U_{tj}(k) c_j. It depends only on h, not on the state (gate read §1.1); it is **not** a predictive-information functional.
- **Record:** add sites in order of w_j while w_j ≥ κ. Because the weights do not interact, the record is exactly the super-level set {j ∉ T : w_j(k) ≥ κ}. **R*** := the largest distance d(j, T) = min_{t∈T}|j − t| over sites in the record (0 if empty).

## Statement
Let g(n) := n·(arccosh(n/2k) − √(1 − (2k/n)²)) for n ≥ 2k. Then g is increasing on [2k, ∞), and
**R*(k, κ) < d\*(k, κ) := min{ n ≥ 2k integer : 2·g(n) > ln(|T|/κ) }.**
As k → ∞ with κ fixed, d\* = 2k + (2k)^{1/3}·2^{−1/3}·(¾·ln(|T|/κ))^{2/3}·(1 + o(1)): the record ends within O(k^{1/3}·(ln(|T|/κ))^{2/3}) of the front 2k, and its κ dependence is only through ln(1/κ).

**General form (PIM given a KNOWN bound).** For any finite-range Hamiltonian with Lieb–Robinson constants (C, μ, v) (Lieb & Robinson 1972, Commun. Math. Phys. 28:251, 10.1007/BF01645779, Crossref-checked this session), with w_j defined as the squared commutator norm ‖[A_T(k), B_j]‖² for unit-norm A_T on T and B_j on j, the same rule gives R* ≤ v·k + (2μ)⁻¹·ln(C²|T|²/κ) up to the bound's own form. Proof: the Lieb–Robinson bound ‖[A_T(k), B_j]‖ ≤ C|T|·e^{−μ(d(j,T) − v k)}, squared, is < κ beyond that distance.

## Proof (nearest-neighbour case)
1. Kapteyn's inequality (DLMF 10.14.8, https://dlmf.nist.gov/10.14.E8, read this session; no DOI claimed): for integers n ≥ 0 and 0 < z ≤ 1, |J_n(nz)| ≤ z^n·e^{n√(1−z²)} / (1 + √(1−z²))^n. Put z = 2k/n = sech α (n ≥ 2k). Then z·e^{√(1−z²)}/(1 + √(1−z²)) = e^{tanh α}/(cosh α + sinh α) = e^{tanh α − α}, so |J_n(2k)| ≤ e^{−g(n)} with g(n) = n(α − tanh α), α = arccosh(n/2k). This is the g above.
2. g is increasing for n ≥ 2k: g(n) = n·φ(α) with φ(α) = α − tanh α ≥ 0 increasing in α, and α increasing in n.
3. For j ∉ T at distance d ≥ 2k from T, every t ∈ T has |j − t| ≥ d, so by 1–2 each term |J_{j−t}(2k)|² ≤ e^{−2g(d)}. Hence w_j ≤ |T|·e^{−2g(d)}.
4. If 2g(d) > ln(|T|/κ), then w_j < κ and j is not in the record; by step 2 the same holds for every larger distance. So every record site has d < d\*.
5. Asymptotics: for n = 2k + ε with ε ≪ k, α ≈ (ε/k)^{1/2} and φ(α) ≈ α³/3, so 2g ≈ 2·2k·(ε/k)^{3/2}/3; solving 2g = ln(|T|/κ) gives ε ≈ (2k)^{1/3}·2^{−1/3}·(¾ ln(|T|/κ))^{2/3}. ∎

## Numerical sanity check (not a test; `lemma_check2.py`, `lemma_check2.out`)
|T| = 5, mpmath at 40 digits: for k ∈ {2, 4, 8, 16, 32} and κ ∈ {1e−2, 1e−4, 1e−6}, R* < d\* in all 15 cases (e.g. k = 32: R* = 65, 70, 75 against d\* = 73, 77, 81). Kapteyn's inequality held at every sampled (n, 2k) with n ≥ 2k (0 violations). The cruder factorial bound (DLMF 10.14.4) gives only R* ≤ max(e²k, ½ ln(|T|/κ)) (`lemma_check.out`).

## What this does and does not show
- **Does:** under a local Hamiltonian, any threshold rule on operator weight ends the record at the dynamics' signal front plus an O(k^{1/3}(ln 1/κ)^{2/3}) edge, with only logarithmic price dependence.
- **Does not:** derive the front, its speed v, or locality (all from h, CHOSEN); remove the cut (it moves from a chosen κ to a chosen lead time k and stake region T, gate D5); say anything about predictive *information* (w ignores the state and what the tracker already holds, gate §1.1); contrast static with predictive value (gate §1.4). The gate read's Airy table (its §1.3) was seen before this note was written.

## Amendments after gate read 2 (GATE_READ_STEPBACK2.md §2; appended; earlier text stands, this section governs)
- **2a (title).** Read the title as: "Lemma D1: a greedy operator-weight record **never extends past** the signal front (upper bound)".
- **2b (Does).** Read "Does" as: R* < d* = 2k + O(k^{1/3}(ln(|T|/κ))^{2/3}); the record never extends past the front plus an Airy edge. It is not shown to reach the front.
- **2c (regime).** The largest weight near the front is max_n |J_n(2k)|² ≈ 0.29·k^{−2/3} per stake site (gate read 2, mpmath: 0.074 at k = 8, 0.029 at 32, 0.011 at 128), so w_j ≲ 0.29·|T|·k^{−2/3}. For fixed κ the record is **empty once κ ≳ c·k^{−2/3}** with c ≈ 0.29|T|; it can reach the front only for κ ≲ c·k^{−2/3}. A lower bound on R* is not proved.
- **2d.** The proof uses |J_{−n}(x)| = |J_n(x)| (j − t can be negative). Step 5 is a leading-order expansion; its error terms are not bounded, so the asymptotic for d* is a statement about the bound, not a proved two-sided estimate. The general form needs a named Lieb–Robinson version for free fermions (not yet cited); until then read it as "for any bound of the form ‖[A_T(k), B_j]‖ ≤ C|T|e^{−μ(d − vk)}".
- Status: PIM (an application of KNOWN mathematics), V ≤ 2.
