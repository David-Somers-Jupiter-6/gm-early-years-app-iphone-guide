"""Guide 2.68 (from 2.67). Cover fills the screen on every iPhone, in Safari and as a Home Screen app.
Cause: since 2.31 the cover photo was capped at 240 px and nothing else grew, so taller screens showed a
white gap above the navigation bar (up to 264 px on a 16 Pro Max Home Screen app).
Fix: the photo takes the free space first, up to 85% of the screen width; the blue panel takes anything
left, text centred; photo framing moved left so the child's face stays in view.
usage: python3 make268.py v2.67.html v2.68.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
FIX = '''/* 2.68 cover fills the screen on every iPhone (Safari and Home Screen app): the photo takes the free space
   first, up to 85% of the screen width; the blue panel takes anything left, so there is no white gap */
.cover-photo{flex:1000 1 0;max-height:85vw}
.cover-panel{flex:1 0 auto;justify-content:center}
.cover-photo .cover-img{object-position:22% 30%}
'''
rep('@media print{', FIX + '@media print{')
rep('Carer role v2.67', 'Carer role v2.68'); rep('Version 2.67 iPhone', 'Version 2.68 iPhone')
rep('<div>Version 2.67</div>', '<div>Version 2.68</div>'); rep('>2.67 – REVIEW DRAFT', '>2.68 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.65</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.67</span>', '<div class="rr"><span class="rv">2.68</span><span class="rd">17 Nov 2026</span><p>Cover fills the screen on every iPhone, in Safari and as a Home Screen app</p></div>\n<div class="rr"><span class="rv">2.67</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
