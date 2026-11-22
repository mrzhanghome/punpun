#!/usr/bin/env python3
"""CLI helper for managing the Chiang Mai Self-Reliance Land Search Board.

Subcommands:
  summary       Export compact board stats & existing URLs (for deduping new searches).
  check-links   Politely check existing listing URLs (1 req/s) for 404/sold status.
  add-plots     Validate, deduplicate, and merge a weekly batch of plots into plots.json.
  update-status Update a single plot's status (shortlisted/visit/contacted/passed/sold) & notes.
  render        Deterministically render the weekly results & stats into index.html.

Stdlib only — runnable with `uv run .agents/skills/chiangmai-land-search/scripts/land_board.py`.
"""

from __future__ import annotations

import argparse
from datetime import date
import html
import json
from pathlib import Path
import re
import sys
import time
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request


REQUESTS_PER_SECOND = 1.0  # Polite default rate limit for public listing portals
VALID_STATUSES = ("shortlisted", "visit", "contacted", "passed", "sold")
VALID_DISTRICTS = {
    "mae-taeng": ("Mae Taeng", "อ.แม่แตง"),
    "doi-saket": ("Doi Saket", "อ.ดอยสะเก็ด"),
    "mae-on": ("Mae On", "อ.แม่ออน"),
    "mae-wang": ("Mae Wang", "อ.แม่วาง"),
    "san-pa-tong": ("San Pa Tong", "อ.สันป่าตอง"),
    "samoeng": ("Samoeng", "อ.สะเมิง"),
    "phrao": ("Phrao", "อ.พร้าว"),
}
FORBIDDEN_DEED_PATTERNS = (
    r"ส\.ป\.ก",
    r"สปก",
    r"ภ\.บ\.ท\.?\s*5",
    r"ภบท\.?\s*5",
    r"ส\.ท\.ก",
    r"\bsor\s*por\s*gor\b",
    r"\bpor\s*bor\s*tor\b",
)
THAI_MONTHS = (
    "",
    "ม.ค.",
    "ก.พ.",
    "มี.ค.",
    "เม.ย.",
    "พ.ค.",
    "มิ.ย.",
    "ก.ค.",
    "ส.ค.",
    "ก.ย.",
    "ต.ค.",
    "พ.ย.",
    "ธ.ค.",
)
EN_MONTHS = (
    "",
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)


class RateLimitError(Exception):
    """Raised when a target site returns HTTP 429 after retries."""


def normalize_url(url: str) -> str:
    parsed = urllib_parse.urlsplit(url.strip())
    path = parsed.path.rstrip("/")
    return f"{parsed.scheme.lower()}://{parsed.netloc.lower()}{path}"


def load_json(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error reading JSON file {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def write_json(data: object, output_file: str) -> None:
    try:
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"Success! Data written to: {output_file}")
    except (OSError, TypeError) as exc:
        print(f"Error writing JSON file {output_file}: {exc}", file=sys.stderr)
        sys.exit(1)


def format_dates(iso_str: str | None = None) -> tuple[str, str, str]:
    d = date.fromisoformat(iso_str) if iso_str else date.today()
    en = f"{EN_MONTHS[d.month]} {d.day}, {d.year}"
    be_short = (d.year + 543) % 100
    th = f"{d.day} {THAI_MONTHS[d.month]} {be_short:02d}"
    return d.isoformat(), en, th


def format_thb_short(amount: int) -> str:
    if amount >= 1_000_000:
        return f"฿{amount / 1_000_000:.2f}M"
    return f"฿{round(amount / 1_000):,}k"


def format_thb_per_rai(amount: int) -> str:
    if amount >= 1_000_000:
        return f"฿{amount / 1_000_000:.2f}M/ไร่"
    return f"฿{round(amount / 1_000):,}k/ไร่"


def check_forbidden_deeds(plot: dict) -> str | None:
    deed_fields = " ".join(
        str(plot.get(k, ""))
        for k in ("title_deed_en", "title_deed_th", "title_en", "title_th")
    )
    for pat in FORBIDDEN_DEED_PATTERNS:
        if re.search(pat, deed_fields, re.IGNORECASE):
            return f"Forbidden title deed pattern '{pat}' found in title/deed fields."
    return None


def cmd_summary(args: argparse.Namespace) -> None:
    board = load_json(args.input)
    plots = board.get("plots", [])
    by_status: dict[str, int] = {}
    by_district: dict[str, int] = {}
    by_week: dict[int, int] = {}
    urls = []
    for p in plots:
        by_status[p["status"]] = by_status.get(p["status"], 0) + 1
        by_district[p["district"]] = by_district.get(p["district"], 0) + 1
        by_week[p["week"]] = by_week.get(p["week"], 0) + 1
        urls.append({"id": p["id"], "week": p["week"], "status": p["status"], "url": p["listing_url"]})

    out = {
        "current_week": board.get("current_week", 1),
        "last_updated_iso": board.get("last_updated_iso"),
        "total_plots": len(plots),
        "by_status": by_status,
        "by_district": by_district,
        "by_week": by_week,
        "existing_listings": urls,
    }
    write_json(out, args.output)


def check_single_url(url: str, last_request_ref: list[float], retries: int = 2) -> dict:
    delay = 1.0 / REQUESTS_PER_SECOND
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    for attempt in range(retries):
        elapsed = time.monotonic() - last_request_ref[0]
        if elapsed < delay:
            time.sleep(delay - elapsed)
        try:
            req = urllib_request.Request(url, headers=headers)
            with urllib_request.urlopen(req, timeout=20) as resp:
                last_request_ref[0] = time.monotonic()
                code = resp.getcode()
                body = resp.read(24000).decode("utf-8", errors="replace").lower()
                sold_markers = (
                    "ขายแล้ว",
                    "ปิดการขาย",
                    "property is no longer available",
                    "listing has been removed",
                    "this listing is sold",
                )
                bot_markers = ("just a moment", "cf-browser-verification", "captcha", "verify you are human")
                if any(m in body for m in bot_markers):
                    return {"http_code": code, "verdict": "needs_browser_check", "detail": "Anti-bot / challenge page detected — verify in browser or skip"}
                if any(m in body for m in sold_markers):
                    return {"http_code": code, "verdict": "sold_detected", "detail": "Sold / removed notice detected in page HTML"}
                return {"http_code": code, "verdict": "live", "detail": "OK"}
        except urllib_error.HTTPError as e:
            last_request_ref[0] = time.monotonic()
            if e.code in (404, 410):
                return {"http_code": e.code, "verdict": "dead", "detail": f"HTTP {e.code} Not Found / Gone"}
            if e.code == 403:
                return {"http_code": 403, "verdict": "needs_browser_check", "detail": "HTTP 403 (bot filter) — verify manually in browser"}
            if e.code == 429:
                wait = 2**attempt
                print(f"Rate limited (429) on {url}, waiting {wait}s...", file=sys.stderr)
                if attempt == retries - 1:
                    return {"http_code": 429, "verdict": "needs_browser_check", "detail": f"HTTP 429 rate limited (limit {REQUESTS_PER_SECOND} req/s)"}
                time.sleep(wait)
                continue
            if e.code >= 500 and attempt < retries - 1:
                time.sleep(2**attempt)
                continue
            return {"http_code": e.code, "verdict": "error", "detail": f"HTTP {e.code}"}
        except urllib_error.URLError as e:
            last_request_ref[0] = time.monotonic()
            if attempt < retries - 1:
                time.sleep(2**attempt)
                continue
            return {"http_code": 0, "verdict": "error", "detail": f"Network error: {e.reason}"}
    return {"http_code": 0, "verdict": "error", "detail": "Exhausted retries"}


def cmd_check_links(args: argparse.Namespace) -> None:
    board = load_json(args.input)
    plots = board.get("plots", [])
    today_iso = date.today().isoformat()
    last_req = [0.0]
    results = []
    marked_count = 0

    for plot in plots:
        if plot.get("status") in ("passed", "sold") and not args.include_closed:
            results.append({"id": plot["id"], "status": plot["status"], "verdict": "skipped_closed", "url": plot["listing_url"]})
            continue
        res = check_single_url(plot["listing_url"], last_req)
        entry = {
            "id": plot["id"],
            "title_en": plot["title_en"],
            "previous_status": plot["status"],
            "url": plot["listing_url"],
            **res,
        }
        results.append(entry)
        if res["verdict"] == "live":
            plot["last_checked"] = today_iso
        elif args.mark_dead and res["verdict"] in ("dead", "sold_detected"):
            plot["status"] = "sold"
            plot["badge_en"] = "Sold / Removed"
            plot["badge_th"] = "ขายแล้ว / ปิดประกาศ"
            plot["last_checked"] = today_iso
            marked_count += 1

    if args.mark_dead:
        write_json(board, args.input)

    report = {
        "checked_at": today_iso,
        "rate_limit_rps": REQUESTS_PER_SECOND,
        "total_checked": sum(1 for r in results if r["verdict"] != "skipped_closed"),
        "marked_sold_count": marked_count,
        "results": results,
    }
    write_json(report, args.output)


def cmd_add_plots(args: argparse.Namespace) -> None:
    board = load_json(args.input)
    batch = load_json(args.batch)
    incoming = batch if isinstance(batch, list) else batch.get("plots", [])
    if not isinstance(incoming, list) or not incoming:
        print("Error: --batch must contain a non-empty JSON list or {'plots': [...]}.", file=sys.stderr)
        sys.exit(1)

    existing_urls = {normalize_url(p["listing_url"]) for p in board.get("plots", [])}
    iso_str, en_date, th_date = format_dates(args.date)
    week_num = args.week

    existing_week_ids = [
        p["id"] for p in board.get("plots", []) if p.get("week") == week_num
    ]
    next_seq = len(existing_week_ids) + 1
    added = []
    skipped = []

    required_fields = (
        "title_en",
        "title_th",
        "district",
        "size_rai_str",
        "size_rai_num",
        "size_sqm",
        "price_total_thb",
        "title_deed_status",
        "title_deed_en",
        "title_deed_th",
        "listing_url",
        "map_url",
        "bullets",
    )

    for raw in incoming:
        missing = [k for k in required_fields if k not in raw or raw[k] in (None, "")]
        if missing:
            print(f"Error: Plot '{raw.get('title_en', '?')}' missing required fields: {missing}", file=sys.stderr)
            sys.exit(1)

        deed_err = check_forbidden_deeds(raw)
        if deed_err:
            skipped.append({"title": raw["title_en"], "reason": deed_err})
            continue

        norm_url = normalize_url(raw["listing_url"])
        if norm_url in existing_urls:
            skipped.append({"title": raw["title_en"], "reason": "Duplicate listing_url already in board"})
            continue

        district = raw["district"]
        if district not in VALID_DISTRICTS:
            print(f"Error: Invalid district '{district}'. Must be one of {list(VALID_DISTRICTS)}.", file=sys.stderr)
            sys.exit(1)

        status = raw.get("status", "visit")
        if status not in VALID_STATUSES:
            print(f"Error: Invalid status '{status}'. Must be one of {VALID_STATUSES}.", file=sys.stderr)
            sys.exit(1)

        size_rai = float(raw["size_rai_num"])
        total_price = int(raw["price_total_thb"])
        price_per_rai = int(raw.get("price_per_rai_thb") or round(total_price / max(size_rai, 0.01)))
        d_en, d_th = VALID_DISTRICTS[district]

        plot_obj = {
            "id": raw.get("id") or f"w{week_num}-{next_seq:02d}",
            "week": week_num,
            "status": status,
            "district": district,
            "district_en": raw.get("district_en") or d_en,
            "district_th": raw.get("district_th") or d_th,
            "badge_en": raw.get("badge_en") or (f"Week {week_num} • Top Pick" if status == "shortlisted" else f"Week {week_num} • New"),
            "badge_th": raw.get("badge_th") or (f"สัปดาห์ {week_num} • ตัวเต็ง" if status == "shortlisted" else f"สัปดาห์ {week_num} • แปลงใหม่"),
            "title_en": raw["title_en"],
            "title_th": raw["title_th"],
            "size_rai_str": raw["size_rai_str"],
            "size_rai_num": round(size_rai, 2),
            "size_sqm": int(raw["size_sqm"]),
            "dimensions_en": raw.get("dimensions_en", ""),
            "dimensions_th": raw.get("dimensions_th", ""),
            "price_total_thb": total_price,
            "price_per_rai_thb": price_per_rai,
            "price_note_en": raw.get("price_note_en", "Total / per Rai"),
            "price_note_th": raw.get("price_note_th", "ราคารวม (เฉลี่ย/ไร่)"),
            "title_deed_status": raw["title_deed_status"],
            "title_deed_en": raw["title_deed_en"],
            "title_deed_th": raw["title_deed_th"],
            "drive_mins": raw.get("drive_mins", "~45–60"),
            "bullets": raw["bullets"],
            "contact": raw.get("contact", ""),
            "listing_url": raw["listing_url"].strip(),
            "listing_source_en": raw.get("listing_source_en", "View Listing"),
            "listing_source_th": raw.get("listing_source_th", "ดูประกาศจริง"),
            "map_url": raw["map_url"].strip(),
            "map_label_en": raw.get("map_label_en", "Area Map"),
            "map_label_th": raw.get("map_label_th", "แผนที่โซน"),
            "last_checked": iso_str,
        }
        board["plots"].append(plot_obj)
        existing_urls.add(norm_url)
        added.append(plot_obj["id"])
        next_seq += 1

    board["current_week"] = max(int(board.get("current_week", 1)), week_num)
    board["last_updated_iso"] = iso_str
    board["last_updated_en"] = en_date
    board["last_updated_th"] = th_date

    write_json(board, args.output)
    print(f"Added {len(added)} plot(s): {added}; Skipped {len(skipped)}: {skipped}")


def cmd_update_status(args: argparse.Namespace) -> None:
    if args.status not in VALID_STATUSES:
        print(f"Error: Invalid status '{args.status}'. Choose from {VALID_STATUSES}.", file=sys.stderr)
        sys.exit(1)

    board = load_json(args.input)
    found = None
    for plot in board.get("plots", []):
        if plot["id"] == args.id:
            found = plot
            break

    if not found:
        print(f"Error: Plot ID '{args.id}' not found in {args.input}.", file=sys.stderr)
        sys.exit(1)

    found["status"] = args.status
    found["last_checked"] = date.today().isoformat()
    if args.badge_en:
        found["badge_en"] = args.badge_en
    if args.badge_th:
        found["badge_th"] = args.badge_th
    if args.note_en or args.note_th:
        found["bullets"].append({
            "icon": "📝",
            "label_en": "Update",
            "text_en": args.note_en or args.note_th,
            "label_th": "อัปเดตล่าสุด",
            "text_th": args.note_th or args.note_en,
        })

    write_json(board, args.output)
    print(f"Updated plot {args.id} -> status={args.status}")


def render_plot_card(plot: dict, display_idx: int) -> str:
    esc = html.escape
    status = plot["status"]
    status_icon = {
        "shortlisted": "⭐",
        "visit": "👀",
        "contacted": "📞",
        "passed": "❌",
        "sold": "🚫",
    }.get(status, "•")
    badge_cls = {
        "shortlisted": "badge-forest",
        "visit": "badge-amber",
        "contacted": "badge-forest",
        "passed": "badge-danger",
        "sold": "badge-danger",
    }.get(status, "badge-amber")
    dist_cls = "badge-amber" if status == "shortlisted" else "badge-forest"
    deed_icon = "✅" if plot["title_deed_status"] == "verified" else "⚠️"

    size_label_en = f"Size ({esc(plot['dimensions_en'])})" if plot.get("dimensions_en") else "Size"
    size_label_th = f"เนื้อที่ ({esc(plot['dimensions_th'])})" if plot.get("dimensions_th") else "เนื้อที่"

    bullets_html = []
    for b in plot.get("bullets", []):
        bullets_html.append(
            f'              <li><span>{esc(b["icon"])}</span><div>'
            f'<span class="en"><strong>{esc(b["label_en"])}:</strong> {esc(b["text_en"])}</span>'
            f'<span class="th"><strong>{esc(b["label_th"])}:</strong> {esc(b["text_th"])}</span>'
            f"</div></li>"
        )
    bullets_str = "\n".join(bullets_html)

    contact_html = ""
    if plot.get("contact"):
        contact_html = f'\n            <div class="contact-pill" style="margin-block-start: 0.7rem;">{esc(plot["contact"])}</div>'

    week_tag = f'W{plot["week"]}'
    return f"""        <!-- PLOT {display_idx}: {esc(plot["id"])} -->
        <article class="plot-card" data-status="{esc(status)}" data-district="{esc(plot["district"])}" data-week="{plot["week"]}" data-price-total="{plot["price_total_thb"]}" data-price-rai="{plot["price_per_rai_thb"]}" data-size-rai="{plot["size_rai_num"]}" data-order="{display_idx}">
          <div>
            <div class="tag-row" style="justify-content: space-between;">
              <span class="badge {badge_cls}">{status_icon} <span class="en">{esc(plot["badge_en"])}</span><span class="th">{esc(plot["badge_th"])}</span></span>
              <span class="badge {dist_cls}">{week_tag} • <span class="en">{esc(plot["district_en"])}</span><span class="th">{esc(plot["district_th"])}</span></span>
            </div>
            <h3 style="margin-block-start: 0.6rem;">
              <span class="en">#{display_idx} — {esc(plot["title_en"])}</span>
              <span class="th">#{display_idx} — {esc(plot["title_th"])}</span>
            </h3>
            <div class="plot-meta-grid">
              <div class="plot-meta-item">
                <span class="plot-meta-label"><span class="en">{size_label_en}</span><span class="th">{size_label_th}</span></span>
                <span class="plot-meta-val">{esc(plot["size_rai_str"])} <span class="en">Rai ({plot["size_sqm"]:,} m²)</span><span class="th">ไร่ ({plot["size_rai_num"]:.2f} ไร่)</span></span>
              </div>
              <div class="plot-meta-item">
                <span class="plot-meta-label"><span class="en">Price ({esc(plot["price_note_en"])})</span><span class="th">{esc(plot["price_note_th"])}</span></span>
                <span class="plot-meta-val">{format_thb_short(plot["price_total_thb"])} <span class="muted">({format_thb_per_rai(plot["price_per_rai_thb"])})</span></span>
              </div>
              <div class="plot-meta-item">
                <span class="plot-meta-label"><span class="en">Title Deed</span><span class="th">เอกสารสิทธิ์</span></span>
                <span class="plot-meta-val">{deed_icon} <span class="en">{esc(plot["title_deed_en"])}</span><span class="th">{esc(plot["title_deed_th"])}</span></span>
              </div>
              <div class="plot-meta-item">
                <span class="plot-meta-label"><span class="en">Drive to CM City</span><span class="th">เวลาเข้าเมือง</span></span>
                <span class="plot-meta-val">{esc(plot["drive_mins"])} <span class="en">mins</span><span class="th">นาที</span></span>
              </div>
            </div>
            <ul class="plot-checklist" style="margin-block-start: 0.8rem;">
{bullets_str}
            </ul>{contact_html}
          </div>
          <div class="btn-row">
            <a class="btn btn-primary" href="{esc(plot["listing_url"])}" target="_blank" rel="noopener">🔗 <span class="en">{esc(plot["listing_source_en"])}</span><span class="th">{esc(plot["listing_source_th"])}</span></a>
            <a class="btn" href="{esc(plot["map_url"])}" target="_blank" rel="noopener">📍 <span class="en">{esc(plot["map_label_en"])}</span><span class="th">{esc(plot["map_label_th"])}</span></a>
          </div>
        </article>"""


def cmd_render(args: argparse.Namespace) -> None:
    board = load_json(args.input)
    plots = board.get("plots", [])
    html_path = Path(args.html)
    doc = html_path.read_text(encoding="utf-8")

    # Sort newest week first, then shortlisted before others, then original order
    status_rank = {"shortlisted": 0, "contacted": 1, "visit": 2, "passed": 3, "sold": 4}
    ordered_plots = sorted(
        enumerate(plots),
        key=lambda item: (-item[1]["week"], status_rank.get(item[1]["status"], 9), item[0]),
    )
    ordered = [p for _, p in ordered_plots]

    total = len(ordered)
    active_plots = [p for p in ordered if p["status"] not in ("passed", "sold")]
    min_total = min((p["price_total_thb"] for p in active_plots), default=0)
    max_total = max((p["price_total_thb"] for p in active_plots), default=0)
    min_per_rai = min((p["price_per_rai_thb"] for p in active_plots), default=0)

    current_week = board.get("current_week", 1)
    updated_en = html.escape(board.get("last_updated_en", ""))
    updated_th = html.escape(board.get("last_updated_th", ""))

    # Build Status filter buttons
    status_meta = [
        ("shortlisted", "⭐", "Top Picks", "ตัวเต็งเข้ารอบ"),
        ("visit", "👀", "To Review / Visit", "น่าสนใจ / รอดูเพิ่ม"),
        ("contacted", "📞", "Contacted", "ติดต่อแล้ว"),
        ("passed", "❌", "Passed", "ตัดออก"),
        ("sold", "🚫", "Sold", "ขายแล้ว"),
    ]
    status_buttons = [
        f'            <button type="button" class="filter-btn" data-status-filter="all" aria-pressed="true">\n'
        f'              <span class="en">All Status ({total})</span><span class="th">ทุกสถานะ ({total})</span>\n'
        f"            </button>"
    ]
    for code, icon, en_lbl, th_lbl in status_meta:
        cnt = sum(1 for p in ordered if p["status"] == code)
        if cnt > 0:
            status_buttons.append(
                f'            <button type="button" class="filter-btn" data-status-filter="{code}" aria-pressed="false">\n'
                f'              {icon} <span class="en">{en_lbl} ({cnt})</span><span class="th">{th_lbl} ({cnt})</span>\n'
                f"            </button>"
            )

    # Build District filter buttons
    district_buttons = [
        '          <button type="button" class="filter-btn district-btn" data-district-filter="all" aria-pressed="true">\n'
        '            <span class="en">All Districts</span><span class="th">ทุกอำเภอ</span>\n'
        "          </button>"
    ]
    for d_code, (d_en, d_th) in VALID_DISTRICTS.items():
        cnt = sum(1 for p in ordered if p["district"] == d_code)
        if cnt > 0:
            short_th = d_th.replace("อ.", "")
            district_buttons.append(
                f'          <button type="button" class="filter-btn district-btn" data-district-filter="{d_code}" aria-pressed="false">\n'
                f'            <span class="en">{d_en} ({cnt})</span><span class="th">{short_th} ({cnt})</span>\n'
                f"          </button>"
            )

    # Build Week filter buttons (shown when >1 week exists)
    weeks = sorted({p["week"] for p in ordered}, reverse=True)
    week_bar_html = ""
    if len(weeks) > 1:
        w_btns = [
            '          <button type="button" class="filter-btn week-btn" data-week-filter="all" aria-pressed="true">\n'
            '            <span class="en">All Weeks</span><span class="th">ทุกสัปดาห์</span>\n'
            "          </button>"
        ]
        for w in weeks:
            cnt = sum(1 for p in ordered if p["week"] == w)
            w_btns.append(
                f'          <button type="button" class="filter-btn week-btn" data-week-filter="{w}" aria-pressed="false">\n'
                f'            <span class="en">Week {w} ({cnt})</span><span class="th">สัปดาห์ {w} ({cnt})</span>\n'
                f"          </button>"
            )
        week_bar_html = (
            '\n        <div class="filter-bar" role="group" aria-label="Filter plots by week">\n'
            + "\n".join(w_btns)
            + "\n        </div>"
        )

    cards_html = "\n\n".join(
        render_plot_card(plot, idx + 1) for idx, plot in enumerate(ordered)
    )

    section_html = f"""<!-- PLOTS_START -->
    <section class="section-block" id="weekly-results">
      <div class="section-header">
        <div>
          <h2 class="mb-0">
            <span class="en">4. Weekly Land Search Results (Week {current_week} • {updated_en})</span>
            <span class="th">4. ผลการค้นหาที่ดินรายสัปดาห์ (สัปดาห์ที่ {current_week} • {updated_th})</span>
          </h2>
          <p class="muted mt-0 mb-0">
            <span class="en">Verified live listings from Teedin108, DotProperty, FazWaz, and LivingInsider. Filter by status, district, or sort by price per rai.</span>
            <span class="th">ประกาศจริงที่ตรวจสอบแล้วจาก Teedin108, DotProperty, FazWaz และ LivingInsider สามารถกรองตามสถานะ อำเภอ หรือเรียงตามราคาต่อไร่ได้</span>
          </p>
        </div>
        <div class="badge badge-forest" id="visible-count">{total} / {total}</div>
      </div>

      <div class="controls-panel">
        <div class="controls-row">
          <div class="filter-bar" role="group" aria-label="Filter plots by status">
{chr(10).join(status_buttons)}
          </div>
          <label>
            <select class="sort-select" id="sort-plots" aria-label="Sort plots">
              <option value="default">Sort: Recommended (เรียงตามแนะนำ)</option>
              <option value="price-rai-asc">Lowest Price / Rai (ราคาต่อไร่ถูกสุด)</option>
              <option value="price-total-asc">Lowest Total Price (ราคารวมถูกสุด)</option>
              <option value="size-desc">Largest Size (พื้นที่มากสุด)</option>
            </select>
          </label>
        </div>

        <div class="filter-bar" role="group" aria-label="Filter plots by district">
{chr(10).join(district_buttons)}
        </div>{week_bar_html}
      </div>

      <div class="plot-grid" id="plot-grid">
{cards_html}
      </div>
    </section>
    <!-- PLOTS_END -->"""

    # Replace PLOTS_START..PLOTS_END
    plots_pat = re.compile(r"<!-- PLOTS_START -->.*?<!-- PLOTS_END -->", re.S)
    if not plots_pat.search(doc):
        print("Error: Missing <!-- PLOTS_START --> / <!-- PLOTS_END --> markers in index.html", file=sys.stderr)
        sys.exit(1)
    doc = plots_pat.sub(lambda _: section_html, doc, count=1)

    # Update HERO_BADGE_START..HERO_BADGE_END
    hero_badge = (
        f"<!-- HERO_BADGE_START -->\n"
        f"        <span>🏡</span>\n"
        f'        <span class="en">Week {current_week} Live Search • Updated {updated_en} • Inspired by Jon Jandai &amp; Pun Pun</span>\n'
        f'        <span class="th">อัปเดตสัปดาห์ที่ {current_week} • {updated_th} • แรงบันดาลใจจาก โจน จันใด (บ้านพันพรรณ)</span>\n'
        f"        <!-- HERO_BADGE_END -->"
    )
    doc = re.sub(r"<!-- HERO_BADGE_START -->.*?<!-- HERO_BADGE_END -->", lambda _: hero_badge, doc, count=1, flags=re.S)

    # Update HERO_STATS_START..HERO_STATS_END
    hero_stats = (
        f"<!-- HERO_STATS_START -->\n"
        f'          <div class="spec-pill-label">\n'
        f'            <span class="en">Week {current_week} Findings</span>\n'
        f'            <span class="th">ผลการค้นหา (ถึงสัปดาห์ {current_week})</span>\n'
        f"          </div>\n"
        f'          <div class="spec-pill-value">\n'
        f'            <span class="en">{len(active_plots)} Active Plots ({total} Total)</span>\n'
        f'            <span class="th">{len(active_plots)} แปลงเปิดขาย (รวม {total})</span>\n'
        f"          </div>\n"
        f'          <div class="muted">\n'
        f'            <span class="en">{format_thb_short(min_total)} – {format_thb_short(max_total)} (from {format_thb_per_rai(min_per_rai)}!)</span>\n'
        f'            <span class="th">ราคา {format_thb_short(min_total)} – {format_thb_short(max_total)} (เริ่ม {format_thb_per_rai(min_per_rai)}!)</span>\n'
        f"          </div>\n"
        f"          <!-- HERO_STATS_END -->"
    )
    doc = re.sub(r"<!-- HERO_STATS_START -->.*?<!-- HERO_STATS_END -->", lambda _: hero_stats, doc, count=1, flags=re.S)

    # Update side nav counts
    doc = re.sub(
        r"<!-- NAV_RESULTS_LABEL_START -->.*?<!-- NAV_RESULTS_LABEL_END -->",
        lambda _: (
            f'<!-- NAV_RESULTS_LABEL_START --><span class="en">4. Weekly Results ({len(active_plots)})</span>'
            f'<span class="th">4. ผลค้นหารายสัปดาห์ ({len(active_plots)})</span><!-- NAV_RESULTS_LABEL_END -->'
        ),
        doc,
        flags=re.S,
    )

    html_path.write_text(doc, encoding="utf-8")
    print(f"Success! Rendered {total} plots ({len(active_plots)} active, Week {current_week}) into: {html_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Chiang Mai Land Search Board CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sum = sub.add_parser("summary", help="Export board statistics and existing listing URLs")
    p_sum.add_argument("--input", required=True, help="Path to data/plots.json")
    p_sum.add_argument("--output", required=True, help="Output summary JSON path")

    p_chk = sub.add_parser("check-links", help="Politely verify existing listing URLs (1 req/s)")
    p_chk.add_argument("--input", required=True, help="Path to data/plots.json")
    p_chk.add_argument("--output", required=True, help="Output report JSON path")
    p_chk.add_argument("--mark-dead", action="store_true", help="Automatically mark 404/sold listings as status=sold in --input")
    p_chk.add_argument("--include-closed", action="store_true", help="Also check plots already marked passed/sold")

    p_add = sub.add_parser("add-plots", help="Validate, deduplicate, and merge new weekly plots")
    p_add.add_argument("--input", required=True, help="Path to data/plots.json")
    p_add.add_argument("--batch", required=True, help="Path to new plots JSON file")
    p_add.add_argument("--week", type=int, required=True, help="Week number (e.g., 2, 3, ...)")
    p_add.add_argument("--date", default=None, help="ISO date YYYY-MM-DD (defaults to today)")
    p_add.add_argument("--output", required=True, help="Output updated plots.json path")

    p_upd = sub.add_parser("update-status", help="Update status and/or notes on an existing plot")
    p_upd.add_argument("--input", required=True, help="Path to data/plots.json")
    p_upd.add_argument("--id", required=True, help="Plot ID (e.g., w1-01)")
    p_upd.add_argument("--status", required=True, choices=VALID_STATUSES, help="New plot status")
    p_upd.add_argument("--badge-en", default=None, help="Optional updated English badge text")
    p_upd.add_argument("--badge-th", default=None, help="Optional updated Thai badge text")
    p_upd.add_argument("--note-en", default=None, help="Optional English update bullet")
    p_upd.add_argument("--note-th", default=None, help="Optional Thai update bullet")
    p_upd.add_argument("--output", required=True, help="Output updated plots.json path")

    p_ren = sub.add_parser("render", help="Render data/plots.json into index.html")
    p_ren.add_argument("--input", required=True, help="Path to data/plots.json")
    p_ren.add_argument("--html", required=True, help="Path to index.html")

    args = parser.parse_args()
    if args.command == "summary":
        cmd_summary(args)
    elif args.command == "check-links":
        cmd_check_links(args)
    elif args.command == "add-plots":
        cmd_add_plots(args)
    elif args.command == "update-status":
        cmd_update_status(args)
    elif args.command == "render":
        cmd_render(args)


if __name__ == "__main__":
    main()
