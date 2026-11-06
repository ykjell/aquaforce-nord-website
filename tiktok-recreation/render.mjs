// Rendert index.html Frame für Frame zu einem MP4 (1080x1920).
//
//   node render.mjs                       → know-your-limits.mp4 (11,9-s-Loop, 30 fps, ohne Ton)
//   node render.mjs --fps 60              → 60 fps
//   node render.mjs --audio song.m4a      → Tonspur dazumischen
//   node render.mjs --out mein.mp4
//
// Voraussetzungen: Node 18+, playwright, ffmpeg im PATH.
import { createRequire } from 'node:module';
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';

const { chromium } = createRequire(import.meta.url)('playwright');

const args = process.argv.slice(2);
const opt = (name, def) => { const i = args.indexOf(`--${name}`); return i >= 0 ? args[i + 1] : def; };
const fps = Number(opt('fps', 30));
const audio = opt('audio', null);
const here = dirname(fileURLToPath(import.meta.url));
const out = resolve(opt('out', join(here, 'know-your-limits.mp4')));

const dir = mkdtempSync(join(tmpdir(), 'kyl-frames-'));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto(pathToFileURL(join(here, 'index.html')).href + '?export');
await page.evaluate(() => window.ready);
const seconds = Number(opt('seconds', await page.evaluate(() => window.LOOP)));

const total = Math.round(seconds * fps);
for (let f = 0; f < total; f++) {
  const data = await page.evaluate(t => { window.render(t); return document.getElementById('c').toDataURL('image/png'); }, f / fps);
  writeFileSync(join(dir, `f${String(f).padStart(5, '0')}.png`), Buffer.from(data.split(',')[1], 'base64'));
  if (f % fps === 0) process.stdout.write(`\r${f}/${total}`);
}
await browser.close();
console.log(`\r${total}/${total} Frames gerendert`);

const ff = ['-y', '-v', 'error', '-framerate', String(fps), '-i', join(dir, 'f%05d.png')];
if (audio) ff.push('-i', audio, '-map', '0:v', '-map', '1:a', '-shortest', '-c:a', 'aac', '-b:a', '192k');
// BT.709 explizit setzen, sonst verschieben Player die Farben (z. B. das Orange)
ff.push('-vf', 'scale=out_color_matrix=bt709:out_range=tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv');
ff.push('-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', out);
execFileSync('ffmpeg', ff, { stdio: 'inherit' });
rmSync(dir, { recursive: true, force: true });
console.log('Fertig:', out);
