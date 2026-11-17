"""Guide 2.71 (from 2.70) - TRIAL for David to review: title boxes in section colours with faded ABC blocks
(mockup options 4 + 5, 17 Nov). The GM Early Years App ABC blocks (white, cut from the app logo already in
the guide: scripts/abc_blocks_white.png) sit faintly behind the right of every title box, in place of the
large faded page number. Each section has its own colour:
  Welcome and Search: blue (unchanged)        Section 1 Your Health Visiting team: indigo
  Section 2 Checklist: teal                    Section 3 Signing in: NHS blue
  Section 4 Troubleshooting: plum              Section 5 Contact & support: green
  Section 6 About this guide: slate
NHS login account issues pages keep their NHS login band (2.70). Contents keeps its own title box.
Also fixes the NHS logo overlapping the Section 1 title (open issue 3).
usage: python3 make271.py v2.70.html v2.71.html
"""
import re, sys, base64, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
BLK = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'abc_blocks_white.png'), 'rb').read()).decode()
SEC = {  # data-sec prefix: gradient
 'Section 1': '#2b2876 0%,#4643a8 100%',
 'Section 2': '#00574f 0%,#00897b 100%',
 'Section 3': '#003087 0%,#005eb8 100%',
 'Section 4': '#5b1a5e 0%,#a3165a 100%',
 'Section 5': '#14532d 0%,#1f7a4d 100%',
 'Section 6': '#2c3a4f 0%,#4b5d75 100%',
}
BOX = '#app .screen%s .pbox:not(.nhs-band),#app .screen%s:not(#contents) .tp-card .tp-body'
css = ['/* 2.71 TRIAL: section colours and faded ABC blocks in every title box (not Contents or NHS login pages) */']
for k, g in SEC.items():
    sel = '[data-sec^="%s"]' % k
    css.append((BOX % (sel, sel)) + '{background:linear-gradient(135deg,%s)!important}' % g)
css.append('#app .screen .pbox:not(.nhs-band),#app .screen:not(#contents) .tp-card .tp-body{position:relative;overflow:hidden}')
css.append('#app .screen .pbox:not(.nhs-band)::before,#app .screen:not(#contents) .tp-card .tp-body::before{content:"";position:absolute;right:-8px;bottom:-16px;width:118px;height:118px;background:url(@@BLK@@) center/contain no-repeat;opacity:.16;transform:rotate(-8deg);pointer-events:none;z-index:0}')
css.append('#app .screen .pbox.has-badge::before,#app .screen .tp-card.has-badge .tp-body::before{bottom:auto;top:-18px;right:-4px;width:104px;height:104px}')
css.append('#app .screen .pbox:not(.nhs-band)>*:not(.tp-n):not(.nhsbadge),#app .screen:not(#contents) .tp-card .tp-body>*:not(.tp-n){position:relative;z-index:1}')
css.append('#app .screen .pbox .tp-n,#app .screen .tp-card .tp-n{display:none!important}')
css.append('#app .screen .pbox.has-badge .nhsbadge{position:absolute!important}')
css.append('#app #hv .tp-body .tp-h{max-width:calc(100% - 66px)!important;white-space:normal!important}  /* NHS logo no longer overlaps the Section 1 title */')
CSS = '\n'.join(c for c in css if c).replace('@@BLK@@', BLK) + '\n'
rep('@media print{', CSS + '@media print{')
rep('Carer role v2.70', 'Carer role v2.71'); rep('Version 2.70 iPhone', 'Version 2.71 iPhone')
rep('<div>Version 2.70</div>', '<div>Version 2.71</div>'); rep('>2.70 – REVIEW DRAFT', '>2.71 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.68</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.70</span>', '<div class="rr"><span class="rv">2.71</span><span class="rd">17 Nov 2026</span><p>Trial: title boxes in section colours with faded ABC blocks</p></div>\n<div class="rr"><span class="rv">2.70</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
