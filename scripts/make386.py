"""Guide 3.86 (from 3.85) – works on every iPhone size (24 Nov 2026).
- Sign-in check questions: on shorter screens (Safari, 760 px high and under) the "?" icon sits on the question's line
  and "Tap an answer, then tap Next." gives way; on 650 px and under the answer boxes are 44 px. The reply after
  Yes or No now shows above the bottom bar on every iPhone (it was partly or fully hidden in Safari since 3.78 or earlier).
- Safety net: if a reply still opens below the bottom bar (iPhone SE in Safari), the page scrolls just enough to show it.
- Sign-in check start page: compact list also at 701-730 px high (iPhone 11/XR in Safari; question 6 was hidden).
- iPhone SE in Safari (600 px high and under): location label above the title (3.85 drew it over the title); Contents
  without the Cover/Introduction/Contents tiles and row subtitles; cover photo a little shorter; NHS login account help,
  Sign-in check start page and Document control slightly tighter, so every page fits.
- Revision history: 3.85 line corrected ("calmer title boxes", not "plain page titles").
Checked with scripts/check_iphone_sizes.py at 16 sizes (iPhone SE to 16 Pro Max, Safari and Home Screen).
usage: python3 make386.py v3.85.html v3.86.html"""
import re, sys, os, subprocess, tempfile
src, dst = sys.argv[1], sys.argv[2]
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review386')
t = tempfile.mkdtemp(); a = os.path.join(t, 'a.html')
subprocess.run([sys.executable, '-I', os.path.join(here, 'fit_all_iphones.py'), src, a], check=True)
s = open(a, encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)
rep('Carer role v3.85', 'Carer role v3.86'); rep('Version 3.85 iPhone', 'Version 3.86 iPhone')
rep('>3.85 – REVIEW DRAFT', '>3.86 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.85</span>', '<span class="cv-ver">Version 3.86</span>')
rep('<p>Design polish: plain page titles, one list style, soft tinted icons, calmer buttons and labels</p>',
    '<p>Design polish: calmer title boxes, one list style, soft tinted icons, calmer buttons and labels</p>')
old = re.search(r'<div class="rr"><span class="rv">3\.81</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.85</span>', '<div class="rr"><span class="rv">3.86</span><span class="rd">24 Nov 2026</span><p>Every page fits on every iPhone size; Sign-in check replies always show</p></div>\n<div class="rr"><span class="rv">3.85</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
