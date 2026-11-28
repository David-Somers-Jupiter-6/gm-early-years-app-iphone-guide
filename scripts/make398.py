"""Guide 3.98 (from 3.97) – fix (David, 28 Nov): after closing the step 1 clip/screenshot, the picture came back the wrong size.
Cause: Safari's toolbars change size while the whole-screen view is open, so fit() measured the enlarged picture and kept that
size (--maxh 560px) after closing. Fix: fit() is skipped while a whole-screen view is open, and runs again when it closes
(tap or Escape). Applies to every screenshot in the guide.
Also (David): Search for the App instructions as numbered steps (abc-steps list); the Tap Search chip goes (step 1 of the list says it).
usage: python3 make398.py v3.97.html v3.98.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)
rep('content="Version 3.97. A screen-by-screen', 'content="Version 3.98. A screen-by-screen')
rep('>3.97 (iPhone edition)<', '>3.98 (iPhone edition)<')
rep('<span class="cv-ver">Version 3.97</span>', '<span class="cv-ver">Version 3.98</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.92</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.97</span>', '<div class="rr"><span class="rv">3.98</span><span class="rd">28 Nov 2026</span><p>Pictures keep their size after closing the whole-screen view</p></div>\n<div class="rr"><span class="rv">3.97</span>')
rep("return base()+n+'.mp4?v=3.97';", "return base()+n+'.mp4?v=3.98';")
rep('function refit(){ fit(); dbg(); }',
    'function refit(){ if(zoomOpen()) return; fit(); dbg(); }   /* 3.98: never measure while a whole-screen view is open */')
rep("function check(){ tsAlign(); refit(); clearTimeout(ft1); clearTimeout(ft2); ft1=setTimeout(refit,350); ft2=setTimeout(refit,1200); }",
    "function check(){ tsAlign(); refit(); clearTimeout(ft1); clearTimeout(ft2); ft1=setTimeout(refit,350); ft2=setTimeout(refit,1200); }\n"
    "  d.addEventListener('change',function(e){ var t=e.target; if(t&&t.classList&&t.classList.contains('zt')&&!t.checked) check(); });   /* 3.98: re-fit after closing */")
rep("var z=zoomOpen(); if(z){ if(e.key==='Escape') z.checked=false; return; }",
    "var z=zoomOpen(); if(z){ if(e.key==='Escape'){ z.checked=false; check(); } return; }")
rep('<p>Tap <strong>Search</strong> at the bottom of the App Store. Tap the search box and type <strong>gm early years</strong>. '
    'Look for <strong>GM Early Years</strong> by Greater Manchester Early Years.</p>\n'
    '<div class="tap"><span class="lbl">Tap</span><span class="chip">Search</span></div>\n',
    '<ol class="abc-steps inst-steps"><li>Tap <strong>Search</strong> at the bottom of the App Store.</li>'
    '<li>Tap the search box and type <strong>gm early years</strong>.</li>'
    '<li>Look for <strong>GM Early Years</strong> by Greater Manchester Early Years.</li></ol>\n')
rep('<p>Pictures keep their size after closing the whole-screen view</p>', '<p>Search for the App: numbered steps; pictures keep their size after closing the whole-screen view</p>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, len(s))
