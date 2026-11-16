"""Guide 2.55 (from 2.54): every piece of text on Apple's recommended iPhone text sizes.

Apple's text styles (default Large setting): Large Title 34, Title 1 28, Title 2 22, Title 3 20,
Headline 17, Body 17, Callout 16, Subheadline 15, Footnote 13, Caption 1 12, Caption 2 11.

- Reading text, links in text, messages, search results, buttons and controls: Body 17
  (earlier versions shrank some of these to 15 or 16 to make pages fit).
- Page titles (21.5 / 23): Title 2 22. Cover title (36): Large Title 34. Headings in the page
  (16 / 18): Headline 17.
- Unchanged, already on the scale: the small capital labels (section line, "Question 1 of 4",
  labels, dates, "Tap to enlarge") at 11 to 13, the cover's subtitle line and bottom bar (15),
  and the numbers and ticks inside circles (icons, not reading text).
One block at the end of the styles, so it wins over every earlier size; pages that no longer
fit are found by the tests and fixed in later versions.
usage: python3 make255.py v2.54.html v2.55.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

A = '#app .screen'      # (1,1,0) + the rest: wins over every earlier page rule (#page .x …)
BODY = [
    # reading text
    'p.lead', 'p.info-lead', '.step-body p', '.step-body li', '.tip-page p', '.facts li', '.info p',
    '.rr p', '.hv-tips p', '.srch-status', '.srch-x', '.ans-msg p', '.ans-msg li', '.amber p', '.tip p',
    '.need-ans', '.how-branch .hb', '.how-branch .hb span', '.sp-link strong', '.q-why', '.q-hint',
    # buttons and controls
    '.nav-btn span', '.nav-btn', '.hv-seg label', '.hv-open', '.sum-help', '.tp-search span',
    '.hv-call', '.hv-call span', '.hv-sel select', '.srch-q',
]
HEAD17 = ['h3', '.stop-head h3', '.info h3', 'h3.h3', '.sp-h3']
css = ['/* 2.55 Apple text sizes everywhere (see make255.py). Last in the styles on purpose. */']
css.append(',\n'.join('%s %s' % (A, x) for x in BODY) + '{font-size:17px!important}')
css.append(',\n'.join('%s %s' % (A, x) for x in HEAD17) + '{font-size:17px!important}')
css.append('%s h2, %s .h2, %s .tp-h, %s .pbox h2{font-size:22px!important}' % (A, A, A, A))
css.append('%s .cover-panel h1{font-size:34px!important}' % A)
# text inside reading text takes the size of its sentence
css.append('%s p strong, %s p a, %s p b, %s p em, %s li strong, %s li a, %s .srch-x mark{font-size:inherit!important}' % ((A,) * 7))
# labels and the cover's small lines keep their Apple label sizes
css.append('%s .cover-panel .plat, %s .cover-bar div{font-size:15px!important}' % (A, A))
block = '\n'.join(css) + '\n'
rep('@media print{', block + '@media print{')

# ---------------------------------------------------------------- version
rep('Carer role v2.54', 'Carer role v2.55'); rep('Version 2.54 iPhone', 'Version 2.55 iPhone')
rep('<div>Version 2.54</div>', '<div>Version 2.55</div>'); rep('>2.54 – REVIEW DRAFT', '>2.55 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.52</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.54</span>', '<div class="rr"><span class="rv">2.55</span><span class="rd">16 Nov 2026</span><p>All text on Apple’s recommended sizes</p></div>\n<div class="rr"><span class="rv">2.54</span>')
open(dst, 'w', encoding='utf-8').write(s)
print('written', dst)
