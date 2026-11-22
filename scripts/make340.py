"""Guide 3.40 (from trial 3.39) – TRIAL. David, 22 Nov: on the Troubleshooter start page, after the list of
questions: "This troubleshooter should be answered by the child's mother or primary carer, not a partner or family
member." "Answer Yes or No. It takes a minute or two." stays at the end. The list rows are a little tighter.
David is fine with the page scrolling on smaller iPhones for now: the page will be cut down later.
usage: python3 make340.py v3.39.html v3.40.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
m = re.search(r'<section class="screen" id="ts".*?</section>', s, re.S); blk = m.group(0)
a = '</ol>\n<p class="cq-end">Answer <strong>Yes</strong> or <strong>No</strong>. It takes a minute or two.</p>'
assert blk.count(a) == 1
blk = blk.replace(a, '</ol>\n<p class="cq-end cq-who">This troubleshooter should be answered by the <strong>child’s mother or primary carer</strong>, '
                     '<strong>not a partner or family member</strong>.</p>\n<p class="cq-end">Answer <strong>Yes</strong> or <strong>No</strong>. It takes a minute or two.</p>')
s = s[:m.start()] + blk + s[m.end():]
CSS = """/* 3.40 Troubleshooter start page: who should answer; list a little tighter */
#app #ts .cq li{padding:5px 12px!important;font-size:16.5px}#app #ts .cq li>span{flex-basis:24px;height:24px}
#app #ts .cq-end{margin-top:10px!important;font-size:16.5px;line-height:1.35}#app #ts .cq-lead{margin-bottom:10px!important}
#app #ts .cq-who+.cq-end{margin-top:8px!important}
@media screen and (max-height:660px){#app #ts .cq li{padding:3px 12px!important;font-size:16px}#app #ts .cq-lead{font-size:16px!important;line-height:1.35!important}#app #ts .cq-end{font-size:16px;margin-top:8px!important}}
"""
anchor = '/* 2.88 Step 1:'; assert s.count(anchor) == 1; s = s.replace(anchor, CSS + anchor); assert CSS.count('{') == CSS.count('}')
rep('Carer role v3.39', 'Carer role v3.40'); rep('Version 3.39 iPhone', 'Version 3.40 iPhone')
rep('>3.39 – REVIEW DRAFT', '>3.40 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.39</span>', '<span class="cv-ver">Version 3.40</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.35</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.39</span>', '<div class="rr"><span class="rv">3.40</span><span class="rd">22 Nov 2026</span><p>Troubleshooter start page: who should answer</p></div>\n<div class="rr"><span class="rv">3.39</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
