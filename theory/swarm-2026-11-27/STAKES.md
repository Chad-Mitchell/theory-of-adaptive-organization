# Stake revelation: who pays what when stakes are private

*Friday 27 November 2026 (America/New_York). Part of `theory/swarm-2026-11-27/` (index: `INDEX.md`). Branched from `863a8a8bb3e0bb46c00a9236a9b4d5192c4b9d8d`. Clause 4 of the swarm rule (`theory/SWARM_RULE_2026-11-23.md:47`) sets cost shares in proportion to stakes, \(s_i=w_i/W\). That needs the stakes. This note asks what happens when each part knows only its own. Checks: `checks/swarm27_checks.py`, section C. A self-check, not an independent review.*

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

Labels as in `FOLD_INS.md`.

## 1. The class (named ST)

CT29's shared-read class (`THEORY.md:486`) at α = 2: \(N\) parties share one read rate \(F\) on a common target with drift \(q\); a read costs \(c\); party \(i\)'s tracking loss is \(w_iq/(2F)\). The joint cost \(J(F;W)=cF+Wq/(2F)\) is minimized at \(F^*(W)=\sqrt{Wq/(2c)}\) with value \(J^*(W)=k\sqrt W\), \(k=\sqrt{2cq}\). Each \(w_i\) is **private** to party \(i\). A mechanism asks for reports \(\hat w_i\), sets \(F=F^*(\hat W)\), and charges payments \(t_i\).

| Term | Meaning | Status |
|---|---|---|
| \(w_i\) | party \(i\)'s stake, known only to it | MEASUREMENT (private) |
| \(c, q\) | read price and drift, common knowledge | MEASUREMENT |
| \(x_i=w_i/W\) | stake share | derived |

## 2. Results

**ST0 (stake shares on reported stakes reward under-reporting; PROVED (in-model)).** If the whole asks for stakes and charges \(s_i=\hat w_i/\hat W\) of the reads at \(F=F^*(\hat W)\), party \(i\)'s cost is \(k(w_i+\hat w_i)/(2\sqrt{\hat W})\), whose derivative in \(\hat w_i\) at the truth is \((k/(2\sqrt W))(1-x_i)>0\). So every party with \(x_i<1\) gains by reporting less: clause 4 cannot be implemented by asking. *Proof.* At \(F^*(\hat W)\), \(cF=k\sqrt{\hat W}/2\) and \(q/(2F)=k/(2\sqrt{\hat W})\); differentiate. ∎ This is the CT17 (ii) externality of `FOLD_INS.md` F1, now created by a report. *Check:* `proportional_shares_reward_underreporting`.

**ST1 (the Clarke pivot is truthful; PROVED (in-model), KNOWN in form: Vickrey 1961, Clarke 1971, Groves 1973).** Charge
\[
t_i=cF+\frac{\hat W_{-i}\,q}{2F}-J^*(\hat W_{-i}),\qquad \hat W_{-i}=\sum_{j\neq i}\hat w_j .
\]
Then reporting \(\hat w_i=w_i\) is a dominant strategy for every party.

*Proof.* Party \(i\)'s total cost is \(w_iq/(2F)+t_i=J(F;w_i+\hat W_{-i})-J^*(\hat W_{-i})\). The second term does not depend on \(\hat w_i\), and the first is minimized over \(F\) at \(F^*(w_i+\hat W_{-i})\), which truthful reporting attains for any \(\hat W_{-i}\). ∎ *Check:* `clarke_truth_dominant`.

**ST2 (Clarke payments fall short of the read cost, by at most half the joint cost; PROVED (in-model)).** At truthful reports the whole must add
\[
\text{deficit}=cF^*-\sum_it_i=J^*(W)\Bigl[\sum_i\sqrt{1-x_i}-(N-1)\Bigr],
\]
which lies in \(\bigl[0,\ N\sqrt{1-1/N}-(N-1)\bigr]\), and the upper end is below \(\tfrac12\). The deficit is zero iff one party holds all the stake, and is largest at equal stakes (\(\sqrt2-1=0.41421\) of \(J^*\) at \(N=2\), rising toward \(\tfrac12\)).

*Proof.* At \(F^*\), \(cF^*=Wq/(2F^*)=J^*(W)/2\), so \(\sum_it_i=NJ^*/2+(N-1)J^*/2-k\sum_i\sqrt{W-w_i}\); subtract from \(J^*/2\). The bracket is concave in \(x\) on the simplex: its minimum is at a vertex (value \(N-1-(N-1)=0\)) and its maximum at the centre. Finally \(\sqrt{N(N-1)}<N-\tfrac12\) because \(N^2-N<N^2-N+\tfrac14\). ∎ *Check:* `clarke_deficit_bounds`.

**Clarke needs an outside subsidy of up to half the joint cost.**

**ST3 (Clarke is individually rational against tracking alone; PROVED (in-model)).** Party \(i\)'s truthful cost under Clarke is \(k\sqrt W-k\sqrt{W-w_i}\le k\sqrt{w_i}\), its cost of tracking alone, because \(\sqrt{a+b}\le\sqrt a+\sqrt b\). ∎

**ST4 (no truthful, efficient, budget-balanced mechanism; PROVED (in-model), an instance of Green & Laffont 1977 and Walker 1980).** No mechanism that sets \(F=F^*(\hat W)\), makes truth a dominant strategy, and has \(\sum_it_i=cF\) at every stake profile exists on an open domain of stakes.

*Proof.* On a smooth connected domain, every efficient mechanism with truth dominant is a Groves mechanism (Holmström 1979): \(t_i=cF+\hat W_{-i}q/(2F)-h_i(\hat w_{-i})\). At truthful reports \(\sum_it_i=(N-\tfrac12)J^*(W)-\sum_ih_i(w_{-i})\), so balance needs \(\sum_ih_i(w_{-i})=(N-1)k\sqrt W\). Apply \(\partial^N/\partial w_1\cdots\partial w_N\): the left side vanishes (each \(h_i\) misses one variable); the right side is \((N-1)k\,N!\binom{1/2}{N}W^{1/2-N}\neq0\). ∎ *Check:* `groves_no_budget_balance` (the mixed derivative is nonzero with sign \((-1)^{N+1}\) for \(N=2\) to 6, symbolic).

## 3. What this means for clause 4

Clause 4's \(s_i=w_i/W\) is the right cost share once stakes are known. With private stakes, asking for them and charging \(s_i=\hat w_i/\hat W\) is not truthful (ST0). The truthful repair is ST1, at the price of ST2's subsidy, and ST4 says no truthful efficient rule avoids some outside money. A whole that cannot subsidize must give up one of: truth as a dominant strategy, the optimal read rate, or balance.

## 4. Prior art (DOIs checked on Crossref, `checks/crossref.out`)

Vickrey 1961, doi [10.1111/j.1540-6261.1961.tb02789.x](https://doi.org/10.1111/j.1540-6261.1961.tb02789.x); Clarke 1971, doi [10.1007/BF01726210](https://doi.org/10.1007/BF01726210); Groves 1973, doi [10.2307/1914085](https://doi.org/10.2307/1914085); Green & Laffont 1977, doi [10.2307/1911219](https://doi.org/10.2307/1911219); Holmström 1979, doi [10.2307/1911954](https://doi.org/10.2307/1911954); Laffont & Maskin 1980, doi [10.2307/1912821](https://doi.org/10.2307/1912821) (the differential approach used in ST4's proof); Walker 1980, doi [10.2307/1912822](https://doi.org/10.2307/1912822); d'Aspremont & Gérard-Varet 1979, doi [10.1016/0047-2727(79)90043-4](https://doi.org/10.1016/0047-2727(79)90043-4); Mailath & Postlewaite 1990, doi [10.2307/2298018](https://doi.org/10.2307/2298018). ST1 and ST4 are these results in the read-rate class; ST0's derivative and ST2's closed form and bound are worked here.

## 5. Not derived here

- **Bayesian balance with the stay constraint.** With a common prior on stakes, the AGV mechanism (d'Aspremont & Gérard-Varet 1979) is truthful in Bayes–Nash equilibrium and balanced, but need not be individually rational against tracking alone; with many parties, Mailath & Postlewaite (1990) show the voluntary-participation version tends to fail. Whether a balanced Bayesian rule that every part prefers to staying alone exists in class ST, for which priors, is OPEN (a CONJECTURE row is not added: no bet is made either way).
- **Stakes that change over time**, so that the report is repeated, are OPEN.
- **Other α.** ST1 and ST3 hold for any convex read cost (the proofs use only optimality and subadditivity of \(J^*\), which is concave with \(J^*(0)=0\)); ST0's derivative, ST2's closed form and ST4's derivative are α = 2.
