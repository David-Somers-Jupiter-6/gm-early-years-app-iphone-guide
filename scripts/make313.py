"""Guide 3.13 (from 3.12) – LIVE. David, 20 Nov: in Troubleshooting > GM Early Years App issues, each choice is a
separate topic. Finishing a topic now goes back to the GM Early Years App issues menu instead of running on into the
next topic.
 - Last page of each topic: Next becomes "Done" and goes to the menu (#s4-gm)
     How to install the App      inst-7-tip       (was: Add to Home Screen)
     Add to Home Screen          a2hs             (was: Activation Link issues)
     Activation Link issues      s4-activation-2  (was: Common sign-in problems)
 - First page of each topic: Back goes to the menu (#s4-gm)
     a2hs (was: last install page), s4-activation (was: Add to Home Screen); inst already did
 - Menus go Back to the Troubleshooting menu (#s4): s4-gm (was: My name has changed),
   s4-reasons (was: Activation Link issues)
Swipe and the arrow keys follow these links, so they change too.
usage: python3 make313.py v3.12.html v3.13.html"""
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

def set_nav(pid, back=None, nxt=None, label=None, aria=None):
    global s
    m = page(pid); blk = m.group(0)
    if back:
        blk, n = re.subn(r'(<a class="nav-btn nav-back[^"]*" href="#)[^"]+(")', r'\g<1>%s\2' % back, blk)
        assert n == 1, (pid, 'back')
    if nxt:
        blk, n = re.subn(r'<a class="nav-btn nav-next([^"]*)" href="#[^"]+"><span>[^<]*</span>',
                         lambda g: '<a class="nav-btn nav-next%s" href="#%s"%s><span>%s</span>' % (
                             g.group(1), nxt, (' aria-label="%s"' % aria) if aria else '', label or 'Next'), blk)
        assert n == 1, (pid, 'next')
    s = s[:m.start()] + blk + s[m.end():]

DONE = 'Done – back to GM Early Years App issues'
for pid in ('inst-7-tip', 'a2hs', 's4-activation-2'):
    set_nav(pid, nxt='s4-gm', label='Done', aria=DONE)
for pid in ('a2hs', 's4-activation'):
    set_nav(pid, back='s4-gm')
for pid in ('s4-gm', 's4-reasons'):
    set_nav(pid, back='s4')

rep('Carer role v3.12', 'Carer role v3.13'); rep('Version 3.12 iPhone', 'Version 3.13 iPhone')
rep('>3.12 – REVIEW DRAFT', '>3.13 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.12</span>', '<span class="cv-ver">Version 3.13</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.10</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.12</span>', '<div class="rr"><span class="rv">3.13</span><span class="rd">20 Nov 2026</span><p>GM Early Years App issues: finishing a topic goes back to its menu</p></div>\n<div class="rr"><span class="rv">3.12</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
