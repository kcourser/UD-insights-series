#!/bin/bash
# run-sync.sh — pull the Substack feed locally and push the result.
#
# GitHub Actions runners are blocked by Substack's Cloudflare (403 on both
# /feed and /api/v1/archive), so the fetch has to originate from a residential
# IP. This script does the whole cycle: pull, sync, commit, push.
#
# Manual:   ./run-sync.sh
# Schedule: see the crontab line at the bottom of this file.

set -euo pipefail

REPO="/Users/kevin/Library/CloudStorage/OneDrive-UprightDigital/Podcasts/PODCAST SHOWS/Transcript Files - Github/UD-insights-series"
LOG="$REPO/sync.log"

cd "$REPO"

{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') ==="

  git pull --quiet --rebase || { echo "git pull failed"; exit 1; }

  python3 sync_series.py --default-series desert-capital

  rm -f series.json.bak

  if git diff --quiet -- series.json; then
    echo "No change."
  else
    git add series.json
    git commit -q -m "chore: sync series.json from Substack feed"
    git push --quiet
    echo "Pushed."
  fi
} >> "$LOG" 2>&1

# ---------------------------------------------------------------------------
# To run automatically every day at 8:15am, run `crontab -e` and add:
#
# 15 8 * * * "/Users/kevin/Library/CloudStorage/OneDrive-UprightDigital/Podcasts/PODCAST SHOWS/Transcript Files - Github/UD-insights-series/run-sync.sh"
#
# Requires the Mac to be awake. Check results with:  tail -20 sync.log
# ---------------------------------------------------------------------------
