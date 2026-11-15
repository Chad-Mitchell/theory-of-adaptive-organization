import json, urllib.request, urllib.parse, sys
dois = ["10.1214/aos/1176349936", "10.1214/aos/1176324317", "10.1111/j.1468-0262.2005.00616.x", "10.1103/PhysRevE.49.1685",
        "10.1109/18.650984", "10.1111/j.1467-9892.1982.tb00349.x", "10.1109/5.18626", "10.1016/0166-5316(93)90035-S",
        "10.1103/PhysRevE.47.992", "10.1093/biomet/74.1.95", "10.1016/S0378-4371(01)00144-3"]
for doi in dois:
    try:
        d = json.load(urllib.request.urlopen("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi, safe="/"), timeout=30))
    except Exception as e:
        print("##", doi, "ERR", e); continue
    ab = d.get("abstract_inverted_index") or {}
    pos = {p: w for w, l in ab.items() for p in l}
    txt = " ".join(pos[i] for i in sorted(pos))
    src = (d.get("primary_location") or {}).get("source") or {}
    print("##", doi, "|", d.get("title"), "|", d.get("publication_year"), "|", src.get("display_name"), "|",
          [a["author"]["display_name"] for a in d.get("authorships", [])][:4])
    print("ABSTRACT:", txt[:1000] if txt else "(none in OpenAlex)")
