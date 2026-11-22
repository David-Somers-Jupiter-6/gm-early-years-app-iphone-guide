"""Guide 3.33 (from live 3.32) – TRIAL. David, 22 Nov: in Troubleshooting,
 - rename "NHS login account issues" to "NHS login account help";
 - rename "GM Early Years App issues" to "GM Early Years App help";
 - merge "Common sign-in problems" into GM Early Years App help, keeping its card format (a title with a short
   explanation underneath). All six topics on the merged menu now use that format.
 - The Common sign-in problems page is removed; its three topics (Details do not match, Partner's details used,
   A partner is signing in) go Back / Done to GM Early Years App help. Section 6 now has 49 pages.
usage: python3 make333.py v3.32.html v3.33.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>\n?' % re.escape(pid), s, re.S)
    assert m, pid
    return m
def put(pid, new):
    global s
    m = page(pid); s = s[:m.start()] + new + s[m.end():]

NHS_OLD, NHS_NEW = 'NHS login account issues', 'NHS login account help'
GM_OLD, GM_NEW = 'GM Early Years App issues', 'GM Early Years App help'

# 1. Troubleshooting menu (s4): new names, remove the Common sign-in problems card
blk = page('s4').group(0)
blk = blk.replace('<b>%s</b>' % NHS_OLD, '<b>%s</b>' % NHS_NEW)
blk = blk.replace('<b>%s</b><span class="tc-s">For issues with access to the app</span>' % GM_OLD,
                  '<b>%s</b><span class="tc-s">Activation Link, installing, sign-in problems</span>' % GM_NEW)
blk, n = re.subn(r'<a class="tc tc-hv" href="#s4-reasons">.*?</a>(?=<a class="tc tc-gm")', '', blk, flags=re.S)
assert n == 1 and NHS_NEW in blk and GM_NEW in blk
put('s4', blk)

# 2. NHS login account help page
blk = page('s4-nhs').group(0)
for a in ['data-title="%s"', 'aria-label="%s">', '>%s</h2>', 'nav aria-label="%s"']:
    assert blk.count(a % NHS_OLD) == 1, a; blk = blk.replace(a % NHS_OLD, a % NHS_NEW)
put('s4-nhs', blk)
rep('See the other <a href="#s4-nhs">NHS login account issues</a>.', 'See <a href="#s4-nhs">NHS login account help</a>.')

# 3. GM Early Years App help: one card list with title + explanation for all six topics
blk = page('s4-gm').group(0)
for a in ['data-title="%s"', 'aria-label="%s">', '>%s</h2>', 'nav aria-label="%s"']:
    assert blk.count(a % GM_OLD) == 1, a; blk = blk.replace(a % GM_OLD, a % GM_NEW)
icons = dict(re.findall(r'<a class="tr" href="#([^"]+)"><span class="tr-i">(<svg.*?</svg>)</span>', blk, re.S))
chev = re.search(r'<span class="tc-c">(<svg.*?</svg>)</span>', blk, re.S).group(1)
reasons = page('s4-reasons').group(0)
hv_cards = re.search(r'<nav aria-label="Common reasons for sign-in problems" class="tc-list">(.*?)</nav>', reasons, re.S).group(1)
assert hv_cards.count('<a class="tc tc-hv"') == 3
app = [('s4-activation', 'Activation Link issues', 'Not arrived, or what to do with it'),
       ('inst', 'How to install the App', 'Get the App from the App Store'),
       ('a2hs', 'Add to Home Screen', 'Put this guide on your Home Screen')]
cards = ''.join('<a class="tc tc-app" href="#%s"><span class="tc-tile">%s</span><span class="tc-t"><b>%s</b>'
                '<span class="tc-s">%s</span></span><span class="tc-c">%s</span></a>' % (h, icons[h], t, d, chev)
                for h, t, d in app)
blk, n = re.subn(r'<nav aria-label="%s" class="tr-list">.*?</nav>' % GM_NEW,
                 '<nav aria-label="%s" class="tc-list">%s%s</nav>' % (GM_NEW, cards, hv_cards), blk, flags=re.S)
assert n == 1
blk = blk.replace('<p class="info-lead">For issues with access to the GM Early Years App.</p>', '<p class="info-lead fit-opt">For issues with access to the GM Early Years App.</p>')
assert 'info-lead fit-opt' in blk
put('s4-gm', blk)
rep('<b>NHS login</b><span>Account issues</span>', '<b>NHS login</b><span>Account help</span>', 8)

# 4. Remove the Common sign-in problems page; its topics return to GM Early Years App help
m = page('s4-reasons'); s = s[:m.start()] + s[m.end():]
for pid in ('s4-problems', 's4-1b', 's4-2'):
    blk = page(pid).group(0)
    assert blk.count('href="#s4-reasons"') == 2, pid
    blk = blk.replace('href="#s4-reasons"', 'href="#s4-gm"')
    put(pid, blk)
assert 'href="#s4-reasons"' not in s

# 5. CSS: the card styles used by Common sign-in problems now apply to GM Early Years App help
css_end = s.index('</style>')
css = s[:css_end].replace(':is(#s4,#s4-reasons)', ':is(#s4,#s4-gm)')
css = css.replace('#app #s4 .tc-app{', '#app :is(#s4,#s4-gm) .tc-app{').replace('#app #s4 .tc-app .tc-tile{', '#app :is(#s4,#s4-gm) .tc-app .tc-tile{')
css = css.replace('#app #s4 .tc-app .tc-s{', '#app :is(#s4,#s4-gm) .tc-app .tc-s{')
s = css + s[css_end:]
NEW_CSS = """/* 3.33 GM Early Years App help: six topics as cards, each with a title and a short explanation */
#app #s4-gm .info-lead{margin:0 0 8px}
#app #s4-gm .tc{padding:7px 10px 7px 9px;gap:10px}
#app #s4-gm .tc-list .tc+.tc{margin-top:7px}
#app #s4-gm .tc-tile{flex-basis:40px;height:40px}
#app #s4-gm .tc-t>b{font-size:16px;line-height:1.22}
#app #s4-gm .tc-s{display:block!important;font-size:14.5px;line-height:1.25;margin-top:1px}
#app #s4-gm.tight .tc{padding-top:5px;padding-bottom:5px}
#app #s4-gm.tight .tc-list .tc+.tc{margin-top:5px}
#app #s4-gm.tight .tc-tile{flex-basis:36px;height:36px}
@media screen and (max-width:345px){#app #s4-gm .tc{gap:8px;padding-right:6px}#app #s4-gm .tc-tile{flex-basis:34px;height:34px}#app #s4-gm .tc-s{font-size:13.5px}#app #s4-gm .tc-t>b{font-size:15.5px}}
"""
anchor = '/* 2.88 Step 1:'
assert s.count(anchor) == 1; s = s.replace(anchor, NEW_CSS + anchor)
assert NEW_CSS.count('{') == NEW_CSS.count('}')

# 6. Section 6 page numbers (one page fewer)
def renum(mm):
    n = int(mm.group(1)); return '<span class="pos">Page %d of 49</span>' % (n - 1 if n > 46 else n)
s, k = re.subn(r'<span class="pos">Page (\d+) of 50</span>', renum, s); assert k >= 40, k

# 7. whole-guide counters by position
ids = re.findall(r'<section class="screen(?: cover)?" id="([^"]+)"', s)
assert ids[:4] == ['cover', 'intro', 'contents', 'how'] and ids[-1] == 'search'; T = len(ids) - 1
for idx, pid in enumerate(ids, 1):
    blk = page(pid).group(0)
    new = re.sub(r'\(page \d+ of \d+\)', f'(page {idx} of {T})', blk)
    new = re.sub(r'<span class="count">\d+ / \d+</span>', f'<span class="count">{idx} / {T}</span>', new)
    if new != blk: put(pid, new)

rep('Carer role v3.32', 'Carer role v3.33'); rep('Version 3.32 iPhone', 'Version 3.33 iPhone')
rep('>3.32 – REVIEW DRAFT', '>3.33 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.32</span>', '<span class="cv-ver">Version 3.33</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.28</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.32</span>', '<div class="rr"><span class="rv">3.33</span><span class="rd">22 Nov 2026</span><p>NHS login account help and GM Early Years App help; Common sign-in problems merged into GM Early Years App help</p></div>\n<div class="rr"><span class="rv">3.32</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, T)
