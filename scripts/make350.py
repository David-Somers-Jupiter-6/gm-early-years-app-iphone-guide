"""Guide 3.50 (from trial 3.49) – TRIAL. David, 22 Nov: in the Troubleshooter, always say which account is meant:
"the GM Early Years App account" or "your NHS login account" (never just "the App" or "the account").
usage: python3 make350.py v3.49.html v3.50.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def edit(pid, a, b, n=1):
    global s
    m = re.search(r'<section class="screen" id="%s".*?</section>' % pid, s, re.S); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:80], blk.count(a)); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
GM = 'GM Early Years App'
CHANGES = [
 ('ts', 'about your account. At the end', 'about your %s account. At the end' % GM),
 ('ts1', 'Your Health Visiting team sets up the account for the ', 'Your Health Visiting team sets up the %s account for the ' % GM),
 ('ts1b', 'Who will be able to access the account?</h3>', 'Who will be able to access the %s account?</h3>' % GM),
 ('ts1b', ' can access the account that has been set up for them.', ' can access the %s account that has been set up for them.' % GM),
 ('ts1b', 'A partner or family member cannot sign in to the account.', 'A partner or family member cannot sign in to the %s account.' % GM),
 ('ts1b', 'Is it clear only the child’s mother or primary carer can access it?', 'Is it clear only the child’s mother or primary carer can access the %s account?' % GM),
 ('ts3', 'Used to sign in to the App</h3>', 'Used to sign in to the %s</h3>' % GM),
 ('ts3', 'You sign in to the App with the <strong>same email address and password</strong> as your NHS login.',
         'You sign in to the %s with the <strong>same email address and password</strong> as your NHS login account.' % GM),
 ('ts3', 'Can you sign in to NHS login?</p>', 'Can you sign in to your NHS login account?</p>'),
 ('ts4', 'NHS login and the App</span>', 'NHS login and %s</span>' % GM),
 ('ts4', '<span class="vh">NHS login and the App: </span>', '<span class="vh">NHS login and %s: </span>' % GM),
 ('ts4', ' must be the same in NHS login and the App.', ' must be the same in your NHS login account and your %s account.' % GM),
 ('ts4', 'Are your details the same in both?</p>', 'Are your details the same in both accounts?</p>'),
 ('ts5', 'by text to the mobile number on your App account.', 'by text to the mobile number on your %s account.' % GM),
 ('ts5', '<h3>You need your Activation Link to sign in</h3>', '<h3>You need your Activation Link to sign in to the %s</h3>' % GM),
]
for pid, a, b in CHANGES: edit(pid, a, b)
rep('Carer role v3.49', 'Carer role v3.50'); rep('Version 3.49 iPhone', 'Version 3.50 iPhone')
rep('>3.49 – REVIEW DRAFT', '>3.50 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.49</span>', '<span class="cv-ver">Version 3.50</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.45</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.49</span>', '<div class="rr"><span class="rv">3.50</span><span class="rd">22 Nov 2026</span><p>Troubleshooter names the GM Early Years App account or NHS login account</p></div>\n<div class="rr"><span class="rv">3.49</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
