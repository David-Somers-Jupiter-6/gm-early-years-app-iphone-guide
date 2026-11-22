"""Guide 3.41 (from trial 3.40) – TRIAL. David, 22 Nov: question 1's title is "Who is set up with an account?"
(was "Who is the account for?"), also in the start page list. Its second line now reads "In this guide, we call this
person the account holder." (was "This troubleshooter should be answered by …").
usage: python3 make341.py v3.40.html v3.41.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
OLD, NEW = 'Who is the account for?', 'Who is set up with an account?'
rep('<span aria-hidden="true">1</span>%s</li>' % OLD, '<span aria-hidden="true">1</span>%s</li>' % NEW)
rep('data-title="Troubleshooter · %s"' % OLD, 'data-title="Troubleshooter · %s"' % NEW)
rep('<span class="vh">Question 1 of 7: </span>%s</h2>' % OLD, '<span class="vh">Question 1 of 7: </span>%s</h2>' % NEW)
rep('<p class="q-why ts-who">This troubleshooter should be answered by the <strong>child’s mother or primary carer</strong>, <strong>not a partner or family member</strong>.</p>',
    '<p class="q-why ts-who">In this guide, we call this person the <strong>account holder</strong>.</p>')
CSS = "/* 3.41 question 1's longer title stays on one line on short screens (where the title box has room for one line) */\n@media screen and (max-height:600px){#app #ts1 .pbox h2{font-size:18.5px!important;letter-spacing:-.01em;white-space:nowrap;line-height:26px!important;height:26px}}\n"
anchor = '/* 2.88 Step 1:'; assert s.count(anchor) == 1; s = s.replace(anchor, CSS + anchor)
rep('Carer role v3.40', 'Carer role v3.41'); rep('Version 3.40 iPhone', 'Version 3.41 iPhone')
rep('>3.40 – REVIEW DRAFT', '>3.41 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.40</span>', '<span class="cv-ver">Version 3.41</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.36</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.40</span>', '<div class="rr"><span class="rv">3.41</span><span class="rd">22 Nov 2026</span><p>Question 1: Who is set up with an account?; account holder line</p></div>\n<div class="rr"><span class="rv">3.40</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
