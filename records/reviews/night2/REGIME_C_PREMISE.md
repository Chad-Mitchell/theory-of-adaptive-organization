# REGIME-C-GAUSSIAN-PREMISE — author note (pick 18, rule slot; ledger 87–90)

**Outcome: authored, awaiting independent review. DO NOT MERGE without separate reviewer PASS.** Author: executor queue-pick18
(for Ace, Chad t1914), 15 Nov 2026, about 4:40 PM ET. The item asks for scope text for THEORY §0 and §2.2 Regime C (a headline
sentence and a premise), so per Chad t1916 a separate reviewer, who did not write it, judges it and alone may merge it. This author
wrote neither `theory/INTERNAL_MODEL.md` nor `HEADLINE_PREMISE_SCOPE.md` (P9, the source of the item). THEORY v1.4.5 → v1.4.6.
No CLAIM_MAP status change (Regime C has no row); no locked prediction or result changed; vigilance stays OPEN.

## 1. Answer

Q^{1/β} is **not Gaussian-only, but it is not shape-free either.** For independent modes that share one shape up to scale, the
exponent of model bits is 1/β for any **sub-Gaussian** shape at every β, and for **any finite-variance** shape when **β > 1**. Only the
constant depends on the shape. Not derived: (i) modes that are uncorrelated but dependent (the usual non-Gaussian principal
components), (ii) β ≤ 1 with tails heavier than Gaussian, (iii) the drifting-world rate Q^{min(½,1/β)}. Because the interior
minimum of the model's budget share lives at β < 1, it is derived only for sub-Gaussian shapes. P9's "the Gaussian R(D) is an
upper bound" is true (read, §2) but does not by itself bound the bits at the optimum, so it does not settle the exponent either way.

## 2. Sources read (only these)

Polyanskiy & Wu, *Information Theory: From Coding to Learning* (Cambridge University Press), author PDF export of 16 Aug 2024,
`https://people.lids.mit.edu/yp/homepage/data/itbook-export.pdf`, fetched 15 Nov 2026 about 4:13 PM ET, sha256
c76c5cd867818ef66e9d63c2f899dccdff9a501456160df153d0fa981db83de3 (not committed). Read: Theorem 26.2 (Gaussian R(D) = ½ log⁺ σ²/D),
Theorem 26.3 (for any zero-mean, variance-σ² source under MSE: ½ log⁺ σ²/D − D(P‖N(0,σ²)) ≤ R(D) ≤ ½ log⁺ σ²/D; scalar statement),
Remark 26.3 (the lower, Shannon bound is asymptotically tight as D → 0 under conditions), Exercise V.21(b) (reverse water-filling
for a Gaussian vector). Nothing else was read. The zero-rate slope result (D3) is derived here from first principles; whether it is
already in the literature was not checked (new item REGIME-C-PRIORART-USTAR).

## 3. Derivation (causal first principles: the organisation pays κ per nat and w per unit squared error; bits go where they cut loss most)

**D1. Setup.** Modes X_i = √λ_i · Z_i, independent, λ_i = i^{−β}, Z one zero-mean unit-variance shape. Cost w·ΣD_i + κ·ΣR_i (MSE).
For independent components and additive distortion, I(X; X̂) ≥ Σ I(X_i; X̂_i) (chain rule; h(X_i | X^{i−1}) = h(X_i) and conditioning
reduces entropy), with equality for per-mode coding, so the problem separates by mode. Per mode R_i(D) = R_Z(D/λ_i).

**D2. Allocation.** With s = w/κ, mode i sits where |R_Z′(d_i)| = s·λ_i (d_i = D_i/λ_i), so its rate is G(sλ_i), G(u) = R_Z at slope u.
G rises with u.

**D3. Which modes get any bits.** Mode i gets zero bits iff sλ_i ≤ u*, where u* = |R_Z′(1⁻)| = **1/(2v*)** and v* is the smallest v with
E e^{tZ} ≤ e^{vt²/2} for all t (the optimal sub-Gaussian proxy; v* ≥ 1). Proof. (⇐) Donsker–Varadhan with f(z) = −s(z−y)² + sz² gives,
for any test channel, I + sE(Z−X̂)² ≥ s − E log c(X̂), c(y) = e^{−sy²}·E e^{2syZ}; if c ≤ 1 everywhere, zero rate (cost s) is optimal.
c(y) ≤ 1 for all y is E e^{tZ} ≤ e^{t²/(4s)} for all t, i.e. s ≤ 1/(2v*). (⇒) If c(y₀) > 1, the channel built from output law
(1−ε)δ₀ + εδ_{y₀} has I + sEd ≤ s − E log(1 − ε + ε e^{sZ² − s(Z−y₀)²}), whose ε-derivative at 0 is −(c(y₀) − 1) < 0; zero rate is beaten.
Consequences: Gaussian v* = 1, u* = ½ (INTERNAL_MODEL's θ = κ/(2 ln2·w) in bits); strictly sub-Gaussian shapes (uniform, symmetric
two-point) have the same u*; other sub-Gaussian shapes have u* < ½; shapes with heavier-than-Gaussian tails (Laplace, Student t) have
**u* = 0: every mode gets some bits**, so the count of represented modes is infinite and model size must mean bits.

**D4. Scaling of bits.** B(s) = Σ_i G(s·i^{−β}). With i = s^{1/β}x, B(s) = s^{1/β}·C_Z(β)·(1 + o(1)), C_Z(β) = ∫₀^∞ G(x^{−β}) dx, if the
integral converges. Two bounds hold for every finite-variance shape: (a) head: G(u) ≤ ½ ln(2u) + ½ for u ≥ ½ (the optimal Lagrangian is at
most the Gaussian one, by Theorem 26.3's upper bound), integrable at x → 0; (b) tail: G(u) ≤ u (R_Z convex, decreasing, zero at d = 1, so
R_Z(d) ≤ |R_Z′(d)|(1−d) ≤ u), integrable at x → ∞ iff β > 1. A sub-Gaussian shape has G = 0 for u ≤ u*, so the tail is empty at every β.
Sum-vs-integral error is O(ln s), relatively O(ln s / s^{1/β}) → 0 (needs the number of modes ≫ s^{1/β}). Hence **B ∝ s^{1/β} ∝ Q^{1/β}**
(stakes ∝ Q, so s ∝ Q) for (a) sub-Gaussian shapes at any β and (b) any finite-variance shape at β > 1. Gaussian check: G = ½ ln⁺(2u) gives
C = (β/2)·2^{1/β}, i.e. bits = (β/(2 ln2))·n* with n* = (2s)^{1/β}, INTERNAL_MODEL §5's ratio. For sub-Gaussian shapes the represented
count is n* = (s/u*)^{1/β} = (2v*s)^{1/β}: same exponent, larger by (v*)^{1/β}.

## 4. What is not derived (scope)

1. **Dependent modes.** For non-Gaussian data, principal components are uncorrelated, not independent. Both the same-covariance Gaussian
   and per-mode coding upper-bound R(D) (Theorem 26.3 read in scalar form; the vector form by the same test channel, not read), but an
   upper bound on R(D) does not bound the optimal bits, so the exponent is not derived. Natural-image modes (§2.2's β ≈ 0.905 example)
   would need this case; not checked.
2. **β ≤ 1, heavier-than-Gaussian tails.** Convergence needs G(u) = o(u^{1/β}) as u → 0; bound (b) gives only O(u). If G decays slower,
   bits grow with the number of modes (as in the random-walk β ≤ 2 case). Not derived; this is exactly the interior-minimum region.
3. **Drifting world.** Q^{min(½,1/β)} uses the scalar Gaussian bound R ≥ log₂|a| + ½ log₂(1 + q/(a²P)) (INTERNAL_MODEL §4). Not checked
   off Gaussian.
4. **Shape varying across modes.** If the shape changes with i (e.g. tails heavier for small modes), C_Z varies with i and the exponent
   can move. Outside the premise.

## 5. Independent numerical checks (`REGIME_C_PREMISE_checks/`, own code, nice 19)

- `ba_rd.py` (Blahut–Arimoto, cold start per slope, 40 slopes u ∈ [0.05, 30]; 30 for Laplace, u ≤ 8): each row has an achievable rate
  I(p, W) and a weak-duality lower bound valid for any output law. Gaussian rows match ½ ln(2u) and d = 1/(2u) (u = 30: d = 0.01667,
  R = 2.047 nats). Gaps ≤ 2.4e-5 nats (Gaussian, uniform, two-point), ≤ 0.022 nats (Laplace, coarser grid, slow convergence; upper rate used).
- Zero-rate slope (D3), exact test c(y) ≤ 1 on a grid vs 1/(2v*) from the MGF: Gaussian ½ and uniform ½ (both: zero rate at u = 0.497,
  positive rate at 0.585); two-point P = 0.2: v* = 1.3525, u* = 0.3697 (zero rate at 0.358, positive at 0.422, R = 0.139 nats); Laplace
  truncated at |x| ≤ 20: u* = 0.0722 (zero at 0.071, positive at 0.085). `laplace_trunc.py`: u* = 0.148, 0.072, 0.036, 0.018, 0.0089 at
  L = 10, 20, 40, 80, 160, i.e. u* ∝ 1/L → 0 for the untruncated Laplace, as D3 says.
- Bound (b): max R/u over all rows 0.37 (Gaussian), 0.39 (uniform), 0.33 (Laplace), 0.62 (two-point), all ≤ 1.
- `modesum.py` (B(s) = Σ G(sλ_i), 2·10⁶ modes, s spanning Gaussian n* = 10² to 10⁴; head above the table by the Shannon-bound asymptote,
  joins within 0.034 nats at u = 30, or by the entropy cap for the two-point source). Local exponent at the top of the range vs 1/β:

  | β (1/β) | Gaussian | uniform | Laplace (trunc. 20) | two-point |
  |---|---|---|---|---|
  | 0.6 (1.6667) | 1.6678 | 1.6677 | 1.6676 | 1.6668 |
  | 0.9 (1.1111) | 1.1118 | 1.1118 | 1.1118 | 1.1112 |
  | 1.5 (0.6667) | 0.6671 | 0.6671 | 0.6671 | 0.6667 |
  | 2.0 (0.5000) | 0.5003 | 0.5003 | 0.5003 | 0.5000 |

  Same exponent, different constants (bits at the top point: 3002, 3226, 3440, 5184 nats at β = 0.6). Limit: a grid source is always
  sub-Gaussian, so the numerics cannot test case 4.2 (true heavy tails at β ≤ 1); the β > 1 part of D4 is a proof, not a numerical claim.

## 6. Proposed THEORY text (applied on this branch, v1.4.6; reviewer judges)

- §0: the Regime C parenthesis gains "for independent modes of one sub-Gaussian shape, Gaussian included, with the size exponent also
  for any finite-variance shape when β > 1".
- §2.2 Regime C: Setting gains the premise (independent modes of one shape; model size means bits); the Q^{1/β} clause names the
  Gaussian tool and the wider derived scope; a new "Not derived" bullet lists §4 items 1–3 and says the interior minimum is derived for
  sub-Gaussian shapes only, and a Regime C prereg states which case its system is in; the natural-images line notes that β < 1 needs the
  premise (not checked for image modes).
- §13 changelog entry; CLAIM_MAP pointer v2.17 → v2.18 (note only).

Each change narrows a claim's stated scope to what is derived, and records that the exponent survives off Gaussian. None widens a claim
beyond a proof. N6 is unchanged (it cites §2.2, which now carries the premise).

## 7. Questions for the reviewer

1. Is D3's proof complete (both directions; the "⇐" step uses Donsker–Varadhan per output value y)? Is the result known (prior art)?
2. Is "sub-Gaussian at any β; any finite-variance shape at β > 1" the right scope wording for §0, or too long for a headline sentence?
3. Should §0 instead say only "for Gaussian modes (wider scope in §2.2)"?
4. Case 4.2: is there a quick bound on G(u) at small u for exponential tails (e.g. Laplace) that would close β ≤ 1 for those shapes?
5. Is requiring a Regime C prereg to state its case (premise met / not derived) the right minimal rule, or should it be in N6?
