"""Guide 3.88 (from 3.87) – fixes 4, 5, 6, 7, 9, 10 and 11 from the problems-and-fixes doc (25 Nov 2026).
See scripts/review388/fixes.py for the list.
usage: python3 make388.py v3.87.html v3.88.html"""
import re, sys, os, subprocess, tempfile
src, dst = sys.argv[1], sys.argv[2]
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review388')
t = tempfile.mkdtemp(); a = os.path.join(t, 'a.html')
subprocess.run([sys.executable, '-I', os.path.join(here, 'fixes.py'), src, a], check=True)
s = open(a, encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)
rep('Carer role v3.87', 'Carer role v3.88'); rep('Version 3.87 iPhone', 'Version 3.88 iPhone')
rep('>3.87 – REVIEW DRAFT', '>3.88 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.87</span>', '<span class="cv-ver">Version 3.88</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.83</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.87</span>', '<div class="rr"><span class="rv">3.88</span><span class="rd">25 Nov 2026</span><p>Finish button at the end; Stage, Step and Question labels; calmer replies and help buttons</p></div>\n<div class="rr"><span class="rv">3.87</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
