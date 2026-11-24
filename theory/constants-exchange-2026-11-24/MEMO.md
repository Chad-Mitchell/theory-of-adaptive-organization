# Memory, tracking, and the exchange rates

*Tuesday 24 November 2026 (UTC). Against `main` `0f37918`, after the lock in `PREREG.md` (`0846e2e`). `THEORY.md` is not edited. No real-world series was opened.*

Why this approach. The cost alone is dimensionless (nats times stakes), so on its own it cannot set a physical scale. The memory coordinate is a number of nats (`THEORY.md:30`, `CORE.md:33`, Theorem R1 at `CORE.md:52`). The stake is the currency, and only dimensionless ratios of those products matter (`THEORY.md:36`). Nothing in that product is a joule or a second until a conversion is supplied. Once the cost is coupled to physics, dimensional constants may enter as exchange rates, and whether they do is an open question, not an established limit. The sentence that the cost contains neither \(G\), \(\hbar\), nor \(c\) (`theory/PHYSICS_CHAIN_2026-11-23.md:73`, pointing at `theory/AREA_LAW_PROBE_2026-11-23.md:17` and `:135`) is too absolute. This note does not adopt it. A miss below is a puzzle about that bridge, not a limit on a later coupling.

**Label.** The mapping from a term to a bridge is **INTERPRETATION**. The dimension identities in `dimension_check.py` are **ELEMENTARY** checks of formulas the repository or the cited papers already state. They are not a derivation of the values of \(k_B\), \(\hbar\), \(c\), or \(G\), and they are not a proof that a physical system uses this coupling. This note does not derive general relativity, quantum mechanics, or holography.

## Which term is which

The question is the memory term and the tracking term. In the five-term display the memory term is \(\kappa I_{\mathrm{mem}}\). In the physical class that term is the bath heat, with floor \(kT\) times the learning rate (`CORE.md:39`). The tracking term is that learning rate: the general floor (`CORE.md:70`), the random-walk floor (`CORE.md:76`, `THEORY.md:295`), the OU and telegraph floors (`CORE.md:90`, `CORE.md:94`), and the clock between looks (`theory/CLOCK_TERM_2026-11-23.md:11`, `:19`, `:35`). The world's rates are measured inputs (`THEORY.md:35`). Upkeep \(hK\), the separate read price \(A\), the link price \(L\), the stake \(w\), and the ruin cap stay assumed (`CORE.md:40-44`); temperature does not set \(w\) (`CORE.md:29`). They are not scored.

A quantum-record price is the modeling choice in `PREREG.md`: \(I_{\mathrm{mem}}\) is not replaced by a von Neumann entropy or a Holevo quantity, because R1 fixes Shannon mutual information for classical records only (`CORE.md:52`). Margolus–Levitin, Mandelstam–Tamm, and the Bekenstein-type bounds are read as external ceilings on a carrier one has chosen to treat as quantum.

## What each bridge puts in the monomial

Bath temperature \(T\) is the intensive partner of the \(k_B\) exchange. It is not a third constant. A pure numerical factor is not part of the score (`PREREG.md`).

**Erasure.** The repository states Landauer's cost as at least \(kT\ln 2\) per bit (`theory/SCALE_ENDS.md:23`). That is \(k_B T\) times a dimensionless count. The 1961 text was not opened. The finite-time paper (Proesmans, Ehrich, and Bechhoefer 2020) was not opened, so no finite-time formula is scored. The quasistatic cost is the one in the table.

**Ongoing heat and the tracking floors.** \(\dot Q_M\ge kT\,\dot I_M\) (`CORE.md:70`). The same \(k_B T\) multiplies a rate the cost already takes: \(\sigma^2/(2D)\) (`THEORY.md:295`), \(a(v-\varepsilon)/\varepsilon\) (`CORE.md:90`), and the telegraph flow (`CORE.md:94`). Each rate is \(1/\mathrm{time}\) once the error is in the world's own units. \(\hbar\) does not appear.

**Clock.** The TUR price is \(kT\,\omega'^2/D\) (`theory/CLOCK_TERM_2026-11-23.md:35`). Phase is dimensionless in that note, so \(\omega'\) and \(D\) are both rates and \(\omega'^2/D\) is a rate. The only dimensionless group of the small-angle model is \(c/(\kappa kT)\) (`theory/CLOCK_TERM_2026-11-23.md:60`). Again \(k_B\) alone.

**Margolus–Levitin.** The 1998 abstract says the bound depends only on \(E-E_0\). The repository records \(\mathrm{ops/s}\le 2E/(\pi\hbar)\) (`theory/SCALE_ENDS.md:169`). Both are a time \(\hbar\) over an energy. This note does not add a prefactor. As a conversion, once \(E-E_0\) is supplied, the monomial is (B). The cost does not name \(E-E_0\). Using the bound as the tracking term's time therefore leaves an extra energy (F3). Setting that energy to \(k_B T\) times a nat count, so that the time becomes \(\hbar/(k_B T)\), puts both constants in one monomial (F1).

**Mandelstam–Tamm.** Deffner and Campbell 2017 treat this as a quantum speed limit. The 1945 text was not opened, so the orthogonalization prefactor is not re-derived. The conversion that was checked is \(\hbar/\Delta E\). \(\Delta E\) is not a width the cost names (F3).

**Bekenstein-type stock.** The repository states \(E/S\ge\hbar c/(2\pi R)\) (`theory/SCALE_ENDS.md:163`). The dimensionless count is \(ER/(\hbar c)\): \(\hbar\), \(c\), and a length (F1 and F3). The printed entropy \(S=kA/(4\ell_p^2)=4\pi k GM^2/(\hbar c)\) (`theory/SCALE_ENDS.md:161`) carries a factor \(k\) and is also given as a nat count. Dividing out \(k\) leaves \(4\pi GM^2/(\hbar c)\). The script checks \(GM^2/(\hbar c)\); the \(4\pi\) is a pure number and is not part of the score. The combination contains \(\hbar\), \(c\), and \(G\). Lloyd's 2000 abstract says the limits it explores are set by \(c\), \(\hbar\), and \(G\). No formula from that paper was dimension-checked. Naming those three constants together is the same miss (F1 and F3).

## Results

Scores are the locked rule applied by `dimension_check.py`. The stored run is `dimension_check.out`.

| Term | Bridge | Constant | Combination | Score |
|---|---|---|---|---|
| Memory erasure | Landauer (`SCALE_ENDS.md:23`) | \(k_B\) | \(k_B T\times\) nats | pass (A) |
| Ongoing memory heat | Horowitz–Esposito (`CORE.md:70`) | \(k_B\) | \(k_B T\times\) (nats/time) | pass (A) |
| Tracking floors | CT7, OU, telegraph (`THEORY.md:295`, `CORE.md:90`, `CORE.md:94`) | \(k_B\) | \(k_B T\times\) (world rate) | pass (A) |
| Clock | TUR, Barato–Seifert (`CLOCK_TERM_2026-11-23.md:35`) | \(k_B\) | \(k_B T\times(\omega'^2/D)\) | pass (A) |
| Speed, mean energy, as the tracking time | Margolus–Levitin (`SCALE_ENDS.md:169`) | \(\hbar\) | \(\hbar/(E-E_0)\) | fail (F3) |
| Same speed, energy set to the erasure cost | Margolus–Levitin composed with Landauer | \(k_B\) and \(\hbar\) | \(\hbar/(k_B T)\) | fail (F1) |
| Speed, energy spread | Mandelstam–Tamm (prefactor not re-derived) | \(\hbar\) | \(\hbar/\Delta E\) | fail (F3) |
| Stock bound | Bekenstein 1981 (`SCALE_ENDS.md:163`) | \(\hbar\) and \(c\) | \(ER/(\hbar c)\) | fail (F1+F3) |
| Printed entropy count | `SCALE_ENDS.md:161`, \(k\) divided out | \(\hbar\), \(c\), and \(G\) | \(GM^2/(\hbar c)\) | fail (F1+F3) |
| Ultimate laptop | Lloyd 2000, abstract only | \(c\), \(\hbar\), and \(G\) | not checked as a formula | fail (F1+F3) |

The first speed row is monomial (B) if \(E-E_0\) is supplied from outside the cost. It is a fail only as the tracking term's own time. Four dimension-checked rows pass and five fail; the Lloyd line is the sixth fail and is not an identity. Every identity in the script holds (`DIMENSIONS OK`).

## What was learned

The classical memory and tracking heat already in the repository is \(k_B T\) per nat, or per nat per time. \(\hbar\) does not enter those formulas. A quantum speed limit prices time as \(\hbar\) over an energy, and that energy is not fixed by the cost unless one inserts \(k_B T\), which mixes the two constants. A Bekenstein-type stock bound mixes \(\hbar\) with \(c\) and a length, and the printed entropy count mixes in \(G\) as well. On these bridges \(k_B\) and \(\hbar\) are the exchange rates in their separate slots. The fused thermal time and the stock bound are puzzles about those bridges. They are not an established limit on every coupling. The question stays open.

Only dimensionless constants are candidates for prediction. The fine-structure constant is the example. That question is the nested-layer fixed point, a conjecture and untested, on branch `ace-probe-memos-2026-11-23` in `theory/probes-2026-11-23/MIRROR_MEMO.md` (the paragraph that begins "The only legitimate pattern found: a fixed point of a nested-layer map", and the claim-map row "Nested-layer fixed point gives a universal GTAO number"). This note does not take it up.
