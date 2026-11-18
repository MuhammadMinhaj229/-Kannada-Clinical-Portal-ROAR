from pathlib import Path

DASHBOARD_PATH = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\dashboard.html")
PUBLIC_DASHBOARD_PATH = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\public\dashboard.html")

txt = DASHBOARD_PATH.read_text(encoding="utf-8")

# 1. Add CSS for POS and Arrow Key Badges
pos_css = """
    /* POS and Linguistic Badges */
    .badge-noun { background-color: #2e1065; color: #c084fc; border: 1px solid #581c87; }
    .badge-verb { background-color: #082f49; color: #38bdf8; border: 1px solid #0369a1; }
    .badge-adj  { background-color: #064e3b; color: #4ade80; border: 1px solid #047857; }
    .badge-adv  { background-color: #451a03; color: #facc15; border: 1px solid #b45309; }
    .badge-key-right { background-color: #1e3a8a; color: #93c5fd; font-weight: 700; border: 1px solid #2563eb; }
    .badge-key-left  { background-color: #7f1d1d; color: #fca5a5; font-weight: 700; border: 1px solid #dc2626; }
    .rule-tag { font-size: 0.72rem; color: var(--text-muted); background: rgba(255,255,255,0.05); padding: 0.15rem 0.4rem; border-radius: 4px; display: inline-block; }
"""

if ".badge-noun" not in txt:
    txt = txt.replace("  </style>", pos_css + "\n  </style>")
    print("[OK] Added POS and Key badge CSS.")

# 2. Add Proportionality and Action Bar to Tab 2
old_header = """          <div style="display: flex; gap: 0.5rem;">
            <button class="btn btn-secondary btn-sm" onclick="openExcelUploadModal()">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
              Import Excel / CSV
            </button>
            <button class="btn btn-primary btn-sm" onclick="openAddWordModal()">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
              Add Word
            </button>
          </div>"""

new_header = """          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <button class="btn btn-secondary btn-sm" onclick="exportCurrentViewCSV()" title="Export CSV for current session or master corpus">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
              Export CSV
            </button>
            <button class="btn btn-secondary btn-sm" onclick="openExcelUploadModal()">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
              Import Excel / CSV
            </button>
            <button class="btn btn-primary btn-sm" onclick="openAddWordModal()">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
              Add Word
            </button>
          </div>"""

txt = txt.replace(old_header, new_header)

# Add Proportionality banner above session pills
proportionality_banner = """
        <!-- Linguistic Proportionality & Engine Status Banner -->
        <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid var(--border); border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 1.25rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;">
            <div>
              <div style="font-size: 0.85rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.25rem;">
                Kannada Clinical Corpus: 540 Words (270 Real + 270 Non-Words)
              </div>
              <div style="font-size: 0.75rem; color: var(--text-muted); display: flex; gap: 0.75rem; flex-wrap: wrap;">
                <span><strong>POS:</strong> Noun: 96 | Verb: 97 | Adjective: 43 | Adverb: 34</span>
                <span>•</span>
                <span><strong>4 Non-Word Logics:</strong> L1 Consonant (68) | L2 Vowel (68) | L3 Splice (67) | L4 Shift (67)</span>
              </div>
            </div>
            <div style="display: flex; gap: 0.5rem; align-items: center;">
              <span class="badge" style="background:#064e3b; color:#6ee7b7; border: 1px solid #059669;">
                Dual-Constraint Engine Active
              </span>
              <button class="btn btn-sm btn-secondary" onclick="exportMasterCorpusDirect()" style="font-size:0.75rem;">
                Export Master (540 CSV)
              </button>
            </div>
          </div>
        </div>
"""

if "<!-- Linguistic Proportionality & Engine Status Banner -->" not in txt:
    txt = txt.replace('        <!-- Session Selection Pills -->', proportionality_banner + '\n        <!-- Session Selection Pills -->')
    print("[OK] Added Proportionality & Engine Status Banner.")

# 3. Update Table Header Columns
old_thead = """            <thead>
              <tr>
                <th>Item ID</th>
                <th>Kannada Word</th>
                <th>Type</th>
                <th>IPA Transcription</th>
                <th>English Meaning</th>
                <th>Actions</th>
              </tr>
            </thead>"""

new_thead = """            <thead>
              <tr>
                <th style="width: 60px;">Trial #</th>
                <th>Kannada Word</th>
                <th>Lexicality</th>
                <th>Part of Speech</th>
                <th>Generation Logic / Source</th>
                <th>Key (Color)</th>
                <th>Meaning</th>
                <th>Actions</th>
              </tr>
            </thead>"""

txt = txt.replace(old_thead, new_thead)

# 4. Enhance JavaScript functions: getSessionList, renderWordsTable, exportCurrentViewCSV, exportMasterCorpusDirect
old_get_session = """function getSessionList(s) {
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
}"""

new_get_session = """function getSessionList(s) {
  var ses = rawSessionsData[String(s)] || {};
  var list = [];
  (ses.demo || []).forEach(function(w, idx) {
    list.push(Object.assign({}, w, { type: 'demo', session: s, trial_number: 'Demo ' + (idx + 1), is_demo: true }));
  });
  if (ses.sequence && ses.sequence.length) {
    ses.sequence.forEach(function(w) {
      list.push(Object.assign({}, w, { session: s }));
    });
  } else {
    (ses.real || []).forEach(function(w, idx) {
      list.push(Object.assign({}, w, { type: 'real', session: s, trial_number: idx + 1 }));
    });
    (ses.pseudo || []).forEach(function(w, idx) {
      list.push(Object.assign({}, w, { type: 'pseudo', session: s, trial_number: idx + 46 }));
    });
  }
  return list;
}"""

txt = txt.replace(old_get_session, new_get_session)

# Update renderWordsTable function body to render the new columns
old_render_words_start = """  tbody.innerHTML = words.map(function(w, idx) {
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
  }).join('');"""

new_render_words_start = """  tbody.innerHTML = words.map(function(w, idx) {
    var word = w.word || w.text || '';
    var type = w.type || (w.realpseudo === 'pseudo' ? 'pseudo' : 'real');
    var pos  = (w.pos || '').toLowerCase();
    var meaning = w.meaning || w.english || '';
    var rule = w.rule_logic || (type === 'real' ? 'Original Real Word' : 'Derived Non-Word');
    var sourceWord = w.source_word ? 'From: ' + w.source_word : '';
    
    var typeBadge = type === 'real' ? 'badge-blue' : (type === 'demo' ? 'badge-green' : 'badge-yellow');
    var typeLabel = type === 'pseudo' ? 'Non-Word' : (type === 'demo' ? 'Demo Practice' : 'Real Word');
    
    // POS badge styling
    var posBadgeClass = 'badge-noun';
    if (pos === 'verb') posBadgeClass = 'badge-verb';
    else if (pos === 'adjective' || pos === 'adj') posBadgeClass = 'badge-adj';
    else if (pos === 'adverb' || pos === 'adv') posBadgeClass = 'badge-adv';
    var posBadge = pos ? '<span class="badge ' + posBadgeClass + '">' + esc(pos.toUpperCase()) + '</span>' : '—';
    
    // Key styling
    var isRight = type === 'real';
    var keyClass = isRight ? 'badge-key-right' : 'badge-key-left';
    var keyLabel = isRight ? 'Right → (Blue)' : '← Left (Red)';
    var keyBadge = '<span class="badge ' + keyClass + '">' + keyLabel + '</span>';

    var trialLabel = w.trial_number ? String(w.trial_number) : String(idx + 1);

    return '<tr>' +
      '<td style="font-size:0.8rem;font-weight:700;color:var(--text-muted)">' + esc(trialLabel) + '</td>' +
      '<td class="kannada-text" style="font-size:1.25rem;font-weight:700;color:#f8fafc">' + esc(word) + '</td>' +
      '<td><span class="badge ' + typeBadge + '">' + esc(typeLabel) + '</span></td>' +
      '<td>' + posBadge + '</td>' +
      '<td>' +
        '<div style="font-size:0.75rem;font-weight:600;color:#cbd5e1">' + esc(rule) + '</div>' +
        (sourceWord ? '<div style="font-size:0.7rem;color:var(--text-muted)">' + esc(sourceWord) + '</div>' : '') +
      '</td>' +
      '<td>' + keyBadge + '</td>' +
      '<td style="font-size:0.8rem;color:var(--text-muted)">' + esc(meaning || '—') + '</td>' +
      '<td style="display:flex;gap:0.4rem">' +
        '<button class="btn btn-sm" onclick="openEditWord(' + idx + ', \'' + (w.id||'') + '\')">Edit</button>' +
        '<button class="btn btn-sm" style="background:var(--danger);color:#fff" onclick="deleteWord(' + idx + ', \'' + (w.id||'') + '\', \'' + (w.session||currentSession) + '\')">Delete</button>' +
      '</td></tr>';
  }).join('');"""

txt = txt.replace(old_render_words_start, new_render_words_start)

# Add CSV Export Functions for Words
export_csv_funcs = """
function exportCurrentViewCSV() {
  var isMaster = currentSession === 'master';
  if (isMaster) {
    exportMasterCorpusDirect();
  } else {
    exportSessionCSV(currentSession);
  }
}

function exportSessionCSV(sessId) {
  var words = getSessionList(sessId);
  if (!words.length) { showToast('No words to export for Session ' + sessId, 'warning'); return; }
  
  var cols = ['trial_number', 'word', 'type', 'pos', 'source_word', 'rule_logic', 'syllables', 'expected_key', 'arrow_color', 'meaning'];
  var headers = ['Trial Number', 'Kannada Word', 'Word Type', 'Part of Speech (POS)', 'Source Word', 'Transformation Rule', 'Syllables', 'Expected Key', 'Arrow Color Hint', 'Meaning'];
  
  var lines = [headers.join(',')];
  words.forEach(function(w, idx) {
    var trial = w.trial_number || (idx + 1);
    var type  = w.type || 'real';
    var pos   = w.pos || '';
    var src   = w.source_word || w.word || '';
    var rule  = w.rule_logic || (type === 'real' ? 'Original Real Word' : '');
    var syl   = w.syllables || 2;
    var key   = type === 'real' ? 'Right' : 'Left';
    var color = type === 'real' ? 'Blue' : 'Red';
    var mean  = w.meaning || '';
    
    var row = [
      String(trial),
      '"' + String(w.word||'').replace(/"/g, '""') + '"',
      type,
      pos,
      '"' + String(src).replace(/"/g, '""') + '"',
      '"' + String(rule).replace(/"/g, '""') + '"',
      String(syl),
      key,
      color,
      '"' + String(mean).replace(/"/g, '""') + '"'
    ];
    lines.push(row.join(','));
  });
  
  downloadBlob(lines.join('\\n'), 'kannada_session_' + sessId + '_sequence_90.csv');
  showToast('Exported Session ' + sessId + ' sequence (' + words.length + ' trials).');
}

function exportMasterCorpusDirect() {
  fetch('/master_corpus_540.csv')
    .then(function(r) { return r.text(); })
    .then(function(csvText) {
      downloadBlob(csvText, 'kannada_master_corpus_540.csv');
      showToast('Exported Master Corpus (540 words: 270 real + 270 non-words).');
    })
    .catch(function() {
      // Fallback: build from getMasterList()
      var words = getMasterList();
      var cols = ['item_id', 'word', 'type', 'pos', 'source_word', 'rule_logic', 'meaning', 'syllables'];
      var lines = [cols.join(',')].concat(words.map(function(w) {
        return [
          w.id||'',
          '"' + (w.word||'').replace(/"/g,'""') + '"',
          w.type||'real',
          w.pos||'',
          '"' + (w.source_word||'').replace(/"/g,'""') + '"',
          '"' + (w.rule_logic||'').replace(/"/g,'""') + '"',
          '"' + (w.meaning||'').replace(/"/g,'""') + '"',
          w.syllables||2
        ].join(',');
      }));
      downloadBlob(lines.join('\\n'), 'kannada_master_corpus_540.csv');
      showToast('Exported Master Corpus (' + words.length + ' words).');
    });
}

function downloadBlob(content, filename) {
  var blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
  var url  = URL.createObjectURL(blob);
  var a    = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
"""

if "function exportCurrentViewCSV()" not in txt:
    txt = txt.replace("function renderWordsTable() {", export_csv_funcs + "\nfunction renderWordsTable() {")
    print("[OK] Added CSV export functions.")

# Write back
DASHBOARD_PATH.write_text(txt, encoding="utf-8")
PUBLIC_DASHBOARD_PATH.write_text(txt, encoding="utf-8")
print("[OK] Updated dashboard.html and public/dashboard.html successfully.")
