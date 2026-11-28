# PILOT part 3: run-history availability (feasibility only)
import json, subprocess, random, datetime as dt
def gh(path):
    r=subprocess.run(['gh','api',path],capture_output=True,text=True)
    return None if r.returncode else json.loads(r.stdout)
recs=[r for r in json.load(open('pilot/files.json')) if r['crons']]
random.seed(2); random.shuffle(recs)
out=[]
for r in recs[:12]:
    wf=r['path'].split('/')[-1]
    s=gh(f"repos/{r['repo']}/actions/workflows/{wf}")
    runs=gh(f"repos/{r['repo']}/actions/workflows/{wf}/runs?per_page=100&event=schedule")
    allr=gh(f"repos/{r['repo']}/actions/workflows/{wf}/runs?per_page=1")
    if not runs: out.append((r['repo'],wf,'ERR')); continue
    rr=runs['workflow_runs']
    dates=[x['created_at'] for x in rr]
    concl=[x['conclusion'] for x in rr]
    out.append(dict(repo=r['repo'],wf=wf,state=(s or {}).get('state'),crons=r['crons'],sched_total=runs['total_count'],all_total=(allr or {}).get('total_count'),
        newest=dates[0] if dates else None, oldest_in_page=dates[-1] if dates else None, fail=sum(c=='failure' for c in concl), n=len(concl)))
for o in out: print(o)
json.dump(out,open('pilot/runs_probe.json','w'),indent=1)
