"""Locked analysis. Usage: python analyze.py <tag> [--synthetic]
Seed 20261115. Inference: property-cluster pairs bootstrap (B_COEF=1000 refits for coefficients; B_AUC=2000 resamples of
leave-one-property-out out-of-fold predictions for dAUC). All logistic fits: sklearn LogisticRegression(C=10, lbfgs, max_iter=2000),
continuous covariates z-scored, fixed effects as one-hot (no reference dropping; L2 handles collinearity)."""
import sys, json, math, collections
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from scipy.stats import spearmanr
from props import PROPS, WIKIS, MONEY
import classify as C
import regime as RG
SEED = 20261115; B_COEF = 1000; B_AUC = 2000
DOM = {p: d for p, _, d, _ in PROPS}; DT = {p: t for p, _, _, t in PROPS}

def years(t0, t1):
    import datetime
    a = datetime.datetime.fromisoformat(t0.replace("Z", "+00:00")); b = datetime.datetime.fromisoformat(t1.replace("Z", "+00:00"))
    return (b - a).days / 365.25

def wilson(k, n, z=1.96):
    if n == 0: return (float("nan"),) * 2
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)

def build(tag):
    D = json.load(open(f"raw/{tag}_items.json")); P = json.load(open(f"raw/{tag}_pages.json"))
    dy = years(D["meta"]["T0"], D["meta"]["t1"])
    drift = {}
    for pid, *_ in PROPS:
        its = [x for x in D["items"] if x["pid"] == pid]
        ch = [C.drift(x) for x in its]; ch = [c for c in ch if c is not None]
        k, n = sum(ch), len(ch)
        pp = (k + 0.5) / (n + 1); lo, hi = wilson(k, n)
        ev = [C.dated_event(x, D["meta"]["T0"], D["meta"]["t1"]) for x in its]
        k2 = sum(ev); n2 = len(ev); m2 = -math.log(1 - (k2 + 0.5) / (n2 + 1)) / dy if n2 else None
        drift[pid] = {"k": k, "n": n, "lam": -math.log(1 - pp) / dy, "lam_raw": (-math.log(1 - k / n) / dy if n and k < n else None),
                      "lam_lo": -math.log(1 - lo) / dy if n else None, "lam_hi": (-math.log(1 - hi) / dy if n and hi < 1 else float("inf")),
                      "m2": m2, "k2": k2, "n2": n2}
    rows = []
    for x in D["items"]:
        for w, t in x["pages"].items():
            pg = P.get(f"{w}|{t}")
            if not pg: continue
            c = C.classify_page(x, pg, D["labels"])
            rows.append({"qid": x["qid"], "pid": x["pid"], "wiki": w, "mode": c["mode"], "refresh": c.get("refresh"),
                         "N": x["sitelinks_wiki"], "views": pg.get("views12m") or 0, "pageid": pg.get("pageid") or 0,
                         "used": c.get("used"), "used_specific": c.get("used_specific"), "mode_rendered": c.get("mode_rendered")})
    # page-age rank within wiki
    for w in WIKIS:
        rs = [r for r in rows if r["wiki"] == w]; ids = sorted(r["pageid"] for r in rs)
        for r in rs: r["age_rank"] = (np.searchsorted(ids, r["pageid"]) + 0.5) / max(1, len(ids))
    return D, drift, rows

def design(rows, drift, use_q=True, use_N=True, fe=("wiki", "domain")):
    cols = []
    for f in fe:
        levels = sorted({(r["wiki"] if f == "wiki" else DOM[r["pid"]] if f == "domain" else DT[r["pid"]]) for r in rows})
        cols.append(("fe", f, levels))
    X = []
    for r in rows:
        v = []
        for _, f, levels in cols:
            key = r["wiki"] if f == "wiki" else DOM[r["pid"]] if f == "domain" else DT[r["pid"]]
            v += [1.0 if key == l else 0.0 for l in levels]
        cont = [r["age_rank"]]
        if use_q: cont.append(math.log(drift[r["pid"]]["lam"]))
        if use_N: cont.append(math.log1p(r["N"]))
        X.append(v + cont)
    X = np.array(X); nfe = X.shape[1] - (1 + use_q + use_N)
    return X, nfe

def fit(X, y, nfe):
    mu = X[:, nfe:].mean(0); sd = X[:, nfe:].std(0); sd[sd == 0] = 1
    Z = X.copy(); Z[:, nfe:] = (X[:, nfe:] - mu) / sd
    m = LogisticRegression(C=10, max_iter=2000).fit(Z, y)
    return m, mu, sd

def predict(m, mu, sd, X, nfe):
    Z = X.copy(); Z[:, nfe:] = (X[:, nfe:] - mu) / sd
    return m.predict_proba(Z)[:, 1]

def coef_boot(rows, drift, ycol, names, rng, **kw):
    pids = sorted({r["pid"] for r in rows}); byp = collections.defaultdict(list)
    for r in rows: byp[r["pid"]].append(r)
    X, nfe = design(rows, drift, **kw); y = np.array([ycol(r) for r in rows])
    m, mu, sd = fit(X, y, nfe); est = m.coef_[0][nfe:]
    bs = []
    for b in range(B_COEF):
        samp = [r for p in rng.choice(pids, len(pids)) for r in byp[p]]
        yb = np.array([ycol(r) for r in samp])
        if yb.min() == yb.max(): continue
        Xb, nfe_b = design(samp, drift, **kw)
        if Xb[:, nfe_b:].std(0).min() == 0: continue
        mb, _, _ = fit(Xb, yb, nfe_b); bs.append(mb.coef_[0][nfe_b:])
    bs = np.array(bs)
    return {n: {"est": float(est[i]), "lo": float(np.percentile(bs[:, i], 2.5)), "hi": float(np.percentile(bs[:, i], 97.5)), "se": float(bs[:, i].std()), "B": len(bs)} for i, n in enumerate(names)}

def lopo(rows, drift, ycol, **kw):
    X, nfe = design(rows, drift, **kw); y = np.array([ycol(r) for r in rows]); pid = np.array([r["pid"] for r in rows])
    pred = np.zeros(len(rows))
    for p in sorted(set(pid)):
        tr = pid != p
        m, mu, sd = fit(X[tr], y[tr], nfe); pred[~tr] = predict(m, mu, sd, X[~tr], nfe)
    return pred, y, pid

def dauc(rows, drift, ycol, rng, kwG, kwR):
    pG, y, pid = lopo(rows, drift, ycol, **kwG); pR, _, _ = lopo(rows, drift, ycol, **kwR)
    est = roc_auc_score(y, pG) - roc_auc_score(y, pR)
    ps = sorted(set(pid)); idx = {p: np.where(pid == p)[0] for p in ps}; bs = []
    for b in range(B_AUC):
        ii = np.concatenate([idx[p] for p in rng.choice(ps, len(ps))])
        if y[ii].min() == y[ii].max(): continue
        bs.append(roc_auc_score(y[ii], pG[ii]) - roc_auc_score(y[ii], pR[ii]))
    return {"aucG": float(roc_auc_score(y, pG)), "aucR": float(roc_auc_score(y, pR)), "dAUC": float(est),
            "lo": float(np.percentile(bs, 2.5)), "hi": float(np.percentile(bs, 97.5)), "se": float(np.std(bs))}

def verdict_ci(lo, hi):
    return "PASS" if lo > 0 else ("FAIL" if hi < 0 else "INCONCLUSIVE")

def run(D, drift, rows):
    rng = np.random.default_rng(SEED); out = {"drift": drift}
    if D is not None:
        out["regime"] = {p: RG.estimate([x for x in D["items"] if x["pid"] == p], years("2000-01-01T00:00:00Z", D["meta"]["t1"]) + 2000, DT[p], rng) for p, *_ in PROPS}
        ok = {p for p, v in out["regime"].items() if v["regime"].startswith("A") and v["split_half"].get("stable")}
        moot = {p for p in drift if drift[p]["lam_hi"] <= 0.02}
        out["regime_ok_props"] = sorted(ok); out["regime_moot_props"] = sorted(moot)
    out["counts"] = {w: dict(collections.Counter(r["mode"] for r in rows if r["wiki"] == w)) for w in WIKIS}
    out["counts_by_prop"] = {p: dict(collections.Counter(r["mode"] for r in rows if r["pid"] == p)) for p, *_ in PROPS}
    lam = {p: drift[p]["lam"] for p in drift}
    # MV5 convergent validity of drift
    ps = [p for p in drift if drift[p]["m2"] is not None]
    out["MV5_spearman"] = float(spearmanr([lam[p] for p in ps], [drift[p]["m2"] for p in ps]).correlation)
    # KG
    order = sorted(lam, key=lam.get); kg_a = (drift["P569"]["lam_hi"] <= 0.02) and ("P569" in order[:3])
    kgb = {}
    for w in WIKIS:
        disp = [r for r in rows if r["wiki"] == w and r["pid"] == "P569" and r["mode"] in ("LOCAL", "LOOKUP")]
        if len(disp) >= 10: kgb[w] = sum(r["mode"] == "LOCAL" for r in disp) / len(disp)
    kgb_pass = {w: s >= 0.5 for w, s in kgb.items()}
    out["KG"] = {"a_drift": kg_a, "P569_rank": order.index("P569") + 1, "P569_lam_hi": drift["P569"]["lam_hi"], "b_local_share": kgb,
                 "b_pass_wikis": [w for w, v in kgb_pass.items() if v],
                 "PASS": bool(kg_a and len(kgb) >= 1 and sum(kgb_pass.values()) >= math.ceil(2 * len(kgb) / 3))}
    # KG-c (descriptive): software version not frozen
    lk = {}
    for w in WIKIS:
        sh = {}
        for p in lam:
            d = [r for r in rows if r["wiki"] == w and r["pid"] == p and r["mode"] in ("LOCAL", "LOOKUP")]
            if len(d) >= 5: sh[p] = sum(r["mode"] == "LOOKUP" for r in d) / len(d)
        lk[w] = sh
    out["lookup_share"] = lk
    # P1
    R = [r for r in rows if r["mode"] in ("LOCAL", "LOOKUP")]; y1 = lambda r: 1 if r["mode"] == "LOOKUP" else 0
    names = ["age_rank", "log_q", "log_N"]
    out["n_P1"] = len(R); out["n_P1_lookup"] = sum(map(y1, R))
    out["P1_coef"] = coef_boot(R, drift, y1, names, rng)
    out["P1_dAUC_domain"] = dauc(R, drift, y1, rng, dict(), dict(use_q=False, use_N=False))
    out["P1_dAUC_datatype"] = dauc(R, drift, y1, rng, dict(), dict(use_q=False, use_N=False, fe=("wiki", "datatype")))
    bq = out["P1_coef"]["log_q"]; da = out["P1_dAUC_domain"]
    if bq["lo"] > 0 and da["dAUC"] >= 0.02 and da["lo"] > 0: v = "PASS"
    elif bq["hi"] < 0 or (da["dAUC"] < 0.02 and da["lo"] <= 0): v = "FAIL"
    else: v = "INCONCLUSIVE"
    out["P1"] = v
    # P1 sensitivities (declared): excluding money props; KG-pass wikis only; TSTORE counted as shared
    Rm = [r for r in R if r["pid"] not in MONEY]; out["P1_sens_nomoney"] = coef_boot(Rm, drift, y1, names, rng)["log_q"]
    kgw = set(out["KG"]["b_pass_wikis"]); Rk = [r for r in R if r["wiki"] in kgw]
    out["P1_sens_kgwikis"] = coef_boot(Rk, drift, y1, names, rng)["log_q"] if len({r["wiki"] for r in Rk}) >= 1 and len(Rk) > 50 else None
    Rt = [r for r in rows if r["mode"] in ("LOCAL", "LOOKUP", "AMBIG")]; yt = lambda r: 0 if r["mode"] == "LOCAL" else 1
    out["P1_sens_ambig_as_lookup"] = coef_boot(Rt, drift, yt, names, rng)["log_q"]
    vr = [r for r in rows if r.get("mode_rendered")]
    out["validation_rendered"] = dict(collections.Counter(f'{r["mode"]}->{r["mode_rendered"]}' for r in vr))
    if D is not None:
        keep = set(out["regime_ok_props"]) | set(out["regime_moot_props"]); Rg = [r for r in R if r["pid"] in keep]
        out["P1_sens_regimeA_or_moot"] = coef_boot(Rg, drift, y1, names, rng)["log_q"] if len({r["pid"] for r in Rg}) >= 5 and 0 < sum(map(y1, Rg)) < len(Rg) else None
    # P2
    bN = out["P1_coef"]["log_N"]; out["P2"] = verdict_ci(bN["lo"], bN["hi"])
    # P3 refresh
    F = [r for r in rows if r["mode"] == "LOCAL" and r["refresh"] in ("REFRESHED", "STALE")]
    out["n_P3"] = len(F); out["n_P3_refreshed"] = sum(r["refresh"] == "REFRESHED" for r in F)
    yf = lambda r: 1 if r["refresh"] == "REFRESHED" else 0
    if len({r["pid"] for r in F}) >= 5 and 0 < out["n_P3_refreshed"] < len(F):
        out["P3_coef"] = coef_boot(F, drift, yf, ["age_rank", "log_q"], rng, use_N=False, fe=("wiki",))
        b3 = out["P3_coef"]["log_q"]; out["P3"] = verdict_ci(b3["lo"], b3["hi"])
    else: out["P3"] = "INCONCLUSIVE (insufficient data)"
    # P4 replication
    per = {}
    for w in WIKIS:
        Rw = [r for r in R if r["wiki"] == w]; nl = sum(map(y1, Rw))
        if nl >= 10 and len(Rw) - nl >= 10:
            X, nfe = design(Rw, drift, fe=("domain",)); m, _, _ = fit(X, np.array([y1(r) for r in Rw]), nfe)
            per[w] = {"b_q": float(m.coef_[0][nfe + 1]), "b_N": float(m.coef_[0][nfe + 2]), "n": len(Rw), "n_lookup": nl}
    k = len(per); pos = sum(v["b_q"] > 0 for v in per.values())
    out["P4_per_wiki"] = per
    out["P4"] = "INCONCLUSIVE (k<4)" if k < 4 else ("PASS" if pos / k >= 5 / 6 - 1e-9 else ("FAIL" if pos / k <= 0.5 else "INCONCLUSIVE"))
    # descriptive band: lookup share by drift tercile
    t = np.percentile(list(lam.values()), [33.3, 66.7])
    out["band"] = {name: {m: sum(1 for r in rows if r["mode"] == m and f(lam[r["pid"]])) for m in ("LOCAL", "LOOKUP", "AMBIG", "ABSENT")}
                   for name, f in [("low", lambda q: q <= t[0]), ("mid", lambda q: t[0] < q <= t[1]), ("high", lambda q: q > t[1])]}
    return out

def synthetic():
    """Dry run on synthetic truth: known positive drift and N effects must be recovered; null must not be."""
    rng = np.random.default_rng(1)
    for eff in (1.0, 0.0):
        drift = {p: {"lam": float(np.exp(rng.uniform(-5, 0))), "lam_hi": 0.01, "k": 0, "n": 60, "m2": 1.0} for p, *_ in PROPS}
        drift["P569"]["lam"] = 0.001
        rows = []
        for p, *_ in PROPS:
            for i in range(60):
                N = int(rng.integers(1, 200)); 
                for w in WIKIS[: rng.integers(1, 7)]:
                    eta = {"en": -2, "de": -2.5, "fr": 0, "ru": 0.5, "it": -1, "ca": 1}[w] + eff * (0.8 * math.log(drift[p]["lam"]) + 2.5 + 0.5 * (math.log1p(N) - 2.5))
                    mode = "LOOKUP" if rng.random() < 1 / (1 + math.exp(-eta)) else "LOCAL"
                    ref = ("REFRESHED" if rng.random() < 1 / (1 + math.exp(-eff * (math.log(drift[p]["lam"]) + 2.5))) else "STALE") if mode == "LOCAL" and rng.random() < 0.3 else None
                    rows.append({"qid": f"{p}-{i}", "pid": p, "wiki": w, "mode": mode, "refresh": ref, "N": N, "views": int(rng.integers(0, 10**5)), "pageid": int(rng.integers(1, 10**7)), "age_rank": rng.random()})
        global B_COEF, B_AUC
        B_COEF, B_AUC = 200, 500
        o = run(None, drift, rows)
        print("synthetic effect", eff, "P1", o["P1"], o["P1_coef"]["log_q"], "dAUC", round(o["P1_dAUC_domain"]["dAUC"], 3), "P2", o["P2"], "P3", o["P3"], "P4", o["P4"])

if __name__ == "__main__":
    if "--synthetic" in sys.argv: synthetic(); sys.exit()
    tag = sys.argv[1]; D, drift, rows = build(tag); out = run(D, drift, rows)
    json.dump({"rows": rows}, open(f"{tag}_rows.json", "w")); json.dump(out, open(f"{tag}_results.json", "w"), indent=1, default=str)
    print(json.dumps({k: out[k] for k in ("P1", "P2", "P3", "P4", "KG", "MV5_spearman", "n_P1", "n_P1_lookup", "n_P3")}, indent=1, default=str))
