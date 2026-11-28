# Fold-ins: five parent-child results read inside the swarm rule

*Friday 27 November 2026 (America/New_York). Part of `theory/swarm-2026-11-27/` (index: `INDEX.md` in this folder). Branched from `863a8a8bb3e0bb46c00a9236a9b4d5192c4b9d8d`. The swarm rule is a SYNTHESIS design (`measurement/CLAIM_MAP_v2.md`, row SWARM-RULE); the results below are each labelled for their own class and each has its own ledger row. `THEORY.md` is not edited; `CORE.md` is edited only at lines 98 and 120, where the swarm paragraph now points to ledger rows SWARM-MERGE and SWARM-REPRICE instead of restating their status. Checks: `checks/swarm27_checks.py`, section A. A self-check, not an independent review.*

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

Labels as in `theory/swarm/SWARM_RULE.md:7`: **PROVED (in-model)** follows inside its named class; **KNOWN** is published and credited, only for what that source states; **CONJECTURE** is a named bet; **OPEN** is not derived; an **OPEN MISS** is a miss with a diagnosis and a next step.

Notation is the swarm rule's (`theory/swarm/SWARM_RULE.md:21-36`): part \(i\) pays the share \(s_i\) of the read-and-follow price \(c\), has stake \(w_i\), and faces a whole with stake \(W\) whose signal changes at rate \(\lambda\). Write \(\kappa_i=s_iW/w_i\) for the part's **pricing ratio**: \(\kappa_i=1\) is clause 4's alignment \(s_i=w_i/W\), \(\kappa_i>1\) means the part pays more than its stake share, \(\kappa_i<1\) less.

## F1. CT17 (ii), the externality, is clause 4's mispricing at full share

**Statement (PROVED (in-model); CT12 class, `THEORY.md:336-338`).** In the read-rate class of CT12, a part that pays the share \(s_i\) of a read and bears stake \(w_i\) reads at \(\kappa_i^{-1/\alpha}\) times the whole's optimal rate. At \(s_i=1\) this is \((w_i/W)^{1/\alpha}\), which is CT17 (ii) (`THEORY.md:384`) with \(\Lambda_i=w_i\) and \(\Lambda_{\text{whole}}=W\). At \(s_i=w_i/W\) the ratio is 1.

*Proof.* CT12 gives the optimal interval \(T^*=[\alpha c'/((\alpha-1)w'q)]^{1/\alpha}\) for price \(c'\) and stake \(w'\). The part has \((c',w')=(s_ic,w_i)\), the whole \((c,W)\). The ratio of read rates is \(T^*_W/T^*_i=[(w_i/(s_ic))/(W/c)]^{1/\alpha}=\kappa_i^{-1/\alpha}\). ∎

So the under-watching of CT17 (ii) and the alignment rule of clause 4 are one statement: under-watching is \(\kappa_i>1\) with the read paid in full by the part, and it is cured exactly by the stake share. *Check:* `ct17ii_is_kappa_power`.

## F2. CT17 (i), one clock, gives every mismatched part a tamper motive

**Statement (PROVED (in-model); α = 2, CT17 (i) with CT13).** Let \(K\) parts track their own components, part \(i\) at read price \(c_i\), stake \(w_i\) and drift \(\sigma_i^2\), and let the whole enforce one shared clock \(T_1=\sqrt{2\sum c_i/\sum w_i\sigma_i^2}\) (CT17 (i), `THEORY.md:384`). Each part pays its own price in full and bears its own stake, so every part is aligned on its own component. Then part \(i\)'s enforcement-tamper gain against the shared clock (the swarm rule's \(D_i^{\text{enf}}\), `theory/swarm/SWARM_RULE.md:69`) is
\[
D_i=\sqrt{2c_iw_i\sigma_i^2}\,\Bigl[\tfrac12\bigl(k_i+k_i^{-1}\bigr)-1\Bigr]\ge0,\qquad k_i=T_1/T_i^*,\quad T_i^*=\sqrt{2c_i/(w_i\sigma_i^2)},
\]
zero iff \(c_i/(w_i\sigma_i^2)=\sum c_j/\sum w_j\sigma_j^2\), and \(\sum_iD_i\) equals CT17 (i)'s shared-clock penalty \(\sqrt{2\sum c_i\sum w_i\sigma_i^2}-\sum_i\sigma_i\sqrt{2c_iw_i}\).

*Proof.* \(D_i=J_i(T_1)-J_i(T_i^*)\) with \(J_i(T)=c_i/T+w_i\sigma_i^2T/2\); CT13 at α = 2 (`THEORY.md:344`) gives \(J_i(kT_i^*)/J_i(T_i^*)=(k+1/k)/2\), which is at least 1 with equality iff \(k=1\). Summing the definitions gives the penalty. ∎

Reading: a whole that imposes one schedule on parts whose own indices \(c_i/(w_i\sigma_i^2)\) differ creates a reason to tamper or leave in every part whose index differs, even when shares are right; the total motive is exactly what the single clock wastes. The design read off is CT17's: separate clocks unless the indices match. *Check:* `ct17i_one_clock_tamper_gains`.

## F3. CT19, reach, enters the stay clause as a latency-discounted signal worth

**Statement (PROVED (in-model); CT9 class, `THEORY.md:303-313`).** If every reading reaches part \(i\) after a latency \(\ell\) (in drift-time units), the part keeps reading and following iff
\[
\pi_i(\ell)=\frac{\lambda s_ic}{w_i\,\Phi_\ell}<1,\qquad \Phi_\ell=\int_\ell^\infty\bigl(r_\infty-r(u)\bigr)\,du ,
\]
and \(\Phi_\ell\) is nonincreasing in \(\ell\). In the swarm rule's telegraph class (\(r(u)=(1-e^{-2u})/2\), `theory/swarm/SWARM_RULE.md:115`), \(\Phi_\ell=e^{-2\ell}/4\), so a part at distance \(L\) from the whole, with signal speed \(v\) and \(\ell=\lambda L/v\), follows iff
\[
L<L_{\text{stay}}=\frac{v}{2\lambda}\ln\frac{1}{\pi_i(0)} .
\]

*Proof.* A reading of age \(u\) since arrival is \(\ell+u\) old at use, so the cost per unit stake is \(p/s+(1/s)\int_0^s r(\ell+u)\,du\) with \(p=\lambda s_ic/w_i\). CT9's argument (`THEORY.md:313`) applies to the shifted curve \(r_\ell(u)=r(\ell+u)\), which is nondecreasing by CT8 (`THEORY.md:305`) and bounded by \(r_\infty\): some \(s\) beats \(r_\infty\) iff \(p<\sup_s\int_0^s(r_\infty-r(\ell+u))\,du=\Phi_\ell\). The integrand is nonnegative, so \(\Phi_\ell\) is nonincreasing in \(\ell\). On the telegraph \(r_\infty-r(u)=e^{-2u}/2\); integrate, and solve \(\pi_i(0)e^{2\lambda L/v}<1\) for \(L\). ∎

CT19 (`THEORY.md:412`) bounds reach by a tolerable error; this is the same latency read through the part's own stay decision. Both say a part beyond reach leaves, and a faster-changing signal (larger \(\lambda\)) shortens reach. The reach here grows only logarithmically as the part's index falls. *Check:* `ct19_latency_stay_index` (CT9's condition re-tested with an optimizer on random draws, and the reach formula at \(0.999L\) and \(1.001L\)).

## F4. Lemma B3, drift direction, in the join clause

**Statement (PROVED (in-model); `THEORY.md:372`).** In CT14's class, shared drift lowers the join threshold and private drift raises it: \(\partial N^*/\partial q_g<0<\partial N^*/\partial q_u\). In swarm terms, a common driver makes a shared layer form with fewer parts; private churn among the parts delays it. No new proof: Lemma B3 is cited as stated. *Check:* `lemma_b3_drift_direction` (finite differences on CT14's \(N^*\), `THEORY.md:354`, for random \((a,b,q_g,q_u)\)).

## F5. Lemma B7, the √N fade, for a signal built from many parts

**Statement (KNOWN; linear readouts only; `THEORY.md:380`).** A shared signal fed by \(N\) independent deposits per step on a drifting target should forget faster by a factor \(\sqrt N\) at small drift-to-noise ratio: the steady-state gain is CT30's \(\lambda^*(\rho)\) with \(\rho=Nq/r\) (`THEORY.md:489`), and \(\lambda^*(\rho)\approx\sqrt\rho\) as \(\rho\to0\). The ant-like nonlinear readout failed in simulation (CLAIM_MAP K9, G15), so the swarm reading holds for linear readouts only. *Check:* `lemma_b7_sqrtN_fade`.

## CT16, the telling price

CT16 (`THEORY.md:366`) is used as stated for the join clause: telling \(N\) members at price \(d\) each beats all-local iff \(d/c<1/N^*(\rho)-1/N\). Its private-information form, a part that tells the whole what only it knows, is the new result of `TELLING_PRICE.md` in this folder.

## Still not derived

- F3 is derived for renewal reads with a fixed latency. Random latency, or latency that depends on the read schedule, is not treated.
- F2 is the α = 2 class. For other α the CT13 factor \([(α-1)/k+k^{α-1}]/α\) gives the same sign, but the closed form above is α = 2 only.
- F5 inherits Lemma B7's limit: no result for nonlinear readouts.
