"""Mean-field (linear-Gaussian) predictions for the RW world, mean readout, MSE metric.
Written before the ant code; its output is part of the preregistration.
Prediction error recursion: eps' = (1-g) eps - g*v - eta + w  =>  Var = (q + g^2 r/n_s + V_eta) / (1-(1-g)^2)
  IND : g = e, n_s = N, V_eta = 0                         (=> optimum is the Kalman gain: T4)
  FOL : fixed follower fraction f; g = e(1-f), n_s=(1-f)N, followers resample the trail: V_eta = e^2 n_f V/N^2
  LOCK: follow prob p = S^2/(S^2+k^2), S = N/e (absolute trail mass); g = e(1-p), n_s = N(1-p), n_f = N p
  PRIV: one ant, own memory: g = e, n_s = 1
V (trail spread) = r + q(1-e)/(e(2-e)).
"""
import numpy as np, json
from world import SIGMA_D, SIGMA_OBS

F_FOLLOW = 0.75
K_LOCK = 100.0
NS = [1, 2, 4, 8, 16, 32, 64, 128, 256]
EGRID = np.exp(np.linspace(np.log(3e-4), np.log(1.0), 19))   # the sim's evaporation grid
FINE = np.exp(np.linspace(np.log(1e-5), np.log(1.0), 4000))


def kstar(z):  # K^2/(1-K) = z
    return (-z + np.sqrt(z * z + 4 * z)) / 2


def mse(arm, e, N, q, r):
    V = r + q * (1 - e) / np.maximum(e * (2 - e), 1e-300)
    if arm in ("IND", "PRIV"):
        n = 1 if arm == "PRIV" else N
        g, R, Ve = e, r / n, 0.0
    else:
        p = F_FOLLOW if arm == "FOL" else (N / e) ** 2 / ((N / e) ** 2 + K_LOCK ** 2)
        ns, nf = N * (1 - p), N * p
        g = e * (1 - p)
        R = r / np.maximum(ns, 1e-12)
        Ve = e * e * nf * V / N ** 2
    g = np.clip(g, 1e-12, 1.0)
    return (q + g * g * R + Ve) / (1 - (1 - g) ** 2)


def predict():
    out = {}
    for di, sd in enumerate(SIGMA_D):
        for so in SIGMA_OBS:
            q, r = sd ** 2, so ** 2 + 1 / 12
            for arm in ("IND", "FOL", "LOCK", "PRIV"):
                for N in NS:
                    m = mse(arm, FINE, N, q, r)
                    i = int(np.argmin(m))
                    out[f"{di}|{so}|{arm}|{N}"] = dict(estar=float(FINE[i]), mse=float(m[i]),
                                                       kstar_T4=float(kstar(N * q / r)))
    return out


if __name__ == "__main__":
    P = predict()
    json.dump(P, open("meanfield_pred.json", "w"), indent=1)
    for di in range(3):
        for so in SIGMA_OBS:
            print(f"drift sd {SIGMA_D[di]} obs sd {so}:")
            for arm in ("IND", "FOL", "LOCK", "PRIV"):
                es = [P[f"{di}|{so}|{arm}|{N}"]["estar"] for N in NS]
                ms = [P[f"{di}|{so}|{arm}|{N}"]["mse"] for N in NS]
                print(f"  {arm:5s} e*: " + " ".join(f"{v:.4f}" for v in es))
                print(f"        mse:" + " ".join(f"{v:8.2f}" for v in ms))
