# Field-2 feasibility & cache anchor: non-silicon candidates for the cross-field map (21 November 2026)

*Saturday 21 November 2026, written beside `main` `cd84095` and `theory/CROSS_FIELD_MAP_2026-11-21.md` (PR #135). **Pass 0 feasibility only: not a prereg, nothing locked, no scored test run.** The hypothesis sentence is unchanged: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." All DOIs below were resolved via Crossref or DataCite this session; no paywall logins or accounts were used; no numbers are invented.*

## 0. Scope and criteria (from `CROSS_FIELD_MAP_2026-11-21.md`)

In `theory/CROSS_FIELD_MAP_2026-11-21.md` (§§1–2, 5–6), the cross-field test requires a **reuse world** (many distinct items whose miss share $m(s)$ decreases with fast-tier capacity $s$, specifically $m(s) \sim s^{-\theta}$ with $\theta > 0$ in the scale-free regime, requiring Zipf rank-frequency exponent $\alpha_{\text{rank}} = 1 + \theta > 1$) paired with a storage technology whose holding cost per unit capacity scales with access latency $t$ as $c(t) = a \cdot t^{-\gamma}$ ($\gamma > 0$), and an observed ladder of $K$ tiers $(s_k, t_k)$ whose interior ratios $(r_s, r_t, q)$ are compared against the finite-$K$ Chow/GTAO solution.

For Pass 0 feasibility, a candidate non-silicon field needs:
1. **$\theta$ (world):** published, verifiable miss or rank-use curves measured independently of the tier sizes.
2. **$\gamma$ (technology):** published, verifiable unit holding cost vs. retrieval/access latency across tiers, measured independently of demand skew.
3. **Ladder:** published capacities, counts, and access delays across $K \ge 2$ (ideally $\ge 3$) physical tiers.
4. **Independence & selection:** the three legs must be mutually independent (R4 in `theory/REVEALED_PRICES_2026-11-21.md`), not circularly engineered via Chow/Roundy geometric-program optimization (R3), and ideally under non-trivial selection pressure.

---

## 1. Cache anchor attempt ($\gamma$ from the five-minute-rule papers)

Before evaluating non-silicon fields, we compile $\gamma$ for the silicon/magnetic **cache anchor** from the two five-minute-rule papers cited in `CROSS_FIELD_MAP_2026-11-21.md` §5–6. Note that engineers size storage hierarchies using these same cost-latency equations, so silicon is an **anchor**, not independent support. Neither paper lists per-bit SRAM/L1/L2 prices; both cover DRAM through Tape.

### 1.1 Compiled price-latency tables

**Gray & Graefe 1997** (*SIGMOD Rec.* 26(4):63–68; MSR-TR-97-33; Crossref DOI `10.1145/271074.271094`), **Table 8** ("Performance Metrics of high-performance devices circa 1997", MSR-TR-97-33 p. 6):

| Device | Unit capacity | Unit price ($) | Cost ($/GB) | Latency (s) |
|---|---|---|---|---|
| RAM | 1 GB | 15,000 | 15,000 | $1.0 \times 10^{-7}$ (0.1 µs) |
| Disk | 9 GB | 2,000 | 222 | $1.0 \times 10^{-2}$ (10 ms) |
| Tape robot | 14 × 35 GB (490 GB) | 10,000 | 20 | $3.0 \times 10^{1}$ (30 s) |

**Appuswamy, Borovica-Gajic, Graefe & Ailamaki 2019** (*Commun. ACM* 62(11):114–120; Crossref DOI `10.1145/3318163`), **Tables 1, 4, 5, and 6** (pp. 116–118, 2018 metrics):

| Device | Source | Unit capacity | Unit price ($) | Cost ($/GB) | Latency / IOPS |
|---|---|---|---|---|---|
| DRAM | Table 1 & Table 6 (pp. 116, 118) | 16 GB | 80 | 5.00 | $1.0 \times 10^{-7}$ s (100 ns) |
| Intel Optane P4800X (3D XPoint) | Table 4 (p. 117) | 480 GB | 617 | 1.285 | 550k IOPS (latency not tabulated; text p. 117: tens of µs end-to-end) |
| Intel 750 PCIe SSD | Table 4 (p. 117) | 800 GB | 589 | 0.736 | 460k IOPS (latency not tabulated) |
| SATA Flash SSD | Table 1 (p. 116) | 800 GB | 415 | 0.519 | 67k read IOPS ($\approx 1.49 \times 10^{-5}$ s as $1/\text{IOPS}$) |
| HDD | Table 6 (p. 118; Table 1: $49) | 2 TB | 50 | 0.025 | $5.0 \times 10^{-3}$ s (5 ms) |
| Tape (SpectraLogic T50e LTO-7) | Tables 5–6 (p. 118) | 10 × 15 TB (150 TB) | 11,000 | 0.0733 | $6.5 \times 10^{1}$ s (65 s) |

*Note on 2018 Tape:* At the 10-slot starter capacity in Table 6, the $11,000 library drive/robotic chassis makes Tape ($0.0733/GB) more expensive per GB than a bare 2 TB HDD ($0.025/GB), breaking cost monotonicity unless amortized over a fuller cartridge count.

### 1.2 Fitted $\gamma_{\text{cache}}$ and Chow fixed-point numbers

Ordinary least squares on $(\ln t, \ln c)$ with $c \propto t^{-\gamma}$ gives:

- **Gray & Graefe 1997 (RAM, Disk, Tape; Table 8):** $\gamma = \mathbf{0.3410}$ ($R^2 = 0.9972$; pairwise RAM–Disk $0.3659$, Disk–Tape $0.3006$).
- **Appuswamy et al. 2019 (DRAM–HDD; Table 6):** $\gamma = \mathbf{0.4897}$.
- **Appuswamy et al. 2019 (DRAM, SATA SSD, HDD; Tables 1 & 6):** $\gamma = \mathbf{0.4905}$ ($R^2 = 0.9984$) using Table 6 HDD cost $\$0.025$/GB, $t_{\text{SSD}} = 1/67{,}000\,\text{s} \approx 14.9\,\mu\text{s}$; sensitivity $\gamma = 0.4826$ ($R^2 = 0.9717$) at $50\,\mu\text{s}$ and $\gamma = 0.4711$ ($R^2 = 0.9426$) at $100\,\mu\text{s}$. (Using Table 1's $\$49$ instead of Table 6's $\$50$ shifts the three-point fit only to $0.4925$.)

Combining $\gamma_{\text{cache}} \in [0.34, 0.49]$ with Hartstein et al. 2006 (`10.1145/1128022.1128064`) $\theta \in [0.3, 0.7]$ gives $\theta\gamma \in [0.102, 0.343] < 1$, well inside the contraction regime, with Chow fixed-point ratios (`CROSS_FIELD_MAP_2026-11-21.md` §2.3):
- For $\gamma = 0.341$, $\theta \in [0.3, 0.7]$: $r_s \in [12.5, 30.1]$, $r_t \in [24.5, 27.2]$, $q \in [4.19, 9.78]$.
- For $\gamma = 0.490$, $\theta \in [0.3, 0.7]$: $r_s \in [11.3, 28.5]$, $r_t \in [16.0, 18.6]$, $q \in [2.92, 6.81]$.

---

## 2. Feasibility table across non-silicon candidates

| Field (substrate) | $\theta$ source / value | $\gamma$ source / value | Ladder source / value | Independence (3 legs & Chow-style design) | Verdict |
|---|---|---|---|---|---|
| **CPU / storage caches** *(silicon anchor)* | Hartstein et al. 2006 (`10.1145/1128022.1128064`): $\theta \approx 0.3\text{--}0.7$. | Gray & Graefe 1997 (`10.1145/271074.271094`, Table 8): **0.341**. Appuswamy et al. 2019 (`10.1145/3318163`, Tables 1, 6): **0.4897–0.4905** (DRAM–HDD pairwise / DRAM–SSD–HDD, Table 6 $\$0.025$/GB). | Hardware specs (L1/L2/L3/DRAM/SSD/HDD); SRAM vs. DRAM public per-bit cost missing from both 5-min-rule papers. | **Not independent** of Chow 1974 / 5-min-rule design (engineers use the same cost model). | **Anchor** (not Field 2) |
| **Library / archive storage tiers** *(print stacks, compact, off-site depository, consortial / ILL)* | **Published, but $\alpha_{\text{rank}} < 1$ in static circulation:** Bulick 1978 (`10.5860/crl_39_03_215`, Table 1, Pitt, 107k items): Bradford-Zipf log curve, direct fit $\alpha_{\text{rank}} \approx 0.26 < 1$. O'Neill & Gammon 2014 (`10.5860/crl.75.6.791`, OhioLINK, 28.5M items, Table 6 & Fig. 3): 7.2% drive >80% of loans, implied $\alpha_{\text{rank}} \approx 0.56 < 1$. Hashimoto 2024 (`10.17605/osf.io/cq987`, Toho Med.): CCDF $\mu \in [1.63, 2.0] \implies \alpha_{\text{rank}} \approx 0.50\text{--}0.61 < 1$. Burrell 1980/85 (`10.1108/eb026693`, `10.1108/eb026772`): negative binomial. **Scale-free $\theta > 0$ unverified** (requires checking temporal-locality/LRU logs). | **Measured, independent:** Courant & Nielsen 2010 (`10.5281/zenodo.7799609`, Table 1, p. 91): open stacks **$4.26/vol/yr** vs. high-density depository **$0.86/vol/yr** (Table 2 no-inflation sensitivity: $2.52 vs. $0.60). Reilly 2003 (CLIR Pub 117, App. 4 p. 44): 8 depositories op. cost **$0.17–$2.38/vol/yr**. Payne 2007 (OCLC, p. 10): depository courier **≤ 24 h**. Implied $\gamma = \mathbf{0.28\text{--}0.35}$ (0.322 at 10 min open stack vs. 24 h depository; 0.289 without construction inflation). ILL (Jackson 2004, ARL): $18.35/tx, 15.6–16 days; OhioLINK: 2–3 days. | **Measured:** Payne 2007 (Tables 1–2, pp. 12–13): 68 North American high-density facilities (>70M vols of ~1B academic vols). O'Neill & Gammon 2014 (Table 3, p. 796): non-circulating reserve/ref (11.4%), ARL open stacks (7.45M items, circ 0.144/yr), depositories (4.18M items, circ 0.025/yr). Cooper 1989/91 (`10.1086/602134`, `10.1086/602396`) also cover on-campus compact shelves. | **High independence:** $\gamma$ (building/utility/staff accounting) is independent of circulation curves and tier capacities; no Chow multi-tier ratio optimization used (Cooper 1989 is a 2-tier cutoff rule). **Selection caveat:** non-profit institutions with weak budget selection (Lawrence et al. 2001, `10.5860/crl.62.6.541`, p. 542). | **Partial** *(strongest non-silicon candidate; $\gamma$ & ladder ready, $\theta > 0$ vs. $\alpha < 1$ gate must be resolved first)* |
| **Records management / NARA Federal Records Centers** *(office, agency staging, FRC off-site)* | **Missing:** no published box/series retrieval-frequency power law or $\theta$ located. | **Sparse:** NARA/GAO-13-668 notes FRC storage fee $0.23/cu ft/mo ($2.76/cu ft/yr in 2013) and 1-business-day turnaround (NARA 2025 FRC Toolkit); no peer-reviewed multi-tier $/cu ft/yr vs. retrieval-latency dataset found across active office/staging/FRC. | **Partial:** NARA 2025 FRC Toolkit documents 18 FRCs (>29M cu ft) with 1-business-day retrieval; office/staging capacities uncompiled. | Independent of Chow optimization, but non-market statutory mandate (44 U.S.C. 2907/3103). | **Partial** *(missing $\theta$ and systematic multi-tier $\gamma$)* |
| **Biological memory** *(synaptic / systems consolidation)* | **Behavioral only:** Anderson & Schooler 1991 (`10.1111/j.1467-9280.1991.tb00174.x`) environmental need odds and Wixted & Ebbesen 1991 (`10.1111/j.1467-9280.1991.tb00175.x`) forgetting curves $R(t) \propto t^{-b}$; no synaptic $m(s) \sim s^{-\theta}$ miss curve. | **Missing:** Cohen et al. 2013 (`10.1371/journal.pone.0063191`), Heo et al. 2018 (`10.1073/pnas.1720956115`), and Karbowski 2019 (`10.1152/jn.00092.2019`) quantify synaptic protein turnover ATP cost ($3.7\times 10^3$ ATP/min/PSD at $t_{1/2} = 3.67$ d), **not** unit cost vs. retrieval latency $t$ across consolidation tiers (consolidation is ordered by retention time, not access speed; cortical task metabolic delta is ~1%). | **Missing as ratio data:** Benna & Fusi 2016 (`10.1038/nn.4401`) fix cascade ratio $n^2$ as a model parameter; working-memory (~3–5 chunks) vs. hippocampal vs. neocortical capacity/latency ratios lack a unified $\theta, \gamma$-matched dataset. | Strong natural selection, but missing two of three quantitative legs. | **No** *(missing synaptic $\theta$, retrieval-latency $\gamma$, and measured ladder ratios)* |
| **Adaptive immune memory** *(effector, central, resident memory, bone-marrow plasma cells)* | **Repertoire size only:** BCR/TCR clone-size power laws (e.g., Chardès et al. 2022 `10.1073/pnas.2113512119`, $\beta \approx 1.2\text{--}2.4$), not an antigen re-encounter miss curve $m(s) \sim s^{-\theta}$ ($\theta > 0$). | **Qualitative only:** plasma cells run high OXPHOS/glycolysis while resting memory cells use low-rate fatty-acid oxidation (Ron-Harel et al. 2014 `10.1159/000362502`); memory recall starts ~1–2 d faster than naïve (Schnaack & Nourmohammad 2021 `10.7554/eLife.61346`). No per-clone ATP/s vs. recall-latency $\gamma$ table. | **Qualitative:** multi-compartment memory subsets exist, without published per-tier capacities and recall delays tied to unit costs. | Strong natural selection, but missing quantitative $\theta$ and $\gamma$. | **No** *(missing $\theta$ miss curve and quantitative $\gamma$)* |
| **Supply chain / multi-echelon inventory** *(store, regional DC, national DC)* | **$\alpha_{\text{rank}} < 1$ or Gaussian:** Amazon books $\alpha_{\text{rank}} = 0.871 < 1$ (Brynjolfsson, Hu & Smith 2003 `10.1287/mnsc.49.11.1580.20580`); consumer electronics $\mu \in [1.35, 1.8] \implies \alpha_{\text{rank}} \in [0.56, 0.74] < 1$ (Hisano et al. 2011 `arXiv:1101.5888`); Willems 2008 (`10.1287/msom.1070.0176`) & Moncayo-Martínez et al. 2026 (`10.1016/j.dib.2026.112991`) use Gaussian stage demand across BOMs, not reuse $m(s) \sim s^{-\theta}$. | **Missing / unpublished:** firm holding costs ($h = i \cdot v$) scale with SKU dollar value rather than a cross-tier $t^{-\gamma}$ storage technology law; retail vs. RDC/NDC space-cost-vs-lead-time tables are proprietary and unpublished. | **Proprietary or normative:** Roundy 1985 (`10.1287/mnsc.31.11.1416`) integer-ratio intervals are an optimization policy; Bartholdi & Hackman 2008 (`10.1080/07408170802167662`) optimize forward-pick vs. reserve space. | **Fails independence & R3:** engineered via Roundy/Graves-Willems optimization (Chow-style design); firm cost data closed. | **No** *(missing open $\gamma$, $\alpha < 1$ or non-reuse demand, Chow-style design)* |
| **Hospital pharmacy tiers** *(ward ADC, central pharmacy, regional wholesaler)* | **Skewed, $\alpha_{\text{rank}}$ unreported:** Wright & Bates 2010 (`10.4338/aci-2009-12-ra-0023`): 442,658 EHR medication orders, top 11.8% generate 80% of orders (fit with `zipfR`, numeric $\alpha_{\text{rank}}$ not reported). | **Missing:** Walczyk et al. 2024 (`10.1177/00185787231214416`) measure ADC carrying-cost savings, but no open unit storage-cost vs. retrieval-delay $\gamma$ table across ADC, central pharmacy, and wholesaler exists. | **Partial:** ADC vs. central pharmacy vs. wholesaler tiers are standard, with 321 ADCs at JHH (`10.1177/00185787231214416`), without published multi-tier capacity/delay ratios. | ADCs explicitly tuned via EOQ / average-daily-usage PAR formulas. | **No** *(missing $\gamma$, numeric $\theta$, and non-EOQ independence)* |
| **Firm knowledge / production hierarchies** *(Garicano / Jaques)* | **Missing:** no independently measured problem-frequency miss exponent $\theta$. | **Missing:** Garicano 2000 (`10.1086/317671`) & Caliendo et al. 2015 (`10.1086/681641`) model/measure wage by layer, which is an equilibrium output rather than a $t^{-\gamma}$ technology law (`CROSS_FIELD_MAP` §5). | **Measured in part:** French/Swedish firm layer counts and span-of-control ratios (Caliendo et al. 2015 `10.1086/681641`). | Missing both $\theta$ and $\gamma$. | **No** *(missing both exponents)* |

---

## 3. Recommended single next field and draft preregistration outline

### 3.1 Recommendation: Research Library Print Storage Tiers (conditional on a Pass 1 $\theta$ check)

**Choice:** **Research library physical storage hierarchies** (Open Stacks $\to$ On-Campus Compact Shelving [where present] $\to$ Off-Site High-Density Depository $\to$ Consortial / Interlibrary Loan), tested beside the **Silicon Cache Anchor** (§1).

**Why it wins on Pass 0:**
1. It is the **only** non-silicon field found where the technology exponent $\gamma \approx 0.28\text{--}0.35$ ($\approx 0.32$ from Courant & Nielsen 2010 $4.26 vs. $0.86/vol/yr and Payne 2007 24 h delivery), multi-tier physical capacities and retrieval delays (O'Neill & Gammon 2014; Payne 2007; Jackson 2004), and circulation-skew datasets all exist in **open, peer-reviewed / institutional publications** with zero paywall barriers.
2. The three legs are **mutually independent**: $\gamma$ comes from building construction, utilities, and staffing accounting; circulation skew comes from patron checkout logs; and no library uses Chow's multi-tier geometric-program ratio formula.
3. Crucially, $\gamma_{\text{library}} \approx 0.32$ sits close to $\gamma_{\text{cache, 1997}} \approx 0.34$ and below $\gamma_{\text{cache, 2018}} \approx 0.49$, enabling a direct cross-substrate check if $\theta$ is established.

**The decisive Pass 0 caveat (honesty gate before locking):**
All four published static print-circulation studies checked here exhibit $\alpha_{\text{rank}} < 1$ ($\approx 0.26$ in Bulick 1978, $\approx 0.56$ in OhioLINK 2014, $\approx 0.50\text{--}0.61$ in Hashimoto 2024, negative-binomial/log-normal in Burrell 1980 and Huddersfield). By `CROSS_FIELD_MAP_2026-11-21.md` §1 & §5 (the same qualification applied to Breslau et al. 1999), $\alpha_{\text{rank}} < 1$ gives a finite-catalog curve $m(s) \approx 1 - (s/N)^{1-\alpha}$, **not** scale-free $m(s) \sim s^{-\theta}$ with $\theta > 0$. Before locking any cross-field prereg, **Pass 1** must test on an open raw circulation transaction log (e.g., an open institutional circulation dataset) whether **recency/LRU stack-distance reuse** follows $m(s) \sim s^{-\theta}$ with $\theta > 0$ — or, if $m(s)$ remains $\alpha_{\text{rank}} < 1$ under recency, replace the scale-free closed-form ratios with the **numerical $J$-minimum** computed on the empirically measured $m(s)$ curve.

### 3.2 Draft outline for a locked preregistration (Pass 1 $\to$ Prereg; do NOT lock yet)

1. **Frozen out-of-sample inputs (R1, R4):**
   - **$\gamma_{\text{lib}}$:** Lock from published cost-per-volume and retrieval-delay pairs disjoint from the test libraries' tier sizes (Courant & Nielsen 2010 Table 1–2; Reilly 2003 App. 4; Payne 2007; Cooper 1989/91; Jackson 2004), with pre-specified open-stack retrieval-time bounds (e.g., 5–30 min) and depreciation sensitivity.
   - **$m(s)$ / $\theta_{\text{lib}}$:** Lock on a pre-specified, disjoint circulation log dataset (e.g., one university library's historical checkout stream or OhioLINK aggregate) *before* fetching held-out target library tier capacities. Pre-specify the functional-form gate: fit $m(s) = A s^{-\theta}$ vs. finite-catalog $1 - (s/N)^{1-\alpha}$ and negative binomial by out-of-sample AIC/KS over $\ge 1.5$ decades in $s$.
   - **Held-out target systems:** $N \ge 3$ research library systems with $\ge 3$ documented physical tiers (e.g., UC campus open stacks / NRLF-SRLF / ILL; Columbia-Princeton-NYPL / ReCAP / ILL; Harvard Widener / Harvard Depository / ILL; OhioLINK ARLs / Depositories / Consortial borrowing), with tier capacities $s_k$, total catalog $S$, retrieval times $t_k$, and budget/selection context recorded before scoring.
2. **Prediction (finite-$K$ Chow/GTAO solution with boundary transient):**
   - Compute predicted tier capacity ratios $s_k / s_{k-1}$ and delay ratios $t_{k+1}/t_k$ from the exact finite-$K$ solution (`CROSS_FIELD_MAP_2026-11-21.md` §2.5 item 1) if $\theta > 0$ passes the functional-form gate, or from the numerical $J$-minimum on the frozen empirical $m(s)$ curve if $\alpha_{\text{rank}} < 1$.
   - Joint cross-field test alongside the silicon cache anchor ($\gamma_{\text{cache}} \approx 0.34\text{--}0.49$, $\theta_{\text{cache}} \in [0.3, 0.7]$): test whether the $(s_k/s_{k-1}, t_{k+1}/t_k)$ shift between caches and libraries matches the $(\theta, \gamma)$ map's predicted direction and magnitude.
3. **Named rivals (R3):**
   - **R0 (Local institutional norm / null cross-field link):** Each field's tier ratios are set locally with no shared dependence on $(\theta, \gamma)$; specifically, library off-site transfer follows uniform institutional heuristics (e.g., "zero circulation in last 5–10 years") yielding capacities uncorrelated with $\gamma$ and $m(s)$ slope.
   - **R1 (Legacy campus-building cap):** Open-stack capacity $s_1$ is frozen at historical building shelf capacity and all overflow moves off-site regardless of retrieval delay $t_2/t_1$ or cost exponent $\gamma$.
4. **Kill conditions (R2):**
   - **K1 (Scope / reuse-curve kill):** If both rank-based and recency/LRU $m(s)$ fail to monotonically predict miss share across tiers, or if $\alpha_{\text{rank}} < 1$ fails the scale-free prerequisite *and* the numerical $J$-optimum on empirical $m(s)$ predicts $K^* = 1$ (no interior tier) at observed $\gamma$, the scale-free cross-field map is inapplicable to print libraries.
   - **K2 (Quantitative / rival kill):** On held-out library systems, if the preregistered finite-$K$ GTAO prediction has higher log-ratio RMSE on $(s_k/s_{k-1}, t_{k+1}/t_k)$ than R0 or R1, or misses the directional cache-vs-library contrast, the cross-field prediction fails. (Note: because libraries are weakly selected non-profit institutions, a miss on libraries must record qualification status per `CORE.md` §3 rather than over-claiming against strongly selected systems.)
   - **K3 (Circularity / R4 kill):** Any discovery that the held-out library system's tier capacities were sized by fitting a multi-tier geometric-program cost-latency model disqualifies that system from the scored set.

---

## 4. Verified source registry (DOIs checked on Crossref / DataCite)

- **Appuswamy et al. 2019** — *Commun. ACM* 62(11):114–120. Crossref DOI: `10.1145/3318163`.
- **Gray & Graefe 1997** — *SIGMOD Rec.* 26(4):63–68 (MSR-TR-97-33). Crossref DOI: `10.1145/271074.271094`.
- **Hartstein et al. 2006** — *Proc. 3rd Conf. Computing Frontiers*. Crossref DOI: `10.1145/1128022.1128064`.
- **Chow 1974** — *IBM J. Res. Dev.* 18(3):194–203. Crossref DOI: `10.1147/rd.183.0194`.
- **Breslau et al. 1999** — *IEEE INFOCOM '99*. Crossref DOI: `10.1109/infcom.1999.749260`.
- **Bulick 1978** — *Coll. Res. Libr.* 39(3):215–219. Crossref DOI: `10.5860/crl_39_03_215`.
- **O'Neill & Gammon 2014** — *Coll. Res. Libr.* 75(6):791–807. Crossref DOI: `10.5860/crl.75.6.791`.
- **Burrell 1980** — *J. Doc.* 36(2):115–132. Crossref DOI: `10.1108/eb026693`.
- **Burrell 1985** — *J. Doc.* 41(1):24–39. Crossref DOI: `10.1108/eb026772`.
- **Cooper 1989** — *Libr. Q.* 59(3):239–260. Crossref DOI: `10.1086/602134`.
- **Cooper 1991** — *Libr. Q.* 61(4):412–432. Crossref DOI: `10.1086/602396`.
- **Lawrence, Connaway & Brigham 2001** — *Coll. Res. Libr.* 62(6):541–553. Crossref DOI: `10.5860/crl.62.6.541`.
- **Sandler 2012** — *Insights* 25(3):282–288. Crossref DOI: `10.1629/2048-7754.25.3.282`.
- **Courant & Nielsen 2010** — in *The Idea of Order*, CLIR Pub 147, pp. 81–105. DataCite DOI: `10.5281/zenodo.7799609`.
- **Hashimoto 2024** — Toho Univ. Medical Media Center circulation study. DataCite DOI: `10.17605/osf.io/cq987`.
- **Reilly & DesRosiers 2003** — *Developing Print Repositories*, CLIR Pub 117 (ISBN 1-932326-01-4; open PDF at clir.org).
- **Payne 2007** — *Library Storage Facilities and the Future of Print Collections in North America*, OCLC Programs and Research (open PDF at oclc.org).
- **Jackson 2004** — *Assessing ILL/DD Services: New Cost-Effective Alternatives*, ARL (ISBN 1-59407-657-X).
- **Anderson & Schooler 1991** — *Psychol. Sci.* 2(6):396–408. Crossref DOI: `10.1111/j.1467-9280.1991.tb00174.x`.
- **Wixted & Ebbesen 1991** — *Psychol. Sci.* 2(6):409–415. Crossref DOI: `10.1111/j.1467-9280.1991.tb00175.x`.
- **Cohen et al. 2013** — *PLoS ONE* 8(5):e63191. Crossref DOI: `10.1371/journal.pone.0063191`.
- **Heo et al. 2018** — *Proc. Natl. Acad. Sci. U.S.A.* Crossref DOI: `10.1073/pnas.1720956115`.
- **Karbowski 2019** — *J. Neurophysiol.* Crossref DOI: `10.1152/jn.00092.2019`.
- **Benna & Fusi 2016** — *Nat. Neurosci.* 19(12):1697–1706. Crossref DOI: `10.1038/nn.4401`.
- **Chardès et al. 2022** — *Proc. Natl. Acad. Sci. U.S.A.* Crossref DOI: `10.1073/pnas.2113512119`.
- **Ron-Harel et al. 2014** — *Gerontology*. Crossref DOI: `10.1159/000362502`.
- **Schnaack & Nourmohammad 2021** — *eLife* 10:e61346. Crossref DOI: `10.7554/eLife.61346`.
- **Roundy 1985** — *Manag. Sci.* 31(11):1416–1430. Crossref DOI: `10.1287/mnsc.31.11.1416`.
- **Willems 2008** — *Manuf. Serv. Oper. Manag.* 10(1):169–173. Crossref DOI: `10.1287/msom.1070.0176`.
- **Moncayo-Martínez et al. 2026** — *Data in Brief*. Crossref DOI: `10.1016/j.dib.2026.112991`.
- **Brynjolfsson, Hu & Smith 2003** — *Manag. Sci.* 49(11):1580–1596. Crossref DOI: `10.1287/mnsc.49.11.1580.20580`.
- **Hisano, Sornette & Mizuno 2011** — `arXiv:1101.5888` (open preprint).
- **Bartholdi & Hackman 2008** — *IIE Trans.* 40(11):1046–1053. Crossref DOI: `10.1080/07408170802167662`.
- **Wright & Bates 2010** — *Appl. Clin. Inform.* Crossref DOI: `10.4338/aci-2009-12-ra-0023`.
- **Walczyk et al. 2024** — *Hosp. Pharm.* Crossref DOI: `10.1177/00185787231214416`.
- **Garicano 2000** — *J. Polit. Econ.* 108(5):874–904. Crossref DOI: `10.1086/317671`.
- **Caliendo, Monte & Rossi-Hansberg 2015** — *J. Polit. Econ.* 123(4):809–852. Crossref DOI: `10.1086/681641`.
