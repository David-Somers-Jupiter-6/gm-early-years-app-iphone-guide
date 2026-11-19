"""Guide 2.96 (from 2.95). David, 19 Nov:
 1. GMDP Support Team page: a round white headset icon in the title box, like the NHS login Support team page
    (in the app colour).
 2. Contact & support > Your Health Visiting team: the page no longer moves when a team is chosen - the one-line
    instruction stays (it used to be hidden once a team was chosen, which shifted everything up).
usage: python3 make296.py v2.95.html v2.96.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>' % re.escape(pid), s, re.S); assert m, pid; return m
def edit(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
HEADSET = re.search(r'<span class="eyi" aria-hidden="true">(<svg.*?</svg>)</span>', page('s5-2').group(0), re.S).group(1)
edit('s5-gmdp', '<div class="pbox"><h2 class="h2" tabindex="-1">GMDP Support Team</h2></div>',
     '<div class="pbox gm-icon"><span class="gm-eyi" aria-hidden="true">' + HEADSET + '</span><h2 class="h2" tabindex="-1">GMDP Support Team</h2></div>')
s, n = re.subn(r'#s5-hv:has\(#hv-loc option\[value="\w+"\]:checked\):has\(#hv-team-\w+ option:not\(\[value=""\]\):checked\) \.hv-how\{display:none\}', '', s)
assert n == 3, n
CSS = '''/* 2.96 GMDP Support title box icon (like NHS login Support) */
#app .screen:not(#contents) .pbox.gm-icon>.gm-eyi{position:absolute!important;right:14px;bottom:14px;width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:#fff;color:#a3124d;box-shadow:0 3px 8px rgba(0,0,0,.25);z-index:2}
#app .screen:not(#contents) .pbox.gm-icon h2{max-width:calc(100% - 54px)!important}
@media screen and (max-height:600px){#app .screen:not(#contents) .pbox.gm-icon>.gm-eyi{display:none!important}#app .screen:not(#contents) .pbox.gm-icon h2{max-width:100%!important}}
/* 2.96 Contact & support > HV team: the instruction always stays, so nothing moves when a team is chosen.
   On shorter screens the lead line gives way instead (the Contact & support card already says what the team is for). */
@media screen and (max-height:700px){#app #s5-hv .hv-lead{display:none!important}}
@media screen and (max-height:600px){#app #s5-hv .scroll .hv-card{margin-top:7px!important}}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'
rep('Carer role v2.95', 'Carer role v2.96'); rep('Version 2.95 iPhone', 'Version 2.96 iPhone')
rep('<div>Version 2.95</div>', '<div>Version 2.96</div>'); rep('>2.95 – REVIEW DRAFT', '>2.96 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.93</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.95</span>', '<div class="rr"><span class="rv">2.96</span><span class="rd">19 Nov 2026</span><p>GMDP Support icon; Contact &amp; support team page no longer moves</p></div>\n<div class="rr"><span class="rv">2.95</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
