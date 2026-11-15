# ONA-MORE: data gate check (pick 16, uniform slot)

Sunday 15 November 2026, about 3:50–4:00 PM ET (America/New_York). Grok Bot executor queue-pick16 for Chad Mitchell, via Ace. Private. Nothing posted, sent or made public.

## What the item asks
QUEUE Q10 / items.json `ONA-MORE`: *"Tier 3 by construction; cannot change vigilance's status. Take only if a dataset with tenure,
real reporting units and a shared-environment vs own-task question appears"* (referee fixes, `reviews/night2/REFEREE/REPORT.md` §6 item 3:
tenure a locked covariate; reporting units, not offices; a shared-environment name generator separate from an own-task one, so GTAO's
rank tilt is predicted on the first and not the second; random-effects pool with HKSJ; QAP-style node permutation as primary inference).

The item is gated. Its required standard is therefore: check the gate honestly; only if it is met, lock a prereg before any outcome.

## Gate criteria (fixed before searching)
A dataset qualifies only if all four hold: (G1) public, downloadable without sign-in or paywall; (G2) whole network inside one
organization with at least two real reporting units (manager-led subtrees), not offices or locations; (G3) a tenure or seniority
attribute per person; (G4) two directed name generators that separate a shared-environment question (customers, markets,
regulation, other units) from an own-task question (help with your own work). Also not previously analysed in VIGIL_ONA
(Krackhardt high-tech, Lazega, Cross & Parker consulting and manufacturing; Krebs IT dropped there).

## What was searched (this run)
1. **Netzschleuder full catalog** (`https://networks.skewed.de/api/nets?full=True`, fetched 15:57 ET, 811 networks, sha256
   be02a352…88d0, not committed: 142 MB). Keyword screen on titles and descriptions (organiz, employee, firm, company, manager,
   corporat, workplace, office, advice, coworker), then descriptions read for every organisational candidate.
2. **networkdata R package index** (schochastics.github.io/networkdata, 990 entries), same keyword screen.
3. **Three web searches** for deposited intra-organisational whole-network data with tenure and reporting lines (Dataverse, OSF,
   Zenodo, openICPSR), and for any public instrument with an environment/market name generator.

## Candidates and verdicts (from the descriptions actually read)
| Dataset | G1 | G2 reporting units | G3 tenure | G4 env vs task | Verdict |
|---|---|---|---|---|---|
| Krackhardt high-tech managers (21) | yes | yes (reports-to, 4 depts) | yes | no (advice, friendship only) | fails G4; already used |
| Lazega law firm (71) | yes | no (office × practice) | yes | no (advice, cowork, friendship) | fails; already used; within-partner check already run by the referee (§2.3, post hoc) |
| Cross & Parker manufacturing (77) | yes | no (location) | yes (banded) | no ("information you use to accomplish your work", "awareness") | fails; already used |
| Cross & Parker consulting (46) | yes | no (location) | no | no | fails; already used |
| Webster accounting firm (24) | yes | no (one firm, job ranks only) | no | no (social, work; observed and reported) | fails G2–G4 |
| Australian bank branch (11; Pattison et al. 2000) | yes | no (one branch) | no | no (advice-seeking, satisfying, confiding, friend) | fails |
| Manufacturing company email (167; Michalski et al.) | yes | partial (hierarchy levels published separately) | no | no (email, no question) | fails G3, G4 |
| Krebs IT department | yes | no usable within-unit rank | no | partial (a CUSTOMER item, truncated for executives) | fails; dropped before VIGIL_ONA lock |
| Thurman office, Kapferer tailor, bank wiring room, sawmill, Bernard–Killworth office/tech, SocioPatterns offices | yes | no | no | no | fail |
| SynthONA (Dataverse doi 10.7910/dvn/pp5ung) | yes | yes | yes | — | **synthetic, not observations**: cannot test anything |
| Burt's bank / software / supply-chain surveys; NIST Interactions Survey (NIST IR 8375); Italian aerospace (Creativity and Innovation Management, doi 10.1111/caim.12434); Chinese hybrid-work department (JCMC, doi 10.1093/jcmc/zmad025) | **no** (no public data link found) | — | yes | not established | fail G1 |

## Result
**Gate NOT MET.** No public dataset found that has tenure, real reporting units and a shared-environment vs own-task contrast.
The closest (Krackhardt) has tenure and reporting lines but n = 21, one advice item, and was already used. No outcome data were
downloaded or analysed, so no prereg was needed or written. This is a search result, not evidence about vigilance: **vigilance
(H8) stays OPEN**; no CLAIM_MAP status changes.

Limits: the search covered two catalogs and three web queries in about ten minutes; it did not cover the UCINET/Pajek archives
page by page, ICPSR's full catalog, or data available on request from authors (requests would be outgoing messages and need
Chad's go). Absence from these sources does not show that no such dataset exists.

## What would meet the gate
Primary collection is the realistic route: a short locked instrument (two name generators, tenure and reporting line from records,
QAP primary inference) given to a real organisation. That needs Chad's decision and a willing organisation, so it is logged as a
new item (ONA-INSTRUMENT-DRAFT: draft and lock the instrument and analysis code on synthetic data only; no contact with anyone).
