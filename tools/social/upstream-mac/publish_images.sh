#!/bin/zsh
# Push a campaign's rendered images to the public loft331-social repo and print the Buffer base URL.
# Usage: ./publish_images.sh <campaign-name>
set -e
C="$1"; [ -n "$C" ] || { echo "usage: publish_images.sh <campaign-name>"; exit 1; }
SRC=~/loft331-mgmt/social/campaigns/"$C"/posts
PUB=~/loft331-mgmt/social/public
[ -d "$SRC" ] || { echo "no posts folder at $SRC (render first)"; exit 1; }
mkdir -p "$PUB/$C/posts"
for d in "$SRC"/*/; do n=$(basename "$d"); mkdir -p "$PUB/$C/posts/$n"; cp "$d"post-*.png "$PUB/$C/posts/$n/"; done
cd "$PUB" && git add -A && git commit -qm "Add $C images" 2>/dev/null || true
git push -q origin main
echo "https://raw.githubusercontent.com/drg44/loft331-social/main/$C"
# Wait until GitHub's CDN serves the new bytes (up to ~2 min) so Buffer never fetches a stale image.
for d in "$SRC"/*/; do
  n=$(basename "$d"); f=$(ls "$d"/post-*.png 2>/dev/null | head -1); [ -f "$f" ] || continue; b=$(basename "$f")
  want=$(md5 -q "$f"); url="https://raw.githubusercontent.com/drg44/loft331-social/main/$C/posts/$n/$b?cb=$(date +%s)"
  for i in $(seq 1 12); do
    got=$(curl -sL --max-time 20 "$url" | md5 -q); [ "$got" = "$want" ] && break; sleep 10
  done
  [ "$got" = "$want" ] || echo "WARNING: CDN still stale for $n"
done
