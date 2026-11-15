"""
Updates dashboard.html with:
1. Visual Shuffle Pattern Selector in Engine Settings
2. Master Corpus (All 540 Words: 270 Real + 270 Pseudo) in Word Bank Tab
3. Auto-distribute & session partitioning for full Excel imports
"""

DASH = r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\public\dashboard.html"

with open(DASH, 'r', encoding='utf-8') as f:
    html = f.read()

# -----------------------------------------------------------------------------
# 1. ADD SHUFFLE PATTERN SELECTOR TO SETTINGS FORM
# -----------------------------------------------------------------------------
shuffle_html = """
          <!-- Word Presentation & Shuffle Sequence -->
          <div class="form-group" style="margin-bottom: 1.5rem; background: #0b1120; padding: 1.25rem; border-radius: 6px; border: 1px solid var(--card-border);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
              <label class="form-label" style="font-weight: 600; color: #fff; margin-bottom: 0;">Word Presentation & Shuffle Sequence</label>
              <span id="activeShuffleLabel" class="badge badge-blue">Strict Alternating</span>
            </div>
            <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 1rem;">Choose how Real words and Non-Words (Pseudo-words) are ordered during child testing sessions:</div>

            <div style="display: grid; grid-template-columns: 1fr; gap: 0.75rem;">
              <!-- Option 1: Strict Alternating -->
              <label style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.85rem; border: 1px solid #334155; border-radius: 6px; cursor: pointer; background: #131d31;" onclick="updateShuffleLabel('Strict Alternating')">
                <input type="radio" name="shufflePattern" value="alternating" id="patternAlternating" checked style="margin-top: 0.25rem;">
                <div style="flex: 1;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <strong style="color: #38bdf8;">Strict Alternating (1 Real : 1 Non-Word)</strong>
                    <span class="badge badge-blue">Recommended</span>
                  </div>
                  <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.5rem;">Evenly alternates between real Kannada words and non-words. Prevents repeated motor response bias.</div>
                  <div style="display: flex; gap: 0.35rem; align-items: center; font-size: 0.7rem; font-family: monospace;">
                    <span style="background: #1e3a8a; color: #93c5fd; padding: 0.15rem 0.4rem; border-radius: 3px;">Real</span> &rarr; 
                    <span style="background: #854d0e; color: #fde047; padding: 0.15rem 0.4rem; border-radius: 3px;">Non-Word</span> &rarr; 
                    <span style="background: #1e3a8a; color: #93c5fd; padding: 0.15rem 0.4rem; border-radius: 3px;">Real</span> &rarr; 
                    <span style="background: #854d0e; color: #fde047; padding: 0.15rem 0.4rem; border-radius: 3px;">Non-Word</span> &rarr; 
                    <span style="background: #1e3a8a; color: #93c5fd; padding: 0.15rem 0.4rem; border-radius: 3px;">Real</span> &rarr; 
                    <span style="background: #854d0e; color: #fde047; padding: 0.15rem 0.4rem; border-radius: 3px;">Non-Word</span>
                  </div>
                </div>
              </label>

              <!-- Option 2: Constrained Balanced -->
              <label style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.85rem; border: 1px solid #334155; border-radius: 6px; cursor: pointer; background: #131d31;" onclick="updateShuffleLabel('Constrained Balanced')">
                <input type="radio" name="shufflePattern" value="constrained" id="patternConstrained" style="margin-top: 0.25rem;">
                <div style="flex: 1;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <strong style="color: #38bdf8;">Constrained Balanced (Max 2 in a Row)</strong>
                    <span class="badge badge-green">Psycholinguistic Standard</span>
                  </div>
                  <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.5rem;">Randomized trial order with a strict guardrail: never allows more than 2 consecutive real words or non-words.</div>
                  <div style="display: flex; gap: 0.35rem; align-items: center; font-size: 0.7rem; font-family: monospace;">
                    <span style="background: #1e3a8a; color: #93c5fd; padding: 0.15rem 0.4rem; border-radius: 3px;">Real</span> &rarr; 
                    <span style="background: #1e3a8a; color: #93c5fd; padding: 0.15rem 0.4rem; border-radius: 3px;">Real</span> &rarr; 
                    <span style="background: #854d0e; color: #fde047; padding: 0.15rem 0.4rem; border-radius: 3px;">Non-Word</span> &rarr; 
                    <span style="background: #1e3a8a; color: #93c5fd; padding: 0.15rem 0.4rem; border-radius: 3px;">Real</span> &rarr; 
                    <span style="background: #854d0e; color: #fde047; padding: 0.15rem 0.4rem; border-radius: 3px;">Non-Word</span> &rarr; 
                    <span style="background: #854d0e; color: #fde047; padding: 0.15rem 0.4rem; border-radius: 3px;">Non-Word</span>
                  </div>
                </div>
              </label>

              <!-- Option 3: Blocked Clusters -->
              <label style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.85rem; border: 1px solid #334155; border-radius: 6px; cursor: pointer; background: #131d31;" onclick="updateShuffleLabel('Block Clusters')">
                <input type="radio" name="shufflePattern" value="blocks" id="patternBlocks" style="margin-top: 0.25rem;">
                <div style="flex: 1;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <strong style="color: #38bdf8;">Block Clusters (Mini-blocks of 5)</strong>
                    <span class="badge badge-yellow">Categorical Practice</span>
                  </div>
                  <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.5rem;">Groups stimuli into blocks of 5 real words followed by 5 non-words throughout the session.</div>
                  <div style="display: flex; gap: 0.35rem; align-items: center; font-size: 0.7rem; font-family: monospace;">
                    <span style="background: #1e3a8a; color: #93c5fd; padding: 0.15rem 0.4rem; border-radius: 3px;">5x Real</span> &rarr; 
                    <span style="background: #854d0e; color: #fde047; padding: 0.15rem 0.4rem; border-radius: 3px;">5x Non-Word</span> &rarr; 
                    <span style="background: #1e3a8a; color: #93c5fd; padding: 0.15rem 0.4rem; border-radius: 3px;">5x Real</span> &rarr; 
                    <span style="background: #854d0e; color: #fde047; padding: 0.15rem 0.4rem; border-radius: 3px;">5x Non-Word</span>
                  </div>
                </div>
              </label>

              <!-- Option 4: Pure Random -->
              <label style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.85rem; border: 1px solid #334155; border-radius: 6px; cursor: pointer; background: #131d31;" onclick="updateShuffleLabel('Completely Random')">
                <input type="radio" name="shufflePattern" value="random" id="patternRandom" style="margin-top: 0.25rem;">
                <div style="flex: 1;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <strong style="color: #38bdf8;">Completely Random (Stanford ROAR Default)</strong>
                    <span class="badge badge-gray">Unconstrained</span>
                  </div>
                  <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.5rem;">Original 50/50 probability coin flip on every trial. May produce unpredictable streaks of 4+ consecutive real or non-words.</div>
                  <div style="display: flex; gap: 0.35rem; align-items: center; font-size: 0.7rem; font-family: monospace; color: var(--text-muted);">
                    <span>Random 50% Real / 50% Non-Word coin flip on each trial</span>
                  </div>
                </div>
              </label>
            </div>
          </div>
"""

save_btn_target = '<div style="margin-top: 1.5rem; display: flex; justify-content: flex-end;">'
if save_btn_target in html and 'Word Presentation & Shuffle Sequence' not in html:
    html = html.replace(save_btn_target, shuffle_html + '\n          ' + save_btn_target, 1)
    print("[1] Injected Shuffle Pattern Selector into Engine Settings HTML.")

# -----------------------------------------------------------------------------
# 2. UPDATE EXCEL TARGET SESSION DROPDOWN (ADD MASTER CORPUS)
# -----------------------------------------------------------------------------
excel_dropdown_old = """          <select class="form-control" id="excelTargetSession">
            <option value="1">Session 1</option>"""

excel_dropdown_new = """          <select class="form-control" id="excelTargetSession">
            <option value="master">Master Corpus (Complete 540 Words — Auto-Distribute across Sessions 1-6)</option>
            <option value="1">Session 1</option>"""

if excel_dropdown_old in html:
    html = html.replace(excel_dropdown_old, excel_dropdown_new, 1)
    print("[2] Added Master Corpus to Excel Import dropdown.")

# -----------------------------------------------------------------------------
# 3. UPDATE WORD BANK CONTROLS (ADD MASTER FILTER PILLS & CORPUS VIEW)
# -----------------------------------------------------------------------------
filter_bar_old = '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; gap: 1rem;">'
filter_bar_new = """<!-- Master Sub-Filters -->
        <div id="masterTypeFilterBar" style="display: none; gap: 0.5rem; margin-bottom: 1rem;">
          <button class="btn btn-sm btn-secondary active" id="btnFilterAll" onclick="setMasterTypeFilter('all')">All Words (540)</button>
          <button class="btn btn-sm btn-secondary" id="btnFilterReal" onclick="setMasterTypeFilter('real')">Real Words (270)</button>
          <button class="btn btn-sm btn-secondary" id="btnFilterPseudo" onclick="setMasterTypeFilter('pseudo')">Non-Words (270)</button>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; gap: 1rem;">"""

if filter_bar_old in html and 'id="masterTypeFilterBar"' not in html:
    html = html.replace(filter_bar_old, filter_bar_new, 1)
    print("[3] Added Master Corpus sub-filters to Word Bank HTML.")

# -----------------------------------------------------------------------------
# 4. REPLACE JAVASCRIPT BLOCK WITH ENHANCED SHUFFLE & MASTER CORPUS LOGIC
# -----------------------------------------------------------------------------
script_start = html.index('<script>')
script_end   = html.rindex('</script>') + len('</script>')
pre  = html[:script_start]
post = html[script_end:]

NEW_JS = r"""<script>
// ================================================================
//  ROAR Dashboard — Pure Frontend Engine (v8.0 Professional)
//  Includes Master Corpus (540 words) + Visual Shuffle Pattern Selector
// ================================================================

const LS = {
  get: function(k, def) {
    if (def === undefined) def = [];
    try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : def; } catch(e) { return def; }
  },
  set: function(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch(e) {} },
  del: function(k)    { try { localStorage.removeItem(k); } catch(e) {} }
};

function getStudents()  { return LS.get('studentsRoster', []); }
function setStudents(a) { LS.set('studentsRoster', a); }
function getSettings()  {
  return LS.get('roarSettings', {
    stimulusDisplayMode: 'infinite', stimulusTimeMs: 10000, trialTimeoutMs: 12000,
    fixationTimeMs: 1000, practiceCount: 5, wordsPerSession: 90,
    shufflePattern: 'alternating'
  });
}
function setSettings(s) { LS.set('roarSettings', s); }
function getResults()   { return LS.get('roarTrialResults', []); }

// State
var allStudents      = [];
var rawSessionsData  = {};
var currentSession   = 'master'; // 'master' | '1'..'6'
var masterTypeFilter = 'all';    // 'all' | 'real' | 'pseudo'
var editingWordId    = null;
var editingStudentId = null;
var pendingImport    = [];

// Toast
function showToast(msg, type) {
  type = type || 'success';
  var t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.className = '';
  t.style.cssText = 'display:block;position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;padding:0.75rem 1.25rem;border-radius:8px;font-size:0.875rem;font-weight:600;max-width:420px;';
  if (type === 'error')   t.style.background = '#ef4444';
  else if (type === 'warning') t.style.background = '#f59e0b';
  else t.style.background = '#10b981';
  t.style.color = '#fff';
  setTimeout(function() { t.style.display = 'none'; }, 3500);
}

// Tab navigation
function switchTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(function(b) { b.classList.remove('active'); });
  document.querySelectorAll('.tab-content').forEach(function(c) { c.classList.remove('active'); });
  document.querySelectorAll('.tab-btn').forEach(function(b) {
    if (b.getAttribute('onclick') && b.getAttribute('onclick').indexOf("'" + tabId + "'") !== -1) {
      b.classList.add('active');
    }
  });
  var tabEl = document.getElementById(tabId);
  if (tabEl) tabEl.classList.add('active');

  if (tabId === 'rosterTab')   initRosterTab();
  if (tabId === 'wordsTab')    initWordsTab();
  if (tabId === 'resultsTab')  initResultsTab();
  if (tabId === 'settingsTab') initSettingsTab();
}

// ================================================================
//  TAB 1 — Children & Test Sessions
// ================================================================
function initRosterTab() {
  allStudents = getStudents();
  renderStudentsTable();
  updateRosterMetrics();
}

function updateRosterMetrics() {
  var students = getStudents();
  var completed = students.filter(function(s) { return s.status === 'Completed'; }).length;
  var settings  = getSettings();
  var el1 = document.getElementById('countStudents');
  var el2 = document.getElementById('countCompleted');
  var el3 = document.getElementById('dispTimingMode');
  if (el1) el1.textContent = students.length;
  if (el2) el2.textContent = completed;
  if (el3) el3.textContent = settings.stimulusDisplayMode === 'timed'
    ? (settings.stimulusTimeMs / 1000).toFixed(1) + 's Timed'
    : 'Infinite';
}

function renderStudentsTable() {
  var tbody = document.getElementById('studentsTableBody');
  if (!tbody) return;
  var students = getStudents();
  if (!students.length) {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--text-muted);padding:2rem;">No children registered. Click "Register Child" to add one.</td></tr>';
    return;
  }
  var results = getResults();
  var accMap = {};
  results.forEach(function(r) {
    if (!accMap[r.participant]) accMap[r.participant] = { total: 0, correct: 0 };
    accMap[r.participant].total++;
    if (r.correct) accMap[r.participant].correct++;
  });

  tbody.innerHTML = students.map(function(s, i) {
    var acc = accMap[s.id] ? Math.round(accMap[s.id].correct / accMap[s.id].total * 100) + '%' : '—';
    var statusClass = s.status === 'Completed' ? 'badge-green' : s.status === 'In Progress' ? 'badge-yellow' : 'badge-gray';
    return '<tr>' +
      '<td><code style="font-size:0.8rem;color:var(--accent)">' + esc(s.id) + '</code></td>' +
      '<td>' + esc(s.name) + '</td>' +
      '<td>' + esc(s.grade || '—') + '</td>' +
      '<td><span class="badge badge-blue">Session ' + esc(String(s.session || 1)) + '</span></td>' +
      '<td><span class="badge ' + statusClass + '">' + esc(s.status || 'Pending') + '</span></td>' +
      '<td>' + esc(acc) + '</td>' +
      '<td style="display:flex;gap:0.4rem;flex-wrap:wrap;">' +
        '<button class="btn btn-primary btn-sm" onclick="launchGame(' + i + ')">Launch</button>' +
        '<button class="btn btn-sm" onclick="openEditStudent(' + i + ')">Edit</button>' +
        '<button class="btn btn-sm" style="background:var(--danger);color:#fff" onclick="deleteStudent(' + i + ')">Delete</button>' +
      '</td></tr>';
  }).join('');
}

function launchGame(idx) {
  var students = getStudents();
  var s = students[idx];
  if (!s) return;
  var url = '/?consent=false&storyoption=false&participant=' + encodeURIComponent(s.id) + '&session=' + (s.session || 1);
  s.status = 'In Progress';
  students[idx] = s;
  setStudents(students);
  renderStudentsTable();
  window.open(url, '_blank');
}

function openStudentModal() {
  editingStudentId = null;
  document.getElementById('studentModalTitle').textContent = 'Register New Child';
  document.getElementById('studentSubmitBtn').textContent  = 'Save Participant';
  document.getElementById('stuIdInput').value      = '';
  document.getElementById('stuNameInput').value    = '';
  document.getElementById('stuGradeInput').value   = 'Grade 1';
  document.getElementById('stuSessionInput').value = '1';
  document.getElementById('stuIdInput').disabled   = false;
  document.getElementById('studentModal').style.display = 'flex';
}

function openEditStudent(idx) {
  var students = getStudents();
  var s = students[idx];
  if (!s) return;
  editingStudentId = idx;
  document.getElementById('studentModalTitle').textContent = 'Edit Child Record';
  document.getElementById('studentSubmitBtn').textContent  = 'Update Participant';
  document.getElementById('stuIdInput').value      = s.id;
  document.getElementById('stuNameInput').value    = s.name;
  document.getElementById('stuGradeInput').value   = s.grade || 'Grade 1';
  document.getElementById('stuSessionInput').value = String(s.session || 1);
  document.getElementById('stuIdInput').disabled   = true;
  document.getElementById('studentModal').style.display = 'flex';
}

function closeStudentModal() {
  document.getElementById('studentModal').style.display = 'none';
  editingStudentId = null;
}

function handleStudentSubmit(event) {
  event.preventDefault();
  var id      = document.getElementById('stuIdInput').value.trim();
  var name    = document.getElementById('stuNameInput').value.trim();
  var grade   = document.getElementById('stuGradeInput').value;
  var session = parseInt(document.getElementById('stuSessionInput').value) || 1;
  if (!id || !name) { showToast('Participant ID and Name are required.', 'error'); return; }

  var students = getStudents();
  if (editingStudentId !== null) {
    students[editingStudentId].name    = name;
    students[editingStudentId].grade   = grade;
    students[editingStudentId].session = session;
    setStudents(students);
    closeStudentModal();
    allStudents = students;
    renderStudentsTable();
    showToast('Child record updated.');
  } else {
    if (students.find(function(s) { return s.id === id; })) {
      showToast('Participant ID already exists.', 'error'); return;
    }
    students.push({ id: id, name: name, grade: grade, session: session, status: 'Pending', registeredAt: new Date().toISOString() });
    setStudents(students);
    allStudents = students;
    closeStudentModal();
    renderStudentsTable();
    updateRosterMetrics();
    showToast('Child registered successfully.');
  }
}

function deleteStudent(idx) {
  if (!confirm('Delete this child record?')) return;
  var students = getStudents();
  students.splice(idx, 1);
  setStudents(students);
  allStudents = students;
  renderStudentsTable();
  updateRosterMetrics();
  showToast('Record deleted.', 'warning');
}

// ================================================================
//  TAB 2 — Word Bank & Master Corpus Management
// ================================================================
function initWordsTab() {
  var stored = LS.get('roarCustomSessionsData', null);
  if (stored) {
    rawSessionsData = stored;
    renderWordsTab();
    return;
  }
  fetch('/sessions_data.json')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      rawSessionsData = data;
      renderWordsTab();
    })
    .catch(function(e) { showToast('Could not load sessions_data.json', 'error'); });
}

function getMasterList() {
  var master = [];
  [1, 2, 3, 4, 5, 6].forEach(function(s) {
    var sesKey = String(s);
    var ses = rawSessionsData[sesKey] || {};
    (ses.real || []).forEach(function(w) {
      master.push(Object.assign({}, w, { session: s, type: 'real' }));
    });
    (ses.pseudo || []).forEach(function(w) {
      master.push(Object.assign({}, w, { session: s, type: 'pseudo' }));
    });
  });
  return master;
}

function getSessionList(s) {
  var ses = rawSessionsData[String(s)] || {};
  var list = [];
  (ses.demo || []).forEach(function(w) {
    list.push(Object.assign({}, w, { type: 'demo', session: s }));
  });
  (ses.real || []).forEach(function(w) {
    list.push(Object.assign({}, w, { type: 'real', session: s }));
  });
  (ses.pseudo || []).forEach(function(w) {
    list.push(Object.assign({}, w, { type: 'pseudo', session: s }));
  });
  return list;
}

function renderWordsTab() {
  updateSessionPills();
  renderWordsTable();
}

function updateSessionPills() {
  var pills = document.getElementById('sessionPills');
  if (!pills) return;
  var masterActive = currentSession === 'master' ? 'active' : '';
  var html = '<button class="session-pill ' + masterActive + '" style="font-weight:700;border-color:var(--accent);" onclick="selectSession(\'master\')">Master Corpus (540 Words)</button>';
  
  [1, 2, 3, 4, 5, 6].forEach(function(n) {
    var active = currentSession === String(n) ? 'active' : '';
    html += '<button class="session-pill ' + active + '" onclick="selectSession(\'' + n + '\')">Session ' + n + '</button>';
  });
  pills.innerHTML = html;

  var subBar = document.getElementById('masterTypeFilterBar');
  if (subBar) {
    subBar.style.display = currentSession === 'master' ? 'flex' : 'none';
  }
}

function selectSession(n) {
  currentSession = String(n);
  renderWordsTab();
}

function setMasterTypeFilter(f) {
  masterTypeFilter = f;
  ['btnFilterAll', 'btnFilterReal', 'btnFilterPseudo'].forEach(function(id) {
    var btn = document.getElementById(id);
    if (btn) btn.classList.remove('active');
  });
  if (f === 'all') document.getElementById('btnFilterAll')?.classList.add('active');
  if (f === 'real') document.getElementById('btnFilterReal')?.classList.add('active');
  if (f === 'pseudo') document.getElementById('btnFilterPseudo')?.classList.add('active');
  renderWordsTable();
}

function renderWordsTable() {
  var tbody = document.getElementById('wordsTableBody');
  if (!tbody) return;

  var isMaster = currentSession === 'master';
  var words = isMaster ? getMasterList() : getSessionList(currentSession);

  if (isMaster && masterTypeFilter !== 'all') {
    words = words.filter(function(w) { return w.type === masterTypeFilter; });
  }

  var q = (document.getElementById('wordSearchInput')?.value || '').toLowerCase().trim();
  if (q) {
    words = words.filter(function(w) {
      return (w.word||w.text||'').toLowerCase().includes(q) ||
             (w.type||'').toLowerCase().includes(q) ||
             (w.meaning||w.english||'').toLowerCase().includes(q) ||
             (w.transcription||w.ipa||'').toLowerCase().includes(q);
    });
  }

  var statsEl = document.getElementById('sessionStatsText');
  if (statsEl) {
    if (isMaster) {
      var totalReal = getMasterList().filter(function(w){return w.type==='real';}).length;
      var totalPseudo = getMasterList().filter(function(w){return w.type==='pseudo';}).length;
      statsEl.textContent = 'Showing ' + words.length + ' / 540 Master Words (' + totalReal + ' Real + ' + totalPseudo + ' Non-Words)';
    } else {
      var total = getSessionList(currentSession).length;
      statsEl.textContent = 'Showing ' + words.length + ' / ' + total + ' words in Session ' + currentSession;
    }
  }

  if (!words.length) {
    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:var(--text-muted);padding:1.5rem;">No words found matching criteria.</td></tr>';
    return;
  }

  tbody.innerHTML = words.map(function(w, idx) {
    var word = w.word || w.text || '';
    var type = w.type || 'real';
    var trans = w.transcription || w.ipa || '';
    var meaning = w.meaning || w.english || (w.source_word ? 'Source: ' + w.source_word : '');
    var typeBadge = type === 'real' ? 'badge-blue' : (type === 'demo' ? 'badge-green' : 'badge-yellow');
    var sesBadge = '<span class="badge badge-gray">Session ' + (w.session || 1) + '</span>';

    return '<tr>' +
      '<td style="font-size:0.75rem;color:var(--text-muted)">' + esc(String(idx + 1)) + '</td>' +
      '<td class="kannada-text" style="font-size:1.15rem;font-weight:600">' + esc(word) + '</td>' +
      '<td><span class="badge ' + typeBadge + '">' + esc(type === 'pseudo' ? 'Non-Word' : type) + '</span></td>' +
      '<td>' + (isMaster ? sesBadge : esc(trans)) + '</td>' +
      '<td style="font-size:0.8rem">' + esc(meaning || trans || '—') + '</td>' +
      '<td style="display:flex;gap:0.4rem">' +
        '<button class="btn btn-sm" onclick="openEditWord(' + idx + ', \'' + (w.id||'') + '\')">Edit</button>' +
        '<button class="btn btn-sm" style="background:var(--danger);color:#fff" onclick="deleteWord(' + idx + ', \'' + (w.id||'') + '\', \'' + (w.session||currentSession) + '\')">Delete</button>' +
      '</td></tr>';
  }).join('');
}

function filterWordsTable() { renderWordsTable(); }

function openAddWordModal() {
  editingWordId = null;
  document.getElementById('wordModalTitle').textContent = 'Add Kannada Word';
  document.getElementById('editWordId').value       = '';
  document.getElementById('wordTextInput').value    = '';
  document.getElementById('wordTransInput').value   = '';
  document.getElementById('wordMeaningInput').value = '';
  document.getElementById('wordTypeSelect').value   = 'real';
  document.getElementById('wordSessionSelect').value = currentSession === 'master' ? '1' : currentSession;
  document.getElementById('wordModal').style.display = 'flex';
}

function openEditWord(idx, wordId) {
  var isMaster = currentSession === 'master';
  var list = isMaster ? getMasterList() : getSessionList(currentSession);
  var w = list[idx];
  if (!w) return;
  editingWordId = idx;
  document.getElementById('wordModalTitle').textContent = 'Edit Kannada Word';
  document.getElementById('editWordId').value       = idx;
  document.getElementById('wordTextInput').value    = w.word || '';
  document.getElementById('wordTransInput').value   = w.transcription || w.ipa || '';
  document.getElementById('wordMeaningInput').value = w.meaning || w.english || '';
  document.getElementById('wordTypeSelect').value   = w.type || 'real';
  document.getElementById('wordSessionSelect').value = String(w.session || 1);
  document.getElementById('wordModal').style.display = 'flex';
}

function closeWordModal() {
  document.getElementById('wordModal').style.display = 'none';
  editingWordId = null;
}

function handleWordSubmit(event) {
  event.preventDefault();
  var word    = document.getElementById('wordTextInput').value.trim();
  var trans   = document.getElementById('wordTransInput').value.trim();
  var meaning = document.getElementById('wordMeaningInput').value.trim();
  var type    = document.getElementById('wordTypeSelect').value;
  var sesNum  = document.getElementById('wordSessionSelect').value;
  if (!word) { showToast('Kannada word is required.', 'error'); return; }

  var sesKey = String(sesNum);
  if (!rawSessionsData[sesKey]) rawSessionsData[sesKey] = { real: [], pseudo: [], demo: [] };

  if (editingWordId !== null) {
    // Edit existing word
    var targetArray = type === 'pseudo' ? rawSessionsData[sesKey].pseudo : rawSessionsData[sesKey].real;
    if (targetArray && targetArray[editingWordId]) {
      targetArray[editingWordId].word = word;
      targetArray[editingWordId].transcription = trans;
      targetArray[editingWordId].meaning = meaning;
    }
    showToast('Word updated successfully.');
  } else {
    // Add new word
    var item = { id: (type === 'real' ? 'R' : 'N') + Date.now().toString().slice(-4), word: word, transcription: trans, meaning: meaning };
    if (type === 'pseudo') rawSessionsData[sesKey].pseudo.push(item);
    else rawSessionsData[sesKey].real.push(item);
    showToast('Added new word to Session ' + sesNum + '.');
  }

  LS.set('roarCustomSessionsData', rawSessionsData);
  closeWordModal();
  renderWordsTab();
}

function deleteWord(idx, wordId, sesNum) {
  if (!confirm('Delete this word from the corpus?')) return;
  var sesKey = String(sesNum);
  if (!rawSessionsData[sesKey]) return;

  var found = false;
  ['real', 'pseudo'].forEach(function(group) {
    var arr = rawSessionsData[sesKey][group] || [];
    var i = arr.findIndex(function(x) { return x.id === wordId || x.word === wordId; });
    if (i !== -1) { arr.splice(i, 1); found = true; }
  });

  if (!found) {
    if (rawSessionsData[sesKey].real && rawSessionsData[sesKey].real[idx]) rawSessionsData[sesKey].real.splice(idx, 1);
  }

  LS.set('roarCustomSessionsData', rawSessionsData);
  renderWordsTab();
  showToast('Word removed.', 'warning');
}

// Excel Import
function openExcelUploadModal() {
  pendingImport = [];
  document.getElementById('excelPreviewSection').style.display = 'none';
  document.getElementById('excelFileInput').value = '';
  document.getElementById('excelModal').style.display = 'flex';
}

function closeExcelModal() {
  document.getElementById('excelModal').style.display = 'none';
}

function handleExcelFile(event) {
  var file = event.target.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function(e) {
    try {
      var words = [];
      if (file.name.endsWith('.csv')) {
        var text  = e.target.result;
        var lines = text.split(/\r?\n/).filter(function(l) { return l.trim(); });
        lines.forEach(function(line, i) {
          if (i === 0 && (line.toLowerCase().includes('word') || line.toLowerCase().includes('type'))) return;
          var cols = line.split(',').map(function(c) { return c.trim().replace(/^"|"$/g,''); });
          if (cols[0]) words.push({ word: cols[0], type: normType(cols[1] || 'real'), meaning: cols[2] || '' });
        });
      } else {
        var data = new Uint8Array(e.target.result);
        var wb   = XLSX.read(data, { type: 'array' });
        var ws   = wb.Sheets[wb.SheetNames[0]];
        var rows = XLSX.utils.sheet_to_json(ws, { header: 1 });
        var headerRow = 0;
        for (var i = 0; i < Math.min(5, rows.length); i++) {
          if (rows[i] && rows[i].some(function(c) { return typeof c === 'string' && c.toLowerCase().includes('word'); })) {
            headerRow = i; break;
          }
        }
        var headers  = (rows[headerRow] || []).map(function(h) { return String(h||'').toLowerCase().trim(); });
        var wordCol  = headers.findIndex(function(h) { return h.includes('word') || h.includes('stimulus') || h.includes('item'); });
        var typeCol  = headers.findIndex(function(h) { return h.includes('type') || h.includes('category') || h.includes('class'); });
        var meanCol  = headers.findIndex(function(h) { return h.includes('meaning') || h.includes('english'); });
        for (var r = headerRow + 1; r < rows.length; r++) {
          var row  = rows[r] || [];
          var word2 = String(row[wordCol >= 0 ? wordCol : 0] || '').trim();
          if (!word2) continue;
          var type2 = normType(typeCol >= 0 ? String(row[typeCol] || 'real') : 'real');
          var mean2 = meanCol >= 0 ? String(row[meanCol] || '') : '';
          words.push({ word: word2, type: type2, meaning: mean2 });
        }
      }
      pendingImport = words;
      renderExcelPreview(words);
    } catch(err) { showToast('Error parsing file: ' + err.message, 'error'); }
  };
  if (file.name.endsWith('.csv')) reader.readAsText(file);
  else reader.readAsArrayBuffer(file);
}

function normType(t) {
  t = String(t).toLowerCase().trim();
  if (['real','word','ನೈಜ'].indexOf(t) !== -1) return 'real';
  if (['pseudo','nonword','non-word','nw','ಕೃತಕ'].indexOf(t) !== -1) return 'pseudo';
  return 'real';
}

function renderExcelPreview(words) {
  var sec = document.getElementById('excelPreviewSection');
  var body = document.getElementById('excelPreviewContent');
  var title = document.getElementById('excelPreviewTitle');
  if (!sec || !body) return;
  var realCount = words.filter(function(w){return w.type==='real';}).length;
  var pseudoCount = words.filter(function(w){return w.type==='pseudo';}).length;
  if (title) title.textContent = words.length + ' words detected (' + realCount + ' Real + ' + pseudoCount + ' Non-Words):';
  sec.style.display = 'block';
  if (!words.length) { body.textContent = 'No words found in file.'; return; }
  body.innerHTML = '<table style="width:100%;border-collapse:collapse"><thead><tr>' +
    '<th style="text-align:left;padding:0.4rem 0.5rem;border-bottom:1px solid #334155">Word</th>' +
    '<th style="text-align:left;padding:0.4rem 0.5rem;border-bottom:1px solid #334155">Type</th>' +
    '<th style="text-align:left;padding:0.4rem 0.5rem;border-bottom:1px solid #334155">Context/Meaning</th>' +
    '</tr></thead><tbody>' +
    words.slice(0, 50).map(function(w) {
      return '<tr><td class="kannada-text" style="padding:0.3rem 0.5rem">' + esc(w.word) + '</td>' +
        '<td style="padding:0.3rem 0.5rem"><span class="badge badge-' + (w.type==='real'?'blue':'yellow') + '">' + esc(w.type) + '</span></td>' +
        '<td style="padding:0.3rem 0.5rem;color:var(--text-muted)">' + esc(w.meaning) + '</td></tr>';
    }).join('') +
    (words.length > 50 ? '<tr><td colspan="3" style="text-align:center;color:var(--text-muted);padding:0.5rem">… and ' + (words.length - 50) + ' more</td></tr>' : '') +
    '</tbody></table>';
}

function commitExcelImport() {
  if (!pendingImport.length) { showToast('No words to import.', 'warning'); return; }
  var target = document.getElementById('excelTargetSession').value;

  if (target === 'master') {
    // Distribute evenly across 6 sessions
    var realWords = pendingImport.filter(function(w){return w.type==='real';});
    var pseudoWords = pendingImport.filter(function(w){return w.type==='pseudo';});

    [1, 2, 3, 4, 5, 6].forEach(function(s) {
      var k = String(s);
      if (!rawSessionsData[k]) rawSessionsData[k] = { real: [], pseudo: [], demo: [] };
      rawSessionsData[k].real = [];
      rawSessionsData[k].pseudo = [];
    });

    realWords.forEach(function(w, i) {
      var s = String((i % 6) + 1);
      rawSessionsData[s].real.push({ id: 'R' + (i+1), word: w.word, meaning: w.meaning });
    });
    pseudoWords.forEach(function(w, i) {
      var s = String((i % 6) + 1);
      rawSessionsData[s].pseudo.push({ id: 'N' + (i+1), word: w.word, meaning: w.meaning });
    });

    showToast('Imported ' + pendingImport.length + ' words and partitioned across 6 sessions (45 real + 45 non-words each).');
  } else {
    var k = String(target);
    if (!rawSessionsData[k]) rawSessionsData[k] = { real: [], pseudo: [], demo: [] };
    pendingImport.forEach(function(w) {
      if (w.type === 'pseudo') rawSessionsData[k].pseudo.push(w);
      else rawSessionsData[k].real.push(w);
    });
    showToast('Imported ' + pendingImport.length + ' words into Session ' + target + '.');
  }

  LS.set('roarCustomSessionsData', rawSessionsData);
  closeExcelModal();
  renderWordsTab();
  pendingImport = [];
}

// ================================================================
//  TAB 3 — Assessment Results & Telemetry
// ================================================================
function initResultsTab() {
  var results = getResults();
  updateResultsMetrics(results);
  renderResultsTable(results);
}

function updateResultsMetrics(results) {
  var total   = results.length;
  var correct = results.filter(function(r) { return r.correct; }).length;
  var acc     = total ? Math.round(correct / total * 100) : 0;
  var rts     = results.filter(function(r) { return r.rt > 0; }).map(function(r) { return r.rt; });
  var meanRt  = rts.length ? Math.round(rts.reduce(function(a,b) { return a+b; }, 0) / rts.length) : 0;

  var el1 = document.getElementById('metricTotalTrials');
  var el2 = document.getElementById('metricAccuracy');
  var el3 = document.getElementById('metricMeanRt');
  if (el1) el1.textContent = total;
  if (el2) el2.textContent = acc + '%';
  if (el3) el3.textContent = meanRt + ' ms';
}

function renderResultsTable(results) {
  var tbody = document.getElementById('resultsTableBody');
  if (!tbody) return;
  if (!results.length) {
    tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:var(--text-muted);padding:2rem;">No trial responses recorded yet. Responses will appear here as children play.</td></tr>';
    return;
  }
  var rows = results.slice(-200).reverse();
  tbody.innerHTML = rows.map(function(r) {
    var ts  = r.ts ? new Date(r.ts).toLocaleString() : '—';
    var okClass = r.correct ? 'badge-green' : 'badge-danger';
    return '<tr>' +
      '<td style="font-size:0.75rem;color:var(--text-muted)">' + esc(ts) + '</td>' +
      '<td><code style="font-size:0.8rem">' + esc(r.participant||'—') + '</code></td>' +
      '<td>' + esc(String(r.session||'—')) + '</td>' +
      '<td style="font-size:0.75rem">' + esc(r.stage||'—') + '</td>' +
      '<td class="kannada-text" style="font-size:1.15rem">' + esc(r.word||'—') + '</td>' +
      '<td><span class="badge ' + okClass + '">' + (r.correct ? 'Correct' : 'Incorrect') + '</span></td>' +
      '<td>' + (r.rt ? r.rt + ' ms' : '—') + '</td>' +
      '<td style="font-size:0.75rem">' + esc(r.response||'—') + '</td>' +
      '</tr>';
  }).join('');
}

function exportCSV() {
  var results = getResults();
  if (!results.length) { showToast('No results to export.', 'warning'); return; }
  var cols = ['ts','participant','session','stage','word','correct','rt','response','trial_index'];
  var lines = [cols.join(',')].concat(results.map(function(r) {
    return cols.map(function(c) {
      var v = r[c];
      if (v === undefined || v === null) return '';
      var s = String(v);
      return s.includes(',') ? '"' + s.replace(/"/g,'""') + '"' : s;
    }).join(',');
  }));
  var blob = new Blob([lines.join('\n')], { type: 'text/csv;charset=utf-8;' });
  var url  = URL.createObjectURL(blob);
  var a    = document.createElement('a');
  a.href = url;
  a.download = 'roar_results_' + new Date().toISOString().slice(0,10) + '.csv';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast('CSV exported (' + results.length + ' rows).');
}

function clearResults() {
  if (!confirm('Clear ALL trial results? This cannot be undone.')) return;
  LS.del('roarTrialResults');
  LS.del('roarSessionComplete');
  initResultsTab();
  showToast('Results cleared.', 'warning');
}

// ================================================================
//  TAB 4 — Engine Settings & Shuffle Sequence
// ================================================================
function initSettingsTab() {
  var s = getSettings();
  var isInfinite = s.stimulusDisplayMode !== 'timed';
  var inf = document.getElementById('modeInfinite');
  var tim = document.getElementById('modeTimed');
  if (inf) inf.checked = isInfinite;
  if (tim) tim.checked = !isInfinite;

  var stEl = document.getElementById('stimulusTimeSec');
  var ttEl = document.getElementById('trialTimeoutSec');
  var ftEl = document.getElementById('fixationTimeMs');
  var pcEl = document.getElementById('practiceCount');
  var wpEl = document.getElementById('wordsPerSession');

  if (stEl) stEl.value = ((s.stimulusTimeMs  || 10000) / 1000).toFixed(1);
  if (ttEl) ttEl.value = ((s.trialTimeoutMs  || 12000) / 1000).toFixed(1);
  if (ftEl) ftEl.value = s.fixationTimeMs  || 1000;
  if (pcEl) pcEl.value = s.practiceCount   || 5;
  if (wpEl) wpEl.value = s.wordsPerSession || 90;

  // Shuffle Pattern Radio
  var pat = s.shufflePattern || 'alternating';
  if (pat === 'alternating') { document.getElementById('patternAlternating').checked = true; updateShuffleLabel('Strict Alternating'); }
  if (pat === 'constrained') { document.getElementById('patternConstrained').checked = true; updateShuffleLabel('Constrained Balanced'); }
  if (pat === 'blocks')      { document.getElementById('patternBlocks').checked = true; updateShuffleLabel('Block Clusters'); }
  if (pat === 'random')      { document.getElementById('patternRandom').checked = true; updateShuffleLabel('Completely Random'); }

  toggleTimingInputs();
}

function updateShuffleLabel(name) {
  var el = document.getElementById('activeShuffleLabel');
  if (el) el.textContent = name;
}

function toggleTimingInputs() {
  var tim = document.getElementById('modeTimed');
  var row = document.getElementById('timedSettingsRow');
  if (!row) return;
  row.style.display = (tim && tim.checked) ? 'grid' : 'none';
}

function saveSettings(event) {
  if (event) event.preventDefault();
  var inf = document.getElementById('modeInfinite');
  var mode = (inf && inf.checked) ? 'infinite' : 'timed';

  var stSec = parseFloat(document.getElementById('stimulusTimeSec')?.value || 10);
  var ttSec = parseFloat(document.getElementById('trialTimeoutSec')?.value || 12);
  var ft    = parseInt(document.getElementById('fixationTimeMs')?.value || 1000);
  var pc    = parseInt(document.getElementById('practiceCount')?.value || 5);
  var wp    = parseInt(document.getElementById('wordsPerSession')?.value || 90);

  var pat = 'alternating';
  if (document.getElementById('patternConstrained')?.checked) pat = 'constrained';
  if (document.getElementById('patternBlocks')?.checked)      pat = 'blocks';
  if (document.getElementById('patternRandom')?.checked)      pat = 'random';

  var s = {
    stimulusDisplayMode: mode,
    stimulusTimeMs:  Math.round(stSec * 1000),
    trialTimeoutMs:  Math.round(ttSec * 1000),
    fixationTimeMs:  ft,
    practiceCount:   pc,
    wordsPerSession: wp,
    shufflePattern:  pat
  };
  setSettings(s);
  updateRosterMetrics();
  showToast('Settings saved. Shuffle pattern set to ' + pat + '.');
}

function resetSettings() {
  if (!confirm('Reset settings to defaults?')) return;
  LS.del('roarSettings');
  initSettingsTab();
  showToast('Settings reset to defaults.', 'warning');
}

function esc(s) {
  if (s === undefined || s === null) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

document.addEventListener('DOMContentLoaded', function() {
  initRosterTab();
});
</script>"""

new_html = pre + NEW_JS + post

with open(DASH, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Updated {DASH} successfully! New size: {len(new_html)} chars.")
