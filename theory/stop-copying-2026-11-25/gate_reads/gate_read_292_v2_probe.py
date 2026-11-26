# Gate reader v2 probes: function-level only. No minimize() call, no T1/T2 search.
import sys, time, os; sys.path.insert(0,'.')
import numpy as np
import run_t2 as R2, run_t1 as R1
c=R2.C_SYM[(10,1)]
x=R2.pack(np.full(8,5.0),np.full(8,c),np.full(8,c))
rng=np.random.default_rng(0)
xa=x+np.r_[np.zeros(8),rng.normal(0,1e-7,16)]; xb=x+np.r_[np.zeros(8),rng.normal(0,1e-7,16)]
Aa,oa,_=R2.edge_A(xa); Ab,ob,_=R2.edge_A(xb)
print('uniform+1e-7 noise: max A_e', max(Aa), max(Ab), 'orients a', oa, 'b', ob)
print('dihedral_match on two numerically reciprocal designs:', R2.dihedral_match(Aa,oa,Ab,ob))
print('A5', R2.a5(Aa), 'label', R2.classify_A5(R2.a5(Aa)))
# timing of one Jtot eval (T2) and T1
t=time.process_time(); n=300
for _ in range(n): R2.Jtot(x,10,1)
e2=(time.process_time()-t)/n
t=time.process_time()
for _ in range(2000): R1.Jtot(np.array([5,0.73,5,0.73]),10,1)
e1=(time.process_time()-t)/2000
print('T2 Jtot eval %.3f ms; one FD gradient (25 evals) %.1f ms'%(e2*1e3,25*e2*1e3))
print('T2: 576 starts x 100 iters x ~1.2 grads -> %.0f CPU-min (cap 12)'%(576*100*1.2*25*e2/60))
print('T2: default maxfun 15000 evals per start -> %.0f iterations max; %.1f CPU-s per start at maxfun'%(15000/25,15000*e2))
print('T1 Jtot eval %.3f ms; 260 starts x 100 iters x 1.2 x 5 evals -> %.1f CPU-min'%(e1*1e3,260*100*1.2*5*e1/60))
# relative vs absolute closeness
for J in [0.0715,0.1846,0.9295,2.7517]: print('J',J,'script window',1e-6*max(1,J),'relative window',1e-6*J)
try:
    from threadpoolctl import threadpool_info; print('threads', [(d['internal_api'],d['num_threads']) for d in threadpool_info()])
except Exception as ex: print('threadpoolctl n/a', ex)
