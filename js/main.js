/* ==========================================================================
   Yeamin Rahman Mahid — portfolio
   main.js · no dependencies, no external requests
   Every animation honours prefers-reduced-motion.
   ========================================================================== */
(function () {
  "use strict";

  var PHRASES = [
    "Machine Learning Enthusiast",
    "Data Science Explorer",
    "Competitive Programmer",
    "Aspiring ML Engineer"
  ];

  var REDUCED = false;

  /* ---------------------------------------------------------------- utils */
  function easeOutCubic(t) {
    t = t < 0 ? 0 : t > 1 ? 1 : t;
    return 1 - Math.pow(1 - t, 3);
  }

  function clamp(v, lo, hi) {
    return v < lo ? lo : v > hi ? hi : v;
  }

  function formatNumber(n) {
    n = Math.round(n);
    if (Math.abs(n) >= 1000) {
      return (n / 1000).toFixed(n % 1000 === 0 ? 0 : 1).replace(/\.0$/, "") + "k";
    }
    return String(n);
  }

  /* Seeded PRNG so the hero background is identical on every load. */
  function mulberry32(a) {
    return function () {
      a |= 0; a = a + 0x6d2b79f5 | 0;
      var t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  /* ------------------------------------------------------- hero network */
  function makeNodes(w, h, count, rnd) {
    var nodes = [], i;
    for (i = 0; i < count; i++) {
      nodes.push({
        x: rnd() * w,
        y: rnd() * h,
        vx: (rnd() - 0.5) * 0.22,
        vy: (rnd() - 0.5) * 0.22,
        r: 0.9 + rnd() * 1.5
      });
    }
    return nodes;
  }

  function linksFor(nodes, maxDist) {
    var out = [], i, j, dx, dy, d;
    for (i = 0; i < nodes.length; i++) {
      for (j = i + 1; j < nodes.length; j++) {
        dx = nodes[i].x - nodes[j].x;
        dy = nodes[i].y - nodes[j].y;
        d = Math.sqrt(dx * dx + dy * dy);
        if (d < maxDist) out.push([i, j, 1 - d / maxDist]);
      }
    }
    return out;
  }

  function stepNodes(nodes, w, h) {
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      n.x += n.vx; n.y += n.vy;
      if (n.x < -20) n.x = w + 20; else if (n.x > w + 20) n.x = -20;
      if (n.y < -20) n.y = h + 20; else if (n.y > h + 20) n.y = -20;
    }
  }

  /* ---------------------------------------------------------- typing */
  function typeLoop(el, phrases, opts) {
    opts = opts || {};
    var speed = opts.speed || 62, del = opts.del || 28;
    var hold = opts.hold || 1700, gap = opts.gap || 380;
    var i = 0, ch = 0, deleting = false, timer = null;

    function step() {
      var word = phrases[i % phrases.length];
      ch += deleting ? -1 : 1;
      el.textContent = word.slice(0, ch);
      var t;
      if (!deleting && ch === word.length) { t = hold; deleting = true; }
      else if (deleting && ch === 0) { deleting = false; i++; t = gap; }
      else { t = (deleting ? del : speed) + Math.random() * 34 - 17; }
      timer = setTimeout(step, t);
    }
    step();
    return {
      stop: function () { if (timer) clearTimeout(timer); },
      state: function () { return { phrase: i % phrases.length, chars: ch, deleting: deleting }; }
    };
  }

  /* ------------------------------------------------------- count up */
  function countUp(el, target, duration, raf, now) {
    raf = raf || window.requestAnimationFrame.bind(window);
    now = now || function () { return Date.now(); };
    duration = duration || 1400;
    var suffix = el.dataset.suffix || "";
    var start = now(), done = false;
    function frame() {
      var t = clamp((now() - start) / duration, 0, 1);
      var v = easeOutCubic(t) * target;
      el.textContent = formatNumber(v) + suffix;
      if (t < 1 && !done) raf(frame);
      else { el.textContent = formatNumber(target) + suffix; done = true; }
    }
    raf(frame);
  }

  /* ------------------------------------------------------- 3D tilt */
  function tilt(card, max) {
    max = max || 6;
    function move(e) {
      var r = card.getBoundingClientRect();
      var px = (e.clientX - r.left) / r.width - 0.5;
      var py = (e.clientY - r.top) / r.height - 0.5;
      card.style.transform =
        "perspective(900px) rotateX(" + (-py * max).toFixed(2) + "deg) rotateY(" +
        (px * max).toFixed(2) + "deg) translateY(-4px)";
      card.style.setProperty("--mx", ((px + 0.5) * 100).toFixed(1) + "%");
      card.style.setProperty("--my", ((py + 0.5) * 100).toFixed(1) + "%");
    }
    function leave() { card.style.transform = ""; }
    card.addEventListener("mousemove", move);
    card.addEventListener("mouseleave", leave);
    return { move: move, leave: leave };
  }

  /* ------------------------------------------------------ magnetic */
  function magnetic(el, strength) {
    strength = strength || 0.25;
    function move(e) {
      var r = el.getBoundingClientRect();
      var dx = (e.clientX - (r.left + r.width / 2)) * strength;
      var dy = (e.clientY - (r.top + r.height / 2)) * strength;
      el.style.transform = "translate(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px)";
    }
    function leave() { el.style.transform = ""; }
    el.addEventListener("mousemove", move);
    el.addEventListener("mouseleave", leave);
  }

  /* ================================================================== boot */
  function boot() {
    REDUCED = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    /* ---- theme toggle (dark / light) ---- */
    var root = document.documentElement;
    var themeBtn = document.getElementById("themeToggle");
    var THEME_KEY = "theme";

    function currentTheme() {
      return root.getAttribute("data-theme") === "light" ? "light" : "dark";
    }
    function applyTheme(t) {
      if (t === "light") root.setAttribute("data-theme", "light");
      else root.removeAttribute("data-theme");
      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta) meta.setAttribute("content", t === "light" ? "#f7f7fb" : "#07070d");
      if (themeBtn) {
        themeBtn.setAttribute("aria-pressed", t === "light" ? "true" : "false");
        themeBtn.setAttribute("aria-label", t === "light" ? "Switch to dark theme" : "Switch to light theme");
      }
    }
    if (themeBtn) {
      applyTheme(currentTheme()); // sync aria state with whatever the head script already set
      themeBtn.addEventListener("click", function () {
        var next = currentTheme() === "light" ? "dark" : "light";
        try { window.localStorage.setItem(THEME_KEY, next); } catch (e) { /* storage unavailable */ }
        applyTheme(next);
      });
    }

    /* ---- mobile nav ---- */
    var burger = document.querySelector(".nav-toggle");
    var menu = document.querySelector(".nav-links");
    if (burger && menu) {
      burger.addEventListener("click", function () {
        var open = document.body.classList.toggle("nav-open");
        burger.setAttribute("aria-expanded", open ? "true" : "false");
      });
      menu.addEventListener("click", function (e) {
        if (e.target.tagName === "A") {
          document.body.classList.remove("nav-open");
          burger.setAttribute("aria-expanded", "false");
        }
      });
    }

    /* ---- scroll progress + sticky nav ---- */
    var bar = document.querySelector(".scroll-progress i");
    var header = document.querySelector(".site-header");
    function onScroll() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var p = h > 0 ? clamp(window.scrollY / h, 0, 1) : 0;
      if (bar) bar.style.transform = "scaleX(" + p + ")";
      if (header) header.classList.toggle("stuck", window.scrollY > 24);
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    /* ---- hero typing ---- */
    var typer = document.getElementById("typer");
    if (typer) {
      if (REDUCED) typer.textContent = PHRASES[0];
      else typeLoop(typer, PHRASES, { speed: 60, del: 26, hold: 1700, gap: 360 });
    }

    /* ---- hero neural network ---- */
    var canvas = document.getElementById("net");
    if (canvas && canvas.getContext && !REDUCED) {
      var ctx = canvas.getContext("2d");
      var w = 0, h = 0, dpr = Math.min(window.devicePixelRatio || 1, 2);
      var nodes = [], mouse = { x: -9999, y: -9999 };
      var rnd = mulberry32(20260905);

      function resize() {
        w = canvas.clientWidth; h = canvas.clientHeight;
        canvas.width = w * dpr; canvas.height = h * dpr;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        var count = clamp(Math.round(w * h / 22000), 26, 70);
        nodes = makeNodes(w, h, count, rnd);
      }
      function draw() {
        ctx.clearRect(0, 0, w, h);
        stepNodes(nodes, w, h);
        var links = linksFor(nodes, 132);
        var i, l, a, b;
        ctx.lineWidth = 1;
        for (i = 0; i < links.length; i++) {
          l = links[i]; a = nodes[l[0]]; b = nodes[l[1]];
          ctx.strokeStyle = "rgba(129,140,248," + (l[2] * 0.34).toFixed(3) + ")";
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
        }
        for (i = 0; i < nodes.length; i++) {
          var n = nodes[i];
          var dxm = n.x - mouse.x, dym = n.y - mouse.y;
          var dm = Math.sqrt(dxm * dxm + dym * dym);
          var near = dm < 150 ? 1 - dm / 150 : 0;
          ctx.fillStyle = "rgba(165,180,252," + (0.35 + near * 0.55).toFixed(3) + ")";
          ctx.beginPath(); ctx.arc(n.x, n.y, n.r + near * 1.4, 0, 6.2832); ctx.fill();
          if (near > 0) {
            ctx.strokeStyle = "rgba(139,92,246," + (near * 0.5).toFixed(3) + ")";
            ctx.beginPath(); ctx.moveTo(n.x, n.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke();
          }
        }
        raf = window.requestAnimationFrame(draw);
      }
      var raf = null;
      resize();
      window.addEventListener("resize", resize);
      window.addEventListener("mousemove", function (e) {
        var r = canvas.getBoundingClientRect();
        mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
      });
      window.addEventListener("mouseout", function () { mouse.x = -9999; mouse.y = -9999; });
      document.addEventListener("visibilitychange", function () {
        if (document.hidden) { if (raf) window.cancelAnimationFrame(raf); raf = null; }
        else if (!raf) raf = window.requestAnimationFrame(draw);
      });
      raf = window.requestAnimationFrame(draw);
    }

    /* ---- reveal on scroll (staggered) ---- */
    var reveals = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window) || REDUCED) {
      for (var r0 = 0; r0 < reveals.length; r0++) reveals[r0].classList.add("in");
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          var el = en.target;
          var delay = parseInt(el.dataset.delay || "0", 10);
          setTimeout(function () { el.classList.add("in"); }, delay);
          io.unobserve(el);
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
      for (var r1 = 0; r1 < reveals.length; r1++) io.observe(reveals[r1]);
    }

    /* ---- skill bars ---- */
    var bars = document.querySelectorAll(".bar i");
    if ("IntersectionObserver" in window && !REDUCED) {
      var bio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          var el = en.target;
          setTimeout(function () { el.style.width = el.dataset.w + "%"; },
            parseInt(el.dataset.delay || "0", 10));
          bio.unobserve(el);
        });
      }, { threshold: 0.4 });
      for (var b = 0; b < bars.length; b++) bio.observe(bars[b]);
    } else {
      for (var b2 = 0; b2 < bars.length; b2++) bars[b2].style.width = bars[b2].dataset.w + "%";
    }

    /* ---- count-up stats ---- */
    var nums = document.querySelectorAll("[data-count]");
    function fire(n) { countUp(n, parseFloat(n.dataset.count), 1500); }
    if ("IntersectionObserver" in window && !REDUCED) {
      var nio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          fire(en.target); nio.unobserve(en.target);
        });
      }, { threshold: 0.6 });
      for (var n = 0; n < nums.length; n++) { nums[n].textContent = "0"; nio.observe(nums[n]); }
    } else {
      for (var n2 = 0; n2 < nums.length; n2++) {
        nums[n2].textContent = formatNumber(parseFloat(nums[n2].dataset.count)) +
          (nums[n2].dataset.suffix || "");
      }
    }

    /* ---- tilt + magnetic ---- */
    if (!REDUCED && window.matchMedia("(hover: hover)").matches) {
      var cards = document.querySelectorAll(".tilt");
      for (var c = 0; c < cards.length; c++) tilt(cards[c], 6);
      var mags = document.querySelectorAll(".magnetic");
      for (var m = 0; m < mags.length; m++) magnetic(mags[m], 0.22);
    }

    /* ---- active section in nav ---- */
    var links = document.querySelectorAll(".nav-links a[href^='#']");
    var sections = [];
    for (var s = 0; s < links.length; s++) {
      var sec = document.querySelector(links[s].getAttribute("href"));
      if (sec) sections.push({ link: links[s], sec: sec });
    }
    if (sections.length && "IntersectionObserver" in window) {
      var sio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          for (var k = 0; k < sections.length; k++) {
            sections[k].link.classList.toggle("active", sections[k].sec === en.target);
          }
        });
      }, { rootMargin: "-45% 0px -50% 0px" });
      for (var q = 0; q < sections.length; q++) sio.observe(sections[q].sec);
    }

    /* ---- cursor glow (pointer devices only) ---- */
    var glow = document.querySelector(".cursor-glow");
    if (glow && !REDUCED && window.matchMedia("(hover: hover)").matches) {
      document.addEventListener("mousemove", function (e) {
        glow.style.transform = "translate(" + e.clientX + "px," + e.clientY + "px)";
        glow.style.opacity = "1";
      });
    }

    /* ---- back to top ---- */
    var top = document.querySelector(".to-top");
    if (top) {
      window.addEventListener("scroll", function () {
        top.classList.toggle("show", window.scrollY > 700);
      }, { passive: true });
    }

    /* ---- footer year ---- */
    var yr = document.getElementById("year");
    if (yr) yr.textContent = String(new Date().getFullYear());
  }

  if (typeof document !== "undefined") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", boot);
    } else { boot(); }
  }

  /* exposed for tests */
  if (typeof module !== "undefined" && module.exports) {
    module.exports = {
      easeOutCubic: easeOutCubic, clamp: clamp, formatNumber: formatNumber,
      mulberry32: mulberry32, makeNodes: makeNodes, linksFor: linksFor,
      stepNodes: stepNodes, typeLoop: typeLoop, countUp: countUp,
      tilt: tilt, magnetic: magnetic, boot: boot, PHRASES: PHRASES
    };
    // theme helpers are attached at call time inside boot(); exported for completeness
    module.exports.THEME_KEY = "theme";
  }
})();
