"""Guide 2.51 (from 2.50).
- New Section 6 · About this guide: a section title page (s6), Document control and Revision history.
- Section 5 · Contact & support keeps the help pages; Accessibility is its last page, with clearer wording.
- Contents: new rows for About this guide (6) and, at the end, Accessibility.
- Page counts, section lines, Back/Next links and the Contents counter updated (71 pages).
usage: python3 make251.py v2.50.html v2.51.html
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

# --- Section 6 title page, made from the Section 5 title page ---
s5 = page('s5').group(0)
nav = re.search(r'<nav class="bnav".*?</nav>', s5, re.S).group(0)
nav6 = nav.replace('href="#s4-help"', 'href="#a11y"', 1).replace('href="#s5-hv"', 'href="#doc-control"', 1)
assert nav6 != nav
s6 = ('<section class="screen" id="s6" data-sec="Section 6 · About this guide" data-title="About this guide" aria-label="Section 6">\n'
      '<div class="scroll">\n'
      '<div class="tp-card"><div class="tp-body"><h2 class="h2 tp-h" tabindex="-1">About this guide</h2><span class="tp-n" aria-hidden="true">6</span></div></div>\n'
      '<div class="strip" aria-hidden="true"><div class="strip-row"><span>Section 6 · About this guide</span><span class="pos">Page 1 of 3</span></div></div>\n'
      '<p class="lead">Information about this guide:</p>\n'
      '<nav aria-label="About this guide" class="toc toc-sm">\n'
      '<a class="toc-row" href="#doc-control"><span class="gb">1</span><span class="tt">Document control<small>Version, owner and review date</small></span>' + CHEV + '</a>\n'
      '<a class="toc-row" href="#revisions"><span class="gb">2</span><span class="tt">Revision history<small>Latest changes to this guide</small></span>' + CHEV + '</a>\n'
      '</nav>\n'
      '</div>\n' + nav6 + '\n</section>\n\n')
m = page('doc-control')
s = s[:m.start()] + s6 + s[m.start():]

# --- Section 5: the fourth row is Accessibility ---
edit('s5', '<a class="toc-row" href="#a11y"><span class="gb">4</span><span class="tt">About this guide<small>Accessibility, document control and revision history</small></span>',
           '<a class="toc-row" href="#a11y"><span class="gb">4</span><span class="tt">Accessibility<small>Large print, easy-read and other formats</small></span>')

# --- Accessibility wording; Next goes to Section 6 ---
edit('a11y', '<p>This guide is available in large print, easy-read and other formats or languages on request. Please contact the GMDP Support Team at <a href="mailto:gmdp.support@greatermanchester-ca.gov.uk">gmdp.support@greatermanchester-ca.gov.uk</a>.</p>',
             '<p>If this guide is hard to read or use, it is available in large print, easy-read and other formats or languages.</p><p>To ask for one, please contact the GMDP Support Team at <a href="mailto:gmdp.support@greatermanchester-ca.gov.uk">gmdp.support@greatermanchester-ca.gov.uk</a>.</p>')
edit('a11y', 'class="nav-btn nav-next" href="#doc-control"', 'class="nav-btn nav-next" href="#s6"')
edit('doc-control', 'class="nav-btn nav-back" href="#a11y"', 'class="nav-btn nav-back" href="#s6"')

# --- Section lines and page positions ---
for pid in ('doc-control', 'revisions'):
    edit(pid, 'data-sec="Section 5 · Contact &amp; support"', 'data-sec="Section 6 · About this guide"')
    edit(pid, '<span>Section 5 · Contact &amp; support</span>', '<span>Section 6 · About this guide</span>')
for pid, a, b in (('doc-control', 'Page 6 of 7', 'Page 2 of 3'), ('revisions', 'Page 7 of 7', 'Page 3 of 3'),
                  ('s5', 'Page 1 of 7', 'Page 1 of 5'), ('s5-hv', 'Page 2 of 7', 'Page 2 of 5'),
                  ('s5-2', 'Page 3 of 7', 'Page 3 of 5'), ('s5-gmdp', 'Page 4 of 7', 'Page 4 of 5'),
                  ('a11y', 'Page 5 of 7', 'Page 5 of 5')):
    edit(pid, '<span class="pos">%s</span>' % a, '<span class="pos">%s</span>' % b)

# --- Contents: About this guide, then Accessibility at the end ---
A11Y_ICON = ('<svg aria-hidden="true" viewBox="0 0 20 20" width="17" height="17"><circle cx="10" cy="3.9" r="1.8" fill="currentColor"/>'
             '<path d="M4 7.3l6 1.2 6-1.2M10 8.5v3.7M10 12.2l-2.7 4.8M10 12.2l2.7 4.8" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>')
row5 = re.search(r'<a class="toc-row" href="#s5"><span class="gb">5</span><span class="tt">Contact &amp; support</span><svg class="chev".*?</svg></a>\n', page('contents').group(0), re.S).group(0)
edit('contents', row5, row5
     + '<a class="toc-row" href="#s6"><span class="gb">6</span><span class="tt">About this guide</span>' + CHEV + '</a>\n'
     + '<a class="toc-row toc-a11y" href="#a11y"><span class="gb" aria-hidden="true">' + A11Y_ICON + '</span><span class="tt">Accessibility</span>' + CHEV + '</a>\n')

# --- Contents counter on every page (now 71) ---
ids = re.findall(r'<section class="screen[^"]*" id="([^"]+)"', s)
total = len(ids); assert total == 71, total
out = []; last = 0
for k, mm in enumerate(re.finditer(r'<section class="screen[^"]*" id="([^"]+)".*?</section>', s, re.S)):
    blk = mm.group(0)
    blk = re.sub(r'<span class="count">\d+ / \d+</span>', '<span class="count">%d / %d</span>' % (k + 1, total), blk)
    blk = re.sub(r'aria-label="Contents \(page \d+ of \d+\)"', 'aria-label="Contents (page %d of %d)"' % (k + 1, total), blk)
    out.append(s[last:mm.start()]); out.append(blk); last = mm.end()
s = ''.join(out) + s[last:]

css = '''/* 2.51 Section 6 About this guide; Contents has nine rows */
#s6 .toc-row .tt small{display:block;font-size:15px;font-weight:400;color:var(--sub);line-height:1.35;margin-top:1px}
#s6 .lead{margin:0 0 6px}
#a11y .tip p+p{margin-top:8px}
#contents .push{flex-basis:2px}
#contents .scroll .strip{margin:8px 0 6px}
#contents .nav-tip{margin-top:4px!important}
'''
rep('@media print{', css + '@media print{')

# --- version ---
rep('Carer role v2.50', 'Carer role v2.51'); rep('Version 2.50 iPhone', 'Version 2.51 iPhone')
rep('<div>Version 2.50</div>', '<div>Version 2.51</div>'); rep('>2.50 – REVIEW DRAFT', '>2.51 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.48</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.50</span>', '<div class="rr"><span class="rv">2.51</span><span class="rd">16 Nov 2026</span><p>New Section 6 About this guide; Accessibility in Contents and Contact &amp; support</p></div>\n<div class="rr"><span class="rv">2.50</span>')
open(dst, 'w', encoding='utf-8').write(s)
print('pages', total, 'written', dst)
