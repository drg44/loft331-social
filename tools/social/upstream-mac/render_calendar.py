#!/usr/bin/env python3
"""Render every row of a Loft 331 content calendar into on-brand social PNGs.

Input: a CSV exported from the NotebookLM calendar sheet (or a Google Sheet URL).
Columns used: Publish Date, Key Message / Headline, Subline (optional), Caption, Photo File, Style (photo|green).
Output: ~/loft331-mgmt/social/out/<YYYY-MM-DD>-<slug>/post-square.png + caption.txt per row.

Usage:
  python3 render_calendar.py calendar.csv
  python3 render_calendar.py "https://docs.google.com/spreadsheets/d/<id>/edit"
  python3 render_calendar.py calendar.csv --size story --rows 1,3
"""
import argparse, csv, html, io, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRIVE = Path.home() / "Library/CloudStorage/GoogleDrive-dan@loft331.ca/My Drive/Loft 331 Social/Photos"
PHOTOS = [DRIVE / d for d in ("space-people", "space-empty", "meeting-room", "call-room", "event-space", "loft-and-found", "members", "stock")] + [
          Path.home() / "loft331-mgmt/brand/notebooklm/assets/photos",   # fallback if Drive isn't synced
          Path.home() / "loft331-mgmt/brand/notebooklm/assets/stock",
          Path.home() / "loft331-mgmt/brand/notebooklm/assets"]
OUT_ROOT = Path.home() / "loft331-mgmt/social/out"
TEMPLATES = {"photo": "template-spotlight.html", "green": "template-spotlight-green.html"}
HEAD_MAX, SUB_MAX = 26, 55  # chars per line, from voice-guide.md


def esc(s):
    return html.escape(s, quote=True)


def find_photo(name):
    name = (name or "").strip()
    if not name:
        return None
    stem = Path(name).stem
    for d in PHOTOS:
        for ext in ("", ".jpg", ".jpeg", ".png", ".webp"):
            p = d / (name if not ext else stem + ext)
            if p.exists():
                return p
    return None


def split_sentences(text):
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p.strip()]
    return parts or [text.strip()]


def load_rows(src):
    if src.startswith("http"):
        m = re.search(r"/d/([A-Za-z0-9_-]+)", src)
        if not m:
            sys.exit("bad Google Sheets URL")
        url = f"https://docs.google.com/spreadsheets/d/{m.group(1)}/export?format=csv"
        r = subprocess.run(["curl", "-sL", "--max-time", "30", url], capture_output=True, text=True)
        if r.returncode != 0 or not r.stdout.strip():
            sys.exit("could not download the sheet (is it shared 'Anyone with the link'?)")
        f = io.StringIO(r.stdout)
    else:
        f = open(src, newline="", encoding="utf-8")
    rows = list(csv.reader(f))
    # header = first row containing "Headline"
    for i, r in enumerate(rows):
        if any("headline" in c.lower() for c in r):
            hdr = [c.strip() for c in r]
            return hdr, [x for x in rows[i + 1:] if any(c.strip() for c in x)]
    sys.exit("no header row with a Headline column found")


def col(hdr, *names):
    for n in names:
        for i, h in enumerate(hdr):
            if n.lower() in h.lower():
                return i
    return None


LOG = Path.home() / "loft331-mgmt/social/posted-log.csv"
REUSE_DAYS = 14  # hard rule (Dave 2026-09-21): no background photo twice within two weeks


def check_photo_reuse(rows, c_date, c_photo):
    """Refuse to render if a photo repeats inside this calendar, or was posted < REUSE_DAYS before its first date."""
    import datetime as dt
    used, problems = {}, []
    for n, r in enumerate(rows, 1):
        g = lambda i: r[i].strip() if i is not None and i < len(r) else ""
        p = Path(g(c_photo) or "loft_gradient.png").stem.lower()
        if p == "loft_gradient":
            continue
        if p in used:
            problems.append(f"row {n} reuses “{p}” (already on row {used[p]})")
        used[p] = n
    dates = []
    for r in rows:
        try:
            dates.append(dt.date.fromisoformat(r[c_date].strip()[:10]))
        except Exception:
            pass
    if dates and LOG.exists():
        first = min(dates)
        rows_by_date = {Path(r[c_photo]).stem.lower(): None for r in rows if c_photo < len(r)}
        for row in csv.DictReader(LOG.open(newline="", encoding="utf-8")):
            try:
                d = dt.date.fromisoformat(row["date"][:10])
            except Exception:
                continue
            p = Path(row.get("photo_file", "")).stem.lower()
            if p and p != "loft_gradient" and p in used and 0 < (first - d).days < REUSE_DAYS:
                problems.append(f"row {used[p]} reuses “{p}” posted {d} (< {REUSE_DAYS} days before {first})")
    if problems:
        sys.exit("PHOTO REUSE — pick a different photo:\n  - " + "\n  - ".join(problems))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="CSV path or Google Sheets URL")
    ap.add_argument("--size", default="facebook", choices=["facebook", "square", "portrait", "story", "link", "landscape"])
    ap.add_argument("--rows", help="comma-separated 1-based row numbers to render (default all)")
    ap.add_argument("--style", choices=["photo", "green"], help="force a style for every row (default: the row's Style column, else photo)")
    ap.add_argument("--campaign", help="output everything into ~/loft331-mgmt/social/campaigns/<name>/ (numbered post folders + captions.md + schedule.csv)")
    a = ap.parse_args()

    hdr, rows = load_rows(a.source)
    c_date = col(hdr, "publish date", "date")
    c_head = col(hdr, "headline", "key message")
    c_sub = col(hdr, "subline")
    c_cap = col(hdr, "caption")
    c_photo = col(hdr, "photo file", "photo")
    c_style = col(hdr, "style")
    c_pos = col(hdr, "photo position")
    if c_head is None or c_photo is None:
        sys.exit(f"need Headline and Photo File columns; got {hdr}")

    want = {int(x) for x in a.rows.split(",")} if a.rows else None
    warnings = []
    check_photo_reuse(rows, c_date, c_photo)
    camp = None
    if a.campaign:
        camp = Path.home() / "loft331-mgmt/social/campaigns" / a.campaign
        (camp / "posts").mkdir(parents=True, exist_ok=True)
        if not a.source.startswith("http"):
            src = Path(a.source).resolve()
            if src != (camp / "calendar.csv").resolve():
                (camp / "calendar.csv").write_bytes(src.read_bytes())
    c_type = col(hdr, "post type")
    c_time = col(hdr, "day & time", "time")
    digest, sched = [], []
    for n, r in enumerate(rows, 1):
        if want and n not in want:
            continue
        g = lambda i: r[i].strip() if i is not None and i < len(r) else ""
        date = g(c_date) or f"row{n}"
        head = g(c_head)
        sub = g(c_sub)
        cap = g(c_cap)
        photo_name = g(c_photo) or "loft_gradient.png"
        style = a.style or ("green" if "green" in g(c_style).lower() else "photo")

        lines = [x.strip() for x in head.split(" / ")][:2] if " / " in head else split_sentences(head)[:2]
        if len(lines) == 1 and ", " in lines[0]:
            first, rest = lines[0].split(", ", 1); lines = [first + ",", rest]
        if len(lines) == 1:  # hard rule (Dave 2026-09-21): every headline is two lines
            words = lines[0].split()
            if len(words) >= 4:
                mid = max(range(1, len(words)), key=lambda i: -abs(len(" ".join(words[:i])) - len(lines[0]) / 2))
                lines = [" ".join(words[:mid]), " ".join(words[mid:])]
                warnings.append(f"row {n}: one-line headline auto-split into two — check it reads naturally: “{lines[0]} / {lines[1]}”")
            else:
                warnings.append(f"row {n}: headline is a single short line — needs a second sentence")
        for ln in lines:
            if len(ln) > HEAD_MAX + 1:
                sys.exit(f"row {n}: headline line is {len(ln)} chars (max {HEAD_MAX + 1}) — it would wrap to a third line: “{ln}”. Shorten it.")
            if len(ln) > HEAD_MAX:
                warnings.append(f"row {n}: headline line >{HEAD_MAX} chars: “{ln}”")
        if not sub and c_sub is None:  # only fall back when the calendar has no Subline column at all
            sub = split_sentences(cap)[0] if cap else ""
        if len(sub) > SUB_MAX * 2:
            warnings.append(f"row {n}: subline >{SUB_MAX*2} chars, trimmed")
            sub = sub[: SUB_MAX * 2].rsplit(" ", 1)[0] + "…"

        photo = find_photo(photo_name)
        if photo is None:
            warnings.append(f"row {n}: photo “{photo_name}” not found, using loft_gradient.png")
            photo = find_photo("loft_gradient.png")

        slug = re.sub(r"[^a-z0-9]+", "-", head.lower()).strip("-")[:40]
        ptype = g(c_type)
        if camp:
            tslug = re.sub(r"[^a-z0-9]+", "-", ptype.lower()).strip("-") or "post"
            outdir = camp / "posts" / f"{n:02d}-{date}-{tslug}"
        else:
            outdir = OUT_ROOT / f"{date}-{slug}"
        outdir.mkdir(parents=True, exist_ok=True)
        out = outdir / f"post-{a.size}.png"
        cmd = [sys.executable, str(HERE / "render.py"), TEMPLATES[style], "--out", str(out), "--size", a.size,
               "--set", "HEADLINE=" + "<br>".join(esc(l) for l in lines),
               "--set", "SUBLINE=" + esc(sub),
               "--set", "PHOTO=" + photo.as_uri(),
               "--set", "PHOTO_POS=" + (g(c_pos) or "center")]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            sys.exit(f"row {n} failed:\n{res.stdout}\n{res.stderr}")
        if cap:
            (outdir / "caption.txt").write_text(cap + "\n")
        print(f"row {n}: {out}  [{photo.name}, {style}]")
        if camp:
            rel = out.relative_to(camp)
            tm = re.sub(r"^[A-Za-z]{3}\s+", "", g(c_time)) or "9:00 AM"
            digest.append(f"## {n:02d} · {date} · {ptype}\n\n**Image:** `{rel}`  \n**Headline:** {head}  \n**Subline:** {sub}\n\n{cap}\n")
            sched.append([date, tm, cap, str(rel), ptype, head])

    if camp:
        (camp / "captions.md").write_text(f"# {a.campaign}\n\nOne section per post, in publish order. Image path is relative to this folder.\n\n" + "\n---\n\n".join(digest))
        with open(camp / "schedule.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["date", "time", "text", "image", "post_type", "headline"]); w.writerows(sched)
        print(f"\ncampaign folder: {camp}")

    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print("  -", w)


if __name__ == "__main__":
    main()
