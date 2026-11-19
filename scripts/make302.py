"""Guide 3.02 (from 3.01). David, 19 Nov: How this guide works – "This guide is designed to help." on its own line.
Short screens (<=600 px tall): paragraph gaps 14->8, card gaps 10->6, card padding 10->7.
usage: python3 make302.py v3.01.html v3.02.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('that can be frustrating. <strong>This guide is designed to help.</strong></p>',
    'that can be frustrating.</p>\n<p class="hw-p hw-help"><strong>This guide is designed to help.</strong></p>')
CSS = '''/* 3.02 How this guide works: "This guide is designed to help." on its own line; tighter spacing on short screens so it still fits */
@media screen and (max-height:600px){#app #how .hw-p{margin-bottom:8px!important}#app #how .hw-list{gap:6px!important}#app #how .hw-list li{padding-top:7px!important;padding-bottom:7px!important}}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'
rep('Carer role v3.01', 'Carer role v3.02'); rep('Version 3.01 iPhone', 'Version 3.02 iPhone')
rep('<div>Version 3.01</div>', '<div>Version 3.02</div>'); rep('>3.01 – REVIEW DRAFT', '>3.02 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.99</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.01</span>', '<div class="rr"><span class="rv">3.02</span><span class="rd">19 Nov 2026</span><p>How this guide works: “This guide is designed to help.” on its own line</p></div>\n<div class="rr"><span class="rv">3.01</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
