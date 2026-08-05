# Handoff: Substack feed sync → Hermes

**From:** Claude (UD 2026 Webflow project) · **To:** Hermes CTO
**Date:** 2026-08-05
**Status:** Working locally; needs a host that Substack doesn't block

## What this is

`sync_series.py` merges the live Upright Digital Substack feed into `series.json`,
replacing the prototype's demo rows with real posts. It respects your data contract
and does not fork the embed.

## Field ownership

| Owner | Fields |
|-------|--------|
| **RSS** | `title`, `date`, `substack_url`, `read_min`, `image` |
| **Humans** | `one_liner`, `summary_bullets`, `verticals`, `thumb_label`, `display_title` (once customized), `paired_episode_id` |
| **Code** | `start_here` / `featured` — via the `CURATION` map in the script, so the editor's cut survives every run |
| **Preserved** | Any field already present that the script doesn't manage, including keys added to the contract later |

Matching is by `substack_url` first, then normalized title. Non-destructive:
writes `series.json.bak`, and only prunes rows when passed `--prune-demo`.

## Two additions to the contract

- **`display_title`** — seeded from the feed, then human-owned. Lets the site carry a
  punchier headline while Substack keeps the canonical one. Sync stops touching it
  once it diverges from `title`.
- **`paired_episode_id`** — empty string default, keyed to `episodes.json` in
  `UD-podcast-network`. ClearSync Connect ships each issue alongside a companion
  *IT Crowd* episode; the schema previously had no way to express that.

Both are additive. The embed ignores unknown keys, so nothing breaks if unused.

## The blocker

**Substack's Cloudflare returns 403 to GitHub Actions runners.** Confirmed on both
`/feed` and `/api/v1/archive`, with browser-realistic headers. This is IP reputation,
not User-Agent — header tuning does not fix it.

The same script from Kevin's Mac pulls all 20 posts fine.

Current workaround: `run-sync.sh` + a weekly Wednesday cron on Kevin's machine.
Works, but depends on his laptop being awake.

## The ask

**Resolved 2026-08-05:** Hermes runs on Kevin's Mac, and `curl` against the feed from
that machine returns **200**. So the sync works under Hermes.

Note what this does and doesn't change: same machine means the same
laptop-must-be-awake dependency. Moving the job to Hermes is an ownership change,
not an infrastructure one.

Suggested split:

- **cron owns the trigger** — `run-sync.sh`, weekly Wednesday. Fires whether or not an
  agent session is live, so it's the more reliable scheduler.
- **Hermes owns the file** — `series.json` behavior, schema changes, and diagnosis when
  a sync looks wrong. Already your lane per `HANDOFF-to-Claude.md`.

If you'd rather own the trigger too, take it — just retire the crontab line at the
bottom of `run-sync.sh` so the job doesn't run twice.

## Deferred from v1 — design system reconciliation

**Status 2026-08-05:** the embed is placed on `/media` (Webflow, `ud-insights-embed`
wrapper containing `#ud-insights-mount`) but set to `display: none`. Markup and data
attributes are intact; unhiding is a one-property change.

### Why

Side by side with the page, the embed reads as a different design system. Specific
mismatches Kevin flagged:

- **Too dark.** The embed's `#01060F` base is deeper than the page's section
  background, so the module sits in a visible well rather than on the page.
- **Rounded corners.** Card radii don't match the site's `ud-card`.
- **Different CTAs.** The embed's buttons don't match `ud-btn` / `ud-btn-line`.
- **Images are hard to control** (see below).

This is not a taste disagreement. The embed was matched to the podcast graph's v7-UD
tokens; the Webflow site has its own class system (`ud-card`, `ud-btn`, `ud-h2`,
`ud-section`, `ud-container`, `ud-eyebrow`). Both are "on brand" against different
references. Nobody had them on one screen until now.

### The ask — inherit, don't repaint

Repainting to today's hex values recreates the same drift the next time the site
changes. Instead:

1. **Consume CSS custom properties from the page** rather than hard-coding. Read
   `--ud-*` vars off `:root` / the wrapper, with the current values as fallbacks:

   ```css
   background: var(--ud-surface, #0F1B35);
   border-radius: var(--ud-radius-card, 4px);
   ```

2. **Match the existing component classes.** Cards should read as `ud-card`; the
   "Read on Substack" CTA should read as `ud-btn ud-btn-line` — same radius, weight,
   border treatment, hover.

3. **Don't set a background on the module root.** Let the section behind it show
   through. That alone fixes "too dark."

The navy vs. black decision is settled (navy — the campaign hero has no black in it),
but inheriting means the embed follows if that ever changes.

### Images

`series.json.image` is populated from Substack `cover_image` and is RSS-owned, so the
weekly sync overwrites any manual edit. Proposed fix, mirroring `display_title`:

- Add **`display_image`** — wins over `image` when set, never touched by sync.
- Embed reads `display_image || image`.

One-line change in `sync_series.py` (add to the human-owned set) plus the fallback in
the embed.

### Not blocking v1

The live section ships with two static series cards and "Read on Substack" — coherent
and on-brand. The interactive rail is depth, not table stakes. The data pipeline is
done and keeps refreshing weekly regardless of what renders it.



## Also unresolved

- **Substack sections aren't configured.** No `/feed/s/<slug>` endpoints, and the main
  feed carries no category tags, so series assignment falls back to
  `--default-series desert-capital` plus the `TITLE_OVERRIDES` map. Setting up real
  sections in Substack would make assignment automatic and permanent.
- **`Clearsync Connect`** in `series.json` vs **`ClearSync Connect`** on the actual
  publication. Capital S.
- **`Osama Rizbe`** — carried from the 2026 Marketing Plan, still unverified. The
  closest public energy analyst is Osama Rizvi. Confirm before it ships.
- The GitHub Action (`.github/workflows/sync-substack.yml`) is retained with
  `workflow_dispatch` only; its schedule was removed since scheduled runs always 403.
