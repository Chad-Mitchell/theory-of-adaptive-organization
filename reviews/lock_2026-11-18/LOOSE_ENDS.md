# LOOSE ENDS: second- and third-order implications, ranked

19 November 2026, early morning ET (America/New_York). Grok Bot executor for Chad Mitchell, via Ace (pt1957u). **Not independent** (see `README.md` in this folder). **Every item here is a HYPOTHESIS.** None is a result, and none changes a status in `measurement/CLAIM_MAP_v2.md`. Three items that could be stated precisely are added as OPEN rows (N51–N53, CLAIM_MAP v2.46). The rest stay here, because they are too loose to score.

**How these were found.** Each THEORY rule was taken one step further than the repo takes it (second order: what follows for a system that obeys the rule) and then two steps (third order: what follows for the systems around it). That was done at each scale: cell, person, firm, institution, AI system, cosmos. Every candidate was then checked against the prior art already in the repo (THEORY §12, `litmap/`), plus a short search per item. Citations not already in the repo were checked this session against the publisher or indexing page; the ones read only in a secondary source are marked [SEC]. No full prior-art sweep was done for any item, so "novel" below means **"not found in a short search"**, never "new".

**How they are ranked.** Three things are weighed:
- **(T) Testability:** can the inputs be measured, and the test run in months with data or a lab that exists?
- **(G) GTAO-specific content:** what is left after crediting the prior art?
- **(C) Consequence:** would the result move the core bet (N13, J6) or one of its rules?

## Ranked shortlist

| Rank | Loose end | Follows from | T | G | C | CLAIM_MAP |
|---|---|---|---|---|---|---|
| 1 | Human attention follows the spectrum exponent 1/α, not a universal ½ | §2.2 read-rate rule | high | medium | high | **N51** OPEN |
| 2 | Cheap lookup dissolves shared-memory levels but not enforcement levels | T8 lookup edge (F13) + J9 | medium | medium | high | **N52** OPEN |
| 3 | Delegation in firms rises with local drift and with latency to the centre | LAT-1 (N27) | medium | low–medium | medium | already **N27** |
| 4 | Rules vs standards as freeze vs lookup, with drift as the missing variable | T8 (F13) | medium | medium | low–medium | **N53** OPEN |
| 5 | Co-adapting trackers raise each other's drift, so read spending escalates | §5 drift reduction; N47 endogenous drift | low | low–medium | medium | not added |
| 6 | An AI multi-agent testbed with explicit prices | whole §2.2 | high | low | medium | not added |
| 7 | Transitions to a new level need shared drift above the T3a threshold *and* aligned fate | T3a (§6) + J9 | low | medium | medium | not added |
| 8 | Science as an adaptive organization: replication is an under-supplied shared read | J9 | low | low | low | not added |
| 9 | Ageing and death as model replacement | §2.2 hold vs replace; T8 | low | low | low | not added |
| 10 | Markets: costly reads keep prices partly stale | §2.2 read rule | low | low | low | not added |
| 11 | The cosmic endpoint: trackers federate into islands | LAT-1; §2.3 ends | none | low | none | not added (classification) |

## The items

### 1. Attention as model upkeep (person scale) → N51
- **Follows from:** THEORY §2.2. With exact reset reads, the read rate ∝ (w·q/c)^{1/α}: elasticity 1/α in stakes w and drift level q, and −1/α in the price c of a read.
- **Second order:** a person deciding how often to check a drifting quantity should change their checking with stakes by a factor that depends on *how the quantity drifts*, not just how fast.
- **Third order:** feeds, dashboards and notification designs that fix one check rate for all sources overpay for smooth sources and underpay for rough ones. Here "smooth" means α > 2 (most variance at slow timescales) and "rough" means α < 2.
- **Prior art:**
  - Sampling rate proportional to signal bandwidth in instrument monitoring (Senders 1964, [SEC]: read in a secondary source only).
  - How often a supervisor should sample (Sheridan 1970, in THEORY §12).
  - The √ rule and rational inattention (Reis 2006; Sims 2003).
  - Costly-sampling lab paradigms (Juni, Gureckis & Maloney 2016, *Decision* 3:147–168, doi 10.1037/dec0000045).
  - The repo's own LAB-AKLMT-TAU proxy test.
- **GTAO-specific:** the stakes and price elasticity is 1/α and so *varies with the measured spectrum*. The √ rule is the α = 2 case.
- **Test:** an online lab task. Participants pay per look to observe a hidden process with a power-law spectrum, α ∈ {1.5, 2.5}, with stakes and look price varied in a factorial and α measured from the generated paths. Train to a preregistered criterion, then measure look rates.
- **Kill (for learned human sampling, not for N13):** the stakes elasticities at α = 1.5 and α = 2.5 are not separated in the predicted direction, or both are consistent with ½, at the preregistered power (MV10).
- **Honest limits:**
  - People in a lab are learners, not a strongly selected system. A miss is evidence against the relation in learned behaviour; it does not count against N13.
  - The training criterion must be locked before data, so a miss cannot be explained away as "not trained enough" (the anti-rescue rule, FRAMEWORK).

### 2. Cheap lookup and the levels that survive it (firm, AI) → N52
- **Follows from:** T8 (F13). When lookup gets cheap relative to holding, facts move past the lookup edge and nobody needs to hold them. Shared-memory levels exist to hold shared facts (T3a), so they lose their reason. Levels that exist for enforcement under unaligned fate (J9) do not, because looking a fact up does not align anyone's fate.
- **Second order:** when lookup cost drops (search, retrieval, AI assistants), relay and coordination layers shrink. Audit, compliance and accountability layers do not shrink, and may grow as a share.
- **Third order:** hierarchy that survives cheap information is mostly about enforcement and shared fate. Debates about "AI flattening organizations" should split layers by function before predicting.
- **Prior art:**
  - Bloom, Garicano, Sadun & Van Reenen 2014 (*Mgmt Sci* 60:2859): information technology decentralizes and communication technology centralizes.
  - Garicano 2000 (knowledge hierarchies).
  - Both are in THEORY §12. The direction for information layers is therefore prior art.
- **GTAO-specific:** only the contrast between memory-pooling and enforcement layers. Whether that contrast is already in the organizational-economics literature was not checked beyond these two papers.
- **Test:** firm or agency panels with a dated drop in lookup cost and role-level headcount coded by function (information relay or coordination versus audit, compliance or enforcement).
- **Kill:** after the drop, the two classes do not diverge in the predicted direction, or enforcement layers shrink at least as fast as relay layers.

### 3. Delegation rises with local drift and latency (firm) → already N27
- LAT-1 says a tracker of extent L holds its target only while q(L/c)^{α−1} is under tolerance, so P(central) should fall with q·ℓ^{α−1}. At firm scale, ℓ is the decision latency to the centre and q is the local drift.
- **Prior art:** Acemoglu, Aghion, Lelarge, Van Reenen & Zilibotti 2007 (*QJE* 122:1759) find decentralization in firms facing newer or more heterogeneous conditions; Hayek 1945.
- **GTAO adds:** the α-dependent exponent and the latency term. N27 already says this and is OPEN, so no new row was added. The firm-scale version is the cheapest route to a first N27 test, provided α and q can be measured for the local conditions.

### 4. Rules versus standards (institutions) → N53
- **Follows from:** the three-way T8 map.
  - A **rule** fixed in advance is a *freeze*: it is paid for once and goes stale as conduct drifts.
  - A **standard** applied case by case is a *lookup*: paid for at each use.
  - A rule **revised on a schedule** is the *hold* band.
- **Prior art:** Kaplow 1992 (*Duke LJ* 42:557–629). Rules pay off when conduct is frequent, because their cost is paid in advance; standards pay off when it is rare.
- **GTAO adds:** drift as a second variable. At fixed frequency, faster drift in the regulated conduct should shift law toward standards or toward rules with scheduled revision (sunset or review clauses).
- **Novelty:** not found in a short search; the law-and-economics literature on legal obsolescence was **not** swept.
- **Test:** a preregistered cross-domain sample. Code rule versus standard and revision clauses; measure the drift in the regulated conduct independently (for example, the rate of change in the technology regulated) and its frequency.
- **Kill:** no partial association with drift, or the opposite sign.

### 5. Red Queen escalation (lineages, firms)
- Trackers that co-adapt are each other's drift (Van Valen 1973, *Evol. Theory* 1:1–30). GTAO's §5 says reducing drift substitutes for watching it, and N47 treats drift as endogenous. In an arms race, each side's tracking raises the other's q, so total read spending should rise until it is limited by price.
- That much is the Red Queen restated with a cost ledger. A GTAO-specific prediction would need a model of how one side's read rate sets the other's q, and that model does not exist. Not added as a row.

### 6. An AI multi-agent testbed with explicit prices
- Language-model agents can be given a drifting world with chosen α and q, explicit prices for memory, reads and errors, and a selection loop (keep the best configurations). This is the only setting where every input of N13 is set and known.
- **Limit:** an optimizer selecting designs under known prices finds the in-model optimum almost by construction, so this tests the search more than the theory, as POOLSIM's circularity did. It is useful as a calibration of a measurement pipeline before field work, not as evidence. Not added.

### 7. Transitions to a new level (cells to multicellularity; firms to alliances)
- **Follows from:** T3a. A shared level pays once N > (√(1+ρ)+1)²/ρ (at zero upkeep), and J9 says the level also needs aligned fate or enforcement. Together they predict that new levels appear when *both* hold.
- **The available evidence fits badly.** Experimental multicellularity under predation (Boraas, Seale & Boxhorn 1998, *Evol Ecol* 12:153; Herron et al. 2019, *Sci Rep* 9:2328) is a size refuge, not a shared model, so it does not test T3a.
- A cleaner test would need a system whose shared and private environmental variance can be measured and varied, such as quorum-sensing investment under manipulated shared versus local signals. No such dataset is known here. Not added.

### 8. Science as an adaptive organization
- Replication is a read of a shared memory (the literature). J9 says such reads are under-supplied unless privately rewarded, and are then made up by shared fate or by enforcement (mandates, registered reports).
- This is the public-goods account of replication restated. GTAO adds nothing testable yet. Not added.

### 9. Ageing and death as model replacement
- A held model goes stale. When the world drifts fast relative to the cost of repair, replacing the holder (reproduction) can beat maintaining it.
- **Prior art:** this sits next to the disposable-soma theory (Kirkwood 1977, *Nature* 270:301–304), which already prices maintenance against reproduction. The GTAO twist, environmental drift as the driver, is confounded with extrinsic mortality in any comparative test. Not added.

### 10. Markets
- The read-rate rule applied to traders gives partly stale prices whose staleness grows with the read price. That is Grossman & Stiglitz 1980 (*AER* 70:393–408) plus a spectrum exponent. Not added.

### 11. The cosmic endpoint
- In an accelerating universe, the bound group a future observer can reach shrinks to an island, and evidence of the expansion becomes unobservable (Krauss & Scherrer 2007, *Gen. Rel. Grav.* 39:1545–1550).
- Under LAT-1, every tracker then federates into islands, and the outermost lookup edge is the island's horizon. This is a **classification** given published cosmology, like N25 and N26: no data could fail it. It is listed so that GTAO is not "silent" at the largest scale, and it is not a hypothesis that can be tested.

## Self-application (third order, about this project)

Theorem G says a checked copy beats letting a fact fade only while drift × check cost is below the fact's value; past the freeze edge, freeze it. The repo's own ledger fits that pattern:
- Six of the first eleven scored outcomes on 15 November are logged as changing the claim map.
- In the next 40 scored outcomes (12:45 PM ET to the end of 15 November), no existing row changed status; four only added new rows (N18, N21, N22, N23). The only later logged change was SENSE-CELL-REFEREE on 18 November, which was unscored.

Read through GTAO's own lens, the canonical text's drift rate has fallen below what continued rewriting costs, which argues for **freezing** it (a lock and a v1.5 tag) and moving the spend to measurement. This is a heuristic, not a test, and `PROCESS.md` §4 states the count's limits.

## Candor

- These items came from one executor in one night. Several (5, 8, 9, 10) are mostly restatements of known ideas. The ranking reflects how cheaply each could be tested, not how important it is.
- Items 1 and 2 are the two most likely to be wrong *and* informative, which is why they rank first.
- None of the CLAIM_MAP rows added here has an independent review. Each needs prior-art sweeps and MV1–MV10 gates before any preregistration.
