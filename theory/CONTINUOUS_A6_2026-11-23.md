# The continuous mutual-information extension of A6

*Monday 23 November 2026 (America/New_York). Open-work row T48, written against `main` `4594eef` (after PR #235). It does not change `THEORY.md` or the hypothesis sentence. DOIs below were resolved on the Crossref API the same day (`theory/continuous_a6_checks/crossref.out`). A check script on finite alphabets and quantized Gaussians, not a new simulation of a real system. A self-check, not an independent review.*

Labels follow the repo: **PROVED (in-model)** is a result inside a named class or under named axioms. **KNOWN** is published and credited, only for what that source states. **ELEMENTARY** is a direct consequence of a proved or known statement, not a new named theorem. **CONJECTURE** is a named bet, not a result. **OPEN** is not derived. This note identifies a coordinate of the cost. It does not derive the cost, and it does not compute a new minimum.

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

## 0. Bottom line

Axiom A6, as written in `theory/REPRESENTATION.md`, characterizes Shannon entropy of a finite law (Aczél, Forte and Ng, with the continuity step in Csiszár's survey), and therefore Shannon mutual information of finite variables. The Gaussian plants in the repository use a differential mutual information. That formula is not a theorem about finite laws, and A6 already named it as an extension. This note states the extension and records how far it goes.

**The extension, under stated conditions.** Let \(X\) and \(Y\) be random variables taking values in standard Borel spaces, and let \(I(X;Y)\) be finite. The mutual information used as the memory coordinate is **KNOWN** to equal both of the following, which therefore agree with each other:

1. the Kullback–Leibler divergence of the joint law from the product of the margins,
   \[
   I(X;Y)=D_{\mathrm{KL}}\bigl(P_{X,Y}\big\|P_X\otimes P_Y\bigr);
   \]
2. the supremum of ordinary finite-law mutual informations over finite measurable partitions of the two value spaces (Gelfand and Yaglom 1957; Dobrushin 1959; Pinsker 1964),
   \[
   I(X;Y)=\sup_{\alpha,\beta} I(X_\alpha;Y_\beta).
   \]

When \(X\) and \(Y\) are finite, the identity partition attains the supremum, so the value is exactly the finite-law mutual information A6 already covers. When the joint and marginal laws have densities and the integral is finite, the same number equals the differential mutual information \(h(X)+h(Y)-h(X,Y)\). That is the formula the Gaussian plants use. Both agreements are **KNOWN**. The packaging — that this is the A6 extension, and that Theorem R1 is unchanged — is **PROVED (in-model)** in §7.

**What carries, and what does not.** Theorem R1 is a theorem about a continuous cost on a product of real interval coordinates. A finite mutual information is such a coordinate. The additive form, the affine freedom, and the role of A8 and of the extra separability assumption for \(hK\) are unchanged. Finite-law results that use only the properties mutual information keeps under this definition — nonnegativity, symmetry, the chain rule, the data-processing inequality, and \(I=0\) if and only if the two variables are independent — carry over under the same measurability and finiteness conditions, and their finite-law statements are not changed. The Aczél–Forte–Ng uniqueness for *entropy itself* does not extend to differential entropy, and is not claimed to. Differential entropy can be negative, is not invariant under a smooth change of coordinates, and is not a limit of discrete entropies. Mutual information is. When \(I(X;Y)=\infty\), the memory coordinate is not a real interval value, and Theorem R1 is not applied.

**Gross stock and net flow.** A6's coordinate remains the gross stock \(I_{\mathrm{mem}}=I(M_t;X^t)\). That stock is already a mutual information, not a raw entropy. It is not the net learning rate \(I_{\mathrm{alt}}\) that the heat notes bound. This extension does not identify those two functionals, and it does not replace a net flow by a gross jump rate.

## 1. The method, and what this note is

The method is the same as everywhere in the theory: write the cost, find its minimum, and read off the design. Shannon's pattern, as `CORE.md` §2 and `theory/SHANNON_2026-11-21.md` §0 state it, is a quantity fixed by the task, a converse no design beats, achievability, and a formula computed from the world's statistics alone.

This note is about the quantity, not about a new converse or a new minimum. In the representation, the memory term of the cost is a price times a memory coordinate. A6 says which coordinate that is. For finite laws the coordinate is Shannon mutual information in nats, and the finite-law uniqueness theorem already on the page supplies it. For continuous laws the same role is played by the Gelfand–Yaglom–Dobrushin mutual information just stated. The formula is computed from the joint law of memory and world alone. The minimum, the design, and the five-term display in THEORY §3 are not re-derived here. Whether a real system sits near a minimum is the hypothesis, and is not decided here.

## 2. What A6 already states

The finite-law half of A6 is unchanged, and is not re-proved. Aczél, Forte and Ng (doi 10.2307/1426210) show that expansibility, symmetry, subadditivity, and additivity characterize the nonnegative cone generated by the Shannon and Hartley entropies. The same postulates plus continuity for \(n=2\) isolate Shannon entropy of a finite law, up to a positive constant. That continuity step is the one in Csiszár's survey (doi 10.3390/e10030261). The constant is the base of the logarithm. The representation note takes natural logarithms, so a finite-law entropy is in nats, and the constant is absorbed into \(\kappa\).

Mutual information of finite variables is a difference of those Shannon entropies, so the finite-law theorem covers it. A6 already chooses which mutual information is the coordinate: the gross stock \(I_{\mathrm{mem}}=I(M_t;X^t)\). Predictive information, directed information, and \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\) are different functionals. This note does not change that choice. It supplies the same functional on a larger class of laws.

## 3. Prior art: what each source establishes, and what is new

Every DOI in this section was resolved on `api.crossref.org` on 23 November 2026. A repository search was done first. Nothing below is claimed as new except the packaging in §7: that this known identification is the A6 extension, and that Theorem R1 and the finite-law Shannon properties listed in §8 carry over under the stated conditions, without change to their finite-law statements. The gap each source leaves is stated for that source, not as a criticism of the paper.

**Gelfand and Yaglom (1957),** English translation *Amer. Math. Soc. Transl. Ser. 2* 12:199–246, 1959, doi 10.1090/trans2/012/09. Crossref returns the author field as a single string "Gel′fand, I. M. and Yaglom A. M." The original is *Uspekhi Mat. Nauk* 12(1):3–52, 1957. They define the amount of information in one random function about another, write it as an integral of a logarithmic likelihood, and compute it for Gaussian processes. The finite-dimensional (partition or coordinate) approximations are part of that development. They do not state axiom A6, and they do not discuss the representation of a cost.

**Dobrushin (1959),** English translation "General formulation of Shannon's main theorem in information theory," *Amer. Math. Soc. Transl. Ser. 2* 33:323–438, 1963, doi 10.1090/trans2/033/11. The original is *Uspekhi Mat. Nauk* 14(6):3–104, 1959. This is the systematic general-alphabet treatment: information defined from finite partitions, and Shannon's theorem in that setting. It is not a representation theorem for a cost, and it is not a characterization of differential entropy.

**Dobrushin (1960),** "Passage to the Limit under the Information and Entropy Signs," *Theory Probab. Appl.* 5:25–32, doi 10.1137/1105003. Mutual information is lower semi-continuous, but a limit of joint laws need not pass inside the information functional without further conditions. The supremum over partitions, and the monotone limit along a generating nested sequence of partitions, are not the same as an unrestricted limit. This paper is the warning used in §5.

**Pinsker (1964),** *Information and Information Stability of Random Variables and Processes*, Holden-Day, San Francisco. Translated and edited by Amiel Feinstein from the 1960 Russian monograph. This is the standard monograph for the general theory: mutual information as the supremum of discrete mutual informations, and as the integral of the information density when the Radon–Nikodym derivative exists (and as \(+\infty\) when it does not). Crossref returned no work record for the book itself, and the 1964 edition predates ISBN. The book is cited from its title page, not from a DOI.

**Kolmogorov (1956),** "On the Shannon theory of information transmission in the case of continuous signals," *IRE Trans. Inf. Theory* 2:102–108, doi 10.1109/TIT.1956.1056823. A continuous-signal information theory, already in the historical line. It is not the partition-supremum theorem, and it is not A6. A later English text, "Theory of transmission of information," *Amer. Math. Soc. Transl. Ser. 2* 33:291–321, 1963, doi 10.1090/trans2/033/10, sits in the same AMS volume as Dobrushin 1959.

**Cover and Thomas,** *Elements of Information Theory*, 2nd ed., Wiley. Crossref issued 7 April 2005 and lists a print date of 16 September 2005, doi 10.1002/047174882X; ISBN 978-0-471-24195-9 (print), 978-0-471-74882-3 (electronic). The book is commonly cited as 2006. Theorem 8.3.1: if the density of \(X\) is Riemann integrable, the entropy of the bin-width-\(\Delta\) quantization satisfies \(H(X^\Delta)+\log\Delta\to h(X)\) as \(\Delta\to 0\). Section 8.5 defines the differential mutual information as the relative entropy of the joint density against the product of the margins, equations (8.47)–(8.49), notes that the \(-\log\Delta\) terms cancel in the quantized mutual information, equations (8.50)–(8.52), and extends the definition to general laws by finite partitions of the range, beginning at (8.53). These are textbook statements of the known identifications, not a uniqueness theorem for differential entropy, and not a cost representation.

**Gray (2011),** *Entropy and Information Theory*, 2nd ed., Springer, doi 10.1007/978-1-4419-7970-4; ISBN 978-1-4419-7969-8 (print), 978-1-4419-7970-4 (electronic). A careful general-alphabet development of entropy and mutual information, including the partition definition and the divergence form. Cited as a modern monograph, not as a source of A6.

**Aczél, Forte and Ng (1974),** doi 10.2307/1426210, and **Csiszár (2008),** doi 10.3390/e10030261, already cited in the representation note, remain the finite-law uniqueness sources. Csiszár surveys axiomatic characterizations. Neither paper extends that uniqueness to differential entropy, and this note does not do so either.

## 4. Definitions and conditions

**Spaces.** Let \(X:\Omega\to\mathcal{X}\) and \(Y:\Omega\to\mathcal{Y}\) be random variables on a probability space, with \(\mathcal{X}\) and \(\mathcal{Y}\) standard Borel spaces (equivalently, Polish spaces with their Borel \(\sigma\)-algebras). This class includes every value space used in the repository: finite sets, \(\mathbb{R}^d\), and the usual path spaces. Standard Borel is a sufficient condition, used so that finite measurable partitions of the value space capture the finite sub-\(\sigma\)-algebras, and so that regular conditionals exist when they are needed. It is not claimed to be the most general setting in which the identities can be written.

**Finite measurable partitions.** A finite measurable partition \(\alpha=\{A_1,\dots,A_n\}\) of \(\mathcal{X}\) is a finite collection of pairwise disjoint Borel sets whose union is \(\mathcal{X}\). The quantized variable \(X_\alpha\) is the finite-valued random variable that names the unique cell containing \(X\). The same applies to a partition \(\beta\) of \(\mathcal{Y}\) and to \(Y_\beta\). Mutual information of the pair \((X_\alpha,Y_\beta)\) is ordinary finite-law Shannon mutual information, in nats,
\[
I(X_\alpha;Y_\beta)=\sum_{i,j}\mathbb{P}(X\in A_i,Y\in B_j)\log\frac{\mathbb{P}(X\in A_i,Y\in B_j)}{\mathbb{P}(X\in A_i)\,\mathbb{P}(Y\in B_j)},
\]
with the usual convention \(0\log 0=0\).

**Kullback–Leibler form.** For any two probability measures \(P\) and \(Q\) on the same \(\sigma\)-algebra, \(D_{\mathrm{KL}}(P\|Q)\in[0,\infty]\) is \(\int\log(dP/dQ)\,dP\) when \(P\ll Q\), and is \(+\infty\) otherwise. The mutual information of a general pair is defined to be
\[
I(X;Y):=D_{\mathrm{KL}}\bigl(P_{X,Y}\big\|P_X\otimes P_Y\bigr)\in[0,\infty].
\]
This is always defined. It is finite if and only if \(P_{X,Y}\ll P_X\otimes P_Y\) and the integral is finite. When the joint and the margins have densities \(f_{XY}\), \(f_X\), and \(f_Y\) with respect to a common product measure (Lebesgue measure on \(\mathbb{R}^{d}\times\mathbb{R}^{e}\), for the plants in this repository), finiteness is the condition
\[
\int f_{XY}\log\frac{f_{XY}}{f_X f_Y}<\infty,
\]
and the integral equals \(I(X;Y)\). A nondegenerate jointly Gaussian pair with correlation \(|\rho|<1\) satisfies the condition; a perfectly correlated continuous pair has \(I=\infty\).

**The memory stock.** When the pair is a memory \(M_t\) and a world path \(X^t\), A6's coordinate is \(I(M_t;X^t)\), provided that number is finite. Path spaces of the usual kind are standard Borel, so the definition applies.

## 5. The Gelfand–Yaglom–Dobrushin theorem, and the passage to the limit

**Theorem (KNOWN: Gelfand–Yaglom–Dobrushin, Pinsker).** In the setting of §4,
\[
I(X;Y)=\sup_{\alpha,\beta} I(X_\alpha;Y_\beta),
\]
the supremum running over all finite measurable partitions of the two value spaces. Equivalently, the supremum runs over finite-valued measurable functions of \(X\) and of \(Y\). When \(P_{X,Y}\ll P_X\otimes P_Y\), the supremum equals the integral of the information density; otherwise both sides are \(+\infty\).

This is the identification the rest of the note uses. It is not re-proved here. The sources are Gelfand and Yaglom 1957, Dobrushin 1959, and Pinsker 1964, as cited in §3; Cover and Thomas §8.5 and Gray 2011 are the textbook and monograph forms.

**Finite alphabets (ELEMENTARY).** If \(\mathcal{X}\) and \(\mathcal{Y}\) are finite, the identity partitions attain the supremum, so \(I(X;Y)\) equals the finite-law mutual information already in A6. A coarser pair of partitions gives a smaller or equal value, by the data-processing inequality. The extension is conservative: it does not change any finite-law value.

**Monotone refinement (ELEMENTARY).** If \(\alpha'\) refines \(\alpha\) and \(\beta'\) refines \(\beta\), then \(I(X_{\alpha'};Y_{\beta'})\ge I(X_\alpha;Y_\beta)\). Along a nested sequence the discrete mutual informations are nondecreasing, and they are bounded above by \(I(X;Y)\).

**Generating sequences (KNOWN).** The supremum is a supremum, not necessarily a maximum: a genuine continuum pair need not have any finite partition that attains \(I(X;Y)\). If \((\alpha_n)\) and \((\beta_n)\) are nested sequences whose generated \(\sigma\)-algebras increase to \(\sigma(X)\) and \(\sigma(Y)\) (modulo null sets), then
\[
I(X_{\alpha_n};Y_{\beta_n})\uparrow I(X;Y).
\]
Equal-width or quantile bins on \(\mathbb{R}^d\) are a generating family under the usual regularity (the cells generate the Borel \(\sigma\)-algebra). A sequence of partitions that leaves a region of positive mass unrefined need not reach the supremum. The general statement in this note is the supremum; convergence of a named sequence is a further claim, and is stated only when the generating condition (or a regularity condition such as Cover and Thomas Theorem 8.3.1) is met.

**Unrestricted limits need not pass inside the functional (KNOWN: Dobrushin 1960).** If a sequence of joint laws converges weakly to \(P_{X,Y}\), the mutual informations need not converge to \(I(X;Y)\). Mutual information is lower semi-continuous with respect to weak convergence, and a passage to the limit in general requires further conditions, which Dobrushin 1960 states. This note does not claim that every convenient approximation of a joint law has mutual information close to \(I(X;Y)\). The partition supremum, and the monotone limit along a generating nested sequence, remain valid.

**Independence (KNOWN, and a genuine biconditional).** \(I(X;Y)=0\) if and only if \(P_{X,Y}=P_X\otimes P_Y\), that is, if and only if \(X\) and \(Y\) are independent. This is the standard identifiability of Kullback–Leibler divergence: \(D_{\mathrm{KL}}(P\|Q)=0\) if and only if \(P=Q\). It holds for general alphabets, not only for finite ones. The biconditional is recorded explicitly because an earlier finite-state heat-floor draft used "if and only if" for a positivity statement that holds in only one direction once the world has three or more states. That error is not repeated here: the independence statement is two-sided, and the generating-sequence limit is not written as a biconditional without the generating hypothesis.

## 6. Differential entropy does not pass to the limit; mutual information does

**KNOWN (Cover and Thomas, Theorem 8.3.1 and §8.5).** If \(X\) has a Riemann-integrable density and \(h(X)\) is finite, the Shannon entropy of the bin-width-\(\Delta\) quantization diverges:
\[
H(X^\Delta)=h(X)-\log\Delta+o(1)\qquad(\Delta\to 0).
\]
The same expansion holds jointly, so the divergent \(-\log\Delta\) terms cancel in the mutual information, and
\[
I(X^\Delta;Y^\Delta)\to h(X)+h(Y)-h(X,Y)=I(X;Y)
\]
when the joint density meets the same kind of regularity and the differential entropies are finite. That is why a differential mutual information can be the limit of discrete mutual informations even though a differential entropy is not the limit of discrete entropies.

This is the precise obstruction to extending the Aczél–Forte–Ng uniqueness theorem from Shannon entropy to differential entropy. Differential entropy can be negative (a uniform law on an interval of length less than one). It changes by \(\log|a|\) under the map \(x\mapsto ax\) (Cover and Thomas, Theorem 8.6.4). Shannon entropy of a finite law is nonnegative and is invariant under relabelling. The two functionals do not share the same axioms, and this note does not invent a substitute uniqueness theorem for \(h\). What is used as the memory coordinate is mutual information, which is nonnegative, invariant under invertible Borel relabelling of either variable, and equal to the partition supremum.

## 7. What this does for A6 and Theorem R1

**The extension of A6 (PROVED in-model, as a packaging of known identifications).** Under the conditions of §4, and when \(I(M_t;X^t)\) is finite, A6's memory coordinate is the Gelfand–Yaglom–Dobrushin mutual information \(I(M_t;X^t)\). That is:

- on a finite alphabet, the finite-law Shannon mutual information already characterized by A6;
- when the relevant densities exist and the integral is finite, the differential mutual information already used for the Gaussian plants;
- in general, the supremum of discrete mutual informations over finite measurable partitions, equivalently the Kullback–Leibler form of §4.

The finite-law uniqueness theorem is not re-proved and is not extended. The choice of stock rather than predictive or directed information is not re-opened. The extension is only the domain of the same functional.

**Theorem R1 is unchanged (ELEMENTARY given the extension).** Theorem R1 assumes A1–A7, a product of at least three essential intervals, and closed contour sets. It concludes that a continuous cost representing the preorder is \(C=a(\sum p_i z_i)+b\) with one \(a>0\) and one real \(b\). A finite mutual information takes values in the interval \([0,\infty)\). When that coordinate is essential, it is one of the interval coordinates the theorem already uses. Nonnegative prices still need A8. The integer layer count \(hK\) still needs the extra separability assumption the representation note states and does not prove. The coordinate list is still an assumption: A6 fixes only which information is the memory coordinate. The five-term display in THEORY §3 is still not derived from the axioms alone.

**The infinite case is a stated boundary, not a loophole in the definition.** Gelfand–Yaglom–Dobrushin mutual information is allowed to be \(+\infty\). Theorem R1 is not: its coordinates are real. If \(I(M_t;X^t)=\infty\), the memory coordinate is not an interval coordinate in the sense of R1, and the representation is not applied. A perfectly observed continuous path is the typical example. No design with infinite mutual information at a positive price \(\kappa\) can be a minimizer of a finite cost, but that remark is not needed for the representation and is not stated as a theorem.

**R1\(^\prime\)** in `theory/ACTING_DERIVATION_2026-11-22.md` uses A6 in the same scope. The extension above applies to that use of A6 as well, at \(b=0\) and under the same finiteness condition. The acting derivation itself is not re-opened.

## 8. What carries from the finite-law Shannon results

The following properties of finite-law mutual information remain valid for the Gelfand–Yaglom–Dobrushin functional, under the conditions of §4, and are **KNOWN**: nonnegativity; symmetry \(I(X;Y)=I(Y;X)\); the chain rule; the data-processing inequality; \(I(X;Y)=0\) if and only if \(X\) and \(Y\) are independent; and the Kullback–Leibler representation. Any result in the repository whose proof uses only those properties, and not a finite alphabet in an essential way, therefore holds for continuous laws under the same conditions, with its finite-law statement unchanged. The information-floor pattern of `theory/SHANNON_2026-11-21.md` (a quantity fixed by the task, a converse, a formula from the world's statistics) is of that kind once the quantity is this mutual information.

The following do *not* automatically extend, and this note does not extend them:

- any uniqueness theorem for entropy itself, including Aczél–Forte–Ng, Faddeev grouping, and the continuity-for-\(n=2\) isolation of Shannon entropy;
- any bound that uses a finite alphabet essentially, such as Fano's inequality in the form that contains \(\log|\mathcal{X}|\), or a state-counting layer cap;
- any difference of two possibly infinite information quantities (in particular \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\) when either term is infinite);
- the net learning rate \(I_{\mathrm{alt}}\) of the heat notes, which is a flow of information, not the stock \(I(M_t;X^t)\).

The last point is the gross-versus-net distinction already flagged in §0. Proposition JP-heat bounds memory-bath heat by the *net* information flow of memory jumps. The present extension is about the *stock* that A6 prices. Both are mutual-information quantities in their own places. They are not the same number, and this note does not substitute one for the other.

## 9. Checks

`theory/continuous_a6_checks/continuous_a6_checks.py` checks, in nats:

- on a finite alphabet, the identity partition attains the discrete mutual information, and a coarser partition does not exceed it;
- independence: a product joint law has \(I=0\) exactly, for a finite alphabet and for every quantile quantization of an uncorrelated Gaussian pair;
- a standard normal \(X\) and the sign \(Y=1_{\{X>0\}}\) have \(I(X;Y)=\log 2\), and a partition of \(X\) that splits only at zero already attains it;
- \(Y=X\) on a finite alphabet gives \(I=H(X)\); \(Y=X\) uniform on the unit interval, quantized into \(n\) equal bins, gives \(I=\log n\), which diverges;
- for bivariate Gaussians, the quantile-bin mutual information is strictly below the closed form \(-\tfrac12\log(1-\rho^2)\) at every finite \(n\) tested with \(0<|\rho|<1\), increases with \(n\), and closes the gap as the bins refine;
- the Shannon entropy of a quantized Gaussian grows like \(-\log\Delta\), while the mutual information stays bounded, which is the cancellation of §6;
- every DOI cited in this note appears in `theory/continuous_a6_checks/crossref.out` as HTTP 200, except Pinsker 1964, which is recorded there as having no Crossref work record.

The run used for this note reports FAILS 0. The checks are identities and numerical evaluations of named closed forms. They are not evidence about a real system.

## 10. What remains open

- A uniqueness theorem for differential entropy, or for mutual information, that would play the role Aczél, Forte and Ng play for finite-law entropy. Not attempted, and not needed for the coordinate identification.
- The representation when \(I=\infty\). Excluded, not filled.
- Continuous versions of results that use a finite alphabet essentially (Fano with \(\log|\mathcal{X}|\), state counts). Not attempted.
- Directed information and predictive information as continuous functionals, including differences that might be infinite. A6's choice of the gross stock is unchanged; those functionals remain different.
- Everything already open in the heat-floor notes (a closed form of \(\Phi_X\) for a general world, attainability outside the telegraph, dual control) is unchanged by this identification.

## References

Resolved on the Crossref API, 23 November 2026, America/New_York, except Pinsker 1964, for which Crossref has no work record. The record is `theory/continuous_a6_checks/crossref.out`.

- Gelfand, I. M. and Yaglom, A. M. 1957. Calculation of the amount of information about a random function contained in another such function. English translation, *Amer. Math. Soc. Transl. Ser. 2* 12:199–246, 1959. doi 10.1090/trans2/012/09. Original: *Uspekhi Mat. Nauk* 12(1):3–52, 1957.
- Dobrushin, R. L. 1959. General formulation of Shannon's main theorem in information theory. English translation, *Amer. Math. Soc. Transl. Ser. 2* 33:323–438, 1963. doi 10.1090/trans2/033/11. Original: *Uspekhi Mat. Nauk* 14(6):3–104, 1959.
- Dobrushin, R. L. 1960. Passage to the Limit under the Information and Entropy Signs. *Theory Probab. Appl.* 5:25–32. doi 10.1137/1105003.
- Pinsker, M. S. 1964. *Information and Information Stability of Random Variables and Processes*. Holden-Day, San Francisco. Translated and edited by Amiel Feinstein from the 1960 Russian monograph. No Crossref work record and no ISBN on the 1964 edition, as recorded in `theory/continuous_a6_checks/crossref.out`.
- Kolmogorov, A. N. 1956. On the Shannon theory of information transmission in the case of continuous signals. *IRE Trans. Inf. Theory* 2:102–108. doi 10.1109/TIT.1956.1056823.
- Kolmogorov, A. N. 1963. Theory of transmission of information. *Amer. Math. Soc. Transl. Ser. 2* 33:291–321. doi 10.1090/trans2/033/10.
- Cover, T. M. and Thomas, J. A. *Elements of Information Theory*, 2nd ed., Wiley. Crossref issued 7 April 2005, print 16 September 2005. doi 10.1002/047174882X. ISBN 978-0-471-24195-9 (print), 978-0-471-74882-3 (electronic). Commonly cited as 2006.
- Gray, R. M. 2011. *Entropy and Information Theory*, 2nd ed., Springer. doi 10.1007/978-1-4419-7970-4. ISBN 978-1-4419-7969-8 (print), 978-1-4419-7970-4 (electronic).
- Aczél, J., Forte, B. and Ng, C. T. 1974. Why the Shannon and Hartley entropies are 'natural'. *Adv. Appl. Probab.* 6:131–146. doi 10.2307/1426210.
- Csiszár, I. 2008. Axiomatic Characterizations of Information Measures. *Entropy* 10:261–273. doi 10.3390/e10030261.
