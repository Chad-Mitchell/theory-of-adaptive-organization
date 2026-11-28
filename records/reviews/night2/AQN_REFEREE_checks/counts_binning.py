"""Event-world check: does the count Whittle (aqn.whittle_counts, object under test) recover the slope of a
CONTINUOUS-time rate when counts integrate the rate over each bin (real event data), rather than the
piecewise-constant per-bin rate used in the locked validation? Rate z(t): own OU-mixture with nominal alpha = 1 from
corners 1e-4 to 1e2 rad/bin (so power above Nyquist exists); Lambda = 5(1 + z), sd(z) = 0.3, 16 substeps per bin."""
import numpy as np, sys
from scipy.signal import lfilter
sys.path.insert(0, '../../../measurement/estimators')
import aqn
def ou_mix(nsteps, dt, corners, sd, rng):
    out = np.zeros(nsteps); v = sd**2/len(corners)
    for w0 in corners:
        phi = np.exp(-w0*dt); e = rng.standard_normal(nsteps)*np.sqrt(v*(1-phi**2))
        x0 = rng.standard_normal()*np.sqrt(v)
        out += lfilter([1], [1, -phi], e, zi=[phi*x0])[0]
    return out
n, sub, Lbar = 8192, 16, 5.0
corners = np.geomspace(1e-4, 1e2, 48)
res = {'binned': [], 'piecewise': []}
for rep in range(40):
    rng = np.random.default_rng(31337 + rep)
    z = ou_mix(n*sub, 1/sub, corners, 0.3, rng)
    lam_bin = Lbar*(1 + z).reshape(n, sub).mean(1)            # integrated rate per bin (real data)
    lam_pw = Lbar*(1 + z[::sub])                              # piecewise constant at bin starts (locked simulator)
    for key, lam in (('binned', lam_bin), ('piecewise', lam_pw)):
        c = rng.poisson(np.clip(lam, 0, None))
        r = aqn.whittle_counts(c, band=(0.002, np.pi), fix_s2=c.mean())
        res[key].append(r['alpha'])
# continuous-time slope of S_z over the band (local log-log slope from the exact Lorentzian sum)
w = np.geomspace(0.002, np.pi, 200); S = sum(2*w0/(w**2 + w0**2) for w0 in corners)
print("continuous-rate band slope (OLS log S on log w over [0.002, pi]): %.3f" % -np.polyfit(np.log(w), np.log(S), 1)[0])
for k, v in res.items():
    v = np.array(v); print(f"{k:9s}: median alpha-hat {np.median(v):.3f}, sd {v.std(ddof=1):.3f} (40 reps, n={n}, Poisson floor fixed)")
