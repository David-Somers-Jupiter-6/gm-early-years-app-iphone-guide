"""Guide 2.60 (from 2.59).
- Section 1 Your Health Visiting team page (hv) only: removed the first line,
  "Your team can check your account and link." (David). Contact & support's team page keeps it.
usage: python3 make260.py v2.59.html v2.60.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def edit(pid, a, b, n=1):
    global s
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

LEAD = '<p class="info-lead hv-lead">Your team can check your account and link.</p>\n'
assert s.count(LEAD) == 2
edit('hv', LEAD, ''); edit('s5-hv', LEAD, LEAD)
assert s.count(LEAD) == 1

rep('Carer role v2.59', 'Carer role v2.60'); rep('Version 2.59 iPhone', 'Version 2.60 iPhone')
rep('<div>Version 2.59</div>', '<div>Version 2.60</div>'); rep('>2.59 – REVIEW DRAFT', '>2.60 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.57</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.59</span>', '<div class="rr"><span class="rv">2.60</span><span class="rd">16 Nov 2026</span><p>Section 1 team page: removed "Your team can check your account and link."</p></div>\n<div class="rr"><span class="rv">2.59</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
