const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 8080;
const PUBLIC_DIR = path.join(__dirname, 'public');
const SESSIONS_FILE = path.join(__dirname, 'sessions_data.json');
const RESULTS_FILE = path.join(__dirname, 'student_results.json');
const STUDENTS_FILE = path.join(__dirname, 'students_roster.json');
const SETTINGS_FILE = path.join(__dirname, 'game_settings.json');

const getStudentsSafe = () => {
  try {
    const raw = fs.readFileSync(STUDENTS_FILE, 'utf-8').replace(/^\uFEFF/, '');
    const data = JSON.parse(raw);
    return Array.isArray(data) ? data : [data];
  } catch(e) { return []; }
};

const getResultsSafe = () => {
  try {
    const raw = fs.readFileSync(RESULTS_FILE, 'utf-8').replace(/^\uFEFF/, '');
    const data = JSON.parse(raw);
    return Array.isArray(data) ? data : [data];
  } catch(e) { return []; }
};
const REMOTE_GCS_BASE = 'https://storage.googleapis.com/roar-swr';

// Ensure data files exist
if (!fs.existsSync(RESULTS_FILE)) {
  fs.writeFileSync(RESULTS_FILE, JSON.stringify([], null, 2), 'utf-8');
}
if (!fs.existsSync(STUDENTS_FILE)) {
  const initialStudents = [
    { id: "minhajid-01", name: "Minhaj", grade: "Grade 1", session: 1, status: "Pending", registeredAt: "2026-11-15" }
  ];
  fs.writeFileSync(STUDENTS_FILE, JSON.stringify(initialStudents, null, 2), 'utf-8');
}
if (!fs.existsSync(SETTINGS_FILE)) {
  const defaultSettings = {
    stimulusDisplayMode: "infinite",
    stimulusTimeMs: 10000,
    trialTimeoutMs: 12000,
    fixationTimeMs: 1000,
    practiceCount: 5,
    wordsPerSession: 90,
    audioFeedback: true
  };
  fs.writeFileSync(SETTINGS_FILE, JSON.stringify(defaultSettings, null, 2), 'utf-8');
}

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json',
  '.css': 'text/css',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.mp3': 'audio/mpeg',
  '.map': 'application/json',
  '.csv': 'text/csv; charset=utf-8',
};

const NO_CACHE_HEADERS = {
  'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0',
  'Pragma': 'no-cache',
  'Expires': '0',
  'Surrogate-Control': 'no-store',
};

// Parse JSON Body Helper
const parseJsonBody = (req) => new Promise((resolve, reject) => {
  let body = '';
  req.on('data', chunk => { body += chunk.toString(); });
  req.on('end', () => {
    try {
      resolve(body ? JSON.parse(body) : {});
    } catch (e) {
      reject(e);
    }
  });
});

const server = http.createServer(async (req, res) => {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const urlPath = decodeURIComponent(parsedUrl.pathname);

  // Helper for JSON responses
  const sendJson = (data, status = 200) => {
    res.writeHead(status, {
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      ...NO_CACHE_HEADERS
    });
    res.end(JSON.stringify(data));
  };

  // Helper to serve local file
  const sendLocalFile = (filePath, contentType) => {
    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Internal Server Error: ' + err.message);
        return;
      }
      res.writeHead(200, {
        'Content-Type': contentType,
        'Access-Control-Allow-Origin': '*',
        ...NO_CACHE_HEADERS,
      });
      res.end(content);
    });
  };

  // ==========================================
  // REST API: SYSTEM SETTINGS
  // ==========================================
  if (urlPath === '/api/settings.js' && req.method === 'GET') {
    let settings = {};
    try {
      settings = JSON.parse(fs.readFileSync(SETTINGS_FILE, 'utf-8'));
    } catch (e) {}
    const jsContent = `window.ROAR_SETTINGS = ${JSON.stringify(settings, null, 2)};`;
    res.writeHead(200, {
      'Content-Type': 'application/javascript; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      ...NO_CACHE_HEADERS
    });
    res.end(jsContent);
    return;
  }

  if (urlPath === '/api/settings' && req.method === 'GET') {
    try {
      const settings = JSON.parse(fs.readFileSync(SETTINGS_FILE, 'utf-8'));
      sendJson(settings);
    } catch (e) {
      sendJson({ error: e.message }, 500);
    }
    return;
  }

  if (urlPath === '/api/settings' && req.method === 'POST') {
    try {
      const newSettings = await parseJsonBody(req);
      const current = JSON.parse(fs.readFileSync(SETTINGS_FILE, 'utf-8'));
      const updated = { ...current, ...newSettings };
      fs.writeFileSync(SETTINGS_FILE, JSON.stringify(updated, null, 2), 'utf-8');
      sendJson({ success: true, settings: updated });
    } catch (e) {
      sendJson({ success: false, error: e.message }, 500);
    }
    return;
  }

  // ==========================================
  // REST API: OVERVIEW
  // ==========================================
  if (urlPath === '/api/overview' && req.method === 'GET') {
    let studentsCount = 0;
    let completedCount = 0;
    try {
      const students = getStudentsSafe();
      studentsCount = students.length;
      completedCount = students.filter(s => s.status === 'Completed').length;
    } catch (e) {}

    let currentSettings = {};
    try {
      currentSettings = JSON.parse(fs.readFileSync(SETTINGS_FILE, 'utf-8'));
    } catch (e) {}

    const overview = {
      gameName: "Stanford ROAR Single Word Recognition — Kannada Edition",
      language: "Kannada (ಕನ್ನಡ)",
      voiceover: "Microsoft Neural AI (kn-IN-SapnaNeural)",
      totalSessions: 6,
      wordsPerSession: 90,
      demosPerSession: 5,
      totalRealWords: 270,
      totalPseudoWords: 270,
      totalCorpusSize: 540,
      audioFilesCount: 42,
      registeredStudentsCount: studentsCount,
      completedTestsCount: completedCount,
      settings: currentSettings
    };
    sendJson(overview);
    return;
  }

  // ==========================================
  // REST API: SESSIONS & WORDS
  // ==========================================
  if (urlPath === '/api/sessions' && req.method === 'GET') {
    try {
      const data = JSON.parse(fs.readFileSync(SESSIONS_FILE, 'utf-8'));
      sendJson(data);
    } catch (e) {
      sendJson({ error: 'Failed to read sessions_data.json' }, 500);
    }
    return;
  }

  // Live word update
  if (urlPath === '/api/words/update' && req.method === 'POST') {
    try {
      const body = await parseJsonBody(req);
      const { session, wordId, newWord, newMeaning, newTranscription } = body;
      const data = JSON.parse(fs.readFileSync(SESSIONS_FILE, 'utf-8'));

      if (data[session]) {
        let found = false;
        ['real', 'pseudo', 'demo'].forEach(type => {
          if (data[session][type]) {
            data[session][type].forEach(item => {
              if (item.id === wordId || item.word === wordId) {
                if (newWord) item.word = newWord;
                if (newMeaning !== undefined) item.meaning = newMeaning;
                if (newTranscription !== undefined) item.transcription = newTranscription;
                found = true;
              }
            });
          }
        });

        if (found) {
          fs.writeFileSync(SESSIONS_FILE, JSON.stringify(data, null, 2), 'utf-8');
          sendJson({ success: true, message: `Word ${wordId} updated.` });
          return;
        }
      }
      sendJson({ success: false, error: 'Word or session not found.' }, 404);
    } catch (e) {
      sendJson({ success: false, error: e.message }, 500);
    }
    return;
  }

  // Add individual word to a session
  if (urlPath === '/api/words/add' && req.method === 'POST') {
    try {
      const body = await parseJsonBody(req);
      const { session, type, word, transcription, meaning } = body; // type = 'real' | 'pseudo'
      if (!session || !type || !word) {
        sendJson({ success: false, error: 'Missing required fields: session, type, word' }, 400);
        return;
      }
      const data = JSON.parse(fs.readFileSync(SESSIONS_FILE, 'utf-8'));
      if (!data[session]) data[session] = { demo: [], real: [], pseudo: [] };
      if (!data[session][type]) data[session][type] = [];

      const newItem = {
        id: `custom_${type}_${Date.now()}`,
        word: word.trim(),
        transcription: transcription ? transcription.trim() : word.trim(),
        meaning: meaning ? meaning.trim() : "",
        realpseudo: type,
        session: parseInt(session, 10),
        b: 0,
        source: 'manual'
      };
      data[session][type].push(newItem);
      fs.writeFileSync(SESSIONS_FILE, JSON.stringify(data, null, 2), 'utf-8');
      sendJson({ success: true, item: newItem });
    } catch (e) {
      sendJson({ success: false, error: e.message }, 500);
    }
    return;
  }

  // Delete word from a session
  if (urlPath === '/api/words/delete' && req.method === 'POST') {
    try {
      const { session, wordId } = await parseJsonBody(req);
      const data = JSON.parse(fs.readFileSync(SESSIONS_FILE, 'utf-8'));
      if (data[session]) {
        ['real', 'pseudo'].forEach(t => {
          if (data[session][t]) {
            data[session][t] = data[session][t].filter(item => item.id !== wordId && item.word !== wordId);
          }
        });
        fs.writeFileSync(SESSIONS_FILE, JSON.stringify(data, null, 2), 'utf-8');
        sendJson({ success: true });
        return;
      }
      sendJson({ success: false, error: 'Session not found' }, 404);
    } catch (e) {
      sendJson({ success: false, error: e.message }, 500);
    }
    return;
  }

  // Bulk words import (from client-side parsed Excel)
  if (urlPath === '/api/words/bulk' && req.method === 'POST') {
    try {
      const { session, words } = await parseJsonBody(req);
      if (!session || !Array.isArray(words)) {
        sendJson({ success: false, error: 'Invalid payload' }, 400);
        return;
      }
      const data = JSON.parse(fs.readFileSync(SESSIONS_FILE, 'utf-8'));
      if (!data[session]) data[session] = { demo: [], real: [], pseudo: [] };

      let addedReal = 0, addedPseudo = 0;
      words.forEach((w, idx) => {
        const itemType = (w.type === 'real' || w.realpseudo === 'real') ? 'real' : 'pseudo';
        const item = {
          id: `bulk_${session}_${idx}_${Date.now()}`,
          word: (w.word || '').trim(),
          transcription: (w.transcription || w.word || '').trim(),
          meaning: (w.meaning || '').trim(),
          realpseudo: itemType,
          session: parseInt(session, 10),
          b: 0,
          source: 'excel_import'
        };
        if (item.word) {
          data[session][itemType].push(item);
          if (itemType === 'real') addedReal++; else addedPseudo++;
        }
      });

      fs.writeFileSync(SESSIONS_FILE, JSON.stringify(data, null, 2), 'utf-8');
      sendJson({ success: true, addedReal, addedPseudo });
    } catch (e) {
      sendJson({ success: false, error: e.message }, 500);
    }
    return;
  }

  // ==========================================
  // REST API: STUDENTS & ROSTER
  // ==========================================
  if (urlPath === '/api/students' && req.method === 'GET') {
    try {
      const students = getStudentsSafe();
      sendJson(students);
    } catch (e) {
      sendJson([], 500);
    }
    return;
  }

  // Add student
  if (urlPath === '/api/students' && req.method === 'POST') {
    try {
      const student = await parseJsonBody(req);
      const students = getStudentsSafe();
      const newStudent = {
        id: student.id || `STU-${Date.now().toString().slice(-4)}`,
        name: student.name || 'Anonymous',
        grade: student.grade || 'Grade 1',
        session: student.session || 1,
        status: 'Pending',
        registeredAt: new Date().toISOString().split('T')[0]
      };
      students.unshift(newStudent);
      fs.writeFileSync(STUDENTS_FILE, JSON.stringify(students, null, 2), 'utf-8');
      sendJson({ success: true, student: newStudent });
    } catch (e) {
      sendJson({ success: false, error: e.message }, 500);
    }
    return;
  }

  // Update student
  if (urlPath === '/api/students/update' && req.method === 'POST') {
    try {
      const body = await parseJsonBody(req);
      const { id, name, grade, session } = body;
      const students = getStudentsSafe();
      const student = students.find(s => s.id === id);
      if (student) {
        if (name !== undefined) student.name = name;
        if (grade !== undefined) student.grade = grade;
        if (session !== undefined) student.session = parseInt(session, 10);
        fs.writeFileSync(STUDENTS_FILE, JSON.stringify(students, null, 2), 'utf-8');
        sendJson({ success: true, student });
        return;
      }
      sendJson({ success: false, error: 'Student not found' }, 404);
    } catch (e) {
      sendJson({ success: false, error: e.message }, 500);
    }
    return;
  }

  // Delete student
  if (urlPath === '/api/students/delete' && req.method === 'POST') {
    try {
      const { id } = await parseJsonBody(req);
      let students = getStudentsSafe();
      students = students.filter(s => s.id !== id);
      fs.writeFileSync(STUDENTS_FILE, JSON.stringify(students, null, 2), 'utf-8');
      sendJson({ success: true });
    } catch (e) {
      sendJson({ success: false, error: e.message }, 500);
    }
    return;
  }

  // ==========================================
  // REST API: TELEMETRY & RESULTS
  // ==========================================
  // Real-time trial telemetry
  if (urlPath === '/api/results/trial' && req.method === 'POST') {
    try {
      const trialData = await parseJsonBody(req);
      const results = getResultsSafe();
      results.push({
        id: `trial_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
        ...trialData,
        recordedAt: new Date().toISOString()
      });
      fs.writeFileSync(RESULTS_FILE, JSON.stringify(results, null, 2), 'utf-8');

      // Update student status in roster to "In Progress"
      if (trialData.participant) {
        const students = getStudentsSafe();
        const stu = students.find(s => s.id === trialData.participant);
        if (stu && stu.status === 'Pending') {
          stu.status = 'In Progress';
          fs.writeFileSync(STUDENTS_FILE, JSON.stringify(students, null, 2), 'utf-8');
        }
      }
      sendJson({ success: true });
    } catch (e) {
      sendJson({ success: false, error: e.message }, 500);
    }
    return;
  }

  // Session completion rollup
  if (urlPath === '/api/results/session' && req.method === 'POST') {
    try {
      const sessionSummary = await parseJsonBody(req);
      const { participant, session, totalTrials, correctCount, meanRt } = sessionSummary;
      const students = getStudentsSafe();
      const stu = students.find(s => s.id === participant);
      if (stu) {
        stu.status = 'Completed';
        stu.lastScore = `${correctCount}/${totalTrials} (${Math.round((correctCount / totalTrials) * 100)}%)`;
        stu.meanRt = `${Math.round(meanRt)} ms`;
        stu.completedAt = new Date().toISOString();
        fs.writeFileSync(STUDENTS_FILE, JSON.stringify(students, null, 2), 'utf-8');
      }
      sendJson({ success: true });
    } catch (e) {
      sendJson({ success: false, error: e.message }, 500);
    }
    return;
  }

  // Get all results
  if (urlPath === '/api/results' && req.method === 'GET') {
    try {
      const results = getResultsSafe();
      sendJson(results);
    } catch (e) {
      sendJson([], 500);
    }
    return;
  }

  // Clear results
  if (urlPath === '/api/results/clear' && req.method === 'POST') {
    try {
      fs.writeFileSync(RESULTS_FILE, JSON.stringify([], null, 2), 'utf-8');
      sendJson({ success: true });
    } catch (e) {
      sendJson({ success: false, error: e.message }, 500);
    }
    return;
  }

  // Export results CSV
  if (urlPath === '/api/results/export' && req.method === 'GET') {
    try {
      const results = getResultsSafe();
      let csv = "ID,Participant,Session,Stage,Word,RealPseudo,Correct,ReactionTime_ms,KeyPress,Timestamp\n";
      results.forEach(r => {
        csv += `"${r.id || ''}","${r.participant || ''}","${r.session || ''}","${r.stage || r.assessment_stage || ''}","${r.word || ''}","${r.realpseudo || ''}","${r.correct ? 1 : 0}","${r.reaction_time || r.rt || ''}","${r.key_response || r.response || ''}","${r.recordedAt || r.timestamp || ''}"\n`;
      });
      res.writeHead(200, {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': 'attachment; filename="kannada_roar_results.csv"',
        ...NO_CACHE_HEADERS
      });
      res.end(csv);
    } catch (e) {
      sendJson({ error: 'Failed to export CSV' }, 500);
    }
    return;
  }

  // ==========================================
  // STATIC ASSETS & PROXY
  // ==========================================
  const sanitizedPath = path.normalize(urlPath).replace(/^(\.\.[\/\\])+/, '');
  let filePath = path.join(PUBLIC_DIR, sanitizedPath === '\\' || sanitizedPath === '/' ? 'index.html' : sanitizedPath);

  fs.stat(filePath, (err, stats) => {
    // 1. Direct local file
    if (!err && stats.isFile()) {
      const ext = path.extname(filePath).toLowerCase();
      const contentType = MIME_TYPES[ext] || 'application/octet-stream';
      sendLocalFile(filePath, contentType);
      return;
    }

    // 2. Audio requests
    const ext = path.extname(urlPath).toLowerCase();
    if (ext === '.mp3') {
      let altPath = urlPath.startsWith('/audio/')
        ? path.join(PUBLIC_DIR, urlPath)
        : path.join(PUBLIC_DIR, 'audio', urlPath);
      
      if (fs.existsSync(altPath) && fs.statSync(altPath).isFile()) {
        sendLocalFile(altPath, 'audio/mpeg');
        return;
      }

      const filename = path.basename(urlPath);
      const knFallback = path.join(PUBLIC_DIR, 'audio', 'kn', 'desktop', filename);
      const sharedFallback = path.join(PUBLIC_DIR, 'audio', 'shared', filename);
      if (fs.existsSync(knFallback)) {
        sendLocalFile(knFallback, 'audio/mpeg');
        return;
      }
      if (fs.existsSync(sharedFallback)) {
        sendLocalFile(sharedFallback, 'audio/mpeg');
        return;
      }

      const dummyAudio = path.join(PUBLIC_DIR, 'audio', 'shared', 'coin.mp3');
      if (fs.existsSync(dummyAudio)) {
        sendLocalFile(dummyAudio, 'audio/mpeg');
        return;
      }
    }

    // 3. Graphic assets (.webp, .png, .jpg)
    if (['.webp', '.png', '.jpg', '.svg'].includes(ext)) {
      let remoteRelPath = urlPath.replace(/^\/audio\//, '/').replace(/^\//, '');
      remoteRelPath = remoteRelPath.replace(/^kn\//, 'en/').replace(/\/kn\//, '/en/');
      const remoteUrl = `${REMOTE_GCS_BASE}/${remoteRelPath}`;

      https.get(remoteUrl, (proxyRes) => {
        if (proxyRes.statusCode === 200) {
          res.writeHead(200, {
            'Content-Type': proxyRes.headers['content-type'] || MIME_TYPES[ext] || 'application/octet-stream',
            'Access-Control-Allow-Origin': '*',
            ...NO_CACHE_HEADERS,
          });
          proxyRes.pipe(res);
          return;
        }
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Asset Not Found: ' + urlPath);
      }).on('error', (proxyErr) => {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Asset Proxy Error: ' + proxyErr.message);
      });
      return;
    }

    // 4. SPA Route Fallback
    const fallbackPath = path.join(PUBLIC_DIR, 'index.html');
    sendLocalFile(fallbackPath, 'text/html; charset=utf-8');
  });
});

server.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(` ROAR SWR — Kannada Edition Server (V5 Professional)  `);
  console.log(` 1. Game URL:      http://localhost:${PORT}/?consent=false&storyoption=false `);
  console.log(` 2. Dashboard URL: http://localhost:${PORT}/dashboard.html `);
  console.log(` Status: Settings API + Live Results Telemetry Active   `);
  console.log(`=======================================================`);
});
