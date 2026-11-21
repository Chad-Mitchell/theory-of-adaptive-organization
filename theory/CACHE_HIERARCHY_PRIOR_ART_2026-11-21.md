# CPU memory hierarchies: prior-art verdict, and why no test was locked (21 November 2026)

*Saturday 21 November 2026, about 8:45 AM ET (America/New_York), beside `main` `a65b64e` and PR #133 (`theory/REVEALED_PRICES_2026-11-21.md`). Not a prereg, not a lock, not a result. No scored data were compiled. The hypothesis sentence is unchanged: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." DOIs below were resolved on Crossref this session; abstracts were read through OpenAlex; the full papers were not read.*

## 1. The idea

Engineered memory hierarchies look like an ideal field for the revealed-price route of PR #133: market competition is strong selection, the world (programs' reuse patterns) is measured as miss-rate-versus-size curves, and the stakes (main-memory latency in core cycles) rose for decades (the "memory wall"). Proposed prediction family: the number of cache levels K\* and the size ratios between levels, as functions of the stakes R = miss penalty / per-level upkeep, given measured miss-rate curves. Rivals: fixed depth; level count tracking transistor budget; and the textbook analytic models.

## 2. Verdict: not distinctive. GTAO's prediction here is the 1974–1996 storage-hierarchy theory

The search for "optimal number of cache levels" found that every part of the prediction GTAO would make in this domain was derived, in this domain, decades ago, from the same kind of cost model (hit-ratio function × technology cost function, minimized):

| GTAO result as it would apply to caches | Prior art (same domain, same form) |
|---|---|
| K\* grows linearly in the log of the scale range (T20 part A, passed 12/12 in-model) | **Chow 1974**, *IBM J. Res. Dev.* 18:194, doi 10.1147/rd.183.0194: "The optimal number of storage levels in a hierarchy is shown to be directly proportional to the logarithm of the systems capacity." **Chow 1976**, *IEEE Trans. Comput.* C-25:157, doi 10.1109/tc.1976.5009230: increases "linearly with the logarithm of the ratio of the required hierarchy capacity and the cache capacity." |
| Geometric spacing of layers under a scale-free world (T7b) | Chow 1974: "The optimal cost ratio of adjacent storage levels is constant, as are the ratios of the device access times and storage capacities of the adjacent levels." Both inputs are power laws, exactly the scale-free case. |
| Fixed cost shares at the optimum, in any currency (CT24) | **Welch 1978**, *IEEE Trans. Comput.* C-27:408, doi 10.1109/tc.1978.1675120: "each memory unit makes the same percentage contribution to memory system cost as it makes to average system access delay." **Jacob, Chen, Silverman & Mudge 1996**, *IEEE Trans. Comput.* 45:1180, doi 10.1109/12.543711 (comment: 46:1151, doi 10.1109/12.628401): closed-form optimal size of each level; "money spent on an n level hierarchy is spent in a fixed proportion until another level is added." |
| A layer's design is set by what the layer above passes down (CT34 linking) | **Przybylski, Horowitz & Hennessy 1989**, ISCA, doi 10.1145/74925.74939: the first-level cache changes the optimal second-level design (size up, cycle time less important). |
| The world enters through its measured law (structure function / exponent α) | **Mattson, Gecsei, Slutz & Traiger 1970**, *IBM Syst. J.* 9:78, doi 10.1147/sj.92.0078 (stack-distance curves: all sizes from one trace). **Hartstein, Srinivasan, Puzak & Emma 2006**, Computing Frontiers, doi 10.1145/1128022.1128064: the miss rate falls as a power law in cache size, exponent −0.3 to −0.7, "directly related to the time dependence of cache references." |

None of these papers is credited anywhere in the repository (grep of all `.md` files for Chow, Welch, Jacob, Przybylski, Mattson, Hartstein, stack distance, miss rate: no hit outside unrelated "Welch spectrum" uses).

**Consequence under R3 (PR #133 §2).** In a cache hierarchy J with power-law hit and technology functions *is* Chow's geometric program. Fitted the same way on the same fit set, GTAO and Chow/Jacob give the same held-out K\* and the same size ratios. A pass would support the storage-hierarchy theory, which is already verified against exhaustive simulation (Jacob et al. 1996: within 5% of optimal in all but one case), not this theory. So, per the brief, **no prereg was written and nothing was locked.**

Additional practical problems, recorded so they need not be rediscovered: level count is nearly collinear in time with both stakes and transistor budget (the two named rivals), and DRAM latency in cycles flattened after clock rates stalled (mid-2000s) while level count stayed at about three, so the usable variation is a handful of steps in a few decades. Public sources exist (Cantin & Hill's SPEC CPU2000 miss-rate data at research.cs.wisc.edu, reachable today; measured per-chip latencies at 7-cpu.com; cache configurations on Wikipedia), so data was not the blocker; distinctiveness was.

## 3. What this does show (plain meaning)

1. **An independent derivation, not a test.** A field with strong selection and measured prices, working with no knowledge of GTAO, arrived at GTAO's layer-count, spacing and cost-share results by minimizing a cost of the same shape. That is consistent with J being the right objective for engineered memory, and it is evidence that these GTAO results are **novelty 0–1** (stated before, same domain or same form), not new.
2. **Prior art to credit.** T20 part A, T7b and CT24 should cite Chow 1974/1976, Welch 1978 and Jacob et al. 1996 before any public novelty claim. `litmap/PRIOR_ART.md` gains a row below.
3. **Where any distinct content in this domain would have to be.** Only in terms the storage-hierarchy models lack: the ruin cap (a tail-latency constraint P(stall > x) ≤ ε, CT18/§(iv)), chosen read rates substituting for layers (prefetching; THEORY B.9's counterexample says K\* need not rise with stakes then), and pooling across agents (shared versus private last-level caches). Each of these also has its own engineering literature (not surveyed here); a targeted search must come before any prereg. None is proposed here.
4. **Lesson for the search.** The engineered domains where J is cleanest are the ones where the optimizer was written down long ago. There, GTAO's claim reduces to the local optimizer and R3 fails by construction. A distinctive test needs a system where the law predicts something the local engineering model does not: a cross-scale relation (one shared technology over several layers, PR #133 §3.2), the ruin cap, or the selection gradient (PR #133 §4).

## 4. Usage

Shared weekly usage at writing: 66.7% (limit resets Friday 27 Nov, 6:56 AM ET).
