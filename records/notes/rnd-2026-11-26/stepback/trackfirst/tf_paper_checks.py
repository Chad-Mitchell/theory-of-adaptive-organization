# TRACKING_FIRST paper checks (ELEMENTARY algebra; no route is run here).
import sympy as sp
kT,a,v,w,I,e=sp.symbols('kT a v w I epsilon',positive=True)
# OU class (CORE.md:90-91): heat infimum kT*a*(v-e)/e  =>  learning rate I(e)=a(v-e)/e  =>  e(I)=a v/(I+a)
eI=a*v/(I+a)
assert sp.simplify(a*(v-eI)/eI - I)==0
theta_task0=sp.simplify(-w*sp.diff(eI,I).subs(I,0))     # task's exchange rate (currency per nat) at zero information
print('OU: theta_task(0) =',theta_task0,'; x = theta_task(0)/kT =',sp.simplify(theta_task0/kT))
J=kT*I+w*eI
Istar=sp.solve(sp.diff(J,I),I)
Istar=[s for s in Istar if s.could_extract_minus_sign() is False or True]
print('OU: interior I* candidates =',Istar)
for s in Istar:
    Js=sp.simplify(J.subs(I,s))
    print('   J(I*) =',Js,'; equals 2sqrt(kT a v w)-kT a ?',sp.simplify(Js-(2*sp.sqrt(kT*a*v*w)-kT*a))==0)
    print('   marginal condition w|de/dI| at I* =',sp.simplify(-w*sp.diff(eI,I).subs(I,s)))
# Envelope (Shephard-type): dJ*/dkT = I*
Js=2*sp.sqrt(kT*a*v*w)-kT*a; s=sp.sqrt(a*v*w/kT)-a
print('OU: dJ*/dkT - I* =',sp.simplify(sp.diff(Js,kT)-s))
# Telegraph (CORE.md:74,94): heat infimum kT r L(e), L=(1-2e)ln((1-e)/e)
r=sp.symbols('r',positive=True)
L=(1-2*e)*sp.log((1-e)/e)
Jt=kT*r*L+w*e
print('Telegraph: dJ/de at e=1/2 =',sp.simplify(sp.limit(sp.diff(Jt,e),e,sp.Rational(1,2))))
print('Telegraph: dL/de at e=1/2 =',sp.limit(sp.diff(L,e),e,sp.Rational(1,2)))
