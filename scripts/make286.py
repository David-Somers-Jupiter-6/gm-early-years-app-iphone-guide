"""Guide 2.86 (from 2.85). David, 18 Nov:
 1. Section 4 page 1 title: "Contact your HV team" (was "Contact your team").
 2. Team cards (Section 4 and Section 8): "Tap the <b>contact number</b> to <b>call</b>."
usage: python3 make286.py v2.85.html v2.86.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('<h2 class="h2" tabindex="-1">Contact your team</h2>', '<h2 class="h2" tabindex="-1">Contact your HV team</h2>')
rep('<p class="hv-tap">Tap the contact number to call.</p>', '<p class="hv-tap">Tap the <strong>contact number</strong> to <strong>call</strong>.</p>', 46)
rep('Carer role v2.85', 'Carer role v2.86'); rep('Version 2.85 iPhone', 'Version 2.86 iPhone')
rep('<div>Version 2.85</div>', '<div>Version 2.86</div>'); rep('>2.85 – REVIEW DRAFT', '>2.86 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.83</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.85</span>', '<div class="rr"><span class="rv">2.86</span><span class="rd">18 Nov 2026</span><p>Title "Contact your HV team"; call note in bold</p></div>\n<div class="rr"><span class="rv">2.85</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
