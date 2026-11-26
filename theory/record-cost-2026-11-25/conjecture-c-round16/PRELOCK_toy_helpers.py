# Pre-lock toy test of the Round 16 helpers (elt, key, fmul, tofloat), run before the lock on toy numbers only (not on the
# icosahedron/dodecahedron data). Run from this directory. Output: PRELOCK_toy_helpers.stdout.
import sympy as sp
src=open('r16_h3_canonical.py').read().split('\n')
s5=sp.sqrt(5)
blk='\n'.join(src[27:36]); exec(blk)
toyA=[[sp.radsimp((1+s5)**2), 6+2*s5],[sp.radsimp(1/(3-s5)), sp.Rational(1,2)]]
toyB=[[(3+s5)/4, sp.Integer(2)],[sp.Integer(1), sp.radsimp(2/(1+s5))]]
CA=[[elt(x) for x in r] for r in toyA]; CB=[[elt(x) for x in r] for r in toyB]
print("toy per-factor classes:", len({key(x) for r in CA for x in r}), len({key(x) for r in CB for x in r}))
vals={}
for a in [x for r in CA for x in r]:
    for b in [x for r in CB for x in r]:
        p=fmul(a,b); vals.setdefault(key(p),(len(vals),p))[0]
num=sorted(tofloat(p) for _,p in vals.values())
print("toy products distinct:", len(vals), "min gap:", min(b-a for a,b in zip(num,num[1:])))
chk=sorted(set(round(float(x*y),9) for x in [x for r in toyA for x in r] for y in [y for r in toyB for y in r]))
print("float check distinct:", len(chk))
