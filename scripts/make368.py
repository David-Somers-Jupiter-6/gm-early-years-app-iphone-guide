"""Guide 3.68 (from trial 3.67) – TRIAL. David, 23 Nov, question 1 (About your account), No reply:
 - only the NHS logo, then WHO CAN HELP and "Contact Your Health Visiting team" (link to Contact your Health Visiting team),
   so the reply is about as short as the Yes reply and the page fits on more iPhones.
usage: python3 make368.py v3.67.html v3.68.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def in_sec(i, a, b, n=1):
    global s
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % i, s, re.S); blk = m.group(0)
    assert blk.count(a) == n, (i, a[:80], blk.count(a)); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
in_sec('ts1', '<div class="ans-msg msg-no ok soft" role="status"><span class="ok-ico" aria-hidden="true">i</span><p class="ok-more">The account is only ever set up for the child’s mother or primary carer.</p><p class="ok-more ts-help"><span class="abc-ic ic-who who-nhs ts-hi" aria-hidden="true"></span><span class="th-t"><span class="th-k">Who can help</span><strong>Your Health Visiting team</strong></span></p></div>',
       '<div class="ans-msg msg-no ok soft ts-noreply" role="status"><p class="ok-more ts-help"><span class="abc-ic ic-who who-nhs ts-hi" aria-hidden="true"></span><span class="th-t"><span class="th-k">Who can help</span><span>Contact <a class="msg-link" href="#hv">Your Health Visiting team</a></span></span></p></div>')
CSS = '''/* 3.68 question 1: No reply is the Who can help line only */
#app #ts1 .ts-replies>.ans-msg.ts-noreply>p.ok-more.ts-help{margin:0 0 0 -41px!important;padding:0!important;border-top:0!important}
#app #ts1 .ts-noreply .msg-link{font-weight:700}
'''
rep('/* 2.95 A. Troubleshooting help pages as three blocks */', CSS + '/* 2.95 A. Troubleshooting help pages as three blocks */')
rep('Carer role v3.67', 'Carer role v3.68'); rep('Version 3.67 iPhone', 'Version 3.68 iPhone')
rep('>3.67 – REVIEW DRAFT', '>3.68 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.67</span>', '<span class="cv-ver">Version 3.68</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.63</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.67</span>', '<div class="rr"><span class="rv">3.68</span><span class="rd">23 Nov 2026</span><p>Question 1: No reply shortened to Who can help</p></div>\n<div class="rr"><span class="rv">3.67</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
