#!/usr/bin/env python3
"""Export a rendered campaign to Buffer bulk-upload CSVs (one per channel) — optional path;
the normal route is the Buffer MCP (see the loft331-social skill).

Buffer spec: columns Text, Image URL, Tags, Posting Time (YYYY-MM-DD HH:mm, 24h).
Images must be public: pass --base-url pointing at the campaign folder in this repo, e.g.
  https://raw.githubusercontent.com/drg44/loft331-social/main/<campaign>

Usage:
  python3 tools/social/buffer_export.py <campaign> --base-url https://raw.githubusercontent.com/drg44/loft331-social/main/<campaign>
Options:
  --times "facebook=09:00,instagram=12:00,linkedin=08:00"   (defaults shown)
  --channels facebook,instagram,linkedin
"""
import argparse, csv, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CAPTION_COL = {"facebook": "Caption", "instagram": "Caption IG", "linkedin": "Caption LinkedIn"}
DEFAULT_TIMES = {"facebook": "09:00", "instagram": "12:00", "linkedin": "08:00"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("campaign")
    ap.add_argument("--base-url", required=True, help="public URL of the campaign folder (no trailing slash)")
    ap.add_argument("--times", default="", help="per-channel HH:mm overrides, e.g. facebook=09:00,linkedin=08:00")
    ap.add_argument("--channels", default="facebook,instagram,linkedin")
    a = ap.parse_args()

    camp = ROOT / a.campaign
    cal = camp / "calendar.csv"
    if not cal.exists():
        sys.exit(f"{cal} missing — render_calendar.py copies the calendar there")
    rows = list(csv.DictReader(open(cal, newline="", encoding="utf-8")))
    times = dict(DEFAULT_TIMES)
    for kv in filter(None, a.times.split(",")):
        k, v = kv.split("=")
        times[k.strip()] = v.strip()
    posts = sorted(p for p in (camp / "posts").iterdir() if p.is_dir())
    if len(posts) != len(rows):
        sys.exit(f"{len(posts)} post folders vs {len(rows)} calendar rows; render first")
    base = a.base_url.rstrip("/")
    for ch in a.channels.split(","):
        ch = ch.strip()
        colname = CAPTION_COL[ch]
        out = camp / f"buffer-{ch}.csv"
        n = 0
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Text", "Image URL", "Tags", "Posting Time"])
            for r, folder in zip(rows, posts):
                text = (r.get(colname) or r.get("Caption") or "").strip()
                if not text:
                    continue
                png = next(folder.glob("post-*.png"))
                w.writerow([text, f"{base}/posts/{folder.name}/{png.name}", r.get("Post Type", "").strip(),
                            f"{r['Publish Date']} {times[ch]}"])
                n += 1
        print(f"{ch:10s} {n:2d} posts -> {out}")


if __name__ == "__main__":
    main()
