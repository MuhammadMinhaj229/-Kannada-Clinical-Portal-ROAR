# Kannada ROAR — Clinical Research & Assessment Portal
### Stanford Rapid Online Assessment of Reading (SWR) — Kannada (ಕನ್ನಡ) Adaptation

A fully localized, psychometrically calibrated Single Word Recognition (SWR) assessment platform adapted for Kannada-speaking children and psycholinguistic researchers.

---

## 1. Provenance & Scientific Origins

This application is an adapted replica of the **Stanford ROAR (Rapid Online Assessment of Reading) — Single Word Recognition (SWR)** instrument:
* **Originating Institution:** Stanford Brain Development & Education Lab (Yeatman Lab / BDE Lab), Stanford University Graduate School of Education.
* **Core Technology:** `jsPsych` psychometric behavioral testing engine + Item Response Theory (CAT/IRT) lexical decision architecture.
* **Original Deployment:** `https://roar-swr.web.app` (Firebase / Firestore cloud pipeline).
* **Adaptation & Local Architecture:** Antigravity Engineering.

### Linguistic & Corpus Datasets
* **270 Real Kannada Words:** Derived from age-of-acquisition (mean AoA), syllable frequency, and lexical phonology metrics.
* **270 Kannada Non-Words (Pseudo-words):** Generated via systematic phonotactic mutations and ligature substitutions adhering to Kannada orthographic rules.
* **5 Demo / Practice Warm-up Items:** Hardcoded with infinite stimulus display time to acclimate young participants to left/right arrow responses.
* **Voiceover Audio:** 42 high-definition audio instructions synthesized using Microsoft Neural AI (`kn-IN-SapnaNeural`).

---

## 2. Key Architecture & Features

1. **Two Core Portals:**
   - 🎮 **Participant Game:** `/?consent=false&storyoption=false` (Local or child-assigned `?participant=ID&session=N`).
   - 📊 **Clinical Research Dashboard:** `/dashboard.html` (Hidden, zero-emoji, professional clinical research UI).
2. **Dynamic Presentation Timing:**
   - **Infinite Mode (Recommended):** Stimulus remains on screen indefinitely until the child responds (matching practice demo mechanics).
   - **Timed Mode:** Configurable in dashboard settings (5s, 8s, 10s, 12s, or custom duration).
3. **Session-Aware Filtering:**
   - Automatically partitions the 540-word corpus into 6 balanced sessions (90 test words each: 45 Real + 45 Pseudo).
4. **Live Telemetry & Results:**
   - Captures every trial (reaction time, key pressed, accuracy) in real-time, stores data locally in `student_results.json`, and provides 1-click CSV export.
5. **Offline Excel / CSV Importer:**
   - Integrated SheetJS client-side parser to import `.xlsx`, `.xlsm`, or `.csv` word lists directly into any session.

---

## 3. Quick Local Setup

```bash
# Clone the repository
git clone https://github.com/MuhammadMinhaj229/-Kannada-Clinical-Portal-ROAR.git
cd -Kannada-Clinical-Portal-ROAR

# Start the Node.js server (zero npm dependencies required!)
npm start
```

Access the application:
- **Child Assessment Portal:** [http://localhost:8080/?consent=false&storyoption=false](http://localhost:8080/?consent=false&storyoption=false)
- **Clinical Dashboard:** [http://localhost:8080/dashboard.html](http://localhost:8080/dashboard.html)

---

## 4. Production Deployment Guide

### Option A: Render.com (Recommended for Persistent Storage)
Render runs the Node.js process 24/7 and supports local JSON file persistence.
1. Sign in to [Render.com](https://render.com).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository `MuhammadMinhaj229/-Kannada-Clinical-Portal-ROAR`.
4. Configure:
   - **Environment:** `Node`
   - **Build Command:** *(leave empty or `npm install`)*
   - **Start Command:** `node server.js`
5. Click **Deploy Web Service**. Your app is live with full REST APIs, audio streaming, and data persistence!

### Option B: Railway.app (Zero-Config 1-Click)
1. Sign in to [Railway.app](https://railway.app).
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select `MuhammadMinhaj229/-Kannada-Clinical-Portal-ROAR`.
4. Railway detects `server.js` and `package.json` and deploys automatically.

### Option C: Vercel (Edge / Serverless)
A production `vercel.json` is included in this repository.
1. Sign in to [Vercel](https://vercel.com).
2. Click **Add New Project** and import `MuhammadMinhaj229/-Kannada-Clinical-Portal-ROAR`.
3. Select **Other** as the framework preset (or let Vercel auto-detect).
4. Deploy. Vercel will route all requests through `server.js` using `@vercel/node`.
*(Note: Vercel serverless functions have ephemeral file storage. For permanent cloud persistence on Vercel, attach a free Vercel KV or PostgreSQL database, or use Render/Railway for simple file-based JSON storage).*

---

## 5. File Structure

```text
├── public/
│   ├── index.html              # Main game bootstrapper with settings hook
│   ├── dashboard.html          # Clinical research & assessment dashboard
│   ├── xlsx.full.min.js        # Local offline SheetJS library
│   ├── index.*.bundle.js       # Patched ROAR Webpack psychometric bundle
│   └── audio/
│       ├── kn/desktop/         # 42 localized Kannada voiceover MP3s
│       └── shared/             # Feedback sounds (coin, beep, fail, etc.)
├── server.js                   # Node.js REST server & proxy router
├── game_settings.json          # Live psychometric timing & engine settings
├── sessions_data.json          # 6 partitioned word sessions (540 words + demos)
├── students_roster.json        # Enrolled child participant roster
├── student_results.json        # Live trial telemetry logs
├── vercel.json                 # Vercel deployment configuration
└── package.json                # Project manifest
```

---

## 6. License & Attribution
- Stanford ROAR codebase licensed under the Stanford Academic Software License.
- Kannada translations, datasets, audio assets, and clinical management suite configured for psycholinguistic and educational research.
