#!/usr/bin/env bash
# AI-upscale a video with Real-ESRGAN (local, free, RTX GPU).
# Usage: bash upscale.sh <input.mp4> [1080|4k|both]   (default: 1080)
# Output: <input>_upscaled_1080p.mp4 / _4k.mp4 next to the input, original audio kept.
set -euo pipefail
IN="$(realpath "$1")"; MODE="${2:-1080}"
HERE="$(cd "$(dirname "$0")" && pwd)"; BIN="$HERE/realesrgan/realesrgan-ncnn-vulkan.exe"
BASE="${IN%.*}"; WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/in" "$WORK/out"

FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$IN")
W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$IN")
H=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$IN")
HASA=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" | head -1)

# 1) back to true generation res (short side 720) so the AI sees real pixels
if [ "$W" -lt "$H" ]; then SC="720:-2"; else SC="-2:720"; fi
ffmpeg -hide_banner -loglevel error -y -i "$IN" -vf "scale=$SC:flags=lanczos" "$WORK/in/%05d.png"
echo "frames: $(ls "$WORK/in" | wc -l) — upscaling x4..."
# 2) Real-ESRGAN x4
"$BIN" -i "$WORK/in" -o "$WORK/out" -n realesrgan-x4plus -s 4 -f png >/dev/null 2>&1
# 3) downscale + light grain (stops plastic skin) + encode, keep audio
enc() { # $1 = short side, $2 = suffix
  if [ "$W" -lt "$H" ]; then S="$1:-2"; else S="-2:$1"; fi
  AUD=(); [ -n "$HASA" ] && AUD=(-i "$IN" -map 0:v -map 1:a -c:a aac -b:a 192k -shortest)
  ffmpeg -hide_banner -loglevel error -y -framerate "$FPS" -i "$WORK/out/%05d.png" "${AUD[@]}" \
    -vf "scale=$S:flags=lanczos,noise=alls=3:allf=t,format=yuv420p" \
    -c:v libx264 -preset slow -crf 16 -movflags +faststart "${BASE}_upscaled_$2.mp4"
  echo "saved ${BASE}_upscaled_$2.mp4"
}
case "$MODE" in
  1080) enc 1080 1080p ;;
  4k)   enc 2160 4k ;;
  both) enc 1080 1080p; enc 2160 4k ;;
esac
