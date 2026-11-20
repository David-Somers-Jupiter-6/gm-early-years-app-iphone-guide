"""Guide 3.11 (from trial 3.10) – TRIAL (/preview/). David, 20 Nov: accessibility statement and a short privacy note.
 - Contrast fixes found by an axe-core check of every page (light and Dark Mode):
   cover quick links (white on 14% white over blue, 4.0:1) -> white buttons with dark blue text;
   green Start / Begin / Yes buttons #00843d (4.4:1 while pulsing) -> NHS dark green #00703c (7:1);
   Dark Mode: NHS login / GM Early Years App card headings on Your account details and "Help from" names on the
   Troubleshooting menu -> lighter blue / pink
 - Section 8 · About this guide: new pages after Document control
     a11y-stmt    Accessibility statement (who it is for, what you should be able to do)
     a11y-stmt-2  Known issues (compliance status: partially compliant until a full audit; known limitations)
     a11y-stmt-3  Feedback and contact (other formats, reporting problems, EHRC / EASS)
     a11y-stmt-4  How it was tested (what was checked, when, statement date)
     privacy      Your privacy (nothing is collected; what stays on the phone; voice search; hosting; links)
   About this guide menu lists them; the Accessibility page (Section 7) links to the statement.
 - Back/Next chain, Section 8 "Page N of 8", Contents counters "N / 86"
usage: python3 make311.py v3.10.html v3.11.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
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

GMDP = 'gmdp.support@greatermanchester-ca.gov.uk'
URL = 'https://david-somers-jupiter-6.github.io/gm-early-years-app-iphone-guide/'
EASS = 'https://www.equalityadvisoryservice.com/'
CHEV = re.search(r'<a class="toc-row" href="#doc-control">.*?(<svg.*?</svg>)</a>', s, re.S).group(1)
TICK = '<svg viewBox="0 0 20 20" width="15" height="15" aria-hidden="true"><path d="M4.5 10.5l3.5 3.5 7.5-8" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
DOT = '<svg viewBox="0 0 20 20" width="15" height="15" aria-hidden="true"><circle cx="10" cy="10" r="3.2" fill="currentColor"/></svg>'
def lst(items, icon=TICK, cls='st-list'):
    return '<ul class="%s">' % cls + ''.join('<li><span aria-hidden="true">%s</span><span>%s</span></li>' % (icon, t) for t in items) + '</ul>\n'

nav_tpl = re.search(r'<nav class="bnav".*?</nav>', page('doc-control').group(0), re.S).group(0)
def nav(prev, nxt):
    n = re.sub(r'class="nav-btn nav-back" href="#[^"]+"', 'class="nav-btn nav-back" href="#%s"' % prev, nav_tpl)
    return re.sub(r'class="nav-btn nav-next" href="#[^"]+"', 'class="nav-btn nav-next" href="#%s"' % nxt, n)
def strip():
    return '<div class="strip" aria-hidden="true"><div class="strip-row"><span>Section 8 · About this guide</span><span class="pos">Page X of 8</span></div></div>\n'
def screen(pid, title, h2, body):
    return ('<section class="screen" id="%s" data-sec="Section 8 · About this guide" data-title="%s" aria-label="%s">\n<div class="scroll">\n'
            '<div class="pbox"><h2 class="h2" tabindex="-1">%s</h2></div>\n' % (pid, title, title, h2) + strip() + body + '</div>\n')

P = []
P.append(('a11y-stmt', screen('a11y-stmt', 'Accessibility statement', 'Accessibility statement',
    '<p class="st-p">This statement is for the <strong>GM Early Years App iPhone guide</strong>, run by the Greater Manchester Combined Authority (GMCA).</p>\n'
    '<p class="st-p">We want as many people as possible to be able to use it. You should be able to:</p>\n' +
    lst(['zoom in up to 200% without text being cut off', 'use portrait or landscape, and Dark Mode', 'search by typing, or by voice in Safari', 'move between pages with Back and Next, or by swiping']))))
P.append(('a11y-stmt-2', screen('a11y-stmt-2', 'Accessibility statement: known issues', 'Known issues',
    '<h3 class="pg-h st-h">Compliance status</h3>\n'
    '<p class="st-p">We believe this guide meets <strong>WCAG 2.2 AA</strong>, but it has not had a full independent audit yet. Until then, it is <strong>partially compliant</strong>.</p>\n'
    '<h3 class="pg-h st-h">What may not work well</h3>\n' +
    lst(['Text does not grow with the iPhone’s <strong>Larger Text</strong> setting. Zoom with Safari’s <strong>aA</strong> button instead.',
         'Screenshots show text from the App and NHS login. Each has a written description, and the steps are written out.',
         'The guide has not yet been tested with people who use screen readers.'], DOT, 'st-list st-dots'))))
P.append(('a11y-stmt-3', screen('a11y-stmt-3', 'Accessibility statement: feedback and contact', 'Feedback and contact',
    '<p class="st-p">If you need this guide in a different format, such as <strong>large print</strong>, <strong>easy read</strong> or <strong>another language</strong>, or you find a problem not listed here, email the GMDP Support Team:</p>\n'
    '<a class="st-mail" href="mailto:%s">%s</a>\n' % (GMDP, GMDP.replace('@', '@<wbr>')) +
    '<p class="st-p">We will consider your request and get back to you.</p>\n'
    '<h3 class="pg-h st-h">If you are not happy with our reply</h3>\n'
    '<p class="st-p">The Equality and Human Rights Commission (EHRC) enforces the accessibility regulations. If you are not happy with how we respond, contact the <a href="%s" target="_blank" rel="noopener">Equality Advisory and Support Service (EASS)</a>.</p>\n' % EASS)))
P.append(('a11y-stmt-4', screen('a11y-stmt-4', 'Accessibility statement: how it was tested', 'How it was tested',
    '<p class="st-p">GMCA is committed to making this guide accessible, in line with the Public Sector Bodies (Websites and Mobile Applications) (No. 2) Accessibility Regulations 2018.</p>\n'
    '<p class="st-p">On <strong>20 November 2026</strong> the guide was checked:</p>\n' +
    lst(['with an automated tool (axe-core) on every page, in light and Dark Mode', 'on 13 iPhone screen sizes, and at 200% zoom', 'in portrait and landscape']) +
    '<p class="st-p st-small">This statement was prepared on 20 November 2026. It will be reviewed by November 2027.</p>\n')))
P.append(('privacy', screen('privacy', 'Your privacy', 'Your privacy',
    '<p class="st-lead"><span aria-hidden="true">%s</span>This guide does not collect any information about you.</p>\n' % TICK +
    lst(['No sign-in, no cookies and no tracking.',
         'What you type and choose stays on your iPhone. It is cleared when you close the guide.',
         'Voice search uses Apple’s speech service, only if you tap the microphone.',
         'The website host, GitHub, may keep technical details such as IP addresses.']) +
    '<p class="st-p st-small">Questions? Email <a href="mailto:%s">GMDP Support</a>.</p>\n' % GMDP)))

order = ['doc-control'] + [p[0] for p in P] + ['revisions']
html = ''.join(body + nav(order[i], order[i + 2]) + '\n</section>\n' for i, (pid, body) in enumerate(P))
in_page('doc-control', 'class="nav-btn nav-next" href="#revisions"', 'class="nav-btn nav-next" href="#a11y-stmt"')
in_page('revisions', 'class="nav-btn nav-back" href="#doc-control"', 'class="nav-btn nav-back" href="#privacy"')
m = page('revisions'); s = s[:m.start()] + html + s[m.start():]

# About this guide menu + Accessibility page link
in_page('s6', '<a class="toc-row" href="#revisions"><span class="gb">2</span><span class="tt">Revision history<small>Latest changes to this guide</small></span>',
        '<a class="toc-row" href="#a11y-stmt"><span class="gb">2</span><span class="tt">Accessibility statement<small>How accessible this guide is</small></span>' + CHEV + '</a>\n'
        '<a class="toc-row" href="#privacy"><span class="gb">3</span><span class="tt">Your privacy<small>Nothing about you is collected</small></span>' + CHEV + '</a>\n'
        '<a class="toc-row" href="#revisions"><span class="gb">4</span><span class="tt">Revision history<small>Latest changes to this guide</small></span>')
in_page('a11y', '<a href="mailto:gmdp.support@greatermanchester-ca.gov.uk">gmdp.support@greatermanchester-ca.gov.uk</a>.</p></div>',
        '<a href="mailto:gmdp.support@greatermanchester-ca.gov.uk">gmdp.support@greatermanchester-ca.gov.uk</a>.</p></div>\n'
        '<a class="st-go" href="#a11y-stmt">Read the accessibility statement' + CHEV + '</a>')

# numbering
ids = re.findall(r'<section class="screen(?: cover)?" id="([^"]+)"', s)
sec8 = [i for i in ids if 'data-sec="Section 8 · About this guide"' in page(i).group(0)[:300]]
assert sec8 == ['s6', 'doc-control', 'a11y-stmt', 'a11y-stmt-2', 'a11y-stmt-3', 'a11y-stmt-4', 'privacy', 'revisions'], sec8
for n, pid in enumerate(sec8, 1):
    blk = page(pid).group(0); new = re.sub(r'<span class="pos">Page (?:\d+|X) of (?:3|8)</span>', f'<span class="pos">Page {n} of 8</span>', blk, count=1)
    assert new != blk, pid; m = page(pid); s = s[:m.start()] + new + s[m.end():]
assert ids[-1] == 'search'; T = len(ids) - 1; assert T == 86, T
for idx, pid in enumerate(ids, 1):
    blk = page(pid).group(0)
    new = re.sub(r'\(page \d+ of \d+\)', f'(page {idx} of {T})', blk)
    new = re.sub(r'<span class="count">\d+ / \d+</span>', f'<span class="count">{idx} / {T}</span>', new)
    if new != blk: m = page(pid); s = s[:m.start()] + new + s[m.end():]
assert 'Page X of' not in s
for a, b in zip(ids, ids[1:]):
    if a in order[:-1]:
        na = re.search(r'class="nav-btn nav-next[^"]*" href="#([^"]+)"', page(a).group(0)).group(1)
        bb = re.search(r'class="nav-btn nav-back" href="#([^"]+)"', page(b).group(0)).group(1)
        assert na == b and bb == a, (a, b, na, bb)

CSS = '''/* 3.11 Contrast fixes (axe-core check) */
#app #cover .cv-q{background:#fff!important;border-color:#fff!important;color:#0e4f86!important}
#app #cover .cv-q:active{background:#eaf2fb!important}
#app .nav-start,#app .screen:has(.ans-yes:checked) .go-yes{background:#00703c!important;border-color:#00703c!important}
#app .screen:has(#c1 .ans-yes:checked):has(#c2 .ans-yes:checked):has(#c3 .ans-yes:checked):has(#c4 .ans-yes:checked) #sum .go-yes{background:#00703c!important;border-color:#00703c!important}
@media (prefers-color-scheme:light){#app :is(#s5-2,#s5-gmdp) a small{color:#0e4f86!important}}
@media (prefers-color-scheme:dark){
  #app #nhs .exc-n .exc-h{color:#8cc4ff!important}
  #app #nhs .exc-a .exc-h{color:#ff9ab8!important}
  #app :is(#s4,#s4-reasons) .tc-t .tc-w b{color:#8cc4ff!important}
}
/* 3.11 Accessibility statement and Your privacy */
#app .screen .st-p{margin:0 0 10px;font-size:17px;line-height:1.42;color:var(--ink)}
#app .screen .st-small{color:var(--sub);margin-top:10px}
#app .screen .st-h{margin:14px 0 6px!important}
#app .screen .st-h:first-of-type{margin-top:0!important}
#app .screen .st-list{list-style:none;margin:0 0 4px;padding:0;border:1px solid var(--line);border-radius:14px;background:var(--surface)}
#app .screen .st-list li{display:flex;align-items:flex-start;gap:10px;margin:0;padding:7px 12px;font-size:17px;line-height:1.35;color:var(--ink)}
#app .screen .st-list li+li{border-top:1px solid var(--line)}
#app .screen .st-list li>span:first-child{flex:0 0 22px;height:22px;margin-top:1px;border-radius:50%;background:#e3f2ea;color:#00703c;display:flex;align-items:center;justify-content:center}
#app .screen .st-dots li>span:first-child{background:var(--accentSoft);color:var(--accent2)}
#app .screen .st-lead{display:flex;align-items:center;gap:10px;margin:0 0 12px;padding:10px 12px;border-radius:14px;background:#e8f5ee;color:#0b4f2c;font:700 17px/1.35 var(--font-body)}
#app .screen .st-lead>span{flex:0 0 28px;height:28px;border-radius:50%;background:#00703c;color:#fff;display:flex;align-items:center;justify-content:center}
#app .screen .st-mail{display:block;margin:0 0 10px;padding:10px 14px;border-radius:14px;background:var(--accentSoft);border:1.5px solid var(--accent);color:var(--accent2);font-weight:700;font-size:17px;line-height:1.3;text-decoration:none;overflow-wrap:anywhere}
#app #a11y .st-go{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:14px;min-height:48px;padding:0 14px;border-radius:14px;border:1px solid var(--line);background:var(--surface);color:var(--accent2);font-weight:700;font-size:17px;text-decoration:none}
@media (prefers-color-scheme:dark){#app .screen .st-lead{background:#12301f;color:#cfeedd}#app .screen .st-list li>span:first-child{background:#12301f;color:#9ee0b8}#app .screen .st-dots li>span:first-child{background:#16314f;color:#8cc4ff}}
@media (prefers-color-scheme:light){#app .screen :is(.st-list,.st-go){box-shadow:0 1px 2px rgba(16,40,70,.04),0 3px 10px rgba(16,40,70,.05)}}
@media screen and (max-height:700px){#app .screen .st-list li{padding:5px 12px}#app .screen .st-p{margin-bottom:8px;line-height:1.36}#app .screen .st-h{margin-top:10px!important}}
@media screen and (max-width:369px){#app .screen .st-list li{padding:4px 10px;line-height:1.3}#app .screen .st-p{line-height:1.32;margin-bottom:7px}#app .screen .st-h{margin-top:8px!important}}
@media screen and (max-height:600px){#app .screen .st-list li{padding:3px 10px;line-height:1.3}#app .screen .st-p{margin-bottom:6px;line-height:1.32}#app .screen .st-lead{padding:7px 10px;margin-bottom:8px}#app .screen .st-small{margin-top:6px}}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

n = s.count('<label class="nav-btn nav-next go-wait off" for='); assert n >= 4, n
s = s.replace('<label class="nav-btn nav-next go-wait off" for=', '<label class="nav-btn nav-next go-wait off" aria-disabled="true" for=')
rep('Carer role v3.10', 'Carer role v3.11'); rep('Version 3.10 iPhone', 'Version 3.11 iPhone')
rep('<div>Version 3.10</div>', '<div>Version 3.11</div>'); rep('>3.10 – REVIEW DRAFT', '>3.11 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">3\.08</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.10</span>', '<div class="rr"><span class="rv">3.11</span><span class="rd">20 Nov 2026</span><p>Accessibility statement, Your privacy, contrast fixes</p></div>\n<div class="rr"><span class="rv">3.10</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
