"""Guide 2.98 (from 2.97). David, 19 Nov: remove Section 2 · Your Health Visiting team, page 2 of 2,
"Confirm your details" (hv-confirm) - that is being done somewhere else. Section 2 is now one page.
usage: python3 make298.py v2.97.html v2.98.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>\n?' % re.escape(pid), s, re.S); assert m, pid; return m
def edit(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
m = page('hv-confirm'); s = s[:m.start()] + s[m.end():]
edit('hv', 'class="nav-btn nav-next" href="#hv-confirm"', 'class="nav-btn nav-next" href="#acct"')
edit('acct', 'class="nav-btn nav-back" href="#hv-confirm"', 'class="nav-btn nav-back" href="#hv"')
assert 'href="#hv-confirm"' not in s and 'id="hv-confirm"' not in s
order = [m.group(1) for m in re.finditer(r'<section class="screen(?: cover)?" id="([^"]+)"', s)]
order = [p for p in order if p != 'search']
total = len(order); assert total == 69, total
secs = {}
for pid in order:
    ds = re.search(r'data-sec="([^"]*)"', page(pid).group(0))
    secs.setdefault(ds.group(1) if ds else 'Welcome', []).append(pid)
for kk, pids in secs.items():
    for i, pid in enumerate(pids):
        pos = re.findall(r'<span class="pos">Page \d+ of \d+</span>', page(pid).group(0))
        if pos: edit(pid, pos[0], '<span class="pos">Page %d of %d</span>' % (i + 1, len(pids)))
for n2, pid in enumerate(order, 1):
    blk2 = page(pid).group(0)
    c2 = re.findall(r'<span class="count">\d+ / \d+</span>', blk2); assert len(c2) == 1, pid
    edit(pid, c2[0], '<span class="count">%d / %d</span>' % (n2, total))
    a2 = re.findall(r'aria-label="Contents \(page \d+ of \d+\)"', blk2)
    if a2: edit(pid, a2[0], 'aria-label="Contents (page %d of %d)"' % (n2, total))
for a, b in zip(order[3:], order[4:]):
    assert re.search(r'class="nav-btn nav-next[^"]*" href="#%s"' % b, page(a).group(0)), ('next', a, b)
    assert re.search(r'class="nav-btn nav-back" href="#%s"' % a, page(b).group(0)), ('back', b, a)
print({k: len(v) for k, v in secs.items()})
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'
rep('Carer role v2.97', 'Carer role v2.98'); rep('Version 2.97 iPhone', 'Version 2.98 iPhone')
rep('<div>Version 2.97</div>', '<div>Version 2.98</div>'); rep('>2.97 – REVIEW DRAFT', '>2.98 – REVIEW DRAFT')
rep('<p>New Home Screen icon: ABC blocks with a GUIDE label</p>', '<p>Home Screen icon trial (ABC blocks with a GUIDE label)</p>')
old = re.search(r'<div class="rr"><span class="rv">2\.95</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.97</span>', '<div class="rr"><span class="rv">2.98</span><span class="rd">19 Nov 2026</span><p>Removed “Confirm your details” (Section 2 page 2)</p></div>\n<div class="rr"><span class="rv">2.97</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
