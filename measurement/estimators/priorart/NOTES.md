# Prior art for AQN-ESTIMATORS — only what was actually read this session (15 Nov 2026)

Metadata and abstracts fetched from OpenAlex (`fetch.py`, output `openalex.out`). "Abstract read" means only the abstract; no full text was read for any item.
Journal volume and page numbers are as recalled or as encoded in the DOI; every DOI resolved in OpenAlex (titles, authors, venue, year from OpenAlex).

| Source | Read | Use here |
|---|---|---|
| Fox & Taqqu 1986, Ann. Stat. 14:517, doi 10.1214/aos/1176349936 | abstract | Parametric Whittle estimation for strongly dependent Gaussian series (consistency, asymptotic normality; fGn, FARIMA). Our Whittle fit on increments is an application, with an aliased power law plus white noise as the parametric family |
| Robinson 1995, Ann. Stat. 23:1630, doi 10.1214/aos/1176324317 | abstract | Local Whittle; limiting variance "of very simple form" not dependent on unknown parameters (the 1/(4m) form for d is recalled from the literature, not from this abstract). Our SE(α̂) ≈ 1/√M rule matches it with α = 2d |
| Hurvich, Moulines & Soulier 2005, Econometrica 73:1283, doi 10.1111/j.1468-0262.2005.00616.x | abstract | Local Whittle for a long-memory signal plus white noise: the noisy-series setting is known; our increment is a parametric, aliased version with an explicit N estimate |
| Gloter & Hoffmann 2007, Ann. Stat., doi 10.1214/009053607000000316 | abstract | Hurst estimation from noisy high-frequency (infill) data: optimal rate n^{−1/(4H+2)}. Contrast with our long-span setting |
| Sykulski, Olhede, Guillaumin & Lilly (OpenAlex year 2018), Biometrika, doi 10.1093/biomet/asy071 | abstract | Debiased Whittle; not used (our biases at M ≥ 250 were small); a candidate fix for small-M bias |
| Peng et al. 1994, PRE 49:1685, doi 10.1103/PhysRevE.49.1685 | abstract | DFA origin (comparator) |
| Kantelhardt et al. 2001, Physica A 295:441, doi 10.1016/S0378-4371(01)00144-3 | metadata only (no abstract in OpenAlex) | DFA artefacts paper; not relied on |
| Abry & Veitch 1998, IEEE Trans. IT 44:2, doi 10.1109/18.650984 | abstract | Wavelet Hurst estimator, compared against Whittle in the original; **not implemented here** |
| Davies & Harte 1987, Biometrika 74:95, doi 10.1093/biomet/74.1.95 | abstract | Hurst-effect tests; the circulant-embedding fGn generator used in `aqn.fgn` is usually credited to this paper (recalled; the abstract does not describe it) |
| Shumway & Stoffer 1982, JTSA 3:253, doi 10.1111/j.1467-9892.1982.tb00349.x | abstract | EM + Kalman smoother for state-space parameters (noise variance estimation); we use direct likelihood maximisation via the Kalman filter instead (same estimand) |
| Rabiner 1989, Proc. IEEE 77:257, doi 10.1109/5.18626 | abstract | HMM forward algorithm and estimation; our two-state Gaussian HMM and MMPP fits are textbook applications |
| Fischer & Meier-Hellstern 1993, Perf. Eval. 18:149, doi 10.1016/0166-5316(93)90035-S | metadata only | MMPP standard reference; not relied on beyond the name |
| Lowen & Teich 1993, PRE 47:992, doi 10.1103/PhysRevE.47.992 | abstract | Fractal renewal processes give 1/f^D count spectra with 0 < D < 1: our renewal control reproduces D ≈ 0.5 for shape 1.5; the count spectrum cannot separate renewal from Cox |

Not swept: Google Scholar; full texts; estimation of switching rates for Wonham/telegraph filters specifically; IV for errors-in-variables (textbook econometrics, recalled, not read). Novelty claim: none. Everything here is an application of known estimators; the contribution is the validation under THEORY's premises and the labelling of which optimum each estimate feeds.
