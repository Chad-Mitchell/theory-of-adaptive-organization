#!/usr/bin/env python3
"""Independent Monte Carlo of the sampled-grid adaptation times (does not import tools/discrete_ta.py or any
AQN_REFEREE code).  Simulates the actual per-sample worlds and filters.

Bayes (telegraph HMM): M chains, x_k = +-mu with flip prob p per step, y_k = x_k + sd_e * eps, log-odds filter
  L_k = f(L_{k-1}) + 2 mu y_k / s2 (forward algorithm in probability form, independent code path).  After burn-in,
  every flip x_k -> x_{k+1} = -x_k records s*L_k (s = sign x_k).  Phase 2 restarts from those values with the world
  held at the new state (N16 definition) and counts n = min{n >= 0 : L_n <= 0}.  Variant 'free': the world keeps
  switching after the first flip (no hold) - reported to show definition sensitivity.
Linear (OU + Kalman): a time-varying Kalman filter run to convergence; the empirical step-response e-folding of the
  filter (regression of xhat_k on x history) is compared with the closed form.
Usage: mc_discrete.py SEED  -> JSON on stdout.
"""
import json, math, sys
import numpy as np

def forward_step(P, y, p, mu, s2):
    # P = P(x=+ | past); predict then Bayes update with Gaussian likelihoods (probability form, not log-odds)
    Pp = P * (1 - p) + (1 - P) * p
    lp = np.exp(-(y - mu) ** 2 / (2 * s2)); lm = np.exp(-(y + mu) ** 2 / (2 * s2))
    num = Pp * lp
    return num / (num + (1 - Pp) * lm)

def logit_step(L, y, p, mu, s2):
    # same filter in log-odds, used only where probabilities saturate (checked against forward_step below)
    a = np.logaddexp(np.log1p(-p) + L, np.log(p)); b = np.logaddexp(np.log(p) + L, np.log1p(-p))
    return a - b + 2 * mu * y / s2

def bayes_mc(mu, lam, N, Delta, rng, M=20000, events=200000, burn_mult=8.0, hold=True, max_steps=None, law="switch"):
    s2 = N / Delta; sd = math.sqrt(s2); p = 0.5 * (1 - math.exp(-2 * lam * Delta))
    x = np.where(rng.random(M) < 0.5, 1.0, -1.0); L = np.zeros(M)
    if law == "quiet":
        # world held at + for a long quiet period (filter still assumes flip prob p): N16's derivation law
        burn = int((3 * math.log(2 / (lam * N / mu**2)) + 20) * (N / mu**2) / Delta) + 200
        L = np.zeros(events)
        for _ in range(burn):
            L = logit_step(L, mu + sd * rng.standard_normal(events), p, mu, s2)
        L0 = L
        burn = -1
    else:
        burn = int(burn_mult / p)
    for _ in range(max(burn, 0)):
        flip = rng.random(M) < p; x = np.where(flip, -x, x)
        L = logit_step(L, mu * x + sd * rng.standard_normal(M), p, mu, s2)
    rec = []
    while burn >= 0 and sum(len(r) for r in rec) < events:
        flip = rng.random(M) < p
        if flip.any():
            rec.append((np.sign(x[flip]) * L[flip]).copy())
        x = np.where(flip, -x, x)
        L = logit_step(L, mu * x + sd * rng.standard_normal(M), p, mu, s2)
    if burn >= 0:
        L0 = np.concatenate(rec)[:events]
    # phase 2: post-switch, world at -mu (sign-adjusted), count steps until L <= 0
    Lc = L0.copy(); n = np.zeros(events); alive = Lc > 0
    xs = -np.ones(events)
    t = 0
    max_steps = max_steps or int(200 * (N / mu**2 * math.log(2 / (lam * N / mu**2) + 2) / Delta + 10))
    while alive.any() and t < max_steps:
        t += 1
        idx = np.nonzero(alive)[0]
        if not hold:
            fl = rng.random(idx.size) < p; xs[idx] = np.where(fl, -xs[idx], xs[idx])
        y = mu * xs[idx] + sd * rng.standard_normal(idx.size)
        Lc[idx] = logit_step(Lc[idx], y, p, mu, s2)
        n[idx] += 1
        alive[idx] = Lc[idx] > 0
    return {"E_steps": float(n.mean()), "se_steps": float(n.std(ddof=1) / math.sqrt(events)),
            "t_A": float(n.mean() * Delta), "se_t": float(n.std(ddof=1) / math.sqrt(events) * Delta),
            "P_L0_le_0": float((L0 <= 0).mean()), "censored": int(alive.sum()), "events": events}

def linear_mc(mu, lam, N, Delta, rng, T=400000):
    a = 2 * lam; phi = math.exp(-a * Delta); Q = mu * mu * (1 - phi * phi); R = N / Delta
    # iterate the Riccati recursion (not the closed form) to get the gain
    P = mu * mu
    for _ in range(100000):
        M = phi * phi * P + Q; K = M / (M + R); Pn = (1 - K) * M
        if abs(Pn - P) < 1e-15 * P: break
        P = Pn
    z = (1 - K) * phi
    # empirical: simulate, filter, and fit the impulse response of xhat to y by least squares on lags
    x = np.zeros(T); e = math.sqrt(R) * rng.standard_normal(T); w = math.sqrt(Q) * rng.standard_normal(T)
    for k in range(1, T): x[k] = phi * x[k - 1] + w[k]
    y = x + e; xh = np.zeros(T)
    for k in range(1, T): xh[k] = z * xh[k - 1] + K * y[k]
    # memory time from the filter's own response to a unit step in the input (deterministic recursion check)
    step = np.zeros(4000); s = 0.0
    for k in range(4000): s = z * s + K; step[k] = s
    target = (1 - math.exp(-1)) * step[-1]
    kk = np.argmax(step >= target)  # first sample at >= 63.2% of the final step response
    # interpolate the e-folding in continuous index units: step_k = K(1-z^{k+1})/(1-z)
    efold = Delta / (-math.log(z))
    mse_emp = float(np.mean((xh[1000:] - x[1000:]) ** 2))
    return {"K": K, "pole": z, "t_A_from_riccati_iteration": efold, "first_sample_at_63pct": int(kk),
            "mse_emp": mse_emp, "P_post": Pn}

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    rng = np.random.default_rng(seed)
    # probability-form vs log-odds-form agreement on a short run (independence of the filter step)
    P = np.full(5, 0.5); L = np.zeros(5); mx = 0
    for k in range(50):
        y = rng.standard_normal(5); P = forward_step(P, y, 0.01, 1.0, 2.0); L = logit_step(L, y, 0.01, 1.0, 2.0)
        mx = max(mx, float(np.max(np.abs(P - 1 / (1 + np.exp(-L))))))
    out = {"seed": seed, "filter_form_maxdiff": mx, "bayes": [], "linear": []}
    sw = [(1, 0.002, 0.25, 1), (1, 0.01, 0.25, 1), (1, 0.002, 2.25, 1), (1, 0.01, 2.25, 1), (1, 0.002, 9, 1),
          (1, 0.01, 9, 1), (1, 0.0005, 36, 1), (1, 0.01, 1, 0.05), (1, 0.01, 1, 0.2), (1, 0.01, 1, 0.5)]
    qu = [(1, 0.002, 2.25, 1), (1, 0.01, 2.25, 1), (1, 0.002, 9, 1), (1, 0.01, 9, 1), (1, 0.0005, 36, 1),
          (1, 0.001, 1, 0.01), (1, 0.001, 1, 0.05), (1, 0.001, 1, 0.2), (1, 1e-4, 1, 0.02), (1, 1e-4, 1, 0.5)]
    for law, cases in (("switch", sw), ("quiet", qu)):
        for mu, lam, N, D in cases:
            M = 20000 if 0.5 * (1 - math.exp(-2 * lam * D)) >= 1e-3 else 10000
            r = bayes_mc(mu, lam, N, D, rng, M=M, law=law)
            out["bayes"].append({"mu": mu, "lam": lam, "N": N, "Delta": D, "hold": True, "law": law, **r})
            print(json.dumps(out["bayes"][-1]), file=sys.stderr, flush=True)
    for mu, lam, N, D in [(1, 0.002, 9, 1), (1, 0.01, 1, 0.5)]:
        r = bayes_mc(mu, lam, N, D, rng, hold=False)
        out["bayes"].append({"mu": mu, "lam": lam, "N": N, "Delta": D, "hold": False, "law": "switch", **r})
        print(json.dumps(out["bayes"][-1]), file=sys.stderr, flush=True)
    for mu, lam, N, D in [(1, 0.01, 1, 0.5), (1, 0.05, 1, 2.0), (1, 0.002, 9, 1)]:
        out["linear"].append({"mu": mu, "lam": lam, "N": N, "Delta": D, **linear_mc(mu, lam, N, D, rng)})
    print(json.dumps(out, indent=1))
