"""
Patches dashboard.html to replace all fetch('/api/...') calls with
pure localStorage equivalents. Zero backend required after this patch.
"""
import re, os, sys

DASH = r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\public\dashboard.html"

with open(DASH, 'r', encoding='utf-8') as f:
    html = f.read()

# Find script block
script_start = html.index('<script>')
script_end   = html.rindex('</script>') + len('</script>')
pre  = html[:script_start]
post = html[script_end:]

# ---------------------------------------------------------------------------
# NEW PURE-FRONTEND SCRIPT BLOCK
# ---------------------------------------------------------------------------
NEW_SCRIPT = r"""<script>
// ============================================================
// ROAR Dashboard — Pure Frontend Engine (localStorage / static)
// ============================================================

const LS = {
  get: (k, def=[]) => { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : def; } catch(_){ return def; } },
  set: (k, v)      => { try { localStorage.setItem(k, JSON.stringify(v)); } catch(_){} },
  del: (k)         => { try { localStorage.removeItem(k); } catch(_){} }
};

// ---- Data accessors -------------------------------------------------------
const getStudents  = ()  => LS.get('studentsRoster', []);
const setStudents  = (a) => LS.set('studentsRoster', a);
const getSettings  = ()  => LS.get('roarSettings', {
  stimulusDisplayMode: 'infinite', stimulusTimeMs: 10000, trialTimeoutMs: 12000,
  fixationTimeMs: 1000, practiceCount: 5, wordsPerSession: 90, audioFeedback: true
});
const setSettings  = (s) => LS.set('roarSettings', s);
const getResults   = ()  => LS.get('roarTrialResults', []);
const clearResultsLS = () => { LS.del('roarTrialResults'); LS.del('roarSessionComplete'); };
const getWordEdits = ()  => LS.get('roarWordEdits', {});   // { "session-N-idx": {word,type} }
const setWordEdits = (e) => LS.set('roarWordEdits', e);

// ---- State ----------------------------------------------------------------
let allStudents   = [];
let allSessionsData = {};
let currentWordSession = 1;
let activeStudentEdit  = null;
let importWordSession  = 1;
let pendingImportWords = [];
let wordSearchQuery    = '';

// ---- Toast ----------------------------------------------------------------
function showToast(msg, type='success') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast-' + type;
  t.style.display = 'block';
  setTimeout(() => { t.style.display = 'none'; }, 3200);
}

// ---- Tab navigation -------------------------------------------------------
function switchTab(id) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === id));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.toggle('active', c.id === 'tab-' + id));
  if (id === 'roster')   loadStudentsTab();
  if (id === 'wordbank') loadWordBankTab();
  if (id === 'results')  loadResultsTab();
  if (id === 'settings') loadSettingsTab();
}

// ===========================================================================
// TAB 1 — Children & Test Sessions
// ===========================================================================
function loadStudentsTab() {
  allStudents = getStudents();
  renderStudentTable();
}

function renderStudentTable() {
  const tbody = document.getElementById('studentTableBody');
  if (!tbody) return;
  if (!allStudents.length) {
    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:var(--text-muted);padding:2rem;">No sessions registered. Add a child below.</td></tr>';
    return;
  }
  tbody.innerHTML = allStudents.map((s, i) => `
    <tr>
      <td><code style="font-size:0.8rem;color:var(--accent)">${esc(s.id)}</code></td>
      <td>${esc(s.name)}</td>
      <td>${esc(s.grade || '—')}</td>
      <td><span class="badge badge-${s.session <= 3 ? 'blue':'green'}">Session ${esc(String(s.session || 1))}</span></td>
      <td><span class="badge badge-${statusBadge(s.status)}">${esc(s.status || 'Pending')}</span></td>
      <td style="display:flex;gap:0.4rem;flex-wrap:wrap;">
        <button class="btn btn-sm btn-primary" onclick="launchGame(${i})">Launch</button>
        <button class="btn btn-sm" onclick="editStudent(${i})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteStudent(${i})">Delete</button>
      </td>
    </tr>`).join('');
}

function statusBadge(s) {
  if (!s || s === 'Pending') return 'gray';
  if (s === 'In Progress')   return 'yellow';
  if (s === 'Completed')     return 'green';
  return 'gray';
}

function launchGame(idx) {
  const s = allStudents[idx];
  if (!s) return;
  const url = `/?consent=false&storyoption=false&participant=${encodeURIComponent(s.id)}&session=${s.session || 1}`;
  // mark in-progress
  s.status = 'In Progress';
  allStudents[idx] = s;
  setStudents(allStudents);
  renderStudentTable();
  window.open(url, '_blank');
}

function editStudent(idx) {
  const s = allStudents[idx];
  if (!s) return;
  activeStudentEdit = idx;
  document.getElementById('editStudentId').value   = s.id;
  document.getElementById('editStudentName').value  = s.name;
  document.getElementById('editStudentGrade').value = s.grade || '';
  document.getElementById('editStudentSession').value = s.session || 1;
  document.getElementById('editStudentModal').style.display = 'flex';
}

function closeEditModal() {
  document.getElementById('editStudentModal').style.display = 'none';
  activeStudentEdit = null;
}

function saveEditStudent() {
  if (activeStudentEdit === null) return;
  const s = allStudents[activeStudentEdit];
  s.name    = document.getElementById('editStudentName').value.trim();
  s.grade   = document.getElementById('editStudentGrade').value.trim();
  s.session = parseInt(document.getElementById('editStudentSession').value) || 1;
  setStudents(allStudents);
  closeEditModal();
  renderStudentTable();
  showToast('Child record updated.');
}

function deleteStudent(idx) {
  if (!confirm('Delete this child record?')) return;
  allStudents.splice(idx, 1);
  setStudents(allStudents);
  renderStudentTable();
  showToast('Record deleted.', 'warning');
}

function registerStudent() {
  const id    = document.getElementById('newStudentId').value.trim();
  const name  = document.getElementById('newStudentName').value.trim();
  const grade = document.getElementById('newStudentGrade').value.trim();
  const sess  = parseInt(document.getElementById('newStudentSession').value) || 1;
  if (!id || !name) { showToast('ID and Name are required.', 'error'); return; }
  if (allStudents.find(s => s.id === id)) { showToast('ID already exists.', 'error'); return; }
  allStudents.push({ id, name, grade, session: sess, status: 'Pending', registeredAt: new Date().toISOString() });
  setStudents(allStudents);
  ['newStudentId','newStudentName','newStudentGrade'].forEach(f => document.getElementById(f).value = '');
  document.getElementById('newStudentSession').value = '1';
  renderStudentTable();
  showToast('Child registered successfully.');
}

function markComplete(idx) {
  allStudents[idx].status = 'Completed';
  setStudents(allStudents);
  renderStudentTable();
  showToast('Marked as Completed.');
}

// ===========================================================================
// TAB 2 — Word Bank & Datasets
// ===========================================================================
async function loadWordBankTab() {
  if (!Object.keys(allSessionsData).length) {
    try {
      const res = await fetch('/sessions_data.json');
      allSessionsData = await res.json();
      // Merge any localStorage edits on top
      const edits = getWordEdits();
      Object.keys(edits).forEach(k => {
        const [, sesN, idxStr] = k.split('-');
        const sesKey = 'session' + sesN;
        if (allSessionsData[sesKey] && allSessionsData[sesKey][parseInt(idxStr)]) {
          Object.assign(allSessionsData[sesKey][parseInt(idxStr)], edits[k]);
        }
      });
    } catch(e) { showToast('Could not load sessions_data.json', 'error'); return; }
  }
  renderWordBank();
}

function renderWordBank() {
  renderSessionPills();
  renderWordTable();
  updateWordCounts();
}

function renderSessionPills() {
  const container = document.getElementById('sessionPills');
  if (!container) return;
  container.innerHTML = [1,2,3,4,5,6].map(n => `
    <button class="pill ${currentWordSession === n ? 'active' : ''}" onclick="switchWordSession(${n})">Session ${n}</button>
  `).join('');
}

function switchWordSession(n) {
  currentWordSession = n;
  wordSearchQuery = '';
  if (document.getElementById('wordSearch')) document.getElementById('wordSearch').value = '';
  renderWordBank();
}

function updateWordCounts() {
  const sesKey = 'session' + currentWordSession;
  const words  = allSessionsData[sesKey] || [];
  const real   = words.filter(w => w.type === 'real' || w.type === 'word').length;
  const pseudo = words.filter(w => w.type === 'pseudo' || w.type === 'nonword').length;
  const demo   = words.filter(w => w.type === 'demo' || w.type === 'practice').length;
  const el = document.getElementById('wordCountBadge');
  if (el) el.textContent = `${words.length} words · ${real} real · ${pseudo} pseudo · ${demo} demo`;
}

function renderWordTable() {
  const tbody = document.getElementById('wordTableBody');
  if (!tbody) return;
  const sesKey = 'session' + currentWordSession;
  let words = (allSessionsData[sesKey] || []);
  if (wordSearchQuery) {
    const q = wordSearchQuery.toLowerCase();
    words = words.filter(w => (w.word||w.text||'').toLowerCase().includes(q) || (w.type||'').toLowerCase().includes(q));
  }
  if (!words.length) {
    tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:var(--text-muted);padding:1.5rem;">No words found.</td></tr>';
    return;
  }
  tbody.innerHTML = words.map((w, i) => {
    const word = w.word || w.text || '';
    const type = w.type || 'real';
    const sesKey2 = 'session' + currentWordSession;
    const realIdx = (allSessionsData[sesKey2] || []).indexOf(w);
    return `<tr>
      <td class="kannada-text" style="font-size:1.1rem;letter-spacing:0.02em">${esc(word)}</td>
      <td><span class="badge badge-${type==='real'||type==='word'?'blue':type==='demo'||type==='practice'?'green':'yellow'}">${esc(type)}</span></td>
      <td>${esc(String(w.audio || w.audioFile || '—'))}</td>
      <td style="display:flex;gap:0.4rem;">
        <button class="btn btn-sm" onclick="editWord(${realIdx})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteWord(${realIdx})">Delete</button>
      </td>
    </tr>`;
  }).join('');
}

function searchWords(q) {
  wordSearchQuery = q;
  renderWordTable();
}

function editWord(idx) {
  const sesKey = 'session' + currentWordSession;
  const w = (allSessionsData[sesKey] || [])[idx];
  if (!w) return;
  document.getElementById('editWordIndex').value = idx;
  document.getElementById('editWordValue').value  = w.word || w.text || '';
  document.getElementById('editWordType').value   = w.type || 'real';
  document.getElementById('editWordModal').style.display = 'flex';
}

function closeEditWordModal() {
  document.getElementById('editWordModal').style.display = 'none';
}

function saveEditWord() {
  const idx  = parseInt(document.getElementById('editWordIndex').value);
  const word = document.getElementById('editWordValue').value.trim();
  const type = document.getElementById('editWordType').value;
  if (!word) { showToast('Word cannot be empty.', 'error'); return; }
  const sesKey = 'session' + currentWordSession;
  if (!allSessionsData[sesKey]) return;
  allSessionsData[sesKey][idx].word = word;
  allSessionsData[sesKey][idx].text = word;
  allSessionsData[sesKey][idx].type = type;
  // persist edit
  const edits = getWordEdits();
  edits[`session-${currentWordSession}-${idx}`] = { word, type };
  setWordEdits(edits);
  closeEditWordModal();
  renderWordTable();
  showToast('Word updated.');
}

function deleteWord(idx) {
  if (!confirm('Delete this word?')) return;
  const sesKey = 'session' + currentWordSession;
  allSessionsData[sesKey].splice(idx, 1);
  renderWordBank();
  showToast('Word deleted.', 'warning');
}

function addWord() {
  const word = document.getElementById('newWordValue').value.trim();
  const type = document.getElementById('newWordType').value;
  if (!word) { showToast('Word cannot be empty.', 'error'); return; }
  const sesKey = 'session' + currentWordSession;
  if (!allSessionsData[sesKey]) allSessionsData[sesKey] = [];
  allSessionsData[sesKey].push({ word, text: word, type, audio: '' });
  document.getElementById('newWordValue').value = '';
  renderWordBank();
  showToast('Word added to Session ' + currentWordSession);
}

// ---- Excel / CSV Import ----
function openImportModal() {
  document.getElementById('importModal').style.display = 'flex';
  pendingImportWords = [];
  document.getElementById('importPreviewBody').innerHTML = '';
  document.getElementById('importPreviewSection').style.display = 'none';
  document.getElementById('importFileInput').value = '';
}
function closeImportModal() {
  document.getElementById('importModal').style.display = 'none';
}

function handleImportFile(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      let words = [];
      if (file.name.endsWith('.csv')) {
        // CSV parse
        const text = e.target.result;
        const lines = text.split(/\r?\n/).filter(l => l.trim());
        lines.forEach((line, i) => {
          if (i === 0 && (line.toLowerCase().includes('word') || line.toLowerCase().includes('type'))) return; // skip header
          const cols = line.split(',').map(c => c.trim().replace(/^"|"$/g,''));
          if (cols[0]) words.push({ word: cols[0], text: cols[0], type: cols[1] || 'real' });
        });
      } else {
        // Excel via SheetJS
        const data  = new Uint8Array(e.target.result);
        const wb    = XLSX.read(data, { type: 'array' });
        const ws    = wb.Sheets[wb.SheetNames[0]];
        const rows  = XLSX.utils.sheet_to_json(ws, { header: 1 });
        let headerRow = 0;
        // find header row
        for (let i = 0; i < Math.min(5, rows.length); i++) {
          if (rows[i] && rows[i].some(c => typeof c === 'string' && c.toLowerCase().includes('word'))) { headerRow = i; break; }
        }
        const headers = (rows[headerRow] || []).map(h => String(h||'').toLowerCase().trim());
        const wordCol = headers.findIndex(h => h.includes('word') || h.includes('stimulus'));
        const typeCol = headers.findIndex(h => h.includes('type') || h.includes('category') || h.includes('class'));
        for (let i = headerRow + 1; i < rows.length; i++) {
          const row = rows[i] || [];
          const word = String(row[wordCol >= 0 ? wordCol : 0] || '').trim();
          const type = typeCol >= 0 ? String(row[typeCol] || 'real').toLowerCase().trim() : 'real';
          if (word) words.push({ word, text: word, type: ['real','pseudo','demo','word','nonword','practice'].includes(type) ? type : 'real' });
        }
      }
      pendingImportWords = words;
      renderImportPreview(words);
    } catch(err) {
      showToast('Error parsing file: ' + err.message, 'error');
    }
  };
  if (file.name.endsWith('.csv')) reader.readAsText(file);
  else reader.readAsArrayBuffer(file);
}

function renderImportPreview(words) {
  const tbody = document.getElementById('importPreviewBody');
  if (!words.length) { tbody.innerHTML = '<tr><td colspan="2" style="text-align:center;color:var(--text-muted)">No words found.</td></tr>'; return; }
  tbody.innerHTML = words.slice(0, 50).map(w => `<tr>
    <td class="kannada-text">${esc(w.word)}</td>
    <td><span class="badge badge-${w.type==='real'||w.type==='word'?'blue':w.type==='demo'?'green':'yellow'}">${esc(w.type)}</span></td>
  </tr>`).join('') + (words.length > 50 ? `<tr><td colspan="2" style="text-align:center;color:var(--text-muted)">... and ${words.length - 50} more</td></tr>` : '');
  document.getElementById('importPreviewSection').style.display = 'block';
  document.getElementById('importWordCount').textContent = words.length + ' words found';
}

function commitExcelImport() {
  if (!pendingImportWords.length) { showToast('No words to import.', 'warning'); return; }
  const sesKey = 'session' + importWordSession;
  if (!allSessionsData[sesKey]) allSessionsData[sesKey] = [];
  pendingImportWords.forEach(w => allSessionsData[sesKey].push(w));
  closeImportModal();
  if (currentWordSession !== importWordSession) switchWordSession(importWordSession);
  else renderWordBank();
  showToast(`Imported ${pendingImportWords.length} words to Session ${importWordSession}.`);
  pendingImportWords = [];
}

// ===========================================================================
// TAB 3 — Assessment Results
// ===========================================================================
function loadResultsTab() {
  const results = getResults();
  renderResultsTable(results);
  renderResultsMetrics(results);
}

function renderResultsMetrics(results) {
  const total   = results.length;
  const correct = results.filter(r => r.correct).length;
  const acc     = total ? Math.round(correct / total * 100) : 0;
  const rts     = results.filter(r => r.rt > 0).map(r => r.rt);
  const meanRt  = rts.length ? Math.round(rts.reduce((a,b) => a+b, 0) / rts.length) : 0;
  const sessions = [...new Set(results.map(r => r.session))];

  const el = document.getElementById('resultsMetrics');
  if (!el) return;
  el.innerHTML = `
    <div class="metric-card"><div class="metric-val">${total}</div><div class="metric-label">Total Trials</div></div>
    <div class="metric-card"><div class="metric-val">${correct}</div><div class="metric-label">Correct</div></div>
    <div class="metric-card"><div class="metric-val">${acc}%</div><div class="metric-label">Accuracy</div></div>
    <div class="metric-card"><div class="metric-val">${meanRt}ms</div><div class="metric-label">Mean RT</div></div>
    <div class="metric-card"><div class="metric-val">${sessions.length}</div><div class="metric-label">Sessions</div></div>
  `;
}

function renderResultsTable(results) {
  const tbody = document.getElementById('resultsTableBody');
  if (!tbody) return;
  if (!results.length) {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--text-muted);padding:2rem;">No results yet. Launch a game session to capture data.</td></tr>';
    return;
  }
  tbody.innerHTML = results.slice(-200).reverse().map(r => `
    <tr>
      <td>${esc(r.participant||'—')}</td>
      <td>${esc(String(r.session||'—'))}</td>
      <td class="kannada-text">${esc(r.word||'—')}</td>
      <td>${esc(r.stage||'—')}</td>
      <td><span class="badge badge-${r.correct?'green':'danger'}">${r.correct ? 'Correct' : 'Incorrect'}</span></td>
      <td>${r.rt ? r.rt + 'ms' : '—'}</td>
      <td style="font-size:0.75rem;color:var(--text-muted)">${r.ts ? new Date(r.ts).toLocaleTimeString() : '—'}</td>
    </tr>`).join('');
}

function exportCSV() {
  const results = getResults();
  if (!results.length) { showToast('No results to export.', 'warning'); return; }
  const cols = ['participant','session','stage','word','correct','rt','response','trial_index','ts'];
  const lines = [cols.join(',')].concat(results.map(r =>
    cols.map(c => { const v = r[c]; return typeof v === 'string' && v.includes(',') ? '"' + v + '"' : (v === undefined ? '' : v); }).join(',')
  ));
  const blob = new Blob([lines.join('\n')], { type: 'text/csv;charset=utf-8;' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href = url; a.download = 'roar_results_' + new Date().toISOString().slice(0,10) + '.csv';
  a.click(); URL.revokeObjectURL(url);
  showToast('CSV exported successfully.');
}

function clearResults() {
  if (!confirm('Clear ALL trial results? This cannot be undone.')) return;
  clearResultsLS();
  loadResultsTab();
  showToast('Results cleared.', 'warning');
}

function refreshResults() {
  loadResultsTab();
  showToast('Results refreshed.');
}

// ===========================================================================
// TAB 4 — Engine Settings
// ===========================================================================
function loadSettingsTab() {
  const s = getSettings();
  const modeEl = document.getElementById('stimulusMode');
  if (modeEl) {
    modeEl.value = s.stimulusDisplayMode || 'infinite';
    toggleTimedFields(s.stimulusDisplayMode || 'infinite');
  }
  setValue('stimulusTimeMs',  s.stimulusTimeMs  || 10000);
  setValue('trialTimeoutMs',  s.trialTimeoutMs  || 12000);
  setValue('fixationTimeMs',  s.fixationTimeMs  || 1000);
  setValue('practiceCount',   s.practiceCount   || 5);
  setValue('wordsPerSession', s.wordsPerSession  || 90);
  const audioEl = document.getElementById('audioFeedback');
  if (audioEl) audioEl.checked = s.audioFeedback !== false;
}

function setValue(id, val) {
  const el = document.getElementById(id);
  if (el) el.value = val;
}

function toggleTimedFields(mode) {
  const wrap = document.getElementById('timedFieldsWrap');
  if (wrap) wrap.style.display = mode === 'timed' ? 'block' : 'none';
}

function saveSettings() {
  const mode = document.getElementById('stimulusMode')?.value || 'infinite';
  const s = {
    stimulusDisplayMode: mode,
    stimulusTimeMs:  parseInt(document.getElementById('stimulusTimeMs')?.value  || 10000),
    trialTimeoutMs:  parseInt(document.getElementById('trialTimeoutMs')?.value  || 12000),
    fixationTimeMs:  parseInt(document.getElementById('fixationTimeMs')?.value  || 1000),
    practiceCount:   parseInt(document.getElementById('practiceCount')?.value   || 5),
    wordsPerSession: parseInt(document.getElementById('wordsPerSession')?.value || 90),
    audioFeedback: document.getElementById('audioFeedback')?.checked !== false
  };
  setSettings(s);
  showToast('Settings saved. Next game launch will use these values.');
}

function resetSettings() {
  if (!confirm('Reset settings to defaults?')) return;
  LS.del('roarSettings');
  loadSettingsTab();
  showToast('Settings reset to defaults.', 'warning');
}

// ===========================================================================
// UTILS
// ===========================================================================
function esc(s) {
  if (s === undefined || s === null) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function copyLink(type) {
  const base = window.location.origin;
  const url  = type === 'game'
    ? base + '/?consent=false&storyoption=false'
    : base + '/dashboard.html';
  navigator.clipboard.writeText(url).then(() => showToast('Link copied: ' + url));
}

// ===========================================================================
// INIT
// ===========================================================================
document.addEventListener('DOMContentLoaded', () => {
  // Default active tab
  switchTab('roster');
});
</script>"""

# Replace the old script block
new_html = pre + NEW_SCRIPT + post

with open(DASH, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Dashboard patched. New size: {len(new_html)} chars")
print("API fetch calls remaining:", new_html.count("fetch('/api/"))
print("localStorage calls:", new_html.count("localStorage."))
