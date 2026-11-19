"""Guide 3.00 (from 2.99). David, 19 Nov:
 - Troubleshooting > Still need help? (s4-help): headset icon in the title box, as on Contact & support > GMDP Support Team
 - Contents: new first row "Cover page" (goes to the front cover); "4 NHS login" row removed
 - "Your account details" (nhs) becomes page 2 of 2 of Section 3 · About your account; sections 5-9 renumbered 4-8
   (data-sec, strips, aria-labels, cross-references, CSS selectors, Contents numbers, roadmap numbers, faint title-box numbers);
   roadmap loses its "NHS login" chip; nhs loses its stage marker (stage marker = a section's first page only)
 - Title-box label ("Question 1 of 4", "Part 1 of 3 · Get started", "Step 11 · Helpful tip" ...) pinned in one place under the
   progress bar, the same place as "Stage N of 3" on a section's first page, so it no longer jumps when a title wraps to two lines
usage: python3 make300.py v2.99.html v3.00.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>' % re.escape(pid), s, re.S); assert m, pid; return m
def in_page(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0); assert blk.count(a) == n, (pid, a[:80], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

# 1. Still need help? title box icon (same markup as s5-gmdp; the .pbox.gm-icon CSS from 2.96 is generic)
icon = re.search(r'<span class="gm-eyi" aria-hidden="true">.*?</svg></span>', page('s5-gmdp').group(0), re.S).group(0)
in_page('s4-help', '<div class="pbox"><h2 class="h2" tabindex="-1">Still need help?</h2></div>',
        '<div class="pbox gm-icon">' + icon + '<h2 class="h2" tabindex="-1">Still need help?</h2></div>')

# 2. "Your account details" joins Section 3 · About your account (before the global renumber)
in_page('acct', '<span class="pos">Page 1 of 1</span>', '<span class="pos">Page 1 of 2</span>')
in_page('nhs', 'data-sec="Section 4 · NHS login"', 'data-sec="Section 3 · About your account"')
in_page('nhs', 'aria-label="Section 4: Your account details"', 'aria-label="Your account details"')
in_page('nhs', '<span>Section 4 · NHS login</span><span class="pos">Page 1 of 1</span>',
        '<span>Section 3 · About your account</span><span class="pos">Page 2 of 2</span>')
stg = re.search(r'<div class="pbox tp-stg"><div class="stg">.*?</div>(?=<h2)', page('nhs').group(0), re.S).group(0)
in_page('nhs', stg, '<div class="pbox">')
rep('/* 2.89 Section 4 page 1: worked example */', '/* 2.89 Section 3 page 2 (Your account details): worked example */')
assert not re.search(r'Section[  ]4', s), 'Section 4 still referenced'

# 3. Contents: Cover page first, NHS login row out, numbers 5-9 -> 4-8
rep('<a class="toc-row" href="#nhs"><span class="gb">4</span><span class="tt">NHS login</span>', '<a class="toc-row" href="#nhs" data-gone>')
s = re.sub(r'<a class="toc-row" href="#nhs" data-gone>.*?</a>\n', '', s, count=1, flags=re.S)
assert 'data-gone' not in s
for old, new, pid in [(5, 4, 's2'), (6, 5, 's3'), (7, 6, 's4'), (8, 7, 's5'), (9, 8, 's6')]:
    rep(f'<a class="toc-row" href="#{pid}"><span class="gb">{old}</span>', f'<a class="toc-row" href="#{pid}"><span class="gb">{new}</span>')
    in_page(pid, f'<span class="tp-n" aria-hidden="true">{old}</span>', f'<span class="tp-n" aria-hidden="true">{new}</span>')
DOC = ('<svg aria-hidden="true" viewBox="0 0 20 20" width="17" height="17"><path d="M5 2.8h7l3.2 3.2v11.2H5z" fill="none" stroke="currentColor" '
       'stroke-width="1.8" stroke-linejoin="round"/><path d="M12 2.8V6h3.2M7.6 10h4.8M7.6 13h4.8" fill="none" stroke="currentColor" '
       'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')
intro = re.search(r'<a class="toc-row" href="#intro">.*?</a>\n', s, re.S).group(0)
cover = (intro.replace('href="#intro"', 'href="#cover"').replace('<span class="gb" aria-hidden="true">i</span>', f'<span class="gb" aria-hidden="true">{DOC}</span>')
         .replace('<span class="tt">Introduction</span>', '<span class="tt">Cover page</span>'))
rep(intro, cover + intro)
toc = re.search(r'<nav aria-label="Contents" class="toc">.*?</nav>', s, re.S).group(0)
assert re.findall(r'href="#([^"]+)"', toc) == ['cover', 'intro', 'how', 'hv', 'acct', 's2', 's3', 's4', 's5', 's6', 'a11y'], toc

# 4. Roadmap: drop the NHS login chip, renumber the chips after it
rep('<a class="rm-chip" href="#nhs"><span class="rm-cn">4</span>NHS login</a>', '')
for old, new, pid in [(5, 4, 's2'), (6, 5, 's3'), (7, 6, 's4'), (8, 7, 's5')]:
    rep(f'<a class="rm-chip" href="#{pid}"><span class="rm-cn">{old}</span>', f'<a class="rm-chip" href="#{pid}"><span class="rm-cn">{new}</span>')
assert 'href="#nhs"' not in page('roadmap').group(0)

# 5. Global renumber "Section 5-9" -> "Section 4-8" in one pass (data-sec, strips, aria-labels, links, CSS selectors, comments)
before = len(re.findall(r'Section([  ])([5-9])', s))
s = re.sub(r'Section([  ])([5-9])', lambda m: 'Section' + m.group(1) + str(int(m.group(2)) - 1), s)
assert not re.search(r'Section[  ]9', s); print('renumbered', before)
for pid, sec in [('s2', 'Section 4 · Checklist'), ('s3', 'Section 5 · Signing in'), ('s4', 'Section 6 · Troubleshooting'), ('s5', 'Section 7 · Contact &amp; support'), ('s6', 'Section 8 · About this guide')]:
    assert f'data-sec="{sec}"' in page(pid).group(0), pid

# 6. Title-box label pinned under the progress bar (title boxes with a progress bar, 110 px boxes only; NHS login band boxes untouched)
K = '#app .screen:not(#contents) .pbox:not(.eyx):has(>.stepper)'
CSS = f'''/* 3.00 Label in the title box fixed under the progress bar (same place as "Stage N of 3"), so it does not move when a title wraps */
@media screen and (min-height:601px){{
{K}{{position:relative!important}}
{K}>.stepper{{position:absolute!important;top:10px;left:16px;right:16px;margin:0!important}}
{K}>.kicker{{position:absolute!important;top:20px;left:16px;right:16px;margin:0!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
}}
#app .screen:not(#contents) :is(.pbox,.tp-body).tp-stg>.stg{{left:16px}}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

# version
rep('Carer role v2.99', 'Carer role v3.00'); rep('Version 2.99 iPhone', 'Version 3.00 iPhone')
rep('<div>Version 2.99</div>', '<div>Version 3.00</div>'); rep('>2.99 – REVIEW DRAFT', '>3.00 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.97</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.99</span>', '<div class="rr"><span class="rv">3.00</span><span class="rd">19 Nov 2026</span><p>Account details moved into About your account; Cover page in Contents</p></div>\n<div class="rr"><span class="rv">2.99</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
