"""One-off: build data/price-history.json from what the repo already knows.

Two sources, both real Amazon captures:
  1. the first committed version of each data/pages/<slug>.json (dated by its data_captured),
     which is the price on the day the page was researched;
  2. every research/refresh/<date>-<slug>.json capture file, one point per ASIN under the
     date in the file name (these are the re-checks the price passes and audits made).
Later commits of a page file are not used on their own, because publish.sh rewrites the
page from the newest capture and the file's data_captured does not move with it.
build.py appends new captures from then on, so this only needs running once.
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout


def num(s):
    m = re.search(r"[\d,]+(?:\.\d+)?", s or "")
    return float(m.group(0).replace(",", "")) if m else None


def main():
    history = {}
    for page in sorted((ROOT / "data/pages").glob("*.json")):
        path = f"data/pages/{page.name}"
        log = git("log", "--follow", "--reverse", "--date=short", "--format=%H %ad", "--", path).splitlines()
        if not log:
            continue
        sha, date = log[0].split(" ", 1)
        try:
            cat = json.loads(git("show", f"{sha}:{path}"))
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            continue
        when = cat.get("data_captured") or date
        for p in cat.get("products", []) + cat.get("avoid", []):
            if isinstance(p.get("price"), (int, float)) and p.get("asin"):
                history.setdefault(p["asin"], {})[when] = p["price"]
    n_files = 0
    for cap in sorted((ROOT / "research/refresh").glob("*.json")):
        m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)\.json$", cap.name)
        if not m or m.group(2) == "holiday-picks":
            continue
        try:
            data = json.loads(cap.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue
        n_files += 1
        for asin, d in data.items():
            if isinstance(d, dict) and re.fullmatch(r"[A-Z0-9]{10}", asin):
                price = num(d.get("price"))
                if price:
                    history.setdefault(asin, {})[m.group(1)] = price
    out = {a: sorted(d.items()) for a, d in sorted(history.items())}
    lines = [f"  {json.dumps(a)}: {json.dumps(v)}" for a, v in out.items()]
    (ROOT / "data/price-history.json").write_text("{\n" + ",\n".join(lines) + "\n}\n", encoding="utf-8")
    print(f"{len(out)} ASINs, {sum(len(v) for v in out.values())} price points, {n_files} capture files")


if __name__ == "__main__":
    main()
