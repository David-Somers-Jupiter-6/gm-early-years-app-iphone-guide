"""Guide 2.77 (from 2.76) (David, 17 Nov):
- Troubleshooting page 11 of 34 "When you can sign in to NHS login" (s4-cannot-4) deleted. My name has changed
  now goes straight to How to sign in to NHS login.
- "Change your password" (s4-pwchange, list item 6) deleted: you can only change your password once signed in
  (NHS login Help: settings > change password, enter your current password), so it is not a sign-in problem;
  forgotten passwords are covered by item 3. Cannot get into your email now goes straight to Mobile number problems.
- How to sign in to NHS login (s4-signin) is the new item 8 on the NHS login account issues list (s4-nhs), so the
  list stays at eight items and still fits; its band reads "NHS login | Account issues" like the others on the list.
- Page numbers: Troubleshooting is now 32 pages; the guide is 71 pages (plus Search).
usage: python3 make277.py v2.76.html v2.77.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>' % re.escape(pid), s, re.S)
    assert m, pid
    return m
def edit(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
# 1. delete s4-cannot-4 and join its neighbours
m = page('s4-cannot-4'); s = s[:m.start()] + s[m.end():].lstrip('\n')
assert 'id="s4-cannot-4"' not in s
edit('s4-name', 'class="nav-btn nav-next" href="#s4-cannot-4"', 'class="nav-btn nav-next" href="#s4-signin"')
edit('s4-signin', 'class="nav-btn nav-back" href="#s4-cannot-4"', 'class="nav-btn nav-back" href="#s4-name"')
assert '#s4-cannot-4' not in s
# 2. delete Change your password; How to sign in to NHS login becomes item 8
m = page('s4-pwchange'); s = s[:m.start()] + s[m.end():].lstrip('\n')
edit('s4-email', 'class="nav-btn nav-next" href="#s4-pwchange"', 'class="nav-btn nav-next" href="#s4-mobile"')
edit('s4-mobile', 'class="nav-btn nav-back" href="#s4-pwchange"', 'class="nav-btn nav-back" href="#s4-email"')
nhs = page('s4-nhs').group(0)
row6 = re.search(r'<a class="toc-row" href="#s4-pwchange"><span class="gb">6</span>.*?</a>\n?', nhs, re.S)
assert row6
edit('s4-nhs', row6.group(0), '')
edit('s4-nhs', '<a class="toc-row" href="#s4-mobile"><span class="gb">7</span>', '<a class="toc-row" href="#s4-mobile"><span class="gb">6</span>')
edit('s4-nhs', '<a class="toc-row" href="#s4-name"><span class="gb">8</span>', '<a class="toc-row" href="#s4-name"><span class="gb">7</span>')
nhs = page('s4-nhs').group(0)
row7 = re.search(r'<a class="toc-row" href="#s4-name"><span class="gb">7</span><span class="tt">My name has changed</span>(<svg.*?</svg>)</a>', nhs, re.S)
assert row7
edit('s4-nhs', row7.group(0), row7.group(0) + '\n<a class="toc-row" href="#s4-signin"><span class="gb">8</span><span class="tt">How to sign in to NHS login</span>%s</a>' % row7.group(1))
assert '#s4-pwchange' not in s and len(re.findall(r'class="toc-row"', page('s4-nhs').group(0))) == 8
edit('s4-signin', '<b>NHS login</b><span>Troubleshooting</span>', '<b>NHS login</b><span>Account issues</span>')
# 3. renumber every page
order = [m.group(1) for m in re.finditer(r'<section class="screen(?: cover)?" id="([^"]+)"', s)]
order = [p for p in order if p != 'search']
total = len(order); assert total == 71, total
secs = {}
for pid in order:
    ds = re.search(r'data-sec="([^"]*)"', page(pid).group(0))
    secs.setdefault(ds.group(1) if ds else 'Welcome', []).append(pid)
for k, pids in secs.items():
    for i, pid in enumerate(pids):
        pos = re.findall(r'<span class="pos">Page \d+ of \d+</span>', page(pid).group(0))
        if pos:
            assert len(pos) == 1, pid
            edit(pid, pos[0], '<span class="pos">Page %d of %d</span>' % (i + 1, len(pids)))
for n, pid in enumerate(order, 1):
    blk = page(pid).group(0)
    c = re.findall(r'<span class="count">\d+ / \d+</span>', blk); assert len(c) == 1, pid
    edit(pid, c[0], '<span class="count">%d / %d</span>' % (n, total))
    a = re.findall(r'aria-label="Contents \(page \d+ of \d+\)"', blk)
    if a: edit(pid, a[0], 'aria-label="Contents (page %d of %d)"' % (n, total))
assert 'Page 10 of 32' in page('s4-signin').group(0) and 'Page 32 of 32' in page('s4-help').group(0)
assert '/ 73<' not in s and 'of 73)' not in s and 'of 34<' not in s and 'of 33<' not in s
# 4. version
rep('Carer role v2.76', 'Carer role v2.77'); rep('Version 2.76 iPhone', 'Version 2.77 iPhone')
rep('<div>Version 2.76</div>', '<div>Version 2.77</div>'); rep('>2.76 – REVIEW DRAFT', '>2.77 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.74</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.76</span>', '<div class="rr"><span class="rv">2.77</span><span class="rd">17 Nov 2026</span><p>NHS login account issues list: Change your password removed, How to sign in to NHS login added; one Troubleshooting page removed</p></div>\n<div class="rr"><span class="rv">2.76</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, 'pages', total)
