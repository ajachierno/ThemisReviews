import json, os
d = json.load(open('prod-all.json', encoding='utf-8'))
if os.path.exists('prod-b9b.json'):
    d.update({k: v for k, v in json.load(open('prod-b9b.json', encoding='utf-8')).items() if v.get('title')})
m = json.load(open('batch9-pages.json'))
for k, v in m.items():
    done = sum(1 for x in v if (d.get(x) or {}).get('title'))
    ed = 'ED' if os.path.exists(f'editorial/{k}.json') else '  '
    print(f"{ed} {k:26} {done}/{len(v)}")
