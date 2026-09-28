# Loft 331 content system — CLAUDE.md

This repo is the **single home for everything Claude needs to make Loft 331 content**: brand rules, voice, photos, fonts, logo, templates, the render pipeline, the posted log, and the rendered images that Buffer serves. Open this repo (cloud or Mac) and every skill below is available. Nothing depends on any other repo or on a specific machine.

## Start here
| You were asked for… | Do this |
|---|---|
| One image (OG / link preview, a post, a story, a banner) | `/loft-image <what for> [size]` → `.claude/skills/loft331-image/SKILL.md` |
| The two-week social cycle / content calendar | `/loft-cycle starting Monday <date>` → `.claude/skills/loft331-social/SKILL.md` |
| A brand / voice / photo question | `/loft-brand <question>` |

## Non-negotiables (from the brand guidelines)
- Real Loft 331 photo (or the listed stock under the green wash). Never AI imagery. Never a plain white background.
- White wordmark top-left, exactly `tools/social/logo.png`. Never redrawn or recoloured.
- Fraunces 600 headline, two lines, ≤ 26 chars each, sentence case; Lato subline ≤ 2 × 55; `LOFT331.CA` bottom-left.
- Colours: brand green `#013C3F`, gradient partner `#1A5C44`, slate body `#334155`, white. No other colours. No borders, badges, icons, chips.
- Prices/facts only from `references/voice-guide.md`. Canadian spelling. No gym. No "premium / sophisticated / excellence".
- Facebook posts are always 1080×905 (`--size facebook`), never square. Square is Instagram only.
- Buffer: drafts only (`saveToDraft: true`). Dave approves. Never `shareNow`.

## Layout
```
.claude/skills/loft331-social/   cycle skill + references/ (brand guidelines, voice guide, wink bank, project memory)
.claude/skills/loft331-image/    one-off image skill
.claude/commands/                /loft-image  /loft-cycle  /loft-brand
tools/social/                    render.py · render_calendar.py · contact_sheet.py · find_stock.py · buffer_export.py · templates · logo
tools/photos/<purpose>/          the photo pool (mirror of Drive → Loft 331 Social/Photos) + _README.txt
tools/fonts/, tools/loft331-brand.css
tools/posted-log.csv             authoritative log of what was posted
<YYYY-MM-DD>-cycle/posts/…       rendered images (committed; Buffer loads them from raw.githubusercontent.com)
site-assets/<page>/              one-off website images (OG images etc.)
```

## Render in one line
```bash
cd tools/social && python3 render.py template-spotlight.html --size link --out ../../site-assets/x/og.png \
  --set "HEADLINE=Line one.<br>Line two." --set "SUBLINE=Plain sentence." --set PHOTO=../photos/space-people/coworking-hero-lounge.jpg
```
Chrome/Chromium is auto-detected (Mac Google Chrome or `/opt/pw-browsers` in Claude cloud). Always open the PNG with the Read tool before showing Dave.

## Drive is still the input side
Inputs sheet, Google Reviews sheet, and Calendars live in Drive folder "Loft 331 Social" (ids in the social skill). Read them with the Drive MCP. New photos Dave drops in Drive → copy into `tools/photos/<purpose>/` and commit.

## Git
Work on `main` directly (this is a content repo, not code). Commit rendered images with `Add <campaign> images`. Never rewrite history: Buffer links to raw URLs.
