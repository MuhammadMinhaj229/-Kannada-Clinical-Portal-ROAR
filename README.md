# Kannada ROAR — Clinical Research & Assessment Portal
### Stanford Rapid Online Assessment of Reading (SWR) — Kannada (ಕನ್ನಡ) Adaptation

A fully localized, psychometrically calibrated Single Word Recognition (SWR) assessment platform adapted for Kannada-speaking children and psycholinguistic researchers.

**100% Pure Frontend Architecture — Zero Server Dependencies — Runs seamlessly on Vercel Free Tier!**

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
   - **Participant Game:** `/?consent=false&storyoption=false` (or child-assigned `?participant=ID&session=N`).
   - **Clinical Research Dashboard:** `/dashboard.html` (Hidden, zero-emoji, professional clinical research UI).
2. **Pure Frontend Architecture (Zero Backend Required):**
   - **100% Client-Side Storage:** Settings, student roster, word bank edits, and trial telemetry are stored in high-performance browser `localStorage`.
   - **Zero Cold Boot / Zero Server Costs:** Operates flawlessly on Vercel's free tier with zero backend, zero database maintenance, and instant CDN asset delivery.
   - **1-Click Offline CSV Export:** Downloads complete psychometric logs directly from the browser memory.
3. **Dynamic Presentation Timing:**
   - **Infinite Mode (Recommended):** Stimulus remains on screen indefinitely until the child responds (matching practice demo mechanics).
   - **Timed Mode:** Configurable in dashboard settings (5s, 8s, 10s, 12s, or custom duration).
4. **Session-Aware Filtering:**
   - Automatically partitions the 540-word corpus into 6 balanced sessions (90 test words each: 45 Real + 45 Pseudo).
5. **Live Telemetry & Results:**
   - Captures every trial (reaction time, key pressed, accuracy) in real-time, displays live metrics in the dashboard, and allows instant export.
6. **Offline Excel / CSV Importer:**
   - Integrated SheetJS client-side parser to import `.xlsx`, `.xlsm`, or `.csv` word lists directly into any session.

---

## 3. Quick Local Setup

```bash
# Clone the repository
git clone https://github.com/MuhammadMinhaj229/-Kannada-Clinical-Portal-ROAR.git
cd -Kannada-Clinical-Portal-ROAR

# Start locally with any static server or Node:
npm start
# OR
npx serve public -p 8080
```

Access the application:
- **Child Assessment Portal:** [http://localhost:8080/?consent=false&storyoption=false](http://localhost:8080/?consent=false&storyoption=false)
- **Clinical Dashboard:** [http://localhost:8080/dashboard.html](http://localhost:8080/dashboard.html)

---

## 4. 1-Click Vercel Deployment Guide (100% Free Tier)

Because this application is 100% static with client-side localStorage state, it is completely free, instant, and never sleeps:

1. Sign in to your [Vercel Dashboard](https://vercel.com).
2. Click **Add New...** -> **Project**.
3. Import `MuhammadMinhaj229/-Kannada-Clinical-Portal-ROAR`.
4. In the project configuration:
   - **Framework Preset:** `Other`
   - **Root Directory:** `./` (or leave default)
   - **Build Command:** *(leave empty)*
   - **Output Directory:** `public` (handled automatically by `vercel.json`)
5. Click **Deploy**.
6. Within seconds, your app will be deployed with a live HTTPS URL (e.g. `https://kannada-portal-roar.vercel.app`).

### Production URLs:
- **Game Portal:** `https://<your-vercel-domain>/?consent=false&storyoption=false`
- **Clinical Dashboard:** `https://<your-vercel-domain>/dashboard.html`

---

## 5. File Structure

```text
├── public/
│   ├── index.html              # Main game bootstrapper with settings hook
│   ├── dashboard.html          # Clinical research & assessment dashboard
│   ├── settings.js             # Static settings loader reading from localStorage
│   ├── sessions_data.json      # 6 partitioned word sessions (540 words + demos)
│   ├── xlsx.full.min.js        # Local offline SheetJS library
│   ├── index.*.bundle.js       # Patched ROAR Webpack psychometric bundle
│   └── audio/
│       ├── kn/desktop/         # 42 localized Kannada voiceover MP3s
│       └── shared/             # Feedback sounds (coin, beep, fail, etc.)
├── server.js                   # Optional local development server
├── vercel.json                 # Vercel static routing & cache headers
└── package.json                # Project manifest
```

---

## 6. License & Attribution
- Stanford ROAR codebase licensed under the Stanford Academic Software License.
- Kannada translations, datasets, audio assets, and clinical management suite configured for psycholinguistic and educational research.
