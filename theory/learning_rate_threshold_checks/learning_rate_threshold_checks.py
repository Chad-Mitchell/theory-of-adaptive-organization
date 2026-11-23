"""Fast checks for T67 (theory/LEARNING_RATE_THRESHOLD_2026-11-23.md). Deterministic output, compared byte-for-byte
with learning_rate_threshold_checks.out by tools/test_learning_rate_threshold_checks.py."""
import os, sys, json, hashlib, subprocess, numpy as np, scipy.linalg as sl
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from t67lib import *
fails = 0
def check(name, ok):
    global fails
    print(f"{'PASS' if ok else 'FAIL'} {name}")
    fails += 0 if ok else 1
# 1. prereg lock
h = hashlib.sha256(open(os.path.join(HERE, "PREREG_T67.md"), "rb").read()).hexdigest()
lock = open(os.path.join(HERE, "PREREG_T67.sha256")).read().split()[0]
check(f"prereg sha256 matches lock ({lock[:12]}...)", h == lock == "b91e2101ec93acf3c22cf8b93241014012938b0db2fccc7df62ea27748d54b98")
# 2. gates G1, G2
w1 = w2 = 0.0
for d, n, L in [(1, 64, 8), (2, 8, 3)]:
    for p in [0.8, 2.5]:
        K = dense_K(d, n, p); lam = spectrum(d, n, p); A = region(d, n, L); T = temps(n ** d, A, "HOT")
        S = lyap_fourier(d, n, lam, T)
        w1 = max(w1, np.abs(S - sl.solve_continuous_lyapunov(-K, -2 * np.diag(T))).max())
        _, idot, _, _ = quantities(K, S, T, A); fd = idot_fd(K, S, T, A)
        w2 = max(w2, abs(fd - idot) / abs(fd))
check("G1 Fourier Lyapunov == scipy to < 1e-10", w1 < 1e-10)
check("G2 boundary-layer identity == finite difference to < 1e-5", w2 < 1e-5)
# 3. equilibrium: gross learning and forgetting cancel (stock costs zero)
K = dense_K(1, 256, 1.5); lam = spectrum(1, 256, 1.5); A = region(1, 256, 32)
S = lyap_fourier(1, 256, lam, np.ones(256)); I, idot, t1, t2 = quantities(K, S, np.ones(256), A)
check(f"EQ: t1 = -t2 (gross terms {t1:.6f}, {t2:.6f}), Idot = 0", abs(idot) < 1e-10 and t1 > 0.01)
# 4. recompute stored raw points
for d, n, p, Ls in [(1, 1024, 1.0, [8, 64, 128]), (1, 1024, 2.0, [32]), (2, 48, 1.5, [3, 6, 12])]:
    raw = json.load(open(os.path.join(HERE, f"raw_d{d}_n{n}.json")))
    rows = {r["L"]: r for r in raw["rows"] if abs(r["p"] - p) < 1e-9}
    K = dense_K(d, n, p); lam = spectrum(d, n, p); N = n ** d; worst = 0.0
    for L in Ls:
        A = region(d, n, L)
        for dr in ["EQ", "HOT", "COLD"]:
            T = temps(N, A, dr); S = lyap_fourier(d, n, lam, T)
            q = quantities(K, S, T, A)
            worst = max(worst, max(abs(a - b) for a, b in zip(q, rows[L][dr])))
    check(f"raw d={d} n={n} p={p} L={Ls} reproduces stored values (max diff < 1e-9)", worst < 1e-9)
# 5. gates G3, G4 recorded in the main run
for d, n in [(1, 1024), (1, 2048), (2, 48), (2, 64)]:
    g = json.load(open(os.path.join(HERE, f"raw_d{d}_n{n}.json")))["gate"]
    check(f"G3/G4 d={d} n={n}: max|Idot_EQ| < 1e-9 and Lyapunov residual < 1e-9", g["eq_idot_max"] < 1e-9 and g["res_max"] < 1e-9)
# 6. post-hoc strip decomposition == dense code
from posthoc_strip import strip_quantities
n, L, wd = 12, 3, 0.0
for p in [1.3, 2.5]:
    K = dense_K(2, n, p); lam = spectrum(2, n, p); A = np.array([i * n + j for i in range(L) for j in range(n)])
    for dr in ["HOT", "COLD"]:
        T = temps(n * n, A, dr); S = lyap_fourier(2, n, lam, T)
        wd = max(wd, np.abs(np.array(quantities(K, S, T, A)) - strip_quantities(n, p, L, dr)).max())
check("post-hoc strip transverse-Fourier decomposition == dense 2D code (< 1e-9)", wd < 1e-9)
# 7. analysis reproduces the stored report
r = subprocess.run([sys.executable, os.path.join(HERE, "analyze_t67.py")], capture_output=True, text=True)
check("analysis reproduces t67_run.out byte for byte", r.returncode == 0 and r.stdout == open(os.path.join(HERE, "t67_run.out")).read())
res = json.load(open(os.path.join(HERE, "t67_results.json")))
print("outcomes:", ", ".join(f"{k}={v['outcome']}" for k, v in sorted(res["cells"].items())))
print("GLOBAL:", res["global"])
print("FAILS", fails)
if fails == 0:
    print("ALL T67 CHECKS PASS")
sys.exit(1 if fails else 0)
