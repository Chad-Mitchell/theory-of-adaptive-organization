# Preregistration: T28, simulation already inside \(J\)

**Locked:** Saturday 21 November 2026, America/New_York. The exact lock timestamp is in `LOCK.txt`. Written *before* any evaluation of \(J\) on the official candidate worlds of this test, and before any Moran chain on those worlds. A SHA-256 of this file, of `predictions.json`, of `run_sim1.py`, and of `sim1_lib.py` is recorded in `LOCK.txt` at lock time (the T27 standing rule: hash-lock the runner and the library with the prereg and the predictions). None of those four files is edited after lock except to correct a typo that does not change a criterion, which would itself be a dated deviation.

**This is a new prereg, not a re-score.** It does not reuse or re-score EVO1, T27, S5, T20, T25, or any other existing run. Official worlds are drawn from the generator in `sim1_lib.draw_world` with fresh RNG seeds that do not collide with prior test sets (checked in `sim1_lib.seed_collides`).

**Hypothesis under test (may be wrong).** Simulation / rehearsal is a judgment mechanism already inside \(J\): a system can buy prediction by paying model memory \(\kappa I_{\mathrm{mem}}\) and compute instead of real losses \(w\mathbb E[\ell]\) and ruin risk. The same objective then predicts that strongly selected systems simulate more when stakes or ruin risk are high and an internal model is cheap, and simulate zero when stakes are near the model's cost. Status labels later: `in-model`; P1–P3 are `analytic` (theorems on the discrete grid, checked exactly); P4 is `numerical`. Nothing here is `PROVED` about nature. Field-untested.

**What is not under test.** The definition of \(J\) in `CORE.md`, CT4, CT20, CT22, CT33, and the T27 Boltzmann law under \(m=-\alpha J\) are already in the repository and are not re-derived as new theorems. This run tests the rehearsal mechanism's comparative statics, and whether high-\(\beta\) Moran search on the \((K,m)\) graph finds \(m^\star\) within a locked tolerance.

---

## 0. What is already on disk (readable, not a result of this test)

- Model and booking: `MODEL.md`. The equation is not a new term in \(J\).
- Design work that informed the locked grid, prices, boxes, jump counts, and the P4 tolerance used *only* the pilot seeds `20261122800..20261122819` and closed-form corner probes of the locked parameter box. Those numbers are not official results and are not scored. They are disclosed in `PILOT.md` and `pilot_explore.json` (the JSON is the first I0-box scan; the tightened box is the one locked here).
- No official candidate seed in `predictions.json` was evaluated before lock.
- Pre-lock change, disclosed: a first box used \(I_0\in[0.10,1.00]\). One corner of that box had joint \(m^\star=0\) at the intended P4 stake \(w=20\). The locked box tightens \(I_0\) to \([0.10,0.50]\) (log-uniform \(10^{U(-1.0,-0.3)}\)) *before* lock, so that every corner of the locked box has joint \(m^\star\ge 3\) at \(w=20\), and \(m^\star(W_{\mathrm{LOW}})=0\) at every \(K\). Official-valid still requires those properties on the drawn world.

---

## 1. The cost, already inside \(J\)

As in `MODEL.md`:

$$
J(K,m)=\kappa I(m)+hK+cm+(w+\lambda\chi)\,E(K,m),
$$

with \(I(m)=I_0\) iff \(m\ge 1\), and

$$
E(K,m)=e_0(K)\Bigl(1-\varphi+\frac{\varphi}{1+\varphi m}\Bigr),\qquad e_0(K)=\frac{e_{\mathrm{base}}}{1+\gamma K}.
$$

Ruin enters only as additive exposure \(\lambda\chi E\). The Lundberg cap is slack by construction. Official monotone gates are stated at fixed \(K\).

The continuous interior formula, used as a diagnostic and as the source of the FOC threshold, not as the official discrete selection, is

$$
m_{\mathrm{cont}}(K)=\Bigl[\sqrt{\frac{W e_0(K)}{c}}-\frac{1}{\varphi}\Bigr]_+,\qquad W=w+\lambda\chi.
$$

Official \(m^\star\) is the least discrete argmin of \(J\) on \(m=0,\ldots,m_{\max}\) (at that \(K\), or jointly when stated).

---

## 2. Locked prices, ladders, and worlds

Prices (all official cells): \(h=0.25\), default \(c=0.05\), \(\kappa=0.2\), default \(\lambda=0\), \(\chi=1\), \(K_{\max}=3\), \(m_{\max}=40\).

Ladders, also in `predictions.json`:

- \(W\)-ladder (P1, P2): \(0.02,0.05,0.10,0.20,0.50,1,2,5,10,20\). \(W_{\mathrm{LOW}}=0.02\), \(W_{\mathrm{HIGH}}=20\).
- \(c\)-ladder (P3), at \(w=5\), \(\lambda=0\): \(0.01,0.02,0.05,0.10,0.20,0.50,1\).
- \(\lambda\)-ladder (P1 ruin clause), at \(w=1\): \(0,0.5,1,2,5,10\).

P4 cell: \(w=20\), \(c=0.05\), \(\lambda=0\), \(\beta=40\), tolerance \(1.5\) on \(|\bar m-m^\star|\).

World generator (`draw_world`): \(e_{\mathrm{base}}=10^{U(-0.3,0.3)}\), \(\gamma=10^{U(-0.3,0.3)}\), \(\varphi=U(0.35,0.80)\), \(I_0=10^{U(-1.0,-0.3)}\).

Candidate rng seeds: `BASE_WORLD_SEED + i` for \(i=0..15\), i.e. `20261122000..20261122015`, listed in `predictions.json`. These must not collide with prior sets; a collision is a protocol bug and aborts the run.

---

## 3. Official-valid worlds

Walk the candidates in listed order. A candidate is **official-valid** if and only if all of the following hold, at the locked P4 prices and \(\beta=40\):

1. Unique discrete joint argmin \((K^\star,m^\star)\) of \(J\).
2. \(2\le m^\star<m_{\max}\) (not zero, not on the cap).
3. The mutation graph is connected from that argmin (it is connected from every design by construction; this is a sanity check).
4. Exact Boltzmann \(\pi\propto e^{-\beta J}\) on that grid already satisfies both official P4 clauses: the mode of the marginal on \(m\) equals \(m^\star\), and \(|\mathbb E_\pi[m]-m^\star|\le 1.5\). (T27 lesson: do not lock a bar the exact weights already miss.)
5. The official Moran occupation mixes: total variation to exact Boltzmann \(\le\mathrm{MIX\_TV\_MAX}=0.20\).

The first \(N_{\mathrm{OFFICIAL}}=3\) official-valid candidates are the official worlds. Further candidates are not run once three are in hand. If fewer than three official-valid worlds are found in the 16 candidates, the test is **INCONCLUSIVE**, not a fail and not a pass. A validity miss is not a prediction fail.

---

## 4. Moran process (locked; P4 only)

Reuses `run_moran_ct`, `moran_fixation`, and `exact_boltzmann` from `theory/bridge_2026-11-21/bridge_lib.py`, unmodified.

- Population \(N_{\mathrm{POP}}=201\), haploid Moran fixation, equal edge clocks, continuous-time occupation.
- Graph: \((K,m)\leftrightarrow(K\pm 1,m)\), \((K,m)\leftrightarrow(K,m\pm 1)\), and adopt/drop \((K,0)\leftrightarrow(K,m)\) for every \(m\ge 1\). The adopt/drop edges are pre-locked, not a rescue: they are there because \(\kappa I_0\) is a fixed cost (see `MODEL.md`).
- \(\beta=40\), so \(\alpha=\beta/(N-1)\).
- \(N_{\mathrm{CHAINS}}=8\) independent chains per official world.
- \(N_{\mathrm{JUMPS}}=150{,}000\) jumps per chain, \(BURN_{\mathrm{JUMPS}}=15{,}000\).
- Chain RNG seeds: `CHAIN_SEED_BASE + 1000·world_index + 10·β + c` with `CHAIN_SEED_BASE=20261122400`, \(c=0..7\), `world_index` the candidate index \(0..15\).
- Starts: chains \(0\)–\(3\) at \((K,m)=(0,0)\); chains \(4\)–\(7\) at the unique joint argmin.
- Official occupation is the pooled continuous-time occupation after burn-in.

---

## 5. Numeric pass / fail gates (written before any official run)

Every P1–P3 number is an exact discrete argmin on a finite grid, not a Monte Carlo estimate. Every such gate was computed on the 20 published pilot worlds, after the I0 tightening, *before* lock, and held 20/20 (80/80 \(K\)-rows). Official P1–P3 are the same exact checks on the official worlds.

### 5.1 Prediction (P1): \(m^\star\) nondecreasing in \(w\) and in \(\lambda\) (Topkis)

For each official world and each locked \(K\in\{0,1,2,3\}\):

1. The least discrete \(m^\star(w)\) at that \(K\) is nondecreasing on the locked \(W\)-ladder.
2. The least discrete \(m^\star(\lambda)\) at that \(K\), at \(w=1\), is nondecreasing on the locked \(\lambda\)-ladder.

The world passes P1 if all eight clauses hold. Official P1 is the conjunction over the three official worlds.

This is an **analytic theorem** (Topkis / CT20-style, \(K\) fixed, cap slack), checked exactly on the discrete grid. Joint \((K^\star,m^\star)\) along the \(W\)-ladder is recorded as a diagnostic and is **not** a gate.

### 5.2 Prediction (P2): \(m^\star=0\) below a stakes threshold

For each official world and each locked \(K\):

1. \(m^\star(W_{\mathrm{LOW}})=0\).
2. \(m^\star(W_{\mathrm{HIGH}})\ge 1\).
3. The exact threshold \(W_{\mathrm{th}}(K)=\inf\{w:m_K^\star(w)\ge 1\}\), computed by bisection on the discrete grid, lies strictly between \(W_{\mathrm{LOW}}\) and \(W_{\mathrm{HIGH}}\).

The world passes P2 if all twelve clauses hold. Official P2 is the conjunction over the three official worlds.

This is an **analytic theorem** (the first model and the first rollout must pay; single-crossing in \(w\)).

### 5.3 Prediction (P3): \(m^\star\) nonincreasing in \(c\)

For each official world and each locked \(K\), at \(w=5\), \(\lambda=0\): the least discrete \(m^\star(c)\) is nonincreasing on the locked \(c\)-ladder. Official P3 is the conjunction over the three official worlds.

This is an **analytic theorem** (Topkis in \((m,-c)\)), checked exactly.

### 5.4 Prediction (P4): high-\(\beta\) evolution finds \(m^\star\) within tolerance

On each official world, at the locked P4 cell, from the *pooled Moran occupation* (not from exact Boltzmann):

1. The mode of the marginal distribution on \(m\) equals the unique discrete joint \(m^\star\).
2. \(|\bar m-m^\star|\le 1.5\).

The world passes P4 if both clauses hold. Official P4 is the conjunction over the three official worlds.

This is a **numerical** test of the finite-sample Moran process. Exact Boltzmann values on the same cell are a validity screen (section 3.4) and a diagnostic. The tolerance \(1.5\) was set from the exact Boltzmann \(|\mathbb E[m]-m^\star|\) on the 20 published pilots at \(\beta=40\) (maximum \(0.767\)) plus room for sampling error; a 5-world mixing probe at the locked jump counts had empirical errors at most \(0.752\) and TV at most \(0.054\). Those pilots are not official worlds.

### 5.5 Overall

- **PASS** if and only if there are three official-valid worlds and P1, P2, P3 and P4 all pass on every one of them.
- **FAIL** if there are three official-valid worlds and any of P1, P2, P3, P4 fails on any official world.
- **INCONCLUSIVE** if fewer than three official-valid worlds are obtained from the 16 candidates.

Predictions will not be patched after seeing official data. A change of criterion, if one is ever needed, goes in a dated DEVIATIONS file *before* any further official scoring, and the original gates remain the official result of this prereg.

---

## 6. Pilot (not official)

See `PILOT.md`. Pilot seeds `20261122800..20261122819` only, plus box-corner probes. Official seeds were not evaluated. The locked P4 jump counts, \(\beta\), tolerance, \(W\)-ladder, and the tightened \(I_0\) box are design inputs informed by those pilots, not results of T28.

---

## 7. What would not be a rescue

- Changing prices, ladders, \(\beta\), the \(1.5\) tolerance, or the validity floors after seeing official scores.
- Scoring official P4 on the exact Boltzmann weights instead of the simulated occupation.
- Promoting the joint-\((K,m)\) diagnostic to a gate, or dropping a failing official world and walking further through the candidate list to replace it. The first three official-valid candidates are the official set; they are not replaced.
- Re-interpreting a mixing miss as a prediction pass or fail.
- Editing `run_sim1.py` or `sim1_lib.py` during the official run (T27 standing rule).
