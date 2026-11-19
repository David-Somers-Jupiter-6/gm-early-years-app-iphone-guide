"""Guide 2.95 (from 2.94). David, 19 Nov - all three mockups approved:
 A. Troubleshooting help pages (12) as three blocks: The issue (amber card) / Who can help (blue card with the
    team's logo) / What to do (green card, with the help buttons inside it as blue pills). Icons sit beside the
    small headings so the text uses the full card width.
 B. Signing in (Section 6 start): the three parts as a connected strip of tiles with icons/logos, and
    "You will need" as three icon rows.
 C. Stage marker on each section's first page, inside the title box above the title (no extra height, title in its
    usual place): three bars + "Stage N of 3 · What you need / How to sign in / Who can help".
    Health Visiting team page: the NHS band says "Stage 1 of 3". Hidden on iPhone SE in Safari (compact title boxes).
usage: python3 make295.py v2.94.html v2.95.html
"""
import re, sys, base64
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
def b64(p): return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
HERE = __file__.rsplit('/', 1)[0]
NHS = b64(HERE + '/nhsmark_white.png'); ABC = b64(HERE + '/abc_round_64.png')

# A. Troubleshooting help pages
ABCPAGES = ['s4-setup', 's4-cannot', 's4-pw', 's4-code', 's4-email', 's4-mobile', 's4-name', 's4-activation', 's4-problems', 's4-1b', 's4-2', 's4-help']
for pid in ABCPAGES:
    blk = page(pid).group(0)
    who = re.search(r'<span class="abc-ic ic-who" aria-hidden="true"><svg.*?</svg></span>', blk, re.S).group(0)
    team = re.search(r'Who can help</p><p><strong>([^<]*)</strong>', blk).group(1)
    kind = 'who-gm' if 'GMDP' in team else 'who-nhs'
    edit(pid, who, '<span class="abc-ic ic-who %s" aria-hidden="true"></span>' % kind)
    blk = page(pid).group(0)
    links = re.search(r'</div></div></div>(<div class="hv-card sp-card abc-links">.*?</a></div>)', blk, re.S)
    if links:
        edit(pid, '</div></div></div>' + links.group(1), links.group(1) + '</div></div></div>')

# B. Signing in overview
PHONE = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><rect x="6.5" y="2.5" width="11" height="19" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10.5 18.5h3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><rect x="3" y="5.5" width="18" height="13" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3.5 7l8.5 6 8.5-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'
KEY = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="8" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 12h9M18 12v3M21 12v2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
ARR = '<span class="jr-a" aria-hidden="true"><svg viewBox="0 0 20 20" width="16" height="16"><path d="M7.5 4.5L13 10l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
s3 = page('s3').group(0)
old = s3[s3.find('<p class="lead">There are <strong>15 steps</strong>, in three parts:</p>'):s3.find('<p class="lead">Select <strong>Begin</strong> below to start.</p>') + len('<p class="lead">Select <strong>Begin</strong> below to start.</p>')]
assert old.startswith('<p class="lead">There are') and old.endswith('start.</p>'), old[:60]
NEW = ('<ol class="jr" aria-label="15 steps, in three parts">'
       '<li class="jr-n"><span class="jr-ic" aria-hidden="true">' + PHONE + '</span><b>Get started</b><small>Steps 1–3</small></li>' + ARR +
       '<li class="jr-n"><span class="jr-ic jr-nhs" aria-hidden="true"></span><b>NHS login</b><small>Steps 4–9</small></li>' + ARR +
       '<li class="jr-n"><span class="jr-ic jr-abc" aria-hidden="true"></span><b>GM Early Years App</b><small>Steps 10–15</small></li></ol>\n'
       '<p class="jr-k">You will need</p>\n<ul class="nd">'
       '<li><span aria-hidden="true">' + MAIL + '</span>Your NHS login email address</li>'
       '<li><span aria-hidden="true">' + KEY + '</span>Your NHS login password</li>'
       '<li><span aria-hidden="true">' + PHONE + '</span>Your iPhone, to get text messages</li></ul>')
edit('s3', old, NEW)

# C. Stage marker
STAGES = {1: 'What you need', 2: 'How to sign in', 3: 'Who can help'}
def marker(n):
    bars = ''.join('<i%s></i>' % (' class="on"' if i == n else '') for i in (1, 2, 3))
    return '<div class="stg"><span class="stg-b" aria-hidden="true">%s</span><span class="stg-t">Stage %d of 3 · %s</span></div>' % (bars, n, STAGES[n])
for pid, n in (('s2', 1), ('s3', 2), ('s4', 3), ('s5', 3)):
    edit(pid, '<div class="tp-card"><div class="tp-body">', '<div class="tp-card"><div class="tp-body tp-stg">' + marker(n))
for pid in ('acct', 'nhs'):
    edit(pid, '<div class="pbox"><h2 class="h2" tabindex="-1">', '<div class="pbox tp-stg">' + marker(1) + '<h2 class="h2" tabindex="-1">')
edit('hv', '<i class="eym"></i><b>Health Visiting team</b></div>', '<i class="eym"></i><b>Health Visiting team</b><span>Stage 1 of 3</span></div>')

CSS = '''/* 2.95 A. Troubleshooting help pages as three blocks */
#app .screen .abc-row{display:block!important;position:relative;margin:0 0 6px;padding:7px 11px 8px!important;border:1px solid var(--line)!important;border-left:5px solid!important;border-radius:14px;background:var(--surface)}
#app .screen .abc-row:nth-child(1){border-left-color:#b26b00!important;background:var(--amberBg,#fff7dc)}
#app .screen .abc-row:nth-child(2){border-left-color:#005eb8!important}
#app .screen .abc-row:nth-child(3){border-left-color:#00703c!important}
#app .screen .abc-ic{position:absolute;left:11px;top:7px;width:22px!important;height:22px!important;font-size:13px!important;color:#fff!important;border:0!important}
#app .screen .abc-ic svg{width:13px;height:13px;color:#fff;stroke:#fff}
#app .screen .abc-ic.ic-issue{background:#b26b00!important}
#app .screen .abc-ic.ic-do{background:#00703c!important}
#app .screen .abc-ic.who-nhs{border-radius:6px;background:#005eb8 url(@NHS@) center/18px auto no-repeat!important}
#app .screen .abc-ic.who-gm{border-radius:6px;background:url(@ABC@) center/16px 16px no-repeat,linear-gradient(135deg,#6c155c,#d01545)!important}
#app .screen .abc-k{padding-left:30px;line-height:22px!important;margin:0 0 2px!important}
#app .screen .abc-row .abc-links{margin:7px 0 1px!important;padding:0!important;background:none!important;border:0!important;box-shadow:none!important;display:flex;flex-direction:column;align-items:flex-start;gap:6px}
#app .screen .abc-row .abc-links .abc-btn{display:inline-flex!important;align-items:center;gap:7px;padding:6px 13px!important;border:0!important;border-radius:999px;background:#005eb8;text-decoration:none!important}
#app .screen .abc-row .abc-links .abc-btn strong,#app .screen .abc-row .abc-links .abc-btn .abc-addr{color:#fff!important}
#app .screen .abc-row .abc-links .abc-btn svg{color:#fff;stroke:currentColor;flex:0 0 auto}
#app .screen .abc-row .abc-links .abc-mail{border-radius:14px;align-items:flex-start!important}
#app .screen .abc-ask{margin:0!important}
@media screen and (max-height:700px),screen and (max-width:369px){#app .screen .abc-row{padding:5px 10px 6px!important;margin-bottom:5px}#app .screen .abc-ic{top:5px;width:19px!important;height:19px!important;font-size:12px!important}#app .screen .abc-ic svg{width:11px;height:11px}#app .screen .abc-ic.who-nhs{background-size:15px auto!important}#app .screen .abc-ic.who-gm{background-size:14px 14px,auto!important}#app .screen .abc-k{line-height:19px!important;margin-bottom:1px!important;padding-left:27px}#app .screen .abc-row .abc-links{margin-top:5px!important;gap:4px}#app .screen .abc-row .abc-links .abc-btn{padding:4px 12px!important}#app .screen .abc-row .abc-links .abc-btn strong{font-size:15px}#app .screen .abc-sub{line-height:1.25!important}#app .screen :is(.abc-steps,.abc-list){gap:1px!important}#app .screen .abc-row :is(p,li){line-height:1.3!important}#app .screen .abc-ask{margin-top:0!important;padding:5px 10px!important}#app .screen .abc-ask p{line-height:1.3!important}#app .screen .abc-ask .k{margin-bottom:1px}}
@media screen and (max-height:600px),screen and (max-width:369px){#app .screen .abc-sub{font-size:14px!important}#app .screen .abc-row{padding:4px 9px 5px!important;margin-bottom:4px}}
@media screen and (max-height:600px){#app .screen .abc-row{margin-bottom:3px}#app .screen .abc-row :is(p,li),#app .screen .abc-ask p{line-height:1.25!important}#app .screen .abc-row .abc-links{margin-top:4px!important;gap:3px}#app .screen .abc-row .abc-links .abc-btn{padding:3px 11px!important}#app .screen .abc-row .abc-links .abc-btn strong{font-size:14px}#app .screen .abc-sub{line-height:1.2!important}#app .screen .abc-k{margin-bottom:0!important}#app .screen :is(.abc-steps,.abc-list){gap:0!important}#app .screen .abc-ask{padding-top:4px!important;padding-bottom:4px!important}}
/* 2.95 B. Signing in overview */
#app #s3 .jr{display:flex;align-items:stretch;gap:2px;margin:0 0 14px;padding:0;list-style:none}
#app #s3 .jr-n{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;margin:0;padding:10px 4px;border:1px solid var(--line);border-radius:12px;background:var(--surface)}
#app #s3 .jr-ic{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;background:var(--accentSoft);color:var(--accent2)}
#app #s3 .jr-nhs{background:#005eb8 url(@NHS@) center/28px auto no-repeat}
#app #s3 .jr-abc{background:url(@ABC@) center/26px 26px no-repeat,linear-gradient(135deg,#6c155c,#d01545)}
#app #s3 .jr-n b{font:700 14px/1.2 var(--font-head);color:var(--ink)}
#app #s3 .jr-n small{font-size:13px!important;line-height:1.2;color:var(--sub)}
#app #s3 .jr-a{align-self:center;color:var(--sub);display:flex}
#app #s3 .jr-k{margin:0 0 6px;font:700 13px/1.2 var(--font-head);letter-spacing:.06em;text-transform:uppercase;color:var(--sub)}
#app #s3 .nd{list-style:none;margin:0;padding:0;border:1px solid var(--line);border-radius:12px;background:var(--surface)}
#app #s3 .nd li{display:flex;align-items:center;gap:10px;margin:0;padding:8px 12px;font-size:16px;line-height:1.3;color:var(--ink)}
#app #s3 .nd li+li{border-top:1px solid var(--line)}
#app #s3 .nd li>span{flex:0 0 30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;background:var(--accentSoft);color:var(--accent2)}
@media screen and (max-height:600px){#app #s3 .jr{margin-bottom:10px}#app #s3 .jr-n{padding:7px 3px}#app #s3 .nd li{padding:6px 12px}}
@media screen and (max-width:369px){#app #s3 .jr-n b{font-size:13px}#app #s3 .jr-ic{width:32px;height:32px}}
/* 2.95 C. Stage marker in the title box of each section's first page */
#app .screen .tp-stg{position:relative}
#app .screen:not(#contents) :is(.pbox,.tp-body).tp-stg>.stg{position:absolute!important;left:18px;right:72px;top:10px;z-index:2;pointer-events:none;margin:0!important}
#app .screen .stg-b{display:flex;gap:4px;width:84px}
#app .screen .stg-b i{flex:1;height:5px;border-radius:3px;background:rgba(255,255,255,.35)}
#app .screen .stg-b i.on{background:#fff}
#app .screen .stg-t{display:block;margin-top:6px;font:700 11.5px/1.2 var(--font-head);letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.9);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media screen and (max-width:369px){#app .screen:not(#contents) :is(.pbox,.tp-body).tp-stg>.stg{right:12px}#app .screen .stg-t{font-size:10.5px;letter-spacing:.06em}}
@media screen and (max-height:600px){#app .screen:not(#contents) :is(.pbox,.tp-body).tp-stg>.stg{display:none}}
'''.replace('@NHS@', NHS).replace('@ABC@', ABC)
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

rep('Carer role v2.94', 'Carer role v2.95'); rep('Version 2.94 iPhone', 'Version 2.95 iPhone')
rep('<div>Version 2.94</div>', '<div>Version 2.95</div>'); rep('>2.94 – REVIEW DRAFT', '>2.95 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.92</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.94</span>', '<div class="rr"><span class="rv">2.95</span><span class="rd">19 Nov 2026</span><p>Troubleshooting three blocks; Signing in overview; stage marker</p></div>\n<div class="rr"><span class="rv">2.94</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
