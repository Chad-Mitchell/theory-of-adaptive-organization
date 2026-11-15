# Prior-art notes for QUEUE Q1 (PRIORART-SWEEP) and Q2 (SPECTRUM-MAP-DERIVE)

Executor, 15 Nov 2026, ~09:05–09:26 AM ET. Every citation below was checked this session against a publisher, DOI or
arXiv/OpenAlex record (web search); screening of citing works was by title and abstract, not full text, unless stated.

## Q1: what was already done, and what this run added
- **Already done (night 1):** `/workspace/gtao/night1/REVIEW/priorart/SWEEP.md` (box copy, not in this repo): OpenAlex
  forward citations of Marschak & Radner 1972 (~1,492 citers screened by query), Van Zandt & Radner 2001, Eppen, Reis 2006,
  Veldkamp & Wolfers 2007, Veldkamp 2011. Found no earlier statement of O1–O5; closest neighbours Bimpikis & Markakis 2016
  (Management Science, doi 10.1287/mnsc.2015.2204) and Abolhassani et al. 2024 (arXiv 2401.03613). Q1 as written mostly
  duplicated this (a divergence-type finding: the queue item did not read the night-1 file).
- **Added here:** OpenAlex forward citations of the two neighbours (`fwd.py`, `fwd_bm2016_abolhassani2024.json`):
  B&M 2016 → 72 records; Abolhassani 2024 → 16. None states O1 (class-dependent onset with a fixed-cost level) or O5
  (freeze/hold band widening with N). Nearest: restless-bandit / Whittle-index fresh caching (MASS 2024,
  doi 10.1109/mass62177.2024.00040; IEEE/ACM ToN 2025, doi 10.1109/ton.2025.3616225); "Optimal Caching for Dynamic Content
  Through Strategic Information Sharing" (INFOCOM 2026, doi 10.1109/infocom59046.2026.11571389), which prices observation.
  None of these is a statement of O1 or O5.
- **Proposition SG prior art (in substance):** Ferragut, Rodríguez & Paganini 2018, "Optimal timer-based caching policies for
  general arrival processes", Queueing Systems 88(3):207–241, doi 10.1007/s11134-017-9540-3: the optimal policy depends on
  the monotonicity of the inter-request hazard, and timer (keep-for-a-while) policies are optimal for decreasing hazards.
  That anticipates SG's "regime-conditional clock" for the keep/refresh decision. SG's surprise threshold rising ~1 per
  ln(dormancy) under a Lomax hazard is a direct computation in that setting. Recommend SG's novelty label: "application".
- **Not done:** Google Scholar (blocked for scripted access; not signed in, per rules). Queued as PRIORART-SCHOLAR.

## Q2: sources for the spectrum map (verified)
- Afterman, Chigansky, Kleptsyna & Marushkevych, "Linear filtering with fractional noises: large time and small noise
  asymptotics", SIAM J. Control Optim. 60(3):1463–1487 (2022), doi 10.1137/20M1360359; arXiv 1911.10062 (read: Thm 2.5,
  eq. 2.8; Remark 2.6).
- Nuzman & Poor 2000, J. Appl. Probab. 37(2):429–452, doi 10.1017/S0021900200015631 (fBm prediction formulae).
- Gripenberg & Norros 1996, J. Appl. Probab. 33(2):400–410 (fBm prediction, H > ½).
- Gatheral, Jaisson & Rosenbaum, "Volatility is rough", Quant. Finance 18(6):933–949 (2018), doi 10.1080/14697688.2017.1393551
  (forecast kernel (t−s)^{−(H+1/2)}/(t−s+Δ); H ≈ 0.1 for log-volatility).
- Hosking 1981, Biometrika 68(1):165–176, doi 10.1093/biomet/68.1.165; Granger & Joyeux 1980, J. Time Ser. Anal. 1(1):15–29,
  doi 10.1111/j.1467-9892.1980.tb00297.x.
- Mandelbrot & Van Ness 1968, SIAM Rev. 10(4):422–437, doi 10.1137/1010093; Davies & Harte 1987, Biometrika 74(1):95–101,
  doi 10.1093/biomet/74.1.95 (the circulant generator used in `checks/fgn.py`).
- Duncan 1970, SIAM J. Appl. Math. 19(1):215–220, doi 10.1137/0119020 (information–filtering-error link); Yovits & Jackson
  1955 (filtering error ∝ log(1+S/N) for white noise; DTIC AD0626449) — cited only as history; the formula used is Afterman
  et al.'s Remark 2.6.
- Kailath, Sayed & Hassibi, *Linear Estimation*, Prentice Hall 2000 (Wiener–Hopf, spectral factorization, rational spectra).
- Braess & Hackbusch 2005, IMA J. Numer. Anal. 25(4):685–697, doi 10.1093/imanum/dri015 (exp(−c√k) on [1,∞));
  Braess & Hackbusch 2009, MPI MIS Leipzig preprint 3/2009 (bound 16 exp(−π²k/log 8R) on [1,R]; text read);
  Beylkin & Monzón 2010, ACHA 28(2):131–149, doi 10.1016/j.acha.2009.08.011.
- Carmona & Coutin 1998, Electron. Commun. Probab. 3:95–107, doi 10.1214/ECP.v3-998; Bayer & Breneis 2023, Quant. Finance
  23(1):53–70, doi 10.1080/14697688.2022.2139193.
- Lee, Flack & Krakauer 2024, "Constructing stability: optimal learning in noisy ecological niches", Proc. R. Soc. B 291:20241606
  (arXiv 2209.00476; derivation of τ_m\* ∼ τ_E^{1/2} read in the CSH PDF).
- Benna & Fusi 2016, Nat. Neurosci., doi 10.1038/nn.4401; Fusi, Drew & Abbott 2005, Neuron 45:599–611,
  doi 10.1016/j.neuron.2005.02.001; Shankar & Howard 2013, JMLR 14(83):3785–3812; Anderson & Schooler 1991, Psychol. Sci.
  2(6):396–408, doi 10.1111/j.1467-9280.1991.tb00174.x; Anderson & Milson 1989, doi 10.1037/0033-295x.96.4.703;
  Reis 2006, Rev. Econ. Stud. 73(3):793–821, doi 10.1111/j.1467-937x.2006.00396.x.
- Lowen & Teich 1993, IEEE Trans. Inf. Theory, doi 10.1109/18.259653; Goh & Barabási 2008, EPL 81:48002,
  doi 10.1209/0295-5075/81/48002.
- Coibion & Gorodnichenko 2015, AER 105(8):2644–2678, doi 10.1257/aer.20110306 (gain measure proposed for test 1).

**Open prior-art question:** whether anyone has stated τ_m\* ∝ τ_E^{1−1/α} (LFK with general slope). One web query found
nothing; a forward-citation sweep of LFK 2024 and of Afterman et al. 2022 is queued (PRIORART-LFK-ALPHA).
