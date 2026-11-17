"""Guide 2.82 (from 2.81). Skeleton of David's new Contents (17 Nov):
  I Introduction
  1 How this guide works
  2 About your account            (checklist Information 1 + 2 combined into one page, id acct)
  3 NHS login                      (new start page nhs with a) and b)
      a) Information needed from NHS login   (placeholder page nhs-info, content to follow)
      b) Signing in to NHS login             (the existing NHS login sign-in pages)
  4 Contact your Health Visiting team
      the team finder (hv) + "Confirm your NHS login contact details" (placeholder page hv-confirm)
  5 Run through the Checklist      (start page, questions 1-4, summary; the two information pages removed)
  6 Signing in to the GM Early Years App   7 Troubleshooting   8 Contact & support   9 About this guide
  Accessibility (unchanged)
Section numbers 2-8 move up by one everywhere (labels, Contents, cross-references, CSS that targets them).
Checklist progress bar: 4 segments (was 2 information + 4 questions); the JS that colours earlier answers is updated.
usage: python3 make282.py v2.81.html v2.82.html
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
def remove(pid):
    global s
    m = page(pid); s = s[:m.start()] + s[m.end():].lstrip('\n')
def insert_after(pid, html):
    global s
    k = page(pid).end(); s = s[:k] + '\n' + html + s[k:]
CHEV = re.search(r'<a class="toc-row" href="#s2"><span class="gb">4</span><span class="tt">Checklist</span>(<svg.*?</svg>)</a>', s, re.S).group(1)

# 1. section numbers 2..8 -> 3..9 (labels, aria, cross-references, CSS)
s, n = re.subn(r'\bSection ([2-8])\b', lambda m: 'Section %d' % (int(m.group(1)) + 1), s)
print('section numbers changed:', n)
assert '[data-sec^="Section 6"]' in s and '[data-sec^="Section 5"]' not in s
for pid, old in (('hv', 3), ('s2', 4), ('s3', 5), ('s4', 6), ('s5', 7), ('s6', 8)):
    edit(pid, '<span class="tp-n" aria-hidden="true">%d</span>' % old, '<span class="tp-n" aria-hidden="true">%d</span>' % (old + 1))
rep('data-sec="Section 4 · Health Visiting team"', 'data-sec="Section 4 · Your Health Visiting team"', 1)
rep('<span>Section 4 · Health Visiting team</span>', '<span>Section 4 · Your Health Visiting team</span>', 1)

# shared parts for new pages
how = page('how').group(0)
NAV = re.search(r'<nav class="bnav".*?</nav>', how, re.S).group(0)
def nav(back, nxt):
    return NAV.replace('class="nav-btn nav-back" href="#intro"', 'class="nav-btn nav-back" href="#%s"' % back) \
              .replace('class="nav-btn nav-next" href="#s4-signin"', 'class="nav-btn nav-next" href="#%s"' % nxt)
def strip(sec):
    return '<div class="strip" aria-hidden="true"><div class="strip-row"><span>%s</span><span class="pos">Page 1 of 1</span></div></div>' % sec
def screen(pid, sec, title, box, body, back, nxt, aria=None):
    return ('<section class="screen" id="%s" data-sec="%s" data-title="%s" aria-label="%s">\n<div class="scroll">\n%s\n%s\n%s\n</div>\n%s\n</section>'
            % (pid, sec, title, aria or title, box, strip(sec), body, nav(back, nxt)))
NHSBOX = re.search(r'<div class="pbox has-badge eyx eyx-nhs">.*?</div>(?=\n<div class="strip")', page('s4-signin').group(0), re.S).group(0)
def nhsbox(sub, h):
    b = NHSBOX.replace('<b>NHS login</b><span>Signing in</span>', '<b>NHS login</b><span>%s</span>' % sub)
    return b.replace('<h2 class="h2" tabindex="-1">Signing in to NHS login</h2>', '<h2 class="h2" tabindex="-1">%s</h2>' % h)
TBC = '<div class="tip tbc" role="note"><p><strong>Content to follow.</strong> This page is part of the new structure and is still being written.</p></div>'

# 2. Section 2 · About your account (Information 1 + 2 combined)
SEC2 = 'Section 2 · About your account'
acct = screen('acct', SEC2, 'About your account',
    '<div class="pbox"><h2 class="h2" tabindex="-1">About your account</h2></div>',
    '<p class="info-lead">Your Health Visiting team sets up a GM Early Years App account for the <strong>child\'s mother</strong> or <strong>primary carer</strong>.</p>\n'
    '<div class="tip info-q"><p>In this guide, this person is called the <strong>account holder</strong>.</p></div>\n'
    '<ul class="facts acct-list"><li>Only the account holder can sign in.</li>'
    '<li>They use the same <strong>email address</strong> and <strong>password</strong> as their own NHS login account.</li></ul>\n'
    '<div class="amber info-q"><p>A partner or another family member cannot sign in to the account.</p></div>',
    'how', 'nhs', 'Section 2: About your account')
insert_after('how', acct)

# 3. Section 3 · NHS login: start page + a) placeholder, then b) the existing sign-in pages
SEC3 = 'Section 3 · NHS login'
nhs = screen('nhs', SEC3, 'NHS login', nhsbox('Overview', 'NHS login'),
    '<p class="lead">This section has two parts:</p>\n<nav aria-label="NHS login" class="toc toc-sm">\n'
    '<a class="toc-row" href="#nhs-info"><span class="gb">a</span><span class="tt">Information needed from NHS login</span>%s</a>\n'
    '<a class="toc-row" href="#s4-signin"><span class="gb">b</span><span class="tt">Signing in to NHS login</span>%s</a>\n</nav>' % (CHEV, CHEV),
    'acct', 'nhs-info', 'Section 3: NHS login')
nhsinfo = screen('nhs-info', SEC3, 'Information needed from NHS login', nhsbox('Information', 'Information needed from NHS login'),
    TBC, 'nhs', 's4-signin')
insert_after('acct', nhs); insert_after('nhs', nhsinfo)
edit('s4-signin', 'class="nav-btn nav-back" href="#how"', 'class="nav-btn nav-back" href="#nhs-info"')

# 4. Section 4 · Contact your Health Visiting team: finder + placeholder
edit('hv', 'data-title="Your Health Visiting team"', 'data-title="Contact your Health Visiting team"')
edit('hv', '<h2 class="h2 tp-h" tabindex="-1">Your Health Visiting team</h2>', '<h2 class="h2 tp-h" tabindex="-1">Contact your Health Visiting team</h2>')
edit('hv', 'aria-label="Your Health Visiting team"', 'aria-label="Section 4: Contact your Health Visiting team"')
hvc = screen('hv-confirm', 'Section 4 · Your Health Visiting team', 'Confirm your NHS login contact details',
    '<div class="pbox"><h2 class="h2" tabindex="-1">Confirm your NHS login contact details</h2></div>', TBC, 'hv', 's2')
insert_after('hv', hvc)
edit('hv', 'class="nav-btn nav-next" href="#s2"', 'class="nav-btn nav-next" href="#hv-confirm"')
edit('s2', 'class="nav-btn nav-back" href="#hv"', 'class="nav-btn nav-back" href="#hv-confirm"')

# 5. Section 5 · Checklist without the two information pages
remove('ci1'); remove('ci2')
edit('s2', 'href="#ci1"', 'href="#c1"')
edit('c1', 'class="nav-btn nav-back" href="#ci2"', 'class="nav-btn nav-back" href="#s2"')
edit('s2', '<h2 class="h2 tp-h" tabindex="-1">Checklist</h2>', '<h2 class="h2 tp-h" tabindex="-1">Run through the Checklist</h2>')
old = re.search(r'<p class="lead chk-has">The checklist has:</p>\n<ul class="facts">.*?</ul>', page('s2').group(0), re.S).group(0)
edit('s2', old, '<p class="lead chk-has">The checklist has <strong>4 questions</strong> with a <strong>Yes</strong> or <strong>No</strong> answer.</p>')
for pid in ('c1', 'c2', 'c3', 'c4', 'sum'):
    blk = page(pid).group(0)
    st = re.search(r'(<div class="stepper chk-steps" aria-hidden="true">)(.*?)(</div>)', blk).group(0)
    spans = re.findall(r'<span class="[^"]*">[^<]*</span>', st); assert len(spans) == 6, pid
    spans = [re.sub(r'>(\d)<', lambda m: '>%d<' % (int(m.group(1)) - 2), x) for x in spans[2:]]
    edit(pid, st, '<div class="stepper chk-steps" aria-hidden="true">' + ''.join(spans) + '</div>')
rep('.stepper.chk-steps span:nth-child(2){margin-right:7px}', '')
rep("var order=['ci1','ci2','c1','c2','c3','c4','sum'];", "var order=['c1','c2','c3','c4','sum'];")
rep('for(var i=2;i<k&&i<order.length;i++)', 'for(var i=0;i<k&&i<order.length;i++)')
rep("if(cur&&cur.id==='s2'&&a.getAttribute('href')==='#ci1') resetChecklist();", "if(cur&&cur.id==='s2'&&a.getAttribute('href')==='#c1') resetChecklist();")
assert not re.search(r'(href="#|id="|\')ci[12]\b', s)   # (old #ci1/#ci2 style rules stay; they match nothing)

# 6. How this guide works -> About your account
edit('how', 'class="nav-btn nav-next" href="#s4-signin"', 'class="nav-btn nav-next" href="#acct"')

# 7. Contents
rows = ''.join('<a class="toc-row" href="#%s"><span class="gb">%d</span><span class="tt">%s</span>%s</a>\n' % (h, i, t, CHEV) for i, (h, t) in enumerate(
    (('how', 'How this guide works'), ('acct', 'About your account'), ('nhs', 'NHS login'), ('hv', 'Contact your Health Visiting team'),
     ('s2', 'Run through the Checklist'), ('s3', 'Signing in to the GM Early Years App'), ('s4', 'Troubleshooting'),
     ('s5', 'Contact &amp; support'), ('s6', 'About this guide')), 1))
old = re.search(r'<a class="toc-row" href="#how">.*?<a class="toc-row" href="#s6">.*?</a>\n', page('contents').group(0), re.S).group(0)
edit('contents', old, rows)

# 8. How this guide works list: sections 2 to 9
h = page('how').group(0)
oldlist = re.search(r'<ol class="how-flow"[^>]*>.*?</ol>', h, re.S).group(0)
branch = re.search(r'<div class="how-branch".*?</div>', oldlist, re.S).group(0)
def li(n, href, t, extra=''):
    return '<li><a class="how-row" href="#%s"><span class="gb">%d</span><span class="tt">%s</span>%s</a>%s</li>\n' % (href, n, t, CHEV, extra)
newlist = ('<ol class="how-flow" aria-label="The sections of this guide">\n'
    + li(2, 'acct', 'About your account') + li(3, 'nhs', 'NHS login') + li(4, 'hv', 'Contact your Health Visiting team')
    + li(5, 's2', 'Run through the Checklist', branch) + li(6, 's3', 'Signing in') + li(7, 's4', 'Troubleshooting')
    + li(8, 's5', 'Contact &amp; support') + li(9, 's6', 'About this guide') + '</ol>')
edit('how', oldlist, newlist)

# 9. styles: placeholder note, NHS blue title box on the new Health Visiting page
CSS = ('/* 2.82 skeleton: placeholder pages; NHS blue on the new Health Visiting page */\n'
       '.tip.tbc{border-style:dashed}\n'
       '#app .screen#hv-confirm:not(#contents) .pbox:not(.eyx){background:linear-gradient(135deg,#003087 0%,#005eb8 100%)!important}\n'
       '#acct .acct-list{margin-top:12px;margin-bottom:12px}\n'
       '/* 2.82 Contents (11 rows) and How this guide works (8 rows) on shorter screens */\n'
       '@media (max-height:700px){#app #contents .toc-row{min-height:40px!important;padding-top:2px!important;padding-bottom:2px!important}#app #how .how-row{min-height:41px}}\n'
       '@media (max-height:600px){#app #contents .toc-row{min-height:34px!important}#app #contents .toc-row .tt{font-size:15.5px}#app #how .how-row{min-height:37px}}\n')
rep('@media print{', CSS + '@media print{')

# 10. renumber every page
order = [m.group(1) for m in re.finditer(r'<section class="screen(?: cover)?" id="([^"]+)"', s)]
order = [p for p in order if p != 'search']
total = len(order); assert total == 73, total
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
# Back/Next chain must follow the page order (the Welcome pages and search excepted)
for a, b in zip(order[3:], order[4:]):
    if b == 'search': continue
    assert re.search(r'class="nav-btn nav-next[^"]*" href="#%s"' % b, page(a).group(0)), ('next', a, b)
    assert re.search(r'class="nav-btn nav-back" href="#%s"' % a, page(b).group(0)), ('back', b, a)

# 11. version
rep('Carer role v2.81', 'Carer role v2.82'); rep('Version 2.81 iPhone', 'Version 2.82 iPhone')
rep('<div>Version 2.81</div>', '<div>Version 2.82</div>'); rep('>2.81 – REVIEW DRAFT', '>2.82 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.79</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.81</span>', '<div class="rr"><span class="rv">2.82</span><span class="rd">17 Nov 2026</span><p>New structure: nine sections, with placeholder pages for new content</p></div>\n<div class="rr"><span class="rv">2.81</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
