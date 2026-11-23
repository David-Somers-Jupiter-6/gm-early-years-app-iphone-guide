"""Guide 3.69 (from trial 3.68) – TRIAL. David, 23 Nov, question 2 (Who will be able to access the account?)
laid out exactly like question 1:
 - Who can help window removed; question window straight under the information (no longer shares heights);
 - no space between the question and "Tap an answer, then tap Next.";
 - reply slot kept from the start, so nothing moves when an answer is tapped;
 - Yes (green tick): "Only the account holder can access the GM Early Years App account.";
 - No: NHS logo, WHO CAN HELP, "Contact Your Health Visiting team" (link to Contact your Health Visiting team);
 - reply icons in line with the answer circles, reply text in line with the answer text.
usage: python3 make369.py v3.68.html v3.69.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def sec(i):
    return re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % i, s, re.S)
def in_sec(i, a, b, n=1):
    global s
    m = sec(i); blk = m.group(0)
    assert blk.count(a) == n, (i, a[:80], blk.count(a)); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
YES = sys.argv[3] if len(sys.argv) > 3 else 'Only the account holder can access the GM Early Years App account.'
rep("var TSQ=['ts1b','ts2','ts3','ts4','ts5'];", "var TSQ=['ts2','ts3','ts4','ts5'];")
in_sec('ts1b', '<div class="abc-row"><span class="abc-ic ic-who who-nhs" aria-hidden="true"></span><div><p class="abc-k">Who can help</p><p><strong>Your Health Visiting team</strong></p></div></div>', '')
# replies: same as question 1
m = sec('ts1b'); blk = m.group(0)
a = blk.index('<p class="need-ans"'); z = blk.index('</div>\n</div>\n<input type="radio" class="nudge-t"')
blk = blk[:a] + '<div class="ts-replies">' + blk[a:z] + '</div>\n' + blk[z:]
s = s[:m.start()] + blk + s[m.end():]
in_sec('ts1b', '<p class="ok-h">That’s right</p><p class="ok-more">Only the account holder can sign in to the account.</p>',
       '<p class="ok-more">%s</p>' % YES)
in_sec('ts1b', '<div class="ans-msg msg-no ok soft" role="status"><span class="ok-ico" aria-hidden="true">i</span><p class="ok-h">That’s OK</p><p class="ok-more">Nobody else can sign in to the account holder’s account. See <a class="msg-link" href="#s4-2">Only the account holder can access</a> for more information.</p></div>',
       '<div class="ans-msg msg-no ok soft ts-noreply" role="status"><p class="ok-more ts-help"><span class="abc-ic ic-who who-nhs ts-hi" aria-hidden="true"></span><span class="th-t"><span class="th-k">Who can help</span><span>Contact <a class="msg-link" href="#hv">Your Health Visiting team</a></span></span></p></div>')
# styles: copy question 1's rules (3.66-3.68) for question 2, plus question 1's older reply padding (3.42/3.43)
a = s.index('/* 3.66 question 1:'); z = s.index('/* 2.95 A. Troubleshooting help pages as three blocks */')
q1 = s[a:z]
q2 = re.sub(r'#ts1(?=[ :.])', '#ts1b', q1)
q2 = q2.replace('/* 3.66 question 1:', '/* 3.69 question 2 copies question 1 (3.66-3.68):', 1)
q2 += ('#app #ts1b .ts-help .ts-hi{position:static!important}\n'
       '#app #ts1b .ts-replies>.ans-msg.ok{padding-top:5px!important;padding-bottom:5px!important;align-items:center}\n'
       '@media screen and (max-height:640px),screen and (max-width:345px){#app #ts1b .ts-replies>.ans-msg.msg-no.ok{padding-top:3px!important;padding-bottom:3px!important}}\n')
s = s[:z] + q2 + s[z:]
rep('Carer role v3.68', 'Carer role v3.69'); rep('Version 3.68 iPhone', 'Version 3.69 iPhone')
rep('>3.68 – REVIEW DRAFT', '>3.69 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.68</span>', '<span class="cv-ver">Version 3.69</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.64</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.68</span>', '<div class="rr"><span class="rv">3.69</span><span class="rd">23 Nov 2026</span><p>Question 2 laid out like question 1</p></div>\n<div class="rr"><span class="rv">3.68</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
