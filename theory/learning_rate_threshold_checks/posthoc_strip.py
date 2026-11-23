"""POST HOC (NOT preregistered) diagnosis of the T67 2D puzzle: corner-free strip judge A = {x < L} x (all y) on the n x n torus.
Exact transverse-Fourier decomposition: each k_y gives an independent real symmetric 1D chain with the same diagonal D(x).
Usage: posthoc_strip.py validate | posthoc_strip.py n L1 L2 L3 -> strip_n{n}.json"""
import sys, os, json, time, numpy as np, scipy.linalg as sl
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from t67lib import *

def strip_quantities(n, p, L, drive):
    J = coupling_vector(2, n, p).reshape(n, n)
    Jh = np.fft.fft2(J).real  # axis0 = k_x, axis1 = k_y
    A = np.arange(L); T = temps(n, A, drive)
    tot = np.zeros(4)
    for m in range(n // 2 + 1):
        lam = (ALPHA + 1.0) - Jh[:, m]
        Jx = np.fft.ifft(Jh[:, m]).real
        idx = (np.arange(n)[None, :] - np.arange(n)[:, None]) % n
        K = (ALPHA + 1.0) * np.eye(n) - Jx[idx]
        S = lyap_fourier(1, n, lam, T)
        q = np.array(quantities(K, S, T, A))
        w = 1.0 if (m == 0 or (n % 2 == 0 and m == n // 2)) else 2.0  # k_y and -k_y blocks are identical
        tot += w * q
    return tot  # I, Idot, t1, t2

if __name__ == "__main__":
    if sys.argv[1] == "validate":
        n, L = 12, 3
        for p in [1.3, 2.5]:
            K = dense_K(2, n, p); lam = spectrum(2, n, p)
            A = np.array([i * n + j for i in range(L) for j in range(n)])
            for drive in ["HOT", "COLD"]:
                T = temps(n * n, A, drive); S = lyap_fourier(2, n, lam, T)
                ref = np.array(quantities(K, S, T, A)); st = strip_quantities(n, p, L, drive)
                print(f"validate p={p} {drive}: dense {ref.round(10)} strip {st.round(10)} maxdiff {np.abs(ref-st).max():.2e}")
                assert np.abs(ref - st).max() < 1e-9
        print("STRIP VALIDATION PASS"); sys.exit()
    n = int(sys.argv[1]); Ls = [int(x) for x in sys.argv[2:5]]
    grid = [round(1.1 + 0.1 * i, 1) for i in range(30)]
    if os.environ.get("PGRID"): grid = [float(x) for x in os.environ["PGRID"].split(",")]
    out = {"n": n, "Ls": Ls, "rows": []}; t0 = time.time()
    for p in grid:
        row = {"p": p}
        for drive in ["EQ", "HOT", "COLD"]:
            row[drive] = [strip_quantities(n, p, L, drive).tolist() for L in Ls]
        out["rows"].append(row)
        json.dump(out, open(os.path.join(HERE, f"strip_n{n}.json"), "w"))
        print(f"strip n={n} p={p} {time.time()-t0:.0f}s", flush=True)
    print("FINISHED")
