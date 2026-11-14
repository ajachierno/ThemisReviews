"""Price pass through the Amazon Creators API (no scraping).

    python -X utf8 research/api_pricepass.py <slug> [<slug>...]

For every listing on those pages it asks the API for price, availability and buy box, then
writes research/refresh/<today>-<slug>.json: the listing's last good capture (title, image,
rating, review count, bought line) with the price and availability replaced by the API's.
The API has no rating or review fields, so those stay as last captured; each record says so
in `rating_captured`. merge.py reads the file like any other refresh capture.

A listing is left out of the file (its previous capture stays in force) and printed as a
FLAG when the API does not return it, returns no price, has no buy-box winner, or returns a
title that no longer matches the captured one. Flags are for a full audit to settle; this
script never removes a pick.
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import creators_api  # noqa: E402
from scrape_data import load_scrape  # noqa: E402

TODAY = dt.date.today().isoformat()


def words(s):
    return set(re.findall(r"[a-z0-9]+", (s or "").lower()))


def main(slugs):
    last = load_scrape()
    pages = {}
    for s in slugs:
        d = json.loads((HERE.parent / "data" / "pages" / f"{s}.json").read_text(encoding="utf-8"))
        pages[s] = [p["asin"] for p in d["products"] + d.get("avoid", [])]
    asins = list(dict.fromkeys(a for v in pages.values() for a in v))
    items, errs = creators_api.get_items(asins)
    recs = {a: creators_api.record(a, items.get(a)) for a in asins}
    hard = [e for e in errs if "http" in e]
    if hard:
        print("API errors:", json.dumps(hard)[:800])
    flagged = {}
    for s, page_asins in pages.items():
        out, moves = {}, []
        for a in page_asins:
            r, old = recs[a], last.get(a)
            why = None
            if old is None:
                why = "no earlier capture"
            elif r["notfound"]:
                why = "not returned by the API"
            elif not r["price"]:
                why = f"no price ({r['avail']})"
            elif not r["buybox"]:
                why = f"no buy-box winner ({r['avail']})"
            else:
                a_w, o_w = words(r["title"]), words(old.get("title"))
                if len(a_w & o_w) < 0.5 * min(len(a_w), len(o_w)):
                    why = f"title changed: {r['title'][:70]!r}"
            if why:
                flagged.setdefault(s, []).append(f"{a} {why}")
                continue
            new = dict(old)
            if new.get("captured") != TODAY or "rating_captured" not in new:
                new["rating_captured"] = old.get("rating_captured") or old.get("captured")
            new.update(price=r["price"], availability=r["avail"], captured=TODAY,
                       price_source="creators_api")
            if old.get("price") != r["price"]:
                moves.append(f"{a} {old.get('price')} -> {r['price']}")
            out[a] = new
        f = HERE / "refresh" / f"{TODAY}-{s}.json"
        if out:
            f.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"{s}: {len(out)} of {len(page_asins)} priced, {len(moves)} moved"
              + (f", {len(flagged[s])} FLAG" if s in flagged else ""))
        for m in moves:
            print("   ", m)
        for x in flagged.get(s, []):
            print("    FLAG", x)
    print(f"\n{len(items)} of {len(asins)} listings returned by the API; "
          f"{sum(len(v) for v in flagged.values())} flagged on {len(flagged)} page(s)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    main(sys.argv[1:])
