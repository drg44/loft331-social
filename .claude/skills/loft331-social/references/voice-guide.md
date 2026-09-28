# Loft 331 — social voice guide

Distilled from live site copy (loft331.ca source: `~/Documents/GitHub/loft331-static/pages/`), 2026-07-22.

## Voice
- **Warm, confident, plain-spoken.** Short sentences. Two-beat headlines are the house style:
  "Great coworking. Even better people." / "The space will draw you in. The people will keep you here." / "Work better. Together."
- **Community-first.** People before amenities. "…introduce you to the people who already call it home."
- **Concrete over hype.** Real numbers, always: "$29 + tax", "05 minutes from downtown", "50\" smart TV", "100+ reviews".
- **Friction-removal framing.** "No meters, no garages, no circling the block — just pull in and get to work." / "No long-term commitment required."
- Never: corporate buzzwords ("synergy", "hustle"), exclamation-point stacking, emoji spam (0–2 max per caption), fake urgency.

## Fact sheet (verify against site pages before citing a price — prices change)
- Address: **331 Elmwood Drive, Moncton** · call/text **506 850 5358** · **loft331.ca**
- Location: 5 min from downtown Moncton, 10 min from Champlain Place, free on-site parking
- Coworking: **Flex Desk from $249/mo** (business-hours, any open desk) · **Dedicated Desk from $299/mo** (24/7, your reserved desk)
- Day passes: **from $29 + tax** · 1, 5, or 10-day packs · no membership required
- Meeting room (The Boardroom): **$49/hr, 2-hr minimum ($98)** · Mon–Fri 8am–8pm · 50" smart TV, screen-casting, whiteboard
- Event space: **from $399 + tax** · 1,046 sq ft · up to 140 guests · 100" TV, podium + mic, speakers, dimmable lighting
- Virtual office: professional business mailing address
- Everywhere: fast fiber WiFi, free espresso, free parking, kitchen · 5.0★ from 100+ reviews

## Captions
- 1–3 short paragraphs. Hook first line (it's what shows before "…more").
- One idea per post. End with one CTA: "Book a tour at loft331.ca" or "Call/text 506 850 5358".
- Hashtags: 3–5 max, on the last line. Pool: #Moncton #MonctonNB #coworking #Loft331 #workstudio #smallbusinessNB #MonctonEvents
- Canadian spelling.

## NO white-background templates (Dave hard rule, 2026-07-22)
Dave deleted the white quote + promo cards — he does NOT want white backgrounds. Only three approved templates remain, all photo/green: **spotlight**, **green-panel**, **statement-green**. For an offer/price post, put the number in the statement-green or spotlight headline/subline — do NOT recreate a white promo card.

## Character limits (hard rules — keeps every post uniform; count per line, break lines yourself with wording, never shrink the font)
- **Line-break rule (headlines):** every sentence gets its own line — insert `<br>` between sentences in the HEADLINE value. A sentence must NEVER wrap mid-line; if a single sentence exceeds its per-line limit, rewrite it shorter.
- **Spotlight headline:** ≤ 26 chars/line, max 2 lines. **Subline:** ≤ 55 chars/line, max 2 lines.
- **Statement headline:** ≤ 22 chars/line, ALWAYS 2 lines (bigger 8vw type — no photo, so typography carries the card). **Subline:** ≤ 48 chars/line, max 2 lines.
If copy can't fit the limit, rewrite the copy — the layout never bends.

## Per-network formats
- **Instagram feed / Facebook feed / LinkedIn feed** → `--size square` (1080×1080), any template
- **Instagram/Facebook Story or Reel cover** → `--size story` (1080×1920), statement-green preferred (it self-centers); spotlight acceptable
- **Facebook/LinkedIn link preview, site OG image** → `--size link` (1200×630), spotlight or statement
- Default when unspecified: square.

## Template selection (only these three — no white backgrounds)
- **template-spotlight.html** — anything with a great photo: spaces, amenities, events, member spotlights, AND offer/price posts that have a good photo. Fields: HEADLINE, SUBLINE, PHOTO (file:// URL) — no LABEL field. **Photo pool (check in this order): 1) `~/loft331-mgmt/photos/` — Dave's drop folder, event/custom photos go here; 2) `~/Documents/GitHub/loft331-static/assets/images/` — the site's stock photos (hero-*, gallery, spaces).** jpg/png/webp all work directly via file:// URL. **Photo rule:** prefer hero-grade shots with a strong subject in the middle of the frame (the hero-* images); avoid shots whose middle is empty floor/wall — the gap between logo and text reads as dead space.
- **variants/statement-green.html** — no-photo statement card: brand lines, announcements, offers/prices without a photo, story/reel covers. Green gradient background, larger centered-left type. Fields: HEADLINE, SUBLINE.
- **variants/spotlight-green-panel.html** — photo on top, centered text on a solid green panel below. Fields: HEADLINE, SUBLINE, PHOTO.

Layout rules (Dave-approved 2026-07-22 vs his Canva mock — don't regress): logo always top-left (8vw top / 10vw left / 9.3vw tall), never bottom; 10vw side margins; spotlight has NO eyebrow label/rule — headline starts directly at 53vw, 6.5vw size; site URL bottom-left at 14vw off the bottom; no lines/rules on photo posts; overlay is a neutral black gradient (top + bottom mirrored), green only as accents. Default size: square.

## Render
```bash
python3 ~/loft331-mgmt/brand/social/render.py template-promo.html \
  --out ~/loft331-mgmt/social/out/2026-07-22-day-pass/post-square.png --size square \
  --set 'LABEL=DAY PASSES' --set 'HEADLINE=...' ...
```
Sizes: `square` 1080×1080 (IG/FB feed) · `story` 1080×1920 (stories/reels cover) · `link` 1200×630 (FB link/OG).
HTML-escape user text in --set values (`&amp;` `&quot;`). {{LOGO_B64}} injects automatically.
