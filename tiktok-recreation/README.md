# „Know your limits." – TikTok-Edit-Nachbau

Nachbau des TikTok-Edits (iMessage-Chat → Claude-Logo → Montage) komplett in Code:
ein `<canvas>` (1080×1920, 9:16), alle Szenen prozedural gezeichnet, 12-Sekunden-Loop.

## Ansehen

`index.html` im Browser öffnen. Klick / Leertaste = Pause, Regler = Spulen.

## Als MP4 exportieren

```bash
npm i playwright && npx playwright install chromium   # einmalig
node render.mjs                     # → know-your-limits.mp4 (30 fps, ohne Ton)
node render.mjs --fps 60
node render.mjs --audio song.m4a    # eigene Tonspur dazumischen
```

## Timeline (Sekunden, Schnitte im 0,5-s-Takt ≈ 120 BPM)

| Zeit | Szene |
|---|---|
| 0.0 – 3.0 | iMessage-Chat „Do you love me? / Yeah / More than Claude? / Know your limits." – 6 harte Zoom-Schnitte |
| 3.0 – 4.25 | Orange Fläche, Funke wächst, Wortmarke „Claude" wird aufgedeckt |
| 4.25 – 4.75 | Navy mit Horizont-Schimmer |
| 4.75 – 5.5 | Cockpit-Fenster mit Erde, Zoom-Out |
| 5.5 – 11.625 | Montage: Draht-Torus, Glitch-Code, Sternen-Baum, isometrische Blöcke, Radial-Diagramm, Entscheidungsbaum, Pipeline, Regenbogenwelle, Pixel-Pyramide, Dashboard, Terminal, Gehirn-Punktwolke |
| 11.625 – 12.0 | Schwarz → Loop |

Die Abstände und Zoomstufen des Chats (`CHAT_KEYS`) und die Farben
(`#232029`, `#0a7afe`, `#ff784e`, `#12131b`) wurden direkt aus dem Original-Video abgemessen.
