"""Referee re-derivation for SCALE_ENDS (independent code path: scipy.constants, surface-gravity route,
numerical integration of evaporation, Page-time with Page 1976/2013's 1.4847 radiation-entropy factor).
Run: nice -n 19 python3 recheck.py"""
import scipy.constants as C
from scipy.integrate import solve_ivp
from math import pi, log
hb,c,G,k=C.hbar,C.c,C.G,C.k; Msun=1.98847e30; yr=C.Julian_year
def T_from_kappa(M):
    kappa=c**4/(4*G*M)              # surface gravity (m/s^2)
    return hb*kappa/(2*pi*c*k)
def S_area(M):
    rs=2*G*M/c**2; A=4*pi*rs**2; lp2=hb*G/c**3; return A/(4*lp2)
M=Msun
print("T_H via surface gravity:", T_from_kappa(M))
print("S via area/4lp^2 (nats):", S_area(M), " bits:", S_area(M)/log(2))
# first law check: dE/dS = kT
dM=M*1e-6; dS=S_area(M+dM)-S_area(M); print("first law dE/(k T dS):", (dM*c**2)/(k*T_from_kappa(M)*dS))
# evaporation by integration, photon-only Hawking power P=hbar c^6/(15360 pi G^2 M^2)
def rhs(t,y): return [-hb*c**4/(15360*pi*G**2*y[0]**2)]   # dM/dt = -P/c^2
# analytic integral rather than ODE stiffness at end: t = M0^3/(3K), K = hb c^4/(15360 pi G^2)
K=hb*c**4/(15360*pi*G**2); print("t_ev photon-only (yr):", M**3/(3*K)/yr)
Kp=2.011e-4*hb*c**4/G**2; print("t_ev Page-1976 massless set (yr):", M**3/(3*Kp)/yr)
sol=solve_ivp(rhs,[0,0.9*M**3/(3*K)],[M],rtol=1e-10); print("ODE M at 0.9 t_ev / M0:", sol.y[0,-1]/M, " analytic:", (0.1)**(1/3))
# Page time: S_rad = 1.4847*(S0-S_BH); Page time when S_rad = S_BH -> S_BH/S0 = 1.4847/2.4847
f=1.4847/2.4847; Mfrac=f**0.5; tP=1-Mfrac**3; print(f"Page time: S_BH/S0={f:.4f}, t_P/t_ev={tP:.4f} (Page 2013: 0.5381, 0.5975)")
print("half initial entropy radiated at t/t_ev =", 1-0.5**1.5)
# scrambling: (beta/2pi) ln S
beta=hb/(k*T_from_kappa(M)); print("t_scr (s):", beta/(2*pi)*log(S_area(M)))
# Bekenstein for proton, using CODATA proton radius 0.8409 fm
R=0.8409e-15; E=C.m_p*c**2; print("proton Bekenstein bits:", 2*pi*R*E/(hb*c*log(2)))
# Lloyd 1 kg check
print("1 kg BH bits:", S_area(1.0)/log(2), "(Lloyd: 3.827e16)")
# de Sitter
H0=67.4e3/(C.parsec*1e6); HL=H0*(0.685)**0.5; print("T_dS:", hb*HL/(2*pi*k), " S_dS:", pi*(c/HL)**2/(hb*G/c**3))
# Hydrogen excitation occupancy at 300K, first excited level 10.2 eV, degeneracy 4 (n=2 incl. 2s,2p; spin ignored both levels)
from math import exp
x=10.2*C.e/(k*300); print(f"H n=2 occupancy at 300K ~ 4 e^-{x:.0f} = 10^{(log(4)-x)/log(10):.0f}")
# ATP in kT
print("ATP ~50 kJ/mol in kT at 310K:", 50e3/(C.R*310), " -> 2.7e10 ATP =", 2.7e10*50e3/(C.R*310), "kT")
