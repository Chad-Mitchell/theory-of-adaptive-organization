"""Value normalization, drift and mode classification. Pure functions over raw/<tag>_items.json + raw/<tag>_pages.json."""
import re, json, math, html as _html
import lxml.html
UNIT_SCALE = {  # to base: area km2, length m
 "Q712226": ("area", 1.0), "Q35852": ("area", 0.01), "Q25343": ("area", 1e-6), "Q232291": ("area", 2.589988), "Q81292": ("area", 0.00404686),
 "Q11573": ("len", 1.0), "Q3710": ("len", 0.3048), "Q828224": ("len", 1000.0), "Q174728": ("len", 0.01)}
MULT = [(r"(milliards?|billions?|mrd\.?|млрд\.?|miliardi|miliards|milers de milions|bn)", 1e9),
        (r"(millions?|mio\.?|mill\.?|млн\.?|milioni|milions|milió|mn)", 1e6),
        (r"(thousand|tsd\.?|тыс\.?|mila|mil)", 1e3)]
MULT_RE = [(re.compile(r"^\s*" + p + r"(?![a-zа-я])", re.I), m) for p, m in MULT]
NUM_RE = re.compile(r"(?<![\d.,])\d{1,3}(?:[ \u00a0\u202f\u2009'’]\d{3})+(?:[.,]\d+)?(?!\d)|(?<![\d.,])\d+(?:[.,]\d+)*(?!\d)")

def best(claims):
    cs = [c for c in claims if c.get("rank") != "deprecated"]
    pref = [c for c in cs if c.get("rank") == "preferred"]
    return pref or cs

def norm(c):
    s = c.get("mainsnak", {})
    if s.get("snaktype") != "value": return ("special", s.get("snaktype"))
    dv = s["datavalue"]; t = dv["type"]; v = dv["value"]
    if t == "time":
        m = re.match(r"([+-])(\d+)-(\d\d)-(\d\d)", v["time"]); y = int(m.group(2)) * (-1 if m.group(1) == "-" else 1)
        return ("time", y, int(m.group(3)), int(m.group(4)), int(v["precision"]))
    if t == "quantity":
        u = v.get("unit", "1").rsplit("/", 1)[-1]
        return ("quantity", float(v["amount"]), u)
    if t == "wikibase-entityid": return ("item", v["id"])
    if t == "string": return ("string", v.strip().lower())
    if t == "monolingualtext": return ("string", v["text"].strip().lower())
    return ("other", json.dumps(v, sort_keys=True))

def same(a, b):
    if a[0] != b[0]: return False
    if a[0] == "time":
        p = min(a[4], b[4])
        if p < 9: return a[1] // 10 == b[1] // 10 if p == 8 else True
        if a[1] != b[1]: return False
        if p >= 10 and a[2] != b[2] and a[2] and b[2]: return False
        if p >= 11 and a[3] != b[3] and a[3] and b[3]: return False
        return True
    if a[0] == "quantity": return a[2] == b[2] and abs(a[1] - b[1]) <= 1e-9 * max(1.0, abs(a[1]))
    return a == b

def set_changed(v0, v1):
    return not (all(any(same(x, y) for y in v0) for x in v1) and all(any(same(x, y) for y in v1) for x in v0))

# ---------- text extraction ----------
def strip_wt(wt):
    wt = re.sub(r"<!--.*?-->", " ", wt, flags=re.S)
    wt = re.sub(r"<ref[^>/]*/>", " ", wt); wt = re.sub(r"<ref[^>]*>.*?</ref>", " ", wt, flags=re.S | re.I)
    return wt

def template_params(wt):
    """Text of named-parameter values of top-level templates with >=5 named params (infobox-like), language-agnostic."""
    wt = strip_wt(wt); out = []; i = 0; n = len(wt)
    while i < n:
        j = wt.find("{{", i)
        if j < 0: break
        depth = 0; k = j
        while k < n:
            if wt.startswith("{{", k): depth += 1; k += 2; continue
            if wt.startswith("}}", k):
                depth -= 1; k += 2
                if depth == 0: break
                continue
            k += 1
        body = wt[j + 2:k - 2]
        # split on top-level pipes
        parts = []; d = 0; cur = []; m = 0
        while m < len(body):
            if body.startswith("{{", m) or body.startswith("[[", m): d += 1; cur.append(body[m:m + 2]); m += 2; continue
            if body.startswith("}}", m) or body.startswith("]]", m): d -= 1; cur.append(body[m:m + 2]); m += 2; continue
            if body[m] == "|" and d == 0: parts.append("".join(cur)); cur = []; m += 1; continue
            cur.append(body[m]); m += 1
        parts.append("".join(cur))
        named = [p.split("=", 1)[1] for p in parts[1:] if "=" in p and re.match(r"\s*[^=\[\]{}|]{1,60}=", p)]
        if len(named) >= 5: out.extend(named)
        i = k if k > j else j + 2
    return "\n".join(out)

def infobox_text(html):
    if not html: return ""
    try: doc = lxml.html.fromstring(html)
    except Exception: return ""
    for bad in doc.xpath("//sup[contains(@class,'reference')]|//style|//script"): bad.drop_tree()
    els = doc.xpath("//table|//*[contains(@class,'infobox')]")
    seen = []; txt = []
    for e in els:
        if any(e in s.iterdescendants() for s in seen): continue
        seen.append(e); txt.append(e.text_content())
    return "\n".join(txt)

def clean(s):
    s = _html.unescape(s)
    return re.sub(r"[\u00a0\u202f\u2009]", " ", s)

# ---------- matchers ----------
def parse_nums(text):
    out = []
    for m in NUM_RE.finditer(text):
        tok = m.group(0).strip(); rest = text[m.end():m.end() + 25]
        mult = 1.0
        for r, mm in MULT_RE:
            if r.match(rest): mult = mm; break
        t = re.sub(r"[\s'’]", "", tok)
        cands = set()
        for dec in (".", ","):
            th = "," if dec == "." else "."
            u = t
            if th in u:
                groups = u.split(dec)[0].split(th)
                if not all(len(g) == 3 for g in groups[1:]) or groups[0] == "0": continue
                u = u.replace(th, "")
            if u.count(dec) > 1: continue
            try: x = float(u.replace(dec, "."))
            except ValueError: continue
            d = len(u.split(dec)[1]) if dec in u else 0
            sig = len(re.sub(r"^0+", "", u.replace(dec, "")).rstrip("0")) if d == 0 else len(re.sub(r"^0+", "", u.replace(dec, "")))
            cands.add((x, d, mult, sig))
        out.extend(cands)
    return out

def match_quantity(val, nums):
    amt, unit = val[1], val[2]
    targets = [abs(amt)]
    if unit in UNIT_SCALE:
        kind, sc = UNIT_SCALE[unit]; base = abs(amt) * sc; targets.append(base)
        if kind == "area": targets += [base / 2.589988, base * 100]
        if kind == "len": targets += [base / 0.3048]
    for x, d, mult, sig in nums:
        if sig < 2 and not (x == 0): continue
        tol = 0.5 * 10 ** (-d) * mult
        for v in targets:
            if v == 0: continue
            if abs(v - x * mult) <= tol + 1e-9 * v:
                if sig >= 2 or abs(v) < 10: return True
            if d == 0 and mult == 1 and v >= 1000 and abs(v - x) <= 0.005 * v and sig >= 3: return True
    return False

def year_in(y, text):
    return re.search(r"(?<!\d)" + str(abs(y)) + r"(?!\d)", text) is not None

def item_strings(qid, labels, wiki):
    L = labels.get(qid, {}); out = set()
    for key in (wiki, "mul", "en" if wiki != "en" else None):
        if key and key in L.get("labels", {}): out.add(L["labels"][key])
    out.update(L.get("aliases", {}).get(wiki, [])[:5])
    t = L.get("sitelinks", {}).get(wiki)
    if t:
        out.add(t); out.add(re.sub(r"\s*\(.*?\)\s*$", "", t))
    return {s for s in out if s and len(s) >= 3}

def match(val, text, nums, labels, wiki, low):
    if val[0] == "time":
        return val[4] >= 9 and year_in(val[1], text)
    if val[0] == "quantity": return match_quantity(val, nums)
    if val[0] == "item":
        return any(s.lower() in low for s in item_strings(val[1], labels, wiki))
    if val[0] == "string":
        s = val[1]
        if s.startswith("http"): s = re.sub(r"^https?://(www\.)?", "", s).rstrip("/")
        return len(s) >= 2 and s in low
    return False

def matchable(val):
    return val[0] in ("item", "string", "quantity") or (val[0] == "time" and val[4] >= 9)

def own_usage(aspects, pid):
    a = set(aspects)
    return (f"C.{pid}" in a) or any(x in ("C", "CQR", "X") or (x.startswith("C") and "." not in x) for x in a)

def classify_page(item, page, labels):
    pid = item["pid"]; w = page["wiki"]
    v1 = [norm(c) for c in best(item["claims_now"])]
    v0 = [norm(c) for c in best((item["old"] or {}).get("claims") or [])] if item["old"] else []
    vals = [v for v in v1 + v0 if matchable(v)]
    if not vals: return {"mode": "UNMATCHABLE"}
    params = clean(template_params(page.get("wt0") or "")); pl = params.lower(); pn = parse_nums(params)
    local = any(match(v, params, pn, labels, w, pl) for v in vals)
    asp = page.get("aspects", [])
    specific = f"C.{pid}" in asp
    allc = any(x in ("C", "CQR", "X") or (x.startswith("C") and "." not in x) for x in asp)
    used = specific or allc
    # primary (locked) rule: LOCAL from infobox parameters; otherwise, for pages recording Wikidata statement usage of their own
    # item, the rendered (Parsoid) section-0 infobox/table text decides LOOKUP (value shown) vs ABSENT.
    mode_r = None
    has_html = "html0" in page and page["html0"] is not None
    if has_html:
        ib = clean(infobox_text(page.get("html0") or "")); il = ib.lower(); inn = parse_nums(ib)
        shown = any(match(v, ib, inn, labels, w, il) for v in vals)
        mode_r = "LOCAL" if local else ("LOOKUP" if (shown and used) else ("TSTORE" if shown else "ABSENT"))
    if local: mode = "LOCAL"
    elif used and has_html: mode = "LOOKUP" if shown else "ABSENT"
    elif used: mode = "AMBIG"
    else: mode = "ABSENT"
    # refresh (hold vs freeze) for changed items
    ref = None
    if item["old"] is not None and v0 and v1 and set_changed(v0, v1) and local:
        new = [x for x in v1 if matchable(x) and not any(same(x, y) for y in v0)]
        old = [x for x in v0 if matchable(x) and not any(same(x, y) for y in v1)]
        hn = any(match(x, params, pn, labels, w, pl) for x in new)
        ho = any(match(x, params, pn, labels, w, pl) for x in old)
        ref = "REFRESHED" if hn else ("STALE" if ho else "UNDET")
    return {"mode": mode, "mode_rendered": mode_r, "used": used, "used_specific": specific, "refresh": ref, "has_infobox_params": bool(params.strip())}

def drift(item):
    if item["old"] is None: return None
    v0 = [norm(c) for c in best(item["old"]["claims"] or [])]
    v1 = [norm(c) for c in best(item["claims_now"])]
    if not v0 or not v1: return None   # property absent at one end: addition/removal, not drift of an existing value
    return set_changed(v0, v1)

DATED = ("P580", "P582", "P585", "P577")
def dated_event(item, t0, t1):
    """Method 2 (convergent): a statement of the property has a start/end/point-in-time/publication qualifier inside [t0, t1)."""
    y0 = t0[:10]; y1 = t1[:10]
    for c in item["claims_now"]:
        if c.get("rank") == "deprecated": continue
        for q in DATED:
            for s in c.get("qualifiers", {}).get(q, []):
                tv = s.get("datavalue", {}).get("value", {})
                if not isinstance(tv, dict) or "time" not in tv: continue
                t = tv["time"].lstrip("+"); p = tv.get("precision", 11)
                if p < 11: continue  # need day precision to place inside the window
                if y0 <= t[:10] < y1: return True
    return False
