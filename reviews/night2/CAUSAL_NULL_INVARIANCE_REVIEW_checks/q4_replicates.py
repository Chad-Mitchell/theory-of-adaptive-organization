"""Q4 follow-up: spread of D across independent replicate runs of the locked design (own implementation, q4_learner.py)."""
import json, math, numpy as np, sys
import q4_learner as Q   # running the module performs replicate 0 (seeds 51000/52000); below: 6 more seed bases
reps = [dict(base=(51000, 52000), D=Q.out["D"], sigma=Q.out["sigma"], verdict=Q.out["verdict"])]
for r in range(1, 7):
    res = {}
    for k, (lam, mu, s0) in {"A": (0.01, 2.0, 51000 + 1000 * r * 2), "B": (0.02, math.sqrt(2.0), 52000 + 1000 * r * 2)}.items():
        PP, G, LIN = Q.family(lam, mu); rows = []
        for i in range(24):
            m = Q.experience_mse(lam, mu, PP, G, LIN, int(20 / (lam * Q.D)), s0 + i); j = int(np.argmin(m))
            rows.append((bool(LIN[j]), Q.test_tA(lam, mu, PP[j], G[j], LIN[j], int(200 / (lam * Q.D)), 9_000_000 + s0 + i), int(j)))
        res[k] = rows
    lt = {k: np.log([t for _, t, _ in v]) for k, v in res.items()}
    Dh = float(lt["B"].mean() - lt["A"].mean()); sig = float(math.sqrt(lt["A"].var(ddof=1) / 24 + lt["B"].var(ddof=1) / 24))
    fail = Dh + 1.959964 * sig < 0.1752; pas = Dh - 1.959964 * sig > 0 and not fail
    reps.append(dict(rep=r, D=Dh, sigma=sig, verdict="FAILED" if fail else ("PASSED" if pas else "INCONCLUSIVE"),
                     nlin=sum(l for l, _, _ in res["A"]) + sum(l for l, _, _ in res["B"])))
    print(reps[-1], flush=True)
Ds = np.array([r["D"] for r in reps]); sg = np.array([r["sigma"] for r in reps])
summ = dict(reps=reps, mean_D=float(Ds.mean()), sd_D_across=float(Ds.std(ddof=1)), mean_sigma=float(sg.mean()),
            pooled_se=float(Ds.std(ddof=1) / math.sqrt(len(Ds))))
print(json.dumps({k: v for k, v in summ.items() if k != "reps"}, indent=1))
json.dump(summ, open("q4_replicates.json", "w"), indent=1, default=float)
