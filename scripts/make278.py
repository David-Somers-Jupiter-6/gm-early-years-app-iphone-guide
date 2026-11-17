"""Guide 2.78 (from 2.77). "Cannot get into your email" follows NHS login's own advice (David, 17 Nov).
NHS login Help (manage/emailaddresses, error-messages-support): you can only change your NHS login email in
Login and security settings after signing in. If you cannot access the email address, you need to create a new
NHS login with an email address you can access; choose "Continue with my new account"; once ID checks are passed
NHS login deletes the old account and the records move to the new one. The old step "Update your email with
NHS login" only works for someone who can still sign in.
usage: python3 make278.py v2.77.html v2.78.html
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
edit('s4-email', '<ol class="abc-steps"><li>Update your email with NHS login.</li><li>Ask your Health Visiting team to update your App account.</li></ol>',
     '<ol class="abc-steps"><li>Set up a new NHS login with an email you can open.</li><li>Ask your Health Visiting team to update your App account.</li></ol>')
# iPhone SE in Safari: the grey bracketed note slightly smaller so the page fits
rep('@media print{', '@media (max-height:600px){#app #s4-email .abc-row p.abc-sub{font-size:14px!important;line-height:1.25!important}#app #s4-email .abc-links .abc-btn{padding:4px 0!important}}\n@media print{')
edit('s4-email', '<strong>Email address help</strong>', '<strong>Lost access to your email</strong>')
rep('Carer role v2.77', 'Carer role v2.78'); rep('Version 2.77 iPhone', 'Version 2.78 iPhone')
rep('<div>Version 2.77</div>', '<div>Version 2.78</div>'); rep('>2.77 – REVIEW DRAFT', '>2.78 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.75</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.77</span>', '<div class="rr"><span class="rv">2.78</span><span class="rd">17 Nov 2026</span><p>Cannot get into your email: follows NHS login&#8217;s advice to create a new NHS login</p></div>\n<div class="rr"><span class="rv">2.77</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
