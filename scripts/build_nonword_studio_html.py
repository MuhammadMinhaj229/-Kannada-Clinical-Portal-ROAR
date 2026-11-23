import csv
import json
from pathlib import Path

REPO = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")
REAL_CSV = REPO / "realwords.csv"
PHONETICS_PY = REPO / "scripts" / "kannada_phonetics.py"
GEN_PY = REPO / "scripts" / "generate_kannada_nonwords.py"

# Load 270 real words
real_words = []
with open(REAL_CSV, encoding="utf-8") as f:
    for idx, r in enumerate(csv.DictReader(f), start=1):
        real_words.append({
            "id": f"R{idx:03d}",
            "word": r["word"].strip(),
            "transcription": r.get("transcription", "").strip(),
            "meaning": r.get("meaning", "").strip(),
            "pos": r.get("POS", "noun").strip().lower(),
            "age_band": r.get("Age band", "").strip(),
            "syllables": int(r.get("syllables") or 2)
        })

real_words_json = json.dumps(real_words, ensure_ascii=False)

# Combine kannada_phonetics.py + generate_kannada_nonwords.py into a clean standalone Python script string
phonetics_src = PHONETICS_PY.read_text(encoding="utf-8")
gen_src = GEN_PY.read_text(encoding="utf-8")
combined_py = (
    "# ============================================================================\n"
    "# Kannada ROAR Non-Word Generator & Akshara Phonetics Engine (Standalone)\n"
    "# Run locally: python kannada_nonword_generator.py\n"
    "# ============================================================================\n\n"
    + phonetics_src
    + "\n\n# --- Main Generator ---\n\n"
    + gen_src
)
combined_py_json = json.dumps(combined_py, ensure_ascii=False)

html_template = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<meta name="theme-color" content="#0f172a">
<title>Kannada Non-Word & Corpus Studio (100% Offline &amp; Mobile Ready)</title>
<style>
  :root {
    --bg: #0f172a;
    --surface: #1e293b;
    --surface-2: #0b1220;
    --border: #334155;
    --text: #f8fafc;
    --muted: #94a3b8;
    --accent: #3b82f6;
    --accent-hover: #2563eb;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --purple: #a855f7;
  }
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  html { scroll-behavior: smooth; }
  body {
    margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Nirmala UI", sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.5; overflow-x: hidden;
  }
  header {
    background: linear-gradient(135deg, #1e3a8a, #0f172a);
    border-bottom: 1px solid var(--border);
    padding: 1.1rem 1.25rem;
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;
  }
  header h1 { margin: 0; font-size: clamp(1.1rem, 3.5vw, 1.4rem); }
  header p { margin: 0.2rem 0 0; color: #cbd5e1; font-size: 0.82rem; }
  .badge-offline {
    background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid #059669;
    padding: 0.3rem 0.75rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600;
  }
  .quick-nav {
    position: sticky; top: 0; z-index: 20; background: rgba(15, 23, 42, 0.94);
    backdrop-filter: blur(8px); border-bottom: 1px solid var(--border);
    padding: 0.5rem 1rem; display: flex; gap: 0.45rem; overflow-x: auto; -webkit-overflow-scrolling: touch;
  }
  .quick-nav a {
    color: #cbd5e1; text-decoration: none; font-size: 0.78rem; font-weight: 600;
    background: var(--surface); border: 1px solid var(--border); border-radius: 999px;
    padding: 0.35rem 0.75rem; white-space: nowrap; flex-shrink: 0;
  }
  .quick-nav a:hover, .quick-nav a:active { background: var(--accent); color: #fff; border-color: var(--accent); }
  main { max-width: 1400px; margin: 0 auto; padding: 1rem; display: flex; flex-direction: column; gap: 1.15rem; }
  .step-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.1rem 1.15rem;
    scroll-margin-top: 56px;
  }
  .step-header {
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;
    margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 1px solid var(--border);
  }
  .step-title { display: flex; align-items: center; gap: 0.65rem; font-size: 1rem; font-weight: 700; }
  .step-num {
    width: 28px; height: 28px; border-radius: 50%; background: var(--accent); color: #fff; flex-shrink: 0;
    display: inline-flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 700;
  }
  .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 0.85rem; }
  .grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 0.75rem; }
  label { display: block; font-size: 0.78rem; color: var(--muted); margin-bottom: 0.25rem; font-weight: 600; }
  input[type="text"], input[type="number"], select, textarea {
    width: 100%; background: var(--surface-2); color: var(--text); border: 1px solid var(--border);
    border-radius: 8px; padding: 0.55rem 0.7rem; font-size: 0.9rem; font-family: inherit; min-height: 40px;
  }
  input[type="checkbox"] { width: 20px; height: 20px; accent-color: var(--accent); cursor: pointer; }
  textarea { resize: vertical; font-family: "Nirmala UI", monospace; }
  .btn {
    background: var(--accent); color: #fff; border: none; border-radius: 8px;
    padding: 0.55rem 0.95rem; font-size: 0.84rem; font-weight: 600; cursor: pointer;
    display: inline-flex; align-items: center; justify-content: center; gap: 0.4rem; min-height: 40px;
  }
  .btn:hover { background: var(--accent-hover); }
  .btn-secondary { background: #334155; }
  .btn-secondary:hover { background: #475569; }
  .btn-success { background: #059669; }
  .btn-success:hover { background: #047857; }
  .btn-danger { background: #dc2626; }
  .btn-danger:hover { background: #b91c1c; }
  .btn-sm { padding: 0.4rem 0.7rem; font-size: 0.78rem; min-height: 36px; }
  .logic-row {
    display: grid; grid-template-columns: 36px 1.6fr 1.2fr 95px 75px 1.4fr 48px;
    gap: 0.6rem; align-items: center; background: var(--surface-2);
    border: 1px solid var(--border); border-radius: 8px; padding: 0.65rem; margin-bottom: 0.55rem;
  }
  .prop-bar {
    height: 12px; border-radius: 999px; background: var(--surface-2); overflow: hidden;
    display: flex; border: 1px solid var(--border); margin: 0.75rem 0;
  }
  .prop-seg { height: 100%; transition: width 0.2s; }
  .table-wrap {
    overflow-x: auto; -webkit-overflow-scrolling: touch; max-height: 460px;
    border: 1px solid var(--border); border-radius: 8px; width: 100%;
  }
  table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
  th {
    position: sticky; top: 0; background: #0b1220; color: #cbd5e1; text-align: left;
    padding: 0.6rem 0.65rem; border-bottom: 1px solid var(--border); z-index: 2; white-space: nowrap;
  }
  td { padding: 0.5rem 0.65rem; border-bottom: 1px solid #1e293b; white-space: nowrap; }
  tr:hover td { background: rgba(59, 130, 246, 0.08); }
  .kn { font-family: "Nirmala UI", "Noto Sans Kannada", sans-serif; font-size: 1.02rem; font-weight: 600; }
  .pill { padding: 0.15rem 0.5rem; border-radius: 999px; font-size: 0.72rem; font-weight: 600; display: inline-block; }
  .pill-noun { background: #2e1065; color: #c084fc; }
  .pill-verb { background: #082f49; color: #38bdf8; }
  .pill-adj { background: #064e3b; color: #34d399; }
  .pill-adv { background: #451a03; color: #fbbf24; }
  .pill-real { background: #1e3a8a; color: #93c5fd; }
  .pill-pseudo { background: #7f1d1d; color: #fca5a5; }
  .stat-box {
    background: var(--surface-2); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem 0.9rem;
  }
  .stat-val { font-size: 1.25rem; font-weight: 700; color: #60a5fa; }
  .stat-lbl { font-size: 0.75rem; color: var(--muted); }
  .tabs { display: flex; gap: 0.45rem; flex-wrap: wrap; }
  .tab {
    background: var(--surface-2); color: var(--muted); border: 1px solid var(--border);
    padding: 0.45rem 0.85rem; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.82rem; min-height: 38px;
  }
  .tab.active { background: var(--accent); color: #fff; border-color: var(--accent); }
  pre {
    background: #020617; color: #e2e8f0; padding: 0.9rem; border-radius: 8px; border: 1px solid var(--border);
    overflow-x: auto; -webkit-overflow-scrolling: touch; max-height: 340px; font-size: 0.76rem; line-height: 1.45;
  }
  .editable-cell {
    background: transparent; border: 1px solid transparent; color: var(--text); padding: 0.25rem 0.4rem;
    border-radius: 4px; width: 120px; font-family: "Nirmala UI", sans-serif; font-size: 0.95rem;
  }
  .editable-cell:focus { background: var(--surface-2); border-color: var(--accent); outline: none; }

  @media (max-width: 768px) {
    header { padding: 0.9rem 1rem; }
    main { padding: 0.75rem; gap: 0.9rem; }
    .step-card { padding: 0.95rem 0.85rem; border-radius: 10px; }
    .grid-4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .logic-row {
      grid-template-columns: 32px 1fr 44px;
      grid-template-areas:
        "chk name del"
        "mode mode mode"
        "cnt pct pct"
        "desc desc desc";
    }
    .logic-row > *:nth-child(1) { grid-area: chk; }
    .logic-row > *:nth-child(2) { grid-area: name; }
    .logic-row > *:nth-child(3) { grid-area: mode; }
    .logic-row > *:nth-child(4) { grid-area: cnt; }
    .logic-row > *:nth-child(5) { grid-area: pct; text-align: left !important; }
    .logic-row > *:nth-child(6) { grid-area: desc; }
    .logic-row > *:nth-child(7) { grid-area: del; justify-self: end; }
    input[type="text"], input[type="number"], select, textarea { font-size: 16px; }
    #searchPreviewInput { width: 100% !important; }
  }
  @media (max-width: 440px) {
    .grid-4 { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>

<header>
  <div>
    <h1>Kannada Non-Word &amp; Corpus Studio</h1>
    <p>Step-by-Step Editable Linguistic Generator, Dual-Constraint Sequencer &amp; Offline Excel (.xlsx) Exporter</p>
  </div>
  <span class="badge-offline">100% Offline &amp; Mobile Ready</span>
</header>

<nav class="quick-nav" aria-label="Step navigation">
  <a href="#step1">1. Real Words</a>
  <a href="#step2">2. Logics &amp; Proportions</a>
  <a href="#step3">3. Sequencing</a>
  <a href="#step4">4. Preview &amp; Excel</a>
  <a href="#step5">5. Python Script</a>
</nav>

<main>
  <!-- STEP 1: REAL WORDS CORPUS -->
  <section class="step-card" id="step1">
    <div class="step-header">
      <div class="step-title"><span class="step-num">1</span> Real Words Corpus (Editable Input)</div>
      <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
        <button class="btn btn-secondary btn-sm" onclick="toggleRealWordsEditor()">Show / Edit Real Words List</button>
        <button class="btn btn-secondary btn-sm" onclick="addBlankRealWord()">+ Add Real Word</button>
        <label class="btn btn-secondary btn-sm" style="margin:0; cursor:pointer;">
          Import CSV <input type="file" accept=".csv,.txt" style="display:none" onchange="importRealCSV(event)">
        </label>
        <button class="btn btn-secondary btn-sm" onclick="resetDefaultRealWords()">Reset 270 Default Words</button>
      </div>
    </div>

    <div class="grid-4">
      <div class="stat-box"><div class="stat-val" id="statRealCount">270</div><div class="stat-lbl">Real Words Loaded</div></div>
      <div class="stat-box"><div class="stat-val" id="statTargetNonwords">270</div><div class="stat-lbl">Target Non-Words to Generate</div></div>
      <div class="stat-box"><div class="stat-val" id="statPosMix">—</div><div class="stat-lbl">POS Breakdown (N / V / Adj / Adv)</div></div>
      <div class="stat-box">
        <label for="targetTotalNonwords">Total Non-Words to Generate</label>
        <input type="number" id="targetTotalNonwords" min="1" max="2000" value="270" onchange="recalcProportionality()">
      </div>
    </div>

    <div id="realWordsEditorWrap" style="display:none; margin-top:1rem;">
      <p style="font-size:0.8rem; color:var(--muted); margin-bottom:0.5rem;">Edit any word, POS, meaning, or syllable count inline. Changes automatically feed into Step 2 generation.</p>
      <div class="table-wrap" style="max-height:280px;">
        <table>
          <thead><tr><th>#</th><th>Word (ಕನ್ನಡ)</th><th>POS</th><th>Syllables</th><th>Meaning</th><th>Action</th></tr></thead>
          <tbody id="realWordsTbody"></tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- STEP 2: EDITABLE LOGICS & PROPORTIONALITY -->
  <section class="step-card" id="step2">
    <div class="step-header">
      <div class="step-title"><span class="step-num">2</span> Non-Word Generation Logics &amp; Proportionality (4 + Custom 5th+ Logics)</div>
      <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
        <button class="btn btn-secondary btn-sm" onclick="addCustomLogic()">+ Add 5th / Custom Logic</button>
        <button class="btn btn-secondary btn-sm" onclick="normalizeProportions()">Auto-Balance to 100%</button>
      </div>
    </div>

    <div id="logicsContainer"></div>

    <div class="prop-bar" id="propBar"></div>
    <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:var(--muted); margin-bottom:1rem;">
      <span id="propSummaryText">Total Allocation: 100% (270 words)</span>
      <span>Strict Syllable Match &amp; Non-Repeating Phoneme Queues Active</span>
    </div>

    <div class="grid-2">
      <div>
        <label for="consonantPoolInput">Non-Repeating Consonant Queue (comma-separated)</label>
        <input type="text" id="consonantPoolInput" value="ಕ,ಗ,ಚ,ಜ,ಟ,ಡ,ಣ,ತ,ದ,ನ,ಪ,ಬ,ಮ,ಯ,ರ,ಲ,ವ,ಶ,ಸ,ಹ,ಳ">
      </div>
      <div>
        <label for="vowelPoolInput">Non-Repeating Matra / Vowel Queue (comma-separated)</label>
        <input type="text" id="vowelPoolInput" value="ಾ,ಿ,ೀ,ು,ೂ,ೆ,ೇ,ೊ,ೋ">
      </div>
    </div>
  </section>

  <!-- STEP 3: SEQUENCING & CONSTRAINTS -->
  <section class="step-card" id="step3">
    <div class="step-header">
      <div class="step-title"><span class="step-num">3</span> Session Partitioning &amp; Randomness Rules</div>
      <button class="btn" onclick="generateEverything()">&#9889; Generate Non-Words &amp; Sequences</button>
    </div>

    <div class="grid-4">
      <div>
        <label for="wordsPerSessionInput">Words Per Session (50% Real / 50% Non-Word)</label>
        <input type="number" id="wordsPerSessionInput" min="10" max="300" value="90">
      </div>
      <div>
        <label for="maxStreakInput">Max Lexicality Streak (Unpredictable Runs)</label>
        <input type="number" id="maxStreakInput" min="1" max="10" value="3">
      </div>
      <div>
        <label for="posRotateSelect">POS Rotation (Avoid Consecutive Same POS)</label>
        <select id="posRotateSelect">
          <option value="true" selected>Enabled (Smart POS Rotation)</option>
          <option value="false">Disabled (Random POS)</option>
        </select>
      </div>
      <div>
        <label for="strictSyllableSelect">Syllable Count Preservation</label>
        <select id="strictSyllableSelect">
          <option value="true" selected>Strict Match (Verify &amp; Log Both)</option>
          <option value="false">Allow Variance</option>
        </select>
      </div>
    </div>
  </section>

  <!-- STEP 4: LIVE PREVIEW, INLINE EDIT & OFFLINE EXCEL EXPORT -->
  <section class="step-card" id="step4">
    <div class="step-header">
      <div class="step-title"><span class="step-num">4</span> Generated Corpus Preview &amp; Offline Excel (.xlsx) Export</div>
      <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
        <button class="btn btn-success" onclick="exportOfflineXLSX()">&#128196; Download Complete Excel (.xlsx)</button>
        <button class="btn btn-secondary btn-sm" onclick="exportCSV('nonwords')">Export Non-Words CSV</button>
        <button class="btn btn-secondary btn-sm" onclick="exportCSV('master')">Export Master Corpus CSV</button>
      </div>
    </div>

    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.75rem; margin-bottom:0.85rem;">
      <div class="tabs">
        <button class="tab active" onclick="switchPreviewTab('nonwords', this)">Non-Words (<span id="cntNonwords">0</span>)</button>
        <button class="tab" onclick="switchPreviewTab('master', this)">Master Corpus (<span id="cntMaster">0</span>)</button>
        <button class="tab" onclick="switchPreviewTab('sessions', this)">Sessions (<span id="cntSessions">0</span>)</button>
      </div>
      <div style="display:flex; gap:0.5rem; align-items:center;">
        <select id="sessionSelectPreview" style="width:auto; display:none;" onchange="renderPreviewTable()"></select>
        <input type="text" id="searchPreviewInput" placeholder="Filter words, source, logic, POS..." style="width:240px;" oninput="renderPreviewTable()">
      </div>
    </div>

    <div class="table-wrap">
      <table>
        <thead id="previewThead"></thead>
        <tbody id="previewTbody"></tbody>
      </table>
    </div>
  </section>

  <!-- STEP 5: COMPLETE PYTHON SCRIPT -->
  <section class="step-card" id="step5">
    <div class="step-header">
      <div class="step-title"><span class="step-num">5</span> Complete Python Non-Word Generation Script (Local Verification)</div>
      <div style="display:flex; gap:0.5rem;">
        <button class="btn btn-secondary btn-sm" onclick="copyPythonScript()">Copy Python Script</button>
        <button class="btn btn-sm" onclick="downloadPythonScript()">Download .py File</button>
      </div>
    </div>
    <pre id="pythonCodeBlock"></pre>
  </section>
</main>

<script>
// =========================================================================
// Embedded 270 Real Words & Complete Python Reference Script
// =========================================================================
const DEFAULT_REAL_WORDS = __REAL_WORDS_JSON__;
const PYTHON_SCRIPT_TEXT = __PYTHON_SCRIPT_JSON__;

let realWords = JSON.parse(JSON.stringify(DEFAULT_REAL_WORDS));
let generatedNonWords = [];
let masterCorpus = [];
let generatedSessions = {};
let activePreviewTab = 'nonwords';

// Editable Logic Definitions (Supports 4 built-in + custom 5th+ logics)
let logicsConfig = [
  { id: 'L1', enabled: true, name: 'Logic 1: Consonant Replacement', mode: 'consonant_replace', count: 68, color: '#3b82f6', desc: 'Replace consonant using non-repeating queue; preserves syllables' },
  { id: 'L2', enabled: true, name: 'Logic 2: Vowel / Matra Replacement', mode: 'vowel_replace', count: 68, color: '#10b981', desc: 'Replace swara/matra using non-repeating queue; preserves syllables' },
  { id: 'L3', enabled: true, name: 'Logic 3: Affix Splicing (Suffix1 + Prefix2)', mode: 'affix_splice', count: 67, color: '#f59e0b', desc: 'Splice suffix of Source Word 1 + prefix of Source Word 2' },
  { id: 'L4', enabled: true, name: 'Logic 4: Prefix Shift (Prefix1 + Suffix2)', mode: 'prefix_shift', count: 67, color: '#a855f7', desc: 'Combine prefix of Source Word 1 + suffix of Source Word 2' },
  { id: 'L5', enabled: false, name: 'Logic 5: Custom Syllable Reversal / Swap', mode: 'syllable_swap', count: 0, color: '#ec4899', desc: 'Reverse or swap aksharas while preserving syllable count' }
];

// =========================================================================
// Kannada Phonetic / Akshara Parser (Exact Sync with Python Engine)
// =========================================================================
const SWARAS = new Set(['ಅ','ಆ','ಇ','ಈ','ಉ','ಊ','ಋ','ಎ','ಏ','ಐ','ಒ','ಓ','ಔ']);
const MATRAS = new Set(['ಾ','ಿ','ೀ','ು','ೂ','ೃ','ೆ','ೇ','ೈ','ೊ','ೋ','ೌ']);
const ANUSVARA_VISARGA = new Set(['\u0c82', '\u0c83']);
const SWARA_ROTATION = ['ಆ','ಇ','ಈ','ಉ','ಊ','ಎ','ಏ','ಒ','ಓ'];

function parseAksharas(word) {
  const re = /(?:[\u0c95-\u0cb9]\u0ccd)*[\u0c95-\u0cb9](?:[\u0cbe-\u0ccc]|\u0ccd)?[\u0c82\u0c83]?|[\u0c85-\u0c94][\u0c82\u0c83]?/g;
  return word.match(re) || [];
}

function countSyllables(word) {
  return parseAksharas(word).length;
}

function decomposeAkshara(ak) {
  if (!ak) return { head: '', tail: '', isSwara: false };
  if (SWARAS.has(ak[0])) {
    return { head: ak[0], tail: ak.slice(1), isSwara: true };
  }
  let idx = ak.length;
  while (idx > 0 && (MATRAS.has(ak[idx - 1]) || ANUSVARA_VISARGA.has(ak[idx - 1]))) {
    idx--;
  }
  return { head: ak.slice(0, idx), tail: ak.slice(idx), isSwara: false };
}

// =========================================================================
// Step 1: Real Words Management
// =========================================================================
function updateRealWordStats() {
  document.getElementById('statRealCount').textContent = realWords.length;
  const counts = { noun: 0, verb: 0, adjective: 0, adverb: 0 };
  realWords.forEach(w => {
    const p = (w.pos || 'noun').toLowerCase();
    if (counts[p] !== undefined) counts[p]++;
  });
  document.getElementById('statPosMix').textContent = `${counts.noun} / ${counts.verb} / ${counts.adjective} / ${counts.adverb}`;
}

function toggleRealWordsEditor() {
  const el = document.getElementById('realWordsEditorWrap');
  el.style.display = el.style.display === 'none' ? 'block' : 'none';
  if (el.style.display === 'block') renderRealWordsTable();
}

function renderRealWordsTable() {
  const tb = document.getElementById('realWordsTbody');
  tb.innerHTML = realWords.map((w, i) => `
    <tr>
      <td>${i + 1}</td>
      <td><input class="editable-cell kn" value="${escHtml(w.word)}" onchange="editRealWord(${i}, 'word', this.value)"></td>
      <td>
        <select style="width:110px" onchange="editRealWord(${i}, 'pos', this.value)">
          <option value="noun" ${w.pos==='noun'?'selected':''}>noun</option>
          <option value="verb" ${w.pos==='verb'?'selected':''}>verb</option>
          <option value="adjective" ${w.pos==='adjective'?'selected':''}>adjective</option>
          <option value="adverb" ${w.pos==='adverb'?'selected':''}>adverb</option>
        </select>
      </td>
      <td>${countSyllables(w.word)}</td>
      <td><input class="editable-cell" style="width:160px" value="${escHtml(w.meaning || '')}" onchange="editRealWord(${i}, 'meaning', this.value)"></td>
      <td><button class="btn btn-danger btn-sm" onclick="removeRealWord(${i})">Delete</button></td>
    </tr>
  `).join('');
}

function editRealWord(idx, field, val) {
  realWords[idx][field] = val.trim();
  if (field === 'word') realWords[idx].syllables = countSyllables(val.trim());
  updateRealWordStats();
  if (field === 'word') renderRealWordsTable();
}

function addBlankRealWord() {
  realWords.unshift({ id: `R${realWords.length + 1}`, word: 'ಹೊಸಪದ', pos: 'noun', meaning: 'Custom Word', syllables: 4, age_band: '3-4' });
  updateRealWordStats();
  document.getElementById('realWordsEditorWrap').style.display = 'block';
  renderRealWordsTable();
}

function removeRealWord(idx) {
  realWords.splice(idx, 1);
  updateRealWordStats();
  renderRealWordsTable();
}

function resetDefaultRealWords() {
  realWords = JSON.parse(JSON.stringify(DEFAULT_REAL_WORDS));
  updateRealWordStats();
  renderRealWordsTable();
}

function importRealCSV(ev) {
  const file = ev.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    const lines = e.target.result.split(/\r?\n/).filter(Boolean);
    if (lines.length < 2) return;
    const hdr = lines[0].split(',').map(s => s.trim().toLowerCase());
    const wIdx = hdr.findIndex(h => h === 'word' || h.includes('kannada'));
    const pIdx = hdr.findIndex(h => h === 'pos' || h.includes('speech'));
    const mIdx = hdr.findIndex(h => h.includes('meaning'));
    const imported = [];
    for (let i = 1; i < lines.length; i++) {
      const cols = lines[i].split(',');
      const w = (cols[wIdx >= 0 ? wIdx : 0] || '').trim();
      if (!w) continue;
      imported.push({
        id: `R${imported.length + 1}`,
        word: w,
        pos: (cols[pIdx >= 0 ? pIdx : 1] || 'noun').trim().toLowerCase(),
        meaning: (cols[mIdx] || '').trim(),
        syllables: countSyllables(w),
        age_band: ''
      });
    }
    if (imported.length) {
      realWords = imported;
      document.getElementById('targetTotalNonwords').value = imported.length;
      recalcProportionality();
      updateRealWordStats();
      renderRealWordsTable();
    }
  };
  reader.readAsText(file, 'UTF-8');
}

// =========================================================================
// Step 2: Editable Logics & Proportionality
// =========================================================================
function renderLogics() {
  const container = document.getElementById('logicsContainer');
  const totalTarget = parseInt(document.getElementById('targetTotalNonwords').value || '270', 10);
  container.innerHTML = logicsConfig.map((lg, idx) => {
    const pct = totalTarget > 0 ? ((lg.count / totalTarget) * 100).toFixed(1) : '0.0';
    return `
      <div class="logic-row">
        <input type="checkbox" ${lg.enabled ? 'checked' : ''} onchange="updateLogic(${idx}, 'enabled', this.checked)">
        <input type="text" value="${escHtml(lg.name)}" onchange="updateLogic(${idx}, 'name', this.value)">
        <select onchange="updateLogic(${idx}, 'mode', this.value)">
          <option value="consonant_replace" ${lg.mode==='consonant_replace'?'selected':''}>Consonant Replacement</option>
          <option value="vowel_replace" ${lg.mode==='vowel_replace'?'selected':''}>Vowel / Matra Replacement</option>
          <option value="affix_splice" ${lg.mode==='affix_splice'?'selected':''}>Affix Splicing (Suffix1 + Prefix2)</option>
          <option value="prefix_shift" ${lg.mode==='prefix_shift'?'selected':''}>Prefix Shift (Prefix1 + Suffix2)</option>
          <option value="syllable_swap" ${lg.mode==='syllable_swap'?'selected':''}>Syllable Reversal / Swap (Logic 5)</option>
        </select>
        <div>
          <input type="number" min="0" max="2000" value="${lg.count}" onchange="updateLogic(${idx}, 'count', parseInt(this.value || 0, 10))">
        </div>
        <div style="font-size:0.82rem; text-align:center; color:${lg.color}; font-weight:700;">${pct}%</div>
        <input type="text" value="${escHtml(lg.desc)}" onchange="updateLogic(${idx}, 'desc', this.value)">
        <button class="btn btn-danger btn-sm" onclick="removeLogic(${idx})" ${logicsConfig.length <= 1 ? 'disabled' : ''}>&times;</button>
      </div>
    `;
  }).join('');
  updatePropBar();
}

function updateLogic(idx, field, val) {
  logicsConfig[idx][field] = val;
  if (field === 'enabled' && val && logicsConfig[idx].count === 0) {
    logicsConfig[idx].count = 20;
  }
  if (field === 'enabled' && !val) {
    logicsConfig[idx].count = 0;
  }
  renderLogics();
}

function addCustomLogic() {
  const n = logicsConfig.length + 1;
  const palette = ['#ec4899', '#14b8a6', '#f97316', '#8b5cf6'];
  logicsConfig.push({
    id: `L${n}`,
    enabled: true,
    name: `Logic ${n}: Custom Syllable Swap`,
    mode: 'syllable_swap',
    count: 20,
    color: palette[(n - 5) % palette.length],
    desc: 'Custom editable transformation rule'
  });
  normalizeProportions();
}

function removeLogic(idx) {
  logicsConfig.splice(idx, 1);
  renderLogics();
}

function recalcProportionality() {
  const total = parseInt(document.getElementById('targetTotalNonwords').value || '270', 10);
  document.getElementById('statTargetNonwords').textContent = total;
  normalizeProportions();
}

function normalizeProportions() {
  const total = parseInt(document.getElementById('targetTotalNonwords').value || '270', 10);
  const enabled = logicsConfig.filter(l => l.enabled);
  if (!enabled.length) return;
  const sumCurrent = enabled.reduce((a, b) => a + (b.count || 0), 0);
  if (sumCurrent === 0) {
    const base = Math.floor(total / enabled.length);
    let rem = total - base * enabled.length;
    enabled.forEach(l => { l.count = base + (rem-- > 0 ? 1 : 0); });
  } else {
    let assigned = 0;
    enabled.forEach((l, i) => {
      if (i === enabled.length - 1) {
        l.count = Math.max(0, total - assigned);
      } else {
        l.count = Math.round((l.count / sumCurrent) * total);
        assigned += l.count;
      }
    });
  }
  renderLogics();
}

function updatePropBar() {
  const totalTarget = parseInt(document.getElementById('targetTotalNonwords').value || '270', 10);
  const active = logicsConfig.filter(l => l.enabled && l.count > 0);
  const sum = active.reduce((a, b) => a + b.count, 0);
  const bar = document.getElementById('propBar');
  bar.innerHTML = active.map(l => {
    const w = sum > 0 ? (l.count / Math.max(sum, totalTarget)) * 100 : 0;
    return `<div class="prop-seg" style="width:${w}%; background:${l.color};" title="${escHtml(l.name)}: ${l.count}"></div>`;
  }).join('');
  document.getElementById('propSummaryText').textContent =
    `Assigned: ${sum} / ${totalTarget} words` + (sum !== totalTarget ? ' (Click "Auto-Balance to 100%" to match target)' : ' (100% Balanced)');
}

// =========================================================================
// Non-Word Generation Engine (All 5 Logics + Non-Repeating Queues)
// =========================================================================
function generateEverything() {
  if (!realWords.length) { alert('Please add at least one real word.'); return; }
  const realSet = new Set(realWords.map(w => w.word));
  const consPool = document.getElementById('consonantPoolInput').value.split(',').map(s => s.trim()).filter(Boolean);
  const matraPool = document.getElementById('vowelPoolInput').value.split(',').map(s => s.trim()).filter(Boolean);
  const strictSyllable = document.getElementById('strictSyllableSelect').value === 'true';

  let cIdx = 0, mIdx = 0, sIdx = 0;
  function nextCons(exclude) {
    for (let i = 0; i < consPool.length; i++) {
      const c = consPool[(cIdx++) % consPool.length];
      if (!exclude || !exclude.includes(c)) return c;
    }
    return consPool[0] || 'ಜ';
  }
  function nextMatra(exclude) {
    for (let i = 0; i < matraPool.length; i++) {
      const m = matraPool[(mIdx++) % matraPool.length];
      if (m !== exclude) return m;
    }
    return matraPool[0] || 'ಿ';
  }
  function nextSwara(exclude) {
    for (let i = 0; i < SWARA_ROTATION.length; i++) {
      const s = SWARA_ROTATION[(sIdx++) % SWARA_ROTATION.length];
      if (s !== exclude) return s;
    }
    return 'ಉ';
  }

  // Build ordered assignment slots per enabled logic
  const slots = [];
  logicsConfig.filter(l => l.enabled && l.count > 0).forEach(lg => {
    for (let i = 0; i < lg.count; i++) slots.push(lg);
  });

  const usedNonwords = new Set(realSet);
  generatedNonWords = [];

  for (let i = 0; i < slots.length; i++) {
    const lg = slots[i];
    const rw1 = realWords[i % realWords.length];
    const rw2 = realWords[(i + 7) % realWords.length];
    const aks1 = parseAksharas(rw1.word);
    const aks2 = parseAksharas(rw2.word);
    let nw = '', sw2Word = '', sw2Syl = '', transformDesc = '';

    if (lg.mode === 'consonant_replace') {
      for (let attempt = 0; attempt < 12; attempt++) {
        const cand = aks1.slice();
        const posIdx = attempt < 4 ? 0 : (cand.length > 1 ? 1 : 0);
        const dec = decomposeAkshara(cand[posIdx]);
        const nc = nextCons(dec.head);
        cand[posIdx] = dec.isSwara ? (nc + (dec.tail || '')) : (nc + dec.tail);
        const joined = cand.join('');
        if (!usedNonwords.has(joined) && (!strictSyllable || countSyllables(joined) === aks1.length)) {
          nw = joined;
          transformDesc = `${aks1[posIdx]} → ${cand[posIdx]}`;
          break;
        }
      }
      if (!nw) {
        const dec = decomposeAkshara(aks1[0]);
        const nc = nextCons(dec.head);
        const cand = [nc + dec.tail, ...aks1.slice(1)].join('');
        nw = cand;
        transformDesc = `${aks1[0]} → ${nc + dec.tail}`;
      }
    } else if (lg.mode === 'vowel_replace') {
      for (let attempt = 0; attempt < 12; attempt++) {
        const cand = aks1.slice();
        const posIdx = (cand.length - 1 + attempt) % cand.length;
        const dec = decomposeAkshara(cand[posIdx]);
        if (dec.isSwara) {
          const ns = nextSwara(dec.head);
          cand[posIdx] = ns + dec.tail;
        } else {
          const nm = nextMatra(dec.tail);
          cand[posIdx] = dec.head + nm;
        }
        const joined = cand.join('');
        if (!usedNonwords.has(joined) && (!strictSyllable || countSyllables(joined) === aks1.length)) {
          nw = joined;
          transformDesc = `${aks1[posIdx]} → ${cand[posIdx]}`;
          break;
        }
      }
      if (!nw) {
        const dec = decomposeAkshara(aks1[0]);
        const rep = dec.isSwara ? (nextSwara(dec.head) + dec.tail) : (dec.head + nextMatra(dec.tail));
        nw = [rep, ...aks1.slice(1)].join('');
        transformDesc = `${aks1[0]} → ${rep}`;
      }
    } else if (lg.mode === 'affix_splice') {
      // Suffix of rw1 + Prefix of rw2 (preserve syllable count of rw1)
      const targetLen = aks1.length;
      const take1 = Math.max(1, Math.floor(targetLen / 2));
      const take2 = Math.max(1, targetLen - take1);
      const part1 = aks1.slice(aks1.length - take1).join('');
      const part2 = aks2.slice(0, Math.min(take2, aks2.length)).join('');
      nw = part1 + part2;
      sw2Word = rw2.word;
      sw2Syl = countSyllables(rw2.word);
      transformDesc = `suffix(${rw1.word}) + prefix(${rw2.word})`;
    } else if (lg.mode === 'prefix_shift') {
      // Prefix of rw1 + Suffix of rw2 (preserve syllable count of rw1)
      const targetLen = aks1.length;
      const take1 = Math.max(1, Math.ceil(targetLen / 2));
      const take2 = Math.max(1, targetLen - take1);
      const part1 = aks1.slice(0, take1).join('');
      const part2 = aks2.slice(Math.max(0, aks2.length - take2)).join('');
      nw = part1 + part2;
      sw2Word = rw2.word;
      sw2Syl = countSyllables(rw2.word);
      transformDesc = `prefix(${rw1.word}) + suffix(${rw2.word})`;
    } else if (lg.mode === 'syllable_swap') {
      if (aks1.length >= 2) {
        const rev = aks1.slice().reverse().join('');
        nw = rev === rw1.word ? (aks1[1] + aks1[0] + aks1.slice(2).join('')) : rev;
        transformDesc = `swap/reverse(${aks1.join('·')})`;
      } else {
        const dec = decomposeAkshara(aks1[0]);
        const nc = nextCons(dec.head);
        nw = nc + dec.tail;
        transformDesc = `${aks1[0]} → ${nw}`;
      }
    }

    usedNonwords.add(nw);
    const sw1Syl = countSyllables(rw1.word);
    const nwSyl = countSyllables(nw);

    generatedNonWords.push({
      id: `N${String(i + 1).padStart(3, '0')}`,
      nonword: nw,
      logic: lg.name,
      source_word_1: rw1.word,
      source_word_2: sw2Word || '—',
      pos: rw1.pos || 'noun',
      transformation: transformDesc,
      nw_syllables: nwSyl,
      sw1_syllables: sw1Syl,
      sw2_syllables: sw2Syl || '—',
      expected_key: 'Left Arrow (←)',
      arrow_color: 'Red (#c0392b)'
    });
  }

  // Build Master Corpus
  masterCorpus = [];
  realWords.forEach((r, idx) => {
    masterCorpus.push({
      id: r.id || `R${String(idx + 1).padStart(3, '0')}`,
      word: r.word,
      lexicality: 'Real Word',
      type: 'real',
      pos: r.pos || 'noun',
      logic: 'Original Real Word',
      source_word_1: '—',
      source_word_2: '—',
      transformation: '—',
      syllables: countSyllables(r.word),
      sw1_syllables: '—',
      sw2_syllables: '—',
      expected_key: 'Right Arrow (→)',
      arrow_color: 'Blue (#2980b9)',
      meaning: r.meaning || ''
    });
  });
  generatedNonWords.forEach(n => {
    masterCorpus.push({
      id: n.id,
      word: n.nonword,
      lexicality: 'Non-Word',
      type: 'pseudo',
      pos: n.pos,
      logic: n.logic,
      source_word_1: n.source_word_1,
      source_word_2: n.source_word_2,
      transformation: n.transformation,
      syllables: n.nw_syllables,
      sw1_syllables: n.sw1_syllables,
      sw2_syllables: n.sw2_syllables,
      expected_key: n.expected_key,
      arrow_color: n.arrow_color,
      meaning: ''
    });
  });

  buildSessions();
  updateCounters();
  renderPreviewTable();
}

function buildSessions() {
  const perSess = parseInt(document.getElementById('wordsPerSessionInput').value || '90', 10);
  const maxStreak = parseInt(document.getElementById('maxStreakInput').value || '3', 10);
  const rotatePos = document.getElementById('posRotateSelect').value === 'true';

  const reals = masterCorpus.filter(w => w.type === 'real').slice().sort(() => Math.random() - 0.5);
  const pseudos = masterCorpus.filter(w => w.type === 'pseudo').slice().sort(() => Math.random() - 0.5);

  const half = Math.floor(perSess / 2);
  const numSessions = Math.max(1, Math.min(Math.floor(reals.length / half), Math.floor(pseudos.length / half)));
  generatedSessions = {};

  const sel = document.getElementById('sessionSelectPreview');
  sel.innerHTML = '';

  for (let s = 1; s <= numSessions; s++) {
    const rSlice = reals.slice((s - 1) * half, s * half);
    const pSlice = pseudos.slice((s - 1) * half, s * half);
    const seq = [];
    let lastType = '', streak = 0, lastPos = '';

    while (rSlice.length || pSlice.length) {
      let pickType;
      if (!rSlice.length) pickType = 'pseudo';
      else if (!pSlice.length) pickType = 'real';
      else if (streak >= maxStreak) pickType = lastType === 'real' ? 'pseudo' : 'real';
      else pickType = Math.random() < (rSlice.length / (rSlice.length + pSlice.length)) ? 'real' : 'pseudo';

      const pool = pickType === 'real' ? rSlice : pSlice;
      let idx = 0;
      if (rotatePos) {
        const nonColliding = pool.findIndex(item => item.pos !== lastPos);
        if (nonColliding >= 0) idx = nonColliding;
      }
      const chosen = pool.splice(idx, 1)[0];
      streak = (pickType === lastType) ? streak + 1 : 1;
      lastType = pickType;
      lastPos = chosen.pos;
      seq.push(Object.assign({ trial: seq.length + 1 }, chosen));
    }
    generatedSessions[s] = seq;
    const opt = document.createElement('option');
    opt.value = String(s);
    opt.textContent = `Session ${s} (${seq.length} words)`;
    sel.appendChild(opt);
  }
}

function updateCounters() {
  document.getElementById('cntNonwords').textContent = generatedNonWords.length;
  document.getElementById('cntMaster').textContent = masterCorpus.length;
  document.getElementById('cntSessions').textContent = Object.keys(generatedSessions).length;
}

function switchPreviewTab(tab, btn) {
  activePreviewTab = tab;
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('sessionSelectPreview').style.display = tab === 'sessions' ? 'inline-block' : 'none';
  renderPreviewTable();
}

function posPill(pos) {
  const p = (pos || 'noun').toLowerCase();
  const cls = p === 'verb' ? 'pill-verb' : (p === 'adjective' ? 'pill-adj' : (p === 'adverb' ? 'pill-adv' : 'pill-noun'));
  return `<span class="pill ${cls}">${p}</span>`;
}

function renderPreviewTable() {
  const thead = document.getElementById('previewThead');
  const tbody = document.getElementById('previewTbody');
  const q = (document.getElementById('searchPreviewInput').value || '').toLowerCase().trim();

  if (activePreviewTab === 'nonwords') {
    thead.innerHTML = '<tr><th>ID</th><th>Non-Word (Editable)</th><th>Logic</th><th>Source Word 1</th><th>Source Word 2</th><th>POS</th><th>NW Syl</th><th>SW1 Syl</th><th>SW2 Syl</th><th>Transformation</th><th>Key</th></tr>';
    const rows = generatedNonWords.filter(r => !q || `${r.nonword} ${r.source_word_1} ${r.source_word_2} ${r.logic} ${r.pos}`.toLowerCase().includes(q));
    tbody.innerHTML = rows.map((r, i) => `
      <tr>
        <td>${r.id}</td>
        <td><input class="editable-cell kn" value="${escHtml(r.nonword)}" onchange="editGeneratedNonword('${r.id}', this.value)"></td>
        <td>${escHtml(r.logic)}</td>
        <td class="kn">${escHtml(r.source_word_1)}</td>
        <td class="kn">${escHtml(r.source_word_2)}</td>
        <td>${posPill(r.pos)}</td>
        <td>${r.nw_syllables}</td>
        <td>${r.sw1_syllables}</td>
        <td>${r.sw2_syllables}</td>
        <td>${escHtml(r.transformation)}</td>
        <td><span class="pill pill-pseudo">${r.expected_key}</span></td>
      </tr>
    `).join('');
  } else if (activePreviewTab === 'master') {
    thead.innerHTML = '<tr><th>ID</th><th>Word</th><th>Lexicality</th><th>POS</th><th>Logic</th><th>Source 1</th><th>Source 2</th><th>Word Syl</th><th>SW1 Syl</th><th>SW2 Syl</th><th>Meaning / Transform</th></tr>';
    const rows = masterCorpus.filter(r => !q || `${r.word} ${r.lexicality} ${r.pos} ${r.logic} ${r.meaning}`.toLowerCase().includes(q));
    tbody.innerHTML = rows.map(r => `
      <tr>
        <td>${r.id}</td>
        <td class="kn">${escHtml(r.word)}</td>
        <td><span class="pill ${r.type==='real'?'pill-real':'pill-pseudo'}">${r.lexicality}</span></td>
        <td>${posPill(r.pos)}</td>
        <td>${escHtml(r.logic)}</td>
        <td class="kn">${escHtml(r.source_word_1)}</td>
        <td class="kn">${escHtml(r.source_word_2)}</td>
        <td>${r.syllables}</td>
        <td>${r.sw1_syllables}</td>
        <td>${r.sw2_syllables}</td>
        <td>${escHtml(r.meaning || r.transformation)}</td>
      </tr>
    `).join('');
  } else {
    const sId = document.getElementById('sessionSelectPreview').value || '1';
    const seq = generatedSessions[sId] || [];
    thead.innerHTML = '<tr><th>Trial #</th><th>Word</th><th>Lexicality</th><th>POS</th><th>Logic</th><th>Syllables</th><th>Expected Key</th></tr>';
    const rows = seq.filter(r => !q || `${r.word} ${r.lexicality} ${r.pos}`.toLowerCase().includes(q));
    tbody.innerHTML = rows.map(r => `
      <tr>
        <td>${r.trial}</td>
        <td class="kn">${escHtml(r.word)}</td>
        <td><span class="pill ${r.type==='real'?'pill-real':'pill-pseudo'}">${r.lexicality}</span></td>
        <td>${posPill(r.pos)}</td>
        <td>${escHtml(r.logic)}</td>
        <td>${r.syllables}</td>
        <td><span class="pill ${r.type==='real'?'pill-real':'pill-pseudo'}">${r.expected_key}</span></td>
      </tr>
    `).join('');
  }
}

function editGeneratedNonword(id, newVal) {
  const item = generatedNonWords.find(x => x.id === id);
  if (item) {
    item.nonword = newVal.trim();
    item.nw_syllables = countSyllables(item.nonword);
    const m = masterCorpus.find(x => x.id === id);
    if (m) { m.word = item.nonword; m.syllables = item.nw_syllables; }
    renderPreviewTable();
  }
}

// =========================================================================
// 100% Offline CSV & Genuine Multi-Sheet Excel (.xlsx) Generator (Zero CDN)
// =========================================================================
function exportCSV(kind) {
  let rows = [];
  if (kind === 'nonwords') {
    rows.push(['Nonword ID','Non-Word','Logic','Source Word 1','Source Word 2','POS','Non-Word Syllables','Source 1 Syllables','Source 2 Syllables','Transformation','Expected Key']);
    generatedNonWords.forEach(r => rows.push([r.id, r.nonword, r.logic, r.source_word_1, r.source_word_2, r.pos, r.nw_syllables, r.sw1_syllables, r.sw2_syllables, r.transformation, r.expected_key]));
  } else {
    rows.push(['ID','Word','Lexicality','POS','Logic','Source Word 1','Source Word 2','Word Syllables','Source 1 Syllables','Source 2 Syllables','Meaning / Transformation','Expected Key']);
    masterCorpus.forEach(r => rows.push([r.id, r.word, r.lexicality, r.pos, r.logic, r.source_word_1, r.source_word_2, r.syllables, r.sw1_syllables, r.sw2_syllables, r.meaning || r.transformation, r.expected_key]));
  }
  const csvStr = '\uFEFF' + rows.map(row => row.map(v => `"${String(v ?? '').replace(/"/g, '""')}"`).join(',')).join('\r\n');
  downloadBlob(new Blob([csvStr], { type: 'text/csv;charset=utf-8;' }), kind === 'nonwords' ? 'kannada_nonwords.csv' : 'kannada_master_corpus.csv');
}

function exportOfflineXLSX() {
  const sheets = [
    {
      name: 'Non-Words',
      rows: [
        ['Nonword ID','Non-Word (ಕನ್ನಡ)','Transformation Method','Source Word 1','Source Word 2','Source POS','Transformation Details','Non-Word Syllables','Source Word 1 Syllables','Source Word 2 Syllables','Expected Key','Arrow Color'],
        ...generatedNonWords.map(r => [r.id, r.nonword, r.logic, r.source_word_1, r.source_word_2, r.pos, r.transformation, r.nw_syllables, r.sw1_syllables, r.sw2_syllables, r.expected_key, r.arrow_color])
      ]
    },
    {
      name: 'Real Words',
      rows: [
        ['Word ID','Kannada Word','POS','Syllables','Meaning','Age Band'],
        ...realWords.map((r, i) => [r.id || `R${i+1}`, r.word, r.pos, countSyllables(r.word), r.meaning || '', r.age_band || ''])
      ]
    },
    {
      name: 'Master Corpus',
      rows: [
        ['ID','Word','Lexicality','POS','Logic','Source Word 1','Source Word 2','Word Syllables','Source 1 Syllables','Source 2 Syllables','Meaning / Transformation','Expected Key'],
        ...masterCorpus.map(r => [r.id, r.word, r.lexicality, r.pos, r.logic, r.source_word_1, r.source_word_2, r.syllables, r.sw1_syllables, r.sw2_syllables, r.meaning || r.transformation, r.expected_key])
      ]
    }
  ];
  Object.keys(generatedSessions).forEach(sId => {
    sheets.push({
      name: `Session ${sId}`,
      rows: [
        ['Trial #','Word','Lexicality','POS','Logic','Syllables','Expected Key'],
        ...generatedSessions[sId].map(r => [r.trial, r.word, r.lexicality, r.pos, r.logic, r.syllables, r.expected_key])
      ]
    });
  });

  const xlsxBytes = buildMinimalXLSX(sheets);
  downloadBlob(new Blob([xlsxBytes], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }), 'kannada_nonwords_studio_export.xlsx');
}

function xmlEsc(s) {
  return String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function colName(idx) {
  let s = '';
  let n = idx + 1;
  while (n > 0) {
    const r = (n - 1) % 26;
    s = String.fromCharCode(65 + r) + s;
    n = Math.floor((n - 1) / 26);
  }
  return s;
}

function sheetToXML(rows) {
  const rowXml = rows.map((row, rIdx) => {
    const cells = row.map((val, cIdx) => {
      const ref = colName(cIdx) + (rIdx + 1);
      if (typeof val === 'number' && !Number.isNaN(val)) {
        return `<c r="${ref}"><v>${val}</v></c>`;
      }
      return `<c r="${ref}" t="inlineStr"><is><t>${xmlEsc(val)}</t></is></c>`;
    }).join('');
    return `<row r="${rIdx + 1}">${cells}</row>`;
  }).join('');
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>${rowXml}</sheetData></worksheet>`;
}

function buildMinimalXLSX(sheets) {
  const files = [];
  const overrides = sheets.map((_, i) => `<Override PartName="/xl/worksheets/sheet${i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`).join('');
  files.push({
    name: '[Content_Types].xml',
    data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>${overrides}</Types>`
  });
  files.push({
    name: '_rels/.rels',
    data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>`
  });
  const sheetTags = sheets.map((s, i) => `<sheet name="${xmlEsc(s.name)}" sheetId="${i+1}" r:id="rId${i+1}"/>`).join('');
  files.push({
    name: 'xl/workbook.xml',
    data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>${sheetTags}</sheets></workbook>`
  });
  const relTags = sheets.map((_, i) => `<Relationship Id="rId${i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet${i+1}.xml"/>`).join('');
  files.push({
    name: 'xl/_rels/workbook.xml.rels',
    data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${relTags}</Relationships>`
  });
  sheets.forEach((s, i) => {
    files.push({ name: `xl/worksheets/sheet${i+1}.xml`, data: sheetToXML(s.rows) });
  });
  return buildZipStore(files);
}

// Pure JS Uncompressed ZIP (STORE) with CRC32
const CRC_TABLE = (() => {
  const t = new Uint32Array(256);
  for (let i = 0; i < 256; i++) {
    let c = i;
    for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    t[i] = c >>> 0;
  }
  return t;
})();

function crc32(bytes) {
  let crc = 0xFFFFFFFF;
  for (let i = 0; i < bytes.length; i++) crc = CRC_TABLE[(crc ^ bytes[i]) & 0xFF] ^ (crc >>> 8);
  return (crc ^ 0xFFFFFFFF) >>> 0;
}

function buildZipStore(entries) {
  const enc = new TextEncoder();
  const localParts = [];
  const centralParts = [];
  let offset = 0;

  entries.forEach(entry => {
    const nameBytes = enc.encode(entry.name);
    const dataBytes = enc.encode(entry.data);
    const crc = crc32(dataBytes);

    const lh = new ArrayBuffer(30);
    const lv = new DataView(lh);
    lv.setUint32(0, 0x04034b50, true);
    lv.setUint16(4, 20, true);
    lv.setUint16(8, 0, true);
    lv.setUint32(14, crc, true);
    lv.setUint32(18, dataBytes.length, true);
    lv.setUint32(22, dataBytes.length, true);
    lv.setUint16(26, nameBytes.length, true);

    localParts.push(new Uint8Array(lh), nameBytes, dataBytes);

    const ch = new ArrayBuffer(46);
    const cv = new DataView(ch);
    cv.setUint32(0, 0x02014b50, true);
    cv.setUint16(4, 20, true);
    cv.setUint16(6, 20, true);
    cv.setUint32(16, crc, true);
    cv.setUint32(20, dataBytes.length, true);
    cv.setUint32(24, dataBytes.length, true);
    cv.setUint16(28, nameBytes.length, true);
    cv.setUint32(42, offset, true);

    centralParts.push(new Uint8Array(ch), nameBytes);
    offset += 30 + nameBytes.length + dataBytes.length;
  });

  const centralSize = centralParts.reduce((a, b) => a + b.length, 0);
  const eocd = new ArrayBuffer(22);
  const ev = new DataView(eocd);
  ev.setUint32(0, 0x06054b50, true);
  ev.setUint16(8, entries.length, true);
  ev.setUint16(10, entries.length, true);
  ev.setUint32(12, centralSize, true);
  ev.setUint32(16, offset, true);

  const totalLen = offset + centralSize + 22;
  const out = new Uint8Array(totalLen);
  let pos = 0;
  [...localParts, ...centralParts, new Uint8Array(eocd)].forEach(part => {
    out.set(part, pos);
    pos += part.length;
  });
  return out;
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.style.display = 'none';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 5000);
}

function escHtml(s) {
  return String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// =========================================================================
// Python Script Viewer & Downloader (with Mobile Chrome Clipboard Fallback)
// =========================================================================
function copyPythonScript() {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(PYTHON_SCRIPT_TEXT)
      .then(() => alert('Complete Python script copied to clipboard!'))
      .catch(() => fallbackCopy(PYTHON_SCRIPT_TEXT));
  } else {
    fallbackCopy(PYTHON_SCRIPT_TEXT);
  }
}
function fallbackCopy(text) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  try {
    document.execCommand('copy');
    alert('Complete Python script copied to clipboard!');
  } catch (e) {
    alert('Please tap "Download .py File" to save the script.');
  }
  document.body.removeChild(ta);
}
function downloadPythonScript() {
  downloadBlob(new Blob([PYTHON_SCRIPT_TEXT], { type: 'text/x-python;charset=utf-8;' }), 'kannada_nonword_generator.py');
}

// Initialize on load
window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('pythonCodeBlock').textContent = PYTHON_SCRIPT_TEXT;
  updateRealWordStats();
  renderLogics();
  generateEverything();
});
</script>
</body>
</html>
'''

html_out = html_template.replace("__REAL_WORDS_JSON__", real_words_json).replace("__PYTHON_SCRIPT_JSON__", combined_py_json)

for dest in [
    REPO / "kannada_nonword_studio.html",
    REPO / "public" / "kannada_nonword_studio.html",
    Path(r"C:\Users\User\Downloads\kannada_nonword_studio.html"),
    Path(r"C:\Users\User\.gemini\antigravity\brain\384e9f2d-2c0d-4f84-a3bf-138e1df437bd\kannada_nonword_studio.html"),
]:
    dest.write_text(html_out, encoding="utf-8")
    print(f"Wrote {dest} ({len(html_out)} bytes)")
