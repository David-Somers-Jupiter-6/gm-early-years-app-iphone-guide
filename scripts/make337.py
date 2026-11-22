"""Guide 3.37 (from trial 3.36) – TRIAL. David, 22 Nov: on GM Early Years App help, every topic card uses the
GM Early Years App colours (the four Health Visiting team topics were blue).
usage: python3 make337.py v3.36.html v3.37.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
m = re.search(r'<section class="screen" id="s4-gm".*?</section>', s, re.S); blk = m.group(0)
assert blk.count('class="tc tc-hv"') == 4 and blk.count('class="tc tc-app"') == 3
s = s[:m.start()] + blk.replace('class="tc tc-hv"', 'class="tc tc-app"') + s[m.end():]
rep('Carer role v3.36', 'Carer role v3.37'); rep('Version 3.36 iPhone', 'Version 3.37 iPhone')
rep('>3.36 – REVIEW DRAFT', '>3.37 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.36</span>', '<span class="cv-ver">Version 3.37</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.32</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.36</span>', '<div class="rr"><span class="rv">3.37</span><span class="rd">22 Nov 2026</span><p>GM Early Years App help: all topic cards in the App colours</p></div>\n<div class="rr"><span class="rv">3.36</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
