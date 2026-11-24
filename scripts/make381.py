"""Guide 3.81 (from 3.80) – text and UX review (24 Nov 2026), published live.
Runs the review patches in scripts/review381 (cover, welcome pages, Contact your HV team, Signing in, Support,
Contacts, Accessibility, About this guide), then recomputes page counters (Signing in 18 → 16 pages: the two
'Helpful tip' pages are folded into steps 12 and 13), bumps the version and adds a revision entry.
usage: python3 make381.py v3.80.html v3.81.html"""
import re, sys, os, subprocess, tempfile
src, dst = sys.argv[1], sys.argv[2]
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review381')
cur = src; tmp = tempfile.mkdtemp()
for k, (script, extra) in enumerate([('si.py', []), ('welcome.py', []), ('contacts.py', []), ('about.py', []), ('cover.py', ['A'])]):
    out = os.path.join(tmp, '%d.html' % k)
    subprocess.run([sys.executable, '-I', os.path.join(here, script), cur, out] + extra, check=True); cur = out
s = open(cur, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
SEC = re.compile(r'<section class="screen[^"]*" id="([^"]+)".*?</section>\n?', re.S)
def blocks(): return [(m.group(1), m.start(), m.end()) for m in SEC.finditer(s)]
def get(i):
    for k, a, b in blocks():
        if k == i: return a, b
    raise KeyError(i)
def edit(i, f):
    global s
    a, b = get(i); s = s[:a] + f(s[a:b]) + s[b:]
def section_of(i):
    a, b = get(i); m = re.search(r'data-sec="([^"]*)"', s[a:b]); return m.group(1) if m else ''
# page counters
pages = [k for k, a, b in blocks() if k != 'search']; T = len(pages); groups = {}
for k in pages: groups.setdefault(section_of(k), []).append(k)
for k in pages:
    g = groups[section_of(k)]; n = g.index(k) + 1; idx = pages.index(k) + 1
    def f(blk, n=n, m=len(g), idx=idx):
        blk = re.sub(r'<span class="pos">Page \d+ of \d+</span>', '<span class="pos">Page %d of %d</span>' % (n, m), blk)
        blk = re.sub(r'<span class="count">\d+ / \d+</span>', '<span class="count">%d / %d</span>' % (idx, T), blk)
        blk = re.sub(r'\(page \d+ of \d+\)', '(page %d of %d)' % (idx, T), blk)
        return blk
    edit(k, f)
rep('Large print, easy-read and other formats', 'Large print, easy read and other formats')
# version
rep('Carer role v3.80', 'Carer role v3.81'); rep('Version 3.80 iPhone', 'Version 3.81 iPhone')
rep('>3.80 – REVIEW DRAFT', '>3.81 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.80</span>', '<span class="cv-ver">Version 3.81</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.76</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.80</span>', '<div class="rr"><span class="rv">3.81</span><span class="rd">24 Nov 2026</span><p>Clearer wording throughout; Signing in tips folded into the steps</p></div>\n<div class="rr"><span class="rv">3.80</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, '| pages', T, '| sections', {k: len(v) for k, v in groups.items()})
