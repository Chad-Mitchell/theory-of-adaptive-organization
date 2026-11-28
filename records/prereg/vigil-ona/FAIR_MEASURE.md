# FAIR_MEASURE — what GTAO accepts as a fair kill of the vigilance prediction

Written 2026-11-15 (ET), before any VIGIL_ONA outcome was computed. Private working file.
Prompted by Chad's t1907 point: email is one layer of the informal network; meetings, calls, texts and
nomination surveys ("who is important to getting your work done") are the other layers, so the Enron and
PIAAC results are weak measures. This file fixes, in advance, which measurements can kill the claim and which
cannot, so that "the measure was unfair" is not available as a rescue afterwards.

## 1. The claim being protected or killed (only the parts that survived the math review)
- Model: members face x_i = g + u_i (g shared by the unit, u_i private); ρ = q_g/q_u. A level forms at N* and
  takes over tracking g.
- **V(N\*) ≥ 1 + (1+ρ)^(−1/2)** for every upkeep and price ratio (claim map E6–E7; class R, γ = ½). At zero
  upkeep V(N\*) = 1 + (1+ρ)^(−1/2), which lies in (1, 2). The exact formula with upkeep h′ and price ratio r is
  V(N\*) = ½(1 + (1+ρ)^(−1/2))(1 + √(1 + 4h′(√(1+ρ) − 1)/(rρ))).
- **Growth:** above onset the level's effort on g grows as N^a (a = ½ in class R), so ln V vs ln N slope in [0.3, 0.7].
- **Comparator:** V divides the level's effort on g by a *flat* member's effort on g (a member of a unit with no
  level). Nested members of the level's own unit should sample g **less** than a flat member (ideally not at all),
  so lead vs own-member contrasts overstate V when the instrument is clean, and are uninterpretable when the
  instrument cannot tell g-sampling from u-sampling (math review Issue 10).
- **Fractal reading (t1901):** "shared" is relative to the level. Each lead samples what its own pool (everyone
  below it) shares; for a VP that is the department's environment, for the CEO the firm's.
- Qualitative direction (leads scan the environment more) is **prior art** (Mintzberg's monitor role; Beer's
  System 4). GTAO's own content is the size floor, the √N growth, price invariance at h = 0, and the specificity
  to *shared* drivers.

## 2. What a fair measurement must have (all of these for a decisive kill)
1. **All channels.** Sampling of g counted across email, meetings, calls, chat/text, documents and systems,
   not one channel. Executives sample mostly verbally (Mintzberg 1973; Porter & Nohria: ~70% of CEO time in
   meetings), so a single written channel is biased against the level.
2. **Sampling, not receipt.** The quantity is the person's *choice* to seek information (queries, reads,
   meetings they called, advice they sought), not mail they received or roles assigned to them.
3. **Specific to the shared driver.** Either a named driver g fixed before data (a supplier price, a regulation,
   a customer segment, an upstream system) or a defensible structural proxy: information sought **from outside
   the unit that the lead's pool shares** (cross-boundary sourcing), contrasted with information sought inside
   it. "Any external contact" is not enough without the inside/outside contrast.
4. **Nomination-based information sourcing is admissible** (Chad's point): survey items such as "who do you go
   to for information/advice to get your work done" and "who provides information you use in your work" measure
   sourcing directly and across channels, because the respondent reports the relationship, not a channel.
   Frequency-weighted nominations are better than binary ones. They measure *breadth* of sources more than
   *frequency* of sampling, which attenuates growth tests (a fixed roster caps out-degree).
5. **Formal structure measured, not inferred:** who reports to whom, so pooled N (subtree size) per lead is
   known, and units are real reporting units rather than offices.
6. **Status controls.** Advice is known to flow up status hierarchies (Blau 1955; Lazega & van Duijn 1997):
   higher-status people are sought more and seek less, and they prefer status-equal alters, who in a pyramid
   sit disproportionately in other units. A fair test must separate GTAO's outward tilt from status-driven alter
   choice (alter-rank, status-matching and alter-popularity controls, plus ego activity controls).
7. **Comparator:** a flat comparator (matched units without a level, or the same units before the level
   existed) for the size floor; lead vs own members is acceptable only for direction/specificity tests.
8. **Power:** the design must detect the GTAO floor. The weakest GTAO effect at onset is
   V = 1 + (1+ρ)^(−1/2); for ρ ≤ 1 that is ≥ 1.71 (log 0.54); for small ρ, ≈ 2 (log 0.69). Above onset it is
   larger by (N/N*)^a. A test that cannot detect a log-ratio of ~0.5 with 80% power cannot kill.
9. **Lock** (sha256 + git timestamp) before outcomes, raw data kept, analysis script hashed, dry run on
   synthetic data with known truth before the lock, and ideally a blind analyst.

## 3. Evidence tiers (fixed now)
- **Tier 1 — decisive.** Meets all of §2 (incl. a named driver or flat comparator, all-channel logs or
  frequency-weighted multi-layer nominations, measured reporting lines, ≥ ~150 people with ≥ ~20 leads across
  ≥ 2 levels, power ≥ 80% at log-ratio 0.5). Kill rules (from claim map §3.2 / E6): pooled upper 95% bound of
  V_obs / (1 + (1+ρ̂)^(−1/2)) < 0.8; or V_obs ≤ 1 with CI excluding 1; or growth slope CI excludes 0.3 and
  includes 0. A Tier-1 kill moves vigilance from OPEN to KILLED.
- **Tier 2 — strong.** Multi-layer nominations with measured reporting lines, status controls and adequate
  power, but no named driver or flat comparator. A Tier-2 failure (GTAO-signed effect excluded at log 0.5,
  or opposite sign with CI excluding 0) moves the claim to **DISFAVORED**, not killed. A Tier-2 pass moves it
  to **SUPPORTED-WEAK** (direction and specificity beyond status, not the size floor).
- **Tier 3 — weak.** Single-layer or small (< 100 people, < 10 leads), units approximated by office or practice,
  no reporting lines, underpowered. Results are reported as consistent / inconsistent / inconclusive and **do not
  change the claim map status** by themselves; they are logged and can be pooled with others.

## 4. What GTAO does NOT accept as a fair kill (and why), fixed now
- Received email or any single written channel (Enron VIGIL-2): not sampling, one channel, assistants filter.
  VIGIL-2 stays a valid kill **of that instrument's prediction** ("external share of received mail rises with
  rank"), not of the vigilance claim.
- Self-reported reading frequency on coarse, top-coded items without driver specificity (PIAAC VIGIL-1).
- Lead vs own-member ratios used to test the size floor (wrong comparator, Issue 10).
- Any test where "external" includes counterparties of the person's *private* task (traders' counterparties,
  sales reps' own clients) with no inside/outside-of-pool contrast.
- Tests without status controls when the outcome is advice in-degree: "leaders are nominated more" is predicted
  by formal authority and status alone and cannot discriminate.

## 5. What GTAO DOES accept, so the claim stays falsifiable
- A Tier-1 failure kills it. A Tier-2 failure disfavors it. The mapping rules above are fixed before data; a
  later complaint that the measure "missed how leaders really gather information" is not admissible for any
  instrument that meets §2.
- Two independent Tier-2 failures in different organizations count as a kill.

## 6. Decisive data that would settle it (if public data are insufficient)
A partner organization's ONA survey (~150–2,000 people) with: HR reporting lines (pooled N per lead), unit
codes, frequency-weighted nominations on ≥ 3 layers ("who do you go to for information to get your work done",
"who provides information you use", "who do you discuss customer/market/regulatory changes with"), plus one
named shared driver per unit; ideally calendar/meeting metadata (who meets outsiders, how often) and a before/after
around a reorg that created or removed a level (gives the flat comparator). Bandiera, Prat, Hansen & Sadun's CEO
diary data (outsider vs insider meetings) would be a strong Tier-2 check on the top level if obtainable.
