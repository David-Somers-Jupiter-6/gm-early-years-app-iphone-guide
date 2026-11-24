"""Guide 3.83 (from 3.82) – light and dark legibility, Apple text sizes in menus (24 Nov 2026).
Dark Mode: the Troubleshooter information box was light with light text (unreadable); reply links now light blue.
Both modes: small labels on the coloured title boxes in white; a Next that waits for an answer is readable.
Menus: every text size is one of Apple's (cover, Contents, Signing in overview, Support menus, stage labels, badges).
Short screens: GM Early Years App help and Your results keep every row on screen.
Wording: section numbers removed from three links/notes (one pointed to the old Section 5); Contacts' team finder says Area.
usage: python3 make383.py v3.82.html v3.83.html"""
import re, sys, os, subprocess, tempfile
src, dst = sys.argv[1], sys.argv[2]
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review383')
tmp = os.path.join(tempfile.mkdtemp(), 'a.html')
subprocess.run([sys.executable, '-I', os.path.join(here, 'polish.py'), src, tmp], check=True)
s = open(tmp, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('Carer role v3.82', 'Carer role v3.83'); rep('Version 3.82 iPhone', 'Version 3.83 iPhone')
rep('>3.82 – REVIEW DRAFT', '>3.83 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.82</span>', '<span class="cv-ver">Version 3.83</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.78</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.82</span>', '<div class="rr"><span class="rv">3.83</span><span class="rd">24 Nov 2026</span><p>Dark Mode and text-size polish</p></div>\n<div class="rr"><span class="rv">3.82</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
