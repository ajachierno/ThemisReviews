"""Add batch pages to data/site.json right before they're published (so unfinished pages never show
"Coming soon"). Reads protocol, menu title, and family from research/batch1N.json.
Usage: python research/add_subs.py <slug> [<slug> ...]   (publish.sh then marks them ready)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
batch = {}
for f in sorted((ROOT / "research").glob("batch1[0-9].json")):
    batch.update(json.loads(f.read_text(encoding="utf-8")))
site_path = ROOT / "data" / "site.json"
site = json.loads(site_path.read_text(encoding="utf-8"))
protos = {p["slug"]: p for p in site["protocols"]}
for slug in sys.argv[1:]:
    b = batch[slug]
    subs = protos[b["proto"]]["subs"]
    if any(s["slug"] == slug for s in subs):
        continue
    subs.append({"slug": slug, "title": b["title"], "family": b["family"]})
    print(f"added {slug} under {b['proto']}")
site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
