"""Apply refresh.py diff's stale-figure list to research/editorial/<slug>.json, scoped to each product.

  python research/fixfigs.py <slug>

A sentence holding two stale figures gets only the first; it prints SKIP for the second, fix that by hand.
Also check "cheapest"/"lowest" claims yourself, since the diff only catches numbers."""
import json, re, subprocess, sys
slug = sys.argv[1]
out = subprocess.run([sys.executable, "-X", "utf8", "research/refresh.py", "diff", slug],
                     capture_output=True, text=True, encoding="utf-8").stdout
path = f"research/editorial/{slug}.json"
raw = open(path, encoding="utf-8").read()
ed = json.loads(raw)
by_name = {f"{p['brand']} {p['model']}": p["asin"] for p in ed["products"] + ([ed["avoid"]] if isinstance(ed.get("avoid"), dict) else [])}
def fmt(old, new):
    if old.startswith("$"):
        return "$" + f"{float(new):,.2f}"
    if old.endswith("stars"):
        return new + " stars"
    if re.fullmatch(r"[\d,]+", old) and re.fullmatch(r"\d+", new):
        return f"{int(new):,}"
    return new
def spans(asin):
    """Text spans of every object that starts with this asin (product, award, avoid)."""
    res = []
    for m in re.finditer(r'\{\s*"asin":\s*"%s"' % asin, raw):
        depth, i = 0, m.start()
        while True:
            c = raw[i]
            if c == '"':
                i += 1
                while raw[i] != '"':
                    i += 2 if raw[i] == "\\" else 1
            elif c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0: break
            i += 1
        res.append((m.start(), i + 1))
    return res
n = 0
for line in out.splitlines():
    m = re.match(r'\s+(.+?): "(.*)"  \((.+?) is now (.+?)\)$', line)
    if not m:
        continue
    name, sent, old, new = m.groups()
    asin = by_name.get(name)
    lit = '"' + json.dumps(sent, ensure_ascii=False)[1:-1]
    newv = fmt(old, new)
    hit = False
    for a, b in sorted(spans(asin), reverse=True) if asin else []:
        seg = raw[a:b]
        if lit in seg:
            idx = seg.index(lit)
            fixed_lit = lit.replace(old, newv, 1)
            raw = raw[:a] + seg.replace(lit, fixed_lit) + raw[b:]
            hit = True
    if hit:
        n += 1; print(f"  {name[:28]:28} {old} -> {newv}")
    else:
        print(f"  SKIP {name[:28]}: {sent[:60]}  ({old} -> {newv})")
json.loads(raw)
open(path, "w", encoding="utf-8").write(raw)
print(slug, n, "fixes")
