# 🚀 SJ88 Mission Control

> **Live interactive dashboard of all 59 GitHub repositories shipped by Mavis (lnwsj)**
> Built as a single-file vanilla HTML+CSS+JS app. No build step. No dependencies. Just open and explore.

🌐 **Live demo (production)**: [https://git88.sj88ai.com/](https://git88.sj88ai.com/) (🔒 Let's Encrypt SSL)
🪞 **GitHub Pages mirror**: [https://lnwsj.github.io/sj88-mission-control/](https://lnwsj.github.io/sj88-mission-control/)
📦 **Source**: [https://github.com/lnwsj/sj88-mission-control](https://github.com/lnwsj/sj88-mission-control)

---

## 🎯 What is this?

This is **Mission Control** for the Mavis ship — a NASA-style command center that visualizes every repo `lnwsj` has published on GitHub. Click any card to drill in. Filter by category. Search by name. Toggle between Grid / Timeline / Category views.

It's a **single-file** dashboard — `index.html` is 63 KB. Open it directly in any modern browser or serve it via `python3 -m http.server`.

## ✨ Features

- 🎨 **Kawaii-pink + indigo gradient design** with floating animated orbs
- 📊 **6 animated stat cards** — total repos, live deployments, recent ship count, categories, total code, days active
- 🔍 **Real-time search** across all 59 repos
- 🏷️ **10 category filters** + "All" — 3D Games, 2D Games, Booking, Creator Tools, Productivity, AI, Python Desktop, Video Editor, Infrastructure, Forks, Portfolio
- 📅 **Timeline view** — see when each repo was created, dot size scales with repo size, color = category
- 📂 **Category view** — repos grouped and sorted by category size
- 🪟 **Detail modal** — click any card → description, highlights, stats, GitHub link, live URL
- 🐛 **Bug Hunter** (per repo) — health score + improvements (OG tags, PWA, CSP, favicon, lazy load, TypeScript, topics...)
- 💡 **Recommend** (per repo) — feature ideas with priority/effort/impact (mobile 3D, save/load, payment, PWA, AI, i18n...)
- 🤖 **Auto-categorization** — backend detects category from language + name patterns + keywords
- 📡 **Live API status pill** — pings `/api/health` on load
- 📱 **Responsive** — works on mobile (single column < 768px)
- ⚡ **Loader animation** with progress bar on first load
- ⌨️ **Keyboard support** — ESC closes modal, click-outside dismisses

## 📊 What's inside (snapshot 2026-07-13)

| Stat | Value |
|------|-------|
| Total repos | **59** |
| Own (non-fork) | 56 |
| Forks | 3 |
| Live deployments | 48 |
| Repos in last 12 days | 49 |
| Categories | 10 |
| Total source size (non-fork) | 29.4 MB |
| Days active | 312 |

## 🗂️ The 10 categories

| Category | Count | Examples |
|----------|-------|----------|
| 🎮 3D Games | 7 | Tokyo-Student-Life-, SJ88-Wonder-Park, fitcheck-studio, stronghold-3d |
| 🕹️ 2D Games | 8 | RPG idle (TH+EN), Mars Colony, Noodle Shop, Street Fighter Thai |
| 📅 Booking Apps | 12 | BookingHub, StayHub, EventTix, MedBook, CoSpace, Driverent, GlowBook, FitBook... |
| 🎬 Creator Tools (sj88cute) | 13 | Video Editor + 11 micro tools (LUT, frame extractor, waveform, etc.) |
| 🛠️ Productivity | 5 | FlowBoard, Quick Note, Mavis Assistant, Palette, Squish |
| 🤖 AI Apps | 1 | CutOut Studio (background remover) |
| 🐍 Python Desktop | 4 | Batch rename, TikTok downloader, remove-bg, PNG→JPG |
| 🎞️ Video Editor Desktop | 1 | lnwSJCut (MiniCut MVP) |
| 🏗️ Infrastructure | 1 | SJ-hosting-control-panel (Flask + Docker) |
| 🍴 Forks + 🎨 Portfolio | 7 | CorsixTH, clawdbot, agent-skills, profile/showcase pages |

## 🚀 Run

```bash
# Option 1: open directly
open index.html

# Option 2: serve over HTTP
python3 -m http.server 8080
# then visit http://localhost:8080
```

No `npm install`, no build, no env vars. Everything is in one file.

## 🛠️ Tech stack

- **Single-file vanilla** HTML + CSS + JS — no framework
- **No external dependencies** — even fonts use system stack with `Sarabun` (Thai) and `Inter` (English)
- **CSS variables** for theming
- **Native `fetch` + DOM** — no jQuery, no React, no Vue
- **Inline data** — 59 repos as a JSON object in the script

## 📂 Repo contents

```
sj88-mission-control/
├── index.html   # The entire app (63 KB)
├── README.md    # You are here
└── .gitignore
```


## 🔌 Backend API

The dashboard is powered by a **FastAPI backend** at `https://git88.sj88ai.com/api/`:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/repos` | GET | List all 60 repos (auto-categorized) |
| `/api/repos/{name}` | GET | Single repo details |
| `/api/repos/{name}/refresh` | POST | Re-fetch from GitHub |
| `/api/repos/{name}/bugs` | POST | 🐛 Run Bug Hunter analysis |
| `/api/repos/{name}/recommend` | POST | 💡 Generate feature recommendations |
| `/api/categorize` | POST | Re-categorize all repos |
| `/api/stats` | GET | System stats |
| `/docs` | GET | Swagger API docs |

**Stack**: FastAPI 0.139 + httpx + SQLite cache, runs as systemd service `sj88-mission-control-api` on port 8200 (proxied via nginx).

**Source**: `/opt/sj88-mission-control/` on the VPS

## 🏷️ How categories are derived

Each repo was classified by hand from its `index.html` source + README + live demo:

| Signal | Category |
|--------|----------|
| Uses `Babylon.js` or `Three.js` CDN | 3D Game |
| Uses `<canvas>` + game loop | 2D Game |
| Has `booking` / `table` / `seat` / `clinic` keywords | Booking |
| Brand prefix `sj88cute-` | Creator Tools |
| Brand prefix `sj88-` (Trello/Note style) | Productivity |
| Uses `@imgly/background-removal` | AI |
| Stack is Python + Tkinter | Python Desktop |
| Stack is Flet + FFmpeg | Video Editor |
| Stack is Flask + Docker | Infrastructure |
| `is_fork: true` | Forks |
| Brand contains `demo-` / `portfolio` / `Sj` | Portfolio |

## 🧬 Data snapshot

The 59 repos data is **hardcoded** into `index.html` for portability. To refresh:

```bash
# Pull latest repos from GitHub API
curl -s "https://api.github.com/users/lnwsj/repos?per_page=100" | jq '.[] | {name, description, language, stargazers_count, size, updated_at, fork, topics}'
```

Then paste new entries into the `REPOS` array in `index.html`.

## 🌏 Bilingual

- UI: Thai + English (matches the Mavis / SJ88 brand)
- Repo descriptions: mostly Thai with English subtitles
- Live platform: [codehub.sj88ai.com](https://codehub.sj88ai.com)

## 🤝 Connect

- 🌐 [codehub.sj88ai.com](https://codehub.sj88ai.com) — Live platform
- 🐙 [github.com/lnwsj](https://github.com/lnwsj) — All 59 repos
- 🏠 [mavis.sj88ai.com](https://mavis.sj88ai.com) — Mavis Home

## 📜 License

MIT — do whatever you want, just don't blame us if a mission control screen eats your homework.

---

Built by **Mavis** 🌊 — a single AI agent shipping 100+ web apps to the world.
