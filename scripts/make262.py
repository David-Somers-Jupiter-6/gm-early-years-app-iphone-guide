"""Guide 2.62 (from 2.61).
- Troubleshooting, NHS login account issues (s4-nhs): new first item "Set up NHS login",
  the other seven renumbered 2 to 8.
- NHS login account issues: "GMDP Support cannot assist with NHS login account issues." under the
  section strip, then the list ("Choose your problem..." and the bottom GMDP line removed) (David).
- New page s4-setup "Set up NHS login" (Troubleshooting page 3 of 34), between s4-nhs and
  s4-cannot, laid out like the other NHS login help pages: what the link covers, the
  NHS login link, and "GMDP Support cannot access NHS login accounts." at the bottom.
- Page numbers: Troubleshooting is now 34 pages; the guide is 73 pages (plus Search).
usage: python3 make262.py v2.61.html v2.62.html
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

# ---------------------------------------------------------------- list on NHS login account issues
nhs = page('s4-nhs').group(0)
rows = re.findall(r'<a class="toc-row" href="#[^"]+"><span class="gb">\d</span>', nhs)
assert len(rows) == 7
chev = re.search(r'<a class="toc-row" href="#s4-cannot"><span class="gb">1</span><span class="tt">Cannot sign in</span>(<svg.*?</svg>)</a>', nhs, re.S).group(1)
for i in range(7, 0, -1):
    edit('s4-nhs', '<span class="gb">%d</span>' % i, '<span class="gb">%d</span>' % (i + 1))
edit('s4-nhs', '<a class="toc-row" href="#s4-cannot">',
     '<a class="toc-row" href="#s4-setup"><span class="gb">1</span><span class="tt">Set up NHS login</span>%s</a>\n<a class="toc-row" href="#s4-cannot">' % chev)

# GMDP line moves to the top of the list page, in place of "Choose your problem..." (David)
edit('s4-nhs', '<p class="lead">Choose your problem to find NHS login help:</p>',
     '<p class="info-lead">GMDP Support cannot assist with NHS login account issues.</p>')
edit('s4-nhs', '<p class="ts-small">GMDP Support cannot access NHS login accounts.</p>\n', '')

# ---------------------------------------------------------------- new page, built from s4-cannot's parts
can = page('s4-cannot').group(0)
link_svg = re.search(r'<a class="sp-link" href="https://help.login.nhs.uk" rel="noopener" target="_blank">(<svg.*?</svg>)', can, re.S).group(1)
bnav = re.search(r'<nav class="bnav".*?</nav>', can, re.S).group(0)
new_nav = (bnav.replace('href="#s4-nhs"', 'href="#s4-setup-BACK"')       # placeholders, fixed below
               .replace('href="#s4-pw"', 'href="#s4-cannot"'))
new_nav = new_nav.replace('href="#s4-setup-BACK"', 'href="#s4-nhs"')
NEW = ('<section class="screen" id="s4-setup" data-sec="Section 4 · Troubleshooting" data-title="Set up NHS login" aria-label="Set up NHS login">\n'
 '<div class="scroll">\n'
 '<div class="pbox"><h2 class="h2" tabindex="-1">Set up NHS login</h2></div>\n'
 '<div class="strip" aria-hidden="true"><div class="strip-row"><span>Section 4 · Troubleshooting</span><span class="pos">Page 3 of 33</span></div></div>\n'
 '<p class="info-lead">The link below gives details on:</p>\n'
 '<ul class="facts setup-facts"><li>What is NHS login?</li><li>Where you can use NHS login</li><li>What you need to set up an NHS login</li><li>How to set up an NHS login</li></ul>\n'
 '<div class="hv-card sp-card"><h3 class="sp-h3">Get help from NHS login</h3>\n'
 '<a class="sp-link" href="https://help.login.nhs.uk/setupnhslogin" rel="noopener" target="_blank">%s<span><strong>Set up an NHS login account</strong><small>help.login.nhs.uk/<wbr>setupnhslogin</small></span></a>\n'
 '</div>\n'
 '<p class="ts-small">GMDP Support cannot access NHS login accounts.</p>\n'
 '</div>\n%s\n</section>\n') % (link_svg, new_nav)
m = page('s4-cannot'); s = s[:m.start()] + NEW + s[m.start():]

# links around the new page
nhs_nav = re.search(r'<nav class="bnav".*?</nav>', page('s4-nhs').group(0), re.S).group(0)
edit('s4-nhs', nhs_nav, nhs_nav.replace('class="nav-btn nav-next" href="#s4-cannot"', 'class="nav-btn nav-next" href="#s4-setup"'))
can_nav = re.search(r'<nav class="bnav".*?</nav>', page('s4-cannot').group(0), re.S).group(0)
edit('s4-cannot', can_nav, can_nav.replace('class="nav-btn nav-back" href="#s4-nhs"', 'class="nav-btn nav-back" href="#s4-setup"'))

# ---------------------------------------------------------------- renumber every page in order
order = [m.group(1) for m in re.finditer(r'<section class="screen(?: cover)?" id="([^"]+)"', s)]
order = [p for p in order if p != 'search']
total = len(order); assert total == 73, total
secs = {}
for pid in order:
    ds = re.search(r'data-sec="([^"]*)"', page(pid).group(0))
    secs.setdefault(ds.group(1) if ds else 'Welcome', []).append(pid)
for k, pids in secs.items():
    for i, pid in enumerate(pids):
        blk = page(pid).group(0)
        pos = re.findall(r'<span class="pos">Page \d+ of \d+</span>', blk)
        if pos:
            assert len(pos) == 1, pid
            edit(pid, pos[0], '<span class="pos">Page %d of %d</span>' % (i + 1, len(pids)))
for n, pid in enumerate(order, 1):
    blk = page(pid).group(0)
    c = re.findall(r'<span class="count">\d+ / \d+</span>', blk); assert len(c) == 1, pid
    edit(pid, c[0], '<span class="count">%d / %d</span>' % (n, total))
    a = re.findall(r'aria-label="Contents \(page \d+ of \d+\)"', blk)
    if a: edit(pid, a[0], 'aria-label="Contents (page %d of %d)"' % (n, total))
assert 'Page 3 of 34' in page('s4-setup').group(0) and 'Page 34 of 34' in page('s4-help').group(0)
assert '/ 72<' not in s and 'of 72)' not in s

# list bullets match the other lists
rep('@media print{', '#s4-setup .setup-facts{margin-bottom:14px}\n@media print{')

# ---------------------------------------------------------------- version
rep('Carer role v2.61', 'Carer role v2.62'); rep('Version 2.61 iPhone', 'Version 2.62 iPhone')
rep('<div>Version 2.61</div>', '<div>Version 2.62</div>'); rep('>2.61 – REVIEW DRAFT', '>2.62 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.59</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.61</span>', '<div class="rr"><span class="rv">2.62</span><span class="rd">16 Nov 2026</span><p>New Troubleshooting page: Set up NHS login</p></div>\n<div class="rr"><span class="rv">2.61</span>')
open(dst, 'w', encoding='utf-8').write(s)
print('written', dst, 'pages', total)
