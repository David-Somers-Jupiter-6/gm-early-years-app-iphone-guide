"""Guide 2.90 (from 2.89). David, 18 Nov:
 1. Section 3 page 2 (Step 1) title "Signing in to NHS login" (was "Go to NHS login"). "NHS login" with a
    lower-case l, as NHS writes it and as the rest of the guide does.
 2. Section 3 pages 3 and 4 deleted (Step 2 "Sign-in page opens" and its note). The NHS login steps are now
    1-7: band labels, progress bars, hidden step text, Search titles, the hidden numbers and the
    "continue at Step 7" reference (now Step 6) all renumbered. Section 3 is 14 pages; the guide is 69 pages.
usage: python3 make290.py v2.89.html v2.90.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('<h2 tabindex="-1"><span class="vh">Step 1 of 8: </span>Go to NHS login</h2>', '<h2 tabindex="-1"><span class="vh">Step 1 of 8: </span>Signing in to NHS login</h2>')
rep('data-title="Step 1 · Go to NHS login"', 'data-title="Step 1 · Signing in to NHS login"')
def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>' % re.escape(pid), s, re.S); assert m, pid; return m
def edit(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
# 2. delete Step 2 and its note; Step 1 leads to the old Step 3
for pid in ('step-b', 'step-b-tip'):
    m = page(pid); s = s[:m.start()] + s[m.end():].lstrip('\n')
edit('step-a', 'class="nav-btn nav-next" href="#step-b"', 'class="nav-btn nav-next" href="#step-c"')
edit('step-c', 'class="nav-btn nav-back" href="#step-b-tip"', 'class="nav-btn nav-back" href="#step-a"')
rep('#app .screen:is(#step-a,#step-b,#step-b-tip,#step-c', '#app .screen:is(#step-a,#step-c', 5)
s = s.replace(':is(#step-b,#step-c', ':is(#step-c')   # shared screenshot styles
assert not re.search(r'(id="|href="#)step-b\b', s)   # (old standalone #step-b style rules remain; they match nothing)
# renumber the remaining NHS login steps (old 3-8 -> 2-7, "of 8" -> "of 7")
STEPS = ['step-a', 'step-c', 'step-c-tip', 'step-d', 'step-d-tip', 'step-e', 'step-e-tip', 'step-f', 'step-f-tip', 'step-g', 'step-g-tip', 'step-h', 'step-h-tip']
def shift(n): return n - 1 if n >= 3 else n
for pid in STEPS:
    m = page(pid); blk = m.group(0)
    blk = re.sub(r'Step (\d+) of 8', lambda mm: 'Step %d of 7' % shift(int(mm.group(1))), blk)
    blk = re.sub(r'\bStep (\d+)\b(?! of)', lambda mm: 'Step %d' % shift(int(mm.group(1))), blk)
    blk = re.sub(r'<span class="tp-n" aria-hidden="true">(\d+)</span>', lambda mm: '<span class="tp-n" aria-hidden="true">%d</span>' % shift(int(mm.group(1))), blk)
    k = int(re.search(r'Step (\d+) of 7', blk).group(1))
    st = re.search(r'<div class="stepper nhs-steps" aria-hidden="true">.*?</div>', blk).group(0)
    new = '<div class="stepper nhs-steps" aria-hidden="true">' + ''.join(
        '<span class="d">✓</span>' if i < k else ('<span class="c">%d</span>' % i if i == k else '<span class="">%d</span>' % i) for i in range(1, 8)) + '</div>'
    blk = blk.replace(st, new)
    s = s[:m.start()] + blk + s[m.end():]
assert 'continue at <a href="#step-g">Step 6</a>' in page('step-d-tip').group(0), 'Step 4 note reference'
assert not re.search(r'Step \d of 8', s)

# renumber every page
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
print('Section 3 pages:', len(secs['Section 3 · NHS login']))

rep('Carer role v2.89', 'Carer role v2.90'); rep('Version 2.89 iPhone', 'Version 2.90 iPhone')
rep('<div>Version 2.89</div>', '<div>Version 2.90</div>'); rep('>2.89 – REVIEW DRAFT', '>2.90 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.87</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.89</span>', '<div class="rr"><span class="rv">2.90</span><span class="rd">18 Nov 2026</span><p>NHS login: Step 1 retitled Signing in to NHS login; Sign-in page step removed (7 steps)</p></div>\n<div class="rr"><span class="rv">2.89</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
