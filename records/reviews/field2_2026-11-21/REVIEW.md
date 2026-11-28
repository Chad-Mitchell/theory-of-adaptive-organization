# Independent hostile review: PR #136 (Field-2 feasibility; no lock)

**Reviewer:** independent (wrote none of PR #136 or `theory/FIELD2_FEASIBILITY_2026-11-21.md`). Same bot family, not a blind second executor.
**Date:** Saturday 21 November 2026, 10:15 AM EST (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/136 (branch `field2-feasibility-2026-11-21`, pre-fix head `c4f798a`).
**Clone:** fresh `/workspace/rev136` (nothing merged; `/workspace/looper` and `/workspace/gtao-evo` untouched; compute at nice 19).

**Verdict: READY-WITH-FIXES**

The note is a Pass 0 scouting memo, not a prereg. It compiles a silicon cache-anchor $\gamma$ from the two five-minute-rule papers, inventories seven non-silicon fields, correctly withholds a lock, and correctly names research-library print tiers as the strongest non-silicon candidate *conditional* on a Pass 1 $\theta$ check. The Zipf-to-miss-curve gate is stated the right way: for $\alpha_{\text{rank}}<1$, $m(s)\approx 1-(s/N)^{1-\alpha}$, which is not scale-free $m(s)\sim s^{-\theta}$ with $\theta>0$, and published static circulation counts do not supply an LRU/stack-distance curve. All 33 cited DOIs resolve (31 on Crossref, 2 on DataCite: Zenodo `10.5281/zenodo.7799609`, OSF `10.17605/osf.io/cq987`). `CORE.md` and `THEORY.md` are byte-identical to `origin/main` (`cd84095`). The hypothesis sentence is unchanged. `tools/check_consistency.py` and `tools/check_open_work.py` both PASS. Nothing is locked or scored.

The bottom line survives: **0 fields are ready to lock**. Four should-fixes belong in this PR before merge. None of them creates a lockable field or withdraws the library-first recommendation, but two of them change reported numbers (cache $\gamma$ at the third decimal; OhioLINK $\alpha_{\text{rank}}$ from 0.56 to $\approx 0.91$), and the library $\gamma$ must be labeled as depending on an assumed open-stack retrieval time.

- **S1 (Inconsistent HDD price in the Appuswamy 2018 three-point $\gamma$ fit).** §1.1 Table 6 lists HDD at **$50 / $0.025/GB** (and correctly notes Table 1's $49). The pairwise DRAM–HDD fit $\gamma=\mathbf{0.4897}$ uses those Table 6 figures and recomputes exactly. The three-point DRAM–SATA–HDD fit $\gamma=\mathbf{0.4925}$ ($R^2=0.9982$) and its 50 µs / 100 µs sensitivities ($0.4844/0.9711$, $0.4728/0.9418$) instead use Table 1's $49/$0.0245/GB (reproduced to four digits). With the tabulated Table 6 cost $0.025/GB$ held fixed, the three-point OLS is $\gamma=\mathbf{0.4905}$ ($R^2=0.9984$), sensitivity $0.4826$ ($R^2=0.9717$) at 50 µs and $0.4711$ ($R^2=0.9426$) at 100 µs. Recompute and report one price consistently. The cache band $\gamma\in[0.34,0.49]$ and the §1.2 Chow ratios at $\gamma=0.490$ are unaffected.

- **S2 (OhioLINK "implied $\alpha_{\text{rank}}\approx 0.56$" does not follow from the cited 7.2%/80% statistic).** O'Neill & Gammon 2014, p. 801, states that 7.2% of manifestations accounted for 80% of circulation (Table 6, p. 802, is the multiuse share that completes the 11.4/72.9/8.5/7.2 partition of 6,660,250 manifestations; Figure 3 is a lin-log rank plot and reports no fitted exponent). Under the note's own finite-catalog formula $H(s)=(s/N)^{1-\alpha}$, $0.072^{1-\alpha}=0.80$ gives $\alpha_{\text{rank}}\approx 0.91$, not 0.56. The value is still $<1$, so the scale-free gate still fails and the Pass 1 recommendation stands. Also, the 11.4% non-circulating share belongs to Table 6 p. 802, not Table 3 p. 796 (Table 3 does carry the ARL $7.45$–$7.47$M / $0.144$/yr and depository $4.18$M / $0.025$/yr figures).

- **S3 (Library $\gamma$ is not fully measured: $t_{\text{open}}$ is assumed, and Courant's \$/vol/yr includes circulation).** The quoted $\gamma=0.322$ at "10 min open stack vs. 24 h depository" recomputes exactly from Courant & Nielsen 2010 Table 1 ($4.26$ vs $0.86$) and Payne's 24 h courier, and $\gamma=0.289$ matches Table 2's no-construction-inflation pair ($2.52$ vs $0.60$). But neither Courant nor Payne measures an open-stack retrieval time; 10 min is an assumption (5 min $\to 0.283$, 15 min $\to 0.351$ on the inflated pair, which is where the $0.28$–$0.35$ band comes from). Payne p. 10 says delivery is "*typically* within 24 hours," not "$\le 24$ h." Separately, Courant's $4.26$ and $0.86$ are perpetual annual averages of a six-element cost that **includes circulation** (Table 1 NPV: open stacks $4.58$, high-density $9.45$), whereas §3.1 item 2 describes $\gamma$ as coming from "building construction, utilities, and staffing." Label $t_{\text{open}}$ as assumed, quote Payne accurately, and disclose the circulation component (or report a no-circulation sensitivity). Do not call library $\gamma$ unconditionally "measured" or "ready" until those qualifications are in the table.

- **S4 (Wrong qualification cite; uncited Huddersfield).** Kill-condition K2 points to `CORE.md` §3 for selection-strength qualification. `CORE.md` §3 is the hypothesis earning/killing paragraph. The five-item operational checklist ($\sigma$, $N_e$, $\varepsilon=10/(\sigma N_e)$, rival excluded, $T_{\text{red}}$) is `THEORY.md` §3 (lines 45–51); `CORE.md` §2 already points there, and the CORE load-bearing table cites "THEORY §3, FRAMEWORK §9." The Pass 0 selection caveat itself is appropriately stated (libraries: weak cost-management incentives; nothing locked), but the cite must be `THEORY.md` §3. Lawrence et al. 2001 p. 542 documents weak *cost-management* incentives, not a recorded $\sigma,N_e$ qualification; say so. Also, "Huddersfield" in the §3.1 honesty gate has no source in the registry (Burrell 1980/85 are already cited for the negative binomial; the log-normal reading is a different, uncited dataset). Drop it or add a verified source. Gray & Graefe 1997 Table 8 is on MSR-TR-97-33 **p. 7**, not p. 6. Jackson 2004 is **$18.35$ and $15.6$ calendar days** (research-library borrowing), not "15.6–16 days."

**Nits:**
- Hashimoto 2024 (`10.17605/osf.io/cq987`) is a conference abstract (口演抄録), not a journal article; CCDF slopes $\approx-1.63$ (five-year) and $\approx-2$ (annual) and the conversion $\alpha_{\text{rank}}=1/\mu\in[0.50,0.61]$ are correct.
- Sandler 2012 is in the §4 registry but is not used in the body.
- Bulick 1978 "direct fit $\alpha_{\text{rank}}\approx 0.26$" is the unweighted OLS on the 15 frequency-class points in Table 1 (end-rank $\alpha=0.25$, $R^2=0.88$); an item-level fit on all 107,152 volumes is $\approx 0.55$, and coverage-implied $\alpha$ rises from $\sim 0.22$ in the head to $\sim 0.59$ in the tail. All of these are $<1$. State the estimator.
- SATA-SSD latency as $1/\text{IOPS}$ is already disclosed, with a 50/100 µs sensitivity; keep it.
- Reilly 2003 Appendix 4 really does list eight depositories at $\$0.17$–$\$2.38$/vol/yr (NRLF–CONStor), p. 44.
- The $3.7\times 10^3$ ATP/min/PSD figure was not found in the open Cohen et al. 2013 text (the $t_{1/2}=3.67$ d is Cohen's median over 191 synaptic proteins). Likely from Karbowski 2019, which was not opened (no paywall login). Attribute it or qualify.

---

## 1. Cache-anchor tables and $\gamma$ refits (nice 19)

Opened the public PDFs (no accounts): Gray & Graefe, MSR-TR-97-33 / Berkeley and CMU mirrors; Appuswamy et al., author PDF and the CACM paginated copy (pp. 114–120).

**Gray & Graefe 1997, Table 8** ("Performance Metrics of high-performance devices circa 1997"), MSR-TR-97-33 **PDF page 7**: RAM 1 GB, $\$15{,}000$, $\$15{,}000$/GB, $0.1$ µs; Disk 9 GB, $\$2{,}000$, $\$222$/GB, 10 ms; Tape robot $14\times 35$ GB, $\$10{,}000$, $\$20$/GB, 30 s. All tabulated figures match the note (490 GB and $\$20$/GB are $14\times 35$ and $10{,}000/490$ rounded as in the paper).

OLS on $(\ln t,\ln c)$ with $c\propto t^{-\gamma}$, using the tabulated $\$222$/GB:

- $\gamma=0.341028$, $R^2=0.997205$; pairwise RAM–Disk $0.365948$, Disk–Tape $0.300629$. Matches the note's $0.3410$, $0.9972$, $0.3659$, $0.3006$.

**Appuswamy et al. 2019, CACM pp. 116–118:** Table 1 (p. 116) DRAM 2018 $\$80$/16 GB / $\$0.005$/MB, SATA SSD $\$415$/800 GB / 67k read IOPS, HDD $\$49$/2 TB; Table 4 (p. 117) Intel 750 800 GB $\$589$ / 460k IOPS, Optane P4800X 480 GB $\$617$ / 550k IOPS; text p. 117 "tens of µs" end-to-end for PCIe 3D XPoint; Table 5 (p. 118) SpectraLogic T50e, 10 slots, 15 TB, library cost $\$11{,}000$, access latency 65 s; Table 6 (p. 118) DRAM 16 GB $\$80$, 100 ns; HDD 2 TB **$\$50$**, 5 ms; Tape $10\times 15$ TB, $\$11{,}000$, 65 s. Compiled $/GB$ values $5.00$, $1.285$, $0.736$, $0.519$, $0.025$, $0.0733$ all recompute from those unit prices. The tape-vs-HDD monotonicity note is correct at the 10-slot starter capacity.

Refits:

- DRAM–HDD, Table 6 $\$5.00$ vs $\$0.025$, $100$ ns vs $5$ ms: $\gamma=0.489688$ (note $0.4897$). Exact.
- DRAM–SATA–HDD with $t_{\text{SSD}}=1/67{,}000$ s and $c_{\text{SSD}}=415/800$, **but $c_{\text{HDD}}=\$0.0245$ (Table 1 $49$)**: $\gamma=0.492450$, $R^2=0.998228$; 50 µs $0.484376$ / $0.9711$; 100 µs $0.472762$ / $0.9418$. This is the note's $0.4925/0.9982/0.4844/0.9711/0.4728/0.9418$ (S1).
- Same three points with tabulated Table 6 $c_{\text{HDD}}=\$0.025$: $\gamma=0.49054$, $R^2=0.99838$; 50 µs $0.48262$ / $0.9717$; 100 µs $0.47111$ / $0.9426$.

Chow fixed-point ratios at $\gamma=0.341$ and $\gamma=0.490$ with $\theta\in[0.3,0.7]$ recompute to the stated ranges (the $r_t$ floor $16.0$ is $15.95$ rounded; $q=6.81$ is from $0.4897$, not $0.490$). $\theta\gamma\in[0.102,0.343]<1$ holds.

Hartstein et al. 2006 $\theta\approx 0.3$–$0.7$ was already source-checked in the PR #135 review; the DOI resolves.

---

## 2. Zipf $\leftrightarrow$ miss-curve reasoning

The note's claim is right, and it is the same qualification applied to Breslau et al. 1999 in PR #135 (S4).

Under an independent-reference model with rank-frequency $p(r)\propto r^{-\alpha}$ on a catalog of $N$ items, the optimal (or IRM-LRU) hit rate from caching the top $s$ items is $H(s)=\sum_{i=1}^{s}i^{-\alpha}/\sum_{i=1}^{N}i^{-\alpha}$.

- If $\alpha>1$, the infinite-catalog tail gives miss rate $m(s)\sim s^{-(\alpha-1)}=s^{-\theta}$ with $\theta=\alpha-1>0$. Scale-free, $N$-independent at large $s$.
- If $\alpha<1$, $\sum_{i=1}^{n}i^{-\alpha}\approx n^{1-\alpha}/(1-\alpha)$, so $H(s)\approx(s/N)^{1-\alpha}$ and $m(s)\approx 1-(s/N)^{1-\alpha}$. Finite-catalog, not $s^{-\theta}$.

Published library circulation studies report static (annual or cumulative) use-by-title, i.e. a rank-use or frequency-of-frequencies curve, not an LRU stack-distance miss curve. With $\alpha_{\text{rank}}<1$ on those static curves, they do **not** give a scale-free $m(s)$. Temporal locality could still produce $\theta>0$ on a transaction log; that is correctly left to Pass 1. The formula $m(s)\approx 1-(s/N)^{1-\alpha}$ is the right IRM conversion.

Static $\alpha$ checks (open PDFs):

- **Bulick 1978**, Table 1, Hillman / Pitt, $N=107{,}152$, $210{,}717$ transactions: frequency-class unweighted log-log slope $\approx 0.25$–$0.27$ (note $0.26$); item-level $\approx 0.55$. Both $<1$. Bradford–Zipf in the paper is a semi-log cumulative law, not a reported Zipf $\alpha$.
- **O'Neill & Gammon 2014**: $28{,}475{,}701$ items, $6{,}660{,}250$ manifestations; 7.2% of manifestations $\to$ 80% of circulation (p. 801); implied IRM $\alpha\approx 0.91$ (S2), still $<1$. OhioLINK pickup "in 2–3" days is in the paper (p. 792). Table 3 p. 796: ARL $7{,}445{,}927$ or $7{,}466{,}865$ items at $0.144$/yr; depositories $4{,}181{,}392$ at $0.025$/yr.
- **Hashimoto 2024** abstract: CCDF slopes $\approx-1.63$ (five-year) and $\approx-2$ (annual); $\alpha_{\text{rank}}=1/\mu\in[0.50,0.61]$. Correct conversion; conference abstract, not a journal article.
- **Burrell 1980/85** DOIs resolve to the negative-binomial / 80/20 papers as cited.

So it is correct that the published circulation evidence checked here does not establish scale-free $m(s)\sim s^{-\theta}$.

---

## 3. Library $\gamma$, ladder, and selection

Opened CLIR Pub 147 (Courant & Nielsen 2010, including the Zenodo-registered volume), Payne 2007 (OCLC), Reilly 2003 (CLIR Pub 117), O'Neill & Gammon 2014, Lawrence et al. 2001, and the Jackson 2004 ARL text (Internet Archive).

- Courant & Nielsen 2010, Table 1 p. 91: open stacks annual average **$\$4.26$/vol/yr**, high-density **$\$0.86$**; Table 2 p. 96 no-construction-increase **$\$2.52$ vs $\$0.60$**. These are perpetual annual averages of a six-element NPV (construction, maintenance, cleaning, electricity, staffing, **circulation**).
- Payne 2007 p. 8 and Tables 1–2 pp. 12–13: 68 North American high-density facilities, over 70 million volumes, $\sim$7% of one billion academic volumes. P. 10: courier or van delivery, "*typically* within 24 hours of the request."
- Reilly 2003, Appendix 4 p. 44: eight repositories, operating cost $\$0.17$ (NRLF) to $\$2.38$ (CONStor) per volume per year.
- Jackson 2004: research libraries **$\$18.35$** per borrowing transaction, **$15.6$ calendar days** average borrowing turnaround. The note's "15.6–16 days" adds an uncited extra day. OhioLINK 2–3 days is from O'Neill & Gammon, not Jackson.
- $\gamma=-\ln(0.86/4.26)/\ln(24\,\text{h}/10\,\text{min})=0.32196$ (note $0.322$); no-inflation $0.28876$ (note $0.289$). The $0.28$–$0.35$ band is the 5–15 min window on the inflated pair, not a measured latency range.

Independence of the three legs (cost accounting vs circulation logs vs no Chow geometric program) is fairly stated; Cooper 1989 as a two-tier cutoff is a reasonable contrast. Selection: Lawrence et al. 2001 p. 542 is about weak *costing systems* and being "content if some reasonable level of service is accomplished within budgetary targets." That is a fair Pass 0 caution, not a `THEORY.md` §3 qualification record. K2 correctly says a miss on libraries must record qualification rather than over-claim against strongly selected systems — once the cite is repaired (S4).

---

## 4. Other fields (spot-checks)

DOIs for all rows resolve. Spot-checks on open texts:

- **Brynjolfsson, Hu & Smith 2003** (open PDF): $\log\text{Quantity}=10.526-0.871\log\text{Rank}$. $\alpha_{\text{rank}}=0.871<1$. Exact.
- **Hisano, Sornette & Mizuno 2011** (arXiv:1101.5888): Table of $\mu(\text{MLE})$ $1.35, 1.5, 1.6, 1.8$ ($\pm 0.1$). $\alpha_{\text{rank}}=1/\mu\in[0.56,0.74]$. Exact.
- **Roundy 1985, Willems 2008, Moncayo-Martínez et al. 2026, Bartholdi & Hackman 2008, Garicano 2000, Caliendo et al. 2015, Benna & Fusi 2016, Anderson & Schooler 1991, Wixted & Ebbesen 1991:** Crossref metadata matches the registry (Moncayo-Martínez is issued August 2026, *Data in Brief*). I did not reopen those full texts in this session; several were source-checked in the PR #135 review (Roundy, Benna & Fusi, Anderson & Schooler). The qualitative verdicts (missing $\theta$ and/or $\gamma$, or Chow/Roundy-style design) are consistent with that earlier inventory.
- **Cohen et al. 2013** (open): median synaptic-protein $t_{1/2}=3.67$ d (mean $4.14$ d, $n=191$). The $3.7\times 10^3$ ATP/min/PSD figure is not in that paper's text.
- **Wright & Bates 2010, Walczyk et al. 2024, Karbowski 2019, NARA/GAO-13-668 / 2025 FRC Toolkit:** not opened this session (no paywall logins; Wright's Thieme PDF was not served). I therefore did not independently confirm $442{,}658$ orders / top $11.8\%$ / 321 ADCs / the FRC fee and 18-facility counts. Those cells are not load-bearing for the "library first, nothing locked" recommendation; they should be treated as unchecked rather than wrong.

---

## 5. Consistency, lock status, and hypothesis sentence

- Diff vs `origin/main` (`cd84095`): **only** `theory/FIELD2_FEASIBILITY_2026-11-21.md` (144 lines added). `CORE.md` and `THEORY.md` are unchanged (empty diff).
- Hypothesis sentence, verbatim: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." Present unchanged in `CORE.md:24`, `THEORY.md:41`, and the note's preamble.
- The note's preamble and §3.2 header state **Pass 0 / not a prereg / nothing locked / no scored test / do NOT lock yet.** No preregistration hash, no scored prediction, no CLAIM_MAP row. Criterion 4 and K2 discuss selection without completing the five-item checklist, which is the right scope for a feasibility note.
- `python3 tools/check_consistency.py`: **PASS** (0 FAIL).
- `python3 tools/check_open_work.py`: **PASS** (0 missing).

---

## 6. What would change the verdict to NOT READY

A lock, a scored test, a silently changed hypothesis sentence, a claim that library $\theta>0$ is already measured, or a claim that library $\gamma$ is a fully measured two-tier exponent with no assumed $t_{\text{open}}$, would be NOT READY. None of those is present. After S1–S4 the note remains a honest Pass 0 map of where a Field-2 test could be built.
