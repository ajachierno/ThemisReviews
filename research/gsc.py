"""Google Search Console setup and sitemap submission for themisreviews.com.

Uses the gsc-reader service account (key outside the repo, GSC_KEY env var or
~/.config/gsc/toolboxtop10-sa.json).

  python research/gsc.py verify       # DNS-verify the domain (TXT record must already be live) and add Adam as owner
  python research/gsc.py add          # add sc-domain:themisreviews.com to Search Console
  python research/gsc.py submit       # (re)submit the sitemap; run after every new page
  python research/gsc.py status       # sitemap status and per-URL index status (URL Inspection API)

Google has no API for the "Request indexing" button; resubmitting the sitemap with
accurate lastmod dates is the supported automated route.
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


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    s, sa = session()
    {"verify": lambda: verify(s, sa), "add": lambda: add(s), "submit": lambda: submit(s), "status": lambda: status(s)}[cmd]()
