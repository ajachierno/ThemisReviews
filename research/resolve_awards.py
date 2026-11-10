"""Re-resolve every page's awards in data/pages from the award rules in research/editorial, without
re-merging (so prices and review counts stay exactly as captured). Use after changing awards.py or
an award rule: python -X utf8 research/resolve_awards.py [slug ...]"""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import awards  # noqa: E402

slugs = sys.argv[1:] or [p.stem for p in sorted((ROOT / "data" / "pages").glob("*.json"))]
for slug in slugs:
    f, ef = ROOT / "data" / "pages" / f"{slug}.json", ROOT / "research" / "editorial" / f"{slug}.json"
    if not ef.exists():
        continue
    ed, page = json.loads(ef.read_text(encoding="utf-8")), json.loads(f.read_text(encoding="utf-8"))
    for a in ed["awards"]:
        awards.check_rule(a["rule"], page, f"{slug} {a['label']}")
    tmp = copy.deepcopy(page)
    tmp["awards"] = ed["awards"]
    page["awards"] = awards.resolve(tmp)
    f.write_text(json.dumps(page, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"resolved awards on {len(slugs)} page(s)")
