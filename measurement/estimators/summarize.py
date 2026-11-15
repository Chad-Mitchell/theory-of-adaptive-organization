"""Summaries of results/*.json -> results/summary_<block>.txt (bias, RMSE, 95% Wald coverage) and the asymptotic
sample-length table (expected Whittle information at the truth)."""
import json, sys, gzip, os, numpy as np
from math import log, pi
import aqn, validate as V

def _load(p):
    p = p if isinstance(p, str) else p[0]
    return json.load(gzip.open(p + ".gz")) if os.path.exists(p + ".gz") else json.load(open(p))

def cov95(est, se, truth):
    est = np.asarray(est, float); se = np.asarray(se, float)
    ok = np.isfinite(est) & np.isfinite(se)
    return float(np.mean(np.abs(est[ok] - truth) <= 1.96 * se[ok])), int(ok.sum())

def stats(est, truth):
    e = np.asarray([x for x in est if x is not None], float); e = e[np.isfinite(e)]
    return float(np.mean(e) - truth), float(np.sqrt(np.mean((e - truth) ** 2))), float(np.median(e) - truth)

def line(name, rs, key, truth, sekey=None):
    b, rm, md = stats([r[key] for r in rs], truth)
    s = f"  {name:10s} truth {truth:8.3f} bias {b:+.3f} (median {md:+.3f}) RMSE {rm:.3f}"
    if sekey:
        c, k = cov95([r[key] if r[key] is not None else np.nan for r in rs], [r[sekey] for r in rs], truth)
        s += f" cov95 {c:.2f} (n={k}) meanSE {np.nanmean([r[sekey] for r in rs]):.3f}"
    return s

def by_ci(d):
    out = {}
    for r in d["results"]:
        out.setdefault(r["ci"], []).append(r)
    return out

def A():
    d = _load(("results/A.json")); g = by_ci(d); L = []
    for ci, (a, wc, n) in enumerate(V.A_conds()):
        rs = g[ci]; s2 = wc ** -a
        L.append(f"A ci={ci} alpha={a} w_c={wc} n={n} reps={len(rs)} at_bound={sum(r['at_bound'] for r in rs)}")
        L.append(line("alpha", rs, "alpha", a, "se_alpha")); L.append(line("log q", rs, "logq", 0.0, "se_logq"))
        L.append(line("log s2", rs, "logs2", log(s2), "se_logs2"))
        if "dfa" in rs[0]:
            r2 = [r for r in rs if "dfa" in r]
            L.append(line("DFA alpha", r2, "dfa", a)); L.append(line("VG alpha", r2, "vg_alpha", a))
            L.append(line("VG log q", r2, "vg_logq", 0.0)); L.append(line("VG log s2", r2, "vg_logs2", log(s2)))
    return L

def B():
    d = _load(("results/B.json")); g = by_ci(d); L = []
    for ci, (kind, n, band) in enumerate(V.B_conds()):
        rs = g[ci]; t = d["truth"][str(ci)]
        LR = np.array([r["LR"] for r in rs])
        L.append(f"B ci={ci} {kind} n={n} band={band} reps={len(rs)} pseudo-true (logq, alpha, logs2) = {np.round(t, 3).tolist()}")
        L.append(line("alpha", rs, "alpha", t[1], "se_alpha")); L.append(line("log q", rs, "logq", t[0], "se_logq"))
        L.append(line("log s2", rs, "logs2", t[2], "se_logs2"))
        L.append(f"  corner check: share LR > 2.71: {np.mean(LR > 2.71):.2f}; > 6.63: {np.mean(LR > 6.63):.2f}; median w0 {np.median([r['w0'] for r in rs]):.4f}; median corner-model alpha {np.median([r['corner_alpha'] for r in rs]):.3f}")
    return L

def C():
    d = _load(("results/C.json")); g = by_ci(d); L = []
    for ci, (s, lam, n) in enumerate(V.C_conds()):
        rs = g[ci]; t = V.C_truth(ci)
        L.append(f"C ci={ci} sigma={s} lam={lam} n={n} kappa={t['kappa']:.4f} per-sample SNR mu^2/s2={1/s**2:.2f} expected switches {lam*n:.0f} reps={len(rs)}")
        for k in ("loglam", "logmu", "logs2", "logtA", "logq"):
            L.append(line(k, rs, k, t[k], "se_" + k))
        L.append(line("OU log q", rs, "ou_logq", t["logq"])); L.append(line("OU loglam", rs, "ou_loglam", t["loglam"]))
        L.append(f"  LR(HMM vs OU) median {np.median([r['LR'] for r in rs]):.1f}")
    return L

def P():
    d = _load(("results/P.json")); g = by_ci(d); L = []
    for ci, c in enumerate(V.P_CONDS):
        rs = g[ci]; p = np.array([r["p"] for r in rs])
        L.append(f"P ci={ci} {c} reps={len(rs)} reject(p<=0.05) {np.mean(p <= 0.05):.2f} reject(p<=0.10) {np.mean(p <= 0.10):.2f} median LR {np.median([r['LR'] for r in rs]):.1f}")
    return L

def E():
    d = _load(("results/E.json")); g = by_ci(d); L = []; ET = V.E_truth()
    for ci, (kind, par, n) in enumerate(V.E_CONDS):
        rs = g[ci]
        L.append(f"E ci={ci} {kind} par={par} n={n} reps={len(rs)}")
        if kind == "cox":
            t = ET[ci]  # recomputed: the truth stored in E.json (first run) was 2*pi too large in density (fixed in validate.E_truth)
            L.append(f"  pseudo-true (logq, alpha, logs2) {np.round(t, 3).tolist()} (s2 true = mean count {par})")
            L.append(line("alpha", rs, "alpha", t[1], "se_alpha")); L.append(line("log q", rs, "logq", t[0], "se_logq"))
            L.append(line("alpha fix", rs, "alpha_fix", t[1], "se_alpha_fix")); L.append(line("logq fix", rs, "logq_fix", t[0], "se_logq_fix"))
        if kind in ("cox", "renewal"):
            ff = np.array([r["fano_floor"] for r in rs]); z = np.array([r["gap_z"] for r in rs])
            L.append(f"  free floor / mean: median {np.median(ff):.3f} [{np.percentile(ff, 5):.3f}, {np.percentile(ff, 95):.3f}]; alpha median {np.median([r['alpha'] for r in rs]):.3f}; gap-order z median {np.median(z):.2f}, share z > 1.96: {np.mean(z > 1.96):.2f}")
        if kind == "mmpp":
            L.append(line("loglam", rs, "loglam", log(par), "se_loglam"))
            L.append(f"  r0 median {np.median([r['r0'] for r in rs]):.3f} (1.0)  r1 median {np.median([r['r1'] for r in rs]):.3f} (3.0)")
    return L

def S():
    d = _load(("results/S.json")); g = by_ci(d); L = []
    for ci, (n, ru, endo) in enumerate(V.S_CONDS):
        rs = g[ci]; w = np.mean([r["w_true_mean"] for r in rs])
        o = np.array([r["w_ols"] for r in rs]); oc = np.mean([(r["ols_lo"] <= w <= r["ols_hi"]) for r in rs])
        s = f"S ci={ci} n={n} meas-noise ratio={ru} self-selected error={endo}: OLS median {np.median(o):.3f} (true mean w {w:.2f}) cov95 {oc:.2f}"
        if "w_iv" in rs[0]:
            iv = np.array([r["w_iv"] for r in rs]); ic = np.mean([(r["iv_lo"] <= w <= r["iv_hi"]) for r in rs])
            s += f"; IV median {np.median(iv):.3f} cov95 {ic:.2f}"
        L.append(s)
    return L

def asym():
    L = ["Asymptotic SE(alpha) from expected Whittle information at the truth (q = 1), and n needed for SE(alpha) <= 0.05 (95% CI about +/-0.1)"]
    for a in (1.4, 2.0, 2.6):
        for wc in (0.005, 0.05, 0.5, 3.0):
            row = []
            for n in (512, 2048, 8192, 32768, 131072):
                w = 2 * pi * np.arange(1, n // 2) / n
                th = [0.0, a, log(wc ** -a)]
                gr = aqn._grad_logf(w, th); cov = np.linalg.inv(gr @ gr.T)
                row.append(np.sqrt(cov[1, 1]))
            # n needed: SE ~ c n^-1/2 asymptotically once n w_c >> 1; interpolate on log scale
            ns = np.array([512, 2048, 8192, 32768, 131072]); se = np.array(row)
            need = next((int(n) for n, s_ in zip(ns, se) if s_ <= 0.05), None)
            if need is None:
                need = int(ns[-1] * (se[-1] / 0.05) ** 2)
                need = f">131072 (~{need} by n^-1/2 extrapolation)"
            L.append(f"  alpha={a} w_c={wc}: SE at n=512..131072: {np.round(se, 3).tolist()}; first n with SE<=0.05: {need}")
    return L

if __name__ == "__main__":
    for b in sys.argv[1:]:
        L = {"A": A, "B": B, "C": C, "P": P, "E": E, "S": S, "asym": asym}[b]()
        open(f"results/summary_{b}.txt", "w").write("\n".join(L) + "\n"); print("\n".join(L))
