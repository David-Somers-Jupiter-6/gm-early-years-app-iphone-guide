"""Guide 3.89 (from 3.88) – the "i" beside "Please tap an answer, then tap Next." is centred in its circle.
usage: python3 make389.py v3.88.html v3.89.html"""
import re, sys, os, subprocess, tempfile
src, dst = sys.argv[1], sys.argv[2]
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review389')
t = tempfile.mkdtemp(); a = os.path.join(t, 'a.html')
subprocess.run([sys.executable, '-I', os.path.join(here, 'fixes.py'), src, a], check=True)
s = open(a, encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)
rep('Carer role v3.88', 'Carer role v3.89'); rep('Version 3.88 iPhone', 'Version 3.89 iPhone')
rep('>3.88 – REVIEW DRAFT', '>3.89 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.88</span>', '<span class="cv-ver">Version 3.89</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.84</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.88</span>', '<div class="rr"><span class="rv">3.89</span><span class="rd">25 Nov 2026</span><p>Sign-in check: help button on each question, no white cards; hint icon centred</p></div>\n<div class="rr"><span class="rv">3.88</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
