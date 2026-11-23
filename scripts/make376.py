"""Guide 3.76 (from trial 3.75) – TRIAL. David, 23 Nov, Troubleshooter results page:
 - each row shows only the question title (no second line such as "Read who can access the account" or
   "You need an NHS login account"), so every row is at most three lines; the icon and the button
   (Get help / Read more / Answer) still show the result.
usage: python3 make376.py v3.75.html v3.76.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
CSS = '''/* 3.76 Troubleshooter results: question title only in each row */
#app #tsum .sum-list .st .sum-t p.sum-s{display:none!important}
'''
rep('/* 2.95 A. Troubleshooting help pages as three blocks */', CSS + '/* 2.95 A. Troubleshooting help pages as three blocks */')
rep('Carer role v3.75', 'Carer role v3.76'); rep('Version 3.75 iPhone', 'Version 3.76 iPhone')
rep('>3.75 – REVIEW DRAFT', '>3.76 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.75</span>', '<span class="cv-ver">Version 3.76</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.71</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.75</span>', '<div class="rr"><span class="rv">3.76</span><span class="rd">23 Nov 2026</span><p>Troubleshooter results: question title only in each row</p></div>\n<div class="rr"><span class="rv">3.75</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
