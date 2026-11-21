"""Guide 3.17 (from 3.16) – TRIAL (/preview/ only). David, 21 Nov:
 - Cover: "Help with a problem" removed (the guide should lead people through the questions, not let them guess).
 - Cover Search row: "Type or say what you need" under Search, and a round microphone button on the right.
   Tapping the microphone opens Search and starts listening straight away.
 - Search page: the microphone in the search box is always shown (it used to be hidden where Safari's own voice
   search is not available, e.g. on the Home Screen). Where voice search is not available, tapping it opens the
   keyboard and says "Now tap the microphone at the bottom of your keyboard". A web page cannot switch on the
   keyboard's own microphone for you (Apple does not allow it).
usage: python3 make317.py v3.16.html v3.17.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

CH = '<svg class="cv-ch" viewBox="0 0 20 20" width="16" height="16" aria-hidden="true"><path d="M7.5 4.5L13 10l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
MIC = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0013 0M12 17.5V21"/></svg>'

# 1. cover: remove Help with a problem
m = re.search(r'<a href="#s4"><span class="cv-ai cv-a2">.*?<span class="cv-t">Help with a problem</span>' + re.escape(CH) + '</a>', s, re.S)
assert m; s = s.replace(m.group(0), '')
# 2. cover: Search row with a microphone button
m = re.search(r'<a href="#search">(<span class="cv-ai cv-a3">.*?</span>)<span class="cv-t">Search</span>' + re.escape(CH) + '</a>', s, re.S)
assert m
s = s.replace(m.group(0), '<div class="cv-sr"><a href="#search" class="cv-sl">' + m.group(1) +
              '<span class="cv-t">Search<span class="cv-st">Type or say what you need</span></span></a>'
              '<a href="#search" class="cv-mic" aria-label="Search by speaking"><span class="cv-mb">' + MIC + '</span></a></div>')

CSS = """/* 3.17 cover Search row with microphone */
#app #cover .cv-sr{display:flex;align-items:stretch;border-top:1px solid #e3e7ea}
#app #cover .cv-rows .cv-sr a{border-top:0}
#app #cover .cv-sl{flex:1 1 auto;min-width:0}
#app #cover .cv-st{display:block;margin-top:2px;font:400 14px/1.25 var(--font-body);color:#5a6b73}
#app #cover .cv-rows a.cv-mic{flex:0 0 auto;padding:0 12px 0 6px;min-width:44px;justify-content:center}
#app #cover .cv-mb{width:38px;height:38px;border-radius:50%;background:#d5573b;color:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 1px 3px rgba(31,58,71,.25)}
#app #cover .cv-mic:active .cv-mb{background:#b5432a}
@media (prefers-color-scheme:dark){
  #app #cover .cv-sr{border-color:#33464f}
  #app #cover .cv-st{color:#b9c4ca}
}
"""
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:')
_css = s[:s.index('@media print{')]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

# 3. search microphone always shown; keyboard fallback
rep("""    if(!SR||!mic||location.protocol!=='https:'||home) return;
    hasMic=true; mic.hidden=false; pg.classList.add('has-mic');""",
"""    if(!mic) return;
    var speech=!!SR&&location.protocol==='https:'&&!home;
    hasMic=true; mic.hidden=false; pg.classList.add('has-mic');""")
rep("""    function off(){ stop(); hasMic=false; mic.hidden=true; pg.classList.remove('has-mic');
      st.innerHTML='Voice search is not available here. Tap the search box, then the <strong>microphone on your keyboard</strong>, to speak.'; }""",
"""    /* where Safari cannot listen: open the keyboard and point to its microphone (a page cannot switch that on) */
    function kb(){ stop(); try{ q.focus(); }catch(x){} st.innerHTML='Now tap the <strong>microphone</strong> at the bottom of your keyboard and say what you need help with.'; }
    function off(){ stop(); speech=false;
      st.innerHTML='Voice search is not available here. Tap the <strong>microphone</strong> again to use the one on your keyboard.'; }""")
rep("""      e.preventDefault(); if(on){ stop(); if(got) run(); else hint(); return; }
      try{ rec=new SR(); }catch(x){ off(); return; }""",
"""      e.preventDefault(); if(on){ stop(); if(got) run(); else hint(); return; }
      if(!speech){ kb(); return; }
      try{ rec=new SR(); }catch(x){ speech=false; kb(); return; }""")
m = re.search(r"      try\{ rec\.start\(\); \}catch\(x\)\{ off\(\); \}\n    \}\);\n  \}\)\(\);", s); assert m
s = s.replace(m.group(0), """      try{ rec.start(); }catch(x){ speech=false; kb(); }
    });
    /* cover microphone: the page has just opened Search (same tap), so start listening */
    d.addEventListener('click',function(e){ if(e.target.closest&&e.target.closest('#cover .cv-mic')) mic.click(); });
  })();""")

rep('Carer role v3.16', 'Carer role v3.17'); rep('Version 3.16 iPhone', 'Version 3.17 iPhone')
rep('>3.16 – REVIEW DRAFT', '>3.17 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.16</span>', '<span class="cv-ver">Version 3.17</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.14</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.16</span>', '<div class="rr"><span class="rv">3.17</span><span class="rd">21 Nov 2026</span><p>Cover: Help with a problem removed; Search by speaking</p></div>\n<div class="rr"><span class="rv">3.16</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
