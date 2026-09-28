#!/bin/bash
# One-time Mac setup for the Loft 331 content system.
# Run from any Terminal, or paste into Claude Code:  bash <(curl -sL https://raw.githubusercontent.com/drg44/loft331-social/main/tools/install-mac.sh)
set -e
REPO="$HOME/loft331-social"
if [ -d "$REPO/.git" ]; then git -C "$REPO" pull -q origin main; else git clone -q https://github.com/drg44/loft331-social "$REPO"; fi
mkdir -p "$HOME/.claude/skills" "$HOME/.claude/commands"
for s in loft331-image loft331-social; do
  rm -rf "$HOME/.claude/skills/$s"; ln -s "$REPO/.claude/skills/$s" "$HOME/.claude/skills/$s"
done
for c in loft-image loft-cycle loft-brand; do
  ln -sf "$REPO/.claude/commands/$c.md" "$HOME/.claude/commands/$c.md"
done
MARK="# loft331-content-system"
if ! grep -q "$MARK" "$HOME/.claude/CLAUDE.md" 2>/dev/null; then
  cat >> "$HOME/.claude/CLAUDE.md" <<'RULE'

# loft331-content-system
Any request for a Loft 331 image, thumbnail, share/OG image, banner, post, or content calendar MUST use the loft331-image
or loft331-social skill in ~/loft331-social (never restyle from the website, never invent a palette or logo).
Run `git -C ~/loft331-social pull` first. See ~/loft331-social/CLAUDE.md.
RULE
fi
echo "Loft 331 content system installed at $REPO"
echo "skills:   ~/.claude/skills/loft331-image, loft331-social"
echo "commands: /loft-image  /loft-cycle  /loft-brand"
