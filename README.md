# A Theory of Adaptive Organization (GTAO)

Author: Chad Mitchell — X: [@torusflow](https://x.com/torusflow). *Public working draft. Not peer reviewed, not independently reviewed as a whole. Public domain (CC0).*

> **The claim is that one cost under the second law sets how adaptive systems should be built at every scale: layered, with the layers at the world's time scales.**

One layer for each separated time scale the world changes on that the stakes can pay for, each with a memory set by that scale and the sensing noise. The cost is the **master equation**: choose the design 𝒟 (how many layers, what each tracks, how it senses, what it shares) to

$$
\min_{\mathcal D}\; \kappa\, I_{\text{mem}} + h\,K \;+\; w\,\mathbb E[\ell_{\mathcal D}] \;+\; A(\mathcal D) + L(\mathcal D) \quad \text{subject to}\quad P(\text{ruin}) \le \varepsilon_r
$$

holding memory, being wrong or late, and acquiring and sharing information, without going broke, in the system's own currency.

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

Here *minimize* means: sit near the minimum of J, given their measured world. It is a bet, untested and not yet earned; THEORY §3 lists the tests that would make it a law or kill it.
 The world enters as a **measured input**. A wrong picture of the world means re-measuring and getting a new design; a wrong or missing cost kills the theory.

The theory is a definition (that cost), a principle (strongly selected systems sit near its minimum; untested, not refuted) and theorems (proved in-model): a best design exists; layers never fall as stakes rise relative to upkeep; one time scale needs one layer, even a random walk; J separated time scales need J layers once stakes clear a threshold; and survival is free above a buffer and decides the design below it. The parts are known and credited; the claim is new. What is established is a principle and in-model theorems, not a law. No field test has yet measured its quantities validly, so every field result is "passed / failed on proxy".

**[`THEORY.md`](THEORY.md) is the one canonical statement of the theory (v2.1 draft, 19 November 2026, America/New_York).** Its main text reads in about 15 minutes.

## Reading paths

| You want | Read |
|---|---|
| The idea in five minutes | THEORY §1–§4 |
| The theorem and its special cases | THEORY §5, Appendix B.9; [`theory/MASTER_EQUATION.md`](theory/MASTER_EQUATION.md), [`theory/LAYERS.md`](theory/LAYERS.md) |
| To design or diagnose an organization | THEORY §7 |
| To test or kill it | THEORY §8; [`measurement/FRAMEWORK.md`](measurement/FRAMEWORK.md) |
| Scope, caveats, credits | THEORY §9–§10 |
| One status per claim | `measurement/CLAIM_MAP_v2.md` (v2.50) |
| Where the work stands | [`STATUS.md`](STATUS.md) |
| Earlier versions (v2.0, v1.4.29) and the changelog | [`reference/`](reference/) |

## Repository layout

```
THEORY.md         The theory, v2.1 draft (start here)
STATUS.md         Where the work stands (rewritten, not appended)
reference/        Frozen THEORY v2.0 and v1.4.29, and the changelog
measurement/      FRAMEWORK (validity gates MV1–MV10) and CLAIM_MAP_v2 (one status per claim)
theory/           Derivations THEORY cites, with their code checks
tests/, prereg/   Preregistered tests: predictions, code, results
reviews/          Reviews, with independence stated per file
litmap/           Literature map, prior art, threats, verified DOIs
process/          The work queue and its ledger
history/          Superseded briefs, posts and long-form pages (not maintained)
applications/     Applications (AI memory; Looper; ants), kept separate from the theory
tools/            check_consistency.py: run before and after any doc change
```

AI agents helped draft, compute and review these files under the author's direction. License: [CC0 1.0](LICENSE.md).
