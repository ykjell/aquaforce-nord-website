# „Know your limits." – TikTok-Edit-Nachbau

Nachbau des TikTok-Edits (iMessage-Chat → Claude-Wortmarke → Cockpit → Montage) komplett in Code:
ein `<canvas>` (1080×1920, 9:16), alle Szenen prozedural gezeichnet, Loop von 11,9 s.

## Ansehen

`index.html` im Browser öffnen. Klick / Leertaste = Pause, Regler = Spulen.

## Als MP4 exportieren

```bash
npm i playwright && npx playwright install chromium   # einmalig
node render.mjs                     # → know-your-limits.mp4 (30 fps, ohne Ton, BT.709)
node render.mjs --fps 60
node render.mjs --audio song.m4a    # eigene Tonspur dazumischen
```

## Wie exakt ist das?

Alle Werte sind aus dem Original-Video gemessen (Bildschirmaufnahme 1170×2532, 60 fps):

- **Schnitte**: per Frame-Differenz ermittelt. Im fertigen MP4 liegt jeder der 21 Schnitte
  innerhalb eines Frames (≤ 33 ms) am Original.
- **Chat**: Blasenkanten, Textbreiten und die sechs Zoomstufen (Skalierung + Versatz) sind
  aus den Pixeln der Blasen berechnet, Abweichung ≤ 8 px.
- **Farben**: Blase grau `#232029`, blau `#0a7afe`, Orange `#ff784e`, Navy `#12131b`,
  Schrift auf Orange `#130810`.
- **Logo-Animation**: Position und Größe des Funkens bei 60 fps vermessen; Buchstaben-Stufen
  „C" → „Clau" → „Claude" wie im Original.
- **Bildausschnitt**: Logo-Szenen im Band Original-y 534–1747, Montage-Clips 499–1783.

Die Montage-Clips im Original sind Bildschirmaufnahmen fremder Projekte. Sie sind hier im
gleichen Layout, Farbschema und Bewegungsablauf neu gezeichnet und keine Pixelkopien.
Das Pixel-Maskottchen ist ein eigener Entwurf.

## Timeline (Sekunden)

| Zeit | Szene |
|---|---|
| 0.000 – 3.033 | iMessage-Chat „Do you love me? / Yeah / More than Claude? / Know your limits." – 6 harte Zoom-Schnitte |
| 3.033 – 4.167 | Orange: Funke erscheint, wächst, wandert nach links, „Claude" tippt sich |
| 4.167 – 4.783 | Navy mit Atmosphären-Schimmer |
| 4.783 – 5.400 | Cockpit-Fenster mit Erde (2 Frames nah, dann Totale) |
| 5.400 – 11.567 | Montage: Draht-Torus, Code, Sternen-Baum, Iso-Blöcke, Radial-Diagramm, Entscheidungsbaum, Merge-Pipeline, Regenbogenwelle, Pixel-Pyramide, Dashboard, Terminal, Gehirn-Punktwolke |
| 11.567 – 11.900 | Schwarz → Loop |
