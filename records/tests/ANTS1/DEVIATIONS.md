# ANTS1 deviations / clarifications after the PREREG commit (d38ff12)
1. Implementation order per step (clarification, decided after a smoke test showed e=1 scoring as a random guess):
   readout of F_{t-1} -> ants decide (followers sample F_{t-1}) -> evaporate -> deposit. The prereg said readouts are
   taken "before each step's deposits"; this keeps that, and makes e=1 mean "trail = last step's deposits" (gain 1),
   which is what the mean-field recursion assumed. Only e=1 behaviour changes; no predictions were edited.
2. The smoke test (4 jobs, seed 0) was looked at before the full run: IND/RW e* near K*, PRIV matching IND at N=1.
3. analyze.py written after the prereg, while the run was in progress; it implements the prereg estimators. It was smoke-tested on a partial copy of results (N=256 jobs only), which exposed only the C0 and P7 counts on 5 and 3 cells.
