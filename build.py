#!/usr/bin/env python3
"""Builds index.html for the portfolio.

Icons are inlined from Simple Icons path data (icons.json) so the page makes
zero external requests. Run:  python3 build.py
"""
from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ICONS = json.load(open(os.path.join(ROOT, "icons.json")))

# index.html links to css/style.css and js/main.js rather than inlining them, so you can
# edit either file and push straight to GitHub Pages -- no build step required.


def ic(slug: str, cls: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" '
            f'focusable="false"><path d="{ICONS[slug]["path"]}"/></svg>')


def chip(slug: str, label: str) -> str:
    return f'<span class="chip">{ic(slug)}{label}</span>'


def skill(slug: str, label: str, pct: int, delay: int) -> str:
    return (f'<div class="skill"><div class="row">'
            f'<span class="name">{ic(slug)}{label}</span>'
            f'<span class="pct">{pct}%</span></div>'
            f'<div class="bar"><i data-w="{pct}" data-delay="{delay}"></i></div></div>')


UI = {
    "brain": '<svg viewBox="0 0 24 24"><path d="M12 2a4 4 0 0 0-3.9 3.1A3.5 3.5 0 0 0 5 8.5c0 .6.15 1.17.42 1.67A3.75 3.75 0 0 0 4 13.5c0 1.2.56 2.27 1.44 2.96A3.5 3.5 0 0 0 9 22a3 3 0 0 0 2-3.2V5a3 3 0 0 0-1-3h2Zm2 0a3 3 0 0 0-1 3v13.8A3 3 0 0 0 15 22a3.5 3.5 0 0 0 3.56-5.54A3.75 3.75 0 0 0 20 13.5a3.75 3.75 0 0 0-1.42-2.83c.27-.5.42-1.07.42-1.67a3.5 3.5 0 0 0-3.1-3.4A4 4 0 0 0 14 2Z"/></svg>',
    "eye": '<svg viewBox="0 0 24 24"><path d="M12 5c-5.2 0-9.4 3.2-11 7 1.6 3.8 5.8 7 11 7s9.4-3.2 11-7c-1.6-3.8-5.8-7-11-7Zm0 11a4 4 0 1 1 0-8 4 4 0 0 1 0 8Zm0-2a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/></svg>',
    "chart": '<svg viewBox="0 0 24 24"><path d="M4 20V10h3v10H4Zm6.5 0V4h3v16h-3ZM17 20v-7h3v7h-3Z"/></svg>',
    "code": '<svg viewBox="0 0 24 24"><path d="m8.7 15.9-3.9-3.9 3.9-3.9-1.4-1.4L2 12l5.3 5.3 1.4-1.4Zm6.6 0 3.9-3.9-3.9-3.9 1.4-1.4L22 12l-5.3 5.3-1.4-1.4Z"/></svg>',
    "repo": '<svg viewBox="0 0 24 24"><path d="M4 3h9a3 3 0 0 1 3 3v13a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Zm1 2v11h9V6a1 1 0 0 0-1-1H5Zm11 2h2v12a2 2 0 0 1-2 2H5v-2h11V7Z"/></svg>',
    "star": '<svg viewBox="0 0 24 24"><path d="m12 2.6 2.9 5.9 6.5.9-4.7 4.6 1.1 6.5-5.8-3.1-5.8 3.1 1.1-6.5L2.6 9.4l6.5-.9L12 2.6Z"/></svg>',
    "flame": '<svg viewBox="0 0 24 24"><path d="M12 2s1 3-1 5.5C9 10 7 11.2 7 14a5 5 0 0 0 10 0c0-1.6-.7-2.8-1.5-3.7 0 1-.6 2-1.5 2.3.6-2.9-1-5.6-2-8.6Z"/></svg>',
    "book": '<svg viewBox="0 0 24 24"><path d="M4 3h7a3 3 0 0 1 3 3 3 3 0 0 1 3-3h7v15h-7a3 3 0 0 0-3 3 3 3 0 0 0-3-3H4V3Zm2 2v11h5a5 5 0 0 1 2 .4V6a1 1 0 0 0-1-1H6Zm12 0h-5a1 1 0 0 0-1 1v9.4a5 5 0 0 1 2-.4h5V5Z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg>',
    "cap": '<svg viewBox="0 0 24 24"><path d="M12 3 1 8.5 12 14l11-5.5L12 3Zm0 12.5L4.5 11.7 3 12.4v3.1L12 20l9-4.5v-3.1l-1.5-.7L12 15.5Z"/></svg>',
    "spark": '<svg viewBox="0 0 24 24"><path d="M12 2 9.5 9.5 2 12l7.5 2.5L12 22l2.5-7.5L22 12l-7.5-2.5L12 2Z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24"><path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Zm0 3.2V18h16V7.2l-8 5-8-5Zm1.6-1.2L12 10l6.4-4H5.6Z"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24"><path d="M5 12h11l-4-4 1.4-1.4L20 12l-6.6 5.4L12 16l4-4H5v-2Z"/></svg>',
    "ext": '<svg viewBox="0 0 24 24"><path d="M14 3h7v7h-2V6.4l-8.3 8.3-1.4-1.4L17.6 5H14V3ZM5 5h5v2H7v10h10v-3h2v5H5V5Z"/></svg>',
    "up": '<svg viewBox="0 0 24 24"><path d="M12 4 4 12h5v8h6v-8h5L12 4Z"/></svg>',
    "clock": '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm1 5v5.4l4 2.3-.9 1.6L11 13V7h2Z"/></svg>',
    "sun": '<svg viewBox="0 0 24 24"><path d="M7.8 12a4.2 4.2 0 1 0 8.4 0a4.2 4.2 0 1 0 -8.4 0 M18.40 12.90L21.20 12.90L21.20 11.10L18.40 11.10Z M15.89 17.16L17.87 19.14L19.14 17.87L17.16 15.89Z M11.10 18.40L11.10 21.20L12.90 21.20L12.90 18.40Z M6.84 15.89L4.86 17.87L6.13 19.14L8.11 17.16Z M5.60 11.10L2.80 11.10L2.80 12.90L5.60 12.90Z M8.11 6.84L6.13 4.86L4.86 6.13L6.84 8.11Z M12.90 5.60L12.90 2.80L11.10 2.80L11.10 5.60Z M17.16 8.11L19.14 6.13L17.87 4.86L15.89 6.84Z"/></svg>',
    "moon": '<svg viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',
}

# Every icon on this page is decorative, so screen readers should skip all of them.
UI = {k: v.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)
      for k, v in UI.items()}

# ------------------------------------------------------------------ content

FACTS = [
    ("pin", "Based in", "Dhaka, Bangladesh · UTC+6"),
    ("cap", "Studying", "CSE at East West University"),
    ("book", "CGPA", "3.95+ / 4.00"),
    ("star", "Merit Scholarship", "Top 10% of batch — full tuition waiver"),
    ("clock", "Teaching Assistant", "1+ year, undergraduate CSE courses"),
    ("brain", "Focus", "Deep learning, computer vision & explainable AI"),
]

STATS = [("13", "", "Public repositories", "repo"),
         ("6", "", "Featured projects", "star"),
         ("100", "+", "Days of ML / DL practice", "flame"),
         ("3", "", "Coursework repos published", "book")]

SKILL_CARDS = [
    ("brain", "Machine Learning", "Models, training and honest evaluation.",
     [("scikitlearn", "scikit-learn", 80), ("pytorch", "PyTorch", 62),
      ("tensorflow", "TensorFlow", 55), ("pandas", "pandas", 85)]),
    ("eye", "Vision & Data", "Image processing, analysis and dashboards.",
     [("opencv", "OpenCV", 68), ("numpy", "NumPy", 82), ("jupyter", "Jupyter", 90),
      ("streamlit", "Streamlit", 60)]),
    ("code", "Programming", "Languages I build with day to day.",
     [("python", "Python", 88), ("cplusplus", "C++", 65), ("openjdk", "Java", 58),
      ("javascript", "JavaScript", 52)]),
    ("chart", "Tools & Practice", "Version control, notebooks and problem solving.",
     [("git", "Git & GitHub", 80), ("googlecolab", "Colab", 88),
      ("kaggle", "Kaggle", 55), ("leetcode", "DSA practice", 70)]),
]

PROJECTS = [
    ("100-days-of-deep-learning", "100 Days of Deep Learning", "Deep Learning", "brain",
     "A 100-day deep learning journey — daily Colab notebooks covering architectures, "
     "training loops and hands-on experiments.",
     [("python", "Python"), ("googlecolab", "Colab"), ("jupyter", "Jupyter")]),
    ("100-days-of-machine-learning", "100 Days of Machine Learning", "Machine Learning", "spark",
     "Machine learning through theory, code and projects — one concept at a time, with "
     "practical implementations you can run.",
     [("python", "Python"), ("scikitlearn", "scikit-learn"), ("jupyter", "Jupyter")]),
    ("CSE438-Digital-Image-Processing", "Digital Image Processing", "Computer Vision", "eye",
     "Coursework for CSE438 — filtering, transforms and feature extraction implemented in "
     "Python, with reports and visualisations.",
     [("python", "Python"), ("opencv", "OpenCV"), ("jupyter", "Jupyter")]),
    ("CSE475-Machine-Learning", "Machine Learning Lab", "Coursework", "brain",
     "Lab work for CSE475 — supervised and unsupervised learning, ensemble methods, "
     "optimisation and neural networks.",
     [("python", "Python"), ("scikitlearn", "scikit-learn"), ("jupyter", "Jupyter")]),
    ("workload-and-mental-health-analysis-dashboard-using-stramlit",
     "Workload & Mental Health Dashboard", "Data Analysis", "chart",
     "An interactive Streamlit dashboard exploring workload and mental-health-related data "
     "through analysis and visualisation.",
     [("python", "Python"), ("streamlit", "Streamlit"), ("pandas", "pandas")]),
    ("loan_data_analysis", "Loan Data Analysis", "Data Analysis", "chart",
     "Exploratory analysis of loan data — distributions, risk patterns and the visualisations "
     "that make them readable.",
     [("python", "Python"), ("pandas", "pandas"), ("jupyter", "Jupyter")]),
]

JOURNEY = [
    ("Aug 2024", "Started the journey",
     "Began Computer Science & Engineering at East West University and opened my first "
     "GitHub account — the commit history starts here."),
    ("Dec 2025", "First end-to-end data project",
     "Built a Streamlit dashboard analysing workload and mental-health data: cleaning, "
     "exploration and interactive visualisation."),
    ("Jan 2026", "Exploratory analysis",
     "Loan data analysis — distributions, risk factors and the storytelling that turns "
     "a dataframe into a decision."),
    ("Apr 2026", "100 Days of Deep Learning",
     "Committed to a daily notebook habit: architectures, training loops, loss curves "
     "and the debugging that comes with them."),
    ("May 2026", "100 Days of Machine Learning",
     "Rebuilt the foundations properly — theory first, then code, then a project for "
     "every concept."),
    ("Jun 2026", "Coursework, published",
     "Opened up three course repos: CSE475 Machine Learning, CSE438 Digital Image "
     "Processing and CSE412 Software Engineering."),
    ("Jul 2026", "First portfolio site",
     "Designed and built my portfolio from scratch — no template."),
    ("Now", "What's next",
     "Deeper into deep learning: computer vision, explainable AI, and research I can "
     "actually contribute to."),
]

PAPER = {
    "venue": "5th IEEE BECITHCON 2026",
    "title": "Explainable Attention-Ensemble Framework for Multi-Magnification "
             "OSCC Histopathology Classification",
    "summary": "A benchmark of attention-augmented CNN architectures (CBAM, ECA, "
               "Self-Attention) and ensemble strategies for oral cancer histopathology "
               "classification, with Grad-CAM confirming the model attends to "
               "diagnostically relevant tissue rather than spurious patterns.",
    "metrics": [("94.31%", "Accuracy"), ("0.979", "AUC-ROC"),
                ("100%", "Sensitivity"), ("5-fold", "Cross-validated")],
}

CP_FACTS = [
    ("flame", "Problems solved", "650+ across Codeforces &amp; LeetCode"),
    ("star", "ICPC 2025", "Dhaka Regional participant"),
    ("cap", "Intra-University Contest", "5th place"),
]

COMPETITIONS = [
    ("chart", "bKash × NSU CEC Datathon", "Churn Prediction",
     "Built an end-to-end churn-prediction pipeline for a mobile wallet platform — "
     "big-data ingestion with Polars, engineered behavioural features, class-imbalance "
     "handling, Optuna-tuned LightGBM, and SHAP-based explainability.",
     "https://cybernauts.nsucec.com/"),
    ("brain", "অলীকবচন", "Bengali LLM Hallucination Detection",
     "A Kaggle competition predicting whether a Bengali LLM response is faithful or "
     "hallucinated, scored on F1 against a held-out leaderboard test set.",
     None),
]

SOCIALS = [
    ("github", "GitHub", "https://github.com/mahidrahman375"),
    ("linkedin", "LinkedIn", "https://linkedin.com/in/yeamin-rahman-mahid-957a551a9"),
    ("codeforces", "Codeforces", "https://codeforces.com/profile/yeaminmahid"),
    ("leetcode", "LeetCode", "https://leetcode.com/u/yeaminmahid/"),
]


def build() -> str:
    p: list[str] = []
    a = p.append

    a("<!DOCTYPE html>")
    a('<html lang="en">')
    a("<head>")
    a('<meta charset="utf-8"/>')
    a('<meta name="viewport" content="width=device-width,initial-scale=1"/>')
    a("<title>Yeamin Rahman Mahid — ML &amp; Data Science</title>")
    a('<meta name="description" content="CSE student at East West University working through '
      "machine learning, computer vision and data science — one notebook, dashboard and "
      'problem at a time."/>')
    a('<meta name="theme-color" content="#07070d"/>')
    a('<meta name="color-scheme" content="dark light"/>')
    # Sets data-theme before first paint so there is no flash of the wrong theme.
    # Reads a saved choice first, falls back to the OS preference, defaults to dark.
    a('<script>(function(){try{var t=localStorage.getItem("theme");'
      'if(!t){t=matchMedia("(prefers-color-scheme: light)").matches?"light":"dark";}'
      'if(t==="light")document.documentElement.setAttribute("data-theme","light");'
      '}catch(e){}})();</script>')
    a('<meta property="og:title" content="Yeamin Rahman Mahid — ML &amp; Data Science"/>')
    a('<meta property="og:description" content="Machine learning, computer vision and data '
      'science. CSE student at East West University, Dhaka."/>')
    a('<meta property="og:type" content="website"/>')
    a('<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' '
      "viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%236366f1'/%3E"
      "%3Ctext x='16' y='22' font-family='sans-serif' font-size='16' font-weight='700' "
      "fill='white' text-anchor='middle'%3EYM%3C/text%3E%3C/svg%3E\"/>")
    a('<link rel="stylesheet" href="css/style.css"/>')
    a("</head>")
    a("<body>")
    a('<div class="cursor-glow" aria-hidden="true"></div>')
    a('<div class="scroll-progress" aria-hidden="true"><i></i></div>')

    # ---- header
    a('<header class="site-header">')
    a('<div class="wrap"><nav class="nav">')
    a('<a class="brand" href="#home"><span class="mark">YM</span>Yeamin<span '
      'style="color:var(--dim);font-weight:500">.dev</span></a>')
    a('<button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false" '
      'aria-controls="nav"><span></span><span></span><span></span></button>')
    a('<div class="nav-links" id="nav">')
    for label, href in [("About", "#about"), ("Research", "#research"), ("Skills", "#skills"),
                        ("Projects", "#projects"), ("Journey", "#journey")]:
        a(f'<a href="{href}">{label}</a>')
    a('<a class="nav-cta" href="#contact">Get in touch</a>')
    a("</div>")
    a('<button class="theme-toggle" id="themeToggle" type="button" '
      'aria-label="Switch to light theme" aria-pressed="false">'
      f'<span class="ti ti-sun">{UI["sun"]}</span>'
      f'<span class="ti ti-moon">{UI["moon"]}</span></button>')
    a("</nav></div></header>")

    # ---- hero
    a('<main>')
    a('<section class="hero" id="home">')
    a('<div class="aurora" aria-hidden="true"><i></i><i></i><i></i></div>')
    a('<canvas id="net" aria-hidden="true"></canvas>')
    a('<div class="wrap">')
    a('<p class="eyebrow reveal"><span class="dot"></span>Open to internships &amp; '
      "research collaborations</p>")
    a('<h1 class="hero-title reveal" data-delay="80">Yeamin Rahman<br/>'
      '<span class="grad">Mahid</span></h1>')
    a('<p class="typed-line reveal" data-delay="140"><span id="typer"></span>'
      '<span class="caret" aria-hidden="true"></span></p>')
    a('<p class="hero-lead reveal" data-delay="200">CSE student at East West University, '
      "learning how intelligent systems actually work — machine learning, computer vision "
      "and the data work underneath them. I learn by building: notebooks, dashboards and "
      "small systems I can break and then explain.</p>")
    a('<div class="hero-actions reveal" data-delay="260">')
    a('<a class="btn btn-primary magnetic" href="#projects">View my work'
      f'{UI["arrow"]}</a>')
    a('<a class="btn btn-ghost magnetic" href="https://github.com/mahidrahman375" '
      f'target="_blank" rel="noopener">{ic("github")}GitHub</a>')
    a("</div>")
    a('<div class="hero-meta reveal" data-delay="320">')
    a(f'<span>{UI["cap"]}East West University</span>')
    a(f'<span>{UI["pin"]}Dhaka, Bangladesh</span>')
    a(f'<span>{UI["brain"]}ML · CV · Data Science</span>')
    a("</div></div>")
    a('<div class="scroll-hint" aria-hidden="true">Scroll<i></i></div>')
    a("</section>")

    # (tech list lives once, in the Skills section below — no marquee duplicate)

    # ---- about
    a('<section id="about">')
    a('<div class="wrap"><div class="sec-head reveal">')
    a('<span class="kicker">01 · About</span>')
    a('<h2 class="sec-title">Curious by default,<br/>rigorous on purpose.</h2>')
    a("</div>")
    a('<div class="about-grid">')
    a('<div class="about-copy reveal">')
    a("<p>I'm a <strong>Computer Science &amp; Engineering</strong> student who got hooked on "
      "machine learning the first time a model learned something I hadn't explicitly told it. "
      "Since then I've been chasing that feeling on purpose — through courses, notebooks and "
      "a hundred-day habit of shipping something small every day.</p>")
    a("<p>Most of my work lives in <strong>Python and Jupyter</strong>: data cleaning, feature "
      "engineering, model evaluation, and the visualisation that makes a result believable. "
      "Alongside that I do <strong>competitive programming</strong> on Codeforces and LeetCode, "
      "because fast, correct thinking about data structures is a skill you either practise or "
      "lose.</p>")
    a("<p>I publish my coursework rather than hiding it — <strong>CSE475 Machine Learning</strong>, "
      "<strong>CSE438 Digital Image Processing</strong> and <strong>CSE412 Software "
      "Engineering</strong> are all open. If something in there is wrong, open an issue; that's "
      "the fastest way I learn.</p>")
    a("</div>")
    a('<div class="facts reveal" data-delay="120">')
    for icon, k, v in FACTS:
        a(f'<div class="fact">{UI[icon]}<div><b>{k}</b><span>{v}</span></div></div>')
    a("</div></div>")

    # stats
    a('<div class="stats">')
    for i, (n, suffix, label, icon) in enumerate(STATS):
        a(f'<div class="stat reveal" data-delay="{i * 90}">'
          f'<div class="n" data-count="{n}" data-suffix="{suffix}">0</div>'
          f'<div class="l">{label}</div></div>')
    a("</div></div></section>")

    # ---- research (paper, competitive programming, competitions)
    a('<section id="research">')
    a('<div class="wrap"><div class="sec-head reveal">')
    a('<span class="kicker">02 · Research</span>')
    a('<h2 class="sec-title">Published work &amp; competitions.</h2>')
    a("</div>")

    a('<div class="paper reveal">')
    a(f'<span class="kicker">{UI["book"]}{PAPER["venue"]}</span>')
    a(f'<h3>{PAPER["title"]}</h3>')
    a(f'<p>{PAPER["summary"]}</p>')
    a('<div class="metrics">')
    for val, label in PAPER["metrics"]:
        a(f'<div class="metric"><b>{val}</b><span>{label}</span></div>')
    a("</div></div>")

    a('<div class="facts cp-facts reveal" data-delay="80">')
    for icon, k, v in CP_FACTS:
        a(f'<div class="fact">{UI[icon]}<div><b>{k}</b><span>{v}</span></div></div>')
    a("</div>")

    a('<div class="projects comp-grid">')
    for i, (icon, title, tag, desc, url) in enumerate(COMPETITIONS):
        a(f'<article class="card reveal tilt" data-delay="{i * 110}">')
        a(f'<div class="card-top"><span class="icon">{UI[icon]}</span>'
          f"<h3>{title}</h3><span class=\"tag\">{tag}</span></div>")
        a(f"<p>{desc}</p>")
        if url:
            a('<div class="card-links">')
            a(f'<a href="{url}" target="_blank" rel="noopener">{UI["ext"]}View competition</a>')
            a("</div>")
        a("</article>")
    a("</div></div></section>")

    # ---- skills
    a('<section id="skills">')
    a('<div class="wrap"><div class="sec-head reveal">')
    a('<span class="kicker">03 · Skills</span>')
    a('<h2 class="sec-title">What I build with.</h2>')
    a('<p class="sec-sub">Percentages are my own honest read on comfort level — not a '
      "certificate count.</p>")
    a("</div><div class=\"skills-grid\">")
    for i, (icon, title, sub, items) in enumerate(SKILL_CARDS):
        a(f'<div class="skill-card reveal tilt" data-delay="{i * 90}">')
        a(f"<h3>{UI[icon]}{title}</h3><p>{sub}</p>")
        for j, (slug, label, pct) in enumerate(items):
            a(skill(slug, label, pct, j * 110))
        a("</div>")
    a("</div></div></section>")

    # ---- projects
    a('<section id="projects">')
    a('<div class="wrap"><div class="sec-head reveal">')
    a('<span class="kicker">04 · Projects</span>')
    a('<h2 class="sec-title">Things I built and broke.</h2>')
    a('<p class="sec-sub">Real repositories — the code, notebooks and mistakes are all '
      "public.</p>")
    a("</div><div class=\"projects\">")
    for i, (repo, title, tag, icon, desc, stack) in enumerate(PROJECTS):
        a(f'<article class="card reveal tilt" data-delay="{(i % 3) * 110}">')
        a(f'<div class="card-top"><span class="icon">{UI[icon]}</span>'
          f"<h3>{title}</h3><span class=\"tag\">{tag}</span></div>")
        a(f"<p>{desc}</p>")
        a('<div class="chips">' + "".join(chip(s, l) for s, l in stack) + "</div>")
        a('<div class="card-links">')
        a(f'<a href="https://github.com/mahidrahman375/{repo}" target="_blank" '
          f'rel="noopener">{UI["repo"]}Source</a>')
        a(f'<a href="https://github.com/mahidrahman375/{repo}/commits" target="_blank" '
          f'rel="noopener">{UI["ext"]}History</a>')
        a("</div></article>")
    a("</div></div></section>")

    # ---- journey
    a('<section id="journey">')
    a('<div class="wrap"><div class="sec-head reveal">')
    a('<span class="kicker">05 · Journey</span>')
    a('<h2 class="sec-title">How the last two years went.</h2>')
    a("</div><div class=\"timeline\">")
    for i, (when, title, body) in enumerate(JOURNEY):
        a(f'<div class="tl reveal" data-delay="{i * 70}">'
          f'<div class="when">{when}</div><h3>{title}</h3><p>{body}</p></div>')
    a("</div></div></section>")

    # ---- contact
    a('<section id="contact">')
    a('<div class="wrap"><div class="contact-card reveal">')
    a(f'<span class="kicker" style="justify-content:center">{UI["mail"]}Contact</span>')
    a('<h2>Let\'s build something worth evaluating.</h2>')
    a("<p>I'm looking for internships, research collaborations and hard problems. If you're "
      "working on ML, vision or data — or you just want to argue about eval sets — say "
      "hello.</p>")
    a('<div class="socials">')
    for slug, label, url in SOCIALS:
        a(f'<a class="soc magnetic" href="{url}" target="_blank" rel="noopener">'
          f"{ic(slug)}{label}</a>")
    a("</div></div></div></section>")
    a("</main>")

    # ---- footer
    a('<footer class="site-footer"><div class="wrap"><div class="foot">')
    a('<div>© <span id="year">2026</span> Yeamin Rahman Mahid · Built from scratch, no '
      "template.</div>")
    a('<div class="sw">Palette '
      '<i style="background:#6366f1"></i><i style="background:#4f46e5"></i>'
      '<i style="background:#8b5cf6"></i><i style="background:#a5b4fc"></i></div>')
    a("</div></div></footer>")
    a(f'<a class="to-top" href="#home" aria-label="Back to top">{UI["up"]}</a>')
    a('<script src="js/main.js" defer></script>')
    a("</body></html>")
    return "\n".join(p)


if __name__ == "__main__":
    html = build()
    out = os.path.join(ROOT, "index.html")
    open(out, "w").write(html)
    print(f"index.html  {len(html):>7,} bytes  {html.count(chr(10)) + 1} lines")
