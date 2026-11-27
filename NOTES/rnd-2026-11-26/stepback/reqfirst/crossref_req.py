import json, urllib.request, time
dois=["10.1002/j.1538-7305.1956.tb03809.x","10.1126/science.1114383","10.1111/j.1600-0706.2009.17781.x","10.1007/s10955-011-0166-2","10.1088/1742-5468/2016/04/043403","10.1109/TIT.1968.1054193","10.1109/18.720541","10.1016/S0304-3932(03)00029-1","10.1103/PhysRevX.4.031015","10.1287/opre.11.3.399","10.1103/PhysRevA.89.052124","10.1038/s41567-019-0732-0","10.1147/rd.53.0183","10.1109/JRPROC.1949.232969"]
for d in dois:
    for k in range(3):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/"+d,headers={"User-Agent":"gtao-notes (mailto:none)"}),timeout=30))["message"]
            print("OK",d,"|",r.get("issued",{}).get("date-parts",[[None]])[0][0],"|",";".join(a.get("family","") for a in r.get("author",[])[:4]),"|",(r.get("title") or [""])[0][:90],"|",(r.get("container-title") or [""])[0],"|",r.get("volume"),r.get("page"),flush=True); break
        except Exception as e:
            if k==2: print("FAIL",d,e,flush=True)
            time.sleep(2)
