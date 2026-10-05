"""Compact review sheet for one batch-9 page: python pagebrief.py <slug> [bullets]"""
import json
import re
import sys

pages = json.load(open("batch9-pages.json", encoding="utf-8"))
d = json.load(open("prod-all.json", encoding="utf-8"))
import os
if os.path.exists("prod-b9b.json"):
    d.update({k: v for k, v in json.load(open("prod-b9b.json", encoding="utf-8")).items() if v.get("title")})
slug = sys.argv[1]
nb = int(sys.argv[2]) if len(sys.argv) > 2 else 4
FLAGS = ["alexa", "google", "homekit|apple home|siri", "matter", "home assistant", "smartthings", "hubitat", "zigbee",
         "thread", "z-?wave", "neutral", "subscription|monthly fee|paid plan", "hub required|requires a hub|hub needed|gateway required"]
for a in pages[slug]:
    v = d.get(a) or {}
    if not v.get("title"):
        print(f"## {a}: NOT SCRAPED")
        continue
    t = (v["title"] + " " + " ".join(v.get("bullets", []))).lower()
    flags = [f.split("|")[0] for f in FLAGS if re.search(f, t)]
    seller = (v.get("seller") or "")[:20]
    av = (v.get("availability") or "").split("{")[0].strip()[:24]
    print(f"## {a} | {v['price']} | {(v.get('rating') or '')[:3]} | {v['reviews']} | {v.get('bought') or ''} | {seller} | {av}")
    print("   ", v["title"][:140])
    print("    flags:", ", ".join(flags))
    for b in v.get("bullets", [])[:nb]:
        print("    -", re.sub(r"\s+", " ", b)[:210])
