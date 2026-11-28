"""Checks for SCALE_ENDS §2 (T8 limit as read cost -> infinity) and §5 (lateness bound on tracker extent).
Run: nice -n 19 python3 band_latency.py"""
import numpy as np
rng=np.random.default_rng(20261118)
# --- T8 (theory/axioms/THEOREMS.md Thm 8): q_f=2c/(W H^2), q_c=(mu u-h)^2/(2cW); band iff mu u H > 2c + h H
W,H,mu,u,h=1.0,10.0,1.0,1.0,0.1
print("T8 band vs read cost c (W=1,H=10,mu=1,u=1,h=0.1):")
for c in [0.01,0.1,1,4.4,4.6,10,1e3,1e9]:
    qf=2*c/(W*H**2); qc=(mu*u-h)**2/(2*c*W); band=(mu*u*H>2*c+h*H)
    print(f"  c={c:<8g} q_f={qf:.3g} q_c={qc:.3g} band_exists={band} (q_c>q_f: {qc>qf})")
# brute-force: for c large, best mode over q grid is never 'hold'
def modes(q,c):
    Ts=np.linspace(1e-3,H,4000); hold=np.min(c/Ts+W*q*Ts/2)+h
    T=H; freeze=c/T+W*q*T/2   # freezing = corner T=H (read once per lifetime)
    look=mu*u
    # hold is the interior; freeze is the corner T=H (hold cost without upkeep counted as frozen copy)
    Tstar=np.sqrt(2*c/(W*q)) if q>0 else np.inf
    interior = Tstar<H
    best=min(("hold",hold if interior else np.inf),("freeze",freeze),("lookup",look),key=lambda x:x[1])
    return best[0]
for c in [0.1,1e3]:
    got=set(modes(q,c) for q in np.logspace(-6,4,200))
    print(f"  brute force modes reached over q in [1e-6,1e4] at c={c}: {sorted(got)}")
# --- Lateness: random walk target, reads every T, each read delivers value l old.
# Mean squared error should be q*(T/2 + l). Monte Carlo.
q,T,l,dt=1.0,1.0,0.7,1e-2
P,n=4000,int(20/dt); lag=int(round(l/dt)); per=int(round(T/dt))
x=np.cumsum(rng.normal(0,np.sqrt(q*dt),(P,n)),axis=1)
i=np.arange(n); k=(i//per)*per-lag; ok=k>=0
est=np.where(ok, x[:,np.clip(k,0,None)], 0.0)
m=lag+per
mse=np.mean((x[:,m:]-est[:,m:])**2)
print(f"Lateness MC ({P} paths): mse={mse:.4f}, predicted q(T/2+l)={q*(T/2+l):.4f} (discrete-time grid adds ~dt/2)")
# fBm-type structure function: E(dx^2)=q tau^(alpha-1); lateness term W q l^(alpha-1). Check scaling symbolically only:
for a in (1.5,2.0,2.5):
    print(f"  alpha={a}: L_max ∝ c*(F/(W q))^(1/(alpha-1)) -> exponent on q = {-1/(a-1):.2f}")
