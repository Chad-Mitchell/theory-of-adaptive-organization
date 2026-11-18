# P5 EXPLORATORY (unblinded). Coder 1 = Ace manual rubric; coder 2 = deterministic keyword rule.
import json,re,collections
E=[json.loads(l) for l in open('<private-app-repo>/archive/pre-graph-29cf8e4/Chad.jsonl')]
recs={i+1:e for i,e in enumerate(E) if e.get('type') in ('mistake','correction')}
manual={186:'N',189:'R',190:'R',308:'J',309:'J',315:'S',326:'S',329:'P',343:'R',344:'R',362:'S',410:'S',421:'S',425:'P',444:'S',447:'S',458:'S',464:'S',466:'S',482:'T',493:'S',494:'N',495:'N',499:'T',500:'C',512:'J',513:'J',535:'N',568:'J',571:'C',598:'J',646:'X',669:'T',679:'X',706:'T',709:'S',710:'T',727:'S',741:'T',748:'S',768:'T',775:'T',848:'T',2295:'T',2342:'T',2519:'J',2520:'J',2521:'J',2522:'S',2637:'S',2638:'J',2676:'X',2686:'J',2759:'X',2842:'J',2868:'T'}
def kw(t):
    t=t.lower()
    if re.search(r'supersed|steer|privacy|do not name',t) and not re.search(r'mistake',t): return 'X'
    if re.search(r'forgot|settled fact|standing .*rule',t): return 'C'
    if re.search(r'never logged|not logged|did not log|never given a reading|log append skipped|not .*logged live',t): return 'N'
    if re.search(r'brief omitted|omitted a waiting',t): return 'R'
    if re.search(r'would go first|before actually|never changed the',t): return 'P'
    if re.search(r'without (first )?checking|from memory|out-of-date|stale|relic|was left in|did not update|showed the oct|before saying|look(ed)? again|check the phone tools|still marked|no longer on|current status',t): return 'S'
    if re.search(r'\bbug\b|fixed:|git add|duplicate|verbatim|does not read|tagged|setup gap|failed',t): return 'T'
    return 'J'
c1=[];c2=[]
for k,e in recs.items(): c1.append(manual[k]); c2.append(kw(e['text']))
cats=sorted(set(c1)|set(c2)); n=len(c1)
po=sum(a==b for a,b in zip(c1,c2))/n
pe=sum((c1.count(c)/n)*(c2.count(c)/n) for c in cats)
kappa=(po-pe)/(1-pe)
m1=collections.Counter(c1); m2=collections.Counter(c2)
misses=[c for c in c1 if c!='X']
mem=[c for c in misses if c in 'SNCRP']
out=dict(records=n,excluded_not_miss=m1['X'],misses=len(misses),coder1=dict(m1),coder2=dict(m2),agreement=po,kappa=kappa,
 memory_caused=len(mem),S_plus_C=sum(c in 'SC' for c in misses),share_S_plus_C_of_memory=sum(c in 'SC' for c in mem)/len(mem),share_S_plus_C_of_all=sum(c in 'SC' for c in misses)/len(misses),
 S_plus_C_coder2=sum(c in 'SC' for c in c2 if c!='X'),misses_coder2=sum(c!='X' for c in c2))
print(json.dumps(out,indent=1)); json.dump(out,open('p5.json','w'),indent=1)
