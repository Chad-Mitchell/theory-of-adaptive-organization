"""Independent re-derivation of SCALE_ENDS numbers (written by the independent referee; does not import or
copy theory/scale_ends_checks/). Route: Planck units for black holes, Page (2005, NJP 7:203, eqs 19-21)
per-species greybody coefficients, numerical integration of mass and entropy, Saha equation for atoms.
Run: nice -n 19 python3 physics_indep.py"""
import numpy as np
from math import pi, log, sqrt, exp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
# CODATA 2018 exact/recommended
hbar=1.054571817e-34; h=2*pi*hbar; c=299792458.0; G=6.67430e-11; kB=1.380649e-23; eV=1.602176634e-19
me=9.1093837015e-31; mp=1.67262192369e-27; Msun=1.98847e30; yr=365.25*86400; muB=9.2740100783e-24
mP=sqrt(hbar*c/G); tP=sqrt(hbar*G/c**5); TP=mP*c**2/kB; lP=sqrt(hbar*G/c**3)
out=[]
def p(*a): s=" ".join(str(x) for x in a); print(s); out.append(s)

p("== 1. ATOMIC END ==")
for T in (300.0,5800.0):
    x=13.598*eV/(kB*T); p(f"H ionisation: E/kT at {T:.0f} K = {x:.2f}; Boltzmann factor = 10^{-x/log(10):.1f}")
# Saha: x^2/(1-x) = (1/n)(2 pi me kT/h^2)^{3/2} exp(-E/kT)   (statistical-weight ratio g_ion*2/g_H = 1)
def saha(T,n):
    A=(2*pi*me*kB*T/h**2)**1.5/n*exp(-13.598*eV/(kB*T))
    return (-A+sqrt(A*A+4*A))/2 if A>1e-300 else sqrt(A)
def saha_log10(T,n):  # log10 ionised fraction for tiny values
    lnA=1.5*log(2*pi*me*kB*T/h**2)-log(n)-13.598*eV/(kB*T)
    return 0.5*lnA/log(10)
p(f"Saha ionised fraction, 300 K, n=2.4e25 m^-3 (1 bar): 10^{saha_log10(300,2.4e25):.1f}")
p(f"Saha ionised fraction, 5800 K, n=1e23 m^-3 (photosphere-like): {saha(5800,1e23):.2e}  (Boltzmann factor alone: 10^-11.8)")
# electronic excitation n=2 (10.2 eV, degeneracy ratio 4 relative to ground incl. spin): occupancy and entropy
for T in (300.0,):
    e=10.199*eV/(kB*T); lnp=log(4)-e; P2=exp(lnp)
    Hel=-P2*lnp+P2  # -p ln p - (1-p)ln(1-p) ~ p(-ln p +1) for 4 substates treated as one level (+p ln4 is inside lnp)
    p(f"n=2 occupancy at {T:.0f} K: 10^{lnp/log(10):.1f}; electronic-excitation entropy ~ p(1-ln p) = 10^{(lnp+log(1-lnp))/log(10):.1f} nats")
# hyperfine ground state (F=0 one state, F=1 three states; splitting 1420.405751 MHz)
dE=h*1420.405751e6
for T in (300.0,2.7255):
    w=np.array([1.0,3*exp(-dE/(kB*T))]); w/=w.sum(); H=-(w[0]*log(w[0])+w[1]*log(w[1]/3))
    p(f"hyperfine spin entropy at T={T} K: {H:.4f} nats (ln 4 = {log(4):.4f})")
# Sackur-Tetrode translational entropy per H atom, 300 K, 1 bar
n=1e5/(kB*300); lam=h/sqrt(2*pi*mp*kB*300); S_tr=log(1/(n*lam**3))+2.5
p(f"translational (Sackur-Tetrode) entropy per H atom, 300 K, 1 bar: {S_tr:.2f} nats")
# Atom as thermometer: I(speed; T) for T uniform on {300 K, 600 K}, Maxwell speed distribution
def maxwell(v,T): a=sqrt(kB*T/mp); return sqrt(2/pi)*v*v/a**3*np.exp(-v*v/(2*a*a))
v=np.linspace(1,2e4,200001); f1=maxwell(v,300); f2=maxwell(v,600); fm=0.5*(f1+f2)
I=0.5*np.trapezoid(f1*np.log(np.where(f1>0,f1/fm,1)),v)+0.5*np.trapezoid(f2*np.log(np.where(f2>0,f2/fm,1)),v)
p(f"I(atom speed; T) with T in {{300,600}} K equiprobable: {I:.3f} nats  (one atom is a weak thermometer)")
# Atom as magnetometer: I(hyperfine/Zeeman state ; B) for B in {0, 1 T} at 300 K (high-field electron spin, 2 states)
x=muB*1.0/(kB*300); pu=1/(1+exp(-2*x)); Hb=lambda q:-(q*log(q)+(1-q)*log(1-q))
p(f"I(electron spin; B in {{0,1 T}}) at 300 K: {Hb(0.5*0.5+0.5*pu)-0.5*Hb(0.5)-0.5*Hb(pu):.2e} nats (tiny but > 0)")
p("Landauer kT ln2 at 300 K:", f"{kB*300*log(2):.4e} J = {kB*300*log(2)/eV:.5f} eV")
# Proton Bekenstein
R=0.8409e-15; Sb=2*pi*R*mp*c/hbar; p(f"Bekenstein bound proton (R={R} m): {Sb:.2f} nats = {Sb/log(2):.2f} bits")

p("== 2. EIGEN THRESHOLD and BACTERIAL BUDGET ==")
for eps in (1e-2,1e-3,1e-4,1e-9):
    for sig in (2,10,100):
        pass
    p(f"eps={eps:g}: L_max = ln(sigma)/eps -> sigma=2: {log(2)/eps:.3g}, sigma=10: {log(10)/eps:.3g}, sigma=100: {log(100)/eps:.3g}")
for ATP in (2.7e10,0.9e10):
    for dG in (40e3,50e3,60e3):
        p(f"E_gen: {ATP:.1e} ATP x {dG/1e3:.0f} kJ/mol at 310 K = {ATP*dG/6.02214076e23/(kB*310):.2e} kT")

p("== 3. BLACK HOLES (Planck units) ==")
def bh(Mkg):
    M=Mkg/mP
    return dict(M_planck=M,S_nats=4*pi*M**2,T_K=TP/(8*pi*M),rs_m=2*M*lP)
for name,Mk in (("1 Msun",Msun),("Sgr A* 4.3e6 Msun",4.3e6*Msun),("1 kg",1.0)):
    d=bh(Mk); p(name, {k:f"{v:.4g}" for k,v in d.items()}, f"bits={d['S_nats']/log(2):.4g}")
M=Msun/mP; S=4*pi*M**2; T=1/(8*pi*M)
p(f"E/(kT_H S) = M/(T S) = {M/(T*S):.6f}  (Smarr: 2);  dM/(T dS) = {1/(T*8*pi*M):.6f} (first law: 1)")
p(f"Bekenstein bound at R=r_s: 2 pi R E = 2 pi (2M) M = {2*pi*2*M*M/S:.6f} x S_BH  (saturated)")
# Page 2005 eqs 19-21: dM/dt = -1e-5 M^-2 (8.1830 n_half + 3.3638 n1 + 0.3836 n2); dSrad/dt = 1e-3/M (3.3710, 1.2684, 0.1300)
coef={'gamma+grav':(0,1,1),'Page1976: 2 massless nu + gamma + grav':(2,1,1),'3 massless nu + gamma + grav':(3,1,1)}
def rates(n):
    a=1e-5*(8.1830*n[0]+3.3638*n[1]+0.3836*n[2]); s=1e-3*(3.3710*n[0]+1.2684*n[1]+0.1300*n[2]); return a,s
naive=1/(15360*pi)
p(f"naive Stefan-Boltzmann photons on horizon area (no greybody): alpha = {naive:.4e}")
for name,n in list(coef.items())+[('naive SB photons',None)]:
    a,s=(naive,None) if n is None else rates(n)
    t_ev=M**3/(3*a)*tP/yr
    # numerical integration check
    sol=solve_ivp(lambda t,y:[-a/y[0]**2],[0,0.999999*M**3/(3*a)],[M],rtol=1e-10,atol=1e-30*M)
    ratio=None
    if s is not None:
        ratio=s/(8*pi*M*a/M**2*1.0) # dSrad/dt / (-dSbh/dt); -dSbh/dt = 8 pi M a/M^2
        ratio=(s/M)/(8*pi*a/M)
        # Page time: Srad = ratio*(S0-Sbh) = Sbh -> Sbh/S0 = ratio/(1+ratio); M^3 linear in t -> t/t_ev = 1-(Sbh/S0)^{3/2}
        x=ratio/(1+ratio); tpage=1-x**1.5; thalf=1-0.5**1.5
        # Hawking power-limited read bandwidth today, nats/s
        bw=(s/M)/tP
        p(f"{name}: alpha={a:.4e}, t_ev = {t_ev:.4g} yr x (M/Msun)^3; Srad/|dSbh| = {ratio:.4f}; Page time = {tpage:.4f} t_ev; half-S-radiated = {thalf:.4f} t_ev; emitted entropy rate (1 Msun) = {bw:.0f} nats/s; ODE M(end)/M0={sol.y[0,-1]/M:.3e}")
    else:
        p(f"{name}: alpha={a:.4e}, t_ev = {t_ev:.4g} yr x (M/Msun)^3")
# massive neutrinos: mass below which kT_H > 0.05 eV; fraction of lifetime spent below it
Mnu=TP/(8*pi*(0.05*eV/kB))*mP
p(f"kT_H = 0.05 eV at M = {Mnu:.2e} kg = {Mnu/Msun:.2e} Msun; fraction of a 1 Msun lifetime spent below that mass = {(Mnu/Msun)**3:.1e} -> realistic 1 Msun lifetime = gamma+grav value")
# scrambling time
p(f"scrambling (hbar/2 pi k T_H) ln S, 1 Msun: {(1/(2*pi*T))*log(S)*tP*1e3:.3f} ms; Sgr A*: {(1/(2*pi/(8*pi*4.3e6*M)))*log(4*pi*(4.3e6*M)**2)*tP/3600:.2f} h")

p("== 4. COSMOLOGICAL HORIZON ==")
Mpc=3.0856775814913673e22
for H0,OL in ((67.4,0.685),(67.66,0.6889)):
    HL=H0*1e3/Mpc*sqrt(OL); Lam=3*HL**2/c**2
    S=3*pi/(Lam*lP**2)    # = pi (c/H)^2 / lP^2
    TdS=hbar*HL/(2*pi*kB)
    p(f"H0={H0}, OmegaL={OL}: 1/H_L={1/HL/yr/1e9:.2f} Gyr; S_dS = 3 pi/(Lambda lP^2) = {S:.3e} nats; T_dS = {TdS:.3e} K; kT_dS ln2 = {kB*TdS*log(2):.2e} J/bit")
open("physics_indep.out","w").write("\n".join(out)+"\n")
