"""Referee check R4: is 'exactly one store at alpha=2' robust? Excess MSE of best K-store tracker for alpha near 2,
using the executor's own c3 machinery (imported unchanged)."""
import sys, json, numpy as np
sys.argv=[sys.argv[0],"2.0"]
sys.path.insert(0,"../SPECTRUM_MAP/checks")
import importlib.util
spec=importlib.util.spec_from_file_location("c3","../SPECTRUM_MAP/checks/c3_layers.py")
src=open("../SPECTRUM_MAP/checks/c3_layers.py").read().split("out={}")[0]   # functions only, no main loop
ns={}; exec(src,ns)
out={}
for alpha in (1.8,1.9,1.95,2.0,2.05,2.1,2.2):
    row={}
    for L in (2,4):
        ex=[max(ns["best_K"](alpha,L,K)[0],0.0) for K in (1,2,3)]
        Ks={f"psi{p:.0e}":int(np.argmin([p*x+K for K,x in zip((1,2,3),ex)]))+1 for p in (1e3,1e4,1e5)}
        row[f"L{L}"]=dict(rel_excess=[float(f"{x:.3g}") for x in ex],**Ks)
    out[str(alpha)]=row; print(alpha,json.dumps(row),flush=True)
json.dump(out,open("r4_near2.json","w"),indent=1)
