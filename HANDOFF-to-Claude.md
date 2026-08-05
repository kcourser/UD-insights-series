# Handoff: UPRT+ Insights Series browser → Claude (UD Website 2026)

**From:** Hermes CTO · **To:** Claude (UD 2026 Webflow project)  
**Date:** 2026-08-04  
**Status:** Prototype ready for section placement; data still placeholder

## Is a separate Hermes project a bad idea?

**No.** Use the same split as the podcast network:

| Surface | Owner |
|---------|--------|
| Webflow page, IA, section layout, CMS collection if any, brand art | **Claude / Kevin** (UD Website 2026) |
| Interactive embed HTML/JS + `series.json` behavior | **Hermes CTO** |
| Real Substack URLs, titles, one-liners, summary bullets | **Kevin editorial** (either thread can edit JSON) |
| GitHub push / jsDelivr (when Claude can’t reach GitHub) | **Hermes** |

Do **not** rebuild this interaction inside Webflow native interactions or a second Claude-only HTML fork. One embed, one data file.

## Product (locked)

```
Series cards → horizontal article rail (thumb + one-liner)
  → on-site summary panel (bullets) → Read on Substack
```

- Not a full article reader  
- Not Three.js bookshelf  
- Sibling to UPRT+ podcast graph (discovery on UD → depth off-site)

## Series (from UD 2026 Marketing Plan)

1. **Desert Capital** — UAE/ME energy (Osama Rizbe)  
2. **Clearsync Connect** — power, AI, tech (Richard Rodriguez)

## Where files live

**GitHub (Claude-friendly):** https://github.com/kcourser/UD-insights-series (**public**)  

**Raw / CDN:**
- HTML: https://cdn.jsdelivr.net/gh/kcourser/UD-insights-series@main/ud-insights-series.html  
- JS: https://cdn.jsdelivr.net/gh/kcourser/UD-insights-series@main/ud-insights-series.js  
- Data: https://cdn.jsdelivr.net/gh/kcourser/UD-insights-series@main/series.json  
- Handoff: https://github.com/kcourser/UD-insights-series/blob/main/HANDOFF-to-Claude.md  

**Mac / OneDrive checkout:**
```
…/OneDrive-UprightDigital/Podcasts/PODCAST SHOWS/Transcript Files - Github/UD-insights-series/
```

PARA: `02 Projects/Upright Digital/website-insights-series.md`

## What Claude should do in Webflow

1. Add / open the **UPRT+** page section for article series (or Insights).
2. Place heading + short franchise line (site copy — Claude).
3. Add an **Embed** element full-width under it.
4. **Preferred (GitHub live):** use the jsDelivr mount below.  
   **Alt:** paste entire contents of `ud-insights-series.html` from the repo.
5. Ensure page loads **Poppins** (already on UD 2026).
6. Give the section enough height (~720px desktop; embed is responsive).
7. Do **not** nest the embed inside a tiny fixed-height div that clips the panel.

### Webflow embed (repo is **public**)

```html
<div id="ud-insights-mount"
     data-series-url="https://cdn.jsdelivr.net/gh/kcourser/UD-insights-series@main/series.json"></div>
<script
  src="https://cdn.jsdelivr.net/gh/kcourser/UD-insights-series@main/ud-insights-series.js"
  defer></script>
```

Same pattern as podcast:

```html
<div id="uprt-network-mount"></div>
<script src="https://cdn.jsdelivr.net/gh/kcourser/UD-podcast-network@main/uprt-network-ud.js" defer></script>
```

**Alt:** paste entire contents of `ud-insights-series.html` into the Embed.

## What Claude should NOT do

- Re-implement the rail/panel in Webflow Ix2 as a parallel version  
- Put full Substack HTML body on the UD page  
- Change navy brand tokens without coordinating (match podcast v7-UD)  
- Fork a second copy of the HTML only in Claude Project files (drift)

## Data handoff

Edit `series.json` (or send Hermes real rows):

**Series:** `id`, `name`, `promise`, `spokesperson`, `verticals[]`, `cover_gradient[]`, `accent`, `substack_home`, `updated`  
**Article:** `id`, `series_id`, `title`, `one_liner`, `summary_bullets[]`, `date`, `read_min`, `verticals[]`, `substack_url`, `thumb_label`, `start_here`, `featured`

Current articles are **demo copy**; Substack links are stubs.

## Brand tokens (match podcast v7-UD)

`#01060F` `#010E1E` `#0F1B35` `#1E2A4A` · text `#F2F7FD` `#9FB2CC` · accents `#4DA9F0` `#A8E0FF` `#FF3DB0`

## Coordination checklist

- [ ] Claude: section + embed paste on staging (`ud-2026.webflow.io`)
- [ ] Kevin: real Substack home + per-article URLs  
- [ ] Kevin/Hermes: replace placeholder titles/deks/bullets  
- [ ] Hermes: create/push `UD-insights-series` GitHub when ready  
- [ ] Claude: swap to jsDelivr mount post-push  
- [ ] Optional: analytics events (series open / summary / Substack CTR)

## One sentence for the Claude project

> Hermes owns a drop-in UPRT+ Insights Series embed (JSON + HTML) next to the podcast network; Claude places it on the Webflow UPRT+/Insights section and supplies layout/chrome — do not rebuild the interaction in Webflow.
