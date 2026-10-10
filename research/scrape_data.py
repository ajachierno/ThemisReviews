"""One place to load scraped Amazon listings.

Base captures (prod-all.json, prod-hubs.json, prod-b9b.json) load first, then every refresh
capture in research/refresh/ in filename order (YYYY-MM-DD-<slug>.json), so the newest
successful read of a listing wins. Entries without a title (failed or dead pages) never
overwrite good data; refresh.py reports those separately.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
BASE = ("prod-all.json", "prod-hubs.json", "prod-b9b.json", "prod-b10a.json", "prod-b10b.json")
REFRESH_DIR = HERE / "refresh"


def load_scrape():
    out = {}
    files = [HERE / f for f in BASE] + sorted(REFRESH_DIR.glob("*.json"))
    for f in files:
        if f.exists():
            out.update({k: v for k, v in json.loads(f.read_text(encoding="utf-8")).items() if v.get("title")})
    return out
