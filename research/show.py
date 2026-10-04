import json, sys
r = json.load(open("search-all.json", encoding="utf-8"))
q = sys.argv[1]; seen = set()
for x in r:
    if x["query"] != q or not x["asin"] or x["asin"] in seen: continue
    seen.add(x["asin"])
    print(x["asin"], "SP" if x["sponsored"] else "  ", (x["price"] or "-").ljust(8), (x["rating"] or "-")[:3], (x["reviews"] or "-")[:22].ljust(22), (x["bought"] or "")[:10].ljust(10), "|", x["title"][:110])
