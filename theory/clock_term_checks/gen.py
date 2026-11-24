# Reviewer re-derivation: J = K w'^2/D + c f + w[ a (om-w')^2/f^2 + b D/f ]   (K = kap kT)
# a=1/3,b=1: time-averaged squared error (memo). a=1,b=2: error scored at the moment before the next read.
import sympy as sp
K,c,w,om,f,D,wp,a,b=sp.symbols('K c w omega f D wp a b',positive=True)
J=K*wp**2/D+c*f+w*(a*(om-wp)**2/f**2+b*D/f)
Dopt=sp.solve(sp.diff(J,D),D); Dopt=[d for d in Dopt if d.is_positive!=False][0]
J1=sp.simplify(J.subs(D,Dopt))
wpopt=sp.solve(sp.diff(J1,wp),wp)[0]
J2=sp.simplify(sp.expand(J1.subs(wp,wpopt)))
print('D*=',Dopt,' wp*=',sp.simplify(wpopt)); print('J(f)=',sp.factor(J2))
# J(f) = A f^-1/2 + B f  -> f*: 
A=sp.simplify(J2.coeff(f,1)); print('coef of f:',A)
