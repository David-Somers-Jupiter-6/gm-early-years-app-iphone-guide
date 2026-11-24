"""Guide 3.82 (from 3.81) – Search page and Contents review (24 Nov 2026), published live.
Search: results cannot be dragged sideways (list was 8px wider than its box); swiping does not leave Search; App icon
in the title box; cleaner result snippets; "Contact your Health Visiting team" topic; greyed-out Next hidden.
Contents: cover-style search button (magnifier, Search, microphone); option B: Cover page / Introduction / Contents
as tiles and the sections grouped under the 3 stages; fix for 3.81 cutting off the bottom of Contents at 375x635.
usage: python3 make382.py v3.81.html v3.82.html"""
import re, sys, os, subprocess, tempfile
src, dst = sys.argv[1], sys.argv[2]
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review382')
tmp = os.path.join(tempfile.mkdtemp(), 'a.html')
subprocess.run([sys.executable, '-I', os.path.join(here, 'search_contents.py'), src, tmp, 'B'], check=True)
s = open(tmp, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('Carer role v3.81', 'Carer role v3.82'); rep('Version 3.81 iPhone', 'Version 3.82 iPhone')
rep('>3.81 – REVIEW DRAFT', '>3.82 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.81</span>', '<span class="cv-ver">Version 3.82</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.77</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.81</span>', '<div class="rr"><span class="rv">3.82</span><span class="rd">24 Nov 2026</span><p>Search fixes; Contents grouped by stage</p></div>\n<div class="rr"><span class="rv">3.81</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
