import json,re,sys
from scrape_data import load_scrape
d=load_scrape();m=json.load(open('batch12-pages.json'))
K=[('wifi',r'wi-?fi|2\.4 ?ghz'),('bt',r'bluetooth'),('matter',r'\bmatter\b(?! (where|most|to))'),('zigbee',r'zigbee'),('thread',r'\bthread\b'),('hub',r'\bhub\b|gateway|bridge|base station'),('app',r'\bapp\b'),('alexa',r'alexa'),('google',r'google'),('ha',r'home assistant'),('lte',r'\blte\b|cellular'),('sub',r'subscription|membership|monthly fee')]
for s in sys.argv[1:]:
    print('#####',s)
    for a in m[s]:
        v=d.get(a) or {}
        t=(v.get('title') or '')+' '+' '.join(v.get('bullets',[]))
        f=[k for k,p in K if re.search(p,t,re.I)]
        print(f"{a} {v.get('price')} {(v.get('rating') or '')[:3]} {v.get('reviews')} | {(v.get('title') or '')[:70]} | {','.join(f)}")
