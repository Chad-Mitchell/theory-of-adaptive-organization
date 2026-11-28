#!/usr/bin/env python3
"""Fresh world generators for the WF-HSV prereg.  Locked with PREREG.md.

Does not yield any of the 21 rhythm-test worlds, seed2_two_light, or S5
seeds 0..119 (different rng streams).  A parameter-collision check is
applied against the excluded (a, v, N) tuples when those files are present.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

# Public-clone root: this file lives at theory/keystone_checks/waterfill_2026-11-20/.
# Do not hardcode a private workdir.
REPO = Path(__file__).resolve().parents[3]
CHECKS = REPO / "theory" / "keystone_checks"
RHYTHM_JSON = CHECKS / "rhythm_rule.json"
S5_JSON = CHECKS / "s5_rerun.json"
T20_JSON = CHECKS / "holographic_2026-11-20" / "predictions.json"
FRAC_JSON = CHECKS / "imp_n60_predictions.json"

R_GRID_S = np.logspace(-1, 7, 161).tolist()
R_GRID_R = [0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0, 300.0, 1000.0]

EXCLUDED_IDS = [
    "1osc_z0.02_N0.04", "1osc_z0.02_N0.2", "1osc_z0.08_N0.04", "1osc_z0.08_N0.2",
    "1osc_z0.25_N0.04", "1osc_z0.25_N0.2", "1osc_z1.0_N0.04", "1osc_z1.0_N0.2",
    "2osc_close2_heavy_heavy", "2osc_close2_light_light", "2osc_close2_light_medium",
    "2osc_close2_medium_medium", "2osc_sep15_heavy_heavy", "2osc_sep15_light_light",
    "2osc_sep15_light_medium", "2osc_sep15_medium_medium",
    "3osc_heavy_heavy_heavy", "3osc_light_light_light", "3osc_medium_medium_medium",
    "3osc_mixed", "seed2_two_light",
]


def _parse_av(raw_a, raw_v):
    # poles / variances may be real lists or [re, im] pairs
    if raw_a and isinstance(raw_a[0], (list, tuple)):
        a = np.array([complex(x[0], x[1]) for x in raw_a], complex)
    else:
        a = np.asarray(raw_a, complex)
    if raw_v and isinstance(raw_v[0], (list, tuple)):
        v = np.array([complex(x[0], x[1]) for x in raw_v], complex)
    else:
        v = np.asarray(raw_v, complex)
    return a, v


def _scalefree_av(alpha, span, per_decade=1, tau_min=1.0):
    """Same construction as stores.scalefree_world (geometric rates, v ∝ τ^{α-1})."""
    J = max(2, int(round(per_decade * np.log10(span))) + 1)
    tau = tau_min * np.logspace(0, np.log10(span), J)
    v = tau ** (alpha - 1)
    v = v / v.sum()
    return 1.0 / tau, v


def _load_excluded():
    """Full prereg §4 exclusion set, for later use.

    The official 20 Nov 2026 confirmation set was built with a narrower
    loader (rhythm_rule.json only; Model S never called _too_close). That
    gap is recorded as post-result deviation D2. The official 64 worlds
    were independently checked and are clean; this function is not a
    rescoring of that run.
    """
    rows = []
    if RHYTHM_JSON.is_file():
        data = json.loads(RHYTHM_JSON.read_text())
        for w in data.get("results", []):
            a, v = _parse_av(w["a"], w["v"])
            rows.append((w.get("id"), a, v, float(w["N"])))
    if S5_JSON.is_file():
        data = json.loads(S5_JSON.read_text())
        for w in data.get("worlds", []):
            seed = w.get("seed")
            if seed is None:
                continue
            seed = int(seed)
            if seed < 0 or seed > 119:
                continue
            a, v = _parse_av(w["a"], w["v"])
            rows.append((f"s5_seed_{seed}", a, v, float(w["N"])))
    if T20_JSON.is_file():
        data = json.loads(T20_JSON.read_text())
        for w in data.get("worlds", []):
            a, v = _parse_av(w["a"], w["v"])
            rows.append((w.get("id"), a, v, float(w["N"])))
    if FRAC_JSON.is_file():
        data = json.loads(FRAC_JSON.read_text())
        for w in data.get("fractal", []):
            a, v = _scalefree_av(float(w["alpha"]), float(w["Gamma"]), int(w["per_decade"]))
            rows.append((w.get("id"), np.asarray(a, complex), np.asarray(v, complex), float(w["N"])))
    return rows


_EXCLUDED = None


def excluded_rows():
    global _EXCLUDED
    if _EXCLUDED is None:
        _EXCLUDED = _load_excluded()
    return _EXCLUDED


def _too_close(a, v, N, tol=1e-10):
    a = np.asarray(a, complex)
    v = np.asarray(v, complex)
    N = float(N)
    order = np.argsort(a)
    a, v = a[order], v[order]
    for _id, a2, v2, N2 in excluded_rows():
        a2, v2 = np.asarray(a2, complex), np.asarray(v2, complex)
        if a2.size != a.size:
            continue
        order2 = np.argsort(a2)
        a2, v2 = a2[order2], v2[order2]
        da = np.max(np.abs(a - a2) / np.maximum(np.abs(a2), 1e-18))
        dv = np.max(np.abs(v - v2) / np.maximum(np.abs(v2), 1e-18))
        dN = abs(N - N2) / max(abs(N2), 1e-18)
        if da < tol and dv < tol and dN < tol:
            return True, _id
    return False, None


def pack_oscillators(omegas, betas, vpoles):
    a, v = [], []
    for om, be, vp in zip(omegas, betas, vpoles):
        a.extend([be + 1j * om, be - 1j * om])
        v.extend([complex(vp, 0.0), complex(vp, 0.0)])
    return np.asarray(a, complex), np.asarray(v, complex)


def model_s_world(i, max_bumps=32):
    # bump=0 keeps the official stream 20261120 + 17*i. The official Model S
    # worlds never ran this check; D2 records the gap. All official draws
    # were later found clean, so bump stays 0 on a regeneration.
    last_eid = None
    for b in range(max_bumps):
        rng = np.random.default_rng(20261120 + 17 * i + 7919 * b)
        J = int(rng.integers(3, 5))
        sep = 10 ** rng.uniform(0.5, 2.0, J - 1)
        taus = np.cumprod(np.r_[10 ** rng.uniform(0, 1), sep])
        v = 10 ** rng.uniform(-1.5, 1.5, J)
        N = 10 ** rng.uniform(-2, 1)
        a = 1.0 / taus
        close, eid = _too_close(a, v, N)
        if not close:
            return dict(
                id=f"ms_{i:04d}", cls="model_s", i=int(i),
                a=a.astype(float).tolist(), v=v.astype(float).tolist(),
                N=float(N), J=int(J), degree=int(J),
                taus=taus.astype(float).tolist(), bumps=int(b),
            )
        last_eid = eid
    raise RuntimeError(f"model S world {i} collided {max_bumps} times (last {last_eid})")


def _draw_oscs(rng, n_osc):
    omega0 = 10 ** rng.uniform(-1.5, 0.5)
    omegas = [float(omega0)]
    for _k in range(1, n_osc):
        omegas.append(omegas[-1] * 10 ** rng.uniform(0.5, 1.3))
    betas, vpoles = [], []
    for k in range(n_osc):
        zeta = 10 ** rng.uniform(-2.0, -0.15)
        betas.append(float(zeta * omegas[k]))
        vpoles.append(float(10 ** rng.uniform(-1.2, 0.0) / 2.0))
    return omegas, betas, vpoles


def _draw_ous(rng, n_ou):
    if n_ou <= 0:
        return [], []
    sep = 10 ** rng.uniform(0.5, 2.0, max(n_ou - 1, 0)) if n_ou > 1 else np.array([])
    taus = np.cumprod(np.r_[10 ** rng.uniform(0, 1), sep]) if n_ou else np.array([])
    if n_ou == 1:
        taus = np.array([10 ** rng.uniform(0, 2)])
    v = 10 ** rng.uniform(-1.5, 1.5, n_ou)
    a = 1.0 / taus
    return [float(x) for x in a], [float(x) for x in v]


def _accept(world, bumps):
    a = world["a"]
    v = world["v"]
    close, eid = _too_close(a, v, world["N"])
    if close:
        return False, eid
    return True, None


def rhythm_world(i, max_bumps=32):
    n_osc = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3][i]
    bumps = 0
    for b in range(max_bumps):
        rng = np.random.default_rng(20261120 + 10007 * (i + 1) + 7919 * b)
        N = float(10 ** rng.uniform(-1.6, -0.3))
        omegas, betas, vpoles = _draw_oscs(rng, n_osc)
        a, v = pack_oscillators(omegas, betas, vpoles)
        w = dict(
            id=f"rh_{i:04d}", cls="rhythm", i=int(i),
            a=[(complex(x).real, complex(x).imag) for x in a],
            v=[(complex(x).real, complex(x).imag) for x in v],
            N=N, n_osc=int(n_osc), n_ou=0, degree=int(2 * n_osc),
            omegas=omegas, betas=betas, vpoles=vpoles, bumps=int(b),
        )
        # store a,v as complex-serializable pairs; also raw lists
        w["_a"] = a
        w["_v"] = v
        ok, eid = _too_close(a, v, N)
        if not ok:
            w.pop("_a"); w.pop("_v")
            w["a"] = [complex(x) for x in a]
            w["v"] = [complex(x) for x in v]
            return _serialise(w)
        bumps = b + 1
    raise RuntimeError(f"rhythm world {i} collided {max_bumps} times (last {eid})")


def mixed_world(i, max_bumps=32):
    n_ou = [1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 2][i]
    n_osc = [1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2][i]
    for b in range(max_bumps):
        rng = np.random.default_rng(20261120 + 20011 * (i + 1) + 7919 * b)
        N = float(10 ** rng.uniform(-1.6, -0.3))
        ao, vo = _draw_ous(rng, n_ou)
        omegas, betas, vpoles = _draw_oscs(rng, n_osc)
        ac, vc = pack_oscillators(omegas, betas, vpoles)
        a = np.concatenate([np.asarray(ao, complex), ac])
        v = np.concatenate([np.asarray(vo, complex), vc])
        w = dict(
            id=f"mx_{i:04d}", cls="mixed", i=int(i),
            N=N, n_osc=int(n_osc), n_ou=int(n_ou),
            degree=int(n_ou + 2 * n_osc),
            ou_a=ao, ou_v=vo,
            omegas=omegas, betas=betas, vpoles=vpoles, bumps=int(b),
        )
        ok, eid = _too_close(a, v, N)
        if not ok:
            w["a"] = [complex(x) for x in a]
            w["v"] = [complex(x) for x in v]
            return _serialise(w)
    raise RuntimeError(f"mixed world {i} collided {max_bumps} times (last {eid})")


def _serialise(w):
    def c_to_pair(x):
        z = complex(x)
        return [float(z.real), float(z.imag)]
    out = {k: v for k, v in w.items() if not k.startswith("_")}
    if "a" in out:
        out["a"] = [c_to_pair(x) for x in out["a"]]
    if "v" in out:
        out["v"] = [c_to_pair(x) for x in out["v"]]
    return out


def restore_av(world):
    def pairs(key):
        raw = world[key]
        if len(raw) == 0:
            return np.zeros(0, complex)
        if isinstance(raw[0], (list, tuple)):
            return np.array([complex(x[0], x[1]) for x in raw], complex)
        return np.array(raw, complex)
    return pairs("a"), pairs("v"), float(world["N"])


def all_worlds():
    ms = [model_s_world(i) for i in range(40)]
    # model S a,v are real lists already
    rh = [rhythm_world(i) for i in range(12)]
    mx = [mixed_world(i) for i in range(12)]
    return ms, rh, mx


def sanity_worlds():
    return [
        dict(id="sane_A", a=[0.3], v=[1.0], N=0.05),
        dict(id="sane_B", a=[1.0], v=[0.4], N=0.2),
        dict(id="sane_C", a=[0.02], v=[2.0], N=0.1),
    ]


if __name__ == "__main__":
    ms, rh, mx = all_worlds()
    print(f"Model S {len(ms)}, rhythm {len(rh)}, mixed {len(mx)}")
    print("sample ms_0000", {k: ms[0][k] for k in ('id','J','N')})
    print("sample rh_0000", {k: rh[0][k] for k in ('id','n_osc','N','bumps')})
    print("sample mx_0000", {k: mx[0][k] for k in ('id','n_ou','n_osc','N','bumps')})
