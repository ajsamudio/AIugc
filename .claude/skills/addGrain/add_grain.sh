#!/usr/bin/env bash
# Usage: add_grain.sh [--strength light|medium|heavy] <image|folder> [...]
# Writes <source dir>/grain/<name>.jpg next to each input. Originals untouched.
set -e
S=medium
[ "$1" = "--strength" ] && { S=$2; shift 2; }
case $S in
  light)  N=6;  Q=4; SH=0.4 ;;
  medium) N=10; Q=6; SH=0.6 ;;
  heavy)  N=18; Q=9; SH=0.8 ;;
  *) echo "strength must be light|medium|heavy"; exit 1 ;;
esac
VF="eq=saturation=0.9:contrast=0.97:brightness=-0.02,unsharp=5:5:$SH,noise=alls=$N:allf=t+u,vignette=PI/6"
proc(){ local f="$1" out="$(dirname "$1")/grain"; mkdir -p "$out"
  local n="$(basename "${f%.*}")"
  ffmpeg -y -loglevel error -i "$f" -vf "$VF" -q:v $Q "$out/$n.jpg" && echo "ok $out/$n.jpg"; }
for a in "$@"; do
  if [ -d "$a" ]; then
    find "$a" -maxdepth 1 -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.webp' \) | while read -r f; do proc "$f"; done
  else proc "$a"; fi
done
