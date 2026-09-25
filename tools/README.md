# Loft 331 render kit (self-contained mirror of ~/loft331-mgmt/brand/social on Dave's Mac)

Everything a Claude cloud session needs to make an on-brand post image in one step. Source of truth for
voice/rules stays the brand MD in Drive → Loft 331 Social/System/brand/Loft331-Brand-Guidelines.md.

    tools/
      loft331-brand.css          brand tokens + self-hosted fonts (fonts/ relative to this file)
      fonts/fraunces.woff2, lato.woff2
      social/render.py           fill template → headless Chrome screenshot (Mac Chrome or /opt/pw-browsers chromium)
      social/template-spotlight.html        photo style (neutral dark gradient)
      social/template-spotlight-green.html  green style (#013C3F wash)
      social/logo.b64 / logo.png  white wordmark, transparent (keyed from Loft311_logo-FINAL_Hor_w.jpg, 2266x1745)
      photos/<space-people|space-empty|meeting-room|call-room|event-space|loft-and-found|members|stock>/  mirror of Drive → Loft 331 Social/Photos

## One post, start to finish (cloud session)

    git clone --depth 1 https://github.com/drg44/loft331-social /home/user/loft331-social
    cd /home/user/loft331-social/tools/social
    python3 render.py template-spotlight.html --size facebook \
      --out ../../<campaign>/posts/01-<date>-<type>/post-facebook.png \
      --set "HEADLINE=Line one, max 26 chars.<br>Line two, max 26 chars." \
      --set "SUBLINE=Max 2 x 55 chars, say-it-out-loud plain speech." \
      --set PHOTO=../photos/loft-and-found/lf-mingling-1.jpg [--set "PHOTO_POS=left"]
    # look at the PNG before showing Dave (Read tool), then:
    git add <campaign> && git commit -m "Add <campaign> images" && git push origin HEAD:main
    # image URL for Buffer: https://raw.githubusercontent.com/drg44/loft331-social/main/<campaign>/posts/.../post-facebook.png
    # Buffer: org 6ab117352302590845670309, FB channel 6ab117c7ea19ca0bdea45dc7, tz America/Moncton (-03:00; -04:00 after Nov 1)
    # create_post/edit_post with assets=[{image:{url,altText=headline}}], metadata.facebook.type="post", schedulingType automatic.
    # editing a scheduled post drops it to draft: re-send with saveToDraft:false + mode customScheduled + dueAt (must be in the future).
    # re-attaching a changed image: bump ?v=N on the URL or Buffer keeps the cached copy.

Rules that bite: no photo twice within 14 days (check posted-log.csv in Drive System/); headline = two lines,
one sentence each; logo top-left always; never AI images; never plain white background; ≤2 emoji, 3–5 hashtags.
