"""Guide 2.69 (from 2.68). Every page fits on every iPhone, in Safari and as a Home Screen app.
Full sweep (74 pages x 8 iPhone sizes x Safari/Home Screen app) after the 2.68 cover fix found:
- Activation Link not received: 4 px over on a 12/13 mini in Safari -> tighter rows at <=660 px tall.
- iPhone SE in Safari (about 548 px tall): 20 pages over by up to 85 px -> at <=600 px tall, title boxes size
  to their content (min 72 px) instead of the fixed 110 px, tighter spacing, and the Contents "Select Next"
  tip and the How this guide works "Tap a section" line are hidden. Text sizes unchanged.
usage: python3 make269.py v2.68.html v2.69.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
FIX = '/* 2.69 short screens: the Activation Link page fits on a 12/13 mini in Safari, and on an iPhone SE in\n   Safari (about 548 px tall) every page fits: shorter title boxes, tighter spacing, and the two hint\n   lines (Contents "Select Next", How this guide works "Tap a section") hidden. Text sizes are unchanged. */\n@media (max-height:660px){.abc-row{padding:6px 0}.abc-links .abc-btn{padding:7px 0!important}}\n@media (max-height:600px){\n#app .screen .pbox,#app .screen:not(#contents) .tp-card .tp-body{height:auto!important;min-height:72px!important;max-height:none!important;padding-top:8px!important}\n#app .screen .pbox .stepper{margin-bottom:6px!important}\n#app .screen .scroll{padding-top:8px!important;padding-bottom:4px!important}\n.scroll .strip{margin:6px 0 8px}\n.abc-row{padding:4px 0}.abc-links .abc-btn{padding:5px 0!important}\n.abc-ask{margin-top:3px!important;padding:5px 12px!important}.abc-list{gap:1px}\n#contents .nav-tip,#how .lead{display:none}\n#contents .toc-row{min-height:40px!important;padding-top:4px!important;padding-bottom:4px!important}\n#s4-nhs .info-lead{margin-bottom:4px!important;line-height:1.28!important}\n#sum .sum-intro{margin-bottom:4px!important}#sum .sum-msg{margin-top:4px!important}\n.step-body .step-tip{margin-top:6px!important;padding-top:6px!important;padding-bottom:6px!important}\n.abc-row:first-child{padding-top:0}\n#app .screen .q-why{min-height:0!important;margin-bottom:4px!important}#app .screen .q-ask{min-height:0!important}\n.ans-msg{margin-top:6px!important;padding-top:6px!important;padding-bottom:6px!important}.radios .radio{padding-top:6px;padding-bottom:6px}#app .screen .abc-ask p{line-height:1.28!important}\n}\n'
rep('@media print{', FIX + '@media print{')
rep('Carer role v2.68', 'Carer role v2.69'); rep('Version 2.68 iPhone', 'Version 2.69 iPhone')
rep('<div>Version 2.68</div>', '<div>Version 2.69</div>'); rep('>2.68 – REVIEW DRAFT', '>2.69 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.66</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.68</span>', '<div class="rr"><span class="rv">2.69</span><span class="rd">17 Nov 2026</span><p>Every page fits on every iPhone, including iPhone SE in Safari</p></div>\n<div class="rr"><span class="rv">2.68</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
