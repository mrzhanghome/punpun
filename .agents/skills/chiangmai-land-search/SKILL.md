---
name: chiangmai-land-search
description: >-
  Run a thorough weekly search for self-reliant homestead land near Chiang Mai
  (Jon Jandai / Pun Pun style: 1-5 Rai, budget <= 2.5M THB, Chanote/NS3G, within ~1 hour of Chiang
  Mai city), re-verify existing listing URLs in data/plots.json, merge newly
  discovered plots tagged by week, regenerate index.html, and push the live
  bilingual (EN/TH) GitHub Pages board. Use when the user asks to run a weekly
  land search, update the Chiang Mai land list, check sold listings, or add/edit
  plots on the Pun Pun land board.
---

# Chiang Mai Weekly Land Search & Board Updater

## Overview
Maintains the live bilingual (`EN` + `ภาษาไทย`) Chiang Mai self-reliance land shortlist hosted on GitHub Pages (`https://mrzhanghome.github.io/punpun/`). Each weekly run:
1. Exports existing listings from `data/plots.json` for deduplication.
2. Politely re-checks existing listing URLs and marks dead/sold listings.
3. Searches Thai & English portals (including Facebook) across all 3 Chiang Mai target zones for fresh 1–5 Rai plots within the budget (currently ≤ ฿2.5M total). Plots with confirmed Chanote/NS3G or unstated (`unknown`) title deeds are included; explicit `ส.ป.ก.` / `ภ.บ.ท.5` plots are excluded.
4. Validates, merges, and tags new plots with `Week N`, renders `index.html`, and commits/pushes to GitHub Pages.

## Dependencies
- **Browser / Web Research Capability**: Use Antigravity's `browser` subagents (3 parallel subagents — one per zone) when running in Antigravity, or Claude Code's web/browser tools + parallel subagents when running in Claude Code.
- **Reference Materials**: Read [references/search_portals.md](./references/search_portals.md) for target districts, portal URLs, Thai search strings, Pun Pun homestead criteria, and the exact `plots.json` schema.
- **CLI Helper**: [scripts/land_board.py](./scripts/land_board.py) (stdlib Python 3, invoked via `uv run`).

## Quick Start
```bash
# 1. Inspect current week & existing URLs
uv run .agents/skills/chiangmai-land-search/scripts/land_board.py summary \
  --input data/plots.json --output /tmp/land_summary.json

# 2. Re-check existing listing links (polite 1 req/s rate limit; marks 404/sold)
uv run .agents/skills/chiangmai-land-search/scripts/land_board.py check-links \
  --input data/plots.json --output /tmp/link_report.json --mark-dead

# 3. After browser research produces /tmp/weekN_new_plots.json, merge into data/plots.json
uv run .agents/skills/chiangmai-land-search/scripts/land_board.py add-plots \
  --input data/plots.json --batch /tmp/weekN_new_plots.json --week 2 --output data/plots.json

# 4. Re-render index.html and verify before committing
uv run .agents/skills/chiangmai-land-search/scripts/land_board.py render \
  --input data/plots.json --html index.html
```

## Utility Scripts (`scripts/land_board.py`)

| Subcommand | Purpose | Key Flags |
|---|---|---|
| `summary` | Writes current week, counts by status/district/week, and all existing URLs to `--output`. | `--input`, `--output` |
| `check-links` | Checks active plots at 1 req/s; classifies `live`, `dead`, `sold_detected`, or `needs_browser_check`. | `--input`, `--output`, `--mark-dead`, `--include-closed` |
| `add-plots` | Validates required fields, rejects `ส.ป.ก.` / `ภ.บ.ท.5`, skips plots outside `criteria` (size/budget; override with `--allow-out-of-criteria`), deduplicates by URL, computes `price_per_rai_thb`, stamps week/date. | `--input`, `--batch`, `--week`, `--date`, `--output` |
| `apply-criteria` | Optionally updates `criteria` (`--min-rai`, `--max-rai`, `--max-budget`) then auto-marks existing plots outside size/budget as `passed` (skip with `keep_despite_criteria: true` on a plot). | `--input`, `--output`, optional criteria flags |
| `update-status` | Updates an existing plot's status (`shortlisted`/`visit`/`contacted`/`passed`/`sold`) and appends bilingual notes. | `--input`, `--id`, `--status`, `--note-en`, `--note-th`, `--output` |
| `render` | Deterministically rewrites `index.html` between `PLOTS_START..PLOTS_END`, hero badges/stats, and side-nav counts. | `--input`, `--html` |

## Weekly Execution Workflow

### Step 1 — Audit Current Board & Re-Verify Existing Links
1. Run `summary` and `check-links --mark-dead` (writing reports to `/tmp/`).
2. Review `/tmp/link_report.json`:
   - Listings returning `dead` or `sold_detected` are automatically marked `status: "sold"`.
   - Listings returning `needs_browser_check` (403/429 bot filter) should be spot-checked in the browser during Step 2 (never bypass CAPTCHAs — if gated, leave status unchanged and note it).
3. Determine `next_week = current_week + 1`.

### Step 2 — Parallel Browser Research Across 3 Chiang Mai Zones
Read [references/search_portals.md](./references/search_portals.md) and search all 3 zones in parallel (passing the list of already-known URLs from `/tmp/land_summary.json` so researchers skip duplicates):
1. **Zone A:** Mae Taeng (`อ.แม่แตง` — Cho Lae, Inthakhin, Khi Lek, Ban Pao, Mae Ho Phra)
2. **Zone B:** Doi Saket & Mae On (`อ.ดอยสะเก็ด`, `อ.แม่ออน`)
3. **Zone C:** Mae Wang, San Pa Tong & Samoeng (`อ.แม่วาง`, `อ.สันป่าตอง`, `อ.สะเมิง`)

Sources: Teedin108, DotProperty, FazWaz, LivingInsider **and Facebook** (Marketplace + group/post search through the user's logged-in browser session — follow the read-only Facebook rules in `references/search_portals.md`; use `listing_source_en: "View Facebook Post"` and the post permalink as `listing_url`).

Research rules:
- Open actual listing detail pages to verify listings are **live**, extract exact size (`Rai-Ngan-Wah` and `sq.m`), exact total THB price, title deed, water/road/power details, and seller contact if public.
- **Strictly exclude** any plot that explicitly states *Sor Por Gor (ส.ป.ก. 4-01)* or *Por Bor Tor 5 (ภ.บ.ท.5)*. If a listing does not mention its title deed type, **include it** with `title_deed_status: "unknown"`, `title_deed_en: "Unknown (Ask Seller)"`, `title_deed_th: "ไม่ระบุ (ต้องถามผู้ขาย)"`.
- **Never attempt to solve or bypass CAPTCHAs or Cloudflare anti-bot challenges** — skip any gated site and use another accessible portal (`Teedin108`, `DotProperty`, `FazWaz`, `LivingInsider`, **Facebook**).
- **Current criteria (stored in `data/plots.json` → `criteria`): 1–5 Rai, total price ≤ ฿2.5M.** Read it from the JSON, not from memory — the user may change it. If the user changes criteria, run `apply-criteria` with the new flags first.
- Aim for **2–4 strong newly discovered plots per zone** that fit the criteria (fewer is fine if the market has little in budget — never pad with out-of-budget plots).

### Step 3 — Merge, Render & Verify
1. Save newly curated listings in bilingual English + Thai (`EN` + `ภาษาไทย`) into `/tmp/week<N>_new_plots.json` following the schema in [references/search_portals.md](./references/search_portals.md).
2. Run `add-plots --week <N>` to validate, deduplicate, and update `data/plots.json`.
3. Run `render --input data/plots.json --html index.html` to regenerate `index.html`.
4. Verify `git diff --stat` and check that all new plots render cleanly with valid links, Thai + English copy, and updated week counts.

### Step 4 — Publish to GitHub Pages & Summarize
1. Commit `data/plots.json` and `index.html` with message `"Update Week <N> Chiang Mai land search results"` and push to `origin main`.
2. Report to the user:
   - Any existing plots marked sold/removed since last week.
   - A compact comparison table of the newly added Week `<N>` plots.
   - The live URL: `https://mrzhanghome.github.io/punpun/`.

## Rate Limiting
- `scripts/land_board.py check-links` enforces a strict **1 request/second** limit via `time.monotonic()` with exponential backoff on transient 5xx/429 errors.
- If a portal returns HTTP 403/429 or an anti-bot challenge page, the script stops immediately and logs `needs_browser_check` instead of hammering the server.

## Common Mistakes
- **Editing `index.html` plot cards by hand:** Always edit `data/plots.json` via `land_board.py` and run `render`; manual edits inside `<!-- PLOTS_START -->..<!-- PLOTS_END -->` will be overwritten on the next render.
- **Confusing per-Rai price with total price on Teedin108:** Teedin108 header fields frequently show the *per-Rai* price (e.g., `฿450,000`) while the description gives the total (e.g., `฿1,500,000`). Always read the full listing body and verify `price_total_thb / size_rai_num`.
- **Letting *Sor Por Gor (ส.ป.ก.)* slip in from Samoeng or hillside Mae Taeng:** Always confirm Red Garuda Chanote (`โฉนด น.ส.4 จ.`) or Green Garuda (`น.ส.3 ก.`), or explicitly flag `title_deed_status: "verify"` with a top warning bullet when unstated in lowland agricultural zones.
