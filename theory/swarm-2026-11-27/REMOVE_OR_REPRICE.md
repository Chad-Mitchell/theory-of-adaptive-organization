# Remove or reprice under the ruin cap (T53, clause 7)

*Friday 27 November 2026 (America/New_York). Part of `theory/swarm-2026-11-27/` (index: `INDEX.md`). Branched from `863a8a8bb3e0bb46c00a9236a9b4d5192c4b9d8d`. Clause 7 (`theory/swarm/SWARM_RULE.md:50` at the branch point) was a CONJECTURE whose inequality "is written, not derived" (T53; ledger row SWARM-REPRICE). This note derives it in a named class. Checks: `checks/swarm27_checks.py`, section F. A self-check, not an independent review.*

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

Labels as in `FOLD_INS.md`.

## 1. The class (named RR)

A part has left (its index is above 1). The whole has a finite menu of responses \(o\), each with a transition time \(\tau_o\) (fixed or random) and a cost \(C_o\) to the whole (what it pays to carry out \(o\) and what it loses afterwards, for example the loss of an entangled part on removal). During the transition the whole is exposed to ruin at hazard \(h_o(t)\): ruin is the first event of a point process with that intensity, independent of the transition time given the option. After the transition, ruin exposure is the same for every option (or is folded into \(C_o\)). The menu used for clause 7 is

| option | transition | hazard during it | cost |
|---|---|---|---|
| remove | \(\tau_R\) | \(h_R\) | \(L_R\): what the whole loses without the part |
| reprice | \(\tau_P\) | \(h_P\) | \(C_P\): the cost of moving the part's index below 1 (clause 5) |
| cut, then remove | \(\tau_R\) | \(h_X\le h_R\) | \(L_R+K_X\) |
| cut, then reprice | \(\tau_P\) | \(h_X\le h_P\) | \(C_P+K_X\) |

with \(K_X\ge0\) the cost of cutting the exposure first. The whole's ruin cap is \(P(\text{ruin})\le\varepsilon\) (`theory/swarm/SWARM_RULE.md:23`). Hazards, times and costs are MEASUREMENTS.

## 2. Results

**RR1 (ruin during a transition; PROVED (in-model), elementary).** For a fixed transition time \(\tau\),
\[
P(\text{ruin during }o)=1-\exp\Bigl(-\int_0^{\tau}h_o(t)\,dt\Bigr),
\]
so option \(o\) meets the cap iff \(\int_0^{\tau_o}h_o\,dt\le\ln\frac1{1-\varepsilon}=\varepsilon+\tfrac{\varepsilon^2}2+O(\varepsilon^3)\). For a constant hazard \(H\) this is \(H\tau\le\ln\frac1{1-\varepsilon}\). If instead the transition time is exponential with rate \(\mu\) and the hazard is constant, \(P=H/(H+\mu)\), and the cap reads \(H/\mu\le\varepsilon/(1-\varepsilon)\). For any random transition time \(T\), \(P=\mathbb E[1-e^{-HT}]\le1-e^{-H\mathbb ET}\) (Jensen), so a random duration with the same mean is never worse than a fixed one.

*Proof.* The survival function of a point process with intensity \(h\) is \(\exp(-\int h)\); average over \(T\) for the random case, and \(\int_0^\infty\mu e^{-\mu t}(1-e^{-Ht})\,dt=H/(H+\mu)\). Concavity of \(1-e^{-Ht}\) gives the last claim. ∎ *Checks:* `ruin_during_transition_formulas` (Monte Carlo, fixed, exponential and time-varying hazards), `cap_threshold_vs_written_form`.

So clause 7's written threshold "\(H\tau_{\text{rep}}>\varepsilon\)" is the first-order form of the exact one, \(H\tau_{\text{rep}}>\ln\frac1{1-\varepsilon}\); the relative difference is \(\varepsilon/2\) to first order (by hand: 0.0536 at \(\varepsilon=0.1\)), and the written form is the stricter of the two.

**RR2 (the remove-or-reprice rule; PROVED (in-model), ELEMENTARY).** The whole's cost-minimizing response under its cap is
\[
o^*=\arg\min\{C_o:\ \textstyle\int_0^{\tau_o}h_o\,dt\le\ln\frac1{1-\varepsilon}\},
\]
and if no option is feasible the menu cannot meet the cap. In the menu above this reads as clause 7:
1. If both remove and reprice meet the cap, remove when \(L_R<C_P\) (a part the whole can lose cheaply) and reprice when \(C_P<L_R\) (an entangled part). A cut option cannot be cheaper than a feasible uncut option with the same transition, since \(K_X\ge0\).
2. If the cheaper of the two breaks the cap (for a constant hazard, \(H\tau>\ln\frac1{1-\varepsilon}\)), the choice is between the other uncut option, if feasible, and cutting the exposure first (the cheaper feasible cut option), whichever costs less.
3. If neither uncut option meets the cap, cut the exposure first, then take the cheaper feasible cut option.

*Proof.* A minimization over a finite set under a constraint; items 1–3 enumerate which constraints bind. ∎ *Check:* `remove_or_reprice_rule` (code sanity: when an uncut option is feasible the check re-implements the brute-force minimum, so it does not test items 1–3 as written; the rule itself is a chance-constrained menu choice, close to definitional, and the ruin formula of RR1 is its content).

## 3. What this changes

T53's clause 7 moves from CONJECTURE to **PROVED (in-model), ELEMENTARY** in class RR, with the threshold corrected from "roughly \(H\tau_{\text{rep}}>\varepsilon\)" to \(\int_0^{\tau_{\text{rep}}}h\,dt>\ln\frac1{1-\varepsilon}\). The derivation is easy because the class makes it a chance-constrained choice from a menu; the content is in the measurements (hazards, times, \(L_R\), \(C_P\), \(K_X\)), which the theory does not supply. The "disperse, then treat" reading of the biofilm case is item 3 and stays an INTERPRETATION.

## 4. Not derived here

- **Hazard that depends on the response.** RR takes each option's hazard as given. Where removing an entangled part itself raises the hazard (or repricing invites tampering), \(h_o\) must come from a model of the part; not derived.
- **Responses chosen over time** (start repricing, switch to removal if it stalls) are a stopping problem, not a menu; not worked out.
- **A ruin cap on the whole's lifetime** rather than per transition needs the post-transition exposure; RR folds it into \(C_o\).
