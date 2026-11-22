"""Guide 3.39 (from trial 3.38) – TRIAL. David, 22 Nov: on "Who the account is for", the "Who it is for" row adds
a new line: "In this guide, we call this person the account holder." What to do: "The account holder signs in
with their own NHS login." (was "The child's mother or primary carer signs in…") and "Not sure? Ask the team.", which keeps the page
from scrolling. On the smallest screens "Still stuck?" gives way if needed.
usage: python3 make339.py v3.38.html v3.39.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('<p>Your Health Visiting team creates the GM Early Years App account for the <strong>child’s mother or primary carer</strong>.</p>',
    '<p>Your Health Visiting team creates the GM Early Years App account for the <strong>child’s mother or primary carer</strong>.</p>'
    '<p class="abc-more">In this guide, we call this person the <strong>account holder</strong>.</p>')
rep('<p>The child’s mother or primary carer signs in with their own NHS login. Not sure who it is for? Ask the team.</p>',
    '<p>The <strong>account holder</strong> signs in with their own NHS login. Not sure? Ask the team.</p>')
m = re.search(r'<section class="screen" id="s4-who".*?</section>', s, re.S); blk = m.group(0)
assert blk.count('<div class="stuck">') == 1
s = s[:m.start()] + blk.replace('<div class="stuck">', '<div class="stuck fit-opt2">') + s[m.end():]
CSS = "/* 3.39 a second line in an a-b-c row */\n#app .abc .abc-more{margin-top:4px}\n"
anchor = '/* 2.88 Step 1:'; assert s.count(anchor) == 1; s = s.replace(anchor, CSS + anchor)
rep('Carer role v3.38', 'Carer role v3.39'); rep('Version 3.38 iPhone', 'Version 3.39 iPhone')
rep('>3.38 – REVIEW DRAFT', '>3.39 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.38</span>', '<span class="cv-ver">Version 3.39</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.34</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.38</span>', '<div class="rr"><span class="rv">3.39</span><span class="rd">22 Nov 2026</span><p>Who the account is for: account holder line</p></div>\n<div class="rr"><span class="rv">3.38</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
