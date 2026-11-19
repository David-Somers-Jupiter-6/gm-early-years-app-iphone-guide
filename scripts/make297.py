"""Guide 2.97 (from 2.96): new Home Screen icon (ABC blocks with the yellow GUIDE label; icons made by make_icons.py).
The guide page itself only changes its version and revision history.
usage: python3 make297.py v2.96.html v2.97.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('Carer role v2.96', 'Carer role v2.97'); rep('Version 2.96 iPhone', 'Version 2.97 iPhone')
rep('<div>Version 2.96</div>', '<div>Version 2.97</div>'); rep('>2.96 – REVIEW DRAFT', '>2.97 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.94</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.96</span>', '<div class="rr"><span class="rv">2.97</span><span class="rd">19 Nov 2026</span><p>New Home Screen icon: ABC blocks with a GUIDE label</p></div>\n<div class="rr"><span class="rv">2.96</span>')
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
