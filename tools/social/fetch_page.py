#!/usr/bin/env python3
"""Read a web page as plain text, including sites behind a Cloudflare "Just a moment" check.

  python3 tools/social/fetch_page.py "https://www.wework.com/ideas/..."          -> headings, paragraphs, link text in order
  python3 tools/social/fetch_page.py "<url>" --html out.html                      -> also keep the rendered DOM

Uses the same headless Chromium as render.py (plain curl/WebFetch get blocked by bot checks).
The cloud environment's network policy must allow the host (Edit environment -> Network access -> Allowed domains).
"""
import argparse, html, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import chrome  # noqa: E402

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"

def fetch(url, budget_ms=15000):
    cmd = [chrome(), "--headless=new", "--disable-gpu", "--no-sandbox", f"--user-agent={UA}",
           f"--virtual-time-budget={budget_ms}", "--dump-dom", url]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return r.stdout

def to_text(dom):
    dom = re.sub(r"<(script|style|svg|noscript)[^>]*>.*?</\1>", "", dom, flags=re.S | re.I)
    seen, out = set(), []
    for tag, inner in re.findall(r"<(h[1-6]|p|li|a|time|blockquote)\b[^>]*>(.*?)</\1>", dom, flags=re.S | re.I):
        s = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", inner))).strip()
        if len(s) < 3 or s in seen:
            continue
        seen.add(s)
        out.append(f"[{tag.lower()}] {s}")
    return "\n".join(out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--html", help="also write the rendered DOM here")
    ap.add_argument("--budget", type=int, default=15000, help="virtual time budget in ms (default 15000)")
    a = ap.parse_args()
    dom = fetch(a.url, a.budget)
    if a.html:
        Path(a.html).write_text(dom, encoding="utf-8")
    if "Just a moment" in dom[:2000]:
        sys.exit("Cloudflare challenge not passed; try a bigger --budget or open the page on the Mac")
    print(to_text(dom))
