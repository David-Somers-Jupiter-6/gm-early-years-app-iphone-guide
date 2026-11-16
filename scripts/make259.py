"""Guide 2.59 (from 2.58).
- Contact & support > Your Health Visiting team (s5-hv): removed the two lines under the card,
  "To view on a map, tap the address." / "To call, tap the contact number." (David), so every
  card fits a 375 x 637 screen with the Option B title box (Stockport "Cheadle Hulme and
  Bramhall" card was 9 px over). Section 1's team page (hv) keeps them.
usage: python3 make259.py v2.58.html v2.59.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def edit(pid, a, b, n=1):
    global s
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

TIPS = '<div class="hv-tips"><p>To view on a map, tap the address.</p><p>To call, tap the contact number.</p></div>'
assert s.count(TIPS) == 2
edit('s5-hv', TIPS + '\n', '')
edit('hv', TIPS, TIPS)   # section 1 keeps them

rep('Carer role v2.58', 'Carer role v2.59'); rep('Version 2.58 iPhone', 'Version 2.59 iPhone')
rep('<div>Version 2.58</div>', '<div>Version 2.59</div>'); rep('>2.58 – REVIEW DRAFT', '>2.59 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.56</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.58</span>', '<div class="rr"><span class="rv">2.59</span><span class="rd">16 Nov 2026</span><p>Contact &amp; support team page: map and call hints removed so every card fits</p></div>\n<div class="rr"><span class="rv">2.58</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
