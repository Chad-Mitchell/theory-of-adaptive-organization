# Memo (HYPOTHESIS): the Hutter Prize budget as a test of the cost of judgment

*Wednesday 25 November 2026 (America/New_York). Branch `forge-hutter-test`. Everything here is a **HYPOTHESIS** or a reading of the scored record in `RESULTS.md`; nothing here is a field result. Internal work: no prize entry, no public claim. `THEORY.md` and `CORE.md` are not edited.*

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

## 1. The map

The prize scores \(S=S_1+S_2\): the program that rebuilds enwik9 plus the archive it reads (`PREREG.md` §1). The cost under test is \(J=\kappa I+q\,\kappa\,P_D+w\,L\). At zero residual (exact rebuild), the priced decision is the next-symbol forecast, its loss is the log loss, and the archive is that loss in bytes, so \(wL=S_2\) with \(w=1\). The program is the memory held before reading, so \(\kappa I=S_1\) with \(\kappa=1\). The record is classical, so \(P_D=0\). The caps (about 50 hours on one core, 10 GB RAM, 100 GB disk, no GPU) are the ruin set, outside the sum. So \(J=S\) under the caps (`PREREG.md` §2).

That makes J and two-part minimum-description-length coding (Rissanen 1978) the same number. It also makes J the contest's own selection criterion. A record sitting near a minimum of S is how the contest works. It says nothing about the hypothesis sentence. Only design structure could test anything, and four structural predictions were locked before the designs were read.

## 2. What happened (updated after gate read and P1 re-score)

| Item | J's bet | Outcome | Who was right |
|---|---|---|---|
| P1 memory split | largest component ≥ 40% of runtime RAM | **hit** (allocation fallback `0.709` for PPMD; `≥ 0.41–0.46` in RAM with residency caveat) | J (allocation constants; R-RI matches) |
| P2 online vs frozen | shipped trained weights ≤ 1% of S | **miss**: 2.92% (one copy, scored); S counts two copies (5.84%) | rival: ship pretrained weights |
| P3 mixing vs single | ≥ 10 components, learned context-selected mixing | **hit**: 460 inputs, 23 + 1 mixers, then SSE (low information) | J, against the single-model rival |
| P4 program share | 0.1% to 2% of S | **miss**: ≥ 2.92% (decompressor); 3.41% (compressor) | rival: ship pretrained weights |

Overall: **open miss** under the locked rule (`PREREG.md` §4). Condition (i) of the overall rule (at least two of P1–P4 hit) is met by P1 and P3, while condition (ii) fails: no unused J-implied design choice was found, and E1 was stopped at the gate and withdrawn.

## 3. Diagnosis

The record's gain over fx2-cmix came from one change: the online LSTM was replaced by a 6-million-parameter transformer trained offline on 8 GPUs for 26 hours, quantized, and shipped as 2.9 MB of weights in each binary (`RESULTS.md`, P2). Its documentation names the trade: online training saves the weights' size but spends run time, so it limits the model's size and how long it can train (`writeup.md:17` in the record's repository).

The map in §1 priced shipped bytes at 1 and run-time memory at 0 below the cap. It left out a third resource, **offline compute**, which the contest does not price at all. With offline compute free, the minimum moves learning out of the decoder and into shipped weights whenever a byte of weights saves more than a byte of archive. Here about 5.9 MB of weights (two copies counted in S) came with an archive 13.4 MB smaller. That is the trade J was mapped to see, and the map pointed it the wrong way because a price was missing, not because the cost was summed wrongly. **Location: model** (the map, a Part-2 reading), not the in-model mathematics.

This is a miss of the map, and it is also the general limit the task warned about. J reproduces the trade between program bytes and archive bytes, and so does MDL. Neither tells you how to build a smaller compressor.

## 4. Unused design choice and experiment: none found

The inaction-band idea from J (CL19, `measurement/CLAIM_MAP_v2.md:580`) was checked against the record and is **already in use** there:

- **Inner mixers (`fxcm`).** The live `train()` at `src/models/fxcmv1.cpp:504-517` opens with `if (e) {` (`:506`). When `err` is zeroed inside `[-elim, elim]` (`:554`), the weight loop is skipped completely, matching the comment at `:4698-4699` ("less updates and better speed"). (An earlier draft cited a commented-out `train()` at `:536`; that error is corrected in `RESULTS.md`.)
- **Outer mixers.** `src/mixer/mixer.cpp:75-77` returns early when `fabs(update) < 5e-12f` and `extra_inputs_size_ > 0` (`mixer_0_[1..22]`), though with a near-zero width.
- **Outside compression.** Selective backpropagation skips low-loss examples to save training time (Jiang et al. 2019, arXiv:1910.00762).

**Post hoc note, not a hit.** Because the record's adaptive inaction band was not preregistered, its presence is an observed match labeled **post hoc** and is not counted as a hit for J.

**E1 withdrawn.** The independent gate read stopped E1 (`GATE STOP`: the G3 rival was contradicted by prior art, the stop rule and implementation details were underspecified, and the 36.5 h decode time leaves slack under the ~49–53 h cap, giving update time a shadow price near 0). E1 was not a locked prediction and was never run; it is withdrawn. **New J-implied design choice not used by the record: none found.** Per the task rule, we say so and stop.

## 5. Next test (HYPOTHESIS, not locked)

Give the map three prices: shipped bytes 1, run-time memory 0 below the cap, offline compute 0. Inference time grows with the shipped model, and the record used about 36.5 of roughly 49–53 decoding hours (LTCB). The three-price map then predicts that the shipped model grows until one more byte of weights saves no more than one byte of archive, or until decoding time binds, whichever comes first. The record's repository holds unshipped 8M and 10M checkpoints (`models/8m.tch`, `models/10m.tch`). A new prereg, locked before reading why they were not shipped, could score that. It would still be a reading of the trade, not a compressor.

## 6. Ledger and queue

- `OPEN_WORK.md` §3, row HUTTER-J: open miss, as above. (`OPEN_WORK.md` is retired on `main`; the row now lives in the README open table as HUTTER-J.)
- **DATA-ONE: not a candidate.** The cost-to-fitness map is S itself, and no scored item excluded both MDL and the engineering rivals (`PREREG.md` §4).
- `measurement/CLAIM_MAP_v2.md`: no ledger status changes. No row claims anything about compressors, and HYP stays "no qualified real test". `theory/GAP_PLAN.md`: no matching row, so it is unchanged.

## References

- Rissanen, J. 1978. Modeling by shortest data description. *Automatica* 14(5):465–471. doi `10.1016/0005-1098(78)90005-5` (Crossref, `crossref.out`).
- Sims, C. A. 2003. Implications of rational inattention. *Journal of Monetary Economics* 50(3):665–690. doi `10.1016/S0304-3932(03)00029-1` (Crossref, `crossref.out`). It was named as a rival in P1 and the withdrawn E1. It did not separate from J in P1, and E1 was not run.
- Delétang, G., Ruoss, A., et al. 2023. Language Modeling Is Compression. arXiv:2309.10668. Background for the ship-pretrained-weights rival.
- Jiang, A. H., Wong, D. L.-K., Zhou, G., Andersen, D. G., Dean, J., et al. 2019. Accelerating Deep Learning by Focusing on the Biggest Losers. arXiv:1910.00762.
- Record: `https://github.com/astOwOlfo/fx2-cmix-transformer-v1` at `83f2603`. Benchmark: `https://mattmahoney.net/dc/text.html`. Prize: `https://www.hutter1.net/prize/hrules.htm`, `https://www.hutter1.net/prize/index.htm`.
