"""Guide 3.62 (from trial 3.61) – TRIAL. David, 23 Nov:
Troubleshooting help pages
 - "Who will be set up with an account" (s4-who): Still stuck? removed;
 - "Only the account holder can access" (s4-2): calm line now "Here is how it works.";
 - "Partner's details used" (s4-1b): Still stuck? removed.
Troubleshooter questions 1-4 (ts1, ts1b, ts2, ts3) laid out like the help pages:
 - "Here is how it works." line, then an information card in labelled blocks
   (what you need to know + who can help), then the question;
 - the reply after Yes / No now says what that answer means (plus the existing help link);
 - question 4 titled "Can you sign in to NHS login?" (was "Do you have NHS login?"),
   also in the start page list and on the results page; its subheading removed.
usage: python3 make362.py v3.61.html v3.62.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def sec(i):
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % i, s, re.S); assert m, i; return m
def in_sec(i, a, b, n=1):
    global s
    m = sec(i); blk = m.group(0); assert blk.count(a) == n, (i, a[:80], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

# ---- help pages
in_sec('s4-who', re.search(r'<div class="stuck fit-opt2">.*?</div>\n', sec('s4-who').group(0), re.S).group(0), '')
in_sec('s4-1b', re.search(r'<div class="stuck">.*?</div>\n', sec('s4-1b').group(0), re.S).group(0), '')
in_sec('s4-2', '</span>Here is what to do instead.</p>', '</span>Here is how it works.</p>')

# ---- troubleshooter questions 1-4
CALM = re.search(r'<p class="calm">.*?</p>', sec('s4-who').group(0), re.S).group(0)
assert 'Here is how it works.' in CALM
def card(rows):
    out = []
    for kind, label, body in rows:
        ic = {'info': '<span class="abc-ic ic-info" aria-hidden="true">i</span>',
              'who': '<span class="abc-ic ic-who who-nhs" aria-hidden="true"></span>'}[kind]
        out.append('<div class="abc-row">%s<div><p class="abc-k">%s</p>%s</div></div>' % (ic, label, body))
    return CALM + '<div class="abc ts-card">' + ''.join(out) + '</div>'
HV = ('who', 'Who can help', '<p><strong>Your Health Visiting team</strong></p>')
NHS = ('who', 'Who can help', '<p><strong>NHS login Support team</strong></p>')
info = {
 'ts1': card([('info', 'Who it is for', '<p>Your Health Visiting team sets up a GM Early Years App account for the <strong>child’s mother or primary carer</strong>.</p><p class="abc-sub">In this guide, we call this person the <strong>account holder</strong>.</p>'), HV]),
 'ts1b': card([('info', 'Who can access it', '<p>Only the <strong>account holder</strong> (the child’s mother or primary carer) can access the GM Early Years App account that has been set up for them.</p>'), HV]),
 'ts2': card([('info', 'What you need', '<p>You need your own <strong>NHS login</strong> account to use the GM Early Years App.</p><p class="abc-sub">NHS login confirms who you are.</p>'), NHS]),
 'ts3': card([('info', 'How you sign in', '<p>You sign in to the GM Early Years App with the <strong>same email address and password</strong> as your NHS login account.</p>'), NHS]),
}
for i, html in info.items():
    m = sec(i); blk = m.group(0)
    old = re.search(r'<div class="ts-info">.*?</div>\n<div class="ts-qa">', blk, re.S).group(0)
    blk = blk.replace(old, '<div class="ts-info">' + html + '</div>\n<div class="ts-qa">')
    s = s[:m.start()] + blk + s[m.end():]

# replies
in_sec('ts1', '<p class="ok-h">Yes, the child’s mother or primary carer</p></div>',
       '<p class="ok-h">That’s right</p><p class="ok-more">The account is for the child’s mother or primary carer – the account holder.</p></div>')
in_sec('ts1', '<p class="ok-h">Please see <a class="msg-link" href="#s4-who">Who will be set up with an account</a> for more information.</p></div>',
       '<p class="ok-h">That’s OK</p><p class="ok-more">The account is only ever set up for the child’s mother or primary carer. See <a class="msg-link" href="#s4-who">Who will be set up with an account</a> for more information.</p></div>')
in_sec('ts1b', '<p class="ok-h">Yes, the child’s mother or primary carer</p></div>',
       '<p class="ok-h">That’s right</p><p class="ok-more">Only the account holder can sign in to the account.</p></div>')
in_sec('ts1b', '<p class="ok-h">See <a class="msg-link" href="#s4-2">Only the account holder can access</a> for help.</p></div>',
       '<p class="ok-h">That’s OK</p><p class="ok-more">Nobody else can sign in to the account holder’s account. See <a class="msg-link" href="#s4-2">Only the account holder can access</a> for more information.</p></div>')
in_sec('ts2', '<p class="ok-h">You have an NHS login account</p></div>',
       '<p class="ok-h">You have an NHS login account</p><p class="ok-more">You will use it to sign in to the GM Early Years App.</p></div>')
in_sec('ts2', '<h3>You need an NHS login account first</h3></div><p class="ok-more">See',
       '<h3>You need an NHS login account first</h3></div><p class="ok-more">You cannot use the GM Early Years App without one. See')
in_sec('ts3', '<p class="ok-h">You can sign in to NHS login</p></div>',
       '<p class="ok-h">You can sign in to NHS login</p><p class="ok-more">Use the same email address and password for the GM Early Years App.</p></div>')
in_sec('ts3', '<h3>You need to sign in to NHS login first</h3></div><p class="ok-more">See',
       '<h3>You need to sign in to NHS login first</h3></div><p class="ok-more">The NHS login Support team can help you get back in. See')

# question 4 title
T4 = 'Can you sign in to NHS login?'
rep('data-title="Troubleshooter · Do you have NHS login?"', 'data-title="Troubleshooter · %s"' % T4)
rep('<span class="vh">Question 4 of 6: </span>Do you have NHS login?</h2>', '<span class="vh">Question 4 of 6: </span>%s</h2>' % T4)
rep('<span aria-hidden="true">4</span>Do you have NHS login?</li>', '<span aria-hidden="true">4</span>%s</li>' % T4)
in_sec('tsum', '<p class="sum-l">Signing in to NHS login</p>', '<p class="sum-l">%s</p>' % T4, 3)

# styles
CSS = '''/* 3.62 troubleshooter questions 1-4: information card like the help pages */
#app :is(#ts1,#ts1b,#ts2,#ts3) .ts-info .calm{margin:0 0 8px!important}
#app .screen .ts-card .abc-row:nth-child(1){border-left-color:#005eb8!important;background:#eef4fb!important}
#app .screen .ts-card .abc-row:nth-child(2){border-left-color:#768692!important;background:var(--surface)!important}
#app .screen .ts-card .abc-ic.ic-info{background:#005eb8!important}
#app .screen .ts-card .abc-row:last-child{margin-bottom:0}
#app :is(#ts1,#ts1b) .ans-msg>p.ok-more{display:block!important;font-size:16px;line-height:1.3;margin:3px 0 0 38px}
#app :is(#ts1,#ts1b,#ts2,#ts3) .ans-msg .ok-more .msg-link{font-weight:700}
#app :is(#ts1,#ts1b,#ts2,#ts3) .ans-msg.ok:not(.stop-msg)>p.ok-more{margin-left:0!important}
'''
rep('/* 2.95 A. Troubleshooting help pages as three blocks */', CSS + '/* 2.95 A. Troubleshooting help pages as three blocks */')

# version
rep('Carer role v3.61', 'Carer role v3.62'); rep('Version 3.61 iPhone', 'Version 3.62 iPhone')
rep('>3.61 – REVIEW DRAFT', '>3.62 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.61</span>', '<span class="cv-ver">Version 3.62</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.57</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.61</span>', '<div class="rr"><span class="rv">3.62</span><span class="rd">23 Nov 2026</span><p>Troubleshooter questions 1–4 laid out like the help pages; replies explain each answer</p></div>\n<div class="rr"><span class="rv">3.61</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
