import json,urllib.request,urllib.parse,sys
H={}
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=30))['message']
def d(doi):
    time.sleep(2)
    try:
        m=get("https://api.crossref.org/works/"+urllib.parse.quote(doi))
        au=", ".join(a.get('family','') for a in m.get('author',[])[:4])
        print("OK",doi,'|',m['title'][0][:100],'|',au,'|',(m.get('container-title') or [''])[0],m.get('volume'),m.get('page'),m['issued']['date-parts'][0][0])
    except Exception as e: print("FAIL",doi,e)
import time
def q(s):
    time.sleep(3)
    m=get("https://api.crossref.org/works?rows=4&query.bibliographic="+urllib.parse.quote(s))['items']
    print("Q:",s)
    for it in m: print("  ?",it.get('DOI'),'|',(it.get('title') or [''])[0][:100],'|',", ".join(a.get('family','') for a in it.get('author',[])[:3]),'|',it.get('issued',{}).get('date-parts'))
if sys.argv[1]=='q':
    for s in sys.argv[2:]: q(s)
else:
    for x in sys.argv[2:]: d(x)
