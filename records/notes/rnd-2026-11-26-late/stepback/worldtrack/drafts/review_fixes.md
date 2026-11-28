
## 4. Review fixes (REVIEW_WORLDTRACK §9; appended 26 Nov 2026 after Step 3's results; governs §§0–2 where they conflict)

*Source: `rnd/review_worldtrack/REVIEW_WORLDTRACK.md`, outcome PASS-WITH-FIXES, reviewed prefix `568eff32…6ed9` (Steps 0–1 and §2). Nothing above is edited. Fixes 1–9 follow in the review's order.*

### 4.1 Fix 1: Step 0's α* values are set by the menu cap

- **The review's own reruns, its §3.1 table:**

| T, λ | α* at N(T) | α* at 3N(T) | α* at N = 720 | α* at N = 1440 |
|---|---|---|---|---|
| 8, 30 | 0.325 | 0.8745 | 0.9975 | 0.9975 |
| 8, 1000 | 0.011 | 0.0415 | 0.1575 | 0.300 |
| 20, 30 | 0.3355 | 0.7925 | 0.990 | 0.9975 |
| 20, 1000 | 0.0115 | 0.035 | 0.065 | 0.130 |

- In the scored menu, the polygon at α* lies within 10% of N(T) in **22 of 60** cells.
- **Relabelled.** The α* values in §0.9 and §0.10, "α* decreases with λ" and "α*·λ → ≈ 12" are **OBSERVED for n ≤ N(T) only**: they describe the menu.
- "α* → 1 over all regular polygons" is **HYP**, with the trend observed up to N = 1440.
- **The single-switch shape is robust:** 59 of 60 at 3N(T), and 8 of 8 big-menu cells at N = 720 and 1440. OBSERVED, on a subset.
- **§0.11 R3 is upgraded from HYP to OBSERVED:** α* rises with N, and the rise is large.

### 4.2 Fix 2: the Step 0 sentence sent to Chad

- "Below α* polygons win, above it the disk does" is corrected to: **"for polygons up to N(T) vertices, polygons are strictly cheaper below α* and none is strictly cheaper above it. With larger menus the switch moves toward α = 1, and the margins are 1e−7 to 1e−4."**
- The parent should carry this wording into any message.

### 4.3 Fix 3: Step 1's corner rule

- REQUIREMENTS_FIRST Route 1 asked for "no corner solutions". The hashed §1.5 relaxed that by treating s* = 1 as a stated regime.
- The tick binds in **150 of 432** primary cells (35%).
- In §1.12 row 1, "a unique interior (n*, s*)" becomes **"a unique (n*, s*), with n* interior; s* is at the lower bound s = 1 in 150 of 432 cells"**.

### 4.4 Fix 4: one scaling identity behind Step 1's read-dominated results

- **The identity** (the review's §3.2; PIM to leading order in σ_w → 0, s ≫ 1, Γ = 0, ignoring wrapping):
  - Use L ≈ π²/(6n²) + σ_w²·s/4, and note that the read entropy depends only on ρ = σ_w√s·n/(2π).
  - Substituting n = 2πρ/(σ_w√s) gives J = h(ρ)/s + x·σ_w²·s·g(ρ), with g = 1/(24ρ²) + 1/4.
  - Minimising over s gives s* = √(h/(g·x·σ_w²)) and J = 2σ_w√x·√(h(ρ)·g(ρ)). One minimisation over ρ remains.
- **Consequences:**
  - ρ* = 0.607 and H* = 1.107 nats are pure numbers;
  - s*·σ_w√x = 1.746;
  - n*·x^{−1/4}·σ_w^{1/2} = 2.888;
  - read cost = loss cost at the optimum;
  - **J*/(σ_w√x) → 1.2675.**
- **Relabelled as one ELEMENTARY result** (PIM to leading order): S1, S2, the R-regime half of H-c, the equal split and J ∝ σ_w√x. These are not separate observations.
- The constant is **1.2675**, not 1.244: the 1.244 was a grid median pulled down by small-s cells. With 1.2675 the register is **≈ 27% above** CORE's continuous frontier σ_w√x, not 24%. That mapping is ELEMENTARY since §2.1.

### 4.5 Fix 5: novelty

- **§1.6 and §1.10** said the R regime is "the read-floor version of Kipnis–Goldsmith–Eldar's finding … KNOWN in substance". That is **withdrawn**.
  - KGE show that under block coding a finite number of bits per sample is always suboptimal: D_W is reached only as the sampling rate goes to infinity.
  - So the interior ≈ 1.1 nats per read is a property of the chosen register class: a scalar register, renewal reads, and a read price H(R′|R) with no block coding.
- **Bar B stays "trivial in substance", for a different reason:** the scaling identity of §4.4, not KGE.
- **The Berger formula is KNOWN,** from KGE eq. (4), read this session (§2.1). That is already done in Step 2.
- **Bar A:** "beyond Gish–Pierce" was met literally but is **uninformative**, because Gish–Pierce has no time in it. Any rate-priced tracking of a Wiener process has the drift in its design scale (Berger 1970; KGE 2019).

### 4.6 Fix 6: the class claim (§1.13 W1) and INFO-BUDGET's criterion

- **W1 is reworded to the review's §6 wording:**
  > *"In the noiseless discrete-register class the design is an integer n\* by construction, and the class fixes H\* ≈ 1.1 nats per read. Across classes, only the σ_w√x cost scaling is supported, and it is KNOWN (Berger 1970). Whether any discrete design is optimal among all memories is OPEN."*
- **"A continuous noisy memory beats every finite register" is HYP,** and "every" is dropped. Step 2 compared the register only with CORE's Gaussian memory, under the costs as booked in Step 2. No noisy register and no event-triggered reads were tested.
- **"The information budget survives a change of class" is HYP, contradicted** for the per-read part:
  - under ideal coding (KGE), the per-look information runs to 0;
  - in CORE's class with no per-look price, Step 2 found the look rate at the sensor limit and the nats per look following s_min·σ_w√x.
- **INFO-BUDGET's criterion.** Step 2 was hashed before this review arrived, and its B1 and B2 were scored as pre-stated. The review asks that the look rate and the per-look information be treated as outcomes, including the possibility that the look rate runs to the fastest sensor rate. Step 2's pre-statement already predicted and observed exactly that (§2.4, §2.9). So no rescoring is needed, and its MISS stands.

### 4.7 Fix 7: the a = 1 arm

§1.9's "n* changes by 1 in 73 cells" is corrected to: **n* changes in 72 cells; 34 by 1; the largest change is 41 (σ_w = 0.3, x = 1e6: 1814 → 1773, 5.9%). s* changes in 2 cells.** The calls are unchanged.

### 4.8 Fix 8: process

- From this section on, WORKLOG hash entries carry the time to the second (`date -Iseconds`).
- **Step 0's ordering within the minute 18:31 cannot be verified after the fact.** The pre-statement hash and the first scripts share that minute.

### 4.9 Fix 9: prior art to read before any novelty claim about the constants

Named as related. **Content not yet read.** Metadata was checked on Crossref by the review (`rnd/review_worldtrack/rv_crossref_dois.txt`) and re-checked by me (`worldtrack/crossref_sp.txt`, 5 of 5 OK):
- Åström & Bernhardsson 2002, periodic against event-based sampling, 10.1109/cdc.2002.1184824;
- Rabi, Moustakides & Baras 2012, 10.1137/090757125;
- Sun, Polyanskiy & Uysal 2020, sampling the Wiener process for remote estimation, 10.1109/tit.2019.2937336;
- Neuhoff & Gilbert 1982, causal source codes, 10.1109/tit.1982.1056552;
- Tatikonda, Sahai & Mitter 2004, 10.1109/tac.2004.834430.

Whether ρ* = 0.607 or H* = 1.107 appear in that literature is OPEN.
