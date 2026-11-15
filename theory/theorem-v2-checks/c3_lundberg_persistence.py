"""C3. Persistence (ruin) as the single objective. Reserve R: income y dt + s0 dW0, pays check cost c every tau and
holding loss w*e_t^2 dt with e = sigma*W (reset at checks).  Ruin when R hits 0 from buffer B."""
import numpy as np, sympy as sp
from scipy import optimize
rng = np.random.default_rng(3)
print("== C3a: Var(int_0^tau W^2 dt) = tau^4/3 and E exp(b int W^2) = cos(tau sqrt(2b))^(-1/2) (Cameron-Martin) ==")
n, steps, tau = 200_000, 1000, 1.0; dt = tau/steps; W = np.zeros(n); I = np.zeros(n)
for _ in range(steps):
    Wn = W + np.sqrt(dt)*rng.standard_normal(n); I += 0.5*(W**2+Wn**2)*dt; W = Wn
print(f"  mean {I.mean():.4f} (1/2)  var {I.var():.4f} (1/3)  E e^(0.3 I)={np.mean(np.exp(0.3*I)):.4f} vs {np.cos(np.sqrt(0.6))**-0.5:.4f}")
y, c, w, sig, s0 = 1.0, 0.05, 1.0, 1.0, 0.5
m = lambda t: y - c/t - w*sig**2*t/2
s2 = lambda t: s0**2 + w**2*sig**4*t**3/3
def theta_exact(t):
    """Lundberg exponent of the cycle-level random walk D = y t - c - w sig^2 I_t + s0 sqrt(t) N : E exp(-th D) = 1."""
    f = lambda th: -th*(y*t-c) + th**2*s0**2*t/2 - 0.5*np.log(np.cos(t*np.sqrt(2*th*w*sig**2)))
    hi = (np.pi/2)**2/(2*w*sig**2*t**2)*0.999999
    if y*t - c - w*sig**2*t**2/2 <= 0: return 0.0   # nonpositive mean increment: ruin certain
    return optimize.brentq(f, 1e-9, hi)
print("== C3b: survival-optimal tau maximizes the Lundberg exponent theta(tau); diffusion approx theta ~ 2 m/s^2 ==")
ts = np.linspace(0.05, 1.2, 400)
th_ex = np.array([theta_exact(t) for t in ts]); th_d = 2*m(ts)/s2(ts)
t_eoq = np.sqrt(2*c/(w*sig**2)); t_ex = ts[np.nanargmax(th_ex)]; t_d = ts[np.argmax(th_d)]
print(f"  EOQ (mean-cost) tau* = {t_eoq:.3f};  survival-optimal tau* (exact Lundberg) = {t_ex:.3f};  (diffusion approx) = {t_d:.3f}")
for t in [0.15, t_ex, t_eoq, 0.6]:
    print(f"   tau={t:.3f}: margin m={m(t):.4f}  s^2={s2(t):.4f}  theta_exact={theta_exact(t):.4f}  theta_diff={2*m(t)/s2(t):.4f}")
print("  => survival-optimal checking is FASTER than cost-optimal when loss variance grows with tau (here s^2 has a tau^3 term).")
print("  => argmax_tau theta does not involve B: under Lundberg asymptotics the optimal check interval is independent of the buffer.")
print("== C3c: Monte Carlo ruin vs exp(-theta B) (cycle-level walk, exact cycle increments sampled from simulated I) ==")
def mc_ruin(t, B, n=20_000, cycles=3000):
    R = np.full(n, B); alive = np.ones(n, bool); k = int(round(t/dt))
    for _ in range(cycles):
        Is = I[rng.integers(0, len(I), n)]*t**2   # scaling: int_0^t W^2 = t^2 * int_0^1 W'^2
        R = R + y*t - c - w*sig**2*Is + s0*np.sqrt(t)*rng.standard_normal(n); alive &= R > 0
    return 1-alive.mean()
for t in [t_ex, 0.6]:
    th = theta_exact(t)
    for B in [0.5, 1.0, 2.0]:
        print(f"  tau={t:.3f} B={B}: MC ruin={mc_ruin(t, B):.4f}  exp(-theta B)={np.exp(-th*B):.4f} (Lundberg bound; Cramer constant <1)")
print("== C3d: value of improving theta when ruin costs V: d/dtheta [V e^{-theta B}] = -V B e^{-theta B}; maximized over B at theta*B = 1 ==")
B = sp.symbols('B', positive=True); th = sp.symbols('theta', positive=True)
print("  argmax_B B e^{-theta B} =", sp.solve(sp.diff(B*sp.exp(-th*B), B), B))
print("  => effort to improve survival is worth most when the buffer is ~one ruin length 1/theta = s^2/(2m):")
print("     'watch most where shocks are large relative to buffers but not yet overwhelming them' (rule 7, last clause) follows here.")
