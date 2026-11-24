"""Guide 3.85 (from 3.84) – Design review, points 1-4 plus How numbers (24 Nov 2026).
- Title box: calmer (no underline, fainter ABC blocks); a location label in the box
  ("Section N", "Your App account · Question 1 of 6", "Installing the App · Step N of 7"); thin top strip on the cover only.
- One list style for Contents, Sign-in check start page, Contacts, Support and results: white grouped panel,
  44-52 px rows, 30 px icon tiles, grey chevrons.
- List icons as soft tints (pale pink + deep magenta; pale blue + NHS blue; grey for Accessibility).
- Blue buttons: Begin, Yes and "Stuck?" all in one calm blue, no pulse or glow (cover unchanged).
- Fewer capitals and less bold: in-page labels in sentence case at 15 px semibold; 36 bold words made regular
  (kept bold: "child's mother or primary carer").
- How this guide works: step numbers as tinted squares (pale pink, deep magenta).
- Help icons (Who is it for, The issue, Who can help, What to do) stay solid.
usage: python3 make385.py v3.84.html v3.85.html"""
import re, sys, os, subprocess, tempfile
src, dst = sys.argv[1], sys.argv[2]
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review385')
t = tempfile.mkdtemp(); cur = src
for i, step in enumerate(['title_box.py', 'list_style.py', 'tinted_icons.py', 'colours.py', 'capitals_bold.py', 'how_numbers.py']):
    out = os.path.join(t, '%d.html' % i)
    extra = [os.path.join(here, 'unbold.json')] if step == 'capitals_bold.py' else []
    subprocess.run([sys.executable, '-I', os.path.join(here, step), cur, out] + extra, check=True)
    cur = out
s = open(cur, encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)
rep('Carer role v3.84', 'Carer role v3.85'); rep('Version 3.84 iPhone', 'Version 3.85 iPhone')
rep('>3.84 – REVIEW DRAFT', '>3.85 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.84</span>', '<span class="cv-ver">Version 3.85</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.80</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.84</span>', '<div class="rr"><span class="rv">3.85</span><span class="rd">24 Nov 2026</span><p>Design polish: plain page titles, one list style, soft tinted icons, calmer buttons and labels</p></div>\n<div class="rr"><span class="rv">3.84</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
