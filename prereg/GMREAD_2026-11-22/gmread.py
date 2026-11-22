"""Decision code for the GMREAD read-floor preregistration.

Simulated series only. This module does not fetch, open, or parse a
real stimulus or spike file. The official real-data label is computed
from the qualification record alone.

The scored coordinate is the directed-information read rate against the
scalar Gauss-Markov floor that a Kalman filter attains. Memory mutual
information is reported and is not part of the label. A fitted antitone
cloud is reported and is not part of the label.
"""

from __future__ import annotations

import math
import random
import statistics

# Locked numerical constants. PREREG.md quotes these values.
A_LO = 0.30
A_HI = 0.98
RHO2_MAX = 0.10
T_MIN = 2000
N_MIN = 8
BIAS_BOUND = 0.05
TAU = 0.15
Z = 1.96
SHIFT_NATS = 0.40
KURTOSIS_MAX = 1.0
LEAD_K = 0
SEED = 20261122

# Worked point in GENERAL_FORM.md §7, recomputed here as a formula check.
# Lead k = 2 is the worked distortion; the scored arm is lead 0.
WORKED = {
    "a": 0.9,
    "Q": 1.0,
    "P": 0.5,
    "k": 2,
    "V": 5.263157894736842,
    "I": 1.176939,
    "r": 0.516592,
    "D": 2.138050,
}


def gm_moments(a, Q, P, k=0):
    """Scalar Gauss-Markov floor in nats. Q > 0, |a| < 1, 0 < P <= V."""
    if not (0 <= abs(a) < 1 and Q > 0 and P > 0):
        raise ValueError("gm_moments domain")
    V = Q / (1.0 - a * a)
    if P > V * (1.0 + 1e-9):
        raise ValueError("P above the prior variance")
    I = 0.5 * math.log(V / P)
    r = 0.5 * math.log(a * a + Q / P)
    ak = a ** (2 * k)
    D = ak * P + V * (1.0 - ak)
    return {"V": V, "I": I, "r": r, "D": D}


def _mean(xs):
    return sum(xs) / len(xs)


def _var(xs):
    m = _mean(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)


def excess_kurtosis(xs):
    m = _mean(xs)
    c2 = sum((x - m) ** 2 for x in xs) / len(xs)
    if c2 <= 0:
        return float("inf")
    c4 = sum((x - m) ** 4 for x in xs) / len(xs)
    return c4 / (c2 * c2) - 3.0


def _demean(xs):
    m = _mean(xs)
    return [x - m for x in xs]


def _corr(u, v):
    mu, mv = _mean(u), _mean(v)
    su = math.sqrt(_var(u))
    sv = math.sqrt(_var(v))
    if su <= 0 or sv <= 0:
        return 0.0
    c = sum((a - mu) * (b - mv) for a, b in zip(u, v)) / len(u)
    return c / (su * sv)


def fit_ar1(xs):
    """Demeaned conditional least squares. Also returns the lag-1 correlation."""
    if len(xs) < 5:
        raise ValueError("series too short")
    z = _demean(xs)
    x0 = z[:-1]
    x1 = z[1:]
    s00 = sum(x * x for x in x0)
    s01 = sum(a * b for a, b in zip(x0, x1))
    a_cls = s01 / s00 if s00 > 0 else 0.0
    a_acf = _corr(x0, x1)
    resid = [b - a_cls * a for a, b in zip(x0, x1)]
    Q_hat = _var(resid) if len(resid) > 1 else float("nan")
    if len(resid) < 4:
        rho2 = 1.0
    else:
        rho2 = _corr(resid[:-2], resid[2:])
    return {
        "a": a_cls,
        "a_acf": a_acf,
        "Q": Q_hat,
        "rho2": rho2,
        "n": len(xs),
    }


def class_gate(fit, xs):
    """True only for a long, roughly Gaussian, one-pole series inside the locked band.

    The two slope estimators must agree (MV5). Disagreement drops the block.
    """
    reasons = []
    if fit["n"] < T_MIN:
        reasons.append("span")
    a = fit["a"]
    if not (A_LO <= abs(a) <= A_HI):
        reasons.append("pole")
    if abs(a - fit["a_acf"]) > 0.05:
        reasons.append("estimator_agreement")
    if not (fit["Q"] > 0):
        reasons.append("noise")
    if abs(fit["rho2"]) > RHO2_MAX:
        reasons.append("residual")
    if abs(excess_kurtosis(xs)) > KURTOSIS_MAX:
        reasons.append("gaussian")
    return (len(reasons) == 0), reasons


def simulate_series(a, Q, n, rng):
    V = Q / (1.0 - a * a)
    x = rng.gauss(0.0, math.sqrt(V))
    out = []
    for _ in range(n):
        x = a * x + rng.gauss(0.0, math.sqrt(Q))
        out.append(x)
    return out


def simulate_ar2(a1, a2, scale, n, rng):
    """A two-pole series. Used only to show the class gate can refuse."""
    x1 = rng.gauss(0.0, scale)
    x2 = rng.gauss(0.0, scale)
    out = []
    for _ in range(n):
        x = a1 * x1 + a2 * x2 + rng.gauss(0.0, scale)
        out.append(x)
        x2, x1 = x1, x
    return out


def run_filter(xs, a, Q, R, rng, memoryless=False, rate_shift=0.0):
    """One design on one series.

    memoryless: observe y = x + noise and set the estimate to the
    memoryless posterior mean. That design is feasible and sits above
    the read floor. rate_shift adds nats to the plug-in rate at fixed
    empirical P, the rigid shift on the read coordinate.
    """
    P = Q / (1.0 - a * a)
    xhat = 0.0
    rows = []
    for x in xs:
        y = x + rng.gauss(0.0, math.sqrt(R))
        P_pred = a * a * P + Q
        x_pred = a * xhat
        if memoryless:
            # posterior of x given y only, using the stationary prior
            V = Q / (1.0 - a * a)
            P_m = 1.0 / (1.0 / V + 1.0 / R)
            x_m = P_m * (y / R)  # prior mean 0
            rows.append((x, x_m, x_pred, P_pred))
            # the filter state is not kept; next prediction uses 0
            xhat = 0.0
            P = V
        else:
            K = P_pred / (P_pred + R)
            xhat = x_pred + K * (y - x_pred)
            P = (1.0 - K) * P_pred
            rows.append((x, xhat, x_pred, P_pred))
    # empirical plug-in on the second half only (train/test split)
    half = len(rows) // 2
    test = rows[half:]
    P_hat = _mean([(x - xh) ** 2 for x, xh, _, _ in test])
    # one-step predictor that is allowed to use the previous filtered
    # estimate: for the Kalman design that predictor is x_pred.
    # Rebuild predicted MSE against the same test points.
    P_pred_hat = _mean([(x - xp) ** 2 for x, _, xp, _ in test])
    if P_hat <= 0 or P_pred_hat <= 0:
        r_hat = float("nan")
    else:
        r_hat = 0.5 * math.log(P_pred_hat / P_hat) + rate_shift
    return {"P": P_hat, "r": r_hat, "n_test": len(test)}


def floor_excess(r_hat, a, Q, P):
    floor = gm_moments(a, Q, P, k=LEAD_K)
    return r_hat - floor["r"], floor


def dominated_fraction(points):
    """Share of points strictly dominated in (r, D), both smaller-is-better."""
    n = len(points)
    if n == 0:
        return float("nan")
    dominated = 0
    for i, (r_i, d_i) in enumerate(points):
        for j, (r_j, d_j) in enumerate(points):
            if i == j:
                continue
            if r_j <= r_i and d_j <= d_i and (r_j < r_i or d_j < d_i):
                dominated += 1
                break
    return dominated / n


def isotonic_decreasing(xs, ys):
    """PAVA for a decreasing fit of y on x. Returns fitted y in input order."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    # decreasing in x means non-increasing along the sorted x
    blocks = []  # each block: (weight, value, indices)
    for i in order:
        blocks.append([1.0, ys[i], [i]])
        while len(blocks) >= 2 and blocks[-2][1] < blocks[-1][1]:
            w1, v1, i1 = blocks[-2]
            w2, v2, i2 = blocks[-1]
            w = w1 + w2
            v = (w1 * v1 + w2 * v2) / w
            blocks[-2] = [w, v, i1 + i2]
            blocks.pop()
    fitted = [0.0] * len(xs)
    for _, v, idxs in blocks:
        for i in idxs:
            fitted[i] = v
    return fitted


def cloud_excess(points):
    """Mean squared residual of D about a decreasing fit on r. Zero on a perfect antitone curve."""
    if len(points) < 2:
        return float("nan")
    rs = [p[0] for p in points]
    ds = [p[1] for p in points]
    fitted = isotonic_decreasing(rs, ds)
    return _mean([(d - f) ** 2 for d, f in zip(ds, fitted)])


def decide(qualification, class_ok, excesses):
    """Return (label, detail).

    labels: supports, fails_to_support, not_a_test.
    """
    detail = {
        "qualification": qualification,
        "class_ok": bool(class_ok),
        "n": len(excesses),
        "tau": TAU,
        "bias_bound": BIAS_BOUND,
        "z": Z,
    }
    if qualification != "established":
        detail["reason"] = "qualification_" + qualification
        return "not_a_test", detail
    if not class_ok:
        detail["reason"] = "world_class"
        return "not_a_test", detail
    if len(excesses) < N_MIN:
        detail["reason"] = "too_few_blocks"
        return "not_a_test", detail
    if any(not math.isfinite(e) for e in excesses):
        detail["reason"] = "non_finite_excess"
        return "not_a_test", detail
    mean_e = _mean(excesses)
    if len(excesses) == 1:
        se = float("inf")
    else:
        se = statistics.pstdev(excesses) / math.sqrt(len(excesses))
    half = Z * se
    detail.update({"mean_excess": mean_e, "se": se, "half_width": half})
    if not math.isfinite(half) or half >= TAU:
        detail["reason"] = "resolution"
        return "not_a_test", detail
    lo = mean_e - half
    hi = mean_e + half
    detail.update({"lo": lo, "hi": hi})
    if hi < -BIAS_BOUND:
        detail["reason"] = "below_floor"
        return "not_a_test", detail
    if hi <= TAU and lo >= -BIAS_BOUND:
        detail["reason"] = "within_read_floor"
        return "supports", detail
    if lo > TAU:
        detail["reason"] = "read_rate_above_floor"
        return "fails_to_support", detail
    detail["reason"] = "unresolved"
    return "not_a_test", detail


def official_real_label():
    """The only label this lock assigns to the named real deposit.

    Qualification inputs (a), (b) and (e) are not established in the
    lock, so the pre-written rule stops before any design series is read.
    """
    label, detail = decide("not_established", True, [0.0] * N_MIN)
    detail["real_files_opened"] = False
    detail["reason"] = "qualification_not_established"
    return label, detail


def _one_block(rng, kind, a=0.8, Q=1.0, R=0.5, n=T_MIN):
    """Return (class_ok, excess, (r, D)) for one simulated block."""
    if kind == "nongm":
        xs = simulate_ar2(0.7, -0.5, 1.0, n, rng)
    else:
        xs = simulate_series(a, Q, n, rng)
    fit = fit_ar1(xs)
    ok, _ = class_gate(fit, xs)
    if kind == "memoryless":
        est = run_filter(xs, a, Q, R, rng, memoryless=True)
    elif kind == "shifted":
        est = run_filter(xs, a, Q, R, rng, rate_shift=SHIFT_NATS)
    elif kind == "below":
        est = run_filter(xs, a, Q, R, rng, rate_shift=-(BIAS_BOUND + TAU + 0.2))
    else:
        est = run_filter(xs, a, Q, R, rng, rate_shift=0.0)
    # Floor uses the stimulus fit, which is what a real run would have,
    # except when the class gate has already failed.
    if est["P"] <= 0 or not math.isfinite(est["r"]) or fit["Q"] <= 0:
        return ok, float("nan"), (float("nan"), float("nan"))
    # clip P into the prior so the floor is defined under sampling noise
    V = fit["Q"] / (1.0 - fit["a"] * fit["a"]) if abs(fit["a"]) < 1 else float("inf")
    P_use = min(est["P"], 0.999 * V) if math.isfinite(V) and V > 0 else est["P"]
    if not (0.3 <= abs(fit["a"]) < 1 and fit["Q"] > 0 and P_use > 0):
        return False, float("nan"), (est["r"], est["P"])
    excess, floor = floor_excess(est["r"], fit["a"], fit["Q"], P_use)
    return ok, excess, (est["r"], floor["D"])


def scenario(kind, n_blocks=N_MIN, seed=SEED, qualification="established"):
    """One full decision, plus the cloud summary, on simulated blocks."""
    rng = random.Random(seed)
    excesses = []
    points = []
    class_oks = []
    for i in range(n_blocks):
        # distinct observation noises so the cloud has a slope
        R = 0.25 + 0.15 * i
        ok, excess, point = _one_block(rng, kind, R=R, n=T_MIN)
        class_oks.append(ok)
        excesses.append(excess)
        points.append(point)
    class_ok = all(class_oks) if kind != "nongm" else (sum(class_oks) == len(class_oks))
    if kind == "nongm":
        class_ok = False
    if kind == "unqualified":
        qualification = "not_established"
    label, detail = decide(qualification, class_ok, excesses if kind != "nongm" else excesses)
    # For a non-GM world the class gate is the stopping rule even if some
    # blocks happened to pass. Force the recorded class flag.
    if kind == "nongm":
        label, detail = decide(qualification, False, excesses)
    finite_points = [p for p in points if all(math.isfinite(v) for v in p)]
    detail["cloud_dominated_fraction"] = dominated_fraction(finite_points)
    detail["cloud_isotonic_mse"] = cloud_excess(finite_points)
    detail["kind"] = kind
    detail["label"] = label
    return detail


def power_study(n_mc=200, seed=SEED):
    """Frequencies of the two decisive labels under the two target worlds."""
    counts = {"on_floor": {}, "shifted": {}}
    for i in range(n_mc):
        for name in ("on_floor", "shifted"):
            detail = scenario(name, seed=seed + 10000 + i)
            label = detail["label"]
            counts[name][label] = counts[name].get(label, 0) + 1
    out = {}
    for name, hist in counts.items():
        out[name] = {k: v / n_mc for k, v in sorted(hist.items())}
        out[name]["n_mc"] = n_mc
    out["pi"] = 0.8
    out["supports_when_on_floor"] = out["on_floor"].get("supports", 0.0)
    out["fails_when_shifted"] = out["shifted"].get("fails_to_support", 0.0)
    out["gate_met"] = (
        out["supports_when_on_floor"] >= 0.8 and out["fails_when_shifted"] >= 0.8
    )
    return out


def check_worked_point(tol=2e-4):
    m = gm_moments(WORKED["a"], WORKED["Q"], WORKED["P"], k=WORKED["k"])
    for key in ("V", "I", "r", "D"):
        if abs(m[key] - WORKED[key]) > tol * max(1.0, abs(WORKED[key])):
            raise AssertionError((key, m[key], WORKED[key]))
    # lead 0: distortion equals the posterior variance
    m0 = gm_moments(WORKED["a"], WORKED["Q"], WORKED["P"], k=0)
    if abs(m0["D"] - WORKED["P"]) > 1e-12:
        raise AssertionError(m0["D"])
    return m


def demonstrate(seed=SEED):
    """Every official label, plus the cloud-versus-floor separation."""
    check_worked_point()
    real_label, real_detail = official_real_label()
    kinds = ["on_floor", "shifted", "below", "nongm", "unqualified", "memoryless"]
    rows = [scenario(k, seed=seed + 17 * (i + 1)) for i, k in enumerate(kinds)]
    return {
        "worked_point_ok": True,
        "official_real": {"label": real_label, **{k: real_detail[k] for k in ("reason", "real_files_opened")}},
        "scenarios": rows,
    }
