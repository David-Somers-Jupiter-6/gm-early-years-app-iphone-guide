"""Guide 2.65 (from 2.64). Checklist questions line up (David, 17 Nov, Option B):
on all four question pages the section line, the first line of the explanation, the first line
of the question, the top of the Yes box and the top of the No box are at the same height.
- The explanation (q-why) always takes the space of three lines; the question (q-ask) the space
  of two lines.
- Q3 question: "Do both accounts use the same email address and mobile number?" (fits two lines).
- Q4 message after No: "Select Next to see your checklist summary."
usage: python3 make265.py v2.64.html v2.65.html
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

edit('c3', '<p class="q-ask" id="ask-c3">Does your GM Early Years App account use the same email address and mobile number as your NHS login account?</p>',
     '<p class="q-ask" id="ask-c3">Do both accounts use the same email address and mobile number?</p>')
edit('c4', '<p>Select <strong>Next</strong> to see your checklist summary and what to do next.</p>',
     '<p>Select <strong>Next</strong> to see your checklist summary.</p>')
rep('@media print{', '/* 2.65 checklist questions line up */\n'
    '#app .screen .q-why{min-height:calc(3 * 1.4em)!important}\n'
    '#app .screen .q-ask{min-height:calc(2 * 1.35em)}\n@media print{')

rep('Carer role v2.64', 'Carer role v2.65'); rep('Version 2.64 iPhone', 'Version 2.65 iPhone')
rep('<div>Version 2.64</div>', '<div>Version 2.65</div>'); rep('>2.64 – REVIEW DRAFT', '>2.65 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.62</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.64</span>', '<div class="rr"><span class="rv">2.65</span><span class="rd">17 Nov 2026</span><p>Checklist questions and answers line up on every question page</p></div>\n<div class="rr"><span class="rv">2.64</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
