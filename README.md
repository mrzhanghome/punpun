# Chiang Mai Self-Reliance Land Search Board (บอร์ดคัดเลือกที่ดินเชียงใหม่ วิถีพึ่งตนเอง)

Bilingual (English + ภาษาไทย) weekly land shortlist and evaluation guide for finding self-reliant homestead land within ~1 hour of Chiang Mai city, inspired by **Jon Jandai & Pun Pun Center for Self-Reliance (บ้านพันพรรณ อ.แม่แตง)**.

## 🌐 Live GitHub Pages Site
**[https://mrzhanghome.github.io/punpun/](https://mrzhanghome.github.io/punpun/)**

## Structure
1. **Thai Land Title Deeds: What to Buy vs. What to Avoid** (`Chanote` vs `Nor Sor 3 Gor` vs `Sor Por Gor 4-01`).
2. **Top 5 Target Areas Within ~1 Hour of Chiang Mai** (Mae Taeng, Doi Saket/Mae On, San Pa Tong/Mae Wang, Samoeng, Phrao).
3. **Field Questions for Sellers, Neighbors & Village Headmen** (Water, 2024 Flood History, Soil for Adobe Bricks, Public Road Frontage).
4. **Weekly Land Search Results** — Backed by `data/plots.json`, filterable by status, district, and week, and sortable by price per rai or size.

## 🔁 Running Next Week's Search (Antigravity & Claude Code)
This repository includes a reusable project skill (`chiangmai-land-search`) installed for both **Antigravity** (`.agents/skills/chiangmai-land-search/`) and **Claude Code** (`.claude/skills/chiangmai-land-search/` + `/weekly-land-search` command):

- **In Antigravity:** Start a new session in this repo and say: *"Run our weekly Chiang Mai land search and update the board."*
- **In Claude Code:** Type `/weekly-land-search` (or ask naturally to run the `chiangmai-land-search` skill).
- **Manual CLI usage:**
  ```bash
  uv run .agents/skills/chiangmai-land-search/scripts/land_board.py summary --input data/plots.json --output /tmp/summary.json
  uv run .agents/skills/chiangmai-land-search/scripts/land_board.py check-links --input data/plots.json --output /tmp/links.json --mark-dead
  uv run .agents/skills/chiangmai-land-search/scripts/land_board.py render --input data/plots.json --html index.html
  ```
