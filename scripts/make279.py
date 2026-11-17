"""Guide 2.79 (from 2.78) (David, 17 Nov):
1. NHS login account issues list: "How to sign in to NHS login" moves from item 8 to item 2 and is renamed
   "Check your NHS account details" (list row, page title). The page and its Steps A-H (16 pages) move to
   follow Set up NHS login, so Next and Back follow the list order.
2. Steps B-H screenshots now work like Section 3 Signing in: 248 points wide and centred, cropped from the
   relevant part of the screen to the highlighted area, with "Tap to enlarge" underneath. Title boxes keep the
   NHS login blue band design.
usage: python3 make279.py v2.78.html v2.79.html
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
NEW = 'Check your NHS account details'
# 1a. list: item 8 -> item 2, renamed
nhs = page('s4-nhs').group(0)
row = re.search(r'\n?<a class="toc-row" href="#s4-signin"><span class="gb">8</span><span class="tt">How to sign in to NHS login</span>(<svg.*?</svg>)</a>', nhs, re.S)
assert row
edit('s4-nhs', row.group(0), '')
for old, new in (('s4-name', 7, 8), ('s4-mobile', 6, 7), ('s4-email', 5, 6), ('s4-code', 4, 5), ('s4-pw', 3, 4), ('s4-cannot', 2, 3)) if False else ():
    pass
for pid, n in (('s4-name', 7), ('s4-mobile', 6), ('s4-email', 5), ('s4-code', 4), ('s4-pw', 3), ('s4-cannot', 2)):
    edit('s4-nhs', '<a class="toc-row" href="#%s"><span class="gb">%d</span>' % (pid, n), '<a class="toc-row" href="#%s"><span class="gb">%d</span>' % (pid, n + 1))
edit('s4-nhs', '<a class="toc-row" href="#s4-cannot">',
     '<a class="toc-row" href="#s4-signin"><span class="gb">2</span><span class="tt">%s</span>%s</a>\n<a class="toc-row" href="#s4-cannot">' % (NEW, row.group(1)))
rows = re.findall(r'href="#([^"]+)"><span class="gb">(\d)</span><span class="tt">([^<]*)', page('s4-nhs').group(0))
assert [r[1] for r in rows] == [str(i) for i in range(1, 9)] and rows[1][0] == 's4-signin', rows
# 1b. rename the page
edit('s4-signin', 'data-title="How to sign in to NHS login"', 'data-title="%s"' % NEW)
edit('s4-signin', '<h2 class="h2" tabindex="-1">How to sign in to your NHS login account</h2>', '<h2 class="h2" tabindex="-1">%s</h2>' % NEW)
al = re.search(r'id="s4-signin"[^>]*aria-label="([^"]*)"', s)
if al and 'sign in' in al.group(1).lower():
    edit('s4-signin', 'aria-label="%s"' % al.group(1), 'aria-label="%s"' % NEW)
# 1c. move s4-signin .. step-h-tip to follow s4-setup
block_ids = ['s4-signin', 'step-a', 'step-b', 'step-b-tip', 'step-c', 'step-c-tip', 'step-d', 'step-d-tip', 'step-e', 'step-e-tip',
             'step-f', 'step-f-tip', 'step-g', 'step-g-tip', 'step-h', 'step-h-tip']
a = page('s4-signin').start(); e = page('step-h-tip').end()
block = s[a:e]
assert [m.group(1) for m in re.finditer(r'<section class="screen" id="([^"]+)"', block)] == block_ids
s = s[:a] + s[e:].lstrip('\n')
k = page('s4-setup').end()
s = s[:k] + '\n' + block + s[k:]
edit('s4-setup', 'class="nav-btn nav-next" href="#s4-cannot"', 'class="nav-btn nav-next" href="#s4-signin"')
edit('s4-signin', 'class="nav-btn nav-back" href="#s4-name"', 'class="nav-btn nav-back" href="#s4-setup"')
edit('step-h-tip', 'class="nav-btn nav-next" href="#s4-activation"', 'class="nav-btn nav-next" href="#s4-cannot"')
edit('s4-cannot', 'class="nav-btn nav-back" href="#s4-setup"', 'class="nav-btn nav-back" href="#step-h-tip"')
edit('s4-name', 'class="nav-btn nav-next" href="#s4-signin"', 'class="nav-btn nav-next" href="#s4-activation"')
edit('s4-activation', 'class="nav-btn nav-back" href="#step-h-tip"', 'class="nav-btn nav-back" href="#s4-name"')
# 2. screenshots like Section 3 (coordinates in the 520-wide space; image height 1126)
CROP = {'step-b': (240, 245, 700, 700), 'step-c': (400, 400, 810, 810), 'step-d': (285, 285, 640, 640), 'step-e': (0, 0, 200, 330),
        'step-f': (300, 690, 905, 905), 'step-g': (285, 285, 640, 640), 'step-h': (405, 405, 800, 800)}
for pid, (y, et, eb, pb) in CROP.items():
    m = re.search(r'style="--cw:520;--ch:\d+;--fw:520;--x:0;--y:\d+"', page(pid).group(0)); assert m, pid
    edit(pid, m.group(0), 'style="--cw:520;--ch:%d;--fw:520;--x:0;--y:%d;--et:%d;--eb:%d;--pb:%d;--ih:1126"' % (eb - y, y, et, eb, pb))
S3 = re.search(r'\.screen\[data-sec\^="Section 3"\] \.zt:not\(:checked\)\+\.shot\{--mh.*?\.screen\[data-sec\^="Section 3"\] \.zt:not\(:checked\)\+\.shot \.zoom\{[^}]*\}', s, re.S).group(0)
SEL = '.screen:is(#step-b,#step-c,#step-d,#step-e,#step-f,#step-g,#step-h)'
CSS = ('/* 2.79 Check your NHS account details, Steps B-H: screenshots like Section 3 (248 points wide, cropped to the highlighted area, Tap to enlarge underneath) */\n'
       + SEL + ' .crop{width:min(248px, calc(var(--maxh) * var(--cw) / var(--ch)))}\n' + S3.replace('.screen[data-sec^="Section 3"]', SEL) + '\n')
rep('@media print{', CSS + '@media print{')
# 3. renumber every page
order = [m.group(1) for m in re.finditer(r'<section class="screen(?: cover)?" id="([^"]+)"', s)]
order = [p for p in order if p != 'search']
total = len(order); assert total == 71, total
secs = {}
for pid in order:
    ds = re.search(r'data-sec="([^"]*)"', page(pid).group(0))
    secs.setdefault(ds.group(1) if ds else 'Welcome', []).append(pid)
for kk, pids in secs.items():
    for i, pid in enumerate(pids):
        pos = re.findall(r'<span class="pos">Page \d+ of \d+</span>', page(pid).group(0))
        if pos: edit(pid, pos[0], '<span class="pos">Page %d of %d</span>' % (i + 1, len(pids)))
for n, pid in enumerate(order, 1):
    blk = page(pid).group(0)
    c = re.findall(r'<span class="count">\d+ / \d+</span>', blk); assert len(c) == 1, pid
    edit(pid, c[0], '<span class="count">%d / %d</span>' % (n, total))
    a2 = re.findall(r'aria-label="Contents \(page \d+ of \d+\)"', blk)
    if a2: edit(pid, a2[0], 'aria-label="Contents (page %d of %d)"' % (n, total))
assert 'Page 4 of 32' in page('s4-signin').group(0) and 'Page 20 of 32' in page('s4-cannot').group(0)
# 4. version
rep('Carer role v2.78', 'Carer role v2.79'); rep('Version 2.78 iPhone', 'Version 2.79 iPhone')
rep('<div>Version 2.78</div>', '<div>Version 2.79</div>'); rep('>2.78 – REVIEW DRAFT', '>2.79 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.76</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.78</span>', '<div class="rr"><span class="rv">2.79</span><span class="rd">17 Nov 2026</span><p>Check your NHS account details is item 2 on the NHS login list; its screenshots match Signing in</p></div>\n<div class="rr"><span class="rv">2.78</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
