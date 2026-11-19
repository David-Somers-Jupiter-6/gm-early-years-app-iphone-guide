"""Guide 2.92 (from 2.91). David, 19 Nov:
 1. "Signing in to NHS login" (NHS login Steps 1-7 and their tips) moves into Section 7 · Troubleshooting,
    straight after "NHS login account issues", and becomes option 1 on that list. Section "NHS login" keeps
    "Before you sign in".
 2. Contact your Health Visiting team becomes Section 2 (Contents, roadmap, page order):
    1 How this guide works · 2 Contact your Health Visiting team · 3 About your account · 4 NHS login ·
    5 Checklist · 6 Signing in · 7 Troubleshooting · 8 Contact & support · 9 About this guide.
 3. Roadmap options listed vertically.
 4. Team finder wording: "If you need to contact your Health Visiting team, you can find their contact details by:
    - selecting your Locality - then selecting your Health Visiting team" (Section 2 and the Section 8 copy).
usage: python3 make292.py v2.91.html v2.92.html
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
def cut(pids):
    global s
    out = []
    for pid in pids:
        m = page(pid); out.append(m.group(0)); s = s[:m.start()] + s[m.end():].lstrip('\n')
    return '\n'.join(out)
def put_after(pid, html):
    global s
    k = page(pid).end(); s = s[:k] + '\n' + html + s[k:]

# 0. section numbers: 4 -> 2, 2 -> 3, 3 -> 4 (labels, aria, text)
MAP = {'2': '3', '3': '4', '4': '2'}
s, n = re.subn(r'\bSection ([234])\b', lambda m: 'Section ' + MAP[m.group(1)], s)
print('section numbers changed:', n)

# 1. NHS login steps -> Section 7, after "NHS login account issues"
STEPS = ['step-a', 'step-c', 'step-c-tip', 'step-d', 'step-d-tip', 'step-e', 'step-e-tip', 'step-f', 'step-f-tip', 'step-g', 'step-g-tip', 'step-h', 'step-h-tip']
blocks = cut(STEPS)
blocks = blocks.replace('data-sec="Section 4 · NHS login"', 'data-sec="Section 7 · Troubleshooting"').replace('<span>Section 4 · NHS login</span>', '<span>Section 7 · Troubleshooting</span>')
assert 'Section 4 · NHS login' not in blocks
put_after('s4-nhs', blocks)
edit('s4-nhs', 'class="nav-btn nav-next" href="#s4-setup"', 'class="nav-btn nav-next" href="#step-a"')
edit('step-a', 'class="nav-btn nav-back" href="#nhs"', 'class="nav-btn nav-back" href="#s4-nhs"')
nx = re.search(r'class="nav-btn nav-next" href="#([^"]+)"', page('step-h-tip').group(0)).group(1)
edit('step-h-tip', 'class="nav-btn nav-next" href="#%s"' % nx, 'class="nav-btn nav-next" href="#s4-setup"')
edit('s4-setup', 'class="nav-btn nav-back" href="#s4-nhs"', 'class="nav-btn nav-back" href="#step-h-tip"')
# option 1 on the issues list
lst = re.search(r'<nav aria-label="NHS login account issues" class="toc toc-sm">.*?</nav>', page('s4-nhs').group(0), re.S).group(0)
def bump(m): return '<span class="gb">%d</span>' % (int(m.group(1)) + 1)
new = re.sub(r'<span class="gb">(\d)</span>', bump, lst)
first = re.search(r'<a class="toc-row" href="#s4-setup">.*?</a>', new, re.S).group(0)
row1 = re.sub(r'href="#s4-setup"', 'href="#step-a"', first).replace('<span class="gb">2</span>', '<span class="gb">1</span>').replace('<span class="tt">Set up NHS login</span>', '<span class="tt">Signing in to NHS login</span>')
new = new.replace(first, row1 + '\n' + first)
edit('s4-nhs', lst, new)
# words that pointed elsewhere
edit('step-a', '<p class="s1-help"><strong>Cannot sign in?</strong> See <a href="#s4-nhs">NHS login account issues</a> in Section 7. ',
     '<p class="s1-help"><strong>Cannot sign in?</strong> See the other <a href="#s4-nhs">NHS login account issues</a>. ')
edit('step-h-tip', '<p style="margin-top:14px">You have now signed in to NHS login. Tap <strong>Next</strong> to go to <a href="#hv">Section 2 · Contact your Health Visiting team</a>.</p>',
     '<p style="margin-top:14px">You have now signed in to NHS login. If any of these details are different from your GM Early Years App account, <a href="#hv">contact your Health Visiting team</a>.</p>')

# 2. Contact your Health Visiting team -> straight after the roadmap
hvb = cut(['hv', 'hv-confirm'])
put_after('roadmap', hvb)
edit('roadmap', 'class="nav-btn nav-next" href="#acct"', 'class="nav-btn nav-next" href="#hv"')
edit('hv', 'class="nav-btn nav-back" href="#step-h-tip"', 'class="nav-btn nav-back" href="#roadmap"')
edit('hv-confirm', 'class="nav-btn nav-next" href="#s2"', 'class="nav-btn nav-next" href="#acct"')
edit('acct', 'class="nav-btn nav-back" href="#roadmap"', 'class="nav-btn nav-back" href="#hv-confirm"')
edit('nhs', 'class="nav-btn nav-next" href="#step-a"', 'class="nav-btn nav-next" href="#s2"')
edit('s2', 'class="nav-btn nav-back" href="#hv-confirm"', 'class="nav-btn nav-back" href="#nhs"')
edit('hv', '<span class="tp-n" aria-hidden="true">4</span>', '<span class="tp-n" aria-hidden="true">2</span>')

# Contents
CHEV = re.search(r'<a class="toc-row" href="#how"><span class="gb">1</span><span class="tt">How this guide works</span>(<svg.*?</svg>)</a>', s, re.S).group(1)
rows = ''.join('<a class="toc-row" href="#%s"><span class="gb">%d</span><span class="tt">%s</span>%s</a>\n' % (h, i, t, CHEV) for i, (h, t) in enumerate(
    (('how', 'How this guide works'), ('hv', 'Contact your Health Visiting team'), ('acct', 'About your account'), ('nhs', 'NHS login'),
     ('s2', 'Run through the Checklist'), ('s3', 'Signing in to the GM Early Years App'), ('s4', 'Troubleshooting'),
     ('s5', 'Contact &amp; support'), ('s6', 'About this guide')), 1))
old = re.search(r'<a class="toc-row" href="#how">.*?<a class="toc-row" href="#s6">.*?</a>\n', page('contents').group(0), re.S).group(0)
edit('contents', old, rows)

# 3. roadmap: stage 1 in the new order, options listed vertically
r = page('roadmap').group(0)
def chip(href, n, t): return '<a class="rm-chip" href="#%s"><span class="rm-cn">%d</span>%s</a>' % (href, n, t)
old1 = re.search(r'<div class="rm-chips"><a class="rm-chip" href="#acct">.*?</div>', r, re.S).group(0)
edit('roadmap', old1, '<div class="rm-chips">' + chip('hv', 2, 'Contact your HV team') + chip('acct', 3, 'About your account') + chip('nhs', 4, 'NHS login') + chip('s2', 5, 'Checklist') + '</div>')

edit('roadmap', '<p class="hw-p rm-lead">Tap a section to go straight to it.</p>\n', '')

# 4. team finder wording (Section 2 and the Section 8 copy)
OLDHOW = '<p class="q-hint hv-how">To see your team’s contact details, select your <strong>Locality</strong>, then your <strong>Health Visiting team</strong>.</p>'
NEWHOW = ('<div class="q-hint hv-how"><div class="hv-how-full"><p class="hv-how-p">If you need to contact your Health Visiting team, you can find their contact details by:</p>'
          '<ul class="hv-how-l"><li>selecting your <strong>Locality</strong></li><li>then selecting your <strong>Health Visiting team</strong></li></ul></div>'
          '<p class="hv-how-short" aria-hidden="true">Select your <strong>Locality</strong>, then your <strong>Health Visiting team</strong>.</p></div>')
rep(OLDHOW, NEWHOW, 2)
# once a team is chosen (Section 2), the same instruction shows on one line so the team card fits
SHORT = ''.join('#app #hv:has(#hvs-loc option[value="%s"]:checked):has(#hvs-team-%s option:not([value=""]):checked) .hv-how-full{display:none}'
                '#app #hv:has(#hvs-loc option[value="%s"]:checked):has(#hvs-team-%s option:not([value=""]):checked) .hv-how-short{display:block}\n' % (t, t, t, t)
                for t in ('Bury', 'Rochdale', 'Stockport'))

CSS = '''/* 2.92 roadmap options listed vertically; team finder instruction as a sentence + two bullets */
#app #roadmap .rm-chips{flex-direction:column;align-items:stretch;gap:3px}
#app #roadmap .rm-chip{display:flex;width:100%;min-height:32px;border-radius:10px;padding:2px 12px 2px 5px}
#app #roadmap .rm-st{padding-bottom:9px}#app #roadmap .rm-st+.rm-st{padding-top:9px}#app #roadmap .rm-h{margin-bottom:6px}
@media screen and (max-height:600px){#app #roadmap .rm-chip{min-height:31px}#app #roadmap .rm-st{padding-bottom:7px}#app #roadmap .rm-st+.rm-st{padding-top:7px}#app #roadmap .rm-h{margin-bottom:4px}}
#app :is(#hv,#s5-hv) .hv-how .hv-how-p{margin:0;font-size:inherit;line-height:inherit;color:inherit}
#app :is(#hv,#s5-hv) .hv-how .hv-how-l{margin:4px 0 0;padding:0 0 0 22px}
#app :is(#hv,#s5-hv) .hv-how .hv-how-l li{margin:0;padding:0;font-size:inherit;line-height:1.35;color:inherit}
#app :is(#hv,#s5-hv) .hv-how .hv-how-short{display:none;margin:0;font-size:inherit;line-height:inherit;color:inherit}
@media screen and (max-width:369px){#app #hv .hv-how{margin-bottom:8px!important}#app #hv .hv-card{margin-top:8px!important}}
''' + SHORT
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)   # after the 2.91 rules, so these win

# renumber every page
order = [m.group(1) for m in re.finditer(r'<section class="screen(?: cover)?" id="([^"]+)"', s)]
order = [p for p in order if p != 'search']
total = len(order); assert total == 70, total
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

rep('Carer role v2.91', 'Carer role v2.92'); rep('Version 2.91 iPhone', 'Version 2.92 iPhone')
rep('<div>Version 2.91</div>', '<div>Version 2.92</div>'); rep('>2.91 – REVIEW DRAFT', '>2.92 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.89</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.91</span>', '<div class="rr"><span class="rv">2.92</span><span class="rd">19 Nov 2026</span><p>New order: Contact your HV team is Section 2; NHS login sign-in steps in Troubleshooting</p></div>\n<div class="rr"><span class="rv">2.91</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
