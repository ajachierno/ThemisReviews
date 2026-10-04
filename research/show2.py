import json, re, sys
r = json.load(open(sys.argv[1], encoding="utf-8"))
q, inc = sys.argv[2], re.compile(sys.argv[3], re.I)
exc = re.compile(sys.argv[4], re.I) if len(sys.argv) > 4 else None
seen, n = set(), 0
for x in r:
    if x["query"] != q or not x["asin"] or x["asin"] in seen: continue
    seen.add(x["asin"]); t = x["title"]
    if not inc.search(t) or (exc and exc.search(t)): continue
    n += 1
    if n > 32: break
    print(x["asin"], "SP" if x["sponsored"] else "  ", (x["price"] or "-").ljust(8), (x["rating"] or "-")[:3], (x["reviews"] or "-").replace(" ratings","")[:9].ljust(9), "|", t[:100])
