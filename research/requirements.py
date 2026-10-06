"""Tag every ranked product with what it needs, for the "Must work without" filters and the
home-page picker. Writes data/requirements.json:

  {"<page-slug>": {"<asin>": {"neutral": "no"|"yes"|"?"|"na", "hub": true|false|null, "sub": true|false}}}

neutral  "no" only when the listing or our specs say no neutral is needed; "na" on pages where
         wiring doesn't apply (sensors, bulbs, plugs...)
hub      true when the product needs a separate hub, bridge, gateway, or Thread border router;
         null on pages that are hubs themselves
sub      true when its main job (recording, for cameras and doorbells) needs a paid plan

Rules first, then research/editorial/requirements-overrides.json ({"<asin>": {...}}) wins.
Usage: python research/requirements.py [--show]
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from scrape_data import load_scrape  # noqa: E402

SCRAPE = load_scrape()
OVR = HERE / "editorial" / "requirements-overrides.json"
OVERRIDES = json.loads(OVR.read_text(encoding="utf-8")) if OVR.exists() else {}

WIRED_FAMILIES = {"light-switches", "dimmers", "fan-controls", "outlets", "relays"}
# pages whose products are hubs, bridges, or network gear: "needs a hub" doesn't apply
HUB_PAGE = re.compile(r"controllers|coordinators|border-routers|bridges|proxies|mesh-routers|smart-displays|smart-speakers")

NO_NEUTRAL = re.compile(r"\bno[- ]neutral\b|neutral (wire )?(is )?not (required|needed)|without (a )?neutral|no need (for )?(a )?neutral"
                        r"|works? with(out)? or without (a )?neutral|neutral (wire )?optional|neutral or no[- ]neutral", re.I)
NEEDS_NEUTRAL = re.compile(r"neutral (wire )?(is )?(required|needed)|requires? (a )?neutral|needs? (a )?neutral|need neutral", re.I)
HUB_NEEDED = re.compile(r"(?<!no )(?<!without )(?<!not )(?<!n't )\b(hub|bridge|gateway) (is )?required|requires? (an? |the )?([\w-]+ ){0,3}(hub|bridge|gateway)\b"
                        r"|(?<!no )\bhub required\b", re.I)
HUB_NOT_NEEDED = re.compile(r"no ([\w-]+ ){0,2}(hub|bridge|gateway)s?( or [\w-]+)?( is)? (required|needed)|without (a |any )?(hub|bridge|gateway)"
                            r"|hub[- ]free|no extra hub|(hub|gateway) included|with (a )?(hub|gateway)\b", re.I)


def text_of(p):
    s = SCRAPE.get(p["asin"], {})
    return " ".join([s.get("title", p.get("name", "")), *s.get("bullets", []), p.get("model", ""),
                     *map(str, p.get("specs", {}).values())])


def neutral(p, cat, fam):
    if fam not in WIRED_FAMILIES:
        return "na"
    spec = str(p.get("specs", {}).get("neutral", "")).strip().lower()
    if spec.startswith(("not stated", "not applicable", "unknown")):
        spec = ""
    if p.get("features", {}).get("no_neutral") is True and not spec:
        return "no"
    if spec:
        if spec.startswith(("no", "not", "optional", "either", "works without")) or "not required" in spec or "not needed" in spec:
            return "no"
        if spec.startswith(("yes", "required", "needed")):
            return "yes"
    t = text_of(p)
    if NO_NEUTRAL.search(t):
        return "no"
    if NEEDS_NEUTRAL.search(t):
        return "yes"
    return "?"


def hub(p, cat, slug):
    if HUB_PAGE.search(slug):
        return None
    if slug.startswith(("z-wave-", "zigbee-", "thread-", "lutron-")):
        return True
    if slug.startswith(("rf-", "bluetooth-")):
        return False          # RF kits are standalone; Bluetooth works from your phone (a hub only adds remote/voice)
    s = SCRAPE.get(p["asin"], {})
    title = s.get("title", p.get("name", ""))
    t = text_of(p)
    if slug.startswith("matter-"):
        if re.search(r"not support thread|wi-?fi \(matter\)|matter over wi-?fi", t + str(p.get("specs", {})), re.I):
            return False
        return bool(re.search(r"over thread|thread/zigbee|thread protocol|thread border router|\(thread\)|thread \(matter\)|via thread", t, re.I))
    hub_spec = " ".join(str(v) for k, v in p.get("specs", {}).items() if "hub" in k or "bridge" in k or "gateway" in k).lower()
    if hub_spec:
        if re.search(r"\b(none|no hub|not needed|not required|included|built[- ]in|optional)\b", hub_spec):
            return False
        if re.search(r"hub|bridge|gateway|border router", hub_spec):
            return True
    if HUB_NOT_NEEDED.search(title):
        return False
    return bool(HUB_NEEDED.search(title))


SUB_NEEDED = re.compile(r"recordings? (history )?needs? (a )?[\w ]*subscription|paid plan is required to activate|plan required"
                        r"|needs a monitoring plan|locked until you start", re.I)


def sub(p):
    t = " ".join(p.get("cons", []) + [p.get("verdict", "")] + p.get("reasons", []) + [str(v) for v in p.get("specs", {}).values()])
    return bool(SUB_NEEDED.search(t))


def build(show=False):
    out = {}
    for f in sorted((ROOT / "data" / "pages").glob("*.json")):
        cat = json.loads(f.read_text(encoding="utf-8"))
        slug, fam = cat["slug"], cat.get("family", "")
        tags = {}
        for p in cat["products"] + cat.get("avoid", []):
            r = {"neutral": neutral(p, cat, fam), "hub": hub(p, cat, slug), "sub": sub(p)}
            r.update(OVERRIDES.get(p["asin"], {}))
            tags[p["asin"]] = r
            if show:
                print(f"{slug[:24]:24} {p['brand'][:12]:12} {p['model'][:34]:34} neutral={r['neutral']:3} hub={r['hub']!s:5} sub={r['sub']}")
        out[slug] = tags
    (ROOT / "data" / "requirements.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(f"requirements: {sum(len(v) for v in out.values())} products on {len(out)} pages")


if __name__ == "__main__":
    build("--show" in sys.argv)
