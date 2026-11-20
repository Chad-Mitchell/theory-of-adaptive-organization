"""Checks for THEORY v2.3: (1) self-similar temperature (CT18 general form, CT25 general), (2) share = elasticity for ANY
price-linear design problem (CT24 general), with a ruin-type constraint, and the scaling (virial) identity, (3) rule 4 archive
theorem (CT26), (4) rule 1/6 information-acquisition model (CT27). Run: nice -n 19 python3 rules_scaling_checks.py ; ends RESULT: PASS."""
import sys
import numpy as np
from scipy.optimize import minimize, brentq
from scipy.stats import norm, beta as betad
rng = np.random.default_rng(11)
bad = []
def chk(name, cond):
    if not cond: bad.append(name)

print("== 1. Self-similar temperature: per-window ruin P = F_H(B/(sigma tau^H)) exactly (self-similarity); sqrt = H=1/2")
def fbm_chol(H, N):
    t = np.arange(1, N+1)/N
    C = 0.5*(t[:, None]**(2*H) + t[None, :]**(2*H) - np.abs(t[:, None]-t[None, :])**(2*H))
    return np.linalg.cholesky(C + 1e-12*np.eye(N))
N, M = 256, 60000
res = {}
for H in (0.3, 0.5, 0.75):
    L = fbm_chol(H, N)
    Z = rng.standard_normal((M, N)) @ L.T          # fBm on [0,1] with unit variance at t=1
    smax = np.maximum(Z.max(1), 0)
    res[H] = smax
    for z in (1.0, 1.6):
        P = (smax >= z).mean()
        print(f"H={H}: P(sup over window >= z={z}) = {P:.4f}" + (f"  (closed form 2*Phibar = {2*norm.sf(z):.4f}, discretisation underestimates)" if H == 0.5 else ""))
# exact scaling: windows (sigma, tau) vs (sigma', tau') with the same B/(sigma tau^H) have the same P: by construction sup_[0,tau] sigma*B_H = sigma tau^H sup_[0,1]
# so the check is that z_eps(H) is a single number per H; report it and the implied buffer law B = z_eps sigma tau^H
for H in (0.3, 0.5, 0.75):
    z99 = np.quantile(res[H], 0.99)
    print(f"H={H}: z_eps (eps=1e-2, MC) = {z99:.3f}  ->  B >= z_eps*sigma*tau^H ; survivable shock ~ tau^(-{H}); elasticity eps_tau = H*eps_sigma - 1")
chk("H=0.5 z_eps within 8% of 2.576 (discretisation)", abs(np.quantile(res[0.5], 0.99)/2.5758 - 1) < 0.08)
# Elasticity check for H: hazard nu = F(z)/tau, z = B/(sigma tau^H); eps_tau = -1 - H*g, eps_sigma = -g with g = dlnF/dlnz
F = lambda z: np.exp(-z**2/2)                       # any smooth F will do for the identity
nu = lambda B, s, tau, H: F(B/(s*tau**H))/tau
for H in (0.3, 0.5, 0.75):
    B, s, tau = 3.0, 1.0, 2.0; h = 1e-6
    el = lambda i: (np.log(nu(*[v*(1+h) if k == i else v for k, v in enumerate((B, s, tau))], H)) - np.log(nu(*[v*(1-h) if k == i else v for k, v in enumerate((B, s, tau))], H)))/(np.log(1+h)-np.log(1-h))
    eB, eS, eT = el(0), el(1), el(2)
    chk(f"eps_B=-eps_sigma H={H}", abs(eB+eS) < 1e-6)
    chk(f"eps_tau=H*eps_sigma-1 H={H}", abs(eT-(H*eS-1)) < 1e-6)
print("elasticity identities eps_B=-eps_sigma, eps_tau=H*eps_sigma-1 verified for H=0.3,0.5,0.75")

print("\n== 2. Shares = elasticities for ANY price-linear problem J(x)=sum p_i phi_i(x), with a price-free constraint")
def run(seed):
    r = np.random.default_rng(seed); n, k = 3, 4
    A = r.uniform(0.5, 2, (k, n)); a = r.uniform(0.3, 2.5, (k, n)); s = r.choice([-1, 1], k)
    phi = lambda x, i: np.sum(A[i]*np.exp(s[i]*a[i]*x)) + 0.0 # convex positive terms exp(+-a.x)
    # make problem well posed: terms alternate growth/decay in a shared scalar direction
    def J(x, p): return sum(p[i]*np.sum(A[i]*np.exp(s[i]*a[i]*x)) for i in range(k))
    con = {'type': 'ineq', 'fun': lambda x: 5.0 - np.sum(x)}      # price-free constraint (e.g. survival exponent)
    def Jstar(p):
        best = None
        for x0 in (np.zeros(n), np.ones(n)*0.3):
            r_ = minimize(lambda x: J(x, p), x0, constraints=[con], method='SLSQP', options={'ftol': 1e-14, 'maxiter': 500})
            if best is None or r_.fun < best.fun: best = r_
        return best
    p = r.uniform(0.5, 2, k)
    b = Jstar(p); x = b.x
    shares = np.array([p[i]*np.sum(A[i]*np.exp(s[i]*a[i]*x)) for i in range(k)])/b.fun
    el = []
    for i in range(k):
        h = 1e-4; pp, pm = p.copy(), p.copy(); pp[i] *= 1+h; pm[i] *= 1-h
        el.append((np.log(Jstar(pp).fun) - np.log(Jstar(pm).fun))/(np.log(1+h)-np.log(1-h)))
    return shares, np.array(el)
for sd in (1, 2, 3):
    sh, el = run(sd)
    print(f"seed {sd}: shares {np.round(sh, 5)} elasticities {np.round(el, 5)} sum shares {sh.sum():.6f}")
    chk(f"shares=elasticities seed {sd}", np.max(np.abs(sh-el)) < 2e-4 and abs(sh.sum()-1) < 1e-9)
# scaling (virial) identity: if each term scales as x^{a_i} under one rescaling of the design, sum a_i s_i = 0 at an interior optimum
for al in (1.4, 2.0, 2.7):
    c, w, q = 3.0, 0.4, 1.7
    f = lambda lt: c*np.exp(-lt) + w*q*np.exp(lt*(al-1))/al
    from scipy.optimize import minimize_scalar
    r_ = minimize_scalar(f, bounds=(-20, 20), method='bounded', options={'xatol': 1e-12}); T = np.exp(r_.x)
    sh = np.array([c/T, w*q*T**(al-1)/al])/r_.fun; ex = np.array([-1.0, al-1])
    chk(f"virial a={al}", abs(sh@ex) < 1e-6)
print("virial identity sum_i a_i s_i = 0 verified for the single tracker; with 2 terms it pins s = (a2, -a1)/(a2-a1), with >2 terms it does not.")

print("\n== 3. Rule 4: keep the superseded version iff k < p*nu*(L_full - L_r), else never (bang-bang in the keep time)")
def Jkeep(t, k, p, nu, Lr, Lf):
    return k*(1-np.exp(-nu*t))/nu + p*(Lr*(1-np.exp(-nu*t)) + Lf*np.exp(-nu*t))
for (k, p, nu, Lr, Lf) in [(0.2, 0.1, 0.5, 1.0, 20.0), (1.0, 0.1, 0.5, 1.0, 20.0), (0.05, 0.3, 2.0, 0.5, 4.0), (0.5, 0.3, 2.0, 0.5, 4.0)]:
    ts = np.linspace(0, 60, 6001); v = Jkeep(ts, k, p, nu, Lr, Lf)
    rule = k < p*nu*(Lf-Lr)
    d = np.diff(v)    # J(t) is monotone in t: decreasing iff keeping longer pays
    print(f"k={k} p={p} nu={nu} dL={Lf-Lr}: J(0)={v[0]:.4f} J(inf)={v[-1]:.4f}; J decreasing in keep-time everywhere={bool(np.all(d <= 1e-12))}; rule says keep-until-proof={rule} (p*nu*dL={p*nu*(Lf-Lr):.3f})")
    chk(f"rule4 {k},{p}", (np.all(d <= 1e-12) and v[-1] < v[0]) == rule and (np.all(d >= -1e-12) and v[-1] >= v[0]) == (not rule))

print("\n== 4. Rules 1 and 6: outcome records as information acquisition (Beta-Bernoulli relevance, uniform prior)")
# item relevance r ~ U(0,1) unknown; return it iff posterior mean >= theta (= interrupt cost / stake); loss when wrong |r-theta|
theta = 0.4
def regret(n, theta=theta):
    tot = 0.0
    for s in range(n+1):
        pm = (s+1)/(n+2); a, b = s+1, n-s+1
        # integral over r of marginal prob of s successes (uniform prior): 1/(n+1) each; posterior is Beta(a,b)
        # expected loss given decision = integral |r-theta| over wrong side
        if pm >= theta:   # return: loss when r<theta : integral (theta-r) dBeta over r<theta
            from scipy.integrate import quad
            l = quad(lambda r: (theta-r)*betad.pdf(r, a, b), 0, theta)[0]
        else:             # not return: loss when r>theta
            from scipy.integrate import quad
            l = quad(lambda r: (r-theta)*betad.pdf(r, a, b), theta, 1)[0]
        tot += l/(n+1)
    return tot
R = np.array([regret(n) for n in range(0, 61)])
mv = R[:-1]-R[1:]                                   # marginal value of one more outcome record
print("regret R(n) at n=0,1,2,5,10,20,40,60:", np.round(R[[0, 1, 2, 5, 10, 20, 40, 60]], 5))
print("marginal value of the n-th record (n=0,1,2,5,10,20,40): ", np.round(mv[[0, 1, 2, 5, 10, 20, 40]], 6))
chk("regret nonincreasing in n", np.all(np.diff(R) <= 1e-12))
nstar = lambda price: int(np.argmin(R + price*np.arange(len(R))))   # records worth buying at a price per record
ps = [0.05, 0.02, 0.01, 0.005, 0.002, 0.001, 0.0002]
ns = [nstar(p) for p in ps]
print("records worth buying n*(price):", dict(zip(ps, ns)))
chk("n* nondecreasing as price falls", all(ns[i] <= ns[i+1] for i in range(len(ns)-1)))
chk("by-product records (price -> storage only) are worth keeping longer than bought ones", ns[-1] > ns[0])
# 'what the outcome would teach' in rule 1: extra value of a first interrupt = marginal value of a record when n is small
print("teaching value of the first record (n=0): ", round(mv[0], 5), " vs of the 20th:", round(mv[20], 6))
chk("teaching value falls with n (from n=5 on; the n=2 plateau is the decision not changing)", mv[0] > mv[5] > mv[20] > mv[40])
# Hebbian/ant form: EWMA of a Bernoulli use stream tracking a drifting relevance is the best LINEAR tracker (L1)
T_, rho = 4000, 0.02
r_true = np.empty(T_); r_true[0] = 0.5
for t in range(1, T_):
    r_true[t] = np.clip(r_true[t-1] + 0.01*rng.standard_normal(), 0.02, 0.98)
use = (rng.random(T_) < r_true).astype(float)
best_g, best_mse = None, 1e9
for g in (0.005, 0.01, 0.02, 0.05, 0.1, 0.3):
    e = 0.5; err = 0
    for t in range(T_):
        e = e + g*(use[t]-e)                          # reinforce on use, decay on disuse
        err += (e-r_true[t])**2
    mse = err/T_
    print(f"EWMA gain {g}: mse {mse:.5f}")
    if mse < best_mse: best_g, best_mse = g, mse
print("best gain", best_g, "(interior optimum: neither the slowest nor the fastest trace)")
chk("EWMA gain has an interior optimum", best_g not in (0.005, 0.3))

print("\n== 5. fBm collapse: windows with different (sigma, tau, B) but equal z = B/(sigma tau^H) have the same ruin probability")
def fbm_cov_chol(H, N, tau, sigma):
    t = np.arange(1, N+1)/N*tau
    C = 0.5*sigma**2*(t[:, None]**(2*H) + t[None, :]**(2*H) - np.abs(t[:, None]-t[None, :])**(2*H))
    return np.linalg.cholesky(C + 1e-12*sigma**2*tau**(2*H)*np.eye(N))
for H in (0.3, 0.75):
    out = []
    for (sg, tau) in ((1.0, 1.0), (2.5, 16.0), (0.4, 0.05)):
        B = 1.4*sg*tau**H
        Z = np.random.default_rng(5).standard_normal((30000, 160)) @ fbm_cov_chol(H, 160, tau, sg).T
        out.append((np.abs(Z).max(1) >= B).mean())
    print(f"H={H}: two-sided P(ruin in window) at z=1.4 for (sigma,tau)=(1,1),(2.5,16),(0.4,0.05): {np.round(out, 4)}")
    chk(f"fBm collapse H={H}", max(out)-min(out) < 0.012)

print("\n== 6. Nesting: pooled level = same J with stake W = sum w_i B_i^2; level-by-level solving vs the joint optimum")
from scipy.optimize import minimize_scalar as _ms
def Jstar(c, W, q, al):
    r = _ms(lambda lt: c/np.exp(lt) + W*q*np.exp(lt)**(al-1)/al, bounds=(-25, 25), method='bounded', options={'xatol': 1e-12})
    return r.fun, np.exp(r.x)
for al in (1.5, 2.0, 2.6):
    J1, T1 = Jstar(1.3, 0.8, 0.5, al)
    for n in (2, 5, 40):
        Jn, Tn = Jstar(1.3, n*0.8, 0.5, al)       # one pooled tracker of a common driver, stake n*w
        chk(f"closure J*(nW)=n^(1/al) J* al={al} n={n}", abs(Jn/(J1*n**(1/al)) - 1) < 1e-6)
        chk(f"pooling cost n^(a-1) al={al} n={n}", abs(Jn/(n*J1) - n**(1/al-1)) < 1e-6)
        chk(f"pooled read interval n^(-1/al) al={al} n={n}", abs(Tn/(T1*n**(-1/al)) - 1) < 1e-6)
print("closure: J*(nW) = n^(1/alpha) J*(W); pooled/separate = n^(a-1) with a = 1/alpha; pooled read interval shrinks as n^(-1/alpha)  (verified)")
# Level-by-level vs joint. Two layers (slow level, fast member). Additive coupling -> exactly separable.
# Product coupling: fast layer's error is multiplied by (1 + kappa*slow error): J = cf/Tf + cs/Ts + w*(qf*Tf/2)*(1 + kappa*qs*Ts/2) + w*qs*Ts/2
def Jjoint(Tf, Ts, k, p):
    cf, cs, w, qf, qs = p
    return cf/Tf + cs/Ts + w*(qf*Tf/2)*(1 + k*qs*Ts/2) + w*qs*Ts/2
P0 = (1.0, 1.0, 1.0, 1.0, 0.02)
def joint_opt(k, p=P0):
    r = minimize(lambda x: Jjoint(np.exp(x[0]), np.exp(x[1]), k, p), [0.0, 1.0], method='Nelder-Mead', options={'xatol': 1e-12, 'fatol': 1e-15, 'maxiter': 4000})
    return r.fun
def seq_opt(k, p=P0):       # slow level solved first ignoring feedback (k=0 form), then fast layer best-responds
    cf, cs, w, qf, qs = p
    Ts = np.sqrt(2*cs/(w*qs))                       # slow layer alone: min cs/Ts + w qs Ts/2
    Tf = np.sqrt(2*cf/(w*qf*(1 + k*qs*Ts/2)))        # fast layer given the slow one
    return Jjoint(Tf, Ts, k, p)
print("kappa, relative regret of level-by-level solving:")
ks = np.array([0.0, 0.05, 0.1, 0.2, 0.4, 0.8]); reg = []
for k in ks:
    jj = joint_opt(k); r_ = seq_opt(k)/jj - 1; reg.append(r_); print(f"  kappa={k}: {r_:.3e}")
reg = np.array(reg)
chk("kappa=0: level-by-level equals joint", abs(reg[0]) < 1e-9)
sl = np.polyfit(np.log(ks[1:4]), np.log(reg[1:4]), 1)[0]
print(f"log-log slope of the regret at small kappa: {sl:.2f} (second order: 2)")
chk("regret is second order in the feedback", abs(sl-2) < 0.15)
# additive coupling (inherited stake only) is exactly separable: joint = sequential with the pooled stake
def Jadd(Tf, Ts, k, p):
    cf, cs, w, qf, qs = p
    return cf/Tf + cs/Ts + w*qf*Tf/2 + w*k*qs*Ts/2 + w*qs*Ts/2
r = minimize(lambda x: Jadd(np.exp(x[0]), np.exp(x[1]), 0.7, P0), [0.0, 1.0], method='Nelder-Mead', options={'xatol': 1e-12, 'fatol': 1e-15, 'maxiter': 4000})
Ts = np.sqrt(2*P0[1]/(P0[2]*P0[4]*(1+0.7))); Tf = np.sqrt(2*P0[0]/(P0[2]*P0[3]))
chk("additive (stake-passing) coupling: sequential = joint", abs(Jadd(Tf, Ts, 0.7, P0)/r.fun - 1) < 1e-9)
print("stake-passing coupling (pooled stake, the case in the theory): sequential = joint exactly; feedback that changes a lower layer's own error: regret O(kappa^2)")

print("\n== 7. Compete, collaborate, organize: N parties free-riding on one shared driver (CX2 toy; alpha = 2, reads of total rate F)")
# Party i pays c*f_i and bears w_i*q/(2F) with F = sum f_j (a freshly read value helps everyone). Nash = each minimizes its own J_i.
def nash_cost(w, c=1.3, q=0.6):
    w = np.asarray(w, float); Fi = np.sqrt(w*q/(2*c)); F = Fi.max()
    return c*F + w.sum()*q/(2*F), F
def joint_cost(w, c=1.3, q=0.6):
    W = np.sum(w); F = np.sqrt(W*q/(2*c)); return c*F + W*q/(2*F), F
rng7 = np.random.default_rng(3)
for trial in range(6):
    n = rng7.integers(2, 7); w = rng7.uniform(0.2, 3, n)
    # brute-force Nash by iterating exact best responses one party at a time (sequential), from a random start
    c, q = 1.3, 0.6
    f = rng7.uniform(0, 1, n)
    for sweep in range(400):
        for i in range(n):
            others = f.sum()-f[i]; f[i] = max(0.0, np.sqrt(w[i]*q/(2*c)) - others)
    Jn = np.sum(c*f + w*q/(2*f.sum()))
    Jn_formula, Fn = nash_cost(w); Jj, Fj = joint_cost(w)
    a, W = w.max(), w.sum(); poa = Jn/Jj; poa_f = 0.5*(np.sqrt(a/W)+np.sqrt(W/a))
    print(f"n={n}: Nash total {Jn:.4f} (formula {Jn_formula:.4f}), joint {Jj:.4f}, price of anarchy {poa:.4f} = (1/2)(sqrt(a/W)+sqrt(W/a)) = {poa_f:.4f}")
    chk("Nash total matches formula", abs(Jn/Jn_formula-1) < 1e-9)
    chk("price of anarchy formula", abs(poa/poa_f-1) < 1e-9)
    chk("Nash never beats joint", Jn >= Jj-1e-12)
for N in (2, 4, 16, 100):
    w = np.ones(N); poa = nash_cost(w)[0]/joint_cost(w)[0]; chk(f"N equal parties PoA=(N+1)/(2 sqrt N), N={N}", abs(poa-(N+1)/(2*np.sqrt(N))) < 1e-9)
for N in (2, 4, 16, 100):
    w = np.ones(N); J1 = nash_cost(w[:1])[0]; Jn = nash_cost(w)[0]; Jj = joint_cost(w)[0]; Jsep = N*J1
    share = (Jsep-Jn)/(Jsep-Jj)
    chk(f"share of the pooling gain captured by free-riding = (sqrt N+1)/(2 sqrt N), N={N}", abs(share-(np.sqrt(N)+1)/(2*np.sqrt(N))) < 1e-9)
    chk(f"joint = n^(a-1) of separate, a=1/2, N={N}", abs(Jj/Jsep - N**(-0.5)) < 1e-9)
print("equal parties: separate trackers cost N*J1, free-riding (N+1)/2*J1, one pooled tracker sqrt(N)*J1; free-riding captures (sqrt N+1)/(2 sqrt N) of the pooling gain, tending to 1/2")
print("equal parties: price of anarchy = (N+1)/(2 sqrt N): 1.06 at N=2, 2.1 at N=16, 5.05 at N=100 (grows as sqrt(N)/2)")
# collaboration: cost shares proportional to stakes (Lindahl-type) implement the joint optimum
w = np.array([0.5, 1.0, 2.5]); c, q = 1.3, 0.6; sh = w/w.sum()
Fi = np.sqrt(w*q/(2*sh*c)); Fj = joint_cost(w)[1]
chk("cost shares proportional to stakes: every party's preferred total equals the joint optimum", np.allclose(Fi, Fj))
# a unilateral over-reader is not better off with equal cost shares: preferred totals differ, so the weaker party free-rides
Fe = np.sqrt(w*q/(2*(np.ones(3)/3)*c)); chk("equal shares misalign preferred totals", not np.allclose(Fe, Fe[0]))
print("cost shares proportional to stakes make every party want the joint total read rate (public-good pricing; needs the stakes to be revealed)")
# decentralized adaptation: damped simultaneous best response f <- f + lam*(BR(f) - f), N equal parties
def run_adapt(N, lam, steps=400):
    F1 = 1.0; f = np.zeros(N); f[0] = 0.3
    hist = []
    for t in range(steps):
        br = np.maximum(0.0, F1 - (f.sum()-f)); f = f + lam*(br-f); hist.append(f.sum())
    return np.array(hist)
for N in (2, 3, 5):
    for lam in (0.5/N, 1.9/N, 2.2/N):
        h_ = run_adapt(N, lam); tail = h_[-40:]; spread = tail.max()-tail.min()
        conv = spread < 1e-6 and abs(tail[-1]-1) < 1e-6
        print(f"N={N}, adaptation step lam={lam:.3f} (2/N={2/N:.3f}): total read rate -> {tail[-1]:.4f}, late spread {spread:.2e}, converged={conv}")
        chk(f"adaptation converges iff lam<2/N (N={N}, lam={lam:.3f})", conv == (lam < 2/N))
print("simultaneous adaptation settles at the Nash total iff the step is below 2/N of a full best response; above 2/N the total read rate does not settle (bounded oscillation here)")
if bad:
    print("FAIL", bad); sys.exit(1)
print("\nRESULT: PASS")
