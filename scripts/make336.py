"""Guide 3.36 (from trial 3.35) – TRIAL. David, 22 Nov: question 7's subheading is "Your Activation Link", so it
no longer repeats the question ("Have you received your Activation Link?").
usage: python3 make336.py v3.35.html v3.36.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('<span class="vh">GM Early Years App: </span>Have you received your Activation Link?</h3>', '<span class="vh">GM Early Years App: </span>Your Activation Link</h3>')
rep('Carer role v3.35', 'Carer role v3.36'); rep('Version 3.35 iPhone', 'Version 3.36 iPhone')
rep('>3.35 – REVIEW DRAFT', '>3.36 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.35</span>', '<span class="cv-ver">Version 3.36</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.31</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.35</span>', '<div class="rr"><span class="rv">3.36</span><span class="rd">22 Nov 2026</span><p>Question 7 subheading: Your Activation Link</p></div>\n<div class="rr"><span class="rv">3.35</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
