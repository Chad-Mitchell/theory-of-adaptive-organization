"""S12 (adversarial pass): first-principles Monte Carlo of the R1 building block, independent of any closed form.
Simulate Brownian drift (rate q), periodic complete reads every T with random phase; measure time-averaged squared
error; compare with qT/2. Then pick T on a grid by simulated cost c/T + W*mean(e^2) and compare the minimized cost
with sqrt(2cWq) and the exponents a=b=1/2 by finite differences on simulated costs."""
import numpy as np
rng=np.random.default_rng(12)
def sim_mse(q,T,n_cycles=4000,steps=200):
    dt=T/steps
    inc=rng.normal(0,np.sqrt(q*dt),(n_cycles,steps))
    e=np.cumsum(inc,axis=1)       # error since last read (reset to 0 at each read)
    return np.mean(e**2)
for q,T in [(1,1),(0.1,2),(4,0.25)]:
    m=sim_mse(q,T); print(f"q={q} T={T}: simulated mse={m:.4f}  qT/2={q*T/2:.4f}")
def sim_cost(W,q,c=1.0):
    Ts=np.geomspace(0.05,20,60)*np.sqrt(2*c/(W*q))
    costs=[c/T+W*sim_mse(q,T,n_cycles=800,steps=60) for T in Ts]
    return min(costs)
base=sim_cost(1,1); print(f"\nmin simulated cost W=q=c=1: {base:.4f} vs sqrt(2)={np.sqrt(2):.4f}")
cW=sim_cost(4,1); cq=sim_cost(1,4)
print(f"stakes elasticity a ~ {np.log(cW/base)/np.log(4):.3f} (1/2);  drift elasticity b ~ {np.log(cq/base)/np.log(4):.3f} (1/2)")
