import json, urllib.request, urllib.parse
dois = ["10.1016/S0034-4877(10)00025-X", "10.1016/j.physrep.2023.09.001", "10.1063/1.3615729", "10.1088/1367-2630/13/6/063024",
        "10.1017/CBO9781139003858", "10.1214/aoms/1177729032", "10.1103/PhysRevA.75.032304",
        "10.1103/PhysRevA.84.012311"]
for d in dois:
    try:
        r = json.load(urllib.request.urlopen("https://api.crossref.org/works/" + urllib.parse.quote(d), timeout=30))["message"]
        au = "; ".join((a.get("family", "") for a in r.get("author", [])[:4]))
        print("OK ", d, "|", r.get("title", [""])[0], "|", au, "|", (r.get("container-title") or [""])[0], "|",
              r.get("volume", ""), r.get("page", ""), "|", r.get("issued", {}).get("date-parts", [[None]])[0][0])
    except Exception as e:
        print("FAIL", d, e)
