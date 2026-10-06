"""Helpers for the page refresh (themisreviews-refresh skill).

  python research/refresh.py order                 # every live page, least recently audited first
  python research/refresh.py scrape <slug>         # re-read every listing on the page from Amazon
  python research/refresh.py diff <slug>           # old vs new numbers, dead listings, stale figures in the copy
  python research/refresh.py search <slug> "query" ["query" ...]
                                                   # where today's search results rank our picks, and
                                                   # the best-ranked listings we don't carry
  python research/refresh.py stamp <slug> ["note"] # record the audit (audit-log.json) and a What changed note

Scrapes go to research/refresh/<date>-<slug>.json (picked up by merge.py through scrape_data.py,
newest wins). Searches go to research/refresh-search/.
"""
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
ED = HERE / "editorial"
TODAY = datetime.date.today().isoformat()
sys.path.insert(0, str(HERE))


def num(s, cast=float):
    if s in (None, ""):
        return None
    if isinstance(s, (int, float)):
        return cast(s)
    m = re.search(r"[\d,]+(?:\.\d+)?", str(s))
    return cast(m.group(0).replace(",", "")) if m else None


def live_slugs():
    site = json.loads((ROOT / "data" / "site.json").read_text(encoding="utf-8"))
    return [s["slug"] for p in site["protocols"] for s in p["subs"] if s.get("ready")]


def page(slug):
    return json.loads((ROOT / "data" / "pages" / f"{slug}.json").read_text(encoding="utf-8"))


def order():
    audits = json.loads((ED / "audit-log.json").read_text(encoding="utf-8"))
    log = json.loads((ROOT / "data" / "changelog.json").read_text(encoding="utf-8"))
    rows = []
    for i, slug in enumerate(live_slugs()):
        a = audits.get(slug)
        key = a or log.get(slug, {}).get("captured") or "0000-00-00"
        rows.append((key, i, slug, "audited" if a else "never audited, captured"))
    rows.sort()
    for key, _i, slug, what in rows:
        print(f"{key}  {slug}  ({what})")
    print(f"{len(rows)} pages")


def scrape(slug):
    d = page(slug)
    asins = [p["asin"] for p in d["products"] + d.get("avoid", [])]
    out = HERE / "refresh" / f"{TODAY}-{slug}.json"
    out.parent.mkdir(exist_ok=True)
    print(f"Scraping {len(asins)} listings into {out.name} (visible Chrome window; ~10 s each)")
    subprocess.run([sys.executable, "-X", "utf8", str(HERE / "amz.py"), "products", str(out), *asins], check=False)


def latest_capture(slug):
    files = sorted((HERE / "refresh").glob(f"*-{slug}.json"))
    if not files:
        sys.exit(f"No refresh capture for {slug}. Run: python research/refresh.py scrape {slug}")
    return files[-1], json.loads(files[-1].read_text(encoding="utf-8"))


def diff(slug):
    d = page(slug)
    f, new = latest_capture(slug)
    ed = json.loads((ED / f"{slug}.json").read_text(encoding="utf-8"))
    print(f"Comparing data/pages/{slug}.json with {f.name}\n")
    print(f"{'':2}{'product':38} {'price':>17} {'rating':>9} {'reviews':>15}  notes")
    dead = []
    for group, items in (("pick", d["products"]), ("avoid", d.get("avoid", []))):
        for p in items:
            n = new.get(p["asin"], {})
            name = f"{p['brand']} {p['model']}"[:38]
            notes = []
            if not n.get("title"):
                notes.append("NO PAGE (dead, blocked, or failed: re-check by hand)")
            avail = (n.get("availability") or "").lower()
            if re.search(r"unavailable|not available|out of stock|no longer", avail):
                notes.append(f"UNAVAILABLE: {n.get('availability')}")
            np_, nr, nc = num(n.get("price")), num(n.get("rating")), num(n.get("reviews"), int)
            if n.get("title") and np_ is None:
                notes.append("NO PRICE (no buy box?)")
            if np_ and abs(np_ - p["price"]) / p["price"] >= 0.15:
                notes.append(f"price moved {round((np_ - p['price']) / p['price'] * 100):+d}%")
            if nr is not None and abs(nr - p["rating"]) >= 0.2:
                notes.append(f"rating {p['rating']} -> {nr}")
            if n.get("seller") and p.get("seller") and n["seller"] != p["seller"]:
                notes.append(f"seller now {n['seller']}")
            if any(x.startswith(("NO PAGE", "UNAVAILABLE", "NO PRICE")) for x in notes):
                dead.append((group, p["asin"], name))
            tag = "x " if group == "avoid" else "  "
            print(f"{tag}{name:38} {p['price']:>7.2f} -> {np_ if np_ is not None else '?':>7} "
                  f"{p['rating']:>4}->{nr if nr is not None else '?':<4} {p['reviews_count']:>6,}->{nc if nc is not None else '?':<7}  {'; '.join(notes)}")
    # figures written into the copy that the new numbers make wrong
    print("\nFigures in the editorial copy that may now be stale:")
    texts = []
    for p in ed["products"] + ed.get("avoid", []):
        for k in ("verdict", "pros", "cons", "reasons"):
            v = p.get(k)
            for s in ([v] if isinstance(v, str) else v or []):
                texts.append((p["asin"], s))
    for a in ed.get("awards", []):
        texts.append((a["asin"], a["why"]))
    found = 0
    for p in d["products"] + d.get("avoid", []):
        n = new.get(p["asin"], {})
        np_, nr, nc = num(n.get("price")), num(n.get("rating")), num(n.get("reviews"), int)
        olds = []
        if nc is not None and nc != p["reviews_count"]:
            olds.append(f"{p['reviews_count']:,}")
        if np_ is not None and abs(np_ - p["price"]) > 0.005:
            olds.append(f"${p['price']:.2f}")
            if p["price"] == int(p["price"]):
                olds.append(f"${int(p['price'])}")
        if nr is not None and nr != p["rating"]:
            olds.append(f"{p['rating']} stars")
        for asin, s in texts:
            if asin == p["asin"]:
                for o in olds:
                    if o in s:
                        found += 1
                        print(f"  {p['brand']} {p['model']}: \"{s}\"  ({o} is now "
                              f"{ {'$': np_}.get(o[0], nc if ',' in o or o.isdigit() else nr) })")
    if not found:
        print("  none")
    if dead:
        print("\nRemoval candidates:")
        for g, a, nm in dead:
            print(f"  {g}: {nm} ({a})")


def search(slug, queries):
    d = page(slug)
    ours = {p["asin"] for p in d["products"] + d.get("avoid", [])}
    out = HERE / "refresh-search" / f"{TODAY}-{slug}.json"
    out.parent.mkdir(exist_ok=True)
    subprocess.run([sys.executable, "-X", "utf8", str(HERE / "amz.py"), "search", str(out), *queries], check=False)
    rows = json.loads(out.read_text(encoding="utf-8"))
    for q in queries:
        organic = []
        for r in rows:
            if r.get("query") == q and not r.get("sponsored") and r.get("asin") and r["asin"] not in [x["asin"] for x in organic]:
                organic.append(r)
        print(f"\n\"{q}\": {len(organic)} organic results")
        for p in d["products"] + d.get("avoid", []):
            pos = next((i + 1 for i, r in enumerate(organic) if r["asin"] == p["asin"]), None)
            print(f"  {'#' + str(pos) if pos else 'not in results':>15}  {p['brand']} {p['model']}")
        print("  Best-ranked listings we don't carry:")
        shown = 0
        for i, r in enumerate(organic):
            if r["asin"] in ours:
                continue
            print(f"    #{i + 1:<3} {r['asin']}  {r.get('price') or '?':>9}  {(r.get('rating') or '?')[:3]}  "
                  f"{r.get('reviews') or '?':>10}  {r['title'][:80]}")
            shown += 1
            if shown == 12:
                break


def stamp(slug, note=None):
    a = json.loads((ED / "audit-log.json").read_text(encoding="utf-8"))
    a[slug] = TODAY
    (ED / "audit-log.json").write_text(json.dumps(a, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if note:
        n = json.loads((ED / "changelog-notes.json").read_text(encoding="utf-8"))
        n.setdefault(slug, []).append({"date": TODAY, "note": note})
        (ED / "changelog-notes.json").write_text(json.dumps(n, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Stamped {slug} audited {TODAY}" + (" with a note" if note else ""))


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    {"order": lambda: order(), "scrape": lambda: scrape(args[0]), "diff": lambda: diff(args[0]),
     "search": lambda: search(args[0], args[1:]), "stamp": lambda: stamp(args[0], args[1] if len(args) > 1 else None)}[cmd]()
