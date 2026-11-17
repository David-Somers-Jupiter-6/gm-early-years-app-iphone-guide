"""Guide 2.76 (from 2.75). Every title box lines up exactly (David, 17 Nov: nothing should move between pages).
The section start pages (Introduction, Your Health Visiting team, Checklist, Signing in, Troubleshooting,
Contact & support, About this guide) use a different kind of title box from the other pages, and it had
slightly different settings: title 18 px from the left (others 16), 16 px from the bottom (others 18), tighter
line spacing (1.15, others 1.2), underline 18 px from the left and 11 px from the bottom (others 16 and 9).
They now use the same settings as every other page. The Contact & support "Your Health Visiting team" page also
had its title 16 px higher, to leave room for the NHS logo underneath; the logo now sits bottom right beside the
title, as on the Section 1 team page.
usage: python3 make276.py v2.75.html v2.76.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
CSS = '''/* 2.76 every title box lines up: section start pages use the same title and underline position as all other pages */
#app .screen:not(#contents) .tp-card .tp-body{padding-left:16px!important;padding-right:16px!important;padding-bottom:18px!important}
#app .screen .tp-card .tp-body .tp-h{line-height:1.2!important}
#app .screen:not(#contents) .tp-card .tp-body::after{left:16px!important;bottom:9px!important}
#app #s5-hv .pbox.has-badge{padding-bottom:18px!important}
#app #s5-hv .pbox h2{max-width:calc(100% - 66px)!important}
'''
rep('@media print{', CSS + '@media print{')
rep('Carer role v2.75', 'Carer role v2.76'); rep('Version 2.75 iPhone', 'Version 2.76 iPhone')
rep('<div>Version 2.75</div>', '<div>Version 2.76</div>'); rep('>2.75 – REVIEW DRAFT', '>2.76 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.73</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.75</span>', '<div class="rr"><span class="rv">2.76</span><span class="rd">17 Nov 2026</span><p>Titles and underlines sit in exactly the same place in every title box</p></div>\n<div class="rr"><span class="rv">2.75</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
