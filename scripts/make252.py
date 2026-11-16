"""Guide 2.52 (from 2.51).
- New page in Section 6: "How this guide works" (id how). It shows the six sections in order as a
  tappable route, with the checklist branch: all Yes goes to Signing in, any No goes to Troubleshooting.
- Section 6 is now 4 pages; its list has the new page first. 72 pages.
usage: python3 make252.py v2.51.html v2.52.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

def page(pid):
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S)
    assert m, pid
    return m

def edit(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

CHEV = re.search(r'<svg class="chev".*?</svg>', s, re.S).group(0)

# --- the new page, with the Section 6 title page's navigation as a pattern ---
nav = re.search(r'<nav class="bnav".*?</nav>', page('s6').group(0), re.S).group(0)
navh = nav.replace('href="#a11y"', 'href="#s6"', 1)
assert navh != nav and 'href="#doc-control"' in navh

def step(n, href, title, sub, extra=''):
    return ('<li><a class="how-row" href="#%s"><span class="gb">%s</span><span class="tt">%s<small>%s</small></span>%s</a>%s</li>\n'
            % (href, n, title, sub, CHEV, extra))

branch = ('<div class="how-branch" role="note">'
          '<span class="hb hb-yes"><b aria-hidden="true">✓</b><span>All <strong>Yes</strong>: go to Signing in</span></span>'
          '<span class="hb hb-no"><b aria-hidden="true">✗</b><span>Any <strong>No</strong>: go to Troubleshooting</span></span>'
          '</div>')
how = ('<section class="screen" id="how" data-sec="Section 6 · About this guide" data-title="How this guide works" aria-label="How this guide works">\n'
       '<div class="scroll">\n'
       '<div class="pbox"><h2 class="h2" tabindex="-1">How this guide works</h2></div>\n'
       '<div class="strip" aria-hidden="true"><div class="strip-row"><span>Section 6 · About this guide</span><span class="pos">Page 2 of 4</span></div></div>\n'
       '<p class="lead how-lead">Tap a section to go straight to it.</p>\n'
       '<ol class="how-flow" aria-label="The sections of this guide">\n'
       + step(1, 'hv', 'Your Health Visiting team', 'Who to contact about your account')
       + step(2, 's2', 'Checklist', 'Are you ready to sign in?', branch)
       + step(3, 's3', 'Signing in', 'Step by step from your link')
       + step(4, 's4', 'Troubleshooting', 'Help with common problems')
       + step(5, 's5', 'Contact &amp; support', 'Who to contact for help')
       + step(6, 's6', 'About this guide', 'This page and the guide’s details')
       + '</ol>\n'
       '</div>\n' + navh + '\n</section>\n\n')
m = page('doc-control')
s = s[:m.start()] + how + s[m.start():]

# --- links around it ---
edit('s6', 'class="nav-btn nav-next" href="#doc-control"', 'class="nav-btn nav-next" href="#how"')
edit('doc-control', 'class="nav-btn nav-back" href="#s6"', 'class="nav-btn nav-back" href="#how"')
edit('s6', '<a class="toc-row" href="#doc-control"><span class="gb">1</span>',
     '<a class="toc-row" href="#how"><span class="gb">1</span><span class="tt">How this guide works<small>The sections and the route through them</small></span>' + CHEV + '</a>\n'
     '<a class="toc-row" href="#doc-control"><span class="gb">2</span>')
edit('s6', '<a class="toc-row" href="#revisions"><span class="gb">2</span>', '<a class="toc-row" href="#revisions"><span class="gb">3</span>')
for pid, a, b in (('s6', 'Page 1 of 3', 'Page 1 of 4'), ('doc-control', 'Page 2 of 3', 'Page 3 of 4'),
                  ('revisions', 'Page 3 of 3', 'Page 4 of 4')):
    edit(pid, '<span class="pos">%s</span>' % a, '<span class="pos">%s</span>' % b)

# --- Contents counter on every page (now 72) ---
ids = re.findall(r'<section class="screen[^"]*" id="([^"]+)"', s)
total = len(ids); assert total == 72, total
out = []; last = 0
for k, mm in enumerate(re.finditer(r'<section class="screen[^"]*" id="([^"]+)".*?</section>', s, re.S)):
    blk = mm.group(0)
    blk = re.sub(r'<span class="count">\d+ / \d+</span>', '<span class="count">%d / %d</span>' % (k + 1, total), blk)
    blk = re.sub(r'aria-label="Contents \(page \d+ of \d+\)"', 'aria-label="Contents (page %d of %d)"' % (k + 1, total), blk)
    out.append(s[last:mm.start()]); out.append(blk); last = mm.end()
s = ''.join(out) + s[last:]

css = '''/* 2.52 How this guide works: the sections as a route, with the checklist branch */
#how .how-lead{margin:0 0 8px}
.how-flow{list-style:none;margin:0;padding:0}
.how-flow li{position:relative}
.how-flow li:not(:last-child)::before{content:"";position:absolute;left:16px;top:38px;bottom:-6px;width:2px;background:#a9c7e6}
.how-row{position:relative;display:flex;align-items:center;gap:12px;min-height:44px;padding:5px 2px;color:var(--ink);text-decoration:none}
.how-row .gb{position:relative;z-index:1;flex:0 0 32px;width:32px;height:32px;border-radius:50%;background:var(--accentSoft);border:1.5px solid var(--accent);color:var(--accent2);font:700 15px/1 var(--font-head);display:flex;align-items:center;justify-content:center}
.how-row .tt{flex:1;font-size:17px;font-weight:700;line-height:1.25}
.how-row .tt small{display:block;font-size:15px;font-weight:400;color:var(--sub);line-height:1.3;margin-top:1px}
.how-row .chev{flex:0 0 auto;color:var(--accent)}
.how-row:focus-visible{outline:3px solid var(--ink);outline-offset:2px;border-radius:8px}
.how-branch{display:flex;flex-direction:column;gap:4px;margin:0 0 4px 44px}
.how-branch .hb{display:flex;align-items:center;gap:7px;font-size:15px;line-height:1.3;padding:4px 10px;border-radius:8px;width:fit-content}
.how-branch .hb b{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;font-size:12px;color:#fff}
.how-branch .hb-yes{background:#e6f4ea;color:#14532d}
.how-branch .hb-yes b{background:#1e7a46}
.how-branch .hb-no{background:#fdecea;color:#7f1d1d}
.how-branch .hb-no b{background:#c0392b}
@media (max-height:700px){ .how-row{padding:3px 2px} .how-row .tt small{line-height:1.25} .how-branch{gap:3px} .how-branch .hb{padding:3px 9px} }
'''
rep('@media print{', css + '@media print{')
rep('@media print{', '@media print{\n  .how-flow li::before{display:none!important}\n  .how-row .chev{display:none!important}')

# --- version ---
rep('Carer role v2.51', 'Carer role v2.52'); rep('Version 2.51 iPhone', 'Version 2.52 iPhone')
rep('<div>Version 2.51</div>', '<div>Version 2.52</div>'); rep('>2.51 – REVIEW DRAFT', '>2.52 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.49</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.51</span>', '<div class="rr"><span class="rv">2.52</span><span class="rd">16 Nov 2026</span><p>New page: How this guide works</p></div>\n<div class="rr"><span class="rv">2.51</span>')
open(dst, 'w', encoding='utf-8').write(s)
print('pages', total, 'written', dst)
