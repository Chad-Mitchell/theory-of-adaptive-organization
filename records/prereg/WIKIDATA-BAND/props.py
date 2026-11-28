# Fixed property list (domain and datatype labels are property-level, fixed before any outcome).
PROPS = [
 # pid, label, domain, datatype
 ("P569","date of birth","person","time"),
 ("P19","place of birth","person","item"),
 ("P27","country of citizenship","person","item"),
 ("P102","member of political party","person","item"),
 ("P108","employer","person","item"),
 ("P1082","population","place","quantity"),
 ("P2046","area","place","quantity"),
 ("P2044","elevation above sea level","place","quantity"),
 ("P281","postal code","place","string"),
 ("P6","head of government","place","item"),
 ("P169","chief executive officer","org","item"),
 ("P1128","employees","org","quantity"),
 ("P2139","total revenue","org","quantity"),
 ("P159","headquarters location","org","item"),
 ("P571","inception","org","time"),
 ("P112","founded by","org","item"),
 ("P286","head coach","sports","item"),
 ("P115","home venue","sports","item"),
 ("P118","league","sports","item"),
 ("P348","software version identifier","software","string"),
 ("P277","programming language","software","item"),
 ("P178","developer","software","item"),
 ("P35","head of state","country","item"),
 ("P2131","nominal GDP","country","quantity"),
 ("P1081","Human Development Index","country","quantity"),
 ("P36","capital","country","item"),
]
WIKIS = ["en","de","fr","ru","it","ca"]
T0 = "2023-11-15T00:00:00Z"   # drift window start; T1 = time of collection
MONEY = {"P2139","P2131"}
