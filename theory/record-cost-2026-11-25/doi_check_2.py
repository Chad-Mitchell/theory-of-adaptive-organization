"""Crossref check for the DOIs cited in theory/RECORD_COST_ROUNDS4-9_2026-11-25.md (same method as doi_check.py)."""
import json, urllib.request, sys, time
dois = """10.1007/BF01378063
10.1007/BF01475864
10.1038/nature10123
10.1038/ncomms2665
10.1038/ncomms2821
10.1038/nnano.2015.250
10.1063/1.4818538
10.1073/pnas.1204263109
10.1088/1367-2630/12/3/033023
10.1088/1367-2630/12/3/033024
10.1088/1367-2630/16/12/123029
10.1088/1367-2630/18/2/023049
10.1090/S0273-0979-03-00992-3
10.1103/PhysRevA.81.062348
10.1103/PhysRevD.27.2885
10.1103/PhysRevD.44.3197
10.1103/PhysRevD.92.045033
10.1103/PhysRevE.88.062128
10.1103/PhysRevE.92.062125
10.1103/PhysRevLett.104.080402
10.1103/PhysRevLett.108.130401
10.1103/PhysRevLett.109.120604
10.1103/PhysRevLett.112.090601
10.1103/PhysRevLett.99.240501
10.1103/PhysRevX.3.041003
10.1103/PhysRevX.6.021036
10.1103/RevModPhys.79.555
10.1112/S002557931100132X
10.1147/rd.176.0525
10.1147/rd.53.0183
10.1209/0295-5075/101/60001
10.1209/0295-5075/95/40004
10.2307/1968975""".split()
out=[]
for d in dois:
    try:
        r=json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/"+d,headers={"User-Agent":"gtao-doi-check (mailto:none)"}),timeout=30))["message"]
        a=", ".join((x.get("family","")) for x in r.get("author",[])[:4])
        y=(r.get("issued",{}).get("date-parts",[[None]])[0][0])
        out.append(f"OK  {d} | {y} | {a} | {r.get('title',[''])[0]} | {r.get('container-title',[''])[0]} {r.get('volume','')}:{r.get('page',r.get('article-number',''))}")
    except Exception as e:
        out.append(f"ERR {d} {e}")
    time.sleep(1.0)
r=json.load(urllib.request.urlopen("https://api.datacite.org/dois/10.48550/arXiv.quant-ph/0101012",timeout=30))["data"]["attributes"]
out.append(f"DATACITE 10.48550/arXiv.quant-ph/0101012 | {r['publicationYear']} | {r['creators'][0]['name']} | {r['titles'][0]['title']}")
print("\n".join(out))
