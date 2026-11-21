# Confirm review of layer lifetime (PR #141, head 5074fff)

Read-only confirm of `5074fff994d65e02824825bcc10a763f1fd9cc01` on `layer-lifetime-2026-11-21`, base `main` `07264237536db1aaf2a8cd663a558dc3f868d469`. Saturday 21 November 2026. Computations at nice 19. The reviewer wrote none of the note, made no commit, and did not merge.

**READY-WITH-FIXES.** No result in the re-derivation failed. Three sentences in the note are false, and the PR text still carries the review's pytest nit and a D5 claim the note retracted.

## Defects

1. `theory/LAYER_LIFETIME_2026-11-21.md:32`. Replace `Nothing in the rest of this note depends on using 6 rather than 2; the exponent \(\tfrac12\) in \(k\) and in \(1/\sigma^2\) is the same.` with `The exponent \(\tfrac12\) in \(k\) and in \(1/\sigma^2\) is the same for the coefficient 6 and the coefficient 2. The factor 3 in §5 uses both: the barrier excess equals the fixed-period excess divided by \(\sqrt{3}\), and the variance-rate crossing is the fixed-period crossing divided by 3.`

2. `theory/LAYER_LIFETIME_2026-11-21.md:89`. Replace `If local updates carry the same delay, the floor is on both sides and the difference does not depend on \(\sigma^2\).` with `If local updates carry the same observation delay, both sides have the floor \(Nw\sigma^2\ell\). The floors cancel. The gap that remains is \(\sqrt{\sigma^2}\bigl(\sqrt{2k_S Nw}-N\sqrt{2k_L w}\bigr)\) for fixed-period refreshes, and that gap divided by \(\sqrt{3}\) for the barrier. The sign is the same at every \(\sigma^2\), so there is no switch.`

3. `theory/LAYER_LIFETIME_2026-11-21.md:67`. Replace `That is Model S's \(E_K\).` with `L3 says \(E_K>E_\infty\) for every finite \(K\) on that spectrum, and \(K^*\to\infty\) only if also \(E_K\to E_\infty\) (THEORY.md, CT21). That is a statement about Model S's \(E_K\), and \(T^*\) does not compute \(E_K\).`

4. PR #141 body. Line 17: replace `Karim, Carroll & Long 2016 already report less business-unit recombination during industry turbulence — a published opposite-sign finding any D5 prereg has to face.` with `Karim, Carroll & Long 2016 report less business-unit recombination during industry dynamism. That coefficient is the opposite of the menu-cost frequency prediction. It is not an opposite-sign result for D5. Karim 2016 and Girod & Whittington 2017 do not identify P2 or P3.` Line 19: replace ``Checks: `theory/layerlife_checks/` (33/33, ALL PASS). `tools/check_consistency.py` PASS, `tools/check_open_work.py` PASS, pytest 149 passed.`` with ``Checks: `theory/layerlife_checks/` (26/26 checks, 6 identities, ALL PASS). `tools/check_consistency.py` PASS, `tools/check_open_work.py` PASS, pytest 150 passed and 1 skipped (`tools/test_lean.py:101`, lake not installed).`` Line 1: replace `Not independently reviewed.` with `Independent review: `reviews/layerlife_2026-11-21/REVIEW.md` (READY-WITH-FIXES).` Line 21: replace the whole line with `Independent review: `reviews/layerlife_2026-11-21/REVIEW.md`.`

## Should-fixes and nits

Landed and correct: bottom-line item 2; the B.11 / CT28 / CT34 citation; the DIR1 sentence as updated for the merge; the barrier paragraph through "divided by 3"; the OU paragraph (\(183\ell\), \(185\)); the rivals paragraph; the repository bullet; Simon credited in THEORY §10; the Sims credit; the Karim and Girod paragraphs, including the two added sentences; the \(k=3\) check; tautologies labelled identities (26 checks, 6 identities); the script writes `layerlife_checks.out` and a rerun matches the committed file; the OU tag is "comparable to tau"; the two-layer line is the domination identity; the fractional-Brownian balance includes \(CT^{2H}/(2H+1)\); Dixit 1989 is off the DOI list.

The pytest nit did not land. The PR body still says 33/33 and pytest 149. This run is 26/26 plus 6 identities, and 150 passed, 1 skipped.

## Re-derivation

Zero discount, quadratic loss, Brownian gap. Exit time \(b^2/\sigma^2\), mean square \(b^2/6\), so \(T^*=\sqrt{6k/(w\sigma^2)}\) and the excess cost is \(2\sqrt{kw\sigma^2/6}\). Equal stakes give \(T_i^*/T_j^*=\sqrt{(k_i/k_j)(\sigma_j^2/\sigma_i^2)}\).

Shared-only fixed-period crossing at the check prices: \(\sigma^{2*}=0.021614229749224\). Barrier crossing \(0.007204743249741\), which is that value divided by 3 (bisection relative error about \(10^{-15}\)). Shared is cheaper below each root and local is cheaper above. Equal delay on local updates: the floors cancel, the gap keeps its sign, and the gap scales with \(\sqrt{\sigma^2}\) (\(-0.07351\) at \(\sigma^2=0.01\), \(-0.7351\) at \(\sigma^2=1\)).

OU, same prices, \(\ell=0.5\): local \(9.49929\) against shared \(10\) at \(\tau=0.05\); \(0.62575\) against \(0.87515\) at \(\tau=20\); \(0.19933\) against \(0.17578\) at \(\tau=200\). The crossing is \(182.57\ell\). The Brownian multiple \(2v/(\sigma^{2*}\ell)\) is \(185.06\). The multiple moves with \(k_S/(Nk_L)\) (about \(40,80,183,932,9480\) at ratios \(0.05,0.2,0.4,0.7,0.9\)) and with the lump scale (\(15.8\ell\) when both lumps are multiplied by 10; both sides sit on the blind cost at the fast end when multiplied by 100).

\(k=3\), \(a=0.2\), \(v=w=1\): \(wv/(2a)=2.5\), and \(J(T)-wv=(1/T)[3-2.5(1-e^{-2aT})]>0\) for every finite \(T\). The committed minimizer returns \(1.00001\), which is not below \(wv\).

## Claims against the repository

`1cb1ac2` (merge of PR #138) is an ancestor of `origin/main`. DIR1's prereg states D5 as the fast-local sign and attributes it to CT35 with the B.11 factor. RESULTS leaves D5 unscored, \(n=2\) (0/2). The note's DIR1 sentence matches that. CT35 is the map theorem. The OU factor is THEORY.md line 488. `figures/face_placements.md` attributes the nesting to CT28 and CT34. THEORY §8 is "Predictions, and how it dies." Simon 1962 is credited in §10. The holographic fail in `core/KEYSTONE_NOTE.md` §5 is 3/24 primary cells, and the equal-value CVs failed. LAYERS1 P2 is G20, SIM-FAIL. CL12 is still proved.

Karim's OpenAlex abstract: 46 firms, 1978–1997, U.S. medical devices and pharmaceuticals; less recombination during industry dynamism and when top-management-team size grows; the paper reads that as delay. Girod's Crossref abstract: performance of restructuring versus reconfiguration for large U.S. corporations, 1985–2004. Issued 2016-07-11, print 2017-05, volume 38, issue 5, pages 1121–1133. The note does not identify either series as P2 or P3. The Fortune-50 counts were not re-counted from the full text.

The hypothesis sentence is byte-identical to `CORE.md`: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." The word "bill" is not used. No locked prereg, `.sha256`, or `LOCK` file differs from `origin/main`.

## DOIs

All 11 DOIs in the note and in `theory/layerlife_checks/dois.txt` resolved on the Crossref API on 21 Nov 2026. The two lists are the same set. Titles, authors, journals, volumes, and start pages match the reference line. Dixit 1989 is not in either list.

## Checks

NumPy 2.5.5, SciPy 1.18.1, pytest 9.2.0, SymPy 1.14, user site. Tree left clean. Stdout of the first command matches the committed `.out`.

| Command | Result |
|---|---|
| `python3 theory/layerlife_checks/layerlife_checks.py` | ALL PASS. 26/26 checks; 6 identities. Exit 0 |
| `python3 tools/check_consistency.py` | RESULT: PASS (0 FAIL, 23 INFO) |
| `python3 tools/check_open_work.py` | RESULT: PASS |
| `python3 -m pytest -q tools` | 150 passed, 1 skipped (`tools/test_lean.py:101`, lake not installed), 127.94 s |

The three defects and the PR-body updates listed above were applied in the next commit.
