// Rendert index.html Frame für Frame zu einem MP4 (1080×1920, 30 fps, H.264 + AAC).
//
//   node render.mjs                         → aquaforce-nord-werbespot.mp4 (mit soundtrack.wav)
//   node render.mjs --no-audio              → ohne Ton
//   node render.mjs --overlay               → nur Schrift + Logo mit Alpha (ProRes 4444 .mov)
//   node render.mjs --stills 2,7,12,19,27   → Einzelbilder als PNG (Kontrolle)
//   node render.mjs --safe                  → Safe-Zone-Raster einblenden
//
// Voraussetzungen: Node 18+, playwright (Chromium), ffmpeg im PATH.
// Für die Tonspur vorher: python3 audio.py  → soundtrack.wav
import { createRequire } from 'node:module';
import { existsSync, writeFileSync, readFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { extname, normalize } from 'node:path';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';

const { chromium } = createRequire(import.meta.url)('playwright');
const args = process.argv.slice(2);
const has = n => args.includes(`--${n}`);
const opt = (n, d) => { const i = args.indexOf(`--${n}`); return i >= 0 ? args[i + 1] : d; };
const here = dirname(fileURLToPath(import.meta.url));
const overlay = has('overlay');
const stills = opt('stills', null);
const out = resolve(opt('out', join(here, overlay ? 'aquaforce-nord-overlay.mov' : 'aquaforce-nord-werbespot.mp4')));
const audio = has('no-audio') || overlay ? null : resolve(opt('audio', join(here, 'soundtrack.wav')));

// Kleiner HTTP-Server: per file:// geladene Bilder (Logo) würden den Canvas-Export sperren
const MIME = { '.html': 'text/html', '.png': 'image/png', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.wav': 'audio/wav' };
const server = createServer((req, res) => {
  const f = join(here, normalize(decodeURIComponent(req.url.split('?')[0])).replace(/^([/\\]|\.\.)+/, '') || 'index.html');
  if (!f.startsWith(here) || !existsSync(f)) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'Content-Type': MIME[extname(f)] || 'application/octet-stream' }); res.end(readFileSync(f));
}).listen(0, '127.0.0.1');
await new Promise(r => server.once('listening', r));
const base = `http://127.0.0.1:${server.address().port}/`;

const browser = await chromium.launch({ args: ['--disable-gpu-vsync', '--force-color-profile=srgb'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
page.on('console', m => { if (m.type() === 'error') console.error('[page]', m.text()); });
const q = ['export', overlay && 'layer=overlay', has('safe') && 'safe'].filter(Boolean).join('&');
await page.goto(base + 'index.html?' + q);
console.log('Texturen werden berechnet …');
await page.evaluate(() => window.ready);
const fps = Number(opt('fps', await page.evaluate(() => window.FPS)));
const seconds = Number(opt('seconds', await page.evaluate(() => window.DUR)));

const grab = t => page.evaluate(t => { window.render(t); return document.getElementById('c').toDataURL('image/png'); }, t)
  .then(d => Buffer.from(d.split(',')[1], 'base64'));

if (stills) {
  for (const s of stills.split(',').map(Number)) {
    const f = join(here, `still-${String(s).replace('.', '_')}.png`);
    writeFileSync(f, await grab(s)); console.log(f);
  }
  await browser.close(); server.close(); process.exit(0);
}

const ff = ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-'];
if (audio && existsSync(audio)) ff.push('-i', audio, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-shortest');
else if (audio) console.warn('Keine Tonspur gefunden (python3 audio.py) – rendere ohne Ton.');
if (overlay) ff.push('-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le');
else ff.push('-vf', 'scale=out_color_matrix=bt709:out_range=tv', '-colorspace', 'bt709', '-color_primaries', 'bt709',
  '-color_trc', 'bt709', '-color_range', 'tv', '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
  '-crf', '16', '-preset', 'slow', '-tune', 'film', '-g', String(fps), '-movflags', '+faststart');
ff.push(out);
const proc = spawn('ffmpeg', ff, { stdio: ['pipe', 'inherit', 'inherit'] });
const done = new Promise((res, rej) => proc.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));

const total = Math.round(seconds * fps), start = Date.now();
for (let f = 0; f < total; f++) {
  const png = await grab(f / fps);
  if (!proc.stdin.write(png)) await new Promise(r => proc.stdin.once('drain', r));
  if (f % fps === 0) process.stdout.write(`\r${f}/${total} Frames · ${((Date.now() - start) / 1000).toFixed(0)} s`);
}
proc.stdin.end();
await done;
await browser.close();
server.close();
console.log(`\r${total}/${total} Frames gerendert → ${out}`);
