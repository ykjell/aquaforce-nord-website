# Vorher / Nachher – Pflasterreinigung (Social-Media-Clip)

HyperFrames-Komposition (`index.html`, 1080×1920, 30 fps, 16,8 s) aus zwei Handy-Videos
(IMG_6536 = vorher, IMG_6539 = nachher). Fertiges Video: `vorher-nachher.mp4`.

## Ablauf

| Zeit | Szene |
|---|---|
| 0.0 – 3.0 | **Einstieg:** Vorher/Nachher-Slider über den Gartenweg (ausgerichtete Standbilder) |
| 3.0 | Whip-Pan in die erste Szene |
| 3.0 – 5.2 | **VORHER · Terrasse**, ruhige Zeitlupe (Quelle 0–1,55 s, Bewegung interpoliert) |
| 5.15 – 6.05 | **Hochdruck-Wipe**: leuchtender Wasserstrahl mit Sprühnebel fährt von unten nach oben und legt das saubere Pflaster frei |
| 6.0 – 8.2 | **NACHHER · Terrasse** |
| 8.25 | Whip-Pan zum Gartenweg |
| 8.3 – 10.1 | **VORHER · Gartenweg** |
| 10.15 – 10.6 | **Zoom-Punch + Weißblitz** |
| 10.4 – 13.3 | **NACHHER · Gartenweg** mit Glanzstreifen und Funkeln |
| 13.3 – 16.8 | Fertiges Bild zoomt raus, wird unscharf → „AQUAFORCE NORD · Pflaster wieder wie neu · Link in Bio" |

Sound: nur selbst erzeugte Effekte (Wasserzischen, Whooshes, Impact, Glitzern) – Musik
am besten direkt in TikTok/Instagram drüberlegen.

## Bearbeiten & neu rendern

```bash
npm run dev      # Vorschau im Browser
npm run check    # Prüfung
npm run render   # → vorher-nachher.mp4
```

Die Clips in `assets/clips/` sind aus den iPhone-HDR-Originalen (HLG/Dolby Vision) nach
SDR BT.709 konvertiert und zugeschnitten, z. B.:

```bash
TM="zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
ffmpeg -i IMG_6539.mov -vf "$TM" -c:v libx264 -crf 16 after.mp4
ffmpeg -ss 5.0 -t 3.4 -i after.mp4 -an -c:v libx264 -crf 19 assets/clips/nachher-terrasse.mp4
```
