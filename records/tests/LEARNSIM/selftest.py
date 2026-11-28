"""Code checks only (uses textbook discrete formulas to validate the simulator; the simulator itself never uses them)."""
import numpy as np, time
import world as w
rng = np.random.default_rng(1)
# R: discrete hold loss per step should be q(T-1)/2, spend C_R/T
for T in [5, 20, 40]:
    x = w.bm(rng, 2_000_000 + T, 1.0)
    e, nr = w.r_errors(x, T, 3)
    print('R T=%d mean e2 %.3f (discrete %.3f)  reads/step %.5f (1/T %.5f)' % (T, np.mean(e**2), (T-1)/2, nr/e.shape[0], 1/T))
# A: alpha self-tuned vs discrete Kalman steady-state gain and filtered variance
for q, k in [(1.0, 13.6), (0.01, 12000), (0.1, 400)]:
    R = w.SIG2 / k
    P = q / 2 + np.sqrt(q * q / 4 + q * R)  # prior variance P- solves P- = q + P- R/(P- + R)
    K = P / (P + R); Pf = P * R / (P + R)
    x = w.bm(rng, 400000, q)
    e, al = w.a_errors(x, k, rng, 100000)
    print('A q=%g k=%g alpha %.4f (Kalman %.4f) mean e2 %.4f (Kalman filtered %.4f)' % (q, k, al, K, np.mean(e**2), Pf))
t0 = time.time()
for W, q in [(1, 1.0), (4, 0.04)]:
    Ts = [w.es_learn('R', W, q, rng) for _ in range(8)]
    print('ES R W=%g q=%g learned T' % (W, q), Ts, 'pop', w.pop_learn('R', W, q, rng))
print('t', time.time() - t0); t0 = time.time()
for W, q in [(1, 1.0), (1000, 0.04)]:
    ks = [round(w.es_learn('A', W, q, rng), 1) for _ in range(4)]
    print('ES A W=%g q=%g learned k' % (W, q), ks, 'pop', round(w.pop_learn('A', W, q, rng), 1))
print('t', time.time() - t0)
