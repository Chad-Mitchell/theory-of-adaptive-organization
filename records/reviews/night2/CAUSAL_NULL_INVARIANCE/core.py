"""CAUSAL-NULL-INVARIANCE (pick 35) own code. Telegraph world +-mu, flip rate lam each way, white noise density N,
sampled every D (per-sample y = x + e, Var e = N/D; flips between samples with prob p=(1-exp(-2 lam D))/2).
Filter family F(pp, g): L <- log(((1-pp)e^L+pp)/(pp e^L+1-pp)) + g*y ; decision sign(L).
  Bayes (discrete Wonham): pp = p, g = 2 mu D / N.  Linear limit g -> 0: L ~ (1-2pp) L + g y, i.e. a linear filter with
  pole (1-2pp); the steady-state Kalman filter for the OU world with the same covariance has pole (1-K) phi, phi=exp(-2 lam D).
Stats from one long stationary record per path: t_A = D * mean #samples from the last pre-switch sample until sign(L)
first equals the new state ('switch' law: every switch of a stationary record); err = fraction of samples with wrong sign."""
import numpy as np, numba as nb, math

@nb.njit(cache=True)
def run(lam, mu, N, D, pp, g, nsamp, seed, lin):
    np.random.seed(seed)
    p = (1 - math.exp(-2 * lam * D)) / 2
    s = math.sqrt(N / D)
    x = 1.0 if np.random.random() < .5 else -1.0
    L = 0.0
    a = 1 - 2 * pp
    waiting = False; cnt = 0
    tot = 0.0; nsw = 0; tot2 = 0.0; nerr = 0
    burn = int(3.0 / (lam * D)) if lam * D > 0 else 0
    for k in range(nsamp + burn):
        if np.random.random() < p:
            x = -x
            if k > burn:
                if waiting:  # unfinished passage overtaken by a new switch: record censoring-free by dropping
                    pass
                waiting = True; cnt = 0
        y = x * mu + s * np.random.standard_normal()
        if lin:
            L = a * L + g * y
        else:
            Lc = min(max(L, -50.0), 50.0)
            eL = math.exp(Lc)
            L = math.log(((1 - pp) * eL + pp) / (pp * eL + 1 - pp)) + g * y
        if waiting:
            cnt += 1
            if L * x > 0:
                tot += cnt * D; tot2 += (cnt * D) ** 2; nsw += 1; waiting = False
        if k > burn and L * x <= 0:
            nerr += 1
    return tot, tot2, nsw, nerr / nsamp

def stats(lam, mu, N, D, pp, g, nsamp, seeds, lin=False):
    r = np.array([run(lam, mu, N, D, pp, g, nsamp, int(sd), lin) for sd in seeds])
    n = r[:, 2].sum(); m = r[:, 0].sum() / n; v = r[:, 1].sum() / n - m * m
    return dict(tA=m, se=math.sqrt(v / n), cv=math.sqrt(v) / m, nsw=int(n), err=r[:, 3].mean(),
                err_se=r[:, 3].std(ddof=1) / math.sqrt(len(seeds)))

def bayes_params(lam, mu, N, D):
    return (1 - math.exp(-2 * lam * D)) / 2, 2 * mu * D / N

def kalman_pole(lam, mu, N, D):
    phi = math.exp(-2 * lam * D); Qw = mu**2 * (1 - phi**2); R = N / D
    P = mu**2
    for _ in range(100000):
        Pm = phi**2 * P + Qw; K = Pm / (Pm + R); Pn = (1 - K) * Pm
        if abs(Pn - P) < 1e-15 * mu**2: break
        P = Pn
    return (1 - K) * phi, K

def tB_cont(lam, mu, N):
    k = lam * N / mu**2
    return N / (2 * mu**2) * (math.log(2 / k) - np.euler_gamma - 1)

def tL_mem(lam, mu, N):
    return 1 / math.sqrt(4 * lam**2 + 4 * lam * mu**2 / N)

@nb.njit(cache=True)
def run2(lam, mu, N, D, pp, g, nsamp, seed, lin):
    """As run(), plus least-squares sums for the estimate xhat = c*h, h = tanh(L/2) (nonlinear) or L (linear):
    returns (tA_sum, tA_sum2, nsw, err_rate, sum h*x, sum h*h, n)."""
    np.random.seed(seed)
    p = (1 - math.exp(-2 * lam * D)) / 2
    s = math.sqrt(N / D)
    x = 1.0 if np.random.random() < .5 else -1.0
    L = 0.0; a = 1 - 2 * pp
    waiting = False; cnt = 0
    tot = 0.0; nsw = 0; tot2 = 0.0; nerr = 0; shx = 0.0; shh = 0.0
    burn = int(3.0 / (lam * D))
    for k in range(nsamp + burn):
        if np.random.random() < p:
            x = -x
            if k > burn:
                waiting = True; cnt = 0
        y = x * mu + s * np.random.standard_normal()
        if lin:
            L = a * L + g * y
            h = L
        else:
            Lc = min(max(L, -50.0), 50.0); eL = math.exp(Lc)
            L = math.log(((1 - pp) * eL + pp) / (pp * eL + 1 - pp)) + g * y
            h = math.tanh(0.5 * L)
        if waiting:
            cnt += 1
            if L * x > 0:
                tot += cnt * D; tot2 += (cnt * D) ** 2; nsw += 1; waiting = False
        if k > burn:
            if L * x <= 0: nerr += 1
            shx += h * x * mu; shh += h * h
    return tot, tot2, nsw, nerr / nsamp, shx, shh, nsamp
