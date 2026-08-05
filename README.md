# UPRT+ Insights Series Browser

**Repo:** https://github.com/kcourser/UD-insights-series (**public**)  

Interactive **Substack series intro** for the UD 2026 site (Webflow embed).

**Not a full article reader.** On-site path:

1. Series cards (Desert Capital, Clearsync Connect, …)
2. Horizontal article rail (thumbnail + one-liner)
3. Summary panel (bullets + meta)
4. **Read on Substack** (canonical long-form)

Mirrors the podcast network pattern: Hermes-owned embed + JSON; Claude/Webflow hosts the page.

## Files

| File | Role |
|------|------|
| `series.json` | Series + articles data |
| `ud-insights-series.html` | Full inline embed (paste into Webflow **or** open via preview) |
| `ud-insights-series.js` | Optional self-mount loader |
| `preview.html` | Local browser preview shell |

## Local preview

```bash
cd "…/UD-insights-series"
python3 -m http.server 8765
# open http://127.0.0.1:8765/preview.html
```

## Webflow (v1 — simplest)

1. Add an **Embed** on the UPRT+ / Insights section.
2. Paste the full contents of `ud-insights-series.html`.
3. Host `series.json` on GitHub (or CDN) and set on the root:

```html
<div id="ud-insights" data-series-url="https://cdn.jsdelivr.net/gh/kcourser/UD-insights-series@main/series.json" …>
```

If pasting the whole file, edit the `DATA_URL` fallback inside the script or add `data-series-url` on `#ud-insights` before the script runs — the script already reads `data-series-url`.

**After GitHub repo exists**, preferred mount:

```html
<div id="ud-insights-mount"
     data-series-url="https://cdn.jsdelivr.net/gh/kcourser/UD-insights-series@main/series.json"></div>
<script
  src="https://cdn.jsdelivr.net/gh/kcourser/UD-insights-series@main/ud-insights-series.js"
  defer></script>
```

## Brand

UD 2026 tokens (aligned with podcast `uprt-network-ud`):

- Navy: `#01060F` / `#010E1E` / `#0F1B35` / `#1E2A4A`
- Text: `#F2F7FD` / `#9FB2CC`
- Accents: `#4DA9F0`, `#A8E0FF`, `#FF3DB0`
- Font: Poppins (site-loaded)

## Data contract

**Series:** `id`, `name`, `promise`, `spokesperson`, `verticals[]`, `cover_gradient[]`, `accent`, `substack_home`, `updated`  
**Article:** `id`, `series_id`, `title`, `one_liner`, `summary_bullets[]`, `date`, `read_min`, `verticals[]`, `substack_url`, `thumb_label`, `start_here`, `featured`

Placeholder Substack URLs are `https://substack.com/` — replace with real publication links before production.

## Owner

Hermes CTO · 2026-08-04  
PARA: `02 Projects/Upright Digital/website-insights-series.md`
