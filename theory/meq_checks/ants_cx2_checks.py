"""Checks for THEORY v2.4: CT30 (the ant-trail update rule: optimal exponential smoothing = reinforce on use + evaporate at rate
lambda*, set by drift over noise, decentralizable), CT31 (CX2 classification: potential-game class, price of anarchy bound,
stake-proportional cost shares), CT32 (no general convergence theorem: counterexamples; time-scale separation changes which stationary point gradient play reaches, not shown to restore equilibrium).
Run: nice -n 19 python3 ants_cx2_checks.py ; prints the numbers, then ends with RESULT: PASS."""
import sys
import numpy as np
from scipy.optimize import minimize, minimize_scalar
rng = np.random.default_rng(2026)
bad = []
def chk(name, cond):
    if not bool(cond): bad.append(name); print("  ** FAIL:", name)

print("== 1a. Steady-state optimal tracker of a random walk seen through noise is exponential smoothing; gain lambda* from q/r")
def Kgain(q, r): rho = q/r; return (-rho + np.sqrt(rho**2 + 4*rho))/2
def V_ewma(lam, q, r): return ((1-lam)**2*q + lam**2*r)/(1-(1-lam)**2)       # stationary error variance of x <- (1-lam)x + lam*y
for (q, r) in [(0.01, 1.0), (0.5, 0.2), (3.0, 0.1), (1e-4, 2.0)]:
    # (i) Riccati iteration (Kalman filter) to steady state
    P = 1.0
    for _ in range(5000):
        Pp = P + q; K = Pp/(Pp + r); P = (1-K)*Pp
    # (ii) brute-force minimum over the smoothing gain
    res = minimize_scalar(lambda l: V_ewma(l, q, r), bounds=(1e-9, 1-1e-9), method='bounded', options={'xatol': 1e-12})
    print(f"q={q}, r={r}: Kalman gain {K:.8f}; closed form {Kgain(q, r):.8f}; best EWMA gain {res.x:.8f}; MSE {res.fun:.6f}")
    chk(f"Kalman gain = closed form q={q}", abs(K - Kgain(q, r)) < 1e-9)
    chk(f"best EWMA gain = Kalman gain q={q}", abs(res.x - K) < 1e-6)
    chk(f"EWMA MSE = the Kalman posterior variance q={q}", abs(res.fun - P) < 1e-9)
# continuous-time limit: evaporation rate gamma = sqrt(q/r), error sqrt(q r)
for dt in (1e-2, 1e-3, 1e-4):
    q, r = 0.7, 1.9; qd, rd = q*dt, r/dt                        # per-step variances for intensity q and noise intensity r
    lam = Kgain(qd, rd); print(f"dt={dt}: lambda/dt = {lam/dt:.5f} vs sqrt(q/r) = {np.sqrt(q/r):.5f}")
chk("evaporation rate -> sqrt(q/r) in continuous time", abs(Kgain(0.7e-4, 1.9e4)/1e-4/np.sqrt(0.7/1.9) - 1) < 2e-3)

print("\n== 1b. Evaporation rate from J: the price terms enter through the read noise r*, the loss weight w drops out at fixed r")
q, c, th = 0.4, 0.8, 1.0
for w in (0.5, 2.0, 8.0):
    Jr = lambda lr: w*np.sqrt(q*np.exp(lr)) + c*np.exp(lr)**(-th)       # J(r) = w*sqrt(q r) + c' r^(-theta): error plus the price of precision
    lr = minimize_scalar(Jr, bounds=(-15, 15), method='bounded', options={'xatol': 1e-12}).x; rs = np.exp(lr)
    r_formula = (2*th*c/(w*np.sqrt(q)))**(1/(th + 0.5))
    print(f"w={w}: r* = {rs:.5f} (formula {r_formula:.5f}); evaporation rate sqrt(q/r*) = {np.sqrt(q/rs):.5f}")
    chk(f"r* formula w={w}", abs(rs/r_formula - 1) < 1e-6)
for w in (0.5, 2.0, 8.0):   # at a FIXED sensing noise the argmin over the gain does not depend on w
    g = minimize_scalar(lambda l: w*V_ewma(l, 0.01, 1.0), bounds=(1e-9, 1-1e-9), method='bounded', options={'xatol': 1e-12}).x
    chk(f"gain independent of w at fixed noise w={w}", abs(g - Kgain(0.01, 1.0)) < 1e-6)
print("evaporation rate = sqrt(q/r); r itself is set by w, c', theta, q when precision is priced (CT15's form)")

print("\n== 1c. Reinforce-by-use + evaporate-at-lambda IS the smoothing update; decentralized trails reach the centralized optimum")
lam = 0.13
x = rng.random(50); use = (rng.random(50) < 0.4).astype(float)
chk("x <- (1-lam)x + lam*u equals x + (deposit lam*u) - (evaporation lam*x)", np.allclose((1-lam)*x + lam*use, x + lam*use - lam*x))
M, T = 12, 6000; q, r = 0.01, 0.5
S = np.cumsum(rng.normal(0, np.sqrt(q), (T, M)), 0) ; Y = S + rng.normal(0, np.sqrt(r), (T, M))
lam_s = Kgain(q, r)
X = np.zeros((T, M)); Xk = np.zeros((T, M)); P = np.eye(M)*1.0
F = np.eye(M); Qm = np.eye(M)*q; Rm = np.eye(M)*r; xk = np.zeros(M)
for t in range(T):
    # local rule: each trail sees only its own signal
    X[t] = ((1-lam_s)*(X[t-1] if t else 0) + lam_s*Y[t]) if t else lam_s*Y[t]
    # central joint Kalman filter over all trails
    xp = xk; Pp = P + Qm; Kk = Pp @ np.linalg.inv(Pp + Rm); xk = xp + Kk @ (Y[t] - xp); P = (np.eye(M) - Kk) @ Pp
    Xk[t] = xk
print(f"after burn-in, max |local EWMA - central Kalman| over {M} trails = {np.max(np.abs(X[500:] - Xk[500:])):.2e}")
chk("local updates equal the central Kalman filter for independent trails (steady state)", np.max(np.abs(X[2000:] - Xk[2000:])) < 1e-6)
mse_local = np.mean((X[500:] - S[500:])**2); print(f"MSE of local updates {mse_local:.5f}; theory V = {V_ewma(lam_s, q, r):.5f}")
chk("MSE matches the closed form (Monte Carlo, 5%)", abs(mse_local/V_ewma(lam_s, q, r) - 1) < 0.05)
# scope: with a driver shared across trails a joint (pooled) filter beats local smoothing, which is what a shared level buys (CT14)
qg, qu = 0.01, 0.0005; Mm = M
n_ = 1 + Mm; Fm = np.eye(n_); Qj = np.diag([qg] + [qu]*Mm); H = np.hstack([np.ones((Mm, 1)), np.eye(Mm)]); Rj = np.eye(Mm)*r
Pj = np.eye(n_)
for _ in range(3000):
    Pp = Pj + Qj; Kj = Pp @ H.T @ np.linalg.inv(H @ Pp @ H.T + Rj); Pj = (np.eye(n_) - Kj @ H) @ Pp
mse_pool = np.trace(H @ Pj @ H.T)/Mm                          # posterior error variance of the estimates of s_i = g + u_i
lam_l = Kgain(qg + qu, r); mse_loc = V_ewma(lam_l, qg + qu, r)
print(f"shared driver (q_g={qg}, q_u={qu}, r={r}, {Mm} trails): local smoothing MSE {mse_loc:.5f}; joint pooled filter MSE {mse_pool:.5f}")
chk("with a shared driver, pooling beats local smoothing", mse_pool < mse_loc)
print("so local updates are the optimum exactly when the trails drift independently; a shared driver is what a shared level (CT14) buys")

print("\n== 1d. When use is endogenous (choice follows the trail) the trail is no longer a relevance estimate")
def trail_run(k, xa0=0.5, xb0=0.5, T=20000, lam=0.05, rA=0.7, rB=0.3, seed=0):
    g = np.random.default_rng(seed); xa, xb = xa0, xb0; sa = []; sb = []; ch = []
    for t in range(T):
        pa = xa**k/(xa**k + xb**k + 1e-12) if k else 0.5; pick_a = g.random() < pa
        succ = g.random() < (rA if pick_a else rB)
        xa = (1-lam)*xa + lam*(1.0 if (pick_a and succ) else 0.0)
        xb = (1-lam)*xb + lam*(1.0 if ((not pick_a) and succ) else 0.0)
        sa.append(xa); sb.append(xb); ch.append(pick_a)
    h = T//2
    return np.mean(sa[h:]), np.mean(sb[h:]), np.mean(ch[h:])
ma, mb, pa = trail_run(0)
print(f"uniform choice (use exogenous): mean trail on A {ma:.3f} = (share {pa:.2f}) x (relevance 0.7); on B {mb:.3f} = 0.5 x 0.3")
chk("trail on a path = choice share x relevance, not the relevance", abs(ma - pa*0.7) < 0.03 and abs(mb - (1-pa)*0.3) < 0.03)
lock_worse = 0; R_ = 20
for sd in range(R_):
    ma, mb, pa = trail_run(2, xa0=0.1, xb0=0.5, T=6000, seed=sd + 1)
    lock_worse += (pa < 0.2)
print(f"positive feedback (choice probability proportional to trail squared), A is the better path (0.7 vs 0.3) but starts with the weaker trail: locked on the worse path in {lock_worse} of {R_} runs")
chk("endogenous use can lock the trail on the worse path", lock_worse >= 1)

print("\n== 2a. Free-riding on a shared driver is a weighted exact potential game (weights w_i), Nash = argmin of the potential")
def Ji(f, i, c, w, q):  F = f.sum(); return c[i]*f[i] + w[i]*q/(2*F)
def Phi(f, c, w, q):    return np.sum(c*f/w) + q/(2*f.sum())
worst = 0
for trial in range(2000):
    n = rng.integers(2, 6); w = rng.uniform(0.2, 3, n); c = rng.uniform(0.5, 2, n); q = rng.uniform(0.2, 1.5)
    f = rng.uniform(0.1, 2, n); i = rng.integers(n); f2 = f.copy(); f2[i] = rng.uniform(0.1, 2)
    worst = max(worst, abs((Ji(f2, i, c, w, q) - Ji(f, i, c, w, q)) - w[i]*(Phi(f2, c, w, q) - Phi(f, c, w, q))))
print(f"max |ΔJ_i − w_i·ΔΦ| over 2000 random unilateral deviations (heterogeneous read prices): {worst:.2e}")
chk("weighted exact potential identity", worst < 1e-12)
n = 4; w = np.array([0.6, 1.4, 2.2, 0.9]); c = np.ones(n)*1.3; q = 0.6
# minimize Phi over f >= 0 by multi-start
best = None
for s in range(30):
    r0 = minimize(lambda z: Phi(np.exp(z), c, w, q), rng.normal(0, 1, n), method='Nelder-Mead', options={'xatol': 1e-12, 'fatol': 1e-14, 'maxiter': 20000})
    if best is None or r0.fun < best.fun: best = r0
fstar = np.exp(best.x); Fa = np.sqrt(w.max()*q/(2*c[0])); print(f"argmin Phi: total reads {fstar.sum():.4f} (Nash formula {Fa:.4f}); largest-stake party reads {fstar[np.argmax(w)]/fstar.sum():.3f} of it")
chk("argmin of the potential has the Nash total reads", abs(fstar.sum()/Fa - 1) < 5e-3)
# sequential best response decreases the potential monotonically and converges
f = rng.uniform(0.1, 1, n); phis = [Phi(f, c, w, q)]
for sweep in range(60):
    for i in range(n):
        f[i] = max(1e-12, np.sqrt(w[i]*q/(2*c[i])) - (f.sum() - f[i])); phis.append(Phi(f, c, w, q))
chk("sequential best response: potential nonincreasing", np.all(np.diff(phis) <= 1e-12))
chk("sequential best response converges to the Nash total", abs(f.sum()/Fa - 1) < 1e-6)

print("\n== 2b. Price of anarchy bound in the toy class: PoA = (1/2)(sqrt(x)+1/sqrt(x)) with x = W/a in [1, N]; so PoA <= (N+1)/(2 sqrt N), tight at equal stakes")
def poa(w, c=1.3, q=0.6):
    W, a = w.sum(), w.max(); Jn = 0.5*np.sqrt(2*c*q)*(np.sqrt(a) + W/np.sqrt(a)); Jj = np.sqrt(2*c*q*W); return Jn/Jj
mx = {}
for trial in range(4000):
    n = rng.integers(2, 9); w = rng.exponential(1.0, n)**rng.uniform(0.5, 3)
    p = poa(w); mx[n] = max(mx.get(n, 0), p); chk("PoA <= (N+1)/(2 sqrt N)", p <= (n+1)/(2*np.sqrt(n)) + 1e-12)
for n in (2, 4, 8): chk(f"bound tight at equal stakes N={n}", abs(poa(np.ones(n)) - (n+1)/(2*np.sqrt(n))) < 1e-12)
print("largest PoA seen at random stakes, by N:", {int(k): round(float(v), 4) for k, v in sorted(mx.items())}, " bound:", {n: round((n+1)/(2*np.sqrt(n)), 4) for n in (2, 4, 8)})
print("N-independent bound: none (the PoA grows as sqrt(N)/2 for equal parties)")

print("\n== 2c. Stake-proportional cost shares make every party's cost proportional to the joint cost: Nash = joint optimum (Groves/Lindahl-type alignment)")
worst = 0
for trial in range(500):
    n = rng.integers(2, 7); w = rng.uniform(0.2, 3, n); c = rng.uniform(0.5, 2); q = rng.uniform(0.2, 1.5); W = w.sum()
    f = rng.uniform(0.1, 2, n); F = f.sum(); Jjoint = c*F + W*q/(2*F)
    for i in range(n):
        Ji_share = (w[i]/W)*c*F + w[i]*q/(2*F)        # i pays the share w_i/W of all reads
        worst = max(worst, abs(Ji_share - (w[i]/W)*Jjoint))
chk("each party's cost = (w_i/W) x joint cost under stake-proportional shares", worst < 1e-12)
print(f"max identity error {worst:.2e}; every best response minimizes the joint cost, so Nash total reads = sqrt(Wq/2c) = the joint optimum; potential = joint cost (exact potential game)")

print("\n== 2d. No general convergence theorem: counterexamples")
# (i) zero-sum bilinear coupling J1 = x1*x2, J2 = -x1*x2 (pursuit and evasion): continuous-time gradient adaptation conserves x1^2+x2^2
x = np.array([1.0, 0.0]); h = 1e-3; r0 = x@x
for _ in range(200000):
    k1 = np.array([-x[1], x[0]]); k2 = np.array([-(x+h/2*k1)[1], (x+h/2*k1)[0]]); k3 = np.array([-(x+h/2*k2)[1], (x+h/2*k2)[0]]); k4 = np.array([-(x+h*k3)[1], (x+h*k3)[0]])
    x = x + h/6*(k1 + 2*k2 + 2*k3 + k4)
print(f"zero-sum bilinear coupling, continuous-time gradient adaptation: x1^2+x2^2 from {r0:.6f} to {x@x:.6f} after 200 time units (never converges)")
chk("the orbit is a closed cycle (radius conserved)", abs(x@x - r0) < 1e-6 and abs(np.linalg.norm(x) - 1) < 1e-6)
x = np.array([1.0, 0.0]); eta = 0.1
for t in range(300): x = x + eta*np.array([-x[1], x[0]])        # simultaneous gradient steps
print(f"same coupling, discrete simultaneous gradient steps (eta = 0.1): radius after 300 steps = {np.linalg.norm(x):.3f} (grows as (1+eta^2)^(t/2) = {(1+eta**2)**150:.3f})")
chk("discrete simultaneous steps spiral outward", np.linalg.norm(x) > 4)
# (ii) Shapley (1964)-type 3x3 game: fictitious play (best responses to the opponent's history) cycles
A = np.array([[0, 2, 1], [1, 0, 2], [2, 1, 0]], float)   # row player's payoffs (rows a,b,c; columns A,B,C) from the table in the literature
B = np.array([[0, 1, 2], [2, 0, 1], [1, 2, 0]], float)   # column player's payoffs
cnt_r = np.array([0.0, 0, 0]); cnt_c = np.array([0.0, 0, 0]); cnt_r[0] = 1; cnt_c[1] = 1    # start at (a, B)
traj = []
for t in range(1, 200000):
    rr = np.argmax(A @ (cnt_c/cnt_c.sum())); cc = np.argmax((cnt_r/cnt_r.sum()) @ B)
    cnt_r[rr] += 1; cnt_c[cc] += 1
    if t % 1000 == 0: traj.append(np.linalg.norm(cnt_r/cnt_r.sum() - 1/3) + np.linalg.norm(cnt_c/cnt_c.sum() - 1/3))
traj = np.array(traj)
print(f"Shapley-type game: distance of empirical play from the mixed Nash (1/3,1/3,1/3), sampled every 1000 steps: first {traj[0]:.3f}, min over the last half {traj[len(traj)//2:].min():.3f}, max over the last half {traj[len(traj)//2:].max():.3f}")
chk("fictitious play in the Shapley-type game does not converge to the mixed Nash", traj[len(traj)//2:].min() > 0.2)
# (iii) time-scale separation changes the stability of gradient play (linear two-player model; its rest point is NOT a Nash equilibrium of the slow party, whose own cost is concave: see scope_checks.py sec. 9: J1 = x1*x2 - (m/2) x1^2 [anti-damped], J2 = -x1*x2 + (b/2) x2^2)
m, b = 1.0, 0.5            # m*b < 1 so the fast player's reduced game is stable
for eps in (2.0, 1.0, 0.6, 0.3, 0.1, 0.02):
    Jac = np.array([[eps*m, -eps], [1.0, -b]])    # xdot1 = -eps*dJ1/dx1 = -eps*(x2 - m x1) ; xdot2 = -dJ2/dx2 = x1 - b x2
    ev = np.linalg.eigvals(Jac); stable = np.all(ev.real < 0)
    print(f"slow player's adaptation speed eps={eps}: eigenvalues real parts {np.round(ev.real, 3)}  -> {'converges' if stable else 'cycles outward'}")
    chk(f"stable iff eps < b/m (eps={eps})", stable == (eps < b/m))
print("proof: trace = eps*m - b, det = eps*(1 - m*b); with m*b < 1 the determinant is positive, so the system is stable iff eps < b/m, i.e. the slow player must be slower than the fast one's damping rate.  CAUTION (review 24 B2): J1 is concave in x1 (m > 0), so the rest point reached is a stationary point of gradient play, not a Nash equilibrium; with convex own costs the speed ratio never changes stability (scope_checks.py sec. 9)")
if bad:
    print("FAIL", bad); sys.exit(1)
print("\nRESULT: PASS")
