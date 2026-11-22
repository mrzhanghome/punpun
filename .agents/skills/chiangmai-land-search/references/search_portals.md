# Chiang Mai Land Search Reference — Portals, Districts & Rubric

## 1. Homestead Criteria (Jon Jandai / Pun Pun Style)
- **Location:** Within ~30–65 minutes of Chiang Mai Old City.
- **Size:** **1 to 5 Rai** (1,600–8,000 sq.m) — enough for a water retention pond, adobe/earthen house (*บ้านดิน*), raised mounds (*โคกหนองนา*), and organic food forest.
- **Title Deed (STRICT):**
  - ✅ **Chanote / Nor Sor 4 Jor (โฉนดครุฑแดง)** — strongly preferred.
  - ⚠️ **Nor Sor 3 Gor (น.ส.3 ก. ครุฑเขียว)** — acceptable if clearly labeled and transferable.
  - ❌ **STRICTLY EXCLUDE:** *Sor Por Gor 4-01 (ส.ป.ก.)*, *Por Bor Tor 5 (ภ.บ.ท.5)*, *Sor Tor Gor (ส.ท.ก.)*, and forest reserve plots.
- **Budget (HARD CAP):** total price **≤ ฿2,500,000 THB** (current `criteria.max_budget_thb` in `data/plots.json`); highlight best value per rai and direct-from-owner (`เจ้าของขายเอง`) listings.
- **Physical Priorities:**
  1. **Water:** Existing pond(s), year-round irrigation canal (*ลำเหมือง / เหมืองฝาย*), stream, or good groundwater depth.
  2. **Soil:** Clay-loam / paddy / mixed orchard soil suitable for pond lining and adobe bricks.
  3. **Access & Flood Safety:** Legal public road (*ทางสาธารณประโยชน์*) and non-flooding (check 2024 Chiang Mai flood history).

---

## 2. Target Districts & Portal Entry URLs

### Zone A — Mae Taeng (อ.แม่แตง) [Pun Pun Home District, 45–60 mins North]
Priority subdistricts: **Cho Lae (ต.ช่อแล)**, **Inthakhin (ต.อินทขิล)**, **Khi Lek (ต.ขี้เหล็ก)**, **Ban Pao (ต.บ้านเป้า)**, **Mae Ho Phra (ต.แม่หอพระ)**.
- Teedin108 Mae Taeng: `https://www.teedin108.com/land/amphur/573/`
- DotProperty Mae Taeng: `https://www.dotproperty.co.th/en/land-for-sale/chiang-mai/mae-taeng`
- FazWaz Mae Taeng: `https://www.fazwaz.com/land-for-sale/thailand/chiang-mai/mae-taeng?order_by=price|asc`
- LivingInsider: `https://www.livinginsider.com/land-buysell` (search `แม่แตง`)

### Zone B — Doi Saket & Mae On (อ.ดอยสะเก็ด / อ.แม่ออน) [30–55 mins East]
Priority subdistricts: **Mae Pong (ต.แม่โป่ง)**, **Sa-Nga Ban (ต.สง่าบ้าน)**, **Samran Rat (ต.สำราญราษฎร์)**, **Pa Pong (ต.ป่าป้อง)**, **On Klang (ต.ออนกลาง)**, **On Nuea (ต.ออนเหนือ)**.
- Teedin108 Chiang Mai: `https://www.teedin108.com/land/chiangmai/`
- DotProperty Doi Saket: `https://www.dotproperty.co.th/en/land-for-sale/chiang-mai/doi-saket`
- DotProperty Mae On: `https://www.dotproperty.co.th/en/land-for-sale/chiang-mai/mae-on`
- FazWaz Doi Saket: `https://www.fazwaz.com/land-for-sale/thailand/chiang-mai/doi-saket?order_by=price|asc`
- FazWaz Mae On: `https://www.fazwaz.com/land-for-sale/thailand/chiang-mai/mae-on?order_by=price|asc`

### Zone C — Mae Wang, San Pa Tong & Samoeng (อ.แม่วาง / อ.สันป่าตอง / อ.สะเมิง) [35–65 mins SW/W]
Priority subdistricts: **Thung Pi (ต.ทุ่งปี้)**, **Ban Kat (ต.บ้านกาด)**, **Makham Luang (ต.มะขามหลวง)**, **Samoeng Tai (ต.สะเมิงใต้ — Chanote ONLY!)**.
- DotProperty Mae Wang: `https://www.dotproperty.co.th/en/land-for-sale/chiang-mai/mae-wang`
- DotProperty San Pa Tong: `https://www.dotproperty.co.th/en/land-for-sale/chiang-mai/san-pa-tong`
- DotProperty Samoeng: `https://www.dotproperty.co.th/en/land-for-sale/chiang-mai/samoeng`
- FazWaz Mae Wang / San Pa Tong: `https://www.fazwaz.com/land-for-sale/thailand/chiang-mai/mae-wang?order_by=price|asc`

### Thai Search Phrases (When Searching Google / Portals)
- `ขายที่ดิน แม่แตง เชียงใหม่ โฉนด เจ้าของขายเอง`
- `ขายที่ดิน ดอยสะเก็ด แม่ออน โฉนด เจ้าของขายเอง`
- `ขายที่ดิน แม่วาง สันป่าตอง ติดลำเหมือง โฉนด`
- `ขายที่ดิน สวนผสม โคกหนองนา เชียงใหม่ โฉนด`

---

## 3. JSON Schema for `add-plots` Batch File

Save newly discovered plots to a temporary JSON array (e.g., `/tmp/week2_plots.json`) matching these fields:

```json
[
  {
    "status": "shortlisted",
    "district": "mae-taeng",
    "badge_en": "Week 2 • Top Pick",
    "badge_th": "สัปดาห์ 2 • ตัวเต็ง",
    "title_en": "Cho Lae 3-Rai Orchard with Irrigation Canal",
    "title_th": "ที่ดินสวนผลไม้ 3 ไร่ ติดลำเหมือง ต.ช่อแล",
    "size_rai_str": "3-0-15",
    "size_rai_num": 3.04,
    "size_sqm": 4860,
    "dimensions_en": "60m × 80m",
    "dimensions_th": "หน้ากว้าง 60×80 ม.",
    "price_total_thb": 1800000,
    "price_per_rai_thb": 592105,
    "price_note_en": "Total / per Rai",
    "price_note_th": "ราคารวม (เฉลี่ย/ไร่)",
    "title_deed_status": "verified",
    "title_deed_en": "Chanote (Red Garuda)",
    "title_deed_th": "โฉนดครุฑแดง (น.ส.4 จ.)",
    "drive_mins": "~45–55",
    "bullets": [
      {
        "icon": "💧",
        "label_en": "Water",
        "text_en": "Borders Mae Ngad canal with year-round flow.",
        "label_th": "แหล่งน้ำ",
        "text_th": "ติดลำเหมืองเขื่อนแม่งัด มีน้ำไหลตลอดปี"
      },
      {
        "icon": "⚠️",
        "label_en": "Check",
        "text_en": "Confirm public road status on Chanote map.",
        "label_th": "สิ่งที่ต้องเช็ค",
        "text_th": "เช็คทางสาธารณประโยชน์ในระวางโฉนด"
      }
    ],
    "contact": "📞 08X-XXX-XXXX",
    "listing_url": "https://www.teedin108.com/land/view/XXXXXXX/",
    "listing_source_en": "View Teedin108",
    "listing_source_th": "ดูประกาศ Teedin108",
    "map_url": "https://www.google.com/maps/search/Cho+Lae+Mae+Taeng+Chiang+Mai",
    "map_label_en": "Area Map",
    "map_label_th": "แผนที่โซน"
  }
]
```

Allowed `district` keys: `mae-taeng`, `doi-saket`, `mae-on`, `mae-wang`, `san-pa-tong`, `samoeng`, `phrao`.
Allowed `status` values: `shortlisted`, `visit`, `contacted`, `passed`, `sold`.
Allowed `title_deed_status` values: `verified` (Red Chanote), `ns3g` (Nor Sor 3 Gor), `verify` (unstated — confirm before deposit).
