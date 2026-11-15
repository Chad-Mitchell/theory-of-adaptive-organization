"""TELEGRAPH-LINEAR-PREMISE symbolic checks (sympy). In-model only. Units of Conti & Mora 2022 (arXiv 2011.09958v2):
y = +-1, switching rate 1/(2 tau) each way (corr e^{-|t|/tau}), observation ds = y dt + sqrt(theta) dW."""
import sympy as sp, json
out = {}
x, L, th, tau, t, dt, eta, k = sp.symbols('x L theta tau t dt eta k', real=True)
# S1: Ito map of the exact log-likelihood-ratio SDE dL = (2/theta) ds - (1/tau) sinh(L) dt to the posterior mean x = tanh(L/2)
#     Ito: dx = f'(L) dL + 1/2 f''(L) (dL)^2,  (dL)^2 = (4/theta) dt
f = sp.tanh(L/2)
fp, fpp = sp.diff(f, L), sp.diff(f, L, 2)
ds_coef = sp.simplify(fp*2/th)                          # coefficient of ds
dt_coef = sp.simplify(fp*(-sp.sinh(L)/tau) + sp.Rational(1, 2)*fpp*4/th)
X = sp.tanh(L/2)
ok_ds = sp.simplify(ds_coef - (1 - X**2)/th) == 0
ok_dt = sp.simplify((dt_coef - (-X/tau - X*(1 - X**2)/th)).rewrite(sp.exp)) == 0
out["S1_ds_coef_is_(1-x^2)/theta"] = bool(ok_ds)
out["S1_dt_coef_is_-x/tau-x(1-x^2)/theta"] = bool(ok_dt)
# S2: continuum limit of the exact discrete update (C&M eq. 11): x_n = tanh(atanh(c x_{n-1}) + s dt/theta), c = 1-2k, k = dt/(2tau)
#     second order in eps = s dt/theta with eps^2 -> dt/theta (Ito)
eps = sp.symbols('eps')
xp = sp.symbols('xp')
g = sp.tanh(sp.atanh(xp) + eps)
ser = sp.series(g, eps, 0, 3).removeO()
c1 = sp.simplify(ser.coeff(eps, 1)); c2 = sp.simplify(ser.coeff(eps, 2))
out["S2_first_order_coef"] = str(sp.factor(c1)); out["S2_second_order_coef"] = str(sp.factor(c2))
out["S2_second_order_is_-x(1-x^2)"] = bool(sp.simplify(c2 + xp*(1 - xp**2)) == 0)
# S3: Kalman steady state for OU with corr e^{-|t|/tau}, var 1 (q = 2/tau), noise density theta
P = sp.symbols('P', positive=True)
q = 2/tau
ric = sp.Eq(-2*P/tau + q - P**2/th, 0)
Ps = [s for s in sp.solve(ric, P)]
Ps = [s for s in Ps if sp.simplify(s.subs({tau: 10, th: 1})) > 0][0]
out["S3_kalman_P"] = str(sp.simplify(Ps))
kap = sp.symbols('kappa', positive=True)   # kappa = lambda*N/mu^2 = theta/(2 tau)
PL = sp.simplify(Ps.subs(th, 2*kap*tau))
out["S3_kalman_P_in_kappa"] = str(sp.simplify(PL))
out["S3_small_kappa_leading"] = str(sp.limit(PL/sp.sqrt(kap), kap, 0))
# S4: elasticities with local error elasticity eta: e = A w lam^eta mu^(2-2eta) P^(-eta) (P precision = 1/N), price c P^th
w, lam, mu, c, A, thp = sp.symbols('w lambda mu c A thetap', positive=True)
Pp = sp.symbols('Pp', positive=True)
cost = w*A*lam**eta*mu**(2 - 2*eta)*Pp**(-eta) + c*Pp**thp
sol = sp.solve(sp.diff(cost, Pp), Pp)[0]
el = {v.name: sp.simplify(sp.diff(sp.log(sol), v)*v) for v in (w, lam, mu)}
out["S4_effort_elasticities"] = {k_: str(v) for k_, v in el.items()}
tot = sp.simplify(cost.subs(Pp, sol))
a = sp.simplify(sp.diff(sp.log(tot), w)*w)
b_rate = sp.simplify(sp.diff(sp.log(tot), lam)*lam)
b_amp2 = sp.simplify(sp.diff(sp.log(tot), mu)*mu/2)   # elasticity in mu^2 (variance-like amplitude)
onset_rate = sp.simplify(-(1 - b_rate)/(1 - a)); onset_amp = sp.simplify(-(1 - b_amp2)/(1 - a))
out["S4_total_cost_elasticities"] = {"a(w)": str(a), "b(rate)": str(b_rate), "b(mu^2)": str(b_amp2)}
out["S4_onset_if_rho_in_rate"] = str(onset_rate); out["S4_onset_if_rho_in_amplitude^2"] = str(onset_amp)
out["S4_check_linear_eta_half"] = {"onset_rate": str(sp.simplify(onset_rate.subs(eta, sp.Rational(1, 2)))),
                                   "onset_amp": str(sp.simplify(onset_amp.subs(eta, sp.Rational(1, 2))))}
out["S4_check_bayes_eta_1"] = {"onset_rate": str(sp.simplify(onset_rate.subs(eta, 1))),
                               "onset_amp": str(sp.simplify(onset_amp.subs(eta, 1)))}
# S5: telegraph conditional mean after an exact read: E[y(t+s)|y(t)] via generator, rate r=1/(2tau)
r = 1/(2*tau)
Q = sp.Matrix([[-r, r], [r, -r]])
Pm = sp.simplify((Q*t).exp())
cm = sp.simplify(Pm[0, 0] - Pm[0, 1])   # E[y(t)|y(0)=+1]
out["S5_cond_mean_given_+1"] = str(cm)
out["S5_equals_exp(-t/tau)"] = bool(sp.simplify(cm - sp.exp(-t/tau)) == 0)
# conditional MSE of the conditional mean: E[(y - cm*y0)^2] = 1 - cm^2 = 1 - exp(-2t/tau)  (same as OU var 1, corr e^{-t/tau})
out["S5_cond_mse"] = str(sp.simplify(1 - cm**2))
print(json.dumps(out, indent=1)); json.dump(out, open("../out_symbolic.json", "w"), indent=1)
