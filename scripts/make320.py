"""Guide 3.20 (from 3.19) – TRIAL (/preview/ only). David, 21 Nov: make the team finder on "Contact your HV team"
really simple.
 - Lead line: "If you need to contact your Health Visiting team, you can find their contact details below."
   (was "Find your team's contact details:").
 - The two choices are now steps, one under the other, each saying what to do:
     1 Choose your area                      (was: Locality)
     2 Choose your Health Visiting team      (was: Health Visiting team; "Choose your HV team" on the narrowest phones)
   and the team list says "Choose your area first" until an area is chosen (was: "Choose a locality first").
 - Same change on Section 7 · Contact your HV team (s5-hv), which uses the same finder.
 - Room: when a team is chosen and the contact card appears, the lead line and the "Tap the contact number to
   call" line give way where the screen is too short (the page re-fits when a choice changes), so the page still
   fits without scrolling.
usage: python3 make320.py v3.19.html v3.20.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

rep('<p class="q-hint hv-how">Find your team’s contact details:</p>',
    '<p class="q-hint hv-how fit-opt">If you need to contact your Health Visiting team, you can find their contact details below.</p>', 2)
rep('<span class="hv-num" aria-hidden="true">1</span>Locality</label>',
    '<span class="hv-num" aria-hidden="true">1</span>Choose your area</label>', 2)
rep('<span class="hv-num" aria-hidden="true">2</span><span class="hv-lt-l">Health Visiting team</span><span class="hv-lt-s" aria-hidden="true">HV team</span></label>',
    '<span class="hv-num" aria-hidden="true">2</span><span class="hv-lt-l">Choose your Health Visiting team</span><span class="hv-lt-s" aria-hidden="true">Choose your HV team</span></label>', 2)
rep('>Choose a locality first<', '>Choose your area first<', 2)
n = s.count('<p class="hv-tap">'); assert n >= 40, n
s = s.replace('<p class="hv-tap">', '<p class="hv-tap fit-opt">')

CSS = """/* 3.20 HV team finder: two steps, one under the other */
#app :is(#hv,#s5-hv) .hv-row{flex-direction:column;gap:10px}
#app :is(#hv,#s5-hv) :is(.hv-f-loc,.hv-f-team){flex:0 0 auto;width:100%}
#app :is(#hv,#s5-hv) .hv-f label{white-space:normal;overflow:visible;font-size:17px!important;color:var(--ink);margin-bottom:5px}
#app :is(#hv,#s5-hv) .hv-how{margin-bottom:10px!important}
@media screen and (max-height:600px){#app :is(#hv,#s5-hv) .hv-row{gap:7px}#app :is(#hv,#s5-hv) .hv-f label{margin-bottom:3px}#app :is(#hv,#s5-hv) .hv-how{margin-bottom:7px!important}}
"""
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:')
_css = s[:s.index('@media print{')]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

# re-fit the page when a team-finder choice changes (the contact card appears)
rep("d.addEventListener('change',function(e){ if(e.target.classList&&e.target.classList.contains('ans')) paintDots(); });",
    "d.addEventListener('change',function(e){ if(e.target.classList&&e.target.classList.contains('ans')) paintDots();\n"
    "    if(e.target.closest&&e.target.closest('.hv-find,.hv-card')) check(); });")

rep('Carer role v3.19', 'Carer role v3.20'); rep('Version 3.19 iPhone', 'Version 3.20 iPhone')
rep('>3.19 – REVIEW DRAFT', '>3.20 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.19</span>', '<span class="cv-ver">Version 3.20</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.17</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.19</span>', '<div class="rr"><span class="rv">3.20</span><span class="rd">21 Nov 2026</span><p>Contact your HV team: simpler team finder in two steps</p></div>\n<div class="rr"><span class="rv">3.19</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
