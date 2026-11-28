# VIGIL_ONA — results (public organizational-network nomination data)

Run 2026-11-15 08:14 ET, after the lock (LOCK.txt, 08:12:56 EST; hashes re-verified immediately before the run).
Git timestamp of the lock: private repo `Chad-Mitchell/theory-of-adaptive-organization`, branch `prereg/vigil-ona`,
commit 52a624a (2026-11-15 08:13:02 −05:00). Repo visibility checked before and after: PRIVATE. Nothing posted or emailed.
Raw data kept in data/raw (sha256 manifest data/SHA256SUMS_raw.txt). Raw output: results_real.json; post-hoc: posthoc.json.
Evidence tier (FAIR_MEASURE.md §3): **Tier 3 for every dataset**, so by the rule fixed before the data, nothing here
moves vigilance off **OPEN**.

## Data actually used (all verified downloadable tonight)
| Dataset | People | Rank used | "Unit" | Primary layer |
|---|---|---|---|---|
| Krackhardt 1987 high-tech managers | 21 (CEO not an ego) | VP vs manager (+ measured reports-to spans 2–7) | department | "go to for advice" |
| Lazega law firm (SG&R, 1988–91) | 71 | partner vs associate | office × practice | "basic professional advice" |
| Cross & Parker 2004 consulting | 46 | 5 org levels | office | "turned to for information or advice", ≥ "sometimes" |
| Cross & Parker 2004 manufacturing R&D | 77 | 4 org levels | site | "provides information you use to accomplish your work", ≥ 4/6 |
Dropped before the lock: Krebs IT department (rank = 3 executives only; their CUSTOMER answers truncated), Thurman office,
Kapferer tailor shop, sawmill, SocioPatterns office (reasons in PREREG §0).

## Locked results (decision CIs use SE × 1.3, the coverage correction fixed in the prereg; nominal CIs in brackets)
| Test | Estimate | Decision 95% CI | Nominal 95% CI | Locked rule | Outcome |
|---|---|---|---|---|---|
| **H1** outside-unit advice-seeking rate, top vs bottom rank, pooled | RR **1.94** | 1.27–2.97 | 1.40–2.69 | CI lower > 1 | **PASS** (direction; also predicted by Mintzberg) |
| H1-spec (outside vs inside, generic-activity control), pooled | ratio of RRs 2.64 | 1.53–4.55 | 1.74–4.01 | reported | GTAO-signed |
| **H2** ego rank × outside-unit, with ego FE, alter FE, status matching, pooled | OR **2.47** (β = 0.91) | 1.18–5.19 | 1.40–4.37 | CI lower > 0 (log) | **PASS** |
| **H3** elasticity of outside seeking on ln(1 + pooled N) | **0.39** | — | 0.11–0.68 | CI lower > 0 and point ≤ 0.7 | **PASS** (GTAO band 0.3–0.7) |
| Locked overall label | | | | H1 PASS and H2 PASS | **CONSISTENT-GTAO-SPECIFIC (Tier 3)** |

Per dataset (β or logRR ± SE):
| | H1 logRR | H2 β | Weight in H2 pool |
|---|---|---|---|
| Krackhardt | 0.03 ± 0.36 (VPs 0.44 vs managers 0.47 outside rate) | −1.38 ± 1.87 | ≈ 2% |
| Lazega | 0.66 ± 0.21 | **1.10 ± 0.32** | ≈ 82% |
| Consulting | 1.17 ± 0.64 | 0.18 ± 0.97 | ≈ 9% |
| Manufacturing | 2.24 ± 0.65 | 0.39 ± 1.10 | ≈ 7% |
Heterogeneity: H1 Q = 9.6 (3 df, p ≈ 0.02); H2 Q = 2.7 (p ≈ 0.45).
**Leave-one-out (pre-declared):** without Lazega, H2 = 0.05 (decision CI −1.68 to 1.78) and H1 = 0.68 (−0.05 to 1.40).
Without any other single dataset, H2 stays 0.95–0.98 with CI above 0.

## Secondary (locked, not decisive)
- **Placebo (friendship):** Lazega friendship H2 β = 0.03 ± 0.34 vs advice 1.10 ± 0.32 and cowork 0.63 ± 0.36. The outward
  tilt is specific to work-information layers, not general sociability. Krackhardt friendship hit separation (β = −16)
  and is excluded by the pre-declared filter.
- Other information layers point the same way but are noisy: Lazega union of work layers 0.50 ± 0.27; consulting
  "has expertise important to my work" 1.21 ± 1.11; manufacturing "awareness of skills" −0.97 ± 1.97. Frequency-weighted
  H1: consulting 0.87 ± 0.46, manufacturing 1.76 ± 0.53. Weighted H3: 0.39 ± 0.11.
- **Status rival:** in-degree rises with rank in all four organizations (top vs bottom logRR 0.85–0.90, about 2.4×), as
  status *and* GTAO both predict, so it doesn't discriminate. The status rival's other half, that higher ranks seek less
  advice, fails: out-degree is flat (Krackhardt −0.12 ± 0.40, Lazega 0.01 ± 0.14) or higher (consulting 1.09 ± 0.35,
  manufacturing 0.64 ± 0.45).

## Post-hoc diagnostics (written after seeing the results; labeled, not part of the rules)
- **Lazega seniority confound:** partners are also the seniors. Adding ego seniority × outside: β = 0.81 ± 0.52 (CI includes 0);
  with age too, 0.71 ± 0.51. Rank and tenure cannot be separated in these data. "Higher-ups source outside" and "people who
  have been around longer know people in other offices" fit equally well.
- **H3 rests on four manufacturing managers.** Without the 3 local managers and the global manager: ε = 0.06 ± 0.16. Without
  the global manager alone: 0.21 ± 0.16. Without manufacturing: 0.15 ± 0.18. Without Krackhardt: 0.51 ± 0.12.
- H3 specificity: the same model on *inside*-unit seeking gives ε = 0.14 ± 0.06, against 0.39 outside. That tilt is GTAO-signed
  but partly generic activity (the global manager nominates everyone at his own site).

## Verdict
- **On the locked rules: CONSISTENT-GTAO-SPECIFIC at Tier 3.** This is the first real-data result in GTAO's direction that
  survives a status control: higher-ranked people tilt their information-seeking outside their own unit about 2.5× more
  (odds) than lower-ranked people, net of each person's activity, each alter's popularity and status matching. The
  friendship placebo is null.
- **Honest weight: weak.** About 82% of H2 comes from one law firm, where "rank" is partner vs associate and is confounded
  with seniority (post-hoc). Without Lazega, H2 is uninformative (0.05, CI −1.7 to 1.8). H3's √-like slope is carried by
  four managers at one company. Krackhardt, the only data with measured reporting lines, is far too small (power ≈ 0.2) and
  shows nothing (VPs 0.44 vs managers 0.47).
- **This is not a size test.** Nominations measure breadth of sources, not sampling frequency, and the comparator is
  lower-ranked colleagues, not a flat member (math Issue 10). The pooled RR of 1.94 sits near the corrected floor
  V(N\*) ≥ 1 + (1+ρ)^(−1/2) (1.71–2 for ρ ≤ 1), but that is a coincidence of scales and is not claimed.
- **Claim-map status: vigilance stays OPEN** (H8), per FAIR_MEASURE. Suggested row: "VIGIL-ONA (4 public ONA datasets): direction
  and outward tilt beyond status PASS at Tier 3; Lazega-driven, seniority-confounded; growth carried by 4 managers." H7 (Enron)
  remains a kill of *that instrument's* prediction (external share of received mail), not of vigilance.

## What would be decisive (public data are insufficient)
A partner organization's ONA survey meeting FAIR_MEASURE Tier 1–2: ≥ 150 people and ≥ 20 leads across ≥ 2 levels; HR reporting
lines (pooled N per lead) and real unit codes; frequency-weighted nominations on ≥ 3 layers ("who do you go to for information
to get your work done", "who provides information you use", "who do you discuss customer, market or regulatory changes with");
tenure recorded, to break the rank–seniority confound; ideally calendar/meeting metadata and a reorg that added or removed a
level (the flat comparator). Locked analysis: this script, with reporting units replacing offices. Power: about 20+ leads gives
SE ≈ 0.15–0.2 on H2 in simulation, enough to exclude β < 0.5. Bandiera–Prat–Hansen–Sadun CEO diaries (outsider vs insider
meetings) would be a Tier-2 check of the top level if they can be obtained.
