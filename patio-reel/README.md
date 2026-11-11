# Terrassenreinigung – Vorher/Nachher-Reel

Ein Hochkant-Reel für TikTok und Instagram, gebaut mit [HyperFrames](https://hyperframes.heygen.com).
1080×1920, 30 fps, 36,2 s, mit Voiceover.

**Fertiges Video:** `export/terrasse-reel.mp4`. Es enthält deinen Voiceover, darunter leise die Maschinengeräusche.
Die Lautstärke liegt bei −14 LUFS, dem üblichen Wert für TikTok und Instagram.

## Schnitt

| Zeit | Szene | Was passiert |
|---|---|---|
| 0,0 – 6,4 | **Intro** | Selfie mit „Diese Terrasse war fällig“, harter Schnitt eng auf die Flecken, Schwenk über die Fläche, dann „Das Werkzeug“ (Hochdruck- und Flächenreiniger) |
| 6,4 – 9,7 | **Schritt 1 – Abfegen** | 2× Tempo, 2 Einstellungen |
| 9,7 – 16,6 | **Schritt 2 – Flächenreiniger** | 1,5× Tempo, 3 Einstellungen. Die mittlere zoomt auf die saubere Bahn |
| 16,6 – 21,0 | **Schritt 3 – Hochdruck** | 3 kurze Detail-Shots in leichter Zeitlupe, eng auf Düse und Strahl, mit Weißblitz bei jedem Schnitt |
| 21,0 – 26,5 | **Schritt 4 – Abspülen** | 2× Tempo, 2 Einstellungen |
| 26,5 – 32,8 | **Vorher/Nachher** | Getimt auf die Stimme: VORHER-Label bei „Vorher“, Wisch bei „und nachher“, zurück zur Mitte bei „Krass, oder?“, danach kurz hin und her |
| 32,8 – 36,2 | **Endkarte** | „Wie neu.“ + AQUAFORCE NORD + „Terrassen- & Pflasterreinigung“ |

Jede Szene schiebt sich mit einem kurzen vertikalen Whip über die vorige.

**Strahl-Clip:** In der Gesamtansicht wirkt das Pflaster fleckig. Deshalb zeigen wir nur drei
enge Ausschnitte von 1,4 bis 1,8 s. Sie zeigen den harten Strahl, den Sprühnebel und frisch freigelegte
Steine in Zeitlupe. So wirkt es nach Detailarbeit und nicht nach „geht nicht weg“.

**Vorher/Nachher-Fotos:** Die beiden Fotos sind aus leicht verschiedenen Positionen aufgenommen.
Das Nachher-Foto ist per Bildabgleich (Homographie) so verzerrt, dass das Pflasterraster
genau auf dem Vorher-Foto liegt. Nur so wirkt der Slider sauber (`tools/align-photos.py`).

## Voiceover

Die Aufnahme liegt unter `assets/audio/voiceover.wav`. Sie wurde von tiefem Rumpeln befreit, leicht entrauscht und komprimiert
und ist auf einheitliche Lautstärke gebracht. Jeder Satz ist ein eigener `<audio>`-Clip in `index.html` (`vo-01` bis `vo-14`).
Dort steht jeweils, wann er im Video kommt (`data-start`) und wo er in der Aufnahme liegt (`data-media-start`).
Der Satztext steht im `title`.

| Video | Satz |
|---|---|
| 0,2 s | Intro Satz 1 (neu aufgenommen, `voiceover-intro.wav`) |
| 2,9 s | Intro Satz 2 (neu aufgenommen, `voiceover-intro.wav`) |
| 4,8 s | „Das ist heute mein Werkzeug.“ |
| 6,6 s | „Erster Schritt, alles einmal grob abfegen.“ |
| 9,8 s | „Dann kommt der Flächenreiniger drauf, Bahn für Bahn über die ganze Fläche.“ |
| 13,9 s | „Der löst den Dreck schön gleichmäßig.“ |
| 16,6 s | „Hartnäckige Stellen nehme ich mir mit dem Strahl einzeln vor.“ |
| 21,0 s | „Zum Schluss alles gründlich abspülen, bis der ganze Dreck runter ist.“ |
| 26,5 s | „Und jetzt der Vergleich.“ |
| 28,1 s | „Vorher …“ |
| 29,2 s | „… und nachher.“ |
| 30,5 s | „Krass, oder?“ |
| 32,8 s | „Wie neu.“ |
| 33,7 s | „Deine Terrasse auch? Schreib uns.“ |

## Bearbeiten und neu rendern

```bash
npm install                       # installiert hyperframes 0.9.29
./prepare-footage.sh IMG_6375.mov IMG_6376.mov IMG_6381.mov IMG_6384.mov intro.mp4   # HDR → SDR, nach assets/footage/
npx hyperframes preview           # Studio-Vorschau im Browser
npm run check                     # Lint + Layout + Kontrast
npm run render                    # → terrasse-reel.mp4 (danach für Social auf −14 LUFS normalisieren)
```

Texte wie Hook-Zeilen, Schritt-Titel, Schlusszeile, Firmenname und Leistung sind
HyperFrames-Variablen. Du kannst sie im Studio ändern, ohne Code anzufassen.
Schnittpunkte stehen als `data-media-start` (Startpunkt im Clip), `data-duration` und
`data-playback-rate` (Tempo) direkt an den `<video>`-Tags in `compositions/*.html`.

Die Original-Clips liegen nicht im Repo, weil sie zu groß sind. `assets/footage/` steht in `.gitignore`.

## Titelbild

`export/titelbild.jpg` (und `.png`), 1080×1920. Das Bild ist diagonal geteilt: oben die Vorher-, unten die Nachher-Seite.
Darauf stehen „NEUESTER AUFTRAG“, „TERRASSE WIE NEU“ und AQUAFORCE NORD.
Die Quelle ist `cover/index.html`, eine eigene HyperFrames-Szene. Oberzeile, Titel und Firmenname sind dort Variablen.
Neu exportieren:

```bash
cd cover && npx hyperframes snapshot . --at 0 --output ../snapshots/cover
```
