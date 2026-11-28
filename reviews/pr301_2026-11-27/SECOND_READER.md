# Second reader, PR #301 (head read: 141438fdb335f2c8326c74760d6cb3802a48c17a)

*Friday 27 November 2026, America/New_York. Full diff and every touched file read on a fresh clone; the author's report was not used as evidence.*

**Units.** Checked by hand with \(V=wp\) (currency per time), \(s=\sigma^2/g^2\) (per time), \(k\) currency, \(T\) time: the held cost \(c+k/T+VsT/6\), the hold rule \(V>c+2\sqrt{kVs/6}\), \(T^*=\sqrt{6k/(Vs)}\) (time), the band \(b^*/g=(6ks/V)^{1/4}\) (pure number, and \((b^*/g)^2/s=T^*\)), the fixed clock \(\sqrt{2k/(Vs)}\) with cost \(\sqrt{2kVs}\), and the range \(V\ge 6ks\). Both worked examples recomputed: 3.394 > 3 with band 0.946 (drop), and 1.816 < 2 (hold).

**Lean.** `post_hold_iff`, `post_band` (WEAKER), `share_cost`, `share_overpay`, `specialist_beats_iff` (refresh terms only, as labelled), `fixed_hold_rule`, `printed_example_flips`, `corrected_example` state what their names and labels say. `tools/check_lean.sh` at nice 19 in `/tmp/gtao-lean`: build OK, AxiomAudit 2342; `#print axioms` on all 31 MemoryRule declarations gives only `propext`, `Classical.choice`, `Quot.sound` (`axioms_MemoryRule.out`).

**Fixed on the branch.**
1. `MEMORY_MISS_COST_BOUNDS` §8, §11, §12, §14 still had \(w\sigma^2T/6\); the PR's note read that \(w\) as the drift weight, which made §11's \(wp-c-2\sqrt{kb}\) mix two units. Now \(wps\,T/6\) with \(w\) the stake; Proposition 10's ratio \(1/\sqrt{1+\rho/w}\) is unchanged.
2. `UFR_FORGETTING:112` carried \(\sqrt{6k/(w\sigma^2)}\); corrected on the same line with a dated note.
3. Five more hash-locked lines copy the old rule (`TRACKABLE_WORLD.md:16`, `prestatement_block.md:8`, `tw_check.py:4-5`, both `NEXT_ROUTES` files at :48); errata rows added, M45 lists them. Locked hashes verified unchanged.
4. The MemoryRule module note still said §4 writes `a = w` and that the theorems hold "under either reading"; reworded.
5. `GROK_BOT_MEMORY:57`: the printed example's free band \(1.5^{1/4}g\) is past the quadratic range; the capped band \(b=g\) costs \(11/6<2\), so the hold conclusion stands (as `printed_example_flips` already checks).
6. Merged main (`a1f5bd5`, #298); one conflict in `process/FAILURES.md` (both sides appended rows), resolved by keeping both.

Every other \(\sqrt{6k/(w\sigma^2)}\) in the repo uses the theory's \(w\) (loss per squared gap per time, `theory/LAYER_LIFETIME_2026-11-21.md`), where it is correct.
