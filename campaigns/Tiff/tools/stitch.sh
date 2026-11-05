#!/usr/bin/env bash
# Jump-cut clips into one post. Usage: stitch.sh OUT.mp4 clip.mp4:END_SEC|START-END|full [clip2:...]
# Each part is scaled to 720x1280, trimmed, concatenated, then loudnorm to -14 LUFS.
set -euo pipefail
out="$1"; shift
inputs=(); filters=""; n=0
for spec in "$@"; do
  f="${spec%:*}"; end="${spec##*:}"
  inputs+=(-i "$f")
  trim=""; atrim=""
  if [[ "$end" == *-* ]]; then
    trim="trim=start=${end%-*}:end=${end#*-},"; atrim="atrim=start=${end%-*}:end=${end#*-},"
  elif [ "$end" != "full" ]; then
    trim="trim=end=$end,"; atrim="atrim=end=$end,"
  fi
  filters+="[$n:v]${trim}setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v$n];"
  filters+="[$n:a]${atrim}asetpts=PTS-STARTPTS,aresample=48000[a$n];"
  n=$((n+1))
done
cat=""; for i in $(seq 0 $((n-1))); do cat+="[v$i][a$i]"; done
filters+="${cat}concat=n=$n:v=1:a=1[v][a0];[a0]loudnorm=I=-14:TP=-1.5:LRA=11[a]"
mkdir -p "$(dirname "$out")"
ffmpeg -loglevel error -y "${inputs[@]}" -filter_complex "$filters" -map "[v]" -map "[a]" \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$out"
echo "saved $out"
