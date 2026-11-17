"""Guide 2.80 (from 2.79). Check your NHS account details: the NHS login sign-in steps are numbered 1 to 8
instead of lettered A to H (David, 17 Nov): band ("Step 3 of 8"), page names, screen reader text, tip pages and
the "continue at Step 7" link. Page ids (step-a ... step-h) are unchanged.
Step 8 and its note page renamed "Your NHS account page", so they no longer share the title of the list item
"Check your NHS account details".
Steps 1-8 and their tip pages have the slim progress bar used in Section 3 Signing in (8 segments: done green,
current white), under the NHS login band; title boxes on these pages are 128 px (as in the banded version) so a
two-line title fits. iPhone SE in Safari: the band is hidden on these pages and the label shows, as elsewhere.
usage: python3 make280.py v2.79.html v2.80.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
N = {c: str(i) for i, c in enumerate('ABCDEFGH', 1)}
s, n1 = re.subn(r'\bStep ([A-H])\b', lambda m: 'Step ' + N[m.group(1)], s)
s, n2 = re.subn(r'\bof H\b', 'of 8', s)
s, n3 = re.subn(r'(<span class="tp-n" aria-hidden="true">)([A-H])(</span>)', lambda m: m.group(1) + N[m.group(2)] + m.group(3), s)
s, n4 = re.subn(r'\bSteps B-H\b', 'Steps 2-8', s)
assert (n1, n2, n3) == (76, 30, 15), (n1, n2, n3)
assert not re.search(r'\bStep [A-H]\b', re.sub(r'data:[^"\')]+', '', s))
# Step 8 (and its note page) renamed so it no longer shares a title with the list item (David: "1. Yes")
rep('data-title="Step 8 · Check your NHS account details"', 'data-title="Step 8 · Your NHS account page"')
rep('<span class="vh">Step 8: </span>Check your NHS account details</h2>', '<span class="vh">Step 8: </span>Your NHS account page</h2>')
rep('<span class="vh">Note – Step 8: </span>Check your NHS account details</h2>', '<span class="vh">Note – Step 8: </span>Your NHS account page</h2>')
assert s.count('Check your NHS account details') >= 2
# progress bar on Steps 1-8 and their tip pages, like Section 3 Signing in (David: "6. Add a progress bar")
STEP = {'step-a': 1, 'step-b': 2, 'step-b-tip': 2, 'step-c': 3, 'step-c-tip': 3, 'step-d': 4, 'step-d-tip': 4, 'step-e': 5,
        'step-e-tip': 5, 'step-f': 6, 'step-f-tip': 6, 'step-g': 7, 'step-g-tip': 7, 'step-h': 8, 'step-h-tip': 8}
for pid, n in STEP.items():
    m = re.search(r'<section class="screen" id="%s".*?</section>' % pid, s, re.S); blk = m.group(0)
    bar = '<div class="stepper nhs-steps" aria-hidden="true">' + ''.join(
        '<span class="d">\u2713</span>' if i < n else ('<span class="c">%d</span>' % i if i == n else '<span class="">%d</span>' % i) for i in range(1, 9)) + '</div>'
    tag = '<span class="tp-n" aria-hidden="true">%d</span>' % n
    assert blk.count(tag) == 1, pid
    s = s[:m.start()] + blk.replace(tag, bar + tag) + s[m.end():]
assert s.count('class="stepper nhs-steps"') == 15
NS = '.stepper.nhs-steps'
CSS = ('/* 2.80 NHS login sign-in steps: slim progress bar like Section 3 Signing in */\n'
  + NS + '{display:flex;gap:3px;margin:2px 0 16px;align-items:center;justify-content:flex-start;height:8px;box-sizing:content-box}\n'
  + NS + ' span{overflow:hidden;text-indent:-99px;flex:1 1 0;width:auto;height:6px;border-radius:3px;border:0;font-size:0;color:transparent;transform:none}\n'
  + NS + ' span.c{height:8px}\n'
  + '@media (min-height:601px){#app .screen:is(#step-a,#step-b,#step-b-tip,#step-c,#step-c-tip,#step-d,#step-d-tip,#step-e,#step-e-tip,#step-f,#step-f-tip,#step-g,#step-g-tip,#step-h,#step-h-tip):not(#contents) :is(.pbox,.tp-body).eyx:has(.stepper){min-height:128px!important}}\n')
rep('@media print{', CSS + '@media print{')
rep('Carer role v2.79', 'Carer role v2.80'); rep('Version 2.79 iPhone', 'Version 2.80 iPhone')
rep('<div>Version 2.79</div>', '<div>Version 2.80</div>'); rep('>2.79 – REVIEW DRAFT', '>2.80 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.77</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.79</span>', '<div class="rr"><span class="rv">2.80</span><span class="rd">17 Nov 2026</span><p>NHS login sign-in steps numbered 1 to 8 with a progress bar; Step 8 renamed Your NHS account page</p></div>\n<div class="rr"><span class="rv">2.79</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, n1, n2, n3, n4)
