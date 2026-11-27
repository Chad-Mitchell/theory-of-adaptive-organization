# The merge clause (CX2, CX3): what holds, and an open miss

*Friday 27 November 2026 (America/New_York). Part of `theory/swarm-2026-11-27/` (index: `INDEX.md`). Branched from `863a8a8bb3e0bb46c00a9236a9b4d5192c4b9d8d`. Clause 1's second sentence (`theory/SWARM_RULE_2026-11-23.md:42` at the branch point) read: "Self-interested parts merge into a new level iff the price-of-anarchy gap exceeds the coupling cost (CX2, CX3; CONJECTURE)." CX3 (`THEORY.md:580`) notes the inequality is a definition of the comparison until \(J_{\text{coupling}}\) and the boundary are specified. This note specifies them in one class, proves the clause in two readings, and shows the unqualified "iff" fails in two others. Checks: `checks/swarm27_checks.py`, section G. A self-check, not an independent review.*

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

Labels as in `FOLD_INS.md`.

## 1. The class (named MG)

CT29's shared-driver class at α = 2 (`THEORY.md:486`): \(N\) parties with stakes \(w_i\), \(W=\sum w_i\), track one driver; \(k=\sqrt{2cq}\). A party alone costs \(k\sqrt{w_i}\). A **merged** coalition \(S\) (one J for its members) costs
\[
c(S)=k\sqrt{W_S}+d\,|S|\quad(|S|\ge2),\qquad c(\{i\})=k\sqrt{w_i},
\]
with \(d\ge0\) the coupling cost per member (links, telling, upkeep of the shared layer). Two read regimes:
- **public reads**: a read by anyone helps everyone (CT29 as written); outside a merger parties play Nash, in which only the largest stake reads;
- **excludable reads**: a coalition's reads help only its members; outside a merger each party tracks alone.

The price-of-anarchy gap of the grand coalition is \(G=\sum_iJ_i(\text{no merger})-k\sqrt W\) and the coupling cost is \(J_{\text{coup}}=Nd\).

## 2. Results

**M1 (the clause as a statement about totals; PROVED, a restatement).** With transferable cost, there is a split of \(c(N)\) that leaves every party no worse off than without the merger iff \(G\ge J_{\text{coup}}\). *Proof.* Such a split exists iff \(c(N)\le\sum_iJ_i(\text{no merger})\). ∎ This is CX3's definition read in reverse; it says nothing about whether any member would rather leave a merger once formed.

**M2 (excludable reads: the clause holds for the grand coalition; PROVED (in-model)).** With excludable reads, the grand merger has a split that every member prefers both to staying out and to leaving (a member who leaves tracks alone, and the rest are unaffected) iff
\[
k\Bigl(\sum_i\sqrt{w_i}-\sqrt W\Bigr)\ge Nd ,
\]
that is \(G\ge J_{\text{coup}}\). For \(N\) equal stakes \(w\) this is \(d\le k\sqrt w\,(1-1/\sqrt N)\): merging needs \(N\ge(1-d/(k\sqrt w))^{-2}\). *Proof.* Without the merger each party tracks alone, so the no-merger cost and the leave payoff are both \(k\sqrt{w_i}\); apply M1. ∎ *Check:* `merge_private_reads_iff_gap` (LP feasibility on random instances, and the equal-stake boundary).

**M3 (public reads, no stake share above one half: no split of a merger is stable against a member leaving; PROVED (in-model)).** With public reads and every stake share at most \(\tfrac12\), for any \(d\ge0\) and any split of \(c(N)\), some member pays more than it would after leaving while the rest stay merged. So the clause's "iff" fails under public reads: with \(d=0\) the gap \(\tfrac k2(\sqrt a+W/\sqrt a)-k\sqrt W\) (\(a\) the largest stake) is positive whenever \(a<W\), which every such stake vector satisfies, yet no merger is stable.

*Proof.* If party \(i\) leaves and the rest (stake \(W-w_i\ge w_i\)) stay merged, CT29's Nash between the two has only the rest reading, at \(F=\sqrt{(W-w_i)q/(2c)}\), and \(i\) pays \(w_iq/(2F)=\tfrac k2\,w_i/\sqrt{W-w_i}\). With \(x_i=w_i/W\), the sum of these leave payoffs is \(\tfrac k2\sqrt W\sum_ix_i/\sqrt{1-x_i}\). The function \(x/\sqrt{1-x}\) is convex, so the sum is maximized at an extreme point of \(\{x:\sum x_i=1,\ 0\le x_i\le\tfrac12\}\), which has two shares at \(\tfrac12\); there it equals \(\sqrt2\). So the leave payoffs sum to at most \(k\sqrt W/\sqrt2<k\sqrt W\le c(N)\), and any split gives some member more than its leave payoff. ∎ *Check:* `merge_public_reads_never_stable` (random stake vectors against the bound \(1/\sqrt2\)).

This is the free-rider result for self-enforcing agreements on a public good (d'Aspremont et al. 1983; Carraro & Siniscalco 1993; Barrett 1994): the gain from merging is a public good to the members, and each prefers to let the others supply it.

**M4 (excludable reads: the gap does not make the merger stable against sub-coalitions; PROVED (in-model) by counterexample).** Stakes \((1,1,10^{-4})\), \(k=1\), \(d=0.05\): by hand, the gap \(G=2.01-\sqrt{2.0001}=0.5958\) exceeds \(J_{\text{coup}}=0.15\), so M2's condition holds, yet the core of \(c\) is empty. The coalition \(\{1,2\}\) with the third party alone costs \(\sqrt2+0.1+0.01=1.5242\), less than the grand merger's \(\sqrt{2.0001}+0.15=1.5642\): the small party adds more coupling cost than it saves. *Check:* `merge_gap_not_sufficient_for_core` (LP infeasible).

**M5 (stake-proportional shares are in the core iff a per-member condition holds; PROVED (in-model)).** With excludable reads, the split \(x_i=k\,w_i/\sqrt W+d\) (clause 4's stake shares of the grand merger's cost \(k\sqrt W\), that is, the member's stake share of the reads, \((k/2)w_i/\sqrt W\), plus its own tracking loss, \((k/2)w_i/\sqrt W\), plus its own coupling cost \(d\)) is in the core of \(c\) iff
\[
d\le k\,\min_i\sqrt{w_i}\Bigl(1-\sqrt{w_i/W}\Bigr).
\]
*Proof.* For \(|S|\ge2\): \(\sum_{i\in S}x_i=kW_S/\sqrt W+d|S|\le k\sqrt{W_S}+d|S|\) because \(W_S\le W\). For singletons: \(kw_i/\sqrt W+d\le k\sqrt{w_i}\) is the stated bound. The shares sum to \(c(N)\). ∎ Without coupling (\(d=0\)), \(k\sqrt{W_S}\) is a concave function of an additive measure, hence submodular, so the core is nonempty (Shapley 1971) and contains the stake shares; the coupling cost's step at \(|S|=2\) is what can empty it. *Check:* `merge_stake_shares_in_core_iff` (all coalitions, random instances).

## 3. Labels for clause 1's second sentence

| Reading | Label | Where |
|---|---|---|
| Totals, transferable cost | PROVED, a restatement (M1) | this note §2 |
| Excludable reads, grand coalition against leaving alone | PROVED (in-model) (M2) | §2 |
| Excludable reads, stability against every sub-coalition with stake shares | PROVED (in-model), with the per-member condition of M5 replacing the gap | §2 |
| Unqualified "merge iff gap exceeds coupling" | **OPEN MISS** (false as stated in class MG) | M3, M4 |

**Diagnosis of the open miss.** The clause compares one number (the gap) with another (the coupling cost) for the grand coalition. Two things it leaves out decide the outcome: whether the merger's gain can be withheld from a part that leaves (excludability: M2 against M3), and whether some smaller coalition does better (M4). **Next step.** Restate clause 1's second sentence with the excludability condition and the coalition-wise test (the core, or M5's per-member condition for stake shares), and pose the public-read case as an enforcement question: what punishment or exclusion rule (an outside enforcer, or repeated play) makes the merger self-enforcing. The restatement is made in `theory/SWARM_RULE_2026-11-23.md` clause 1; the enforcement question is an open row (SWARM-MERGE-ENFORCE), not derived.

## 4. Prior art (DOIs checked, `checks/crossref.out`)

d'Aspremont, Jacquemin, Gabszewicz & Weymark 1983, doi [10.2307/134972](https://doi.org/10.2307/134972) (internal and external stability); Carraro & Siniscalco 1993, doi [10.1016/0047-2727(93)90037-T](https://doi.org/10.1016/0047-2727(93)90037-T); Barrett 1994, doi [10.1093/oep/46.Supplement_1.878](https://doi.org/10.1093/oep/46.Supplement_1.878); Shapley 1971, doi [10.1007/BF01753431](https://doi.org/10.1007/BF01753431); Olson & Zeckhauser 1966, doi [10.2307/1927082](https://doi.org/10.2307/1927082) (the large member bears the burden in alliances, as in CT29's Nash). M2–M5 are these ideas in class MG; the class and the counterexample are worked here.

## 5. Not derived here

- The unqualified clause (OPEN MISS above).
- Coupling costs other than per-member (for example per link, \(d\binom{|S|}2\)), and external stability (whether outsiders want to join), are not worked out.
- A dominant-stake member (share above \(\tfrac12\)) can make a public-read merger stable against leaving: with \(d=0\), \(N=2\) and stakes \((0.9,0.1)\) the two leave payoffs sum to \(1.00139\,k\sqrt W\ge c(N)\) (counterexample from the review of #298). M3's hypothesis is needed; the dominant-stake case is not worked out.
- The level-creation reading ("each merger creates the next level", `THEORY.md:179`) stays a CONJECTURE.
