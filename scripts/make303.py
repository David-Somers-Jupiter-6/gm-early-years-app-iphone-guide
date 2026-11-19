"""Guide 3.03 (from 3.02). David, 19 Nov: the checklist progress bar the same size and colours as Signing in.
 - segments the width of a Signing in step segment: (bar width - 14 gaps of 3 px - 2 part gaps of 7 px) / 15
 - colours: answered = green (Yes or No), current = white (stays white after answering), to come = faint; no red
   (dark mode: current stays #111821, as Signing in)
usage: python3 make303.py v3.02.html v3.03.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
B = '#app .screen:not(#contents) .pbox .stepper.chk-steps'
CSS = f'''/* 3.03 Checklist progress bar = Signing in bar: same segment size, same colours (green answered, white current, no red) */
{B} span{{flex:0 0 calc((100% - 56px) / 15)!important;width:auto!important}}
{B} span.bad{{background:#5fd38d!important}}
#app .screen:not(#contents):has(.ans-yes:checked) .pbox .stepper.chk-steps span.cur,#app .screen:not(#contents):has(.ans-no:checked) .pbox .stepper.chk-steps span.cur{{background:#fff!important}}
@media screen and (prefers-color-scheme:dark){{#app .screen:not(#contents):has(.ans-yes:checked) .pbox .stepper.chk-steps span.cur,#app .screen:not(#contents):has(.ans-no:checked) .pbox .stepper.chk-steps span.cur{{background:#111821!important}}}}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'
rep('Carer role v3.02', 'Carer role v3.03'); rep('Version 3.02 iPhone', 'Version 3.03 iPhone')
rep('<div>Version 3.02</div>', '<div>Version 3.03</div>'); rep('>3.02 – REVIEW DRAFT', '>3.03 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">3\.00</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.02</span>', '<div class="rr"><span class="rv">3.03</span><span class="rd">19 Nov 2026</span><p>Checklist progress bar the same size and colours as Signing in</p></div>\n<div class="rr"><span class="rv">3.02</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
