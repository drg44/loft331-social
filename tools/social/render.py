#!/usr/bin/env python3
"""Loft 331 social render — fill a template's {{PLACEHOLDERS}} and screenshot with headless Chrome.
Works on the Mac (Google Chrome) and in Claude cloud sessions (Playwright chromium under /opt/pw-browsers).

  python3 render.py template-spotlight.html --out out.png --size facebook \
    --set HEADLINE="Line one.<br>Line two." --set SUBLINE="..." --set PHOTO=/abs/path/photo.jpg

Sizes: facebook 1080x905 (default) · square 1080x1080 · story 1080x1920 · link 1200x630
{{LOGO_B64}} is injected from logo.b64; {{PHOTO_POS}} defaults to center.
"""
import argparse, glob, html, os, re, subprocess, sys, tempfile
from pathlib import Path

SIZES = {"facebook": (1080, 905), "square": (1080, 1080), "landscape": (1080, 864), "portrait": (1080, 1350), "story": (1080, 1920), "link": (1200, 630), "email": (1200, 600)}
HERE = Path(__file__).resolve().parent

def chrome():
    for c in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"] + sorted(glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell")) + sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")) + ["/usr/bin/chromium", "/usr/bin/google-chrome"]:
        if os.path.exists(c):
            return c
    sys.exit("no Chrome/Chromium found")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", choices=SIZES, default="facebook")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE")
    a = ap.parse_args()
    t = (HERE / a.template).read_text()
    f = {"LOGO_B64": (HERE / "logo.b64").read_text().strip(), "PHOTO_POS": "center"}
    for pair in a.set:
        k, v = pair.split("=", 1); f[k.strip()] = v
    if "PHOTO" in f and not f["PHOTO"].startswith(("file:", "http", "data:")):
        f["PHOTO"] = Path(f["PHOTO"]).resolve().as_uri()
    for k, v in f.items():
        t = t.replace("{{%s}}" % k, v)
    left = sorted(set(re.findall(r"{{([A-Z_]+)}}", t)))
    if left:
        sys.exit("unfilled placeholders: " + ", ".join(left))
    w, h = SIZES[a.size]; out = Path(a.out).resolve(); out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=HERE, suffix=".html", delete=False) as fh:
        fh.write(t); tmp = Path(fh.name)
    try:
        r = subprocess.run([chrome(), "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2", f"--window-size={w},{h}", "--virtual-time-budget=3000", f"--screenshot={out}", tmp.as_uri()], capture_output=True, text=True)
        if r.returncode != 0 or not out.exists():
            sys.exit("chrome render failed:\n" + r.stderr[-800:])
    finally:
        tmp.unlink(missing_ok=True)
    print(out)

if __name__ == "__main__":
    main()
