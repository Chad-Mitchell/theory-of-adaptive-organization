"""GITHUB-UPSTREAM data pull (public GitHub data only, read-only GET calls).
Stages (resumable, cached under data/):
  1 search  : sharded code search -> candidate workflow files
  2 blobs   : fetch file text, parse crons / git+ upstreams / checkout repos
  3 repos   : downstream repo metadata (+ commit count in window)
  4 runs    : scheduled runs in WINDOW for eligible workflows
  5 ups     : upstream repo metadata + default-branch commit count in WINDOW
"""
import json, os, re, subprocess, sys, time, base64, threading
from concurrent.futures import ThreadPoolExecutor
D=os.path.join(os.path.dirname(__file__),'..','data'); os.makedirs(D,exist_ok=True)
WINDOW=('2025-11-16','2026-11-14')   # 52 weeks, Sunday..Saturday
REFS_OK={'main','master','develop','dev','trunk','head','nightly','devel','development'}
lock=threading.Lock()

def gh(path, raw_headers=False, tries=40):
    for t in range(tries):
        cmd=['gh','api',path]+(['-i'] if raw_headers else [])
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode==0:
            if raw_headers: return r.stdout
            return json.loads(r.stdout) if r.stdout.strip() else None
        err=r.stderr
        if 'rate limit' in err.lower() or 'secondary' in err.lower() or '403' in err and 'limit' in err.lower():
            # POST-LOCK I/O FIX (declared): wait for the core reset instead of giving up; never mark a unit bad because of rate limiting
            try:
                rl=json.loads(subprocess.run(['gh','api','rate_limit'],capture_output=True,text=True).stdout)['resources']['core']
                wait=max(30,rl['reset']-time.time()+5) if rl['remaining']<50 else 30
            except Exception: wait=120
            print('rate-limited; sleeping',int(wait),flush=True); time.sleep(wait); continue
        if '404' in err or '410' in err or '409' in err or '451' in err: return {'_missing':err[:120]}
        time.sleep(5*(t+1))
    return {'_err':err[:200]}

def cache(name):
    p=os.path.join(D,name)
    return (json.load(open(p)) if os.path.exists(p) else {}), p

# ---------------- stage 1
SHARDS=['size:<1000','size:1000..1999','size:2000..2999','size:3000..3999','size:4000..4999',
        'size:5000..6499','size:6500..8499','size:8500..11999','size:12000..19999','size:>=20000']
BASEQ=['"git+https://github.com" cron path:.github/workflows extension:yml',
       '"git+https://github.com" cron path:.github/workflows extension:yaml']
def stage_search():
    hits,p=cache('search_hits.json')
    for bq in BASEQ:
        for sh in SHARDS:
            q=f'{bq} {sh}'
            if q in hits.get('_done',[]): continue
            for page in range(1,11):
                res=gh(f'search/code?q={subprocess.list2cmdline([q])[0:0]}'+'' ) if False else None
                r=subprocess.run(['gh','api','-X','GET','search/code','-f',f'q={q}','-f','per_page=100','-f',f'page={page}'],capture_output=True,text=True)
                if r.returncode:
                    if 'rate limit' in r.stderr.lower() or 'secondary' in r.stderr.lower():
                        time.sleep(65); r=subprocess.run(['gh','api','-X','GET','search/code','-f',f'q={q}','-f','per_page=100','-f',f'page={page}'],capture_output=True,text=True)
                    if r.returncode: print('search err',q,page,r.stderr[:150],flush=True); break
                res=json.loads(r.stdout); items=res.get('items',[])
                for it in items:
                    k=it['repository']['full_name']+'::'+it['path']
                    hits[k]={'repo':it['repository']['full_name'],'path':it['path'],'sha':it['sha'],'fork':it['repository'].get('fork')}
                print(q,page,res.get('total_count'),len(items),'uniq',len([k for k in hits if k!='_done']),flush=True)
                time.sleep(6.5)
                if len(items)<100: break
            hits.setdefault('_done',[]).append(q); json.dump(hits,open(p,'w'))

# ---------------- stage 2
def parse(txt, repo):
    crons=[c.strip() for c in re.findall(r"cron:\s*['\"]?([^'\"\n#]+)",txt)]
    ups=[]
    for m in re.finditer(r"git\+https://github\.com/([\w.-]+)/([\w.-]+?)(?:\.git)?(@[\w./-]+)?(?=[\s\"'#&;)\]]|$|#egg|\\)",txt):
        owner,name,ref=m.group(1),m.group(2),(m.group(3) or '')[1:]
        if '$' in owner or '$' in name: continue
        ups.append({'up':f'{owner}/{name}'.lower(),'ref':ref})
    chk=set(x.strip().strip('\'"').lower() for x in re.findall(r"repository:\s*([\w.\-'\"]+/[\w.\-'\"]+)",txt))
    return {'crons':crons,'ups':ups,'checkouts':sorted(c for c in chk if '$' not in c and '{' not in c)}
def stage_blobs():
    hits,_=cache('search_hits.json'); files,p=cache('files.json')
    todo=[k for k in hits if k!='_done' and k not in files]
    print('blobs todo',len(todo),flush=True)
    def work(k):
        h=hits[k]; b=gh(f"repos/{h['repo']}/git/blobs/{h['sha']}")
        if not b or '_err' in b or '_missing' in b: rec={'_bad':True}
        else:
            txt=base64.b64decode(b['content']).decode('utf8','replace')
            rec=dict(h,**parse(txt,h['repo'])); rec['sha256_text']=__import__('hashlib').sha256(txt.encode()).hexdigest()
        with lock: files[k]=rec
    with ThreadPoolExecutor(4) as ex:
        for i,_ in enumerate(ex.map(work,todo)):
            if i%200==0:
                with lock: json.dump(files,open(p,'w'))
                print('blobs',i,flush=True)
    json.dump(files,open(p,'w'))

# cron -> nominal runs per week
def per_week(c):
    f=c.split()
    if len(f)!=5: return None
    mi,h,dom,mon,dow=f
    DOW={'sun':0,'mon':1,'tue':2,'wed':3,'thu':4,'fri':5,'sat':6}
    def n(field,lo,hi):
        if field=='*': return hi-lo+1
        tot=set()
        for part in field.split(','):
            step=1
            if '/' in part: part,s=part.split('/'); step=int(s)
            part=part.lower()
            for k,v in DOW.items(): part=part.replace(k,str(v))
            if part=='*': a,b=lo,hi
            elif '-' in part: a,b=map(int,part.split('-'))
            else: a=int(part); b=a if step==1 else hi
            tot.update(range(a,b+1,step))
        return len(tot)
    try:
        m=n(mi,0,59); hh=n(h,0,23)
        if dom=='*' and dow=='*': d=7.0
        elif dom=='*': d=float(n(dow.replace('7','0'),0,6))
        elif dow=='*': d=7*n(dom,1,31)/30.44
        else: d=7.0
        mo=1 if mon=='*' else n(mon,1,12)/12
        return m*hh*d*mo
    except Exception: return None

def classify(rec):
    """eligibility per PREREG §3"""
    owner=rec['repo'].split('/')[0].lower()
    ext=[u for u in rec['ups'] if u['up'].split('/')[0]!=owner]
    unpinned=[u for u in ext if (u['ref']=='' or u['ref'].lower() in REFS_OK)]
    pinned=[u for u in ext if not (u['ref']=='' or u['ref'].lower() in REFS_OK)]
    pw=[per_week(c) for c in rec['crons']]
    nom=sum(x for x in pw if x) if pw and all(x is not None for x in pw) else None
    ups_set={u['up'] for u in ext}
    members=[c for c in rec['checkouts'] if c!=rec['repo'].lower() and c not in ups_set]
    return {'ext_unpinned':sorted({u['up'] for u in unpinned}),'ext_pinned':sorted({u['up'] for u in pinned}-{u['up'] for u in unpinned}),
            'nominal_pw':nom,'n_members':len(set(members)),'members':sorted(set(members))}

# ---------------- stage 3
def link_count(path):
    out=gh(path,raw_headers=True)
    if not isinstance(out,str): return None
    head,_,body=out.partition('\r\n\r\n') if '\r\n\r\n' in out else out.partition('\n\n')
    m=re.search(r'[?&]page=(\d+)>; rel="last"',head)
    if m: return int(m.group(1))
    try: return len(json.loads(body))
    except Exception: return None
def stage_repos(keys):
    meta,p=cache('repos.json')
    todo=[r for r in keys if r not in meta]; print('repos todo',len(todo),flush=True)
    def work(r):
        j=gh(f'repos/{r}')
        if not j or '_err' in j or '_missing' in j: m={'_bad':True}
        else:
            m={k:j.get(k) for k in ['stargazers_count','forks_count','archived','fork','created_at','pushed_at','default_branch']}
            m['owner_type']=j['owner']['type']
            m['commits_window']=link_count(f"repos/{r}/commits?sha={j.get('default_branch')}&since={WINDOW[0]}T00:00:00Z&until={WINDOW[1]}T23:59:59Z&per_page=1")
        with lock: meta[r]=m
    with ThreadPoolExecutor(4) as ex:
        for i,_ in enumerate(ex.map(work,todo)):
            if i%200==0:
                with lock: json.dump(meta,open(p,'w'))
                print('repos',i,flush=True)
    json.dump(meta,open(p,'w'))

# ---------------- stage 4
def stage_runs(wfs):
    runs,p=cache('runs.json')
    todo=[k for k in wfs if k not in runs]; print('runs todo',len(todo),flush=True)
    def work(k):
        repo,path=k.split('::'); wf=path.split('/')[-1]
        st=gh(f'repos/{repo}/actions/workflows/{wf}')
        out={'state':(st or {}).get('state') if isinstance(st,dict) else None,'runs':[]}
        base=f'repos/{repo}/actions/workflows/{wf}/runs?event=schedule&created={WINDOW[0]}..{WINDOW[1]}&per_page=100'
        for page in range(1,9):
            j=gh(base+f'&page={page}')
            if not j or '_err' in j or '_missing' in j: out['err']=str(j)[:100]; break
            if page==1: out['total']=j.get('total_count')
            for x in j['workflow_runs']:
                out['runs'].append([x['created_at'],x['conclusion'],x['head_sha'][:10],x.get('run_started_at'),x.get('updated_at')])
            if len(j['workflow_runs'])<100: break
        allr=gh(f'repos/{repo}/actions/workflows/{wf}/runs?created={WINDOW[0]}..{WINDOW[1]}&per_page=1')
        out['total_all_events']=allr.get('total_count') if isinstance(allr,dict) else None
        with lock: runs[k]=out
    with ThreadPoolExecutor(4) as ex:
        for i,_ in enumerate(ex.map(work,todo)):
            if i%100==0:
                with lock: json.dump(runs,open(p,'w'))
                print('runs',i,flush=True)
    json.dump(runs,open(p,'w'))

if __name__=='__main__':
    st=sys.argv[1]
    if st=='search': stage_search()
    elif st=='blobs': stage_blobs()
    elif st in ('repos','runs','ups'):
        files,_=cache('files.json')
        el={}
        for k,r in files.items():
            if r.get('_bad') or r.get('fork'): continue
            c=classify(r); 
            if not r['crons']: continue
            el[k]=(r,c)
        if st=='repos':
            stage_repos(sorted({r['repo'] for r,c in el.values() if c['ext_unpinned'] or c['ext_pinned']}))
        elif st=='runs':
            ok=[k for k,(r,c) in el.items() if (c['ext_unpinned'] or c['ext_pinned']) and c['nominal_pw'] and 1<=c['nominal_pw']<=168]
            stage_runs(sorted(ok))
        else:
            ups=sorted({u for r,c in el.values() for u in c['ext_unpinned']})
            meta,p=cache('upstreams.json'); todo=[u for u in ups if u not in meta]
            print('ups todo',len(todo),flush=True)
            def work(u):
                j=gh(f'repos/{u}')
                if not j or '_err' in j or '_missing' in j: m={'_bad':True}
                else:
                    m={'stars':j.get('stargazers_count'),'default_branch':j.get('default_branch'),'full_name':j.get('full_name'),'archived':j.get('archived')}
                    m['commits_window']=link_count(f"repos/{u}/commits?sha={j.get('default_branch')}&since={WINDOW[0]}T00:00:00Z&until={WINDOW[1]}T23:59:59Z&per_page=1")
                with lock: meta[u]=m
            with ThreadPoolExecutor(4) as ex: list(ex.map(work,todo))
            json.dump(meta,open(p,'w'))
