"""Guide 2.74 (from 2.73). Same look, much smaller file: the ABC app icon in the title box bands was
stored 45 times (2.73 grew from 1.9 MB to 3.6 MB). It is now stored once, at 64 px (scripts/abc_round_64.png),
as a CSS background.
usage: python3 make274.py v2.73.html v2.74.html
"""
import re, sys, base64, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
ICON = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'abc_round_64.png'), 'rb').read()).decode()
s, n = re.subn(r'<img class="eyl" alt="" src="data:image/png;base64,[^"]+">', '<i class="eyl"></i>', s)
assert n == 45, n  # 45 app bands (the 18 NHS login bands use the NHS mark)
rep('.eyx>.eyb .eyl{flex:0 0 18px;height:18px;width:18px;border-radius:4px;',
    '.eyx>.eyb .eyl{display:block;background:url(%s) center/cover no-repeat;flex:0 0 18px;height:18px;width:18px;border-radius:4px;' % ICON)
rep('Carer role v2.73', 'Carer role v2.74'); rep('Version 2.73 iPhone', 'Version 2.74 iPhone')
rep('<div>Version 2.73</div>', '<div>Version 2.74</div>'); rep('>2.73 – REVIEW DRAFT', '>2.74 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.69</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.73</span>', '<div class="rr"><span class="rv">2.74</span><span class="rd">17 Nov 2026</span><p>Smaller file: the app icon in the title boxes is stored once</p></div>\n<div class="rr"><span class="rv">2.73</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
