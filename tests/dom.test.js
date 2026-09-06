/* Boots the real index.html + js/main.js inside a DOM and asserts the page
   actually initialises: reveals fire, bars fill, counters land on their final
   value, the typing loop runs, the theme toggle works, and every in-page
   anchor resolves.                                                     */
const fs = require("fs");
const path = require("path");
const assert = require("node:assert");
const { JSDOM, VirtualConsole } = require("jsdom");

const ROOT = path.join(__dirname, "..");
const html = fs.readFileSync(path.join(ROOT, "index.html"), "utf8");
const js = fs.readFileSync(path.join(ROOT, "js", "main.js"), "utf8");
const css = fs.readFileSync(path.join(ROOT, "css", "style.css"), "utf8");

const REDUCED = process.argv.includes("--reduced");
const errors = [];
const vc = new VirtualConsole();
vc.on("jsdomError", (e) => errors.push("jsdomError: " + e.message));
vc.on("error", (...a) => errors.push("console.error: " + a.join(" ")));

const dom = new JSDOM(html, {
  runScripts: "outside-only",
  pretendToBeVisual: true,
  url: "http://localhost/",
  virtualConsole: vc
});
const { window } = dom;
const doc = window.document;

/* ---- browser shims jsdom does not provide ---- */
window.matchMedia = (q) => ({
  matches: REDUCED ? /reduce/.test(q) : false, media: q, onchange: null,
  addEventListener() {}, removeEventListener() {},
  addListener() {}, removeListener() {}
});

const observed = [];
window.IntersectionObserver = class {
  constructor(cb) { this.cb = cb; observed.push(this); }
  observe(el) {
    // fire immediately, like an element already in the viewport
    this.cb([{ isIntersecting: true, target: el }], this);
  }
  unobserve() {}
  disconnect() {}
};

const ctxStub = new Proxy({}, {
  get: (t, k) => (k === "canvas" ? {} : () => {})
});
window.HTMLCanvasElement.prototype.getContext = () => ctxStub;

/* ---- run the site's own script ---- */
window.eval(js);

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

(async function run() {
  await wait(2200); // let the typing loop and the rAF count-up finish

  const q = (s) => doc.querySelector(s);
  const qa = (s) => Array.from(doc.querySelectorAll(s));

  /* ---- structure ---- */
  console.log("== structure ==");
  const counts = {
    "project cards": qa(".card").length,
    "skill cards": qa(".skill-card").length,
    "skill bars": qa(".bar i").length,
    "timeline items": qa(".tl").length,
    "stat tiles": qa(".stat").length,
    "inline <svg>": qa("svg").length,
    "social links": qa(".soc").length,
    "facts": qa(".fact").length
  };
  for (const [k, v] of Object.entries(counts)) console.log("  " + k.padEnd(16), v);
  // .card is shared by project repos (6) and the two competition entries in
  // the Research section (2) — same visual language, different content.
  assert.strictEqual(counts["project cards"], 8, "6 project cards + 2 competition cards");
  assert.strictEqual(counts["skill cards"], 4, "4 skill cards");
  assert.strictEqual(counts["timeline items"], 8, "8 timeline entries");
  assert.strictEqual(counts["stat tiles"], 4, "4 stat tiles");
  assert.strictEqual(counts["social links"], 4, "4 social links");
  assert.ok(counts["skill bars"] >= 16, "at least 16 skill bars");
  // +2 vs the earlier baseline: the theme-toggle's sun/moon icons are always
  // in the DOM (CSS just switches which one is visible), in both motion modes.
  // The marquee (a duplicate of the Skills tech list) was removed entirely.
  assert.strictEqual(counts["inline <svg>"], 82, "icons are inlined, not fetched");

  /* ---- no page errors ---- */
  console.log("\n== runtime ==");
  console.log("  console/jsdom errors:", errors.length ? errors : "none");
  assert.deepStrictEqual(errors, [], "page initialises without errors");

  /* ---- typing loop ran ---- */
  const typed = q("#typer").textContent;
  console.log('  #typer text:', JSON.stringify(typed));
  assert.ok(typed.length > 0, "typing loop produced text");
  assert.ok(js.includes("PHRASES"), "phrases defined in shipped JS");

  /* ---- reveals fired ---- */
  const reveals = qa(".reveal");
  const shown = reveals.filter((e) => e.classList.contains("in")).length;
  console.log(`  reveals shown: ${shown}/${reveals.length}`);
  assert.strictEqual(shown, reveals.length, "every reveal element was activated");

  /* ---- skill bars filled ---- */
  const filled = qa(".bar i").filter((e) => e.style.width && e.style.width !== "0%").length;
  console.log(`  skill bars filled: ${filled}/${qa(".bar i").length}`);
  assert.strictEqual(filled, qa(".bar i").length, "every skill bar got a width");

  /* ---- count-up landed on final values ---- */
  const nums = qa("[data-count]").map((e) => e.textContent);
  console.log("  counters:", nums.join(" | "));
  assert.deepStrictEqual(nums, ["13", "6", "100+", "3"], "counters reached final values");

  /* ---- theme toggle ---- */
  console.log("\n== theme toggle ==");
  const themeBtn = q("#themeToggle");
  assert.ok(themeBtn, "theme toggle button exists");
  assert.strictEqual(doc.documentElement.hasAttribute("data-theme"), false,
    "defaults to dark (no data-theme attribute)");
  assert.strictEqual(themeBtn.getAttribute("aria-pressed"), "false", "starts aria-pressed=false");
  console.log("  initial aria-label:", themeBtn.getAttribute("aria-label"));

  themeBtn.click();
  assert.strictEqual(doc.documentElement.getAttribute("data-theme"), "light",
    "click switches to light theme");
  assert.strictEqual(themeBtn.getAttribute("aria-pressed"), "true", "aria-pressed flips to true");
  assert.strictEqual(window.localStorage.getItem("theme"), "light", "choice persisted to localStorage");
  console.log("  after 1 click -> data-theme:", doc.documentElement.getAttribute("data-theme"));

  themeBtn.click();
  assert.strictEqual(doc.documentElement.hasAttribute("data-theme"), false,
    "click again switches back to dark");
  assert.strictEqual(window.localStorage.getItem("theme"), "dark", "dark choice persisted too");
  console.log("  after 2nd click -> data-theme:", doc.documentElement.getAttribute("data-theme") || "(dark)");

  /* ---- research content present ---- */
  console.log("\n== research ==");
  assert.ok(q(".paper"), "featured paper card present");
  assert.strictEqual(qa(".paper .metric").length, 4, "4 paper metrics");
  assert.strictEqual(qa(".cp-facts .fact").length, 3, "3 competitive-programming facts");
  assert.strictEqual(qa(".comp-grid .card").length, 2, "2 competition cards");

  /* ---- footer year ---- */
  const yr = q("#year").textContent;
  console.log("  footer year:", yr);
  assert.strictEqual(yr, String(new Date().getFullYear()), "footer year is current");

  /* ---- nav integrity: every in-page anchor resolves ---- */
  console.log("\n== links ==");
  const anchors = qa("a[href^='#']").map((a) => a.getAttribute("href"));
  const broken = anchors.filter((h) => h !== "#" && !doc.querySelector(h));
  console.log("  in-page anchors:", anchors.join(" "));
  assert.deepStrictEqual(broken, [], "no broken in-page anchors");
  for (const id of ["#about", "#skills", "#projects", "#journey", "#contact", "#home"]) {
    assert.ok(anchors.includes(id), `nav links to ${id}`);
  }
  const external = qa("a[target='_blank']").map((a) => a.href);
  console.log("  external links:", external.length);
  assert.ok(external.every((h) => /^https:\/\/(github\.com|linkedin\.com|codeforces\.com|leetcode\.com|cybernauts\.nsucec\.com)/.test(h)),
    "external links point where expected");
  for (const a of qa("a[target='_blank']")) {
    assert.match(a.getAttribute("rel") || "", /noopener/, "external links use rel=noopener");
  }

  /* ---- no runtime asset fetching ---- */
  console.log("\n== self-containment ==");
  const extCss = qa("link[rel='stylesheet']").map((l) => l.getAttribute("href"));
  const extJs = qa("script[src]").map((s) => s.getAttribute("src"));
  console.log("  stylesheets:", extCss, "scripts:", extJs);
  assert.ok(extCss.every((h) => !/^https?:/.test(h)), "no remote stylesheets");
  assert.ok(extJs.every((h) => !/^https?:/.test(h)), "no remote scripts");
  assert.strictEqual(qa("img").length, 0, "no <img> fetches — icons are inline SVG");
  console.log("  css bytes:", css.length, "| js bytes:", js.length);
  assert.ok(css.includes("prefers-reduced-motion"), "CSS honours reduced motion");
  assert.ok(js.includes("prefers-reduced-motion"), "JS honours reduced motion");

  /* ---- a11y basics ---- */
  console.log("\n== a11y ==");
  assert.ok(q("html").getAttribute("lang"), "html has lang");
  assert.ok(q("meta[name='viewport']"), "viewport meta present");
  assert.ok(q(".nav-toggle").getAttribute("aria-label"), "menu button labelled");
  assert.strictEqual(qa("svg[aria-hidden='true']").length, qa("svg").length,
    "decorative SVGs are aria-hidden");
  console.log("  headings:", qa("h1").length, "h1 /", qa("h2").length, "h2 /", qa("h3").length, "h3");
  assert.strictEqual(qa("h1").length, 1, "exactly one h1");

  /* ---- reduced-motion path ---- */
  if (REDUCED) {
    console.log("\n== prefers-reduced-motion ==");
    assert.strictEqual(q("#typer").textContent, "Machine Learning Enthusiast",
      "typing replaced by static first phrase");
    const net = q("#net");
    console.log("  canvas untouched (width):", net.width);
    assert.strictEqual(net.width, 300, "canvas never initialised");
    console.log("  counters static:", qa("[data-count]").map((e) => e.textContent).join(" | "));
    console.log("  reduced-motion path verified");
  }

  console.log("\nAll DOM assertions passed.");
  dom.window.close();
  process.exit(0);
})().catch((e) => { console.error("\nFAILED:", e.message); process.exit(1); });
