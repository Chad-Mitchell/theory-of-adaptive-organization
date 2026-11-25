# Unified factored representations and forgetting: a locked prediction and three open gaps

*Tuesday 24 November 2026, evening (America/New_York). One application note, written by one executor for Chad Mitchell; self-checked only, **no independent review yet** (a separate reviewer is owed, `OPEN_WORK.md`, row `UFR-GAPS`). Not a test of the hypothesis. No new derivation. `THEORY.md` and `CORE.md` are not edited. No data have been run.*

> **The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.** (`CORE.md:7`)

Labels used below: **observed** (stated by the paper, with its section or figure), **repo** (stated or proved in this repository, cited `file:line`), **hypothesis** (a guess this note makes and does not derive), **open** (a gap, with the derivation it needs).

## 1. What the paper reports (observed)

Paper: J. Lehman and K. O. Stanley, *Unified Factored Representations Resist Catastrophic Forgetting*, arXiv:2611.11020v1, 7 Nov 2026, https://arxiv.org/abs/2611.11020. Announced by Lila Sciences on 24 November 2026 (thread https://x.com/joelbot3000/status/2125280929967190380). Everything in this section is the authors' claim, not ours.

- **Hypothesis (Abstract, §1).** Catastrophic forgetting is largely a side effect of a fractured, entangled representation (FER). A unified, factored representation (UFR) resists it with no change to the training algorithm or the architecture. UFR means each regularity is encoded once and reused, and independent factors are kept separate (§2.1). Outputs can be identical while internal organization differs (§2.1; thread post 2125280932055888237).
- **Method (§3.3, Fig 2).** Cyclic fine-tuning: train on part of the input range toward a variant, then back, repeatedly. Forgetting is the loss on the held-out complement.
- **Toy domain (§4, Fig 3, Fig 6, App A).** Four hidden layers of 20 ReLU units. Targets are even functions on [−1, 1]; the Abs setup switches between |x| and 0.25|x|. A hand-built UFR network forgets much less than SGD networks of the same architecture over 20 seeds. In that network only two units per hidden layer carry signal; the other 18 have zero incoming and outgoing weights (App A).
- **Image domain (§5, Fig 7, Fig 8).** Evolved Picbreeder networks (Skull, Butterfly, Apple) forget less than the best SGD networks found by a search over depth, width, optimizer and activation.
- **Controls (§5.3, §6; App C, H).** Adding free capacity to a UFR network raises forgetting (Fig 11). SGD networks with the evolved topology or fewer parameters forget more (App C). A large GELU network that copies the evolved features keeps most of the resistance (App H). A representation loss applied only before fine-tuning reduces forgetting: the symmetry loss gave a 47% reduction on Butterfly (fly) (§6.2). Representation distillation reduced it in three of four Picbreeder tasks (§6.2, Fig 8).
- **Stated limits.**
  - The change being fine-tuned must fit how the network is factored: Sawtooth on a symmetric UFR, and an X on the skull, still cause forgetting (Fig 6, Fig 8, §5).
  - There is no general way to construct UFR; the UFR networks are hand-built or evolved (§3.4).
  - Naive incremental elaboration breaks the UFR (Discussion, App J): of 20 seeds, 2-level UFR elaborated to 3-level fits the target in 6; those 6 reach a median held-out loss 6.1 times the reference.
  - The paper does not present a method ready to scale (Discussion).
- **Thread (observed).** Joel Lehman: "We don't have a mathematical definition" of UFR (post 2125314236582948960). He also describes a related method as looking for "regular (compressible/low rank) activation patterns" (post 2125322529602666625).

## 2. LOCKED PREDICTION UFR-P1 (a hypothesis, not derived)

The block between the two markers is the locked text. Its SHA-256 is given under the block. It is computed over the exact bytes of the lines strictly between the markers (UTF-8, LF line ends, each line including its newline). Any edit to the block after the lock is a breach (`process/PROCESS.md` §1 item 4), not a miss. To verify:

```
awk '/^<!-- PREDICTION-BLOCK-END -->$/{f=0} f{print} /^<!-- PREDICTION-BLOCK-START -->$/{f=1}' applications/UFR_FORGETTING_2026-11-24.md | sha256sum
```

<!-- PREDICTION-BLOCK-START -->
**UFR-P1. Status: hypothesis. Not derived from the repository. No data run by us at the time of locking.**

**What is claimed.** At equal fit, among networks trained from scratch on the Abs setup of arXiv:2611.11020 (§4, Fig 3a, App A), the more redundant the activations a network holds at the end of initial training, the more it forgets under the authors' cyclic fine-tuning. "Redundant" is defined only by the measure R below.

**Protocol (all of it is the authors' App A, unchanged, except what this block adds).**
- Architecture: four hidden layers of 20 ReLU units, scalar input and output. Optimizer, learning rate, warmup, batching, iteration counts, early stopping, gradations (5 per half-cycle), cycles (20), the 101-point input draw per seed, the training half (x ≥ 0) and the held-out half (x < 0): all as in App A. If a re-implementation is used instead of released code, it follows App A and is reported as a re-implementation.
- Target class: only the Abs setup (|x| and 0.25|x|), a UFR-compatible change of slope. The Sawtooth and any other target that does not fit the regularity are outside the class. No claim is made about them.
- Arms (20 seeds each): SGD from scratch; SGD plus the symmetry loss (weight 0.25); SGD plus representation distillation (weight 0.1, k = 8, teacher the hand-built UFR). Seeds 0–19 for the first two arms and 100–119 for distillation (disjoint, as the paper does). If the authors' release fixes other seeds, use those and log the change before any data.
- The hand-built UFR network is not in the scored set (it has no initial-training phase).

**Equal-fit criterion.** A network enters the scored set only if its mean squared error on the 101 training points of its seed, at the end of initial training and before any fine-tuning, is below 1e-4. (The number is borrowed from the paper's own fit threshold in App J; the use here is this block's choice.)

**Primary measure R (computed once, at the end of initial training, before any fine-tuning, with parameters cast to float64).**
1. Grid: x_k = −1 + k/100, k = 0, …, 200 (201 points; inputs only, both halves, no labels).
2. For each hidden layer l = 1, …, 4: A_l is the 201 × 20 matrix of post-ReLU activations. Subtract each column's mean over the 201 points.
3. Singular values s_1 ≥ … ≥ s_20 of the centered A_l (numpy.linalg.svd, compute_uv=False). Let S_l be their sum. If S_l < 1e-12, set erank_l = 0. Otherwise p_i = s_i / S_l and erank_l = exp(−sum over p_i > 0 of p_i ln p_i) (the entropy effective rank).
4. R = (erank_1 + erank_2 + erank_3 + erank_4) / 4.

**Outcome F.** The paper's forgetting quantity for the Abs setup: mean squared error on the held-out half (the 50 points with x < 0 of the seed's draw) after the 20th cycle of cyclic fine-tuning.

**Ranking statistic.** Spearman rank correlation rho (average ranks for ties) between R and F over the pooled scored set.

**Predicted sign and threshold.** rho > 0. A hit needs rho ≥ +0.40 and a one-sided permutation p ≤ 0.01 (10,000 random permutations of F over the pooled set, numpy default_rng seed 20261124, p = (1 + number of permutations with rho ≥ the observed rho) / 10,001).

**Miss.** Any scored result that is not a hit. Its signed size is rho_observed − 0.40, in correlation units, always reported (so a rho of 0.25 is a miss of −0.15). A scored result with rho_observed ≤ −0.40 is logged as a sign-reversed miss. Misses and hits are logged on the template `process/MISS_LOG_TEMPLATE.md`.

**Inconclusive (logged, neither hit nor miss).** Fewer than 30 networks pass the equal-fit criterion; or any arm contributes fewer than 8 passing networks; or a code error is found (location: `measurement/code`).

**Reported but not scored.**
- S1: within-arm Spearman rho for each arm. Reporting rule: if the pooled result is a hit but the median within-arm rho is below +0.20, every write-up must say "arm-level association only".
- S2: whether the hand-built UFR network has R at or below the smallest R of the scored networks, and F at or below the smallest F.
- S3: Spearman rho between F and the L2 norm of all weights at the end of initial training (the named rival measure), and whether |rho_R| exceeds |rho_norm| by at least 0.10.

**Named null.** rho = 0. Under it the standard error of rho is about 1/sqrt(n − 1), about 0.13 at n = 60, so the threshold is roughly three standard errors from the null. No other odds are stated.

**What was known before locking.** The author read the paper's text, figure captions and the announcement thread, which report forgetting by arm in aggregate. No network was loaded, and neither R nor F was computed on any network by us. The measure and the threshold 0.40 were chosen after reading the paper and without data. R was chosen over parameter count because the paper's own controls (Fig 11; App C) show that size alone does not track forgetting. The threshold is a judgment, not a derived value.
<!-- PREDICTION-BLOCK-END -->

**SHA-256 of the block above:** `5360c2ba48ca9837cfcdd2bdc8e0f88f954f1753b5abf77746f9c53ad1b4d98f`

**Why this is a hypothesis.** The repository prices memory by the amount held (κ per nat, `THEORY.md:30`) and states a physical floor for "memory that does not predict" (`THEORY.md:36`). It has no result that links held redundancy to forgetting under fine-tuning. The step needs an interference mechanism (gap 1, §3). R is a proxy for "held beyond what predicts" and is not I_mem − I_pred. A hit would support the hypothesis; a miss is logged and the proxy or the idea is revised, not patched after the fact (`measurement/FRAMEWORK.md`, anti-rescue rule).

**Who runs it.** Not run. Either the authors, on their networks, or a later pull request here with its own run record. Compute here would run at nice 19.

## 3. Three open gaps the paper exposes

These are not results. Each says where the repository stands now, what the paper shows, and what a derivation would need.

### Gap 1. Coupled, self-induced drift (open; hypothesis for the form)

- **Repo today.** The per-item specialization sums over "separate items that drift" (`applications/GROK_BOT_MEMORY_2026-11-23.md:42`), each with an exogenous drift variance σ_i², and the hold and re-check rules follow from it (`:54-55`). The master equation holds the world exogenous, and the case where the design changes the world is the open theorem CX2/CL11 (`THEORY.md:35, 37`). The nearest results are the feedback boundary T61 (`OPEN_WORK.md:112`) and cost nesting CT34 (`THEORY.md:497`), which covers a parent that passes quantities to a team, not collateral change among held items.
- **Observed.** The system's own update on part of the domain changes what it holds on another part: destructive in FER, coordinated in UFR (§1, §3.3).
- **Candidate form (hypothesis).** σ_eff,i² = σ_i² + Σ_{j≠i} γ_ij u_j, where u_j is the rate of updates to item j and γ_ij is the variance an update on j injects into item i. A factored representation would be one where γ is sparse. If it held, T_i* = √(6k_i/(w_i σ_eff,i²)) would shorten for entangled items and the hold rule (`:54`) would tighten.
- **Derivation needed.**
  - Define γ_ij operationally (for example, the expected squared change of item i's output per update on j, from the network's Jacobian).
  - Show when variance rates add (uncorrelated increments); the cyclic back-and-forth in the paper is partly reversible, so additivity may fail.
  - Because the u_j are chosen by the design, the problem is a joint choice of updates and re-check times, so it belongs to the coupled class (CX2). The world-fixed theorems do not apply until that class is treated.
  - Check the Abs toy exactly, where γ can be computed.

### Gap 2. Redesign cost that depends on the representation (open)

- **Repo today.** A lump-sum redesign cost k makes not moving optimal inside a band (6kσ²/w)^{1/4} for a drifting optimum (`THEORY.md:182`; `theory/DYNAMICS.md:43`, CL19, prior art). k is a constant of the problem. The hysteresis consequence, CX9, is open (`THEORY.md:182`). The record needed for a redesign is open item N54 (`THEORY.md:166`).
- **Observed (App J).** Moving a 2-level UFR to the 3-level target by plain fine-tuning fits the target in 6 of 20 seeds, those 6 reach 6.1 times the reference loss, and the SGD-elaborated networks fit 20 of 20 but forget 10 times more than the reference. The paper itself calls the gap "the cost of arriving at 3-Level Abs by elaboration rather than by construction".
- **Reading (hypothesis).** The cost of moving is a function of the representation held, k = k(x), not a constant.
- **Derivation needed.** A model of k as a function of the held design; whether the band b* and the hysteresis result of CX9 survive a state-dependent k; and which part of k is a one-time lump and which depends on the path (the paper's incremental targets suggest the path matters).

### Gap 3. Saturating forgetting against diffusive drift (open; partly covered by an existing note)

- **Repo today.** The re-check interval T* = √(6k/(wσ²)) assumes Brownian drift, quadratic loss, a lumpy reset and a slack ruin cap (`applications/GROK_BOT_MEMORY_2026-11-23.md:71`). It is false as a quantitative rule when T* is not short next to the correlation time (`:72`). The check for the Ornstein–Uhlenbeck case is in `theory/LAYER_LIFETIME_2026-11-21.md:51` (§3b): a case with T_bm/τ ≈ 0.63 missed the exact fixed-period optimum by 137%, because the error has begun to saturate.
- **Observed.** The hand-built UFR networks change most in the first cycles and more slowly afterward (Fig 13 caption); UFR networks accrue almost no forgetting over 20 cycles while SGD networks forget progressively (Fig 14 caption). Neither is a measured diffusive growth.
- **Derivation needed.** First fit the shape of held-out loss against cycles on the authors' curves (data not in this repository): linear growth would be the diffusive signature, saturation points to the mean-reverting case. Then derive the barrier policy and its cost for the drift class that fits, using §3b as the starting point. Until then no re-check rule from this repository should be applied to their curves.

## 4. What this repository does not claim

- It does not claim GTAO predicts or explains the paper's result. The repository has no neural-network experiment and no derivation of forgetting.
- It does not claim the hypothesis is supported by this paper. The hypothesis is untested (`THEORY.md:41`); an observation in neural networks is not a qualifying test under `THEORY.md:45-51`.
- It does not define unified or factored representations. The paper's "factored" is a property of neural features. The repository's nesting results are about time-scale layers, levels and cost nesting (`process/VOCABULARY.md:72`), and are not evidence for UFR.
- It does not connect GTAO to novelty search or to Stanley and Lehman's earlier work; a search of main found no link (`theory/NOVELTY_NOTE_2026-11-21.md` concerns whether J itself is new).
- UFR-P1 is a hypothesis with a proxy measure. It does not claim a hit in advance, does not claim R equals I_mem − I_pred, and does not cover targets that do not fit the regularity.
- The three gaps are open questions with candidate forms. None is a theorem, and none changes `THEORY.md` or `CORE.md`.
- It does not claim the authors have seen, reviewed or endorse this note.
- The cost-bounds note (`applications/MEMORY_MISS_COST_BOUNDS_2026-11-24.md`) is about answering from a summary, not about training dynamics. It shares the picture of one wrong item contaminating dependents (`:142`), which is a parallel of structure, not evidence.

## 5. References (as the paper cites them; not re-fetched here unless noted)

- Lehman and Stanley, arXiv:2611.11020 (fetched and read in full 24 Nov 2026).
- Kumar, Clune, Lehman and Stanley 2025, *Questioning representational optimism in deep learning: the fractured entangled representation hypothesis*, arXiv:2505.11581 (cited by the paper; not read here).
- Kirkpatrick et al. 2017, doi 10.1073/pnas.1611835114, already listed at `litmap/LITMAP.md:204`.
- The entropy effective rank used for R is defined fully in §2, so the result does not depend on a citation. A Crossref search this session did not resolve the usual citation for it, so none is given.
