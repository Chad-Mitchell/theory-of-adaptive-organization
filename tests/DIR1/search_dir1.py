#!/usr/bin/env python3
"""DIR1 retrieval (locked before any outcome retrieval).

For each cell in PREDICTIONS_DIR1.json: query OpenAlex with the locked string, filter and sort,
take the first `screen_depth` results in rank order, and fetch an abstract through the locked
fallback order. Writes the screening pool (with abstracts) OUTSIDE the repository, because
abstracts are publisher text, and writes a hash manifest inside it.

Usage: nice -n 19 python3 search_dir1.py <outdir>
"""
import hashlib, html, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAIL = "chad39@gmail.com"


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"GTAO-DIR1 (mailto:{MAIL})"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            if i == tries - 1:
                return {"_error": repr(e)}
            time.sleep(2 * (i + 1))


def inv_to_text(inv):
    if not inv:
        return ""
    pos = {}
    for w, idxs in inv.items():
        for i in idxs:
            pos[i] = w
    return " ".join(pos[i] for i in sorted(pos))


def clean(t):
    t = re.sub(r"<[^>]+>", " ", t or "")
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def abstract_for(work):
    doi = (work.get("doi") or "").replace("https://doi.org/", "")
    a = clean(inv_to_text(work.get("abstract_inverted_index")))
    if len(a) > 100:
        return a, "openalex"
    if doi:
        cr = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
        a = clean(cr.get("message", {}).get("abstract", "")) if "message" in cr else ""
        if len(a) > 100:
            return a, "crossref"
        ep = get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&resultType=core&query="
                 + urllib.parse.quote(f'DOI:"{doi}"'))
        res = ep.get("resultList", {}).get("result", []) if isinstance(ep, dict) else []
        a = clean(res[0].get("abstractText", "")) if res else ""
        if len(a) > 100:
            return a, "europepmc"
        ss = get("https://api.semanticscholar.org/graph/v1/paper/DOI:" + urllib.parse.quote(doi) + "?fields=abstract")
        a = clean(ss.get("abstract") or "") if isinstance(ss, dict) else ""
        if len(a) > 100:
            return a, "semanticscholar"
    return "", "none"


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    spec = json.loads((HERE / "PREDICTIONS_DIR1.json").read_text())
    s = spec["search"]
    pool = []
    for cell in spec["cells"]:
        url = ("https://api.openalex.org/works?search=" + urllib.parse.quote(cell["query"])
               + "&filter=" + s["filter"] + "&sort=" + s["sort"]
               + f"&per-page={s['screen_depth']}&mailto={MAIL}")
        d = get(url)
        raw = out / f"openalex_{cell['id']}.json"
        raw.write_text(json.dumps(d))
        for rank, w in enumerate(d.get("results", [])[: s["screen_depth"]], 1):
            a, src = abstract_for(w)
            pool.append({"cell": cell["id"], "class": cell["class"], "prediction": cell["prediction"], "rank": rank,
                         "openalex": w.get("id"), "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                         "title": clean(w.get("title") or ""), "year": w.get("publication_year"),
                         "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                         "abstract_source": src, "abstract": a})
            time.sleep(0.2)
    (out / "pool.json").write_text(json.dumps(pool, indent=1))
    man = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob("*.json"))}
    (HERE / "data").mkdir(exist_ok=True)
    (HERE / "data" / "POOL_SHA256.json").write_text(json.dumps({"retrieved": time.strftime("%Y-%m-%d %H:%M:%S %Z"), "files": man}, indent=1))
    (HERE / "data" / "pool_index.csv").write_text(
        "cell,rank,doi,year,abstract_source,title\n" + "\n".join(
            f'{p["cell"]},{p["rank"]},{p["doi"]},{p["year"]},{p["abstract_source"]},"{p["title"].replace(chr(34), chr(39))}"' for p in pool) + "\n")
    print(len(pool), "records")


if __name__ == "__main__":
    main()
