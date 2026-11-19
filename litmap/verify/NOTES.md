# Verification notes (litmap sweep, Sat 2026-11-14 ET)
- VERIFIED_DOIS.txt: every DOI resolved against the Crossref API this pass (title/authors/journal/year printed).
- Wrong DOIs caught and NOT used: 10.1016/j.neuron.2005.01.027 (is Cisek), 10.1146/annurev.ecolsys.29.1.1, 10.1016/j.tree.2018.07.004,
  10.1073/pnas.1204263109 (is Mandal-Jarzynski, not Murugan-Huse-Leibler), 10.2307/2392467 (is Feldman-March, not Weick),
  10.1086/285324, 10.2307/2410126, 10.1007/BF02223790 (is Ellis, not Grasse), 10.1016/j.plrev.2017.12.001 (not Ramstead), 10.1287/orsc.1040.0116.
- Other items were checked by WebSearch/WebFetch result pages (abstract or publisher page) this pass; see per-item notes in LITMAP.md.
- Items marked [classic, not fetched] are standard books whose bibliographic details were not re-fetched.

- 19 Nov 2026 (ET), with THEORY v2.0: three DOIs added after resolving them against the Crossref API (title, authors, journal, volume, pages and year matched): Black & Cox 1976 (10.1111/j.1540-6261.1976.tb01891.x), Merton 1974 (10.1111/j.1540-6261.1974.tb03058.x; JSTOR also lists 10.2307/2978814), Alchian 1950 (10.1086/256940). The first two were marked [unverified] in THEORY v1.4.29 §10.
