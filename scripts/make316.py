"""Guide 3.16 (from 3.15) – LIVE. David, 21 Nov: in Troubleshooting > GM Early Years App issues, list
Activation Link issues first, How to install the App second, Add to Home Screen third.
 - Menu rows reordered on s4-gm.
 - The two Activation Link issues pages (s4-activation, s4-activation-2) move to just after the menu, so the
   "Page N of 41" and "N / 86" counters follow the menu order. Navigation is unchanged (each topic still ends
   with Done back to the menu).
usage: python3 make316.py v3.15.html v3.16.html"""
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

# 1. menu rows
m = page('s4-gm'); blk = m.group(0)
rows = re.findall(r'<a class="tr" href="#[^"]+">.*?</a>(?=<a class="tr"|</nav>)', blk, re.S)
assert [re.search(r'href="#([^"]+)"', r).group(1) for r in rows] == ['inst', 'a2hs', 's4-activation'], rows
blk = blk.replace(''.join(rows), rows[2] + rows[0] + rows[1]); assert blk != m.group(0)
put('s4-gm', blk)

# 2. move the Activation Link issues pages to just after the menu
act = page('s4-activation').group(0) + page('s4-activation-2').group(0)
for pid in ('s4-activation', 's4-activation-2'):
    put(pid, '')
m = page('s4-gm'); s = s[:m.end()] + act + s[m.end():]

# 3. counters by position
ids = re.findall(r'<section class="screen(?: cover)?" id="([^"]+)"', s)
assert ids[-1] == 'search'; T = len(ids) - 1; assert T == 86, T
sec6 = [i for i in ids if 'data-sec="Section 6 · Troubleshooting"' in page(i).group(0)[:300]]
assert len(sec6) == 41, len(sec6)
assert sec6[sec6.index('s4-gm'):sec6.index('s4-gm') + 4] == ['s4-gm', 's4-activation', 's4-activation-2', 'inst'], sec6
for n, pid in enumerate(sec6, 1):
    blk = page(pid).group(0)
    new = re.sub(r'<span class="pos">Page \d+ of 41</span>', f'<span class="pos">Page {n} of 41</span>', blk, count=1)
    assert 'Page %d of 41' % n in new, pid; put(pid, new)
for idx, pid in enumerate(ids, 1):
    blk = page(pid).group(0)
    new = re.sub(r'\(page \d+ of \d+\)', f'(page {idx} of {T})', blk)
    new = re.sub(r'<span class="count">\d+ / \d+</span>', f'<span class="count">{idx} / {T}</span>', new)
    if new != blk: put(pid, new)

rep('Carer role v3.15', 'Carer role v3.16'); rep('Version 3.15 iPhone', 'Version 3.16 iPhone')
rep('>3.15 – REVIEW DRAFT', '>3.16 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.15</span>', '<span class="cv-ver">Version 3.16</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.13</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.15</span>', '<div class="rr"><span class="rv">3.16</span><span class="rd">21 Nov 2026</span><p>GM Early Years App issues: Activation Link issues listed first</p></div>\n<div class="rr"><span class="rv">3.15</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
