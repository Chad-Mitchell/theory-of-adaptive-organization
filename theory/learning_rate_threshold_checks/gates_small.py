"""Gates G1, G2 on small cases (PREREG_T67.md)."""
import sys, numpy as np, scipy.linalg as sl
sys.path.insert(0, __import__('os').path.dirname(__file__))
from t67lib import *
worst1 = worst2 = 0.0
for d, n, L in [(1, 64, 8), (2, 8, 3)]:
    for p in [0.8, 2.5]:
        K = dense_K(d, n, p); lam = spectrum(d, n, p)
        assert np.allclose(np.linalg.eigvalsh(K), np.sort(lam), atol=1e-12)
        A = region(d, n, L); T = temps(n ** d, A, "HOT")
        Sf = lyap_fourier(d, n, lam, T)
        Ss = sl.solve_continuous_lyapunov(-K, -2 * np.diag(T))
        e1 = np.abs(Sf - Ss).max(); worst1 = max(worst1, e1)
        I, idot, t1, t2 = quantities(K, Sf, T, A)
        fd = idot_fd(K, Sf, T, A)
        e2 = abs(fd - idot) / abs(fd); worst2 = max(worst2, e2)
        Id = mi_direct(Sf, A)
        print(f"d={d} n={n} p={p} L={L}: G1 |S_fft-S_scipy|={e1:.2e}  Idot_id={idot:.10f} Idot_fd={fd:.10f} rel={e2:.2e}  I={I:.10f} I_direct={Id:.10f}")
        assert abs(I - Id) < 1e-10
print(f"G1 worst {worst1:.2e} {'PASS' if worst1 < 1e-10 else 'FAIL'}")
print(f"G2 worst {worst2:.2e} {'PASS' if worst2 < 1e-5 else 'FAIL'}")
