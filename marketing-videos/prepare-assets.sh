#!/bin/bash
# Erzeugt assets/clips und assets/img aus dem Original-Handymaterial (HDR -> SDR, Grade, 9:16, 30 fps).
#   ./prepare-assets.sh /pfad/zum/originalmaterial
# Erwartete Dateien: IMG_6539_2.MOV, IMG_6549.MOV, IMG_6536_2.MOV, worker.mp4 (464x832),
# pov_sonne.mp4 (39 s), pov_nass.mp4 (44 s), rundgang_halb.mp4 (25 s) sowie die 8 Fotos (Namen siehe unten).
set -e
U="$1"; mkdir -p assets/clips assets/img
TM="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
G="eq=contrast=1.07:saturation=1.12:gamma=0.96,curves=m='0/0 0.25/0.22 0.75/0.78 1/1'"
ENC="-an -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -g 15 -movflags +faststart"
hd(){ ffmpeg -v error -y -ss $2 -t $3 -i "$U/$1" -vf "$TM,$G,scale=1080:1920,fps=30" $ENC assets/clips/$4.mp4; }
lo(){ ffmpeg -v error -y -ss $2 -t $3 -i "$U/$1" -vf "${6}scale=1080:1920:flags=lanczos,unsharp=7:7:0.8,$G,noise=alls=5:allf=t,fps=$5" $ENC assets/clips/$4.mp4; }
hd IMG_6539_2.MOV 0 4.6 a_point;  hd IMG_6539_2.MOV 4.6 17.4 a_walk
hd IMG_6549.MOV 0 17 b_walk;      hd IMG_6536_2.MOV 0 13.6 c_walk
lo pov_sonne.mp4 0 16 e_pov 30 "";  lo pov_nass.mp4 0 14 g_pov 30 "";  lo pov_nass.mp4 22 12 g_edge 30 ""
lo worker.mp4 0 10.6 d_worker 60 ""
lo rundgang_halb.mp4 0 3.2 f_point 30 "crop=432:768,";  lo rundgang_halb.mp4 10.5 5.2 f_half 30 "crop=432:768,"
for n in steps_a split terrace_before steps_b entrance_before path_before terrace_after side_after; do
  ffmpeg -v error -y -i "$U/$n.jpg" -vf "scale=1620:-2:flags=lanczos,$G" -q:v 3 assets/img/$n.jpg
done
ffmpeg -v error -y -ss 13.3 -i assets/clips/c_walk.mp4 -frames:v 1 -q:v 2 assets/img/side_before.jpg
