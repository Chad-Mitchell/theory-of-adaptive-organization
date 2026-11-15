#!/usr/bin/env python3
"""Pre-lock dry run on synthetic truth (FRAMEWORK MV7/MV9). Synthetic SPF: each 'variable' is a world with known
(tauE, alpha, phi); 40 forecasters with private white noise K run the exact Wiener forecaster; actuals = x.
Arm T (truth = GTAO model): the pipeline should PASS. Arm X (forecasters use a static rule, beta = K regardless of
spectrum; i.e. they ignore the spectrum) and arm W (forecasters with alpha-2 filter in alpha != 2 worlds) check that the
verdict can come out otherwise."""
import json, sys
import numpy as np, pandas as pd
import model, analysis as A

def simulate_spf(tauE, alpha, phi, K, n, rng, nf=35, filt_env=None):
    burn = 600; L = n + burn + 8
    x = model.simulate(L, tauE, alpha, phi, rng); x = x / x.std()
    S = model.env_grid(*(filt_env or (tauE, alpha, phi)))
    H3, H4 = model.filters(S, K)
    h3 = np.fft.ifft(H3).real[:500]; h4 = np.fft.ifft(H4).real[:500]
    F3 = np.zeros((nf, L)); F4 = np.zeros((nf, L))
    for i in range(nf):
        y = x + np.sqrt(K) * rng.standard_normal(L)
        F3[i] = np.convolve(y, h3)[:L]; F4[i] = np.convolve(y, h4)[:L]
    t = np.arange(burn, burn + n)
    p = pd.DataFrame({"survey_q": t, "target_q": t + 3, "F_t": F3[:, t].mean(0), "F_tm1": F4[:, t - 1].mean(0), "actual": x[t + 3]})
    q75, q25 = np.percentile(F3[:, t], [75, 25], axis=0)
    disp = pd.DataFrame({"survey_q": t, "n": nf, "rvar": ((q75 - q25) / 1.349) ** 2, "sd": F3[:, t].std(0, ddof=1)})
    return x[burn - 240 + n: burn + n] if False else x[t], p, disp

def run(arm, seed, nvar=24, ndraw=20):
    rng = np.random.default_rng(seed)
    per = {}; rows = []
    for j in range(nvar):
        tauE = float(np.exp(rng.uniform(np.log(1.0), np.log(40)))); alpha = float(rng.uniform(1.3, 3.5)); phi = float(rng.uniform(0, 0.6))
        K = float(np.exp(rng.uniform(np.log(0.05), np.log(3))))
        fe = (tauE, 2.0, phi) if arm == "W" else None
        x, p, disp = simulate_spf(tauE, alpha, phi, K, 200, rng, filt_env=fe)
        th = model.whittle_fit(x); thM = A.whittle_fixed_alpha(x)
        mom, m = A.spf_moments(p, disp)
        gates = dict(E2=1.05 < th["alpha"] < 5.9, E3=th["tauE"] < len(x) / 4, E4=mom["se"] <= A.MAX_SE)
        if not all(gates.values()):
            print(f"{arm} v{j}: tau={tauE:.2f} a={alpha:.2f} phi={phi:.2f} K={K:.2f} excluded {gates} fit a={th['alpha']:.2f} se={mom['se']:.2f}", flush=True); continue
        nf = mom["nf"]
        G_, Kh, flag = A.predict(th, mom["ratio"], nf); Mk = A.predict(thM, mom["ratio"], nf)[0]
        sd = A.block_boot(m, rng, ndraw)
        draws = []
        for d in range(ndraw):
            xs = model.simulate(len(x), th["tauE"], th["alpha"], th["phi"], rng)
            e = model.whittle_fit(xs, starts=[(np.log(th["tauE"]), th["alpha"], th["phi"]), (np.log(2), 2.0, 0.3)])
            eM = A.whittle_fixed_alpha(model.simulate(len(x), thM["tauE"], 2.0, thM["phi"], rng))
            draws.append((sd[d][0], A.predict(e, sd[d][1], nf)[0], sd[d][1], A.predict(eM, sd[d][1], nf)[0]))
        per[f"v{j}"] = dict(beta=mom["beta"], G=G_, S=mom["ratio"], M=Mk, draws=draws)
        rows.append(dict(tauE=tauE, alpha=alpha, phi=phi, K=K, fit=th, beta=mom["beta"], pred=G_, static=mom["ratio"], alpha2=Mk,
                         Khat=Kh, beta_true=model.moments(model.env_grid(tauE, alpha, phi), K, nf=35)[0]))
        print(f"{arm} v{j}: tau={tauE:.2f} a={alpha:.2f} phi={phi:.2f} K={K:.2f} | fit tau={th['tauE']:.2f} a={th['alpha']:.2f} "
              f"| beta^={mom['beta']:.3f} true={rows[-1]['beta_true']:.3f} predG={G_:.3f} static={mom['ratio']:.3f} a2={Mk:.3f}", flush=True)
    res = A.evaluate(per, np.random.default_rng(seed + 1))
    nonpos = sum(per[v]["beta"] <= 0 for v in per)
    res["verdict"] = A.verdict(res, nonpos, len(per))
    print(arm, json.dumps(res))
    return dict(rows=rows, res=res)

if __name__ == "__main__":
    arm = sys.argv[1]; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    out = run(arm, seed)
    json.dump(out, open(f"results/synth_{arm}_{seed}.json", "w"), indent=1, default=float)
