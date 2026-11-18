"""Guide 2.88 (from 2.87). Section 3 · NHS login pages 2 and 3 combined (David, 18 Nov):
 "Signing in to NHS login" (what this is) and "Step 1 · Go to NHS login" (the link) become one Step 1 page:
 why -> open this website -> the link -> a quieter "Cannot sign in?" line. The sign-in start page (s4-signin)
 is removed; "Sign in to check your details" and Next on page 1 go straight to Step 1.
 Section 3 is 16 pages; the guide is 71 pages.
usage: python3 make288.py v2.87.html v2.88.html
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

# 1. Step 1 carries the introduction, the link and the help line
edit('step-a', '<div class="step-body">\n<p>To see and manage your NHS login details, open this website in Safari on your iPhone, or on any computer:</p>\n'
     '<a class="btn" href="https://settings.login.nhs.uk/" rel="noopener" target="_blank">https://settings.login.nhs.uk/</a>\n</div>',
     '<div class="step-body s1-body">\n'
     '<p class="s1-why">Sign in to your own <strong>NHS login</strong> account to check your details. You use the same <strong>email address</strong> and <strong>password</strong> for the GM Early Years App.</p>\n'
     '<p class="s1-do">Open this website in <strong>Safari</strong> on your iPhone, or on any computer:</p>\n'
     '<a class="btn s1-link" href="https://settings.login.nhs.uk/" rel="noopener" target="_blank">settings.login.nhs.uk</a>\n'
     '<p class="s1-help"><strong>Cannot sign in?</strong> See <a href="#s4-nhs">NHS login account issues</a> in Section 7. '
     '(The GMDP Support team cannot assist with NHS login account issues, as they do not have access to NHS login accounts.)</p>\n'
     '</div>')
edit('step-a', 'class="nav-btn nav-back" href="#s4-signin"', 'class="nav-btn nav-back" href="#nhs"')

# 2. remove the separate sign-in start page; page 1 leads straight to Step 1
m = page('s4-signin'); s = s[:m.start()] + s[m.end():].lstrip('\n')
edit('nhs', 'class="nav-btn nav-next" href="#s4-signin"', 'class="nav-btn nav-next" href="#step-a"')
edit('nhs', '<a class="match-go" href="#s4-signin">', '<a class="match-go" href="#step-a">')
rep('#s4-signin .lead.nhs-only{font-size:15px;color:var(--muted,#4c6272)}\n', '')
assert 's4-signin' not in s, s.count('s4-signin')

CSS = '''/* 2.88 Step 1: introduction + link + help line in one page */
#app #step-a .s1-why{margin:0 0 12px}
#app #step-a .s1-do{margin:0}
#app #step-a .s1-link{display:flex;align-items:center;justify-content:center;width:100%;box-sizing:border-box;margin-top:10px;text-decoration:none}
#app #step-a .s1-help{margin:16px 0 0;padding-top:12px;border-top:1px solid var(--line);color:var(--sub)}
'''
rep('/* 2.87 Section 3 start page', CSS + '/* 2.87 Section 3 start page', 1)

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
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

rep('Carer role v2.87', 'Carer role v2.88'); rep('Version 2.87 iPhone', 'Version 2.88 iPhone')
rep('<div>Version 2.87</div>', '<div>Version 2.88</div>'); rep('>2.87 – REVIEW DRAFT', '>2.88 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.85</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.87</span>', '<div class="rr"><span class="rv">2.88</span><span class="rd">18 Nov 2026</span><p>NHS login: introduction and Step 1 combined into one page</p></div>\n<div class="rr"><span class="rv">2.87</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
