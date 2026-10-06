"""Google Search Console setup and sitemap submission for themisreviews.com.

Uses the gsc-reader service account (key outside the repo, GSC_KEY env var or
~/.config/gsc/toolboxtop10-sa.json).

  python research/gsc.py verify       # DNS-verify the domain (TXT record must already be live) and add Adam as owner
  python research/gsc.py add          # add sc-domain:themisreviews.com to Search Console
  python research/gsc.py submit       # (re)submit the sitemap; run after every new page
  python research/gsc.py status       # sitemap status and per-URL index status (URL Inspection API)
  python research/gsc.py inspect [url ...]   # index status for the given URLs (default: every sitemap URL),
                                             # saved to research/gsc-index.json
  python research/gsc.py queue [N]           # the N (default 10) URLs most worth a "Request indexing" click today
  python research/gsc.py requested url ...   # record that indexing was requested (skipped by queue for 7 days)

Google has no API for the "Request indexing" button (the Indexing API only accepts job
postings and livestreams). The button lives in the Search Console UI, about 10 requests a
day per property; queue picks which URLs get them. Resubmitting the sitemap with accurate
lastmod dates is the automated route for everything else.
"""
import json
import os
import pathlib
import sys
import urllib.parse

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

DOMAIN = "themisreviews.com"
PROPERTY = f"sc-domain:{DOMAIN}"
SITEMAP = f"https://{DOMAIN}/sitemap.xml"
OWNERS = ["ajachierno@gmail.com"]
KEY = pathlib.Path(os.environ.get("GSC_KEY", pathlib.Path.home() / ".config/gsc/toolboxtop10-sa.json"))
SCOPES = ["https://www.googleapis.com/auth/siteverification", "https://www.googleapis.com/auth/webmasters"]
SV = "https://www.googleapis.com/siteVerification/v1"
WM = "https://searchconsole.googleapis.com/webmasters/v3"


def session():
    creds = service_account.Credentials.from_service_account_file(str(KEY), scopes=SCOPES)
    creds.refresh(Request())
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {creds.token}"
    return s, creds.service_account_email


def ok(r, what):
    if not r.ok:
        sys.exit(f"{what} failed: {r.status_code} {r.text[:400]}")
    return r.json() if r.text else {}


def verify(s, sa):
    r = s.post(f"{SV}/webResource", params={"verificationMethod": "DNS_TXT"},
               json={"site": {"type": "INET_DOMAIN", "identifier": DOMAIN}})
    res = ok(r, "Verification")
    rid = res["id"]
    owners = sorted(set(res.get("owners", []) + OWNERS + [sa]))
    res = ok(s.put(f"{SV}/webResource/{urllib.parse.quote(rid, safe='')}",
                   json={"site": res["site"], "owners": owners}), "Adding owners")
    print("Verified. Owners:", ", ".join(res["owners"]))


def add(s):
    ok(s.put(f"{WM}/sites/{urllib.parse.quote(PROPERTY, safe='')}"), "Adding property")
    print("Property added:", PROPERTY)


def submit(s):
    ok(s.put(f"{WM}/sites/{urllib.parse.quote(PROPERTY, safe='')}/sitemaps/{urllib.parse.quote(SITEMAP, safe='')}"),
       "Sitemap submit")
    print("Sitemap submitted:", SITEMAP)


def status(s):
    site = urllib.parse.quote(PROPERTY, safe="")
    sm = ok(s.get(f"{WM}/sites/{site}/sitemaps/{urllib.parse.quote(SITEMAP, safe='')}"), "Sitemap status")
    print(f"Sitemap: submitted {sm.get('lastSubmitted')} downloaded {sm.get('lastDownloaded')} "
          f"pending={sm.get('isPending')} errors={sm.get('errors')} warnings={sm.get('warnings')}")
    for c in sm.get("contents", []):
        print(f"  {c.get('type')}: submitted {c.get('submitted')}, indexed {c.get('indexed', 'n/a')}")
    urls = requests.get(SITEMAP, timeout=30).text
    for u in [x.split("</loc>")[0] for x in urls.split("<loc>")[1:]]:
        r = s.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                   json={"inspectionUrl": u, "siteUrl": PROPERTY})
        res = r.json().get("inspectionResult", {}).get("indexStatusResult", {}) if r.ok else {}
        print(f"  {res.get('coverageState', r.status_code if not r.ok else 'unknown'):38} {u}")


HERE = pathlib.Path(__file__).parent
INDEX = HERE / "gsc-index.json"
REQUESTED = HERE / "gsc-requested.json"


def sitemap_urls():
    xml = requests.get(SITEMAP, timeout=30).text
    out = []
    for chunk in xml.split("<url>")[1:]:
        loc = chunk.split("<loc>")[1].split("</loc>")[0]
        mod = chunk.split("<lastmod>")[1].split("</lastmod>")[0] if "<lastmod>" in chunk else ""
        out.append((loc, mod))
    return out


def inspect(s, urls=None):
    import datetime
    data = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else {}
    targets = urls or [u for u, _m in sitemap_urls()]
    for i, u in enumerate(targets, 1):
        r = s.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                   json={"inspectionUrl": u, "siteUrl": PROPERTY})
        if not r.ok:
            print(f"  {r.status_code} {u} {r.text[:150]}")
            continue
        res = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
        data[u] = {"state": res.get("coverageState", "unknown"), "verdict": res.get("verdict"),
                   "crawled": res.get("lastCrawlTime"), "checked": datetime.datetime.utcnow().isoformat(timespec="seconds")}
        print(f"  [{i}/{len(targets)}] {data[u]['state']:40} {u}")
    INDEX.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    states = {}
    for u in targets:
        if u in data:
            states[data[u]["state"]] = states.get(data[u]["state"], 0) + 1
    print("Summary:", ", ".join(f"{v} {k}" for k, v in sorted(states.items(), key=lambda x: -x[1])))


def priority(url):
    """Lower sorts first: home, then product-type and trust pages, then review pages."""
    path = url.rsplit("/", 1)[-1]
    if path == "":
        return 0
    if path.startswith("smart-") or path in ("how-we-rank.html", "about.html"):
        return 1
    return 2


def queue(n=10):
    import datetime
    if not INDEX.exists():
        sys.exit("Run: python research/gsc.py inspect   (no index data yet)")
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    asked = json.loads(REQUESTED.read_text(encoding="utf-8")) if REQUESTED.exists() else {}
    week_ago = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    mods = dict(sitemap_urls())
    todo = []
    for u, mod in mods.items():
        st = data.get(u, {}).get("state", "unknown")
        if st.startswith("Submitted and indexed") or st.startswith("Indexed"):
            # indexed, but changed since Google last crawled it: worth a recrawl
            crawled = (data[u].get("crawled") or "")[:10]
            if not (mod and crawled and mod > crawled):
                continue
            reason = f"changed {mod}, crawled {crawled}"
        else:
            reason = st
        if asked.get(u, "") >= week_ago:
            continue
        todo.append((reason.startswith("changed"), priority(u), u, reason))
    todo.sort()
    pick = todo[:n]
    print(f"{len(todo)} URLs could use a request; today's {len(pick)}:")
    for _c, _p, u, why in pick:
        print(f"  {u}   ({why})")
    (HERE / "gsc-queue.txt").write_text("\n".join(u for *_x, u, _w in pick) + "\n", encoding="utf-8")


def requested(urls):
    import datetime
    asked = json.loads(REQUESTED.read_text(encoding="utf-8")) if REQUESTED.exists() else {}
    for u in urls:
        asked[u] = datetime.date.today().isoformat()
    REQUESTED.write_text(json.dumps(asked, indent=1) + "\n", encoding="utf-8")
    print(f"Recorded {len(urls)} request(s).")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    args = sys.argv[2:]
    if cmd == "queue":
        queue(int(args[0]) if args else 10)
    elif cmd == "requested":
        requested(args)
    else:
        s, sa = session()
        {"verify": lambda: verify(s, sa), "add": lambda: add(s), "submit": lambda: submit(s),
         "status": lambda: status(s), "inspect": lambda: inspect(s, args or None)}[cmd]()
