# A Theory of Adaptive Organization (GTAO)

Author: Chad Mitchell — X: [@torusflow](https://x.com/torusflow). *Public working draft. Not peer reviewed, not independently reviewed as a whole. Public domain (CC0).*

**[`THEORY.md`](THEORY.md) is the one canonical statement of the theory (v2.0 draft, 19 November 2026, America/New_York).** Its main text reads in about 20 minutes; the appendices hold the notation, the proofs and a claim index. Where anything else disagrees, it governs.

## The idea in one screen

Everything obeys the second law. Things last in one of three ways:

| Way to last | What it pays | Does a model of the world pay? | Examples |
|---|---|---|---|
| **Keep** (frozen) | Nothing | No: nothing it does changes whether it lasts | Atoms, crystals, a virus particle |
| **Hold** (self-regulating) | A steady flow of energy | No: it regulates itself but anticipates nothing outside | Stars, flames, hurricanes |
| **Know** (tracks) | A flow *and* the cost of staying matched to a changing world | Yes, once acting late is costly | Cells, people, ant colonies, firms, cities |

**Judgment** is carrying a model in order to act ahead of the world. The theory's claim: judgment costs **one bill in three parts**: (1) holding memory, (2) being wrong or late, (3) the reads and effort that keep the memory fresh. The risk of ruin comes on top. The bill is priced the same way at every scale; only the currency changes (heat in a cell, attention in a person, money in a firm). Designs that last under strong selection sit near its balance point. From that come buildable rules, such as when to keep, check or let go of a fact, how often to look, when to share a model, who must be in charge and how far one tracker can reach, and tests at every scale that can kill the theory.

Most of the pieces are known and credited (THEORY §8). The synthesis is what is new. **It is a theory, not a law. Its bet about real systems is untested, not refuted:** no field test has yet measured its quantities validly, and every field result so far is labeled "passed / failed on proxy" (THEORY §7).

## Where to go next

| You want | Read |
|---|---|
| The theory | [`THEORY.md`](THEORY.md) (§0–§9; Appendix B for the proofs) |
| Where the work stands, and what is next | [`STATUS.md`](STATUS.md) |
| One status per claim | `measurement/CLAIM_MAP_v2.md` (v2.49) |
| How quantities must be measured | [`measurement/FRAMEWORK.md`](measurement/FRAMEWORK.md) |
| The earlier long version, full prior-art list and changelog | [`reference/`](reference/) |

## Repository layout

```
THEORY.md         The theory, v2.0 draft (start here)
STATUS.md         Where the work stands (rewritten, not appended)
reference/        Frozen THEORY v1.4.29 (with a section map) and the changelog
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
