"""Guide 2.75 (from 2.74). Back to clear title boxes with the ABC blocks faintly behind (David, 17 Nov:
"light rather than busy"). The 2.73-2.74 design is called "the banded version".
- Every title box: GM Early Years App colours (#6c155c -> #d01545) with the white ABC blocks from the app logo
  faintly behind the right-hand side (scripts/abc_blocks_white.png, one CSS background). No band, no page icon;
  the small label above the title ("Question 1 of 4", "Part 2 of 3 ...") is back.
- Your Health Visiting team pages (hv, s5-hv): NHS blue (#003087 -> #005eb8), ABC blocks and NHS logo.
- NHS login pages keep the banded look (NHS blue, "NHS login | ..." band, NHS mark, page icon):
  the NHS login account issues pages (2.70) and s4-cannot-4, s4-signin, Steps A-H and tips, s5-2 (2.73).
- Large faded page numbers stay hidden. The Section 1 title no longer runs under the NHS logo.
usage: python3 make275.py v2.74.html v2.75.html
"""
import re, sys, base64, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
BLK = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(here, 'abc_blocks_white.png'), 'rb').read()).decode()
# 1. remove the app band and page icon from every non-NHS box
n = 0
def strip(m):
    global n
    n += 1
    cls = m.group(1).replace(' eyx', '')
    return '<div class="%s">' % cls
s = re.sub(r'<div class="((?:pbox[^"]*|tp-body) eyx)"><div class="eyb" aria-hidden="true">.*?</div>(?:<span class="eyi" aria-hidden="true"><svg.*?</svg></span>)?', strip, s)
assert n == 45, n
assert s.count('class="eyb eyb-nhs"') == 18
APP = 'linear-gradient(135deg,#6c155c 0%,#d01545 100%)'
NHS = 'linear-gradient(135deg,#003087 0%,#005eb8 100%)'
BOX = '#app .screen:not(#contents) .pbox:not(.eyx):not(.nhs-band),#app .screen:not(#contents) .tp-card .tp-body:not(.eyx)'
CSS = '''/* 2.75 clear title boxes: GM Early Years App colours with the ABC blocks faintly behind; Health Visiting team in NHS blue;
   NHS login pages keep their band (.eyx-nhs, .nhs-band) */
@@BOX@@,#app #contents .tp-card .tp-body{background:@@APP@@!important}
#app .screen#hv:not(#contents) .tp-card .tp-body:not(.eyx),#app .screen#s5-hv:not(#contents) .pbox:not(.eyx){background:@@NHS@@!important}
@@BOX@@{position:relative;overflow:hidden}
#app .screen:not(#contents) .pbox:not(.eyx):not(.nhs-band)::before,#app .screen:not(#contents) .tp-card .tp-body:not(.eyx)::before{content:"";position:absolute;right:-8px;bottom:-16px;width:118px;height:118px;background:url(@@BLK@@) center/contain no-repeat;opacity:.14;transform:rotate(-8deg);pointer-events:none;z-index:0}
#app .screen .pbox.has-badge:not(.eyx)::before,#app .screen .tp-card.has-badge .tp-body:not(.eyx)::before{bottom:auto;top:-18px;right:-4px;width:104px;height:104px}
#app .screen:not(#contents) .pbox:not(.eyx):not(.nhs-band)>*:not(.tp-n):not(.nhsbadge),#app .screen:not(#contents) .tp-card .tp-body:not(.eyx)>*:not(.tp-n){position:relative;z-index:1}
#app .screen .pbox .tp-n,#app .screen .tp-card .tp-n{display:none!important}
#app #hv .tp-body .tp-h{max-width:calc(100% - 66px)!important;white-space:normal!important}
#app .screen .tp-card:has(.tp-body:not(.eyx))>.nhsbadge{display:block!important}
'''.replace('@@BOX@@', BOX).replace('@@APP@@', APP).replace('@@NHS@@', NHS).replace('@@BLK@@', BLK)
rep('@media print{', CSS + '@media print{')
rep('Carer role v2.74', 'Carer role v2.75'); rep('Version 2.74 iPhone', 'Version 2.75 iPhone')
rep('<div>Version 2.74</div>', '<div>Version 2.75</div>'); rep('>2.74 – REVIEW DRAFT', '>2.75 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.70</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.74</span>', '<div class="rr"><span class="rv">2.75</span><span class="rd">17 Nov 2026</span><p>Clear title boxes in the app colours with the ABC blocks faintly behind; NHS login pages keep their band</p></div>\n<div class="rr"><span class="rv">2.74</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, n, 'bands removed')
