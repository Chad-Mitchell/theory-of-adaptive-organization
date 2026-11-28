# A part that can rewrite the whole's objective

*Friday 27 November 2026 (America/New_York). Part of `theory/swarm-2026-11-27/` (index: `INDEX.md`). Branched from `863a8a8bb3e0bb46c00a9236a9b4d5192c4b9d8d`. Answers part of the item "a part that changes the whole's own objective (moves \(W\) or the loss itself …; Carroll et al. 2024, arXiv 2405.17713) … OPEN" (`theory/swarm/SWARM_RULE.md:89` at the branch point). Checks: `checks/swarm27_checks.py`, section D. A self-check, not an independent review.*

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

Labels as in `FOLD_INS.md`.

## 1. The class (named OB)

The swarm rule's stay class (CT9 with renewal reads, `THEORY.md:311`; telegraph curve in the checks). The whole enforces the read interval that is optimal for the stake it **believes** it has:
\[
T_W(W')=\arg\min_T\Bigl[\frac{\lambda c}{T}+W'A(T)\Bigr],\qquad A(T)=\frac1T\int_0^Tr(u)\,du ,
\]
with \(T_W=\infty\) (no reads) when the whole's own index exceeds 1. The part's cost at interval \(T\) and share \(s\) is \(J_i(T;s)=\lambda sc/T+w_iA(T)\). The part can **rewrite** the whole's stake from its true value \(W_0\) to any \(W'>0\) (the simplest change to the whole's objective: it moves \(W\), not the curve \(r\)). Rewriting is free in this class; a cost of rewriting only lowers the gains below.

## 2. Results

**OB1 (fixed, aligned reference share: rewriting gains nothing; PROVED (in-model)).** If \(s_i=w_i/W_0\) is fixed against the true stake, then \(J_i(T;s_i)=(w_i/W_0)J_{W_0}(T)\), so the part's cost is minimized at \(T_W(W_0)\): no rewrite helps. ∎ *Check:* `objective_fixed_reference_no_gain`.

**OB2 (fixed, misaligned share: rewriting is the enforcement tamper by another route; PROVED (in-model)).** If \(s_i\) is fixed, the part's best rewrite is \(W'=w_i/s_i\), and its gain is exactly the enforcement-tamper gain \(D_i^{\text{enf}}\) of `theory/swarm/SWARM_RULE.md:69`.

*Proof.* \(J_i(T;s_i)=s_i\bigl[\lambda c/T+(w_i/s_i)A(T)\bigr]\), whose minimizer over \(T\) (including \(T=\infty\), leaving) is \(T_W(w_i/s_i)\) by definition. So rewriting to \(w_i/s_i\) makes the whole enforce the part's own preferred interval, and the gain \(J_i(T_W(W_0))-\min_TJ_i(T)\) is \(D_i^{\text{enf}}\). ∎ *Check:* `objective_misaligned_gain_equals_Denf`.

So a mispriced part that can move the whole's objective will move it to the stake at which its share would be aligned, \(W'=w_i/s_i\). The guard is clause 4 against the true stake: with \(s_i=w_i/W_0\), OB1 applies.

**OB3 (share indexed to the rewritable stake: pressure to inflate at every level; PROVED (in-model)).** If the share is recomputed from the stake the whole believes, \(s_i=w_i/W'\), the part's cost is
\[
J_i\bigl(T_W(W');w_i/W'\bigr)=w_i\,g\!\left(\lambda c/W'\right),\qquad g(p)=\min\Bigl(\min_T\bigl[p/T+A(T)\bigr],\ r_\infty\Bigr),
\]
which is strictly decreasing in \(W'\) wherever the whole reads, so the part gains from every inflation of the whole's stake and no finite inflation is a resting point. The total gain is bounded by \(w_ig(\lambda c/W_0)\), the part's whole cost, which falls toward \(w_ir(0)=0\) as \(W'\to\infty\).

*Proof.* With \(s_i=w_i/W'\), \(J_i(T;s_i)=(w_i/W')[\lambda c/T+W'A(T)]\), minimized over \(T\) by the whole's choice \(T_W(W')\), giving \(w_ig(\lambda c/W')\). \(g\) is a minimum of functions increasing in \(p\), with derivative \(1/T^*(p)>0\) where the inner minimum is below \(r_\infty\) (envelope theorem). ∎ *Check:* `objective_indexed_share_rewards_inflation`.

This is the swarm-rule form of reward tampering: a part paid by "your share of what the whole says it cares about" profits from making the whole say it cares more, because the share rule makes the whole carry the added reads.

## 3. Reading

The three results give one design statement: **fix the reference against which the part's share is set, and set it at the true stake**. A reference the part can move (OB3) is worse than a fixed wrong one (OB2): the fixed wrong one has a motive of \(D^{\text{enf}}\), second order in a small share error, while the moving one rewards inflation at every level, up to the part's whole cost.

## 4. Prior art

- Everitt, Hutter, Kumar & Krakovna 2021, *Synthese* 198:6435, doi [10.1007/s11229-021-03141-4](https://doi.org/10.1007/s11229-021-03141-4): reward tampering and the incentive to influence one's own reward signal, in causal influence diagrams. OB3 is an instance in the read-rate class.
- Carroll, Foote, Siththaranjan, Russell & Dragan 2024, "AI Alignment with Changing and Influenceable Reward Functions", arXiv 2405.17713 (no DOI; authors and title checked on the arXiv API): the choice of which reward to align to when it can change. That choice is the first item below.

## 5. Not derived here

- **Which benchmark.** When the part can change what the whole truly cares about (a real change in \(W\) or in \(r\), not a false belief), there is no fixed \(W_0\) to align to. Whether alignment should be measured against the whole's initial, current or some reflective objective is the question Carroll et al. 2024 raise; this cost has no term that prices it. OPEN.
- **Rewriting the loss curve itself** (moving \(r\), not \(W\)) is not treated. OPEN.
- **Costly or detectable rewriting.** With a cost or a detection chance per rewrite, the deterrence inequality of `theory/swarm/SWARM_RULE.md:85` (item 4) applies with \(D_i\) from OB2; for OB3 the motive is up to the part's whole cost \(w_ig(\lambda c/W_0)\), so a deterring fine must exceed that, unless the share index is fixed. Not worked out beyond that remark.
