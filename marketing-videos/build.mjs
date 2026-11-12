// Baut die fünf Reel-Kompositionen aus src/*.html + gemeinsamen Marken-Bausteinen.
//   node build.mjs            -> schreibt reels/<name>/index.html (je ein HyperFrames-Projekt)
// Rendern:  npx hyperframes render reels/01-die-linie -o renders/01-die-linie.mp4
import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync, symlinkSync } from "node:fs";

const brandCss = readFileSync("src/_brand.css", "utf8");

const head = (title) => `<!doctype html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>${title}</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
${brandCss}
    </style>`;

// Dauerhaftes Marken-Signet oben links (innerhalb der Safe-Zone, y > 168 px)
const bug = (a, d) => `
      <div id="bug" class="clip bug" data-start="${a}" data-duration="${d}" data-track-index="8">
        <div class="bug-in" id="bug-in">
          <svg class="bug-mark" viewBox="0 0 48 48"><path d="M24 4C24 4 9 21 9 31a15 15 0 0 0 30 0C39 21 24 4 24 4Z" fill="#18C8FF"/><path d="M15 33h18M18 27h12" stroke="#06192B" stroke-width="3.4" stroke-linecap="round"/></svg>
          <span class="bug-w">AQUAFORCE<b>NORD</b></span>
        </div>
      </div>`;

// Gemeinsame Endkarte (3,4 s): Wasser-Wisch -> Wortmarke -> CTA
const endcard = (a) => `
      <div id="end" class="clip end" data-start="${a}" data-duration="3.4" data-track-index="9">
        <div class="end-bg" id="end-bg"></div>
        <div class="end-sweep" id="end-sweep" data-layout-ignore></div>
        <div class="end-stack">
          <svg class="end-mark" id="end-mark" viewBox="0 0 48 48"><path d="M24 4C24 4 9 21 9 31a15 15 0 0 0 30 0C39 21 24 4 24 4Z" fill="#18C8FF"/><path d="M15 33h18M18 27h12" stroke="#06192B" stroke-width="3.4" stroke-linecap="round"/></svg>
          <div class="end-word"><span class="end-clip"><span id="end-w1">AQUAFORCE</span></span></div>
          <div class="end-nord"><i id="end-l1"></i><span id="end-w2">NORD</span><i id="end-l2"></i></div>
          <div class="end-sub" id="end-sub">Professionelle Hochdruckreinigung</div>
          <div class="end-cta" id="end-cta"><span>Jetzt Angebot anfragen</span><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="#06192B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div class="end-note" id="end-note">Terrassen · Einfahrten · Gehwege</div>
        </div>
      </div>`;

const endTl = (a) => `
      // ---- Endkarte
      tl.fromTo("#end-bg", { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }, ${a});
      tl.fromTo("#end-sweep", { y: 0 }, { y: -2400, duration: 0.5, ease: "power3.inOut" }, ${a});
      tl.fromTo("#end-mark", { opacity: 0, scale: 0.4, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.6, ease: "back.out(1.6)" }, ${a} + 0.34);
      tl.fromTo("#end-w1", { yPercent: 105 }, { yPercent: 0, duration: 0.6, ease: "expo.out" }, ${a} + 0.42);
      tl.fromTo("#end-w2", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.7, ease: "power3.out" }, ${a} + 0.62);
      tl.fromTo(["#end-l1", "#end-l2"], { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.out" }, ${a} + 0.62);
      tl.fromTo("#end-sub", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, ${a} + 0.9);
      tl.fromTo("#end-cta", { opacity: 0, y: 34, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "back.out(1.5)" }, ${a} + 1.15);
      tl.fromTo("#end-note", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, ${a} + 1.45);`;

const helpers = `
      const tl = gsap.timeline({ paused: true });
      const up = (sel, t, st = 0.07) => tl.fromTo(sel, { yPercent: 112 }, { yPercent: 0, duration: 0.55, ease: "expo.out", stagger: st }, t);
      const out = (sel, t) => tl.to(sel, { yPercent: -112, duration: 0.28, ease: "power3.in", stagger: 0.04 }, t);
      const pop = (sel, t, dx = -24) => { tl.fromTo(sel, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t); tl.fromTo(sel + "-in", { x: dx }, { x: 0, duration: 0.45, ease: "power3.out" }, t); };
      const hide = (sel, t) => tl.to(sel, { opacity: 0, duration: 0.2, ease: "power2.in" }, t);
      // Wasser-Wisch: Shot wird von rechts nach links freigelegt, eine Aqua-Kante läuft mit
      const sweep = (shot, edge, t, d = 0.55) => {
        tl.fromTo(shot, { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: d, ease: "power2.inOut" }, t);
        tl.fromTo(edge, { x: 1080, opacity: 1 }, { x: -40, opacity: 1, duration: d, ease: "power2.inOut" }, t);
        tl.set(edge, { opacity: 0 }, t + d);
      };`;

for (const f of readdirSync("src").filter((f) => /^\d\d-.*\.html$/.test(f))) {
  let s = readFileSync(`src/${f}`, "utf8");
  s = s
    .replace(/\{\{HEAD (.*?)\}\}/, (_, t) => head(t))
    .replace("{{HELPERS}}", helpers)
    .replace(/\{\{BUG ([\d.]+) ([\d.]+)\}\}/, (_, a, d) => bug(a, d))
    .replace(/\{\{ENDCARD ([\d.]+)\}\}/, (_, a) => endcard(a))
    .replace(/\{\{ENDTL ([\d.]+)\}\}/, (_, a) => endTl(a));
  const dir = `reels/${f.replace(".html", "")}`;
  mkdirSync(dir, { recursive: true });
  if (!existsSync(`${dir}/assets`)) symlinkSync("../../assets", `${dir}/assets`);
  writeFileSync(`${dir}/meta.json`, JSON.stringify({ id: f.replace(".html", ""), name: "AquaForce-Nord " + f.replace(".html", "") }));
  writeFileSync(`${dir}/index.html`, s);
  console.log("built", f);
}
