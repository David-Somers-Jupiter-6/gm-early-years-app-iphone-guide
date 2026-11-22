"""Guide 3.49 (from trial 3.48) – TRIAL. David, 22 Nov: Troubleshooter review fixes (agreed from mock-ups):
 - Your results: "All six checks are done" (was seven); Yes lines match the questions; "you" wording.
 - Questions 3 and 4 use "you" (Do you have an NHS login account? / Can you sign in to NHS login?).
 - Question 4 explains: "You sign in to the App with the same email address and password as your NHS login."
 - Every No on questions 3-6 says what it means and links straight to its help page ("See … for help.").
usage: python3 make349.py v3.48.html v3.49.html"""
import sys
import re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def edit(pid, a, b):
    global s
    m = re.search(r'<section class="screen" id="%s".*?</section>' % pid, s, re.S); blk = m.group(0)
    assert blk.count(a) == 1, (pid, a[:70], blk.count(a)); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
MUM = 'child’s mother or primary carer'
# 1. results count
edit('tsum', 'All seven checks are done', 'All six checks are done')
# 2 + 3. results wording
for a, b in [('That is clear', 'The %s' % MUM), ('You are the account holder', 'Only the %s' % MUM),
             ('The account holder has one', 'You have an NHS login account'), ('The account holder needs one', 'You need an NHS login account'),
             ('They can sign in', 'You can sign in'), ('They cannot sign in yet', 'You cannot sign in yet')]:
    edit('tsum', '<p class="sum-s">%s</p>' % a, '<p class="sum-s">%s</p>' % b)
# 3. "you" on questions 3 and 4
edit('ts2', '<p class="q-why">The account holder signs in to the GM Early Years App with their own <strong>NHS login</strong> account.</p>',
            '<p class="q-why">You sign in to the GM Early Years App with your own <strong>NHS login</strong> account.</p>')
edit('ts2', 'Does the child’s mother or primary carer have an NHS login account?', 'Do you have an NHS login account?')
edit('ts2', '<span>Yes, they have NHS login</span>', '<span>Yes, I have NHS login</span>')
edit('ts2', '<p class="ok-h">The account holder has an NHS login account</p>', '<p class="ok-h">You have an NHS login account</p>')
edit('ts3', 'Can the child’s mother or primary carer sign in to NHS login?', 'Can you sign in to NHS login?')
edit('ts3', '<span>Yes, they can sign in</span>', '<span>Yes, I can sign in</span>')
edit('ts3', '<span>No, they cannot sign in</span>', '<span>No, I cannot sign in</span>')
edit('ts3', '<p class="ok-h">They can sign in to NHS login</p>', '<p class="ok-h">You can sign in to NHS login</p>')
# 5. which details to sign in with
edit('ts3', '<p class="q-why"><strong>NHS login</strong> is used to access the GM Early Years App account.</p>',
            '<p class="q-why">You sign in to the App with the <strong>same email address and password</strong> as your NHS login.</p>')
# 6 + 7. every No: what it means, and a direct link to help
def no(pid, old_h, head, href, name):
    m = re.search(r'<section class="screen" id="%s".*?</section>' % pid, s, re.S); blk = m.group(0)
    mm = re.search(r'(<div class="ans-msg msg-no amber stop-msg" role="status"><div class="stop-head">.*?)<h3>%s</h3></div>.*?</div>' % re.escape(old_h), blk, re.S)
    assert mm, pid
    new = mm.group(1) + '<h3>%s</h3></div><p class="ok-more">See <a class="msg-link" href="#%s">%s</a> for help.</p></div>' % (head, href, name)
    globals()['s'] = s[:m.start()] + blk.replace(mm.group(0), new) + s[m.end():]
no('ts2', 'The account holder needs an NHS login account', 'You need an NHS login account first', 's4-setup', 'Set up NHS login')
no('ts3', 'NHS login needs to work first', 'You need to sign in to NHS login first', 's4-cannot', 'Cannot sign in')
no('ts4', 'Your details need to match', 'You cannot sign in until your details match', 's4-problems', 'Details do not match')
no('ts5', 'Your link has not arrived', 'You need your Activation Link to sign in', 's4-activation', 'Activation Link not received')
CSS = """/* 3.49 No messages on questions 3-6 show a help link */
#app :is(#ts2,#ts3,#ts4,#ts5) .ans-msg>p.ok-more{display:block!important;font-size:16px;line-height:1.3;margin:3px 0 0 38px}
#app :is(#ts2,#ts3,#ts4,#ts5) .msg-link{color:var(--nhs-blue,#005eb8);text-decoration:underline;text-underline-offset:2px;text-decoration-thickness:1.5px;font-weight:700}
"""
s = s.replace('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('Carer role v3.48', 'Carer role v3.49'); rep('Version 3.48 iPhone', 'Version 3.49 iPhone')
rep('>3.48 – REVIEW DRAFT', '>3.49 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.48</span>', '<span class="cv-ver">Version 3.49</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.44</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.48</span>', '<div class="rr"><span class="rv">3.49</span><span class="rd">22 Nov 2026</span><p>Troubleshooter review fixes: you wording, help links on every No</p></div>\n<div class="rr"><span class="rv">3.48</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
