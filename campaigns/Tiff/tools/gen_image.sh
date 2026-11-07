#!/usr/bin/env bash
# Codex CLI (GPT Image) wrapper. Usage: gen_image.sh OUT.png PROMPT.txt REF1 [REF2 ...]
# Paths are relative to campaigns/Tiff. Codex writes into ~/.codex/generated_images/<session>/; we copy the newest PNG to OUT.
set -euo pipefail
cd "$(dirname "$0")"
# WindowsApps can't be globbed; ask Appx for the current install folder
CODEX="$(cygpath -u "$(powershell -NoProfile -c '(Get-AppxPackage OpenAI.Codex).InstallLocation' | tr -d '\r')")/app/resources/codex.exe"
out="$1"; prompt="$2"; shift 2
imgs=(); for r in "$@"; do imgs+=("--image=$r"); done
stamp="$(mktemp)"; log="$(mktemp)"; sleep 1
"$CODEX" exec --skip-git-repo-check "${imgs[@]}" \
  "Use your built-in image generation tool to create exactly ONE image from the attached references and the instructions below. Do not write code, do not edit files, just generate the image. $(cat "$prompt")" </dev/null 2>&1 | tee "$log"
# other Codex runs may write to generated_images at the same time; only look in this run's session folder
sid="$(grep -oiE 'session id: [0-9a-f-]+' "$log" | head -1 | awk '{print $3}')"
[ -n "$sid" ] || { echo "no session id in codex output" >&2; exit 1; }
new="$(find ~/.codex/generated_images/"$sid" -type f -name '*.png' -newer "$stamp" -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)"
rm -f "$stamp" "$log"
[ -n "$new" ] || { echo "no image generated" >&2; exit 1; }
mkdir -p "$(dirname "$out")"; cp "$new" "$out"; echo "saved $out"
