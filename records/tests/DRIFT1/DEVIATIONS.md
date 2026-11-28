# DRIFT1 deviations (after prereg commits ecac666 / 2a1fef8, 2026-11-14 22:26 ET)
1. Clock: PREREG.md says "~11:05 PM ET"; it was actually written and committed at 22:26 ET (git log is authoritative).
2. PROJECT/GitHub: the C3 pull only contains issues created <= 2021-12-31 AND updated since 2021-01-01, so the only
   complete window is issues+PRs created in calendar 2021; rate = count/365. Its hourly spectrum covers 2021 only,
   so no yearly cycle could be removed and the fit range is short.
3. CITY/311 hourly: Socrata has no date_trunc_ymdh; pulled with date_trunc_ymd + date_extract_hh instead (same counts).
4. POST HOC (found after the prereg'd run): for domains where every item shares one window (GitHub 2021, 311 2025),
   counts/365 sit on a discrete grid in log-rate, which the dip test and the GMM read as multimodality. supp.py
   dequantizes counts (n + U(-0.5, 0.5)) and reruns the same prereg'd rule. The prereg'd verdicts are reported alongside.
5. POST HOC, labelled: 311 items = complaint type only (n=185); Wikipedia rate over the last 5 years only.
6. Design weakness noticed after running (not changed): the GMM "well separated" check compares ANY pair of components,
   so a flat plateau tiled by several Gaussians passes it; the dip test (p < 0.01 required jointly) is the binding guard.
