"""
Writes the final pure-frontend JS block into dashboard.html.
Matches actual HTML element IDs exactly.
"""

DASH = r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\public\dashboard.html"

with open(DASH, 'r', encoding='utf-8') as f:
    html = f.read()

script_start = html.index('<script>')
script_end   = html.rindex('</script>') + len('</script>')
pre  = html[:script_start]
post = html[script_end:]

NEW_JS = r"""<script>
// ================================================================
//  ROAR Dashboard — Pure Frontend (100% localStorage, Zero Backend)
//  v7.0 — Vercel Static Deploy Ready
// ================================================================

// ── LocalStorage helpers ─────────────────────────────────────────
const LS = {
  get: function(k, def) {
    if (def === undefined) def = [];
    try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : def; } catch(e) { return def; }
  },
  set: function(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch(e) {} },
  del: function(k)    { try { localStorage.removeItem(k); } catch(e) {} }
};

// ── Data accessors ───────────────────────────────────────────────
function getStudents()  { return LS.get('studentsRoster', []); }
function setStudents(a) { LS.set('studentsRoster', a); }
function getSettings()  {
  return LS.get('roarSettings', {
    stimulusDisplayMode: 'infinite', stimulusTimeMs: 10000, trialTimeoutMs: 12000,
    fixationTimeMs: 1000, practiceCount: 5, wordsPerSession: 90
  });
}
function setSettings(s) { LS.set('roarSettings', s); }
function getResults()   { return LS.get('roarTrialResults', []); }

// ── State ────────────────────────────────────────────────────────
var allStudents     = [];
var allSessionsData = {};
var currentSession  = '1';
var editingWordId   = null;
var editingStudentId = null;
var pendingImport   = [];

// ── Toast ─────────────────────────────────────────────────────────
function showToast(msg, type) {
  type = type || 'success';
  var t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.className = '';
  t.style.cssText = 'display:block;position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;padding:0.75rem 1.25rem;border-radius:8px;font-size:0.875rem;font-weight:600;max-width:380px;';
  if (type === 'error')   t.style.background = '#ef4444';
  else if (type === 'warning') t.style.background = '#f59e0b';
  else t.style.background = '#10b981';
  t.style.color = '#fff';
  setTimeout(function() { t.style.display = 'none'; }, 3500);
}

// ── Tab navigation ───────────────────────────────────────────────
function switchTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(function(b) {
    b.classList.remove('active');
  });
  document.querySelectorAll('.tab-content').forEach(function(c) {
    c.classList.remove('active');
  });
  // find tab button that calls switchTab(tabId)
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
  // Compute accuracy per participant from results
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

// ── Student Modal (Add / Edit) ───────────────────────────────────
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
  document.getElementById('stuIdInput').disabled   = true; // cannot change ID after creation
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
    // Edit existing
    students[editingStudentId].name    = name;
    students[editingStudentId].grade   = grade;
    students[editingStudentId].session = session;
    setStudents(students);
    closeStudentModal();
    allStudents = students;
    renderStudentsTable();
    showToast('Child record updated.');
  } else {
    // Add new
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
  if (!confirm('Delete this child record? This cannot be undone.')) return;
  var students = getStudents();
  students.splice(idx, 1);
  setStudents(students);
  allStudents = students;
  renderStudentsTable();
  updateRosterMetrics();
  showToast('Record deleted.', 'warning');
}

// ================================================================
//  TAB 2 — Word Bank & Datasets
// ================================================================
function initWordsTab() {
  if (Object.keys(allSessionsData).length > 0) {
    renderWordsTab(); return;
  }
  fetch('/sessions_data.json')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      allSessionsData = data;
      // Apply any localStorage edits
      var edits = LS.get('roarWordEdits', {});
      Object.keys(edits).forEach(function(k) {
        var parts = k.split('-');
        var sesKey = 'session' + parts[0];
        var idx = parseInt(parts[1]);
        if (allSessionsData[sesKey] && allSessionsData[sesKey][idx]) {
          Object.assign(allSessionsData[sesKey][idx], edits[k]);
        }
      });
      renderWordsTab();
    })
    .catch(function(e) { showToast('Could not load sessions_data.json', 'error'); });
}

function renderWordsTab() {
  updateSessionPills();
  renderWordsTable();
}

function updateSessionPills() {
  var pills = document.getElementById('sessionPills');
  if (!pills) return;
  pills.innerHTML = [1,2,3,4,5,6].map(function(n) {
    var active = currentSession === String(n) ? 'active' : '';
    return '<button class="session-pill ' + active + '" onclick="selectSession(\'' + n + '\')">' +
      'Session ' + n + '</button>';
  }).join('');
}

function selectSession(n) {
  currentSession = String(n);
  renderWordsTab();
}

function renderWordsTable() {
  var tbody = document.getElementById('wordsTableBody');
  if (!tbody) return;
  var sesKey = 'session' + currentSession;
  var words  = allSessionsData[sesKey] || [];
  var q = '';
  var searchEl = document.getElementById('wordSearchInput');
  if (searchEl) q = searchEl.value.toLowerCase();
  if (q) words = words.filter(function(w) {
    return (w.word||w.text||'').toLowerCase().includes(q) ||
           (w.type||'').toLowerCase().includes(q) ||
           (w.meaning||w.english||'').toLowerCase().includes(q);
  });

  var total = (allSessionsData[sesKey] || []).length;
  var statsEl = document.getElementById('sessionStatsText');
  if (statsEl) statsEl.textContent = 'Showing ' + words.length + ' / ' + total + ' words in Session ' + currentSession;

  if (!words.length) {
    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:var(--text-muted);padding:1.5rem;">No words found.</td></tr>';
    return;
  }
  var allWords = allSessionsData[sesKey] || [];
  tbody.innerHTML = words.map(function(w) {
    var realIdx = allWords.indexOf(w);
    var word  = w.word || w.text || '';
    var type  = w.type || 'real';
    var trans = w.ipa || w.transcription || w.trans || '';
    var meaning = w.meaning || w.english || '';
    var typeBadge = type === 'real' || type === 'word' ? 'badge-blue' :
                    type === 'demo' || type === 'practice' ? 'badge-green' : 'badge-yellow';
    return '<tr>' +
      '<td style="font-size:0.75rem;color:var(--text-muted)">' + esc(String(realIdx + 1)) + '</td>' +
      '<td class="kannada-text" style="font-size:1.1rem">' + esc(word) + '</td>' +
      '<td><span class="badge ' + typeBadge + '">' + esc(type) + '</span></td>' +
      '<td style="font-size:0.8rem;color:var(--text-muted)">' + esc(trans) + '</td>' +
      '<td style="font-size:0.8rem">' + esc(meaning) + '</td>' +
      '<td style="display:flex;gap:0.4rem">' +
        '<button class="btn btn-sm" onclick="openEditWord(' + realIdx + ')">Edit</button>' +
        '<button class="btn btn-sm" style="background:var(--danger);color:#fff" onclick="deleteWord(' + realIdx + ')">Delete</button>' +
      '</td></tr>';
  }).join('');
}

function filterWordsTable() { renderWordsTable(); }

// ── Word Modal (Add / Edit) ──────────────────────────────────────
function openAddWordModal() {
  editingWordId = null;
  document.getElementById('wordModalTitle').textContent = 'Add Kannada Word';
  document.getElementById('editWordId').value       = '';
  document.getElementById('wordTextInput').value    = '';
  document.getElementById('wordTransInput').value   = '';
  document.getElementById('wordMeaningInput').value = '';
  document.getElementById('wordTypeSelect').value   = 'real';
  document.getElementById('wordSessionSelect').value = currentSession;
  document.getElementById('wordModal').style.display = 'flex';
}

function openEditWord(idx) {
  var sesKey = 'session' + currentSession;
  var w = (allSessionsData[sesKey] || [])[idx];
  if (!w) return;
  editingWordId = idx;
  document.getElementById('wordModalTitle').textContent = 'Edit Word';
  document.getElementById('editWordId').value       = idx;
  document.getElementById('wordTextInput').value    = w.word || w.text || '';
  document.getElementById('wordTransInput').value   = w.ipa || w.transcription || w.trans || '';
  document.getElementById('wordMeaningInput').value = w.meaning || w.english || '';
  document.getElementById('wordTypeSelect').value   = w.type || 'real';
  document.getElementById('wordSessionSelect').value = currentSession;
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

  var sesKey = 'session' + sesNum;
  if (!allSessionsData[sesKey]) allSessionsData[sesKey] = [];

  if (editingWordId !== null) {
    // Edit
    allSessionsData[sesKey][editingWordId].word = word;
    allSessionsData[sesKey][editingWordId].text = word;
    allSessionsData[sesKey][editingWordId].type = type;
    allSessionsData[sesKey][editingWordId].ipa  = trans;
    allSessionsData[sesKey][editingWordId].meaning = meaning;
    // persist edit to localStorage
    var edits = LS.get('roarWordEdits', {});
    edits[sesNum + '-' + editingWordId] = { word: word, type: type };
    LS.set('roarWordEdits', edits);
    showToast('Word updated.');
  } else {
    // Add
    allSessionsData[sesKey].push({ word: word, text: word, type: type, ipa: trans, meaning: meaning });
    if (sesNum !== currentSession) { currentSession = sesNum; }
    showToast('Word added to Session ' + sesNum + '.');
  }
  closeWordModal();
  renderWordsTab();
}

function deleteWord(idx) {
  if (!confirm('Delete this word?')) return;
  var sesKey = 'session' + currentSession;
  allSessionsData[sesKey].splice(idx, 1);
  renderWordsTab();
  showToast('Word deleted.', 'warning');
}

// ── Excel / CSV Import ───────────────────────────────────────────
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
          if (cols[0]) words.push({ word: cols[0], text: cols[0], type: normType(cols[1] || 'real'), meaning: cols[2] || '' });
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
          words.push({ word: word2, text: word2, type: type2, meaning: mean2 });
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
  if (['pseudo','nonword','non-word','nw'].indexOf(t) !== -1) return 'pseudo';
  if (['demo','practice'].indexOf(t) !== -1) return 'demo';
  return 'real';
}

function renderExcelPreview(words) {
  var sec = document.getElementById('excelPreviewSection');
  var body = document.getElementById('excelPreviewContent');
  var title = document.getElementById('excelPreviewTitle');
  if (!sec || !body) return;
  if (title) title.textContent = words.length + ' words found — Preview (first 50):';
  sec.style.display = 'block';
  if (!words.length) { body.textContent = 'No words found in file.'; return; }
  body.innerHTML = '<table style="width:100%;border-collapse:collapse"><thead><tr>' +
    '<th style="text-align:left;padding:0.4rem 0.5rem;border-bottom:1px solid #334155">Word</th>' +
    '<th style="text-align:left;padding:0.4rem 0.5rem;border-bottom:1px solid #334155">Type</th>' +
    '<th style="text-align:left;padding:0.4rem 0.5rem;border-bottom:1px solid #334155">Meaning</th>' +
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
  var sesNum = document.getElementById('excelTargetSession').value;
  var sesKey = 'session' + sesNum;
  if (!allSessionsData[sesKey]) allSessionsData[sesKey] = [];
  pendingImport.forEach(function(w) { allSessionsData[sesKey].push(w); });
  closeExcelModal();
  if (currentSession !== sesNum) { currentSession = sesNum; }
  renderWordsTab();
  showToast('Imported ' + pendingImport.length + ' words to Session ' + sesNum + '.');
  pendingImport = [];
}

// ================================================================
//  TAB 3 — Results & Telemetry
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
      '<td class="kannada-text" style="font-size:1.1rem">' + esc(r.word||'—') + '</td>' +
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
//  TAB 4 — Engine Settings
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

  toggleTimingInputs();
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

  var s = {
    stimulusDisplayMode: mode,
    stimulusTimeMs:  Math.round(stSec * 1000),
    trialTimeoutMs:  Math.round(ttSec * 1000),
    fixationTimeMs:  ft,
    practiceCount:   pc,
    wordsPerSession: wp
  };
  setSettings(s);
  updateRosterMetrics();
  showToast('Settings saved. Next game launch will use these values.');
}

function resetSettings() {
  if (!confirm('Reset settings to defaults?')) return;
  LS.del('roarSettings');
  initSettingsTab();
  showToast('Settings reset to defaults.', 'warning');
}

// ================================================================
//  UTILITIES
// ================================================================
function esc(s) {
  if (s === undefined || s === null) return '';
  return String(s)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}

function copyLink(type) {
  var base = window.location.origin;
  var url  = type === 'game'
    ? base + '/?consent=false&storyoption=false'
    : base + '/dashboard.html';
  if (navigator.clipboard) {
    navigator.clipboard.writeText(url).then(function() { showToast('Link copied: ' + url); });
  } else {
    prompt('Copy this URL:', url);
  }
}

// ── Init ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  // Fix Export CSV button (was pointing to /api/results/export)
  document.querySelectorAll('a[href*="/api/results/export"]').forEach(function(a) {
    a.removeAttribute('href');
    a.style.cursor = 'pointer';
    a.onclick = function(e) { e.preventDefault(); exportCSV(); };
  });

  // Load initial tab
  initRosterTab();
});
</script>"""

with open(DASH, 'w', encoding='utf-8') as f:
    f.write(pre + NEW_JS + post)

with open(DASH, 'r', encoding='utf-8') as f:
    final = f.read()

print(f"Dashboard patched. Size: {len(final)} chars")
api_calls = final.count("fetch('/api/")
print(f"API fetch('/api/ calls remaining: {api_calls}")
print(f"localStorage refs: {final.count('localStorage.')}")
print(f"getResults() refs: {final.count('getResults()')}")
print(f"/api/results/export refs: {final.count('/api/results/export')}")

