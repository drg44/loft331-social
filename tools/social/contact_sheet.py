#!/usr/bin/env python3
"""Tile a campaign's rendered PNGs into one contact-sheet PNG so a human (or the Read tool) can review
every post at once before anything goes to Buffer.

  python3 tools/social/contact_sheet.py 2026-10-12-cycle            -> <campaign>/contact-sheet.png
  python3 tools/social/contact_sheet.py 2026-10-12-cycle --cols 3 --size facebook
"""
import argparse, glob, os, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
from render import chrome  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("campaign")
    ap.add_argument("--size", default="facebook", help="which post-<size>.png to tile")
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--out")
    a = ap.parse_args()
    camp = ROOT / a.campaign
    pngs = sorted(camp.glob(f"posts/*/post-{a.size}.png"))
    if not pngs:
        sys.exit(f"no posts/*/post-{a.size}.png under {camp}")
    tile_w = 380
    cells = "".join(
        f"<div><img src='{p.as_uri()}'><div class='cap'>{p.parent.name}</div></div>" for p in pngs)
    rows = -(-len(pngs) // a.cols)
    ratio = 1.0
    try:
        import struct
        d = pngs[0].read_bytes()[16:24]
        w, h = struct.unpack(">II", d)
        ratio = h / w
    except Exception:
        pass
    height = int(rows * (tile_w * ratio + 34) + 16)
    width = int(a.cols * (tile_w + 8) + 16)
    html = (f"<html><body style='margin:0;background:#fff;font-family:sans-serif;display:grid;"
            f"grid-template-columns:repeat({a.cols},{tile_w}px);gap:8px;padding:8px'>"
            f"<style>img{{width:{tile_w}px;display:block}}.cap{{font-size:12px;color:#334155;padding:4px 0 10px}}</style>"
            f"{cells}</body></html>")
    out = Path(a.out) if a.out else camp / "contact-sheet.png"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=camp) as fh:
        fh.write(html)
        tmp = Path(fh.name)
    try:
        r = subprocess.run([chrome(), "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            f"--window-size={width},{height}", "--virtual-time-budget=4000",
                            f"--screenshot={out}", tmp.as_uri()], capture_output=True, text=True)
        if r.returncode != 0 or not out.exists():
            sys.exit("chrome failed:\n" + r.stderr[-600:])
    finally:
        tmp.unlink(missing_ok=True)
    print(out)


if __name__ == "__main__":
    main()
