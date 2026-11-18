from pathlib import Path

REPO = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")

new_render_fn = '''function renderWordsTable() {
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
             (w.pos||'').toLowerCase().includes(q) ||
             (w.rule_logic||'').toLowerCase().includes(q) ||
             (w.source_word||'').toLowerCase().includes(q) ||
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
    tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:var(--text-muted);padding:1.5rem;">No words found matching criteria.</td></tr>';
    return;
  }

  tbody.innerHTML = words.map(function(w, idx) {
    var word = w.word || w.text || '';
    var type = w.type || 'real';
    var pos = (w.pos || 'noun').toLowerCase();
    var rule = w.rule_logic || (type === 'real' ? 'Original Real Word' : 'Transformed Non-Word');
    var src = w.source_word && w.source_word !== word ? w.source_word : '';
    var meaning = w.meaning || w.english || '';

    // Lexicality Badge
    var lexBadge = type === 'real' 
      ? '<span class="badge badge-blue">Real Word</span>' 
      : (type === 'demo' ? '<span class="badge badge-green">Demo</span>' : '<span class="badge badge-yellow">Non-Word</span>');

    // POS Badge
    var posClass = 'badge-noun';
    var posLabel = 'Noun';
    if (pos === 'verb') { posClass = 'badge-verb'; posLabel = 'Verb'; }
    else if (pos === 'adjective' || pos === 'adj') { posClass = 'badge-adj'; posLabel = 'Adjective'; }
    else if (pos === 'adverb' || pos === 'adv') { posClass = 'badge-adv'; posLabel = 'Adverb'; }
    var posBadge = '<span class="badge ' + posClass + '">' + posLabel + '</span>';

    // Key Badge
    var keyBadge = (type === 'real' || w.expected_key === 'Right')
      ? '<span class="badge badge-key-right">Right → (Blue)</span>'
      : '<span class="badge badge-key-left">← Left (Red)</span>';

    // Trial label
    var trialLabel = w.trial_number || (w.is_demo ? ('Demo ' + (idx + 1)) : String(idx + 1));

    // Rule/Source html
    var ruleHtml = '<div style="font-size:0.8rem;font-weight:500;">' + esc(rule) + '</div>' +
                   (src ? '<div style="font-size:0.72rem;color:var(--text-muted);">Source: ' + esc(src) + '</div>' : '');

    return '<tr>' +
      '<td style="font-size:0.75rem;color:var(--text-muted)">' + esc(String(trialLabel)) + '</td>' +
      '<td class="kannada-text" style="font-size:1.15rem;font-weight:600">' + esc(word) + '</td>' +
      '<td>' + lexBadge + '</td>' +
      '<td>' + posBadge + '</td>' +
      '<td>' + ruleHtml + '</td>' +
      '<td>' + keyBadge + '</td>' +
      '<td style="font-size:0.8rem">' + esc(meaning || '—') + '</td>' +
      '<td style="display:flex;gap:0.4rem">' +
        '<button class="btn btn-sm" onclick="openEditWord(' + idx + ', \'' + (w.id||'') + '\')">Edit</button>' +
        '<button class="btn btn-sm" style="background:var(--danger);color:#fff" onclick="deleteWord(' + idx + ', \'' + (w.id||'') + '\', \'' + (w.session||currentSession) + '\')">Delete</button>' +
      '</td></tr>';
  }).join('');
}'''

for html_file in [REPO / "dashboard.html", REPO / "public" / "dashboard.html"]:
    txt = html_file.read_text(encoding="utf-8")
    start = txt.find("function renderWordsTable() {")
    end = txt.find("function filterWordsTable() {", start)
    if start != -1 and end != -1:
        txt = txt[:start] + new_render_fn + "\n\n" + txt[end:]
        html_file.write_text(txt, encoding="utf-8")
        print(f"Updated {html_file.name}")
    else:
        print(f"Could not locate function boundaries in {html_file.name}")
