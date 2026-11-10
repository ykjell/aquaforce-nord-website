# Terrassenreinigung – Vorher/Nachher-Reel

Ein Hochkant-Reel für TikTok und Instagram, gebaut mit [HyperFrames](https://hyperframes.heygen.com).
1080×1920, 30 fps, 32,7 s.

**Fertige Videos:**

- `export/terrasse-reel.mp4`: mit leisem Originalton (Maschinengeräusch als Atmo, ca. −35 dB im Mittel)
- `export/terrasse-reel-ohne-ton.mp4`: ohne Ton, für die eigene Sprachaufnahme in CapCut, TikTok oder Instagram

## Schnitt

| Zeit | Szene | Was passiert |
|---|---|---|
| 0,0 – 5,0 | **Intro** | Selfie mit „Diese Terrasse war fällig“, harter Schnitt eng auf die Flecken, Schwenk über die Fläche, dann „Das Werkzeug“ (Hochdruck- und Flächenreiniger). Der Clip ist stumm, weil im Original nicht gesprochen wird |
| 5,0 – 8,0 | **Schritt 1 – Abfegen** | 2× Tempo, 2 Einstellungen |
| 8,0 – 14,6 | **Schritt 2 – Flächenreiniger** | 1,5× Tempo, 3 Einstellungen. Die mittlere zoomt auf die saubere Bahn |
| 14,6 – 19,0 | **Schritt 3 – Hochdruck** | 3 kurze Detail-Shots in leichter Zeitlupe, eng auf Düse und Strahl, mit Weißblitz bei jedem Schnitt |
| 19,0 – 24,5 | **Schritt 4 – Abspülen** | 2× Tempo, 2 Einstellungen |
| 24,5 – 30,2 | **Vorher/Nachher** | Slider wischt einmal komplett durch, geht zurück auf die Mitte (VORHER / NACHHER), wackelt kurz hin und her und gibt am Ende das ganze Nachher-Bild frei |
| 30,2 – 32,7 | **Endkarte** | „Wie neu.“ + AQUAFORCE NORD + „Terrassen- & Pflasterreinigung“ |

Jede Szene schiebt sich mit einem kurzen vertikalen Whip über die vorige.

**Strahl-Clip:** In der Gesamtansicht wirkt das Pflaster fleckig. Deshalb zeigen wir nur drei
enge Ausschnitte von 1,4 bis 1,8 s. Sie zeigen den harten Strahl, den Sprühnebel und frisch freigelegte
Steine in Zeitlupe. So wirkt es nach Detailarbeit und nicht nach „geht nicht weg“.

**Vorher/Nachher-Fotos:** Die beiden Fotos sind aus leicht verschiedenen Positionen aufgenommen.
Das Nachher-Foto ist per Bildabgleich (Homographie) so verzerrt, dass das Pflasterraster
genau auf dem Vorher-Foto liegt. Nur so wirkt der Slider sauber (`tools/align-photos.py`).

## Sprechertext

Du sprichst etwa 2,5 Wörter pro Sekunde. Die Längen passen zu den Szenen.

| Zeit | Szene | Text |
|---|---|---|
| 0 – 1,8 s | Selfie | „Diese Terrasse war echt fällig.“ |
| 1,8 – 3,4 s | Flecken | „Schau dir mal diese Flecken an.“ |
| 3,4 – 5,0 s | Werkzeug | „Mein Werkzeug für heute.“ |
| 5,0 – 8,0 s | Abfegen | „Schritt eins: Erstmal alles grob abfegen.“ |
| 8,0 – 14,6 s | Flächenreiniger | „Dann geht's mit dem Flächenreiniger drüber. Der löst den Dreck gleichmäßig und spritzt nicht rum – Bahn für Bahn über die ganze Fläche.“ |
| 14,6 – 19,0 s | Hochdruck | „Hartnäckige Stellen nehm ich mir danach mit dem Strahl einzeln vor.“ |
| 19,0 – 24,5 s | Abspülen | „Zum Schluss alles gründlich abspülen, damit der ganze gelöste Dreck runter ist.“ |
| 24,5 – 30,2 s | Vorher/Nachher | „Und jetzt der Vergleich … vorher … *(kurze Pause)* … und nachher.“ |
| 30,2 – 32,7 s | Endkarte | „Wie neu! Ist deine Terrasse auch fällig? Schreib uns.“ |

Tipp: Sprich das „vorher“ genau dann, wenn links das Label VORHER steht (ab ca. 27,4 s), und
„nachher“, wenn rechts NACHHER erscheint.

## Bearbeiten und neu rendern

```bash
npm install                       # installiert hyperframes 0.9.29
./prepare-footage.sh IMG_6375.mov IMG_6376.mov IMG_6381.mov IMG_6384.mov intro.mp4   # HDR → SDR, nach assets/footage/
npx hyperframes preview           # Studio-Vorschau im Browser
npm run check                     # Lint + Layout + Kontrast
npm run render                    # → terrasse-reel.mp4
```

Texte wie Hook-Zeilen, Schritt-Titel, Schlusszeile, Firmenname und Leistung sind
HyperFrames-Variablen. Du kannst sie im Studio ändern, ohne Code anzufassen.
Schnittpunkte stehen als `data-media-start` (Startpunkt im Clip), `data-duration` und
`data-playback-rate` (Tempo) direkt an den `<video>`-Tags in `compositions/*.html`.

Die Original-Clips liegen nicht im Repo, weil sie zu groß sind. `assets/footage/` steht in `.gitignore`.
