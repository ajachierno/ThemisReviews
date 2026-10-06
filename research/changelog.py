"""Build data/changelog.json from the git history of data/pages/<slug>.json.

For each page it records:
  captured  the date of the last commit that changed a price, rating, or review count
            (merge.py runs right after a scrape, so this is when the Amazon data was pulled)
  updated   the date of the last reader-visible change
  entries   [{date, notes[]}] newest first: products added or dropped, award changes,
            refreshed prices, and a "published" line for the first version

Run it after committing page data (publish.sh does), then rebuild. The working-tree version
of each page counts as "today" if it differs from HEAD.
Usage: python research/changelog.py
"""
import datetime
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "data" / "pages"
OUT = ROOT / "data" / "changelog.json"
# Hand-written notes for changes the diff can't see (corrections, rewritten verdicts):
# {"<slug>": [{"date": "YYYY-MM-DD", "note": "..."}]}
NOTES = Path(__file__).parent / "editorial" / "changelog-notes.json"
MANUAL = json.loads(NOTES.read_text(encoding="utf-8")) if NOTES.exists() else {}
# {"<slug>": "YYYY-MM-DD"}: the last full refresh (themisreviews-refresh skill). Every listing was
# re-read that day, so the page's "prices checked" date moves even if no number changed.
AUDITS_FILE = Path(__file__).parent / "editorial" / "audit-log.json"
AUDITS = json.loads(AUDITS_FILE.read_text(encoding="utf-8")) if AUDITS_FILE.exists() else {}


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout


def versions(slug):
    """[(date, data)] oldest first, plus the working copy if it differs from the last commit."""
    rel = f"data/pages/{slug}.json"
    out = []
    for line in reversed(git("log", "--format=%H %ad", "--date=short", "--", rel).split("\n")):
        if not line.strip():
            continue
        sha, date = line.split()
        try:
            out.append((date, json.loads(git("show", f"{sha}:{rel}"))))
        except json.JSONDecodeError:
            continue
    cur = json.loads((PAGES / f"{slug}.json").read_text(encoding="utf-8"))
    if not out or cur != out[-1][1]:
        out.append((datetime.date.today().isoformat(), cur))
    return out


def label(p):
    return f"{p['brand']} {p['model']}"


def market(d):
    return {p["asin"]: (p["price"], p["rating"], p["reviews_count"]) for p in d["products"] + d.get("avoid", [])}


def diff(old, new):
    notes = []
    o = {p["asin"]: p for p in old["products"]}
    n = {p["asin"]: p for p in new["products"]}
    added = [label(n[a]) for a in n if a not in o]
    dropped = [label(o[a]) for a in o if a not in n]
    if added:
        notes.append("Added " + ", ".join(added) + ".")
    if dropped:
        notes.append("Dropped " + ", ".join(dropped) + ".")
    oa = {a["label"]: a["asin"] for a in old.get("awards", [])}
    for a in new.get("awards", []):
        if oa.get(a["label"]) not in (None, a["asin"]) and a["asin"] in n:
            notes.append(f"New {a['label']}: {label(n[a['asin']])}.")
    ov = {a["asin"] for a in old.get("avoid", [])}
    for a in new.get("avoid", []):
        if a["asin"] not in ov:
            notes.append(f"New avoid pick: {label(a)}.")
    for a in old.get("avoid", []):
        if a["asin"] not in {x["asin"] for x in new.get("avoid", [])}:
            notes.append(f"Removed {label(a)} from the avoid list.")
    mo, mn = market(old), market(new)
    if any(mo[a] != mn[a] for a in mn if a in mo):
        notes.append("Prices, ratings, and review counts refreshed from Amazon.")
    return notes


def build():
    log = {}
    for f in sorted(PAGES.glob("*.json")):
        slug = f.stem
        vs = versions(slug)
        first_date, first = vs[0]
        avoid = len(first.get("avoid", []))
        entries = {first_date: [f"Published with {len(first['products'])} picks"
                                + (f" and {avoid} to avoid." if avoid else ".")]}
        captured = first_date
        for (_d0, old), (d1, new) in zip(vs, vs[1:]):
            notes = diff(old, new)
            if market(old) != market(new):
                captured = d1
            if notes:
                entries.setdefault(d1, []).extend(notes)
        for m in MANUAL.get(slug, []):
            entries.setdefault(m["date"], []).append(m["note"])
        merged = [{"date": d, "notes": list(dict.fromkeys(ns))} for d, ns in sorted(entries.items(), reverse=True)]
        if AUDITS.get(slug, "") > captured:
            captured = AUDITS[slug]
        log[slug] = {"captured": captured, "updated": merged[0]["date"], "entries": merged,
                     "audited": AUDITS.get(slug)}
    OUT.write_text(json.dumps(log, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"changelog: {len(log)} pages")


if __name__ == "__main__":
    build()
