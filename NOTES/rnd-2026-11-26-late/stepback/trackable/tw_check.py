# TRACKABLE_WORLD paper checks (sympy). Model: hold-rule class (MEMORY_CHALLENGE.md:38) plus a record leak rate G.
import sympy as sp
T,c,k,w,s2,p,G=sp.symbols('T c k w sigma2 p Gamma',positive=True)
J0=c+k/T+w*s2*T/6                      # hold-rule cost per unit time (no leak)
Ts=sp.sqrt(6*k/(w*s2)); print('C1 T* check:',sp.simplify(sp.diff(J0,T).subs(T,Ts)), '| J* =',sp.simplify(J0.subs(T,Ts)))
lost=1-(1-sp.exp(-G*T))/(G*T)          # expected fraction of the interval with the record gone
J=J0+w*p*lost
print('C2 lost-fraction series in G*T:',sp.series(lost.subs(G,sp.Symbol('g')/T),sp.Symbol('g'),0,3))
# lower bound: lost >= min(G T/2 - (G T)^2/6, ...) ; use: for any T, J >= k/T + w p*lost(T) ; check J* grows without bound in G numerically
import math
def Jnum(Tv,Gv,cv=0.1,kv=1.0,wv=1.0,s2v=0.01,pv=1.0):
    x=Gv*Tv; L=1-(1-math.exp(-x))/x
    return cv+kv/Tv+wv*s2v*Tv/6+wv*pv*L
for Gv in [0,1e-3,1e-2,0.1,1,10,100]:
    best=min(Jnum(10**(e/200),max(Gv,1e-12)) for e in range(-800,800))
    print(f'C3 Gamma={Gv:g}: min_T J = {best:.4f}  (blind cost w p = 1.0) tracker viable: {best<1.0}')
# R4: J* finite iff sigma2 finite; J* -> c as sigma2 -> 0 (conserved coordinate is cheapest, R6 sufficiency)
Js=sp.simplify(J0.subs(T,Ts)); print('C4 limit sigma2->0:',sp.limit(Js,s2,0),'| sigma2->oo:',sp.limit(Js,s2,sp.oo))
# R8: zero-drift reserve walk is recurrent -> ruin a.s.; positive drift -> ruin prob <1. Gambler's-ruin check for +/-1 walk with up-prob q from R=5:
q=sp.Symbol('q',positive=True); R=5
psi=lambda qq: 1 if qq<=sp.Rational(1,2) else (( (1-qq)/qq )**R)
print('C5 infinite-horizon ruin prob from R=5: q=1/2 ->',psi(sp.Rational(1,2)),'; q=0.55 ->',float(psi(sp.Rational(11,20))),'; q=0.6 ->',float(psi(sp.Rational(3,5))))
