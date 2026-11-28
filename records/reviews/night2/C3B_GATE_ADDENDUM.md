# C3B-GATE-ADDENDUM (pick 31, unaided slot; ledger 142–144, outcome 152) — 15 Nov 2026 ~6:40 PM ET

**Deliverable:** `tests/C3b/PREREG_ADDENDUM_A3.md` (dated, before stage 4; hash appended to `tests/C3b/PREREG.sha256`;
PREREG/A1/A2 hashes verified unchanged). Checks: `reviews/night2/C3B_GATE_checks/` (`count_n.py` + `count_n.json`,
`gate_sim.py` + `sim_n{1000,1500,2294,5000}.jsonl`; own code, imports nothing from `tests/C3b/code`; nice 19).

**Result (process; not a proxy test of the theory).** Real Arm P n from the pre-shock screen (rules 1–4, deduped):
**2,294** upper bound (exposure and landmark not yet applied), about 5× the 300–500 the audit assumed. At that bound,
on PREREG §5's own assumed data: P(HIT | theory-sized effect) 0.86, P(MISS | null) 0.65 → **MV10 NOT MET** (FAIL side);
without the assumed confounder, 0.75 and 0.93 → still not met (PASS side; S9's latency control is nearly collinear with
tau). Gate would need n ≈ 3,500–4,000 (interpolated), which the frame cannot supply. Closed form (`power_gate.py`, H1/K1
only) agrees with the simulation (P(FAIL | null) 0.90 vs 0.925 simulated at matching SE). The author's own
`power_output.txt` K1 rate (0.44 at n 1,200, confounded) sits between this simulation's 0.32 (n 1,000) and 0.51 (n 1,500).

**Reading rule added before stage 4:** the C3b mechanism and index verdicts, if run, are labelled exploratory (MV10 not
met at lock); no CLAIM_MAP status change on them alone. Locked rules unchanged.

**Surprise read: weak.** The real n is ~5× the audit's projection, so H1/K1 alone would pass the gate; the binding
constraints are the conjunctive HIT (S9 collinearity) and the assumed confounder's +0.045 bias against K1's absolute
0.15 margin. New item C3B-STAGE4-DECIDE.

**Not done:** stages 3–6 not run; index verdict (K3/bootstrap) not simulated; landmark/exposure attrition unknown.
No THEORY edit, no CLAIM_MAP change, nothing contacted or bought. Vigilance (H8) stays OPEN.
