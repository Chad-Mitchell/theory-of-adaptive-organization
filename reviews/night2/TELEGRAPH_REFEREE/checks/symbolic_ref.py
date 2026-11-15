"""Referee symbolic checks (independent of TELEGRAPH_LINEAR_PREMISE/code). sympy.
R1: Wonham filter for y in {+mu,-mu}, symmetric switching rate lam, ds = y dt + sqrt(N) dW, written for x = E[y]/mu.
R2: Ito map of the Wonham x-equation to L = ln(p/(1-p)) = 2 artanh(x).
R3: second-order (Ito) expansion of C&M eq.(11) with sigma^2 = theta/dt, k = dt/(2 tau).
R4: C&M eq.(20) as printed read as Ito: drift difference from Wonham; its Stratonovich->Ito conversion.
R5: printed eq.(20) mapped to L: drift under y = -1 (after a switch).
R6: stationary density of L in the observation filtration (innovations form) and the exact MSE in Bessel functions.
"""
import sympy as sp, json
x, L, mu, lam, N, th, tau, y, dt, s, eps = sp.symbols('x L mu lambda N theta tau y dt s epsilon', real=True)
out = {}
# R1: Wonham for p = P(y=+mu): dp = lam(1-2p)dt + p(h1-hbar)/N (ds - hbar dt), h1=mu, hbar = mu(2p-1)
p = sp.symbols('p')
hbar = mu*(2*p-1)
drift_p_given_ds = lam*(1-2*p)  # dt part, plus gain*(ds - hbar dt)
gain_p = p*(mu-hbar)/N
# x = 2p - 1 (in units of mu): dx = 2 dp (linear, no Ito term)
gain_x = sp.simplify((2*gain_p).subs(p,(x+1)/2))
drift_x = sp.simplify((2*drift_p_given_ds).subs(p,(x+1)/2))
out['R1_wonham_x'] = f"dx = [{drift_x}] dt + [{sp.factor(gain_x)}] (ds - mu*x dt)"
# C&M units mu=1, lam=1/(2tau), N=theta
gx = sp.factor(gain_x.subs({mu:1,N:th}))
dx_cm = sp.simplify(drift_x.subs({lam:1/(2*tau)}))
out['R1_cm_units'] = f"dx = [{dx_cm}] dt + [{gx}] (ds - x dt)"
# R2: Ito to L = 2 atanh(x). Under general y: ds = y dt + sqrt(N) dW (y in units of mu here mu=1)
f = 2*sp.atanh(x)
fx, fxx = sp.diff(f,x), sp.diff(f,x,2)
g = gx  # diffusion coefficient on ds; ds quadratic variation theta dt
drift_L_x = sp.simplify(fx*(dx_cm + gx*(y - x)) + sp.Rational(1,2)*fxx*g**2*th)
dL = sp.simplify(drift_L_x.subs(x, sp.tanh(L/2)).rewrite(sp.exp))
target = 2*y/th - sp.sinh(L)/tau
out['R2_L_drift_minus_target(2y/theta - sinh(L)/tau)'] = str(sp.simplify((dL - target.rewrite(sp.exp))))
out['R2_L_noise_coeff'] = str(sp.simplify(fx*gx*sp.sqrt(th)))
# R3: expand C&M eq.(11): x_n = [sinh(s/sig2) + (1-2k)x cosh(s/sig2)]/[cosh(s/sig2) + (1-2k) x sinh(s/sig2)]
# with s_n = y + sig*eta, sig^2 = theta/dt; let u = s_n/sig^2 = (y dt + sqrt(theta dt) eta)/theta.
eta = sp.symbols('eta', real=True)
u = (y*dt + sp.sqrt(th*dt)*eta)/th
k = dt/(2*tau)
xn = (sp.sinh(u) + (1-2*k)*x*sp.cosh(u))/(sp.cosh(u) + (1-2*k)*x*sp.sinh(u))
h = sp.symbols('h', positive=True)
ser = sp.series(xn.subs(dt, h**2), h, 0, 3).removeO()
ser = sp.expand(ser)
# E over eta (eta^2 -> 1, eta -> 0 in drift); collect h^2 (dt) term
c2 = ser.coeff(h,2)
c2 = sp.expand(c2).subs(eta**2,1)
c1 = ser.coeff(h,1)
drift_eq11 = sp.simplify(c2.subs(eta,0) if c2.has(eta) is False else sp.expand(c2).coeff(eta,0))
out['R3_eq11_Ito_drift'] = str(sp.factor(drift_eq11))
out['R3_eq11_noise_coeff_per_sqrtdt'] = str(sp.factor(c1))
out['R3_matches_wonham'] = bool(sp.simplify(drift_eq11 - (dx_cm + gx*(y - x))) == 0)
# R4: printed eq.(20): dx = -x/tau dt + (1-x^2)/theta * ds  (ds = y dt + sqrt(theta) dW), read as Ito
printed_drift = -x/tau + (1-x**2)/th*y
out['R4_printed_minus_wonham_drift'] = str(sp.factor(sp.simplify(printed_drift - (dx_cm + gx*(y-x)))))
b = (1-x**2)/th
strat_corr = sp.Rational(1,2)*b*sp.diff(b,x)*th
out['R4_strat_to_ito_correction'] = str(sp.factor(strat_corr))
out['R4_printed_as_Stratonovich_equals_wonham'] = bool(sp.simplify(printed_drift + strat_corr - (dx_cm + gx*(y-x))) == 0)
# R5: printed eq. mapped to L, Ito
drift_L_pr = sp.simplify(fx*printed_drift + sp.Rational(1,2)*fxx*b**2*th)
dLp = sp.simplify(drift_L_pr.subs(x, sp.tanh(L/2)))
out['R5_printed_L_drift'] = str(sp.simplify(dLp.rewrite(sp.exp)))
out['R5_printed_L_drift_y=-1_large_L_limit'] = str(sp.limit((dLp.subs(y,-1) + sp.sinh(L)/tau), L, sp.oo))
out['R5_printed_L_drift_y=+1_large_L_limit(+sinh/tau)'] = str(sp.limit((dLp.subs(y,1) + sp.sinh(L)/tau), L, sp.oo))
# R6: innovations form: ds = x dt + sqrt(theta) dnu (C&M units) -> drift_L = 2x/theta - sinh L/tau, x = tanh(L/2); sigma^2 = 4/theta
kap = sp.symbols('kappa', positive=True)
two_b_over_s2 = sp.simplify((2*sp.tanh(L/2)/th - sp.sinh(L)/tau)*th/2)
Phi = sp.integrate(two_b_over_s2.subs(tau, th/(2*kap)), L)
out['R6_log_stationary_density_L'] = str(sp.simplify(Phi))
out['R6_note'] = "p(L) ∝ exp(Phi) = cosh^2(L/2) exp(-kappa cosh L) (up to const); MSE/mu^2 = E[sech^2(L/2)] = 2K0/(K0+K1)"
print(json.dumps(out, indent=1, default=str))
json.dump(out, open('out_symbolic_ref.json','w'), indent=1, default=str)
