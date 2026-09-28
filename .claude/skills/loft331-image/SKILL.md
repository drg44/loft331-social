---
name: loft331-image
description: Make ONE on-brand Loft 331 image on demand — a link preview / OG image for a loft331.ca page, a single social post, a story cover, an event or email banner, a sponsor thank-you. Use when Dave asks for "an image", "a thumbnail", "a share image", "a banner", "a graphic", "a post" for Loft 331 and it is NOT the two-week content cycle (that is the loft331-social skill). Everything needed is in this repo; never restyle, never invent a palette, logo, or photo.
---

# Loft 331 — one-off image

The brand is not negotiable. Every Loft 331 visual is produced by the render kit in this repo, from a real Loft 331 photo, with the real white wordmark, Fraunces headline, Lato subline and `LOFT331.CA`. If you find yourself writing CSS colours or drawing a logo, stop: you are off-brand.

## 0. Setup (30 seconds)
- The repo `drg44/loft331-social` must be on disk: Mac → `~/loft331-social` (installed by `tools/install-mac.sh`; run `git -C ~/loft331-social pull` first), cloud → `/home/user/loft331-social` (clone it if missing: `git clone --depth 1 https://github.com/drg44/loft331-social /home/user/loft331-social`). All paths below are relative to that folder; `cd` into it.
- Sanity: `python3 tools/social/render.py --help` prints usage. Chrome/Chromium is found automatically (Mac Google Chrome, or `/opt/pw-browsers` in the cloud).

## 1. Read the rules first (every time)
1. `.claude/skills/loft331-social/references/Loft331-Brand-Guidelines.md` — §3 colours, §4 type, §7 logo, §8 photo table, §9 visual rules.
2. `.claude/skills/loft331-social/references/voice-guide.md` — fact sheet (prices, address, phone), character limits, template selection.
3. `tools/photos/_README.txt` — which photo folder is for what.

## 2. Decide four things, in this order
| Decision | Rule |
|---|---|
| **Size** | link preview / OG image → `link` (1200×630) · Facebook feed → `facebook` (1080×905, default) · Instagram → `square` · story/reel cover → `story` · email header → `email` (1200×600) |
| **Template** | photo with strong subject → `template-spotlight.html` (neutral dark gradient). Stock photo or testimonial → `template-spotlight-green.html` (#013C3F wash). No usable photo → `template-statement-green.html`. Photo-top + green panel → `template-spotlight-green-panel.html`. Email → `template-email-banner.html` (fields EYEBROW, HEADLINE, SUBLINE, DETAIL). |
| **Photo** | Pick from `tools/photos/<folder>/` by the §8 table + `_README.txt`. People line → people photo (`space-people/` or `loft-and-found/`). Room offer → `space-empty/`, `meeting-room/`, `call-room/`, `event-space/`. Never AI, never a file that is not in the folder. Check `tools/posted-log.csv`: no photo twice within 14 days for social posts (an OG image is exempt). |
| **Copy** | Headline: **two lines, one sentence each, ≤ 26 chars per line**, sentence case, two-beat house style ("Upcoming events. / Hosted by our members."). Subline: ≤ 2 × 55 chars, say-it-out-loud plain speech. Prices only from the voice-guide fact sheet. Canadian spelling. |

If the ask does not pin these down, decide with the rules above and say what you chose. Ask only when a wrong guess would cost a re-shoot (e.g. which event photo, a price).

## 3. Render
```bash
cd tools/social
python3 render.py template-spotlight.html --size link \
  --out ../../<where>/<name>.png \
  --set "HEADLINE=Line one.<br>Line two." \
  --set "SUBLINE=One plain sentence.<br>Optional second line." \
  --set PHOTO=../photos/space-people/loft_and_found_event_people.jpg \
  --set "PHOTO_POS=center 30%"
```
- `--set` values are HTML: escape `&` as `&amp;`, `"` as `&quot;`; `<br>` is the only tag.
- `PHOTO_POS` moves the crop (`left`, `right`, `center`, `30% 50%`). Use it when the crop lands on empty wall or cuts a face.
- Output at 2× device scale (a `link` render is 2400×1260). That is fine for every platform.

## 4. Look before you show
Open the PNG with the Read tool. Fail and re-render if: a headline wraps to a third line; a face or the subject is cropped; the subline orphans one word; the logo overlaps a face; the crop is mostly empty wall. Two failed fixes → stop and show Dave the options.

## 5. Deliver
- One-off image for the website/OG: commit it under `site-assets/<page>/` in this repo and give Dave the raw URL (`https://raw.githubusercontent.com/drg44/loft331-social/main/site-assets/...`) plus the PNG itself. Tell him where to set it (e.g. the page's `og:image`).
- Social post outside the cycle: put it in `<YYYY-MM-DD>-<slug>/posts/01-<date>-<type>/post-<size>.png`, commit, push, and — only if Dave asked for Buffer — create a **draft** via the Buffer MCP (org `6ab117352302590845670309`, Facebook channel `6ab117c7ea19ca0bdea45dc7`, `saveToDraft: true`, `mode: customScheduled`, `dueAt` in the future at `-03:00` / `-04:00` after Nov 1). Never publish live. Append the row to `tools/posted-log.csv`.

## Hard rules
- Logo top-left, white, exactly as `tools/social/logo.png`. Never redrawn, recoloured, boxed, or moved.
- Only the templates in `tools/social/`. No white backgrounds, no borders, badges, icons, chips, or extra colours.
- Real Loft 331 photos or the listed stock only. Never AI-generated imagery.
- If it cannot fit the character limits, rewrite the copy. The layout never bends.
