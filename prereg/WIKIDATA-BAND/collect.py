"""Data collection (read-only public APIs). Usage: python collect.py <tag> <seed> <n_per_prop> [exclude_json]
Writes raw/<tag>_items.json, raw/<tag>_pages.json. All responses cached in raw/cache (sha256-keyed)."""
import sys, json, random, os, time, datetime, re, urllib.parse
import wm
from props import PROPS, WIKIS, T0
SITES = [w + "wiki" for w in WIKIS]
LANGS = WIKIS + ["mul"]
CLAIM_ACTS = ("wbcreateclaim", "wbsetclaim-", "wbsetclaimvalue", "wbremoveclaims")

def chunks(x, n):
    for i in range(0, len(x), n): yield x[i:i + n]

def sample_prop(pid, seed, n, exclude):
    q = f"SELECT ?item ?sl WHERE {{ SERVICE bd:sample {{ ?item wdt:{pid} ?v . bd:serviceParam bd:sample.limit 3000 . bd:serviceParam bd:sample.seed {seed} }} ?item wikibase:sitelinks ?sl . }}"
    b = wm.sparql(q)["results"]["bindings"]
    cand = sorted({x["item"]["value"].rsplit("/", 1)[1] for x in b if int(x["sl"]["value"]) >= 1} - set(exclude))
    random.Random(f"{seed}-{pid}").shuffle(cand)
    out = []
    for ch in chunks(cand, 50):
        r = wm.api("www.wikidata.org", action="wbgetentities", ids="|".join(ch), props="sitelinks", sitefilter="|".join(SITES))
        for qid in ch:
            sl = r.get("entities", {}).get(qid, {}).get("sitelinks", {})
            if sl: out.append({"qid": qid, "pages": {k[:-4]: v["title"] for k, v in sl.items()}})
            if len(out) >= n: return out, len(cand)
    return out, len(cand)

def entity_now(qids):
    res = {}
    for ch in chunks(qids, 10):
        r = wm.api("www.wikidata.org", action="wbgetentities", ids="|".join(ch), props="claims|sitelinks")
        for qid, e in r.get("entities", {}).items(): res[qid] = e
    return res

def entity_old(qid):
    r = wm.api("www.wikidata.org", action="query", prop="revisions", titles=qid, rvstart=T0, rvdir="older", rvlimit=1, rvprop="ids|timestamp")
    pg = r["query"]["pages"][0]
    if "revisions" not in pg: return None
    rev = pg["revisions"][0]
    e = wm.get(f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json", {"revision": rev["revid"]})
    if not isinstance(e, dict) or "entities" not in e: return None
    ent = next(iter(e["entities"].values()))
    return {"revid": rev["revid"], "ts": rev["timestamp"], "claims": ent.get("claims", {})}

def comments(qid, pid, max_pages=6):
    n_all = n_p = 0; params = dict(action="query", prop="revisions", titles=qid, rvprop="timestamp|comment", rvend=T0, rvlimit=500)
    pat = f"[[Property:{pid}]]"
    for _ in range(max_pages):
        r = wm.api("www.wikidata.org", **params)
        pg = r["query"]["pages"][0]
        for rv in pg.get("revisions", []):
            c = rv.get("comment", ""); n_all += 1
            if pat in c and any(a in c for a in CLAIM_ACTS): n_p += 1
        if "continue" in r: params.update(r["continue"])
        else: return n_all, n_p, True
    return n_all, n_p, False

def fetch_page(host, tt):
    """Section 0 of the current rendered Parsoid HTML (REST, CDN-served), plus the wikitext of named parameters of
    infobox-like templates (>= 5 named params) read from Parsoid's data-mw. Only section 0 is stored."""
    import hashlib, lxml.html
    key = hashlib.sha256((host + tt).encode()).hexdigest(); p = os.path.join(wm.CACHE, "pg2", key + ".json")
    if os.path.exists(p): return tuple(json.load(open(p)))
    h = wm.raw(f"https://{host}/api/rest_v1/page/html/{tt}")
    m = re.search(r'<section data-mw-section-id="0".*?</section>', h or "", re.S)
    h0 = m.group(0) if m else ""
    params = []
    if h0:
        try: doc = lxml.html.fromstring(h0)
        except Exception: doc = None
        for el in (doc.xpath("//*[@data-mw]") if doc is not None else []):
            try: j = json.loads(el.get("data-mw"))
            except Exception: continue
            for part in j.get("parts", []):
                if isinstance(part, dict) and "template" in part:
                    pr = part["template"].get("params", {})
                    named = [v.get("wt", "") for k, v in pr.items() if not k.isdigit()]
                    if len(named) >= 5: params.extend(named)
    w0 = "\n".join(params)
    os.makedirs(os.path.dirname(p), exist_ok=True); json.dump([h0, w0], open(p, "w"))
    return h0, w0

def stage_sample(tag, seed, n, exclude):
    t1 = datetime.datetime.now(datetime.timezone.utc).isoformat()
    items = []; meta = {"tag": tag, "seed": seed, "n": n, "t1": t1, "T0": T0, "frame": {}}
    for pid, lab, dom, dt in PROPS:
        s, ncand = sample_prop(pid, seed, n, exclude); meta["frame"][pid] = ncand
        for x in s: x.update(pid=pid, domain=dom, datatype=dt)
        items += s; print(pid, len(s), "of", ncand, flush=True)
    now = entity_now(sorted({x["qid"] for x in items}))
    for x in items:
        e = now.get(x["qid"], {})
        x["claims_now"] = e.get("claims", {}).get(x["pid"], [])
        x["sitelinks_wiki"] = sum(1 for k in e.get("sitelinks", {}) if k.endswith("wiki") and k not in ("commonswiki", "specieswiki", "metawiki", "mediawikiwiki", "wikidatawiki", "sourceswiki", "outreachwiki", "wikimaniawiki", "foundationwiki", "incubatorwiki"))
    json.dump({"meta": meta, "items": items}, open(f"raw/{tag}_sample.json", "w")); print("sample done", len(items), flush=True)

def stage_old(tag):
    D = json.load(open(f"raw/{tag}_sample.json"))
    for i, x in enumerate(D["items"]):
        o = entity_old(x["qid"])
        x["old"] = None if o is None else {"revid": o["revid"], "ts": o["ts"], "claims": o["claims"].get(x["pid"], [])}
        x["comments"] = None
        if i % 50 == 0: print("old", i, flush=True)
    tq = set()
    for x in D["items"]:
        for c in x["claims_now"] + ((x["old"] or {}).get("claims") or []):
            dv = c.get("mainsnak", {}).get("datavalue", {})
            if dv.get("type") == "wikibase-entityid": tq.add(dv["value"]["id"])
    labels = {}
    for ch in chunks(sorted(tq), 50):
        r = wm.api("www.wikidata.org", action="wbgetentities", ids="|".join(ch), props="labels|aliases|sitelinks", languages="|".join(LANGS), sitefilter="|".join(SITES))
        for qid, e in r.get("entities", {}).items():
            labels[qid] = {"labels": {k: v["value"] for k, v in e.get("labels", {}).items()},
                           "aliases": {k: [a["value"] for a in v] for k, v in e.get("aliases", {}).items()},
                           "sitelinks": {k[:-4]: v["title"] for k, v in e.get("sitelinks", {}).items()}}
    D["labels"] = labels
    json.dump(D, open(f"raw/{tag}_items.json", "w")); print("old+labels done", flush=True)

def stage_pages(tag, html_n=0):
    """Batched: entity usage + current wikitext (section 0) for 20 titles per request. Optional Parsoid HTML for the
    first html_n pages per wiki (validation of the LOOKUP rule against rendering)."""
    D = json.load(open(f"raw/{tag}_sample.json")); items = D["items"]; pages = {}
    for w in WIKIS:
        host = f"{w}.wikipedia.org"
        tl = sorted({(x["pages"][w], x["qid"]) for x in items if w in x["pages"]})
        for ch in chunks(tl, 20):
            params = dict(action="query", prop="wbentityusage|revisions|info", titles="|".join(t for t, _ in ch), wbeuentities="|".join(sorted({q for _, q in ch})),
                          wbeulimit="max", rvprop="content|timestamp", rvslots="main", redirects=1)
            usage = {}; info = {}; content = {}; redir = {}
            while True:
                r = wm.api(host, **params)
                for rd in r["query"].get("redirects", []): redir[rd["from"]] = rd["to"]
                for nm in r["query"].get("normalized", []): redir[nm["from"]] = nm["to"]
                for pg in r["query"].get("pages", []):
                    info[pg["title"]] = pg.get("pageid")
                    for q, a in pg.get("wbentityusage", {}).items(): usage.setdefault(pg["title"], {}).setdefault(q, []).extend(a["aspects"])
                    if pg.get("revisions"): content[pg["title"]] = pg["revisions"][0]["slots"]["main"].get("content", "")
                if "continue" in r:
                    cont = r["continue"]; params.update(cont)
                    if "rvcontinue" not in cont and "revisions" in params.get("prop", ""): pass
                else: break
            for t, q in ch:
                tt = redir.get(redir.get(t, t), redir.get(t, t))
                wt = content.get(tt, ""); mm = re.search(r"\n==[^=]", wt)
                pages[f"{w}|{t}"] = {"wiki": w, "title": t, "qid": q, "pageid": info.get(tt), "aspects": sorted(set(usage.get(tt, {}).get(q, []))),
                                     "wt0": wt[:mm.start()] if mm else wt}
        need = [(t, q) for t, q in tl if any(a.startswith("C") for a in pages[f"{w}|{t}"]["aspects"])]
        print(w, "html needed", len(need), flush=True)
        for t, q in (need if html_n < 0 else tl[:html_n]):
            tt = urllib.parse.quote(t.replace(" ", "_"), safe="")
            h0, p0 = fetch_page(host, tt); pages[f"{w}|{t}"]["html0"] = h0; pages[f"{w}|{t}"]["params_parsoid"] = p0
        print(w, "pages done", len(tl), flush=True)
    json.dump(pages, open(f"raw/{tag}_pages.json", "w")); print("pages DONE", len(pages), flush=True)

if __name__ == "__main__":
    st, tag = sys.argv[1], sys.argv[2]
    if st == "sample":
        exclude = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else []
        stage_sample(tag, int(sys.argv[3]), int(sys.argv[4]), exclude)
    elif st == "old": stage_old(tag)
    elif st == "pages": stage_pages(tag, int(sys.argv[3]) if len(sys.argv) > 3 else 0)
