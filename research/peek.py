import json, sys
d = json.load(open("prod-all.json", encoding="utf-8"))
for a in sys.argv[1:]:
    v = d.get(a) or {}
    if not v.get("title"):
        print(f"### {a}: NOT SCRAPED\n"); continue
    print(f"### {a} | {v['price']} | {v['rating']} | {v['reviews']} | {v.get('bought')} | avail: {(v.get('availability') or '')[:40]} | seller: {v.get('seller')}")
    print("T:", v["title"][:200]); print("BY:", v.get("byline"))
    for b in v["bullets"][:7]: print(" -", b[:260])
    sp = {k: x for k, x in v["specs"].items() if not any(s in k for s in ("Customer Reviews", "Best Sellers", "ASIN", "Date First"))}
    print(" SPECS:", "; ".join(f"{k}={x[:40]}" for k, x in list(sp.items())[:14]))
    print()
