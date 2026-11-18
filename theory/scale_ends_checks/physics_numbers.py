"""SCALE_ENDS numerical checks. CODATA 2018 constants. Run: nice -n 19 python3 physics_numbers.py"""
from math import pi, log, exp, sqrt
hbar=1.054571817e-34; c=2.99792458e8; G=6.67430e-11; k=1.380649e-23
Msun=1.98847e30; yr=3.15576e7; mp=1.67262192e-27; eV=1.602176634e-19
lp2=hbar*G/c**3
def bh(M):
    rs=2*G*M/c**2
    S=4*pi*G*M**2/(hbar*c)          # S/k (nats)
    T=hbar*c**3/(8*pi*G*M*k)
    P_photon=hbar*c**6/(15360*pi*G**2*M**2)
    t_photon=5120*pi*G**2*M**3/(hbar*c**4)
    P_page=2.011e-4*hbar*c**6/(G**2*M**2)  # Page 1976, massless nu+gamma+graviton
    t_page=M**3*G**2/(3*2.011e-4*hbar*c**4)
    beta=hbar/(k*T)
    t_scr=beta/(2*pi)*log(S)
    return dict(rs=rs,S_nats=S,S_bits=S/log(2),T=T,P_photon=P_photon,t_photon_yr=t_photon/yr,
                P_page=P_page,t_page_yr=t_page/yr,t_scr=t_scr,rs_over_c=rs/c,
                E_per_nat_over_kT=(M*c**2)/(S*k*T))
for name,M in [("1 Msun",Msun),("Sgr A* 4.3e6 Msun",4.3e6*Msun),("1 kg",1.0)]:
    d=bh(M); print(name); [print(f"   {a} = {b:.4g}") for a,b in d.items()]
# Page time: S(t) ∝ M^2, M^3 decreases linearly: M(t)^3 = M0^3 (1 - t/t_ev). Half entropy: M = M0/sqrt2
print("Page time fraction of lifetime (half entropy radiated, constant species):", 1-2**-1.5)
# Bekenstein bound for a proton: S <= 2 pi k R E/(hbar c)
for R in (0.8409e-15,0.84e-15):
    Sn=2*pi*R*mp*c**2/(hbar*c); print(f"Bekenstein proton R={R}: {Sn:.3f} nats = {Sn/log(2):.2f} bits")
# Bekenstein minimum energy per nat at radius R equals 2kT_H when R=r_s
M=Msun; d=bh(M); print("hbar c/(2 pi r_s k T_H) =", hbar*c/(2*pi*d['rs'])/(k*d['T']))
# Hydrogen ionisation Boltzmann factor at 300 K and 5800 K
for T in (300,5800):
    x=13.6*eV/(k*T); print(f"H ionisation E/kT at {T} K = {x:.1f}; exp(-E/kT)=10^{-x/log(10):.1f}")
# Landauer at 300 K
print("kT ln2 at 300K (J):", k*300*log(2), " in eV:", k*300*log(2)/eV)
# de Sitter: H_L = H0 sqrt(Omega_L)
H0=67.4e3/3.0857e22; OL=0.685; HL=H0*sqrt(OL)
Rds=c/HL; Sds=pi*Rds**2/lp2; TdS=hbar*HL/(2*pi*k)
print(f"H_Lambda^-1 = {1/HL/yr/1e9:.2f} Gyr; de Sitter S = {Sds:.3g} nats; T_dS = {TdS:.3g} K")
print(f"kT_dS ln2 = {k*TdS*log(2):.3g} J per bit")
# time for CMB to cool to T_H(1 Msun) in Lambda-dominated expansion (approx, ignores matter era remainder)
TH=bh(Msun)['T']; print(f"T_H(1 Msun)={TH:.3g} K; ln(2.7255/T_H)={log(2.7255/TH):.2f}; t ~ {log(2.7255/TH)/HL/yr/1e9:.0f} Gyr after now")
print(f"mass with T_H = T_dS: {hbar*c**3/(8*pi*G*k*TdS)/Msun:.3g} Msun")
# energy per generation E. coli vs kT: ~1e10 ATP? not computed (cited elsewhere)
# alpha drift bound
print("alpha-dot/alpha bound (Rosenband 2008): (-1.6 +- 2.3)e-17 /yr")
