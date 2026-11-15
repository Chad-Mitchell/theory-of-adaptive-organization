# COLLAPSE1 amendment 1 (written ~22:45 ET Sat 2026-11-14, before reading the numbers it concerns)

## Trigger (disclosed)
While searching for antibody half-lives, a search snippet showed that "Quantifying the waning of
humoral immunity" (PMC12132162) fits POWER-LAW waning, reports that the power-law coefficient m is
"broadly similar" across vaccines and virus antigens, and argues the toxoid-vs-virus half-life gap
in Amanna 2007 is largely a measurement-time artifact (snippet: tetanus/diphtheria half-lives would
be 72 and 88 y if measured at year 45). The author has seen only that snippet, not the paper's
exponent values. Saved to sources/ but not read before this commit.

## Consequence for A (stated now)
Under power-law decay, an exponential "half-life" measured at age t is t·ln2/m: it grows linearly
with when you measure. So cross-antigen half-life comparisons are confounded by measurement age.
A1 is still scored as locked, but the result will be reported with this confound, and a
time-matched re-score done where the source allows.

## New prediction E: collapse in EXPONENT space (dimensionless, so no units problem)
Physicist's reasoning: if a world has drift/need at all timescales (no characteristic time; the T7b
condition), the efficient held memory is a superposition of geometrically spaced timescales (T7
layering), which sums to a power law. Rule 2 (keep while need x miss cost > upkeep) then says the
memory's decay exponent should match the decay exponent of the probability the item is needed
again (the rational-analysis claim of Anderson & Schooler 1991, prior art for human memory only).
- **E1 (power law is the norm for long-held memories in multi-scale worlds):** in every substrate
  where long-horizon decay data exist (immune antibodies, human memory, citations/attention, word
  use), a power law fits at least as well as a single exponential over ≥ 1 decade of time.
  Kill if ≥ 2 of the substrates found are clearly better fit by one exponential.
- **E2 (matching, the diagnostic):** within a system, memory decay exponent m_mem and the
  need/relevance decay exponent m_env agree within a factor of 2. Kill if any system with both
  measured differs by more than a factor of 3; "fails" if a factor 2-3.
- **E3 (cross-substrate):** exponents from different substrates are reported on one chart; the
  theory does NOT predict one universal value (that would need universal world statistics), so a
  wide spread is not a failure. A tight universal value would be a surprise worth reporting.
- **E4 (immune, prior art check):** the paper's antigen exponents are within a factor 2 of each
  other (this is the paper's own claim; extraction, not a test).
