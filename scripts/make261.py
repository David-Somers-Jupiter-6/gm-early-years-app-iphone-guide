"""Guide 2.61 (from 2.60).
- Section 3 Signing in, Step 5 (page 6 of 18, Part 2 of 3 · NHS login): title
  "Enter your email and password" -> "Enter your credentials" (David).
  Troubleshooting Step C and its Helpful tip keep "Enter your email and password".
- Section 3 titles (David, 16 Nov):
  page 7  Step 6   "Get your NHS login security code"   -> "Enter the security code"
  page 8  Step 7   "Enter your NHS login security code" -> "Enter security code"
  page 12 Step 11  "Get your App verification code"     -> "App verification code"
  page 13 Step 11 Helpful tip (same title)              -> "App verification code"
  page 14 Step 12  "Enter your App verification code"   -> "App verification code"
usage: python3 make261.py v2.60.html v2.61.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def edit(pid, a, b, n=1):
    global s
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

edit('step-5', 'data-title="Step 5 · Enter your email and password"', 'data-title="Step 5 · Enter your credentials"')
edit('step-5', '<span class="vh">Step 5 of 15: </span>Enter your email and password</h2>', '<span class="vh">Step 5 of 15: </span>Enter your credentials</h2>')

def title(pid, vh, old, new, data=True):
    if data: edit(pid, 'data-title="%s · %s"' % (vh.split(' of ')[0].replace('Helpful tip – ', ''), old), 'data-title="%s · %s"' % (vh.split(' of ')[0], new))
    edit(pid, '<span class="vh">%s: </span>%s</h2>' % (vh, old), '<span class="vh">%s: </span>%s</h2>' % (vh, new))
title('step-6', 'Step 6 of 15', 'Get your NHS login security code', 'Enter the security code')
title('step-7', 'Step 7 of 15', 'Enter your NHS login security code', 'Enter security code')
title('step-11', 'Step 11 of 15', 'Get your App verification code', 'App verification code')
title('step-11-tip', 'Helpful tip – Step 11 of 15', 'Get your App verification code', 'App verification code', data=False)
title('step-12', 'Step 12 of 15', 'Enter your App verification code', 'App verification code')

rep('Carer role v2.60', 'Carer role v2.61'); rep('Version 2.60 iPhone', 'Version 2.61 iPhone')
rep('<div>Version 2.60</div>', '<div>Version 2.61</div>'); rep('>2.60 – REVIEW DRAFT', '>2.61 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.58</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.60</span>', '<div class="rr"><span class="rv">2.61</span><span class="rd">16 Nov 2026</span><p>Signing in: new titles for Steps 5, 6, 7, 11 and 12</p></div>\n<div class="rr"><span class="rv">2.60</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
