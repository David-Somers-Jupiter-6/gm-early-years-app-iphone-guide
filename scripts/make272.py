"""Guide 2.72 (from the 2.71 trial) - TRIAL (David, 17 Nov):
1. Every title box is the GM Early Years App colour - the plum to crimson of the ABC app logo
   (#6c155c -> #d01545), with the faded ABC blocks from 2.71. Contents and Search included.
2. Health Visiting team pages and NHS login pages use NHS blue (#003087 -> #005eb8):
   hv, s5-hv (Health Visiting team); s4-cannot-4, s4-signin, Steps A-H and their tips, s5-2 (NHS login).
   The NHS login account issues pages keep their NHS login band (2.70), already NHS blue.
usage: python3 make272.py v2.71.html v2.72.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
APP = 'linear-gradient(135deg,#6c155c 0%,#d01545 100%)'
NHS = 'linear-gradient(135deg,#003087 0%,#005eb8 100%)'
NHS_PAGES = ['hv', 's5-hv', 's4-cannot-4', 's4-signin', 's5-2'] + ['step-' + c for c in 'abcdefgh'] + ['step-%s-tip' % c for c in 'bcdefgh']
for p in NHS_PAGES:
    assert ('id="%s"' % p) in s, p
nhs_sel = ','.join('#app .screen#%s[data-sec]:not(#contents) .pbox,#app .screen#%s[data-sec]:not(#contents) .tp-card .tp-body' % (p, p) for p in NHS_PAGES)
CSS = ('/* 2.72 TRIAL: every title box in the GM Early Years App colour; Health Visiting team and NHS login pages in NHS blue */\n'
       '#app .screen[data-sec] .pbox:not(.nhs-band),#app .screen[data-sec]:not(#contents) .tp-card .tp-body,#app #contents .tp-card .tp-body{background:%s!important}\n'
       '%s{background:%s!important}\n') % (APP, nhs_sel, NHS)
rep('@media print{', CSS + '@media print{')
rep('Carer role v2.71', 'Carer role v2.72'); rep('Version 2.71 iPhone', 'Version 2.72 iPhone')
rep('<div>Version 2.71</div>', '<div>Version 2.72</div>'); rep('>2.71 – REVIEW DRAFT', '>2.72 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.69</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.71</span>', '<div class="rr"><span class="rv">2.72</span><span class="rd">17 Nov 2026</span><p>Trial: title boxes in the app colour; Health Visiting team and NHS login pages in NHS blue</p></div>\n<div class="rr"><span class="rv">2.71</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
