"""Monte Carlo check of the analytic error laws (stake E cos e and ruin tail) at fixed read times."""
import numpy as np, duel_core as d
rng = np.random.default_rng(7); n = 400000
def sample_density_from_c(c, n):
    # rejection sampling from p(phi) = |sum c_k e^{ik phi}|^2/(2pi); max <= N*sum c^2/(2pi)
    N = len(c); out = []
    while sum(len(o) for o in out) < n:
        x = rng.uniform(-np.pi, np.pi, 2*n); z = np.exp(1j*np.outer(x, np.arange(N)))@c
        acc = rng.uniform(0, N, 2*n) < np.abs(z)**2; out.append(x[acc])
    return np.concatenate(out)[:n]
def common_noise(t, s, k):
    z = rng.normal(0, np.sqrt(s*t), n) if s > 0 else np.zeros(n)
    if k is not None: z = z + rng.vonmises(0, k, n)
    return z
worst = 0
for (N, t, s, k, eps) in [(8, 3.0, 0.0, None, 0.01), (16, 0.6, 0.01, None, 0.01), (12, 0.5, 0.001, 100.0, 0.05), (32, 10.0, 0.001, None, 1e-3), (5, 0.9, 0.0, 100.0, 0.05)]:
    # b
    R, tl, c = d.best_state(N, eps, s*t, k)
    if c is not None:
        e = d.wrap(sample_density_from_c(c, n) + common_noise(t, s, k))
        an_s = R*d.noise_char(1, s*t, k); an_t = d.b_tail(c, s*t, k)
        print(f"b  N={N} t={t} s={s} k={k}: Ecos MC {np.cos(e).mean():.4f} an {an_s:.4f} | tail MC {np.mean(np.abs(e)>np.pi/2):.5f} an {an_t:.5f}")
        worst = max(worst, abs(np.cos(e).mean()-an_s))
    # a3 and a1 and a2
    rstar = 2*np.pi/np.sin(2*np.pi/N)
    for name, r, ticks in [('a3', rstar, False), ('a1', 0.0, False), ('a2', 0.0, True)]:
        u = rng.uniform(-np.pi/N, np.pi/N, n)
        if ticks:
            sh = d.tick_shift(N, t); e = d.wrap(u + sh + common_noise(t, s, k))
            an_s = d.a_char1(N, 0, t, shift=sh)*d.noise_char(1, s*t, k); an_t = d.a_tail_fourier(N, 0, t, s*t, k, shift=sh)
        else:
            K = rng.poisson(r*t, n); e = d.wrap(u + 2*np.pi*t - 2*np.pi*K/N + common_noise(t, s, k))
            an_s = d.a_char1(N, r, t)*d.noise_char(1, s*t, k); an_t = d.a_tail_fourier(N, r, t, s*t, k)
        print(f"{name} N={N} t={t} s={s} k={k}: Ecos MC {np.cos(e).mean():.4f} an {an_s:.4f} | tail MC {np.mean(np.abs(e)>np.pi/2):.5f} an {an_t:.5f}")
        worst = max(worst, abs(np.cos(e).mean()-an_s))
print("max |MC - analytic| E cos:", round(worst, 5), "(MC s.e. ~ 0.0015)")
