"""Guide 3.24 (from 3.23) – TRIAL (/preview/ only). David, 21 Nov: Contents was out of order. The pages run
7 Contact & support -> Accessibility -> About this guide, but Contents listed About this guide (8) before
Accessibility.
 - Contents: 7 Contact & support, then Accessibility (its icon), then About this guide with an open-book icon
   instead of the number 8.
 - About this guide is no longer numbered elsewhere either: page strips say "About this guide" (was
   "Section 8 · About this guide") and its title box shows the book icon instead of 8.
usage: python3 make324.py v3.23.html v3.24.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

BOOK = ('<svg aria-hidden="true" viewBox="0 0 20 20" width="17" height="17"><path d="M10 5.2C8.4 3.9 6 3.4 2.8 3.6v11.6c3.2-.2 5.6.3 7.2 1.6 1.6-1.3 4-1.8 7.2-1.6V3.6c-3.2-.2-5.6.3-7.2 1.6z" '
        'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M10 5.2v11.6" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>')

# 1. Contents: Accessibility before About this guide, which gets the book icon
m = re.search(r'(<div class="toc-g">)(<a class="toc-row" href="#s6"><span class="gb">8</span>.*?</a>)\n(<a class="toc-row toc-a11y" href="#a11y">.*?</a>)(</div>)', s, re.S)
assert m
about = m.group(2).replace('<span class="gb">8</span>', '<span class="gb" aria-hidden="true">' + BOOK + '</span>')
s = s.replace(m.group(0), m.group(1) + m.group(3) + '\n' + about + m.group(4))

# 2. no "Section 8" label on its pages
rep('Section 8 · About this guide', 'About this guide', 16)
rep('<section class="screen" id="s6" data-sec="About this guide" data-title="About this guide" aria-label="Section 8">',
    '<section class="screen" id="s6" data-sec="About this guide" data-title="About this guide" aria-label="About this guide">')
rep('<h2 class="h2 tp-h" tabindex="-1">About this guide</h2><span class="tp-n" aria-hidden="true">8</span>',
    '<h2 class="h2 tp-h" tabindex="-1">About this guide</h2><span class="tp-n tp-ico" aria-hidden="true">' + BOOK.replace('width="17" height="17"', 'width="44" height="44"') + '</span>')
CSS = """/* 3.24 About this guide: icon instead of a section number */
#app .tp-n.tp-ico{display:flex;align-items:center;justify-content:center}
#app .tp-n.tp-ico svg{width:44px;height:44px}
"""
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:')
_css = s[:s.index('@media print{')]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

rep('Carer role v3.23', 'Carer role v3.24'); rep('Version 3.23 iPhone', 'Version 3.24 iPhone')
rep('>3.23 – REVIEW DRAFT', '>3.24 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.23</span>', '<span class="cv-ver">Version 3.24</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.19</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.23</span>', '<div class="rr"><span class="rv">3.24</span><span class="rd">21 Nov 2026</span><p>Contents in page order: Accessibility, then About this guide</p></div>\n<div class="rr"><span class="rv">3.23</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
