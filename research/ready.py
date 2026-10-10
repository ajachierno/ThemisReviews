import json
from scrape_data import load_scrape
d=load_scrape();m=json.load(open('batch12-pages.json'))
for s,v in m.items():
    n=sum(1 for a in v if (d.get(a) or {}).get('title'))
    print(f"{s}: {n}/{len(v)}")
