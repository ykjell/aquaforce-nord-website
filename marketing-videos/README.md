# AquaForce-Nord · 5 Reels (TikTok / Instagram, 9:16)

Fünf eigenständige Werbevideos aus dem Material eines Reinigungsauftrags (Terrasse + Gehweg),
gebaut mit [HyperFrames](https://hyperframes.heygen.com) (HTML + GSAP → MP4). 1080×1920, 30 fps, ohne Ton
(Voiceover und Musik kommen später dazu).

| Datei | Konzept | Länge | Hook (Frame 0) |
|---|---|---|---|
| `renders/01-die-linie.mp4` | Satisfying-POV: die Lanze zieht die Linie, Reveal „Derselbe Stein." | 17,4 s | „Wie viel Dreck steckt in Ihrem Pflaster?" |
| `renders/02-vorher-nachher.mp4` | Schieberegler + Wasser-Wisch: Weg, Terrasse, echte Grenze | 17,0 s | Halb/halb-Bild mit Regler |
| `renders/03-der-rundgang.mp4` | Synchroner Split-Screen: derselbe Rundgang vorher/nachher | 17,4 s | „Gleicher Rundgang." |
| `renders/04-markenfilm.mp4` | Markenfilm: Profi in Zeitlupe, Leistungen, Fenster wird zur Welt | 16,0 s | „Keine halben Sachen." |
| `renders/05-drei-zeichen.mp4` | Ratgeber-Listicle: 3 Zeichen, dass das Pflaster überfällig ist | 21,6 s | „3 Zeichen, dass Ihr Pflaster überfällig ist." |

## Markensystem

- Farben: Navy `#06192B`, Aqua `#18C8FF`, Weiß `#F4F8FB`
- Schrift: Barlow Condensed (Headlines), Inter (Fließtext), JetBrains Mono (Labels)
- Signet oben links, einheitliche Endkarte mit CTA „Jetzt Angebot anfragen"
- Safe-Zones: alle Texte zwischen y = 168 px und 1330 px, nichts unter der rechten Button-Leiste
- Wortmarke und Tropfen-Signet sind ein Platzhalter-Entwurf: echtes Logo in `build.mjs` (`bug`, `endcard`) einsetzen

## Aufbau

```
src/_brand.css          gemeinsames Design
src/0X-….html           je ein Reel (Markup + GSAP-Timeline)
build.mjs               setzt Kopf, Signet, Endkarte ein → reels/<name>/index.html
prepare-assets.sh       Originalmaterial → assets/clips (HDR→SDR, Grade, 9:16)
assets/img, fonts       Fotos (gegradet), Schriften, GSAP
renders/                fertige MP4s
```

`assets/clips/` (ca. 290 MB) liegt nicht im Repo; mit `prepare-assets.sh` aus dem Originalmaterial neu erzeugen.

## Ändern und neu rendern

```bash
node build.mjs
./hf.sh render reels/01-die-linie -o renders/01-die-linie.mp4 --crf 21
./hf.sh preview reels/01-die-linie      # Vorschau im Browser
```

Texte stehen direkt im jeweiligen `src/0X-….html`, die Zeiten in `data-start` / `data-duration` und in der Timeline darunter.
