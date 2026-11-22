---
description: Run a thorough weekly Chiang Mai self-reliance land search, re-check existing listings, update data/plots.json & index.html, and push to GitHub Pages.
---

Load and follow the complete runbook in `.agents/skills/chiangmai-land-search/SKILL.md` (and its reference guide `.agents/skills/chiangmai-land-search/references/search_portals.md`).

User arguments (optional week number, focus districts, or budget overrides): $ARGUMENTS

Current criteria live in `data/plots.json` → `criteria` (1–5 rai, ≤ ฿2.5M total); respect them.

Execute all 4 steps:
1. Run `summary` and `check-links --mark-dead` via `uv run .agents/skills/chiangmai-land-search/scripts/land_board.py`.
2. Perform thorough parallel research across Mae Taeng, Doi Saket/Mae On, Mae Wang/San Pa Tong/Samoeng, and Lamphun (Mueang Lamphun/Pa Sang/Ban Thi, optional Mae Tha) (skipping duplicates already in `data/plots.json`, strictly excluding Sor Por Gor / Por Bor Tor 5, and never bypassing CAPTCHAs).
3. Merge new bilingual (EN + Thai) listings with `add-plots`, regenerate `index.html` with `render`, and verify cleanly.
4. Commit and push to `origin main`, then present a clear summary table of sold/updated plots and new Week N findings along with the live link `https://mrzhanghome.github.io/punpun/`.
