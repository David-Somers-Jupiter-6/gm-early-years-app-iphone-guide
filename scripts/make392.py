"""Guide 3.92 (from 3.91) – Sign-in check: question box stays put from question 4 to 5.
usage: python3 make392.py v3.91.html v3.92.html"""
import re, sys, os, subprocess, tempfile
src, dst = sys.argv[1], sys.argv[2]
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review392')
t = tempfile.mkdtemp(); a = os.path.join(t, 'a.html')
subprocess.run([sys.executable, '-I', os.path.join(here, 'fixes.py'), src, a], check=True)
s = open(a, encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)
rep('content="Version 3.91. A screen-by-screen', 'content="Version 3.92. A screen-by-screen')
rep('>3.91 (iPhone edition)<', '>3.92 (iPhone edition)<')
rep('<span class="cv-ver">Version 3.91</span>', '<span class="cv-ver">Version 3.92</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.87</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.91</span>', '<div class="rr"><span class="rv">3.92</span><span class="rd">26 Nov 2026</span><p>Sign-in check: the question stays in the same place on question 5</p></div>\n<div class="rr"><span class="rv">3.91</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
