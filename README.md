# SJ88 Mission Control

Dashboard ที่ดูแล **59 repos** ของ `lnwsj` — Mavis AI agent ที่ ship ตั้งแต่เกม Babylon.js 3D, single-file booking apps, DirectAdmin clone ไปจนถึง multiplayer Sims.

🌐 **Live**: https://git88.sj88ai.com/  
📦 **Frontend repo**: https://github.com/lnwsj/sj88-mission-control  
🔌 **Backend API**: https://github.com/lnwsj/sj88-mission-control-api  
🐙 **GitHub**: https://github.com/lnwsj  

## Features (v6)

### 🎮 Views
- **Grid** — 60 repos with mini heatmap (13 weeks) + growth sparkline
- **Timeline** — chronological ship history
- **By Category** — 10 categories: 3D Games, 2D Games, Booking, Creator Tools, AI Apps
- **Commits** — full commit analytics with heatmap, streak, top words

### 🚀 Per-repo actions (4 + 3)
- 🐛 **Bug Hunter** — pattern-based bug detection
- 💡 **Recommend** — suggest features based on repo state
- 🤖 **AI Code Review** — quality score (0-100) + issues + suggestions
- 🔧 **Auto-PR** — generate diff + 7-step instructions to apply
- 🔄 **Refresh** · 🚀 **Deploy** · 🐛 **Scan** (Cockpit)

### 🏆 Achievements (15)
🎯 First Commit · 💯 Century Club · 🚀 The Big Ship · 🔥 Streak Master · 🌍 Polyglot · 🤖 Auto-Categorized · 🐛 Bug Hunter · 🌐 Deployment King · 🌱 First Repo · 📦 Mass Producer · 👥 Multi-Author · 💎 200+ Commits · 🤖 AI-Dominant · 📚 Fully Documented · 🟢 Always Active

**Currently unlocked: 6/15 (40%)**

### ⌨️ Keyboard shortcuts
`D` Dark mode · `A` Achievements · `C` Chat with Mavis · `?` Show shortcuts · `/` Focus search · `G/T/V/M` Grid/Timeline/Category/Commits · `F` Favorites · `S` Share · `R` Refresh · `ESC` Close

### 💬 Mavis Chat Agent (Pattern-based)
Ask anything: "Which repo should I work on?", "Show me the most buggy repos", "What's the deploy status?", "Best 3D game?", "Most starred"

### 🟢 Live commit ticker
- Auto-refreshes /api/commits every 60s
- Shows "● Live · last: YYYY-MM-DD"
- Toast on new commits

### 📊 Backend API (19 endpoints)
```
GET  /api/health
GET  /api/repos
GET  /api/repos/all-meta         (with real issues cache, 24h TTL)
GET  /api/repos/{name}
POST /api/repos/{name}/refresh
POST /api/repos/{name}/bugs
POST /api/repos/{name}/recommend
GET  /api/repos/{name}/readme
GET  /api/repos/{name}/files
GET  /api/repos/{name}/files/{path}
GET  /api/repos/{name}/deploy
GET  /api/repos/{name}/review    (NEW v6)
GET  /api/repos/{name}/autopr    (NEW v6)
POST /api/categorize
GET  /api/stats
GET  /api/commits
POST /api/commits/refresh
GET  /api/achievements
POST /api/chat                   (NEW v6)
```

### 🗃️ Stack
- **Frontend**: single-file HTML + CSS + JS (no build step), 160KB
- **Backend**: FastAPI + SQLite, port 8200
- **Deploy**: VPS 103.22.183.111 + Let's Encrypt
- **Cache**: SQLite at `/opt/sj88-mission-control/data/cache.db`
- **Service**: `sj88-mission-control-api.service` (systemd, root)

## Snapshot 2026-07-13
- **60 repos** (59 own + 1 extra)
- **175 commits** (124 lnwsj = 71%, 51 others = 29%)
- **11 unique authors**
- Peak: 2026-07-09 (48 commits = THE SHIP DAY)
- W28 (Jul 6-12): 127 commits = SHIP WEEK
- Current streak: 6 days

## Screenshots
See `screenshot-v6-*.png` in the repo.

---
Made with 💖 by Mavis — your AI agent for shipping.
