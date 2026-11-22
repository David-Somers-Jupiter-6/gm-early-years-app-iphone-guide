"""Guide 3.55 (from trial 3.54) – TRIAL. David, 22 Nov, question 4 (was "NHS login access"):
 - title "Do you have NHS login?" ("Do you have an NHS login?" took two lines) (also in the start page list);
 - the "Not sure? Try it on the NHS website / Try signing in" box is removed.
usage: python3 make355.py v3.54.html v3.55.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
NEW = 'Do you have NHS login?'
rep('data-title="Troubleshooter · NHS login access"', 'data-title="Troubleshooter · %s"' % NEW)
rep('<span class="vh">Question 4 of 6: </span>NHS login access</h2>', '<span class="vh">Question 4 of 6: </span>%s</h2>' % NEW)
rep('<span aria-hidden="true">4</span>NHS login access</li>', '<span aria-hidden="true">4</span>%s</li>' % NEW)
m = re.search(r'<section class="screen" id="ts3".*?</section>', s, re.S); blk = m.group(0)
blk2, n = re.subn(r'\n?<div class="ts-tip">.*?</a></div></div>', '', blk, flags=re.S); assert n == 1 and 'ts-try' not in blk2
s = s[:m.start()] + blk2 + s[m.end():]
rep('Carer role v3.54', 'Carer role v3.55'); rep('Version 3.54 iPhone', 'Version 3.55 iPhone')
rep('>3.54 – REVIEW DRAFT', '>3.55 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.54</span>', '<span class="cv-ver">Version 3.55</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.50</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.54</span>', '<div class="rr"><span class="rv">3.55</span><span class="rd">22 Nov 2026</span><p>Question 4: Do you have NHS login?; Try signing in box removed</p></div>\n<div class="rr"><span class="rv">3.54</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
