# Loft 331 render kit

Self-contained. Works on Dave's Mac and in Claude cloud sessions. The skills in `.claude/skills/` tell Claude how to use it;
the brand rulebook is `.claude/skills/loft331-social/references/Loft331-Brand-Guidelines.md`.

    tools/
      loft331-brand.css              brand tokens + self-hosted fonts (fonts/ relative to this file)
      fonts/fraunces.woff2, lato.woff2
      social/render.py               fill a template → headless Chrome screenshot (auto-finds Mac Chrome or /opt/pw-browsers chromium)
      social/render_calendar.py      calendar.csv → every post image + captions.md + schedule.csv (14-day photo-reuse guard, 2-line headline guard)
      social/contact_sheet.py        tile a campaign's PNGs into one review image
      social/find_stock.py           CC0/CC-BY photo search (Openverse + Commons) → tools/photos/stock + CREDITS.csv
      social/buffer_export.py        optional Buffer bulk-upload CSVs
      social/template-spotlight.html             photo style (neutral dark gradient)   fields HEADLINE SUBLINE PHOTO [PHOTO_POS]
      social/template-spotlight-green.html       green style (#013C3F wash)            same fields
      social/template-spotlight-green-panel.html photo top, solid green panel below      same fields
      social/template-statement-green.html       no photo, green gradient, big type     HEADLINE SUBLINE
      social/template-email-banner.html          1200x600 email header                  EYEBROW HEADLINE SUBLINE DETAIL PHOTO
      social/logo.png / logo.b64     white wordmark, transparent (from Loft311_logo-FINAL_Hor_w)
      photos/<purpose>/              mirror of Drive → Loft 331 Social/Photos (see photos/_README.txt)
      posted-log.csv                 what was posted (date,channel,post_type,headline,photo_file,campaign)

Sizes: facebook 1080×905 (default) · square 1080×1080 · portrait 1080×1350 · story 1080×1920 · link 1200×630 · email 1200×600. Rendered at 2×.

## One image
    cd tools/social
    python3 render.py template-spotlight.html --size link --out ../../site-assets/<page>/og.png \
      --set "HEADLINE=Line one, max 26 chars.<br>Line two, max 26 chars." \
      --set "SUBLINE=Max 2 x 55 chars, plain speech." \
      --set PHOTO=../photos/loft-and-found/lf-mingling-1.jpg [--set "PHOTO_POS=left"]

## A cycle
    python3 tools/social/render_calendar.py <cycle>/calendar.csv --campaign <cycle>
    python3 tools/social/contact_sheet.py <cycle>        # look at <cycle>/contact-sheet.png before showing Dave
    git add <cycle> && git commit -m "Add <cycle> images" && git push origin HEAD:main
    # Buffer image URL: https://raw.githubusercontent.com/drg44/loft331-social/main/<cycle>/posts/<folder>/post-facebook.png
    # Buffer MCP: org 6ab117352302590845670309 · FB channel 6ab117c7ea19ca0bdea45dc7 · tz America/Moncton (-03:00; -04:00 after Nov 1)
    # HARD RULE: every post is a DRAFT (saveToDraft:true, mode customScheduled, dueAt in the future). Dave approves. Never shareNow.
    # re-attaching a changed image: bump ?v=N on the URL or Buffer keeps its cached copy.

Rules that bite: no photo twice within 14 days; headline = two lines, one sentence each, ≤26 chars; logo top-left always;
never AI images; never a plain white background; ≤2 emoji, 3–5 hashtags; prices only from the voice guide.
