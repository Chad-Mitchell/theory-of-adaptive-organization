# Round 10b sources: Crossref check.
import json, urllib.request, time
dois = ["10.1080/00927879508825218","10.1090/S0273-0979-1995-00593-8","10.1090/S0002-9904-1946-08506-7",
"10.2307/1969795","10.2307/1969796","10.2307/1969792","10.2307/1968117","10.1016/0022-4049(88)90125-9",
"10.1063/1.2883740","10.1007/s00220-009-0865-6","10.1007/BF02940714","10.1090/s0002-9947-1905-1500717-7","10.1007/978-3-642-46248-1_8",
"10.1512/iumj.1957.6.56050"]
for d in dois:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/"+d, headers={"User-Agent":"gtao-rnd"}), timeout=30))["message"]
        au = "; ".join(a.get("family","?") for a in r.get("author",[]))
        print("OK", d, "|", r["issued"]["date-parts"][0][0], "|", (r.get("title") or ["?"])[0], "|", au, "|", (r.get("container-title") or ["?"])[0], r.get("volume",""), r.get("page",""))
    except Exception as e:
        print("FAIL", d, e)
    time.sleep(0.4)
