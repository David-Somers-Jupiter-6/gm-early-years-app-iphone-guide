"""Guide 2.58 (from 2.57): Option B title boxes - every title box the same height (110 px).
- .pbox (page title boxes) and .tp-card .tp-body (section title pages, team pages) are fixed
  at 110 px; the title sits at the bottom of the box; the progress bar stays at the top.
  Tighter top spacing (11 px) so a progress bar, a label and a two-line title fit.
  110 not 112 (the mockup): 2 px less lets "Cannot get into your email" and
  "Mobile number problems" fit on a 375 x 637 screen; no title box gets tighter than 8 px.
- Contents is the one exception: it keeps its shorter title box and the "Select Next" tip (David).
- Shorter titles so they fit the box (David, 16 Nov):
  Step H and its Note page: "Check your NHS account details"
      (was "Check your name, date of birth and NHS number")
  Step C and its Helpful tip page: "Enter your email and password"
      (was "Enter your email address and password")
  Step D Good to know page: "Security code page" (was "The security code page opens";
      Step D itself unchanged)
- Left as they are at 320 wide (David): How this guide works and Mobile number problems
  need a short scroll; "I have not received an Activation Link" is to be reworked later.
usage: python3 make258.py v2.57.html v2.58.html
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

# ---------------------------------------------------------------- titles
H_OLD, H_NEW = 'Check your name, date of birth and NHS number', 'Check your NHS account details'
edit('step-h', 'data-title="Step H · %s"' % H_OLD, 'data-title="Step H · %s"' % H_NEW)
edit('step-h', '<span class="vh">Step H: </span>%s</h2>' % H_OLD, '<span class="vh">Step H: </span>%s</h2>' % H_NEW)
edit('step-h-tip', '<span class="vh">Note – Step H: </span>%s</h2>' % H_OLD, '<span class="vh">Note – Step H: </span>%s</h2>' % H_NEW)

C_OLD, C_NEW = 'Enter your email address and password', 'Enter your email and password'
edit('step-c', 'data-title="Step C · Enter email and password"', 'data-title="Step C · %s"' % C_NEW)
edit('step-c', '<span class="vh">Step C: </span>%s</h2>' % C_OLD, '<span class="vh">Step C: </span>%s</h2>' % C_NEW)
edit('step-c-tip', '<span class="vh">Helpful tip – Step C: </span>%s</h2>' % C_OLD, '<span class="vh">Helpful tip – Step C: </span>%s</h2>' % C_NEW)

edit('step-d-tip', '<span class="vh">Good to know – Step D: </span>The security code page opens</h2>',
     '<span class="vh">Good to know – Step D: </span>Security code page</h2>')
assert s.count(H_OLD) == 0 and s.count(C_OLD) == 0

# ---------------------------------------------------------------- one title box height
CSS = ('/* 2.58 Option B: every title box the same height (Contents keeps its own) */\n'
 '#app .screen .pbox,#app .screen:not(#contents) .tp-card .tp-body{box-sizing:border-box!important;height:110px!important;min-height:110px!important;max-height:110px!important;display:flex!important;flex-direction:column!important;justify-content:flex-end!important;padding-top:11px!important}\n'
 '#app .screen:not(#contents) .tp-card{height:auto!important;min-height:0!important}\n'
 '#app .screen:not(#contents) .tp-card .tp-body{align-items:stretch}\n'
 '#app .screen .pbox .stepper{margin-top:0!important;margin-bottom:auto!important}\n'
 '#app .screen .pbox .kicker{margin-top:2px!important}\n')
rep('@media print{', CSS + '@media print{')

# ---------------------------------------------------------------- version
rep('Carer role v2.57', 'Carer role v2.58'); rep('Version 2.57 iPhone', 'Version 2.58 iPhone')
rep('<div>Version 2.57</div>', '<div>Version 2.58</div>'); rep('>2.57 – REVIEW DRAFT', '>2.58 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.55</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.57</span>', '<div class="rr"><span class="rv">2.58</span><span class="rd">16 Nov 2026</span><p>Title boxes the same height; shorter titles for Steps C and H and Step D Good to know</p></div>\n<div class="rr"><span class="rv">2.57</span>')
open(dst, 'w', encoding='utf-8').write(s)
print('written', dst)
