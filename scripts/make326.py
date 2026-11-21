"""Guide 3.26 (from 3.22, the live version) – LIVE. David, 21 Nov: put the section badges (trial 3.25) live.
Also includes the Contents order fix (trial 3.24). The Troubleshooter (trial 3.23) stays on the trial page only.
 - Contents: 7 Contact & support, then Accessibility, then About this guide (book icon instead of 8); its pages say
   "About this guide" instead of "Section 8 · About this guide".
 - Section badges: the Contents icon in the title box of each section's opening page; Signing in shows the App's
   ABC block icon. Hidden at 600 px tall or less and under 370 px wide.
usage: python3 make326.py v3.22.html v3.26.html"""
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

BOOK17 = ('<svg aria-hidden="true" viewBox="0 0 20 20" width="17" height="17"><path d="M10 5.2C8.4 3.9 6 3.4 2.8 3.6v11.6c3.2-.2 5.6.3 7.2 1.6 1.6-1.3 4-1.8 7.2-1.6V3.6c-3.2-.2-5.6.3-7.2 1.6z" '
          'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M10 5.2v11.6" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>')

# --- 1. Contents order (as trial 3.24)
m = re.search(r'(<div class="toc-g">)(<a class="toc-row" href="#s6"><span class="gb">8</span>.*?</a>)\n(<a class="toc-row toc-a11y" href="#a11y">.*?</a>)(</div>)', s, re.S)
assert m
about = m.group(2).replace('<span class="gb">8</span>', '<span class="gb" aria-hidden="true">' + BOOK17 + '</span>')
s = s.replace(m.group(0), m.group(1) + m.group(3) + '\n' + about + m.group(4))
rep('Section 8 · About this guide', 'About this guide', 16)
rep('<section class="screen" id="s6" data-sec="About this guide" data-title="About this guide" aria-label="Section 8">',
    '<section class="screen" id="s6" data-sec="About this guide" data-title="About this guide" aria-label="About this guide">')
rep('<h2 class="h2 tp-h" tabindex="-1">About this guide</h2><span class="tp-n" aria-hidden="true">8</span>',
    '<h2 class="h2 tp-h" tabindex="-1">About this guide</h2>')

# --- 2. Section badges (as trial 3.25)
ICON = base64.b64encode(open(__file__.rsplit('/', 1)[0] + '/assets/app-icon-88.png', 'rb').read()).decode()
A11Y = '<svg viewBox="0 0 20 20" width="22" height="22"><circle cx="10" cy="3.9" r="1.8" fill="currentColor"/><path d="M4 7.3l6 1.2 6-1.2M10 8.5v3.7M10 12.2l-2.7 4.8M10 12.2l2.7 4.8" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
BOOK = BOOK17.replace('<svg aria-hidden="true" ', '<svg ').replace('width="17" height="17"', 'width="22" height="22"')
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
    box = re.search(r'<div class="(pbox[^"]*|tp-body[^"]*)">(?=(?:(?!<div class="(?:pbox|tp-body)).)*?<span aria-hidden="true" class="sec-b)', new, re.S); assert box, pid
    new = new[:box.start()] + '<div class="%s has-sb">' % box.group(1) + new[box.end():]
    s = s[:m.start()] + new + s[m.end():]
assert s.count('class="sec-b') == 10

CSS = """/* 3.26 section badges: the Contents icon in the title box of each section's opening page (trial 3.25) */
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

rep('Carer role v3.22', 'Carer role v3.26'); rep('Version 3.22 iPhone', 'Version 3.26 iPhone')
rep('>3.22 – REVIEW DRAFT', '>3.26 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.22</span>', '<span class="cv-ver">Version 3.26</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.18</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.22</span>', '<div class="rr"><span class="rv">3.26</span><span class="rd">21 Nov 2026</span><p>Section badges in the title boxes; Contents in page order</p></div>\n<div class="rr"><span class="rv">3.22</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
