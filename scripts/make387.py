"""Guide 3.87 (from 3.86) – Sign-in check results navigation (24 Nov 2026).
- Results page: the bottom button is always Next and always goes to Section 4 Signing in, whatever the answers.
  (3.86 and earlier: with anything red it said Done and went to Support, and Back from there went to "You are signed in".)
- Get help / Answer / Read more on the results page: Next (or Done) keeps bringing you back to the results; Back too.
- Side trips: a Health Visiting team or Contacts page opened from a link on a Sign-in check, Signing in or Support page
  has a Done button back to where you were (as the GMDP help page already had). Reached from Contents, Search or in page
  order, those pages work as before.
usage: python3 make387.py v3.86.html v3.87.html"""
import re, sys, os, subprocess, tempfile
src, dst = sys.argv[1], sys.argv[2]
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review387')
t = tempfile.mkdtemp(); a = os.path.join(t, 'a.html')
subprocess.run([sys.executable, '-I', os.path.join(here, 'nav_fix.py'), src, a], check=True)
s = open(a, encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)
rep('Carer role v3.86', 'Carer role v3.87'); rep('Version 3.86 iPhone', 'Version 3.87 iPhone')
rep('>3.86 – REVIEW DRAFT', '>3.87 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.86</span>', '<span class="cv-ver">Version 3.87</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.82</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.86</span>', '<div class="rr"><span class="rv">3.87</span><span class="rd">24 Nov 2026</span><p>Sign-in check results: Next always goes on to Signing in; help pages bring you back</p></div>\n<div class="rr"><span class="rv">3.86</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
