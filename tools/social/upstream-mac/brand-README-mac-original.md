# LOFT331 brand pipeline

Automated on-brand documents (contracts, proposals, flyers, one-pagers) without Canva.

## How it works
1. Every document is an HTML file that links `loft331-brand.css` + Google Fonts
   (Fraunces 600 + Lato — same as loft331.ca).
2. Render to PDF (print docs) or PNG (marketing graphics) with headless Chrome:

```bash
# PDF (contracts, proposals — US Letter)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-pdf-header-footer --print-to-pdf=OUT.pdf "file:///path/to/doc.html"

# 4K PNG (social / TV / marketing graphics)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --window-size=3840,2160 --screenshot=OUT.png "file:///path/to/doc.html"
```

3. PDFs can be dragged into Canva (Create a design → Import file) when Dave wants
   to hand-tweak — Canva keeps text editable and colors intact. Canva's AI
   generator is NOT part of the pipeline (it strips brand styling).

## Brand tokens (verified against site.css 2026-07-10)
- **Body text = gray-700 `#334155`, NOT green.** Green `#013C3F` is for headings/accents only.
- Display headings: Fraunces 600, tracking **-0.065em** (tighter). Legal-copy section heads: Fraunces **800**.
- Body: Lato; muted meta text gray-500 `#64748b`, small-caps 0.05em.
- Panels: gray-50 `#f8fafc` + 1px gray-200 `#e2e8f0` border, 10px radius (site card style). Beige `#f1f1e6` exists but is muted/secondary.
- Pages are white and airy — no dark banner blocks.
- Logo `~/Documents/GitHub/loft331-static/assets/images/logo.webp` is **white** — must sit on a green chip. Convert to PNG (`sips -s format png`) and inline as base64 **stripped of newlines** (`base64 -i file | tr -d '\n'`); this Chrome build won't decode that webp.
- Fonts: self-hosted woff2 in `~/Documents/GitHub/loft331-static/assets/fonts/` (fraunces.woff2 + lato.woff2), reference via file:// @font-face.

## Templates
- `../contracts/event-venue-agreement-alp-2026-10-22.html` — contract layout
  (green header band, beige parties panel, aqua-rule sections, fee box,
  two-column signatures). Copy + edit for new contracts.

## Social content pipeline (`social/`)
Automated on-brand social posts via the `/content` slash command (`~/.claude/commands/content.md`).
- 3 templates (all link `../loft331-brand.css`, vw-sized so any aspect works):
  `template-quote.html` (statements/tips/testimonials), `template-promo.html`
  (offers with a price + feature list), `template-spotlight.html` (full-bleed
  site photo + green gradient overlay — site webp files work directly via file://).
- `render.py` fills `{{PLACEHOLDERS}}`, auto-injects the base64 logo (`logo.b64`),
  and screenshots with headless Chrome. Sizes: square 1080×1080, story 1080×1920,
  link 1200×630. Errors on unfilled placeholders.
- `voice-guide.md` — voice, fact sheet (prices/phone/address), caption rules,
  template selection. Verify prices against site pages before citing.
- Output convention: `~/loft331-mgmt/social/out/YYYY-MM-DD-<slug>/` (PNG + caption.txt).
- Sample renders in `social/test/`.
