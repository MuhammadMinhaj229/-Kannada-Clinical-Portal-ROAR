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
    audioFeedback: true
  };
})();
