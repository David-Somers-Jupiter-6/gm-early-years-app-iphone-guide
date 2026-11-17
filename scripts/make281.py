"""Guide 2.81 (from 2.80). New section order (David, 17 Nov):
  1 How this guide works (was in About this guide)
  2 Signing in to NHS login (the NHS login sign-in pages, moved out of Troubleshooting completely)
  3 Your Health Visiting team   4 Checklist   5 Signing in to the GM Early Years App
  6 Troubleshooting   7 Contact & support   8 About this guide
Cover, Contents and Introduction stay first. Section numbers are renumbered everywhere (page labels, Contents,
How this guide works, cross-references, CSS that targets Section 3 -> Section 5). The NHS login account issues
list loses "Check your NHS account details" (7 items). The NHS login section start page is titled
"Signing in to NHS login". Back/Next follow the new order.
Room: Contents drops the Cover page row and the "Select Next below" tip; How this guide works drops the grey
descriptions and the "Tap a section" line; Contents rows 37 px on iPhone SE in Safari.
usage: python3 make281.py v2.80.html v2.81.html
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
CHEV = re.search(r'<a class="toc-row" href="#s2"><span class="gb">2</span><span class="tt">Checklist</span>(<svg.*?</svg>)</a>', s, re.S).group(1)
# 1. old section numbers -> new (1->3 ... 6->8), everywhere (labels, aria, CSS, cross-references)
MAP = {'1': '3', '2': '4', '3': '5', '4': '6', '5': '7', '6': '8'}
s, n = re.subn(r'\bSection ([1-6])\b', lambda m: 'Section ' + MAP[m.group(1)], s)
print('section numbers changed:', n)
assert '[data-sec^="Section 5"]' in s and '[data-sec^="Section 3"]' not in s
# hidden big numbers on section start pages
for pid, old, new in (('hv', 1, 3), ('s2', 2, 4), ('s3', 3, 5), ('s4', 4, 6), ('s5', 5, 7), ('s6', 6, 8)):
    edit(pid, '<span class="tp-n" aria-hidden="true">%d</span>' % old, '<span class="tp-n" aria-hidden="true">%d</span>' % new)
# 2. new Section 1 (How this guide works) and Section 2 (NHS login)
NEW1, NEW2 = 'Section 1 · How this guide works', 'Section 2 · NHS login'
edit('how', 'data-sec="Section 8 · About this guide"', 'data-sec="%s"' % NEW1)
edit('how', '<span>Section 8 · About this guide</span>', '<span>%s</span>' % NEW1)
BLOCK = ['s4-signin', 'step-a', 'step-b', 'step-b-tip', 'step-c', 'step-c-tip', 'step-d', 'step-d-tip', 'step-e', 'step-e-tip',
         'step-f', 'step-f-tip', 'step-g', 'step-g-tip', 'step-h', 'step-h-tip']
for pid in BLOCK:
    edit(pid, 'data-sec="Section 6 · Troubleshooting"', 'data-sec="%s"' % NEW2)
    edit(pid, '<span>Section 6 · Troubleshooting</span>', '<span>%s</span>' % NEW2)
edit('s4-signin', 'data-title="Check your NHS account details"', 'data-title="Signing in to NHS login"')
edit('s4-signin', '<h2 class="h2" tabindex="-1">Check your NHS account details</h2>', '<h2 class="h2" tabindex="-1">Signing in to NHS login</h2>')
edit('s4-signin', 'aria-label="Check your NHS account details"', 'aria-label="Section 2: Signing in to NHS login"')
edit('s4-signin', '<b>NHS login</b><span>Account issues</span>', '<b>NHS login</b><span>Signing in</span>')
# 3. move pages: how, then the NHS login block, straight after the Introduction
m = page('how'); how = m.group(0); s = s[:m.start()] + s[m.end():].lstrip('\n')
a = page('s4-signin').start(); e = page('step-h-tip').end(); blk = s[a:e]; s = s[:a] + s[e:].lstrip('\n')
k = page('intro').end(); s = s[:k] + '\n' + how + '\n' + blk + s[k:]
# 4. Back / Next where the order changed
for pid, kind, old, new in (('intro', 'next', 'hv', 'how'), ('how', 'back', 's6', 'intro'), ('how', 'next', 'doc-control', 's4-signin'),
                            ('s4-signin', 'back', 's4-setup', 'how'), ('step-h-tip', 'next', 's4-cannot', 'hv'), ('hv', 'back', 'intro', 'step-h-tip'),
                            ('s4-setup', 'next', 's4-signin', 's4-cannot'), ('s4-cannot', 'back', 'step-h-tip', 's4-setup'),
                            ('s6', 'next', 'how', 'doc-control'), ('doc-control', 'back', 'how', 's6')):
    edit(pid, 'class="nav-btn nav-%s" href="#%s"' % (kind, old), 'class="nav-btn nav-%s" href="#%s"' % (kind, new))
# 5. Contents
rows = ''.join('<a class="toc-row" href="#%s"><span class="gb">%d</span><span class="tt">%s</span>%s</a>\n' % (h, i, t, CHEV) for i, (h, t) in enumerate(
    (('how', 'How this guide works'), ('s4-signin', 'Signing in to NHS login'), ('hv', 'Your Health Visiting team'), ('s2', 'Checklist'),
     ('s3', 'Signing in to the GM Early Years App'), ('s4', 'Troubleshooting'), ('s5', 'Contact &amp; support'), ('s6', 'About this guide')), 1))
c = page('contents').group(0)
old = re.search(r'<a class="toc-row" href="#hv">.*?<a class="toc-row" href="#s6">.*?</a>\n', c, re.S).group(0)
edit('contents', old, rows)
# 6. How this guide works: the new route (sections 2 to 8)
h = page('how').group(0)
oldlist = re.search(r'<ol class="how-flow"[^>]*>.*?</ol>', h, re.S).group(0)
branch = re.search(r'<div class="how-branch".*?</div>', oldlist, re.S).group(0)
def li(n, href, t, sub, extra=''):
    return '<li><a class="how-row" href="#%s"><span class="gb">%d</span><span class="tt">%s<small>%s</small></span>%s</a>%s</li>\n' % (href, n, t, sub, CHEV, extra)
newlist = ('<ol class="how-flow" aria-label="The sections of this guide">\n'
    + li(2, 's4-signin', 'Signing in to NHS login', 'Sign in and check your NHS details')
    + li(3, 'hv', 'Your Health Visiting team', 'Who to contact about your account')
    + li(4, 's2', 'Checklist', 'Are you ready to sign in?', branch)
    + li(5, 's3', 'Signing in', 'Step by step from your link')
    + li(6, 's4', 'Troubleshooting', 'Help with common problems')
    + li(7, 's5', 'Contact &amp; support', 'Who to contact for help')
    + li(8, 's6', 'About this guide', 'Document control and revisions') + '</ol>')
edit('how', oldlist, newlist)
# 7. About this guide list: How this guide works has moved
edit('s6', re.search(r'<a class="toc-row" href="#how">.*?</a>\n', page('s6').group(0), re.S).group(0), '')
edit('s6', '<a class="toc-row" href="#doc-control"><span class="gb">2</span>', '<a class="toc-row" href="#doc-control"><span class="gb">1</span>')
edit('s6', '<a class="toc-row" href="#revisions"><span class="gb">3</span>', '<a class="toc-row" href="#revisions"><span class="gb">2</span>')
# 8. NHS login account issues list: Check your NHS account details has moved out
edit('s4-nhs', re.search(r'\n?<a class="toc-row" href="#s4-signin">.*?</a>', page('s4-nhs').group(0), re.S).group(0), '')
for pid, n in (('s4-cannot', 3), ('s4-pw', 4), ('s4-code', 5), ('s4-email', 6), ('s4-mobile', 7), ('s4-name', 8)):
    edit('s4-nhs', '<a class="toc-row" href="#%s"><span class="gb">%d</span>' % (pid, n), '<a class="toc-row" href="#%s"><span class="gb">%d</span>' % (pid, n - 1))
assert len(re.findall(r'class="toc-row"', page('s4-nhs').group(0))) == 7
# 9. renumber every page
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
for n2, pid in enumerate(order, 1):
    blk2 = page(pid).group(0)
    c2 = re.findall(r'<span class="count">\d+ / \d+</span>', blk2); assert len(c2) == 1, pid
    edit(pid, c2[0], '<span class="count">%d / %d</span>' % (n2, total))
    a2 = re.findall(r'aria-label="Contents \(page \d+ of \d+\)"', blk2)
    if a2: edit(pid, a2[0], 'aria-label="Contents (page %d of %d)"' % (n2, total))
print({k: len(v) for k, v in secs.items()})
# 9b. make room (Contents gained two rows, How this guide works one): Contents loses the Cover page row (Back
#     from Contents still goes to the cover) and the "Select Next below..." tip; How this guide works loses the
#     grey descriptions under each section and the "Tap a section..." line. iPhone SE in Safari: Contents rows 37 px.
cv = re.search(r'<a class="toc-row" href="#cover">.*?</a>\n', page('contents').group(0), re.S).group(0)
edit('contents', cv, '')
tip = re.search(r'<div class="tip nav-tip" role="note">.*?</div>\n?', page('contents').group(0), re.S).group(0)
edit('contents', tip, '')
h = page('how').group(0)
h2 = re.sub(r'<small>[^<]*</small>', '', h)
h2 = re.sub(r'<p class="lead how-lead">[^<]*</p>\n?', '', h2)
assert h2 != h and '<small>' not in h2 and 'how-lead' not in h2
s = s.replace(h, h2)
rep('@media print{', '/* 2.81 Contents on iPhone SE in Safari: 37 px rows so all ten rows fit */\n@media (max-height:600px){#app #contents .toc-row{min-height:37px!important;padding-top:3px!important;padding-bottom:3px!important}}\n@media print{')
# 10. version
rep('Carer role v2.80', 'Carer role v2.81'); rep('Version 2.80 iPhone', 'Version 2.81 iPhone')
rep('<div>Version 2.80</div>', '<div>Version 2.81</div>'); rep('>2.80 – REVIEW DRAFT', '>2.81 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.78</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.80</span>', '<div class="rr"><span class="rv">2.81</span><span class="rd">17 Nov 2026</span><p>New section order: How this guide works and Signing in to NHS login first</p></div>\n<div class="rr"><span class="rv">2.80</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
