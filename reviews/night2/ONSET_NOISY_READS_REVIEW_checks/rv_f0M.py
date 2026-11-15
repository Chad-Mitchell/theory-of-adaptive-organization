# f_alpha(0) convergence in M (reviewer's own code), and C_alpha sensitivity
from rv_f import f_cond, g_alpha
for a in [1.5,2.5]:
    for M in [600,1200,2400,3600]:
        f0=f_cond(a,0.0,M=M)[0]; K=(2*a-1)/(a-1); D0=(a-1)**(1/a-1)*f0**(1/a)
        C=(K/D0)**((2*a-1)/(a-1))*(g_alpha(a)*(a-1)/a)**(a/(a-1))
        print(a,M,round(f0,6),round(C,4),round(C/a**(a/(a-1)),4))
