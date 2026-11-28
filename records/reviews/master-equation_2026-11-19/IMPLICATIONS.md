# IMPLICATIONS: if the claim holds, what follows

> **Repository copy (added 19 Nov 2026 with THEORY v2.1).** A dated working record, copied from the working directory with paths updated: `checks/` now means `theory/layers_checks/` (layer scripts) or `theory/meq_checks/` (master-equation scripts). Not edited otherwise. THEORY v2.1 governs where they disagree; its framing supersedes this file's on novelty (known parts, new claim), applicability (general; the bottleneck is measurement) and responsive worlds (an open theorem, CX2, not a scope limit). Message ids such as t1973u are the author's chat references.


Written 19 Nov 2026, about 11:15 PM ET. Read-only. Locked claim (Chad, t1969, wording updated t1971; verbatim): **"the claim is that one cost under the second law sets how adaptive systems should be built at every scale: layered, with the layers at the world's time scales."**

**Labels.**
- **DERIVED:** follows in-model from a proved result (named).
- **CONDITIONAL:** follows if a named premise or open item holds.
- **SPECULATIVE:** a plausible reading that nothing in the repo derives.

"Should" is normative: it is what the optimum of the cost says. Whether real systems *are* built that way is the open bet (N13).

## 1. What kind of claim this is (by-the-book framing)

- **It is a normative optimality theory plus an adaptationist bet.**
  - The normative half says what design minimizes one total cost of judgment, given a world's spectrum, stakes, prices and upkeep. That half is mathematics and can be proved.
  - The descriptive half says strongly selected systems sit near that optimum, with the same relations (not constants) at every scale. That half is empirical, and it can die.
  - This is the structure of optimal foraging theory and of efficient-coding theory in neuroscience, which are the closest comparables. Neither was citation-checked this pass.
- **How comparable theories were stated and tested.** Citations were checked against Crossref unless marked otherwise; see `checks/cites_crossref.out`.
  - **Simon 1962, "The Architecture of Complexity".** A qualitative argument: hierarchy and near-decomposability make complex systems evolvable and fast inside units, slow between them. It made no quantitative prediction and became influential as a lens, tested indirectly through modularity studies. (Credited in the repo. This pass did not DOI-check it: it has no DOI, and it is JSTOR-hosted.) This claim aims at what Simon did not give: when a layer pays, how many, and at what timescales.
  - **Conant & Ashby 1970, "Every good regulator of a system must be a model of that system"** (verified). This is a theorem, but its proof covers only optimal, simplest regulators (the repo's own note, `theory/THEOREMS.md` l.208–210). The sharper form is Francis & Wonham's internal model principle. This claim's C2 sits in that tradition.
  - **Free-energy principle, Friston 2010** (verified). A unifying principle stated so generally that critics call it unfalsifiable as a principle, so it is tested through specific process models. The lesson: keep the claim at the level of falsifiable relations (read rate ∝ (wq/c)^{1/α}, onset N\*(ρ), layer count against span), not a principle that fits anything. Kiebel, Daunizeau & Friston 2008 (verified) already proposed that the brain's hierarchy tracks a hierarchy of timescales. That is the closest prior statement of "layers at the world's time scales" in neuroscience.
  - **Scaling laws: West, Brown & Enquist 1997; Bettencourt et al. 2007** (both verified). A network-optimality argument yields specific exponents (¾ in metabolism; about 0.85 and 1.15 in cities) and is tested on cross-sectional data across sizes. Both drew strong empirical support and also sustained challenges. This claim's analogue is the onset exponent −(1−b)/(1−a) and the read-rate exponent 1/α: a cross-scale relation with measured inputs.
- **Importance if true (without overclaiming).** It would give a quantitative bridge between three literatures that rarely meet:
  - estimation theory (multi-timescale filters);
  - organization design (when a shared level or a hierarchy pays);
  - biology (multi-timescale memory, hierarchical cortex).
  The bridge would be one cost with measured inputs. Most pieces are known (THEORY §8). What is new is the assembly and the cross-scale bet. If the bet held at two or more scales with measured inputs, it would be a significant unifying result of the scaling-law kind. Until then it is a well-posed program with proved in-model parts.

## 2. Implications by scale

| Scale | Implication | Label | From |
|---|---|---|---|
| **All** | A system that tracks a world with one timescale needs one tracker, however self-similar that world is (a random walk) | DERIVED | PROOF_A L1 |
| All | A world with J separated timescales needs at most J trackers, exactly J once stakes × error ÷ upkeep is high enough; with a continuum, more layers keep paying as stakes rise | DERIVED (linear-Gaussian) | L2, L3 |
| All | A shared layer forms when the group exceeds N\*(ρ) ≈ 4/ρ; cheaper upkeep only adds layers; cheaper lookup can remove holding layers | DERIVED | Result 4; formal Thm 6 |
| All | Beyond L_max = v(D\*/q)^{1/(α−1)} a system federates | DERIVED (in-model); real form N27 CONDITIONAL | Result 6 |
| **Cells** | Signalling and adaptation pathways carry about as many separately timed memory variables as the environment has separated timescales that matter at the cell's stakes; a cell in a near-random-walk environment needs one adaptation timescale | CONDITIONAL (Gaussian/linear premise; stakes in ATP unmeasured) | L1–L3; Lemma B2 |
| Cells | Sensing is where the second-law floor binds (Lan et al. 2012), so the cost of a layer is physically priced there | DERIVED floor + CONDITIONAL scale-up | THEORY §2.3 |
| **Brains** | Intrinsic timescales should be ordered and roughly log-spaced where the stimulus spectrum is broad, and placed near cadences where it has lines. Murray et al. 2014 (verified) found a hierarchy of intrinsic timescales across cortex; whether it matches stimulus spectra at the predicted count is untested | CONDITIONAL | L2–L4; T7 |
| Brains | Synaptic memory with power-law forgetting needs many coupled variables (Benna & Fusi 2016, verified): the known neural instance of L3 | DERIVED in substance (prior art) | L3 |
| **Firms** | Review cadences (daily, weekly, quarterly, annual) are justified where demand and risk have those separated timescales. Adding a management layer pays when the shared share ρ of what members track is large enough for the group size; it does not pay just because the firm grows | DERIVED (onset); CONDITIONAL (mapping) | Result 4; formal Thm 7; L2 |
| Firms | Cheap lookup (search, dashboards, AI retrieval) removes layers that only hold shared facts, not layers that enforce under unaligned fate | CONDITIONAL (N52 OPEN) | Thm 6 lookup case; Result 5 |
| **Cities** | City services should run nested responders matched to the timescales of the demand they serve. NYC 311 shows a break near one day in time and a broad, scale-free spread across categories (DRIFT1, post hoc), so expect a sub-daily layer plus category-level layers at log-spread rates | SPECULATIVE until a city's per-category spectra are measured (G1) | T7; L2; DRIFT1 |
| **AI agent systems** | An agent memory should be layered: a fast working store, slower consolidated stores, and a shared store across agents once N > N\*(ρ). The number of stores grows with the span of timescales in the user's world and with stakes over the upkeep per store; one store suffices when the world is close to a single timescale | DERIVED (in-model) for the design; CONDITIONAL on measured spectra | L1–L3; Result 4; T8 |
| AI agent systems | Each store checks its facts at a rate ∝ (wq/c)^{1/α} and lets facts fade outside the hold band; a store shared by N agents widens the hold band N²-fold | DERIVED | Result 3; T8 |
| AI agent systems | Agents act from the current model, not copies (rule 5), and a federation boundary appears where latency × drift exceeds tolerance | DERIVED | G1; Result 6 |

## 3. What would change in practice (if true)

1. **Design by measurement.**
   - Measure the spectrum of what you track (corners and lines, not just α), the stakes and the upkeep per layer.
   - Then choose the number of layers and their timescales from L2 and L3, and the shared layers from N\*(ρ).
   - This replaces rule-of-thumb hierarchies ("add a manager every 7 people", "review quarterly because everyone does") with computed ones.
2. **Stop layering where the world has one timescale.** Extra layers then cost upkeep and buy nothing (L1).
3. **Expect the gain from time layers to be modest per tracker** (single digits to about 20% of the error cost). The large gains come from shared layers (pooling) and from avoiding ruin. So layering matters most where stakes are high and margins thin.
4. **Expect cheap lookup to flatten information layers but not enforcement layers.** This is a testable prediction for AI adoption in firms (N52).

## 4. What would kill it (part by part)

| Part | Dies if |
|---|---|
| C1 "one cost" | some level's design needs a cost that cannot be booked as holding, error or lateness, reads and effort, or ruin (J16) |
| C2 "under the second law" | (as a physical claim above the cell) the cell test of THEORY l.52 shows the physics adds nothing beyond floors; the claim then survives only as "same form" |
| C3 "sets how … should be built" | the normative half cannot die except by a math error. The descriptive bet dies if strongly selected systems at two or more scales miss their measured-input optimum beyond error and a named rival fits better (THEORY §6) |
| C4 "at every scale" | the relations hold at one scale and fail at another with valid measures (J6) |
| C5 "layered" | layer count does not rise with measured span and stakes/upkeep where the world has many timescales (N4 kill); or shared layers do not appear near N\*(ρ) |
| C6 "at the world's time scales" | measured layer timescales do not follow the measured spectrum: no layer near a strong cadence, or layers where the world has no variance |
