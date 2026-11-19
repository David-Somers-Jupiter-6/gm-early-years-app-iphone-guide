"""Guide 2.91 (from 2.90). Section 1 · How this guide works (David, 19 Nov):
 page 1 "How this guide works" - David's description (why the guide exists, what it will do: three points);
 page 2 "Your roadmap" (new) - what happens next, in the same three stages:
   1 What you need       -> 2 About your account, 3 NHS login, 4 Contact your HV team, 5 Checklist
   2 How to sign in      -> 6 Signing in to the GM Early Years App
   3 Who can help        -> 7 Troubleshooting, 8 Contact & support
 The section list moves from page 1 to the roadmap (every section still one tap away). Guide 70 pages.
usage: python3 make291.py v2.90.html v2.91.html
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

how = page('how').group(0)
oldlist = re.search(r'<ol class="how-flow".*?</ol>', how, re.S).group(0)
# 1. page 1: David's description
INTRO = ('<p class="hw-p">Sometimes connecting to things online does not go the way we hope, and that can be frustrating. '
         '<strong>This guide is designed to help.</strong></p>\n'
         '<p class="hw-p hw-will">Working through the steps in this guide will:</p>\n'
         '<ol class="hw-list">'
         '<li><span class="hw-n" aria-hidden="true">1</span><span>Show you <strong>what you need</strong> to access the app</span></li>'
         '<li><span class="hw-n" aria-hidden="true">2</span><span>Show you <strong>examples</strong> of how to access the app</span></li>'
         '<li><span class="hw-n" aria-hidden="true">3</span><span>Show you <strong>who can help</strong>, and what to do, when there are problems</span></li>'
         '</ol>')
edit('how', oldlist, INTRO)
edit('how', 'class="nav-btn nav-next" href="#acct"', 'class="nav-btn nav-next" href="#roadmap"')

# 2. page 2: the roadmap
def chip(href, n, t):
    return '<a class="rm-chip" href="#%s"><span class="rm-cn">%d</span>%s</a>' % (href, n, t)
STAGES = [('What you need', [('acct', 2, 'About your account'), ('nhs', 3, 'NHS login'), ('hv', 4, 'Contact your HV team'), ('s2', 5, 'Checklist')]),
          ('How to sign in', [('s3', 6, 'Signing in to the GM Early Years App')]),
          ('Who can help', [('s4', 7, 'Troubleshooting'), ('s5', 8, 'Contact &amp; support')])]
stages = ''.join('<li class="rm-st"><p class="rm-h"><span class="rm-dot" aria-hidden="true">%d</span>%s</p><div class="rm-chips">%s</div></li>'
                 % (i, t, ''.join(chip(*c) for c in cs)) for i, (t, cs) in enumerate(STAGES, 1))
RM_BODY = ('<p class="hw-p rm-lead">Tap a section to go straight to it.</p>\n'
           '<ol class="rm" aria-label="Your roadmap">' + stages + '</ol>')
nav = re.search(r'<nav class="bnav".*?</nav>', page('how').group(0), re.S).group(0)
nav = nav.replace('class="nav-btn nav-back" href="#intro"', 'class="nav-btn nav-back" href="#how"').replace('class="nav-btn nav-next" href="#roadmap"', 'class="nav-btn nav-next" href="#acct"')
SEC1 = 'Section 1 · How this guide works'
RM = ('<section class="screen" id="roadmap" data-sec="%s" data-title="Your roadmap" aria-label="Your roadmap">\n<div class="scroll">\n'
      '<div class="pbox"><h2 class="h2" tabindex="-1">Your roadmap</h2></div>\n'
      '<div class="strip" aria-hidden="true"><div class="strip-row"><span>%s</span><span class="pos">Page 2 of 2</span></div></div>\n'
      '%s\n</div>\n%s\n</section>' % (SEC1, SEC1, RM_BODY, nav))
k = page('how').end(); s = s[:k] + '\n' + RM + s[k:]
edit('acct', 'class="nav-btn nav-back" href="#how"', 'class="nav-btn nav-back" href="#roadmap"')

CSS = '''/* 2.91 How this guide works (David's description) + Your roadmap */
#app #how .hw-p,#app #roadmap .hw-p{font-size:17px;line-height:1.45;color:var(--ink);margin:0 0 14px}
#app #how .hw-will{margin-bottom:10px}
#app #how .hw-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
#app #how .hw-list li{display:flex;align-items:flex-start;gap:12px;margin:0;padding:10px 12px;border:1px solid var(--line);border-radius:14px;background:var(--surface);font-size:17px;line-height:1.35;color:var(--ink)}
#app :is(#how,#roadmap) :is(.hw-n,.rm-dot){flex:0 0 28px;width:28px;height:28px;border-radius:50%;background:var(--accentSoft);border:1.5px solid var(--accent);color:var(--accent2);font:700 15px/1 var(--font-head);display:flex;align-items:center;justify-content:center;box-sizing:border-box}
#app #roadmap .rm-lead{margin-bottom:12px;color:var(--sub)}
#app #roadmap .rm{list-style:none;margin:0;padding:0}
#app #roadmap .rm-st{margin:0;padding:0 0 14px}
#app #roadmap .rm-st:last-child{padding-bottom:0}
#app #roadmap .rm-st+.rm-st{padding-top:12px;border-top:1px solid var(--line)}
#app #roadmap .rm-h{display:flex;align-items:center;gap:10px;margin:0 0 8px;font-family:var(--font-head);font-weight:700;font-size:18px;line-height:1.25;color:var(--ink)}
#app #roadmap .rm-chips{display:flex;flex-wrap:wrap;gap:6px}
#app #roadmap .rm-chip{display:inline-flex;align-items:center;gap:6px;min-height:36px;box-sizing:border-box;padding:3px 12px 3px 4px;border:1px solid var(--line);border-radius:999px;background:var(--surface);color:var(--accent2);font-weight:700;line-height:1.2;text-decoration:none}
#app #roadmap .rm-cn{flex:0 0 24px;width:24px;height:24px;border-radius:50%;background:var(--accentSoft);color:var(--accent2);font:700 13px/1 var(--font-head);display:flex;align-items:center;justify-content:center}
#app #roadmap .rm-chip:active{background:var(--accentSoft)}
#app #roadmap .rm-chip:focus-visible{outline:3px solid var(--ink);outline-offset:2px}
@media screen and (max-width:369px){#app #roadmap .rm-cn{display:none}#app #roadmap .rm-chip{padding:3px 11px;min-height:34px}#app #roadmap .rm-chips{gap:5px}#app #roadmap .rm-st{padding-bottom:10px}#app #roadmap .rm-st+.rm-st{padding-top:9px}#app #roadmap .rm-lead{margin-bottom:8px}}
@media screen and (max-height:600px){#app #roadmap .rm-lead{margin-bottom:8px}#app #roadmap .rm-st{padding-bottom:9px}#app #roadmap .rm-st+.rm-st{padding-top:8px}#app #roadmap .rm-h{margin-bottom:6px}#app #roadmap .rm-chips{gap:5px}#app #roadmap .rm-chip{min-height:34px}}
'''
rep('/* 2.89 Section 3 page 1: worked example */', CSS + '/* 2.89 Section 3 page 1: worked example */', 1)

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
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

rep('Carer role v2.90', 'Carer role v2.91'); rep('Version 2.90 iPhone', 'Version 2.91 iPhone')
rep('<div>Version 2.90</div>', '<div>Version 2.91</div>'); rep('>2.90 – REVIEW DRAFT', '>2.91 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.88</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.90</span>', '<div class="rr"><span class="rv">2.91</span><span class="rd">19 Nov 2026</span><p>How this guide works rewritten; new Your roadmap page</p></div>\n<div class="rr"><span class="rv">2.90</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
