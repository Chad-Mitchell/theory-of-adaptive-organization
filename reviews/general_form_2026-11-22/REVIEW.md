# Review of draft PR #161

**Verdict: NOT-READY.**

Head reviewed: `a6a7c7c49b095646f22754d66fa079a48981016c` on `general-form-2026-11-22`. The note is `theory/GENERAL_FORM.md`, CLAIM_MAP v2.79 section W, and `tools/general_form_checks.py`. This review did not edit that branch.

The dominance lemma under an assumed coordinatewise strict order is correct, the worked arithmetic matches an independent recalculation, and the twenty-one DOIs resolve. The load-bearing step does not. Coordinatewise strict monotone retention (S-M+) is an assumption. Section 2 says so. The conclusion of §3, the claim-map introduction, GF1's status, and `OPEN_WORK.md` row T32 treat the Pareto front as what selection forces. Growth-rate selection in an exogenous world forces a complete preorder by the Lyapunov exponent. S-M+ is what remains when that exponent is known only to be strictly decreasing in a chosen vector. The vector in this repository is not derived from copying. One counterexample, inside the exogenous-world hypothesis, reverses retention on a strictly dominated expected-bad vector. A second, outside that hypothesis, sends the dominated type to fixation.

A second blocker sits in Q5. Strict excess over the Gauss–Markov relaxation does not certify interiority of the achievable set. The arithmetic that an interior cloud can be antitone is correct and is a different claim.

## What was read, and what was already in the tree

Read for this review: `theory/GENERAL_FORM.md`, CLAIM_MAP section W and the v2.79 note, `tools/general_form_checks.py`, `THEORY.md` (master equation, CT8, CT12–CT16, CT20, CT22, CT24, CT33, L3 via `theory/LAYERS.md`), `CORE.md` §§1 and the frontier paragraph, `theory/SELECTION_AXIOMS.md` §§0–2, `theory/REPRESENTATION.md` §§0–1 and §7, CLAIM_MAP section V, `theory/SHANNON_2026-11-21.md` §§2–5, `theory/DYNAMICS.md` §3 (CT42), `theory/THEOREM_P_DRIFT.md` PD6. Grep covered Pareto, viability, attention-as-coordinate, and the hypothesis sentence.

Already merged, and used here as authority:

- `theory/SELECTION_AXIOMS.md:25–29`. A2-M says retention is strictly decreasing in a scalar cost \(J\). The note states that this is an axiom. A2-P is persistence only and is marked open. Frequency dependence is excluded from the theorems (`:33`).
- `theory/REPRESENTATION.md` F-0 (`:248`) is the same compactness argument as GF-1(i), including the same discontinuous example. Hypothesis F (`:255`, CLAIM_MAP V5) is the five-name front, status **OPEN**. V6 is the price-free scope list for that front.
- `theory/SHANNON_2026-11-21.md:37–41` writes the scalar Gauss–Markov curve this note recomputes, on the same world \(a=0.9\), \(Q=1\), lead \(2\). Theorem S2 (`:60–62`) is already the price-free reachable set \((I,r,K,D)\) and its support function. Section 3 records efficiency \(0.9574\) when memory and reads are both priced, and leaves joint achievability **OPEN**.
- `CORE.md:30` already records that frontier. `theory/DYNAMICS.md` CT42 is already the Kelly mixture \(q^\star=0.26\) against per-unit means \(1.235\) and \(1.0425\).

The geometry of Pareto order, supporting prices, proper efficiency, and scalarizations that reach unsupported points is prior art, and §8 says so. That part of the hostile reading agrees with the note. The packaging is the claim under review. The packaging upgrades V5 from an open hypothesis to a proved general form, and the upgrade is where the argument breaks.

## Blocker 1. S-M is assumed, and the copying dynamics do not yield the front

### What is proved

GF-1(iii) (`theory/GENERAL_FORM.md:54`) is one line, and the line is right. If \(z\le z'\) and \(z\neq z'\) imply a strictly higher retention for \(z\), then a retention maximizer is undominated. Finiteness is not used. The same sentence holds on any set on which a maximizer exists. On a nonempty compact design set with a continuous retention that satisfies S-M+, a maximizer exists and is Pareto. That continuous case is not stated.

GF-1(i), (ii), (iv), (v), and the viability and Lundberg comparisons are the right comparisons among the relations the note defines. The viable pair \((e,\rho)=(1,0.2)\) and \((0.5,0.2)\) shows that S-P leaves a dominated design in place. The order that reads the second coordinate first ranks \((1,0)\) above \((0,1)\), both Pareto. A viability kernel does not rank designs inside the constraint set. Maximizing \(\theta=2m/s^2\) is a complete ranking. Each of those sentences is about S-M or S-P. None of them is about a copying process.

Section 2 (`:40–44`) and §9 (`:221`) say S-M is an assumption and is not derived from copying. Those two sentences are the right description of the manuscript.

### What is asserted beyond the proof

The conclusion (`:64`) says the Pareto front is the object forced by S-W, S-Z, and S-M+, and by nothing weaker in the list. The claim-map introduction (`measurement/CLAIM_MAP_v2.md:689`) says coordinatewise strict monotone retention forces the front. GF1 is **PROVED (in-model)** (`:693`). `OPEN_WORK.md:80` says the general form is derived. The FALSE list (`theory/GENERAL_FORM.md:66`) includes the sentence "Selection alone forces a complete preorder."

S-M+ is built so that it does not rank incomparable points. A lemma that S-M+ does not produce a complete preorder restates the definition. It does not answer whether copying produces a complete preorder.

The accurate identification statement, which the note does not write, is the following. On a finite set, a score is Pareto if and only if it uniquely maximizes some retention that satisfies S-M+. One direction is GF-1(iii). The other direction has a direct construction. For a Pareto point \(z^\star\), set \(r(z^\star)=0\) and \(r(z)=-1-\sum_i\exp(z_i)\) for every other feasible \(z\). If \(a\le b\) and \(a\neq b\), then \(a\) does not strictly dominate a Pareto point, so the case \(b=z^\star\) does not arise. If \(a=z^\star\), then \(r(a)=0>r(b)\). If neither is \(z^\star\), the constant \(-1\) cancels and \(\sum_i\exp(b_i)>\sum_i\exp(a_i)\). So \(r\) satisfies S-M+ and selects \(z^\star\). A single retention obeying S-M+ selects a subset of the front. The front is the union of those subsets. It is the identified set of an observer who knows only S-M+. It is not the set occupied by one copying process.

### When copying does derive S-M+

Let the environment \(\omega\) be exogenous and ergodic, and let a pure design's offspring number \(W\) depend on the design and on \(\omega\) only (G1). Let retention be the Lyapunov exponent \(\lambda=\mathbb{E}[\log W]\), assumed finite (G2). Let \(W=W(z,\omega)\) for a finite bad vector \(z\), and assume that for almost every \(\omega\) the map \(z\mapsto W(z,\omega)\) is strictly decreasing in each coordinate, with \(W>0\) (G3).

Then \(z\le z'\) and \(z\neq z'\) imply \(\log W(z,\omega)\ge\log W(z',\omega)\) almost surely, with a strict inequality on a set of positive probability. The difference of the logs is integrable and nonnegative and is not almost surely zero, so \(\lambda(z)>\lambda(z')\). That is S-M+. Every maximizer of \(\lambda\) is Pareto in \(z\). The replicator equation \(\dot x_i=x_i(\lambda(z_i)-\bar\lambda)\) increases the share of higher \(\lambda\) and has its global attractors on \(\arg\max\lambda\).

G3 is a monotonicity hypothesis on offspring. The replicator equation does not supply it. A2-M is the scalar special case of the same hypothesis, already labeled an axiom in the selection note. S-M is the vector form of A2-M, with the scalar \(J\) deleted and the order on \(z\) put in its place.

The log-linear case shows what "stronger" means. If \(\log W=-\langle c(\omega),z\rangle\) with \(c(\omega)\ge 0\) and \(\mathbb{E}[c_i]>0\), then

\[
\lambda(z)=-\langle\mathbb{E}[c],z\rangle.
\]

Growth-rate selection minimizes a nonnegative linear cost. The selected object is a priced point. The Pareto front is the set of points that some nonnegative price could have selected. An observer who knows the signs of the prices and does not know the prices sees the front. The organism, under this map, does not sit on an unranked front. It minimizes \(\langle\mathbb{E}[c],z\rangle\).

So the ladder in §3 is a ladder of assumptions, and as a ladder of assumptions it is correctly ordered: S-P is weaker than S-M+, and a complete ranking is stronger than S-M+. It is not a ladder of outputs of copying. Under G1 and G2, copying emits the complete preorder \(\lambda\). S-M+ is recovered only by adding G3 and then forgetting every feature of \(\lambda\) except the product order. The FALSE stamp on "selection alone forces a complete preorder" is the wrong theorem for G1–G2. The counterexamples in §3(iv)–(vii) never mention a copying process.

### Where S-M+ fails

**Expected bads, geometric-mean retention, exogenous world.** G1 and G2 hold. G3 fails for the score the repository would actually write down.

Two states, probability \(1/2\), i.i.d. Both designs use a constant resource and make a constant error, so the expected-bad vector is the certain vector.

| Design | Resource | Error | Offspring in the two states | \(\lambda=\mathbb{E}[\log W]\) |
|---|---|---|---|---|
| L | 1 | 0 | \(4\) and \(0.05\) | \(0.5\ln 0.2=-0.804718956\) |
| H | 2 | \(0.4\) | \(1.1\) and \(1.1\) | \(\ln 1.1=0.095310180\) |

The score of L is strictly smaller in both coordinates. The long-run growth of L is strictly smaller. S-M+ applied to \((\mathbb{E}[\text{resource}],\mathbb{E}[\text{error}])\) is false. Both offspring numbers are positive, so this is not a ruin-cap comparison: neither lineage is eliminated by S-P.

The state-contingent log-offspring vectors are \((\ln 4,\ln 0.05)\approx(1.386294,-2.995732)\) and \((\ln 1.1,\ln 1.1)\). Those two vectors are incomparable, and \(\lambda\) is monotone in each of them. S-M+ comes back if and only if the coordinates are the arguments of \(\lambda\). Choosing \((\mathbb{E}[\text{resource}],\mathbb{E}[\text{error}])\) drops the argument geometric-mean selection actually uses. This is the same Jensen gap as CT42, moved onto a vector that looks like the note's bad vector. CT42 itself does not quite serve, because the lean design's shock factor is \(0\) and its geometric growth is \(-\infty\); a ruin coordinate then separates the two pure designs. The table above closes that gap.

Bet-hedging under a shared shock is already CL20 and CT42 in this repository (`theory/DYNAMICS.md:131–155`). The note uses CT42 to separate Kelly from expected currency (`:98`). It does not apply the same separation to S-M.

**Frequency dependence.** Drop G1. Random matching. Bad vectors \(z_A=(1,1)\) and \(z_B=(2,2)\). Payoffs to the row player:

|  | meet A | meet B |
|---|---|---|
| A | 1 | 0 |
| B | 3 | \(0.5\) |

At frequency \(x\) of B, \(f_A=1-x\) and \(f_B=3-2.5x\), so \(f_B-f_A=2-1.5x\ge 0.5\) on \([0,1]\). The replicator derivative of \(x\) is positive on \((0,1)\). The strictly dominated type goes to fixation. At \(x=0\) the invasion gap is \(2\).

**Non-transitive selection.** Payoffs in which A beats B, B beats C, and C beats A by the same margin have no frequency-independent scalar on the three types. The replicator does not converge to a pure maximizer. In this regime the note's FALSE sentence is the right description, and the manuscript's counterexample is not this regime. The sentence has to be scoped to the regime, or it is false in the exogenous regime and true in this one.

**A trait with an interior optimum.** Memory, attention, or layer count can raise offspring over one range and lower it over another. Such a trait is not a bad, and S-M+ stated for it is false. The note already says this for layer count and for attention (`:84–86`). That negative conclusion is right. It is also the reason those coordinates cannot be smuggled back in as "forced bads" by a floor that merely mentions them.

### What would discharge the blocker

State G1–G3 as the derivation, prove the lemma above, and put the two counterexamples next to it. Then replace the conclusion on line 64 with the trichotomy:

1. G1–G2 with a known \(\lambda\) produce \(\arg\max\lambda\), a complete preorder.
2. G1–G3 with \(\lambda\) known only to be strictly decreasing produce the Pareto set as an identified set.
3. S-P produces the viable set.

Narrow every FALSE sentence to the relation it actually refutes: S-M+ does not rank incomparable points; S-P does not produce the front; S-M+ does not produce a ruin cap, a lexicographic order, or a Lundberg objective. Delete "selection alone forces a complete preorder" from the FALSE list, or restrict it to frequency-dependent and non-transitive copying and give those counterexamples. Keep GF-1(iii) as a proved lemma under S-M+. Do not call that lemma the derived general form.

Until that case split is the claim, GF1's **PROVED** status overstates the manuscript, and T32's word "Derived" (`OPEN_WORK.md:80`) overstates it in the work list.

## Blocker 2. Excess over the relaxation does not certify a miss

`theory/GENERAL_FORM.md:177` says that a design whose loss equals \(D(P)\) and whose memory and directed-information rate both strictly exceed the two right-hand sides is strictly dominated inside the relaxation, hence strictly inside every achievable set contained in the relaxation. The same certificate is item 3 of the measurement list (`:185`) and the Why cell of GF5 (`measurement/CLAIM_MAP_v2.md:697`).

The first half is true. The score \((I(P),r(P),D(P))\) is in the relaxation and strictly dominates \((I(P)+\delta,r(P)+\delta,D(P))\) for \(\delta>0\). The "hence" is false. A point can be strictly inside a set \(R\) and Pareto in a subset \(A\subset R\).

Concrete counterexample. Let the relaxation \(R\) be the set of scores lying on or above the curve of §7. Let

\[
A=\bigl\{\bigl(I(P)+0.4,\; r(P)+0.4,\; D(P)\bigr):0<P\le V\bigr\}.
\]

Then \(A\subset R\). Every point of \(A\) lies \(0.4\) nats above both curves. Every point of \(A\) is undominated in \(A\), because \(A\) is a translate of the efficient curve. Strict excess over the relaxation is compatible with sitting on the achievable front, whenever the achievable front is a shift of the relaxation. The manuscript leaves that shift open: `theory/SHANNON_2026-11-21.md:55` records \(J_{\mathrm{floor}}/J=0.9574\) on this same world when both resources are priced, and leaves joint achievability **OPEN**. The note repeats the open status at `:222`. The certificate contradicts that open status.

The separate arithmetic, that the cloud \((I(P)+0.4,\,D(P))\) for \(P\in\{0.3,0.5,0.8,1.2\}\) is antitone and interior to the memory curve, is correct. Recomputed below. Antitonicity of a fitted cloud does not locate the relaxation boundary. That sub-claim can stay, labeled as arithmetic. The certification sentence cannot.

GF5's row status **OPEN** is the right status for a field prediction that is not locked. The false sentence is inside the row. An open row that states a false certificate is not saved by the word OPEN.

### What a test would have to fix

A miss of "on the achievable front" needs a dominating score that is achievable, or excess over a bound that has been proved tight for the preregistered class. Excess over the relaxation is neither. On the world already in SHANNON §3, a design that minimizes additive \(J\) at positive prices can sit off the relaxation boundary. Interiority to the relaxation is therefore not a prediction that additive \(J\) fails to make. Undominatedness in the achievable set is a prediction that strictly positive prices already make (S3(i), which the note cites). The floors locate the relaxation. The general form does not locate it a second time.

A test that separates this hypothesis from additive \(J\) has to use something additive \(J\) does not share. Three comparisons do that, and none of them is GF-P1:

- An unsupported feasible point, with mixtures infeasible, selected in a designed world. Section 7 states this as in-model arithmetic and correctly refuses it as a field protocol.
- A stake change that moves the operating point along one computed front while the world is held fixed. Additive \(J\) predicts the direction (CT33). An unranked front does not.
- Two designs tied on every priced coordinate, both inside a slack cap, ranked by ruin. Additive \(J\) ties them. That comparison treats ruin as a bad, which §4 says is a modelling choice.

Until a preregistration, the measurement list in §7 is a sketch, as the note says. A preregistration that used the §7 certificate would lock a false rejection rule. The list also has to grow, before it is a test, by the following items.

1. The loss, the memory functional (stock on the stationary domain, rate when variance diverges, PD6), the lead, and the world class, fixed before the design's resources are computed.
2. World parameters from a series the design does not choose, with an error budget. Lead from the task.
3. An estimator of the memory mutual information and of directed information, with a bias bound. Mutual-information estimators are biased. The margin has to exceed that bound in the direction of the error the test is aimed at. Underestimating information manufactures interior points. Overestimating information manufactures points on the floor.
4. Channel noise and store noise (`theory/STORE_NOISE.md`) measured or excluded. A second task and a nonstationary world move the front. The note names these as nuisances. A protocol has to say what is done with them.
5. The existing qualification gate and the binomial allowance in THEORY §8. This note sets neither. GF5 stays a sketch until they are set, and the certificate above has to be replaced before they are set.

## Status labels

| Row | Status in the map | What the text proves | Label |
|---|---|---|---|
| GF1 | PROVED (in-model) | S-M+ implies maximizers are Pareto. Existence of one Pareto point from a continuous score on a nonempty compact design set. S-P, lex, viability, and Lundberg sit on different rungs of the assumption ladder. | The lemma is proved. "Selection forces the front" and the FALSE stamp on a complete preorder are not. Overstated. Blocker 1. |
| GF2 | PROVED (in-model) | An audit of which proved floors mention which slots, plus the negative claims on attention and on \(K\). | Defensible as an audit of mentions. Overstated as a derivation that retention decreases in those slots. Should-fix 1. |
| GF3 | PROVED (in-model) | Risk-neutral expected currency, a half-space cap, and nonnegative linear prices are each doing work, by the Kelly pair, the Lundberg pair, the negative-price witness, the square, and the dent. | Holds, as a conditional theorem. The geometry is prior art and is labeled as such. |
| GF4 | PROVED (in-model) | The survival list matches the cited theorems, with one false parameter name. | Holds after the \(\rho\) cell is corrected. Should-fix 2. |
| GF5 | OPEN | The antitone-interior arithmetic. A sketch of a measurement. | OPEN is right. The certification sentence is false. Blocker 2. |

The FALSE sentences that survive are these. S-P does not force the front (the two-point viable pair). S-M+ does not force a lexicographic cap or a Lundberg ranking. A coordinate cap \(\rho\le\varepsilon\) preserves convexity of a convex score set (`:121`). Separability yields \(\sum f_i\), and linearity is concatenation (`:116`, the square \((1+1)^2\neq 1^2+1^2\)). Convexity of the image yields some \(p\ge 0\), \(p\neq 0\), and does not yield risk neutrality, the cap, or the choice of memory functional (`:125`). Calling one memory stock the coordinate on every world is false, by PD6. The unconditional claim that the floors make \(K\) a bad is false (`:86`). Attention as a derived peer of the other four is false (`:84`). An antitone cloud is not a test (`:195`). Each of those has a counterexample or a one-line proof in the note, and the counterexamples check.

## Q2. The coordinate audit, and what is new

The definition on `:72` says a coordinate is forced when every scored design must carry it because the task or a proved floor refers to it. The opening on `:9` puts those coordinates into the bad vector whose retention is monotone. Those are two relations.

A floor constrains the feasible set. \(D\ge D_{\mathrm{IB}}(I_{\mathrm{mem}})\) (CT1, S1) mentions a memory slot and a loss. It does not say that retention decreases in the memory slot. If memory is free, the floor still constrains designs, and extra memory at the same loss is not dominated. The same split applies to the causal rate floor (S1, PD1a; Tatikonda, Sahai and Mitter) and to a ruin statistic. S-P needs something to read. Growth-rate selection with \(W=0\) on ruin already has the hitting event inside \(\lambda\), and a second ruin coordinate double-counts it. Section 4 says the choice among trading ruin, capping it, and maximizing \(\theta\) is open. That sentence is right. "A ruin statistic is forced" is right only for an elimination rule that reads one.

The negative half of the audit is right, and most of it is already in the representation note.

- Which loss is used is a modelling choice. Folding lateness into the loss is the identification in THEORY §3, not a theorem that every late action is worthless (`:74`).
- The gross stock, predictive information, and Still's nonpredictive information are different functionals. Still, Sivak, Bell and Crooks bound dissipation by the nonpredictive part under their hypotheses. They do not force the gross stock to be the bad (`:76`). PD6, already proved, says the raw stock diverges for every uniformly accurate design when variance diverges. A rate can be the slot there. Aczél, Forte and Ng characterize a nonnegative cone: a negative multiple of Shannon entropy is outside it, and \(-\!H\) fails subadditivity whenever \(H(X,Y)<H(X)+H(Y)\). That sign remark is correct.
- S-A, \(A\ge c\cdot r\), is an assumption (SHANNON). Which concatenating coordinate carries the acquisition price is V4 and stays open (`:78`).
- Attention, if it is the currency named in THEORY §3, repeats a unit already used to pay the other terms (`:84`). A simultaneous-processing limit is a constraint on the feasible set. As a derived fifth bad it is not obtained from S-M or from a floor. V5 can remain an open hypothesis about a chosen vector. This note should not be read as deriving that vector.
- An extra layer that leaves \((I,r,e,\rho)\) unchanged is not dominated. Dominance of \(K\ge 2\) by \(K=1\) at the same error needs an extra monotonicity (`:86`). S1 charges no \(h\cdot 1[I>0]\). The memoryless comparison \(J=2.197<3.187\) is SHANNON §2, same world.
- Linking is a further slot when communication consumes a resource the acquisition coordinate does not count (`:88`).

The five-name list in V5 is therefore not a derived list. The note says this (`:90`). The new sentence is the split between "a floor mentions the slot" and "the slot is a bad." The manuscript then collapses the split in the opening paragraph and in the GF2 status. Should-fix 1: keep the mention-audit as the proved content, and mark "retention decreases in these coordinates" as open until a map into \(\log W\) is stated.

Nothing in §4 is a new information inequality. Rate–distortion, the information bottleneck, Still et al., and the causal rate are used as floors the repository already proved. Viability theory is used for the name of the set S-P produces. Multiobjective optimization is used for the name of the set S-M+ produces. Shoval et al. 2012 already read phenotype clouds as sitting near a low-dimensional front. Farrell 1957 and Debreu's coefficient of resource utilization are the price-free efficiency facts. Theorem S2 is the price-free frontier inside this repository. The manuscript's own §8 is the right prior-art paragraph. The sentence that should be added is that V5 is already the open field claim, and GF1 does not promote it.

## Q3. The reduction to additive \(J\)

The conditional theorem is in good shape. Recomputed independently (`reviews/general_form_2026-11-22/checks/recompute.py`, and a 200-step bisection plus a 20,000-point sign count):

- Kelly: \(q^\star=0.05\times 1.30/(1.30-1.05)=0.26\) exactly. Lean mean \(0.95\times 1.30=1.235\) exactly. Robust mean \(0.95\times 1.05+0.05\times 0.90=1.0425\) exactly. Expected factor ranks pure lean first. These are CT42's published inputs. The manuscript's \(G=0.128\) is in `theory/DYNAMICS.md`, not restated as a new constant here; a direct evaluation of the mixture growth is \(0.1279\), which rounds to the published \(0.128\).
- Lundberg, published path \(y=1\), \(c=0.05\), \(w=\sigma=1\), \(s_0=0.3\). \(\alpha=1/2\), \(\beta=1/3\), \(\tau_E=\sqrt{0.1}=0.316227766017\). The numerator \(\varphi=m's^2-m(s^2)'\) has one sign change on the positive-margin interval \((r_1,r_2)\), and the unique zero inside \((r_1,\tau_E)\) is \(\tau_S=0.236207526722\). The printed \(0.2362\) and \(0.3162\) are the right four-decimal roundings. The representation review's \(0.236208\) and \(0.316228\) are the same root.
- Dent: \(A=(0,1)\), \(B=(1,0)\), \(C=(0.6,0.6)\) are pairwise incomparable. \(C\) minimizes \(\langle p,\cdot\rangle\) for no \(p\ge 0\) other than zero, because the two ratio bounds are \(p_1/p_2\le 2/3\) and \(p_2/p_1\le 2/3\), and \((2/3)^2=4/9<1\). A \(501\times 501\) grid finds no supporting weight. The mixture \((1/2,1/2)=(0.5,0.5)\) dominates \(C\). Unweighted Chebyshev scores \(1,1,0.6\).
- Quartic Gibbs factor: \(\Gamma(5/4)/\Gamma(1/4)=1/4\) by \(\Gamma(z+1)=z\Gamma(z)\). For \(J=x^4\) the mean under \(e^{-\beta J}\) is \(1/(4\beta)\). The homogeneous identity \(d/(p\beta)\) is the Lean equipartition (`formal/lean/README.md`, `gibbs_excess`). The citation is accurate.
- Single-crossing illustration: on \(e=1/m\), the scalar minimizer \(m^\star=\sqrt{w}\) has error \(1,0.707,0.5\) at \(w=1,2,4\), and the pick \(m=1/w\) has error \(1,2,4\). CT33 needs the scalar.

The separating-hyperplane paragraph (`:106`) is the standard argument: \(Z-z^\star\) misses the open negative orthant, so a separating normal may be taken nonnegative and nonzero. Free disposal is stated and not used. Debreu 1954, "Valuation Equilibrium and Pareto Optimum," is the valuation-equilibrium theorem; the finite-dimensional step written out is the separating hyperplane theorem. The citation can stay as the classical price theorem this case instantiates, with that scope. Geoffrion 1968 is correctly reserved for strictly positive weights, and it is not re-proved. The two routes to linear prices are correctly distinguished (`:110`): convexity produces a linear price directly; Debreu's additive representation on at least three essential intervals produces \(\sum f_i\), and linearity is a further Cauchy equation. A discrete layer count is the integer Cauchy equation under an extra separability assumption the \(n\ge 3\) citation does not prove. A negative error price on three intervals is V1's witness \(I+A-\mathbb{E}[\ell]\), and it is not a negative multiple of a Shannon coordinate. Nonnegative prices are A8. That matches the merged representation note.

One repair inside an otherwise correct section. Unweighted \(\max(z_1,z_2)\) is weakly monotone: moving \((0.6,0.6)\) to \((0.6,0.5)\) does not change the value, so this scalarization is not an S-M+ retention (`:118`). On the three-point set no pair is ordered by the product order, so every ranking satisfies S-M+. The retention with \(r(C)=0\) and \(r(A)=r(B)=-1\) is an S-M+ witness that selects \(C\). The augmented form \(-\max_i(z_i-z_i^\star)-\varepsilon\sum_i(z_i-z_i^\star)\) for small \(\varepsilon>0\) is a strictly monotone scalarization that does the same job on larger sets. Should-fix 3.

## Q4. The scope list

No new inequality is claimed, and the placement of the named theorems matches the statements they cite, with one exception.

Survives as a constraint or as dominance, under the hypotheses those theorems already have: antitonicity of a Pareto pair with the other coordinates fixed; existence from GF-1(i); CT1, S1, and PD1a as curves that do not pick a point; CT8 as Blackwell's theorem that a garbling does not lower Bayes risk, in a stationary Markov world with renewal checks, false for non-Markov observations (`theory/GENERAL_THEOREM.md` on rule 5); CT25's buffer scaling \(B\ge z_\varepsilon\sigma\tau^H\) as the shape of a per-window chance constraint (THEORY §5(iv)); L3's \(E_K>E_\infty\) for every finite \(K\) on a non-rational spectrum (`theory/LAYERS.md:51`), with \(K^\star(R)\to\infty\) still needing the ratio \(R\); layer caps only under the extra monotonicity of §4(6).

Needs a scalar, a stake, or a ratio: CT33; CT20(ii); \(K^\star(R)\), \(R^\star\), and \(K^\star_0(R)\); CT24, with the binding-ruin elasticities \(0.584\) and \(0.563\) summing to \(1.147\) against shares \(0.528\) and \(0.472\) as THEORY states them; \((\alpha-1):1\) only with CT12 added; \(d/(2\beta)\) under A2-L and a quadratic well, with degree \(p\) giving \(d/(p\beta)\); CT22's multiplier on the scalar path; CT7; CT12's elasticity \(1/\alpha\); \(T^\star=\sqrt{6k/(w\sigma^2)}\), which is CORE §3's barrier lifetime, the minimizer of \(k/T+w\sigma^2 T/6\). CT42 is correctly refused as a survivor of risk-neutral \(J\).

The exception is the sharing row (`theory/GENERAL_FORM.md:159`). The cell says the minimal extra assumption is "the price ratio inside \(\rho\)." In CT14, \(\rho=q_g/q_u\), the ratio of shared drift intensity to private drift intensity (`THEORY.md:351`). At zero upkeep and equal prices, \(N^\star=(\sqrt{1+\rho}+1)^2/\rho\) for the square-root technology, and the common price cancels. The price ratio in that neighborhood is the telling threshold \(d/c\) of CT16, which is a different row. The second sentence of the cell, that a sign about shared versus private drift needs the drift as a parameter, is the right sentence. The row belongs in the "needs a scalar cost" table, because \(N^\star\) is a comparison of scalar costs in the class \(P(a,b)\). The named parameter is the drift ratio, not a price. Should-fix 2.

## Q5. Distinctiveness, after the certificate is removed

What remains of Q5, once the false certificate is deleted, is a real distinction and a narrow one.

A fitted antitone cloud is predicted by any strictly monotone tradeoff. Shoval et al. fit fronts to traits. Farrell and Debreu's coefficient measure efficiency against a front. Theorem S2 already defines the front from the reachable set and says the definition contains no prices. The worked cloud at \(+0.4\) nats is antitone and interior to the memory curve, so antitonicity does not see interiority to the relaxation. That is a correct warning against adopting the frontier re-read's antitone test. The note is right to refuse that draft as authority (`:165`).

The prediction that is not thereby established is that a selected design sits on the boundary computed from the floors. Additive \(J\) at strictly positive prices predicts undominatedness in the achievable set and does not predict attainment of an unattainable relaxation. The general form under S-M+, applied to the achievable set, predicts the same undominatedness and does not predict attainment of the relaxation either. The worked point is an illustration of the relaxation, on a world SHANNON §2 already used. The numbers are right. They are not a new curve.

Recomputed with `Decimal` at 50 places, natural log, \(a=0.9\), \(Q=1\), \(k=2\), \(P=0.5\):

\[
V=\frac{1}{1-0.81}=\frac{1}{0.19},\qquad
a^{4}=0.6561,\qquad
D=0.6561\times 0.5+V\times 0.3439=2.13805
\]

exactly in decimal arithmetic. \(I=\tfrac12\ln(V/P)=1.176939193691\), which prints as \(1.176939\). \(r=\tfrac12\ln(a^2+Q/P)=\tfrac12\ln(2.81)=0.516592241673\), which prints as \(0.516592\). Float and `Decimal` agree through the printed digits. The four-point cloud is antitone, and each memory coordinate sits \(0.4\) nats above \(I(P)\). The point \((I+0.4,\,r+0.4,\,D)\) is dominated by \((I,r,D)\) inside the relaxation. That is all the arithmetic shows.

## Wording, the hypothesis sentence, and the diff

The hypothesis sentence is byte-identical, 103 bytes, one copy each, in `THEORY.md:41`, `CORE.md:9`, `README.md:9`, `theory/SELECTION_AXIOMS.md:13`, and `theory/GENERAL_FORM.md:20`:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

`theory/DIRECTIONS_2026-11-22.md` quotes the same bytes. The diff of `THEORY.md`, `README.md`, and `STATUS.md` against `origin/main` (`37794bb`) is the claim-map pointer v2.78 to v2.79. No preregistration, lock, or hash is in `git diff --name-only origin/main...a6a7c7c`.

The word "bill" does not occur in `theory/GENERAL_FORM.md` or in section W. The word "kill" does not occur there either. The phrase barred by the house style for a name of this theory occurs twice, both times as a denial: `theory/GENERAL_FORM.md:18` and `:219`. Should-fix 4: delete the phrase. A denial still prints it.

`OPEN_WORK.md:80` says the general form is derived and that the row needs a reviewer. The second clause is right. The first is Blocker 1.

## Commands and results

All of these were run from `/agent/repos/theory-of-adaptive-organization` at `a6a7c7c`, after `git fetch origin main`. `origin/main` is `37794bbb269027fb7ef5b18b7908bc42d989fbba`. `lake build` was not run. `nice -n 19` was used for the Python checks and for pytest.

| Command | Result |
|---|---|
| `git fetch origin main` | `origin/main` = `37794bb`. STATUS's `eddf64e` is the fourth first-parent commit of that tip. |
| `nice -n 19 python3 tools/check_consistency.py` | `FAIL: 0`. Tally 371. `RESULT: PASS`. Exit 0. Advisory length warnings on THEORY and README, not failures. |
| `nice -n 19 python3 tools/check_fresh.py` | Window `37794bb f84997c 32cc8e0 eddf64e 886d69b`. `RESULT: PASS`. Exit 0. |
| `nice -n 19 python3 tools/check_open_work.py` | Union missing from `OPEN_WORK.md`: 0. `RESULT: PASS`. Exit 0. |
| `nice -n 19 python3 -m pytest -q tools` | `251 passed, 1 skipped` in 300.79s. Exit 0. The machine had no pytest, numpy, scipy, or sympy; those were installed with `pip install --user` in order to run the suite. The count matches the PR body. |
| Independent arithmetic, `Decimal` and a separate bisection | \(I=1.176939193691\), \(r=0.516592241673\), \(D=2.13805\) exactly, \(q^\star=0.26\), means \(1.235\) and \(1.0425\), \(\tau_S=0.236207526722\), \(\tau_E=0.316227766017\), \(\Gamma(5/4)/\Gamma(1/4)=1/4\), one sign change of \(\varphi\). |
| Crossref, 22 November 2026, all 21 DOIs in `tools/general_form_checks.py` | 21/21 titles contain the note's needle. Debreu's two reprint chapters return an empty year, as the note says. Aubin, *Viability Theory*, author Jean-Pierre Aubin, issued year 2009, container empty. Shoval et al. resolves with nine authors, the last U. Alon, matching the note's list. Miettinen issued year 1998. |

## What would make the derivation complete

In order:

1. **Derive S-M+, or stop calling it the general form.** Prove the Lyapunov lemma under G1–G3. Put the expected-bad counterexample and the frequency-dependent fixation counterexample in §3. State the trichotomy: known \(\lambda\) gives a complete preorder; unknown monotone \(\lambda\) gives the Pareto set as an identified set; S-P gives the viable set. Narrow the FALSE list to the relations the counterexamples actually hit. Relabel GF1 so the proved lemma and the undischarged axiom are different sentences. Change `OPEN_WORK.md:80` from "Derived" to the conditional statement.
2. **Split the coordinate audit.** Proved content: which floors mention which slots, the PD6 domain split, attention not a derived peer, \(K\) a bad only under an extra monotonicity, V4 still open. Open content: that retention decreases in those slots. That decrease is G3, and G3 is a map into \(\log W\). A floor is not that map. Leave V5 **OPEN**.
3. **Repair the Q5 certificate.** Delete the "hence strictly inside every achievable set" inference at `:177`, the matching item at `:185`, and the certification clause in the GF5 Why cell. Keep the antitone-cloud arithmetic. State that a miss needs an achievable dominator or a tight bound. State one comparison that additive \(J\) does not share, and mark it as a sketch.
4. **Correct the scope cell and the scalarization witness.** In the \(N^\star(\rho)\) row, name \(\rho=q_g/q_u\). Say that unweighted Chebyshev is weakly monotone, and give the S-M+ ranking that selects \(C\).
5. **Delete the barred phrase** at `theory/GENERAL_FORM.md:18` and `:219`.

After (1)–(3), the manuscript would be a conditional theorem with an honest identification result, a coordinate audit that does not promote floors into bads, and a field sketch that does not reject achievable designs for missing an unattainable relaxation. That is a different paper from the one GF1–GF5 currently label, and it is the paper the lemmas actually prove. The arithmetic, the DOI resolutions, the hypothesis sentence, and the scope of CT8, CT33, L3, CT22, and \(T^\star\) can stay.
