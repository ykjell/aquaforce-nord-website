#!/usr/bin/env bash
# Wandelt die iPhone-Originale (HEVC, HDR/HLG, Dolby Vision) in SDR-H.264-Clips um,
# die die Komposition unter assets/footage/ erwartet. Die Clips sind zu groß für Git.
#
#   ./prepare-footage.sh IMG_6375.mov IMG_6376.mov IMG_6381.mov IMG_6384.mov
#   (Reihenfolge: Fegen, Flächenreiniger, Strahl, Abspülen)
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p assets/footage
names=(01-fegen 02-flaechenreiniger 03-strahl 04-abspuelen)
VF="zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv:w=1080:h=1920,format=yuv420p,fps=30"
i=0
for src in "$@"; do
  ffmpeg -v error -i "$src" -map 0:v:0 -map 0:a:0 -vf "$VF" -c:v libx264 -crf 19 -preset fast -g 15 \
    -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 160k -movflags +faststart \
    -y "assets/footage/${names[$i]}.mp4" &
  i=$((i + 1))
done
wait
echo "Fertig: assets/footage/"
