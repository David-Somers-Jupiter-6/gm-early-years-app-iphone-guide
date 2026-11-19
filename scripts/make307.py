"""Guide 3.07 (from 3.06). David, 19 Nov: checklist progress bar colours change as soon as an answer is chosen:
the current question's segment turns green for Yes and red for No (before Next), and earlier answers stay green (Yes)
or red (No). This removes the 3.03 colour overrides (answered = green, current stays white); 3.03 segment size and
3.04 right-hand position are kept. Dark Mode uses the existing rules (same green/red).
usage: python3 make307.py v3.06.html v3.07.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
B = '#app .screen:not(#contents) .pbox .stepper.chk-steps'
rep(f'{B} span.bad{{background:#5fd38d!important}}\n', '')
rep('#app .screen:not(#contents):has(.ans-yes:checked) .pbox .stepper.chk-steps span.cur,#app .screen:not(#contents):has(.ans-no:checked) .pbox .stepper.chk-steps span.cur{background:#fff!important}\n', '')
rep('@media screen and (prefers-color-scheme:dark){#app .screen:not(#contents):has(.ans-yes:checked) .pbox .stepper.chk-steps span.cur,#app .screen:not(#contents):has(.ans-no:checked) .pbox .stepper.chk-steps span.cur{background:#111821!important}}\n', '')
rep('/* 3.03 Checklist progress bar = Signing in bar: same segment size, same colours (green answered, white current, no red) */',
    '/* 3.03 Checklist progress bar = Signing in bar segment size (3.07: colours back to green Yes / red No, shown on selection) */')
rep('Carer role v3.06', 'Carer role v3.07'); rep('Version 3.06 iPhone', 'Version 3.07 iPhone')
rep('<div>Version 3.06</div>', '<div>Version 3.07</div>'); rep('>3.06 – REVIEW DRAFT', '>3.07 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">3\.04</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.06</span>', '<div class="rr"><span class="rv">3.07</span><span class="rd">19 Nov 2026</span><p>Checklist progress bar: green for Yes, red for No, as soon as an answer is chosen</p></div>\n<div class="rr"><span class="rv">3.06</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
