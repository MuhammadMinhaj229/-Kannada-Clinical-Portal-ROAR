// ROAR Settings — read by game bundle before execution
// Defaults are overridden at runtime by Dashboard Engine Settings (stored in localStorage)
window.ROAR_SETTINGS = (function() {
  try {
    var saved = localStorage.getItem('roarSettings');
    if (saved) {
      var parsed = JSON.parse(saved);
      if (parsed && typeof parsed === 'object') return parsed;
    }
  } catch(e) {}
  return {
    stimulusDisplayMode: "infinite",
    stimulusTimeMs: 10000,
    trialTimeoutMs: 12000,
    fixationTimeMs: 1000,
    practiceCount: 5,
    wordsPerSession: 90,
    audioFeedback: true,
    shufflePattern: "constrained" // "alternating" | "constrained" | "blocks" | "random"
  };
})();

// Active Session Words Initializer
(function() {
  try {
    var CORPUS_VER = 'kn14';
    if (localStorage.getItem('roarCorpusVersion') !== CORPUS_VER) {
      localStorage.removeItem('roarCustomSessionsData');
      localStorage.setItem('roarCorpusVersion', CORPUS_VER);
    }
    var params = new URLSearchParams(window.location.search);
    var sessId = params.get('session') || '1';
    
    // Check localStorage first
    var custom = localStorage.getItem('roarCustomSessionsData');
    var data = null;
    if (custom) {
      try { data = JSON.parse(custom); } catch(e) {}
    }
    
    function applySession(dataObj) {
      if (!dataObj || !dataObj[sessId]) return;
      var ses = dataObj[sessId];
      var words = [];
      if (ses.sequence && ses.sequence.length) {
        words = ses.sequence.map(function(w) {
          return {
            word: w.word,
            realpseudo: w.type || w.realpseudo,
            corpusId: (w.type === 'real' || w.realpseudo === 'real') ? 'kn-real' : 'kn-pseudo',
            pos: w.pos || '',
            rule_logic: w.rule_logic || '',
            source_word: w.source_word || '',
            a: 1.0,
            b: 0.0,
            c: 0.25,
            d: 0.0
          };
        });
      }
      if (words.length > 0) {
        window.ROAR_ACTIVE_WORDS = words;
        console.log('[ROAR] Loaded Session ' + sessId + ' (' + words.length + ' words, dual-constraint sequence).');
      }
    }
    
    if (data) {
      applySession(data);
    } else {
      // Synchronous XMLHttpRequest or fast fetch for initial setup before bundle run
      var xhr = new XMLHttpRequest();
      xhr.open('GET', '/sessions_data.json?v=kn14', false); // synchronous to guarantee execution before bundle
      xhr.onload = function() {
        if (xhr.status === 200) {
          try {
            var fetched = JSON.parse(xhr.responseText);
            applySession(fetched);
          } catch(e) {}
        }
      };
      try { xhr.send(); } catch(e) {}
    }
  } catch(err) {
    console.warn('[ROAR] Session loader fallback:', err);
  }
})();
