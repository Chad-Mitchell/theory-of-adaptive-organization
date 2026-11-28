#!/usr/bin/env python3
"""Independent numerical check of a = b = 1/(1+2H) for hold-last-value
refresh of fBm under upkeep + squared-error cost.

Method:
  1. Generate fBm paths by Davies-Harte circulant embedding of fGn.
  2. For integer intervals T, estimate mean squared hold-last-value error.
  3. Confirm MSE ≈ T^{2H}/(1+2H) (continuous-time exact mean, discrete sum bias noted).
  4. For a log-grid of stakes W (c=1, q=1), minimize J(T)=c/T + W*MSE(T); fit
     log(effort=1/T*) vs log W to get â.
  5. Equivalently scale path variance by q and fit ˆb vs log q at fixed W.
  6. Also report the exact (non-simulated) elasticities from minimizing the
     closed-form J, as a sanity check that the claim is the EOQ calculus result.

Usage: nice -n 19 python3 fbm_exponent.py
"""
import numpy as np
from numpy.linalg import LinAlgError

# ---------------- fBm generation (Davies-Harte) ----------------

def fgn_acf(k, H):
    k = np.asarray(k, dtype=float)
    return 0.5 * (np.abs(k + 1) ** (2 * H) + np.abs(k - 1) ** (2 * H) - 2 * np.abs(k) ** (2 * H))


def davies_harte_fgn(n, H, rng):
    """n standard fGn samples, covariance γ(k)=0.5(|k+1|^{2H}+|k-1|^{2H}-2|k|^{2H})."""
    # Expand until eigenvalues are non-negative (Dietrich & Newsam).
    m = 1 << int(np.ceil(np.log2(max(n, 2))))
    for _ in range(6):
        k = np.arange(0, m + 1)
        c = fgn_acf(k, H)
        # circulant first row of length 2m: c0..c_{m-1}, c_m, c_{m-1}..c1
        first = np.concatenate([c[:-1], c[:0:-1]])
        lam = np.real(np.fft.fft(first))
        if np.min(lam) > -1e-12:
            lam = np.maximum(lam, 0.0)
            break
        m *= 2
    else:
        raise RuntimeError(f"Davies-Harte eigenvalues negative for H={H}, n={n}")
    # Complex white noise with correct reality constraints
    ncirc = 2 * m
    z = rng.normal(size=ncirc) + 1j * rng.normal(size=ncirc)
    z[0] = np.sqrt(2) * rng.normal()  # real
    z[m] = np.sqrt(2) * rng.normal()  # Nyquist, real
    # conjugate symmetry so the IFFT is real
    z[ncirc // 2 + 1 :] = np.conj(z[1:ncirc // 2][::-1])
    # scale: Var = (1/ncirc) * sum lam * E|z|^2 / 2 ... standard is
    # W = IFFT(sqrt(lam) * Z) with Z_0, Z_m real N(0,1) and others CN(0,1)
    # and we need Var(fGn)=γ(0)=1, which is (1/ncirc) sum lam = c0 = 1.
    # For complex Z with E|Z|^2=2 for off-zero (independent real/imag N(0,1)),
    # IFFT convention: numpy ifft divides by n, so
    # E|ifft(sqrt(lam) Z)|^2 = (1/n^2) * n * 2 * lam_mean * n/2 ... careful.
    # Standard formula used in literature with numpy:
    #   w = np.fft.ifft(np.sqrt(lam) * z) * np.sqrt(ncirc)
    # and take real part of first n samples; with z as above (E|z_j|^2=2 except ends=1)
    # a cleaner construction:
    sqrt_lam = np.sqrt(lam / ncirc)
    x = np.fft.ifft(sqrt_lam * z) * ncirc  # ifft already /ncirc, multiply back
    # With this, Var(x) = sum (lam/ncirc) * E|z|^2 ... messy.
    # Use the well-tested construction from Wood & Chan / Dietrich-Newsam:
    # I'll instead use the real-even construction below and empirically
    # renormalize to unit fGn variance, then report the renormalization.
    fgn = np.real(x[:n])
    s = np.std(fgn, ddof=1)
    return fgn / s, s


def davies_harte_fgn_v2(n, H, rng):
    """Standard real-valued Davies-Harte (Craigmile / Dietrich-Newsam form)."""
    m = 1 << int(np.ceil(np.log2(max(n, 2))))
    for _ in range(6):
        k = np.arange(0, m)
        r = fgn_acf(k, H)
        # first row of 2m circulant: r[0..m-1], 0? actually
        # γ(0), γ(1), ..., γ(m-1), γ(m), γ(m-1), ..., γ(1)
        # γ(m) = fgn_acf(m, H)
        mid = fgn_acf(m, H)
        first = np.concatenate([r, [mid], r[1:][::-1]])
        lam = np.real(np.fft.fft(first))
        if np.min(lam) >= -1e-10:
            lam = np.maximum(lam, 0.0)
            break
        m *= 2
    else:
        raise RuntimeError(f"negative eigenvalues H={H} n={n}")
    ncirc = 2 * m
    # Independent N(0,1) for real and imag; IFFT
    # Construction: W_k = sqrt(lam_k / (2 ncirc)) * (Z1 + i Z2) for k=1..ncirc-1,
    # W_0 = sqrt(lam_0 / ncirc) * Z0, W_{ncirc/2} similarly.
    z1 = rng.normal(size=ncirc)
    z2 = rng.normal(size=ncirc)
    W = np.empty(ncirc, dtype=complex)
    W[0] = np.sqrt(lam[0] / ncirc) * z1[0]
    W[m] = np.sqrt(lam[m] / ncirc) * z1[m]
    scale = np.sqrt(lam[1:m] / (2 * ncirc))
    W[1:m] = scale * (z1[1:m] + 1j * z2[1:m])
    W[m + 1 :] = np.conj(W[1:m][::-1])
    x = np.real(np.fft.fft(W))  # fft of Hermitian is real; numpy fft no 1/n
    # With W already scaled by 1/sqrt(ncirc), fft gives sum, so *no* extra factor?
    # E|fft(W)_t|^2 = ncirc * E|W|^2 * ncirc? 
    # fft(W)_t = sum_k W_k exp(...); Var = sum_k E|W_k|^2 * ncirc? No:
    # Var(sum W_k ω^{kt}) = sum E|W_k|^2  (orthogonal).
    # E|W_0|^2 = lam[0]/ncirc, E|W_k|^2 = lam[k]/(2 ncirc)*2 = lam[k]/ncirc for k=1..m-1
    # so Var = sum_k lam[k]/ncirc = (1/ncirc) * (ncirc * c0) = c0 = 1, if we used IFFT?
    # Wait: fft vs ifft. numpy fft is sum, ifft is (1/n) sum.
    # I used fft. Then Var = sum E|W|^2 = 1. Good — use fft (not ifft) with this scaling.
    return x[:n]


def fbm_paths(n, H, npaths, rng):
    """Return array (npaths, n+1) of fBm starting at 0, unit fGn variance."""
    out = np.zeros((npaths, n + 1))
    for i in range(npaths):
        inc = davies_harte_fgn_v2(n, H, rng)
        out[i, 1:] = np.cumsum(inc)
    return out


def hold_mse(paths, T):
    """Mean squared zero-order-hold error for integer interval T.
    paths: (npaths, N+1) values at times 0..N.
    Error at t is (X(t)-X(t-t%T))^2; include all t=1..N with a defined hold
    (t may extend past last exact multiple). Average over time and paths.
    """
    N = paths.shape[1] - 1
    if T < 1:
        raise ValueError(T)
    # hold index: last multiple of T at or before t
    t = np.arange(N + 1)
    hold_idx = (t // T) * T
    err2 = (paths - paths[:, hold_idx]) ** 2
    # exclude t=0 (err 0) and, optionally, times after last full interval
    n_full = (N // T) * T
    if n_full < T:
        return np.mean(err2[:, 1:])
    return np.mean(err2[:, 1 : n_full + 1])


def analytic_mse_continuous(T, H, q=1.0):
    return q * (T ** (2 * H)) / (1 + 2 * H)


def analytic_mse_discrete(T, H, q=1.0):
    """Average of k^{2H} for k=1..T-1 plus 0 at k=0, over T instants in the cycle.
    At the right endpoint t=T the error resets, so average over t=0,1,...,T-1
    is (1/T) sum_{k=0}^{T-1} q k^{2H}.
    """
    k = np.arange(T, dtype=float)
    return q * np.mean(k ** (2 * H))


def main():
    rng = np.random.default_rng(20261115)
    Hs = [0.20, 0.35, 0.50, 0.70, 0.85]
    n = 2 ** 14          # 16384 steps per path
    npaths = 48
    c = 1.0
    print(f"fBm hold-last-value exponent check  n={n}  npaths={npaths}  seed=20261115")
    print()

    # --- variance sanity of generated fBm ---
    print("== path variance vs t^{2H} (mean over paths, t=n//4, n//2, n) ==")
    all_mse = {}
    Ts = np.unique(np.concatenate([
        np.arange(1, 32),
        np.unique(np.geomspace(32, n // 8, 40).astype(int)),
    ]))
    for H in Hs:
        paths = fbm_paths(n, H, npaths, rng)
        for t in (n // 4, n // 2, n):
            v = np.mean(paths[:, t] ** 2)
            pred = t ** (2 * H)
            print(f"  H={H:.2f} t={t:5d}  emp Var={v:.4g}  t^{{2H}}={pred:.4g}  ratio={v/pred:.3f}")
        # MSE(T)
        mses = np.array([hold_mse(paths, int(T)) for T in Ts])
        all_mse[H] = (Ts, mses)
        # compare a few T
        print(f"  MSE(T) vs continuous T^{{2H}}/(1+2H) and discrete mean k^{{2H}}:")
        for T in (2, 4, 8, 16, 32, 64, 128, 256):
            if T not in Ts:
                continue
            emp = mses[np.where(Ts == T)[0][0]]
            ac = analytic_mse_continuous(T, H)
            ad = analytic_mse_discrete(T, H)
            print(f"    T={T:4d}  emp={emp:.5g}  cont={ac:.5g} (ratio {emp/ac:.3f})  disc={ad:.5g} (ratio {emp/ad:.3f})")
        print()

    # --- optimize T* and fit exponents ---
    # Choose W grid so T* sits well inside [2, n/16] using continuous formula
    # T* = [c(1+2H)/(W*2H)]^{1/(1+2H)}
    print("== fitted elasticities from simulated MSE(T) ==")
    print(f"{'H':>6} {'theory a':>10} {'â (vs W)':>10} {'ˆb (vs q)':>10} {'nW':>5} {'T* range':>18} {'R^2_a':>8}")
    results = []
    for H in Hs:
        Ts, mses = all_mse[H]
        # theoretical T* at a reference W to center the grid
        a_th = 1.0 / (1.0 + 2.0 * H)
        # W such that T*_cont in [8, n/16]
        Tlo, Thi = 8.0, n / 16.0
        def W_of_T(T):
            return c * (1 + 2 * H) / (2 * H) / (T ** (1 + 2 * H))
        Wmin, Wmax = W_of_T(Thi), W_of_T(Tlo)
        Ws = np.geomspace(Wmin, Wmax, 17)
        Tstars = []
        efforts = []
        used_W = []
        for W in Ws:
            J = c / Ts + W * mses
            i = int(np.argmin(J))
            Tstar = int(Ts[i])
            # reject boundary optima
            if i == 0 or i == len(Ts) - 1:
                continue
            Tstars.append(Tstar)
            efforts.append(1.0 / Tstar)
            used_W.append(W)
        used_W = np.array(used_W)
        efforts = np.array(efforts)
        Tstars = np.array(Tstars)
        if len(used_W) < 6:
            print(f"  H={H} too few interior optima ({len(used_W)})")
            continue
        # log-log slope: log effort = const + a log W
        coef, cov = np.polyfit(np.log(used_W), np.log(efforts), 1, cov=True)
        a_hat, intercept = coef
        resid = np.log(efforts) - (a_hat * np.log(used_W) + intercept)
        ss_res = np.sum(resid ** 2)
        ss_tot = np.sum((np.log(efforts) - np.mean(np.log(efforts))) ** 2)
        r2 = 1 - ss_res / ss_tot
        se = np.sqrt(cov[0, 0])

        # b: scale q, fix W at geometric mean of used_W. MSE scales linearly with q
        # (paths are unit-q), so J = c/T + W*q*MSE_unit(T) ≡ c/T + W'*MSE with W'=W q
        # so ˆb should equal â if we vary q at fixed W — identically the same fit
        # if we use the same grid. To do a distinct numerical pass, pick mid W
        # and vary q so that W*q covers the same range.
        Wfix = np.exp(np.mean(np.log(used_W)))
        qs = used_W / Wfix  # so Wfix*q = used_W
        Tstars_q = []
        efforts_q = []
        used_q = []
        for q in qs:
            J = c / Ts + Wfix * q * mses
            i = int(np.argmin(J))
            if i == 0 or i == len(Ts) - 1:
                continue
            Tstars_q.append(int(Ts[i]))
            efforts_q.append(1.0 / Ts[i])
            used_q.append(q)
        used_q = np.array(used_q)
        efforts_q = np.array(efforts_q)
        b_hat = np.polyfit(np.log(used_q), np.log(efforts_q), 1)[0]

        print(f"{H:6.2f} {a_th:10.4f} {a_hat:10.4f} {b_hat:10.4f} {len(used_W):5d} "
              f"{Tstars.min():4d}–{Tstars.max():<5d} {r2:8.4f}   se(a)={se:.4f}")
        results.append((H, a_th, a_hat, b_hat, se, r2, Tstars.min(), Tstars.max(), len(used_W)))

        # print a few T*(W)
        print(f"         T*(W): " + ", ".join(f"W={W:.3g}->T={T}" for W, T in list(zip(used_W, Tstars))[::4]))

    print()
    print("== exact (closed-form continuous MSE) elasticities, same W grid rule ==")
    for H in Hs:
        a_th = 1.0 / (1.0 + 2.0 * H)
        Tlo, Thi = 8.0, n / 16.0
        def W_of_T(T):
            return c * (1 + 2 * H) / (2 * H) / (T ** (1 + 2 * H))
        Ws = np.geomspace(W_of_T(Thi), W_of_T(Tlo), 17)
        # Use a fine continuous T grid
        Tgrid = np.geomspace(1.0, n / 4, 2000)
        efforts = []
        used_W = []
        for W in Ws:
            J = c / Tgrid + W * analytic_mse_continuous(Tgrid, H)
            Tstar = Tgrid[int(np.argmin(J))]
            # also the exact T*
            T_ex = (c * (1 + 2 * H) / (W * 2 * H)) ** (1.0 / (1 + 2 * H))
            efforts.append(1.0 / Tstar)
            used_W.append(W)
        a_hat = np.polyfit(np.log(used_W), np.log(efforts), 1)[0]
        print(f"  H={H:.2f}  theory={a_th:.6f}  fitted on numeric min of exact J={a_hat:.6f}")

    print()
    print("== discrete-time exact MSE (mean k^{2H}), numeric elasticity ==")
    for H in Hs:
        a_th = 1.0 / (1.0 + 2.0 * H)
        Tgrid = np.arange(2, n // 8 + 1)
        mse_d = np.array([analytic_mse_discrete(int(T), H) for T in Tgrid])
        Tlo, Thi = 8.0, n / 16.0
        def W_of_T(T):
            return c * (1 + 2 * H) / (2 * H) / (T ** (1 + 2 * H))
        Ws = np.geomspace(W_of_T(Thi), W_of_T(Tlo), 17)
        efforts, used_W = [], []
        for W in Ws:
            J = c / Tgrid + W * mse_d
            i = int(np.argmin(J))
            if i == 0 or i == len(Tgrid) - 1:
                continue
            efforts.append(1.0 / Tgrid[i])
            used_W.append(W)
        a_hat = np.polyfit(np.log(used_W), np.log(efforts), 1)[0]
        print(f"  H={H:.2f}  theory(cont)={a_th:.6f}  fitted discrete-grid={a_hat:.6f}  nW={len(used_W)}")

if __name__ == "__main__":
    main()
