# Preregistration: the Hutter Prize budget as a test of the cost of judgment

*Wednesday 25 November 2026 (America/New_York). Branch `forge-hutter-test`, cut from upstream `main` `1eed183`. Locked before any primary source on the designs of paq8, cmix or fx2-cmix-T was opened for this work. Only the prize rules page and the prize page's records table and task box were read (§1). This file and `PREREG.sha256` go in their own commit, with no other file. Results go append-only in `RESULTS.md`; any change of plan goes in `DEVIATIONS.md`. `THEORY.md`, `CORE.md` and the locked blobs are not edited. Internal work only: no prize entry, no email, no public claim.*

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

The sentence is copied byte for byte from `CORE.md:7`. Everything below is labeled **OBSERVED** (read on a named page before this lock) or **HYPOTHESIS** (a bet locked here). Nothing here is a field result.

## 0. Prior knowledge, disclosed

The author has general background knowledge, from before this work, that the PAQ and cmix families mix many context-model predictions and learn online during decoding. No design document, source file or paper of paq8, cmix or fx2-cmix-T was opened for this work before the lock. The internals of fx2-cmix-T (July 2026) are not known to the author; what the suffix "T" stands for is not known. The odds below are set with that prior knowledge, so items whose answer the author expects are given low miss odds and are said to carry little information (`process/PROCESS.md:28`).

## 1. OBSERVED: the prize facts (read 25 November 2026, about 11:25 ET)

Sources: `https://www.hutter1.net/prize/hrules.htm` (HTML sha256 `e55d9f96b227e61ec0996adaf36304185d74db8c17093b403bb325240b2dc163`) and `https://www.hutter1.net/prize/index.htm` (HTML sha256 `aed08e09d3a83ef50b09f01434567844e6cfd7d2aa9cf546b4e91c9429a69f56`), both fetched with curl, HTTP 200. Text inside HTML comments is not shown to readers and is not used.

- **Size.** Rules page: "Total size is measured as S := length(comp9.exe/zip)+length(archive9.exe)." Relaxation: "S := length(comp9a.exe/zip)+2×length(decomp9.exe/zip)+length(archive9.bhm)", and "If comp9a.exe=decomp9.exe, the 2× can be reduced to 1×". "If command-line options for execution or compilation are necessary, their length is added to S."
- **Current record.** Prize page table: Vladimir Ivanov, 24 Jul 2026, fx2-cmix-T, total size 100'424'672, "9.96 | ~10GB | ~50h", "7.46%". Task box: "S:=S1+S2 < L := 100'424'672 (previous record)". This matches Ace's figure (100,424,672 bytes, July 2026).
- **1% threshold.** Prize page table, top row: "<99'420'425", ">1%", ">5'000€". Rules page: "Award = Z×(L-S)/L", "Z = amount in prize fund (500'000€)", "Minimum award is 1% of Z." This matches Ace's figure (S < 99,420,425). Difference noted: by the award formula, 0.99 × 100,424,672 = 99,420,425.28, so S = 99,420,425 gives (L−S)/L = 1.0000028%, which meets the 1% minimum. The table's strict "<" is one byte tighter than the formula. The page is used as written; the one-byte gap is recorded, not resolved.
- **Caps.** Rules page: "Each program must run in less than 70'000/T hours on a machine using at most 10GB RAM and 100GB HDD for temporary files, where T is the machine's Geekbench5 score. No GPU usage." Test machines listed there: Intel Core i7-1165G7 "with T≈1427 (1 core) and T≈4667 (4 cores)" and AMD Ryzen 7 3.6GHz "with T=1310 (1 core) and T=8228 (8 cores)". At the 1-core scores, 70'000/T is 49.1 h and 53.4 h. Prize page task box: "Must run in ≲50 hours using a single CPU core and <10GB RAM and <100GB HDD on our test machine." The rules page's visible text does not itself say "single core"; the prize page does. Programs "must run without input from other sources (files, network, dictionaries, etc.)".
- **Header lines.** The rules page header still says "less than the current record of about 116MB"; the prize page header says "about 100MB". The records table is used.
- **Lineage, top line only.** The prize page table lists (date, name, total size): fx2-cmix-T 24 Jul 2026 100'424'672; cmix-obias 19 Jul 2026 108'521'870; cmix-lex 26 Jun 2026 109'671'639; fx2-cmix 3 Sep 2024 110'793'128; fx-cmix 2 Feb 2024 112'578'322; fast cmix 16 Jul 2023 114'156'155; starlit 31 May 2021 115'352'938; phda9v1.8 4 Jul 2019 116'673'681 (pre-prize). The recent rows list "~10GB" RAM and "~50h" time. So the RAM and time caps bind at the record (OBSERVED, not scored).

## 2. The map from S to J

The cost under test is \(J=\kappa I+q\,\kappa\,P_D+w\,L\) (the form of `theory/QUANTUM_RECORD_PRICE_2026-11-24.md:12` with \(\kappa_D=q\kappa\)), under the ruin cap \(P(\mathrm{ruin})\le\varepsilon\) kept outside the sum (`CORE.md:25-27`).

- **Zero residual.** The decoder must reproduce enwik9 exactly. The reconstruction loss is therefore 0, and the decision being priced is the next-symbol forecast. Its loss is the log loss, and with arithmetic coding the archive length is that log loss in bytes up to a constant of a few bytes: \(S_2 \approx \sum_t -\log_{256} p(x_t\mid x_{<t})\). So \(w\,L = S_2\) with \(w=1\) (one archive byte is worth one decompressor byte).
- **Held memory.** \(\kappa I\) is the information the decoder carries before it reads the archive: the decompressor and its constants, \(S_1\) bytes, with \(\kappa=1\). Memory built during decoding (tables, weights, up to 10 GB) is not priced in S. In J it has price \(\kappa_{\mathrm{run}}=0\) below the cap.
- **Disturbance term.** The record is classical and the read does not disturb what is read, so \(P_D=0\) and \(q\) has no effect here.
- **Budget.** The caps (about 50 h on one core, 10 GB RAM, 100 GB disk, no GPU, no outside input) are the ruin set: a program over any cap is not a record. They sit outside the sum, as in `CORE.md:27`.

So, at zero residual, \(J = S_1 + S_2 = S\) subject to the caps. **This map is an identity on the total**: J and the two-part minimum-description-length code length (Rissanen 1978) are the same number here. Any prediction about the total alone is a `CONSISTENCY_CHECK`. The predictions below are about design structure, where J's in-model results (prices of zero below a cap; the layer, timescale and inaction-band results cited in `CORE.md`) say more than "minimize S", and where a plain-engineering rival says something different.

**Also not a test of the hypothesis itself.** S is both J and the prize's selection criterion. A record minimizes S by construction of the contest. That a record sits near a minimum of S says nothing about the hypothesis sentence (G2).

## 3. Gate (draft PR #263, `process/PREREG_GATE.md` at `8c4b3c0`)

Labels are given up front. **Rivals.** (R-MDL) two-part minimum-description-length coding, Rissanen 1978, which here predicts the same value as J for every item and is named to say so. (R-ENG) the plain-engineering reading: components and table sizes set by habit and trial on the benchmark, every component updated every step, no reason for any split. (R-SHIP) the pretrain-and-ship practice of current language models: train a model offline and ship its weights. (R-RI) rational inattention, Sims 2003, where an item overlaps: an agent with a cost per bit of processed information chooses a noisy signal; it fixes no learning dynamics and no number of components.

### P1 (TEST). How runtime memory is split across predictors

**Quantity.** \(f_{\max}\): the share of the record's runtime RAM held by its single largest component (one named model or table family), read from the record's own documentation or, if not stated there, summed from allocation constants in its source.

**HYPOTHESIS.** With \(\kappa_{\mathrm{run}}=0\) below a binding 10 GB cap, J's minimum sets equal marginal log-loss gain per byte across components in use. Gains per byte differ widely across context orders, so the split is uneven: \(f_{\max}\ge 0.40\) in fx2-cmix-T.

- **G1 miss:** \(f_{\max}<0.40\). Odds of a miss: 0.45.
- **G2:** depends on the record's measured allocation; not fixed by S or by any formula on `main`.
- **G3:** R-ENG predicts near-equal tables per model under one global memory option, so \(f_{\max}\) near \(1/n\) for \(n\) components, below 0.40 when \(n\ge3\). R-RI predicts the same uneven shape as J (water-filling on value), so it does not discriminate here; said so. R-MDL is silent on runtime memory.
- **G4:** level (c), a real record.
- **G5:** hit: the equal-margin reading is kept for P1 only and the next step is to check whether the record's sizes were tuned by search (a selection run). Miss: J's uneven-split reading is logged as an open miss with location `model`; the next step is to measure per-component gain per byte on a small slice.
- **Lineage.** Report \(f_{\max}\) for paq8 and cmix too, where readable. Not scored.
- **Not scorable** if neither documentation nor source gives the split within about one hour of reading. That is reported as not scorable, not as a hit.

### P2 (TEST, low information). Online versus frozen

**Quantity.** \(s_{\mathrm{ship}}\): bytes of trained model parameters (weights or tables fitted to data before decoding, from enwik9 or elsewhere) shipped inside the decompressor, as a share of S. Hand-set or tuned scalar constants (rates, sizes, a few thousand numbers at most) are not counted. A word list or dictionary used to transform text is counted separately as \(s_{\mathrm{dict}}\) and reported.

**HYPOTHESIS.** Shipped bytes cost 1 each; memory learned while decoding costs 0 bytes and only time under the cap. So the record learns online and ships almost nothing trained: \(s_{\mathrm{ship}}\le 0.01\) for fx2-cmix-T.

- **G1 miss:** \(s_{\mathrm{ship}}>0.01\). Odds of a miss: 0.12 (prior knowledge, §0).
- **G2:** depends on the record's contents.
- **G3:** R-SHIP predicts a shipped pretrained model with \(s_{\mathrm{ship}}>0.01\) (about 1 MB or more). R-MDL: the two-part code allows either; prequential MDL is online; it does not choose. R-RI: silent.
- **G4:** level (c).
- **G5:** hit: low information, logged as such. Miss: the 1:1 price did not keep trained weights out; open miss, location `model`, and the next step is to price the time the shipped weights save.
- **Lineage.** \(s_{\mathrm{ship}}\) for paq8 and cmix, scored the same way, reported.

### P3 (TEST). Mixing versus a single model

**Quantity.** Whether the final probability for each coded bit or symbol is a learned, context-selected combination of at least 10 separate component predictions (mixing), or comes from one model whose output is coded directly (single).

**HYPOTHESIS.** J's layer results price each extra predictor only in time (no S cost beyond its code), and the enwik9 stream carries structure on many timescales, so the minimum under the cap keeps many predictors and a learned combination: fx2-cmix-T mixes at least 10 components with a learned, context-selected combiner.

- **G1 miss:** the record codes from a single model (for example one neural network predicting directly), or combines fewer than 10 components. Odds of a miss: 0.25 (raised from prior knowledge because the internals of fx2-cmix-T, and the "T", are not known).
- **G2:** depends on the record.
- **G3:** R-SHIP and the single-large-network practice predict one model. R-ENG is neutral. R-MDL and R-RI: silent.
- **G4:** level (c).
- **G5:** hit: the next step asks whether the number of mixed components tracks the timescale spread (a T-layer count), which needs a measured spectrum. Miss: open miss, location `model`; the next step is to ask what J term a single model saves.
- **Lineage.** Mixing yes or no and component count for paq8 and cmix, reported.

### P4 (TEST). Model size versus archive

**Quantity.** \(r_1=S_1/S\) for fx2-cmix-T, where \(S_1\) is the decompressor size as counted in S (zipped source or executable, with any 2× relaxation applied as the record used it).

**HYPOTHESIS.** At J's minimum the decoder ships code plus whatever fixed data pays for itself 1:1 and builds the rest at run time, so \(S_1\) is small but not bare: \(0.001\le r_1\le 0.02\) (about 100 KB to 2 MB).

- **G1 miss:** \(r_1<0.001\) or \(r_1>0.02\). Odds of a miss: 0.25.
- **G2:** depends on the record.
- **G3:** R-SHIP predicts \(r_1>0.02\). R-ENG with a code-only decoder predicts \(r_1<0.001\). R-MDL predicts the same as J and is not a discriminator.
- **G4:** level (c).
- **G5:** hit: the next step reads which fixed data the decoder carries and whether each piece pays 1:1. Miss below: shipped data never pays here; miss above: J's run-time-memory reading is wrong for this record; both are open misses, location `model`.
- **Lineage.** \(r_1\) for the cmix-family records where the size split is published, reported.

### C1 (CONSISTENCY_CHECK). Each record step buys back its decompressor growth

Between consecutive records, if \(S_1\) grows then \(S_2\) falls by more. This follows from S falling at each record. It is logged only, with information about 0.

### E1 (TEST, a design choice and its smallest experiment). An inaction band on updates

**Design choice.** Under a binding time cap, each update has a lumpy time cost. J's inaction-band result (CL19, `measurement/CLAIM_MAP_v2.md:580`; the band rule at `CORE.md:100`; `process/PROCESS.md:24`) says: skip an update when its expected gain is below that cost. In a compressor: skip the model and mixer updates for a bit whose mixed prediction already put at least 0.95 on the outcome, and spend the saved time on more or larger components. Whether the lineage already does this is scored after the lock (`RESULTS.md`), with prior art.

**Smallest local experiment (preregistered; runs only after a separate gate check of this section).** Data: the first \(10^6\) bytes of enwik8 (from `http://mattmahoney.net/dc/enwik8.zip`; the slice's sha256 is recorded at run time). Predictor: bitwise; five hashed context models of orders 0 to 4 over whole previous bytes plus the partial current byte, each a table of \(2^{22}\) 16-bit probabilities updated by \(p\leftarrow p+(y-p)/16\); a logistic mixer over the stretched inputs plus a bias, 256 weight sets selected by the partial current byte, learning rate 0.002, weights starting at 0.3. Cost: ideal code length \(\sum -\log_2 p\) in bits. Arm A updates everything every bit. Arm B skips all updates (models and mixer) on a bit when \(|y-p_{\mathrm{mix}}|<0.05\). Measured: update fraction \(u_B\) and ratio \(\rho=L_B/L_A\). Single run each, deterministic, C, under a minute.

- **HYPOTHESIS.** \(\rho\le 1.005\) and \(u_B\le 0.70\).
- **G1 miss:** \(\rho>1.005\) or \(u_B>0.70\). Odds of a miss: 0.55.
- **G2:** the value depends on the data's statistics and a run with no closed form.
- **G3:** R-ENG and R-RI both predict that every step should update, with step size scaled by the error (R-RI's cost per bit gives a smooth, partial response, not a band), so skipping costs more than 0.5%: \(\rho>1.005\). Resolution: \(\rho\) is exact to 6 digits for a deterministic run.
- **G4:** level (a), a toy we build. Route to (c): a hit justifies a test inside an open cmix-family compressor at the time cap; that larger run is not done here.
- **G5:** hit: name the reinvestment test (same time, larger tables) as the next step. Miss: open miss for E1, location `model`; the band is not worth its loss at this threshold.

## 4. Scoring

Primary sources only, after this lock: the prize page's links for each record, the records' own repositories and documentation, Mahoney's own paq8 pages and source, and published papers. Every citation is checked; DOIs are checked on Crossref. No number is filled from memory; an unreadable number is "not scorable". Each TEST is scored hit or miss on fx2-cmix-T, with a signed size where it has one. Lineage values are reported, not scored. P1–P4 are read from published sources, not run; the work order directs scoring them after this lock. No separate gate check of §3 is available on this branch before that scoring, and this is disclosed in `DEVIATIONS.md` when scoring starts. E1 is a run and waits for a separate gate check.

**Overall outcome rule.** The overall result is a pass only if (i) at least two of P1–P4 hit, and (ii) a J-implied design choice not used by the record has prior-art status checked and its smallest experiment hits. If the map explains the trade but yields no compressor change that wins in the experiment, the overall result is an **open miss** ("explains the trade but gives no compressor"), logged in `OPEN_WORK.md`.

**DATA-ONE call, fixed now.** DATA-ONE (`OPEN_WORK.md:251`) needs a band that excludes a named rival and a cost-to-fitness map. Here the cost-to-fitness map is S itself, by contest rule, and R-MDL predicts the same as J on the total. This setting is therefore **not a DATA-ONE candidate** unless a scored TEST hits where R-MDL, R-ENG and R-SHIP all predict a different value. P1–P4 do not meet that condition (R-MDL is silent or the same). E1 could meet it only at level (a), which is not a real system. So the expected call is: not a candidate.

## 5. References

- Rissanen, J. 1978. Modeling by shortest data description. *Automatica* 14(5):465–471. doi `10.1016/0005-1098(78)90005-5` (checked on the Crossref API, 25 November 2026).
- Sims, C. A. 2003. Implications of rational inattention. *Journal of Monetary Economics* 50(3):665–690. doi `10.1016/S0304-3932(03)00029-1` (checked on the Crossref API, 25 November 2026).
- Hutter Prize rules and prize page, URLs and hashes in §1.
