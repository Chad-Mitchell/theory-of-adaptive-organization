import json,sys
for lab,fn,n in [('V1','../stepback/c1/c1_greedy_v0_c3_n200.json',120),('V2','../stepback/c1/c1_greedy_v1_c3_n200.json',123),('V3','../stepback/c1/c1_greedy_v2_c3_n200.json',124),('NN mu=-2','rv_mu2.json',128)]:
    d=json.load(open(fn)); S=set(tuple(p) for p in d['sel'][:n]); T={(0,0),(1,0),(0,1),(1,1)}
    print(lab, n)
    for y in range(10,-10,-1): print(''.join('T' if (x,y) in T else ('#' if (x,y) in S else '.') for x in range(-10,12)))
