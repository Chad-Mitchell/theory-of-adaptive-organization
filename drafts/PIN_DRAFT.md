# Draft: replacement pinned post for @torusflow

*Draft only, 27 November 2026. Nothing here is posted. The pin is Chad's; it goes up only after he approves the exact text on a post card. The text below the line is the post; everything above and after it is notes.*

**What changed from the live pin** (https://x.com/torusflow/status/2125614287997534386, posted 25 Nov 2026 10:35 ET), following the judgment framing check of 27 Nov 2026:

- Date line: 25 Nov → 27 Nov 2026, and it now replaces the 25 Nov pin.
- "What holds": the stake result moves from item 3 to item 1, with the CT2 sentence added (a ruin cap that acting blind cannot meet needs memory at any price; `THEORY.md:269`). Old items 1 and 2 follow, word for word. Items 4 to 7 are unchanged. A new item 8 states the swarm rule (`README.md` §The swarm rule; `theory/SWARM_RULE_2026-11-23.md`).
- Lean count: 1,370 → 2,285 declarations. Source: `formal/lean/AUDIT.json` on `main` (`8b4d5a13dc52f4ef3a84204478826f7ac6c11f98`, 27 Nov 2026 13:49 ET) records `audit_count` 2285, and `tools/check_pending.py` confirms the Lean sources still hash to that audit. Not re-run in this PR. This is a raw declaration count; `formal/lean/README.md` warns that raw counts are not a measure of depth.
- Credit: the telegraph floor's divergence step is KNOWN (Gilardoni 2006; Sason 2015), as `CORE.md:74` now says.
- Evidence: the latest open misses are named (two-route A-T2, who-copies-whom, the Hutter map, the composite contest T72), each with its row in the headline ledger.
- Closing line: "physics may be the minimum-cost way for a universe to keep track of itself" is replaced by the open question below. Keeping track with no decision is the case where, by CT5, holding never pays, so the old line described a case the theory gives no value.
- Re-check before posting: the Lean count and the date, against `main` on the day.

---

A Theory of Adaptive Organization: where it stands (27 Nov 2026). This replaces the 25 Nov pinned summary.

The idea: anything that must act before its world arrives (a cell, a brain, a team, a firm, an AI system) faces a cost of judgment: being wrong or late, plus the cost of holding, getting and sharing information, under a cap on the chance of ruin. In the physical models where it is proved, the memory part is heat. In worked cases, minimizing it gives the design: how much to remember, how many layers, what to share, when a boundary is enough.

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

That sentence is a bet about nature. It is untested, and no real system has yet been shown to qualify for a test.

What holds, inside stated math models (not real systems):

1. Memory pays only when the stake on being wrong is high enough against its price. Below that threshold the cheapest design remembers nothing. A ruin cap that acting blind cannot meet is the one exception: then some memory is needed at any price.
2. Tracking a changing world costs heat: at least kT times the net rate at which the memory learns that world. This is published physics for bipartite jump processes (Horowitz and Esposito 2014) and proved here for additive-noise diffusions.
3. Storage is cheap; tracking change is what costs. A record of an unchanging world can be kept at vanishing ongoing heat after a one-time write.
4. How the cost grows with the stake depends on how the world moves. In continuously drifting worlds the minimum cost grows like the square root of the stake. In worlds hit by rare reset shocks it grows only like its logarithm at high stakes, and the best memory keeps a small uncommitted reserve.
5. When a system steers its world, the heat bound on learning still holds, but there is no design-independent floor on memory heat alone. Some steering designs have vanishing ongoing memory heat; in the linear-feedback class, acting does not cut the tracking floor, and acting costs heat of its own.
6. Predictable rhythms add a cost the basic floor misses: once looks are costly enough, a memory that keeps the beat between them needs an internal clock, and clocks cost heat.
7. Where no formula exists, selection acts as a search scored by the cost. It settles near the minimum only under four conditions: strong selection, a reachable minimum, a cost that counts everything that matters, and a coupling that settles.
8. The swarm rule: a part keeps following a whole only while the whole's signal changes slowly enough against the part's own stake in it, and the part's choice is the whole's when each part's share of the cost matches its share of the stake. Proved in its stated classes; reading it onto cells, people or AI agents is interpretation.

How strong the evidence is:

- 2,285 Lean declarations are machine-checked, covering the core finite-menu results, the refresh time, the layer count, the selection gap, and some physics steps: the two-state heat floor, the finite-state pairwise and path bounds, and the telegraph lower bound. Two physics formalizations came in weaker than the paper sentences and are logged as open misses: the diffusion heat step takes two integral identities as assumptions rather than deriving them, and the many-carrier repair inequality is proved only for strictly positive distributions. The general heat floors, the acting-world results, the area-scaling results, and the physical argument as a whole are not formalized yet.
- The telegraph floor's divergence step is published (Gilardoni 2006; Sason 2015) and is credited as such.
- AI agents helped draft, compute and review this work under the author's direction; all reviews so far are by one bot family. No human expert review; not peer reviewed.
- In simulations of our own model worlds, selection reached the predicted minimum in clean worlds and missed where the world added an obstacle. Several locked predictions missed, among them the two-route heat ratio, who copies whom between two judges, the Hutter Prize map and the composite contest; each is an open miss with its row in the claim ledger, and the work continues from them.
- Real data: no qualified real-world test yet. Every scored field result so far is not a test or inconclusive.

Physics edges (open):

- The cost alone does not cap static records by surface area: they pack by volume at zero ongoing heat.
- Leaky records pay steady repair heat; self-correcting media, such as cold magnet-like materials in 2D or 3D, can hold a record passively for any fixed time at zero ongoing heat.
- Any area cap from gravity needs extra physical inputs, and one of them, that a record's energy barrier is at most a fixed multiple of its mass, does not hold in general in field theory.
- We do not derive general relativity, quantum mechanics, or holography.

Errors: predictions are locked before data. A wrong one is a miss, logged with size and direction (earlier ones sit in the claim map), and the update scales with it.

What to believe now: the math holds inside its models (AI-reviewed, partly Lean-checked). Whether real, strongly selected systems sit at the minimum is open.

Open question, not a result: whether the laws of physics can be read as a minimum cost of judgment, and if so, what plays the role of the stake.

Open and CC0: https://github.com/Chad-Mitchell/theory-of-adaptive-organization
