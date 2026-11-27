import json,urllib.request,urllib.parse
def q(s):
    u="https://api.crossref.org/works?rows=3&query.bibliographic="+urllib.parse.quote(s)
    m=json.load(urllib.request.urlopen(u,timeout=30))['message']['items']
    for it in m: print(" ?",it.get('DOI'),'|',(it.get('title') or [''])[0][:90],'|',it.get('container-title',[''])[:1],it.get('issued',{}).get('date-parts'))
def d(doi):
    try:
        m=json.load(urllib.request.urlopen("https://api.crossref.org/works/"+doi,timeout=30))['message']
        a=m.get('author',[{}])[0].get('family','')
        print("OK",doi,'|',m['title'][0][:90],'|',a,'|',(m.get('container-title') or [''])[0],m.get('volume'),m.get('page'),m['issued']['date-parts'][0][0])
    except Exception as e: print("FAIL",doi,e)
import sys
if sys.argv[1]=='q':
    for s in ["Kipnis Goldsmith Eldar distortion rate function of sampled Wiener processes","Berger information rates of Wiener processes 1970","Sagawa Ueda minimal energy cost for thermodynamic information processing measurement and information erasure"]:
        print(s); q(s)
else:
    for x in sys.argv[2:]: d(x)
