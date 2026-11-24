"""Guide 3.84 (from 3.83) – Sign-in check (24 Nov 2026), published live.
- "Troubleshooter" renamed "Sign-in check" in all visible text.
- Sign-in check start page, option B: "Who should answer" box; one-line questions grouped under Your App account,
  Your NHS login and Both accounts; "Answer Yes or No. It takes about 2 minutes." (gives way on short screens).
- Questions 1-2 "Who can help · contact" reply on two lines; Your results rows on at most two lines (short titles);
  short-screen results rows tighter so six answered rows fit.
- Next: a second tap within 450 ms is ignored (a quick double tap turned two pages); Home Screen on iPhones with a
  home indicator: bottom bar raised above the swipe-up area.
usage: python3 make384.py v3.83.html v3.84.html"""
import re, sys, os, subprocess, tempfile
src, dst = sys.argv[1], sys.argv[2]
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review384')
t = tempfile.mkdtemp(); a = os.path.join(t, 'a.html'); b = os.path.join(t, 'b.html')
subprocess.run([sys.executable, '-I', os.path.join(here, 'changes.py'), src, a, 'Sign-in check'], check=True)
subprocess.run([sys.executable, '-I', os.path.join(here, 'start_page.py'), a, b, 'B'], check=True)
s = open(b, encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)
rep('Carer role v3.83', 'Carer role v3.84'); rep('Version 3.83 iPhone', 'Version 3.84 iPhone')
rep('>3.83 – REVIEW DRAFT', '>3.84 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.83</span>', '<span class="cv-ver">Version 3.84</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.79</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.83</span>', '<div class="rr"><span class="rv">3.84</span><span class="rd">24 Nov 2026</span><p>Troubleshooter renamed Sign-in check; clearer start and results pages</p></div>\n<div class="rr"><span class="rv">3.83</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
