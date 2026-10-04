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
