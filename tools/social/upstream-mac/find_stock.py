#!/usr/bin/env python3
"""Find a free-licence photo that literally shows what a headline says.

  find_stock.py "cat sitting on a laptop keyboard"            -> contact sheet + numbered list
  find_stock.py "cat sitting on a laptop keyboard" --pick 3 --name stock-cat-laptop.jpg
Sources: Openverse (CC0/PDM/BY/BY-SA) + Wikimedia Commons. Min width 1600. Stdlib only.
"""
import argparse, csv, json, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path
UA = "loft331-social/1.0 (dan@loft331.ca)"
DRIVE = Path.home() / "Library/CloudStorage/GoogleDrive-dan@loft331.ca/My Drive/Loft 331 Social/Photos/stock"
WORK = Path.home() / "loft331-mgmt/social/stock-search"
OK = {"cc0", "pdm", "by", "by-sa", "CC0", "CC BY", "CC BY 2.0", "CC BY 3.0", "CC BY 4.0", "CC BY-SA 2.0", "CC BY-SA 3.0", "CC BY-SA 4.0", "Public domain"}

def get(url):  # curl: this Mac's python has no CA bundle for urllib
    r = subprocess.run(["curl", "-sL", "--max-time", "60", "-A", UA, url], capture_output=True)
    if r.returncode != 0 or not r.stdout: raise RuntimeError(f"fetch failed: {url[:80]}")
    return r.stdout

def openverse(q, n=12):
    u = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": q, "license": "cc0,pdm,by,by-sa", "size": "large", "mature": "false", "page_size": n})
    out = []
    for r in json.loads(get(u)).get("results", []):
        if (r.get("width") or 0) >= 1600 and (r.get("url") or "").lower().split("?")[0].endswith((".jpg", ".jpeg", ".png")):
            out.append(dict(src="openverse", title=r.get("title") or "", author=r.get("creator") or "", licence=r["license"].upper(), w=r["width"], h=r["height"], url=r["url"], page=r.get("foreign_landing_url") or r["url"]))
    return out

def commons(q, n=15):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "generator": "search", "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": n, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 2400, "format": "json"})
    out = []
    for p in json.loads(get(u)).get("query", {}).get("pages", {}).values():
        ii = p["imageinfo"][0]; em = ii.get("extmetadata", {})
        lic = em.get("LicenseShortName", {}).get("value", "?")
        if ii["width"] >= 1600 and ii["url"].lower().endswith((".jpg", ".jpeg", ".png")) and (lic in OK or lic.startswith("CC BY")):
            out.append(dict(src="commons", title=p["title"].replace("File:", ""), author=em.get("Artist", {}).get("value", "").split("<")[0].strip() or "unknown", licence=lic, w=ii["width"], h=ii["height"], url=ii.get("thumburl") or ii["url"], page=ii.get("descriptionurl", ii["url"])))
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("query"); ap.add_argument("--pick", type=int); ap.add_argument("--name"); a = ap.parse_args()
    WORK.mkdir(parents=True, exist_ok=True); state = WORK / "last.json"
    if a.pick:
        cands = json.loads(state.read_text()); c = cands[a.pick - 1]
        name = a.name or f"stock-{a.query.replace(' ', '-')[:30]}.jpg"
        DRIVE.mkdir(parents=True, exist_ok=True); dst = DRIVE / name
        dst.write_bytes(get(c["url"]))
        if dst.suffix.lower() != ".jpg":
            subprocess.run(["sips", "-s", "format", "jpeg", str(dst), "--out", str(dst.with_suffix(".jpg"))], capture_output=True); dst.unlink(); dst = dst.with_suffix(".jpg")
        cred = DRIVE / "CREDITS.csv"; new = not cred.exists()
        with cred.open("a", newline="") as f:
            w = csv.writer(f); new and w.writerow(["file", "title", "author", "licence", "source"]); w.writerow([dst.name, c["title"], c["author"], c["licence"], c["page"]])
        credit = "" if c["licence"].upper() in ("CC0", "PDM", "PUBLIC DOMAIN") else f'Photo: {c["author"]}, {c["licence"]}'
        print(f"saved {dst}\ncredit line for caption: {credit or '(none needed, CC0)'}"); return
    cands = []
    try: cands += openverse(a.query)
    except Exception as e: print("openverse failed:", e, file=sys.stderr)
    try: cands += commons(a.query)
    except Exception as e: print("commons failed:", e, file=sys.stderr)
    seen, uniq = set(), []
    for c in cands:
        k = c["url"].split("?")[0]
        if k not in seen: seen.add(k); uniq.append(c)
    cands = uniq[:12]
    if not cands: sys.exit("no usable free-licence photos ≥1600px — ask Dave for a photo or change the line")
    for f in WORK.glob("cand-*.jpg"): f.unlink()
    for i, c in enumerate(cands, 1):
        try: (WORK / f"cand-{i}.jpg").write_bytes(get(c["url"]))
        except Exception: c["url"] = ""
    state.write_text(json.dumps(cands))
    html = "<html><body style='margin:0;background:#fff;font-family:sans-serif;display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:6px;width:1588px'>"
    for i, c in enumerate(cands, 1):
        html += f"<div style='font-size:13px'><img src='file://{WORK}/cand-{i}.jpg' style='width:390px;height:280px;object-fit:cover;display:block'><b>#{i}</b> {c['licence']} {c['w']}x{c['h']} — {c['title'][:40]} ({c['author'][:20]})</div>"
        print(f"#{i}: {c['licence']} {c['w']}x{c['h']} | {c['title'][:50]} | {c['author'][:25]} | {c['src']}")
    (WORK / "sheet.html").write_text(html + "</body></html>")
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless", "--disable-gpu", "--hide-scrollbars", "--window-size=1600,1000", f"--screenshot={WORK}/sheet.png", f"file://{WORK}/sheet.html"], capture_output=True)
    print(f"\ncontact sheet: {WORK}/sheet.png\npick with: find_stock.py \"{a.query}\" --pick N --name stock-<slug>.jpg")

if __name__ == "__main__":
    main()
