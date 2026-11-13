// node thumbnails/render.mjs  -> thumbnails/<name>.jpg (1080x1920)
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)("playwright");
import { readdirSync } from "node:fs";
import { resolve } from "node:path";
const dir = resolve("thumbnails");
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
for (const f of readdirSync(dir).filter((f) => f.endsWith(".html"))) {
  await p.goto("file://" + resolve(dir, f));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({ path: resolve(dir, f.replace(".html", ".jpg")), type: "jpeg", quality: 92 });
  console.log("ok", f);
}
await b.close();
