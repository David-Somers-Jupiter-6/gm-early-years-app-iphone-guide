"""Guide 3.21 (from 3.19; replaces trial 3.20) – TRIAL (/preview/ only). David, 21 Nov: in 3.20 the two steps one
under the other made the page too long when the Map is chosen (the map shrank to about 100 px on small iPhones and
the page still scrolled). Keep the new lead line, and keep Locality and Health Visiting team side by side.
 - Contact your HV team (Section 2 and Section 7): lead line "If you need to contact your Health Visiting team, you
   can find their contact details below." (was "Find your team's contact details:"). Always shown.
 - Choices stay side by side as before: 1 Locality, 2 Health Visiting team.
 - The page re-fits when a choice changes; "Tap the contact number to call" gives way if the screen is too short.
usage: python3 make321.py v3.19.html v3.21.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

rep('<p class="q-hint hv-how">Find your team’s contact details:</p>',
    '<p class="q-hint hv-how">If you need to contact your Health Visiting team, you can find their contact details below.</p>', 2)
n = s.count('<p class="hv-tap">'); assert n >= 40, n
s = s.replace('<p class="hv-tap">', '<p class="hv-tap fit-opt">')
rep("d.addEventListener('change',function(e){ if(e.target.classList&&e.target.classList.contains('ans')) paintDots(); });",
    "d.addEventListener('change',function(e){ if(e.target.classList&&e.target.classList.contains('ans')) paintDots();\n"
    "    if(e.target.closest&&e.target.closest('.hv-find,.hv-card')) check(); });")

rep('Carer role v3.19', 'Carer role v3.21'); rep('Version 3.19 iPhone', 'Version 3.21 iPhone')
rep('>3.19 – REVIEW DRAFT', '>3.21 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.19</span>', '<span class="cv-ver">Version 3.21</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.17</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.19</span>', '<div class="rr"><span class="rv">3.21</span><span class="rd">21 Nov 2026</span><p>Contact your HV team: clearer lead line (3.20 two-step layout withdrawn)</p></div>\n<div class="rr"><span class="rv">3.19</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
