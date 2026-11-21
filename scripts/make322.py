"""Guide 3.22 (from 3.19; replaces trials 3.20 and 3.21) – TRIAL (/preview/ only). David, 21 Nov: leave the team
finder as it was ("Find your team's contact details:", Locality and Health Visiting team side by side) and change
the page title instead.
 - Section 2 page title: "How to contact your HV team" (was "Contact your HV team").
usage: python3 make322.py v3.19.html v3.22.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

rep('<h2 class="h2" tabindex="-1">Contact your HV team</h2>', '<h2 class="h2" tabindex="-1">How to contact your HV team</h2>')
rep('Carer role v3.19', 'Carer role v3.22'); rep('Version 3.19 iPhone', 'Version 3.22 iPhone')
rep('>3.19 – REVIEW DRAFT', '>3.22 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.19</span>', '<span class="cv-ver">Version 3.22</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.17</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.19</span>', '<div class="rr"><span class="rv">3.22</span><span class="rd">21 Nov 2026</span><p>Section 2 title: How to contact your HV team</p></div>\n<div class="rr"><span class="rv">3.19</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
