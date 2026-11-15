# PILOT part 2: fetch workflow files, parse cron & upstream (feasibility only)
import json, subprocess, re, base64, collections, random
def gh(path):
    r=subprocess.run(['gh','api',path],capture_output=True,text=True)
    return None if r.returncode else json.loads(r.stdout)
hits=json.load(open('pilot/search_hits.json'))
random.seed(1)
recs=[]
for q,v in hits.items():
    items=v['items'][:]; random.shuffle(items)
    for it in items[:35]:
        b=gh(f"repos/{it['repo']}/git/blobs/{it['sha']}")
        if not b: continue
        txt=base64.b64decode(b['content']).decode('utf8','replace')
        crons=re.findall(r"cron:\s*['\"]?([^'\"\n#]+)",txt)
        ups=sorted(set(re.findall(r"git\+https://github\.com/([\w.-]+/[\w.-]+?)(?:\.git)?(?:[@#\s\"']|$)",txt)))
        recs.append({'q':q,'repo':it['repo'],'path':it['path'],'crons':[c.strip() for c in crons],'git_upstreams':ups,'len':len(txt)})
json.dump(recs,open('pilot/files.json','w'),indent=1)
def per_week(c):
    f=c.split()
    if len(f)!=5: return None
    mi,h,dom,mon,dow=f
    def n(field,lo,hi):
        if field=='*': return hi-lo+1
        tot=0
        for part in field.split(','):
            step=1
            if '/' in part: part,step=part.split('/'); step=int(step)
            if part=='*': a,b=lo,hi
            elif '-' in part: a,b=map(int,part.split('-'))
            else:
                try: a=b=int(part)
                except: return None
            tot+=len(range(a,b+1,step))
        return tot
    try:
        m=n(mi,0,59); hh=n(h,0,23)
        if dom=='*' and dow=='*': d=7
        elif dom=='*': d=n(dow,0,6)
        elif dow=='*': d=7*n(dom,1,31)/30.44
        else: d=7
        mo=1 if mon=='*' else n(mon,1,12)/12
        return m*hh*d*mo
    except Exception: return None
dist=collections.Counter()
for r in recs:
    w=[per_week(c) for c in r['crons']]
    r['pw']=w
    tot=sum(x for x in w if x)
    dist[round(tot,2) if tot else 0]+=1
print('n files',len(recs))
print('runs/week distribution', sorted(dist.items()))
print('with cron', sum(1 for r in recs if r['crons']))
ups=collections.Counter(u for r in recs for u in r['git_upstreams'])
print('distinct git upstreams',len(ups)); print(ups.most_common(25))
