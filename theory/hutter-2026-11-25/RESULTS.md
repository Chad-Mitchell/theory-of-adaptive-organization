# Results: the Hutter Prize budget against the locked prereg

*Wednesday 25 November 2026 (America/New_York). Append-only. Prereg `PREREG.md`, sha256 `501a82ded728e6616393ca88d2bf92114287061e219ecd25cd58680893771a77`, lock commit `4a0d5e9` (11:29:09 ET), pushed to the fork branch `forge-hutter-test` before any design source was opened. Design sources were first opened at about 11:31 ET. Deviations are in `DEVIATIONS.md`. Every line below is labeled **OBSERVED** (read in a named source) or **HYPOTHESIS**. No compression job was run.*

## Sources read after the lock

- **LTCB.** Mahoney, Large Text Compression Benchmark, `https://mattmahoney.net/dc/text.html` (linked from each record row of the prize page), fetched 25 November 2026, HTML sha256 `4d1224b7065dc11c2813c401012843fa9a750385b98809908aa6ba9f10b38889`. Entries used: `.0969 fx2-cmix-transformer`, `.1091 fx3-cmix` (which holds the fx2-cmix text and table), `.1082 cmix`, `.1250 paq8px_v206fix1` (the PAQ series history).
- **Record source.** `https://github.com/astOwOlfo/fx2-cmix-transformer-v1`, the GitHub home LTCB gives for fx2-cmix-transformer ("Moved to Github on Sept. 2, 2026"), commit `83f2603f3f7751da5f429fd32669807eb8510494`. Its `writeup.md` is the record's documentation. The prize page's name for this record is fx2-cmix-T; LTCB's is fx2-cmix-transformer; the size row (24 Jul 2026, total 100,424,672) is the same.

## Scores

| Item | Label | Locked bar | Value | Score |
|---|---|---|---|---|
| P1 | TEST | \(f_{\max}\ge0.40\) | not readable as locked | **not scorable** |
| P2 | TEST | \(s_{\mathrm{ship}}\le0.01\) | 0.0292 (one copy); 0.0584 (both binaries) | **miss**, +0.0192 |
| P3 | TEST | at least 10 components, learned context-selected combiner | at least 31 component inputs, 23 context-selected first-layer mixers, one second-layer mixer, then SSE | **hit** |
| P4 | TEST | \(0.001\le r_1\le0.02\) | at least 0.0341 | **miss** above, at least +0.0141 |
| C1 | CONSISTENCY_CHECK | identity | holds | logged, information about 0 |
| E1 | TEST | \(\rho\le1.005\), \(u_B\le0.70\) | not run | **waits for a separate gate check** |

**Overall (rule at `PREREG.md` §4): open miss.** One TEST hit out of the two needed, and no J-implied design change has won its experiment. The map explains the trade between program bytes and archive bytes, but it gives no compressor, and it got the most important trade in the record (P2, P4) wrong.

## P1. Runtime memory split: not scorable

- OBSERVED: the PPMD byte model is built with memory 14000 (`src/predictor.cpp:302`, `byte_model_.emplace(25, 14000, ...)`), which `StartSubAllocator` turns into a heap of 14000 MiB (`src/models/ppmd.cpp:140-144`, `SASize << 20U`). That heap is memory-mapped to disk (`src/models/ppmd.cpp:29-33`, `bool mmap_to_disk = true;`). The writeup: "The PPMD model implemented in `src/models/ppmd.cpp` uses a lot of memory. To comply with the Hutter Prize's 10GB RAM limit, it stores its state on the disk using mmap." (`writeup.md:134`). LTCB reports decompression memory 9547 MB (AMD).
- Not scorable as locked. The quantity is the share of **runtime RAM**. How much of a disk-mapped 14000 MiB heap is resident is set by the operating system, and neither the writeup nor the source states a split. Summing the fxcm model's table allocations (`src/models/fxcmv1.cpp`, about 4,800 lines) was not finished inside the one-hour reading limit the prereg set.
- Not counted, and stated only as a lean: by allocation, the PPMD heap alone is larger than the whole RAM cap, so an allocation-based share would very likely be above 0.40. That is not the locked quantity.
- Lineage (reported): paq8hp "Most take a single option controlling memory usage" (LTCB `.1323`). That fits the R-ENG reading for paq8. cmix v4 "uses 28,976,428 KiB memory (29.7 GB)" (LTCB `.1082`), above the present cap. No split was read for either.

## P2. Online versus frozen: miss

- OBSERVED: the record "replace[s] the LSTM with a transformer with 6 million parameters", trained "on 8 RTX 5090 GPUs for 26 hours". "We append the weights to the compressor and decompressor binaries so our solution can run on a CPU. We quantize the weights so they only add 2.9MB each binary (or 5.9MB combined)." (`writeup.md:9`). LTCB: "pre-trained on enwik9 on 8 RTX 5090 GPUs for 26 hours, adding 2.9 MB to the compressor and decompressor."
- The shipped weight file at the pinned commit is `models/6m-q4-fp32.tfwc2`, 2,930,652 bytes. It is appended to the compressor as it is (`build_and_construct_comp.sh`: `cp $ROOT/models/6m-q4-fp32.tfwc2 ./comp_tfweights`, then `cat ./cmix_orig ./comp_dict ./comp_order ./comp_tfweights header.dat > ./cmix`). The self-extracting archive also carries it (`src/runner.cpp:1083`: "archive9 = decomp_binary(upxed) + comp_dict + tf_weights + cmix_output").
- \(s_{\mathrm{ship}}\) = 2,930,652 / 100,424,672 = **0.0292** for one copy, and **0.0584** for the two copies S counts. Bar 0.01. **Miss**, signed size +0.0192 (one copy, the conservative value).
- Rival R-SHIP predicted this outcome; J as mapped did not. The writeup states the trade in its own words: online training avoids paying for weights in size, but "time spent training counts towards the compressor's and decompressor's runtimes", so "training online reduces the size of the biggest model usable within the time limits and makes it impossible to heavily overtrain the model" (`writeup.md:17`). Its result: loss 0.911 nats per byte for the quantized transformer against the LSTM's 1.23 (`writeup.md:51`).
- Separately reported: a dictionary (`dictionary/english.dic`, 411,996 bytes raw, shipped compressed) and an article order fitted offline to enwik9 (`src/readalike_prepr/data/new_article_order`, 1,094,862 bytes raw, shipped compressed). Both came from fx2-cmix. The article order is a table fitted before decoding. Its compressed size was not read, so it is not added to \(s_{\mathrm{ship}}\); the miss holds without it.
- Lineage: fx2-cmix's LSTM "is trained online during compression and decompression" (`writeup.md:17`), so it shipped no trained weights. Its compressor was 441,468 bytes (LTCB `.1091`), and that bounds its shipped tables (article order and dictionary included) at 0.0040 of S. cmix "v12 ... includes a LSTM model" (LTCB `.1082`) and ships a dictionary, "compressed with cmix from 465211 to 90207 bytes" (v6). paq8: adaptive mixing learned online (LTCB `.1250`, paq8f). So the lineage met the bar until this record.

## P3. Mixing versus a single model: hit

- OBSERVED: the record keeps fx2-cmix and changes only the LSTM: "We do not do any modifications to fx2-cmix other than replacing the LSTM with a transformer, fixing three bugs, and minor changes" (`writeup.md:9`). The transformer's distribution goes to the byte mixer (`src/predictor.cpp:527-529`, "passes the transformer's output distribution (over the next byte) to the byte mixer").
- The first mixing layer takes, per bit: the bracket model, every fxcm output, 1 direct model, 15 indirect nonstationary models (1 bracket, 10 word, 4 double-indirect), 10 match models, 1 run model, the PPMD byte model and the byte mixer (`src/predictor.cpp:248-260`, `:263-277`, `:292-368`, `:426-485`). That is at least 31 inputs. They are combined by 23 first-layer mixers, each selected by its own context (`:394-416`), then one second-layer mixer (`:421`), then SSE (`:500-501`).
- **Hit.** The single-model rival (R-SHIP's practice) predicted one model coding directly. The record's new model is one input among many.
- Lineage: paq8f has "adaptive linear mixing of models with a neural network" (LTCB `.1250`). cmix v1 is "a context mixing compressor ... increasing the number of context models and mixer layers" (LTCB `.1082`). All three mix.

## P4. Model size versus archive: miss above

- OBSERVED (LTCB `.0969`, 24 Jul 2026 row): archive9 96,996,198; compressor ("C size") 3,428,474; total 100,424,672. "The compressor size is shown because it is used for scoring in the Hutter prize".
- \(r_1\ge\) 3,428,474 / 100,424,672 = **0.0341**. The decompressor inside archive9 (`src/runner.cpp:1083`) adds more, and its size is not listed separately, so 0.0341 is a lower bound. Bar \(\le0.02\). **Miss** above, signed size at least +0.0141.
- Lineage: cmix v21: decompressor 281,387, total 108,244,767, \(r_1=0.0026\) (LTCB `.1082` table). fx2-cmix: compressor 441,468, total 110,793,128, \(r_1\ge0.0040\) (LTCB `.1091`). Both were inside the band. The band held for the lineage and failed at the record, for the reason in P2.

## C1. Consistency check (information about 0)

fx2-cmix to fx2-cmix-T: the compressor grew by 2,987,006 bytes (441,468 to 3,428,474), and archive9 fell by 13,355,467 bytes (110,351,665 to 96,996,198). It holds, as it must when S falls.

## Unscored observations

- **The time cap is not binding in decompression at the record.** LTCB lists D time 131,561 s (36.5 h) and C time 133,766 s (37.2 h) on the AMD machine. The prize page's "~50h" is a rounded column. RAM (9547 MB) is near the 10 GB cap. J with run-time memory priced at 0 below the cap expects both caps to bind. This was not locked, so it is not scored.
- **The contest prices no offline compute.** The rules cap the programs' run time, RAM, disk and GPU use (`PREREG.md` §1). The 26 hours on 8 GPUs that trained the weights is outside every cap. This is the term the S-to-J map left out (see `MEMO.md`).

## E1. The inaction band: not run; its "not used" premise is half false

- OBSERVED, prior art inside the record: fxcm's inner mixer zeroes small errors before training: `if(err>=-elim && err<=elim) err=0;` (`src/models/fxcmv1.cpp:554`). The band width adapts once per byte: "When last byte was predicted good/below error treshold then set new limits to mixer update // larger value means less updates and better speed." (`:4697-4702`). So an inaction band on updates is already used in the record's inner mixers. As written there, the training loop still runs with err = 0 (`:555`), so the band filters small errors and does not save the time of the loop.
- Not used: the outer cmix mixers update on every bit (`src/mixer/mixer.cpp:74`, `float update = learning_rate_ * (Sigmoid::Logistic(p_) - bit);`). Skipping work on in-band bits, so that time is saved and can be spent elsewhere, is not used anywhere read.
- Prior art outside compression: selective backpropagation skips the backward pass on low-loss examples to save training time (Jiang, Wong, Zhou, Andersen, Dean et al. 2019, "Accelerating Deep Learning by Focusing on the Biggest Losers", arXiv:1910.00762, checked on the arXiv API, 25 November 2026; no DOI).
- E1 is a run. It waits for a separate gate check of `PREREG.md` §3 E1, as locked. It is not run here.

## DATA-ONE

Not a candidate, as fixed before scoring (`PREREG.md` §4). The cost-to-fitness map is S itself by contest rule. The one hit (P3) does not exclude R-MDL or R-ENG, and the two discriminating items (P2, P4) went to the rival R-SHIP.

## Citations checked

- Rissanen 1978, doi `10.1016/0005-1098(78)90005-5`, and Sims 2003, doi `10.1016/S0304-3932(03)00029-1`: Crossref API, `crossref.out`.
- Delétang et al., "Language Modeling Is Compression", arXiv:2309.10668 (arXiv API, 25 November 2026), cited in `MEMO.md` as background for R-SHIP; no DOI used.
- Jiang et al. 2019, arXiv:1910.00762 (arXiv API, 25 November 2026).

---

## Corrections after independent gate read (Wednesday 25 November 2026, ~12:30 ET, append-only)

All lines above are preserved as committed at `66640ab`. The independent gate read (`<local>/gtao-notes/gate_read_290.md`, checking `process/PREREG_GATE.md` at `8c4b3c0`) found 4 blocking items and gave `E1` a **GATE STOP**. The corrections below are appended without editing `PREREG.md` or earlier lines.

### 1. Withdrawal of E1 and correction of the prior-art reading (blocking items 1–3)

- **Correction to lines 63–64 above (OBSERVED in `83f2603`):**
  - The `train()` at `src/models/fxcmv1.cpp:536-544` cited at line 63 is inside a comment block (`:520-545`). The live `train()` at `src/models/fxcmv1.cpp:504-517` opens with `if (e) {` (`:506`). When `err == 0` inside `[-elim, elim]` (`:554`), the weight-update loop is skipped completely, which matches the comment at `:4698-4699` ("less updates and better speed").
  - `src/mixer/mixer.cpp:74-77` immediately after line 74 reads `if(fabs(update)<0.000000000005f && extra_inputs_size_>0) { return; }`, an early-return skip on tiny updates (active on `mixer_0_[1..22]`, where `extra_inputs_size_ > 0`, though with a near-zero width `5e-12`).
- **Effect on E1 and section 5:** The record **already uses** J's time-saving inaction band in its inner `fxcm` mixers (with adaptive width `elim`). The premise that the band was unused is false, and the gate read stopped E1 (G3 rival contradicted by prior art; missing stop rule and underspecified implementation in `PREREG.md:102`; slack decoding time of 36.5 h vs ~49–53 h cap). **E1 is withdrawn as a new-design experiment.** It was never run, and it was not a locked prediction of the record.
- **New J-implied design choice not used by the record:** **none found.** Per the work order, when none is found, say so and stop.
- **No post hoc hit:** The record's use of an adaptive inaction band (`fxcmv1.cpp:506, 554, 4697-4702`) is **not** counted as a hit for J because it was not preregistered; it is recorded only as an observed match, labeled **post hoc**.

### 2. Re-score of P1 under the lock's allocation-constant fallback (blocking item 4)

- **Correction to lines 26–27 above:** `PREREG.md:43` explicitly names "summed from allocation constants in its source" as the fallback when documentation does not state the RAM split, and only about 4 minutes elapsed between opening the sources (~11:31 ET) and commit `66640ab` (11:35:11 ET), so the one-hour reading limit had not run out. P1 is therefore **scorable** under the locked fallback.
- **Allocation sum (OBSERVED in `83f2603`):**
  - **PPMD** (`src/predictor.cpp:302`, `src/models/ppmd.cpp:140-144`, `mmap_to_disk = true`): `StartSubAllocator(14000)` allocates `14000 << 20` = **14,000.0 MiB** (14,680,064,000 B, memory-mapped to disk).
  - **fxcm** (`src/models/fxcmv1.cpp`): **4,163.6 MiB** total, consisting of `cmC2[0..17]` (3,668.5 MiB: `Init(m1, ...)` sets `m = 2*m1` and allocates `m >> 7` elements of `E1<14,128>` = 128 B each, `:1370-1378`, `:3287-3330`), `mxA[0..11]` (308.0 MiB: `alloc1(wx, N*M+32)` with `N = 512` `short`s for `mxA[0..9]`, `:578, :3255-3266, :3275-3282`), `rcmA[0]` (16.0 MiB, `:692, :3273`), `cmC[0..5]` (4.7 MiB, `:939`), `cmC1[0..4,6,7]` (0.59 MiB of `E<3,32>`, `:1144`), and static/global arrays (`ind3` 64 MiB, `buffer` 16 MiB, `mhashtable` 24 MiB, `smatch.Table` 4 MiB, `apmA0..5` 57.8 MiB, `:3169, :3181, :4795, :1670, :3218-3222`).
  - **ContextManager** (`src/context-manager.cpp:58-65`): **666.9 MiB** (`hashes_ind1..5` 512.0 MiB, `shared_map_` 97.7 MiB, `history_` 57.2 MiB).
  - **SSE** (`src/mixer/sse.cpp:206-222`): **423.6 MiB** (`s6` 336.0 MiB, `s7` 83.7 MiB, `x1`/`x2` 4.0 MiB).
  - **Mixer** (`src/predictor.cpp:394-421`, `src/mixer/mixer.cpp:19`): at most **404.5 MiB** (23 layer-0 + 1 layer-1 mixers, each capped at 10,000 contexts × ~460 `float` inputs).
  - **Match** (`src/predictor.cpp:333, 356`): **61.0 MiB** (8 map tables of 2M `uint32_t` each plus two tiny tables).
  - **TransformerOpt, Bracket, Direct**: **~30.1 MiB** combined (6M-parameter quantized weight arenas in `cpp_infer/src/opt/`, 1024-token KV/KDA spool, and small bracket/direct tables).
  - **Total allocated:** **~19,750 MiB** (14,000 MiB PPMD + ~5,750 MiB non-PPMD).
- **Score (updated):**
  - Under the lock's allocation-constant fallback: PPMD's share is `14,000 / 19,750` = **0.709 ≥ 0.40** → **hit**.
  - **RAM-residency caveat:** LTCB `.0969` measures decompression RAM at 9,547 MB (`9,105 MiB` if decimal MB; `9,547 MiB` if MiB) because PPMD is `mmap_to_disk = true`. Assuming the non-mmapped tables sit in RAM, `fxcm` alone allocates `4,163.6 MiB` = **0.436** of 9,547 MiB (or **0.457** of 9,105 MiB), which is already ≥ 0.40; any unpaged non-PPMD pages simply leave more RAM for PPMD (all other non-PPMD, non-`fxcm` tables together allocate ≤ 1,586 MiB, so `max(fxcm, PPMD_resident) ≥ 0.413` of 9,105 MiB). Either by allocation constants (PPMD) or in RAM (`fxcm`/PPMD), \(f_{\max} \ge 0.40\) holds, subject to the assumption that `fxcm` is counted as one named model family and no hidden OS/process buffer dominates RAM.
- **Updated P1–P4 tally:** **two TEST hits (P1, P3)** and two TEST misses (P2, P4). Condition (i) of the overall rule (`PREREG.md:115`) is now met, while condition (ii) fails because E1 is withdrawn and no unused J-implied design choice was found. **The overall outcome remains `open miss`** ("explains the trade but gives no compressor").

### 3. Non-blocking clarifications from the gate read

- **P2 (line 34):** Stated explicitly: `S` counts the 2,930,652 B weights **twice** (once appended to the `cmix` compressor and once inside `archive9`, 5,861,304 B = 0.0584 of `S`). The scored `s_ship` for P2 (inside the decompressor) is the one-copy figure **0.0292** (+0.0192 over the 0.01 bar).
- **P4 (lines 48–49):** `PREREG.md:83` defines `S_1` as the decompressor, whereas the prize page and LTCB report `3,428,474` B (`0.0341` of `S`) as the **compressor**. Inside `archive9`, the decompressor carries at least the `2,930,652` B transformer weights (`r_1 ≥ 0.0292`). Thus "≥ 0.0341" applies under the all-program-bytes reading and "≥ 0.0292" applies strictly to the decompressor; the miss (> 0.02) holds under both readings.
- **P2 and P4 dependence:** Both misses stem from the same observation (the 2.93 MB shipped weights), though their miss odds were set separately before reading.
- **P3 (line 42–43):** P3 carries little information given the prior knowledge of the cmix family disclosed in `PREREG.md` §0; also note `fxcm` itself supplies 431 outputs (`fxcmv1.cpp:93`), so total inputs are 460 (≥ 31).
- **Decode time vs cap (line 58):** LTCB D-time `131,561 s` (36.5 h) on AMD sits comfortably below the ~49–53 h cap (`70'000/T`), leaving slack; under J, slack time gives update time a shadow price near 0, further weakening E1's "binding time cap" premise.
- **LTCB curl note:** `ltcb.html` was fetched with curl at 11:30 ET (sha256 `4d1224b7…`); some automated fetchers encounter a bot wall on `mattmahoney.net`, though the figures match the page text.

## Note on P1 (appended 27 November 2026, after the hostile review of PR #295; the lines above are unchanged)

- **P1 is reported as contested, not as a hit.** The first score above was **not scorable** (line 14). The later re-score to **hit** (lines 104–108) rests on readings chosen after the numbers were seen. The lock defines P1 as a share of the record's **runtime RAM** (`PREREG.md:43`). The lock does name allocation constants as the fallback method (`PREREG.md:43`); the contested choice is counting a disk-mapped table as runtime RAM.
  - The allocation-constant reading counts PPMD's 14,000 MiB, which is memory-mapped to disk (`mmap_to_disk = true`) and exceeds the measured decompression RAM of 9,547 MB. So the 0.709 share is a share of allocated address space, not of RAM.
  - The RAM reading (fxcm about 0.44 of RAM) needs fxcm, a bundle of 18 context-map banks, 12 mixers and APM/SSE tables, to count as "one named model or table family", and needs the non-mapped tables to be resident. Neither was fixed before scoring.
- **Tally as read now:** P1 contested (post-hoc reading); P3 hit; P2, P4 miss. With P1 contested, condition (i) of the overall rule (`PREREG.md:115`) is not met on uncontested hits; condition (ii) fails either way. **Overall: open miss**, unchanged.
- No locked line, number or script is changed. Source of the review: the hostile review of #295 at main `ecf5bdbb4aae33bb5511816dac901dac2596e6c7` (27 Nov 2026).
