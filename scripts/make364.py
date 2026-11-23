"""Guide 3.64 (from trial 3.63) – TRIAL. David, 23 Nov:
 - Troubleshooter questions: "Here is how it works." removed (it was on questions 1-4).
usage: python3 make364.py v3.63.html v3.64.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
s, n = re.subn(r'(<div class="ts-info">)<p class="calm">.*?</p>', r'\1', s, flags=re.S); assert n == 4, n
rep('#app :is(#ts1,#ts1b,#ts2,#ts3) .ts-info .calm{margin:0 0 8px!important}\n', '')
rep('Carer role v3.63', 'Carer role v3.64'); rep('Version 3.63 iPhone', 'Version 3.64 iPhone')
rep('>3.63 – REVIEW DRAFT', '>3.64 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.63</span>', '<span class="cv-ver">Version 3.64</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.59</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.63</span>', '<div class="rr"><span class="rv">3.64</span><span class="rd">23 Nov 2026</span><p>Troubleshooter questions: Here is how it works removed</p></div>\n<div class="rr"><span class="rv">3.63</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
