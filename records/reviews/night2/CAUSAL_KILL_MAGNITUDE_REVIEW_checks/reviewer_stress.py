#!/usr/bin/env python3
"""Stress for Q2: short lag relative to tau (small s) with large tau uncertainty, and low reliability from few
duplicates. Reuses reviewer_mc.study/kill (reviewer's code). Plug-in and propagated rules; true design (b = b*)."""
import json, math, numpy as np
import reviewer_mc as M
rng = np.random.default_rng(505); out = {}
for z in (1.645, 1.96):
    for Lt in (0.25, 0.1):
        s = 1 - math.exp(-Lt)
        for sig_x, m in ((0.0, 0), (M.SD * math.sqrt(7 / 3), 10), (M.SD * math.sqrt(7 / 3), 20)):   # lam = 1, 0.3
            st = M.study(rng, .5, s=s, sig_x=sig_x)
            lam = M.SD**2 / (M.SD**2 + sig_x**2)
            for sd_lt in (0.5, 1.0):
                lt = Lt * np.exp(-sd_lt * rng.standard_normal(M.R)); sh = 1 - np.exp(-lt); ses = lt * np.exp(-lt) * sd_lt
                if sig_x:
                    sx2 = ((sig_x * math.sqrt(2) * rng.standard_normal((M.R, m))) ** 2).mean(1) / 2; V = st["sxx"] / M.K
                    lh = np.clip(1 - sx2 / V, 0.05, 1); sel = np.sqrt(2 * (sx2 / V) ** 2 * (1 / m + 1 / M.K))
                else:
                    lh = np.ones(M.R); sel = np.zeros(M.R)
                vs = (lh * ses) ** 2 + (sh * sel) ** 2
                for k in (.25, .5, 1.):
                    out[f"z={z} s={s:.2f} lam={lam:.1f} m={m} sd_logtau={sd_lt} k={k}"] = {
                        "plug": round(M.kill(st, k, z, sh * lh), 3), "prop": round(M.kill(st, k, z, sh * lh, (k * .5) ** 2 * vs), 3),
                        "known": round(M.kill(st, k, z, s * lam), 3)}
json.dump(out, open("reviewer_stress.json", "w"), indent=1)
for k, v in out.items(): print(f"{k:55s} {v}")
