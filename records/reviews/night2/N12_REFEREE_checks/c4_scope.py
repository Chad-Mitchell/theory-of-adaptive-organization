"""N12 referee, check 4: what N12 does NOT cover. Finite rho, constants, vigilance growth, mixed technologies,
precision-unit vigilance, integer N. Uses the power class only through phi = k p^(1-a) W^a q^b (Lemma 1(vi))."""
import math, sympy as sp

def ab(tech, al, th=1.0):
    if tech == "reset": return 1/al, 1/al
    D = al*(th+1)-1; return al*th/D, th/D

def Nstar(r, a, b): return (r**b/((1+r)**b-1))**(1/(1-a))

print("== A. finite-rho local onset slope and fitted slope over rho in [0.01, 1] (h=0, equal prices) ==")
for tech, th in [("reset",1),("prec",1),("prec",2)]:
    for al in (1.2, 1.5, 2, 2.5, 2.9):
        a,b = ab(tech, al, th)
        rs = [10**(-k/4) for k in range(0, 9)]
        xs=[math.log(r) for r in rs]; ys=[math.log(Nstar(r,a,b)) for r in rs]
        mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
        fit=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
        loc = lambda r: (b/(1-a))*(1-r*(1+r)**(b-1)/((1+r)**b-1))
        print(f" {tech:5} th={th} alpha={al}: e_g(1)={loc(1):+.3f} e_g(0.1)={loc(.1):+.3f} fit[0.01,1]={fit:+.3f}  Pi*=b^(-1/(1-a))={b**(-1/(1-a)):.3f}  N*(0.1)={Nstar(.1,a,b):.1f} ceil {math.ceil(Nstar(.1,a,b))}")

print("\n== B. vigilance growth beyond onset V(N) ∝ N^a (THEOREMS T5.5): exponent a in spend units, a/theta in precision units ==")
for al in (1.5, 2, 2.5):
    print(f" alpha={al}: reset a={ab('reset',al)[0]:.3f};  prec th=1 a={ab('prec',al,1)[0]:.3f};  prec th=2 a={ab('prec',al,2)[0]:.3f} (precision units {ab('prec',al,2)[0]/2:.3f})")

print("\n== C. small-share onset vigilance value V(N*) = b^(-a/(1-a)) rho^((b-a)/(1-a)) (T5.3) ==")
for al in (1.5, 2, 2.5, 3):
    a,b=ab('reset',al); print(f" reset alpha={al}: V(N*) = {b**(-a/(1-a)):.3f} (rho-free; value moves with alpha)")

print("\n== D. mixed technologies (T1.8): e_g = -(1-b_L)/(1-a_L), e_u = +(1-b_m)/(1-a_L) ==")
al,th=sp.symbols('alpha theta',positive=True); D=al*(th+1)-1
aP,bP=al*th/D, th/D; aR=bR=1/al
for name,(aL,bL),(am,bm) in [("prec level / reset members",(aP,bP),(aR,bR)),("reset level / prec members",(aR,bR),(aP,bP))]:
    print(f" {name}: e_g = {sp.simplify(-(1-bL)/(1-aL))};  e_u = {sp.factor(sp.simplify((1-bm)/(1-aL)))}")

print("\n== E. same-alpha premise (analytic note, numerics in c2 mixed rows and c5) ==")
print(" Flat member's marginal error from adding S_g: (1/pi) Int S_g(w) r/(r+S_u(w)) dw; near w->0 the integrand ~ q_g r w^(alpha_u-alpha_g)/q_u,")
print(" finite iff alpha_g - alpha_u < 1. Then the flat gain is linear in q_g and d ln N*/d ln q_g -> -(1+theta) at fixed q_u;")
print(" at alpha_g - alpha_u >= 1 the gain is sub-linear in q_g and the exponent changes (c5).")
