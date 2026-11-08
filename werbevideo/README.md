# AquaForce-Nord – Premium-Werbespot (30 s, 9:16)

**Fertiger Clip:** `aquaforce-nord-werbespot.mp4`, 1080 × 1920, 30 fps, H.264 + AAC, ca. −14 LUFS (Social-Media-Norm)

Der Spot ist komplett **prozedural gerendert**: Steinoberflächen, Licht, Wasserstrahl, Partikel,
Typografie und Ton entstehen aus Code. Dadurch gibt es keine KI-Artefakte. Der Text bleibt scharf
und richtig geschrieben, die Steine verzerren nicht, und alle Szenen haben dieselbe Lichtsprache.

> **Ehrlicher Hinweis zu Higgsfield:** In der Umgebung, in der dieser Spot gebaut wurde, gab es
> **keinen Zugang zu Higgsfield** (kein Konto, keine API). Higgsfield wurde deshalb **nicht verwendet**.
> Bild, Bewegung und Ton sind selbst programmiert bzw. synthetisiert. Unten steht ein
> [Workflow](#optional-szenen-mit-higgsfield-ersetzen), mit dem du einzelne Szenen später durch
> Higgsfield-Footage ersetzen kannst, ohne Schrift und Logo neu zu bauen.

## Dein Logo einsetzen (wichtig)

Im Repository lag noch kein Logo. Bis dahin zeigt der Abschluss eine **Platzhalter-Wortmarke**
(„AQUAFORCE NORD“).

1. Logo als `werbevideo/assets/logo.png` ablegen (transparenter Hintergrund, mindestens 1200 px breit;
   `.svg`, `.webp` und `.jpg` werden auch erkannt).
2. `node render.mjs` erneut ausführen.

Das Logo wird **unverändert** eingesetzt: kein Umfärben, kein Verzerren, das Seitenverhältnis bleibt
erhalten. Es wird nur in eine Box von max. 640 × 360 px eingepasst. Die Lichtkante beim Reveal läuft
einmal kurz darüber, danach steht das Logo im Original.

## Ablauf

| Zeit | Szene | Bild | Text | Ton |
|---|---|---|---|---|
| 0–4 s | Einstieg | Schwarz, Lichtstrahl fährt durchs Bild, Tropfen in Zeitlupe, Aufprall mit Ringen auf dunkler Wasserfläche | „Schmutz / hinterlässt / **Spuren.**“ | Licht-Whoosh L→R, Tropfen-Plink, Pad setzt ein |
| 4–9 s | Problem | Vermooste Terrassenplatten (Algenfilm, Flechten, Moos in den Fugen) in Streiflicht, langsame Kamerafahrt mit Tiefenunschärfe | – | Bassimpuls, Arpeggio beginnt, Riser |
| 9–16 s | Transformation | Wasserfächer fährt von links nach rechts durchs Bild. Links davon sauber und nass, mit Schmutzwasser-Kante und Gischt. **Zeitlupe 10,4–13,6 s** (Tropfen frieren fast ein) | – | Hochdruckstrahl (Stereo folgt dem Strahl), in der Zeitlupe tief und dumpf, Herzschlag-Sub |
| 16–22 s | Ergebnis | Drei saubere, nasse Flächen mit wandernden Reflexen: Platten, Fischgrät-Pflaster, Granit-Kleinpflaster | „Terrassen.“ · „Einfahrten.“ · „Pflasterflächen.“ (nacheinander) | Weiche Kick, Swishes an den Schnitten |
| 22–30 s | Abschluss | Dunkler Raum, blauer Lichtschein, Logo-Reveal mit Lichtkante | „Deine Fläche. **Wie neu.**“ → Button „Jetzt Hochdruckreinigung anfragen.“ → „Unverbindlich & fair.“ → „Bordesholm · Schleswig-Holstein“ | Logo-Hit mit Glocke, Auflösung nach Dsus2 |

Musik: 120 BPM, damit alle Szenenwechsel (4 / 9 / 16 / 22 s) genau auf einem Schlag liegen.
Akkordfolge Dm(add9) → B♭maj7 → Fmaj9 → Dsus2. Sie bleibt dunkel und öffnet sich zum Ergebnis.
Klassische Werbe-Fanfaren gibt es nicht.

## Safe Zones

Alle Texte und das Logo liegen in einem Rahmen von **x 170–890, y 220–1440**:

- oben 220 px frei (Statusleiste, „Für dich / Folge ich“, Reels-Header)
- unten 480 px frei (Profilname, Caption, Musik-Zeile, Kommentarfeld)
- rechts 160 px frei zwischen y 700 und 1440 (Like-, Kommentar-, Teilen-Buttons)
- die optische Mitte liegt bei x = 530 statt 540, also leicht von der Button-Spalte weg

Kontrolle: `index.html` im Browser öffnen und **S** drücken (rot = UI-Flächen, grün = Textrahmen),
oder `node render.mjs --safe` rendern.

## Selbst rendern

```bash
cd werbevideo
python3 audio.py            # → soundtrack.wav (nur numpy nötig)
node render.mjs             # → aquaforce-nord-werbespot.mp4   (playwright + ffmpeg nötig)

node render.mjs --stills 2,7,12,19,27   # Einzelbilder zur Kontrolle
node render.mjs --overlay               # nur Schrift + Logo mit Alpha → ProRes 4444 .mov
```

`index.html` direkt im Browser öffnen = Vorschau mit Ton, Klick/Leertaste = Pause, Regler = Spulen.
Beim ersten Laden werden die Steintexturen etwa 5–10 s lang berechnet.

### Texte ändern

Alle Texte stehen in `index.html`. Suche nach `headline1` (Szene 1), `SHOTS` (Szene 4) und
`scene5fg` (Abschluss). Telefonnummer oder Website gab es keine, deshalb fehlen sie im Spot.
Ergänzen kannst du sie bei `Bordesholm · Schleswig-Holstein`.

## Optional: Szenen mit Higgsfield ersetzen

Wenn du die Steinflächen später durch fotorealistisches KI-Footage ersetzen willst, ist das der
sinnvolle Weg. Die Typografie und das Logo bleiben aus diesem Projekt und damit garantiert
fehlerfrei. Die verfügbaren Funktionen hängen von deinem Higgsfield-Plan ab. Bitte dort prüfen,
was es gerade gibt (z. B. Bildgenerierung, Bild-zu-Video mit Kamerabewegungen, ggf. Audio).

1. **Stil-Referenz zuerst.** Ein Standbild aus diesem Spot (`node render.mjs --stills 7,14,17`)
   in Higgsfield als Referenz hochladen. Dann passen Farbwelt und Licht zu den übrigen Szenen.
2. **Erst ein Standbild erzeugen, dann animieren.** Bild-zu-Video ist deutlich konsistenter als
   Text-zu-Video.
3. **Kurze Clips mit einer einzigen, langsamen Kamerabewegung.** Keine Schnitte im Clip und keine
   Schrift im KI-Bild.
4. **Zusammensetzen:** `node render.mjs --overlay` liefert alle Texte und das Logo als
   transparentes ProRes-4444-Video. In CapCut, DaVinci Resolve oder Premiere kommt es auf eine
   Spur über dein Footage. Dazu `soundtrack.wav` als Tonspur.

Prompt-Vorlagen (Englisch funktioniert bei Bildmodellen meist zuverlässiger):

- **Szene 2 – Problem:** *Macro close-up of weathered concrete patio slabs covered in green algae
  film, dark lichen spots and moss growing in the joints, low raking side light from the left,
  dark navy ambient, shallow depth of field, cinematic product photography, 9:16 vertical, no text.*
  Kamera: langsame Vorwärtsfahrt knapp über dem Boden.
- **Szene 3 – Transformation:** gleiches Startbild. *A flat-fan high-pressure water jet sweeps
  from left to right, revealing clean light-grey stone behind it, fine mist and droplets in slow
  motion, dirty water pushed ahead of the jet, realistic physics, cool cyan backlight, no people,
  no text.* Danach in deinem Schnittprogramm die Mitte des Clips auf ca. 30 % verlangsamen.
- **Szene 4 – Ergebnis:** drei Standbilder: *freshly cleaned wet terrace slabs / anthracite
  herringbone driveway pavers / granite cobblestones, soft studio reflection gliding across the wet
  surface, dark fog in the background, premium minimal look, 9:16, no text*. Kamera: langsamer
  Seitwärts-Slide.

Zum Vermeiden: Schrift oder Logo in Higgsfield generieren lassen, Text-zu-Video ohne Referenzbild,
schnelle Kamerafahrten, Personen mit Geräten (Hände und Lanzen werden oft verzerrt).

## Dateien

| Datei | Inhalt |
|---|---|
| `index.html` | Der gesamte Spot: Texturen, Kamera, Wasserstrahl, Typografie, Vorschau-Player |
| `render.mjs` | Export: Frames → ffmpeg (MP4, Overlay-MOV oder Standbilder) |
| `audio.py` | Musik und Sounddesign → `soundtrack.wav` |
| `assets/` | Hier `logo.png` ablegen |
