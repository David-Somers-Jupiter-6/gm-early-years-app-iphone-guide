"""Guide 3.19 (from 3.18) – TRIAL (/preview/ only). David, 21 Nov: on the cover, Search has a second line
("Type or say what you need") but Start the guide did not, so the two rows did not match.
 - Start the guide gets a second line: "Step-by-step help to sign in" (same style as the Search line).
usage: python3 make319.py v3.18.html v3.19.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

rep('<span class="cv-t">Start the guide</span>', '<span class="cv-t">Start the guide<span class="cv-st">Step-by-step help to sign in</span></span>')
rep('Carer role v3.18', 'Carer role v3.19'); rep('Version 3.18 iPhone', 'Version 3.19 iPhone')
rep('>3.18 – REVIEW DRAFT', '>3.19 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.18</span>', '<span class="cv-ver">Version 3.19</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.16</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.18</span>', '<div class="rr"><span class="rv">3.19</span><span class="rd">21 Nov 2026</span><p>Cover: Start the guide gets a second line to match Search</p></div>\n<div class="rr"><span class="rv">3.18</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
