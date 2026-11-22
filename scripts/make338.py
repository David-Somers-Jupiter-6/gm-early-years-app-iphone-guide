"""Guide 3.38 (from trial 3.37) – TRIAL. David, 22 Nov: on "Who the account is for", the first row says
"the GM Early Years App account" (was "the App account").
usage: python3 make338.py v3.37.html v3.38.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('<p>Your Health Visiting team creates the App account for the <strong>child’s mother or primary carer</strong>.</p>',
    '<p>Your Health Visiting team creates the GM Early Years App account for the <strong>child’s mother or primary carer</strong>.</p>')
rep('Carer role v3.37', 'Carer role v3.38'); rep('Version 3.37 iPhone', 'Version 3.38 iPhone')
rep('>3.37 – REVIEW DRAFT', '>3.38 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.37</span>', '<span class="cv-ver">Version 3.38</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.33</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.37</span>', '<div class="rr"><span class="rv">3.38</span><span class="rd">22 Nov 2026</span><p>Who the account is for: says GM Early Years App account</p></div>\n<div class="rr"><span class="rv">3.37</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
