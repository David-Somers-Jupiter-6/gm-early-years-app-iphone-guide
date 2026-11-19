"""Guide 3.05 (from 3.04). David, 19 Nov:
 - Troubleshooting menu (s4): "Activation Link issues" card becomes "GM Early Years App issues" (user icon, GM Early Years App
   colours for the tile and the left highlight, short line "For issues with access to the app") -> new page s4-gm
 - New page s4-gm "GM Early Years App issues" (Section 6, after s4-name, before s4-activation): app title box with a round
   white user icon (like the GMDP headset icon), lead "For issues with access to the GM Early Years App.", and an icon list
   in the NHS login account issues style but in app colours. First (only) item: Activation Link issues -> s4-activation.
 - Back/Next chain, "Page N of 30" in Troubleshooting, and Contents counters "N / 70" updated.
usage: python3 make305.py v3.04.html v3.05.html"""
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

CHEV = '<span class="tc-c"><svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M7.5 4.5L13 10l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
USER_O = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 20c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>'
USER_F = '<svg viewBox="0 0 24 24" width="22" height="22"><circle cx="12" cy="8" r="4" fill="currentColor"/><path d="M4 20.5c.7-4.2 4-6.6 8-6.6s7.3 2.4 8 6.6z" fill="currentColor"/></svg>'
LINK = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 14a4.5 4.5 0 006.4 0l3-3a4.5 4.5 0 00-6.4-6.4l-1.2 1.2"/><path d="M14 10a4.5 4.5 0 00-6.4 0l-3 3a4.5 4.5 0 006.4 6.4l1.2-1.2"/></svg>'

# 1. Troubleshooting menu card
old_card = re.search(r'<a class="tc tc-hv" href="#s4-activation">.*?</a>', page('s4').group(0), re.S).group(0)
in_page('s4', old_card, '<a class="tc tc-app" href="#s4-gm"><span class="tc-tile">' + USER_O + '</span><span class="tc-t"><b>GM Early Years App issues</b>'
        '<span class="tc-s">For issues with access to the app</span></span>' + CHEV + '</a>')

# 2. New page s4-gm (copy s4-name's frame for strip + nav, then rebuild)
NEW = ('<section class="screen" id="s4-gm" data-sec="Section 6 · Troubleshooting" data-title="GM Early Years App issues" aria-label="GM Early Years App issues">\n'
       '<div class="scroll">\n'
       '<div class="pbox gm-icon"><span class="gm-eyi" aria-hidden="true">' + USER_F + '</span><h2 class="h2" tabindex="-1">GM Early Years App issues</h2></div>\n'
       '<div class="strip" aria-hidden="true"><div class="strip-row"><span>Section 6 · Troubleshooting</span><span class="pos">Page X of 30</span></div></div>\n'
       '<p class="info-lead">For issues with access to the GM Early Years App.</p>\n'
       '<nav aria-label="GM Early Years App issues" class="tr-list"><a class="tr" href="#s4-activation"><span class="tr-i">' + LINK + '</span>'
       '<span class="tr-t">Activation Link issues</span>' + CHEV + '</a></nav>\n'
       '</div>\n')
nav = re.search(r'<nav class="bnav".*?</nav>\n</section>', page('s4-activation').group(0), re.S).group(0)
nav = nav.replace('href="#s4-name"', 'href="#s4-name"').replace('href="#s4-activation-2"', 'href="#s4-activation"')
NEW += nav
in_page('s4-activation', '<a class="nav-btn nav-back" href="#s4-name">', '<a class="nav-btn nav-back" href="#s4-gm">')
in_page('s4-name', '<a class="nav-btn nav-next" href="#s4-activation">', '<a class="nav-btn nav-next" href="#s4-gm">')
m = page('s4-activation'); s = s[:m.start()] + NEW + '\n' + s[m.start():]

# 3. Page numbers: Troubleshooting "Page N of 30", Contents counters "N / 70"
ids = re.findall(r'<section class="screen(?: cover)?" id="([^"]+)"', s)
tr = [i for i in ids if 'data-sec="Section 6 · Troubleshooting"' in page(i).group(0)[:300]]
assert len(tr) == 30 and tr[tr.index('s4-name') + 1] == 's4-gm' and tr[tr.index('s4-gm') + 1] == 's4-activation', tr
for n, pid in enumerate(tr, 1):
    blk = page(pid).group(0); new = re.sub(r'<span class="pos">Page (?:\d+|X) of 29</span>|<span class="pos">Page X of 30</span>', f'<span class="pos">Page {n} of 30</span>', blk, count=1)
    assert new != blk, pid; m = page(pid); s = s[:m.start()] + new + s[m.end():]
cnt = 0
for idx, pid in enumerate(ids, 1):
    blk = page(pid).group(0)
    new = re.sub(r'\(page \d+ of 69\)', f'(page {idx} of 70)', blk)
    new = re.sub(r'<span class="count">\d+ / 69</span>', f'<span class="count">{idx} / 70</span>', new)
    if new != blk: m = page(pid); s = s[:m.start()] + new + s[m.end():]; cnt += 1
assert not re.search(r'of 69\)|/ 69</span>', s); print('counters', cnt)
# Back/Next chain sanity across the whole guide
for a, b in zip(ids, ids[1:]):
    na = re.search(r'class="nav-btn nav-next" href="#([^"]+)"', page(a).group(0))
    bb = re.search(r'class="nav-btn nav-back" href="#([^"]+)"', page(b).group(0))
    if a in ('s4-name', 's4-gm'): assert na.group(1) == b and bb.group(1) == a, (a, b)

# 4. CSS: s4-gm list uses the s4-nhs list rules; app colours; the new card like the GMDP card
css_start = s.find('<style'); css_end = s.find('</style>', css_start); css = s[css_start:css_end]
def widen(mt):
    sel, body = mt.group(1), mt.group(2)
    if '#s4-nhs' in sel and re.search(r'\.tr\b|\.tr-|\.tc-c|\.info-lead', sel):
        sel = sel.replace('#s4-nhs', ':is(#s4-nhs,#s4-gm)')
    return sel + '{' + body + '}'
css2 = re.sub(r'([^{}]+)\{([^{}]*)\}', widen, css)
print('widened rules', css2.count(':is(#s4-nhs,#s4-gm)'))
s = s[:css_start] + css2 + s[css_end:]
CSS = '''/* 3.05 GM Early Years App issues: Troubleshooting card + menu page in the app colours */
#app #s4 .tc-app{border-left-color:#c0174e}
#app #s4 .tc-app .tc-tile{background:linear-gradient(135deg,#6c155c,#d01545)}
#app #s4 .tc-app .tc-s{display:block!important}
#app #s4-gm .tr-i{background:#fbe7ee;color:#a3124d}
#app #s4-gm .tr-list{box-shadow:0 1px 2px rgba(163,18,77,.10)}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

# version
rep('Carer role v3.04', 'Carer role v3.05'); rep('Version 3.04 iPhone', 'Version 3.05 iPhone')
rep('<div>Version 3.04</div>', '<div>Version 3.05</div>'); rep('>3.04 – REVIEW DRAFT', '>3.05 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">3\.02</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.04</span>', '<div class="rr"><span class="rv">3.05</span><span class="rd">19 Nov 2026</span><p>Troubleshooting: GM Early Years App issues page (Activation Link issues moved inside)</p></div>\n<div class="rr"><span class="rv">3.04</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
