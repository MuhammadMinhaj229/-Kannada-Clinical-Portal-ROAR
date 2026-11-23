from pathlib import Path

REPO = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")

for p in [REPO / "index.f9505d51fec8273c6b0b.bundle.js", REPO / "public" / "index.f9505d51fec8273c6b0b.bundle.js"]:
    txt = p.read_text(encoding="utf-8")
    old1 = "gr=(0,t.bD)(Ge,mr,a),"
    new1 = 'gr=(0,t.bD)(Ge,mr,a),Object.keys(gr.images||{}).forEach(k=>{if(gr.images[k]&&!gr.images[k].includes("?"))gr.images[k]+="?v=kn13"}),'
    if old1 in txt and new1 not in txt:
        txt = txt.replace(old1, new1, 1)

    old2 = 'fr.images=(fr.images||[]).filter(x=>x.includes("arrow")||x.includes("coin"))'
    new2 = 'fr.images=(fr.images||[]).filter(x=>x.includes("arrow")||x.includes("coin")).map(x=>x.includes("?")?x:x+"?v=kn13")'
    if old2 in txt and new2 not in txt:
        txt = txt.replace(old2, new2, 1)

    p.write_text(txt, encoding="utf-8")
    print(f"Updated {p} (kn13 present: {'kn13' in txt})")

# Also update dashboard.html and public/dashboard.html to clear stale roarCustomSessionsData on version bump
for d in [REPO / "dashboard.html", REPO / "public" / "dashboard.html"]:
    txt = d.read_text(encoding="utf-8")
    old_d = "function initWordsTab() {\n  var stored = LS.get('roarCustomSessionsData', null);"
    new_d = """function initWordsTab() {
  if (localStorage.getItem('roarCorpusVersion') !== 'kn13') {
    localStorage.removeItem('roarCustomSessionsData');
    localStorage.setItem('roarCorpusVersion', 'kn13');
  }
  var stored = LS.get('roarCustomSessionsData', null);"""
    if old_d in txt:
        txt = txt.replace(old_d, new_d, 1)
        d.write_text(txt, encoding="utf-8")
        print(f"Updated {d} with kn13 version guard")
    else:
        print(f"Note: initWordsTab pattern not matched in {d}")
