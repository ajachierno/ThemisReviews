# ThemisReviews

Static review site for smart home tech, organized by communication protocol (Z-Wave,
Zigbee, Wi-Fi, Bluetooth, Thread, Matter, Lutron Clear Connect, 433 MHz RF). Same build
approach as ToolboxTop10: data in JSON, a zero-dependency Python generator, static output
served by GitHub Pages.

## How it works

- `data/site.json` holds the brand settings and every protocol: summary, verdict, quick
  facts (used by the comparison table), pros, cons, and the list of sub-pages (`subs`).
- `build.py` reads the JSON and writes the site into `docs/`.
- A sub-page shows as "Coming soon" in its protocol's dropdown until its entry in `subs`
  has `"ready": true`. Then it becomes a link to `<slug>.html`.

## Build

```
python build.py
```

Never hand-edit `docs/` (except `docs/assets/` images). Edit the JSON or `build.py` and rebuild.

## Deploy

GitHub Pages serves the `main` branch, `/docs` folder. To use a custom domain, set
`custom_domain` in `data/site.json`, rebuild (this writes `docs/CNAME`), and add the DNS
records at your registrar.

## Category pages

Each ready sub-page has `data/pages/<slug>.json` (products, one avoid pick, awards,
scoring weights, spec/table columns, buyer's guide). Those files are generated, so don't
hand-edit them. The workflow lives in `research/`:

1. `python research/amz.py search research/search-all.json "<query>"` and
   `python research/amz.py products research/prod-all.json <ASIN>...` pull live Amazon data
   with real Chrome (Amazon blocks headless browsers, and it rate-limits fast scraping, so the
   scraper is paced).
2. Write the editorial (verdicts, pros, cons, specs, awards, avoid reasons) in
   `research/editorial/<slug>.json`. Page titles, intros, and buyer's guides are in
   `research/meta.py`.
3. `python research/merge.py <slug>` fills price, rating, review count, title, and image
   from the scrape into `data/pages/<slug>.json`. Numbers never come from the editorial file.
4. Set `"ready": true` on the sub-page in `data/site.json`, then `python build.py`.
5. Commit and push, wait for GitHub Pages to deploy, then `python research/gsc.py submit` to
   resubmit the sitemap to Google Search Console (`python research/gsc.py status` shows
   per-URL index status). Bump `updated` in `data/site.json` when the home page changes.

Every product and avoid pick needs a `"systems"` list naming the smart home systems it
works with (slugs from `data/systems.json`, or `[]` for standalone gear). `merge.py`
refuses to run without it. The build turns the list into the "Works with" icon column.
Rules used so far: Matter-certified = all systems; Z-Wave = Home Assistant, SmartThings,
Hubitat, Homey (minus any the listing excludes); Zigbee 3.0 = the Zigbee-capable systems;
brand-hub and app-based devices = what the listing names, plus Home Assistant where it has
an official integration (TP-Link, Tuya/Smart Life, Lutron Caseta). Icons live in
`SYSTEM_ICONS` in `build.py`; a new system needs an icon there and an entry in
`research/editorial/systems.json`.
