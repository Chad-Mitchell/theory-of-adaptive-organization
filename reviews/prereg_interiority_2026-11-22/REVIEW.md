# Review of draft PR #171

Independent hostile review of the design-phase lock in `prereg/GMREAD_2026-11-22/` (branch `prereg-interiority-2026-11-22`, head `69af0039ebde647d00d2d5683babb4dc41f70733`, commit time 2026-11-22 09:41:19 +0000). This pass wrote none of `PREREG.md`, `gmread.py`, `run_sim.py`, or `LOCK.txt`. No DANDI asset byte was transferred. Stimulus and spike series were not opened. The calculations below use the locked decision code, synthetic series, and public metadata.

**Verdict: NOT-INFORMATIVE.**

The locked comparison cannot fail on any causal decoder of a series the class gate accepts, and a label of supports would be the prediction of efficient coding, predictive coding, and the Kalman filter theorem. It would also be the prediction of a decoder that ignores the spikes. The official real-data label is already fixed as not a test. Beliefs about the hypothesis do not move.

The Gauss–Markov arithmetic is transcribed correctly. The worked point passes `check_worked_point`. The failure is the identification of the task and of the rate.

## 1. Task identification

The floor \(r \ge \tfrac12 \ln(a^2 + Q/P)\) is the sequential rate–distortion function of a scalar Gauss–Markov source under squared error, attained by the Kalman filter (SHANNON §3; Tatikonda, Sahai and Mitter 2004; Tanaka, Kim, Parrilo and Mitter 2017). It is a lower bound on the directed information rate required to hold posterior variance \(P\) on that source, at the lead the bound was proved for.

The lock names a different object.

- The target is the demeaned mean luminance of a frame, lead \(k = 0\). The dandiset's own description (metadata only) asks how representations of oriented bars and of movies of eagles and squirrels change from the LGN through visual cortex to the hippocampus. Frame-mean luminance is an analyst reduction of that stimulus. Nothing in the metadata says a mouse visual population is tracking that scalar, at that lead, as its judgment.
- Lead 0 is the filtered state. At lead 0 the distortion identity is \(D = P\). The worked GF5 point uses lead \(k = 2\), and the lock correctly treats that point as a formula check. The scored arm drops the lateness the theory treats as part of the loss.
- \(P\) is the second-half mean squared error of a linear decoder the protocol chooses: spike counts in the current bin and the previous \(L = 5\) bins, bin width equal to the frame period, fit on the first half. The floor is then evaluated at that \(P\). The floor is a property of the decoder the protocol built.

The population identity makes this circular. Let the world be stationary AR(1), \(X_t = a X_{t-1} + \varepsilon_t\), with \(\varepsilon_t\) independent of the past and of variance \(Q\). For any causal point estimate \(\hat x_{t-1}\),

\[
X_t - a\hat x_{t-1} = a(X_{t-1} - \hat x_{t-1}) + \varepsilon_t,
\]

so the prediction mean squared error is \(a^2 P + Q\). The plug-in in section 5,

\[
r = \tfrac12 \ln(P_{\mathrm{pred}}/P),
\]

equals the floor \(\tfrac12 \ln(a^2 + Q/P)\) for every causal decoder. A decoder that outputs 0 has \(P = V\) and \(r = 0\), and the floor at \(P = V\) is also 0, because \(a^2 + Q/V = 1\). A unit that does not track luminance is labeled on the floor.

Finite-sample check, not a deposit series: length 4000, \(a = 0.8\), \(Q = 1\), observation noise variance 0.5, \((a, Q)\) from conditional least squares on the first half, scores on the second half, predictor \(a\hat x_{t-1}\), 20 replicates.

| Decoder | Mean excess (nats) | Range | Mean \(P\) | Mean \(r\) |
|---|---:|---:|---:|---:|
| Output 0 | −0.007 | −0.022 to −0.000 | 2.812 | 0.000 |
| Kalman | −0.001 | −0.039 to +0.035 | 0.357 | 0.618 |
| Memoryless posterior mean | −0.000 | −0.037 to +0.032 | 0.424 | 0.550 |
| Shrunk gain \(0.15\,y_t\) | −0.001 | −0.024 to +0.040 | 2.043 | 0.063 |
| Lagged observation only | −0.002 | −0.027 to +0.025 | 1.383 | 0.155 |
| Kalman estimate plus independent noise | −0.001 | −0.020 to +0.023 | 2.596 | 0.014 |

No replicate left the band \([-0.05, 0.15]\). Eight memoryless blocks scored with that written predictor are labeled **supports** (mean excess −0.0023, half-width 0.014). The committed memoryless scenario is labeled **fails to support** (mean excess 0.333) because `run_filter` resets the filter state and scores the predictor 0. That is a different statistic from section 5.

Directed information from the movie into the spike train is a different quantity. The plug-in does not upper-bound it. A high-rate spike code whose linear luminance decode is poor still sits on the floor under section 5. The region **fails to support** is unreachable for the written predictor, up to sampling error of a few hundredths of a nat.

## 2. Estimator feasibility

The rate in section 5 is a Gaussian variance ratio of the decoder's own residuals. It is not a plug-in directed-information estimator, not a Kraskov–Stögbauer–Grassberger estimator, and not a point-process GLM directed-information estimator.

What those estimators actually deliver:

- The plug-in entropy estimator has a bias of order \((K-1)/(2N)\) nats (Miller–Madow; Paninski 2003, doi 10.1162/089976603321780272, Crossref 200). For a population spike word, \(K\) is exponential in the number of cells and the history, and the bias exceeds 0.15 nats at sample sizes a single movie block can supply. A one-cell binary word is a different, smaller problem, and it is not the population the deposit records.
- Kraskov, Stögbauer and Grassberger 2004 (doi 10.1103/PhysRevE.69.066138, Crossref 200) estimate mutual information. The bias grows with dimension. The estimator is not directed information from a movie to a spike train.
- Quinn, Coleman, Kiyavash and Hatsopoulos (doi 10.1007/s10827-010-0247-2, Crossref year 2010) give a GLM / minimum-description-length estimator that is consistent when the processes are stationary and ergodic, Markov, and the GLM is the right model. Schamberg and Coleman (arXiv:1902.00580) show that the conditional-Markov assumption those finite-order estimators use fails except on a set of parameters of Lebesgue measure zero, and they bound the bias by the gap between partial and truncated directed information. Neither paper supplies a half-width below 0.15 nats for a natural movie driving a cortical population.
- Strong, Koberle, de Ruyter van Steveninck and Bialek 1998 (doi 10.1103/PhysRevLett.80.197, Crossref 200) is the direct method. Its plug-in bias grows with word length, which is why the paper extrapolates. It needs repeated presentations of one stimulus. The metadata does not state a repeat count.

The deposit, from the version record and the asset list, with no asset body read: DANDI:000690 version 0.260330.2144, 156 files, 600242801107 bytes, 25 subjects, all files `.nwb` (106 probe `ecephys` files, 50 session files). `variableMeasured` is ElectricalSeries, LFP, ProcessingModule, Units. The approach is extracellular electrophysiology. Calcium imaging is not in the summary. The description's only timed stimuli are bars crossing the screen in 2 seconds or 6 seconds. Natural-movie duration, frame rate, and frame count are not in the metadata. A first half of length 2000 is not shown to exist. `variableMeasured` does not name a stimulus frame array, so the schema rule in section 4 may itself return not a test. That is the right refusal, and it is not a measurement of the floor.

On the oracle the locked code does run, the half-width is about 0.010 nat (`sim_outcomes.json`, on-floor, \(n = 8\), \(T = 2000\)). That is the standard error of the variance ratio, which the identity pins to the floor. It is not a standard error for spike directed information.

The not-a-test bin does swallow every real outcome of this lock: rule 1 fires before any file is opened. After a qualification addendum, the written plug-in would not be swallowed. With a half-width near 0.01 and a mean near 0 it would be labeled supports, including for the decoder that outputs 0. A genuine directed-information estimator is the other uninformative landing. Support at a mean of 0 requires half-width \(\le 0.05\), because the lower edge of the band is −0.05. The fail rule requires the whole interval to lie above 0.15. Half-widths from 0.05 to 0.15 are unresolved, and half-widths at least 0.15 are a resolution failure. Calling `decide` on a mean of 0:

| Half-width | Label |
|---:|---|
| 0.04 | supports |
| 0.06 | not a test (unresolved) |
| 0.12 | not a test (unresolved) |
| 0.15 | not a test (resolution) |

The power study never enters that region. Its oracle half-width is 0.010.

## 3. The world-class gate

A natural-movie block is not, as a class, scalar Gauss–Markov. The repository already dropped the photoreceptor candidate because published natural intensity series are near \(1/f\) and the one-pole floor is the wrong class (the lock's own section 0, item C). Frame-mean luminance can be smoother than a pixel trace, and it can also be nonstationary at scene cuts. The metadata does not say which.

The gate checks a length, a pole in \([0.30, 0.98]\), \(Q > 0\), agreement of two slope estimators within 0.05, a residual lag-2 correlation at most 0.10 in absolute value, and an absolute excess kurtosis at most 1. It does not check the spectrum, residual lags beyond 2, stationarity, or whether any unit uses the scalar as its task.

Spectral surrogates, magnitude \(|f|^{-\alpha/2}\), random phase, real inverse FFT, length 2000, 30 draws, scored with `class_gate` on the full series:

| \(\alpha\) | Passes | Median \(\|a\|\) | Median residual lag-2 |
|---:|---:|---:|---:|
| 0.5 | 30/30 | 0.360 | 0.067 |
| 1.0 | 30/30 | 0.780 | 0.028 |
| 1.5 | 0/30 | 0.971 | 0.114 |
| 2.0 | 0/30 | 0.998 | pole above 0.98 |

The spectra for which VIS-1F was dropped pass the gate that is supposed to enforce scalar Gauss–Markov. On length-4000 surrogates with \(\alpha = 1\), the first half meets \(T_{\min} = 2000\), the gate passes 25/25, and the written plug-in stays near zero: mean excess −0.011 for a zero decoder, +0.015 for a fixed gain, −0.026 for a Kalman filter built from the fitted \((a, Q)\). A misspecified world is labeled like a success.

The bundled AR(2) does fail this gate (residual lag-2, 0/40 draws, and all eight blocks of the demonstration seed). The scenario then overwrites that result and forces the class flag false anyway.

## 4. Specificity

A label of supports is the prediction of several theories that do not use this hypothesis.

| Theory | What it predicts on this task |
|---|---|
| Efficient coding (Barlow; Laughlin; the energy–information tradeoff in Niven, Anderson and Laughlin 2007, the paper section 0 cites) | A sensory code under a rate or metabolic constraint sits on a rate–distortion bound. For squared error and a Gauss–Markov source, that bound is this floor. |
| Predictive coding (Rao and Ballard 1999, doi 10.1038/4580, Crossref 200) | The linear-Gaussian case is the Kalman filter, which attains the floor. |
| Sequential rate–distortion and rational inattention (Tatikonda, Sahai and Mitter 2004; Tanaka et al. 2017; Sims 2003, already credited in SHANNON) | The minimum directed information for posterior variance \(P\) is this floor. SHANNON §3 marks the Kalman attainment KNOWN. |
| Any causal point estimate, selected or not | The written plug-in sits on the floor, including a readout of zeros. |

Section 0 scores candidate C (dipteran photoreceptors) at 1 on GTAO-specificity because a pass would not separate the hypothesis from efficient coding, and scores candidate G at 5. The scored claim of G is the same floor. Section 9 says efficient coding is distinguished because a whitened kernel can still use more rate than the floor at its \(P\). That distinction needs the channel rate. The locked rate cannot show it.

What is particular to this hypothesis is not in the label. The joint memory-and-read corner is left out because the published efficiency is 0.9574 and joint achievability is open (SHANNON §3; GF5). That exclusion matches GF5. The layer price has no formula (SHANNON §7). The selection distance \(d/(2\sigma N_e)\) needs a qualified class. A stake move along one computed front (the comparison GENERAL_FORM §7 says additive expected-currency \(J\) does not share) is not this deposit. GF5's row on the claim map is still OPEN and "not a prereg." This lock does not close it.

The seven public candidates in section 0 do not contain a repair. A and the frontier re-read are antitone clouds, which GF5 says are not the prediction. B is an unscored drift sign, not an information floor. C is the efficient-coding comparison the lock correctly refuses, on a \(1/f\) world. D is prior art (Kussell and Leibler) and is not this floor. E already failed the vigilance gates. F is Chow's storage hierarchy. G is this protocol.

## 5. Qualification, and what the lock is worth

Rule 1 fires. `official_real_label()` returns not a test, reason `qualification_not_established`, `real_files_opened` false. The rerun matches the committed JSON. Under this commit the deposit cannot support the hypothesis and cannot miss it.

The hashes are a real commitment to that refusal. Opening an asset under this lock is a deviation, as section 3 says. That negative commitment is intact. It is not a commitment to an informative test. An addendum that only supplies (a), (b), and (e) and then evaluates section 5 still cannot fail, for the reason in §1.

Qualification is all five items in THEORY §3 and FRAMEWORK §9 item 1, from sources that are not the deposit, recorded before any asset byte.

- (a) \(\sigma\), the fractional change in growth, survival, or reproduction per fractional change in \(J\). No public source states that elasticity for this \(J\). Frame-mean luminance error is not a published fitness currency for *Mus musculus*.
- (b) \(N_e\), independent lineages in the same world per redesign time. The named source is Sung, Ackerman, Dillon, Platt, Fuqua, Cooper and Lynch 2016, Table 1. Europe PMC lists the paper as CC-BY, PMC4978911, open access, so an account is not the barrier. The full-text XML request in this pass returned HTTP 500, the same class of failure the lock reports, and the PMC HTML is a bot wall, so this pass did not re-isolate the cell. A prior reading in `reviews/discrim_2026-11-21/REVIEW.md` reports that the table prints *Mus musculus* at \(1.77 \times 10^6\) and says a large species \(N_e\) is not qualification. This lock correctly refuses to import that reading. A species-wide \(N_e\) is a different number from the count of independent visual-coding designs. The lock itself says the 25 mice are technical replicates of one design.
- (c) stops while (a) or (b) is missing. The factor 10 is the repository's choice. Lynch et al. 2016 is the drift-barrier citation. That part of the text matches THEORY §3.
- (d) the band plus measurement error must exclude a named rival from FRAMEWORK §9 item 6 (a fixed budget share, an exponent \(1/2\), or the world's time scales with no price). Section 3 says (d) is not evaluated. Section 9 says the exponent-\(1/2\) rival is not computed. The \(+0.40\) nat shift is the GF5 arithmetic illustration. It is not that rival.
- (e) \(T_{\mathrm{red}}\) and at least \(10\,T_{\mathrm{red}}\) of the same world. No source is locked. A laboratory movie is not shown to be the world the lineage was selected in. Section 10 says so. Evolutionary redesign time is not a closing time measured for this \(J\), and a contrast-adaptation time constant is not redesign of the design.

All five are required. They are not established, and they are not available from public sources without an account in the form the definition demands. Sung's species cell, even if re-read later from the open XML, would not finish (a), (d), or (e), and would not be item (b).

The small-class allowance (\(c = 0.999\), \(n_{\min} = 1\), \(\alpha = 0.01\)) would treat one miss of this single design as a miss of the class. That allowance is attached to a statistic that cannot miss.

## 6. Thresholds and the power study

The band \([-0.05, 0.15]\) and the half-width cutoff 0.15 are not derived from \(\varepsilon\), from a bias calculation, or from a named rival's predicted gap. \(\varepsilon\) is not computed. The bias bound 0.05 is a threshold in the rule. The code never estimates a bias. The \(+0.40\) nat alternative is the shift in the GF5 worked cloud, an illustration that an antitone cloud can sit inside a relaxation. It is not an effect size measured before seeing this deposit.

The acceptance window has width 0.20. A confidence interval fits inside it only if the half-width is at most 0.10, and a mean of 0 is inside it only if the half-width is at most 0.05. The resolution rule uses 0.15. The binding constraint for an on-floor estimate is the bias bound, and the text does not say that.

`power_study` draws the oracle Kalman plug-in and the same plug-in plus 0.40 nats, 200 times, at \(T = 2000\) and \(n = 8\). The committed result, reproduced byte-for-byte, is supports in 200/200 on-floor draws and fails to support in 200/200 shifted draws. `gate_met` is true. The standard error of that oracle mean is about 0.005 nat, so 0.40 nats is tens of standard errors. The study shows that a hand-added constant larger than the threshold is detected. It does not show power against a suboptimal code, against a \(1/f\) world the gate accepts, or against a directed-information estimator. The written memoryless alternative, which section 9 says sits above the floor, is labeled supports when the predictor is the one section 5 defines.

FRAMEWORK MV10 asks for the standard deviation of the planned contrast on the planned data. The planned data are spikes or, in the question posed to this review, calcium. The simulation uses Gaussian state noise and the latent state. MV7's known group is that same oracle. The lock calls the tier Tier 3 and says MV7 is not met for a field claim. That self-label is accurate. It does not make the later field comparison informative. MV1 fails because the named target is not the decision-relevant quantity in the dandiset description. MV2 fails because the observable is the variance ratio of an analyst's decoder, and the model quantity is directed information into the memory.

The interval uses \(z = 1.96\) and the population standard deviation, as the text says. With \(n = 8\) that interval is tighter than a \(t\) interval on the sample standard deviation. Next to the identity, the difference does not change a label.

## 7. Code against the preregistration

`decide` implements the eight-row table in section 7, in that order, with one extra stop: any non-finite excess returns not a test with reason `non_finite_excess` instead of being dropped from the finite set the table counts. `statistics.pstdev` matches the text's population standard deviation.

The simulation does not implement the real-data procedure the prose locks.

- There is no luminance reducer, no spike or calcium decoder, and no reader of a deposit file. The hashed program cannot execute section 5. `run_filter` feeds the latent state to a Kalman filter that knows the true \(a\), \(Q\), and noise variance.
- Section 4 and section 5 say \((a, Q)\) and the class gate use the first half only, and that the first half has length at least \(T_{\min} = 2000\). The simulator draws length 2000 and fits and gates the full series. `class_gate` on the first half of a true AR(1) of length 2000 returns span, because that half has length 1000. A literal reading requires a block of at least 4000 frames. The power study's span is the other reading.
- Section 5 says a \(P\) outside \((0, V]\) is not finite and the block is dropped. `_one_block` clips \(P\) to \(0.999\,V\) and continues. A value \(P = 10\) with \(V = 2.778\) is clipped and still passed to `floor_excess`.
- `scenario` sets the class flag true only when every block passes. The text drops failing blocks, requires eight that remain, and treats the class gate as failed when every block is dropped or the schema fails. Mixed blocks cannot be scored as written.
- For `kind == "nongm"` the class flag is forced false after the gate runs. On the bundled AR(2) the gate already fails, so the demonstration label coincides with the gate. The force does not consult the gate.
- The memoryless predictor in `run_filter` is 0. Section 5's predictor is a function of the decoder's previous output. Under that predictor the memoryless design is supports, which contradicts the sentence in section 9 and the committed scenario label.
- `rate_shift` adds nats to the plug-in at fixed empirical \(P\). No observation channel produces the shifted scenario. That is the alternative the power study rejects.
- The \(+0.40\) cloud in the committed shifted scenario is undominated and has isotonic mean squared residual 0, and the label is fails to support. That is the GF5 arithmetic, and it is purchased by adding the constant.

`python3 run_sim.py` writes JSON to stdout and does not open a socket. The rerun exited 0. `worked_point_ok` is true. The three labels appear. The official real label is not a test. The stdout JSON is equal to the committed `sim_outcomes.json`.

## 8. Hashes

`LOCK.txt` matches the files at `69af003`, byte for byte:

```
50b5230184c87f0dd10fefeb66ef4b0e15d70801b856f5656e3ad42795b4f09b  PREREG.md
a61990f5d674cd49123e0c275bc0db453adb69a1d89e9bbbc8e37e3e84c3e036  gmread.py
d63c10da3c7f2eb6a3448003d80d072c8056f2ecda3823adc9a0afc7ba41aa01  run_sim.py
```

`crossref.json` and `sim_outcomes.json` are outside the hash. The JSON file is an output, and the rerun reproduced it. The lock covers the three files it names.

## 9. DOIs

Each of the eleven bibliographic DOIs in section 12 returned HTTP 200 from `https://api.crossref.org/works/{doi}`. Title, year, and container match `crossref.json` in every case. Author lists match the names in the prose, including both Chow papers (C. K. Chow, 1974 and 1976) and Sung et al. 2016.

The dataset DOI `10.48324/dandi.000690/0.260330.2144` is in section 4. It is not in section 12 and not in `crossref.json`. Crossref returned HTTP 404. DataCite returned HTTP 200: title "Allen Institute Openscope - Vision2Hippocampus project", publication year 2026, type Dataset, license CC-BY-4.0, publisher DANDI Archive. The sentence "Each DOI in this file is resolved on the Crossref API" does not hold for that DOI. The bibliographic list is clean.

## 10. Wording

The hypothesis sentence occurs once in `PREREG.md` and is byte-identical to the sentence in `THEORY.md` §3, `CORE.md`, `theory/DERIVATION_CHAIN.md`, and `README.md`:

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

The locked folder contains no "bill", no "kill", and no "verdict".

## What would be informative

A new version that only repairs the mismatches in §7 (first-half split, the clip, the forced class flag, the memoryless predictor) would make the simulator agree with the identity. It would still be unable to fail, and a support would still be shared with efficient coding and predictive coding. Those repairs belong in a new preregistration if anyone wants the prose and the code to describe the same non-test. They do not make a test. The locked files should not be edited.

An informative design would need all of the following, fixed before any outcome series is read.

- A world the design does not choose, in a class a proved tight bound applies to. For this floor, that class is scalar Gauss–Markov. The gate has to reject the \(1/f\) surrogates above, not only an AR(2) with residual correlation −0.37.
- A task loss at a pre-registered lead, equal to an error the organism pays. Posterior variance \(P\) has to be that error. It cannot be the mean squared error of a decoder whose one-step predictor is \(a\hat x\), because that pair is the floor by algebra.
- A directed-information rate for the channel into the memory, with an estimator whose bias is bounded on synthetic series matched to the planned length and the planned response dimension, and with that bound smaller than the margin. The quantity has to be able to come in above the floor when the code spends excess rate. A lower bound that meets the floor cannot do that.
- A rival prediction that is not the Kalman equality. Efficient coding, predictive coding, and sequential rate–distortion all predict this floor. The comparisons in GENERAL_FORM §7 that those theories do not share are a stake move along one computed front, and the selection distance across two qualified classes. The joint \((I, r)\) corner is not available: SHANNON §3 leaves it open at efficiency 0.9574, and GF5 says excess over the relaxation is not a miss.
- Qualification under THEORY §3, all five items, for that class and that world.

None of the seven public options in this lock is that design. This dandiset is not, on the metadata: the target is not identified, the movie is not shown to be scalar Gauss–Markov, the timed stimuli are a few seconds, the class is one laboratory design, and (a), (d), and (e) are not in public sources. Pasting a species \(N_e\) into an addendum would not supply them.

## Command results

Head `69af0039ebde647d00d2d5683babb4dc41f70733`. Python 3.12.3. No deposit file opened. Lean was not built: `lake` is not installed, and `tools/test_lean.py::test_lean_build_if_available` skipped for that reason. The source scan in that file passed.

| Command | Result |
|---|---|
| `nice -n 19 python3 run_sim.py` in `prereg/GMREAD_2026-11-22` | Exit 0. stdout JSON identical to `sim_outcomes.json`. `worked_point_ok` true. Labels supports, fails_to_support, not_a_test. Official real label not_a_test, reason `qualification_not_established`, `real_files_opened` false. Power: supports given on-floor 1.0 (200/200), fails to support given the shifted plug-in 1.0 (200/200), `gate_met` true. |
| `sha256sum` of `PREREG.md`, `gmread.py`, `run_sim.py` | Equal to the three lines in `LOCK.txt`. |
| Crossref, paced, the eleven section-12 DOIs | HTTP 200. Stored title, year, and container match. |
| Crossref, dataset DOI | HTTP 404. |
| DataCite, dataset DOI | HTTP 200. Title, year 2026, CC-BY-4.0, as in §9. |
| DANDI version metadata and the asset-path list | HTTP 200. Counts, license, access, species, and `variableMeasured` match section 4. 156 paths, all `.nwb`. No frame rate and no movie duration in the description. |
| `git fetch origin main` | Fetched. |
| `nice -n 19 python3 tools/check_fresh.py` | RESULT: PASS. `STATUS.md` main is `5fa4b8c`; window `a30f89d 5839dbb 5fa4b8c f3a8fd0 2d9a812`. |
| `nice -n 19 python3 tools/check_consistency.py` | RESULT: PASS. 0 FAIL. 27 INFO on frozen records. Claim-map tally 378. Advisory length warnings: THEORY.md main text 11093 words, README.md 1476 words. |
| `nice -n 19 python3 tools/check_open_work.py` | RESULT: PASS. `items.json` not-DONE 62; `QUEUE.md` not-DONE 90; union missing from `OPEN_WORK.md` 0. |
| `nice -n 19 python3 -m pytest -q tools` | 252 passed, 1 skipped, in 301.19 s. The skip is the Lean build. `pytest` and `scipy` were not installed in this environment and were installed for this run; the first collection failed on a missing `sympy`, which was then installed. No lake build. |
