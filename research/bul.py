import json, sys, time
def load(f):
    for _ in range(10):
        try: return json.load(open(f, encoding='utf-8'))
        except Exception: time.sleep(2)
d = load('prod-all.json'); d.update(load('prod-b9b.json'))
kw = [k.lower() for k in sys.argv[2:]] if len(sys.argv) > 2 else None
for a in sys.argv[1].split(','):
    p = d[a]; print('##', a, p['title'][:120])
    for b in p.get('bullets', []):
        if not kw or any(k in b.lower() for k in kw): print('  -', b[:260])
