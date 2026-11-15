# PILOT (feasibility only; no outcome relations computed). Declared in PREREG.
import json, subprocess, time, re, base64, sys, os
def gh(path, params=None):
    cmd=['gh','api','-X','GET',path]
    for k,v in (params or {}).items(): cmd+=['-f',f'{k}={v}']
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: return {'_err':r.stderr[:300]}
    return json.loads(r.stdout)
Q=[ 'scientific-python-nightly-wheels path:.github/workflows',
    '"pip install git+https://github.com" cron path:.github/workflows',
    '"3.x-dev" cron path:.github/workflows',
    '"toolchain: nightly" cron path:.github/workflows']
out={}
for q in Q:
    res=gh('search/code',{'q':q,'per_page':'100','page':'1'})
    out[q]={'total':res.get('total_count'),'items':[{'repo':i['repository']['full_name'],'path':i['path'],'sha':i['sha']} for i in res.get('items',[])], 'err':res.get('_err')}
    print(q, res.get('total_count'), len(out[q]['items']), res.get('_err'), flush=True)
    time.sleep(7)
json.dump(out,open('pilot/search_hits.json','w'),indent=1)
