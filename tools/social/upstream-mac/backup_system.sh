#!/bin/zsh
# Back up everything Claude needs to run Loft 331 social into the synced Drive master folder.
# Run at the end of every cycle (the skill does this) or any time: ./backup_system.sh
set -e
DEST="$HOME/Library/CloudStorage/GoogleDrive-dan@loft331.ca/My Drive/Loft 331 Social/System"
[ -d "$(dirname "$DEST")" ] || { echo "Drive not synced — is Google Drive for Desktop running?"; exit 1; }
mkdir -p "$DEST"/{brand,social-tools,skill,memory,fonts}
rsync -a --delete ~/loft331-mgmt/brand/notebooklm/Loft331-Brand-Guidelines.md "$DEST/brand/"
rsync -a --delete ~/loft331-mgmt/brand/loft331-brand.css ~/loft331-mgmt/brand/README.md "$DEST/brand/"
rsync -a --delete --exclude 'samples' --exclude 'test' ~/loft331-mgmt/brand/social/ "$DEST/social-tools/"
rsync -a --delete ~/Documents/GitHub/loft331-static/assets/fonts/ "$DEST/fonts/"
rsync -a --delete ~/.claude/skills/loft331-social/ "$DEST/skill/"
rsync -a ~/.claude/projects/-Users-daveg-claude-skills/memory/loft331-notebooklm-gem-pipeline.md "$DEST/memory/"
rsync -a ~/loft331-mgmt/social/posted-log.csv "$DEST/"
cat > "$DEST/RESTORE.txt" <<'R'
LOFT 331 SOCIAL - SYSTEM BACKUP

Everything Claude needs to run the social cycle, if the Mac is gone.

brand/         Loft331-Brand-Guidelines.md (the rulebook), brand CSS, brand README
social-tools/  render.py, render_calendar.py, buffer_export.py, publish_images.sh, backup_system.sh, templates, logo (logo.png + logo.b64), voice-guide.md
fonts/         fraunces.woff2, lato.woff2 (the real site fonts the templates use)
skill/         SKILL.md - Claude's step-by-step process
memory/        Claude's project notes (IDs for Buffer, Drive, GitHub; what was decided and why)
posted-log.csv What has been posted (prevents repeats)

TO RESTORE ON A NEW MAC
1. Install Google Drive for Desktop, sign in as dan@loft331.ca. This folder syncs back.
2. Copy: brand/ -> ~/loft331-mgmt/brand/notebooklm/ and ~/loft331-mgmt/brand/
         social-tools/ -> ~/loft331-mgmt/brand/social/
         fonts/ -> ~/Documents/GitHub/loft331-static/assets/fonts/ (or edit the font paths in loft331-brand.css)
         skill/ -> ~/.claude/skills/loft331-social/
         memory/ -> Claude's memory folder for the project
         posted-log.csv -> ~/loft331-mgmt/social/
3. Install Google Chrome (the renderer uses headless Chrome) and Python 3.
4. Reconnect the Buffer MCP (claude mcp add --transport http buffer https://mcp.buffer.com/mcp) and GitHub (gh auth login as drg44).
5. Tell Claude: "Read the Loft 331 Social System backup and restore the social pipeline."

Photos, Inputs sheet, calendars, and the How It Works doc live in the parent folder and never left Drive.
Rendered images are also in the public repo github.com/drg44/loft331-social.
R
echo "backed up to: $DEST"; du -sh "$DEST" | cut -f1
