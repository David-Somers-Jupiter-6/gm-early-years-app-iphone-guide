"""Guide 3.04 (from 3.03). David, 19 Nov (from mock-up): checklist progress on the right-hand side of the title box
(bar and "Question N of 4" right-aligned) so it reads differently from "Stage N of 3" on the left. Checklist pages only
(c1-c4 and the summary); Signing in and NHS login steps unchanged. All screen heights.
usage: python3 make304.py v3.03.html v3.04.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
P = '#app .screen:not(#contents) .pbox:has(>.stepper.chk-steps)'
CSS = f'''/* 3.04 Checklist progress on the right of the title box (Signing in stays on the left) */
{P}>.stepper{{justify-content:flex-end!important}}
{P}>.kicker{{text-align:right!important}}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'
rep('Carer role v3.03', 'Carer role v3.04'); rep('Version 3.03 iPhone', 'Version 3.04 iPhone')
rep('<div>Version 3.03</div>', '<div>Version 3.04</div>'); rep('>3.03 – REVIEW DRAFT', '>3.04 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">3\.01</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.03</span>', '<div class="rr"><span class="rv">3.04</span><span class="rd">19 Nov 2026</span><p>Checklist progress on the right of the title box</p></div>\n<div class="rr"><span class="rv">3.03</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
