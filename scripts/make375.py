"""Guide 3.75 (from trial 3.74) – TRIAL. Fix for iPhones that show the guide 375 points wide
(e.g. iPhone 11 with Display Zoom, iPhone 12/13 mini) where question 1's Yes reply was cut off:
 - question 5: "Did you give your Health Visiting team these same details?" (2 lines; was 3 at 375 wide,
   which made every question reserve 3 lines);
 - question 2 Yes reply: "Only the account holder can access the account." (2 lines; was 3 at 375 wide,
   which made every reply box 3 lines tall).
usage: python3 make375.py v3.74.html v3.75.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('<p class="q-ask" id="ask-ts4">Did you give your Health Visiting team the same details you use for NHS login?</p>',
    '<p class="q-ask" id="ask-ts4">Did you give your Health Visiting team these same details?</p>')
rep('<p class="ok-more">Only the account holder can access the GM Early Years App account.</p>',
    '<p class="ok-more">Only the account holder can access the account.</p>')
rep('Carer role v3.74', 'Carer role v3.75'); rep('Version 3.74 iPhone', 'Version 3.75 iPhone')
rep('>3.74 – REVIEW DRAFT', '>3.75 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.74</span>', '<span class="cv-ver">Version 3.75</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.70</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.74</span>', '<div class="rr"><span class="rv">3.75</span><span class="rd">23 Nov 2026</span><p>Troubleshooter: shorter question 5 and question 2 reply so pages fit 375-wide iPhones</p></div>\n<div class="rr"><span class="rv">3.74</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
