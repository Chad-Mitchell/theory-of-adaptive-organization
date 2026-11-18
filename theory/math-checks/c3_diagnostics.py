"""Task 2 / C3: measurement diagnostics using ONLY the predictor columns of C3's analysis_dataset.csv
(no outcome columns E, T, event_time, last_commit are read). Plus the identity-based prediction for beta_tau."""
import csv, numpy as np
rows = list(csv.DictReader(open('<local>/gtao/tests/C3/data/analysis_dataset.csv')))
def col(k): return np.array([float(r[k]) if r[k] not in ('', 'None') else np.nan for r in rows])
sig, mu, B, tau = col('sigma'), col('noncore_mean'), col('B'), col('tau')
ok = np.isfinite(sig) & np.isfinite(mu) & np.isfinite(B) & np.isfinite(tau) & (sig > 0) & (mu > 0) & (B > 0)
sig, mu, B, tau = sig[ok], mu[ok], B[ok], tau[ok]
print("n =", ok.sum())
fano = sig**2/mu
print("Fano factor sigma^2/mean(monthly noncore inflow): quartiles", np.round(np.percentile(fano, [25, 50, 75]), 2),
      " share with Fano<2 (near pure Poisson counting noise):", round(np.mean(fano < 2), 2))
b = np.polyfit(np.log(mu), np.log(sig), 1)[0]
print("slope d ln sigma / d ln mean inflow =", round(b, 3), " (0.5 = pure Poisson; 1 = shocks proportional to size)")
print("corr(ln sigma, ln B) =", round(np.corrcoef(np.log(sig), np.log(B))[0, 1], 3))
tau_m = tau/30.44
z_naive = B/(sig*np.sqrt(tau_m))
print("naive z = B/(sigma sqrt(tau[months])) if B were a stock (it is a flow, items/month): quartiles",
      np.round(np.percentile(z_naive, [10, 25, 50, 75, 90]), 2))
print("tau (months) quartiles", np.round(np.percentile(tau_m, [10, 25, 50, 75, 90]), 2))
print("NOTE: units do not match the first-passage model: B is closures/month (flow), sigma is SD of monthly",
      "inflow counts (items/month), tau days. sigma*sqrt(tau)/B has units sqrt(month); z is undefined.")

print("\n== Identity-based prediction for C3's Cox coefficients ==")
print("Dimensional identity (any F): eps_tau = eps_sigma/2 - 1, eps_B = -eps_sigma, with eps_sigma >= 2 in models A,B,C.")
bs = 0.28   # C3 literal beta_sigma (point)
print(f"(a) no attenuation: beta_sigma={bs} < 2 is impossible in A,B,C; identity would give beta_tau = {bs/2-1:.2f} (observed ~0.00)")
print("(b) equal attenuation a = beta_sigma/eps_sigma_true (eps_true >= 2):  beta_tau = beta_sigma/2 - a, in [0, beta_sigma/2)")
for eps in [2, 2.5, 3, 5, 10, 1e9]:
    a = bs/eps
    print(f"    eps_sigma_true={eps:>6}: attenuation a={a:.3f}, predicted beta_tau={bs/2 - a:.3f}, predicted r_tau={0.5-1/eps:.3f}")
print("    C3 literal beta_tau 95% CI [-0.09, 0.10]: covers predictions for eps_sigma_true up to ~",
      round(1/(0.5-0.10/bs) if 0.5-0.10/bs > 0 else float('inf'), 1), "(solve 0.28/2 - 0.28/eps = 0.10)")
print("(c) prereg band r_tau in [0.25,1] requires eps_sigma_true >= 4 (r_tau = 1/2 - 1/eps < 1/2 always): the band's upper half was unreachable.")
