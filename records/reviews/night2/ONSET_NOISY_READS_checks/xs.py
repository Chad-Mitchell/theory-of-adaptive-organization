"""ONSET-NOISY-READS check 4 (own code). The small-rho scaling function X(s): N* rho = X(s), s = s2/rho (level read noise
over shared drift, member units), from x D_m = Psi(x, s), Psi(x,s) = min_T 1/T + x T^(a-1) f(s/T^(a-1)), D_m = D0 (members
exact). Reports the local onset exponent e(s) = -1 - dlnX/dlns, s where e = -1.25/-1.5/-1.75, the asymptote-crossing
s_c = X0/C_inf, the level's z at the onset, and the max error of the two-asymptote sum X0 + C_inf s."""
import numpy as np, math, json
from scipy import optimize
import onset as O
O.ZHI.update({1.25: 1e3, 2.75: 1e4})
res = {}
for a in (1.25, 1.5, 2.0, 2.5, 2.75):
    Fa = O.F(a); X0, Ci, D0 = O.closed(a, Fa.f0, Fa.g)
    def Psi(x, s, retT=False):
        obj = lambda lT: math.exp(-lT) + x*math.exp((a-1)*lT)*Fa(s/math.exp((a-1)*lT))
        r = optimize.minimize_scalar(obj, bounds=(-60, 60), method='bounded', options={'xatol': 1e-11})
        return (r.fun, math.exp(r.x)) if retT else r.fun
    def X(s):
        if s == 0: return optimize.brentq(lambda lx: math.exp(lx)*D0 - Psi(math.exp(lx), 0.0), -5, 20)
        return math.exp(optimize.brentq(lambda lx: math.exp(lx)*D0 - Psi(math.exp(lx), s), math.log(0.5*X0), math.log(5*(X0+Ci*s)), xtol=1e-13))
    ss = np.logspace(-4, 3, 57); Xs = np.array([X(s) for s in ss])
    e = -1 - np.gradient(np.log(Xs), np.log(ss))
    def s_at(target):
        i = np.where(np.diff(np.sign(e - target)))[0][0]
        return float(math.exp(np.interp(target, [e[i+1], e[i]], [math.log(ss[i+1]), math.log(ss[i])])))
    sc = X0/Ci
    z_at = {}
    for s in (sc, 10*sc, 0.1*sc):
        x = X(s); _, T = Psi(x, s, True); z_at[f"{s:.4g}"] = s/T**(a-1)
    r = {"f0": Fa.f0, "g": Fa.g, "X0": X0, "X0_numeric": math.exp(X(0)), "Cinf": Ci, "s_c": sc, "rhoc_over_s2": 1/sc,
         "s_e": {str(t): s_at(t) for t in (-1.25, -1.5, -1.75)},
         "two_asym_max_dev": float(np.max(np.abs(Xs/(X0+Ci*ss)-1))), "s_at_max_dev": float(ss[np.argmax(np.abs(Xs/(X0+Ci*ss)-1))]),
         "e_table": {f"{s:.3g}": round(float(v), 4) for s, v in zip(ss[::4], e[::4])}, "z_level_at": z_at,
         "XoverCs_at_1e3": float(Xs[-1]/(Ci*ss[-1]))}
    res[str(a)] = r
    print(f"\n== alpha={a}: f0={Fa.f0:.6f} g={Fa.g:.6f} X0={X0:.5f} (numeric {r['X0_numeric']:.5f}) C_inf={Ci:.4f} "
          f"s_c=X0/C_inf={sc:.4f} (rho_c = {1/sc:.3f} s2)")
    print(f"  s where local exponent = -1.25/-1.5/-1.75: " + ", ".join(f"{v:.4g}" for v in r['s_e'].values()))
    print(f"  two-asymptote sum max |dev| {r['two_asym_max_dev']:.3f} at s={r['s_at_max_dev']:.3g}; X/(C s) at s=1e3: {r['XoverCs_at_1e3']:.4f}")
    print(f"  level z at onset (s_c, 10 s_c, 0.1 s_c): " + ", ".join(f"{v:.3g}" for v in z_at.values()))
    print("  e(s):", r['e_table'], flush=True)
json.dump(res, open("xs.json", "w"), indent=1)
