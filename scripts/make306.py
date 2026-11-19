"""Guide 3.06 (from 3.05). David, 19 Nov: "How to install the GM Early Years App" (from the A4 guide
"GM Early Years App – How to install the App on a mobile phone (iOS) – Carer Role v1.04") added inside
Troubleshooting > GM Early Years App issues, in the Signing in design.
 - s4-gm list: new first item "How to install the App" -> inst
 - inst: intro (You will need: Apple ID signed in, internet connection; GMDP Support help line)
 - inst-1 ... inst-7 step pages (title box with progress bar, "Installing the App" label, "Step N of 7" for screen readers,
   instruction, Tap chip, screenshot 248 wide cropped to the highlighted part, Tap to enlarge), plus tip pages
   inst-4-tip ("Get" button for first-time downloads) and inst-7-tip (installation complete -> Section 5 · Signing in)
 - CSS: every Signing in rule (`[data-sec^="Section 5"]`, `[id^="step-"]`) also applies to pages with data-inst;
   the intro uses the Signing in "You will need" list style; install progress bar segments = Signing in segment size
 - Back/Next chain, Troubleshooting "Page N of 40", Contents counters "N / 80"
Screenshots: scripts/assets/install/shot*.png (417 px wide, from the A4 guide), stored as JPEG.
usage: python3 make306.py v3.05.html v3.06.html"""
import re, sys, io, base64, os
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'install')
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>' % re.escape(pid), s, re.S); assert m, pid; return m
def in_page(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0); assert blk.count(a) == n, (pid, a[:80], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

CHEV = '<span class="tc-c"><svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M7.5 4.5L13 10l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
DL = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 10l5 5 5-5"/><path d="M4 17v2.5A1.5 1.5 0 005.5 21h13a1.5 1.5 0 001.5-1.5V17"/></svg>'
ZOOM = re.search(r'<span class="zoom" aria-hidden="true">.*?</span>', page('step-2').group(0), re.S).group(0)
BACK_SVG = re.search(r'<a class="nav-btn nav-back" href="#[^"]+">(<svg.*?</svg>)', s, re.S).group(1)
NEXT_SVG = re.search(r'<a class="nav-btn nav-next" href="#[^"]+"><span>Next</span>(<svg.*?</svg>)', s, re.S).group(1)
MENU = re.search(r'<a class="menu-btn" href="#contents" aria-label="Contents \(page \d+ of \d+\)">(<svg.*?</svg>)', s, re.S).group(1)
def nav(prev, nxt, label='Next', start=False):
    return ('<nav class="bnav" aria-label="Page navigation"><a class="nav-btn nav-back" href="#%s">%s<span>Back</span></a>'
            '<a class="menu-btn" href="#contents" aria-label="Contents (page 0 of 0)">%s<span class="ml">Contents</span><span class="count">0 / 0</span></a>'
            '<a class="nav-btn nav-next%s" href="#%s"><span>%s</span>%s</a></nav>') % (prev, BACK_SVG, MENU, ' nav-start' if start else '', nxt, label, NEXT_SVG)
def strip():
    return '<div class="strip" aria-hidden="true"><div class="strip-row"><span>Section 6 · Troubleshooting</span><span class="pos">Page X of 40</span></div></div>\n'

def shot(fn, alt, y, et, eb, pb):
    im = Image.open(os.path.join(ASSETS, fn)).convert('RGB'); w, h = im.size
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=84, optimize=True, progressive=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    zid = 'z-in' + fn[4:6]
    return ('<input type="checkbox" class="zt" id="%s" aria-label="Show the whole screen: %s"/>'
            '<label class="shot" for="%s" style="--cw:%d;--ch:%d;--fw:%d;--x:0;--y:%d;--et:%d;--eb:%d;--pb:%d;--ih:%d">'
            '<span class="crop"><img alt="%s" src="data:image/jpeg;base64,%s" width="%d" height="%d"/></span>%s'
            '<span class="zoom-close" aria-hidden="true">Tap anywhere to close</span></label>\n') % (
            zid, alt, zid, w, pb - y, w, y, et, eb, pb, h, alt, b64, w, h, ZOOM)

def stepper(cur, tip=False):
    out = []
    for i in range(1, 8):
        if i < cur: out.append('<span class="d">✓</span>')
        elif i == cur: out.append('<span class="c">%d</span>' % i)
        else: out.append('<span class="">%d</span>' % i)
    return '<div class="stepper" aria-hidden="true">' + ''.join(out) + '</div>'

def tapc(lbl, chip):
    return '<div class="tap"><span class="lbl">%s</span><span class="chip">%s</span></div>\n' % (lbl, chip)

STEPS = [  # n, title, body html, tap, shot args
    (1, 'Open the App Store', '<p>On your iPhone, find the <strong>App Store</strong> and tap it.</p>\n', tapc('Tap', 'App Store'),
     ('shot06.png', 'iPhone Home Screen with the App Store icon highlighted', 300, 470, 620, 760)),
    (2, 'Tap Search', '<p>When the App Store opens, tap <strong>Search</strong> at the bottom of the screen.</p>\n', tapc('Tap', 'Search'),
     ('shot09.png', 'App Store Today screen with Search highlighted at the bottom of the screen', 440, 760, 885, 904)),
    (3, 'Search for the App', '<p>Tap the search box and type <strong>gm early years</strong>. Look for <strong>GM Early Years</strong> with the ABC blocks icon.</p>\n', '',
     ('shot10.png', 'App Store search for gm early years, with GM Early Years by Greater Manchester Early Years in the results', 30, 40, 600, 600)),
    (4, 'Download the App', '<p>Next to <strong>GM Early Years</strong>, tap the <strong>Download</strong> button.</p>\n', tapc('Tap', 'Download'),
     ('shot13.png', 'GM Early Years in the App Store results with the Download button highlighted', 330, 520, 660, 700)),
    (5, 'Wait while it installs', '<p>The App downloads and installs. The button fills in a circle to show the progress.</p>\n', tapc('Look for', 'Progress circle'),
     ('shot15.png', 'GM Early Years in the App Store results with the download progress circle highlighted', 330, 520, 660, 700)),
    (6, 'Open the App', '<p>When it has finished, the button changes to <strong>Open</strong>. Tap <strong>Open</strong>.</p>\n', tapc('Tap', 'Open'),
     ('shot17.png', 'GM Early Years in the App Store results with the Open button highlighted', 330, 520, 660, 700)),
    (7, 'The sign-in screen opens', '<p>The GM Early Years App opens on its sign-in screen. The App is now installed on your iPhone.</p>\n', '',
     ('shot18.png', 'The GM Early Years App sign-in screen with Continue with NHS login highlighted', 120, 150, 460, 720)),
]

pages = []  # (id, html-without-nav)
# intro
ND = lambda svg, txt: '<li><span aria-hidden="true">%s</span>%s</li>' % (svg, txt)
SVG_ID = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="12" cy="8" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M4.5 20c1.3-3.7 4.2-5.6 7.5-5.6s6.2 1.9 7.5 5.6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
SVG_WIFI = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M2.5 9a14 14 0 0119 0M5.5 12.5a9.5 9.5 0 0113 0M8.6 15.8a5 5 0 016.8 0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="19" r="1.4" fill="currentColor"/></svg>'
pages.append(('inst', '<section class="screen" id="inst" data-sec="Section 6 · Troubleshooting" data-title="How to install the GM Early Years App" aria-label="How to install the GM Early Years App">\n'
    '<div class="scroll">\n<div class="pbox"><h2 class="h2" tabindex="-1">How to install the App</h2></div>\n' + strip() +
    '<p class="info-lead">Install the GM Early Years App from the App Store in 7 steps. Follow them in order.</p>\n'
    '<p class="jr-k">You will need</p>\n<ul class="nd">' + ND(SVG_ID, 'Your Apple ID, signed in on your iPhone') + ND(SVG_WIFI, 'An internet connection') + '</ul>\n'
    '<div class="tip inst-help"><span class="k">Need help installing the App?</span><p>Contact the <a href="#s5-gmdp">GMDP Support Team</a>.</p></div>\n'
    '</div>\n', 'Begin'))
for n, title, body, tap, sh in STEPS:
    pages.append(('inst-%d' % n,
        '<section class="screen" id="inst-%d" data-sec="Section 6 · Troubleshooting" data-inst="" data-title="Install step %d · %s" aria-label="Install step %d">\n' % (n, n, title, n) +
        '<div class="scroll">\n<div class="pbox has-n">' + stepper(n) + '<span class="tp-n" aria-hidden="true">%d</span><div class="kicker part">Installing the App</div>' % n +
        '<h2 tabindex="-1"><span class="vh">Step %d of 7: </span>%s</h2></div>\n' % (n, title) + strip() +
        '<div class="step-body">\n' + body + tap + shot(*sh) + '</div>\n</div>\n', 'Next'))
    if n == 4:
        pages.append(('inst-4-tip',
            '<section class="screen" id="inst-4-tip" data-sec="Section 6 · Troubleshooting" data-inst="" data-title="Install step 4 · Helpful tip" aria-label="Install step 4, helpful tip">\n'
            '<div class="scroll">\n<div class="pbox has-n">' + stepper(4) + '<span class="tp-n" aria-hidden="true">4</span><div class="kicker">Helpful tip</div>'
            '<h2 tabindex="-1"><span class="vh">Helpful tip – Step 4 of 7: </span>Download the App</h2></div>\n' + strip() +
            '<div class="step-body tip-page">\n<div class="tip"><span class="k">Helpful tip</span><p>If you have not had the App before, the button says <strong>Get</strong>. '
            'Tap <strong>Get</strong>. Your iPhone may ask you to confirm with Face ID, Touch ID or your Apple ID password.</p></div>\n</div>\n</div>\n', 'Next'))
    if n == 7:
        pages.append(('inst-7-tip',
            '<section class="screen" id="inst-7-tip" data-sec="Section 6 · Troubleshooting" data-inst="" data-title="Install step 7 · Next step" aria-label="Install step 7, next step">\n'
            '<div class="scroll">\n<div class="pbox has-n">' + stepper(8) + '<span class="tp-n" aria-hidden="true">7</span><div class="kicker">Installation complete</div>'
            '<h2 tabindex="-1"><span class="vh">Installation complete – Step 7 of 7: </span>Next, sign in</h2></div>\n' + strip() +
            '<div class="step-body tip-page">\n<div class="tip"><span class="k">Installation complete</span><p>The GM Early Years App is installed on your iPhone.</p></div>\n'
            '<p class="inst-next">To sign in to the App, go to <a href="#s3">Section 5 · Signing in</a>.</p>\n</div>\n</div>\n', 'Next'))

# chain: s4-gm -> inst ... inst-7-tip -> s4-activation
chain = ['s4-gm'] + [p[0] for p in pages] + ['s4-activation']
html = ''
for i, (pid, body, label) in enumerate(pages):
    html += body + nav(chain[i], chain[i + 2], label, start=(label == 'Begin')) + '\n</section>\n'
in_page('s4-gm', '<a class="nav-btn nav-next" href="#s4-activation">', '<a class="nav-btn nav-next" href="#inst">')
in_page('s4-activation', '<a class="nav-btn nav-back" href="#s4-gm">', '<a class="nav-btn nav-back" href="#inst-7-tip">')
m = page('s4-activation'); s = s[:m.start()] + html + s[m.start():]
# s4-gm list: install first
in_page('s4-gm', '<nav aria-label="GM Early Years App issues" class="tr-list">',
        '<nav aria-label="GM Early Years App issues" class="tr-list"><a class="tr" href="#inst"><span class="tr-i">' + DL + '</span><span class="tr-t">How to install the App</span>' + CHEV + '</a>')

# numbering
ids = re.findall(r'<section class="screen(?: cover)?" id="([^"]+)"', s)
tr = [i for i in ids if 'data-sec="Section 6 · Troubleshooting"' in page(i).group(0)[:300]]
assert len(tr) == 40, len(tr)
for n, pid in enumerate(tr, 1):
    blk = page(pid).group(0); new = re.sub(r'<span class="pos">Page (?:\d+|X) of (?:30|40)</span>', f'<span class="pos">Page {n} of 40</span>', blk, count=1)
    assert new != blk, pid; m = page(pid); s = s[:m.start()] + new + s[m.end():]
assert ids[-1] == 'search', ids[-3:]
T = len(ids) - 1; assert T == 80, T
for idx, pid in enumerate(ids, 1):
    blk = page(pid).group(0)
    new = re.sub(r'\(page \d+ of \d+\)', f'(page {idx} of {T})', blk)
    new = re.sub(r'<span class="count">\d+ / \d+</span>', f'<span class="count">{idx} / {T}</span>', new)
    if new != blk: m = page(pid); s = s[:m.start()] + new + s[m.end():]
assert not re.search(r'of 70\)|/ 70</span>|Page X of', s)
for a, b in zip(ids, ids[1:]):
    na = re.search(r'class="nav-btn nav-next[^"]*" href="#([^"]+)"', page(a).group(0))
    bb = re.search(r'class="nav-btn nav-back" href="#([^"]+)"', page(b).group(0))
    if a in chain: assert na.group(1) == b and bb.group(1) == a, (a, b, na.group(1), bb.group(1))

# CSS: Signing in rules also for install pages
cs = s.find('<style'); ce = s.find('</style>', cs); css = s[cs:ce]
def widen(mt):
    sel, body = mt.group(1), mt.group(2)
    if 'nth-child' in sel: return mt.group(0)
    sel = sel.replace('[data-sec^="Section 5"]', ':is([data-sec^="Section 5"],[data-inst])').replace('[id^="step-"]', ':is([id^="step-"],[data-inst])')
    if '#app #s3 .jr-k' in sel or re.search(r'#app #s3 \.nd\b', sel): sel = sel.replace('#app #s3 ', '#app :is(#s3,#inst) ')
    return sel + '{' + body + '}'
css2 = re.sub(r'([^{}]+)\{([^{}]*)\}', widen, css)
print('widened', css2.count('[data-inst]'), css2.count(':is(#s3,#inst)'))
s = s[:cs] + css2 + s[ce:]
CSS = '''/* 3.06 How to install the App (Troubleshooting > GM Early Years App issues), Signing in design */
#app .screen[data-inst] .pbox .stepper span{flex:0 0 calc((100% - 56px) / 15)!important;width:auto!important}
#app #inst .info-lead{margin-bottom:14px}
#app #inst .tip.inst-help{margin-top:16px}
#app #inst-7-tip .inst-next{margin-top:14px;font-size:17px;line-height:1.5}
@media screen and (max-height:600px){#app #inst .info-lead{margin-bottom:10px}#app #inst .tip.inst-help{margin-top:12px}}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

# version
rep('Carer role v3.05', 'Carer role v3.06'); rep('Version 3.05 iPhone', 'Version 3.06 iPhone')
rep('<div>Version 3.05</div>', '<div>Version 3.06</div>'); rep('>3.05 – REVIEW DRAFT', '>3.06 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">3\.03</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.05</span>', '<div class="rr"><span class="rv">3.06</span><span class="rd">19 Nov 2026</span><p>How to install the App added to GM Early Years App issues</p></div>\n<div class="rr"><span class="rv">3.05</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, len(s))
