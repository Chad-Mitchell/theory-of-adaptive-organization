import json, urllib.request, urllib.parse
def get(doi):
    try:
        r = json.load(urllib.request.urlopen("https://api.crossref.org/works/"+urllib.parse.quote(doi), timeout=30))["message"]
        a = ", ".join(x.get("family", "") for x in r.get("author", [])[:4])
        return f"{doi} | {r.get('title',[''])[0]} | {a} | {r.get('container-title',[''])[0]} | {r.get('issued',{}).get('date-parts',[[None]])[0]}"
    except Exception as e: return f"{doi} | NOT RESOLVED ({e})"
def q(text):
    r = json.load(urllib.request.urlopen("https://api.crossref.org/works?rows=3&query.bibliographic="+urllib.parse.quote(text), timeout=30))["message"]["items"]
    return [f"{x.get('DOI')} | {x.get('title',[''])[0]} | {x.get('issued',{}).get('date-parts',[[None]])[0]}" for x in r]
for t in ["Janotta Gogolin Barrett Brunner limits on nonlocal correlations from the structure of the local state space",
          "Massar Patra information and communication in polygon theories",
          "Aharonov Vardi meaning of an individual Feynman path",
          "Lami Palazuelos Winter ultimate data hiding in quantum mechanics and beyond",
          "Kimura Nuida Imai distinguishability measures and entropies for general probabilistic theories"]:
    print("QUERY:", t); [print("   ", s) for s in q(t)]
for d in ["10.1088/1367-2630/13/6/063024", "10.1103/PhysRevA.89.052124", "10.1103/PhysRevD.21.2235",
          "10.1007/s00220-018-3154-4", "10.1016/S0034-4877(10)80044-8"]:
    print("DOI:", get(d))
