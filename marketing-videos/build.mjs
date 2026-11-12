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

// Markendaten: hier zentral ändern, gilt für alle fünf Reels
const BRAND = {
  phone: "+49 176 438 57587",
  web: "www.aquaforce-nord.de",
  mail: "info@aquaforce-nord.de",
  price: "2,49",
};
const END_DUR = 4.6;

// Dauerhaftes Logo oben rechts (innerhalb der Safe-Zone, y > 168 px)
const bug = (a, d) => `
      <div id="bug" class="clip bug" data-start="${a}" data-duration="${d}" data-track-index="8">
        <img class="bug-logo" id="bug-in" src="assets/img/logo_sticker.png" alt="AquaForce-Nord" />
      </div>`;

// Gemeinsame Endkarte: Wasser-Wisch -> Logo -> Preisangebot -> CTA -> Kontakt
const endcard = (a) => `
      <div id="end" class="clip end" data-start="${a}" data-duration="${END_DUR}" data-track-index="9">
        <div class="end-bg" id="end-bg"></div>
        <div class="end-sweep" id="end-sweep" data-layout-ignore></div>
        <div class="end-stack">
          <img class="end-logo" id="end-logo" src="assets/img/logo_sticker.png" alt="AquaForce-Nord" />
          <div class="end-kicker" id="end-kicker"><i id="end-l1"></i><span>Pflasterreinigung vom Profi</span><i id="end-l2"></i></div>
          <div class="end-price" id="end-price"><span class="ab">schon ab</span><span class="eur">${BRAND.price}&nbsp;€</span><span class="qm">pro m²</span></div>
          <div class="end-cta" id="end-cta"><span>Jetzt Angebot sichern</span><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="#06192B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div class="end-contact" id="end-c1">${BRAND.phone}</div>
          <div class="end-web" id="end-c2">${BRAND.web}</div>
        </div>
      </div>`;

const endTl = (a) => `
      // ---- Endkarte
      tl.fromTo("#end-bg", { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }, ${a});
      tl.fromTo("#end-sweep", { y: 0 }, { y: -2400, duration: 0.5, ease: "power3.inOut" }, ${a});
      tl.fromTo("#end-logo", { opacity: 0, scale: 0.72, y: 40 }, { opacity: 1, scale: 1, y: 0, duration: 0.7, ease: "back.out(1.4)" }, ${a} + 0.34);
      tl.fromTo("#end-kicker", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, ${a} + 0.8);
      tl.fromTo(["#end-l1", "#end-l2"], { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.out" }, ${a} + 0.8);
      tl.fromTo("#end-price", { opacity: 0, scale: 1.18 }, { opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }, ${a} + 1.0);
      tl.fromTo("#end-cta", { opacity: 0, y: 34, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "back.out(1.5)" }, ${a} + 1.4);
      tl.fromTo(["#end-c1", "#end-c2"], { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out", stagger: 0.12 }, ${a} + 1.75);`;

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
