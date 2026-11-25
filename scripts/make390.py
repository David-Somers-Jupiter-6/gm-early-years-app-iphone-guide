"""Guide 3.90 (from 3.89) – points 3, 9, 11, 13, 14, 15, 16, 17 and 19 of the problems-and-solutions doc.
usage: python3 make390.py v3.89.html v3.90.html"""
import re, sys, os, subprocess, tempfile
src, dst = sys.argv[1], sys.argv[2]
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review390')
t = tempfile.mkdtemp(); a = os.path.join(t, 'a.html')
b = os.path.join(t, 'b.html'); c = os.path.join(t, 'c.html')
subprocess.run([sys.executable, '-I', os.path.join(here, 'fixes.py'), src, b], check=True)
subprocess.run([sys.executable, '-I', os.path.join(here, 'fixes2.py'), b, c], check=True)
subprocess.run([sys.executable, '-I', os.path.join(here, 'example_details_images.py'), c, a], check=True)
s = open(a, encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)
# point 19: names carers see outside the guide; REVIEW DRAFT removed
rep('<title>GM Early Years App – How to sign in (iOS) – Carer role v3.89 iPhone edition review draft</title>', '<title>GM Early Years App – help signing in</title>')
rep('content="Version 3.89 iPhone edition review draft. A screen-by-screen', 'content="Version 3.90. A screen-by-screen')
rep('<meta name="apple-mobile-web-app-title" content="EY App Guide"/>', '<meta name="apple-mobile-web-app-title" content="EY App help"/>')
rep('>3.89 – REVIEW DRAFT (iPhone edition)<', '>3.90 (iPhone edition)<')
rep('<span class="cv-ver">Version 3.89</span>', '<span class="cv-ver">Version 3.90</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.85</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.89</span>', '<div class="rr"><span class="rv">3.90</span><span class="rd">25 Nov 2026</span><p>Clearer questions 1 and 2; Find your Health Visiting team; NHS login tips on their step pages; one set of example details; tidier help buttons and wording</p></div>\n<div class="rr"><span class="rv">3.89</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
