"""Sync "N+ bought in the past month" figures in editorial copy with the newest refresh capture.

Usage: python -X utf8 research/fixbought.py <slug> [<slug> ...]

fixfigs.py only touches prices, ratings and review counts; this fixes the "bought" line
(verdict, pros, cons, award why) for every pick whose capture has a bought figure.
Preserves the file as JSON (indent=2), same as the other editorial writers.
"""
import json, re, sys, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ED = ROOT / "editorial"
RX = re.compile(r"(\d+K?\+) bought (?:in the past|last) month")


def newest_capture(slug):
    files = sorted(glob.glob(str(ROOT / "refresh" / f"*-{slug}.json")))
    out = {}
    for f in files:  # oldest first, newest wins
        d = json.load(open(f, encoding="utf-8"))
        items = d.get("products", d) if isinstance(d, dict) else d
        for p in (items.values() if isinstance(items, dict) else items):
            if isinstance(p, dict) and p.get("asin") and p.get("title"):
                out[p["asin"]] = p
    return out


def main(slugs):
    for slug in slugs:
        path = ED / f"{slug}.json"
        e = json.loads(path.read_text(encoding="utf-8"))
        cap = newest_capture(slug)
        n = 0
        for p in e.get("products", []):
            m = re.match(r"(\d+K?\+) bought", cap.get(p["asin"], {}).get("bought") or "")
            if not m:
                continue
            cur = m.group(1)

            def fix(s):
                nonlocal n
                def rep(mm):
                    nonlocal n
                    if mm.group(1) != cur:
                        n += 1
                        print(f"  {slug} {p['asin']}: {mm.group(1)} -> {cur}")
                        return mm.group(0).replace(mm.group(1), cur)
                    return mm.group(0)
                return RX.sub(rep, s)

            if p.get("verdict"):
                p["verdict"] = fix(p["verdict"])
            p["pros"] = [fix(x) for x in p.get("pros", [])]
            p["cons"] = [fix(x) for x in p.get("cons", [])]
            for a in e.get("awards", []):
                if a["asin"] == p["asin"]:
                    a["why"] = fix(a["why"])
        if n:
            path.write_text(json.dumps(e, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{slug}: {n} bought-line fix(es)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
