# Chiang Mai Land Search Reference — Portals, Districts & Rubric

## 1. Homestead Criteria (Jon Jandai / Pun Pun Style)
- **Location:** Within ~30–65 minutes of Chiang Mai Old City.
- **Size:** **1 to 5 Rai** (1,600–8,000 sq.m) — enough for a water retention pond, adobe/earthen house (*บ้านดิน*), raised mounds (*โคกหนองนา*), and organic food forest.
- **Title Deed (STRICT):**
  - ✅ **Chanote / Nor Sor 4 Jor (โฉนดครุฑแดง)** — strongly preferred.
  - ⚠️ **Nor Sor 3 Gor (น.ส.3 ก. ครุฑเขียว)** — acceptable if clearly labeled and transferable.
  - ❓ **Unknown / Unstated (`title_deed_status: "unknown"`)** — **ALLOWED!** Especially on Facebook, sellers often omit the title deed type. List it as `"Unknown (Ask Seller)"` / `"ไม่ระบุ (ต้องถามผู้ขาย)"` with `title_deed_status: "unknown"`.
  - ❌ **STRICTLY EXCLUDE:** Any plot that explicitly states *Sor Por Gor 4-01 (ส.ป.ก.)*, *Por Bor Tor 5 (ภ.บ.ท.5)*, *Sor Tor Gor (ส.ท.ก.)*, or forest reserve (`ป่าสงวน`).
- **Budget (HARD CAP):** total price **≤ ฿2,500,000 THB** (current `criteria.max_budget_thb` in `data/plots.json`); highlight best value per rai and direct-from-owner (`เจ้าของขายเอง`) listings.
- **Physical Priorities:**
  1. **Water:** Existing pond(s), year-round irrigation canal (*ลำเหมือง / เหมืองฝาย*), stream, or good groundwater depth.
  2. **Soil:** Clay-loam / paddy / mixed orchard soil suitable for pond lining and adobe bricks.
  3. **Access & Flood Safety:** Legal public road (*ทางสาธารณประโยชน์*) and non-flooding (check 2024 Chiang Mai / Lamphun flood history).

---

## 2. Target Districts & Portal Entry URLs

**Access notes (checked 2026-11-22):** DotProperty and thailand-property.com work over plain HTTP (`curl`). **Teedin108, FazWaz and LivingInsider return 403/Cloudflare to `curl` but load normally in the user's real Chrome** (no login needed) — search them in the browser lane. If any site shows an interactive challenge (checkbox, puzzle, "confirm it's you"), stop and skip it; never try to solve or bypass it.

### Zone A — Mae Taeng (อ.แม่แตง) [Pun Pun Home District, 45–60 mins North]
Priority subdistricts: **Cho Lae (ต.ช่อแล)**, **Inthakhin (ต.อินทขิล)**, **Khi Lek (ต.ขี้เหล็ก)**, **Ban Pao (ต.บ้านเป้า)**, **Mae Ho Phra (ต.แม่หอพระ)**.
- Teedin108 Mae Taeng: `https://www.teedin108.com/land/amphur/573/`
- DotProperty Mae Taeng: `https://www.dotproperty.co.th/en/land-for-sale/chiang-mai/mae-taeng`
- FazWaz Mae Taeng: `https://www.fazwaz.com/land-for-sale/thailand/chiang-mai/mae-taeng?order_by=price|asc`
- LivingInsider: `https://www.livinginsider.com/land-buysell` (search `แม่แตง`)

### Zone B — Doi Saket & Mae On (อ.ดอยสะเก็ด / อ.แม่ออน) [30–55 mins East]
Priority subdistricts: **Mae Pong (ต.แม่โป่ง)**, **Sa-Nga Ban (ต.สง่าบ้าน)**, **Samran Rat (ต.สำราญราษฎร์)**, **Pa Pong (ต.ป่าป้อง)**, **On Klang (ต.ออนกลาง)**, **On Nuea (ต.ออนเหนือ)**.
- Teedin108 Chiang Mai (province): `https://www.teedin108.com/land/province/38/`
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

### Zone D — Lamphun (จ.ลำพูน: อ.เมืองลำพูน / อ.ป่าซาง / อ.บ้านธิ / อ.แม่ทา) [30–70 mins South/Southeast]
Usually cheaper per rai than the Chiang Mai zones: flat irrigated longan orchards and paddy with good clay soil. Districts and approximate drive from Chiang Mai Old City:
- **Mueang Lamphun (อ.เมืองลำพูน)** ~30–40 mins — prefer **Si Bua Ban (ต.ศรีบัวบาน)** and the eastern foothills. **Avoid Ban Klang (ต.บ้านกลาง) & Makhuea Chae (ต.มะเขือแจ้)** near the Northern Region Industrial Estate (นิคมอุตสาหกรรมภาคเหนือ) — groundwater/air contamination risk.
- **Ban Thi (อ.บ้านธิ)** ~35–45 mins — Mae Kuang irrigation (`เขื่อนแม่กวงอุดมธารา`), foothills toward Doi Saket.
- **Pa Sang (อ.ป่าซาง)** ~40–50 mins — **Nam Dip (ต.น้ำดิบ)**, **Makok (ต.มะกอก)**, **Tha Tum (ต.ท่าตุ้ม)**; longan orchard country.
- **Mae Tha (อ.แม่ทา)** ~55–70 mins — *optional / edge of range*; drop any listing whose realistic drive exceeds ~70 mins.
- **Out of range — do not search:** Li (อ.ลี้), Thung Hua Chang (อ.ทุ่งหัวช้าง), Wiang Nong Long and Ban Hong unless the user widens the drive limit. Lampang province is also out of scope.

Zone D cautions (add a ⚠️ bullet on every Lamphun plot that touches one of these):
- **Flood plains:** low land along the Ping (แม่น้ำปิง, e.g. ต.ริมปิง) and Kuang (น้ำแม่กวง) rivers flooded in 2024 — ask for flood history and look for a raised site.
- **Industrial estate:** flag any plot within ~5 km of the Northern Region Industrial Estate.
- **Deeds:** lots of `ส.ป.ก.` farmland in Lamphun — the standard exclusion rules apply.

Portals:
- DotProperty Lamphun: `https://www.dotproperty.co.th/en/land-for-sale/lamphun` (district pages: `/lamphun/mueang-lamphun`, `/lamphun/pa-sang`, `/lamphun/ban-thi`, `/lamphun/mae-tha`)
- Teedin108 Lamphun (province 39): `https://www.teedin108.com/land/province/39/` — districts: Mueang Lamphun `/land/amphur/595/`, Pa Sang `/land/amphur/600/`, Ban Thi `/land/amphur/601/`, Mae Tha `/land/amphur/596/`
- FazWaz Lamphun: `https://www.fazwaz.com/land-for-sale/thailand/lamphun?order_by=price|asc`
- LivingInsider: `https://www.livinginsider.com/land-buysell` (search `ลำพูน`, `ป่าซาง`, `บ้านธิ`)
- Facebook group #8 (ซื้อขายที่ดินเชียงใหม่-ลำพูน) below covers Lamphun.

### Facebook (logged-in browser session — owner-direct listings, often the cheapest)
The user keeps a logged-in Facebook session in the browser. Facebook is where most owner-direct (`เจ้าของขายเอง`) rural plots appear, but listings are messy (missing deed/price, stale posts).
- Marketplace: `https://www.facebook.com/marketplace/chiangmai/` (Property → Land) and Marketplace search with the Thai phrases below.
- Facebook search → Posts / Groups: `https://www.facebook.com/search/posts?q=<thai phrase>` (URL-encode the phrase).
- Rules: **read-only** (never post, comment, react, message, add friends, or join groups); scroll modestly (~40–60 posts per zone); if a checkpoint / CAPTCHA / "confirm it's you" / login wall appears, STOP and report — never solve or bypass it.
- Marketplace price fields are often placeholders (฿1, ฿123) — read the post text for the real asking price. If the title deed is not mentioned in the post, include it with `title_deed_status: "unknown"`, `title_deed_en: "Unknown (Ask Seller)"`, `title_deed_th: "ไม่ระบุ (ต้องถามผู้ขาย)"`.

#### Productive Chiang Mai Facebook Land Groups (Revisit Weekly)
1. **ซื้อ-ขายบ้าน ที่ดิน แม่ริม แม่แตง เชียงใหม่**: `https://www.facebook.com/groups/271099162090762/`
2. **ที่ดินเชียงใหม่ราคาหลักแสน**: `https://www.facebook.com/groups/160579518040515/`
3. **บ้าน ที่ดิน ราคาถูก เชียงใหม่**: `https://www.facebook.com/groups/236116797208244/`
4. **ซื้อขาย บ้านและที่ดิน เชียงใหม่**: `https://www.facebook.com/groups/911463042274859/`
5. **ขาย บ้านที่ดิน เชียงใหม่**: `https://www.facebook.com/groups/2531174597196960/`
6. **ซื้อ ขาย บ้านและที่ดินเชียงใหม่**: `https://www.facebook.com/groups/1709840645946215/`
7. **ตลาดซื้อขายบ้านและที่ดิน เชียงใหม่และภาคเหนือ**: `https://www.facebook.com/groups/430225152136340/`
8. **ซื้อขายที่ดินเชียงใหม่-ลำพูน-ทั่วภาคเหนือ**: `https://www.facebook.com/groups/298225005848173/`
9. **ซื้อขายบ้านและที่ดินใน จ.เชียงใหม่ และ ภาคเหนือ**: `https://www.facebook.com/groups/322977734828852/`
10. **กลุ่มซื้อขายที่ดิน เชียงดาว เชียงใหม่ ทั่วประเทศ โพสต์ฟรี**: `https://www.facebook.com/groups/428599314464047/`
11. **ขายบ้านและที่ดินโซนสันทรายแม่โจ้หนองหารแม่แฝกเจดีย์แม่ครัว**: `https://www.facebook.com/groups/306527483862118/`
12. **ซื้อขาย บ้าน ที่ดิน ลำพูน ป่าซาง สารภี บ้านธิ แม่ทา เวียงหนองล่อง** (Zone D): `https://www.facebook.com/groups/3934415109961272/` — use in-group search, e.g. `/groups/3934415109961272/search/?q=ไร่ โฉนด`

Facebook Marketplace tip: `https://www.facebook.com/marketplace/chiangmai/search/?query=<thai phrase>&maxPrice=2500000` covers Lamphun too (e.g. `ที่ดิน ป่าซาง`, `ที่ดิน 2 ไร่ ลำพูน`, `สวนลำไย ลำพูน`).

### Thai Search Phrases (When Searching Google / Portals / Facebook)
- `ขายที่ดิน แม่แตง เชียงใหม่ โฉนด เจ้าของขายเอง`
- `ขายที่ดิน ดอยสะเก็ด แม่ออน โฉนด เจ้าของขายเอง`
- `ขายที่ดิน แม่วาง สันป่าตอง ติดลำเหมือง โฉนด`
- `ขายที่ดิน สวนผสม โคกหนองนา เชียงใหม่ โฉนด`
- `ขายที่ดิน ลำพูน โฉนด เจ้าของขายเอง`
- `ขายที่ดิน ป่าซาง สวนลำไย โฉนด`
- `ขายที่ดิน บ้านธิ ติดลำเหมือง โฉนด`
- `ขายสวนลำไย ลำพูน 2 ไร่ โฉนด`

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

Allowed `district` keys: `mae-taeng`, `doi-saket`, `mae-on`, `mae-wang`, `san-pa-tong`, `samoeng`, `phrao`, `mueang-lamphun`, `pa-sang`, `ban-thi`, `mae-tha-lamphun`.
Allowed `status` values: `shortlisted`, `visit`, `contacted`, `passed`, `sold`.
Allowed `title_deed_status` values: `verified` (Red Chanote), `ns3g` (Nor Sor 3 Gor), `unknown` (title deed not mentioned in post — list as Unknown), `verify` (needs verification before deposit).
