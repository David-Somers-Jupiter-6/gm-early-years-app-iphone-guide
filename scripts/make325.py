"""Guide 3.25 (from 3.24) – TRIAL (/preview/ only) mock-up. David, 21 Nov: put the Contents icon in the title box of
each section's opening page, on the right, so people can see where they are; Signing in gets the App's ABC block
icon.
 - Badge (white circle, bottom right of the title box, like the Troubleshooter / NHS login Support badges) on the
   pages Contents links to: Introduction (i), How this guide works (1), How to contact your HV team (2),
   About your account (3), Run through the Checklist (4), Signing in (the App icon), Troubleshooting (6),
   Contact & support (7), Accessibility (its icon), About this guide (book).
 - As with the existing badges, hidden on the shortest screens (600 px tall or less), and on the narrowest
   (under 370 px wide, where Signing in would go to three lines), so titles keep their room.
usage: python3 make325.py v3.24.html v3.25.html"""
import re, sys, base64
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>\n?' % re.escape(pid), s, re.S)
    assert m, pid
    return m

ICON = base64.b64encode(open(__file__.rsplit('/', 1)[0] + '/assets/app-icon-88.png', 'rb').read()).decode()
A11Y = '<svg viewBox="0 0 20 20" width="22" height="22"><circle cx="10" cy="3.9" r="1.8" fill="currentColor"/><path d="M4 7.3l6 1.2 6-1.2M10 8.5v3.7M10 12.2l-2.7 4.8M10 12.2l2.7 4.8" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
BOOK = '<svg viewBox="0 0 20 20" width="22" height="22"><path d="M10 5.2C8.4 3.9 6 3.4 2.8 3.6v11.6c3.2-.2 5.6.3 7.2 1.6 1.6-1.3 4-1.8 7.2-1.6V3.6c-3.2-.2-5.6.3-7.2 1.6z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M10 5.2v11.6" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>'
BADGES = {'intro': '<span class="sec-b sec-i">i</span>', 'how': '<span class="sec-b">1</span>', 'hv': '<span class="sec-b">2</span>',
          'acct': '<span class="sec-b">3</span>', 's2': '<span class="sec-b">4</span>',
          's3': '<span class="sec-b sec-app"><img src="data:image/png;base64,' + ICON + '" alt="" width="44" height="44"/></span>',
          's4': '<span class="sec-b">6</span>', 's5': '<span class="sec-b">7</span>', 'a11y': '<span class="sec-b">' + A11Y + '</span>',
          's6': '<span class="sec-b">' + BOOK + '</span>'}
for pid, badge in BADGES.items():
    m = page(pid); blk = m.group(0)
    badge = badge.replace('<span class="sec-b', '<span aria-hidden="true" class="sec-b')
    h = re.search(r'<h2 class="h2[^"]*" tabindex="-1">', blk); assert h, pid
    new = blk[:h.start()] + badge + blk[h.start():]
    # mark the title box so the title leaves room for the badge
    box = re.search(r'<div class="(pbox[^"]*|tp-body[^"]*)">(?=(?:(?!<div class="(?:pbox|tp-body)).)*?<span aria-hidden="true" class="sec-b)', new, re.S); assert box, pid
    new = new[:box.start()] + '<div class="%s has-sb">' % box.group(1) + new[box.end():]
    s = s[:m.start()] + new + s[m.end():]
assert s.count('class="sec-b') == 10

CSS = """/* 3.25 section badges: the Contents icon in the title box of each section's opening page */
#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb>.sec-b{position:absolute!important;right:14px;bottom:14px;z-index:2;width:42px;height:42px;border-radius:50%;display:grid;place-items:center;background:#fff;color:#a3124d;box-shadow:0 3px 8px rgba(0,0,0,.25);font:800 21px/1 var(--font-head)}
#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb>.sec-b.sec-i{font-family:Georgia,serif;font-style:italic;font-size:23px}
#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb>.sec-b.sec-app{width:44px;height:44px;border-radius:11px;background:none;overflow:hidden}
#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb>.sec-b.sec-app img{display:block;width:44px;height:44px}
#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb h2{max-width:calc(100% - 56px)!important}
@media screen and (max-height:600px),screen and (max-width:369px){#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb>.sec-b{display:none!important}#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb h2{max-width:100%!important}}
"""
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:')
_css = s[:s.index('@media print{')]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

rep('Carer role v3.24', 'Carer role v3.25'); rep('Version 3.24 iPhone', 'Version 3.25 iPhone')
rep('>3.24 – REVIEW DRAFT', '>3.25 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.24</span>', '<span class="cv-ver">Version 3.25</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.20</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.24</span>', '<div class="rr"><span class="rv">3.25</span><span class="rd">21 Nov 2026</span><p>Section badges in the title boxes (mock-up)</p></div>\n<div class="rr"><span class="rv">3.24</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
