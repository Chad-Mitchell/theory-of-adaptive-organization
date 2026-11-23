# The transport channel: can a trapped carrier's barrier against leaving exceed its gravitating mass? And A2 from stability of matter

*Monday 23 November 2026 (America/New_York). A probe, not a change to `THEORY.md`, `CORE.md`, `theory/SCALE_ENDS.md`, or the hypothesis sentence. Written against `main` `b611a68` (PR #244, T65). Open-work row T66. It takes up the "strongest next angle" of the independent review of PR #244 (`/workspace/gtao/reviews-indep-2026-11-23/PR244.md`, outside the repository): bound \(\beta_{\rm transport}\), the barrier against a record's carrier leaving its region relative to the record's gravitating mass, using carriers held by traps of known mass, and replace T65's input A2 with a proved stability-of-matter statement for Coulomb systems. Every DOI below was resolved on the Crossref API the same day (`theory/transport_barrier_checks/crossref.out`). Opened this session: Lieb's 2004 review (arXiv math-ph/0401004, §3), and the abstracts of Lieb–Yau 1988 and Lieb 1984. Every other source is cited for what is standard about it, and a statement taken from an abstract or a later paper says so. A check script, not a simulation of a real system. Not yet independently reviewed.*

Labels follow T64 and T65. **PROVED (in-model)** is a result inside a named class, given the stated inputs. **KNOWN** is published and credited, only for what that source states. **ELEMENTARY** is a direct consequence of a proved or known inequality. **NUMERICAL** is a computed value of a stated finite problem. **ASSUMED INPUT** is a physical premise brought in from outside the cost of judgment. **SKETCH** is an estimate, not a result. **CONJECTURE** is a named bet. **OPEN** is not derived.

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

## 0. Bottom line

**Question (T65 §5, §11).** A record held in a region is erased just as well by its carrier leaving as by its carrier being destroyed (T65 Lemma C). Can the barrier against leaving be much larger than the record's gravitating mass-energy, \(\beta_{\rm transport}\gg1\), while the record stays locally readable? And must the trap's own mass be charged to the record?

**Plain answer.** In every weakly coupled class checked here, no: \(\beta_{\rm transport}\) is small, and it is small because the trap's mass has to be charged. At strong coupling a light trap can hold a heavy carrier with \(\beta\gg1\) against the carrier escaping. But then the carrier and its trap move together as one free object, and the question comes back one level up: what holds that object in the region? That regress is not closed here (**OPEN**). Separately, for Coulomb matter T65's input A2 can now be replaced by a proved theorem (Lieb–Yau 1988), with a stated constant.

1. **The trap must be charged (ELEMENTARY).** The hoop input counts every gravitating joule in the region, the trap's included. So \(E_{\rm rec}\) is the record's share of the carrier plus whatever holds it. Without that charge the answer is empty: both occupations of a fermion zero mode have the same energy, so a zero-mode record "costs" nothing and its \(\beta\) is infinite as an artefact.
2. **Lemma Z: the barrier against leaving is at most the carrier's rest energy (PROVED in-model, given input Z0).** An occupation record ("this trap holds a carrier") has two erase routes: the carrier leaves (barrier \(I\), its binding) or a pair is made, the carrier binds and its antiparticle escapes (\(2mc^2-I\)). So the barrier is at most \(\min(I,2mc^2-I)\le mc^2\). For a bound level \(E_b\) inside the gap the barrier is \(mc^2-|E_b|\), largest at the mid-gap zero mode.
3. **Lemma P: a free trap gives no transport barrier (PROVED).** A carrier and its trap that are not pinned translate together at constant energy. Their barrier against leaving the region is zero. A trap raises \(\beta_{\rm transport}\) of a region record only if something pins it, and the pin is the next carrier in line.
4. **Topological traps at weak coupling: small \(\beta\) (PROVED in-model, KNOWN inputs).**
   - *Monopole.* For fermions on a monopole (Jackiw–Rebbi; Callias), the Bogomolny bound \(M\ge4\pi vk/g\) and the zero-mode count give \(\beta_{\rm unbind}\le n_f\,y\,g\,S_t/(4\pi)\), with \(y=m_f/v\), \(S_t\) the zero modes per unit charge and \(n_f\) the number of fermion flavors. With one flavor that is 0.052 for an isospinor and 0.103 for an isovector at \(g=0.65\), \(y=1\).
   - *String loop.* For zero modes on a string loop (Jackiw–Rossi; Witten), the tension bound \(\mu\ge2\pi v^2|n|\) gives \(\beta\le n_f\bigl(y^2/(4\pi^2)+y/(2\pi vL)\bigr)\), which is 0.0253 plus an end term at \(y=1\) with one flavor. Many flavors raise both bounds in proportion, the species problem again.
5. **Coulomb traps: small \(\beta\) (PROVED in-model, KNOWN inputs).** Electrons held by nuclei: each electron's barrier is at most \(m_ec^2\) (Lemma Z). A nucleus binds fewer than \(2z+1\) electrons, and a molecule fewer than \(2Z+K\) (Lieb 1984). Nuclear mass per unit charge is at least \(m_p-8.79\) MeV. So \(\beta\le1.10\times10^{-3}\) for atoms and \(\le1.65\times10^{-3}\) for any molecule or solid. Actual values are far smaller: \(1.45\times10^{-8}\) for hydrogen and \(6.0\times10^{-7}\) for the 132 keV 1s electron of U\(^{91+}\). T65's field-energy-only sketch (18.1) does not survive once the well's source charges are charged their rest mass.
6. **Strong coupling: a light trap can hold a heavy carrier (NUMERICAL, mean field).**
   - *The bag.* In a fermion bag, a scalar field that makes the fermion light inside (Friedberg–Lee; the SLAC bag of Bardeen et al.), a variational trial gives \(\beta_{\rm unbind}\ge0.40\), \(7.46\) and \(45.2\) at Yukawa coupling \(g=10,100,1000\). It grows without bound as \(g\to\infty\).
   - *Caveats.* This holds only where \(g^2/4\pi\gg1\), and there mean field has no controlled justification.
   - *What it does not settle.* The bag is a free object (Lemma P), and Lemma Z caps the barrier of whatever pins it by the bag's own rest energy. So a large \(\beta_{\rm transport}\) for a region record needs a pin that binds an object by nearly the object's whole rest energy while weighing less per record than that object, at the last level. That is the same strong-binding pattern one level up (**OPEN**).
7. **Self-gravity as the pin (SKETCH).** Objects held in the region by its own gravity escape over \(GMm/R\le mc^2/2\) (hoop input), so \(\beta\le1/2\).
8. **A2 replaced for Coulomb matter (PROVED in-model, from KNOWN Lieb–Yau 1988).**
   - *Constant.* For electrons (two spin states) with kinetic energy \(\sqrt{p^2c^2+m^2c^4}\), and static nuclei of charge \(z\le59\), interactions cancel at most a fraction \(\kappa_{\rm int}=0.686\) of the localization energy. The fraction reaches \(1-0.0027\) at \(z=87\), and nothing is covered above that.
   - *Cap.* T65's cap holds for electrons with this constant: \(1.66\times10^{52}\) at 1 m, a factor 2.84 above the free-carrier value.
   - *Bosons.* Charged bosons have no such theorem (they are unstable in the relativistic case), so A2 stays an input for them.

**What the cost adds.** It adds nothing new to the bounds themselves; they come from the mass bounds, index theorems and stability theorems cited. The cost reads off the design. Put record levels at mid-gap (zero modes give the largest two-sided barrier per unit of carrier mass, and an index theorem supplies them for free). Share each trap among as many records as its index allows. Buy no barrier above \(B^*\). This is the model's implication, stated plainly. Nothing here derives general relativity, quantum mechanics, or holography.

## 1. What is already in the repository

- T65 (`theory/BARRIER_MASS_FIELD_THEORY_2026-11-23.md`, §5, line 65) states Lemma C and moves A1 to the transport channel. Line 67 gives the two transport sketches (18.1 field-only; \(1.96\times10^{-6}\) with one electron as source). Line 77 states A2 as an input, citing Lieb–Yau 1988 for context only. §11 lists \(\beta_{\rm transport}\) and A2 as OPEN.
- T64 (`theory/GRAVITY_BARRIER_PROBE_2026-11-23.md`) states A1 and the hoop input. Its ordinary-matter values (\(10^{-10}\) to \(10^{-16}\)) are illustrative.
- Grep before writing: "Jackiw" appears only in T65 (the vacuum-periodicity paper, not the zero-mode paper). "Callias", "vorton", "Bogomolny", "Friedberg", "SLAC bag", "MIT bag", "Lieb–Thirring", "Dyson–Lenard" and "zero mode" in the soliton sense do not appear. "Lieb–Yau" appears only in T65 and its OPEN_WORK row. "T66" appears only as unrelated identifiers in `tests/C3/data/`.

## 2. Prior art (credited; §10 says what, if anything, is not found elsewhere)

- **Fermion zero modes.** Jackiw and Rebbi 1976, *Phys. Rev. D* 13:3398, doi 10.1103/PhysRevD.13.3398 (zero modes and fermion number \(\pm\tfrac12\) on kinks and monopoles). Callias 1978, *Commun. Math. Phys.* 62:213, doi 10.1007/BF01202525 (index theorem on open spaces). The count per unit charge, \(\tfrac12\sum_w{\rm sign}(w\cdot\phi)\,w\cdot g\), equals \(\sum_m|m|\) for isospin \(t\): 1, 2, 4, 6 for \(t=\tfrac12,1,\tfrac32,2\). That count is taken as stated in later literature (not opened in the original). Vortices: Jackiw and Rossi 1981, *Nucl. Phys. B* 190:681, doi 10.1016/0550-3213(81)90044-4; the index \(|n|\) is from E. Weinberg 1981, *Phys. Rev. D* 24:2669, doi 10.1103/PhysRevD.24.2669. In 3+1 dimensions these become chiral modes moving along the string: Witten 1985, *Nucl. Phys. B* 249:557, doi 10.1016/0550-3213(85)90022-7. Loops held open by their carriers: Davis and Shellard 1989, *Nucl. Phys. B* 323:209, doi 10.1016/0550-3213(89)90594-4.
- **Trap masses.** Monopoles: 't Hooft 1974, *Nucl. Phys. B* 79:276, doi 10.1016/0550-3213(74)90486-6. The bound \(M\ge4\pi v|k|/g\): Bogomolny 1976 (*Sov. J. Nucl. Phys.* 24:449; no Crossref record). It is saturated by Prasad and Sommerfield 1975, *Phys. Rev. Lett.* 35:760, doi 10.1103/PhysRevLett.35.760 (script §3 integrates their solution to 1.00000000). Strings: Nielsen and Olesen 1973, *Nucl. Phys. B* 61:45, doi 10.1016/0550-3213(73)90350-7. The bound \(\mu\ge2\pi v^2|n|\) (for \(|\phi|\to v\), kinetic term \(|D\phi|^2\)) is Bogomolny's, and script §4 integrates the BPS equations for \(n=1,2\). Nuclear binding per nucleon is at most 8.79 MeV (Ni-62): Wang et al. 2021, AME 2020, *Chinese Phys. C* 45:030003, doi 10.1088/1674-1137/abddaf.
- **Bags.** Chodos et al. 1974, *Phys. Rev. D* 9:3471, doi 10.1103/PhysRevD.9.3471 (MIT bag; lowest mode \(x=2.0428\)). Bardeen, Chanowitz, Drell, Weinstein and Yan 1975, *Phys. Rev. D* 11:1094, doi 10.1103/PhysRevD.11.1094: the SLAC bag, built for heavy quarks strongly bound into light hadrons, which is exactly the pattern of §6. Friedberg and Lee 1977, *Phys. Rev. D* 15:1694, doi 10.1103/PhysRevD.15.1694: fermion nontopological solitons.
- **Stability of matter.** Dyson 1967, *J. Math. Phys.* 8:423, doi 10.1063/1.1705209, and Lenard and Dyson 1968, *J. Math. Phys.* 9:698, doi 10.1063/1.1664631: nonrelativistic stability of the second kind, energy at least \(-C(N+K)\) for fermion electrons (Pauli essential). Lieb and Thirring 1975, *Phys. Rev. Lett.* 35:687, doi 10.1103/PhysRevLett.35.687: the kinetic-energy inequality and a short proof with a better constant. Lieb and Yau 1988, *Commun. Math. Phys.* 118:177, doi 10.1007/BF01218577, abstract: electrons with \(q\) spin states, fixed nuclei, kinetic energy \(\sqrt{p^2c^2+m^2c^4}-mc^2\). Stability holds in the many-body case if \(z\alpha\le2/\pi\) and \(\alpha<1/(47q)\). There is a critical \(\alpha_c\le128/(15\pi)\) above which instability occurs for every \(z>0\) with enough nuclei. Lieb 2004 (arXiv math-ph/0401004, §3, opened) restates this as \(z\alpha\le2/\pi\), \(\alpha<1/94\) for \(H_N=\sum|p_i|+\alpha V_c\). It notes the replacement of \(\sqrt{p^2+1}\) by \(|p|\) changes energies by at most a constant times \(N\), and that charged bosons are unstable for every \(z,\alpha>0\). Magnetic fields add conditions: Lieb, Loss and Solovej 1995, *Phys. Rev. Lett.* 75:985, doi 10.1103/PhysRevLett.75.985 (scope only). Lieb and Yau 1987, *Commun. Math. Phys.* 112:147, doi 10.1007/BF01217684, is the Chandrasekhar comparison already credited in T65.
- **Ionization.** Lieb 1984, *Phys. Rev. A* 29:3018, doi 10.1103/PhysRevA.29.3018 (abstract, opened). The number of negative particles bound to an atom of charge \(z\) satisfies \(N_c<2z+1\), and \(N_c<2Z+K\) for \(K\) atoms of total charge \(Z\). The particles may be a mixture of species and statistics plays no role. It holds for static nuclei, with relativistic or nonrelativistic kinetic energy and with magnetic fields.
- **Count under gravity.** Cohen, Kaplan and Nelson 1999, *Phys. Rev. Lett.* 82:4971, doi 10.1103/PhysRevLett.82.4971, as in T65.

## 3. Set-up: what is charged, and two lemmas

**Record and charge.** A record is "this trap (or region) holds a carrier" versus "it does not", read by a local gauge-invariant density (fermion number or charge). Following T64 and T65, \(\beta=B/E_{\rm rec}\), where \(E_{\rm rec}\) is the record's share of the gravitating energy of everything that holds it, averaged over its two states: \(E_{\rm rec}\ge s_{\rm trap}+\tfrac12(E_c-I)\). Here \(s_{\rm trap}\) is the trap's mass divided by the records it holds, \(E_c\) is the carrier's free rest energy, and \(I\) is its binding. Charging the trap is not optional, because the hoop input bounds the region's total energy (§0 item 1).

**Input Z0 (ASSUMED INPUT).** In the thermally activated reading used by T64 and T65, the activation energy of a channel is the energy of its end state when nothing higher lies on the way. For pair creation of an elementary carrier this is the threshold, which is why thermal pair densities go as \(e^{-mc^2/kT}\) per particle. For solitonic or composite carriers the pair route may have an extra barrier. Lemma Z is then not claimed.

**Lemma Z (PROVED in-model, given Z0).** For an occupation record with a carrier of free rest energy \(E_c\) bound by \(I\in[0,2E_c]\), the barrier is at most \(\min(I,\,2E_c-I)\le E_c\). For a bound level \(E_b\in(-E_c,E_c)\) it is at most \(E_c-|E_b|\), with the maximum \(E_c\) at \(E_b=0\). *Proof.* The occupied state is erased by unbinding, whose end state lies \(I\) higher. The empty state is erased by creating a pair, binding the carrier and sending the antiparticle away: end state \(2E_c-I\) higher. Any trap or reservoir for the antiparticle only lowers this. The record needs both states kept, so its barrier is the smaller. ∎ Script §1.

**Lemma P (PROVED).** If the dynamics is translation invariant and a composite (carrier plus trap) is not bound to anything else, the rigid translation of the composite is a path of constant energy. Its barrier against leaving any region is zero. *Proof.* Energy is invariant under the symmetry, so it is constant along the path. ∎ Script §2 checks a lattice lump. Consequence: a trap raises a region record's \(\beta_{\rm transport}\) only if it is pinned. Pinning is an occupation record of the composite in its pin, to which Lemma Z applies with the composite's rest energy.

**Proposition R (ELEMENTARY, from Z and P).** Let \(X\) be the outermost free composite that carries the record (carrier plus traps, pinned in the region by a pin of share \(s_{\rm pin}\) and binding \(I_{\rm pin}\)). Then
\[
\beta_{\rm transport}\ \le\ \frac{\min(I_{\rm pin},\,2E_X-I_{\rm pin})}{s_{\rm pin}+\tfrac12(E_X-I_{\rm pin})}.
\]
Both record states have nonnegative energy (\(s_{\rm pin}\ge0\) empty, \(s_{\rm pin}+E_X-I_{\rm pin}\ge0\) occupied). So \(\beta_{\rm transport}\gg1\) needs both to be \(\ll E_X\): the pin, and the pin with \(X\) bound in it, must each weigh far less per record than \(X\) does when free. That is, a light pin must bind \(X\) by nearly all of \(X\)'s rest energy. If the bound pair (\(X\) plus pin) is itself free, Lemma P applies again one level up.

## 4. Topological traps at weak coupling

**Proposition M (PROVED in-model; KNOWN inputs Bogomolny, Callias).** Take an SU(2) gauge theory with adjoint Higgs \(\phi^a\to v\), \(m_W=gv\), and fermions in isospin \(t\) that get their mass only from the Higgs, with largest asymptotic mass \(m_f=yv\). Records are occupations of the fermion zero modes of a charge-\(k\) monopole. Then \(B\le m_f\) per record (Lemma Z; zero modes sit at mid-gap, where the bound is attained). With \(n_f\) flavors the monopole holds \(n_fkS_t\) zero-mode records, with \(S_t=\sum_m|m|\), so the trap share is at least \((4\pi v|k|/g)/(n_fkS_t)\). So
\[
\beta_{\rm unbind}\ \le\ \frac{n_f\,y\,g\,S_t}{4\pi}:\qquad 0.052\ (t=\tfrac12),\quad 0.103\ (t=1)\quad\text{at } g=0.65,\ y=1,\ n_f=1 .
\]
In the regime where a monopole is a controlled semiclassical object (\(g^2/4\pi\ll1\)) and the Yukawa coupling is perturbative, this is \(\ll1\). The bound grows as \(t^3\) through \(S_t\) and \(y\) (largest weight), so very large representations at very small \(g\) are not excluded by it. Whether such a theory keeps its zero modes and stays weakly coupled is **OPEN**. Non-zero bound levels add records with smaller barriers (\(m_f-|E_b|\)) and do not raise the per-record maximum. And by Lemma P a free monopole gives no transport barrier at all. This bound is on unbinding only.

**Proposition S (PROVED in-model; KNOWN inputs Bogomolny, Jackiw–Rossi, Weinberg, Witten).** Take an abelian Higgs string with winding \(n\), \(|\phi|\to v\), tension \(\mu\ge2\pi v^2|n|\), and \(|n|\) chiral zero-mode branches of a fermion with asymptotic mass \(m_f=yv\). On a closed loop of length \(L\) the bound modes have energies \(2\pi\hbar c\,j/L<m_f\), at most \(Lm_f/(2\pi\hbar c)+1\) per branch, each with barrier at most \(m_f\). With the loop's mass shared over the records it holds,
\[
\beta\ \le\ n_f\Bigl(\frac{y^2}{4\pi^2}+\frac{y}{2\pi vL}\Bigr)\qquad(0.0253\ \text{plus the end term at } y=1,\ n_f=1),
\]
independent of \(n\), with \(n_f\) fermion flavors. A loop with no current shrinks with no barrier, releasing its modes (the analogue of T65 Lemma W). Loops held open by their carriers (vortons; Davis–Shellard 1989) carry carrier energy comparable to \(\mu L\), which only lowers \(\beta\) (SKETCH). Straight infinite strings are not local records.

## 5. Coulomb traps

**Proposition Q (PROVED in-model; KNOWN inputs Lieb 1984, AME 2020).** Electrons held by nuclei (static nuclei, any kinetic energy Lieb 1984 covers). Per electron \(B\le m_ec^2\) by Lemma Z. A point-nucleus Dirac 1s level is bound by \(m_ec^2(1-\sqrt{1-(z\alpha)^2})<m_ec^2\) for every \(z\alpha\le1\), so the leave route alone already obeys this. Records per nucleus are fewer than \(2z+1\), and per unit of nuclear charge in any molecule or solid fewer than \(2+K/Z\le3\). Nuclear mass per unit charge is at least \(A(m_p-8.79\ \text{MeV})/z\ge929.48\) MeV. Hence
\[
\beta\le\frac{2m_ec^2}{929.48\ \text{MeV}}=1.10\times10^{-3}\ \text{(atoms)},\qquad \beta\le1.65\times10^{-3}\ \text{(molecules, solids)}.
\]
Actual values (NUMERICAL, trap charged): hydrogen \(13.6\ \text{eV}/m_pc^2=1.45\times10^{-8}\). For U\(^{91+}\), the point-nucleus Dirac 1s binding is 132 keV against a 221.7 GeV nucleus, \(6.0\times10^{-7}\). A light positive trap is not available among stable particles (the positron annihilates its partner, a destruction channel). For a hypothetical light trap of charge \(Z\), the nonrelativistic hydrogenic estimate gives \(\beta\lesssim n(Z\alpha)^2/2\), which is \(\alpha^2=5.3\times10^{-5}\) at \(Z=1\), \(n=2\) (SKETCH, valid for \(Z\alpha\ll1\)). T65's field-only figure of 18.1 counted a well's field energy but not the rest mass of the charges that make it. Charged, the same well is a Coulomb trap and falls under this proposition.

## 6. Strong coupling: a light trap holding a heavy carrier

**Bag (NUMERICAL, mean field; KNOWN existence: Friedberg–Lee 1977; the SLAC bag, Bardeen et al. 1975).** A fermion of Yukawa coupling \(g\) to a scalar \(\sigma\) with \(U=\tfrac\lambda4(\sigma^2-\sigma_v^2)^2\) has mass \(m=g\sigma_v\) outside and is light where \(\sigma\to0\). The variational trial is \(\sigma=\sigma_v(1-e^{-r^2/R^2})\), \(R=0.9/\sigma_v\), \(\lambda=1\), with one valence fermion in the lowest Dirac \(s_{1/2}\) level, a classical \(\sigma\), and no Dirac sea. It gives a soliton energy \(E_{\rm trial}\) that bounds the true mean-field minimum from above. So \(\beta_{\rm unbind}=(m-E_1)/E_1\ge(m-E_{\rm trial})/E_{\rm trial}\): **0.40, 7.46, 45.2** at \(g=10,100,1000\) (\(g^2/4\pi=8,\ 796,\ 7.96\times10^{4}\)). The script's Dirac solver reproduces the bag limit \(x=2.0428\) from below. The record ("this bag holds fermion number one") is readable, and the trap is charged (the bag's whole energy is \(E_1\)). So the unbind channel can give \(\beta\gg1\) with the trap charged, but only at couplings where mean field has no controlled justification. Confinement in QCD is the extreme form: a colored carrier cannot leave at all, but color is not a gauge-invariant reading (T65 Lemma G), and the readable carrier is the hadron, which translates freely.

**What it settles and what it does not.** The bag translates (Lemma P). Pinning it is subject to Lemma Z with \(E_X=E_1\), and Proposition R then asks for a second light pin binding the bag by nearly \(E_1\). Whether such a tower can reach the region's scale, with records as occupations of distinct pinned cells (internal hops between cells are a transport route too), is the open form of A1 (**OPEN**).

## 7. Self-gravity as the pin (SKETCH)

If the region's own gravity holds its objects, an object of mass \(m\) escapes over \(GMm/R\). With the hoop input \(GM/(Rc^2)\le\tfrac12\) this is at most \(mc^2/2\), so \(\beta\le\tfrac12\) (Newtonian estimate; strong-field corrections and regions near collapse are outside scope, as in T65).

## 8. A2 from stability of matter (Coulomb case)

**Proposition LY (PROVED in-model, from KNOWN Lieb–Yau 1988).**
- *Setting.* \(N\) electrons with \(q=2\) spin states and \(K\) static nuclei of charges \(z_k\), Coulomb interaction \(\alpha V_c\) (all pairs, no self-energies), no magnetic field and no quantized field.
- *Statement.* For any \(\kappa\in(0,1]\) with \(\alpha/\kappa<1/94\) and \(z_k\alpha/\kappa\le2/\pi\) for every \(k\),
\[
\sum_i\sqrt{p_i^2c^2+m^2c^4}+\alpha V_c\ \ge\ (1-\kappa)\sum_i c|p_i| .
\]
- *Proof.* \(\sqrt{p^2c^2+m^2c^4}\ge c|p|\). Then \(\kappa\sum c|p_i|+\alpha V_c=\kappa\bigl[\sum c|p_i|+(\alpha/\kappa)V_c\bigr]\), and the bracket is Lieb–Yau's massless operator at fine-structure constant \(\alpha/\kappa\). It is stable under the stated conditions. Being homogeneous of degree \(-1\) under dilation of all coordinates, bounded below is the same as nonnegative. ∎
- *Constant.* A2 holds with \(\kappa_{\rm int}=0.686\) (any value above \(94\alpha=0.68595\)) for all \(z\le59\), and with \(\kappa_{\rm int}=\pi z_{\max}\alpha/2\) up to \(z=87\), where \(1-\kappa_{\rm int}=0.0027\). Above \(z=87\) it is not covered.
- *Consequence.* T65 Lemma L applies to the electrons' one-particle density matrix, \(0\le\gamma\le1\), \(g=2\). With nuclear rest masses only adding, the region's gravitating energy is at least \(0.314\,C_B\,2^{-1/3}N^{4/3}\hbar c/R\) for \(z\le59\). The cap of T65 Proposition 2 then holds for Coulomb matter with A2 replaced by a theorem: \(N\le1.66\times10^{52}\) at \(R=1\) m, a factor 2.84 above T65's free-carrier value (\(5.86\times10^{51}\)).

**Scope and the other theorems.** The constant comes from Lieb–Yau's sufficient condition \(\alpha<1/94\), not from the sharp critical value, which is not established here. Lieb–Loss–Siedentop (1996) improved the constants; the numbers are not quoted here because the paper was not opened. The nonrelativistic theorems (Dyson–Lenard; Lieb–Thirring) bound the energy below by \(-C(N+K)\) at fixed \(z_{\max}\). That says interactions cancel at most a small fraction of the rest energy, a rest-mass form of A2, but it does not control \(c|p|\), so it cannot give the \(N^{4/3}\) cap. Charged bosons are unstable in the relativistic case for every \(z,\alpha>0\) (Lieb 2004). So A2 cannot be replaced for them, and T65's boson-encoding condition stays an input. Magnetic fields and the quantized field (Lieb–Loss–Solovej 1995 and later) are outside this proposition.

## 9. The GTAO method, run explicitly

1. **The cost, with named terms.**
   \(J=\sum_i\bigl[c_{\rm err}\,\varepsilon_i+\lambda_G\,E_{{\rm rec},i}\bigr]+J_{\rm write}+J_{\rm read}\). The terms:
   - *Retention-loss term:* \(\varepsilon_i\approx\nu\tau e^{-B_{{\rm eff},i}/kT}\) with \(B_{\rm eff}=\min(B_{\rm destroy},B_{\rm unbind},B_{\rm pin})\) (T65 Lemma C, split here).
   - *Mass-energy term:* \(E_{\rm rec}\ge s_{\rm trap}+s_{\rm pin}+\tfrac12(E_c-I)\), with the trap charged (§3).
   - *Barrier constraint:* each channel's barrier is at most the rest energy of what moves (Lemma Z), and zero for a free composite (Lemma P).
   - *Class trap-mass floors:* Propositions M, S and Q.
   - *Localization term:* with Lieb–Yau's \(\kappa_{\rm int}\) for Coulomb matter (Proposition LY).
   - *Gravitational budget:* \(\sum E_{\rm rec}\le Rc^4/2G\) (hoop input), with multiplier \(\lambda_G\).
   - *Write and read terms:* as in T65.
2. **Its minimum.** Each record at \(B_{\rm eff}=B^*=kT\ln(\nu\tau/\tilde\varepsilon)\) (1.70 eV at 300 K, one year, \(10^{-9}\)). The least mass per record is \(B^*/\beta_{\max}(\text{class})\): at least 1.03 keV in the nuclear-trap class (actual atoms carry about a GeV per record). Count \(N^*=\min(\beta Rc^4/(2GkT\ln),\ N_{\rm loc})\), as in T65, with \(N_{\rm loc}\) now proved for Coulomb electrons.
3. **Read-off design.**
   - Place record levels at mid-gap: Lemma Z's two-sided barrier \(E_c-|E_b|\) is largest at a zero mode, and an index theorem supplies zero modes at no tuning cost.
   - Fill a trap's zero modes, so its mass is shared by as many records as its index allows.
   - Pin the outermost composite, since the free composite is the weakest channel (Lemma P).
   - Pay for no barrier above \(B^*\).
   - Where traps are heavy per record (all weakly coupled classes here), capacity is set by trap mass and localization, not by barrier.
4. **Scope.**
   - *Covered:* thermally activated erasure; flat space with the hoop limit as input; weakly coupled semiclassical solitons with BPS-type mass bounds; static nuclei; no magnetic or quantized field in Proposition LY; input Z0 for Lemma Z.
   - *Excluded:* tunneling, strongly coupled theories beyond the mean-field bag, regions near collapse, black holes, and any claim that \(\beta_{\rm transport}\) is bounded in general.

## 10. What is new, and what is not

- **Known:** zero modes and their counts (Jackiw–Rebbi; Callias; Jackiw–Rossi; Weinberg; Witten); the Bogomolny bounds and the Prasad–Sommerfield solution; bags (MIT, SLAC, Friedberg–Lee); stability of matter (Dyson–Lenard; Lieb–Thirring; Lieb–Yau); Lieb's ionization bound; nuclear masses.
- **Not found stated elsewhere (search not exhaustive):** the two-sided barrier bound (Lemma Z) as a cap on any occupation record's barrier by its carrier's rest energy; its use, with trap masses charged, to bound \(\beta\) for zero-mode records on monopoles and strings and for Coulomb-held electrons; the reduction (Proposition R) of A1's transport form to one question about light pins; and the reading of Lieb–Yau as a quantitative A2 with \(\kappa_{\rm int}=0.686\). These are modest. None is a new inequality, and none is an area law.

## 11. Open

- A bound or a counterexample for \(\beta_{\rm transport}\) of a region record at strong coupling, where the bag shows the unbind channel can exceed 1 (**OPEN**): can a tower of light pins reach the region's scale with records in distinct cells?
- Large representations at small gauge coupling, and many flavors, in Propositions M and S (**OPEN**).
- Input Z0 for solitonic carriers (**OPEN**).
- A2 with magnetic and quantized fields, sharper constants, and the species problem (**OPEN**; KNOWN as problems).
- Whether long-lived records in real strongly selected systems sit at mid-gap levels in shared traps, near \(B^*\) (**CONJECTURE**, the hypothesis's design read-off; untested).

## 12. Claim map for this note

| Claim | Label |
|---|---|
| Trap mass must be charged to the record (hoop counts it); uncharged zero-mode records give an artefactual infinite \(\beta\) | ELEMENTARY |
| Lemma Z: two-sided barrier \(\le\min(I,2E_c-I)\le E_c\); \(E_c-|E_b|\) for gap levels | PROVED (in-model, given Z0) |
| Lemma P: free composite has zero transport barrier | PROVED |
| Proposition R: \(\beta_{\rm transport}\gg1\) needs a light pin binding by nearly the full rest energy | ELEMENTARY |
| Monopole zero modes: \(\beta_{\rm unbind}\le n_fygS_t/4\pi\) (0.052, 0.103 at \(n_f=1\)) | PROVED (in-model, KNOWN inputs) |
| String loop zero modes: \(\beta\le n_f(y^2/4\pi^2+y/(2\pi vL))\) (0.0253 at \(n_f=1\)) | PROVED (in-model, KNOWN inputs) |
| Coulomb nuclear traps: \(\beta\le1.10\times10^{-3}\) (atoms), \(1.65\times10^{-3}\) (molecules) | PROVED (in-model, KNOWN inputs) |
| Hydrogen \(1.45\times10^{-8}\), U\(^{91+}\) 1s \(6.0\times10^{-7}\) | NUMERICAL |
| Light Coulomb trap \(\beta\lesssim\alpha^2\) | SKETCH |
| Bag: \(\beta_{\rm unbind}\ge0.40,\ 7.46,\ 45.2\) at \(g=10,100,1000\), unbounded in \(g\) | NUMERICAL (mean field, variational) |
| Self-gravity pin: \(\beta\le1/2\) | SKETCH |
| A2 for Coulomb electrons: \(\kappa_{\rm int}=0.686\) (\(z\le59\)); cap \(1.66\times10^{52}\) at 1 m | PROVED (in-model, from KNOWN Lieb–Yau) |
| Charged bosons: no A2 replacement | KNOWN (Lieb–Yau; Lieb 2004) |
| \(\beta_{\rm transport}\) for region records in general | OPEN |
| Real selected records sit at mid-gap in shared traps | CONJECTURE (untested) |

## 13. What the checks verify, and what this note does not do

- **What the checks verify.** `theory/transport_barrier_checks/transport_barrier_checks.py` (stored output `transport_barrier_checks.out`; run under `tools/test_transport_barrier_checks.py`) checks:
  - Lemma Z on random bindings and gap levels, and Lemma P on a lattice lump;
  - the Prasad–Sommerfield energy, the Callias counts and the monopole numbers;
  - the BPS string tension for \(n=1,2\), the mode count and the string bound;
  - the Coulomb bounds, the hydrogen and U\(^{91+}\) values and the Dirac 1s bound;
  - the bag-limit mode, the Dirac solver's bag limit and the three variational bag bounds;
  - the Lieb–Yau constants and the cap;
  - the read-off mass floor, every number quoted here, the wording rules, and that every DOI cited is in `crossref.out`.
- **What a green run means.** It is not a proof and is not evidence about a real system.
- **What this note does not do.** It does not edit `THEORY.md`, `CORE.md` or `theory/SCALE_ENDS.md`, and it changes no CLAIM_MAP row. It does not derive general relativity, quantum mechanics, or holography.
