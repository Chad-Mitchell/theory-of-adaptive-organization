# COLLAPSE1 amendment 2 (written ~22:50 ET Sat 2026-11-14, before computing anything it concerns)

## Disclosures since amendment 1 (already seen, so NOT preregistered)
- Hummingbird revisit medians/modes (Henderson 2006) and Wark 2009 Fig 1E/2E time constants
  (read off figures) have been seen. PREDICTIONS.md did not say median vs mode or which Wark
  panel; both are reported, marked post hoc.
- Several immune half-lives (Slifka & Amanna 2019; pertussis JMM 2010; SARS-CoV-2 review) have
  been seen and are scored by the locked A1 rule; ambiguities are reported, not resolved in favour.

## New computed test E5: is "need" in a software environment scale-free? (new domain)
Data: full commit histories (file names per commit) of numpy, django and rails (public GitHub).
Analysis copies Anderson & Schooler 1991's retention analysis: for each file and each day d,
need = "file modified on day d"; predictor = days since the file was last modified (within a
365-day lookback). Need odds vs lag, fit on log-log (power) and log-linear (exponential),
lags 1-365 days, weighted least squares on log odds with binomial weights.
- **E5a (T7b/E1 in a new domain):** a power law fits better than a single exponential
  (lower weighted SSE, and power-law R^2 ≥ 0.9) in all 3 repos. Kill if exponential fits better
  in ≥ 2 of 3.
- **E5b (exploratory, no kill):** fitted exponent reported next to Anderson & Schooler's
  0.73 (news), 0.77 (child speech), 0.83 (email). Not predicted to match: theory does not require a
  universal exponent; a match within ±0.15 in all three repos would be a surprise worth flagging.
