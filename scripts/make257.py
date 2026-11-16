"""Guide 2.57 (from 2.56).
- NHS login Support Team (s5-2), NHS login help links:
  "What is NHS login / Set up an NHS login account" -> "Set up an NHS login account"
  "Contact the NHS login Support Team"              -> "Contact NHS login support"
  "Change your email, mobile number or password"    -> "Change contact details"
  (the same links elsewhere in Troubleshooting are left as they are; those pages are being redone)
- I have not received an Activation Link (s4-activation), "What should I check?", third point:
  "If you cannot find the link, or it does not open, contact your Health Visiting team."
  -> "If you cannot find the link, contact your Health Visiting team."
usage: python3 make257.py v2.56.html v2.57.html
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

edit('s5-2', '<strong>What is NHS login / Set up an NHS login account</strong>', '<strong>Set up an NHS login account</strong>')
edit('s5-2', '<strong>Contact the NHS login Support Team</strong>', '<strong>Contact NHS login support</strong>')
edit('s5-2', '<strong>Change your email, mobile number or password</strong>', '<strong>Change contact details</strong>')
edit('s4-activation', '<li>If you cannot find the link, or it does not open, contact your Health Visiting team.</li>',
     '<li>If you cannot find the link, contact your Health Visiting team.</li>')

# ---------------------------------------------------------------- version
rep('Carer role v2.56', 'Carer role v2.57'); rep('Version 2.56 iPhone', 'Version 2.57 iPhone')
rep('<div>Version 2.56</div>', '<div>Version 2.57</div>'); rep('>2.56 – REVIEW DRAFT', '>2.57 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.54</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.56</span>', '<div class="rr"><span class="rv">2.57</span><span class="rd">16 Nov 2026</span><p>Shorter NHS login help links; Activation Link check wording</p></div>\n<div class="rr"><span class="rv">2.56</span>')
open(dst, 'w', encoding='utf-8').write(s)
print('written', dst)
